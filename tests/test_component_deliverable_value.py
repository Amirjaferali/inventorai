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

COMPONENT-PROTOTYPE-NEED-HANDOFF-01 (section 4) intentionally advances the earlier session-only boundary of the
PR #820 prototype-need note: each current component in this section also carries its CURRENT note — verbatim,
escaped, direction-isolated, OWNER_STATED / UNVALIDATED — or "not stated", read through the existing
``load_component_prototype_needs`` snapshot and shown only when that snapshot's current components equal the
listed ones; an unreadable, corrupt or inconsistent note record reads as ONE "notes unavailable" notice (never
"not stated", never a partial set) while the component list stays.
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
        # Advanced by COMPONENT-PROTOTYPE-NEED-HANDOFF-01: a store without the notes reader reads the notes
        # as unavailable, never as "not stated".
        assert view == {"available": True, "has_parts": False, "needs_available": False,
                        "components": [{"name": "A", "function": "does a", "parts": [],
                                        "need": None}]}
        assert store.calls == 1
        store.result = ((), (dataclasses.replace(comp, subsystem_ids=("sub-x",)),))
        assert appmod._component_report_view("sid") == {"available": False}   # unresolvable part
        store.result = ((), ())
        assert appmod._component_report_view("sid") == {"available": True, "has_parts": False,
                                                       "needs_available": False, "components": []}
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


# ==========================================================================
# 4. COMPONENT-PROTOTYPE-NEED-HANDOFF-01 — the current prototype-need note beside its component
# ==========================================================================
NOTE_RE = re.compile(r"<bdi dir=\"auto\" data-dc-need-text>(.*?)</bdi>", re.S)


def _note(sid, item, text):
    _store().set_component_prototype_need(sid, item.component_id,
                                          sm.normalize_prototype_need_text(text), None)


def _notes(section):
    """``[note | None]`` per rendered item, in order (None = "not stated")."""
    out = []
    for li in re.findall(r"<li data-dc-item.*?</li>", section, re.S):
        m = NOTE_RE.search(li)
        assert (m is None) == ("data-dc-need-none" in li), li
        out.append(_html.unescape(m.group(1)) if m else None)
    return out


def test_n01_recorded_notes_appear_in_html_and_pdf_beside_their_component(client, monkeypatch):
    sid = _integrated(client)
    both = _declare(sid, "Shared harness", "Links both parts",
                    domains=("mechanical", "electronics_electrical"))
    _declare(sid, "Bare bracket", "Holds the board")
    _note(sid, both, "  four similar units, 2 spare  ")
    for raw in (_report(client, sid), _pdf_source(client, sid, monkeypatch)):
        section = _section(raw)
        assert [i[0] for i in _items(section)] == ["Shared harness", "Bare bracket"]   # one item per component
        assert len(_items(section)[0][2]) == 2                                         # both part links kept
        assert _notes(section) == ["four similar units, 2 spare", None]
        assert section.count("data-dc-need-status") == 1 and _has(section, "UI_DC_NEED_STATUS")
        assert _has(section, "UI_CI_NEED_NOT_STATED") and "data-dc-need-unavailable" not in section
        assert "four similar units" not in _without_section(raw)


def test_n02_corrected_component_keeps_its_note_and_a_withdrawn_one_shows_none(client, monkeypatch):
    sid = _ordinary(client)
    kept = _declare(sid, "Wheel v1", "Rolls")
    gone = _declare(sid, "Old axle", "Was replaced")
    _note(sid, kept, "four wheels")
    _note(sid, gone, "Zq-withdrawn-note-881")
    _correct(sid, kept.component_id, "Wheel v2", "Rolls smoothly")
    _withdraw(sid, gone.component_id)
    for raw in (_report(client, sid), _pdf_source(client, sid, monkeypatch)):
        section = _section(raw)
        assert [i[:2] for i in _items(section)] == [("Wheel v2", "Rolls smoothly")]
        assert _notes(section) == ["four wheels"]
        assert "Zq-withdrawn-note-881" not in raw and "Wheel v1" not in raw and "Old axle" not in raw


def _unavailable_notes(section, *hidden):
    assert "data-dc-need-unavailable" in section and _has(section, "UI_DC_NEED_UNAVAILABLE")
    for marker in ("data-dc-need-none", "data-dc-need-text", "data-dc-need-status"):
        assert marker not in section, marker
    for text in hidden:
        assert text not in section, text
    assert "data-dc-item" in section and "data-dc-unavailable" not in section   # the list itself stays


def test_n03_a_corrupt_note_record_reads_unavailable_never_not_stated(client, monkeypatch):
    sid = _ordinary(client)
    a = _declare(sid, "Listed part", "Still listed")
    _declare(sid, "Second part", "No note")
    _note(sid, a, "Zq-good-note-114")
    section = _section(_report(client, sid))
    assert _notes(section) == ["Zq-good-note-114", None]                 # absent reads "not stated"
    _raw("UPDATE component_prototype_needs SET need_text = ? WHERE project_id = ?", ("bad\x01", sid))
    for raw in (_report(client, sid), _pdf_source(client, sid, monkeypatch)):
        _unavailable_notes(_section(raw), "Zq-good-note-114", "bad")


