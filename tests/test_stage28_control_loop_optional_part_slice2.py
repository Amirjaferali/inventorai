"""Stage 28 — Control-Loop Optional Part — Slice 2 (part-scoped governed question service + part answers, DORMANT).

For a project whose DURABLE composition holds the optional ``control_loop`` part, and only while the canonical policy
lists that part as part-eligible (the shipped allowlist is EMPTY), the inventor may record, edit and clear their own
answers to the part's ALREADY-QUALIFIED MECHANISM_COMPLETENESS and BOUNDARY_AMBIGUITY questions, served verbatim from
``domains/control_loop/domain.json``. The answers are OWNER_STATED / UNVALIDATED current values keyed by
(project, subsystem id, governed question id) in ONE additive sidecar. They never touch the root focus, a root gap,
maturity, progression, readiness, the Stage-15 interface owners, Integration evidence, the report, the PDF or the
Structured Export. The three-part paths are exercised only through a test-only eligibility double.
"""
import ast
import html as _html
import json
import os
import re
import sqlite3

import pytest

import web.app as appmod
from engine import domain_activation
from engine import domain_rules
from engine import subsystem_model as sm
from engine.domain_rules import get_domain_questions
from engine.record_store import (
    PartAnswerRejected, PartAnswersCorrupt, ProjectNotFound, SqliteRecordStore)
from tests.test_stage15_integrated_invention_entry import (
    ELEC, MECH, TIE_IDEA, _compose, _contract, _created, _live, _pair, _pdf_source, _ri)
from tests.test_stage28_control_loop_optional_part_slice1 import (  # noqa: F401  (fixtures)
    CL, CTRL, _rows, _three_part_project, client, part_eligible)
from tests.test_stage15_integration_closure import _login
from web import ui_text

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
MC, BA, PF = "MECHANISM_COMPLETENESS", "BOUNDARY_AMBIGUITY", "PHYSICAL_FEASIBILITY"
Q1 = "control_loop:MECHANISM_COMPLETENESS:Q1"
Q2 = "control_loop:MECHANISM_COMPLETENESS:Q2"
B1 = "control_loop:BOUNDARY_AMBIGUITY:Q1"


def _pack_questions(gap_type, domain=CL):
    with open(os.path.join(_ROOT, "domains", domain, "domain.json"), encoding="utf-8") as fh:
        pack = json.load(fh)
    for mapping in pack["gap_type_mappings"]:
        if mapping["gap_type_id"] == gap_type:
            return [(q["question_id"], q["text"]) for q in mapping["questions"]]
    return None


def _all_current_ids():
    return [qid for g in (MC, BA) for qid, _t in _pack_questions(g)]


def _store(tmp_path, name="s.db"):
    return SqliteRecordStore(str(tmp_path / name))


def _stored_three_part(store, idea_id="i-s28s2"):
    mech, elec = _pair()
    ctrl = sm.declared_subsystem(CL, "Thermostat logic", "Compares the temperature with the target")
    pid = store.create_project(_contract(idea_id), reconstruction_inputs=_ri(), subsystems=(mech, elec, ctrl))
    return pid, mech, elec, ctrl


def _ctrl_id(sid):
    return next(s.subsystem_id for s in appmod._get_store().load_project_subsystems(sid) if s.domain == CL)


def _page(c, sid):
    return c.get("/session/%s/part-questions" % sid)


def _form(c, sid):
    """The form fields exactly as the page rendered them (answers + baselines + part id)."""
    raw = _page(c, sid).get_data(as_text=True)
    fields = {"part_id": _html.unescape(re.search(r'name="part_id" value="([^"]*)"', raw).group(1))}
    for name, value in re.findall(r'<textarea[^>]*name="(part_answer__[^"]+)"[^>]*>([^<]*)</textarea>', raw, re.S):
        fields[_html.unescape(name)] = _html.unescape(value)
    for name, value in re.findall(r'name="(part_base__[^"]+)" value="([^"]*)"', raw):
        fields[_html.unescape(name)] = _html.unescape(value)
    return fields


