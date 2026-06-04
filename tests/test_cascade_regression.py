"""
test_cascade_regression.py — Cascade Transition Regression Suite

Governance basis: CASCADE_TRANSITION_REGRESSION_TEST_PLAN.md
Defect addressed: result-overwrite bug fixed in d9835f5

Invariant under test:
    Gap closes
    → Cascade opens next gap
    → result["gap_targeted"] == newly opened gap type
    → result["question"] == correct question for that gap
    → iteration_log[-1].gap_targeted == newly opened gap type
    → iteration_log[-1].question_asked == correct question

Scope: structural verification only.
       No engine logic changes.
       No authorization changes.
       No maturity logic changes.
"""

import pytest
from engine.idea_state import (
    IdeaState, Evidence, Gap,
    PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY, MECHANISM_COMPLETENESS,
    PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS,
    OPEN, PARTIAL, CLOSED,
    ASSERTED, REASONED,
    PROGRESSING,
)
from engine.progression_loop import run_iteration

_CLOSING_Q_FRAGMENT = "NOT do or NOT cover"

_REASONED_RESPONSE = (
    "The sensor detects voltage drop across the shunt resistor. "
    "When the measured voltage falls below the threshold, the comparator "
    "triggers the relay which disconnects the load. "
    "This mechanism relies on Ohm's law and uses an LM393 comparator IC."
)


def _make_state_mech_closed() -> IdeaState:
    state = IdeaState(idea_id="cascade-test-mech-closed")
    state.maturity_level = 1
    state.current_stage = 2
    state.domain = "electronics_electrical"
    state.idea_summary = "IoT fault detection device"
    state.known_problem = Evidence(
        content="existing systems miss micro-faults",
        quality=REASONED,
        iteration=1,
    )
    state.known_mechanism = Evidence(
        content=_REASONED_RESPONSE,
        quality=REASONED,
        iteration=2,
    )
    mech_gap = Gap(
        gap_type=MECHANISM_COMPLETENESS,
        status=CLOSED,
        opened_at=1,
        closed_at=2,
    )
    state.gaps.append(mech_gap)
    state.iteration = 2
    return state


def _make_state_mech_and_pf_closed() -> IdeaState:
    state = _make_state_mech_closed()
    state.idea_id = "cascade-test-pf-closed"
    pf_gap = Gap(
        gap_type=PHYSICAL_FEASIBILITY,
        status=CLOSED,
        opened_at=3,
        closed_at=4,
    )
    state.gaps.append(pf_gap)
    state.iteration = 4
    return state


def _make_state_all_s2_closed() -> IdeaState:
    state = IdeaState(idea_id="cascade-test-s3-entry")
    state.maturity_level = 2
    state.current_stage = 3
    state.domain = "electronics_electrical"
    state.idea_summary = "IoT fault detection device"
    state.known_problem = Evidence(
        content="existing systems miss micro-faults",
        quality=REASONED,
        iteration=1,
    )
    state.known_mechanism = Evidence(
        content=_REASONED_RESPONSE,
        quality=REASONED,
        iteration=2,
    )
    for gap_type, closed_at in [
        (MECHANISM_COMPLETENESS, 2),
        (PHYSICAL_FEASIBILITY, 4),
        (BOUNDARY_AMBIGUITY, 6),
    ]:
        gap = Gap(
            gap_type=gap_type,
            status=CLOSED,
            opened_at=1,
            closed_at=closed_at,
        )
        state.gaps.append(gap)
    state.iteration = 6
    return state


def _make_state_s3_pmf_closed() -> IdeaState:
    state = _make_state_all_s2_closed()
    state.idea_id = "cascade-test-s3-pmf-closed"
    pmf_gap = Gap(
        gap_type=PROBLEM_MECHANISM_FIT,
        status=CLOSED,
        opened_at=7,
        closed_at=8,
    )
    state.gaps.append(pmf_gap)
    state.iteration = 8
    return state


