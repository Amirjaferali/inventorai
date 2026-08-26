"""W2-B / RVR-6a (amended contract) — Option-C serving policy.

Authority: Contract Amendment 1 §4-§6 (authoritative via PR #575).
Capability 3 = state-aware next-question/next-action prioritization WITHIN
the canonical gap. These tests pin the behavioral floor:

  same canonical gap + different governed state/history
  → a materially DIFFERENT truthful served question/action
  (never a cue, label, tuple, or metadata change),

the exactly-four trigger vocabulary, the question-slot precedence PROPOSAL
resolving REAL competing serving consequences, fail-closed behavior (no
fabricated adaptation), determinism, and idle-re-render idempotence.
`select_next_gap` remains the sole canonical gap owner throughout.
"""
import copy
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from engine.idea_state import (
    IdeaState, Gap, Evidence,
    OPEN, PARTIAL, CLOSED, ACCEPTED_RISK,
    ASSERTED, REASONED, OWNER_STATED,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
    DISPOSITION_ANSWERED, DISPOSITION_RISK_ACCEPTED,
)
from engine.progression_loop import (
    select_next_gap, evaluate_transition, run_iteration, accept_gap_risk,
    advance_after_disposition, get_question, get_display_question,
    QUESTIONS, STALL_THRESHOLD, _STALL_REFRAME, _EXHAUSTED_EXIT_PROMPT,
    compute_serving_decision, ServingDecision,
    TRIGGER_CRITICAL_UNRESOLVED, TRIGGER_LAPSED_ACCEPTANCE,
    TRIGGER_MULTIPLE_ALTERNATIVES, TRIGGER_COMPLETED_INTENT_SKIP,
    W2B_QUESTION_SLOT_PRECEDENCE, W2B_TRIGGERS,
    _level1_blocking_gap,
)

MC_STRONG = ("(1) unfolding: the operator lifts the handle and the panel "
             "rotates on the hinge until flat. (2) locking: the toggle latch "
             "snaps over the center rib and holds the panel rigid. "
             "(3) folding: pressing the release lever frees the latch and the "
             "panel folds upward.")
PF_PLAIN = ("I have not tested whether the toggle latch stays reliable "
            "under repeated loading and outdoor use.")


def _state(domain="software", path="N"):
    s = IdeaState(idea_id="w2b-serve")
    s.domain = domain
    s.domain_signal = domain
    s.path = path
    return s


def _answered(state, content, gap, **kw):
    return state.record_interaction(action=DISPOSITION_ANSWERED,
                                    content=content, gap_context=gap, **kw)


def _display_baseline(state, gap_type):
    gap = state.get_gap(gap_type)
    k = gap.iterations_open if gap else 0
    return get_display_question(getattr(state, "domain", None), gap_type, k,
                                path=getattr(state, "path", None))


def _stalled_blocker_pf(k=3, with_attempt=False):
    """Level-1 state where PF blocks the transition and is stalled at k."""
    s = _state()
    s.maturity_level = 1
    s.known_mechanism = Evidence(content=MC_STRONG, quality=REASONED,
                                 iteration=1, provenance=OWNER_STATED)
    s.gaps.append(Gap(MECHANISM_COMPLETENESS, CLOSED, 0, closed_at=2))
    s.gaps.append(Gap(PHYSICAL_FEASIBILITY, OPEN, 3, iterations_open=k))
    if with_attempt:
        _answered(s, PF_PLAIN, PHYSICAL_FEASIBILITY)
    return s


def _lapsed_pf(k=4, re_engaged=False):
    """PF acceptance lapsed: active risk_accepted record while PF is
    OPEN again with a stale variant index k."""
    s = _stalled_blocker_pf(k=k, with_attempt=True)
    s.record_interaction(action=DISPOSITION_RISK_ACCEPTED,
                         content="cannot verify yet",
                         gap_context=PHYSICAL_FEASIBILITY)
    if re_engaged:
        _answered(s, PF_PLAIN, PHYSICAL_FEASIBILITY)  # post-lapse re-answer
    return s


