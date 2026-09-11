"""T2-A — Quantified Requirements, Slice 1 (bounded).

File path: ``engine/requirement_quantity.py``
Purpose: the ONE pure, deterministic owner of the requirement-quantity
vocabulary, the canonical stored value form, the fail-closed history
validation, and the read-only derivation of the CURRENTLY ACTIVE quantified
requirements for an ``IdeaState``. Consumed by the durable store (validation
on load), the deliverable assembler (presentation-ready rows) and the web
layer (eligible anchors / active chain lookup).

Product boundary (Owner-fixed reduced Slice 1):
  * one ACTIVE quantity chain per eligible requirement anchor — an anchor is
    the ``rec_N`` id of an ACTIVE accepted ``answered`` record that the
    Requirement Landscape currently derives as an ``assertion`` requirement;
  * a superseded anchor (an answer withdrawn through the governed correction
    path) makes its chain INACTIVE deterministically — the rows are retained
    durably and are never deleted, they simply attach to nothing current;
  * correction/supersession WITHIN a chain reuses the same forward-edge idiom
    as the ledger (the NEW row names the row it supersedes; prior rows are
    never rewritten);
  * canonical STORED values (decimal text, bound token, unit code) are kept
    separate from localized PRESENTATION (the ``web.ui_text`` catalogue owns
    every display label);
  * validation here is STRUCTURAL only. Nothing in this module (or anywhere in
    Slice 1) claims feasibility, validation, safety, compliance or specialist
    review of a recorded quantity.

Provider-free, network-free, standard library only. Never mutates its inputs.
"""
import re
from dataclasses import dataclass, replace
from decimal import Decimal, InvalidOperation
from typing import Optional, Tuple

from engine.idea_state import DISPOSITION_ANSWERED
from engine.requirement_landscape import derive_requirement_landscape


class QuantityHistoryError(ValueError):
    """A durably stored requirement-quantity history is structurally invalid
    (corruption). Raised by ``validate_quantity_history`` and propagated by
    the store's load; every outward consumer fails CLOSED on it (no partial
    history is ever served). The message names structural facts only —
    never a value, identifier, path, SQL detail or user content."""


class QuantityValueError(ValueError):
    """A submitted quantity value / bound / unit is not acceptable."""


# --- Frozen canonical vocabularies (stored tokens; display lives in ui_text) ----
QUANTITY_BOUND_TARGET = "target"
QUANTITY_BOUND_MINIMUM = "minimum"
QUANTITY_BOUND_MAXIMUM = "maximum"
QUANTITY_BOUNDS = (
    QUANTITY_BOUND_TARGET, QUANTITY_BOUND_MINIMUM, QUANTITY_BOUND_MAXIMUM,
)

# Closed unit vocabulary. Codes are ASCII identifiers so they can key a
# localization catalogue entry (``UI_T2A_UNIT_<code>``). No free-text unit is
# ever accepted or stored.
QUANTITY_UNITS = (
    "mm", "cm", "m",
    "g", "kg",
    "s", "min", "h",
    "V", "A", "W", "Wh", "mAh", "Hz", "ohm",
    "degC",
    "percent",
    "count",
)

_BOUND_SET = frozenset(QUANTITY_BOUNDS)
_UNIT_SET = frozenset(QUANTITY_UNITS)

# Bounded numeric grammar: optional sign, up to 12 integer digits, up to 6
# fraction digits, ASCII digits only, no exponent, no thousands separator.
_INPUT_VALUE_RE = re.compile(r"^-?[0-9]{1,12}(\.[0-9]{1,6})?$")
_CANONICAL_VALUE_RE = re.compile(r"^-?(0|[1-9][0-9]{0,11})(\.[0-9]{0,5}[1-9])?$")
_QUANTITY_ID_RE = re.compile(r"^qty-[0-9a-f]{32}$")
_ANCHOR_ID_RE = re.compile(r"^rec_[1-9][0-9]*$")
MAX_VALUE_INPUT_CHARS = 32


@dataclass(frozen=True)
class RequirementQuantity:
    """One durable requirement-quantity row (frozen; never mutated in place).

    ``supersedes`` is the forward edge carried by the NEW row (the row it
    corrects); ``superseded_by`` is the inverse edge, re-derived on load from
    the forward edges exactly like ``record_contract.reconcile_supersession_edges``
    — it is never stored."""
    quantity_id: str
    anchor_record_id: str
    bound: str
    value: str            # canonical decimal text (see canonical_value)
    unit: str             # one of QUANTITY_UNITS
    supersedes: Optional[str] = None
    superseded_by: Optional[str] = None


