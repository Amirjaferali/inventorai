"""T2-A — Quantified Requirements, Slice 1 (bounded; frozen Slice-1 data contract).

File path: ``engine/requirement_quantity.py``
Purpose: the ONE pure, deterministic owner of the requirement-quantity data
contract, the closed ``quantity_kind`` vocabulary, the bounded ``value_text``
policy, the fail-closed history validation, the per-anchor chain derivation
(active row / replaced prior values / withdrawn anchor) and the canonical
package rows for the deliverable. Consumed by the durable store (validation
INSIDE the write transaction and on load), the web layer (propose / confirm
glue and the shared deliverable seam) and the tests.

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
  * ``value_text`` is the inventor's text kept exactly (outer whitespace
    stripped only): never parsed, converted, normalized, localized, logged or
    placed in an exception; ``quantity_kind`` is a closed token localized only
    at display;
  * validation here is STRUCTURAL only. Nothing in Slice 1 claims feasibility,
    attainability, validation, safety, compliance or specialist review.

Provider-free, network-free, standard library only. Never mutates its inputs.
"""
import re
from dataclasses import dataclass
from datetime import datetime
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


# --- Frozen Slice-1 limits and vocabulary (accepted design delta §6) ------------
# Hard per-project cap on durable quantity rows (ALL rows, active and replaced).
# Enforced by the store INSIDE its serialized write transaction.
MAX_REQUIREMENT_QUANTITIES_PER_PROJECT = 200

# The closed ``quantity_kind`` vocabulary (six tokens). Each token keys one
# bilingual display entry (``UI_T2A_KIND_<TOKEN>``); no other kind is accepted
# or stored.
QUANTITY_KINDS = (
    "target_value",
    "minimum_value",
    "maximum_value",
    "range",
    "count",
    "other_quantity",
)

# The ``value_text`` policy: text only; outer whitespace stripped only; empty
# result rejected; C0 and C1 control characters rejected; more than
# MAX_VALUE_TEXT_CHARS Unicode code points rejected; nothing parsed, converted,
# collapsed, normalized or reinterpreted. The stored value is exactly the
# submitted value after outer-whitespace stripping.
MAX_VALUE_TEXT_CHARS = 120

# Fixed canonical row values (part of the canonical row contract, never
# localized prose).
QUANTITY_VALIDATION_STATUS = "UNVALIDATED"
QUANTITY_PROVENANCE = "OWNER_STATED"

# --- Durable write outcomes (the truthful outcome vocabulary) --------------------
# A quantity write reports WHAT IS KNOWN about the durable outcome. It never
# reports a definite non-write it has not established, and never reports a
# success it has not established. INSERTED and EXACT_REPLAY mean the exact
# canonical event is durably present. CONFLICT and REJECTED are established
# refusals decided BEFORE any row was written. STORAGE_FAILURE means the write
# was attempted and the durable absence of the event was afterwards PROVEN
# through the stable (project, event_key). COMMIT_UNKNOWN means the durable
# outcome could not be determined at all — the only honest answer left.
QUANTITY_INSERTED = "INSERTED"
QUANTITY_EXACT_REPLAY = "EXACT_REPLAY"
QUANTITY_CONFLICT = "CONFLICT"
QUANTITY_REJECTED = "REJECTED"
QUANTITY_STORAGE_FAILURE = "STORAGE_FAILURE"
QUANTITY_COMMIT_UNKNOWN = "COMMIT_UNKNOWN"
QUANTITY_WRITE_OUTCOMES = (
    QUANTITY_INSERTED, QUANTITY_EXACT_REPLAY, QUANTITY_CONFLICT,
    QUANTITY_REJECTED, QUANTITY_STORAGE_FAILURE, QUANTITY_COMMIT_UNKNOWN,
)
# The canonical identity fields an exact replay must match EXACTLY before a
# stored row may be reported as "the same event".
QUANTITY_EVENT_IDENTITY_FIELDS = (
    "anchor_record_id", "requirement_id", "quantity_kind", "value_text",
    "supersedes_quantity_id",
)

