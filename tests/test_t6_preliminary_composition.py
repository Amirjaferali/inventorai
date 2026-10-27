"""T6-PRELIMINARY-COMPOSITION-PROJECTION-01 — Slice 1: the read-only preliminary composition.

Under the activated per-lane authorization (docs/governance/T6_FIRST_LANE_AUTHORIZATION_PRELIMINARY_COMPOSITION.md
§§2–4) and MVP_SCOPE_FREEZE.md Amendment 2, ONE request-local, PRELIMINARY / ADVISORY / NON-BINDING composition
traces each CURRENT declared component through every CURRENT participation the inventor recorded for it to the notes
stored for that exact ``(interface_id, component_id)`` pair. What is pinned:
  * read ONLY through ``load_preliminary_composition`` — ``load_participation_preparations`` extended inside the
    same snapshot by T6-INTERFACE-VERIFICATION-REFERENCE-01 — (once per request) behind the central project
    authorization; joins only by validated identity; current participations and notes from the Stage 15 owner's own
    projections;
  * CURRENT / EARLIER_NOT_RECONFIRMED / NOT_RECORDED per pair, and the whole composition UNAVAILABLE on any defect;
  * no invented relationship; withdrawn components absent; ids only in data attributes;
  * deterministic, read-only, no persistence; EN / AR;
  * the report, PDF, Stage 35 export, Validation Plan and Stage 15 writers are unchanged.
"""
import hashlib
import html as _html
import os
import re
import sqlite3

import pytest

import web.app as appmod
from engine import subsystem_model as sm
from engine.record_store import SqliteRecordStore
from tests.test_component_interface_participation import (  # noqa: F401
    PCI, REPORT, _cmp, _form as _icp_form, _ifc, _post as _icp_post, _project, _raw, _store, _web_project, client)
from tests.test_component_inventory_correct_withdraw import _correct, _withdraw
from tests.test_component_participation_verification_preparation import (
    EVIDENCE, EXPECTED, _forms as _ppv_forms, _page as _prep_page, _post as _ppv_post)
from web import ui_text

T6 = "/session/%s/preliminary-composition"


def _t(key, lang="en"):
    return ui_text.text(key, lang)


def _notes(e=None, v=None):
    return {EXPECTED: e, EVIDENCE: v}


def _shown(e=None, v=None, carried=False):
    return dict(_notes(e, v), carried_over=carried)


def _compose(store, pid):
    return appmod._t6_composition(store.load_preliminary_composition(pid))


def _setup(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "t6.db"))
    pid, subs = _project(store)
    ifc = _ifc(store, pid, subs)
    a = _cmp(store, pid, subs, "Hinge motor", parts=(subs[0].subsystem_id, subs[1].subsystem_id))
    b = _cmp(store, pid, subs, "Battery pack")
    return store, pid, subs, ifc, a, b


def _items(raw):
    """``[(component_id, name, [(interface_id, status, {field: text})])]`` from a rendered page."""
    out = []
    for block in re.findall(r'<div class="block" data-t6-component .*?(?=<div class="block" data-t6-component |'
                            r'<p class="meta" style="margin:10px 0 0 0" data-t6-withdrawn-note)', raw, re.S):
        cid = re.search(r'data-t6-component-id="([^"]+)"', block).group(1)
        name = _html.unescape(re.search(r"data-t6-component-name>(.*?)</bdi>", block, re.S).group(1))
        links = []
        for link in re.findall(r'<div class="link" data-t6-link .*?</div>\s*(?=<div class="link"|$|\s*</div>)',
                               block + "</div>", re.S):
            iid = re.search(r'data-t6-interface-id="([^"]+)"', link).group(1)
            status = re.search(r'data-t6-status="([^"]+)"', link).group(1)
            notes = {f: _html.unescape(t) for f, t in
                     re.findall(r'data-t6-note="([^"]+)">(.*?)</bdi>', link, re.S)}
            links.append((iid, status, notes))
        out.append((cid, name, links))
    return out


