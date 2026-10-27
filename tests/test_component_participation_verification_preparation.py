"""COMPONENT-PARTICIPATION-VERIFICATION-PREPARATION-01 — the inventor's notes for ONE component taking part in ONE interaction.

For ONE CURRENT participation (an existing ``InterfaceParticipation``) the inventor may record, in their own words,
the observable contribution they expect from that component and the evidence or review needed to check it.
Verification PREPARATION only: OWNER_STATED / UNVALIDATED, never a mechanism, compatibility, feasibility,
requirement or evidence. What is pinned:
  * semantics (``engine/subsystem_model.py``): keyed only by ``(interface_id, component_id)``; whole-collection
    validation refuses orphans; CURRENT notes are those of current participations only; the interface-preparation
    text rule (1,000 characters each);
  * persistence (``engine/record_store.py``): ONE additive sidecar ``subsystem_participation_preparations``
    anchored to the exact interaction and declaration rows but NOT to the participation row (Owner decision "keep,
    hide while absent"); removing a participation keeps its notes, marked ``carried_over`` in the same
    transaction, and re-adding it shows them as earlier statements until they are saved again; an unknown table
    shape is refused; stale forms never overwrite; exact retries write nothing;
  * web (``web/app.py``): ONE dedicated POST behind the central project authorization and the CSRF guard,
    committed-truth SAVED / NOT SAVED / UNKNOWN, shown on the interaction-preparation page only (EN / AR);
  * the participation writer's outcomes, the interface preparation, the report / PDF, the Parts / Components /
    Interactions view and the Stage 35 export are unchanged.
"""
import html as _html
import re
import sqlite3

import pytest

import web.app as appmod
from engine import subsystem_model as sm
from engine.idea_state import OWNER_STATED, UNVALIDATED
from engine.record_store import (
    INTERFACE_PARTICIPATION_SAVED, PARTICIPATION_PREPARATION_CLEARED, PARTICIPATION_PREPARATION_SAVED,
    PARTICIPATION_PREPARATION_UNCHANGED, ParticipationPreparationRejected, ParticipationPreparationStale,
    ParticipationPreparationWithdrawn, ParticipationPreparationsCorrupt, SqliteRecordStore)
from tests.test_component_interface_participation import (
    PREP, POST as ICP_POST, PCI, REPORT, _cmp, _form as _icp_form, _ifc, _post as _icp_post, _project, _raw,
    _says, _store, _t, _web_project, client)  # noqa: F401
from tests.test_component_inventory_correct_withdraw import _correct, _withdraw
from tests.test_stage15_integrated_invention_entry import _CommitAndRollbackFail
from tests.test_stage15_subsystem_interface_declaration import _FailOn, _restart
from web import ui_text

POST = "/session/%s/participation-preparation"
EXPECTED = sm.PARTICIPATION_EXPECTED_CONTRIBUTION
EVIDENCE = sm.PARTICIPATION_EVIDENCE_NEEDED
_FORM_RE = re.compile(
    r'<form method="POST" action="/session/[^"]+/participation-preparation" data-ppv-form>.*?</form>', re.S)


# ==========================================================================
# harness
# ==========================================================================
def _notes(e=None, v=None):
    return {EXPECTED: e, EVIDENCE: v}


def _shown(e=None, v=None, carried=False):
    return dict(_notes(e, v), carried_over=carried)


def _rows(pid):
    return _raw("SELECT interface_id, component_id, expected_contribution, evidence_needed, carried_over "
                "FROM subsystem_participation_preparations WHERE project_id = ? "
                "ORDER BY interface_id, component_id", (pid,))


def _store_rows(store, pid):
    return [tuple(row) for row in store._conn.execute(
        "SELECT interface_id, component_id, expected_contribution, evidence_needed, carried_over "
        "FROM subsystem_participation_preparations WHERE project_id = ? "
        "ORDER BY interface_id, component_id", (pid,)).fetchall()]


