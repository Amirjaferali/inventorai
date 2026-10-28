"""Real Chromium + the existing Flask server: IDEA-DESIGN-UNDERSTANDING-
PROJECTION-01 (EN and AR, RTL, 390 px).

Synthetic invention data only. A Mechanical project is started from an idea the
existing functional reading proposes as screen support; the collapsed picture
opens, shows the original statement verbatim, the provisional reading with its
status, the absence lines for undeclared parts / components / interactions, the
fixed boundary disclosure and the one existing Step-6 continuation link, which
still leads to the unchanged CAP-13 page with nothing pre-filled.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_step6_functional_capability_action_browser import _start, IDEA


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_design_understanding_picture_journey(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start(page, server, lang)
    picture = page.locator("[data-design-understanding]")
    expect(picture).to_have_count(1)
    picture.locator("summary").click()
    expect(picture.locator("summary")).to_have_text(text("UI_DU_TITLE", lang))
    original = picture.locator('[data-du-section="original_idea"]')
    expect(original).to_have_attribute("data-du-status", "PRESENT")
    expect(original.locator("[data-du-text]")).to_have_text(IDEA)
    reading = picture.locator('[data-du-section="functional_readings"] [data-du-item="functional_role"]')
    expect(reading).to_have_count(1)
    expect(reading).to_contain_text(text("UI_DU_VAL_PROPOSED", lang))
    for key in ("parts", "components", "interactions", "constraints"):
        section = picture.locator('[data-du-section="%s"]' % key)
        expect(section).to_have_attribute("data-du-status", "ABSENT")
        expect(section.locator("[data-du-section-absent]")).to_have_text(
            text("UI_DU_ABSENT_" + key.upper(), lang))
    expect(picture.locator("[data-du-boundary]")).to_have_text(text("UI_DU_BOUNDARY", lang))
    action = picture.locator("[data-du-action]")
    expect(action).to_have_count(1)
    assert action.get_attribute("href") == f"/session/{sid}/support-reactions"
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    page.set_viewport_size({"width": 1280, "height": 900})
    action.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/support-reactions")
    form = page.locator("[data-cap13-form]")
    assert form.locator("input[type=radio]:checked").count() == 0
    for name in ("P", "L", "x"):
        assert page.input_value(f"#cap13-{name}") == ""
    assert not errors
