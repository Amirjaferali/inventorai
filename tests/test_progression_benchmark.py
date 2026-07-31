"""
Progression Benchmark Suite — Step 4
Tests only. No engine changes. No fixes.

Covers:
    A. assess_response quality classification   (8 cases)
    B. integrate_response gap status behavior   (12 cases)
    C. evaluate_transition transition gates     (11 cases)

Total: 31 cases
"""

from engine.idea_state import IdeaState, Evidence, Gap
from engine.progression_loop import (
    assess_response,
    integrate_response,
    evaluate_transition,
    ASSERTED, REASONED, DEMONSTRATED,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
)

OPEN = "OPEN"
PARTIAL = "PARTIAL"
CLOSED = "CLOSED"


def make_state(domain="electronics"):
    state = IdeaState(idea_id="test-001")
    state.domain = domain
    state.iteration = 1
    return state

def make_gap(gap_type, status=OPEN, iterations_open=1):
    gap = Gap(gap_type=gap_type, status=status, opened_at=1)
    gap.iterations_open = iterations_open
    return gap

def make_evidence(quality, content="test evidence"):
    return Evidence(content=content, quality=quality, iteration=1)


# ═══════════════════════════════════════════════
# SECTION A: assess_response (8 cases)
# ═══════════════════════════════════════════════

class TestAssessResponseQuality:

    def test_A1_empty_response_is_asserted(self):
        assert assess_response("") == ASSERTED

    def test_A2_vague_filler_is_asserted(self):
        assert assess_response("somehow something") == ASSERTED

    def test_A3_rich_reasoning_is_reasoned(self):
        result = assess_response(
            "A Hall sensor measures magnetic flux density by detecting voltage "
            "perpendicular to current flow, enabling non-contact position sensing."
        )
        assert result == REASONED

    def test_A4_demonstrated_not_producible(self):
        result = assess_response(
            "Lab test confirmed: sensor accuracy 0.1mm at 1000Hz sampling rate."
        )
        assert result != DEMONSTRATED

    def test_A5_single_token_sensor_should_be_asserted(self):
        assert assess_response("sensor") == ASSERTED

    def test_A6_short_phrase_should_be_asserted(self):
        assert assess_response("it processes data") == ASSERTED

    def test_A7_vague_plus_token_should_be_asserted(self):
        assert assess_response("it detects things somehow") == ASSERTED

    def test_A8_substring_match_should_be_asserted(self):
        assert assess_response("barrier protection") == ASSERTED


# ═══════════════════════════════════════════════
# SECTION B: integrate_response (12 cases)
# ═══════════════════════════════════════════════

