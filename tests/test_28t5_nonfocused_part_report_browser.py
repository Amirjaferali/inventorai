"""Real Chromium + the existing Flask server: 28-T5-NONFOCUSED-PART-REPORT-01 (EN and AR,
desktop and phone width).

Synthetic invention data only. An integrated Mechanical + Electrical / Electronics invention
is started through the real composition form; the inventor saves one answer about the part
OUTSIDE the focus on its question page, then opens the report: the part's governed questions
are shown verbatim (LTR-isolated), the saved answer verbatim with the OWNER_STATED /
UNVALIDATED label, and the safety disclosure beside them. No horizontal overflow at 390 px;
RTL in Arabic.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import _start_integrated

ANSWER = "It turns the arm — يدير الذراع"
TITLE = {"mechanical": "UI_PQRR_TITLE_MECH", "electronics_electrical": "UI_PQRR_TITLE_ELEC"}
OTHER = {"mechanical": "electronics_electrical", "electronics_electrical": "mechanical"}


@pytest.mark.parametrize("lang,width,focus", [("en", 1280, "mechanical"), ("ar", 390, "mechanical"),
                                              ("en", 390, "electronics_electrical"),
                                              ("ar", 1280, "electronics_electrical")])
def test_report_shows_the_nonfocused_part_answers(server, page, lang, width, focus):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.set_viewport_size({"width": width, "height": 900})
    sid = _start_integrated(page, server, lang, focus)
    page.locator("[data-scope-required-part-questions] a").click()
    page.wait_for_load_state()
    page.locator("textarea").first.fill(ANSWER)
    page.get_by_role("button", name=text("UI_PQ_SAVE", lang)).click()
    page.wait_for_load_state()

    page.goto(f"{server}/session/{sid}/deliverable")
    block = page.locator("[data-nonfocused-part-answers]")
    expect(block).to_have_count(1)
    expect(block.locator("h3")).to_have_text(text(TITLE[OTHER[focus]], lang))
    expect(block.locator("[data-npr-answer]")).to_have_text([ANSWER])
    expect(block.locator("[data-npr-provenance]")).to_have_text([text("UI_PQRR_PROVENANCE", lang)])
    expect(block.locator("[data-npr-safety]")).to_have_text(text("UI_PQRR_SAFETY", lang))
    questions = block.locator("[data-npr-question]")
    assert questions.count() >= 5 and questions.first.get_attribute("dir") == "ltr"
    assert block.locator("[data-npr-unavailable]").count() == 0
    expect(block).to_be_visible()

    viewport = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= viewport + 1
    assert block.bounding_box()["width"] <= viewport
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
