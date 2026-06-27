"""
FDC001_FIRST_INCREMENT_ACCEPTANCE

Behavioral acceptance tests for the FDC-001 first increment (Technical Decision
Workspace). Maps to FDC-001 §14 acceptance criteria. Tests assert actual
behavior; static source inspection is used only for prohibitions that cannot be
observed behaviorally (e.g. confirming no persistence import).
"""

import os
import sys
import json
import inspect

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine import decision_workspace as dw
from engine.decision_workspace import (
    DecisionRecord, DecisionError,
    OWNER_REQUIREMENT, OBSERVED_FACT, OPERATOR_REPORTED_RESULT, ASSUMPTION,
    EXTERNAL_REFERENCE, MISSING_INFORMATION, CONSTRAINT,
    SEEDED_OWNER_CONTEXT, OPERATOR_ENTERED, DERIVED_BY_RULE,
    MANDATORY_CONSTRAINT, SOFT_CONSTRAINT, PREFERENCE,
    INSUFFICIENT_INFORMATION, BLOCKED_BY_EVIDENCE_GAP, COMPARISON_IN_PROGRESS,
    DECISION_READY_FOR_OWNER_REVIEW,
    INCOMPATIBLE_WITH_RECORDED_REQUIREMENT, DEFERRED_PENDING_INPUT,
    ELIMINATED, DEFERRED, BLOCKED, ACTIVE,
    OPERATOR_REPORTED_UNVERIFIED, EXTERNAL_REFERENCE_UNVERIFIED,
    PROHIBITED_STATUS_VALUES, REVIEW_REQUIRED_LABEL,
    CANDIDATE_NAMES, WIRED_BRAKE_LEVER_SWITCH,
    INPUT_ADDED, INPUT_UPDATED, INPUT_REMOVED, GAP_RESOLVED, GAP_RECLASSIFIED,
    CANDIDATE_STATUS_CHANGED, OWNER_PREFERENCE_SET, OWNER_PREFERENCE_CLEARED,
    CONSTRAINT_ADDED, UNEVALUABLE_MANDATORY_CONSTRAINT,
)
from web.app import app, FDC001_DECISIONS


# --- helpers -----------------------------------------------------------------
def _make_two_candidates_comparable(rec):
    """Give >=2 active candidates a decision_relevant input so minimum
    comparison context exists."""
    actives = [c for c in rec.candidates if c.option_status == ACTIVE]
    for c in actives[:2]:
        rec.add_input("relevant note for %s" % c.name, OBSERVED_FACT,
                      OPERATOR_ENTERED, decision_relevant=True,
                      candidate_ids=[c.candidate_id])
    return actives


def _clear_blocking_gaps(rec):
    for g in list(rec.gaps):
        if g.blocks_readiness:
            rec.resolve_gap(g.gap_id)


def _account_third_candidate(rec):
    actives = [c for c in rec.candidates if c.option_status == ACTIVE]
    covered = [c for c in actives if rec._covered(c)]
    for c in actives:
        if c not in covered[:2] and not rec._covered(c):
            rec.dispose_candidate(c.candidate_id, DEFERRED,
                                  "needs mounting/sensing inputs",
                                  DEFERRED_PENDING_INPUT)


# 1 -------------------------------------------------------------------- §14.5
def test_initial_state_insufficient_information():
    rec = DecisionRecord()
    # Pre-seeded gaps exist but must NOT force blocked_by_evidence_gap at open.
    assert any(g.blocks_readiness for g in rec.gaps)
    assert rec.readiness_status == INSUFFICIENT_INFORMATION
    assert len(rec.candidates) == 3


