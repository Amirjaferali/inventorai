"""Real Chromium + the existing Flask server: G1-PCC-LITERAL-SOURCE-AID-01 (EN and AR).

Synthetic data only. An integrated project whose original idea states ONE literal board pair reaches
the existing planar clearance page through the real forms. The aid shows the passage; its controls
appear only with the script. Nothing is applied until the inventor has chosen the board component
in the form AND an explicit X / Y assignment; the reversed choice fills ONLY the two board values and
the board note; a later change of a board value or of the choice removes only the aid's own unedited
note, never an inventor-edited one; a second apply never overwrites; no component, region, other
value or declaration is touched; the existing save records exactly what the inventor submits. At
phone width nothing overflows, and the Arabic page is RTL.
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
def test_literal_aid_needs_the_board_and_an_explicit_choice_and_fills_only_empty_fields(
        server, page, lang):
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
    board, case = NAMES[lang]

    def board_fields():
        return (page.input_value("#pcc-v-board_x"), page.input_value("#pcc-v-board_y"),
                page.input_value("#pcc-basis_board"))

    # no board chosen: nothing is applied, even with an assignment chosen
    box.locator("input[name=pcc_aid_order][value=first_y]").check()
    apply.click()
    expect(status).to_have_text(text("UI_PCC_AID_MSG_BOARD_FIRST", lang))
    assert board_fields() == ("", "", "")
    assert form.locator("#pcc-board").input_value() == ""                # never chosen for them

    # board chosen by the inventor, no assignment yet: nothing is applied
    form.locator("#pcc-board").select_option(label=board)
    page.reload()
    page.wait_for_load_state()
    form.locator("#pcc-board").select_option(label=board)
    apply.click()
    expect(status).to_have_text(text("UI_PCC_AID_MSG_CHOOSE", lang))
    assert board_fields() == ("", "", "")

    # the inventor reverses the order: only the two board values and the note are filled
    box.locator("input[name=pcc_aid_order][value=first_y]").check()
    apply.click()
    expect(status).to_have_text(text("UI_PCC_AID_MSG_DONE", lang))
    x, y, note = board_fields()
    assert (x, y) == ("56", "85")
    assert note.startswith("من فكرتي الأصلية: " if lang == "ar" else "From my original idea: ")
    for role in ("region_x", "region_y", "c"):
        assert page.input_value("#pcc-v-%s" % role) == ""
    assert form.locator("#pcc-enclosure").input_value() == ""
    assert form.locator("input[type=radio]:checked").count() == 0        # no declaration answered
    assert page.input_value("#pcc-region") == ""

    # a second apply never overwrites
    box.locator("input[name=pcc_aid_order][value=first_x]").check()      # changing the choice ...
    expect(status).to_have_text(text("UI_PCC_AID_MSG_NOTE_CLEARED", lang))
    assert board_fields() == ("56", "85", "")                            # ... removes only the note
    apply.click()
    expect(status).to_have_text(text("UI_PCC_AID_MSG_OCCUPIED", lang))
    assert board_fields() == ("56", "85", "")
    _no_overflow(page, "[data-pcc-aid]")
    page.set_viewport_size({"width": 1280, "height": 900})

    # empty the fields and apply again; then an edited value removes the unedited proposal
    page.fill("#pcc-v-board_x", "")
    page.fill("#pcc-v-board_y", "")
    apply.click()
    expect(status).to_have_text(text("UI_PCC_AID_MSG_DONE", lang))
    assert board_fields()[:2] == ("85", "56")
    page.fill("#pcc-v-board_x", "86")
    expect(status).to_have_text(text("UI_PCC_AID_MSG_NOTE_CLEARED", lang))
    assert board_fields() == ("86", "56", "")

    # changing the BOARD after applying removes the unedited proposal
    page.fill("#pcc-v-board_x", "")
    page.fill("#pcc-v-board_y", "")
    apply.click()
    expect(status).to_have_text(text("UI_PCC_AID_MSG_DONE", lang))
    form.locator("#pcc-board").select_option(label=case)
    expect(status).to_have_text(text("UI_PCC_AID_MSG_NOTE_CLEARED", lang))
    assert board_fields() == ("85", "56", "")
    form.locator("#pcc-board").select_option(label=board)

    # a note the inventor has edited is theirs: a later change keeps it and asks for a review
    page.fill("#pcc-v-board_x", "")
    page.fill("#pcc-v-board_y", "")
    apply.click()
    proposed = page.input_value("#pcc-basis_board")
    page.fill("#pcc-basis_board", proposed + " Checked with calipers.")
    page.fill("#pcc-v-board_y", "57")
    expect(status).to_have_text(text("UI_PCC_AID_MSG_NOTE_REVIEW", lang))
    assert board_fields() == ("85", "57", proposed + " Checked with calipers.")

    # the inventor completes the existing form; the existing save records exactly that
    form.locator("#pcc-enclosure").select_option(label=case)
    page.fill("#pcc-region", REGION[lang])
    for role, value in (("region_x", "95"), ("region_y", "95"), ("c", "2")):
        page.fill("#pcc-v-%s" % role, value)
    for fieldset in form.locator("[data-pcc-decl]").all():
        fieldset.locator("input[value=applies]").check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-pcc-notice]")).to_have_text(text("UI_PCC_MSG_SAVED", lang))
    expect(page.locator("[data-pcc-outcome]")).to_have_attribute("data-pcc-outcome", "MET")
    assert board_fields() == ("85", "57", proposed + " Checked with calipers.")
    assert errors == []


def test_a_proposed_note_loaded_with_the_page_is_removed_when_a_value_changes(server, page):
    """A saved declaration whose board note is still exactly the proposal: on the correction page,
    changing a board value removes that unedited proposal instead of leaving it describing the
    old assignment (follow-up review finding)."""
    lang = "en"
    _start(page, server, lang)
    _prepare(page, lang)
    page.locator("[data-pcc-link] a").first.click()
    page.wait_for_load_state()
    form = page.locator("[data-pcc-form]")
    box = page.locator("[data-pcc-aid]")
    board, case = NAMES[lang]
    form.locator("#pcc-board").select_option(label=board)
    box.locator("input[name=pcc_aid_order][value=first_x]").check()
    box.locator("[data-pcc-aid-apply]").click()
    proposed = page.input_value("#pcc-basis_board")
    form.locator("#pcc-enclosure").select_option(label=case)
    page.fill("#pcc-region", REGION[lang])
    for role, value in (("region_x", "95"), ("region_y", "95"), ("c", "2")):
        page.fill("#pcc-v-%s" % role, value)
    for fieldset in form.locator("[data-pcc-decl]").all():
        fieldset.locator("input[value=applies]").check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-pcc-notice]")).to_have_text(text("UI_PCC_MSG_SAVED", lang))
    page.goto(page.url)
    page.wait_for_load_state()
    assert page.input_value("#pcc-basis_board") == proposed          # loaded from the saved record
    page.fill("#pcc-v-board_x", "90")
    expect(page.locator("[data-pcc-aid-status]")).to_have_text(text("UI_PCC_AID_MSG_NOTE_CLEARED", lang))
    assert page.input_value("#pcc-basis_board") == ""
    assert page.input_value("#pcc-v-board_y") == "56"
