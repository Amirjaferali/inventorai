"""Real Chromium + the existing Flask server: CURRENT-QUESTION-GAP-CONTEXT-01
(EN and AR, RTL, 390 px).

Synthetic invention data only. A Mechanical project is started; while answering
the current question is the one primary action, the label beside the question
and the marker on the matching picture item show the same friendly gap name; the
label and marker carry no control and the page keeps exactly one primary action.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from web.gap_labels import GAP_DISPLAY_NAMES, GAP_DISPLAY_NAMES_AR
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_step6_functional_capability_action_browser import _start


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_current_question_gap_context_journey(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    _start(page, server, lang)
    names = GAP_DISPLAY_NAMES_AR if lang == "ar" else GAP_DISPLAY_NAMES
    primary = page.locator("[data-primary-action]")
    expect(primary).to_have_count(1)
    assert primary.get_attribute("href") == "#response"
    label = page.locator("[data-question-gap]")
    expect(label).to_have_count(1)
    expect(label).to_be_visible()
    label_text = label.inner_text().strip()
    assert label_text.startswith(text("UI_CQG_LABEL", lang))
    gap_name = label_text[len(text("UI_CQG_LABEL", lang)):].strip()
    assert gap_name in names.values(), gap_name
    assert label.locator("a, button, input, form").count() == 0
    picture = page.locator("[data-design-understanding]")
    picture.locator("summary").click()
    marker = page.locator("[data-du-current-question]")
    expect(marker).to_have_count(1)
    expect(marker).to_be_visible()
    expect(marker).to_contain_text(text("UI_CQG_MARKER", lang))
    item = page.locator('[data-du-item="gap"]', has=marker)
    expect(item).to_have_count(1)
    assert item.inner_text().strip().startswith(gap_name)
    assert marker.locator("a, button, input, form").count() == 0
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert not errors
