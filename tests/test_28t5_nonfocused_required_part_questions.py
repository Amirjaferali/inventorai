"""28-T5-NONFOCUSED-REQUIRED-PART-QUESTIONS-SAFETY-01 — governed MECHANISM_COMPLETENESS / BOUNDARY_AMBIGUITY
questions for the REQUIRED part that is NOT the initial analysis focus, with part-local inventor-stated safety
signals.

What is pinned:
- the exact durable non-focused required part is a question part in BOTH focus directions; the focused required
  part, an unknown, stale or foreign id is refused (page, route and store, inside the write transaction);
- the part's own pack MC / BA questions are served verbatim in pack order; PHYSICAL_FEASIBILITY never is (route
  AND store);
- save / edit / clear / reload keep the existing current-value guarantees (atomic delta, confirm-by-reload);
- part-local safety signals come from the SafetySignal owner, from COMMITTED answers only, each answer on its own,
  under the part's governed family; unavailable coverage never reads as a clean result;
- the optional control-loop page, its eligibility and its safety exclusion, root SafetySignal derivation, root
  gaps / progression / readiness, the report / PDF (beyond the root-only coverage note) and the Structured Export
  are unchanged.
"""
import html as _html
import json
import os
import re
import sqlite3

import pytest

import web.app as appmod
from engine import safety_signal as ss
from engine import subsystem_model as sm
from engine.domain_rules import get_domain_questions
from engine.record_store import PartAnswerRejected, PartAnswersCorrupt, SqliteRecordStore
from engine.safety_signal import derive_inventor_stated_safety_signals, derive_part_safety_signals
from tests.test_stage15_integrated_invention_entry import (
    ELEC, MECH, TIE_IDEA, _compose, _contract, _created, _live, _pair, _pdf_source, _ri)
from tests.test_stage28_control_loop_optional_part_slice1 import (  # noqa: F401  (fixtures)
    CL, _rows, _three_part_project, client, part_eligible)
from tests.test_stage28_control_loop_optional_part_slice2 import (
    _all_table_counts, _answers_rows, _root_snapshot)
from tests.test_stage15_integration_closure import _login
from web import ui_text

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
MC, BA, PF = "MECHANISM_COMPLETENESS", "BOUNDARY_AMBIGUITY", "PHYSICAL_FEASIBILITY"
OTHER = {MECH: ELEC, ELEC: MECH}
MECH_HAZARD = "If the guard comes loose, fingers could be caught in the rotating parts and crushed."
ELEC_HAZARD = "If protection fails, the high voltage could cause a fire."
HAZARD = {MECH: MECH_HAZARD, ELEC: ELEC_HAZARD}
TITLE = {MECH: "UI_PQR_TITLE_MECH", ELEC: "UI_PQR_TITLE_ELEC"}


def _text(resp):
    return _html.unescape(resp.get_data(as_text=True))


def _pack_questions(domain, gap_type):
    with open(os.path.join(_ROOT, "domains", domain, "domain.json"), encoding="utf-8") as fh:
        pack = json.load(fh)
    for mapping in pack["gap_type_mappings"]:
        if mapping["gap_type_id"] == gap_type:
            return [(q["question_id"], q["text"]) for q in mapping["questions"]]
    return None


def _ids(domain):
    return [qid for g in (MC, BA) for qid, _t in _pack_questions(domain, g)]


def _two_part(c, focus=MECH):
    sid = _created(_compose(c, TIE_IDEA, focus=focus))
    assert [s.domain for s in _live(sid).subsystems] == [MECH, ELEC]
    return sid


def _part(sid, domain):
    return next(s.subsystem_id for s in appmod._get_store().load_project_subsystems(sid) if s.domain == domain)


def _url(sid, part_id=None):
    base = "/session/%s/part-questions" % sid
    return base if part_id is None else base + "?part=" + part_id


