"""T6-INTERFACE-VERIFICATION-REFERENCE-01: the interaction's own preparation beside each participation.

The T6 preliminary composition (Slice 1) traces each CURRENT component through its CURRENT participations to the
notes of that exact ``(interface_id, component_id)`` pair. This increment adds, apart from those notes, the inventor's
CURRENT verification-preparation inputs of the interaction itself (Stage 15 Slice 3: operating conditions,
acceptance criterion, evidence needed), keyed only by the exact ``interface_id``. What is pinned:
  * ONE reader, ``load_preliminary_composition``: the record of ``load_participation_preparations`` plus the
    interface preparations, validated by the Stage 15 owner inside the SAME read snapshot (proved under a concurrent
    writer); ``load_participation_preparations`` itself is unchanged and never fails on an interface-preparation row;
  * the two levels stay separate; each field RECORDED (verbatim) or NOT_RECORDED; current value only;
  * a malformed, orphaned or unreadable preparation shows the WHOLE composition unavailable, never partial;
  * the Validation Plan step is neither read nor derived: its reference is UNRESOLVED; no check, result,
    compatibility or validation is claimed;
  * withdrawn components carry nothing; project authorization and isolation; deterministic and read-only; EN / AR.
"""
import hashlib
import html as _html
import re
import sqlite3

import pytest

import web.app as appmod
from engine import subsystem_model as sm
from engine.record_store import InterfacePreparationsCorrupt, SqliteRecordStore
from tests.test_component_interface_participation import (  # noqa: F401
    _cmp, _form as _icp_form, _ifc, _post as _icp_post, _project, _raw, _store, _web_project, client)
from tests.test_component_inventory_correct_withdraw import _withdraw
from tests.test_component_participation_verification_preparation import (
    EVIDENCE, EXPECTED, _forms as _ppv_forms, _page as _prep_page, _post as _ppv_post)
from tests.test_stage15_interface_preparation import _save as _ifc_save
from web import ui_text

T6 = "/session/%s/preliminary-composition"
F_C, F_A, F_E = sm.PREPARATION_FIELDS
COND, CRIT, EVID = "Indoors, 20 to 25 °C", "The hinge reaches 90 degrees", "Watch 10 cycles"


def _t(key, lang="en"):
    return ui_text.text(key, lang)


def _setup(tmp_path):
    path = str(tmp_path / "t6i.db")
    store = SqliteRecordStore(path)
    pid, subs = _project(store)
    ifc = _ifc(store, pid, subs)
    a = _cmp(store, pid, subs, "Hinge motor")
    b = _cmp(store, pid, subs, "Battery pack")
    store.set_interface_participation(pid, ifc, (a,), ())
    return store, path, pid, subs, ifc, a, b


def _pair_notes(store, pid, ifc, cid, expected, evidence):
    shown = {EXPECTED: None, EVIDENCE: None, "carried_over": False}
    store.set_participation_preparation(pid, ifc, cid, {EXPECTED: expected, EVIDENCE: evidence}, shown)


def _link(store, pid, index=0):
    return appmod._t6_composition(store.load_preliminary_composition(pid))["components"][index]["links"]


def _fields(link):
    return {f["field"]: (f["status"], f["text"]) for f in link["interface_fields"]}


def _insert_prep(path, row, fk=False):
    conn = sqlite3.connect(path)
    try:
        conn.execute("PRAGMA foreign_keys = %s" % ("ON" if fk else "OFF"))
        conn.execute("INSERT INTO subsystem_interface_preparations VALUES (?, ?, ?, ?, ?)", row)
        conn.commit()
    finally:
        conn.close()


# ==========================================================================
# 1. The reader: one snapshot; the existing reader unchanged
# ==========================================================================
def test_r01_the_reader_extends_the_participation_record_with_interface_preparations(tmp_path):
    store, _path, pid, _subs, ifc, a, _b = _setup(tmp_path)
    store.apply_interface_preparation_delta(pid, {ifc: {F_C: COND, F_A: CRIT}})
    base = store.load_participation_preparations(pid)
    record = store.load_preliminary_composition(pid)
    assert set(base) == {"interfaces", "components", "participations", "preparations"}
    assert {k: record[k] for k in base} == base
    [prep] = record["interface_preparations"]
    assert (prep.interface_id, prep.operating_conditions, prep.acceptance_criterion, prep.evidence_needed) == (
        ifc, COND, CRIT, None)
    assert store.load_preliminary_composition(pid)["interface_preparations"] == record["interface_preparations"]


