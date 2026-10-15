"""COMPONENT-PROTOTYPE-NEED-NOTE-01 — the inventor's prototype-need note for ONE declared component.

For ONE existing ACTIVE declared component the inventor may record, view, replace and clear ONE optional,
free-text planning statement of what they expect to need of that component for ONE prototype. What is
pinned:
  * semantics (``engine/subsystem_model.py``): a current-value attribute keyed ONLY by the stable
    ``component_id``; the bounded text policy of the existing quantity-text discipline (outer trim, C0 / C1
    control characters rejected, at most 120 code points, nothing parsed); OWNER_STATED / UNVALIDATED;
    absence = NOT STATED (never a default of one); ``ProjectComponent`` identity and revision material
    unchanged; a withdrawn component's note is never a current need;
  * persistence (``engine/record_store.py``): ONE additive current-value sidecar
    ``component_prototype_needs`` (composite foreign key to the exact declaration row; upsert / delete; no
    history); whole-collection validation with the whole inventory; project, membership, active status,
    stale baseline and exact retry decided inside ONE serialized write transaction; the component tables,
    correction quota and the active / lifetime bounds untouched;
  * web (``web/app.py``): ONE POST route behind the central project authorization and the CSRF guard, the
    F724-1 baseline discipline, SAVED / NOT SAVED / UNKNOWN by committed truth; ONE display / entry surface
    in the session page's Component Inventory, EN / AR;
  * no IdeaState, Stage 35 export, Parts / Components / Interactions view, readiness, evidence,
    progression, gap or SafetySignal effect; no count, total, grouping or matching. The report / PDF
    exclusion of this slice is intentionally ADVANCED by COMPONENT-PROTOTYPE-NEED-HANDOFF-01: the current
    note now appears beside its component inside the report / PDF "declared components" section only
    (pinned in ``tests/test_component_deliverable_value.py``); everywhere else the report is unchanged.
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
from engine import requirement_quantity as rq
from engine import subsystem_model as sm
from engine.idea_state import OWNER_STATED, UNVALIDATED
from engine.record_store import (
    COMPONENT_PROTOTYPE_NEED_CLEARED, COMPONENT_PROTOTYPE_NEED_SAVED,
    COMPONENT_PROTOTYPE_NEED_UNCHANGED, ComponentPrototypeNeedRejected,
    ComponentPrototypeNeedStale, ComponentPrototypeNeedWithdrawn, ComponentPrototypeNeedsCorrupt,
    ProjectNotFound, RecordStoreConnectionUnsafe, SqliteRecordStore)
from tests.csrf_client import csrf_client
from tests.test_component_inventory_correct_withdraw import _correct, _withdraw
from tests.test_component_inventory_declare_list import (
    _block, _declare, _integrated, _ordinary, _page, _stable, _components_section,
    _outside_components_section)
from tests.test_stage15_integrated_invention_entry import (
    MECH, _CommitAndRollbackFail, _contract, _pair, _ri, _visible)
from tests.test_stage15_subsystem_interface_declaration import _FailOn, _restart
from web import ui_text

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SECRET = "Zq-prototype-need-5527"
WHEELS = "I expect to need four similar wheel units for one prototype."
_NEED_RE = re.compile(
    r'<form method="POST" action="/session/[^"]+/component-prototype-need" data-ci-need-form.*?</form>',
    re.S)


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


def _needs(pid):
    return _raw("SELECT component_id, need_text FROM component_prototype_needs "
                "WHERE project_id = ? ORDER BY component_id", (pid,))


def _new_project(store, integrated=True):
    subs = _pair() if integrated else ()
    pid = store.create_project(_contract(), reconstruction_inputs=_ri(MECH),
                               subsystems=subs or None)
    return pid, tuple(subs)


def _declare_store(store, pid, subs, name, function="Does a thing", key=None):
    item = sm.declared_component(subs, name, function, ())
    store.append_project_component(pid, item, key or ("k-" + name))
    return item


def _need_forms(raw):
    """Every rendered prototype-need form of the page, in list order, as dicts."""
    forms = []
    for form in _NEED_RE.findall(raw):
        def value(name):
            m = re.search(r'name="%s" value="([^"]*)"' % name, form)
            return _html.unescape(m.group(1)) if m else None
        forms.append({"id": value("component_id"), "base": value("need_base"),
                      "text": value("need_text"), "has_clear": 'value="clear"' in form})
    return forms


def _post_need(c, sid, form, text=None, action="save", **override):
    data = {"component_id": form["id"], "need_base": form["base"], "need_action": action,
            "need_text": form["text"] if text is None else text}
    data.update(override)
    return c.post(f"/session/{sid}/component-prototype-need", data=data)


def _notice(sid):
    entry = appmod.SESSION_STORE[sid]
    return entry.get(appmod.COMPONENT_ACK_SLOT), entry.get(appmod.COMPONENT_ERROR_SLOT)


def _first_form(c, sid):
    forms = _need_forms(_page(c, sid))
    assert forms, "no prototype-need form rendered"
    return forms[0]


# ==========================================================================
# 1. Semantic owner
# ==========================================================================
@pytest.mark.parametrize("raw,stored", [
    ("  four similar wheel units  ", "four similar wheel units"),
    ("4", "4"),                                         # never parsed as a number
    ("four", "four"),
    ("أربع وحدات عجلات متشابهة", "أربع وحدات عجلات متشابهة"),
    ("x" * 120, "x" * 120),
    ("🛞" * 120, "🛞" * 120),                           # code points, not bytes
])
def test_m01_the_bounded_text_policy_keeps_the_inventors_words(raw, stored):
    assert sm.normalize_prototype_need_text(raw) == stored
    assert sm.is_stored_prototype_need_text(stored)


@pytest.mark.parametrize("raw", [
    "", "   ", None, 4, "x" * 121, "two\nunits", "two\tunits", "two\x00units", "two\x7funits",
    "two\x85units", "two\x9funits", "\r\n",
])
def test_m02_empty_controls_overlong_and_non_text_are_rejected_never_repaired(raw):
    with pytest.raises(sm.ComponentPrototypeNeedError):
        sm.normalize_prototype_need_text(raw)
    assert not sm.is_stored_prototype_need_text(raw)


@pytest.mark.parametrize("raw", [
    "  four units ", "4", "x" * 120, "x" * 121, "", "a\nb", "a\x85b", "a\x7fb", "عجلات", "a​b",
])
def test_m03_the_policy_is_exactly_the_existing_quantity_text_discipline(raw):
    def outcome(fn, err):
        try:
            return ("ok", fn(raw))
        except err:
            return ("rejected", None)
    assert sm.MAX_COMPONENT_PROTOTYPE_NEED_LENGTH == rq.MAX_VALUE_TEXT_CHARS == 120
    assert outcome(sm.normalize_prototype_need_text, sm.ComponentPrototypeNeedError) == outcome(
        rq.normalize_value_text, rq.QuantityValueError)


def test_m04_component_identity_and_revision_material_are_unchanged():
    from dataclasses import fields
    assert [f.name for f in fields(sm.ProjectComponent)] == [
        "component_id", "display_name", "function_text", "subsystem_ids", "provenance",
        "validation_state"]
    assert [f.name for f in fields(sm.ComponentRevision)] == [
        "revision_id", "component_id", "revision_no", "kind", "display_name", "function_text",
        "subsystem_ids", "provenance", "validation_state"]
    need = sm.ComponentPrototypeNeed("cmp-" + "0" * 32, "two units")
    assert (need.provenance, need.validation_state) == (OWNER_STATED, UNVALIDATED)
    assert [f.name for f in fields(sm.ComponentPrototypeNeed)] == [
        "component_id", "need_text", "provenance", "validation_state"]


def test_m05_validation_is_whole_and_withdrawn_notes_are_history_not_current():
    subs = _pair()
    a = sm.declared_component(subs, "Wheel", "Rolls", ())
    b = sm.declared_component(subs, "Wheel", "Rolls", ())        # equal names: two identities
    inv = sm.project_component_inventory((a, b), (), subs)
    wd = sm.withdrawn_component_revision(inv, b.component_id, 0)
    inv2 = sm.project_component_inventory((a, b), (wd,), subs)
    na, nb = (sm.ComponentPrototypeNeed(a.component_id, "four units"),
              sm.ComponentPrototypeNeed(b.component_id, "two units"))
    assert sm.validate_component_prototype_needs((nb, na), inv2) == (na, nb)   # declaration order
    assert sm.current_prototype_needs((na, nb), inv2) == {a.component_id: "four units"}
    assert sm.validate_component_prototype_needs((), inv2) == ()
    for bad in ((na, na),                                                        # duplicate
                (sm.ComponentPrototypeNeed("cmp-" + "1" * 32, "x"),),           # orphan
                (sm.ComponentPrototypeNeed(a.component_id, " padded "),),       # not stored form
                (sm.ComponentPrototypeNeed(a.component_id, "a\nb"),),
                (sm.ComponentPrototypeNeed(a.component_id, "x", provenance="SYSTEM_INFERRED"),),
                (sm.ComponentPrototypeNeed(a.component_id, "x", validation_state="VALIDATED"),),
                ("not a need",)):
        with pytest.raises(sm.ComponentPrototypeNeedError):
            sm.validate_component_prototype_needs(bad, inv2)
    assert sm.prototype_need_target(inv2, a.component_id).component_id == a.component_id
    with pytest.raises(sm.ComponentAlreadyWithdrawn):
        sm.prototype_need_target(inv2, b.component_id)
    with pytest.raises(sm.ComponentUnknown):
        sm.prototype_need_target(inv2, "cmp-" + "2" * 32)


# ==========================================================================
# 2. Persistence owner
# ==========================================================================
def test_s01_set_replace_clear_retry_and_no_default(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "n.db"))
    pid, subs = _new_project(store)
    comp = _declare_store(store, pid, subs, "Wheel")
    inv, needs = store.load_component_prototype_needs(pid)
    assert needs == () and sm.current_prototype_needs(needs, inv) == {}   # NOT STATED, no "1"
    cid = comp.component_id
    assert store.set_component_prototype_need(pid, cid, "four units", None) == \
        COMPONENT_PROTOTYPE_NEED_SAVED
    assert store.set_component_prototype_need(pid, cid, "four units", None) == \
        COMPONENT_PROTOTYPE_NEED_UNCHANGED                                  # exact retry: no write
    assert store.set_component_prototype_need(pid, cid, "five units", "four units") == \
        COMPONENT_PROTOTYPE_NEED_SAVED
    _inv, needs = store.load_component_prototype_needs(pid)
    assert needs == (sm.ComponentPrototypeNeed(cid, "five units"),)
    assert store.set_component_prototype_need(pid, cid, None, "five units") == \
        COMPONENT_PROTOTYPE_NEED_CLEARED
    assert store.set_component_prototype_need(pid, cid, None, "five units") == \
        COMPONENT_PROTOTYPE_NEED_UNCHANGED
    assert store.load_component_prototype_needs(pid)[1] == ()
    rows = store._conn.execute("SELECT COUNT(*) FROM component_prototype_needs").fetchone()[0]
    assert rows == 0


def test_s02_a_stale_baseline_never_overwrites_a_newer_note(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "n.db"))
    pid, subs = _new_project(store)
    cid = _declare_store(store, pid, subs, "Wheel").component_id
    store.set_component_prototype_need(pid, cid, "four units", None)
    for target, expected in (("six units", None), ("six units", "two units"), (None, None)):
        with pytest.raises(ComponentPrototypeNeedStale):
            store.set_component_prototype_need(pid, cid, target, expected)
    assert store.load_component_prototype_needs(pid)[1] == (
        sm.ComponentPrototypeNeed(cid, "four units"),)


def test_s03_membership_withdrawal_project_and_text_are_decided_before_any_write(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "n.db"))
    pid, subs = _new_project(store)
    other, osubs = _new_project(store)
    cid = _declare_store(store, pid, subs, "Wheel").component_id
    foreign = _declare_store(store, other, osubs, "Lid").component_id
    for args, exc in (
            ((pid, foreign, "x", None), ComponentPrototypeNeedRejected),       # another project's
            ((pid, "cmp-" + "3" * 32, "x", None), ComponentPrototypeNeedRejected),
            ((pid, "", "x", None), ComponentPrototypeNeedRejected),
            ((pid, cid, " padded ", None), ComponentPrototypeNeedRejected),    # not stored form
            ((pid, cid, "a\nb", None), ComponentPrototypeNeedRejected),
            ((pid, cid, "x" * 121, None), ComponentPrototypeNeedRejected),
            ((pid, cid, "x", "a\x00b"), ComponentPrototypeNeedRejected),
            (("no-such-project", cid, "x", None), ProjectNotFound)):
        with pytest.raises(exc):
            store.set_component_prototype_need(*args)
    _withdraw(store, pid, cid, 0)
    with pytest.raises(ComponentPrototypeNeedWithdrawn):
        store.set_component_prototype_need(pid, cid, "x", None)
    assert store._conn.execute("SELECT COUNT(*) FROM component_prototype_needs").fetchone()[0] == 0


def test_s04_correction_keeps_withdrawal_hides_and_redeclaration_inherits_nothing(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "n.db"))
    pid, subs = _new_project(store)
    cid = _declare_store(store, pid, subs, "Wheel").component_id
    store.set_component_prototype_need(pid, cid, "four units", None)
    _correct(store, pid, cid, 0, "Drive wheel")
    inv, needs = store.load_component_prototype_needs(pid)
    assert inv.record_for(cid).current.display_name == "Drive wheel"
    assert sm.current_prototype_needs(needs, inv) == {cid: "four units"}          # same id -> kept
    _withdraw(store, pid, cid, 1)
    inv, needs = store.load_component_prototype_needs(pid)
    assert sm.current_prototype_needs(needs, inv) == {}                           # never current
    assert needs == (sm.ComponentPrototypeNeed(cid, "four units"),)              # kept as stored
    again = _declare_store(store, pid, subs, "Drive wheel", key="k-again").component_id
    inv, needs = store.load_component_prototype_needs(pid)
    assert again != cid and again not in sm.current_prototype_needs(needs, inv)


def test_s05_identity_quotas_and_capacity_bounds_are_untouched(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "n.db"))
    pid, subs = _new_project(store)
    cid = _declare_store(store, pid, subs, "Wheel").component_id
    before = store.load_component_inventory_record(pid)
    comp_rows = store._conn.execute(
        "SELECT * FROM project_components WHERE project_id = ?", (pid,)).fetchall()
    for n in range(5):
        store.set_component_prototype_need(
            pid, cid, "units %d" % n, None if n == 0 else "units %d" % (n - 1))
    after = store.load_component_inventory_record(pid)
    assert after == before
    record = after[1].record_for(cid)
    assert (record.head_revision_no, record.corrections, after[1].declared_count) == (0, 0, 1)
    assert store._conn.execute("SELECT * FROM project_components WHERE project_id = ?",
                               (pid,)).fetchall() == comp_rows
    assert store._conn.execute("SELECT COUNT(*) FROM project_component_revisions").fetchone()[0] == 0


def test_s06_migration_is_additive_idempotent_and_refuses_an_unknown_shape(tmp_path):
    path = str(tmp_path / "m.db")
    store = SqliteRecordStore(path)
    pid, subs = _new_project(store)
    cid = _declare_store(store, pid, subs, "Wheel").component_id
    store.set_component_prototype_need(pid, cid, "four units", None)
    store.close()
    # A database written BEFORE this capability: the table does not exist yet.
    conn = sqlite3.connect(path)
    conn.execute("DROP TABLE component_prototype_needs")
    conn.commit()
    conn.close()
    store = SqliteRecordStore(path)                  # created additively; components intact
    inv, needs = store.load_component_prototype_needs(pid)
    assert needs == () and [c.component_id for c in inv.active] == [cid]
    store.close()
    SqliteRecordStore(path).close()                  # idempotent reopen
    conn = sqlite3.connect(path)
    conn.execute("DROP TABLE component_prototype_needs")
    conn.execute("CREATE TABLE component_prototype_needs (project_id TEXT, component_id TEXT, "
                 "quantity INTEGER)")
    conn.commit()
    conn.close()
    with pytest.raises(sqlite3.DatabaseError):
        SqliteRecordStore(path)


def test_s07_the_database_backstop_and_the_whole_collection_validation(tmp_path):
    path = str(tmp_path / "c.db")
    store = SqliteRecordStore(path)
    pid, subs = _new_project(store)
    cid = _declare_store(store, pid, subs, "Wheel").component_id
    with pytest.raises(sqlite3.IntegrityError):                   # FK: no such component
        store._conn.execute("INSERT INTO component_prototype_needs VALUES (?, ?, ?)",
                            (pid, "cmp-" + "4" * 32, "x"))
    for text in ("", "x" * 121, "a\x00b", b"bytes"):
        with pytest.raises(sqlite3.IntegrityError):
            store._conn.execute("INSERT INTO component_prototype_needs VALUES (?, ?, ?)",
                                (pid, cid, text))
    store._conn.execute("INSERT INTO component_prototype_needs VALUES (?, ?, ?)",
                        (pid, cid, "two\nunits"))                 # passes the backstop only
    with pytest.raises(ComponentPrototypeNeedsCorrupt):
        store.load_component_prototype_needs(pid)
    with pytest.raises(ComponentPrototypeNeedsCorrupt):
        store.set_component_prototype_need(pid, cid, "x", None)
    store._conn.execute("UPDATE component_prototype_needs SET need_text = ' padded '")
    with pytest.raises(ComponentPrototypeNeedsCorrupt):
        store.load_component_prototype_needs(pid)
    # the inventory itself still reads (the notes fail closed on their own)
    assert [c.component_id for c in store.load_component_inventory_record(pid)[1].active] == [cid]


def test_s08_failed_and_unresolved_writes_roll_back_and_refuse_reads(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "f.db"))
    pid, subs = _new_project(store)
    cid = _declare_store(store, pid, subs, "Wheel").component_id
    real = store._conn
    store._conn = _FailOn(real, prefix="INSERT INTO component_prototype_needs")
    with pytest.raises(sqlite3.OperationalError):
        store.set_component_prototype_need(pid, cid, "four units", None)
    store._conn = real
    assert store.load_component_prototype_needs(pid)[1] == ()
    store._conn = _CommitAndRollbackFail(real)
    with pytest.raises(sqlite3.OperationalError):
        store.set_component_prototype_need(pid, cid, "four units", None)
    store._conn = real
    with pytest.raises(RecordStoreConnectionUnsafe):
        store.load_component_prototype_needs(pid)
    with pytest.raises(RecordStoreConnectionUnsafe):
        store.set_component_prototype_need(pid, cid, "four units", None)


def test_s09_concurrent_writers_from_one_baseline_never_both_win(tmp_path):
    path = str(tmp_path / "race.db")
    seed = SqliteRecordStore(path)
    pid, subs = _new_project(seed)
    cid = _declare_store(seed, pid, subs, "Wheel").component_id
    seed.close()
    writers = 4
    barrier = threading.Barrier(writers)
    results = []

    def run(i):
        store = SqliteRecordStore(path)          # one connection per thread
        try:
            barrier.wait()
            results.append(store.set_component_prototype_need(pid, cid, "units %d" % i, None))
        except ComponentPrototypeNeedStale:
            results.append("STALE")
        except sqlite3.OperationalError:
            results.append("BUSY")
        finally:
            store.close()
    threads = [threading.Thread(target=run, args=(i,)) for i in range(writers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(results) == writers
    assert results.count(COMPONENT_PROTOTYPE_NEED_SAVED) == 1
    assert set(results) <= {COMPONENT_PROTOTYPE_NEED_SAVED, "STALE", "BUSY"}
    check = SqliteRecordStore(path)
    [stored] = check.load_component_prototype_needs(pid)[1]
    assert stored.need_text in {"units %d" % i for i in range(writers)}
    check.close()


# ==========================================================================
# 3. Web: the session page's Component Inventory surface and the POST route
# ==========================================================================
def test_w01_record_view_replace_and_clear_on_the_session_page(client):
    sid = _integrated(client)
    _declare(client, sid, name="Wheel", function="Rolls the cart")
    raw = _page(client, sid)
    block = _block(raw)
    assert "data-ci-need-none" in block and ui_text.text("UI_CI_NEED_NOT_STATED", "en") in block
    [form] = _need_forms(raw)
    assert form["base"] == "" and form["text"] == "" and not form["has_clear"]
    assert form["id"] not in _visible(block)                         # id is a form value only
    _post_need(client, sid, form, text="  " + WHEELS + "  ")
    assert _notice(sid) == ("UI_CI_NEED_MSG_SAVED", None)
    assert _needs(sid) == [(form["id"], WHEELS)]
    block = _block(_page(client, sid))
    assert '<bdi dir="auto" data-ci-need-text>%s</bdi>' % _html.escape(WHEELS) in block
    assert "data-ci-need-status" in block and "data-ci-need-none" not in block
    form = _first_form(client, sid)
    assert form["base"] == WHEELS and form["has_clear"]
    _post_need(client, sid, form, text="Two wheel units for the first test rig")
    assert _notice(sid) == ("UI_CI_NEED_MSG_SAVED", None)
    assert _needs(sid) == [(form["id"], "Two wheel units for the first test rig")]
    _post_need(client, sid, _first_form(client, sid), action="clear", text="")
    assert _notice(sid) == ("UI_CI_NEED_MSG_CLEARED", None)
    assert _needs(sid) == []
    block = _block(_page(client, sid))
    assert "data-ci-need-none" in block and "Wheel" in _visible(block)        # component stays


def test_w02_each_note_belongs_to_its_own_component_by_identity(client):
    sid = _integrated(client)
    _declare(client, sid, name="Wheel", function="Rolls")
    _declare(client, sid, name="Wheel", function="Rolls")             # equal names, two identities
    first, second = _need_forms(_page(client, sid))
    assert first["id"] != second["id"]
    _post_need(client, sid, second, text="four similar wheel units")
    rows = _needs(sid)
    assert rows == [(second["id"], "four similar wheel units")]
    first, second = _need_forms(_page(client, sid))
    assert (first["base"], second["base"]) == ("", "four similar wheel units")


@pytest.mark.parametrize("text,key", [
    ("", "UI_CI_NEED_MSG_EMPTY"),
    ("   ", "UI_CI_NEED_MSG_EMPTY"),
    ("x" * 121, "UI_CI_NEED_MSG_TOO_LONG"),
    ("two\nunits", "UI_CI_NEED_MSG_INVALID_CHAR"),
    ("two\x85units", "UI_CI_NEED_MSG_INVALID_CHAR"),
    ("two\x00units", "UI_CI_NEED_MSG_INVALID_CHAR"),
])
def test_w03_invalid_text_is_rejected_never_truncated_or_repaired(client, text, key):
    sid = _integrated(client)
    _declare(client, sid, name="Wheel", function="Rolls")
    _post_need(client, sid, _first_form(client, sid), text=text)
    assert _notice(sid) == (None, key) and _needs(sid) == []


@pytest.mark.parametrize("override", [
    {"component_id": "cmp-NOT-AN-ID"},
    {"need_action": "delete"},
    {"need_action": ""},
    {"need_base": ["", ""]},
    {"need_base": "two\nunits"},
    {"need_base": " padded "},
])
def test_w04_malformed_forms_are_rejected_and_write_nothing(client, override):
    sid = _integrated(client)
    _declare(client, sid, name="Wheel", function="Rolls")
    form = _first_form(client, sid)
    data = {"component_id": form["id"], "need_base": "", "need_action": "save",
            "need_text": "four units"}
    data.update(override)
    client.post(f"/session/{sid}/component-prototype-need", data=data)
    assert _notice(sid) == (None, "UI_CI_NEED_MSG_REJECTED") and _needs(sid) == []
    missing = {k: v for k, v in data.items() if k != "need_base"}
    missing["need_action"] = "save"
    missing["component_id"] = form["id"]
    client.post(f"/session/{sid}/component-prototype-need", data=missing)
    assert _notice(sid) == (None, "UI_CI_NEED_MSG_REJECTED") and _needs(sid) == []


def test_w05_stale_form_retry_and_unchanged_submissions(client):
    sid = _integrated(client)
    _declare(client, sid, name="Wheel", function="Rolls")
    old = _first_form(client, sid)
    _post_need(client, sid, old, text="four units")
    _post_need(client, sid, old, text="four units")                  # exact retry / double submit
    assert _notice(sid) == ("UI_CI_NEED_MSG_SAVED", None)
    assert _needs(sid) == [(old["id"], "four units")]
    _post_need(client, sid, old, text="six units")                   # the form is now stale
    assert _notice(sid) == (None, "UI_CI_NEED_MSG_STALE")
    _post_need(client, sid, old, action="clear", text="")            # a stale clear removes nothing
    assert _notice(sid) == ("UI_CI_NEED_MSG_UNCHANGED", None)        # (target == its own baseline)
    assert _needs(sid) == [(old["id"], "four units")]
    current = _first_form(client, sid)
    _post_need(client, sid, current, text="four units")
    assert _notice(sid) == ("UI_CI_NEED_MSG_UNCHANGED", None)
    assert _needs(sid) == [(old["id"], "four units")]


def test_w06_authorization_csrf_and_foreign_components(client):
    from tests.test_commercial_evidence_capture import _client_for
    owner, _aid = _client_for("cpn-owner@example.com")
    sid = _integrated(owner)
    _declare(owner, sid, name="Wheel", function="Rolls")
    form = _first_form(owner, sid)
    intruder, _bid = _client_for("cpn-intruder@example.com")
    r = _post_need(intruder, sid, form, text=SECRET)
    assert r.status_code in (302, 403, 404) and SECRET not in r.get_data(as_text=True)
    raw_client = appmod.app.test_client()                            # no CSRF token
    r = raw_client.post(f"/session/{sid}/component-prototype-need", data={
        "component_id": form["id"], "need_base": "", "need_action": "save", "need_text": SECRET})
    assert r.status_code == 403
    assert _needs(sid) == []
    other = _integrated(owner)
    _declare(owner, other, name="Lid", function="Covers")
    foreign = _first_form(owner, other)
    _post_need(owner, sid, dict(form, id=foreign["id"]), text=SECRET)
    assert _notice(sid) == (None, "UI_CI_NEED_MSG_REJECTED")
    assert _needs(sid) == [] and _needs(other) == []


def test_w07_a_withdrawn_component_shows_no_need_and_takes_none(client):
    sid = _integrated(client)
    _declare(client, sid, name=SECRET, function="Rolls")
    form = _first_form(client, sid)
    _post_need(client, sid, form, text="four units")
    _withdraw(_store(), sid, form["id"], 0)
    raw = _page(client, sid)
    assert "four units" not in raw and _need_forms(raw) == []
    _post_need(client, sid, dict(form, base="four units"), text="six units")
    assert _notice(sid) == (None, "UI_CI_NEED_MSG_WITHDRAWN")
    assert _needs(sid) == [(form["id"], "four units")]                # stored, never current


def test_w08_failed_uncertain_and_unresolved_commits_are_truthful(client):
    sid = _integrated(client)
    _declare(client, sid, name="Wheel", function="Rolls")
    store = _store()
    real = store._conn
    store._conn = _FailOn(real, prefix="INSERT INTO component_prototype_needs")
    _post_need(client, sid, _first_form(client, sid), text="four units")
    store._conn = real
    assert _needs(sid) == [] and _notice(sid) == (None, "UI_CI_NEED_MSG_NOT_SAVED")
    form = _first_form(client, sid)
    store._conn = _FailOn(real, commit_then=True)                    # committed, then raised
    _post_need(client, sid, form, text="four units")
    store._conn = real
    assert _needs(sid) == [(form["id"], "four units")]
    assert _notice(sid) == ("UI_CI_NEED_MSG_SAVED", None)
    store._conn = _CommitAndRollbackFail(real)                        # unresolved
    _post_need(client, sid, _first_form(client, sid), text="six units")
    store._conn = real
    assert _notice(sid) == (None, "UI_CI_NEED_MSG_UNKNOWN")
    _restart()                                                        # drop the unresolved handle
    assert _needs(sid) == [(form["id"], "four units")]


def test_w09_unreadable_notes_read_unavailable_never_not_stated(client):
    sid = _integrated(client)
    _declare(client, sid, name="Wheel", function="Rolls")
    form = _first_form(client, sid)
    _post_need(client, sid, form, text="four units")
    _raw("UPDATE component_prototype_needs SET need_text = ? WHERE project_id = ?",
         ("two\nunits " + SECRET, sid))
    raw = _page(client, sid)
    block = _block(raw)
    assert 'data-ci-status="available"' in block and "Wheel" in _visible(block)
    assert "data-ci-need-unavailable" in block and "data-ci-need-none" not in block
    assert _need_forms(raw) == [] and SECRET not in raw
    _post_need(client, sid, dict(form, base="four units"), text="six units")
    assert _notice(sid) == (None, "UI_CI_NEED_MSG_NOT_SAVED")


def test_w10_the_note_survives_restart_and_a_correction(client):
    sid = _integrated(client)
    _declare(client, sid, name="Wheel", function="Rolls")
    form = _first_form(client, sid)
    _post_need(client, sid, form, text="four units")
    _restart()
    assert _first_form(client, sid)["base"] == "four units"
    _correct(_store(), sid, form["id"], 0, "Drive wheel")
    block = _block(_page(client, sid))
    assert "Drive wheel" in _visible(block) and "four units" in _visible(block)


def test_w11_arabic_rtl_copy_and_inventor_text_isolation(client):
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    sid = _ordinary(client)
    _declare(client, sid, name="عجلة", function="تدحرج العربة")
    _post_need(client, sid, _first_form(client, sid), text="<script>alert(1)</script>")
    raw = _page(client, sid)
    block = _block(raw)
    for key in ("UI_CI_NEED_LABEL", "UI_CI_NEED_STATUS", "UI_CI_NEED_SUMMARY_CHANGE",
                "UI_CI_NEED_HINT", "UI_CI_NEED_FIELD", "UI_CI_NEED_SAVE_BUTTON",
                "UI_CI_NEED_CLEAR_BUTTON", "UI_CI_NEED_MSG_SAVED"):
        assert ui_text.text(key, "ar") in _html.unescape(block), key
    assert "<script>alert(1)</script>" not in raw
    assert '<bdi dir="auto" data-ci-need-text>&lt;script&gt;' in block
    assert 'dir="rtl"' in raw


def test_w12_every_need_key_has_english_and_arabic_copy_and_claims_nothing():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_CI_NEED_")]
    assert len(keys) == 22
    for key in keys:
        assert ui_text.has_string(key), key
        en = ui_text.text(key, "en").lower()
        for claim in ("verified requirement.", "validated.", "bill of materials", " bom",
                      "total:", "in stock"):
            assert claim not in en, (key, claim)
    hint = ui_text.text("UI_CI_NEED_HINT", "en")
    assert "does not count, compare, total or check it" in hint
    assert "not a verified requirement or a parts list" in hint


# ==========================================================================
# 4. No effect beyond the note; no count, total or grouping anywhere
# ==========================================================================
def test_x01_no_state_report_pdf_view_export_or_progression_effect(client, monkeypatch, caplog):
    from tests.test_commercial_evidence_capture import _client_for
    from tests.test_stage15_integrated_invention_entry import _pdf_source
    owner, _aid = _client_for("cpn-x01@example.com")
    sid = _integrated(owner)
    _declare(owner, sid, name="Wheel", function="Rolls")
    report_before = owner.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    view_before = owner.get(f"/session/{sid}/parts-components-interactions").get_data(as_text=True)
    export_before = owner.get(f"/account/projects/{sid}/disclosure-export/json").get_data()
    state_before = pickle.dumps(appmod.SESSION_STORE[sid]["state"])
    with caplog.at_level("DEBUG"):
        _post_need(owner, sid, _first_form(owner, sid), text=SECRET)
    assert _needs(sid) and _notice(sid) == ("UI_CI_NEED_MSG_SAVED", None)
    assert pickle.dumps(appmod.SESSION_STORE[sid]["state"]) == state_before
    report = owner.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    # Advanced by COMPONENT-PROTOTYPE-NEED-HANDOFF-01: the note reaches the report / PDF ONLY inside the
    # declared-components section, beside its component; outside that section the report is unchanged.
    assert SECRET in _components_section(report)
    assert SECRET not in _outside_components_section(report)
    assert _stable(_outside_components_section(report)) == _stable(
        _outside_components_section(report_before))
    pdf = _pdf_source(owner, sid, monkeypatch)
    assert SECRET in _components_section(pdf) and "Wheel" in _components_section(pdf)
    assert SECRET not in _outside_components_section(pdf)
    view = owner.get(f"/session/{sid}/parts-components-interactions").get_data(as_text=True)
    assert SECRET not in view and _stable(view) == _stable(view_before)
    export_after = owner.get(f"/account/projects/{sid}/disclosure-export/json").get_data()
    stamp = re.compile(rb"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z")
    assert stamp.sub(b"", export_after) == stamp.sub(b"", export_before)
    assert SECRET.encode() not in export_after
    assert SECRET not in caplog.text
    for path in ("engine/read_export_service.py", "web/api_v1.py",
                 "engine/export_adapter.py", "engine/disclosure_export.py",
                 "engine/derived_readiness.py", "engine/readiness_snapshot.py",
                 "engine/safety_signal.py", "engine/session_reconstruction.py",
                 "engine/idea_state.py", "engine/deterministic_calculation.py",
                 "engine/deliverable_assembler.py", "engine/requirement_quantity.py",
                 "engine/commercial_evidence.py"):
        text = open(os.path.join(_ROOT, path), encoding="utf-8").read()
        assert "prototype_need" not in text and "PrototypeNeed" not in text, path


def test_x02_nothing_counts_totals_multiplies_or_groups_the_notes():
    src = open(os.path.join(_ROOT, "engine", "subsystem_model.py"), encoding="utf-8").read()
    section = src[src.index("# --- COMPONENT-PROTOTYPE-NEED-NOTE-01"):]
    code = "\n".join(line for line in section.splitlines()
                     if not line.lstrip().startswith("#") and '"""' not in line)
    for forbidden in ("int(", "float(", "Decimal", "sum(", "isdigit", "isnumeric", "groupby",
                      "lower()", "casefold"):
        assert forbidden not in code, forbidden
    app_src = open(os.path.join(_ROOT, "web", "app.py"), encoding="utf-8").read()
    route = app_src[app_src.index("# --- COMPONENT-PROTOTYPE-NEED-NOTE-01"):
                    app_src.index("# --- Stage 15 Slice 3: Interface Verification Preparation")]
    for forbidden in ("int(", "float(", "sum(", "isdigit", "display_name ==", "groupby"):
        assert forbidden not in route, forbidden


def test_x03_the_slice_reaches_no_report_pdf_or_export_template():
    # deliverable.html (the report AND the PDF) is intentionally ADVANCED by
    # COMPONENT-PROTOTYPE-NEED-HANDOFF-01 and pinned in tests/test_component_deliverable_value.py; it
    # carries the note read-only (no form, no data-ci-need marker). The other templates stay untouched.
    report_src = open(os.path.join(_ROOT, "web", "templates", "deliverable.html"), encoding="utf-8").read()
    assert "data-ci-need" not in report_src and "component-prototype-need" not in report_src
    for name in ("pdf_report.html", "pdf_base.html", "parts_components_interactions.html"):
        path = os.path.join(_ROOT, "web", "templates", name)
        if os.path.exists(path):
            text = open(path, encoding="utf-8").read()
            assert "need" not in re.findall(r"data-ci-need\w*", text), name
            assert "prototype_need" not in text and "UI_CI_NEED_" not in text, name
