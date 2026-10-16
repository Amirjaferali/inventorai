"""IDEA-GROUNDED-FUNCTIONAL-NEED-01 — the inventor's own explicit unknown,
grounded in their idea statement or their answers, shown with the question
that develops it.

Synthetic ideas only. The inventor states a goal and says, in their own words,
that they do not know how a part of it would work. Before this increment an
unknown written INSIDE THE IDEA STATEMENT was never captured (the Level-0 seed
runs no detector), so the first question asked about it cold. Now it is
established as input truth (attributed, verbatim, by the EXISTING detector),
listed under the existing recorded-unknowns owner, and shown with the served
question together with how far an EXISTING admitted mapping connects it:
QUESTION (the served variant's committed intent markers — the T2-G test),
GAP (provenance, another variant's markers or the canonical relevance owner)
or NONE (nothing claimed). No component, sensor, method or design is inferred;
no gap, maturity, progression, routing, serving decision or primary action
changes; live, reconstructed and resumed sessions agree.
"""
import html as _html
import re

import pytest

import engine.progression_loop as pl
import web.app as appmod
from engine import intent_serving as isv
from engine.idea_state import (
    IdeaState, Gap, AssertionRecord, OPEN, MECHANISM_COMPLETENESS,
    PHYSICAL_FEASIBILITY, DISPOSITION_ANSWERED, DISPOSITION_UNKNOWN,
    OWNER_STATED,
)
from engine.path_n_questions import get_served_question
from engine.session_reconstruction import reconstruct_readonly_state
from tests.csrf_client import csrf_client
from web import ui_text

ELEC = "electronics_electrical"
MECH = "mechanical"
MC, PF = MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY

# Case A — the primary example: goal + explicit unknown in ONE sentence.
PLANT = ("I want a solution that waters plants when necessary, but I don't know "
         "how it should determine when watering is needed.")
# Case A variant whose unknown carries the served question's committed markers.
PLANT_NOTICE = ("I want a solution that waters plants when necessary. I don't know "
                "how it would notice that the soil is dry.")
PLANT_NOTICE_UNKNOWN = "I don't know how it would notice that the soil is dry."
PLANT_AR = "أريد حلاً يروي النباتات عند الحاجة، لكن لا أعرف كيف سيلاحظ النظام أن التربة جافة."
# Case B — a different idea, a different unknown.
ASSIST = ("I want to help a person request assistance when they need it, but I "
          "don't know how the need or request will be initiated.")
# Mechanical: the unknown names the second committed variant's vocabulary.
GATE = ("I want a gate that closes itself after someone walks through. I do not "
        "know how the spring would transfer force to the hinge line.")
GATE_UNKNOWN = "I do not know how the spring would transfer force to the hinge line."
MC_Q1 = "mechanical:MECHANISM_COMPLETENESS:Q1"
MC_Q2 = "mechanical:MECHANISM_COMPLETENESS:Q2"

PF_ANSWER = ("It works because gravity pulls the water down the tubes, and the "
             "valve only opens when the float drops, so no pump is needed.")
MC_COVERING = ("The system would notice the dry soil when the float drops and "
               "respond by opening the valve so water flows by gravity.")
MC_WITH_UNKNOWN = ("A float in a small tank drops as water is used and pushes a "
                   "lever that opens a valve. I don't know the spring rate of "
                   "that lever yet.")
MC_WITH_UNKNOWN_FRAGMENT = "I don't know the spring rate of that lever yet."


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

@pytest.fixture()
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


def _start(c, idea, domain=ELEC, lang="en"):
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    r = c.post("/start", data={"idea": idea, "domain_choice": domain,
                               "domain_confirm": domain})
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/", 1)[-1]


def _page(c, sid):
    return c.get(f"/session/{sid}").get_data(as_text=True)


def _state(sid):
    return appmod.SESSION_STORE[sid]["state"]


def _token(body):
    return _html.unescape(re.search(r'name="answer_token" value="([^"]+)"', body).group(1))


def _question(body):
    m = re.search(r'<p class="question"[^>]*>(.*?)</p>', body, re.S)
    return " ".join(_html.unescape(m.group(1)).split()) if m else None


def _act(c, sid, action, text=""):
    r = c.post(f"/session/{sid}", data={"response": text, "action": action,
                                       "answer_token": _token(_page(c, sid))})
    assert r.status_code == 302
    return r


