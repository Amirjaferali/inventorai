"""Real Chromium + the existing Flask server: MECHANICAL-FREE-LINEAR-THERMAL-EXPANSION-01
Free Linear Thermal Expansion Slice 1 (EN and AR).

Synthetic invention data only. A Mechanical project is started through the real
forms; the optional link leads to the request-local page, every declaration and
screen item is answered explicitly (nothing is pre-selected and no coefficient is
suggested), the values are typed, and the free change in length renders in the
response itself with its exact label, sign note and bounded next-step wording.
At phone width the page has no horizontal overflow; in Arabic it is RTL and the
numbers, unit tokens and role symbols stay direction-isolated. An integrated
project with a Mechanical part names that part.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_safe_question_routing_pf_q2_weak_recovery_browser import (
    _start_mechanical,
)
from tests.test_cap13_therm01_integrated_part_browser import (
    _no_overflow, _start_integrated, MECH_PART)


def _fill_and_submit(page, form, alpha, length, delta_t):
    for fieldset in form.locator("[data-mte-declaration]").all():
        fieldset.locator("input[value=applies]").check()
    for fieldset in form.locator("[data-mte-screen]").all():
        fieldset.locator("input[value=no]").check()
    page.fill("#mte-alpha_avg", alpha)
    page.fill("#mte-L_ref", length)
    page.fill("#mte-delta_T", delta_t)
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_thermal_expansion_journey(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_mechanical(page, server, lang)
    link = page.locator("[data-mte-link] a")
    expect(link).to_have_text(text("UI_MTE_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/thermal-expansion")

    form = page.locator("[data-mte-form]")
    radios = form.locator("input[type=radio]")
    expect(radios).to_have_count(34)  # 8 declarations + 9 screen items, two answers each
    assert form.locator("input[type=radio]:checked").count() == 0
    for role in ("alpha_avg", "L_ref", "delta_T"):
        assert page.locator("#mte-%s" % role).input_value() == ""
        expect(page.locator("[data-mte-field-help=%s]" % role)).to_be_visible()
    _fill_and_submit(page, form, "0.0000231", "1000", "50")
    assert page.url.endswith(f"/session/{sid}/thermal-expansion")

    value = page.locator("[data-mte-result-value]")
    expect(value).to_have_count(1)
    expect(value).to_have_text("1.155 mm")
    assert value.locator("bdi").get_attribute("dir") == "ltr"
    expect(page.locator("[data-mte-exact]")).to_be_visible()
    expect(page.locator("[data-mte-sign]")).to_be_visible()
    expect(page.locator("[data-mte-next-step]")).to_be_visible()
    expect(page.locator("[data-mte-method] bdi").first).to_have_text(
        "mechanical:free_linear_thermal_expansion")
    expect(page.locator("[data-mte-disclosure] li")).to_have_count(7)
    expect(page.locator("[data-mte-status]")).to_contain_text("UNVALIDATED")
    expect(page.locator("[data-mte-sources]")).to_contain_text("Circular 486")

    # cooling gives a negative change
    page.fill("#mte-delta_T", "-50")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-mte-result-value]")).to_have_text("-1.155 mm")

    # a declaration that does not apply shows one reason and no number
    form.locator("[data-mte-declaration=free_unrestrained] input[value=does_not_apply]").check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-mte-outcome]")).to_have_count(1)
    expect(page.locator("[data-mte-outcome]")).to_contain_text(
        text("UI_MTE_UNABLE_HEADING", lang).split(" (")[0])
    expect(page.locator("[data-mte-result-value]")).to_have_count(0)

    # a coefficient written with an exponent is refused before any calculation
    form.locator("[data-mte-declaration=free_unrestrained] input[value=applies]").check()
    page.fill("#mte-alpha_avg", "2.3e-5")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-mte-outcome]")).to_have_count(1)
    expect(page.locator("[data-mte-result-value]")).to_have_count(0)

    # layout: coherent at phone width, no horizontal overflow; RTL on Arabic
    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator("[data-mte-form]").bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
        assert page.locator("#mte-alpha_avg").get_attribute("dir") == "ltr"
        isolated = page.locator("label[for=mte-alpha_avg] bdi[dir=ltr]")
        assert "1/K" in isolated.all_inner_texts()
        assert "α_avg" in isolated.all_inner_texts()
    assert not errors


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_integrated_project_names_the_mechanical_part(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, lang, "electronics_electrical")
    link = page.locator("[data-mte-link] a")
    expect(link).to_have_text(text("UI_MTE_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/thermal-expansion")
    part = page.locator("[data-mte-part]")
    expect(part).to_contain_text(text("UI_CAP13_PART_LABEL", lang))
    name = page.locator("[data-mte-part-name]")
    expect(name).to_have_text(MECH_PART)
    assert name.get_attribute("dir") == "auto"
    form = page.locator("[data-mte-form]")
    assert form.locator("input[type=radio]:checked").count() == 0
    _fill_and_submit(page, form, "0.0000231", "1000", "50")
    expect(page.locator("[data-mte-result-value]")).to_have_text("1.155 mm")
    expect(page.locator("[data-mte-part-name]")).to_have_text(MECH_PART)
    _no_overflow(page, "[data-mte-form]")
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
