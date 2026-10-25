"""STAGE15-PARTS-COMPONENTS-INTERACTIONS-VIEW-01 — ONE read-only Stage 15 composition view.

What is pinned:
- offered only for a valid durable Mechanical + Electrical / Electronics integrated composition (both focus
  directions; with or without the optional part); an ordinary project gets no link and a refusal;
- ONE coherent store snapshot (``load_parts_components_interactions``) feeds every collection, each validated
  WHOLE; corrupt, unreadable or unresolved storage shows the WHOLE view unavailable, never partial or empty;
- each part (name, function, role), each component exactly ONCE with all its part associations (unassigned kept
  apart), each interaction with its preparation and dependency, recording presence only, links to the existing
  pages; no internal identifier as visible text;
- project authorization; a GET writes nothing; no calculation offer, no engineering / compatibility / validation
  claim; the report, PDF and the existing owners are unchanged.
"""
import html as _html
import re
import sqlite3

import pytest

import web.app as appmod
from engine import subsystem_model as sm
from engine.record_store import (
    InterfaceDependenciesCorrupt, PartAnswersCorrupt, ProjectComponentsCorrupt, ProjectNotFound,
    RecordStoreConnectionUnsafe, SqliteRecordStore)
from tests.test_stage15_integrated_invention_entry import ELEC, MECH, _contract, _pdf_source
from tests.test_stage28_control_loop_optional_part_slice1 import (  # noqa: F401  (fixtures)
    CL, _three_part_project, client, part_eligible)
from tests.test_stage15_integration_closure import _login
from tests.test_28t5_nonfocused_required_part_questions import (
    BA, MC, OTHER, _ids, _pack_questions, _part, _stored, _two_part)
from tests.test_component_inventory_declare_list import _ordinary, _raw
from web import ui_text

URL = "/session/%s/parts-components-interactions"
CALC_ROUTES = ("support-reactions", "temperature-difference", "form-mockup-advisory",
               "planar-moment", "rotational-load", "tmp36-temperature",
               "control-cycle", "temperature-control-condition", "dc-load-current")


def _get(c, sid, lang="en"):
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    return c.get(URL % sid)


def _visible(raw):
    """The page's visible text: tags and attribute values removed, entities decoded."""
    body = raw.split('<main id="main-content">', 1)[1]
    return _html.unescape(re.sub(r"<[^>]+>", " ", body))


def _t(key, lang="en"):
    return ui_text.text(key, lang)


def _store():
    return appmod._get_store()


def _subs(sid):
    return {s.domain: s for s in _store().load_project_subsystems(sid)}


def _component(sid, name, function, domains, key):
    subs = _store().load_project_subsystems(sid)
    parts = tuple(s.subsystem_id for s in subs if s.domain in domains)
    _store().append_project_component(sid, sm.declared_component(subs, name, function, parts), key)


def _interface(sid, x, y, description, key):
    subs = _store().load_project_subsystems(sid)
    by = {s.domain: s.subsystem_id for s in subs}
    ifc = sm.declared_interface(subs, by[x], by[y], description)
    _store().append_subsystem_interface(sid, ifc, key)
    return ifc


def _db_dump():
    _store()
    conn = sqlite3.connect(appmod.os.environ["INVENTORAI_DB_PATH"])
    try:
        return list(conn.iterdump())
    finally:
        conn.close()


