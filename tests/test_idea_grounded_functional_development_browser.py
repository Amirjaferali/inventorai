"""Real Chromium + the existing Flask server: IDEA-GROUNDED-FUNCTIONAL-DEVELOPMENT-02
(EN and AR).

Synthetic idea only. A Mechanical idea whose own statement says the inventor
does not know how the spring transfers force: the first question served is the
committed question about how parts move and transfer force, the page says why
it was chosen and that the statement is not an answer, ONE primary action
stands, and after the answer the journey resumes at the displaced question.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from engine.path_n_questions import get_served_question
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_idea_grounded_functional_development import GATE, MECH, MC, Q2_ANSWER


def _start_mechanical(page, base, lang):
    page.goto(base + "/")
    if lang == "ar":
        page.get_by_role("button", name="العربية", exact=True).click()
    page.fill("#idea", GATE)
    page.click("main input[type=submit], main button[type=submit]")
    page.wait_for_load_state()
    choice = page.locator(f'input[name=domain_choice][value="{MECH}"]')
    if choice.count():
        choice.check()
        page.click("main input[type=submit], main button[type=submit]")
        page.wait_for_load_state()
    confirm = page.locator("input[name=domain_confirm]")
    assert confirm.input_value() == MECH
    confirm.check()
    page.click("main input[type=submit], main button[type=submit]")
    page.wait_for_load_state()


def _q(index, lang):
    served = get_served_question(MC, index, domain=MECH)
    return served.text if lang == "en" else served.text_ar


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_the_stated_unknown_chooses_the_first_question(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    _start_mechanical(page, server, lang)
    question = page.locator("p.question")
    expect(question).to_have_count(1)
    expect(question).to_have_text(_q(1, lang))
    block = page.locator("#grounded-need")
    expect(block).to_be_visible()
    expect(block.locator("[data-grounded-focus]")).to_have_text(text("UI_GFN_CHOSEN", lang))
    expect(block).to_contain_text(text("UI_GFN_BINDING_QUESTION", lang))
    expect(page.locator("[data-primary-action]")).to_have_count(1)

    page.locator("#response").fill(Q2_ANSWER)
    page.locator("#answer-form button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("p.question")).to_have_text(_q(0, lang))
    expect(page.locator("[data-grounded-focus]")).to_have_count(0)
    expect(page.locator("[data-primary-action]")).to_have_count(1)
    assert errors == []
