"""
Increment 1A — structured owner actions (conformance correction).

Proves the structured-action contract WITHOUT changing gate, scoring, maturity,
closure, deliverable, transcript, IdeaState, or persistence semantics:

  * ONLY `answered` enters the existing assessment path (run_iteration).
  * The five non-answer actions (unknown / deferred / provisional_assumption /
    specialist_requested / evidence_requested) never assess, score, close or
    alter a gap, advance maturity, satisfy a gate, or create an evidence record.
    They are recorded ONLY as additive in-memory metadata on the session entry.
  * The ILT-002 transcript record shape is unchanged for `answered` and no
    answered transcript record is written for non-answer actions.

Tests inspect observable state (iteration, gap statuses, maturity, transcript,
entry metadata, HTTP behavior), not private implementation details.

Legacy-compatibility rule under test: a POST with NO `action` field is treated
as `answered` (identical to pre-1A behavior). An explicit but unrecognized
action is rejected with HTTP 400 and changes nothing.
"""
import copy
import uuid

import pytest

from web.app import app, SESSION_STORE, INTERACTION_ACTIONS
from engine.idea_state import IdeaState, OPEN, PARTIAL, CLOSED
from engine.progression_loop import run_iteration


def _new_session():
    """Seed a realistic in-memory session with at least one open gap, mirroring
    the existing test pattern (direct SESSION_STORE construction)."""
    state = IdeaState(idea_id="i1a-" + uuid.uuid4().hex[:8])
    # The web /start route sets state.domain via infer_domain before iterating;
    # replicate that here so run_iteration() seeds gaps exactly as in normal use.
    state.domain = "electronics_electrical"
    # Realistic seeding: one iteration so gaps/known_problem exist as in normal use.
    run_iteration(state, "A bicycle brake light that turns on when the rider "
                         "decelerates, using a sensor to detect slowing down.")
    sid = "i1a-" + uuid.uuid4().hex
    SESSION_STORE[sid] = {
        "state": state,
        "last_result": None,
        "transcript": [],
        "last_question": "What is the core mechanism?",
    }
    return sid


def _snapshot(state):
    """Observable epistemic snapshot for before/after comparison."""
    return {
        "iteration": state.iteration,
        "maturity_level": state.maturity_level,
        "gaps": [(g.gap_type, g.status) for g in state.gaps],
        "n_acknowledged": len(getattr(state, "acknowledged_unknowns", [])),
    }


def _teardown(sid):
    SESSION_STORE.pop(sid, None)


NON_ANSWER = ["unknown", "deferred", "provisional_assumption",
              "specialist_requested", "evidence_requested"]


# 1. ANSWERED invokes the existing assessment path.
def test_answered_invokes_assessment_path():
    sid = _new_session()
    try:
        entry = SESSION_STORE[sid]
        before = _snapshot(entry["state"])
        before_transcript = len(entry["transcript"])
        client = app.test_client()
        r = client.post(f"/session/{sid}",
                        data={"action": "answered",
                              "response": "The accelerometer measures deceleration and "
                                          "triggers the light when it crosses a threshold."},
                        follow_redirects=False)
        assert r.status_code in (301, 302)
        after = _snapshot(entry["state"])
        # Assessment path ran: iteration advanced and a transcript record was added.
        assert after["iteration"] == before["iteration"] + 1
        assert len(entry["transcript"]) == before_transcript + 1
        # No interaction metadata is created for answered.
        assert "interaction_actions" not in entry
    finally:
        _teardown(sid)


# 2. Legacy submission without an explicit action is treated as ANSWERED.
def test_legacy_submission_without_action_is_answered():
    sid = _new_session()
    try:
        entry = SESSION_STORE[sid]
        before_iter = entry["state"].iteration
        before_transcript = len(entry["transcript"])
        client = app.test_client()
        r = client.post(f"/session/{sid}",
                        data={"response": "The sensor detects deceleration by measuring "
                                          "the rate of change of speed over time."},
                        follow_redirects=False)
        assert r.status_code in (301, 302)
        # Identical to pre-1A answered behavior.
        assert entry["state"].iteration == before_iter + 1
        assert len(entry["transcript"]) == before_transcript + 1
        assert "interaction_actions" not in entry
    finally:
        _teardown(sid)


# (compat) An explicit but unrecognized action is rejected and changes nothing.
def test_unrecognized_action_rejected_400_no_change():
    sid = _new_session()
    try:
        entry = SESSION_STORE[sid]
        before = _snapshot(entry["state"])
        before_transcript = len(entry["transcript"])
        client = app.test_client()
        r = client.post(f"/session/{sid}",
                        data={"action": "totally_unknown_action", "response": "x"},
                        follow_redirects=False)
        assert r.status_code == 400
        assert _snapshot(entry["state"]) == before
        assert len(entry["transcript"]) == before_transcript
        assert "interaction_actions" not in entry
    finally:
        _teardown(sid)


