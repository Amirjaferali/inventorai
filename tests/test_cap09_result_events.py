"""Stage 19 / CAP-09 — Result Event Slice 1.

The inventor records, in their own words, what actually happened when they
performed ONE current canonical Section-11 experiment. APPEND-ONLY events:
every separately reported execution is an independent root carrying its
frozen CONTEXT AT RECORDING; a correction supersedes the current head of one
chain; history is never rewritten. OWNER-STATED / UNVALIDATED: no outcome,
no validation, no readiness / progression / maturity / gap effect.
"""
import html
import re
import sqlite3

import pytest

import web.app as webapp
from web.app import app, SESSION_STORE
from web.ui_text import text
from engine import experiment_result as er
from engine.record_store import (
    RecordStoreConnectionUnsafe, ResultEventConflict, ResultEventRejected,
    ResultEventsCorrupt, SqliteRecordStore, RESULT_EVENT_EXACT_REPLAY)
from tests.csrf_client import csrf_client
from tests.test_stage19_durable_success_criteria import (
    ELEC_DISPLACING_ANSWER, PREFIX, _journey, _restart, _live_ids, _answer,
    _criteria_page, _db_path, _progression_snapshot, _CommitThenRaise,
    _CommitAndRollbackFail)

OBS = "The lid opened in about 3 seconds, twice out of three tries."
OBS2 = "On a retest the lid opened every time."
TABLE = "prototype_test_results"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return csrf_client(app)


def _store():
    return webapp._get_store()


def _page(client, sid):
    r = client.get("/session/%s/success-criteria" % sid)
    assert r.status_code == 200
    return r.get_data(as_text=True)


def _forms(raw):
    """Every Result form on the page as a dict of its hidden fields."""
    forms = []
    for body in re.findall(r'<form method="POST" action="[^"]*experiment-result"[^>]*>(.*?)</form>',
                           raw, re.S):
        fields = dict(re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]*)"', body))
        forms.append({k: html.unescape(v) for k, v in fields.items()})
    return forms


def _record_form(client, sid, eid):
    [form] = [f for f in _forms(_page(client, sid))
              if f.get("experiment_id") == eid and "supersedes" not in f]
    return form


def _correct_form(client, sid, head_id):
    [form] = [f for f in _forms(_page(client, sid)) if f.get("supersedes") == head_id]
    return form


def _post(client, sid, form, result_text):
    data = dict(form)
    data["result_text"] = result_text
    return client.post("/session/%s/experiment-result" % sid, data=data)


def _events(sid):
    return _store().load_result_events(sid)


def _rows(sid):
    con = sqlite3.connect(_db_path())
    try:
        return con.execute("SELECT * FROM %s WHERE project_id = ? ORDER BY result_seq"
                           % TABLE, (sid,)).fetchall()
    finally:
        con.close()


def _ctx(title="Experiment", **kw):
    return er.ResultContext(experiment_title=title, **kw)


def _project(client):
    sid = _journey(client)
    return sid, _live_ids(sid)


# ==========================================================================
# 1-3 roots: first result, retest, identical text retest
# ==========================================================================
def test_first_result_is_one_root_event(client):
    sid, ids = _project(client)
    r = _post(client, sid, _record_form(client, sid, ids[0]), "  " + OBS + "  ")
    assert r.status_code == 200
    assert webapp._RESULT_SAVED_MESSAGE in html.unescape(r.get_data(as_text=True))
    [ev] = _events(sid)
    assert ev.experiment_id == ids[0] and ev.result_text == OBS
    assert ev.supersedes_result_event_id is None and ev.context is not None
    assert er.is_valid_result_event_id(ev.result_event_id)
    assert OBS not in ev.result_event_id and ids[0] not in ev.result_event_id


def test_a_retest_is_a_second_independent_root(client):
    sid, ids = _project(client)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS2)
    first, second = _events(sid)
    assert first.supersedes_result_event_id is None
    assert second.supersedes_result_event_id is None            # never supersedes
    assert [c["root"].result_event_id for c in er.result_chains(_events(sid), ids[0])] \
        == [first.result_event_id, second.result_event_id]


def test_identical_text_from_a_new_form_is_a_real_retest(client):
    sid, ids = _project(client)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    events = _events(sid)
    assert len(events) == 2 and events[0].result_event_id != events[1].result_event_id


