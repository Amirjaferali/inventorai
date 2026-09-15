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
ACTIVATED here: `TOPICS_BY_DIMENSION[DIMENSION_MANUFACTURING]` is deliberately
EMPTY, so no manufacturing row can ever validate and therefore no manufacturing
writer exists until a separate Owner authorization supplies that vocabulary.

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
import re
from dataclasses import dataclass
from typing import Optional

from engine.idea_state import (
    EXPERT_SUPPLIED,
    EXTERNAL_EVIDENCE,
    LEGACY_UNSPECIFIED,
    OWNER_STATED,
    SYSTEM_INFERRED,
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
ACTIVE_DIMENSIONS = (DIMENSION_COMMERCIAL,)

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

# Manufacturing is REPRESENTABLE but NOT ACTIVATED: an empty vocabulary means no
# manufacturing topic can validate, so no manufacturing row can be written.
TOPICS_BY_DIMENSION = {
    DIMENSION_COMMERCIAL: COMMERCIAL_TOPICS,
    DIMENSION_MANUFACTURING: (),
}

# --- Evidence strength ------------------------------------------------------
# ONE value, deliberately (see the module docstring). Because the writer has no
# second value available, no code path can promote a recorded statement, and
# this can never grow into a competing validation ladder.
CLAIM_STATUS_UNVALIDATED = "UNVALIDATED"
CLAIM_STATUSES = (CLAIM_STATUS_UNVALIDATED,)

# The canonical provenance axis, reused unchanged. The default is the only value
# any writer can reach today: nothing in this increment collects specialist or
# external evidence.
PROVENANCE_VALUES = (
    OWNER_STATED,
    SYSTEM_INFERRED,
    EXPERT_SUPPLIED,
    EXTERNAL_EVIDENCE,
    LEGACY_UNSPECIFIED,
)
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


CANONICAL_ROW_FIELDS = tuple(ReadinessEvidence.__dataclass_fields__)

# The fields that define WHAT the owner recorded. Two events with the same
# canonical identity are the same event; the recording facts (iteration, time,
# sequence, generated id) are never part of it.
_IDENTITY_FIELDS = (
    "dimension", "topic", "subject_text", "statement_text", "source_identity",
    "provenance", "occurred_on", "scope_text", "limitation_text",
    "claim_status", "withdrawn", "supersedes_evidence_id", "event_key",
)


def make_readiness_evidence(*, evidence_id, evidence_seq, dimension, topic,
                            subject_text, statement_text, source_identity,
                            occurred_on=None, scope_text, limitation_text,
                            provenance=DEFAULT_PROVENANCE, withdrawn=False,
                            supersedes_evidence_id=None, event_key,
                            recorded_iteration, recorded_at):
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
    return ReadinessEvidence(
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
    )


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
    return tuple(rows)


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


def commercial_evidence_view(rows):
    """The minimum READ projection for one project's Commercial evidence.

    Returns ``{"total", "active", "topics"}`` where ``active`` is the canonical
    rows of the current items in append order and ``topics`` is the sorted set
    of topics those items cover. It reports WHAT WAS RECORDED and nothing more:
    no readiness status, no disposition token, no score, no percentage, no
    sufficiency judgement, and no claim that any recorded statement is
    validated. An empty project yields ``total`` 0 with an empty active tuple —
    the truthful absence, stated by the caller in the caller's own words."""
    active = active_evidence(rows, DIMENSION_COMMERCIAL)
    return {
        "total": len(active),
        "active": tuple(canonical_evidence_dict(r) for r in active),
        "topics": tuple(sorted({r.topic for r in active})),
    }
