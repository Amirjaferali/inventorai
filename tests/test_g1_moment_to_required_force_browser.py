# -*- coding: utf-8 -*-
"""G1-MOMENT-TO-REQUIRED-FORCE-01 - the real journey in Chromium against the real Flask server, EN / AR.

A Mechanical project is started through the real forms; the inventor declares a component, calculates and saves
one planar moment for it, follows the step from that CURRENT saved configuration, sees P (the exact product of the
saved inputs) and the computed moment M as two separate figures, is refused until BOTH confirmations are ticked
(nothing is pre-selected), answers every declaration and screen item, types d⊥ and gets the force size from the
unchanged required-force calculation. At phone width there is no horizontal overflow; Arabic is right-to-left with
the numbers and unit tokens direction-isolated. Synthetic data only.
"""
import pytest
from playwright.sync_api import expect

from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_safe_question_routing_pf_q2_weak_recovery_browser import _start_mechanical
from web.ui_text import text


def _declare_component(page, server, sid):
    page.goto(f"{server}/session/{sid}")
    page.wait_for_load_state()
    page.evaluate("document.getElementById('component-inventory').open = true")
    form = page.locator("[data-ci-form]")
    form.locator("#component_name").fill("Folding flap")
    form.locator("#component_function").fill("Covers the opening")
    form.locator("button[type=submit], input[type=submit]").first.click()
    page.wait_for_load_state()


def _answer_all(form, decl_attr, screen_attr):
    for fieldset in form.locator(decl_attr).all():
        fieldset.locator("input[value=applies]").check()
    for fieldset in form.locator(screen_attr).all():
        fieldset.locator("input[value=no]").check()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_saved_moment_to_required_force_journey(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_mechanical(page, server, lang)
    _declare_component(page, server, sid)

    # calculate and save one planar moment for the component
    page.goto(f"{server}/session/{sid}/planar-moment")
    page.wait_for_load_state()
    form = page.locator("[data-cap13m-form]")
    _answer_all(form, "[data-cap13m-declaration]", "[data-cap13m-screen]")
    page.fill("#cap13m-F", "12.5")
    page.fill("#cap13m-d_perp", "80")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    save = page.locator("[data-pm-save-form]")
    save.locator("[data-pm-target]").select_option(index=1)
    save.locator("[data-pm-point]").fill("The hinge pin at the lower edge of the flap")
    save.locator("[data-pm-force]").fill("A hand pressing down on the far corner")
    save.locator("button[type=submit]").click()
    page.wait_for_load_state()

    # the step is offered from the CURRENT saved configuration
    link = page.locator("[data-pm-required-force]")
    expect(link).to_have_count(1)
    expect(link).to_have_text(text("UI_PMF_LINK", lang))
    link.click()
    page.wait_for_load_state()
    assert f"/session/{sid}/planar-moment/pmd-" in page.url and page.url.endswith("/required-force?head=0")
    expect(page.locator("[data-pmf-product]")).to_have_text("1000 N·mm")
    expect(page.locator("[data-pmf-computed-moment]")).to_have_text("1000.0 N·mm")
    step = page.locator("[data-pmf-form]")
    assert step.locator("input:checked").count() == 0                   # nothing pre-selected
    assert step.locator("input[name=value_M_target]").count() == 0      # the target is not typed

    # without the confirmations nothing is calculated
    _answer_all(step, "[data-pmf-declaration]", "[data-pmf-screen]")
    page.fill("#pmf-d_perp", "250")
    step.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-pmf-error]")).to_have_text(text("UI_PMF_MSG_NOT_CONFIRMED", lang))
    expect(page.locator("[data-pmf-result-value]")).to_have_count(0)

    # with both confirmations: the unchanged required-force result
    step = page.locator("[data-pmf-form]")
    for field in ("confirm_same_point", "confirm_size_only"):
        step.locator(f"[data-pmf-confirm={field}]").check()
    step.locator("button[type=submit]").click()
    page.wait_for_load_state()
    value = page.locator("[data-pmf-result-value]")
    expect(value).to_have_text("4 N")
    assert value.locator("bdi").get_attribute("dir") == "ltr"
    expect(page.locator("[data-pmf-transfer-disclosure]")).to_be_visible()
    expect(page.locator("[data-pmf-status]")).to_contain_text("UNVALIDATED")

    # layout: no horizontal overflow at phone width; RTL in Arabic
    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator("[data-pmf-form]").bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
        assert page.locator("[data-pmf-product]").get_attribute("dir") == "ltr"
        assert page.locator("#pmf-d_perp").get_attribute("dir") == "ltr"
    assert not errors
