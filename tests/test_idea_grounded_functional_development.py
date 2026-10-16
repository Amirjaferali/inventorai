"""IDEA-GROUNDED-FUNCTIONAL-DEVELOPMENT-02 — the inventor's own explicit
unknown chooses the next development question, once, when an admitted mapping
supports it.

PR #836 shows an inventor-stated unknown beside the served question. This
increment lets that statement direct WHICH committed question of the current
canonical gap is served: when the unknown carries the committed EN/AR-paired
intent markers of a knowledge-seeking variant that is uncovered, not routed
and not yet asked, the W2-C serving owner serves that variant and the page
says why. Otherwise nothing changes. The statement is never an answer; gap
selection, progression, coverage, routing, the PR #835 pause, UQTR-01 and
live / reconstructed / resumed parity are unchanged. Synthetic ideas only.
"""
import html as _html
import re

import pytest

import engine.progression_loop as pl
import web.app as appmod
from engine import intent_serving as isv
from engine import need_routing
from engine.idea_state import (
    IdeaState, Gap, AssertionRecord, OPEN, MECHANISM_COMPLETENESS,
    PHYSICAL_FEASIBILITY, DISPOSITION_ANSWERED, OWNER_STATED,
)
from engine.path_n_questions import get_served_question
from engine.session_reconstruction import (
    reconstruct_readonly_state, ENGINE_CONTRACT_VERSION_NR1)
from tests.csrf_client import csrf_client
from web import ui_text

ELEC = "electronics_electrical"
MECH = "mechanical"
MC, PF = MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY
MQ1, MQ2 = "mechanical:MECHANISM_COMPLETENESS:Q1", "mechanical:MECHANISM_COMPLETENESS:Q2"

# Idea A (Mechanical): the unknown names what Q2 asks about.
GATE = ("I want a gate that closes itself after someone walks through. I do not "
        "know how the spring would transfer force to the hinge line.")
# Idea B (Electronics): the unknown names what N-MC-2 asks about.
REMINDER = ("I want a device that reminds my grandmother to drink water during "
            "the day, but I don't know what the main parts would be.")
# Abstention: the primary example has no admitted mapping.
PLANT = ("I want a solution that waters plants when necessary, but I don't know "
         "how it should determine when watering is needed.")
# The unknown already concerns the served question: nothing to change.
PLANT_NOTICE = ("I want a solution that waters plants when necessary. I don't know "
                "how it would notice that the soil is dry.")
FLOAT = "I want a plant waterer that uses a float in a small tank above the pots."
STEP_UNKNOWN_ANSWER = ("It would notice the dry soil when the float drops and respond "
                       "by opening the valve. I don't know what happens step by step "
                       "after that.")
COVERING_ANSWER = ("It would notice the dry soil when the float drops and respond by "
                   "opening the valve so water flows by gravity.")
Q2_ANSWER = ("The spring is wound around the hinge pin, so when the gate opens it "
             "twists the spring, and the spring pushes the gate back closed.")


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

@pytest.fixture()
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


def _start(c, idea, domain, lang="en"):
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


def _text(gap, index, domain, lang="en"):
    served = get_served_question(gap, index, domain=domain)
    return " ".join((served.text if lang == "en" else served.text_ar).split())


def _by_id(gap, qid, domain, lang="en"):
    from engine.path_n_questions import get_served_question_by_id
    served = get_served_question_by_id(gap, qid, domain=domain)
    return " ".join((served.text if lang == "en" else served.text_ar).split())


def _engine_state(domain, idea, records=(), iterations_open=0, version=None):
    state = IdeaState(idea_id="synthetic")
    state.domain = domain
    state.path = "N"
    if version is not None:
        state.engine_contract_version = version
    state.idea_summary = pl._trim_idea_summary(idea)
    state.gaps.append(Gap(gap_type=MC, status=OPEN, opened_at=1,
                          iterations_open=iterations_open))
    for n, (content, target, superseded) in enumerate(records, 1):
        state.assertions.append(AssertionRecord(
            record_id=f"rec_{n}", iteration=n, gap_context=MC, content=content,
            disposition=DISPOSITION_ANSWERED, provenance=OWNER_STATED,
            question_target=target, superseded_by="rec_x" if superseded else None))
    return state


def _serving(state, gap=MC):
    return isv.w2c_served_question(state, gap)


# ---------------------------------------------------------------------------
# 1. engine: a qualified stated unknown chooses the variant, once
# ---------------------------------------------------------------------------

def test_mechanical_unknown_serves_the_variant_that_asks_about_it():
    serving = _serving(_engine_state(MECH, GATE))
    assert (serving.question_id, serving.adjusted, serving.basis) == (
        MQ2, True, isv.BASIS_STATED_UNKNOWN)
    assert serving.text == get_served_question(MC, 1, domain=MECH).text
    assert isv.stated_unknown_serving(_engine_state(MECH, GATE), MC)


