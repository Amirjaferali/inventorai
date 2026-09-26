"""Safe Question Reduction Slice 1 — PF:Q2 non-Owner NeedRouting.

Proves, over the real engine, the real durable store and the real web routes:

* mechanical:PHYSICAL_FEASIBILITY:Q2 is no longer a mandatory inventor question
  on a NEW routing-aware project, while PF:Q1 is served unchanged;
* the underlying requirement stays OUTSTANDING: PF can never be CLOSED while the
  routed need is outstanding (DEMONSTRATED and REASONED follow-up alike), it
  vetoes Level 1 -> 2 (risk acceptance never discharges it), and it stays
  visible in open-gap truth, the requirement landscape, the validation plan and
  derived readiness;
* routing is a SYSTEM_INFERRED sidecar record — never an Owner AssertionRecord,
  never Evidence, never a validation or specialist-review award;
* durable, append-only, replay-safe (live == cold reconstruction == writable
  resume), with ROUTE / RETRACT correction, idempotent retries, no phantom state
  on failure and truthful ambiguous-commit handling;
* existing project versions keep the 10-question behavior; MECHANISM_COMPLETENESS
  is rejected at every boundary; electronics and BA:Q3 / BA:Q4 are unchanged;
* the optional Owner note binds to the exact PF:Q2 identity even while BA is the
  primary gap; EN / AR copy is truthful; rendering writes nothing; no network or
  model path is reachable.

Fixtures are neutral synthetic ideas written for this slice; no study corpus.
"""
import dataclasses
import html as _html
import json
import os
import re
import socket
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

import engine.path_n_questions as pnq
import engine.progression_loop as pl
import engine.session_reconstruction as SR
from engine import need_routing as nr
from engine.derived_readiness import derive_readiness
from engine.idea_state import (
    IdeaState, MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
    OPEN, PARTIAL, CLOSED, ACCEPTED_RISK, DEMONSTRATED, REASONED,
    SYSTEM_INFERRED, OWNER_STATED, UNVALIDATED, VALIDATED_STATUSES,
    DISPOSITION_SPECIALIST_REQUESTED, DISPOSITION_EVIDENCE_REQUESTED,
)
from engine.record_contract import ProjectRecordContract
from engine.record_store import (
    NEED_ROUTING_EXACT_REPLAY, NEED_ROUTING_INSERTED, NeedRoutingConflict,
    NeedRoutingHistoryError, RecordStoreConnectionUnsafe, SqliteRecordStore,
)
from engine.requirement_landscape import derive_requirement_landscape
from engine.validation_plan import derive_validation_plan, SPECIALIST_REQUIRED
from tests.csrf_client import csrf_client
import web.app as appmod

PF_Q1 = "mechanical:PHYSICAL_FEASIBILITY:Q1"
PF_Q2 = "mechanical:PHYSICAL_FEASIBILITY:Q2"
BA_Q1 = "mechanical:BOUNDARY_AMBIGUITY:Q1"
# The canonical RVR-7 served-question identity carried by answer targets and
# by every durable question_target.
ID = "PATHN:".__add__
PF_Q1_TEXT = pnq.get_served_question(PHYSICAL_FEASIBILITY, 0, domain="mechanical").text
PF_Q2_TEXT = pnq.get_served_question(PHYSICAL_FEASIBILITY, 1, domain="mechanical").text
PF_Q2_TEXT_AR = pnq.get_served_question(PHYSICAL_FEASIBILITY, 1, domain="mechanical").text_ar
NR1 = SR.ENGINE_CONTRACT_VERSION_NR1
T2G2 = SR.ENGINE_CONTRACT_VERSION_T2G2

SEED = ("A folding mechanical wheelchair ramp with a spring latch. The "
        "inventor wants the ramp to stay reliably locked in the flat, "
        "load-bearing position and to fold away without tools")
MECH = ("The load path runs from the deck panel into the hinge line and the "
        "spring latch transfers force into the frame rail, so the ramp stays "
        "locked flat.")
PF_STRONG = ("The physical principle is a compressed spring whose stored energy "
             "pushes the latch pin into the rail, and the steel material is "
             "rated to withstand the deck load, so the locking is feasible.")
BA_1 = ("Existing portable ramps fold in half; mine uses a spring latch that "
        "locks automatically.")
BA_2 = ("Unlike folding ramps, mine locks automatically with the spring latch "
        "without any tools.")
NOTE = "The ramp should carry a wheelchair and its user, about 150 kg."

ELEC_SEED = ("a small device that switches off a room heater when the room gets "
             "too warm, using a temperature sensor and a relay circuit")

FORBIDDEN_CLAIMS = ("assigned", "reviewed", "verified", "validated", "certified",
                    "solved", "safe")
FORBIDDEN_CLAIMS_AR = ("تم التحقق", "معتمد", "آمن", "حُلّت", "تمت مراجعة")


# ---------------------------------------------------------------------------
# engine helpers
# ---------------------------------------------------------------------------

def _state(version=NR1, routed=True, pid="p-nr"):
    s = IdeaState(idea_id="i-nr")
    s.domain = "mechanical"
    s.domain_signal = "mechanical"
    s.path = "N"
    s.engine_contract_version = version
    if routed:
        for rev in nr.creation_revisions(pid, "mechanical", "N", version):
            nr.apply_revision(s, rev)
    pl.run_iteration(s, SEED)
    return s


def _to_pf(s):
    pl.run_iteration(s, MECH)
    pl.run_iteration(s, MECH)
    assert s.get_gap(MECHANISM_COMPLETENESS).status == CLOSED
    assert s.get_gap(PHYSICAL_FEASIBILITY).status == OPEN
    return s


