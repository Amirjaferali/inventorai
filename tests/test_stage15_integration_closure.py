"""Stage 15 — Integration Evidence & IRL-Compatible View — Closure.

For the current Mechanical + Electrical / Electronics integrated scope:

  * an optional Owner-declared DEPENDENCY per durable interface (current
    value, ``engine/subsystem_model.py``; one additive sidecar keyed by
    ``interface_id``; one-way persists the exact dependent / depends-on part
    ids, mutual is explicit; clear removes the row) saved by the SAME
    preparation Save; it changes no interface, preparation, observation,
    landscape, plan, gap, progression or readiness truth;
  * INTEGRATION evidence through the EXISTING shared evidence owner
    (``engine/commercial_evidence.py``): closed topics, OWNER_STATED /
    UNVALIDATED, append-only supersession and withdrawal, and exactly ONE
    immutable interface anchor per Integration event in ONE additive sidecar
    committed atomically with its row; load fails closed on any anchor defect;
  * a fresh signed submission identity per form with a material-independent
    durable key: exact retry (also after restart) returns the stored pair; the
    same identity with other material is a conflict; unknown stays UNKNOWN;
  * a fourth readiness-snapshot row "Integration" (INSUFFICIENT_EVIDENCE only;
    active items only) and a read-only per-interface status block;
  * report, PDF and Structured Export unchanged.
"""
import html as _html
import re

import pytest

import web.app as appmod
from engine import account_credentials as _acct
from engine import commercial_evidence as ce
from engine import readiness_snapshot as rs
from engine import subsystem_model as sm
from engine.idea_state import IdeaState
from engine.record_store import (
    EVIDENCE_EXACT_REPLAY, IntegrationEvidenceConflict,
    IntegrationEvidenceRejected, InterfaceDependenciesCorrupt,
    InterfacePreparationRejected, StoreError)
from engine.requirement_landscape import derive_requirement_landscape
from engine.validation_plan import derive_validation_plan
from tests.csrf_client import csrf_client
from tests.test_stage15_integrated_invention_entry import _pair, _visible
from tests.test_stage15_interface_preparation import (
    F_C, _integrated_with_interface, _prep_rows, _save)
from tests.test_stage15_interface_observations import (
    _events, _observe, _record_form)
from tests.test_stage15_subsystem_interface_declaration import (
    _FailOn, _declare, _ifc, _new_project, _raw)
from tests.test_stage19_durable_success_criteria import (
    _progression_snapshot, _restart)
from web import ui_text

PW = "correct horse battery staple"
PREP = "/session/%s/interface-preparation"
IEV = "/session/%s/integration-evidence"
DEP_TABLE = "subsystem_interface_dependencies"
ANCHORS = "integration_evidence_anchors"
ITEM = {
    "topic": "interface_test",
    "subject_text": "Arm-to-board connector",
    "statement_text": "The connector held through 50 open/close cycles.",
    "source_identity": "My own bench test",
    "occurred_on": "2026-09-01",
    "scope_text": "One prototype at room temperature",
    "limitation_text": "Not tested under vibration or heat",
}
TEXT = tuple(k for k in ITEM if k != "topic")


def _login(c, email):
    accounts = appmod._get_account_store()
    aid = _acct.new_account_id()
    accounts.create_account(aid, _acct.normalize_email(email), _acct.hash_password(PW),
                            "2026-01-01T00:00:00.000000Z", status="active")
    accounts.mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    c.post("/login", data={"email": email, "password": PW})


@pytest.fixture
def owner():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        _login(c, "s15-closure@example.com")
        sid, ifc = _integrated_with_interface(c)
        yield c, sid, ifc


@pytest.fixture
def anonymous():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        sid, ifc = _integrated_with_interface(c)
        yield c, sid, ifc


def _store():
    return appmod._get_store()


def _fk_raw(sql, params=()):
    """One raw statement with foreign-key enforcement ON (the store's own
    connection setting), so the schema backstops are exercised as written."""
    import os
    import sqlite3
    conn = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute(sql, params)
        conn.commit()
    finally:
        conn.close()


def _raw_page(c, sid):
    r = c.get(PREP % sid)
    assert r.status_code == 200, r.status_code
    return r.get_data(as_text=True)


def _body(resp):
    return _html.unescape(resp.get_data(as_text=True))


def _hidden(body):
    return {k: _html.unescape(v) for k, v in re.findall(
        r'<input type="hidden" name="([^"]+)" value="([^"]*)"', body)}


def _iev_forms(raw):
    out = []
    for attrs, body in re.findall(
            r'<form method="POST" action="[^"]*integration-evidence"([^>]*)>(.*?)</form>',
            raw, re.S):
        kind = re.search(r"data-iev-(record|correct|withdraw)", attrs).group(1)
        out.append((kind, _hidden(body)))
    return out


def _form(c, sid, kind, interface_id=None, target=None):
    [form] = [f for k, f in _iev_forms(_raw_page(c, sid)) if k == kind
              and (interface_id is None or f["interface_id"] == interface_id)
              and (target is None or f.get("supersedes_evidence_id") == target)]
    return form


def _record(c, sid, iid, **over):
    data = dict(_form(c, sid, "record", interface_id=iid))
    data.update(ITEM)
    data.update(over)
    return c.post(IEV % sid, data=data), data


def _correct(c, sid, target, **over):
    data = dict(_form(c, sid, "correct", target=target))
    data.update({k: ITEM[k] for k in TEXT})
    data.update(over)
    return c.post(IEV % sid, data=data), data


