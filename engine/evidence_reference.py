"""
engine/evidence_reference.py
T2-E Option B — the OWNER-RECORDED, EXPLICITLY UNVERIFIED evidence reference.

What this is
------------
One append-only record in which the project owner states, about ONE exact
active answered assertion: who they say reviewed or supports it, when, what
that covered, and — required — what it did NOT cover. It is a CLAIM the owner
recorded. InventorAI has verified none of it.

What this is NOT (each enforced by construction, not by convention)
-------------------------------------------------------------------
* NOT evidence. A named source is attribution, not proof that the material
  exists, is authentic, was inspected, or supports the assertion.
* NOT an ``answered`` ledger record. Answered records are REPLAYED by
  ``engine.session_reconstruction`` into ``progression_loop.run_iteration``;
  a reference must never be replayed as an inventor answer, so it is a
  separate durable row type and never enters that stream.
* NOT a provenance promotion. The anchor's ``provenance`` stays whatever the
  owner action made it (``OWNER_STATED``); ``EXTERNAL_EVIDENCE`` is NEVER
  written by anything here. Owner-typed attribution is testimonial, not
  documentary.
* NOT a validation promotion. ``claim_status`` is a FROZEN SINGLE VALUE, so
  this writer has no second value to write and can never become a ladder.
  The anchor's ``validation_status`` stays ``UNVALIDATED``.
* NOT a second ledger, confidence model, readiness model or state machine.
  It adds no axis, no score and no threshold, and it is read by nothing that
  decides anything.

Input contract
--------------
``make_evidence_reference(...)`` with an explicit, well-typed field set; the
four owner text fields pass the bounded text policy below. Returns an
immutable ``EvidenceReference`` or raises ``EvidenceReferenceError``
(fail closed).

Output contract
---------------
An immutable value object plus the canonical row dict for the durable store.
Values are stored verbatim after outer-whitespace stripping only.

Prohibited behaviours
---------------------
No effect on quality, validation status, provenance, readiness, scoring,
progression, maturity, gap status, next-question selection or quantities; no
in-place update of a stored row (change is supersession, withdrawal is a
superseding row); no parsing, interpretation or reinterpretation of the
owner's text; no echo of a rejected value in any exception.
"""
import re
from dataclasses import dataclass
from datetime import date
from typing import Optional, Tuple

# REUSE, not a second model: the merged T2-A anchor resolution is the canonical
# answer to "is this record a valid, currently ACTIVE answered assertion of this
# project?". Duplicating it here would create exactly the second model this
# increment forbids, so it is imported. `engine/requirement_quantity.py` is NOT
# modified by this increment.
from engine.requirement_quantity import (
    ANCHOR_ACTIVE, ANCHOR_WITHDRAWN, ANCHOR_INVALID,
    classify_ledger_anchor, classify_state_anchor,
)


class EvidenceReferenceError(ValueError):
    """Fail-closed validation error. Carries a field name and a reason only —
    never the submitted value, an identifier, or any surrounding state."""


class EvidenceReferenceHistoryError(ValueError):
    """Raised when a loaded reference history is structurally invalid. A
    populated corrupt history fails CLOSED; zero rows is always valid."""


# --- The frozen claim status -------------------------------------------------
# ONE value, deliberately. This records that the owner made a claim and that
# nothing has been verified. Because the writer has no second value available,
# no code path can promote a reference, and this can never grow into a
# competing validation ladder. (Precedents: requirement_quantity
# .QUANTITY_VALIDATION_STATUS and safety_signal's single-value vocabulary.)
CLAIM_STATUS_UNVALIDATED = "UNVALIDATED"
CLAIM_STATUSES = (CLAIM_STATUS_UNVALIDATED,)

# --- Bounded owner text policy ----------------------------------------------
# Text only; outer whitespace stripped only; empty rejected; C0 and C1 control
# characters rejected; over the per-field cap rejected. Nothing is parsed,
# converted, collapsed, normalized or reinterpreted. Each cap is far below the
# global MAX_FREE_TEXT_CHARS so oversized input is refused before staging.
MAX_SOURCE_IDENTITY_CHARS = 200
MAX_SCOPE_TEXT_CHARS = 600
MAX_LIMITATION_TEXT_CHARS = 600
_CONTROL_RE = re.compile(r"[\x00-\x1f\x7f-\x9f]")

# A bounded per-project cap, mirroring the merged T2-A precedent. Reaching it is
# an established refusal, never a silent drop.
MAX_EVIDENCE_REFERENCES_PER_PROJECT = 200