def _setup(tmp_path, name="p.db"):
    store = SqliteRecordStore(str(tmp_path / name))
    pid, subs = _project(store)
    ifc = _ifc(store, pid, subs)
    a, b = _cmp(store, pid, subs, "A"), _cmp(store, pid, subs, "B")
    store.set_interface_participation(pid, ifc, (a, b), ())
    return store, pid, subs, ifc, a, b


def _current_notes(store, pid):
    record = store.load_participation_preparations(pid)
    return sm.current_participation_preparations(
        record["preparations"], record["participations"], record["components"])


def _forms(raw):
    out = []
    for form in _FORM_RE.findall(raw):
        def value(name):
            m = re.search(r'name="%s" value="([^"]*)"' % name, form)
            return _html.unescape(m.group(1)) if m else None

        def area(name):
            m = re.search(r'name="%s"[^>]*>(.*?)</textarea>' % name, form, re.S)
            return _html.unescape(m.group(1)) if m else None
        out.append({"interface": value("interface_id"), "component": value("component_id"),
                    "carried": value("pp_base_carried"),
                    "base": _notes(value("pp_base_" + EXPECTED), value("pp_base_" + EVIDENCE)),
                    "text": _notes(area("pp_" + EXPECTED), area("pp_" + EVIDENCE))})
    return out


def _page(c, sid):
    return c.get(PREP % sid).get_data(as_text=True)


def _post(c, sid, form, expected=None, evidence=None, **override):
    data = {"interface_id": form["interface"], "component_id": form["component"],
            "pp_base_carried": form["carried"],
            "pp_base_" + EXPECTED: form["base"][EXPECTED], "pp_base_" + EVIDENCE: form["base"][EVIDENCE],
            "pp_" + EXPECTED: form["text"][EXPECTED] if expected is None else expected,
            "pp_" + EVIDENCE: form["text"][EVIDENCE] if evidence is None else evidence}
    data.update(override)
    return c.post(POST % sid, data=data)


def _participating_web_project(c, count=2):
    sid = _web_project(c)
    form = _icp_form(c, sid)
    ids = [i for i, _c in form["options"]]
    _icp_post(c, sid, form, ids[:count])
    return sid, ids


# ==========================================================================
# 1. Semantic owner
# ==========================================================================
def test_m01_validation_is_whole_canonical_and_refuses_orphans(tmp_path):
    store, pid, subs, ifc, a, b = _setup(tmp_path)
    record = store.load_participation_preparations(pid)
    inventory = store.load_component_inventory_record(pid)[1]
    interfaces = record["interfaces"]
    good = [sm.ParticipationPreparation(ifc, b, expected_contribution="turns"),
            sm.ParticipationPreparation(ifc, a, evidence_needed="bench test")]
    assert [p.component_id for p in sm.validate_participation_preparations(good, interfaces, inventory)] == [a, b]
    assert sm.validate_participation_preparations((), interfaces, inventory) == ()
    for bad in ([sm.ParticipationPreparation("ifc-" + "1" * 32, a, expected_contribution="x")],
                [sm.ParticipationPreparation(ifc, "cmp-" + "1" * 32, expected_contribution="x")],
                [sm.ParticipationPreparation(ifc, a)],                                  # records nothing
                [sm.ParticipationPreparation(ifc, a, expected_contribution=" padded")],
                [sm.ParticipationPreparation(ifc, a, expected_contribution="x" * 1001)],
                [sm.ParticipationPreparation(ifc, a, expected_contribution="x", carried_over=1)],
                [sm.ParticipationPreparation(ifc, a, expected_contribution="x", provenance="SYSTEM")],
                [good[0], good[0]]):
        with pytest.raises(sm.ParticipationPreparationError):
            sm.validate_participation_preparations(bad, interfaces, inventory)
    item = good[0]
    assert (item.provenance, item.validation_state) == (OWNER_STATED, UNVALIDATED)


