"""STAGE15-OBSERVATION-WITHDRAW-01 — terminal withdrawal of ONE recorded
interface check.

The inventor may withdraw one recorded check so it no longer counts as a
current record. ONE appended terminal event through the existing writer: a
fresh ``obs-`` identity, ``event_kind`` ``WITHDRAWAL``, the owner's fixed
internal marker, no context and no reason; the whole chain stays in the
history (withdrawal is not erasure) and nothing may follow it. The table gains
ONE closed ``event_kind`` column and its order column is renamed
``observation_seq`` -> ``observation_event_seq`` (the downgrade guard), both
atomically inside the store's migration transaction. Capacity: 200 ordinary
events plus ONE reserved withdrawal per root (at most 400). Current counts use
the current-chain projection.
"""
import os
import re
import sqlite3
import threading

import pytest

import web.app as appmod
from engine import interface_observation as io
from engine import record_store as rs
from engine.readiness_snapshot import readiness_snapshot
from engine.record_store import (
    INTERFACE_OBSERVATION_EXACT_REPLAY, InterfaceObservationCapReached,
    InterfaceObservationConflict, InterfaceObservationRejected,
    InterfaceObservationsCorrupt, RecordStoreConnectionUnsafe, SqliteRecordStore)
from tests.csrf_client import csrf_client
from tests.test_stage15_integrated_invention_entry import (
    _CommitAndRollbackFail, _pdf_source)
from tests.test_stage15_interface_observations import (
    OBS, OBS2, TABLE, _body, _correct_form, _events, _forms, _observe, _page,
    _page_raw, _record_form, _root, _rows, _store, _store_project,
    _two_interfaces)
from tests.test_stage15_interface_preparation import (
    ACCEPT, COND, EVID, F_A, F_C, F_E, _integrated_with_interface, _prep_rows, _save)
from tests.test_stage15_subsystem_interface_declaration import _raw
from tests.test_stage19_durable_success_criteria import (
    _CommitThenRaise, _client_for, _db_path, _progression_snapshot, _restart)
from web import ui_text

MARKER = io.WITHDRAWAL_MARKER
WITHDRAW = "/session/%s/interface-observation/withdraw"
IFC_A = "ifc-" + "a" * 32
IFC_B = "ifc-" + "b" * 32


@pytest.fixture
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


def _withdraw_forms(raw):
    forms = []
    for body in re.findall(
            r'<form method="POST" action="[^"]*interface-observation/withdraw"[^>]*>(.*?)</form>',
            raw, re.S):
        fields = dict(re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]*)"', body))
        forms.append({k: _unescape(v) for k, v in fields.items()})
    return forms


def _unescape(value):
    import html
    return html.unescape(value)


def _withdraw_form(c, sid, head_id):
    [form] = [f for f in _withdraw_forms(_page_raw(c, sid)) if f.get("supersedes") == head_id]
    return form


def _withdraw(c, sid, form, confirm=True):
    data = dict(form)
    if confirm:
        data["withdraw_confirm"] = "yes"
    return c.post(WITHDRAW % sid, data=data)


def _check(c, sid, iid, text=OBS):
    _observe(c, sid, _record_form(c, sid, iid), text)
    return [e for e in _events(sid) if e.supersedes_observation_id is None][-1]


def _key(n):
    return "k%040d" % n


def _status_count(page, lang="en"):
    return ui_text.text("UI_S15_ST_CHECKS_COUNT", lang)


