"""
test_stage3_evaluator.py — Stage 3 Evaluator Test Suite

Governance basis: STAGE3_EVALUATOR_TEST_STRATEGY.md
HEAD at authoring: 304c3ad

Scope:
    Tests engine/stage3_evaluator.py behavior only.
    No engine integration.
    No run_iteration() changes.
    No IdeaState modification by evaluator — TS-ACT4-003 is mandatory.
"""

import pytest
from engine.stage3_evaluator import (
    evaluate_stage3_response,
    check_cross_gap_integration,
    Stage3EvaluationResult,
    EvidenceObservation,
    CapabilityObservation,
    ResolutionObservation,
    PMF_E1, PMF_E2, PMF_E3,
    AI_E1, AI_E2, AI_E3,
    EGA_E1, EGA_E2, EGA_E3,
)
from engine.idea_state import (
    IdeaState, Evidence, Gap,
    PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
    OPEN, CLOSED,
    ASSERTED, REASONED,
)

_PMF_STRONG = (
    "My invention addresses the problem of undetected micro-faults in industrial motors. "
    "The motor vibration sensor detects micro-faults because it measures harmonic distortion "
    "in the vibration frequency spectrum. Without this mechanism, faults go undetected until "
    "catastrophic failure. However, this mechanism does not address thermal faults — "
    "that is a limitation of the approach."
)
_AI_STRONG = (
    "I assume the vibration baseline profile is stable across operating temperatures. "
    "This assumption is unvalidated and load-bearing — if wrong, the mechanism would "
    "produce false positives constantly. I also assume the sensor can be mounted without "
    "affecting motor balance, but if wrong I would just need to adjust the mounting bracket. "
    "The first assumption is essential; the second is peripheral."
)
_EGA_STRONG = (
    "The implementation demands expertise in signal processing, specifically FFT analysis "
    "of vibration data, and in embedded firmware for real-time processing. "
    "I lack sufficient knowledge of FFT implementation at the firmware level — "
    "I would need to bring in a DSP engineer. Without that expertise, "
    "the sampling rate configuration would be wrong and the fault detection would fail."
)
_EMPTY_RESPONSE = ""
_ASSERTED_RESPONSE = "I don't know"


def _make_clean_state() -> IdeaState:
    state = IdeaState(idea_id="evaluator-test-state")
    state.maturity_level = 2
    state.current_stage = 3
    state.known_problem = Evidence(content="motors fail without warning", quality=REASONED, iteration=1)
    for gap_type in [MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY]:
        state.gaps.append(Gap(gap_type=gap_type, status=CLOSED, opened_at=1, closed_at=3))
    state.iteration = 6
    return state


class TestAct1Detection:

    def test_pmf_signals_detected(self):
        """TS-ACT1-001"""
        result = evaluate_stage3_response(PROBLEM_MECHANISM_FIT, _PMF_STRONG, REASONED)
        assert len(result.act1_signals) >= 1
        assert any(s in result.act1_signals for s in ["addresses", "because", "does not"])

    def test_ai_signals_detected(self):
        """TS-ACT1-002"""
        result = evaluate_stage3_response(ASSUMPTION_INVENTORY, _AI_STRONG, REASONED)
        assert len(result.act1_signals) >= 1
        assert any(s in result.act1_signals for s in ["assume", "unvalidated", "if"])

    def test_ega_signals_detected(self):
        """TS-ACT1-003"""
        result = evaluate_stage3_response(EXPERTISE_GAP_AWARENESS, _EGA_STRONG, REASONED)
        assert len(result.act1_signals) >= 1
        assert any(s in result.act1_signals for s in ["lack", "need to", "would need"])

    def test_no_signals_in_weak_response(self):
        """TS-ACT1-004"""
        result = evaluate_stage3_response(PROBLEM_MECHANISM_FIT, _ASSERTED_RESPONSE, ASSERTED)
        assert result.act1_signals == []

    def test_non_stage3_gap_returns_empty_immediately(self):
        """TS-ACT1-005"""
        result = evaluate_stage3_response(MECHANISM_COMPLETENESS, _PMF_STRONG, REASONED)
        assert result.is_stage3_gap == False
        assert result.act1_signals == []
        assert result.act2_evidence is None
        assert result.act3_capability is None
        assert result.act4_resolution is None