# --- Anchor resolution states (never conflated) ---------------------------------
# ACTIVE    : a valid, currently answered assertion anchor.
# WITHDRAWN : a valid, previously answered assertion anchor that was GENUINELY
#             superseded/withdrawn through the governed correction path. ONLY
#             this state may be presented as withdrawn history.
# INVALID   : missing, never a valid answered assertion anchor, or an anchor
#             whose assertion/requirement relationship is inconsistent. Every
#             outward surface fails CLOSED on it; it is NEVER presented as
#             legitimate withdrawn history and is never silently repaired.
ANCHOR_ACTIVE = "active"
ANCHOR_WITHDRAWN = "withdrawn"
ANCHOR_INVALID = "invalid"

_KIND_SET = frozenset(QUANTITY_KINDS)
_QUANTITY_ID_RE = re.compile(r"^qty-[0-9a-f]{32}$")
_ANCHOR_ID_RE = re.compile(r"^rec_[1-9][0-9]*$")
_EVENT_KEY_RE = re.compile(r"^[0-9a-f]{32}$")
# C0 controls (U+0000–U+001F, tab and line breaks included) and C1 controls
# (U+007F–U+009F). Nothing else is excluded by the policy.
_CONTROL_RE = re.compile("[\\x00-\\x1f\\x7f-\\x9f]")


@dataclass(frozen=True)
class RequirementQuantity:
    """One requirement-quantity row — EXACTLY the accepted canonical row.
    Frozen; never mutated in place; the inverse edge and every chain view are
    DERIVED (``quantity_chains``), never stored. Project scoping is enforced by
    the store and the database ``project_id`` column, not by this row.
    ``recorded_iteration`` / ``recorded_at`` are recording facts generated once
    per event and are never part of event identity."""
    quantity_id: str                     # "qty-" + uuid4().hex, generated once
    quantity_seq: int                    # per-project 0-based, generated once
    anchor_record_id: str                # rec_N of the anchoring answered record
    requirement_id: str                  # "req:assertion:" + anchor_record_id
    quantity_kind: str                   # vocabulary token
    value_text: str                      # exact post-policy value
    supersedes_quantity_id: Optional[str]
    event_key: str
    recorded_iteration: int
    recorded_at: str                     # UTC ISO-8601, never part of identity
    validation_status: str = QUANTITY_VALIDATION_STATUS
    provenance: str = QUANTITY_PROVENANCE


CANONICAL_ROW_FIELDS = tuple(RequirementQuantity.__dataclass_fields__)


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
    """Apply the accepted value_text policy and return the stored form, or
    raise ``QuantityValueError``. Text only; outer whitespace stripped only;
    empty rejected; C0/C1 controls rejected; more than MAX_VALUE_TEXT_CHARS
    code points rejected. Deterministic and idempotent. The text is never
    parsed, converted, normalized, localized, logged or placed in the
    exception."""
    if not isinstance(text, str):
        raise QuantityValueError("value text must be text")
    stripped = text.strip()
    if not stripped:
        raise QuantityValueError("value text is empty")
    if _CONTROL_RE.search(stripped):
        raise QuantityValueError("value text contains control characters")
    if len(stripped) > MAX_VALUE_TEXT_CHARS:
        raise QuantityValueError("value text is too long")
    return stripped


def is_stored_value_text(text):
    """True iff ``text`` is EXACTLY a stored (post-policy) value text."""
    if not isinstance(text, str):
        return False
    try:
        return normalize_value_text(text) == text
    except QuantityValueError:
        return False


def is_recorded_at(text):
    """True iff ``text`` is a UTC ISO-8601 timestamp (offset +00:00 / Z)."""
    if not isinstance(text, str) or not text:
        return False
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset().total_seconds() == 0