def _withdraw(c, sid, target):
    data = dict(_form(c, sid, "withdraw", target=target))
    return c.post(IEV % sid, data=data), data


def _history(sid):
    return _store().load_integration_evidence(sid)


def _anchor_rows(sid):
    _store()
    return _raw("SELECT evidence_id, interface_id FROM %s WHERE project_id = ? "
                "ORDER BY evidence_id" % ANCHORS, (sid,))


def _evidence_rows(sid):
    _store()
    return _raw("SELECT evidence_id, dimension, withdrawn, supersedes_evidence_id "
                "FROM readiness_evidence WHERE project_id = ? ORDER BY evidence_seq",
                (sid,))


def _dep_rows(sid):
    _store()
    return _raw("SELECT interface_id, dependency_kind, dependent_subsystem_id, "
                "depends_on_subsystem_id, note FROM %s WHERE project_id = ?"
                % DEP_TABLE, (sid,))


def _dep_save(c, sid, iid, choice, note=""):
    shown = _hidden(_raw_page(c, sid))
    data = {"dep_choice__" + iid: choice, "dep_note__" + iid: note,
            "dep_base_choice__" + iid: shown["dep_base_choice__" + iid],
            "dep_base_note__" + iid: shown["dep_base_note__" + iid]}
    return c.post(PREP % sid, data=data)


def _one_way(ifc, reverse=False):
    a, b = ifc.subsystem_a_id, ifc.subsystem_b_id
    if reverse:
        a, b = b, a
    return "one_way:%s:%s" % (a, b), a, b


def _second_interface(c, sid, first):
    assert _declare(c, sid, "Bolted mounting between the arm and the board.").status_code == 302
    [second] = [i for i in _store().load_subsystem_interfaces(sid)
                if i.interface_id != first.interface_id]
    return second


def _live(sid):
    return appmod.SESSION_STORE[sid]["state"]


def _section(page, key):
    start = page.index(ui_text.text(key, "en"))
    return _visible(re.sub(r"<style.*?</style>", " ", page[start:], flags=re.S))


def _snapshot_rows(c, sid):
    page = c.get("/session/%s" % sid).get_data(as_text=True)
    return page, re.findall(r'<li class="readiness-snapshot-row"[^>]*data-rs-dimension="([a-z]+)"'
                            r'[^>]*data-rs-disposition="([A-Z_]+)"', page)


# ==========================================================================
# 1. The Owner-declared dependency (engine owner)
# ==========================================================================
def test_the_dependency_owner_accepts_only_exact_endpoint_declarations():
    pair = _pair()
    ifc = _ifc(pair)
    a, b = ifc.subsystem_a_id, ifc.subsystem_b_id
    for dependent, on in ((a, b), (b, a)):
        dep = sm.InterfaceDependency(ifc.interface_id, sm.DEPENDENCY_ONE_WAY, dependent, on)
        assert sm.check_interface_dependency(dep, ifc) == dep
    mutual = sm.InterfaceDependency(ifc.interface_id, sm.DEPENDENCY_MUTUAL, note="Both ways.")
    assert sm.check_interface_dependency(mutual, ifc) == mutual
    for bad in (
            sm.InterfaceDependency(ifc.interface_id, sm.DEPENDENCY_ONE_WAY, a, a),
            sm.InterfaceDependency(ifc.interface_id, sm.DEPENDENCY_ONE_WAY, a, None),
            sm.InterfaceDependency(ifc.interface_id, sm.DEPENDENCY_ONE_WAY, a, "sub-" + "f" * 32),
            sm.InterfaceDependency(ifc.interface_id, sm.DEPENDENCY_MUTUAL, a, b),
            sm.InterfaceDependency(ifc.interface_id, "depends", a, b),
            sm.InterfaceDependency("ifc-" + "0" * 32, sm.DEPENDENCY_MUTUAL),
            sm.InterfaceDependency(ifc.interface_id, sm.DEPENDENCY_MUTUAL, note=""),
            sm.InterfaceDependency(ifc.interface_id, sm.DEPENDENCY_MUTUAL, note="a\x00b"),
            sm.InterfaceDependency(ifc.interface_id, sm.DEPENDENCY_MUTUAL,
                                   note="x" * (sm.MAX_INTERFACE_DEPENDENCY_NOTE_LENGTH + 1))):
        with pytest.raises(sm.InterfaceError):
            sm.check_interface_dependency(bad, ifc)


# ==========================================================================
# 2. The dependency through the preparation page / Save
# ==========================================================================
def test_the_page_offers_not_declared_both_directions_and_mutual(owner):
    c, sid, ifc = owner
    raw = _raw_page(c, sid)
    values = re.findall(r'name="dep_choice__%s" value="([^"]*)"' % ifc.interface_id, raw)
    assert values == ["", _one_way(ifc)[0], _one_way(ifc, reverse=True)[0], "mutual"]
    assert re.search(r'name="dep_choice__%s" value="" checked' % ifc.interface_id, raw)
    status = _section(_html.unescape(raw), "UI_S15_ST_HEADING")
    assert ui_text.text("UI_S15_DEP_NOT_DECLARED", "en") in status


