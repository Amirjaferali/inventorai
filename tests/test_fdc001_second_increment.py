"""
FDC002_SECOND_INCREMENT_ACCEPTANCE

Behavioral acceptance tests for the FDC-002 second increment (external evidence
re-entry and gap assessment) layered on the FDC-001 bicycle braking-detection
decision. Maps to the reconciled FDC-002 specification
(docs/product/FDC-002_EXTERNAL_EVIDENCE_REENTRY_AND_GAP_ASSESSMENT_SPECIFICATION.md),
including guarantees #31-#33 and the §12.1 governed route-contract reconciliation.

Tests assert actual behavior; static source inspection is used only for
prohibitions that cannot be observed behaviorally (e.g. no persistence import,
no caller-controlled verification status).
"""

import os
import sys
import json
import inspect

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine import decision_workspace as dw
from engine.decision_workspace import (
    DecisionRecord, DecisionError,
    OPERATOR_REPORTED_RESULT, EXTERNAL_REFERENCE, OBSERVED_FACT,
    OPERATOR_ENTERED, DERIVED_BY_RULE,
    EVIDENCE_VERIFICATION_UNVERIFIED,
    EVIDENCE_CLAIM_CLASSES,
    SUPPORTS_RESOLUTION, PARTIALLY_ADDRESSES, CONTRADICTS_ASSUMPTION, INSUFFICIENT,
    RESOLVED, REMAINS_BLOCKING, RECLASSIFIED_NONBLOCKING,
    EVIDENCE_ADDED, GAP_ASSESSED, GAP_RESOLVED_VIA_EVIDENCE,
    MISSING_PHYSICAL_OR_CALIBRATION_INFORMATION,
    BLOCKER_CLEARING_GUIDANCE,
    PROHIBITED_STATUS_VALUES,
    BLOCKED_BY_EVIDENCE_GAP,
    OBSERVED_FACT as _OBSERVED_FACT,
    ACTIVE,
)
from web.app import app, FDC001_DECISIONS

FDC002_SECOND_INCREMENT_ACCEPTANCE = "FDC002_SECOND_INCREMENT_ACCEPTANCE"


# --- helpers -----------------------------------------------------------------
def _physical_gap(rec):
    for g in rec.gaps:
        if rec.gap_blocker_code(g.gap_id) == MISSING_PHYSICAL_OR_CALIBRATION_INFORMATION:
            return g
    raise AssertionError("expected a seeded physical/calibration gap")


def _nonphysical_gap(rec):
    for g in rec.gaps:
        if rec.gap_blocker_code(g.gap_id) != MISSING_PHYSICAL_OR_CALIBRATION_INFORMATION:
            return g
    raise AssertionError("expected a seeded non-physical gap")


def _add_phys_evidence(rec, text="bench result: 2% false trigger over 50 brakes",
                       claim_class=OPERATOR_REPORTED_RESULT,
                       provenance=OPERATOR_ENTERED, **kw):
    g = _physical_gap(rec)
    return rec.add_evidence(g.gap_id, text, claim_class, provenance, **kw)


def _make_comparable(rec):
    """Give >=2 active candidates a decision-relevant input so the physical gap
    actually gates readiness (blocked_by_evidence_gap) rather than rule 1."""
    actives = [c for c in rec.candidates if c.option_status == ACTIVE]
    for c in actives[:2]:
        rec.add_input("relevant note for %s" % c.name, OBSERVED_FACT,
                      OPERATOR_ENTERED, decision_relevant=True,
                      candidate_ids=[c.candidate_id])


def _snapshot(rec):
    return {
        "rev": rec.revision,
        "hist": len(rec.history),
        "readiness": rec.readiness_status,
        "gaps": [(g.gap_id, g.blocks_readiness) for g in rec.gaps],
        "evidence": len(rec.evidence),
        "assessments": len(rec.gap_assessments),
        "blockers": sorted(b.code for b in rec.blocking_reasons),
        "impact": rec.change_impact_summary,
    }


def _start(client):
    start = client.get("/decision-workspace", follow_redirects=False)
    did = start.headers["Location"].rstrip("/").split("/")[-1]
    return did, FDC001_DECISIONS[did]


# 1 -------------------------------------------------------------- evidence model
def test_operator_reported_result_evidence_accepted():
    rec = DecisionRecord()
    ev = _add_phys_evidence(rec, claim_class=OPERATOR_REPORTED_RESULT)
    assert ev in rec.evidence
    assert ev.claim_class == OPERATOR_REPORTED_RESULT
    assert ev.linked_gap_id == _physical_gap(rec).gap_id


# 2 -------------------------------------------------------------- evidence model
def test_external_reference_evidence_accepted():
    rec = DecisionRecord()
    ev = _add_phys_evidence(rec, claim_class=EXTERNAL_REFERENCE,
                            text="vendor datasheet calibration note")
    assert ev.claim_class == EXTERNAL_REFERENCE
    assert EVIDENCE_CLAIM_CLASSES == {OPERATOR_REPORTED_RESULT, EXTERNAL_REFERENCE}


# 3 -------------------------------------------------------- forbidden claim class
def test_observed_fact_rejected_for_evidence():
    rec = DecisionRecord()
    before = _snapshot(rec)
    try:
        _add_phys_evidence(rec, claim_class=OBSERVED_FACT)
        assert False, "observed_fact must be rejected for evidence"
    except DecisionError:
        pass
    assert _snapshot(rec)["evidence"] == before["evidence"] == 0
    assert _snapshot(rec)["hist"] == before["hist"]