def test_m02_target_requires_a_current_participation_of_an_active_component(tmp_path):
    store, pid, subs, ifc, a, b = _setup(tmp_path)
    c = _cmp(store, pid, subs, "C")                                      # declared, not participating
    record = store.load_participation_preparations(pid)
    inventory = store.load_component_inventory_record(pid)[1]
    args = (inventory, record["interfaces"], record["participations"])
    target = sm.participation_preparation_target(*args, ifc, a, _notes("turns", None))
    assert target == sm.ParticipationPreparation(ifc, a, expected_contribution="turns")
    assert sm.participation_preparation_target(*args, ifc, a, _notes()) is None
    for interface_id, component_id, values in (
            (ifc, c, _notes("x")), ("ifc-" + "2" * 32, a, _notes("x")), ("bad", a, _notes("x")),
            (ifc, a, {EXPECTED: "x"}), (ifc, a, _notes("x" * 1001)), (ifc, a, _notes(""))):
        with pytest.raises(sm.ParticipationPreparationError):
            sm.participation_preparation_target(*args, interface_id, component_id, values)
    _withdraw(store, pid, b, 0)
    inventory = store.load_component_inventory_record(pid)[1]
    with pytest.raises(sm.ComponentAlreadyWithdrawn):
        sm.participation_preparation_target(inventory, record["interfaces"], record["participations"],
                                            ifc, b, _notes("x"))


# ==========================================================================
# 2. Persistence
# ==========================================================================
def test_s01_save_retry_replace_clear(tmp_path):
    store, pid, _subs, ifc, a, b = _setup(tmp_path)
    assert store.load_participation_preparations(pid)["preparations"] == ()
    assert store.set_participation_preparation(pid, ifc, a, _notes("Turns the hinge"), _shown()) \
        == PARTICIPATION_PREPARATION_SAVED
    assert store.set_participation_preparation(pid, ifc, a, _notes("Turns the hinge"), _shown()) \
        == PARTICIPATION_PREPARATION_UNCHANGED                            # exact retry
    assert store.set_participation_preparation(
        pid, ifc, a, _notes("Turns the hinge", "Bench test"), _shown("Turns the hinge")) \
        == PARTICIPATION_PREPARATION_SAVED
    note = _current_notes(store, pid)[(ifc, a)]
    assert (note.expected_contribution, note.evidence_needed, note.carried_over) == (
        "Turns the hinge", "Bench test", False)
    assert (ifc, b) not in _current_notes(store, pid)
    assert store.set_participation_preparation(pid, ifc, a, _notes(), _shown("Turns the hinge", "Bench test")) \
        == PARTICIPATION_PREPARATION_CLEARED
    assert store.load_participation_preparations(pid)["preparations"] == ()
    assert store.set_participation_preparation(pid, ifc, a, _notes(), _shown()) \
        == PARTICIPATION_PREPARATION_UNCHANGED


def test_s02_a_stale_form_never_overwrites_newer_notes(tmp_path):
    store, pid, _subs, ifc, a, _b = _setup(tmp_path)
    store.set_participation_preparation(pid, ifc, a, _notes("first"), _shown())
    with pytest.raises(ParticipationPreparationStale):
        store.set_participation_preparation(pid, ifc, a, _notes("second"), _shown())    # form showed nothing
    with pytest.raises(ParticipationPreparationStale):
        store.set_participation_preparation(pid, ifc, a, _notes("second"), _shown("first", carried=True))
    assert _current_notes(store, pid)[(ifc, a)].expected_contribution == "first"


def test_s03_line_breaks_are_not_a_difference_and_unchanged_text_keeps_its_bytes(tmp_path):
    store, pid, _subs, ifc, a, _b = _setup(tmp_path)
    store.set_participation_preparation(pid, ifc, a, _notes("one\r\ntwo"), _shown())
    assert store.set_participation_preparation(pid, ifc, a, _notes("one\ntwo"), _shown("one\ntwo")) \
        == PARTICIPATION_PREPARATION_UNCHANGED
    assert store.set_participation_preparation(pid, ifc, a, _notes("one\ntwo", "check"),
                                               _shown("one\ntwo")) == PARTICIPATION_PREPARATION_SAVED
    assert _current_notes(store, pid)[(ifc, a)].expected_contribution == "one\r\ntwo"


