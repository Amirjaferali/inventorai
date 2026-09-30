"""Stage 15 Slice 3 — Interface Verification Preparation Metadata.

For each CURRENT durable Owner-declared interface (Stage 15 Slice 2) the
inventor durably records, edits and clears, in their own words, the three
verification-preparation inputs that interface's Validation Plan step already
asks for: the intended operating conditions, an observable acceptance
criterion and the evidence or review needed.

  * semantic owner ``engine/subsystem_model.py``; the existing immutable
    ``interface_id`` is the ONLY identity; the append-only declaration is
    unchanged;
  * ONE additive CURRENT-VALUE sidecar ``subsystem_interface_preparations``
    keyed by ``(project_id, interface_id)`` with a composite foreign key to
    that exact durable interface; partial values; clear-all deletes the row;
  * ONE atomic write that re-validates the identities inside the transaction;
    confirm-by-reload SAVED / NOT SAVED / UNKNOWN (IR-01 preserved);
  * the Validation Plan step states truthfully what is recorded; all three
    present means only "recorded" — never verified, compatible or ready.
"""
import html as _html
import os
import re
import sqlite3

import pytest

import web.app as appmod
from engine import session_reconstruction as SR
from engine import subsystem_model as sm
from engine.idea_state import IdeaState
from engine.readiness_snapshot import readiness_snapshot
from engine.record_store import (
    InterfacePreparationRejected, InterfacePreparationsCorrupt,
    RecordStoreConnectionUnsafe, SqliteRecordStore)
from engine.requirement_landscape import derive_requirement_landscape
from engine.validation_plan import derive_validation_plan
from tests.csrf_client import csrf_client
from tests.test_stage15_integrated_invention_entry import (
    ELEC, MECH, PARTS, TIE_IDEA, _CommitAndRollbackFail, _compose, _contract,
    _created, _live, _pair, _ri, _visible)
from tests.test_stage15_subsystem_interface_declaration import (
    DESC, _FailOn, _declare, _ifc, _ifc_block, _new_project, _page, _raw)
from web import ui_text

COND = "Indoors, 10 to 40 °C, lid cycled up to 50 times a day."
ACCEPT = "The arm reaches fully open within 2 seconds, every time."
EVID = "A bench test log, reviewed by an electrical engineer."
F_C, F_A, F_E = sm.PREPARATION_FIELDS


@pytest.fixture
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


def _store():
    return appmod._get_store()


def _db_path():
    return os.environ["INVENTORAI_DB_PATH"]


def _prep_rows(pid):
    _store()
    return _raw("SELECT interface_id, operating_conditions, acceptance_criterion, "
                "evidence_needed FROM subsystem_interface_preparations "
                "WHERE project_id = ? ORDER BY interface_id", (pid,))


def _project_with_interfaces(store, n=1, description=DESC):
    pid, subs = _new_project(store)
    items = []
    for k in range(n):
        item = _ifc(subs, description)
        store.append_subsystem_interface(pid, item, "key-%d" % k)
        items.append(item)
    return pid, subs, items


def _integrated_with_interface(c, focus=MECH, description=DESC):
    sid = _created(_compose(c, TIE_IDEA, focus=focus))
    assert _declare(c, sid, description).status_code == 302
    [ifc] = _store().load_subsystem_interfaces(sid)
    return sid, ifc


def _field(field_name, interface_id):
    return appmod._S15_PREP_FIELD_PREFIXES[field_name] + interface_id


def _save(c, sid, values):
    """POST the preparation page as a user who just opened it and typed
    ``values`` ((field, interface_id) -> text): each submitted field carries
    the baseline that fresh page displayed (F724-1). A field the page does not
    offer (an unknown interface) has no baseline."""
    raw = c.get(f"/session/{sid}/interface-preparation").get_data(as_text=True)
    shown = {n: _html.unescape(v) for n, v in re.findall(
        r'<input type="hidden" name="(prep_base_[^"]+)" value="([^"]*)"', raw)}
    data = {}
    for (f, i), text in values.items():
        data[_field(f, i)] = text
        base = appmod._S15_PREP_BASE_PREFIXES[f] + i
        if base in shown:
            data[base] = shown[base]
    return c.post(f"/session/{sid}/interface-preparation", data=data)


def _text(resp):
    return _html.unescape(resp.get_data(as_text=True))


def _interface_step(state):
    [step] = [s for s in derive_validation_plan(state).steps
              if s.provenance.anchor_kind == "subsystem_interface"]
    return step


def _state_with_preparation(preparation_values=None, attached=True):
    subs = _pair()
    state = IdeaState(idea_id="prep")
    state.domain = MECH
    state.subsystems = list(subs)
    item = _ifc(subs)
    state.subsystem_interfaces = [item]
    if attached:
        prep = None if preparation_values is None else sm.InterfacePreparation(
            item.interface_id, **preparation_values)
        state.subsystem_interface_preparations = [] if prep is None else [prep]
    return state, item