def _served_id(s):
    gap = pl.select_next_gap(s)
    if gap is None:
        return None
    served = pnq.get_served_question(gap, s.get_gap(gap).iterations_open,
                                     domain="mechanical")
    return served.question_id


def _full_journey(s):
    _to_pf(s)
    ids = [_served_id(s)]
    for text in (PF_STRONG, BA_1, BA_2):
        pl.run_iteration(s, text)
        ids.append(_served_id(s))
    return ids


# ---------------------------------------------------------------------------
# web helpers
# ---------------------------------------------------------------------------

@pytest.fixture()
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


def _start(c, seed=SEED, domain="mechanical", lang="en"):
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    r = c.post("/start", data={"idea": seed, "domain_confirm": domain})
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/", 1)[-1]


def _stamped_start(c, version, **kw):
    original = appmod.CURRENT_ENGINE_CONTRACT_VERSION
    appmod.CURRENT_ENGINE_CONTRACT_VERSION = version
    try:
        return _start(c, **kw)
    finally:
        appmod.CURRENT_ENGINE_CONTRACT_VERSION = original


def _body(c, sid):
    return _html.unescape(c.get(f"/session/{sid}").get_data(as_text=True))


def _answer(c, sid, text):
    raw = c.get(f"/session/{sid}").get_data(as_text=True)
    token = re.search(r'name="answer_token" value="([^"]*)"', raw).group(1)
    r = c.post(f"/session/{sid}", data={"response": text, "answer_token": token})
    assert r.status_code == 302


def _live(sid):
    return appmod.SESSION_STORE[sid]["state"]


def _store():
    return appmod._get_store()


def _decode(target):
    body = target.rpartition(".")[0]
    import base64
    return json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))


def _answer_form_target(c, sid):
    raw = c.get(f"/session/{sid}").get_data(as_text=True)
    m = re.search(r'<form id="answer-form".*?</form>', raw, re.S)
    tgt = re.search(r'name="answer_target" value="([^"]*)"', m.group(0)).group(1)
    return _decode(_html.unescape(tgt))


def _routed_form(c, sid):
    raw = c.get(f"/session/{sid}").get_data(as_text=True)
    m = re.search(r'<div class="routed-need.*?</form>', raw, re.S)
    assert m, "the routed-need block must render"
    f = m.group(0)
    return {"answer_token": _html.unescape(re.search(
                r'name="answer_token" value="([^"]*)"', f).group(1)),
            "answer_target": _html.unescape(re.search(
                r'name="answer_target" value="([^"]*)"', f).group(1))}


def _web_to_ba(c, sid):
    _answer(c, sid, MECH)
    _answer(c, sid, MECH)
    _answer(c, sid, PF_STRONG)
    assert pl.select_next_gap(_live(sid)) == BOUNDARY_AMBIGUITY


def _facts(state):
    return (state.maturity_level, state.current_stage,
            [(g.gap_type, g.status, g.iterations_open) for g in state.gaps],
            tuple(state.need_routing), pl.select_next_gap(state),
            [(r.record_id, r.disposition, r.gap_context, r.question_target)
             for r in state.assertions])


def _row_counts(sid):
    conn = _store()._conn
    return (conn.execute("SELECT COUNT(*) FROM need_routing_revisions WHERE "
                         "project_id = ?", (sid,)).fetchone()[0],
            conn.execute("SELECT COUNT(*) FROM records WHERE project_id = ?",
                         (sid,)).fetchone()[0])


def _retract(sid, state=None):
    head = _store().load_need_routing(sid)[-1]
    return nr.NeedRoutingRevision(
        project_id=sid, routing_seq=-1, gap_type=PHYSICAL_FEASIBILITY,
        question_id=PF_Q2, after_assertion_seq=-1, operation=nr.OPERATION_RETRACT,
        required_input=None, policy_ref=head.policy_ref,
        supersedes_seq=head.routing_seq, provenance=SYSTEM_INFERRED,
        event_key="nr:%s:retract:%d" % (sid, head.routing_seq))


# ===========================================================================
# 1-4. questioning vs satisfaction
# ===========================================================================

def test_01_pf_q2_is_no_longer_mandatory_owner_work():
    s = _state()
    served = _full_journey(s)
    assert PF_Q2 not in served
    assert served[0] == PF_Q1 and served[1] == BA_Q1
    assert not nr.eligible_for_owner_questioning(s, PHYSICAL_FEASIBILITY, PF_Q2)
    assert not nr.satisfied_for_maturity(s, PHYSICAL_FEASIBILITY, PF_Q2)


def test_01b_web_never_serves_pf_q2_in_the_question_slot(client):
    sid = _start(client)
    seen = []
    for text in (MECH, MECH, PF_STRONG, BA_1, BA_2):
        seen.append(_answer_form_target(client, sid)["q"])
        _answer(client, sid, text)
    assert ID(PF_Q1) in seen
    assert ID(PF_Q2) not in seen and PF_Q2 not in seen
    body = _body(client, sid)
    m = re.search(r'<form id="answer-form".*?</form>', body, re.S)
    assert PF_Q2_TEXT not in (m.group(0) if m else "")


def test_02_pf_q1_remains_owner_visible_and_unchanged(client):
    s = _to_pf(_state())
    assert _served_id(s) == PF_Q1
    assert pl.get_question("mechanical", PHYSICAL_FEASIBILITY, 0, path="N") == PF_Q1_TEXT
    assert pnq.get_served_question(PHYSICAL_FEASIBILITY, 0, domain="mechanical").routing is None
    sid = _start(client)
    _answer(client, sid, MECH)
    _answer(client, sid, MECH)
    assert _answer_form_target(client, sid)["q"] == ID(PF_Q1)
    assert PF_Q1_TEXT in _body(client, sid)


