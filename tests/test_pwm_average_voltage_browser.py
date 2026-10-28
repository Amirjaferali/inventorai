"""Real Chromium + the existing Flask server: Electrical / Electronics PWM
Average Voltage Slice 1 (EN and AR).

Synthetic data only. An Electrical / Electronics project is started through the
real forms; the optional link leads to the request-local page, every declaration
and screen item is answered explicitly (nothing is pre-selected), the inventor's
own declared supply level, on-time and period are typed, and the waveform average
V_avg = V_supply x t_on / T renders in the response itself in V, never negative,
labelled exact or rounded, with the statements that it is not an equivalent DC
voltage or a load response and must not be carried into the DC load
calculations, and the next engineering need. A refusal shows one reason and no
number. At phone width the page has no horizontal overflow; in Arabic it is RTL
and the numbers, unit tokens and role symbols stay direction-isolated.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_therm01_temperature_difference_browser import _start_electronics


def _answer_all(form):
    assert form.locator("input[type=radio]:checked").count() == 0
    for fieldset in form.locator("[data-pwm-declaration]").all():
        fieldset.locator("input[value=applies]").check()
    for fieldset in form.locator("[data-pwm-screen]").all():
        fieldset.locator("input[value=no]").check()


def _type(page, v, on, period):
    page.fill("#pwm-v_supply", v)
    page.fill("#pwm-t_on", on)
    page.fill("#pwm-t_period", period)


def _fill_and_submit(page, v, on, period):
    form = page.locator("[data-pwm-form]")
    _answer_all(form)
    _type(page, v, on, period)
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()


def _resubmit(page, v, on, period):
    _type(page, v, on, period)
    page.locator("[data-pwm-form] button[type=submit]").click()
    page.wait_for_load_state()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_pwm_average_journey_on_an_electronics_project(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    link = page.locator("[data-pwm-link] a")
    expect(link).to_have_text(text("UI_PWM_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/pwm-average-voltage")
    expect(page.locator("[data-pwm-form] input[type=radio]")).to_have_count(20)
    expect(page.locator("[data-pwm-value-note]")).to_be_visible()

    _fill_and_submit(page, "12", "0.25", "1")
    value = page.locator("[data-pwm-result-value]")
    expect(value).to_have_text("3 V")
    assert value.locator("bdi").get_attribute("dir") == "ltr"
    expect(page.locator("[data-pwm-exactness]")).to_have_attribute("data-pwm-exactness", "exact")
    expect(page.locator("[data-pwm-not-dc-equivalent]")).to_be_visible()
    expect(page.locator("[data-pwm-no-transfer]")).to_be_visible()
    expect(page.locator("[data-pwm-status]")).to_contain_text("UNVALIDATED")
    expect(page.locator("[data-pwm-disclosure] li")).to_have_count(7)
    no_transfer = text("UI_PWM_DISCLOSURE", lang).split("\n\n")[4]
    expect(page.locator("[data-pwm-disclosure] li").nth(4)).to_have_text(no_transfer)
    expect(page.locator("[data-pwm-method] bdi").first).to_have_text(
        "electrical:pwm_average_voltage")
    heading = page.locator("h1").inner_text()
    assert text("UI_PWM_TITLE", lang) == heading

    # the boundary cases: t_on = T gives exactly the supply level, t_on = 0 and
    # V_supply = 0 give exactly zero; a rounded result; the smallest average
    _resubmit(page, "24", "1", "1")
    expect(page.locator("[data-pwm-result-value]")).to_have_text("24 V")
    _resubmit(page, "12", "0", "1")
    expect(page.locator("[data-pwm-result-value]")).to_have_text("0 V")
    _resubmit(page, "0", "0.5", "1")
    expect(page.locator("[data-pwm-result-value]")).to_have_text("0 V")
    _resubmit(page, "5", "1", "3")
    expect(page.locator("[data-pwm-result-value]")).to_have_text("1.66666666667 V")
    expect(page.locator("[data-pwm-exactness]")).to_have_attribute(
        "data-pwm-exactness", "rounded")
    _resubmit(page, "0.000000001", "0.000000001", "999999999.999999999")
    expect(page.locator("[data-pwm-result-value]")).to_have_text("1 × 10^-27 V")

    # the refusals, each with one reason and no number, in the contracted order
    for v, on, period, outcome in (("-12", "0.25", "1", "VOLTAGE_NEGATIVE"),
                                   ("12", "0.25", "0", "PERIOD_NOT_POSITIVE"),
                                   ("12", "-0.25", "1", "ON_TIME_NEGATIVE"),
                                   ("12", "1.5", "1", "ON_TIME_EXCEEDS_PERIOD")):
        _resubmit(page, v, on, period)
        expect(page.locator("[data-pwm-outcome]")).to_have_count(1)
        expect(page.locator("[data-pwm-outcome]")).to_contain_text(
            text("UI_PWM_OUTCOME_" + outcome, lang))
        expect(page.locator("[data-pwm-result-value]")).to_have_count(0)

    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator("[data-pwm-form]").bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
        assert page.locator("#pwm-t_period").get_attribute("dir") == "ltr"
        isolated = page.locator("label[for=pwm-t_period] bdi[dir=ltr]").all_inner_texts()
        assert any("(s)" in run for run in isolated)
        assert any("(T)" in run for run in isolated)
        isolated = page.locator("label[for=pwm-v_supply] bdi[dir=ltr]").all_inner_texts()
        assert any("(V)" in run for run in isolated)
    assert not errors


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_pwm_mains_screen_requires_engineering_review(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    page.goto(f"{server}/session/{sid}/pwm-average-voltage")
    form = page.locator("[data-pwm-form]")
    _answer_all(form)
    form.locator("[data-pwm-screen=mains_or_high_voltage] input[value=yes]").check()
    _type(page, "12", "0.25", "1")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-pwm-outcome]")).to_contain_text(
        text("UI_PWM_OUTCOME_ENGINEERING_REVIEW_REQUIRED", lang))
    expect(page.locator("[data-pwm-result-value]")).to_have_count(0)
    assert not errors
