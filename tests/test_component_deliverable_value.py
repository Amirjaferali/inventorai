"""COMPONENT-DELIVERABLE-VALUE-01 — the inventor's CURRENT declared components in the analysis report and PDF.

What is pinned:
  * one read-only "Components you have declared" section in ``web/templates/deliverable.html``, rendered by the
    HTML report AND the PDF from the SAME view (``_component_report_view`` in ``web/app.py``), on ordinary and
    integrated projects alike;
  * the view reads ``load_component_inventory`` (the composition and the CURRENT inventory, validated whole) ONCE
    per render: current components only, latest corrected material, original declaration order, part names
    resolved by identity, project level for a component linked to no part; never an earlier version, a withdrawn
    component or a component id;
  * three states — current components, "no current components" after a successful read, UNAVAILABLE for anything
    unreadable or corrupt (never "none" or a partial list) — and no section at all for a project absent from the
    store; the rest of the report is unchanged and still renders;
  * the same order and latest wording as Stage 35 export field 7 for an unchanged project;
  * the report / PDF audience is unchanged (the central project authorization), opening either writes nothing,
    inventor text is escaped and direction-isolated, EN / AR copy.
"""
import dataclasses
import html as _html
import json
import os
import re
import sqlite3

import pytest

import web.app as appmod
from engine import subsystem_model as sm
from engine.record_store import ProjectNotFound, RecordStoreConnectionUnsafe
from tests.csrf_client import csrf_client
from tests.test_component_inventory_declare_list import _integrated, _ordinary, _stable
from tests.test_stage15_integrated_invention_entry import _pdf_source
from tests.test_stage19_durable_success_criteria import _client_for, _journey
from web import ui_text

F7 = "component_descriptions_beyond_parts"
SECTION_RE = re.compile(r'<section class="declared-components".*?</section>', re.S)


@pytest.fixture
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


def _store():
    return appmod._get_store()


def _declare(sid, name, function, domains=(), key=None):
    subs = _store().load_project_subsystems(sid)
    parts = tuple(s.subsystem_id for s in subs if s.domain in domains)
    item = sm.declared_component(subs, name, function, parts)
    _store().append_project_component(sid, item, key or ("k-" + name))
    return item


def _correct(sid, component_id, name, function, domains=()):
    subs, inv = _store().load_component_inventory_record(sid)
    record = inv.record_for(component_id)
    parts = tuple(s.subsystem_id for s in subs if s.domain in domains)
    rev = sm.corrected_component_revision(inv, subs, component_id, record.head_revision_no,
                                          name, function, parts)
    _store().append_component_revision(sid, rev, "c-%s-%d" % (component_id, record.head_revision_no))


def _withdraw(sid, component_id):
    _subs, inv = _store().load_component_inventory_record(sid)
    record = inv.record_for(component_id)
    rev = sm.withdrawn_component_revision(inv, component_id, record.head_revision_no)
    _store().append_component_revision(sid, rev, "w-" + component_id)


def _raw(sql, params=()):
    _store()
    con = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        con.execute(sql, params)
        con.commit()
    finally:
        con.close()


def _dump():
    con = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        return list(con.iterdump())
    finally:
        con.close()


def _report(c, sid):
    r = c.get(f"/session/{sid}/deliverable")
    assert r.status_code == 200, r.status_code
    return r.get_data(as_text=True)


def _section(raw):
    found = SECTION_RE.findall(raw)
    assert len(found) <= 1
    return found[0] if found else None


def _without_section(raw):
    return SECTION_RE.sub("", raw)


def _items(section):
    """``[(name, function, [parts] | None)]`` in rendered order, unescaped."""
    out = []
    for li in re.findall(r"<li data-dc-item.*?</li>", section, re.S):
        name = _html.unescape(re.search(r"<bdi dir=\"auto\" data-dc-name>(.*?)</bdi>", li, re.S).group(1))
        function = _html.unescape(re.search(r"<bdi dir=\"auto\" data-dc-function>(.*?)</bdi>", li, re.S).group(1))
        parts = [_html.unescape(p) for p in re.findall(r"<bdi dir=\"auto\" data-dc-part>(.*?)</bdi>", li, re.S)]
        out.append((name, function, parts if "data-dc-unassigned" not in li else None))
    return out


