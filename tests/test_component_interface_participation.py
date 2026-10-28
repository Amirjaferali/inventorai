"""COMPONENT-INTERFACE-PARTICIPATION-01 — the components the inventor says take part in ONE declared interaction.

For ONE existing declared interaction of a valid durable integrated composition the inventor may state which of
the project's CURRENT declared physical components take part in it. What is pinned:
  * semantics (``engine/subsystem_model.py``): a current-value attribute of ONE interaction keyed only by the
    interaction's and the components' stable ids; OWNER_STATED / UNVALIDATED; CURRENT participation = stored rows
    whose component is active, in declaration order; nothing inferred from part links (no endpoint overlap is
    required); a withdrawn component is never current and never newly named;
  * persistence (``engine/record_store.py``): ONE additive sidecar ``subsystem_interface_components`` keyed by
    ``(project_id, interface_id, component_id)`` with composite foreign keys to the exact interaction and
    declaration rows, created AFTER the interface and component migrations (the legacy component rebuild
    included); an unknown table shape is refused; the whole composition, interactions, inventory and every row
    validated inside ONE serialized write; target == current -> UNCHANGED (nothing written); current != the
    displayed baseline -> STALE (nothing written); otherwise only ACTIVE membership is replaced — rows of
    withdrawn components are never compared, reasserted or deleted;
  * web (``web/app.py``): ONE dedicated POST behind the central project authorization and the CSRF guard,
    committed-truth SAVED / NOT SAVED / UNKNOWN; shown on the interaction-preparation page, the Parts, Components
    & Interactions view and the shared report / PDF interaction section (EN / AR), each with the boundary that it
    is the inventor's statement, not an engineering check;
  * the existing preparation save, the Stage 35 export, SafetySignal, readiness, evidence, IdeaState and
    progression are unchanged.
"""
import html as _html
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
    INTERFACE_PARTICIPATION_CLEARED, INTERFACE_PARTICIPATION_SAVED, INTERFACE_PARTICIPATION_UNCHANGED,
    InterfaceParticipationRejected, InterfaceParticipationStale, InterfaceParticipationWithdrawn,
    InterfaceParticipationsCorrupt, ProjectNotFound, RecordStoreConnectionUnsafe, SqliteRecordStore)
from tests.csrf_client import csrf_client
from tests.test_28t5_nonfocused_part_report import _strip
from tests.test_component_inventory_correct_withdraw import _correct, _legacy_db, _withdraw
from tests.test_component_inventory_declare_list import _declare as _declare_component, _integrated
from tests.test_stage15_integrated_invention_entry import (
    ELEC, MECH, _CommitAndRollbackFail, _contract, _pair, _pdf_source, _ri)
from tests.test_stage15_subsystem_interface_declaration import _FailOn, _restart
from tests.test_stage15_subsystem_interface_declaration import _declare as _declare_interface
from web import ui_text

PREP = "/session/%s/interface-preparation"
POST = "/session/%s/interface-participation"
PCI = "/session/%s/parts-components-interactions"
REPORT = "/session/%s/deliverable"
SECRET = "Zq-participation-8841"
_FORM_RE = re.compile(
    r'<form method="POST" action="/session/[^"]+/interface-participation" data-icp-form>.*?</form>', re.S)


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


def _rows(pid):
    return _raw("SELECT interface_id, component_id FROM subsystem_interface_components "
                "WHERE project_id = ? ORDER BY interface_id, component_id", (pid,))


def _t(key, lang="en"):
    return ui_text.text(key, lang)


# --- store-level construction -------------------------------------------------
def _project(store, idea="i-icp"):
    subs = _pair()
    pid = store.create_project(_contract(idea), reconstruction_inputs=_ri(MECH), subsystems=subs)
    return pid, tuple(subs)


def _ifc(store, pid, subs, description="Motor turns the hinge", key="i1"):
    item = sm.declared_interface(subs, subs[0].subsystem_id, subs[1].subsystem_id, description)
    store.append_subsystem_interface(pid, item, key)
    return item.interface_id


def _cmp(store, pid, subs, name, parts=(), key=None):
    item = sm.declared_component(subs, name, "Does " + name, parts)
    store.append_project_component(pid, item, key or ("k-" + name))
    return item.component_id


def _current(store, pid, interface_id):
    record = store.load_interface_participation(pid)
    return sm.current_interface_participants(record["participations"],
                                             record["components"]).get(interface_id, ())


# --- web-level construction ---------------------------------------------------
def _web_project(c, focus=MECH, names=("Hinge motor", "Driver board", "Battery pack")):
    sid = _integrated(c, focus)
    r = _declare_interface(c, sid, "Motor turns the hinge")
    assert r.status_code == 302, r.status_code
    for name in names:
        assert _declare_component(c, sid, name=name, function="Does its job").status_code in (200, 302)
    return sid