def test_03_boundary_questioning_continues_while_pf_q2_is_outstanding():
    s = _to_pf(_state())
    pl.run_iteration(s, PF_STRONG)
    assert pl.select_next_gap(s) == BOUNDARY_AMBIGUITY
    assert s.get_gap(BOUNDARY_AMBIGUITY).status == OPEN
    assert nr.gap_has_outstanding_routing(s, PHYSICAL_FEASIBILITY)
    # the legacy cascade would still be parked on PF
    old = _to_pf(_state(version=T2G2, routed=False))
    pl.run_iteration(old, PF_STRONG)
    assert pl.select_next_gap(old) == PHYSICAL_FEASIBILITY


def test_04_pf_stays_unresolved_and_visible_everywhere():
    s = _state()
    _full_journey(s)
    pf = s.get_gap(PHYSICAL_FEASIBILITY)
    assert pf.status in (OPEN, PARTIAL) and pf.closed_at is None
    assert PHYSICAL_FEASIBILITY in [g.gap_type for g in s.get_open_gaps()]
    ids = [r.requirement_id for r in derive_requirement_landscape(s).requirements]
    assert "req:gap:PHYSICAL_FEASIBILITY" in ids
    routed_id = "req:specialist:routing:PHYSICAL_FEASIBILITY:" + PF_Q2
    assert routed_id in ids
    steps = {st.step_id: st for st in derive_validation_plan(s).steps}
    assert steps["vstep:" + routed_id].responsibility == SPECIALIST_REQUIRED
    readiness = derive_readiness(s)
    assert readiness.is_verified(PHYSICAL_FEASIBILITY) is False
    assert PHYSICAL_FEASIBILITY in readiness.unverified_contexts()
    assert readiness.overall_verified() is False


# ===========================================================================
# 5-7. closure guards and the Level 1 -> 2 veto
# ===========================================================================

def _pf_pair(monkeypatch, quality, status):
    """(routed, unrouted control) at PF with ``status``; the quality ladder is
    pinned only AFTER both journeys reached PF."""
    routed, control = _to_pf(_state()), _to_pf(_state(routed=False))
    for s in (routed, control):
        s.get_gap(PHYSICAL_FEASIBILITY).status = status
    monkeypatch.setattr(pl, "assess_response", lambda *a, **k: quality)
    monkeypatch.setattr(pl, "addresses_gap", lambda *a, **k: True)
    return routed, control


def test_05_demonstrated_answer_cannot_close_routed_pf(monkeypatch):
    s, control = _pf_pair(monkeypatch, DEMONSTRATED, OPEN)
    result, _ = pl.integrate_response(s, PHYSICAL_FEASIBILITY, "", PF_STRONG)
    gap = s.get_gap(PHYSICAL_FEASIBILITY)
    assert gap.status == PARTIAL and gap.closed_at is None and result == "WARN"
    # control: the SAME answer closes an unrouted PF
    pl.integrate_response(control, PHYSICAL_FEASIBILITY, "", PF_STRONG)
    assert control.get_gap(PHYSICAL_FEASIBILITY).status == CLOSED


def test_06_reasoned_follow_up_cannot_close_routed_pf(monkeypatch):
    s, control = _pf_pair(monkeypatch, REASONED, PARTIAL)
    pl.integrate_response(s, PHYSICAL_FEASIBILITY, "", PF_STRONG)
    assert s.get_gap(PHYSICAL_FEASIBILITY).status == PARTIAL
    assert s.get_gap(PHYSICAL_FEASIBILITY).closed_at is None
    pl.integrate_response(control, PHYSICAL_FEASIBILITY, "", PF_STRONG)
    assert control.get_gap(PHYSICAL_FEASIBILITY).status == CLOSED


def test_06b_real_strong_answers_never_close_routed_pf():
    s = _to_pf(_state())
    for _ in range(4):
        pl.integrate_response(s, PHYSICAL_FEASIBILITY, "", PF_STRONG)
    assert s.get_gap(PHYSICAL_FEASIBILITY).status != CLOSED


def test_07_routed_open_or_partial_pf_blocks_level_1_to_2():
    for status in (OPEN, PARTIAL):
        s = _state()
        _full_journey(s)
        assert s.get_gap(BOUNDARY_AMBIGUITY).status == CLOSED
        s.get_gap(PHYSICAL_FEASIBILITY).status = status
        can, reason = pl.evaluate_transition(s)
        assert can is False and PHYSICAL_FEASIBILITY in reason
        assert pl._level1_blocking_gap(s) == PHYSICAL_FEASIBILITY
        pl.run_iteration(s, "")
        assert s.maturity_level == 1


def test_07b_accepted_risk_is_a_maturity_exception_not_a_discharge():
    s = _state()
    _full_journey(s)
    pl.accept_gap_risk(s, PHYSICAL_FEASIBILITY)        # the existing OD-R1 writer
    can, _ = pl.evaluate_transition(s)
    assert can is True and pl._level1_blocking_gap(s) is None
    # the routed requirement is still outstanding and unresolved
    assert nr.gap_has_outstanding_routing(s, PHYSICAL_FEASIBILITY)
    assert not nr.satisfied_for_maturity(s, PHYSICAL_FEASIBILITY, PF_Q2)
    assert s.get_gap(PHYSICAL_FEASIBILITY).closed_at is None


def test_07c_other_level_1_to_2_requirements_still_govern():
    s = _to_pf(_state())
    pl.run_iteration(s, PF_STRONG)                 # PF exhausted; BA opened, not closed
    pl.accept_gap_risk(s, PHYSICAL_FEASIBILITY)
    can, reason = pl.evaluate_transition(s)
    assert can is False and BOUNDARY_AMBIGUITY in reason
    assert pl._level1_blocking_gap(s) == BOUNDARY_AMBIGUITY