_TEXT_FIELDS = {
    "source_identity": MAX_SOURCE_IDENTITY_CHARS,
    "scope_text": MAX_SCOPE_TEXT_CHARS,
    "limitation_text": MAX_LIMITATION_TEXT_CHARS,
}

# --- Durable write outcomes (the merged T2-A truthful vocabulary, reused) ----
# INSERTED / EXACT_REPLAY: the exact canonical event is durably present.
# CONFLICT / REJECTED: established refusals decided BEFORE any row was written.
# STORAGE_FAILURE: the write was attempted and the durable ABSENCE of the event
# was afterwards PROVEN through the stable (project, event_key).
# COMMIT_UNKNOWN: the durable outcome could not be determined at all.
REFERENCE_INSERTED = "INSERTED"
REFERENCE_EXACT_REPLAY = "EXACT_REPLAY"
REFERENCE_CONFLICT = "CONFLICT"
REFERENCE_REJECTED = "REJECTED"
REFERENCE_STORAGE_FAILURE = "STORAGE_FAILURE"
REFERENCE_COMMIT_UNKNOWN = "COMMIT_UNKNOWN"
REFERENCE_WRITE_OUTCOMES = (
    REFERENCE_INSERTED, REFERENCE_EXACT_REPLAY, REFERENCE_CONFLICT,
    REFERENCE_REJECTED, REFERENCE_STORAGE_FAILURE, REFERENCE_COMMIT_UNKNOWN,
)
# The canonical identity fields an exact replay must match EXACTLY before a
# stored row may be reported as "the same event".
REFERENCE_EVENT_IDENTITY_FIELDS = (
    "anchor_record_id", "source_identity", "occurred_on", "scope_text",
    "limitation_text", "withdrawn", "supersedes_reference_id",
)

__all__ = [
    "EvidenceReference", "EvidenceReferenceError",
    "EvidenceReferenceHistoryError", "CLAIM_STATUS_UNVALIDATED",
    "CLAIM_STATUSES", "MAX_SOURCE_IDENTITY_CHARS", "MAX_SCOPE_TEXT_CHARS",
    "MAX_LIMITATION_TEXT_CHARS", "MAX_EVIDENCE_REFERENCES_PER_PROJECT",
    "REFERENCE_INSERTED", "REFERENCE_EXACT_REPLAY",
    "REFERENCE_CONFLICT", "REFERENCE_REJECTED", "REFERENCE_STORAGE_FAILURE",
    "REFERENCE_COMMIT_UNKNOWN", "REFERENCE_WRITE_OUTCOMES",
    "REFERENCE_EVENT_IDENTITY_FIELDS", "ANCHOR_ACTIVE", "ANCHOR_WITHDRAWN",
    "ANCHOR_INVALID", "classify_ledger_anchor", "classify_state_anchor",
    "normalize_reference_text", "normalize_occurred_on",
    "make_evidence_reference", "canonical_reference_dict",
    "validate_reference_history", "validate_new_reference",
    "active_reference_for_anchor", "reference_chain_for_anchor",
    "evidence_references_meta",
]


def normalize_reference_text(text, field):
    """Apply the bounded owner-text policy for ``field`` and return the stored
    form, or raise ``EvidenceReferenceError``. The submitted value is never
    parsed, localized, logged, or placed in the exception."""
    cap = _TEXT_FIELDS.get(field)
    if cap is None:
        raise EvidenceReferenceError("%s: unknown text field" % field)
    if not isinstance(text, str):
        raise EvidenceReferenceError("%s: must be text" % field)
    stripped = text.strip()
    if not stripped:
        raise EvidenceReferenceError("%s: is empty" % field)
    if _CONTROL_RE.search(stripped):
        raise EvidenceReferenceError("%s: contains control characters" % field)
    if len(stripped) > cap:
        raise EvidenceReferenceError("%s: is too long" % field)
    return stripped


def normalize_occurred_on(text):
    """The owner-stated date the review/support occurred, as an exact ISO-8601
    calendar date (``YYYY-MM-DD``). Stored verbatim; never reformatted,
    localized or converted to a timestamp, and never compared against the wall
    clock (a date the owner states is their statement, not ours to police)."""
    if not isinstance(text, str):
        raise EvidenceReferenceError("occurred_on: must be text")
    stripped = text.strip()
    if not stripped:
        raise EvidenceReferenceError("occurred_on: is empty")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", stripped):
        raise EvidenceReferenceError("occurred_on: must be YYYY-MM-DD")
    try:
        date.fromisoformat(stripped)
    except ValueError:
        raise EvidenceReferenceError("occurred_on: is not a real date") from None
    return stripped