# --- vocabulary --------------------------------------------------------------

def test_exactly_four_triggers_no_fifth():
    assert W2B_TRIGGERS == frozenset({
        TRIGGER_CRITICAL_UNRESOLVED, TRIGGER_LAPSED_ACCEPTANCE,
        TRIGGER_MULTIPLE_ALTERNATIVES, TRIGGER_COMPLETED_INTENT_SKIP})
    assert len(W2B_TRIGGERS) == 4
    assert "newly_comparable_decision_state" not in W2B_TRIGGERS
    assert set(W2B_QUESTION_SLOT_PRECEDENCE) <= W2B_TRIGGERS


def test_served_gap_always_canonical():
    for st in (_state(), _stalled_blocker_pf(), _lapsed_pf()):
        for elevated in (False, True):
            d = compute_serving_decision(st, register_elevated=elevated)
            assert d.served_gap == select_next_gap(st)


# --- no trigger: byte-preserving ---------------------------------------------

def test_no_trigger_no_override_no_action():
    s = _state()
    s.gaps.append(Gap(MECHANISM_COMPLETENESS, OPEN, 0))
    d = compute_serving_decision(s, register_elevated=False)
    assert d.triggers == ()
    assert d.question_override is None
    assert d.question_override_source is None
    assert d.primary_action is None


# --- trigger 1: critical unresolved (stalled blocker, generic surface) -------

def test_critical_serves_reframe_then_exit_instead_of_verbatim_repeat():
    s3 = _stalled_blocker_pf(k=3)
    baseline3 = _display_baseline(s3, PHYSICAL_FEASIBILITY)
    assert baseline3 == QUESTIONS[PHYSICAL_FEASIBILITY][-1]  # verbatim repeat
    d3 = compute_serving_decision(s3, register_elevated=False)
    assert TRIGGER_CRITICAL_UNRESOLVED in d3.triggers
    assert d3.question_override == _STALL_REFRAME            # REAL difference
    assert d3.question_override != baseline3
    s5 = _stalled_blocker_pf(k=5)
    d5 = compute_serving_decision(s5, register_elevated=False)
    assert d5.question_override == _EXHAUSTED_EXIT_PROMPT


def test_critical_no_fire_below_stall_threshold_or_off_blocker():
    fresh = _stalled_blocker_pf(k=STALL_THRESHOLD - 1)
    d = compute_serving_decision(fresh, register_elevated=False)
    assert TRIGGER_CRITICAL_UNRESOLVED not in d.triggers
    assert d.question_override is None
    # stalled but NOT the transition blocker (level 0): no fire
    s = _state()
    s.gaps.append(Gap(MECHANISM_COMPLETENESS, PARTIAL, 0, iterations_open=4))
    d0 = compute_serving_decision(s, register_elevated=False)
    assert TRIGGER_CRITICAL_UNRESOLVED not in d0.triggers


def test_critical_defers_to_governed_artifact_surface():
    """On the Path-N artifact surface RVR-2 already serves the reframe/exit;
    the policy fails closed to that governed behavior (no double-governing,
    no fire)."""
    s = _stalled_blocker_pf(k=4)
    s.domain = "mechanical"       # committed artifact domain
    s.domain_signal = "mechanical"
    d = compute_serving_decision(s, register_elevated=False)
    assert TRIGGER_CRITICAL_UNRESOLVED not in d.triggers
    assert d.question_override is None


def test_blocking_gap_truth_link():
    s = _stalled_blocker_pf()
    can, _ = evaluate_transition(s)
    assert can is False and _level1_blocking_gap(s) == PHYSICAL_FEASIBILITY
    s.get_gap(PHYSICAL_FEASIBILITY).status = ACCEPTED_RISK
    s.gaps.append(Gap(BOUNDARY_AMBIGUITY, CLOSED, 4, closed_at=5))
    can2, _ = evaluate_transition(s)
    assert can2 is True and _level1_blocking_gap(s) is None


