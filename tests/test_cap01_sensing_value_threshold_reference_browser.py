"""Real Chromium + the existing Flask server: 28-T1-SENSING-VALUE-THRESHOLD-01
(EN and AR).

Synthetic invention data only. An Electronics project is started through the real
forms; its canonical MECHANISM_COMPLETENESS gap is set current in-process (as the
unit harness does), and the report then shows the ONE prose-only sensing group —
title, intro, the approved explanation, the CC BY 4.0 attribution and the boundary —
with no equation element. At 1280 px and at 390 px there is no horizontal overflow
(the long attribution URLs wrap inside the group); in Arabic the page is RTL.
"""
import pytest
from playwright.sync_api import expect

import web.app as webapp
from engine.idea_state import MECHANISM_COMPLETENESS, OPEN
from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap01_mechanical_open_gap_context import _gaps
from tests.test_cap01_electrical_energy_time_reference_browser import _start_electronics

SN = "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_MECHANISM_COMPLETENESS_SENSING_FUNDAMENTALS_"


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_sensing_group_renders_prose_only_and_fits_desktop_and_phone_width(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    webapp.SESSION_STORE[sid]["state"].gaps = _gaps((MECHANISM_COMPLETENESS, OPEN))

    page.goto(f"{server}/session/{sid}/deliverable")
    groups = page.locator("[data-cap01-fundamentals]")
    expect(groups).to_have_count(1)
    group = groups.nth(0)
    assert group.get_attribute("data-cap01-fundamentals") == "sensing-value-threshold-reference-v1"
    expect(group).to_be_visible()
    expect(group.locator("[data-cap01-fund-title]")).to_have_text(text(SN + "TITLE", lang))
    expect(group.locator("[data-cap01-fund-intro]")).to_have_text(text(SN + "INTRO", lang))
    items = group.locator("[data-cap01-fund-claim]")
    expect(items).to_have_count(1)
    expect(items.locator("[data-cap01-fund-item-title]")).to_have_text(text(SN + "ITEM_1_TITLE", lang))
    expect(items.locator("[data-cap01-fund-item-text]")).to_have_text(text(SN + "ITEM_1_TEXT", lang))
    expect(group.locator("[data-cap01-fund-source]")).to_have_text(text(SN + "SOURCE", lang))
    expect(group.locator("[data-cap01-fund-boundary]")).to_have_text(text(SN + "BOUNDARY", lang))
    # prose only: no equation, lead or note element (never an empty placeholder), no control
    for sel in ("[data-cap01-fund-equation]", "[data-cap01-fund-item-lead]",
                "[data-cap01-fund-item-note]", "a, button, form, input, select, textarea"):
        assert group.locator(sel).count() == 0, sel

    for width in (1280, 390):
        page.set_viewport_size({"width": width, "height": 900})
        client_width = page.evaluate("document.documentElement.clientWidth")
        assert page.evaluate("document.documentElement.scrollWidth") <= client_width + 1, width
        box = group.bounding_box()
        assert box["x"] >= -1 and box["x"] + box["width"] <= client_width + 1, width
        source = group.locator("[data-cap01-fund-source]")
        assert source.evaluate("e => e.scrollWidth <= e.clientWidth + 1"), width
        expect(source).to_be_visible()
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
