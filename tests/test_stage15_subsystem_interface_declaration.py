"""Stage 15 Slice 2 — Subsystem Interface Declaration & Verification Preparation.

For ONE integrated Mechanical + Electrical / Electronics invention (Stage 15
Slice 1 composition), the inventor can durably state, in their own words, how
the two existing parts are intended to interact, and obtains ONE traceable
verification-PREPARATION action for each such interaction:

  * the interface is owned by ``engine/subsystem_model.py`` — a bounded
    relation between existing durable subsystem identities (never an answer,
    assumption, contradiction, decision, gap, evidence, readiness or
    compatibility fact; never a ledger record);
  * ONE additive project-scoped sidecar (``subsystem_interfaces``) in the
    existing SQLite store; append-only; system-generated opaque ids; an
    UNORDERED endpoint pair (no direction); OWNER_STATED / UNVALIDATED;
  * durable write through the shared declared-action mechanics (binding →
    freshness → durable append → committed-state confirmation → retry /
    recovery) with IR-01 preserved;
  * composition + interfaces read under ONE snapshot; outside the replay;
  * ONE derived Requirement Landscape row + ONE Validation Plan
    verification-preparation step per interface — preparation, never
    verification, no compatibility conclusion.
"""
import dataclasses
import html as _html
import os
import random
import re
import sqlite3

import pytest

import web.app as appmod
from engine import domain_activation
from engine import session_reconstruction as SR
from engine import subsystem_model as sm
from engine.domain_rules import DomainResultKind, classify_domain
from engine.idea_state import (
    IdeaState, OWNER_STATED, UNVALIDATED, RELATIONSHIP_METADATA_DISPOSITIONS,
    DISPOSITION_CONTRADICTION_DECLARED, DISPOSITION_ASSUMPTION_DEPENDENCY_DECLARED)
from engine.requirement_landscape import derive_requirement_landscape
from engine.validation_plan import derive_validation_plan
from engine import record_store as rs
from engine.record_store import (
    ProjectNotFound, RecordStoreConnectionUnsafe, SqliteRecordStore,
    SubsystemInterfaceConflict, SubsystemInterfaceRejected,
    SubsystemInterfacesCorrupt, SUBSYSTEM_INTERFACE_EXACT_REPLAY,
    SUBSYSTEM_INTERFACE_INSERTED)
from tests.csrf_client import csrf_client
from tests.test_stage15_integrated_invention_entry import (
    ELEC, ELEC_IDEA, MECH, PARTS, TIE_IDEA, _CommitAndRollbackFail, _compose,
    _contract, _created, _live, _pair, _ri, _scope_block, _visible)
from web import ui_text

DESC = "The motor driver board powers the motor that swings the hinge arm."
_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


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


def _db_path():
    return os.environ["INVENTORAI_DB_PATH"]


def _raw(sql, params=(), fk=True, ignore_checks=False):
    conn = sqlite3.connect(_db_path())
    try:
        if not fk:
            conn.execute("PRAGMA foreign_keys = OFF")
        if ignore_checks:
            conn.execute("PRAGMA ignore_check_constraints = ON")
        cur = conn.execute(sql, params)
        rows = cur.fetchall()
        conn.commit()
        return rows
    finally:
        conn.close()


def _ifc_rows(pid=None):
    _store()
    if pid is None:
        return _raw("SELECT * FROM subsystem_interfaces")
    return _raw("SELECT * FROM subsystem_interfaces WHERE project_id = ? "
                "ORDER BY interface_seq", (pid,))


def _form(raw):
    out = {}
    for name in ("answer_token", "interface_binding", "interface_submission"):
        m = re.search(r'name="%s" value="([^"]*)"' % name, raw)
        out[name] = _html.unescape(m.group(1)) if m else None
    return out


def _page(c, sid):
    r = c.get(f"/session/{sid}")
    assert r.status_code == 200, r.status_code
    return r.get_data(as_text=True)


def _declare(c, sid, description=DESC, form=None, **over):
    data = dict(form or _form(_page(c, sid)))
    data["interface_description"] = description
    data["interface_confirm"] = "yes"
    data.update(over)
    return c.post(f"/session/{sid}/declare-interface", data=data)


def _integrated(c, focus=MECH):
    return _created(_compose(c, TIE_IDEA, focus=focus))


def _entry(sid):
    return appmod.SESSION_STORE[sid]


def _error(sid):
    return _entry(sid).get("_answer_error")


def _ifc_block(raw):
    m = re.search(r'<div class="integrated-interfaces".*?</section>', raw, re.S)
    return m.group(0) if m else None


def _new_project(store, focus=MECH):
    subs = _pair()
    pid = store.create_project(_contract(), reconstruction_inputs=_ri(focus),
                               subsystems=subs)
    return pid, subs


def _ifc(subs, description=DESC, reverse=False):
    a, b = subs[0].subsystem_id, subs[1].subsystem_id
    if reverse:
        a, b = b, a
    return sm.declared_interface(subs, a, b, description)


class _FailOn:
    """Wraps the store connection: the named statement(s) fail. ``commit_then``
    lets a COMMIT really happen and THEN raise (an uncertain outcome that did
    commit)."""

    def __init__(self, conn, prefix=None, commit_then=False):
        self._conn = conn
        self.prefix = prefix
        self.commit_then = commit_then
        self.armed = True

    def execute(self, sql, *args):
        if self.armed and self.commit_then and sql == "COMMIT":
            self.armed = False
            self._conn.execute(sql, *args)
            raise sqlite3.OperationalError("injected: outcome unknown")
        if self.armed and self.prefix and sql.startswith(self.prefix):
            self.armed = False
            raise sqlite3.OperationalError("injected: %s failed" % self.prefix)
        return self._conn.execute(sql, *args)

    def __getattr__(self, name):
        return getattr(self._conn, name)


# ==========================================================================
# 18.1 Model / semantic owner
# ==========================================================================
def test_interface_ids_are_system_generated_opaque_and_immutable():
    subs = _pair()
    a, b = _ifc(subs), _ifc(subs)
    for item in (a, b):
        assert sm.is_valid_interface_id(item.interface_id)
        assert re.fullmatch(r"ifc-[0-9a-f]{32}", item.interface_id)
        assert DESC not in item.interface_id and "sub-" not in item.interface_id
    assert a.interface_id != b.interface_id
    with pytest.raises(dataclasses.FrozenInstanceError):
        a.interface_id = "ifc-" + "0" * 32
    # the builder takes no id at all: a caller can never choose one
    assert "interface_id" not in sm.declared_interface.__code__.co_varnames[:4]


def test_the_client_can_never_choose_the_interface_id(client):
    sid = _integrated(client)
    forced = "ifc-" + "a" * 32
    assert _declare(client, sid, interface_id=forced).status_code == 302
    [row] = _ifc_rows(sid)
    assert row[2] != forced and sm.is_valid_interface_id(row[2])


def test_endpoints_must_be_two_distinct_parts_of_the_same_composition():
    subs = _pair()
    a, b = subs[0].subsystem_id, subs[1].subsystem_id
    with pytest.raises(sm.InterfaceError):
        sm.declared_interface(subs, a, a, DESC)                     # self
    with pytest.raises(sm.InterfaceError):
        sm.declared_interface(subs, a, sm.new_subsystem_id(), DESC)   # unknown
    other = _pair()
    with pytest.raises(sm.InterfaceError):
        sm.declared_interface(subs, a, other[1].subsystem_id, DESC)   # another project
    with pytest.raises(sm.InterfaceError):
        sm.declared_interface((), a, b, DESC)                         # no composition


def test_store_rejects_unknown_self_and_cross_project_endpoints():
    store = _store()
    pid, subs = _new_project(store)
    other_pid, other = _new_project(store)
    bad = [
        sm.SubsystemInterface(sm.new_interface_id(), subs[0].subsystem_id,
                              subs[0].subsystem_id, DESC, OWNER_STATED, UNVALIDATED),
        sm.SubsystemInterface(sm.new_interface_id(), subs[0].subsystem_id,
                              sm.new_subsystem_id(), DESC, OWNER_STATED, UNVALIDATED),
        sm.SubsystemInterface(sm.new_interface_id(), subs[0].subsystem_id,
                              other[1].subsystem_id, DESC, OWNER_STATED, UNVALIDATED),
        sm.SubsystemInterface(sm.new_interface_id(), subs[1].subsystem_id,
                              subs[0].subsystem_id, DESC, OWNER_STATED, UNVALIDATED),
    ]
    for n, item in enumerate(bad):
        with pytest.raises(SubsystemInterfaceRejected):
            store.append_subsystem_interface(pid, item, "k%d" % n)
    assert _ifc_rows(pid) == [] and _ifc_rows(other_pid) == []
    # a project WITHOUT a composition accepts no interface at all
    plain = store.create_project(_contract("plain"), reconstruction_inputs=_ri())
    with pytest.raises(SubsystemInterfaceRejected):
        store.append_subsystem_interface(plain, _ifc(subs), "kp")


def test_owner_text_is_trimmed_and_bounded_never_truncated():
    subs = _pair()
    assert _ifc(subs, "  " + DESC + "\n").description == DESC
    assert _ifc(subs, "x" * sm.MAX_INTERFACE_DESCRIPTION_LENGTH).description \
        == "x" * sm.MAX_INTERFACE_DESCRIPTION_LENGTH
    for bad in ("", "   \n", "a\x00b", "x" * (sm.MAX_INTERFACE_DESCRIPTION_LENGTH + 1),
                None, 7):
        with pytest.raises(sm.InterfaceError):
            _ifc(subs, bad)
    # the bound follows the repository precedent (the part function text)
    assert sm.MAX_INTERFACE_DESCRIPTION_LENGTH == sm.MAX_SUBSYSTEM_FUNCTION_LENGTH


