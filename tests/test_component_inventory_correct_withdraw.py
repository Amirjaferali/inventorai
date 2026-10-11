"""COMPONENT-INVENTORY-CORRECT-WITHDRAW-01 — correcting and withdrawing a declared component.

The inventor may CORRECT a current component (name, function and part links, replaced as a whole) or
WITHDRAW it (terminal). What is pinned:
  * semantics (``engine/subsystem_model.py``): append-only revisions over the immutable declaration;
    ONE contiguous linear history per component; nothing after a withdrawal; 20 corrections plus ONE
    separately reserved withdrawal; the ONE current projection (latest material, declaration order,
    withdrawn excluded) and the withdrawn remainder as history; OWNER_STATED / UNVALIDATED throughout;
  * persistence (``engine/record_store.py``): the forward-only migration of a first-shape
    ``project_components`` table (every row, identity, order value and submission key copied exactly;
    ``component_seq`` -> ``declaration_seq``; lifetime bound 500) and the additive
    ``project_component_revisions`` table; a revision-unaware reader / writer fails closed on the
    migrated database; whole-history validation with no fallback; stale / terminal / capacity / retry /
    conflict / isolation decided inside ONE write transaction; 50 active / 500 lifetime;
  * web (``web/app.py``): two POST routes behind the central project authorization, the CSRF guard and
    signed action-specific submission identities; SAVED only from committed durable state;
  * the three consumers present the SAME current projection: session page (with earlier versions and a
    separate withdrawn-history list), Parts / Components / Interactions view, Stage 35 export v2 field 7
    (current components only, original surviving order, no id, no revision history; v2 unchanged);
  * no IdeaState, replay, report, PDF, readiness, evidence, SafetySignal or calculation effect.
"""
import html as _html
import json
import os
import pickle
import re
import sqlite3
import threading

import pytest

import web.app as appmod
from engine import subsystem_model as sm
from engine.idea_state import OWNER_STATED, UNVALIDATED
from engine.record_store import (
    PROJECT_COMPONENT_EXACT_REPLAY, PROJECT_COMPONENT_INSERTED, ProjectComponentAlreadyWithdrawn,
    ProjectComponentConflict, ProjectComponentLimitReached, ProjectComponentRejected,
    ProjectComponentStale, ProjectComponentsCorrupt, ProjectComponentUnchanged,
    RecordStoreConnectionUnsafe, SqliteRecordStore)
from tests.csrf_client import csrf_client
from tests.test_component_inventory_declare_list import (
    _block, _declare, _form, _integrated, _notice, _ordinary, _page, _rows, _stable)
from tests.test_stage15_integrated_invention_entry import (
    MECH, TIE_IDEA, _compose, _contract, _created, _pair, _ri, _visible)
from web import ui_text

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SECRET = "Zq-corrected-component-4410"
F7 = "component_descriptions_beyond_parts"

# The base commit's (07989d2) reader and writer statements, verbatim: a revision-unaware build.
_OLD_COLUMNS = ("component_seq, component_id, display_name, function_text, "
                "subsystem_ids, provenance, validation_state, submission_key")
_OLD_SELECT = ("SELECT " + _OLD_COLUMNS + " FROM project_components "
               "WHERE project_id = ? ORDER BY component_seq ASC")
_OLD_INSERT = ("INSERT INTO project_components (project_id, " + _OLD_COLUMNS
               + ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)")
_OLD_DDL = """
    CREATE TABLE IF NOT EXISTS project_components (
        project_id        TEXT    NOT NULL,
        component_seq     INTEGER NOT NULL,
        component_id      TEXT    NOT NULL,
        display_name      TEXT    NOT NULL,
        function_text     TEXT    NOT NULL,
        subsystem_ids     TEXT    NOT NULL,
        provenance        TEXT    NOT NULL,
        validation_state  TEXT    NOT NULL,
        submission_key    TEXT    NOT NULL,
        PRIMARY KEY (project_id, component_id),
        UNIQUE (project_id, component_seq),
        UNIQUE (project_id, submission_key),
        FOREIGN KEY (project_id) REFERENCES projects(project_id),
        CHECK (component_seq >= 0 AND component_seq < 50),
        CHECK (provenance = 'OWNER_STATED'),
        CHECK (validation_state = 'UNVALIDATED'),
        CHECK (typeof(component_id) = 'text' AND length(component_id) = 36),
        CHECK (typeof(display_name) = 'text'
               AND length(display_name) BETWEEN 1 AND 80
               AND instr(CAST(display_name AS BLOB), X'00') = 0),
        CHECK (typeof(function_text) = 'text'
               AND length(function_text) BETWEEN 1 AND 300
               AND instr(CAST(function_text AS BLOB), X'00') = 0),
        CHECK (typeof(subsystem_ids) = 'text' AND length(subsystem_ids) <= 512),
        CHECK (typeof(submission_key) = 'text' AND length(submission_key) > 0)
    )"""
_OLD_INDEX = ("CREATE UNIQUE INDEX IF NOT EXISTS project_components_id_uq "
              "ON project_components (component_id)")


# ==========================================================================
# harness
# ==========================================================================
@pytest.fixture
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


def _store():
    return appmod._get_store()


def _raw(sql, params=(), fk=True):
    _store()
    conn = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        conn.execute("PRAGMA foreign_keys = %s" % ("ON" if fk else "OFF"))
        rows = conn.execute(sql, params).fetchall()
        conn.commit()
        return rows
    finally:
        conn.close()


def _revs(pid):
    return _raw("SELECT component_id, revision_no, kind, display_name FROM "
                "project_component_revisions WHERE project_id = ? "
                "ORDER BY component_id, revision_no", (pid,))


def _new_project(store, integrated=True):
    subs = _pair() if integrated else ()
    pid = store.create_project(_contract(), reconstruction_inputs=_ri(MECH),
                               subsystems=subs or None)
    return pid, tuple(subs)


def _declare_store(store, pid, subs, name, function="Does a thing", parts=(), key=None):
    item = sm.declared_component(subs, name, function, parts)
    store.append_project_component(pid, item, key or ("k-" + name))
    return item


def _inventory(store, pid):
    return store.load_component_inventory_record(pid)


def _correct(store, pid, component_id, expected, name, function="Does a thing", parts=(),
             key=None):
    subs, inv = _inventory(store, pid)
    rev = sm.corrected_component_revision(inv, subs, component_id, expected, name, function, parts)
    return store.append_component_revision(pid, rev, key or ("c-%s-%d" % (component_id, expected)))