def _form(c, sid, part_id):
    raw = c.get(_url(sid, part_id)).get_data(as_text=True)
    fields = {"part_id": _html.unescape(re.search(r'name="part_id" value="([^"]*)"', raw).group(1))}
    for name, value in re.findall(r'<textarea[^>]*name="(part_answer__[^"]+)"[^>]*>([^<]*)</textarea>', raw, re.S):
        fields[_html.unescape(name)] = _html.unescape(value)
    for name, value in re.findall(r'name="(part_base__[^"]+)" value="([^"]*)"', raw):
        fields[_html.unescape(name)] = _html.unescape(value)
    return fields


def _save(c, sid, part_id, answers, form=None, post_part=None):
    data = dict(form if form is not None else _form(c, sid, part_id))
    for qid, text in answers.items():
        data["part_answer__" + qid] = text
    return c.post(_url(sid, part_id if post_part is None else post_part), data=data)


def _rows_for(sid, part_id):
    return [(q, t) for s, q, t in _answers_rows(sid) if s == part_id]


def _store(tmp_path, name="s.db"):
    return SqliteRecordStore(str(tmp_path / name))


def _stored(store, focus=MECH, idea_id="i-28t5", with_ctrl=False):
    mech, elec = _pair()
    parts = (mech, elec)
    if with_ctrl:
        parts += (sm.declared_subsystem(CL, "Thermostat logic", "Compares the temperature with the target"),)
    pid = store.create_project(_contract(idea_id), reconstruction_inputs=_ri(domain=focus), subsystems=parts)
    return (pid,) + parts


# ==========================================================================
# 1. Model: the question parts of a durable composition
# ==========================================================================
def test_m01_nonfocused_required_part_is_resolved_by_durable_domain_against_the_focus():
    mech, elec = _pair()
    ctrl = sm.declared_subsystem(CL, "Loop", "Keeps the level")
    assert sm.nonfocused_required_part((mech, elec), MECH) is elec
    assert sm.nonfocused_required_part((mech, elec), ELEC) is mech
    assert sm.nonfocused_required_part((mech, elec, ctrl), ELEC) is mech
    for focus in (None, "", CL, "software", "Mechanical"):
        assert sm.nonfocused_required_part((mech, elec), focus) is None
    assert sm.nonfocused_required_part((), MECH) is None
    assert sm.question_parts((mech, elec, ctrl), MECH) == (elec, ctrl)
    assert sm.question_parts((mech, elec), ELEC) == (mech,)
    assert sm.question_parts((), MECH) == ()


def test_m02_question_part_owner_accepts_exactly_the_nonfocused_and_optional_parts():
    mech, elec = _pair()
    ctrl = sm.declared_subsystem(CL, "Loop", "Keeps the level")
    comp = (mech, elec, ctrl)
    assert sm.part_question_owner(comp, elec.subsystem_id, MECH) is elec
    assert sm.part_question_owner(comp, ctrl.subsystem_id, MECH) is ctrl
    for bad in (mech.subsystem_id, "sub-" + "0" * 32, "", None):
        with pytest.raises(sm.PartAnswerError):
            sm.part_question_owner(comp, bad, MECH)
    # without the durable focus the original contract holds: the optional part only
    assert sm.part_question_owner(comp, ctrl.subsystem_id) is ctrl
    with pytest.raises(sm.PartAnswerError):
        sm.part_question_owner(comp, elec.subsystem_id)


def test_m03_the_part_question_families_exclude_physical_feasibility_at_the_model():
    _mech, elec = _pair()
    sm.check_part_answer_target(elec, "electronics_electrical:MECHANISM_COMPLETENESS:Q1")
    sm.check_part_answer_target(elec, "electronics_electrical:BOUNDARY_AMBIGUITY:Q9")
    for bad in ("electronics_electrical:PHYSICAL_FEASIBILITY:Q1", "mechanical:MECHANISM_COMPLETENESS:Q1",
                "electronics_electrical:NOT_A_FAMILY:Q1"):
        with pytest.raises(sm.PartAnswerError):
            sm.check_part_answer_target(elec, bad)