@dataclass(frozen=True)
class QuantifiedRequirement:
    """Read-only derivation row: a CURRENT requirement (statement + anchor)
    together with its ACTIVE quantity. Presentation-ready, JSON-safe."""
    anchor_record_id: str
    statement: str
    quantity: RequirementQuantity


# --- Canonical value ------------------------------------------------------------
def canonical_value(text):
    """Canonicalize a submitted numeric string, or raise ``QuantityValueError``.

    Accepts the bounded ASCII grammar only (see ``_INPUT_VALUE_RE``) and
    returns the ONE canonical decimal text: no exponent, no leading zeros,
    no trailing fraction zeros, no negative zero, no whitespace. Deterministic
    and idempotent: ``canonical_value(canonical_value(x)) == canonical_value(x)``."""
    if not isinstance(text, str):
        raise QuantityValueError("value must be text")
    stripped = text.strip()
    if not stripped or len(stripped) > MAX_VALUE_INPUT_CHARS:
        raise QuantityValueError("value is empty or too long")
    if not _INPUT_VALUE_RE.match(stripped):
        raise QuantityValueError("value is not a plain decimal number")
    try:
        number = Decimal(stripped)
    except InvalidOperation as exc:      # unreachable after the regex; defensive
        raise QuantityValueError("value is not a plain decimal number") from exc
    if number == 0:
        return "0"
    normalized = number.normalize()
    out = format(normalized, "f")
    # ``normalize`` can produce an exponent form for e.g. 1000 -> 1E+3;
    # ``format(..., "f")`` expands it back to plain digits.
    if not _CANONICAL_VALUE_RE.match(out):     # defensive: never store a non-canonical
        raise QuantityValueError("value could not be canonicalized")
    return out


def is_canonical_value(text):
    """True iff ``text`` is EXACTLY a canonical stored value."""
    if not isinstance(text, str) or not _CANONICAL_VALUE_RE.match(text):
        return False
    try:
        return canonical_value(text) == text
    except QuantityValueError:
        return False


def validate_bound(bound):
    if bound not in _BOUND_SET:
        raise QuantityValueError("unknown bound")
    return bound


def validate_unit(unit):
    if unit not in _UNIT_SET:
        raise QuantityValueError("unknown unit")
    return unit


# --- History validation (fail closed) ------------------------------------------
def validate_quantity_history(rows):
    """Validate a project's durable quantity rows (in stored ``seq`` order) and
    return the immutable validated history as a tuple of
    ``RequirementQuantity`` with inverse edges derived.

    ``rows`` is an iterable of mappings with the keys ``quantity_id``,
    ``anchor_record_id``, ``bound``, ``value``, ``unit`` and ``supersedes``.
    ZERO rows are VALID (the empty tuple). Any structural defect raises
    ``QuantityHistoryError`` with NOTHING returned (no partial history):

      * malformed / duplicate quantity id; malformed anchor id;
      * unknown bound or unit; a non-canonical stored value;
      * a forward edge to an unknown or LATER row, to a row of a DIFFERENT
        anchor, or to a row that is already superseded (one chain, one
        successor);
      * more than one ACTIVE row for the same anchor.

    Never mutates its input; derives (never stores) ``superseded_by``."""
    validated = []
    by_id = {}
    superseded_by = {}
    for row in rows:
        try:
            qid = row["quantity_id"]
            anchor = row["anchor_record_id"]
            bound = row["bound"]
            value = row["value"]
            unit = row["unit"]
            supersedes = row["supersedes"]
        except (KeyError, TypeError) as exc:
            raise QuantityHistoryError("quantity row is missing a field") from exc
        if not isinstance(qid, str) or not _QUANTITY_ID_RE.match(qid):
            raise QuantityHistoryError("malformed quantity id")
        if qid in by_id:
            raise QuantityHistoryError("duplicate quantity id")
        if not isinstance(anchor, str) or not _ANCHOR_ID_RE.match(anchor):
            raise QuantityHistoryError("malformed anchor record id")
        if bound not in _BOUND_SET:
            raise QuantityHistoryError("unknown bound token")
        if unit not in _UNIT_SET:
            raise QuantityHistoryError("unknown unit code")
        if not is_canonical_value(value):
            raise QuantityHistoryError("stored value is not canonical")
        if supersedes is not None:
            if not isinstance(supersedes, str) or supersedes not in by_id:
                raise QuantityHistoryError(
                    "supersession edge to an unknown or later row")
            if supersedes == qid:
                raise QuantityHistoryError("a row cannot supersede itself")
            prior = by_id[supersedes]
            if prior.anchor_record_id != anchor:
                raise QuantityHistoryError("cross-anchor supersession")
            if supersedes in superseded_by:
                raise QuantityHistoryError("row superseded more than once")
            superseded_by[supersedes] = qid
        record = RequirementQuantity(
            quantity_id=qid, anchor_record_id=anchor, bound=bound,
            value=value, unit=unit, supersedes=supersedes)
        by_id[qid] = record
        validated.append(record)
    # Derive inverse edges (never stored) and enforce one ACTIVE row per anchor.
    active_anchors = set()
    out = []
    for record in validated:
        successor = superseded_by.get(record.quantity_id)
        if successor is None:
            if record.anchor_record_id in active_anchors:
                raise QuantityHistoryError(
                    "more than one active quantity for one anchor")
            active_anchors.add(record.anchor_record_id)
        out.append(replace(record, superseded_by=successor))
    return tuple(out)