def _block(body):
    """The grounded-need block (outer div), or None."""
    start = body.find('<div class="grounded-need" id="grounded-need"')
    if start < 0:
        return None
    end = body.find('<p class="grounded-need-boundary"', start)
    return body[start:end]


def _bindings(block):
    return re.findall(r'data-grounded-source="(\w+)" data-grounded-binding="(\w+)"', block)


def _visible(fragment):
    return " ".join(_html.unescape(re.sub(r"<[^>]+>", " ", fragment)).split())


def _panel_item(body):
    m = re.search(r'<li data-idea-stated-unknown>.*?</li>', body, re.S)
    return _visible(m.group(0)) if m else None


def _first(gap, domain):
    return " ".join(get_served_question(gap, 0, domain=domain).text.split())


def _engine_state(domain, idea, records=()):
    """A canonical state as the Level-0 seam leaves it after the seed, with an
    OPEN first gap and the given ACTIVE answered records on it."""
    state = IdeaState(idea_id="synthetic")
    state.domain = domain
    state.idea_summary = pl._trim_idea_summary(idea)
    state.gaps.append(Gap(gap_type=MC, status=OPEN, opened_at=1))
    for n, (gap, content, disposition, superseded) in enumerate(records, 1):
        state.assertions.append(AssertionRecord(
            record_id=f"rec_{n}", iteration=n, gap_context=gap, content=content,
            disposition=disposition, provenance=OWNER_STATED,
            superseded_by="rec_x" if superseded else None))
    return state


def _needs(state, gap=MC, qid="N-MC-1"):
    return isv.grounded_functional_needs(state, gap, qid)


# ---------------------------------------------------------------------------
# 1. input truth: the idea statement's explicit unknown, by the EXISTING
#    detector only (registered phrasings, both languages, its own bounds)
# ---------------------------------------------------------------------------

def test_idea_stated_unknown_is_recognised_by_the_existing_detector_only():
    assert isv.idea_stated_unknown(_engine_state(ELEC, PLANT)) == (PLANT, "i don't know")
    assert isv.idea_stated_unknown(_engine_state(ELEC, PLANT_NOTICE)) == (
        PLANT_NOTICE_UNKNOWN, "i don't know")          # the sentence, not the whole
    statement, basis = isv.idea_stated_unknown(_engine_state(ELEC, PLANT_AR))
    assert statement == PLANT_AR and basis == "لا اعرف"  # verbatim, normalised basis
    # not recognised: no registered marker, the bare technical word, too short,
    # negation / knowledge, nothing captured, a corrupt carrier
    for idea in ("I want something that waters my plants when they are dry.",
                 "Whether the market wants this is unknown, but the valve opens when the float drops.",
                 "I don't know.",
                 "I know exactly how it detects the moisture and opens the valve by gravity.",
                 ""):
        assert isv.idea_stated_unknown(_engine_state(ELEC, idea)) is None, idea
    state = _engine_state(ELEC, PLANT)
    for corrupt in (None, 42, "   "):
        state.idea_summary = corrupt
        assert isv.idea_stated_unknown(state) is None
    # the Level-0 display trim (word boundary + visible marker) is what is
    # read: a cut sentence shows cut, a sentence wholly past the cut is not
    # recognised — identical on every replay, under-recognition by design
    filler = "The pots sit on a balcony shelf and the tank hangs above them. " * 7
    assert len(filler) < 500 < len(filler) + 60               # the sentence straddles the cut
    cut = _engine_state(ELEC, filler + "But I don't know how it should determine when watering is needed.")
    statement, _basis = isv.idea_stated_unknown(cut)
    assert statement.startswith("But I don't know") and statement.endswith("…")
    beyond = _engine_state(ELEC, filler + "It also feeds the herbs on the shelf. " * 2
                           + "I don't know how it should determine when watering is needed.")
    assert isv.idea_stated_unknown(beyond) is None


# ---------------------------------------------------------------------------
# 2. Case A: grounded, attributed, bound to NO question (no admitted mapping)
# ---------------------------------------------------------------------------

def test_primary_example_is_grounded_but_claims_no_question_connection():
    needs = _needs(_engine_state(ELEC, PLANT))
    assert len(needs) == 1
    need = needs[0]
    assert need.source == isv.GROUNDED_SOURCE_IDEA
    assert need.statement == PLANT                       # verbatim
    assert need.basis == "i don't know"
    assert need.gap_type == MC
    assert need.binding == isv.GROUNDED_BINDING_NONE
    assert need.question_id is None
    # nothing in the derived need names a component, discipline or method
    for word in ("sensor", "pump", "controller", "wireless", "moisture", "electronics"):
        assert word not in repr(need).lower()