# 2 -------------------------------------------------------------------- §14.5
def test_readiness_ordered_table_transitions():
    rec = DecisionRecord()
    assert rec.readiness_status == INSUFFICIENT_INFORMATION
    # Establish minimum comparison context (2 candidates) while blocking gaps
    # still exist -> rule 2 fires (blocked_by_evidence_gap), not rule 1.
    _make_two_candidates_comparable(rec)
    assert rec.readiness_status == BLOCKED_BY_EVIDENCE_GAP
    # Remove blocking gaps -> rule 3 (comparison_in_progress) because the 3rd
    # candidate is not yet accounted for.
    _clear_blocking_gaps(rec)
    assert rec.readiness_status == COMPARISON_IN_PROGRESS
    # Account for the 3rd candidate -> rule 4 (ready).
    _account_third_candidate(rec)
    assert rec.readiness_status == DECISION_READY_FOR_OWNER_REVIEW
    # Determinism: identical recompute yields identical status.
    assert rec._compute_readiness() == DECISION_READY_FOR_OWNER_REVIEW


# 3 -------------------------------------------------------------------- §14.6
def test_all_three_candidates_required_for_ready():
    rec = DecisionRecord()
    _clear_blocking_gaps(rec)
    actives = _make_two_candidates_comparable(rec)
    # Two comparable, third active+uncovered -> not ready.
    assert rec.readiness_status == COMPARISON_IN_PROGRESS
    third = [c for c in rec.candidates if not rec._covered(c)][0]
    # Disposing the third with a valid basis makes it accounted for -> ready.
    rec.dispose_candidate(third.candidate_id, DEFERRED, "needs inputs",
                          DEFERRED_PENDING_INPUT)
    assert rec.readiness_status == DECISION_READY_FOR_OWNER_REVIEW


# 4 -------------------------------------------------------------------- §14.3
def test_claim_class_and_provenance_separate():
    rec = DecisionRecord()
    ci = rec.add_input("Owner wants no wire to the brake lever.",
                       OWNER_REQUIREMENT, OPERATOR_ENTERED)
    assert ci.claim_class == OWNER_REQUIREMENT
    assert ci.provenance == OPERATOR_ENTERED
    # Owner statements are never observed facts.
    assert ci.claim_class != OBSERVED_FACT
    # Seeded owner context is recorded as requirement/assumption, never fact.
    seeded = [i for i in rec.inputs if i.provenance == SEEDED_OWNER_CONTEXT]
    assert seeded and all(i.claim_class != OBSERVED_FACT for i in seeded)
    # provenance alone does not upgrade truth-status.
    op = rec.add_input("operator says calibration passed", OPERATOR_REPORTED_RESULT,
                       OPERATOR_ENTERED)
    assert op.display_label == OPERATOR_REPORTED_UNVERIFIED
    ext = rec.add_input("see datasheet", EXTERNAL_REFERENCE, OPERATOR_ENTERED,
                        source_label="vendor datasheet")
    assert ext.display_label == EXTERNAL_REFERENCE_UNVERIFIED


# 5 -------------------------------------------------------------------- §14.4
def test_missing_info_only_as_gap_not_evidence():
    rec = DecisionRecord()
    # Cannot store missing information as an input.
    try:
        rec.add_input("unknown false-positive rate", MISSING_INFORMATION,
                      OPERATOR_ENTERED)
        assert False, "missing_information must not be storable as an input"
    except DecisionError:
        pass
    # Missing info present only as gaps.
    assert all(i.claim_class != MISSING_INFORMATION for i in rec.inputs)
    assert len(rec.gaps) >= 1


