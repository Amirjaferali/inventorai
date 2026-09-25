"""Commercial Evidence Owner — durable ownership for future Commercial Readiness.

`COMMERCIAL-EVIDENCE-OWNER-IMPLEMENT-01` (Owner-authorized), adopting
`READINESS-OWNER-DISPOSITION-01` recommendation B. This module creates the
EVIDENCE OWNER ONLY. It is emphatically NOT:

  * a readiness engine — nothing here computes, stores or renders a readiness
    status, and the authorized disposition vocabulary (PASS /
    PASS_WITH_CONDITIONS / HOLD / INSUFFICIENT_EVIDENCE) appears nowhere in
    this lane;
  * a second evidence engine — the canonical provenance axis is imported from
    `engine.idea_state`, never redefined;
  * a second risk store — commercial RISK is deliberately absent from the topic
    vocabulary and continues to belong to the canonical risk owner
    (`RequirementLandscape.risks` / `GroundedRisk`). A recorded evidence item
    may DESCRIBE a condition in its own words; it never becomes a risk record;
  * a decision owner — FDC-001 / `DecisionRecord` remains canonical for
    decisions, and nothing here makes an investment, funding or go/no-go call;
  * a commercial conclusion — storing a statement never makes demand, price,
    willingness to pay or market fit validated, and no code path promotes one.

Storage shape (Owner instruction §2): ONE shared append-only readiness-evidence
table carrying an explicit `dimension`, so Manufacturing may reuse the same
substrate later WITHOUT a schema redesign. Only the COMMERCIAL dimension is
ACTIVATED at the time this module was written: `TOPICS_BY_DIMENSION` gave
Manufacturing an EMPTY vocabulary, so no manufacturing row could validate.
`MANUFACTURING-EVIDENCE-OWNER-IMPLEMENT-01` has since supplied that vocabulary
and activated the dimension, so BOTH are now live evidence dimensions on this
one table. Activation is of EVIDENCE OWNERSHIP only: Manufacturing Readiness
evaluation remains unauthorized, and the Readiness Snapshot still gives
Manufacturing no disposition of any kind.

Append-only discipline, mirroring the merged T2-E precedent exactly: per-project
sequence assigned by the store, generated identifier, unique event key, a
single-target supersession edge, withdrawal expressed ONLY as a superseding
row, and no UPDATE path anywhere. Nothing is repaired, deleted, rewritten or
re-normalized.

Evidence strength: this module reuses the canonical provenance axis and carries
exactly ONE claim status, `UNVALIDATED`. That is the merged single-value
discipline (precedents: `requirement_quantity.QUANTITY_VALIDATION_STATUS`,
`evidence_reference.CLAIM_STATUS_UNVALIDATED`) and it exists so no
commercial-specific quality ladder can grow here and no recorded statement can
be promoted by any code path.

Human, customer, survey, interview and market-research COLLECTION are NOT
authorized by the instruction that created this module. The provenance axis is
reused in full so such evidence can later be REPRESENTED without a schema
redesign; representing a provenance value is not collecting it.
"""
import decimal
import re
from dataclasses import dataclass
from typing import Optional

from engine.idea_state import (
    OWNER_STATED,
    PROVENANCE_VALUES as _CANONICAL_PROVENANCE_VALUES,
)


class CommercialEvidenceError(ValueError):
    """Fail-closed validation error. Carries a field name and a reason only —
    never the submitted value, an identifier, or any surrounding state."""


class CommercialEvidenceHistoryError(ValueError):
    """Raised when a loaded evidence history is structurally invalid. A
    populated corrupt history fails CLOSED; zero rows is always valid."""


class EvidenceCapExceeded(CommercialEvidenceError):
    """The per-project cap is an established refusal, never a silent drop."""


# --- Dimensions -------------------------------------------------------------
# The shared substrate structurally supports a second dimension so Manufacturing
# can reuse it later. ACTIVATION is a separate matter from representation:
# `ACTIVE_DIMENSIONS` is what this increment permits a writer to use.
DIMENSION_COMMERCIAL = "COMMERCIAL"
DIMENSION_MANUFACTURING = "MANUFACTURING"
DIMENSIONS = (DIMENSION_COMMERCIAL, DIMENSION_MANUFACTURING)
ACTIVE_DIMENSIONS = (DIMENSION_COMMERCIAL, DIMENSION_MANUFACTURING)

# --- Commercial topic vocabulary (closed; Owner instruction §4) --------------
# Commercial RISK is INTENTIONALLY ABSENT: it routes to the canonical risk
# owner. Adding a risk topic here would create the second risk store that
# §16.F of the Commercial Differentiation Direction prohibits.
TOPIC_TARGET_CUSTOMER = "target_customer"
TOPIC_PROBLEM_SEVERITY = "problem_severity"
TOPIC_MARKET_ALTERNATIVE = "market_alternative"
TOPIC_DIFFERENTIATION = "differentiation"
TOPIC_PRICE = "price"
TOPIC_WILLINGNESS_TO_PAY = "willingness_to_pay"
TOPIC_DEMAND = "demand"
TOPIC_CUSTOMER_EVIDENCE = "customer_evidence"
TOPIC_MARKET_ENTRY = "market_entry"
TOPIC_CHANNEL = "channel"
TOPIC_LICENSING = "licensing"
TOPIC_REVENUE_MODEL = "revenue_model"
TOPIC_COST_REVENUE_ASSUMPTION = "cost_revenue_assumption"
TOPIC_FUNDING_NEED = "funding_need"
TOPIC_FIRST_SALE_VIABILITY = "first_sale_viability"

