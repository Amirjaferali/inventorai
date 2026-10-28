# -*- coding: utf-8 -*-
"""FUNCTIONAL-NEED-TO-CAPABILITY-HANDOFF-01 — the read-only, provisional
functional-role projection and the original-statement source seam.

The fixture ``tests/fixtures/functional_handoff_cases_v1.json`` was written by a
separate agent from the role definitions only, without access to the
implementation, and is frozen by digest here. Precision is strict: no role may
be proposed that the fixture does not read as AFFIRMED, and no conflict may be
reported that it does not list. Recall is required only for the cases it marks
``must_recognize``. Synthetic data only.
"""
import hashlib
import html
import json
import os
import pickle
import re

import pytest

import web.app as webapp
from engine import functional_need_handoff as fh
from engine.semantic_registry import normalize_ar
from tests.test_cap12_form_mockup_advisory import (
    SESSION_STORE, _client_for, _new_client, _page, _snapshot)
from web import ui_text

FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures",
                       "functional_handoff_cases_v1.json")
FIXTURE_SHA256 = "670f37e40dd5ed72cd86cdf153db7491d49d88cbec47d7d965e2e453b7c1c9a6"

WATER_IDEA = ("I want a device that waters my plants automatically when the "
              "soil gets dry, but I don't know how it should work.")
FAN_IDEA = ("أبي مروحة تشتغل لحالها في غرفتي إذا صار الجو حار وتطفي "
            "نفسها بعدين بدون ما ألمسها")
FAN_IDEA_EN = "I want an automatic fan that turns on when my room gets hot."
SCREEN_IDEA = ("أريد حاملًا خشبيًا يرفع شاشة الحاسوب فوق مكتبي حتى تكون "
               "في مستوى النظر بدون براغي")


def _cases():
    with open(FIXTURE, encoding="utf-8") as handle:
        return json.load(handle)["cases"]


def _project(case):
    return fh.project_functional_roles(
        [(s["kind"], "s%d" % i, s["text"]) for i, s in enumerate(case["statements"])])


def _start(client, idea, domain):
    """Start a project through the real /start, answering the domain choice."""
    r = client.post("/start", data={"idea": idea, "domain_choice": domain,
                                    "domain_confirm": domain})
    assert r.status_code in (302, 303), r.status_code
    return r.headers["Location"].rsplit("/session/", 1)[-1]


def _section(body):
    start = body.find("data-functional-handoff")
    if start == -1:
        return None
    return body[start:body.index("</details>", start)]


# ==========================================================================
# 1. frozen independent fixture: precision, recall, conflicts, quotes
# ==========================================================================
def test_the_fixture_is_frozen():
    with open(FIXTURE, "rb") as handle:
        assert hashlib.sha256(handle.read()).hexdigest() == FIXTURE_SHA256
    cases = _cases()
    assert {c["lang"] for c in cases} == {"EN", "MSA", "GULF"}
    categories = {c["category"] for c in cases}
    for needed in ("core", "paraphrase", "unknown_method", "negation",
                   "without_scope", "different_object", "contradiction",
                   "hypothetical", "long_text", "diacritics"):
        assert needed in categories, needed


@pytest.mark.parametrize("case", _cases(), ids=lambda c: c["id"])
def test_no_role_is_proposed_that_the_inventor_did_not_affirm(case):
    projection = _project(case)
    affirmed = {(e["role"], e["object"]) for e in case["expected"]
                if e["polarity"] == "AFFIRMED"}
    for role in projection.roles:
        assert (role.role, role.object_key) in affirmed, (role.role, role.object_key)
        assert role.interpretation_status == "PROVISIONAL_READING"
    listed = {(c["role"], c["object"]) for c in case["conflicts"]}
    for role in projection.roles:
        if role.status == fh.CONFLICTING:
            assert (role.role, role.object_key) in listed


@pytest.mark.parametrize("case", [c for c in _cases() if c["must_recognize"]],
                         ids=lambda c: c["id"])