# ==========================================================================
# W. the semantic owner (pure)
# ==========================================================================
def test_w1_a_withdrawal_is_a_terminal_marker_successor_decided_by_kind_not_text():
    root = _root(IFC_A)
    w = io.recorded_withdrawal(IFC_A, root.observation_id)
    assert io.is_valid_observation_id(w.observation_id)            # a fresh obs- identity
    assert w.event_kind == io.EVENT_WITHDRAWAL and io.is_withdrawal(w)
    assert w.observation_text == MARKER and w.context is None
    assert io.validate_observation_history([root, w]) == (root, w)
    # ordinary text equal to the marker stays an ordinary observation
    plain = io.recorded_root(IFC_A, MARKER, io.ObservationContext())
    fix = io.recorded_correction(IFC_A, MARKER, plain.observation_id)
    assert plain.event_kind == fix.event_kind == io.EVENT_OBSERVATION
    assert not io.is_withdrawal(plain) and not io.is_withdrawal(fix)
    assert len(io.current_observation_chains(io.validate_observation_history([plain, fix]))) == 1
    for bad in (
            io.InterfaceObservation(w.observation_id, IFC_A, "other", root.observation_id,
                                    w.recorded_at, None, io.EVENT_WITHDRAWAL),
            io.InterfaceObservation(w.observation_id, IFC_A, MARKER, None, w.recorded_at,
                                    io.ObservationContext(), io.EVENT_WITHDRAWAL),
            io.InterfaceObservation(w.observation_id, IFC_A, MARKER, root.observation_id,
                                    w.recorded_at, io.ObservationContext(), io.EVENT_WITHDRAWAL),
            io.InterfaceObservation(w.observation_id, IFC_A, "x", None, w.recorded_at,
                                    io.ObservationContext(), "BOGUS")):
        with pytest.raises(io.ObservationError):
            io.validate_observation_history([root, bad])
        assert not io.is_withdrawal(bad)


def test_w2_terminality_forks_cross_interface_and_double_withdrawal_are_refused():
    root = _root(IFC_A)
    w = io.recorded_withdrawal(IFC_A, root.observation_id)
    fix = io.recorded_correction(IFC_A, "fix", root.observation_id)
    for bad, why in (
            ([root, w, io.recorded_correction(IFC_A, "late", w.observation_id)], "terminal"),
            ([root, w, io.recorded_withdrawal(IFC_A, w.observation_id)], "terminal"),
            ([root, fix, io.recorded_withdrawal(IFC_A, root.observation_id)], "two successors"),
            ([root, io.recorded_withdrawal(IFC_B, root.observation_id)], "crosses interfaces"),
            ([io.recorded_withdrawal(IFC_A, root.observation_id), root], "no earlier event")):
        with pytest.raises(io.ObservationError, match=why):
            io.validate_observation_history(bad)


def test_w3_capacity_is_200_ordinary_plus_one_withdrawal_per_root():
    roots = [_root(IFC_A, "r%d" % i) for i in range(io.MAX_OBSERVATIONS_PER_PROJECT)]
    full = roots + [io.recorded_withdrawal(IFC_A, r.observation_id) for r in roots]
    assert len(full) == io.MAX_TOTAL_OBSERVATION_EVENTS == 400
    assert io.validate_observation_history(full) == tuple(full)
    with pytest.raises(io.ObservationError, match="ordinary"):
        io.validate_observation_history(roots + [_root(IFC_A, "r200")])
    with pytest.raises(io.ObservationError):                       # never replenished
        io.validate_observation_history(full + [_root(IFC_A, "after")])


def test_w4_full_history_keeps_withdrawn_chains_and_current_drops_them():
    a, b = _root(IFC_A, "first"), _root(IFC_A, "second")
    fix = io.recorded_correction(IFC_A, "first, corrected", a.observation_id)
    w = io.recorded_withdrawal(IFC_A, fix.observation_id)
    events = io.validate_observation_history([a, b, fix, w])
    full = io.observation_chains(events, IFC_A)
    assert [c["root"] for c in full] == [a, b]
    assert full[0]["withdrawal"] == w and full[0]["head"] == fix
    assert full[0]["history"] == [a, fix]                          # the marker is never history
    assert [c["root"] for c in io.current_observation_chains(events, IFC_A)] == [b]
    w2 = io.recorded_withdrawal(IFC_A, b.observation_id)
    gone = io.validate_observation_history([a, b, fix, w, w2])
    assert io.current_observation_chains(gone) == [] and len(io.observation_chains(gone)) == 2
    assert io.head_ids(gone) == {w.observation_id, w2.observation_id}


def test_w5_material_comparison_includes_the_action_kind():
    root = _root(IFC_A)
    w = io.recorded_withdrawal(IFC_A, root.observation_id)
    fix = io.recorded_correction(IFC_A, MARKER, root.observation_id)
    assert io.same_observation_material(w, io.recorded_withdrawal(IFC_A, root.observation_id))
    assert not io.same_observation_material(w, fix)
    assert not io.same_observation_material(fix, w)


