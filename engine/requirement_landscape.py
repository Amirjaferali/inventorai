"""Increment 4 — Atomic Requirements & Criticality-Aware Risk Register.

Single source of truth for the pure, deterministic, read-only derivation of the
Requirement Landscape from an already-recorded ``IdeaState``. This is an
ADDITIONAL, INDEPENDENT selector over the same state; it is NOT the Increment 3
next-development-step selector, does not call it, and changes nothing about it.

Governance (merged, binding): docs/governance/INCREMENT_4_AUTHORITY_RULINGS.md
(C4-R1..C4-R13), docs/governance/INCREMENT_4_DESIGN.md (D-1..D-7), and
docs/governance/INCREMENT_4_IMPLEMENTATION_CONTRACT.md.

Contract of ``derive_requirement_landscape(state)``:
  * pure, deterministic, read-only; NEVER mutates the input;
  * imports ONLY from ``engine.idea_state`` among project modules;
  * one coarse atomic requirement per active primary anchor (no fragment splitting);
  * deterministic, order-independent identifiers and ordering;
  * every MVP-1 criticality is ``UNDETERMINED`` with ``system-derived`` authority;
  * ZERO grounded risks in MVP-1; the empty landscape appears only when no valid
    active anchor remains.
"""
import re
from dataclasses import dataclass, field, replace
from typing import Optional, Tuple

from engine.idea_state import (
    OPEN,
    DISPOSITION_EVIDENCE_REQUESTED,
    DISPOSITION_SPECIALIST_REQUESTED,
    CRITICALITY_ACTION_CONFIRMED,
)

# --- Frozen category / status vocabularies (contract §4.2, §9.7) ------------------
UNDETERMINED = "UNDETERMINED"                 # the never-interacted criticality category
AUTHORITY_SYSTEM_DERIVED = "system-derived"   # the never-interacted criticality authority
# Workstream 4 (STRUCTURED_CRITICALITY_CAPTURE_INCREMENT_CONTRACT.md §4/§16.1):
# the two additional authorities of the narrow three-state model. Never-
# interacted requirements keep UNDETERMINED / system-derived byte-identically;
# an explicit deferral derives UNDETERMINED / undetermined; an explicit
# confirmation derives the selected category / owner-confirmed. Criticality is
# NEVER inferred from free text — only the recorded explicit inventor actions
# in IdeaState.criticality_confirmations (current lookup, latest governs) are
# applied here. A stale confirmation (its requirement_id is no longer
# generated) simply does not apply and is never reattached.
AUTHORITY_OWNER_CONFIRMED = "owner-confirmed"
AUTHORITY_UNDETERMINED = "undetermined"

_SOURCE_STATUS = {
    "assertion": "recorded",
    "active_contradiction": "active contradiction",
    "pending_evidence": "evidence pending",
    "pending_specialist": "specialist input pending",
    "gap_open": "open",
    "gap_partial": "partially addressed",
}

# Fixed anchor-kind display labels (contract §9.10.5). No raw enum is ever shown.
_ANCHOR_LABELS = {
    "assertion": "Recorded answer",
    "active_contradiction": "Recorded contradiction",
    "pending_evidence": "Pending evidence request",
    "pending_specialist": "Pending specialist request",
}

# Canonical human-readable gap labels, resident here to honor the import boundary
# (a "_GAP_LABELS-style map", contract §9.10.5); mirrors the deliverable's map.
_GAP_LABELS = {
    "PHYSICAL_FEASIBILITY":    "Physical Feasibility",
    "BOUNDARY_AMBIGUITY":      "Boundary and Scope",
    "MECHANISM_COMPLETENESS":  "Mechanism Completeness",
    "PROBLEM_MECHANISM_FIT":   "Problem–Mechanism Fit",
    "ASSUMPTION_INVENTORY":    "Assumption Inventory",
    "EXPERTISE_GAP_AWARENESS": "Expertise-Gap Awareness",
}

# Fixed resolving-action vocabulary, exactly one per anchor kind (contract §9.9.2).
_ACTION = {
    "assertion": ("validate_recorded_answer",
                  "Validate the recorded answer against the available evidence."),
    "active_contradiction": ("reconcile_recorded_contradiction",
                             "Reconcile the conflicting recorded answers "
                             "without assuming either is correct."),
    "pending_evidence": ("provide_requested_evidence",
                         "Provide the requested empirical evidence."),
    "pending_specialist": ("obtain_requested_specialist_input",
                           "Obtain the requested specialist input."),
}
_CONTRADICTION_STATEMENT = (
    "Resolve the active contradiction between the two recorded answers."
)

