"""
test_workstream_9_single_intent_question_design.py — Workstream 9 BASE RED suite

Governance basis:
    docs/governance/WORKSTREAM_9_SINGLE_INTENT_QUESTION_DESIGN_INCREMENT_CONTRACT.md
    (base contract + Addendum A [paid-product experience] + Addendum B [F-1…F-5,
    operational single-intent rule and probes] + Addendum C [WS9-FV-1/FV-2]).
Authoritative tip at authoring: 4c7a57142e7714f331a280b4aaaba140da5d4de1
(WS9 contract merged via PR #235; status canonicalized via PR #236).

Purpose:
    Deterministic BASE RED for Single-Intent Question Design, targeting the
    committed observable question-serving seam
    engine.path_n_questions.get_path_n_question(gap_type, iterations_open),
    which returns the approved Path N question text verbatim from
    docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json.

Classification / design (see Addendum B/C of the contract):
    RED — expected to FAIL now, on a deterministic assertion, for the exact
          missing WS9 behavior: the CONFIRMED MULTI-INTENT questions
          (N-PF-1, N-PF-2, N-BA-1) are still served with BOTH of their two
          independently-answerable component anchors present in one served
          question event. A single-intent redesign (GREEN) asks only one
          component, so the served text will no longer contain both anchors.
          The anchors are the SPECIFIC committed component phrases the contract
          identified as bundled — NOT the generic word "and" (Addendum B.1/C.2
          prohibit classifying merely on length or "and").
    PROTECTED — expected to PASS now, proving existing valid single-intent
          questions and Workstreams 1–8 behavior are unchanged, and that no
          Workstream 10–14 capability is introduced.

    UNRESOLVED (no RED created; recorded, not forced): N-MC-2, N-PF-3, N-BA-2,
          N-BA-3 remain UNRESOLVED — PENDING BASE RED SOURCE ANALYSIS (contract
          B.2/C). The four diagnostic probes are semantic judgments the owner
          left unresolved; per contract §5 no failing test is created for them.

No production code is modified. No GREEN. No registry/schema/evaluator/
progression/persistence/UI change. No Arabic-parity RED (no committed Arabic
variant exists — parity is mandatory-but-conditional per Addendum B.3). No
perceptual/usability RED (those require later independent usability evidence).
RED cases fail by assertion against real served behavior; they do not crash.
"""

import importlib

import pytest

from engine.path_n_questions import get_path_n_question
from engine.idea_state import (
    IdeaState, Gap,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
    OPEN, PARTIAL,
)
from engine.progression_loop import select_next_gap, GAP_PRIORITY


# Committed serving indices (get_path_n_question indexes the per-gap variant list
# by min(iterations_open, len-1)). Verified against the committed JSON at authoring.
CONFIRMED_MULTI_INTENT = {
    # question_id: (gap_type, iterations_open, [component-anchor-A, component-anchor-B])
    "N-PF-1": (PHYSICAL_FEASIBILITY, 0, ["work safely", "confirm it"]),
    "N-PF-2": (PHYSICAL_FEASIBILITY, 1, ["keep the system running", "not know yet"]),
    "N-BA-1": (BOUNDARY_AMBIGUITY, 0, ["should it not work", "confuse it"]),
}

# Committed single-intent questions that must remain unchanged (protected baseline).
PROTECTED_SINGLE_INTENT = {
    "N-MC-3": (MECHANISM_COMPLETENESS, 2,
               "Walk through what happens step by step, from the moment the problem "
               "starts to the moment someone knows about it."),
    "N-MC-4": (MECHANISM_COMPLETENESS, 3,
               "Is there any part of how it works that you're unsure about or imagining "
               "loosely? Describe it as best you can."),
    "N-PF-4": (PHYSICAL_FEASIBILITY, 3,
               "If an engineer offered to check one thing about whether this can "
               "physically work, what would you ask them to check first?"),
}


# ─────────────────────────────────────────────
# RED — confirmed multi-intent questions still bundle two independent components
# ─────────────────────────────────────────────

