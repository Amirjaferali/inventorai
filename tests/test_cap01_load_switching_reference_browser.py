"""Real Chromium + the existing Flask server: 28-T3-LOAD-SWITCHING-PRINCIPLE-REFERENCE-01
(EN and AR).

Synthetic invention data only. An Electronics project is started through the real
forms; its canonical MECHANISM_COMPLETENESS gap is set current in-process (as the
unit harness does), and the report then shows the sensing, accuracy / resolution and
controller groups and, FOURTH, the ONE prose-only load-switching group — title, the
conditional intro, the explanation, the CC BY 4.0 attribution and the boundary — with
no equation element. At 1280 px and at 390 px there is no horizontal overflow; in
Arabic the page is RTL. A CLOSED gap shows no group.
"""
import pytest
from playwright.sync_api import expect

import web.app as webapp
from engine.idea_state import CLOSED, MECHANISM_COMPLETENESS, OPEN, PHYSICAL_FEASIBILITY
from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap01_mechanical_open_gap_context import _gaps
from tests.test_cap01_electrical_energy_time_reference_browser import _start_electronics

LS = "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_MECHANISM_COMPLETENESS_LOAD_SWITCHING_FUNDAMENTALS_"
TOKENS = ("https://www.ibiblio.org/kuphaldt/electricCircuits/Semi/SEMI_4.html",
          "https://creativecommons.org/licenses/by/4.0/", "Tony R. Kuphaldt")


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_load_switching_group_renders_fourth_prose_only_and_fits_desktop_and_phone_width(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    webapp.SESSION_STORE[sid]["state"].gaps = _gaps((MECHANISM_COMPLETENESS, OPEN))

    page.goto(f"{server}/session/{sid}/deliverable")
    groups = page.locator("[data-cap01-fundamentals]")
    expect(groups).to_have_count(4)
    assert [groups.nth(i).get_attribute("data-cap01-fundamentals") for i in range(4)] == [
        "sensing-value-threshold-reference-v1", "measurement-accuracy-resolution-reference-v1",
        "controller-input-logic-output-reference-v1", "transistor-load-switching-reference-v1"]
    group = groups.nth(3)
    expect(group).to_be_visible()
    expect(group.locator("[data-cap01-fund-title]")).to_have_text(text(LS + "TITLE", lang))
    intro = group.locator("[data-cap01-fund-intro]")
    expect(intro).to_have_text(text(LS + "INTRO", lang))
    expect(intro).to_contain_text("may not apply to your invention" if lang == "en"
                                  else "قد لا ينطبق هذا المبدأ العام على اختراعك")
    items = group.locator("[data-cap01-fund-claim]")
    expect(items).to_have_count(1)
    assert items.get_attribute("data-cap01-fund-claim") == "bjt-current-controlled-load-switching"
    expect(items.locator("[data-cap01-fund-item-title]")).to_have_text(text(LS + "ITEM_1_TITLE", lang))
    expect(items.locator("[data-cap01-fund-item-text]")).to_have_text(text(LS + "ITEM_1_TEXT", lang))
    source = group.locator("[data-cap01-fund-source]")
    expect(source).to_have_text(text(LS + "SOURCE", lang))
    for token in TOKENS:
        expect(source).to_contain_text(token)
    expect(group.locator("[data-cap01-fund-boundary]")).to_have_text(text(LS + "BOUNDARY", lang))
    for sel in ("[data-cap01-fund-equation]", "[data-cap01-fund-item-lead]", "[data-cap01-fund-item-note]",
                "a, button, form, input, select, textarea", "img, svg, table, figure, code, pre"):
        assert group.locator(sel).count() == 0, sel

    for width in (1280, 390):
        page.set_viewport_size({"width": width, "height": 900})
        client_width = page.evaluate("document.documentElement.clientWidth")
        assert page.evaluate("document.documentElement.scrollWidth") <= client_width + 1, width
        box = group.bounding_box()
        assert box["x"] >= -1 and box["x"] + box["width"] <= client_width + 1, width
        assert source.evaluate("e => e.scrollWidth <= e.clientWidth + 1"), width
        expect(source).to_be_visible()
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
        assert group.evaluate("e => getComputedStyle(e).direction") == "rtl"

    webapp.SESSION_STORE[sid]["state"].gaps = _gaps((MECHANISM_COMPLETENESS, CLOSED), (PHYSICAL_FEASIBILITY, OPEN))
    page.goto(f"{server}/session/{sid}/deliverable")
    assert page.locator("[data-cap01-fundamentals='transistor-load-switching-reference-v1']").count() == 0
    assert not errors