# ==========================================================================
# 4-8 corrections: successor, fork, non-head, cross-project, cross-experiment
# ==========================================================================
def test_a_correction_appends_a_successor_and_keeps_the_old_text(client):
    sid, ids = _project(client)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    [root] = _events(sid)
    r = _post(client, sid, _correct_form(client, sid, root.result_event_id), OBS2)
    assert r.status_code == 200
    root2, fix = _events(sid)
    assert root2 == root                                          # never rewritten
    assert fix.supersedes_result_event_id == root.result_event_id
    assert fix.context is None and fix.experiment_id == ids[0]
    [chain] = er.result_chains(_events(sid), ids[0])
    assert chain["head"] == fix and chain["root"] == root
    page = html.unescape(_page(client, sid))
    assert OBS2 in page and OBS in page                           # history kept
    assert text("UI_R_EARLIER", "en") in page


def test_a_successor_fork_and_a_non_head_correction_are_refused(client):
    sid, ids = _project(client)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    [root] = _events(sid)
    stale_form = _correct_form(client, sid, root.result_event_id)
    _post(client, sid, _correct_form(client, sid, root.result_event_id), OBS2)
    r = _post(client, sid, stale_form, "Another correction")      # root is no head now
    assert r.status_code == 400
    assert webapp._RESULT_STALE_TARGET_MESSAGE in html.unescape(r.get_data(as_text=True))
    assert len(_events(sid)) == 2
    store = _store()
    with pytest.raises(ResultEventRejected):
        store.append_result_event(sid, er.recorded_correction(ids[0], "x", root.result_event_id),
                                  "k-fork")
    con = sqlite3.connect(_db_path())                              # database backstop
    try:
        row = list(_rows(sid)[1])
        row[1], row[2], row[6] = 5, er.new_result_event_id(), "raw-key"
        with pytest.raises(sqlite3.IntegrityError):
            con.execute("INSERT INTO %s VALUES (%s)" % (TABLE, ",".join("?" * len(row))), row)
    finally:
        con.close()


def test_cross_project_and_cross_experiment_targets_are_refused(client):
    sid, ids = _project(client)
    other, other_ids = _project(client)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    _post(client, other, _record_form(client, other, other_ids[0]), OBS)
    [mine] = _events(sid)
    [theirs] = _events(other)
    store = _store()
    with pytest.raises(ResultEventRejected):                      # another project's event
        store.append_result_event(sid, er.recorded_correction(
            ids[0], "x", theirs.result_event_id), "k1")
    with pytest.raises(ResultEventRejected):                      # another experiment
        store.append_result_event(sid, er.recorded_correction(
            ids[1], "x", mine.result_event_id), "k2")
    form = _correct_form(client, sid, mine.result_event_id)
    form["experiment_id"] = ids[1]
    assert _post(client, sid, form, "x").status_code == 400
    assert len(_events(sid)) == 1 and len(_events(other)) == 1


# ==========================================================================
# 9-10 retry identity
# ==========================================================================
def test_an_exact_retry_creates_no_duplicate(client):
    sid, ids = _project(client)
    form = _record_form(client, sid, ids[0])
    for _ in range(3):
        r = _post(client, sid, form, OBS)
        assert r.status_code == 200
    assert len(_events(sid)) == 1
    _restart()
    assert _post(client, sid, form, OBS).status_code == 200      # after a restart too
    assert len(_events(sid)) == 1


def test_the_same_identity_with_a_changed_payload_fails_closed(client):
    sid, ids = _project(client)
    form = _record_form(client, sid, ids[0])
    _post(client, sid, form, OBS)
    r = _post(client, sid, form, OBS2)
    assert r.status_code == 400
    assert webapp._RESULT_NOT_SAVED_MESSAGE in html.unescape(r.get_data(as_text=True))
    other = dict(form, experiment_id=ids[1])
    assert _post(client, sid, other, OBS).status_code == 400
    assert [e.result_text for e in _events(sid)] == [OBS]
    [ev] = _events(sid)
    with pytest.raises(ResultEventConflict):
        _store().append_result_event(sid, er.recorded_root(ids[0], OBS2, _ctx()),
                                     webapp._result_action_key(sid, form["result_submission"][:32]))


def test_a_forged_or_missing_submission_identity_saves_nothing(client):
    sid, ids = _project(client)
    form = _record_form(client, sid, ids[0])
    for bad in ("", "0" * 32 + ".forged", form["result_submission"][:-2] + "zz"):
        assert _post(client, sid, dict(form, result_submission=bad), OBS).status_code == 400
    assert _events(sid) == ()
    client_ids = [f["result_submission"] for f in _forms(_page(client, sid))]
    assert len(set(client_ids)) == len(client_ids)                # one per form


