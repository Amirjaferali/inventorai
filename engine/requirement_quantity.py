"""T2-A — Quantified Requirements, Slice 1 (bounded; frozen Slice-1 data contract).

File path: ``engine/requirement_quantity.py``
Purpose: the ONE pure, deterministic owner of the requirement-quantity data
contract, the closed ``quantity_kind`` vocabulary, the bounded ``value_text``
policy, the fail-closed history validation, the per-anchor chain derivation
(active row / replaced prior values / withdrawn anchor) and the presentation
rows for the deliverable. Consumed by the durable store (validation INSIDE the
write transaction and on load), the web layer (propose / confirm glue and the
shared deliverable seam) and the tests.

Product boundary (Owner-fixed reduced Slice 1):
  * one ACTIVE quantity chain per eligible requirement anchor — an anchor is
    the ``rec_N`` id of an ACTIVE accepted ``answered`` ledger record that the
    Requirement Landscape currently derives as an ``assertion`` requirement;
  * a superseded anchor (an answer withdrawn through the governed correction
    path) makes its chain INACTIVE deterministically; rows are retained
    durably and are surfaced as a withdrawn-anchor chain, never deleted;
  * correction/supersession WITHIN a chain reuses the ledger's forward-edge
    idiom (the NEW row names the row it supersedes; prior rows are never
    rewritten);
  * ``value_text`` is inventor text kept presentation-neutral: it is stored
    as normalized, never localized, never logged, never placed in an
    exception; ``quantity_kind`` is a closed token localized only at display;
  * validation here is STRUCTURAL only. Nothing in Slice 1 claims feasibility,
    attainability, validation, safety, compliance or specialist review.

Provider-free, network-free, standard library only. Never mutates its inputs.
"""
import re
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from engine.idea_state import DISPOSITION_ANSWERED
from engine.requirement_landscape import derive_requirement_landscape


class QuantityHistoryError(ValueError):
    """A durably stored requirement-quantity history is structurally invalid
    (corruption). Raised by ``validate_quantity_history`` — inside the store's
    write transaction before any append, and on every load — and every
    outward consumer fails CLOSED on it (no partial history is ever served).
    The message names structural facts only: never a value, identifier, path,
    SQL detail or user content."""


class QuantityValueError(ValueError):
    """A proposed quantity kind / value text is not acceptable."""


# --- Frozen Slice-1 limits ---------------------------------------------------------
# Hard per-project cap on durable quantity rows (ALL rows, active and replaced).
# Enforced by the store INSIDE its serialized write transaction.
MAX_REQUIREMENT_QUANTITIES_PER_PROJECT = 200

# ==============================================================================
# PROVISIONAL BLOCK — pending the exact wording of the accepted final design
# delta (closed ``quantity_kind`` vocabulary and bounded ``value_text`` policy).
# The structure around this block (contract, store, routes, presentation,
# tests) does not depend on the specific tokens; only this block is swapped
# when the accepted values are supplied. Tokens are ASCII identifiers so each
# can key a localization catalogue entry (``UI_T2A_KIND_<token>``).
# ==============================================================================
QUANTITY_KINDS = (
    "target",       # the value the inventor aims for
    "minimum",      # a lower limit
    "maximum",      # an upper limit
    "range",        # an interval (both limits in the text)
    "tolerance",    # an allowed deviation
)
# Bounded, presentation-neutral value text: 1..MAX chars after normalization
# (surrounding whitespace stripped, internal runs of spaces/tabs collapsed to
# one space); no line breaks and no other control characters. Not parsed, not
# localized, not interpreted — kept exactly as the inventor stated it.
MAX_VALUE_TEXT_CHARS = 80
# ==============================================================================

_KIND_SET = frozenset(QUANTITY_KINDS)
_QUANTITY_ID_RE = re.compile(r"^qty-[0-9a-f]{32}$")
_ANCHOR_ID_RE = re.compile(r"^rec_[1-9][0-9]*$")
_EVENT_KEY_RE = re.compile(r"^[0-9a-f]{32}$")
_WS_RUN_RE = re.compile(r"\s+")
# Every C0/C1 control except TAB (a tab is whitespace and collapses to one
# space); the Unicode line/paragraph separators, NBSP and zero-width space
# are rejected too.
_CONTROL_RE = re.compile("[\\x00-\\x08\\x0a-\\x1f\\x7f-\\x9f\\u00a0\\u200b\\u2028\\u2029]")


