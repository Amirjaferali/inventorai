"""Real Chromium + the existing Flask server: MECHANICAL-NATURAL-FREQUENCY-01
Spring-Mass Natural Frequency Slice 1 (EN and AR).

Synthetic invention data only. A Mechanical project is started through the real
forms; the optional link leads to the request-local page, every declaration and
screen item is answered explicitly (nothing is pre-selected), the values are
typed, and the natural frequency renders in the response itself with its rounded
label and bounded next-step wording. At phone width the page has no horizontal
overflow; in Arabic it is RTL and the numbers, unit tokens and role symbols stay
direction-isolated. An integrated project with a Mechanical part names that part.
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


def _fill_and_submit(page, form, k, m):
    for fieldset in form.locator("[data-mnf-declaration]").all():
        fieldset.locator("input[value=applies]").check()
    for fieldset in form.locator("[data-mnf-screen]").all():
        fieldset.locator("input[value=no]").check()
    page.fill("#mnf-k", k)
    page.fill("#mnf-m", m)
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_natural_frequency_journey(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_mechanical(page, server, lang)
    link = page.locator("[data-mnf-link] a")
    expect(link).to_have_text(text("UI_MNF_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/natural-frequency")

    form = page.locator("[data-mnf-form]")
    radios = form.locator("input[type=radio]")
    expect(radios).to_have_count(32)  # 7 declarations + 9 screen items, two answers each
    assert form.locator("input[type=radio]:checked").count() == 0
    _fill_and_submit(page, form, "1000", "2.5")
    assert page.url.endswith(f"/session/{sid}/natural-frequency")

    value = page.locator("[data-mnf-result-value]")
    expect(value).to_have_count(1)
    expect(value).to_have_text("3.18309886184 Hz")
    assert value.locator("bdi").get_attribute("dir") == "ltr"
    expect(page.locator("[data-mnf-rounded]")).to_contain_text("12")
    expect(page.locator("[data-mnf-next-step]")).to_be_visible()
    expect(page.locator("[data-mnf-method] bdi").first).to_have_text(
        "mechanical:spring_mass_natural_frequency")
    expect(page.locator("[data-mnf-disclosure]")).to_be_visible()
    expect(page.locator("[data-mnf-disclosure] li")).to_have_count(7)
    expect(page.locator("[data-mnf-status]")).to_contain_text("UNVALIDATED")
    expect(page.locator("[data-mnf-sources]")).to_contain_text("Technical Note 487")

    # a declaration that does not apply shows one reason and no number
    form.locator("[data-mnf-declaration=damping_not_modelled] input[value=does_not_apply]").check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-mnf-outcome]")).to_have_count(1)
    expect(page.locator("[data-mnf-outcome]")).to_contain_text(
        text("UI_MNF_UNABLE_HEADING", lang).split(" (")[0])
    expect(page.locator("[data-mnf-result-value]")).to_have_count(0)

    # a zero mass is refused before any calculation
    form.locator("[data-mnf-declaration=damping_not_modelled] input[value=applies]").check()
    page.fill("#mnf-m", "0")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-mnf-outcome]")).to_have_count(1)
    expect(page.locator("[data-mnf-result-value]")).to_have_count(0)

    # layout: coherent at phone width, no horizontal overflow; RTL on Arabic
    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator("[data-mnf-form]").bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
        assert page.locator("#mnf-k").get_attribute("dir") == "ltr"
        isolated = page.locator("label[for=mnf-k] bdi[dir=ltr]")
        assert "N/m" in isolated.all_inner_texts()
        assert "k" in isolated.all_inner_texts()
    assert not errors


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_integrated_project_names_the_mechanical_part(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, lang, "electronics_electrical")
    link = page.locator("[data-mnf-link] a")
    expect(link).to_have_text(text("UI_MNF_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/natural-frequency")
    part = page.locator("[data-mnf-part]")
    expect(part).to_contain_text(text("UI_CAP13_PART_LABEL", lang))
    name = page.locator("[data-mnf-part-name]")
    expect(name).to_have_text(MECH_PART)
    assert name.get_attribute("dir") == "auto"
    form = page.locator("[data-mnf-form]")
    assert form.locator("input[type=radio]:checked").count() == 0
    _fill_and_submit(page, form, "1000", "2.5")
    expect(page.locator("[data-mnf-result-value]")).to_have_text("3.18309886184 Hz")
    expect(page.locator("[data-mnf-part-name]")).to_have_text(MECH_PART)
    _no_overflow(page, "[data-mnf-form]")
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
