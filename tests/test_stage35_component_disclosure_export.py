"""STAGE35-COMPONENT-DISCLOSURE-EXPORT-01 — the Stage 35 disclosure export v2 carries the inventor's declared
components in field 7 (``component_descriptions_beyond_parts``).

What is pinned:
- v2 = v1 plus exactly ONE item kind, ``component``: name and function quoted verbatim, the inventory owner's own
  OWNER_STATED / UNVALIDATED envelope under ``SUBSYSTEM_COMPOSITION``, one ref per declared part (none = project
  level), durable order, each component once; components present -> RECORDED, none -> NOTHING_RECORDED (never
  NOT_CAPTURED), on integrated AND ordinary projects;
- the inventory is read inside the export's ONE store-owned snapshot through the seventh R1 admission of
  ``load_component_inventory``; its composition must equal the reconstructed parts; anything corrupt, foreign or
  inconsistent refuses the WHOLE export (bare empty 503, no file);
- the shared reader keeps its committed-read behaviour for its session-page caller and only strengthens refusal;
- every other field, the disclaimers and the scope label are unchanged; JSON content is locale-independent; EN / AR
  HTML with RTL; no component id anywhere; no write.
"""
import copy
import html as _html
import json
import os
import re
import sqlite3

import pytest

import web.app as webapp
from engine import disclosure_export as dx
from engine import subsystem_model as sm
from engine.record_store import (
    ProjectComponentsCorrupt, RecordStoreConnectionUnsafe, SqliteRecordStore)
from tests.test_stage15_integrated_invention_entry import MECH, TIE_IDEA, _compose, _created, _pair, _contract, _ri
from tests.test_stage19_durable_success_criteria import _client_for, _journey
from tests.test_stage35_disclosure_projection import _rich_sources
from web import ui_text

PAGE = "/account/projects/%s/disclosure-export"
JSON_URL = PAGE + "/json"
HTML_URL = PAGE + "/html"
F7 = "component_descriptions_beyond_parts"


@pytest.fixture()
def ordinary():
    webapp.app.config["TESTING"] = True
    c, aid = _client_for("s35c-ordinary@example.com")
    return c, aid, _journey(c)


@pytest.fixture()
def integrated():
    webapp.app.config["TESTING"] = True
    c, aid = _client_for("s35c-integrated@example.com")
    return c, aid, _created(_compose(c, TIE_IDEA, focus=MECH))


def _store():
    return webapp._get_store()


def _declare(sid, name, function, domains=(), key=None):
    subs = _store().load_project_subsystems(sid)
    parts = tuple(s.subsystem_id for s in subs if s.domain in domains)
    item = sm.declared_component(subs, name, function, parts)
    _store().append_project_component(sid, item, key or ("k-" + name))
    return item


def _doc(c, sid):
    r = c.get(JSON_URL % sid)
    assert r.status_code == 200, r.status_code
    return json.loads(r.data.decode("utf-8"))


def _field(content, token):
    [f] = [f for f in content["fields"] if f["field"] == token]
    return f


def _dump():
    con = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        return list(con.iterdump())
    finally:
        con.close()


def _raw(sql, params=()):
    _store()
    con = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        con.execute(sql, params)
        con.commit()
    finally:
        con.close()


# ==========================================================================
# 1. Field 7 on ordinary and integrated projects
# ==========================================================================
def test_v2_versions_and_closed_vocabulary():
    # AMENDED at PATHN-CONSTRAINT-DECLARATION-01 (Owner-approved v3): v3 = v2 plus
    # field 30 and ONE item kind (`constraint`); the field-7 rules below are unchanged.
    assert dx.DISCLOSURE_SCHEMA_VERSION == "inventorai-disclosure/3"
    assert (dx.JSON_FORMAT_VERSION, dx.HTML_FORMAT_VERSION) == (
        "inventorai-disclosure-json/3", "inventorai-disclosure-html/3")
    assert (dx.JSON_FILE_NAME, dx.HTML_FILE_NAME) == (
        "inventorai-disclosure-export-v3.json", "inventorai-disclosure-export-v3.html")
    assert len(dx.ITEM_KINDS) == 19 and "component" in dx.ITEM_KINDS     # v2 kind kept; v3 adds one
    assert "SUBSYSTEM_COMPOSITION" in dx.SOURCE_OWNERS and len(dx.SOURCE_OWNERS) == 13
    assert dx._FIELD_DISPOSITIONS[F7] == {(dx.RECORDED, None, None), (dx.NOTHING_RECORDED, None, None)}


