"""Real Chromium + the existing Flask server: THERM01-VERIFICATION-MEASUREMENT-STEP-01
(EN and AR, RTL, 390 px).

Synthetic invention data only. On an Electronics project the THERM-01 page shows the
"How to check this estimate" block only after a successful result, under the fixed
disclosure, with five steps, its assumption note, its boundary and its collapsed source
notice; a screen YES removes it together with the number.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.cap01_therm01_verification_addition import TVM_SLUG, TVM_STEM
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_therm01_temperature_difference_browser import _start_electronics


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_verification_preparation_journey(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    page.goto(f"{server}/session/{sid}/temperature-difference")
    page.wait_for_load_state()
    expect(page.locator("[data-therm01-verification]")).to_have_count(0)
    form = page.locator("[data-therm01-form]")
    for fieldset in form.locator("[data-therm01-declaration]").all():
        fieldset.locator("input[value=applies]").check()
    for fieldset in form.locator("[data-therm01-screen]").all():
        fieldset.locator("input[value=no]").check()
    page.fill("#therm01-P", "10")
    page.fill("#therm01-R_theta", "2.5")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-therm01-result-value]")).to_have_text("25.0 K")
    block = page.locator("[data-therm01-verification]")
    expect(block).to_have_count(1)
    assert block.get_attribute("data-therm01-verification") == TVM_SLUG
    expect(block).to_be_visible()
    expect(block.locator("[data-therm01-verify-title]")).to_have_text(text(TVM_STEM + "TITLE", lang))
    expect(block.locator("[data-therm01-verify-steps] li")).to_have_count(5)
    expect(block.locator("[data-therm01-verify-assumption]")).to_be_visible()
    expect(block.locator("[data-therm01-verify-boundary]")).to_be_visible()
    assert block.locator("input, button, a, form, select, textarea").count() == 0
    disclosure = page.locator("[data-therm01-disclosure]").bounding_box()
    assert block.bounding_box()["y"] > disclosure["y"]
    source = block.locator("[data-therm01-verify-source-text]")
    expect(source).to_be_hidden()
    block.locator("[data-therm01-verify-source] summary").click()
    expect(source).to_be_visible()
    expect(source).to_contain_text("400-86")
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
        assert block.locator("[data-therm01-verify-steps] li bdi[dir=ltr]").count() >= 1
    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    page.set_viewport_size({"width": 1280, "height": 900})
    form.locator("[data-therm01-screen=cryogenic] input[value=yes]").check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-therm01-result-value]")).to_have_count(0)
    expect(page.locator("[data-therm01-verification]")).to_have_count(0)
    assert not errors
