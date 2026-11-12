# -*- coding: utf-8 -*-
"""G1-SINGLE-DOMAIN-ENGINEERING-CONTINUATION-01 — a valid single-domain Mechanical project whose
Compass rests on routed recovery or on a suppressed question is offered ONE optional secondary
step through the SAME template rule as the integrated continuation:
  Step A — while no current component exists: the existing component declaration form;
  Step B — once a current component exists: the existing planar-moment page.

Synthetic data only. What is pinned:
  * the existing primary action is unchanged and stays the ONLY primary action; at most ONE
    secondary link, never both steps; Step A becomes Step B after a real declaration;
  * Step A's form is reachable: the collapsed inventory panel renders open only while Step A is
    offered;
  * no link while an ordinary governed question is served, on an Electrical / Electronics or
    integrated project, or when the inventory, the moment gate or the declaration form is
    unavailable; integrated guidance keeps precedence;
  * rendering and following the link change nothing (no gap, maturity, routing, record or R2 effect);
  * the inventor can go from the blocked point to a declared component, the moment page, a saved
    configuration of their own and the existing report / PDF;
  * EN / AR boundary copy; the Arabic page is RTL.
"""
import html as _html
import re

import pytest

import web.app as appmod
from engine import need_routing as nr
from engine import progression_loop as pl
from engine.idea_state import PHYSICAL_FEASIBILITY as PF
from engine.progression_loop import compute_non_answer_suppression
from tests.test_component_inventory_declare_list import _declare
from tests.test_g1_integrated_engineering_continuation import _answer, _raw, client  # noqa: F401
from tests.test_g1_planar_moment_saved_declaration import _evaluate, _save, _save_form, URL
from tests.test_g1_routed_recovery_continuation import (
    LINK_RE as RRC_LINK_RE, _integrated as _routed_integrated, _snapshot, _to_routed_recovery)
from tests.test_g1_uqtr_integrated_continuation import UQC_LINK_RE, _deliverable, _post
from tests.test_safe_question_routing_pf_q2 import (
    BA_1, BA_2, ELEC_SEED, MECH as MECH_ANSWER, MECH_2 as MECH_ANSWER_2, _start)
from tests.test_safe_question_routing_pf_q2_weak_recovery import WEAK
from tests.test_stage15_integrated_invention_entry import _live, _pdf_source
from web import ui_text

PRIMARY_RE = re.compile(r'<a class="journey-primary" data-primary-action[^>]*href="([^"]*)"')
INVENTORY_RE = re.compile(r'<details id="component-inventory"[^>]*>')
NEW_KEYS = ("UI_SDC_NOTE_COMPONENTS", "UI_SDC_NOTE_MOMENT")


def _routed(c, lang=None):
    """A single-domain Mechanical project: Mechanism and Boundary answered in the inventor's own
    words and ONE non-substantive Physical Feasibility answer, so the routed point waits."""
    sid = _start(c, lang=lang or "en")
    for value in (MECH_ANSWER, MECH_ANSWER_2, WEAK, BA_1, BA_2):
        _answer(c, sid, value)
    state = _live(sid)
    assert state.get_gap(PF).status == "OPEN" and nr.gap_has_outstanding_routing(state, PF)
    return sid


def _suppressed(c, seed=None, domain="mechanical"):
    sid = _start(c, **({"seed": seed, "domain": domain} if seed else {}))
    assert _post(c, sid, action="specialist_requested", response="").status_code == 302
    assert compute_non_answer_suppression(_live(sid)) is not None
    return sid


def _primaries(page):
    return [_html.unescape(h) for h in PRIMARY_RE.findall(page)]


def _rrc(page):
    return [(k, _html.unescape(h)) for k, h in RRC_LINK_RE.findall(page)]


def _uqc(page):
    return [(k, _html.unescape(h)) for k, h in UQC_LINK_RE.findall(page)]


def _inventory_open(page):
    m = INVENTORY_RE.search(page)
    assert m, "the inventory section must be on the page"
    return " open" in m.group(0)