def test_s04_identity_membership_and_shape_are_decided_before_any_write(tmp_path):
    store, pid, subs, ifc, a, _b = _setup(tmp_path)
    other, osubs = _project(store, idea="i-other")
    oifc = _ifc(store, other, osubs, key="o1")
    oc = _cmp(store, other, osubs, "OA", key="ok")
    store.set_interface_participation(other, oifc, (oc,), ())
    c = _cmp(store, pid, subs, "C")
    for interface_id, component_id in ((oifc, a), (ifc, oc), (ifc, c), ("x", a), (ifc, "")):
        with pytest.raises(ParticipationPreparationRejected):
            store.set_participation_preparation(pid, interface_id, component_id, _notes("x"), _shown())
    for values, shown in ((_notes(" padded"), _shown()), (_notes("x" * 1001), _shown()),
                          ({EXPECTED: "x"}, _shown()), (_notes("x"), _notes()),
                          (_notes("x"), dict(_shown(), carried_over="no")), (_notes("a\x00b"), _shown())):
        with pytest.raises(ParticipationPreparationRejected):
            store.set_participation_preparation(pid, ifc, a, values, shown)
    assert _store_rows(store, pid) == [] and _store_rows(store, other) == []


def test_s05_removal_keeps_and_hides_readding_shows_earlier_notes_until_saved(tmp_path):
    store, pid, _subs, ifc, a, b = _setup(tmp_path)
    store.set_participation_preparation(pid, ifc, a, _notes("Turns the hinge", "Bench test"), _shown())
    store.set_participation_preparation(pid, ifc, b, _notes("Powers it"), _shown())
    assert store.set_interface_participation(pid, ifc, (b,), (a, b)) == INTERFACE_PARTICIPATION_SAVED
    assert set(_current_notes(store, pid)) == {(ifc, b)}                    # hidden while absent
    assert _store_rows(store, pid) == sorted([(ifc, a, "Turns the hinge", "Bench test", 1),
                                              (ifc, b, "Powers it", None, 0)])
    with pytest.raises(ParticipationPreparationRejected):                  # not a participant now
        store.set_participation_preparation(pid, ifc, a, _notes("x"), _shown())
    store.set_interface_participation(pid, ifc, (a, b), (b,))              # the same participation again
    note = _current_notes(store, pid)[(ifc, a)]
    assert (note.expected_contribution, note.carried_over) == ("Turns the hinge", True)
    # An unchanged save of the earlier notes is an explicit reconfirmation, not a no-op.
    with pytest.raises(ParticipationPreparationStale):                     # the form must have shown them
        store.set_participation_preparation(pid, ifc, a, _notes("Turns the hinge", "Bench test"),
                                            _shown("Turns the hinge", "Bench test"))
    assert store.set_participation_preparation(
        pid, ifc, a, _notes("Turns the hinge", "Bench test"),
        _shown("Turns the hinge", "Bench test", carried=True)) == PARTICIPATION_PREPARATION_SAVED
    assert _current_notes(store, pid)[(ifc, a)].carried_over is False
    assert store.set_participation_preparation(
        pid, ifc, a, _notes("Turns the hinge", "Bench test"),
        _shown("Turns the hinge", "Bench test")) == PARTICIPATION_PREPARATION_UNCHANGED
    # clearing carried-over notes removes them
    store.set_interface_participation(pid, ifc, (b,), (a, b))
    store.set_interface_participation(pid, ifc, (a, b), (b,))
    assert store.set_participation_preparation(
        pid, ifc, a, _notes(), _shown("Turns the hinge", "Bench test", carried=True)) \
        == PARTICIPATION_PREPARATION_CLEARED
    assert [r[1] for r in _store_rows(store, pid)] == [b]


