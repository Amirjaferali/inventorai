"""CONSTRAINT-ACCEPTANCE-TO-VALIDATION-PLAN-01 — the inventor's acceptance notes beside their constraint step.

The notes recorded for a mandatory constraint (MANDATORY-CONSTRAINT-ACCEPTANCE-PREPARATION-01, PR #873) are shown
beside that constraint's existing Validation Plan step (MANDATORY-CONSTRAINT-VERIFICATION-PREPARATION-01, PR #857),
in Section 14 of the HTML report and the PDF alike (Owner Option B). What is pinned:
  * plan owner (``engine/validation_plan.py``): ``ValidationStep.constraint_acceptance`` — ``None`` when no carrier is
    attached; RECORDED (current-version notes verbatim, with what is not recorded yet), NONE_RECORDED,
    EARLIER_VERSION (earlier statements, counted as recorded for nothing) or UNAVAILABLE (unreadable or inconsistent,
    never "not recorded"); the notes are validated whole against the state's own ledger by the constraint owner;
  * every other field of every step, the blocked items, the outcome, the canonical package and the Stage 35 export
    are unchanged;
  * web: ONE attachment at the shared deliverable seam through the existing reader; HTML / PDF parity in EN / AR.
"""
import html as _html
import re

import pytest

import web.app as appmod
from engine.deliverable_assembler import assemble_deliverable
from engine.idea_state import (
    CONSTRAINT_ACCEPTANCE_CRITERION as CRIT, CONSTRAINT_ACCEPTANCE_EVIDENCE as EVID,
    CONSTRAINT_ACCEPTANCE_UNREADABLE, ConstraintAcceptancePreparation as Prep, IdeaState, MECHANISM_COMPLETENESS,
)
from engine.validation_plan import (
    CONSTRAINT_ACCEPTANCE_EARLIER, CONSTRAINT_ACCEPTANCE_NONE, CONSTRAINT_ACCEPTANCE_RECORDED,
    CONSTRAINT_ACCEPTANCE_UNAVAILABLE, CONSTRAINT_ANCHOR_KIND, ConstraintAcceptanceView, derive_validation_plan,
)
from tests.test_mandatory_constraint_acceptance_preparation import (  # noqa: F401
    MECH, TEXT, _answer, _correct, _declare, _form_for, _heads, _live, _non_constraint, _post, _project, _raw,
    _rows, _start, _withdraw, client,
)
from tests.test_stage15_interface_preparation import _pdf_source
from web import ui_text

REPORT = "/session/%s/deliverable"


def _t(key, lang="en"):
    return ui_text.text(key, lang)


# ==========================================================================
# 1. Plan owner (pure)
# ==========================================================================
def _ledger():
    s = IdeaState(idea_id="cavp")
    s.record_interaction("answered", "A spring latch locks the deck.", gap_context=MECHANISM_COMPLETENESS)
    d = s.record_constraint_action("declare", TEXT, "mandatory_constraint")
    p = s.record_constraint_action("declare", "Nice if it is blue", "preference")
    return s, d, p


def _constraint_steps(plan):
    return [st for st in plan.steps if st.provenance.anchor_kind == CONSTRAINT_ANCHOR_KIND]


def _without_acceptance(plan):
    return [(st.step_id, st.statement, st.responsibility, st.evidence_category, st.closure_condition,
             st.provenance, st.confidence, st.interface_preparation) for st in plan.steps]


def test_e01_not_attached_claims_nothing_and_the_plan_is_unchanged():
    s, d, _p = _ledger()
    plan = derive_validation_plan(s)
    [step] = _constraint_steps(plan)
    assert step.step_id == "vstep:constraint:" + d.record_id and step.constraint_acceptance is None
    s.constraint_acceptance_preparations = [Prep(d.record_id, d.record_id, "It reads under 2 kg", None)]
    attached = derive_validation_plan(s)
    assert _without_acceptance(attached) == _without_acceptance(plan)
    assert (attached.outcome, attached.blocked_items) == (plan.outcome, plan.blocked_items)
    assert [st.constraint_acceptance for st in attached.steps
            if st.provenance.anchor_kind != CONSTRAINT_ANCHOR_KIND] == [None] * (len(attached.steps) - 1)