def _accept_pf_via_route(c, sid, confirm="yes"):
    raw = c.get(f"/session/{sid}").get_data(as_text=True)
    token = re.search(r'name="answer_token" value="([^"]*)"', raw).group(1)
    return c.post(f"/session/{sid}/accept-risk", data={
        "answer_token": token, "gap_type": PHYSICAL_FEASIBILITY,
        "risk_confirm": confirm, "reason": "Accepting the open limits for now."})


def test_07d_explicit_od_r1_acceptance_of_routed_pf_reaches_level_2(client):
    sid = _start(client)
    _web_to_ba(client, sid)
    _answer(client, sid, BA_1)
    _answer(client, sid, BA_2)
    state = _live(sid)
    assert state.get_gap(BOUNDARY_AMBIGUITY).status == CLOSED
    assert state.maturity_level == 1                   # blocked by routed PF
    body = _body(client, sid)
    block = re.search(r'<div class="routed-need.*?</details>', body, re.S).group(0)
    assert 'action="/session/%s/accept-risk"' % sid in block
    # never silent: without the explicit confirmation nothing changes
    _accept_pf_via_route(client, sid, confirm="")
    assert _live(sid).get_gap(PHYSICAL_FEASIBILITY).status != ACCEPTED_RISK
    assert _accept_pf_via_route(client, sid).status_code == 302
    state = _live(sid)
    assert state.get_gap(PHYSICAL_FEASIBILITY).status == ACCEPTED_RISK
    assert state.maturity_level == 2
    records = _store().load_contract(sid).assertions
    risk = [r for r in records if r.disposition == "risk_accepted"]
    assert len(risk) == 1 and risk[0].provenance == OWNER_STATED
    assert risk[0].gap_context == PHYSICAL_FEASIBILITY
    # NeedRouting untouched; PF still technically unresolved
    assert [r.operation for r in _store().load_need_routing(sid)] == ["ROUTE"]
    assert nr.gap_has_outstanding_routing(state, PHYSICAL_FEASIBILITY)
    assert state.get_gap(PHYSICAL_FEASIBILITY).closed_at is None
    # nothing specialist / evidence / validated was fabricated
    assert not any(r.disposition in (DISPOSITION_SPECIALIST_REQUESTED,
                                     DISPOSITION_EVIDENCE_REQUESTED) for r in records)
    assert all(r.validation_status == UNVALIDATED for r in records)
    readiness = derive_readiness(state)
    assert readiness.is_verified(PHYSICAL_FEASIBILITY) is False
    assert readiness.overall_verified() is False
    # still visible, and still truthful: accepted risk is not a resolved need
    ids = [r.requirement_id for r in derive_requirement_landscape(state).requirements]
    assert "req:specialist:routing:PHYSICAL_FEASIBILITY:" + PF_Q2 in ids
    steps = {st.step_id: st for st in derive_validation_plan(state).steps}
    assert steps["vstep:req:specialist:routing:PHYSICAL_FEASIBILITY:" + PF_Q2
                 ].responsibility == SPECIALIST_REQUIRED
    body = _body(client, sid)
    assert "Specialist input required" in body
    assert "Technical operating limits remain unresolved." in body
    assert "routed-accept-risk" not in body            # accepted once, not re-offered
    deliverable = _html.unescape(client.get(
        f"/session/{sid}/deliverable").get_data(as_text=True))
    assert "specialist input is required" in deliverable.lower()
    # replay and writable resume reconstruct the same accepted-risk + routing state
    live = _facts(state)
    assert _facts(SR.reconstruct_readonly_state(_store(), sid).state) == live
    appmod.SESSION_STORE.pop(sid)
    assert client.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _facts(_live(sid)) == live
    # the Target-Aware routed note still binds to PF:Q2 after acceptance
    form = _routed_form(client, sid)
    assert _decode(form["answer_target"])["q"] == ID(PF_Q2)
    client.post(f"/session/{sid}", data=dict(
        form, action="provisional_assumption", response=NOTE), answer_binding=False)
    note = _store().load_contract(sid).assertions[-1]
    assert (note.question_target, note.gap_context) == (ID(PF_Q2), PHYSICAL_FEASIBILITY)
    assert nr.gap_has_outstanding_routing(_live(sid), PHYSICAL_FEASIBILITY)


def test_07e_od_r1_safeguards_are_unchanged_for_routed_pf(client):
    sid = _start(client)
    _answer(client, sid, MECH)
    _answer(client, sid, MECH)
    # PF served but no substantive attempt yet: the W2-D gate refuses
    _accept_pf_via_route(client, sid)
    assert _live(sid).get_gap(PHYSICAL_FEASIBILITY).status == OPEN
    assert "routed-accept-risk" not in _body(client, sid)
    # MECHANISM_COMPLETENESS is never a target, routed or not
    raw = client.get(f"/session/{sid}").get_data(as_text=True)
    token = re.search(r'name="answer_token" value="([^"]*)"', raw).group(1)
    client.post(f"/session/{sid}/accept-risk", data={
        "answer_token": token, "gap_type": MECHANISM_COMPLETENESS,
        "risk_confirm": "yes"})
    assert _live(sid).get_gap(MECHANISM_COMPLETENESS).status == CLOSED
    assert appmod._routed_risk_targets(_live(sid)) == ()


