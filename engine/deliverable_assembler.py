"""
engine/deliverable_assembler.py
FDC-001 MVP Package Assembler — Phase 5 Step 1
Pure transformation: IdeaState -> FDC-001 package dict.
No LLM calls. No registry dependency. No IdeaState mutation.
"""
from __future__ import annotations
import uuid
import hashlib
from datetime import datetime, timezone
from typing import Any
from engine.idea_state import (
    IdeaState, Evidence, ASSERTED, REASONED, DEMONSTRATED, OPEN, PARTIAL, CLOSED,
    STAGE_3_GAP_TYPES, PROBLEM_MECHANISM_FIT,
    ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS,
    LEGACY_UNSPECIFIED, UNVALIDATED,
)
from engine.derived_readiness import derive_readiness
# Increment 3: the SAME shared public derivation that feeds the session callout.
# Imported as a module-level name so a single selection feeds both surfaces (O-2).
from engine.idea_development_outputs import derive_next_development_step
# Increment 4 (additive): the pure Requirement Landscape derivation. Consumed by
# the single additive section _s13; adds no new truth and changes no prior section.
from engine.requirement_landscape import derive_requirement_landscape
# Increment 5 (additive): the pure Validation Plan derivation. Consumed by the
# single additive section _s14; adds no new truth and changes no prior section.
from engine.validation_plan import derive_validation_plan

PACKAGE_VERSION = "1.0.0"
SCHEMA_ID       = "fdc-001-mvp-v1"

_DISCLAIMER_STANDARD = (
    "This assessment package is produced by an automated invention analysis "
    "system. It is advisory only. No claim made in this package constitutes "
    "engineering certification, regulatory approval, or legal advice. The "
    "inventor is responsible for independent verification of all technical "
    "claims, feasibility conclusions, and recommendations before acting on "
    "this assessment."
)
# Increment 2: evidence QUALITY (a reasoning-structure axis, ADR-003) is not
# validation. The REASONED label no longer implies technical confirmation
# "beyond stored evidence" — validation is surfaced separately on each evidence
# view via `validation_status`.
_QUALITY_LABELS = {
    ASSERTED:     "Asserted (inventor-stated, unvalidated)",
    REASONED:     "Reasoned (inventor's structured rationale; not validated)",
    DEMONSTRATED: "Demonstrated (externally evidenced)",
    None:         "No evidence recorded",
}
# Honest, human-readable labels for the Increment 2 validation axis.
_VALIDATION_LABELS = {
    "UNVALIDATED":              "Not validated",
    "SPECIALIST_REVIEWED":      "Specialist-reviewed",
    "EMPIRICALLY_DEMONSTRATED": "Empirically demonstrated",
    "INDEPENDENTLY_VERIFIED":   "Independently verified",
}
_MATURITY_LABELS = {
    0: "Level 0 — Problem signal not yet established",
    1: "Level 1 — Exploratory / Incomplete: problem signal received at minimum "
       "evidence threshold. No engineering claim validated. Not a deliverable gate.",
    2: "Level 2 — Mechanism established: operating principle substantiated.",
    3: "Level 3 — Boundary defined: scope and constraints documented.",
}
_GAP_LABELS = {
    "PHYSICAL_FEASIBILITY":   "Physical Feasibility",
    "BOUNDARY_AMBIGUITY":     "Boundary and Scope",
    "MECHANISM_COMPLETENESS": "Mechanism Completeness",
    # Stage 3 reasoning areas (human-readable; never expose raw enum names)
    "PROBLEM_MECHANISM_FIT":   "Problem–Mechanism Fit",
    "ASSUMPTION_INVENTORY":    "Assumption Inventory",
    "EXPERTISE_GAP_AWARENESS": "Expertise-Gap Awareness",
}

_STAGE3_MISSING_EVIDENCE = (
    "No substantiated response captured for this area yet. "
    "It remains open for the inventor to address."
)
_STATUS_LABELS = {
    OPEN: "Open", PARTIAL: "Partially addressed",
    CLOSED: "Answered (not yet validated)", "ACCEPTED_RISK": "Accepted risk",
}
_RECOMMENDATION_A = {
    (2, False): ("PROCEED",
        "Mechanism established and all identified gaps resolved."),
    (2, True):  ("PROCEED WITH CAUTION",
        "Mechanism established but open gaps remain. Address before detailed design."),
    (1, False): ("REVISE",
        "Problem established at exploratory level only. Mechanism not yet substantiated."),
    (1, True):  ("REVISE",
        "Problem established at exploratory level with open gaps."),
    (0, False): ("BLOCK",
        "Problem not yet established. Provide a clear problem statement first."),
    (0, True):  ("BLOCK",
        "Problem not yet established and open gaps recorded."),
}

