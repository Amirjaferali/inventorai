"""Increment 3 — Visible Next Development Step — shared pure engine derivation.

Single source of truth for the one prioritized, user-visible "next development
step" derived from Increment 2's already-recorded truthful state. Both visible
surfaces (the deliverable assembler section and the session-screen callout)
consume EXACTLY this public function — there is no second selector.

Governance (merged, binding): docs/governance/INCREMENT_3_AUTHORITY_RULINGS.md
(R-1..R-6) and the six-path INCREMENT_3_IMPLEMENTATION_CONTRACT.md.

Contract of `derive_next_development_step(state)`:
  * pure, deterministic, read-only;
  * NO Flask / route / template / session / persistence / file / database
    knowledge; NO scoring, progression, or stage-transition behavior;
  * NEVER mutates IdeaState, assertions, gaps, history, maturity, readiness,
    or stage;
  * returns ONE immutable payload for the single primary unresolved issue, or
    None when nothing is actionable (verified-ready: do NOT invent a problem);
  * only reorganizes and explains ALREADY-RECORDED facts (R-4): it fabricates
    no technical requirement, claims no verification, and selects no
    contradiction winner.

This module imports ONLY from engine.idea_state. It does not import or depend on
the web layer, the web responsibility-label display map, persistence, or session
storage; provider grounding is engine-resident (see O-1 below).
"""
import re
from dataclasses import dataclass
from typing import Optional

from engine.idea_state import (
    DISPOSITION_ANSWERED,
    DISPOSITION_PROVISIONAL_ASSUMPTION,
    DISPOSITION_SPECIALIST_REQUESTED,
    DISPOSITION_EVIDENCE_REQUESTED,
    OWNER_STATED,
    VALIDATED_STATUSES,
    OWNER_INPUT,
    SYSTEM_ANALYSIS,
    SPECIALIST_INPUT,
    EMPIRICAL_EVIDENCE,
    UNDETERMINED,
)

# Engine-resident responsibility vocabulary (O-1). No web-layer mapping is used.
_PROVIDER_VOCAB = frozenset({
    OWNER_INPUT, SYSTEM_ANALYSIS, SPECIALIST_INPUT, EMPIRICAL_EVIDENCE, UNDETERMINED,
})

_MATURITY_THRESHOLD = 2          # Stage 2 maturity threshold (level 0|1|2 only)
_REC_ID_RE = re.compile(r"^rec_(\d+)$")


@dataclass(frozen=True)
class NextDevelopmentStep:
    """Immutable payload for the single primary unresolved issue.

    Frozen: equality is by value (identical state yields an equal payload) and
    attribute assignment raises FrozenInstanceError (a subclass of
    AttributeError). Optional fields are truthfully None when absent; no field
    is fabricated and no certainty is invented.
    """
    issue_type: str
    reference_id: str
    title: str
    why_it_matters: str
    next_action: str
    evidence_needed: Optional[str] = None
    suggested_provider: Optional[str] = None
    sufficiency_condition: Optional[str] = None
    unlock_condition: Optional[str] = None
    remaining_uncertainty: Optional[str] = None


# --- Active-set filtering (Increment 2 supersession rule) -------------------------
def _active_records(state):
    """Active = not superseded. Superseded/inactive records are excluded BEFORE any
    priority selection, tie-breaking, provider grounding, or payload construction."""
    return [r for r in getattr(state, "assertions", [])
            if getattr(r, "superseded_by", None) is None]


# --- R-6 deterministic within-level tie-break -------------------------------------
def _record_sort_key(indexed):
    """Key for one (original_index, record). Staged exactly per R-6:
      1. lowest numeric record_id for valid rec_N identifiers;
      2. otherwise earliest iteration;
      3. otherwise stable first-encountered source order.
    rec_N candidates always precede non-rec_N candidates (tuple lead 0 < 1 < 2);
    `index` is the stable original order and breaks any remaining ties. No extra
    tie-break axis is introduced."""
    index, r = indexed
    m = _REC_ID_RE.match(r.record_id or "")
    if m:
        return (0, int(m.group(1)), index)          # numeric rec_N (rec_2 < rec_10)
    iteration = getattr(r, "iteration", None)
    if iteration is not None:
        return (1, iteration, index)                # earliest iteration
    return (2, 0, index)                            # stable first-encountered