def test_plain_affirmed_roles_are_recognized(case):
    projection = _project(case)
    got = {(r.role, r.object_key): r for r in projection.roles}
    for e in case["expected"]:
        if e["polarity"] != "AFFIRMED":
            continue
        role = got[(e["role"], e["object"])]
        assert bool(role.method_uncertainties) == e["method_uncertain"]
    for c in case["conflicts"]:
        assert got[(c["role"], c["object"])].status == fh.CONFLICTING


@pytest.mark.parametrize("case", _cases(), ids=lambda c: c["id"])
def test_every_quote_is_an_exact_slice_of_its_source(case):
    texts = {"s%d" % i: s["text"] for i, s in enumerate(case["statements"])}
    projection = _project(case)
    quotes = [q for m in projection.mentions
              for q in (m.clause, m.trigger, m.method_uncertainty) if q]
    for q in quotes:
        assert texts[q.source_ref][q.start:q.end] == q.quote and q.quote


def test_offsets_survive_harakat_tatweel_and_decomposed_hamza():
    for text in ("أُرِيدُ جِهَازًا يَسْقِي النَّبَاتَاتِ",
                 "أريد مـــروحـة لغرفتي",
                 "أريد جهازا يسقي النباتات"):
        role = fh.project_functional_roles([("IDEA", "idea", text)]).roles[0]
        for q in role.groundings:
            assert text[q.start:q.end] == q.quote
    # the per-character normalization is the registry's own normalization
    for text in ("أُرِيدُ جِهَازًا يَسْقِي", "مـــروحة", "لا أعرف كيف"):
        normalized, index = fh._normalize_with_offsets(text)
        assert normalized == normalize_ar(text.lower())
        assert len(index) == len(normalized)


# ==========================================================================
# 2. semantic rules called out by the Lead
# ==========================================================================
@pytest.mark.parametrize("text,expected", [
    ("I want a plant waterer without a pump.", {("WATERING", "PLANTS")}),
    ("I want a pot that keeps my plants alive without watering.", set()),
    ("أريد جهازًا يسقي النباتات بدون مضخة", {("WATERING", "PLANTS")}),
    ("أريد أصيصًا يحافظ على النبات بدون سقي", set()),
    ("I want a cooling fan for my room that never stops.", set()),  # unsupported negation
    ("Would a gadget that waters the garden be useful?", set()),
    ("لو كان فيه جهاز يسقي الزرع", set()),
    ("I want a glass of water next to my plants.", set()),
    ("I'm a big fan of gardening and want to grow plants.", set()),
])
def test_positive_evidence_is_required(text, expected):
    got = {(r.role, r.object_key)
           for r in fh.project_functional_roles([("IDEA", "idea", text)]).roles}
    assert got == expected


