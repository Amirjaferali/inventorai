"""Real Chromium + the existing Flask server: G1-CURRENT-ANSWER-DIMENSION-HANDOFF-01 (EN and AR).

Synthetic data only. An integrated project whose original idea states no board size gets ONE
ordinary answer, through the real answer form, that states the board size literally. The existing
planar clearance page then offers those two numbers, labelled as coming from a recorded answer,
with nothing chosen. Only after the inventor chooses the board and an X / Y assignment does the
existing script fill the two board values and the note; the inventor completes the rest and saves
through the existing path, which records exactly what was submitted. The general freshness note
sits beside the values. Arabic is RTL; nothing overflows at 390 px.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import _no_overflow, _start_integrated
from tests.test_board_enclosure_planar_clearance_browser import NAMES, REGION, _prepare

ANSWER = {"en": "My circuit board is 85 x 56 mm.", "ar": "مقاس اللوحة 85 × 56 mm."}
PREFIX = {"en": "From my recorded answer: ", "ar": "من إجابتي المسجّلة: "}


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_a_current_answer_is_offered_and_saved_only_by_the_inventors_choices(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, lang, "mechanical")
    page.goto(f"{server}/session/{sid}")
    page.fill("#response", ANSWER[lang])
    page.locator("#answer-form button[type=submit]").click()
    page.wait_for_load_state()
    page.goto(f"{server}/session/{sid}")
    _prepare(page, lang)
    page.locator("[data-pcc-link] a").first.click()
    page.wait_for_load_state()
    assert page.locator("[data-pcc-page]").get_attribute("dir") == ("rtl" if lang == "ar" else "ltr")

    box = page.locator("[data-pcc-aid]")
    expect(box).to_have_count(1)
    expect(box.locator("h3")).to_have_text(text("UI_PCC_AID_HEADING_ANSWER", lang))
    expect(box.locator("[data-pcc-aid-passage]")).to_contain_text("85")
    expect(page.locator("[data-pcc-aid-conflict]")).to_have_count(0)
    expect(page.locator("[data-pcc-freshness]")).to_have_text(text("UI_PCC_VALUES_FRESHNESS", lang))
    assert box.locator("input[name=pcc_aid_order]:checked").count() == 0
    form = page.locator("[data-pcc-form]")
    assert form.locator("#pcc-board").input_value() == ""                # never chosen for them
    _no_overflow(page, "[data-pcc-aid]")
    page.set_viewport_size({"width": 1280, "height": 900})

    board, case = NAMES[lang]
    form.locator("#pcc-board").select_option(label=board)
    box.locator("input[name=pcc_aid_order][value=first_x]").check()
    box.locator("[data-pcc-aid-apply]").click()
    expect(box.locator("[data-pcc-aid-status]")).to_have_text(text("UI_PCC_AID_MSG_DONE", lang))
    assert (page.input_value("#pcc-v-board_x"), page.input_value("#pcc-v-board_y")) == ("85", "56")
    note = page.input_value("#pcc-basis_board")
    assert note.startswith(PREFIX[lang])
    assert form.locator("#pcc-enclosure").input_value() == ""
    assert form.locator("input[type=radio]:checked").count() == 0        # no declaration answered

    # the inventor completes the form and saves through the existing path
    form.locator("#pcc-enclosure").select_option(label=case)
    page.fill("#pcc-region", REGION[lang])
    for role, value in (("region_x", "90"), ("region_y", "60"), ("c", "2")):
        page.fill("#pcc-v-%s" % role, value)
    for fieldset in form.locator("[data-pcc-decl]").all():
        fieldset.locator("input[value=applies]").check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-pcc-notice]")).to_have_text(text("UI_PCC_MSG_SAVED", lang))
    expect(page.locator("[data-pcc-outcome]")).to_have_attribute("data-pcc-outcome", "MET")
    assert page.input_value("#pcc-basis_board") == note                  # saved exactly as submitted
    assert not errors, errors
