"""T6-PART-ASSOCIATION-TRACE-01: the names of each component's own linked parts in the preliminary composition.

The T6 preliminary composition showed only how many parts a component is linked to. It now shows the inventor-declared
names of exactly that component's validated part links, in their stored canonical order. What is pinned:
  * the names come from the composition ``_participation_snapshot`` already loads inside the held read snapshot,
    exposed only through ``load_preliminary_composition`` (``"subsystems"``) with no further query;
  * ``load_participation_preparations`` keeps its exact four-key record and its failure boundaries;
  * only the component's own links are named (an unlinked project part never appears under it); a correction shows
    the latest links only; an unlinked component keeps "not linked"; a withdrawn component is absent;
  * a stale, foreign or mismatched part reference shows the WHOLE composition unavailable, never partial;
  * ids only in data attributes; EN / AR.
"""
import html as _html
import re
import sqlite3

import pytest

import web.app as appmod
from engine import subsystem_model as sm
from engine.record_store import ProjectComponentsCorrupt, SqliteRecordStore
from tests.test_component_interface_participation import (  # noqa: F401
    _cmp, _ifc, _project, _raw, _store, _web_project, client)
from tests.test_component_inventory_correct_withdraw import _correct, _withdraw
from tests.test_component_inventory_declare_list import _declare as _declare_component
from web import ui_text

T6 = "/session/%s/preliminary-composition"
LEGACY_KEYS = {"interfaces", "components", "participations", "preparations"}


def _t(key, lang="en"):
    return ui_text.text(key, lang)


def _setup(tmp_path):
    path = str(tmp_path / "t6p.db")
    store = SqliteRecordStore(path)
    pid, subs = _project(store)
    _ifc(store, pid, subs)
    return store, path, pid, subs


def _view(store, pid):
    return {c["name"]: c for c in appmod._t6_composition(store.load_preliminary_composition(pid))["components"]}


# ==========================================================================
# 1. The reader: the same snapshot's composition; the existing reader unchanged
# ==========================================================================
def test_r01_the_composition_comes_from_the_same_snapshot_with_no_further_query(tmp_path, monkeypatch):
    store, _path, pid, subs = _setup(tmp_path)
    _cmp(store, pid, subs, "Hinge motor", parts=(subs[0].subsystem_id,))
    record = store.load_preliminary_composition(pid)
    assert record["subsystems"] == tuple(store.load_project_subsystems(pid)) == tuple(subs)
    assert set(record) == LEGACY_KEYS | {"subsystems", "interface_preparations"}

    real, inside = store.load_project_subsystems, []

    def counted(project_id):
        inside.append(store._read_snapshot_owned)
        return real(project_id)
    monkeypatch.setattr(store, "load_project_subsystems", counted)
    store.load_preliminary_composition(pid)
    assert inside == [True]                                   # loaded once, inside the held snapshot
    monkeypatch.undo()

    def selects(load):
        seen = []
        store._conn.set_trace_callback(lambda sql: seen.append(sql) if sql.lstrip().upper().startswith("SELECT")
                                       else None)
        try:
            load(pid)
        finally:
            store._conn.set_trace_callback(None)
        return seen
    legacy, extended = selects(store.load_participation_preparations), selects(store.load_preliminary_composition)
    assert len(extended) - len(legacy) == 1                    # only the interface-preparation read of #881
    assert "subsystem_interface_preparations" in [s for s in extended if s not in legacy][0]


def test_r02_the_existing_reader_keeps_its_record_and_failure_boundaries(tmp_path):
    store, path, pid, subs = _setup(tmp_path)
    a = _cmp(store, pid, subs, "Hinge motor", parts=(subs[0].subsystem_id,))
    legacy = store.load_participation_preparations(pid)
    assert set(legacy) == LEGACY_KEYS and "subsystems" not in legacy
    assert {k: store.load_preliminary_composition(pid)[k] for k in LEGACY_KEYS} == legacy
    conn = sqlite3.connect(path)
    try:
        conn.execute("PRAGMA foreign_keys = OFF")
        conn.execute("UPDATE project_components SET subsystem_ids = ? WHERE component_id = ?",
                     ('["sub-' + "0" * 32 + '"]', a))
        conn.commit()
    finally:
        conn.close()
    for load in (store.load_participation_preparations, store.load_preliminary_composition):
        with pytest.raises(ProjectComponentsCorrupt):         # the same owner refusal, before and after
            load(pid)


# ==========================================================================
# 2. The composition: exactly the component's own links, current only
# ==========================================================================
def test_c01_only_the_components_own_links_by_name_in_canonical_order(tmp_path):
    store, _path, pid, subs = _setup(tmp_path)
    _cmp(store, pid, subs, "Hinge motor", parts=(subs[1].subsystem_id, subs[0].subsystem_id))
    _cmp(store, pid, subs, "Arm bracket", parts=(subs[0].subsystem_id,))
    _cmp(store, pid, subs, "Battery pack")
    view = _view(store, pid)
    names = [s.display_name for s in subs]
    assert view["Hinge motor"]["parts"] == names                       # stored canonical order
    assert view["Hinge motor"]["part_ids"] == [s.subsystem_id for s in subs]
    assert view["Arm bracket"]["parts"] == [names[0]]                  # the other project part never appears
    assert view["Battery pack"]["parts"] == [] and view["Battery pack"]["part_ids"] == []


