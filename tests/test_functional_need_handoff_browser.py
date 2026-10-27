"""Real Chromium + the existing Flask server: FUNCTIONAL-NEED-TO-CAPABILITY-
HANDOFF-01 (EN and AR).

Synthetic invention data only. A watering idea is started through the real
forms; the session page shows InventorAI's proposed reading as a closed
section that opens to the inventor's own words, labelled as a proposal, with
no method link inside it. At phone width there is no horizontal overflow; in
Arabic the page is RTL and the quote keeps its own direction.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import _no_overflow

IDEA = "I want a device that waters my plants automatically, but I don't know how."


def _start(page, base, lang):
    page.goto(base + "/")
    if lang == "ar":
        page.get_by_role("button", name="العربية", exact=True).click()
    page.fill("#idea", IDEA)
    page.click("main input[type=submit], main button[type=submit]")
    page.wait_for_load_state()
    for _ in range(3):
        if "/session/" in page.url:
            break
        choice = page.locator('input[type=radio][name=domain_choice]'
                              '[value="electronics_electrical"]')
        if choice.count():
            choice.check()
        confirm = page.locator("input[type=checkbox][name=domain_confirm]")
        if confirm.count():
            confirm.check()
        page.click("main input[type=submit], main button[type=submit]")
        page.wait_for_load_state()
    assert "/session/" in page.url


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_the_proposed_reading_is_shown_with_the_inventors_words(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    _start(page, server, lang)
    section = page.locator("[data-functional-handoff]")
    expect(section).to_have_count(1)
    section.locator("summary").click()
    expect(section).to_contain_text(text("UI_FH_TITLE", lang))
    role = section.locator('[data-fh-role="WATERING"]')
    expect(role).to_have_count(1)
    expect(role).to_contain_text(text("UI_FH_STATUS_PROPOSED", lang))
    expect(role.locator("[data-fh-quote]")).to_contain_text("waters my plants automatically")
    assert role.locator("[data-fh-quote]").first.get_attribute("dir") == "auto"
    expect(role.locator("[data-fh-uncertain]")).to_have_count(1)
    expect(role.locator("[data-fh-uncovered]")).to_contain_text(
        text("UI_FH_UNCOVERED_WATERING", lang))
    assert section.locator("a").count() == 0
    _no_overflow(page, "[data-functional-handoff]")
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