# ---------------------------------------------------------------------------
# 3. a qualified connection uses ONLY the committed intent markers / the
#    canonical relevance owner — never a new heuristic
# ---------------------------------------------------------------------------

def test_question_binding_is_the_served_variants_committed_markers():
    state = _engine_state(ELEC, PLANT_NOTICE)
    (need,) = _needs(state, MC, "N-MC-1")
    assert (need.statement, need.binding, need.question_id) == (
        PLANT_NOTICE_UNKNOWN, isv.GROUNDED_BINDING_QUESTION, "N-MC-1")
    assert isv.matches_committed_intent(need.statement, "N-MC-1")
    # a different served variant of the SAME gap: the committed markers of
    # N-MC-1 and the relevance owner still tie it to the gap, not that question
    (need,) = _needs(state, MC, "N-MC-2")
    assert (need.binding, need.question_id) == (isv.GROUNDED_BINDING_GAP, None)
    # another gap entirely: no mapping at all
    (need,) = _needs(state, PF, "N-PF-1")
    assert need.binding == isv.GROUNDED_BINDING_NONE
    # the Arabic paired surface binds identically (EN/AR parity by construction)
    (need,) = _needs(_engine_state(ELEC, PLANT_AR), MC, "N-MC-1")
    assert (need.statement, need.binding) == (PLANT_AR, isv.GROUNDED_BINDING_QUESTION)


def test_mechanical_binding_follows_the_committed_variant_order():
    state = _engine_state(MECH, GATE)
    (need,) = _needs(state, MC, MC_Q1)
    assert (need.statement, need.binding) == (GATE_UNKNOWN, isv.GROUNDED_BINDING_GAP)
    (need,) = _needs(state, MC, MC_Q2)
    assert (need.binding, need.question_id) == (isv.GROUNDED_BINDING_QUESTION, MC_Q2)
    # the served ask is not a committed record (generic / stall / intake):
    # a QUESTION binding is impossible, the gap-level evidence still stands
    (need,) = _needs(state, MC, None)
    assert (need.binding, need.question_id) == (isv.GROUNDED_BINDING_GAP, None)


# ---------------------------------------------------------------------------
# 4. an unconnected idea need greets the first question(s) only; a connected
#    one stays with the gap it concerns
# ---------------------------------------------------------------------------

def test_unconnected_idea_need_is_shown_only_before_the_first_answered_record():
    answered = [(PF, PF_ANSWER, DISPOSITION_ANSWERED, False)]
    assert _needs(_engine_state(ELEC, PLANT)) != ()
    assert _needs(_engine_state(ELEC, PLANT, answered)) == ()
    # a non-answer disposition is not an answered record: still shown
    paused = [(MC, "", DISPOSITION_UNKNOWN, False)]
    assert len(_needs(_engine_state(ELEC, PLANT, paused))) == 1
    # a superseded answer is not active: still shown
    corrected = [(PF, PF_ANSWER, DISPOSITION_ANSWERED, True)]
    assert len(_needs(_engine_state(ELEC, PLANT, corrected))) == 1
    # a connected need outlives the first answer
    (need,) = _needs(_engine_state(ELEC, PLANT_NOTICE, answered))
    assert need.binding == isv.GROUNDED_BINDING_QUESTION


# ---------------------------------------------------------------------------
# 5. answer-time unknowns: ACTIVE answered records of the served gap only,
#    bound by provenance; superseded, other-gap and non-answer records never
# ---------------------------------------------------------------------------