def test_e02_none_recorded_and_current_notes_with_what_is_missing():
    s, d, _p = _ledger()
    s.constraint_acceptance_preparations = []
    [step] = _constraint_steps(derive_validation_plan(s))
    assert step.constraint_acceptance == ConstraintAcceptanceView(CONSTRAINT_ACCEPTANCE_NONE, (), (CRIT, EVID))
    s.constraint_acceptance_preparations = [Prep(d.record_id, d.record_id, None, "A kitchen scale")]
    [step] = _constraint_steps(derive_validation_plan(s))
    assert step.constraint_acceptance == ConstraintAcceptanceView(
        CONSTRAINT_ACCEPTANCE_RECORDED, ((EVID, "A kitchen scale"),), (CRIT,))
    s.constraint_acceptance_preparations = [Prep(d.record_id, d.record_id, "Reads under 2 kg", "A scale")]
    [step] = _constraint_steps(derive_validation_plan(s))
    assert step.constraint_acceptance == ConstraintAcceptanceView(
        CONSTRAINT_ACCEPTANCE_RECORDED, ((CRIT, "Reads under 2 kg"), (EVID, "A scale")), ())


def test_e03_correction_and_strength_changes_keep_identity_and_mark_earlier_notes():
    s, d, _p = _ledger()
    note = Prep(d.record_id, d.record_id, "Reads under 2 kg", None)
    s.constraint_acceptance_preparations = [note]
    c1 = s.record_constraint_action("correct", "It must weigh under 1.5 kg", "mandatory_constraint",
                                    target_record_id=d.record_id)
    [step] = _constraint_steps(derive_validation_plan(s))
    assert step.step_id == "vstep:constraint:" + d.record_id                     # founding identity kept
    assert "It must weigh under 1.5 kg" in step.statement
    assert step.constraint_acceptance == ConstraintAcceptanceView(
        CONSTRAINT_ACCEPTANCE_EARLIER, ((CRIT, "Reads under 2 kg"),), (CRIT, EVID))   # counted for nothing
    c2 = s.record_constraint_action("correct", "It must weigh under 1.5 kg", "soft_constraint",
                                    target_record_id=c1.record_id)
    assert _constraint_steps(derive_validation_plan(s)) == []                   # no step, notes hidden
    c3 = s.record_constraint_action("correct", "It must weigh under 1.5 kg", "mandatory_constraint",
                                    target_record_id=c2.record_id)
    [step] = _constraint_steps(derive_validation_plan(s))
    assert step.constraint_acceptance.status == CONSTRAINT_ACCEPTANCE_EARLIER
    s.constraint_acceptance_preparations = [Prep(d.record_id, c3.record_id, "Reads under 1.5 kg", None)]
    [step] = _constraint_steps(derive_validation_plan(s))
    assert step.constraint_acceptance.status == CONSTRAINT_ACCEPTANCE_RECORDED
    s.record_constraint_action("withdraw", target_record_id=c3.record_id)
    assert _constraint_steps(derive_validation_plan(s)) == []


def test_e04_unreadable_or_inconsistent_notes_read_unavailable_never_none():
    s, d, _p = _ledger()
    answer = s.assertions[0].record_id
    for carrier in (CONSTRAINT_ACCEPTANCE_UNREADABLE,
                    [Prep(answer, answer, "x", None)],                      # names no constraint
                    [Prep(d.record_id, "rec_999", "x", None)],              # a version this ledger lacks
                    [Prep(d.record_id, d.record_id, None, None)],           # empty
                    [Prep(d.record_id, d.record_id, "x", None)] * 2,        # duplicated
                    ["not a preparation"]):
        s.constraint_acceptance_preparations = carrier
        plan = derive_validation_plan(s)
        [step] = _constraint_steps(plan)
        assert step.constraint_acceptance == ConstraintAcceptanceView(CONSTRAINT_ACCEPTANCE_UNAVAILABLE), carrier
        assert plan.outcome == "PLAN" and not plan.blocked_items