COMMERCIAL_TOPICS = (
    TOPIC_TARGET_CUSTOMER,
    TOPIC_PROBLEM_SEVERITY,
    TOPIC_MARKET_ALTERNATIVE,
    TOPIC_DIFFERENTIATION,
    TOPIC_PRICE,
    TOPIC_WILLINGNESS_TO_PAY,
    TOPIC_DEMAND,
    TOPIC_CUSTOMER_EVIDENCE,
    TOPIC_MARKET_ENTRY,
    TOPIC_CHANNEL,
    TOPIC_LICENSING,
    TOPIC_REVENUE_MODEL,
    TOPIC_COST_REVENUE_ASSUMPTION,
    TOPIC_FUNDING_NEED,
    TOPIC_FIRST_SALE_VIABILITY,
)

# --- Manufacturing topics (MANUFACTURING-EVIDENCE-OWNER-IMPLEMENT-01) --------
# The closed Manufacturing vocabulary. Reconciled at authorization against the
# nearest recorded design — the standing Owner product direction in the Deferred
# Obligations Register, which names in prose "materials, components,
# specifications, safety, cost, supplier, tooling or production" evidence. No
# EXACT prior taxonomy existed anywhere in the repository, so these tokens define
# it rather than rename one.
#
# SAFETY is deliberately absent although the prose direction names it: a
# manufacturing safety concern belongs to the EXISTING safety seam, exactly as
# commercial RISK belongs to the canonical risk owner rather than to a topic
# here. Neither dimension grows a second safety or risk owner by way of a topic
# list. `manufacturing_risk` is likewise not a topic, for the same reason.
#
# These describe WHAT THE INVENTOR RECORDED about making the thing. None of them
# asserts that it can be made, made affordably, or made at all.
TOPIC_PROTOTYPE_MATURITY = "prototype_maturity"
TOPIC_MATERIAL = "material"
TOPIC_COMPONENT = "component"
TOPIC_SPECIFICATION = "specification"
TOPIC_TOLERANCE = "tolerance"
TOPIC_PROCESS = "process"
TOPIC_TOOLING = "tooling"
TOPIC_SUPPLIER = "supplier"
TOPIC_COST = "cost"
TOPIC_MANUFACTURABILITY = "manufacturability"

MANUFACTURING_TOPICS = (
    TOPIC_PROTOTYPE_MATURITY,
    TOPIC_MATERIAL,
    TOPIC_COMPONENT,
    TOPIC_SPECIFICATION,
    TOPIC_TOLERANCE,
    TOPIC_PROCESS,
    TOPIC_TOOLING,
    TOPIC_SUPPLIER,
    TOPIC_COST,
    TOPIC_MANUFACTURABILITY,
)

# Manufacturing is now ACTIVATED as an EVIDENCE dimension: a manufacturing topic
# validates, so a manufacturing row can be written and read. That is ownership of
# evidence and nothing more — it authorizes no Manufacturing Readiness
# evaluation, and the Readiness Snapshot still gives Manufacturing no
# disposition. Recording what you know about making something is not an
# assessment of whether it can be made.
TOPICS_BY_DIMENSION = {
    DIMENSION_COMMERCIAL: COMMERCIAL_TOPICS,
    DIMENSION_MANUFACTURING: MANUFACTURING_TOPICS,
}

# --- D2: bounded quantitative structure -------------------------------------
# APPROXIMATE IS NOT ARBITRARY. A commercial number is recorded only in one of
# three truthful states, and the third is a real answer rather than a failure:
#
#   NONE             no defensible quantitative basis exists. Nothing is stored.
#   EXACT            one value, with a documented basis behind it.
#   ESTIMATED_RANGE  a low and a high value, with a documented basis behind it.
#
# No midpoint is ever derived from a range, no range is ever derived from a
# value, and no value is ever derived from prose. The rules below are the
# reason: a quantified row without a basis type and a rationale is REFUSED, so
# the only way to get a number in is to say where it came from.
VALUE_STATE_NONE = "NONE"
VALUE_STATE_EXACT = "EXACT"
VALUE_STATE_ESTIMATED_RANGE = "ESTIMATED_RANGE"
VALUE_STATES = (VALUE_STATE_NONE, VALUE_STATE_EXACT, VALUE_STATE_ESTIMATED_RANGE)

# Currency is stored SEPARATELY from the amount and is never inferred. USD is
# the default and, today, the only supported value: the field is explicit and
# structured so another currency can be added later without a redesign, and
# nothing here ever converts between currencies.
CURRENCY_USD = "USD"
CURRENCIES = (CURRENCY_USD,)
DEFAULT_CURRENCY = CURRENCY_USD

# What the amount is per. A closed list, because "per unit" and "per month" are
# different claims and free text would let them blur.
VALUE_BASES = (
    "per_unit", "per_month", "per_project", "per_installation", "other",
)

# WHERE the number came from. Closed, because "we estimated it" and "a supplier
# quoted it" are not the same evidence, and a quantified row must name one.
ESTIMATE_BASES = (
    "supplier_quote",
    "comparable_product_price",
    "preliminary_component_cost",
    "manufacturing_cost_estimate",
    "willingness_to_pay_evidence",
    "reference_market_price",
    "owner_assumption",
    "prior_prototype_cost",
    "channel_margin_assumption",
    "other_documented",
)