# 4 ---------------------------------------- verification status is system-only (API)
def test_verification_status_is_not_a_caller_parameter():
    sig = inspect.signature(DecisionRecord.add_evidence)
    assert "verification_status" not in sig.parameters
    rec = DecisionRecord()
    ev = _add_phys_evidence(rec)
    assert ev.verification_status == EVIDENCE_VERIFICATION_UNVERIFIED == "unverified"


# 5 ---------------------------------- posted verification_status ignored (route)
def test_route_ignores_posted_verification_status():
    client = app.test_client()
    did, rec = _start(client)
    g = _physical_gap(rec)
    resp = client.post("/decision-workspace/%s/evidence" % did, data={
        "gap_id": g.gap_id, "text": "field test note",
        "claim_class": "operator_reported_result", "provenance": "operator_entered",
        "verification_status": "verified"})  # attacker-supplied; must be ignored
    assert resp.status_code == 302
    assert len(rec.evidence) == 1
    assert rec.evidence[0].verification_status == "unverified"
    obj = json.loads(client.get(
        "/decision-workspace/%s/export" % did).get_data(as_text=True))
    assert all(e["verification_status"] == "unverified" for e in obj["evidence"])


# 6 ------------------------------------------------- linked-gap validation (domain)
def test_invalid_linked_gap_rejected_no_event():
    rec = DecisionRecord()
    before = _snapshot(rec)
    try:
        rec.add_evidence("gap-does-not-exist", "x", OPERATOR_REPORTED_RESULT,
                         OPERATOR_ENTERED)
        assert False
    except DecisionError:
        pass
    assert _snapshot(rec)["hist"] == before["hist"]
    assert rec.evidence == []


# 7 ----------------------------------------------- evidence creation single event
def test_evidence_entry_emits_exactly_one_evidence_added():
    rec = DecisionRecord()
    before = len(rec.history)
    _add_phys_evidence(rec)
    added = rec.history[before:]
    assert len(added) == 1
    assert added[0].change_type == EVIDENCE_ADDED
    assert not any(e.change_type in (GAP_ASSESSED, GAP_RESOLVED_VIA_EVIDENCE)
                   for e in added)


# 8 ----------------------------------------------- evidence alone, readiness fixed
def test_evidence_entry_leaves_readiness_unchanged():
    rec = DecisionRecord()
    _make_comparable(rec)
    before = rec.readiness_status
    _add_phys_evidence(rec)
    assert rec.readiness_status == before
    # the physical gap still blocks; no auto-resolution
    assert _physical_gap(rec).blocks_readiness is True


# 9 ------------------------------------------------- candidate relevance validation
def test_invalid_candidate_in_evidence_rejected_no_mutation():
    rec = DecisionRecord()
    before = _snapshot(rec)
    g = _physical_gap(rec)
    try:
        rec.add_evidence(g.gap_id, "x", OPERATOR_REPORTED_RESULT, OPERATOR_ENTERED,
                         candidate_ids=["cand-nope"])
        assert False
    except DecisionError:
        pass
    assert rec.evidence == []
    assert _snapshot(rec)["hist"] == before["hist"]


# 10 -------------------------------------------------------- blank evidence text
def test_blank_evidence_text_rejected():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    try:
        rec.add_evidence(g.gap_id, "   ", OPERATOR_REPORTED_RESULT, OPERATOR_ENTERED)
        assert False
    except DecisionError:
        pass
    assert rec.evidence == []


# 11 ----------------------------------- evidence_version + limitations preserved
def test_evidence_version_and_limitations_preserved_in_export():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = rec.add_evidence(g.gap_id, "bench sample", OPERATOR_REPORTED_RESULT,
                          OPERATOR_ENTERED, evidence_version="proto-rev-B",
                          limitations="single indoor sample, no vibration")
    assert ev.evidence_version == "proto-rev-B"
    assert ev.limitations == "single indoor sample, no vibration"
    # blank optional metadata normalizes to None
    ev2 = rec.add_evidence(g.gap_id, "second", EXTERNAL_REFERENCE, OPERATOR_ENTERED,
                           evidence_version="   ", limitations="")
    assert ev2.evidence_version is None and ev2.limitations is None
    obj = json.loads(rec.to_json())
    exported = {e["evidence_id"]: e for e in obj["evidence"]}
    assert exported[ev.evidence_id]["evidence_version"] == "proto-rev-B"
    assert exported[ev.evidence_id]["limitations"] == "single indoor sample, no vibration"
    assert exported[ev2.evidence_id]["evidence_version"] is None
    assert exported[ev2.evidence_id]["limitations"] is None


# 12 --------------------------------------- assessment supports_resolution+remains
def test_supports_resolution_with_remains_blocking_records_assessment():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    before = len(rec.history)
    ga = rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION,
                        "looks supportive but owner defers", REMAINS_BLOCKING)
    assert ga in rec.gap_assessments
    assert g.blocks_readiness is True  # remains_blocking did not clear it
    added = rec.history[before:]
    assert len(added) == 1 and added[0].change_type == GAP_ASSESSED


# 13 ------------------------------------ partially_addresses leaves gap blocking
def test_partially_addresses_leaves_gap_blocking():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    rec.assess_gap(g.gap_id, [ev.evidence_id], PARTIALLY_ADDRESSES,
                   "only covers indoor", REMAINS_BLOCKING)
    assert g.blocks_readiness is True