@dataclass(frozen=True)
class RequirementQuantity:
    """One durable requirement-quantity row — EXACTLY the frozen Slice-1
    data contract. Frozen; never mutated in place; the inverse edge and every
    chain view are DERIVED (``quantity_chains``), never stored."""
    project_id: str
    quantity_seq: int
    quantity_id: str
    anchor_record_id: str
    requirement_id: str
    quantity_kind: str
    value_text: str
    supersedes_quantity_id: Optional[str]
    event_key: str


@dataclass(frozen=True)
class QuantityChain:
    """Derived per-anchor chain view: the ACTIVE row, the replaced prior rows
    (oldest first) and whether the answer anchor is still active."""
    anchor_record_id: str
    requirement_id: str
    active: RequirementQuantity
    replaced: Tuple[RequirementQuantity, ...]
    anchor_active: bool


# --- Kind / value policy ---------------------------------------------------------
def validate_quantity_kind(kind):
    """Return ``kind`` iff it is a closed-vocabulary token; else raise."""
    if kind not in _KIND_SET:
        raise QuantityValueError("unknown quantity kind")
    return kind


def normalize_value_text(text):
    """Apply the bounded value_text policy and return the stored form, or
    raise ``QuantityValueError``. Deterministic and idempotent. The text is
    never interpreted, localized, logged or placed in the exception."""
    if not isinstance(text, str):
        raise QuantityValueError("value text must be text")
    if _CONTROL_RE.search(text):
        raise QuantityValueError("value text contains control characters")
    normalized = _WS_RUN_RE.sub(" ", text).strip()
    if not normalized:
        raise QuantityValueError("value text is empty")
    if len(normalized) > MAX_VALUE_TEXT_CHARS:
        raise QuantityValueError("value text is too long")
    return normalized


def is_stored_value_text(text):
    """True iff ``text`` is EXACTLY a stored (normalized) value text."""
    if not isinstance(text, str):
        return False
    try:
        return normalize_value_text(text) == text
    except QuantityValueError:
        return False


