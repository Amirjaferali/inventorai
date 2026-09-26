"""Safe Question Reduction Slice 1 — weak-PF recovery and null-question safety.

A weak first PHYSICAL_FEASIBILITY answer exhausts PF Owner questioning (PF:Q2
is routed to specialist input) without satisfying the W2-D substantive-attempt
gate of the existing OD-R1 accept-risk exit. Once the other Stage-2 gaps close,
no question is served while routed PF still blocks Level 1 -> 2.

Proves, over the real engine, store and web routes, that this state:

* renders no literal "None" question and no answer form, and instead shows a
  truthful recovery that points at the EXISTING correction path;
* refuses any answer post without a current question (forged, stale or
  absent target) and never persists an orphan record;
* leaves PF routed, unresolved and non-Owner, the W2-D gate unweakened and the
  PR #701 OD-R1 / veto semantics unchanged;
* replays and resumes identically; existing versions and Electronics are
  unaffected.

Neutral synthetic fixtures only; no study corpus.
"""
import html as _html
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import engine.path_n_questions as pnq
import engine.progression_loop as pl
import engine.session_reconstruction as SR
from engine import need_routing as nr
from engine.idea_state import (
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
    OPEN, PARTIAL, CLOSED, ACCEPTED_RISK, OWNER_STATED, UNVALIDATED,
    DISPOSITION_SPECIALIST_REQUESTED, DISPOSITION_EVIDENCE_REQUESTED,
)
from web import ui_text
import web.app as appmod
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    client, SEED, MECH, PF_STRONG, BA_1, BA_2, ELEC_SEED, NR1, T2G2, PF_Q1,
    PF_Q2, ID, _start, _stamped_start, _answer, _live, _store, _body,
    _answer_form_target, _accept_pf_via_route, _facts, _row_counts, _decode,
    _routed_form,
)

WEAK = "I am not sure yet."
STALE = appmod.ANSWER_FORM_STALE_MESSAGE


def _raw(c, sid):
    return c.get(f"/session/{sid}").get_data(as_text=True)


def _token(c, sid):
    return re.search(r'name="answer_token" value="([^"]*)"', _raw(c, sid)).group(1)


def _to_stuck(c, sid):
    """MC closed, one WEAK PF attempt, BA closed: the dead end before repair."""
    _answer(c, sid, MECH)
    _answer(c, sid, MECH)
    _answer(c, sid, WEAK)
    _answer(c, sid, BA_1)
    _answer(c, sid, BA_2)
    state = _live(sid)
    assert state.get_gap(MECHANISM_COMPLETENESS).status == CLOSED
    assert state.get_gap(BOUNDARY_AMBIGUITY).status == CLOSED
    assert state.get_gap(PHYSICAL_FEASIBILITY).status == OPEN
    assert pl.select_next_gap(state) is None
    assert state.maturity_level == 1
    return state


def _weak_pf_record(state):
    recs = [r for r in state.assertions if r.gap_context == PHYSICAL_FEASIBILITY
            and r.disposition == "answered" and r.superseded_by is None]
    assert len(recs) == 1 and recs[0].content == WEAK
    return recs[0]


def _correct(c, sid, record_id, text):
    return c.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": record_id, "response": text,
        "answer_token": _token(c, sid)})


# ===========================================================================
# 1-5. the weak attempt: no dead end, no weakened gate, PF still routed
# ===========================================================================

