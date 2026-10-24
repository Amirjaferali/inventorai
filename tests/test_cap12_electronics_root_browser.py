"""Real Chromium + the existing Flask server: CAP12-ELECTRONICS-ROOT-01 (EN and AR).

Synthetic invention data only. A single-domain Electrical / Electronics project
is started through the real forms; the session page offers the form mock-up
advisory, the advisory page carries no part attribution, the same two
family-level alternatives are returned, and at phone width (390 px) there is no
horizontal overflow. In Arabic the page is RTL.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import _no_overflow
from tests.test_therm01_temperature_difference_browser import _start_electronics


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_a_single_domain_electronics_project_reaches_cap12(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    link = page.locator("[data-cap12-link] a")
    expect(link).to_have_text(text("UI_CAP12_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/form-mockup-advisory")
    expect(page.locator("[data-cap12-part]")).to_have_count(0)

    form = page.locator("[data-cap12-form]")
    page.fill("#cap12-name", "Sensor box shell")
    page.fill("#cap12-function", "Shows the outer shape of the sensor box for review.")
    page.select_option("#cap12-role", "form_mockup")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator('[data-cap12-result="available"]')).to_have_count(1)
    assert page.locator("[data-cap12-alternative]").count() == 2
    expect(page.locator("[data-cap12-part]")).to_have_count(0)
    expect(page.locator("[data-cap12-shown-name]")).to_have_text("Sensor box shell")

    _no_overflow(page, "[data-cap12-result]")
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