def _withdraw(store, pid, component_id, expected, key=None):
    _subs, inv = _inventory(store, pid)
    rev = sm.withdrawn_component_revision(inv, component_id, expected)
    return store.append_component_revision(pid, rev, key or ("w-" + component_id))


def _legacy_db(path, rows_per_project=3):
    """A database holding the FIRST-shape ``project_components`` table with real rows, exactly as the
    base commit wrote it (the current store creates the project; the table is then swapped back)."""
    store = SqliteRecordStore(path)
    subs = _pair()
    pid = store.create_project(_contract(), reconstruction_inputs=_ri(MECH), subsystems=subs)
    other = store.create_project(_contract(), reconstruction_inputs=_ri(MECH))
    store.close()
    conn = sqlite3.connect(path)
    conn.execute("DROP TABLE project_component_revisions")
    conn.execute("DROP TABLE project_components")
    conn.execute(_OLD_DDL)
    conn.execute(_OLD_INDEX)
    for project, parts in ((pid, subs), (other, ())):
        for i in range(rows_per_project):
            item = sm.declared_component(parts, "Part %d" % i, "Does %d" % i,
                                         (parts[0].subsystem_id,) if parts and i == 1 else ())
            conn.execute(_OLD_INSERT, (project, i, item.component_id, item.display_name,
                                       item.function_text,
                                       json.dumps(list(item.subsystem_ids), separators=(",", ":")),
                                       OWNER_STATED, UNVALIDATED, "key-%s-%d" % (project, i)))
    conn.commit()
    before = conn.execute("SELECT * FROM project_components ORDER BY project_id, component_seq").fetchall()
    conn.close()
    return pid, other, subs, before


# ==========================================================================
# 1. Semantic owner
# ==========================================================================
def test_m01_a_declaration_only_inventory_is_its_own_current_projection():
    subs = _pair()
    a = sm.declared_component(subs, "A", "a", (subs[0].subsystem_id,))
    b = sm.declared_component(subs, "B", "b", ())
    inv = sm.project_component_inventory((a, b), (), subs)
    assert inv.active == (a, b) and inv.withdrawn == () and inv.declared_count == 2
    assert [r.head_revision_no for r in inv.records] == [0, 0]
    assert [r.versions[0].revision_no for r in inv.records] == [0, 0]


def test_m02_a_correction_continues_the_head_and_refuses_stale_unchanged_unknown_and_foreign():
    subs = _pair()
    a = sm.declared_component(subs, "A", "a", ())
    inv = sm.project_component_inventory((a,), (), subs)
    rev = sm.corrected_component_revision(inv, subs, a.component_id, 0, "A2", "a2",
                                          (subs[1].subsystem_id, subs[0].subsystem_id))
    assert (rev.revision_no, rev.kind, rev.provenance, rev.validation_state) == (
        1, sm.COMPONENT_REVISION_CORRECTED, OWNER_STATED, UNVALIDATED)
    assert rev.subsystem_ids == (subs[0].subsystem_id, subs[1].subsystem_id)   # canonical order
    assert sm.is_valid_component_revision_id(rev.revision_id)
    inv2 = sm.project_component_inventory((a,), (rev,), subs)
    assert inv2.active[0].display_name == "A2" and inv2.active[0].component_id == a.component_id
    assert [v.display_name for v in inv2.records[0].versions] == ["A", "A2"]
    with pytest.raises(sm.ComponentStale):
        sm.corrected_component_revision(inv2, subs, a.component_id, 0, "A3", "a3", ())
    with pytest.raises(sm.ComponentUnchanged):
        sm.corrected_component_revision(inv2, subs, a.component_id, 1, "A2", "a2",
                                        (subs[0].subsystem_id, subs[1].subsystem_id))
    with pytest.raises(sm.ComponentUnknown):
        sm.corrected_component_revision(inv2, subs, "cmp-" + "0" * 32, 0, "X", "x", ())
    with pytest.raises(sm.ComponentError):
        sm.corrected_component_revision(inv2, subs, a.component_id, 1, "A3", "a3",
                                        ("sub-" + "0" * 32,))
    for bad in ("", " padded", "n" * 81):
        with pytest.raises(sm.ComponentError):
            sm.corrected_component_revision(inv2, subs, a.component_id, 1, bad, "a3", ())


def test_m03_withdrawal_is_terminal_and_reserved_after_twenty_corrections():
    subs = _pair()
    a = sm.declared_component(subs, "A", "a", ())
    revs = []
    for n in range(sm.MAX_CORRECTIONS_PER_COMPONENT):
        inv = sm.project_component_inventory((a,), tuple(revs), subs)
        revs.append(sm.corrected_component_revision(inv, subs, a.component_id, n, "A%d" % n, "a", ()))
    inv = sm.project_component_inventory((a,), tuple(revs), subs)
    assert inv.records[0].corrections == 20
    with pytest.raises(sm.ComponentCorrectionLimit):
        sm.corrected_component_revision(inv, subs, a.component_id, 20, "A-more", "a", ())
    w = sm.withdrawn_component_revision(inv, a.component_id, 20)
    assert w.revision_no == 21 and w.display_name is None and w.subsystem_ids is None
    done = sm.project_component_inventory((a,), tuple(revs) + (w,), subs)
    assert done.active == () and [r.component_id for r in done.withdrawn] == [a.component_id]
    assert done.withdrawn[0].current.display_name == "A19"      # last recorded material kept
    with pytest.raises(sm.ComponentAlreadyWithdrawn):
        sm.withdrawn_component_revision(done, a.component_id, 21)
    with pytest.raises(sm.ComponentAlreadyWithdrawn):
        sm.corrected_component_revision(done, subs, a.component_id, 21, "Z", "z", ())


def _rev(component_id, n, kind=sm.COMPONENT_REVISION_CORRECTED, name="N", function="F", parts=(),
         rid=None):
    corrected = kind == sm.COMPONENT_REVISION_CORRECTED
    return sm.ComponentRevision(
        revision_id=rid or sm.new_component_revision_id(), component_id=component_id,
        revision_no=n, kind=kind, display_name=name if corrected else None,
        function_text=function if corrected else None,
        subsystem_ids=tuple(parts) if corrected else None,
        provenance=OWNER_STATED, validation_state=UNVALIDATED)