@pytest.mark.parametrize("reverse", [False, True])
def test_a_one_way_dependency_persists_the_exact_dependent_and_depends_on_ids(owner, reverse):
    c, sid, ifc = owner
    choice, dependent, on = _one_way(ifc, reverse=reverse)
    r = _dep_save(c, sid, ifc.interface_id, choice, "  The board drives the arm motor.  ")
    assert r.status_code == 200 and appmod.S15_PREP_SAVED_MESSAGE in _body(r)
    assert _dep_rows(sid) == [(ifc.interface_id, "one_way", dependent, on,
                               "The board drives the arm motor.")]
    [dep] = _store().load_interface_dependencies(sid)
    assert (dep.dependent_subsystem_id, dep.depends_on_subsystem_id) == (dependent, on)


def test_mutual_is_explicit_and_clearing_removes_the_row(owner):
    c, sid, ifc = owner
    assert _dep_save(c, sid, ifc.interface_id, "mutual").status_code == 200
    assert _dep_rows(sid) == [(ifc.interface_id, "mutual", None, None, None)]
    r = _dep_save(c, sid, ifc.interface_id, "")
    assert r.status_code == 200 and appmod.S15_PREP_SAVED_MESSAGE in _body(r)
    assert _dep_rows(sid) == []
    assert _store().load_interface_dependencies(sid) == ()


@pytest.mark.parametrize("choice,note,message", [
    ("", "An orphan explanation.", "S15_DEP_NOTE_ALONE_MESSAGE"),
    ("one_way:sub-x:sub-y", "", "S15_DEP_INVALID_MESSAGE"),
    ("sideways", "", "S15_DEP_INVALID_MESSAGE"),
    ("mutual", "x" * 301, "S15_DEP_TOO_LONG_MESSAGE"),
])
def test_an_invalid_dependency_saves_nothing(owner, choice, note, message):
    c, sid, ifc = owner
    r = _dep_save(c, sid, ifc.interface_id, choice, note)
    assert r.status_code == 400
    assert getattr(appmod, message) in _body(r)
    assert _dep_rows(sid) == []


def test_a_dependency_on_a_same_endpoint_or_another_interface_is_refused(owner):
    c, sid, ifc = owner
    a = ifc.subsystem_a_id
    assert _dep_save(c, sid, ifc.interface_id, "one_way:%s:%s" % (a, a)).status_code == 400
    shown = _hidden(_raw_page(c, sid))
    data = {"dep_choice__ifc-" + "0" * 32: "mutual", "dep_note__ifc-" + "0" * 32: "",
            "dep_base_choice__ifc-" + "0" * 32: "", "dep_base_note__ifc-" + "0" * 32: ""}
    assert "dep_base_choice__ifc-" + "0" * 32 not in shown
    r = c.post(PREP % sid, data=data)
    assert r.status_code == 400 and appmod.S15_PREP_UNKNOWN_INTERFACE_MESSAGE in _body(r)
    assert _dep_rows(sid) == []


def test_a_stale_untouched_dependency_field_never_overwrites_newer_truth(owner):
    c, sid, ifc = owner
    stale = _hidden(_raw_page(c, sid))               # displays "not declared"
    assert _dep_save(c, sid, ifc.interface_id, "mutual").status_code == 200
    data = {"dep_choice__" + ifc.interface_id: "",
            "dep_note__" + ifc.interface_id: "",
            "dep_base_choice__" + ifc.interface_id: stale["dep_base_choice__" + ifc.interface_id],
            "dep_base_note__" + ifc.interface_id: stale["dep_base_note__" + ifc.interface_id]}
    r = c.post(PREP % sid, data=data)
    assert r.status_code == 200 and appmod.S15_PREP_UNCHANGED_MESSAGE in _body(r)
    assert _dep_rows(sid) == [(ifc.interface_id, "mutual", None, None, None)]


def test_a_dependency_changes_no_interface_preparation_observation_or_derived_truth(owner):
    c, sid, ifc = owner
    _save(c, sid, {(F_C, ifc.interface_id): "Indoor, 20 C."})
    _observe(c, sid, _record_form(c, sid, ifc.interface_id), "It opened.")
    before_ifc = _store().load_subsystem_interfaces(sid)
    before_prep = _prep_rows(sid)
    before_obs = _events(sid)
    before_progress = _progression_snapshot(sid)
    state = _live(sid)
    before_landscape = derive_requirement_landscape(state)
    before_plan = derive_validation_plan(state)
    before_ledger = _raw("SELECT COUNT(*) FROM records WHERE project_id = ?", (sid,))
    assert _dep_save(c, sid, ifc.interface_id, _one_way(ifc)[0], "Board powers arm.").status_code == 200
    assert _store().load_subsystem_interfaces(sid) == before_ifc
    assert _prep_rows(sid) == before_prep and _events(sid) == before_obs
    assert _progression_snapshot(sid) == before_progress
    assert _raw("SELECT COUNT(*) FROM records WHERE project_id = ?", (sid,)) == before_ledger
    state = _live(sid)
    assert derive_requirement_landscape(state) == before_landscape
    assert derive_validation_plan(state) == before_plan
    assert _evidence_rows(sid) == []                    # never converted into evidence


