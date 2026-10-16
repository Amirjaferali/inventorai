"""Real Chromium + the existing Flask server: IDEA-GROUNDED-FUNCTIONAL-NEED-01,
the inventor's own explicit unknown shown with the first question (EN and AR).

Synthetic invention data only. The plant-watering idea is entered through the
real /start form and the starting-focus chooser; the served question and the
ONE primary action are unchanged; the grounded-need block sits beside the
question, quotes the inventor verbatim, claims no question connection for
this wording, and the recorded-unknowns panel lists the same statement. After
"not known yet" the journey continues to the next gap (PR #835) and the idea's
unknown still greets it.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_idea_grounded_functional_need import PLANT, ELEC


def _start_electronics(page, base, lang, idea):
    page.goto(base + "/")
    if lang == "ar":
        page.get_by_role("button", name="العربية", exact=True).click()
    page.fill("#idea", idea)
    page.click("main input[type=submit], main button[type=submit]")
    page.wait_for_load_state()
    choice = page.locator(f'input[name=domain_choice][value="{ELEC}"]')
    if choice.count():
        choice.check()
        page.click("main input[type=submit], main button[type=submit]")
        page.wait_for_load_state()
    confirm = page.locator("input[name=domain_confirm]")
    assert confirm.input_value() == ELEC
    confirm.check()
    page.click("main input[type=submit], main button[type=submit]")
    page.wait_for_load_state()
    return page.url.rsplit("/session/", 1)[1].split("?")[0]


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_idea_unknown_greets_the_first_question(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    _start_electronics(page, server, lang, PLANT)

    block = page.locator("#grounded-need")
    expect(block).to_be_visible()
    expect(block).to_contain_text(text("UI_GFN_HEADING", lang))
    expect(block).to_contain_text(PLANT)
    expect(block).to_contain_text(text("UI_GFN_BINDING_NONE", lang))
    expect(block).to_contain_text(text("UI_GFN_BOUNDARY", lang))
    assert block.locator("[data-grounded-source='idea'][data-grounded-binding='none']").count() == 1
    assert block.locator("a, button, form, input, textarea, select").count() == 0
    # beside the question, above the answer form; the ONE primary action stands
    question = page.locator("p.question")
    expect(question).to_have_count(1)
    assert question.bounding_box()["y"] < block.bounding_box()["y"] \
        < page.locator("#answer-form").bounding_box()["y"]
    expect(page.locator("[data-primary-action]")).to_have_count(1)
    # the recorded-unknowns panel lists the same statement, labelled by source
    panel = page.locator("[data-idea-stated-unknown]")
    expect(panel).to_have_count(1)
    expect(panel).to_contain_text(text("UI_GFN_PANEL_IDEA", lang))
    expect(panel).to_contain_text(PLANT)

    # "not known yet": the journey continues (PR #835) and the unknown still greets it
    page.locator('input[name=action][value="unknown"]').check()
    page.locator("#answer-form button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-paused-gap]")).to_have_count(1)
    expect(page.locator("#grounded-need")).to_be_visible()
    expect(page.locator("[data-idea-stated-unknown]")).to_have_count(1)
    expect(page.locator("[data-primary-action]")).to_have_count(1)
    assert errors == []
