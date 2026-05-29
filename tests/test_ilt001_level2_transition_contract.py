"""
ILT-001 regression tests: Level 1->2 transition requires all Stage Two gaps CLOSED.

Contract (GD-001 / ILT-F-001 fix):
  REQUIRED_STAGE_TWO_GAPS = [MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY]
  All three must exist AND be CLOSED before maturity can reach 2.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.idea_state import IdeaState, Evidence, Gap, CLOSED, OPEN, PARTIAL
from engine.progression_loop import evaluate_transition
from engine.idea_state import (
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY, REASONED
)


def _state_at_level_1_with_gaps(*gap_specs):
    """Build an IdeaState at maturity_level=1 with specified gaps.
    Each gap_spec is (gap_type, status).
    known_mechanism set to REASONED evidence so the quality check passes.
    """
    state = IdeaState(idea_id="ilt-001-regression")
    state.maturity_level = 1
    state.known_mechanism = Evidence(
        content="Dielectric constant changes RC charge time proportionally.",
        quality=REASONED,
        iteration=1,
    )
    state.known_problem = Evidence(
        content="Soil moisture level is unknown without measurement.",
        quality=REASONED,
        iteration=1,
    )
    for gap_type, status in gap_specs:
        gap = Gap(gap_type=gap_type, status=status, opened_at=1)
        state.gaps.append(gap)
    return state


# ── Test 1: MC CLOSED alone — must NOT allow Level 2 ────────────────────────
def test_mc_closed_alone_does_not_allow_level_2():
    """MECHANISM_COMPLETENESS closed but PF and BA missing — must block."""
    state = _state_at_level_1_with_gaps(
        (MECHANISM_COMPLETENESS, CLOSED),
    )
    can, reason = evaluate_transition(state)
    assert can is False, f"Expected False, got True. Reason: {reason}"
    assert "PHYSICAL_FEASIBILITY" in reason or "BLOCK" in reason, (
        f"Expected BLOCK reason mentioning PHYSICAL_FEASIBILITY, got: {reason}"
    )


# ── Test 2: MC CLOSED + PF missing + BA missing — must block ────────────────
def test_mc_closed_pf_missing_ba_missing_blocks():
    """Only MC present and CLOSED — PF and BA never opened — must block."""
    state = _state_at_level_1_with_gaps(
        (MECHANISM_COMPLETENESS, CLOSED),
    )
    can, reason = evaluate_transition(state)
    assert can is False, f"Expected False, got True. Reason: {reason}"


# ── Test 3: MC CLOSED + PF CLOSED + BA missing — must block ─────────────────
def test_mc_closed_pf_closed_ba_missing_blocks():
    """MC and PF both CLOSED but BA never opened — must block."""
    state = _state_at_level_1_with_gaps(
        (MECHANISM_COMPLETENESS, CLOSED),
        (PHYSICAL_FEASIBILITY, CLOSED),
    )
    can, reason = evaluate_transition(state)
    assert can is False, f"Expected False, got True. Reason: {reason}"
    assert "BOUNDARY_AMBIGUITY" in reason or "BLOCK" in reason, (
        f"Expected BLOCK reason mentioning BOUNDARY_AMBIGUITY, got: {reason}"
    )


# ── Test 4: MC CLOSED + PF PARTIAL — must block ─────────────────────────────
def test_mc_closed_pf_partial_blocks():
    """PF is PARTIAL (not CLOSED) — must block."""
    state = _state_at_level_1_with_gaps(
        (MECHANISM_COMPLETENESS, CLOSED),
        (PHYSICAL_FEASIBILITY, PARTIAL),
        (BOUNDARY_AMBIGUITY, OPEN),
    )
    can, reason = evaluate_transition(state)
    assert can is False, f"Expected False, got True. Reason: {reason}"


# ── Test 5: All three CLOSED — must allow Level 2 ───────────────────────────
def test_all_three_gaps_closed_allows_level_2():
    """MC + PF + BA all CLOSED — transition must be allowed."""
    state = _state_at_level_1_with_gaps(
        (MECHANISM_COMPLETENESS, CLOSED),
        (PHYSICAL_FEASIBILITY, CLOSED),
        (BOUNDARY_AMBIGUITY, CLOSED),
    )
    can, reason = evaluate_transition(state)
    assert can is True, f"Expected True, got False. Reason: {reason}"
    assert "LEVEL 2" in reason or "ready" in reason.lower(), (
        f"Expected ready-for-LEVEL-2 reason, got: {reason}"
    )
