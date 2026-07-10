"""
tests/test_acknowledged_unknowns.py
Governance: TRANSITION_AUTHORIZATION_GOVERNANCE s4 Layer 1 PGC-3
Authorization: Owner-authorized 2026-06-06
"""
import pytest
from engine.idea_state import (
    IdeaState, AcknowledgedUnknown,
    PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
    ASSERTED, REASONED, PARTIAL,
)
from engine.progression_loop import (
    _detect_acknowledged_unknown, assess_response, integrate_response,
)


class TestDataclass:
    def test_importable(self):
        u = AcknowledgedUnknown(3, PHYSICAL_FEASIBILITY,
            "I do not know the exact sensing principle and have not yet "
            "identified the specific method to use.", "i do not know")
        assert u.iteration == 3
        assert u.gap_context == PHYSICAL_FEASIBILITY

    def test_no_resolved_field(self):
        u = AcknowledgedUnknown(1, "PF", "test verbatim here long enough", "marker")
        assert not hasattr(u, "resolved")
        assert not hasattr(u, "resolved_at")

    def test_ideastate_has_field(self):
        s = IdeaState(idea_id="t1")
        assert hasattr(s, "acknowledged_unknowns")
        assert s.acknowledged_unknowns == []

    def test_independent_lists(self):
        s1, s2 = IdeaState(idea_id="a"), IdeaState(idea_id="b")
        s1.acknowledged_unknowns.append(
            AcknowledgedUnknown(1, "PF", "verbatim text here long enough", "m"))
        assert s2.acknowledged_unknowns == []


class TestDetection:
    def test_detects_explicit_ignorance(self):
        r = ("I am not sure about the exact physical principle. "
             "I understand the outcome but have not yet identified "
             "the specific sensing method or engineering approach.")
        result = _detect_acknowledged_unknown(r, PHYSICAL_FEASIBILITY, 3)
        assert result is not None
        assert result.gap_context == PHYSICAL_FEASIBILITY
        # Fragment-capture correction (owner-authorized 2026-07-10): only the
        # sentence containing the explicit unknown marker is stored, not the
        # whole response.
        assert result.verbatim == "I am not sure about the exact physical principle."

    def test_detects_do_not_yet_know(self):
        r = ("I do not know the approximate power consumption or the "
             "exact energy source that would be used in the final "
             "implementation. Those details need further investigation.")
        assert _detect_acknowledged_unknown(r, PHYSICAL_FEASIBILITY, 4) is not None

    def test_detects_not_yet_researched(self):
        r = ("I am not aware of a specific existing solution using exactly "
             "the same pressure and flow monitoring for leak detection. "
             "Similar systems may exist but I have not yet researched them.")
        assert _detect_acknowledged_unknown(r, BOUNDARY_AMBIGUITY, 8) is not None

    def test_no_detection_short_response(self):
        assert _detect_acknowledged_unknown(
            "I don't know the sensing principle.", PHYSICAL_FEASIBILITY, 3) is None

    def test_no_detection_no_marker(self):
        r = ("The system uses pressure sensors to detect flow anomalies "
             "in building pipes. Pressure differential triggers comparator.")
        assert _detect_acknowledged_unknown(r, PHYSICAL_FEASIBILITY, 3) is None

    def test_no_detection_belief_statement(self):
        r = ("I believe the invention will require electrical power because "
             "it continuously monitors flow and analyzes patterns in real time.")
        assert _detect_acknowledged_unknown(r, PHYSICAL_FEASIBILITY, 4) is None

    def test_verbatim_is_bounded_marker_sentence(self):
        # Fragment-capture correction (owner-authorized 2026-07-10): this test
        # previously asserted the WHOLE multi-sentence response was stored as
        # the unknown — that was the defect. Only the marker sentence is kept,
        # verbatim.
        r = ("I do not yet know the exact technical limits, such as sensor "
             "accuracy, pressure range, signal frequency, or material "
             "constraints. These need investigation before building a prototype. "
             "The system must operate in normal building environments.")
        result = _detect_acknowledged_unknown(r, PHYSICAL_FEASIBILITY, 5)
        assert result is not None
        assert result.verbatim == (
            "I do not yet know the exact technical limits, such as sensor "
            "accuracy, pressure range, signal frequency, or material "
            "constraints.")


