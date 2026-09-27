"""
IdeaState — MVP data structure only.
Scope: electronics/electrical, LEVEL 0-2.
Governed by: MVP_SCOPE_FREEZE.md
"""

import re
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


# --- Evidence quality ---
ASSERTED    = "ASSERTED"
REASONED    = "REASONED"
DEMONSTRATED = "DEMONSTRATED"

# --- Gap types ---
# Stage 2 gap types (3 only per GD-001 frozen)
PHYSICAL_FEASIBILITY    = "PHYSICAL_FEASIBILITY"
BOUNDARY_AMBIGUITY      = "BOUNDARY_AMBIGUITY"
MECHANISM_COMPLETENESS  = "MECHANISM_COMPLETENESS"

# Stage 3 gap types (per STAGE3_GAP_TAXONOMY_PROPOSAL)
PROBLEM_MECHANISM_FIT   = "PROBLEM_MECHANISM_FIT"
ASSUMPTION_INVENTORY    = "ASSUMPTION_INVENTORY"
EXPERTISE_GAP_AWARENESS = "EXPERTISE_GAP_AWARENESS"

# Stage registry
STAGE_2_GAP_TYPES = {MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY}
STAGE_3_GAP_TYPES = {PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS}

# --- Gap status ---
OPEN          = "OPEN"
PARTIAL       = "PARTIAL"
CLOSED        = "CLOSED"
ACCEPTED_RISK = "ACCEPTED_RISK"

# --- Direction ---
PROGRESSING = "PROGRESSING"
STALLED     = "STALLED"
REGRESSING  = "REGRESSING"


# ===========================================================================
# Increment 2 — Truthful Gap and Evidence State.
#
# Four ORTHOGONAL axes (per the committed EPISTEMIC_FOUNDATION_DESIGN_DECISION
# and INCREMENT_2_AUTHORITY_RULINGS / INCREMENT_2_IMPLEMENTATION_CONTRACT):
#   * Provenance  — where a record came from (capture origin).
#   * Validation  — whether it has been validated, INDEPENDENT of provenance and
#                   of evidence quality (ADR-003 reasoning-structure axis).
#   * Disposition — which of the six owner actions created it.
#   * Responsibility — explicit only when owner-created; otherwise derived.
# These are additive and backward compatible. Provenance and validation are NEVER
# inferred from text, vocabulary, evidence quality, maturity, or gap status: the
# defaults are the truthful "we do not know" values below.
# ===========================================================================

# --- Provenance / source (capture origin) ---
LEGACY_UNSPECIFIED = "LEGACY_UNSPECIFIED"   # default for legacy/unspecified records
OWNER_STATED       = "OWNER_STATED"
SYSTEM_INFERRED    = "SYSTEM_INFERRED"
EXPERT_SUPPLIED    = "EXPERT_SUPPLIED"
EXTERNAL_EVIDENCE  = "EXTERNAL_EVIDENCE"

# --- Validation status (independent of provenance and of evidence quality) ---
UNVALIDATED              = "UNVALIDATED"     # default; never auto-promoted
SPECIALIST_REVIEWED      = "SPECIALIST_REVIEWED"
EMPIRICALLY_DEMONSTRATED = "EMPIRICALLY_DEMONSTRATED"
INDEPENDENTLY_VERIFIED   = "INDEPENDENTLY_VERIFIED"

# --- Responsibility (explicit only when owner-created; else derived/undetermined)
OWNER_INPUT        = "OWNER_INPUT"
SYSTEM_ANALYSIS    = "SYSTEM_ANALYSIS"
SPECIALIST_INPUT   = "SPECIALIST_INPUT"
EMPIRICAL_EVIDENCE = "EMPIRICAL_EVIDENCE"
UNDETERMINED       = "UNDETERMINED"

# --- Provenance Hardening Step 1: closed vocabularies (no new value) --------
# The ONE canonical provenance vocabulary: exactly the five constants above, in
# a fixed order. Every other module reuses this tuple; none re-lists it.
PROVENANCE_VALUES = (
    OWNER_STATED,
    SYSTEM_INFERRED,
    EXPERT_SUPPLIED,
    EXTERNAL_EVIDENCE,
    LEGACY_UNSPECIFIED,
)
# The provenance values legal on the owner-interaction AssertionRecord carrier
# TODAY. SYSTEM_INFERRED, EXPERT_SUPPLIED and EXTERNAL_EVIDENCE stay canonical
# values, but no writer of this carrier may produce them: a system, expert or
# external claim is not an owner interaction, and its carrier is undecided.
ASSERTION_PROVENANCE_VALUES = frozenset({OWNER_STATED, LEGACY_UNSPECIFIED})
# The closed responsibility vocabulary: the five constants above.
RESPONSIBILITY_VALUES = frozenset({
    OWNER_INPUT, SYSTEM_ANALYSIS, SPECIALIST_INPUT, EMPIRICAL_EVIDENCE,
    UNDETERMINED,
})
# The responsibility this carrier stores for each legal provenance: the owner
# is responsible for what the owner stated; otherwise nothing is stored and
# responsibility stays derived at display time. Nothing else is ever inferred
# from provenance.
ASSERTION_RESPONSIBILITY_BY_PROVENANCE = {
    OWNER_STATED: OWNER_INPUT,
    LEGACY_UNSPECIFIED: None,
}

# --- Workstream 4: structured criticality confirmation vocabulary ---------
# (STRUCTURED_CRITICALITY_CAPTURE_INCREMENT_CONTRACT.md §4/§6; C4-R4/C4-R5.)
# Confirmable categories: exactly the three non-UNDETERMINED C4-R4 categories.
# `confirmed + UNDETERMINED` is an invalid combination and is rejected;
# uncertainty must use the `deferred` action, which carries no category.
CRITICALITY_FEASIBILITY_THREATENING = "FEASIBILITY-THREATENING"
CRITICALITY_VALUE_ENHANCING         = "VALUE-ENHANCING"
CRITICALITY_REFINEMENT              = "REFINEMENT"
CONFIRMABLE_CRITICALITY_CATEGORIES = frozenset({
    CRITICALITY_FEASIBILITY_THREATENING,
    CRITICALITY_VALUE_ENHANCING,
    CRITICALITY_REFINEMENT,
})
CRITICALITY_ACTION_CONFIRMED = "confirmed"
CRITICALITY_ACTION_DEFERRED  = "deferred"
CRITICALITY_ACTIONS = frozenset({
    CRITICALITY_ACTION_CONFIRMED, CRITICALITY_ACTION_DEFERRED,
})
# rationale_source vocabulary (contract §6.1): an attributed reuse of an
# existing ledger record, an inventor-edited variant, or freshly typed text.
_RATIONALE_SOURCE_REUSED_PREFIX = "reused_statement:"
_RATIONALE_SOURCE_FIXED = frozenset({"inventor_edited", "inventor_typed"})


# --- Interaction dispositions: exactly the six preserved owner actions ---
DISPOSITION_ANSWERED               = "answered"
DISPOSITION_UNKNOWN                = "unknown"
DISPOSITION_DEFERRED               = "deferred"
DISPOSITION_PROVISIONAL_ASSUMPTION = "provisional_assumption"
DISPOSITION_SPECIALIST_REQUESTED   = "specialist_requested"
DISPOSITION_EVIDENCE_REQUESTED     = "evidence_requested"

