"""
test_workstream_11_question_aware_evaluation_base_red.py
Workstream 11 — Question-Aware Evaluation BASE RED.

Governance basis (merged, authoritative):
    docs/governance/WORKSTREAM_11_QUESTION_AWARE_EVALUATION_OWNER_DECISIONS.md
        (F1–F11 baseline; D1–D18 owner decisions, incl. D4 atomic ServedQuestion
        binding, D7.1 structural tier→outcome, D7.1.T/D14.T truthful boundary,
        D9 fail-loud typed errors, D13/D14 registry + observation boundaries).

Purpose (deterministic BASE RED):
    Encode the ratified WS11 v1 public contract through the approved seams that
    do NOT yet exist:

      * the pure evaluator module `engine.question_aware_evaluation` with
        `evaluate_question_intent(question_id, base_quality, served_design_gap_id,
        registry) -> QuestionIntentEvaluation` and the typed
        `QuestionIntentEvaluationError` (D3/D6/D9);
      * the atomic served-question producer `engine.path_n_questions.
        get_served_question(gap_type, iterations_open) -> ServedQuestion`
        carrying `question_id`/`text`/`design_gap_id` from one committed entry,
        with `get_path_n_question` retained as a backward-compatible text wrapper
        (D4).

Controlled-RED discipline (contract §RED-design; mirrors the merged WS10 RED):
    This module imports ONLY the standard library and already-existing engine
    modules at top level; it never imports `engine.question_aware_evaluation` at
    module scope and never references the not-yet-existing served-question seam at
    collection time. Every test resolves the missing WS11 seam through a helper
    (`_require_evaluator` / `_require_served_question_*`) that converts a missing
    module/symbol into a clear, decision-tagged `pytest.fail(...)`. Therefore all
    tests COLLECT cleanly and each fails for the one intended reason — the
    authorized WS11 seam is absent — never as an uncontrolled import/collection or
    fixture error. No skips, xfails, placeholders, or pass-forcing monkeypatches
    are used, and no test merely asserts the module is absent.

Scope: no production code, existing test, governance file, or registry artifact is
modified; `engine.question_aware_evaluation` is NOT created. The already-merged
WS10 loader is reused (dependency injection) to build valid registries on
temporary fixtures; WS11 must consume that object and never re-parse registry JSON.
"""

import importlib
import json
import pathlib

import pytest

# Already-existing, merged WS10 public surface (safe to import at module scope).
from engine.question_intent_registry import (
    load_question_intent_registry,
    QuestionIntentRegistry,
    QuestionIntentNotFoundError,
)

_WS11_MODULE = "engine.question_aware_evaluation"

# Approved deterministic base-quality tiers (existing assess_response tiers, F2).
_DEMONSTRATED = "DEMONSTRATED"
_REASONED = "REASONED"
_ASSERTED = "ASSERTED"

# Approved D7.1 structural outcome vocabulary (returned results).
_SATISFIED = "SATISFIED"
_PARTIALLY_SATISFIED = "PARTIALLY_SATISFIED"
_NOT_SATISFIED = "NOT_SATISFIED"

# Approved tier → outcome mapping (D7.1).
_TIER_TO_OUTCOME = {
    _DEMONSTRATED: _SATISFIED,
    _REASONED: _PARTIALLY_SATISFIED,
    _ASSERTED: _NOT_SATISFIED,
}

# Approved D9 typed failure reason codes for WS11 integrity/identity failures.
_DESIGN_GAP_MISMATCH = "DESIGN_GAP_MISMATCH"
_MISSING_ACTIVE_QUESTION_ID = "MISSING_ACTIVE_QUESTION_ID"
_INVALID_BASE_QUALITY = "INVALID_BASE_QUALITY"