# ==========================================================================
# 1. Semantic owner
# ==========================================================================
def test_merged_preparation_supports_partial_edit_clear_and_clear_all():
    iid = sm.new_interface_id()
    one = sm.merged_preparation(iid, None, {F_C: COND})
    assert one == sm.InterfacePreparation(iid, operating_conditions=COND)
    assert sm.preparation_presence(one) == sm.PREPARATION_PARTLY_RECORDED
    two = sm.merged_preparation(iid, one, {F_A: ACCEPT})
    assert (two.operating_conditions, two.acceptance_criterion, two.evidence_needed) \
        == (COND, ACCEPT, None)                     # untouched field kept
    three = sm.merged_preparation(iid, two, {F_E: EVID})
    assert sm.preparation_presence(three) == sm.PREPARATION_ALL_RECORDED
    edited = sm.merged_preparation(iid, three, {F_C: "Outdoors."})
    assert edited.operating_conditions == "Outdoors." and edited.evidence_needed == EVID
    cleared = sm.merged_preparation(iid, edited, {F_A: None})
    assert cleared.acceptance_criterion is None and cleared.recorded_fields() == (F_C, F_E)
    assert sm.merged_preparation(iid, cleared, {F_C: None, F_E: None}) is None
    assert sm.preparation_presence(None) == sm.PREPARATION_NONE_RECORDED


@pytest.mark.parametrize("bad", ["", "  padded ", "a\x00b", "x" * 1001, 7])
def test_invalid_preparation_text_is_refused_never_truncated(bad):
    with pytest.raises(sm.InterfaceError):
        sm.merged_preparation(sm.new_interface_id(), None, {F_C: bad})
    assert sm.valid_preparation_text("x" * 1000)
    assert sm.valid_preparation_text("line one\nline two")


def test_unknown_fields_and_orphans_are_invalid_and_never_remapped():
    subs = _pair()
    a, b = _ifc(subs), _ifc(subs)                   # same endpoint pair, same text
    with pytest.raises(sm.InterfaceError):
        sm.merged_preparation(a.interface_id, None, {"result": "PASS"})
    orphan = sm.InterfacePreparation(sm.new_interface_id(), operating_conditions=COND)
    with pytest.raises(sm.InterfaceError):
        sm.validate_interface_preparations([orphan], [a, b])
    dup = sm.InterfacePreparation(a.interface_id, operating_conditions=COND)
    with pytest.raises(sm.InterfaceError):
        sm.validate_interface_preparations([dup, dup], [a, b])
    with pytest.raises(sm.InterfaceError):
        sm.validate_interface_preparations([sm.InterfacePreparation(a.interface_id)], [a, b])
    pb = sm.InterfacePreparation(b.interface_id, evidence_needed=EVID)
    assert sm.validate_interface_preparations([pb], [a, b]) == (pb,)
    assert sm.preparation_for([pb], a.interface_id) is None      # identity only
    assert sm.preparation_for([pb], b.interface_id) == pb


def test_the_append_only_declaration_is_unchanged():
    fields = [f.name for f in sm.SubsystemInterface.__dataclass_fields__.values()]
    assert fields == ["interface_id", "subsystem_a_id", "subsystem_b_id",
                      "description", "provenance", "validation_state"]
    prep_fields = [f.name for f in sm.InterfacePreparation.__dataclass_fields__.values()]
    assert prep_fields == ["interface_id", F_C, F_A, F_E]       # no second identity


# ==========================================================================
# 2. Durable persistence: migration, record / edit / clear, binding
# ==========================================================================
def _columns(conn, table):
    return [row[1] for row in conn.execute("PRAGMA table_info(%s)" % table)]


def test_fresh_migration_creates_one_narrow_current_value_sidecar(tmp_path):
    path = str(tmp_path / "fresh.db")
    SqliteRecordStore(path).close()
    conn = sqlite3.connect(path)
    try:
        assert _columns(conn, "subsystem_interface_preparations") == [
            "project_id", "interface_id", F_C, F_A, F_E]
        fks = conn.execute(
            "PRAGMA foreign_key_list(subsystem_interface_preparations)").fetchall()
        targets = {(row[2], row[3], row[4]) for row in fks}
        assert ("subsystem_interfaces", "project_id", "project_id") in targets
        assert ("subsystem_interfaces", "interface_id", "interface_id") in targets
        # the Slice-2 table is not widened
        assert "operating_conditions" not in _columns(conn, "subsystem_interfaces")
    finally:
        conn.close()


def test_migration_is_additive_and_idempotent_on_a_populated_database(tmp_path):
    path = str(tmp_path / "populated.db")
    store = SqliteRecordStore(path)
    pid, _subs, [item] = _project_with_interfaces(store)
    store.apply_interface_preparation_delta(pid, {item.interface_id: {F_C: COND}})
    before = sqlite3.connect(path).execute(
        "SELECT * FROM subsystem_interfaces").fetchall()
    store.close()
    for _ in range(2):                               # reopen = migrate again
        again = SqliteRecordStore(path)
        assert again.load_interface_preparations(pid) == (
            sm.InterfacePreparation(item.interface_id, operating_conditions=COND),)
        again.close()
    conn = sqlite3.connect(path)
    try:
        assert conn.execute("SELECT * FROM subsystem_interfaces").fetchall() == before
    finally:
        conn.close()