class TestProgressionUnchanged:
    def _s(self):
        state = IdeaState(idea_id="pt", domain_signal="electronics_electrical")
        state.domain = "electronics_electrical"  # set by run_iteration() normally
        return state

    def test_asserted_behavior_unchanged(self):
        r = ("I am not sure about the exact physical principle. "
             "I understand the outcome but not the sensing method "
             "or engineering approach that would be required.")
        result, reason = integrate_response(
            self._s(), PHYSICAL_FEASIBILITY, "Q?", r)
        assert result == "WARN"
        assert "asserted" in reason.lower()

    def test_unknown_recorded_with_asserted_gap(self):
        state = self._s()
        r = ("I am not sure about the exact physical principle. "
             "I understand the outcome but not the sensing method "
             "or engineering approach that would be required.")
        integrate_response(state, PHYSICAL_FEASIBILITY, "Q?", r)
        assert state.get_gap(PHYSICAL_FEASIBILITY).status == PARTIAL
        assert len(state.acknowledged_unknowns) == 1

    def test_reasoned_no_marker_records_nothing(self):
        state = self._s()
        r = ("The mechanism relies on capacitive sensing where the dielectric "
             "constant of water differs from air. The sensor measures capacitance "
             "across pipe wall sections and detects liquid presence.")
        integrate_response(state, PHYSICAL_FEASIBILITY, "Q?", r)
        assert state.acknowledged_unknowns == []
        assert state.get_gap(PHYSICAL_FEASIBILITY).status == PARTIAL

    def test_reasoned_with_marker_records_unknown_and_remains_reasoned(self):
        """REGRESSION: REASONED response with acknowledged unknown -- both recorded."""
        state = self._s()
        # Response contains causal structure + domain substance signal (sensor)
        # AND an explicit ignorance marker -- both should be recorded.
        # Confirmed REASONED by assess_response before adding to test.
        r = ("The sensor measures pressure differential across the pipe section "
             "because a leak causes a drop in flow resistance, which produces a "
             "measurable voltage change at the ADC input. The microcontroller "
             "compares the sampled value against a baseline threshold and triggers "
             "an alert when the deviation exceeds the configured limit. However, "
             "I do not yet know the required sensor accuracy or the sampling "
             "interval needed to reliably detect slow leaks without false positives.")
        # Verify REASONED independently before asserting on integration
        from engine.progression_loop import assess_response as ar
        quality = ar(r, "electronics_electrical")
        assert quality == REASONED, f"Test response must be REASONED, got {quality}"
        result, reason = integrate_response(state, PHYSICAL_FEASIBILITY, "Q?", r)
        assert result == "WARN"
        assert state.get_gap(PHYSICAL_FEASIBILITY).status == PARTIAL
        assert len(state.acknowledged_unknowns) == 1
        assert "i do not yet know" in state.acknowledged_unknowns[0].category_basis

    def test_assess_response_unchanged_asserted(self):
        assert assess_response("I don't know", "electronics_electrical") == ASSERTED

    def test_assess_response_unchanged_reasoned(self):
        r = ("The capacitive sensor measures dielectric change across the pipe "
             "wall because water has a dielectric constant of 80 vs air at 1, "
             "causing a measurable capacitance shift when liquid contacts wall.")
        assert assess_response(r, "electronics_electrical") == REASONED

    def test_evaluate_transition_ignores_unknowns(self):
        from engine.progression_loop import evaluate_transition
        state = self._s()
        state.acknowledged_unknowns.append(AcknowledgedUnknown(
            1, PHYSICAL_FEASIBILITY,
            "I do not know the sensing principle at all and cannot "
            "determine which approach would be most appropriate.", "i do not know"))
        can, _ = evaluate_transition(state)
        assert can is False

    def test_multiple_unknowns_accumulate(self):
        state = self._s()
        for gap, q, r in [
            (PHYSICAL_FEASIBILITY, "Q1?",
             "I am not sure about the exact physical principle. I understand "
             "the outcome but have not yet identified the sensing method or "
             "the underlying physics that would be required."),
            (PHYSICAL_FEASIBILITY, "Q2?",
             "I do not yet know the approximate power consumption or the "
             "exact energy source. Those engineering details need investigation."),
        ]:
            integrate_response(state, gap, q, r)
        assert len(state.acknowledged_unknowns) == 2