# Canonical committed design gaps (D5) and the exact approved result field set (D6).
_CANONICAL_GAPS = ("MECHANISM_COMPLETENESS", "PHYSICAL_FEASIBILITY", "BOUNDARY_AMBIGUITY")
_APPROVED_RESULT_FIELDS = frozenset({
    "question_id", "intent_id", "design_gap_id", "base_quality", "outcome",
    "matched_objectives", "unmet_objectives", "reason_code",
})

# Names that would constitute a prohibited text -> question_id recovery path (D4.4).
_FORBIDDEN_REVERSE_LOOKUP_NAMES = (
    "question_id_for_text", "get_question_id_from_text", "id_from_text",
    "lookup_question_id", "reverse_lookup", "match_question_by_text",
    "question_id_by_text", "text_to_question_id",
)

# A small self-consistent registry fixture in committed source order.
_SOURCE_QUESTIONS = (
    ("MECHANISM_COMPLETENESS", "N-MC-1", "How does it notice the problem?"),
    ("MECHANISM_COMPLETENESS", "N-MC-2", "What are the main parts?"),
    ("PHYSICAL_FEASIBILITY", "N-PF-1", "What must be true to work safely?"),
    ("BOUNDARY_AMBIGUITY", "N-BA-1", "Which situations should it handle?"),
)
_KNOWN_QID = "N-MC-1"
_KNOWN_GAP = "MECHANISM_COMPLETENESS"


# ── Controlled-RED seam resolvers (missing seam -> decision-tagged failure) ──
def _require_evaluator_module():
    try:
        return importlib.import_module(_WS11_MODULE)
    except ModuleNotFoundError as exc:
        pytest.fail(
            f"WS11 BASE RED (D2/D3): approved pure evaluator module "
            f"'{_WS11_MODULE}' does not exist yet (GREEN not authorized/started): {exc}"
        )


def _require_evaluator_attr(name, decision):
    module = _require_evaluator_module()
    if not hasattr(module, name):
        pytest.fail(
            f"WS11 BASE RED ({decision}): approved public symbol "
            f"'{_WS11_MODULE}.{name}' is not exposed yet."
        )
    return getattr(module, name)


def _require_served_question_producer():
    import engine.path_n_questions as path_n_questions
    fn = getattr(path_n_questions, "get_served_question", None)
    if fn is None:
        pytest.fail(
            "WS11 BASE RED (D4.1): approved atomic served-question producer "
            "'engine.path_n_questions.get_served_question' does not exist yet."
        )
    return fn


def _require_served_question_type():
    import engine.path_n_questions as path_n_questions
    cls = getattr(path_n_questions, "ServedQuestion", None)
    if cls is None:
        pytest.fail(
            "WS11 BASE RED (D4.1): approved frozen value object "
            "'engine.path_n_questions.ServedQuestion' does not exist yet."
        )
    return cls


# ── Registry fixture helpers (reuse the merged WS10 loader; D13 injection) ──
def _write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    return path


def _source_obj():
    gaps = {g: [] for g in _CANONICAL_GAPS}
    for gap, qid, text in _SOURCE_QUESTIONS:
        gaps[gap].append({"question_id": qid, "text": text})
    return {
        "metadata": {"path": "Path N", "domain": "electronics_electrical",
                     "runtime_integrated": True},
        "gaps": gaps,
    }


def _record(qid, gap, sap):
    return {
        "question_id": qid,
        "intent_id": "QI-" + qid,
        "design_gap_id": gap,
        "primary_intent": f"design-time intent for {qid}",
        "answer_objective": f"a complete answer for {qid}",
        "completion_condition": f"observable completion for {qid}",
        "source_reference": {"artifact_path": sap, "question_id": qid},
    }


def _registry_obj(sap):
    gap_of = {qid: gap for (gap, qid, _t) in _SOURCE_QUESTIONS}
    order = [qid for (_g, qid, _t) in _SOURCE_QUESTIONS]
    return {
        "metadata": {
            "schema_version": "1.0.0", "registry_version": "1.0.0",
            "owner": "InventorAI Owner", "source_artifact": sap,
            "review_date": "2026-07-24", "stage": 2, "language": "en",
        },
        "records": [_record(qid, gap_of[qid], sap) for qid in order],
    }