def _forms(raw):
    forms = []
    for form in _FORM_RE.findall(raw):
        def value(name):
            m = re.search(r'name="%s" value="([^"]*)"' % name, form)
            return _html.unescape(m.group(1)) if m else None
        options = [(_html.unescape(v), bool(chk)) for v, chk in re.findall(
            r'name="participant" value="([^"]*)"( checked)?', form)]
        forms.append({"interface": value("interface_id"), "base": value("participant_base"),
                      "options": options})
    return forms


def _form(c, sid):
    forms = _forms(c.get(PREP % sid).get_data(as_text=True))
    assert len(forms) == 1, len(forms)
    return forms[0]


def _post(c, sid, form, selected, **override):
    data = {"interface_id": form["interface"], "participant_base": form["base"],
            "participant": list(selected)}
    data.update(override)
    return c.post(POST % sid, data=data)


def _says(resp, message):
    return _html.unescape(resp.get_data(as_text=True)).count(message) >= 1


def _report_lines(raw):
    return [re.sub(r"<[^>]+>", "", _html.unescape(m)) for m in re.findall(
        r"<p[^>]*data-ifc-participants>(.*?)</p>", raw, re.S)]


def _pci_lines(raw):
    return [re.sub(r"<[^>]+>", "", _html.unescape(m)) for m in re.findall(
        r"<p[^>]*data-pci-participants>(.*?)</p>", raw, re.S)]


# ==========================================================================
# 1. Semantic owner
# ==========================================================================
def _inventory(store, pid):
    return store.load_component_inventory_record(pid)[1]


def test_m01_validation_is_whole_canonical_and_refuses_orphans(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "m.db"))
    pid, subs = _project(store)
    ifc = _ifc(store, pid, subs)
    a, b = _cmp(store, pid, subs, "A"), _cmp(store, pid, subs, "B")
    interfaces = store.load_subsystem_composition(pid)[1]
    inv = _inventory(store, pid)
    rows = (sm.InterfaceParticipation(ifc, b), sm.InterfaceParticipation(ifc, a))
    assert [p.component_id for p in sm.validate_interface_participations(rows, interfaces, inv)] == [a, b]
    assert sm.validate_interface_participations((), interfaces, inv) == ()
    for bad in ((sm.InterfaceParticipation(ifc, a), sm.InterfaceParticipation(ifc, a)),
                (sm.InterfaceParticipation("ifc-" + "0" * 32, a),),
                (sm.InterfaceParticipation(ifc, "cmp-" + "0" * 32),),
                (sm.InterfaceParticipation(ifc, a, provenance="SYSTEM_INFERRED"),),
                (sm.InterfaceParticipation(ifc, a, validation_state="VALIDATED"),),
                ("not a participation",)):
        with pytest.raises(sm.InterfaceParticipationError):
            sm.validate_interface_participations(bad, interfaces, inv)
    assert sm.InterfaceParticipation(ifc, a).provenance == OWNER_STATED
    assert sm.InterfaceParticipation(ifc, a).validation_state == UNVALIDATED


def test_m02_current_is_active_only_in_declaration_order_and_the_target_is_strict(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "m2.db"))
    pid, subs = _project(store)
    ifc = _ifc(store, pid, subs)
    a, b, c = (_cmp(store, pid, subs, n) for n in ("A", "B", "C"))
    _withdraw(store, pid, b, 0)
    inv = _inventory(store, pid)
    interfaces = store.load_subsystem_composition(pid)[1]
    rows = tuple(sm.InterfaceParticipation(ifc, x) for x in (c, b, a))
    assert sm.current_interface_participants(rows, inv.active) == {ifc: (a, c)}
    assert sm.participation_target(inv, interfaces, ifc, (c, a)) == (a, c)
    assert sm.participation_target(inv, interfaces, ifc, ()) == ()
    with pytest.raises(sm.ComponentAlreadyWithdrawn):
        sm.participation_target(inv, interfaces, ifc, (b,))
    for args in ((("ifc-" + "1" * 32), (a,)), (ifc, (a, a)), (ifc, ("cmp-bad",)),
                 (ifc, ("cmp-" + "2" * 32,))):
        with pytest.raises(sm.InterfaceParticipationError):
            sm.participation_target(inv, interfaces, *args)


def test_m03_participation_needs_no_overlap_with_the_interactions_parts(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "m3.db"))
    pid, subs = _project(store)
    ifc = _ifc(store, pid, subs)
    unassigned = _cmp(store, pid, subs, "Loose bracket")                       # project level
    store.set_interface_participation(pid, ifc, (unassigned,), ())
    assert _current(store, pid, ifc) == (unassigned,)