def assemble_deliverable(state: IdeaState) -> dict:
    if not isinstance(state, IdeaState):
        raise TypeError(f"state must be IdeaState, got {type(state).__name__}")
    if not getattr(state, "idea_id", None):
        raise ValueError("state.idea_id must be set before assembling a deliverable")
    open_gaps   = [g for g in state.gaps if g.status == OPEN]
    closed_gaps = [g for g in state.gaps if g.status == CLOSED]
    return {
        "package_version": PACKAGE_VERSION,
        "schema_id":       SCHEMA_ID,
        "session_id":      state.idea_id,
        "generated_at":    _now_iso(),
        "section_1_disclaimer":          _s1(),
        "section_2_invention_summary":   _s2(state),
        "section_3_assessment_overview": _s3(state, open_gaps),
        "section_4_requirements":        _s4(state),
        "section_5_assumptions":         _s5(state),
        "section_6_risks":               _s6(state, open_gaps),
        "section_7_recommendations":     _s7(state, open_gaps),
        "section_8_unresolved_items":    _s8(open_gaps, state),
        "section_9_stage3_reasoning":    _s9(state),
        "section_10_recommended_next_steps": _s10(state, open_gaps),
        "section_11_prototype_test_plan": _s11(state),
        # Increment 3 (additive, R-3): one visible "Next Development Step" section
        # consuming the SAME shared engine derivation as the session callout. It
        # adds no new truth; it reorganizes already-recorded state for display.
        "section_12_next_development_step": _s12(state),
        # Increment 4 (additive): the provenance-anchored Requirement Landscape.
        # Human-readable only; adds no new truth and changes no prior section.
        "section_13_requirement_landscape": _s13(state),
        # Increment 5 (additive): the Validation Plan (proposed validation actions
        # and blocked items). Human-readable only; adds no new truth, proposes
        # nothing verified, and changes no prior section.
        "section_14_validation_plan": _s14(state),
        "_session_meta": {
            "total_iterations":     state.iteration,
            "total_gaps":           len(state.gaps),
            "open_gap_count":       len(open_gaps),
            "closed_gap_count":     len(closed_gaps),
            "maturity_level":       state.maturity_level,
            "maturity_label":       _MATURITY_LABELS.get(state.maturity_level, "Unknown"),
            "direction":            getattr(state, "direction", None),
            "domain_signal":        getattr(state, "domain_signal", None),
            "evidence_quality":     _overall_quality(state),
            "idea_summary":          getattr(state, "idea_summary", None),  # R-007
            "deliverable_eligible": _eligible(state, open_gaps),
            # Increment 2: derived verified readiness, presented SEPARATELY from
            # stored maturity/lifecycle and from legacy `deliverable_eligible`.
            # Purely recomputed; it never overrides or mutates stored state, and
            # stored CLOSED / high maturity does not force it True.
            "derived_verified_ready": _derived_verified_ready(state),
            # Phase 3A (additive, nested under _session_meta so the top-level
            # canonical-section contract is unchanged): minimal problem/mechanism
            # evidence registry. Full text is carried once here; Section 4
            # references it by id. No evidence removed, no claim added.
            "evidence_registry": _evidence_registry(state),
            # Phase 3B-1 (additive, nested, SEPARATE from evidence_registry so
            # EV-001/EV-002 are untouched): acknowledged-unknown registry. Full
            # verbatim is carried once here; Section 8 references it by id while
            # Section 5 shows the full text. No unknown removed, no claim added.
            "unknown_registry": _unknown_registry(state),
        },
    }

_ZERO_RISK_DISCLAIMER = (
    "No structurally grounded risks are recorded for the current requirements. "
    "This is not a statement that the idea is risk-free, safe, or verified; it "
    "means no structural adverse-consequence signal exists in the recorded state."
)
_REQUIREMENT_LANDSCAPE_EMPTY = (
    "No active, provenance-anchored requirements are recorded yet. This is an "
    "idea-development state, not an error: nothing outstanding has been captured "
    "to derive a requirement from."
)


def _s13(state):
    """Increment 4 additive section: render the pure Requirement Landscape
    derivation as a presentation-ready, JSON-safe dict (read-only; mirrors _s12).
    Human-readable labels only — no raw enum or internal identifier is exposed."""
    landscape = derive_requirement_landscape(state)
    requirements = []
    for r in landscape.requirements:
        action = r.resolving_action
        requirements.append({
            "statement":             r.statement,
            "provenance":            r.primary_anchor.display_label,
            "status":                r.source_status,
            "criticality":           r.criticality,
            "criticality_authority": r.criticality_authority,
            "criticality_rationale": r.criticality_rationale,
            "resolving_action":      (action.statement if action is not None else None),
            "supporting_references": [ref.display_label for ref in r.supporting_references],
            "has_linked_risk":       bool(r.linked_risk_ids),
        })
    return {
        "title":           "Requirement Landscape",
        "requirements":    requirements,
        "total":           len(requirements),
        "empty_statement": _REQUIREMENT_LANDSCAPE_EMPTY,
        "risks":           [],
        "has_risks":       bool(landscape.risks),
        "risk_disclaimer": _ZERO_RISK_DISCLAIMER,
    }


# --- Increment 5 additive Validation Plan section (mirrors _s13 discipline) --------
_VALIDATION_PLAN_EMPTY = (
    "No active, provenance-anchored requirements are recorded yet, so no validation "
    "steps can be proposed. This is an idea-development state, not an error."
)
# Fixed human labels for the bounded responsibility/confidence tokens (contract §15).
# Raw tokens are never rendered; the template shows these labels only.
_RESPONSIBILITY_LABELS = {
    "OWNER_EXECUTABLE":            "Owner can perform",
    "SYSTEM_DERIVABLE":            "System can derive",
    "SPECIALIST_REQUIRED":         "Specialist input required",
    "EMPIRICAL_EVIDENCE_REQUIRED": "Empirical evidence required",
    "UNDETERMINED":                "Responsibility undetermined",
}
_CONFIDENCE_LABELS = {
    "UNDETERMINED": "Confidence undetermined",
}


def _s14(state):
    """Increment 5 additive section: render the pure Validation Plan derivation as a
    presentation-ready, JSON-safe dict (read-only; mirrors _s12/_s13). Human-readable
    labels only — no raw enum, token, or internal identifier is exposed. Both `steps`
    and `blocked_items` are always emitted as lists (never null); the bounded status
    tokens (`outcome`, `responsibility`, `confidence`) may appear in the package but
    are rendered only via their fixed human labels (contract §15/§16)."""
    plan = derive_validation_plan(state)
    steps = []
    for st in plan.steps:
        steps.append({
            "statement":            st.statement,
            "responsibility":       st.responsibility,
            "responsibility_label": _RESPONSIBILITY_LABELS.get(st.responsibility, ""),
            "evidence_category":    st.evidence_category,
            "closure_condition":    st.closure_condition,
            "provenance":           st.provenance.display_label,
            "confidence":           st.confidence,
            "confidence_label":     _CONFIDENCE_LABELS.get(st.confidence, ""),
        })
    blocked_items = []
    for b in plan.blocked_items:
        blocked_items.append({
            "reason":               b.reason,
            "missing":              b.missing,
            "responsibility":       b.responsibility,
            "responsibility_label": _RESPONSIBILITY_LABELS.get(b.responsibility, ""),
            "provenance":           b.provenance.display_label,
        })
    return {
        "title":           "Validation Plan",
        "outcome":         plan.outcome,
        "steps":           steps,
        "blocked_items":   blocked_items,
        "empty_statement": _VALIDATION_PLAN_EMPTY,
    }