def _select_record(records):
    """Choose exactly one record from same-level active candidates via R-6."""
    return min(enumerate(records), key=_record_sort_key)[1]


def _gap_sort_key(indexed):
    """R-6-aligned tie-break for open gaps (no rec_N id): earliest opened_at, then
    stable first-encountered order."""
    index, g = indexed
    opened = getattr(g, "opened_at", None)
    if opened is not None:
        return (0, opened, index)
    return (1, 0, index)


def _select_gap(gaps):
    return min(enumerate(gaps), key=_gap_sort_key)[1]


# --- O-1 provider grounding (engine-resident only; no invention) ------------------
def _record_provider(r):
    """Truthful provider grounded ONLY in engine-resident state. Request records
    ground to the request's nature; owner-stated records ground to the recorded
    responsibility (OWNER_INPUT). Never invents a provider or certainty."""
    if r.disposition == DISPOSITION_EVIDENCE_REQUESTED:
        return EMPIRICAL_EVIDENCE
    if r.disposition == DISPOSITION_SPECIALIST_REQUESTED:
        return SPECIALIST_INPUT
    responsibility = getattr(r, "responsibility", None)
    if responsibility in _PROVIDER_VOCAB:
        return responsibility
    if getattr(r, "provenance", None) == OWNER_STATED:
        return OWNER_INPUT
    return UNDETERMINED


# --- Level predicates over the active set -----------------------------------------
def _active_contradiction_candidates(active):
    """Active records that contradict at least one OTHER active record. A
    contradiction whose only partner has been superseded is no longer active."""
    active_ids = {r.record_id for r in active}
    return [r for r in active
            if any(pid in active_ids for pid in getattr(r, "contradicts", []))]


def _records_with_disposition(active, disposition):
    return [r for r in active if r.disposition == disposition]


def _owner_unvalidated_records(active):
    return [r for r in active
            if r.disposition == DISPOSITION_ANSWERED
            and getattr(r, "provenance", None) == OWNER_STATED
            and getattr(r, "validation_status", None) not in VALIDATED_STATUSES]


def _open_gaps(state):
    getter = getattr(state, "get_open_gaps", None)
    if callable(getter):
        return list(getter())
    return [g for g in getattr(state, "gaps", []) if getattr(g, "status", None) == "OPEN"]


# --- Payload builders (truthful restatement only; R-4) ----------------------------
def _from_record(issue_type, r, *, title, why, action, evidence=None,
                 sufficiency=None, unlock=None, uncertainty=None, provider=None):
    return NextDevelopmentStep(
        issue_type=issue_type,
        reference_id=r.record_id,
        title=title,
        why_it_matters=why,
        next_action=action,
        evidence_needed=evidence,
        suggested_provider=provider if provider is not None else _record_provider(r),
        sufficiency_condition=sufficiency,
        unlock_condition=unlock,
        remaining_uncertainty=uncertainty,
    )