# ==========================================================================
# 2. Store: durable focus and target re-validated inside the transaction
# ==========================================================================
@pytest.mark.parametrize("focus", [MECH, ELEC])
def test_s01_store_records_and_reloads_the_nonfocused_part_and_refuses_the_focused_one(tmp_path, focus):
    store = _store(tmp_path)
    pid, mech, elec = _stored(store, focus=focus)
    nonfocused, focused = (elec, mech) if focus == MECH else (mech, elec)
    qid = _ids(nonfocused.domain)[0]
    store.apply_part_answer_delta(pid, nonfocused.subsystem_id, {qid: "It turns the arm"})
    assert [(a.question_id, a.answer_text) for a in store.load_part_answers(pid, nonfocused.subsystem_id)] \
        == [(qid, "It turns the arm")]
    assert store.load_part_question_scope(pid) == ((mech, elec), focus)
    for target, question in ((focused.subsystem_id, _ids(focused.domain)[0]),       # the focused part
                             ("sub-" + "1" * 32, qid),                               # unknown id
                             (nonfocused.subsystem_id, _ids(focused.domain)[0]),     # the other pack's question
                             (nonfocused.subsystem_id, nonfocused.domain + ":PHYSICAL_FEASIBILITY:Q1")):
        with pytest.raises(PartAnswerRejected):
            store.apply_part_answer_delta(pid, target, {question: "x"})
    with pytest.raises(PartAnswerRejected):
        store.load_part_answers(pid, focused.subsystem_id)
    assert [a.answer_text for a in store.load_part_answers(pid, nonfocused.subsystem_id)] == ["It turns the arm"]


def test_s02_another_projects_part_is_never_a_question_part(tmp_path):
    store = _store(tmp_path)
    pid_a, _m_a, elec_a = _stored(store, idea_id="i-a")
    pid_b, _m_b, elec_b = _stored(store, idea_id="i-b")
    qid = _ids(ELEC)[0]
    with pytest.raises(PartAnswerRejected):
        store.apply_part_answer_delta(pid_a, elec_b.subsystem_id, {qid: "x"})
    store.apply_part_answer_delta(pid_a, elec_a.subsystem_id, {qid: "ours"})
    assert store.load_part_answers(pid_b, elec_b.subsystem_id) == ()


def test_s03_a_whole_delta_rolls_back_when_one_item_is_refused(tmp_path):
    store = _store(tmp_path)
    pid, _mech, elec = _stored(store)
    good, bad = _ids(ELEC)[0], "electronics_electrical:PHYSICAL_FEASIBILITY:Q1"
    store.apply_part_answer_delta(pid, elec.subsystem_id, {good: "before"})
    with pytest.raises(PartAnswerRejected):
        store.apply_part_answer_delta(pid, elec.subsystem_id, {good: "after", bad: "x"})
    assert [a.answer_text for a in store.load_part_answers(pid, elec.subsystem_id)] == ["before"]


def test_s04_a_durable_answer_on_the_focused_part_fails_the_collection_closed(tmp_path):
    store = _store(tmp_path, "c.db")
    pid, mech, elec = _stored(store)
    store.apply_part_answer_delta(pid, elec.subsystem_id, {_ids(ELEC)[0]: "ok"})
    conn = sqlite3.connect(str(tmp_path / "c.db"))
    conn.execute("INSERT INTO subsystem_part_answers (project_id, subsystem_id, question_id, answer_text) "
                 "VALUES (?, ?, ?, ?)", (pid, mech.subsystem_id, _ids(MECH)[0], "smuggled"))
    conn.commit()
    conn.close()
    reopened = SqliteRecordStore(str(tmp_path / "c.db"))
    with pytest.raises(PartAnswersCorrupt):
        reopened.load_part_answers(pid, elec.subsystem_id)
    with pytest.raises(PartAnswersCorrupt):
        reopened.apply_part_answer_delta(pid, elec.subsystem_id, {_ids(ELEC)[0]: "new"})