def test_01_weak_pf_leaves_a_real_forward_path(client):
    sid = _start(client)
    state = _to_stuck(client, sid)
    weak = _weak_pf_record(state)
    body = _body(client, sid)
    # the truthful recovery replaces the empty question slot
    assert 'id="routed-recovery"' in body
    assert ui_text.text("UI_NR_RECOVERY_HEADING", "en") in body
    assert 'href="#correct-answer"' in body
    # the journey's primary action points at it (not a "completed flow" handoff)
    primary = re.search(r'<a class="journey-primary"[^>]*href="([^"]*)"', body).group(1)
    assert primary == "#routed-recovery"
    # the EXISTING correction path is opened with the weak PF answer preselected
    assert re.search(r'<details class="correct-answer" id="correct-answer" open', body)
    assert re.search(r'<option value="%s" selected>' % weak.record_id, body)
    # following it through the real routes reaches the existing OD-R1 exit ...
    assert _correct(client, sid, weak.record_id, PF_STRONG).status_code == 302
    assert pl.substantive_attempt_recorded(_live(sid), PHYSICAL_FEASIBILITY)
    assert "routed-accept-risk" in _body(client, sid)
    assert 'id="routed-recovery"' not in _body(client, sid)
    # ... and an explicit acceptance progresses under PR #701 semantics
    assert _accept_pf_via_route(client, sid).status_code == 302
    state = _live(sid)
    assert state.get_gap(PHYSICAL_FEASIBILITY).status == ACCEPTED_RISK
    # the correction replay re-derived BA; any remaining requirement is still
    # served as a real question (never a dead end) and still has to be met
    for text in (BA_1, BA_2, BA_2):
        if pl.select_next_gap(state) != BOUNDARY_AMBIGUITY:
            break
        assert state.maturity_level == 1
        assert _answer_form_target(client, sid)["g"] == BOUNDARY_AMBIGUITY
        _answer(client, sid, text)
        state = _live(sid)
    assert state.get_gap(BOUNDARY_AMBIGUITY).status == CLOSED
    assert state.maturity_level == 2
    assert nr.gap_has_outstanding_routing(state, PHYSICAL_FEASIBILITY)


def test_02_weak_pf_never_satisfies_the_substantive_attempt_gate(client):
    sid = _start(client)
    state = _to_stuck(client, sid)
    assert pl.substantive_attempt_recorded(state, PHYSICAL_FEASIBILITY) is False
    assert "routed-accept-risk" not in _body(client, sid)
    before = _row_counts(sid)
    _accept_pf_via_route(client, sid)                   # direct post: refused
    state = _live(sid)
    assert state.get_gap(PHYSICAL_FEASIBILITY).status == OPEN
    assert state.maturity_level == 1
    assert _row_counts(sid) == before
    # the recovery never accepts, closes or answers anything by itself
    assert not any(r.disposition == "risk_accepted" for r in state.assertions)


def test_03_pf_stays_routed_to_specialist_and_non_owner(client):
    sid = _start(client)
    state = _to_stuck(client, sid)
    assert [(r.operation, r.required_input)
            for r in _store().load_need_routing(sid)] == [("ROUTE", "SPECIALIST")]
    assert nr.eligible_for_owner_questioning(state, PHYSICAL_FEASIBILITY, PF_Q2) is False
    assert nr.owner_questioning_exhausted(state, state.get_gap(PHYSICAL_FEASIBILITY))
    assert state.get_gap(PHYSICAL_FEASIBILITY).closed_at is None
    assert PHYSICAL_FEASIBILITY in pl.routed_maturity_veto_gaps(state)
    body = _body(client, sid)
    assert "Specialist input required" in body
    assert PF_Q2 not in [_decode(_html.unescape(t))["q"] for t in re.findall(
        r'name="answer_target" value="([^"]*)"', _raw(client, sid))
        if _decode(_html.unescape(t))["k"] == "QUESTION"]


def test_04_mandatory_visible_inventory_stays_nine(client):
    sid = _start(client)
    walk = [WEAK] * 4 + [MECH, MECH] + [WEAK] + [WEAK] * 4 + [BA_1, BA_2]
    seen = []
    for text in walk:
        q = _answer_form_target(client, sid)["q"]
        if q.startswith("PATHN:") and q not in seen:
            seen.append(q)
        _answer(client, sid, text)
    state = _live(sid)
    assert pl.select_next_gap(state) is None          # the formerly stuck state
    assert seen == [ID("mechanical:MECHANISM_COMPLETENESS:Q%d" % i)
                    for i in (1, 2, 3, 4)] + [ID(PF_Q1)] + [
        ID("mechanical:BOUNDARY_AMBIGUITY:Q%d" % i) for i in (1, 2, 3, 4)]
    assert len(seen) == 9 and ID(PF_Q2) not in seen