def test_07f_retract_is_not_a_route_to_maturity(client):
    sid = _start(client)
    _web_to_ba(client, sid)
    _answer(client, sid, BA_1)
    _answer(client, sid, BA_2)
    _store().append_need_routing(sid, _retract(sid))
    cold = SR.reconstruct_readonly_state(_store(), sid).state
    assert not nr.gap_has_outstanding_routing(cold, PHYSICAL_FEASIBILITY)
    # the unrouted PF is simply Owner work again; nothing was satisfied
    assert cold.get_gap(PHYSICAL_FEASIBILITY).status in (OPEN, PARTIAL)
    assert cold.maturity_level == 1
    assert pl.evaluate_transition(cold)[0] is False


# ===========================================================================
# 8-12. record / provenance / validation / evidence boundaries
# ===========================================================================

def test_08_routing_creates_no_owner_assertion_record(client):
    sid = _start(client)
    assert list(_store().load_contract(sid).assertions) == []
    assert _live(sid).assertions == []
    assert len(_store().load_need_routing(sid)) == 1
    _web_to_ba(client, sid)
    for rec in _store().load_contract(sid).assertions:
        assert rec.disposition not in (DISPOSITION_SPECIALIST_REQUESTED,
                                       DISPOSITION_EVIDENCE_REQUESTED)
        assert rec.provenance != SYSTEM_INFERRED
    assert len(_store().load_contract(sid).assertions) == 3   # the 3 Owner answers


def test_09_routing_provenance_is_system_inferred_only(client, tmp_path):
    sid = _start(client)
    rows = _store().load_need_routing(sid)
    assert [r.provenance for r in rows] == [SYSTEM_INFERRED]
    bad = dataclasses.replace(rows[0], provenance=OWNER_STATED)
    with pytest.raises(nr.NeedRoutingError):
        nr.validate_revision_fields(bad)
    with pytest.raises(sqlite3.IntegrityError):
        _store()._conn.execute(
            "INSERT INTO need_routing_revisions (project_id, routing_seq, gap_type, "
            "question_id, after_assertion_seq, operation, required_input, policy_ref, "
            "supersedes_seq, provenance, event_key) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (sid, 9, PHYSICAL_FEASIBILITY, PF_Q2, -1, "ROUTE", "SPECIALIST",
             rows[0].policy_ref, None, OWNER_STATED, "x"))


def test_10_no_validation_promotion(client):
    sid = _start(client)
    _web_to_ba(client, sid)
    state = _live(sid)
    assert all(r.validation_status == UNVALIDATED for r in state.assertions)
    assert not any(r.validation_status in VALIDATED_STATUSES for r in state.assertions)
    assert derive_readiness(state).overall_verified() is False


def test_11_no_evidence_is_fabricated():
    routed, plain = _state(), _state(routed=False)
    for s in (routed, plain):
        _to_pf(s)
    assert [g.evidence for g in routed.gaps] == [g.evidence for g in plain.gaps]
    assert routed.acknowledged_unknowns == plain.acknowledged_unknowns
    assert routed.known_mechanism == plain.known_mechanism
    assert routed.assertions == [] and plain.assertions == []


def test_12_specialist_required_never_becomes_specialist_reviewed(client):
    s = _state()
    _full_journey(s)
    for step in derive_validation_plan(s).steps:
        assert "reviewed" not in step.statement.lower()
    sid = _start(client)
    _web_to_ba(client, sid)
    block = re.search(r'<div class="routed-need.*?</form>',
                      _body(client, sid), re.S).group(0).lower()
    for word in FORBIDDEN_CLAIMS:
        assert not re.search(r"\b%s\b" % word, block), word


# ===========================================================================
# 13-17. replay, correction, idempotency, failure, ambiguity
# ===========================================================================

def test_13_live_reconstructed_and_resumed_state_agree(client):
    sid = _start(client)
    _web_to_ba(client, sid)
    _answer(client, sid, BA_1)
    live = _facts(_live(sid))
    cold = SR.reconstruct_readonly_state(_store(), sid).state
    assert _facts(cold) == live
    appmod.SESSION_STORE.pop(sid)
    assert client.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _facts(_live(sid)) == live


def test_14a_owner_correction_replays_routing_in_durable_order(client):
    sid = _start(client)
    _web_to_ba(client, sid)
    first = _store().load_contract(sid).assertions[0].record_id
    raw = client.get(f"/session/{sid}").get_data(as_text=True)
    token = re.search(r'name="answer_token" value="([^"]*)"', raw).group(1)
    r = client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": first, "response": MECH, "answer_token": token})
    assert r.status_code == 302
    state = _live(sid)
    assert nr.gap_has_outstanding_routing(state, PHYSICAL_FEASIBILITY)
    assert state.get_gap(PHYSICAL_FEASIBILITY).status != CLOSED
    assert _facts(SR.reconstruct_readonly_state(_store(), sid).state) == _facts(state)


def test_14b_retract_and_reroute_replay_truthfully(client):
    sid = _start(client)
    _web_to_ba(client, sid)
    before = _live(sid).get_gap(PHYSICAL_FEASIBILITY).status
    assert _store().append_need_routing(sid, _retract(sid)) == NEED_ROUTING_INSERTED
    rows = _store().load_need_routing(sid)
    assert [r.operation for r in rows] == ["ROUTE", "RETRACT"]
    assert rows[1].after_assertion_seq == 2          # after the third Owner record
    cold = SR.reconstruct_readonly_state(_store(), sid).state
    # RETRACT withdraws the routing; it claims nothing was solved
    assert not nr.gap_has_outstanding_routing(cold, PHYSICAL_FEASIBILITY)
    assert cold.get_gap(PHYSICAL_FEASIBILITY).status == before
    assert cold.get_gap(PHYSICAL_FEASIBILITY).closed_at is None
    assert pl.select_next_gap(cold) == PHYSICAL_FEASIBILITY     # Owner-eligible again
    assert _served_id(cold) == PF_Q2
    reroute = nr.NeedRoutingRevision(
        project_id=sid, routing_seq=-1, gap_type=PHYSICAL_FEASIBILITY,
        question_id=PF_Q2, after_assertion_seq=-1, operation=nr.OPERATION_ROUTE,
        required_input="SPECIALIST", policy_ref=rows[0].policy_ref,
        supersedes_seq=1, provenance=SYSTEM_INFERRED, event_key="nr:%s:re" % sid)
    assert _store().append_need_routing(sid, reroute) == NEED_ROUTING_INSERTED
    again = SR.reconstruct_readonly_state(_store(), sid).state
    assert nr.gap_has_outstanding_routing(again, PHYSICAL_FEASIBILITY)
    assert pl.select_next_gap(again) == BOUNDARY_AMBIGUITY
    # the Owner ledger was never edited
    assert [r.disposition for r in _store().load_contract(sid).assertions] == \
        ["answered"] * 3