# ==========================================================================
# 2. Persistence
# ==========================================================================
def test_s01_save_retry_replace_clear_and_absence_is_not_recorded(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "s1.db"))
    pid, subs = _project(store)
    ifc = _ifc(store, pid, subs)
    a, b = _cmp(store, pid, subs, "A"), _cmp(store, pid, subs, "B")
    assert store.load_interface_participation(pid)["participations"] == ()
    assert _current(store, pid, ifc) == ()
    assert store.set_interface_participation(pid, ifc, (b, a), ()) == INTERFACE_PARTICIPATION_SAVED
    assert _current(store, pid, ifc) == (a, b)
    assert store.set_interface_participation(pid, ifc, [a, b], ()) == INTERFACE_PARTICIPATION_UNCHANGED
    assert store.set_interface_participation(pid, ifc, (b,), (a, b)) == INTERFACE_PARTICIPATION_SAVED
    assert _current(store, pid, ifc) == (b,)
    assert store.set_interface_participation(pid, ifc, (), (b,)) == INTERFACE_PARTICIPATION_CLEARED
    assert store.load_interface_participation(pid)["participations"] == ()


def test_s02_a_stale_baseline_never_overwrites_newer_truth(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "s2.db"))
    pid, subs = _project(store)
    ifc = _ifc(store, pid, subs)
    a, b = _cmp(store, pid, subs, "A"), _cmp(store, pid, subs, "B")
    store.set_interface_participation(pid, ifc, (a,), ())
    with pytest.raises(InterfaceParticipationStale):
        store.set_interface_participation(pid, ifc, (b,), ())                 # form showed "none"
    assert _current(store, pid, ifc) == (a,)


def test_s03_membership_project_and_shape_are_decided_before_any_write(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "s3.db"))
    pid, subs = _project(store)
    other, osubs = _project(store, idea="i-other")
    ifc = _ifc(store, pid, subs)
    oifc = _ifc(store, other, osubs, key="o1")
    a = _cmp(store, pid, subs, "A")
    foreign = _cmp(store, other, osubs, "Foreign")
    for call in ((pid, ifc, (foreign,), ()),          # another project's component
                 (pid, oifc, (a,), ()),               # another project's interaction
                 (pid, "ifc-" + "3" * 32, (a,), ()),  # unknown interaction
                 (pid, ifc, (a, a), ()),              # named twice
                 (pid, ifc, ("",), ()),               # malformed
                 (pid, "", (a,), ())):
        with pytest.raises(InterfaceParticipationRejected):
            store.set_interface_participation(*call)
    with pytest.raises(ProjectNotFound):
        store.set_interface_participation("p-missing", ifc, (a,), ())
    assert _rows_of(store, pid) == [] and _rows_of(store, other) == []


def _rows_of(store, pid):
    return store._conn.execute("SELECT interface_id, component_id FROM subsystem_interface_components "
                               "WHERE project_id = ?", (pid,)).fetchall()


def test_s04_correction_keeps_withdrawal_hides_history_and_redeclaration_inherits_nothing(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "s4.db"))
    pid, subs = _project(store)
    ifc = _ifc(store, pid, subs)
    a, b = _cmp(store, pid, subs, "A"), _cmp(store, pid, subs, "B")
    store.set_interface_participation(pid, ifc, (a, b), ())
    _correct(store, pid, a, 0, "A renamed")                                    # same identity
    assert _current(store, pid, ifc) == (a, b)
    _withdraw(store, pid, b, 0)
    assert _current(store, pid, ifc) == (a,)                                   # current projection
    assert sorted(_rows_of(store, pid)) == sorted([(ifc, a), (ifc, b)])        # history preserved
    with pytest.raises(InterfaceParticipationWithdrawn):
        store.set_interface_participation(pid, ifc, (a, b), (a,))
    # The CURRENT projection is the baseline: the withdrawn row is never compared ...
    with pytest.raises(InterfaceParticipationStale):
        store.set_interface_participation(pid, ifc, (), (a, b))
    assert store.set_interface_participation(pid, ifc, (a,), ()) == INTERFACE_PARTICIPATION_UNCHANGED
    # ... and an ordinary replacement never deletes or reasserts it.
    assert store.set_interface_participation(pid, ifc, (), (a,)) == INTERFACE_PARTICIPATION_CLEARED
    assert _rows_of(store, pid) == [(ifc, b)]
    c = _cmp(store, pid, subs, "B")                                            # a new declaration
    assert _current(store, pid, ifc) == () and c != b