# ==========================================================================
# 1. The composition (pure, over the owner's validated snapshot)
# ==========================================================================
def test_c01_traces_component_participation_and_the_exact_pair_notes(tmp_path):
    store, pid, subs, ifc, a, b = _setup(tmp_path)
    store.set_interface_participation(pid, ifc, (a,), ())
    store.set_participation_preparation(pid, ifc, a, _notes("Hinge opens in 2 s", "Stopwatch"), _shown())
    view = _compose(store, pid)
    first, second = view["components"]
    assert (first["component_id"], first["name"], first["function"]) == (a, "Hinge motor", "Does Hinge motor")
    assert first["part_ids"] == [subs[0].subsystem_id, subs[1].subsystem_id]
    assert (first["provenance"], first["validation_state"]) == ("OWNER_STATED", "UNVALIDATED")
    [link] = first["links"]
    assert (link["interface_id"], link["interaction"], link["status"]) == (
        ifc, "Motor turns the hinge", appmod.T6_STATUS_CURRENT)
    assert link["notes"] == [{"field": EXPECTED, "text": "Hinge opens in 2 s"},
                             {"field": EVIDENCE, "text": "Stopwatch"}]
    assert second["component_id"] == b and second["links"] == []      # no participation: none invented


def test_c02_not_recorded_earlier_and_never_current_for_carried_notes(tmp_path):
    store, pid, _subs, ifc, a, _b = _setup(tmp_path)
    store.set_interface_participation(pid, ifc, (a,), ())
    assert _compose(store, pid)["components"][0]["links"][0]["status"] == appmod.T6_STATUS_NOT_RECORDED
    store.set_participation_preparation(pid, ifc, a, _notes("Opens"), _shown())
    store.set_interface_participation(pid, ifc, (), (a,))                # removed: notes kept, hidden
    assert _compose(store, pid)["components"][0]["links"] == []
    store.set_interface_participation(pid, ifc, (a,), ())                # added back: earlier notes
    [link] = _compose(store, pid)["components"][0]["links"]
    assert link["status"] == appmod.T6_STATUS_EARLIER and link["notes"][0]["text"] == "Opens"
    store.set_participation_preparation(pid, ifc, a, _notes("Opens"), _shown("Opens", carried=True))
    assert _compose(store, pid)["components"][0]["links"][0]["status"] == appmod.T6_STATUS_CURRENT


def test_c03_withdrawn_and_corrected_components(tmp_path):
    store, pid, _subs, ifc, a, b = _setup(tmp_path)
    store.set_interface_participation(pid, ifc, (a, b), ())
    store.set_participation_preparation(pid, ifc, b, _notes("Powers it"), _shown())
    _correct(store, pid, a, 0, name="Hinge motor v2")
    view = _compose(store, pid)
    assert view["components"][0]["component_id"] == a and view["components"][0]["name"] == "Hinge motor v2"
    _withdraw(store, pid, b, 0)
    view = _compose(store, pid)
    assert [c["component_id"] for c in view["components"]] == [a]      # withdrawn: gone, notes not shown
    assert "Powers it" not in repr(view)


def test_c04_deterministic_and_read_only(tmp_path):
    store, pid, _subs, ifc, a, _b = _setup(tmp_path)
    store.set_interface_participation(pid, ifc, (a,), ())
    store.set_participation_preparation(pid, ifc, a, _notes("x"), _shown())
    path = str(tmp_path / "t6.db")

    def digest():
        conn = sqlite3.connect(path)
        try:
            return hashlib.sha256("\n".join(conn.iterdump()).encode()).hexdigest()
        finally:
            conn.close()
    before = digest()
    assert _compose(store, pid) == _compose(store, pid)
    assert digest() == before


def test_c05_an_inconsistent_snapshot_raises_rather_than_inventing(tmp_path):
    store, pid, _subs, ifc, a, _b = _setup(tmp_path)
    store.set_interface_participation(pid, ifc, (a,), ())
    record = dict(store.load_preliminary_composition(pid))
    record["interfaces"] = ()                                           # participation names a missing interaction
    with pytest.raises(ValueError):
        appmod._t6_composition(record)


# ==========================================================================
# 2. The page
# ==========================================================================
def _traced_project(c):
    sid = _web_project(c)
    form = _icp_form(c, sid)
    ids = [i for i, _c in form["options"]]
    _icp_post(c, sid, form, ids[:1])
    _ppv_post(c, sid, _ppv_forms(_prep_page(c, sid))[0], "Hinge opens in 2 s", "Stopwatch")
    return sid, ids


