"""Wave-1 RVR-1 — Truthful unknown progression & completion semantics.

Contract: docs/governance/WAVE_1_REMEDIATION_IMPLEMENTATION_CONTRACTS.md (RVR-1).
Covers: the single canonical ACCEPTED_RISK writer; mechanism refusal; completion
semantics; deliverable truthfulness; the explicit route (auth/token/confirmation/
persistence/idempotency); replay determinism of recorded acceptances.
"""
import os, sys, tempfile, uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from engine.idea_state import (
    IdeaState, Gap, OPEN, PARTIAL, CLOSED, ACCEPTED_RISK,
    INTERACTION_DISPOSITIONS, DISPOSITION_RISK_ACCEPTED,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
    OWNER_STATED, Evidence, REASONED,
)
from engine.progression_loop import (
    accept_gap_risk, evaluate_transition, select_next_gap,
)
from engine.deliverable_assembler import assemble_deliverable


# --- vocabulary boundaries ---------------------------------------------------

def test_seventh_disposition_exists_and_ws12_vocabulary_stays_disjoint():
    from engine.controlled_unknown_progression import (
        WS12_UNKNOWN_PATH_CLASSIFICATIONS)
    assert DISPOSITION_RISK_ACCEPTED in INTERACTION_DISPOSITIONS
    assert WS12_UNKNOWN_PATH_CLASSIFICATIONS.isdisjoint(INTERACTION_DISPOSITIONS)
    assert "ACCEPTED_RISK" not in INTERACTION_DISPOSITIONS


def test_web_answered_action_allowlist_unchanged():
    from web.app import INTERACTION_ACTIONS
    assert INTERACTION_ACTIONS == {
        "answered", "unknown", "deferred", "provisional_assumption",
        "specialist_requested", "evidence_requested"}


def test_risk_accepted_record_provenance_is_owner_stated():
    s = IdeaState(idea_id="x")
    r = s.record_interaction(action=DISPOSITION_RISK_ACCEPTED, content="why",
                             gap_context=PHYSICAL_FEASIBILITY, iteration=3)
    assert r.provenance == OWNER_STATED
    assert r.resolves_gap is False


# --- canonical lifecycle writer ---------------------------------------------

def _state_with(gap_type, status):
    s = IdeaState(idea_id="x")
    s.gaps.append(Gap(gap_type=gap_type, status=status, opened_at=1))
    return s

def test_accept_from_open_and_partial():
    for st in (OPEN, PARTIAL):
        s = _state_with(PHYSICAL_FEASIBILITY, st)
        accept_gap_risk(s, PHYSICAL_FEASIBILITY)
        assert s.gaps[0].status == ACCEPTED_RISK
        assert s.gaps[0].closed_at is None

def test_mechanism_can_never_be_risk_accepted():
    s = _state_with(MECHANISM_COMPLETENESS, OPEN)
    with pytest.raises(ValueError):
        accept_gap_risk(s, MECHANISM_COMPLETENESS)
    assert s.gaps[0].status == OPEN

def test_closed_and_accepted_never_move():
    for st in (CLOSED, ACCEPTED_RISK):
        s = _state_with(PHYSICAL_FEASIBILITY, st)
        with pytest.raises(ValueError):
            accept_gap_risk(s, PHYSICAL_FEASIBILITY)
        assert s.gaps[0].status == st

def test_missing_gap_refused():
    with pytest.raises(ValueError):
        accept_gap_risk(IdeaState(idea_id="x"), PHYSICAL_FEASIBILITY)

def test_accepted_risk_gap_not_selected_and_not_open():
    s = _state_with(PHYSICAL_FEASIBILITY, OPEN)
    accept_gap_risk(s, PHYSICAL_FEASIBILITY)
    assert select_next_gap(s) is None
    assert s.get_open_gaps() == []


# --- completion semantics ----------------------------------------------------

def _level1_state(feas_status, bound_status):
    s = IdeaState(idea_id="x")
    s.maturity_level = 1
    s.known_mechanism = Evidence(content="m", quality=REASONED, iteration=1)
    s.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=1))
    s.gaps.append(Gap(gap_type=PHYSICAL_FEASIBILITY, status=feas_status, opened_at=2))
    s.gaps.append(Gap(gap_type=BOUNDARY_AMBIGUITY, status=bound_status, opened_at=3))
    return s

def test_accepted_risk_counts_toward_level2():
    ok, reason = evaluate_transition(_level1_state(ACCEPTED_RISK, CLOSED))
    assert ok, reason
    ok, reason = evaluate_transition(_level1_state(ACCEPTED_RISK, ACCEPTED_RISK))
    assert ok, reason

def test_open_gap_still_blocks_level2():
    ok, reason = evaluate_transition(_level1_state(OPEN, CLOSED))
    assert not ok and "PHYSICAL_FEASIBILITY" in reason

