"""engine/question_intent_registry.py — Workstream 10 Behavioral GREEN.

Scope (owner-authorized Behavioral GREEN, D33):
    Implement the real behavioral loader that satisfies the merged Behavioral
    Validation BASE RED tests, using only the ratified WS10 decisions
    (D1–D17 record shape; D18–D33 loader interface and validation contract).

    The public interface established by Minimal Interface GREEN is preserved
    exactly (D18–D22):
      * the public types are immutable (frozen) dataclasses with the approved
        fields (D3/D8/D21);
      * the registry public API is read-only — `get` / `list_records` (D20);
      * the two approved exception types exist, and the load error exposes a
        stable `reason_code` drawn only from the approved D26 taxonomy (D22/D26);
      * `load_question_intent_registry` has the exact explicit two-Path signature
        (D19/D24) and performs no registry I/O at import time (D19/D25).

    The Minimal Interface fail-loud placeholder behavior is fully replaced — not
    shadowed — by the real loader below. There is no hidden placeholder path and
    no fallback: every read/parse/structural/metadata/
    record/source-reference/source-ID-set failure raises
    `QuestionIntentRegistryLoadError` with an approved reason_code, and no empty,
    partial, default, or fabricated registry is ever returned (D14/D30).

Validation (all during `load_question_intent_registry`, D23):
    1. read + JSON-parse the registry file       (FILE_READ_ERROR / INVALID_JSON)
    2. read + JSON-parse the source artifact      (FILE_READ_ERROR / INVALID_JSON)
    3. extract the source question-ID order,
       excluding `_STALL_REFRAME` (D15)           (INVALID_SOURCE_ARTIFACT_PATH)
    4. validate the {metadata, records} shape and
       the approved metadata fields (D8/D28)      (INVALID_METADATA)
    5. per record: required fields (D3),
       canonical design_gap_id (D5), and
       source_reference consistency (D6)          (MISSING_REQUIRED_FIELD /
                                                    INVALID_DESIGN_GAP_ID /
                                                    SOURCE_REFERENCE_MISMATCH)
    6. reject duplicate question_id / intent_id    (DUPLICATE_QUESTION_ID /
                                                    DUPLICATE_INTENT_ID)
    7. require exact source/registry ID-set
       equality (D11)                             (SOURCE_ID_SET_MISMATCH)
    8. return an immutable registry with records
       in committed source-artifact order (D29).

    Unknown-ID lookup fails at `QuestionIntentRegistry.get` (D22/D23).

Only the Python standard library is used for parsing and validation; no schema
dependency and no JSON Schema artifact are introduced (D27). The loader adds no
caching, persistence, database, runtime, network, UI, or prompt/AI behavior.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

# Approved D26 reason-code taxonomy (the only ratified codes). This module
# introduces no new reason codes.
_FILE_READ_ERROR = "FILE_READ_ERROR"
_INVALID_JSON = "INVALID_JSON"
_INVALID_SOURCE_ARTIFACT_PATH = "INVALID_SOURCE_ARTIFACT_PATH"
_INVALID_METADATA = "INVALID_METADATA"
_MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
_INVALID_DESIGN_GAP_ID = "INVALID_DESIGN_GAP_ID"
_SOURCE_REFERENCE_MISMATCH = "SOURCE_REFERENCE_MISMATCH"
_DUPLICATE_QUESTION_ID = "DUPLICATE_QUESTION_ID"
_DUPLICATE_INTENT_ID = "DUPLICATE_INTENT_ID"
_SOURCE_ID_SET_MISMATCH = "SOURCE_ID_SET_MISMATCH"

# Canonical design gaps (D5) — no aliases in v1.
_CANONICAL_DESIGN_GAP_IDS = frozenset(
    {"MECHANISM_COMPLETENESS", "PHYSICAL_FEASIBILITY", "BOUNDARY_AMBIGUITY"}
)

# Required v1 record fields (D3), in approved order.
_REQUIRED_RECORD_FIELDS = (
    "question_id",
    "intent_id",
    "design_gap_id",
    "primary_intent",
    "answer_objective",
    "completion_condition",
    "source_reference",
)

# Record fields that must be present, non-empty strings (D3; D33 item 15 — the
# semantic fields are required as non-empty strings, with no automated
# semantic-quality judgment). `source_reference` is a structured field, checked
# separately (D6).
_REQUIRED_STRING_RECORD_FIELDS = (
    "question_id",
    "intent_id",
    "design_gap_id",
    "primary_intent",
    "answer_objective",
    "completion_condition",
)

# Required registry metadata fields (D8).
_REQUIRED_METADATA_FIELDS = (
    "schema_version",
    "registry_version",
    "owner",
    "source_artifact",
    "review_date",
    "stage",
    "language",
)

# Non-artifact display substitution — excluded entirely from the v1 registry and
# from the approved source-question set (D15).
_STALL_REFRAME_ID = "_STALL_REFRAME"


class QuestionIntentRegistryLoadError(Exception):
    """Raised for any registry read/parse/validation failure (D22/D30).

    Exposes a stable ``reason_code`` drawn only from the approved D26 taxonomy;
    tests assert the exception type and this code, not human-readable text."""

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
    Instances are produced only by ``load_question_intent_registry``."""

    _metadata: QuestionIntentRegistryMetadata | None = None
    _records: tuple[QuestionIntentRecord, ...] = ()

    def get(self, question_id: str) -> QuestionIntentRecord:
        for record in self._records:
            if record.question_id == question_id:
                return record
        raise QuestionIntentNotFoundError(question_id)

    def list_records(self) -> tuple[QuestionIntentRecord, ...]:
        return tuple(self._records)


