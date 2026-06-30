"""
IdeaState — MVP data structure only.
Scope: electronics/electrical, LEVEL 0-2.
Governed by: MVP_SCOPE_FREEZE.md
"""

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

# --- Interaction dispositions: exactly the six preserved owner actions ---
DISPOSITION_ANSWERED               = "answered"
DISPOSITION_UNKNOWN                = "unknown"
DISPOSITION_DEFERRED               = "deferred"
DISPOSITION_PROVISIONAL_ASSUMPTION = "provisional_assumption"
DISPOSITION_SPECIALIST_REQUESTED   = "specialist_requested"
DISPOSITION_EVIDENCE_REQUESTED     = "evidence_requested"

INTERACTION_DISPOSITIONS = frozenset({
    DISPOSITION_ANSWERED, DISPOSITION_UNKNOWN, DISPOSITION_DEFERRED,
    DISPOSITION_PROVISIONAL_ASSUMPTION, DISPOSITION_SPECIALIST_REQUESTED,
    DISPOSITION_EVIDENCE_REQUESTED,
})

# Durable pending state for the two request actions (None for the others).
_PENDING_BY_DISPOSITION = {
    DISPOSITION_SPECIALIST_REQUESTED: "specialist",
    DISPOSITION_EVIDENCE_REQUESTED:   "evidence",
}

# Default provenance is derived ONLY from the owner action that created the
# record (the action itself is the source fact) — never from text, vocabulary,
# quality, maturity, or gap status. An explicit provenance argument always wins.
# Owner-asserting actions default to OWNER_STATED; the non-asserting actions
# (unknown / deferred / specialist_requested / evidence_requested) assert no
# content and so remain LEGACY_UNSPECIFIED.
_DEFAULT_PROVENANCE_BY_DISPOSITION = {
    DISPOSITION_ANSWERED:               OWNER_STATED,
    DISPOSITION_PROVISIONAL_ASSUMPTION: OWNER_STATED,
}

# Validation levels treated as "validated" (i.e. not owner-unvalidated) by the
# pure derived-readiness recomputation. UNVALIDATED is deliberately excluded.
VALIDATED_STATUSES = frozenset({
    SPECIALIST_REVIEWED, EMPIRICALLY_DEMONSTRATED, INDEPENDENTLY_VERIFIED,
})


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
    path           : str                    = "legacy_undesignated_current_behavior"

    # Per-experiment owner-defined success criteria (planning metadata only).
    # Keyed by stable prototype experiment_id -> SuccessCriterion. Default empty
    # for backward compatibility. NOT Evidence, NOT graded, NOT read by
    # progression/maturity, NOT written to the ILT-002 transcript.
    # SuccessCriterion is defined above and the module evaluates annotations
    # eagerly (no `from __future__ import annotations`), so the parameterized
    # form is safe — matching the Gap.evidence: list[Evidence] precedent.
    success_criteria : dict[str, SuccessCriterion] = field(default_factory=dict)

    # Increment 2 append-only interaction/assertion ledger. Distinct from the
    # legacy compatibility fields (known_problem/known_mechanism/gaps/maturity):
    # this is the durable disposition history, not progression state. Empty by
    # default and persistence-independent (in-memory only).
    assertions : list = field(default_factory=list)

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
                           responsibility=None):
        """Append a durable disposition record for one of the six owner actions.

        Append-only: never mutates an existing record and never removes one. Has
        NO effect on maturity, lifecycle, gaps, transitions, or the transcript.
        Provenance, when not given explicitly, is derived ONLY from the action
        (never from text/quality/maturity). Returns the new record.
        """
        if action not in INTERACTION_DISPOSITIONS:
            raise ValueError(f"unknown interaction action: {action!r}")
        if provenance is None:
            provenance = _DEFAULT_PROVENANCE_BY_DISPOSITION.get(
                action, LEGACY_UNSPECIFIED)
        # Responsibility is stored EXPLICITLY only for owner-created records
        # (contract §3.4): when this record is owner-stated, the owner is
        # responsible. Otherwise it is left None and remains DERIVED by the
        # existing display behavior (web.responsibility_labels) — never fabricated.
        if responsibility is None and provenance == OWNER_STATED:
            responsibility = OWNER_INPUT
        record_id = f"rec_{len(self.assertions) + 1}"   # stable; append-only
        record = AssertionRecord(
            record_id=record_id, disposition=action, content=content,
            gap_context=gap_context, iteration=iteration, provenance=provenance,
            validation_status=validation_status, quality=quality,
            pending=_PENDING_BY_DISPOSITION.get(action),
            responsibility=responsibility, resolves_gap=False,
        )
        self.assertions.append(record)
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

    def mark_contradiction(self, record_id_a, record_id_b):
        """Mark two existing records as mutually contradictory. Non-destructive:
        both records are retained. Rejects unknown record ids (no invalid edges)
        and rejects a self-contradiction — a record cannot contradict itself, so
        no self-edge is ever created (F-5). Repeated valid calls are idempotent."""
        a = self._require_record(record_id_a)
        b = self._require_record(record_id_b)
        if record_id_a == record_id_b:
            raise ValueError(
                f"a record cannot contradict itself: {record_id_a!r}")
        if record_id_b not in a.contradicts:
            a.contradicts.append(record_id_b)
        if record_id_a not in b.contradicts:
            b.contradicts.append(record_id_a)

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

    def has_unresolved_contradiction(self, gap_context):
        """True if any record in the given gap_context carries an (unresolved)
        contradiction edge. The first contract has no resolution workflow, so any
        marked contradiction is, by definition, still unresolved."""
        return any(
            r.contradicts for r in self.assertions
            if r.gap_context == gap_context
        )