# 6 -------------------------------------------------------------------- §14.7
def test_blocking_gap_reclassification_requires_rationale():
    rec = DecisionRecord()
    blocking = [g for g in rec.gaps if g.blocks_readiness][0]
    gid = blocking.gap_id
    prior_readiness = rec.readiness_status
    # No rationale -> rejected, with no mutation and no history event.
    try:
        rec.reclassify_gap(gid, "")
        assert False, "reclassification without rationale must be rejected"
    except DecisionError:
        pass
    assert rec._gap(gid).blocks_readiness is True
    assert not any(e.change_type == GAP_RECLASSIFIED for e in rec.history)

    rec.reclassify_gap(gid, "owner accepts this risk for the prototype stage")
    g = rec._gap(gid)
    assert g.blocks_readiness is False
    assert g.reclassification_rationale

    # The committed history event preserves BOTH the prior and the new blocking
    # state (not merely the final gap's rationale): gap id, previous/new
    # blocking value, rationale, revision, and prior/new readiness.
    evt = [e for e in rec.history if e.change_type == GAP_RECLASSIFIED][-1]
    assert evt.target_id == gid
    assert evt.details is not None
    assert evt.details["gap_id"] == gid
    assert evt.details["previous_blocks_readiness"] is True
    assert evt.details["new_blocks_readiness"] is False
    assert evt.details["rationale"]
    assert evt.revision == rec.revision
    assert evt.prior_readiness_status == prior_readiness
    assert evt.new_readiness_status == rec.readiness_status

    # Both states are recoverable from export, not only from the live object.
    exp = rec.to_export_dict()
    exported_gap = [x for x in exp["gaps"] if x["gap_id"] == gid][0]
    assert exported_gap["reclassification_rationale"]
    exported_evt = [e for e in exp["history"]
                    if e["change_type"] == GAP_RECLASSIFIED][-1]
    assert exported_evt["details"]["previous_blocks_readiness"] is True
    assert exported_evt["details"]["new_blocks_readiness"] is False
    assert exported_evt["details"]["rationale"]


# 7 -------------------------------------------------------------------- §14.9
def test_change_events_add_update_remove_resolve_revision():
    rec = DecisionRecord()
    r0 = rec.revision
    ci = rec.add_input("note", OBSERVED_FACT, OPERATOR_ENTERED)
    assert rec.revision == r0 + 1
    assert rec.history[-1].change_type == INPUT_ADDED
    rec.update_input(ci.claim_id, text="note v2")
    assert rec.revision == r0 + 2
    assert rec.history[-1].change_type == INPUT_UPDATED
    rec.remove_input(ci.claim_id)
    assert rec.revision == r0 + 3
    assert rec.history[-1].change_type == INPUT_REMOVED
    g = rec.gaps[0]
    rec.resolve_gap(g.gap_id)
    assert rec.revision == r0 + 4
    assert rec.history[-1].change_type == GAP_RESOLVED


# 8 -------------------------------------------------------------------- §14.9
def test_change_impact_summary_deterministic():
    rec = DecisionRecord()
    cand = rec.candidates[0]
    rec.add_input("x", OBSERVED_FACT, OPERATOR_ENTERED, decision_relevant=True,
                  candidate_ids=[cand.candidate_id])
    cis = rec.change_impact_summary.to_dict()
    for key in ("changed_item", "affected_candidates",
                "affected_gaps_or_blockers", "prior_readiness", "new_readiness"):
        assert key in cis
    assert cand.candidate_id in cis["affected_candidates"]
    assert cis["new_readiness"] == rec.readiness_status


# 9 -------------------------------------------------------------------- §14.13
def test_owner_preference_not_technical_selection():
    rec = DecisionRecord()
    cand = rec.candidates[1]
    rec.set_owner_preference(cand.candidate_id, "owner likes it")
    assert rec.history[-1].change_type == OWNER_PREFERENCE_SET
    # No candidate acquires a technical-selection status.
    for c in rec.candidates:
        assert c.option_status in (ACTIVE, ELIMINATED, DEFERRED, "blocked")
        assert c.option_status not in PROHIBITED_STATUS_VALUES
    blob = rec.to_json()
    assert "technically_selected" not in blob


# 10 ------------------------------------------------------------------- §14.2
def test_candidate_elimination_contextual_basis():
    rec = DecisionRecord()
    wired = [c for c in rec.candidates if c.name == WIRED_BRAKE_LEVER_SWITCH][0]
    rec.add_constraint("No wire to the brake lever.", MANDATORY_CONSTRAINT,
                       OPERATOR_ENTERED, confirmed=True,
                       candidate_ids=[wired.candidate_id])
    rec.eliminate_for_requirement(wired.candidate_id, "No wire to the brake lever.")
    w = rec._candidate(wired.candidate_id)
    assert w.option_status == ELIMINATED
    assert w.disposition_basis == INCOMPATIBLE_WITH_RECORDED_REQUIREMENT
    assert "technically_invalid" not in (w.disposition_basis or "")
    assert "technically_invalid" not in rec.to_json()