# Display precedence — a stable, readable order that carries NO severity meaning.
_PRECEDENCE = {
    "active_contradiction": 0,
    "pending_evidence": 1,
    "pending_specialist": 2,
    "assertion": 3,
    "gap": 4,
}

_REC_ID_RE = re.compile(r"^rec_(\d+)$")


# --- Frozen, immutable payloads (contract §4.1) -----------------------------------
@dataclass(frozen=True)
class ProvenanceAnchor:
    anchor_kind: str
    anchor_reference: str
    display_label: str


@dataclass(frozen=True)
class SupportingReference:
    reference_kind: str
    reference: str
    display_label: str


@dataclass(frozen=True)
class ResolvingAction:
    action_kind: str
    statement: str
    source_reference: str


@dataclass(frozen=True)
class GroundedRisk:
    risk_id: str
    linked_requirement_ids: Tuple[str, ...]
    consequence: str
    grounding_references: Tuple[SupportingReference, ...]
    authority: str
    status: str
    rationale: str


@dataclass(frozen=True)
class DerivedRequirement:
    requirement_id: str
    statement: str
    primary_anchor: ProvenanceAnchor
    supporting_references: Tuple[SupportingReference, ...]
    source_status: str
    criticality: str
    criticality_authority: str
    criticality_rationale: Optional[str]
    resolving_action: Optional[ResolvingAction]
    linked_risk_ids: Tuple[str, ...]


@dataclass(frozen=True)
class RequirementLandscape:
    requirements: Tuple[DerivedRequirement, ...]
    risks: Tuple[GroundedRisk, ...]


# --- Helpers ----------------------------------------------------------------------
def _rec_sort_key(record_id):
    """Stable numeric rec_N key; valid rec_N precede non-rec_N (contract §8.3)."""
    m = _REC_ID_RE.match(record_id or "")
    if m:
        return (0, int(m.group(1)), "")
    return (1, 0, record_id or "")


def _order_pair(a, b):
    """Order-normalized (lo, hi) record-id pair by the rec_N key (contract §6.7)."""
    return (a, b) if _rec_sort_key(a) <= _rec_sort_key(b) else (b, a)


def _gap_label(gap_type):
    """Canonical human-readable label; never leaks the raw enum token (§7.3)."""
    label = _GAP_LABELS.get(gap_type)
    if label is not None:
        return label
    return " ".join(w.capitalize() for w in str(gap_type).split("_"))


def _record_kind(record):
    disposition = getattr(record, "disposition", None)
    if disposition == DISPOSITION_EVIDENCE_REQUESTED:
        return "pending_evidence"
    if disposition == DISPOSITION_SPECIALIST_REQUESTED:
        return "pending_specialist"
    return "assertion"


def _record_id_prefix(kind):
    return {"assertion": "req:assertion:",
            "pending_evidence": "req:evidence:",
            "pending_specialist": "req:specialist:"}[kind]


def _restate(content, kind):
    text = (content or "").strip()
    if text:
        return text
    return {"assertion": "Recorded answer awaiting restatement.",
            "pending_evidence": "Empirical evidence requested for the recorded item.",
            "pending_specialist": "Specialist input requested for the recorded item."}[kind]


def _requirement_from_record(record, kind):
    anchor = ProvenanceAnchor(anchor_kind=kind, anchor_reference=record.record_id,
                              display_label=_ANCHOR_LABELS[kind])
    action_kind, statement = _ACTION[kind]
    return DerivedRequirement(
        requirement_id=_record_id_prefix(kind) + record.record_id,
        statement=_restate(getattr(record, "content", ""), kind),
        primary_anchor=anchor,
        supporting_references=(),
        source_status=_SOURCE_STATUS[kind],
        criticality=UNDETERMINED,
        criticality_authority=AUTHORITY_SYSTEM_DERIVED,
        criticality_rationale=None,
        resolving_action=ResolvingAction(action_kind, statement, record.record_id),
        linked_risk_ids=(),
    )


def _requirement_from_pair(lo, hi):
    ref = lo + "|" + hi
    anchor = ProvenanceAnchor(anchor_kind="active_contradiction", anchor_reference=ref,
                              display_label=_ANCHOR_LABELS["active_contradiction"])
    action_kind, statement = _ACTION["active_contradiction"]
    return DerivedRequirement(
        requirement_id="req:contradiction:" + ref,
        statement=_CONTRADICTION_STATEMENT,
        primary_anchor=anchor,
        supporting_references=(),
        source_status=_SOURCE_STATUS["active_contradiction"],
        criticality=UNDETERMINED,
        criticality_authority=AUTHORITY_SYSTEM_DERIVED,
        criticality_rationale=None,
        resolving_action=ResolvingAction(action_kind, statement, ref),
        linked_risk_ids=(),
    )