def _s12(state):
    """Increment 3 additive section: render the shared next-development-step
    derivation as a presentation-ready dict (read-only; no priority logic here).

    When the derivation finds nothing actionable (verified-ready), the section is
    present but non-actionable (`actionable=False`) — no problem is invented."""
    payload = derive_next_development_step(state)
    if payload is None:
        return {
            "actionable":            False,
            "issue_type":            None,
            "reference_id":          None,
            "title":                 None,
            "why_it_matters":        None,
            "next_action":           None,
            "evidence_needed":       None,
            "suggested_provider":    None,
            "sufficiency_condition": None,
            "unlock_condition":      None,
            "remaining_uncertainty": None,
        }
    return {
        "actionable":            True,
        "issue_type":            payload.issue_type,
        "reference_id":          payload.reference_id,
        "title":                 payload.title,
        "why_it_matters":        payload.why_it_matters,
        "next_action":           payload.next_action,
        "evidence_needed":       payload.evidence_needed,
        "suggested_provider":    payload.suggested_provider,
        "sufficiency_condition": payload.sufficiency_condition,
        "unlock_condition":      payload.unlock_condition,
        "remaining_uncertainty": payload.remaining_uncertainty,
    }


def _derived_verified_ready(state):
    """Truthful, recomputed-on-demand verified-readiness flag for the deliverable.
    Reads the append-only ledger via the pure derived-readiness module; defaults
    to False when there is no validated basis (e.g. legacy states with no ledger
    records). Never overstates certainty from stored maturity/lifecycle alone."""
    return derive_readiness(state).overall_verified()

def _s1():
    return {"tier": "standard", "text": _DISCLAIMER_STANDARD, "applies": True}

# Phase 3A Evidence Registry pilot (problem/mechanism only). Stable fixed-slot
# IDs: the problem is always EV-001, the mechanism always EV-002. When one is
# absent no fake entry is created and the other keeps its fixed ID. The registry
# carries the full evidence text once (so it is never deleted), with a
# human-readable label and provenance. It lives under _session_meta so the
# top-level canonical-section contract is unchanged. Presentation/packaging only:
# no new truth, no summarization, no maturity/readiness/progression change.
_EVIDENCE_PROBLEM_ID = "EV-001"
_EVIDENCE_MECHANISM_ID = "EV-002"
_EVIDENCE_PROBLEM_LABEL = "Known Problem"
_EVIDENCE_MECHANISM_LABEL = "Known Mechanism"


def _evidence_registry(state):
    """Minimal problem/mechanism evidence registry (Phase 3A). Full text is
    carried once here so downstream sections can reference it by id instead of
    re-copying it. No evidence is deleted and no claim is added."""
    reg = []
    problem = _resolved_problem(state)
    if problem is not None:
        reg.append({
            "evidence_id": _EVIDENCE_PROBLEM_ID,
            "label": _EVIDENCE_PROBLEM_LABEL,
            "content": _txt(problem),
            "provenance": getattr(problem, "provenance", LEGACY_UNSPECIFIED),
            "quality_label": _QUALITY_LABELS.get(getattr(problem, "quality", None), "Unknown"),
        })
    mech = getattr(state, "known_mechanism", None)
    if mech is not None:
        reg.append({
            "evidence_id": _EVIDENCE_MECHANISM_ID,
            "label": _EVIDENCE_MECHANISM_LABEL,
            "content": _txt(mech),
            "provenance": getattr(mech, "provenance", LEGACY_UNSPECIFIED),
            "quality_label": _QUALITY_LABELS.get(getattr(mech, "quality", None), "Unknown"),
        })
    return reg


# Phase 3B-1 Unknown Registry (acknowledged unknowns only). A SEPARATE namespace
# and a SEPARATE registry from Phase 3A: acknowledged unknowns are gaps, not
# established evidence, so they never enter evidence_registry and EV-001/EV-002
# behavior is untouched. IDs are UNK-001, UNK-002, ... assigned by 1-based order
# in state.acknowledged_unknowns (NOT iteration, which may not be unique). No
# fake entry is created when there is no acknowledged unknown. The registry
# carries the full verbatim once (never deleted); Section 8 references it by id
# while Section 5 remains the primary visible location for the full text. Lives
# under _session_meta so the top-level canonical-section contract is unchanged.
# Presentation/packaging only: no new truth, no summarization, no claim.
_UNKNOWN_ID_PREFIX = "UNK"
_UNKNOWN_LABEL_PREFIX = "Acknowledged Unknown"


def _unknown_id(index):
    """Stable visible id for the index-th (0-based) acknowledged unknown."""
    return f"{_UNKNOWN_ID_PREFIX}-{index + 1:03d}"


def _unknown_registry(state):
    """Acknowledged-unknown registry (Phase 3B-1). Full verbatim is carried once
    here so Section 8 can reference it by id instead of re-copying it. Section 5
    stays the primary visible location. No unknown is deleted and no claim is
    added. Empty list when there are no acknowledged unknowns."""
    reg = []
    for i, u in enumerate(getattr(state, "acknowledged_unknowns", [])):
        reg.append({
            "unknown_id": _unknown_id(i),
            "label": f"{_UNKNOWN_LABEL_PREFIX} {i + 1}",
            "content": getattr(u, "verbatim", None),
            "gap_context": getattr(u, "gap_context", None),
            "category_basis": getattr(u, "category_basis", None),
            "source": "inventor_stated",
        })
    return reg


def _s2(state):
    resolved_problem = _resolved_problem(state)
    # Phase 3A: surface the fixed-slot evidence id next to the full text that is
    # shown once here, so Section 4 can reference it instead of re-copying it.
    known_problem = _ev(resolved_problem)
    if known_problem is not None:
        known_problem["evidence_id"] = _EVIDENCE_PROBLEM_ID
    known_mechanism = _ev(getattr(state, "known_mechanism", None))
    if known_mechanism is not None:
        known_mechanism["evidence_id"] = _EVIDENCE_MECHANISM_ID
    return {
        "maturity_level":         state.maturity_level,
        "maturity_label":         _MATURITY_LABELS.get(state.maturity_level, "Unknown"),
        "domain_signal":          getattr(state, "domain_signal", None),
        "known_problem":          known_problem,
        "known_problem_note":     None if resolved_problem else
                                  "Problem evidence has not yet been captured clearly.",
        "known_mechanism":        known_mechanism,
        "known_boundaries":       [_ev(b) for b in getattr(state, "known_boundaries", []) if b],
        "assessment_completeness": _completeness(state),
    }