def _assert_cascade_result(result: dict, expected_gap: str, state: IdeaState):
    assert result["gap_targeted"] == expected_gap, (
        f"Expected gap_targeted={expected_gap!r}, got {result['gap_targeted']!r}"
    )
    assert result["question"] is not None, (
        f"question is None for cascade to {expected_gap}"
    )
    assert len(result["question"]) > 10, (
        f"question too short for cascade to {expected_gap}: {result['question']!r}"
    )
    assert _CLOSING_Q_FRAGMENT not in result["question"], (
        f"Cascade question for {expected_gap} contains closing_q fragment. "
        f"Overwrite defect may have returned."
    )
    assert len(state.iteration_log) > 0, "iteration_log is empty"
    last_log = state.iteration_log[-1]
    assert last_log.gap_targeted == expected_gap, (
        f"iteration_log.gap_targeted={last_log.gap_targeted!r}, expected {expected_gap!r}"
    )
    assert last_log.question_asked == result["question"], (
        "iteration_log.question_asked does not match result['question']. Audit trail inaccurate."
    )


class TestCascadeTransitionRegression:

    def test_stage2_cascade_mech_to_pf(self):
        """TC-CASCADE-001: MECHANISM_COMPLETENESS closed → PHYSICAL_FEASIBILITY opens."""
        state = _make_state_mech_closed()
        result = run_iteration(state, _REASONED_RESPONSE)
        _assert_cascade_result(result, PHYSICAL_FEASIBILITY, state)

    def test_stage2_cascade_pf_to_boundary(self):
        """TC-CASCADE-002: PHYSICAL_FEASIBILITY closed → BOUNDARY_AMBIGUITY opens."""
        state = _make_state_mech_and_pf_closed()
        result = run_iteration(state, _REASONED_RESPONSE)
        _assert_cascade_result(result, BOUNDARY_AMBIGUITY, state)

    def test_non_cascade_path_remains_valid(self):
        """TC-CASCADE-003: Normal iteration with OPEN gap — no cascade — does not break."""
        state = IdeaState(idea_id="cascade-test-normal-iter")
        state.maturity_level = 1
        state.current_stage = 2
        state.domain = "electronics_electrical"
        state.known_problem = Evidence(
            content="existing systems miss micro-faults",
            quality=REASONED,
            iteration=1,
        )
        mech_gap = Gap(gap_type=MECHANISM_COMPLETENESS, status=OPEN, opened_at=1)
        state.gaps.append(mech_gap)
        state.iteration = 1
        result = run_iteration(state, _REASONED_RESPONSE)
        assert result is not None
        assert len(state.iteration_log) == 1

    def test_stage3_cascade_first_gap_opens(self):
        """TC-CASCADE-004 CRITICAL: All S2 closed, first Stage 3 gap opens correctly."""
        state = _make_state_all_s2_closed()
        result = run_iteration(state, _REASONED_RESPONSE)
        _assert_cascade_result(result, PROBLEM_MECHANISM_FIT, state)

    def test_stage3_cascade_second_gap_opens(self):
        """TC-CASCADE-005: PMF closed → ASSUMPTION_INVENTORY opens correctly."""
        state = _make_state_s3_pmf_closed()
        result = run_iteration(state, _REASONED_RESPONSE)
        _assert_cascade_result(result, ASSUMPTION_INVENTORY, state)

    def test_cascade_question_non_null_non_empty_non_closing(self):
        """TC-CASCADE-006: Question is valid at all Stage 2 cascade points."""
        cascade_states = [
            (_make_state_mech_closed(), PHYSICAL_FEASIBILITY),
            (_make_state_mech_and_pf_closed(), BOUNDARY_AMBIGUITY),
        ]
        for state, expected_gap in cascade_states:
            result = run_iteration(state, _REASONED_RESPONSE)
            assert result["question"] is not None, f"None at {expected_gap}"
            assert result["question"].strip() != "", f"Empty at {expected_gap}"
            assert _CLOSING_Q_FRAGMENT not in result["question"], (
                f"closing_q at {expected_gap} — overwrite defect returned"
            )

    def test_iteration_log_accuracy_across_stage2_cascades(self):
        """TC-CASCADE-007: Audit log accurate at both Stage 2 cascade points."""
        state_1 = _make_state_mech_closed()
        result_1 = run_iteration(state_1, _REASONED_RESPONSE)
        log_1 = state_1.iteration_log[-1]
        assert log_1.gap_targeted == PHYSICAL_FEASIBILITY
        assert log_1.question_asked == result_1["question"]
        assert _CLOSING_Q_FRAGMENT not in (log_1.question_asked or "")

        state_2 = _make_state_mech_and_pf_closed()
        result_2 = run_iteration(state_2, _REASONED_RESPONSE)
        log_2 = state_2.iteration_log[-1]
        assert log_2.gap_targeted == BOUNDARY_AMBIGUITY
        assert log_2.question_asked == result_2["question"]
        assert _CLOSING_Q_FRAGMENT not in (log_2.question_asked or "")


