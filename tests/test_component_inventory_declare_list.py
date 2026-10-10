"""COMPONENT-INVENTORY-DECLARE-LIST-01 — manual Component Inventory, declare and
list only.

The inventor declares the physical components their invention includes — ONE
record per component — and may link each to zero or more of the project's OWN
durable parts:

  * semantic owner ``engine/subsystem_model.py`` (``ProjectComponent``);
    persistence owner the record store (ONE additive ``project_components``
    sidecar, append-only; part references stored as a bounded canonical JSON
    array, re-validated against the durable composition inside the write
    transaction and on every load);
  * a system-generated, opaque, immutable ``component_id``; OWNER_STATED /
    UNVALIDATED; equal names never merge; an exact retry returns the committed
    component, the same submission identity with other material fails closed;
  * composition + inventory read under ONE snapshot; never in IdeaState, the
    accepted-input history or replay; no edit / delete;
  * session page only (EN / AR); report, PDF, exports, evidence, readiness,
    gaps, progression, SafetySignal and calculation eligibility unchanged.
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
    PROJECT_COMPONENT_EXACT_REPLAY, PROJECT_COMPONENT_INSERTED, ProjectNotFound,
    ProjectComponentConflict, ProjectComponentRejected, ProjectComponentsCorrupt,
    RecordStoreConnectionUnsafe, SqliteRecordStore)
from tests.csrf_client import csrf_client
from tests.test_stage15_integrated_invention_entry import (
    ELEC, ELEC_IDEA, MECH, PARTS, TIE_IDEA, _CommitAndRollbackFail, _compose,
    _contract, _created, _pair, _ri, _visible)
from tests.test_stage15_subsystem_interface_declaration import _FailOn, _restart
from web import ui_text

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
NAME = "Brushless DC motor"
FUNCTION = "Turns the hinge arm when the lid opens."
SECRET = "Zq-private-component-7731"


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


def _raw(sql, params=()):
    _store()
    conn = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        rows = conn.execute(sql, params).fetchall()
        conn.commit()
        return rows
    finally:
        conn.close()


def _rows(pid=None):
    if pid is None:
        return _raw("SELECT * FROM project_components")
    return _raw("SELECT * FROM project_components WHERE project_id = ? "
                "ORDER BY component_seq", (pid,))


def _page(c, sid):
    r = c.get(f"/session/{sid}")
    assert r.status_code == 200, r.status_code
    return r.get_data(as_text=True)


def _block(raw):
    m = re.search(r'<details id="component-inventory".*?</details>', raw, re.S)
    return m.group(0) if m else None


def _form(raw):
    m = re.search(r'name="component_submission" value="([^"]*)"', raw)
    return {"submission": _html.unescape(m.group(1)) if m else None,
            "parts": re.findall(r'name="component_part" value="([^"]*)"', raw)}


def _declare(c, sid, name=NAME, function=FUNCTION, parts=(), submission=None):
    if submission is None:
        submission = _form(_page(c, sid))["submission"]
    return c.post(f"/session/{sid}/declare-component", data={
        "component_submission": submission, "component_name": name,
        "component_function": function, "component_part": list(parts)})


def _notice(sid):
    entry = appmod.SESSION_STORE[sid]
    return entry.get(appmod.COMPONENT_ACK_SLOT), entry.get(appmod.COMPONENT_ERROR_SLOT)


def _ordinary(c):
    return _created(c.post("/start", data={"idea": ELEC_IDEA, "domain_confirm": ELEC}))


def _integrated(c, focus=MECH):
    return _created(_compose(c, TIE_IDEA, focus=focus))


def _new_store_project(store, integrated=True):
    subs = _pair() if integrated else ()
    pid = store.create_project(_contract(), reconstruction_inputs=_ri(MECH),
                               subsystems=subs or None)
    return pid, tuple(subs)


def _stable(report):
    """A report render with its per-render values masked: form token values and
    the package's second-resolution ``generated_at`` timestamp."""
    report = re.sub(r'value="[^"]*"', "", report)
    return re.sub(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:\d\d)?", "",
                  report)


def _component(subs=(), name=NAME, function=FUNCTION, parts=()):
    return sm.declared_component(subs, name, function, parts)


