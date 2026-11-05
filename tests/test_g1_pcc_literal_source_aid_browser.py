"""Real Chromium + the existing Flask server: G1-PCC-LITERAL-SOURCE-AID-01 (EN and AR).

Synthetic data only. An integrated project whose original idea states ONE literal board pair reaches
the existing planar clearance page through the real forms. The aid shows the passage; its controls
appear only with the script. Applying without a choice changes nothing; the inventor's explicit
reversed choice fills ONLY the two board values and the board note; a second apply over filled
fields changes nothing; no component, region, other value or declaration is touched; the inventor
then completes the existing form and the existing save records exactly those values. At phone
width nothing overflows, and the Arabic page is RTL.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import SUBMIT, _no_overflow
from tests.test_board_enclosure_planar_clearance_browser import NAMES, REGION, _prepare

IDEA = {"en": "A smart planter that opens its lid on a hinge when the soil is dry. "
              "My circuit board is 85 x 56 mm.",
        "ar": "حوض نباتات ذكي يفتح غطاءه على مفصّلة عندما تجف التربة. مقاس اللوحة 85 × 56 mm."}


def _start(page, base, lang):
    page.goto(base + "/")
    if lang == "ar":
        page.get_by_role("button", name="العربية", exact=True).click()
    page.fill("#idea", IDEA[lang])
    offer = page.locator("input[type=checkbox][name=integrated_invention]")
    for _ in range(3):
        if page.locator("[data-composition-form]").count():
            break
        if offer.count():
            offer.check()
        page.click(SUBMIT)
        page.wait_for_load_state()
    form = page.locator("[data-composition-form]")
    expect(form).to_have_count(1)
    form.locator("input[name=composition_answer][value=yes]").check()
    page.fill("#mech_part_name", "Lid hinge")
    page.fill("#mech_part_function", "Opens the lid")
    page.fill("#elec_part_name", "Controller")
    page.fill("#elec_part_function", "Reads the soil sensor")
    form.locator("input[name=initial_focus][value=mechanical]").check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    assert "/session/" in page.url


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_literal_aid_fills_only_empty_board_fields_after_an_explicit_choice(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    _start(page, server, lang)
    _prepare(page, lang)
    page.locator("[data-pcc-link] a").first.click()
    page.wait_for_load_state()
    assert page.locator("[data-pcc-page]").get_attribute("dir") == ("rtl" if lang == "ar" else "ltr")
    box = page.locator("[data-pcc-aid]")
    expect(box).to_have_count(1)
    expect(box.locator("[data-pcc-aid-passage]")).to_contain_text("85")
    expect(box.locator("[data-pcc-aid-controls]")).to_be_visible()       # the script enabled them
    assert box.locator("input[name=pcc_aid_order]:checked").count() == 0
    form = page.locator("[data-pcc-form]")
    apply = box.locator("[data-pcc-aid-apply]")
    status = box.locator("[data-pcc-aid-status]")

    apply.click()                                                        # no choice: nothing changes
    expect(status).to_have_text(text("UI_PCC_AID_MSG_CHOOSE", lang))
    assert page.input_value("#pcc-v-board_x") == "" and page.input_value("#pcc-basis_board") == ""

    box.locator("input[name=pcc_aid_order][value=first_y]").check()      # the inventor reverses it
    apply.click()
    expect(status).to_have_text(text("UI_PCC_AID_MSG_DONE", lang))
    assert (page.input_value("#pcc-v-board_x"), page.input_value("#pcc-v-board_y")) == ("56", "85")
    note = page.input_value("#pcc-basis_board")
    assert note.startswith("من فكرتي الأصلية: " if lang == "ar" else "From my original idea: ")
    for role in ("region_x", "region_y", "c"):
        assert page.input_value("#pcc-v-%s" % role) == ""
    assert form.locator("#pcc-board").input_value() == ""                # no component chosen
    assert form.locator("#pcc-enclosure").input_value() == ""
    assert form.locator("input[type=radio]:checked").count() == 0        # no declaration answered
    assert page.input_value("#pcc-region") == ""

    box.locator("input[name=pcc_aid_order][value=first_x]").check()      # never overwrites
    apply.click()
    expect(status).to_have_text(text("UI_PCC_AID_MSG_OCCUPIED", lang))
    assert (page.input_value("#pcc-v-board_x"), page.input_value("#pcc-v-board_y")) == ("56", "85")
    assert page.input_value("#pcc-basis_board") == note
    _no_overflow(page, "[data-pcc-aid]")
    page.set_viewport_size({"width": 1280, "height": 900})

    board, case = NAMES[lang]                                            # the inventor completes it
    form.locator("#pcc-board").select_option(label=board)
    form.locator("#pcc-enclosure").select_option(label=case)
    page.fill("#pcc-region", REGION[lang])
    for role, value in (("region_x", "90"), ("region_y", "90"), ("c", "2")):
        page.fill("#pcc-v-%s" % role, value)
    for fieldset in form.locator("[data-pcc-decl]").all():
        fieldset.locator("input[value=applies]").check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-pcc-notice]")).to_have_text(text("UI_PCC_MSG_SAVED", lang))
    expect(page.locator("[data-pcc-outcome]")).to_have_attribute("data-pcc-outcome", "MET")
    assert (page.input_value("#pcc-v-board_x"), page.input_value("#pcc-v-board_y")) == ("56", "85")
    assert page.input_value("#pcc-basis_board") == note

    # a value changed after the note was proposed is refused and nothing is written
    page.fill("#pcc-v-board_x", "57")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-pcc-error]")).to_have_text(text("UI_PCC_AID_MSG_NOTE_MISMATCH", lang))
    page.goto(page.url)
    assert page.input_value("#pcc-v-board_x") == "56"
    assert errors == []