# ==========================================================================
# 1. Store: one coherent, project-scoped snapshot
# ==========================================================================
@pytest.mark.parametrize("focus", [MECH, ELEC])
def test_s01_one_reader_returns_every_collection_of_this_project_only(tmp_path, focus):
    store = SqliteRecordStore(str(tmp_path / "r.db"))
    pid, mech, elec, ctrl = _stored(store, focus=focus, with_ctrl=True)
    other_pid, *_rest = _stored(store, focus=focus, idea_id="i-other")
    subs = (mech, elec, ctrl)
    ifc = sm.declared_interface(subs, mech.subsystem_id, elec.subsystem_id, "Motor drives the arm")
    store.append_subsystem_interface(pid, ifc, "i1")
    store.apply_interface_preparation_delta(
        pid, {ifc.interface_id: {sm.PREPARATION_OPERATING_CONDITIONS: "Indoors"}},
        dependency_delta={ifc.interface_id: sm.InterfaceDependency(ifc.interface_id, sm.DEPENDENCY_MUTUAL)})
    store.append_project_component(pid, sm.declared_component(subs, "Motor", "Turns", (
        mech.subsystem_id, elec.subsystem_id)), "c1")
    nonfocused = elec if focus == MECH else mech
    store.apply_part_answer_delta(pid, nonfocused.subsystem_id, {_ids(nonfocused.domain)[0]: "Ours"})
    store.apply_part_answer_delta(pid, ctrl.subsystem_id, {"control_loop:MECHANISM_COMPLETENESS:Q1": "Loop"})
    record = store.load_parts_components_interactions(pid)
    # AMENDED at COMPONENT-INVENTORY-CORRECT-WITHDRAW-01: the loader also returns the withdrawn
    # components (historical, apart from the CURRENT ``components`` projection).
    # AMENDED at COMPONENT-INTERFACE-PARTICIPATION-01: and every stored participation row of
    # this project's interactions, validated in the same snapshot.
    assert set(record) == {"subsystems", "focus", "interfaces", "preparations", "dependencies",
                           "components", "withdrawn_components", "part_answers",
                           "participations"}
    assert record["withdrawn_components"] == ()
    assert record["participations"] == ()
    assert record["subsystems"] == subs and record["focus"] == focus
    assert record["interfaces"] == (ifc,)
    assert [p.interface_id for p in record["preparations"]] == [ifc.interface_id]
    assert [d.kind for d in record["dependencies"]] == [sm.DEPENDENCY_MUTUAL]
    assert [c.display_name for c in record["components"]] == ["Motor"]
    assert sorted(a.answer_text for a in record["part_answers"]) == ["Loop", "Ours"]
    other = store.load_parts_components_interactions(other_pid)
    assert other["interfaces"] == () and other["components"] == () and other["part_answers"] == ()
    with pytest.raises(ProjectNotFound):
        store.load_parts_components_interactions("no-such-project")


def test_s02_an_ordinary_project_reads_an_empty_composition(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "o.db"))
    pid = store.create_project(_contract("i-ord"))
    record = store.load_parts_components_interactions(pid)
    assert record["subsystems"] == () and record["components"] == () and record["interfaces"] == ()


def test_s03_every_read_happens_inside_one_snapshot(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "t.db"))
    pid, *_parts = _stored(store)
    seen = []
    store._conn.set_trace_callback(seen.append)
    store.load_parts_components_interactions(pid)
    store._conn.set_trace_callback(None)
    begin = next(i for i, s in enumerate(seen) if s.startswith("SAVEPOINT"))
    end = next(i for i, s in enumerate(seen) if s.startswith("RELEASE"))
    selects = [i for i, s in enumerate(seen) if s.lstrip().upper().startswith("SELECT")]
    assert selects and all(begin < i < end for i in selects)
    assert not [s for s in seen if re.match(r"\s*(INSERT|UPDATE|DELETE|CREATE|DROP)", s, re.I)]


@pytest.mark.parametrize("corrupt,error", [
    ("UPDATE project_components SET subsystem_ids = '[\"sub-" + "9" * 32 + "\"]'", ProjectComponentsCorrupt),
    ("UPDATE subsystem_interface_dependencies SET dependency_kind = 'sideways'", InterfaceDependenciesCorrupt),
    ("INSERT_ANSWER", PartAnswersCorrupt),
])
def test_s04_a_corrupt_collection_fails_the_whole_read_closed(tmp_path, corrupt, error):
    path = str(tmp_path / "c.db")
    store = SqliteRecordStore(path)
    pid, mech, elec = _stored(store)
    ifc = sm.declared_interface((mech, elec), mech.subsystem_id, elec.subsystem_id, "Link")
    store.append_subsystem_interface(pid, ifc, "i1")
    store.apply_interface_preparation_delta(pid, {}, dependency_delta={
        ifc.interface_id: sm.InterfaceDependency(ifc.interface_id, sm.DEPENDENCY_MUTUAL)})
    store.append_project_component(pid, sm.declared_component((mech, elec), "M", "F", ()), "c1")
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = OFF")
    conn.execute("PRAGMA ignore_check_constraints = ON")
    if corrupt == "INSERT_ANSWER":   # an answer about the FOCUSED part is never a stored part answer
        conn.execute("INSERT INTO subsystem_part_answers (project_id, subsystem_id, question_id, answer_text) "
                     "VALUES (?, ?, ?, ?)", (pid, mech.subsystem_id, _ids(MECH)[0], "smuggled"))
    else:
        conn.execute(corrupt + " WHERE project_id = ?", (pid,))
    conn.commit()
    conn.close()
    with pytest.raises(error):
        SqliteRecordStore(path).load_parts_components_interactions(pid)