class TestIntegrateResponseGapStatus:

    def test_B1_asserted_response_returns_warn(self):
        state = make_state()
        state.gaps.append(make_gap(MECHANISM_COMPLETENESS, OPEN))
        transition, reason = integrate_response(
            state, MECHANISM_COMPLETENESS, "question", "sensor"
        )
        assert transition == "WARN"

    def test_B2_asserted_response_gap_becomes_partial(self):
        state = make_state()
        state.gaps.append(make_gap(MECHANISM_COMPLETENESS, OPEN))
        integrate_response(state, MECHANISM_COMPLETENESS, "question", "sensor")
        gap = state.get_gap(MECHANISM_COMPLETENESS)
        assert gap.status == PARTIAL

    def test_B3_reasoned_on_open_gap_returns_warn(self):
        state = make_state()
        state.gaps.append(make_gap(MECHANISM_COMPLETENESS, OPEN))
        transition, reason = integrate_response(
            state, MECHANISM_COMPLETENESS, "question",
            "The Hall sensor detects magnetic flux by measuring perpendicular voltage "
            "to current, enabling non-contact rotation sensing."
        )
        assert transition == "WARN"

    def test_B4_reasoned_on_partial_gap_closes_it(self):
        state = make_state()
        state.gaps.append(make_gap(MECHANISM_COMPLETENESS, PARTIAL))
        transition, reason = integrate_response(
            state, MECHANISM_COMPLETENESS, "question",
            "The Hall sensor detects magnetic flux by measuring perpendicular voltage "
            "to current, enabling non-contact rotation sensing."
        )
        assert transition == "PASS"
        gap = state.get_gap(MECHANISM_COMPLETENESS)
        assert gap.status == CLOSED

    def test_B5_gap_created_if_not_exists(self):
        state = make_state()
        assert state.get_gap(MECHANISM_COMPLETENESS) is None
        integrate_response(state, MECHANISM_COMPLETENESS, "question", "sensor")
        assert state.get_gap(MECHANISM_COMPLETENESS) is not None

    def test_B6_known_mechanism_updated_on_reasoned(self):
        state = make_state()
        state.gaps.append(make_gap(MECHANISM_COMPLETENESS, OPEN))
        assert state.known_mechanism is None
        integrate_response(
            state, MECHANISM_COMPLETENESS, "question",
            "The Hall sensor detects magnetic flux by measuring perpendicular voltage "
            "to current, enabling non-contact rotation sensing."
        )
        assert state.known_mechanism is not None

    def test_B7_asserted_response_does_not_set_known_problem(self):
        """After RISK-002 fix: ASSERTED evidence must NOT set known_problem."""
        state = make_state()
        state.gaps.append(make_gap(MECHANISM_COMPLETENESS, OPEN))
        assert state.known_problem is None
        integrate_response(state, MECHANISM_COMPLETENESS, "question", "sensor")
        assert state.known_problem is None  # RISK-002 fix: ASSERTED blocked

    def test_B8_known_problem_should_require_reasoned_floor(self):
        state = make_state()
        state.gaps.append(make_gap(MECHANISM_COMPLETENESS, OPEN))
        integrate_response(state, MECHANISM_COMPLETENESS, "question", "sensor")
        assert state.known_problem is None

    def test_B9_asserted_on_partial_gap_stays_partial(self):
        state = make_state()
        state.gaps.append(make_gap(MECHANISM_COMPLETENESS, PARTIAL))
        integrate_response(state, MECHANISM_COMPLETENESS, "question", "sensor")
        gap = state.get_gap(MECHANISM_COMPLETENESS)
        assert gap.status == PARTIAL

    def test_B10_integrate_response_returns_tuple(self):
        state = make_state()
        state.gaps.append(make_gap(MECHANISM_COMPLETENESS, OPEN))
        result = integrate_response(state, MECHANISM_COMPLETENESS, "question", "sensor")
        assert isinstance(result, tuple) and len(result) == 2
        assert isinstance(result[0], str) and isinstance(result[1], str)

    def test_B11_warn_does_not_close_gap(self):
        state = make_state()
        state.gaps.append(make_gap(MECHANISM_COMPLETENESS, OPEN))
        integrate_response(state, MECHANISM_COMPLETENESS, "question", "sensor")
        gap = state.get_gap(MECHANISM_COMPLETENESS)
        assert gap.status != CLOSED

    def test_B12_two_reasoned_calls_close_gap(self):
        state = make_state()
        state.gaps.append(make_gap(MECHANISM_COMPLETENESS, OPEN))
        r = ("The Hall sensor detects magnetic flux by measuring perpendicular voltage "
             "to current, enabling non-contact rotation sensing.")
        integrate_response(state, MECHANISM_COMPLETENESS, "q", r)
        integrate_response(state, MECHANISM_COMPLETENESS, "q", r)
        gap = state.get_gap(MECHANISM_COMPLETENESS)
        assert gap.status == CLOSED


# ═══════════════════════════════════════════════
# SECTION C: evaluate_transition (11 cases)
# ═══════════════════════════════════════════════

