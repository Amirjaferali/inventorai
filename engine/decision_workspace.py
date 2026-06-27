"""
engine/decision_workspace.py

FDC-001 first increment — Technical Decision Workspace domain model.

Pure, in-memory, deterministic domain logic for ONE bounded technical decision
(the bicycle braking-detection architecture case). Implements the accepted
specification:
  docs/product/FDC-001_FIRST_INCREMENT_IMPLEMENTATION_SPECIFICATION.md

Scope / prohibitions (enforced by construction):
- in-memory only; no database, filesystem persistence, network, or external API;
- NO session persistence: this module imports nothing from engine.session_store
  and writes no durable state;
- NO benchmark execution and no benchmark result is represented;
- the lane may NOT issue a final technical selection: the status values
  `technically_selected`, `approved`, `validated`, `certified`,
  `production_ready`, and `frozen` are never produced as an output status;
- owner preference records preference only and never becomes a technical
  selection (owner_preferred != technically_selected);
- missing information is recorded only as a Gap, never as a stored input that
  asserts content;
- operator-reported and external inputs are explicitly UNVERIFIED.

Conventions follow the existing repository style: dataclasses plus module-level
string constants (mirroring engine/idea_state.py and engine/enums.py); no
enum.Enum is introduced.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import json
import uuid

SCHEMA_VERSION = "fdc001-decision-workspace-v1"
EXPORT_FORMAT = "json"

# --- claim_class (what the input asserts) -------------------------------------
OBSERVED_FACT = "observed_fact"
OWNER_REQUIREMENT = "owner_requirement"
OPERATOR_REPORTED_RESULT = "operator_reported_result"
ASSUMPTION = "assumption"
EXTERNAL_REFERENCE = "external_reference"
UNSUPPORTED_CLAIM = "unsupported_claim"
MISSING_INFORMATION = "missing_information"   # only ever a Gap, never a stored input
CONSTRAINT = "constraint"

CLAIM_CLASSES = {
    OBSERVED_FACT, OWNER_REQUIREMENT, OPERATOR_REPORTED_RESULT, ASSUMPTION,
    EXTERNAL_REFERENCE, UNSUPPORTED_CLAIM, MISSING_INFORMATION, CONSTRAINT,
}
# Claim classes that may be stored as a ClaimItem in `inputs`.
STORABLE_INPUT_CLAIM_CLASSES = {
    OBSERVED_FACT, OWNER_REQUIREMENT, OPERATOR_REPORTED_RESULT, ASSUMPTION,
    EXTERNAL_REFERENCE, UNSUPPORTED_CLAIM, CONSTRAINT,
}

# --- provenance (where the input came from) -----------------------------------
SEEDED_OWNER_CONTEXT = "seeded_owner_context"
OPERATOR_ENTERED = "operator_entered"
PLATFORM_PROPOSED = "platform_proposed"
DERIVED_BY_RULE = "derived_by_rule"

PROVENANCES = {
    SEEDED_OWNER_CONTEXT, OPERATOR_ENTERED, PLATFORM_PROPOSED, DERIVED_BY_RULE,
}

# --- explicitly-unverified labels (spec §12) ----------------------------------
OPERATOR_REPORTED_UNVERIFIED = "operator_reported_unverified"
EXTERNAL_REFERENCE_UNVERIFIED = "external_reference_unverified"

# --- option_status ------------------------------------------------------------
ACTIVE = "active"
ELIMINATED = "eliminated"
DEFERRED = "deferred"
BLOCKED = "blocked"

# --- disposition_basis (spec §13) ---------------------------------------------
INCOMPATIBLE_WITH_RECORDED_REQUIREMENT = "incompatible_with_recorded_requirement"
DEFERRED_PENDING_INPUT = "deferred_pending_input"
DISP_BLOCKED_BY_EVIDENCE_GAP = "blocked_by_evidence_gap"

# --- constraint_strength ------------------------------------------------------
PREFERENCE = "preference"
SOFT_CONSTRAINT = "soft_constraint"
MANDATORY_CONSTRAINT = "mandatory_constraint"

# --- readiness_status (spec §5) -----------------------------------------------
INSUFFICIENT_INFORMATION = "insufficient_information"
BLOCKED_BY_EVIDENCE_GAP = "blocked_by_evidence_gap"
COMPARISON_IN_PROGRESS = "comparison_in_progress"
DECISION_READY_FOR_OWNER_REVIEW = "decision_ready_for_owner_review"

# Prohibited output statuses (never produced by this lane).
PROHIBITED_STATUS_VALUES = {
    "technically_selected", "approved", "validated", "certified",
    "production_ready", "frozen",
}

# User-facing label only (never a stored status).
REVIEW_REQUIRED_LABEL = "REVIEW REQUIRED"

# --- blocking_reasons codes (spec §5) -----------------------------------------
MISSING_INSTALLATION_CONSTRAINT = "missing_installation_constraint"
MISSING_FALSE_POSITIVE_TOLERANCE = "missing_false_positive_tolerance"
MISSING_PHYSICAL_OR_CALIBRATION_INFORMATION = "missing_physical_or_calibration_information"
UNRESOLVED_EVIDENCE_CONFLICT = "unresolved_evidence_conflict"
OWNER_PREFERENCE_CONFLICTS_WITH_READINESS = "owner_preference_conflicts_with_readiness"
CANDIDATE_NOT_YET_COMPARABLE = "candidate_not_yet_comparable"
UNEVALUABLE_MANDATORY_CONSTRAINT = "unevaluable_mandatory_constraint"

# --- change_type (spec §10) ---------------------------------------------------
INPUT_ADDED = "input_added"
INPUT_UPDATED = "input_updated"
INPUT_REMOVED = "input_removed"
CONSTRAINT_ADDED = "constraint_added"
CONSTRAINT_UPDATED = "constraint_updated"
CONSTRAINT_REMOVED = "constraint_removed"
GAP_RESOLVED = "gap_resolved"
GAP_RECLASSIFIED = "gap_reclassified"
CONFLICT_RESOLVED = "conflict_resolved"
OWNER_PREFERENCE_SET = "owner_preference_set"
OWNER_PREFERENCE_CLEARED = "owner_preference_cleared"
CANDIDATE_STATUS_CHANGED = "candidate_status_changed"

# --- FDC-002 second increment: evidence claim classes (user-selectable) -------
# Only these two unverified classes may be entered as external evidence;
# observed_fact is explicitly forbidden for evidence entry.
EVIDENCE_CLAIM_CLASSES = {OPERATOR_REPORTED_RESULT, EXTERNAL_REFERENCE}

# --- FDC-002 verification status (system-controlled; never user-supplied) ------
EVIDENCE_VERIFICATION_UNVERIFIED = "unverified"

# --- FDC-002 gap-assessment values --------------------------------------------
SUPPORTS_RESOLUTION = "supports_resolution"
PARTIALLY_ADDRESSES = "partially_addresses"
CONTRADICTS_ASSUMPTION = "contradicts_assumption"
INSUFFICIENT = "insufficient"
ASSESSMENT_VALUES = {
    SUPPORTS_RESOLUTION, PARTIALLY_ADDRESSES, CONTRADICTS_ASSUMPTION, INSUFFICIENT,
}

# --- FDC-002 resolution decisions ---------------------------------------------
RESOLVED = "resolved"
REMAINS_BLOCKING = "remains_blocking"
RECLASSIFIED_NONBLOCKING = "reclassified_nonblocking"
RESOLUTION_DECISIONS = {RESOLVED, REMAINS_BLOCKING, RECLASSIFIED_NONBLOCKING}
# A gap transitions to non-blocking only under these two decisions.
RESOLUTION_DECISIONS_CLEARING = {RESOLVED, RECLASSIFIED_NONBLOCKING}

# --- FDC-002 history change types ----------------------------------------------
EVIDENCE_ADDED = "evidence_added"
GAP_ASSESSED = "gap_assessed"
GAP_RESOLVED_VIA_EVIDENCE = "gap_resolved_via_evidence"

# --- FDC-002 deterministic blocker-clearing guidance (keyed by blocker code) ---
# Codes with no entry render no guidance (never invented text).
BLOCKER_CLEARING_GUIDANCE = {
    MISSING_PHYSICAL_OR_CALIBRATION_INFORMATION: (
        "Record an externally-produced operator or physical observation/result "
        "against this gap, then make an explicit assessment and resolution "
        "decision. This lane performs no verification; recorded evidence is "
        "operator-reported and unverified."
    ),
}

# --- FDC-002 export limitation disclaimer (appended at export time) ------------
FDC002_EXPORT_LIMITATION = (
    "no verification performed by this lane; recorded evidence is "
    "operator-reported and unverified"
)

# --- fixed first-case definition ----------------------------------------------
DECISION_QUESTION = (
    "Which braking-detection architecture should the bicycle automatic brake "
    "light use?"
)
WIRED_BRAKE_LEVER_SWITCH = "wired_brake_lever_switch"
ACCELEROMETER_INFERENCE = "accelerometer_inference"
WHEEL_SPEED_INFERENCE = "wheel_speed_inference"
CANDIDATE_NAMES = (
    WIRED_BRAKE_LEVER_SWITCH, ACCELEROMETER_INFERENCE, WHEEL_SPEED_INFERENCE,
)

EXPORT_LIMITATIONS = [
    "in-memory only; not durable",
    "restart restoration not supported",
    "no benchmark run",
    "no external retrieval",
    "no physical testing",
    "no verified evidence",
    "no final technical selection",
    "advisory only",
]


def _new_id(prefix):
    return prefix + "-" + uuid.uuid4().hex[:12]


def _classify_blocking_gap_code(text):
    """Deterministic blocker code for a readiness-blocking gap's text. Single
    source of truth shared by readiness-reason derivation and the FDC-002
    user-facing route guard, so both classify a gap identically — the route guard
    therefore protects exactly the gaps that surface as a
    `missing_physical_or_calibration_information` blocking reason (no divergent
    second classifier).

    BOUNDED-SCOPE LIMITATION (intentional historical FDC-001 policy, preserved):
    the final `return` defaults any gap text matching none of the keyword groups
    to `missing_physical_or_calibration_information`. This is the original
    first-increment readiness-derivation behavior (this function was extracted
    behavior-identically from `_derive_blocking_reasons`), so changing it would
    silently alter historical readiness. It is preserved deliberately. In the
    bounded model this default is unreachable for any user-facing gap: gaps are
    only the two fixed seeded gaps and there is no route that adds an arbitrary
    gap (`add_gap` is programmatic/test-only), so every user-facing gap matches a
    positive keyword group. An arbitrary-text gap added programmatically would be
    classified physical by this same historical default for BOTH readiness and the
    guard, consistently — never a divergence."""
    low = text.lower()
    if "false-positive" in low or "false positive" in low or "false-braking" in low:
        return MISSING_FALSE_POSITIVE_TOLERANCE
    if ("calibration" in low or "physical" in low or "field" in low
            or "bench" in low):
        return MISSING_PHYSICAL_OR_CALIBRATION_INFORMATION
    if "wire" in low or "install" in low:
        return MISSING_INSTALLATION_CONSTRAINT
    return MISSING_PHYSICAL_OR_CALIBRATION_INFORMATION


# ------------------------------------------------------------------ dataclasses
@dataclass
class ClaimItem:
    claim_id: str
    text: str
    claim_class: str
    provenance: str
    decision_relevant: bool = False
    confirmed: bool = False
    source_label: Optional[str] = None
    candidate_ids: list = field(default_factory=list)

    @property
    def display_label(self):
        if self.claim_class == OPERATOR_REPORTED_RESULT:
            return OPERATOR_REPORTED_UNVERIFIED
        if self.claim_class == EXTERNAL_REFERENCE:
            return EXTERNAL_REFERENCE_UNVERIFIED
        return self.claim_class

    def to_dict(self):
        return {
            "claim_id": self.claim_id,
            "text": self.text,
            "claim_class": self.claim_class,
            "provenance": self.provenance,
            "decision_relevant": self.decision_relevant,
            "confirmed": self.confirmed,
            "source_label": self.source_label,
            "candidate_ids": list(self.candidate_ids),
            "display_label": self.display_label,
        }


@dataclass
class Constraint:
    constraint_id: str
    text: str
    constraint_strength: str
    provenance: str
    confirmed: bool = False
    candidate_ids: list = field(default_factory=list)

    def to_dict(self):
        return {
            "constraint_id": self.constraint_id,
            "text": self.text,
            "constraint_strength": self.constraint_strength,
            "provenance": self.provenance,
            "confirmed": self.confirmed,
            "candidate_ids": list(self.candidate_ids),
        }


@dataclass
class Gap:
    gap_id: str
    text: str
    blocks_readiness: bool = True
    reclassification_rationale: Optional[str] = None

    def to_dict(self):
        return {
            "gap_id": self.gap_id,
            "text": self.text,
            "blocks_readiness": self.blocks_readiness,
            "reclassification_rationale": self.reclassification_rationale,
        }


@dataclass
class Risk:
    risk_id: str
    text: str
    candidate_ids: list = field(default_factory=list)

    def to_dict(self):
        return {
            "risk_id": self.risk_id,
            "text": self.text,
            "candidate_ids": list(self.candidate_ids),
        }


@dataclass
class OwnerPreference:
    candidate_id: str
    rationale: Optional[str] = None

    def to_dict(self):
        # owner_preferred records preference ONLY; never a technical selection.
        return {"candidate_id": self.candidate_id, "rationale": self.rationale}


@dataclass
class BlockingReason:
    code: str
    text: str
    affected_scope: str               # "decision" | "candidate"
    affected_candidate_id: Optional[str] = None
    # Optional: the constraint a blocker is tied to (e.g. an unevaluable
    # confirmed mandatory constraint). Defaults to None for all other reasons.
    affected_constraint_id: Optional[str] = None

    def to_dict(self):
        return {
            "code": self.code,
            "text": self.text,
            "affected_scope": self.affected_scope,
            "affected_candidate_id": self.affected_candidate_id,
            "affected_constraint_id": self.affected_constraint_id,
        }


@dataclass
class Candidate:
    candidate_id: str
    name: str
    option_status: str = ACTIVE
    disposition_reason: Optional[str] = None
    disposition_basis: Optional[str] = None

    def to_dict(self):
        return {
            "candidate_id": self.candidate_id,
            "name": self.name,
            "option_status": self.option_status,
            "disposition_reason": self.disposition_reason,
            "disposition_basis": self.disposition_basis,
        }


@dataclass
class ChangeEvent:
    event_id: str
    revision: int
    change_type: str
    target_id: Optional[str]
    summary: str
    prior_readiness_status: str
    new_readiness_status: str
    # Optional per-event detail payload. Defaults to None for every event;
    # only events that must preserve extra truthful state (e.g. a gap
    # reclassification recording previous/new blocking value + rationale)
    # populate it. Smallest change compatible with the existing design.
    details: Optional[dict] = None

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "revision": self.revision,
            "change_type": self.change_type,
            "target_id": self.target_id,
            "summary": self.summary,
            "prior_readiness_status": self.prior_readiness_status,
            "new_readiness_status": self.new_readiness_status,
            "details": dict(self.details) if self.details else None,
        }


@dataclass
class ChangeImpactSummary:
    changed_item: str
    affected_candidates: list
    affected_gaps_or_blockers: list
    prior_readiness: str
    new_readiness: str

    def to_dict(self):
        return {
            "changed_item": self.changed_item,
            "affected_candidates": list(self.affected_candidates),
            "affected_gaps_or_blockers": list(self.affected_gaps_or_blockers),
            "prior_readiness": self.prior_readiness,
            "new_readiness": self.new_readiness,
        }


@dataclass(frozen=True)
class EvidenceItem:
    """FDC-002: one externally-produced, explicitly-unverified evidence item
    recorded against an existing gap. verification_status is system-controlled
    and never caller-supplied (§7.4).

    Immutable epistemic record: this is a `frozen` dataclass so no truth-bearing
    field (verification_status, linked_gap_id, text, claim_class, provenance,
    candidate_ids, ...) can be reassigned after a successful creation. The only
    collection field, `candidate_ids`, is stored as an immutable tuple (its
    elements are immutable str ids) so the nested collection cannot be mutated in
    place either; it is still exported as a JSON list by `to_dict`."""
    evidence_id: str
    linked_gap_id: str
    text: str
    claim_class: str
    provenance: str
    verification_status: str = EVIDENCE_VERIFICATION_UNVERIFIED
    method: Optional[str] = None
    source_label: Optional[str] = None
    evidence_version: Optional[str] = None
    limitations: Optional[str] = None
    candidate_ids: tuple = field(default_factory=tuple)
    decision_relevant: bool = False

    def __post_init__(self):
        # §7.4 defensive guarantee: verification_status is permanently
        # `unverified`. The public mutation never supplies any other value, but if
        # a future revision ever did, construction is rejected here (frozen blocks
        # later reassignment), so the value can never become anything else.
        if self.verification_status != EVIDENCE_VERIFICATION_UNVERIFIED:
            raise DecisionError(
                "verification_status is system-controlled and must remain %r"
                % EVIDENCE_VERIFICATION_UNVERIFIED)
        # The class ITSELF guarantees nested-collection immutability regardless of
        # how it is constructed (not only via add_evidence): normalize
        # candidate_ids to an immutable tuple here. frozen=True forbids ordinary
        # assignment, so the controlled `object.__setattr__` is used inside
        # __post_init__. §7.1 types these as string candidate ids, so reject any
        # non-string member rather than silently stringifying an arbitrary object.
        ids = tuple(self.candidate_ids)
        for cid in ids:
            if not isinstance(cid, str):
                raise DecisionError("candidate_ids members must be strings")
        object.__setattr__(self, "candidate_ids", ids)

    def to_dict(self):
        return {
            "evidence_id": self.evidence_id,
            "linked_gap_id": self.linked_gap_id,
            "text": self.text,
            "claim_class": self.claim_class,
            "provenance": self.provenance,
            "verification_status": self.verification_status,
            "method": self.method,
            "source_label": self.source_label,
            "evidence_version": self.evidence_version,
            "limitations": self.limitations,
            "candidate_ids": list(self.candidate_ids),
            "decision_relevant": self.decision_relevant,
        }


@dataclass(frozen=True)
class GapAssessment:
    """FDC-002: an explicit assessment of an existing gap against >=1 linked
    evidence item plus a separate resolution decision.

    Immutable epistemic record: this is a `frozen` dataclass so no field
    (assessment, resolution_decision, evidence_ids, ...) can be reassigned after
    a successful creation. `evidence_ids` is stored as an immutable tuple (its
    elements are immutable str ids) so the nested collection cannot be mutated in
    place either; it is still exported as a JSON list by `to_dict`."""
    assessment_id: str
    gap_id: str
    evidence_ids: tuple
    assessment: str
    rationale: str
    resolution_decision: str
    resolution_rationale: Optional[str] = None

    def __post_init__(self):
        # The class ITSELF guarantees nested-collection immutability regardless of
        # how it is constructed (not only via assess_gap): normalize evidence_ids
        # to an immutable tuple here. frozen=True forbids ordinary assignment, so
        # the controlled `object.__setattr__` is used inside __post_init__. §7.2
        # types these as evidence ids (strings), so reject any non-string member
        # rather than silently stringifying an arbitrary object.
        ids = tuple(self.evidence_ids)
        for eid in ids:
            if not isinstance(eid, str):
                raise DecisionError("evidence_ids members must be strings")
        object.__setattr__(self, "evidence_ids", ids)

    def to_dict(self):
        return {
            "assessment_id": self.assessment_id,
            "gap_id": self.gap_id,
            "evidence_ids": list(self.evidence_ids),
            "assessment": self.assessment,
            "rationale": self.rationale,
            "resolution_decision": self.resolution_decision,
            "resolution_rationale": self.resolution_rationale,
        }


class DecisionError(ValueError):
    """Raised when an operation would violate the spec's invariants."""