def test_a_database_without_the_sidecar_migrates_with_nothing_backfilled(tmp_path):
    path = str(tmp_path / "old.db")
    store = SqliteRecordStore(path)
    pid, _subs, _items = _project_with_interfaces(store)
    store.close()
    conn = sqlite3.connect(path)
    conn.execute("DROP TABLE subsystem_interface_preparations")   # pre-slice shape
    conn.commit()
    conn.close()
    again = SqliteRecordStore(path)
    assert again.load_interface_preparations(pid) == ()
    again.close()


def test_record_edit_clear_one_and_clear_all():
    store = _store()
    pid, _subs, [item] = _project_with_interfaces(store)
    iid = item.interface_id
    assert store.load_interface_preparations(pid) == ()
    store.apply_interface_preparation_delta(pid, {iid: {F_C: COND}})
    assert _prep_rows(pid) == [(iid, COND, None, None)]          # partial is durable
    store.apply_interface_preparation_delta(pid, {iid: {F_A: ACCEPT, F_E: EVID}})
    assert _prep_rows(pid) == [(iid, COND, ACCEPT, EVID)]
    store.apply_interface_preparation_delta(pid, {iid: {F_C: "Outdoors."}})
    assert _prep_rows(pid) == [(iid, "Outdoors.", ACCEPT, EVID)]
    store.apply_interface_preparation_delta(pid, {iid: {F_A: None}})
    assert _prep_rows(pid) == [(iid, "Outdoors.", None, EVID)]
    store.apply_interface_preparation_delta(pid, {iid: {F_C: None, F_E: None}})
    assert _prep_rows(pid) == []                     # no semantically empty row
    assert store.load_interface_preparations(pid) == ()


def test_wrong_project_and_nonexistent_interfaces_are_refused_atomically():
    store = _store()
    pid, _subs, [mine] = _project_with_interfaces(store)
    other_pid, _other, [theirs] = _project_with_interfaces(store)
    for bad in (theirs.interface_id, sm.new_interface_id(), "ifc-short", ""):
        with pytest.raises(InterfacePreparationRejected):
            store.apply_interface_preparation_delta(
                pid, {mine.interface_id: {F_C: COND}, bad: {F_C: COND}})
    assert _prep_rows(pid) == [] and _prep_rows(other_pid) == []   # nothing partial
    with pytest.raises(Exception):
        store.apply_interface_preparation_delta("no-such-project",
                                                {mine.interface_id: {F_C: COND}})
    # the database backstop: a row can never name another project's interface
    conn = sqlite3.connect(_db_path())
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("INSERT INTO subsystem_interface_preparations "
                         "VALUES (?, ?, ?, NULL, NULL)", (pid, theirs.interface_id, COND))
    finally:
        conn.close()


@pytest.mark.parametrize("delta", [
    None, [], {"x": "y"}, {"ifc": {}}, {"ifc": {"result": "PASS"}},
    {"ifc": {F_C: "  untrimmed "}}, {"ifc": {F_C: "a\x00b"}},
    {"ifc": {F_C: "x" * 1001}}])
def test_malformed_deltas_are_refused_before_any_write(delta):
    store = _store()
    pid, _subs, [item] = _project_with_interfaces(store)
    if isinstance(delta, dict) and "ifc" in delta:
        delta = {item.interface_id: delta["ifc"]}
    with pytest.raises(InterfacePreparationRejected):
        store.apply_interface_preparation_delta(pid, delta)
    assert _prep_rows(pid) == []


def test_interfaces_on_the_same_endpoint_pair_never_share_or_swap_preparation():
    store = _store()
    pid, _subs, (first, second) = _project_with_interfaces(store, n=2)
    assert {first.subsystem_a_id, first.subsystem_b_id} == \
        {second.subsystem_a_id, second.subsystem_b_id}
    assert first.description == second.description
    store.apply_interface_preparation_delta(pid, {second.interface_id: {F_A: ACCEPT}})
    loaded = store.load_interface_preparations(pid)
    assert [p.interface_id for p in loaded] == [second.interface_id]
    assert sm.preparation_for(loaded, first.interface_id) is None
    store.apply_interface_preparation_delta(pid, {first.interface_id: {F_E: EVID}})
    loaded = store.load_interface_preparations(pid)
    assert [p.interface_id for p in loaded] == [first.interface_id, second.interface_id]
    assert sm.preparation_for(loaded, first.interface_id).acceptance_criterion is None
    assert sm.preparation_for(loaded, second.interface_id).evidence_needed is None


class _FailNth:
    """The Nth statement starting with ``prefix`` fails (the earlier ones ran)."""

    def __init__(self, conn, prefix, nth):
        self._conn, self.prefix, self.left = conn, prefix, nth

    def execute(self, sql, *args):
        if sql.startswith(self.prefix):
            self.left -= 1
            if self.left == 0:
                raise sqlite3.OperationalError("injected")
        return self._conn.execute(sql, *args)

    def __getattr__(self, name):
        return getattr(self._conn, name)


