# -*- coding: utf-8 -*-
"""G1-PLANAR-MOMENT-SAVED-DECLARATION-01 - saved planar-moment configurations.

Owner-authorized (with two narrow corrections): the inventor may save, for ONE
component they declared and chose themselves, the INPUTS of an admitted
configuration of the existing ``cap13:planar_single_force_moment`` calculation,
plus their own description of the chosen point and of the force context. The
semantic owner is ``engine/subsystem_model.py``; persistence is ONE append-only
family ``planar_moment_revisions`` (the planar-clearance pattern). The moment is
never stored: every read re-runs the unchanged consumer through its one trusted
binding. Only a configuration the method admits with SUCCESS is saved, checked
by the route and again inside the serialized write. A changed component, part
link, method or governed artifact reads NEEDS RECONFIRMATION with no number;
an unreadable history reads UNAVAILABLE. Synthetic data only.
"""
import html as _html
import json
import os
import re
import sqlite3

import pytest

import web.app as webapp
from engine import record_store
from engine import cap13_planar_moment as moment
from engine import subsystem_model as sm
from engine.idea_state import OWNER_STATED, UNVALIDATED
from engine.record_store import (
    PLANAR_MOMENT_EXACT_REPLAY, PLANAR_MOMENT_INSERTED, PlanarMomentConflict,
    PlanarMomentCorrupt, PlanarMomentRejected, SqliteRecordStore)
from tests.test_cap12_form_mockup_advisory import _client_for, _start, _snapshot, SEED, ELEC_FORM
from tests.test_cap13_planar_moment import _form as _moment_form
from tests.test_cap13_therm01_integrated_part_eligibility import _integrated, MECH, ELEC
from tests.test_component_inventory_correct_withdraw import (
    _correct as _correct_component, _declare_store, _withdraw as _withdraw_component)
from tests.test_component_inventory_declare_list import _declare
from tests.test_stage15_integrated_invention_entry import _contract, _pair, _ri
from web import ui_text

URL = "/session/%s/planar-moment"
POINT = "The hinge pin at the lower edge of the flap"
FORCE = "A hand pressing down on the far corner of the flap"
EXPECTED = "1000.0 N·mm"           # 12.5 N x 80 mm, as the consumer formats it


# ─── store-level helpers ─────────────────────────────────────────────────────

def _admit(material):
    return webapp._pm_admit(material)


@pytest.fixture
def store(tmp_path):
    s = SqliteRecordStore(str(tmp_path / "pm.db"))
    yield s
    s.close()


def _mech_project(store):
    return store.create_project(_contract(), reconstruction_inputs=_ri(MECH))


def _material(store, pid, component_id, **over):
    snap = store.load_planar_moments(pid)
    record = snap["inventory"].record_for(component_id)
    kw = dict(point_description=POINT, force_context=FORCE,
              values=("12.5", "80"),
              declarations=(moment.ANSWER_APPLIES,) * len(moment.DECLARATION_IDS),
              screen=(moment.SCREEN_NO,) * len(moment.SCREEN_ITEMS))
    kw.update(over)
    return sm.planar_moment_material(
        snap["inventory"], snap["subsystems"], snap["root_domain"], component_id,
        record.head_revision_no if record else 0, kw["point_description"],
        kw["force_context"], kw["values"], kw["declarations"], kw["screen"],
        record_store.planar_moment_method_identity())


def _declare_pm(store, pid, component_id, key="k1", **over):
    snap = store.load_planar_moments(pid)
    revision = sm.declared_planar_moment(snap["ledger"], _material(store, pid, component_id, **over))
    return store.append_planar_moment_revision(pid, revision, key, admit=_admit)


def _rows(store):
    return store._conn.execute("SELECT * FROM planar_moment_revisions").fetchall()


# ─── 1. inputs only: never a number ─────────────────────────────────────────

def test_the_table_holds_inputs_and_identity_only_never_a_result(store):
    pid = _mech_project(store)
    comp = _declare_store(store, pid, (), "Folding flap")
    outcome, stored = _declare_pm(store, pid, comp.component_id)
    assert outcome == PLANAR_MOMENT_INSERTED
    columns = [r[1] for r in store._conn.execute("PRAGMA table_info(planar_moment_revisions)")]
    assert not [c for c in columns if re.search(r"result|output|moment|value_m\b|^m$", c, re.I)]
    for row in _rows(store):
        assert "1000" not in json.dumps(row, default=str)
    record = store.load_planar_moments(pid)["ledger"].record_for(stored.declaration_id)
    m = record.current
    assert (m.point_description, m.force_context, m.values) == (POINT, FORCE, ("12.5", "80"))
    assert (m.method_id, m.method_version) == (moment.METHOD_ID, moment.METHOD_VERSION)
    assert (m.part_id, stored.provenance, stored.validation_state) == (None, OWNER_STATED, UNVALIDATED)
    assert re.fullmatch(r"[0-9a-f]{64}", m.artifact_sha256)