def active_quantities(history):
    """``{anchor_record_id: RequirementQuantity}`` for the ACTIVE rows (those
    with no successor) of an already-validated history. Deterministic."""
    result = {}
    for record in history:
        if record.superseded_by is None:
            result[record.anchor_record_id] = record
    return result


# --- Anchor eligibility and read-only derivation -------------------------------
def eligible_anchors(state):
    """Return the tuple of ``(requirement, record)`` pairs for every eligible
    requirement anchor of ``state``, in the landscape's stable order.

    Eligible == the Requirement Landscape currently derives an ``assertion``
    requirement whose primary anchor is an ACTIVE (not superseded) accepted
    ``answered`` ledger record with non-empty content. A withdrawn answer is
    never eligible, so a chain attached to it becomes inactive the moment
    the correction is durable. Pure and read-only."""
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


# --- Presentation rows for the deliverable (additive; nested; None at zero) -----
# The canonical deliverable assembler (`engine/deliverable_assembler.py`) is
# FROZEN by the merged G-3 A-20/A-21 pin (tests/test_g3_decision_value.py), so
# this candidate does not modify it. The additive nested key is composed at the
# web deliverable seam instead — the same precedent the W2-A decision-capture
# view already follows on that surface — from this pure builder. It returns
# None whenever no CURRENT quantified requirement exists, so a project with
# zero quantities adds NO package key.
QUANTIFIED_REQUIREMENTS_META_KEY = "quantified_requirements"
QUANTIFIED_REQUIREMENTS_TITLE = "Quantities you recorded"
QUANTIFIED_REQUIREMENTS_NOTE = (
    "These values were entered by the inventor for the listed requirements. "
    "They are recorded as stated and have not been checked, validated, or "
    "assessed for feasibility, safety, or compliance.")
QUANTITY_PROVENANCE_PUBLIC = "Recorded by the inventor (not yet verified)"


def quantified_requirements_meta(state):
    """Presentation-ready rows for the CURRENT quantified requirements of
    ``state`` (JSON-safe dict), or ``None`` when there are none — the caller
    then adds no key. Canonical STORED tokens only (bound token / decimal text
    / unit code); localized display labels are resolved by the template
    through the ui_text catalogue. No internal identifier is exported and no
    feasibility / validation / safety / compliance claim is made."""
    rows = derive_quantified_requirements(state)
    if not rows:
        return None
    return {
        "title": QUANTIFIED_REQUIREMENTS_TITLE,
        "note": QUANTIFIED_REQUIREMENTS_NOTE,
        "total": len(rows),
        "items": [
            {
                "statement": row.statement,
                "bound": row.quantity.bound,
                "value": row.quantity.value,
                "unit": row.quantity.unit,
                "provenance": QUANTITY_PROVENANCE_PUBLIC,
            }
            for row in rows
        ],
    }


def derive_quantified_requirements(state) -> Tuple[QuantifiedRequirement, ...]:
    """The CURRENT quantified requirements of ``state``: every eligible anchor
    that has an ACTIVE quantity in ``state.requirement_quantities`` (an
    already-validated history attached by the web/store layer; absent or
    empty means no quantities). Rows whose anchor is no longer eligible are
    deliberately omitted — that is the deterministic "superseded anchor is
    inactive" rule. Pure, read-only, stable order (landscape order)."""
    history = getattr(state, "requirement_quantities", None) or ()
    if not history:
        return ()
    active = active_quantities(history)
    rows = []
    for req, record in eligible_anchors(state):
        quantity = active.get(record.record_id)
        if quantity is None:
            continue
        rows.append(QuantifiedRequirement(
            anchor_record_id=record.record_id,
            statement=req.statement,
            quantity=quantity))
    return tuple(rows)