def test_05_recovery_copy_is_truthful_in_english_and_arabic(client):
    keys = ("UI_NR_RECOVERY_HEADING", "UI_NR_RECOVERY_TEXT",
            "UI_NR_RECOVERY_CORRECT", "UI_NR_RECOVERY_LINK",
            "UI_NR_RECOVERY_WAIT", "UI_NR_RECOVERY_JOURNEY_NOTE",
            "UI_NR_RECOVERY_CTA", "UI_NO_QUESTION_NOTE")
    for key in keys:
        en, ar = ui_text.text(key, "en"), ui_text.text(key, "ar")
        assert en and ar and en != ar
        assert re.search("[؀-ۿ]", ar)
        for claim in ("assigned", "reviewed", "verified", "validated",
                      "certified", "solved", "resolved", " safe"):
            assert claim not in en.lower().replace("unresolved", ""), (key, claim)
        for claim in ("تم التحقق", "معتمد", "آمن", "حُلّت", "تمت مراجعة"):
            assert claim not in ar, (key, claim)
    sid = _start(client, lang="ar")
    _to_stuck(client, sid)
    body = _body(client, sid)
    assert ui_text.text("UI_NR_RECOVERY_HEADING", "ar") in body
    assert ui_text.text("UI_NR_RECOVERY_LINK", "ar") in body
    assert 'id="answer-form"' not in body


# ===========================================================================
# 6-9. no null question, no form, no null-target write, no orphan record
# ===========================================================================

def test_06_07_no_none_question_and_no_answer_form(client):
    sid = _start(client)
    _to_stuck(client, sid)
    raw = _raw(client, sid)
    assert '<p class="question"' not in raw
    assert ">None<" not in raw
    assert 'id="answer-form"' not in raw
    assert 'name="response" rows="5"' not in raw
    # the optional routed note stays available on its own bound target
    assert _decode(_routed_form(client, sid)["answer_target"])["q"] == ID(PF_Q2)
    # server side: no QUESTION context exists at all for this state
    state = _live(sid)
    qctx = appmod._resolve_question_context(state, None)
    assert qctx.question is None
    assert appmod._answer_target_from(qctx, state, False) is None
    assert appmod._issue_answer_target(sid, "t", None) == ""


def test_08_09_forged_null_question_posts_fail_safely_without_orphans(client):
    sid = _start(client)
    _to_stuck(client, sid)
    token = _token(client, sid)
    ecv = _live(sid).engine_contract_version
    forged = appmod._issue_answer_target(sid, token, appmod._AnswerTarget(
        appmod.UQTR_TARGET_QUESTION, None, None, ecv))
    stale_pf = appmod._issue_answer_target(sid, token, appmod._AnswerTarget(
        appmod.UQTR_TARGET_QUESTION, ID(PF_Q1), PHYSICAL_FEASIBILITY, ecv))
    before_rows = _row_counts(sid)
    before = _facts(_live(sid))
    for target in (forged, stale_pf, ""):
        for action in ("answered", "unknown", "deferred", "specialist_requested"):
            r = client.post(f"/session/{sid}", data={
                "response": PF_STRONG, "answer_token": token,
                "answer_target": target, "action": action}, answer_binding=False)
            assert r.status_code in (302, 400)
            assert _row_counts(sid) == before_rows
            assert _facts(_live(sid)) == before
    assert STALE in _body(client, sid)
    records = _store().load_contract(sid).assertions
    assert all(r.gap_context is not None for r in records)
    assert all(r.question_target is not None for r in records
               if r.disposition == "answered")


# ===========================================================================
# 10-14. PR #701 semantics unchanged
# ===========================================================================

def test_10_substantive_pf_still_opens_the_existing_od_r1_path(client):
    sid = _start(client)
    _answer(client, sid, MECH)
    _answer(client, sid, MECH)
    _answer(client, sid, PF_STRONG)
    assert pl.substantive_attempt_recorded(_live(sid), PHYSICAL_FEASIBILITY)
    body = _body(client, sid)
    assert "routed-accept-risk" in body
    assert 'id="answer-form"' in body                 # BA is the served question
    assert 'id="routed-recovery"' not in body