def test_s05_the_optional_part_keeps_its_original_store_contract(tmp_path):
    store = _store(tmp_path)
    pid, _mech, elec, ctrl = _stored(store, with_ctrl=True)
    store.apply_part_answer_delta(pid, ctrl.subsystem_id, {"control_loop:MECHANISM_COMPLETENESS:Q1": "Level"})
    store.apply_part_answer_delta(pid, elec.subsystem_id, {_ids(ELEC)[0]: "Drives"})
    assert [a.answer_text for a in store.load_part_answers(pid, ctrl.subsystem_id)] == ["Level"]
    assert [a.answer_text for a in store.load_part_answers(pid, elec.subsystem_id)] == ["Drives"]


# ==========================================================================
# 3. Route: both focus directions, verbatim MC / BA, explicit identity
# ==========================================================================
@pytest.mark.parametrize("focus", [MECH, ELEC])
def test_r01_page_serves_the_nonfocused_parts_governed_questions_verbatim(client, focus):
    sid = _two_part(client, focus)
    other = OTHER[focus]
    pid = _part(sid, other)
    session = client.get("/session/%s" % sid).get_data(as_text=True)
    assert ('href="/session/%s/part-questions?part=%s"' % (sid, pid)) in session
    assert "part-questions?part=%s" % _part(sid, focus) not in session   # the focused part is never linked
    assert session.count("/part-questions") == 1
    r = client.get(_url(sid, pid))
    raw = _text(r)
    assert r.status_code == 200 and ui_text.text(TITLE[other], "en") in raw
    served = re.findall(r'data-pq-question>([^<]*)</span>', r.get_data(as_text=True))
    expected = [t for g in (MC, BA) for _q, t in _pack_questions(other, g)]
    assert [_html.unescape(x) for x in served] == expected
    assert [q for g in (MC, BA) for q, _t in get_domain_questions(other, g)] == _ids(other)
    for _q, text in _pack_questions(other, PF):
        assert text not in raw                                     # PHYSICAL_FEASIBILITY never served
    assert 'name="part_id" value="%s"' % pid in raw
    assert 'action="/session/%s/part-questions?part=%s"' % (sid, pid) in raw
    assert ui_text.text("UI_PQ_TITLE", "en") not in raw            # never the control-loop wording


@pytest.mark.parametrize("focus", [MECH, ELEC])
def test_r02_save_edit_clear_reload_touch_only_that_parts_answers(client, focus):
    sid = _two_part(client, focus)
    other = OTHER[focus]
    pid = _part(sid, other)
    q1, q2 = _ids(other)[0], _ids(other)[-1]
    before_root, before_tables = _root_snapshot(sid), _all_table_counts()
    r = _save(client, sid, pid, {q1: "  It turns the arm  ", q2: "It does not lift people"})
    assert r.status_code == 200 and ui_text.text("UI_PQ_MSG_SAVED", "en") in _text(r)
    assert _rows_for(sid, pid) == sorted([(q1, "It turns the arm"), (q2, "It does not lift people")])
    _save(client, sid, pid, {q1: "It rotates the arm"})
    _save(client, sid, pid, {q2: ""})                                # clear
    assert _rows_for(sid, pid) == [(q1, "It rotates the arm")]
    reload = _text(client.get(_url(sid, pid)))
    assert "It rotates the arm" in reload and "It does not lift people" not in reload
    assert _root_snapshot(sid) == before_root and _all_table_counts() == before_tables
    assert _rows("SELECT confirmed_domain FROM projects WHERE project_id = ?", (sid,)) == [(focus,)]