def test_a_dependency_commit_then_error_is_confirmed_saved_by_reload(owner):
    c, sid, ifc = owner
    shown = _hidden(_raw_page(c, sid))
    data = {"dep_choice__" + ifc.interface_id: "mutual", "dep_note__" + ifc.interface_id: "",
            "dep_base_choice__" + ifc.interface_id: shown["dep_base_choice__" + ifc.interface_id],
            "dep_base_note__" + ifc.interface_id: shown["dep_base_note__" + ifc.interface_id]}
    store = _store()
    real = store._conn
    store._conn = _FailOn(real, commit_then=True)
    try:
        r = c.post(PREP % sid, data=data)
    finally:
        store._conn = real
    assert r.status_code == 200 and appmod.S15_PREP_SAVED_MESSAGE in _body(r)
    assert _dep_rows(sid) == [(ifc.interface_id, "mutual", None, None, None)]


def test_the_observation_context_still_freezes_exactly_three_preparation_fields(owner):
    c, sid, ifc = owner
    _dep_save(c, sid, ifc.interface_id, "mutual", "Each needs the other.")
    _observe(c, sid, _record_form(c, sid, ifc.interface_id), "Opened in 2 s.")
    [ev] = _events(sid)
    import dataclasses
    assert [f.name for f in dataclasses.fields(ev.context)] == [
        "operating_conditions", "acceptance_criterion", "evidence_needed"]
    cols = [r[1] for r in _raw("PRAGMA table_info(subsystem_interface_observations)")]
    assert not any("depend" in col for col in cols)


def test_an_unreadable_dependency_collection_reads_unavailable_not_absent(owner, monkeypatch):
    c, sid, ifc = owner
    store = _store()

    def boom(_pid):
        raise InterfaceDependenciesCorrupt("injected")
    monkeypatch.setattr(store, "load_interface_dependencies", boom)
    page = _html.unescape(_raw_page(c, sid))
    status = _section(page, "UI_S15_ST_HEADING").split(
        ui_text.text("UI_S15_PREP_FORM_HEADING", "en"))[0]
    assert ui_text.text("UI_S15_ST_UNAVAILABLE", "en") in status
    assert ui_text.text("UI_S15_DEP_NOT_DECLARED", "en") not in status
    assert 'name="dep_choice__' not in page                 # nothing offered to overwrite
    r = _save(c, sid, {(F_C, ifc.interface_id): "Outdoors."})   # preparation still saves
    assert r.status_code == 200 and appmod.S15_PREP_SAVED_MESSAGE in _body(r)


def test_the_dependency_store_validates_membership_and_corrupt_rows_fail_closed(owner):
    c, sid, ifc = owner
    store = _store()
    with pytest.raises(InterfacePreparationRejected):
        store.apply_interface_preparation_delta(
            sid, {}, dependency_delta={"ifc-" + "0" * 32: None})
    with pytest.raises(InterfacePreparationRejected):
        store.apply_interface_preparation_delta(sid, {}, dependency_delta={
            ifc.interface_id: sm.InterfaceDependency(
                ifc.interface_id, sm.DEPENDENCY_ONE_WAY, ifc.subsystem_a_id,
                ifc.subsystem_a_id)})
    # A row naming a part of ANOTHER interface pairing is refused by the
    # loader even if it was smuggled past the write path.
    _raw("INSERT INTO %s VALUES (?, ?, 'one_way', ?, ?, NULL)" % DEP_TABLE,
         (sid, ifc.interface_id, ifc.subsystem_b_id, ifc.subsystem_b_id),
         fk=False, ignore_checks=True)
    with pytest.raises(InterfaceDependenciesCorrupt):
        store.load_interface_dependencies(sid)


def test_the_dependency_schema_backstops_ids_kind_and_note():
    import sqlite3
    store = _store()
    pid, subs = _new_project(store)
    item = _ifc(subs)
    store.append_subsystem_interface(pid, item, "dep-key")
    a, b = item.subsystem_a_id, item.subsystem_b_id
    for row in ((item.interface_id, "one_way", a, a, None),
                (item.interface_id, "mutual", a, None, None),
                (item.interface_id, "both", None, None, None),
                (item.interface_id, "mutual", None, None, ""),
                ("ifc-" + "1" * 32, "mutual", None, None, None)):
        with pytest.raises(sqlite3.IntegrityError):
            _fk_raw("INSERT INTO %s VALUES (?, ?, ?, ?, ?, ?)" % DEP_TABLE, (pid,) + row)
    _raw("INSERT INTO %s VALUES (?, ?, 'one_way', ?, ?, 'ok')" % DEP_TABLE,
         (pid, item.interface_id, b, a))
    [dep] = store.load_interface_dependencies(pid)
    assert (dep.dependent_subsystem_id, dep.depends_on_subsystem_id) == (b, a)


# ==========================================================================
# 3. Integration evidence: owner vocabulary and anchors
# ==========================================================================
def test_integration_is_one_more_dimension_of_the_existing_owner():
    assert ce.DIMENSION_INTEGRATION == "INTEGRATION"
    assert ce.DIMENSION_INTEGRATION in ce.DIMENSIONS
    assert ce.DIMENSION_INTEGRATION in ce.ACTIVE_DIMENSIONS
    assert ce.TOPICS_BY_DIMENSION[ce.DIMENSION_INTEGRATION] == ce.INTEGRATION_TOPICS == (
        "interface_test", "interface_inspection", "interface_specification",
        "interface_review")
    assert ce.CLAIM_STATUSES == (ce.CLAIM_STATUS_UNVALIDATED,)