# ─── 2. Correction 2: admission at the serialized save boundary ──────────────

@pytest.mark.parametrize("over", [
    {"declarations": (moment.ANSWER_DOES_NOT_APPLY,) + (moment.ANSWER_APPLIES,) * 4},
    {"screen": (moment.SCREEN_YES,) + (moment.SCREEN_NO,) * 8},
    {"values": ("0", "80")}, {"values": ("-1", "80")}, {"values": ("1e3", "80")},
    {"values": ("12,5", "80")}, {"values": ("", "80")},
])
def test_an_unadmitted_configuration_cannot_even_be_built(store, over):
    pid = _mech_project(store)
    comp = _declare_store(store, pid, (), "Folding flap")
    with pytest.raises(sm.PlanarMomentNotAdmitted):
        _material(store, pid, comp.component_id, **over)


def test_the_store_requires_the_methods_success_inside_the_write(store):
    pid = _mech_project(store)
    comp = _declare_store(store, pid, (), "Folding flap")
    snap = store.load_planar_moments(pid)
    revision = sm.declared_planar_moment(snap["ledger"], _material(store, pid, comp.component_id))
    for admit in (None, lambda m: False, lambda m: 1, lambda m: (_ for _ in ()).throw(RuntimeError())):
        with pytest.raises(PlanarMomentRejected) as caught:
            store.append_planar_moment_revision(pid, revision, "k-%s" % id(admit), admit=admit)
        assert isinstance(caught.value.cause, sm.PlanarMomentNotAdmitted)
    assert _rows(store) == []
    assert store.append_planar_moment_revision(pid, revision, "k-ok", admit=_admit)[0] \
        == PLANAR_MOMENT_INSERTED


def test_the_database_refuses_an_unadmitted_row_directly(store):
    pid = _mech_project(store)
    comp = _declare_store(store, pid, (), "Folding flap")
    _declare_pm(store, pid, comp.component_id)
    for sql in ("UPDATE planar_moment_revisions SET decl_planar = 'does_not_apply'",
                "UPDATE planar_moment_revisions SET screen_children = 'yes'",
                "UPDATE planar_moment_revisions SET value_F = '1e3'"):
        with pytest.raises(sqlite3.IntegrityError):
            store._conn.execute(sql)


# ─── 3. eligibility: the inventor's component, never inferred ────────────────

def test_eligibility_follows_the_project_and_the_part_link(store):
    ordinary = _mech_project(store)
    comp = _declare_store(store, ordinary, (), "Folding flap")
    assert _material(store, ordinary, comp.component_id).part_id is None
    elec = store.create_project(_contract(), reconstruction_inputs=_ri(ELEC))
    other = _declare_store(store, elec, (), "Board")
    with pytest.raises(sm.PlanarMomentNotEligible):
        _material(store, elec, other.component_id)
    subs = _pair()
    integ = store.create_project(_contract(), reconstruction_inputs=_ri(ELEC), subsystems=subs)
    mech_part = next(s for s in subs if s.domain == MECH)
    elec_part = next(s for s in subs if s.domain == ELEC)
    unlinked = _declare_store(store, integ, subs, "Loose part", parts=(elec_part.subsystem_id,))
    linked = _declare_store(store, integ, subs, "Arm", parts=(mech_part.subsystem_id,))
    with pytest.raises(sm.PlanarMomentNotEligible):
        _material(store, integ, unlinked.component_id)
    assert _material(store, integ, linked.component_id).part_id == mech_part.subsystem_id


def test_a_withdrawn_or_foreign_component_is_refused(store):
    pid = _mech_project(store)
    comp = _declare_store(store, pid, (), "Folding flap")
    _withdraw_component(store, pid, comp.component_id, 0)
    with pytest.raises(sm.PlanarMomentNotEligible):
        _material(store, pid, comp.component_id)
    other = _mech_project(store)
    foreign = _declare_store(store, other, (), "Elsewhere", key="k-foreign")
    with pytest.raises(sm.PlanarMomentNotEligible):
        _material(store, pid, foreign.component_id)


# ─── 4. staleness: conservative, never a stale number ────────────────────────

def _issues(store, pid, declaration_id, identity="current"):
    snap = store.load_planar_moments(pid)
    record = snap["ledger"].record_for(declaration_id)
    ident = record_store.planar_moment_method_identity() if identity == "current" else identity
    return sm.planar_moment_binding_issues(record.current, snap["inventory"],
                                           snap["subsystems"], snap["root_domain"], ident)


