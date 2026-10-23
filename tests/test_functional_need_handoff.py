# -*- coding: utf-8 -*-
"""FUNCTIONAL-NEED-TO-CAPABILITY-HANDOFF-01 — the read-only, SYSTEM_PROPOSED
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
        assert role.interpretation_status == "SYSTEM_PROPOSED"
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
    ("I want a fan that never stops.", set()),          # unsupported negation
    ("Would a gadget that waters the garden be useful?", set()),
    ("لو كان فيه جهاز يسقي الزرع", set()),
    ("I want a glass of water next to my plants.", set()),
    ("I'm a big fan of gardening and want to grow plants.", set()),
])
def test_positive_evidence_is_required(text, expected):
    got = {(r.role, r.object_key)
           for r in fh.project_functional_roles([("IDEA", "idea", text)]).roles}
    assert got == expected


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
    assert imports == ["dataclasses", "engine.progression_loop",
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
    assert "support-reactions" not in section and "form-mockup" not in section
    assert "CAP12" not in section and "<a " not in section
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
    section = _section(body)
    assert section is None or "data-fh-idea-unavailable" in section


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
        start = body.find("<details id=\"functional-handoff\"")
        if start == -1:
            return body
        return body[:start] + body[body.index("</details>", start) + len("</details>"):]
    token = re.compile(r'value="[A-Za-z0-9_.=-]{40,}"')
    def norm(body):
        return re.sub(r"\s+", " ", token.sub("", body))
    assert norm(strip(with_handoff)) == norm(without)


def test_the_view_fails_closed():
    assert webapp._functional_handoff_view("sid", None) is None

    class Broken:
        @property
        def assertions(self):
            raise RuntimeError("boom")
    assert webapp._functional_handoff_view("no-such-project", Broken()) == {
        "available": False}