def _save(c, sid, answers, form=None):
    data = dict(form if form is not None else _form(c, sid))
    for qid, text in answers.items():
        data["part_answer__" + qid] = text
    return c.post("/session/%s/part-questions" % sid, data=data)


def _answers_rows(sid=None):
    if sid is None:
        return _rows("SELECT project_id, subsystem_id, question_id, answer_text FROM subsystem_part_answers")
    return _rows("SELECT subsystem_id, question_id, answer_text FROM subsystem_part_answers "
                 "WHERE project_id = ? ORDER BY question_id", (sid,))


def _all_table_counts(exclude=("subsystem_part_answers",)):
    names = [r[0] for r in _rows("SELECT name FROM sqlite_master WHERE type = 'table'")]
    return {n: _rows("SELECT COUNT(*) FROM %s" % n)[0][0] for n in names if n not in exclude}


def _root_snapshot(sid):
    state = _live(sid)
    return (len(state.assertions), [(g.gap_type, g.status) for g in state.gaps], state.maturity_level,
            state.current_stage, state.domain, getattr(state, "iteration", None),
            [(s.subsystem_id, s.domain) for s in state.subsystems])


# ==========================================================================
# 1-4. Governed question accessor: exact pack source, no fallback, MC + BA only
# ==========================================================================
@pytest.mark.parametrize("gap_type", [MC, BA])
def test_accessor_serves_the_exact_pack_ids_text_and_order(gap_type):
    served = get_domain_questions(CL, gap_type)
    assert list(served) == _pack_questions(gap_type)
    assert [qid for qid, _t in served] == ["control_loop:%s:Q%d" % (gap_type, n) for n in range(1, len(served) + 1)]


def test_accessor_returns_none_never_a_substitute():
    assert get_domain_questions(CL, PF) is None                       # the pack has no PF mapping
    assert get_domain_questions(CL, "NOT_A_GAP") is None
    assert get_domain_questions("no_such_pack", MC) is None
    assert get_domain_questions("", MC) is None
    # the existing single-question seam still reads its own packs unchanged
    assert domain_rules.get_domain_question(MECH, MC, 0) == _pack_questions(MC, MECH)[0][1]


@pytest.mark.parametrize("bad_questions", [
    [],                                                             # no questions
    [{"question_id": "x:MECHANISM_COMPLETENESS:Q1", "text": " "}],  # blank text
    [{"text": "A question"}],                                       # missing id
    [{"question_id": "d:MECHANISM_COMPLETENESS:Q1", "text": "A"},
     {"question_id": "d:MECHANISM_COMPLETENESS:Q1", "text": "B"}],  # duplicate id
])
def test_accessor_fails_unavailable_on_an_unreadable_question_list(monkeypatch, bad_questions):
    fake = {"d": {"gap_type_mappings": [{"gap_type_id": MC, "questions": bad_questions}]}}
    monkeypatch.setattr(domain_rules, "_REGISTRY", fake)
    assert get_domain_questions("d", MC) is None


def test_only_mechanism_completeness_and_boundary_ambiguity_are_part_question_families():
    assert sm.PART_QUESTION_GAP_TYPES == (MC, BA)
    assert PF not in sm.PART_QUESTION_GAP_TYPES


def test_page_shows_exactly_the_governed_mc_and_ba_questions_verbatim(client, part_eligible):
    sid = _three_part_project(client)
    raw = _page(client, sid).get_data(as_text=True)
    served = [_html.unescape(t) for t in re.findall(r'data-pq-question>([^<]*)</span>', raw)]
    assert served == [t for g in (MC, BA) for _qid, t in _pack_questions(g)]
    names = [_html.unescape(n) for n in re.findall(r'name="part_answer__([^"]+)"', raw)]
    assert names == _all_current_ids()
    assert raw.count("data-pq-family ") + raw.count("data-pq-family>") == 2
    assert PF not in raw and "PHYSICAL" not in raw


