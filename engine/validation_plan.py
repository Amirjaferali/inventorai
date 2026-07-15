"""Increment 5 — Concrete Validation-Plan Generation.

Single source of truth for the pure, deterministic, read-only derivation of a
Validation Plan from an already-recorded ``IdeaState``. This is an ADDITIONAL,
INDEPENDENT selector over the same state: it consumes the Increment 4 Requirement
Landscape and proposes, per requirement, ONE concrete validation step (level 1
proposed action + level 2 required evidence category) or ONE blocked item. It
generates NO level-3 (supplied) or level-4 (verified) claim.

Governance (merged, binding): docs/governance/INCREMENT_5_DESIGN.md and
docs/governance/INCREMENT_5_IMPLEMENTATION_CONTRACT.md.

Contract of ``derive_validation_plan(state)`` (§4–§14):
  * pure, deterministic, read-only; NEVER mutates the input;
  * imports ONLY ``engine.idea_state`` and ``engine.requirement_landscape`` among
    project modules; no Increment 3, scoring, persistence, web, or domain deps;
  * one-to-one: one requirement -> at most one step OR one blocked item;
  * stable, non-positional identity reusing Increment 4 requirement keys
    (``vstep:`` / ``vblock:`` prefixes);
  * ordering inherited from the Increment 4 landscape order (organizational only);
  * every MVP-1 ``confidence`` is ``UNDETERMINED``; outcome ∈ {PLAN, EMPTY, BLOCKED}.

The module-level name ``derive_requirement_landscape`` is the authorized §19 test
seam: tests may monkeypatch it at this import site to construct BLOCKED / mixed /
malformed cases. Production behavior is driven by the real Increment 4 derivation.
"""
from dataclasses import dataclass
from typing import Optional, Tuple

from engine.idea_state import (
    OWNER_STATED,
    OWNER_INPUT, SYSTEM_ANALYSIS, SPECIALIST_INPUT, EMPIRICAL_EVIDENCE, UNDETERMINED,
    DISPOSITION_ANSWERED, DISPOSITION_PROVISIONAL_ASSUMPTION,
)
from engine.requirement_landscape import derive_requirement_landscape

# --- Frozen ValidationStep responsibility vocabulary (contract §7; exactly five) --
OWNER_EXECUTABLE            = "OWNER_EXECUTABLE"
SYSTEM_DERIVABLE           = "SYSTEM_DERIVABLE"
SPECIALIST_REQUIRED        = "SPECIALIST_REQUIRED"
EMPIRICAL_EVIDENCE_REQUIRED = "EMPIRICAL_EVIDENCE_REQUIRED"
# (UNDETERMINED is shared with the ledger vocabulary and is valid in both.)

# Frozen outcome tokens (contract §6).
OUTCOME_PLAN    = "PLAN"
OUTCOME_EMPTY   = "EMPTY"
OUTCOME_BLOCKED = "BLOCKED"

# The bounded MVP-1 confidence value (contract §14).
CONFIDENCE_UNDETERMINED = "UNDETERMINED"

# Workstream 7 (ACTIONABLE_VALIDATION_PLAN_INCREMENT_CONTRACT.md §3.1/§5.1;
# owner decisions D3/C1): eligible answered-record steps carry the owner-approved
# requirement-linked action embedding the requirement's already-derived statement
# BYTE-VERBATIM. Selected SOLELY by the underlying active record's exact
# disposition value "answered" — never inferred from content, vocabulary, answer
# quality, domain, or technical complexity. Contradiction, gap, pending, unknown,
# deferred, and provisional actions are unchanged; the Section 13 landscape
# statement and resolving action are not modified.
_ANSWERED_STEP_STATEMENT_PREFIX = (
    "Validate this recorded answer against the available evidence: ")

# §7-T ledger -> ValidationStep responsibility translation (recognized tokens only).
_LEDGER_TRANSLATION = {
    OWNER_INPUT:        OWNER_EXECUTABLE,
    SYSTEM_ANALYSIS:    SYSTEM_DERIVABLE,
    SPECIALIST_INPUT:   SPECIALIST_REQUIRED,
    EMPIRICAL_EVIDENCE: EMPIRICAL_EVIDENCE_REQUIRED,
    UNDETERMINED:       UNDETERMINED,
}