def test_mechanism_must_still_be_closed():
    s = _level1_state(CLOSED, CLOSED)
    s.get_gap(MECHANISM_COMPLETENESS).status = PARTIAL
    ok, reason = evaluate_transition(s)
    assert not ok


# --- deliverable truthfulness ------------------------------------------------

def test_deliverable_shows_accepted_risk_everywhere():
    s = _state_with(PHYSICAL_FEASIBILITY, OPEN)
    s.record_interaction(action=DISPOSITION_RISK_ACCEPTED, content="",
                         gap_context=PHYSICAL_FEASIBILITY, iteration=1)
    accept_gap_risk(s, PHYSICAL_FEASIBILITY)
    pkg = assemble_deliverable(s)
    s8 = pkg["section_8_unresolved_items"]
    risk_items = [i for i in s8["items"] if i["type"] == "accepted_risk"]
    assert len(risk_items) == 1 and s8["accepted_risk_count"] == 1
    item = risk_items[0]
    assert "NOT resolved" in item["resolution"]
    assert item["path_classification"] == "DEFERRED_BY_USER"
    a = pkg["section_7_recommendations"]["category_a_proceed_revise_block"]
    assert a["basis"]["accepted_risk_count"] == 1
    assert "ACCEPTED RISK" in a["rationale"]
    assert "not resolved" in a["rationale"]
    cat_d = pkg["section_7_recommendations"]["category_d_open_items"]
    assert any(i.get("item_type") == "accepted_risk" for i in cat_d)

def test_no_accepted_risk_means_no_qualifier():
    s = _state_with(PHYSICAL_FEASIBILITY, OPEN)
    pkg = assemble_deliverable(s)
    a = pkg["section_7_recommendations"]["category_a_proceed_revise_block"]
    assert a["basis"]["accepted_risk_count"] == 0
    assert "ACCEPTED RISK" not in a["rationale"]


# --- route + persistence + replay -------------------------------------------

@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "rvr1.sqlite"))
    import web.app as appmod
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with appmod.app.test_client() as c:
        yield c, appmod

SEED = ("a manually foldable wheelchair ramp for a home doorway — the inventor "
        "wants the ramp to stay reliably locked in the flat, load-bearing "
        "position and to fold away without tools")
# Proven-relevant mechanism answer (frozen S2 run corpus, M-1 novice answer 1 —
# closed MECHANISM_COMPLETENESS live in the recorded run).
MECH = ("The ramp folds up and down by hand. When it is down flat, it must "
        "stay firmly held so a wheelchair can roll over it. I am considering "
        "three ways to hold it: a toggle latch that snaps over its center, a "
        "spring pin that clicks into place, or a small gate piece that drops "
        "into place by its own weight.")

def _start(c):
    r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
    assert r.status_code == 302 and "/session/" in r.headers["Location"]
    return r.headers["Location"].rsplit("/", 1)[-1]

def _token(c, sid):
    import re, html
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    m = re.search(r'name="answer_token" value="([^"]+)"', page)
    return html.unescape(m.group(1))

def _answer_until(c, appmod, sid, gap, max_steps=8):
    from engine.progression_loop import select_next_gap as sng
    state = appmod.SESSION_STORE[sid]["state"]
    steps = 0
    while sng(state) == gap and steps < max_steps:
        c.post(f"/session/{sid}", data={"response": MECH,
                                        "answer_token": _token(c, sid),
                                        "action": "answered"})
        steps += 1

# W2-D reconciliation (Wave-2 contract §F, W1-S2 — intentional new
# expectation): Accept Risk now requires at least one ACTIVE substantive
# attempt (active-set rule) for the served gap. These substantive-but-
# unresolved attempts unlock the gate without closing the gap.
_ATTEMPT = {
    PHYSICAL_FEASIBILITY: ("I have not tested whether the toggle latch stays "
                           "reliable under repeated loading and outdoor use."),
    BOUNDARY_AMBIGUITY: ("One person is responsible for locking the ramp and "
                         "handles checking it before each use."),
}

def _attempt(c, sid, gap):
    c.post(f"/session/{sid}", data={"response": _ATTEMPT[gap],
                                    "answer_token": _token(c, sid),
                                    "action": "answered"})