def test_page_fails_closed_without_generic_or_path_n_questions(client, part_eligible, monkeypatch):
    sid = _three_part_project(client)
    monkeypatch.setattr(appmod, "get_domain_questions",
                        lambda domain, gap: None if gap == BA else get_domain_questions(domain, gap))
    r = _page(client, sid)
    raw = _html.unescape(r.get_data(as_text=True))
    assert r.status_code == 503
    assert ui_text.text("UI_PQ_MSG_UNAVAILABLE", "en") in raw
    assert "part_answer__" not in raw and "data-pq-question" not in raw
    for _qid, text in _pack_questions(MC):                       # not even the readable family
        assert text not in raw
    assert domain_rules.get_domain_question(MECH, BA, 0) not in raw
    before = _answers_rows(sid)
    assert client.post("/session/%s/part-questions" % sid, data={"part_id": "x"}).status_code == 503
    assert _answers_rows(sid) == before


# ==========================================================================
# 5-8. Part answers: identity, fail-closed writes, record / edit / clear, confirm-by-reload
# ==========================================================================
def test_sidecar_is_keyed_by_project_subsystem_and_question_and_anchored_to_the_part(tmp_path):
    store = _store(tmp_path)
    conn = sqlite3.connect(str(tmp_path / "s.db"))
    try:
        cols = conn.execute("PRAGMA table_info(subsystem_part_answers)").fetchall()
        fks = conn.execute("PRAGMA foreign_key_list(subsystem_part_answers)").fetchall()
    finally:
        conn.close()
    assert [c[1] for c in cols] == ["project_id", "subsystem_id", "question_id", "answer_text"]
    assert [c[1] for c in sorted(cols, key=lambda c: c[5]) if c[5]] == ["project_id", "subsystem_id", "question_id"]
    anchors = {(f[2], f[3], f[4]) for f in fks}
    assert ("project_subsystems", "project_id", "project_id") in anchors
    assert ("project_subsystems", "subsystem_id", "subsystem_id") in anchors
    assert ("projects", "project_id", "project_id") in anchors
    store.close()


def test_store_records_edits_and_clears_one_part_answer_at_a_time(tmp_path):
    store = _store(tmp_path)
    pid, _m, _e, ctrl = _stored_three_part(store)
    assert store.load_part_answers(pid, ctrl.subsystem_id) == ()
    store.apply_part_answer_delta(pid, ctrl.subsystem_id, {Q1: "Room temperature", B1: "It does not heat water"})
    assert {a.question_id: a.answer_text for a in store.load_part_answers(pid, ctrl.subsystem_id)} == {
        Q1: "Room temperature", B1: "It does not heat water"}
    store.apply_part_answer_delta(pid, ctrl.subsystem_id, {Q1: "Water level"})          # edit; B1 untouched
    store.apply_part_answer_delta(pid, ctrl.subsystem_id, {B1: None})                   # clear removes the row
    answers = store.load_part_answers(pid, ctrl.subsystem_id)
    assert [(a.subsystem_id, a.question_id, a.answer_text) for a in answers] == [
        (ctrl.subsystem_id, Q1, "Water level")]
    assert all(isinstance(a, sm.PartAnswer) for a in answers)
    store.close()