#: The topics where a MONETARY quantity is a truthful thing to record. Every
#: other topic — Commercial or Manufacturing — must stay `VALUE_STATE_NONE`.
#:
#: `demand` is deliberately absent: it wants an observation COUNT, not money,
#: and forcing it through a currency-bearing model would misdescribe it.
#: `market_entry` and `first_sale_viability` are deliberately absent too: a
#: target window is a forecast, and this product does not make forecasts.
QUANTIFIABLE_TOPICS = frozenset({
    "price", "willingness_to_pay", "cost_revenue_assumption", "funding_need",
})

# The rationale is bounded like every other owner text. It is NOT in
# TEXT_FIELD_CAPS: that loop runs for every row, and a NONE row must carry an
# EMPTY rationale, which `validate_quantity` asserts directly.
MAX_ESTIMATE_RATIONALE_CHARS = 600
MAX_AMOUNT_DIGITS = 15          # before the decimal point
MAX_AMOUNT_DECIMALS = 2
_AMOUNT_RE = re.compile(r"^(0|[1-9][0-9]{0,%d})(\.[0-9]{1,%d})?$"
                        % (MAX_AMOUNT_DIGITS - 1, MAX_AMOUNT_DECIMALS))


def normalize_amount(text, field):
    """A recorded amount, or the empty string. Never a float, never rounded.

    Stored as the owner's own digits so nothing is lost to binary floating
    point and nothing is silently reformatted. An empty value is legitimate and
    means NO AMOUNT — it is not zero. Zero itself is a valid amount and is
    stored as ``"0"``, which is why the two can never be confused downstream.

    Anything else — a negative, a thousands separator, a currency symbol, a
    range written as prose, an exponent, whitespace inside — is REFUSED rather
    than parsed, because guessing what a malformed amount meant is exactly the
    invention this slice exists to prevent."""
    if text is None:
        return ""
    if not isinstance(text, str):
        raise CommercialEvidenceError("%s: must be text" % field)
    stripped = text.strip()
    if not stripped:
        return ""
    if not _AMOUNT_RE.match(stripped):
        raise CommercialEvidenceError("%s: is not a recordable amount" % field)
    return stripped


def is_stored_amount(text):
    """True iff ``text`` is exactly what `normalize_amount` would have stored."""
    if not isinstance(text, str):
        return False
    return text == "" or bool(_AMOUNT_RE.match(text))


def _amount_value(text):
    """Decimal comparison of two stored amounts. Never used for arithmetic on
    the owner's numbers — only to check that a low is not above a high."""
    return decimal.Decimal(text)


def validate_quantity(row):
    """Every quantitative rule for ONE row, or a refusal. Returns the row.

    The whole point is what it REFUSES. A range with no basis, a value on a
    topic that has no money in it, an amount with no currency, a high below a
    low, a leftover min on an EXACT row: each is a way a number could arrive
    without anyone having stood behind it, and each is rejected rather than
    normalised into something plausible."""
    state = row.value_state
    if state not in VALUE_STATES:
        raise CommercialEvidenceError("value_state: unknown state")
    for field in ("value_exact", "value_min", "value_max"):
        if not is_stored_amount(getattr(row, field)):
            raise CommercialEvidenceError("%s: is not a stored amount" % field)

    if state == VALUE_STATE_NONE:
        # NOTHING may linger. A NONE row that still carried a currency or a
        # stale min would read as "no value" while holding one.
        for field in ("value_exact", "value_min", "value_max", "currency",
                      "value_basis", "estimate_basis", "estimate_rationale"):
            if getattr(row, field) != "":
                raise CommercialEvidenceError(
                    "%s: must be empty when no value is recorded" % field)
        return row

    # From here the row CLAIMS a number, so every support it needs is required.
    if row.topic not in QUANTIFIABLE_TOPICS:
        raise CommercialEvidenceError(
            "value_state: this topic records no monetary quantity")
    if row.currency not in CURRENCIES:
        raise CommercialEvidenceError("currency: unsupported currency")
    if row.value_basis not in VALUE_BASES:
        raise CommercialEvidenceError("value_basis: unknown basis")
    # NO BASIS -> NONE. This is the rule that makes the other rules mean
    # something: without it an estimate could enter with nothing behind it.
    if row.estimate_basis not in ESTIMATE_BASES:
        raise CommercialEvidenceError("estimate_basis: unknown basis type")
    if not is_stored_text(row.estimate_rationale, "estimate_rationale",
                          MAX_ESTIMATE_RATIONALE_CHARS) or \
            not row.estimate_rationale.strip():
        raise CommercialEvidenceError("estimate_rationale: is empty")

    if state == VALUE_STATE_EXACT:
        if not row.value_exact:
            raise CommercialEvidenceError("value_exact: is empty")
        if row.value_min or row.value_max:
            raise CommercialEvidenceError(
                "value_min/value_max: an exact value carries no range")
        return row

    # ESTIMATED_RANGE
    if not row.value_min or not row.value_max:
        raise CommercialEvidenceError("value_min/value_max: a range needs both")
    if row.value_exact:
        raise CommercialEvidenceError(
            "value_exact: a range carries no exact value")
    if _amount_value(row.value_min) > _amount_value(row.value_max):
        raise CommercialEvidenceError("value_min: is above value_max")
    return row


# --- Evidence strength ------------------------------------------------------
# ONE value, deliberately (see the module docstring). Because the writer has no
# second value available, no code path can promote a recorded statement, and
# this can never grow into a competing validation ladder.
CLAIM_STATUS_UNVALIDATED = "UNVALIDATED"
CLAIM_STATUSES = (CLAIM_STATUS_UNVALIDATED,)

# The canonical provenance axis, reused unchanged from its single owner
# (`engine.idea_state.PROVENANCE_VALUES`, the same five values in the same
# order). The default is the only value any writer can reach today: nothing in
# this increment collects specialist or external evidence.
PROVENANCE_VALUES = _CANONICAL_PROVENANCE_VALUES
DEFAULT_PROVENANCE = OWNER_STATED