def _build_registry(tmp_path):
    """Build a valid, injected QuestionIntentRegistry via the merged WS10 loader."""
    src = _write_json(tmp_path / "source.json", _source_obj())
    reg = _write_json(tmp_path / "registry.json", _registry_obj(str(src)))
    registry = load_question_intent_registry(reg, src)
    assert isinstance(registry, QuestionIntentRegistry)
    return registry


# ── 1. ServedQuestion is frozen and binds id/text/gap atomically (D4.1) ──
def test_served_question_is_frozen_and_binds_id_text_gap_atomically():
    import dataclasses
    produce = _require_served_question_producer()
    ServedQuestion = _require_served_question_type()
    served = produce(_KNOWN_GAP, 0)
    assert isinstance(served, ServedQuestion)
    assert dataclasses.is_dataclass(ServedQuestion)
    params = getattr(ServedQuestion, "__dataclass_params__", None)
    assert params is not None and params.frozen is True, "ServedQuestion must be frozen (D4.1)."
    for field in ("question_id", "text", "design_gap_id"):
        assert hasattr(served, field), f"ServedQuestion must carry '{field}' (D4.1)."
    assert served.design_gap_id in _CANONICAL_GAPS
    # Atomic binding: identity/text/gap all describe the same committed entry.
    assert served.question_id and served.text and served.design_gap_id


# ── 2. Backward-compatible text wrapper returns the same served text (D4.3) ──
def test_backward_compatible_text_wrapper_returns_same_served_text():
    import engine.path_n_questions as path_n_questions
    produce = _require_served_question_producer()
    for gap in _CANONICAL_GAPS:
        for iterations_open in (0, 1):
            served = produce(gap, iterations_open)
            legacy_text = path_n_questions.get_path_n_question(gap, iterations_open)
            assert served.text == legacy_text, (
                "get_path_n_question must remain a backward-compatible wrapper "
                "returning ServedQuestion.text for the same inputs (D4.3)."
            )


# ── 3. question_id cannot be recovered from question text (D4.4) ──
def test_question_id_cannot_be_recovered_from_text():
    import engine.path_n_questions as path_n_questions
    produce = _require_served_question_producer()
    # The only valid identity source is the ServedQuestion produced in one read;
    # the serving module must expose no text -> question_id recovery path.
    leaked = [n for n in _FORBIDDEN_REVERSE_LOOKUP_NAMES if hasattr(path_n_questions, n)]
    assert not leaked, (
        f"engine.path_n_questions must expose no text->question_id recovery API "
        f"(D4.4); found {leaked}."
    )
    served = produce(_KNOWN_GAP, 0)
    assert served.question_id, "question_id must be carried atomically, not derived from text (D4.4)."


# ── 4. Same ServedQuestion instance supplies evaluation identity and gap (D3/D4.2) ──
def test_same_served_question_supplies_identity_and_gap(tmp_path):
    produce = _require_served_question_producer()
    evaluate = _require_evaluator_attr("evaluate_question_intent", "D3 seam")
    registry = _build_registry(tmp_path)
    served = produce(_KNOWN_GAP, 0)
    # Identity and gap for the evaluator MUST come from the same ServedQuestion.
    result = evaluate(
        question_id=served.question_id,
        base_quality=_DEMONSTRATED,
        served_design_gap_id=served.design_gap_id,
        registry=registry,
    )
    assert result.question_id == served.question_id
    assert result.design_gap_id == served.design_gap_id