def test_store_rejects_cross_project_wrong_subsystem_and_foreign_questions(tmp_path):
    store = _store(tmp_path)
    pid_a, mech_a, elec_a, ctrl_a = _stored_three_part(store, "i-a")
    pid_b, _mb, _eb, ctrl_b = _stored_three_part(store, "i-b")
    two = store.create_project(_contract("i-two"), reconstruction_inputs=_ri(), subsystems=_pair())
    bad = [
        (pid_a, ctrl_b.subsystem_id, {Q1: "x"}),                                  # another project's part
        (pid_a, mech_a.subsystem_id, {"mechanical:MECHANISM_COMPLETENESS:Q1": "x"}),  # a required part
        (pid_a, elec_a.subsystem_id, {Q1: "x"}),
        (pid_a, ctrl_a.subsystem_id, {"mechanical:MECHANISM_COMPLETENESS:Q1": "x"}),  # same family, other domain
        (pid_a, ctrl_a.subsystem_id, {"control_loop:BAD": "x"}),                  # malformed question id
        (pid_a, ctrl_a.subsystem_id, {Q1: " padded "}),                           # untrimmed
        (pid_a, ctrl_a.subsystem_id, {Q1: "nul\x00"}),
        (pid_a, ctrl_a.subsystem_id, {Q1: "x" * (sm.MAX_PART_ANSWER_LENGTH + 1)}),
        (pid_a, ctrl_a.subsystem_id, {}),
        (two, ctrl_a.subsystem_id, {Q1: "x"}),                                    # a project with no optional part
        (pid_a, "sub-" + "0" * 32, {Q1: "x"}),
    ]
    for project_id, subsystem_id, delta in bad:
        with pytest.raises(PartAnswerRejected):
            store.apply_part_answer_delta(project_id, subsystem_id, delta)
    with pytest.raises(ProjectNotFound):
        store.apply_part_answer_delta("no-such-project", ctrl_a.subsystem_id, {Q1: "x"})
    with pytest.raises(PartAnswerRejected):
        store.load_part_answers(pid_a, ctrl_b.subsystem_id)
    # a mixed delta with ONE bad question writes nothing at all
    with pytest.raises(PartAnswerRejected):
        store.apply_part_answer_delta(pid_a, ctrl_a.subsystem_id, {Q1: "ok", "mechanical:BOUNDARY_AMBIGUITY:Q1": "x"})
    assert store.load_part_answers(pid_a, ctrl_a.subsystem_id) == ()
    assert store.load_part_answers(pid_b, ctrl_b.subsystem_id) == ()
    store.close()


def test_a_stored_answer_to_a_question_no_longer_asked_is_preserved_never_remapped(tmp_path):
    store = _store(tmp_path)
    pid, _m, _e, ctrl = _stored_three_part(store)
    old = "control_loop:MECHANISM_COMPLETENESS:Q99"
    store.apply_part_answer_delta(pid, ctrl.subsystem_id, {old: "Earlier answer"})
    answers = store.load_part_answers(pid, ctrl.subsystem_id)
    assert [(a.question_id, a.answer_text) for a in answers] == [(old, "Earlier answer")]
    store.close()


def test_corrupt_durable_rows_fail_closed_for_the_whole_collection(tmp_path):
    store = _store(tmp_path)
    pid, mech, _e, ctrl = _stored_three_part(store)
    store.apply_part_answer_delta(pid, ctrl.subsystem_id, {Q1: "Room temperature"})
    conn = sqlite3.connect(str(tmp_path / "s.db"))
    try:
        conn.execute("INSERT INTO subsystem_part_answers VALUES (?, ?, ?, ?)",
                     (pid, mech.subsystem_id, "mechanical:MECHANISM_COMPLETENESS:Q1", "planted"))
        conn.commit()
    finally:
        conn.close()
    with pytest.raises(PartAnswersCorrupt):
        store.load_part_answers(pid, ctrl.subsystem_id)
    with pytest.raises(PartAnswersCorrupt):
        store.apply_part_answer_delta(pid, ctrl.subsystem_id, {Q2: "x"})
    store.close()


def test_route_records_edits_and_clears_with_presence_only_status(client, part_eligible):
    sid = _three_part_project(client)
    ctrl = _ctrl_id(sid)
    raw = _html.unescape(_page(client, sid).get_data(as_text=True))
    assert raw.count(ui_text.text("UI_PQ_FAMILY_NONE", "en")) == 2
    r = _save(client, sid, {Q1: "  Room temperature  ", B1: "It does not heat water"})
    raw = _html.unescape(r.get_data(as_text=True))
    assert r.status_code == 200 and ui_text.text("UI_PQ_MSG_SAVED", "en") in raw
    assert _answers_rows(sid) == [(ctrl, B1, "It does not heat water"), (ctrl, Q1, "Room temperature")]
    assert raw.count(ui_text.text("UI_PQ_FAMILY_SOME", "en")) == 2
    assert raw.count(ui_text.text("UI_PQ_RECORDED", "en")) == 2
    assert raw.count(ui_text.text("UI_PQ_NOT_RECORDED", "en")) == len(_all_current_ids()) - 2
    # all BA answered -> ALL RECORDED for that family only (presence, never a gap state)
    r = _save(client, sid, {qid: "Answer %s" % qid[-2:] for qid, _t in _pack_questions(BA)})
    raw = _html.unescape(r.get_data(as_text=True))
    assert ui_text.text("UI_PQ_FAMILY_ALL", "en") in raw and ui_text.text("UI_PQ_FAMILY_SOME", "en") in raw
    for word in ("OPEN", "PARTIAL", "CLOSED", "Resolved", "Validated"):
        assert word not in _html.unescape(re.sub(r"<[^>]+>", " ", raw.split("<form", 1)[1]))
    # edit + clear
    _save(client, sid, {Q1: "Water level", B1: ""})
    rows = dict(((q, t) for _s, q, t in _answers_rows(sid)))
    assert rows[Q1] == "Water level" and B1 not in rows
    # an exact retry of a committed save changes nothing
    form = _form(client, sid)
    form["part_answer__" + Q2] = "20 C"
    assert client.post("/session/%s/part-questions" % sid, data=form).status_code == 200
    before = _answers_rows(sid)
    r = client.post("/session/%s/part-questions" % sid, data=form)
    assert ui_text.text("UI_PQ_MSG_UNCHANGED", "en") in _html.unescape(r.get_data(as_text=True))
    assert _answers_rows(sid) == before


