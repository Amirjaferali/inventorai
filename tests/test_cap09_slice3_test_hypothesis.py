"""Stage 19 / CAP-09 SLICE 3 — durable Owner-defined Test Hypothesis.

File-creation contract:
  Path: tests/test_cap09_slice3_test_hypothesis.py
  Purpose: prove that the inventor can record, edit and clear, for each CURRENT
    Section-11 experiment, their OWN test hypothesis (what they expect to
    happen); that it is durable in the SAME SQLite store as a narrowly typed
    sibling sidecar (``prototype_test_hypotheses``); that it is saved with the
    success criteria and measurement methods as ONE atomic planning write
    whose uncertain outcome is resolved truthfully (SAVED / NOT SAVED /
    UNKNOWN, IR-01 included); that stale, corrupt, missing-project and
    memory-only cases stay distinct; and that it stays planning metadata only
    — never Evidence, a result, validation, readiness, progression, a CAP-08
    assumption or a CAP-10 contradiction.
  Input contract: the live web app, the conftest per-test on-disk SQLite
    database and REAL /start -> answer journeys. A "restart" clears
    SESSION_STORE and reopens the SAME database with a fresh store.
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
    TestHypothesisCorrupt, TestHypothesisInvalid, MAX_TEST_HYPOTHESIS_LENGTH,
)
from engine.record_contract import ProjectRecordContract, assertion_to_dict
from engine.idea_state import IdeaState, TestHypothesis
from tests.csrf_client import csrf_client
from tests.test_stage19_durable_success_criteria import (
    ELEC_DISPLACING_ANSWER, PREFIX, _journey, _restart, _plan_items, _live_ids,
    _answer, _correct, _answered_record, _reopened_items, _criteria_page,
    _db_path, _durable, _report, _progression_snapshot, _no_writable_session,
    _CommitThenRaise, _CommitAndRollbackFail,
)

METHOD = "method__"
HYP = "hypothesis__"
TABLE = "prototype_test_hypotheses"
OUTCOME_UNKNOWN = webapp.SC_OUTCOME_UNKNOWN_MESSAGE
NOT_SAVED = webapp.SC_NOT_SAVED_MESSAGE
SAVED_NOT_SHOWN = webapp.SC_SAVED_NOT_SHOWN_MESSAGE
NOT_A_PROJECT = webapp.SC_NOT_SAVED_PROJECT_MESSAGE
UNAVAILABLE = webapp.SC_CRITERIA_UNAVAILABLE_MESSAGE
TOO_LONG = webapp.SC_HYPOTHESIS_TOO_LONG_MESSAGE
NOT_CURRENT = "A submitted experiment is not part of the current plan."
EID_SHAPE = "exp_v1_acknowledged_unknown_" + "e" * 32


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return csrf_client(app)


def _post(client, sid, criteria=None, methods=None, hypotheses=None):
    data = {PREFIX + k: v for k, v in (criteria or {}).items()}
    data.update({METHOD + k: v for k, v in (methods or {}).items()})
    data.update({HYP + k: v for k, v in (hypotheses or {}).items()})
    return client.post("/session/%s/success-criteria" % sid, data=data)


def _hyps(sid):
    """The DURABLE hypotheses, read through the application store."""
    return dict(webapp._get_store().load_test_hypotheses(sid))


def _methods(sid):
    return dict(webapp._get_store().load_measurement_methods(sid))


def _raw_rows(sid, table=TABLE):
    col = {"prototype_test_hypotheses": "test_hypothesis",
           "prototype_measurement_methods": "measurement_method",
           "prototype_plan_metadata": "success_criterion"}[table]
    con = sqlite3.connect(_db_path())
    try:
        return con.execute(
            "SELECT experiment_id, %s FROM %s WHERE project_id = ? "
            "ORDER BY experiment_id" % (col, table), (sid,)).fetchall()
    finally:
        con.close()


def _insert_raw(sid, experiment_id, value):
    """Test-only corruption injection: bypass the store (and its CHECKs)."""
    con = sqlite3.connect(_db_path())
    try:
        con.execute("PRAGMA ignore_check_constraints = ON")
        con.execute("INSERT INTO %s VALUES (?, ?, ?)" % TABLE, (sid, experiment_id, value))
        con.commit()
    finally:
        con.close()


def _independent(sid, eid):
    """The COMMITTED hypothesis, read through a SEPARATE SQLite connection."""
    con = sqlite3.connect(_db_path())
    try:
        row = con.execute("SELECT test_hypothesis FROM %s WHERE project_id = ? "
                          "AND experiment_id = ?" % TABLE, (sid, eid)).fetchone()
        return None if row is None else row[0]
    finally:
        con.close()


def _memory(sid):
    return {k: v.hypothesis for k, v in
            SESSION_STORE[sid]["state"].test_hypotheses.items()}


def _pdf_source(monkeypatch, sid):
    seen = {}

    def capture(source):
        # Bounded double: capture the exact trusted source handed to the PDF
        # renderer; the PDF engine itself is not under test here.
        seen["source"] = source
        return b"%PDF-1.7 captured"

    monkeypatch.setattr(webapp, "_render_pdf_bytes", capture)
    r = csrf_client(app).post("/session/%s/deliverable.pdf" % sid, data={})
    assert r.status_code == 200
    return seen["source"]


def _new_store_project(tmp_path, name="th"):
    store = SqliteRecordStore(str(tmp_path / (name + ".sqlite")))
    pid = store.create_project(
        ProjectRecordContract.from_state(IdeaState(idea_id=name)), project_id="p-" + name)
    return store, pid


def _textarea(raw, name):
    """The raw (still escaped) content of the named textarea."""
    start = raw.index('name="%s"' % name)
    open_end = raw.index(">", start) + 1
    return raw[open_end:raw.index("</textarea>", open_end)]


class _FailOnMutation:
    """Bounded failure injection: counts planning-metadata mutations on ALL
    THREE sidecars inside the one transaction and fails the ``fail_at``-th."""

    _MUTATIONS = tuple(verb + table for verb in ("INSERT INTO ", "DELETE FROM ")
                       for table in ("PROTOTYPE_PLAN_METADATA",
                                     "PROTOTYPE_MEASUREMENT_METHODS",
                                     "PROTOTYPE_TEST_HYPOTHESES"))

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
# A-D — create, reload, edit, clear
# ==========================================================================
def test_a_b_hypothesis_is_created_and_survives_restart(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    r, body = _criteria_page(client, sid)
    assert r.status_code == 200
    for eid in ids:                                    # one field per experiment
        assert 'name="%s%s"' % (HYP, eid) in body
    r = _post(client, sid, hypotheses={ids[0]: "The light stays visible at 50 m"})
    assert r.status_code == 302 and r.headers["Location"].endswith("/deliverable")
    assert _hyps(sid) == {ids[0]: "The light stays visible at 50 m"}
    assert _memory(sid) == {ids[0]: "The light stays visible at 50 m"}   # published
    _restart()
    items = _reopened_items(sid)
    assert set(items) == set(ids)                                        # same ids
    assert items[ids[0]]["test_hypothesis"] == "The light stays visible at 50 m"
    assert items[ids[0]]["test_hypothesis_provenance"] == "user_defined"
    for other in ids[1:]:                                                # that id only
        assert "test_hypothesis" not in items[other]
    r, body = _criteria_page(csrf_client(app), sid)
    assert "The light stays visible at 50 m</textarea>" in body


def test_c_hypothesis_is_edited_in_place(client):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    assert _post(client, sid, hypotheses={eid: "first expectation"}).status_code == 302
    assert _post(client, sid, hypotheses={eid: "  revised expectation  "}).status_code == 302
    assert _raw_rows(sid) == [(eid, "revised expectation")]              # trimmed, one row
    _restart()
    assert _reopened_items(sid)[eid]["test_hypothesis"] == "revised expectation"


def test_d_clearing_removes_only_that_hypothesis(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post(client, sid, hypotheses={ids[0]: "h0", ids[1]: "h1"})
    assert _post(client, sid, hypotheses={ids[0]: " \t\r\n "}).status_code == 302
    assert _hyps(sid) == {ids[1]: "h1"}
    _restart()
    items = _reopened_items(sid)
    assert "test_hypothesis" not in items[ids[0]]
    assert items[ids[1]]["test_hypothesis"] == "h1"
    body = _report(csrf_client(app), sid)
    assert text("UI_DELIV_HYPOTHESIS_ABSENT", "en") in body


# ==========================================================================
# E-G — the other two concepts are untouched; ONE three-way save
# ==========================================================================
def test_e_f_hypothesis_edit_leaves_criterion_and_method_byte_identical(client):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    _post(client, sid, criteria={eid: "crit\r\nwith CRLF"}, methods={eid: "method\ttab"})
    before = (_raw_rows(sid, "prototype_plan_metadata"),
              _raw_rows(sid, "prototype_measurement_methods"))
    assert _post(client, sid, hypotheses={eid: "expect it to hold"}).status_code == 302
    assert (_raw_rows(sid, "prototype_plan_metadata"),
            _raw_rows(sid, "prototype_measurement_methods")) == before
    assert _hyps(sid) == {eid: "expect it to hold"}


def test_g_three_concepts_save_as_one_request(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    r = _post(client, sid, criteria={ids[0]: "c0"}, methods={ids[1]: "m1"},
              hypotheses={ids[0]: "h0", ids[2]: "h2"})
    assert r.status_code == 302
    assert _durable(sid) == {ids[0]: "c0"}
    assert _methods(sid) == {ids[1]: "m1"}
    assert _hyps(sid) == {ids[0]: "h0", ids[2]: "h2"}
    _restart()
    items = _reopened_items(sid)
    assert (items[ids[0]]["success_criterion"], items[ids[0]]["test_hypothesis"]) == ("c0", "h0")
    assert items[ids[1]]["measurement_method"] == "m1"
    assert items[ids[2]]["test_hypothesis"] == "h2"


def test_g_store_applies_all_three_deltas_in_one_transaction(tmp_path, monkeypatch):
    store, pid = _new_store_project(tmp_path, "one-tx")
    begins = []
    real = store._conn

    class _Spy:
        def execute(self, sql, *args):
            if sql.strip().upper().startswith("BEGIN"):
                begins.append(sql)
            return real.execute(sql, *args)

        def __getattr__(self, name):
            return getattr(real, name)

    try:
        store._conn = _Spy()
        store.apply_planning_metadata_delta(pid, {EID_SHAPE: "c"}, {EID_SHAPE: "m"},
                                            {EID_SHAPE: "h"})
        store._conn = real
        assert len(begins) == 1                                   # ONE transaction
        assert store.load_test_hypotheses(pid) == ((EID_SHAPE, "h"),)
        assert store.load_measurement_methods(pid) == ((EID_SHAPE, "m"),)
        assert store.load_success_criteria(pid) == ((EID_SHAPE, "c"),)
        # None is an EMPTY delta, never a deletion; the two-delta call is unchanged
        store.apply_planning_metadata_delta(pid, {EID_SHAPE: "c2"}, {})
        store.apply_planning_metadata_delta(pid, {}, {}, None)
        assert store.load_test_hypotheses(pid) == ((EID_SHAPE, "h"),)
    finally:
        store._conn = real
        store.close()


# ==========================================================================
# H — a forced failure anywhere leaves NO partial commit
# ==========================================================================
@pytest.mark.parametrize("fail_at", [1, 2, 3, 4])
def test_h_failure_anywhere_in_the_three_way_write_rolls_back_everything(
        client, monkeypatch, fail_at):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post(client, sid, criteria={ids[2]: "keep c"}, methods={ids[2]: "keep m"},
          hypotheses={ids[2]: "keep h"})
    live = SESSION_STORE[sid]["state"]
    memory_before = copy.deepcopy((live.success_criteria, live.measurement_methods,
                                   live.test_hypotheses))
    store = webapp._get_store()
    proxy = _FailOnMutation(store._conn, fail_at)
    monkeypatch.setattr(store, "_conn", proxy)
    r = _post(client, sid, criteria={ids[0]: "new c"}, methods={ids[0]: "new m"},
              hypotheses={ids[0]: "new h", ids[2]: " "})
    monkeypatch.setattr(store, "_conn", proxy._conn)
    assert len(proxy.seen) == fail_at                  # earlier mutations DID run
    assert r.status_code == 503
    body = html.unescape(r.get_data(as_text=True))
    assert NOT_SAVED in body and SAVED_NOT_SHOWN not in body and OUTCOME_UNKNOWN not in body
    assert _durable(sid) == {ids[2]: "keep c"}
    assert _methods(sid) == {ids[2]: "keep m"}
    assert _hyps(sid) == {ids[2]: "keep h"}
    assert (live.success_criteria, live.measurement_methods,
            live.test_hypotheses) == memory_before


# ==========================================================================
# I-K — SAVED / NOT SAVED / UNKNOWN after a raised write
# ==========================================================================
def test_i_committed_then_raised_three_way_delta_is_saved(client, monkeypatch):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post(client, sid, hypotheses={ids[1]: "to delete", ids[2]: "omitted, untouched"})
    store = webapp._get_store()
    proxy = _CommitThenRaise(store._conn)
    monkeypatch.setattr(store, "_conn", proxy)
    r = _post(client, sid, criteria={ids[0]: "c"}, methods={ids[0]: "m"},
              hypotheses={ids[0]: "committed then raised", ids[1]: ""})
    monkeypatch.setattr(store, "_conn", proxy._conn)
    assert r.status_code == 302 and r.headers["Location"].endswith("/deliverable")
    expected = {ids[0]: "committed then raised", ids[2]: "omitted, untouched"}
    assert _hyps(sid) == expected and _memory(sid) == expected


def test_j_hypothesis_not_reflected_is_not_saved(client, monkeypatch):
    """Criterion already durable, hypothesis not: the COMPLETE submitted delta
    does not match -> NOT SAVED, never SAVED."""
    sid = _journey(client)
    ids = _live_ids(sid)
    _post(client, sid, criteria={ids[0]: "already there"})

    def failing_apply(self, project_id, criteria_delta, method_delta,
                      hypothesis_delta=None):
        raise sqlite3.OperationalError("injected: failed before commit")

    monkeypatch.setattr(SqliteRecordStore, "apply_planning_metadata_delta", failing_apply)
    r = _post(client, sid, criteria={ids[0]: "already there"},
              hypotheses={ids[0]: "never written"})
    assert r.status_code == 503 and NOT_SAVED in html.unescape(r.get_data(as_text=True))
    assert _hyps(sid) == {}


def test_k_ir01_unresolved_transaction_on_a_hypothesis_write_is_unknown(
        client, monkeypatch):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post(client, sid, criteria={ids[0]: "old c"}, hypotheses={ids[0]: "old h"})
    live = SESSION_STORE[sid]["state"]
    memory_before = copy.deepcopy(live.test_hypotheses)
    store = webapp._get_store()
    real_conn = store._conn
    monkeypatch.setattr(store, "_conn", _CommitAndRollbackFail(real_conn))
    r = _post(client, sid, criteria={ids[0]: "new c"}, hypotheses={ids[0]: "new h"})
    assert real_conn.in_transaction is True
    same = dict(real_conn.execute("SELECT experiment_id, test_hypothesis FROM %s "
                                  "WHERE project_id = ?" % TABLE, (sid,)).fetchall())
    assert same[ids[0]] == "new h"                          # own uncommitted view
    assert _independent(sid, ids[0]) == "old h"
    body = html.unescape(r.get_data(as_text=True))
    assert r.status_code == 503 and OUTCOME_UNKNOWN in body
    assert NOT_SAVED not in body and SAVED_NOT_SHOWN not in body
    assert live.test_hypotheses == memory_before            # not published
    monkeypatch.setattr(store, "_conn", real_conn)
    _restart()
    items = _reopened_items(sid)
    assert items[ids[0]]["test_hypothesis"] == "old h"
    assert items[ids[0]]["success_criterion"] == "old c"


@pytest.mark.parametrize("durable_h,hypotheses,expected", [
    ({"a": "h"}, {"a": "h"}, "saved"),
    ({}, {"a": None}, "saved"),                         # delete confirmed by absence
    ({"a": "h"}, {"a": None}, "not_saved"),             # delete not reflected
    ({"a": "old"}, {"a": "new"}, "not_saved"),
    ({"a": "h", "omitted": "x"}, {"a": "h"}, "saved"),  # omitted ignored
])
def test_i_j_confirmation_rule_covers_the_hypothesis_delta(
        monkeypatch, durable_h, hypotheses, expected):
    class _Store:
        def load_success_criteria(self, project_id):
            return (("a", "c"),)

        def load_measurement_methods(self, project_id):
            return ()

        def load_test_hypotheses(self, project_id):
            return tuple(durable_h.items())

    monkeypatch.setattr(webapp, "_get_store", lambda: _Store())
    assert webapp._resolve_criteria_write("p", {"a": "c"}, {}, hypotheses) == expected


def test_k_confirmation_rule_unreadable_hypotheses_is_unknown(monkeypatch):
    class _Store:
        def load_success_criteria(self, project_id):
            return (("a", "c"),)

        def load_measurement_methods(self, project_id):
            return ()

        def load_test_hypotheses(self, project_id):
            raise TestHypothesisCorrupt("malformed")

    monkeypatch.setattr(webapp, "_get_store", lambda: _Store())
    assert webapp._resolve_criteria_write("p", {"a": "c"}, {}, {"a": "h"}) == "unknown"
    # no hypothesis delta -> the hypotheses are not part of the comparison
    assert webapp._resolve_criteria_write("p", {"a": "c"}, {}) == "saved"


# ==========================================================================
# L-M — over-limit or NUL rejects the WHOLE submission
# ==========================================================================
def test_l_over_limit_hypothesis_rejects_the_whole_planning_delta(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    limit = webapp.MAX_TEST_HYPOTHESIS_LENGTH
    assert limit == MAX_TEST_HYPOTHESIS_LENGTH == 1000
    _post(client, sid, criteria={ids[2]: "pre c"}, hypotheses={ids[2]: "pre h"})
    r = _post(client, sid, criteria={ids[0]: "valid c"}, methods={ids[0]: "valid m"},
              hypotheses={ids[0]: "valid h", ids[1]: "x" * (limit + 1)})
    assert r.status_code == 400 and TOO_LONG in html.unescape(r.get_data(as_text=True))
    assert _durable(sid) == {ids[2]: "pre c"}
    assert _methods(sid) == {}
    assert _hyps(sid) == {ids[2]: "pre h"}
    assert _post(client, sid, hypotheses={ids[0]: "h" * limit}).status_code == 302
    assert _hyps(sid)[ids[0]] == "h" * limit                 # exactly the limit is kept


@pytest.mark.parametrize("value", ["\x00leading", "mid\x00dle", "trailing\x00"])
@pytest.mark.parametrize("lang", ["en", "ar"])
def test_m_nul_in_a_hypothesis_rejects_the_whole_submission(client, value, lang):
    sid = _journey(client)
    ids = _live_ids(sid)
    client.post("/ui-language", data={"lang": lang})
    r = _post(client, sid, criteria={ids[0]: "valid c"}, hypotheses={ids[1]: value})
    client.post("/ui-language", data={"lang": "en"})
    assert r.status_code == 400
    assert _durable(sid) == {} and _hyps(sid) == {}


def test_l_m_store_api_and_database_refuse_invalid_hypothesis_text(tmp_path):
    store, pid = _new_store_project(tmp_path, "invalid")
    try:
        for bad in ("", " padded ", "nul\x00", "x" * 1001, 7):
            with pytest.raises(TestHypothesisInvalid):
                store.apply_planning_metadata_delta(pid, {EID_SHAPE: "c"}, {},
                                                    {EID_SHAPE: bad})
        with pytest.raises(TestHypothesisInvalid):
            store.apply_planning_metadata_delta(pid, {}, {}, {"not-an-id": "h"})
        # validated WHOLE before the transaction: the criterion was not written
        assert store.load_success_criteria(pid) == ()
        assert store.load_test_hypotheses(pid) == ()
        with pytest.raises(sqlite3.IntegrityError):          # the DB CHECK backstop
            store._conn.execute("INSERT INTO %s VALUES (?, ?, ?)" % TABLE,
                                (pid, EID_SHAPE, "nul\x00inside"))
        store._conn.execute("ROLLBACK") if store._conn.in_transaction else None
    finally:
        store.close()


# ==========================================================================
# N — a rejected submission re-shows all three drafts, unsaved
# ==========================================================================
def test_n_rejected_submission_redisplays_all_three_drafts(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post(client, sid, hypotheses={ids[0]: "durable h"})
    r = _post(client, sid, criteria={ids[0]: "typed c"}, methods={ids[0]: "typed m"},
              hypotheses={ids[0]: "<b>typed h</b>", ids[1]: "y" * 1001})
    assert r.status_code == 400
    raw = r.get_data(as_text=True)
    assert 'id="draft-unsaved"' in raw
    assert html.unescape(_textarea(raw, HYP + ids[0])) == "<b>typed h</b>"
    assert "&lt;b&gt;typed h&lt;/b&gt;" in raw                   # escaped, not markup
    assert html.unescape(_textarea(raw, PREFIX + ids[0])) == "typed c"
    assert html.unescape(_textarea(raw, METHOD + ids[0])) == "typed m"
    assert _hyps(sid) == {ids[0]: "durable h"}                  # nothing saved


# ==========================================================================
# O-Q — unknown / stale ids; omitted fields; line-ending equivalence
# ==========================================================================
def test_o_unknown_hypothesis_id_is_rejected(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    r = _post(client, sid, criteria={ids[0]: "valid c"},
              hypotheses={"exp_v1_acknowledged_unknown_" + "9" * 32: "rogue"})
    assert r.status_code == 400 and NOT_CURRENT in html.unescape(r.get_data(as_text=True))
    assert _durable(sid) == {} and _hyps(sid) == {}


def test_p_omitted_fields_are_never_changed(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post(client, sid, criteria={ids[0]: "c0"}, methods={ids[0]: "m0"},
          hypotheses={ids[0]: "h0", ids[1]: "h1"})
    assert _post(client, sid, criteria={ids[0]: "c0 edited"}).status_code == 302
    assert _hyps(sid) == {ids[0]: "h0", ids[1]: "h1"}          # no hypothesis field sent
    assert _post(client, sid, hypotheses={ids[1]: "h1 edited"}).status_code == 302
    assert _hyps(sid) == {ids[0]: "h0", ids[1]: "h1 edited"}
    assert _durable(sid) == {ids[0]: "c0 edited"} and _methods(sid) == {ids[0]: "m0"}


def test_q_crlf_equivalent_hypothesis_is_not_rewritten(client, monkeypatch):
    sid = _journey(client)
    ids = _live_ids(sid)
    webapp._get_store().apply_planning_metadata_delta(
        sid, {}, {}, {ids[0]: "line one\nline two"})              # stored with LF
    seen = []
    real_apply = SqliteRecordStore.apply_planning_metadata_delta

    def spy(self, project_id, criteria_delta, method_delta, hypothesis_delta=None):
        seen.append(hypothesis_delta)
        return real_apply(self, project_id, criteria_delta, method_delta, hypothesis_delta)

    monkeypatch.setattr(SqliteRecordStore, "apply_planning_metadata_delta", spy)
    r = _post(client, sid, criteria={ids[1]: "unrelated edit"},
              hypotheses={ids[0]: "line one\r\nline two"})         # browser CRLF
    assert r.status_code == 302
    assert seen == [None]                                          # not part of the delta
    assert _raw_rows(sid) == [(ids[0], "line one\nline two")]      # bytes unchanged


# ==========================================================================
# R-S — stale preserved, never remapped; the same identity resolves again
# ==========================================================================
def test_r_s_stale_hypothesis_is_preserved_and_reattaches_by_identity(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    claim_id = [i for i in ids if "_reasoned_leading_claim_" in i][0]
    keep_id = ids[0]
    _post(client, sid, hypotheses={claim_id: "Braking is detected within 0.2 s",
                                   keep_id: "Ten stops give ten events"})
    _answer(client, sid, ELEC_DISPLACING_ANSWER)          # displaces the claim experiment
    current = _live_ids(sid)
    assert claim_id not in current and keep_id in current
    report = _report(client, sid)
    assert text("UI_SC_HYPOTHESIS_STALE", "en") in report
    assert "Braking is detected within 0.2 s" not in report   # never shown elsewhere
    with app.test_request_context():
        plan = webapp._deliverable_context(sid)[1]["section_11_prototype_test_plan"]
    assert [s["experiment_id"] for s in plan["stale_test_hypotheses"]] == [claim_id]
    assert all(it.get("test_hypothesis") != "Braking is detected within 0.2 s"
               for it in plan["items"])                        # never remapped
    assert _hyps(sid)[claim_id] == "Braking is detected within 0.2 s"   # preserved
    r, body = _criteria_page(client, sid)
    assert r.status_code == 200 and text("UI_SC_HYPOTHESIS_STALE", "en") in body
    assert _post(client, sid, hypotheses={claim_id: "retarget"}).status_code == 400
    record = _answered_record(sid, ELEC_DISPLACING_ANSWER)
    assert _correct(client, sid, record.record_id,
                    "The threshold will be chosen by measuring real stops.").status_code == 302
    _restart()
    items = _reopened_items(sid)
    assert items[claim_id]["test_hypothesis"] == "Braking is detected within 0.2 s"
    assert items[keep_id]["test_hypothesis"] == "Ten stops give ten events"


# ==========================================================================
# T-U — cold project without Resume; a session that is not a saved project
# ==========================================================================
def test_t_cold_project_edits_hypotheses_without_resume(client):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    _post(client, sid, hypotheses={eid: "cold hypothesis"})
    _restart()
    before = _progression_snapshot(sid)
    fresh = csrf_client(app)
    r, body = _criteria_page(fresh, sid)
    assert r.status_code == 200 and "cold hypothesis</textarea>" in body
    assert _post(fresh, sid, hypotheses={eid: "edited cold"}).status_code == 302
    assert _hyps(sid) == {eid: "edited cold"}
    assert _no_writable_session(sid)
    assert _progression_snapshot(sid) == before


def test_u_no_saved_project_refuses_and_names_the_hypothesis(client, tmp_path):
    from engine.idea_state import AcknowledgedUnknown, ASSUMPTION_INVENTORY
    store = SqliteRecordStore(str(tmp_path / "missing.sqlite"))
    try:
        with pytest.raises(ProjectNotFound):
            store.load_test_hypotheses("no-such-project")
        with pytest.raises(ProjectNotFound):
            store.apply_planning_metadata_delta("no-such-project", {}, {},
                                                {EID_SHAPE: "h"})
    finally:
        store.close()
    assert "test hypotheses" in NOT_A_PROJECT
    sid = "mem-only-th-" + "0" * 8
    state = IdeaState(idea_id=sid)
    state.domain = "electronics_electrical"
    state.acknowledged_unknowns.append(AcknowledgedUnknown(
        iteration=1, gap_context=ASSUMPTION_INVENTORY,
        verbatim="I do not know the lockout count", category_basis="explicit"))
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    eid = [it["experiment_id"] for it in _plan_items(state)][0]
    r = _post(client, sid, hypotheses={eid: "would only live in memory"})
    assert r.status_code == 409
    assert NOT_A_PROJECT in html.unescape(r.get_data(as_text=True))
    assert state.test_hypotheses == {}


def test_u_non_owner_and_anonymous_cannot_write_hypotheses(client):
    from tests.test_stage19_durable_success_criteria import _client_for
    owner, _aid = _client_for("owner-th@example.com")
    sid = _journey(owner)
    eid = _live_ids(sid)[0]
    assert _post(owner, sid, hypotheses={eid: "owner h"}).status_code == 302
    intruder, _ = _client_for("other-th@example.com")
    for c in (intruder, csrf_client(app)):
        r = _post(c, sid, hypotheses={eid: "intruder"})
        assert r.status_code == 302 and r.headers["Location"].endswith("/")
    assert _hyps(sid) == {eid: "owner h"}


# ==========================================================================
# V-Y — not Evidence; no readiness / progression change; CAP-08 / CAP-10 intact
# ==========================================================================
def _non_plan_sections(sid):
    """Every deliverable section except Section 11, through the real shared
    HTML / PDF deliverable seam."""
    with app.test_request_context():
        package = webapp._deliverable_context(sid)[1]
    return {k: v for k, v in package.items()
            if k != "section_11_prototype_test_plan" and "generated" not in k}


def test_v_w_hypothesis_is_not_evidence_and_changes_no_readiness(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    store = webapp._get_store()
    records_before = [assertion_to_dict(r) for r in store.load_contract(sid).assertions]
    evidence_before = store.load_readiness_evidence(sid)
    progression_before = _progression_snapshot(sid)
    sections_before = _non_plan_sections(sid)
    assert _post(client, sid, hypotheses={i: "I expect this to pass" for i in ids}
                 ).status_code == 302
    assert [assertion_to_dict(r) for r in store.load_contract(sid).assertions] \
        == records_before                                   # no record / Evidence row
    assert store.load_readiness_evidence(sid) == evidence_before
    assert _progression_snapshot(sid) == progression_before
    assert _non_plan_sections(sid) == sections_before
    _restart()
    assert _non_plan_sections(sid) == sections_before


def test_x_y_cap08_and_cap10_declarations_are_unchanged(client):
    """A project carrying a CAP-08 assumption -> answer dependency AND a CAP-10
    declared contradiction: a hypothesis save adds no record and changes
    neither declaration nor any progression, readiness or plan output."""
    from tests.test_cap08_assumption_dependency import (
        _web_project, _declare as _declare_dep, _rows, _progress, _cform,
    )
    from tests.test_cap10_declared_contradiction import _declare as _declare_conflict
    from tests.test_safe_question_routing_pf_q2 import _live
    sid, assumption, answered = _web_project(client)
    assert _declare_dep(client, sid, assumption, [answered[0]]).status_code == 302
    assert _cform(client, sid), "the CAP-10 form must be offered"
    assert _declare_conflict(client, sid, answered[:2]).status_code == 302
    rows_before = _rows(sid)
    dispositions = {p["disposition"] for p in rows_before}
    assert {"assumption_dependency_declared", "contradiction_declared"} <= dispositions
    progress_before = _progress(_live(sid))
    ids = _live_ids(sid)
    assert _post(client, sid, hypotheses={ids[0]: "The hinge holds the deck load"}
                 ).status_code == 302
    assert _rows(sid) == rows_before
    assert _progress(_live(sid)) == progress_before
    assert _hyps(sid) == {ids[0]: "The hinge holds the deck load"}


# ==========================================================================
# Z — report and PDF: the hypothesis when present, truthful absence otherwise
# ==========================================================================
def test_z_report_shows_the_hypothesis_escaped_and_truthful_absence(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post(client, sid, hypotheses={ids[1]: "<i>brighter</i> & sooner"})
    _restart()
    raw = csrf_client(app).get("/session/%s/deliverable" % sid).get_data(as_text=True)
    assert "&lt;i&gt;brighter&lt;/i&gt; &amp; sooner" in raw
    assert "<i>brighter</i>" not in raw
    assert '<span class="user-hypothesis" dir="auto">' in raw
    body = html.unescape(raw)
    assert body.count(text("UI_DELIV_HYPOTHESIS_DEFINED", "en")) == 1
    assert body.count(text("UI_DELIV_HYPOTHESIS_ABSENT", "en")) == len(ids) - 1
    for phrase in ("has been validated", "is confirmed", "is resolved"):
        assert phrase not in body.lower()


def test_z_pdf_source_carries_the_hypothesis_after_restart(client, monkeypatch):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    _post(client, sid, hypotheses={eid: "PDF carries this durable hypothesis"})
    _restart()
    source = html.unescape(_pdf_source(monkeypatch, sid))
    assert "PDF carries this durable hypothesis" in source
    assert text("UI_DELIV_HYPOTHESIS_DEFINED", "en") in source


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_z_planning_page_and_report_are_bilingual(client, lang):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post(client, sid, hypotheses={ids[0]: "أتوقع أن يضيء المصباح"})
    client.post("/ui-language", data={"lang": lang})
    r, body = _criteria_page(client, sid)
    assert r.status_code == 200
    for key in ("UI_SC_HYPOTHESIS_INTRO", "UI_SC_HYPOTHESIS_LABEL",
                "UI_SC_HYPOTHESIS_PLACEHOLDER", "UI_B_SC_004", "UI_SC_SAVE_CLEAR"):
        assert text(key, lang) in body, key
    assert "أتوقع أن يضيء المصباح</textarea>" in body              # verbatim
    report = _report(client, sid)
    assert text("UI_DELIV_HYPOTHESIS_DEFINED", lang) in report
    assert text("UI_DELIV_HYPOTHESIS_ABSENT", lang) in report
    r = _post(client, sid, hypotheses={ids[1]: "y" * 1001})
    assert r.status_code == 400
    assert text("UI_SC_ERR_HYPOTHESIS_TOO_LONG", lang) in html.unescape(
        r.get_data(as_text=True))
    client.post("/ui-language", data={"lang": "en"})


def test_z_every_new_ui_key_has_english_and_arabic_copy():
    from web import ui_text
    keys = ("UI_SC_HYPOTHESIS_INTRO", "UI_SC_HYPOTHESIS_LABEL",
            "UI_SC_HYPOTHESIS_PLACEHOLDER", "UI_SC_HYPOTHESIS_STALE",
            "UI_SC_ERR_HYPOTHESIS_TOO_LONG", "UI_DELIV_HYPOTHESIS_DEFINED",
            "UI_DELIV_HYPOTHESIS_ABSENT_LABEL", "UI_DELIV_HYPOTHESIS_ABSENT")
    for key in keys:
        entry = ui_text.UI_STRINGS[key]
        assert entry["en"].strip() and entry["ar"].strip(), key
        assert entry["en"] != entry["ar"], key
    assert "(Test Hypothesis)" in ui_text.UI_STRINGS["UI_SC_HYPOTHESIS_LABEL"]["ar"]
    intro = ui_text.UI_STRINGS["UI_SC_HYPOTHESIS_INTRO"]["en"]
    assert "what you expect to happen in this test" in intro
    assert "does not make it correct or validated" in intro
    en = " ".join(ui_text.UI_STRINGS[k]["en"] for k in keys).lower()
    for word in ("has been validated", "is confirmed", "verified", "passed", "proven"):
        assert word not in en
    # every outcome message now names all three concepts, EN and AR
    for key in ("UI_SC_ERR_NOT_SAVED_PROJECT", "UI_SC_ERR_NOT_SAVED",
                "UI_SC_ERR_SAVED_NOT_SHOWN", "UI_SC_ERR_OUTCOME_UNKNOWN",
                "UI_SC_ERR_CRITERIA_UNAVAILABLE", "UI_SC_ERR_PLAN_UNAVAILABLE"):
        assert "test hypotheses" in ui_text.UI_STRINGS[key]["en"], key
        assert "فرضيات الاختبار" in ui_text.UI_STRINGS[key]["ar"], key
    assert ui_text.localize_message(TOO_LONG, "ar") == \
        ui_text.UI_STRINGS["UI_SC_ERR_HYPOTHESIS_TOO_LONG"]["ar"]


# ==========================================================================
# Store — schema, migration, loader semantics, corruption, IR-01, isolation
# ==========================================================================
def test_store_fresh_table_has_exactly_the_bounded_shape(tmp_path):
    path = str(tmp_path / "shape.sqlite")
    SqliteRecordStore(path).close()
    con = sqlite3.connect(path)
    try:
        cols = [(r[1], r[2], r[3], r[5]) for r in con.execute("PRAGMA table_info(%s)" % TABLE)]
        fks = [(r[2], r[3], r[4]) for r in con.execute("PRAGMA foreign_key_list(%s)" % TABLE)]
        others = {t: [(r[1], r[2], r[3], r[5]) for r in
                      con.execute("PRAGMA table_info(%s)" % t)]
                  for t in ("prototype_plan_metadata", "prototype_measurement_methods")}
    finally:
        con.close()
    # ONLY the hypothesis text: no provenance, variable, result, validation,
    # readiness, confidence or PASS/FAIL column.
    assert cols == [("project_id", "TEXT", 1, 1), ("experiment_id", "TEXT", 1, 2),
                    ("test_hypothesis", "TEXT", 1, 0)]
    assert fks == [("projects", "project_id", "project_id")]
    assert others == {   # the sibling sidecars are NOT widened
        "prototype_plan_metadata": [("project_id", "TEXT", 1, 1),
                                    ("experiment_id", "TEXT", 1, 2),
                                    ("success_criterion", "TEXT", 1, 0)],
        "prototype_measurement_methods": [("project_id", "TEXT", 1, 1),
                                          ("experiment_id", "TEXT", 1, 2),
                                          ("measurement_method", "TEXT", 1, 0)]}


def test_store_existing_database_migrates_additively_and_idempotently(client):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    _post(client, sid, criteria={eid: "pre c"}, methods={eid: "pre m"})
    before_contract = [assertion_to_dict(r)
                       for r in webapp._get_store().load_contract(sid).assertions]
    _restart()
    con = sqlite3.connect(_db_path())                   # a database from before SLICE 3
    con.execute("DROP TABLE %s" % TABLE)
    con.commit()
    con.close()
    store = SqliteRecordStore(_db_path())
    try:
        assert [assertion_to_dict(r) for r in store.load_contract(sid).assertions] \
            == before_contract
        assert store.load_success_criteria(sid) == ((eid, "pre c"),)
        assert store.load_measurement_methods(sid) == ((eid, "pre m"),)
        assert store.load_test_hypotheses(sid) == ()                 # zero rows -> ()
        store.apply_planning_metadata_delta(sid, {}, {}, {eid: "kept"})
    finally:
        store.close()
    for _ in range(3):                                   # re-initialization is idempotent
        SqliteRecordStore(_db_path()).close()
    assert _raw_rows(sid) == [(eid, "kept")]


@pytest.mark.parametrize("corruption", [
    ("valid_id", "  untrimmed  "),
    ("valid_id", b"blob-value"),
    ("valid_id", "nul\x00inside"),
    ("not-an-experiment-id", "fine text"),
])
def test_store_corrupt_row_fails_the_whole_collection_and_section_11_closed(
        client, corruption):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post(client, sid, criteria={ids[0]: "good c"}, hypotheses={ids[0]: "good h"})
    bad_id, bad_value = corruption
    _insert_raw(sid, ids[1] if bad_id == "valid_id" else bad_id, bad_value)
    with pytest.raises(TestHypothesisCorrupt):
        webapp._get_store().load_test_hypotheses(sid)
    r, body = _criteria_page(client, sid)
    assert r.status_code == 503 and UNAVAILABLE in body
    assert 'name="%s' % HYP not in body and "good h" not in body
    assert _post(client, sid, hypotheses={ids[2]: "blocked"}).status_code == 503
    r = client.get("/session/%s/deliverable" % sid)
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    assert len(_raw_rows(sid)) == 2                                   # not repaired
    assert _durable(sid) == {ids[0]: "good c"}


def test_store_corrupt_hypotheses_never_yield_a_partial_attachment(client):
    from engine.idea_state import SuccessCriterion
    sid = _journey(client)
    ids = _live_ids(sid)
    _post(client, sid, criteria={ids[0]: "durable good c"})
    _insert_raw(sid, ids[1], "\tbad\t")
    state = SESSION_STORE[sid]["state"]
    state.success_criteria = {"prior": SuccessCriterion("carrier c")}
    state.test_hypotheses = {"prior": TestHypothesis("carrier h")}
    assert webapp._attach_planning_metadata(sid, state) is False
    assert {k: v.criterion for k, v in state.success_criteria.items()} == {"prior": "carrier c"}
    assert {k: v.hypothesis for k, v in state.test_hypotheses.items()} == {"prior": "carrier h"}


def test_store_corrupt_hypothesis_never_blocks_progression(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    _insert_raw(sid, ids[0], " bad ")
    _restart()
    fresh = csrf_client(app)
    assert fresh.get("/session/%s" % sid).status_code in (200, 302)
    assert _progression_snapshot(sid)                          # reconstruction unaffected


def test_store_ir01_refuses_hypothesis_reads_and_writes_when_unsafe(tmp_path):
    store, pid = _new_store_project(tmp_path, "unsafe")
    try:
        store.apply_planning_metadata_delta(pid, {}, {}, {EID_SHAPE: "h"})
        real = store._conn
        store._conn = _CommitAndRollbackFail(real)
        with pytest.raises(sqlite3.OperationalError):
            store.apply_planning_metadata_delta(pid, {}, {}, {EID_SHAPE: "uncommitted"})
        store._conn = real
        assert real.in_transaction is True
        with pytest.raises(RecordStoreConnectionUnsafe):
            store.load_test_hypotheses(pid)
        with pytest.raises(RecordStoreConnectionUnsafe):
            store.apply_planning_metadata_delta(pid, {}, {}, {EID_SHAPE: "h2"})
        real.execute("ROLLBACK")
        with pytest.raises(RecordStoreConnectionUnsafe):       # still never trusted
            store.load_test_hypotheses(pid)
    finally:
        store.close()


def test_store_identical_experiment_ids_in_two_projects_stay_isolated(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "iso.sqlite"))
    try:
        a = store.create_project(ProjectRecordContract.from_state(IdeaState(idea_id="a")),
                                 project_id="p-a")
        b = store.create_project(ProjectRecordContract.from_state(IdeaState(idea_id="b")),
                                 project_id="p-b")
        store.apply_planning_metadata_delta(a, {}, {}, {EID_SHAPE: "A"})
        store.apply_planning_metadata_delta(b, {}, {}, {EID_SHAPE: "B"})
        store.apply_planning_metadata_delta(a, {}, {}, {EID_SHAPE: None})
        assert store.load_test_hypotheses(a) == ()
        assert store.load_test_hypotheses(b) == ((EID_SHAPE, "B"),)
    finally:
        store.close()


# ==========================================================================
# Carrier and identity — one typed field; experiment identity unchanged
# ==========================================================================
def test_idea_state_carries_one_typed_hypothesis_field():
    names = {f.name for f in dataclasses.fields(IdeaState)}
    assert "test_hypotheses" in names
    assert IdeaState(idea_id="x").test_hypotheses == {}
    assert [f.name for f in dataclasses.fields(TestHypothesis)] == ["hypothesis", "provenance"]
    assert TestHypothesis("h").provenance == "user_defined"


def test_experiment_identity_and_generated_fields_are_unchanged(client):
    from engine.deliverable_assembler import _experiment_id, assemble_deliverable
    sid = _journey(client)
    before = {it["experiment_id"]: it for it in _plan_items(SESSION_STORE[sid]["state"])}
    ids = list(before)
    _post(client, sid, hypotheses={ids[0]: "calipers show under 1 mm"})
    after = {it["experiment_id"]: it for it in _plan_items(SESSION_STORE[sid]["state"])}
    assert list(after) == ids
    for eid, item in after.items():
        src = item["traceability"]
        assert _experiment_id(src["source_type"], src["content"]) == eid
        extra = {"test_hypothesis", "test_hypothesis_provenance"} if eid == ids[0] else set()
        assert set(item) == set(before[eid]) | extra              # additive only
        for key in before[eid]:
            assert item[key] == before[eid][key], key
    plan = assemble_deliverable(SESSION_STORE[sid]["state"])["section_11_prototype_test_plan"]
    assert "stale_test_hypotheses" not in plan


def test_retention_inventory_states_the_factual_behaviour():
    import os
    path = os.path.join(os.path.dirname(__file__), "..", "docs", "DATA_RETENTION_POLICY.md")
    with open(path, encoding="utf-8") as fh:
        doc = " ".join(fh.read().split())
    assert "`prototype_test_hypotheses`" in doc
    assert "test hypotheses" in doc.lower()
    assert "NOT an erasure capability" in doc