# 14 ------------------------------------------ insufficient leaves gap blocking
def test_insufficient_leaves_gap_blocking():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    rec.assess_gap(g.gap_id, [ev.evidence_id], INSUFFICIENT,
                   "not enough samples", REMAINS_BLOCKING)
    assert g.blocks_readiness is True


# 15 -------------------------------- contradicts_assumption leaves gap blocking
def test_contradicts_assumption_leaves_gap_blocking():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    rec.assess_gap(g.gap_id, [ev.evidence_id], CONTRADICTS_ASSUMPTION,
                   "result contradicts the assumption", REMAINS_BLOCKING)
    assert g.blocks_readiness is True


# 16 --------------------------- non-supporting assessment cannot resolve the gap
def test_resolution_requires_supports_resolution():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    for bad in (PARTIALLY_ADDRESSES, CONTRADICTS_ASSUMPTION, INSUFFICIENT):
        before = _snapshot(rec)
        try:
            rec.assess_gap(g.gap_id, [ev.evidence_id], bad, "r", RESOLVED,
                           resolution_rationale="should be rejected")
            assert False, "non-supporting assessment must not resolve"
        except DecisionError:
            pass
        assert g.blocks_readiness is True
        assert _snapshot(rec)["hist"] == before["hist"]


# 17 ------------------------------------------------- invalid resolution decision
def test_invalid_resolution_decision_rejected():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    try:
        rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION, "r",
                       "definitely_resolved")
        assert False
    except DecisionError:
        pass
    assert rec.gap_assessments == []


# 18 ----------------------------------------------- missing assessment rationale
def test_missing_assessment_rationale_rejected():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    try:
        rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION, "  ",
                       REMAINS_BLOCKING)
        assert False
    except DecisionError:
        pass
    assert rec.gap_assessments == []


# 19 ----------------------------------------------- missing resolution rationale
def test_missing_resolution_rationale_rejected_for_clearing():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    for decision in (RESOLVED, RECLASSIFIED_NONBLOCKING):
        before = _snapshot(rec)
        try:
            rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION,
                           "supportive", decision, resolution_rationale="")
            assert False
        except DecisionError:
            pass
        assert g.blocks_readiness is True
        assert _snapshot(rec)["hist"] == before["hist"]


# 20 ---------------------------------------------------- empty evidence set
def test_assessment_requires_at_least_one_evidence():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    try:
        rec.assess_gap(g.gap_id, [], SUPPORTS_RESOLUTION, "r", REMAINS_BLOCKING)
        assert False
    except DecisionError:
        pass
    assert rec.gap_assessments == []


# 21 ------------------------------------------------- invalid evidence id ref
def test_unknown_evidence_id_in_assessment_rejected():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    _add_phys_evidence(rec)
    try:
        rec.assess_gap(g.gap_id, ["ev-nope"], SUPPORTS_RESOLUTION, "r",
                       REMAINS_BLOCKING)
        assert False
    except DecisionError:
        pass
    assert rec.gap_assessments == []


# 22 ----------------------------------------------- cross-gap evidence rejected
def test_cross_gap_evidence_rejected():
    rec = DecisionRecord()
    phys = _physical_gap(rec)
    other = _nonphysical_gap(rec)
    ev_other = rec.add_evidence(other.gap_id, "false-positive note",
                                OPERATOR_REPORTED_RESULT, OPERATOR_ENTERED)
    before = _snapshot(rec)
    try:
        rec.assess_gap(phys.gap_id, [ev_other.evidence_id], SUPPORTS_RESOLUTION,
                       "r", REMAINS_BLOCKING)
        assert False, "evidence linked to another gap must be rejected"
    except DecisionError:
        pass
    assert _snapshot(rec)["hist"] == before["hist"]
    assert rec.gap_assessments == []


# 23 ----------------------------------------------------- atomic failed assessment
def test_failed_assessment_is_atomic():
    rec = DecisionRecord()
    _make_comparable(rec)
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    before = _snapshot(rec)
    try:
        # supports_resolution + RESOLVED but missing resolution rationale -> fail
        rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION,
                       "supportive", RESOLVED, resolution_rationale=None)
        assert False
    except DecisionError:
        pass
    after = _snapshot(rec)
    assert after == before  # full-state snapshot proves no partial change
    assert rec.change_impact_summary is before["impact"]


# 24 -------------------------------------- successful resolved clears + recompute
def test_successful_resolved_clears_gap_and_recomputes_readiness():
    rec = DecisionRecord()
    _make_comparable(rec)
    # reclassify the non-physical gap so only the physical gap blocks
    rec.reclassify_gap(_nonphysical_gap(rec).gap_id, "owner accepts FP risk")
    assert rec.readiness_status == BLOCKED_BY_EVIDENCE_GAP
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    ga = rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION,
                        "bench result supports resolution", RESOLVED,
                        resolution_rationale="owner accepts the externally-produced result")
    assert ga.resolution_decision == RESOLVED
    assert g.blocks_readiness is False
    assert rec.readiness_status != BLOCKED_BY_EVIDENCE_GAP
    # deterministic recompute
    assert rec._compute_readiness() == rec.readiness_status


# 25 ----------------------------------- successful reclassified_nonblocking clears
def test_successful_reclassified_nonblocking_clears_gap():
    rec = DecisionRecord()
    _make_comparable(rec)
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    ga = rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION,
                        "supportive", RECLASSIFIED_NONBLOCKING,
                        resolution_rationale="owner reclassifies as non-blocking")
    assert g.blocks_readiness is False
    assert g.reclassification_rationale == "owner reclassifies as non-blocking"
    assert ga.resolution_decision == RECLASSIFIED_NONBLOCKING


