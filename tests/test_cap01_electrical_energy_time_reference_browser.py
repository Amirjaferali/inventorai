"""Real Chromium + the existing Flask server: ELECTRICAL-ENERGY-TIME-REFERENCE-01
(EN and AR).

Synthetic invention data only. An Electronics project is started through the real
forms; its canonical PHYSICAL_FEASIBILITY gap is set current in-process (as the
unit harness does), and the report then shows the existing basic electrical
reference group FIRST and the energy-time group SECOND, with LTR-isolated
equations, its attribution and its limitations. At phone width there is no
horizontal overflow; in Arabic the page is RTL.
"""
import pytest
from playwright.sync_api import expect

import web.app as webapp
from engine.idea_state import OPEN, PHYSICAL_FEASIBILITY
from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap01_mechanical_open_gap_context import _gaps

ELEC_IDEA = "ESP32 microcontroller circuit with a voltage sensor"
DOMAIN = "electronics_electrical"
ET = "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_ENERGY_TIME_FUNDAMENTALS_"
SUBMIT = "main input[type=submit], main button[type=submit]"


def _start_electronics(page, base, lang):
    page.goto(base + "/")
    if lang == "ar":
        page.get_by_role("button", name="العربية", exact=True).click()
    page.fill("#idea", ELEC_IDEA)
    page.click(SUBMIT)
    page.wait_for_load_state()
    choice = page.locator('input[name=domain_choice][value="%s"]' % DOMAIN)
    if choice.count():
        choice.check()
        page.click(SUBMIT)
        page.wait_for_load_state()
    confirm = page.locator("input[name=domain_confirm]")
    assert confirm.input_value() == DOMAIN
    confirm.check()
    page.click(SUBMIT)
    page.wait_for_load_state()
    return page.url.rsplit("/session/", 1)[1].split("?")[0]


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_energy_time_group_renders_second_and_fits_phone_width(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    webapp.SESSION_STORE[sid]["state"].gaps = _gaps((PHYSICAL_FEASIBILITY, OPEN))

    page.goto(f"{server}/session/{sid}/deliverable")
    groups = page.locator("[data-cap01-fundamentals]")
    expect(groups).to_have_count(2)
    assert groups.nth(0).get_attribute("data-cap01-fundamentals") == "basic-electrical-reference-v1"
    group = groups.nth(1)
    assert group.get_attribute("data-cap01-fundamentals") == "electrical-energy-time-reference-v1"
    expect(group).to_be_visible()
    expect(group.locator("[data-cap01-fund-title]")).to_have_text(text(ET + "TITLE", lang))
    equations = group.locator("[data-cap01-fund-equation]")
    expect(equations).to_have_count(2)
    expect(equations.nth(0)).to_have_text("E = P × t")
    expect(equations.nth(1)).to_have_text("J = W · s")
    assert equations.nth(0).get_attribute("dir") == "ltr"
    for part in ("ITEM_1_LEAD", "ITEM_1_NOTE", "ITEM_2_LEAD", "INTRO"):
        expect(group).to_contain_text(text(ET + part, lang))
    expect(group.locator("[data-cap01-fund-source]")).to_have_text(text(ET + "SOURCE", lang))
    expect(group.locator("[data-cap01-fund-boundary]")).to_have_text(text(ET + "BOUNDARY", lang))
    assert group.locator("a, button, form, input, select, textarea").count() == 0

    # each note starts below its equation, and each equation stays on one line, at
    # desktop and phone width; the original groups keep their inline notes
    base_note = groups.nth(0).locator("[data-cap01-fund-item-note]").first
    assert base_note.evaluate("e => getComputedStyle(e).display") == "inline"
    for width in (1280, 390):
        page.set_viewport_size({"width": width, "height": 900})
        for i in range(2):
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