def test_committed_but_unconfirmed_resolves_saved_and_unresolved_stays_unknown(client):
    sid, ids = _project(client)
    form = _record_form(client, sid, ids[0])
    store = _store()
    real = store._conn
    store._conn = _CommitThenRaise(real)
    try:
        r = _post(client, sid, form, OBS)
    finally:
        store._conn = real
    assert r.status_code == 200 and len(_events(sid)) == 1
    assert webapp._RESULT_SAVED_MESSAGE in html.unescape(r.get_data(as_text=True))
    form2 = _record_form(client, sid, ids[1])
    store._conn = _CommitAndRollbackFail(real)
    try:
        r = _post(client, sid, form2, OBS2)
    finally:
        store._conn = real
    try:
        assert r.status_code == 503
        body = html.unescape(r.get_data(as_text=True))
        assert webapp._RESULT_UNKNOWN_MESSAGE in body
        assert webapp._RESULT_SAVED_MESSAGE not in body
        with pytest.raises(RecordStoreConnectionUnsafe):
            store.load_result_events(sid)
    finally:
        real.close()
        webapp._STORE = None
    assert len(_events(sid)) == 1                                  # nothing half-written
    assert _post(client, sid, form2, OBS2).status_code == 200     # the same retry resolves
    assert len(_events(sid)) == 2


# ==========================================================================
# 11-12 frozen context
# ==========================================================================
def test_context_is_frozen_at_first_recording_and_never_rewritten(client):
    sid, ids = _project(client)
    eid = ids[0]
    client.post("/session/%s/success-criteria" % sid,
                data={PREFIX + eid: "Opens within 5 seconds", "method__" + eid: "Stopwatch"})
    _post(client, sid, _record_form(client, sid, eid), OBS)
    [root] = _events(sid)
    assert root.context.success_criterion == "Opens within 5 seconds"
    assert root.context.measurement_method == "Stopwatch"
    assert root.context.test_hypothesis is None                   # explicit absence
    assert root.context.experiment_title
    client.post("/session/%s/success-criteria" % sid,
                data={PREFIX + eid: "Opens within 1 second", "method__" + eid: ""})
    _post(client, sid, _correct_form(client, sid, root.result_event_id), OBS2)
    root2, fix = _events(sid)
    assert root2.context == root.context                          # history untouched
    assert fix.context is None                                    # a correction adds none
    page = html.unescape(_page(client, sid))
    assert "Opens within 5 seconds" in page and text("UI_R_CONTEXT", "en") in page
    _post(client, sid, _record_form(client, sid, eid), "A later execution.")
    assert _events(sid)[2].context.success_criterion == "Opens within 1 second"
    assert _events(sid)[2].context.measurement_method is None


# ==========================================================================
# 13-15 currentness, stale history, cold load
# ==========================================================================
def test_a_new_root_needs_a_current_experiment_and_stale_history_is_kept(client):
    sid, ids = _project(client)
    claim = [i for i in ids if "_reasoned_leading_claim_" in i][0]
    _post(client, sid, _record_form(client, sid, claim), OBS)
    stale_record = _record_form(client, sid, claim)
    [root] = _events(sid)
    stale_fix = _correct_form(client, sid, root.result_event_id)
    _answer(client, sid, ELEC_DISPLACING_ANSWER)
    assert claim not in _live_ids(sid)
    r = _post(client, sid, stale_record, OBS2)
    assert r.status_code == 400
    assert webapp._RESULT_NOT_CURRENT_MESSAGE in html.unescape(r.get_data(as_text=True))
    assert _post(client, sid, stale_fix, OBS2).status_code == 400
    assert _events(sid) == (root,)                                 # preserved, unchanged
    page = html.unescape(_page(client, sid))
    assert text("UI_R_STALE", "en") in page and OBS in page
    assert all(f.get("experiment_id") != claim for f in _forms(page))   # never remapped
    bogus = dict(_record_form(client, sid, ids[0]), experiment_id="exp_v1_unknown_" + "a" * 32)
    assert _post(client, sid, bogus, OBS).status_code == 400


def test_cold_load_and_restart_preserve_identity_and_history(client):
    sid, ids = _project(client)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    [root] = _events(sid)
    _post(client, sid, _correct_form(client, sid, root.result_event_id), OBS2)
    before = _events(sid)
    _restart()
    assert _events(sid) == before
    page = html.unescape(_page(client, sid))
    assert OBS2 in page and OBS in page
    assert root.result_event_id not in re.sub(r"<[^>]+>", " ", page)   # id never shown