def test_several_distinct_interfaces_may_join_the_same_two_parts():
    store = _store()
    pid, subs = _new_project(store)
    texts = ["Power flows over a two-wire cable.", "The board is screwed to the arm.",
             "A limit switch reports the arm position."]
    for n, text in enumerate(texts):
        outcome, stored = store.append_subsystem_interface(pid, _ifc(subs, text), "k%d" % n)
        assert outcome == SUBSYSTEM_INTERFACE_INSERTED
    loaded = store.load_subsystem_interfaces(pid)
    assert [i.description for i in loaded] == texts
    assert len({i.interface_id for i in loaded}) == 3
    assert {(i.subsystem_a_id, i.subsystem_b_id) for i in loaded} == {
        (subs[0].subsystem_id, subs[1].subsystem_id)}


def test_endpoint_order_carries_no_direction():
    subs = _pair()
    forward, backward = _ifc(subs), _ifc(subs, reverse=True)
    # both inputs are stored as the same canonical (composition-order) pair
    assert (forward.subsystem_a_id, forward.subsystem_b_id) == (
        backward.subsystem_a_id, backward.subsystem_b_id) == (
        subs[0].subsystem_id, subs[1].subsystem_id)
    assert sm.same_interface_material(forward, backward)
    # no field or column names a direction, flow, dependency or role
    names = [f.name for f in dataclasses.fields(sm.SubsystemInterface)]
    assert names == ["interface_id", "subsystem_a_id", "subsystem_b_id",
                     "description", "provenance", "validation_state"]
    columns = [r[1] for r in _raw("PRAGMA table_info(subsystem_interfaces)")] \
        if _store() else []
    assert columns == ["project_id", "interface_seq", "interface_id",
                       "subsystem_a_id", "subsystem_b_id", "description",
                       "provenance", "validation_state", "submission_key"]
    for word in ("source", "target", "direction", "flow", "from", "to_",
                 "depend", "upstream", "downstream", "compatib"):
        assert all(word not in name for name in names + columns), word


def test_provenance_and_validation_state_are_fixed():
    item = _ifc(_pair())
    assert item.provenance == OWNER_STATED == "OWNER_STATED"
    assert item.validation_state == UNVALIDATED == "UNVALIDATED"


def test_part_facts_are_never_copied_into_the_interface():
    subs = _pair()
    item = _ifc(subs)
    values = dataclasses.asdict(item).values()
    for sub in subs:
        assert sub.display_name not in values and sub.function_text not in values
        assert sub.domain not in values


def test_no_interface_taxonomy_or_inference_exists():
    src = open(os.path.join(_ROOT, "engine", "subsystem_model.py"), encoding="utf-8").read()
    assert "NASA" not in src
    public = [n.upper() for n in dir(sm)]
    for word in ("CATEGOR", "TAXONOM", "INTERFACE_TYPE", "INTERFACE_KIND"):
        assert not any(word in n for n in public), word
    fields = [f.name for f in dataclasses.fields(sm.SubsystemInterface)]
    assert not any(w in f for f in fields for w in ("category", "type", "kind", "class"))
    # nothing infers an interface from a composition: a fresh project has none
    store = _store()
    pid, _subs = _new_project(store)
    assert store.load_subsystem_interfaces(pid) == ()


def test_ordinary_projects_have_zero_interfaces(client):
    sid = _created(client.post("/start", data={"idea": ELEC_IDEA, "domain_confirm": ELEC}))
    assert _live(sid).subsystem_interfaces == []
    assert _store().load_subsystem_interfaces(sid) == ()
    raw = _page(client, sid)
    assert _form(raw)["interface_binding"] is None
    assert "integrated-interfaces" not in raw
    assert IdeaState(idea_id="x").subsystem_interfaces == []


# ==========================================================================
# 18.2 Persistence / schema
# ==========================================================================
def test_fresh_database_has_the_additive_table_and_no_rows():
    _store()
    names = {r[0] for r in _raw("SELECT name FROM sqlite_master")}
    assert {"subsystem_interfaces", "subsystem_interfaces_id_uq"} <= names
    assert _ifc_rows() == []


def test_migration_is_additive_idempotent_and_never_backfills(tmp_path):
    path = str(tmp_path / "pre_slice.db")
    store = SqliteRecordStore(path)
    pid, subs = _new_project(store)
    store.close()
    conn = sqlite3.connect(path)
    conn.execute("DROP TABLE subsystem_interfaces")         # a pre-slice database
    conn.commit()
    tables = ("projects", "records", "project_subsystems", "need_routing_revisions")
    before = {t: conn.execute("SELECT * FROM %s ORDER BY 1, 2" % t).fetchall()
              for t in tables}
    conn.close()
    for _ in range(2):                                      # forward, then idempotent
        store = SqliteRecordStore(path)
        assert store.load_subsystem_interfaces(pid) == ()   # nothing backfilled
        assert [s.subsystem_id for s in store.load_project_subsystems(pid)] == [
            s.subsystem_id for s in subs]
        store.close()
        conn = sqlite3.connect(path)
        after = {t: conn.execute("SELECT * FROM %s ORDER BY 1, 2" % t).fetchall()
                 for t in tables}
        assert after == before
        assert conn.execute("SELECT COUNT(*) FROM subsystem_interfaces").fetchone()[0] == 0
        conn.close()
    for stmt in rs._SUBSYSTEM_INTERFACES_SCHEMA:
        for word in ("DROP", "DELETE", "UPDATE", "ALTER"):
            assert word not in stmt.upper()


def test_append_close_and_reopen_round_trips_the_exact_declarations(tmp_path):
    path = str(tmp_path / "rt.db")
    store = SqliteRecordStore(path)
    pid, subs = _new_project(store)
    written = [store.append_subsystem_interface(pid, _ifc(subs, t), "k%d" % n)[1]
               for n, t in enumerate(["First interaction.", "Second interaction."])]
    store.close()
    reopened = SqliteRecordStore(path)
    assert list(reopened.load_subsystem_interfaces(pid)) == written
    subs2, ifcs2 = reopened.load_subsystem_composition(pid)
    assert [s.subsystem_id for s in subs2] == [s.subsystem_id for s in subs]
    assert list(ifcs2) == written
    reopened.close()


def test_exact_retry_returns_the_committed_declaration_and_writes_nothing():
    store = _store()
    pid, subs = _new_project(store)
    first = _ifc(subs)
    assert store.append_subsystem_interface(pid, first, "key-1")[0] == SUBSYSTEM_INTERFACE_INSERTED
    retry = _ifc(subs, reverse=True)                  # a NEW id, same material
    outcome, stored = store.append_subsystem_interface(pid, retry, "key-1")
    assert outcome == SUBSYSTEM_INTERFACE_EXACT_REPLAY
    assert stored == first and stored.interface_id != retry.interface_id
    assert len(_ifc_rows(pid)) == 1


def test_same_submission_identity_with_different_material_is_rejected():
    store = _store()
    pid, subs = _new_project(store)
    store.append_subsystem_interface(pid, _ifc(subs), "key-1")
    with pytest.raises(SubsystemInterfaceConflict):
        store.append_subsystem_interface(pid, _ifc(subs, "Something else."), "key-1")
    [row] = _ifc_rows(pid)
    assert row[5] == DESC


def test_duplicate_durable_identity_is_rejected():
    store = _store()
    pid, subs = _new_project(store)
    item = _ifc(subs)
    store.append_subsystem_interface(pid, item, "key-1")
    same_id = dataclasses.replace(_ifc(subs, "Other text."), interface_id=item.interface_id)
    with pytest.raises(SubsystemInterfaceRejected):
        store.append_subsystem_interface(pid, same_id, "key-2")
    # the database is a backstop too (store-wide unique id)
    other_pid, other = _new_project(store)
    with pytest.raises(sqlite3.IntegrityError):
        _raw("INSERT INTO subsystem_interfaces VALUES (?,?,?,?,?,?,?,?,?)",
             (other_pid, 0, item.interface_id, other[0].subsystem_id,
              other[1].subsystem_id, DESC, OWNER_STATED, UNVALIDATED, "k"))
    assert len(_ifc_rows(pid)) == 1 and _ifc_rows(other_pid) == []


@pytest.mark.parametrize("mutation", [
    ("UPDATE subsystem_interfaces SET interface_id = ? WHERE project_id = ?",
     "ifc-" + "Z" * 32, {}),
    ("UPDATE subsystem_interfaces SET subsystem_a_id = ? WHERE project_id = ?",
     "sub-" + "f" * 32, {"fk": False}),
    ("UPDATE subsystem_interfaces SET subsystem_a_id = subsystem_b_id, "
     "subsystem_b_id = subsystem_a_id WHERE project_id = ? AND ? IS NOT NULL",
     None, {}),
    ("UPDATE subsystem_interfaces SET provenance = ? WHERE project_id = ?",
     "SYSTEM_INFERRED", {"ignore_checks": True}),
    ("UPDATE subsystem_interfaces SET validation_state = ? WHERE project_id = ?",
     "VALIDATED", {"ignore_checks": True}),
    ("UPDATE subsystem_interfaces SET interface_seq = ? WHERE project_id = ?",
     5, {}),
    ("UPDATE subsystem_interfaces SET description = ? WHERE project_id = ?",
     " padded ", {}),
])
def test_malformed_durable_rows_fail_closed(mutation):
    sql, value, kw = mutation
    store = _store()
    pid, subs = _new_project(store)
    store.append_subsystem_interface(pid, _ifc(subs), "key-1")
    if value is None:
        _raw(sql, (pid, 1), **kw)
    else:
        _raw(sql, (value, pid), **kw)
    with pytest.raises(SubsystemInterfacesCorrupt):
        store.load_subsystem_interfaces(pid)
    with pytest.raises(SubsystemInterfacesCorrupt):
        store.committed_subsystem_interface_for_submission(pid, "key-1")
    with pytest.raises(SubsystemInterfacesCorrupt):
        store.append_subsystem_interface(pid, _ifc(subs, "New."), "key-2")


