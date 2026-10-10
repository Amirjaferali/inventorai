"""Real Chromium + the existing Flask server: CAP13-THERM01-INTEGRATED-PART-01
(EN and AR).

Synthetic invention data only. An integrated Mechanical + Electrical /
Electronics invention is started through the real composition form, with each
initial analysis focus; the session page offers the calculation that belongs to
the OTHER declared part, the page names that part by its declared name with the
fixed attribution note, the calculation runs, and at phone width there is no
horizontal overflow. In Arabic the page is RTL and the part name is
direction-auto isolated.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401

TIE_IDEA = "circuit and hinge"
MECH_PART = "Hinge arm"
ELEC_PART = "لوحة تشغيل المحرك"          # an Arabic declared name on purpose
SUBMIT = "main input[type=submit], main button[type=submit]"


def _start_integrated(page, base, lang, focus):
    page.goto(base + "/")
    if lang == "ar":
        page.get_by_role("button", name="العربية", exact=True).click()
    page.fill("#idea", TIE_IDEA)
    offer = page.locator("input[type=checkbox][name=integrated_invention]")
    for _ in range(3):
        if page.locator("[data-composition-form]").count():
            break
        if offer.count():
            offer.check()
        page.click(SUBMIT)
        page.wait_for_load_state()
    form = page.locator("[data-composition-form]")
    expect(form).to_have_count(1)
    form.locator("input[name=composition_answer][value=yes]").check()
    page.fill("#mech_part_name", MECH_PART)
    page.fill("#mech_part_function", "Swings the window open and closed")
    page.fill("#elec_part_name", ELEC_PART)
    page.fill("#elec_part_function", "Switches battery power to the motor")
    form.locator("input[name=initial_focus][value=%s]" % focus).check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    assert "/session/" in page.url
    return page.url.rsplit("/session/", 1)[1].split("?")[0]


def _no_overflow(page, selector):
    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator(selector).bounding_box()["width"] <= width


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_electrical_focus_reaches_cap13_for_its_mechanical_part(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, lang, "electronics_electrical")
    link = page.locator("[data-cap13-link] a")
    expect(link).to_have_text(text("UI_CAP13_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/support-reactions")
    part = page.locator("[data-cap13-part]")
    expect(part).to_contain_text(text("UI_CAP13_PART_LABEL", lang))
    expect(part).to_contain_text(text("UI_CAP13_PART_NOTE", lang))
    name = page.locator("[data-cap13-part-name]")
    expect(name).to_have_text(MECH_PART)
    assert name.get_attribute("dir") == "auto"

    form = page.locator("[data-cap13-form]")
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
    reactions = page.locator("[data-cap13-reaction]")
    expect(reactions.nth(0)).to_have_text("750.0 N")
    expect(reactions.nth(1)).to_have_text("250.0 N")
    expect(page.locator("[data-cap13-part-name]")).to_have_text(MECH_PART)

    _no_overflow(page, "[data-cap13-part]")
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_mechanical_focus_reaches_therm01_for_its_electrical_part(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, lang, "mechanical")
    link = page.locator("[data-therm01-link] a")
    expect(link).to_have_text(text("UI_THERM01_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/temperature-difference")
    part = page.locator("[data-therm01-part]")
    expect(part).to_contain_text(text("UI_THERM01_PART_LABEL", lang))
    expect(part).to_contain_text(text("UI_THERM01_PART_NOTE", lang))
    name = page.locator("[data-therm01-part-name]")
    expect(name).to_have_text(ELEC_PART)
    assert name.get_attribute("dir") == "auto"

    form = page.locator("[data-therm01-form]")
    assert form.locator("input[type=radio]:checked").count() == 0
    for fieldset in form.locator("[data-therm01-declaration]").all():
        fieldset.locator("input[value=applies]").check()
    for fieldset in form.locator("[data-therm01-screen]").all():
        fieldset.locator("input[value=no]").check()
    page.fill("#therm01-P", "10")
    page.fill("#therm01-R_theta", "2.5")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-therm01-result-value]")).to_have_text("25.0 K")
    expect(page.locator("[data-therm01-part-name]")).to_have_text(ELEC_PART)

    _no_overflow(page, "[data-therm01-part]")
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
