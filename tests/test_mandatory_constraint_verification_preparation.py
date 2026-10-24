"""MANDATORY-CONSTRAINT-VERIFICATION-PREPARATION-01 — a current mandatory
project constraint yields ONE verification-preparation step in the existing
Validation Plan.

Proves, over the real engine and the real web routes:

* one current ``mandatory_constraint`` -> exactly one step, identified by the
  constraint's founding ledger record, quoting the CURRENT wording verbatim,
  with responsibility and confidence UNDETERMINED and no check, outcome,
  value or acceptance criterion invented;
* ``soft_constraint``, ``preference`` and withdrawn constraints yield nothing;
  a correction keeps the identity and shows only the current form;
* the steps follow every landscape-derived item, in declaration order;
* an unreadable or malformed constraint history yields ONE blocked item, never
  a silent absence; a ledger without constraint material is unchanged;
* constraints stay out of every Requirement Landscape row, and the Gap Action
  Packs, next development step, readiness and SafetySignal are unchanged;
* the report Section 14, the Decision Room action summary and the session note
  (EN / AR) carry it; the Stage 35 export stays v3 with no requirement row for
  it.

Neutral synthetic fixtures only; no study corpus.
"""
import copy
import html as _html

from engine import disclosure_export as dx
from engine.derived_readiness import derive_readiness
from engine.gap_action_pack import derive_gap_action_packs
from engine.idea_development_outputs import derive_next_development_step
from engine.idea_state import IdeaState, MECHANISM_COMPLETENESS
from engine.requirement_landscape import RequirementLandscape, derive_requirement_landscape
from engine.safety_signal import derive_inventor_stated_safety_signals as derive_safety_signals
from engine.validation_plan import (
    CONFIDENCE_UNDETERMINED, CONSTRAINT_ANCHOR_KIND, OUTCOME_BLOCKED, OUTCOME_PLAN,
    UNDETERMINED, derive_validation_plan,
)
from web import ui_text
import web.app as appmod
from tests.test_pathn_constraint_declaration import _post, _heads
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    client, MECH, _start, _answer, _live,
)

TEXT = "It must run on two AA batteries for a month"


def _ledger():
    s = IdeaState(idea_id="mcv")
    s.record_interaction("answered", "A spring latch locks the deck.",
                         gap_context=MECHANISM_COMPLETENESS)
    return s


def _constraint_steps(plan):
    return [st for st in plan.steps if st.provenance.anchor_kind == CONSTRAINT_ANCHOR_KIND]


# ===========================================================================
# 1. the step and its provenance
# ===========================================================================

def test_one_current_mandatory_constraint_yields_one_preparation_step():
    s = _ledger()
    d = s.record_constraint_action("declare", TEXT, "mandatory_constraint")
    plan = derive_validation_plan(s)
    [step] = _constraint_steps(plan)
    assert step.step_id == "vstep:constraint:" + d.record_id
    assert (step.provenance.reference, step.provenance.display_label) == (
        d.record_id, "Mandatory constraint you declared")
    assert "“" + TEXT + "”" in step.statement
    assert (step.responsibility, step.confidence) == (UNDETERMINED, CONFIDENCE_UNDETERMINED)
    assert step.interface_preparation == ()
    assert "evidence or specialist review" in step.evidence_category
    assert "does not verify the constraint or show that it can be met" in step.closure_condition
    assert "has not been checked" in step.statement
    assert plan.outcome == OUTCOME_PLAN and plan.blocked_items == ()


def test_no_value_outcome_or_acceptance_criterion_is_invented():
    s = _ledger()
    s.record_constraint_action("declare", "Quiet enough for a bedroom", "mandatory_constraint")
    [step] = _constraint_steps(derive_validation_plan(s))
    fixed = (step.statement.replace("Quiet enough for a bedroom", "")
             + step.evidence_category + step.closure_condition)
    assert not any(ch.isdigit() for ch in fixed)
    lowered = fixed.lower()
    for word in ("verified", "validated", "passed", "satisfied", "feasible",
                 "threshold", "acceptance criterion"):
        assert word not in lowered, word


def test_soft_constraints_preferences_and_withdrawn_constraints_yield_nothing():
    s = _ledger()
    s.record_constraint_action("declare", "Should fold flat", "soft_constraint")
    s.record_constraint_action("declare", "I would like a green case", "preference")
    m = s.record_constraint_action("declare", TEXT, "mandatory_constraint")
    s.record_constraint_action("withdraw", target_record_id=m.record_id)
    assert _constraint_steps(derive_validation_plan(s)) == []
    assert derive_validation_plan(s) == derive_validation_plan(_ledger())


def test_a_correction_keeps_the_identity_and_shows_only_the_current_form():
    s = _ledger()
    d = s.record_constraint_action("declare", TEXT, "mandatory_constraint")
    c = s.record_constraint_action("correct", TEXT + " or mains power", "mandatory_constraint",
                                   target_record_id=d.record_id)
    [step] = _constraint_steps(derive_validation_plan(s))
    assert step.step_id == "vstep:constraint:" + d.record_id
    assert "“" + TEXT + " or mains power”" in step.statement
    # mandatory -> soft removes it; soft -> mandatory brings back the same identity
    soft = s.record_constraint_action("correct", TEXT, "soft_constraint",
                                      target_record_id=c.record_id)
    assert _constraint_steps(derive_validation_plan(s)) == []
    s.record_constraint_action("correct", TEXT, "mandatory_constraint",
                               target_record_id=soft.record_id)
    [again] = _constraint_steps(derive_validation_plan(s))
    assert again.step_id == step.step_id and "“" + TEXT + "”" in again.statement


