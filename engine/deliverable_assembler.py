"""
engine/deliverable_assembler.py
FDC-001 MVP Package Assembler — Phase 5 Step 1
Pure transformation: IdeaState -> FDC-001 package dict.
No LLM calls. No registry dependency. No IdeaState mutation.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import Any
from engine.idea_state import (
    IdeaState, ASSERTED, REASONED, DEMONSTRATED, OPEN, PARTIAL, CLOSED,
)

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
_QUALITY_LABELS = {
    ASSERTED:     "Asserted (inventor-stated, unvalidated)",
    REASONED:     "Reasoned (technically substantiated)",
    DEMONSTRATED: "Demonstrated (externally evidenced)",
    None:         "No evidence recorded",
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
}
_STATUS_LABELS = {
    OPEN: "Open", PARTIAL: "Partially addressed",
    CLOSED: "Resolved", "ACCEPTED_RISK": "Accepted risk",
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
        "section_8_unresolved_items":    _s8(open_gaps),
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
            "deliverable_eligible": _eligible(state, open_gaps),
        },
    }

def _s1():
    return {"tier": "standard", "text": _DISCLAIMER_STANDARD, "applies": True}

def _s2(state):
    return {
        "maturity_level":         state.maturity_level,
        "maturity_label":         _MATURITY_LABELS.get(state.maturity_level, "Unknown"),
        "domain_signal":          getattr(state, "domain_signal", None),
        "known_problem":          _ev(getattr(state, "known_problem", None)),
        "known_mechanism":        _ev(getattr(state, "known_mechanism", None)),
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
    if getattr(state, "known_problem", None):
        reqs.append({"id": f"REQ-{n:03d}", "type": "functional",
            "statement": _txt(state.known_problem), "source": "session_evidence",
            "evidence_quality": state.known_problem.quality, "resolution_status": "stated",
            "note": "Derived from inventor-stated problem evidence. Verification required."})
        n += 1
    if getattr(state, "known_mechanism", None):
        reqs.append({"id": f"REQ-{n:03d}", "type": "technical",
            "statement": _txt(state.known_mechanism), "source": "session_evidence",
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
    return {"assumptions": asmp, "total": len(asmp),
            "note": "Assumptions inferred from session state in MVP."}

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
    return {
        "category_a_proceed_revise_block": {"verdict": verdict, "rationale": rationale,
            "basis": {"maturity_level": state.maturity_level,
                      "open_gap_count": len(open_gaps),
                      "evidence_quality": _overall_quality(state)}},
        "category_b_material_selection": {"status": "DEFERRED",
            "note": "Requires Options Database (ODS-001). Not in Phase 5 MVP."},
        "category_c_manufacturing":      {"status": "DEFERRED",
            "note": "Requires Options Database (ODS-001). Not in Phase 5 MVP."},
        "category_d_open_items": cat_d,
    }

def _s8(open_gaps):
    return {
        "open_gaps": [{"id": f"OPEN-{i+1:03d}", "gap_type": g.gap_type,
            "gap_label": _GAP_LABELS.get(g.gap_type, g.gap_type),
            "status": g.status, "iterations_open": g.iterations_open,
            "resolution": "Address in next session with substantive evidence"}
            for i, g in enumerate(open_gaps)],
        "open_gap_count": len(open_gaps),
        "cross_capability_conflicts": [], "conflict_count": 0,
        "note_conflicts": "Cross-capability conflict detection deferred to Phase 6.",
    }

def _now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def _ev(ev):
    if ev is None: return None
    return {"content": getattr(ev, "content", str(ev)),
            "quality": getattr(ev, "quality", None),
            "quality_label": _QUALITY_LABELS.get(getattr(ev, "quality", None), "Unknown")}

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
        return "COMPLETE — eligible for Phase 5 deliverable"
    if state.maturity_level >= 1 and has_prob:
        return "PARTIAL — mechanism or boundaries still required"
    return "INCOMPLETE — problem statement not yet established"

def _eligible(state, open_gaps):
    return state.maturity_level >= 2 and len(open_gaps) == 0
