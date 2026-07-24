"""
test_workstream_9_single_intent_question_design.py — Workstream 9 BASE RED suite

Governance basis:
    docs/governance/WORKSTREAM_9_SINGLE_INTENT_QUESTION_DESIGN_INCREMENT_CONTRACT.md
    (base contract + Addendum A [paid-product experience] + Addendum B [F-1…F-5,
    operational single-intent rule and probes] + Addendum C [WS9-FV-1/FV-2]).
Authoritative tip at authoring: 4c7a57142e7714f331a280b4aaaba140da5d4de1
(WS9 contract merged via PR #235; status canonicalized via PR #236).
Hardened per independent BASE RED verdicts C: WS9-BR-F1/F2/F3 then F8/F9/F10.

Purpose:
    Deterministic BASE RED for Single-Intent Question Design against the committed
    observable serving seam engine.path_n_questions.get_path_n_question, which
    serves approved Path N question text verbatim from the committed artifact
    docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json.

Hardening summary:
    F1  bounded, reviewable MARKER SETS per independent component (not "and",
        length-independent).
    F2  N-BA-1 has THREE components (operate/non-operate/confusion); failing on
        ANY two-or-more.
    F3  sweep the WHOLE committed serving surface, not just the original index.
    F8  exclusions are EXACT committed-text identity literals for the currently
        UNRESOLVED/protected baselines (N-PF-3, N-PF-4, N-BA-2, N-BA-3) — NOT
        index-derived. A confirmed multi-intent question moved into a formerly
        excluded index still fails; a rewritten unresolved question that no longer
        matches its committed baseline is no longer auto-excluded.
    F9  the sweep is ARTIFACT-DRIVEN: the current variant list per gap is read
        from the committed JSON artifact (test-only read of the same file the
        serving implementation uses), so a bundled question appended at a new
        reachable index still fails. A diagnostic confirms the serving seam
        reaches every artifact-defined variant. No count is frozen.
    F10 N-PF-2 sustaining-operation markers cover obvious inflections
        ("keeps the system running", "system running") without bare "run".

    Note (contract §5): this marker-based RED is a strengthened deterministic
    guard against cosmetic single-intent passes; it is NOT a substitute for the
    later independent GREEN implementation review.

No production code, question content, UI, schema, registry, evaluator,
progression, persistence, prompt, or AI logic is modified. No GREEN. No
Arabic-parity RED (no committed Arabic variant; parity mandatory-but-conditional,
Addendum B.3). No perceptual/usability RED. Adversarial controls use synthetic
in-memory served surfaces only (no on-disk patching). RED cases fail by assertion
against real served behavior; they do not crash.
"""

import json
import pathlib

import importlib
import pytest

from engine.path_n_questions import get_path_n_question
from engine.idea_state import (
    IdeaState, Gap,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
    OPEN, PARTIAL,
)
from engine.progression_loop import select_next_gap, GAP_PRIORITY


# The committed question-content artifact the serving implementation uses.
_ARTIFACT_PATH = pathlib.Path(
    "docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json"
)


def _artifact_variants(gap_type):
    """(F9) Read the current committed variant texts for a gap from the artifact.
    Test-only read of the same file engine.path_n_questions serves from; the
    variant count is NOT frozen — newly added variants are swept automatically."""
    data = json.loads(_ARTIFACT_PATH.read_text(encoding="utf-8"))
    return [entry["text"] for entry in data["gaps"][gap_type]]


# (F8) EXACT committed-text identity exclusions — pinned string literals, not
# index-derived. Only a served text EXACTLY equal to one of these is excluded.
EXCLUDED_BASELINES = {
    # UNRESOLVED — PENDING BASE RED (contract Addendum B.2/C):
    "N-PF-3": "Are there real-world conditions, such as heat, water, time, or wear, "
              "that might stop it from working? Which ones worry you most?",
    "N-BA-2": "What is your idea responsible for, and what is someone or something else's job?",
    "N-BA-3": "Describe a situation where the system should definitely react, and one "
              "where it should definitely stay quiet.",
    # Protected single-intent (also separately protected verbatim below):
    "N-PF-4": "If an engineer offered to check one thing about whether this can "
              "physically work, what would you ask them to check first?",
}
_EXCLUDED_TEXTS = frozenset(EXCLUDED_BASELINES.values())


def _matches(text, markers):
    low = text.lower()
    return any(m.lower() in low for m in markers)


def _bundle_offenders(served_texts, components, excluded=_EXCLUDED_TEXTS):
    """Pure helper: served texts (excluding exact pinned baselines) that present
    markers for >= 2 distinct independent components of a confirmed profile."""
    offenders = []
    for text in served_texts:
        if text in excluded:
            continue
        present = [name for name, markers in components.items() if _matches(text, markers)]
        if len(present) >= 2:
            offenders.append((text, present))
    return offenders


# CONFIRMED MULTI-INTENT profiles — bounded marker sets per independent component.
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
            # F10: inflection coverage ("keeps the system running", "system running")
            # without introducing bare "run".
            "sustaining_operation": ["keep the system running", "keeps the system running",
                                     "system running", "keep running", "keeps running",
                                     "keep it running", "keeps it running", "continue operating",
                                     "maintain operation", "keep working", "keeps working"],
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


# ─────────────────────────────────────────────
# RED — no served question event may bundle >= 2 independent components
# (artifact-driven full-surface sweep; identity-based exclusions)
# ─────────────────────────────────────────────