def _s3(state, open_gaps):
    cap = getattr(state, "domain_signal", None) or "unknown"
    return {
        "capabilities_assessed": [{
            "capability_id":  cap,
            "maturity_level": state.maturity_level,
            "overall_quality": _overall_quality(state),
            "gaps_total":  len(state.gaps),
            "gaps_open":   len(open_gaps),
            "gaps_resolved": len([g for g in state.gaps if g.status == CLOSED]),
            "gaps_detail": [{"gap_type": g.gap_type,
                             "gap_label": _GAP_LABELS.get(g.gap_type, g.gap_type),
                             "status": g.status,
                             "status_label": _STATUS_LABELS.get(g.status, g.status),
                             "iterations_open": g.iterations_open} for g in state.gaps],
        }],
        "cross_capability_conflicts": [],
        "note": "Single-capability assessment. Cross-capability deferred to Phase 6.",
    }

def _s4(state):
    reqs, n = [], 1
    problem = _resolved_problem(state)
    if problem:
        # Phase 3A: reference the registry entry instead of re-copying the full
        # problem text (which is shown once in Section 2 / the evidence registry).
        reqs.append({"id": f"REQ-{n:03d}", "type": "functional",
            "statement": f"See {_EVIDENCE_PROBLEM_ID} — {_EVIDENCE_PROBLEM_LABEL}",
            "evidence_id": _EVIDENCE_PROBLEM_ID,
            "source": "session_evidence",
            "evidence_quality": problem.quality, "resolution_status": "stated",
            "note": "Derived from inventor-stated problem evidence. Verification required."})
        n += 1
    if getattr(state, "known_mechanism", None):
        # Phase 3A: reference the registry entry instead of re-copying the full
        # mechanism text (which is shown once in Section 2 / the evidence registry).
        reqs.append({"id": f"REQ-{n:03d}", "type": "technical",
            "statement": f"See {_EVIDENCE_MECHANISM_ID} — {_EVIDENCE_MECHANISM_LABEL}",
            "evidence_id": _EVIDENCE_MECHANISM_ID,
            "source": "session_evidence",
            "evidence_quality": state.known_mechanism.quality, "resolution_status": "stated",
            "note": "Component-level specification required before implementation."})
        n += 1
    for g in state.gaps:
        if g.status == CLOSED:
            reqs.append({"id": f"REQ-{n:03d}", "type": "constraint",
                "statement": f"{_GAP_LABELS.get(g.gap_type, g.gap_type)} addressed",
                "source": "gap_resolution", "evidence_quality": REASONED,
                "resolution_status": "resolved", "note": None})
            n += 1
    return {"requirements": reqs, "total": len(reqs),
            "note": "Requirements derived from session evidence in MVP."}

def _s5(state):
    asmp, n = [], 1
    mech = getattr(state, "known_mechanism", None)
    if mech:
        q = getattr(mech, "quality", None)
        asmp.append({"id": f"ASM-{n:03d}",
            "assumption": "The stated mechanism is technically feasible" if q == ASSERTED
                          else "The stated mechanism operates as described",
            "validation_approach": "Prototype or simulation required" if q == ASSERTED
                                   else "Component-level testing to confirm operating principle",
            "risk_if_invalid": "Session assessment may not reflect true feasibility",
            "basis": f"{q} evidence"})
        n += 1
    for g in state.gaps:
        if g.status == OPEN:
            asmp.append({"id": f"ASM-{n:03d}",
                "assumption": f"{_GAP_LABELS.get(g.gap_type, g.gap_type)} can be resolved",
                "validation_approach": "Address open gap in next session",
                "risk_if_invalid": "Assessment remains incomplete at this gap",
                "basis": "Open gap"})
            n += 1
    # Phase 3B-1: attach the stable unknown id (UNK-00N) next to the full text
    # that is shown once here, so Section 8 can reference it instead of re-copying
    # it. Full verbatim is unchanged and still shown in this primary location.
    inventor_unknowns = [
        {"unknown_id": _unknown_id(i),
         "iteration": u.iteration, "gap_context": u.gap_context,
         "statement": u.verbatim, "source": "inventor_stated"}
        for i, u in enumerate(getattr(state, "acknowledged_unknowns", []))
    ]
    return {
        "assumptions":       asmp,
        "total":             len(asmp),
        "inventor_unknowns": inventor_unknowns,
        "note": "Assumptions inferred from session state in MVP. "
                "Inventor-stated unknowns recorded separately.",
    }

def _s6(state, open_gaps):
    risks, n = [], 1
    if state.maturity_level < 2:
        risks.append({"id": f"RISK-{n:03d}", "category": "assessment_completeness",
            "description": f"Session is at {_MATURITY_LABELS.get(state.maturity_level)}. Assessment incomplete.",
            "severity": "high" if state.maturity_level == 0 else "medium",
            "residual_risk": "Assessment remains incomplete until maturity_level >= 2.",
            "status": "open"})
        n += 1
    q = _overall_quality(state)
    if q == ASSERTED:
        risks.append({"id": f"RISK-{n:03d}", "category": "evidence_quality",
            "description": "All evidence is ASSERTED (inventor-stated, unvalidated).",
            "severity": "high",
            "residual_risk": "Technical claims may not reflect actual feasibility.",
            "status": "open"})
        n += 1
    elif q == REASONED:
        risks.append({"id": f"RISK-{n:03d}", "category": "evidence_quality",
            "description": "Evidence is REASONED (substantiated but not demonstrated).",
            "severity": "low",
            "residual_risk": "Prototype validation recommended before detailed design.",
            "status": "open"})
        n += 1
    for g in open_gaps:
        risks.append({"id": f"RISK-{n:03d}", "category": "unresolved_gap",
            "description": f"{_GAP_LABELS.get(g.gap_type, g.gap_type)} unresolved after {g.iterations_open} iteration(s).",
            "severity": "high" if g.iterations_open >= 3 else "medium",
            "residual_risk": "Gap must be addressed before assessment is complete.",
            "status": "open"})
        n += 1
    return {"risks": risks, "total": len(risks),
            "high_count":   sum(1 for r in risks if r["severity"] == "high"),
            "medium_count": sum(1 for r in risks if r["severity"] == "medium"),
            "low_count":    sum(1 for r in risks if r["severity"] == "low")}

