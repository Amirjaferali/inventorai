"""Stage 19 / CAP-09 SLICE-02 — durable user-written Measurement Method.

File-creation contract:
  Path: tests/test_stage19_measurement_method.py
  Purpose: prove that the inventor can record, for each EXISTING Section-11
    experiment, their OWN description of HOW they plan to measure or check it;
    that it is durable through the saved-project architecture in the same
    SQLite store (a narrowly typed sibling sidecar, never a widened
    ``prototype_plan_metadata``); that it is saved together with the success
    criteria as ONE atomic planning write whose uncertain outcome is resolved
    truthfully (SAVED / NOT SAVED / UNKNOWN, with the IR-01 unresolved-
    transaction rule); that stale, corrupt, isolated and missing-project cases
    stay distinct; and that it remains planning metadata only.
  Input contract: the live web app, the conftest per-test on-disk SQLite
    database, and REAL /start -> answer journeys (Electronics and Mechanical).
    A "restart" clears SESSION_STORE, closes the application store and drops the
    handle, so the next request reopens the SAME database file with a fresh
    store — the governed P4-2/PC1/PC2 convention.
  Output contract: pass/fail evidence only.
  Prohibited behaviors: no activation doubles; no fabricated results; the only
    doubles are named, bounded failure injections (documented inline).
"""
import copy
import dataclasses
import html
import sqlite3

import pytest

import web.app as webapp
from web.app import app, SESSION_STORE
from web.ui_text import text
from engine.record_store import (
    SqliteRecordStore, ProjectNotFound, RecordStoreConnectionUnsafe,
    MeasurementMethodCorrupt, MeasurementMethodInvalid, SuccessCriterionInvalid,
)
from engine.record_contract import ProjectRecordContract, assertion_to_dict
from engine.idea_state import IdeaState
from tests.csrf_client import csrf_client
from tests.test_stage19_durable_success_criteria import (
    ELEC_IDEA, ELEC_ANSWERS, ELEC_DISPLACING_ANSWER, MECH_IDEA, MECH_ANSWERS,
    PREFIX, _journey, _legacy_journey, _restart, _plan_items, _live_ids,
    _live_ids_after_restart, _answer, _adopt, _correct, _answered_record,
    _reopened_items, _criteria_page, _db_path, _durable, _report,
    _progression_snapshot, _no_writable_session, _completed_project,
    _CommitThenRaise, _CommitAndRollbackFail,
)

METHOD = "method__"
TABLE = "prototype_measurement_methods"
OUTCOME_UNKNOWN = webapp.SC_OUTCOME_UNKNOWN_MESSAGE
NOT_SAVED = webapp.SC_NOT_SAVED_MESSAGE
SAVED_NOT_SHOWN = webapp.SC_SAVED_NOT_SHOWN_MESSAGE
NOT_A_PROJECT = webapp.SC_NOT_SAVED_PROJECT_MESSAGE
UNAVAILABLE = webapp.SC_CRITERIA_UNAVAILABLE_MESSAGE
EID_SHAPE = "exp_v1_acknowledged_unknown_" + "d" * 32


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return csrf_client(app)


def _post_plan(client, sid, criteria=None, methods=None):
    data = {PREFIX + k: v for k, v in (criteria or {}).items()}
    data.update({METHOD + k: v for k, v in (methods or {}).items()})
    return client.post("/session/%s/success-criteria" % sid, data=data)


def _methods(sid):
    """The DURABLE measurement methods, read through the application store."""
    return dict(webapp._get_store().load_measurement_methods(sid))


def _raw_methods(sid):
    con = sqlite3.connect(_db_path())
    try:
        return con.execute(
            "SELECT experiment_id, measurement_method FROM %s "
            "WHERE project_id = ? ORDER BY experiment_id" % TABLE, (sid,)).fetchall()
    finally:
        con.close()


def _insert_raw_method(sid, experiment_id, value):
    """Test-only corruption injection: bypass the store (and its CHECKs)."""
    con = sqlite3.connect(_db_path())
    try:
        con.execute("PRAGMA ignore_check_constraints = ON")
        con.execute("INSERT INTO %s VALUES (?, ?, ?)" % TABLE,
                    (sid, experiment_id, value))
        con.commit()
    finally:
        con.close()


def _independent_method(sid, eid):
    """The COMMITTED method, read through a SEPARATE SQLite connection."""
    con = sqlite3.connect(_db_path())
    try:
        row = con.execute(
            "SELECT measurement_method FROM %s WHERE project_id = ? "
            "AND experiment_id = ?" % TABLE, (sid, eid)).fetchone()
        return None if row is None else row[0]
    finally:
        con.close()


def _memory_methods(sid):
    return {k: v.method for k, v in
            SESSION_STORE[sid]["state"].measurement_methods.items()}


def _pdf_source(monkeypatch, sid):
    seen = {}

    def capture(source):
        # Bounded double: capture the exact trusted source handed to the
        # renderer; the PDF engine itself is not under test here.
        seen["source"] = source
        return b"%PDF-1.7 captured"

    monkeypatch.setattr(webapp, "_render_pdf_bytes", capture)
    r = csrf_client(app).post("/session/%s/deliverable.pdf" % sid, data={})
    assert r.status_code == 200
    return seen["source"]


def _new_store_project(tmp_path, name="mm"):
    store = SqliteRecordStore(str(tmp_path / (name + ".sqlite")))
    pid = store.create_project(
        ProjectRecordContract.from_state(IdeaState(idea_id=name)), project_id="p-" + name)
    return store, pid


class _FailOnMutation:
    """Bounded failure injection: a proxy for the store connection that counts
    planning-metadata mutations (BOTH sidecars) inside the one transaction and
    fails the ``fail_at``-th one."""

    _MUTATIONS = ("INSERT INTO PROTOTYPE_PLAN_METADATA", "DELETE FROM PROTOTYPE_PLAN_METADATA",
                  "INSERT INTO PROTOTYPE_MEASUREMENT_METHODS",
                  "DELETE FROM PROTOTYPE_MEASUREMENT_METHODS")

    def __init__(self, conn, fail_at):
        self._conn = conn
        self.fail_at = fail_at
        self.seen = []

    def execute(self, sql, *args):
        head = sql.lstrip().upper()
        if head.startswith(self._MUTATIONS):
            self.seen.append(head.split("(")[0].split(" WHERE")[0].strip())
            if len(self.seen) == self.fail_at:
                raise sqlite3.OperationalError("injected failure on a planning mutation")
        return self._conn.execute(sql, *args)

    def __getattr__(self, name):
        return getattr(self._conn, name)


