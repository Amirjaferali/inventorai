"""
Controlled Unknown Progression — Workstream 12 v1 (observation-only).

Governed by (merged, authoritative):
    docs/governance/WORKSTREAM_12_CONTROLLED_UNKNOWN_PROGRESSION_INCREMENT_CONTRACT.md
        (ratified Owner Decisions OD-1 through OD-16).

Purpose:
    A pure, deterministic, AI-free, observation-only surface that classifies and
    reports controlled unknowns. It never mutates progression, maturity,
    readiness, gap status, closure state, the ledger, or criticality. It reuses
    the existing `AcknowledgedUnknown` and `AssertionRecord` records (OD-2) and
    introduces no third record system.

Boundaries (enforced here and by the merged BASE RED tests):
    * OD-3: the six proposed controlled-unknown PATH classifications below are a
      SEPARATE vocabulary from the existing `INTERACTION_DISPOSITIONS`; the two
      are never silently mapped, aliased, substituted, or auto-transitioned.
    * OD-1/OD-4/OD-5/OD-6: observation-only; blocker classification is
      report-only; criticality is read-only; closure is recommendation-only
      (no gap closure, no unknown resolution, no `resolves_gap=True`).
    * OD-6/OD-11: `ACCEPTED_RISK` is a `Gap.status` value, never a WS12 path; it
      is rejected loudly and never created/assigned/recommended by WS12.
    * OD-10: uniform sufficiency — no user-attribute inputs.
    * OD-12: in-memory, non-exporting (no persistence/export surface).
    * OD-13/OD-14/OD-15/OD-16: no D13, WS13, WS14, CAP-04/08/10 full behavior,
      or CAP-12/13/14 behavior.

This module imports only the standard library and the already-existing, merged
`engine.idea_state` surface. It performs no I/O and no network access.
"""

from dataclasses import dataclass
from typing import Optional

from engine.idea_state import (
    AcknowledgedUnknown,
    AssertionRecord,
    INTERACTION_DISPOSITIONS,
    ACCEPTED_RISK,
    DISPOSITION_ANSWERED,
)

# --- OD-3: the six proposed WS12 controlled-unknown PATH classifications ------
# A SEPARATE vocabulary from INTERACTION_DISPOSITIONS. These describe the path
# required to evaluate or manage a controlled unknown (never an interaction
# disposition, and never silently mapped to one).
NEEDS_EVIDENCE = "NEEDS_EVIDENCE"
NEEDS_MEASUREMENT = "NEEDS_MEASUREMENT"
NEEDS_TEST = "NEEDS_TEST"
NEEDS_SPECIALIST = "NEEDS_SPECIALIST"
DEFERRED_BY_USER = "DEFERRED_BY_USER"
OUT_OF_SCOPE = "OUT_OF_SCOPE"

WS12_UNKNOWN_PATH_CLASSIFICATIONS = frozenset({
    NEEDS_EVIDENCE, NEEDS_MEASUREMENT, NEEDS_TEST,
    NEEDS_SPECIALIST, DEFERRED_BY_USER, OUT_OF_SCOPE,
})

# --- Stable typed-error reason codes -----------------------------------------
_INVALID_PATH_CLASSIFICATION = "INVALID_PATH_CLASSIFICATION"
_CROSS_VOCABULARY_MAPPING_FORBIDDEN = "CROSS_VOCABULARY_MAPPING_FORBIDDEN"
_ACCEPTED_RISK_NOT_A_PATH = "ACCEPTED_RISK_NOT_A_PATH"
_UNSUPPORTED_RECORD_TYPE = "UNSUPPORTED_RECORD_TYPE"

# Source-kind labels for the two reused record families (OD-2).
_SOURCE_ACKNOWLEDGED_UNKNOWN = "acknowledged_unknown"
_SOURCE_ASSERTION_RECORD = "assertion_record"


class ControlledUnknownProgressionError(Exception):
    """Fail-loud typed error for WS12. Always carries a stable, non-empty
    `reason_code` (OD-3/OD-6 governed rejection)."""

    def __init__(self, message: str, *, reason_code: str) -> None:
        super().__init__(message)
        self.reason_code = reason_code


@dataclass(frozen=True)
class ControlledUnknownView:
    """A frozen, observation-only view over ONE existing unknown record.

    It records a controlled unknown's WS12 path classification and advisory
    attributes WITHOUT mutating anything. `resolves_gap` and
    `mutates_progression` are structurally always False: a WS12 view neither
    resolves a gap nor moves progression (OD-1/OD-4/OD-6). Deliberately carries
    NO user-attribute field (OD-10 uniform sufficiency)."""
    source_kind: str
    source_ref: Optional[str]
    gap_context: Optional[str]
    path_classification: Optional[str]
    blocking: bool = False
    criticality: Optional[str] = None
    safety_critical: bool = False
    closure_recommendation: Optional[str] = None
    resolves_gap: bool = False
    mutates_progression: bool = False