def _s7(state, open_gaps):
    key = (min(state.maturity_level, 2), len(open_gaps) > 0)
    verdict, rationale = _RECOMMENDATION_A.get(key,
        ("REVISE", "Insufficient evidence to recommend proceeding."))
    cat_d = [{"item_type": "open_gap", "gap_type": g.gap_type,
              "gap_label": _GAP_LABELS.get(g.gap_type, g.gap_type),
              "action": f"Provide substantive evidence for {_GAP_LABELS.get(g.gap_type, g.gap_type).lower()}",
              "priority": "high" if g.iterations_open >= 2 else "normal"}
             for g in open_gaps]
    if state.maturity_level < 2:
        cat_d.append({"item_type": "maturity_gap", "gap_type": None,
            "gap_label": "Maturity level",
            "action": "Continue with technically substantive answers to reach Level 2.",
            "priority": "high"})
    # F-1 truthfulness: when derived verified readiness is NOT met, a positive
    # verdict/rationale must not imply verified readiness. Stored maturity and the
    # stored gap lifecycle remain visible as stored state (deliverable_eligible,
    # maturity_label and gap statuses are unchanged); derived readiness is shown
    # separately. We qualify only the already-rendered verdict/rationale and add a
    # visible Open Item — no template change, no new verdict value, no change to
    # stored eligibility, and no claim that the idea is technically verified.
    derived_ready = _derived_verified_ready(state)
    if not derived_ready and verdict in ("PROCEED", "PROCEED WITH CAUTION"):
        verdict = "PROCEED WITH CAUTION"
        rationale = (
            "Structurally progressed: stored maturity and the stored gap "
            "lifecycle are recorded as shown, but derived verified readiness is "
            "NOT met — recorded supporting evidence remains unvalidated, "
            "provisional, pending, or contradicted. Proceed only with "
            "verification caution; this is not a determination that the idea is "
            "technically verified, and unresolved validation items remain even "
            "where stored gaps are CLOSED.")
        cat_d.append({"item_type": "validation_unresolved", "gap_type": None,
            "gap_label": "Evidence validation",
            "action": "Validate the supporting evidence (specialist review, "
                      "demonstration, or independent verification): verification "
                      "remains incomplete even where stored gaps are CLOSED.",
            "priority": "high"})
    return {
        "category_a_proceed_revise_block": {"verdict": verdict, "rationale": rationale,
            "basis": {"maturity_level": state.maturity_level,
                      "open_gap_count": len(open_gaps),
                      "evidence_quality": _overall_quality(state),
                      "derived_verified_ready": derived_ready}},
        "category_b_material_selection": {"status": "DEFERRED",
            "note": "Requires Options Database (ODS-001). Not in the current MVP."},
        "category_c_manufacturing":      {"status": "DEFERRED",
            "note": "Requires Options Database (ODS-001). Not in the current MVP."},
        "category_d_open_items": cat_d,
    }

def _s8(open_gaps, state=None):
    items = [
        {"id": f"OPEN-{i+1:03d}", "type": "open_gap",
         "gap_type": g.gap_type,
         "gap_label": _GAP_LABELS.get(g.gap_type, g.gap_type),
         "status": g.status, "iterations_open": g.iterations_open,
         "resolution": "Address in next session with substantive evidence"}
        for i, g in enumerate(open_gaps)
    ]
    for i, u in enumerate(getattr(state, "acknowledged_unknowns", [])):
        # Phase 3B-1: reference the unknown registry entry (UNK-00N) instead of
        # re-copying the full verbatim text (shown once in Section 5 / the
        # unknown registry). Existing item id, gap_context, iteration, and source
        # are preserved. Sections 10/11 are intentionally unchanged in this PR.
        uid = _unknown_id(i)
        items.append({
            "id": f"UNKNOWN-{u.iteration:03d}",
            "type": "acknowledged_unknown",
            "gap_context": u.gap_context,
            "statement": f"See {uid} — Acknowledged unknown",
            "unknown_id": uid,
            "iteration": u.iteration,
            "source": "inventor_stated",
        })
    return {
        "items": items,
        "open_gap_count": len(open_gaps),
        "acknowledged_unknown_count": len(getattr(state, "acknowledged_unknowns", [])),
        "cross_capability_conflicts": [], "conflict_count": 0,
        "note_conflicts": "Cross-capability conflict detection deferred to Phase 6.",
    }

def _s9(state):
    """
    Stage 3 reasoning areas: surface each Stage 3 gap that exists in the state
    with its human-readable label, current status, and the inventor's captured
    accepted evidence (or an honest missing-evidence statement). Reads existing
    state only — no mutation, no validation/feasibility claim. Empty for
    Stage-2-only sessions (no Stage 3 gaps present).
    """
    items = []
    for g in state.gaps:
        if g.gap_type in STAGE_3_GAP_TYPES:
            ev = [_ev(e) for e in getattr(g, "evidence", []) if e]
            items.append({
                "gap_type":     g.gap_type,
                "gap_label":    _GAP_LABELS.get(g.gap_type, g.gap_type),
                "status":       g.status,
                "status_label": _STATUS_LABELS.get(g.status, g.status),
                "evidence":     ev,
                "missing_evidence_statement": None if ev else _STAGE3_MISSING_EVIDENCE,
            })
    return {
        "items": items,
        "stage3_gap_count": len(items),
        "note": "Stage 3 reasoning areas. Captured evidence is the inventor's own "
                "substantiated wording. This is not validation, feasibility "
                "confirmation, completeness, or expert review.",
    }


