"""Real Chromium + the existing Flask server: Stage 25 / CAP-13 Two-Support
Static Reactions Slice 1 (EN and AR).

Synthetic invention data only. A Mechanical project is started through the real
forms; the optional link leads to the request-local page, every declaration and
screen item is answered explicitly (nothing is pre-selected), the values are
typed, and the reactions render in the response itself. At phone width the
page has no horizontal overflow; in Arabic it is RTL and the numbers, unit
tokens and role symbols stay direction-isolated.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_safe_question_routing_pf_q2_weak_recovery_browser import (
    _start_mechanical,
)


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_support_reactions_journey(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_mechanical(page, server, lang)
    link = page.locator("[data-cap13-link] a")
    expect(link).to_have_text(text("UI_CAP13_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/support-reactions")

    form = page.locator("[data-cap13-form]")
    radios = form.locator("input[type=radio]")
    expect(radios).to_have_count(38)
    assert form.locator("input[type=radio]:checked").count() == 0
    for fieldset in form.locator("[data-cap13-declaration]").all():
        fieldset.locator("input[value=matches]").check()
    for fieldset in form.locator("[data-cap13-screen]").all():
        fieldset.locator("input[value=no]").check()
    page.fill("#cap13-P", "1000")
    page.fill("#cap13-L", "2000")
    page.fill("#cap13-x", "500")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/support-reactions")

    reactions = page.locator("[data-cap13-reaction]")
    expect(reactions).to_have_count(2)
    expect(reactions.nth(0)).to_have_text("750.0 N")
    expect(reactions.nth(1)).to_have_text("250.0 N")
    assert reactions.nth(0).locator("bdi").get_attribute("dir") == "ltr"
    expect(page.locator("[data-cap13-method] bdi").first).to_have_text(
        "cap13:static_reactions_two_support")
    expect(page.locator("[data-cap13-disclosure]")).to_be_visible()
    expect(page.locator("[data-cap13-status]")).to_contain_text("UNVALIDATED")

    # a refusal shows one reason and no number
    page.fill("#cap13-x", "2500")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-cap13-outcome]")).to_have_count(1)
    expect(page.locator("[data-cap13-reaction]")).to_have_count(0)

    # layout: coherent at phone width, no horizontal overflow; RTL on Arabic
    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator("[data-cap13-form]").bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
        assert page.locator("#cap13-x").get_attribute("dir") == "ltr"
        iso = page.locator("label[for=cap13-P] bdi[dir=ltr]")
        expect(iso).to_have_text("N")
    assert not errors