class TestFDC001:
    def _state_with_unknown(self):
        state = IdeaState(idea_id="fdc", domain_signal="electronics_electrical")
        state.acknowledged_unknowns.append(AcknowledgedUnknown(
            3, PHYSICAL_FEASIBILITY,
            "I am not sure about the exact physical principle. "
            "I understand the outcome but have not yet identified the sensing method.",
            "i am not sure about"))
        return state

    def test_s5_has_inventor_unknowns(self):
        from engine.deliverable_assembler import assemble_deliverable
        pkg = assemble_deliverable(self._state_with_unknown())
        assert "inventor_unknowns" in pkg["section_5_assumptions"]

    def test_s5_source_is_inventor_stated(self):
        from engine.deliverable_assembler import assemble_deliverable
        pkg = assemble_deliverable(self._state_with_unknown())
        u = pkg["section_5_assumptions"]["inventor_unknowns"]
        assert len(u) == 1
        assert u[0]["source"] == "inventor_stated"
        assert u[0]["gap_context"] == PHYSICAL_FEASIBILITY

    def test_s5_inferred_separate_from_stated(self):
        from engine.deliverable_assembler import assemble_deliverable
        pkg = assemble_deliverable(self._state_with_unknown())
        s5 = pkg["section_5_assumptions"]
        assert "assumptions" in s5
        assert "inventor_unknowns" in s5
        for a in s5.get("assumptions", []):
            assert a.get("source") != "inventor_stated"

    def test_s8_contains_acknowledged_unknown_type(self):
        from engine.deliverable_assembler import assemble_deliverable
        pkg = assemble_deliverable(self._state_with_unknown())
        items = pkg["section_8_unresolved_items"].get("items", [])
        assert any(i.get("type") == "acknowledged_unknown" for i in items)

    def test_s8_count(self):
        from engine.deliverable_assembler import assemble_deliverable
        pkg = assemble_deliverable(self._state_with_unknown())
        assert pkg["section_8_unresolved_items"]["acknowledged_unknown_count"] == 1

    def test_empty_state_no_break(self):
        from engine.deliverable_assembler import assemble_deliverable
        state = IdeaState(idea_id="e", domain_signal="electronics_electrical")
        pkg = assemble_deliverable(state)
        assert pkg["section_5_assumptions"]["inventor_unknowns"] == []
        assert pkg["section_8_unresolved_items"]["acknowledged_unknown_count"] == 0


class TestPGC3:
    def test_met_when_unknowns_present(self):
        state = IdeaState(idea_id="p1")
        state.acknowledged_unknowns.append(AcknowledgedUnknown(
            3, PHYSICAL_FEASIBILITY,
            "I do not know the exact sensing principle and have not yet "
            "identified which measurement approach to use.", "i do not know"))
        assert len(state.acknowledged_unknowns) > 0

    def test_not_met_when_empty(self):
        assert len(IdeaState(idea_id="p2").acknowledged_unknowns) == 0

    def test_evidence_references_gap_and_iteration(self):
        state = IdeaState(idea_id="p3")
        state.acknowledged_unknowns.append(AcknowledgedUnknown(
            3, PHYSICAL_FEASIBILITY,
            "I do not know the sensing principle and cannot determine "
            "which physical measurement approach to use.", "i do not know"))
        ev = [{"iteration": u.iteration, "gap_context": u.gap_context}
              for u in state.acknowledged_unknowns]
        assert ev[0]["iteration"] == 3
        assert ev[0]["gap_context"] == PHYSICAL_FEASIBILITY