def test_s06_correction_keeps_withdrawal_hides_and_redeclaration_inherits_nothing(tmp_path):
    store, pid, subs, ifc, a, b = _setup(tmp_path)
    store.set_participation_preparation(pid, ifc, a, _notes("Turns"), _shown())
    store.set_participation_preparation(pid, ifc, b, _notes("Powers"), _shown())
    _correct(store, pid, a, 0, "A renamed")                                 # same identity
    assert _current_notes(store, pid)[(ifc, a)].expected_contribution == "Turns"
    _withdraw(store, pid, b, 0)
    assert set(_current_notes(store, pid)) == {(ifc, a)}
    assert len(store.load_participation_preparations(pid)["preparations"]) == 2   # history kept
    with pytest.raises(ParticipationPreparationWithdrawn):
        store.set_participation_preparation(pid, ifc, b, _notes("x"), _shown("Powers"))
    c = _cmp(store, pid, subs, "B", key="k-B-again")                     # a new, separate declaration
    store.set_interface_participation(pid, ifc, (a, c), (a,))
    assert c != b and (ifc, c) not in _current_notes(store, pid)       # participates, inherits no note


def test_s07_migration_is_additive_idempotent_and_refuses_an_unknown_shape(tmp_path):
    path = str(tmp_path / "m.db")
    store, pid, _subs, ifc, a, _b = _setup(tmp_path, "m.db")
    store.set_participation_preparation(pid, ifc, a, _notes("kept"), _shown())
    store.close()
    store = SqliteRecordStore(path)                                         # idempotent reopen
    assert _current_notes(store, pid)[(ifc, a)].expected_contribution == "kept"
    store.close()
    conn = sqlite3.connect(path)
    conn.execute("DROP TABLE subsystem_participation_preparations")
    conn.execute("CREATE TABLE subsystem_participation_preparations (project_id TEXT, note TEXT)")
    conn.commit()
    conn.close()
    with pytest.raises(sqlite3.DatabaseError):
        SqliteRecordStore(path).load_participation_preparations(pid)


def test_s08_the_database_backstop_and_whole_collection_validation(tmp_path):
    store, pid, _subs, ifc, a, _b = _setup(tmp_path)
    path = str(tmp_path / "p.db")
    conn = sqlite3.connect(path, isolation_level=None)                    # autocommit: PRAGMAs apply
    conn.execute("PRAGMA foreign_keys = ON")
    for row in ((pid, ifc, a, None, None, 0), (pid, ifc, a, "x", None, 2), (pid, ifc, a, "x" * 1001, None, 0),
                (pid, ifc, "cmp-" + "3" * 32, "x", None, 0)):
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("INSERT INTO subsystem_participation_preparations VALUES (?, ?, ?, ?, ?, ?)", row)
    conn.execute("PRAGMA foreign_keys = OFF")
    conn.execute("INSERT INTO subsystem_participation_preparations VALUES (?, ?, ?, ?, ?, ?)",
                 (pid, ifc, "cmp-" + "3" * 32, "orphan", None, 0))
    conn.commit()
    conn.close()
    with pytest.raises(ParticipationPreparationsCorrupt):
        store.load_participation_preparations(pid)
    with pytest.raises(ParticipationPreparationsCorrupt):
        store.set_participation_preparation(pid, ifc, a, _notes("x"), _shown())
    # the participation owner itself is unaffected by a corrupt note row
    assert store.load_interface_participation(pid)["participations"]


def test_s09_failed_writes_roll_back(tmp_path):
    store, pid, _subs, ifc, a, _b = _setup(tmp_path)
    real = store._conn
    store._conn = _FailOn(real, prefix="INSERT INTO subsystem_participation_preparations")
    with pytest.raises(Exception):
        store.set_participation_preparation(pid, ifc, a, _notes("x"), _shown())
    store._conn = real
    assert store.load_participation_preparations(pid)["preparations"] == ()