def test_a_multi_interface_multi_field_delta_is_all_or_nothing():
    store = _store()
    pid, _subs, (first, second) = _project_with_interfaces(store, n=2)
    store.apply_interface_preparation_delta(pid, {first.interface_id: {F_C: COND}})
    before = _prep_rows(pid)
    real = store._conn
    store._conn = _FailNth(real, "INSERT INTO subsystem_interface_preparations", 2)
    try:
        with pytest.raises(sqlite3.OperationalError):
            store.apply_interface_preparation_delta(pid, {
                first.interface_id: {F_C: "changed", F_A: ACCEPT},
                second.interface_id: {F_E: EVID}})
    finally:
        store._conn = real
    assert store._connection_unsafe is False and not real.in_transaction
    assert _prep_rows(pid) == before                 # the first upsert rolled back


def test_corrupt_durable_preparation_fails_closed_for_the_whole_collection():
    store = _store()
    pid, _subs, (first, second) = _project_with_interfaces(store, n=2)
    store.apply_interface_preparation_delta(pid, {first.interface_id: {F_C: COND}})
    cases = [
        ("INSERT INTO subsystem_interface_preparations VALUES (?, ?, ?, NULL, NULL)",
         (pid, "ifc-" + "0" * 32, COND), dict(fk=False)),             # orphan
        ("INSERT INTO subsystem_interface_preparations VALUES (?, ?, NULL, NULL, NULL)",
         (pid, second.interface_id), dict(ignore_checks=True)),        # empty row
        ("UPDATE subsystem_interface_preparations SET operating_conditions = ? "
         "WHERE project_id = ?", ("  padded  ", pid), {}),              # untrimmed
    ]
    for sql, params, opts in cases:
        _raw(sql, params, **opts)
        with pytest.raises(InterfacePreparationsCorrupt):
            store.load_interface_preparations(pid)
        with pytest.raises(InterfacePreparationsCorrupt):
            store.apply_interface_preparation_delta(
                pid, {first.interface_id: {F_E: EVID}})
        probe = IdeaState(idea_id="probe")
        assert appmod._attach_project_subsystems(pid, probe) is False
        _raw("DELETE FROM subsystem_interface_preparations WHERE project_id = ?",
             (pid,), fk=False)
        store.apply_interface_preparation_delta(pid, {first.interface_id: {F_C: COND}})
    # the user text that was stored is never silently discarded by a load
    assert _prep_rows(pid) == [(first.interface_id, COND, None, None)]


def test_unresolved_commit_and_rollback_is_never_read_as_committed():
    store = _store()
    pid, _subs, [item] = _project_with_interfaces(store)
    real = store._conn
    store._conn = _CommitAndRollbackFail(real)
    try:
        with pytest.raises(Exception):
            store.apply_interface_preparation_delta(pid, {item.interface_id: {F_C: COND}})
    finally:
        store._conn = real
    try:
        assert store._connection_unsafe is True and real.in_transaction
        assert real.execute("SELECT COUNT(*) FROM subsystem_interface_preparations"
                            ).fetchone()[0] == 1           # its own uncommitted row
        assert _raw("SELECT COUNT(*) FROM subsystem_interface_preparations")[0][0] == 0
        for call in (lambda: store.load_interface_preparations(pid),
                     lambda: store.load_subsystem_integration(pid),
                     lambda: store.apply_interface_preparation_delta(
                         pid, {item.interface_id: {F_A: ACCEPT}})):
            with pytest.raises(RecordStoreConnectionUnsafe):
                call()
        assert appmod._resolve_interface_preparation_write(
            pid, {item.interface_id: {F_C: COND}}) == appmod._S15_PREP_WRITE_UNKNOWN
    finally:
        real.close()
        appmod._STORE = None
    assert _store().load_interface_preparations(pid) == ()


# ==========================================================================
# 3. Web write path: SAVED / NOT SAVED / UNKNOWN, retry, binding
# ==========================================================================
def test_the_page_offers_each_interface_without_leaking_identifiers(client):
    sid, ifc = _integrated_with_interface(client)
    r = client.get(f"/session/{sid}/interface-preparation")
    assert r.status_code == 200
    visible = _visible(re.sub(r"<style.*?</style>", " ", r.get_data(as_text=True),
                              flags=re.S))
    for key in ("UI_S15_PREP_TITLE", "UI_S15_PREP_CONDITIONS", "UI_S15_PREP_ACCEPTANCE",
                "UI_S15_PREP_EVIDENCE", "UI_S15_PREP_NONE", "UI_S15_IFC_NOT_ESTABLISHED"):
        assert ui_text.text(key, "en") in visible, key
    assert DESC in visible and PARTS["mech_part_name"] in visible
    for leaked in (ifc.interface_id, "ifc-", "sub-", "interface_id",
                   "subsystem_interface_preparations", F_C, F_A, F_E):
        assert leaked not in visible


