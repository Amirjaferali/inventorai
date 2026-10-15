"""Real Chromium: COMPONENT-INTERFACE-PARTICIPATION-01 — the components the inventor says take part in one declared
interaction, on the interaction-preparation page, the Parts, Components & Interactions view and the report
(EN and AR, 390 and 1280 px).

Synthetic data only. Pages are rendered by the real application (Flask test client) and loaded into Chromium; at
every width there is no horizontal overflow, the selection form lists each current component once with a
checkbox, the saved participants read verbatim and direction-isolated (``dir="auto"``) with the boundary shown on
every surface, and Arabic renders RTL.
"""
import glob
import html as _html
import re

import pytest

import web.app as appmod
from tests.csrf_client import csrf_client
from tests.test_stage15_integrated_invention_entry import MECH, TIE_IDEA, _compose, _created
from tests.test_stage15_subsystem_interface_declaration import _declare as _declare_interface
from web import ui_text

LONG = "M" * 80                                          # one unbroken 80-character name
NAMES = {"en": (LONG, "Driver board"), "ar": ("محرك المفصلة", "لوحة التشغيل driver")}


def _pages(lang):
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        if lang == "ar":
            c.post("/ui-language", data={"lang": "ar"})
        sid = _created(_compose(c, TIE_IDEA, focus=MECH))
        assert _declare_interface(c, sid, "Motor turns the hinge").status_code == 302
        for name in NAMES[lang]:
            raw = c.get(f"/session/{sid}").get_data(as_text=True)
            sub = _html.unescape(re.search(r'name="component_submission" value="([^"]*)"', raw).group(1))
            c.post(f"/session/{sid}/declare-component", data={
                "component_submission": sub, "component_name": name, "component_function": "Does its job"})
        raw = c.get(f"/session/{sid}/interface-preparation").get_data(as_text=True)
        form = re.search(r"data-icp-form>.*?</form>", raw, re.S).group(0)
        ifc = _html.unescape(re.search(r'name="interface_id" value="([^"]*)"', form).group(1))
        first = _html.unescape(re.search(r'name="participant" value="([^"]*)"', form).group(1))
        r = c.post(f"/session/{sid}/interface-participation", data={
            "interface_id": ifc, "participant_base": "", "participant": [first]})
        assert r.status_code == 200
        return {"prep": c.get(f"/session/{sid}/interface-preparation").get_data(as_text=True),
                "pci": c.get(f"/session/{sid}/parts-components-interactions").get_data(as_text=True),
                "report": c.get(f"/session/{sid}/deliverable").get_data(as_text=True)}


def test_participation_renders_on_every_surface_without_overflow_in_both_locales():
    pytest.importorskip("playwright.sync_api")
    from playwright.sync_api import sync_playwright
    exe = (glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome") or [None])[0]
    rendered = {lang: _pages(lang) for lang in ("en", "ar")}
    markers = {"prep": "[data-icp-name]", "pci": "[data-pci-participant]", "report": "[data-ifc-participant]"}
    with sync_playwright() as p:
        kw = {"headless": True, "args": ["--no-sandbox"]}
        if exe:
            kw["executable_path"] = exe
        browser = p.chromium.launch(**kw)
        try:
            for lang, pages in rendered.items():
                boundary = ui_text.text("UI_ICP_BOUNDARY", lang)
                for surface, html in pages.items():
                    for width in (390, 1280):
                        page = browser.new_page(viewport={"width": width, "height": 900})
                        page.set_content(html)
                        sw, cw = page.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
                        assert sw <= cw, (lang, surface, width, sw, cw)
                        names = page.locator(markers[surface])
                        assert names.count() == 1, (lang, surface)
                        assert names.first.inner_text() == NAMES[lang][0]
                        assert names.first.get_attribute("dir") == "auto"
                        assert names.first.bounding_box()["width"] <= cw
                        assert boundary in page.locator("body").inner_text()
                        if surface == "prep":
                            boxes = page.locator("[data-icp-form] input[type=checkbox][name=participant]")
                            assert boxes.count() == 2
                            assert boxes.nth(0).is_checked() and not boxes.nth(1).is_checked()
                            assert page.locator("[data-icp-form] button[type=submit]").is_visible()
                        else:
                            assert page.locator("[data-icp-form]").count() == 0
                        assert (page.locator("html").get_attribute("dir") == "rtl") == (lang == "ar")
                        page.close()
        finally:
            browser.close()