# --- trigger 2: lapsed acceptance (re-ask the area's primary question) -------

def test_lapse_serves_primary_question_instead_of_stale_clamp():
    s = _lapsed_pf(k=4)
    baseline = _display_baseline(s, PHYSICAL_FEASIBILITY)
    d = compute_serving_decision(s, register_elevated=False)
    assert TRIGGER_LAPSED_ACCEPTANCE in d.triggers
    assert d.question_override == QUESTIONS[PHYSICAL_FEASIBILITY][0]
    assert d.question_override != baseline                   # REAL difference
    assert d.lapsed_served_gap is True


def test_lapse_no_override_after_re_engagement():
    """Once the inventor answers the reopened area again (active answered
    record newer than the lapsed acceptance), the re-ask override expires —
    it never loops the primary question. The capability-4 transparency duty
    (lapsed_served_gap) remains truthfully reported."""
    s = _lapsed_pf(k=4, re_engaged=True)
    d = compute_serving_decision(s, register_elevated=False)
    assert TRIGGER_LAPSED_ACCEPTANCE not in d.triggers
    assert d.lapsed_served_gap is True


def test_no_lapse_while_acceptance_holds_or_record_superseded():
    s = _lapsed_pf(k=4)
    s.get_gap(PHYSICAL_FEASIBILITY).status = ACCEPTED_RISK
    d = compute_serving_decision(s, register_elevated=False)
    assert TRIGGER_LAPSED_ACCEPTANCE not in d.triggers
    assert d.lapsed_served_gap is False
    s2 = _lapsed_pf(k=4)
    risk = [r for r in s2.assertions
            if r.disposition == DISPOSITION_RISK_ACCEPTED][0]
    _answered(s2, PF_PLAIN, PHYSICAL_FEASIBILITY,
              supersedes=[risk.record_id])
    d2 = compute_serving_decision(s2, register_elevated=False)
    assert TRIGGER_LAPSED_ACCEPTANCE not in d2.triggers


# --- trigger 4: completed-intent skip ----------------------------------------

def test_skip_requires_register_clamp_and_active_attempt():
    s = _stalled_blocker_pf(k=3, with_attempt=True)
    d = compute_serving_decision(s, register_elevated=True)
    assert TRIGGER_COMPLETED_INTENT_SKIP in d.triggers
    assert d.question_override == _EXHAUSTED_EXIT_PROMPT
    assert compute_serving_decision(
        s, register_elevated=False).triggers.count(
            TRIGGER_COMPLETED_INTENT_SKIP) == 0
    bare = _stalled_blocker_pf(k=3, with_attempt=False)
    d2 = compute_serving_decision(bare, register_elevated=True)
    assert TRIGGER_COMPLETED_INTENT_SKIP not in d2.triggers


def test_skip_superseded_attempt_does_not_count():
    s = _stalled_blocker_pf(k=3, with_attempt=True)
    attempt = s.assertions[-1]
    s.record_interaction(
        action=DISPOSITION_ANSWERED,
        content="That earlier statement was a mistake and I take it back.",
        gap_context=PHYSICAL_FEASIBILITY, supersedes=[attempt.record_id])
    d = compute_serving_decision(s, register_elevated=True)
    assert TRIGGER_COMPLETED_INTENT_SKIP not in d.triggers


# --- precedence: REAL competing serving consequences -------------------------