def test_s05_an_unresolved_connection_refuses_before_any_read(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "u.db"))
    pid, *_parts = _stored(store)
    store._connection_unsafe = True
    seen = []
    store._conn.set_trace_callback(seen.append)
    with pytest.raises(RecordStoreConnectionUnsafe):
        store.load_parts_components_interactions(pid)
    assert seen == []


# ==========================================================================
# 2. The page: offered only for a valid integrated composition
# ==========================================================================
@pytest.mark.parametrize("focus", [MECH, ELEC])
def test_w01_both_focus_directions_show_each_part_with_its_role_and_links(client, focus):
    sid = _two_part(client, focus)
    subs = _subs(sid)
    session = client.get("/session/%s" % sid).get_data(as_text=True)
    assert session.count("data-scope-pci-link") == 1 and URL % sid in session
    r = _get(client, sid)
    assert r.status_code == 200 and r.headers["Cache-Control"] == "no-store"
    raw = r.get_data(as_text=True)
    text = _visible(raw)
    assert _t("UI_PCI_TITLE") in text and _t("UI_PCI_BOUNDARY") in text and _t("UI_PCI_PRESENCE_NOTE") in text
    roles = re.findall(r'data-pci-part-role="([^"]+)"', raw)
    expected = {MECH: "UI_PCI_ROLE_FOCUS" if focus == MECH else "UI_PCI_ROLE_REQUIRED",
                ELEC: "UI_PCI_ROLE_FOCUS" if focus == ELEC else "UI_PCI_ROLE_REQUIRED"}
    assert roles == [expected[MECH], expected[ELEC]]
    names = [_html.unescape(x) for x in re.findall(r"data-pci-part-name>([^<]*)<", raw)]
    assert names == [subs[MECH].display_name, subs[ELEC].display_name]
    other = subs[OTHER[focus]]
    assert raw.count("data-pci-main-link") == 1
    links = re.findall(r'href="([^"]*)" data-pci-questions-link', raw)
    assert [_html.unescape(x) for x in links] == ["/session/%s/part-questions?part=%s" % (sid, other.subsystem_id)]
    for sub in subs.values():                                   # identities travel only in a URL
        assert sub.subsystem_id not in text
    assert sid not in text


def test_w02_an_ordinary_project_has_no_link_and_the_view_is_not_offered(client):
    sid = _ordinary(client)
    assert "data-scope-pci-link" not in client.get("/session/%s" % sid).get_data(as_text=True)
    r = _get(client, sid)
    raw = r.get_data(as_text=True)
    assert r.status_code == 404 and 'data-pci-notice="UI_PCI_NOT_OFFERED"' in raw
    assert "data-pci-parts" not in raw and "data-pci-components" not in raw


def test_w03_a_session_without_a_saved_project_is_refused(client, monkeypatch):
    sid = _two_part(client, MECH)
    monkeypatch.setattr(_store(), "load_owner", lambda _sid: (False, None))
    r = _get(client, sid)
    assert r.status_code == 409 and 'data-pci-notice="UI_PCI_NO_PROJECT"' in r.get_data(as_text=True)