def test_record_partial_then_all_then_clear_through_the_page(client):
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    r = _save(client, sid, {(F_C, iid): "  " + COND + "  "})
    assert r.status_code == 200
    assert appmod.S15_PREP_SAVED_MESSAGE in _text(r)
    assert _prep_rows(sid) == [(iid, COND, None, None)]          # trimmed only
    assert ui_text.text("UI_S15_PREP_PARTIAL", "en") in _visible(_page(client, sid))
    _save(client, sid, {(F_C, iid): COND, (F_A, iid): ACCEPT, (F_E, iid): EVID})
    assert _prep_rows(sid) == [(iid, COND, ACCEPT, EVID)]
    assert ui_text.text("UI_S15_PREP_ALL", "en") in _visible(_page(client, sid))
    _save(client, sid, {(F_C, iid): COND, (F_A, iid): "", (F_E, iid): EVID})
    assert _prep_rows(sid) == [(iid, COND, None, EVID)]           # one field cleared
    _save(client, sid, {(F_C, iid): " ", (F_A, iid): "", (F_E, iid): ""})
    assert _prep_rows(sid) == []                                  # clear all
    assert ui_text.text("UI_S15_PREP_NONE", "en") in _visible(_page(client, sid))


def test_an_omitted_field_is_no_edit_and_an_exact_retry_changes_nothing(client):
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    _save(client, sid, {(F_C, iid): COND, (F_A, iid): ACCEPT})
    r = _save(client, sid, {(F_E, iid): EVID})                    # others omitted
    assert _prep_rows(sid) == [(iid, COND, ACCEPT, EVID)]
    rows = _prep_rows(sid)
    for _ in range(2):                                            # exact retries
        r = _save(client, sid, {(F_C, iid): COND.replace(" ", " "),
                                (F_A, iid): ACCEPT, (F_E, iid): EVID})
        assert r.status_code == 200
        assert appmod.S15_PREP_UNCHANGED_MESSAGE in _text(r)
    assert _prep_rows(sid) == rows
    # a browser's CRLF line breaks do not turn an unchanged value into an edit
    _save(client, sid, {(F_C, iid): "line one\nline two"})
    r = _save(client, sid, {(F_C, iid): "line one\r\nline two"})
    assert appmod.S15_PREP_UNCHANGED_MESSAGE in _text(r)
    assert _prep_rows(sid)[0][1] == "line one\nline two"


def test_another_projects_or_unknown_interface_rejects_the_whole_submission(client):
    sid, ifc = _integrated_with_interface(client)
    other_sid, other = _integrated_with_interface(client)
    for bad in (other.interface_id, sm.new_interface_id(), "../x"):
        r = _save(client, sid, {(F_C, ifc.interface_id): COND, (F_C, bad): COND})
        assert r.status_code == 400
        body = _text(r)
        assert appmod.S15_PREP_UNKNOWN_INTERFACE_MESSAGE in body
        assert ui_text.text("UI_S15_PREP_DRAFT_UNSAVED", "en") in body
        assert COND in body                                       # draft kept
    assert _prep_rows(sid) == [] and _prep_rows(other_sid) == []


@pytest.mark.parametrize("raw", ["x" * 1001, "bad\x00text"])
def test_over_limit_or_nul_text_is_rejected_whole_and_never_truncated(client, raw):
    sid, ifc = _integrated_with_interface(client)
    r = _save(client, sid, {(F_C, ifc.interface_id): COND,
                            (F_A, ifc.interface_id): raw})
    assert r.status_code == 400
    assert _prep_rows(sid) == []


def test_a_failed_commit_is_not_saved_and_keeps_the_draft(client):
    sid, ifc = _integrated_with_interface(client)
    store = _store()
    real = store._conn
    store._conn = _FailOn(real, prefix="COMMIT")
    try:
        r = _save(client, sid, {(F_C, ifc.interface_id): COND})
    finally:
        store._conn = real
    assert r.status_code == 503 and store._connection_unsafe is False
    assert appmod.S15_PREP_NOT_SAVED_MESSAGE in _text(r) and COND in _text(r)
    assert _prep_rows(sid) == []


def test_a_committed_but_unconfirmed_write_is_recognised_as_saved(client):
    sid, ifc = _integrated_with_interface(client)
    store = _store()
    real = store._conn
    store._conn = _FailOn(real, commit_then=True)                 # commits, then raises
    try:
        r = _save(client, sid, {(F_C, ifc.interface_id): COND})
    finally:
        store._conn = real
    assert r.status_code == 200 and appmod.S15_PREP_SAVED_MESSAGE in _text(r)
    assert _prep_rows(sid) == [(ifc.interface_id, COND, None, None)]
    r = _save(client, sid, {(F_C, ifc.interface_id): COND})       # retry: no dup
    assert appmod.S15_PREP_UNCHANGED_MESSAGE in _text(r)
    assert len(_prep_rows(sid)) == 1


def test_an_unresolved_transaction_is_reported_as_unknown(client):
    sid, ifc = _integrated_with_interface(client)
    store = _store()
    real = store._conn
    store._conn = _CommitAndRollbackFail(real)
    try:
        r = _save(client, sid, {(F_C, ifc.interface_id): COND})
    finally:
        store._conn = real
    try:
        assert r.status_code == 503
        body = _text(r)
        assert appmod.S15_PREP_UNKNOWN_MESSAGE in body
        assert appmod.S15_PREP_SAVED_MESSAGE not in body
        assert appmod.S15_PREP_NOT_SAVED_MESSAGE not in body
        assert DESC not in body                  # no project state rendered
        assert _raw("SELECT COUNT(*) FROM subsystem_interface_preparations")[0][0] == 0
    finally:
        real.close()
        appmod._STORE = None


