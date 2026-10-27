"""Real Chromium + the existing Flask server: CAP13-PLANAR-MOMENT-INTEGRATED-PART-01
(EN and AR).

Synthetic invention data only. An integrated Mechanical + Electrical /
Electronics invention is started through the real composition form with an
Electrical / Electronics initial analysis focus; the session page offers the
planar moment for the declared Mechanical part, the page names that part by its
declared name with the fixed attribution note, nothing is pre-selected, the
calculation runs on the inventor's own values, and at phone width there is no
horizontal overflow. In Arabic the page is RTL and the part name is
direction-auto isolated.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import (
    _start_integrated, _no_overflow, MECH_PART)


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_electrical_focus_reaches_the_moment_for_its_mechanical_part(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, lang, "electronics_electrical")
    link = page.locator("[data-cap13m-link] a")
    expect(link).to_have_text(text("UI_CAP13M_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/planar-moment")
    part = page.locator("[data-cap13m-part]")
    expect(part).to_contain_text(text("UI_CAP13_PART_LABEL", lang))
    expect(part).to_contain_text(text("UI_CAP13_PART_NOTE", lang))
    name = page.locator("[data-cap13m-part-name]")
    expect(name).to_have_text(MECH_PART)
    assert name.get_attribute("dir") == "auto"

    form = page.locator("[data-cap13m-form]")
    assert form.locator("input[type=radio]:checked").count() == 0
    assert page.input_value("#cap13m-F") == "" and page.input_value("#cap13m-d_perp") == ""
    for fieldset in form.locator("[data-cap13m-declaration]").all():
        fieldset.locator("input[value=applies]").check()
    for fieldset in form.locator("[data-cap13m-screen]").all():
        fieldset.locator("input[value=no]").check()
    page.fill("#cap13m-F", "12.5")
    page.fill("#cap13m-d_perp", "80")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-cap13m-result-value]")).to_have_text("1000.0 N·mm")
    expect(page.locator("[data-cap13m-status]")).to_contain_text("UNVALIDATED")
    expect(page.locator("[data-cap13m-disclosure] li")).to_have_count(7)
    expect(page.locator("[data-cap13m-part-name]")).to_have_text(MECH_PART)

    _no_overflow(page, "[data-cap13m-part]")
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