def test_m04_the_projection_rejects_every_malformed_history_whole():
    subs = _pair()
    a = sm.declared_component(subs, "A", "a", ())
    cid = a.component_id
    W = sm.COMPONENT_REVISION_WITHDRAWN
    dup = sm.new_component_revision_id()
    bad = {
        "gap": (_rev(cid, 2),),
        "fork": (_rev(cid, 1), _rev(cid, 1, name="other")),
        "after withdrawal": (_rev(cid, 1, kind=W), _rev(cid, 2)),
        "unknown component": (_rev("cmp-" + "1" * 32, 1),),
        "duplicate revision id": (_rev(cid, 1, rid=dup), _rev(cid, 2, rid=dup)),
        "position out of range": (_rev(cid, 22, kind=W),),
        "correction beyond twenty": (_rev(cid, 21),),
        "withdrawal with material": (sm.ComponentRevision(
            sm.new_component_revision_id(), cid, 1, W, "N", None, None, OWNER_STATED, UNVALIDATED),),
        "correction without material": (sm.ComponentRevision(
            sm.new_component_revision_id(), cid, 1, sm.COMPONENT_REVISION_CORRECTED, None, None,
            None, OWNER_STATED, UNVALIDATED),),
        "foreign part": (_rev(cid, 1, parts=("sub-" + "0" * 32,)),),
        "unknown kind": (sm.ComponentRevision(
            sm.new_component_revision_id(), cid, 1, "DELETED", None, None, None, OWNER_STATED,
            UNVALIDATED),),
        "validated": (sm.ComponentRevision(
            sm.new_component_revision_id(), cid, 1, W, None, None, None, OWNER_STATED, "VALIDATED"),),
        "malformed id": (_rev(cid, 1, rid="crv-" + "Z" * 32),),
    }
    for label, history in bad.items():
        with pytest.raises(sm.ComponentError):
            sm.project_component_inventory((a,), history, subs)
        assert label
    many = tuple(sm.declared_component(subs, "C%d" % i, "c", ())
                 for i in range(sm.MAX_PROJECT_COMPONENTS_PER_PROJECT + 1))
    with pytest.raises(sm.ComponentError):
        sm.project_component_inventory(many, (), subs)          # > 50 ACTIVE
    withdrawn_one = (sm.ComponentRevision(sm.new_component_revision_id(), many[0].component_id, 1,
                                          W, None, None, None, OWNER_STATED, UNVALIDATED),)
    assert len(sm.project_component_inventory(many, withdrawn_one, subs).active) == 50


def test_m05_revision_material_identity():
    subs = _pair()
    a = sm.declared_component(subs, "A", "a", ())
    inv = sm.project_component_inventory((a,), (), subs)
    one = sm.corrected_component_revision(inv, subs, a.component_id, 0, "B", "b",
                                          (subs[0].subsystem_id,))
    again = sm.corrected_component_revision(inv, subs, a.component_id, 0, "B", "b",
                                            (subs[0].subsystem_id,))
    assert one.revision_id != again.revision_id and sm.same_revision_material(one, again)
    other = sm.corrected_component_revision(inv, subs, a.component_id, 0, "B", "c", ())
    assert not sm.same_revision_material(one, other)
    w = sm.withdrawn_component_revision(inv, a.component_id, 0)
    assert not sm.same_revision_material(one, w)
    assert sm.same_revision_material(w, sm.withdrawn_component_revision(inv, a.component_id, 0))


# ==========================================================================
# 2. Persistence: migration and rollback safety
# ==========================================================================
def test_s01_a_first_shape_table_is_rebuilt_once_with_every_row_exact(tmp_path):
    path = str(tmp_path / "legacy.db")
    pid, other, subs, before = _legacy_db(path)
    store = SqliteRecordStore(path)
    cols = [r[1] for r in store._conn.execute("PRAGMA table_info(project_components)")]
    assert cols == ["project_id", "declaration_seq", "component_id", "display_name",
                    "function_text", "subsystem_ids", "provenance", "validation_state",
                    "submission_key"]
    after = store._conn.execute(
        "SELECT * FROM project_components ORDER BY project_id, declaration_seq").fetchall()
    assert after == before                                  # identities, order, keys: exact
    indexes = {r[1] for r in store._conn.execute("PRAGMA index_list(project_components)")}
    assert "project_components_id_uq" in indexes
    sql = store._conn.execute("SELECT sql FROM sqlite_master WHERE name = 'project_components'"
                              ).fetchone()[0]
    assert "declaration_seq < 500" in sql and "component_seq" not in sql
    assert store._conn.execute("SELECT name FROM sqlite_master WHERE name = "
                               "'project_components_rebuild_v2'").fetchone() is None
    _subs, comps = store.load_component_inventory(pid)
    assert [c.display_name for c in comps] == ["Part 0", "Part 1", "Part 2"]
    assert comps[1].subsystem_ids == (subs[0].subsystem_id,)
    # every unaffected constraint survives: the per-project unique submission key and the CHECKs
    with pytest.raises(sqlite3.IntegrityError):
        store._conn.execute("INSERT INTO project_components VALUES (?,?,?,?,?,?,?,?,?)",
                            (pid, 3, "cmp-" + "e" * 32, "X", "x", "[]", OWNER_STATED,
                             "VALIDATED", "new"))
    store.close()
    again = SqliteRecordStore(path)                         # idempotent reopen
    assert again._conn.execute(
        "SELECT * FROM project_components ORDER BY project_id, declaration_seq").fetchall() == before
    item = sm.declared_component(subs, "Next", "n", ())
    assert again.append_project_component(pid, item, "next")[0] == PROJECT_COMPONENT_INSERTED
    seqs = again._conn.execute("SELECT declaration_seq FROM project_components WHERE project_id = ?"
                               " ORDER BY declaration_seq", (pid,)).fetchall()
    assert [s[0] for s in seqs] == [0, 1, 2, 3]             # continues; never recycled
    again.close()


def test_s02_an_unrecognised_shape_or_a_leftover_rebuild_refuses_instead_of_guessing(tmp_path):
    path = str(tmp_path / "odd.db")
    _legacy_db(path)
    conn = sqlite3.connect(path)
    conn.execute("ALTER TABLE project_components ADD COLUMN extra TEXT")
    conn.commit()
    conn.close()
    with pytest.raises(sqlite3.DatabaseError):
        SqliteRecordStore(path)
    path2 = str(tmp_path / "leftover.db")
    _legacy_db(path2)
    conn = sqlite3.connect(path2)
    conn.execute("CREATE TABLE project_components_rebuild_v2 (x)")
    conn.commit()
    conn.close()
    with pytest.raises(sqlite3.DatabaseError):
        SqliteRecordStore(path2)
    conn = sqlite3.connect(path2)                           # the refusal changed nothing
    cols = [r[1] for r in conn.execute("PRAGMA table_info(project_components)")]
    conn.close()
    assert "component_seq" in cols


