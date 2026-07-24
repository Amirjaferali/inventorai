"""engine/question_intent_registry.py — Workstream 10 Minimal Interface GREEN.

Scope (owner-authorized Minimal Interface GREEN, D32):
    Introduce ONLY the approved D18–D33 public interface so the six merged
    Interface-Contract BASE RED tests pass. This is the *interface* skeleton, not
    the behavioral loader:

      * the public types exist as immutable (frozen) dataclasses with the exact
        approved fields (D3/D8/D21);
      * the registry public API is read-only — `get` / `list_records` only, no
        mutation (D20);
      * the two approved exception types exist, and the load error exposes a
        stable `reason_code` (D22/D26);
      * `load_question_intent_registry` has the exact explicit two-Path signature
        (D19/D24) and FAILS LOUD as a bounded placeholder — successful registry
        loading, JSON parsing, and all structural/behavioral validation are
        deliberately NOT implemented in this gate (D32).

    No registry loading or file I/O occurs at import time; there is no module-level
    or global cache (D19/D25).

Explicitly NOT implemented in this gate (D32/prohibitions): registry JSON, schema,
successful valid-registry loading, JSON parsing behavior, structural/metadata/
source-reference/source-ID-set validation, duplicate detection, `design_gap_id`
validation, `_STALL_REFRAME` exclusion, source-artifact ordering, behavioral
no-fallback validation, runtime/Path N integration, persistence, or WS11 behavior.

`QuestionIntentSourceReference` is the faithful immutable encoding of the approved
`source_reference` shape (D6: `{artifact_path, question_id}`, referenced in the
merged decisions as `source_reference.question_id`); it types the approved
`source_reference` field and adds no record field.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# Bounded placeholder reason_code for the Minimal Interface gate. It is distinct
# from the D26 behavioral reason codes and implements no behavioral-validation
# reason-code coverage; it exists only so the placeholder loader can fail loud
# with a stable code (this gate's owner authorization).
_MINIMAL_INTERFACE_PLACEHOLDER_REASON_CODE = "MINIMAL_INTERFACE_PLACEHOLDER"


class QuestionIntentRegistryLoadError(Exception):
    """Raised for any registry read/parse/validation failure (D22/D30).

    Exposes a stable ``reason_code`` (D26). In this Minimal Interface gate the
    only reason_code used is the bounded placeholder; the D26 behavioral reason
    codes are introduced by the later Behavioral Validation gate."""

    reason_code: str

    def __init__(self, message: str, *, reason_code: str) -> None:
        super().__init__(message)
        self.reason_code = reason_code


class QuestionIntentNotFoundError(Exception):
    """Raised only by ``QuestionIntentRegistry.get`` for an unknown committed
    question_id (D22/D23)."""

    def __init__(self, question_id: str) -> None:
        super().__init__(
            f"question_id {question_id!r} is not present in the question intent registry"
        )
        self.question_id = question_id


@dataclass(frozen=True)
class QuestionIntentSourceReference:
    """Immutable encoding of the approved `source_reference` shape (D6)."""

    artifact_path: str
    question_id: str


@dataclass(frozen=True)
class QuestionIntentRecord:
    """Immutable design-time intent record — exact approved v1 fields (D3)."""

    question_id: str
    intent_id: str
    design_gap_id: str
    primary_intent: str
    answer_objective: str
    completion_condition: str
    source_reference: QuestionIntentSourceReference


@dataclass(frozen=True)
class QuestionIntentRegistryMetadata:
    """Immutable registry metadata — exact approved v1 fields (D8)."""

    schema_version: str
    registry_version: str
    owner: str
    source_artifact: str
    review_date: str
    stage: int
    language: str


@dataclass(frozen=True)
class QuestionIntentRegistry:
    """Immutable registry with a read-only public API (D20/D21).

    Public surface is exactly ``get`` and ``list_records``; the stored metadata
    and records are private and immutable (a tuple, never a mutable collection).
    Instances are produced only by ``load_question_intent_registry`` — which is a
    fail-loud placeholder in this gate — so no populated registry is constructed
    here."""

    _metadata: QuestionIntentRegistryMetadata | None = None
    _records: tuple[QuestionIntentRecord, ...] = ()

    def get(self, question_id: str) -> QuestionIntentRecord:
        for record in self._records:
            if record.question_id == question_id:
                return record
        raise QuestionIntentNotFoundError(question_id)

    def list_records(self) -> tuple[QuestionIntentRecord, ...]:
        return tuple(self._records)


def load_question_intent_registry(
    registry_path: Path,
    source_artifact_path: Path,
) -> QuestionIntentRegistry:
    """Load the governed question intent registry (D19).

    Minimal Interface GREEN (D32): this is a bounded fail-loud placeholder.
    Successful registry loading, JSON parsing, and all validation are NOT part of
    this gate, so the function raises immediately with a stable placeholder
    ``reason_code`` and performs no file I/O. It never returns an empty registry,
    fabricated records, or fallback data."""
    raise QuestionIntentRegistryLoadError(
        "WS10 Minimal Interface GREEN: successful question intent registry loading "
        "is not implemented in this gate; the behavioral loader is a separately "
        "authorized later gate.",
        reason_code=_MINIMAL_INTERFACE_PLACEHOLDER_REASON_CODE,
    )