def test_record_writes_one_unvalidated_row_and_exactly_one_anchor(owner):
    c, sid, ifc = owner
    r, _data = _record(c, sid, ifc.interface_id)
    assert r.status_code == 200 and appmod.S15_IEV_SAVED_MESSAGE in _body(r)
    history, anchored = _history(sid)
    [row] = history
    assert row.dimension == "INTEGRATION" and row.topic == "interface_test"
    assert row.claim_status == ce.CLAIM_STATUS_UNVALIDATED
    assert row.provenance == appmod._CEV_PROVENANCE and not row.withdrawn
    assert all(getattr(row, k) == ITEM[k] for k in TEXT)
    assert anchored == {row.evidence_id: ifc.interface_id}
    assert _anchor_rows(sid) == [(row.evidence_id, ifc.interface_id)]


def test_correct_and_withdraw_append_and_keep_the_anchor(owner):
    c, sid, ifc = owner
    _record(c, sid, ifc.interface_id)
    [first], _ = _history(sid)
    r, _ = _correct(c, sid, first.evidence_id, statement_text="Held through 80 cycles.")
    assert r.status_code == 200 and appmod.S15_IEV_CORRECTED_MESSAGE in _body(r)
    history, anchored = _history(sid)
    second = history[1]
    assert second.supersedes_evidence_id == first.evidence_id and second.topic == first.topic
    r, _ = _withdraw(c, sid, second.evidence_id)
    assert r.status_code == 200 and appmod.S15_IEV_WITHDRAWN_MESSAGE in _body(r)
    history, anchored = _history(sid)
    third = history[2]
    assert third.withdrawn and third.supersedes_evidence_id == second.evidence_id
    assert third.statement_text == "Held through 80 cycles."          # carried verbatim
    assert set(anchored.values()) == {ifc.interface_id} and len(anchored) == 3
    assert [e for e, _ in _anchor_rows(sid)] == sorted(r.evidence_id for r in history)
    view = ce.integration_evidence_by_interface(history, anchored, ifc.interface_id)
    assert view == {"active": [], "history": 3}
    assert rs.integration_row(history)["recorded_items"] == 0


def test_a_correction_cannot_move_to_another_interface(owner):
    c, sid, ifc = owner
    second = _second_interface(c, sid, ifc)
    _record(c, sid, ifc.interface_id)
    [first], _ = _history(sid)
    data = dict(_form(c, sid, "correct", target=first.evidence_id))
    data.update({k: ITEM[k] for k in TEXT})
    data["interface_id"] = second.interface_id
    r = c.post(IEV % sid, data=data)
    assert r.status_code == 400 and appmod.S15_IEV_STALE_MESSAGE in _body(r)
    assert len(_history(sid)[0]) == 1
    store = _store()
    moved = ce.make_readiness_evidence(
        evidence_id=store.new_readiness_evidence_id(), evidence_seq=0,
        dimension="INTEGRATION", topic=first.topic,
        **{k: getattr(first, k) for k in TEXT},
        provenance=appmod._CEV_PROVENANCE,
        supersedes_evidence_id=first.evidence_id, event_key="k" * 32,
        recorded_iteration=0, recorded_at="2026-10-01T00:00:00.000000Z")
    with pytest.raises(IntegrationEvidenceRejected):
        store.append_integration_evidence(sid, moved, second.interface_id)


def test_an_unknown_or_foreign_interface_records_nothing(owner):
    c, sid, ifc = owner
    r, _ = _record(c, sid, ifc.interface_id, interface_id="ifc-" + "0" * 32)
    assert r.status_code == 400 and appmod.S15_IEV_NOT_CURRENT_MESSAGE in _body(r)
    store = _store()
    other, subs = _new_project(store)
    foreign = _ifc(subs, "Another project's interaction.")
    store.append_subsystem_interface(other, foreign, "foreign-key")
    r, _ = _record(c, sid, ifc.interface_id, interface_id=foreign.interface_id)
    assert r.status_code == 400 and _evidence_rows(sid) == [] and _anchor_rows(sid) == []


def test_closed_topics_and_the_text_policy_are_enforced(owner):
    c, sid, ifc = owner
    r, _ = _record(c, sid, ifc.interface_id, topic="target_customer")
    assert r.status_code == 400 and appmod.S15_IEV_NOT_SAVED_MESSAGE in _body(r)
    r, _ = _record(c, sid, ifc.interface_id, limitation_text="  ")
    assert r.status_code == 400 and appmod.S15_IEV_TEXT_REJECTED_MESSAGE in _body(r)
    assert ITEM["statement_text"] in _body(r)                     # the draft is kept
    r, _ = _record(c, sid, ifc.interface_id, claim_status="VALIDATED")
    assert r.status_code == 400                                   # field allowlist
    assert _evidence_rows(sid) == []


def test_the_shared_writer_refuses_an_unanchored_integration_row(owner):
    _c, sid, _ifc_ = owner
    store = _store()
    row = ce.make_readiness_evidence(
        evidence_id=store.new_readiness_evidence_id(), evidence_seq=0,
        dimension="INTEGRATION", topic="interface_test",
        **{k: ITEM[k] for k in TEXT}, provenance=appmod._CEV_PROVENANCE,
        event_key="u" * 32, recorded_iteration=0,
        recorded_at="2026-10-01T00:00:00.000000Z")
    with pytest.raises(StoreError):
        store.append_readiness_evidence(sid, row)
    assert _evidence_rows(sid) == []