def _has(section, key, lang="en"):
    """True when the catalogue text for ``key`` is visible in ``section`` (compared unescaped, so the
    escaping spelling of an apostrophe or ampersand does not matter)."""
    return ui_text.text(key, lang) in _html.unescape(section)


# ==========================================================================
# 1. What the section shows
# ==========================================================================
def test_v01_ordinary_project_lists_current_components_in_declaration_order(client):
    sid = _ordinary(client)
    _declare(sid, "Thermal fuse", "Cuts power when too hot")
    _declare(sid, "Fan", "Moves air over the board")
    section = _section(_report(client, sid))
    assert section is not None and 'data-dc-unavailable' not in section
    assert _items(section) == [("Thermal fuse", "Cuts power when too hot", []),
                               ("Fan", "Moves air over the board", [])]
    for key in ("UI_CI_HEADING", "UI_CI_BOUNDARY", "UI_DC_PROVENANCE", "UI_DC_HISTORY"):
        assert _has(section, key), key
    assert _html.unescape(section).count(ui_text.text("UI_DC_PROVENANCE", "en")) == 2
    assert "data-dc-part" not in section and "data-dc-unassigned" not in section   # no parts to link
    assert "data-dc-none" not in section


def test_v02_integrated_project_resolves_part_names_and_project_level(client):
    sid = _integrated(client)
    subs = _store().load_project_subsystems(sid)
    names = {s.domain: s.display_name for s in subs}
    _declare(sid, "Gear motor", "Turns the arm", domains=("mechanical", "electronics_electrical"))
    _declare(sid, "Enclosure screws", "Hold the case together")
    section = _section(_report(client, sid))
    rows = _items(section)
    assert rows[0][:2] == ("Gear motor", "Turns the arm")
    assert rows[0][2] == [names["mechanical"], names["electronics_electrical"]]
    assert rows[1] == ("Enclosure screws", "Hold the case together", None)
    assert _has(section, "UI_CI_UNASSIGNED") and _has(section, "UI_CI_PARTS_LABEL")
    for sub in subs:
        assert sub.subsystem_id not in section


def test_v03_only_the_latest_current_material_and_never_a_withdrawn_component(client, monkeypatch):
    sid = _integrated(client)
    a = _declare(sid, "Motor v1", "Old function text")
    b = _declare(sid, "Sensor", "Reads temperature")
    _declare(sid, "Spring", "Returns the lever")
    _correct(sid, a.component_id, "Motor v2", "New function text", domains=("mechanical",))
    _withdraw(sid, b.component_id)
    raw = _report(client, sid)
    section = _section(raw)
    assert [r[:2] for r in _items(section)] == [("Motor v2", "New function text"),
                                                ("Spring", "Returns the lever")]
    for stale in ("Motor v1", "Old function text", "Sensor", "Reads temperature"):
        assert stale not in raw, stale
    assert "cmp-" not in raw                                       # no component id anywhere
    pdf = _pdf_source(client, sid, monkeypatch)
    pdf_section = _section(pdf)
    assert [r[:2] for r in _items(pdf_section)] == [r[:2] for r in _items(section)]
    for stale in ("Motor v1", "Old function text", "Sensor", "Reads temperature", "cmp-"):
        assert stale not in pdf, stale


