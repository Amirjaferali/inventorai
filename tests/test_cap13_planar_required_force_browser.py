"""Real Chromium + the existing Flask server: CAP13-PLANAR-REQUIRED-FORCE-01,
Planar Required Force Slice 1 (EN and AR).

Synthetic invention data only. A Mechanical project is started through the real
forms; the optional link leads to the request-local page, every declaration and
screen item is answered explicitly (nothing is pre-selected), the target moment
and distance are typed, and the force renders in the response itself with its
exact / rounded label. A zero distance shows one reason and no number. At phone
width the page has no horizontal overflow; in Arabic it is RTL and the numbers,
unit tokens and role symbols stay direction-isolated.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_safe_question_routing_pf_q2_weak_recovery_browser import (
    _start_mechanical,
)


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_planar_required_force_journey(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_mechanical(page, server, lang)
    link = page.locator("[data-cap13f-link] a")
    expect(link).to_have_text(text("UI_CAP13F_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/planar-required-force")

    form = page.locator("[data-cap13f-form]")
    radios = form.locator("input[type=radio]")
    expect(radios).to_have_count(30)  # 6 declarations + 9 screen items, two answers each
    assert form.locator("input[type=radio]:checked").count() == 0
    for fieldset in form.locator("[data-cap13f-declaration]").all():
        fieldset.locator("input[value=applies]").check()
    for fieldset in form.locator("[data-cap13f-screen]").all():
        fieldset.locator("input[value=no]").check()
    page.fill("#cap13f-M_target", "1000")
    page.fill("#cap13f-d_perp", "3")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/planar-required-force")

    value = page.locator("[data-cap13f-result-value]")
    expect(value).to_have_count(1)
    expect(value).to_have_text("333.333333333 N")
    assert value.locator("bdi").get_attribute("dir") == "ltr"
    expect(page.locator("[data-cap13f-exactness]")).to_have_attribute(
        "data-cap13f-exactness", "rounded")
    expect(page.locator("[data-cap13f-method] bdi").first).to_have_text(
        "cap13:planar_required_force")
    expect(page.locator("[data-cap13f-disclosure]")).to_be_visible()
    expect(page.locator("[data-cap13f-disclosure] li")).to_have_count(7)
    expect(page.locator("[data-cap13f-status]")).to_contain_text("UNVALIDATED")

    # a zero distance shows one reason and no number
    page.fill("#cap13f-d_perp", "0")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-cap13f-outcome]")).to_have_count(1)
    expect(page.locator("[data-cap13f-outcome]")).to_contain_text(
        text("UI_CAP13F_UNABLE_HEADING", lang).split(" (")[0])
    expect(page.locator("[data-cap13f-result-value]")).to_have_count(0)

    # layout: coherent at phone width, no horizontal overflow; RTL on Arabic
    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator("[data-cap13f-form]").bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
        assert page.locator("#cap13f-d_perp").get_attribute("dir") == "ltr"
        isolated = page.locator("label[for=cap13f-d_perp] bdi[dir=ltr]")
        assert "mm" in isolated.all_inner_texts()
        assert "d⊥" in isolated.all_inner_texts()
        isolated = page.locator("label[for=cap13f-M_target] bdi[dir=ltr]")
        assert "M_target" in isolated.all_inner_texts()
        assert "N·mm" in isolated.all_inner_texts()
    assert not errors