def test_w04_each_component_appears_once_with_all_its_part_associations(client):
    sid = _two_part(client, MECH)
    subs = _subs(sid)
    _component(sid, "Brushless motor", "Turns the arm", (MECH, ELEC), "k1")
    _component(sid, "Gearbox", "Slows the motor", (MECH,), "k2")
    _component(sid, "Mounting kit", "Holds everything", (), "k3")
    raw = _get(client, sid).get_data(as_text=True)
    names = [_html.unescape(x) for x in re.findall(r"data-pci-component-name>([^<]*)<", raw)]
    assert names == ["Brushless motor", "Gearbox", "Mounting kit"]          # once each, declared order
    linked = re.search(r"data-pci-linked>.*?</ul>", raw, re.S).group(0)
    unassigned = re.search(r"data-pci-unassigned>.*?</ul>", raw, re.S).group(0)
    assert "Mounting kit" in unassigned and "Mounting kit" not in linked
    rows = re.findall(r"<li class=\"item\" data-pci-component>(.*?)</li>", linked, re.S)
    parts = [[_html.unescape(p) for p in re.findall(r"data-pci-component-part>([^<]*)<", row)] for row in rows]
    assert parts == [[subs[MECH].display_name, subs[ELEC].display_name], [subs[MECH].display_name]]
    assert _t("UI_PCI_ASSOCIATION_NOTE") in _visible(raw)


def test_w05_empty_component_states_are_distinct(client):
    sid = _two_part(client, ELEC)
    raw = _get(client, sid).get_data(as_text=True)
    assert "data-pci-components-none" in raw and "data-pci-linked" not in raw
    _component(sid, "Relay", "Switches power", (ELEC,), "k1")
    raw = _get(client, sid).get_data(as_text=True)
    assert "data-pci-unassigned-none" in raw and "data-pci-linked-none" not in raw
    assert "data-pci-components-none" not in raw


def test_w06_interfaces_show_preparation_and_dependency_as_recorded(client):
    sid = _two_part(client, MECH)
    subs = _subs(sid)
    raw = _get(client, sid).get_data(as_text=True)
    assert "data-pci-interfaces-none" in raw and "data-pci-declare-link" in raw
    one = _interface(sid, MECH, ELEC, "The motor <drives> the hinge", "i1")
    two = _interface(sid, ELEC, MECH, "A sensor reads the arm", "i2")
    _store().apply_interface_preparation_delta(sid, {
        one.interface_id: {sm.PREPARATION_OPERATING_CONDITIONS: "Indoors, 20 C",
                           sm.PREPARATION_ACCEPTANCE_CRITERION: "Opens in 2 s",
                           sm.PREPARATION_EVIDENCE_NEEDED: "A timed video"},
        two.interface_id: {sm.PREPARATION_OPERATING_CONDITIONS: "Outdoors"}},
        dependency_delta={
            one.interface_id: sm.InterfaceDependency(one.interface_id, sm.DEPENDENCY_ONE_WAY,
                                                     subs[MECH].subsystem_id, subs[ELEC].subsystem_id,
                                                     "Needs power"),
        })
    raw = _get(client, sid).get_data(as_text=True)
    blocks = re.findall(r'<div class="item" data-pci-interface>(.*?)\n  </div>', raw, re.S)
    assert len(blocks) == 2
    first, second = (_visible('<main id="main-content">' + b) for b in blocks)
    assert "The motor <drives> the hinge" in first and "&lt;drives&gt;" in blocks[0]
    assert _t("UI_S15_PREP_ALL") in first and "Opens in 2 s" in first and "A timed video" in first
    assert ("%s %s %s" % (subs[MECH].display_name, _t("UI_S15_DEP_RELIES_ON"), subs[ELEC].display_name)) \
        in re.sub(r"\s+", " ", first) and "Needs power" in first
    assert _t("UI_S15_PREP_PARTIAL") in second and _t("UI_S15_DEP_NOT_DECLARED") in second
    assert second.count(_t("UI_S15_PREP_NOT_RECORDED")) == 2
    assert raw.count("data-pci-not-established") == 2 and "data-pci-prep-link" in raw
    for ifc in (one, two):
        assert ifc.interface_id not in _visible(raw)