def derive_next_development_step(state):
    """Return the single primary NextDevelopmentStep for `state`, or None when
    nothing is actionable (verified-ready). Pure / read-only / deterministic."""
    active = _active_records(state)

    # 1. active unresolved contradiction
    contradictions = _active_contradiction_candidates(active)
    if contradictions:
        r = _select_record(contradictions)
        return _from_record(
            "active_contradiction", r,
            title="Unresolved contradiction between recorded answers",
            why="Two recorded answers conflict; the conflict must be reconciled "
                "before the idea can advance.",
            action="Reconcile the conflicting recorded answers "
                   "(the system does not choose a winner).",
            sufficiency="The conflicting answers are reconciled into one "
                        "consistent recorded answer.",
            unlock="The contradiction is resolved.",
            uncertainty="Which recorded answer is correct is undetermined until "
                        "reconciled.",
            provider=UNDETERMINED,
        )

    # 2. pending empirical evidence
    evidence = _records_with_disposition(active, DISPOSITION_EVIDENCE_REQUESTED)
    if evidence:
        r = _select_record(evidence)
        return _from_record(
            "pending_evidence", r,
            title="Pending empirical evidence request",
            why="A recorded evidence request is still unresolved; the claim is "
                "not technically verified.",
            action="Provide the requested empirical evidence.",
            evidence=(r.content or "Empirical evidence for the recorded request."),
            sufficiency="Independently demonstrated empirical evidence is recorded.",
            unlock="The requested evidence is supplied and validated.",
            uncertainty="The recorded evidence is not technically verified.",
        )

    # 3. pending specialist input
    specialist = _records_with_disposition(active, DISPOSITION_SPECIALIST_REQUESTED)
    if specialist:
        r = _select_record(specialist)
        return _from_record(
            "pending_specialist", r,
            title="Pending specialist input request",
            why="A recorded specialist request is still unresolved.",
            action="Obtain the requested specialist input.",
            sufficiency="Specialist input is recorded and validated.",
            unlock="The requested specialist input is supplied.",
            uncertainty="Awaiting specialist review.",
        )

    # 4. provisional assumption
    provisional = _records_with_disposition(active, DISPOSITION_PROVISIONAL_ASSUMPTION)
    if provisional:
        r = _select_record(provisional)
        return _from_record(
            "provisional_assumption", r,
            title="Provisional assumption awaiting validation",
            why="A provisional assumption is recorded but not validated.",
            action="Validate or replace the provisional assumption.",
            sufficiency="The assumption is validated or replaced with a recorded "
                        "answer.",
            unlock="The assumption is validated.",
            uncertainty="Currently assumed, not validated.",
        )

    # 5. owner-stated but unvalidated assertion
    owner_unvalidated = _owner_unvalidated_records(active)
    if owner_unvalidated:
        r = _select_record(owner_unvalidated)
        return _from_record(
            "owner_unvalidated", r,
            title="Owner-stated answer awaiting validation",
            why="An owner-provided answer is recorded but not independently "
                "validated.",
            action="Validate the owner-stated answer.",
            sufficiency="The owner-stated answer is independently validated.",
            unlock="Independent validation is recorded.",
            uncertainty="Owner-stated, not validated.",
            provider=OWNER_INPUT,
        )

    # 6. open gap
    open_gaps = _open_gaps(state)
    if open_gaps:
        g = _select_gap(open_gaps)
        return NextDevelopmentStep(
            issue_type="open_gap",
            reference_id=g.gap_type,
            title="An open gap remains to be addressed",
            why_it_matters="A recorded gap remains open.",
            next_action="Address the open gap.",
            evidence_needed=None,
            suggested_provider=UNDETERMINED,
            sufficiency_condition="The gap is resolved or explicitly accepted.",
            unlock_condition="The gap is closed.",
            remaining_uncertainty="The gap is not yet resolved.",
        )

    # 7. maturity below level 2 (final fallback)
    if getattr(state, "maturity_level", 0) < _MATURITY_THRESHOLD:
        return NextDevelopmentStep(
            issue_type="maturity",
            reference_id=f"maturity_level_{getattr(state, 'maturity_level', 0)}",
            title="Maturity below the Stage 2 assessment threshold",
            why_it_matters="The idea has not yet reached the Stage 2 maturity "
                           "threshold.",
            next_action="Continue developing the idea to raise its maturity.",
            evidence_needed=None,
            suggested_provider=None,
            sufficiency_condition="Maturity reaches level 2.",
            unlock_condition="Maturity level 2 is reached.",
            remaining_uncertainty="Idea maturity is still developing.",
        )

    # Verified-ready / nothing actionable: do NOT invent a problem.
    return None