def _s10(state, open_gaps):
    """
    Recommended next steps — synthesized ONLY from already-computed state and
    captured evidence. No new analysis, no domain-specific advice, no invented
    recommendations. Each step names the existing state element it derives from.

    Sources (in order): unresolved gaps (OPEN/PARTIAL), maturity below Level 2,
    inventor-stated unknowns, and an evidence-strength step when the leading
    evidence is REASONED but not yet DEMONSTRATED. Duplicate source evidence
    (e.g. an unknown stated twice) does not create duplicate actions. Empty ->
    a single honest statement that no outstanding next steps were identified.
    """
    steps, seen = [], set()

    def _add(action, priority, basis):
        if action in seen:                 # duplicate source -> no duplicate action
            return
        seen.add(action)
        steps.append({"id": f"NEXT-{len(steps) + 1:03d}",
                      "action": action, "priority": priority, "basis": basis})

    for g in open_gaps:
        label = _GAP_LABELS.get(g.gap_type, g.gap_type)
        _add(f"Provide substantive evidence for {label.lower()}.",
             "high" if g.iterations_open >= 2 else "normal",
             f"open_gap:{g.gap_type}")
    if state.maturity_level < 2:
        _add("Continue with technically substantive answers to reach "
             "Level 2 (mechanism established).",
             "high", f"maturity_level:{state.maturity_level}")
    # Phase 3B-2a: reference the unknown registry entry (UNK-00N, position-based
    # to match Section 5/8) instead of repeating the full verbatim, which is shown
    # once in Section 5 and referenced in Section 8. Dedup stays keyed on the
    # verbatim (not the UNK id), so a repeated unknown still yields no duplicate
    # action — the first occurrence's UNK id is the one referenced. Basis,
    # priority, and NEXT-00N numbering are unchanged.
    seen_unknown_text = set()
    for i, u in enumerate(getattr(state, "acknowledged_unknowns", [])):
        if u.verbatim in seen_unknown_text:   # duplicate source -> no duplicate action
            continue
        seen_unknown_text.add(u.verbatim)
        _add(f"Resolve the inventor-stated unknown: See {_unknown_id(i)} "
             f"— Acknowledged unknown",
             "normal", f"acknowledged_unknown:iteration_{u.iteration}")
    if _overall_quality(state) == REASONED:
        _add("Validate the leading claims with a prototype or "
             "demonstration to raise evidence from Reasoned to Demonstrated.",
             "normal", "evidence_quality:REASONED")
    return {
        "items": steps,
        "count": len(steps),
        "empty_statement": None if steps else
            "No outstanding next steps identified from the current session state.",
        "note": "Synthesized from current session state and captured evidence. "
                "Advisory only; no new analysis was performed.",
    }


_PLAN_MAX_EXPERIMENTS = 3
_OWNER_CRITERION_REQUIRED = "Owner-defined criterion required."

# Stable prototype-experiment identifiers. The id is derived ONLY from the
# experiment's source_type and the normalized verbatim source content — never
# from list position or any synthesized display wording — so user-authored
# planning metadata (a later increment) can attach to it safely. SHA-256 is used
# (not the process-randomized built-in hash()). The id is deterministic and
# stable for the same source_type + normalized source content across re-assembly
# and process restarts; it is NOT claimed globally permanent.
_EXPERIMENT_ID_VERSION = "v1"
_EXPERIMENT_ID_DIGEST_LEN = 32  # hex chars (128 bits); silent-collision risk negligible at this scope


def _canonical_source(text):
    """Narrow, documented canonicalization for stable identity: trim, collapse
    internal whitespace runs to a single space, and Unicode-casefold. No
    paraphrase, stemming, stopword removal, or lexical-dedup signature."""
    import re
    return re.sub(r"\s+", " ", (text or "").strip()).casefold()


def _experiment_id(source_type, source_text):
    """exp_v1_<source_type>_<sha256(source_type + U+001F + normalized source),
    truncated to _EXPERIMENT_ID_DIGEST_LEN lowercase hex chars (128 bits)>."""
    canonical = _canonical_source(source_text)
    payload = f"{source_type}\x1f{canonical}".encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()[:_EXPERIMENT_ID_DIGEST_LEN]
    return f"exp_{_EXPERIMENT_ID_VERSION}_{source_type}_{digest}"


def _resolve_success_criterion(exp, eid, source_text, state):
    """Set success_criterion / _provenance / _status on an experiment item.
    Precedence: a user-authored criterion (state.success_criteria[eid]) wins;
    else an explicit owner criterion stated verbatim in the source; else the
    honest "Owner-defined criterion required." placeholder. Never invents,
    grades, validates, or claims a criterion was met. status is 'captured' or
    'required' — never 'met'/'validated'."""
    user = (getattr(state, "success_criteria", None) or {}).get(eid)
    user_text = (getattr(user, "criterion", "") or "").strip() if user else ""
    if user_text:
        exp["success_criterion"] = user_text
        exp["success_criterion_provenance"] = getattr(user, "provenance", "user_defined")
        exp["success_criterion_status"] = "captured"
        return
    scanned = _owner_success_criterion(source_text)
    if scanned:
        exp["success_criterion"] = scanned
        exp["success_criterion_provenance"] = "source_stated"
        exp["success_criterion_status"] = "captured"
        return
    exp["success_criterion"] = _OWNER_CRITERION_REQUIRED
    exp["success_criterion_provenance"] = None
    exp["success_criterion_status"] = "required"


def _stale_success_criteria(state, current_ids):
    """User criteria whose experiment_id is no longer generated. Preserved and
    surfaced honestly; never reattached. Deterministic (dict insertion order)."""
    stale = []
    for eid, sc in (getattr(state, "success_criteria", None) or {}).items():
        if eid in current_ids:
            continue
        txt = (getattr(sc, "criterion", "") or "").strip()
        if txt:
            stale.append({"experiment_id": eid, "criterion": txt,
                          "provenance": getattr(sc, "provenance", "user_defined")})
    return stale
_PLAN_STOPWORDS = {
    "that", "this", "with", "from", "would", "which", "have", "been", "they",
    "their", "there", "when", "what", "into", "such", "than", "then", "them",
    "because", "could", "should", "about", "where", "while", "still", "only",
    "also", "does", "your", "yet", "the", "and", "for", "are", "but", "not",
}


def _plan_sig(text):
    """Significant-token signature of a source string, for uncertainty dedup."""
    import re
    toks = re.findall(r"[a-z0-9]+", (text or "").lower())
    return frozenset(t for t in toks if len(t) > 3 and t not in _PLAN_STOPWORDS)


