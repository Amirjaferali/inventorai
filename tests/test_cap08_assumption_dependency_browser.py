"""Real Chromium + the existing Flask server: CAP-08 Slice 1.

Synthetic invention data only. The inventor records a provisional assumption,
declares through the real form that two of their recorded answers depend on it,
sees the dependency on the existing surfaces (compact view, project record,
report), leaves and resumes the saved project, corrects ONE of the two answers
through the existing correction path, and only that edge becomes inactive while
the other stays active — with no "resolved" / "confirmed" / "validated" claim.
"""
import pytest
from playwright.sync_api import expect

import web.app as webapp
from web.ui_text import text
from engine.idea_state import project_assumption_dependencies
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_safe_question_routing_pf_q2 import MECH, PF_STRONG, BA_1
from tests.test_safe_question_routing_pf_q2_weak_recovery_browser import (
    _start_mechanical, _answer,
)

ASSUMPTION = "Assume the hinge pin carries the full deck load."


def _record_assumption(page, value):
    page.locator("#response").fill(value)
    page.locator("details.response-more-choices > summary").click()
    page.locator('#answer-form input[name=action][value="provisional_assumption"]').check()
    page.locator("#answer-form button[type=submit]").click()
    page.wait_for_load_state()


def _active_edges(sid):
    return set(project_assumption_dependencies(
        webapp.SESSION_STORE[sid]["state"].assertions).active_edges)


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_declare_see_resume_and_correct_one_dependent_answer(server, page, lang):
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
    lo, hi = answered[0], answered[-1]

    # the compact view says nothing is recorded yet (never "none exists")
    view = page.locator("section#assumption-dependencies")
    expect(view).to_contain_text(text("UI_CAP08_NONE", lang))

    # declare a multi-answer dependency through the real form
    block = page.locator("details.declare-dependency")
    block.locator("summary").click()
    expect(block).to_contain_text(text("UI_CAP08_EXPLAIN", lang))
    block.locator(f'input[name=assumption][value="{assumption}"]').check()
    block.locator(f'input[name=dependent][value="{lo}"]').check()
    block.locator(f'input[name=dependent][value="{hi}"]').check()
    block.locator("input[name=dependency_confirm]").check()
    block.locator("button[type=submit]").click()
    page.wait_for_load_state()
    assert _active_edges(sid) == {(assumption, lo), (assumption, hi)}

    # visible on the compact view and the project record
    view = page.locator("section#assumption-dependencies")
    expect(view).to_contain_text(text("UI_CAP08_VIEW_NOTE", lang))
    expect(view.locator(f'[data-dependency-assumption="{assumption}"] li')).to_have_count(2)
    record = page.locator("details#t3a-project-record")
    record.locator("summary").first.click()
    expect(record).to_contain_text(
        text("UI_T3A_EVENT_ASSUMPTION_DEPENDENCY_DECLARED", lang))

    # save / resume: the process forgets the live session; the saved project
    # comes back read-only and is resumed through the real button
    webapp.SESSION_STORE.pop(sid)
    page.goto(server + f"/session/{sid}")
    page.locator("#resume-project").click()
    page.wait_for_load_state()
    assert _active_edges(sid) == {(assumption, lo), (assumption, hi)}
    expect(page.locator("section#assumption-dependencies")
           .locator(f'[data-dependency-assumption="{assumption}"] li')).to_have_count(2)

    # the report carries the inventor-declared subsection
    page.goto(server + f"/session/{sid}/deliverable")
    expect(page.locator("div.cap08-declared-dependencies")).to_contain_text(
        text("UI_CAP08_REPORT_HEADING", lang))

    # correct ONE dependent answer through the existing correction path
    page.goto(server + f"/session/{sid}")
    page.locator("details.correct-answer > summary").click()
    page.locator("#correct-target").select_option(lo)
    page.locator("#correct-response").fill(MECH + " The frame rail is steel.")
    page.locator("details.correct-answer form button[type=submit]").click()
    page.wait_for_load_state()

    # only that edge is inactive; the other stays active; history is kept
    assert _active_edges(sid) == {(assumption, hi)}
    view = page.locator("section#assumption-dependencies")
    expect(view.locator(f'[data-dependency-assumption="{assumption}"] li')).to_have_count(1)
    record = page.locator("details#t3a-project-record")
    record.locator("summary").first.click()
    expect(record.locator("[data-record-dependency-inactive]")).to_have_count(1)
    page.goto(server + f"/session/{sid}/deliverable")
    report = page.locator("body").inner_text().lower()
    for claim in ("is resolved", "was resolved", "is confirmed", "was confirmed",
                  "dependency is validated", "has been validated"):
        assert claim not in report

    # Astra F2: correcting the remaining dependent answer leaves declarations
    # in history but none active — never shown as "no dependency recorded"
    page.goto(server + f"/session/{sid}")
    page.locator("details.correct-answer > summary").click()
    page.locator("#correct-target").select_option(hi)
    page.locator("#correct-response").fill(BA_1 + " It locks on its own.")
    page.locator("details.correct-answer form button[type=submit]").click()
    page.wait_for_load_state()
    assert _active_edges(sid) == set()
    view = page.locator("section#assumption-dependencies")
    expect(view.locator("[data-dependency-inactive-history]")).to_have_text(
        text("UI_CAP08_INACTIVE_HISTORY", lang))
    expect(view).not_to_contain_text(text("UI_CAP08_NONE", lang))
    page.goto(server + f"/session/{sid}/deliverable")
    expect(page.locator("[data-dependency-inactive-history]")).to_have_count(2)
    assert text("UI_CAP08_NONE", lang) not in page.locator("body").inner_text()
    assert page.locator("html").get_attribute("lang") == lang
    assert not errors