# ==========================================================================
# S. the store: append, terminality, replay, capacity, races, SQL shape
# ==========================================================================
def test_s1_one_withdrawal_appends_at_a_head_and_every_other_target_is_refused(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "s1.db"))
    pid, [one, two] = _store_project(store, 2)
    other, [theirs] = _store_project(store)
    a, b = one.interface_id, two.interface_id
    root = store.append_interface_observation(pid, _root(a), "r1")[1]
    fix = store.append_interface_observation(
        pid, io.recorded_correction(a, OBS2, root.observation_id), "r2")[1]
    their_root = store.append_interface_observation(other, _root(theirs.interface_id), "t1")[1]
    for target, iid in ((root.observation_id, a),                  # not the head
                        (fix.observation_id, b),                   # another interface
                        (their_root.observation_id, a),            # another project
                        ("obs-" + "f" * 32, a)):                   # unknown
        with pytest.raises(InterfaceObservationRejected):
            store.append_interface_observation(pid, io.recorded_withdrawal(iid, target), _key(1))
    with pytest.raises(InterfaceObservationRejected):              # a foreign interface
        store.append_interface_observation(
            pid, io.recorded_withdrawal(theirs.interface_id, their_root.observation_id), _key(1))
    w = store.append_interface_observation(
        pid, io.recorded_withdrawal(a, fix.observation_id), _key(2))[1]
    events = store.load_interface_observations(pid)
    assert events == (root, fix, w)                                # nothing rewritten
    for event in (io.recorded_correction(a, OBS, w.observation_id),
                  io.recorded_withdrawal(a, w.observation_id),
                  io.recorded_withdrawal(a, fix.observation_id)):
        with pytest.raises(InterfaceObservationRejected):
            store.append_interface_observation(pid, event, _key(3))
    assert store.load_interface_observations(pid) == events
    assert store.load_interface_observations(other) == (their_root,)
    store.close()


def test_s2_exact_replay_writes_nothing_and_cross_action_replay_conflicts(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "s2.db"))
    pid, [item] = _store_project(store)
    iid = item.interface_id
    root = store.append_interface_observation(pid, _root(iid), "r1")[1]
    w = io.recorded_withdrawal(iid, root.observation_id)
    store.append_interface_observation(pid, w, _key(1))
    outcome, stored = store.append_interface_observation(
        pid, io.recorded_withdrawal(iid, root.observation_id), _key(1))
    assert outcome == INTERFACE_OBSERVATION_EXACT_REPLAY and stored == w
    with pytest.raises(InterfaceObservationConflict):              # same key, other action
        store.append_interface_observation(
            pid, io.recorded_correction(iid, MARKER, root.observation_id), _key(1))
    second = store.append_interface_observation(pid, _root(iid, OBS2), "r2")[1]
    with pytest.raises(InterfaceObservationConflict):              # ordinary key reused
        store.append_interface_observation(
            pid, io.recorded_withdrawal(iid, second.observation_id), "r2")
    assert len(store.load_interface_observations(pid)) == 3
    store.close()


def test_s3_capacity_extremes_reserve_one_withdrawal_per_root_and_never_reclaim(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "s3.db"))
    pid, [item] = _store_project(store)
    iid = item.interface_id
    roots = [store.append_interface_observation(pid, _root(iid, "c%d" % i), _key(i))[1]
             for i in range(io.MAX_OBSERVATIONS_PER_PROJECT)]
    with pytest.raises(InterfaceObservationCapReached):
        store.append_interface_observation(pid, _root(iid, "over"), _key(900))
    with pytest.raises(InterfaceObservationCapReached):
        store.append_interface_observation(
            pid, io.recorded_correction(iid, "over", roots[0].observation_id), _key(901))
    outcome, stored = store.append_interface_observation(pid, _root(iid, "c7"), _key(7))
    assert outcome == INTERFACE_OBSERVATION_EXACT_REPLAY and stored == roots[7]
    for i, root in enumerate(roots):
        store.append_interface_observation(
            pid, io.recorded_withdrawal(iid, root.observation_id), _key(1000 + i))
    assert len(store.load_interface_observations(pid)) == io.MAX_TOTAL_OBSERVATION_EVENTS
    with pytest.raises(InterfaceObservationCapReached):            # nothing reclaimed
        store.append_interface_observation(pid, _root(iid, "after"), _key(902))
    assert store.append_interface_observation(
        pid, io.recorded_withdrawal(iid, roots[3].observation_id),
        _key(1003))[0] == INTERFACE_OBSERVATION_EXACT_REPLAY
    assert io.current_observation_chains(store.load_interface_observations(pid)) == []
    store.close()