def test_answer_time_unknowns_come_from_active_records_of_the_served_gap_only():
    records = [
        (MC, MC_WITH_UNKNOWN, DISPOSITION_ANSWERED, False),            # active, MC
        (MC, "An older wording; I do not know the lever ratio yet, really.",
         DISPOSITION_ANSWERED, True),                                   # superseded
        (PF, "It runs on gravity; I don't know the tube diameter yet, honestly.",
         DISPOSITION_ANSWERED, False),                                  # other gap
        (MC, "I am not sure about the lever at all, to be honest here.",
         DISPOSITION_UNKNOWN, False),                                   # not an answer
    ]
    needs = _needs(_engine_state(ELEC, "A plant waterer that uses a float.", records))
    assert [(n.source, n.statement, n.binding, n.question_id) for n in needs] == [
        (isv.GROUNDED_SOURCE_ANSWER, MC_WITH_UNKNOWN_FRAGMENT,
         isv.GROUNDED_BINDING_GAP, None)]
    # a connected idea need first, then answers in ledger order; identical
    # statements once (the idea's sentence repeated in an answer is one need)
    needs = _needs(_engine_state(ELEC, PLANT_NOTICE, records + [
        (MC, PLANT_NOTICE_UNKNOWN, DISPOSITION_ANSWERED, False)]))
    assert [n.source for n in needs] == [isv.GROUNDED_SOURCE_IDEA, isv.GROUNDED_SOURCE_ANSWER]
    assert [n.statement for n in needs] == [PLANT_NOTICE_UNKNOWN, MC_WITH_UNKNOWN_FRAGMENT]
    # an answer-time unknown that carries the served variant's markers binds
    # to that question
    records = [(MC, "A float opens a valve. I don't know how it would notice "
                    "that the tank is empty.", DISPOSITION_ANSWERED, False)]
    (need,) = _needs(_engine_state(ELEC, "A plant waterer that uses a float.", records))
    assert (need.binding, need.question_id) == (isv.GROUNDED_BINDING_QUESTION, "N-MC-1")


# ---------------------------------------------------------------------------
# 6. negative cases: negation, non-equivalent wording, technology as context,
#    ambiguity — nothing is manufactured, nothing is inferred
# ---------------------------------------------------------------------------

def test_negation_non_equivalent_and_context_wording_derive_nothing_extra():
    assert _needs(_engine_state(ELEC, "I know exactly how it detects the moisture "
                                      "and opens the valve by gravity.")) == ()
    assert _needs(_engine_state(ELEC, "Whether the market wants this is unknown, "
                                      "but the valve opens when the float drops.")) == ()
    assert _needs(_engine_state(ELEC, "A plant waterer, something like that.")) == ()
    # a technology named only as context stays the inventor's own words; the
    # derived need adds no component and claims no connection
    context = ("Like the sensor my neighbour uses, but I don't know how it should "
               "decide when to water.")
    (need,) = _needs(_engine_state(ELEC, context))
    assert need.statement == context and need.binding == isv.GROUNDED_BINDING_NONE
    assert need.question_id is None


def test_fails_closed_on_missing_domain_gap_or_corrupt_state():
    state = _engine_state(ELEC, PLANT)
    state.domain = None
    assert _needs(state) == ()
    assert isv.grounded_functional_needs(_engine_state(ELEC, PLANT), None) == ()
    assert isv.grounded_functional_needs(_engine_state(ELEC, PLANT), "") == ()

    class Broken:
        domain = ELEC
        idea_summary = PLANT

        @property
        def assertions(self):
            raise RuntimeError("unreadable ledger")

    assert isv.grounded_functional_needs(Broken(), MC, "N-MC-1") == ()
    assert isv.idea_stated_unknown(Broken()) == (PLANT, "i don't know")


def test_derivation_persists_nothing_and_moves_no_state():
    state = _engine_state(ELEC, PLANT_NOTICE)
    before = (repr(state.gaps), repr(state.assertions), state.maturity_level,
              state.iteration, list(state.acknowledged_unknowns), state.idea_summary)
    _needs(state)
    isv.idea_stated_unknown(state)
    assert (repr(state.gaps), repr(state.assertions), state.maturity_level,
            state.iteration, list(state.acknowledged_unknowns), state.idea_summary) == before
    assert pl.select_next_gap(state) == MC