# ==========================================================================
# 3. Web
# ==========================================================================
def test_w01_record_view_replace_and_clear_on_the_preparation_page(client):
    sid, ids = _participating_web_project(client)
    raw = _page(client, sid)
    text = _html.unescape(raw)
    assert _t("UI_PPV_HEADING") in text and _t("UI_PPV_BOUNDARY") in text
    forms = _forms(raw)
    assert [f["component"] for f in forms] == ids[:2]                      # current participants only
    assert forms[0]["base"] == _notes("", "") and forms[0]["carried"] == "0"
    r = _post(client, sid, forms[0], "It turns the hinge when powered", "")
    assert r.status_code == 200 and _says(r, _t("UI_PPV_MSG_SAVED"))
    form = _forms(_page(client, sid))[0]
    assert form["text"][EXPECTED] == "It turns the hinge when powered" and form["base"][EXPECTED] == form["text"][EXPECTED]
    r = _post(client, sid, form, None, "Bench test with a timer")
    assert _says(r, _t("UI_PPV_MSG_SAVED"))
    assert [row[2:] for row in _rows(sid)] == [("It turns the hinge when powered", "Bench test with a timer", 0)]
    r = _post(client, sid, _forms(_page(client, sid))[0])                  # resubmitted untouched
    assert _says(r, _t("UI_PPV_MSG_UNCHANGED"))
    r = _post(client, sid, _forms(_page(client, sid))[0], "", "")
    assert _says(r, _t("UI_PPV_MSG_CLEARED")) and _rows(sid) == []


def test_w02_crlf_resubmission_is_unchanged_and_a_stale_form_writes_nothing(client):
    sid, _ids = _participating_web_project(client)
    form = _forms(_page(client, sid))[0]
    _post(client, sid, form, "line one\r\nline two")
    form = _forms(_page(client, sid))[0]
    r = _post(client, sid, form, "line one\r\nline two")                   # browser CRLF vs LF baseline
    assert _says(r, _t("UI_PPV_MSG_UNCHANGED"))
    stale = dict(form, base=_notes("", ""))
    r = _post(client, sid, stale, "overwrite attempt")
    assert r.status_code == 409 and _says(r, _t("UI_PPV_MSG_STALE"))
    assert _rows(sid)[0][2] == "line one\r\nline two"


def test_w03_removal_hides_and_readding_shows_earlier_notes_labelled(client):
    sid, ids = _participating_web_project(client)
    _post(client, sid, _forms(_page(client, sid))[0], "Turns the hinge", "Bench test")
    icp = _icp_form(client, sid)
    _icp_post(client, sid, icp, [ids[1]])                                   # remove the first component
    raw = _page(client, sid)
    assert [f["component"] for f in _forms(raw)] == [ids[1]] and "Turns the hinge" not in raw
    assert _rows(sid)[0][4] == 1
    _icp_post(client, sid, _icp_form(client, sid), [ids[0], ids[1]])        # add it back
    raw = _page(client, sid)
    form = [f for f in _forms(raw) if f["component"] == ids[0]][0]
    assert form["carried"] == "1" and form["text"][EXPECTED] == "Turns the hinge"
    assert raw.count("data-ppv-carried") == 1 and _t("UI_PPV_CARRIED") in _html.unescape(raw)
    r = _post(client, sid, form)                                            # explicit reconfirmation
    assert _says(r, _t("UI_PPV_MSG_SAVED")) and "data-ppv-carried" not in r.get_data(as_text=True)
    assert _rows(sid)[0][4] == 0


def test_w04_malformed_forms_are_rejected_and_write_nothing(client):
    sid, ids = _participating_web_project(client)
    form = _forms(_page(client, sid))[0]
    for override in ({"interface_id": "bad"}, {"component_id": "bad"}, {"pp_base_carried": "2"},
                     {"pp_base_" + EXPECTED: "z" * 1001}, {"component_id": ids[2]}):
        r = _post(client, sid, form, "x", **override)
        assert r.status_code == 400 and _says(r, _t("UI_PPV_MSG_REJECTED")), override
    data = {"interface_id": [form["interface"]] * 2, "component_id": form["component"],
            "pp_base_carried": "0", "pp_base_" + EXPECTED: "", "pp_base_" + EVIDENCE: "",
            "pp_" + EXPECTED: "x", "pp_" + EVIDENCE: ""}
    assert client.post(POST % sid, data=data).status_code == 400
    r = _post(client, sid, form, "y" * 1001)
    assert r.status_code == 400 and _says(r, _t("UI_PPV_MSG_TOO_LONG"))
    assert "data-ppv-draft" in r.get_data(as_text=True) and "y" * 1001 in r.get_data(as_text=True)
    assert _rows(sid) == []