# 26 -------------------------------------- duplicate resolution of cleared gap
def test_duplicate_resolution_rejected():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION, "supportive",
                   RESOLVED, resolution_rationale="cleared")
    assert g.blocks_readiness is False
    before = _snapshot(rec)
    try:
        rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION, "again",
                       RESOLVED, resolution_rationale="again")
        assert False, "already-non-blocking gap cannot be resolved again"
    except DecisionError:
        pass
    assert _snapshot(rec)["hist"] == before["hist"]


# 27 ------------------------------- exactly-one-event: gap_assessed (remains)
def test_history_cardinality_gap_assessed_only():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    before = len(rec.history)
    rec.assess_gap(g.gap_id, [ev.evidence_id], PARTIALLY_ADDRESSES, "r",
                   REMAINS_BLOCKING)
    added = rec.history[before:]
    assert len(added) == 1
    assert added[0].change_type == GAP_ASSESSED
    assert not any(e.change_type == GAP_RESOLVED_VIA_EVIDENCE for e in added)


# 28 ------------------- exactly-one-event: gap_resolved_via_evidence + audit
def test_history_cardinality_gap_resolved_via_evidence_only_with_audit():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    before = len(rec.history)
    rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION, "supportive",
                   RESOLVED, resolution_rationale="cleared")
    added = rec.history[before:]
    assert len(added) == 1
    e = added[0]
    assert e.change_type == GAP_RESOLVED_VIA_EVIDENCE
    assert not any(x.change_type == GAP_ASSESSED for x in added)
    d = e.details
    for k in ("gap_id", "evidence_ids", "assessment", "rationale",
              "resolution_decision", "resolution_rationale",
              "previous_blocks_readiness", "new_blocks_readiness"):
        assert k in d, "missing audit key %s" % k
    assert d["previous_blocks_readiness"] is True
    assert d["new_blocks_readiness"] is False
    assert d["evidence_ids"] == [ev.evidence_id]


# 29 --------------------------------------------- route guard: resolve physical
def test_route_guard_rejects_resolve_of_physical_gap():
    client = app.test_client()
    did, rec = _start(client)
    _make_comparable(rec)
    g = _physical_gap(rec)
    before = _snapshot(rec)
    resp = client.post("/decision-workspace/%s/gap" % did, data={
        "action": "resolve", "gap_id": g.gap_id})
    assert resp.status_code == 400
    assert any(x.gap_id == g.gap_id for x in rec.gaps)
    assert g.blocks_readiness is True
    assert _snapshot(rec) == before


# 30 ------------------------------------------- route guard: reclassify physical
def test_route_guard_rejects_reclassify_of_physical_gap():
    client = app.test_client()
    did, rec = _start(client)
    g = _physical_gap(rec)
    before = _snapshot(rec)
    resp = client.post("/decision-workspace/%s/gap" % did, data={
        "action": "reclassify", "gap_id": g.gap_id,
        "rationale": "should be ignored"})
    assert resp.status_code == 400
    assert any(x.gap_id == g.gap_id for x in rec.gaps)
    assert g.blocks_readiness is True
    assert _snapshot(rec) == before


# 31 ------------------------- non-physical legacy route behavior unchanged
def test_route_nonphysical_gap_still_resolves_and_reclassifies():
    client = app.test_client()
    did, rec = _start(client)
    np_gid = _nonphysical_gap(rec).gap_id
    # reclassify a non-physical gap still succeeds (302) and becomes non-blocking
    r = client.post("/decision-workspace/%s/gap" % did, data={
        "action": "reclassify", "gap_id": np_gid,
        "rationale": "owner accepts"})
    assert r.status_code == 302
    assert rec._gap(np_gid).blocks_readiness is False


# 32 ----------------------------------- domain methods remain compatible
def test_legacy_domain_methods_still_clear_physical_gap_programmatically():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    # the internal/programmatic contract is unchanged: resolve_gap removes it
    rec.resolve_gap(g.gap_id)
    assert all(x.gap_id != g.gap_id for x in rec.gaps)
    rec2 = DecisionRecord()
    g2 = _physical_gap(rec2)
    rec2.reclassify_gap(g2.gap_id, "programmatic reclassify")
    assert rec2._gap(g2.gap_id).blocks_readiness is False


# 33 ------------------------- FDC-002 evidence-assessment route is sole UI path
def test_route_evidence_then_assessment_clears_physical_gap():
    client = app.test_client()
    did, rec = _start(client)
    _make_comparable(rec)
    rec.reclassify_gap(_nonphysical_gap(rec).gap_id, "owner accepts FP")
    assert rec.readiness_status == BLOCKED_BY_EVIDENCE_GAP
    g = _physical_gap(rec)
    # record evidence via the route
    r1 = client.post("/decision-workspace/%s/evidence" % did, data={
        "gap_id": g.gap_id, "text": "field result supports resolution",
        "claim_class": "operator_reported_result", "provenance": "operator_entered"})
    assert r1.status_code == 302
    assert rec.readiness_status == BLOCKED_BY_EVIDENCE_GAP  # evidence alone: no change
    ev_id = rec.evidence[0].evidence_id
    # assess + decide via the route -> clears the physical gap
    r2 = client.post("/decision-workspace/%s/gap-assessment" % did, data={
        "gap_id": g.gap_id, "evidence_ids": [ev_id],
        "assessment": "supports_resolution", "rationale": "supportive",
        "resolution_decision": "resolved",
        "resolution_rationale": "owner accepts the result"})
    assert r2.status_code == 302
    assert g.blocks_readiness is False
    assert rec.readiness_status != BLOCKED_BY_EVIDENCE_GAP


