# -*- coding: utf-8 -*-
"""G1-INTEGRATED-ENGINEERING-CONTINUATION-01 — after an inventor explicitly creates an integrated
invention, the EXISTING Project Compass guides them, one optional step at a time, to the next existing
engineering declaration and, once the existing gate admits it, to the existing planar clearance check.

Synthetic English invention (a control board inside a plastic enclosure), with Arabic rendering guards.
What is pinned:
  * the connected route: declared parts -> interaction declaration -> Component Inventory ->
    participation -> (preparation, unchanged) with an optional, SECONDARY clearance link -> the existing
    clearance page -> a bounded result -> the existing DXF download;
  * an unknown dimension stays MISSING_INFORMATION with no DXF; no declaration stays NONE;
  * exactly one primary action, the handoff one click away, the clearance link never primary and never
    a claim that the check applies;
  * negative controls: single-domain projects, another project's components, withdrawn components,
    an unreadable or disagreeing snapshot and an already-declared clearance give no link; declarations
    stay OWNER_STATED / UNVALIDATED; no maturity, gap, readiness or answer change; question serving keeps
    priority; a page view writes nothing.
"""
import html as _html
import os
import pickle
import re
import sqlite3

import pytest

import web.app as appmod
from engine import mechanical_planar_clearance as pcc
from tests.test_stage15_integrated_invention_entry import ELEC, MECH, _compose, _created, _live
from tests.test_stage28_control_loop_optional_part_slice1 import client  # noqa: F401  (fixture)
from tests.test_28t5_nonfocused_required_part_questions import _ids, _part, _save as _save_part
from tests.test_stage15_subsystem_interface_declaration import _declare as _declare_interface
from tests.test_component_inventory_declare_list import _declare as _declare_component
from tests.test_component_inventory_correct_withdraw import _form_for, _post_withdraw
from tests.test_component_interface_participation import _form as _icp_form, _post as _icp_post
from tests.test_board_enclosure_planar_clearance import _page as _pcc_page, _save as _pcc_save
from tests.test_safe_question_routing_pf_q2 import MECH as MECH_ANSWER, PF_STRONG, BA_1, BA_2, _start
from web import planar_clearance as view_mod
from web import ui_text

IDEA = ("I want to develop a small electronic device with a circuit board inside an enclosure. I want "
        "the board to fit with enough clearance, but I have not decided the components or dimensions yet.")
PARTS = {"mech_part_name": "Plastic enclosure", "mech_part_function": "Holds and protects the board",
         "elec_part_name": "Control board", "elec_part_function": "Reads the sensor and lights the LED"}
NEW_KEYS = ("UI_IJG_DECLARE_NOTE", "UI_IJG_DECLARE_CTA", "UI_IJG_COMPONENTS_NOTE",
            "UI_IJG_COMPONENTS_CTA", "UI_IJG_PARTICIPATION_NOTE", "UI_IJG_PARTICIPATION_CTA",
            "UI_IJG_CLEARANCE_NOTE", "UI_IJG_CLEARANCE_LINK")


def _raw(c, sid):
    r = c.get(f"/session/{sid}")
    assert r.status_code == 200, r.status_code
    return r.get_data(as_text=True)


def _primary(page):
    found = re.findall(r'<(?:a|button) class="journey-primary" data-primary-action[^>]*>', page)
    assert len(found) == 1, found
    return found[0]


def _kind(page):
    m = re.search(r'data-ijg-action="([^"]+)"', _primary(page))
    return m.group(1) if m else None


def _links(page):
    return re.findall(r'<a data-ijg-clearance-link href="([^"]+)"', page)


def _answer(c, sid, text):
    raw = _raw(c, sid)
    token = re.search(r'name="answer_token" value="([^"]*)"', raw).group(1)
    assert c.post(f"/session/{sid}", data={"response": text, "answer_token": token}).status_code == 302


def _dump():
    with sqlite3.connect(os.environ["INVENTORAI_DB_PATH"]) as connection:
        return list(connection.iterdump())


def _project(c, lang=None):
    """The integrated invention with its focus questioning and other-part questions done."""
    sid = _created(_compose(c, IDEA, focus=MECH, lang=lang, **PARTS))
    for value in (MECH_ANSWER, MECH_ANSWER, PF_STRONG, BA_1, BA_2):
        _answer(c, sid, value)
    r = _save_part(c, sid, _part(sid, ELEC), {q: "My own words about it." for q in _ids(ELEC)})
    assert r.status_code == 200
    return sid


def _to_participation(c, sid):
    assert _declare_interface(c, sid, "The control board sits inside the plastic enclosure.").status_code == 302
    for name, function in (("Control board", "Carries the circuit"),
                           ("Plastic enclosure", "Surrounds the board")):
        assert _declare_component(c, sid, name=name, function=function).status_code in (200, 302)


def _participate(c, sid):
    form = _icp_form(c, sid)
    ids = [o[0] for o in form["options"]]
    assert _icp_post(c, sid, form, ids).status_code in (200, 302)
    return ids


def _ifc(sid):
    return appmod._get_store().load_planar_clearance(sid)["interfaces"][0].interface_id