def test_corrupt_preparation_fails_the_page_session_and_report_closed(client):
    sid, ifc = _integrated_with_interface(client)
    _raw("INSERT INTO subsystem_interface_preparations VALUES (?, ?, ?, NULL, NULL)",
         (sid, "ifc-" + "1" * 32, COND), fk=False)
    r = client.get(f"/session/{sid}/interface-preparation")
    assert r.status_code == 503
    assert appmod.S15_PREP_UNAVAILABLE_MESSAGE in _text(r) and DESC not in _text(r)
    assert _save(client, sid, {(F_C, ifc.interface_id): ACCEPT}).status_code == 503
    assert client.get(f"/session/{sid}").status_code == 302
    assert client.get(f"/session/{sid}/deliverable").status_code == 302
    assert _raw("SELECT COUNT(*) FROM subsystem_interface_preparations "
                "WHERE project_id = ?", (sid,))[0][0] == 1    # nothing repaired


def test_a_session_that_is_not_a_saved_project_has_no_preparation_owner():
    assert appmod._s15_preparation_context("never-saved")[0] == appmod._S15_PREP_NO_PROJECT


def test_values_survive_restart_cold_load_and_reconstruction(client):
    sid, ifc = _integrated_with_interface(client)
    _save(client, sid, {(F_C, ifc.interface_id): COND, (F_E, ifc.interface_id): EVID})
    appmod.SESSION_STORE.pop(sid, None)
    old = appmod._STORE
    appmod._STORE = None                                          # restart
    try:
        page = _visible(_page(client, sid))                       # cold entry
        assert COND in page and EVID in page
        assert ui_text.text("UI_S15_PREP_PARTIAL", "en") in page
        report = _text(client.get(f"/session/{sid}/deliverable"))
        assert COND in report and EVID in report
        session = SR.reconstruct_readonly_state(_store(), sid)
        assert [i.interface_id for i in session.state.subsystem_interfaces] == [
            ifc.interface_id]
    finally:
        if old is not None:
            old.close()


def test_declaring_interfaces_is_unchanged_and_new_interfaces_start_empty(client):
    sid, ifc = _integrated_with_interface(client)
    _save(client, sid, {(F_C, ifc.interface_id): COND})
    before = _raw("SELECT * FROM subsystem_interfaces WHERE project_id = ?", (sid,))
    assert _declare(client, sid, "Bolted mounting.").status_code == 302
    after = _raw("SELECT * FROM subsystem_interfaces WHERE project_id = ?", (sid,))
    assert after[:1] == before and len(after) == 2               # append-only intact
    preps = _store().load_interface_preparations(sid)
    assert [p.interface_id for p in preps] == [ifc.interface_id]  # never remapped
    page = _visible(_page(client, sid))
    assert ui_text.text("UI_S15_PREP_NONE", "en") in page        # the new one


# ==========================================================================
# 4. Validation Plan truth and no compatibility / readiness effect
# ==========================================================================
def test_validation_plan_states_none_partial_all_and_unread_truthfully():
    unread, _ = _state_with_preparation(attached=False)
    step = _interface_step(unread)
    assert "none is recorded yet" not in step.closure_condition
    assert step.interface_preparation == ()
    none, _ = _state_with_preparation()
    assert "none is recorded yet" in _interface_step(none).closure_condition
    partial, _ = _state_with_preparation({F_C: COND})
    step = _interface_step(partial)
    assert "none is recorded yet" not in step.closure_condition
    assert "Recorded so far: the intended operating conditions." in step.closure_condition
    assert ("Not recorded yet: an observable acceptance criterion; the evidence or "
            "review needed.") in step.closure_condition
    assert step.interface_preparation == ((F_C, COND),)
    full, _ = _state_with_preparation({F_C: COND, F_A: ACCEPT, F_E: EVID})
    step = _interface_step(full)
    assert "verification-preparation inputs are recorded" in step.closure_condition
    assert step.interface_preparation == ((F_C, COND), (F_A, ACCEPT), (F_E, EVID))
    for state in (unread, none, partial, full):
        step = _interface_step(state)
        for phrase in ("intended operating conditions", "observable acceptance criterion",
                       "evidence or review",
                       "does not verify the interaction or establish compatibility"):
            assert phrase in step.closure_condition
        assert step.responsibility == "UNDETERMINED" and step.confidence == "UNDETERMINED"
        generated = step.closure_condition.lower()
        for word in ("verified", "passed", "is compatible", "feasible", "ready", "valid "):
            assert word not in generated