def test_route_rejects_wrong_part_foreign_and_unknown_questions(client, part_eligible):
    sid_a = _three_part_project(client)
    sid_b = _three_part_project(client)
    mech_a = next(s.subsystem_id for s in _live(sid_a).subsystems if s.domain == MECH)
    cases = []
    form = _form(client, sid_a)
    cases.append(dict(form, part_id=_ctrl_id(sid_b)))                       # another project's part
    cases.append(dict(form, part_id=mech_a))                                # a required part of THIS project
    cases.append(dict(form, **{"part_answer__mechanical:MECHANISM_COMPLETENESS:Q1": "x",
                               "part_base__mechanical:MECHANISM_COMPLETENESS:Q1": ""}))
    cases.append(dict(form, **{"part_answer__control_loop:MECHANISM_COMPLETENESS:Q99": "x",
                               "part_base__control_loop:MECHANISM_COMPLETENESS:Q99": ""}))
    cases.append(dict(form, **{"part_answer__control_loop:PHYSICAL_FEASIBILITY:Q1": "x",
                               "part_base__control_loop:PHYSICAL_FEASIBILITY:Q1": ""}))
    for data in cases:
        data["part_answer__" + Q1] = "should never be written"
        r = client.post("/session/%s/part-questions" % sid_a, data=data)
        assert r.status_code == 400
        assert ui_text.text("UI_PQ_MSG_UNKNOWN_QUESTION", "en") in _html.unescape(r.get_data(as_text=True))
    missing_base = dict(form)
    missing_base.pop("part_base__" + Q1)
    missing_base["part_answer__" + Q1] = "x"
    assert client.post("/session/%s/part-questions" % sid_a, data=missing_base).status_code == 400
    too_long = _save(client, sid_a, {Q1: "x" * (sm.MAX_PART_ANSWER_LENGTH + 1)})
    assert too_long.status_code == 400
    assert ui_text.text("UI_PQ_MSG_TOO_LONG", "en") in _html.unescape(too_long.get_data(as_text=True))
    assert _answers_rows(sid_a) == [] and _answers_rows(sid_b) == []


def test_route_is_guarded_by_the_central_project_authorization(client, part_eligible, monkeypatch):
    sid = _three_part_project(client)
    form = _form(client, sid)
    denied = appmod._deny_project
    monkeypatch.setattr(appmod, "_project_authorized", lambda _sid: False)
    for r in (client.get("/session/%s/part-questions" % sid),
              client.post("/session/%s/part-questions" % sid, data=dict(form, **{"part_answer__" + Q1: "x"}))):
        with appmod.app.test_request_context():
            assert r.status_code == denied().status_code
        assert "part_answer__" not in r.get_data(as_text=True)
    assert _answers_rows(sid) == []