def test_w05_authorization_csrf_and_cross_project_identities(client):
    from tests.test_commercial_evidence_capture import _client_for
    owner, _aid = _client_for("ppv-owner@example.com")
    sid, _ids = _participating_web_project(owner)
    form = _forms(_page(owner, sid))[0]
    intruder, _bid = _client_for("ppv-intruder@example.com")
    r = _post(intruder, sid, form, "intrusion")
    assert r.status_code in (302, 403, 404) and "Hinge motor" not in r.get_data(as_text=True)
    raw_client = appmod.app.test_client()                                   # no CSRF token
    r = raw_client.post(POST % sid, data={"interface_id": form["interface"], "component_id": form["component"],
                                          "pp_base_carried": "0", "pp_base_" + EXPECTED: "",
                                          "pp_base_" + EVIDENCE: "", "pp_" + EXPECTED: "x",
                                          "pp_" + EVIDENCE: ""})
    assert r.status_code == 403
    other, _oids = _participating_web_project(owner)
    foreign = _forms(_page(owner, other))[0]
    r = _post(owner, sid, dict(form, component=foreign["component"]), "x")
    assert r.status_code == 400
    r = _post(owner, sid, dict(form, interface=foreign["interface"]), "x")
    assert r.status_code == 400
    assert _rows(sid) == [] and _rows(other) == []


def test_w06_a_withdrawn_component_is_not_shown_and_takes_no_note(client):
    sid, ids = _participating_web_project(client)
    forms = _forms(_page(client, sid))
    _post(client, sid, forms[1], "Powers it")
    form = _forms(_page(client, sid))[1]
    _withdraw(_store(), sid, ids[1], 0)
    raw = _page(client, sid)
    assert [f["component"] for f in _forms(raw)] == [ids[0]] and "Powers it" not in raw
    r = _post(client, sid, form, "changed")
    assert r.status_code == 409 and _says(r, _t("UI_PPV_MSG_WITHDRAWN"))
    assert _rows(sid)[0][2] == "Powers it"


def test_w07_failed_uncertain_and_unresolved_commits_are_truthful(client):
    sid, _ids = _participating_web_project(client)
    store = _store()
    real = store._conn
    form = _forms(_page(client, sid))[0]
    store._conn = _FailOn(real, prefix="INSERT INTO subsystem_participation_preparations")
    r = _post(client, sid, form, "x")
    store._conn = real
    assert r.status_code == 503 and _says(r, _t("UI_PPV_MSG_NOT_SAVED")) and _rows(sid) == []
    store._conn = _FailOn(real, commit_then=True)                           # committed, then raised
    r = _post(client, sid, form, "x")
    store._conn = real
    assert r.status_code == 200 and _says(r, _t("UI_PPV_MSG_SAVED")) and _rows(sid)[0][2] == "x"
    form = _forms(_page(client, sid))[0]
    store._conn = _CommitAndRollbackFail(real)                              # unresolved
    r = _post(client, sid, form, "y")
    store._conn = real
    assert r.status_code == 503 and _says(r, _t("UI_PPV_MSG_UNKNOWN"))
    _restart()
    assert _rows(sid)[0][2] == "x"