def test_electronics_unknown_serves_its_own_variant():
    serving = _serving(_engine_state(ELEC, REMINDER))
    assert (serving.question_id, serving.basis) == ("N-MC-2", isv.BASIS_STATED_UNKNOWN)


def test_no_admitted_mapping_or_already_served_abstains():
    assert _serving(_engine_state(ELEC, PLANT)) is None            # no mapping
    assert _serving(_engine_state(ELEC, PLANT_NOTICE)) is None     # it IS the question
    assert _serving(_engine_state(ELEC, FLOAT)) is None            # no unknown
    assert not isv.stated_unknown_serving(_engine_state(ELEC, PLANT), MC)


def test_uncertainty_seeking_variants_are_never_chosen():
    # carries only N-MC-4's markers ("unclear how"); naming the uncertainty is
    # what N-MC-4 asks for, so it is never the focus
    idea = "I am not sure, it is unclear how it would fit on the balcony shelf."
    assert isv.matches_committed_intent(
        isv.idea_stated_unknown(_engine_state(ELEC, idea))[0], "N-MC-4")
    assert _serving(_engine_state(ELEC, idea)) is None


def test_two_matches_choose_the_first_in_committed_order():
    idea = ("I want a device that reminds my grandmother to drink water. I don't know "
            "the main parts or what happens step by step.")
    assert _serving(_engine_state(ELEC, idea)).question_id == "N-MC-2"


def test_covered_routed_or_already_asked_variants_are_not_chosen(monkeypatch):
    # covered by an active answer (legacy marker coverage)
    covered = _engine_state(MECH, GATE, records=[(
        "The spring would transfer force to the hinge line through a short lever.",
        "PATHN:" + MQ1, False)])
    assert _serving(covered) is None or _serving(covered).question_id != MQ2
    # already asked: any active record targeting Q2, even a weak one
    asked = _engine_state(MECH, GATE, records=[("Not much to say there yet.",
                                                "PATHN:" + MQ2, False)])
    serving = _serving(asked)
    assert serving is None or serving.basis != isv.BASIS_STATED_UNKNOWN
    # a superseded record no longer counts as asked
    superseded = _engine_state(MECH, GATE, records=[("Not much to say there yet.",
                                                     "PATHN:" + MQ2, True)])
    assert _serving(superseded).question_id == MQ2
    # an outstanding routed need is never chosen
    monkeypatch.setattr(need_routing, "outstanding_routed_question_ids",
                        lambda state, gap: frozenset({MQ2}))
    assert _serving(_engine_state(MECH, GATE)) is None


def test_answer_time_unknown_chooses_a_later_variant_under_t2g():
    # the inventor answered N-MC-1 and said in it what they do not know; the
    # canonical next variant is N-MC-2, the unknown points at N-MC-3
    state = _engine_state(ELEC, FLOAT, records=[(STEP_UNKNOWN_ANSWER, "PATHN:N-MC-1", False)],
                          iterations_open=1, version=ENGINE_CONTRACT_VERSION_NR1)
    serving = _serving(state)
    assert (serving.question_id, serving.basis) == ("N-MC-3", isv.BASIS_STATED_UNKNOWN)


def test_the_statement_is_never_an_answer_and_moves_no_state():
    state = _engine_state(MECH, GATE)
    before = (repr(state.gaps), repr(state.assertions), state.maturity_level,
              state.iteration, state.idea_summary)
    coverage = isv.compute_intent_coverage(state, MC)
    _serving(state)
    assert coverage == frozenset()                       # nothing covered by it
    assert isv.compute_intent_coverage(state, MC) == coverage
    assert (repr(state.gaps), repr(state.assertions), state.maturity_level,
            state.iteration, state.idea_summary) == before
    assert pl.select_next_gap(state) == MC
    assert isv.supplemental_relevance(state, MC, Q2_ANSWER) == \
        isv.matches_committed_intent(Q2_ANSWER, MQ1)     # canonical scope kept


def test_fails_closed_on_an_unreadable_ledger():
    state = _engine_state(MECH, GATE)
    state.assertions.append(AssertionRecord(
        record_id="weird", iteration=9, gap_context=MC, content="x",
        disposition=DISPOSITION_ANSWERED, provenance=OWNER_STATED))
    serving = _serving(state)
    assert serving is None or serving.basis != isv.BASIS_STATED_UNKNOWN