# Reproducers from the independent technical review (all must not propose).
REVIEW_NOT_PROPOSED = (
    # unlisted "n't" forms and lexical negation
    "I didn't want a device that waters my plants",
    "I wouldn't want a device that waters my plants",
    "I shouldn't need a device that waters my plants",
    "It isn't a device that waters plants",
    "I refuse to build a device that waters my plants",
    "I want to avoid a device that waters my plants",
    "I want nothing that waters my plants",
    "Nobody wants a device that waters plants",
    "I want a system to stop watering my plants",
    "I need a device that prevents watering the plants when it rains",
    "أبي جهاز يوقف سقي الزرع",
    "أبي جهاز يمنع ري الحديقة لما تمطر",
    "أرفض جهازا يسقي النباتات",
    # Arabic negation joined to و or written fused with the want
    "عندي فكرة للحديقة ولا أريد جهازا يسقي النباتات",
    "فكرتي حلوة وما أبي جهاز يسقي الزرع",
    "أنا وما أبي مروحة للغرفة",
    "مابي جهاز يسقي الزرع",
    "ماابغى جهاز يسقي الزرع",
    # role word and object not related
    "I want a device that holds my phone near the screen",
    "I want a TV remote holder",
    "I want a device that raises the alarm when the screen is on",
    "I want to build a holder for my monitor cable",
    "I need a device to hold my coffee while I look at the screen",
    "I want to remove the stand from my monitor",
    "أريد جهازا يحمل هاتفي بجانب الشاشة",
    "أبي حامل للريموت حق التلفزيون",
    "أبي أسوي حامل للجوال جنب التلفزيون",
    "أبي جهاز يشيل الغبار عن الشاشة",
    "I need to stop my dog from drinking the water in the plant pot",
    # someone else's, past or replaced wants; descriptions of existing devices
    "Existing products include a system that waters plants, and mine is a lamp.",
    "My neighbour has a device that waters his garden",
    "يوجد في السوق جهاز يسقي النباتات",
    "My friend wants a device that waters my plants but I think it is silly",
    "صديقي يريد جهازا يسقي النباتات",
    "I used to want a device that waters my plants",
    "كنت أريد جهازا يسقي النباتات",
    "Instead of a device that waters my plants, I want a lamp",
    "بدل جهاز يسقي الزرع أبي مصباح",
    "I don't know why anyone would want a device that waters plants",
    # doubt about the want itself
    "I am not sure about a device that waters my plants",
    "I'm not sure about wanting a device that waters my plants",
    "لست متأكد من جهاز يسقي النباتات",
    "I have not decided on a device that waters my plants",
    # negation elsewhere in the sentence or right after it
    "I do not, ever, want a device that waters my plants",
    "I don't want this, a device that waters my plants",
    "لا أريد هذا، جهاز يسقي النباتات",
    "I want a device that waters my plants, NOT",
    "I want a device that waters my plants. Not really.",
    # monitoring is not watering
    "I want a device that tells me how much water my plants need",
    "I want a device to measure the water my plants got",
    # targeted re-verification: verbs that govern something other than the role
    "I want to quit watering my plants",
    "I want to cease watering the garden",
    "I want to skip watering my plants",
    "I want to give up watering my plants",
    "I want to forget about watering my plants",
    "أبي أوقف سقي الزرع",
    "أبي أبطل أسقي الزرع",
    "أريد أن أتوقف عن ري الحديقة",
    "أبي أترك سقي الزرع",
    "I want to get rid of the stand for my monitor",
    "I want to take down the stand for my monitor",
    "أبي أشيل حامل الشاشة",
    "I want to sell my monitor stand",
    "I want to paint the stand for my TV",
    "أبي أصلح حامل التلفزيون",
    "I want to support my TV channel",
    "I want to raise my TV budget",
    "I want a phone holder for my TV room",
    "ماني أبي جهاز يسقي الزرع",
    "I want to hold my laptop fan",
    "I want to fan the flames in my room",
    "I want a device that waters my plants. No, I mean the garden.",
    # second targeted re-verification: an EXISTING item changed or removed
    "I want the TV support to be removed",
    "I want the monitor stand gone",
    "I want the monitor stand taken away",
    "I want my TV stand replaced by a wall",
    "I want the fan in my room switched off forever",
    "I want the fan for my room turned off",
    "I want a device that waters my plants to be cancelled",
    "أبي حامل الشاشة يتشال",
    "أبي حامل التلفزيون ينشال من الغرفة",
    "أبي المروحة اللي في الغرفة تنطفي للأبد",
    "I want my TV stand painted",
    "I want the stand of my TV to be lower",
    # retraction in the next sentence; "water" as a noun after "and"
    "I want a fan for my room. Nope.",
    "I want a fan for my room. Scratch that.",
    "I want a fan for my room. Just kidding.",
    "أبي مروحة للغرفة. انسَ الموضوع.",
    "أبي مروحة للغرفة. أمزح.",
    "I want a pot and water for my plants",
    # "to be" after an existing item; the Arabic construct form
    "I want the TV stand to be gone",
    "I want the monitor stand to be away from the wall",
    "I want the monitor stand to be in the bin",
    "I want my TV stand to be someone else's",
    "I want the fan to be gone from my room",
    "أبي حامل الشاشة يروح",
    "أبي حامل الشاشة يختفي",
    "أبي حامل الشاشة أرميه",
    "أبي حامل الشاشة برا",
    "أبي حامل الشاشة في المخزن",
    "أبي مروحة الغرفة تختفي",
    "أبي مروحة الغرفة تطفي للأبد",
    "أبي حامل الشاشة اللي في الصالة يروح",
    "أبي مروحة الغرفة اللي فوق تروح",
    "أبي حامل التلفزيون اللي بالصالة برا البيت",
    "أبي حامل الشاشة اللي عندي أرميها",
    # a verb after the construct form moves the existing item
    "أبي مروحة الغرفة يرفعها العامل للسطح",
    "أبي حامل الشاشة يشيله أحد من هنا",
    "أبي حامل الشاشة تشيلها البلدية",
    "أبي حامل التلفزيون يرفعه أحد للمخزن",
    "أبي حامل الشاشة يحمله أخوي للسيارة",
    "أبي حامل التلفزيون اللي يشيلونه العمال",
)