def test_e05_two_constraints_each_get_their_own_notes():
    s, d, _p = _ledger()
    e = s.record_constraint_action("declare", "It must be waterproof", "mandatory_constraint")
    s.constraint_acceptance_preparations = [Prep(e.record_id, e.record_id, "No water inside after a shower", None)]
    first, second = _constraint_steps(derive_validation_plan(s))
    assert first.constraint_acceptance.status == CONSTRAINT_ACCEPTANCE_NONE
    assert second.constraint_acceptance.recorded == ((CRIT, "No water inside after a shower"),)


# ==========================================================================
# 2. Report / PDF
# ==========================================================================
def _section14(raw):
    start = raw.index("vp-intro")
    return _html.unescape(raw[start:])


def _ca_blocks(raw):
    return re.findall(r'<div class="vp-constraint-acceptance" data-vp-constraint-acceptance="([A-Z_]+)"', raw)


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_w01_report_and_pdf_show_the_same_notes(client, monkeypatch, lang):
    sid, cid = _project(client)
    note = "يقرأ الميزان أقل من 2 كغ" if lang == "ar" else "The scale reads under 2 kg"
    _post(client, sid, _form_for(client, sid, cid), note)
    if lang == "ar":
        assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    report = client.get(REPORT % sid).get_data(as_text=True)
    pdf = _pdf_source(client, sid, monkeypatch)
    for raw in (report, pdf):
        assert _ca_blocks(raw) == [CONSTRAINT_ACCEPTANCE_RECORDED]
        text = _section14(raw)
        for key in ("UI_PCA_VP_CRITERION", "UI_PCA_VP_EVIDENCE", "UI_PCA_VP_MISSING", "UI_PCA_VP_BOUNDARY"):
            assert _t(key, lang) in text, key
        assert note in text
        assert re.search(r'<bdi dir="auto"[^>]*>%s</bdi>' % re.escape(note), raw)   # direction-isolated
    if lang == "ar":
        assert 'dir="rtl"' in report


def test_w02_a_correction_shows_earlier_notes_until_saved_again(client, monkeypatch):
    sid, cid = _project(client)
    _post(client, sid, _form_for(client, sid, cid), "Zq-earlier-4411")
    _correct(client, sid, cid, "It must weigh under 1.5 kg")
    for raw in (client.get(REPORT % sid).get_data(as_text=True), _pdf_source(client, sid, monkeypatch)):
        assert _ca_blocks(raw) == [CONSTRAINT_ACCEPTANCE_EARLIER]
        assert _t("UI_PCA_VP_EARLIER") in _section14(raw) and "Zq-earlier-4411" in raw
    _post(client, sid, _form_for(client, sid, cid))                              # saved again, same text
    raw = client.get(REPORT % sid).get_data(as_text=True)
    assert _ca_blocks(raw) == [CONSTRAINT_ACCEPTANCE_RECORDED] and _t("UI_PCA_VP_EARLIER") not in _section14(raw)


def test_w03_soft_and_withdrawn_constraints_show_no_notes(client):
    sid, cid = _project(client)
    _post(client, sid, _form_for(client, sid, cid), "Zq-hidden-5512")
    _correct(client, sid, cid, TEXT, "soft_constraint")
    raw = client.get(REPORT % sid).get_data(as_text=True)
    assert _ca_blocks(raw) == [] and "Zq-hidden-5512" not in raw
    _correct(client, sid, cid, TEXT, "mandatory_constraint")
    _withdraw(client, sid, cid)
    raw = client.get(REPORT % sid).get_data(as_text=True)
    assert _ca_blocks(raw) == [] and "Zq-hidden-5512" not in raw
    assert _rows(sid)[0][2] == "Zq-hidden-5512"                                  # kept