@dataclass(frozen=True)
class EvidenceReference:
    """One immutable, append-only owner-recorded evidence reference.

    ``withdrawn`` is carried by a SUPERSEDING row, never written onto an
    existing one: the durable table has no UPDATE path, exactly like the
    INSERT-only records table."""
    reference_id: str
    reference_seq: int
    anchor_record_id: str
    source_identity: str
    occurred_on: str
    scope_text: str
    limitation_text: str
    claim_status: str
    withdrawn: bool
    supersedes_reference_id: Optional[str]
    event_key: str
    recorded_iteration: int
    recorded_at: str


def make_evidence_reference(*, reference_id, reference_seq, anchor_record_id,
                            source_identity, occurred_on, scope_text,
                            limitation_text, withdrawn=False,
                            supersedes_reference_id=None, event_key,
                            recorded_iteration, recorded_at):
    """Build a validated ``EvidenceReference`` or raise
    ``EvidenceReferenceError``. ``claim_status`` is not a parameter: it is the
    frozen constant, so no caller can supply another value."""
    for name, value in (("reference_id", reference_id),
                        ("anchor_record_id", anchor_record_id),
                        ("event_key", event_key),
                        ("recorded_at", recorded_at)):
        if not isinstance(value, str) or not value.strip():
            raise EvidenceReferenceError("%s: must be a non-empty string" % name)
    if not isinstance(reference_seq, int) or isinstance(reference_seq, bool) \
            or reference_seq < 0:
        raise EvidenceReferenceError("reference_seq: must be a non-negative int")
    if not isinstance(recorded_iteration, int) \
            or isinstance(recorded_iteration, bool) or recorded_iteration < 0:
        raise EvidenceReferenceError(
            "recorded_iteration: must be a non-negative int")
    if not isinstance(withdrawn, bool):
        raise EvidenceReferenceError("withdrawn: must be a bool")
    if supersedes_reference_id is not None:
        if not isinstance(supersedes_reference_id, str) \
                or not supersedes_reference_id.strip():
            raise EvidenceReferenceError(
                "supersedes_reference_id: must be a non-empty string or None")
        if supersedes_reference_id == reference_id:
            raise EvidenceReferenceError(
                "supersedes_reference_id: a reference cannot supersede itself")
    return EvidenceReference(
        reference_id=reference_id,
        reference_seq=reference_seq,
        anchor_record_id=anchor_record_id,
        source_identity=normalize_reference_text(source_identity, "source_identity"),
        occurred_on=normalize_occurred_on(occurred_on),
        scope_text=normalize_reference_text(scope_text, "scope_text"),
        # REQUIRED by the accepted design: a reference that does not say what it
        # did NOT cover cannot be recorded at all.
        limitation_text=normalize_reference_text(limitation_text, "limitation_text"),
        claim_status=CLAIM_STATUS_UNVALIDATED,
        withdrawn=withdrawn,
        supersedes_reference_id=supersedes_reference_id,
        event_key=event_key,
        recorded_iteration=recorded_iteration,
        recorded_at=recorded_at,
    )


def canonical_reference_dict(reference):
    """The canonical row for the durable store and the render carrier."""
    return {
        "reference_id": reference.reference_id,
        "reference_seq": reference.reference_seq,
        "anchor_record_id": reference.anchor_record_id,
        "source_identity": reference.source_identity,
        "occurred_on": reference.occurred_on,
        "scope_text": reference.scope_text,
        "limitation_text": reference.limitation_text,
        "claim_status": reference.claim_status,
        "withdrawn": bool(reference.withdrawn),
        "supersedes_reference_id": reference.supersedes_reference_id,
        "event_key": reference.event_key,
        "recorded_iteration": reference.recorded_iteration,
        "recorded_at": reference.recorded_at,
    }