# --- History validation (fail closed) -------------------------------------------
def validate_quantity_history(rows, project_id=None):
    """Validate a project's durable quantity rows (in stored ``quantity_seq``
    order) and return the immutable validated history as a tuple of
    ``RequirementQuantity``.

    ``rows`` is an iterable of mappings carrying the nine contract fields.
    ZERO rows are VALID (the empty tuple). Any structural defect raises
    ``QuantityHistoryError`` with NOTHING returned (no partial history):

      * a row of another project (when ``project_id`` is given); a
        non-ascending or duplicate sequence; a malformed / duplicate
        quantity id, event key or anchor id; an empty requirement id;
      * an unknown kind; a value text that is not in stored form;
      * a forward edge to an unknown or LATER row, to a row of a DIFFERENT
        anchor, or to a row already superseded (one chain, one successor);
        a row that changes the requirement id of its chain;
      * more than one ACTIVE row for the same anchor;
      * more rows than ``MAX_REQUIREMENT_QUANTITIES_PER_PROJECT``.

    Never mutates its input."""
    validated = []
    by_id = {}
    superseded = set()
    event_keys = set()
    last_seq = None
    for row in rows:
        try:
            record = RequirementQuantity(
                project_id=row["project_id"], quantity_seq=row["quantity_seq"],
                quantity_id=row["quantity_id"],
                anchor_record_id=row["anchor_record_id"],
                requirement_id=row["requirement_id"],
                quantity_kind=row["quantity_kind"], value_text=row["value_text"],
                supersedes_quantity_id=row["supersedes_quantity_id"],
                event_key=row["event_key"])
        except (KeyError, TypeError) as exc:
            raise QuantityHistoryError("quantity row is missing a field") from exc
        if project_id is not None and record.project_id != project_id:
            raise QuantityHistoryError("row belongs to another project")
        if not isinstance(record.project_id, str) or not record.project_id:
            raise QuantityHistoryError("malformed project id")
        if (not isinstance(record.quantity_seq, int) or isinstance(record.quantity_seq, bool)
                or record.quantity_seq < 0
                or (last_seq is not None and record.quantity_seq <= last_seq)):
            raise QuantityHistoryError("sequence is not strictly ascending")
        last_seq = record.quantity_seq
        if not isinstance(record.quantity_id, str) or not _QUANTITY_ID_RE.match(record.quantity_id):
            raise QuantityHistoryError("malformed quantity id")
        if record.quantity_id in by_id:
            raise QuantityHistoryError("duplicate quantity id")
        if not isinstance(record.anchor_record_id, str) or not _ANCHOR_ID_RE.match(record.anchor_record_id):
            raise QuantityHistoryError("malformed anchor record id")
        if not isinstance(record.requirement_id, str) or not record.requirement_id.strip():
            raise QuantityHistoryError("missing requirement id")
        if record.quantity_kind not in _KIND_SET:
            raise QuantityHistoryError("unknown quantity kind")
        if not is_stored_value_text(record.value_text):
            raise QuantityHistoryError("value text is not in stored form")
        if not isinstance(record.event_key, str) or not _EVENT_KEY_RE.match(record.event_key):
            raise QuantityHistoryError("malformed event key")
        if record.event_key in event_keys:
            raise QuantityHistoryError("duplicate event key")
        event_keys.add(record.event_key)
        target = record.supersedes_quantity_id
        if target is not None:
            if not isinstance(target, str) or target not in by_id:
                raise QuantityHistoryError("supersession edge to an unknown or later row")
            prior = by_id[target]
            if prior.anchor_record_id != record.anchor_record_id:
                raise QuantityHistoryError("cross-anchor supersession")
            if prior.requirement_id != record.requirement_id:
                raise QuantityHistoryError("requirement id changes within a chain")
            if target in superseded:
                raise QuantityHistoryError("row superseded more than once")
            superseded.add(target)
        by_id[record.quantity_id] = record
        validated.append(record)
        if len(validated) > MAX_REQUIREMENT_QUANTITIES_PER_PROJECT:
            raise QuantityHistoryError("history exceeds the per-project cap")
    active_anchors = set()
    for record in validated:
        if record.quantity_id not in superseded:
            if record.anchor_record_id in active_anchors:
                raise QuantityHistoryError("more than one active quantity for one anchor")
            active_anchors.add(record.anchor_record_id)
    return tuple(validated)


def superseded_ids(history):
    """The set of quantity ids that a later row supersedes (derived)."""
    return {r.supersedes_quantity_id for r in history
            if r.supersedes_quantity_id is not None}


def active_quantities(history) -> Dict[str, RequirementQuantity]:
    """``{anchor_record_id: active row}`` for an already-validated history."""
    replaced = superseded_ids(history)
    return {r.anchor_record_id: r for r in history if r.quantity_id not in replaced}


# --- Anchor eligibility and chain derivation --------------------------------------
def eligible_anchors(state):
    """Tuple of ``(requirement, record)`` for every ELIGIBLE requirement
    anchor of ``state`` in the landscape's stable order: an ``assertion``
    requirement whose primary anchor is an ACTIVE (not superseded) accepted
    ``answered`` ledger record with non-empty content. Pure and read-only."""
    by_id = {r.record_id: r for r in getattr(state, "assertions", []) or []}
    out = []
    for req in derive_requirement_landscape(state).requirements:
        anchor = req.primary_anchor
        if anchor.anchor_kind != "assertion":
            continue
        record = by_id.get(anchor.anchor_reference)
        if record is None:
            continue
        if getattr(record, "disposition", None) != DISPOSITION_ANSWERED:
            continue
        if getattr(record, "superseded_by", None) is not None:
            continue
        if not (getattr(record, "content", "") or "").strip():
            continue
        out.append((req, record))
    return tuple(out)