# Anchor kinds that can support an eligible step (contract §7 / §8).
_STEP_ANCHOR_KINDS = frozenset({
    "active_contradiction", "pending_evidence", "pending_specialist",
    "assertion", "gap",
})

# Fixed, generic wording for a blocked item (contract §8 / §12; no fabrication).
_BLOCKED_REASON = (
    "This recorded signal cannot yet support a concrete validation step."
)


# --- Frozen, immutable payloads (contract §5) -------------------------------------
@dataclass(frozen=True)
class ProvenanceRef:
    anchor_kind: str
    reference: str
    display_label: str


@dataclass(frozen=True)
class ValidationStep:
    step_id: str
    statement: str
    responsibility: str
    evidence_category: str
    closure_condition: str
    provenance: ProvenanceRef
    confidence: str


@dataclass(frozen=True)
class BlockedValidationItem:
    item_id: str
    reason: str
    missing: str
    responsibility: str
    provenance: ProvenanceRef


@dataclass(frozen=True)
class ValidationPlan:
    outcome: str
    steps: Tuple[ValidationStep, ...]
    blocked_items: Tuple[BlockedValidationItem, ...]


# --- Classification helpers (pure) ------------------------------------------------
def _active_record(state, record_id):
    """Return the active ledger record with ``record_id`` (or None). Only records
    with ``superseded_by is None`` participate (inherited active-set discipline)."""
    for r in getattr(state, "assertions", []) or []:
        if getattr(r, "record_id", None) == record_id and getattr(r, "superseded_by", None) is None:
            return r
    return None


def _assertion_responsibility(record):
    """Resolve the ValidationStep responsibility for an ``assertion`` anchor from
    the underlying record (contract §7 precedence, §7-T translation, §7-P).

    Precedence 1 (explicit recognized ledger token, translated) applies ONLY when
    the token is structurally distinguishable: for a ``provisional_assumption``
    record an ``OWNER_INPUT`` token is indistinguishable as to origin (explicit vs
    auto-populated) and MUST NOT resolve to OWNER_EXECUTABLE — it falls through.
    Precedence 2 uses disposition/provenance; otherwise UNDETERMINED.
    """
    if record is None:
        return UNDETERMINED
    resp = getattr(record, "responsibility", None)
    disp = getattr(record, "disposition", None)
    prov = getattr(record, "provenance", None)
    # precedence 1 — explicit, recognized, structurally sufficient responsibility.
    if resp in _LEDGER_TRANSLATION:
        provisional_owner_collision = (
            disp == DISPOSITION_PROVISIONAL_ASSUMPTION and resp == OWNER_INPUT
        )
        if not provisional_owner_collision:
            return _LEDGER_TRANSLATION[resp]
    # precedence 2 — disposition/provenance mapping.
    if disp == DISPOSITION_ANSWERED and prov == OWNER_STATED:
        return OWNER_EXECUTABLE
    # unknown / deferred / provisional-without-support / LEGACY_UNSPECIFIED, and any
    # unrecognized token that fell through, resolve to UNDETERMINED.
    return UNDETERMINED


def _classify(requirement, state):
    """Return (responsibility, evidence_category) for an eligible requirement."""
    kind = requirement.primary_anchor.anchor_kind
    if kind == "active_contradiction":
        return OWNER_EXECUTABLE, "reconciliation of conflicting records"
    if kind == "pending_evidence":
        return EMPIRICAL_EVIDENCE_REQUIRED, "empirical evidence"
    if kind == "pending_specialist":
        return SPECIALIST_REQUIRED, "specialist input"
    if kind == "gap":
        return UNDETERMINED, "clarifying information"
    # assertion anchor: consult the underlying record's disposition/provenance/resp.
    responsibility = _assertion_responsibility(
        _active_record(state, requirement.primary_anchor.anchor_reference))
    return responsibility, _evidence_category(responsibility)


def _evidence_category(responsibility):
    """Bounded, generic evidence category for a non-contradiction responsibility."""
    if responsibility == OWNER_EXECUTABLE:
        return "owner confirmation"
    if responsibility == EMPIRICAL_EVIDENCE_REQUIRED:
        return "empirical evidence"
    if responsibility == SPECIALIST_REQUIRED:
        return "specialist input"
    if responsibility == SYSTEM_DERIVABLE:
        return "system analysis"
    return "clarifying information"