# ==========================================================================
# BASE RED — the missing product behaviour, through the real application
# ==========================================================================
def test_red_a_b_method_entered_on_the_planning_page_survives_restart(client):
    """A + B: the inventor enters a measurement method on the existing planning
    page and saves; it must still be attached to the SAME stable experiment
    after process memory loss and a same-database reopen."""
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    r, body = _criteria_page(client, sid)
    assert r.status_code == 200
    assert 'name="%s%s"' % (METHOD, eid) in body          # the field is offered
    r = _post_plan(client, sid, criteria={eid: "brake light seen at 50 m"},
                   methods={eid: "Walk back with a tape measure on a sunny day"})
    assert r.status_code == 302
    _restart()
    item = _reopened_items(sid)[eid]
    assert item["measurement_method"] == "Walk back with a tape measure on a sunny day"
    assert item["measurement_method_provenance"] == "user_defined"
    assert item["success_criterion"] == "brake light seen at 50 m"


def test_red_c_html_and_pdf_section_11_show_the_saved_method(client, monkeypatch):
    sid = _journey(client)
    eid = _live_ids(sid)[1]
    assert _post_plan(client, sid, methods={eid: "Log ten stops with a phone "
                                                  "accelerometer app"}).status_code == 302
    _restart()
    assert "Log ten stops with a phone accelerometer app" in _report(csrf_client(app), sid)
    assert "Log ten stops with a phone accelerometer app" in _pdf_source(monkeypatch, sid)


def test_red_d_no_existing_owner_already_carries_an_inventor_method(client):
    """D: the durable owner is the new typed sidecar; the pre-existing owners
    (``what_to_observe`` — fixed system text — and the SuccessCriterion
    sidecar) neither carry nor are changed by an inventor-authored method."""
    sid = _journey(client)
    ids = _live_ids(sid)
    observe_before = {it["experiment_id"]: it["what_to_observe"]
                      for it in _plan_items(SESSION_STORE[sid]["state"])}
    assert _post_plan(client, sid, methods={ids[0]: "Stopwatch, three repeats"}
                      ).status_code == 302
    assert _methods(sid) == {ids[0]: "Stopwatch, three repeats"}
    assert _durable(sid) == {}                      # not a criterion row
    items = {it["experiment_id"]: it for it in _plan_items(SESSION_STORE[sid]["state"])}
    assert {k: v["what_to_observe"] for k, v in items.items()} == observe_before
    assert "Stopwatch" not in items[ids[0]]["what_to_observe"]


# ==========================================================================
# Schema — one narrowly typed sibling sidecar; the criterion table unchanged
# ==========================================================================
def test_s01_fresh_table_has_exactly_the_bounded_shape(tmp_path):
    path = str(tmp_path / "shape.sqlite")
    SqliteRecordStore(path).close()
    con = sqlite3.connect(path)
    try:
        cols = [(r[1], r[2], r[3], r[5]) for r in con.execute("PRAGMA table_info(%s)" % TABLE)]
        fks = [(r[2], r[3], r[4]) for r in
               con.execute("PRAGMA foreign_key_list(%s)" % TABLE)]
        crit = [(r[1], r[2], r[3], r[5]) for r in
                con.execute("PRAGMA table_info(prototype_plan_metadata)")]
    finally:
        con.close()
    # ONLY the method text: no experiment definition, source, provenance,
    # variable, unit, result, validation, readiness or PASS/FAIL column.
    assert cols == [("project_id", "TEXT", 1, 1), ("experiment_id", "TEXT", 1, 2),
                    ("measurement_method", "TEXT", 1, 0)]
    assert fks == [("projects", "project_id", "project_id")]
    # The SuccessCriterion sidecar is NOT widened.
    assert crit == [("project_id", "TEXT", 1, 1), ("experiment_id", "TEXT", 1, 2),
                    ("success_criterion", "TEXT", 1, 0)]


def test_s02_existing_populated_database_migrates_additively(client):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    _post_plan(client, sid, criteria={eid: "pre-existing criterion"})
    before_contract = [assertion_to_dict(r)
                       for r in webapp._get_store().load_contract(sid).assertions]
    _restart()
    con = sqlite3.connect(_db_path())            # a database from before this slice
    con.execute("DROP TABLE %s" % TABLE)
    con.commit()
    con.close()
    store = SqliteRecordStore(_db_path())
    try:
        assert [assertion_to_dict(r) for r in store.load_contract(sid).assertions] \
            == before_contract
        assert store.load_success_criteria(sid) == ((eid, "pre-existing criterion"),)
        assert store.load_measurement_methods(sid) == ()
    finally:
        store.close()


def test_s03_repeated_initialization_is_idempotent_and_keeps_rows(client):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    assert _post_plan(client, sid, methods={eid: "kept across inits"}).status_code == 302
    _restart()
    for _ in range(3):
        SqliteRecordStore(_db_path()).close()
    assert _raw_methods(sid) == [(eid, "kept across inits")]


# ==========================================================================
# 1-2 — save one method; restart / reopen durability in both domains
# ==========================================================================
@pytest.mark.parametrize("idea,domain,answers", [
    (ELEC_IDEA, "electronics_electrical", ELEC_ANSWERS),
    (MECH_IDEA, "mechanical", MECH_ANSWERS),
])
def test_01_02_one_method_is_saved_and_survives_restart_in_both_domains(
        client, idea, domain, answers):
    sid = _journey(client, idea, domain, answers)
    ids = _live_ids(sid)
    assert len(ids) >= 2
    r = _post_plan(client, sid, methods={ids[0]: "Measure it with a scale"})
    assert r.status_code == 302 and r.headers["Location"].endswith("/deliverable")
    assert _methods(sid) == {ids[0]: "Measure it with a scale"}
    assert _memory_methods(sid) == {ids[0]: "Measure it with a scale"}   # published
    _restart()
    items = _reopened_items(sid)
    assert set(items) == set(ids)                   # same stable identities
    assert items[ids[0]]["measurement_method"] == "Measure it with a scale"
    for other in ids[1:]:                           # attached to THAT id only
        assert "measurement_method" not in items[other]
    r, body = _criteria_page(csrf_client(app), sid)
    assert r.status_code == 200 and "Measure it with a scale</textarea>" in body


# ==========================================================================
# 3-5 — cold and completed projects edit without Resume; progression untouched
# ==========================================================================
def test_03_05_cold_in_progress_project_edits_methods_without_resume(client):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    _post_plan(client, sid, methods={eid: "cold method"})
    _restart()
    before = _progression_snapshot(sid)
    fresh = csrf_client(app)
    r, body = _criteria_page(fresh, sid)
    assert r.status_code == 200 and "cold method</textarea>" in body
    assert _no_writable_session(sid)
    r = _post_plan(fresh, sid, methods={eid: "edited cold, without resume"})
    assert r.status_code == 302
    assert _methods(sid) == {eid: "edited cold, without resume"}
    assert _no_writable_session(sid)                     # nothing established
    assert _progression_snapshot(sid) == before          # progression untouched
    _restart()
    assert _reopened_items(sid)[eid]["measurement_method"] == "edited cold, without resume"