def test_component_and_method_changes_need_reconfirmation(store):
    pid = _mech_project(store)
    comp = _declare_store(store, pid, (), "Folding flap")
    _o, stored = _declare_pm(store, pid, comp.component_id)
    assert _issues(store, pid, stored.declaration_id) == ()
    ident = record_store.planar_moment_method_identity()
    assert _issues(store, pid, stored.declaration_id, ident[:3] + ("0" * 64,)) \
        == (sm.PM_ISSUE_METHOD_CHANGED,)
    assert _issues(store, pid, stored.declaration_id, None) == (sm.PM_ISSUE_METHOD_CHANGED,)
    _correct_component(store, pid, comp.component_id, 0, "Folding flap, longer")
    assert _issues(store, pid, stored.declaration_id) == (sm.PM_ISSUE_COMPONENT_CHANGED,)
    _withdraw_component(store, pid, comp.component_id, 1)
    assert _issues(store, pid, stored.declaration_id) == (sm.PM_ISSUE_COMPONENT_WITHDRAWN,)


def test_losing_the_part_link_needs_reconfirmation(store):
    subs = _pair()
    pid = store.create_project(_contract(), reconstruction_inputs=_ri(MECH), subsystems=subs)
    mech_part = next(s for s in subs if s.domain == MECH)
    elec_part = next(s for s in subs if s.domain == ELEC)
    comp = _declare_store(store, pid, subs, "Arm", parts=(mech_part.subsystem_id,))
    _o, stored = _declare_pm(store, pid, comp.component_id)
    _correct_component(store, pid, comp.component_id, 0, "Arm", parts=(elec_part.subsystem_id,))
    assert _issues(store, pid, stored.declaration_id) == (
        sm.PM_ISSUE_COMPONENT_CHANGED, sm.PM_ISSUE_PART_LINK_LOST)


def test_a_correction_is_the_explicit_reconfirmation(store):
    pid = _mech_project(store)
    comp = _declare_store(store, pid, (), "Folding flap")
    _o, stored = _declare_pm(store, pid, comp.component_id)
    _correct_component(store, pid, comp.component_id, 0, "Folding flap, longer")
    snap = store.load_planar_moments(pid)
    material = _material(store, pid, comp.component_id)          # same inputs, new revision
    revision = sm.corrected_planar_moment(snap["ledger"], stored.declaration_id, 0, material)
    store.append_planar_moment_revision(pid, revision, "k2", admit=_admit)
    assert _issues(store, pid, stored.declaration_id) == ()
    with pytest.raises(sm.PlanarMomentUnchanged):
        sm.corrected_planar_moment(store.load_planar_moments(pid)["ledger"],
                                   stored.declaration_id, 1, material)


def test_a_stale_component_revision_is_refused(store):
    pid = _mech_project(store)
    comp = _declare_store(store, pid, (), "Folding flap")
    snap = store.load_planar_moments(pid)
    with pytest.raises(sm.PlanarMomentStale):
        sm.planar_moment_material(
            snap["inventory"], snap["subsystems"], snap["root_domain"], comp.component_id, 3,
            POINT, FORCE, ("12.5", "80"), (moment.ANSWER_APPLIES,) * 5, (moment.SCREEN_NO,) * 9,
            record_store.planar_moment_method_identity())
    material = _material(store, pid, comp.component_id)
    _correct_component(store, pid, comp.component_id, 0, "Changed meanwhile")
    revision = sm.declared_planar_moment(snap["ledger"], material)
    with pytest.raises(PlanarMomentRejected) as caught:
        store.append_planar_moment_revision(pid, revision, "k-stale", admit=_admit)
    assert isinstance(caught.value.cause, sm.PlanarMomentStale) and _rows(store) == []


# ─── 5. lifecycle, retry and limits ─────────────────────────────────────────

def test_one_active_per_component_withdrawal_is_terminal_and_kept(store):
    pid = _mech_project(store)
    comp = _declare_store(store, pid, (), "Folding flap")
    _o, stored = _declare_pm(store, pid, comp.component_id)
    with pytest.raises(sm.PlanarMomentActiveExists):
        _declare_pm(store, pid, comp.component_id, key="k-again")
    ledger = store.load_planar_moments(pid)["ledger"]
    store.append_planar_moment_revision(
        pid, sm.withdrawn_planar_moment(ledger, stored.declaration_id, 0), "k-w")
    record = store.load_planar_moments(pid)["ledger"].record_for(stored.declaration_id)
    assert record.withdrawn and len(record.revisions) == 2 and record.current.point_description == POINT
    with pytest.raises(sm.PlanarMomentAlreadyWithdrawn):
        sm.withdrawn_planar_moment(store.load_planar_moments(pid)["ledger"], stored.declaration_id, 1)
    _o, again = _declare_pm(store, pid, comp.component_id, key="k-new")    # a NEW identity
    assert again.declaration_id != stored.declaration_id