def test_s03_a_revision_unaware_build_fails_closed_on_the_migrated_database(tmp_path):
    """Rollback safety: the base commit's own statements cannot read or write the inventory once the
    store has migrated it, so an older build can never present original declarations as current."""
    path = str(tmp_path / "rollback.db")
    pid, _other, subs, _before = _legacy_db(path)
    store = SqliteRecordStore(path)
    _correct(store, pid, store.load_component_inventory(pid)[1][0].component_id, 0, "Fixed")
    store.close()
    conn = sqlite3.connect(path)
    try:
        conn.execute(_OLD_DDL)            # the older build's migration: a no-op on the new table
        conn.execute(_OLD_INDEX)
        with pytest.raises(sqlite3.OperationalError, match="component_seq"):
            conn.execute(_OLD_SELECT, (pid,)).fetchall()
        with pytest.raises(sqlite3.OperationalError, match="component_seq"):
            conn.execute(_OLD_INSERT, (pid, 3, "cmp-" + "a" * 32, "X", "x", "[]",
                                       OWNER_STATED, UNVALIDATED, "old-writer"))
        cols = [r[1] for r in conn.execute("PRAGMA table_info(project_components)")]
        assert "declaration_seq" in cols and "component_seq" not in cols
    finally:
        conn.close()
    fresh = str(tmp_path / "fresh.db")                      # a fresh database is guarded the same way
    SqliteRecordStore(fresh).close()
    conn = sqlite3.connect(fresh)
    try:
        with pytest.raises(sqlite3.OperationalError, match="component_seq"):
            conn.execute(_OLD_SELECT, ("p",)).fetchall()
    finally:
        conn.close()


# ==========================================================================
# 3. Persistence: revisions
# ==========================================================================
def test_s04_correct_and_withdraw_keep_identity_order_and_original_rows():
    store = _store()
    pid, subs = _new_project(store)
    a = _declare_store(store, pid, subs, "A", parts=(subs[0].subsystem_id,))
    b = _declare_store(store, pid, subs, "B")
    c = _declare_store(store, pid, subs, "C")
    originals = _rows(pid)
    outcome, rev = _correct(store, pid, b.component_id, 0, "B-fixed", "b2", (subs[1].subsystem_id,))
    assert outcome == PROJECT_COMPONENT_INSERTED and rev.revision_no == 1
    assert _withdraw(store, pid, a.component_id, 0)[0] == PROJECT_COMPONENT_INSERTED
    assert _rows(pid) == originals                          # declarations never touched
    _subs, current = store.load_component_inventory(pid)
    assert [x.component_id for x in current] == [b.component_id, c.component_id]   # original order
    assert (current[0].display_name, current[0].function_text, current[0].subsystem_ids) == (
        "B-fixed", "b2", (subs[1].subsystem_id,))
    assert all((x.provenance, x.validation_state) == (OWNER_STATED, UNVALIDATED) for x in current)
    _subs, inv = store.load_component_inventory_record(pid)
    assert [r.component_id for r in inv.withdrawn] == [a.component_id]
    assert [v.display_name for v in inv.record_for(b.component_id).versions] == ["B", "B-fixed"]
    assert _revs(pid) == sorted([(b.component_id, 1, "CORRECTED", "B-fixed"),
                                 (a.component_id, 1, "WITHDRAWN", None)])
    view = store.load_parts_components_interactions(pid)
    assert view["components"] == current
    assert [x.component_id for x in view["withdrawn_components"]] == [a.component_id]


def test_s05_an_exact_retry_replays_and_a_spent_identity_with_other_material_conflicts():
    store = _store()
    pid, subs = _new_project(store)
    a = _declare_store(store, pid, subs, "A")
    _subs, inv = _inventory(store, pid)
    rev = sm.corrected_component_revision(inv, subs, a.component_id, 0, "A2", "a", ())
    assert store.append_component_revision(pid, rev, "r1")[0] == PROJECT_COMPONENT_INSERTED
    twin = sm.corrected_component_revision(inv, subs, a.component_id, 0, "A2", "a", ())
    outcome, stored = store.append_component_revision(pid, twin, "r1")
    assert outcome == PROJECT_COMPONENT_EXACT_REPLAY and stored.revision_id == rev.revision_id
    other = sm.corrected_component_revision(inv, subs, a.component_id, 0, "A3", "a", ())
    with pytest.raises(ProjectComponentConflict):
        store.append_component_revision(pid, other, "r1")
    assert len(_revs(pid)) == 1
    assert store.committed_component_revision_for_submission(pid, "r1") == rev
    assert store.committed_component_revision_for_submission(pid, "nope") is None


def test_s06_stale_and_concurrent_attempts_commit_exactly_once(tmp_path):
    path = str(tmp_path / "race.db")
    store = SqliteRecordStore(path)
    pid, subs = _new_project(store)
    a = _declare_store(store, pid, subs, "A")
    _subs, inv = _inventory(store, pid)
    first = sm.corrected_component_revision(inv, subs, a.component_id, 0, "One", "a", ())
    second = sm.corrected_component_revision(inv, subs, a.component_id, 0, "Two", "a", ())
    results, barrier = [], threading.Barrier(2)

    def attempt(rev, key):
        own = SqliteRecordStore(path)          # one connection per thread
        try:
            barrier.wait()
            try:
                results.append(own.append_component_revision(pid, rev, key)[0])
            except ProjectComponentStale:
                results.append("STALE")
        finally:
            own.close()

    threads = [threading.Thread(target=attempt, args=(first, "t1")),
               threading.Thread(target=attempt, args=(second, "t2"))]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sorted(results) == [PROJECT_COMPONENT_INSERTED, "STALE"]
    check = SqliteRecordStore(path)
    _s, inv2 = check.load_component_inventory_record(pid)
    assert inv2.record_for(a.component_id).head_revision_no == 1
    # a revision prepared against the old head is refused, never merged
    with pytest.raises(ProjectComponentStale):
        check.append_component_revision(pid, sm.corrected_component_revision(
            inv, subs, a.component_id, 0, "Late", "a", ()), "late")
    check.close()
    store.close()


