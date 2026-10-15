"""Real Chromium + the existing Flask server: CAP12-INTEGRATED-MECHANICAL-PART-01
(EN and AR).

Synthetic invention data only. An integrated Mechanical + Electrical /
Electronics invention is started through the real composition form with the
Electrical / Electronics part as the initial analysis focus; the session page
offers the form mock-up advisory, the advisory page names the declared
Mechanical part with the fixed attribution note, the advice is returned for it,
and at phone width (390 px) there is no horizontal overflow. In Arabic the page
is RTL and the part name is direction-auto isolated.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import (
    MECH_PART, _no_overflow, _start_integrated)


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_electronics_focus_reaches_cap12_for_its_mechanical_part(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, lang, "electronics_electrical")
    link = page.locator("[data-cap12-link] a")
    expect(link).to_have_text(text("UI_CAP12_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/form-mockup-advisory")
    part = page.locator("[data-cap12-part]")
    expect(part).to_contain_text(text("UI_CAP12_PART_LABEL", lang))
    expect(part).to_contain_text(text("UI_CAP12_PART_NOTE", lang))
    name = page.locator("[data-cap12-part-name]")
    expect(name).to_have_text(MECH_PART)
    assert name.get_attribute("dir") == "auto"
    _no_overflow(page, "[data-cap12-part]")

    form = page.locator("[data-cap12-form]")
    page.fill("#cap12-name", "Hinge arm shell")
    page.fill("#cap12-function", "Shows the shape of the hinge arm for review.")
    page.select_option("#cap12-role", "form_mockup")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator('[data-cap12-result="available"]')).to_have_count(1)
    assert page.locator("[data-cap12-alternative]").count() == 2
    expect(page.locator("[data-cap12-part-name]")).to_have_text(MECH_PART)

    _no_overflow(page, "[data-cap12-result]")
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
