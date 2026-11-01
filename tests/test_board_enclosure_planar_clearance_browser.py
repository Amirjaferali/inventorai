"""Real Chromium + the existing Flask server: BOARD-ENCLOSURE-PLANAR-CLEARANCE-01, in English and (since
BOARD-ENCLOSURE-ARABIC-QUALIFICATION-01) in Arabic.

Synthetic invention data only. The whole journey runs through the real forms, in each language: an integrated
Mechanical + Electrical / Electronics project, one declared interaction, two declared components taking part in it,
then the planar clearance page — board and enclosure chosen explicitly (nothing pre-selected), the region
described, the nominal values typed, every applicability answer given. 84 x 50 board in an 86 x 56 region with
c = 2 reads NOT MET (margins -1 / 1 mm) with the overlap sketch; correcting region_x to 90 reads MET (1 / 1 mm)
on the NEW revision while the earlier report render keeps its own, clearly historical identity; an unknown
clearance reads MISSING INFORMATION with no comparison; an Arabic-Indic digit is refused, never read as a number.
The Arabic page is RTL with every number LTR-isolated; at phone width nothing overflows. Set
``PCC_SCREENSHOT_DIR`` to keep screenshots.
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


NAMES = {"en": ("Driver board", "Plastic case"),
         "ar": ("لوحة التحكم driver", "العلبة البلاستيكية")}
REGION = {"en": "Inner floor between the four mounting posts, at board height",
          "ar": "الأرضية الداخلية بين أعمدة التثبيت الأربعة، عند ارتفاع اللوحة"}


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
    for name, function in zip(NAMES[lang], ("Controls the motor", "Holds and protects the board")):
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


def _fill(page, lang, values, unknown=()):
    form = page.locator("[data-pcc-form]")
    board, case = NAMES[lang]
    form.locator("#pcc-board").select_option(label=board)
    form.locator("#pcc-enclosure").select_option(label=case)
    page.fill("#pcc-region", REGION[lang])
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


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_planar_clearance_journey(server, page, lang):
    """The SAME journey in English and in Arabic (BOARD-ENCLOSURE-ARABIC-QUALIFICATION-01):
    the outcome, margins, revisions and snapshot identity do not depend on the language."""
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, lang, "mechanical")
    _prepare(page, lang)
    link = page.locator("[data-pcc-link] a").first
    expect(link).to_have_text(text("UI_PCC_LINK", lang))
    link.click()
    page.wait_for_load_state()
    assert "/interface-clearance/" in page.url
    clearance_url = page.url
    content = page.locator("[data-pcc-page]")
    assert content.get_attribute("lang") == lang
    assert content.get_attribute("dir") == ("rtl" if lang == "ar" else "ltr")
    expect(page.locator("h1")).to_have_text(text("UI_PCC_TITLE", lang))
    expect(page.locator("[data-pcc-none]")).to_have_text(text("UI_PCC_STATE_NONE", lang))
    form = page.locator("[data-pcc-form]")
    assert form.locator("input[type=radio]:checked").count() == 0          # nothing pre-answered
    assert form.locator("#pcc-board").input_value() == ""                   # nothing pre-selected
    expect(form.locator("[data-pcc-decl] legend")).to_have_count(8)
    expect(page.locator("[data-pcc-digits-help]")).to_have_text(text("UI_PCC_DIGITS_HELP", lang))
    assert page.locator("#pcc-v-board_x").get_attribute("dir") == "ltr"
    _shot(page, "%s_01_empty_form" % lang)

    _fill(page, lang, ("84", "50", "86", "56", "2"))
    expect(page.locator("[data-pcc-notice]")).to_have_text(text("UI_PCC_MSG_SAVED", lang))
    expect(page.locator("[data-pcc-outcome]")).to_have_attribute("data-pcc-outcome", "NOT_MET")
    expect(page.locator("[data-pcc-outcome]")).to_have_text(text("UI_PCC_OUTCOME_NOT_MET", lang))
    expect(page.locator("[data-pcc-margin]")).to_have_text(["-1 mm", "1 mm"])
    expect(page.locator("[data-pcc-shortfall]")).to_have_text(
        text("UI_PCC_AXIS_NOT_MET", lang) + " 1 mm")
    expect(page.locator("[data-pcc-diagram] [data-pcc-dg-overlap]")).to_be_visible()
    expect(page.locator("[data-pcc-disclosure] li")).to_have_count(7)
    expect(page.locator("[data-pcc-disclosure] li").nth(6)).to_have_text(
        text("UI_PCC_DISCLOSURE_7", lang))
    expect(page.locator("[data-pcc-board] bdi").first).to_have_text(NAMES[lang][0])
    expect(page.locator("[data-pcc-region-description] bdi")).to_have_text(REGION[lang])
    # the negative margin keeps its sign and order in the rendered text, whatever the direction
    first_margin = page.locator("[data-pcc-margin]").first
    assert first_margin.get_attribute("dir") == "ltr"
    assert first_margin.evaluate("e => getComputedStyle(e).direction") == "ltr"
    old_revision = page.locator("[data-pcc-revision]").inner_text()
    old_digest = page.locator("[data-pcc-digest]").inner_text()
    assert old_revision == "0"
    _shot(page, "%s_02_not_met" % lang)

    page.goto(server + "/session/%s/deliverable" % sid)
    page.wait_for_load_state()
    old_report = page.content()
    section = page.locator("[data-pcc-report]")
    assert section.get_attribute("lang") == lang
    expect(section.locator("[data-pcc-outcome]")).to_have_attribute("data-pcc-outcome", "NOT_MET")
    expect(section.locator("h2")).to_have_text(text("UI_PCC_REPORT_HEADING", lang))
    _shot(page, "%s_03_report_not_met" % lang)
    page.goto(clearance_url)
    page.wait_for_load_state()

    page.fill("#pcc-v-region_x", "90")
    page.locator("[data-pcc-form] button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-pcc-outcome]")).to_have_attribute("data-pcc-outcome", "MET")
    expect(page.locator("[data-pcc-outcome]")).to_have_text(text("UI_PCC_OUTCOME_MET", lang))
    expect(page.locator("[data-pcc-margin]")).to_have_text(["1 mm", "1 mm"])
    assert page.locator("[data-pcc-revision]").inner_text() == "1"
    assert page.locator("[data-pcc-digest]").inner_text() != old_digest
    expect(page.locator("[data-pcc-history-item]")).to_have_count(2)
    _shot(page, "%s_04_met_after_correction" % lang)

    page.goto(server + "/session/%s/deliverable" % sid)
    page.wait_for_load_state()
    expect(page.locator("[data-pcc-report] [data-pcc-outcome]")).to_have_attribute(
        "data-pcc-outcome", "MET")
    assert page.locator("[data-pcc-report] [data-pcc-revision]").inner_text() == "1"
    # the earlier render still names its own revision, digest, outcome and historical status
    assert 'data-pcc-outcome="NOT_MET"' in old_report
    assert re.search(r"data-pcc-revision[^>]*>0<", old_report)
    assert old_digest in old_report
    assert text("UI_PCC_HISTORICAL_NOTE", lang) in old_report
    _shot(page, "%s_05_report_met" % lang)
    page.goto(clearance_url)
    page.wait_for_load_state()

    _fill(page, lang, ("84", "50", "90", "56", ""), unknown=("c",))
    expect(page.locator("[data-pcc-outcome]")).to_have_attribute(
        "data-pcc-outcome", "MISSING_INFORMATION")
    expect(page.locator("[data-pcc-margin]")).to_have_count(0)
    expect(page.locator("[data-pcc-missing-item=c]")).to_have_text(text("UI_PCC_VALUE_c", lang))
    expect(page.locator("[data-pcc-value=c] [data-pcc-value-state]")).to_have_text(
        text("UI_PCC_VALUE_UNKNOWN", lang))
    _shot(page, "%s_06_unknown_clearance" % lang)

    # an Arabic-Indic number is refused, never read as a value
    page.fill("#pcc-v-c", "٢")
    page.locator("[data-pcc-form] input[name=unknown_c]").uncheck()
    page.locator("[data-pcc-form] button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-pcc-error]")).to_have_text(text("UI_PCC_MSG_REJECTED", lang))
    expect(page.locator("[data-pcc-outcome]")).to_have_attribute(
        "data-pcc-outcome", "MISSING_INFORMATION")
    _shot(page, "%s_07_arabic_indic_refused" % lang)

    page.set_viewport_size({"width": 390, "height": 900})
    _no_overflow(page, "[data-pcc-page]")
    _shot(page, "%s_08_phone" % lang)
    assert not errors, errors