@pytest.mark.parametrize("rival", ["correction", "withdrawal"])
def test_s4_a_concurrent_correction_or_second_withdrawal_of_the_same_head_loses(tmp_path, rival):
    path = str(tmp_path / "s4.db")
    store = SqliteRecordStore(path)
    pid, [item] = _store_project(store)
    iid = item.interface_id
    head = store.append_interface_observation(pid, _root(iid), "r1")[1].observation_id
    store.close()
    events = [io.recorded_withdrawal(iid, head),
              io.recorded_correction(iid, OBS2, head) if rival == "correction"
              else io.recorded_withdrawal(iid, head)]
    barrier = threading.Barrier(2)
    outcomes = [None, None]

    def run(i):
        s = SqliteRecordStore(path)
        try:
            barrier.wait()
            s.append_interface_observation(pid, events[i], _key(500 + i))
            outcomes[i] = "ok"
        except Exception as exc:                                    # noqa: BLE001
            outcomes[i] = type(exc).__name__
        finally:
            s.close()
    threads = [threading.Thread(target=run, args=(i,)) for i in (0, 1)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(30)
    assert sorted(outcomes) == sorted(["ok", "InterfaceObservationRejected"]), outcomes
    check = SqliteRecordStore(path)
    loaded = check.load_interface_observations(pid)
    assert len(loaded) == 2 and loaded[1].supersedes_observation_id == head
    check.close()


def test_s5_the_database_enforces_the_closed_kind_and_the_withdrawal_shape(tmp_path):
    path = str(tmp_path / "s5.db")
    store = SqliteRecordStore(path)
    pid, [item] = _store_project(store)
    root = store.append_interface_observation(pid, _root(item.interface_id), "r1")[1]
    store.close()
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    cols = ("project_id, observation_event_seq, observation_id, interface_id, "
            "observation_text, supersedes_observation_id, submission_key, recorded_at, "
            "event_kind")
    try:
        for text, target, kind in (("not the marker", root.observation_id, "WITHDRAWAL"),
                                   (MARKER, None, "WITHDRAWAL"),
                                   ("x", None, "BOGUS"),
                                   ("x", None, None)):
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute("INSERT INTO %s (%s) VALUES (?, 1, ?, ?, ?, ?, 'raw', 't', ?)"
                             % (TABLE, cols),
                             (pid, io.new_observation_id(), item.interface_id, text, target,
                              kind))
    finally:
        conn.close()


# ==========================================================================
# M. the migration: fresh, populated legacy, idempotent, partial, interrupted
# ==========================================================================
def _legacy_db(tmp_path, name="legacy.db", rows=2):
    """A database whose observation table is EXACTLY the legacy shape, holding
    ``rows`` legacy events written in the legacy column layout."""
    path = str(tmp_path / name)
    store = SqliteRecordStore(path)
    pid, [item] = _store_project(store)
    store.close()
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("DROP TABLE %s" % TABLE)
    for stmt in rs._INTERFACE_OBSERVATIONS_SCHEMA:
        conn.execute(stmt)
    first = io.new_observation_id()
    legacy = [(pid, 0, first, item.interface_id, "legacy check", None, "lk0",
               "2026-10-01T00:00:00+00:00", COND, None, None)]
    if rows > 1:
        legacy.append((pid, 1, io.new_observation_id(), item.interface_id, "legacy fix",
                       first, "lk1", "2026-10-01T00:01:00+00:00", None, None, None))
    conn.executemany("INSERT INTO %s VALUES (%s)" % (TABLE, ",".join("?" * 11)), legacy)
    conn.commit()
    conn.close()
    return path, pid, item, legacy


def _shape(path):
    conn = sqlite3.connect(path)
    try:
        return rs._observation_schema_shape(conn)
    finally:
        conn.close()


def _all_rows(path):
    conn = sqlite3.connect(path)
    try:
        return conn.execute("SELECT * FROM %s ORDER BY project_id, 2" % TABLE).fetchall()
    finally:
        conn.close()


def test_m1_fresh_and_migrated_databases_are_identical_and_reopening_is_idempotent(tmp_path):
    legacy_ref, current_ref = rs._observation_reference_shapes()
    assert legacy_ref != current_ref
    fresh = str(tmp_path / "fresh.db")
    SqliteRecordStore(fresh).close()
    path, _pid, _item, _rows_ = _legacy_db(tmp_path)
    assert _shape(path) == legacy_ref
    SqliteRecordStore(path).close()
    assert _shape(fresh) == _shape(path) == current_ref
    before = _all_rows(path)
    SqliteRecordStore(path).close()                                # idempotent reopen
    assert _shape(path) == current_ref and _all_rows(path) == before
    conn = sqlite3.connect(path)
    try:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(%s)" % TABLE)]
    finally:
        conn.close()
    assert "observation_seq" not in cols and cols[1] == "observation_event_seq"
    assert cols[-1] == "event_kind"


def test_m2_a_populated_legacy_table_is_upgraded_preserving_every_value(tmp_path):
    path, pid, item, legacy = _legacy_db(tmp_path)
    store = SqliteRecordStore(path)
    rows = _all_rows(path)
    assert [r[:11] for r in rows] == legacy                        # every value kept
    assert [r[11] for r in rows] == ["OBSERVATION", "OBSERVATION"]
    events = store.load_interface_observations(pid)
    assert [e.observation_text for e in events] == ["legacy check", "legacy fix"]
    assert events[0].context.operating_conditions == COND
    assert events[1].supersedes_observation_id == legacy[0][2]
    conn = sqlite3.connect(path)
    try:
        assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
        assert conn.execute("PRAGMA integrity_check").fetchone() == ("ok",)
    finally:
        conn.close()
    w = store.append_interface_observation(
        pid, io.recorded_withdrawal(item.interface_id, events[1].observation_id), "w1")[1]
    assert store.load_interface_observations(pid)[-1] == w
    store.close()


@pytest.mark.parametrize("damage", [
    "ALTER TABLE {t} ADD COLUMN event_kind TEXT NOT NULL DEFAULT 'OBSERVATION'",
    "ALTER TABLE {t} RENAME COLUMN observation_seq TO observation_event_seq",
    "DROP INDEX subsystem_interface_observations_successor_uq",
    "CREATE TRIGGER obs_extra AFTER INSERT ON {t} BEGIN SELECT 1; END",
    "ALTER TABLE {t} ADD COLUMN note TEXT",
])
def test_m3_a_partial_or_unknown_shape_is_refused_and_left_untouched(tmp_path, damage):
    path, _pid, _item, legacy = _legacy_db(tmp_path)
    conn = sqlite3.connect(path)
    conn.execute(damage.format(t=TABLE))
    conn.commit()
    conn.close()
    shape = _shape(path)
    with pytest.raises(sqlite3.DatabaseError, match="unrecognised shape"):
        SqliteRecordStore(path)
    assert _shape(path) == shape
    assert [r[:11] for r in _all_rows(path)] == legacy


def test_m4_a_check_fragment_alone_is_not_accepted_as_the_legacy_shape(tmp_path):
    path, _pid, _item, legacy = _legacy_db(tmp_path)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA writable_schema = ON")                    # fixture only
    conn.execute("UPDATE sqlite_master SET sql = replace(sql, 'BETWEEN 1 AND 1000', "
                 "'BETWEEN 1 AND 999') WHERE name = ?", (TABLE,))
    conn.commit()
    conn.close()
    with pytest.raises(sqlite3.DatabaseError, match="unrecognised shape"):
        SqliteRecordStore(path)
    assert [r[:11] for r in _all_rows(path)] == legacy


def test_m5_an_interrupted_upgrade_rolls_back_completely(tmp_path, monkeypatch):
    rs._observation_reference_shapes()                             # cached before the fault
    path, _pid, _item, legacy = _legacy_db(tmp_path)
    shape = _shape(path)
    monkeypatch.setattr(rs, "_OBSERVATION_UPGRADE", (
        rs._OBSERVATION_UPGRADE[0], "ALTER TABLE no_such_table RENAME COLUMN a TO b"))
    with pytest.raises(sqlite3.OperationalError):
        SqliteRecordStore(path)
    assert _shape(path) == shape                                   # neither change remains
    assert _all_rows(path) == legacy
    monkeypatch.undo()
    SqliteRecordStore(path).close()                                # a later open upgrades
    assert _shape(path) == rs._observation_reference_shapes()[1]


def test_m6_a_linked_sqlite_without_rename_support_refuses_the_upgrade(tmp_path, monkeypatch):
    rs._observation_reference_shapes()
    path, _pid, _item, legacy = _legacy_db(tmp_path)
    monkeypatch.setattr(rs.sqlite3, "sqlite_version_info", (3, 24, 0))
    with pytest.raises(sqlite3.DatabaseError, match="linked SQLite"):
        SqliteRecordStore(path)
    monkeypatch.undo()
    assert [r[:11] for r in _all_rows(path)] == legacy


# ==========================================================================
# R. the route: confirmation, signed binding, retry, staleness, ambiguity
# ==========================================================================
def test_r1_withdrawing_keeps_labelled_history_drops_the_current_count_and_controls(client):
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    root = _check(client, sid, iid)
    _observe(client, sid, _correct_form(client, sid, root.observation_id), OBS2)
    other = _check(client, sid, iid, "A separate retest.")
    fix = _events(sid)[1]
    assert _status_count(None).format(count=2) in _page(client, sid)
    r = _withdraw(client, sid, _withdraw_form(client, sid, fix.observation_id))
    assert r.status_code == 200 and appmod.S15_OBS_WITHDRAW_SAVED_MESSAGE in _body(r)
    events = _events(sid)
    assert len(events) == 4 and io.is_withdrawal(events[3])
    page = _page(client, sid)
    assert OBS in page and OBS2 in page                            # last, earlier text kept
    assert ui_text.text("UI_S15_OBS_WITHDRAWN", "en") in page
    assert page.count("data-obs-chain-withdrawn") == 1
    assert _status_count(None).format(count=1) in page             # CURRENT checks only
    assert MARKER not in page and events[3].observation_id not in page
    raw = _page_raw(client, sid)
    targets = {f.get("supersedes") for f in _forms(raw) + _withdraw_forms(raw)}
    assert root.observation_id not in targets and fix.observation_id not in targets
    assert other.observation_id in targets


def test_r2_confirmation_is_required(client):
    sid, ifc = _integrated_with_interface(client)
    root = _check(client, sid, ifc.interface_id)
    form = _withdraw_form(client, sid, root.observation_id)
    for extra in ({}, {"withdraw_confirm": "no"}):
        r = client.post(WITHDRAW % sid, data=dict(form, **extra))
        assert r.status_code == 400 and appmod.S15_OBS_WITHDRAW_CONFIRM_MESSAGE in _body(r)
    assert _events(sid) == (root,)


def test_r3_the_signature_binds_project_interface_head_and_action(client):
    sid, first, second = _two_interfaces(client)
    a = _check(client, sid, first.interface_id)
    b = _check(client, sid, first.interface_id, OBS2)
    c2 = _check(client, sid, second.interface_id)
    form = _withdraw_form(client, sid, a.observation_id)
    record = _record_form(client, sid, first.interface_id)
    other, theirs_ifc = _integrated_with_interface(client)
    theirs_root = _check(client, other, theirs_ifc.interface_id)
    theirs = _withdraw_form(client, other, theirs_root.observation_id)
    for data in (dict(form, supersedes=b.observation_id),
                 dict(form, interface_id=second.interface_id, supersedes=c2.observation_id),
                 dict(form, observation_withdrawal_submission=""),
                 dict(form, observation_withdrawal_submission=record["observation_submission"]),
                 dict(form, observation_withdrawal_submission=theirs[
                     "observation_withdrawal_submission"])):
        r = _withdraw(client, sid, data)
        assert r.status_code == 400 and appmod.S15_OBS_WITHDRAW_NOT_SAVED_MESSAGE in _body(r)
    assert _withdraw(client, sid, theirs).status_code == 400       # foreign form, this project
    assert len(_events(sid)) == 3 and _events(other) == (theirs_root,)


def test_r4_an_exact_retry_writes_nothing_also_after_a_restart(client):
    sid, ifc = _integrated_with_interface(client)
    root = _check(client, sid, ifc.interface_id)
    form = _withdraw_form(client, sid, root.observation_id)
    assert _withdraw(client, sid, form).status_code == 200
    _restart()
    r = _withdraw(client, sid, form)
    assert r.status_code == 200 and appmod.S15_OBS_WITHDRAW_SAVED_MESSAGE in _body(r)
    assert len(_rows(sid)) == 2


def test_r5_stale_forms_never_extend_or_rewithdraw_a_changed_chain(client):
    sid, ifc = _integrated_with_interface(client)
    root = _check(client, sid, ifc.interface_id)
    early = _withdraw_form(client, sid, root.observation_id)
    twin = _withdraw_form(client, sid, root.observation_id)
    fix_form = _correct_form(client, sid, root.observation_id)
    _observe(client, sid, fix_form, OBS2)
    r = _withdraw(client, sid, early)
    assert r.status_code == 400 and appmod.S15_OBS_WITHDRAW_STALE_MESSAGE in _body(r)
    fix = _events(sid)[1]
    late_fix = _correct_form(client, sid, fix.observation_id)
    assert _withdraw(client, sid, _withdraw_form(client, sid, fix.observation_id)).status_code == 200
    assert _withdraw(client, sid, twin).status_code == 400
    r = _observe(client, sid, late_fix, "A correction after the withdrawal.")
    assert r.status_code == 400 and appmod.S15_OBS_STALE_MESSAGE in _body(r)
    assert len(_events(sid)) == 3 and io.is_withdrawal(_events(sid)[2])


def test_r6_a_cross_action_replay_under_the_withdrawal_key_is_never_confirmed(client):
    sid, ifc = _integrated_with_interface(client)
    root = _check(client, sid, ifc.interface_id)
    form = _withdraw_form(client, sid, root.observation_id)
    key = appmod._s15_obs_withdrawal_key(sid, form["observation_withdrawal_submission"][:32])
    _store().append_interface_observation(
        sid, io.recorded_correction(ifc.interface_id, MARKER, root.observation_id), key)
    r = _withdraw(client, sid, form)
    assert r.status_code == 400
    assert appmod.S15_OBS_WITHDRAW_NOT_SAVED_MESSAGE in _body(r)
    assert not any(io.is_withdrawal(e) for e in _events(sid))
    page = _page(client, sid)
    assert MARKER in page                                         # it is ordinary text here


def test_r7_commit_ambiguity_resolves_from_committed_truth_or_stays_unknown(client):
    sid, ifc = _integrated_with_interface(client)
    a = _check(client, sid, ifc.interface_id)
    b = _check(client, sid, ifc.interface_id, OBS2)
    store = _store()
    real = store._conn
    store._conn = _CommitThenRaise(real)
    try:
        r = _withdraw(client, sid, _withdraw_form(client, sid, a.observation_id))
    finally:
        store._conn = real
    assert r.status_code == 200 and appmod.S15_OBS_WITHDRAW_SAVED_MESSAGE in _body(r)
    form = _withdraw_form(client, sid, b.observation_id)
    store._conn = _CommitAndRollbackFail(real)
    try:
        r = _withdraw(client, sid, form)
    finally:
        store._conn = real
    try:
        assert r.status_code == 503 and appmod.S15_OBS_WITHDRAW_UNKNOWN_MESSAGE in _body(r)
        with pytest.raises(RecordStoreConnectionUnsafe):
            store.load_interface_observations(sid)
        retry = _withdraw(client, sid, form)
        assert retry.status_code == 503
    finally:
        real.close()
        appmod._STORE = None
    assert len(_events(sid)) == 3
    assert _withdraw(client, sid, form).status_code == 200
    assert len(_events(sid)) == 4


def test_r8_only_the_project_owner_can_withdraw():
    appmod.app.config["TESTING"] = True
    owner, _a = _client_for("obs-withdraw-owner@example.com")
    stranger, _b = _client_for("obs-withdraw-stranger@example.com")
    sid, ifc = _integrated_with_interface(owner)
    root = _check(owner, sid, ifc.interface_id)
    form = _withdraw_form(owner, sid, root.observation_id)
    form.pop("csrf_token")
    r = _withdraw(stranger, sid, form)
    assert r.status_code == 302
    assert _events(sid) == (root,)


def test_r9_unreadable_history_reads_unavailable_never_zero(client):
    sid, ifc = _integrated_with_interface(client)
    root = _check(client, sid, ifc.interface_id)
    _withdraw(client, sid, _withdraw_form(client, sid, root.observation_id))
    _raw("UPDATE %s SET observation_text = 'not the marker' WHERE event_kind = 'WITHDRAWAL'"
         % TABLE, ignore_checks=True)
    with pytest.raises(InterfaceObservationsCorrupt):
        _events(sid)
    page = _page(client, sid)
    assert ui_text.text("UI_S15_OBS_UNAVAILABLE", "en") in page
    [checks] = re.findall(r"<dd data-status-checks>(.*?)</dd>", page, re.S)
    assert ui_text.text("UI_S15_ST_UNAVAILABLE", "en") in checks
    assert _status_count(None).format(count=0) not in checks
    assert not _withdraw_forms(_page_raw(client, sid))


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_r10_the_withdrawal_journey_is_localized(client, lang):
    sid, ifc = _integrated_with_interface(client)
    root = _check(client, sid, ifc.interface_id)
    client.post("/ui-language", data={"lang": lang})
    page = _page(client, sid)
    for key in ("UI_S15_OBS_WITHDRAW", "UI_S15_OBS_WITHDRAW_NOTE",
                "UI_S15_OBS_WITHDRAW_CONFIRM", "UI_S15_OBS_WITHDRAW_BUTTON"):
        assert ui_text.text(key, lang) in page, key
    r = _withdraw(client, sid, _withdraw_form(client, sid, root.observation_id))
    assert ui_text.text("UI_S15_OBS_MSG_WITHDRAW_SAVED", lang) in _body(r)
    page = _page(client, sid)
    assert ui_text.text("UI_S15_OBS_WITHDRAWN", lang) in page
    assert ui_text.text("UI_S15_ST_CHECKS_COUNT", lang).format(count=0) in page
    for key in ("UI_S15_OBS_WITHDRAW", "UI_S15_OBS_WITHDRAW_NOTE", "UI_S15_OBS_WITHDRAW_CONFIRM",
                "UI_S15_OBS_WITHDRAW_BUTTON", "UI_S15_OBS_WITHDRAWN",
                "UI_S15_OBS_MSG_WITHDRAW_SAVED", "UI_S15_OBS_MSG_WITHDRAW_NOT_SAVED",
                "UI_S15_OBS_MSG_WITHDRAW_CONFIRM", "UI_S15_OBS_MSG_WITHDRAW_STALE",
                "UI_S15_OBS_MSG_WITHDRAW_UNKNOWN"):
        assert ui_text.text(key, "en") and ui_text.text(key, "ar") != ui_text.text(key, "en")


# ==========================================================================
# B. boundaries: report / PDF / export / readiness / evidence unchanged
# ==========================================================================
def test_b1_withdrawal_changes_no_report_pdf_export_readiness_or_evidence(client, monkeypatch):
    from engine import read_export_service as rx
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    _save(client, sid, {(F_C, iid): COND, (F_A, iid): ACCEPT, (F_E, iid): EVID})
    root = _check(client, sid, iid)

    def stable(source):
        source = re.sub(r'name="csrf_token" value="[^"]*"', "", source)
        return re.sub(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|\+00:00)", "T", source)

    def snapshot():
        store = _store()
        st = appmod.SESSION_STORE[sid]["state"]
        return (stable(client.get("/session/%s/deliverable" % sid).get_data(as_text=True)),
                rx._compose_export(store.load_contract(sid), rx._domain_support_state(store, sid)),
                _progression_snapshot(sid), _prep_rows(sid),
                store.load_evidence_references(sid), store.load_readiness_evidence(sid),
                readiness_snapshot(st, ())["rows"])
    before = snapshot()
    pdf_before = stable(_pdf_source(client, sid, monkeypatch))
    _withdraw(client, sid, _withdraw_form(client, sid, root.observation_id))
    assert snapshot() == before
    assert stable(_pdf_source(client, sid, monkeypatch)) == pdf_before
    for path in (os.path.join("web", "templates", "deliverable.html"),
                 os.path.join("engine", "disclosure_export.py"),
                 os.path.join("engine", "readiness_snapshot.py"),
                 os.path.join("engine", "commercial_evidence.py")):
        source = open(path, encoding="utf-8").read()
        assert "interface_observation" not in source and "observation_chains" not in source, path
