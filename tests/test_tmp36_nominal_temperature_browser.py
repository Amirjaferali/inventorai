"""Real Chromium + the existing Flask server: Sensors C3 TMP36 Nominal
Voltage-to-Temperature Slice 1 (EN and AR).

Synthetic data only. An Electrical / Electronics project, and a Mechanical-focus
integrated project with a declared Electrical / Electronics part, are started
through the real forms; the optional link leads to the request-local page, every
declaration and screen item is answered explicitly (nothing is pre-selected), the
inventor's own declared voltage is typed, and the nominal temperature renders in
the response itself, as the exact decimal value, with the nominal-relation note.
At phone width the page has no horizontal overflow; in Arabic it is RTL and the
numbers, unit tokens and role symbols stay direction-isolated.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_therm01_temperature_difference_browser import _start_electronics
from tests.test_cap13_therm01_integrated_part_browser import (
    _start_integrated, _no_overflow, ELEC_PART)


def _fill_and_submit(page, v_out):
    form = page.locator("[data-tmp36-form]")
    assert form.locator("input[type=radio]:checked").count() == 0
    for fieldset in form.locator("[data-tmp36-declaration]").all():
        fieldset.locator("input[value=applies]").check()
    for fieldset in form.locator("[data-tmp36-screen]").all():
        fieldset.locator("input[value=no]").check()
    page.fill("#tmp36-v_out", v_out)
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()


def _resubmit(page, v_out):
    page.fill("#tmp36-v_out", v_out)
    page.locator("[data-tmp36-form] button[type=submit]").click()
    page.wait_for_load_state()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_tmp36_journey_on_an_electronics_project(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    link = page.locator("[data-tmp36-link] a")
    expect(link).to_have_text(text("UI_TMP36_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/tmp36-temperature")
    expect(page.locator("[data-tmp36-form] input[type=radio]")).to_have_count(22)
    expect(page.locator("[data-tmp36-voltage-note]")).to_be_visible()

    _fill_and_submit(page, "750")
    value = page.locator("[data-tmp36-result-value]")
    expect(value).to_have_text("25.0 °C")
    assert value.locator("bdi").get_attribute("dir") == "ltr"
    expect(page.locator("[data-tmp36-nominal-note]")).to_be_visible()
    expect(page.locator("[data-tmp36-status]")).to_contain_text("UNVALIDATED")
    expect(page.locator("[data-tmp36-disclosure] li")).to_have_count(7)
    expect(page.locator("[data-tmp36-method] bdi").first).to_have_text(
        "tmp36:nominal_voltage_to_temperature")
    verify = page.locator("[data-tmp36-verification]")
    expect(verify).to_be_visible()
    expect(verify.locator("[data-tmp36-verify-items] li")).to_have_count(5)
    expect(verify.locator("[data-tmp36-verify-boundary]")).to_have_text(
        text("UI_TMP36_VERIFY_BOUNDARY", lang))
    expect(verify.locator("[data-tmp36-verify-authority]")).to_have_text(
        text("UI_TMP36_VERIFY_AUTHORITY", lang))

    # the zero crossing, a negative temperature and a decimal fraction
    for typed, shown in (("500", "0.0 °C"), ("100", "-40.0 °C"), ("499.999", "-0.0001 °C"),
                         ("750.1", "25.01 °C")):
        _resubmit(page, typed)
        expect(page.locator("[data-tmp36-result-value]")).to_have_text(shown)

    # outside the nominal-model interval: one reason and no number
    _resubmit(page, "1750.001")
    expect(page.locator("[data-tmp36-outcome]")).to_have_count(1)
    expect(page.locator("[data-tmp36-result-value]")).to_have_count(0)
    expect(page.locator("[data-tmp36-verification]")).to_have_count(0)

    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator("[data-tmp36-form]").bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
        assert page.locator("#tmp36-v_out").get_attribute("dir") == "ltr"
        isolated = page.locator("label[for=tmp36-v_out] bdi[dir=ltr]").all_inner_texts()
        assert any("V_OUT" in run for run in isolated)
        assert any("mV" in run for run in isolated)
    assert not errors


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_tmp36_for_the_declared_electronics_part(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, lang, "mechanical")
    page.locator("[data-tmp36-link] a").click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/tmp36-temperature")
    expect(page.locator("[data-tmp36-part-name]")).to_have_text(ELEC_PART)
    _fill_and_submit(page, "400")
    expect(page.locator("[data-tmp36-result-value]")).to_have_text("-10.0 °C")
    expect(page.locator("[data-tmp36-part-name]")).to_have_text(ELEC_PART)
    _no_overflow(page, "[data-tmp36-part]")
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