def test_orphaned_cross_project_endpoint_fails_closed():
    store = _store()
    pid, subs = _new_project(store)
    _other_pid, other = _new_project(store)
    store.append_subsystem_interface(pid, _ifc(subs), "key-1")
    _raw("UPDATE subsystem_interfaces SET subsystem_b_id = ? WHERE project_id = ?",
         (other[1].subsystem_id, pid), fk=False)
    with pytest.raises(SubsystemInterfacesCorrupt):
        store.load_subsystem_interfaces(pid)
    # interfaces surviving without any composition fail closed as well
    _raw("DELETE FROM project_subsystems WHERE project_id = ?", (pid,), fk=False)
    with pytest.raises(SubsystemInterfacesCorrupt):
        store.load_subsystem_interfaces(pid)


def test_failure_during_the_interface_insert_leaves_nothing_partial():
    store = _store()
    pid, subs = _new_project(store)
    before = (_raw("SELECT * FROM projects WHERE project_id = ?", (pid,)),
              _raw("SELECT * FROM project_subsystems WHERE project_id = ?", (pid,)))
    real = store._conn
    store._conn = _FailOn(real, prefix="INSERT INTO subsystem_interfaces")
    try:
        with pytest.raises(sqlite3.OperationalError):
            store.append_subsystem_interface(pid, _ifc(subs), "key-1")
    finally:
        store._conn = real
    assert store._connection_unsafe is False
    assert _ifc_rows(pid) == []
    assert (_raw("SELECT * FROM projects WHERE project_id = ?", (pid,)),
            _raw("SELECT * FROM project_subsystems WHERE project_id = ?", (pid,))) == before


def test_only_the_existing_sqlite_store_is_used(tmp_path):
    path = str(tmp_path / "one.db")
    store = SqliteRecordStore(path)
    pid, subs = _new_project(store)
    store.append_subsystem_interface(pid, _ifc(subs), "key-1")
    store.close()
    assert sorted(os.listdir(tmp_path)) == ["one.db"]
    src = open(os.path.join(_ROOT, "engine", "subsystem_model.py"), encoding="utf-8").read()
    for word in ("sqlite", "open(", "requests", "urllib", "socket", "json"):
        assert word not in src, word


# ==========================================================================
# 18.3 Transaction / recovery / IR-01
# ==========================================================================
def test_commit_failure_with_a_clean_rollback_writes_nothing(client):
    sid = _integrated(client)
    form = _form(_page(client, sid))
    store = _store()
    real = store._conn
    store._conn = _FailOn(real, prefix="COMMIT")
    try:
        r = _declare(client, sid, form=form)
    finally:
        store._conn = real
    assert r.status_code == 302
    assert store._connection_unsafe is False and not real.in_transaction
    assert _ifc_rows(sid) == []
    assert _live(sid).subsystem_interfaces == []
    assert _error(sid) == appmod.S15_INTERFACE_NOT_SAVED_MESSAGE


def test_unresolved_commit_and_rollback_is_reported_as_unknown_and_never_read(client):
    sid = _integrated(client)
    form = _form(_page(client, sid))
    store = _store()
    real = store._conn
    store._conn = _CommitAndRollbackFail(real)
    try:
        r = _declare(client, sid, form=form)
    finally:
        store._conn = real
    try:
        assert r.status_code == 503                          # bounded UNKNOWN response
        assert store._connection_unsafe is True and real.in_transaction
        # the hazard is real: THIS connection sees its own uncommitted row ...
        assert real.execute("SELECT COUNT(*) FROM subsystem_interfaces").fetchone()[0] == 1
        # ... an independent connection sees nothing committed
        assert _raw("SELECT COUNT(*) FROM subsystem_interfaces")[0][0] == 0
        assert appmod.S15_INTERFACE_UNKNOWN_MESSAGE in _html.unescape(r.get_data(as_text=True))
        assert _error(sid) is None                           # never NOT SAVED
        assert _live(sid).subsystem_interfaces == []        # nothing published
        for call in (lambda: store.load_subsystem_interfaces(sid),
                     lambda: store.load_subsystem_composition(sid),
                     lambda: store.committed_subsystem_interface_for_submission(sid, "k"),
                     lambda: store.append_subsystem_interface(sid, _ifc(_pair()), "k")):
            with pytest.raises(RecordStoreConnectionUnsafe):
                call()
        probe = IdeaState(idea_id="probe")
        assert appmod._attach_project_subsystems(sid, probe) is False
        assert probe.subsystem_interfaces == []
        with pytest.raises(RecordStoreConnectionUnsafe):
            SR.reconstruct_readonly_state(store, sid)
        assert store._connection_unsafe is True               # never cleared
    finally:
        real.close()
        appmod._STORE = None
    assert _store().load_subsystem_interfaces(sid) == ()


def test_a_healthy_read_snapshot_is_not_refused(client):
    sid = _integrated(client)
    assert _declare(client, sid).status_code == 302
    store = _store()
    with store.read_snapshot():
        assert store._conn.in_transaction
        subs, ifcs = store.load_subsystem_composition(sid)
        assert len(ifcs) == 1 and len(subs) == 2
    session = SR.reconstruct_readonly_state(store, sid)
    assert [i.interface_id for i in session.state.subsystem_interfaces] == [
        ifcs[0].interface_id]


def test_committed_but_unconfirmed_attempt_publishes_the_stored_id(client):
    sid = _integrated(client)
    form = _form(_page(client, sid))
    store = _store()
    real = store._conn
    store._conn = _FailOn(real, commit_then=True)             # commits, then raises
    try:
        r = _declare(client, sid, form=form)
    finally:
        store._conn = real
    assert r.status_code == 302 and store._connection_unsafe is False
    [row] = _ifc_rows(sid)
    assert [i.interface_id for i in _live(sid).subsystem_interfaces] == [row[2]]
    assert _entry(sid).get("_interaction_ack") == appmod.S15_INTERFACE_DECLARED_ACK
    # the retry of the SAME submission is recognised before any new mint
    minted = []
    real_new = sm.new_interface_id
    try:
        sm.new_interface_id = lambda: minted.append(1) or real_new()
        assert _declare(client, sid, form=form).status_code == 302
    finally:
        sm.new_interface_id = real_new
    assert minted == [] and len(_ifc_rows(sid)) == 1
    assert [i.interface_id for i in _live(sid).subsystem_interfaces] == [row[2]]


def test_recovery_never_publishes_a_new_id_when_another_attempt_committed():
    store = _store()
    pid, subs = _new_project(store)
    committed = _ifc(subs)
    store.append_subsystem_interface(pid, committed, "key-1")
    fresh_attempt = _ifc(subs)
    outcome, stored = store.append_subsystem_interface(pid, fresh_attempt, "key-1")
    assert outcome == SUBSYSTEM_INTERFACE_EXACT_REPLAY
    assert stored.interface_id == committed.interface_id != fresh_attempt.interface_id
    assert store.committed_subsystem_interface_for_submission(pid, "key-1") == committed


# ==========================================================================
# 18.4 Reconstruction / cold load / resume
# ==========================================================================
def test_cold_load_reconstruction_and_resume_restore_the_exact_interfaces(client):
    sid = _integrated(client)
    _declare(client, sid, "First interaction.")
    _declare(client, sid, "Second interaction.")
    ids = [i.interface_id for i in _live(sid).subsystem_interfaces]
    sub_ids = [s.subsystem_id for s in _live(sid).subsystems]
    assert len(ids) == 2
    appmod.SESSION_STORE.clear()
    with appmod.app.test_request_context("/"):
        cold = appmod._cold_load_entry(sid)["state"]
    assert [i.interface_id for i in cold.subsystem_interfaces] == ids
    session = SR.reconstruct_readonly_state(_store(), sid)
    assert [i.interface_id for i in session.state.subsystem_interfaces] == ids
    assert [s.subsystem_id for s in session.state.subsystems] == sub_ids
    assert client.post(f"/session/{sid}/resume", data={}).status_code == 302
    resumed = _live(sid)
    assert [i.interface_id for i in resumed.subsystem_interfaces] == ids
    assert [i.description for i in resumed.subsystem_interfaces] == [
        "First interaction.", "Second interaction."]
    assert [s.subsystem_id for s in resumed.subsystems] == sub_ids
    for item in resumed.subsystem_interfaces:
        assert {item.subsystem_a_id, item.subsystem_b_id} == set(sub_ids)