@pytest.mark.parametrize("project", ["ordinary", "integrated"])
def test_no_components_is_nothing_recorded_never_not_captured(request, project):
    c, aid, sid = request.getfixturevalue(project)
    f = _field(_doc(c, sid)["content"], F7)
    assert (f["marker"], f["reason"], f["pointer"], f["items"]) == ("NOTHING_RECORDED", None, None, [])


def test_ordinary_project_components_are_project_level(ordinary):
    c, aid, sid = ordinary
    first = _declare(sid, "Thermal fuse <TF-1>", "Cuts power & stops heating")
    _declare(sid, "حساس حرارة", "يقيس درجة الحرارة")
    doc = _doc(c, sid)
    f = _field(doc["content"], F7)
    assert f["marker"] == "RECORDED" and [i["item_key"] for i in f["items"]] == [F7 + ".1", F7 + ".2"]
    one, two = f["items"]
    assert one["kind"] == "component" and one["refs"] == [] and one["tokens"] == {}
    assert one["slots"]["name"]["value"] == "Thermal fuse <TF-1>"          # verbatim, JSON-escaped only
    assert one["slots"]["function"]["value"] == "Cuts power & stops heating"
    assert two["slots"]["name"]["value"] == "حساس حرارة"
    for slot in one["slots"].values():
        assert slot["content_class"] == "QUOTED_INVENTOR_CONTENT"
        assert slot["source_owner"] == "SUBSYSTEM_COMPOSITION"
        assert slot["envelope"]["provenance"] == {"marker": "RECORDED", "value": "OWNER_STATED"}
        assert slot["envelope"]["validation_state"] == {"marker": "RECORDED", "value": "UNVALIDATED"}
        assert slot["envelope"]["currency"]["marker"] == "NOT_APPLICABLE"
    assert first.component_id not in json.dumps(doc)
    assert (_field(doc["content"], "parts")["marker"],
            _field(doc["content"], "parts")["reason"]) == ("NOT_CAPTURED", "NON_INTEGRATED_PROJECT")


def test_integrated_components_once_each_with_all_part_refs_in_durable_order(integrated):
    c, aid, sid = integrated
    items = [_declare(sid, "Motor", "Turns the arm", ("mechanical", "electronics_electrical")),
             _declare(sid, "Gearbox", "Slows the motor", ("mechanical",)),
             _declare(sid, "Mounting kit", "Holds everything", ()),
             _declare(sid, "Driver board", "Switches the motor", ("electronics_electrical",))]
    content = _doc(c, sid)["content"]
    parts = _field(content, "parts")["items"]
    keys = {p["tokens"]["part_domain"]: p["item_key"] for p in parts}
    f = _field(content, F7)
    assert [i["slots"]["name"]["value"] for i in f["items"]] == ["Motor", "Gearbox", "Mounting kit",
                                                                  "Driver board"]
    assert [i["refs"] for i in f["items"]] == [
        [keys["mechanical"], keys["electronics_electrical"]], [keys["mechanical"]], [],
        [keys["electronics_electrical"]]]
    dumped = json.dumps(content)
    for item in items:
        assert item.component_id not in dumped
    for sub in _store().load_project_subsystems(sid):
        assert sub.subsystem_id not in dumped


# ==========================================================================
# 2. One snapshot, refusal, authorization, no writes
# ==========================================================================
def test_the_inventory_is_read_inside_the_one_export_snapshot(integrated):
    c, aid, sid = integrated
    _declare(sid, "Motor", "Turns", ("mechanical",))
    store = _store()
    seen = []
    store._conn.set_trace_callback(seen.append)
    try:
        assert c.get(JSON_URL % sid).status_code == 200
    finally:
        store._conn.set_trace_callback(None)
    begins = [i for i, s in enumerate(seen) if s.startswith("SAVEPOINT")]
    ends = [i for i, s in enumerate(seen) if s.startswith("RELEASE")]
    component_reads = [i for i, s in enumerate(seen) if "FROM project_components" in s]
    assert component_reads
    window = [(b, e) for b, e in zip(begins, ends) if any(b < i < e for i in component_reads)]
    assert len(window) == 1                                       # one snapshot holds every component read
    b, e = window[0]
    assert all(b < i < e for i in component_reads)
    assert any("FROM project_subsystems" in seen[i] for i in range(b, e))
    assert any("FROM records" in seen[i] or "FROM project" in seen[i] for i in range(b, e))