# ── 5–7. Structural tier -> outcome mapping (D7.1) ──
@pytest.mark.parametrize(
    "base_quality,expected_outcome",
    [
        (_DEMONSTRATED, _SATISFIED),
        (_REASONED, _PARTIALLY_SATISFIED),
        (_ASSERTED, _NOT_SATISFIED),
    ],
)
def test_tier_maps_to_outcome(tmp_path, base_quality, expected_outcome):
    assert _TIER_TO_OUTCOME[base_quality] == expected_outcome  # guards the fixture
    evaluate = _require_evaluator_attr("evaluate_question_intent", "D7.1 tier mapping")
    registry = _build_registry(tmp_path)
    result = evaluate(
        question_id=_KNOWN_QID,
        base_quality=base_quality,
        served_design_gap_id=_KNOWN_GAP,
        registry=registry,
    )
    assert result.base_quality == base_quality
    assert result.outcome == expected_outcome, (
        f"WS11 D7.1: base_quality {base_quality} must map to {expected_outcome}."
    )


# ── 8. Unknown question_id fails loud (D9; reuse WS10 typed error) ──
def test_unknown_question_id_fails_loud(tmp_path):
    evaluate = _require_evaluator_attr("evaluate_question_intent", "D9 unknown id")
    registry = _build_registry(tmp_path)
    with pytest.raises(QuestionIntentNotFoundError):
        evaluate(
            question_id="N-XX-DOES-NOT-EXIST",
            base_quality=_DEMONSTRATED,
            served_design_gap_id=_KNOWN_GAP,
            registry=registry,
        )


# ── 9. Question/design-gap mismatch -> typed failure (D7.1/D9) ──
def test_design_gap_mismatch_yields_typed_failure(tmp_path):
    evaluate = _require_evaluator_attr("evaluate_question_intent", "D9 design-gap mismatch")
    error_cls = _require_evaluator_attr("QuestionIntentEvaluationError", "D9 typed error")
    registry = _build_registry(tmp_path)
    with pytest.raises(error_cls) as exc_info:
        evaluate(
            question_id=_KNOWN_QID,               # record gap is MECHANISM_COMPLETENESS
            base_quality=_DEMONSTRATED,
            served_design_gap_id="PHYSICAL_FEASIBILITY",  # mismatched served gap
            registry=registry,
        )
    assert getattr(exc_info.value, "reason_code", None) == _DESIGN_GAP_MISMATCH


# ── 10. Missing authentic identity fails loud (D9/D10) ──
def test_missing_authentic_identity_fails_loud(tmp_path):
    evaluate = _require_evaluator_attr("evaluate_question_intent", "D10 missing identity")
    error_cls = _require_evaluator_attr("QuestionIntentEvaluationError", "D10 typed error")
    registry = _build_registry(tmp_path)
    with pytest.raises(error_cls) as exc_info:
        evaluate(
            question_id="",                       # no authentic identity
            base_quality=_DEMONSTRATED,
            served_design_gap_id=_KNOWN_GAP,
            registry=registry,
        )
    assert getattr(exc_info.value, "reason_code", None) == _MISSING_ACTIVE_QUESTION_ID


# ── 11. Invalid base quality fails deterministically (D7.1/D9) ──
def test_invalid_base_quality_fails_deterministically(tmp_path):
    evaluate = _require_evaluator_attr("evaluate_question_intent", "D9 invalid base quality")
    error_cls = _require_evaluator_attr("QuestionIntentEvaluationError", "D9 typed error")
    registry = _build_registry(tmp_path)
    with pytest.raises(error_cls) as exc_info:
        evaluate(
            question_id=_KNOWN_QID,
            base_quality="EXCELLENT",             # not an approved tier
            served_design_gap_id=_KNOWN_GAP,
            registry=registry,
        )
    assert getattr(exc_info.value, "reason_code", None) == _INVALID_BASE_QUALITY


