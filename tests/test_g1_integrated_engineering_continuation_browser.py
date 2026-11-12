"""Real Chromium + the existing Flask server: G1-INTEGRATED-ENGINEERING-CONTINUATION-01 (EN and AR).

Synthetic data only. An integrated invention is started through the real composition form and its
focus and other-part questions are answered through the real forms; the inventor then FOLLOWS the
Project Compass primary action at each step: the interaction declaration opens on the session page,
the Component Inventory opens on the session page, the participation form opens on the interaction
page, and the optional planar clearance link (secondary, never primary) opens the existing check.
Exactly one primary action every time; Arabic is RTL; no horizontal overflow at 390 px.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import _no_overflow, _start_integrated
from tests.test_safe_question_routing_pf_q2 import MECH as MECH_ANSWER, MECH_2 as MECH_ANSWER_2, PF_STRONG, BA_1, BA_2


def _compass_action(page, server, sid, kind):
    page.goto(f"{server}/session/{sid}")
    primary = page.locator("[data-primary-action]")
    expect(primary).to_have_count(1)
    assert primary.get_attribute("data-ijg-action") == kind
    return primary


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_the_compass_leads_from_parts_to_the_clearance_check(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, lang, "mechanical")
    for value in (MECH_ANSWER, MECH_ANSWER_2, PF_STRONG, BA_1, BA_2):
        page.goto(f"{server}/session/{sid}")
        page.fill("#response", value)
        page.locator("#answer-form button[type=submit]").click()
        page.wait_for_load_state()
    _compass_action(page, server, sid, "part_questions").click()
    page.wait_for_load_state()
    areas = page.locator("textarea[name^=part_answer__]")
    for i in range(areas.count()):
        areas.nth(i).fill("My own words about it.")
    page.locator("textarea[name^=part_answer__]").first.locator("xpath=ancestor::form").locator(
        "button[type=submit]").click()
    page.wait_for_load_state()

    # 1. the interaction declaration opens where the Compass points
    primary = _compass_action(page, server, sid, "declare_interaction")
    expect(primary).to_have_text(text("UI_IJG_DECLARE_CTA", lang))
    _no_overflow(page, '[data-pc-row="do"]')
    page.set_viewport_size({"width": 1280, "height": 900})
    primary.click()
    expect(page.locator("#interface_description")).to_be_visible()
    page.fill("#interface_description", "The board sits inside the case.")
    form = page.locator("#interface_description").locator("xpath=ancestor::form")
    form.locator("input[name=interface_confirm]").check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()

    # 2. the Component Inventory opens where the Compass points
    for name in ("Control board", "Plastic case"):
        primary = _compass_action(page, server, sid, "component_inventory")
        primary.click()
        expect(page.locator("#component_name")).to_be_visible()
        page.fill("#component_name", name)
        page.fill("#component_function", "Does its job")
        page.locator("[data-ci-form] button[type=submit]").click()
        page.wait_for_load_state()

    # 3. the participation form on the interaction page
    _compass_action(page, server, sid, "participation").click()
    page.wait_for_load_state()
    assert f"/session/{sid}/interface-preparation" in page.url
    boxes = page.locator("[data-icp-form] input[name=participant]")
    expect(boxes).to_have_count(2)
    boxes.nth(0).check()
    boxes.nth(1).check()
    page.locator("[data-icp-form] button[type=submit]").click()
    page.wait_for_load_state()

    # 4. the optional, secondary clearance link opens the existing check
    _compass_action(page, server, sid, "interface_preparation")
    link = page.locator("[data-ijg-clearance-link]")
    expect(link).to_have_count(1)
    assert link.get_attribute("data-primary-action") is None
    expect(page.locator("[data-ijg-clearance]")).to_contain_text(text("UI_IJG_CLEARANCE_NOTE", lang))
    _no_overflow(page, '[data-pc-row="do"]')
    page.set_viewport_size({"width": 1280, "height": 900})
    link.click()
    page.wait_for_load_state()
    assert "/interface-clearance/" in page.url
    assert page.locator("[data-pcc-form]").count() == 1
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