def test_r02_every_read_happens_under_one_held_read_snapshot(tmp_path, monkeypatch):
    """A concurrent writer cannot commit while the reader validates the interface preparations: the reads before it
    (interactions, components, participations, notes) and this one share ONE held read transaction."""
    store, path, pid, _subs, ifc, a, _b = _setup(tmp_path)
    real, seen = store._validated_preparations, []

    def during(project_id, interfaces):
        seen.append(store._read_snapshot_owned)
        writer = sqlite3.connect(path, timeout=0.2)
        try:
            writer.execute("INSERT INTO subsystem_interface_preparations VALUES (?, ?, ?, NULL, NULL)",
                           (pid, ifc, "written concurrently"))
            with pytest.raises(sqlite3.OperationalError, match="locked"):
                writer.commit()
            writer.rollback()
        finally:
            writer.close()
        return real(project_id, interfaces)
    monkeypatch.setattr(store, "_validated_preparations", during)
    record = store.load_preliminary_composition(pid)
    assert seen == [True] and record["interface_preparations"] == ()
    monkeypatch.undo()
    store.apply_interface_preparation_delta(pid, {ifc: {F_C: "after"}})       # the snapshot was released
    assert store.load_preliminary_composition(pid)["interface_preparations"][0].operating_conditions == "after"


@pytest.mark.parametrize("row", [
    lambda pid, ifc: (pid, "ifc-" + "0" * 32, "orphan", None, None),          # names no interaction
    lambda pid, ifc: (pid, ifc, " untrimmed", None, None),                    # not what the owner stores
])
def test_r03_a_malformed_preparation_refuses_the_whole_record_but_not_the_existing_reader(tmp_path, row):
    store, path, pid, _subs, ifc, a, _b = _setup(tmp_path)
    _pair_notes(store, pid, ifc, a, "Opens", None)
    before = store.load_participation_preparations(pid)
    _insert_prep(path, row(pid, ifc))
    with pytest.raises(InterfacePreparationsCorrupt):
        store.load_preliminary_composition(pid)
    assert store.load_participation_preparations(pid) == before        # existing contract and callers unaffected


def test_r04_project_scope_and_missing_project(tmp_path):
    store, _path, pid, subs, ifc, a, _b = _setup(tmp_path)
    store.apply_interface_preparation_delta(pid, {ifc: {F_C: COND}})
    other, osubs = _project(store, idea="i-other")
    oifc = _ifc(store, other, osubs, description="Other", key="o1")
    assert store.load_preliminary_composition(other)["interface_preparations"] == ()
    assert [p.interface_id for p in store.load_preliminary_composition(pid)["interface_preparations"]] == [ifc]
    assert oifc != ifc
    from engine.record_store import ProjectNotFound
    with pytest.raises(ProjectNotFound):
        store.load_preliminary_composition("no-such-project")


# ==========================================================================
# 2. The composition: two separate levels, exact identity, truthful states
# ==========================================================================
def test_c01_the_two_levels_stay_separate_and_bound_to_their_exact_identities(tmp_path):
    store, _path, pid, subs, ifc, a, b = _setup(tmp_path)
    second = _ifc(store, pid, subs, description="Battery feeds the motor", key="i2")
    store.set_interface_participation(pid, second, (a, b), ())
    _pair_notes(store, pid, ifc, a, "Opens in 2 s", "Stopwatch")
    store.apply_interface_preparation_delta(pid, {ifc: {F_C: COND, F_A: CRIT, F_E: EVID}})
    first_link, second_link = _link(store, pid)
    assert first_link["interface_id"] == ifc
    assert first_link["notes"] == [{"field": EXPECTED, "text": "Opens in 2 s"}, {"field": EVIDENCE, "text": "Stopwatch"}]
    assert _fields(first_link) == {F_C: ("RECORDED", COND), F_A: ("RECORDED", CRIT), F_E: ("RECORDED", EVID)}
    assert second_link["interface_id"] == second and second_link["notes"] == []      # nothing borrowed
    assert _fields(second_link) == {f: ("NOT_RECORDED", None) for f in sm.PREPARATION_FIELDS}
    [b_link] = _link(store, pid, 1)                                       # the same interaction for every component
    assert b_link["interface_id"] == second and b_link["interface_fields"] == second_link["interface_fields"]
    assert [f["field"] for f in first_link["interface_fields"]] == list(sm.PREPARATION_FIELDS)


def test_c02_partial_absent_edited_and_cleared_inputs(tmp_path):
    store, _path, pid, _subs, ifc, a, _b = _setup(tmp_path)
    [link] = _link(store, pid)
    assert _fields(link) == {f: ("NOT_RECORDED", None) for f in sm.PREPARATION_FIELDS}
    store.apply_interface_preparation_delta(pid, {ifc: {F_A: CRIT}})
    assert _fields(_link(store, pid)[0]) == {F_C: ("NOT_RECORDED", None), F_A: ("RECORDED", CRIT),
                                             F_E: ("NOT_RECORDED", None)}
    store.apply_interface_preparation_delta(pid, {ifc: {F_A: "Edited"}})
    assert _fields(_link(store, pid)[0])[F_A] == ("RECORDED", "Edited")
    store.apply_interface_preparation_delta(pid, {ifc: {F_A: None}})
    assert _fields(_link(store, pid)[0]) == {f: ("NOT_RECORDED", None) for f in sm.PREPARATION_FIELDS}


