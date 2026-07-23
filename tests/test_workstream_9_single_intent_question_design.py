"""
test_workstream_9_single_intent_question_design.py — Workstream 9 BASE RED suite

Governance basis:
    docs/governance/WORKSTREAM_9_SINGLE_INTENT_QUESTION_DESIGN_INCREMENT_CONTRACT.md
    (base contract + Addendum A [paid-product experience] + Addendum B [F-1…F-5,
    operational single-intent rule and probes] + Addendum C [WS9-FV-1/FV-2]).
Authoritative tip at authoring: 4c7a57142e7714f331a280b4aaaba140da5d4de1
(WS9 contract merged via PR #235; status canonicalized via PR #236).
Hardened per independent BASE RED verdict C (findings WS9-BR-F1, F2, F3).

Purpose:
    Deterministic BASE RED for Single-Intent Question Design, targeting the
    committed observable serving seam
    engine.path_n_questions.get_path_n_question(gap_type, iterations_open),
    which returns approved Path N question text verbatim from
    docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json.

Design (hardened):
    * F1 — each independent answer component is detected by a small, bounded,
      reviewable MARKER SET (multiple synonyms), so a superficial synonym
      substitution that preserves the multi-intent structure still fails. The
      markers are tied to the contract-confirmed committed components; they are
      NOT the generic word "and" and are independent of question length
      (Addendum B.1/C.2).
    * F2 — N-BA-1 has THREE independently answerable components (operate /
      non-operate / confusion). The RED fails when a served question event
      matches markers for ANY two-or-more of the three; a GREEN preserving any
      pair (operate+non-operate, operate+confusion, non-operate+confusion)
      still fails.
    * F3 — for each confirmed gap the RED sweeps ALL currently reachable
      committed serving indices (not only the original defect index), so a
      confirmed multi-intent question cannot be dodged by moving it to another
      index within the same served surface.

    UNRESOLVED / protected boundary: the sweep EXCLUDES served texts that exactly
    equal a currently UNRESOLVED — PENDING BASE RED baseline (N-PF-3, N-BA-2,
    N-BA-3) or a protected single-intent baseline (N-PF-4). This guarantees the
    confirmed-defect sweep never forces an unresolved item into confirmed-defect
    status (contract Addendum B.2/C); those items remain UNRESOLVED and are not
    asserted here.

    Note (contract §5): this marker-based RED is a STRENGTHENED deterministic
    guard against cosmetic single-intent passes; it is NOT a substitute for the
    later independent GREEN implementation review of true single-intent design.

No production code, question text, UI, schema, registry, evaluator, progression,
persistence, prompt, or AI logic is modified. No GREEN. No Arabic-parity RED
(no committed Arabic variant; parity mandatory-but-conditional, Addendum B.3).
No perceptual/usability RED (requires later independent usability evidence).
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


# Number of committed variants per gap (serving-reachable indices are 0..N-1;
# get_path_n_question clamps iterations_open >= N-1 to the last variant).
_GAP_VARIANT_COUNT = {
    PHYSICAL_FEASIBILITY: 4,
    BOUNDARY_AMBIGUITY: 3,
    MECHANISM_COMPLETENESS: 4,
}


def _reachable_served_texts(gap_type):
    """All unique committed served texts for a gap across reachable indices."""
    seen = []
    for i in range(_GAP_VARIANT_COUNT[gap_type]):
        t = get_path_n_question(gap_type, i)
        assert isinstance(t, str) and t.strip()
        if t not in seen:
            seen.append(t)
    return seen


def _matches(text, markers):
    low = text.lower()
    return any(m.lower() in low for m in markers)


def _component_hits(text, components):
    """Number of distinct components (each a marker set) present in text."""
    return sum(1 for markers in components.values() if _matches(text, markers))


# CONFIRMED MULTI-INTENT profiles (bounded marker sets per independent component).
# A served text "bundles" the profile when it hits >= 2 distinct components.
CONFIRMED_PROFILES = {
    "N-PF-1": {
        "gap": PHYSICAL_FEASIBILITY,
        "components": {
            "safety_condition": ["work safely", "safely", "safe operation", "safe conditions"],
            "confirmation_evidence": ["confirm", "verify", "check later", "prove", "validate",
                                      "information would you need", "information you would need"],
        },
    },
    "N-PF-2": {
        "gap": PHYSICAL_FEASIBILITY,
        "components": {
            "sustaining_operation": ["keep the system running", "keep running", "keep it running",
                                     "continue operating", "maintain operation", "keep working"],
            "unknown_information": ["not know", "do not know", "don't know", "unsure",
                                    "uncertain", "not sure", "unresolved"],
        },
    },
    "N-BA-1": {  # three components (F2): failing on ANY two-or-more
        "gap": BOUNDARY_AMBIGUITY,
        "components": {
            "operate": ["should the system work", "should work", "expected to operate",
                        "react", "should activate"],
            "non_operate": ["should it not work", "should not work", "stay inactive",
                            "not react", "stay quiet", "should stay off"],
            "confusion": ["confuse", "confusing", "false trigger", "ambiguous", "mislead"],
        },
    },
}

# Currently UNRESOLVED — PENDING BASE RED (N-PF-3, N-BA-2, N-BA-3) and protected
# single-intent (N-PF-4) committed baselines, excluded from the confirmed sweep so
# no unresolved/protected item is forced into confirmed-defect status.
_EXCLUDED_BASELINES_BY_GAP = {
    PHYSICAL_FEASIBILITY: [get_path_n_question(PHYSICAL_FEASIBILITY, 2),   # N-PF-3 (unresolved)
                           get_path_n_question(PHYSICAL_FEASIBILITY, 3)],  # N-PF-4 (protected single-intent)
    BOUNDARY_AMBIGUITY: [get_path_n_question(BOUNDARY_AMBIGUITY, 1),       # N-BA-2 (unresolved)
                         get_path_n_question(BOUNDARY_AMBIGUITY, 2)],      # N-BA-3 (unresolved)
}


# ─────────────────────────────────────────────
# RED — no served question event may bundle >= 2 independent components
# ─────────────────────────────────────────────

@pytest.mark.parametrize("qid", list(CONFIRMED_PROFILES))
def test_RED_confirmed_multi_intent_not_served_anywhere(qid):
    """RED · Contract §8 AC-1/AC-2, Addendum B.1/C (F1/F2/F3): sweeping the full
    committed serving surface of the confirmed gap (excluding separately-recorded
    UNRESOLVED/protected baselines), NO served question event may present markers
    for two-or-more independently answerable components of the confirmed profile.
    Fails now because the confirmed multi-intent question is still served."""
    profile = CONFIRMED_PROFILES[qid]
    gap = profile["gap"]
    components = profile["components"]
    excluded = _EXCLUDED_BASELINES_BY_GAP.get(gap, [])
    offenders = []
    for text in _reachable_served_texts(gap):
        if text in excluded:
            continue
        hits = _component_hits(text, components)
        if hits >= 2:
            present = [c for c, m in components.items() if _matches(text, m)]
            offenders.append((text, present))
    assert not offenders, (
        f"{qid}: served question event(s) bundle >= 2 independent components "
        f"{[(o[1], o[0]) for o in offenders]}"
    )


# ─────────────────────────────────────────────
# PROTECTED — existing valid behavior unchanged (must PASS now)  [unchanged]
# ─────────────────────────────────────────────

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


@pytest.mark.parametrize("qid", list(PROTECTED_SINGLE_INTENT))
def test_PROTECTED_single_intent_questions_unchanged(qid):
    """PROTECTED · Contract §6/§8 AC-4: committed single-intent questions
    (N-MC-3, N-MC-4, N-PF-4) remain served verbatim and must not change."""
    gap_type, iters, expected = PROTECTED_SINGLE_INTENT[qid]
    assert get_path_n_question(gap_type, iters) == expected


def test_PROTECTED_serving_is_deterministic_by_index():
    """PROTECTED · Contract §12 (persistence/resume): the same committed state
    (gap_type, iterations_open) deterministically serves the same question."""
    for gap_type in (PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY, MECHANISM_COMPLETENESS):
        for i in range(_GAP_VARIANT_COUNT[gap_type]):
            assert get_path_n_question(gap_type, i) == get_path_n_question(gap_type, i)


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