def test_s07_nothing_is_accepted_after_a_withdrawal_and_unchanged_corrections_are_refused():
    store = _store()
    pid, subs = _new_project(store)
    a = _declare_store(store, pid, subs, "A")
    _subs, inv = _inventory(store, pid)
    unchanged = sm.ComponentRevision(sm.new_component_revision_id(), a.component_id, 1,
                                     sm.COMPONENT_REVISION_CORRECTED, "A", "Does a thing", (),
                                     OWNER_STATED, UNVALIDATED)
    with pytest.raises(ProjectComponentUnchanged):
        store.append_component_revision(pid, unchanged, "u")
    _withdraw(store, pid, a.component_id, 0, key="w")
    for kind in (sm.COMPONENT_REVISION_CORRECTED, sm.COMPONENT_REVISION_WITHDRAWN):
        late = _rev(a.component_id, 2, kind=kind)
        with pytest.raises(ProjectComponentAlreadyWithdrawn):
            store.append_component_revision(pid, late, "late-" + kind)
    assert len(_revs(pid)) == 1
    # an exact retry of the committed withdrawal still replays
    outcome, _stored = store.append_component_revision(
        pid, sm.ComponentRevision(sm.new_component_revision_id(), a.component_id, 1,
                                  sm.COMPONENT_REVISION_WITHDRAWN, None, None, None,
                                  OWNER_STATED, UNVALIDATED), "w")
    assert outcome == PROJECT_COMPONENT_EXACT_REPLAY


def test_s08_active_lifetime_and_correction_bounds(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "caps.db"))
    pid, subs = _new_project(store, integrated=False)
    made = [_declare_store(store, pid, (), "C%d" % i, key="d%d" % i)
            for i in range(sm.MAX_PROJECT_COMPONENTS_PER_PROJECT)]
    with pytest.raises(ProjectComponentLimitReached) as exc:
        _declare_store(store, pid, (), "over", key="over")
    assert exc.value.limit == "active"
    # an exact retry of a committed declaration consumes no quota even at the bound
    assert store.append_project_component(pid, made[0], "d0")[0] == PROJECT_COMPONENT_EXACT_REPLAY
    _withdraw(store, pid, made[0].component_id, 0)             # withdrawal frees an active slot
    _declare_store(store, pid, (), "after", key="after")
    # 20 corrections, then the reserved withdrawal
    cid = made[1].component_id
    for n in range(sm.MAX_CORRECTIONS_PER_COMPONENT):
        _correct(store, pid, cid, n, "V%d" % n, key="v%d" % n)
    _s, inv = _inventory(store, pid)
    over = _rev(cid, 21)
    with pytest.raises((ProjectComponentLimitReached, ProjectComponentRejected)):
        store.append_component_revision(pid, over, "v-over")
    assert _withdraw(store, pid, cid, 20)[0] == PROJECT_COMPONENT_INSERTED
    store.close()
    # lifetime: 500 declared identities, never recycled (rows set up directly; 460 withdrawn)
    big = SqliteRecordStore(str(tmp_path / "lifetime.db"))
    pid2, _s = _new_project(big, integrated=False)
    with big._write():
        for i in range(sm.MAX_DECLARED_COMPONENTS_PER_PROJECT):
            item = sm.declared_component((), "L%d" % i, "l", ())
            big._conn.execute(
                "INSERT INTO project_components VALUES (?,?,?,?,?,?,?,?,?)",
                (pid2, i, item.component_id, item.display_name, item.function_text, "[]",
                 OWNER_STATED, UNVALIDATED, "L%d" % i))
            if i < 460:
                big._conn.execute(
                    "INSERT INTO project_component_revisions VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (pid2, item.component_id, 1, sm.new_component_revision_id(), "WITHDRAWN",
                     None, None, None, OWNER_STATED, UNVALIDATED, "W%d" % i))
    _subs, current = big.load_component_inventory(pid2)
    assert len(current) == 40
    with pytest.raises(ProjectComponentLimitReached) as exc:
        _declare_store(big, pid2, (), "501", key="501")
    assert exc.value.limit == "lifetime"
    with pytest.raises(sqlite3.IntegrityError):                # the database backstop
        with big._write():
            big._conn.execute("INSERT INTO project_components VALUES (?,?,?,?,?,?,?,?,?)",
                              (pid2, 500, "cmp-" + "b" * 32, "X", "x", "[]", OWNER_STATED,
                               UNVALIDATED, "raw"))
    big.close()


@pytest.mark.parametrize("label,sql,params_fn,fk", [
    ("gap", "UPDATE project_component_revisions SET revision_no = 2", None, True),
    ("after withdrawal", "INSERT INTO project_component_revisions VALUES "
     "(?, ?, 2, ?, 'CORRECTED', 'Again', 'x', '[]', 'OWNER_STATED', 'UNVALIDATED', 'raw-2')",
     "after", True),
    ("foreign component", "INSERT INTO project_component_revisions VALUES "
     "(?, ?, 1, ?, 'WITHDRAWN', NULL, NULL, NULL, 'OWNER_STATED', 'UNVALIDATED', 'raw-3')",
     "foreign", False),
    ("malformed parts", "UPDATE project_component_revisions SET subsystem_ids = '[ ]' "
     "WHERE kind = 'CORRECTED'", None, True),
    ("part of another project", "UPDATE project_component_revisions SET subsystem_ids = "
     "'[\"sub-%s\"]' WHERE kind = 'CORRECTED'" % ("0" * 32), None, True),
    ("malformed revision id", "UPDATE project_component_revisions SET revision_id = "
     "'crv-' || upper(substr(revision_id, 5))", None, True),
])
def test_s09_any_history_defect_fails_every_reader_and_writer_closed(label, sql, params_fn, fk):
    store = _store()
    pid, subs = _new_project(store)
    a = _declare_store(store, pid, subs, "A")
    b = _declare_store(store, pid, subs, "B")
    _correct(store, pid, b.component_id, 0, "B2", parts=(subs[0].subsystem_id,))
    _withdraw(store, pid, a.component_id, 0)
    params = ()
    if params_fn == "after":
        params = (pid, a.component_id, sm.new_component_revision_id())
    elif params_fn == "foreign":
        other, osubs = _new_project(store)
        foreign = _declare_store(store, other, osubs, "Foreign", key="foreign")
        params = (pid, foreign.component_id, sm.new_component_revision_id())
    if sql.startswith("INSERT"):
        _raw(sql, params, fk=fk)
    elif " WHERE " in sql:
        _raw(sql + " AND project_id = ?", (pid,), fk=fk)
    else:
        _raw(sql + " WHERE project_id = ?", (pid,), fk=fk)
    for read in (lambda: store.load_component_inventory(pid),
                 lambda: store.load_component_inventory_record(pid),
                 lambda: store.load_parts_components_interactions(pid),
                 lambda: store.committed_project_component_for_submission(pid, "k-A"),
                 lambda: store.committed_component_revision_for_submission(pid, "x")):
        with pytest.raises(ProjectComponentsCorrupt):
            read()
    with pytest.raises(ProjectComponentsCorrupt):
        _declare_store(store, pid, subs, "New", key="new")
    with pytest.raises(ProjectComponentsCorrupt):
        store.append_component_revision(pid, _rev(b.component_id, 2, name="B3"), "b3")
    assert label


