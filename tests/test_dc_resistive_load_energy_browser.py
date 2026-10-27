"""Real Chromium + the existing Flask server: Electrical / Electronics DC
Resistive Load Energy Slice 1 (EN and AR).

Synthetic data only. An Electrical / Electronics project is started through the
real forms; the optional link leads to the request-local page, every declaration
and screen item is answered explicitly (nothing is pre-selected), the inventor's
own declared voltage, resistance and duration are typed, and the theoretical
absorbed energy renders in the response itself, never negative, labelled exact
or rounded, with the statement that it is not a battery capacity, a runtime or
a temperature and the next engineering need. A refusal shows one reason and no
number. At phone width the page has no horizontal overflow; in Arabic it is RTL
and the numbers, signs, unit tokens and role symbols stay direction-isolated.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_therm01_temperature_difference_browser import _start_electronics


def _answer_all(form):
    assert form.locator("input[type=radio]:checked").count() == 0
    for fieldset in form.locator("[data-dce-declaration]").all():
        fieldset.locator("input[value=applies]").check()
    for fieldset in form.locator("[data-dce-screen]").all():
        fieldset.locator("input[value=no]").check()


def _type(page, v, r, t):
    page.fill("#dce-v_load", v)
    page.fill("#dce-r_load", r)
    page.fill("#dce-t_duration", t)


def _fill_and_submit(page, v, r, t):
    form = page.locator("[data-dce-form]")
    _answer_all(form)
    _type(page, v, r, t)
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()


def _resubmit(page, v, r, t):
    _type(page, v, r, t)
    page.locator("[data-dce-form] button[type=submit]").click()
    page.wait_for_load_state()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_dc_load_energy_journey_on_an_electronics_project(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    link = page.locator("[data-dce-link] a")
    expect(link).to_have_text(text("UI_DCE_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/dc-load-energy")
    expect(page.locator("[data-dce-form] input[type=radio]")).to_have_count(22)
    expect(page.locator("[data-dce-value-note]")).to_be_visible()

    _fill_and_submit(page, "12", "24", "3600")
    value = page.locator("[data-dce-result-value]")
    expect(value).to_have_text("21600 J")
    assert value.locator("bdi").get_attribute("dir") == "ltr"
    expect(page.locator("[data-dce-exactness]")).to_have_attribute("data-dce-exactness", "exact")
    expect(page.locator("[data-dce-not-battery]")).to_be_visible()
    expect(page.locator("[data-dce-status]")).to_contain_text("UNVALIDATED")
    expect(page.locator("[data-dce-disclosure] li")).to_have_count(7)
    next_need = text("UI_DCE_DISCLOSURE", lang).split("\n\n")[5]
    expect(page.locator("[data-dce-disclosure] li").nth(5)).to_have_text(next_need)
    expect(page.locator("[data-dce-method] bdi").first).to_have_text(
        "electrical:dc_resistive_load_energy")

    # the second reference vector, a negative voltage (same energy), a zero
    # duration, a rounded result and the smallest representable energy
    _resubmit(page, "5", "10", "60")
    expect(page.locator("[data-dce-result-value]")).to_have_text("150 J")
    _resubmit(page, "-12", "24", "3600")
    expect(page.locator("[data-dce-result-value]")).to_have_text("21600 J")
    _resubmit(page, "12", "24", "0")
    expect(page.locator("[data-dce-result-value]")).to_have_text("0 J")
    _resubmit(page, "1", "3", "1")
    expect(page.locator("[data-dce-result-value]")).to_have_text("0.333333333333 J")
    expect(page.locator("[data-dce-exactness]")).to_have_attribute(
        "data-dce-exactness", "rounded")
    _resubmit(page, "0.000000001", "999999999999.999999999", "0.000000001")
    expect(page.locator("[data-dce-result-value]")).to_have_text("1 × 10^-39 J")

    # a negative duration: one reason and no number
    _resubmit(page, "12", "24", "-1")
    expect(page.locator("[data-dce-outcome]")).to_have_count(1)
    expect(page.locator("[data-dce-outcome]")).to_contain_text(
        text("UI_DCE_OUTCOME_DURATION_NEGATIVE", lang))
    expect(page.locator("[data-dce-result-value]")).to_have_count(0)

    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator("[data-dce-form]").bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
        assert page.locator("#dce-t_duration").get_attribute("dir") == "ltr"
        isolated = page.locator("label[for=dce-t_duration] bdi[dir=ltr]").all_inner_texts()
        assert any("(s)" in run for run in isolated)
        assert any("(t)" in run for run in isolated)
    assert not errors


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_dc_load_energy_battery_screen_requires_engineering_review(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    page.goto(f"{server}/session/{sid}/dc-load-energy")
    form = page.locator("[data-dce-form]")
    _answer_all(form)
    form.locator("[data-dce-screen=battery_or_storage_cell] input[value=yes]").check()
    _type(page, "12", "24", "3600")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-dce-outcome]")).to_contain_text(
        text("UI_DCE_OUTCOME_ENGINEERING_REVIEW_REQUIRED", lang))
    expect(page.locator("[data-dce-result-value]")).to_have_count(0)
    assert not errors