class TestStage3Reachability:
    """
    Regression suite for Stage 3 reachability fix (commit after 0da3d65).
    Proves current_stage advances to 3 naturally after maturity_level reaches 2,
    and that PROBLEM_MECHANISM_FIT opens without manual state manipulation.
    """

    _REASONED = (
        "The sensor detects voltage drop across the shunt resistor. "
        "When the measured voltage falls below the threshold, the comparator "
        "triggers the relay which disconnects the load. "
        "This mechanism relies on Ohm's law and uses an LM393 comparator IC."
    )

    def _make_state_s2_almost_complete(self):
        """maturity_level=1, MECH+PF closed, BA open — one step from Stage 3."""
        state = IdeaState(idea_id="reachability-regression")
        state.maturity_level = 1
        state.current_stage = 2
        state.domain = "electronics_electrical"
        state.known_problem = Evidence(
            content="motors fail without warning", quality=REASONED, iteration=1)
        state.known_mechanism = Evidence(
            content=self._REASONED, quality=REASONED, iteration=2)
        for gap_type, closed_at in [
            (MECHANISM_COMPLETENESS, 2),
            (PHYSICAL_FEASIBILITY, 4),
        ]:
            state.gaps.append(Gap(
                gap_type=gap_type, status=CLOSED,
                opened_at=1, closed_at=closed_at))
        state.gaps.append(Gap(
            gap_type=BOUNDARY_AMBIGUITY, status=OPEN, opened_at=4))
        state.iteration = 4
        return state

    def test_current_stage_advances_to_3_after_maturity_level_2(self):
        """
        TC-REACH-001
        After all Stage 2 gaps close and maturity_level reaches 2,
        current_stage must become 3 automatically.
        No manual state manipulation.
        """
        state = self._make_state_s2_almost_complete()
        run_iteration(state, self._REASONED)
        run_iteration(state, self._REASONED)

        assert state.maturity_level == 2, (
            f"maturity_level={state.maturity_level}, expected 2"
        )
        assert state.current_stage == 3, (
            "REGRESSION: current_stage did not advance to 3 after maturity_level=2. "
            "Stage 3 is unreachable. Fix: set state.current_stage=3 when maturity_level reaches 2."
        )

    def test_stage3_gap_opens_naturally_after_stage2_complete(self):
        """
        TC-REACH-002
        After Stage 2 complete, the next run_iteration must open
        PROBLEM_MECHANISM_FIT without any manual intervention.
        """
        state = self._make_state_s2_almost_complete()
        run_iteration(state, self._REASONED)
        run_iteration(state, self._REASONED)

        # One more iteration triggers cascade
        result = run_iteration(state, self._REASONED)

        pmf_gaps = [g for g in state.gaps if g.gap_type == PROBLEM_MECHANISM_FIT]
        assert len(pmf_gaps) > 0, (
            "REGRESSION: PROBLEM_MECHANISM_FIT never opened after Stage 2 complete."
        )
        assert pmf_gaps[0].status == OPEN, (
            f"REGRESSION: PMF gap status={pmf_gaps[0].status}, expected OPEN"
        )
        assert result.get("gap_targeted") == PROBLEM_MECHANISM_FIT, (
            f"REGRESSION: gap_targeted={result.get('gap_targeted')}, "
            "expected PROBLEM_MECHANISM_FIT"
        )

    def test_stage3_question_delivered_not_closing_q(self):
        """
        TC-REACH-003
        When Stage 3 first opens, the question delivered must not be
        the Stage 2 closing prompt.
        """
        state = self._make_state_s2_almost_complete()
        run_iteration(state, self._REASONED)
        run_iteration(state, self._REASONED)
        result = run_iteration(state, self._REASONED)

        question = result.get("question")
        assert question is not None, "REGRESSION: no question delivered at Stage 3 opening"
        assert "NOT do or NOT cover" not in (question or ""), (
            "REGRESSION: closing_q delivered instead of Stage 3 question"
        )