# 34 ------------------------------- bounded route validation error (no mutation)
def test_route_assessment_validation_error_is_bounded_and_atomic():
    client = app.test_client()
    did, rec = _start(client)
    g = _physical_gap(rec)
    _add_phys_evidence(rec)
    ev_id = rec.evidence[0].evidence_id
    before = _snapshot(rec)
    # supports_resolution + resolved but no resolution_rationale -> bounded 400
    resp = client.post("/decision-workspace/%s/gap-assessment" % did, data={
        "gap_id": g.gap_id, "evidence_ids": [ev_id],
        "assessment": "supports_resolution", "rationale": "supportive",
        "resolution_decision": "resolved", "resolution_rationale": ""})
    assert resp.status_code == 400
    assert g.blocks_readiness is True
    assert _snapshot(rec) == before


# 35 ------------------------------------- blocker-clearing guidance present
def test_blocker_clearing_guidance_present_for_physical_blocker():
    rec = DecisionRecord()
    _make_comparable(rec)
    rec.reclassify_gap(_nonphysical_gap(rec).gap_id, "owner accepts FP")
    assert rec.readiness_status == BLOCKED_BY_EVIDENCE_GAP
    live = [b for b in rec.blocking_reasons
            if b.code == MISSING_PHYSICAL_OR_CALIBRATION_INFORMATION]
    assert len(live) == 1
    obj = json.loads(rec.to_json())
    exp = [b for b in obj["blocking_reasons"]
           if b["code"] == MISSING_PHYSICAL_OR_CALIBRATION_INFORMATION]
    assert len(exp) == 1
    assert exp[0]["clearing_guidance"]
    assert exp[0]["clearing_guidance"] == \
        BLOCKER_CLEARING_GUIDANCE[MISSING_PHYSICAL_OR_CALIBRATION_INFORMATION]
    assert "operator-reported and unverified" in exp[0]["clearing_guidance"].lower()


# 36 ----------------------------- export shape + audit recoverable
def test_export_shape_evidence_assessments_and_audit():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION, "supportive",
                   RESOLVED, resolution_rationale="cleared")
    obj = json.loads(rec.to_json())
    assert "evidence" in obj and "gap_assessments" in obj
    assert obj["evidence"][0]["evidence_id"] == ev.evidence_id
    assert obj["gap_assessments"][0]["resolution_decision"] == RESOLVED
    rv = [e for e in obj["history"]
          if e["change_type"] == GAP_RESOLVED_VIA_EVIDENCE][-1]
    assert rv["details"]["new_blocks_readiness"] is False
    # FDC-002 export limitation disclaimer present
    lim = " | ".join(obj["export_metadata"]["limitations"]).lower()
    assert "no verification performed by this lane" in lim


# 37 ------------------------ prohibited statuses absent + bounded scope preserved
def test_no_prohibited_status_and_bounded_scope_after_fdc002_ops():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION, "supportive",
                   RESOLVED, resolution_rationale="cleared")
    blob = rec.to_json().lower()
    for bad in PROHIBITED_STATUS_VALUES:
        assert bad not in blob
    # bounded FDC-001 scope preserved: three fixed candidates, fixed question
    assert len(rec.candidates) == 3
    assert rec.decision_question == dw.DECISION_QUESTION


# 38 ----------------------------- no persistence coupling (static, behavioral)
def test_no_persistence_coupling_and_no_ui_bypass():
    import re
    src = inspect.getsource(dw)
    # No ACTUAL persistence import (the module docstring may mention the name in
    # a "does NOT import" disclaimer; only a real import statement is forbidden).
    assert not re.search(r"^\s*(from|import)\s+\S*session_store", src, re.M)
    # The web route layer exposes no user-facing path that clears the physical
    # blocker via the legacy domain methods: the only success path through
    # decision_workspace_gap_action for a physical gap is the 400 guard.
    web_src = inspect.getsource(__import__("web.app", fromlist=["app"]))
    assert "MISSING_PHYSICAL_OR_CALIBRATION_INFORMATION" in web_src
    assert "gap_blocker_code" in web_src


# === Code-review correction coverage (immutable records, normalization, =======
# === classifier completeness, atomicity, and specification-permitted rules) ===

# 39 ---------------------------- immutable evidence fields (behavioral)
def test_evidence_fields_are_immutable():
    from dataclasses import FrozenInstanceError
    rec = DecisionRecord()
    ev = _add_phys_evidence(rec)
    # to_record_dict is deterministic (no export timestamp); use it for stability.
    before = rec.to_record_dict()
    for field_name, val in [
            ("verification_status", "verified"), ("linked_gap_id", "gap-x"),
            ("text", "tampered"), ("claim_class", EXTERNAL_REFERENCE),
            ("provenance", DERIVED_BY_RULE), ("candidate_ids", ("c",)),
            ("decision_relevant", True)]:
        try:
            setattr(ev, field_name, val)
            assert False, "mutated immutable evidence field %s" % field_name
        except FrozenInstanceError:
            pass
    assert rec.to_record_dict() == before
    assert ev.verification_status == "unverified"