# ---------------------------------------------------------------------------
# 7. the live journey — Case A, EN and AR
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("lang", ["en", "ar"])
def test_plant_watering_journey_acknowledges_the_unknown_and_continues(client, lang):
    sid = _start(client, PLANT, ELEC, lang)
    body = _page(client, sid)
    # the question itself and the ONE primary action are unchanged
    assert _question(body) == (_first(MC, ELEC) if lang == "en"
                               else " ".join(get_served_question(MC, 0, domain=ELEC).text_ar.split()))
    assert body.count("data-primary-action") == 1
    block = _block(body)
    assert block is not None
    assert _bindings(block) == [("idea", "none")]
    shown = _visible(block)
    for key in ("UI_GFN_HEADING", "UI_GFN_SOURCE_IDEA", "UI_GFN_BINDING_NONE", "UI_GFN_NEXT"):
        assert ui_text.text(key, lang) in shown, key
    assert ui_text.text("UI_GFN_BOUNDARY", lang) in _visible(body)
    assert PLANT in shown                                  # verbatim, escaped
    assert "&#39;" in block or "&#x27;" in block or "'" not in PLANT  # escaped apostrophe
    assert 'dir="auto"' in block
    # the existing recorded-unknowns owner lists it, labelled by its source
    assert _panel_item(body) == f"{ui_text.text('UI_GFN_PANEL_IDEA', lang)} {PLANT}"
    assert ui_text.text("UI_B_SESSION_006", lang) in _visible(body)
    # the Compass counts are untouched (not an answer-time unknown)
    assert 'data-pc-category="noted_unknowns"' not in body
    # the inventor marks the question not known yet: the PR #835 pause is
    # unchanged, the next gap is served, the idea's unknown still greets it
    _act(client, sid, "unknown")
    body = _page(client, sid)
    assert pl.paused_gap_types(_state(sid)) == {MC}
    assert _question(body) == (_first(PF, ELEC) if lang == "en"
                               else " ".join(get_served_question(PF, 0, domain=ELEC).text_ar.split()))
    assert _bindings(_block(body)) == [("idea", "none")]
    assert _panel_item(body) is not None
    # after the first answered record the unconnected need leaves the question
    # slot; the recorded-unknowns panel keeps it
    _act(client, sid, "answered", PF_ANSWER)
    body = _page(client, sid)
    assert _block(body) is None
    assert _panel_item(body) is not None
    state = _state(sid)
    assert state.maturity_level < 2 and state.current_stage == 2
    assert [r.disposition for r in state.assertions] == ["unknown", "answered"]
    assert state.acknowledged_unknowns == []                # no ledger / track write


def test_qualified_idea_unknown_is_shown_with_the_question_that_asks_about_it(client):
    sid = _start(client, PLANT_NOTICE, ELEC)
    body = _page(client, sid)
    assert _question(body) == _first(MC, ELEC)
    block = _block(body)
    assert _bindings(block) == [("idea", "question")]
    assert PLANT_NOTICE_UNKNOWN in _visible(block)
    assert ui_text.text("UI_GFN_BINDING_QUESTION", "en") in _visible(block)
    assert _panel_item(body).endswith(PLANT_NOTICE_UNKNOWN)
    # the inventor covers N-MC-1; W2-C serves the next variant exactly as
    # before, and the need now says the AREA is where it is developed
    _act(client, sid, "answered", MC_COVERING)
    body = _page(client, sid)
    assert _question(body) == " ".join(get_served_question(MC, 1, domain=ELEC).text.split())
    assert _bindings(_block(body)) == [("idea", "gap")]
    assert ui_text.text("UI_GFN_BINDING_GAP", "en") in _visible(_block(body))


def test_arabic_idea_unknown_renders_verbatim_in_the_arabic_journey(client):
    sid = _start(client, PLANT_AR, ELEC, "ar")
    body = _page(client, sid)
    block = _block(body)
    assert _bindings(block) == [("idea", "question")]
    assert PLANT_AR in _visible(block)
    assert ui_text.text("UI_GFN_BINDING_QUESTION", "ar") in _visible(block)
    assert _panel_item(body).endswith(PLANT_AR)


# ---------------------------------------------------------------------------
# 8. Case B — a different idea yields its own need; refusal stays refusal
# ---------------------------------------------------------------------------

def test_assistance_request_idea_yields_its_own_need_without_assumed_technology(client):
    sid = _start(client, ASSIST, ELEC)
    body = _page(client, sid)
    block = _block(body)
    assert _bindings(block) == [("idea", "none")]
    shown = _visible(block)
    assert ASSIST in shown
    assert PLANT not in shown
    for word in ("wearable", "camera", "alarm", "pump", "microcontroller",
                 "wireless", "medical", "button", "sensor"):
        assert word not in shown.lower(), word
    assert _panel_item(body).endswith(ASSIST)


def test_an_idea_the_entry_gate_refuses_starts_no_journey(client):
    refused = ("A wearable that tells a nurse when a patient needs help, but I "
               "don't know how the request will be initiated.")
    assert appmod._has_strong_unsupported_evidence(refused.lower())
    before = set(appmod.SESSION_STORE)
    r = client.post("/start", data={"idea": refused, "domain_choice": ELEC,
                                    "domain_confirm": ELEC})
    assert r.status_code == 200 and "/session/" not in (r.headers.get("Location") or "")
    assert set(appmod.SESSION_STORE) == before
    assert 'id="grounded-need"' not in r.get_data(as_text=True)


# ---------------------------------------------------------------------------
# 9. answer-time unknowns, correction, and live / reconstructed / resumed parity
# ---------------------------------------------------------------------------