def test_c02_a_correction_shows_the_latest_links_only(tmp_path):
    store, _path, pid, subs = _setup(tmp_path)
    a = _cmp(store, pid, subs, "Hinge motor", parts=(subs[0].subsystem_id, subs[1].subsystem_id))
    _correct(store, pid, a, 0, name="Hinge motor v2", parts=(subs[1].subsystem_id,))
    view = _view(store, pid)
    assert "Hinge motor" not in view and view["Hinge motor v2"]["parts"] == [subs[1].display_name]
    _correct(store, pid, a, 1, name="Hinge motor v3", parts=())
    assert _view(store, pid)["Hinge motor v3"]["parts"] == []


def test_c03_a_withdrawn_component_is_absent(tmp_path):
    store, _path, pid, subs = _setup(tmp_path)
    a = _cmp(store, pid, subs, "Old sensor", parts=(subs[0].subsystem_id,))
    _cmp(store, pid, subs, "Battery pack")
    _withdraw(store, pid, a, 0)
    assert list(_view(store, pid)) == ["Battery pack"]


def test_c04_a_mismatched_snapshot_raises_rather_than_inventing(tmp_path):
    store, _path, pid, subs = _setup(tmp_path)
    _cmp(store, pid, subs, "Hinge motor", parts=(subs[0].subsystem_id,))
    record = dict(store.load_preliminary_composition(pid))
    record["subsystems"] = (subs[1],)                                   # the linked part is missing
    with pytest.raises(KeyError):
        appmod._t6_composition(record)


# ==========================================================================
# 3. The page
# ==========================================================================
def _web(c):
    sid = _web_project(c, names=("Battery pack",))
    subs = _store().load_project_subsystems(sid)
    assert _declare_component(c, sid, name="Hinge motor", function="Turns the hinge",
                              parts=(subs[0].subsystem_id,)).status_code in (200, 302)
    assert _declare_component(c, sid, name="Main board", function="Controls it",
                              parts=[s.subsystem_id for s in subs]).status_code in (200, 302)
    return sid, subs


def _parts_line(raw, name):
    block = re.search(r'<div class="block" data-t6-component .*?data-t6-component-name>%s</bdi>.*?'
                      r'data-t6-component-parts="(\d+)">(.*?)</p>' % re.escape(name), raw, re.S)
    return int(block.group(1)), block.group(2)


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_w01_the_page_names_each_components_own_parts(client, lang):
    if lang == "ar":
        client.post("/ui-language", data={"lang": "ar"})
    sid, subs = _web(client)
    raw = client.get(T6 % sid).get_data(as_text=True)
    count, line = _parts_line(raw, "Hinge motor")
    shown = [(i, _html.unescape(n)) for i, n in
             re.findall(r'<bdi dir="auto" data-t6-part-name data-t6-part-id="([^"]+)">(.*?)</bdi>', line)]
    assert count == 1 and shown == [(subs[0].subsystem_id, subs[0].display_name)]
    assert subs[1].display_name not in _html.unescape(line)
    count, line = _parts_line(raw, "Main board")
    shown = [_html.unescape(n) for n in re.findall(r"data-t6-part-name[^>]*>(.*?)</bdi>", line)]
    assert count == 2 and shown == [s.display_name for s in subs]
    assert _t("UI_T6_PARTS_SEPARATOR", lang) in _html.unescape(line)
    assert _t("UI_T6_PARTS_COUNT", lang) in _html.unescape(line)
    count, line = _parts_line(raw, "Battery pack")
    assert count == 0 and _html.unescape(line) == _t("UI_T6_PARTS_NONE", lang)
    body = re.sub(r"<[^>]+>", " ", raw)
    assert all(s.subsystem_id not in body for s in subs)


def test_w02_a_stale_part_reference_shows_only_the_unavailable_notice(client):
    sid, subs = _web(client)
    _raw("UPDATE project_components SET subsystem_ids = ? WHERE project_id = ? AND display_name = ?",
         ('["sub-' + "0" * 32 + '"]', sid, "Hinge motor"), fk=False)
    r = client.get(T6 % sid)
    raw = r.get_data(as_text=True)
    assert r.status_code == 503 and "data-t6-composition" not in raw and "data-t6-part-name" not in raw
    assert _t("UI_T6_UNAVAILABLE") in _html.unescape(raw)


def test_w03_a_mismatched_record_is_unavailable(client, monkeypatch):
    sid, subs = _web(client)
    store = _store()
    real = store.load_preliminary_composition

    def mismatched(pid):
        record = dict(real(pid))
        record["subsystems"] = ()
        return record
    monkeypatch.setattr(store, "load_preliminary_composition", mismatched)
    r = client.get(T6 % sid)
    assert r.status_code == 503 and "data-t6-part-name" not in r.get_data(as_text=True)