class TestAct2EvidenceConfirmation:

    def test_pmf_e1_confirmed(self):
        """TS-ACT2-PMF-001"""
        result = evaluate_stage3_response(PROBLEM_MECHANISM_FIT, _PMF_STRONG, REASONED)
        assert PMF_E1 in result.act2_evidence.confirmed_items

    def test_pmf_e1_missing_short_response(self):
        """TS-ACT2-PMF-002"""
        result = evaluate_stage3_response(PROBLEM_MECHANISM_FIT, "it addresses the problem", REASONED)
        assert PMF_E1 in result.act2_evidence.missing_items

    def test_pmf_e2_confirmed(self):
        """TS-ACT2-PMF-003"""
        result = evaluate_stage3_response(PROBLEM_MECHANISM_FIT, _PMF_STRONG, REASONED)
        assert PMF_E2 in result.act2_evidence.confirmed_items

    def test_pmf_e3_confirmed(self):
        """TS-ACT2-PMF-004"""
        result = evaluate_stage3_response(PROBLEM_MECHANISM_FIT, _PMF_STRONG, REASONED)
        assert PMF_E3 in result.act2_evidence.confirmed_items

    def test_ai_e1_confirmed(self):
        """TS-ACT2-AI-001"""
        result = evaluate_stage3_response(ASSUMPTION_INVENTORY, _AI_STRONG, REASONED)
        assert AI_E1 in result.act2_evidence.confirmed_items

    def test_ai_e2_confirmed(self):
        """TS-ACT2-AI-002"""
        result = evaluate_stage3_response(ASSUMPTION_INVENTORY, _AI_STRONG, REASONED)
        assert AI_E2 in result.act2_evidence.confirmed_items

    def test_ai_e3_confirmed(self):
        """TS-ACT2-AI-003"""
        result = evaluate_stage3_response(ASSUMPTION_INVENTORY, _AI_STRONG, REASONED)
        assert AI_E3 in result.act2_evidence.confirmed_items

    def test_ega_e1_confirmed(self):
        """TS-ACT2-EGA-001"""
        result = evaluate_stage3_response(EXPERTISE_GAP_AWARENESS, _EGA_STRONG, REASONED)
        assert EGA_E1 in result.act2_evidence.confirmed_items

    def test_ega_e2_confirmed(self):
        """TS-ACT2-EGA-002"""
        result = evaluate_stage3_response(EXPERTISE_GAP_AWARENESS, _EGA_STRONG, REASONED)
        assert EGA_E2 in result.act2_evidence.confirmed_items

    def test_ega_e3_confirmed(self):
        """TS-ACT2-EGA-003"""
        result = evaluate_stage3_response(EXPERTISE_GAP_AWARENESS, _EGA_STRONG, REASONED)
        assert EGA_E3 in result.act2_evidence.confirmed_items

    def test_all_items_missing_empty_response(self):
        """TS-ACT2-EMPTY-001"""
        for gap_type in [PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS]:
            result = evaluate_stage3_response(gap_type, _EMPTY_RESPONSE, ASSERTED)
            assert len(result.act2_evidence.confirmed_items) == 0
            assert len(result.act2_evidence.missing_items) == 3


