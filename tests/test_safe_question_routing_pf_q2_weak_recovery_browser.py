"""Real Chromium + the existing Flask server: the weak-PF no-question state.

Synthetic invention data only. Proves in a real browser that a routing-aware
Mechanical project whose single PF attempt was weak renders no "None" question
and no answer form once BA closes, and that the truthful recovery is visible and
reachable through the EXISTING correction path and OD-R1 exit.
"""
import pytest
from playwright.sync_api import expect

import web.app as webapp
from web.ui_text import text
from engine.idea_state import PHYSICAL_FEASIBILITY, ACCEPTED_RISK
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_safe_question_routing_pf_q2 import SEED, MECH, PF_STRONG, BA_1, BA_2

WEAK = "I am not sure yet."


def _start_mechanical(page, base, lang):
    page.goto(base + "/")
    if lang == "ar":
        page.get_by_role("button", name="العربية", exact=True).click()
    page.fill("#idea", SEED)
    page.click("main input[type=submit], main button[type=submit]")
    page.wait_for_load_state()
    choice = page.locator('input[name=domain_choice][value="mechanical"]')
    if choice.count():
        choice.check()
        page.click("main input[type=submit], main button[type=submit]")
        page.wait_for_load_state()
    confirm = page.locator("input[name=domain_confirm]")
    assert confirm.input_value() == "mechanical"
    confirm.check()
    page.click("main input[type=submit], main button[type=submit]")
    page.wait_for_load_state()
    return page.url.rsplit("/session/", 1)[1].split("?")[0]


def _answer(page, value):
    page.locator("#response").fill(value)
    page.locator("#answer-form button[type=submit]").click()
    page.wait_for_load_state()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_weak_pf_no_question_state_is_safe_and_recoverable(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_mechanical(page, server, lang)
    for value in (MECH, MECH, WEAK, BA_1, BA_2):
        _answer(page, value)
    # no null question, no answer form — the recovery renders instead
    assert page.locator("p.question").count() == 0
    assert page.locator("#answer-form").count() == 0
    assert "None" not in page.locator("main").inner_text().split()
    recovery = page.locator("#routed-recovery")
    expect(recovery).to_be_visible()
    expect(recovery).to_contain_text(text("UI_NR_RECOVERY_HEADING", lang))
    assert page.locator("div.routed-need").count() == 1
    assert page.locator("details.routed-accept-risk").count() == 0
    primary = page.locator("[data-primary-action]")
    assert primary.count() == 1
    assert primary.get_attribute("href") == "#routed-recovery"
    # the recovery link reaches the EXISTING correction form, preselected
    page.locator("a.routed-recovery-correct").click()
    weak_id = next(r.record_id for r in webapp.SESSION_STORE[sid]["state"].assertions
                   if r.gap_context == PHYSICAL_FEASIBILITY and r.content == WEAK)
    expect(page.locator("#correct-target")).to_have_value(weak_id)
    page.locator("#correct-response").fill(PF_STRONG)
    page.locator("details.correct-answer form button[type=submit]").click()
    page.wait_for_load_state()
    # the substantive attempt re-opens the existing OD-R1 exit for routed PF
    offer = page.locator("details.routed-accept-risk")
    expect(offer).to_have_count(1)
    offer.locator("summary").click()
    offer.locator("input[name=risk_confirm]").check()
    offer.locator("button[type=submit]").click()
    page.wait_for_load_state()
    state = webapp.SESSION_STORE[sid]["state"]
    assert state.get_gap(PHYSICAL_FEASIBILITY).status == ACCEPTED_RISK
    assert page.locator("div.routed-need").count() == 1      # still outstanding
    assert page.locator("#routed-recovery").count() == 0
    assert all(r.gap_context is not None for r in state.assertions)
    assert page.locator("html").get_attribute("lang") == lang
    assert not errors