def test_confirm_by_reload_saved_not_saved_and_unknown(client, part_eligible, monkeypatch):
    sid = _three_part_project(client)
    store = appmod._get_store()
    real = store.apply_part_answer_delta

    def commit_then_raise(*a, **k):
        real(*a, **k)
        raise sqlite3.OperationalError("injected: commit outcome uncertain")
    monkeypatch.setattr(store, "apply_part_answer_delta", commit_then_raise)
    r = _save(client, sid, {Q1: "Room temperature"})
    assert r.status_code == 200
    assert ui_text.text("UI_PQ_MSG_SAVED", "en") in _html.unescape(r.get_data(as_text=True))

    def raise_only(*a, **k):
        raise sqlite3.OperationalError("injected: nothing committed")
    monkeypatch.setattr(store, "apply_part_answer_delta", raise_only)
    r = _save(client, sid, {Q1: "Water level"})
    raw = _html.unescape(r.get_data(as_text=True))
    assert r.status_code == 503 and ui_text.text("UI_PQ_MSG_NOT_SAVED", "en") in raw
    assert "Water level" in raw and ui_text.text("UI_PQ_DRAFT_UNSAVED", "en") in raw   # request-local draft
    assert [t for _s, _q, t in _answers_rows(sid)] == ["Room temperature"]

    form = _form(client, sid)
    real_load, calls = store.load_part_answers, []

    def load_once_then_fail(*a, **k):          # the page context reads; the confirm read fails
        calls.append(1)
        if len(calls) > 1:
            raise sqlite3.OperationalError("injected: committed truth unreadable")
        return real_load(*a, **k)
    monkeypatch.setattr(store, "load_part_answers", load_once_then_fail)
    form["part_answer__" + Q1] = "Water level"
    r = client.post("/session/%s/part-questions" % sid, data=form)
    raw = _html.unescape(r.get_data(as_text=True))
    assert r.status_code == 503 and ui_text.text("UI_PQ_MSG_UNKNOWN", "en") in raw
    assert "part_answer__" not in raw


# ==========================================================================
# 9-13. Isolation: root gaps, maturity, progression, readiness, Integration,
#       report, PDF and Structured Export are unchanged
# ==========================================================================
def test_part_answers_touch_no_root_gap_progression_or_other_table(client, part_eligible):
    sid = _three_part_project(client)
    before_root = _root_snapshot(sid)
    before_tables = _all_table_counts()
    focus = _rows("SELECT confirmed_domain FROM projects WHERE project_id = ?", (sid,))
    _save(client, sid, {qid: "Answer to %s" % qid for qid in _all_current_ids()})
    assert len(_answers_rows(sid)) == len(_all_current_ids())
    assert _root_snapshot(sid) == before_root
    assert _all_table_counts() == before_tables
    assert _rows("SELECT confirmed_domain FROM projects WHERE project_id = ?", (sid,)) == focus == [(MECH,)]


def test_report_pdf_export_readiness_and_session_carry_no_part_answer(client, part_eligible, monkeypatch):
    _login(client, "s28-s2-owner@example.com")
    sid = _three_part_project(client)
    assert appmod._get_store().load_owner(sid)[1] is not None          # an OWNED project
    readiness_before = appmod._readiness_snapshot_context(sid, _live(sid))
    report_before = client.get("/session/%s/deliverable" % sid).get_data(as_text=True)
    export_before = client.get("/account/projects/%s/export" % sid).get_data(as_text=True)
    marker = "PartAnswerMarkerS28S2"
    _save(client, sid, {Q1: marker, B1: marker + " boundary"})
    report = client.get("/session/%s/deliverable" % sid)
    export = client.get("/account/projects/%s/export" % sid)
    assert report.status_code == 200 and export.status_code == 200
    pdf = _pdf_source(client, sid, monkeypatch)
    session = client.get("/session/%s" % sid).get_data(as_text=True)
    for body in (report.get_data(as_text=True), export.get_data(as_text=True), pdf, session):
        assert marker not in body
        assert Q1 not in body and "subsystem_part_answers" not in body
    strip = lambda raw: re.sub(r'name="csrf_token" value="[^"]*"', "", raw)  # noqa: E731
    assert strip(report.get_data(as_text=True)) == strip(report_before)
    assert export.get_data(as_text=True) == export_before
    assert appmod._readiness_snapshot_context(sid, _live(sid)) == readiness_before
    # another signed-in account is denied the part page and its write
    form = _form(client, sid)
    from tests.csrf_client import csrf_client
    with csrf_client(appmod.app) as other:
        _login(other, "s28-s2-other@example.com")
        assert other.get("/session/%s/part-questions" % sid).status_code in (302, 403, 404)
        r = other.post("/session/%s/part-questions" % sid, data=dict(form, **{"part_answer__" + Q2: "intruder"}))
        assert r.status_code in (302, 403, 404)
    assert "intruder" not in [t for _s, _q, t in _answers_rows(sid)]


