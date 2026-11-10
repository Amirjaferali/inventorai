"""Real Chromium + the existing Flask server: G1-UQTR-INTEGRATED-CONTINUATION-01 (EN and AR).

Synthetic data only. An Electrical / Electronics-focus integrated invention is started through
the real composition form; its focus questions are answered in ordinary words through the real
answer form until the point moves on, and then the inventor records "a specialist is needed"
through the real form. The UQTR primary action ("Review what is still needed") stays the only
primary action; the secondary link the existing guidance owner derives is visible beside it,
states its boundary and opens the existing part-question form. Arabic is RTL; no horizontal
overflow at 390 px.
"""
import pytest
from playwright.sync_api import expect

from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import _no_overflow, _start_integrated
from tests.test_g1_uqtr_integrated_continuation import ORDINARY
from web.ui_text import text

CONTEXT = ".current-question-context strong"


def _submit(page):
    page.locator("#answer-form button[type=submit]").click()
    page.wait_for_load_state()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_suppressed_question_shows_one_secondary_integrated_step(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    _start_integrated(page, server, lang, "electronics_electrical")
    sid = page.url.rsplit("/session/", 1)[1].split("?")[0].split("#")[0]
    page.goto(f"{server}/session/{sid}")
    first_point = page.locator(CONTEXT).inner_text()
    for value in ORDINARY * 2:                     # ordinary words until the next point is served
        page.goto(f"{server}/session/{sid}")
        if page.locator(CONTEXT).inner_text() != first_point:
            break
        page.fill("#response", value)
        _submit(page)
    page.goto(f"{server}/session/{sid}")
    assert page.locator(CONTEXT).inner_text() != first_point
    page.locator("#answer-form input[name=action][value=specialist_requested]").check()
    page.fill("#response", "I need an engineer to look at this.")
    _submit(page)

    page.goto(f"{server}/session/{sid}")
    primary = page.locator("[data-primary-action]")
    expect(primary).to_have_count(1)
    assert primary.get_attribute("href").endswith(f"/session/{sid}/deliverable")
    expect(primary).to_have_text(text("UI_UQTR_CTA", lang))
    block = page.locator("[data-uqc]")
    expect(block).to_have_count(1)
    expect(block.locator("[data-uqc-note]")).to_have_text(text("UI_UQC_NOTE", lang))
    link = block.locator("[data-uqc-link]")
    expect(link).to_have_text(text("UI_IJG_PART_CTA_MECH", lang))
    assert link.get_attribute("data-primary-action") is None
    expect(page.locator("[data-rrc]")).to_have_count(0)
    expect(page.locator("details.uqtr-revisit")).to_have_count(1)     # the question stays revisitable
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    _no_overflow(page, "[data-uqc]")
    page.set_viewport_size({"width": 1280, "height": 900})
    link.click()
    page.wait_for_load_state()
    assert f"/session/{sid}/part-questions" in page.url
    assert page.locator("textarea[name^=part_answer__]").count() > 0
    assert not errors, errors