# --- Bounded owner text policy ----------------------------------------------
# Text only; outer whitespace stripped only; C0/C1 controls rejected; over the
# per-field cap rejected. Nothing is parsed, converted, collapsed, normalized,
# localized, logged or reinterpreted.
MAX_SUBJECT_TEXT_CHARS = 200
MAX_STATEMENT_TEXT_CHARS = 2000
MAX_SOURCE_IDENTITY_CHARS = 200
MAX_SCOPE_TEXT_CHARS = 600
MAX_LIMITATION_TEXT_CHARS = 600
_CONTROL_RE = re.compile(r"[\x00-\x1f\x7f-\x9f]")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# A bounded per-project cap, mirroring the merged T2-A / T2-E precedent.
MAX_READINESS_EVIDENCE_PER_PROJECT = 200

# Durable outcome tokens (mirroring the merged store vocabulary).
EVIDENCE_INSERTED = "INSERTED"
EVIDENCE_EXACT_REPLAY = "EXACT_REPLAY"


def normalize_text(text, field, cap):
    """Apply the bounded owner-text policy and return the stored form, or raise.
    Deterministic and idempotent; the text is never placed in the exception."""
    if not isinstance(text, str):
        raise CommercialEvidenceError("%s: must be text" % field)
    stripped = text.strip()
    if not stripped:
        raise CommercialEvidenceError("%s: is empty" % field)
    if _CONTROL_RE.search(stripped):
        raise CommercialEvidenceError("%s: contains control characters" % field)
    if len(stripped) > cap:
        raise CommercialEvidenceError("%s: is too long" % field)
    return stripped


def normalize_optional_date(text):
    """``occurred_on`` is the evidence date WHERE KNOWN. An empty value is
    legitimate — much commercial evidence carries no single date — and is stored
    as the empty string. A supplied value must be an exact ISO calendar date; no
    value is ever inferred, defaulted to today, or reformatted."""
    if text is None:
        return ""
    if not isinstance(text, str):
        raise CommercialEvidenceError("occurred_on: must be text")
    stripped = text.strip()
    if not stripped:
        return ""
    if not _DATE_RE.match(stripped):
        raise CommercialEvidenceError("occurred_on: must be an ISO date")
    return stripped


def validate_dimension(dimension, active_only=True):
    """Return ``dimension`` iff it is representable and (by default) ACTIVATED.
    A structurally representable but unactivated dimension — Manufacturing today
    — is refused for writes, which is what keeps this increment Commercial-only."""
    if dimension not in DIMENSIONS:
        raise CommercialEvidenceError("dimension: unknown dimension")
    if active_only and dimension not in ACTIVE_DIMENSIONS:
        raise CommercialEvidenceError("dimension: not activated")
    return dimension


def validate_topic(dimension, topic):
    """Return ``topic`` iff it belongs to the closed vocabulary of ``dimension``.
    Manufacturing's vocabulary is empty, so every manufacturing topic fails."""
    if topic not in TOPICS_BY_DIMENSION.get(dimension, ()):
        raise CommercialEvidenceError("topic: not a topic of this dimension")
    return topic


def normalize_optional_link(value):
    """The stored form of a supporting-item reference: an exact identifier, or
    ``None`` meaning NO LINK.

    Empty, blank and ``None`` all mean the same ordinary thing — the owner named
    no supporting item — so they collapse to ``None`` rather than to an empty
    string that would later read as "a link to nothing". A non-empty value is
    kept EXACTLY as given: an identifier is not text to be tidied, and repairing
    one would be inventing a reference the owner did not make."""
    if value is None:
        return None
    if not isinstance(value, str):
        raise CommercialEvidenceError("supporting_evidence_id: must be text")
    if not value.strip():
        return None
    if value != value.strip():
        raise CommercialEvidenceError(
            "supporting_evidence_id: is not a stored value")
    return value


def is_stored_link(value):
    """True iff ``value`` is EXACTLY the stored form of a supporting link. The
    rule is asked, never re-stated."""
    try:
        return normalize_optional_link(value) == value
    except CommercialEvidenceError:
        return False


@dataclass(frozen=True)
class ReadinessEvidence:
    """One immutable, append-only owner-recorded readiness-evidence item.

    ``withdrawn`` is carried by a SUPERSEDING row, never written onto an
    existing one: the durable table has no UPDATE path, exactly like the
    INSERT-only records, quantity, reference and adoption tables.

    There is deliberately NO assertion anchor: commercial evidence is about the
    market, not about an answer to a served invention question, so requiring an
    anchor would make most of the vocabulary unrecordable.

    ``evidence_seq`` is assigned by the store on append; the caller's value is
    ignored. ``recorded_iteration`` / ``recorded_at`` are recording facts and
    are never part of event identity."""
    evidence_id: str
    evidence_seq: int
    dimension: str
    topic: str
    subject_text: str
    statement_text: str
    source_identity: str
    provenance: str
    occurred_on: str
    scope_text: str
    limitation_text: str
    claim_status: str
    withdrawn: bool
    supersedes_evidence_id: Optional[str]
    event_key: str
    recorded_iteration: int
    recorded_at: str
    # D2 quantitative structure. Every field defaults to the empty/NONE state,
    # so every row written before this slice stays valid and stays honest: no
    # value, no currency, no basis, nothing inferred for it afterwards.
    value_state: str = VALUE_STATE_NONE
    value_exact: str = ""
    value_min: str = ""
    value_max: str = ""
    currency: str = ""
    value_basis: str = ""
    estimate_basis: str = ""
    estimate_rationale: str = ""
    # D3 linkage. The SECOND edge this row may carry, and deliberately not the
    # first: `supersedes_evidence_id` says "this REPLACES that item",
    # `supporting_evidence_id` says "that item SUPPORTS this one". They are
    # different claims, so they are different columns and a row may never point
    # both at the same item. NULL is the ordinary state and means exactly no
    # supporting item was named — never "unknown support" and never "unsupported
    # therefore weaker". A link is a traversal, not a rating: it changes no
    # status, no provenance and no readiness anywhere.
    supporting_evidence_id: Optional[str] = None