#: Plain requests that must stay recognized under the stricter rules.
STILL_PROPOSED = (
    ("I want a device that waters my plants", "WATERING", "PLANTS"),
    ("I want to water my plants automatically", "WATERING", "PLANTS"),
    ("I want a device that waters my plants while I am away", "WATERING", "PLANTS"),
    ("I need a stand for my monitor", "SCREEN_SUPPORT", "SCREEN"),
    ("I want a monitor stand", "SCREEN_SUPPORT", "SCREEN"),
    ("I want a stand that holds my monitor", "SCREEN_SUPPORT", "SCREEN"),
    ("I want the stand to hold my monitor", "SCREEN_SUPPORT", "SCREEN"),
    ("I want an automatic fan that turns on when my room gets hot", "FAN", "ROOM"),
    ("I want a fan that turns on and off automatically in my room", "FAN", "ROOM"),
    ("أريد جهازا يسقي النباتات", "WATERING", "PLANTS"),
    ("أبي جهاز ذكي يسقي الزرع", "WATERING", "PLANTS"),
    ("أريد أن أسقي النباتات", "WATERING", "PLANTS"),
    ("أريد حاملًا خشبيًا يرفع شاشة الحاسوب", "SCREEN_SUPPORT", "SCREEN"),
    ("أبي مروحة تشتغل لحالها وتطفي نفسها", "FAN", "NONE"),
    ("أبي حامل الشاشة اللي يرفع الشاشة", "SCREEN_SUPPORT", "SCREEN"),
    ("أبي حامل للشاشة", "SCREEN_SUPPORT", "SCREEN"),
)


@pytest.mark.parametrize("text,role,obj", STILL_PROPOSED)
def test_plain_requests_stay_recognized(text, role, obj):
    roles = fh.project_functional_roles([("IDEA", "idea", text)]).roles
    assert [(r.role, r.object_key, r.status) for r in roles] == [(role, obj, fh.PROPOSED)]


@pytest.mark.parametrize("text", REVIEW_NOT_PROPOSED)
def test_review_reproducers_propose_nothing(text):
    assert fh.project_functional_roles([("IDEA", "idea", text)]).roles == ()


@pytest.mark.parametrize("idea,answer", [
    ("I want a fan for my room.", "Actually I don't want a fan at all."),
    ("أبي مروحة للغرفة", "ما أبي مروحة"),
    ("I want a device that waters my plants.", "I don't want it to water anything."),
])
def test_a_rejection_of_the_whole_role_is_disclosed(idea, answer):
    projection = fh.project_functional_roles(
        [("IDEA", "idea", idea), ("ANSWER", "rec_1", answer)])
    (role,) = projection.roles
    assert role.status == fh.PROPOSED and role.negations == ()
    assert [(q.source_ref, q.quote) for q in role.related_statements] == [
        ("rec_1", answer)]


def test_an_unclear_rejection_is_shown_beside_the_proposal():
    projection = fh.project_functional_roles([
        ("IDEA", "idea", "I want a device that waters my plants."),
        ("ANSWER", "rec_1", "Forget the watering, I just want a lamp.")])
    (role,) = projection.roles
    assert role.status == fh.PROPOSED
    assert [q.source_ref for q in role.related_statements] == ["rec_1"]