# ==========================================================================
# 1. Semantic owner
# ==========================================================================
def test_m01_a_declaration_is_one_owner_stated_unvalidated_component():
    subs = _pair()
    item = _component(subs, parts=(subs[1].subsystem_id, subs[0].subsystem_id))
    assert sm.is_valid_component_id(item.component_id)
    assert item.subsystem_ids == (subs[0].subsystem_id, subs[1].subsystem_id)
    assert (item.provenance, item.validation_state) == (OWNER_STATED, UNVALIDATED)
    plain = _component()
    assert plain.subsystem_ids == () and plain.component_id != item.component_id


def test_m02_invalid_text_and_references_are_rejected_never_repaired():
    subs = _pair()
    other = _pair()
    for name, function in (("", FUNCTION), (NAME, ""), (" x", FUNCTION),
                           ("a\x00b", FUNCTION), ("n" * 81, FUNCTION),
                           (NAME, "f" * 301)):
        with pytest.raises(sm.ComponentError):
            _component(subs, name=name, function=function)
    assert _component(subs, name="n" * 80, function="f" * 300).display_name == "n" * 80
    for parts in ((subs[0].subsystem_id, subs[0].subsystem_id),
                  (other[0].subsystem_id,)):
        with pytest.raises(sm.ComponentError):
            _component(subs, parts=parts)
    with pytest.raises(sm.ComponentError):
        _component((), parts=(subs[0].subsystem_id,))


def test_m03_the_complete_inventory_is_validated_whole():
    subs = _pair()
    one = _component(subs, parts=(subs[0].subsystem_id,))
    assert sm.validate_components((one,), subs) == (one,)
    with pytest.raises(sm.ComponentError):
        sm.validate_components((one, one), subs)
    reordered = sm.ProjectComponent(
        component_id=one.component_id, display_name=NAME, function_text=FUNCTION,
        subsystem_ids=(subs[1].subsystem_id, subs[0].subsystem_id),
        provenance=OWNER_STATED, validation_state=UNVALIDATED)
    with pytest.raises(sm.ComponentError):
        sm.validate_components((reordered,), subs)
    many = tuple(_component(subs) for _ in range(sm.MAX_PROJECT_COMPONENTS_PER_PROJECT + 1))
    with pytest.raises(sm.ComponentError):
        sm.validate_components(many, subs)


# ==========================================================================
# 2. Persistence owner
# ==========================================================================
def test_s01_an_ordinary_project_declares_and_lists_in_deterministic_order():
    store = _store()
    pid, _subs = _new_store_project(store, integrated=False)
    assert store.load_component_inventory(pid) == ((), ())
    first, second = _component(), _component()          # equal names
    assert store.append_project_component(pid, first, "k1")[0] == PROJECT_COMPONENT_INSERTED
    assert store.append_project_component(pid, second, "k2")[0] == PROJECT_COMPONENT_INSERTED
    _subs2, items = store.load_component_inventory(pid)
    assert [i.component_id for i in items] == [first.component_id, second.component_id]
    assert [r[1] for r in _rows(pid)] == [0, 1]
    assert all(r[5] == "[]" for r in _rows(pid))


def test_s02_one_multi_part_component_survives_a_cold_store_with_one_id(tmp_path):
    path = str(tmp_path / "cold.db")
    store = SqliteRecordStore(path)
    pid, subs = _new_store_project(store)
    item = _component(subs, parts=(subs[1].subsystem_id, subs[0].subsystem_id))
    store.append_project_component(pid, item, "k1")
    store.close()
    cold = SqliteRecordStore(path)
    loaded_subs, [loaded] = cold.load_component_inventory(pid)
    assert loaded == item and loaded_subs == subs
    assert loaded.subsystem_ids == (subs[0].subsystem_id, subs[1].subsystem_id)
    [row] = cold._conn.execute("SELECT subsystem_ids FROM project_components").fetchall()
    assert row[0] == json.dumps([subs[0].subsystem_id, subs[1].subsystem_id],
                                separators=(",", ":"))
    cold.close()


