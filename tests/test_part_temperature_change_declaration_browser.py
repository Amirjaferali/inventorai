"""Real Chromium + the existing Flask server: PART-BOUND-TEMPERATURE-CHANGE-DECLARATION-01
(Increment A), EN and AR.

Synthetic invention data only. An integrated Mechanical + Electrical / Electronics
project is started through the real forms. On the session page the Mechanical
part reads NOT DECLARED; recording needs the explicit confirmation; the
statement then reads as the inventor's own (OWNER_STATED / UNVALIDATED) and can
be withdrawn, after which it reads NOT DECLARED again. Arabic is RTL; at phone
width there is no horizontal overflow.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import _start_integrated


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_declare_and_withdraw_journey(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, lang, "electronics_electrical")
    assert page.url.endswith(f"/session/{sid}") or f"/session/{sid}" in page.url
    block = page.locator("[data-part-tc]")
    expect(block).to_have_count(1)
    expect(block.locator("[data-part-tc-state=not_declared]")).to_have_text(
        text("UI_PTC_STATUS_NOT_DECLARED", lang))
    form = block.locator("[data-part-tc-form=declare]")
    confirm = form.locator("input[name=tc_confirm]")
    assert not confirm.is_checked()
    # without the confirmation nothing is recorded
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-part-tc-error]")).to_have_text(
        text("UI_PTC_MSG_CONFIRM_REQUIRED", lang))
    expect(page.locator("[data-part-tc-state=not_declared]")).to_have_count(1)
    page.locator("[data-part-tc-form=declare] input[name=tc_confirm]").check()
    page.locator("[data-part-tc-form=declare] button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-part-tc-ack]")).to_have_text(text("UI_PTC_MSG_DECLARED", lang))
    declared = page.locator("[data-part-tc-state=declared]")
    expect(declared).to_have_text(text("UI_PTC_STATUS_DECLARED", lang))
    expect(declared).to_contain_text("OWNER_STATED")
    expect(declared).to_contain_text("UNVALIDATED")
    expect(page.locator("[data-part-tc-withdraw-note]")).to_have_text(
        text("UI_PTC_WITHDRAW_NOTE", lang))
    # it survives a reload
    page.reload()
    expect(page.locator("[data-part-tc-state=declared]")).to_have_count(1)
    page.locator("[data-part-tc-form=withdraw] button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-part-tc-ack]")).to_have_text(text("UI_PTC_MSG_WITHDRAWN", lang))
    expect(page.locator("[data-part-tc-state=not_declared]")).to_have_count(1)

    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator("[data-part-tc]").bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