def test_composition_and_interfaces_are_read_in_one_snapshot(monkeypatch):
    store = _store()
    pid, subs = _new_project(store)
    store.append_subsystem_interface(pid, _ifc(subs), "key-1")
    seen = []
    real_rows = store._interface_rows

    def spy(project_id):
        seen.append(store._conn.in_transaction)
        return real_rows(project_id)
    monkeypatch.setattr(store, "_interface_rows", spy)
    store.load_subsystem_composition(pid)
    assert seen == [True]                           # inside ONE read transaction
    assert not store._conn.in_transaction           # and the snapshot ended
    # reconstruction reads both through the SAME combined reader
    calls = []
    real_combined = store.load_subsystem_composition
    monkeypatch.setattr(store, "load_subsystem_composition",
                        lambda p: calls.append(p) or real_combined(p))
    SR.reconstruct_readonly_state(store, pid)
    assert calls == [pid]


def test_corrupt_interface_state_fails_every_read_path_closed(client):
    sid = _integrated(client)
    _declare(client, sid)
    _raw("UPDATE subsystem_interfaces SET interface_id = ? WHERE project_id = ?",
         ("ifc-" + "Z" * 32, sid))
    with pytest.raises(SubsystemInterfacesCorrupt):
        SR.reconstruct_readonly_state(_store(), sid)
    assert appmod._attach_project_subsystems(sid, IdeaState(idea_id="p")) is False
    with appmod.app.test_request_context("/"):
        assert appmod._cold_load_entry(sid) is None
    assert client.get(f"/session/{sid}").status_code == 302
    assert client.get(f"/session/{sid}/deliverable").status_code in (302, 503)


def _question(raw):
    m = re.search(r'<p class="question" lang=[^>]*>(.*?)</p>', raw, re.S)
    return _html.unescape(m.group(1)).strip() if m else None


def _replay_facts(state):
    return (tuple((r.record_id, r.disposition, r.content, r.superseded_by)
                  for r in state.assertions),
            tuple((g.gap_type, g.status) for g in state.gaps),
            state.maturity_level, state.current_stage, getattr(state, "domain", None),
            state.domain_signal, tuple(state.need_routing or ()))


def test_interfaces_stay_outside_the_replay_and_change_nothing_else(client):
    sid = _integrated(client, focus=MECH)
    tok = _form(_page(client, sid))["answer_token"]
    client.post(f"/session/{sid}", data={
        "response": "The arm swings on a pin.", "action": "answered",
        "answer_token": tok})
    before = SR.reconstruct_readonly_state(_store(), sid).state
    live_before = _replay_facts(_live(sid))
    question_before = _form(_page(client, sid))
    question_text = _question(_page(client, sid))
    assert _declare(client, sid).status_code == 302
    assert len(_live(sid).subsystem_interfaces) == 1
    after = SR.reconstruct_readonly_state(_store(), sid).state
    assert _replay_facts(after) == _replay_facts(before)
    assert _replay_facts(_live(sid)) == live_before
    assert after.domain == MECH == _live(sid).domain
    ledger = _store().load_contract(sid).assertions
    assert all("interface" not in (r.disposition or "") for r in ledger)
    # the served question and its answer token are unchanged
    assert _form(_page(client, sid))["answer_token"] == question_before["answer_token"]
    assert _question(_page(client, sid)) == question_text and question_text
    assert _store().load_reconstruction_inputs(sid)["confirmed_domain"] == MECH


# ==========================================================================
# 18.5 Requirement Landscape
# ==========================================================================
def _state_with(interfaces_texts, focus=MECH):
    subs = _pair()
    state = IdeaState(idea_id="landscape")
    state.domain = focus
    state.subsystems = list(subs)
    state.subsystem_interfaces = [_ifc(subs, t) for t in interfaces_texts]
    return state, subs


def test_one_deterministic_derived_requirement_per_interface():
    state, subs = _state_with(["Power over a cable.", "Bolted mounting."])
    reqs = [r for r in derive_requirement_landscape(state).requirements
            if r.primary_anchor.anchor_kind == "subsystem_interface"]
    assert len(reqs) == 2
    by_ref = {r.primary_anchor.anchor_reference: r for r in reqs}
    for item in state.subsystem_interfaces:
        req = by_ref[item.interface_id]
        assert req.requirement_id == "req:interface:" + item.interface_id
        assert req.primary_anchor.display_label == "Interface you declared"
        assert subs[0].display_name in req.statement and subs[1].display_name in req.statement
        assert item.description in req.statement
        assert "compatibility between the parts has not been assessed" in req.statement
        assert req.criticality == "UNDETERMINED" and req.linked_risk_ids == ()
    # identity follows the id, never the position or the wording
    shuffled, _ = _state_with([])
    shuffled.subsystems = state.subsystems
    shuffled.subsystem_interfaces = list(reversed(state.subsystem_interfaces))
    assert derive_requirement_landscape(shuffled) == derive_requirement_landscape(state)
    reworded = dataclasses.replace(state.subsystem_interfaces[0], description="Changed.")
    state.subsystem_interfaces[0] = reworded
    assert "req:interface:" + reworded.interface_id in {
        r.requirement_id for r in derive_requirement_landscape(state).requirements}


def test_interface_requirements_are_derived_only_never_persisted(client):
    sid = _integrated(client)
    _declare(client, sid)
    iid = _live(sid).subsystem_interfaces[0].interface_id
    assert "req:interface:" + iid in {
        r.requirement_id for r in derive_requirement_landscape(_live(sid)).requirements}
    conn = sqlite3.connect(_db_path())
    try:
        for (table,) in conn.execute("SELECT name FROM sqlite_master WHERE type='table'"):
            for row in conn.execute("SELECT * FROM %s" % table):
                assert not any(isinstance(v, str) and "req:interface" in v for v in row)
    finally:
        conn.close()


def test_no_interface_keeps_the_landscape_and_plan_unchanged(client):
    sid = _integrated(client)
    tok = _form(_page(client, sid))["answer_token"]
    client.post(f"/session/{sid}", data={"response": "It swings on a pin.",
                                         "action": "answered", "answer_token": tok})
    state = _live(sid)
    base_l, base_p = derive_requirement_landscape(state), derive_validation_plan(state)
    legacy = IdeaState(idea_id=state.idea_id)
    for f in dataclasses.fields(state):
        setattr(legacy, f.name, getattr(state, f.name))
    object.__delattr__(legacy, "subsystem_interfaces") if hasattr(
        type(legacy), "__slots__") else legacy.__dict__.pop("subsystem_interfaces")
    assert derive_requirement_landscape(legacy) == base_l
    assert derive_validation_plan(legacy) == base_p
    # adding an interface adds exactly one row / one step and nothing else
    _declare(client, sid)
    after_l = derive_requirement_landscape(_live(sid))
    after_p = derive_validation_plan(_live(sid))
    assert tuple(r for r in after_l.requirements
                 if r.primary_anchor.anchor_kind != "subsystem_interface") == base_l.requirements
    assert tuple(s for s in after_p.steps
                 if s.provenance.anchor_kind != "subsystem_interface") == base_p.steps
    assert after_p.blocked_items == base_p.blocked_items
    assert after_l.risks == base_l.risks == ()


def test_relationship_exclusions_and_risk_ownership_are_unchanged():
    assert RELATIONSHIP_METADATA_DISPOSITIONS == frozenset({
        DISPOSITION_CONTRADICTION_DECLARED, DISPOSITION_ASSUMPTION_DEPENDENCY_DECLARED})
    state, _subs = _state_with(["Power over a cable."])
    assert derive_requirement_landscape(state).risks == ()


def test_interface_text_never_becomes_compatibility_truth():
    state, _ = _state_with(["They are fully compatible and verified."])
    for req in derive_requirement_landscape(state).requirements:
        if req.primary_anchor.anchor_kind == "subsystem_interface":
            assert req.source_status == "declared by you; not validated"
            assert "has not been validated" in req.statement
    for step in derive_validation_plan(state).steps:
        assert "Compatibility remains unassessed." in step.statement
        assert "does not verify the interaction or establish compatibility" \
            in step.closure_condition


# ==========================================================================
# 18.6 Validation Plan
# ==========================================================================
def test_one_bounded_verification_preparation_step_per_interface():
    state, subs = _state_with(["Power over a cable.", "Bolted mounting."])
    steps = [s for s in derive_validation_plan(state).steps
             if s.provenance.anchor_kind == "subsystem_interface"]
    assert len(steps) == 2
    for item in state.subsystem_interfaces:
        [step] = [s for s in steps if s.provenance.reference == item.interface_id]
        assert step.step_id == "vstep:req:interface:" + item.interface_id
        assert step.responsibility == "UNDETERMINED"
        assert step.confidence == "UNDETERMINED"
        assert step.statement.startswith("Prepare how the interaction you declared")
        assert subs[0].display_name in step.statement and item.description in step.statement
        for phrase in ("intended operating conditions", "observable acceptance criterion",
                       "evidence or review"):
            assert phrase in step.statement and phrase in step.closure_condition
        assert "Closed when" not in step.closure_condition     # no generic closure
        for word in ("verified", "passed", "compatible", "feasible", "safe", "ready"):
            assert word not in step.statement.lower().replace(
                item.description.lower(), "")


def test_no_responsibility_value_threshold_or_procedure_is_invented():
    state, _ = _state_with(["Power over a cable."])
    [step] = [s for s in derive_validation_plan(state).steps
              if s.provenance.anchor_kind == "subsystem_interface"]
    generated = (step.statement.replace("Power over a cable.", "")
                 + step.closure_condition + step.evidence_category)
    assert not re.search(r"\d", generated)
    for unit in (" V", " A ", "volt", "amp", "torque", "newton", " N ", "mm",
                 "tolerance", "procedure", "test at", "specialist", "laboratory"):
        assert unit not in generated
    assert step.responsibility not in ("SPECIALIST_REQUIRED",
                                       "EMPIRICAL_EVIDENCE_REQUIRED", "OWNER_EXECUTABLE")