def test_the_row_and_its_anchor_commit_atomically(owner):
    c, sid, ifc = owner
    form = _form(c, sid, "record", interface_id=ifc.interface_id)
    store = _store()
    real = store._conn
    store._conn = _FailOn(real, prefix="INSERT INTO " + ANCHORS)
    try:
        r = c.post(IEV % sid, data=dict(form, **ITEM))
    finally:
        store._conn = real
    assert r.status_code == 503 and appmod.S15_IEV_NOT_SAVED_MESSAGE in _body(r)
    assert _evidence_rows(sid) == [] and _anchor_rows(sid) == []


@pytest.mark.parametrize("defect", [
    "missing", "duplicate_target", "non_integration", "chain_moved", "unknown_evidence"])
def test_load_fails_closed_on_any_anchor_defect(owner, defect):
    c, sid, ifc = owner
    second = _second_interface(c, sid, ifc)
    _record(c, sid, ifc.interface_id)
    [first], _ = _history(sid)
    if defect == "missing":
        _raw("DELETE FROM %s WHERE project_id = ?" % ANCHORS, (sid,))
    elif defect == "duplicate_target":
        _correct(c, sid, first.evidence_id, statement_text="Corrected.")
        _raw("UPDATE %s SET interface_id = ? WHERE evidence_id != ?" % ANCHORS,
             (second.interface_id, first.evidence_id))
    elif defect == "non_integration":
        _raw("UPDATE readiness_evidence SET dimension = 'COMMERCIAL', "
             "topic = 'target_customer' WHERE project_id = ?", (sid,), ignore_checks=True)
    elif defect == "chain_moved":
        _correct(c, sid, first.evidence_id, statement_text="Corrected.")
        _raw("UPDATE %s SET interface_id = ? WHERE evidence_id = ?" % ANCHORS,
             (second.interface_id, first.evidence_id))
    else:
        _raw("INSERT INTO %s VALUES (?, ?, ?)" % ANCHORS,
             (sid, "rev-" + "9" * 32, ifc.interface_id), fk=False)
    with pytest.raises(ce.CommercialEvidenceHistoryError):
        _history(sid)
    page = _html.unescape(_raw_page(c, sid))
    assert ui_text.text("UI_S15_IEV_UNAVAILABLE", "en") in page
    session = c.get("/session/%s" % sid).get_data(as_text=True)
    assert 'data-rs-dimension="integration"' not in session      # snapshot fails closed


def test_the_anchor_schema_refuses_cross_project_and_duplicate_anchors(owner):
    import sqlite3
    c, sid, ifc = owner
    _record(c, sid, ifc.interface_id)
    [row], _ = _history(sid)
    store = _store()
    other, subs = _new_project(store)
    foreign = _ifc(subs, "Elsewhere.")
    store.append_subsystem_interface(other, foreign, "elsewhere")
    with pytest.raises(sqlite3.IntegrityError):
        _fk_raw("INSERT INTO %s VALUES (?, ?, ?)" % ANCHORS,
                (sid, row.evidence_id, ifc.interface_id))
    with pytest.raises(sqlite3.IntegrityError):
        _fk_raw("UPDATE %s SET interface_id = ? WHERE project_id = ?" % ANCHORS,
                (foreign.interface_id, sid))
    with pytest.raises(sqlite3.IntegrityError):
        _fk_raw("INSERT INTO %s VALUES (?, ?, ?)" % ANCHORS,
                (other, row.evidence_id, foreign.interface_id))


def test_commercial_and_manufacturing_evidence_get_no_anchor(owner):
    c, sid, ifc = owner
    from tests.test_readiness_snapshot_runtime import ITEM as CEV_ITEM
    r = c.post("/session/%s/commercial-evidence" % sid, data=CEV_ITEM)
    assert r.status_code in (200, 302)
    [(_eid, dimension, _w, _s)] = _evidence_rows(sid)
    assert dimension == "COMMERCIAL" and _anchor_rows(sid) == []
    history, anchored = _history(sid)
    assert anchored == {} and len(history) == 1


def test_only_the_verified_owner_can_write(anonymous):
    c, sid, ifc = anonymous
    page = _html.unescape(_raw_page(c, sid))
    assert ui_text.text("UI_S15_IEV_READONLY", "en") in page
    assert not _iev_forms(_raw_page(c, sid))
    data = dict(ITEM, interface_id=ifc.interface_id, action="record",
                evidence_submission=appmod._s15_evidence_submission_identity(sid))
    r = c.post(IEV % sid, data=data)
    assert r.status_code == 302 and "/session/" not in r.headers["Location"]
    assert _evidence_rows(sid) == []


# ==========================================================================
# 4. Retry: signed identity, committed-first reconciliation, conflicts
# ==========================================================================
def test_an_exact_retry_returns_the_stored_pair_without_a_duplicate(owner):
    c, sid, ifc = owner
    r, data = _record(c, sid, ifc.interface_id)
    before = _evidence_rows(sid), _anchor_rows(sid)
    again = c.post(IEV % sid, data=data)
    assert again.status_code == 200 and appmod.S15_IEV_SAVED_MESSAGE in _body(again)
    assert (_evidence_rows(sid), _anchor_rows(sid)) == before
    _restart()
    again = c.post(IEV % sid, data=data)
    assert again.status_code == 200 and appmod.S15_IEV_SAVED_MESSAGE in _body(again)
    assert (_evidence_rows(sid), _anchor_rows(sid)) == before


