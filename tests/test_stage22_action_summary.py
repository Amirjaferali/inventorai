"""Stage 22 / CAP-05 + CAP-07 Slice 2 — the read-only, project-level
Actionable Decision Room Summary.

The summary composes the canonical Validation Plan (grouped ONLY by its own
responsibility tokens) and the existing next development step. It asks the
inventor nothing, writes nothing, ranks nothing, and links nothing to a
decision or alternative; Section 14 stays the detailed owner. A derivation that
cannot be trusted reads "unavailable", never empty.

Synthetic data only.
"""
import copy
import html
import re

import pytest

import engine.validation_plan as vp
from engine.decision_composition import (
    declare_alternative, declare_decision_context, decision_trace_view)
from engine.idea_development_outputs import derive_next_development_step
from engine.idea_state import (
    IdeaState, MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY,
    DISPOSITION_DECISION_CONTEXT_DECLARED)
from web.ui_text import UI_STRINGS, text
from tests.test_stage22_decision_trace import (  # noqa: F401  (fixture)
    client, _journey, _element, _spans, _visible, FORBIDDEN_EN, FORBIDDEN_AR,
    A2, REASON)

QUESTION = "Which latch mechanism should hold the ramp flat?"


def _summary(state):
    import web.app as webapp
    return webapp._decision_action_summary(state)


def _groups(summary):
    return {g["key"]: g for g in summary["groups"]}


def _live_state():
    """A live project with one decision and records of several kinds."""
    s = IdeaState(idea_id="as")
    s.domain = "mechanical"
    ctx = declare_decision_context(s, QUESTION).record_id
    declare_alternative(s, "Toggle latch", ctx)
    s.record_interaction("answered", "steel frame", gap_context=PHYSICAL_FEASIBILITY)
    s.record_interaction("answered", "folds flat", gap_context=MECHANISM_COMPLETENESS)
    s.record_interaction("specialist_requested", "", gap_context=PHYSICAL_FEASIBILITY)
    s.record_interaction("evidence_requested", "", gap_context=PHYSICAL_FEASIBILITY)
    s.record_interaction("unknown", "", gap_context=MECHANISM_COMPLETENESS)
    return s


def _step(statement, responsibility, n=1, label="Recorded answer"):
    return vp.ValidationStep(
        step_id=f"vstep:req:{n}", statement=statement, responsibility=responsibility,
        evidence_category="x", closure_condition="x",
        provenance=vp.ProvenanceRef("assertion", f"rec_{n}", label),
        confidence=vp.CONFIDENCE_UNDETERMINED)


def _blocked(label, n=1):
    return vp.BlockedValidationItem(
        item_id=f"vblock:req:{n}", reason="r", missing="m",
        responsibility=vp.UNDETERMINED,
        provenance=vp.ProvenanceRef("assertion", f"rec_{n}", label))


# ---------------------------------------------------------------------------
# composition over the canonical owner
# ---------------------------------------------------------------------------

def test_no_decision_derives_no_summary():
    s = IdeaState(idea_id="none")
    s.domain = "mechanical"
    s.record_interaction("answered", "x", gap_context=PHYSICAL_FEASIBILITY)
    assert _summary(s) is None


def test_b_n_every_step_lands_once_in_its_own_responsibility_group():
    s = _live_state()
    plan = vp.derive_validation_plan(s)
    summary = _summary(s)
    assert summary["status"] == "available"
    groups = _groups(summary)
    key_of = {"OWNER_EXECUTABLE": "owner", "SPECIALIST_REQUIRED": "specialist",
              "EMPIRICAL_EVIDENCE_REQUIRED": "evidence", "SYSTEM_DERIVABLE": "system",
              "UNDETERMINED": "clarification"}
    for step in plan.steps:
        entries = groups[key_of[step.responsibility]]["entries"]
        shown = (step.provenance.display_label + ": " + step.statement
                 if step.responsibility == vp.UNDETERMINED else step.statement)
        assert [e["text"] for e in entries].count(shown) == 1
    assert summary["total"] == len(plan.steps) + len(plan.blocked_items)
    assert sum(g["count"] for g in summary["groups"]) == summary["total"]
    # the realistic state yields owner, specialist, evidence and clarification
    assert {"owner", "specialist", "evidence", "clarification"} <= set(groups)
    assert [g["key"] for g in summary["groups"]] == [
        k for k in ("owner", "specialist", "evidence", "system", "clarification")
        if k in groups]