# --- Anchor resolution against the durable ledger assertions ---------------------
def answered_anchor_index(records):
    """``{record_id: record}`` over the ledger records that ARE valid answered
    assertion anchors: a well-formed ``rec_N`` id, the accepted ``answered``
    disposition and non-empty content. A record of any other disposition, an
    empty-content record and a malformed id are absent — they were never a
    valid answered assertion anchor. Pure; never mutates its input."""
    index = {}
    for record in records or ():
        record_id = getattr(record, "record_id", None)
        if not isinstance(record_id, str) or not _ANCHOR_ID_RE.match(record_id):
            continue
        if getattr(record, "disposition", None) != DISPOSITION_ANSWERED:
            continue
        if not (getattr(record, "content", "") or "").strip():
            continue
        index[record_id] = record
    return index


def supersession_relations(records):
    """``({prior_record_id: successor_record_id}, {record_id: record})`` built
    from the DURABLE FORWARD edge only.

    The durable store is INSERT-only, so a governed correction carries the
    relationship FORWARD on the NEW record (``successor.supersedes`` names the
    prior record); the prior row's persisted ``superseded_by`` is filled in by
    load-time reconciliation and may also be a stale or corrupt persisted
    value. The forward map is therefore built from ``supersedes`` alone and is
    never derived from ``superseded_by``, so a one-sided persisted reference
    cannot manufacture its own evidence. A prior record named by two different
    successors yields no forward edge at all (the inverse edge must be
    single-valued), which resolves to ANCHOR_INVALID below."""
    forward, by_id, ambiguous = {}, {}, set()
    for record in records or ():
        record_id = getattr(record, "record_id", None)
        if isinstance(record_id, str):
            by_id[record_id] = record
        for prior_id in (getattr(record, "supersedes", None) or ()):
            if prior_id in forward and forward[prior_id] != record_id:
                ambiguous.add(prior_id)
            forward[prior_id] = record_id
    for prior_id in ambiguous:
        forward.pop(prior_id, None)
    return forward, by_id


def _supersession_is_cyclic(forward, anchor_record_id, limit):
    """True iff following the forward edges from ``anchor_record_id`` returns
    to it (a self- or longer supersession cycle). Bounded by ``limit``."""
    seen, node = set(), forward.get(anchor_record_id)
    while node is not None and len(seen) <= limit:
        if node == anchor_record_id:
            return True
        if node in seen:
            return False
        seen.add(node)
        node = forward.get(node)
    return False


def classify_ledger_anchor(records, anchor_record_id, index=None, relations=None):
    """Resolve ``anchor_record_id`` against the project's DURABLE ledger
    assertions and return ``ANCHOR_ACTIVE`` / ``ANCHOR_WITHDRAWN`` /
    ``ANCHOR_INVALID``.

    ``ANCHOR_WITHDRAWN`` is returned ONLY when the record really is a valid
    answered assertion anchor AND the COMPLETE reciprocal governed correction
    relationship is proven from the durable records:

      * the old answered record identifies the alleged successor
        (``superseded_by``);
      * that successor exists among this project's records;
      * the successor's durable forward relation identifies the old record
        (``successor.supersedes`` contains it), single-valued;
      * the relationship is neither self-referential nor cyclic.

    A non-null ``superseded_by`` is NEVER sufficient on its own. A missing
    record, a record that was never a valid answered assertion anchor, a
    malformed anchor id, and a one-sided, mis-targeted, cross-project, absent,
    ambiguous or cyclic supersession are all ``ANCHOR_INVALID`` — never
    withdrawn."""
    resolved = answered_anchor_index(records) if index is None else index
    record = resolved.get(anchor_record_id)
    if record is None:
        return ANCHOR_INVALID
    forward, by_id = (supersession_relations(records) if relations is None else relations)
    declared = getattr(record, "superseded_by", None)
    successor_id = forward.get(anchor_record_id)
    if declared is None and successor_id is None:
        return ANCHOR_ACTIVE
    # One or both sides claim a supersession: it must be complete and reciprocal.
    if declared is None or successor_id is None or declared != successor_id:
        return ANCHOR_INVALID
    if successor_id == anchor_record_id:
        return ANCHOR_INVALID
    successor = by_id.get(successor_id)
    if successor is None:
        return ANCHOR_INVALID
    if anchor_record_id not in (getattr(successor, "supersedes", None) or ()):
        return ANCHOR_INVALID
    if _supersession_is_cyclic(forward, anchor_record_id, len(by_id)):
        return ANCHOR_INVALID
    return ANCHOR_WITHDRAWN