# RVR-1 (Wave-1 remediation contract, OD-R1): a SEVENTH governed ledger
# disposition recording the explicit owner action of accepting a gap as a
# known risk. It is an owner-action record, NEVER a WS12 path classification
# (WS12 OD-3/OD-11 preserved: the WS12 vocabulary stays disjoint from this
# set) and NEVER added to the web answered-route action allowlist (the six
# structured actions there remain frozen; risk acceptance has its own
# explicit route). The record itself resolves nothing — the gap-status write
# happens only through the canonical lifecycle function
# `engine.progression_loop.accept_gap_risk`.
DISPOSITION_RISK_ACCEPTED          = "risk_accepted"

# W2-A / RVR-4 (authoritative contract §2, PR #567): the exact frozen
# decision-action vocabulary. Refinement is NOT a disposition — it is the
# existing single-target supersession relation within a same-class chain.
# Context withdrawal is OUTSIDE W2-A. These are carrier dispositions only:
# FDC-001 `DecisionRecord` remains the sole canonical decision-semantics owner.
DISPOSITION_DECISION_CONTEXT_DECLARED     = "decision_context_declared"
DISPOSITION_DECISION_ALTERNATIVE_DECLARED = "decision_alternative_declared"
DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN = "decision_alternative_withdrawn"

DECISION_ACTION_DISPOSITIONS = frozenset({
    DISPOSITION_DECISION_CONTEXT_DECLARED,
    DISPOSITION_DECISION_ALTERNATIVE_DECLARED,
    DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN,
})

INTERACTION_DISPOSITIONS = frozenset({
    DISPOSITION_ANSWERED, DISPOSITION_UNKNOWN, DISPOSITION_DEFERRED,
    DISPOSITION_PROVISIONAL_ASSUMPTION, DISPOSITION_SPECIALIST_REQUESTED,
    DISPOSITION_EVIDENCE_REQUESTED, DISPOSITION_RISK_ACCEPTED,
}) | DECISION_ACTION_DISPOSITIONS

# CAP-10 Slice 1 (Stage 21): the inventor's explicit declaration that TWO of
# their own active recorded answers conflict. Relationship metadata over two
# existing answers — NOT an answer, NOT an owner interaction on a question, and
# deliberately NOT in INTERACTION_DISPOSITIONS (`record_interaction` refuses it;
# its one carrier is `record_contradiction_declaration`). It resolves nothing,
# chooses no winner and changes no gap, maturity, progression or score.
DISPOSITION_CONTRADICTION_DECLARED = "contradiction_declared"

# CAP-08 Slice 1 (Stage 20): the inventor's explicit declaration that ONE of
# their recorded answers depends on ONE of their own provisional assumptions.
# One record = one DIRECTED edge (assumption -> dependent answer). Like the
# CAP-10 record it is relationship metadata over two existing records, NOT in
# INTERACTION_DISPOSITIONS (`record_interaction` refuses it; its one carrier is
# `record_assumption_dependency_declarations`). It validates, confirms or
# rejects nothing and changes no gap, maturity, progression, score, routing or
# readiness.
DISPOSITION_ASSUMPTION_DEPENDENCY_DECLARED = "assumption_dependency_declared"

# The closed set of relationship-metadata dispositions: records that relate
# existing records and are never themselves an answer, a requirement, a
# question event or a serving event.
RELATIONSHIP_METADATA_DISPOSITIONS = frozenset({
    DISPOSITION_CONTRADICTION_DECLARED,
    DISPOSITION_ASSUMPTION_DEPENDENCY_DECLARED,
})

# The seven pre-W2-A dispositions, needed by the bounded legacy-payload load
# rule in engine.record_contract (contract §4: only a LEGACY payload may omit
# `decision_context_root`).
LEGACY_INTERACTION_DISPOSITIONS = INTERACTION_DISPOSITIONS - DECISION_ACTION_DISPOSITIONS

# Durable pending state for the two request actions (None for the others).
_PENDING_BY_DISPOSITION = {
    DISPOSITION_SPECIALIST_REQUESTED: "specialist",
    DISPOSITION_EVIDENCE_REQUESTED:   "evidence",
}

# Default provenance is derived ONLY from the owner action that created the
# record (the action itself is the source fact) — never from text, vocabulary,
# quality, maturity, or gap status. An explicit provenance argument may only
# restate this value (Provenance Hardening Step 1); it never overrides it.
# Owner-asserting actions default to OWNER_STATED; the non-asserting actions
# (unknown / deferred / specialist_requested / evidence_requested) assert no
# content and so remain LEGACY_UNSPECIFIED.
_DEFAULT_PROVENANCE_BY_DISPOSITION = {
    DISPOSITION_ANSWERED:               OWNER_STATED,
    DISPOSITION_PROVISIONAL_ASSUMPTION: OWNER_STATED,
    # RVR-1: accepting a risk is an owner assertion about the owner's own
    # decision — provenance is the owner's statement, never platform-derived.
    DISPOSITION_RISK_ACCEPTED:          OWNER_STATED,
    # W2-A (contract §2 frozen provenance rule): declaring a context, declaring
    # an alternative, and withdrawing an alternative are each an owner
    # assertion about the owner's own decision — same semantics as the
    # risk_accepted precedent above. Never LEGACY_UNSPECIFIED.
    DISPOSITION_DECISION_CONTEXT_DECLARED:      OWNER_STATED,
    DISPOSITION_DECISION_ALTERNATIVE_DECLARED:  OWNER_STATED,
    DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN: OWNER_STATED,
    # CAP-10 Slice 1: an inventor's own conflict declaration. Its carrier is
    # `record_contradiction_declaration` (record_interaction refuses it).
    DISPOSITION_CONTRADICTION_DECLARED:         OWNER_STATED,
    # CAP-08 Slice 1: an inventor's own dependency declaration. Its carrier is
    # `record_assumption_dependency_declarations` (record_interaction refuses it).
    DISPOSITION_ASSUMPTION_DEPENDENCY_DECLARED: OWNER_STATED,
}

# Provenance Hardening Step 1 — the provenance a STORED record of each known
# disposition may carry when it is loaded (engine.record_contract). It is the
# load-side twin of the mint map above, kept explicit so no disposition can
# enter without its own load policy. Each set holds exactly the mint value,
# plus LEGACY_UNSPECIFIED for answered / provisional_assumption ONLY: those
# owner-asserting records were persisted before provenance was stamped, so
# LEGACY is their truthful historical source. A non-asserting disposition can
# never have been OWNER_STATED, and risk / decision actions were OWNER_STATED
# from their introduction. Load compatibility grants nothing to the mint seam.
# Distinct from LEGACY_INTERACTION_DISPOSITIONS (W2-A decision_context_root).
ASSERTION_LOAD_PROVENANCE_BY_DISPOSITION = {
    DISPOSITION_ANSWERED:               frozenset({OWNER_STATED, LEGACY_UNSPECIFIED}),
    DISPOSITION_PROVISIONAL_ASSUMPTION: frozenset({OWNER_STATED, LEGACY_UNSPECIFIED}),
    DISPOSITION_UNKNOWN:                frozenset({LEGACY_UNSPECIFIED}),
    DISPOSITION_DEFERRED:               frozenset({LEGACY_UNSPECIFIED}),
    DISPOSITION_SPECIALIST_REQUESTED:   frozenset({LEGACY_UNSPECIFIED}),
    DISPOSITION_EVIDENCE_REQUESTED:     frozenset({LEGACY_UNSPECIFIED}),
    DISPOSITION_RISK_ACCEPTED:          frozenset({OWNER_STATED}),
    DISPOSITION_DECISION_CONTEXT_DECLARED:      frozenset({OWNER_STATED}),
    DISPOSITION_DECISION_ALTERNATIVE_DECLARED:  frozenset({OWNER_STATED}),
    DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN: frozenset({OWNER_STATED}),
    # CAP-10 Slice 1: singleton — introduced OWNER_STATED, never LEGACY.
    DISPOSITION_CONTRADICTION_DECLARED:         frozenset({OWNER_STATED}),
    # CAP-08 Slice 1: singleton — introduced OWNER_STATED, never LEGACY.
    DISPOSITION_ASSUMPTION_DEPENDENCY_DECLARED: frozenset({OWNER_STATED}),
}