CANONICAL_ROW_FIELDS = tuple(ReadinessEvidence.__dataclass_fields__)

# The fields that define WHAT the owner recorded. Two events with the same
# canonical identity are the same event; the recording facts (iteration, time,
# sequence, generated id) are never part of it.
_IDENTITY_FIELDS = (
    "dimension", "topic", "subject_text", "statement_text", "source_identity",
    "provenance", "occurred_on", "scope_text", "limitation_text",
    "claim_status", "withdrawn", "supersedes_evidence_id", "event_key",
    # The quantity IS part of what the owner recorded: two rows that differ
    # only in the amount are different events, not a replay of one another.
    "value_state", "value_exact", "value_min", "value_max", "currency",
    "value_basis", "estimate_basis", "estimate_rationale",
    # Likewise the supporting link: naming a different supporting item is a
    # different statement about the same words, not a replay of one of them.
    "supporting_evidence_id",
)


def make_readiness_evidence(*, evidence_id, evidence_seq, dimension, topic,
                            subject_text, statement_text, source_identity,
                            occurred_on=None, scope_text, limitation_text,
                            provenance=DEFAULT_PROVENANCE, withdrawn=False,
                            supersedes_evidence_id=None, event_key,
                            recorded_iteration, recorded_at,
                            value_state=VALUE_STATE_NONE, value_exact=None,
                            value_min=None, value_max=None, currency="",
                            value_basis="", estimate_basis="",
                            estimate_rationale="",
                            supporting_evidence_id=None):
    """Build ONE validated canonical row, or raise ``CommercialEvidenceError``.

    Conservative by construction: ``claim_status`` is the single UNVALIDATED
    value and is not a parameter, so no caller can record a stronger claim, and
    a withdrawal must name the row it supersedes."""
    validate_dimension(dimension)
    validate_topic(dimension, topic)
    if provenance not in PROVENANCE_VALUES:
        raise CommercialEvidenceError("provenance: unknown provenance")
    if withdrawn and not supersedes_evidence_id:
        raise CommercialEvidenceError(
            "withdrawn: a withdrawal must supersede an existing item")
    # Both rule sets are asked ONCE, here and at the durable boundary, so the
    # sanctioned constructor and the store cannot drift apart on either edge.
    return validate_link(validate_quantity(ReadinessEvidence(
        evidence_id=evidence_id,
        evidence_seq=evidence_seq,
        dimension=dimension,
        topic=topic,
        subject_text=normalize_text(subject_text, "subject_text",
                                    MAX_SUBJECT_TEXT_CHARS),
        statement_text=normalize_text(statement_text, "statement_text",
                                      MAX_STATEMENT_TEXT_CHARS),
        source_identity=normalize_text(source_identity, "source_identity",
                                       MAX_SOURCE_IDENTITY_CHARS),
        provenance=provenance,
        occurred_on=normalize_optional_date(occurred_on),
        scope_text=normalize_text(scope_text, "scope_text",
                                  MAX_SCOPE_TEXT_CHARS),
        limitation_text=normalize_text(limitation_text, "limitation_text",
                                       MAX_LIMITATION_TEXT_CHARS),
        claim_status=CLAIM_STATUS_UNVALIDATED,
        withdrawn=bool(withdrawn),
        supersedes_evidence_id=supersedes_evidence_id,
        event_key=event_key,
        recorded_iteration=recorded_iteration,
        recorded_at=recorded_at,
        # Amounts are normalised (or refused) here; every quantitative RULE is
        # then asked once, by `validate_quantity` below, so the constructor and
        # the durable boundary cannot drift apart.
        value_state=value_state,
        value_exact=normalize_amount(value_exact, "value_exact"),
        value_min=normalize_amount(value_min, "value_min"),
        value_max=normalize_amount(value_max, "value_max"),
        currency=currency,
        value_basis=value_basis,
        estimate_basis=estimate_basis,
        # Empty is legitimate here and means NO RATIONALE, which is only ever
        # valid on a NONE row — `validate_quantity` refuses it on any row that
        # claims a number, so emptiness cannot become a way past the basis rule.
        estimate_rationale=("" if not (estimate_rationale or "").strip()
                            else normalize_text(
                                estimate_rationale, "estimate_rationale",
                                MAX_ESTIMATE_RATIONALE_CHARS)),
        # An empty submission means NO LINK, which is an ordinary answer. The
        # id itself is never parsed, trimmed into shape or repaired: whatever
        # survives here must name a real item of this project's own history,
        # and `validate_new_evidence` is what asks that question.
        supporting_evidence_id=normalize_optional_link(supporting_evidence_id),
    )))


def canonical_evidence_dict(evidence):
    """JSON-safe canonical row. Presentation adds nothing and removes nothing."""
    return {field: getattr(evidence, field) for field in CANONICAL_ROW_FIELDS}