@pytest.mark.parametrize("change", ["statement_text", "topic", "interface", "action"])
def test_the_same_identity_with_other_material_is_a_conflict(owner, change):
    c, sid, ifc = owner
    second = _second_interface(c, sid, ifc)
    r, data = _record(c, sid, ifc.interface_id)
    before = _evidence_rows(sid), _anchor_rows(sid)
    altered = dict(data)
    if change == "statement_text":
        altered["statement_text"] = "Something else entirely."
    elif change == "topic":
        altered["topic"] = "interface_review"
    elif change == "interface":
        altered["interface_id"] = second.interface_id
    else:
        [row], _ = _history(sid)
        altered = {k: v for k, v in data.items() if k not in ITEM}
        altered.update(action="withdraw", supersedes_evidence_id=row.evidence_id)
    r = c.post(IEV % sid, data=altered)
    assert r.status_code == 400 and appmod.S15_IEV_NOT_SAVED_MESSAGE in _body(r)
    assert (_evidence_rows(sid), _anchor_rows(sid)) == before


def test_the_store_resolves_the_event_key_first(owner):
    c, sid, ifc = owner
    second = _second_interface(c, sid, ifc)
    _record(c, sid, ifc.interface_id)
    [row], _ = _history(sid)
    store = _store()
    outcome, stored = store.append_integration_evidence(sid, row, ifc.interface_id)
    assert outcome == EVIDENCE_EXACT_REPLAY and stored == row
    with pytest.raises(IntegrationEvidenceConflict):
        store.append_integration_evidence(sid, row, second.interface_id)
    found = store.committed_integration_evidence_for_event_key(sid, row.event_key)
    assert found[0] == row and found[1] == ifc.interface_id


def test_a_forged_or_cross_project_identity_is_refused(owner):
    c, sid, ifc = owner
    form = _form(c, sid, "record", interface_id=ifc.interface_id)
    forged = dict(form, **ITEM)
    forged["evidence_submission"] = form["evidence_submission"][:-2] + "00"
    assert c.post(IEV % sid, data=forged).status_code == 400
    other_sid, _other = _integrated_with_interface(c)
    foreign = dict(forged, evidence_submission=appmod._s15_evidence_submission_identity(other_sid))
    assert c.post(IEV % sid, data=foreign).status_code == 400
    assert _evidence_rows(sid) == []


def test_a_commit_then_error_is_reconciled_as_saved(owner):
    c, sid, ifc = owner
    form = _form(c, sid, "record", interface_id=ifc.interface_id)
    store = _store()
    real = store._conn
    store._conn = _FailOn(real, commit_then=True)
    try:
        r = c.post(IEV % sid, data=dict(form, **ITEM))
    finally:
        store._conn = real
    assert r.status_code == 200 and appmod.S15_IEV_SAVED_MESSAGE in _body(r)
    assert len(_evidence_rows(sid)) == 1 and len(_anchor_rows(sid)) == 1


def test_an_unconfirmable_outcome_stays_unknown(owner, monkeypatch):
    c, sid, ifc = owner
    form = _form(c, sid, "record", interface_id=ifc.interface_id)
    store = _store()

    def unreadable(*_a, **_k):
        raise StoreError("injected: committed truth unreadable")
    monkeypatch.setattr(store, "committed_integration_evidence_for_event_key", unreadable)
    r = c.post(IEV % sid, data=dict(form, **ITEM))
    assert r.status_code == 503 and appmod.S15_IEV_UNKNOWN_MESSAGE in _body(r)
    assert appmod.S15_IEV_SAVED_MESSAGE not in _body(r)
    assert _evidence_rows(sid) == []


def test_a_correction_of_a_stale_head_is_refused(owner):
    c, sid, ifc = owner
    _record(c, sid, ifc.interface_id)
    [first], _ = _history(sid)
    stale = _form(c, sid, "correct", target=first.evidence_id)
    _withdraw(c, sid, first.evidence_id)
    r = c.post(IEV % sid, data=dict(stale, **{k: ITEM[k] for k in TEXT}))
    assert r.status_code == 400 and appmod.S15_IEV_STALE_MESSAGE in _body(r)
    assert len(_evidence_rows(sid)) == 2


# ==========================================================================
# 5. The IRL-compatible view: snapshot row and per-interface status
# ==========================================================================
def test_the_snapshot_has_a_fourth_integration_row_and_no_aggregate():
    snap = rs.readiness_snapshot(IdeaState(idea_id="x"), ())
    assert snap["dimensions"] == ("technical", "commercial", "manufacturing", "integration")
    row = snap["rows"][3]
    assert row["dimension"] == "integration"
    assert row["disposition"] == rs.DISPOSITION_INSUFFICIENT_EVIDENCE
    assert sorted(snap) == ["dimensions", "evidence_dimensions_active", "rows"]
    assert "INTEGRATION" in snap["evidence_dimensions_active"]


def test_the_integration_row_counts_only_current_items(owner):
    c, sid, ifc = owner
    _record(c, sid, ifc.interface_id)
    _record(c, sid, ifc.interface_id, topic="interface_review", subject_text="Peer review")
    history, _ = _history(sid)
    _correct(c, sid, history[0].evidence_id, statement_text="Held 60 cycles.")
    _withdraw(c, sid, history[1].evidence_id)
    page, rows = _snapshot_rows(c, sid)
    assert rows == [("technical", "INSUFFICIENT_EVIDENCE"), ("commercial", "INSUFFICIENT_EVIDENCE"),
                    ("manufacturing", "INSUFFICIENT_EVIDENCE"),
                    ("integration", "INSUFFICIENT_EVIDENCE")]
    row = rs.integration_row(_history(sid)[0])
    assert row["recorded_items"] == 1 and row["topics"] == ("interface_test",)
    block = _html.unescape(page.split('data-rs-dimension="integration"', 1)[1].split("</li>", 1)[0])
    assert ui_text.text("UI_IEV_TOPIC_INTERFACE_TEST", "en") in block
    assert ui_text.text("UI_RS_INTEGRATION_NOT_A_CONCLUSION", "en") in block
    for claim in ("compatible.", "integration ready", "IRL ", "validated", "verified"):
        assert claim not in _visible(block), claim