def test_the_correction_limit_still_leaves_the_reserved_withdrawal(store):
    pid = _mech_project(store)
    comp = _declare_store(store, pid, (), "Folding flap")
    _o, stored = _declare_pm(store, pid, comp.component_id)
    for n in range(sm.MAX_PLANAR_MOMENT_CORRECTIONS):
        ledger = store.load_planar_moments(pid)["ledger"]
        material = _material(store, pid, comp.component_id, values=(str(n + 1), "80"))
        store.append_planar_moment_revision(
            pid, sm.corrected_planar_moment(ledger, stored.declaration_id, n, material),
            "k-c%d" % n, admit=_admit)
    ledger = store.load_planar_moments(pid)["ledger"]
    with pytest.raises(sm.PlanarMomentCorrectionLimit):
        sm.corrected_planar_moment(ledger, stored.declaration_id, 20,
                                   _material(store, pid, comp.component_id, values=("99", "1")))
    store.append_planar_moment_revision(
        pid, sm.withdrawn_planar_moment(ledger, stored.declaration_id, 20), "k-w")
    assert store.load_planar_moments(pid)["ledger"].record_for(stored.declaration_id).withdrawn


def test_an_exact_retry_writes_nothing_and_a_reused_key_conflicts(store):
    pid = _mech_project(store)
    comp = _declare_store(store, pid, (), "Folding flap")
    snap = store.load_planar_moments(pid)
    revision = sm.declared_planar_moment(snap["ledger"], _material(store, pid, comp.component_id))
    assert store.append_planar_moment_revision(pid, revision, "k1", admit=_admit)[0] \
        == PLANAR_MOMENT_INSERTED
    retry = sm.declared_planar_moment(sm.PlanarMomentLedger(records=()), revision.material)
    outcome, stored = store.append_planar_moment_revision(pid, retry, "k1", admit=_admit)
    assert (outcome, stored.revision_id) == (PLANAR_MOMENT_EXACT_REPLAY, revision.revision_id)
    other = sm.declared_planar_moment(sm.PlanarMomentLedger(records=()),
                                      _material(store, pid, comp.component_id, values=("2", "3")))
    with pytest.raises(PlanarMomentConflict):
        store.append_planar_moment_revision(pid, other, "k1", admit=_admit)
    assert len(_rows(store)) == 1


def test_a_corrupt_history_reads_corrupt_never_partial(store):
    pid = _mech_project(store)
    comp = _declare_store(store, pid, (), "Folding flap")
    _declare_pm(store, pid, comp.component_id)
    store._conn.execute("UPDATE planar_moment_revisions SET event_seq = 7")
    with pytest.raises(PlanarMomentCorrupt):
        store.load_planar_moments(pid)


def test_an_unknown_table_shape_is_refused_and_migration_is_idempotent(tmp_path):
    path = str(tmp_path / "shape.db")
    SqliteRecordStore(path).close()
    again = SqliteRecordStore(path)                       # idempotent
    again.close()
    con = sqlite3.connect(path)
    con.execute("DROP TABLE planar_moment_revisions")
    con.execute("CREATE TABLE planar_moment_revisions (project_id TEXT, other TEXT)")
    con.commit()
    con.close()
    with pytest.raises(sqlite3.DatabaseError):
        SqliteRecordStore(path, create=False)


# ─── 6. the web journey ─────────────────────────────────────────────────────

def _client(tag):
    client, _aid = _client_for("pm-saved-%s@example.com" % tag)
    return client


def _page(c, sid, **args):
    r = c.get(URL % sid, query_string=args)
    return r.status_code, r.get_data(as_text=True)


def _evaluate(c, sid, correct=None, head="0", **over):
    r = c.post(URL % sid, data=_moment_form(**over),
               query_string={"correct": correct, "head": head} if correct else None)
    assert r.status_code == 200
    return r.get_data(as_text=True)


def _save_form(raw):
    block = raw.split("data-pm-save-form", 1)[1].split("</form>", 1)[0]
    hidden = {n: _html.unescape(v) for n, v in re.findall(
        r'<input type="hidden" name="([^"]+)" value="([^"]*)"', block)}
    hidden.pop("csrf_token", None)
    options = re.findall(r'<option value="(cmp-[0-9a-f]{32}:[0-9]+)"', block)
    return hidden, options


