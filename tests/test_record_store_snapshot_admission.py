"""Stage 35 — first bounded slice — R1 snapshot participation (BASE RED, file R).

Implementation contract ``docs/governance/STAGE35_DISCLOSURE_EXPORT_FIRST_SLICE_IMPLEMENTATION_CONTRACT.md``
§3.2 and §14 (R1–R13): the six named readers are admitted inside a snapshot the
store itself acquired, and nowhere else; every other IR-01 behaviour is unchanged.

Real on-disk SQLite (autouse conftest isolation); the real store; no mocks.
"""
import inspect
import sqlite3

import pytest

import web.app as webapp
from engine import experiment_result as er
from engine.record_store import (
    ProjectNotFound, RecordStoreConnectionUnsafe, SqliteRecordStore,
)
from tests.csrf_client import csrf_client

SIX = ("load_interface_dependencies", "load_success_criteria",
       "load_measurement_methods", "load_test_hypotheses", "load_test_variables",
       "load_result_events")
EID = "exp_stage35_r1_probe"
SEED = ("A folding ramp for wheelchairs with a spring latch that locks the deck "
        "flat on a step.")


@pytest.fixture()
def project():
    """A durable project with one stored value in each planning collection and
    one Result event, so each reader returns non-trivial data."""
    webapp.app.config["TESTING"] = True
    with csrf_client(webapp.app) as c:
        r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
        assert r.status_code == 302
        pid = r.headers["Location"].rsplit("/", 1)[-1]
    store = webapp._get_store()
    store.apply_planning_metadata_delta(pid, {EID: "criterion"}, {EID: "method"},
                                        {EID: "hypothesis"}, {EID: "variable"})
    event = er.recorded_root(EID, "observed", er.ResultContext("Experiment"))
    store.append_result_event(pid, event, "a" * 32)
    return store, pid


def _read_all(store, pid):
    return {name: getattr(store, name)(pid) for name in SIX}


def _flag(store):
    return getattr(store, "_read_snapshot_owned", None)


def test_r1_six_readers_admitted_inside_a_healthy_snapshot(project):
    store, pid = project
    standalone = _read_all(store, pid)
    with store.read_snapshot():
        inside = _read_all(store, pid)
    assert inside == standalone
    assert standalone["load_success_criteria"] == ((EID, "criterion"),)
    assert len(standalone["load_result_events"]) == 1


def test_r2_six_readers_standalone_unchanged(project):
    store, pid = project
    assert store.committed_state_readable()
    first = _read_all(store, pid)
    assert first == _read_all(store, pid)
    for name in SIX:
        with pytest.raises(ProjectNotFound):
            getattr(store, name)("no-such-project")
    assert store.committed_state_readable()


def test_r3_bare_caller_owned_transaction_refused(project):
    store, pid = project
    store._conn.execute("BEGIN IMMEDIATE")
    try:
        for name in SIX:
            with pytest.raises(RecordStoreConnectionUnsafe):
                getattr(store, name)(pid)
        # A no-op read_snapshot() inside the caller-owned transaction grants nothing.
        with store.read_snapshot():
            assert not _flag(store)
            for name in SIX:
                with pytest.raises(RecordStoreConnectionUnsafe):
                    getattr(store, name)(pid)
    finally:
        store._conn.execute("ROLLBACK")


def test_r4_sticky_unsafe_state_refused_inside_and_outside(project):
    store, pid = project
    with store.read_snapshot():
        store._connection_unsafe = True
        try:
            for name in SIX:
                with pytest.raises(RecordStoreConnectionUnsafe):
                    getattr(store, name)(pid)
        finally:
            store._connection_unsafe = False
    store._connection_unsafe = True
    try:
        for name in SIX:
            with pytest.raises(RecordStoreConnectionUnsafe):
                getattr(store, name)(pid)
        with store.read_snapshot():
            for name in SIX:
                with pytest.raises(RecordStoreConnectionUnsafe):
                    getattr(store, name)(pid)
    finally:
        store._connection_unsafe = False


def test_r5_nested_snapshot_neither_sets_nor_clears_the_evidence(project):
    store, pid = project
    assert _flag(store) is False
    with store.read_snapshot():
        assert _flag(store) is True
        with store.read_snapshot():
            assert _flag(store) is True
            _read_all(store, pid)
        assert _flag(store) is True
        after_inner = _read_all(store, pid)
    assert _flag(store) is False
    assert after_inner == _read_all(store, pid)


def test_r6_no_op_branch_grants_no_admission(project):
    store, pid = project
    store._conn.execute("BEGIN")
    try:
        assert not store.committed_state_readable()
        with store.read_snapshot():
            assert _flag(store) is False
            with pytest.raises(RecordStoreConnectionUnsafe):
                store.load_success_criteria(pid)
        assert _flag(store) is False
    finally:
        store._conn.execute("ROLLBACK")