def test_v04_matches_stage35_field_7_for_an_unchanged_project():
    appmod.app.config["TESTING"] = True
    c, _aid = _client_for("dcv-owner@example.com")
    sid = _journey(c)
    a = _declare(sid, "Thermal fuse <TF-1>", "Cuts power & stops heating")
    _declare(sid, "حساس حرارة", "يقيس درجة الحرارة")
    _declare(sid, "Relay", "Switches the heater")
    _correct(sid, a.component_id, "Thermal fuse <TF-2>", "Cuts power")
    r = c.get("/account/projects/%s/disclosure-export/json" % sid)
    assert r.status_code == 200
    [f7] = [f for f in json.loads(r.data.decode("utf-8"))["content"]["fields"] if f["field"] == F7]
    export = [(item["slots"]["name"]["value"], item["slots"]["function"]["value"])
              for item in f7["items"]]
    report = [r_[:2] for r_ in _items(_section(_report(c, sid)))]
    assert export == report == [("Thermal fuse <TF-2>", "Cuts power"),
                                ("حساس حرارة", "يقيس درجة الحرارة"),
                                ("Relay", "Switches the heater")]


# ==========================================================================
# 2. The three states and the absent project
# ==========================================================================
@pytest.mark.parametrize("project", ["ordinary", "integrated"])
def test_s01_no_current_components_reads_none_after_a_successful_read(client, project):
    sid = _ordinary(client) if project == "ordinary" else _integrated(client)
    section = _section(_report(client, sid))
    assert section is not None and _has(section, "UI_DC_NONE")
    assert "data-dc-item" not in section and "data-dc-unavailable" not in section
    gone = _declare(sid, "Temporary", "Was here")
    _withdraw(sid, gone.component_id)
    section = _section(_report(client, sid))
    assert _has(section, "UI_DC_NONE") and "Temporary" not in section
    assert _has(section, "UI_DC_HISTORY")


def test_s02_a_corrupt_history_reads_unavailable_never_none_or_partial(client, monkeypatch):
    sid = _integrated(client)
    a = _declare(sid, "Kept component", "Still current")
    _declare(sid, "Other component", "Also current")
    _correct(sid, a.component_id, "Corrected name", "Corrected function")
    _raw("UPDATE project_component_revisions SET revision_no = 2 WHERE project_id = ?", (sid,))
    raw = _report(client, sid)
    section = _section(raw)
    assert 'data-dc-unavailable' in section and _has(section, "UI_DC_UNAVAILABLE")
    for marker in ("data-dc-item", "data-dc-none", "data-dc-history", "data-dc-boundary"):
        assert marker not in section, marker
    for text in ("Kept component", "Other component", "Corrected name"):
        assert text not in raw, text
    assert 'id="report-contents"' in raw and 'id="integrated-scope"' in raw   # the rest still renders
    pdf = _pdf_source(client, sid, monkeypatch)
    assert "data-dc-unavailable" in _section(pdf) and "Kept component" not in pdf


@pytest.mark.parametrize("error", [RuntimeError("store down"), RecordStoreConnectionUnsafe("unsafe"),
                                   sqlite3.OperationalError("locked")])
def test_s03_any_read_failure_is_unavailable(client, monkeypatch, error):
    sid = _ordinary(client)
    _declare(sid, "Visible part", "Visible function")

    def boom(_sid):
        raise error
    monkeypatch.setattr(_store(), "load_component_inventory", boom)
    section = _section(_report(client, sid))
    assert "data-dc-unavailable" in section and "Visible part" not in section


def test_s04_a_project_absent_from_the_store_shows_no_section(client, monkeypatch):
    sid = _ordinary(client)

    def missing(project_id):
        raise ProjectNotFound(project_id)
    monkeypatch.setattr(_store(), "load_component_inventory", missing)
    raw = _report(client, sid)
    assert _section(raw) is None and "data-declared-components" not in raw
    monkeypatch.setattr(_store(), "load_component_inventory", None)
    assert appmod._component_report_view(sid) is None


def test_s05_view_contract_unit():
    class Store:
        def __init__(self, result):
            self.result, self.calls = result, 0

        def load_component_inventory(self, sid):
            self.calls += 1
            return self.result

    subs = ()
    comp = sm.declared_component(subs, "A", "does a", ())
    store = Store((subs, (comp,)))
    real = appmod._get_store
    appmod._get_store = lambda: store
    try:
        view = appmod._component_report_view("sid")
        assert view == {"available": True, "has_parts": False,
                        "components": [{"name": "A", "function": "does a", "parts": []}]}
        assert store.calls == 1
        store.result = ((), (dataclasses.replace(comp, subsystem_ids=("sub-x",)),))
        assert appmod._component_report_view("sid") == {"available": False}   # unresolvable part
        store.result = ((), ())
        assert appmod._component_report_view("sid") == {"available": True, "has_parts": False,
                                                       "components": []}
    finally:
        appmod._get_store = real


