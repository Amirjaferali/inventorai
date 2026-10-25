"""Real Chromium + the existing Flask server: 28-T4 Control-Cycle Slice 1 (EN and AR).

Synthetic data only. An Electrical / Electronics project is started through the
real forms; the optional link leads to the request-local page, every
confirmation and screen item is answered explicitly (nothing is pre-selected),
the previous state and start_input are chosen, and the cycle result renders in
the response itself: all four reference cases, a no-transition result shown as
a normal result, a refusal with no state or output, no horizontal overflow at
phone width and, in Arabic, an RTL page with the tokens direction-isolated.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_therm01_temperature_difference_browser import _start_electronics

REFERENCE = (("READY", "true", "RUNNING", "true", "APPLIED"),
             ("READY", "false", "READY", "false", "NOT_APPLIED_CONDITION_FALSE"),
             ("RUNNING", "true", "RUNNING", "true", "NOT_APPLICABLE_FROM_STATE"),
             ("RUNNING", "false", "RUNNING", "true", "NOT_APPLICABLE_FROM_STATE"))


def _answer_all(page):
    form = page.locator("[data-cc-form]")
    for fieldset in form.locator("[data-cc-declaration]").all():
        fieldset.locator("input[value=applies]").check()
    for fieldset in form.locator("[data-cc-screen]").all():
        fieldset.locator("input[value=no]").check()


def _run(page, previous, start_input):
    form = page.locator("[data-cc-form]")
    form.locator(f"[data-cc-previous] input[value={previous}]").check()
    form.locator(f"[data-cc-input] input[value={start_input}]").check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_control_cycle_journey(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    link = page.locator("[data-cc-link] a")
    expect(link).to_have_text(text("UI_CC_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/control-cycle")
    form = page.locator("[data-cc-form]")
    expect(form.locator("input[type=radio]")).to_have_count(26)
    assert form.locator("input[type=radio]:checked").count() == 0
    expect(page.locator("[data-cc-definition] li")).to_have_count(4)

    _answer_all(page)
    for previous, start_input, next_state, output, status in REFERENCE:
        _run(page, previous, start_input)
        expect(page.locator("[data-cc-result-previous]")).to_have_text(previous)
        expect(page.locator("[data-cc-result-input]")).to_have_text(start_input)
        expect(page.locator("[data-cc-result-next]")).to_have_text(next_state)
        expect(page.locator("[data-cc-result-output]")).to_have_text(output)
        assert page.locator("[data-cc-result-transition]").get_attribute(
            "data-cc-transition-status") == status
        expect(page.locator("[data-cc-outcome]")).to_have_count(0)
    expect(page.locator("[data-cc-status]")).to_contain_text("UNVALIDATED")
    expect(page.locator("[data-cc-disclosure] li")).to_have_count(7)

    # a high-risk YES refuses with one reason and no state or output
    page.locator("[data-cc-screen=safety_function] input[value=yes]").check()
    page.locator("[data-cc-form] button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-cc-outcome]")).to_have_count(1)
    expect(page.locator("[data-cc-result-next]")).to_have_count(0)

    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator("[data-cc-form]").bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
        isolated = page.locator("[data-cc-definition] bdi[dir=ltr]").all_inner_texts()
        assert any("READY" in run for run in isolated)
        assert any("start_input" in run for run in isolated)
    assert not errors
