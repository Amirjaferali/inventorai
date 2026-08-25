"""W2-A / RVR-4 — OW-6 downstream containment (frozen contract §10).

One explicit test per consumer: decision-action records never become
requirements, gap answers, gap evidence, deliverable claims, or legacy
assertions anywhere downstream. Consumer #1 (`requirement_landscape`) is the
PRIMARY containment point (repository truth: no disposition inclusion gate);
#3 (`validation_plan`) and #4 (`deliverable_assembler`) inherit through it and
are NOT directly modified.
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.idea_state import (
    IdeaState, Gap, OPEN, PHYSICAL_FEASIBILITY, DISPOSITION_ANSWERED,
    DECISION_ACTION_DISPOSITIONS,
)
from engine.decision_composition import (
    declare_decision_context, declare_alternative, withdraw_alternative,
)
from engine.requirement_landscape import derive_requirement_landscape
from engine.validation_plan import derive_validation_plan
from engine.deliverable_assembler import assemble_deliverable
from engine.derived_readiness import derive_readiness
from engine.progression_loop import substantive_attempt_recorded
from engine.record_contract import ProjectRecordContract
from engine.read_export_service import _compose_export


ANSWER = ("The ramp is held flat by a toggle latch that snaps over its center "
          "and is checked by the operator before each use.")


def _mixed_state():
    """Legacy answered record + open gap + a full decision-action family."""
    s = IdeaState(idea_id="pid-1")
    s.gaps.append(Gap(gap_type=PHYSICAL_FEASIBILITY, status=OPEN, opened_at=1))
    ans = s.record_interaction(action=DISPOSITION_ANSWERED, content=ANSWER,
                               gap_context=PHYSICAL_FEASIBILITY)
    ctx = declare_decision_context(s, "Which latch mechanism should hold it?")
    a1 = declare_alternative(s, "Toggle latch", ctx.record_id)
    a2 = declare_alternative(s, "Spring pin", ctx.record_id)
    withdraw_alternative(s, a2.record_id, "too fiddly")
    return s, ans, ctx, a1, a2


def _decision_ids(s):
    return {r.record_id for r in s.assertions
            if r.disposition in DECISION_ACTION_DISPOSITIONS}


# --- RVR4-OW6-1: requirement landscape (PRIMARY containment) -----------------

def test_ow6_1_no_decision_record_becomes_requirement_row():
    s, ans, *_ = _mixed_state()
    landscape = derive_requirement_landscape(s)
    anchors = {r.primary_anchor.anchor_reference
               for r in landscape.requirements}
    assert not (anchors & _decision_ids(s))
    # control (non-vacuity): the legacy answer IS a requirement row
    assert ans.record_id in anchors
    # and no decision content leaked into any statement
    for r in landscape.requirements:
        assert "Toggle latch" not in r.statement
        assert "Which latch mechanism" not in r.statement


# --- RVR4-OW6-2: derived readiness (gap-context level) -----------------------

def test_ow6_2_gap_context_readiness_unaffected():
    s, ans, *_ = _mixed_state()
    control = IdeaState(idea_id="pid-1")
    control.gaps.append(Gap(gap_type=PHYSICAL_FEASIBILITY, status=OPEN,
                            opened_at=1))
    control.assertions.append(ans)
    with_d = derive_readiness(s)
    without = derive_readiness(control)
    assert (with_d.is_verified(PHYSICAL_FEASIBILITY)
            == without.is_verified(PHYSICAL_FEASIBILITY))
    # decision records never enter any GAP context's active set
    assert all(r.record_id not in _decision_ids(s)
               for r in with_d._active(PHYSICAL_FEASIBILITY))


# --- RVR4-OW6-3: validation plan (inherits, untouched) -----------------------

def test_ow6_3_no_validation_step_anchors_a_decision_record():
    s, ans, *_ = _mixed_state()
    plan = derive_validation_plan(s)
    refs = {step.provenance.reference for step in plan.steps}
    refs |= {b.provenance.reference for b in plan.blocked_items}
    assert not (refs & _decision_ids(s))
    # control: the legacy answer produced a validation step
    assert any(ans.record_id == r for r in refs)


# --- RVR4-OW6-4: deliverable (inherits, untouched) ---------------------------

def test_ow6_4_deliverable_sections_contain_no_decision_claims():
    s, ans, *_ = _mixed_state()
    package = assemble_deliverable(s)
    import json
    s13 = json.dumps(package["section_13_requirement_landscape"])
    s14 = json.dumps(package["section_14_validation_plan"])
    for rid in _decision_ids(s):
        assert rid not in s13 and rid not in s14
    assert "Which latch mechanism" not in s13
    assert ANSWER[:40] in s13                       # control: legacy answer rendered


# --- RVR4-OW6-6: W2-D attempt gate -------------------------------------------

def test_ow6_6_decision_records_never_satisfy_attempt_gate():
    s = IdeaState(idea_id="pid-1")
    s.gaps.append(Gap(gap_type=PHYSICAL_FEASIBILITY, status=OPEN, opened_at=1))
    ctx = declare_decision_context(s, "Which latch mechanism should hold it?")
    declare_alternative(s, "Toggle latch stays engaged under load",
                        ctx.record_id)
    assert substantive_attempt_recorded(s, PHYSICAL_FEASIBILITY) is False
    # control: a PROVEN qualifying attempt (frozen Wave-1/W2-D fixture text)
    s.record_interaction(
        action=DISPOSITION_ANSWERED,
        content=("I have not tested whether the toggle latch stays reliable "
                 "under repeated loading and outdoor use."),
        gap_context=PHYSICAL_FEASIBILITY)
    assert substantive_attempt_recorded(s, PHYSICAL_FEASIBILITY) is True


# --- RVR4-OW6-7: contract restore is verbatim (no reclassification) ----------

def test_ow6_7_reconstruction_restores_decision_records_verbatim():
    s, ans, ctx, a1, a2 = _mixed_state()
    restored = ProjectRecordContract.from_dict(
        ProjectRecordContract.from_state(s).to_dict()).to_state()
    got = {r.record_id: r for r in restored.assertions}
    assert got[a1.record_id].disposition == a1.disposition
    assert got[a1.record_id].decision_context_root == ctx.record_id
    assert got[a2.record_id].superseded_by is not None   # withdrawal edge kept
    # nothing was re-labeled into a legacy class
    assert {got[r].disposition for r in _decision_ids(s)} \
        == {r.disposition for r in s.assertions
            if r.disposition in DECISION_ACTION_DISPOSITIONS}


# --- RVR4-OW6-8: P7-I1 development outputs -----------------------------------

def test_ow6_8_development_outputs_never_reference_decision_records():
    from engine.idea_development_outputs import derive_next_development_step
    s, ans, *_ = _mixed_state()
    step = derive_next_development_step(s)
    import dataclasses, json
    blob = json.dumps(dataclasses.asdict(step), default=str)
    for rid in _decision_ids(s):
        assert rid not in blob
    assert "Which latch mechanism" not in blob


# --- RVR4-OW6-9: P10-D3a export exposes truthfully, no relabel/expansion -----

def test_ow6_9_export_projection_truthful_and_not_expanded():
    s, *_ = _mixed_state()
    contract = ProjectRecordContract.from_state(s)
    export = _compose_export(contract, {"supported": True})
    by_id = {p["record_id"]: p for p in export["assertions"]}
    for rid in _decision_ids(s):
        assert by_id[rid]["disposition"] in DECISION_ACTION_DISPOSITIONS
        # the governed subset is NOT expanded (no export expansion in W2-A)
        assert set(by_id[rid]) == {"record_id", "disposition", "provenance",
                                   "validation_status"}
    assert export["assertion_count"] == len(s.assertions)