def test_w04_unreadable_notes_read_unavailable_and_the_report_still_renders(client, monkeypatch):
    sid, _cid = _project(client)
    answer = _non_constraint(sid)
    _raw("INSERT INTO constraint_acceptance_preparations VALUES (?, ?, ?, ?, ?)", (sid, answer, answer, "x", None))
    r = client.get(REPORT % sid)
    raw = r.get_data(as_text=True)
    assert r.status_code == 200 and _ca_blocks(raw) == [CONSTRAINT_ACCEPTANCE_UNAVAILABLE]
    assert _t("UI_PCA_VP_UNAVAILABLE") in _section14(raw) and _t("UI_PCA_VP_MISSING") not in _section14(raw)
    assert _ca_blocks(_pdf_source(client, sid, monkeypatch)) == [CONSTRAINT_ACCEPTANCE_UNAVAILABLE]


def test_w05_nothing_recorded_states_both_inputs_missing(client):
    sid, _cid = _project(client)
    raw = client.get(REPORT % sid).get_data(as_text=True)
    assert _ca_blocks(raw) == [CONSTRAINT_ACCEPTANCE_NONE]
    missing = re.search(r"<div data-vp-ca-missing>(.*?)</div>", raw, re.S).group(1)
    assert _t("UI_PCA_VP_CRITERION") in _html.unescape(missing) and _t("UI_PCA_VP_EVIDENCE") in _html.unescape(missing)


def test_w06_project_isolation(client):
    sid, cid = _project(client)
    other = _start(client)
    _answer(client, other, MECH)
    _declare(client, other)
    _post(client, sid, _form_for(client, sid, cid), "Zq-mine-6613")
    assert "Zq-mine-6613" in client.get(REPORT % sid).get_data(as_text=True)
    raw = client.get(REPORT % other).get_data(as_text=True)
    assert "Zq-mine-6613" not in raw and _ca_blocks(raw) == [CONSTRAINT_ACCEPTANCE_NONE]


def _stable_package(package):
    """The canonical package without its intentionally time-varying stamp.

    ``assemble_deliverable`` stamps every assembly with ``generated_at`` (one-
    second resolution), so two legitimate assemblies may differ in that one
    field alone. The invariant under test — acceptance preparation changes no
    canonical package semantics — is judged on every other field verbatim."""
    assert "generated_at" in package
    return {key: value for key, value in package.items() if key != "generated_at"}


def test_w07_canonical_package_and_export_are_unchanged(client):
    sid, cid = _project(client)
    state = _live(sid)
    state.constraint_acceptance_preparations = None
    before = assemble_deliverable(state)
    _post(client, sid, _form_for(client, sid, cid), "Zq-pkg-7714", "Zq-pkg-evidence")
    client.get(REPORT % sid)                                                      # attaches the carrier
    assert _live(sid).constraint_acceptance_preparations                          # attached on the live state
    after = assemble_deliverable(_live(sid))
    assert _stable_package(after) == _stable_package(before) and "Zq-pkg-7714" not in repr(after)
    import engine.disclosure_export as export
    source = open(export.__file__, encoding="utf-8").read()
    assert "constraint_acceptance" not in source and "validation_plan" not in source


def test_w08_no_overclaim_and_the_step_wording_is_unchanged(client):
    sid, cid = _project(client)
    plain = client.get(REPORT % sid).get_data(as_text=True)
    _post(client, sid, _form_for(client, sid, cid), "Reads under 2 kg", "A scale")
    raw = client.get(REPORT % sid).get_data(as_text=True)
    statement = "Prepare how your mandatory constraint “%s” will be checked" % TEXT
    assert _html.escape(statement, quote=False) in plain and _html.escape(statement, quote=False) in raw
    for phrase in ("specialist review", "expert review", "constraint is verified", "has been verified", "constraint is satisfied", "constraint has been met"):
        assert phrase not in raw.lower(), phrase
    assert _ca_blocks(raw) == [CONSTRAINT_ACCEPTANCE_RECORDED]
    assert "data-vp-ca-missing" not in raw                                        # both recorded


def test_w09_rendering_leaves_projects_without_a_mandatory_constraint_untouched(client):
    sid = _start(client)
    _answer(client, sid, MECH)
    _declare(client, sid, "Nice if it is blue", "preference")
    client.get(REPORT % sid)
    assert _live(sid).constraint_acceptance_preparations is None                 # never attached
    raw = client.get(REPORT % sid).get_data(as_text=True)
    assert _ca_blocks(raw) == []