# ── 12. No content-intent alignment claim is exposed (D7.1.T/D14.T) ──
def test_no_content_intent_alignment_claim_exposed(tmp_path):
    evaluate = _require_evaluator_attr("evaluate_question_intent", "D7.1.T/D14.T truthful boundary")
    registry = _build_registry(tmp_path)
    result = evaluate(
        question_id=_KNOWN_QID,
        base_quality=_DEMONSTRATED,
        served_design_gap_id=_KNOWN_GAP,
        registry=registry,
    )
    import dataclasses
    field_names = {f.name for f in dataclasses.fields(type(result))}
    assert _APPROVED_RESULT_FIELDS <= field_names, (
        f"WS11 D6: result must expose the approved fields {sorted(_APPROVED_RESULT_FIELDS)}; "
        f"got {sorted(field_names)}."
    )
    # v1 is structural only: objective tuples stay empty and no content verdict exists.
    assert tuple(result.matched_objectives) == (), "matched_objectives must be empty in v1 (D7.2 deferred)."
    assert tuple(result.unmet_objectives) == (), "unmet_objectives must be empty in v1 (D7.2 deferred)."
    for banned in ("content_alignment", "objective_fulfilled", "semantically_satisfied",
                   "answer_objective_met", "completion_condition_met"):
        assert not hasattr(result, banned), (
            f"WS11 v1 must expose no content-intent alignment claim; found '{banned}' (D14.T)."
        )


# ── 13. Evaluation is observation-only — no state/evidence/transition change (D1/D8/D14) ──
def test_evaluation_is_observation_only(tmp_path):
    from engine.idea_state import IdeaState
    from engine.progression_loop import evaluate_transition
    evaluate = _require_evaluator_attr("evaluate_question_intent", "D1/D8/D14 observation-only")
    registry = _build_registry(tmp_path)
    state = IdeaState(idea_id="ws11-observation-only")
    gaps_before = [(g.gap_type, g.status, g.iterations_open) for g in state.gaps]
    transition_before = evaluate_transition(state)
    evaluate(
        question_id=_KNOWN_QID,
        base_quality=_DEMONSTRATED,
        served_design_gap_id=_KNOWN_GAP,
        registry=registry,
    )
    gaps_after = [(g.gap_type, g.status, g.iterations_open) for g in state.gaps]
    assert gaps_after == gaps_before, "WS11 evaluation must not mutate gaps/Evidence/IdeaState (D14)."
    assert evaluate_transition(state) == transition_before, (
        "WS11 evaluation must not change evaluate_transition (D8)."
    )


# ── 14. Registry is injected and no registry file I/O occurs (D3/D13) ──
def test_registry_is_injected_and_no_registry_file_io(tmp_path):
    import sys
    evaluate = _require_evaluator_attr("evaluate_question_intent", "D3/D13 injection + no I/O")
    registry = _build_registry(tmp_path)
    opened = []
    recording = {"on": False}

    def _hook(event, args):
        if recording["on"] and event == "open" and args and args[0] is not None:
            opened.append(str(args[0]))

    sys.addaudithook(_hook)
    recording["on"] = True
    try:
        evaluate(
            question_id=_KNOWN_QID,
            base_quality=_DEMONSTRATED,
            served_design_gap_id=_KNOWN_GAP,
            registry=registry,
        )
    finally:
        recording["on"] = False
    bad = [p for p in opened if p.endswith(".json")
           and ("registry" in p or "electronics_electrical_path_n_questions" in p)]
    assert not bad, (
        f"WS11 evaluate_question_intent must consume the injected registry and perform "
        f"no registry/artifact file I/O (D3/D13); opened {bad}."
    )


# ── 15. Legacy non-WS11 behavior remains unchanged (D10) ──
def test_legacy_non_ws11_behavior_unchanged(tmp_path):
    import engine.path_n_questions as path_n_questions
    # Introducing the WS11 seam must not change the legacy text-serving contract.
    produce = _require_served_question_producer()
    served = produce(_KNOWN_GAP, 0)
    legacy_text = path_n_questions.get_path_n_question(_KNOWN_GAP, 0)
    assert isinstance(legacy_text, str) and legacy_text.strip()
    assert served.text == legacy_text, (
        "Legacy get_path_n_question output must be unchanged and equal to "
        "ServedQuestion.text (D4.3/D10)."
    )