def is_same_evidence_event(stored, candidate):
    """True iff two rows are the SAME canonical event (identity fields only)."""
    return all(getattr(stored, f) == getattr(candidate, f)
               for f in _IDENTITY_FIELDS)


def is_stored_text(text, field, cap):
    """True iff ``text`` is EXACTLY the stored (post-policy) form for ``field``.

    This is the SAME bounded policy `normalize_text` applies — it is asked, not
    re-implemented — so the store boundary can reject text that never passed
    through the sanctioned constructor without creating a second normalization
    policy."""
    try:
        return normalize_text(text, field, cap) == text
    except CommercialEvidenceError:
        return False


def is_stored_date(text):
    """True iff ``text`` is EXACTLY the stored form of ``occurred_on``: the
    ISO-shaped date the owner's existing rule accepts, or the empty string when
    no date is known. The shape rule is asked, never re-stated."""
    try:
        return normalize_optional_date(text) == text
    except CommercialEvidenceError:
        return False


#: Every bounded text field with its cap, in canonical row order.
TEXT_FIELD_CAPS = (
    ("subject_text", MAX_SUBJECT_TEXT_CHARS),
    ("statement_text", MAX_STATEMENT_TEXT_CHARS),
    ("source_identity", MAX_SOURCE_IDENTITY_CHARS),
    ("scope_text", MAX_SCOPE_TEXT_CHARS),
    ("limitation_text", MAX_LIMITATION_TEXT_CHARS),
)


def validate_evidence_row(row):
    """Validate ONE canonical row against every owner rule, and return it.

    This is the rule set the sanctioned constructor enforces, expressed so the
    STORE can enforce it independently: a caller that builds a
    ``ReadinessEvidence`` directly — bypassing ``make_readiness_evidence`` —
    is refused at the durable boundary rather than committing a row the
    loader would later reject. It creates no new policy: the dimension,
    topic, provenance, claim-status and bounded-text rules are the module's
    own, asked here a second time.

    Raises ``CommercialEvidenceError``; never mutates or repairs the row."""
    if not isinstance(row, ReadinessEvidence):
        raise CommercialEvidenceError("row: must be a ReadinessEvidence")
    validate_dimension(row.dimension)
    validate_topic(row.dimension, row.topic)
    if row.provenance not in PROVENANCE_VALUES:
        raise CommercialEvidenceError("provenance: unknown provenance")
    if row.claim_status not in CLAIM_STATUSES:
        raise CommercialEvidenceError("claim_status: unknown claim status")
    for field, cap in TEXT_FIELD_CAPS:
        if not is_stored_text(getattr(row, field), field, cap):
            raise CommercialEvidenceError("%s: is not a stored value" % field)
    if not is_stored_date(row.occurred_on):
        raise CommercialEvidenceError("occurred_on: is not a stored value")
    if not isinstance(row.event_key, str) or not row.event_key.strip():
        raise CommercialEvidenceError("event_key: is empty")
    if not isinstance(row.evidence_id, str) or not row.evidence_id.strip():
        raise CommercialEvidenceError("evidence_id: is empty")
    if row.supersedes_evidence_id == row.evidence_id:
        raise CommercialEvidenceError(
            "supersedes_evidence_id: a row cannot supersede itself")
    if row.withdrawn and not row.supersedes_evidence_id:
        raise CommercialEvidenceError(
            "withdrawn: a withdrawal must supersede an existing item")
    validate_link(row)
    validate_quantity(row)
    return row


def validate_link(row):
    """The supporting-link rules that ONE row can answer by itself, and return
    the row. Whether the named item exists, is of this project and is of this
    dimension is a question about the HISTORY, so it is asked there.

    Fails closed on every violation and repairs nothing: an invalid link is
    refused, never quietly dropped to NO LINK, because silently discarding the
    reference the owner chose would leave an item looking deliberately
    unsupported when in fact its support was thrown away."""
    if not is_stored_link(row.supporting_evidence_id):
        raise CommercialEvidenceError(
            "supporting_evidence_id: is not a stored value")
    if row.supporting_evidence_id is None:
        return row
    if row.supporting_evidence_id == row.evidence_id:
        raise CommercialEvidenceError(
            "supporting_evidence_id: an item cannot support itself")
    # The two edges are different claims and must stay distinguishable. "This
    # replaces that" and "that supports this" cannot both be true of one pair:
    # an item does not become the evidence for its own replacement.
    if row.supersedes_evidence_id is not None \
            and row.supporting_evidence_id == row.supersedes_evidence_id:
        raise CommercialEvidenceError(
            "supporting_evidence_id: cannot also be the superseded item")
    return row


def validate_evidence_history(rows):
    """Structural validation of ONE project's rows in sequence order.

    Valid when every row carries an activated dimension and a topic of that
    dimension, every ``supersedes_evidence_id`` names an EARLIER row of the same
    project exactly once (no fork), no row supersedes itself, and every
    withdrawal supersedes something. An empty history is valid. Raises
    ``CommercialEvidenceHistoryError`` with a structural message only."""
    rows = list(rows)
    seen = {}
    superseded = set()
    for row in rows:
        if row.evidence_id in seen:
            raise CommercialEvidenceHistoryError("duplicate evidence id")
        # Every stored row must still satisfy the owner's own row rules —
        # dimension, topic, PROVENANCE, claim status and the bounded text
        # policy. A history is never "valid enough": a row that could not be
        # written today must not be readable as canonical history either.
        try:
            validate_evidence_row(row)
        except CommercialEvidenceError as exc:
            raise CommercialEvidenceHistoryError(str(exc))
        prior = row.supersedes_evidence_id
        if prior is not None:
            if prior == row.evidence_id:
                raise CommercialEvidenceHistoryError("row supersedes itself")
            if prior not in seen:
                raise CommercialEvidenceHistoryError(
                    "superseded item is not an earlier item")
            if prior in superseded:
                raise CommercialEvidenceHistoryError(
                    "superseded item already has a successor")
            superseded.add(prior)
        elif row.withdrawn:
            raise CommercialEvidenceHistoryError(
                "a withdrawal must supersede an existing item")
        seen[row.evidence_id] = row
    _validate_supporting_links(rows, seen)
    return tuple(rows)