def test_s05_migration_is_additive_ordered_idempotent_and_refuses_an_unknown_shape(tmp_path):
    path = str(tmp_path / "mig.db")
    store = SqliteRecordStore(path)
    pid, subs = _project(store)
    ifc = _ifc(store, pid, subs)
    a = _cmp(store, pid, subs, "A")
    store.set_interface_participation(pid, ifc, (a,), ())
    columns = [r[1] for r in store._conn.execute("PRAGMA table_info(subsystem_interface_components)")]
    assert columns == ["project_id", "interface_id", "component_id"]
    fks = {(r[2], r[3], r[4]) for r in store._conn.execute(
        "PRAGMA foreign_key_list(subsystem_interface_components)")}
    assert ("subsystem_interfaces", "interface_id", "interface_id") in fks
    assert ("project_components", "component_id", "component_id") in fks
    store.close()
    SqliteRecordStore(path).close()                                            # idempotent reopen
    check = SqliteRecordStore(path)
    assert _current(check, pid, ifc) == (a,)                                   # rows preserved
    check.close()
    conn = sqlite3.connect(path)                                               # a pre-capability database
    conn.execute("DROP TABLE subsystem_interface_components")
    conn.commit()
    conn.close()
    store = SqliteRecordStore(path)
    assert store.load_interface_participation(pid)["participations"] == ()
    assert [c.component_id for c in store.load_interface_participation(pid)["components"]] == [a]
    store.close()
    conn = sqlite3.connect(path)
    conn.execute("DROP TABLE subsystem_interface_components")
    conn.execute("CREATE TABLE subsystem_interface_components (project_id TEXT, interface_id TEXT, "
                 "component_id TEXT, quantity INTEGER)")
    conn.commit()
    conn.close()
    with pytest.raises(sqlite3.DatabaseError):
        SqliteRecordStore(path)
    source = open(os.path.join("engine", "record_store.py"), encoding="utf-8").read()
    order = [source.index("self._migrate_%s(self._conn)" % name) for name in (
        "subsystem_interfaces", "project_components", "component_prototype_needs",
        "interface_components")]
    assert order == sorted(order)


def test_s06_a_legacy_component_database_is_rebuilt_before_the_sidecar_is_created(tmp_path):
    path = str(tmp_path / "legacy.db")
    pid, _other, subs, before = _legacy_db(path)
    conn = sqlite3.connect(path)
    for table in ("subsystem_interface_components", "component_prototype_needs"):
        conn.execute("DROP TABLE IF EXISTS %s" % table)
    conn.commit()
    conn.close()
    store = SqliteRecordStore(path)
    ifc = _ifc(store, pid, subs)
    legacy = [c.component_id for c in store.load_interface_participation(pid)["components"]]
    assert len(legacy) == len(before) // 2 == 3
    assert store.set_interface_participation(pid, ifc, tuple(legacy[:2]), ()) == INTERFACE_PARTICIPATION_SAVED
    assert _current(store, pid, ifc) == tuple(legacy[:2])


def test_s07_the_database_backstop_and_the_whole_collection_validation(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "c.db"))
    pid, subs = _project(store)
    other, osubs = _project(store, idea="i-other")
    ifc = _ifc(store, pid, subs)
    a = _cmp(store, pid, subs, "A")
    foreign = _cmp(store, other, osubs, "Foreign")
    with pytest.raises(sqlite3.IntegrityError):                                # FK: other project
        store._conn.execute("INSERT INTO subsystem_interface_components VALUES (?, ?, ?)",
                            (pid, ifc, foreign))
    store._conn.execute("PRAGMA foreign_keys = OFF")
    store._conn.execute("INSERT INTO subsystem_interface_components VALUES (?, ?, ?)",
                        (pid, ifc, "cmp-" + "9" * 32))                         # orphan
    store._conn.execute("PRAGMA foreign_keys = ON")
    for read in (store.load_interface_participation, store.load_parts_components_interactions):
        with pytest.raises(InterfaceParticipationsCorrupt):
            read(pid)
    with pytest.raises(InterfaceParticipationsCorrupt):
        store.set_interface_participation(pid, ifc, (a,), ())
    assert (ifc, a) not in _rows_of(store, pid)
    # the inventory itself still reads, and another project is untouched
    assert [c.component_id for c in store.load_component_inventory_record(pid)[1].active] == [a]
    assert store.load_interface_participation(other)["participations"] == ()


def test_s08_failed_and_unresolved_writes_roll_back_and_refuse(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "f.db"))
    pid, subs = _project(store)
    ifc = _ifc(store, pid, subs)
    a, b = _cmp(store, pid, subs, "A"), _cmp(store, pid, subs, "B")
    store.set_interface_participation(pid, ifc, (a,), ())
    real = store._conn
    store._conn = _FailOn(real, prefix="INSERT INTO subsystem_interface_components")
    with pytest.raises(sqlite3.OperationalError):
        store.set_interface_participation(pid, ifc, (b,), (a,))                # delete then failed insert
    store._conn = real
    assert _current(store, pid, ifc) == (a,)                                   # whole replacement rolled back
    store._conn = _CommitAndRollbackFail(real)
    with pytest.raises(sqlite3.OperationalError):
        store.set_interface_participation(pid, ifc, (b,), (a,))
    store._conn = real
    for call in ((store.load_interface_participation, (pid,)),
                 (store.set_interface_participation, (pid, ifc, (b,), (a,)))):
        with pytest.raises(RecordStoreConnectionUnsafe):
            call[0](*call[1])