def test_answer_time_unknown_is_shown_by_provenance_and_a_correction_withdraws_it(client):
    sid = _start(client, "I want a plant waterer that uses a float in a tank.", ELEC)
    assert _block(_page(client, sid)) is None            # no explicit unknown
    _act(client, sid, "answered", MC_WITH_UNKNOWN)
    body = _page(client, sid)
    state = _state(sid)
    assert pl.select_next_gap(state) == MC               # still the served gap
    block = _block(body)
    assert _bindings(block) == [("answer", "gap")]
    assert MC_WITH_UNKNOWN_FRAGMENT in _visible(block)
    assert ui_text.text("UI_GFN_SOURCE_ANSWER", "en") in _visible(block)
    assert len(state.acknowledged_unknowns) == 1         # the existing track, unchanged
    # the inventor corrects that answer: the superseded statement is gone
    target = state.assertions[-1].record_id
    r = client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": target, "response": MC_COVERING,
        "answer_token": _token(body)})
    assert r.status_code == 302
    body = _page(client, sid)
    assert _block(body) is None
    # the recorded-unknowns panel no longer carries it either (full replay
    # rebuilt the track); the correction history itself stays visible as before
    assert ui_text.text("UI_B_SESSION_006", "en") not in _visible(body)
    assert _state(sid).acknowledged_unknowns == []


def test_cold_read_only_page_renders_without_the_block_and_without_error(client):
    sid = _start(client, PLANT_NOTICE, ELEC)
    appmod.SESSION_STORE.clear()
    r = client.get(f"/session/{sid}")
    assert r.status_code == 200
    body = r.get_data(as_text=True)
    assert getattr(_state(sid), "domain", None) is None   # the non-resumable cold entry
    assert 'id="grounded-need"' not in body and 'data-idea-stated-unknown' not in body


def test_live_reconstructed_and_resumed_sessions_agree(client):
    sid = _start(client, PLANT_NOTICE, ELEC)
    _act(client, sid, "answered", MC_WITH_UNKNOWN)
    live = _state(sid)
    qctx = appmod._resolve_question_context(live, appmod.SESSION_STORE[sid]["last_result"])
    served = getattr(qctx.served, "question_id", None)
    live_needs = isv.grounded_functional_needs(live, qctx.gap_type, served)
    assert [n.source for n in live_needs] == ["idea", "answer"]
    live_block = _visible(_block(_page(client, sid)))
    recon = reconstruct_readonly_state(appmod._get_store(), sid).state
    assert isv.grounded_functional_needs(recon, qctx.gap_type, served) == live_needs
    assert isv.idea_stated_unknown(recon) == isv.idea_stated_unknown(live)
    appmod.SESSION_STORE.clear()
    assert client.post(f"/session/{sid}/resume").status_code == 302
    assert _visible(_block(_page(client, sid))) == live_block
    assert isv.grounded_functional_needs(_state(sid), qctx.gap_type, served) == live_needs


# ---------------------------------------------------------------------------
# 10. boundaries: copy is attributed and claims nothing; no engine import of
#     the MSNL shadow; the catalogue carries both languages
# ---------------------------------------------------------------------------

def test_copy_is_attributed_bilingual_and_claims_nothing():
    keys = ("UI_GFN_HEADING", "UI_GFN_SOURCE_IDEA", "UI_GFN_SOURCE_ANSWER",
            "UI_GFN_BINDING_QUESTION", "UI_GFN_BINDING_GAP", "UI_GFN_BINDING_NONE",
            "UI_GFN_NEXT", "UI_GFN_BOUNDARY", "UI_GFN_PANEL_IDEA")
    for key in keys:
        assert ui_text.has_string(key), key
        assert ui_text.text(key, "en") != ui_text.text(key, "ar")
    boundary = ui_text.text("UI_GFN_BOUNDARY", "en").lower()
    assert "has not assumed" in boundary and "not a checked requirement" in boundary
    for key in keys:
        for claim in ("feasible", "validated", "verified", "required component",
                      "must use", "recommend"):
            assert claim not in ui_text.text(key, "en").lower(), (key, claim)


def test_intent_serving_does_not_import_the_msnl_shadow_or_any_provider():
    import pathlib
    source = pathlib.Path(isv.__file__).read_text(encoding="utf-8")
    for forbidden in ("msnl_shadow", "ai_advisor", "openai", "requests", "urllib"):
        assert forbidden not in source, forbidden