def test_w07_recording_presence_follows_saved_answers_only(client):
    sid = _two_part(client, MECH)
    elec = _part(sid, ELEC)
    presence = lambda: re.findall(r'data-pci-presence="([^"]+)"', _get(client, sid).get_data(as_text=True))  # noqa
    assert presence() == ["UI_PQ_FAMILY_NONE", "UI_PQ_FAMILY_NONE"]
    mc = [q for q, _t in _pack_questions(ELEC, MC)]
    _store().apply_part_answer_delta(sid, elec, {mc[0]: "One"})
    assert presence() == ["UI_PQ_FAMILY_SOME", "UI_PQ_FAMILY_NONE"]
    _store().apply_part_answer_delta(sid, elec, {q: "Answer %d" % i for i, q in enumerate(mc)})
    assert presence() == ["UI_PQ_FAMILY_ALL", "UI_PQ_FAMILY_NONE"]
    ba = [q for q, _t in _pack_questions(ELEC, BA)]
    _store().apply_part_answer_delta(sid, elec, {q: "B" for q in ba})
    raw = _get(client, sid).get_data(as_text=True)
    assert re.findall(r'data-pci-presence="([^"]+)"', raw) == ["UI_PQ_FAMILY_ALL", "UI_PQ_FAMILY_ALL"]
    assert "Answer 0" not in raw                                # presence only — no answer text


def test_w08_the_optional_part_has_its_own_role_presence_and_original_page_link(client, part_eligible):
    sid = _three_part_project(client)
    raw = _get(client, sid).get_data(as_text=True)
    assert re.findall(r'data-pci-part-role="([^"]+)"', raw) == [
        "UI_PCI_ROLE_FOCUS", "UI_PCI_ROLE_REQUIRED", "UI_PCI_ROLE_OPTIONAL"]
    links = [_html.unescape(x) for x in re.findall(r'href="([^"]*)" data-pci-questions-link', raw)]
    assert links == ["/session/%s/part-questions?part=%s" % (sid, _part(sid, ELEC)),
                     "/session/%s/part-questions" % sid]
    assert len(re.findall(r'data-pci-presence="', raw)) == 4
    assert _t("UI_S15_IFC_TITLE_3") in _visible(raw)


# ==========================================================================
# 3. Fail closed, authorization and no mutation
# ==========================================================================
def test_f01_an_unreadable_snapshot_shows_the_whole_view_unavailable(client, monkeypatch):
    sid = _two_part(client, MECH)
    _component(sid, "Motor", "Turns", (MECH,), "k1")

    def broken(*a, **k):
        raise sqlite3.OperationalError("disk I/O error")
    monkeypatch.setattr(_store(), "load_parts_components_interactions", broken)
    r = _get(client, sid)
    raw = r.get_data(as_text=True)
    assert r.status_code == 503 and 'data-pci-notice="UI_PCI_UNAVAILABLE"' in raw
    for marker in ("data-pci-parts", "data-pci-components", "data-pci-interfaces", "Motor",
                   "data-pci-components-none", "data-pci-interfaces-none"):
        assert marker not in raw


def test_f02_corrupt_durable_data_shows_the_whole_view_unavailable(client):
    sid = _two_part(client, MECH)
    _component(sid, "Motor", "Turns", (MECH,), "k1")
    _raw("UPDATE project_components SET subsystem_ids = ? WHERE project_id = ?",
         ('["sub-' + "8" * 32 + '"]', sid))
    r = _get(client, sid)
    assert r.status_code == 503 and "data-pci-parts" not in r.get_data(as_text=True)


def test_f03_a_stale_answer_to_a_foreign_question_fails_closed_never_remapped(client):
    sid = _two_part(client, MECH)
    _raw("INSERT INTO subsystem_part_answers (project_id, subsystem_id, question_id, answer_text) "
         "VALUES (?, ?, ?, ?)", (sid, _part(sid, ELEC), "mechanical:MECHANISM_COMPLETENESS:Q1", "x"))
    r = _get(client, sid)
    assert r.status_code == 503 and "data-pci-presence=\"" not in r.get_data(as_text=True)


def test_f04_unreadable_governed_questions_fail_the_whole_view_closed(client, monkeypatch):
    sid = _two_part(client, MECH)
    monkeypatch.setattr(appmod, "get_domain_questions", lambda *a, **k: None)
    r = _get(client, sid)
    assert r.status_code == 503 and "data-pci-parts" not in r.get_data(as_text=True)