class TestAct3CapabilityAssessment:

    def test_capability_present_two_items_reasoned(self):
        """TS-ACT3-001"""
        result = evaluate_stage3_response(PROBLEM_MECHANISM_FIT, _PMF_STRONG, REASONED)
        if len(result.act2_evidence.confirmed_items) >= 2:
            assert result.act3_capability.capability_present == True

    def test_full_integration_three_items_reasoned(self):
        """TS-ACT3-002"""
        result = evaluate_stage3_response(PROBLEM_MECHANISM_FIT, _PMF_STRONG, REASONED)
        if len(result.act2_evidence.confirmed_items) == 3:
            assert result.act3_capability.integration_observed == True

    def test_capability_absent_asserted_quality(self):
        """TS-ACT3-003"""
        result = evaluate_stage3_response(PROBLEM_MECHANISM_FIT, _PMF_STRONG, ASSERTED)
        assert result.act3_capability.capability_present == False

    def test_capability_absent_reasoned_one_item(self):
        """TS-ACT3-004"""
        response = "my invention addresses the core problem of motor failure detection"
        result = evaluate_stage3_response(PROBLEM_MECHANISM_FIT, response, REASONED)
        if len(result.act2_evidence.confirmed_items) < 2:
            assert result.act3_capability.capability_present == False

    def test_capability_absent_zero_items(self):
        """TS-ACT3-005"""
        result = evaluate_stage3_response(PROBLEM_MECHANISM_FIT, _EMPTY_RESPONSE, ASSERTED)
        assert result.act3_capability.capability_present == False
        assert result.act3_capability.integration_observed == False


class TestAct4ResolutionObservation:

    def test_resolution_indicated_when_capable(self):
        """TS-ACT4-001"""
        result = evaluate_stage3_response(PROBLEM_MECHANISM_FIT, _PMF_STRONG, REASONED)
        if result.act3_capability.capability_present:
            assert result.act4_resolution.sufficient_for_resolution == True
            assert "OA-1" in result.act4_resolution.notes

    def test_resolution_not_indicated_when_incapable(self):
        """TS-ACT4-002"""
        result = evaluate_stage3_response(PROBLEM_MECHANISM_FIT, _EMPTY_RESPONSE, ASSERTED)
        assert result.act4_resolution.sufficient_for_resolution == False

    def test_evaluator_does_not_modify_idea_state(self):
        """
        TS-ACT4-003 — MANDATORY
        evaluate_stage3_response() must not modify IdeaState in any way.
        """
        state = _make_clean_state()
        maturity_before = state.maturity_level
        stage_before = state.current_stage
        gaps_count_before = len(state.gaps)
        gaps_statuses_before = [g.status for g in state.gaps]
        iteration_before = state.iteration
        log_count_before = len(state.iteration_log)
        problem_before = state.known_problem
        mechanism_before = state.known_mechanism

        result = evaluate_stage3_response(
            PROBLEM_MECHANISM_FIT, _PMF_STRONG, REASONED,
            invention_reference=state.idea_summary
        )

        assert state.maturity_level == maturity_before, \
            "VIOLATION: evaluator modified maturity_level"
        assert state.current_stage == stage_before, \
            "VIOLATION: evaluator modified current_stage"
        assert len(state.gaps) == gaps_count_before, \
            "VIOLATION: evaluator modified gaps list"
        assert [g.status for g in state.gaps] == gaps_statuses_before, \
            "VIOLATION: evaluator modified gap statuses"
        assert state.iteration == iteration_before, \
            "VIOLATION: evaluator modified iteration"
        assert len(state.iteration_log) == log_count_before, \
            "VIOLATION: evaluator modified iteration_log"
        assert state.known_problem is problem_before, \
            "VIOLATION: evaluator modified known_problem"
        assert state.known_mechanism is mechanism_before, \
            "VIOLATION: evaluator modified known_mechanism"
        assert isinstance(result, Stage3EvaluationResult)
        assert result.is_stage3_gap == True