def test_observations_preparation_and_dependency_never_count_as_evidence(owner):
    c, sid, ifc = owner
    _save(c, sid, {(F_C, ifc.interface_id): "Indoor."})
    _observe(c, sid, _record_form(c, sid, ifc.interface_id), "It worked.")
    _dep_save(c, sid, ifc.interface_id, "mutual")
    assert _evidence_rows(sid) == []
    page, rows = _snapshot_rows(c, sid)
    block = _html.unescape(page.split('data-rs-dimension="integration"', 1)[1].split("</li>", 1)[0])
    assert ui_text.text("UI_RS_INTEGRATION_NOTHING", "en") in block


def test_the_status_block_reports_each_fact_and_labels_observations_not_evidence(owner):
    c, sid, ifc = owner
    _save(c, sid, {(F_C, ifc.interface_id): "Indoor."})
    _observe(c, sid, _record_form(c, sid, ifc.interface_id), "It worked.")
    _dep_save(c, sid, ifc.interface_id, _one_way(ifc)[0], "Arm needs board power.")
    _record(c, sid, ifc.interface_id)
    [row], _ = _history(sid)
    _correct(c, sid, row.evidence_id, statement_text="Held 60 cycles.")
    page = _html.unescape(_raw_page(c, sid))
    status = _section(page, "UI_S15_ST_HEADING").split(
        ui_text.text("UI_S15_PREP_FORM_HEADING", "en"))[0]
    assert ui_text.text("UI_S15_PREP_PARTIAL", "en") in status
    assert "Arm needs board power." in status
    assert ui_text.text("UI_S15_DEP_RELIES_ON", "en") in status
    assert ui_text.text("UI_S15_ST_CHECKS_COUNT", "en").format(count=1) in status
    assert ui_text.text("UI_S15_ST_CHECKS_NOT_EVIDENCE", "en") in status
    assert ui_text.text("UI_S15_ST_EVIDENCE_COUNT", "en").format(count=1) in status
    assert ui_text.text("UI_S15_ST_EVIDENCE_HISTORY", "en").format(count=1) in status
    assert ui_text.text("UI_S15_ST_NOT_A_VERDICT", "en") in status


def test_unreadable_observations_or_evidence_read_unavailable_not_absent(owner, monkeypatch):
    c, sid, ifc = owner
    store = _store()

    def boom(*_a, **_k):
        raise StoreError("injected")
    monkeypatch.setattr(store, "load_interface_observations", boom)
    monkeypatch.setattr(store, "load_integration_evidence", boom)
    page = _html.unescape(_raw_page(c, sid))
    status = _section(page, "UI_S15_ST_HEADING").split(
        ui_text.text("UI_S15_PREP_FORM_HEADING", "en"))[0]
    assert status.count(ui_text.text("UI_S15_ST_UNAVAILABLE", "en")) == 2
    assert ui_text.text("UI_S15_ST_EVIDENCE_COUNT", "en").format(count=0) not in status
    assert ui_text.text("UI_S15_IEV_UNAVAILABLE", "en") in page


def test_the_arabic_page_renders_every_new_surface(owner):
    c, sid, ifc = owner
    _record(c, sid, ifc.interface_id)
    c.post("/ui-language", data={"lang": "ar"})
    try:
        page = _html.unescape(_raw_page(c, sid))
        session = _html.unescape(c.get("/session/%s" % sid).get_data(as_text=True))
    finally:
        c.post("/ui-language", data={"lang": "en"})
    for key in ("UI_S15_ST_HEADING", "UI_S15_DEP_LEGEND", "UI_S15_IEV_HEADING",
                "UI_S15_IEV_LABEL", "UI_IEV_TOPIC_INTERFACE_TEST"):
        assert ui_text.text(key, "ar") in page, key
    assert ui_text.text("UI_RS_DIM_INTEGRATION", "ar") in session


# ==========================================================================
# 6. Isolation: report, PDF and Structured Export unchanged
# ==========================================================================
def test_report_pdf_and_export_carry_no_dependency_or_integration_evidence(owner, monkeypatch):
    from tests.test_stage15_integrated_invention_entry import _pdf_source
    c, sid, ifc = owner
    _dep_save(c, sid, ifc.interface_id, "mutual", "Dependency note text.")
    _record(c, sid, ifc.interface_id)
    report = c.get("/session/%s/deliverable" % sid)
    assert report.status_code == 200
    export = c.get("/account/projects/%s/export" % sid)
    assert export.status_code == 200
    pdf = _pdf_source(c, sid, monkeypatch)
    for body in (report.get_data(as_text=True), export.get_data(as_text=True), pdf):
        for needle in ("Dependency note text.", ITEM["statement_text"],
                       ITEM["limitation_text"], "interface_test", "INTEGRATION"):
            assert needle not in body, needle