def _lexically_overlaps(a, b):
    """Best-effort LEXICAL overlap test between two source token signatures: True
    when one is a subset of the other, or token-set Jaccard overlap >= 0.6. This
    is a heuristic to suppress near-duplicate sources; it does NOT establish
    semantic equivalence and may keep two lexically distinct sources that test a
    related idea, or (rarely) merge two that differ semantically."""
    if not a or not b:
        return False
    if a <= b or b <= a:
        return True
    inter, union = len(a & b), len(a | b)
    return union > 0 and inter / union >= 0.6


def _owner_success_criterion(text):
    """Return a verbatim owner-provided success criterion if the captured source
    explicitly states one ("success criterion: ..."), else None. Never invents
    a criterion."""
    import re
    m = re.search(r"success criterion\s*[:\-]\s*(.+)", text or "", re.I)
    if not m:
        return None
    crit = m.group(1).strip()
    crit = re.split(r"(?<=[.!?])\s", crit)[0].strip()  # first sentence only
    return crit or None


def _plan_expertise(state):
    """First captured Expertise-Gap Awareness evidence content, or None.
    Supplies required expertise/tools ONLY when actually captured."""
    ega = state.get_gap(EXPERTISE_GAP_AWARENESS)
    if ega is not None:
        for e in getattr(ega, "evidence", []):
            c = (getattr(e, "content", "") or "").strip()
            if c:
                return c
    return None


def _s11(state):
    """
    Prototype & Test Plan — at most three traceable PROPOSED experiments that
    reorganize already-captured evidence into "what to test next". Deterministic;
    reads existing state only. Never invents specifications, thresholds,
    measurements, results, feasibility, validation, certification, safety, or
    expert conclusions. Success criteria are surfaced as owner-provided (verbatim)
    when captured, otherwise "Owner-defined criterion required."

    Source priority (de-duplicated by best-effort LEXICAL overlap only — not
    semantic equivalence — keeping the first-priority source):
      1. acknowledged unknowns;
      2. accepted ASSUMPTION_INVENTORY evidence (essential/untested assumption);
      3. a REASONED-but-not-DEMONSTRATED leading mechanism claim.
    Expertise-Gap Awareness evidence supplies required expertise/tools. The
    per-experiment `required_expertise_or_tools` field is retained unchanged for
    output backward-compatibility (schema fdc-001-mvp-v1); an additive
    section-level `shared_required_expertise` field carries the same captured
    text verbatim so the web view can render it once instead of per experiment.
    EGA evidence never creates a standalone experiment.
    """
    # Per-experiment expertise value — UNCHANGED from prior behavior (legacy
    # output contract). Same prefixed string on every item, or None.
    expertise = _plan_expertise(state)
    expertise_field = (
        f"Inventor-identified (Expertise-Gap Awareness): {expertise}"
        if expertise else None
    )
    # Additive, presentation-only shared field: the exact captured text (no
    # prefix, no summary, no split, no per-experiment mapping). The
    # "inventor-identified" framing is carried by the section heading. None when
    # no EGA evidence was captured.
    shared_expertise = expertise or None
    items, sigs, seen_ids = [], [], {}

    def _add(source_text, exp):
        if len(items) >= _PLAN_MAX_EXPERIMENTS:
            return
        sig = _plan_sig(source_text)
        if any(_lexically_overlaps(sig, s) for s in sigs):
            return  # near-duplicate source (best-effort lexical overlap) already covered
        sigs.append(sig)
        source_type = exp["traceability"]["source_type"]
        eid = _experiment_id(source_type, source_text)
        payload = (source_type, _canonical_source(source_text))
        if eid in seen_ids and seen_ids[eid] != payload:
            # Fail closed on a digest collision between distinct canonical
            # payloads; never silently reuse an id or invent an order-based suffix.
            raise ValueError(f"experiment_id collision for {eid!r}")
        seen_ids[eid] = payload
        exp["experiment_id"] = eid
        _resolve_success_criterion(exp, eid, source_text, state)
        exp["required_expertise_or_tools"] = expertise_field  # legacy per-item field, unchanged
        items.append(exp)

    # Priority 1 — acknowledged unknowns. Phase 3B-2b: the user-facing "Based on:"
    # line references the acknowledged unknown by its stable registry id (See
    # UNK-00N) instead of re-copying the full verbatim, mirroring Section 10. The
    # index is the same 1-based position used by _unknown_registry / Section 5 / 8
    # / 10, so the reference resolves to the same entry. Presentation-only: the
    # full verbatim is still passed as the identity/digest/dedup source_text and is
    # still carried in traceability.content below; _experiment_id, _plan_sig, dedup,
    # and success-criterion resolution are unchanged.
    for i, u in enumerate(getattr(state, "acknowledged_unknowns", [])):
        verbatim = (getattr(u, "verbatim", "") or "").strip()
        if not verbatim:
            continue
        _add(verbatim, {
            "experiment_title": "Proposed experiment: resolve a stated unknown",
            "objective": "Evaluate the inventor's stated unknown under controlled "
                         "conditions to reduce its uncertainty.",
            "source_basis": f"See {_unknown_id(i)} — Acknowledged unknown",
            "minimum_prototype": "A minimal build that exercises only the part of "
                                 "the described mechanism this unknown depends on.",
            "what_to_observe": "Observe whether the stated unknown can be "
                               "distinguished or measured under conditions you control.",
            "failure_or_revision_condition": "If the unknown cannot be resolved as "
                "assumed, revise the assumption or the mechanism that depends on it.",
            "expected_evidence_upgrade": "Reduce this uncertainty and move the "
                "dependent claim toward Demonstrated.",
            "traceability": {"source_type": "acknowledged_unknown",
                             "source_ref": f"iteration_{u.iteration}",
                             "content": verbatim},
        })

    # Priority 2 — accepted ASSUMPTION_INVENTORY evidence (essential/untested).
    ai = state.get_gap(ASSUMPTION_INVENTORY)
    if ai is not None:
        for e in getattr(ai, "evidence", []):
            content = (getattr(e, "content", "") or "").strip()
            if not content:
                continue
            _add(content, {
                "experiment_title": "Proposed experiment: test an essential assumption",
                "objective": "Test an essential or untested assumption the mechanism "
                             "depends on.",
                "source_basis": f"Assumption Inventory evidence: \"{content}\"",
                "minimum_prototype": "A minimal build that puts the stated assumption "
                                     "under test without the full system.",
                "what_to_observe": "Observe whether the assumption holds under "
                                   "conditions you control.",
                "failure_or_revision_condition": "If the assumption does not hold, "
                    "revise the mechanism or the design choices that rely on it.",
                "expected_evidence_upgrade": "Move this assumption from Reasoned "
                    "toward Demonstrated.",
                "traceability": {"source_type": "assumption_inventory_evidence",
                                 "source_ref": "ASSUMPTION_INVENTORY",
                                 "content": content},
            })

    # Priority 3 — a REASONED-but-not-DEMONSTRATED leading mechanism claim.
    if _overall_quality(state) == REASONED:
        mech = getattr(state, "known_mechanism", None)
        claim = (getattr(mech, "content", "") or "").strip()
        if claim:
            _add(claim, {
                "experiment_title": "Proposed experiment: demonstrate the leading "
                                    "mechanism claim",
                "objective": "Build a minimum prototype of the described mechanism and "
                             "observe whether it behaves as the inventor described, to "
                             "raise the evidence from Reasoned toward Demonstrated.",
                "source_basis": f"Leading claim at Reasoned quality: \"{claim}\"",
                "minimum_prototype": "A minimal end-to-end build of the described "
                                     "operating principle, no more than needed to "
                                     "observe the claimed behavior.",
                "what_to_observe": "Observe whether the described input-to-output "
                                   "behavior occurs as stated.",
                "failure_or_revision_condition": "If the described behavior does not "
                    "occur, revise the mechanism before relying on it.",
                "expected_evidence_upgrade": "Reasoned -> Demonstrated.",
                "traceability": {"source_type": "reasoned_leading_claim",
                                 "source_ref": "known_mechanism",
                                 "content": claim},
            })

    stale = _stale_success_criteria(state, {it["experiment_id"] for it in items})
    return {
        "title": "Prototype & Test Plan",
        "items": items,
        "count": len(items),
        # One shared, plan-level expertise/tools statement (verbatim captured
        # Expertise-Gap Awareness evidence), or None when none was captured.
        # Not mapped to any single experiment.
        "shared_required_expertise": shared_expertise,
        "empty_statement": None if items else
            "No evidence-grounded prototype experiment can be proposed from the "
            "currently captured information.",
        "stale_criteria": stale,
        "stale_criteria_notice": None if not stale else
            "A previously entered success criterion no longer matches a current "
            "proposed experiment. It has been preserved but is not applied.",
        "note": "Proposed experiments synthesized from your own captured evidence. "
                "Advisory only: nothing here has been built, tested, demonstrated, "
                "validated, certified, or shown feasible. You define the success "
                "criteria.",
    }


