"""Real Chromium + the existing Flask server: Stage 22 / CAP-05 + CAP-07
Slice 1, the read-only decision trace and the separated project-context panel.

Synthetic invention data only. The inventor records answers and a provisional
assumption and declares a dependency through the real CAP-08 form (so the
project context is built by canonical behaviour, never fabricated), then
declares a decision, two alternatives, refines one and withdraws the other
with a reason — all through the existing W2-A forms. The decision section
shows each alternative's full recorded history and a project-context panel
outside every decision whose links resolve on the session; the report shows
the same read-only trace and links only to report-local sections.
"""
import pytest
from playwright.sync_api import expect

import web.app as webapp
from web.ui_text import text
from engine.idea_state import (
    DISPOSITION_DECISION_ALTERNATIVE_DECLARED,
    DISPOSITION_DECISION_CONTEXT_DECLARED,
)
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_safe_question_routing_pf_q2 import MECH, PF_STRONG, BA_1
from tests.test_safe_question_routing_pf_q2_weak_recovery_browser import (
    _start_mechanical, _answer,
)
from tests.test_cap08_assumption_dependency_browser import _record_assumption

QUESTION = "Which latch mechanism should hold the ramp flat?"
ALT_A, ALT_A2 = "Toggle latch", "Toggle latch, stainless"
ALT_B = "Spring-loaded pin"
REASON = "not robust enough under repeated load"
ASSUMPTION = "Assume the hinge pin carries the full deck load."


def _all_links_resolve(page, scope):
    hrefs = scope.locator("a.dt-ctx-link").evaluate_all(
        "els => els.map(e => e.getAttribute('href'))")
    for href in hrefs:
        assert href.startswith("#"), href
        assert page.locator(href).count() == 1, href
    return hrefs


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_decision_trace_and_project_context_journey(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_mechanical(page, server, lang)
    for value in (MECH, MECH, PF_STRONG, BA_1):
        _answer(page, value)
    _record_assumption(page, ASSUMPTION)
    state = webapp.SESSION_STORE[sid]["state"]
    [assumption] = [r.record_id for r in state.assertions
                    if r.disposition == "provisional_assumption"]
    answered = [r.record_id for r in state.assertions if r.disposition == "answered"]
    block = page.locator("details.declare-dependency")
    block.locator("summary").click()
    block.locator(f'input[name=assumption][value="{assumption}"]').check()
    block.locator(f'input[name=dependent][value="{answered[0]}"]').check()
    block.locator("input[name=dependency_confirm]").check()
    block.locator("button[type=submit]").click()
    page.wait_for_load_state()

    # decision journey through the EXISTING W2-A forms
    decisions = page.locator("details#w2b-decision-capture")
    if decisions.get_attribute("open") is None:
        decisions.locator("summary").first.click()
    decisions.locator("#w2a-context-content").fill(QUESTION)
    decisions.locator('form[action$="/decision/declare-context"] button').click()
    page.wait_for_load_state()
    for alt in (ALT_A, ALT_B):
        form = page.locator('form[action$="/decision/declare-alternative"]')
        form.locator("input[name=content]").fill(alt)
        form.locator("button").click()
        page.wait_for_load_state()
    alt_a = page.locator("li.g3-alternative", has=page.locator(
        "span.g3-name", has_text=ALT_A))
    alt_a.locator('form[action$="/decision/refine-alternative"] input[name=content]').fill(ALT_A2)
    alt_a.locator('form[action$="/decision/refine-alternative"] button').click()
    page.wait_for_load_state()
    alt_b = page.locator("li.g3-alternative", has=page.locator(
        "span.g3-name", has_text=ALT_B))
    alt_b.locator('form[action$="/decision/withdraw-alternative"] input[name=reason]').fill(REASON)
    alt_b.locator('form[action$="/decision/withdraw-alternative"] button').click()
    page.wait_for_load_state()

    state = webapp.SESSION_STORE[sid]["state"]
    [ctx] = [r.record_id for r in state.assertions
             if r.disposition == DISPOSITION_DECISION_CONTEXT_DECLARED]
    roots = [r.record_id for r in state.assertions
             if r.disposition == DISPOSITION_DECISION_ALTERNATIVE_DECLARED
             and not r.supersedes]

    # the trace: collapsed by default, complete and verbatim when opened
    history_a = page.locator(f'details.dt-history[data-dt-root="{roots[0]}"]')
    assert history_a.get_attribute("open") is None
    history_a.locator("summary").click()
    events_a = history_a.locator("li.dt-event")
    expect(events_a).to_have_count(2)
    expect(events_a.nth(0).locator(".dt-text")).to_have_text(ALT_A)
    expect(events_a.nth(1).locator(".dt-text")).to_have_text(ALT_A2)
    expect(events_a.nth(1)).to_contain_text(text("UI_DT_EVENT_REFINED", lang))
    history_b = page.locator(f'details.dt-history[data-dt-root="{roots[1]}"]')
    history_b.locator("summary").click()
    expect(history_b.locator("li.dt-withdrawn .dt-text")).to_have_text(REASON)
    expect(page.locator("li.g3-withdrawn span.g3-name")).to_have_text(ALT_B)

    # the project-context panel: outside every decision, truthful statuses
    panel = page.locator("section#decision-project-context")
    expect(panel).to_contain_text(text("UI_DT_CTX_HEADING", lang))
    assert page.locator(".w2a-context #decision-project-context").count() == 0
    assert page.locator("li.g3-alternative #decision-project-context").count() == 0
    dep_row = panel.locator('li[data-dt-category="assumption_dependencies"]')
    assert dep_row.get_attribute("data-dt-status") == "items"
    expect(dep_row.locator(".dt-ctx-count")).to_have_text("1")
    assert panel.locator(
        'li[data-dt-category="provisional_assumptions"]').get_attribute(
            "data-dt-status") == "items"
    hrefs = _all_links_resolve(page, panel)
    assert "#assumption-dependencies" in hrefs
    dep_row.locator("a.dt-ctx-link").click()
    assert page.url.endswith("#assumption-dependencies")
    expect(page.locator("section#assumption-dependencies")).to_be_visible()
    assert ctx and not errors

    # the report: the same read-only trace, report-local links only
    page.goto(server + f"/session/{sid}/deliverable")
    report = page.locator("section.w2a-decisions")
    expect(report.locator(f'.dt-history[data-dt-root="{roots[0]}"] li.dt-event')).to_have_count(2)
    expect(report.locator("li.dt-withdrawn .dt-text")).to_have_text(REASON)
    assert report.locator("form, details").count() == 0
    rpanel = page.locator("#report-decision-project-context")
    expect(rpanel).to_contain_text(text("UI_DT_CTX_HEADING", lang))
    for href in _all_links_resolve(page, rpanel):
        assert href in ("#report-needs", "#report-next-steps"), href
    rpanel.locator('li[data-dt-category="assumption_dependencies"] a.dt-ctx-link').click()
    assert page.url.endswith("#report-needs")
    assert page.locator("html").get_attribute("lang") == lang
    assert not errors