def test_evidence_reference_and_quantity_eligibility_do_not_widen(client):
    from engine.requirement_quantity import eligible_anchors
    sid = _integrated(client)
    tok = _form(_page(client, sid))["answer_token"]
    client.post(f"/session/{sid}", data={"response": "It swings on a pin.",
                                         "action": "answered", "answer_token": tok})
    state = _live(sid)
    before = ([r.requirement_id for r, _ in eligible_anchors(state)],
              [r.record_id for r in appmod._evref_eligible_anchors(state)])
    _declare(client, sid)
    state = _live(sid)
    assert ([r.requirement_id for r, _ in eligible_anchors(state)],
            [r.record_id for r in appmod._evref_eligible_anchors(state)]) == before


# ==========================================================================
# 18.7 Web / authorization / request integrity
# ==========================================================================
def test_the_owner_declares_through_the_normal_journey(client):
    sid = _integrated(client)
    raw = _page(client, sid)
    assert raw.index('id="integrated-scope"') < raw.index('id="declare-interface"')
    assert _declare(client, sid, "  " + DESC + "  ").status_code == 302
    [row] = _ifc_rows(sid)
    assert row[5] == DESC and row[6] == OWNER_STATED and row[7] == UNVALIDATED
    assert _entry(sid).get("_interaction_ack") == appmod.S15_INTERFACE_DECLARED_ACK
    assert DESC in _page(client, sid)


def test_a_non_owner_can_neither_see_nor_declare():
    from tests.test_commercial_evidence_capture import _client_for
    owner, _aid = _client_for("ifc-owner@example.com")
    sid = _integrated(owner)
    form = _form(_page(owner, sid))
    intruder, _bid = _client_for("ifc-intruder@example.com")
    data = dict(form, interface_description=DESC, interface_confirm="yes")
    r = intruder.post(f"/session/{sid}/declare-interface", data=data)
    assert r.status_code in (302, 403, 404)
    assert _ifc_rows(sid) == []
    body = r.get_data(as_text=True)
    assert DESC not in body and PARTS["mech_part_name"] not in body


def test_a_missing_project_writes_nothing(client):
    r = client.post("/session/does-not-exist/declare-interface",
                    data={"interface_description": DESC, "interface_confirm": "yes"})
    assert r.status_code in (302, 403, 404)
    assert _ifc_rows() == []


def test_an_ordinary_project_is_offered_nothing_and_a_forged_post_fails(client):
    sid = _integrated(client)
    forged = _form(_page(client, sid))
    plain = _created(client.post("/start", data={"idea": ELEC_IDEA, "domain_confirm": ELEC}))
    assert _form(_page(client, plain))["interface_binding"] is None
    data = dict(forged, answer_token=_form(_page(client, plain))["answer_token"])
    assert _declare(client, plain, form=data).status_code == 302
    assert _ifc_rows(plain) == [] and _error(plain) == appmod.S15_INTERFACE_NOT_SAVED_MESSAGE


def test_a_corrupt_composition_fails_closed(client):
    sid = _integrated(client)
    form = _form(_page(client, sid))
    _raw("DELETE FROM project_subsystems WHERE project_id = ? AND subsystem_seq = 1",
         (sid,), fk=False)
    r = _declare(client, sid, form=form)
    assert r.status_code == 302
    assert _raw("SELECT COUNT(*) FROM subsystem_interfaces")[0][0] == 0
    assert client.get(f"/session/{sid}").status_code == 302


def test_csrf_is_enforced(client):
    sid = _integrated(client)
    form = _form(_page(client, sid))
    raw = appmod.app.test_client()                         # no CSRF token injection
    r = raw.post(f"/session/{sid}/declare-interface",
                 data=dict(form, interface_description=DESC, interface_confirm="yes"))
    assert r.status_code in (400, 403)
    assert _ifc_rows(sid) == []


def test_tampered_or_stale_forms_write_nothing(client):
    sid = _integrated(client)
    form = _form(_page(client, sid))
    # tampered binding / submission / missing confirmation. The binding tamper
    # flips the final hex character of the HMAC: always a different, well-formed
    # signature (``[:-2] + "00"`` was a no-op when the genuine one ended in 00).
    binding = form["interface_binding"]
    for over, message in (
            ({"interface_binding": binding[:-1] + ("0" if binding[-1] != "0" else "1")},
             appmod.S15_INTERFACE_NOT_SAVED_MESSAGE),
            ({"interface_submission": "0" * 32 + ".bad"},
             appmod.S15_INTERFACE_NOT_SAVED_MESSAGE),
            ({"interface_confirm": ""}, appmod.S15_INTERFACE_INVALID_MESSAGE),
            ({"interface_description": "   "}, appmod.S15_INTERFACE_INVALID_MESSAGE),
            ({"interface_description": "a\x00b"}, appmod.S15_INTERFACE_INVALID_CHAR_MESSAGE),
            ({"interface_description": "x" * 301}, appmod.S15_INTERFACE_TOO_LONG_MESSAGE)):
        data = dict(form, interface_description=DESC, interface_confirm="yes")
        data.update(over)
        assert client.post(f"/session/{sid}/declare-interface", data=data).status_code == 302
        assert _error(sid) == message, over
    # a form rendered before the answer token rotated is stale
    client.post(f"/session/{sid}", data={"response": "It swings on a pin.",
                                         "action": "answered",
                                         "answer_token": form["answer_token"]})
    assert _declare(client, sid, form=form).status_code == 302
    assert _error(sid) == appmod.S15_INTERFACE_STALE_MESSAGE
    assert _ifc_rows(sid) == []


def test_exact_retry_and_double_submit_write_once(client):
    sid = _integrated(client)
    form = _form(_page(client, sid))
    for _ in range(3):
        assert _declare(client, sid, form=form).status_code == 302
        assert _entry(sid).get("_interaction_ack") == appmod.S15_INTERFACE_DECLARED_ACK
    assert len(_ifc_rows(sid)) == 1
    assert len(_live(sid).subsystem_interfaces) == 1
    # a fresh form carries a fresh submission identity: a new declaration
    assert _declare(client, sid, "Another interaction.").status_code == 302
    assert len(_ifc_rows(sid)) == 2


def test_conflicting_retry_material_is_refused(client):
    sid = _integrated(client)
    form = _form(_page(client, sid))
    _declare(client, sid, form=form)
    assert _declare(client, sid, "Different text.", form=form).status_code == 302
    assert _error(sid) == appmod.S15_INTERFACE_NOT_SAVED_MESSAGE
    [row] = _ifc_rows(sid)
    assert row[5] == DESC


def test_a_storage_failure_is_truthful_and_leaks_nothing(client):
    sid = _integrated(client)
    form = _form(_page(client, sid))
    store = _store()
    real = store._conn
    store._conn = _FailOn(real, prefix="INSERT INTO subsystem_interfaces")
    try:
        _declare(client, sid, form=form)
    finally:
        store._conn = real
    assert _error(sid) == appmod.S15_INTERFACE_NOT_SAVED_MESSAGE
    assert _ifc_rows(sid) == []
    for message in (appmod.S15_INTERFACE_NOT_SAVED_MESSAGE,
                    appmod.S15_INTERFACE_UNKNOWN_MESSAGE,
                    appmod.S15_INTERFACE_STALE_MESSAGE):
        for secret in (sid, DESC, PARTS["mech_part_name"], "sub-", "ifc-"):
            assert secret not in message


def test_every_render_reattaches_the_durable_interfaces(client, monkeypatch):
    """The session page, the report and the PDF show the DURABLE interfaces of
    the project on every render — never only what the live state happens to
    hold (a declaration committed by another request is shown too)."""
    sid = _integrated(client)
    subs = _live(sid).subsystems
    _store().append_subsystem_interface(sid, _ifc(subs, "Committed elsewhere."), "other")
    assert _live(sid).subsystem_interfaces == []             # not in live memory yet
    assert "Committed elsewhere." in _visible(_ifc_block(_page(client, sid)))
    assert [i.description for i in _live(sid).subsystem_interfaces] == ["Committed elsewhere."]
    _store().append_subsystem_interface(sid, _ifc(subs, "Second elsewhere."), "other-2")
    report = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert "Second elsewhere." in _visible(_ifc_block(report))
    _store().append_subsystem_interface(sid, _ifc(subs, "Third elsewhere."), "other-3")
    assert "Third elsewhere." in _visible(_ifc_block(_pdf_source(client, sid, monkeypatch)))


def test_committed_but_unrenderable_state_fails_the_page_closed(client):
    sid = _integrated(client)
    _declare(client, sid)
    assert len(_ifc_rows(sid)) == 1
    _raw("UPDATE subsystem_interfaces SET interface_seq = 3 WHERE project_id = ?", (sid,))
    assert client.get(f"/session/{sid}").status_code == 302
    assert client.get(f"/session/{sid}/deliverable").status_code in (302, 503)


# ==========================================================================
# 18.8 User-facing presentation
# ==========================================================================
_IFC_KEYS = ("UI_S15_IFC_TITLE", "UI_S15_IFC_DESCRIPTION", "UI_S15_IFC_PROVENANCE",
             "UI_S15_IFC_ACTION_LABEL", "UI_S15_IFC_ACTION", "UI_S15_IFC_NOT_ESTABLISHED")