def test_14c_chain_rules_refuse_invalid_corrections(client):
    sid = _start(client)
    head = _store().load_need_routing(sid)[0]
    double_route = dataclasses.replace(
        _retract(sid), operation=nr.OPERATION_ROUTE, required_input="SPECIALIST",
        event_key="nr:dbl")
    with pytest.raises(NeedRoutingHistoryError):
        _store().append_need_routing(sid, double_route)
    wrong_head = dataclasses.replace(_retract(sid), supersedes_seq=None,
                                     event_key="nr:nohead")
    with pytest.raises(NeedRoutingHistoryError):
        _store().append_need_routing(sid, wrong_head)
    other_question = dataclasses.replace(_retract(sid), question_id=PF_Q1,
                                         event_key="nr:q1")
    with pytest.raises(NeedRoutingHistoryError):
        _store().append_need_routing(sid, other_question)
    assert _store().load_need_routing(sid) == (head,)


def test_15_retries_and_duplicates_are_idempotent(client):
    sid = _start(client)
    rev = _retract(sid)
    assert _store().append_need_routing(sid, rev) == NEED_ROUTING_INSERTED
    assert _store().append_need_routing(sid, rev) == NEED_ROUTING_EXACT_REPLAY
    assert len(_store().load_need_routing(sid)) == 2
    clash = dataclasses.replace(rev, policy_ref="other")
    with pytest.raises(NeedRoutingConflict):
        _store().append_need_routing(sid, clash)
    # the optional note: a double submit of the same form is one record
    sid2 = _start(client)
    _web_to_ba(client, sid2)
    form = _routed_form(client, sid2)
    data = dict(form, action="provisional_assumption", response=NOTE)
    client.post(f"/session/{sid2}", data=data, answer_binding=False)
    n = len(_store().load_contract(sid2).assertions)
    client.post(f"/session/{sid2}", data=data, answer_binding=False)
    assert len(_store().load_contract(sid2).assertions) == n


def test_16_failed_writes_publish_no_phantom_routing(client, monkeypatch, tmp_path):
    store = SqliteRecordStore(str(tmp_path / "fail.sqlite"))
    try:
        revs = nr.creation_revisions("p-f", "mechanical", "N", NR1)

        def boom(*a, **k):
            raise sqlite3.OperationalError("injected")
        monkeypatch.setattr(store, "_insert_need_routing", boom)
        with pytest.raises(sqlite3.OperationalError):
            store.create_project(
                ProjectRecordContract.from_state(IdeaState(idea_id="f")),
                project_id="p-f",
                reconstruction_inputs={"seed_idea_text": "s", "confirmed_domain":
                                       "mechanical", "path": "N",
                                       "engine_contract_version": NR1},
                need_routing=revs)
        assert store._conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0] == 0
        assert store._conn.execute(
            "SELECT COUNT(*) FROM need_routing_revisions").fetchone()[0] == 0
    finally:
        store.close()
    # the live /start publishes nothing when durable creation fails
    monkeypatch.setattr(appmod._get_store(), "create_project",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("down")))
    before = set(appmod.SESSION_STORE)
    r = client.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
    assert r.status_code == 503 and set(appmod.SESSION_STORE) == before


class _CommitThenRaise:
    def __init__(self, conn):
        self._conn = conn
        self.armed = True

    def execute(self, sql, *args):
        if sql == "COMMIT" and self.armed:
            self.armed = False
            self._conn.execute("COMMIT")
            raise sqlite3.OperationalError("injected: error after the commit point")
        return self._conn.execute(sql, *args)

    def __getattr__(self, name):
        return getattr(self._conn, name)


class _CommitAndRollbackFail:
    def __init__(self, conn):
        self._conn = conn
        self.armed = True

    def execute(self, sql, *args):
        if self.armed and sql in ("COMMIT", "ROLLBACK"):
            if sql == "ROLLBACK":
                self.armed = False
            raise sqlite3.OperationalError("injected: %s failed" % sql)
        return self._conn.execute(sql, *args)

    def __getattr__(self, name):
        return getattr(self._conn, name)


def test_17_ambiguous_commit_outcomes_are_resolved_truthfully(client):
    sid = _start(client)
    store = _store()
    real = store._conn
    rev = _retract(sid)
    try:
        store._conn = _CommitThenRaise(real)
        with pytest.raises(sqlite3.OperationalError):
            store.append_need_routing(sid, rev)
        store._conn = real
        # confirm by reload: the SAME event is recognized, never written twice
        assert store.append_need_routing(sid, rev) == NEED_ROUTING_EXACT_REPLAY
        assert len(store.load_need_routing(sid)) == 2
        reroute = dataclasses.replace(
            rev, operation=nr.OPERATION_ROUTE, required_input="SPECIALIST",
            supersedes_seq=1, event_key="nr:%s:unresolved" % sid)
        store._conn = _CommitAndRollbackFail(real)
        with pytest.raises(sqlite3.OperationalError):
            store.append_need_routing(sid, reroute)
        assert store.committed_state_readable() is False
        # never a write on top of an unresolved transaction
        with pytest.raises(RecordStoreConnectionUnsafe):
            store.append_need_routing(sid, reroute)
        # and the read snapshot opens nothing on it
        with store.read_snapshot():
            pass
        assert store.committed_state_readable() is False
    finally:
        store._conn = real
        if real.in_transaction:
            real.execute("ROLLBACK")


