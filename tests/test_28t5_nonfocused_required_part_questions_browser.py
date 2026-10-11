"""Real Chromium + the existing Flask server: 28-T5-NONFOCUSED-REQUIRED-PART-QUESTIONS-SAFETY-01
(EN and AR, desktop and phone width).

Synthetic invention data only. An integrated Mechanical + Electrical / Electronics
invention is started through the real composition form in BOTH focus directions; the
inventor follows the session page's link to the questions of the part OUTSIDE the
focus, sees that part's governed questions verbatim (LTR-isolated), saves an answer
that states a hazard and sees ONE part-local safety signal; clearing it removes the
signal. No horizontal overflow at 390 px; RTL in Arabic.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import _start_integrated

HAZARD = {
    "mechanical": "If the guard comes loose, fingers could be caught in the rotating parts and crushed.",
    "electronics_electrical": "If protection fails, the high voltage could cause a fire.",
}
TITLE = {"mechanical": "UI_PQR_TITLE_MECH", "electronics_electrical": "UI_PQR_TITLE_ELEC"}
OTHER = {"mechanical": "electronics_electrical", "electronics_electrical": "mechanical"}


@pytest.mark.parametrize("lang,width,focus", [("en", 1280, "mechanical"), ("ar", 390, "mechanical"),
                                              ("en", 390, "electronics_electrical"),
                                              ("ar", 1280, "electronics_electrical")])
def test_nonfocused_part_questions_and_part_local_safety(server, page, lang, width, focus):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.set_viewport_size({"width": width, "height": 900})
    _start_integrated(page, server, lang, focus)
    link = page.locator("[data-scope-required-part-questions] a")
    expect(link).to_have_count(1)
    expect(link).to_have_text(text("UI_PQ_LINK", lang))
    link.click()
    page.wait_for_load_state()
    other = OTHER[focus]
    expect(page.locator("h1")).to_have_text(text(TITLE[other], lang))
    questions = page.locator("[data-pq-question]")
    assert questions.count() >= 5
    assert questions.first.get_attribute("dir") == "ltr"
    expect(page.locator("[data-pq-safety-nothing]")).to_have_text(text("UI_PQR_SS_NOTHING_SAVED", lang))

    page.locator("textarea").first.fill(HAZARD[other])
    page.get_by_role("button", name=text("UI_PQ_SAVE", lang)).click()
    page.wait_for_load_state()
    expect(page.locator("[data-pq-notice]")).to_have_text(text("UI_PQ_MSG_SAVED", lang))
    signals = page.locator("[data-pq-safety-signal]")
    expect(signals).to_have_count(1)
    expect(signals.first.locator("[data-pq-safety-statement]")).to_contain_text(HAZARD[other])
    expect(page.locator("[data-pq-safety-caution]")).to_have_text(text("UI_PQR_SS_CAUTION", lang))

    page.reload()
    expect(page.locator("[data-pq-safety-signal]")).to_have_count(1)
    viewport = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= viewport + 1
    assert page.locator("[data-pq-safety]").bounding_box()["width"] <= viewport
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"

    page.locator("textarea").first.fill("")
    page.get_by_role("button", name=text("UI_PQ_SAVE", lang)).click()
    page.wait_for_load_state()
    expect(page.locator("[data-pq-safety-signal]")).to_have_count(0)
    expect(page.locator("[data-pq-safety-nothing]")).to_have_count(1)
    assert not errors