def _save(c, sid, raw, target=None, point=POINT, force=FORCE, **over):
    hidden, options = _save_form(raw)
    data = dict(hidden)
    data.update({"component_target": target if target is not None else options[0],
                 "point_description": point, "force_context": force})
    data.update(over)
    return c.post(URL % sid + "/save", data=data)


def _items(raw):
    return re.findall(r'data-pm-item="(pmd-[0-9a-f]{32})"', raw)


def _state(raw):
    return re.findall(r'<span class="pm-state" data-pm-state="([A-Z_]+)"', raw)


def _value(raw):
    m = re.search(r'data-pm-result-value><bdi dir="ltr">([^<]*)</bdi>', raw)
    return m.group(1) if m else None


@pytest.fixture
def mech_client():
    c = _client("mech")
    sid = _start(c, {"idea": SEED, "domain_confirm": "mechanical"})
    _declare(c, sid, name="Folding flap", function="Covers the opening")
    return c, sid


def test_save_reopen_and_recalculate_on_every_render(mech_client):
    c, sid = mech_client
    status, raw = _page(c, sid)
    assert status == 200 and "data-pm-none" in raw and "data-pm-save-form" not in raw
    raw = _evaluate(c, sid)
    hidden, options = _save_form(raw)
    assert len(options) == 1 and hidden["expected_head"] == "none"
    assert re.search(r'<option value="">', raw)                 # nothing pre-selected
    r = _save(c, sid, raw)
    body = r.get_data(as_text=True)
    assert r.status_code == 200 and ui_text.text("UI_PM_MSG_SAVED", "en") in _html.unescape(body)
    status, raw = _page(c, sid)
    assert _state(raw) == ["CURRENT"] and _value(raw) == EXPECTED
    for shown in (POINT, FORCE, "Folding flap", moment.METHOD_ID, "12.5", "80"):
        assert shown in _html.unescape(raw)
    assert "data-pm-sources" in raw
    row = webapp._get_store()._conn.execute("SELECT * FROM planar_moment_revisions").fetchall()
    assert len(row) == 1 and "1000" not in json.dumps(row, default=str)


@pytest.mark.parametrize("over, error", [
    ({"screen_children": moment.SCREEN_YES}, "UI_PM_MSG_NOT_ADMITTED"),
    ({"decl_planar": moment.ANSWER_DOES_NOT_APPLY}, "UI_PM_MSG_NOT_ADMITTED"),
    ({"value_F": "0"}, "UI_PM_MSG_NOT_ADMITTED"),
    ({"point_description": ""}, "UI_PM_MSG_TEXT"),
    ({"force_context": "x" * 301}, "UI_PM_MSG_TEXT"),
    ({"component_target": "not-a-target"}, "UI_PM_MSG_CHOOSE_COMPONENT"),
    ({"component_target": ""}, "UI_PM_MSG_CHOOSE_COMPONENT"),
    ({"expected_head": "forged"}, "UI_PM_MSG_REJECTED"),
    ({"pm_submission": "forged"}, "UI_PM_MSG_NOT_SAVED"),
    ({"surprise": "x"}, "UI_PM_MSG_REJECTED"),
])
def test_a_refused_save_writes_nothing(mech_client, over, error):
    c, sid = mech_client
    raw = _evaluate(c, sid)
    before = _snapshot(c)[0]
    r = _save(c, sid, raw, **over)
    assert r.status_code in (400, 409)
    assert ui_text.text(error, "en") in _html.unescape(r.get_data(as_text=True))
    assert _snapshot(c)[0] == before


def test_a_foreign_component_or_project_is_refused(mech_client):
    c, sid = mech_client
    other = _start(c, {"idea": SEED, "domain_confirm": "mechanical"})
    _declare(c, other, name="Elsewhere", function="Other project")
    _status, raw_other = _page(c, other)
    foreign = webapp._get_store().load_component_inventory_record(other)[1].records[0]
    raw = _evaluate(c, sid)
    before = _snapshot(c)[0]
    r = _save(c, sid, raw, target="%s:0" % foreign.component_id)
    assert r.status_code == 409 and _snapshot(c)[0] == before
    intruder = _client("intruder")
    assert intruder.post(URL % sid + "/save", data={}).status_code in (302, 403, 404)
    assert intruder.get(URL % sid).status_code in (302, 403, 404)


