"""Real Chromium + the existing Flask server: CAP-11 Slice 1, Evidence Details
in report Section 2 (EN and AR).

Synthetic invention data only. A Mechanical project is started and the
mechanism answered through the real form; the report then shows, under each
Known Problem / Known Mechanism statement, "About this evidence" with three
separate rows (Form / Source / Validation), and nothing else in the report
gains them.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_safe_question_routing_pf_q2 import MECH
from tests.test_safe_question_routing_pf_q2_weak_recovery_browser import (
    _start_mechanical, _answer,
)


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_evidence_details_in_report_section_2(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_mechanical(page, server, lang)
    for value in (MECH, MECH):
        _answer(page, value)
    # the live session page gains nothing
    assert page.locator("[data-ev-details]").count() == 0

    page.goto(f"{server}/session/{sid}/deliverable")
    blocks = page.locator("[data-ev-details]")
    expect(blocks).to_have_count(2)
    for i in range(2):
        block = blocks.nth(i)
        expect(block).to_be_visible()
        expect(block).to_contain_text(text("UI_ED_HEADING", lang))
        labels = block.locator("dt").all_inner_texts()
        assert [l.strip() for l in labels] == [
            text("UI_ED_FORM", lang), text("UI_ED_SOURCE", lang),
            text("UI_ED_VALIDATION", lang)]
        expect(block.locator("[data-ed-validation]")).to_have_text(
            text("UI_ED_VALIDATION_UNVALIDATED", lang))
        assert block.locator("a, button, form, input, select, textarea").count() == 0
    problem, mechanism = blocks.nth(0), blocks.nth(1)
    expect(problem.locator("[data-ed-source]")).to_have_text(
        text("UI_ED_SOURCE_LEGACY_UNSPECIFIED", lang))
    expect(mechanism.locator("[data-ed-source]")).to_have_text(
        text("UI_ED_SOURCE_OWNER_STATED", lang))
    expect(mechanism.locator("[data-ed-form]")).to_have_text(
        text("UI_ED_FORM_REASONED", lang))
    # both blocks sit inside Section 2, before the reasoning section
    reasoning_y = page.locator("#report-reasoning").bounding_box()["y"]
    assert mechanism.bounding_box()["y"] < reasoning_y

    # layout: coherent at phone width, no horizontal overflow; RTL on Arabic
    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert problem.bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