def _requirement_from_gap(gap_type, group):
    label = _gap_label(gap_type)
    any_open = any(getattr(g, "status", None) == OPEN for g in group)
    source_status = _SOURCE_STATUS["gap_open"] if any_open else _SOURCE_STATUS["gap_partial"]
    anchor = ProvenanceAnchor(anchor_kind="gap", anchor_reference=gap_type,
                              display_label=label)
    return DerivedRequirement(
        requirement_id="req:gap:" + gap_type,
        statement=label,
        primary_anchor=anchor,
        supporting_references=(),
        source_status=source_status,
        criticality=UNDETERMINED,
        criticality_authority=AUTHORITY_SYSTEM_DERIVED,
        criticality_rationale=None,
        resolving_action=ResolvingAction(
            "address_open_gap", "Address the open gap: " + label + ".", gap_type),
        linked_risk_ids=(),
    )


def _order_key(requirement):
    kind = requirement.primary_anchor.anchor_kind
    precedence = _PRECEDENCE[kind]
    if kind == "active_contradiction":
        lo, hi = requirement.primary_anchor.anchor_reference.split("|", 1)
        within = (_rec_sort_key(lo), _rec_sort_key(hi))
    elif kind == "gap":
        within = (requirement.primary_anchor.anchor_reference,)
    else:
        within = (_rec_sort_key(requirement.primary_anchor.anchor_reference),)
    return (precedence, within)


def derive_requirement_landscape(state):
    """Return the immutable RequirementLandscape for ``state``. Pure / read-only /
    deterministic (contract §6.1). Empty ONLY when no valid active anchor remains."""
    active = [r for r in getattr(state, "assertions", [])
              if getattr(r, "superseded_by", None) is None]
    active_ids = {r.record_id for r in active}

    # 1. Active contradiction pairs (order-normalized; F-2 / §6.5). A malformed edge
    #    whose partner is missing or inactive yields no pair.
    pairs = set()
    for r in active:
        for pid in (getattr(r, "contradicts", None) or []):
            if pid in active_ids and pid != r.record_id:
                pairs.add(_order_pair(r.record_id, pid))
    paired = {rid for pair in pairs for rid in pair}

    requirements = [_requirement_from_pair(lo, hi) for (lo, hi) in pairs]

    # 2. Non-contradiction active records -> exactly one requirement each (§6.5).
    for r in active:
        if r.record_id in paired:
            continue
        requirements.append(_requirement_from_record(r, _record_kind(r)))

    # 3. Open/partial gaps, collapsed to one anchor per gap_type (F-1 / §6.7).
    getter = getattr(state, "get_open_gaps", None)
    open_gaps = list(getter()) if callable(getter) else [
        g for g in getattr(state, "gaps", []) if getattr(g, "status", None) == OPEN]
    by_type = {}
    for g in open_gaps:
        by_type.setdefault(g.gap_type, []).append(g)
    for gap_type in by_type:
        requirements.append(_requirement_from_gap(gap_type, by_type[gap_type]))

    ordered = tuple(sorted(requirements, key=_order_key))

    # 4. Workstream 4 (§16.1 three-state authority model): apply the latest
    #    explicit inventor action per requirement_id from the session-bounded
    #    confirmation history. Read-only over the input; requirements without
    #    a recorded action stay byte-identical (UNDETERMINED/system-derived).
    confirmations = getattr(state, "criticality_confirmations", None) or []
    if confirmations:
        latest = {}
        for record in confirmations:          # append order == action order
            latest[record.requirement_id] = record
        applied = []
        for r in ordered:
            record = latest.get(r.requirement_id)
            if record is None:
                applied.append(r)
            elif record.action == CRITICALITY_ACTION_CONFIRMED:
                applied.append(replace(
                    r, criticality=record.category,
                    criticality_authority=AUTHORITY_OWNER_CONFIRMED,
                    criticality_rationale=record.rationale_verbatim))
            else:                              # explicit deferral
                applied.append(replace(
                    r, criticality=UNDETERMINED,
                    criticality_authority=AUTHORITY_UNDETERMINED,
                    criticality_rationale=None))
        ordered = tuple(applied)

    return RequirementLandscape(requirements=ordered, risks=())
