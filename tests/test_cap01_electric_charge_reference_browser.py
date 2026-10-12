"""Real Chromium + the existing Flask server: ELECTRICAL-CHARGE-AMPERE-HOUR-REFERENCE-01
(EN and AR).

Synthetic invention data only. An Electronics project is started through the real
forms; its canonical PHYSICAL_FEASIBILITY gap is set current in-process (as the
unit harness does), and the report then shows the basic electrical and energy-time
reference groups and THEN the electric-charge group, with three LTR-isolated
equations kept on one line, each note on its own line, its attribution and its
limitations. At phone width there is no horizontal overflow; in Arabic the page is RTL.
"""
import pytest
from playwright.sync_api import expect

import web.app as webapp
from engine.idea_state import OPEN, PHYSICAL_FEASIBILITY
from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap01_mechanical_open_gap_context import _gaps
from tests.test_cap01_electrical_energy_time_reference_browser import _start_electronics
from tests.cap01_charge_addition import CHARGE_EQUATIONS

CH = "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_CHARGE_FUNDAMENTALS_"


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_charge_group_renders_third_and_fits_phone_width(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    webapp.SESSION_STORE[sid]["state"].gaps = _gaps((PHYSICAL_FEASIBILITY, OPEN))

    page.goto(f"{server}/session/{sid}/deliverable")
    groups = page.locator("[data-cap01-fundamentals]")
    expect(groups).to_have_count(3)
    assert [groups.nth(i).get_attribute("data-cap01-fundamentals") for i in range(3)] == [
        "basic-electrical-reference-v1", "electrical-energy-time-reference-v1", "electric-charge-reference-v1"]
    group = groups.nth(2)
    expect(group).to_be_visible()
    expect(group.locator("[data-cap01-fund-title]")).to_have_text(text(CH + "TITLE", lang))
    equations = group.locator("[data-cap01-fund-equation]")
    expect(equations).to_have_count(3)
    for i, equation in enumerate(CHARGE_EQUATIONS):
        expect(equations.nth(i)).to_have_text(equation)
        assert equations.nth(i).get_attribute("dir") == "ltr"
    for part in ("INTRO", "ITEM_1_LEAD", "ITEM_1_NOTE", "ITEM_2_LEAD", "ITEM_2_NOTE", "ITEM_3_LEAD",
                 "ITEM_3_NOTE"):
        expect(group).to_contain_text(text(CH + part, lang))
    expect(group.locator("[data-cap01-fund-source]")).to_have_text(text(CH + "SOURCE", lang))
    expect(group.locator("[data-cap01-fund-boundary]")).to_have_text(text(CH + "BOUNDARY", lang))
    assert group.locator("a, button, form, input, select, textarea").count() == 0

    # each note starts below its equation, and each equation stays on one line, at
    # desktop and phone width
    for width in (1280, 390):
        page.set_viewport_size({"width": width, "height": 900})
        for i in range(3):
            item = group.locator("[data-cap01-fund-claim]").nth(i)
            eq = item.locator("[data-cap01-fund-equation]")
            note = item.locator("[data-cap01-fund-item-note]")
            assert note.evaluate("e => getComputedStyle(e).display") == "block"
            assert eq.evaluate("e => getComputedStyle(e).whiteSpace") == "nowrap"
            eq_box, note_box = eq.bounding_box(), note.bounding_box()
            assert note_box["y"] >= eq_box["y"] + eq_box["height"] - 1, (width, i)
            assert eq.evaluate("e => e.getClientRects().length") == 1, (width, i)

    # layout: coherent at phone width, no horizontal overflow; RTL on Arabic
    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert group.bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