def _pdf_source(c, sid, monkeypatch):
    seen = {}
    real = appmod._render_pdf_bytes
    monkeypatch.setattr(appmod, "_render_pdf_bytes",
                        lambda source: seen.setdefault("s", source) and real(source))
    r = c.post(f"/session/{sid}/deliverable.pdf", data={})
    assert r.status_code == 200 and r.data[:5] == b"%PDF-"
    return seen["s"]


def test_session_report_and_pdf_carry_the_same_truth_in_english(client, monkeypatch):
    sid = _integrated(client)
    _declare(client, sid)
    for raw in (_page(client, sid),
                client.get(f"/session/{sid}/deliverable").get_data(as_text=True),
                _pdf_source(client, sid, monkeypatch)):
        block = _visible(_ifc_block(raw))
        for key in _IFC_KEYS:
            assert ui_text.text(key, "en") in block, key
        assert PARTS["mech_part_name"] in block and PARTS["elec_part_name"] in block
        assert DESC in block
    report = _html.unescape(client.get(f"/session/{sid}/deliverable").get_data(as_text=True))
    assert "Prepare how the interaction you declared between" in report   # Section 14
    assert "You declared an interaction between" in report                # Section 13


def test_arabic_surfaces_render_the_interface_truth(client, monkeypatch):
    sid = _integrated(client, focus=ELEC)
    arabic = "لوحة التحكم تغذي المحرك بالطاقة."
    _declare(client, sid, arabic)
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    for raw in (_page(client, sid),
                client.get(f"/session/{sid}/deliverable").get_data(as_text=True),
                _pdf_source(client, sid, monkeypatch)):
        block = _visible(_ifc_block(raw))
        for key in _IFC_KEYS:
            assert ui_text.text(key, "ar") in block, key
        assert ui_text.text("UI_S15_IFC_NOT_ESTABLISHED", "en") not in block
        assert arabic in block                                   # verbatim
    page = _page(client, sid)
    assert ui_text.text("UI_S15_IFC_FORM_SUMMARY", "ar") in _html.unescape(page)
    assert "خطة التحقق (Validation Plan)" in ui_text.text("UI_S15_IFC_INTRO", "ar")


def test_arabic_acknowledgement_and_errors_are_localized():
    assert ui_text.localize_deep(appmod.S15_INTERFACE_DECLARED_ACK, "ar") \
        != appmod.S15_INTERFACE_DECLARED_ACK
    for message in (appmod.S15_INTERFACE_NOT_SAVED_MESSAGE,
                    appmod.S15_INTERFACE_INVALID_MESSAGE,
                    appmod.S15_INTERFACE_TOO_LONG_MESSAGE,
                    appmod.S15_INTERFACE_INVALID_CHAR_MESSAGE,
                    appmod.S15_INTERFACE_STALE_MESSAGE,
                    appmod.S15_INTERFACE_UNKNOWN_MESSAGE):
        assert ui_text.localize_message(message, "en") == message
        assert ui_text.localize_message(message, "ar") != message


def test_owner_text_is_escaped_and_no_internal_identifier_is_shown(client):
    sid = _integrated(client)
    hostile = '<img src=x onerror="alert(1)"> motor & arm'
    _declare(client, sid, hostile)
    iid = _live(sid).subsystem_interfaces[0].interface_id
    for path in (f"/session/{sid}", f"/session/{sid}/deliverable"):
        raw = client.get(path).get_data(as_text=True)
        assert '<img src=x' not in raw
        visible = _visible(_ifc_block(raw))
        assert hostile in visible
        for ident in [iid, "ifc-", "sub-", "OWNER_STATED", "UNVALIDATED"] + [
                s.subsystem_id for s in _live(sid).subsystems]:
            assert ident not in visible


def test_ordinary_projects_render_no_interface_block(client, monkeypatch):
    sid = _created(client.post("/start", data={"idea": ELEC_IDEA, "domain_confirm": ELEC}))
    for raw in (_page(client, sid),
                client.get(f"/session/{sid}/deliverable").get_data(as_text=True),
                _pdf_source(client, sid, monkeypatch)):
        assert _ifc_block(raw) is None and "declare-interface" not in raw


def test_an_integrated_project_without_interfaces_says_so(client):
    sid = _integrated(client)
    block = _visible(_ifc_block(_page(client, sid)))
    assert ui_text.text("UI_S15_IFC_NONE", "en") in block


def test_ui_copy_stays_plain_language():
    for key in [k for k in ui_text.UI_STRINGS if k.startswith("UI_S15_IFC_")]:
        for lang in ("en", "ar"):
            for word in ("Domain Pack", "D4", "IRL", "subsystem", "Mechatronics",
                         "NASA", "compatible with", "verified"):
                assert word not in ui_text.UI_STRINGS[key][lang], (key, word)


# ==========================================================================
# 18.9 Non-interference
# ==========================================================================
def test_classifier_activation_and_multi_domain_semantics_are_unchanged():
    assert domain_activation._ACTIVATED_DOMAINS == frozenset({ELEC, MECH})
    assert classify_domain(TIE_IDEA).kind is DomainResultKind.AMBIGUOUS_TIE
    for idea in (TIE_IDEA, ELEC_IDEA, "A hinge mounted bracket with a lever"):
        assert classify_domain(idea).kind is not DomainResultKind.MULTI_DOMAIN_NEEDS_D4


def test_focus_is_immutable_and_no_focus_route_exists(client):
    sid = _integrated(client, focus=ELEC)
    _declare(client, sid)
    assert _live(sid).domain == ELEC
    assert _store().load_reconstruction_inputs(sid)["confirmed_domain"] == ELEC
    rules = [str(r) for r in appmod.app.url_map.iter_rules()]
    assert not any("focus" in r for r in rules)
    # Stage 15 Slice 3 adds exactly ONE more interface path (its GET page and
    # POST save) and Stage 15 Slice 4 exactly one observation POST; still no
    # focus route.
    assert sorted({r for r in rules if "interface" in r}) == [
        "/session/<sid>/declare-interface", "/session/<sid>/interface-observation",
        "/session/<sid>/interface-preparation"]


def test_the_extracted_submission_identity_is_mechanically_identical_for_cap08():
    import hashlib
    import hmac
    sid, nonce = "proj-1", "0123456789abcdef0123456789abcdef"
    legacy = hmac.new(appmod._answer_secret(),
                      appmod._canonical_message("cap08-submission-v1", sid, nonce),
                      hashlib.sha256).hexdigest()
    assert appmod._cap08_submission_sig(sid, nonce) == legacy
    assert appmod._verified_cap08_submission(sid, nonce + "." + legacy) == nonce
    entry = {}
    issued = appmod._cap08_submission_for(sid, entry)
    assert entry == {appmod._CAP08_SUBMISSION_ENTRY_KEY: issued}
    assert appmod._cap08_submission_for(sid, entry) == issued       # retained
    assert appmod._verified_cap08_submission(sid, issued) == issued.split(".")[0]
    # the domains are separated: one action's identity never authorizes another
    ifc = appmod._submission_identity_for(sid, {}, appmod._S15_IFC_SUBMISSION_DOMAIN,
                                          appmod._S15_IFC_SUBMISSION_ENTRY_KEY)
    assert appmod._verified_cap08_submission(sid, ifc) is None
    assert appmod._verified_submission_identity(
        sid, issued, appmod._S15_IFC_SUBMISSION_DOMAIN) is None
    assert appmod._verified_cap08_submission("proj-2", issued) is None


def test_no_generic_relation_engine_graph_or_ledger_authority_is_introduced():
    src = open(os.path.join(_ROOT, "engine", "idea_state.py"), encoding="utf-8").read()
    assert "interface" not in src.split("RELATIONSHIP_METADATA_DISPOSITIONS = frozenset")[1][:200]
    for mod in ("subsystem_model", "requirement_landscape", "validation_plan"):
        text = open(os.path.join(_ROOT, "engine", mod + ".py"), encoding="utf-8").read()
        for word in ("networkx", "class Graph", "class Edge", "def traverse",
                     "propagat", "AssertionRecord("):
            assert word not in text, (mod, word)


def test_structured_export_decision_and_fdc_owners_are_unchanged(client):
    from engine import read_export_service
    for path in (os.path.join("engine", "read_export_service.py"),
                 os.path.join("web", "api_v1.py"),
                 os.path.join("engine", "export_adapter.py"),
                 os.path.join("engine", "decision_workspace.py"),
                 os.path.join("engine", "decision_composition.py"),
                 os.path.join("engine", "derived_readiness.py")):
        text = open(os.path.join(_ROOT, path), encoding="utf-8").read()
        assert "interface_id" not in text and "subsystem_interfaces" not in text, path
    sid = _integrated(client)
    _declare(client, sid)
    from engine.record_store import SqliteRecordStore as _S  # noqa: F401
    assert callable(read_export_service.produce_project_export)


def test_no_provider_network_or_source_material_is_introduced():
    for path in (os.path.join("engine", "subsystem_model.py"),
                 os.path.join("engine", "requirement_landscape.py"),
                 os.path.join("engine", "validation_plan.py")):
        text = open(os.path.join(_ROOT, path), encoding="utf-8").read()
        for word in ("openai", "requests", "urllib", "http://", "https://", "NASA"):
            assert word not in text, (path, word)