def test_route_accepts_current_gap_and_persists_and_replays(client):
    c, appmod = client
    sid = _start(c)
    state = appmod.SESSION_STORE[sid]["state"]
    _answer_until(c, appmod, sid, MECHANISM_COMPLETENESS)
    gap = select_next_gap(state)
    assert gap == PHYSICAL_FEASIBILITY
    _attempt(c, sid, gap)   # W2-D: substantive attempt unlocks Accept Risk
    r = c.post(f"/session/{sid}/accept-risk", data={
        "gap_type": gap, "risk_confirm": "yes", "reason": "cannot test yet",
        "answer_token": _token(c, sid)})
    assert r.status_code == 302
    assert state.get_gap(PHYSICAL_FEASIBILITY).status == ACCEPTED_RISK
    # the cascade opened the next priority gap
    assert select_next_gap(state) == BOUNDARY_AMBIGUITY
    # durable record present
    from web.app import _get_store
    ledger = [r_ for r_ in state.assertions
              if r_.disposition == DISPOSITION_RISK_ACCEPTED]
    assert len(ledger) == 1 and ledger[0].content == "cannot test yet"
    # replay determinism: cold reconstruction preserves the acceptance
    from engine.session_reconstruction import reconstruct_readonly_state
    recon = reconstruct_readonly_state(_get_store(), sid)
    assert recon.review.level == 1
    rgap = recon.state.get_gap(PHYSICAL_FEASIBILITY)
    assert rgap is not None and rgap.status == ACCEPTED_RISK
    assert PHYSICAL_FEASIBILITY not in recon.review.open_gaps

def test_route_refuses_without_confirmation_or_token_or_wrong_gap(client):
    c, appmod = client
    sid = _start(c)
    state = appmod.SESSION_STORE[sid]["state"]
    _answer_until(c, appmod, sid, MECHANISM_COMPLETENESS)
    gap = select_next_gap(state)
    before = state.get_gap(gap).status
    # no confirmation
    c.post(f"/session/{sid}/accept-risk", data={
        "gap_type": gap, "answer_token": _token(c, sid)})
    assert state.get_gap(gap).status == before
    # bad token
    c.post(f"/session/{sid}/accept-risk", data={
        "gap_type": gap, "risk_confirm": "yes", "answer_token": "forged"})
    assert state.get_gap(gap).status == before
    # wrong (not currently served) gap
    c.post(f"/session/{sid}/accept-risk", data={
        "gap_type": BOUNDARY_AMBIGUITY, "risk_confirm": "yes",
        "answer_token": _token(c, sid)})
    assert state.get_gap(BOUNDARY_AMBIGUITY) is None
    # nothing durable was written by any refusal
    risk_records = [r_ for r_ in state.assertions
                    if r_.disposition == DISPOSITION_RISK_ACCEPTED]
    assert risk_records == []

def test_route_refuses_mechanism_gap(client):
    c, appmod = client
    sid = _start(c)
    state = appmod.SESSION_STORE[sid]["state"]
    assert select_next_gap(state) == MECHANISM_COMPLETENESS
    c.post(f"/session/{sid}/accept-risk", data={
        "gap_type": MECHANISM_COMPLETENESS, "risk_confirm": "yes",
        "answer_token": _token(c, sid)})
    assert state.get_gap(MECHANISM_COMPLETENESS).status in (OPEN, PARTIAL)

def test_disposition_completing_stage2_advances_maturity_and_replays(client):
    """When explicit dispositions satisfy the last stage-2 gap, the canonical
    continuation advances maturity/stage exactly as an answered iteration
    would - live and in replay, identically."""
    c, appmod = client
    sid = _start(c)
    state = appmod.SESSION_STORE[sid]["state"]
    _answer_until(c, appmod, sid, MECHANISM_COMPLETENESS)
    assert state.get_gap(MECHANISM_COMPLETENESS).status == CLOSED
    for gap in (PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY):
        assert select_next_gap(state) == gap
        _attempt(c, sid, gap)   # W2-D: substantive attempt unlocks Accept Risk
        c.post(f"/session/{sid}/accept-risk", data={
            "gap_type": gap, "risk_confirm": "yes",
            "answer_token": _token(c, sid)})
        assert state.get_gap(gap).status == ACCEPTED_RISK
    # the continuation ran: maturity advanced and Stage 3 opened
    assert state.maturity_level == 2
    assert state.current_stage == 3
    assert select_next_gap(state) is not None  # a stage-3 gap is being served
    # replay equivalence: the reconstructed state matches the live one
    from web.app import _get_store
    from engine.session_reconstruction import reconstruct_readonly_state
    recon = reconstruct_readonly_state(_get_store(), sid)
    assert recon.review.level == 1
    assert recon.state.maturity_level == state.maturity_level
    assert recon.state.current_stage == state.current_stage
    assert {g.gap_type: g.status for g in recon.state.gaps} ==            {g.gap_type: g.status for g in state.gaps}


def test_histories_without_risk_records_replay_identically(client):
    c, appmod = client
    sid = _start(c)
    _answer_until(c, appmod, sid, MECHANISM_COMPLETENESS, max_steps=2)
    from web.app import _get_store
    from engine.session_reconstruction import reconstruct_readonly_state
    r1 = reconstruct_readonly_state(_get_store(), sid)
    r2 = reconstruct_readonly_state(_get_store(), sid)
    assert r1.review.level == 1
    assert [g.gap_type + g.status for g in r1.state.gaps] == \
           [g.gap_type + g.status for g in r2.state.gaps]
    assert r1.state.maturity_level == r2.state.maturity_level
