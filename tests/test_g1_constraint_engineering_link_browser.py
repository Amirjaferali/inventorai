"""Real Chromium + the existing Flask server: G1-2 CONSTRAINT-ENGINEERING-LINK-01 (EN and AR).

Synthetic data only. Through the real forms: an integrated project saves one planar clearance check, the inventor
declares one mandatory constraint, opens the project constraints section and links the saved check from the
constraint's own block. The block then shows the link as current, the check's own saved result, that whether the
constraint is met is not assessed, and opens the exact linked check. Removing the link leaves no link. Arabic is
RTL; nothing overflows at 390 px.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import _no_overflow, _start_integrated
from tests.test_board_enclosure_planar_clearance_browser import _fill, _prepare

CONSTRAINT = {"en": "The board must keep at least 2 mm clearance on every side",
              "ar": "يجب أن تبقى حول اللوحة مسافة 2 mm على الأقل من كل جانب"}


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_link_a_saved_check_from_the_constraint_and_open_it(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, lang, "mechanical")
    _prepare(page, lang)
    page.locator("[data-pcc-link] a").first.click()
    page.wait_for_load_state()
    clearance_url = page.url
    _fill(page, lang, ("85", "56", "90", "60", "2"))
    expect(page.locator("[data-pcc-outcome]")).to_have_attribute("data-pcc-outcome", "MET")

    page.goto(f"{server}/session/{sid}")
    section = page.locator("#project-constraints")
    section.locator("summary").first.click()
    form = section.locator("[data-pcn-form]")
    form.locator("#constraint_text").fill(CONSTRAINT[lang])
    form.locator("input[name=constraint_strength][value=mandatory_constraint]").check()
    form.locator("input[name=constraint_confirm]").check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()

    block = page.locator("[data-cel]")
    expect(block).to_have_count(1)
    expect(block).to_have_attribute("data-cel-status", "NONE")
    expect(block.locator("[data-cel-heading]")).to_have_text(text("UI_CEL_HEADING", lang))
    block.locator("[data-cel-link-form] button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-pcn-ack]")).to_have_text(text("UI_CEL_MSG_LINKED", lang))

    block = page.locator("[data-cel]")
    expect(block).to_have_attribute("data-cel-status", "CURRENT")
    expect(block.locator("[data-cel-current]")).to_have_text(text("UI_CEL_STATUS_CURRENT", lang))
    expect(block.locator('[data-cel-result="MET"]')).to_contain_text(text("UI_CEL_RESULT_MET", lang))
    expect(block.locator("[data-cel-not-assessed]")).to_have_text(text("UI_CEL_NOT_ASSESSED", lang))
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    _no_overflow(page, "[data-cel]")
    page.set_viewport_size({"width": 1280, "height": 900})

    block.locator("[data-cel-open]").click()
    page.wait_for_load_state()
    assert page.url.split("#")[0] == clearance_url.split("#")[0]

    page.goto(f"{server}/session/{sid}")
    page.locator("#project-constraints summary").first.click()
    page.locator("[data-cel] [data-cel-unlink-form] button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-pcn-ack]")).to_have_text(text("UI_CEL_MSG_UNLINKED", lang))
    expect(page.locator("[data-cel]")).to_have_attribute("data-cel-status", "NONE")
    assert not errors, errors
