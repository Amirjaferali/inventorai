"""Real Chromium + the existing Flask server: Stage 27 / THERM-01 Single-Path
Temperature-Difference Slice 1 (EN and AR).

Synthetic invention data only. An Electrical / Electronics project is started
through the real forms; the optional link leads to the request-local page, every
declaration and screen item is answered explicitly (nothing is pre-selected), the
values are typed, and the temperature difference renders in the response itself.
At phone width the page has no horizontal overflow; in Arabic it is RTL and the
numbers, unit tokens and role symbols stay direction-isolated.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401

SEED = "ESP32 microcontroller circuit with a voltage sensor"


def _start_electronics(page, base, lang):
    page.goto(base + "/")
    if lang == "ar":
        page.get_by_role("button", name="العربية", exact=True).click()
    page.fill("#idea", SEED)
    page.click("main input[type=submit], main button[type=submit]")
    page.wait_for_load_state()
    choice = page.locator('input[name=domain_choice][value="electronics_electrical"]')
    if choice.count():
        choice.check()
        page.click("main input[type=submit], main button[type=submit]")
        page.wait_for_load_state()
    confirm = page.locator("input[name=domain_confirm]")
    assert confirm.input_value() == "electronics_electrical"
    confirm.check()
    page.click("main input[type=submit], main button[type=submit]")
    page.wait_for_load_state()
    return page.url.rsplit("/session/", 1)[1].split("?")[0]


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_temperature_difference_journey(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    link = page.locator("[data-therm01-link] a")
    expect(link).to_have_text(text("UI_THERM01_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/temperature-difference")

    form = page.locator("[data-therm01-form]")
    radios = form.locator("input[type=radio]")
    expect(radios).to_have_count(32)
    assert form.locator("input[type=radio]:checked").count() == 0
    for fieldset in form.locator("[data-therm01-declaration]").all():
        fieldset.locator("input[value=applies]").check()
    for fieldset in form.locator("[data-therm01-screen]").all():
        fieldset.locator("input[value=no]").check()
    page.fill("#therm01-P", "10")
    page.fill("#therm01-R_theta", "2.5")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/temperature-difference")

    value = page.locator("[data-therm01-result-value]")
    expect(value).to_have_count(1)
    expect(value).to_have_text("25.0 K")
    assert value.locator("bdi").get_attribute("dir") == "ltr"
    expect(page.locator("[data-therm01-method] bdi").first).to_have_text(
        "therm01:conduction_temperature_difference_single_path")
    expect(page.locator("[data-therm01-disclosure]")).to_be_visible()
    expect(page.locator("[data-therm01-disclosure] li")).to_have_count(7)
    expect(page.locator("[data-therm01-status]")).to_contain_text("UNVALIDATED")

    # a screen YES shows one reason and no number
    form.locator("[data-therm01-screen=cryogenic] input[value=yes]").check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-therm01-outcome]")).to_have_count(1)
    expect(page.locator("[data-therm01-result-value]")).to_have_count(0)

    # layout: coherent at phone width, no horizontal overflow; RTL on Arabic
    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator("[data-therm01-form]").bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
        assert page.locator("#therm01-R_theta").get_attribute("dir") == "ltr"
        isolated = page.locator("label[for=therm01-R_theta] bdi[dir=ltr]")
        assert "K/W" in isolated.all_inner_texts()
        assert "Rθ" in isolated.all_inner_texts()
    assert not errors
