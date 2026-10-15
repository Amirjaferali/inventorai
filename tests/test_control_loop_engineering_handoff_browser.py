"""Real Chromium + the existing Flask server: CONTROL-LOOP-ENGINEERING-HANDOFF-01 (EN and AR, desktop and phone
width).

Synthetic invention data only. An integrated Mechanical + Electrical / Electronics invention with the optional
control-loop part is started through the real composition form; the inventor saves one answer on the
control-loop part's question page, then opens the report: the section shows the part's governed questions
verbatim (LTR-isolated), the saved answer verbatim with the OWNER_STATED / UNVALIDATED label, "not recorded" for
the unanswered questions and the safety disclosure; no control inside it. No horizontal overflow at 390 px
(a long unbroken answer included); RTL in Arabic.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import ELEC_PART, MECH_PART, SUBMIT, TIE_IDEA

ANSWER = "Room temperature — درجة حرارة الغرفة " + "x" * 120


def _start_three_part(page, base, lang, focus):
    page.goto(base + "/")
    if lang == "ar":
        page.get_by_role("button", name="العربية", exact=True).click()
    page.fill("#idea", TIE_IDEA)
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
    page.fill("#mech_part_name", MECH_PART)
    page.fill("#mech_part_function", "Swings the window open and closed")
    page.fill("#elec_part_name", ELEC_PART)
    page.fill("#elec_part_function", "Switches battery power to the motor")
    page.fill("#ctrl_part_name", "Thermostat logic")
    page.fill("#ctrl_part_function", "Compares the temperature with the target")
    form.locator("input[name=initial_focus][value=%s]" % focus).check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    assert "/session/" in page.url
    return page.url.rsplit("/session/", 1)[1].split("?")[0]


@pytest.mark.parametrize("lang,width,focus", [("en", 1280, "mechanical"), ("ar", 390, "mechanical"),
                                              ("en", 390, "electronics_electrical"),
                                              ("ar", 1280, "electronics_electrical")])
def test_report_shows_the_control_loop_answers(server, page, lang, width, focus):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.set_viewport_size({"width": width, "height": 900})
    sid = _start_three_part(page, server, lang, focus)
    page.goto(f"{server}/session/{sid}/part-questions")
    page.locator("textarea").first.fill(ANSWER)
    page.get_by_role("button", name=text("UI_PQ_SAVE", lang)).click()
    page.wait_for_load_state()

    page.goto(f"{server}/session/{sid}/deliverable")
    block = page.locator("[data-control-loop-answers]")
    expect(block).to_have_count(1)
    expect(block).to_be_visible()
    expect(block.locator("h3")).to_have_text(text("UI_CLR_TITLE", lang))
    expect(block.locator("[data-clr-intro]")).to_have_text(text("UI_CLR_INTRO", lang))
    expect(block.locator("[data-clr-answer]")).to_have_text([ANSWER])
    assert block.locator("[data-clr-answer]").get_attribute("dir") == "auto"
    expect(block.locator("[data-clr-provenance]")).to_have_text([text("UI_PQRR_PROVENANCE", lang)])
    expect(block.locator("[data-clr-safety]")).to_have_text(text("UI_PQ_SAFETY_SCOPE", lang))
    questions = block.locator("[data-clr-question]")
    assert questions.count() == 10 and questions.first.get_attribute("dir") == "ltr"
    assert block.locator("[data-clr-not-recorded]").count() == 9
    assert block.locator("[data-clr-unavailable]").count() == 0
    assert block.locator("a, button, form, input, select, textarea").count() == 0
    expect(page.locator(".safety-signals")).not_to_contain_text("Room temperature")
    expect(page.locator("[data-nonfocused-part-answers]")).not_to_contain_text("Room temperature")

    viewport = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= viewport + 1
    assert block.bounding_box()["width"] <= viewport
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