def test_a_long_statement_stays_fast():
    import time
    text = ("I want a device that waters my plants, and it is green. " * 2300)[:125000]
    started = time.perf_counter()
    projection = fh.project_functional_roles([("IDEA", "idea", text)])
    assert time.perf_counter() - started < 5
    assert projection.roles and projection.roles[0].role == "WATERING"


def test_unknown_method_attaches_to_an_affirmed_goal():
    role = fh.project_functional_roles([("IDEA", "idea", WATER_IDEA)]).roles[0]
    assert (role.role, role.status) == ("WATERING", fh.PROPOSED)
    assert [q.quote for q in role.method_uncertainties] == ["I don't know"]
    ar = "أريد جهازًا يسقي النباتات لكن لا أعرف كيف"
    role = fh.project_functional_roles([("IDEA", "idea", ar)]).roles[0]
    assert role.status == fh.PROPOSED and role.method_uncertainties


def test_contradictions_need_the_same_role_and_object():
    same = fh.project_functional_roles([
        ("IDEA", "idea", "I want a device that waters my plants."),
        ("ANSWER", "rec_1", "I don't want it to water the plants.")])
    assert [(r.role, r.object_key, r.status) for r in same.roles] == [
        ("WATERING", "PLANTS", fh.CONFLICTING)]
    assert same.roles[0].negations[0].source_ref == "rec_1"
    different = fh.project_functional_roles([
        ("IDEA", "idea", "I want a stand for my monitor."),
        ("ANSWER", "rec_1", "I don't want to hold the TV.")])
    assert [(r.role, r.object_key, r.status) for r in different.roles] == [
        ("SCREEN_SUPPORT", "SCREEN", fh.PROPOSED)]


def test_capability_references_exclude_cap12_and_therm01():
    refs = {ref for refs in fh.ROLE_CAPABILITY_REFERENCES.values() for ref in refs}
    assert refs == {fh.CAP13_CONDITIONAL_REACTIONS, fh.CAP09_EXPERIMENT_PLANNING}
    assert fh.ROLE_CAPABILITY_REFERENCES[fh.ROLE_SCREEN_SUPPORT] == (
        fh.CAP13_CONDITIONAL_REACTIONS,)
    source = open(fh.__file__, encoding="utf-8").read()
    imports = sorted(set(re.findall(r"^(?:from|import) ([\w.]+)", source, re.M)))
    assert imports == ["bisect", "dataclasses", "engine.progression_loop",
                       "engine.semantic_registry", "re", "unicodedata"]


def test_bad_input_never_raises():
    for value in (None, 5, [("IDEA",)], [("IDEA", "x", None)], [("IDEA", "x", "")]):
        assert fh.project_functional_roles(value).roles == ()


# ==========================================================================
# 3. the session page: three journeys
# ==========================================================================
def test_watering_journey(monkeypatch):
    c, _aid = _client_for("fh-water@example.com")
    sid = _start(c, WATER_IDEA, "electronics_electrical")
    section = _section(_page(c, sid))
    assert section is not None
    assert 'data-fh-role="WATERING"' in section and 'data-fh-object="PLANTS"' in section
    assert 'data-fh-status="PROPOSED"' in section
    assert "I want a device that waters my plants automatically when the soil gets dry" in section
    assert "data-fh-uncertain" in section and "I don&#39;t know" in section
    assert 'data-fh-capability="CAP09_EXPERIMENT_PLANNING"' in section
    assert ui_text.text("UI_FH_UNCOVERED_WATERING", "en") in section
    assert "<a " not in section and "href" not in section


def test_fan_journey_in_arabic_never_offers_therm01():
    c, _aid = _client_for("fh-fan@example.com")
    sid = _start(c, FAN_IDEA, "electronics_electrical")
    assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    body = _page(c, sid)
    section = _section(body)
    assert 'data-fh-role="FAN"' in section and 'data-fh-object="ROOM"' in section
    assert ui_text.text("UI_FH_ROLE_FAN", "ar") in section
    assert ui_text.text("UI_FH_UNCOVERED_FAN", "ar") in section
    for word in ("THERM", "therm01", "temperature-difference", "CAP13", "CAP12"):
        assert word not in section, word
    assert "<a " not in section
    assert 'dir="rtl"' in body