@pytest.mark.parametrize("url", [JSON_URL, HTML_URL])
def test_corrupt_inventory_refuses_the_whole_export(integrated, url):
    c, aid, sid = integrated
    _declare(sid, "Motor", "Turns", ("mechanical",))
    _raw("UPDATE project_components SET subsystem_ids = ? WHERE project_id = ?",
         ('["sub-' + "9" * 32 + '"]', sid))
    r = c.get(url % sid)
    assert (r.status_code, r.data) == (503, b"") and "Content-Disposition" not in r.headers


@pytest.mark.parametrize("url", [JSON_URL, HTML_URL])
def test_a_failing_inventory_read_refuses_the_whole_export(ordinary, monkeypatch, url):
    c, aid, sid = ordinary

    def boom(*a, **kw):
        raise sqlite3.OperationalError("disk I/O error")
    monkeypatch.setattr(_store(), "load_component_inventory", boom)
    r = c.get(url % sid)
    assert (r.status_code, r.data) == (503, b"")


def test_a_composition_that_is_not_the_reconstructed_one_refuses():
    sources = _rich_sources()
    other = (sm.declared_subsystem("mechanical", "Other arm", "Moves"),
             sm.declared_subsystem("electronics_electrical", "Other board", "Switches"))
    bad = dx.MaterializedSources(
        state=sources.state, requirement_quantities=sources.requirement_quantities,
        planning_metadata=sources.planning_metadata,
        interface_dependencies=sources.interface_dependencies, result_events=sources.result_events,
        component_composition=other, components=())
    with pytest.raises(dx.DisclosureExportRefused):
        dx.compose_projection(bad)


def test_a_component_naming_an_unknown_part_refuses():
    sources = _rich_sources()
    subs = tuple(sources.state.subsystems)
    stray = sm.ProjectComponent(component_id=sm.new_component_id(), display_name="X", function_text="Y",
                                subsystem_ids=("sub-" + "7" * 32,), provenance="OWNER_STATED",
                                validation_state="UNVALIDATED")
    bad = dx.MaterializedSources(
        state=sources.state, requirement_quantities=sources.requirement_quantities,
        planning_metadata=sources.planning_metadata,
        interface_dependencies=sources.interface_dependencies, result_events=sources.result_events,
        component_composition=subs, components=(stray,))
    with pytest.raises(dx.DisclosureExportRefused):
        dx.compose_projection(bad)


def _component_content(**override):
    sources = _rich_sources()
    subs = tuple(sources.state.subsystems)
    comp = sm.declared_component(subs, "Motor", "Turns", (subs[0].subsystem_id,))
    content = dx.compose_projection(dx.MaterializedSources(
        state=sources.state, requirement_quantities=sources.requirement_quantities,
        planning_metadata=sources.planning_metadata,
        interface_dependencies=sources.interface_dependencies, result_events=sources.result_events,
        component_composition=subs, components=(comp,)))
    return content


@pytest.mark.parametrize("mutate", [
    lambda item: item["tokens"].update({"part_domain": "mechanical"}),        # no token is allowed
    lambda item: item["refs"].append(item["refs"][0]),                        # duplicate ref
    lambda item: item["refs"].append("relationships.1"),                      # ref to a non-part
    lambda item: item["slots"].update({"description": item["slots"]["name"]}),  # foreign slot
    lambda item: item["slots"]["name"].update({"source_owner": "COMPONENT_INVENTORY"}),  # no new owner token
    lambda item: item["slots"]["name"]["envelope"]["currency"].update(
        {"marker": "RECORDED", "value": "CURRENT"}),                          # owner holds no currency
])
def test_the_schema_check_refuses_a_malformed_component_item(mutate):
    content = _component_content()
    item = _field(content, F7)["items"][0]
    mutate(item)
    with pytest.raises(dx.DisclosureExportRefused):
        dx.check_projection(content)


