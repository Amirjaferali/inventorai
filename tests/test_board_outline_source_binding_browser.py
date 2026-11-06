"""Real Chromium + the existing Flask server: BOARD-OUTLINE-SOURCE-BINDING-01 in English and Arabic.

Synthetic data only (the committed KiCad 10.0.8 fixture of the #936 proof). With v2 writes
enabled for this test, the inventor chooses the board and the enclosure, picks the file and
inspects it; the offer shows the file outline and saves nothing; the inventor chooses the
axis assignment, declares 80 x 50 (not the file's 84 x 50) and saves. The page then shows
the file link: "File outline: 84 x 50 mm. Your declared board: 80 x 50 mm. Calculation uses
your declared dimensions." with DIFFERS on X, and the comparison uses 80 x 50. With writes
OFF the intake is absent. The Arabic page is RTL with numbers LTR-isolated; nothing overflows
at phone width. Set ``PCC_SCREENSHOT_DIR`` to keep screenshots.
"""
import os

import pytest
from playwright.sync_api import expect

import web.app as appmod
from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import _no_overflow, _start_integrated
from tests.test_board_enclosure_planar_clearance_browser import NAMES, REGION, _prepare, _shot

FIXTURE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs",
                       "benchmarks", "evidence", "kicad10_format_qualification_v1", "fixtures",
                       "k10_board_v1.kicad_pcb")


@pytest.fixture
def writes_on(monkeypatch):
    monkeypatch.setitem(appmod.app.config, "PCC_SOURCE_BINDING_WRITES", True)


def _open_clearance(page, server, lang):
    _start_integrated(page, server, lang, "mechanical")
    _prepare(page, lang)
    page.locator("[data-pcc-link] a").first.click()
    page.wait_for_load_state()
    assert "/interface-clearance/" in page.url


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_inspect_offer_declare_and_show_the_file_link(server, page, writes_on, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    _open_clearance(page, server, lang)
    intake = page.locator("[data-pcc-source-intake]")
    expect(intake.locator("h3")).to_have_text(text("UI_PCC_SRC_HEADING", lang))
    expect(intake.locator("[data-pcc-source-privacy]")).to_have_text(text("UI_PCC_SRC_PRIVACY", lang))
    board, case = NAMES[lang]
    intake.locator("#pcc-src-board").select_option(label=board)
    intake.locator("#pcc-src-enclosure").select_option(label=case)
    intake.locator("#pcc-src-file").set_input_files(FIXTURE)
    intake.locator("button[type=submit]").click()
    page.wait_for_load_state()
    offer = page.locator("[data-pcc-source-offer]")
    expect(offer.locator("[data-pcc-offer-outline]")).to_have_text("X = 84 mm, Y = 50 mm")
    assert "k10_board_v1" not in page.content()                      # the file name is not echoed
    _shot(page, "src_%s_01_offer" % lang)
    form = page.locator("[data-pcc-form]")
    assert form.locator("input[name=source_axis]:checked").count() == 0   # nothing pre-chosen
    form.locator("input[name=source_axis][value=file_x_is_board_x]").check()
    assert form.locator("#pcc-board").input_value() != ""                # board chosen before file
    page.fill("#pcc-region", REGION[lang])
    for role, value in zip(("board_x", "board_y", "region_x", "region_y", "c"),
                           ("80", "50", "86", "56", "2")):
        page.fill("#pcc-v-%s" % role, value)
    for fieldset in form.locator("[data-pcc-decl]").all():
        fieldset.locator("input[value=applies]").check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-pcc-notice]")).to_have_text(text("UI_PCC_MSG_SAVED", lang))
    link = page.locator("[data-pcc-source-link]")
    expect(link).to_have_attribute("data-pcc-agreement", "DIFFERS")
    expect(link.locator("[data-pcc-file-outline]")).to_have_text("84 × 50 mm")
    expect(link.locator("[data-pcc-declared-outline]")).to_have_text("80 × 50 mm")
    expect(link.locator("[data-pcc-changed-axis]")).to_have_text(["X"])
    expect(link.locator("p").first).to_have_text(text("UI_PCC_SRC_LINKED", lang))
    if lang == "en":
        expect(link.locator("[data-pcc-source-dims]")).to_have_text(
            "File outline: 84 × 50 mm. Your declared board: 80 × 50 mm. "
            "Calculation uses your declared dimensions.")
    assert link.locator("[data-pcc-file-outline]").evaluate(
        "e => getComputedStyle(e).direction") == "ltr"
    assert page.locator("[data-pcc-page]").get_attribute("dir") == ("rtl" if lang == "ar" else "ltr")
    # the comparison uses the declared 80 x 50: margins (86-80)/2-2 = 1 and (56-50)/2-2 = 1
    expect(page.locator("[data-pcc-outcome]")).to_have_attribute("data-pcc-outcome", "MET")
    expect(page.locator("[data-pcc-margin]")).to_have_text(["1 mm", "1 mm"])
    _shot(page, "src_%s_02_linked" % lang)
    _no_overflow(page, "[data-pcc-source-link]")
    _shot(page, "src_%s_03_phone" % lang)
    assert not errors


def test_with_writes_off_there_is_no_intake(server, page):
    assert appmod.app.config["PCC_SOURCE_BINDING_WRITES"] is False
    _open_clearance(page, server, "en")
    expect(page.locator("[data-pcc-source-intake]")).to_have_count(0)
    expect(page.locator("[data-pcc-form]")).to_have_count(1)