def test_r03_focused_unknown_stale_and_foreign_targets_are_refused(client):
    sid = _two_part(client, MECH)
    elec, mech = _part(sid, ELEC), _part(sid, MECH)
    other_sid = _two_part(client, MECH)
    foreign = _part(other_sid, ELEC)
    not_offered = ui_text.text("UI_PQ_MSG_PART_NOT_OFFERED", "en")
    for bad in (mech, "sub-" + "2" * 32, foreign, ""):
        r = client.get(_url(sid, bad))
        assert r.status_code == 404 and not_offered in _text(r) and "part_answer__" not in _text(r)
        assert ui_text.text("UI_PQ_TITLE", "en") not in _text(r)
    form = _form(client, sid, elec)
    q = _ids(ELEC)[0]
    # the focused part named in the URL
    assert _save(client, sid, elec, {q: "x"}, form=form, post_part=mech).status_code == 404
    # the URL names the non-focused part but the form names another part
    r = _save(client, sid, elec, {q: "x"}, form=dict(form, part_id=mech))
    assert r.status_code == 400 and ui_text.text("UI_PQ_MSG_UNKNOWN_QUESTION", "en") in _text(r)
    # no URL selection: the original optional-part page, which this project does not have
    assert client.post(_url(sid), data=dict(form, **{"part_answer__" + q: "x"})).status_code == 404
    # a PHYSICAL_FEASIBILITY question or a question of the focused pack is never accepted
    for qid in ("electronics_electrical:PHYSICAL_FEASIBILITY:Q1", _ids(MECH)[0]):
        r = _save(client, sid, elec, {}, form=dict(form, **{"part_answer__" + qid: "x", "part_base__" + qid: ""}))
        assert r.status_code == 400
    # a stale form: another tab saved first; an untouched field is never re-written
    first = _form(client, sid, elec)
    _save(client, sid, elec, {q: "From tab one"})
    r = _save(client, sid, elec, {_ids(ELEC)[1]: "From tab two"}, form=first)
    assert r.status_code == 200
    assert dict(_rows_for(sid, elec)) == {q: "From tab one", _ids(ELEC)[1]: "From tab two"}
    assert _rows_for(sid, mech) == [] and _answers_rows(other_sid) == []


def test_r04_confirm_by_reload_and_transaction_failures_keep_store_guarantees(client, monkeypatch):
    sid = _two_part(client, MECH)
    elec = _part(sid, ELEC)
    q = _ids(ELEC)[0]
    store = appmod._get_store()
    real = store.apply_part_answer_delta

    def commit_then_raise(*a, **k):
        real(*a, **k)
        raise sqlite3.OperationalError("injected: commit outcome uncertain")
    monkeypatch.setattr(store, "apply_part_answer_delta", commit_then_raise)
    r = _save(client, sid, elec, {q: "Drives the motor"})
    assert r.status_code == 200 and ui_text.text("UI_PQ_MSG_SAVED", "en") in _text(r)

    def raise_only(*a, **k):
        raise sqlite3.OperationalError("injected: nothing committed")
    monkeypatch.setattr(store, "apply_part_answer_delta", raise_only)
    r = _save(client, sid, elec, {q: "Switches the motor"})
    assert r.status_code == 503 and ui_text.text("UI_PQ_MSG_NOT_SAVED", "en") in _text(r)
    assert _rows_for(sid, elec) == [(q, "Drives the motor")]


def test_r05_the_route_is_guarded_by_project_authorization(client):
    _login(client, "t5-owner@example.com")
    sid = _two_part(client, MECH)
    elec = _part(sid, ELEC)
    form = _form(client, sid, elec)
    from tests.csrf_client import csrf_client
    with csrf_client(appmod.app) as other:
        _login(other, "t5-other@example.com")
        assert other.get(_url(sid, elec)).status_code in (302, 403, 404)
        r = other.post(_url(sid, elec), data=dict(form, **{"part_answer__" + _ids(ELEC)[0]: "intruder"}))
        assert r.status_code in (302, 403, 404)
    assert _rows_for(sid, elec) == []


