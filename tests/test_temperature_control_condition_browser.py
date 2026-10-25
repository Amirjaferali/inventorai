"""Real Chromium + the existing Flask server: TEMPERATURE-TO-CONTROL-CONDITION-01 (EN and AR).

Synthetic data only. An Electrical / Electronics project is started through the
real forms; the optional link leads to the request-local composition page, every
TMP36 declaration and screen item, the threshold confirmation, every 28-T4
confirmation and screen item are answered explicitly (nothing is pre-selected),
and the result renders in the response itself: a success at exact equality, a
RUNNING / false cycle that is not reset, a TMP36 refusal and a 28-T4 refusal
that show no temperature, condition, state or output, no horizontal overflow at
phone width and, in Arabic, an RTL page.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_therm01_temperature_difference_browser import _start_electronics


def _answer_all(page):
    form = page.locator("[data-tcc-form]")
    for selector in ("[data-tcc-tmp36-declaration]", "[data-tcc-cc-declaration]",
                     "[data-tcc-condition-declaration]"):
        for fieldset in form.locator(selector).all():
            fieldset.locator("input[value=applies]").check()
    for selector in ("[data-tcc-tmp36-screen]", "[data-tcc-cc-screen]"):
        for fieldset in form.locator(selector).all():
            fieldset.locator("input[value=no]").check()


def _submit(page, v_out, threshold, previous):
    page.fill("#tcc-v_out", v_out)
    page.fill("#tcc-threshold", threshold)
    page.locator(f"[data-tcc-previous] input[value={previous}]").check()
    page.locator("[data-tcc-form] button[type=submit]").click()
    page.wait_for_load_state()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_temperature_control_condition_journey(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    link = page.locator("[data-tcc-link] a")
    expect(link).to_have_text(text("UI_TCC_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/temperature-control-condition")
    form = page.locator("[data-tcc-form]")
    assert form.locator("input[type=radio]:checked").count() == 0
    assert form.locator("input[name$=start_input]").count() == 0

    _answer_all(page)
    _submit(page, "750.1", "25.01", "READY")           # exact equality -> true
    expect(page.locator("[data-tcc-result-temperature]")).to_have_text("25.01 °C")
    assert page.locator("[data-tcc-result-condition]").get_attribute("data-tcc-condition") == "true"
    expect(page.locator("[data-tcc-result-next]")).to_have_text("RUNNING")
    expect(page.locator("[data-tcc-result-output]")).to_have_text("true")
    expect(page.locator("[data-tcc-status]")).to_contain_text("UNVALIDATED")
    expect(page.locator("[data-tcc-disclosure] li")).to_have_count(7)

    _submit(page, "750", "30", "RUNNING")              # false does not reset RUNNING
    assert page.locator("[data-tcc-result-condition]").get_attribute("data-tcc-condition") == "false"
    expect(page.locator("[data-tcc-result-next]")).to_have_text("RUNNING")
    expect(page.locator("[data-tcc-result-output]")).to_have_text("true")

    _submit(page, "2000", "25", "READY")               # TMP36 refusal: nothing shown
    expect(page.locator("[data-tcc-outcome]")).to_have_count(1)
    expect(page.locator("[data-tcc-part-refusal]")).to_have_count(1)
    expect(page.locator("[data-tcc-result-temperature]")).to_have_count(0)
    expect(page.locator("[data-tcc-result-next]")).to_have_count(0)

    page.locator("[data-tcc-cc-screen=safety_function] input[value=yes]").check()
    _submit(page, "750", "25", "READY")                # 28-T4 refusal: nothing shown
    expect(page.locator("[data-tcc-outcome]")).to_have_count(1)
    expect(page.locator("[data-tcc-result-condition]")).to_have_count(0)

    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator("[data-tcc-form]").bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
        assert page.locator("#tcc-threshold").get_attribute("dir") == "ltr"
    assert not errors