# 11 ------------------------------------------------------------------- §14.10/§14.14
def test_canonical_json_export_fields_and_single_timestamp():
    rec = DecisionRecord()
    obj = json.loads(rec.to_json())
    assert obj["schema_version"] == dw.SCHEMA_VERSION
    assert obj["export_metadata"]["export_format"] == "json"
    for key in ("decision_id", "decision_question", "revision", "candidates",
                "inputs", "constraints", "gaps", "readiness_status",
                "blocking_reasons", "history", "export_metadata"):
        assert key in obj, "missing export key %s" % key
    # Exactly one authoritative generated_at, inside export_metadata.
    assert "generated_at" in obj["export_metadata"]
    assert "generated_at" not in obj  # not duplicated at the record top level

    def _count(o):
        n = 0
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "generated_at":
                    n += 1
                n += _count(v)
        elif isinstance(o, list):
            for v in o:
                n += _count(v)
        return n
    assert _count(obj) == 1


# 12 ------------------------------------------------------------------- §14.10
def test_export_limitations_block():
    rec = DecisionRecord()
    obj = json.loads(rec.to_json())
    lim = " | ".join(obj["export_metadata"]["limitations"]).lower()
    assert "in-memory" in lim
    assert "restart restoration not supported" in lim
    assert "no benchmark run" in lim
    assert "no verified evidence" in lim
    assert "no final technical selection" in lim


# 13 ------------------------------------------------------------------- §14.11
def test_no_persistence_import_or_dependency():
    import re
    src = inspect.getsource(dw)
    # No import of the paused persistence module (a docstring mention is fine;
    # an import statement is not).
    assert not re.search(r"^\s*(from|import)\s+.*session_store", src, re.M)
    # No database or durable filesystem write APIs in the module.
    assert "sqlite3" not in src
    assert "open(" not in src
    assert ".save(" not in src
    # Importing the module must not pull in a persistence module.
    assert "engine.session_store" not in sys.modules


# 14 ------------------------------------------------------------------- §14.12
def test_no_fabricated_content():
    rec = DecisionRecord()
    # Seeded record invents no operator-reported physical result and no observed
    # fact; absent data is only ever a gap.
    assert all(i.claim_class != OPERATOR_REPORTED_RESULT for i in rec.inputs)
    assert all(i.claim_class != OBSERVED_FACT for i in rec.inputs)
    assert len(rec.gaps) >= 1


# 15 ------------------------------------------------------------------- §14.13
def test_no_prohibited_status_values():
    rec = DecisionRecord()
    _clear_blocking_gaps(rec)
    _make_two_candidates_comparable(rec)
    _account_third_candidate(rec)
    blob = rec.to_json()
    for bad in PROHIBITED_STATUS_VALUES:
        assert bad not in blob, "prohibited status %s leaked into export" % bad
    assert rec.readiness_status not in PROHIBITED_STATUS_VALUES


# 16 ------------------------------------------------------------------- §14.1/§14.2 (route)
def test_workspace_route_renders_three_candidates():
    client = app.test_client()
    resp = client.get("/decision-workspace", follow_redirects=True)
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    for name in CANDIDATE_NAMES:
        assert name in body
    assert "braking-detection architecture" in body
    # No candidate is declared the winner.
    assert "technically_selected" not in body
    assert "winner" not in body.lower()