def test_recording_preparation_changes_no_other_project_truth():
    base, item = _state_with_preparation()
    full, _ = _state_with_preparation({F_C: COND, F_A: ACCEPT, F_E: EVID})
    full.subsystems, full.subsystem_interfaces = base.subsystems, base.subsystem_interfaces
    full.subsystem_interface_preparations = [
        sm.InterfacePreparation(item.interface_id, COND, ACCEPT, EVID)]
    assert derive_requirement_landscape(base) == derive_requirement_landscape(full)
    assert readiness_snapshot(base, ()) == readiness_snapshot(full, ())
    plan_a, plan_b = derive_validation_plan(base), derive_validation_plan(full)
    assert plan_a.outcome == plan_b.outcome
    assert [s.step_id for s in plan_a.steps] == [s.step_id for s in plan_b.steps]
    assert [s for s in plan_a.steps if s.provenance.anchor_kind != "subsystem_interface"] \
        == [s for s in plan_b.steps if s.provenance.anchor_kind != "subsystem_interface"]


def test_saving_preparation_leaves_ledger_gaps_and_progression_untouched(client):
    sid, ifc = _integrated_with_interface(client)
    state = _live(sid)
    before = (len(state.assertions), [(g.gap_type, g.status) for g in state.gaps],
              state.maturity_level, state.current_stage, state.domain,
              _raw("SELECT COUNT(*) FROM records WHERE project_id = ?", (sid,)))
    _save(client, sid, {(F_C, ifc.interface_id): COND, (F_A, ifc.interface_id): ACCEPT,
                        (F_E, ifc.interface_id): EVID})
    state = _live(sid)
    assert before == (len(state.assertions), [(g.gap_type, g.status) for g in state.gaps],
                      state.maturity_level, state.current_stage, state.domain,
                      _raw("SELECT COUNT(*) FROM records WHERE project_id = ?", (sid,)))


# ==========================================================================
# 5. Rendering: session / HTML report / PDF, English and Arabic / RTL
# ==========================================================================
def _pdf_source(c, sid, monkeypatch):
    seen = {}
    real = appmod._render_pdf_bytes
    monkeypatch.setattr(appmod, "_render_pdf_bytes",
                        lambda source: seen.setdefault("s", source) and real(source))
    r = c.post(f"/session/{sid}/deliverable.pdf", data={})
    assert r.status_code == 200 and r.data[:5] == b"%PDF-"
    return seen["s"]


def _section14(raw):
    m = re.search(r'id="vp-heading".*?</section>', raw, re.S) or \
        re.search(r'Validation Plan.*?</section>', raw, re.S)
    return _html.unescape(m.group(0)) if m else ""


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_session_report_and_pdf_carry_the_same_preparation(client, monkeypatch, lang):
    arabic = "داخل المبنى، بين 10 و40 درجة مئوية."
    sid, ifc = _integrated_with_interface(client, focus=ELEC)
    cond = arabic if lang == "ar" else COND
    _save(client, sid, {(F_C, ifc.interface_id): cond, (F_A, ifc.interface_id): ACCEPT})
    if lang == "ar":
        assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    report_raw = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    pdf_raw = _pdf_source(client, sid, monkeypatch)
    for raw in (_page(client, sid), report_raw, pdf_raw):
        block = _visible(_ifc_block(raw))
        for key in ("UI_S15_PREP_PARTIAL", "UI_S15_PREP_CONDITIONS",
                    "UI_S15_PREP_ACCEPTANCE", "UI_S15_PREP_EVIDENCE",
                    "UI_S15_PREP_NOT_RECORDED"):
            assert ui_text.text(key, lang) in block, key
        assert cond in block and ACCEPT in block                  # verbatim
        assert ifc.interface_id not in block
    for raw in (report_raw, pdf_raw):
        text = _html.unescape(raw)
        assert "Recorded so far: the intended operating conditions; an observable " \
               "acceptance criterion." in text                      # Section 14
        assert ui_text.text("UI_S15_PREP_OWNER_STATED", lang) in text
        assert text.count(cond) >= 2                               # scope + Section 14
    assert "data-prep-link" in _page(client, sid)                  # edit path
    assert "data-prep-link" not in pdf_raw
    page = client.get(f"/session/{sid}/interface-preparation").get_data(as_text=True)
    assert ui_text.text("UI_S15_PREP_TITLE", lang) in _html.unescape(page)
    if lang == "ar":
        assert 'dir="rtl"' in page or "dir='rtl'" in page


def test_every_new_catalogue_key_is_bilingual():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_S15_PREP_")]
    assert len(keys) >= 20
    for key in keys:
        assert ui_text.UI_STRINGS[key].get("en") and ui_text.UI_STRINGS[key].get("ar")
    for message in (appmod.S15_PREP_NO_PROJECT_MESSAGE, appmod.S15_PREP_UNAVAILABLE_MESSAGE,
                    appmod.S15_PREP_UNKNOWN_INTERFACE_MESSAGE, appmod.S15_PREP_TOO_LONG_MESSAGE,
                    appmod.S15_PREP_NOT_SAVED_MESSAGE, appmod.S15_PREP_SAVED_MESSAGE,
                    appmod.S15_PREP_UNCHANGED_MESSAGE, appmod.S15_PREP_SAVED_NOT_SHOWN_MESSAGE,
                    appmod.S15_PREP_UNKNOWN_MESSAGE):
        assert ui_text.localize_message(message, "en") == message
        assert ui_text.localize_message(message, "ar") != message


