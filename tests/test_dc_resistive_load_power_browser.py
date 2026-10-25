"""Real Chromium + the existing Flask server: Electrical / Electronics DC
Resistive Load Power Slice 1 (EN and AR).

Synthetic data only. An Electrical / Electronics project is started through the
real forms; the optional link leads to the request-local page, every declaration
and screen item is answered explicitly (nothing is pre-selected), the inventor's
own declared voltage and resistance are typed, and the theoretical absorbed
power renders in the response itself, never negative, labelled exact or
rounded, with the statement that it is not a temperature and the next
engineering need. A refusal shows one reason and no number. At phone width
the page has no horizontal overflow; in Arabic it is RTL and the numbers, signs,
unit tokens and role symbols stay direction-isolated.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_therm01_temperature_difference_browser import _start_electronics


def _fill_and_submit(page, v, r):
    form = page.locator("[data-dcp-form]")
    assert form.locator("input[type=radio]:checked").count() == 0
    for fieldset in form.locator("[data-dcp-declaration]").all():
        fieldset.locator("input[value=applies]").check()
    for fieldset in form.locator("[data-dcp-screen]").all():
        fieldset.locator("input[value=no]").check()
    page.fill("#dcp-v_load", v)
    page.fill("#dcp-r_load", r)
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()


def _resubmit(page, v, r):
    page.fill("#dcp-v_load", v)
    page.fill("#dcp-r_load", r)
    page.locator("[data-dcp-form] button[type=submit]").click()
    page.wait_for_load_state()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_dc_load_power_journey_on_an_electronics_project(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    link = page.locator("[data-dcp-link] a")
    expect(link).to_have_text(text("UI_DCP_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/dc-load-power")
    expect(page.locator("[data-dcp-form] input[type=radio]")).to_have_count(20)
    expect(page.locator("[data-dcp-value-note]")).to_be_visible()

    _fill_and_submit(page, "12", "24")
    value = page.locator("[data-dcp-result-value]")
    expect(value).to_have_text("6 W")
    assert value.locator("bdi").get_attribute("dir") == "ltr"
    expect(page.locator("[data-dcp-exactness]")).to_have_attribute("data-dcp-exactness", "exact")
    expect(page.locator("[data-dcp-not-temperature]")).to_be_visible()
    expect(page.locator("[data-dcp-status]")).to_contain_text("UNVALIDATED")
    expect(page.locator("[data-dcp-disclosure] li")).to_have_count(7)
    next_need = text("UI_DCP_DISCLOSURE", lang).split("\n\n")[5]
    expect(page.locator("[data-dcp-disclosure] li").nth(5)).to_have_text(next_need)
    expect(page.locator("[data-dcp-method] bdi").first).to_have_text(
        "electrical:dc_resistive_load_power")

    # the second reference vector, a negative voltage (same power), a rounded
    # result and the smallest representable power
    _resubmit(page, "5", "10")
    expect(page.locator("[data-dcp-result-value]")).to_have_text("2.5 W")
    _resubmit(page, "-12", "24")
    expect(page.locator("[data-dcp-result-value]")).to_have_text("6 W")
    _resubmit(page, "1", "3")
    expect(page.locator("[data-dcp-result-value]")).to_have_text("0.333333333333 W")
    expect(page.locator("[data-dcp-exactness]")).to_have_attribute(
        "data-dcp-exactness", "rounded")
    _resubmit(page, "0.000000001", "999999999999.999999999")
    expect(page.locator("[data-dcp-result-value]")).to_have_text("1 × 10^-30 W")
    _resubmit(page, "-0", "5")
    expect(page.locator("[data-dcp-result-value]")).to_have_text("0 W")

    # a zero resistance: one reason and no number
    _resubmit(page, "12", "0")
    expect(page.locator("[data-dcp-outcome]")).to_have_count(1)
    expect(page.locator("[data-dcp-outcome]")).to_contain_text(
        text("UI_DCP_OUTCOME_RESISTANCE_NOT_POSITIVE", lang))
    expect(page.locator("[data-dcp-result-value]")).to_have_count(0)

    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator("[data-dcp-form]").bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
        assert page.locator("#dcp-v_load").get_attribute("dir") == "ltr"
        isolated = page.locator("label[for=dcp-r_load] bdi[dir=ltr]").all_inner_texts()
        assert any("(Ω)" in run for run in isolated)
        assert any("(R)" in run for run in isolated)
    assert not errors


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_dc_load_power_refusal_with_engineering_review(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    page.goto(f"{server}/session/{sid}/dc-load-power")
    form = page.locator("[data-dcp-form]")
    for fieldset in form.locator("[data-dcp-declaration]").all():
        fieldset.locator("input[value=applies]").check()
    for fieldset in form.locator("[data-dcp-screen]").all():
        fieldset.locator("input[value=no]").check()
    form.locator("[data-dcp-screen=mains_or_high_voltage] input[value=yes]").check()
    page.fill("#dcp-v_load", "230")
    page.fill("#dcp-r_load", "50")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-dcp-outcome]")).to_contain_text(
        text("UI_DCP_OUTCOME_ENGINEERING_REVIEW_REQUIRED", lang))
    expect(page.locator("[data-dcp-result-value]")).to_have_count(0)
    assert not errors