def test_r06_control_loop_page_and_its_safety_exclusion_are_unchanged(client, part_eligible):
    sid = _three_part_project(client)
    ctrl, elec = _part(sid, CL), _part(sid, ELEC)
    legacy = _text(client.get(_url(sid)))
    assert ui_text.text("UI_PQ_TITLE", "en") in legacy and ui_text.text("UI_PQ_SAFETY_SCOPE", "en") in legacy
    assert "data-pq-safety>" not in legacy and 'name="part_id" value="%s"' % ctrl in legacy
    assert 'action="/session/%s/part-questions"' % sid in legacy           # the original form action
    explicit = _text(client.get(_url(sid, ctrl)))                           # explicit identity, same page kind
    assert ui_text.text("UI_PQ_TITLE", "en") in explicit and "data-pq-safety>" not in explicit
    # a control-loop hazard is never read for safety; the required part's is, on its own page only
    ctrl_form = _form(client, sid, ctrl)
    r = client.post(_url(sid), data=dict(ctrl_form, **{"part_answer__control_loop:MECHANISM_COMPLETENESS:Q1":
                                                        ELEC_HAZARD}))
    assert r.status_code == 200 and "data-pq-safety-signal" not in r.get_data(as_text=True)
    _save(client, sid, elec, {_ids(ELEC)[0]: ELEC_HAZARD})
    page = client.get(_url(sid, elec)).get_data(as_text=True)
    assert page.count("data-pq-safety-signal") == 1
    assert len(_answers_rows(sid)) == 2


# ==========================================================================
# 4. Part-local SafetySignal: committed answers, per answer, part family
# ==========================================================================
@pytest.mark.parametrize("focus", [MECH, ELEC])
def test_sf01_a_part_hazard_shows_on_the_part_page_only_and_root_signals_are_unchanged(client, focus):
    sid = _two_part(client, focus)
    other = OTHER[focus]
    pid = _part(sid, other)
    q = _ids(other)[1]
    root_before = derive_inventor_stated_safety_signals(_live(sid))
    report_before = client.get("/session/%s/deliverable" % sid).get_data(as_text=True)
    r = _save(client, sid, pid, {q: HAZARD[other]})
    page = r.get_data(as_text=True)
    assert page.count("data-pq-safety-signal") == 1
    signal = page.split("data-pq-safety-signal", 1)[1]
    assert _html.unescape(dict(_pack_questions(other, MC) + _pack_questions(other, BA))[q]) in _html.unescape(signal)
    assert HAZARD[other] in _html.unescape(signal)
    assert derive_inventor_stated_safety_signals(_live(sid)) == root_before
    report = client.get("/session/%s/deliverable" % sid).get_data(as_text=True)
    assert HAZARD[other] not in _html.unescape(report)
    strip = lambda raw: re.sub(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", "<ts>",  # noqa: E731
                               re.sub(r'name="csrf_token" value="[^"]*"', "", raw))
    assert strip(report) == strip(report_before)
    assert ui_text.text("UI_SS_PART_PAGE_SCOPE", "en") in _html.unescape(report)


def test_sf02_detection_uses_only_the_parts_own_governed_family(client):
    sid = _two_part(client, MECH)                    # the electrical part is outside the focus
    elec = _part(sid, ELEC)
    r = _save(client, sid, elec, {_ids(ELEC)[0]: MECH_HAZARD})
    assert "data-pq-safety-signal" not in r.get_data(as_text=True)
    assert "data-pq-safety-none" in r.get_data(as_text=True)