def test_s09_concurrent_writers_from_one_baseline_never_both_win(tmp_path):
    path = str(tmp_path / "race.db")
    seed = SqliteRecordStore(path)
    pid, subs = _project(seed)
    ifc = _ifc(seed, pid, subs)
    ids = [_cmp(seed, pid, subs, "C%d" % i) for i in range(4)]
    seed.close()
    barrier = threading.Barrier(len(ids))
    results = []

    def run(i):
        store = SqliteRecordStore(path)
        try:
            barrier.wait()
            results.append(store.set_interface_participation(pid, ifc, (ids[i],), ()))
        except InterfaceParticipationStale:
            results.append("STALE")
        except sqlite3.OperationalError:
            results.append("BUSY")
        finally:
            store.close()
    threads = [threading.Thread(target=run, args=(i,)) for i in range(len(ids))]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert results.count(INTERFACE_PARTICIPATION_SAVED) == 1
    assert set(results) <= {INTERFACE_PARTICIPATION_SAVED, "STALE", "BUSY"}
    check = SqliteRecordStore(path)
    assert len(_current(check, pid, ifc)) == 1
    check.close()


# ==========================================================================
# 3. Web: the preparation page and the dedicated POST
# ==========================================================================
def test_w01_declare_view_replace_and_clear_on_the_preparation_page(client):
    sid = _web_project(client)
    raw = client.get(PREP % sid).get_data(as_text=True)
    text = _html.unescape(raw)
    assert _t("UI_ICP_HEADING") in text and _t("UI_ICP_BOUNDARY") in text
    assert "data-icp-not-recorded" in raw
    form = _form(client, sid)
    assert form["base"] == "" and len(form["options"]) == 3 and not any(c for _i, c in form["options"])
    ids = [i for i, _c in form["options"]]
    r = _post(client, sid, form, [ids[2], ids[0]])
    assert r.status_code == 200 and _says(r, _t("UI_ICP_MSG_SAVED"))
    form = _form(client, sid)
    assert form["base"] == ",".join([ids[0], ids[2]])
    assert [c for _i, c in form["options"]] == [True, False, True]
    page = _html.unescape(client.get(PREP % sid).get_data(as_text=True))
    assert re.search(r"Hinge motor.*Battery pack", page.split(_t("UI_ICP_LABEL"))[1], re.S)
    r = _post(client, sid, form, [ids[1]])
    assert _says(r, _t("UI_ICP_MSG_SAVED")) and [c for _i, c in _form(client, sid)["options"]] == [
        False, True, False]
    r = _post(client, sid, _form(client, sid), [])
    assert _says(r, _t("UI_ICP_MSG_CLEARED")) and _rows(sid) == []
    for internal in ids:
        assert internal not in re.sub(r'<[^>]+>', " ", r.get_data(as_text=True))  # no id as visible text


def test_w02_retry_unchanged_and_stale_forms_write_nothing(client):
    sid = _web_project(client)
    form = _form(client, sid)
    ids = [i for i, _c in form["options"]]
    assert _says(_post(client, sid, form, []), _t("UI_ICP_MSG_UNCHANGED"))
    _post(client, sid, form, [ids[0]])
    r = _post(client, sid, form, [ids[0]])                                     # exact retry
    assert r.status_code == 200 and _says(r, _t("UI_ICP_MSG_UNCHANGED"))
    r = _post(client, sid, form, [ids[1]])                                     # stale: showed "none"
    assert r.status_code == 409 and _says(r, _t("UI_ICP_MSG_STALE"))
    assert [c for _i, c in _rows(sid)] == [ids[0]]


def test_w02b_a_resubmitted_baseline_is_decided_by_the_store_never_answered_unchanged(client):
    sid = _web_project(client)
    stale = _form(client, sid)                                                 # shows "none"
    ids = [i for i, _c in stale["options"]]
    _post(client, sid, stale, [ids[0]])                                        # another tab saves
    r = _post(client, sid, stale, [])                                          # stale form, unchanged by it
    assert r.status_code == 409 and _says(r, _t("UI_ICP_MSG_STALE"))
    assert not _says(r, _t("UI_ICP_MSG_UNCHANGED"))
    assert [c for _i, c in _rows(sid)] == [ids[0]]
    other = _web_project(client, names=("Lid",))
    foreign = _form(client, other)                                             # base "" and no selection
    r = _post(client, sid, dict(stale, interface=foreign["interface"], base=""), [])
    assert r.status_code == 400 and _says(r, _t("UI_ICP_MSG_REJECTED"))
    r = _post(client, sid, dict(stale, interface="ifc-" + "6" * 32, base=""), [])
    assert r.status_code == 400 and _says(r, _t("UI_ICP_MSG_REJECTED"))
    assert [c for _i, c in _rows(sid)] == [ids[0]] and _rows(other) == []