def classify_state_anchor(state, anchor_record_id, eligible=None, index=None,
                          relations=None):
    """Resolve ``anchor_record_id`` against a live/replayed ``state``.

    ACTIVE only when the requirement landscape currently derives the anchor as
    an eligible ``assertion`` requirement. Otherwise the durable ledger decides:
    a genuinely superseded answered anchor is WITHDRAWN; anything else —
    missing, never a valid answered assertion anchor, or an anchor the ledger
    still calls active while the landscape derives no requirement for it (an
    INCONSISTENT assertion/requirement relationship) — is INVALID."""
    if eligible is None:
        eligible = {record.record_id for _req, record in eligible_anchors(state)}
    if anchor_record_id in eligible:
        return ANCHOR_ACTIVE
    records = getattr(state, "assertions", []) or []
    ledger = classify_ledger_anchor(records, anchor_record_id, index=index,
                                    relations=relations)
    return ANCHOR_WITHDRAWN if ledger == ANCHOR_WITHDRAWN else ANCHOR_INVALID


def resolved_anchor_states(state):
    """``{anchor_record_id: resolution}`` for every anchor named by the history
    attached to ``state``. Computed once per render/package pass."""
    history = tuple(getattr(state, "requirement_quantities", None) or ())
    if not history:
        return {}
    eligible = {record.record_id for _req, record in eligible_anchors(state)}
    records = getattr(state, "assertions", []) or []
    index = answered_anchor_index(records)
    relations = supersession_relations(records)
    return {row.anchor_record_id: classify_state_anchor(
        state, row.anchor_record_id, eligible=eligible, index=index, relations=relations)
        for row in history}


def _require_resolvable_anchors(resolutions):
    """Fail CLOSED on any anchor that does not resolve to a valid answered
    assertion record. Never repairs, deletes or reinterprets the durable row."""
    if any(value == ANCHOR_INVALID for value in resolutions.values()):
        raise QuantityHistoryError(
            "quantity anchor does not resolve to a valid answered record")


def canonical_row_dict(record):
    """The canonical row of ``record`` as a plain JSON-safe dict."""
    return {name: getattr(record, name) for name in CANONICAL_ROW_FIELDS}