class DecisionRecord:
    """One bounded technical decision, evolved deterministically in memory."""

    def __init__(self, decision_id=None):
        self.decision_id = decision_id or _new_id("decision")
        self.decision_question = DECISION_QUESTION
        self.revision = 0
        self.candidates = [
            Candidate(_new_id("cand"), name) for name in CANDIDATE_NAMES
        ]
        self.inputs = []            # list[ClaimItem]
        self.constraints = []       # list[Constraint]
        self.gaps = []              # list[Gap]
        self.evidence = []          # list[EvidenceItem]  (FDC-002)
        self.gap_assessments = []   # list[GapAssessment] (FDC-002)
        self.risks = []             # list[Risk]
        self.owner_preference = None
        self.blocking_reasons = []  # list[BlockingReason] (derived each recompute)
        self.history = []           # list[ChangeEvent]
        self.change_impact_summary = None
        self.readiness_status = INSUFFICIENT_INFORMATION
        self._open_conflicts = []   # list[str] conflict ids
        self._seed_owner_context()
        # Initial deterministic readiness (no change event for seeding).
        self.readiness_status = self._compute_readiness()

    # -- seeding ---------------------------------------------------------------
    def _seed_owner_context(self):
        """Seed the inventor's stated context as owner requirements / assumptions.

        These are recorded with provenance=seeded_owner_context and are NEVER
        observed facts. They are general (not per-candidate decision-relevant
        comparison inputs), so the initial readiness is insufficient_information
        rather than a forced block.
        """
        self.inputs.append(ClaimItem(
            _new_id("claim"),
            "Automatic brake indication without manually pressing a control.",
            OWNER_REQUIREMENT, SEEDED_OWNER_CONTEXT, decision_relevant=False,
        ))
        self.inputs.append(ClaimItem(
            _new_id("claim"),
            "Avoid or minimize a wire to the brake lever.",
            OWNER_REQUIREMENT, SEEDED_OWNER_CONTEXT, decision_relevant=False,
        ))
        self.inputs.append(ClaimItem(
            _new_id("claim"),
            "Rough roads and vibration are an owner-stated concern.",
            ASSUMPTION, SEEDED_OWNER_CONTEXT, decision_relevant=False,
        ))
        # Named missing information lives ONLY as gaps (never as evidence).
        self.gaps.append(Gap(
            _new_id("gap"),
            "Acceptable false-positive (false-braking) rate is unknown.",
            blocks_readiness=True,
        ))
        self.gaps.append(Gap(
            _new_id("gap"),
            "No physical / calibration / field result is available.",
            blocks_readiness=True,
        ))

    # -- helpers ---------------------------------------------------------------
    def _candidate(self, candidate_id):
        for c in self.candidates:
            if c.candidate_id == candidate_id:
                return c
        raise DecisionError("unknown candidate_id: %r" % candidate_id)

    def _gap(self, gap_id):
        for g in self.gaps:
            if g.gap_id == gap_id:
                return g
        raise DecisionError("unknown gap_id: %r" % gap_id)

    def _evidence_item(self, evidence_id):
        for e in self.evidence:
            if e.evidence_id == evidence_id:
                return e
        raise DecisionError("unknown evidence_id: %r" % evidence_id)

    def gap_blocker_code(self, gap_id):
        """The deterministic blocker code for an existing gap. Used by the
        FDC-002 user-facing route guard to decide whether the legacy bare-text
        route must reject clearing/reclassifying a physical/calibration gap.
        Raises DecisionError for an unknown gap_id (read-only; never mutates)."""
        g = self._gap(gap_id)
        return _classify_blocking_gap_code(g.text)

    def _input(self, claim_id):
        for ci in self.inputs:
            if ci.claim_id == claim_id:
                return ci
        raise DecisionError("unknown claim_id: %r" % claim_id)

    def _validate_candidate_ids(self, candidate_ids):
        """Every supplied candidate id must reference a known candidate.
        Raises before any mutation; returns a fresh list on success."""
        if not candidate_ids:
            return []
        known = {c.candidate_id for c in self.candidates}
        unknown = [cid for cid in candidate_ids if cid not in known]
        if unknown:
            raise DecisionError("unknown candidate_id(s): %r" % unknown)
        return list(candidate_ids)

    def _covered(self, candidate):
        """A candidate is comparable when >=1 decision_relevant input or
        constraint references it."""
        cid = candidate.candidate_id
        for ci in self.inputs:
            if ci.decision_relevant and cid in ci.candidate_ids:
                return True
        for con in self.constraints:
            if cid in con.candidate_ids:
                return True
        return False

    def _min_comparison_context(self):
        """At least two ACTIVE candidates are each covered by >=1
        decision-relevant input/constraint. (All-three-accounted-for is a
        separate rule-3 gate, not part of minimum context.)"""
        active = [c for c in self.candidates if c.option_status == ACTIVE]
        if len(active) < 2:
            return False
        covered_active = [c for c in active if self._covered(c)]
        return len(covered_active) >= 2

    def _all_candidates_accounted_for(self):
        for c in self.candidates:
            if c.option_status == ACTIVE:
                if not self._covered(c):
                    return False
            else:
                # eliminated / deferred / blocked must carry a basis
                if not c.disposition_basis:
                    return False
        return True

    def _decision_relevant_nonblocking_gap_remains(self):
        return any((not g.blocks_readiness) for g in self.gaps)

    # -- readiness (spec §5 ordered decision table) ----------------------------
    def _compute_readiness(self):
        self.blocking_reasons = self._derive_blocking_reasons()
        # Rule 1
        if not self._min_comparison_context():
            return INSUFFICIENT_INFORMATION
        # Rule 2
        if any(g.blocks_readiness for g in self.gaps):
            return BLOCKED_BY_EVIDENCE_GAP
        if self._mandatory_constraint_unevaluable():
            return BLOCKED_BY_EVIDENCE_GAP
        # Rule 3
        if (not self._all_candidates_accounted_for()
                or self._decision_relevant_nonblocking_gap_remains()
                or self._open_conflicts):
            return COMPARISON_IN_PROGRESS
        # Rule 4
        return DECISION_READY_FOR_OWNER_REVIEW

    def _unevaluable_mandatory_constraints(self):
        """The confirmed mandatory constraints that have no evaluable
        known-candidate scope. A confirmed mandatory constraint is evaluable
        only when it is scoped to at least one known candidate, i.e. there is a
        relevant candidate scope to evaluate it against. One with no such scope
        cannot be evaluated (it is not silently treated as satisfied, and no
        technical evidence is invented). Unconfirmed mandatory constraints do
        not gate readiness — they are not yet asserted. Single source of truth
        for both the readiness gate and the blocking-reason derivation."""
        known_ids = {c.candidate_id for c in self.candidates}
        out = []
        for con in self.constraints:
            if con.constraint_strength != MANDATORY_CONSTRAINT or not con.confirmed:
                continue
            scoped = [cid for cid in con.candidate_ids if cid in known_ids]
            if not scoped:
                out.append(con)
        return out

    def _mandatory_constraint_unevaluable(self):
        """Smallest deterministic readiness gate: True iff any confirmed
        mandatory constraint has no evaluable known-candidate scope."""
        return bool(self._unevaluable_mandatory_constraints())

    def _derive_blocking_reasons(self):
        reasons = []
        for g in self.gaps:
            if not g.blocks_readiness:
                continue
            code = _classify_blocking_gap_code(g.text)
            reasons.append(BlockingReason(code, g.text, "decision", None))
        for con in self._unevaluable_mandatory_constraints():
            reasons.append(BlockingReason(
                UNEVALUABLE_MANDATORY_CONSTRAINT,
                "Confirmed mandatory constraint cannot be evaluated against any "
                "known candidate scope.",
                "decision", None, affected_constraint_id=con.constraint_id))
        for cid in self._open_conflicts:
            reasons.append(BlockingReason(
                UNRESOLVED_EVIDENCE_CONFLICT,
                "Recorded inputs disagree (conflict %s)." % cid,
                "decision", None))
        if self._owner_preference_conflicts():
            reasons.append(BlockingReason(
                OWNER_PREFERENCE_CONFLICTS_WITH_READINESS,
                "Owner preference conflicts with current candidate disposition.",
                "candidate",
                self.owner_preference.candidate_id if self.owner_preference else None))
        for c in self.candidates:
            if c.option_status == ACTIVE and not self._covered(c):
                reasons.append(BlockingReason(
                    CANDIDATE_NOT_YET_COMPARABLE,
                    "Candidate %s lacks inputs to be compared." % c.name,
                    "candidate", c.candidate_id))
        return reasons

    def _owner_preference_conflicts(self):
        if not self.owner_preference:
            return False
        try:
            c = self._candidate(self.owner_preference.candidate_id)
        except DecisionError:
            return True
        return c.option_status in (ELIMINATED, BLOCKED)

    # -- change recording ------------------------------------------------------
    def _record(self, change_type, target_id, summary,
                affected_candidates=None, affected_gaps_or_blockers=None,
                details=None):
        prior = self.readiness_status
        self.revision += 1
        new = self._compute_readiness()
        self.readiness_status = new
        ev = ChangeEvent(_new_id("evt"), self.revision, change_type, target_id,
                         summary, prior, new, details=details)
        self.history.append(ev)
        self.change_impact_summary = ChangeImpactSummary(
            changed_item="%s:%s" % (change_type, target_id or ""),
            affected_candidates=affected_candidates or [],
            affected_gaps_or_blockers=affected_gaps_or_blockers or [],
            prior_readiness=prior,
            new_readiness=new,
        )
        return ev

    # -- mutations -------------------------------------------------------------
    def add_input(self, text, claim_class, provenance, decision_relevant=False,
                  confirmed=False, source_label=None, candidate_ids=None):
        if not text or not str(text).strip():
            raise DecisionError("input text must not be blank")
        if claim_class not in CLAIM_CLASSES:
            raise DecisionError("invalid claim_class: %r" % claim_class)
        if claim_class == MISSING_INFORMATION:
            raise DecisionError(
                "missing information must be recorded as a Gap, not an input")
        if claim_class not in STORABLE_INPUT_CLAIM_CLASSES:
            raise DecisionError("claim_class not storable as input: %r" % claim_class)
        if provenance not in PROVENANCES:
            raise DecisionError("invalid provenance: %r" % provenance)
        # Validate candidate scope before any mutation (atomic).
        validated_ids = self._validate_candidate_ids(candidate_ids)
        ci = ClaimItem(_new_id("claim"), text, claim_class, provenance,
                       decision_relevant=bool(decision_relevant),
                       confirmed=bool(confirmed), source_label=source_label,
                       candidate_ids=validated_ids)
        self.inputs.append(ci)
        self._record(INPUT_ADDED, ci.claim_id, "added %s input" % claim_class,
                     affected_candidates=list(ci.candidate_ids))
        return ci

    def update_input(self, claim_id, text=None, decision_relevant=None,
                     confirmed=None, candidate_ids=None):
        # Resolve first, then validate EVERY supplied value before mutating any
        # field. On any validation failure the input fields, revision, history,
        # readiness, and change-impact summary all remain unchanged (atomic).
        ci = self._input(claim_id)
        if text is not None and not str(text).strip():
            raise DecisionError("input text must not be blank")
        validated_ids = None
        if candidate_ids is not None:
            validated_ids = self._validate_candidate_ids(candidate_ids)
        # All supplied values passed validation -> apply, then record exactly
        # one INPUT_UPDATED event and one revision increment.
        if text is not None:
            ci.text = text
        if decision_relevant is not None:
            ci.decision_relevant = bool(decision_relevant)
        if confirmed is not None:
            ci.confirmed = bool(confirmed)
        if validated_ids is not None:
            ci.candidate_ids = validated_ids
        self._record(INPUT_UPDATED, claim_id, "updated input",
                     affected_candidates=list(ci.candidate_ids))
        return ci

    def remove_input(self, claim_id):
        ci = self._input(claim_id)
        self.inputs.remove(ci)
        self._record(INPUT_REMOVED, claim_id, "removed input",
                     affected_candidates=list(ci.candidate_ids))

    def add_constraint(self, text, constraint_strength, provenance,
                       confirmed=False, candidate_ids=None):
        if not text or not str(text).strip():
            raise DecisionError("constraint text must not be blank")
        if constraint_strength not in (PREFERENCE, SOFT_CONSTRAINT, MANDATORY_CONSTRAINT):
            raise DecisionError("invalid constraint_strength: %r" % constraint_strength)
        if provenance not in PROVENANCES:
            raise DecisionError("invalid provenance: %r" % provenance)
        # Validate candidate scope before any mutation (atomic).
        validated_ids = self._validate_candidate_ids(candidate_ids)
        con = Constraint(_new_id("con"), text, constraint_strength, provenance,
                         confirmed=bool(confirmed),
                         candidate_ids=validated_ids)
        self.constraints.append(con)
        self._record(CONSTRAINT_ADDED, con.constraint_id, "added constraint",
                     affected_candidates=list(con.candidate_ids))
        return con

    def add_gap(self, text, blocks_readiness=True):
        if not text or not str(text).strip():
            raise DecisionError("gap text must not be blank")
        g = Gap(_new_id("gap"), text, blocks_readiness=bool(blocks_readiness))
        self.gaps.append(g)
        self._record(INPUT_ADDED, g.gap_id, "added gap",
                     affected_gaps_or_blockers=[g.gap_id])
        return g

    def resolve_gap(self, gap_id):
        g = self._gap(gap_id)
        self.gaps.remove(g)
        self._record(GAP_RESOLVED, gap_id, "resolved gap",
                     affected_gaps_or_blockers=[gap_id])

    def reclassify_gap(self, gap_id, rationale):
        """Move a readiness-blocking gap to non-blocking. A rationale is
        mandatory; the gap and its rationale remain visible in history/export."""
        if not rationale or not str(rationale).strip():
            raise DecisionError(
                "reclassifying a readiness-blocking gap requires a rationale")
        g = self._gap(gap_id)
        previous_blocks_readiness = g.blocks_readiness
        g.blocks_readiness = False
        g.reclassification_rationale = rationale
        # Preserve both the prior and new blocking state (plus rationale) in
        # committed history/export. revision and prior/new readiness are already
        # carried on the ChangeEvent itself.
        self._record(GAP_RECLASSIFIED, gap_id,
                     "reclassified gap to non-blocking",
                     affected_gaps_or_blockers=[gap_id],
                     details={
                         "gap_id": gap_id,
                         "previous_blocks_readiness": previous_blocks_readiness,
                         "new_blocks_readiness": False,
                         "rationale": rationale,
                     })
        return g

    # -- FDC-002 evidence re-entry & gap assessment ----------------------------
    def add_evidence(self, linked_gap_id, text, claim_class, provenance,
                     method=None, source_label=None, evidence_version=None,
                     limitations=None, candidate_ids=None, decision_relevant=False):
        """Record ONE externally-produced evidence item against an existing gap.

        claim_class is restricted to operator_reported_result / external_reference
        (observed_fact is rejected). verification_status is system-set to
        `unverified` and is NEVER a caller-controlled parameter (§7.4). Evidence
        lives in a separate `evidence` list (not `inputs`) and entry alone changes
        no readiness. Validate-before-mutate and atomic: on any failure nothing is
        appended and no event/revision is recorded; on success exactly one
        `evidence_added` event is recorded."""
        # Evidence text is operator-entered text (§7.1, type str). Reject non-text
        # values rather than silently stringifying an arbitrary object, then store
        # the stripped string so no leading/trailing whitespace is preserved.
        if not isinstance(text, str):
            raise DecisionError("evidence text must be a string")
        text = text.strip()
        if not text:
            raise DecisionError("evidence text must not be blank")
        if claim_class not in EVIDENCE_CLAIM_CLASSES:
            raise DecisionError("unsupported evidence claim_class: %r" % claim_class)
        if provenance not in PROVENANCES:
            raise DecisionError("invalid provenance: %r" % provenance)
        # linked gap must exist (raises before any mutation)
        self._gap(linked_gap_id)
        validated_ids = self._validate_candidate_ids(candidate_ids)

        def _norm(v):
            if v is None:
                return None
            v = str(v).strip()
            return v or None

        ev = EvidenceItem(
            _new_id("ev"), linked_gap_id, text, claim_class, provenance,
            verification_status=EVIDENCE_VERIFICATION_UNVERIFIED,
            method=_norm(method), source_label=_norm(source_label),
            evidence_version=_norm(evidence_version), limitations=_norm(limitations),
            candidate_ids=tuple(validated_ids),
            decision_relevant=bool(decision_relevant))
        self.evidence.append(ev)
        self._record(EVIDENCE_ADDED, ev.evidence_id, "recorded evidence",
                     affected_candidates=list(ev.candidate_ids),
                     affected_gaps_or_blockers=[linked_gap_id],
                     details={
                         "evidence_id": ev.evidence_id,
                         "linked_gap_id": linked_gap_id,
                         "claim_class": claim_class,
                         "provenance": provenance,
                         "verification_status": EVIDENCE_VERIFICATION_UNVERIFIED,
                         "evidence_version": ev.evidence_version,
                         "limitations": ev.limitations,
                     })
        return ev

    def assess_gap(self, gap_id, evidence_ids, assessment, rationale,
                   resolution_decision, resolution_rationale=None):
        """Assess an existing gap against >=1 linked evidence item and make an
        explicit, separate resolution decision.

        A gap transitions to non-blocking ONLY for a `resolved` or
        `reclassified_nonblocking` decision backed by `assessment ==
        supports_resolution` and >=1 valid linked evidence item;
        `partially_addresses` / `contradicts_assumption` / `insufficient` cannot
        clear it, and `remains_blocking` records the assessment without changing
        gap state. Validate-before-mutate and atomic; emits EXACTLY ONE event —
        `gap_assessed` (remains_blocking) or `gap_resolved_via_evidence` (a valid
        clearing) — never both, and nothing on failure."""
        g = self._gap(gap_id)
        if assessment not in ASSESSMENT_VALUES:
            raise DecisionError("invalid assessment: %r" % assessment)
        if resolution_decision not in RESOLUTION_DECISIONS:
            raise DecisionError("invalid resolution_decision: %r" % resolution_decision)
        if not rationale or not str(rationale).strip():
            raise DecisionError("assessment rationale must not be blank")
        if not evidence_ids:
            raise DecisionError(
                "an assessment requires at least one linked evidence item")
        # Reject duplicate ids within one assessment request. The spec is silent
        # on duplicates; the conservative, non-misleading choice is to reject so
        # the recorded audit never carries duplicate evidence references (no
        # invented normalization policy is introduced).
        if len(set(evidence_ids)) != len(evidence_ids):
            raise DecisionError(
                "duplicate evidence id in a single assessment is not permitted")
        # every referenced evidence must exist AND be linked to this gap
        for eid in evidence_ids:
            ev = self._evidence_item(eid)
            if ev.linked_gap_id != gap_id:
                raise DecisionError("evidence %r is linked to a different gap" % eid)
        clearing = resolution_decision in RESOLUTION_DECISIONS_CLEARING
        if resolution_decision != REMAINS_BLOCKING:
            if not resolution_rationale or not str(resolution_rationale).strip():
                raise DecisionError(
                    "resolution rationale is required for a %s decision"
                    % resolution_decision)
        if clearing:
            if assessment != SUPPORTS_RESOLUTION:
                raise DecisionError(
                    "only a supports_resolution assessment may clear or "
                    "reclassify a gap")
            if not g.blocks_readiness:
                raise DecisionError("gap is already non-blocking")
        # All validation passed -> mutate atomically and record exactly one event.
        ga = GapAssessment(
            _new_id("ga"), gap_id, tuple(evidence_ids), assessment, rationale,
            resolution_decision,
            (str(resolution_rationale).strip() if resolution_rationale else None))
        self.gap_assessments.append(ga)
        if clearing:
            previous = g.blocks_readiness
            g.blocks_readiness = False
            if resolution_decision == RECLASSIFIED_NONBLOCKING:
                g.reclassification_rationale = ga.resolution_rationale
            self._record(GAP_RESOLVED_VIA_EVIDENCE, gap_id,
                         "gap cleared via evidence (%s)" % resolution_decision,
                         affected_gaps_or_blockers=[gap_id],
                         details={
                             "assessment_id": ga.assessment_id,
                             "gap_id": gap_id,
                             "evidence_ids": list(ga.evidence_ids),
                             "assessment": assessment,
                             "rationale": rationale,
                             "resolution_decision": resolution_decision,
                             "resolution_rationale": ga.resolution_rationale,
                             "previous_blocks_readiness": previous,
                             "new_blocks_readiness": False,
                         })
        else:
            self._record(GAP_ASSESSED, gap_id, "gap assessed (%s)" % assessment,
                         affected_gaps_or_blockers=[gap_id],
                         details={
                             "assessment_id": ga.assessment_id,
                             "gap_id": gap_id,
                             "evidence_ids": list(ga.evidence_ids),
                             "assessment": assessment,
                             "rationale": rationale,
                             "resolution_decision": resolution_decision,
                         })
        return ga

    def dispose_candidate(self, candidate_id, option_status, disposition_reason,
                          disposition_basis):
        # Atomic: validate option_status, candidate identity, and all required
        # non-active disposition fields BEFORE mutating anything. If validation
        # fails the candidate, revision, history, readiness, and change-impact
        # state remain unchanged.
        if option_status not in (ACTIVE, ELIMINATED, DEFERRED, BLOCKED):
            raise DecisionError("invalid option_status: %r" % option_status)
        c = self._candidate(candidate_id)
        if option_status != ACTIVE and not (
                disposition_basis and str(disposition_basis).strip()):
            raise DecisionError("disposition_basis required for non-active status")
        # All validation passed -> mutate.
        if option_status == ACTIVE:
            c.option_status = ACTIVE
            c.disposition_reason = None
            c.disposition_basis = None
        else:
            c.option_status = option_status
            c.disposition_reason = disposition_reason
            c.disposition_basis = disposition_basis
        self._record(CANDIDATE_STATUS_CHANGED, candidate_id,
                     "candidate status -> %s" % option_status,
                     affected_candidates=[candidate_id])
        return c

    def eliminate_for_requirement(self, candidate_id, requirement_text):
        """Contextual elimination: incompatible with a recorded requirement,
        NOT a verdict of technical invalidity (spec §13)."""
        return self.dispose_candidate(
            candidate_id, ELIMINATED,
            "Conflicts with the recorded requirement: %s" % requirement_text,
            INCOMPATIBLE_WITH_RECORDED_REQUIREMENT)

    def set_owner_preference(self, candidate_id, rationale=None):
        self._candidate(candidate_id)  # validate
        self.owner_preference = OwnerPreference(candidate_id, rationale)
        self._record(OWNER_PREFERENCE_SET, candidate_id,
                     "owner preference set (preference only)",
                     affected_candidates=[candidate_id])
        return self.owner_preference

    def clear_owner_preference(self):
        prev = self.owner_preference.candidate_id if self.owner_preference else None
        self.owner_preference = None
        self._record(OWNER_PREFERENCE_CLEARED, prev, "owner preference cleared")

    def open_conflict(self, conflict_id=None):
        cid = conflict_id or _new_id("conflict")
        self._open_conflicts.append(cid)
        self._record(INPUT_ADDED, cid, "recorded an unresolved evidence conflict",
                     affected_gaps_or_blockers=[cid])
        return cid

    def resolve_conflict(self, conflict_id):
        # Resolving a nonexistent conflict raises and records no event/revision.
        if conflict_id not in self._open_conflicts:
            raise DecisionError("unknown conflict_id: %r" % conflict_id)
        self._open_conflicts.remove(conflict_id)
        self._record(CONFLICT_RESOLVED, conflict_id, "resolved evidence conflict",
                     affected_gaps_or_blockers=[conflict_id])

    # -- user-facing label -----------------------------------------------------
    def review_required_label(self):
        """A user-facing label only; never a stored status."""
        if self.readiness_status in (INSUFFICIENT_INFORMATION,
                                     BLOCKED_BY_EVIDENCE_GAP,
                                     COMPARISON_IN_PROGRESS):
            return REVIEW_REQUIRED_LABEL
        return None

    # -- export (spec §8/§11/§12) ----------------------------------------------
    def to_record_dict(self):
        return {
            "schema_version": SCHEMA_VERSION,
            "decision_id": self.decision_id,
            "decision_question": self.decision_question,
            "revision": self.revision,
            "candidates": [c.to_dict() for c in self.candidates],
            "inputs": [i.to_dict() for i in self.inputs],
            "constraints": [c.to_dict() for c in self.constraints],
            "gaps": [g.to_dict() for g in self.gaps],
            "risks": [r.to_dict() for r in self.risks],
            "owner_preference": (self.owner_preference.to_dict()
                                 if self.owner_preference else None),
            "readiness_status": self.readiness_status,
            "review_required_label": self.review_required_label(),
            "blocking_reasons": [
                dict(b.to_dict(),
                     clearing_guidance=BLOCKER_CLEARING_GUIDANCE.get(b.code))
                for b in self.blocking_reasons
            ],
            "evidence": [e.to_dict() for e in self.evidence],
            "gap_assessments": [a.to_dict() for a in self.gap_assessments],
            "history": [e.to_dict() for e in self.history],
            "change_impact_summary": (self.change_impact_summary.to_dict()
                                      if self.change_impact_summary else None),
        }

    def to_export_dict(self):
        """Canonical export object. Exactly one authoritative timestamp lives in
        export_metadata.generated_at (stamped here, at export time)."""
        rec = self.to_record_dict()
        rec["export_metadata"] = {
            "schema_version": SCHEMA_VERSION,
            "export_format": EXPORT_FORMAT,
            "export_revision": self.revision,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "limitations": list(EXPORT_LIMITATIONS) + [FDC002_EXPORT_LIMITATION],
        }
        return rec

    def to_json(self, indent=2):
        return json.dumps(self.to_export_dict(), indent=indent, sort_keys=True)