def test_an_integrated_project_offers_only_components_linked_to_its_mechanical_part():
    c = _client("integrated")
    sid = _integrated(c, ELEC)
    subs = webapp._get_store().load_project_subsystems(sid)
    mech_part = next(s for s in subs if s.domain == MECH)
    elec_part = next(s for s in subs if s.domain == ELEC)
    _declare(c, sid, name="Arm", function="Lifts", parts=(mech_part.subsystem_id,))
    _declare(c, sid, name="Sensor", function="Senses", parts=(elec_part.subsystem_id,))
    raw = _evaluate(c, sid)
    hidden, options = _save_form(raw)
    names = re.findall(r'<option value="cmp-[^"]+"[^>]*>([^<]+)</option>', raw)
    assert names == ["Arm"] and len(options) == 1
    inv = webapp._get_store().load_component_inventory_record(sid)[1]
    sensor = next(r for r in inv.records if r.current.display_name == "Sensor")
    r = _save(c, sid, raw, target="%s:0" % sensor.component_id)
    assert r.status_code == 409
    assert ui_text.text("UI_PM_MSG_NOT_ELIGIBLE", "en") in _html.unescape(r.get_data(as_text=True))
    assert _save(c, sid, raw).status_code == 200
    status, page = _page(c, sid)
    assert _state(page) == ["CURRENT"] and mech_part.display_name in _html.unescape(page)


def test_a_component_correction_suspends_the_number_until_reconfirmed(mech_client):
    c, sid = mech_client
    _save(c, sid, _evaluate(c, sid))
    store = webapp._get_store()
    comp = store.load_component_inventory_record(sid)[1].records[0]
    _correct_component(store, sid, comp.component_id, 0, "Folding flap, longer")
    status, raw = _page(c, sid)
    assert _state(raw) == ["NEEDS_RECONFIRMATION"] and _value(raw) is None
    assert ui_text.text("UI_PM_ISSUE_COMPONENT_CHANGED", "en") in _html.unescape(raw)
    declaration_id = _items(raw)[0]
    status, prefilled = _page(c, sid, correct=declaration_id)
    assert 'value="12.5"' in prefilled and "data-pm-correcting" in prefilled
    raw = _evaluate(c, sid, correct=declaration_id)
    hidden, _options = _save_form(raw)
    assert (hidden["declaration_id"], hidden["expected_head"]) == (declaration_id, "0")
    assert _save(c, sid, raw).status_code == 200
    status, raw = _page(c, sid)
    assert _state(raw) == ["CURRENT"] and _value(raw) == EXPECTED


def test_a_changed_method_identity_shows_no_number(mech_client, monkeypatch):
    c, sid = mech_client
    _save(c, sid, _evaluate(c, sid))
    real = record_store.planar_moment_method_identity()
    monkeypatch.setattr(record_store, "planar_moment_method_identity",
                        lambda: real[:3] + ("f" * 64,))
    status, raw = _page(c, sid)
    assert _state(raw) == ["NEEDS_RECONFIRMATION"] and _value(raw) is None
    assert ui_text.text("UI_PM_ISSUE_METHOD_CHANGED", "en") in _html.unescape(raw)


def test_a_refusal_on_re_evaluation_shows_its_reason_and_no_number(mech_client, monkeypatch):
    c, sid = mech_client
    _save(c, sid, _evaluate(c, sid))
    real = moment.evaluate
    monkeypatch.setattr(moment, "evaluate",
                        lambda captured, binding, **kw: {"outcome": moment.KNOWLEDGE_UNAVAILABLE,
                                                         "owner_state": None,
                                                         "owner_reason": None, "result": None})
    status, raw = _page(c, sid)
    assert _state(raw) == ["RESULT_UNAVAILABLE"] and _value(raw) is None
    monkeypatch.setattr(moment, "evaluate", real)


def test_withdrawal_needs_confirmation_and_keeps_the_history(mech_client):
    c, sid = mech_client
    _save(c, sid, _evaluate(c, sid))
    status, raw = _page(c, sid)
    block = raw.split("data-pm-withdraw-form", 1)[1].split("</form>", 1)[0]
    data = {n: _html.unescape(v) for n, v in re.findall(
        r'<input type="hidden" name="([^"]+)" value="([^"]*)"', block)}
    data.pop("csrf_token")
    r = c.post(URL % sid + "/withdraw", data=data)
    assert r.status_code == 400
    assert _state(_page(c, sid)[1]) == ["CURRENT"]
    r = c.post(URL % sid + "/withdraw", data=dict(data, withdraw_confirm="yes"))
    assert r.status_code == 200
    status, raw = _page(c, sid)
    assert _state(raw) == ["WITHDRAWN"] and _value(raw) is None and POINT in _html.unescape(raw)
    assert "data-pm-withdraw-form" not in raw
    assert len(webapp._get_store()._conn.execute(
        "SELECT * FROM planar_moment_revisions").fetchall()) == 2