@pytest.mark.parametrize("qid", list(CONFIRMED_MULTI_INTENT))
def test_RED_confirmed_question_no_longer_bundles_two_independent_components(qid):
    """RED · Contract §8 AC-1/AC-2, Addendum B.1/C: a CONFIRMED MULTI-INTENT question
    must be redesigned to a single component, so the served text must NOT contain
    BOTH of its identified independently-answerable component anchors at once."""
    gap_type, iters, (anchor_a, anchor_b) = CONFIRMED_MULTI_INTENT[qid]
    served = get_path_n_question(gap_type, iters)
    assert served is not None
    both_present = (anchor_a in served) and (anchor_b in served)
    # WS9 target: not both — a single-intent question asks one component.
    assert not both_present, (
        f"{qid} still bundles two independently-answerable components "
        f"({anchor_a!r} and {anchor_b!r}) in one served question: {served!r}"
    )


# ─────────────────────────────────────────────
# PROTECTED — existing valid behavior unchanged (must PASS now)
# ─────────────────────────────────────────────

@pytest.mark.parametrize("qid", list(PROTECTED_SINGLE_INTENT))
def test_PROTECTED_single_intent_questions_unchanged(qid):
    """PROTECTED · Contract §6/§8 AC-4: committed single-intent questions
    (N-MC-3, N-MC-4, N-PF-4) remain served verbatim and must not change."""
    gap_type, iters, expected = PROTECTED_SINGLE_INTENT[qid]
    assert get_path_n_question(gap_type, iters) == expected


def test_PROTECTED_serving_is_deterministic_by_index():
    """PROTECTED · Contract §12 (persistence/resume): the same committed state
    (gap_type, iterations_open) deterministically serves the same question."""
    for gap_type, iters, _ in CONFIRMED_MULTI_INTENT.values():
        assert get_path_n_question(gap_type, iters) == get_path_n_question(gap_type, iters)


def test_PROTECTED_ordering_selection_unchanged():
    """PROTECTED · Contract §6 / P4: WS8 fixed-priority selection is unchanged;
    WS9 introduces no ordering (WS8) behavior."""
    s = IdeaState(idea_id="ws9")
    for gt in (BOUNDARY_AMBIGUITY, MECHANISM_COMPLETENESS):
        s.gaps.append(Gap(gap_type=gt, status=OPEN, opened_at=1))
    assert select_next_gap(s) == GAP_PRIORITY[0] == MECHANISM_COMPLETENESS


def test_PROTECTED_partial_and_unknown_states_preserved():
    """PROTECTED · Contract §11 / P3: PARTIAL gaps remain selectable and the
    acknowledged-unknown model remains importable (unknown/deferred preserved)."""
    s = IdeaState(idea_id="ws9-partial")
    s.gaps.append(Gap(gap_type=BOUNDARY_AMBIGUITY, status=PARTIAL, opened_at=1))
    assert select_next_gap(s) == BOUNDARY_AMBIGUITY
    from engine.idea_state import AcknowledgedUnknown  # noqa: F401 — must remain importable


def test_PROTECTED_workstreams_1_to_8_modules_intact():
    """PROTECTED · Contract §6 / P2: WS1–8 protected modules import unchanged."""
    for mod, attr in (
        ("engine.safety_signal", "SafetySignal"),
        ("engine.requirement_landscape", None),
        ("engine.validation_plan", None),
    ):
        m = importlib.import_module(mod)
        if attr:
            assert hasattr(m, attr)


def test_PROTECTED_no_workstream_10_to_14_capability_introduced():
    """PROTECTED · Contract §5 / P6 / F-4: no WS10 registry, WS11 evaluator,
    WS13 guided-answer, or WS14 adaptive-follow-up module is introduced."""
    for absent in (
        "engine.question_intent_registry",   # WS10
        "engine.question_aware_evaluation",  # WS11
        "engine.guided_answer_support",      # WS13
        "engine.adaptive_follow_up",         # WS14
    ):
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module(absent)