def _validate_supporting_links(rows, by_id):
    """Every supporting link must name a real item of THIS project's own
    dimension, and the links must not run in a circle.

    Cross-project is answered by the same question as "does it exist": the
    store loads one project's rows, so an item of another project is simply not
    here and the history fails closed rather than reaching across.

    Circularity is checked even though the write path cannot create it — a
    candidate may only point at an item that ALREADY exists — because this
    validator also reads histories it did not write, and a loop would otherwise
    be a durable, silently traversable lie."""
    for row in rows:
        target_id = row.supporting_evidence_id
        if target_id is None:
            continue
        target = by_id.get(target_id)
        if target is None:
            raise CommercialEvidenceHistoryError(
                "supporting item is not an item of this project")
        if target.dimension != row.dimension:
            raise CommercialEvidenceHistoryError(
                "supporting item belongs to a different dimension")
    for row in rows:
        seen_ids, cursor, limit = set(), row, len(rows) + 1
        while cursor.supporting_evidence_id is not None:
            if cursor.evidence_id in seen_ids or limit <= 0:
                raise CommercialEvidenceHistoryError("supporting link cycle")
            seen_ids.add(cursor.evidence_id)
            limit -= 1
            cursor = by_id[cursor.supporting_evidence_id]


def evidence_index(rows):
    """``{evidence_id: row}`` over one project's WHOLE history. Pure."""
    return {r.evidence_id: r for r in rows}


def supporting_item(rows, evidence):
    """The item named as supporting ``evidence``, or ``None`` when it names
    none.

    Resolved against the FULL history, not the current items, because a
    supporting item that has since been corrected or withdrawn is still exactly
    the item this row was recorded against. Silently dropping the link once its
    target stopped being current would rewrite what the owner said.

    Pure. Returns a row; it derives no status, strength or conclusion from the
    fact that a link exists."""
    if evidence.supporting_evidence_id is None:
        return None
    return evidence_index(rows).get(evidence.supporting_evidence_id)


def superseded_ids(rows):
    """Every id that a later row replaces."""
    return {r.supersedes_evidence_id for r in rows
            if r.supersedes_evidence_id is not None}


def validate_new_evidence(existing_rows, candidate):
    """Validate ``candidate`` against a VALID existing history. Raises on any
    violation; the caller writes nothing when this raises."""
    rows = validate_evidence_history(existing_rows)
    by_id = {r.evidence_id: r for r in rows}
    if candidate.evidence_id in by_id:
        raise CommercialEvidenceError("evidence_id: already exists")
    if any(r.event_key == candidate.event_key for r in rows):
        raise CommercialEvidenceError("event_key: already exists")
    validate_evidence_row(candidate)
    support_id = candidate.supporting_evidence_id
    if support_id is not None:
        support = by_id.get(support_id)
        # An item can only be supported by something that is ALREADY recorded.
        # This is what makes a cross-project or invented reference impossible
        # rather than merely unlikely: the candidate is checked against this
        # project's own durable history and nothing else.
        if support is None:
            raise CommercialEvidenceError(
                "supporting_evidence_id: unknown item")
        if support.dimension != candidate.dimension:
            raise CommercialEvidenceError(
                "supporting_evidence_id: belongs to a different dimension")
    prior_id = candidate.supersedes_evidence_id
    if prior_id is None:
        if candidate.withdrawn:
            raise CommercialEvidenceError(
                "withdrawn: a withdrawal must supersede an existing item")
        return candidate
    prior = by_id.get(prior_id)
    if prior is None:
        raise CommercialEvidenceError("supersedes_evidence_id: unknown item")
    if prior.dimension != candidate.dimension:
        raise CommercialEvidenceError(
            "supersedes_evidence_id: belongs to a different dimension")
    if prior_id in superseded_ids(rows):
        raise CommercialEvidenceError(
            "supersedes_evidence_id: that item is already superseded")
    return candidate


# --- Read owner -------------------------------------------------------------
def evidence_for_dimension(rows, dimension):
    """Every row of one dimension, in append order. Pure."""
    return tuple(r for r in validate_evidence_history(rows)
                 if r.dimension == dimension)


def active_evidence(rows, dimension=DIMENSION_COMMERCIAL):
    """The CURRENT items of one dimension: every row that no later row
    supersedes and that is not itself a withdrawal. A withdrawn chain therefore
    contributes NOTHING to the active set while every row of it is retained in
    history. Pure; derives no status and no conclusion."""
    scoped = evidence_for_dimension(rows, dimension)
    replaced = superseded_ids(scoped)
    return tuple(r for r in scoped
                 if r.evidence_id not in replaced and not r.withdrawn)


def evidence_chain(rows, evidence_id):
    """The full lineage containing ``evidence_id``, oldest first. Pure."""
    scoped = validate_evidence_history(rows)
    by_id = {r.evidence_id: r for r in scoped}
    if evidence_id not in by_id:
        return ()
    root = by_id[evidence_id]
    while root.supersedes_evidence_id is not None:
        root = by_id[root.supersedes_evidence_id]
    successors = {r.supersedes_evidence_id: r for r in scoped
                  if r.supersedes_evidence_id is not None}
    chain, node = [root], root
    while node.evidence_id in successors:
        node = successors[node.evidence_id]
        chain.append(node)
    return tuple(chain)