@pytest.mark.parametrize("error", [RuntimeError("store down"), RecordStoreConnectionUnsafe("unsafe"),
                                   sqlite3.OperationalError("locked"), ProjectNotFound("gone")])
def test_n04_any_note_read_failure_is_unavailable(client, monkeypatch, error):
    sid = _ordinary(client)
    a = _declare(sid, "Visible part", "Visible function")
    _note(sid, a, "Zq-hidden-note-302")

    def boom(_sid):
        raise error
    monkeypatch.setattr(_store(), "load_component_prototype_needs", boom)
    _unavailable_notes(_section(_report(client, sid)), "Zq-hidden-note-302")
    monkeypatch.setattr(_store(), "load_component_prototype_needs", None)
    _unavailable_notes(_section(_report(client, sid)), "Zq-hidden-note-302")


def test_n05_notes_from_a_different_component_snapshot_are_never_shown():
    subs = ()
    a = sm.declared_component(subs, "A", "does a", ())
    b = sm.declared_component(subs, "B", "does b", ())

    class Store:
        def __init__(self, listed, noted):
            self.listed, self.noted = listed, noted

        def load_component_inventory(self, sid):
            return subs, self.listed

        def load_component_prototype_needs(self, sid):
            inventory = sm.project_component_inventory(self.noted, (), subs)
            needs = tuple(sm.ComponentPrototypeNeed(component_id=c.component_id, need_text="n-" + c.display_name)
                          for c in self.noted)
            return inventory, needs

    real = appmod._get_store
    try:
        appmod._get_store = lambda: Store((a, b), (a, b))
        view = appmod._component_report_view("sid")
        assert view["needs_available"] and [c["need"] for c in view["components"]] == ["n-A", "n-B"]
        for noted in ((a,), (b, a), (a, b, sm.declared_component(subs, "C", "does c", ())),
                      (dataclasses.replace(a, display_name="A2"), b)):
            appmod._get_store = lambda noted=noted: Store((a, b), noted)
            view = appmod._component_report_view("sid")
            assert view["needs_available"] is False, noted
            assert [c["need"] for c in view["components"]] == [None, None]
            assert [c["name"] for c in view["components"]] == ["A", "B"]
    finally:
        appmod._get_store = real


def test_n06_cold_reload_owner_only_one_read_and_nothing_written(client, monkeypatch):
    from tests.test_stage15_subsystem_interface_declaration import _restart
    appmod.app.config["TESTING"] = True
    owner, _aid = _client_for("dcv-need-owner@example.com")
    sid = _journey(owner)
    a = _declare(sid, "Private wheel", "Rolls")
    _note(sid, a, "Zq-private-note-640")
    _restart()
    assert _notes(_section(_report(owner, sid))) == ["Zq-private-note-640"]
    other, _ = _client_for("dcv-need-other@example.com")
    for c in (other, csrf_client(appmod.app)):
        for r in (c.get(f"/session/{sid}/deliverable"), c.post(f"/session/{sid}/deliverable.pdf", data={})):
            assert r.status_code == 302 and b"Zq-private-note-640" not in r.data
    store = _store()
    real = store.load_component_prototype_needs
    calls = []

    def spy(project_id):
        calls.append(project_id)
        return real(project_id)
    monkeypatch.setattr(store, "load_component_prototype_needs", spy)
    _report(owner, sid)
    assert calls == [sid]
    calls.clear()
    _pdf_source(owner, sid, monkeypatch)
    assert calls == [sid]
    before = _dump()
    _report(owner, sid)
    _pdf_source(owner, sid, monkeypatch)
    assert _dump() == before


def test_n07_escaped_isolated_arabic_and_the_disclosure_export_unchanged():
    appmod.app.config["TESTING"] = True
    c, _aid = _client_for("dcv-need-export@example.com")
    sid = _journey(c)
    a = _declare(sid, "Motor", "محرّك صغير")
    stamp = re.compile(rb"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z")
    export_before = stamp.sub(b"", c.get("/account/projects/%s/disclosure-export/json" % sid).data)
    html_before = stamp.sub(b"", c.get("/account/projects/%s/disclosure-export/html" % sid).data)
    _note(sid, a, "<script>x()</script> أربع وحدات & more")
    export_after = stamp.sub(b"", c.get("/account/projects/%s/disclosure-export/json" % sid).data)
    html_after = stamp.sub(b"", c.get("/account/projects/%s/disclosure-export/html" % sid).data)
    assert export_after == export_before and html_after == html_before
    raw = _report(c, sid)
    section = _section(raw)
    assert "<script>x()</script>" not in raw
    assert re.search(r'<bdi dir="auto" data-dc-need-text>&lt;script&gt;x\(\)&lt;/script&gt; أربع وحدات &amp; more</bdi>',
                     section)
    for key in ("UI_DC_NEED_STATUS", "UI_DC_NEED_UNAVAILABLE"):
        entry = ui_text.UI_STRINGS[key]
        assert entry["en"].strip() and entry["ar"].strip() and entry["en"] != entry["ar"], key
        for claim in ("bill of materials", " bom", "total:", "verified", "validated."):
            assert claim not in entry["en"].lower(), (key, claim)
    assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    ar = _html.unescape(_section(_report(c, sid)))
    for key in ("UI_CI_NEED_LABEL", "UI_DC_NEED_STATUS"):
        assert ui_text.text(key, "ar") in ar, key