# Validation levels treated as "validated" (i.e. not owner-unvalidated) by the
# pure derived-readiness recomputation. UNVALIDATED is deliberately excluded.
VALIDATED_STATUSES = frozenset({
    SPECIALIST_REVIEWED, EMPIRICALLY_DEMONSTRATED, INDEPENDENTLY_VERIFIED,
})

# The CLOSED validation vocabulary: the four values declared above, named once
# so a boundary can check membership instead of re-listing them. This is NOT a
# new vocabulary and NOT a new axis — it is the existing four constants, and it
# grants nothing: which of them any writer may award is decided entirely
# elsewhere, and today no live path writes anything but UNVALIDATED.
VALIDATION_STATUSES = frozenset({UNVALIDATED}) | VALIDATED_STATUSES


@dataclass
class Evidence:
    content   : str
    quality   : str        # ASSERTED | REASONED | DEMONSTRATED
    iteration : int
    # Increment 2 additive axes (defaulted, backward compatible). NEVER inferred:
    # legacy/keyword construction defaults to the truthful "unknown" values.
    provenance        : str = LEGACY_UNSPECIFIED
    validation_status : str = UNVALIDATED


@dataclass
class Gap:
    gap_type        : str  # one of the 3 gap types above
    status          : str  # OPEN | PARTIAL | CLOSED | ACCEPTED_RISK
    opened_at       : int  # iteration number
    iterations_open : int  = 0
    closed_at       : Optional[int] = None
    # Accepted (substantiated) Evidence captured for this gap (written only for
    # Stage 3 reasoning gaps). Optional and backward compatible: states/fixtures
    # that omit it default to []. Evidence is defined above and the module
    # evaluates annotations eagerly, so list[Evidence] is safe here.
    evidence        : list[Evidence] = field(default_factory=list)
    # Increment 2 additive, defaulted resolution provenance (no lifecycle change).
    # Empty/None for legacy and unresolved gaps — never fabricated.
    resolution_rationale : Optional[str] = None
    resolution_source    : Optional[str] = None


@dataclass
class AssertionRecord:
    """Increment 2 append-only interaction/assertion ledger entry on IdeaState.

    A durable, in-memory record of one owner interaction (one of the six
    dispositions). It is NOT Evidence, NOT a gap, and has NO effect on maturity,
    lifecycle, gap status, transitions, or the ILT-002 transcript. It records the
    truthful provenance/validation/disposition of what the owner did. Multiple
    records may coexist for the same gap_context; contradiction and supersession
    are non-destructive (history is retained).
    """
    record_id         : str
    disposition       : str            # one of INTERACTION_DISPOSITIONS
    content           : str
    gap_context       : Optional[str]
    iteration         : int
    provenance        : str = LEGACY_UNSPECIFIED
    validation_status : str = UNVALIDATED
    quality           : Optional[str] = None
    pending           : Optional[str] = None   # "specialist" | "evidence" | None
    responsibility    : Optional[str] = None   # explicit only when owner-created
    resolves_gap      : bool = False           # a disposition never resolves a gap
    contradicts       : list = field(default_factory=list)   # record_ids in conflict
    supersedes        : list = field(default_factory=list)   # record_ids this supersedes
    superseded_by     : Optional[str] = None
    # W2-A (contract §3): explicit decision-context attachment. None on every
    # legacy record and on every `decision_context_declared` record (chain
    # membership is derived from the supersession edge, never from this field);
    # the exact founding-chain root record_id on alternative declarations and
    # withdrawals. Never carried by gap_context/question_id/content/position.
    decision_context_root : Optional[str] = None
    # UQTR-01 Step 2B: the canonical RVR-7 identity of the question this record
    # answered, minted ONLY from the server-verified signed answer target of a
    # new question-bearing write. None on every legacy record (never inferred
    # from content, wording, language, current state or replay), on records with
    # no canonical question (e.g. the completion-stage criticality correction)
    # and on decision actions. A correction inherits its prior's value verbatim.
    question_target : Optional[str] = None
    # CAP-10 Slice 1: the canonical (lo, hi) pair of endpoint record ids on a
    # `contradiction_declared` record ONLY; None on every other record. The
    # endpoints' own questions, gaps and text stay owned by the endpoints.
    contradiction_endpoints : Optional[list] = None
    # CAP-08 Slice 1: the directed edge of an `assumption_dependency_declared`
    # record ONLY — {"assumption_record_id": ..., "dependent_answer_record_id":
    # ...}; None on every other record. Questions, gaps, requirements and text
    # stay owned by the two endpoints and are resolved from them, never copied.
    dependency_edge : Optional[dict] = None


# CAP-10 Slice 1 — the ONE shared projection path. The durable authority for an
# owner-declared contradiction is the `contradiction_declared` record; the
# symmetric `contradicts` edges on its two endpoints are a DERIVED projection,
# applied here (live after mint, and on every load) through the same linking
# primitive `IdeaState.mark_contradiction` uses. The projected partners are
# remembered on the record instance (never a dataclass field), so the
# serializer can keep them out of any durable payload: the endpoint rows are
# never rewritten and no second, independently editable truth source exists.
_PROJECTED_CONTRADICTS_ATTR = "_projected_contradicts"
_REC_ID_RE = re.compile(r"^rec_[1-9][0-9]*$")


def _link_contradiction(a, b):
    """The existing symmetric, idempotent contradiction link between two
    distinct records (the body `mark_contradiction` always had)."""
    if a.record_id == b.record_id:
        raise ValueError(
            f"a record cannot contradict itself: {a.record_id!r}")
    if b.record_id not in a.contradicts:
        a.contradicts.append(b.record_id)
    if a.record_id not in b.contradicts:
        b.contradicts.append(a.record_id)


def projected_contradicts(record):
    """The partner ids on ``record.contradicts`` that are a CAP-10 projection
    (empty for every record that is not a declared endpoint)."""
    return frozenset(getattr(record, _PROJECTED_CONTRADICTS_ATTR, ()) or ())