@pytest.mark.parametrize("override", [
    {"interface_id": "ifc-not-an-id"}, {"interface_id": ["ifc-" + "0" * 32, "ifc-" + "1" * 32]},
    {"participant_base": ["", ""]}, {"participant": ["cmp-x"]}, {"dup": True}, {"no_base": True},
    {"unknown_interface": True}])
def test_w03_malformed_forms_are_rejected_and_write_nothing(client, override):
    sid = _web_project(client)
    form = _form(client, sid)
    ids = [i for i, _c in form["options"]]
    data = {"interface_id": form["interface"], "participant_base": form["base"], "participant": [ids[0]]}
    if override.get("dup"):
        data["participant"] = [ids[0], ids[0]]
    elif override.get("no_base"):
        data.pop("participant_base")
    elif override.get("unknown_interface"):
        data["interface_id"] = "ifc-" + "7" * 32
    else:
        data.update(override)
    r = client.post(POST % sid, data=data)
    assert r.status_code == 400 and _says(r, _t("UI_ICP_MSG_REJECTED"))
    assert _rows(sid) == []


def test_w04_authorization_csrf_and_cross_project_identities(client):
    from tests.test_commercial_evidence_capture import _client_for
    owner, _aid = _client_for("icp-owner@example.com")
    sid = _web_project(owner)
    form = _form(owner, sid)
    ids = [i for i, _c in form["options"]]
    intruder, _bid = _client_for("icp-intruder@example.com")
    r = _post(intruder, sid, form, ids)
    assert r.status_code in (302, 403, 404) and "Hinge motor" not in r.get_data(as_text=True)
    assert intruder.get(PREP % sid).status_code in (302, 403, 404)
    raw_client = appmod.app.test_client()                                      # no CSRF token
    r = raw_client.post(POST % sid, data={"interface_id": form["interface"], "participant_base": "",
                                          "participant": ids[:1]})
    assert r.status_code == 403
    assert _rows(sid) == []
    other = _web_project(owner, names=("Lid",))
    foreign = _form(owner, other)
    r = _post(owner, sid, form, [foreign["options"][0][0]])                    # other project's component
    assert r.status_code == 400 and _says(r, _t("UI_ICP_MSG_REJECTED"))
    r = _post(owner, sid, dict(form, interface=foreign["interface"]), ids[:1])  # other project's interaction
    assert r.status_code == 400
    assert _rows(sid) == [] and _rows(other) == []


def test_w05_a_withdrawn_component_is_not_offered_not_current_and_takes_none(client):
    sid = _web_project(client)
    form = _form(client, sid)
    ids = [i for i, _c in form["options"]]
    _post(client, sid, form, ids[:2])
    _withdraw(_store(), sid, ids[1], 0)
    form = _form(client, sid)
    assert [i for i, _c in form["options"]] == [ids[0], ids[2]] and form["base"] == ids[0]
    page = _html.unescape(client.get(PREP % sid).get_data(as_text=True))
    assert "Driver board" not in page.split(_t("UI_ICP_HEADING"))[1].split(_t("UI_S15_OBS_HEADING"))[0]
    r = _post(client, sid, dict(form, base=ids[0]), [ids[0], ids[1]])
    assert r.status_code in (400, 409) and _rows(sid) == sorted(
        [(form["interface"], ids[0]), (form["interface"], ids[1])])           # history kept, not reasserted
    r = _post(client, sid, form, [])                                           # clears the CURRENT set only
    assert _says(r, _t("UI_ICP_MSG_CLEARED")) and _rows(sid) == [(form["interface"], ids[1])]


def test_w06_failed_uncertain_and_unresolved_commits_are_truthful(client):
    sid = _web_project(client)
    store = _store()
    real = store._conn
    form = _form(client, sid)
    ids = [i for i, _c in form["options"]]
    store._conn = _FailOn(real, prefix="INSERT INTO subsystem_interface_components")
    r = _post(client, sid, form, ids[:1])
    store._conn = real
    assert r.status_code == 503 and _says(r, _t("UI_ICP_MSG_NOT_SAVED")) and _rows(sid) == []
    store._conn = _FailOn(real, commit_then=True)                              # committed, then raised
    r = _post(client, sid, form, ids[:1])
    store._conn = real
    assert r.status_code == 200 and _says(r, _t("UI_ICP_MSG_SAVED"))
    assert [c for _i, c in _rows(sid)] == ids[:1]
    form = _form(client, sid)
    store._conn = _CommitAndRollbackFail(real)                                 # unresolved
    r = _post(client, sid, form, ids[1:2])
    store._conn = real
    assert r.status_code == 503 and _says(r, _t("UI_ICP_MSG_UNKNOWN"))
    _restart()
    assert [c for _i, c in _rows(sid)] == ids[:1]