def test_s03_retry_replays_and_changed_material_conflicts():
    store = _store()
    pid, subs = _new_store_project(store)
    item = _component(subs, parts=(subs[0].subsystem_id,))
    store.append_project_component(pid, item, "key")
    again = _component(subs, parts=(subs[0].subsystem_id,))   # new id, same material
    outcome, stored = store.append_project_component(pid, again, "key")
    assert outcome == PROJECT_COMPONENT_EXACT_REPLAY and stored == item
    assert store.committed_project_component_for_submission(pid, "key") == item
    for changed in (_component(subs, name="Other", parts=(subs[0].subsystem_id,)),
                    _component(subs, parts=(subs[1].subsystem_id,)),
                    _component(subs)):
        with pytest.raises(ProjectComponentConflict):
            store.append_project_component(pid, changed, "key")
    assert len(_rows(pid)) == 1


def test_s04_cross_project_or_absent_parts_are_rejected_and_write_nothing():
    store = _store()
    pid, subs = _new_store_project(store)
    other_pid, other = _new_store_project(store)
    forged = sm.ProjectComponent(
        component_id=sm.new_component_id(), display_name=NAME, function_text=FUNCTION,
        subsystem_ids=(other[0].subsystem_id,), provenance=OWNER_STATED,
        validation_state=UNVALIDATED)
    with pytest.raises(ProjectComponentRejected):
        store.append_project_component(pid, forged, "k")
    plain, _none = _new_store_project(store, integrated=False)
    with pytest.raises(ProjectComponentRejected):
        store.append_project_component(plain, _component(subs, parts=(subs[0].subsystem_id,)), "k")
    with pytest.raises(ProjectNotFound):
        store.append_project_component("no-such-project", _component(), "k")
    assert _rows() == []


def test_s05_the_inventory_is_bounded():
    store = _store()
    pid, _subs = _new_store_project(store, integrated=False)
    for i in range(sm.MAX_PROJECT_COMPONENTS_PER_PROJECT):
        store.append_project_component(pid, _component(), "k%d" % i)
    with pytest.raises(ProjectComponentRejected):
        store.append_project_component(pid, _component(), "over")
    assert len(_rows(pid)) == sm.MAX_PROJECT_COMPONENTS_PER_PROJECT


@pytest.mark.parametrize("sql", [
    "UPDATE project_components SET component_seq = 5",
    "UPDATE project_components SET subsystem_ids = 'not json'",
    "UPDATE project_components SET subsystem_ids = '[ ]'",
    "UPDATE project_components SET subsystem_ids = '[\"sub-%s\"]'" % ("0" * 32),
    "UPDATE project_components SET component_id = 'cmp-XYZ' || substr(component_id, 8)",
])
def test_s06_invalid_storage_fails_the_whole_inventory_closed(sql):
    store = _store()
    pid, subs = _new_store_project(store)
    store.append_project_component(pid, _component(subs, parts=(subs[0].subsystem_id,)), "a")
    store.append_project_component(pid, _component(subs), "b")
    _raw(sql + " WHERE project_id = ? AND component_seq = 1", (pid,))
    with pytest.raises(ProjectComponentsCorrupt):
        store.load_component_inventory(pid)
    with pytest.raises(ProjectComponentsCorrupt):
        store.committed_project_component_for_submission(pid, "a")
    with pytest.raises(ProjectComponentsCorrupt):
        store.append_project_component(pid, _component(subs), "c")
    assert len(_rows(pid)) == 2


def test_s07_a_failed_commit_rolls_back_and_an_unresolved_one_refuses_reads(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "f.db"))
    pid, subs = _new_store_project(store)
    real = store._conn
    store._conn = _FailOn(real, prefix="INSERT INTO project_components")
    with pytest.raises(sqlite3.OperationalError):
        store.append_project_component(pid, _component(subs), "k")
    store._conn = real
    assert store.load_component_inventory(pid) == (subs, ())
    store._conn = _CommitAndRollbackFail(real)
    with pytest.raises(sqlite3.OperationalError):
        store.append_project_component(pid, _component(subs), "k")
    store._conn = real
    for read in (lambda: store.load_component_inventory(pid),
                 lambda: store.committed_project_component_for_submission(pid, "k")):
        with pytest.raises(RecordStoreConnectionUnsafe):
            read()


