"""Real Chromium + the existing Flask server: Step 6 functional-to-qualified-
engineering action continuity (EN and AR).

Synthetic invention data only. A Mechanical project is started from an idea the
FUNCTIONAL-NEED-TO-CAPABILITY-HANDOFF-01 reading proposes as screen support; the
provisional reading shows ONE link to the existing CAP-13 page; following it
opens the unchanged form with nothing selected or filled; the inventor's own
declarations and values give the existing deterministic, UNVALIDATED result.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401

IDEA = "I want a stand that holds my monitor above my desk."


def _start(page, base, lang):
    page.goto(base + "/")
    if lang == "ar":
        page.get_by_role("button", name="العربية", exact=True).click()
    page.fill("#idea", IDEA)
    page.click("main input[type=submit], main button[type=submit]")
    page.wait_for_load_state()
    choice = page.locator('input[name=domain_choice][value="mechanical"]')
    if choice.count():
        choice.check()
        page.click("main input[type=submit], main button[type=submit]")
        page.wait_for_load_state()
    confirm = page.locator("input[name=domain_confirm]")
    assert confirm.input_value() == "mechanical"
    confirm.check()
    page.click("main input[type=submit], main button[type=submit]")
    page.wait_for_load_state()
    return page.url.rsplit("/session/", 1)[1].split("?")[0]


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_reading_to_cap13_journey(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start(page, server, lang)
    handoff = page.locator("[data-functional-handoff]")
    handoff.locator("summary").click()
    role = handoff.locator('[data-fh-role="SCREEN_SUPPORT"]')
    expect(role).to_have_attribute("data-fh-status", "PROPOSED")
    expect(role.locator("[data-fh-quote]").first).to_have_text(IDEA)
    action = role.locator("[data-fh-action]")
    expect(action).to_have_count(1)
    expect(action).to_have_text(text("UI_FH_ACTION_CAP13_CONDITIONAL_REACTIONS", lang))
    assert action.get_attribute("href") == f"/session/{sid}/support-reactions"
    expect(role).to_contain_text(text("UI_FH_ACTION_NOTE", lang))
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    page.set_viewport_size({"width": 1280, "height": 900})

    action.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/support-reactions")
    form = page.locator("[data-cap13-form]")
    assert form.locator("input[type=radio]:checked").count() == 0
    for name in ("P", "L", "x"):
        assert page.input_value(f"#cap13-{name}") == ""
    for fieldset in form.locator("[data-cap13-declaration]").all():
        fieldset.locator("input[value=matches]").check()
    for fieldset in form.locator("[data-cap13-screen]").all():
        fieldset.locator("input[value=no]").check()
    page.fill("#cap13-P", "1000")
    page.fill("#cap13-L", "2000")
    page.fill("#cap13-x", "500")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    reactions = page.locator("[data-cap13-reaction]")
    expect(reactions).to_have_count(2)
    expect(reactions.nth(0)).to_have_text("750.0 N")
    expect(reactions.nth(1)).to_have_text("250.0 N")
    expect(page.locator("[data-cap13-status]")).to_contain_text("UNVALIDATED")
    expect(page.locator("[data-cap13-disclosure]")).to_be_visible()
    assert not errors