# 17 ------------------------------------------------------------------- §14.10 (route/export)
def test_export_route_available_without_restart():
    client = app.test_client()
    start = client.get("/decision-workspace", follow_redirects=False)
    assert start.status_code == 302
    loc = start.headers["Location"]
    did = loc.rstrip("/").rsplit("/", 1)[-1]
    assert did in FDC001_DECISIONS
    exp = client.get("/decision-workspace/%s/export" % did)
    assert exp.status_code == 200
    assert exp.mimetype == "application/json"
    # Downloadable artifact: attachment disposition with a deterministic safe
    # filename tied to the decision id.
    cd = exp.headers.get("Content-Disposition", "")
    assert "attachment" in cd.lower()
    assert ("fdc001-decision-%s.json" % did) in cd
    assert did in cd
    obj = json.loads(exp.get_data(as_text=True))
    assert obj["decision_id"] == did
    assert "export_metadata" in obj
    assert obj["export_metadata"]["limitations"]


# 18 ------------------------------------------------------------------- §14.12 (no benchmark)
def test_no_benchmark_result_represented():
    rec = DecisionRecord()
    obj = json.loads(rec.to_json())
    blob = rec.to_json().lower()
    # No benchmark *result* representation (a "no benchmark run" limitation
    # disclaimer is allowed; a result/score is not).
    assert "weighted_score" not in blob
    assert "benchmark_result" not in blob
    assert "pass/fail" not in blob

    def _keys(o):
        ks = set()
        if isinstance(o, dict):
            for k, v in o.items():
                ks.add(k)
                ks |= _keys(v)
        elif isinstance(o, list):
            for v in o:
                ks |= _keys(v)
        return ks
    all_keys = _keys(obj)
    assert "score" not in all_keys
    assert "benchmark" not in all_keys
    # The only 'benchmark' mention is the limitations disclaimer.
    assert any("no benchmark run" in l.lower()
               for l in obj["export_metadata"]["limitations"])

    client = app.test_client()
    resp = client.get("/decision-workspace", follow_redirects=True)
    page = resp.get_data(as_text=True).lower()
    assert "benchmark result" not in page


# --- helpers for route tests -------------------------------------------------
def _start_decision(client):
    start = client.get("/decision-workspace", follow_redirects=False)
    assert start.status_code == 302
    did = start.headers["Location"].rstrip("/").rsplit("/", 1)[-1]
    return did, FDC001_DECISIONS[did]


# 19 ----------------------------------------------------- defect 1: atomicity
def test_invalid_candidate_disposition_is_atomic():
    rec = DecisionRecord()
    c = rec.candidates[0]
    # Snapshot the full relevant state.
    snap = (c.option_status, c.disposition_reason, c.disposition_basis)
    rev_before = rec.revision
    hist_before = len(rec.history)
    readiness_before = rec.readiness_status
    cis_before = rec.change_impact_summary

    # Provoke: a non-active disposition with no basis must raise BEFORE any
    # mutation of candidate.option_status.
    try:
        rec.dispose_candidate(c.candidate_id, ELIMINATED, "some reason", "")
        assert False, "missing disposition_basis must raise"
    except DecisionError:
        pass

    # Nothing changed: candidate, revision, history, readiness, change-impact.
    assert (c.option_status, c.disposition_reason, c.disposition_basis) == snap
    assert c.option_status == ACTIVE
    assert rec.revision == rev_before
    assert len(rec.history) == hist_before
    assert rec.readiness_status == readiness_before
    assert rec.change_impact_summary is cis_before

    # An unknown candidate id is likewise atomic (no partial state, no event).
    try:
        rec.dispose_candidate("cand-does-not-exist", ELIMINATED, "r", "b")
        assert False, "unknown candidate_id must raise"
    except DecisionError:
        pass
    assert rec.revision == rev_before
    assert len(rec.history) == hist_before


# 20 -------------------------------- defect 2: mandatory-constraint evaluability
def test_unevaluable_confirmed_mandatory_constraint_blocks_readiness():
    rec = DecisionRecord()
    _clear_blocking_gaps(rec)
    _make_two_candidates_comparable(rec)
    _account_third_candidate(rec)
    assert rec.readiness_status == DECISION_READY_FOR_OWNER_REVIEW
    # A confirmed mandatory constraint with no candidate scope cannot be
    # evaluated against the relevant candidate scope -> readiness stays blocked.
    rec.add_constraint(
        "A confirmed mandatory rule with no candidate scope.",
        MANDATORY_CONSTRAINT, OPERATOR_ENTERED, confirmed=True, candidate_ids=[])
    assert rec._mandatory_constraint_unevaluable() is True
    assert rec.readiness_status == BLOCKED_BY_EVIDENCE_GAP