def test_sf03_separate_answers_never_combine_into_a_synthetic_hazard(client):
    sid = _two_part(client, MECH)
    elec = _part(sid, ELEC)
    q1, q2 = _ids(ELEC)[0], _ids(ELEC)[1]
    r = _save(client, sid, elec, {q1: "If protection fails.", q2: "The high voltage could cause a fire."})
    assert "data-pq-safety-signal" not in r.get_data(as_text=True)
    r = _save(client, sid, elec, {q1: "If protection fails. The high voltage could cause a fire.", q2: ""})
    assert r.get_data(as_text=True).count("data-pq-safety-signal") == 1   # same answer: adjacent pairing


def test_sf04_negation_suppresses_and_clear_or_edit_removes_the_signal(client):
    sid = _two_part(client, MECH)
    elec = _part(sid, ELEC)
    q = _ids(ELEC)[0]
    negated = "There is no risk of fire: if protection fails, the high voltage could cause a fire."
    assert "data-pq-safety-signal" not in _save(client, sid, elec, {q: negated}).get_data(as_text=True)
    assert "data-pq-safety-signal" in _save(client, sid, elec, {q: ELEC_HAZARD}).get_data(as_text=True)
    assert "data-pq-safety-signal" in client.get(_url(sid, elec)).get_data(as_text=True)      # reload
    assert "data-pq-safety-signal" not in _save(client, sid, elec, {q: "It switches a lamp"}).get_data(
        as_text=True)
    _save(client, sid, elec, {q: ELEC_HAZARD})
    cleared = _save(client, sid, elec, {q: ""}).get_data(as_text=True)
    assert "data-pq-safety-signal" not in cleared and "data-pq-safety-nothing" in cleared


def test_sf05_a_refused_draft_is_never_read_for_safety(client):
    sid = _two_part(client, MECH)
    elec = _part(sid, ELEC)
    form = _form(client, sid, elec)
    r = _save(client, sid, elec, {_ids(ELEC)[0]: ELEC_HAZARD + "x" * 1000}, form=form)
    assert r.status_code == 400 and "data-pq-safety-signal" not in r.get_data(as_text=True)
    assert "data-pq-safety-nothing" in r.get_data(as_text=True)


def test_sf06_unavailable_coverage_never_reads_as_a_clean_result(client, monkeypatch):
    sid = _two_part(client, MECH)
    elec = _part(sid, ELEC)
    _save(client, sid, elec, {_ids(ELEC)[0]: ELEC_HAZARD})

    def broken(*a, **k):
        raise ValueError("injected")
    monkeypatch.setattr(appmod._safety_signal, "derive_part_safety_signals", broken)
    raw = client.get(_url(sid, elec)).get_data(as_text=True)
    assert "data-pq-safety-unavailable" in raw
    for clean in ("data-pq-safety-none", "data-pq-safety-nothing", "data-pq-safety-signal"):
        assert clean not in raw
    assert ui_text.text("UI_PQR_SS_UNAVAILABLE", "en") in _html.unescape(raw)


def test_sf07_owner_unit_contract():
    q = "electronics_electrical:MECHANISM_COMPLETENESS:Q1"
    sigs = derive_part_safety_signals(ELEC, [(q, ELEC_HAZARD), ("electronics_electrical:BOUNDARY_AMBIGUITY:Q1",
                                                                ELEC_HAZARD)])
    assert len(sigs) == 1                                    # exact duplicate: the first answer wins
    sig = sigs[0]
    assert (sig.source, sig.domain_context, sig.provenance, sig.validation_status) == (
        ss.PART_SIGNAL_SOURCE_PREFIX + q, ELEC, ss.PROVENANCE_INVENTOR_STATED, ss.VALIDATION_REQUIRES_INDEPENDENT)
    assert derive_part_safety_signals(MECH, []) == ()
    for bad_domain in (None, "", CL, "software", "unknown"):
        with pytest.raises(ValueError):
            derive_part_safety_signals(bad_domain, [(q, ELEC_HAZARD)])
    for bad in ([(None, "x")], [("", "x")], [(q, None)]):
        with pytest.raises(ValueError):
            derive_part_safety_signals(ELEC, bad)