# ---------------------------------------------------------------------------
# 2. the live journey (EN / AR): idea A and idea B
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("lang", ["en", "ar"])
def test_gate_journey_asks_about_the_stated_unknown_then_resumes(client, lang):
    sid = _start(client, GATE, MECH, lang)
    body = _page(client, sid)
    assert _question(body) == _text(MC, 1, MECH, lang) != _text(MC, 0, MECH, lang)
    assert "data-grounded-focus" in body
    assert ui_text.text("UI_GFN_CHOSEN", lang) in _html.unescape(body)
    assert 'data-grounded-binding="question"' in body
    assert body.count("data-primary-action") == 1
    # the answer is bound to the question actually shown, integrated into MC
    _act(client, sid, "answered", Q2_ANSWER)
    state = _state(sid)
    record = state.assertions[-1]
    assert (record.gap_context, record.question_target) == (MC, "PATHN:" + MQ2)
    assert record.content == Q2_ANSWER
    # asked once: never repeated; the journey resumes at the question the
    # focus displaced (the earliest committed question not yet asked)
    body = _page(client, sid)
    assert _question(body) == _text(MC, 0, MECH, lang)
    assert "data-grounded-focus" not in body
    serving = _serving(_state(sid))
    assert (serving.question_id, serving.basis) == (MQ1, isv.BASIS_RESUMED)
    _act(client, sid, "answered", "Someone pushes the gate open and walks "
                                  "through, then the gate swings back shut.")
    assert _state(sid).assertions[-1].question_target == "PATHN:" + MQ1
    assert _question(_page(client, sid)) not in (_text(MC, 0, MECH, lang),
                                                 _text(MC, 1, MECH, lang))


def test_reminder_journey_asks_for_the_main_parts_first(client):
    sid = _start(client, REMINDER, ELEC)
    body = _page(client, sid)
    assert _question(body) == _by_id(MC, "N-MC-2", ELEC)
    assert "data-grounded-focus" in body
    for word in ("sensor", "pump", "microcontroller", "wireless", "alarm"):
        assert word not in _html.unescape(body[body.find('id="grounded-need"'):
                                               body.find('class="grounded-need-boundary"')]).lower()


@pytest.mark.parametrize("idea", [PLANT, PLANT_NOTICE, FLOAT])
def test_unsupported_or_already_matching_ideas_keep_the_journey(client, idea):
    sid = _start(client, idea, ELEC)
    body = _page(client, sid)
    assert _question(body) == _text(MC, 0, ELEC)
    assert "data-grounded-focus" not in body


def test_answer_time_unknown_directs_the_next_question(client):
    sid = _start(client, FLOAT, ELEC)
    _act(client, sid, "answered", STEP_UNKNOWN_ANSWER)
    body = _page(client, sid)
    assert pl.select_next_gap(_state(sid)) == MC
    assert _question(body) == _by_id(MC, "N-MC-3", ELEC)
    assert "data-grounded-focus" in body
    # the inventor corrects that answer: the unknown is gone and so is the focus
    target = _state(sid).assertions[-1].record_id
    r = client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": target, "response": COVERING_ANSWER,
        "answer_token": _token(body)})
    assert r.status_code == 302
    body = _page(client, sid)
    assert "data-grounded-focus" not in body
    assert _question(body) != _by_id(MC, "N-MC-3", ELEC)


# ---------------------------------------------------------------------------
# 3. PR #835 pause, UQTR-01 revisit and parity are preserved
# ---------------------------------------------------------------------------

def test_not_known_yet_on_the_chosen_question_pauses_and_revisits_it(client):
    sid = _start(client, GATE, MECH)
    _act(client, sid, "unknown")
    state = _state(sid)
    assert pl.paused_gap_types(state) == {MC}
    assert state.assertions[-1].question_target == "PATHN:" + MQ2
    body = _page(client, sid)
    assert _question(body) == _text(PF, 0, MECH)          # the next independent gap
    start = body.find('data-paused-gap="%s"' % MC)
    block = _html.unescape(body[start:body.find("</details>", start)])
    assert _text(MC, 1, MECH) in " ".join(block.split())  # revisit = the paused ask


def test_live_reconstructed_and_resumed_sessions_serve_the_same_question(client):
    sid = _start(client, GATE, MECH)
    live = _serving(_state(sid))
    live_question = _question(_page(client, sid))
    recon = reconstruct_readonly_state(appmod._get_store(), sid).state
    assert _serving(recon) == live
    appmod.SESSION_STORE.clear()
    assert client.post(f"/session/{sid}/resume").status_code == 302
    assert _question(_page(client, sid)) == live_question
    assert _serving(_state(sid)) == live


def test_copy_is_bilingual_attributed_and_claims_nothing():
    assert ui_text.has_string("UI_GFN_CHOSEN")
    en = ui_text.text("UI_GFN_CHOSEN", "en")
    assert "fixed set" in en and "not treated as an answer" in en
    for claim in ("feasible", "validated", "verified", "recommend", "required"):
        assert claim not in en.lower()
    assert ui_text.text("UI_GFN_CHOSEN", "ar") != en
