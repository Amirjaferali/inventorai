"""Real Chromium + the existing Flask server: Electrical / Electronics DC
Resistive Load Current Slice 1 (EN and AR).

Synthetic data only. An Electrical / Electronics project is started through the
real forms; the optional link leads to the request-local page, every declaration
and screen item is answered explicitly (nothing is pre-selected), the inventor's
own declared voltage and resistance are typed, and the theoretical current
renders in the response itself, signed, labelled exact or rounded, with the
next engineering need. A refusal shows one reason and no number. At phone width
the page has no horizontal overflow; in Arabic it is RTL and the numbers, signs,
unit tokens and role symbols stay direction-isolated.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_therm01_temperature_difference_browser import _start_electronics


def _fill_and_submit(page, v, r):
    form = page.locator("[data-dcl-form]")
    assert form.locator("input[type=radio]:checked").count() == 0
    for fieldset in form.locator("[data-dcl-declaration]").all():
        fieldset.locator("input[value=applies]").check()
    for fieldset in form.locator("[data-dcl-screen]").all():
        fieldset.locator("input[value=no]").check()
    page.fill("#dcl-v_load", v)
    page.fill("#dcl-r_load", r)
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()


def _resubmit(page, v, r):
    page.fill("#dcl-v_load", v)
    page.fill("#dcl-r_load", r)
    page.locator("[data-dcl-form] button[type=submit]").click()
    page.wait_for_load_state()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_dc_load_current_journey_on_an_electronics_project(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    link = page.locator("[data-dcl-link] a")
    expect(link).to_have_text(text("UI_DCL_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/dc-load-current")
    expect(page.locator("[data-dcl-form] input[type=radio]")).to_have_count(20)
    expect(page.locator("[data-dcl-value-note]")).to_be_visible()

    _fill_and_submit(page, "12", "24")
    value = page.locator("[data-dcl-result-value]")
    expect(value).to_have_text("0.5 A")
    assert value.locator("bdi").get_attribute("dir") == "ltr"
    expect(page.locator("[data-dcl-exactness]")).to_have_attribute("data-dcl-exactness", "exact")
    expect(page.locator("[data-dcl-magnitude]")).to_have_count(0)
    expect(page.locator("[data-dcl-status]")).to_contain_text("UNVALIDATED")
    expect(page.locator("[data-dcl-disclosure] li")).to_have_count(7)
    next_need = text("UI_DCL_DISCLOSURE", lang).split("\n\n")[5]
    expect(page.locator("[data-dcl-disclosure] li").nth(5)).to_have_text(next_need)
    expect(page.locator("[data-dcl-method] bdi").first).to_have_text(
        "electrical:dc_resistive_load_current")

    # the second reference vector, a signed negative current and a nonterminating quotient
    _resubmit(page, "5", "10")
    expect(page.locator("[data-dcl-result-value]")).to_have_text("0.5 A")
    _resubmit(page, "-12", "24")
    expect(page.locator("[data-dcl-result-value]")).to_have_text("-0.5 A")
    expect(page.locator("[data-dcl-magnitude]")).to_have_text("0.5 A")
    _resubmit(page, "1", "3")
    expect(page.locator("[data-dcl-result-value]")).to_have_text("0.333333333333 A")
    expect(page.locator("[data-dcl-exactness]")).to_have_attribute(
        "data-dcl-exactness", "rounded")
    _resubmit(page, "0.000000001", "999999999999.999999999")
    expect(page.locator("[data-dcl-result-value]")).to_have_text("1 × 10^-21 A")

    # a zero resistance: one reason and no number
    _resubmit(page, "12", "0")
    expect(page.locator("[data-dcl-outcome]")).to_have_count(1)
    expect(page.locator("[data-dcl-outcome]")).to_contain_text(
        text("UI_DCL_OUTCOME_RESISTANCE_NOT_POSITIVE", lang))
    expect(page.locator("[data-dcl-result-value]")).to_have_count(0)

    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator("[data-dcl-form]").bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
        assert page.locator("#dcl-v_load").get_attribute("dir") == "ltr"
        isolated = page.locator("label[for=dcl-r_load] bdi[dir=ltr]").all_inner_texts()
        assert any("(Ω)" in run for run in isolated)
        assert any("(R)" in run for run in isolated)
    assert not errors


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_dc_load_current_refusal_with_engineering_review(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    page.goto(f"{server}/session/{sid}/dc-load-current")
    form = page.locator("[data-dcl-form]")
    for fieldset in form.locator("[data-dcl-declaration]").all():
        fieldset.locator("input[value=applies]").check()
    for fieldset in form.locator("[data-dcl-screen]").all():
        fieldset.locator("input[value=no]").check()
    form.locator("[data-dcl-screen=mains_or_high_voltage] input[value=yes]").check()
    page.fill("#dcl-v_load", "230")
    page.fill("#dcl-r_load", "50")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-dcl-outcome]")).to_contain_text(
        text("UI_DCL_OUTCOME_ENGINEERING_REVIEW_REQUIRED", lang))
    expect(page.locator("[data-dcl-result-value]")).to_have_count(0)
    assert not errors