def test_c03_the_validation_plan_reference_is_unresolved_and_never_read(tmp_path, monkeypatch):
    import engine.validation_plan as vp
    import engine.requirement_landscape as rl
    store, _path, pid, _subs, ifc, a, _b = _setup(tmp_path)
    store.apply_interface_preparation_delta(pid, {ifc: {F_C: COND, F_A: CRIT, F_E: EVID}})

    def forbidden(*_a, **_k):
        raise AssertionError("the Validation Plan / Requirement Landscape must not be read")
    for module in (vp, rl):
        for name in dir(module):
            if name.startswith(("build", "derive")) and callable(getattr(module, name)):
                monkeypatch.setattr(module, name, forbidden)
    [link] = _link(store, pid)
    assert link["vp_reference"] == appmod.T6_VP_REFERENCE_UNRESOLVED
    assert "vstep:" not in repr(link) and "req:interface" not in repr(link)


def test_c04_carried_pair_notes_stay_earlier_beside_current_interface_inputs(tmp_path):
    store, _path, pid, _subs, ifc, a, _b = _setup(tmp_path)
    _pair_notes(store, pid, ifc, a, "Opens", None)
    store.apply_interface_preparation_delta(pid, {ifc: {F_C: COND}})
    store.set_interface_participation(pid, ifc, (), (a,))
    assert _link(store, pid) == []                                       # removed: neither level shown
    store.set_interface_participation(pid, ifc, (a,), ())
    [link] = _link(store, pid)
    assert link["status"] == appmod.T6_STATUS_EARLIER and _fields(link)[F_C] == ("RECORDED", COND)


def test_c05_withdrawn_component_carries_nothing(tmp_path):
    store, _path, pid, _subs, ifc, a, b = _setup(tmp_path)
    store.apply_interface_preparation_delta(pid, {ifc: {F_C: COND}})
    _withdraw(store, pid, a, 0)
    view = appmod._t6_composition(store.load_preliminary_composition(pid))
    assert [c["component_id"] for c in view["components"]] == [b] and view["components"][0]["links"] == []
    assert COND not in repr(view)


def test_c06_a_mismatched_snapshot_raises_rather_than_inventing(tmp_path):
    store, _path, pid, _subs, ifc, a, _b = _setup(tmp_path)
    store.apply_interface_preparation_delta(pid, {ifc: {F_C: COND}})
    record = dict(store.load_preliminary_composition(pid))
    good = record["interface_preparations"]
    record["interface_preparations"] = (sm.InterfacePreparation("ifc-" + "1" * 32, operating_conditions="x"),)
    with pytest.raises(ValueError):
        appmod._t6_composition(record)
    record["interface_preparations"] = good + good                     # one interaction, two values
    with pytest.raises(ValueError):
        appmod._t6_composition(record)


def test_c07_deterministic_and_read_only(tmp_path):
    store, path, pid, _subs, ifc, a, _b = _setup(tmp_path)
    store.apply_interface_preparation_delta(pid, {ifc: {F_C: COND}})

    def digest():
        conn = sqlite3.connect(path)
        try:
            return hashlib.sha256("\n".join(conn.iterdump()).encode()).hexdigest()
        finally:
            conn.close()
    before = digest()
    first = appmod._t6_composition(store.load_preliminary_composition(pid))
    assert appmod._t6_composition(store.load_preliminary_composition(pid)) == first and digest() == before


# ==========================================================================
# 3. The page
# ==========================================================================
def _web(c):
    sid = _web_project(c)
    form = _icp_form(c, sid)
    ids = [i for i, _c in form["options"]]
    _icp_post(c, sid, form, ids[:1])
    _ppv_post(c, sid, _ppv_forms(_prep_page(c, sid))[0], "Hinge opens in 2 s", "Stopwatch")
    return sid, ids, form["interface"]