# --- History validation (fail closed) -------------------------------------------
def validate_quantity_history(rows, assertions=None):
    """Validate a project's durable quantity rows (in stored ``quantity_seq``
    order) and return the immutable validated history as a tuple of
    ``RequirementQuantity``.

    ``rows`` is an iterable of mappings carrying the persisted contract
    fields (``validation_status`` / ``provenance`` may be absent — they are
    the fixed canonical values — or present with exactly those values).
    ZERO rows are VALID (the empty tuple). Any structural defect raises
    ``QuantityHistoryError`` with NOTHING returned (no partial history):

      * a non-ascending or duplicate sequence; a malformed / duplicate
        quantity id, event key or anchor id; a requirement id that is not
        ``req:assertion:<anchor>``;
      * an unknown kind; a value text that is not in stored form; a
        negative or non-integer recorded iteration; a recorded_at that is
        not a UTC ISO-8601 timestamp; a non-canonical validation status or
        provenance;
      * a forward edge to an unknown or LATER row, to a row of a DIFFERENT
        anchor, or to a row already superseded (one chain, one successor);
      * a second chain root for one anchor, or more than one ACTIVE row for
        one anchor;
      * more rows than ``MAX_REQUIREMENT_QUANTITIES_PER_PROJECT``.

    ``assertions`` — when given — is the project's DURABLE ledger assertion
    records. Every row is then additionally validated AGAINST THE LEDGER, not
    only against the other quantity rows: the anchor must resolve to a record
    of THIS project that really is a valid answered assertion anchor (active or
    genuinely withdrawn), and the requirement identity must be the canonical
    ``req:assertion:<anchor>`` of that same record. An anchor that is missing,
    was never a valid answered assertion, or whose requirement relationship is
    inconsistent raises — it is never silently accepted and never presented as
    withdrawn history. Passing ``None`` (the default) keeps the pure
    row-against-row validation for callers that hold no ledger.

    Never mutates its input."""
    anchor_index = None if assertions is None else answered_anchor_index(assertions)
    anchor_relations = None if assertions is None else supersession_relations(assertions)
    validated = []
    by_id = {}
    superseded = set()
    roots = set()
    event_keys = set()
    last_seq = None
    for row in rows:
        try:
            record = RequirementQuantity(
                quantity_id=row["quantity_id"], quantity_seq=row["quantity_seq"],
                anchor_record_id=row["anchor_record_id"],
                requirement_id=row["requirement_id"],
                quantity_kind=row["quantity_kind"], value_text=row["value_text"],
                supersedes_quantity_id=row["supersedes_quantity_id"],
                event_key=row["event_key"],
                recorded_iteration=row["recorded_iteration"],
                recorded_at=row["recorded_at"],
                validation_status=row.get("validation_status", QUANTITY_VALIDATION_STATUS),
                provenance=row.get("provenance", QUANTITY_PROVENANCE))
        except (KeyError, TypeError, AttributeError) as exc:
            raise QuantityHistoryError("quantity row is missing a field") from exc
        seq = record.quantity_seq
        if (not isinstance(seq, int) or isinstance(seq, bool) or seq < 0
                or (last_seq is not None and seq <= last_seq)):
            raise QuantityHistoryError("sequence is not strictly ascending")
        last_seq = seq
        if not isinstance(record.quantity_id, str) or not _QUANTITY_ID_RE.match(record.quantity_id):
            raise QuantityHistoryError("malformed quantity id")
        if record.quantity_id in by_id:
            raise QuantityHistoryError("duplicate quantity id")
        if not isinstance(record.anchor_record_id, str) or not _ANCHOR_ID_RE.match(record.anchor_record_id):
            raise QuantityHistoryError("malformed anchor record id")
        if record.requirement_id != "req:assertion:" + record.anchor_record_id:
            raise QuantityHistoryError("requirement id does not match its anchor")
        if anchor_index is not None and classify_ledger_anchor(
                None, record.anchor_record_id, index=anchor_index,
                relations=anchor_relations) == ANCHOR_INVALID:
            raise QuantityHistoryError(
                "anchor is not a valid answered assertion record of this project")
        if record.quantity_kind not in _KIND_SET:
            raise QuantityHistoryError("unknown quantity kind")
        if not is_stored_value_text(record.value_text):
            raise QuantityHistoryError("value text is not in stored form")
        if not isinstance(record.event_key, str) or not _EVENT_KEY_RE.match(record.event_key):
            raise QuantityHistoryError("malformed event key")
        if record.event_key in event_keys:
            raise QuantityHistoryError("duplicate event key")
        event_keys.add(record.event_key)
        it = record.recorded_iteration
        if not isinstance(it, int) or isinstance(it, bool) or it < 0:
            raise QuantityHistoryError("malformed recorded iteration")
        if not is_recorded_at(record.recorded_at):
            raise QuantityHistoryError("malformed recorded_at timestamp")
        if record.validation_status != QUANTITY_VALIDATION_STATUS:
            raise QuantityHistoryError("non-canonical validation status")
        if record.provenance != QUANTITY_PROVENANCE:
            raise QuantityHistoryError("non-canonical provenance")
        target = record.supersedes_quantity_id
        if target is None:
            if record.anchor_record_id in roots:
                raise QuantityHistoryError("second chain root for one anchor")
            roots.add(record.anchor_record_id)
        else:
            if not isinstance(target, str) or target not in by_id:
                raise QuantityHistoryError("supersession edge to an unknown or later row")
            prior = by_id[target]
            if prior.anchor_record_id != record.anchor_record_id:
                raise QuantityHistoryError("cross-anchor supersession")
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