# 21 -------------------------------- defect 2: no false block when evaluable
def test_evaluable_confirmed_mandatory_constraint_does_not_create_false_block():
    rec = DecisionRecord()
    _clear_blocking_gaps(rec)
    actives = _make_two_candidates_comparable(rec)
    _account_third_candidate(rec)
    assert rec.readiness_status == DECISION_READY_FOR_OWNER_REVIEW
    # A confirmed mandatory constraint scoped to a known candidate IS evaluable
    # and must NOT create a false block.
    scoped = actives[0].candidate_id
    rec.add_constraint("No wire to the brake lever.", MANDATORY_CONSTRAINT,
                       OPERATOR_ENTERED, confirmed=True, candidate_ids=[scoped])
    assert rec._mandatory_constraint_unevaluable() is False
    assert rec.readiness_status == DECISION_READY_FOR_OWNER_REVIEW


# 22 ------------------------------------------- defect 4: add-constraint route
def test_route_add_constraint_persists_and_exports():
    client = app.test_client()
    did, rec = _start_decision(client)
    cand = rec.candidates[0].candidate_id
    resp = client.post("/decision-workspace/%s/constraint" % did, data={
        "text": "Must fit within the existing handlebar enclosure.",
        "constraint_strength": "soft_constraint",
        "provenance": "operator_entered",
        "candidate_id": cand,
    }, follow_redirects=False)
    assert resp.status_code == 302
    assert any(c.text.startswith("Must fit") for c in rec.constraints)
    assert any(e.change_type == CONSTRAINT_ADDED for e in rec.history)
    exp = client.get("/decision-workspace/%s/export" % did)
    obj = json.loads(exp.get_data(as_text=True))
    assert any("handlebar" in c["text"] for c in obj["constraints"])


# 23 ----------------------------------- defect 4: gap resolve/reclassify routes
def test_route_gap_resolve_and_reclassify():
    client = app.test_client()
    did, rec = _start_decision(client)
    gids = [g.gap_id for g in rec.gaps]
    assert len(gids) >= 2
    r1 = client.post("/decision-workspace/%s/gap" % did, data={
        "action": "reclassify", "gap_id": gids[0],
        "rationale": "owner accepts for the prototype stage"})
    assert r1.status_code == 302
    assert rec._gap(gids[0]).blocks_readiness is False
    r2 = client.post("/decision-workspace/%s/gap" % did, data={
        "action": "resolve", "gap_id": gids[1]})
    assert r2.status_code == 302
    assert all(g.gap_id != gids[1] for g in rec.gaps)
    # The reclassification's prior/new blocking state survives into export.
    obj = json.loads(client.get(
        "/decision-workspace/%s/export" % did).get_data(as_text=True))
    evt = [e for e in obj["history"]
           if e["change_type"] == GAP_RECLASSIFIED][-1]
    assert evt["details"]["previous_blocks_readiness"] is True
    assert evt["details"]["new_blocks_readiness"] is False


# 24 ------------------------------- defect 4: owner-preference set/clear routes
def test_route_owner_preference_set_and_clear():
    client = app.test_client()
    did, rec = _start_decision(client)
    cand = rec.candidates[1].candidate_id
    rs = client.post("/decision-workspace/%s/preference" % did, data={
        "action": "set", "candidate_id": cand, "rationale": "owner likes it"})
    assert rs.status_code == 302
    assert rec.owner_preference is not None
    assert rec.owner_preference.candidate_id == cand
    assert rec.history[-1].change_type == OWNER_PREFERENCE_SET
    rc = client.post("/decision-workspace/%s/preference" % did, data={
        "action": "clear"})
    assert rc.status_code == 302
    assert rec.owner_preference is None
    assert rec.history[-1].change_type == OWNER_PREFERENCE_CLEARED