# 40 ---------------------------- immutable assessment fields (behavioral)
def test_assessment_fields_are_immutable():
    from dataclasses import FrozenInstanceError
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    ga = rec.assess_gap(g.gap_id, [ev.evidence_id], PARTIALLY_ADDRESSES,
                        "review", REMAINS_BLOCKING)
    before = rec.to_record_dict()
    for field_name, val in [
            ("resolution_decision", RESOLVED), ("evidence_ids", ("x",)),
            ("assessment", SUPPORTS_RESOLUTION), ("gap_id", "gap-x"),
            ("rationale", "tampered")]:
        try:
            setattr(ga, field_name, val)
            assert False, "mutated immutable assessment field %s" % field_name
        except FrozenInstanceError:
            pass
    assert rec.to_record_dict() == before


# 41 ---------------------------- immutable nested id collections (behavioral)
def test_nested_id_collections_are_immutable():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    cid = rec.candidates[0].candidate_id
    ev = rec.add_evidence(g.gap_id, "bench", OPERATOR_REPORTED_RESULT,
                          OPERATOR_ENTERED, candidate_ids=[cid])
    ga = rec.assess_gap(g.gap_id, [ev.evidence_id], PARTIALLY_ADDRESSES,
                        "review", REMAINS_BLOCKING)
    # stored as immutable tuples; no in-place mutation possible
    assert isinstance(ev.candidate_ids, tuple)
    assert isinstance(ga.evidence_ids, tuple)
    for coll in (ev.candidate_ids, ga.evidence_ids):
        assert not hasattr(coll, "append")
        try:
            coll[0] = "hacked"
            assert False, "tuple element assignment must fail"
        except TypeError:
            pass
    # mutating an exported list does NOT affect stored state (independent copy)
    d = ev.to_dict()
    d["candidate_ids"].append("injected")
    assert "injected" not in ev.candidate_ids
    assert ev.to_dict()["candidate_ids"] == [cid]
    d2 = ga.to_dict()
    d2["evidence_ids"].append("injected")
    assert "injected" not in ga.evidence_ids


# 42 ---------------------------- exports stable after attempted mutation
def test_exports_stable_after_attempted_mutation():
    from dataclasses import FrozenInstanceError
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION, "supportive",
                   RESOLVED, resolution_rationale="cleared")
    snap = rec.to_record_dict()  # deterministic (no export timestamp)
    for obj, field_name, val in [
            (rec.evidence[0], "verification_status", "verified"),
            (rec.evidence[0], "text", "x"),
            (rec.gap_assessments[0], "resolution_decision", REMAINS_BLOCKING)]:
        try:
            setattr(obj, field_name, val)
            assert False
        except FrozenInstanceError:
            pass
    # mutating exported JSON structures in place must not feed back into storage
    parsed = json.loads(rec.to_json())
    parsed["evidence"][0]["verification_status"] = "verified"
    parsed["evidence"][0]["candidate_ids"].append("x")
    assert rec.to_record_dict() == snap


# 43 ---------------------------- evidence text stripped + must be text
def test_evidence_text_is_stripped_and_must_be_text():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = rec.add_evidence(g.gap_id, "   bench result   ",
                          OPERATOR_REPORTED_RESULT, OPERATOR_ENTERED)
    assert ev.text == "bench result"
    assert json.loads(rec.to_json())["evidence"][0]["text"] == "bench result"
    # non-text input rejected before mutation (no silent stringify)
    before = _snapshot(rec)
    try:
        rec.add_evidence(g.gap_id, 12345, OPERATOR_REPORTED_RESULT, OPERATOR_ENTERED)
        assert False, "non-text evidence value must be rejected"
    except DecisionError:
        pass
    assert _snapshot(rec)["evidence"] == before["evidence"]
    assert _snapshot(rec)["hist"] == before["hist"]


# 44 ---------------------------- duplicate evidence ids in one assessment
def test_duplicate_evidence_ids_in_assessment_rejected():
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    before = _snapshot(rec)
    try:
        rec.assess_gap(g.gap_id, [ev.evidence_id, ev.evidence_id],
                       SUPPORTS_RESOLUTION, "r", REMAINS_BLOCKING)
        assert False, "duplicate evidence id must be rejected"
    except DecisionError:
        pass
    assert rec.gap_assessments == []
    assert _snapshot(rec)["hist"] == before["hist"]
    assert g.blocks_readiness is True


# 45 ---------------------------- seeded-gap classification completeness
def test_seeded_gap_classification_completeness_and_guard_consistency():
    rec = DecisionRecord()
    codes = {rec.gap_blocker_code(g.gap_id) for g in rec.gaps}
    assert codes == {dw.MISSING_FALSE_POSITIVE_TOLERANCE,
                     MISSING_PHYSICAL_OR_CALIBRATION_INFORMATION}
    phys = [g for g in rec.gaps
            if rec.gap_blocker_code(g.gap_id)
            == MISSING_PHYSICAL_OR_CALIBRATION_INFORMATION]
    fp = [g for g in rec.gaps
          if rec.gap_blocker_code(g.gap_id) == dw.MISSING_FALSE_POSITIVE_TOLERANCE]
    assert len(phys) == 1 and len(fp) == 1  # exhaustive, no fallback reached
    # guard/readiness consistency: every blocking gap's gap_blocker_code equals
    # the code that surfaces as its blocking_reason (one shared classifier).
    reason_code_by_text = {b.text: b.code for b in rec.blocking_reasons}
    for g in rec.gaps:
        if g.blocks_readiness:
            assert rec.gap_blocker_code(g.gap_id) == reason_code_by_text[g.text]