def canonical_contradiction_pair(record_id_a, record_id_b):
    """Deterministic (lo, hi) order of two ``rec_N`` ids by their number, so the
    selection order never makes a different relationship. Refuses malformed
    ids and a pair naming one record twice."""
    for rid in (record_id_a, record_id_b):
        if not isinstance(rid, str) or not _REC_ID_RE.match(rid):
            raise ValueError("a contradiction endpoint must be a rec_N id")
    if record_id_a == record_id_b:
        raise ValueError("a contradiction needs two distinct recorded answers")
    return sorted((record_id_a, record_id_b), key=lambda r: int(r[4:]))


def project_declared_contradictions(assertions):
    """Apply every `contradiction_declared` record in ``assertions`` to its two
    endpoints through the shared link. Idempotent; an endpoint missing from the
    list is skipped (the record contract rejects such a history before this is
    reached). Returns ``assertions``."""
    by_id = {r.record_id: r for r in assertions}
    for record in assertions:
        if record.disposition != DISPOSITION_CONTRADICTION_DECLARED:
            continue
        pair = record.contradiction_endpoints or ()
        if len(pair) != 2 or pair[0] not in by_id or pair[1] not in by_id:
            continue
        a, b = by_id[pair[0]], by_id[pair[1]]
        for this, other in ((a, b), (b, a)):
            if other.record_id not in this.contradicts:
                projected = set(projected_contradicts(this))
                projected.add(other.record_id)
                setattr(this, _PROJECTED_CONTRADICTS_ATTR, frozenset(projected))
        _link_contradiction(a, b)
    return assertions


def active_declared_contradiction_pairs(assertions):
    """The (lo, hi) pairs of every owner declaration whose BOTH endpoints are
    still active (not superseded). A declaration never transfers to a
    correction's replacement answer; once either endpoint is superseded the
    pair is simply no longer active — historical, never 'resolved'."""
    by_id = {r.record_id: r for r in assertions}
    pairs = set()
    for record in assertions:
        if record.disposition != DISPOSITION_CONTRADICTION_DECLARED:
            continue
        pair = record.contradiction_endpoints or ()
        if len(pair) != 2:
            continue
        ends = [by_id.get(rid) for rid in pair]
        if all(e is not None and e.superseded_by is None for e in ends):
            pairs.add(tuple(pair))
    return frozenset(pairs)


# CAP-08 Slice 1 — the directed assumption -> answer dependency primitive.
# Domain-neutral: it keys only on canonical record types and record ids, never
# on a domain, a question catalog, a gap or technical vocabulary.
DEPENDENCY_EDGE_KEYS = ("assumption_record_id", "dependent_answer_record_id")


def _rec_number(record_id):
    if not isinstance(record_id, str) or not _REC_ID_RE.match(record_id):
        raise ValueError("a dependency endpoint must be a rec_N id")
    return int(record_id[4:])


def normalize_dependent_answers(record_ids):
    """The unique, deterministic (numeric ``rec_N``) order of a submitted set of
    dependent answer ids. Refuses an empty submission and malformed ids."""
    ids = list(record_ids or ())
    if not ids:
        raise ValueError("a dependency needs at least one dependent answer")
    for rid in ids:
        _rec_number(rid)
    return sorted(set(ids), key=_rec_number)


def dependency_edge_of(record):
    """``(assumption_record_id, dependent_answer_record_id)`` of a well-formed
    dependency declaration, else None."""
    if getattr(record, "disposition", None) != \
            DISPOSITION_ASSUMPTION_DEPENDENCY_DECLARED:
        return None
    edge = getattr(record, "dependency_edge", None)
    if not isinstance(edge, dict) or set(edge) != set(DEPENDENCY_EDGE_KEYS):
        return None
    return (edge["assumption_record_id"], edge["dependent_answer_record_id"])


@dataclass(frozen=True)
class DeclaredDependency:
    """One historical dependency declaration and whether its edge is active
    (BOTH endpoints still present and not superseded). Derived, never stored."""
    declaration_record_id      : str
    assumption_record_id       : str
    dependent_answer_record_id : str
    active                     : bool


@dataclass(frozen=True)
class AssumptionDependencyProjection:
    """The ONE derived view of every `assumption_dependency_declared` record:
    the declarations in durable ledger order (historical and active), the
    active directed edges, and the active edges grouped by assumption (groups
    in assumption ledger order, answers in ledger order). The declaration
    records are the authority; this view is recomputed, never persisted."""
    declarations  : tuple
    active_edges  : tuple
    by_assumption : tuple        # ((assumption_record_id, (answer_id, ...)), ...)


def project_assumption_dependencies(assertions):
    """Pure, deterministic projection over ``assertions`` (ledger order). A
    declaration's edge is active iff its assumption AND its dependent answer
    are both present and not superseded; a superseded endpoint makes that
    exact edge inactive and nothing transfers to a replacement record. Endpoint
    rows are never touched."""
    records = list(assertions or ())
    by_id = {r.record_id: r for r in records}
    position = {r.record_id: i for i, r in enumerate(records)}
    declarations, active = [], []
    for record in records:
        edge = dependency_edge_of(record)
        if edge is None:
            continue
        ends = [by_id.get(rid) for rid in edge]
        is_active = all(e is not None and e.superseded_by is None for e in ends)
        declarations.append(DeclaredDependency(record.record_id, edge[0],
                                               edge[1], is_active))
        if is_active and edge not in active:
            active.append(edge)
    grouped = {}
    for assumption_id, answer_id in active:
        grouped.setdefault(assumption_id, []).append(answer_id)
    by_assumption = tuple(
        (aid, tuple(sorted(answers, key=lambda rid: position[rid])))
        for aid, answers in sorted(grouped.items(),
                                   key=lambda item: position[item[0]]))
    return AssumptionDependencyProjection(
        declarations=tuple(declarations), active_edges=tuple(active),
        by_assumption=by_assumption)


@dataclass(frozen=True)
class CriticalityConfirmation:
    """Workstream 4 (contract §6.1): one frozen record per explicit inventor
    criticality action — `confirmed` (with exactly one non-UNDETERMINED
    category and a verbatim rationale) or `deferred` (no category, no
    rationale). Lives ONLY in the in-memory session-bounded append-only
    history IdeaState.criticality_confirmations; records are never mutated or
    removed within the session — later actions supersede by ordering only.
    NOT Evidence, NOT a gap, NO effect on maturity, scoring, lifecycle,
    transitions, the ledger, or the transcript; no durable retention."""
    confirmation_id    : int
    requirement_id     : str
    action             : str                      # confirmed | deferred
    category           : Optional[str]            # one of the three, or None
    rationale_verbatim : Optional[str]            # byte-verbatim; None for deferred
    rationale_source   : Optional[str]            # reused_statement:<rec_N> | inventor_edited | inventor_typed
    iteration          : int
    provenance         : str = "owner_confirmed"


@dataclass
class SuccessCriterion:
    """
    A user-authored success criterion for one proposed Prototype & Test Plan
    experiment. Planning metadata ONLY: never graded, never read by progression
    or maturity, never written to the ILT-002 transcript, and never treated as a
    result. Keyed in IdeaState.success_criteria by the experiment's stable
    experiment_id. provenance records that the inventor authored it.
    """
    criterion  : str
    provenance : str = "user_defined"