def test_c_g_categories_come_from_tokens_never_from_wording(monkeypatch):
    plan = vp.ValidationPlan(outcome=vp.OUTCOME_PLAN, steps=(
        _step("Ask a specialist to run an empirical test", vp.OWNER_EXECUTABLE, 1),
        _step("You can do this yourself", vp.SPECIALIST_REQUIRED, 2),
        _step("Compute the load path", vp.SYSTEM_DERIVABLE, 3),
        _step("Measure deflection", vp.EMPIRICAL_EVIDENCE_REQUIRED, 4),
    ), blocked_items=())
    monkeypatch.setattr(vp, "derive_validation_plan", lambda state: plan)
    groups = _groups(_summary(_live_state()))
    assert [e["text"] for e in groups["owner"]["entries"]] == [
        "Ask a specialist to run an empirical test"]
    assert [e["text"] for e in groups["specialist"]["entries"]] == ["You can do this yourself"]
    assert [e["text"] for e in groups["system"]["entries"]] == ["Compute the load path"]
    assert [e["text"] for e in groups["evidence"]["entries"]] == ["Measure deflection"]


def test_h_blocked_and_undetermined_items_are_kept_as_clarification(monkeypatch):
    plan = vp.ValidationPlan(outcome=vp.OUTCOME_PLAN, steps=(
        _step("Address the open gap: Physical Feasibility.", vp.UNDETERMINED, 1),
    ), blocked_items=(_blocked("Recorded unknown", 2),))
    monkeypatch.setattr(vp, "derive_validation_plan", lambda state: plan)
    groups = _groups(_summary(_live_state()))
    assert set(groups) == {"clarification"}
    assert [e["text"] for e in groups["clarification"]["entries"]] == [
        "Recorded answer: Address the open gap: Physical Feasibility.",
        "Recorded unknown"]
    assert groups["clarification"]["count"] == 2


GENERIC = "Validate, revise, or replace it before relying on it."


def test_correction_01_undetermined_step_carries_its_canonical_subject(monkeypatch):
    """A: outside Section 14 an UNDETERMINED step keeps its own canonical
    provenance label, verbatim, in front of its verbatim statement; C: the
    other responsibility groups keep the bare canonical statement."""
    plan = vp.ValidationPlan(outcome=vp.OUTCOME_PLAN, steps=(
        _step(GENERIC, vp.UNDETERMINED, 1, label="Provisional assumption"),
        _step("Obtain the requested specialist input.", vp.SPECIALIST_REQUIRED, 2,
              label="Pending specialist request"),
        _step("Confirm the frame", vp.OWNER_EXECUTABLE, 3),
    ), blocked_items=())
    monkeypatch.setattr(vp, "derive_validation_plan", lambda state: plan)
    groups = _groups(_summary(_live_state()))
    assert [e["text"] for e in groups["clarification"]["entries"]] == [
        "Provisional assumption: " + GENERIC]
    assert [e["text"] for e in groups["specialist"]["entries"]] == [
        "Obtain the requested specialist input."]
    assert [e["text"] for e in groups["owner"]["entries"]] == ["Confirm the frame"]


def test_correction_01_same_generic_statement_different_subjects_stay_apart(
        monkeypatch):
    """B: two UNDETERMINED steps with the same generic statement but different
    canonical subjects never collapse into one ambiguous entry; the same
    subject twice still collapses with its count."""
    plan = vp.ValidationPlan(outcome=vp.OUTCOME_PLAN, steps=(
        _step(GENERIC, vp.UNDETERMINED, 1, label="Provisional assumption"),
        _step(GENERIC, vp.UNDETERMINED, 2, label="Recorded unknown"),
        _step(GENERIC, vp.UNDETERMINED, 3, label="Provisional assumption"),
    ), blocked_items=())
    monkeypatch.setattr(vp, "derive_validation_plan", lambda state: plan)
    [group] = _summary(_live_state())["groups"]
    assert group["entries"] == [
        {"text": "Provisional assumption: " + GENERIC, "repeat": 2},
        {"text": "Recorded unknown: " + GENERIC, "repeat": 1}]
    assert group["count"] == 3


@pytest.mark.parametrize("label", [None, "", "   ", 7])
def test_correction_01_missing_subject_fails_closed(monkeypatch, label):
    """A referent-less UNDETERMINED statement is never rendered: a missing or
    malformed canonical label makes the whole summary unavailable."""
    plan = vp.ValidationPlan(outcome=vp.OUTCOME_PLAN, steps=(
        _step(GENERIC, vp.UNDETERMINED, 1, label=label),), blocked_items=())
    monkeypatch.setattr(vp, "derive_validation_plan", lambda state: plan)
    summary = _summary(_live_state())
    assert (summary["status"], summary["groups"], summary["total"]) == (
        "unavailable", [], None)