def _note(page, prefix):
    m = re.search(r'<p[^>]*data-%s-note>(.*?)</p>' % prefix, page, re.S)
    return _html.unescape(m.group(1)) if m else None


# ==========================================================================
# 1. routed recovery: Step A, then Step B
# ==========================================================================
def test_01_routed_recovery_offers_the_component_step_beside_its_unchanged_primary(client):
    sid = _routed(client)
    page = _raw(client, sid)
    assert _primaries(page) == ["#routed-recovery"]
    assert _rrc(page) == [("component_inventory", "#component_name")]
    assert 'data-rrc-scope="single"' in page
    assert _note(page, "rrc") == ui_text.text("UI_SDC_NOTE_COMPONENTS", "en")
    assert 'id="component_name"' in page and _inventory_open(page)      # the form is reachable
    assert "data-uqc" not in page


def test_02_after_a_declaration_the_step_becomes_the_moment_page_and_never_both(client):
    sid = _routed(client)
    assert _declare(client, sid, name="Long door handle",
                    function="Lever the user pushes down").status_code == 302
    _raw(client, sid)                                       # consumes the one-time acknowledgement
    page = _raw(client, sid)
    assert _primaries(page) == ["#routed-recovery"]
    assert _rrc(page) == [("planar_moment", URL % sid)]
    assert _note(page, "rrc") == ui_text.text("UI_SDC_NOTE_MOMENT", "en")
    assert not _inventory_open(page)                        # Step A no longer opens the panel
    assert page.count("data-rrc-link") == 1 and "data-uqc" not in page


def test_03_rendering_and_following_the_steps_change_nothing(client):
    sid = _routed(client)
    before = _snapshot(sid)
    _raw(client, sid)
    _raw(client, sid)
    assert _snapshot(sid) == before
    state = _live(sid)
    assert state.get_gap(PF).status == "OPEN" and nr.gap_has_outstanding_routing(state, PF)
    assert not pl.substantive_attempt_recorded(state, PF)
    assert client.get(URL % sid).status_code == 200
    assert _snapshot(sid) == before


# ==========================================================================
# 2. UQTR suppression: Step A, then Step B
# ==========================================================================
def test_04_a_suppressed_question_offers_the_same_steps(client):
    sid = _suppressed(client)
    page = _raw(client, sid)
    assert _primaries(page) == [_deliverable(sid)]
    assert _uqc(page) == [("component_inventory", "#component_name")]
    assert 'data-uqc-scope="single"' in page and _inventory_open(page)
    assert _declare(client, sid).status_code == 302
    _raw(client, sid)
    page = _raw(client, sid)
    assert _primaries(page) == [_deliverable(sid)]
    assert _uqc(page) == [("planar_moment", URL % sid)] and "data-rrc" not in page


# ==========================================================================
# 3. exclusions and precedence
# ==========================================================================
def test_05_no_step_while_an_ordinary_question_is_served(client):
    sid = _start(client)
    assert _declare(client, sid).status_code == 302
    for _ in range(2):
        page = _raw(client, sid)
    assert _primaries(page) == ["#response"]
    assert "data-rrc" not in page and "data-uqc" not in page
    assert not _inventory_open(page)


def test_06_an_electrical_project_gets_no_step(client):
    sid = _suppressed(client, seed=ELEC_SEED, domain="electronics_electrical")
    page = _raw(client, sid)
    assert _primaries(page) == [_deliverable(sid)]
    assert "data-uqc" not in page and not _inventory_open(page)


def test_07_an_integrated_project_keeps_its_own_step_and_precedence(client):
    sid = _routed_integrated(client)
    _to_routed_recovery(client, sid)
    page = _raw(client, sid)
    assert _rrc(page) == [("part_questions", _rrc(page)[0][1])]
    assert "data-rrc-scope" not in page
    assert appmod._single_domain_continuation(
        sid, appmod._component_inventory_context(sid, {})) is None


def test_08_an_unreadable_inventory_offers_nothing(client, monkeypatch):
    sid = _routed(client)

    def boom(_pid):
        raise RuntimeError("synthetic")
    monkeypatch.setattr(appmod._get_store(), "load_component_inventory_record", boom)
    page = _raw(client, sid)
    assert _primaries(page) == ["#routed-recovery"] and "data-rrc" not in page