@dataclass
class MeasurementMethod:
    """
    Stage 19 / CAP-09 SLICE-02: the inventor's OWN description of HOW they plan
    to measure or check one proposed Prototype & Test Plan experiment. Planning
    metadata ONLY: never a measurement, a result, Evidence, a validation outcome
    or readiness; never generated, inferred, interpreted or graded; never read
    by progression or maturity; never written to the ILT-002 transcript.
    Distinct from the system-provided ``what_to_observe`` context, which it
    never replaces or combines with. Keyed in IdeaState.measurement_methods by
    the experiment's stable experiment_id. provenance records that the inventor
    authored it.
    """
    method     : str
    provenance : str = "user_defined"


@dataclass
class TestHypothesis:
    """
    Stage 19 / CAP-09 SLICE 3: the inventor's OWN test hypothesis for one
    proposed Prototype & Test Plan experiment — what they expect to happen in
    it, in their own words. Planning metadata ONLY: never Evidence, a result,
    a validation outcome, readiness, an assumption (CAP-08) or a contradiction
    (CAP-10); never generated, inferred, parsed, interpreted, checked or
    graded; never read by progression or maturity; never written to the
    ILT-002 transcript. Distinct from the system-generated ``objective``, the
    success criterion and the measurement method, which it never replaces or
    combines with. Keyed in IdeaState.test_hypotheses by the experiment's stable
    experiment_id. provenance records that the inventor authored it.
    """
    __test__ = False          # not a pytest test class despite its name
    hypothesis : str
    provenance : str = "user_defined"


@dataclass
class TestVariable:
    """
    Stage 19 / CAP-09 SLICE 4: the inventor's OWN test variable / condition for
    one proposed Prototype & Test Plan experiment — in their own free-text
    words, the factor, setting, input, configuration or condition they intend
    to deliberately change, compare or vary during that ONE experiment ("What
    will you change or compare in this test?"). It is NOT a formal
    experimental-design model: no independent / dependent / control variable,
    unit, range, factor taxonomy or causal relationship, and the text is never
    parsed into one. Planning metadata ONLY: never Evidence, a result, a
    validation outcome, readiness, an assumption (CAP-08) or a contradiction
    (CAP-10); never generated, inferred (from the hypothesis, the method,
    ``what_to_observe``, the mechanism or anything else), interpreted, checked
    or graded; never read by progression or maturity; never written to the
    ILT-002 transcript. Distinct from the system-generated ``objective`` and
    ``what_to_observe``, the success criterion, the test hypothesis and the
    measurement method, which it never replaces or combines with. Keyed in
    IdeaState.test_variables by the experiment's stable experiment_id.
    provenance records that the inventor authored it.
    """
    __test__ = False          # not a pytest test class despite its name
    variable   : str
    provenance : str = "user_defined"


@dataclass
class IterationLog:
    iteration       : int
    gap_targeted    : str
    question_asked  : str
    response_summary: str
    gaps_changed    : list
    maturity_before : int
    maturity_after  : int


@dataclass
class AcknowledgedUnknown:
    """
    Records an explicit inventor acknowledgment of a specific unknown.
    Parallel track in integrate_response(). NO effect on progression.
    Governance: TRANSITION_AUTHORIZATION_GOVERNANCE s4 Layer 1 PGC-3
    Authorization: Owner-authorized 2026-06-06
    """
    iteration      : int
    gap_context    : str
    verbatim       : str
    category_basis : str


