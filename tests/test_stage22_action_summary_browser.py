"""Real Chromium + the existing Flask server: Stage 22 / CAP-05 + CAP-07
Slice 2, the read-only project-level Actionable Decision Room Summary.

Synthetic invention data only. The inventor answers a few questions through the
real form and declares a decision with two alternatives through the existing
W2-A forms; nothing is fabricated for display. The Decision Room then shows the
action summary outside every decision (grouped by the canonical Validation Plan
responsibility), the current next development step with a working link, and a
link to the full Validation Plan in the report; the report shows the same
summary read-only with report-local links. The summary itself holds no control.
"""
import pytest
from playwright.sync_api import expect

import web.app as webapp
from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_safe_question_routing_pf_q2 import MECH, PF_STRONG, BA_1
from tests.test_safe_question_routing_pf_q2_weak_recovery_browser import (
    _start_mechanical, _answer,
)

QUESTION = "Which latch mechanism should hold the ramp flat?"
ALTS = ("Toggle latch", "Spring-loaded pin")


def _declare_decision(page):
    decisions = page.locator("details#w2b-decision-capture")
    if decisions.get_attribute("open") is None:
        decisions.locator("summary").first.click()
    decisions.locator("#w2a-context-content").fill(QUESTION)
    decisions.locator('form[action$="/decision/declare-context"] button').click()
    page.wait_for_load_state()
    for alt in ALTS:
        form = page.locator('form[action$="/decision/declare-alternative"]')
        form.locator("input[name=content]").fill(alt)
        form.locator("button").click()
        page.wait_for_load_state()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_action_summary_journey(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_mechanical(page, server, lang)
    for value in (MECH, MECH, PF_STRONG, BA_1):
        _answer(page, value)
    _declare_decision(page)

    summary = page.locator("section#decision-action-summary")
    expect(summary).to_contain_text(text("UI_AS_HEADING", lang))
    expect(summary).to_contain_text(text("UI_AS_NOTE", lang))
    # outside every decision / alternative, and holds no control at all
    assert page.locator(".w2a-context #decision-action-summary").count() == 0
    assert page.locator("li.g3-alternative #decision-action-summary").count() == 0
    assert summary.locator("form, input, textarea, select, button").count() == 0

    # grouped by canonical responsibility; owner group plus at least one other
    groups = summary.locator("details.as-group")
    keys = groups.evaluate_all("els => els.map(e => e.dataset.asGroup)")
    assert "owner" in keys and len(keys) >= 2, keys
    owner = summary.locator('details.as-group[data-as-group="owner"]')
    assert owner.get_attribute("open") is None
    owner.locator("summary").click()
    expect(owner.locator("li.as-item").first).to_be_visible()
    count = int(owner.locator(".as-count").inner_text())
    repeats = owner.locator("li.as-item").evaluate_all(
        "els => els.map(e => { const r = e.querySelector('.as-repeat');"
        " return r ? parseInt(r.textContent.replace(/\\D+/g, ''), 10) : 1; })")
    assert sum(repeats) == count

    # the current next development step, with a link to the existing callout
    nxt = summary.locator("p.as-next")
    assert nxt.get_attribute("data-as-next-status") == "items"
    nxt.locator("a.as-link").click()
    assert page.url.endswith("#next-development-step")
    expect(page.locator("#next-development-step")).to_be_visible()

    # the Decision Trace (Slice 1) still renders beside the summary
    expect(page.locator("details.dt-history")).to_have_count(len(ALTS))

    # detail lives in the existing Validation Plan (Section 14) in the report
    summary.locator("p.as-plan-link a").click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/deliverable#report-validation-plan")
    expect(page.locator("#report-validation-plan + h3")).to_have_text(
        text("UI_B_DELIV_085", lang))
    rsum = page.locator("#report-decision-action-summary")
    expect(rsum).to_contain_text(text("UI_AS_HEADING", lang))
    assert rsum.locator("form, input, textarea, select, button, details").count() == 0
    hrefs = rsum.locator("a").evaluate_all(
        "els => els.map(e => e.getAttribute('href'))")
    assert hrefs and set(hrefs) <= {"#report-validation-plan", "#report-next-steps"}
    for href in hrefs:
        assert page.locator(href).count() == 1, href
    assert webapp.SESSION_STORE[sid]["state"].domain is not None
    assert page.locator("html").get_attribute("lang") == lang
    assert not errors