# 46 ---------------------------- non-physical seeded gap not caught by guard
def test_nonphysical_seeded_gap_not_classified_physical():
    rec = DecisionRecord()
    npg = _nonphysical_gap(rec)
    assert rec.gap_blocker_code(npg.gap_id) \
        != MISSING_PHYSICAL_OR_CALIBRATION_INFORMATION


# 47 ----- spec-permitted: decision_relevant=false evidence MAY clear a gap
def test_decision_relevant_false_evidence_may_clear_gap():
    # §7.2 resolution gate = supports_resolution + >=1 valid linked evidence; §7.3
    # keeps relevance distinct from resolution; decision_relevant is NOT a gate.
    rec = DecisionRecord()
    _make_comparable(rec)
    g = _physical_gap(rec)
    ev = rec.add_evidence(g.gap_id, "bench result", OPERATOR_REPORTED_RESULT,
                          OPERATOR_ENTERED, decision_relevant=False)
    assert ev.decision_relevant is False
    rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION, "supportive",
                   RESOLVED, resolution_rationale="owner accepts")
    assert g.blocks_readiness is False


# 48 ----- spec-permitted: empty candidate scope evidence MAY clear a gap
def test_empty_candidate_scope_evidence_may_clear_gap():
    # §7.1 candidate_ids optional; §12 item 4 lists "decision-scoped evidence
    # (no candidate)" as a valid case; resolution gate does not reference scope.
    rec = DecisionRecord()
    _make_comparable(rec)
    g = _physical_gap(rec)
    ev = rec.add_evidence(g.gap_id, "bench result", OPERATOR_REPORTED_RESULT,
                          OPERATOR_ENTERED, candidate_ids=[])
    assert tuple(ev.candidate_ids) == ()
    rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION, "supportive",
                   RECLASSIFIED_NONBLOCKING,
                   resolution_rationale="owner reclassifies")
    assert g.blocks_readiness is False


# 49 ----- spec-permitted: candidate-scoped (known id) evidence MAY clear a gap
def test_candidate_scoped_evidence_may_clear_gap():
    rec = DecisionRecord()
    _make_comparable(rec)
    g = _physical_gap(rec)
    cid = rec.candidates[0].candidate_id
    ev = rec.add_evidence(g.gap_id, "bench result", OPERATOR_REPORTED_RESULT,
                          OPERATOR_ENTERED, candidate_ids=[cid])
    assert cid in ev.candidate_ids
    rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION, "supportive",
                   RESOLVED, resolution_rationale="owner accepts")
    assert g.blocks_readiness is False


# 50 ----- spec-permitted: evidence MAY be added to an already non-blocking gap
def test_evidence_may_be_added_to_already_nonblocking_gap():
    # §7.1 linked_gap_id requires only an EXISTING gap (need not be blocking).
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION, "supportive",
                   RESOLVED, resolution_rationale="cleared")
    assert g.blocks_readiness is False
    ev2 = rec.add_evidence(g.gap_id, "follow-up note", OPERATOR_REPORTED_RESULT,
                           OPERATOR_ENTERED)
    assert ev2 in rec.evidence
    assert ev2.linked_gap_id == g.gap_id


# 51 ----- spec-permitted: same evidence MAY appear in multiple assessments
def test_same_evidence_may_appear_in_multiple_assessments():
    # The spec imposes no cross-assessment uniqueness; evidence linked to a gap
    # may back more than one assessment (e.g. successive remains_blocking reviews).
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    a1 = rec.assess_gap(g.gap_id, [ev.evidence_id], PARTIALLY_ADDRESSES,
                        "first review", REMAINS_BLOCKING)
    a2 = rec.assess_gap(g.gap_id, [ev.evidence_id], INSUFFICIENT,
                        "second review", REMAINS_BLOCKING)
    assert a1 in rec.gap_assessments and a2 in rec.gap_assessments
    assert ev.evidence_id in a1.evidence_ids and ev.evidence_id in a2.evidence_ids
    assert g.blocks_readiness is True


# 52 --- confirmed distinction: resolved & reclassified leave the gap PRESENT
def test_resolved_and_reclassified_leave_gap_present_but_nonblocking():
    # FDC-002 resolution does NOT remove the gap (unlike legacy resolve_gap); it
    # sets blocks_readiness False and the gap record remains (§9.6).
    rec = DecisionRecord()
    g = _physical_gap(rec)
    ev = _add_phys_evidence(rec)
    rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION, "supportive",
                   RESOLVED, resolution_rationale="cleared")
    assert any(x.gap_id == g.gap_id for x in rec.gaps)  # still present
    assert g.blocks_readiness is False
    rec2 = DecisionRecord()
    _make_comparable(rec2)
    g2 = _physical_gap(rec2)
    ev2 = _add_phys_evidence(rec2)
    rec2.assess_gap(g2.gap_id, [ev2.evidence_id], SUPPORTS_RESOLUTION,
                    "supportive", RECLASSIFIED_NONBLOCKING,
                    resolution_rationale="reclassified")
    assert any(x.gap_id == g2.gap_id for x in rec2.gaps)  # still present
    assert g2.blocks_readiness is False
    assert g2.reclassification_rationale == "reclassified"