def test_screen_support_journey_names_cap13_as_conditional_only():
    c, _aid = _client_for("fh-screen@example.com")
    sid = _start(c, SCREEN_IDEA, "mechanical")
    section = _section(_page(c, sid))
    assert 'data-fh-role="SCREEN_SUPPORT"' in section
    assert 'data-fh-capability="CAP13_CONDITIONAL_REACTIONS"' in section
    assert 'data-fh-capability-state="CONDITIONAL"' in section
    assert ui_text.text("UI_FH_UNCOVERED_SCREEN_SUPPORT", "en") in section
    # Step 6: ONE plain link to the existing CAP-13 page, carrying nothing
    assert section.count("<a ") == 1
    assert ('href="/session/%s/support-reactions"' % sid) in section
    assert "form-mockup" not in section and "?" not in section.split("support-reactions", 1)[1][:2]
    assert "CAP12" not in section
    # the inventor's own "screws" exclusion is a quote, never a selected part
    assert "بدون براغي" in section
    assert ui_text.text("UI_FH_COMPONENT_NOTE", "en") in section


def test_an_ineligible_project_reads_cap13_as_not_offered():
    c, _aid = _client_for("fh-screen-elec@example.com")
    sid = _start(c, SCREEN_IDEA, "electronics_electrical")
    section = _section(_page(c, sid))
    assert 'data-fh-capability-state="NOT_FOR_PROJECT"' in section
    assert ui_text.text("UI_FH_CAP13_NOT_FOR_PROJECT", "en") in html.unescape(section)


def test_unreadable_capability_reads_unavailable(monkeypatch):
    def broken(*_a):
        raise OSError("disk I/O error")
    monkeypatch.setattr(webapp, "_cap13_eligible", broken)
    monkeypatch.setattr(webapp, "_current_experiment_ids", broken)
    for role in fh.ROLES:
        items = webapp._handoff_capabilities("sid", object(), role)
        assert items and all(i["state"] == "UNAVAILABLE" for i in items)


# ==========================================================================
# 4. the original statement is the source (also for PR #848)
# ==========================================================================
LONG_FILLER = ("My grandmother kept a small balcony full of herbs and taught me "
               "to notice how the light moves across the city in the evening. ") * 6


def test_a_role_after_500_characters_is_read_from_the_original_statement():
    idea = LONG_FILLER + "I want a device that waters my plants automatically."
    assert idea.index("I want a device") > 520
    c, _aid = _client_for("fh-long@example.com")
    sid = _start(c, idea, "electronics_electrical")
    state = SESSION_STORE[sid]["state"]
    assert "waters my plants" not in (state.idea_summary or "")
    section = _section(_page(c, sid))
    assert 'data-fh-role="WATERING"' in section
    assert "I want a device that waters my plants automatically." in section


def test_the_dimensional_fit_now_reads_the_original_statement():
    idea = (LONG_FILLER + "أريد رفع جسم صغير 3 سم فوق مكتبي وأبعاده 18 × 12 سم")
    c, _aid = _client_for("fh-fit-long@example.com")
    sid = _start(c, idea, "mechanical")
    assert "18 × 12" not in (SESSION_STORE[sid]["state"].idea_summary or "")
    assert "data-engineering-fit-link" in _page(c, sid)
    r = c.get("/session/%s/functional-configuration" % sid)
    assert r.status_code == 200 and "18 × 12 سم" in r.get_data(as_text=True)


def test_an_original_statement_over_the_fit_bound_offers_no_fit():
    # The dimensional recognizer's own 2,000-character capture bound now
    # applies to the whole original statement, not to its trimmed summary.
    idea = ("أريد رفع جسم صغير 3 سم فوق مكتبي وأبعاده 18 × 12 سم. "
            + "قصة طويلة عن المكتب والضوء والكتب. " * 70)
    assert len(idea) > 2000
    c, _aid = _client_for("fh-fit-bound@example.com")
    sid = _start(c, idea, "mechanical")
    assert "18 × 12" in (SESSION_STORE[sid]["state"].idea_summary or "")
    assert "data-engineering-fit-link" not in _page(c, sid)


