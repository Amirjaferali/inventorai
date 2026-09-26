"""Real Chromium + the existing Flask server: CAP-10 Slice 1.

Synthetic invention data only. The inventor marks two of their own recorded
answers as conflicting through the real form, sees the declaration on the
existing product surfaces (next development step, project record, deliverable),
corrects one of the two answers through the existing correction path, and the
conflict becomes inactive with no "resolved" / "verified" claim.
"""
import pytest
from playwright.sync_api import expect

import web.app as webapp
from web.ui_text import text
from engine.idea_state import active_declared_contradiction_pairs
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_safe_question_routing_pf_q2 import MECH, PF_STRONG, BA_1
from tests.test_safe_question_routing_pf_q2_weak_recovery_browser import (
    _start_mechanical, _answer,
)

NOTE = "The latch cannot be both spring-loaded and tool-free."


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_declare_see_and_correct_a_conflict(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_mechanical(page, server, lang)
    for value in (MECH, MECH, PF_STRONG, BA_1):
        _answer(page, value)
    state = webapp.SESSION_STORE[sid]["state"]
    answered = [r.record_id for r in state.assertions if r.disposition == "answered"]
    lo, hi = answered[0], answered[-1]

    # 45 — declare through the real form
    block = page.locator("details.declare-conflict")
    expect(block).to_have_count(1)
    block.locator("summary").click()
    expect(block).to_contain_text(text("UI_CAP10_EXPLAIN", lang))
    block.locator(f'input[name=endpoint][value="{lo}"]').check()
    block.locator(f'input[name=endpoint][value="{hi}"]').check()
    block.locator("textarea[name=note]").fill(NOTE)
    block.locator("input[name=conflict_confirm]").check()
    block.locator("button[type=submit]").click()
    page.wait_for_load_state()
    assert (lo, hi) in active_declared_contradiction_pairs(
        webapp.SESSION_STORE[sid]["state"].assertions)

    # 46 — visible on the existing surfaces
    main = page.locator("main").inner_text()
    assert "Two recorded answers you marked as conflicting" in main   # next step (EN content)
    record = page.locator("details#t3a-project-record")
    record.locator("summary").first.click()
    expect(record).to_contain_text(text("UI_T3A_EVENT_CONTRADICTION_DECLARED", lang))
    expect(record).to_contain_text(NOTE)
    page.goto(server + f"/session/{sid}/deliverable")
    deliverable = page.locator("body").inner_text()
    assert "Contradiction you declared" in deliverable
    assert "not been validated" in deliverable

    # 47 — correct one endpoint through the existing correction path
    page.goto(server + f"/session/{sid}")
    page.locator("details.correct-answer > summary").click()
    page.locator("#correct-target").select_option(lo)
    page.locator("#correct-response").fill(MECH + " The frame rail is steel.")
    page.locator("details.correct-answer form button[type=submit]").click()
    page.wait_for_load_state()

    # 48 — inactive, kept as history, never called resolved
    state = webapp.SESSION_STORE[sid]["state"]
    assert active_declared_contradiction_pairs(state.assertions) == frozenset()
    main = page.locator("main").inner_text()
    assert "Two recorded answers you marked as conflicting" not in main
    record = page.locator("details#t3a-project-record")
    record.locator("summary").first.click()
    expect(record).to_contain_text(text("UI_T3A_EVENT_CONTRADICTION_DECLARED", lang))
    page.goto(server + f"/session/{sid}/deliverable")
    deliverable = page.locator("body").inner_text()
    assert "Contradiction you declared" not in deliverable
    for claim in ("contradiction is resolved", "conflict was resolved",
                  "conflict is verified"):
        assert claim not in deliverable.lower()
    assert page.locator("html").get_attribute("lang") == lang
    assert not errors
