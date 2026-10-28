"""Real Chromium + the existing Flask server: CONTROL-CYCLE-INTEGRATED-PART-01
(EN and AR).

Synthetic invention data only. An integrated Mechanical + Electrical /
Electronics invention with a MECHANICAL initial focus is started through the
real composition form; the session page offers the READY / RUNNING control-cycle
evaluation and the TMP36 -> threshold -> cycle composition for the declared
Electrical / Electronics part; each page names that part by its declared name
with the fixed attribution note, nothing is pre-selected, the cycle gives the
same result as on an Electronics root, and at phone width (390 px) there is no
horizontal overflow. In Arabic the page is RTL and the part name is
direction-auto isolated.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import (
    ELEC_PART, _no_overflow, _start_integrated)


def _check_part(page, prefix, lang):
    part = page.locator("[data-%s-part]" % prefix)
    expect(part).to_contain_text(text("UI_THERM01_PART_LABEL", lang))
    expect(part).to_contain_text(text("UI_%s_PART_NOTE" % prefix.upper(), lang))
    name = page.locator("[data-%s-part-name]" % prefix)
    expect(name).to_have_text(ELEC_PART)
    assert name.get_attribute("dir") == "auto"


def _answer_fieldsets(form, declaration_selectors, screen_selectors):
    assert form.locator("input[type=radio]:checked").count() == 0
    for selector in declaration_selectors:
        for fieldset in form.locator(selector).all():
            fieldset.locator("input[value=applies]").check()
    for selector in screen_selectors:
        for fieldset in form.locator(selector).all():
            fieldset.locator("input[value=no]").check()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_mechanical_focus_reaches_the_cycle_pages_for_its_electrical_part(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, lang, "mechanical")
    session_url = page.url

    # 28-T4: READY with start_input true -> RUNNING, output true
    link = page.locator("[data-cc-link] a")
    expect(link).to_have_text(text("UI_CC_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith("/session/%s/control-cycle" % sid)
    _check_part(page, "cc", lang)
    form = page.locator("[data-cc-form]")
    _answer_fieldsets(form, ("[data-cc-declaration]",), ("[data-cc-screen]",))
    form.locator("[data-cc-previous] input[value=READY]").check()
    form.locator("[data-cc-input] input[value=true]").check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-cc-result-next]")).to_have_text("RUNNING")
    expect(page.locator("[data-cc-result-output]")).to_have_text("true")
    expect(page.locator("[data-cc-status]")).to_contain_text("UNVALIDATED")
    _check_part(page, "cc", lang)
    _no_overflow(page, "[data-cc-form]")
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"

    # the composition: 750 mV -> 25 °C >= 25 °C -> start_input true -> RUNNING
    page.set_viewport_size({"width": 1200, "height": 900})
    page.goto(session_url)
    link = page.locator("[data-tcc-link] a")
    expect(link).to_have_text(text("UI_TCC_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith("/session/%s/temperature-control-condition" % sid)
    _check_part(page, "tcc", lang)
    form = page.locator("[data-tcc-form]")
    _answer_fieldsets(form, ("[data-tcc-tmp36-declaration]", "[data-tcc-cc-declaration]",
                             "[data-tcc-condition-declaration]"),
                      ("[data-tcc-tmp36-screen]", "[data-tcc-cc-screen]"))
    page.fill("#tcc-v_out", "750")
    page.fill("#tcc-threshold", "25")
    form.locator("[data-tcc-previous] input[value=READY]").check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    assert page.locator("[data-tcc-result-condition]").get_attribute("data-tcc-condition") == "true"
    expect(page.locator("[data-tcc-result-next]")).to_have_text("RUNNING")
    expect(page.locator("[data-tcc-result-output]")).to_have_text("true")
    expect(page.locator("[data-tcc-status]")).to_contain_text("UNVALIDATED")
    _check_part(page, "tcc", lang)
    _no_overflow(page, "[data-tcc-form]")
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_electronics_focus_integrated_pages_name_the_part(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, lang, "electronics_electrical")
    # an Electronics-FOCUS integrated project names the part for attribution
    page.goto("%s/session/%s/control-cycle" % (server, sid))
    expect(page.locator("[data-cc-form]")).to_have_count(1)
    _check_part(page, "cc", lang)
    page.goto("%s/session/%s/temperature-control-condition" % (server, sid))
    expect(page.locator("[data-tcc-form]")).to_have_count(1)
    _check_part(page, "tcc", lang)
    assert not errors
