"""Real Chromium + the existing Flask server: G1-INTEGRATED-JOURNEY-RECOVERY-01 (EN and AR).

Synthetic data only. A board-inside-enclosure idea is started as an ordinary single-focus project
through the real start form (the integrated box left unticked); the inventor then follows the
session page's secondary recovery form (the acknowledgement is required by the browser), lands on the
EXISTING composition clarification showing the full original idea, declares both parts and a focus,
and arrives on a NEW integrated session. The original session keeps its offer. Arabic is RTL; no
horizontal overflow at 390 px; the recovery form is never the primary action.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import _no_overflow
from tests.test_g1_integrated_journey_recovery import BOARD_IDEA

SUBMIT = "form[action='/start'] button[type=submit]"


def _start_single(page, base, lang):
    page.goto(base + "/")
    if lang == "ar":
        page.get_by_role("button", name="العربية", exact=True).click()
    page.fill("#idea", BOARD_IDEA)
    page.click(SUBMIT)
    page.wait_for_load_state()
    page.locator("input[name=domain_confirm]").check()
    page.click(SUBMIT)
    page.wait_for_load_state()
    assert "/session/" in page.url
    return page.url.rsplit("/session/", 1)[1].split("?")[0].split("#")[0]


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_a_single_project_recovers_into_a_separate_integrated_project(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_single(page, server, lang)
    section = page.locator("[data-integrated-restart]")
    expect(section).to_have_count(1)
    expect(section).to_contain_text(text("UI_IJR_NOTE", lang))
    assert section.locator("[data-primary-action]").count() == 0
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    _no_overflow(page, "[data-integrated-restart]")
    page.set_viewport_size({"width": 1280, "height": 900})

    # The browser itself requires the acknowledgement: an unticked submit stays on the page.
    page.locator("[data-ijr-submit]").click()
    assert page.url.split("#")[0].endswith(f"/session/{sid}")
    expect(page.locator("[data-composition-form]")).to_have_count(0)
    page.locator("[data-ijr-ack]").check()
    page.locator("[data-ijr-submit]").click()
    page.wait_for_load_state()

    form = page.locator("[data-composition-form]")
    expect(form).to_have_count(1)
    expect(page.locator(".composition-idea")).to_have_text(BOARD_IDEA)
    assert form.locator("input[type=radio]:checked").count() == 0
    _no_overflow(page, "[data-composition-form]")
    page.set_viewport_size({"width": 1280, "height": 900})
    form.locator("input[name=composition_answer][value=yes]").check()
    page.fill("#mech_part_name", "Plastic enclosure")
    page.fill("#mech_part_function", "Holds and protects the board")
    page.fill("#elec_part_name", "Control board")
    page.fill("#elec_part_function", "Reads the sensor and lights the LED")
    form.locator("input[name=initial_focus][value=mechanical]").check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()

    assert "/session/" in page.url
    new = page.url.rsplit("/session/", 1)[1].split("?")[0].split("#")[0]
    assert new != sid
    expect(page.locator("[data-integrated-scope]")).to_have_count(1)
    expect(page.locator("[data-integrated-restart]")).to_have_count(0)
    expect(page.locator("[data-primary-action]")).to_have_count(1)
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"

    page.goto(f"{server}/session/{sid}")
    expect(page.locator("[data-integrated-restart]")).to_have_count(1)
    expect(page.locator("[data-integrated-scope]")).to_have_count(0)
    assert not errors


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_no_returns_the_inventor_to_their_unchanged_project(server, page, lang):
    sid = _start_single(page, server, lang)
    page.locator("[data-ijr-ack]").check()
    page.locator("[data-ijr-submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-ijr-origin-note]")).to_contain_text(text("UI_IJR_ORIGIN_NOTE", lang))
    expect(page.locator("[data-ijr-back]")).to_have_text(text("UI_IJR_BACK", lang))
    page.locator("[data-composition-form] input[name=composition_answer][value=no]").check()
    page.locator("[data-composition-form] button[type=submit]").click()
    page.wait_for_load_state()
    assert f"/session/{sid}" in page.url
    expect(page.locator("[data-ijr-declined]")).to_have_text(text("UI_IJR_DECLINED", lang))
    expect(page.locator("[data-integrated-scope]")).to_have_count(0)
    page.goto(f"{server}/session/{sid}")
    page.locator("[data-ijr-ack]").check()
    page.locator("[data-ijr-submit]").click()
    page.wait_for_load_state()
    page.locator("[data-ijr-back]").click()
    page.wait_for_load_state()
    assert page.url.split("#")[0].split("?")[0].endswith(f"/session/{sid}")