def test_w07_unreadable_participation_reads_unavailable_never_not_recorded(client, monkeypatch):
    sid = _web_project(client)
    form = _form(client, sid)
    ids = [i for i, _c in form["options"]]
    _post(client, sid, form, ids[:1])
    _raw("INSERT INTO subsystem_interface_components VALUES (?, ?, ?)",
         (sid, form["interface"], "cmp-" + "8" * 32), fk=False)               # orphan row
    raw = client.get(PREP % sid).get_data(as_text=True)
    assert "data-icp-unavailable" in raw and "data-icp-not-recorded" not in raw and _forms(raw) == []
    assert "data-prep-intro" in raw                                            # the rest of the page stays
    r = _post(client, sid, form, ids[:2])
    assert r.status_code == 503 and _says(r, _t("UI_ICP_MSG_NOT_SAVED"))
    # the shared snapshot fails closed for every consumer — never partial or mismatched
    pci = client.get(PCI % sid)
    assert pci.status_code == 503 and "Hinge motor" not in pci.get_data(as_text=True)
    report = client.get(REPORT % sid).get_data(as_text=True)
    assert "data-ifc-participation-unavailable" in report and "data-ifc-participants" not in report
    assert "data-ifc-participants-none" not in report


# ==========================================================================
# 4. Parts, Components & Interactions view and the report / PDF
# ==========================================================================
@pytest.mark.parametrize("focus", [MECH, ELEC])
def test_v01_the_view_report_and_pdf_show_the_same_current_participants(client, focus, monkeypatch):
    sid = _web_project(client, focus=focus)
    report = client.get(REPORT % sid).get_data(as_text=True)
    assert "data-ifc-participants-none" in report and _t("UI_ICP_BOUNDARY") in _html.unescape(report)
    form = _form(client, sid)
    ids = [i for i, _c in form["options"]]
    _post(client, sid, form, [ids[2], ids[0]])
    expected = _t("UI_ICP_LABEL") + " Hinge motor, Battery pack"
    pci = client.get(PCI % sid).get_data(as_text=True)
    assert _pci_lines(pci) == [expected] and _t("UI_ICP_BOUNDARY") in _html.unescape(pci)
    report = client.get(REPORT % sid).get_data(as_text=True)
    assert _report_lines(report) == [expected]
    assert _report_lines(_pdf_source(client, sid, monkeypatch)) == [expected]
    _correct(_store(), sid, ids[0], 0, "Hinge motor v2")
    _withdraw(_store(), sid, ids[2], 0)
    expected = _t("UI_ICP_LABEL") + " Hinge motor v2"
    assert _pci_lines(client.get(PCI % sid).get_data(as_text=True)) == [expected]
    assert _report_lines(client.get(REPORT % sid).get_data(as_text=True)) == [expected]


def test_v02_inventor_text_is_escaped_and_direction_isolated(client):
    sid = _web_project(client, names=("<b>Motor</b> & gear",))
    form = _form(client, sid)
    _post(client, sid, form, [form["options"][0][0]])
    for raw in (client.get(PREP % sid).get_data(as_text=True), client.get(PCI % sid).get_data(as_text=True),
                client.get(REPORT % sid).get_data(as_text=True)):
        assert "<b>Motor</b>" not in raw and "&lt;b&gt;Motor&lt;/b&gt; &amp; gear" in raw
    report = client.get(REPORT % sid).get_data(as_text=True)
    assert re.search(r'<bdi dir="auto" data-ifc-participant>&lt;b&gt;', report)


def test_v03_the_report_uses_one_snapshot_and_refuses_a_mismatched_one(client, monkeypatch):
    sid = _web_project(client)
    form = _form(client, sid)
    _post(client, sid, form, [form["options"][0][0]])
    store = _store()
    real = store.load_parts_components_interactions
    calls = []

    def spy(project_id):
        calls.append(project_id)
        return real(project_id)
    monkeypatch.setattr(store, "load_parts_components_interactions", spy)
    client.get(REPORT % sid)
    assert calls == [sid]
    calls.clear()
    _pdf_source(client, sid, monkeypatch)
    assert calls == [sid]

    def mismatched(project_id):
        record = dict(real(project_id))
        ifc = record["interfaces"][0]
        record["interfaces"] = (sm.SubsystemInterface(
            interface_id=ifc.interface_id, subsystem_a_id=ifc.subsystem_a_id,
            subsystem_b_id=ifc.subsystem_b_id, description="Something else",
            provenance=ifc.provenance, validation_state=ifc.validation_state),)
        return record
    monkeypatch.setattr(store, "load_parts_components_interactions", mismatched)
    report = client.get(REPORT % sid).get_data(as_text=True)
    assert "data-ifc-participation-unavailable" in report and "data-ifc-participants>" not in report

    def broken(project_id):
        raise ProjectNotFound(project_id)
    monkeypatch.setattr(store, "load_parts_components_interactions", broken)
    report = client.get(REPORT % sid).get_data(as_text=True)
    assert "data-ifc-participation-unavailable" in report