# 25 --------------------------------- defect 4: candidate-disposition route
def test_route_candidate_disposition():
    client = app.test_client()
    did, rec = _start_decision(client)
    cand = rec.candidates[2].candidate_id
    resp = client.post("/decision-workspace/%s/candidate" % did, data={
        "candidate_id": cand, "option_status": "deferred",
        "disposition_reason": "needs sensing inputs",
        "disposition_basis": "deferred_pending_input"})
    assert resp.status_code == 302
    c = rec._candidate(cand)
    assert c.option_status == DEFERRED
    assert c.disposition_basis == DEFERRED_PENDING_INPUT
    assert rec.history[-1].change_type == CANDIDATE_STATUS_CHANGED


# 26 -------------------------- defect 4: bounded error + no mutation on invalid
def test_route_invalid_mutation_shows_bounded_error_and_does_not_mutate():
    client = app.test_client()
    did, rec = _start_decision(client)
    rev_before = rec.revision
    hist_before = len(rec.history)
    status_before = rec.candidates[0].option_status
    # Invalid: non-active disposition with no basis.
    resp = client.post("/decision-workspace/%s/candidate" % did, data={
        "candidate_id": rec.candidates[0].candidate_id,
        "option_status": "eliminated",
        "disposition_reason": "x", "disposition_basis": ""})
    assert resp.status_code == 400
    body = resp.get_data(as_text=True)
    assert "rejected" in body.lower()
    assert "Traceback" not in body          # no traceback leaked
    # The record is unchanged.
    assert rec.revision == rev_before
    assert len(rec.history) == hist_before
    assert rec.candidates[0].option_status == status_before


# 27 ------------------------- defect 6: unknown candidate id rejected atomically
def test_unknown_candidate_id_rejected_without_mutation():
    rec = DecisionRecord()
    rev = rec.revision
    hist = len(rec.history)
    n_inputs = len(rec.inputs)
    n_constraints = len(rec.constraints)
    try:
        rec.add_input("note", OBSERVED_FACT, OPERATOR_ENTERED,
                      candidate_ids=["cand-nope"])
        assert False, "unknown candidate_id on input must raise"
    except DecisionError:
        pass
    try:
        rec.add_constraint("c", MANDATORY_CONSTRAINT, OPERATOR_ENTERED,
                           candidate_ids=["cand-nope"])
        assert False, "unknown candidate_id on constraint must raise"
    except DecisionError:
        pass
    assert len(rec.inputs) == n_inputs
    assert len(rec.constraints) == n_constraints
    assert rec.revision == rev
    assert len(rec.history) == hist


# 28 ----------------- defect 6: resolving nonexistent gap/conflict raises, no event
def test_resolving_nonexistent_gap_or_conflict_raises_and_no_event():
    rec = DecisionRecord()
    rev = rec.revision
    hist = len(rec.history)
    try:
        rec.resolve_gap("gap-nope")
        assert False, "resolving a nonexistent gap must raise"
    except DecisionError:
        pass
    try:
        rec.resolve_conflict("conflict-nope")
        assert False, "resolving a nonexistent conflict must raise"
    except DecisionError:
        pass
    assert rec.revision == rev
    assert len(rec.history) == hist


# 29 ----------------------------- defect 6: blank text rejected without mutation
def test_blank_text_rejected_without_mutation():
    rec = DecisionRecord()
    rev = rec.revision
    hist = len(rec.history)
    for call in (
        lambda: rec.add_input("   ", OBSERVED_FACT, OPERATOR_ENTERED),
        lambda: rec.add_constraint("", SOFT_CONSTRAINT, OPERATOR_ENTERED),
        lambda: rec.add_gap("   "),
    ):
        try:
            call()
            assert False, "blank text must be rejected"
        except DecisionError:
            pass
    assert rec.revision == rev
    assert len(rec.history) == hist