def _now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def _ev(ev):
    if ev is None: return None
    validation = getattr(ev, "validation_status", UNVALIDATED)
    return {"content": getattr(ev, "content", str(ev)),
            "quality": getattr(ev, "quality", None),
            "quality_label": _QUALITY_LABELS.get(getattr(ev, "quality", None), "Unknown"),
            # Increment 2: provenance and validation are surfaced separately from
            # quality, so REASONED is never presented as verified by quality alone.
            "provenance": getattr(ev, "provenance", LEGACY_UNSPECIFIED),
            "validation_status": validation,
            "validation_label": _VALIDATION_LABELS.get(validation, "Not validated")}

def _resolved_problem(state):
    """
    The Evidence to display as the inventor's actual *problem*, selected by
    PROVENANCE (capture origin) — never by keyword or string analysis, and
    never the mechanism. Returns an Evidence or None.

    Priority:
      1. state.idea_summary — the dedicated problem-establishment capture, set
         once at the maturity-0 "describe the problem" step from a REASONED+
         response (_trim_idea_summary) and NOT exposed to RISK-002 mechanism
         pollution. When present it is the most reliable problem provenance, and
         it must win over a Problem–Mechanism Fit answer that happens to lead
         with mechanism-fit wording (e.g. "This mechanism is a good fit because…").
      2. first accepted non-empty PROBLEM_MECHANISM_FIT evidence — the inventor's
         answer to the PMF problem question — used only when no idea_summary
         exists (e.g. legacy/water-leak states where the idea graded ASSERTED at
         problem establishment).
      3. None — honest absence ("Problem evidence has not yet been captured…").

    state.known_problem is deliberately NOT used: RISK-002 can populate it from a
    mechanism answer, so it lacks reliable problem-only provenance.
    """
    summary = (getattr(state, "idea_summary", None) or "").strip()
    if summary:
        # idea_summary is captured only from a REASONED+ problem-establishment
        # response; wrap it for uniform rendering. No quality is fabricated above
        # what the capture path already guarantees.
        return Evidence(content=summary, quality=REASONED, iteration=0)
    pmf = state.get_gap(PROBLEM_MECHANISM_FIT)
    if pmf is not None:
        for e in getattr(pmf, "evidence", []):
            if e and (getattr(e, "content", "") or "").strip():
                return e
    return None

def _txt(ev):
    return getattr(ev, "content", str(ev)) if ev else ""

def _overall_quality(state):
    qs = []
    for attr in ("known_problem", "known_mechanism"):
        ev = getattr(state, attr, None)
        if ev:
            q = getattr(ev, "quality", None)
            if q: qs.append(q)
    if not qs: return None
    order = {ASSERTED: 0, REASONED: 1, DEMONSTRATED: 2}
    return min(qs, key=lambda q: order.get(q, 0))

def _completeness(state):
    has_prob = getattr(state, "known_problem", None) is not None
    has_mech = getattr(state, "known_mechanism", None) is not None
    open_gaps = [g for g in state.gaps if g.status == OPEN]
    if state.maturity_level >= 2 and not open_gaps and has_mech:
        return ("INQUIRY COMPLETE — all current inquiry areas addressed. "
                "Technical validation and demonstration remain outstanding.")
    if state.maturity_level >= 1 and has_prob:
        return "PARTIAL — mechanism or boundaries still required"
    return "INCOMPLETE — problem statement not yet established"

def _eligible(state, open_gaps):
    return state.maturity_level >= 2 and len(open_gaps) == 0