# ==========================================================================
# PR #720 bounded repair — F1 (completed project after restart), F2 (direct
# committed retry after restart), F3 (UNKNOWN stays UNKNOWN)
# ==========================================================================
def _restart():
    """Process / session memory loss + a SAME-database reopen: drop every live
    session and the application store handle; the next request constructs a
    fresh store on the same file."""
    appmod.SESSION_STORE.clear()
    store = appmod._STORE
    if store is not None:
        store.close()
    appmod._STORE = None


def _progression(sid):
    recon = SR.reconstruct_readonly_state(_store(), sid)
    return (recon.review.maturity_level, recon.review.current_stage,
            sorted((g.gap_type, g.status) for g in recon.state.gaps),
            recon.review.open_gaps, len(recon.review.accepted_answer_evidence),
            recon.review.next_question)


def _no_writable_session(sid):
    entry = appmod.SESSION_STORE.get(sid)
    return entry is None or getattr(entry["state"], "domain", None) is None


def _completed_integrated(c):
    """A LEGITIMATELY completed integrated project through the real routes (the
    existing accepted-risk journey helpers): maturity 2, no open gap."""
    from engine.progression_loop import select_next_gap
    from engine.idea_state import (MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY,
                                   BOUNDARY_AMBIGUITY)
    from tests.test_wave1_rvr1_accepted_risk import (
        _answer_until, _token as _ramp_token, _ATTEMPT)
    strong = {
        "PROBLEM_MECHANISM_FIT": (
            "My invention addresses the problem of a folding ramp that can collapse "
            "under a wheelchair. The toggle latch holds the ramp flat because it "
            "snaps over its center point and resists folding under load. Without "
            "this mechanism the ramp could fold while in use. However, this "
            "mechanism does not address a ramp that is installed on uneven ground "
            "— that is a limitation of the approach."),
        "ASSUMPTION_INVENTORY": (
            "I assume the toggle latch stays engaged under repeated wheelchair "
            "loading. This assumption is unvalidated and load-bearing — if wrong, "
            "the ramp could fold during use. I also assume the hinge paint will not "
            "wear, but if wrong I would just repaint it. The first assumption is "
            "essential; the second is peripheral."),
        "EXPERTISE_GAP_AWARENESS": (
            "The implementation demands expertise in structural load analysis, "
            "specifically hinge and latch fatigue, and in accessibility standards "
            "for ramps. I lack sufficient knowledge of fatigue analysis — I would "
            "need to bring in a structural engineer. Without that expertise, the "
            "latch sizing would be wrong and the ramp could fail."),
    }
    sid = _integrated(c)
    state = _live(sid)
    _answer_until(c, appmod, sid, MECHANISM_COMPLETENESS)

    def _accept(gap):
        c.post("/session/%s/accept-risk" % sid, data={
            "gap_type": gap, "risk_confirm": "yes",
            "answer_token": _ramp_token(c, sid)})

    for gap in (PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY):
        c.post("/session/%s" % sid, data={
            "response": _ATTEMPT[gap], "answer_token": _ramp_token(c, sid),
            "action": "answered"})
        _accept(gap)
    for _ in range(6):
        gap = select_next_gap(state)
        if gap is None:
            break
        c.post("/session/%s" % sid, data={
            "response": strong[gap], "answer_token": _ramp_token(c, sid),
            "action": "answered"})
        if state.get_gap(gap).status in ("OPEN", "PARTIAL"):
            _accept(gap)
    assert state.maturity_level >= 2 and not state.get_open_gaps(), "not completed"
    return sid


def test_f1_completed_integrated_project_declares_after_restart_without_reopening(client):
    sid = _completed_integrated(client)
    assert _declare(client, sid, "Declared while live.").status_code == 302
    [first] = [i.interface_id for i in _live(sid).subsystem_interfaces]
    _restart()
    before = _progression(sid)
    assert before[0] >= 2 and before[3] == ()                 # completed, no open gap
    # the completed-project Resume prohibition is preserved
    client.post(f"/session/{sid}/resume", data={})
    assert _no_writable_session(sid)
    page = _page(client, sid)
    assert "Declared while live." in _visible(_ifc_block(page))   # still visible
    form = _form(page)
    assert form["interface_binding"] and form["interface_submission"]
    minted = []
    real_new = sm.new_interface_id
    try:
        sm.new_interface_id = lambda: minted.append(1) or real_new()
        r = _declare(client, sid, "Declared after restart.", form=form)
    finally:
        sm.new_interface_id = real_new
    assert r.status_code == 302 and minted == [1]
    assert _entry(sid).get("_interaction_ack") == appmod.S15_INTERFACE_DECLARED_ACK
    assert [row[5] for row in _ifc_rows(sid)] == [
        "Declared while live.", "Declared after restart."]
    assert _ifc_rows(sid)[0][2] == first
    # no writable question session, no progression change, same focus
    assert _no_writable_session(sid)
    assert getattr(_live(sid), "domain", None) is None
    assert _progression(sid) == before
    assert "Declared after restart." in _visible(_ifc_block(_page(client, sid)))
    _restart()
    assert _progression(sid) == before
    assert [i.description for i in _store().load_subsystem_interfaces(sid)] == [
        "Declared while live.", "Declared after restart."]
    client.post(f"/session/{sid}/resume", data={})
    assert _no_writable_session(sid)                          # still never reopens


def test_f1_cold_action_keeps_the_cap_and_ordinary_projects_unchanged(client):
    sid = _integrated(client)
    subs = _live(sid).subsystems
    for n in range(sm.MAX_SUBSYSTEM_INTERFACES_PER_PROJECT - 1):
        _store().append_subsystem_interface(sid, _ifc(subs, "Interaction %d." % n), "k%d" % n)
    _restart()
    form = _form(_page(client, sid))                          # one slot left
    assert form["interface_binding"]
    assert _declare(client, sid, "The last one.", form=form).status_code == 302
    assert len(_ifc_rows(sid)) == sm.MAX_SUBSYSTEM_INTERFACES_PER_PROJECT
    _restart()
    page = _page(client, sid)
    assert _form(page)["interface_binding"] is None           # cap reached: no form
    assert _declare(client, sid, "One too many.", form=form).status_code == 302
    assert len(_ifc_rows(sid)) == sm.MAX_SUBSYSTEM_INTERFACES_PER_PROJECT
    # an ordinary single-domain project is offered nothing cold either
    plain = _created(client.post("/start", data={"idea": ELEC_IDEA,
                                                 "domain_confirm": ELEC}))
    _restart()
    assert _form(_page(client, plain))["interface_binding"] is None
    assert _ifc_rows(plain) == []


def test_f2_exact_committed_retry_resolves_directly_after_restart(client):
    sid = _integrated(client)
    form = _form(_page(client, sid))
    assert _declare(client, sid, form=form).status_code == 302
    [row] = _ifc_rows(sid)
    _restart()                                                # no intervening GET
    minted = []
    real_new = sm.new_interface_id
    try:
        sm.new_interface_id = lambda: minted.append(1) or real_new()
        r = _declare(client, sid, form=form)
    finally:
        sm.new_interface_id = real_new
    assert r.status_code == 302 and r.headers["Location"].endswith(f"/session/{sid}")
    assert minted == []                                       # no new identity
    assert _ifc_rows(sid) == [row]                            # no new row
    assert _entry(sid).get("_interaction_ack") == appmod.S15_INTERFACE_DECLARED_ACK
    assert [i.interface_id for i in _live(sid).subsystem_interfaces] == [row[2]]
    assert _no_writable_session(sid)
    # changed material under the same identity, directly after another restart
    _restart()
    assert _declare(client, sid, "Different text.", form=form).status_code == 302
    assert _error(sid) == appmod.S15_INTERFACE_NOT_SAVED_MESSAGE
    assert _ifc_rows(sid) == [row]


def test_f2_forged_cross_project_and_uncommitted_retries_stay_refused(client):
    sid = _integrated(client)
    other = _integrated(client)
    form = _form(_page(client, sid))
    other_form = _form(_page(client, other))
    _declare(client, sid, form=form)
    fresh = _form(_page(client, sid))                         # issued, never submitted
    _restart()
    tampered = dict(form, interface_submission=form["interface_submission"][:-1] + (
        "0" if form["interface_submission"][-1] != "0" else "1"))
    assert _declare(client, sid, form=tampered).status_code == 302
    assert _error(sid) == appmod.S15_INTERFACE_NOT_SAVED_MESSAGE
    # project A's signed action replayed against project B
    assert _declare(client, other, form=form).status_code == 302
    assert _error(other) == appmod.S15_INTERFACE_NOT_SAVED_MESSAGE
    assert _ifc_rows(other) == []
    # B's own form bound to A's parts cannot exist; B's identity on A fails too
    assert _declare(client, sid, form=other_form).status_code == 302
    assert _error(sid) == appmod.S15_INTERFACE_NOT_SAVED_MESSAGE
    # a never-committed action after restart is not current: nothing saved
    _restart()
    assert _declare(client, sid, "Never committed.", form=fresh).status_code == 302
    assert _error(sid) == appmod.S15_INTERFACE_STALE_MESSAGE
    assert len(_ifc_rows(sid)) == 1
    # malformed / missing pieces
    for broken in (dict(form, interface_binding="x.y"), dict(form, answer_token=""),
                   dict(form, interface_submission="")):
        _restart()
        assert _declare(client, sid, form=broken).status_code == 302
        assert _error(sid) == appmod.S15_INTERFACE_NOT_SAVED_MESSAGE
    assert len(_ifc_rows(sid)) == 1


