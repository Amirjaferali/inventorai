"""Real Chromium + the existing Flask server: DC-RESISTIVE-LOAD-INTEGRATED-PART-01
(EN and AR).

Synthetic invention data only. An integrated Mechanical + Electrical /
Electronics invention with a MECHANICAL initial focus is started through the
real composition form; the session page offers each of the three DC resistive
load calculations for the declared Electrical / Electronics part, each page
names that part by its declared name with the fixed attribution note, nothing
is pre-selected, the calculation returns the same value as on an Electronics
root, and at phone width (390 px) there is no horizontal overflow. In Arabic the
page is RTL and the part name is direction-auto isolated.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import (
    ELEC_PART, _no_overflow, _start_integrated)

CALCS = (
    ("dcl", "dc-load-current", {"v_load": "12", "r_load": "24"}, "0.5 A"),
    ("dcp", "dc-load-power", {"v_load": "12", "r_load": "24"}, "6 W"),
    ("dce", "dc-load-energy", {"v_load": "12", "r_load": "24", "t_duration": "3600"},
     "21600 J"),
)


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_mechanical_focus_reaches_the_dc_load_pages_for_its_electrical_part(
        server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, lang, "mechanical")
    session_url = page.url
    for prefix, route, values, expected in CALCS:
        page.goto(session_url)
        link = page.locator("[data-%s-link] a" % prefix)
        expect(link).to_have_text(text("UI_%s_LINK_TEXT" % prefix.upper(), lang))
        link.click()
        page.wait_for_load_state()
        assert page.url.endswith("/session/%s/%s" % (sid, route))
        part = page.locator("[data-%s-part]" % prefix)
        expect(part).to_contain_text(text("UI_THERM01_PART_LABEL", lang))
        expect(part).to_contain_text(text("UI_THERM01_PART_NOTE", lang))
        name = page.locator("[data-%s-part-name]" % prefix)
        expect(name).to_have_text(ELEC_PART)
        assert name.get_attribute("dir") == "auto"

        form = page.locator("[data-%s-form]" % prefix)
        assert form.locator("input[type=radio]:checked").count() == 0
        for fieldset in form.locator("[data-%s-declaration]" % prefix).all():
            fieldset.locator("input[value=applies]").check()
        for fieldset in form.locator("[data-%s-screen]" % prefix).all():
            fieldset.locator("input[value=no]").check()
        for role, value in values.items():
            page.fill("#%s-%s" % (prefix, role), value)
        form.locator("button[type=submit]").click()
        page.wait_for_load_state()
        expect(page.locator("[data-%s-result-value]" % prefix)).to_have_text(expected)
        expect(page.locator("[data-%s-part-name]" % prefix)).to_have_text(ELEC_PART)

        _no_overflow(page, "[data-%s-part]" % prefix)
        assert page.locator("html").get_attribute("lang") == lang
        if lang == "ar":
            assert page.locator("html").get_attribute("dir") == "rtl"
        page.set_viewport_size({"width": 1280, "height": 900})
    assert not errors
