"""Real Chromium + the existing Flask server: COMPONENT-INVENTORY-DECLARE-LIST-01
(EN and AR, desktop and phone width).

Synthetic invention data only. An integrated Mechanical + Electrical /
Electronics invention is started through the real composition form; the
inventor opens the component list, declares ONE component linked to both
declared parts and one unlinked component, and the list shows each once, with
escaped, direction-isolated inventor text and the declared-not-validated
wording. No horizontal overflow at 390 px; RTL in Arabic.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import (
    _start_integrated, MECH_PART, ELEC_PART)

NAME = "<i>Brushless motor</i>"
FUNCTION = "يدير ذراع المفصلة"           # Arabic inventor text on purpose


@pytest.mark.parametrize("lang,width", [("en", 1280), ("ar", 390), ("en", 390),
                                        ("ar", 1280)])
def test_declare_and_list_components(server, page, lang, width):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.set_viewport_size({"width": width, "height": 900})
    _start_integrated(page, server, lang, "mechanical")
    section = page.locator("#component-inventory")
    expect(section).to_have_count(1)
    section.locator("summary").click()
    expect(section.locator("[data-ci-none]")).to_have_text(text("UI_CI_NONE", lang))
    expect(section.locator("[data-ci-boundary]")).to_have_text(text("UI_CI_BOUNDARY", lang))
    form = section.locator("[data-ci-form]")
    assert form.locator("input[type=checkbox]:checked").count() == 0
    page.fill("#component_name", NAME)
    page.fill("#component_function", FUNCTION)
    for box in form.locator("input[name=component_part]").all():
        box.check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()

    section = page.locator("#component-inventory")
    expect(section.locator("[data-ci-ack]")).to_have_text(text("UI_CI_MSG_SAVED", lang))
    page.fill("#component_name", "Lid")
    page.fill("#component_function", "Covers the box")
    section.locator("[data-ci-form] button[type=submit]").click()
    page.wait_for_load_state()

    items = page.locator("#component-inventory [data-ci-item]")
    expect(items).to_have_count(2)
    first = items.nth(0)
    expect(first.locator("[data-ci-name]")).to_have_text(NAME)      # escaped, literal
    assert first.locator("[data-ci-name]").get_attribute("dir") == "auto"
    expect(first.locator("[data-ci-function]")).to_have_text(FUNCTION)
    expect(first.locator("[data-ci-part]")).to_have_text([MECH_PART, ELEC_PART])
    expect(first.locator("[data-ci-item-status]")).to_contain_text(
        text("UI_CI_ITEM_STATUS", lang))
    expect(items.nth(1).locator("[data-ci-unassigned]")).to_have_text(
        text("UI_CI_UNASSIGNED", lang))
    assert page.locator("#component-inventory i").count() == 0     # no markup injected

    viewport = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= viewport + 1
    assert page.locator("#component-inventory").bounding_box()["width"] <= viewport
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