def test_04_05_completed_project_edits_methods_after_restart_without_resume(client):
    sid = _completed_project(client)
    ids = _live_ids(sid)
    assert ids
    _restart()
    before = _progression_snapshot(sid)
    assert before[0] >= 2 and before[3] == ()            # completed: no open gap
    fresh = csrf_client(app)
    fresh.post("/session/%s/resume" % sid, data={})     # refused by design
    assert _no_writable_session(sid)
    r = _post_plan(fresh, sid, criteria={ids[0]: "done when latch holds"},
                   methods={ids[0]: "Load the ramp with 150 kg sandbags"})
    assert r.status_code == 302
    assert _methods(sid) == {ids[0]: "Load the ramp with 150 kg sandbags"}
    assert _durable(sid) == {ids[0]: "done when latch holds"}
    assert _no_writable_session(sid)
    assert _progression_snapshot(sid) == before          # nothing reopened


def test_05_planning_metadata_only_never_touches_progression_or_records(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    store = webapp._get_store()
    ledger_before = [assertion_to_dict(r) for r in store.load_contract(sid).assertions]
    state = SESSION_STORE[sid]["state"]
    progression_before = (state.maturity_level, state.current_stage,
                          sorted((g.gap_type, g.status) for g in state.gaps),
                          len(state.iteration_log))
    transcript_before = copy.deepcopy(SESSION_STORE[sid].get("transcript"))
    snapshot = _progression_snapshot(sid)
    assert _post_plan(client, sid, methods={ids[0]: "Oscilloscope on the LED pin"}
                      ).status_code == 302
    assert [assertion_to_dict(r) for r in store.load_contract(sid).assertions] \
        == ledger_before                                  # no record, no answer
    assert (state.maturity_level, state.current_stage,
            sorted((g.gap_type, g.status) for g in state.gaps),
            len(state.iteration_log)) == progression_before
    assert SESSION_STORE[sid].get("transcript") == transcript_before
    assert _progression_snapshot(sid) == snapshot
    contract = store.load_contract(sid)
    assert "Oscilloscope on the LED pin" not in repr(contract)


# ==========================================================================
# 6-9 — combined atomic delta: upsert, delete, omitted; one transaction
# ==========================================================================
def test_06_combined_criterion_and_method_save_as_one_request(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    r = _post_plan(client, sid,
                   criteria={ids[0]: "light visible at 50 m", ids[1]: "lasts 3 h"},
                   methods={ids[0]: "tape measure, daylight", ids[2]: "timer on a bench"})
    assert r.status_code == 302
    assert _durable(sid) == {ids[0]: "light visible at 50 m", ids[1]: "lasts 3 h"}
    assert _methods(sid) == {ids[0]: "tape measure, daylight", ids[2]: "timer on a bench"}
    _restart()
    items = _reopened_items(sid)
    assert items[ids[0]]["success_criterion"] == "light visible at 50 m"
    assert items[ids[0]]["measurement_method"] == "tape measure, daylight"
    assert items[ids[2]]["measurement_method"] == "timer on a bench"


@pytest.mark.parametrize("fail_at", [1, 2, 3])
def test_07_22_failure_anywhere_in_the_combined_write_rolls_back_everything(
        client, monkeypatch, fail_at):
    """ONE submission = ONE transaction: a failure on the criterion part OR on
    the method part leaves BOTH concepts exactly as they were (confirmed
    rollback -> NOT SAVED; memory untouched)."""
    sid = _journey(client)
    ids = _live_ids(sid)
    _post_plan(client, sid, criteria={ids[2]: "keep criterion"},
               methods={ids[2]: "keep method"})
    live = SESSION_STORE[sid]["state"]
    memory_before = (copy.deepcopy(live.success_criteria),
                     copy.deepcopy(live.measurement_methods))
    store = webapp._get_store()
    proxy = _FailOnMutation(store._conn, fail_at)
    monkeypatch.setattr(store, "_conn", proxy)
    r = _post_plan(client, sid, criteria={ids[0]: "new criterion"},
                   methods={ids[0]: "new method", ids[2]: "  "})
    monkeypatch.setattr(store, "_conn", proxy._conn)
    assert len(proxy.seen) == fail_at                 # earlier mutations DID run
    assert r.status_code == 503
    body = html.unescape(r.get_data(as_text=True))
    assert NOT_SAVED in body and SAVED_NOT_SHOWN not in body and OUTCOME_UNKNOWN not in body
    assert _durable(sid) == {ids[2]: "keep criterion"}
    assert _methods(sid) == {ids[2]: "keep method"}
    assert (live.success_criteria, live.measurement_methods) == memory_before


def test_08_09_combined_delete_upsert_and_omitted_fields(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post_plan(client, sid, criteria={ids[0]: "c0", ids[1]: "c1"},
               methods={ids[0]: "m0", ids[1]: "m1", ids[2]: "m2"})
    # delete method 0 and criterion 1, upsert method 1; everything else omitted
    r = _post_plan(client, sid, criteria={ids[1]: "   "},
                   methods={ids[0]: "\t \n", ids[1]: "m1 edited"})
    assert r.status_code == 302
    assert _durable(sid) == {ids[0]: "c0"}
    assert _methods(sid) == {ids[1]: "m1 edited", ids[2]: "m2"}
    # a submission with ONLY criteria fields leaves every method untouched
    assert _post_plan(client, sid, criteria={ids[0]: "c0 edited"}).status_code == 302
    assert _methods(sid) == {ids[1]: "m1 edited", ids[2]: "m2"}
    _restart()
    items = _reopened_items(sid)
    assert "measurement_method" not in items[ids[0]]
    assert items[ids[1]]["measurement_method"] == "m1 edited"
    assert items[ids[2]]["measurement_method"] == "m2"
    assert items[ids[0]]["success_criterion"] == "c0 edited"


# ==========================================================================
# 10 — an unknown / no-longer-current id or invalid value rejects everything
# ==========================================================================
@pytest.mark.parametrize("bad", ["unknown_method_id", "over_limit_method",
                                 "over_limit_criterion"])
def test_10_14_invalid_submission_rejects_the_whole_planning_delta(client, bad):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post_plan(client, sid, criteria={ids[2]: "pre criterion"},
               methods={ids[2]: "pre method"})
    live = SESSION_STORE[sid]["state"]
    memory_before = (copy.deepcopy(live.success_criteria),
                     copy.deepcopy(live.measurement_methods))
    criteria = {ids[0]: "valid and would be saved", ids[2]: ""}
    methods = {ids[0]: "valid method", ids[2]: ""}
    if bad == "unknown_method_id":
        methods["exp_v1_acknowledged_unknown_" + "9" * 32] = "rogue"
        expected = "A submitted experiment is not part of the current plan."
    elif bad == "over_limit_method":
        methods[ids[1]] = "x" * (webapp.MAX_MEASUREMENT_METHOD_LENGTH + 1)
        expected = "A measurement method exceeds the 1000-character limit."
    else:
        criteria[ids[1]] = "x" * (webapp.MAX_CRITERION_LENGTH + 1)
        expected = "A criterion exceeds the 1000-character limit."
    r = _post_plan(client, sid, criteria=criteria, methods=methods)
    assert r.status_code == 400
    assert expected in html.unescape(r.get_data(as_text=True))
    assert _durable(sid) == {ids[2]: "pre criterion"}
    assert _methods(sid) == {ids[2]: "pre method"}
    assert (live.success_criteria, live.measurement_methods) == memory_before


def test_14_exactly_the_limit_is_accepted_and_one_more_is_refused(client):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    limit = webapp.MAX_MEASUREMENT_METHOD_LENGTH
    assert limit == 1000
    assert _post_plan(client, sid, methods={eid: "m" * limit}).status_code == 302
    assert _methods(sid) == {eid: "m" * limit}
    r = _post_plan(client, sid, methods={eid: "n" * (limit + 1)})
    assert r.status_code == 400
    assert _methods(sid) == {eid: "m" * limit}


# ==========================================================================
# 11-12 — stale retained, never remapped; exact-id reattachment
# ==========================================================================
def test_11_12_stale_method_is_preserved_never_remapped_and_reattaches(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    claim_id = [i for i in ids if "_reasoned_leading_claim_" in i][0]
    unknown_id = ids[0]
    _post_plan(client, sid, methods={claim_id: "Ride at 20 km/h and brake ten times",
                                     unknown_id: "Record ten stops"})
    _answer(client, sid, ELEC_DISPLACING_ANSWER)      # displaces the claim experiment
    current = _live_ids(sid)
    assert claim_id not in current and unknown_id in current
    report = _report(client, sid)
    assert text("UI_SC_METHOD_STALE", "en") in report
    with app.test_request_context():
        package = webapp._deliverable_context(sid)[1]
    plan = package["section_11_prototype_test_plan"]
    assert [s["experiment_id"] for s in plan["stale_measurement_methods"]] == [claim_id]
    assert all(it.get("measurement_method") != "Ride at 20 km/h and brake ten times"
               for it in plan["items"])                  # never remapped
    assert _methods(sid)[claim_id] == "Ride at 20 km/h and brake ten times"
    r, body = _criteria_page(client, sid)
    assert r.status_code == 200 and text("UI_SC_METHOD_STALE", "en") in body
    # A stale id is not part of the current plan: submitting it is refused.
    assert _post_plan(client, sid, methods={claim_id: "retarget"}).status_code == 400
    # The withdrawn answer brings the SAME canonical source back -> SAME id.
    record = _answered_record(sid, ELEC_DISPLACING_ANSWER)
    assert _correct(client, sid, record.record_id,
                    "The threshold will be chosen by measuring real stops.").status_code == 302
    items = _reopened_items(sid)
    assert items[claim_id]["measurement_method"] == "Ride at 20 km/h and brake ten times"
    assert items[unknown_id]["measurement_method"] == "Record ten stops"
    _restart()
    items = _reopened_items(sid)
    assert items[claim_id]["measurement_method"] == "Ride at 20 km/h and brake ten times"


# ==========================================================================
# 13 — NUL (leading / embedded / trailing): HTTP 400, store API, DB CHECK
# ==========================================================================
NUL_CASES = [("leading", "\x00leading nul"), ("embedded", "mid\x00dle"),
             ("trailing", "trailing nul\x00")]


@pytest.mark.parametrize("where,value", NUL_CASES)
@pytest.mark.parametrize("lang", ["en", "ar"])
def test_13_http_rejects_nul_before_persistence(client, where, value, lang):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post_plan(client, sid, methods={ids[1]: "existing"})
    live = SESSION_STORE[sid]["state"]
    memory_before = copy.deepcopy(live.measurement_methods)
    client.post("/ui-language", data={"lang": lang})
    r = _post_plan(client, sid, criteria={ids[2]: "would be saved"},
                   methods={ids[0]: value, ids[1]: "would change"})
    body = html.unescape(r.get_data(as_text=True))
    assert r.status_code == 400
    assert webapp._free_text_error(value, lang) in body
    assert _methods(sid) == {ids[1]: "existing"}
    assert _durable(sid) == {}
    assert live.measurement_methods == memory_before


@pytest.mark.parametrize("where,value", NUL_CASES)
def test_13_store_api_and_database_reject_nul(tmp_path, where, value):
    store, pid = _new_store_project(tmp_path, "nul")
    try:
        with pytest.raises(MeasurementMethodInvalid):
            store.apply_planning_metadata_delta(pid, {}, {EID_SHAPE: value})
        with pytest.raises(sqlite3.IntegrityError):          # CHECK, defence in depth
            store._conn.execute("INSERT INTO %s VALUES (?, ?, ?)" % TABLE,
                                (pid, EID_SHAPE, value))
        assert store.load_measurement_methods(pid) == ()
    finally:
        store.close()


@pytest.mark.parametrize("value", ["", "  padded  ", "x" * 1001, 42, b"bytes"])
def test_13_14_store_api_and_database_reject_invalid_text(tmp_path, value):
    store, pid = _new_store_project(tmp_path, "inv")
    try:
        with pytest.raises(MeasurementMethodInvalid):
            store.apply_planning_metadata_delta(pid, {}, {EID_SHAPE: value})
        # (an integer is coerced to TEXT by the column affinity, so only the
        # store API — asserted above — can refuse it; the CHECK backstops the rest)
        if value in ("", "x" * 1001, b"bytes"):
            with pytest.raises(sqlite3.IntegrityError):
                store._conn.execute("INSERT INTO %s VALUES (?, ?, ?)" % TABLE,
                                    (pid, EID_SHAPE, value))
        assert store.load_measurement_methods(pid) == ()
    finally:
        store.close()


def test_store_validates_the_whole_combined_delta_before_any_write(tmp_path):
    store, pid = _new_store_project(tmp_path, "whole")
    try:
        # a bad method refuses the valid criterion too; a bad criterion refuses
        # the valid method too — nothing is written either way.
        with pytest.raises(MeasurementMethodInvalid):
            store.apply_planning_metadata_delta(pid, {EID_SHAPE: "ok"},
                                                {EID_SHAPE: "\x00"})
        with pytest.raises(SuccessCriterionInvalid):
            store.apply_planning_metadata_delta(pid, {EID_SHAPE: " bad "},
                                                {EID_SHAPE: "ok"})
        with pytest.raises(MeasurementMethodInvalid):
            store.apply_planning_metadata_delta(pid, {}, {"not-an-id": "ok"})
        with pytest.raises(MeasurementMethodInvalid):
            store.apply_planning_metadata_delta(pid, {}, ["not", "a", "mapping"])
        assert store.load_success_criteria(pid) == ()
        assert store.load_measurement_methods(pid) == ()
        store.apply_planning_metadata_delta(pid, {EID_SHAPE: "c"}, {EID_SHAPE: "m"})
        assert store.load_success_criteria(pid) == ((EID_SHAPE, "c"),)
        assert store.load_measurement_methods(pid) == ((EID_SHAPE, "m"),)
    finally:
        store.close()


# ==========================================================================
# 15 — Arabic / Unicode / newline / tab / punctuation preserved exactly
# ==========================================================================
def test_15_legitimate_text_is_preserved_exactly(client, monkeypatch):
    sid = _journey(client)
    ids = _live_ids(sid)
    values = {ids[0]: "أقيس زمن الإضاءة بساعة إيقاف — ١٠ مرات ✓",
              ids[1]: "line one\nline two\twith a tab",
              ids[2]: "Punctuation: (a), [b]; {c}! ? \"q\" 'r' 50% ±1 °C"}
    assert _post_plan(client, sid, methods=values).status_code == 302
    assert _methods(sid) == values
    _restart()
    items = _reopened_items(sid)
    for eid, value in values.items():
        assert items[eid]["measurement_method"] == value
    assert values[ids[0]] in _report(csrf_client(app), sid)
    assert values[ids[0]] in _pdf_source(monkeypatch, sid)


# ==========================================================================
# 16-17 — project isolation; missing project / memory-only context
# ==========================================================================
def test_16_identical_experiment_ids_in_two_projects_stay_isolated(client):
    a = _journey(client)
    other = csrf_client(app)
    b = _journey(other)
    assert _live_ids(a) == _live_ids(b)                 # the SAME canonical ids
    eid = _live_ids(a)[0]
    _post_plan(client, a, methods={eid: "project A method"})
    _post_plan(other, b, methods={eid: "project B method"})
    _post_plan(client, a, methods={eid: " "})           # delete in A
    assert _methods(a) == {}
    assert _methods(b) == {eid: "project B method"}
    assert "project B method" not in _report(client, a)
    assert "project A method" not in _report(other, b)


def test_17_missing_project_and_memory_only_context(client, tmp_path):
    from engine.idea_state import AcknowledgedUnknown, ASSUMPTION_INVENTORY
    store = SqliteRecordStore(str(tmp_path / "missing.sqlite"))
    try:
        with pytest.raises(ProjectNotFound):
            store.load_measurement_methods("no-such-project")
        with pytest.raises(ProjectNotFound):
            store.apply_planning_metadata_delta("no-such-project", {}, {EID_SHAPE: "m"})
    finally:
        store.close()
    sid = "mem-only-mm-" + "0" * 8
    state = IdeaState(idea_id=sid)
    state.domain = "electronics_electrical"
    state.acknowledged_unknowns.append(AcknowledgedUnknown(
        iteration=1, gap_context=ASSUMPTION_INVENTORY,
        verbatim="I do not know the lockout count", category_basis="explicit"))
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    eid = [it["experiment_id"] for it in _plan_items(state)][0]
    r = _post_plan(client, sid, methods={eid: "would only live in memory"})
    assert r.status_code == 409
    assert NOT_A_PROJECT in html.unescape(r.get_data(as_text=True))
    assert state.measurement_methods == {}
    assert webapp._get_store().load_owner(sid) == (False, None)


def test_17b_non_owner_and_anonymous_cannot_read_or_write_methods(client):
    from tests.test_stage19_durable_success_criteria import _client_for
    owner, _aid = _client_for("owner-mm@example.com")
    sid = _journey(owner)
    eid = _live_ids(sid)[0]
    assert _post_plan(owner, sid, methods={eid: "owner method"}).status_code == 302
    intruder, _ = _client_for("other-mm@example.com")
    for c in (intruder, csrf_client(app)):
        r = c.get("/session/%s/success-criteria" % sid)
        assert r.status_code == 302 and r.headers["Location"].endswith("/")
        r = _post_plan(c, sid, methods={eid: "intruder"})
        assert r.status_code == 302 and r.headers["Location"].endswith("/")
    assert _methods(sid) == {eid: "owner method"}


# ==========================================================================
# 18-19 — corruption fails closed on Section 11 only; never gates progression
# ==========================================================================
@pytest.mark.parametrize("corruption", [
    ("valid_id", "  untrimmed  "),
    ("valid_id", b"blob-value"),
    ("valid_id", "nul\x00inside"),
    ("not-an-experiment-id", "fine text"),
])
def test_18_corrupt_method_fails_every_section_11_surface_closed(client, corruption):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post_plan(client, sid, criteria={ids[0]: "good criterion"},
               methods={ids[0]: "good method"})
    bad_id, bad_value = corruption
    _insert_raw_method(sid, ids[1] if bad_id == "valid_id" else bad_id, bad_value)
    with pytest.raises(MeasurementMethodCorrupt):
        webapp._get_store().load_measurement_methods(sid)
    r, body = _criteria_page(client, sid)                           # planning GET
    assert r.status_code == 503 and UNAVAILABLE in body
    assert 'name="%s' % METHOD not in body and "good method" not in body
    r = _post_plan(client, sid, methods={ids[2]: "blocked while corrupt"})  # POST
    assert r.status_code == 503
    r = client.get("/session/%s/deliverable" % sid)                 # HTML
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    r = csrf_client(app).post("/session/%s/deliverable.pdf" % sid, data={})   # PDF
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    assert len(_raw_methods(sid)) == 2                               # not repaired
    assert _durable(sid) == {ids[0]: "good criterion"}               # untouched


def test_18b_a_bad_method_row_never_yields_a_partial_attachment(client):
    """Both collections load before either is assigned: good durable criteria
    are NOT attached when the method collection is corrupt."""
    from engine.idea_state import SuccessCriterion, MeasurementMethod
    sid = _journey(client)
    ids = _live_ids(sid)
    _post_plan(client, sid, criteria={ids[0]: "durable good criterion"},
               methods={ids[0]: "durable good method"})
    _insert_raw_method(sid, ids[1], "\tbad\t")
    state = SESSION_STORE[sid]["state"]
    state.success_criteria = {"prior": SuccessCriterion("carrier criterion")}
    state.measurement_methods = {"prior": MeasurementMethod("carrier method")}
    assert webapp._attach_planning_metadata(sid, state) is False
    assert {k: v.criterion for k, v in state.success_criteria.items()} == {
        "prior": "carrier criterion"}                         # untouched, not the good set
    assert {k: v.method for k, v in state.measurement_methods.items()} == {
        "prior": "carrier method"}


def test_19_corrupt_method_never_blocks_entry_resume_answer_or_correction(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    _insert_raw_method(sid, ids[0], "  untrimmed  ")
    store = webapp._get_store()
    ledger_before = [assertion_to_dict(r) for r in store.load_contract(sid).assertions]
    record = _answered_record(sid, ELEC_ANSWERS[3])
    assert _correct(client, sid, record.record_id,
                    "The rain question is answered by a sealed enclosure.").status_code == 302
    assert SESSION_STORE[sid].get("_answer_error") is None
    assert SESSION_STORE[sid].get("_interaction_ack") == webapp.CORRECTION_APPLIED_ACK
    assert len(store.load_contract(sid).assertions) == len(ledger_before) + 1
    _restart()
    fresh = csrf_client(app)
    assert fresh.get("/session/%s" % sid).status_code == 200         # cold entry
    assert fresh.post("/session/%s/resume" % sid, data={}).status_code == 302
    assert not _no_writable_session(sid)                              # resumed
    _answer(fresh, sid, "The LED is a bright red one.")               # progression
    assert (ids[0], "  untrimmed  ") in _raw_methods(sid)             # not repaired
    r, body = _criteria_page(fresh, sid)
    assert r.status_code == 503 and UNAVAILABLE in body


def test_19b_corrupt_method_never_blocks_adoption_or_reversal(client):
    sid = _legacy_journey(client)
    ids = _live_ids(sid)
    _insert_raw_method(sid, ids[0], "\tcorrupt\t")
    for action, ack in (("adopt", "EVA_ADOPTED"), ("revert", "EVA_REVERTED")):
        before = SESSION_STORE[sid]["state"]
        assert _adopt(client, sid, action).status_code == 302
        assert SESSION_STORE[sid]["state"] is not before
        assert SESSION_STORE[sid].get("_eva_ack") == ack
        assert SESSION_STORE[sid].get("_eva_error") is None
    assert (ids[0], "\tcorrupt\t") in _raw_methods(sid)


def test_19c_adoption_and_reversal_carry_the_durable_methods(client):
    sid = _legacy_journey(client)
    ids = _live_ids(sid)
    _post_plan(client, sid, methods={ids[0]: "held across adoption", ids[1]: "and reversal"})
    for action in ("adopt", "revert"):
        before = SESSION_STORE[sid]["state"]
        assert _adopt(client, sid, action).status_code == 302
        after = SESSION_STORE[sid]["state"]
        assert after is not before
        with app.test_request_context():
            context = webapp._deliverable_context(sid)
        assert context is not None and context[4] is after
        assert _memory_methods(sid) == {ids[0]: "held across adoption",
                                        ids[1]: "and reversal"}
        plan = context[1]["section_11_prototype_test_plan"]
        plan_ids = [it["experiment_id"] for it in plan["items"]]
        stale = {s["experiment_id"] for s in plan.get("stale_measurement_methods", ())}
        for eid in (ids[0], ids[1]):
            assert (eid in plan_ids) != (eid in stale)          # never dropped


# ==========================================================================
# 20-25 — F-04 / IR-01 over the COMBINED planning write
# ==========================================================================
def test_20_ir01_unresolved_transaction_on_a_method_write_is_unknown(client, monkeypatch):
    sid = _journey(client)
    ids = _live_ids(sid)
    eid = ids[0]
    assert _post_plan(client, sid, methods={eid: "old committed method"}).status_code == 302
    live = SESSION_STORE[sid]["state"]
    memory_before = copy.deepcopy(live.measurement_methods)
    store = webapp._get_store()
    real_conn = store._conn
    monkeypatch.setattr(store, "_conn", _CommitAndRollbackFail(real_conn))
    r = _post_plan(client, sid, methods={eid: "new uncommitted method"})
    assert real_conn.in_transaction is True                       # the real shape
    same = dict(real_conn.execute(
        "SELECT experiment_id, measurement_method FROM %s WHERE project_id = ?" % TABLE,
        (sid,)).fetchall())
    assert same[eid] == "new uncommitted method"                  # own uncommitted view
    assert _independent_method(sid, eid) == "old committed method"
    body = html.unescape(r.get_data(as_text=True))
    assert r.status_code == 503 and OUTCOME_UNKNOWN in body
    assert NOT_SAVED not in body and SAVED_NOT_SHOWN not in body
    assert live.measurement_methods == memory_before              # not published
    r2, body2 = _criteria_page(client, sid)
    assert r2.status_code == 503 and "new uncommitted method" not in body2
    monkeypatch.setattr(store, "_conn", real_conn)
    _restart()
    assert _reopened_items(sid)[eid]["measurement_method"] == "old committed method"


def test_21_ir01_combined_criterion_and_method_delta_is_unknown(client, monkeypatch):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post_plan(client, sid, criteria={ids[0]: "old criterion"},
               methods={ids[0]: "old method", ids[1]: "method to delete"})
    live = SESSION_STORE[sid]["state"]
    memory_before = (copy.deepcopy(live.success_criteria),
                     copy.deepcopy(live.measurement_methods))
    store = webapp._get_store()
    real_conn = store._conn
    monkeypatch.setattr(store, "_conn", _CommitAndRollbackFail(real_conn))
    r = _post_plan(client, sid, criteria={ids[0]: "new criterion"},
                   methods={ids[0]: "new method", ids[1]: "  "})
    assert real_conn.in_transaction is True
    body = html.unescape(r.get_data(as_text=True))
    assert r.status_code == 503 and OUTCOME_UNKNOWN in body
    assert NOT_SAVED not in body
    assert _independent_method(sid, ids[0]) == "old method"
    assert _independent_method(sid, ids[1]) == "method to delete"
    assert (live.success_criteria, live.measurement_methods) == memory_before
    monkeypatch.setattr(store, "_conn", real_conn)
    _restart()
    items = _reopened_items(sid)
    assert items[ids[0]]["success_criterion"] == "old criterion"
    assert items[ids[0]]["measurement_method"] == "old method"
    assert items[ids[1]]["measurement_method"] == "method to delete"


def test_20_21_store_refuses_method_reads_and_combined_writes_when_unsafe(tmp_path):
    store, pid = _new_store_project(tmp_path, "unsafe")
    try:
        store.apply_planning_metadata_delta(pid, {EID_SHAPE: "c"}, {EID_SHAPE: "m"})
        real = store._conn
        store._conn = _CommitAndRollbackFail(real)
        with pytest.raises(sqlite3.OperationalError):
            store.apply_planning_metadata_delta(pid, {}, {EID_SHAPE: "uncommitted"})
        store._conn = real
        assert real.in_transaction is True
        assert store.committed_state_readable() is False
        with pytest.raises(RecordStoreConnectionUnsafe):
            store.load_measurement_methods(pid)
        with pytest.raises(RecordStoreConnectionUnsafe):
            store.load_success_criteria(pid)
        with pytest.raises(RecordStoreConnectionUnsafe):
            store.apply_planning_metadata_delta(pid, {EID_SHAPE: "c2"}, {})
        real.execute("ROLLBACK")                       # resolved by hand ...
        assert store.committed_state_readable() is False   # ... still never trusted
        with pytest.raises(RecordStoreConnectionUnsafe):
            store.load_measurement_methods(pid)
    finally:
        store.close()


@pytest.mark.parametrize("shape", ["method_only", "combined_mixed"])
def test_23_committed_complete_planning_delta_is_saved(client, monkeypatch, shape):
    """The commit happened, then an error was raised: the COMPLETE requested
    state is durably present -> SAVED, published only after that is known."""
    sid = _journey(client)
    ids = _live_ids(sid)
    _post_plan(client, sid, criteria={ids[1]: "crit to delete"},
               methods={ids[1]: "method to delete", ids[2]: "omitted, untouched"})
    criteria = {}
    methods = {ids[0]: "committed then raised"}
    if shape == "combined_mixed":
        criteria = {ids[0]: "criterion committed", ids[1]: " "}
        methods[ids[1]] = " "
    store = webapp._get_store()
    proxy = _CommitThenRaise(store._conn)
    monkeypatch.setattr(store, "_conn", proxy)
    r = _post_plan(client, sid, criteria=criteria, methods=methods)
    monkeypatch.setattr(store, "_conn", proxy._conn)
    assert r.status_code == 302 and r.headers["Location"].endswith("/deliverable")
    expected_m = {ids[0]: "committed then raised", ids[2]: "omitted, untouched"}
    expected_c = {ids[1]: "crit to delete"}
    if shape == "method_only":
        expected_m[ids[1]] = "method to delete"
    else:
        expected_c = {ids[0]: "criterion committed"}
    assert _methods(sid) == expected_m and _durable(sid) == expected_c
    assert _memory_methods(sid) == expected_m


def test_22_24_partial_match_across_concepts_is_not_saved(client, monkeypatch):
    """The criterion part is already durable, the method part is not: the
    complete submitted delta does not match -> NOT SAVED, never SAVED."""
    sid = _journey(client)
    ids = _live_ids(sid)
    _post_plan(client, sid, criteria={ids[0]: "already there"})

    def failing_apply(self, project_id, criteria_delta, method_delta):
        raise sqlite3.OperationalError("injected: failed before commit")

    monkeypatch.setattr(SqliteRecordStore, "apply_planning_metadata_delta", failing_apply)
    r = _post_plan(client, sid, criteria={ids[0]: "already there"},
                   methods={ids[0]: "never written"})
    assert r.status_code == 503 and NOT_SAVED in html.unescape(r.get_data(as_text=True))
    assert _methods(sid) == {}


def test_24_25_unreadable_method_confirmation_is_unknown_and_memory_untouched(
        client, monkeypatch):
    sid = _journey(client)
    ids = _live_ids(sid)
    live = SESSION_STORE[sid]["state"]
    memory_before = (copy.deepcopy(live.success_criteria),
                     copy.deepcopy(live.measurement_methods))
    real_load = SqliteRecordStore.load_measurement_methods
    calls = {"n": 0}

    def load(self, project_id):
        # call 1 establishes the current plan BEFORE the write; the reload that
        # would resolve the outcome after the failed write is unreadable.
        calls["n"] += 1
        if calls["n"] >= 2:
            raise sqlite3.OperationalError("injected: database is locked")
        return real_load(self, project_id)

    def failing_apply(self, project_id, criteria_delta, method_delta):
        raise sqlite3.OperationalError("injected: disk I/O error")

    monkeypatch.setattr(SqliteRecordStore, "load_measurement_methods", load)
    monkeypatch.setattr(SqliteRecordStore, "apply_planning_metadata_delta", failing_apply)
    r = _post_plan(client, sid, criteria={ids[0]: "c"}, methods={ids[0]: "outcome unknown"})
    body = html.unescape(r.get_data(as_text=True))
    assert r.status_code == 503 and OUTCOME_UNKNOWN in body
    assert NOT_SAVED not in body and SAVED_NOT_SHOWN not in body
    assert 'name="%s' % METHOD not in body                          # no stale form
    assert (live.success_criteria, live.measurement_methods) == memory_before


@pytest.mark.parametrize("durable_c,durable_m,criteria,methods,expected", [
    ({}, {"a": "m"}, {}, {"a": "m"}, "saved"),
    ({"a": "c"}, {"a": "m"}, {"a": "c"}, {"a": "m"}, "saved"),
    ({}, {}, {}, {"a": None}, "saved"),                    # delete confirmed by absence
    ({}, {"a": "m"}, {}, {"a": None}, "not_saved"),        # delete not reflected
    ({"a": "c"}, {"a": "old"}, {"a": "c"}, {"a": "new"}, "not_saved"),
    ({"a": "old"}, {"a": "m"}, {"a": "new"}, {"a": "m"}, "not_saved"),
    ({}, {"a": "m", "omitted": "x"}, {}, {"a": "m"}, "saved"),   # omitted ignored
])
def test_confirmation_rule_compares_the_complete_submitted_planning_delta(
        monkeypatch, durable_c, durable_m, criteria, methods, expected):
    class _Store:
        def load_success_criteria(self, project_id):
            return tuple(durable_c.items())

        def load_measurement_methods(self, project_id):
            return tuple(durable_m.items())

    monkeypatch.setattr(webapp, "_get_store", lambda: _Store())
    assert webapp._resolve_criteria_write("p", criteria, methods) == expected


@pytest.mark.parametrize("unreadable", ["criteria", "methods"])
def test_confirmation_rule_unreadable_either_concept_is_unknown(monkeypatch, unreadable):
    class _Store:
        def load_success_criteria(self, project_id):
            if unreadable == "criteria":
                raise RecordStoreConnectionUnsafe("unresolved")
            return (("a", "c"),)

        def load_measurement_methods(self, project_id):
            if unreadable == "methods":
                raise MeasurementMethodCorrupt("malformed")
            return (("a", "m"),)

    monkeypatch.setattr(webapp, "_get_store", lambda: _Store())
    assert webapp._resolve_criteria_write("p", {"a": "c"}, {"a": "m"}) == "unknown"


def test_25_memory_is_published_only_after_the_durable_outcome(client, monkeypatch):
    sid = _journey(client)
    ids = _live_ids(sid)
    live = SESSION_STORE[sid]["state"]
    seen = {}
    real_apply = SqliteRecordStore.apply_planning_metadata_delta

    def observing_apply(self, project_id, criteria_delta, method_delta):
        seen["memory_during_write"] = dict(live.measurement_methods)
        return real_apply(self, project_id, criteria_delta, method_delta)

    monkeypatch.setattr(SqliteRecordStore, "apply_planning_metadata_delta", observing_apply)
    assert _post_plan(client, sid, methods={ids[0]: "published after commit"}
                      ).status_code == 302
    assert seen["memory_during_write"] == {}                 # not yet published
    assert _memory_methods(sid) == {ids[0]: "published after commit"}


# ==========================================================================
# 26-28 — HTML, PDF and EN/AR UI
# ==========================================================================
def test_26_html_renders_the_saved_method_escaped_and_truthful_absence(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post_plan(client, sid, methods={ids[1]: "<b>ruler</b> & a camera"})
    _restart()
    fresh = csrf_client(app)
    raw = fresh.get("/session/%s/deliverable" % sid).get_data(as_text=True)
    assert "&lt;b&gt;ruler&lt;/b&gt; &amp; a camera" in raw        # escaped, verbatim
    assert "<b>ruler</b>" not in raw
    body = html.unescape(raw)
    assert text("UI_DELIV_METHOD_DEFINED", "en") in body
    # the other experiments carry truthful absence copy, never a fabricated method
    assert body.count(text("UI_DELIV_METHOD_ABSENT", "en")) == len(ids) - 1


def test_27_pdf_source_carries_the_saved_method_after_restart(client, monkeypatch):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    _post_plan(client, sid, methods={eid: "PDF carries this durable method"})
    _restart()
    source = _pdf_source(monkeypatch, sid)
    assert "PDF carries this durable method" in source
    assert text("UI_DELIV_METHOD_DEFINED", "en") in html.unescape(source)


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_28_planning_page_and_report_are_bilingual(client, lang):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post_plan(client, sid, methods={ids[0]: "قياس بمسطرة"})
    client.post("/ui-language", data={"lang": lang})
    r, body = _criteria_page(client, sid)
    assert r.status_code == 200
    for key in ("UI_SC_METHOD_INTRO", "UI_SC_METHOD_LABEL", "UI_SC_METHOD_PLACEHOLDER",
                "UI_B_SC_004", "UI_SC_SAVE_CLEAR", "UI_B_SC_002"):
        assert text(key, lang) in body, key
    for eid in ids:
        assert 'name="%s%s"' % (METHOD, eid) in body
        assert 'name="%s%s"' % (PREFIX, eid) in body
    report = _report(client, sid)
    assert text("UI_DELIV_METHOD_DEFINED", lang) in report
    assert text("UI_DELIV_METHOD_ABSENT", lang) in report
    r = _post_plan(client, sid, methods={ids[1]: "y" * 1001})
    assert r.status_code == 400
    assert text("UI_SC_ERR_METHOD_TOO_LONG", lang) in html.unescape(r.get_data(as_text=True))
    client.post("/ui-language", data={"lang": "en"})


def test_28b_every_new_ui_key_has_english_and_arabic_copy():
    from web import ui_text
    for key in ("UI_SC_METHOD_INTRO", "UI_SC_METHOD_LABEL", "UI_SC_METHOD_PLACEHOLDER",
                "UI_SC_METHOD_STALE", "UI_SC_ERR_METHOD_TOO_LONG",
                "UI_DELIV_METHOD_DEFINED", "UI_DELIV_METHOD_ABSENT_LABEL",
                "UI_DELIV_METHOD_ABSENT"):
        entry = ui_text.UI_STRINGS[key]
        assert entry["en"].strip() and entry["ar"].strip(), key
        assert entry["en"] != entry["ar"], key
    # the method copy never presents the plan as a measurement, result or proof
    en = " ".join(ui_text.UI_STRINGS[k]["en"] for k in
                  ("UI_SC_METHOD_INTRO", "UI_SC_METHOD_LABEL", "UI_DELIV_METHOD_DEFINED"))
    for word in ("validated", "verified", "passed", "proven", "result recorded"):
        assert word not in en.lower()


# ==========================================================================
# 29 — retention truth
# ==========================================================================
def test_29_retention_inventory_states_the_factual_behaviour():
    import os
    path = os.path.join(os.path.dirname(__file__), "..", "docs", "DATA_RETENTION_POLICY.md")
    with open(path, encoding="utf-8") as fh:
        doc = " ".join(fh.read().split())
    assert "`prototype_measurement_methods`" in doc
    assert "measurement method" in doc.lower()
    # current value, user-initiated clear, never an erasure or expiry claim
    assert "clearing the box removes that row" in doc
    assert "NOT an erasure capability" in doc
    assert "may persist in backups" in doc


# ==========================================================================
# 30 — experiment identity and every generated Section-11 field unchanged
# ==========================================================================
def test_30_experiment_identity_and_generated_fields_are_unchanged(client):
    from engine.deliverable_assembler import _experiment_id
    sid = _journey(client)
    before = {it["experiment_id"]: it for it in _plan_items(SESSION_STORE[sid]["state"])}
    ids = list(before)
    _post_plan(client, sid, methods={ids[0]: "calipers and a notebook"})
    after = {it["experiment_id"]: it for it in _plan_items(SESSION_STORE[sid]["state"])}
    assert list(after) == ids                                     # same ids, same order
    for eid, item in after.items():
        src = item["traceability"]
        assert _experiment_id(src["source_type"], src["content"]) == eid
        extra = {"measurement_method", "measurement_method_provenance"} \
            if eid == ids[0] else set()
        assert set(item) == set(before[eid]) | extra              # additive only
        for key in before[eid]:
            assert item[key] == before[eid][key], key             # byte-identical
    assert after[ids[0]]["measurement_method_provenance"] == "user_defined"
    # the plan-level shape is unchanged when nothing is stale
    plan = __import__("engine.deliverable_assembler", fromlist=["x"]).assemble_deliverable(
        SESSION_STORE[sid]["state"])["section_11_prototype_test_plan"]
    assert "stale_measurement_methods" not in plan


def test_30b_idea_state_carries_one_typed_planning_field():
    from engine.idea_state import MeasurementMethod, SuccessCriterion
    names = {f.name for f in dataclasses.fields(IdeaState)}
    assert "measurement_methods" in names and "success_criteria" in names
    assert IdeaState(idea_id="x").measurement_methods == {}
    assert [f.name for f in dataclasses.fields(MeasurementMethod)] == ["method", "provenance"]
    assert MeasurementMethod("m").provenance == "user_defined"
    # the existing semantic owner is unchanged
    assert [f.name for f in dataclasses.fields(SuccessCriterion)] == ["criterion", "provenance"]