def test_an_unreadable_history_reads_unavailable_never_none(mech_client, monkeypatch):
    c, sid = mech_client
    _save(c, sid, _evaluate(c, sid))
    store = webapp._get_store()

    def boom(_pid):
        raise PlanarMomentCorrupt("synthetic")
    monkeypatch.setattr(store, "load_planar_moments", boom)
    status, raw = _page(c, sid)
    assert status == 503 and "data-pm-unavailable" in raw and "data-pm-none" not in raw


def test_the_calculation_post_and_get_still_write_nothing(mech_client):
    c, sid = mech_client
    before = _snapshot(c)
    _evaluate(c, sid)
    _page(c, sid)
    assert _snapshot(c) == before


def test_the_page_states_the_boundary_in_arabic(mech_client):
    c, sid = mech_client
    c.post("/ui-language", data={"lang": "ar"})
    raw = _evaluate(c, sid)
    text = _html.unescape(raw)
    for key in ("UI_PM_SAVE_HEADING", "UI_PM_SAVE_NOTE", "UI_PM_SAVED_INTRO", "UI_PM_LIMIT_NOTE"):
        assert ui_text.text(key, "ar") in text
    assert _save(c, sid, raw).status_code == 200
    text = _html.unescape(_page(c, sid)[1])
    assert ui_text.text("UI_PM_STATE_CURRENT", "ar") in text


def test_every_new_copy_key_has_english_and_arabic():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_PM_")]
    assert len(keys) >= 40
    for key in keys:
        assert ui_text.UI_STRINGS[key].get("en") and ui_text.UI_STRINGS[key].get("ar"), key
    for state in ("CURRENT", "NEEDS_RECONFIRMATION", "RESULT_UNAVAILABLE", "WITHDRAWN"):
        assert ui_text.has_string("UI_PM_STATE_" + state)
    for issue in sm.PM_ISSUES:
        assert ui_text.has_string("UI_PM_ISSUE_" + issue)


def test_the_calculation_owner_and_consumer_stay_stateless():
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    for module in ("engine/deterministic_calculation.py", "engine/cap13_planar_moment.py",
                   "engine/cap13_planar_moment_method.py"):
        source = (root / module).read_text(encoding="utf-8")
        # each reads only its own governed artifact; none gains a store
        for banned in ("sqlite", "record_store", "planar_moment_revisions", "INSERT",
                       "subsystem_model"):
            assert banned not in source, (module, banned)
    model = (root / "engine/subsystem_model.py").read_text(encoding="utf-8")
    for banned in ("sqlite", "open(", "json", "hashlib"):
        assert banned not in model, banned          # the semantic owner does no IO
    assert os.environ.get("INVENTORAI_DB_PATH")


def test_csrf_and_authorization_guard_both_new_routes(mech_client):
    c, sid = mech_client
    raw = _evaluate(c, sid)
    hidden, options = _save_form(raw)
    data = dict(hidden, component_target=options[0], point_description=POINT, force_context=FORCE)
    rows = lambda: webapp._get_store()._conn.execute(          # noqa: E731
        "SELECT * FROM planar_moment_revisions").fetchall()
    for path in ("/save", "/withdraw"):
        assert webapp.app.test_client().post(URL % sid + path, data=data).status_code == 403
        other = _client("other-%s" % path.strip("/"))
        response = other.post(URL % sid + path, data=data)
        assert response.status_code == 302 and "data-pm-" not in response.get_data(as_text=True)
    assert rows() == []


def test_a_recoverable_refusal_keeps_the_forms_the_draft_and_the_correction(mech_client):
    """Codex review (PR #960): a save refusal must not hide the forms - the
    inventor fixes the field on the returned page and retries."""
    c, sid = mech_client
    r = _save(c, sid, _evaluate(c, sid), point="")
    body = r.get_data(as_text=True)
    assert r.status_code == 400 and "data-pm-error" in body
    assert "data-pm-save-form" in body and "data-cap13m-form" in body and "data-pm-saved" in body
    assert FORCE in _html.unescape(body)                       # the draft is kept
    assert _save(c, sid, body).status_code == 200            # fixed and retried on the same page
    declaration_id = _items(_page(c, sid)[1])[0]
    raw = _evaluate(c, sid, correct=declaration_id)
    r = _save(c, sid, raw, force="")
    body = r.get_data(as_text=True)
    hidden, _options = _save_form(body)
    assert r.status_code == 400 and hidden["declaration_id"] == declaration_id
    assert hidden["expected_head"] == "0" and "data-pm-correcting" in body
    raw_page = _page(c, sid)[1]
    block = raw_page.split("data-pm-withdraw-form", 1)[1].split("</form>", 1)[0]
    data = {n: _html.unescape(v) for n, v in re.findall(
        r'<input type="hidden" name="([^"]+)" value="([^"]*)"', block)}
    data.pop("csrf_token")
    r = c.post(URL % sid + "/withdraw", data=data)            # no confirmation ticked
    body = r.get_data(as_text=True)
    assert r.status_code == 400 and "data-pm-error" in body and "data-pm-withdraw-form" in body


