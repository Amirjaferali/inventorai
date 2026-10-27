"""Real Chromium + the existing Flask server: MEASUREMENT-PLANNING-INTEGRATED-PART-01
(EN and AR).

Synthetic invention data only. An integrated Mechanical + Electrical /
Electronics invention with a MECHANICAL initial focus is started through the
real composition form; its CAP-09 experiment-planning page shows the existing
quantity-versus-condition guidance, the conditions-of-use awareness and the
collapsed reference panel, preceded by ONE line naming the declared Electrical /
Electronics part (direction-auto isolated) with the note that this says nothing
about any experiment. At phone width (390 px) there is no horizontal overflow;
in Arabic the page is RTL.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import (
    ELEC_PART, _no_overflow, _start_integrated)


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_mechanical_focus_shows_measurement_planning_for_its_electrical_part(
        server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, lang, "mechanical")
    page.goto("%s/session/%s/success-criteria" % (server, sid))
    page.wait_for_load_state()
    part = page.locator("[data-mguide-part]")
    expect(part).to_have_count(1)
    expect(part).to_contain_text(text("UI_SC_MGUIDE_PART_LABEL", lang))
    expect(part).to_contain_text(text("UI_SC_MGUIDE_PART_NOTE", lang))
    name = page.locator("[data-mguide-part-name]")
    expect(name).to_have_text(ELEC_PART)
    assert name.get_attribute("dir") == "auto"

    expect(page.locator("[data-measurement-guidance]")).to_be_visible()
    expect(page.locator("[data-measurement-conditions]")).to_be_visible()
    panel = page.locator("details[data-measurement-reference]")
    expect(panel).to_have_count(1)
    assert panel.get_attribute("open") is None            # still collapsed by default
    # the line precedes the elements it explains
    assert part.bounding_box()["y"] < page.locator(
        "[data-measurement-guidance]").bounding_box()["y"]

    _no_overflow(page, "[data-mguide-part]")
    assert page.locator("[data-measurement-guidance]").bounding_box()["width"] <= \
        page.evaluate("document.documentElement.clientWidth")
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    page.set_viewport_size({"width": 1280, "height": 900})
    assert not errors


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_electronics_focus_shows_the_elements_without_a_part_line(server, page, lang):
    sid = _start_integrated(page, server, lang, "electronics_electrical")
    page.goto("%s/session/%s/success-criteria" % (server, sid))
    page.wait_for_load_state()
    expect(page.locator("[data-measurement-guidance]")).to_be_visible()
    expect(page.locator("[data-mguide-part]")).to_have_count(0)