def _read_json(path: Path, *, kind: str):
    """Read and JSON-parse a file, failing loud with an approved reason_code."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise QuestionIntentRegistryLoadError(
            f"unable to read {kind} file {str(path)!r}: {exc}",
            reason_code=_FILE_READ_ERROR,
        ) from exc
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise QuestionIntentRegistryLoadError(
            f"{kind} file {str(path)!r} is not valid JSON: {exc}",
            reason_code=_INVALID_JSON,
        ) from exc


def _extract_source_question_ids(source_data) -> list[str]:
    """Return the committed source question IDs in source-artifact order (D29),
    excluding `_STALL_REFRAME` (D15). Rejects a structurally invalid source
    artifact with INVALID_SOURCE_ARTIFACT_PATH (D14)."""
    if not isinstance(source_data, dict):
        raise QuestionIntentRegistryLoadError(
            "source artifact top-level is not a JSON object",
            reason_code=_INVALID_SOURCE_ARTIFACT_PATH,
        )
    gaps = source_data.get("gaps")
    if not isinstance(gaps, dict) or not gaps:
        raise QuestionIntentRegistryLoadError(
            "source artifact has no valid 'gaps' mapping",
            reason_code=_INVALID_SOURCE_ARTIFACT_PATH,
        )
    ids: list[str] = []
    for questions in gaps.values():
        if not isinstance(questions, list):
            raise QuestionIntentRegistryLoadError(
                "source artifact gap group is not a list",
                reason_code=_INVALID_SOURCE_ARTIFACT_PATH,
            )
        for question in questions:
            if not isinstance(question, dict) or "question_id" not in question:
                raise QuestionIntentRegistryLoadError(
                    "source artifact question entry is missing 'question_id'",
                    reason_code=_INVALID_SOURCE_ARTIFACT_PATH,
                )
            question_id = question["question_id"]
            if question_id == _STALL_REFRAME_ID:
                continue
            ids.append(question_id)
    if not ids:
        raise QuestionIntentRegistryLoadError(
            "source artifact contains no committed questions",
            reason_code=_INVALID_SOURCE_ARTIFACT_PATH,
        )
    return ids


def _validate_metadata(
    registry_data, source_artifact: str
) -> QuestionIntentRegistryMetadata:
    """Validate the {metadata, records} top-level shape and the approved
    metadata fields (D8/D28); fail with INVALID_METADATA on any violation."""
    if not isinstance(registry_data, dict):
        raise QuestionIntentRegistryLoadError(
            "registry top-level is not a JSON object",
            reason_code=_INVALID_METADATA,
        )
    metadata = registry_data.get("metadata")
    if not isinstance(metadata, dict):
        raise QuestionIntentRegistryLoadError(
            "registry is missing a valid top-level 'metadata' object",
            reason_code=_INVALID_METADATA,
        )
    for field in _REQUIRED_METADATA_FIELDS:
        if field not in metadata:
            raise QuestionIntentRegistryLoadError(
                f"registry metadata is missing required field {field!r}",
                reason_code=_INVALID_METADATA,
            )
    if metadata["source_artifact"] != source_artifact:
        raise QuestionIntentRegistryLoadError(
            "registry metadata 'source_artifact' does not match the provided "
            "source artifact path",
            reason_code=_INVALID_METADATA,
        )
    return QuestionIntentRegistryMetadata(
        schema_version=metadata["schema_version"],
        registry_version=metadata["registry_version"],
        owner=metadata["owner"],
        source_artifact=metadata["source_artifact"],
        review_date=metadata["review_date"],
        stage=metadata["stage"],
        language=metadata["language"],
    )


def _reject_duplicates(values: list[str], *, reason_code: str, label: str) -> None:
    seen: set[str] = set()
    for value in values:
        if value in seen:
            raise QuestionIntentRegistryLoadError(
                f"duplicate {label} {value!r} in registry records",
                reason_code=reason_code,
            )
        seen.add(value)


def _validate_records(registry_data, source_artifact: str) -> list[dict]:
    """Validate the registry records list: required fields (D3), canonical
    design_gap_id (D5), source_reference consistency (D6), and duplicate
    question_id / intent_id rejection (D11). Returns the raw record dicts."""
    records = registry_data.get("records")
    if not isinstance(records, list):
        raise QuestionIntentRegistryLoadError(
            "registry is missing a valid top-level 'records' list",
            reason_code=_MISSING_REQUIRED_FIELD,
        )

    for record in records:
        if not isinstance(record, dict):
            raise QuestionIntentRegistryLoadError(
                "registry record is not a JSON object",
                reason_code=_MISSING_REQUIRED_FIELD,
            )
        for field in _REQUIRED_RECORD_FIELDS:
            if field not in record:
                raise QuestionIntentRegistryLoadError(
                    f"registry record is missing required field {field!r}",
                    reason_code=_MISSING_REQUIRED_FIELD,
                )
        for field in _REQUIRED_STRING_RECORD_FIELDS:
            value = record[field]
            if not isinstance(value, str) or not value:
                raise QuestionIntentRegistryLoadError(
                    f"registry record field {field!r} must be a non-empty string",
                    reason_code=_MISSING_REQUIRED_FIELD,
                )

        if record["design_gap_id"] not in _CANONICAL_DESIGN_GAP_IDS:
            raise QuestionIntentRegistryLoadError(
                f"registry record {record['question_id']!r} has non-canonical "
                f"design_gap_id {record['design_gap_id']!r}",
                reason_code=_INVALID_DESIGN_GAP_ID,
            )

        source_reference = record["source_reference"]
        if (
            not isinstance(source_reference, dict)
            or "artifact_path" not in source_reference
            or "question_id" not in source_reference
        ):
            raise QuestionIntentRegistryLoadError(
                f"registry record {record['question_id']!r} has a malformed "
                f"source_reference",
                reason_code=_SOURCE_REFERENCE_MISMATCH,
            )
        if source_reference["question_id"] != record["question_id"]:
            raise QuestionIntentRegistryLoadError(
                f"registry record {record['question_id']!r} source_reference."
                f"question_id does not equal the record question_id",
                reason_code=_SOURCE_REFERENCE_MISMATCH,
            )
        if source_reference["artifact_path"] != source_artifact:
            raise QuestionIntentRegistryLoadError(
                f"registry record {record['question_id']!r} source_reference."
                f"artifact_path does not match the approved source artifact path",
                reason_code=_SOURCE_REFERENCE_MISMATCH,
            )

    _reject_duplicates(
        [record["question_id"] for record in records],
        reason_code=_DUPLICATE_QUESTION_ID,
        label="question_id",
    )
    _reject_duplicates(
        [record["intent_id"] for record in records],
        reason_code=_DUPLICATE_INTENT_ID,
        label="intent_id",
    )
    return records


def load_question_intent_registry(
    registry_path: Path,
    source_artifact_path: Path,
) -> QuestionIntentRegistry:
    """Load and validate the governed question intent registry (D19).

    Reads both explicitly-provided paths, validates the registry against the
    ratified WS10 contract and the committed source artifact, and returns an
    immutable :class:`QuestionIntentRegistry` whose records are ordered by the
    committed source-artifact order (D29). Any failure raises
    :class:`QuestionIntentRegistryLoadError` with an approved D26 reason_code;
    no empty, partial, default, or fabricated registry is ever returned
    (D14/D30). No registry I/O occurs at import time (D19/D25)."""
    source_artifact = str(source_artifact_path)

    registry_data = _read_json(registry_path, kind="registry")
    source_data = _read_json(source_artifact_path, kind="source artifact")

    source_ids = _extract_source_question_ids(source_data)

    metadata = _validate_metadata(registry_data, source_artifact)
    records = _validate_records(registry_data, source_artifact)

    registry_ids = {record["question_id"] for record in records}
    if registry_ids != set(source_ids):
        raise QuestionIntentRegistryLoadError(
            "registry question-ID set does not exactly equal the committed "
            "source question-ID set",
            reason_code=_SOURCE_ID_SET_MISMATCH,
        )

    records_by_id = {record["question_id"]: record for record in records}
    ordered_records = tuple(
        QuestionIntentRecord(
            question_id=record["question_id"],
            intent_id=record["intent_id"],
            design_gap_id=record["design_gap_id"],
            primary_intent=record["primary_intent"],
            answer_objective=record["answer_objective"],
            completion_condition=record["completion_condition"],
            source_reference=QuestionIntentSourceReference(
                artifact_path=record["source_reference"]["artifact_path"],
                question_id=record["source_reference"]["question_id"],
            ),
        )
        for record in (records_by_id[question_id] for question_id in source_ids)
    )

    return QuestionIntentRegistry(_metadata=metadata, _records=ordered_records)