def validate_reference_history(rows):
    """Structurally validate a loaded history. ZERO ROWS IS ALWAYS VALID; a
    POPULATED corrupt history raises ``EvidenceReferenceHistoryError`` so the
    caller fails closed rather than rendering partial truth."""
    rows = tuple(rows)
    if not rows:
        return rows
    seen_ids, seen_seq, seen_keys = set(), set(), set()
    successors, roots = {}, {}
    for row in rows:
        if not isinstance(row, EvidenceReference):
            raise EvidenceReferenceHistoryError("row is not an EvidenceReference")
        if row.claim_status != CLAIM_STATUS_UNVALIDATED:
            raise EvidenceReferenceHistoryError("row carries an unknown claim status")
        if row.reference_id in seen_ids:
            raise EvidenceReferenceHistoryError("duplicate reference_id")
        if row.reference_seq in seen_seq:
            raise EvidenceReferenceHistoryError("duplicate reference_seq")
        if row.event_key in seen_keys:
            raise EvidenceReferenceHistoryError("duplicate event_key")
        seen_ids.add(row.reference_id)
        seen_seq.add(row.reference_seq)
        seen_keys.add(row.event_key)
        prior = row.supersedes_reference_id
        if prior is None:
            if row.anchor_record_id in roots:
                raise EvidenceReferenceHistoryError(
                    "more than one chain root for one anchor")
            roots[row.anchor_record_id] = row.reference_id
        else:
            if prior in successors:
                raise EvidenceReferenceHistoryError(
                    "more than one successor for one reference")
            successors[prior] = row.reference_id
    for prior in successors:
        if prior not in seen_ids:
            raise EvidenceReferenceHistoryError("successor targets an unknown reference")
    # Every non-root must reach a root without cycling, and must stay on ONE anchor.
    by_id = {r.reference_id: r for r in rows}
    for row in rows:
        seen, cursor, limit = set(), row, len(rows) + 1
        while cursor.supersedes_reference_id is not None:
            if cursor.reference_id in seen or limit <= 0:
                raise EvidenceReferenceHistoryError("supersession cycle")
            seen.add(cursor.reference_id)
            limit -= 1
            nxt = by_id[cursor.supersedes_reference_id]
            if nxt.anchor_record_id != cursor.anchor_record_id:
                raise EvidenceReferenceHistoryError("chain crosses two anchors")
            cursor = nxt
    return rows


def _superseded_ids(rows):
    return {r.supersedes_reference_id for r in rows
            if r.supersedes_reference_id is not None}


def validate_new_reference(existing_rows, candidate):
    """Validate ``candidate`` against a VALID existing history. Raises
    ``EvidenceReferenceError`` on any violation; nothing is written by the
    caller when this raises."""
    rows = validate_reference_history(existing_rows)
    by_id = {r.reference_id: r for r in rows}
    if candidate.reference_id in by_id:
        raise EvidenceReferenceError("reference_id: already exists")
    if any(r.event_key == candidate.event_key for r in rows):
        raise EvidenceReferenceError("event_key: already exists")
    superseded = _superseded_ids(rows)
    prior_id = candidate.supersedes_reference_id
    if prior_id is None:
        if any(r.anchor_record_id == candidate.anchor_record_id
               and r.supersedes_reference_id is None for r in rows):
            raise EvidenceReferenceError(
                "supersedes_reference_id: this anchor already has a chain root")
        return candidate
    prior = by_id.get(prior_id)
    if prior is None:
        raise EvidenceReferenceError("supersedes_reference_id: unknown reference")
    if prior.anchor_record_id != candidate.anchor_record_id:
        raise EvidenceReferenceError(
            "supersedes_reference_id: belongs to a different anchor")
    if prior_id in superseded:
        raise EvidenceReferenceError(
            "supersedes_reference_id: that reference is already superseded")
    return candidate


def reference_chain_for_anchor(rows, anchor_record_id):
    """Every reference for one anchor, in append order."""
    return tuple(r for r in validate_reference_history(rows)
                 if r.anchor_record_id == anchor_record_id)


def active_reference_for_anchor(rows, anchor_record_id):
    """The CURRENT head of this anchor's chain, or None. The head is the only
    row that speaks for the anchor now; every earlier row is retained history."""
    chain = reference_chain_for_anchor(rows, anchor_record_id)
    if not chain:
        return None
    superseded = _superseded_ids(chain)
    heads = [r for r in chain if r.reference_id not in superseded]
    if len(heads) != 1:
        raise EvidenceReferenceHistoryError("anchor does not have exactly one head")
    return heads[0]


def evidence_references_meta(rows) -> Tuple[dict, ...]:
    """Read-only presentation carrier: the CURRENT head per anchor, ordered by
    append order, each as its canonical row plus the count of earlier rows it
    replaced. Derived only; nothing here is persisted or fed to any decision."""
    rows = validate_reference_history(rows)
    anchors = []
    for row in rows:
        if row.anchor_record_id not in anchors:
            anchors.append(row.anchor_record_id)
    out = []
    for anchor in anchors:
        head = active_reference_for_anchor(rows, anchor)
        if head is None:
            continue
        chain = reference_chain_for_anchor(rows, anchor)
        entry = canonical_reference_dict(head)
        entry["replaced_count"] = len(chain) - 1
        out.append(entry)
    return tuple(out)