class TestEvaluateTransition:

    def test_C1_level0_no_known_problem_blocks(self):
        state = make_state()
        state.maturity_level = 0
        can, reason = evaluate_transition(state)
        assert can is False

    def test_C2_level0_asserted_problem_blocks(self):
        state = make_state()
        state.maturity_level = 0
        state.known_problem = make_evidence(ASSERTED)
        can, reason = evaluate_transition(state)
        assert can is False

    def test_C3_level0_reasoned_problem_no_mech_gap_allows(self):
        state = make_state()
        state.maturity_level = 0
        state.known_problem = make_evidence(REASONED)
        can, reason = evaluate_transition(state)
        assert can is True

    def test_C4_level0_mech_gap_open_zero_iterations_blocks(self):
        state = make_state()
        state.maturity_level = 0
        state.known_problem = make_evidence(REASONED)
        gap = make_gap(MECHANISM_COMPLETENESS, OPEN, iterations_open=0)
        state.gaps.append(gap)
        can, reason = evaluate_transition(state)
        assert can is False

    def test_C5_level1_no_known_mechanism_blocks(self):
        state = make_state()
        state.maturity_level = 1
        can, reason = evaluate_transition(state)
        assert can is False

    def test_C6_level1_asserted_mechanism_blocks(self):
        state = make_state()
        state.maturity_level = 1
        state.known_mechanism = make_evidence(ASSERTED)
        can, reason = evaluate_transition(state)
        assert can is False

    def test_C7_level1_all_stage_two_gaps_closed_allows(self):
        # GD-001: all three Stage Two gaps must be CLOSED for Level 1->2
        state = make_state()
        state.maturity_level = 1
        state.known_mechanism = make_evidence(REASONED)
        state.gaps.append(make_gap(MECHANISM_COMPLETENESS, CLOSED))
        state.gaps.append(make_gap(PHYSICAL_FEASIBILITY, CLOSED))
        state.gaps.append(make_gap(BOUNDARY_AMBIGUITY, CLOSED))
        can, reason = evaluate_transition(state)
        assert can is True

    def test_C8_level1_reasoned_mechanism_open_gap_blocks(self):
        state = make_state()
        state.maturity_level = 1
        state.known_mechanism = make_evidence(REASONED)
        gap = make_gap(MECHANISM_COMPLETENESS, OPEN)
        state.gaps.append(gap)
        can, reason = evaluate_transition(state)
        assert can is False

    def test_C9_level2_is_max_for_mvp(self):
        state = make_state()
        state.maturity_level = 2
        can, reason = evaluate_transition(state)
        assert can is False
        assert "max" in reason.lower() or "MVP" in reason

    def test_C10_returns_correct_types(self):
        state = make_state()
        state.maturity_level = 0
        result = evaluate_transition(state)
        assert isinstance(result, tuple) and len(result) == 2
        assert isinstance(result[0], bool) and isinstance(result[1], str)

    def test_C11_asserted_problem_blocks_level0_regression(self):
        """Regression: ASSERTED known_problem must never allow level 0 transition."""
        state = make_state()
        state.maturity_level = 0
        state.known_problem = make_evidence(ASSERTED)
        can, _ = evaluate_transition(state)
        assert can is False

# SECTION D: ILT-001S closure
class TestUpdateDirection:
    def test_D1_partial_gap_at_threshold_triggers_stalled(self):
        from engine.progression_loop import STALL_THRESHOLD
        from engine.idea_state import STALLED
        """ILT-001S: PARTIAL gap at STALL_THRESHOLD causes STALLED direction."""
        from engine.progression_loop import update_direction
        state = make_state()
        state.maturity_level = 1
        gap = make_gap(MECHANISM_COMPLETENESS, PARTIAL, iterations_open=STALL_THRESHOLD)
        state.gaps.append(gap)
        update_direction(state, state.maturity_level)
        assert state.direction == STALLED

# SECTION E: R-007 closure
class TestIdeaSummaryInDeliverable:
    def test_E1_idea_summary_included_in_fdc001_package(self):
        """R-007: assemble_deliverable includes idea_summary in _session_meta."""
        from engine.deliverable_assembler import assemble_deliverable
        state = make_state()
        state.idea_summary = "Capacitive soil moisture sensor using ESP32 discharge timing"
        state.maturity_level = 2
        state.known_problem  = make_evidence(REASONED, "inventor stated problem")
        state.known_mechanism = make_evidence(REASONED, "capacitive discharge mechanism")
        pkg = assemble_deliverable(state)
        meta = pkg.get("_session_meta", {})
        assert meta.get("idea_summary") == "Capacitive soil moisture sensor using ESP32 discharge timing"