def test_correction_01_real_provisional_assumption_keeps_its_subject(client):
    """A (end to end): a real provisional assumption recorded through the
    carrier renders with its canonical subject on the served page; D: the
    summary still holds no control."""
    c, appmod = client
    sid = _project(c, appmod)
    state = appmod.SESSION_STORE[sid]["state"]
    state.record_interaction("provisional_assumption", "pin carries the load",
                             gap_context=PHYSICAL_FEASIBILITY)
    plan = vp.derive_validation_plan(state)
    [step] = [s for s in plan.steps if s.provenance.display_label
              == "Provisional assumption"]
    assert step.responsibility == vp.UNDETERMINED
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    _, _, block = _element(page, "decision-action-summary")
    assert html.escape("Provisional assumption: " + step.statement) in block
    _no_controls(block)


def test_n_identical_statements_collapse_with_a_count(monkeypatch):
    plan = vp.ValidationPlan(outcome=vp.OUTCOME_PLAN, steps=(
        _step("Obtain the requested specialist input.", vp.SPECIALIST_REQUIRED, 1),
        _step("Obtain the requested specialist input.", vp.SPECIALIST_REQUIRED, 2),
    ), blocked_items=())
    monkeypatch.setattr(vp, "derive_validation_plan", lambda state: plan)
    [group] = _summary(_live_state())["groups"]
    assert group["entries"] == [{"text": "Obtain the requested specialist input.",
                                 "repeat": 2}]
    assert group["count"] == 2


def test_empty_plan_is_available_and_empty_not_unavailable(monkeypatch):
    plan = vp.ValidationPlan(outcome=vp.OUTCOME_EMPTY, steps=(), blocked_items=())
    monkeypatch.setattr(vp, "derive_validation_plan", lambda state: plan)
    summary = _summary(_live_state())
    assert (summary["status"], summary["groups"], summary["total"]) == (
        "available", [], 0)


def test_i_derivation_failure_and_foreign_tokens_are_unavailable(monkeypatch):
    def boom(state):
        raise RuntimeError("plan failed")
    monkeypatch.setattr(vp, "derive_validation_plan", boom)
    summary = _summary(_live_state())
    assert (summary["status"], summary["groups"], summary["total"]) == (
        "unavailable", [], None)
    foreign = vp.ValidationPlan(outcome=vp.OUTCOME_PLAN, steps=(
        _step("x", "SOMEBODY_ELSE", 1),), blocked_items=())
    monkeypatch.setattr(vp, "derive_validation_plan", lambda state: foreign)
    assert _summary(_live_state())["status"] == "unavailable"


def test_j_cold_state_is_unavailable_never_a_false_zero():
    s = _live_state()
    s.domain = None
    summary = _summary(s)
    assert summary["status"] == "unavailable" and summary["total"] is None
    assert summary["next_step"]["status"] == "unavailable"


def test_k_next_step_is_the_existing_derivation_verbatim(monkeypatch):
    import web.app as webapp
    s = _live_state()
    step = derive_next_development_step(s)
    assert _summary(s)["next_step"] == {"status": "items", "title": step.title}

    def boom(state):
        raise RuntimeError("next step failed")
    monkeypatch.setattr(webapp, "derive_next_development_step", boom)
    summary = _summary(s)
    assert summary["next_step"]["status"] == "unavailable"
    assert summary["status"] == "available"


def test_r_s_summary_is_pure_and_leaves_the_trace_unchanged():
    s = _live_state()
    before, trace = copy.deepcopy(s.assertions), decision_trace_view(s)
    first = _summary(s)
    assert _summary(s) == first
    assert s.assertions == before
    assert decision_trace_view(s) == trace


def test_q_every_new_key_has_distinct_en_and_ar():
    keys = [k for k in UI_STRINGS if k.startswith("UI_AS_")]
    assert len(keys) >= 14
    for k in keys:
        en, ar = text(k, "en"), text(k, "ar")
        assert en.strip() and ar.strip() and en != ar, k
        assert re.search(r"[؀-ۿ]", ar), k


# ---------------------------------------------------------------------------
# rendered surfaces
# ---------------------------------------------------------------------------