def test_foreign_and_anonymous_access_are_denied_like_a_missing_project(integrated):
    c, aid, sid = integrated
    _declare(sid, "Secret motor", "Turns", ("mechanical",))
    other, _ = _client_for("s35c-other@example.com")
    for url in (JSON_URL, HTML_URL):
        missing, foreign = other.get(url % "no-such-project"), other.get(url % sid)
        assert (missing.status_code, missing.data) == (foreign.status_code, foreign.data)
        assert b"Secret motor" not in foreign.data


def test_downloads_write_nothing(integrated):
    c, aid, sid = integrated
    _declare(sid, "Motor", "Turns", ("mechanical",))
    before = _dump()
    for lang in ("en", "ar"):
        if lang == "ar":
            c.post("/ui-language", data={"lang": "ar"})
            before = _dump()
        assert c.get(JSON_URL % sid).status_code == 200
        assert c.get(HTML_URL % sid).status_code == 200
        assert _dump() == before


# ==========================================================================
# 3. Unrelated content unchanged; locale parity
# ==========================================================================
def test_only_field_7_changes_when_components_are_declared(integrated):
    c, aid, sid = integrated
    before = _doc(c, sid)["content"]
    _declare(sid, "Motor", "Turns", ("mechanical",))
    after = _doc(c, sid)["content"]
    for key in ("disclaimers", "scope_label", "unavailable_notice"):
        assert before[key] == after[key]
    assert after["disclaimers"] == [{"id": i, "en": en, "ar": ar} for i, en, ar in dx.DISCLAIMERS]
    for b, a in zip(before["fields"], after["fields"]):
        if b["field"] != F7:
            assert a == b, b["field"]
    assert _field(before, F7)["marker"] == "NOTHING_RECORDED" and _field(after, F7)["marker"] == "RECORDED"


def test_json_content_is_locale_independent(integrated):
    c, aid, sid = integrated
    _declare(sid, "Motor", "Turns", ("mechanical", "electronics_electrical"))
    en = _doc(c, sid)
    c.post("/ui-language", data={"lang": "ar"})
    ar = _doc(c, sid)
    assert en["content"] == ar["content"] and en["content_digest"] == ar["content_digest"]


# ==========================================================================
# 4. HTML EN / AR
# ==========================================================================
@pytest.mark.parametrize("lang", ["en", "ar"])
def test_html_shows_each_component_with_its_parts_or_project_level(integrated, lang):
    c, aid, sid = integrated
    _declare(sid, "Motor <M1>", "Turns the arm", ("mechanical", "electronics_electrical"))
    _declare(sid, "Mounting kit", "Holds everything", ())
    if lang == "ar":
        c.post("/ui-language", data={"lang": "ar"})
    body = c.get(HTML_URL % sid).data.decode("utf-8")
    t = lambda k: ui_text.text(k, lang)
    section = body[body.index('id="field-%s"' % F7):body.index('id="field-relationships"')]
    assert section.count('data-kind="component"') == 2
    assert "Motor &lt;M1&gt;" in section and "<M1>" not in section
    assert _html.escape(t("UI_S35_COMPONENTS_CLARIFICATION"), quote=True) in section \
        or t("UI_S35_COMPONENTS_CLARIFICATION").replace("'", "&#39;") in section
    assert t("UI_S35_COMPONENT_LABEL") in section
    assert section.count("data-component-parts") == 1 and section.count("data-component-project-level") == 1
    assert 'href="#parts.1"' in section and 'href="#parts.2"' in section
    assert t("UI_S35_COMPONENT_PROJECT_LEVEL") in section
    assert ui_text.text("UI_S35_SOURCE_OWNER_STATED", lang) in section     # "Inventor", never "You"
    assert ('<html lang="ar" dir="rtl">' in body) == (lang == "ar")
    assert "inventorai-disclosure-html/3" in body          # v3 (PATHN-CONSTRAINT-DECLARATION-01)


