"""Real Chromium + the existing Flask server: INTEGRATED-JOURNEY-GUIDANCE-01 (EN and AR).

Synthetic data only. An integrated Mechanical + Electrical / Electronics invention is
started through the real composition form with the Mechanical part as the initial
analysis focus and its questions answered through the real answer form; the Project
Compass "What to do now" then offers the other part's questions as the one primary
action, with the review handoff one click away; following the primary action lands on
that part's question page. In Arabic the page is RTL, and at phone width (390 px)
there is no horizontal overflow.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import _no_overflow, _start_integrated
from tests.test_safe_question_routing_pf_q2 import MECH as MECH_ANSWER, PF_STRONG, BA_1, BA_2


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_finished_focus_is_guided_to_the_other_part(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, lang, "mechanical")
    for value in (MECH_ANSWER, MECH_ANSWER, PF_STRONG, BA_1, BA_2):
        page.goto(f"{server}/session/{sid}")
        page.fill("#response", value)
        page.locator("#answer-form button[type=submit]").click()
        page.wait_for_load_state()
    page.goto(f"{server}/session/{sid}")
    primary = page.locator("[data-primary-action]")
    expect(primary).to_have_count(1)
    assert primary.get_attribute("data-ijg-action") == "part_questions"
    expect(primary).to_have_text(text("UI_IJG_PART_CTA_ELEC", lang))
    expect(page.locator("[data-ijg-note]")).to_have_text(text("UI_IJG_PART_NOTE_ELEC", lang))
    handoff = page.locator("[data-ijg-handoff] a")
    expect(handoff).to_have_text(text("UI_A1_REVIEW_HANDOFF", lang))
    assert handoff.get_attribute("href").endswith(f"/session/{sid}/deliverable")
    _no_overflow(page, '[data-pc-row="do"]')
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    primary.click()
    page.wait_for_load_state()
    assert f"/session/{sid}/part-questions?part=" in page.url
    assert page.locator("textarea[name^=part_answer__]").count() > 0
    assert not errors