# ===========================================================================
# 18-20. versions and MECHANISM_COMPLETENESS
# ===========================================================================

def test_18_existing_versions_keep_the_ten_question_behavior(client):
    for version in (SR.RECONSTRUCTION_VERSION, SR.ENGINE_CONTRACT_VERSION_T2G1, T2G2):
        assert nr.creation_revisions("p", "mechanical", "N", version) == ()
        sid = _stamped_start(client, version)
        assert _store().load_need_routing(sid) == ()
        assert _live(sid).need_routing == []
    s = _to_pf(_state(version=T2G2, routed=False))
    pl.run_iteration(s, PF_STRONG)
    if s.get_gap(PHYSICAL_FEASIBILITY).status != CLOSED:
        assert _served_id(s) == PF_Q2
    ids = [e["question_id"] for v in json.load(open(os.path.join(
        os.path.dirname(pnq.__file__), "..", "docs", "governance",
        "path_n_content_config", "mechanical_path_n_questions.json"),
        encoding="utf-8"))["gaps"].values() for e in v]
    assert len(ids) == 10 and PF_Q2 in ids


def test_18b_routing_on_a_non_routing_version_fails_closed(client):
    sid = _stamped_start(client, T2G2)
    _store()._conn.execute(
        "INSERT INTO need_routing_revisions (project_id, routing_seq, gap_type, "
        "question_id, after_assertion_seq, operation, required_input, policy_ref, "
        "supersedes_seq, provenance, event_key) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (sid, 0, PHYSICAL_FEASIBILITY, PF_Q2, -1, "ROUTE", "SPECIALIST",
         "mechanical-path-n-routing-v1:PHYSICAL_FEASIBILITY:Q2", None,
         SYSTEM_INFERRED, "forged"))
    with pytest.raises(nr.NeedRoutingError):
        SR.reconstruct_readonly_state(_store(), sid)
    with pytest.raises(NeedRoutingConflict):
        _store().append_need_routing(sid, dataclasses.replace(
            _retract(sid), event_key="nr:t2g2"))


def test_19_new_routing_aware_project_uses_the_new_behavior(client):
    assert appmod.CURRENT_ENGINE_CONTRACT_VERSION == NR1
    sid = _start(client)
    assert _live(sid).engine_contract_version == NR1
    rows = _store().load_need_routing(sid)
    assert [(r.gap_type, r.question_id, r.operation, r.required_input,
             r.after_assertion_seq) for r in rows] == [
        (PHYSICAL_FEASIBILITY, PF_Q2, "ROUTE", "SPECIALIST", -1)]
    assert NR1 in SR.SUPPORTED_ENGINE_CONTRACT_VERSIONS
    # T2-G-2 rules are carried unchanged
    from engine.answer_stance import t2g_rule_level
    assert t2g_rule_level(_live(sid), MECHANISM_COMPLETENESS) == 2


def test_20_mechanism_completeness_is_rejected_at_every_boundary(client):
    # artifact validation
    entry = {"question_id": "x", "text": "t", "routing": {
        "required_input": "SPECIALIST", "policy_ref": "p", "need_text": "n",
        "need_text_ar": "n", "owner_input_prompt": "o",
        "owner_input_prompt_ar": "o"}}
    with pytest.raises(ValueError):
        pnq._routing_from_entry(entry, MECHANISM_COMPLETENESS, 0)
    # routing mint
    sid = _start(client)
    mc = dataclasses.replace(_store().load_need_routing(sid)[0],
                             gap_type=MECHANISM_COMPLETENESS,
                             question_id="mechanical:MECHANISM_COMPLETENESS:Q4")
    with pytest.raises(nr.NeedRoutingError):
        nr.validate_revision_fields(mc)
    with pytest.raises(NeedRoutingHistoryError):
        _store().append_need_routing(sid, dataclasses.replace(
            mc, routing_seq=1, supersedes_seq=None, event_key="nr:mc"))
    # routing load (database backstop) and replay/apply
    with pytest.raises(sqlite3.IntegrityError):
        _store()._conn.execute(
            "INSERT INTO need_routing_revisions (project_id, routing_seq, gap_type, "
            "question_id, after_assertion_seq, operation, required_input, "
            "policy_ref, supersedes_seq, provenance, event_key) VALUES "
            "(?,?,?,?,?,?,?,?,?,?,?)",
            (sid, 5, MECHANISM_COMPLETENESS, mc.question_id, -1, "ROUTE",
             "SPECIALIST", "p", None, SYSTEM_INFERRED, "mc"))
    with pytest.raises(nr.NeedRoutingError):
        nr.validate_routing_history([mc])
    s = _state(routed=False)
    with pytest.raises(nr.NeedRoutingError):
        nr.apply_revision(s, mc)
    # question eligibility: MC questioning is never exhausted by routing
    assert pl.select_next_gap(s) == MECHANISM_COMPLETENESS
    with pytest.raises(ValueError):
        pl.accept_gap_risk(s, MECHANISM_COMPLETENESS)


# ===========================================================================
# 21-24. Target-Aware identity, optional note, copy, render purity
# ===========================================================================