def test_precedence_resolves_competing_question_consequences():
    """At k == STALL_THRESHOLD with an active attempt and elevated register,
    trigger 1 wants the reframe while trigger 4 wants the exit prompt — a
    REAL competition over the served text. The frozen proposal resolves it
    deterministically (skip precedes critical: a substantive attempt exists,
    so re-engagement reframing would be redundant; the honest serving is
    the exit vocabulary)."""
    s = _stalled_blocker_pf(k=3, with_attempt=True)
    d = compute_serving_decision(s, register_elevated=True)
    assert {TRIGGER_CRITICAL_UNRESOLVED,
            TRIGGER_COMPLETED_INTENT_SKIP} <= set(d.triggers)
    assert d.question_override == _EXHAUSTED_EXIT_PROMPT      # skip wins
    assert d.question_override_source == TRIGGER_COMPLETED_INTENT_SKIP
    # without the attempt the competition disappears and critical serves
    s2 = _stalled_blocker_pf(k=3, with_attempt=False)
    d2 = compute_serving_decision(s2, register_elevated=True)
    assert d2.question_override == _STALL_REFRAME
    assert d2.question_override_source == TRIGGER_CRITICAL_UNRESOLVED


def test_precedence_lapse_wins_the_question_slot():
    """Lapsed + stalled-blocker + clamp + attempt + elevated: three
    candidate texts compete (primary re-ask vs exit vs reframe); the lapse
    re-ask wins — the correction invalidated the area's support, so the
    truthful restart is its primary question."""
    s = _lapsed_pf(k=3)
    d = compute_serving_decision(s, register_elevated=True)
    assert {TRIGGER_LAPSED_ACCEPTANCE, TRIGGER_COMPLETED_INTENT_SKIP,
            TRIGGER_CRITICAL_UNRESOLVED} <= set(d.triggers)
    assert d.question_override == QUESTIONS[PHYSICAL_FEASIBILITY][0]
    assert d.question_override_source == TRIGGER_LAPSED_ACCEPTANCE


def test_precedence_is_the_frozen_proposal():
    assert W2B_QUESTION_SLOT_PRECEDENCE == (
        TRIGGER_LAPSED_ACCEPTANCE,
        TRIGGER_COMPLETED_INTENT_SKIP,
        TRIGGER_CRITICAL_UNRESOLVED,
    )


def test_no_starvation_resolution_paths_stay_open():
    """The override never blocks resolution: the answered path, the six
    governed actions, and (with an active attempt) Accept-Risk remain the
    exits; a resolving event ends the trigger condition itself."""
    from engine.progression_loop import substantive_attempt_recorded
    s = _stalled_blocker_pf(k=3, with_attempt=True)
    assert substantive_attempt_recorded(s, PHYSICAL_FEASIBILITY) is True
    accept_gap_risk(s, PHYSICAL_FEASIBILITY)     # the exit works
    advance_after_disposition(s)
    d = compute_serving_decision(s, register_elevated=True)
    assert d.served_gap != PHYSICAL_FEASIBILITY  # journey moved on
    assert d.accepted_risk_gaps == (PHYSICAL_FEASIBILITY,)


# --- determinism / idempotence / purity --------------------------------------

def test_deterministic_and_idempotent_re_render():
    s = _lapsed_pf(k=3)
    first = compute_serving_decision(s, register_elevated=True)
    for _ in range(3):                       # idle re-renders: same ledger
        assert compute_serving_decision(s, register_elevated=True) == first
    sh = copy.deepcopy(s)
    rng = random.Random(9)
    for _ in range(5):
        rng.shuffle(sh.assertions)
        assert compute_serving_decision(sh, register_elevated=True) == first


def test_policy_is_read_only():
    s = _lapsed_pf(k=3)
    before = repr(s.__dict__)
    compute_serving_decision(s, register_elevated=True)
    compute_serving_decision(s, register_elevated=False)
    assert repr(s.__dict__) == before


def test_fail_closed_on_malformed_state():
    """A state the selectors cannot serve fails closed to no adaptation —
    never an exception, never a fabricated candidate."""
    s = _state(domain=None, path=None)
    s.gaps.append(Gap(PHYSICAL_FEASIBILITY, OPEN, 0, iterations_open=9))
    d = compute_serving_decision(s, register_elevated=True)
    assert isinstance(d, ServingDecision)
    assert d.primary_action is None