def quantity_chains(state) -> Tuple[QuantityChain, ...]:
    """Derive one ``QuantityChain`` per anchor from the validated history
    attached at ``state.requirement_quantities`` (absent or empty means no
    chains). Order: chains whose anchor is still eligible first, in landscape
    order; then withdrawn-anchor chains in first-seen stored order. Pure."""
    history = tuple(getattr(state, "requirement_quantities", None) or ())
    if not history:
        return ()
    replaced_ids = superseded_ids(history)
    per_anchor = {}
    order = []
    for row in history:
        if row.anchor_record_id not in per_anchor:
            per_anchor[row.anchor_record_id] = []
            order.append(row.anchor_record_id)
        per_anchor[row.anchor_record_id].append(row)
    eligible = [record.record_id for _req, record in eligible_anchors(state)]
    ordered = [a for a in eligible if a in per_anchor] + \
        [a for a in order if a not in eligible]
    chains = []
    for anchor in ordered:
        rows = per_anchor[anchor]
        active = [r for r in rows if r.quantity_id not in replaced_ids]
        if len(active) != 1:      # unreachable for a validated history; defensive
            continue
        chains.append(QuantityChain(
            anchor_record_id=anchor, requirement_id=active[0].requirement_id,
            active=active[0],
            replaced=tuple(r for r in rows if r.quantity_id in replaced_ids),
            anchor_active=anchor in eligible))
    return tuple(chains)


# --- Presentation rows for the deliverable (additive; nested; absent at zero) ----
# The canonical deliverable assembler (`engine/deliverable_assembler.py`) is
# FROZEN by the merged G-3 A-20/A-21 pin, so the additive nested key
# ``_session_meta["requirement_quantities"]`` is composed at the shared web
# deliverable seam from this pure builder, which returns None whenever no
# quantity row exists (zero rows add NO package key).
REQUIREMENT_QUANTITIES_META_KEY = "requirement_quantities"
REQUIREMENT_QUANTITIES_TITLE = "Quantities you recorded"
REQUIREMENT_QUANTITIES_NOTE = (
    "These values were entered by the inventor for the listed requirements. "
    "They are recorded as stated and have not been checked, validated, or "
    "assessed for feasibility, attainability, safety, or compliance.")
QUANTITY_PROVENANCE_PUBLIC = "Recorded by the inventor (not yet verified)"
QUANTITY_STATUS_CURRENT = "current"
QUANTITY_STATUS_WITHDRAWN_ANCHOR = "anchor_withdrawn"


def _statement_for(state, chain):
    """The requirement statement for a chain: the current landscape statement
    while the anchor is active; otherwise the retained withdrawn answer text
    (never an identifier)."""
    for req, record in eligible_anchors(state):
        if record.record_id == chain.anchor_record_id:
            return req.statement
    for record in getattr(state, "assertions", []) or []:
        if record.record_id == chain.anchor_record_id:
            return (getattr(record, "content", "") or "").strip()
    return ""


def requirement_quantities_meta(state):
    """Presentation-ready rows for every quantity chain of ``state`` (JSON-
    safe dict), or ``None`` when no row exists. Each row carries the current
    value (kind token + value text), the replaced prior values (oldest first)
    and whether the answer anchor is still active. Canonical tokens only —
    display labels are resolved by the template; no internal identifier and
    no raw internal status word beyond the two fixed status tokens."""
    chains = quantity_chains(state)
    if not chains:
        return None
    items = []
    for chain in chains:
        items.append({
            "statement": _statement_for(state, chain),
            "status": (QUANTITY_STATUS_CURRENT if chain.anchor_active
                       else QUANTITY_STATUS_WITHDRAWN_ANCHOR),
            "anchor_active": chain.anchor_active,
            "kind": chain.active.quantity_kind,
            "value_text": chain.active.value_text,
            "provenance": QUANTITY_PROVENANCE_PUBLIC,
            "replaced": [{"kind": r.quantity_kind, "value_text": r.value_text}
                         for r in chain.replaced],
        })
    return {
        "title": REQUIREMENT_QUANTITIES_TITLE,
        "note": REQUIREMENT_QUANTITIES_NOTE,
        "total": len(items),
        "active_total": sum(1 for i in items if i["anchor_active"]),
        "withdrawn_total": sum(1 for i in items if not i["anchor_active"]),
        "items": items,
    }