# 53 ---------------------------- atomicity + recompute consistency proof
def test_record_atomicity_and_recompute_consistency():
    # _record -> _compute_readiness reads only validated lists (and swallows the
    # owner-preference lookup's DecisionError), so it cannot throw for validated
    # inputs: each successful op advances revision+history by exactly one and
    # leaves readiness equal to a fresh deterministic recompute.
    rec = DecisionRecord()
    _make_comparable(rec)
    g = _physical_gap(rec)
    r0 = (rec.revision, len(rec.history))
    ev = _add_phys_evidence(rec)
    assert (rec.revision, len(rec.history)) == (r0[0] + 1, r0[1] + 1)
    assert rec._compute_readiness() == rec.readiness_status
    r1 = (rec.revision, len(rec.history))
    rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION, "supportive",
                   RESOLVED, resolution_rationale="cleared")
    assert (rec.revision, len(rec.history)) == (r1[0] + 1, r1[1] + 1)
    assert rec._compute_readiness() == rec.readiness_status
    # a subsequent failing op leaves a full-state snapshot identical (atomic)
    before = _snapshot(rec)
    try:
        rec.assess_gap(g.gap_id, [ev.evidence_id], SUPPORTS_RESOLUTION, "again",
                       RESOLVED, resolution_rationale="again")
        assert False
    except DecisionError:
        pass
    assert _snapshot(rec) == before


# 54 ---- class-level immutability: EvidenceItem constructed directly with a list
def test_evidence_item_direct_construction_is_immutable():
    from dataclasses import FrozenInstanceError
    from engine.decision_workspace import EvidenceItem
    caller_list = ["candidate-1", "candidate-2"]
    ev = EvidenceItem("ev-x", "gap-x", "observation", OPERATOR_REPORTED_RESULT,
                      OPERATOR_ENTERED, candidate_ids=caller_list)
    # (1) the stored field is a tuple, not the caller's list
    assert isinstance(ev.candidate_ids, tuple)
    assert ev.candidate_ids == ("candidate-1", "candidate-2")
    # (2) mutating the original caller-owned list does NOT alter the record
    caller_list.append("injected")
    caller_list[0] = "tampered"
    assert ev.candidate_ids == ("candidate-1", "candidate-2")
    # (3) the stored nested collection has no append; (4) item assignment fails
    assert not hasattr(ev.candidate_ids, "append")
    try:
        ev.candidate_ids[0] = "hacked"
        assert False, "tuple element assignment must fail"
    except TypeError:
        pass
    # the frozen field itself also cannot be reassigned
    try:
        ev.candidate_ids = ("z",)
        assert False
    except FrozenInstanceError:
        pass
    # (5) exported value is a JSON list; (6) export stable after input mutation
    exported = ev.to_dict()["candidate_ids"]
    assert exported == ["candidate-1", "candidate-2"]
    assert isinstance(exported, list)
    exported.append("injected")  # mutate the export copy
    assert ev.to_dict()["candidate_ids"] == ["candidate-1", "candidate-2"]
    # (7) permanent-unverified enforcement still rejects direct construction
    try:
        EvidenceItem("ev-y", "gap-x", "obs", OPERATOR_REPORTED_RESULT,
                     OPERATOR_ENTERED, verification_status="verified")
        assert False, "non-unverified verification_status must be rejected"
    except DecisionError:
        pass
    # non-string candidate id member rejected (no silent stringify)
    try:
        EvidenceItem("ev-z", "gap-x", "obs", OPERATOR_REPORTED_RESULT,
                     OPERATOR_ENTERED, candidate_ids=[123])
        assert False, "non-string candidate id must be rejected"
    except DecisionError:
        pass


# 55 -- class-level immutability: GapAssessment constructed directly with a list
def test_gap_assessment_direct_construction_is_immutable():
    from dataclasses import FrozenInstanceError
    from engine.decision_workspace import GapAssessment
    caller_list = ["evidence-1", "evidence-2"]
    ga = GapAssessment("ga-x", "gap-x", caller_list, SUPPORTS_RESOLUTION,
                       "rationale", REMAINS_BLOCKING)
    # (1) stored as a tuple, independent of the caller's list
    assert isinstance(ga.evidence_ids, tuple)
    assert ga.evidence_ids == ("evidence-1", "evidence-2")
    # (2) mutating the original list does not alter the record
    caller_list.append("injected")
    caller_list[0] = "tampered"
    assert ga.evidence_ids == ("evidence-1", "evidence-2")
    # (3) no append; (4) item assignment fails
    assert not hasattr(ga.evidence_ids, "append")
    try:
        ga.evidence_ids[0] = "hacked"
        assert False, "tuple element assignment must fail"
    except TypeError:
        pass
    try:
        ga.evidence_ids = ("z",)
        assert False
    except FrozenInstanceError:
        pass
    # (5) exported as a JSON list; (6) export stable after input mutation
    exported = ga.to_dict()["evidence_ids"]
    assert exported == ["evidence-1", "evidence-2"]
    assert isinstance(exported, list)
    exported.append("injected")
    assert ga.to_dict()["evidence_ids"] == ["evidence-1", "evidence-2"]
    # non-string evidence id member rejected (no silent stringify)
    try:
        GapAssessment("ga-y", "gap-x", [object()], SUPPORTS_RESOLUTION, "r",
                      REMAINS_BLOCKING)
        assert False, "non-string evidence id must be rejected"
    except DecisionError:
        pass