class TestCrossGapIntegration:

    def _capable(self, gap_type):
        responses = {
            PROBLEM_MECHANISM_FIT: _PMF_STRONG,
            ASSUMPTION_INVENTORY: _AI_STRONG,
            EXPERTISE_GAP_AWARENESS: _EGA_STRONG,
        }
        return evaluate_stage3_response(gap_type, responses[gap_type], REASONED)

    def _incapable(self, gap_type):
        return evaluate_stage3_response(gap_type, _EMPTY_RESPONSE, ASSERTED)

    def test_integration_checkable_two_evaluations(self):
        """TS-CGI-001"""
        evals = [self._capable(PROBLEM_MECHANISM_FIT), self._capable(ASSUMPTION_INVENTORY)]
        if all(e.act3_capability and e.act3_capability.capability_present for e in evals):
            result = check_cross_gap_integration(evals)
            assert result["integration_checkable"] == True
            assert result["sl_r3_proxy_met"] == True
            assert "OA-1" in result["note"]

    def test_integration_not_checkable_one_evaluation(self):
        """TS-CGI-002"""
        result = check_cross_gap_integration([self._capable(PROBLEM_MECHANISM_FIT)])
        assert result["integration_checkable"] == False

    def test_sl_r3_not_met_one_capable(self):
        """TS-CGI-003"""
        evals = [self._capable(PROBLEM_MECHANISM_FIT), self._incapable(ASSUMPTION_INVENTORY)]
        result = check_cross_gap_integration(evals)
        assert result["integration_checkable"] == True
        if result["capable_gap_count"] < 2:
            assert result["sl_r3_proxy_met"] == False

    def test_cross_gap_does_not_modify_state(self):
        """TS-CGI-004"""
        state = _make_clean_state()
        m_before = state.maturity_level
        g_before = len(state.gaps)
        i_before = state.iteration
        evals = [self._capable(PROBLEM_MECHANISM_FIT), self._capable(ASSUMPTION_INVENTORY)]
        check_cross_gap_integration(evals)
        assert state.maturity_level == m_before
        assert len(state.gaps) == g_before
        assert state.iteration == i_before


class TestFalsePositiveScenarios:

    def test_fp_enthusiasm_asserted(self):
        """TS-FP-001"""
        response = (
            "My invention completely addresses the problem because it uses advanced "
            "technology and solves all the key issues very effectively. It does not "
            "cover other domains but this mechanism is perfect for the problem."
        )
        result = evaluate_stage3_response(PROBLEM_MECHANISM_FIT, response, ASSERTED)
        assert result.act3_capability.capability_present == False

    def test_fp_keyword_stuffing_asserted(self):
        """TS-FP-002"""
        response = (
            "assume assumes assuming depends relies requires presupposes if given that "
            "unvalidated not yet proven need to verify uncertain I believe I expect "
            "should work might — these are all my assumptions about my invention."
        )
        result = evaluate_stage3_response(ASSUMPTION_INVENTORY, response, ASSERTED)
        assert result.act3_capability.capability_present == False

    def test_fp_long_no_signals_asserted(self):
        """TS-FP-003"""
        response = "a " * 100
        result = evaluate_stage3_response(EXPERTISE_GAP_AWARENESS, response, ASSERTED)
        assert result.act1_signals == []
        assert result.act3_capability.capability_present == False


class TestFalseNegativeScenarios:

    def test_fn_pmf_no_signal_words(self):
        """TS-FN-001: Document baseline — genuine PMF reasoning without signal words."""
        response = (
            "The root cause of the failure mode is insufficient real-time monitoring. "
            "Our approach provides continuous measurement rather than periodic sampling. "
            "This distinction is critical — periodic sampling misses transient events. "
            "The mechanism is not suitable for static load conditions."
        )
        result = evaluate_stage3_response(PROBLEM_MECHANISM_FIT, response, REASONED)
        confirmed_count = len(result.act2_evidence.confirmed_items)
        assert isinstance(confirmed_count, int)  # result is structurally valid

    def test_fn_ai_different_phrasing(self):
        """TS-FN-002: Document baseline — genuine AI without signal words."""
        response = (
            "The motor draws 2A under normal load — this figure comes from the datasheet "
            "but we have not tested it at scale. If this turns out to be wrong, "
            "the power supply would be undersized and the whole system would shut down."
        )
        result = evaluate_stage3_response(ASSUMPTION_INVENTORY, response, REASONED)
        confirmed_count = len(result.act2_evidence.confirmed_items)
        assert isinstance(confirmed_count, int)


