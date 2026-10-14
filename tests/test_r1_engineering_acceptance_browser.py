"""Real Chromium + the existing Flask server: R1-ENGINEERING-ACCEPTANCE-PROOF-01
(EN and AR, phone and desktop width).

Only the two user-facing paths that no earlier browser test drives:

* Mechanical — the governed questions are answered in the browser; the
  report then explains the routed, still-partial feasibility gap with its
  next steps and reference fundamentals; the CAP-12 form mock-up advisory is
  opened from the session page's own link and returns its alternatives.
* Integrated — a THREE-part invention (Mechanical + Electrical / Electronics +
  the one optional third part) is created through the real composition
  form; an interface is declared and its verification preparation is saved
  through the real forms; the read-only Parts, Components & Interactions view
  shows the result.

Each page is checked for no horizontal overflow, `lang` and RTL. The other
acceptance behaviours already have real-browser proof in their own suites
(see the R1 acceptance record). Synthetic invention data only.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_safe_question_routing_pf_q2 import BA_1, BA_2, MECH, PF_STRONG
from tests.test_safe_question_routing_pf_q2_weak_recovery_browser import _answer, _start_mechanical

SUBMIT = "main input[type=submit], main button[type=submit]"
TIE_IDEA = "circuit and hinge"
PARTS = {"mech_part_name": "Hinge arm",
         "mech_part_function": "Swings the window open and closed",
         "elec_part_name": "لوحة تشغيل المحرك",       # an Arabic declared name on purpose
         "elec_part_function": "Switches battery power to the motor",
         "ctrl_part_name": "Thermostat logic",
         "ctrl_part_function": "Compares the temperature with the target"}
INTERFACE = "The motor board drives the hinge arm through a geared motor."
PREPARATION = ("Indoor use at room temperature.",
               "The arm reaches the open stop within 5 seconds.",
               "A timed video of each cycle.")


def _fits(page, lang):
    """No horizontal page overflow, correct language and direction."""
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"


def _both_widths(page, lang):
    for width in (390, 1280):
        page.set_viewport_size({"width": width, "height": 900})
        _fits(page, lang)


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_mechanical_report_and_cap12_advisory(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.set_viewport_size({"width": 390, "height": 900})
    sid = _start_mechanical(page, server, lang)
    for value in (MECH, MECH, PF_STRONG, BA_1, BA_2):
        _answer(page, value)
    expect(page.locator("#answer-form")).to_have_count(0)  # the governed questions are done

    page.goto(server + "/session/%s/deliverable" % sid)
    page.wait_for_load_state()
    expect(page.locator('[data-cap01-gap="physical-feasibility"]')).to_have_count(1)
    expect(page.locator("[data-cap01-next-steps]")).to_have_count(1)
    expect(page.locator('[data-cap01-fundamentals="force-moment-pressure-v1"]')).to_have_count(1)
    _both_widths(page, lang)

    page.goto(server + "/session/%s" % sid)
    page.wait_for_load_state()
    link = page.locator("[data-cap12-link] a")
    expect(link).to_have_count(1)
    expect(link).to_have_text(text("UI_CAP12_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    _both_widths(page, lang)

    page.fill("#cap12-name", "Ramp handle shell")
    page.fill("#cap12-function", "Shows the shape of the grip for review.")
    page.select_option("#cap12-role", "form_mockup")
    page.click(SUBMIT)
    page.wait_for_load_state()
    expect(page.locator('[data-cap12-result="available"]')).to_have_count(1)
    assert page.locator("[data-cap12-alternative]").count() >= 2
    _both_widths(page, lang)
    assert not errors


def _start_three_part(page, base, lang):
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
    expect(form.locator("[data-optional-part]")).to_have_count(1)
    _fits(page, lang)
    form.locator("input[name=composition_answer][value=yes]").check()
    for field, value in PARTS.items():
        page.fill("#" + field, value)
    form.locator("input[name=initial_focus][value=mechanical]").check()
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    assert "/session/" in page.url


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_three_part_invention_interface_and_preparation(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.set_viewport_size({"width": 390, "height": 900})
    _start_three_part(page, server, lang)
    _both_widths(page, lang)

    declare = page.locator("#declare-interface")
    declare.locator("summary").click()
    pairs = declare.locator("input[name=interface_binding]")
    assert pairs.count() == 3                               # every pair of the three parts
    pairs.first.check()
    declare.locator("#interface_description").fill(INTERFACE)
    declare.locator("input[name=interface_confirm]").check()
    declare.get_by_role("button", name=text("UI_S15_IFC_BUTTON", lang)).click()
    page.wait_for_load_state()

    page.locator("[data-prep-link] a").click()
    page.wait_for_load_state()
    for n, value in enumerate(PREPARATION, 1):
        page.fill("#prep-1-%d" % n, value)
    page.get_by_role("button", name=text("UI_S15_PREP_SAVE", lang)).click()
    page.wait_for_load_state()
    expect(page.locator("[data-prep-notice]")).to_have_count(1)
    _both_widths(page, lang)

    sid = page.url.rsplit("/session/", 1)[1].split("/")[0]
    page.goto(server + "/session/%s/parts-components-interactions" % sid)
    page.wait_for_load_state()
    expect(page.locator("[data-pci-part-name]")).to_have_text(
        [PARTS["mech_part_name"], PARTS["elec_part_name"], PARTS["ctrl_part_name"]])
    view = page.locator("main").inner_text()
    for value in (INTERFACE,) + PREPARATION:
        assert value in view, value
    _both_widths(page, lang)
    assert not errors