def _evidence(sid):
    state = _live(sid)
    return (state.maturity_level, [(g.gap_type, g.status) for g in state.gaps], len(state.assertions))


# ==========================================================================
# 1. the connected route, end to end (English)
# ==========================================================================
def test_e01_the_route_reaches_the_clearance_check_and_its_dxf(client):
    sid = _project(client)
    before = _evidence(sid)
    page = _raw(client, sid)
    assert _kind(page) == "declare_interaction"
    assert 'href="#interface_description"' in _primary(page) and 'id="interface_description"' in page
    assert "data-ijg-handoff" in page and not _links(page)

    assert _declare_interface(client, sid, "The control board sits inside the plastic enclosure.").status_code == 302
    page = _raw(client, sid)
    assert _kind(page) == "component_inventory"
    assert 'href="#component_name"' in _primary(page) and 'id="component_name"' in page
    assert not _links(page)

    assert _declare_component(client, sid, name="Control board", function="Carries the circuit").status_code in (200, 302)
    assert _kind(_raw(client, sid)) == "component_inventory"          # one is not enough for the check
    assert _declare_component(client, sid, name="Plastic enclosure", function="Surrounds the board").status_code in (200, 302)
    page = _raw(client, sid)
    assert _kind(page) == "participation"
    assert f'href="/session/{sid}/interface-preparation#participation-heading"' in _primary(page)
    assert not _links(page)

    ids = _participate(client, sid)
    page = _raw(client, sid)
    assert _kind(page) == "interface_preparation"                       # the unchanged next step
    ifc = _ifc(sid)
    assert _links(page) == [f"/session/{sid}/interface-clearance/{ifc}"]
    block = re.search(r'<div class="journey-note" data-ijg-clearance>.*?</div>', page, re.S).group(0)
    assert "data-primary-action" not in block
    text = _html.unescape(re.sub(r"<[^>]+>", " ", block))
    assert ui_text.text("UI_IJG_CLEARANCE_NOTE", "en") in text
    assert "Plastic enclosure" in text and "Control board" in text

    # the existing clearance page, a bounded result, the existing DXF download
    assert client.get(_links(page)[0]).status_code == 200
    resp = _pcc_save(client, sid, ifc, ids)
    assert resp.status_code in (200, 302)
    view = view_mod.clearance_view(appmod._get_store().load_planar_clearance(sid), ifc, appmod._PCC_BINDING)
    assert view["state"] == view_mod.STATE_CURRENT
    assert view["evaluation"]["outcome"] in (pcc.OUTCOME_MET, pcc.OUTCOME_NOT_MET)
    assert view_mod.cad_eligible(view)
    body = _pcc_page(client, sid, ifc).get_data(as_text=True)
    href = _html.unescape(re.search(r'href="([^"]*cad\.zip[^"]*)"', body).group(1))
    zipped = client.get(href)
    assert zipped.status_code == 200 and zipped.mimetype == "application/zip"
    # once declared, the Compass no longer lists it; the inventor reaches it from the interaction page
    assert not _links(_raw(client, sid))
    # nothing here changed the analysis: no answer, gap, maturity or progression effect
    assert _evidence(sid) == before


def test_e02_an_unknown_dimension_stays_missing_information_with_no_dxf(client):
    sid = _project(client)
    _to_participation(client, sid)
    ids = _participate(client, sid)
    ifc = _ifc(sid)
    none_view = view_mod.clearance_view(appmod._get_store().load_planar_clearance(sid), ifc, appmod._PCC_BINDING)
    assert none_view["state"] == view_mod.STATE_NONE and none_view["evaluation"] is None
    assert _pcc_save(client, sid, ifc, ids, values=("84", "50", "86", "56", ""),
                     unknown=(pcc.VALUE_ROLES[4],)).status_code in (200, 302)
    view = view_mod.clearance_view(appmod._get_store().load_planar_clearance(sid), ifc, appmod._PCC_BINDING)
    assert view["evaluation"]["outcome"] == pcc.OUTCOME_MISSING and not view_mod.cad_eligible(view)
    assert "cad.zip" not in _pcc_page(client, sid, ifc).get_data(as_text=True)


# ==========================================================================
# 2. precedence and the one-primary-action rule
# ==========================================================================
def test_e03_a_waiting_question_keeps_priority_and_no_link_is_shown(client):
    sid = _created(_compose(client, IDEA, focus=MECH, **PARTS))
    page = _raw(client, sid)
    assert 'href="#response"' in _primary(page)
    assert "data-ijg" not in page


def test_e04_the_other_part_questions_still_come_first(client):
    sid = _created(_compose(client, IDEA, focus=MECH, **PARTS))
    for value in (MECH_ANSWER, MECH_ANSWER, PF_STRONG, BA_1, BA_2):
        _answer(client, sid, value)
    assert _kind(_raw(client, sid)) == "part_questions"


def test_e05_single_domain_projects_never_gain_an_integrated_action(client):
    sid = _start(client)
    for value in (MECH_ANSWER, MECH_ANSWER, PF_STRONG, BA_1, BA_2):
        _answer(client, sid, value)
    page = _raw(client, sid)
    assert "data-ijg" not in page
    assert appmod._integrated_journey_guidance(sid, appmod._integrated_scope_context(_live(sid))) is None