def _answer(c, sid, value):
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    data = {"response": value, "action": "answered",
            "answer_token": html.unescape(re.search(
                r'name="answer_token" value="([^"]+)"', page).group(1))}
    target = re.search(r'name="answer_target" value="([^"]*)"', page)
    if target:
        data["answer_target"] = html.unescape(target.group(1))
    c.post(f"/session/{sid}", data=data)


def _project(c, appmod, lang="en"):
    sid = _journey(c, appmod, lang)
    _answer(c, sid, "The deck panel carries the load into two steel side rails.")
    return sid


EXTRA_FORBIDDEN = ("recommend", "best option", "you should choose", "test passed",
                   "is safe", "is ready", "prototype-ready", "feasible")


def _no_controls(fragment):
    for tag in ("<form", "<input", "<textarea", "<select", "<button"):
        assert tag not in fragment, tag


def _outside_decisions(page, element_id):
    start, _, _ = _element(page, element_id)
    for s0, e0 in (_spans(page, r'<div class="w2a-context"', "div")
                   + _spans(page, r'<li class="g3-alternative', "li")):
        assert not (s0 <= start < e0), "action summary inside a decision"


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_session_summary_is_read_only_project_level_and_navigable(client, lang):
    c, appmod = client
    sid = _project(c, appmod, lang)
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    _, _, block = _element(page, "decision-action-summary")
    _outside_decisions(page, "decision-action-summary")
    _no_controls(block)
    assert text("UI_AS_HEADING", lang) in block and text("UI_AS_NOTE", lang) in block
    assert 'data-as-group="owner"' in block
    assert text("UI_AS_GROUP_OWNER", lang) in block
    for token in ("OWNER_EXECUTABLE", "SPECIALIST_REQUIRED", "UNDETERMINED",
                  "vstep:", "vblock:", "req:"):
        assert token not in block, token
    hrefs = re.findall(r'href="([^"]*)"', block)
    assert f"/session/{sid}/deliverable#report-validation-plan" in hrefs
    for href in hrefs:
        if href.startswith("#"):
            assert f'id="{href[1:]}"' in page, href
    report = c.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert 'id="report-validation-plan"' in report
    words = _visible(block)
    for phrase in FORBIDDEN_EN + FORBIDDEN_AR + EXTRA_FORBIDDEN:
        assert phrase.lower() not in words, phrase
    # the Slice-1 trace still renders unchanged beside it
    assert html.escape(A2) in page and html.escape(REASON) in page


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_o_p_t_report_and_pdf_are_read_only_with_report_local_links(
        client, monkeypatch, lang):
    c, appmod = client
    sid = _project(c, appmod, lang)
    report = c.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    _, _, block = _element(report, "report-decision-action-summary")
    _outside_decisions(report, "report-decision-action-summary")
    _no_controls(block)
    assert "<details" not in block
    hrefs = re.findall(r'href="([^"]*)"', block)
    assert set(hrefs) <= {"#report-validation-plan", "#report-next-steps"} and hrefs
    for href in hrefs:
        assert f'id="{href[1:]}"' in report, href
    # Section 14 remains the detailed owner and still renders in full
    assert text("UI_B_DELIV_085", lang) in report
    seen = {}
    monkeypatch.setattr(appmod, "_render_pdf_bytes",
                        lambda source: seen.setdefault("source", source) and b"%PDF-")
    c.post(f"/session/{sid}/deliverable.pdf", data={})
    source = seen["source"]
    _, _, pdf_block = _element(source, "report-decision-action-summary")
    _no_controls(pdf_block)
    for href in re.findall(r'href="([^"]*)"', source):
        assert href.startswith("#") and f'id="{href[1:]}"' in source, href


def test_e_i_failure_renders_unavailable_not_empty(client, monkeypatch):
    c, appmod = client
    sid = _project(c, appmod)

    def boom(state):
        raise RuntimeError("plan failed")
    monkeypatch.setattr(vp, "derive_validation_plan", boom)
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    _, _, block = _element(page, "decision-action-summary")
    assert "data-as-unavailable" in block and "data-as-empty" not in block
    assert text("UI_AS_EMPTY", "en") not in block
    assert "plan failed" not in page


def test_j_cold_read_only_view_shows_unavailable(client):
    c, appmod = client
    sid = _project(c, appmod)
    appmod.SESSION_STORE.pop(sid)
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    _, _, block = _element(page, "decision-action-summary")
    assert "data-as-unavailable" in block and "data-as-empty" not in block
    assert 'data-as-next-status="unavailable"' in block
    assert html.escape(A2) in page   # the trace still renders