def _source_kind(record) -> str:
    """Reuse-only record typing (OD-2): the record must be one of the two
    existing families. No third record system is introduced."""
    if isinstance(record, AcknowledgedUnknown):
        return _SOURCE_ACKNOWLEDGED_UNKNOWN
    if isinstance(record, AssertionRecord):
        return _SOURCE_ASSERTION_RECORD
    raise ControlledUnknownProgressionError(
        f"unsupported unknown-record type: {type(record).__name__!r} "
        "(WS12 reuses AcknowledgedUnknown / AssertionRecord only)",
        reason_code=_UNSUPPORTED_RECORD_TYPE,
    )


def _require_valid_path(path) -> None:
    """Validate a WS12 path classification, rejecting — loudly and with a stable
    reason code — any INTERACTION_DISPOSITIONS value (OD-3 no silent mapping),
    the ACCEPTED_RISK gap-status value (OD-6), and any other invalid value."""
    if path in WS12_UNKNOWN_PATH_CLASSIFICATIONS:
        return
    if path == ACCEPTED_RISK:
        raise ControlledUnknownProgressionError(
            f"{path!r} is a Gap.status value, not a WS12 path classification; "
            "WS12 must never create, assign, infer, recommend, or transition to "
            "ACCEPTED_RISK (OD-6)",
            reason_code=_ACCEPTED_RISK_NOT_A_PATH,
        )
    if path in INTERACTION_DISPOSITIONS:
        raise ControlledUnknownProgressionError(
            f"{path!r} is an INTERACTION_DISPOSITIONS value and must not be "
            "silently mapped to a WS12 controlled-unknown path (OD-3)",
            reason_code=_CROSS_VOCABULARY_MAPPING_FORBIDDEN,
        )
    raise ControlledUnknownProgressionError(
        f"{path!r} is not a WS12 controlled-unknown path classification",
        reason_code=_INVALID_PATH_CLASSIFICATION,
    )


def classify_controlled_unknown(
    record,
    *,
    path,
    blocking: bool = False,
    safety_critical: bool = False,
    criticality: Optional[str] = None,
    closure_recommendation: Optional[str] = None,
) -> ControlledUnknownView:
    """Classify one existing unknown record into a WS12 path (observation-only).

    Pure and deterministic. It reads the record and returns a frozen view; it
    NEVER mutates the record, the owning IdeaState, gaps, maturity, the ledger,
    or criticality. `criticality` is echoed read-only (OD-5). `blocking` is
    reported, never acted upon (OD-4). `closure_recommendation` is advisory only
    and closes/resolves nothing; `resolves_gap` is always False (OD-6). Exposes
    NO user-attribute parameter (OD-10). Raises ControlledUnknownProgressionError
    for an invalid/cross-vocabulary/ACCEPTED_RISK path or an unsupported record
    type.
    """
    _require_valid_path(path)
    source_kind = _source_kind(record)
    return ControlledUnknownView(
        source_kind=source_kind,
        source_ref=getattr(record, "record_id", None),
        gap_context=getattr(record, "gap_context", None),
        path_classification=path,
        blocking=bool(blocking),
        criticality=criticality,
        safety_critical=bool(safety_critical),
        closure_recommendation=closure_recommendation,
        resolves_gap=False,
        mutates_progression=False,
    )


def report_controlled_unknowns(state) -> tuple:
    """Report every controlled unknown in an IdeaState as an observation-only
    view tuple (OD-1). Reads the existing `acknowledged_unknowns` track and every
    non-`answered` `AssertionRecord` (OD-2). Preserves multiplicity — multiple
    records sharing one gap_context are all reported, with NO automatic
    deduplication (OD-9) — and preserves history, including superseded records,
    with no silent overwrite (OD-8). Views produced here are unclassified
    (`path_classification` is None) until an explicit `classify_controlled_unknown`
    call assigns a path. Mutates nothing.
    """
    views = []
    for unknown in getattr(state, "acknowledged_unknowns", ()) or ():
        views.append(ControlledUnknownView(
            source_kind=_SOURCE_ACKNOWLEDGED_UNKNOWN,
            source_ref=getattr(unknown, "record_id", None),
            gap_context=getattr(unknown, "gap_context", None),
            path_classification=None,
        ))
    for record in getattr(state, "assertions", ()) or ():
        if getattr(record, "disposition", None) == DISPOSITION_ANSWERED:
            continue
        views.append(ControlledUnknownView(
            source_kind=_SOURCE_ASSERTION_RECORD,
            source_ref=getattr(record, "record_id", None),
            gap_context=getattr(record, "gap_context", None),
            path_classification=None,
        ))
    return tuple(views)