def validate_new_quantity(existing_rows, candidate, assertions=None):
    """Validate a PROPOSED canonical quantity row TOGETHER with the project's
    existing durable history, exactly as the durable history will read after
    the insert, and return the validated combined history.

    ``existing_rows`` is the stored row mapping sequence (``quantity_seq``
    order); ``candidate`` is the ``RequirementQuantity`` about to be inserted
    with its final assigned ``quantity_seq``. Because the combined sequence
    goes through the SAME ``validate_quantity_history``, a direct store caller
    cannot commit an invalid kind, a malformed generated quantity id or event
    key, an inconsistent requirement identity, an anchor that is not a valid
    answered assertion record of this project, a duplicate event key, a second
    chain root, a cross-anchor or already-consumed supersession edge, a
    non-canonical validation status/provenance or any other invalid canonical
    row. Raises ``QuantityHistoryError``; writes nothing."""
    if not isinstance(candidate, RequirementQuantity):
        raise QuantityHistoryError("quantity row is missing a field")
    return validate_quantity_history(
        list(existing_rows) + [canonical_row_dict(candidate)], assertions=assertions)


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
    resolutions = resolved_anchor_states(state)
    _require_resolvable_anchors(resolutions)
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
            anchor_active=resolutions[anchor] == ANCHOR_ACTIVE))
    return tuple(chains)


# --- Canonical package rows (additive; nested; absent at zero) -----------------
# The canonical deliverable assembler (`engine/deliverable_assembler.py`) is
# FROZEN by the merged G-3 A-20/A-21 pin, so the additive nested key
# ``_session_meta["requirement_quantities"]`` is composed at the shared web
# deliverable seam from this pure builder, which returns None whenever no
# quantity row exists (zero rows add NO package key). The shape is
# ``{"total": n, "rows": [...]}``: each row is the canonical row plus the two
# derived canonical booleans ``active`` and ``anchor_active``, ordered by
# ``quantity_seq``. No label, title, note, translated prose or presentation
# sentence is ever placed in the package.
REQUIREMENT_QUANTITIES_META_KEY = "requirement_quantities"


def requirement_quantities_meta(state):
    """Canonical package rows for every quantity row of ``state`` (JSON-safe
    dict ``{"total", "rows"}``), or ``None`` when no row exists."""
    history = tuple(getattr(state, "requirement_quantities", None) or ())
    if not history:
        return None
    replaced = superseded_ids(history)
    resolutions = resolved_anchor_states(state)
    _require_resolvable_anchors(resolutions)
    rows = []
    for record in sorted(history, key=lambda r: r.quantity_seq):
        row = canonical_row_dict(record)
        row["active"] = record.quantity_id not in replaced
        row["anchor_active"] = resolutions[record.anchor_record_id] == ANCHOR_ACTIVE
        rows.append(row)
    return {"total": len(rows), "rows": rows}


def requirement_statement(state, anchor_record_id):
    """The requirement statement for an anchor: the current landscape
    statement while the anchor is active; otherwise the retained withdrawn
    answer text (never an identifier). Presentation helper for templates."""
    for req, record in eligible_anchors(state):
        if record.record_id == anchor_record_id:
            return req.statement
    for record in getattr(state, "assertions", []) or []:
        if record.record_id == anchor_record_id:
            return (getattr(record, "content", "") or "").strip()
    return ""