def test_root_owners_never_read_part_answers():
    """Static: progression, gap, readiness, classifier, Stage-15 interface and evidence owners do not reference
    the part-answer owner or its table."""
    owners = ["engine/progression_loop.py", "engine/controlled_unknown_progression.py", "engine/domain_rules.py",
              "engine/readiness_snapshot.py", "engine/validation_plan.py", "engine/commercial_evidence.py",
              "engine/interface_observation.py", "engine/idea_state.py", "engine/deliverable_assembler.py",
              "engine/path_n_questions.py", "engine/read_export_service.py", "engine/domain_activation.py"]
    for rel in owners:
        with open(os.path.join(_ROOT, rel), encoding="utf-8") as fh:
            src = fh.read()
        for needle in ("subsystem_part_answers", "PartAnswer", "part_family_presence", "load_part_answers",
                       "apply_part_answer_delta"):
            assert needle not in src, (rel, needle)
    with open(os.path.join(_ROOT, "engine", "progression_loop.py"), encoding="utf-8") as fh:
        assert "get_domain_questions" not in fh.read()


# ==========================================================================
# 14-17. Two-part unchanged; dormant; schema additive; not activated / enabled
# ==========================================================================
def test_two_part_projects_get_no_part_questions_even_when_eligible(client, part_eligible):
    sid = _created(_compose(client, TIE_IDEA, focus=MECH))
    assert [s.domain for s in _live(sid).subsystems] == [MECH, ELEC]
    r = _page(client, sid)
    assert r.status_code == 404
    assert ui_text.text("UI_PQ_MSG_NOT_OFFERED", "en") in _html.unescape(r.get_data(as_text=True))
    session = client.get("/session/%s" % sid).get_data(as_text=True)
    assert "data-scope-part-questions" not in session and "part-questions" not in session
    assert client.post("/session/%s/part-questions" % sid, data={"part_id": "x"}).status_code == 404
    assert _answers_rows(sid) == []


def test_three_part_functionality_is_dormant_while_the_allowlist_is_empty(client, part_eligible, monkeypatch):
    sid = _three_part_project(client)
    link = 'data-scope-part-questions'
    assert link in client.get("/session/%s" % sid).get_data(as_text=True)          # eligible double: offered
    form = _form(client, sid)
    monkeypatch.setattr(domain_activation, "_PART_ONLY_DOMAINS", frozenset())        # the SHIPPED state
    assert domain_activation.is_part_eligible(CL) is False
    # AMENDED at Stage 30 Slice 1 (Owner-authorized withdrawal readability): an already-saved part stays
    # READABLE (read-only view, read-only link); recording stays refused and nothing is written.
    assert ui_text.text("UI_PQ_LINK_READ_ONLY", "en") in _html.unescape(
        client.get("/session/%s" % sid).get_data(as_text=True))
    page = _page(client, sid)
    assert page.status_code == 200 and "part_answer__" not in page.get_data(as_text=True)
    r = client.post("/session/%s/part-questions" % sid, data=dict(form, **{"part_answer__" + Q1: "x"}))
    assert r.status_code == 409
    assert _answers_rows(sid) == []


def test_arabic_page_keeps_governed_text_verbatim_and_says_so(client, part_eligible):
    sid = _three_part_project(client)
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    try:
        raw = _html.unescape(_page(client, sid).get_data(as_text=True))
    finally:
        client.post("/ui-language", data={"lang": "en"})
    for key in ("UI_PQ_TITLE", "UI_PQ_INTRO", "UI_PQ_NOT_ROOT", "UI_PQ_SOURCE_NOTE", "UI_PQ_FAMILY_MECHANISM",
                "UI_PQ_FAMILY_BOUNDARY", "UI_PQ_SAVE"):
        assert ui_text.text(key, "ar") in raw, key
    for _qid, text in _pack_questions(MC) + _pack_questions(BA):
        assert '<span dir="ltr" lang="en" data-pq-question>%s</span>' % text in raw