def test_11_12_open_pf_blocks_and_explicit_acceptance_progresses(client):
    sid = _start(client)
    _answer(client, sid, MECH)
    _answer(client, sid, MECH)
    _answer(client, sid, PF_STRONG)
    _answer(client, sid, BA_1)
    _answer(client, sid, BA_2)
    state = _live(sid)
    assert state.get_gap(PHYSICAL_FEASIBILITY).status in (OPEN, PARTIAL)
    assert state.maturity_level == 1           # OPEN/PARTIAL routed PF blocks
    body = _body(client, sid)
    assert 'id="answer-form"' not in body and ">None<" not in body
    # a substantive attempt exists, so no correction recovery is offered
    assert 'id="routed-recovery"' not in body
    assert "routed-accept-risk" in body
    assert _accept_pf_via_route(client, sid).status_code == 302
    state = _live(sid)
    assert state.get_gap(PHYSICAL_FEASIBILITY).status == ACCEPTED_RISK
    assert state.maturity_level == 2
    records = _store().load_contract(sid).assertions
    assert not any(r.disposition in (DISPOSITION_SPECIALIST_REQUESTED,
                                     DISPOSITION_EVIDENCE_REQUESTED) for r in records)
    assert all(r.validation_status == UNVALIDATED for r in records)
    risk = [r for r in records if r.disposition == "risk_accepted"]
    assert len(risk) == 1 and risk[0].provenance == OWNER_STATED


def test_13_14_mechanism_and_boundary_serving_are_unchanged(client):
    sid = _start(client)
    served = []
    for _ in range(4):
        served.append(_answer_form_target(client, sid)["q"])
        _answer(client, sid, WEAK)
    assert served == [ID("mechanical:MECHANISM_COMPLETENESS:Q%d" % i)
                      for i in (1, 2, 3, 4)]
    for _ in range(3):
        _answer(client, sid, MECH)
        if pl.select_next_gap(_live(sid)) == PHYSICAL_FEASIBILITY:
            break
    assert _answer_form_target(client, sid)["q"] == ID(PF_Q1)
    _answer(client, sid, WEAK)
    served = []
    for _ in range(4):
        served.append(_answer_form_target(client, sid)["q"])
        _answer(client, sid, WEAK)
    assert served == [ID("mechanical:BOUNDARY_AMBIGUITY:Q%d" % i)
                      for i in (1, 2, 3, 4)]
    # BA keeps serving (stall / exhausted-exit) while it is open: never a dead end
    for _ in range(3):
        raw = _raw(client, sid)
        assert 'id="answer-form"' in raw and ">None<" not in raw
        assert _answer_form_target(client, sid)["g"] == BOUNDARY_AMBIGUITY
        _answer(client, sid, WEAK)


# ===========================================================================
# 15-17. replay / resume, existing versions, Electronics
# ===========================================================================

def test_15_replay_and_resume_preserve_the_repaired_state(client):
    sid = _start(client)
    state = _to_stuck(client, sid)
    live = _facts(state)
    assert _facts(SR.reconstruct_readonly_state(_store(), sid).state) == live
    appmod.SESSION_STORE.pop(sid)
    assert client.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _facts(_live(sid)) == live
    raw = _raw(client, sid)
    assert 'id="routed-recovery"' in raw
    assert 'id="answer-form"' not in raw and ">None<" not in raw


def test_16_existing_versions_keep_their_pf_q2_question(client):
    sid = _stamped_start(client, T2G2)
    _answer(client, sid, MECH)
    _answer(client, sid, MECH)
    _answer(client, sid, WEAK)
    state = _live(sid)
    assert state.need_routing == []
    assert _answer_form_target(client, sid) == {
        "k": "QUESTION", "q": ID(PF_Q2), "g": PHYSICAL_FEASIBILITY, "v": T2G2}
    body = _body(client, sid)
    assert 'id="routed-recovery"' not in body and ">None<" not in body


def test_17_electronics_is_unaffected(client):
    sid = _start(client, seed=ELEC_SEED, domain="electronics_electrical")
    assert _live(sid).need_routing == []
    target = _answer_form_target(client, sid)
    assert target["k"] == "QUESTION" and target["q"].startswith("PATHN:N-")
    for _ in range(6):
        _answer(client, sid, WEAK)
        raw = _raw(client, sid)
        assert 'id="routed-recovery"' not in raw and ">None<" not in raw
        assert 'id="answer-form"' in raw
    assert appmod._routed_recovery_context(_live(sid), None) is None
