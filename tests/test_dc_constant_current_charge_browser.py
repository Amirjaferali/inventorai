"""Real Chromium + the existing Flask server: Electrical / Electronics DC
Constant-Current Charge Slice 1 (EN and AR).

Synthetic data only. An Electrical / Electronics project is started through the
real forms; the optional link leads to the request-local page, every declaration
and screen item is answered explicitly (nothing is pre-selected), the inventor's
own declared current and duration are typed, and the charge Q = I x t renders in
the response itself in A·h, never negative, labelled exact or rounded, with the
statements that it is a charge and not an energy, that it is not a battery
capacity, a runtime or a state of charge, and the next engineering need. A
refusal shows one reason and no number. At phone width the page has no
horizontal overflow; in Arabic it is RTL and the numbers, unit tokens and role
symbols stay direction-isolated.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_therm01_temperature_difference_browser import _start_electronics

FORBIDDEN = ("battery capacity needed", "battery requirement", "required capacity",
             "runtime requirement", "battery size")


def _answer_all(form):
    assert form.locator("input[type=radio]:checked").count() == 0
    for fieldset in form.locator("[data-dcq-declaration]").all():
        fieldset.locator("input[value=applies]").check()
    for fieldset in form.locator("[data-dcq-screen]").all():
        fieldset.locator("input[value=no]").check()


def _type(page, i, t):
    page.fill("#dcq-i_load", i)
    page.fill("#dcq-t_duration", t)


def _fill_and_submit(page, i, t):
    form = page.locator("[data-dcq-form]")
    _answer_all(form)
    _type(page, i, t)
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()


def _resubmit(page, i, t):
    _type(page, i, t)
    page.locator("[data-dcq-form] button[type=submit]").click()
    page.wait_for_load_state()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_dc_charge_journey_on_an_electronics_project(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    link = page.locator("[data-dcq-link] a")
    expect(link).to_have_text(text("UI_DCQ_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/dc-constant-current-charge")
    expect(page.locator("[data-dcq-form] input[type=radio]")).to_have_count(20)
    expect(page.locator("[data-dcq-value-note]")).to_be_visible()

    _fill_and_submit(page, "0.5", "4")
    value = page.locator("[data-dcq-result-value]")
    expect(value).to_have_text("2 A·h")
    assert value.locator("bdi").get_attribute("dir") == "ltr"
    expect(page.locator("[data-dcq-exactness]")).to_have_attribute("data-dcq-exactness", "exact")
    expect(page.locator("[data-dcq-charge-not-energy]")).to_be_visible()
    expect(page.locator("[data-dcq-not-battery]")).to_be_visible()
    expect(page.locator("[data-dcq-status]")).to_contain_text("UNVALIDATED")
    expect(page.locator("[data-dcq-disclosure] li")).to_have_count(7)
    next_need = text("UI_DCQ_DISCLOSURE", lang).split("\n\n")[5]
    expect(page.locator("[data-dcq-disclosure] li").nth(5)).to_have_text(next_need)
    expect(page.locator("[data-dcq-method] bdi").first).to_have_text(
        "electrical:dc_constant_current_charge")
    body = page.locator("body").inner_text().lower()
    for phrase in FORBIDDEN:
        assert phrase not in body, phrase

    # the other reference vectors, a zero duration, a rounded result and the
    # smallest representable charge; nothing is converted (1 A for 1 h is 1 A·h)
    _resubmit(page, "2", "1.5")
    expect(page.locator("[data-dcq-result-value]")).to_have_text("3 A·h")
    _resubmit(page, "1", "1")
    expect(page.locator("[data-dcq-result-value]")).to_have_text("1 A·h")
    _resubmit(page, "0.5", "0")
    expect(page.locator("[data-dcq-result-value]")).to_have_text("0 A·h")
    _resubmit(page, "1.234567891", "1.234567891")
    expect(page.locator("[data-dcq-result-value]")).to_have_text("1.52415787749 A·h")
    expect(page.locator("[data-dcq-exactness]")).to_have_attribute(
        "data-dcq-exactness", "rounded")
    _resubmit(page, "0.000000001", "0.000000001")
    expect(page.locator("[data-dcq-result-value]")).to_have_text("1 × 10^-18 A·h")

    # a negative current, then a negative duration: one reason each and no number
    _resubmit(page, "-0.5", "4")
    expect(page.locator("[data-dcq-outcome]")).to_have_count(1)
    expect(page.locator("[data-dcq-outcome]")).to_contain_text(
        text("UI_DCQ_OUTCOME_CURRENT_NEGATIVE", lang))
    expect(page.locator("[data-dcq-result-value]")).to_have_count(0)
    _resubmit(page, "0.5", "-4")
    expect(page.locator("[data-dcq-outcome]")).to_contain_text(
        text("UI_DCQ_OUTCOME_DURATION_NEGATIVE", lang))
    expect(page.locator("[data-dcq-result-value]")).to_have_count(0)

    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator("[data-dcq-form]").bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
        assert page.locator("#dcq-t_duration").get_attribute("dir") == "ltr"
        isolated = page.locator("label[for=dcq-t_duration] bdi[dir=ltr]").all_inner_texts()
        assert any("(h)" in run for run in isolated)
        assert any("(t)" in run for run in isolated)
        isolated = page.locator("label[for=dcq-i_load] bdi[dir=ltr]").all_inner_texts()
        assert any("(A)" in run for run in isolated)
    assert not errors


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_dc_charge_battery_screen_requires_engineering_review(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    page.goto(f"{server}/session/{sid}/dc-constant-current-charge")
    form = page.locator("[data-dcq-form]")
    _answer_all(form)
    form.locator("[data-dcq-screen=battery_or_storage_cell] input[value=yes]").check()
    _type(page, "0.5", "4")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-dcq-outcome]")).to_contain_text(
        text("UI_DCQ_OUTCOME_ENGINEERING_REVIEW_REQUIRED", lang))
    expect(page.locator("[data-dcq-result-value]")).to_have_count(0)
    assert not errors