# ==========================================================================
# 3. One snapshot, no writes, no new audience, escaping, the rest unchanged
# ==========================================================================
def test_a01_one_inventory_read_per_render_for_html_and_pdf(client, monkeypatch):
    sid = _integrated(client)
    _declare(sid, "Counted", "Once")
    store = _store()
    real = store.load_component_inventory
    calls = []

    def spy(project_id):
        calls.append(project_id)
        return real(project_id)
    monkeypatch.setattr(store, "load_component_inventory", spy)
    _report(client, sid)
    assert calls == [sid]
    calls.clear()
    _pdf_source(client, sid, monkeypatch)
    assert calls == [sid]


def test_a02_opening_the_report_or_pdf_writes_nothing(client, monkeypatch):
    sid = _integrated(client)
    _declare(sid, "Read only", "Never written by a read")
    _report(client, sid)                                   # warm any lazy state first
    before = _dump()
    _report(client, sid)
    _pdf_source(client, sid, monkeypatch)
    assert _dump() == before


def test_a03_the_audience_is_unchanged_owner_only_for_owned_projects():
    appmod.app.config["TESTING"] = True
    owner, aid = _client_for("dcv-audience-owner@example.com")
    sid = _journey(owner)
    _declare(sid, "Owner-only component", "Private text")
    assert "Owner-only component" in _report(owner, sid)
    other, _ = _client_for("dcv-audience-other@example.com")
    anon = csrf_client(appmod.app)
    for c in (other, anon):
        for r in (c.get(f"/session/{sid}/deliverable"), c.post(f"/session/{sid}/deliverable.pdf", data={})):
            assert r.status_code == 302 and r.headers["Location"].endswith("/")
            assert b"Owner-only component" not in r.data
        page = c.get(f"/session/{sid}")
        assert page.status_code == 302                     # the same principal set as the session page


def test_a04_inventor_text_is_escaped_and_direction_isolated(client):
    sid = _ordinary(client)
    _declare(sid, "<script>x()</script>", "حساس <b>حرارة</b> & more")
    raw = _report(client, sid)
    section = _section(raw)
    assert "<script>x()</script>" not in raw and "&lt;script&gt;" in section
    assert "<b>حرارة</b>" not in section
    assert re.search(r'<bdi dir="auto" data-dc-name>&lt;script&gt;', section)
    assert re.search(r'<bdi dir="auto" data-dc-function>حساس &lt;b&gt;', section)


def test_a05_outside_the_section_the_report_is_unchanged(client):
    sid = _integrated(client)
    before = _report(client, sid)
    _declare(sid, "Added later", "Changes only the section")
    after = _report(client, sid)
    assert _stable(_without_section(after)) == _stable(_without_section(before))
    assert "Added later" in _section(after) and "Added later" not in _without_section(after)


def test_a06_arabic_copy(client):
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    sid = _ordinary(client)
    _declare(sid, "Motor", "محرّك صغير")
    raw = _report(client, sid)
    section = _html.unescape(_section(raw))
    for key in ("UI_CI_HEADING", "UI_CI_BOUNDARY", "UI_DC_PROVENANCE", "UI_DC_HISTORY", "UI_CI_FUNCTION_LABEL"):
        assert ui_text.text(key, "ar") in section, key
    assert 'dir="rtl"' in raw
    for key in ("UI_DC_PROVENANCE", "UI_DC_NONE", "UI_DC_HISTORY", "UI_DC_UNAVAILABLE"):
        entry = ui_text.UI_STRINGS[key]
        assert entry["en"].strip() and entry["ar"].strip() and entry["en"] != entry["ar"], key