def _unknown_attempt(c, sid, form, lang=None):
    store = _store()
    real = store._conn
    store._conn = _CommitAndRollbackFail(real)
    try:
        r = _declare(c, sid, form=form)
    finally:
        store._conn = real
    assert store._connection_unsafe is True and real.in_transaction
    return store, real, r


def _retry_fields(raw):
    fields = {}
    for name in ("answer_token", "interface_binding", "interface_submission",
                 "interface_description", "interface_confirm"):
        m = re.search(r'name="%s" value="([^"]*)"' % name, raw)
        fields[name] = _html.unescape(m.group(1)) if m else None
    return fields


def test_f3_unknown_is_visible_and_never_saved_or_not_saved(client):
    sid = _integrated(client)
    form = _form(_page(client, sid))
    store, real, r = _unknown_attempt(client, sid, form)
    try:
        body = _html.unescape(r.get_data(as_text=True))
        assert r.status_code == 503 and r.headers["Cache-Control"] == "no-store"
        assert appmod.S15_INTERFACE_UNKNOWN_MESSAGE in body          # visible truth
        assert appmod.S15_INTERFACE_DECLARED_ACK not in body          # no false SAVED
        assert appmod.S15_INTERFACE_NOT_SAVED_MESSAGE not in body     # no false NOT SAVED
        assert DESC not in _visible(r.get_data(as_text=True))         # no project state
        assert _entry(sid).get("_interaction_ack") is None and _error(sid) is None
        assert _live(sid).subsystem_interfaces == []                  # never durable truth
        assert _raw("SELECT COUNT(*) FROM subsystem_interfaces")[0][0] == 0
        # the SAME signed action is offered again, unconsumed
        retry = _retry_fields(r.get_data(as_text=True))
        assert retry == dict(form, interface_description=DESC, interface_confirm="yes")
        assert _entry(sid).get(appmod._S15_IFC_SUBMISSION_ENTRY_KEY) == form["interface_submission"]
        # repeated while still unknowable: UNKNOWN again, never NOT SAVED
        again = client.post(f"/session/{sid}/declare-interface", data=retry)
        assert again.status_code == 503
        assert appmod.S15_INTERFACE_UNKNOWN_MESSAGE in _html.unescape(again.get_data(as_text=True))
        assert _error(sid) is None
        # ... also after the runtime entry is lost while the store stays unsafe
        appmod.SESSION_STORE.clear()
        lost = client.post(f"/session/{sid}/declare-interface", data=retry)
        assert lost.status_code == 503
        assert appmod.S15_INTERFACE_UNKNOWN_MESSAGE in _html.unescape(lost.get_data(as_text=True))
        # ... and a forged action is never dressed up as UNKNOWN
        forged = client.post(f"/session/{sid}/declare-interface",
                             data=dict(retry, interface_binding="x.y"))
        assert forged.status_code == 302
    finally:
        real.close()                                           # uncommitted row discarded
        appmod._STORE = None
    # later, a healthy store reports the ACTUAL outcome: it never committed
    appmod.SESSION_STORE.clear()
    resolved = client.post(f"/session/{sid}/declare-interface", data=retry)
    assert resolved.status_code == 302
    assert _error(sid) == appmod.S15_INTERFACE_STALE_MESSAGE      # nothing was saved
    assert _ifc_rows(sid) == [] and _live(sid).subsystem_interfaces == []


def test_f3_unknown_resolves_to_the_committed_declaration_once_readable(client, monkeypatch):
    sid = _integrated(client)
    form = _form(_page(client, sid))
    store = _store()
    real = store._conn
    store._conn = _FailOn(real, commit_then=True)             # commits, then raises
    real_lookup = rs.SqliteRecordStore.committed_subsystem_interface_for_submission
    calls = []

    def lookup(self, pid, key):
        calls.append(key)
        if len(calls) == 1:                    # the pre-write check reads fine
            return real_lookup(self, pid, key)
        raise RecordStoreConnectionUnsafe("injected: committed state unreadable")

    monkeypatch.setattr(
        rs.SqliteRecordStore, "committed_subsystem_interface_for_submission", lookup)
    try:
        r = _declare(client, sid, form=form)
    finally:
        store._conn = real
    assert r.status_code == 503 and len(calls) == 2
    assert appmod.S15_INTERFACE_UNKNOWN_MESSAGE in _html.unescape(r.get_data(as_text=True))
    assert _live(sid).subsystem_interfaces == []                  # not published
    [row] = _ifc_rows(sid)                                        # it DID commit
    monkeypatch.setattr(rs.SqliteRecordStore,
                        "committed_subsystem_interface_for_submission", real_lookup)
    _restart()
    retry = _retry_fields(r.get_data(as_text=True))
    resolved = client.post(f"/session/{sid}/declare-interface", data=retry)
    assert resolved.status_code == 302
    assert _entry(sid).get("_interaction_ack") == appmod.S15_INTERFACE_DECLARED_ACK
    assert _ifc_rows(sid) == [row]                                # never twice
    assert [i.interface_id for i in _live(sid).subsystem_interfaces] == [row[2]]


def test_f3_unknown_response_is_localized(client):
    sid = _integrated(client)
    form = _form(_page(client, sid))
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    store, real, r = _unknown_attempt(client, sid, form)
    try:
        body = _html.unescape(r.get_data(as_text=True))
        assert r.status_code == 503 and 'dir="rtl"' in body
        for key in ("UI_S15_IFC_ERR_UNKNOWN", "UI_S15_IFC_UNKNOWN_TITLE",
                    "UI_S15_IFC_UNKNOWN_RETRY", "UI_S15_IFC_UNKNOWN_BACK"):
            assert ui_text.text(key, "ar") in body
            assert ui_text.text(key, "en") != ui_text.text(key, "ar")
        assert ui_text.localize_message(appmod.S15_INTERFACE_UNKNOWN_MESSAGE, "ar") == \
            ui_text.text("UI_S15_IFC_ERR_UNKNOWN", "ar")
    finally:
        real.close()
        appmod._STORE = None
        client.post("/ui-language", data={"lang": "en"})


class _CommitThenInterfaceReadsFail:
    """The COMMIT really happens and then raises (acknowledgement lost); from
    then on every durable SELECT touching ``subsystem_interfaces`` fails while
    the connection itself stays transaction-safe (no unresolved transaction,
    no IR-01 flag) — a required committed read that cannot complete."""

    def __init__(self, conn):
        self._conn = conn
        self.committed = False

    def execute(self, sql, *args):
        if sql == "COMMIT" and not self.committed:
            self._conn.execute(sql, *args)
            self.committed = True
            raise sqlite3.OperationalError("injected: acknowledgement lost")
        if self.committed and "subsystem_interfaces" in sql:
            raise sqlite3.OperationalError("injected: interface read failing")
        return self._conn.execute(sql, *args)

    def __getattr__(self, name):
        return getattr(self._conn, name)


def test_f3_residual_unknown_survives_session_loss_while_the_required_read_fails(client):
    sid = _integrated(client)
    form = _form(_page(client, sid))
    store = _store()
    real = store._conn
    store._conn = _CommitThenInterfaceReadsFail(real)
    minted = []
    real_new = sm.new_interface_id
    try:
        r = _declare(client, sid, form=form)                  # committed, unconfirmable
        assert r.status_code == 503
        assert store._connection_unsafe is False and not real.in_transaction
        assert store.committed_state_readable() is True        # transaction-safe ...
        [row] = _ifc_rows(sid)                                 # ... and it DID commit
        retry = _retry_fields(r.get_data(as_text=True))
        # retry with the runtime entry present: UNKNOWN
        again = client.post(f"/session/{sid}/declare-interface", data=retry)
        assert again.status_code == 503
        # the runtime entry is lost; the SAME signed retry, read still failing
        appmod.SESSION_STORE.clear()
        sm.new_interface_id = lambda: minted.append(1) or real_new()
        lost = client.post(f"/session/{sid}/declare-interface", data=retry)
        body = _html.unescape(lost.get_data(as_text=True))
        assert lost.status_code == 503                         # never a redirect to /
        assert "Location" not in lost.headers
        assert appmod.S15_INTERFACE_UNKNOWN_MESSAGE in body
        assert appmod.S15_INTERFACE_DECLARED_ACK not in body   # not SAVED
        assert appmod.S15_INTERFACE_NOT_SAVED_MESSAGE not in body  # not NOT SAVED
        assert sid not in appmod.SESSION_STORE                 # nothing half-built
    finally:
        store._conn = real                                     # durable reads restored
    try:
        resolved = client.post(f"/session/{sid}/declare-interface", data=retry)
    finally:
        sm.new_interface_id = real_new
    assert resolved.status_code == 302
    assert resolved.headers["Location"].endswith(f"/session/{sid}")
    assert _entry(sid).get("_interaction_ack") == appmod.S15_INTERFACE_DECLARED_ACK
    assert [i.interface_id for i in _live(sid).subsystem_interfaces] == [row[2]]
    assert _ifc_rows(sid) == [row] and minted == []            # stored id; no new row
    # control: durable history READ and found corrupt still fails closed —
    # never UNKNOWN — with no runtime entry
    _raw("UPDATE subsystem_interfaces SET interface_seq = 3 WHERE project_id = ?", (sid,))
    appmod.SESSION_STORE.clear()
    corrupt = client.post(f"/session/{sid}/declare-interface", data=retry)
    assert corrupt.status_code == 302 and corrupt.headers["Location"].endswith("/")