# ==========================================================================
# 3. negative controls: no inferred or foreign eligibility
# ==========================================================================
def test_e06_another_projects_components_never_count(client):
    sid = _project(client)
    other = _project(client)
    _to_participation(client, other)
    _participate(client, other)
    assert _declare_interface(client, sid, "The control board sits inside the plastic enclosure.").status_code == 302
    page = _raw(client, sid)
    assert _kind(page) == "component_inventory" and not _links(page)


def test_e07_a_withdrawn_component_removes_the_link(client):
    sid = _project(client)
    _to_participation(client, sid)
    _participate(client, sid)
    assert _links(_raw(client, sid))
    form = _form_for(_raw(client, sid), "withdraw")
    assert _post_withdraw(client, sid, form).status_code in (200, 302)
    page = _raw(client, sid)
    assert _kind(page) == "component_inventory" and not _links(page)


def test_e08_an_unreadable_snapshot_keeps_the_earlier_behaviour(client, monkeypatch):
    sid = _project(client)
    _to_participation(client, sid)
    _participate(client, sid)

    def boom(*_a, **_k):
        raise RuntimeError("unreadable")
    monkeypatch.setattr(type(appmod._get_store()), "load_planar_clearance", boom)
    page = _raw(client, sid)
    assert _kind(page) == "interface_preparation"          # the pre-increment step stands
    assert not _links(page)


def test_e09_a_snapshot_that_disagrees_with_the_live_scope_offers_nothing_new(client):
    sid = _project(client)
    _to_participation(client, sid)
    _participate(client, sid)
    scope = appmod._integrated_scope_context(_live(sid))
    scope["interfaces"][0] = dict(scope["interfaces"][0], description="not the stored one")
    assert appmod._ijg_connection(sid, scope) is None
    assert appmod._integrated_journey_guidance(sid, scope) == {"kind": "interface_preparation", "clearance": []}


def test_e10_declarations_stay_owner_stated_and_a_view_writes_nothing(client):
    sid = _project(client)
    _to_participation(client, sid)
    _participate(client, sid)
    snapshot = appmod._get_store().load_planar_clearance(sid)
    records = (list(snapshot["interfaces"]) + list(snapshot["participations"])
               + list(snapshot["inventory"].active))
    assert records and all((r.provenance, r.validation_state) == ("OWNER_STATED", "UNVALIDATED")
                           for r in records)
    before = (_dump(), pickle.dumps(_live(sid)))
    for _ in range(2):
        _raw(client, sid)
    assert (_dump(), pickle.dumps(_live(sid))) == before


# ==========================================================================
# 4. EN / AR copy
# ==========================================================================
def test_e11_arabic_rendering_of_the_steps_and_the_link(client):
    sid = _project(client, lang="ar")
    page = _raw(client, sid)
    assert 'dir="rtl"' in page[:2000]
    assert ui_text.text("UI_IJG_DECLARE_NOTE", "ar") in _html.unescape(page)
    _to_participation(client, sid)
    assert ui_text.text("UI_IJG_PARTICIPATION_CTA", "ar") in _html.unescape(_raw(client, sid))
    _participate(client, sid)
    page = _html.unescape(_raw(client, sid))
    assert ui_text.text("UI_IJG_CLEARANCE_NOTE", "ar") in page
    assert ui_text.text("UI_IJG_CLEARANCE_LINK", "ar") in page
    assert re.search(r'<bdi dir="auto">Plastic enclosure</bdi>', page)


def test_e12_copy_is_bilingual_optional_and_claims_nothing():
    for key in NEW_KEYS:
        for lang in ("en", "ar"):
            assert ui_text.has_string(key) and ui_text.text(key, lang).strip(), (key, lang)
    for key in ("UI_IJG_DECLARE_NOTE", "UI_IJG_COMPONENTS_NOTE", "UI_IJG_PARTICIPATION_NOTE",
                "UI_IJG_CLEARANCE_NOTE"):
        en = ui_text.text(key, "en").lower()
        assert "optional" in en, key
        for word in ("validated", "verified", "compatible", "safe ", "required", "must ", "guarantee"):
            assert word not in en, (key, word)
        assert "اختيار" in ui_text.text(key, "ar"), key
    assert "does not know whether it applies" in ui_text.text("UI_IJG_CLEARANCE_NOTE", "en")


def test_e13_the_owner_reuses_existing_seams_and_writes_nothing():
    src = open(appmod.__file__, encoding="utf-8").read()
    body = src[src.index("def _ijg_connection"):src.index("def _experiment_planning_guidance")]
    for owner in ("load_planar_clearance", "current_interface_participants", "clearance_view",
                  "STATE_NONE", "load_nonfocused_part_record", "PREPARATION_ALL_RECORDED"):
        assert owner in body, owner
    for forbidden in ("_write", "append_", "save_", "request.", "classify", "ai_advisor"):
        assert forbidden not in body, forbidden