# 3-7 + 8 + 10: every non-answer action — no assessment/score/closure/maturity/
# gate/evidence; recorded only in entry metadata; no answered transcript record.
@pytest.mark.parametrize("action", NON_ANSWER)
def test_non_answer_action_does_not_advance_or_assess(action):
    sid = _new_session()
    try:
        entry = SESSION_STORE[sid]
        before = _snapshot(entry["state"])
        before_transcript = len(entry["transcript"])
        client = app.test_client()
        r = client.post(f"/session/{sid}",
                        data={"action": action,
                              "response": "some optional note text that is long enough "
                                          "to be assessed as reasoned if it were assessed"},
                        follow_redirects=False)
        assert r.status_code in (301, 302)
        after = _snapshot(entry["state"])
        # No epistemic movement whatsoever.
        assert after["iteration"] == before["iteration"], action
        assert after["maturity_level"] == before["maturity_level"], action
        assert after["gaps"] == before["gaps"], action          # no gap opened/closed/altered
        assert after["n_acknowledged"] == before["n_acknowledged"], action
        # No answered transcript record was written.
        assert len(entry["transcript"]) == before_transcript, action
        # Recorded only as additive in-memory metadata.
        actions = entry.get("interaction_actions")
        assert actions and actions[-1]["action"] == action, action
    finally:
        _teardown(sid)


# 5 (focus): PROVISIONAL_ASSUMPTION text is retained as metadata, not validated.
def test_provisional_assumption_text_is_metadata_not_validated():
    sid = _new_session()
    try:
        entry = SESSION_STORE[sid]
        before = _snapshot(entry["state"])
        note = "Assume a 3.7V battery is acceptable for now."
        client = app.test_client()
        client.post(f"/session/{sid}",
                    data={"action": "provisional_assumption", "response": note},
                    follow_redirects=False)
        # Text retained verbatim as metadata.
        rec = entry["interaction_actions"][-1]
        assert rec["action"] == "provisional_assumption"
        assert rec["text"] == note
        # Did not become validated knowledge / did not satisfy a gate.
        assert _snapshot(entry["state"]) == before
        # Not recorded as an answered transcript record.
        assert entry["transcript"] == []
    finally:
        _teardown(sid)


# 6/7 (focus): specialist/evidence requests create no technical assertion/evidence.
def test_specialist_and_evidence_requests_create_no_assertion():
    for action in ("specialist_requested", "evidence_requested"):
        sid = _new_session()
        try:
            entry = SESSION_STORE[sid]
            before = _snapshot(entry["state"])
            client = app.test_client()
            client.post(f"/session/{sid}", data={"action": action},
                        follow_redirects=False)
            # No gap evidence created, no known_* asserted, no progression.
            assert _snapshot(entry["state"]) == before, action
            assert all(len(getattr(g, "evidence", [])) == 0 for g in entry["state"].gaps), action
            assert entry["transcript"] == [], action
        finally:
            _teardown(sid)


# 4 (explicit) DEFERRED does not invoke assessment or closure (covered by the
# parametrized test; kept explicit for the required enumeration).
def test_deferred_no_assessment_no_closure():
    sid = _new_session()
    try:
        entry = SESSION_STORE[sid]
        before = _snapshot(entry["state"])
        client = app.test_client()
        client.post(f"/session/{sid}", data={"action": "deferred", "response": ""},
                    follow_redirects=False)
        # No assessment and no closure: full epistemic snapshot is unchanged,
        # so no gap moved to CLOSED and no maturity/iteration advanced.
        assert _snapshot(entry["state"]) == before
    finally:
        _teardown(sid)


# Stronger behavioral guard: for a non-answer action, the assessment entry point
# run_iteration must NOT be invoked. Patch the symbol web.app uses and assert it
# is never called.
@pytest.mark.parametrize("action", NON_ANSWER)
def test_non_answer_action_never_calls_run_iteration(action, monkeypatch):
    sid = _new_session()
    try:
        called = {"n": 0}
        import web.app as webapp

        def _boom(*a, **k):
            called["n"] += 1
            raise AssertionError("run_iteration must not be called for " + action)

        monkeypatch.setattr(webapp, "run_iteration", _boom)
        client = app.test_client()
        r = client.post(f"/session/{sid}", data={"action": action, "response": "note"},
                        follow_redirects=False)
        assert r.status_code in (301, 302)
        assert called["n"] == 0
    finally:
        _teardown(sid)


# 9. The transcript record SHAPE is unchanged for ANSWERED.
def test_answered_transcript_record_shape_unchanged():
    sid = _new_session()
    try:
        entry = SESSION_STORE[sid]
        client = app.test_client()
        client.post(f"/session/{sid}",
                    data={"action": "answered", "response": "The Hall-effect sensor "
                          "detects wheel slowing and the controller switches the light."},
                    follow_redirects=False)
        assert len(entry["transcript"]) == 1
        rec = entry["transcript"][0]
        assert set(rec.keys()) == {
            "session_id", "iteration", "question", "response", "domain", "timestamp"
        }
        assert rec["session_id"] == sid
    finally:
        _teardown(sid)


# 8 (explicit) Non-answer metadata structure is additive and absent by default.
def test_interaction_metadata_is_additive_and_default_absent():
    sid = _new_session()
    try:
        entry = SESSION_STORE[sid]
        # Default-on-read: legacy entries have no interaction_actions key.
        assert "interaction_actions" not in entry
        client = app.test_client()
        client.post(f"/session/{sid}", data={"action": "unknown"}, follow_redirects=False)
        assert isinstance(entry["interaction_actions"], list)
        assert entry["interaction_actions"][-1]["action"] == "unknown"
        # IdeaState carries no Increment 1A field.
        assert not hasattr(entry["state"], "interaction_actions")
    finally:
        _teardown(sid)


# Contract sanity: the action allowlist is exactly the six structured actions.
def test_action_allowlist_is_exactly_six():
    assert INTERACTION_ACTIONS == {
        "answered", "unknown", "deferred", "provisional_assumption",
        "specialist_requested", "evidence_requested",
    }