def test_v04_no_interaction_means_no_line_and_ordinary_projects_are_unchanged(client):
    sid = _integrated(client)
    report = client.get(REPORT % sid).get_data(as_text=True)
    assert "data-interface-participation" not in report and "data-ifc-participation-boundary" not in report
    raw = client.get(PREP % sid).get_data(as_text=True)
    assert "data-icp-form" not in raw


# ==========================================================================
# 5. Isolation: export, safety, readiness, state and the existing preparation save
# ==========================================================================
def test_x01_export_safety_readiness_and_state_are_unchanged(monkeypatch):
    from tests.test_stage19_durable_success_criteria import _client_for
    appmod.app.config["TESTING"] = True
    c, _aid = _client_for("icp-isolation@example.com")
    sid = _web_project(c, names=("Hinge motor overheating fire hazard", "Driver board"))
    stamp = re.compile(rb"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z")
    export = "/account/projects/%s/disclosure-export/json" % sid
    before_export = stamp.sub(b"", c.get(export).data)
    before_report = c.get(REPORT % sid).get_data(as_text=True)
    c.get(f"/session/{sid}")                                                     # consume one-shot acks
    before_session = c.get(f"/session/{sid}").get_data(as_text=True)
    before_state = pickle.dumps(appmod.SESSION_STORE[sid]["state"])
    form = _form(c, sid)
    _post(c, sid, form, [i for i, _ch in form["options"]])
    assert stamp.sub(b"", c.get(export).data) == before_export
    after_report = c.get(REPORT % sid).get_data(as_text=True)

    def safety(raw):
        m = re.search(r'<div[^>]*class="safety-signals".*?</div>', raw, re.S)
        return m.group(0) if m else None
    assert safety(before_report) and safety(after_report) == safety(before_report)
    strip = re.compile(r'<div data-interface-participation.*?</div>', re.S)
    assert _strip(strip.sub("", after_report)) == _strip(strip.sub("", before_report))
    hidden = re.compile(r'<input type="hidden"[^>]*>')                         # per-render tokens only
    # IDEA-DESIGN-UNDERSTANDING-PROJECTION-01: the session page's read-only
    # design-understanding picture presents the CURRENT participation rows by
    # component name (an identity-bound link the owner holds), so that one
    # block legitimately changes after a participation write; everything else
    # on the page must stay identical.
    picture = re.compile(r'<details id="design-understanding".*?</details>', re.S)

    def session(raw):
        return hidden.sub("", picture.sub("", raw))
    assert session(c.get(f"/session/{sid}").get_data(as_text=True)) == session(before_session)
    assert pickle.dumps(appmod.SESSION_STORE[sid]["state"]) == before_state      # IdeaState untouched


def test_x02_the_existing_preparation_save_ignores_participation_fields(client):
    sid = _web_project(client)
    form = _form(client, sid)
    ifc = form["interface"]
    r = client.post(PREP % sid, data={"participant": [form["options"][0][0]], "interface_id": ifc,
                                      "participant_base": ""})
    assert r.status_code == 200 and _rows(sid) == []


# ==========================================================================
# 6. Copy
# ==========================================================================
def test_c01_every_key_is_bilingual_and_the_boundary_claims_nothing():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_ICP_")]
    assert len(keys) == 21
    for key in keys:
        assert ui_text.has_string(key), key
    boundary = _t("UI_ICP_BOUNDARY").lower()
    for word in ("own statement", "not checked", "connect", "fit", "work together", "complete", "safe",
                 "assemble"):
        assert word in boundary
    for lang in ("en", "ar"):                    # internal provenance tokens are never visible text
        assert "OWNER_STATED" not in _t("UI_ICP_BOUNDARY", lang) and "UNVALIDATED" not in _t(
            "UI_ICP_BOUNDARY", lang)


def test_c02_arabic_pages_are_rtl_with_isolated_inventor_text(client):
    sid = _web_project(client, names=("محرك المفصلة",))
    form = _form(client, sid)
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    r = _post(client, sid, form, [form["options"][0][0]])
    page = r.get_data(as_text=True)
    assert 'dir="rtl"' in page and _t("UI_ICP_MSG_SAVED", "ar") in _html.unescape(page)
    assert _t("UI_ICP_HEADING", "ar") in _html.unescape(page)
    report = _html.unescape(client.get(REPORT % sid).get_data(as_text=True))
    assert _t("UI_ICP_LABEL", "ar") + " محرك المفصلة" in re.sub(r"<[^>]+>", "", report)
    assert _t("UI_ICP_BOUNDARY", "ar") in report
