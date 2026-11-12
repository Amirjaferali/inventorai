"""Real Chromium + the existing Flask server: G1-ROUTED-RECOVERY-CONTINUATION-01 (EN and AR).

Synthetic data only. An integrated invention is started through the real composition form; its
focus questions are answered through the real answer form with ONE non-substantive Physical
Feasibility answer, so routed recovery is the Compass primary action. The secondary link the
existing guidance owner derives is visible beside it (never primary), states its boundary and
opens the existing part-question form. Exactly one primary action; Arabic is RTL; no horizontal
overflow at 390 px.
"""
import pytest
from playwright.sync_api import expect

from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import _no_overflow, _start_integrated
from tests.test_safe_question_routing_pf_q2 import MECH as MECH_ANSWER, MECH_2 as MECH_ANSWER_2, BA_1, BA_2
from tests.test_safe_question_routing_pf_q2_weak_recovery import WEAK
from web.ui_text import text


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_routed_recovery_shows_one_secondary_integrated_step(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    _start_integrated(page, server, lang, "mechanical")
    sid = page.url.rsplit("/session/", 1)[1].split("?")[0].split("#")[0]
    for value in (MECH_ANSWER, MECH_ANSWER_2, WEAK, BA_1, BA_2):
        page.goto(f"{server}/session/{sid}")
        page.fill("#response", value)
        page.locator("#answer-form button[type=submit]").click()
        page.wait_for_load_state()
    page.goto(f"{server}/session/{sid}")
    primary = page.locator("[data-primary-action]")
    expect(primary).to_have_count(1)
    assert primary.get_attribute("href") == "#routed-recovery"
    block = page.locator("[data-rrc]")
    expect(block).to_have_count(1)
    expect(block.locator("[data-rrc-note]")).to_have_text(text("UI_RRC_NOTE", lang))
    link = block.locator("[data-rrc-link]")
    expect(link).to_have_text(text("UI_IJG_PART_CTA_ELEC", lang))
    assert link.get_attribute("data-primary-action") is None
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    _no_overflow(page, "[data-rrc]")
    page.set_viewport_size({"width": 1280, "height": 900})
    link.click()
    page.wait_for_load_state()
    assert f"/session/{sid}/part-questions" in page.url
    assert page.locator("textarea[name^=part_answer__]").count() > 0
    assert not errors, errors