# 30 ----------------------- final defect 1: update_input atomicity + validation
def test_invalid_input_update_is_atomic():
    rec = DecisionRecord()
    known = rec.candidates[0].candidate_id
    ci = rec.add_input("original text", OBSERVED_FACT, OPERATOR_ENTERED,
                       decision_relevant=False, candidate_ids=[known])
    # Snapshot all input fields plus record state.
    snap = (ci.text, ci.decision_relevant, ci.confirmed, list(ci.candidate_ids))
    rev_before = rec.revision
    hist_before = len(rec.history)
    readiness_before = rec.readiness_status
    cis_before = rec.change_impact_summary

    # One valid proposed change (decision_relevant) + one invalid candidate id:
    # the whole update must be rejected with NO partial mutation.
    try:
        rec.update_input(ci.claim_id, decision_relevant=True,
                         candidate_ids=["cand-does-not-exist"])
        assert False, "invalid candidate_id must raise"
    except DecisionError:
        pass
    assert (ci.text, ci.decision_relevant, ci.confirmed,
            list(ci.candidate_ids)) == snap
    assert rec.revision == rev_before
    assert len(rec.history) == hist_before
    assert rec.readiness_status == readiness_before
    assert rec.change_impact_summary is cis_before

    # Blank replacement text is rejected without mutation.
    try:
        rec.update_input(ci.claim_id, text="   ")
        assert False, "blank replacement text must be rejected"
    except DecisionError:
        pass
    assert ci.text == snap[0]
    assert rec.revision == rev_before
    assert len(rec.history) == hist_before

    # A fully valid multi-field update succeeds with exactly one revision/event.
    other = rec.candidates[1].candidate_id
    rec.update_input(ci.claim_id, text="updated text", decision_relevant=True,
                     confirmed=True, candidate_ids=[other])
    assert ci.text == "updated text"
    assert ci.decision_relevant is True
    assert ci.confirmed is True
    assert ci.candidate_ids == [other]
    assert rec.revision == rev_before + 1
    assert len(rec.history) == hist_before + 1
    assert rec.history[-1].change_type == INPUT_UPDATED


# 31 ----------- final defect 2: explicit blocker for unevaluable mandatory constraint
def test_unevaluable_mandatory_constraint_has_explicit_blocking_reason():
    rec = DecisionRecord()
    con = rec.add_constraint(
        "Confirmed mandatory rule with no candidate scope.",
        MANDATORY_CONSTRAINT, OPERATOR_ENTERED, confirmed=True, candidate_ids=[])
    # Live record exposes exactly one explicit unevaluable-mandatory blocker
    # identifying the constraint, at decision scope, with a concise explanation.
    live = [b for b in rec.blocking_reasons
            if b.code == UNEVALUABLE_MANDATORY_CONSTRAINT]
    assert len(live) == 1
    assert live[0].affected_scope == "decision"
    assert live[0].affected_constraint_id == con.constraint_id
    assert live[0].text.strip()
    # The same blocker is present in canonical export.
    obj = json.loads(rec.to_json())
    exp = [b for b in obj["blocking_reasons"]
           if b["code"] == UNEVALUABLE_MANDATORY_CONSTRAINT]
    assert len(exp) == 1
    assert exp[0]["affected_scope"] == "decision"
    assert exp[0]["affected_constraint_id"] == con.constraint_id
    assert exp[0]["text"].strip()


# 32 --------- final defect 2: evaluable mandatory constraint emits no such blocker
def test_evaluable_mandatory_constraint_has_no_unevaluable_blocking_reason():
    rec = DecisionRecord()
    scoped = rec.candidates[0].candidate_id
    rec.add_constraint("No wire to the brake lever.", MANDATORY_CONSTRAINT,
                       OPERATOR_ENTERED, confirmed=True, candidate_ids=[scoped])
    # No unevaluable-mandatory blocker in the live record...
    assert all(b.code != UNEVALUABLE_MANDATORY_CONSTRAINT
               for b in rec.blocking_reasons)
    # ...nor in canonical export.
    obj = json.loads(rec.to_json())
    assert all(b["code"] != UNEVALUABLE_MANDATORY_CONSTRAINT
               for b in obj["blocking_reasons"])
