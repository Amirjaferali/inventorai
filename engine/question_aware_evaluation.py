"""engine/question_aware_evaluation.py — Workstream 11 Question-Aware Evaluation GREEN.

Scope (owner-authorized WS11 GREEN, minimal):
    Implement the ratified WS11 v1 evaluator that satisfies the merged BASE RED
    contract (docs/governance/WORKSTREAM_11_QUESTION_AWARE_EVALUATION_OWNER_DECISIONS.md;
    tests/test_workstream_11_question_aware_evaluation_base_red.py).

    WS11 v1 is a **deterministic, question-bound STRUCTURAL evaluation observation**
    (D1/D7.1). It is NOT semantic answer evaluation:

      * `outcome` is a deterministic function of the existing, unchanged
        `assess_response` quality tier alone (D7.1) —
        DEMONSTRATED→SATISFIED, REASONED→PARTIALLY_SATISFIED, ASSERTED→NOT_SATISFIED;
      * a `SATISFIED` result means ONLY that the generic quality tier reached
        DEMONSTRATED for an authentic identified question — it does NOT prove
        semantic fulfilment of `answer_objective` or `completion_condition`
        (D7.1.T); `primary_intent`/`answer_objective`/`completion_condition` are
        audit-carried metadata only and never influence the outcome, and no
        content-intent alignment claim is produced (D14.T);
      * content-level matching against free-text intent is deferred and blocked;
        no AI, LLM, embeddings, keyword approximation, or language-specific
        fallback is used (D7.2/D15).

    The evaluator is a pure function: it consumes the already-loaded WS10
    `QuestionIntentRegistry` through dependency injection, performs no file/registry
    I/O, adds no caching, and mutates no IdeaState/Evidence/gap/transition/scoring/
    registry state (D3/D13/D14). It never returns a fallback, partial-success, or
    fabricated result (D9/D30); every identity/integrity failure is a typed,
    fail-loud error.
"""

from __future__ import annotations

from dataclasses import dataclass

from engine.question_intent_registry import QuestionIntentRegistry

# Approved deterministic quality tiers (the existing assess_response tiers, F2).
_DEMONSTRATED = "DEMONSTRATED"
_REASONED = "REASONED"
_ASSERTED = "ASSERTED"

# Approved D7.1 structural outcome vocabulary.
_SATISFIED = "SATISFIED"
_PARTIALLY_SATISFIED = "PARTIALLY_SATISFIED"
_NOT_SATISFIED = "NOT_SATISFIED"

# Approved deterministic tier -> outcome mapping (D7.1). This is the only
# determinant of `outcome`; free-text intent content is never consulted.
_TIER_TO_OUTCOME = {
    _DEMONSTRATED: _SATISFIED,
    _REASONED: _PARTIALLY_SATISFIED,
    _ASSERTED: _NOT_SATISFIED,
}

# Approved D9 typed failure reason codes for WS11 integrity/identity failures.
_MISSING_ACTIVE_QUESTION_ID = "MISSING_ACTIVE_QUESTION_ID"
_INVALID_BASE_QUALITY = "INVALID_BASE_QUALITY"
_DESIGN_GAP_MISMATCH = "DESIGN_GAP_MISMATCH"


class QuestionIntentEvaluationError(Exception):
    """Raised for a WS11 identity/integrity failure (D9).

    Exposes a stable ``reason_code`` drawn only from the approved WS11 failure
    codes. An unknown ``question_id`` is surfaced through the WS10
    ``QuestionIntentNotFoundError`` raised by ``registry.get`` (D9), not this type."""

    reason_code: str

    def __init__(self, message: str, *, reason_code: str) -> None:
        super().__init__(message)
        self.reason_code = reason_code


@dataclass(frozen=True)
class QuestionIntentEvaluation:
    """Immutable, auditable WS11 v1 structural observation (D6).

    `outcome` is the structural tier mapping (D7.1); it is NOT a semantic
    content verdict. `matched_objectives`/`unmet_objectives` are reserved for the
    deferred content layer (D7.2) and are always empty in v1. No free-form or
    model-generated text is carried."""

    question_id: str
    intent_id: str
    design_gap_id: str
    base_quality: str
    outcome: str
    matched_objectives: tuple[str, ...] = ()
    unmet_objectives: tuple[str, ...] = ()
    reason_code: str | None = None


def evaluate_question_intent(
    question_id: str,
    base_quality: str,
    served_design_gap_id: str,
    registry: QuestionIntentRegistry,
) -> QuestionIntentEvaluation:
    """Produce the deterministic WS11 v1 question-bound structural observation (D3).

    Args:
        question_id: the authentic committed question identity (from the same
            immutable ServedQuestion that supplied the served text/gap, D4.2).
        base_quality: the existing, unchanged assess_response tier
            (ASSERTED | REASONED | DEMONSTRATED).
        served_design_gap_id: the design-gap under which the question was served,
            sourced from the same ServedQuestion instance (D4.2).
        registry: the already-loaded WS10 QuestionIntentRegistry (dependency
            injection; no file I/O, no second truth source — D13).

    Returns an immutable :class:`QuestionIntentEvaluation`. Raises fail-loud, typed
    errors for every identity/integrity failure; never returns a fallback,
    partial-success, or fabricated result (D9/D30)."""
    if not isinstance(question_id, str) or not question_id.strip():
        raise QuestionIntentEvaluationError(
            "WS11: missing authentic active question_id",
            reason_code=_MISSING_ACTIVE_QUESTION_ID,
        )
    if base_quality not in _TIER_TO_OUTCOME:
        raise QuestionIntentEvaluationError(
            f"WS11: base_quality {base_quality!r} is not an approved quality tier",
            reason_code=_INVALID_BASE_QUALITY,
        )

    # Unknown question_id fails loud through the WS10 registry (QuestionIntentNotFoundError).
    record = registry.get(question_id)

    if served_design_gap_id != record.design_gap_id:
        raise QuestionIntentEvaluationError(
            f"WS11: served design_gap_id {served_design_gap_id!r} does not match the "
            f"committed design_gap_id {record.design_gap_id!r} for question "
            f"{question_id!r}",
            reason_code=_DESIGN_GAP_MISMATCH,
        )

    return QuestionIntentEvaluation(
        question_id=record.question_id,
        intent_id=record.intent_id,
        design_gap_id=record.design_gap_id,
        base_quality=base_quality,
        outcome=_TIER_TO_OUTCOME[base_quality],
        matched_objectives=(),
        unmet_objectives=(),
        reason_code=None,
    )