def test_09_a_full_inventory_with_no_current_component_offers_nothing(client, monkeypatch):
    sid = _routed(client)
    monkeypatch.setattr(appmod._subsystem_model, "MAX_DECLARED_COMPONENTS_PER_PROJECT", 0)
    page = _raw(client, sid)
    assert 'id="component_name"' not in page and "data-rrc" not in page
    assert not _inventory_open(page)


@pytest.mark.parametrize("declared", [False, True])
def test_10_a_closed_moment_gate_offers_nothing(client, monkeypatch, declared):
    sid = _routed(client)
    if declared:
        assert _declare(client, sid).status_code == 302
        _raw(client, sid)
    monkeypatch.setattr(appmod, "_calc_gate", lambda *_a, **_k: (False, None))
    page = _raw(client, sid)
    assert _primaries(page) == ["#routed-recovery"] and "data-rrc" not in page


def test_11_a_declared_part_never_qualifies_the_single_domain_step(client, monkeypatch):
    sid = _routed(client)
    monkeypatch.setattr(appmod, "_calc_gate", lambda *_a, **_k: (True, object()))
    assert "data-rrc" not in _raw(client, sid)


def test_12_the_helper_fails_closed_on_every_unusable_inventory():
    for ci in (None, {}, {"status": "unavailable"},
               {"status": "available", "has_parts": True, "components": [], "can_add": True},
               {"status": "available", "has_parts": False, "components": [], "can_add": False}):
        assert appmod._single_domain_continuation("no-such-project", ci) is None


# ==========================================================================
# 4. the connected journey, copy and language
# ==========================================================================
def test_13_blocked_point_to_component_to_saved_moment_to_report_and_pdf(client, monkeypatch):
    sid = _routed(client)
    page = _raw(client, sid)
    assert _rrc(page) == [("component_inventory", "#component_name")]
    assert _declare(client, sid, name="Long door handle",
                    function="Lever the user pushes down").status_code == 302
    _raw(client, sid)
    page = _raw(client, sid)
    assert _rrc(page) == [("planar_moment", URL % sid)]
    raw = _evaluate(client, sid, F="20", d_perp="120")
    hidden, options = _save_form(raw)
    assert len(options) == 1 and not re.search(r'<option value="cmp[^"]*" selected', raw)
    assert _save(client, sid, raw, target=options[0]).status_code == 200
    report = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    pdf = _pdf_source(client, sid, monkeypatch)
    for doc in (report, pdf):
        section = re.search(r'<section class="saved-moments-report".*?</section>', doc, re.S)
        assert section and "2400.0 N·mm" in section.group(0)
        assert "Long door handle" in _html.unescape(section.group(0))
    state = _live(sid)
    assert state.get_gap(PF).status == "OPEN" and nr.gap_has_outstanding_routing(state, PF)


def test_14_copy_is_bilingual_and_states_the_boundary():
    for key in NEW_KEYS:
        assert ui_text.has_string(key)
        en, ar = ui_text.text(key, "en"), ui_text.text(key, "ar")
        assert en.startswith("Optional") and ar.startswith("اختياري")
        assert "does not answer" in en
    moment = ui_text.text("UI_SDC_NOTE_MOMENT", "en")
    for phrase in ("does not mean your project needs this calculation", "carries such a force",
                   "You enter every value"):
        assert phrase in moment


def test_15_arabic_page_is_rtl_with_the_arabic_step(client):
    sid = _routed(client, lang="ar")
    page = _raw(client, sid)
    assert re.search(r'<html[^>]*dir="rtl"', page)
    assert _note(page, "rrc") == ui_text.text("UI_SDC_NOTE_COMPONENTS", "ar")
    link = re.search(r'<a data-rrc-link[^>]*>([^<]*)</a>', page).group(1)
    assert _html.unescape(link) == ui_text.text("UI_IJG_COMPONENTS_CTA", "ar")