def test_a_refused_correction_write_keeps_the_correction_identity(mech_client):
    """Codex review (PR #960): an unchanged correction (a write-level refusal)
    keeps correction mode; only a confirmed save clears it."""
    c, sid = mech_client
    _save(c, sid, _evaluate(c, sid))
    declaration_id = _items(_page(c, sid)[1])[0]
    raw = _evaluate(c, sid, correct=declaration_id)
    r = _save(c, sid, raw)                                     # identical to the saved one
    body = r.get_data(as_text=True)
    assert r.status_code == 409
    assert ui_text.text("UI_PM_MSG_UNCHANGED", "en") in _html.unescape(body)
    hidden, options = _save_form(body)
    assert "data-pm-correcting" in body and len(options) == 1
    assert (hidden["declaration_id"], hidden["expected_head"]) == (declaration_id, "0")
    r = _save(c, sid, body.replace('value="12.5"', 'value="25"'))   # edit and retry here
    assert r.status_code == 200 and "data-pm-correcting" not in r.get_data(as_text=True)
    assert _value(_page(c, sid)[1]) == "2000.0 N·mm"


@pytest.mark.parametrize("over, error", [
    ({"component_target": ""}, "UI_PM_MSG_CHOOSE_COMPONENT"),
    ({"point_description": ""}, "UI_PM_MSG_TEXT"),
    ({"screen_children": moment.SCREEN_YES}, "UI_PM_MSG_NOT_ADMITTED"),
])
def test_every_recoverable_save_refusal_keeps_inputs_and_descriptions(mech_client, over, error):
    """Codex review (PR #960), fixed at the root: once the calculation inputs
    are captured, every save refusal shows them, the descriptions and the
    forms back - never a blank page."""
    c, sid = mech_client
    r = _save(c, sid, _evaluate(c, sid), **over)
    body = _html.unescape(r.get_data(as_text=True))
    assert r.status_code in (400, 409) and ui_text.text(error, "en") in body
    assert 'value="12.5"' in body and 'value="80"' in body           # calculation inputs
    assert "data-cap13m-form" in body and "data-pm-saved" in body
    if error != "UI_PM_MSG_NOT_ADMITTED":
        # admitted: the save form is back with both descriptions, ready to retry
        assert "data-pm-save-form" in body and FORCE in body
        if "point_description" not in over:
            assert POINT in body
    else:
        # not admitted (reachable only by a tampered form or a method change
        # between showing and saving): no save form, the refusal reason shown
        assert "data-pm-save-form" not in body and "data-cap13m-outcome" in body


def test_a_correction_opened_in_another_tab_is_refused_as_stale(mech_client):
    """Codex review (PR #960): the revision opened for correction travels
    through the calculation step, so tab A cannot silently overwrite tab B."""
    c, sid = mech_client
    _save(c, sid, _evaluate(c, sid))
    page = _page(c, sid)[1]
    declaration_id = _items(page)[0]
    link = re.search(r'href="([^"]*correct=%s[^"]*)" data-pm-correct' % declaration_id, page)
    assert link and "head=0" in _html.unescape(link.group(1))
    tab_a = _evaluate(c, sid, correct=declaration_id, head="0")           # opened revision 0
    tab_b = _evaluate(c, sid, correct=declaration_id, head="0", F="25")
    assert _save(c, sid, tab_b).status_code == 200                          # now revision 1
    assert _save_form(tab_a)[0]["expected_head"] == "0"
    r = _save(c, sid, tab_a, point="Tab A wording")
    assert r.status_code == 409
    assert ui_text.text("UI_PM_MSG_STALE", "en") in _html.unescape(r.get_data(as_text=True))
    assert _value(_page(c, sid)[1]) == "2000.0 N·mm"                       # B's change kept
    # a re-render of tab A after the calculation still carries revision 0
    again = _evaluate(c, sid, correct=declaration_id, head="0", F="30")
    assert _save_form(again)[0]["expected_head"] == "0"
    # a calculation POST that omits the opened revision is not in correction mode
    plain = c.post(URL % sid, data=_moment_form(), query_string={"correct": declaration_id})
    assert "data-pm-correcting" not in plain.get_data(as_text=True)