def test_a_missing_original_statement_is_never_replaced(monkeypatch):
    c, _aid = _client_for("fh-no-seed@example.com")
    sid = _start(c, "أريد رفع جسم صغير 3 سم فوق مكتبي وأبعاده 18 × 12 سم",
                 "mechanical")
    assert "data-engineering-fit-link" in _page(c, sid)
    store = webapp._get_store()
    real = store.load_reconstruction_inputs
    monkeypatch.setattr(store, "load_reconstruction_inputs",
                        lambda s: dict(real(s), seed_idea_text=None))
    body = _page(c, sid)
    assert "data-engineering-fit-link" not in body
    assert c.get("/session/%s/functional-configuration" % sid).status_code != 200
    assert webapp._original_idea_text(sid) is None
    # the trimmed summary still holds the request, and is not used instead
    assert "18 × 12" in (SESSION_STORE[sid]["state"].idea_summary or "")
    # the reading says the original statement was not read, and no role is
    # taken from any other copy of it
    section = _section(body)
    assert "data-fh-idea-unavailable" in section and "data-fh-role" not in section


def test_answers_are_a_source_and_the_idea_notice_shows_when_unreadable(monkeypatch):
    c, _aid = _client_for("fh-answer@example.com")
    sid = _start(c, WATER_IDEA, "electronics_electrical")
    state = SESSION_STORE[sid]["state"]
    store = webapp._get_store()
    real = store.load_reconstruction_inputs
    monkeypatch.setattr(store, "load_reconstruction_inputs",
                        lambda s: dict(real(s), seed_idea_text=None))
    statements, available = webapp._handoff_statements(sid, state)
    assert available is False
    assert all(kind == fh.SOURCE_ANSWER for kind, _r, _t in statements)


# ==========================================================================
# 5. authorization, read-only, journey unchanged
# ==========================================================================
def test_another_account_and_anonymous_see_nothing():
    c, _aid = _client_for("fh-owner@example.com")
    sid = _start(c, WATER_IDEA, "electronics_electrical")
    other, _b = _client_for("fh-other@example.com")
    for client in (other, _new_client()):
        for url in ("/session/%s" % sid, "/session/%s/functional-configuration" % sid):
            r = client.get(url)
            assert r.status_code in (302, 403, 404)
            assert "data-functional-handoff" not in r.get_data(as_text=True)
            assert "waters my plants" not in r.get_data(as_text=True)


def test_rendering_the_handoff_changes_no_state(monkeypatch):
    c, _aid = _client_for("fh-readonly@example.com")
    sid = _start(c, WATER_IDEA, "electronics_electrical")
    _page(c, sid)
    before = _snapshot(c)
    with_handoff = _page(c, sid)
    assert _snapshot(c) == before
    monkeypatch.setattr(webapp, "_functional_handoff_view", lambda *_a: None)
    without = _page(c, sid)
    assert _snapshot(c) == before

    def strip(body):
        # IDEA-DESIGN-UNDERSTANDING-PROJECTION-01: the design-understanding
        # picture reuses this same view (computed once per render), so it is
        # the second block that legitimately differs without the view.
        for marker in ("<details id=\"functional-handoff\"",
                       "<details id=\"design-understanding\""):
            start = body.find(marker)
            if start != -1:
                body = body[:start] + body[body.index("</details>", start) + len("</details>"):]
        return body
    token = re.compile(r'value="[A-Za-z0-9_.=-]{40,}"')
    def norm(body):
        return re.sub(r"\s+", " ", token.sub("", body))
    assert norm(strip(with_handoff)) == norm(strip(without))


def test_the_view_fails_closed():
    assert webapp._functional_handoff_view("sid", None) is None

    class Broken:
        @property
        def assertions(self):
            raise RuntimeError("boom")
    assert webapp._functional_handoff_view("no-such-project", Broken()) == {
        "available": False}