def test_s10_a_fork_cannot_be_stored_and_cross_project_revisions_are_refused():
    store = _store()
    pid, subs = _new_project(store)
    a = _declare_store(store, pid, subs, "A")
    _correct(store, pid, a.component_id, 0, "A2")
    with pytest.raises(sqlite3.IntegrityError):              # one position, one revision
        _raw("INSERT INTO project_component_revisions VALUES "
             "(?, ?, 1, ?, 'WITHDRAWN', NULL, NULL, NULL, 'OWNER_STATED', 'UNVALIDATED', 'fork')",
             (pid, a.component_id, sm.new_component_revision_id()))
    other, osubs = _new_project(store)
    with pytest.raises(ProjectComponentRejected):            # A is not a component of OTHER
        store.append_component_revision(other, _rev(a.component_id, 1, kind="WITHDRAWN"), "x")
    with pytest.raises(sqlite3.IntegrityError):              # composite FK backstop
        _raw("INSERT INTO project_component_revisions VALUES "
             "(?, ?, 1, ?, 'WITHDRAWN', NULL, NULL, NULL, 'OWNER_STATED', 'UNVALIDATED', 'fk')",
             (other, a.component_id, sm.new_component_revision_id()))
    assert _revs(other) == []


def test_s11_an_unresolved_connection_refuses_reads_and_writes(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "ir01.db"))
    pid, subs = _new_project(store)
    a = _declare_store(store, pid, subs, "A")
    store._conn.execute("BEGIN")
    try:
        for call in (lambda: store.load_component_inventory_record(pid),
                     lambda: store.committed_component_revision_for_submission(pid, "x"),
                     lambda: store.append_component_revision(
                         pid, _rev(a.component_id, 1, kind="WITHDRAWN"), "x")):
            with pytest.raises(RecordStoreConnectionUnsafe):
                call()
    finally:
        store._conn.execute("ROLLBACK")
    store.close()


# ==========================================================================
# 4. Web: routes, session page, consumers
# ==========================================================================
def _revision_forms(raw):
    return [{"action": a, "submission": _html.unescape(s), "id": i, "revision": r}
            for a, s, i, r in re.findall(
                r'action="/session/[^/]+/(correct|withdraw)-component".*?'
                r'name="component_revision_submission" value="([^"]*)".*?'
                r'name="component_id" value="([^"]*)".*?'
                r'name="component_revision" value="([^"]*)"', raw, re.S)]


def _form_for(raw, action, index=0):
    return [f for f in _revision_forms(raw) if f["action"] == action][index]


def _post_correct(c, sid, form, name, function="Turns slowly", parts=(), revision=None):
    return c.post(f"/session/{sid}/correct-component", data={
        "component_revision_submission": form["submission"], "component_id": form["id"],
        "component_revision": form["revision"] if revision is None else revision,
        "correction_name": name, "correction_function": function,
        "correction_part": list(parts)})


def _post_withdraw(c, sid, form, confirm=True, revision=None):
    data = {"component_revision_submission": form["submission"], "component_id": form["id"],
            "component_revision": form["revision"] if revision is None else revision}
    if confirm:
        data["withdraw_confirm"] = "yes"
    return c.post(f"/session/{sid}/withdraw-component", data=data)


def test_w01_a_correction_is_saved_and_shown_as_current_with_its_history(client):
    sid = _integrated(client)
    form = _form(_page(client, sid))
    _declare(client, sid, name="Motor", function="Turns", parts=[form["parts"][0]],
             submission=form["submission"])
    raw = _page(client, sid)
    r = _post_correct(client, sid, _form_for(raw, "correct"), "Gear motor", parts=[form["parts"][1]])
    assert r.status_code == 302 and _notice(sid) == ("UI_CI_MSG_CORRECTED", None)
    block = _block(_page(client, sid))
    assert block.count("<li data-ci-item ") == 1
    assert ">Gear motor<" in block and "data-ci-corrected" in block
    assert "data-ci-history" in block and 'data-ci-version-name>Motor<' in block
    assert ui_text.text("UI_CI_VERSION_ORIGINAL", "en") in block
    current = _block(_page(client, sid))
    assert _form_for(current, "correct")["revision"] == "1"
    assert len(_rows(sid)) == 1 and len(_revs(sid)) == 1


def test_w02_withdrawal_needs_confirmation_and_moves_the_component_to_history(client):
    sid = _integrated(client)
    _declare(client, sid, name="Motor", function="Turns")
    _declare(client, sid, name="Lid", function="Covers")
    raw = _page(client, sid)
    motor = _form_for(raw, "withdraw", 0)
    _post_withdraw(client, sid, motor, confirm=False)
    assert _notice(sid) == (None, "UI_CI_MSG_CONFIRM_WITHDRAW") and _revs(sid) == []
    raw = _page(client, sid)
    _post_withdraw(client, sid, _form_for(raw, "withdraw", 0))
    assert _notice(sid) == ("UI_CI_MSG_WITHDRAWN", None)
    block = _block(_page(client, sid))
    current = block.split("data-ci-withdrawn")[0]
    assert ">Lid<" in current and ">Motor<" not in current
    assert "data-ci-withdrawn-item" in block and "data-ci-withdrawn-name>Motor<" in block
    assert ui_text.text("UI_CI_WITHDRAWN_NOTE", "en").replace("'", "&#39;") in block
    raw = _page(client, sid)
    _post_withdraw(client, sid, _form_for(raw, "withdraw", 0))     # the last one too
    block = _block(_page(client, sid))
    assert "data-ci-item " not in block
    assert ui_text.text("UI_CI_NONE_CURRENT", "en") in block


def test_w03_an_exact_retry_is_recognised_and_a_reused_identity_fails_closed(client):
    sid = _ordinary(client)
    _declare(client, sid, name="Motor", function="Turns")
    form = _form_for(_page(client, sid), "correct")
    _post_correct(client, sid, form, "Gear motor")
    _post_correct(client, sid, form, "Gear motor")                   # refresh / double submit
    assert _notice(sid) == ("UI_CI_MSG_CORRECTED", None) and len(_revs(sid)) == 1
    _post_correct(client, sid, form, "Something else")               # spent identity, other material
    assert _notice(sid) == (None, "UI_CI_MSG_NOT_SAVED") and len(_revs(sid)) == 1