def test_html_without_components_shows_nothing_recorded(ordinary):
    c, aid, sid = ordinary
    body = c.get(HTML_URL % sid).data.decode("utf-8")
    section = body[body.index('id="field-%s"' % F7):body.index('id="field-relationships"')]
    assert 'data-marker="NOTHING_RECORDED"' in section and "data-components-clarification" not in section
    assert ui_text.text("UI_S35_MARKER_NOT_CAPTURED", "en") not in section


def test_new_copy_keys_are_bilingual_and_neutral():
    for key in ("UI_S35_COMPONENT_LABEL", "UI_S35_COMPONENT_PARTS", "UI_S35_COMPONENT_PROJECT_LEVEL",
                "UI_S35_COMPONENTS_CLARIFICATION"):
        en, ar = ui_text.text(key, "en"), ui_text.text(key, "ar")
        assert en and ar and en != ar
        assert not re.search(r"\byou\b|\byour\b", en, re.I)


# ==========================================================================
# 5. The shared reader (seventh R1 admission) keeps its callers' behaviour
# ==========================================================================
def _store_project(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "r.db"))
    subs = _pair()
    pid = store.create_project(_contract("i-s35c"), reconstruction_inputs=_ri(MECH), subsystems=subs)
    store.append_project_component(pid, sm.declared_component(subs, "Motor", "Turns",
                                                              (subs[0].subsystem_id,)), "k1")
    return store, pid, subs


def test_standalone_committed_read_is_unchanged(tmp_path):
    store, pid, subs = _store_project(tmp_path)
    got_subs, items = store.load_component_inventory(pid)
    assert got_subs == subs and [i.display_name for i in items] == ["Motor"]


def test_inside_an_owned_snapshot_the_read_is_admitted_and_joins_it(tmp_path):
    store, pid, subs = _store_project(tmp_path)
    seen = []
    with store.read_snapshot():
        store._conn.set_trace_callback(seen.append)
        _subs, items = store.load_component_inventory(pid)
        store._conn.set_trace_callback(None)
    assert [i.display_name for i in items] == ["Motor"]
    assert not [s for s in seen if s.startswith("SAVEPOINT")]          # no second snapshot is opened


def test_a_lost_snapshot_and_the_unsafe_state_refuse(tmp_path):
    store, pid, subs = _store_project(tmp_path)
    with store.read_snapshot():
        store._conn.execute("RELEASE SAVEPOINT need_routing_read_snapshot")   # lost underneath its owner
        with pytest.raises(RecordStoreConnectionUnsafe):
            store.load_component_inventory(pid)
        store._conn.execute("SAVEPOINT need_routing_read_snapshot")          # let the owner release it
    store._connection_unsafe = True
    with pytest.raises(RecordStoreConnectionUnsafe):
        store.load_component_inventory(pid)


def test_a_bare_caller_owned_transaction_is_now_refused(tmp_path):
    """The only strengthening: a read inside an unresolved caller-owned write transaction
    (uncommitted state) is refused, as the six other R1 readers already do."""
    store, pid, subs = _store_project(tmp_path)
    store._conn.execute("BEGIN")
    try:
        with pytest.raises(RecordStoreConnectionUnsafe):
            store.load_component_inventory(pid)
    finally:
        store._conn.execute("ROLLBACK")
    assert len(store.load_component_inventory(pid)[1]) == 1


def test_whole_collection_validation_is_unchanged(tmp_path):
    store, pid, subs = _store_project(tmp_path)
    store._conn.execute("UPDATE project_components SET subsystem_ids = ? WHERE project_id = ?",
                        ('["sub-' + "9" * 32 + '"]', pid))
    with pytest.raises(ProjectComponentsCorrupt):
        store.load_component_inventory(pid)


def test_the_session_page_component_list_is_unchanged(integrated):
    c, aid, sid = integrated
    _declare(sid, "Motor", "Turns", ("mechanical",))
    page = c.get("/session/%s" % sid).get_data(as_text=True)
    block = re.search(r'<details id="component-inventory".*?</details>', page, re.S).group(0)
    assert 'data-ci-status="available"' in block and block.count("<li data-ci-item ") == 1
    assert ">Motor<" in block
