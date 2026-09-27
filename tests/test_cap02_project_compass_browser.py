"""Real Chromium + the existing Flask server: CAP-02 Slice 1, the Project
Compass at the top of the live journey (EN and AR).

Synthetic invention data only. A Mechanical project is started and answered
through the real forms; a decision is declared through the existing W2-A forms.
The Compass shows four plain rows with ONE primary action; the former
standalone Next Development Step is its "why it matters now" row; the gap
detail link opens the existing Gap Action Packs; the Decision Room stays a
separate section further down.
"""
import pytest
from playwright.sync_api import expect

import web.app as webapp
from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_safe_question_routing_pf_q2 import MECH
from tests.test_safe_question_routing_pf_q2_weak_recovery_browser import (
    _start_mechanical, _answer,
)
from tests.test_stage22_action_summary_browser import _declare_decision


def _rows(compass):
    return compass.locator("[data-pc-row]").evaluate_all(
        "els => els.map(e => e.dataset.pcRow)")


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_project_compass_journey(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_mechanical(page, server, lang)

    compass = page.locator("section#project-compass")
    expect(compass).to_be_visible()
    expect(compass).to_contain_text(text("UI_PC_HEADING", lang))
    assert _rows(compass) == ["recorded", "unresolved", "why", "do"]
    expect(compass.locator('[data-pc-row="recorded"]')).to_contain_text(
        text("UI_PC_ANSWERS_NONE", lang))
    # ONE primary action on the whole page, inside the Compass, and it works
    primary = page.locator("[data-primary-action]")
    expect(primary).to_have_count(1)
    assert compass.locator("[data-primary-action]").count() == 1
    assert primary.get_attribute("href") == "#response"
    primary.click()
    assert page.url.endswith("#response")
    # the next development step is context: no control inside that row
    why = compass.locator('[data-pc-row="why"]')
    expect(why.locator("#next-development-step")).to_have_count(1)
    assert why.locator("a, button, form, input, textarea, select").count() == 0
    # the Compass sits above the Gap Action Packs, which stay collapsed detail
    packs = page.locator("details#gap-action-packs")
    assert packs.get_attribute("open") is None
    assert compass.bounding_box()["y"] < packs.bounding_box()["y"]

    # later state: answers recorded, an open gap and a routed need
    for value in (MECH, MECH):
        _answer(page, value)
    compass = page.locator("section#project-compass")
    expect(compass.locator('[data-pc-row="recorded"] [data-pc-answers="2"]')).to_have_count(1)
    cats = compass.locator("[data-pc-category]").evaluate_all(
        "els => els.map(e => e.dataset.pcCategory)")
    assert "gaps" in cats and "specialist" in cats, cats
    expect(compass).to_contain_text(text("UI_PC_NOT_SUMMED", lang))
    link = compass.locator('a.pc-link[href="#gap-action-packs"]')
    expect(link).to_have_count(1)
    link.click()
    assert page.url.endswith("#gap-action-packs")
    expect(page.locator("details#gap-action-packs")).to_be_visible()
    expect(page.locator("[data-primary-action]")).to_have_count(1)

    # a declared decision: the Compass does not absorb the Decision Room
    _declare_decision(page)
    compass = page.locator("section#project-compass")
    expect(compass.locator('[data-pc-answers="2"]')).to_have_count(1)
    for marker in ("#decision-action-summary", "#decision-project-context",
                   "details.dt-history", "#w2b-decision-capture"):
        assert compass.locator(marker).count() == 0, marker
    expect(page.locator("section#decision-action-summary")).to_have_count(1)
    expect(page.locator("[data-primary-action]")).to_have_count(1)

    # layout: no horizontal overflow at the page width; RTL on Arabic
    width = page.evaluate("document.documentElement.clientWidth")
    assert compass.bounding_box()["width"] <= width
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert webapp.SESSION_STORE[sid]["state"].domain is not None
    assert not errors