def test_r7_release_failure_keeps_todays_handling(project):
    store, pid = project
    with store.read_snapshot():
        _read_all(store, pid)
        # Take the snapshot away mid-body and open another transaction so the
        # RELEASE fails AND leaves the connection unresolved.
        store._conn.execute("ROLLBACK")
        store._conn.execute("BEGIN")
    assert store._connection_unsafe is True
    assert _flag(store) is False
    assert not store.committed_state_readable()
    store._conn.execute("ROLLBACK")
    store._connection_unsafe = False


def test_r8_writers_still_refused_inside_a_read_snapshot(project):
    store, pid = project
    before = _read_all(store, pid)
    with store.read_snapshot():
        with pytest.raises(RecordStoreConnectionUnsafe):
            store.apply_planning_metadata_delta(pid, {EID: "changed"}, {})
        event = er.recorded_root(EID, "again", er.ResultContext("Experiment"))
        with pytest.raises(RecordStoreConnectionUnsafe):
            store.append_result_event(pid, event, "b" * 32)
        assert _read_all(store, pid) == before
    assert _read_all(store, pid) == before


def test_r9_lifetime_expiry_returns_to_standalone_behaviour(project):
    store, pid = project
    with store.read_snapshot():
        _read_all(store, pid)
    assert _flag(store) is False
    store._conn.execute("BEGIN IMMEDIATE")
    try:
        for name in SIX:
            with pytest.raises(RecordStoreConnectionUnsafe):
                getattr(store, name)(pid)
    finally:
        store._conn.execute("ROLLBACK")


def test_r10_snapshot_lost_underneath_refuses_the_next_admission(project):
    store, pid = project
    with store.read_snapshot():
        _read_all(store, pid)
        store._conn.execute("ROLLBACK")          # the read transaction ends underneath
        assert _flag(store) is True
        for name in SIX:
            with pytest.raises(RecordStoreConnectionUnsafe):
                getattr(store, name)(pid)
        # The composer's step-5 check sees the loss even with no R1 read.
        assert store.committed_state_readable() is True
    assert _flag(store) is False


def test_r11_committed_confirmation_readers_refuse_inside_a_snapshot(project):
    store, pid = project
    with store.read_snapshot():
        with pytest.raises(RecordStoreConnectionUnsafe):
            store.committed_result_event_for_submission(pid, "a" * 32)
    assert store.committed_result_event_for_submission(pid, "a" * 32) is not None


def test_r12_no_global_relaxation():
    src_refuse = inspect.getsource(SqliteRecordStore._refuse_uncommitted_reads)
    assert "committed_state_readable()" in src_refuse
    assert "_read_snapshot_owned" not in src_refuse
    src_readable = inspect.getsource(SqliteRecordStore.committed_state_readable)
    assert "_read_snapshot_owned" not in src_readable
    guard = inspect.getsource(SqliteRecordStore._admit_snapshot_read)
    assert guard.index("_connection_unsafe") < guard.index("_read_snapshot_owned") \
        < guard.index("_refuse_uncommitted_reads()")
    source = inspect.getsource(SqliteRecordStore)
    # Exactly six substitutions.
    assert source.count("self._admit_snapshot_read()") == 6
    for name in SIX:
        body = inspect.getsource(getattr(SqliteRecordStore, name))
        assert "self._admit_snapshot_read()" in body
        assert "self._refuse_uncommitted_reads()" not in body
    # The ownership evidence is written only by read_snapshot() and __init__.
    writers = [line for line in source.splitlines()
               if "self._read_snapshot_owned =" in line]
    assert len(writers) == 3
    snapshot_src = inspect.getsource(SqliteRecordStore.read_snapshot)
    assert snapshot_src.count("self._read_snapshot_owned =") == 2


def test_r13_requirement_quantities_is_not_an_r1_reader(project):
    store, pid = project
    body = inspect.getsource(SqliteRecordStore.load_requirement_quantities)
    assert "_admit_snapshot_read" not in body
    standalone = store.load_requirement_quantities(pid)
    with store.read_snapshot():
        inside = store.load_requirement_quantities(pid)
    assert inside == standalone


def test_r_evidence_is_not_durable(project, tmp_path):
    store, pid = project
    with store.read_snapshot():
        pass
    tables = {row[0] for row in store._conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'")}
    assert not any("snapshot" in t for t in tables)
    fresh = SqliteRecordStore(str(tmp_path / "fresh.sqlite"))
    try:
        assert fresh._read_snapshot_owned is False
    finally:
        fresh.close()


def test_r_savepoint_failure_sets_no_evidence(project, monkeypatch):
    store, pid = project

    class _Conn:
        def __init__(self, real):
            self._real = real

        def execute(self, sql, *a):
            if sql.startswith("SAVEPOINT"):
                raise sqlite3.OperationalError("injected")
            return self._real.execute(sql, *a)

        def __getattr__(self, name):
            return getattr(self._real, name)

    real = store._conn
    monkeypatch.setattr(store, "_conn", _Conn(real))
    with pytest.raises(sqlite3.OperationalError):
        with store.read_snapshot():
            pass
    assert _flag(store) is False