def test_corrupt_history_fails_the_result_surface_closed_only(client):
    sid, ids = _project(client)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    con = sqlite3.connect(_db_path())
    try:
        con.execute("PRAGMA ignore_check_constraints = ON")
        con.execute("UPDATE %s SET result_text = '  padded  ' WHERE project_id = ?" % TABLE, (sid,))
        con.commit()
    finally:
        con.close()
    with pytest.raises(ResultEventsCorrupt):
        _store().load_result_events(sid)
    page = html.unescape(_page(client, sid))
    assert text("UI_R_UNAVAILABLE", "en") in page                  # Result block closed
    assert 'name="%s' % PREFIX in page                            # planning form still works
    assert client.get("/session/%s" % sid).status_code == 200     # progression unaffected


def test_migration_is_additive_and_idempotent(tmp_path):
    path = str(tmp_path / "r.db")
    SqliteRecordStore(path).close()
    SqliteRecordStore(path).close()
    con = sqlite3.connect(path)
    try:
        cols = [r[1] for r in con.execute("PRAGMA table_info(%s)" % TABLE)]
    finally:
        con.close()
    for banned in ("outcome", "status", "validation", "quality", "readiness",
                   "confidence", "score", "pass", "fail"):
        assert not any(banned in c for c in cols), banned
    assert "recorded_at" in cols and "supersedes_result_event_id" in cols


# ==========================================================================
# 16-17 no side effects, no judgement
# ==========================================================================
def test_recording_results_changes_no_other_project_truth(client):
    sid, ids = _project(client)
    state = SESSION_STORE[sid]["state"]
    before = (len(state.assertions),
              [(r.record_id, getattr(r, "validation_status", None), getattr(r, "quality", None),
                getattr(r, "provenance", None)) for r in state.assertions],
              _progression_snapshot(sid))
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    [root] = _events(sid)
    _post(client, sid, _correct_form(client, sid, root.result_event_id), OBS2)
    state = SESSION_STORE[sid]["state"]
    after = (len(state.assertions),
             [(r.record_id, getattr(r, "validation_status", None), getattr(r, "quality", None),
               getattr(r, "provenance", None)) for r in state.assertions],
             _progression_snapshot(sid))
    assert before == after
    from engine.readiness_snapshot import readiness_snapshot
    assert readiness_snapshot(state, ())["rows"][0]["verified_contexts"] == 0


def test_no_pass_fail_judgement_is_generated(client):
    sid, ids = _project(client)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    page = html.unescape(_page(client, sid))
    section = page[page.index(text("UI_R_HEADING", "en")):]
    visible = re.sub(r"<[^>]+>", " ", section)
    for word in ("PASSED", "FAILED", "PARTIAL", "INCONCLUSIVE", "Verified", "validated",
                 "Criterion met", "confirmed"):
        assert word not in visible, word
    assert text("UI_R_LABEL", "en") in visible
    for key in ("UI_R_HEADING", "UI_R_LABEL", "UI_R_RECORD", "UI_R_CORRECT", "UI_R_CONTEXT",
                "UI_R_UNAVAILABLE", "UI_R_STALE", "UI_R_MSG_SAVED", "UI_R_MSG_UNKNOWN"):
        assert text(key, "en") != text(key, "ar")
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    arabic = html.unescape(_page(client, sid))
    assert text("UI_R_LABEL", "ar") in arabic and OBS in arabic


def test_history_validation_refuses_malformed_chains():
    ctx = _ctx()
    root = er.recorded_root("exp_v1_a_" + "1" * 8, "one", ctx)
    fix = er.recorded_correction(root.experiment_id, "two", root.result_event_id)
    assert er.validate_result_history([root, fix]) == (root, fix)
    for bad in ([fix], [root, fix, er.recorded_correction(root.experiment_id, "3",
                                                         root.result_event_id)],
                [root, er.recorded_correction("exp_v1_b_" + "2" * 8, "x", root.result_event_id)]):
        with pytest.raises(er.ResultEventError):
            er.validate_result_history(bad)
    with pytest.raises(er.ResultEventError):
        er.recorded_root(root.experiment_id, "x", None)            # a root needs context
    for text_value in ("", " x", "a\x00b", "x" * 1001):
        with pytest.raises(er.ResultEventError):
            er.recorded_root(root.experiment_id, text_value, ctx)
