"""Real Chromium + the existing Flask server: STAGE15-PARTS-COMPONENTS-INTERACTIONS-VIEW-01 (EN and AR,
desktop and phone width, both focus directions).

Synthetic invention data only. An integrated Mechanical + Electrical / Electronics invention is started through
the real composition form; the inventor declares ONE component linked to both parts on the session page, then
follows the session page's link to the read-only view: both parts with their roles, the component shown ONCE
with both part names, the interactions empty state and the disclosures. No horizontal overflow at 390 px; RTL in
Arabic; one h1, labelled sections, named links, no form.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import ELEC_PART, MECH_PART, _start_integrated

COMPONENT = "Hinge motor — محرك المفصلة"
ROLE = {"mechanical": ["UI_PCI_ROLE_FOCUS", "UI_PCI_ROLE_REQUIRED"],
        "electronics_electrical": ["UI_PCI_ROLE_REQUIRED", "UI_PCI_ROLE_FOCUS"]}


@pytest.mark.parametrize("lang,width,focus", [("en", 1280, "mechanical"), ("ar", 390, "mechanical"),
                                              ("en", 390, "electronics_electrical"),
                                              ("ar", 1280, "electronics_electrical")])
def test_parts_components_interactions_view(server, page, lang, width, focus):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.set_viewport_size({"width": width, "height": 900})
    _start_integrated(page, server, lang, focus)

    inventory = page.locator("#component-inventory")
    inventory.locator("summary").click()
    inventory.locator("#component_name").fill(COMPONENT)
    inventory.locator("#component_function").fill("Turns the hinge arm")
    boxes = inventory.locator("input[name=component_part]")
    for i in range(boxes.count()):
        boxes.nth(i).check()
    inventory.get_by_role("button", name=text("UI_CI_BUTTON", lang)).click()
    page.wait_for_load_state()

    link = page.locator("[data-scope-pci-link] a")
    expect(link).to_have_count(1)
    expect(link).to_have_text(text("UI_PCI_LINK", lang))
    link.click()
    page.wait_for_load_state()

    expect(page.locator("h1")).to_have_count(1)
    expect(page.locator("h1")).to_have_text(text("UI_PCI_TITLE", lang))
    expect(page.locator("[data-pci-boundary]")).to_have_text(text("UI_PCI_BOUNDARY", lang))
    expect(page.locator("[data-pci-part-name]")).to_have_text([MECH_PART, ELEC_PART])
    expect(page.locator("[data-pci-part-role]")).to_have_text([text(k, lang) for k in ROLE[focus]])
    expect(page.locator("[data-pci-questions-link]")).to_have_count(1)
    expect(page.locator("[data-pci-questions-link]")).to_have_text(text("UI_PQ_LINK", lang))
    expect(page.locator("[data-pci-component-name]")).to_have_text([COMPONENT])
    expect(page.locator("[data-pci-component-part]")).to_have_text([MECH_PART, ELEC_PART])
    expect(page.locator("[data-pci-unassigned-none]")).to_have_count(1)
    expect(page.locator("[data-pci-interfaces-none]")).to_have_count(1)
    assert page.locator("form").count() <= 1                  # the shared language selector only
    assert page.locator("main form, main input, main textarea").count() == 0
    for region in ("pci-parts-title", "pci-components-title", "pci-interfaces-title"):
        assert page.locator(f"section[aria-labelledby={region}]").count() == 1
    for anchor in page.locator("main a").all():
        assert anchor.inner_text().strip()
    assert page.locator("[data-pci-component-name]").get_attribute("dir") == "auto"

    viewport = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= viewport + 1
    for section in page.locator("section.block").all():
        assert section.bounding_box()["width"] <= viewport
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