def test_f05_another_owner_and_malformed_ids_are_refused(client):
    _login(client, "pci-owner@example.com")
    sid = _two_part(client, MECH)
    _component(sid, "Secret motor", "Turns", (MECH,), "k1")
    from tests.csrf_client import csrf_client
    with csrf_client(appmod.app) as other:
        _login(other, "pci-other@example.com")
        r = other.get(URL % sid)
        assert r.status_code in (302, 403, 404) and "Secret motor" not in r.get_data(as_text=True)
    for bad in ("no-such-session", "x" * 40, "sub-" + "1" * 32):
        r = client.get(URL % bad)
        assert r.status_code in (302, 403, 404) and "data-pci-parts" not in r.get_data(as_text=True)


def test_f06_a_get_writes_nothing(client):
    sid = _two_part(client, MECH)
    _component(sid, "Motor", "Turns", (MECH, ELEC), "k1")
    _interface(sid, MECH, ELEC, "Link", "i1")
    before = _db_dump()
    for lang in ("en", "ar"):
        assert _get(client, sid, lang).status_code == 200
    assert _db_dump() == before


# ==========================================================================
# 4. Boundary: no calculation, no engineering claim, other surfaces unchanged
# ==========================================================================
def test_b01_no_calculation_offer_or_engineering_conclusion(client):
    sid = _two_part(client, MECH)
    _component(sid, "Motor", "Turns", (MECH,), "k1")
    raw = _get(client, sid).get_data(as_text=True)
    for route in CALC_ROUTES:
        assert route not in raw
    for marker in ("data-ss", "deliverable", "<form", "method=\"POST\"", "<input", "<textarea"):
        assert marker not in raw.split('<main id="main-content">', 1)[1]
    text = _visible(raw)
    for key in ("UI_PCI_INTRO", "UI_PCI_BOUNDARY", "UI_PCI_PRESENCE_NOTE", "UI_PCI_ASSOCIATION_NOTE"):
        assert _t(key) in text
        text = text.replace(_t(key), "")                       # the disclosures themselves name what is NOT claimed
    text = text.lower()
    for claim in ("is compatible", "are compatible", "validated.", "verified", "bill of materials:",
                  "recommended", "rating:", "size:"):
        assert claim not in text


def test_b02_report_pdf_and_existing_pages_do_not_carry_the_view(client, monkeypatch):
    sid = _two_part(client, ELEC)
    _component(sid, "Motor", "Turns", (MECH,), "k1")
    for raw in (client.get("/session/%s/deliverable" % sid).get_data(as_text=True),
                _pdf_source(client, sid, monkeypatch),
                client.get("/session/%s/interface-preparation" % sid).get_data(as_text=True),
                client.get("/session/%s/part-questions?part=%s" % (sid, _part(sid, MECH))).get_data(as_text=True)):
        assert "parts-components-interactions" not in raw and _t("UI_PCI_TITLE") not in raw


def test_b03_arabic_page_is_rtl_with_isolated_inventor_text(client):
    sid = _two_part(client, MECH)
    _component(sid, "Motor M-1", "Turns the arm", (MECH, ELEC), "k1")
    raw = _get(client, sid, "ar").get_data(as_text=True)
    assert '<html lang="ar" dir="rtl">' in raw
    text = _visible(raw)
    for key in ("UI_PCI_TITLE", "UI_PCI_INTRO", "UI_PCI_BOUNDARY", "UI_PCI_ASSOCIATION_NOTE",
                "UI_PCI_ROLE_FOCUS", "UI_PCI_ROLE_REQUIRED"):
        assert _t(key, "ar") in text
    assert '<bdi dir="auto" style="font-weight:bold" data-pci-component-name>Motor M-1</bdi>' in raw


def test_b04_every_new_copy_key_is_bilingual():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_PCI_")]
    assert len(keys) == 20
    for key in keys:
        assert ui_text.text(key, "en") and ui_text.text(key, "ar")
        assert ui_text.text(key, "en") != ui_text.text(key, "ar")