def test_w01_the_inventor_traces_one_component_to_its_exact_pair_notes(client):
    sid, ids = _traced_project(client)
    pci = client.get(PCI % sid).get_data(as_text=True)
    assert "data-t6-link-entry" in pci and T6 % sid in pci             # the one entry point
    r = client.get(T6 % sid)
    raw = r.get_data(as_text=True)
    assert r.status_code == 200 and r.headers["Cache-Control"] == "no-store"
    items = _items(raw)
    assert [cid for cid, _n, _l in items] == ids                       # every current component, in order
    first = items[0]
    [(iid, status, notes)] = first[2]
    assert status == appmod.T6_STATUS_CURRENT
    assert notes == {EXPECTED: "Hinge opens in 2 s", EVIDENCE: "Stopwatch"}
    assert f'data-t6-pair="{iid} {ids[0]}"' in raw
    assert all(links == [] for _c, _n, links in items[1:])             # never invented
    text = _html.unescape(raw)
    for key in ("UI_T6_TITLE", "UI_T6_PRELIMINARY", "UI_T6_BOUNDARY", "UI_T6_PROVENANCE", "UI_T6_STATUS_CURRENT",
                "UI_T6_NO_PARTICIPATION", "UI_T6_WITHDRAWN_NOTE"):
        assert _t(key) in text, key
    visible = re.sub(r"<[^>]+>", " ", raw)
    assert ids[0] not in visible and iid not in visible                # ids in data attributes only
    composition = raw[raw.index("data-t6-composition"):raw.index("data-t6-withdrawn-note")]
    assert "<form" not in composition and "<input" not in composition and "<textarea" not in composition


def test_w02_earlier_and_not_recorded_states_on_the_page(client):
    sid, ids = _traced_project(client)
    form = _icp_form(client, sid)
    _icp_post(client, sid, form, ())                                    # removed
    _icp_post(client, sid, _icp_form(client, sid), ids[:2])             # first added back + second added
    items = _items(client.get(T6 % sid).get_data(as_text=True))
    assert items[0][2][0][1] == appmod.T6_STATUS_EARLIER and items[0][2][0][2][EXPECTED] == "Hinge opens in 2 s"
    assert items[1][2][0][1] == appmod.T6_STATUS_NOT_RECORDED and items[1][2][0][2] == {}
    text = _html.unescape(client.get(T6 % sid).get_data(as_text=True))
    assert _t("UI_T6_STATUS_EARLIER") in text and _t("UI_T6_STATUS_NOT_RECORDED") in text


def test_w03_a_withdrawn_component_never_appears_with_its_notes(client):
    sid, ids = _traced_project(client)
    _withdraw(_store(), sid, ids[0], 0)
    raw = client.get(T6 % sid).get_data(as_text=True)
    assert ids[0] not in raw and "Hinge opens in 2 s" not in raw
    assert [cid for cid, _n, _l in _items(raw)] == ids[1:]


def test_w04_unreadable_or_corrupt_records_show_nothing_but_unavailable(client):
    sid, _ids = _traced_project(client)
    form = _ppv_forms(_prep_page(client, sid))[0]
    _raw("INSERT INTO subsystem_participation_preparations VALUES (?, ?, ?, ?, ?, ?)",
         (sid, form["interface"], "cmp-" + "9" * 32, "orphan", None, 0), fk=False)
    r = client.get(T6 % sid)
    raw = r.get_data(as_text=True)
    assert r.status_code == 503 and "data-t6-composition" not in raw
    assert _t("UI_T6_UNAVAILABLE") in _html.unescape(raw) and "Hinge opens" not in raw


def test_w05_a_store_failure_is_unavailable_not_empty(client, monkeypatch):
    sid, _ids = _traced_project(client)

    def boom(_sid):
        raise sqlite3.OperationalError("injected")
    monkeypatch.setattr(_store(), "load_preliminary_composition", boom)
    r = client.get(T6 % sid)
    assert r.status_code == 503 and "data-t6-no-components" not in r.get_data(as_text=True)


def test_w06_the_reader_is_called_once_per_request(client, monkeypatch):
    sid, _ids = _traced_project(client)
    store = _store()
    real, calls = store.load_preliminary_composition, []

    def counted(pid):
        calls.append(pid)
        return real(pid)
    monkeypatch.setattr(store, "load_preliminary_composition", counted)
    assert client.get(T6 % sid).status_code == 200 and calls == [sid]