@pytest.mark.parametrize("qid", list(CONFIRMED_PROFILES))
def test_RED_confirmed_multi_intent_not_served_anywhere(qid):
    """RED · Contract §8 AC-1/AC-2, Addendum B.1/C (F1/F2/F3/F8/F9): sweeping the
    full artifact-defined serving surface of the confirmed gap (excluding only
    exact committed UNRESOLVED/protected baseline strings), NO served question
    event may present markers for two-or-more independent components of the
    confirmed profile. Fails now because the confirmed multi-intent question is
    still served."""
    profile = CONFIRMED_PROFILES[qid]
    served = _artifact_variants(profile["gap"])
    offenders = _bundle_offenders(served, profile["components"])
    assert not offenders, (
        f"{qid}: served question event(s) bundle >= 2 independent components: "
        f"{[(o[1], o[0]) for o in offenders]}"
    )


def test_diagnostic_serving_seam_reaches_every_artifact_variant():
    """Diagnostic (F9): the serving seam get_path_n_question reaches every
    artifact-defined variant for the swept gaps (no frozen count)."""
    for gap in (PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY, MECHANISM_COMPLETENESS):
        variants = _artifact_variants(gap)
        for i, expected in enumerate(variants):
            assert get_path_n_question(gap, i) == expected


# ─────────────────────────────────────────────
# ADVERSARIAL CONTROLS (synthetic in-memory served surfaces; no on-disk patching)
# ─────────────────────────────────────────────

_N_PF_1 = "What would need to be true for this system to work safely, and what information would you need later to confirm it?"
_N_BA_1 = "When should the system work, when should it not work, and what situations might confuse it?"
_HONEST_SINGLE = "What would need to be true for this system to work safely?"


def test_ADV_confirmed_defect_at_formerly_excluded_index_still_fails():
    """ADV-1 (F8): a still-multi-intent question placed where an excluded baseline
    used to sit is NOT excluded (identity, not index) and is flagged."""
    surface = [EXCLUDED_BASELINES["N-BA-3"], _N_BA_1]  # N-BA-1 sits at the ex-N-BA-3 slot
    offenders = _bundle_offenders(surface, CONFIRMED_PROFILES["N-BA-1"]["components"])
    assert [o[0] for o in offenders] == [_N_BA_1]


def test_ADV_confirmed_defect_appended_as_new_variant_fails():
    """ADV-2 (F9): the verbatim confirmed defect appended at a new reachable index
    is flagged even alongside an honest single-intent question."""
    surface = [_HONEST_SINGLE, _N_PF_1]
    offenders = _bundle_offenders(surface, CONFIRMED_PROFILES["N-PF-1"]["components"])
    assert [o[0] for o in offenders] == [_N_PF_1]


def test_ADV_n_pf_2_inflection_fails():
    """ADV-3 (F10): the sustaining-operation inflection is caught."""
    surface = ["What keeps the system running, and what are you still uncertain about?"]
    offenders = _bundle_offenders(surface, CONFIRMED_PROFILES["N-PF-2"]["components"])
    assert len(offenders) == 1


def test_ADV_honest_single_intent_split_passes():
    """ADV-4: an honest single-intent split (one component only) is NOT flagged."""
    for prof in ("N-PF-1", "N-PF-2", "N-BA-1"):
        assert _bundle_offenders([_HONEST_SINGLE], CONFIRMED_PROFILES[prof]["components"]) == []


def test_ADV_exact_unresolved_baselines_excluded_but_rewrites_not():
    """ADV-5 (F8): exact committed unresolved baselines remain excluded (not forced
    into confirmed-defect status), while a rewritten unresolved question that no
    longer matches the baseline is no longer auto-excluded."""
    ba = CONFIRMED_PROFILES["N-BA-1"]["components"]
    # N-BA-3 baseline bundles operate+non_operate but is excluded by identity:
    assert _bundle_offenders([EXCLUDED_BASELINES["N-BA-3"]], ba) == []
    # A rewritten unresolved question (not equal to the baseline) is evaluated:
    rewritten = ("When should it react, when should it stay quiet, and what might "
                 "confuse it?")
    assert len(_bundle_offenders([rewritten], ba)) == 1


def test_ADV_protected_single_intent_baseline_excluded_from_sweep():
    """ADV-6: N-PF-4 protected baseline is excluded from the confirmed sweep."""
    for prof in ("N-PF-1", "N-PF-2"):
        assert _bundle_offenders([EXCLUDED_BASELINES["N-PF-4"]],
                                 CONFIRMED_PROFILES[prof]["components"]) == []


# ─────────────────────────────────────────────
# PROTECTED — existing valid behavior unchanged (must PASS now)
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
    (gap_type, iterations_open) deterministically serves the same question,
    across every artifact-defined variant."""
    for gap_type in (PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY, MECHANISM_COMPLETENESS):
        for i in range(len(_artifact_variants(gap_type))):
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
    """PROTECTED · Contract §5 / P6 / F-4: no WS11 evaluator, WS13 guided-answer,
    or WS14 adaptive-follow-up module is introduced.

    WS10 (engine.question_intent_registry) is intentionally NOT guarded here: WS10
    is the active, owner-authorized workstream explicitly authorized to introduce
    that module, so the WS10 absence guard is stale (owner-approved amendment). The
    WS11/WS13/WS14 protections remain valid and unchanged."""
    for absent in (
        "engine.question_aware_evaluation",  # WS11
        "engine.guided_answer_support",      # WS13
        "engine.adaptive_follow_up",         # WS14
    ):
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module(absent)