def test_new_sidecar_is_additive_and_existing_rows_survive_reopening(tmp_path):
    store = _store(tmp_path)
    pid, _m, _e, ctrl = _stored_three_part(store)
    store.close()
    conn = sqlite3.connect(str(tmp_path / "s.db"))
    try:
        conn.execute("DROP TABLE subsystem_part_answers")       # an existing pre-slice database
        conn.commit()
        before = {n: conn.execute("SELECT sql FROM sqlite_master WHERE name = ?", (n,)).fetchone()
                  for (n,) in conn.execute("SELECT name FROM sqlite_master")}
    finally:
        conn.close()
    reopened = _store(tmp_path)
    conn = sqlite3.connect(str(tmp_path / "s.db"))
    try:
        after = {n: conn.execute("SELECT sql FROM sqlite_master WHERE name = ?", (n,)).fetchone()
                 for (n,) in conn.execute("SELECT name FROM sqlite_master")}
    finally:
        conn.close()
    assert set(after) - set(before) == {"subsystem_part_answers", "sqlite_autoindex_subsystem_part_answers_1"}
    assert {n: after[n] for n in before} == before                  # no existing table / index altered
    assert [s.subsystem_id for s in reopened.load_project_subsystems(pid)][-1] == ctrl.subsystem_id
    from engine.record_store import _PART_ANSWERS_SCHEMA
    assert all(stmt.strip().startswith("CREATE TABLE IF NOT EXISTS subsystem_part_answers")
               for stmt in _PART_ANSWERS_SCHEMA)
    reopened.close()


def test_control_loop_stays_not_root_activated_and_not_part_enabled():
    assert domain_activation._PART_ONLY_DOMAINS == frozenset()
    assert domain_activation._ACTIVATED_DOMAINS == frozenset({"electronics_electrical", "mechanical"})
    assert domain_activation.is_part_eligible(CL) is False
    assert domain_activation.is_activated(CL) is False
    assert domain_activation.support_state(CL) == domain_activation.RECOGNIZED_NOT_ACTIVATED
    assert CL not in domain_activation.activated_domains()


def test_part_answer_presence_is_scoped_to_the_part_and_never_shares_root_state():
    ctrl = sm.declared_subsystem(CL, "Loop", "Keeps it")
    other = sm.declared_subsystem(CL, "Loop", "Keeps it")
    ids = [Q1, Q2]
    answers = (sm.PartAnswer(ctrl.subsystem_id, Q1, "a"), sm.PartAnswer(other.subsystem_id, Q2, "b"))
    assert sm.part_family_presence(ids, answers, ctrl.subsystem_id) == sm.PART_FAMILY_SOME_RECORDED
    assert sm.part_family_presence(ids, (), ctrl.subsystem_id) == sm.PART_FAMILY_NONE_RECORDED
    assert sm.part_family_presence([Q1], answers, ctrl.subsystem_id) == sm.PART_FAMILY_ALL_RECORDED
    mech, elec = _pair()
    with pytest.raises(sm.PartAnswerError):                      # a root-domain question id under the part
        sm.validate_part_answers([sm.PartAnswer(ctrl.subsystem_id, "mechanical:MECHANISM_COMPLETENESS:Q1", "a")],
                                 (mech, elec, ctrl))
    with pytest.raises(sm.PartAnswerError):                      # a required part never carries part answers
        sm.validate_part_answers([sm.PartAnswer(mech.subsystem_id, Q1, "a")], (mech, elec, ctrl))
    # nothing in the owner reaches for a gap, a gap state or a progression owner
    tree = ast.parse(open(os.path.join(_ROOT, "engine", "subsystem_model.py"), encoding="utf-8").read())
    imported = {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
    assert imported <= {"engine", "engine.idea_state", "dataclasses", "typing"}, imported