@dataclass
class IdeaState:
    idea_id        : str
    iteration      : int                    = 0
    maturity_level : int                    = 0  # 0 | 1 | 2 only (Stage 2)
    current_stage  : int                    = 2  # 2 = Stage 2, 3 = Stage 3
    domain_signal  : Optional[str]          = None
    direction      : str                    = PROGRESSING

    # What is established
    known_problem   : Optional[Evidence]    = None
    known_mechanism : Optional[Evidence]    = None

    # Open gaps
    gaps           : list                   = field(default_factory=list)

    # History
    iteration_log  : list                   = field(default_factory=list)

    # Acknowledged unknowns -- inventor-stated knowledge gaps (parallel track)
    # No effect on progression. Governance: PGC-3, Priority 5, FDC-001.
    acknowledged_unknowns : list            = field(default_factory=list)

    # Idea capture
    idea_summary   : Optional[str]          = None
    # MG-8 (`MG8-BOUNDED-FIX-IMPLEMENT-01`): the TRUE assessed quality of the
    # statement captured in `idea_summary`, recorded at the same moment by the
    # same level-0 seam. Additive, defaulted, in-memory ONLY: it is not a second
    # problem store, is never persisted (the durable envelope keeps the seed and
    # the ledger keeps the answers), and is re-derived identically by replay.
    # None on every legacy state, where `idea_summary` could only have been
    # captured at REASONED or better.
    idea_summary_quality : Optional[str]    = None
    path           : str                    = "legacy_undesignated_current_behavior"

    # Per-experiment owner-defined success criteria (planning metadata only).
    # Keyed by stable prototype experiment_id -> SuccessCriterion. Default empty
    # for backward compatibility. NOT Evidence, NOT graded, NOT read by
    # progression/maturity, NOT written to the ILT-002 transcript.
    # SuccessCriterion is defined above and the module evaluates annotations
    # eagerly (no `from __future__ import annotations`), so the parameterized
    # form is safe — matching the Gap.evidence: list[Evidence] precedent.
    success_criteria : dict[str, SuccessCriterion] = field(default_factory=dict)

    # Stage 19 / CAP-09 SLICE-02: per-experiment inventor-written measurement
    # methods (planning metadata only), keyed like success_criteria. Default
    # empty; same boundaries as success_criteria above.
    measurement_methods : dict[str, MeasurementMethod] = field(default_factory=dict)

    # Stage 19 / CAP-09 SLICE 3: per-experiment inventor-written test
    # hypotheses (planning metadata only), keyed like success_criteria. Default
    # empty; same boundaries as success_criteria above.
    test_hypotheses : dict[str, TestHypothesis] = field(default_factory=dict)

    # Stage 19 / CAP-09 SLICE 4: per-experiment inventor-written test variable /
    # condition (planning metadata only), keyed like success_criteria. Default
    # empty; same boundaries as success_criteria above.
    test_variables : dict[str, TestVariable] = field(default_factory=dict)

    # Increment 2 append-only interaction/assertion ledger. Distinct from the
    # legacy compatibility fields (known_problem/known_mechanism/gaps/maturity):
    # this is the durable disposition history, not progression state. Empty by
    # default and persistence-independent (in-memory only).
    assertions : list = field(default_factory=list)

    # Workstream 4 (contract §6.1): session-bounded, append-only criticality
    # confirmation history. In-memory only — nothing here survives restart or
    # reload, and no durable retention is implied (persistence stays frozen).
    criticality_confirmations : list = field(default_factory=list)

    # §5-I3 subsystem foundation (D-S5-04 / D-S5-05): optional, in-memory,
    # persistence-independent subsystem descriptors. Empty by default so absence
    # preserves the current single-domain behavior. NOTHING here is written to
    # durable persistence, and it NEVER changes the project root domain (the
    # scalar `domain`/`confirmed_domain`). A subsystem may reference a canonical
    # domain as metadata only — a reference never activates a domain. See
    # engine/subsystem_model.py.
    subsystems : list = field(default_factory=list)

    # T2-A Quantified Requirements Slice 1: the in-memory CARRIER of the
    # project's validated durable requirement-quantity history (a list of
    # frozen ``engine.requirement_quantity.RequirementQuantity`` rows in
    # stored order). It is attached from the durable store by the web layer
    # (cold-load, render, resume, correction reconstruction) and consumed
    # READ-ONLY by the deliverable assembler. Empty by default, so every
    # pre-T2A state, fixture and replay is byte-identical. It is NOT
    # Evidence, NOT a gap, NOT a ledger record and has NO effect on maturity,
    # scoring, lifecycle, transitions, the transcript, or replay; it is never
    # serialized into the P4-0 record contract.
    requirement_quantities : list = field(default_factory=list)

    # Safe Question Reduction Slice 1: the in-memory CARRIER of the project's
    # durable NeedRouting revisions (frozen
    # ``engine.need_routing.NeedRoutingRevision`` rows in routing order),
    # applied through ``engine.need_routing.apply_revision`` at the SAME
    # durable position live and in replay. It is a SYSTEM routing record, not
    # an Owner ledger record, not Evidence and not a gap status; it is never
    # serialized into the P4-0 record contract. Empty by default, so every
    # pre-routing state, fixture and replay is byte-identical.
    need_routing : list = field(default_factory=list)

    def get_open_gaps(self):
        return [g for g in self.gaps if g.status in (OPEN, PARTIAL)]

    def get_gap(self, gap_type):
        for g in self.gaps:
            if g.gap_type == gap_type:
                return g
        return None

    # --- Increment 2 append-only ledger operations (in-memory, non-destructive)

    def record_interaction(self, action, content="", gap_context=None,
                           iteration=0, provenance=None,
                           validation_status=UNVALIDATED, quality=None,
                           responsibility=None, supersedes=None,
                           decision_context_root=None, question_target=None):
        """Append a durable disposition record for one of the six owner actions.

        Append-only: never mutates an existing record and never removes one. Has
        NO effect on maturity, lifecycle, gaps, transitions, or the transcript.
        Provenance is derived ONLY from the action (never from text/quality/
        maturity); an explicit value may only restate it. Returns the new record.

        W2-A (authoritative contract §3 mint-seam rule): the three
        decision-action dispositions receive class-bounded STRUCTURAL
        fail-closed validation HERE, in the carrier itself, so no caller can
        bypass the composition seam and create invalid live decision-action
        state (nothing is appended on any violation). This is carrier
        legality only — decision SEMANTICS stay with FDC-001.
        """
        if action not in INTERACTION_DISPOSITIONS:
            raise ValueError(f"unknown interaction action: {action!r}")
        if action in DECISION_ACTION_DISPOSITIONS:
            # Frozen provenance rule (§2), preserved: provenance is dictated
            # by the disposition, and an explicit provenance argument may only
            # restate that dictated value — it can never override or
            # reclassify the source. A decision action is always OWNER_STATED,
            # so any other explicit value is refused here with its own message.
            if provenance is not None and provenance != OWNER_STATED:
                raise ValueError(
                    "decision-action provenance must be OWNER_STATED, got "
                    f"{provenance!r}")
            # No gap linkage/attachment overload (§3): decision actions never
            # carry a gap context.
            if gap_context is not None:
                raise ValueError(
                    "a decision-action record may not carry gap_context")
        elif decision_context_root is not None:
            # Legacy/non-decision records always carry None (§3).
            raise ValueError(
                "decision_context_root is reserved for decision-action "
                "dispositions")
        # Provenance Hardening Step 1: this is an OWNER-INTERACTION carrier, so
        # the source is dictated by the disposition alone. An explicit value may
        # only restate it — it can never change who the source is.
        dictated = _DEFAULT_PROVENANCE_BY_DISPOSITION.get(
            action, LEGACY_UNSPECIFIED)
        if provenance is not None and provenance != dictated:
            raise ValueError(
                f"provenance of a {action!r} record is dictated by its "
                f"disposition ({dictated})")
        provenance = dictated
        # Mint authority is not vocabulary: the other canonical statuses stay
        # representable and loadable, but no writer is authorized to award
        # them, so this generic seam mints UNVALIDATED only.
        if validation_status != UNVALIDATED:
            raise ValueError(
                "record_interaction mints UNVALIDATED only; no validation "
                "award is authorized through this seam")
        # Responsibility is stored EXPLICITLY only for owner-created records
        # (contract §3.4): when this record is owner-stated, the owner is
        # responsible. Otherwise it is left None and remains DERIVED by the
        # existing display behavior (web.responsibility_labels) — never fabricated.
        # An explicit value may only restate that; it may not contradict it.
        carried = ASSERTION_RESPONSIBILITY_BY_PROVENANCE[provenance]
        if responsibility is not None and responsibility != carried:
            raise ValueError(
                f"responsibility of a {provenance} record must be {carried}")
        responsibility = carried
        # P10-PC3 B1 repair (Independent Review): the next id derives from the
        # ledger's MAX existing rec_N, not its length. For every live ledger
        # (ids minted here sequentially, hence contiguous 1..N) max == len, so
        # live behavior is byte-identical. For a RECONSTRUCTED ledger (the
        # durable answered subset restored verbatim after a restart — sparse,
        # because non-answer actions consume ids without durable persistence),
        # the ledger max IS the durable max, so a resumed append can never
        # re-mint an already-persisted rec_N (PRIMARY KEY (project_id,
        # record_id) collision). Historical ids are never reused or renumbered.
        _max_n = max((int(r.record_id[4:]) for r in self.assertions
                      if isinstance(r.record_id, str)
                      and r.record_id.startswith("rec_")
                      and r.record_id[4:].isdigit()), default=0)
        record_id = f"rec_{_max_n + 1}"                 # stable; append-only
        # PVCG-R4-C §6 C-4: additive, backward-compatible correction seam. With
        # `supersedes=None` (every pre-R4 caller) behaviour is byte-identical.
        # When given, the NEW record carries the relationship FORWARD (C-3),
        # because the durable store is INSERT-only and the prior row must never
        # be rewritten (C-2, §7 S-1). Fail-closed BEFORE anything is appended
        # (C-5): unknown ids, self-supersession, an already-superseded target,
        # and any cycle are refused with NOTHING stored. This reuses the ONE
        # canonical supersession model (§7 S-4) — no second concept.
        superseded_ids = list(supersedes or ())
        if superseded_ids:
            if len(set(superseded_ids)) != len(superseded_ids):
                raise ValueError("duplicate supersedes reference")
            for prior_id in superseded_ids:
                prior = self._require_record(prior_id)      # unknown id -> refuse
                if prior_id == record_id:
                    raise ValueError(
                        f"a record cannot supersede itself: {prior_id!r}")
                if prior.superseded_by is not None:
                    raise ValueError(
                        f"record already superseded: {prior_id!r}")
        # W2-A (contract §3/§8) — class-bounded structural validation, still
        # BEFORE anything is appended. The generic supersession primitive
        # above is untouched for legacy-to-legacy behavior (ID-11).
        self._validate_decision_action_structure(
            action, decision_context_root, superseded_ids)
        # UQTR-01 Step 2B — question_target carrier legality, still BEFORE
        # anything is appended: a non-empty string or None; never on a decision
        # action; and a correction carries its prior's value VERBATIM (a
        # content correction never becomes a target correction).
        if question_target is not None:
            if not isinstance(question_target, str) or not question_target:
                raise ValueError("question_target must be a non-empty string")
            if action in DECISION_ACTION_DISPOSITIONS:
                raise ValueError(
                    "a decision-action record may not carry question_target")
        for prior_id in superseded_ids:
            if self._require_record(prior_id).question_target != question_target:
                raise ValueError(
                    "a correction must inherit its prior's question_target "
                    f"verbatim: {prior_id!r}")
        record = AssertionRecord(
            record_id=record_id, disposition=action, content=content,
            gap_context=gap_context, iteration=iteration, provenance=provenance,
            validation_status=validation_status, quality=quality,
            pending=_PENDING_BY_DISPOSITION.get(action),
            responsibility=responsibility, resolves_gap=False,
            supersedes=list(superseded_ids),
            decision_context_root=decision_context_root,
            question_target=question_target,
        )
        self.assertions.append(record)
        # In-memory inverse edge, set through the EXISTING canonical primitive so
        # the acyclicity guard and the five derived-module active-set consumers
        # behave exactly as they already do. Durably the prior row is untouched;
        # the inverse is re-derived on load by
        # `record_contract.reconcile_supersession_edges` (C-3).
        for prior_id in superseded_ids:
            self.mark_supersession(prior_id, record_id)
        return record

    def get_assertions(self, gap_context=None):
        """Return ledger records, optionally filtered to one gap_context. Returns
        a new list (the caller cannot mutate the ledger through it)."""
        if gap_context is None:
            return list(self.assertions)
        return [r for r in self.assertions if r.gap_context == gap_context]

    def _require_record(self, record_id):
        for r in self.assertions:
            if r.record_id == record_id:
                return r
        raise ValueError(f"unknown record_id: {record_id!r}")

    def _validate_decision_action_structure(self, action, decision_context_root,
                                            superseded_ids):
        """W2-A carrier legality (authoritative contract §3/§8) — STRUCTURAL
        only, fail-closed, nothing appended by the caller on a raise.

        Enforced here so NO direct `record_interaction` call can bypass the
        composition seam: root existence/class, founding-root reference,
        cross-context and cross-class supersession, single-target decision
        supersession (ID-11), and protection of decision-class records from
        legacy-action supersession. Decision SEMANTICS remain FDC-001's."""
        if action not in DECISION_ACTION_DISPOSITIONS:
            # Legacy actions: only class protection — a legacy record may not
            # supersede a decision-action record (cross-class, ID-11). All
            # legacy-to-legacy behavior is byte-identical.
            for prior_id in superseded_ids:
                prior = self._require_record(prior_id)
                if prior.disposition in DECISION_ACTION_DISPOSITIONS:
                    raise ValueError(
                        "a legacy action may not supersede a decision-action "
                        f"record: {prior_id!r}")
            return
        # ID-11: a decision action supersedes at most ONE prior record.
        if len(superseded_ids) > 1:
            raise ValueError(
                "a decision action may supersede at most one prior record")
        if action == DISPOSITION_DECISION_CONTEXT_DECLARED:
            if decision_context_root is not None:
                raise ValueError(
                    "a decision_context_declared record carries no "
                    "decision_context_root (chain membership is derived from "
                    "the supersession edge)")
            for prior_id in superseded_ids:
                prior = self._require_record(prior_id)
                if prior.disposition != DISPOSITION_DECISION_CONTEXT_DECLARED:
                    raise ValueError(
                        "a context refinement must supersede a "
                        "decision_context_declared record")
            return
        # Alternative declaration / withdrawal: a valid founding context root
        # is mandatory.
        if not decision_context_root:
            raise ValueError(
                f"{action} requires a decision_context_root")
        root = self._require_record(decision_context_root)
        if root.disposition != DISPOSITION_DECISION_CONTEXT_DECLARED:
            raise ValueError(
                "decision_context_root must reference a "
                "decision_context_declared record")
        if root.supersedes:
            raise ValueError(
                "decision_context_root must be the FOUNDING record of its "
                "context chain (a refinement is not a root)")
        if action == DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN \
                and len(superseded_ids) != 1:
            raise ValueError(
                "a withdrawal must supersede exactly one active alternative")
        for prior_id in superseded_ids:
            prior = self._require_record(prior_id)
            if prior.disposition != DISPOSITION_DECISION_ALTERNATIVE_DECLARED:
                raise ValueError(
                    "an alternative refinement/withdrawal must supersede a "
                    "decision_alternative_declared record")
            if prior.decision_context_root != decision_context_root:
                raise ValueError(
                    "cross-context decision supersession is not allowed")

    def mark_contradiction(self, record_id_a, record_id_b):
        """Mark two existing records as mutually contradictory. Non-destructive:
        both records are retained. Rejects unknown record ids (no invalid edges)
        and rejects a self-contradiction — a record cannot contradict itself, so
        no self-edge is ever created (F-5). Repeated valid calls are idempotent."""
        a = self._require_record(record_id_a)
        b = self._require_record(record_id_b)
        _link_contradiction(a, b)

    def record_contradiction_declaration(self, record_id_a, record_id_b,
                                         content="", iteration=0):
        """CAP-10 Slice 1 — the ONE carrier of a `contradiction_declared`
        record: the inventor's explicit statement that two of their own
        currently ACTIVE `answered` records conflict. Append-only; fails closed
        with NOTHING appended on malformed, unknown, identical, non-answer or
        already-superseded endpoints, or on a pair already actively declared.

        The record is OWNER_STATED / OWNER_INPUT / UNVALIDATED, carries no gap,
        question, decision context, quality, pending state, supersession or
        contradiction edge of its own, and keeps the optional note verbatim in
        ``content``. The symmetric edges are then projected onto the two
        endpoints through the shared path. It changes no gap, maturity,
        progression, score or routing, and chooses no winner."""
        pair = canonical_contradiction_pair(record_id_a, record_id_b)
        for rid in pair:
            endpoint = self._require_record(rid)
            if endpoint.disposition != DISPOSITION_ANSWERED:
                raise ValueError("a contradiction endpoint must be an answer")
            if endpoint.superseded_by is not None:
                raise ValueError("a contradiction endpoint must be active")
        if tuple(pair) in active_declared_contradiction_pairs(self.assertions):
            raise ValueError("this contradiction is already declared")
        _max_n = max((int(r.record_id[4:]) for r in self.assertions
                      if isinstance(r.record_id, str)
                      and r.record_id.startswith("rec_")
                      and r.record_id[4:].isdigit()), default=0)
        record = AssertionRecord(
            record_id=f"rec_{_max_n + 1}",
            disposition=DISPOSITION_CONTRADICTION_DECLARED,
            content=content or "", gap_context=None, iteration=iteration,
            provenance=_DEFAULT_PROVENANCE_BY_DISPOSITION[
                DISPOSITION_CONTRADICTION_DECLARED],
            validation_status=UNVALIDATED, quality=None, pending=None,
            responsibility=ASSERTION_RESPONSIBILITY_BY_PROVENANCE[OWNER_STATED],
            resolves_gap=False, decision_context_root=None,
            question_target=None, contradiction_endpoints=list(pair),
        )
        self.assertions.append(record)
        project_declared_contradictions(self.assertions)
        return record

    def record_assumption_dependency_declarations(self, assumption_record_id,
                                                  dependent_answer_record_ids,
                                                  iteration=0):
        """CAP-08 Slice 1 — the ONE carrier of `assumption_dependency_declared`
        records: the inventor's explicit statement that each of the given
        recorded answers depends on the given provisional assumption.

        The dependent answers are normalized to a unique deterministic order
        and minted as ONE record per directed edge (assumption -> answer). The
        batch is all-or-nothing: it fails closed with NOTHING appended when the
        assumption is not an ACTIVE `provisional_assumption`, when any answer
        is not an ACTIVE `answered` record, or when any edge is already
        actively declared. Each record is OWNER_STATED / OWNER_INPUT /
        UNVALIDATED with empty content and every other field neutral. It
        changes no gap, maturity, progression, score, routing or readiness."""
        _rec_number(assumption_record_id)
        answers = normalize_dependent_answers(dependent_answer_record_ids)
        assumption = self._require_record(assumption_record_id)
        if assumption.disposition != DISPOSITION_PROVISIONAL_ASSUMPTION:
            raise ValueError("a dependency names a provisional assumption")
        if assumption.superseded_by is not None:
            raise ValueError("a dependency assumption must be active")
        for rid in answers:
            answer = self._require_record(rid)
            if answer.disposition != DISPOSITION_ANSWERED:
                raise ValueError("a dependent record must be an answer")
            if answer.superseded_by is not None:
                raise ValueError("a dependent answer must be active")
        active = set(project_assumption_dependencies(self.assertions).active_edges)
        if any((assumption_record_id, rid) in active for rid in answers):
            raise ValueError("this dependency is already declared")
        _max_n = max((int(r.record_id[4:]) for r in self.assertions
                      if isinstance(r.record_id, str)
                      and r.record_id.startswith("rec_")
                      and r.record_id[4:].isdigit()), default=0)
        minted = []
        for offset, rid in enumerate(answers, start=1):
            minted.append(AssertionRecord(
                record_id=f"rec_{_max_n + offset}",
                disposition=DISPOSITION_ASSUMPTION_DEPENDENCY_DECLARED,
                content="", gap_context=None, iteration=iteration,
                provenance=_DEFAULT_PROVENANCE_BY_DISPOSITION[
                    DISPOSITION_ASSUMPTION_DEPENDENCY_DECLARED],
                validation_status=UNVALIDATED, quality=None, pending=None,
                responsibility=ASSERTION_RESPONSIBILITY_BY_PROVENANCE[OWNER_STATED],
                resolves_gap=False, decision_context_root=None,
                question_target=None, contradiction_endpoints=None,
                dependency_edge={"assumption_record_id": assumption_record_id,
                                 "dependent_answer_record_id": rid},
            ))
        self.assertions.extend(minted)
        return minted

    def mark_supersession(self, superseded_id, by_id):
        """Mark superseded_id as superseded by by_id. Non-destructive: the
        superseded record is retained immutably in history. Rejects unknown
        record ids, self-supersession (F-5), and any direct or indirect cycle —
        the supersession graph must stay acyclic (O-2). The cycle check runs
        BEFORE any mutation, so a rejected call leaves every record unchanged
        (atomic). Existing acyclic chains of arbitrary finite length are accepted;
        repeated valid calls are idempotent; records are never deleted."""
        superseded = self._require_record(superseded_id)
        by = self._require_record(by_id)
        if superseded_id == by_id:
            raise ValueError(
                f"a record cannot supersede itself: {superseded_id!r}")
        # Edges point superseded -> by (record.superseded_by). Adding
        # superseded_id -> by_id closes a cycle iff by_id already reaches
        # superseded_id by walking superseded_by. Walk BEFORE mutating; the `seen`
        # set guards against any pre-existing cycle so the walk always terminates.
        node, seen = by_id, set()
        while node is not None and node not in seen:
            if node == superseded_id:
                raise ValueError(
                    f"supersession would create a cycle: "
                    f"{superseded_id!r} -> {by_id!r}")
            seen.add(node)
            node = self._require_record(node).superseded_by
        superseded.superseded_by = by_id
        if superseded_id not in by.supersedes:
            by.supersedes.append(superseded_id)

    # --- Workstream 4 structured criticality (contract §6; append-only) ----

    def record_criticality_confirmation(self, requirement_id, action,
                                        category=None, rationale_verbatim=None,
                                        rationale_source=None, iteration=0):
        """Guarded recorder (contract §6.3). Appends one frozen
        CriticalityConfirmation for an explicit inventor action and returns
        it. Rejections store NOTHING: unknown actions; `confirmed` with any
        category outside the three confirmable ones (in particular the
        invalid `confirmed + UNDETERMINED` combination); `confirmed` without
        a non-empty verbatim rationale or a valid rationale_source; and
        `deferred` carrying a category. The rationale is stored byte-verbatim
        (an attributed copy — the original ledger record stays unchanged).
        Affects nothing else: no gaps, maturity, transitions, ledger content,
        Evidence, transcript, or scoring."""
        if action not in CRITICALITY_ACTIONS:
            raise ValueError(f"unknown criticality action: {action!r}")
        if action == CRITICALITY_ACTION_CONFIRMED:
            if category not in CONFIRMABLE_CRITICALITY_CATEGORIES:
                raise ValueError(
                    "a confirmed criticality must carry exactly one of the "
                    f"confirmable categories, not {category!r} "
                    "(confirmed + UNDETERMINED is invalid; use the deferred "
                    "action for uncertainty)")
            if not (rationale_verbatim or "").strip():
                raise ValueError(
                    "a confirmed (non-UNDETERMINED) criticality requires a "
                    "non-empty verbatim rationale")
            if not (rationale_source in _RATIONALE_SOURCE_FIXED
                    or (isinstance(rationale_source, str)
                        and rationale_source.startswith(_RATIONALE_SOURCE_REUSED_PREFIX)
                        and len(rationale_source) > len(_RATIONALE_SOURCE_REUSED_PREFIX))):
                raise ValueError(
                    f"invalid rationale_source: {rationale_source!r}")
        else:  # deferred — carries no category and no rationale (§4/§6.1)
            if category is not None:
                raise ValueError(
                    "a deferred criticality action carries no category")
            rationale_verbatim = None
            rationale_source = None
        record = CriticalityConfirmation(
            confirmation_id=len(self.criticality_confirmations) + 1,
            requirement_id=requirement_id, action=action, category=category,
            rationale_verbatim=rationale_verbatim,
            rationale_source=rationale_source, iteration=iteration,
        )
        self.criticality_confirmations.append(record)
        return record

    def current_criticality_confirmation(self, requirement_id):
        """Current lookup (contract §6.2): the latest recorded explicit action
        for requirement_id, or None. Later actions govern by append order;
        earlier records remain retained for in-session traceability."""
        latest = None
        for record in self.criticality_confirmations:
            if record.requirement_id == requirement_id:
                latest = record
        return latest

    def has_unresolved_contradiction(self, gap_context):
        """True if any record in the given gap_context carries an (unresolved)
        contradiction edge. The first contract has no resolution workflow, so any
        marked contradiction is, by definition, still unresolved."""
        return any(
            r.contradicts for r in self.assertions
            if r.gap_context == gap_context
        )