# ==========================================================================
# 6. F724-1 — a stale full-form submission never overwrites untouched fields
# ==========================================================================
def _browser_form(c, sid):
    """Everything a browser would submit from a freshly rendered preparation
    page: every visible textarea (its rendered content) and every hidden
    ``prep_*`` input, as ONE full-form snapshot."""
    raw = c.get(f"/session/{sid}/interface-preparation").get_data(as_text=True)
    form = {}
    for name, body in re.findall(
            r'<textarea[^>]*name="(prep_[^"]+)"[^>]*>(.*?)</textarea>', raw, re.S):
        form[name] = _html.unescape(body)
    for name, value in re.findall(
            r'<input type="hidden" name="(prep_[^"]+)" value="([^"]*)"', raw):
        form[name] = _html.unescape(value)
    return form


def _submit_full(c, sid, form, edits):
    """Submit the WHOLE stale form with only ``edits`` ((field, iid) -> text)
    typed into it, exactly as a browser does."""
    data = dict(form)
    for (f, i), text in edits.items():
        data[_field(f, i)] = text
    return c.post(f"/session/{sid}/interface-preparation", data=data)


def test_f724_stale_blank_never_clears_a_newer_value(client):
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    tab_a, tab_b = _browser_form(client, sid), _browser_form(client, sid)
    assert _submit_full(client, sid, tab_a, {(F_C, iid): COND}).status_code == 200
    r = _submit_full(client, sid, tab_b, {(F_A, iid): ACCEPT})     # B edits ONLY this
    assert r.status_code == 200
    assert _prep_rows(sid) == [(iid, COND, ACCEPT, None)]           # A's value kept


def test_f724_stale_value_never_restores_a_cleared_value(client):
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    _submit_full(client, sid, _browser_form(client, sid), {(F_C, iid): COND})
    tab_a, tab_b = _browser_form(client, sid), _browser_form(client, sid)
    _submit_full(client, sid, tab_a, {(F_C, iid): ""})              # A clears it
    assert _prep_rows(sid) == []
    _submit_full(client, sid, tab_b, {(F_A, iid): ACCEPT})
    assert _prep_rows(sid) == [(iid, None, ACCEPT, None)]           # stays cleared


def test_f724_untouched_fields_of_another_interface_are_never_overwritten(client):
    sid, first = _integrated_with_interface(client)
    assert _declare(client, sid, "Bolted mounting.").status_code == 302
    second = [i for i in _store().load_subsystem_interfaces(sid)
              if i.interface_id != first.interface_id][0]
    tab_a, tab_b = _browser_form(client, sid), _browser_form(client, sid)
    _submit_full(client, sid, tab_a, {(F_E, second.interface_id): EVID,
                                      (F_C, first.interface_id): COND})
    _submit_full(client, sid, tab_b, {(F_A, first.interface_id): ACCEPT})
    rows = {r[0]: r[1:] for r in _prep_rows(sid)}
    assert rows[first.interface_id] == (COND, ACCEPT, None)
    assert rows[second.interface_id] == (None, None, EVID)


def test_f724_an_explicit_clear_still_clears(client):
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    _submit_full(client, sid, _browser_form(client, sid),
                 {(F_C, iid): COND, (F_A, iid): ACCEPT})
    form = _browser_form(client, sid)
    assert form[_field(F_C, iid)] == COND
    _submit_full(client, sid, form, {(F_C, iid): ""})
    assert _prep_rows(sid) == [(iid, None, ACCEPT, None)]


def test_f724_a_visible_field_without_its_baseline_fails_closed(client):
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    _submit_full(client, sid, _browser_form(client, sid), {(F_C, iid): COND})
    r = client.post(f"/session/{sid}/interface-preparation",
                    data={_field(F_A, iid): ACCEPT})                 # no baseline
    assert r.status_code == 400
    assert appmod.S15_PREP_NOT_SAVED_MESSAGE in _text(r)
    assert _prep_rows(sid) == [(iid, COND, None, None)]


def test_f724_a_refused_retry_keeps_the_original_baseline(client):
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    tab_b = _browser_form(client, sid)                               # rendered empty
    _submit_full(client, sid, _browser_form(client, sid), {(F_C, iid): COND})
    r = _submit_full(client, sid, tab_b, {(F_A, iid): "x" * 1001})  # refused
    assert r.status_code == 400
    raw = r.get_data(as_text=True)
    base = re.search(r'name="%s" value="([^"]*)"'
                     % re.escape(appmod._S15_PREP_BASE_PREFIXES[F_C] + iid), raw)
    assert base is not None and base.group(1) == ""                  # not the newer "COND"
    retry = {name: _html.unescape(v) for name, v in re.findall(
        r'<input type="hidden" name="(prep_[^"]+)" value="([^"]*)"', raw)}
    retry.update({n: _html.unescape(b) for n, b in re.findall(
        r'<textarea[^>]*name="(prep_[^"]+)"[^>]*>(.*?)</textarea>', raw, re.S)})
    retry[_field(F_A, iid)] = ACCEPT
    assert client.post(f"/session/{sid}/interface-preparation",
                       data=retry).status_code == 200
    assert _prep_rows(sid) == [(iid, COND, ACCEPT, None)]
