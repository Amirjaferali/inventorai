# -*- coding: utf-8 -*-
"""Real Chromium + the existing Flask server: G1-SINGLE-DOMAIN-ENGINEERING-CONTINUATION-01 (EN, AR).

Synthetic data only. A single-domain Mechanical project is started through the real start form;
its questions are answered through the real answer form with ONE non-substantive Physical
Feasibility answer, so routed recovery is the Compass primary action. On a phone-width screen the
ONE secondary step opens the collapsed inventory so its form is usable; the inventor declares a
component there; the secondary step then leads to the existing moment page, where every
declaration, screen answer and value is entered by hand and the configuration is saved to a
component the inventor chooses; the existing report shows it and offers the PDF. Exactly one
primary action throughout; Arabic is RTL; no horizontal overflow at 390 px.
"""
import pytest
from playwright.sync_api import expect

from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_safe_question_routing_pf_q2 import MECH as MECH_ANSWER, BA_1, BA_2
from tests.test_safe_question_routing_pf_q2_weak_recovery import WEAK
from tests.test_safe_question_routing_pf_q2_weak_recovery_browser import _answer, _start_mechanical
from web.ui_text import text


def _no_overflow(page, selector):
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator(selector).first.bounding_box()["width"] <= width


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_blocked_point_to_component_to_saved_moment_and_report(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_mechanical(page, server, lang)
    for value in (MECH_ANSWER, MECH_ANSWER, WEAK, BA_1, BA_2):
        _answer(page, value)

    # Step A at phone width: one primary action, one secondary step to the existing form.
    page.set_viewport_size({"width": 390, "height": 900})
    page.goto(f"{server}/session/{sid}")
    primary = page.locator("[data-primary-action]")
    expect(primary).to_have_count(1)
    assert primary.get_attribute("href") == "#routed-recovery"
    block = page.locator("[data-rrc]")
    expect(block).to_have_count(1)
    expect(block.locator("[data-rrc-note]")).to_have_text(text("UI_SDC_NOTE_COMPONENTS", lang))
    link = block.locator("[data-rrc-link]")
    expect(link).to_have_text(text("UI_IJG_COMPONENTS_CTA", lang))
    assert link.get_attribute("data-primary-action") is None
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    _no_overflow(page, "[data-rrc]")
    link.click()
    name = page.locator("#component_name")
    expect(name).to_be_visible()
    expect(name).to_be_editable()
    name.fill("Long door handle")
    page.fill("#component_function", "Lever the user pushes down to turn around the pin")
    page.locator("[data-ci-form] button[type=submit]").click()
    page.wait_for_load_state()

    # Step B at desktop width: the same single secondary place now leads to the moment page.
    page.set_viewport_size({"width": 1280, "height": 900})
    page.goto(f"{server}/session/{sid}")
    expect(page.locator("[data-primary-action]")).to_have_count(1)
    block = page.locator("[data-rrc]")
    expect(block).to_have_count(1)
    expect(block.locator("[data-rrc-note]")).to_have_text(text("UI_SDC_NOTE_MOMENT", lang))
    link = block.locator("[data-rrc-link]")
    expect(link).to_have_text(text("UI_CAP13M_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/planar-moment")

    # Nothing is pre-selected: every declaration, screen answer and value is entered by hand.
    form = page.locator("[data-cap13m-form]")
    assert form.locator("input[type=radio]:checked").count() == 0
    for fieldset in form.locator("[data-cap13m-declaration]").all():
        fieldset.locator("input[value=applies]").check()
    for fieldset in form.locator("[data-cap13m-screen]").all():
        fieldset.locator("input[value=no]").check()
    page.fill("#cap13m-F", "20")
    page.fill("#cap13m-d_perp", "120")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-cap13m-result-value]")).to_have_text("2400.0 N·mm")
    save = page.locator("[data-pm-save-form]")
    target = save.locator("#pm-target")
    assert target.input_value() == ""                         # the component is the inventor's choice
    target.select_option(index=1)
    page.fill("#pm-point", "The pin the handle turns on")
    page.fill("#pm-force", "A person with weak hands pushing down on the far end")
    save.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-pm-saved] span.pm-state")).to_have_attribute("data-pm-state", "CURRENT")

    # The existing report carries the saved configuration and offers the PDF.
    page.goto(f"{server}/session/{sid}/deliverable")
    section = page.locator("[data-pm-report]")
    expect(section).to_have_count(1)
    expect(section.locator("[data-pm-result-value]")).to_have_text("2400.0 N·mm")
    expect(page.locator("form.pdf-download")).to_have_count(1)
    page.set_viewport_size({"width": 390, "height": 900})
    _no_overflow(page, "[data-pm-report]")
    assert not errors, errors
