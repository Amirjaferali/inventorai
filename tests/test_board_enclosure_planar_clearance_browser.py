"""Real Chromium + the existing Flask server: BOARD-ENCLOSURE-PLANAR-CLEARANCE-01 (EN; AR notice).

Synthetic invention data only. The whole journey runs through the real forms: an integrated Mechanical +
Electrical / Electronics project, one declared interaction, two declared components taking part in it, then the
planar clearance page — board and enclosure chosen explicitly (nothing pre-selected), the region described, the
nominal values typed, every applicability answer given. 84 x 50 board in an 86 x 56 region with c = 2 reads NOT
MET (margins -1 / 1 mm) with the overlap sketch; correcting region_x to 90 reads MET (1 / 1 mm) on the NEW
revision while the earlier report render keeps its own, clearly historical identity; an unknown clearance reads
MISSING INFORMATION with no comparison. At phone width nothing overflows; on the Arabic interface the localized
English-only notice is shown and the tool itself stays English. Set ``PCC_SCREENSHOT_DIR`` to keep screenshots.
"""
import os
import re

import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import _no_overflow, _start_integrated

SHOTS = os.environ.get("PCC_SCREENSHOT_DIR")


def _shot(page, name):
    if SHOTS:
        os.makedirs(SHOTS, exist_ok=True)
        page.screenshot(path=os.path.join(SHOTS, name + ".png"), full_page=True)


def _prepare(page, lang):
    """Declare one interaction, two components and their participation through the real forms."""
    declare = page.locator("#declare-interface")
    declare.locator("summary").click()
    binding = declare.locator("input[name=interface_binding]").first
    if binding.get_attribute("type") != "hidden":          # a two-part project has one pair
        binding.check()
    declare.locator("#interface_description").fill("The board sits inside the case")
    declare.locator("input[name=interface_confirm]").check()
    declare.get_by_role("button", name=text("UI_S15_IFC_BUTTON", lang)).click()
    page.wait_for_load_state()
    for name, function in (("Driver board", "Controls the motor"),
                           ("Plastic case", "Holds and protects the board")):
        section = page.locator("#component-inventory")
        if not section.locator("#component_name").is_visible():
            section.locator("summary").click()
        page.fill("#component_name", name)
        page.fill("#component_function", function)
        section.locator("[data-ci-form] button[type=submit]").click()
        page.wait_for_load_state()
    page.locator("[data-prep-link] a").click()
    page.wait_for_load_state()
    form = page.locator("[data-icp-form]")
    for box in form.locator("input[name=participant]").all():
        box.check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()


def _fill(page, values, unknown=()):
    form = page.locator("[data-pcc-form]")
    options = form.locator("#pcc-board option")
    names = [options.nth(i).inner_text() for i in range(options.count())]
    form.locator("#pcc-board").select_option(label="Driver board")
    form.locator("#pcc-enclosure").select_option(label="Plastic case")
    assert "Driver board" in names and "Plastic case" in names
    page.fill("#pcc-region", "Inner floor between the four mounting posts, at board height")
    for role, value in zip(("board_x", "board_y", "region_x", "region_y", "c"), values):
        page.fill("#pcc-v-%s" % role, value)
        box = form.locator("input[name=unknown_%s]" % role)
        if role in unknown:
            box.check()
        elif box.is_checked():
            box.uncheck()
    for fieldset in form.locator("[data-pcc-decl]").all():
        fieldset.locator("input[value=applies]").check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()


