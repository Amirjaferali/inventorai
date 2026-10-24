"""Real Chromium + the existing Flask server: Stage 25 / CAP-13 Linear
Speed-Dependent Rotational Load Slice 1 (EN and AR).

Synthetic data only. A Mechanical project, and an Electrical / Electronics-focus
integrated project with a declared Mechanical part, are started through the real
forms; the optional link leads to the request-local page, every declaration and
screen item is answered explicitly (nothing is pre-selected), the inventor's own
values are typed (τ_nominal = -2 N·m at ω_nominal = 10 rad/s), and the signed
torque renders in the response itself with the sign convention. At phone width
the page has no horizontal overflow; in Arabic it is RTL and the numbers, unit
tokens and role symbols stay direction-isolated.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_safe_question_routing_pf_q2_weak_recovery_browser import (
    _start_mechanical,
)
from tests.test_cap13_therm01_integrated_part_browser import (
    _start_integrated, _no_overflow, MECH_PART)


def _fill_and_submit(page, w):
    form = page.locator("[data-cap13r-form]")
    assert form.locator("input[type=radio]:checked").count() == 0
    for fieldset in form.locator("[data-cap13r-declaration]").all():
        fieldset.locator("input[value=applies]").check()
    for fieldset in form.locator("[data-cap13r-screen]").all():
        fieldset.locator("input[value=no]").check()
    page.fill("#cap13r-tau_nominal", "-2")
    page.fill("#cap13r-w_nominal", "10")
    page.fill("#cap13r-w", w)
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_rotational_load_journey_on_a_mechanical_project(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_mechanical(page, server, lang)
    link = page.locator("[data-cap13r-link] a")
    expect(link).to_have_text(text("UI_CAP13R_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/rotational-load")
    expect(page.locator("[data-cap13r-form] input[type=radio]")).to_have_count(28)

    _fill_and_submit(page, "5")
    value = page.locator("[data-cap13r-result-value]")
    expect(value).to_have_text("-1.0 N·m")
    assert value.locator("bdi").get_attribute("dir") == "ltr"
    expect(page.locator("[data-cap13r-sign-note]")).to_have_text(
        text("UI_CAP13R_SIGN_NOTE", lang).replace("  ", " "), use_inner_text=True)
    expect(page.locator("[data-cap13r-status]")).to_contain_text("UNVALIDATED")
    expect(page.locator("[data-cap13r-disclosure] li")).to_have_count(7)
    expect(page.locator("[data-cap13r-method] bdi").first).to_have_text(
        "cap13:linear_speed_dependent_rotational_load")

    # negative rotation: the resisting torque is positive; zero speed: exactly zero
    page.fill("#cap13r-w", "-10")
    page.locator("[data-cap13r-form] button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-cap13r-result-value]")).to_have_text("2.0 N·m")
    page.fill("#cap13r-w", "0")
    page.locator("[data-cap13r-form] button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-cap13r-result-value]")).to_have_text("0.0 N·m")

    # a wrong-signed nominal torque shows one reason and no number
    page.fill("#cap13r-tau_nominal", "2")
    page.locator("[data-cap13r-form] button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-cap13r-outcome]")).to_have_count(1)
    expect(page.locator("[data-cap13r-result-value]")).to_have_count(0)

    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator("[data-cap13r-form]").bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
        assert page.locator("#cap13r-w").get_attribute("dir") == "ltr"
        isolated = page.locator("label[for=cap13r-tau_nominal] bdi[dir=ltr]").all_inner_texts()
        assert "τ_nominal" in isolated and "N·m" in isolated
    assert not errors


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_rotational_load_for_the_declared_mechanical_part(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, lang, "electronics_electrical")
    page.locator("[data-cap13r-link] a").click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/rotational-load")
    expect(page.locator("[data-cap13r-part-name]")).to_have_text(MECH_PART)
    _fill_and_submit(page, "-5")
    expect(page.locator("[data-cap13r-result-value]")).to_have_text("1.0 N·m")
    expect(page.locator("[data-cap13r-part-name]")).to_have_text(MECH_PART)
    _no_overflow(page, "[data-cap13r-part]")
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