# ==========================================================================
# 5. No downstream effect; EN / AR
# ==========================================================================
def test_x01_no_state_gap_readiness_export_or_report_effect(client, monkeypatch):
    _login(client, "t5-x01@example.com")
    sid = _two_part(client, MECH)
    elec = _part(sid, ELEC)
    readiness_before = appmod._readiness_snapshot_context(sid, _live(sid))
    export_before = client.get("/account/projects/%s/export" % sid).get_data(as_text=True)
    pdf_before = _pdf_source(client, sid, monkeypatch)
    marker = "NonFocusedPartMarker28T5"
    _save(client, sid, elec, {_ids(ELEC)[0]: marker, _ids(ELEC)[-1]: ELEC_HAZARD})
    assert client.get("/account/projects/%s/export" % sid).get_data(as_text=True) == export_before
    assert appmod._readiness_snapshot_context(sid, _live(sid)) == readiness_before
    pdf = _pdf_source(client, sid, monkeypatch)
    strip = lambda raw: re.sub(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", "<ts>",  # noqa: E731
                               re.sub(r'name="csrf_token" value="[^"]*"', "", raw))
    assert strip(pdf) == strip(pdf_before) and marker not in pdf
    assert ui_text.text("UI_SS_PART_PAGE_SCOPE", "en") in _html.unescape(pdf)
    session = client.get("/session/%s" % sid).get_data(as_text=True)
    assert marker not in session
    state = _live(sid)
    for name in vars(state):
        assert "part_answer" not in name, name
    assert all(not isinstance(v, sm.PartAnswer) for v in vars(state).values())


def test_x02_single_domain_projects_carry_no_part_link_or_report_note(client):
    from tests.test_safe_question_routing_pf_q2 import ELEC_SEED, _start
    sid = _start(client, seed=ELEC_SEED, domain=ELEC)
    session = client.get("/session/%s" % sid).get_data(as_text=True)
    assert "part-questions" not in session
    report = _text(client.get("/session/%s/deliverable" % sid))
    assert ui_text.text("UI_SS_PART_PAGE_SCOPE", "en") not in report


@pytest.mark.parametrize("focus", [MECH, ELEC])
def test_x03_arabic_page_uses_arabic_copy_and_keeps_governed_questions_verbatim(client, focus):
    sid = _two_part(client, focus)
    other = OTHER[focus]
    pid = _part(sid, other)
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    _save(client, sid, pid, {_ids(other)[0]: HAZARD[other]})
    raw = client.get(_url(sid, pid)).get_data(as_text=True)
    text = _html.unescape(raw)
    for key in (TITLE[other], "UI_PQR_SS_TITLE", "UI_PQR_SS_LABEL", "UI_PQR_SS_CAUTION",
                "UI_PQR_SAFETY_SCOPE_" + ("MECH" if other == MECH else "ELEC")):
        assert ui_text.text(key, "ar") in text, key
    assert 'dir="rtl"' in raw
    first = _pack_questions(other, MC)[0][1]
    assert ('<span dir="ltr" lang="en" data-pq-question>%s</span>' % _html.escape(first, quote=False)) in raw \
        or first in text
    report = _text(client.get("/session/%s/deliverable" % sid))
    assert ui_text.text("UI_SS_PART_PAGE_SCOPE", "ar") in report


def test_x04_every_new_copy_key_is_bilingual():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_PQR_")] + [
        "UI_PQ_MSG_PART_NOT_OFFERED", "UI_SS_PART_PAGE_SCOPE"]
    assert len(keys) >= 25
    for k in keys:
        assert ui_text.UI_STRINGS[k]["en"].strip() and ui_text.UI_STRINGS[k]["ar"].strip(), k
        for word in ("certified", "compliant", "safe to use", "guarantee"):
            assert word not in ui_text.UI_STRINGS[k]["en"].lower(), (k, word)