def test_s08_concurrent_duplicate_submissions_commit_exactly_once(tmp_path):
    path = str(tmp_path / "c.db")
    seed = SqliteRecordStore(path)
    pid, subs = _new_store_project(seed)
    seed.close()
    barrier = threading.Barrier(4)
    results = []

    def run():
        st = SqliteRecordStore(path)          # one connection per thread
        item = sm.declared_component(subs, NAME, FUNCTION, (subs[0].subsystem_id,))
        barrier.wait()
        try:
            results.append(st.append_project_component(pid, item, "same-key"))
        finally:
            st.close()

    threads = [threading.Thread(target=run) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sorted(o for o, _ in results) == [PROJECT_COMPONENT_EXACT_REPLAY] * 3 + [
        PROJECT_COMPONENT_INSERTED]
    assert len({s.component_id for _, s in results}) == 1
    check = SqliteRecordStore(path)
    assert len(check.load_component_inventory(pid)[1]) == 1
    check.close()


def test_s09_the_migration_is_additive_and_existing_projects_start_empty(tmp_path):
    path = str(tmp_path / "m.db")
    store = SqliteRecordStore(path)
    pid, subs = _new_store_project(store)
    store._conn.execute("DROP TABLE project_components")      # a pre-slice database
    store.close()
    again = SqliteRecordStore(path)                           # forward migration
    assert again.load_component_inventory(pid) == (subs, ())
    assert again.load_project_subsystems(pid) == subs
    again.close()
    SqliteRecordStore(path).close()                           # idempotent


# ==========================================================================
# 3. Web journey, trust boundary and honest outcomes
# ==========================================================================
def test_w01_an_ordinary_project_declares_and_lists(client):
    sid = _ordinary(client)
    block = _block(_page(client, sid))
    assert block and 'data-ci-none' in block and 'data-ci-parts' not in block
    assert _declare(client, sid, "  " + NAME + "  ").status_code == 302
    [row] = _rows(sid)
    assert row[3:9] == (NAME, FUNCTION, "[]", OWNER_STATED, UNVALIDATED, row[8])
    assert _notice(sid) == ("UI_CI_MSG_SAVED", None)
    block = _block(_page(client, sid))
    assert NAME in block and "data-ci-unassigned" not in block
    assert ui_text.text("UI_CI_MSG_SAVED", "en") in block
    assert ui_text.text("UI_CI_BOUNDARY", "en") in _visible(block)


def test_w02_one_component_linked_to_both_parts_survives_restart_with_one_id(client):
    sid = _integrated(client)
    form = _form(_page(client, sid))
    assert len(form["parts"]) == 2
    _declare(client, sid, parts=list(reversed(form["parts"])),
             submission=form["submission"])
    _declare(client, sid, name="Lid", function="Covers the box.")
    [linked, unlinked] = _rows(sid)
    assert json.loads(linked[5]) == form["parts"] and unlinked[5] == "[]"
    _restart()
    block = _block(_page(client, sid))
    assert _visible(block).count(NAME) == 1
    assert PARTS["mech_part_name"] in block and PARTS["elec_part_name"] in block
    assert "data-ci-unassigned" in block
    assert [r[2] for r in _rows(sid)] == [linked[2], unlinked[2]]
    assert linked[2] not in block                          # no identifier shown


def test_w03_retry_and_changed_material_under_one_submission(client):
    sid = _integrated(client)
    form = _form(_page(client, sid))
    for _ in range(2):
        _declare(client, sid, parts=form["parts"][:1], submission=form["submission"])
    assert len(_rows(sid)) == 1 and _notice(sid) == ("UI_CI_MSG_SAVED", None)
    _declare(client, sid, name="Different", submission=form["submission"])
    assert len(_rows(sid)) == 1 and _notice(sid) == (None, "UI_CI_MSG_NOT_SAVED")
    fresh = _form(_page(client, sid))["submission"]
    assert fresh != form["submission"]
    _declare(client, sid, submission=fresh, parts=form["parts"][:1])   # equal name
    assert len(_rows(sid)) == 2 and len({r[2] for r in _rows(sid)}) == 2


def test_w04_forged_identities_and_foreign_parts_grant_nothing(client):
    sid = _integrated(client)
    other = _integrated(client)
    foreign = _form(_page(client, other))
    _declare(client, sid, submission=foreign["submission"])
    assert _notice(sid) == (None, "UI_CI_MSG_NOT_SAVED")
    _declare(client, sid, parts=foreign["parts"][:1])
    assert _notice(sid) == (None, "UI_CI_MSG_REJECTED")
    _declare(client, sid, parts=["sub-not-an-id"])
    _declare(client, sid, submission="tampered.value")
    assert _rows() == []


def test_w05_non_owner_missing_project_and_csrf_failures_write_nothing(client):
    from tests.test_commercial_evidence_capture import _client_for
    owner, _aid = _client_for("ci-owner@example.com")
    sid = _integrated(owner)
    form = _form(_page(owner, sid))
    intruder, _bid = _client_for("ci-intruder@example.com")
    r = _declare(intruder, sid, name=SECRET, submission=form["submission"])
    assert r.status_code in (302, 403, 404) and SECRET not in r.get_data(as_text=True)
    assert "component-inventory" not in intruder.get(f"/session/{sid}").get_data(as_text=True)
    r = client.post("/session/does-not-exist/declare-component",
                    data={"component_name": NAME, "component_function": FUNCTION})
    assert r.status_code in (302, 403, 404)
    raw_client = appmod.app.test_client()
    r = raw_client.post(f"/session/{sid}/declare-component", data={
        "component_submission": form["submission"], "component_name": NAME,
        "component_function": FUNCTION})
    assert r.status_code == 403
    assert _rows() == []


@pytest.mark.parametrize("name,function,key", [
    ("", FUNCTION, "UI_CI_MSG_INVALID"),
    (NAME, "   ", "UI_CI_MSG_INVALID"),
    ("n" * 81, FUNCTION, "UI_CI_MSG_TOO_LONG"),
    (NAME, "f" * 301, "UI_CI_MSG_TOO_LONG"),
    ("a\x00b", FUNCTION, "UI_CI_MSG_INVALID_CHAR"),
])
def test_w06_invalid_input_is_rejected_never_truncated(client, name, function, key):
    sid = _ordinary(client)
    _declare(client, sid, name=name, function=function)
    assert _rows(sid) == [] and _notice(sid) == (None, key)


def test_w07_invalid_storage_shows_no_list_and_no_form_and_saves_nothing(client):
    sid = _integrated(client)
    _declare(client, sid, name=SECRET)
    _raw("UPDATE project_components SET subsystem_ids = 'broken' WHERE project_id = ?",
         (sid,))
    raw = _page(client, sid)
    block = _block(raw)
    assert 'data-ci-status="unavailable"' in block and "data-ci-form" not in block
    assert SECRET not in raw
    fresh = appmod._submission_identity_for(
        sid, appmod.SESSION_STORE[sid], appmod._COMPONENT_SUBMISSION_DOMAIN,
        appmod._COMPONENT_SUBMISSION_ENTRY_KEY)
    _declare(client, sid, name="Another", submission=fresh)
    assert len(_rows(sid)) == 1 and _notice(sid) == (None, "UI_CI_MSG_NOT_SAVED")


def test_w08_failed_and_uncertain_commits_never_claim_saved_falsely(client, monkeypatch):
    sid = _integrated(client)
    store = _store()
    real = store._conn
    store._conn = _FailOn(real, prefix="INSERT INTO project_components")
    _declare(client, sid)
    store._conn = real
    assert _rows(sid) == [] and _notice(sid) == (None, "UI_CI_MSG_NOT_SAVED")
    store._conn = _FailOn(real, commit_then=True)          # committed, then raised
    _declare(client, sid)
    store._conn = real
    assert len(_rows(sid)) == 1 and _notice(sid) == ("UI_CI_MSG_SAVED", None)
    submission = _form(_page(client, sid))["submission"]

    def unreadable(*_a, **_k):
        raise sqlite3.OperationalError("injected: unreadable")
    store.committed_project_component_for_submission = unreadable
    try:
        _declare(client, sid, name="Gear", submission=submission)
    finally:
        del store.committed_project_component_for_submission
    assert len(_rows(sid)) == 1 and _notice(sid) == (None, "UI_CI_MSG_UNKNOWN")
    assert appmod.SESSION_STORE[sid][appmod._COMPONENT_SUBMISSION_ENTRY_KEY] == submission
    _declare(client, sid, name="Gear", submission=submission)
    assert len(_rows(sid)) == 2 and _notice(sid) == ("UI_CI_MSG_SAVED", None)


def test_w09_unresolved_commit_is_unknown_not_saved(client):
    sid = _ordinary(client)
    store = _store()
    real = store._conn
    store._conn = _CommitAndRollbackFail(real)
    _declare(client, sid)
    store._conn = real
    ack, error = _notice(sid)
    assert ack is None and error == "UI_CI_MSG_UNKNOWN"
    _restart()                                 # drop the unresolved connection
    assert _rows(sid) == []


# ==========================================================================
# 4. No effect beyond the declared list; existing journeys intact
# ==========================================================================
def test_x01_no_state_report_pdf_export_or_progression_effect(client, monkeypatch, caplog):
    from tests.test_stage15_integrated_invention_entry import _pdf_source
    sid = _integrated(client)
    report_before = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    form = _form(_page(client, sid))
    before = pickle.dumps(appmod.SESSION_STORE[sid]["state"])
    with caplog.at_level("DEBUG"):
        _declare(client, sid, name=SECRET, function=SECRET + " function",
                 parts=form["parts"], submission=form["submission"])
    assert len(_rows(sid)) == 1
    assert pickle.dumps(appmod.SESSION_STORE[sid]["state"]) == before
    assert not hasattr(appmod.SESSION_STORE[sid]["state"], "project_components")
    report = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert SECRET not in report
    assert _stable(report) == _stable(report_before)
    assert SECRET not in _pdf_source(client, sid, monkeypatch)
    assert SECRET not in caplog.text
    for path in ("engine/read_export_service.py", "web/api_v1.py",
                 "engine/export_adapter.py", "engine/disclosure_export.py",
                 "engine/derived_readiness.py", "engine/readiness_snapshot.py",
                 "engine/safety_signal.py", "engine/session_reconstruction.py",
                 "engine/idea_state.py", "engine/deterministic_calculation.py",
                 "engine/deliverable_assembler.py"):
        text = open(os.path.join(_ROOT, path), encoding="utf-8").read()
        assert "project_components" not in text and "ProjectComponent" not in text, path


def test_x02_existing_scope_interface_and_calculation_journeys_are_intact(client):
    sid = _integrated(client)
    raw = _page(client, sid)
    assert 'id="integrated-scope"' in raw and 'id="declare-interface"' in raw
    assert "data-cap13-link" in raw or "data-therm01-link" in raw
    _declare(client, sid, parts=_form(raw)["parts"])
    after = _page(client, sid)
    assert 'id="declare-interface"' in after
    assert ("data-cap13-link" in after) == ("data-cap13-link" in raw)
    assert ("data-therm01-link" in after) == ("data-therm01-link" in raw)
    assert _store().load_project_subsystems(sid) == tuple(
        appmod.SESSION_STORE[sid]["state"].subsystems)


def test_x03_arabic_copy_is_rendered_and_inventor_text_isolated(client):
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    sid = _ordinary(client)
    _declare(client, sid, name="<script>alert(1)</script>", function="محرّك صغير")
    raw = _page(client, sid)
    block = _block(raw)
    for key in ("UI_CI_HEADING", "UI_CI_BOUNDARY", "UI_CI_ITEM_STATUS",
                "UI_CI_MSG_SAVED", "UI_CI_FORM_TITLE"):
        assert ui_text.text(key, "ar") in _html.unescape(block), key
    assert "<script>alert(1)</script>" not in raw
    assert '<bdi dir="auto" data-ci-name>&lt;script&gt;' in block
    assert 'dir="rtl"' in raw


def test_x04_every_component_key_has_english_and_arabic_copy():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_CI_")]
    assert len(keys) == 24
    for key in keys:
        assert ui_text.has_string(key), key