def test_steps_follow_the_landscape_in_declaration_order_once_each():
    s = _ledger()
    a = s.record_constraint_action("declare", "Must be under 2 kg", "mandatory_constraint")
    s.record_constraint_action("declare", "Nice if it is blue", "preference")
    b = s.record_constraint_action("declare", TEXT, "mandatory_constraint")
    plan = derive_validation_plan(s)
    landscape_ids = ["vstep:" + r.requirement_id
                     for r in derive_requirement_landscape(s).requirements]
    ids = [st.step_id for st in plan.steps]
    assert ids == landscape_ids + ["vstep:constraint:" + a.record_id,
                                   "vstep:constraint:" + b.record_id]
    assert len(set(ids)) == len(ids)
    assert derive_validation_plan(copy.deepcopy(s)) == plan


# ===========================================================================
# 2. degraded input and isolation
# ===========================================================================

def test_a_malformed_constraint_history_yields_one_blocked_item_not_an_absence():
    s = _ledger()
    s.record_constraint_action("declare", TEXT, "mandatory_constraint")
    s.assertions[-1].constraint_strength = "absolute"          # corrupt in memory
    plan = derive_validation_plan(s)
    assert _constraint_steps(plan) == []
    [item] = plan.blocked_items
    assert item.item_id == "vblock:constraint:unavailable"
    assert item.provenance.anchor_kind == CONSTRAINT_ANCHOR_KIND
    assert item.provenance.display_label == "Mandatory constraints you declared"
    assert item.responsibility == UNDETERMINED
    assert plan.outcome == OUTCOME_PLAN            # the landscape step still stands


def test_an_unreadable_history_blocks_rather_than_reading_as_empty(monkeypatch):
    import engine.validation_plan as vp

    def unreadable(_records):
        raise RuntimeError("unreadable")

    s = _ledger()
    s.record_constraint_action("declare", TEXT, "mandatory_constraint")
    monkeypatch.setattr(vp, "constraint_history", unreadable)
    plan = derive_validation_plan(s)
    assert _constraint_steps(plan) == []
    assert [b.item_id for b in plan.blocked_items] == ["vblock:constraint:unavailable"]
    # with no landscape step left, the outcome is BLOCKED, never EMPTY
    monkeypatch.setattr(vp, "derive_requirement_landscape",
                        lambda _state: RequirementLandscape(requirements=(), risks=()))
    assert derive_validation_plan(s).outcome == OUTCOME_BLOCKED


def test_constraints_stay_out_of_the_landscape_and_other_consumers():
    base = _ledger()
    s = copy.deepcopy(base)
    s.record_constraint_action("declare", TEXT, "mandatory_constraint")

    def view(state):
        return ([r.requirement_id for r in derive_requirement_landscape(state).requirements],
                repr(derive_next_development_step(state)),
                derive_readiness(state).overall_verified(),
                repr(derive_safety_signals(state)),
                repr(derive_gap_action_packs(state)))

    assert view(s) == view(base)
    # only the Validation Plan gains the one step
    assert derive_validation_plan(s).steps[:-1] == derive_validation_plan(base).steps


# ===========================================================================
# 3. consumers: Decision Room, report, session note, Stage 35 export
# ===========================================================================

def test_the_decision_room_summary_lists_it_under_its_own_label():
    from engine.decision_composition import declare_decision_context
    s = _ledger()
    s.domain = "mechanical"
    declare_decision_context(s, "Which latch design should hold?")
    s.record_constraint_action("declare", TEXT, "mandatory_constraint")
    summary = appmod._decision_action_summary(s)
    assert summary["status"] == appmod.AS_AVAILABLE
    entries = [e["text"] for g in summary["groups"] for e in g["entries"]]
    assert any(e.startswith("Mandatory constraint you declared: Prepare how your "
                            "mandatory constraint “" + TEXT + "”") for e in entries)


def test_report_session_note_and_export_through_the_routes(client):
    sid = _start(client)
    _answer(client, sid, MECH)
    _post(client, sid, constraint_action="declare", constraint_text=TEXT,
          constraint_strength="mandatory_constraint")
    _post(client, sid, constraint_action="declare", constraint_text="Nice if it is blue",
          constraint_strength="preference")
    [mandatory, _pref] = _heads(sid)
    report = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    plan_block = report[report.index("vp-intro"):]
    assert _html.escape("“" + TEXT + "”", quote=False) in plan_block
    assert "Nice if it is blue" not in plan_block.split('id="project-constraints-report"')[0]
    session = client.get(f"/session/{sid}").get_data(as_text=True)
    assert _html.escape(ui_text.text("UI_PCN_PLAN_NOTE", "en"), quote=False) in session
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    session_ar = client.get(f"/session/{sid}").get_data(as_text=True)
    assert _html.escape(ui_text.text("UI_PCN_PLAN_NOTE", "ar"), quote=False) in session_ar
    assert 'dir="rtl"' in session_ar
    # the canonical plan of the live state carries exactly this one constraint step
    [step] = _constraint_steps(derive_validation_plan(_live(sid)))
    assert step.step_id == "vstep:constraint:" + mandatory.record_id


def test_the_stage35_export_stays_v3_with_no_requirement_row_for_it():
    from tests.test_stage35_disclosure_projection import _rich_sources
    sources = _rich_sources()
    sources.state.record_constraint_action("declare", TEXT, "mandatory_constraint")
    content = dx.compose_projection(sources)
    doc = dx.export_document(content, "2026-10-24T00:00:00Z", dx.JSON_FORMAT_VERSION)
    assert dx.JSON_FORMAT_VERSION.endswith("/3")
    text = repr(doc)
    assert "vstep:" not in text and "Prepare how your mandatory constraint" not in text
    assert text.count(TEXT) == 1                     # field 30 only