def _closure_condition(evidence_category):
    return (f"Closed when {evidence_category} is provided and recorded; "
            "no such evidence is recorded yet.")


def _provenance(requirement):
    a = requirement.primary_anchor
    return ProvenanceRef(anchor_kind=a.anchor_kind, reference=a.anchor_reference,
                         display_label=a.display_label)


def _is_wellformed(requirement):
    """A requirement is structurally addressable when it carries a requirement_id
    and a well-formed primary_anchor (contract §8; malformed-beyond-addressability
    is skipped per-record, never raised)."""
    rid = getattr(requirement, "requirement_id", None)
    anchor = getattr(requirement, "primary_anchor", None)
    if not rid or anchor is None:
        return False
    return bool(getattr(anchor, "anchor_kind", None)
                and getattr(anchor, "anchor_reference", None) is not None
                and getattr(anchor, "display_label", None) is not None)


# --- Entry point ------------------------------------------------------------------
def derive_validation_plan(state):
    """Return the immutable ``ValidationPlan`` for ``state``. Pure / read-only /
    deterministic (contract §4–§14). One step or one blocked item per eligible
    requirement, in the Increment 4 landscape order; never raises on malformed
    input (degrades per-record)."""
    landscape = derive_requirement_landscape(state)
    requirements = tuple(landscape.requirements)

    steps = []
    blocked = []
    seen_steps = set()
    seen_blocked = set()
    for req in requirements:
        if not _is_wellformed(req):
            # malformed beyond structural addressability -> skip (never raise, §8).
            continue
        kind = req.primary_anchor.anchor_kind
        eligible = (req.resolving_action is not None) and (kind in _STEP_ANCHOR_KINDS)
        if eligible:
            step_id = "vstep:" + req.requirement_id
            if step_id in seen_steps:        # defensive dedup (§10); keys are unique
                continue
            seen_steps.add(step_id)
            responsibility, evidence_category = _classify(req, state)
            statement = req.resolving_action.statement
            if kind == "assertion":
                record = _active_record(state, req.primary_anchor.anchor_reference)
                if record is not None and \
                        getattr(record, "disposition", None) == DISPOSITION_ANSWERED:
                    statement = (_ANSWERED_STEP_STATEMENT_PREFIX
                                 + "“" + req.statement + "”")
            steps.append(ValidationStep(
                step_id=step_id,
                statement=statement,
                responsibility=responsibility,
                evidence_category=evidence_category,
                closure_condition=_closure_condition(evidence_category),
                provenance=_provenance(req),
                confidence=CONFIDENCE_UNDETERMINED,
            ))
        else:
            item_id = "vblock:" + req.requirement_id
            if item_id in seen_blocked:
                continue
            seen_blocked.add(item_id)
            if kind in _STEP_ANCHOR_KINDS and kind != "assertion":
                responsibility, missing = _classify_blocked(req, state)
            else:
                responsibility = _assertion_responsibility(
                    _active_record(state, req.primary_anchor.anchor_reference)) \
                    if kind == "assertion" else UNDETERMINED
                missing = _evidence_category(responsibility)
            blocked.append(BlockedValidationItem(
                item_id=item_id,
                reason=_BLOCKED_REASON,
                missing=missing,
                responsibility=responsibility,
                provenance=_provenance(req),
            ))

    if steps:
        outcome = OUTCOME_PLAN
    elif blocked:
        outcome = OUTCOME_BLOCKED
    elif not requirements:
        outcome = OUTCOME_EMPTY
    else:
        # Non-empty landscape whose every requirement was malformed-skipped is
        # unreachable through the real feed (§12-C); degrade truthfully to EMPTY
        # rather than invent a fourth outcome.
        outcome = OUTCOME_EMPTY

    return ValidationPlan(outcome=outcome, steps=tuple(steps),
                          blocked_items=tuple(blocked))


def _classify_blocked(requirement, state):
    """(responsibility, missing) for a non-assertion blocked requirement."""
    responsibility, evidence_category = _classify(requirement, state)
    return responsibility, evidence_category