def test_w01_the_page_shows_both_levels_apart_with_unresolved_reference(client):
    sid, ids, ifc = _web(client)
    assert _ifc_save(client, sid, {(F_A, ifc): CRIT}).status_code in (200, 302)
    r = client.get(T6 % sid)
    raw = r.get_data(as_text=True)
    page = _html.unescape(raw)
    assert r.status_code == 200 and r.headers["Cache-Control"] == "no-store"
    link = re.search(r"<div class=\"link\" data-t6-link .*?data-t6-vp-ref=\"UNRESOLVED\"[^<]*</p>", raw, re.S).group(0)
    pair = re.search(r"data-t6-pair-prep>.*?</div>", link, re.S).group(0)
    inter = re.search(r"data-t6-interface-prep data-t6-interface-prep-id=\"([^\"]+)\">(.*)", link, re.S)
    assert inter.group(1) == ifc and "Hinge opens in 2 s" in pair and CRIT not in pair
    assert "Hinge opens in 2 s" not in inter.group(2) and CRIT in _html.unescape(inter.group(2))
    assert re.findall(r'data-t6-interface-field="([^"]+)" data-t6-interface-field-status="([^"]+)"', link) == [
        (F_C, "NOT_RECORDED"), (F_A, "RECORDED"), (F_E, "NOT_RECORDED")]
    for key in ("UI_T6_PAIR_TITLE", "UI_T6_IFC_TITLE", "UI_T6_IFC_NOTE", "UI_T6_VP_UNRESOLVED",
                "UI_S15_PREP_CONDITIONS", "UI_S15_PREP_ACCEPTANCE", "UI_S15_PREP_EVIDENCE"):
        assert _t(key) in page
    body = re.sub(r"<[^>]+>", " ", raw)
    assert ifc not in body and "vstep:" not in raw and "req:interface" not in raw
    added = _html.unescape(re.sub(r"<[^>]+>", " ", inter.group(2))).lower()
    for claim in ("is compatible", "are compatible", "verified", "check passed", "validated design", "is safe",
                  "complete"):
        assert claim not in added


def test_w02_arabic_page(client):
    client.post("/ui-language", data={"lang": "ar"})
    sid, _ids, ifc = _web(client)
    _ifc_save(client, sid, {(F_C, ifc): "داخل المنزل"})
    page = _html.unescape(client.get(T6 % sid).get_data(as_text=True))
    assert 'dir="rtl"' in page and "داخل المنزل" in page
    for key in ("UI_T6_PAIR_TITLE", "UI_T6_IFC_TITLE", "UI_T6_IFC_NOTE", "UI_T6_VP_UNRESOLVED",
                "UI_T6_IFC_NOT_RECORDED", "UI_S15_PREP_CONDITIONS"):
        assert _t(key, "ar") in page


def test_w03_a_corrupt_interface_preparation_shows_only_the_unavailable_notice(client):
    sid, _ids, ifc = _web(client)
    _ifc_save(client, sid, {(F_C, ifc): COND})
    _raw("INSERT INTO subsystem_interface_preparations VALUES (?, ?, ?, ?, ?)",
         (sid, "ifc-" + "7" * 32, "orphan", None, None), fk=False)
    r = client.get(T6 % sid)
    raw = r.get_data(as_text=True)
    assert r.status_code == 503 and "data-t6-composition" not in raw
    assert COND not in _html.unescape(raw) and "Hinge opens" not in raw
    assert _t("UI_T6_UNAVAILABLE") in _html.unescape(raw)


def test_w04_a_store_failure_is_unavailable_and_the_reader_is_called_once(client, monkeypatch):
    sid, _ids, _ifc_id = _web(client)
    store = _store()
    real, calls = store.load_preliminary_composition, []

    def counted(pid):
        calls.append(pid)
        return real(pid)
    monkeypatch.setattr(store, "load_preliminary_composition", counted)
    assert client.get(T6 % sid).status_code == 200 and calls == [sid]

    def boom(_sid):
        raise sqlite3.OperationalError("injected")
    monkeypatch.setattr(store, "load_preliminary_composition", boom)
    assert client.get(T6 % sid).status_code == 503


def test_w05_authorization_and_project_isolation():
    from tests.test_commercial_evidence_capture import _client_for
    owner, _aid = _client_for("t6i-owner@example.com")
    sid, _ids, ifc = _web(owner)
    _ifc_save(owner, sid, {(F_C, ifc): "Owner-only conditions"})
    other, _oids, _oifc = _web(owner)
    intruder, _bid = _client_for("t6i-intruder@example.com")
    r = intruder.get(T6 % sid)
    assert r.status_code in (302, 403, 404) and "Owner-only conditions" not in r.get_data(as_text=True)
    assert "Owner-only conditions" not in _html.unescape(owner.get(T6 % other).get_data(as_text=True))
    assert "Owner-only conditions" in _html.unescape(owner.get(T6 % sid).get_data(as_text=True))


def test_w06_reports_and_existing_pages_do_not_carry_the_composition(client):
    sid, _ids, ifc = _web(client)
    _ifc_save(client, sid, {(F_C, ifc): COND})
    for path in ("/session/%s/deliverable", "/session/%s/parts-components-interactions",
                 "/session/%s/interface-preparation"):
        raw = client.get(path % sid).get_data(as_text=True)
        assert "data-t6-interface-prep" not in raw and "data-t6-vp-ref" not in raw
