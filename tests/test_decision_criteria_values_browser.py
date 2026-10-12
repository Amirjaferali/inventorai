"""Real Chromium + the existing Flask server:
INVENTOR-DECLARED-ALTERNATIVE-CRITERIA-VALUES-01 (EN and AR, phone width).

Synthetic invention data only. A Mechanical project is started through the real
forms; a decision and two alternatives are declared through the existing W2-A
forms; then, through the new Decision Room forms only, the inventor adds a
criterion and records a value for one alternative. Refining that alternative
makes the value NEEDS CONFIRMATION (shown with the earlier text, labelled);
"Confirm unchanged" makes it current again. At 390 px there is no horizontal
page overflow; in Arabic the page is RTL and inventor text is
direction-isolated. The report shows the same values with no control.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_safe_question_routing_pf_q2_weak_recovery_browser import _start_mechanical

QUESTION = "Which hinge should carry the folding ramp?"
ALT_A, ALT_A2, ALT_B = "Piano hinge", "Piano hinge, stainless", "Two barrel hinges"
CRITERION = "Added weight"
VALUE = "about 300 g — measured on the bench"
VALUE_AR = "حوالي 300 غرام"


def _no_overflow(page):
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1


def _open_decisions(page):
    decisions = page.locator("details#w2b-decision-capture")
    if decisions.get_attribute("open") is None:
        decisions.locator("summary").first.click()
    return decisions


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_criteria_and_values_journey_en_ar_phone_width(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_mechanical(page, server, lang)
    decisions = _open_decisions(page)
    decisions.locator("#w2a-context-content").fill(QUESTION)
    decisions.locator('form[action$="/decision/declare-context"] button').click()
    page.wait_for_load_state()
    for alt in (ALT_A, ALT_B):
        form = page.locator('form[action$="/decision/declare-alternative"]')
        form.locator("input[name=content]").fill(alt)
        form.locator("button").click()
        page.wait_for_load_state()

    section = page.locator("section.cmp[data-cmp-surface=session]")
    expect(section).to_have_count(1)
    expect(section.locator("h4")).to_have_text(text("UI_CMP_HEADING", lang))
    declare = section.locator("form[data-cmp-declare-form]")
    declare.locator("input[name=criterion_label]").fill(CRITERION)
    declare.locator("button[value=declare]").click()
    page.wait_for_load_state()
    section = page.locator("section.cmp[data-cmp-surface=session]")
    expect(section.locator("[data-cmp-ack]")).to_have_text(
        text("UI_CMP_MSG_CRITERION_ADDED", lang))
    expect(section.locator("[data-cmp-label]")).to_have_text(CRITERION)

    first = section.locator("tr[data-cmp-cell]").first
    expect(first.locator("[data-cmp-alt-name]")).to_have_text(ALT_A)
    first.locator("details[data-cmp-cell-edit] summary").click()
    first.locator("textarea[name=value_text]").fill(VALUE if lang == "en" else VALUE_AR)
    first.locator("button[value=save]").click()
    page.wait_for_load_state()
    section = page.locator("section.cmp[data-cmp-surface=session]")
    first = section.locator("tr[data-cmp-cell]").first
    expect(first).to_have_attribute("data-cmp-state", "recorded")
    shown = first.locator("[data-cmp-text]")
    expect(shown).to_have_text(VALUE if lang == "en" else VALUE_AR)
    assert shown.evaluate("e => e.tagName") == "BDI" and shown.get_attribute("dir") == "auto"
    expect(section.locator("tr[data-cmp-cell]").nth(1)).to_have_attribute(
        "data-cmp-state", "not_recorded")

    # refining the alternative makes the value need confirmation — never rebound
    alt_a = page.locator("li.g3-alternative", has=page.locator("span.g3-name", has_text=ALT_A))
    alt_a.locator('form[action$="/decision/refine-alternative"] input[name=content]').fill(ALT_A2)
    alt_a.locator('form[action$="/decision/refine-alternative"] button').click()
    page.wait_for_load_state()
    first = page.locator("section.cmp[data-cmp-surface=session] tr[data-cmp-cell]").first
    expect(first).to_have_attribute("data-cmp-state", "needs_confirmation")
    expect(first.locator("[data-cmp-stale-reason=alternative]")).to_have_count(1)
    expect(first.locator("[data-cmp-alt-name]")).to_have_text(ALT_A2)
    first.locator("details[data-cmp-cell-edit] summary").click()
    first.locator("button[value=reconfirm]").click()
    page.wait_for_load_state()
    first = page.locator("section.cmp[data-cmp-surface=session] tr[data-cmp-cell]").first
    expect(first).to_have_attribute("data-cmp-state", "recorded")

    page.set_viewport_size({"width": 390, "height": 900})
    page.locator("section.cmp[data-cmp-surface=session]").scroll_into_view_if_needed()
    _no_overflow(page)
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"

    page.goto(f"{server}/session/{sid}/deliverable")
    report = page.locator("section.cmp[data-cmp-surface=report]")
    expect(report).to_have_count(1)
    expect(report.locator("tr[data-cmp-cell]").first.locator("[data-cmp-text]")).to_have_text(
        VALUE if lang == "en" else VALUE_AR)
    assert report.locator("form, input, textarea, button, select, details").count() == 0
    _no_overflow(page)
    assert not errors