def test_w04_a_stale_form_is_refused_and_writes_nothing(client):
    sid = _ordinary(client)
    _declare(client, sid, name="Motor", function="Turns")
    raw = _page(client, sid)
    old_correct, old_withdraw = _form_for(raw, "correct"), _form_for(raw, "withdraw")
    _post_correct(client, sid, old_correct, "Gear motor")
    fresh = _form_for(_page(client, sid), "correct")
    stale = dict(fresh, revision="0")
    _post_correct(client, sid, stale, "Other motor")
    assert _notice(sid) == (None, "UI_CI_MSG_STALE")
    _post_withdraw(client, sid, dict(old_withdraw, submission=_form_for(
        _page(client, sid), "withdraw")["submission"]))
    assert _notice(sid) == (None, "UI_CI_MSG_STALE")
    assert len(_revs(sid)) == 1


def test_w05_authorization_csrf_identity_domain_and_foreign_components(client):
    from tests.test_commercial_evidence_capture import _client_for
    owner, _aid = _client_for("ccw-owner@example.com")
    sid = _integrated(owner)
    _declare(owner, sid, name="Motor", function="Turns")
    raw = _page(owner, sid)
    correct, withdraw = _form_for(raw, "correct"), _form_for(raw, "withdraw")
    intruder, _bid = _client_for("ccw-intruder@example.com")
    for r in (_post_correct(intruder, sid, correct, SECRET), _post_withdraw(intruder, sid, withdraw)):
        assert r.status_code in (302, 403, 404) and SECRET not in r.get_data(as_text=True)
    raw_client = appmod.app.test_client()                            # no CSRF token
    r = raw_client.post(f"/session/{sid}/withdraw-component", data={
        "component_revision_submission": withdraw["submission"], "component_id": withdraw["id"],
        "component_revision": "0", "withdraw_confirm": "yes"})
    assert r.status_code == 403
    # a declaration identity, or the other action's identity, is not a revision identity
    _post_correct(owner, sid, dict(correct, submission=_form(raw)["submission"]), SECRET)
    assert _notice(sid) == (None, "UI_CI_MSG_NOT_SAVED")
    _post_correct(owner, sid, dict(correct, submission=withdraw["submission"]), SECRET)
    assert _notice(sid) == (None, "UI_CI_MSG_NOT_SAVED")
    # a component of another project is never revisable from this one
    other = _integrated(owner)
    _declare(owner, other, name="Lid", function="Covers")
    foreign_id = _form_for(_page(owner, other), "correct")["id"]
    _post_correct(owner, sid, dict(correct, id=foreign_id), SECRET)
    assert _notice(sid) == (None, "UI_CI_MSG_REVISION_REJECTED")
    assert _revs(sid) == [] and _revs(other) == []


@pytest.mark.parametrize("field,value,key", [
    ("component_id", "cmp-NOT-AN-ID", "UI_CI_MSG_REVISION_REJECTED"),
    ("component_revision", "-1", "UI_CI_MSG_REVISION_REJECTED"),
    ("component_revision", "01", "UI_CI_MSG_REVISION_REJECTED"),
    ("correction_name", "", "UI_CI_MSG_INVALID"),
    ("correction_name", "n" * 81, "UI_CI_MSG_TOO_LONG"),
    ("correction_function", "f" * 301, "UI_CI_MSG_TOO_LONG"),
    ("correction_part", "sub-" + "0" * 32, "UI_CI_MSG_REVISION_REJECTED"),
])
def test_w06_invalid_input_is_rejected_never_repaired(client, field, value, key):
    sid = _integrated(client)
    _declare(client, sid, name="Motor", function="Turns")
    form = _form_for(_page(client, sid), "correct")
    data = {"component_revision_submission": form["submission"], "component_id": form["id"],
            "component_revision": form["revision"], "correction_name": "Gear motor",
            "correction_function": "Turns slowly", "correction_part": []}
    data[field] = [value] if field == "correction_part" else value
    client.post(f"/session/{sid}/correct-component", data=data)
    assert _notice(sid) == (None, key) and _revs(sid) == []


def test_w07_a_corrupt_history_shows_no_list_and_every_consumer_fails_closed(client):
    sid = _integrated(client)
    _declare(client, sid, name=SECRET, function="Turns")
    _post_correct(client, sid, _form_for(_page(client, sid), "correct"), SECRET + " v2")
    _raw("UPDATE project_component_revisions SET revision_no = 2 WHERE project_id = ?", (sid,))
    raw = _page(client, sid)
    block = _block(raw)
    assert 'data-ci-status="unavailable"' in block
    for marker in ("data-ci-form", "data-ci-correct-form", "data-ci-withdraw-form", "data-ci-item"):
        assert marker not in block
    assert SECRET not in raw                                    # never the declarations instead
    pci = client.get(f"/session/{sid}/parts-components-interactions")
    assert SECRET not in pci.get_data(as_text=True)
    assert ui_text.text("UI_PCI_UNAVAILABLE", "en").split(".")[0] in pci.get_data(as_text=True)


def test_w08_arabic_copy_and_isolated_inventor_text(client):
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    sid = _ordinary(client)
    _declare(client, sid, name="<b>Motor</b>", function="محرّك")
    _post_correct(client, sid, _form_for(_page(client, sid), "correct"), "<i>محرّك مُصحَّح</i>")
    raw = _page(client, sid)
    block = _html.unescape(_block(raw))
    for key in ("UI_CI_CORRECTED_MARK", "UI_CI_HISTORY_SUMMARY", "UI_CI_CORRECT_SUMMARY",
                "UI_CI_WITHDRAW_SUMMARY", "UI_CI_WITHDRAW_HINT", "UI_CI_WITHDRAW_CONFIRM",
                "UI_CI_MSG_CORRECTED"):
        assert ui_text.text(key, "ar") in block, key
    assert "<i>محرّك مُصحَّح</i>" not in raw and "&lt;i&gt;" in raw
    assert 'dir="rtl"' in raw
    for key in [k for k in ui_text.UI_STRINGS if k.startswith("UI_CI_")]:
        assert ui_text.UI_STRINGS[key]["en"].strip() and ui_text.UI_STRINGS[key]["ar"].strip(), key