def test_planar_clearance_journey_en(server, page):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, "en", "mechanical")
    _prepare(page, "en")
    link = page.locator("[data-pcc-link] a").first
    expect(link).to_have_text(text("UI_PCC_LINK", "en"))
    link.click()
    page.wait_for_load_state()
    assert "/interface-clearance/" in page.url
    clearance_url = page.url
    expect(page.locator("[data-pcc-none]")).to_be_visible()
    form = page.locator("[data-pcc-form]")
    assert form.locator("input[type=radio]:checked").count() == 0          # nothing pre-answered
    assert form.locator("#pcc-board").input_value() == ""                   # nothing pre-selected
    _shot(page, "01_empty_form")

    _fill(page, ("84", "50", "86", "56", "2"))
    expect(page.locator("[data-pcc-notice]")).to_have_text("Saved.")
    expect(page.locator("[data-pcc-outcome]")).to_have_attribute("data-pcc-outcome", "NOT_MET")
    expect(page.locator("[data-pcc-margin]")).to_have_text(["-1 mm", "1 mm"])
    expect(page.locator("[data-pcc-shortfall]")).to_have_text("not met: short by 1 mm")
    expect(page.locator("[data-pcc-diagram] [data-pcc-dg-overlap]")).to_be_visible()
    expect(page.locator("[data-pcc-disclosure] li")).to_have_count(7)
    old_identity = page.locator("[data-pcc-identity]").inner_text()
    assert "revision 0" in old_identity
    _shot(page, "02_not_met")

    page.goto(server + "/session/%s/deliverable" % sid)
    page.wait_for_load_state()
    old_report = page.content()
    expect(page.locator("[data-pcc-report] [data-pcc-outcome]")).to_have_attribute(
        "data-pcc-outcome", "NOT_MET")
    _shot(page, "03_report_not_met")
    page.goto(clearance_url)
    page.wait_for_load_state()

    page.fill("#pcc-v-region_x", "90")
    page.locator("[data-pcc-form] button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-pcc-outcome]")).to_have_attribute("data-pcc-outcome", "MET")
    expect(page.locator("[data-pcc-margin]")).to_have_text(["1 mm", "1 mm"])
    new_identity = page.locator("[data-pcc-identity]").inner_text()
    assert "revision 1" in new_identity and new_identity != old_identity
    expect(page.locator("[data-pcc-history-item]")).to_have_count(2)
    _shot(page, "04_met_after_correction")

    page.goto(server + "/session/%s/deliverable" % sid)
    page.wait_for_load_state()
    expect(page.locator("[data-pcc-report] [data-pcc-outcome]")).to_have_attribute(
        "data-pcc-outcome", "MET")
    assert "revision 1" in page.locator("[data-pcc-report] [data-pcc-identity]").inner_text()
    # the earlier render still names its own revision, outcome and historical status
    assert 'data-pcc-outcome="NOT_MET"' in old_report and "revision 0" in old_report
    assert "does not update" in old_report
    _shot(page, "05_report_met")
    page.goto(clearance_url)
    page.wait_for_load_state()

    _fill(page, ("84", "50", "90", "56", ""), unknown=("c",))
    expect(page.locator("[data-pcc-outcome]")).to_have_attribute(
        "data-pcc-outcome", "MISSING_INFORMATION")
    expect(page.locator("[data-pcc-margin]")).to_have_count(0)
    expect(page.locator("[data-pcc-missing-item=c]")).to_be_visible()
    _shot(page, "06_unknown_clearance")

    page.set_viewport_size({"width": 390, "height": 900})
    _no_overflow(page, "[data-pcc-page]")
    assert not errors, errors


def test_planar_clearance_arabic_interface_notice(server, page):
    sid = _start_integrated(page, server, "ar", "mechanical")
    _prepare(page, "ar")
    page.locator("[data-pcc-link] a").first.click()
    page.wait_for_load_state()
    expect(page.locator("[data-pcc-english-only]")).to_have_text(text("UI_PCC_ENGLISH_ONLY", "ar"))
    content = page.locator("[data-pcc-page]")
    assert content.get_attribute("lang") == "en" and content.get_attribute("dir") == "ltr"
    expect(page.locator("h1")).to_have_text(text("UI_PCC_TITLE", "en"))
    page.set_viewport_size({"width": 390, "height": 900})
    _no_overflow(page, "[data-pcc-page]")
    _shot(page, "07_arabic_interface_notice")
    assert re.search(r"/session/%s/interface-clearance/" % sid, page.url)