def test_21_target_aware_identities_stay_exact(client):
    sid = _start(client)
    _web_to_ba(client, sid)
    records = _store().load_contract(sid).assertions
    targets = [r.question_target for r in records]
    assert len(targets) == 3
    assert all(t.startswith(ID("mechanical:MECHANISM_COMPLETENESS:"))
               for t in targets[:2])
    assert targets[2] == ID(PF_Q1) and records[2].gap_context == PHYSICAL_FEASIBILITY
    assert _answer_form_target(client, sid)["q"] == ID(BA_Q1)


def test_22_optional_note_binds_to_pf_q2_while_ba_is_primary(client):
    sid = _start(client)
    _web_to_ba(client, sid)
    form = _routed_form(client, sid)
    assert _decode(form["answer_target"]) == {
        "k": "ROUTED_NEED", "q": ID(PF_Q2), "g": PHYSICAL_FEASIBILITY, "v": NR1}
    before = _facts(_live(sid))
    client.post(f"/session/{sid}", data=dict(
        form, action="provisional_assumption", response=NOTE), answer_binding=False)
    rec = _store().load_contract(sid).assertions[-1]
    assert (rec.disposition, rec.gap_context, rec.question_target,
            rec.provenance, rec.content) == (
        "provisional_assumption", PHYSICAL_FEASIBILITY, ID(PF_Q2), OWNER_STATED, NOTE)
    state = _live(sid)
    # the note establishes and discharges nothing
    assert nr.gap_has_outstanding_routing(state, PHYSICAL_FEASIBILITY)
    assert _facts(state)[:5] == before[:5]
    assert pl.select_next_gap(state) == BOUNDARY_AMBIGUITY


def test_22b_routed_form_refuses_other_actions_stale_and_swapped_targets(client):
    sid = _start(client)
    _web_to_ba(client, sid)
    n = len(_store().load_contract(sid).assertions)
    form = _routed_form(client, sid)
    client.post(f"/session/{sid}", data=dict(form, action="answered",
                response=NOTE), answer_binding=False)
    form = _routed_form(client, sid)
    client.post(f"/session/{sid}", data=dict(form, action="provisional_assumption",
                response=""), answer_binding=False)
    assert len(_store().load_contract(sid).assertions) == n
    # after a RETRACT the need is no longer outstanding: the old form is dead
    form = _routed_form(client, sid)
    _store().append_need_routing(sid, _retract(sid))
    nr.apply_revision(_live(sid), _store().load_need_routing(sid)[-1])
    client.post(f"/session/{sid}", data=dict(form, action="provisional_assumption",
                response=NOTE), answer_binding=False)
    assert len(_store().load_contract(sid).assertions) == n
    assert appmod.SESSION_STORE[sid].get("_answer_error") == \
        appmod.ANSWER_FORM_STALE_MESSAGE


def test_23_english_and_arabic_copy_is_truthful_and_one_identity(client):
    sid = _start(client)
    _web_to_ba(client, sid)
    en = _body(client, sid)
    assert "Specialist input required" in en
    assert "Technical operating limits remain unresolved." in en
    assert "Add intended use conditions if known." in en
    assert 'data-routed-question="%s"' % PF_Q2 in en
    client.post("/ui-language", data={"lang": "ar"})
    ar = _body(client, sid)
    assert "مدخلات مختص مطلوبة" in ar
    assert "الحدود التشغيلية الفنية ما زالت غير محسومة." in ar
    assert "يمكنك إضافة ظروف الاستخدام المقصودة إذا كنت تعرفها." in ar
    assert 'data-routed-question="%s"' % PF_Q2 in ar
    block_ar = re.search(r'<div class="routed-need.*?</form>', ar, re.S).group(0)
    for phrase in FORBIDDEN_CLAIMS_AR:
        assert phrase not in block_ar
    assert PF_Q2_TEXT not in en and PF_Q2_TEXT_AR not in ar


def test_24_repeated_rendering_writes_nothing(client):
    sid = _start(client)
    _web_to_ba(client, sid)
    before = _row_counts(sid)
    for _ in range(4):
        _body(client, sid)
        client.get(f"/session/{sid}/deliverable")
    SR.reconstruct_readonly_state(_store(), sid)
    assert _row_counts(sid) == before


# ===========================================================================
# 25-27. electronics, BA:Q3 / BA:Q4, no network or model
# ===========================================================================

def test_25_electronics_is_unchanged(client):
    assert pnq.routing_policies("electronics_electrical") == ()
    assert pnq.routing_policies(None) == ()
    sid = _start(client, seed=ELEC_SEED, domain="electronics_electrical")
    assert _store().load_need_routing(sid) == ()
    assert _live(sid).need_routing == []
    assert 'class="routed-need' not in _body(client, sid)


def test_26_boundary_q3_q4_are_unchanged():
    policies = pnq.routing_policies("mechanical")
    assert [(g, q) for g, q, _ in policies] == [(PHYSICAL_FEASIBILITY, PF_Q2)]
    for index in range(4):
        served = pnq.get_served_question(BOUNDARY_AMBIGUITY, index, domain="mechanical")
        assert served.routing is None
        assert served.question_id == "mechanical:BOUNDARY_AMBIGUITY:Q%d" % (index + 1)
    s = _state()
    assert not nr.outstanding_routed_question_ids(s, BOUNDARY_AMBIGUITY)


def test_27_no_network_or_model_path_is_reachable(client, monkeypatch):
    def refuse(*a, **k):
        raise AssertionError("network or model call attempted")
    monkeypatch.setattr(socket.socket, "connect", refuse)
    import engine.ai_advisor as advisor
    monkeypatch.setattr(advisor, "get_ai_question", refuse)
    sid = _start(client)
    _web_to_ba(client, sid)
    _body(client, sid)
    SR.reconstruct_readonly_state(_store(), sid)