def test_w09_the_declaration_form_states_which_bound_is_reached(client):
    sid = _ordinary(client)
    store = _store()
    for i in range(sm.MAX_PROJECT_COMPONENTS_PER_PROJECT):
        store.append_project_component(sid, sm.declared_component((), "C%d" % i, "c", ()),
                                       "cap-%d" % i)
    block = _block(_page(client, sid))
    assert "data-ci-form" not in block and ui_text.text("UI_CI_CAP", "en") in block
    entry = appmod.SESSION_STORE[sid]
    sub = appmod._submission_identity_for(sid, entry, appmod._COMPONENT_SUBMISSION_DOMAIN,
                                          appmod._COMPONENT_SUBMISSION_ENTRY_KEY)
    _declare(client, sid, name="Over", submission=sub)
    assert _notice(sid) == (None, "UI_CI_MSG_ACTIVE_LIMIT")
    _post_withdraw(client, sid, _form_for(_page(client, sid), "withdraw", 0))
    block = _block(_page(client, sid))
    assert "data-ci-form" in block                              # a withdrawal frees a place


# ==========================================================================
# 5. The three consumers present the same current projection
# ==========================================================================
def test_c01_parts_components_view_shows_current_and_withdrawn_apart(client):
    sid = _integrated(client)
    form = _form(_page(client, sid))
    _declare(client, sid, name="Motor", function="Turns", parts=[form["parts"][0]],
             submission=form["submission"])
    _declare(client, sid, name="Lid", function="Covers")
    raw = _page(client, sid)
    _post_correct(client, sid, _form_for(raw, "correct", 0), "Gear motor", parts=[form["parts"][1]])
    raw = _page(client, sid)
    _post_withdraw(client, sid, _form_for(raw, "withdraw", 1))
    page = client.get(f"/session/{sid}/parts-components-interactions").get_data(as_text=True)
    current, _, history = page.partition("data-pci-withdrawn-title")
    assert "data-pci-component-name>Gear motor<" in current and ">Motor<" not in current
    assert "data-pci-component-name>Lid<" not in current
    assert "data-pci-withdrawn-name>Lid<" in history
    assert ui_text.text("UI_CI_WITHDRAWN_STATUS", "en") in history


def test_c02_export_field_7_carries_current_components_only_in_original_order():
    from tests.test_stage35_component_disclosure_export import _doc, _field
    from tests.test_stage19_durable_success_criteria import _client_for
    appmod.app.config["TESTING"] = True
    c, _aid = _client_for("ccw-export@example.com")
    sid = _created(_compose(c, TIE_IDEA, focus=MECH))
    store = _store()
    subs = store.load_project_subsystems(sid)
    a = _declare_store(store, sid, subs, "Alpha")
    b = _declare_store(store, sid, subs, "Beta", parts=(subs[0].subsystem_id,))
    g = _declare_store(store, sid, subs, "Gamma")
    before = _field(_doc(c, sid)["content"], F7)
    assert [i["slots"]["name"]["value"] for i in before["items"]] == ["Alpha", "Beta", "Gamma"]
    _correct(store, sid, b.component_id, 0, "Beta corrected", "b2", (subs[1].subsystem_id,))
    _withdraw(store, sid, a.component_id, 0)
    doc = _doc(c, sid)
    f = _field(doc["content"], F7)
    assert f["marker"] == "RECORDED"
    assert [i["slots"]["name"]["value"] for i in f["items"]] == ["Beta corrected", "Gamma"]
    assert [i["item_key"] for i in f["items"]] == [F7 + ".1", F7 + ".2"]
    beta = f["items"][0]
    assert beta["slots"]["function"]["value"] == "b2" and len(beta["refs"]) == 1
    assert set(beta) == set(before["items"][1]) and set(beta["slots"]) == set(before["items"][1]["slots"])
    dumped = json.dumps(doc)
    for item in (a, b, g):
        assert item.component_id not in dumped
    assert "crv-" not in dumped and "Alpha" not in dumped and '"Beta"' not in dumped
    assert doc["disclosure_schema_version"] == "inventorai-disclosure/2"
    assert doc["export_format_version"] == "inventorai-disclosure-json/2"
    _withdraw(store, sid, b.component_id, 1)
    _withdraw(store, sid, g.component_id, 0)
    f = _field(_doc(c, sid)["content"], F7)
    assert (f["marker"], f["items"]) == ("NOTHING_RECORDED", [])


# ==========================================================================
# 6. No effect beyond the inventory; retention truth
# ==========================================================================
def test_x01_no_state_report_pdf_readiness_or_progression_effect(client, monkeypatch, caplog):
    from tests.test_stage15_integrated_invention_entry import _pdf_source
    sid = _integrated(client)
    _declare(client, sid, name="Motor", function="Turns")
    report_before = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    state_before = pickle.dumps(appmod.SESSION_STORE[sid]["state"])
    records_before = _raw("SELECT COUNT(*) FROM records WHERE project_id = ?", (sid,))
    with caplog.at_level("DEBUG"):
        _post_correct(client, sid, _form_for(_page(client, sid), "correct"), SECRET)
        _post_withdraw(client, sid, _form_for(_page(client, sid), "withdraw"))
    assert len(_revs(sid)) == 2
    assert pickle.dumps(appmod.SESSION_STORE[sid]["state"]) == state_before
    assert _raw("SELECT COUNT(*) FROM records WHERE project_id = ?", (sid,)) == records_before
    report = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert SECRET not in report and _stable(report) == _stable(report_before)
    assert SECRET not in _pdf_source(client, sid, monkeypatch)
    assert SECRET not in caplog.text
    for path in ("engine/read_export_service.py", "web/api_v1.py", "engine/export_adapter.py",
                 "engine/disclosure_export.py", "engine/derived_readiness.py",
                 "engine/readiness_snapshot.py", "engine/safety_signal.py",
                 "engine/session_reconstruction.py", "engine/idea_state.py",
                 "engine/deterministic_calculation.py", "engine/deliverable_assembler.py",
                 "engine/progression_loop.py"):
        text = open(os.path.join(_ROOT, path), encoding="utf-8").read()
        assert "project_component_revisions" not in text and "ComponentRevision" not in text, path


def test_x02_retention_document_states_withdrawal_is_not_erasure():
    doc = open(os.path.join(_ROOT, "docs", "DATA_RETENTION_POLICY.md"), encoding="utf-8").read()
    flat = re.sub(r"\s+", " ", doc)
    assert "`project_component_revisions`" in flat
    assert "Withdrawing a component is NOT deletion, NOT erasure" in flat
    assert "every version may persist in backups" in flat
    engine_src = "".join(open(os.path.join(_ROOT, "engine", n), encoding="utf-8").read()
                         for n in os.listdir(os.path.join(_ROOT, "engine")) if n.endswith(".py"))
    assert "DELETE FROM project_component" not in engine_src
    assert "UPDATE project_component" not in engine_src