# The lifecycle state of ONE row, as the existing append-only model already
# determines it. These are names for states the owner has always had; no new
# lifecycle, no new stored field and no new vocabulary is introduced.
LIFECYCLE_CURRENT = "current"        # nothing supersedes it, it is not a withdrawal
LIFECYCLE_REPLACED = "replaced"      # a later row supersedes it
LIFECYCLE_WITHDRAWN = "withdrawn"    # it IS the withdrawal row of its chain
LIFECYCLE_STATES = (LIFECYCLE_CURRENT, LIFECYCLE_REPLACED, LIFECYCLE_WITHDRAWN)


def evidence_lifecycle(rows, dimension):
    """Every row of one dimension in append order, each labelled with the
    lifecycle state the EXISTING model already implies. Pure.

    Returns a tuple of ``(row, state, replaces_id)``, oldest first, where
    ``state`` is one of ``LIFECYCLE_STATES`` and ``replaces_id`` is the row this
    one supersedes, or None. Nothing is recomputed: ``replaced`` is read from
    the same ``superseded_ids`` that ``active_evidence`` reads, and
    ``withdrawn`` is the stored flag.

    What it is NOT:

      * NOT a second lifecycle. It renames nothing and decides nothing; a caller
        that ignored it entirely would get the same active set as before.
      * NOT a judgement. A replaced row is not wrong and a withdrawn one is not
        a failure; both are what the owner said at the time, kept because the
        ledger is append-only.
      * NOT ordered by importance. Append order is the owner's own order, and
        it carries no ranking, score or recency preference.
      * NOT a validation signal. Every row still carries the one frozen claim
        status, and nothing here can change it."""
    scoped = evidence_for_dimension(rows, dimension)
    replaced = superseded_ids(scoped)
    out = []
    for row in scoped:
        if row.withdrawn:
            state = LIFECYCLE_WITHDRAWN
        elif row.evidence_id in replaced:
            state = LIFECYCLE_REPLACED
        else:
            state = LIFECYCLE_CURRENT
        out.append((row, state, row.supersedes_evidence_id))
    return tuple(out)


def evidence_view(rows, dimension):
    """The minimum READ projection for ONE dimension of one project's evidence.

    Returns ``{"total", "active", "topics"}`` where ``active`` is the canonical
    rows of that dimension's current items in append order and ``topics`` is the
    sorted set of topics those items cover. It reports WHAT WAS RECORDED and
    nothing more: no readiness status, no disposition token, no score, no
    percentage, no sufficiency judgement, and no claim that any recorded
    statement is validated. An empty project yields ``total`` 0 with an empty
    active tuple — the truthful absence, stated by the caller in the caller's own
    words.

    Scoped by dimension, so a Commercial view can never show a Manufacturing row
    and vice versa: the isolation is a property of this projection rather than a
    convention the callers are trusted to keep."""
    active = active_evidence(rows, dimension)
    return {
        "total": len(active),
        "active": tuple(canonical_evidence_dict(r) for r in active),
        "topics": tuple(sorted({r.topic for r in active})),
    }


def uncovered_topics(dimension, view):
    """The governed topics of ONE dimension that its CURRENT view does not cover.

    Pure set arithmetic over two things that already exist: the governed
    vocabulary of `dimension`, and the topics the canonical view reports as
    covered. It reads no store, writes nothing, and adds no state.

    What it is NOT, each true by construction rather than by convention:

      * NOT a second source of truth. The vocabulary and the view are both the
        existing owner's; this returns the difference and holds nothing.
      * NOT a judgement. An uncovered topic means no evidence has been RECORDED
        for it. It is not a finding about the market, the demand, the viability
        or the idea, and no caller may render it as one.
      * NOT a score, count-based threshold, ranking, weighting or readiness
        signal. The result is a list in the vocabulary's own committed order,
        never sorted by importance, because no importance exists.
      * NOT cross-dimension. `dimension` selects the vocabulary AND the view is
        already dimension-scoped, so a Commercial gap can never be computed from
        Manufacturing coverage or the reverse.

    Coverage is derived from ACTIVE rows, so the two lifecycle acts differ and
    the difference matters. A WITHDRAWAL can make a topic uncovered again, when
    no active row remains for it. A CORRECTION/SUPERSESSION replaces the old row
    with its active replacement, so coverage REMAINS when that replacement
    carries the same topic — supersession alone never uncovers a topic.

    Order is the committed vocabulary order, so the caller renders a stable list
    and no ordering can be read as priority."""
    if dimension not in TOPICS_BY_DIMENSION:
        raise ValueError("unknown evidence dimension: %r" % (dimension,))
    covered = set(view["topics"])
    return tuple(t for t in TOPICS_BY_DIMENSION[dimension] if t not in covered)


def commercial_evidence_view(rows):
    """The Commercial projection. Unchanged behaviour: the shared `evidence_view`
    is the same code this function always ran, now named once and reused."""
    return evidence_view(rows, DIMENSION_COMMERCIAL)


def manufacturing_evidence_view(rows):
    """The Manufacturing projection — the same projection, other dimension.

    It carries no Manufacturing Readiness meaning whatsoever. A project with ten
    recorded manufacturing items and one with none are both simply projects with
    recorded evidence counts; neither is closer to being manufacturable, because
    nothing here judges that."""
    return evidence_view(rows, DIMENSION_MANUFACTURING)