def test_w08_unreadable_notes_read_unavailable_and_the_rest_of_the_page_stays(client):
    sid, ids = _participating_web_project(client)
    form = _forms(_page(client, sid))[0]
    _raw("INSERT INTO subsystem_participation_preparations VALUES (?, ?, ?, ?, ?, ?)",
         (sid, form["interface"], "cmp-" + "9" * 32, "orphan", None, 0), fk=False)
    raw = _page(client, sid)
    assert "data-ppv-unavailable" in raw and _forms(raw) == []
    assert "data-icp-form" in raw and "data-prep-intro" in raw              # participation block unaffected
    r = _post(client, sid, form, "x")
    assert r.status_code == 503 and _says(r, _t("UI_PPV_MSG_NOT_SAVED"))
    # the participation save itself still works
    r = _icp_post(client, sid, _icp_form(client, sid), ids[:1])
    assert r.status_code == 200


def test_w09_arabic_page_and_copy_parity(client):
    sid, _ids = _participating_web_project(client)
    _post(client, sid, _forms(_page(client, sid))[0], "يدير المفصلة")
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    raw = _html.unescape(_page(client, sid))
    for key in ("UI_PPV_HEADING", "UI_PPV_INTRO", "UI_PPV_BOUNDARY", "UI_PPV_EXPECTED_LABEL",
                "UI_PPV_EVIDENCE_LABEL", "UI_PPV_SAVE"):
        assert _t(key, "ar") in raw, key
    assert "يدير المفصلة" in raw
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_PPV_")] if hasattr(ui_text, "UI_STRINGS") else []
    for key in keys or ["UI_PPV_HEADING", "UI_PPV_CARRIED", "UI_PPV_MSG_SAVED", "UI_PPV_MSG_STALE"]:
        assert _t(key, "en") and _t(key, "ar") and _t(key, "en") != _t(key, "ar"), key
    for name in ("SAVED", "CLEARED", "UNCHANGED", "STALE", "WITHDRAWN", "REJECTED", "TOO_LONG", "NOT_SAVED",
                 "UNKNOWN"):
        english = getattr(appmod, "PPV_%s_MESSAGE" % name)
        assert ui_text.localize_message(english, "ar") == _t("UI_PPV_MSG_" + name, "ar"), name
    lowered = " ".join(_t(k, "en") for k in ("UI_PPV_BOUNDARY", "UI_PPV_INTRO", "UI_PPV_CARRIED")).lower()
    # positive claims only: the copy names these topics in order to deny them
    for claim in ("has been verified", "it will work", "it is safe", "is now verified"):
        assert claim not in lowered


def test_w10_report_pdf_parts_view_and_export_do_not_carry_the_notes(client):
    sid, _ids = _participating_web_project(client)
    _post(client, sid, _forms(_page(client, sid))[0], "Zq-note-5521", "Zq-evidence-5521")
    for url in (REPORT % sid, PCI % sid, "/session/%s" % sid):
        body = client.get(url).get_data(as_text=True)
        assert "Zq-note-5521" not in body and "Zq-evidence-5521" not in body, url
    for template in ("deliverable.html", "parts_components_interactions.html", "session.html"):
        source = (appmod.app.root_path + "/templates/" + template)
        assert "ppv" not in open(source, encoding="utf-8").read(), template
    import engine.disclosure_export as export
    assert "participation_preparation" not in open(export.__file__, encoding="utf-8").read()


def test_w11_the_participation_and_preparation_writers_are_otherwise_unchanged(client):
    sid, ids = _participating_web_project(client)
    r = _icp_post(client, sid, _icp_form(client, sid), ids[:2])
    assert _says(r, _t("UI_ICP_MSG_UNCHANGED"))
    assert [f["component"] for f in _forms(_page(client, sid))] == ids[:2]
    src = open(appmod.__file__, encoding="utf-8").read()
    section = src[src.index("# --- COMPONENT-PARTICIPATION-VERIFICATION-PREPARATION-01"):
                  src.index('@app.route("/session/<sid>/interface-preparation", methods=["GET"])')]
    for banned in ("safety_signal", "SafetySignal(", "append_", "/api/", "run_iteration",
                   "derive_", "set_interface_participation(", "apply_interface_preparation"):
        assert banned not in section, banned