class TestIOCEmergenceObservation:

    def test_ioc_emergence_all_three_capable(self):
        """TS-IOC-001"""
        evals = [
            evaluate_stage3_response(PROBLEM_MECHANISM_FIT, _PMF_STRONG, REASONED),
            evaluate_stage3_response(ASSUMPTION_INVENTORY, _AI_STRONG, REASONED),
            evaluate_stage3_response(EXPERTISE_GAP_AWARENESS, _EGA_STRONG, REASONED),
        ]
        integration = check_cross_gap_integration(evals)
        assert integration["integration_checkable"] == True
        assert isinstance(integration["capable_gap_count"], int)
        assert "IOC_CAP" not in str(integration)
        assert "IOC_SCORE" not in str(integration)

    def test_no_ioc_cap_constant_in_module(self):
        """TS-IOC-002"""
        import engine.stage3_evaluator as ev
        assert not hasattr(ev, "IOC_CAP"), "VIOLATION: IOC_CAP defined — IOC position violated"
        assert not hasattr(ev, "IOC_SCORE"), "VIOLATION: IOC_SCORE defined"
        assert not hasattr(ev, "IOC_THRESHOLD"), "VIOLATION: IOC_THRESHOLD defined"


class TestBoundaryConditions:

    def test_empty_response_no_exception(self):
        """TS-BC-001"""
        for gap_type in [PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS]:
            result = evaluate_stage3_response(gap_type, _EMPTY_RESPONSE, ASSERTED)
            assert result is not None
            assert result.act3_capability.capability_present == False

    def test_none_invention_reference_no_exception(self):
        """TS-BC-002"""
        result = evaluate_stage3_response(
            PROBLEM_MECHANISM_FIT, _PMF_STRONG, REASONED, invention_reference=None
        )
        assert isinstance(result, Stage3EvaluationResult)

    def test_unknown_gap_type_returns_empty(self):
        """TS-BC-003"""
        result = evaluate_stage3_response("UNKNOWN_GAP", _PMF_STRONG, REASONED)
        assert result.is_stage3_gap == False
        assert result.act2_evidence is None

    def test_all_stage3_gaps_no_exception(self):
        """TS-BC-004"""
        pairs = [
            (PROBLEM_MECHANISM_FIT, _PMF_STRONG),
            (ASSUMPTION_INVENTORY, _AI_STRONG),
            (EXPERTISE_GAP_AWARENESS, _EGA_STRONG),
        ]
        for gap_type, response in pairs:
            result = evaluate_stage3_response(gap_type, response, REASONED)
            assert result.is_stage3_gap == True
            assert result.act2_evidence is not None
            assert result.act3_capability is not None
            assert result.act4_resolution is not None

    def test_stage2_gaps_return_gracefully(self):
        """TS-BC-005"""
        for gap_type in [MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY]:
            result = evaluate_stage3_response(gap_type, _PMF_STRONG, REASONED)
            assert result.is_stage3_gap == False
            assert result.act1_signals == []

    def test_result_structure_complete_all_stage3(self):
        """TS-BC-006"""
        for gap_type, response in [
            (PROBLEM_MECHANISM_FIT, _PMF_STRONG),
            (ASSUMPTION_INVENTORY, _AI_STRONG),
            (EXPERTISE_GAP_AWARENESS, _EGA_STRONG),
        ]:
            result = evaluate_stage3_response(gap_type, response, REASONED)
            assert result.gap_type == gap_type
            assert isinstance(result.act1_signals, list)
            assert isinstance(result.act2_evidence, EvidenceObservation)
            assert isinstance(result.act3_capability, CapabilityObservation)
            assert isinstance(result.act4_resolution, ResolutionObservation)