def test_w07_authorization_and_project_isolation(client):
    from tests.test_commercial_evidence_capture import _client_for
    owner, _aid = _client_for("t6-owner@example.com")
    sid, _ids = _traced_project(owner)
    other, _oids = _traced_project(owner)
    intruder, _bid = _client_for("t6-intruder@example.com")
    r = intruder.get(T6 % sid)
    assert r.status_code in (302, 403, 404) and "Hinge opens" not in r.get_data(as_text=True)
    anonymous = appmod.app.test_client()
    r = anonymous.get(T6 % sid)
    assert r.status_code in (302, 403, 404) and "Hinge opens" not in r.get_data(as_text=True)
    mine = {cid for cid, _n, _l in _items(owner.get(T6 % sid).get_data(as_text=True))}
    theirs = {cid for cid, _n, _l in _items(owner.get(T6 % other).get_data(as_text=True))}
    assert mine and theirs and not mine & theirs


def test_w08_a_project_without_interactions_states_it_and_invents_nothing(client):
    from tests.test_component_inventory_declare_list import _declare as _declare_component
    from tests.test_safe_question_routing_pf_q2 import _start
    sid = _start(client)
    _declare_component(client, sid, name="Spring", function="Holds the latch")
    raw = client.get(T6 % sid).get_data(as_text=True)
    assert "data-t6-no-interactions" in raw and "data-t6-no-participation" in raw
    assert "data-t6-link " not in raw


def test_w09_read_only_route_and_unchanged_reports_exports_and_writers(client):
    sid, _ids = _traced_project(client)
    assert client.post(T6 % sid).status_code == 405                     # GET only
    stamp = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?")
    before = stamp.sub("", client.get(REPORT % sid).get_data(as_text=True))
    client.get(T6 % sid)
    assert stamp.sub("", client.get(REPORT % sid).get_data(as_text=True)) == before
    for template in ("deliverable.html", "session.html"):
        source = open(os.path.join(appmod.app.root_path, "templates", template), encoding="utf-8").read()
        assert "data-t6" not in source and "preliminary_composition" not in source, template
    import engine.disclosure_export as export
    assert "preliminary_composition" not in open(export.__file__, encoding="utf-8").read()
    src = open(appmod.__file__, encoding="utf-8").read()
    section = src[src.index("# --- T6-PRELIMINARY-COMPOSITION-PROJECTION-01"):
                  src.index('@app.route("/session/<sid>/interface-observation", methods=["POST"])')]
    code = "\n".join(line.split("#", 1)[0] for line in section.splitlines())
    code = re.sub(r'"""[\s\S]*?"""', "", code)                           # docstrings state the exclusions
    for banned in ("append_", "set_", "_write", "INSERT", "DELETE", "derive_", "run_iteration", "safety_signal",
                   "load_parts_components_interactions", "load_component_inventory", "bom", "quantit"):
        assert banned not in code.lower() if banned.islower() else banned not in code, banned


def test_w10_arabic_page_and_copy(client):
    sid, _ids = _traced_project(client)
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    raw = client.get(T6 % sid).get_data(as_text=True)
    text = _html.unescape(raw)
    assert 'dir="rtl"' in raw
    for key in ("UI_T6_TITLE", "UI_T6_PRELIMINARY", "UI_T6_BOUNDARY", "UI_T6_STATUS_CURRENT", "UI_T6_EXPECTED"):
        assert _t(key, "ar") in text, key
    assert re.search(r'<bdi dir="auto" data-t6-note="expected_contribution">Hinge opens in 2 s</bdi>', raw)
    keys = [k for k in ui_text.__dict__.get("UI_STRINGS", {}) if k.startswith("UI_T6_")] or [
        "UI_T6_TITLE", "UI_T6_LINK", "UI_T6_PRELIMINARY", "UI_T6_INTRO", "UI_T6_BOUNDARY", "UI_T6_STATUS_CURRENT",
        "UI_T6_STATUS_EARLIER", "UI_T6_STATUS_NOT_RECORDED", "UI_T6_UNAVAILABLE", "UI_T6_NO_PARTICIPATION"]
    for key in keys:
        assert _t(key, "en") and _t(key, "ar") and _t(key, "en") != _t(key, "ar"), key
    lowered = " ".join(_t(k) for k in keys).lower()
    for claim in ("specialist review", "expert review", "it is compatible", "it is verified", "has been verified",
                  "it is safe", "it is ready to build"):
        assert claim not in lowered, claim
