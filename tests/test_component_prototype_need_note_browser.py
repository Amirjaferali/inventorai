"""Real Chromium: COMPONENT-PROTOTYPE-NEED-NOTE-01 — the session page's component inventory with one component
carrying the inventor's prototype-need note and one with no note (EN and AR, 390 and 1280 px).

Synthetic data only. The page is rendered by the real application (Flask test client) and loaded into Chromium with
every disclosure open; at every width there is no horizontal overflow, the note sits beside its own component only,
the other component reads "not stated" (never a default), inventor text is direction-isolated (``dir="auto"``),
Arabic renders RTL and the note field accepts at most 120 typed characters.
"""
import glob
import html as _html
import re

import pytest

import web.app as appmod
from tests.csrf_client import csrf_client
from tests.test_stage15_integrated_invention_entry import MECH, TIE_IDEA, _compose, _created
from web import ui_text

LONG_NEED = "W" * 120                                   # one unbroken 120-character word
MIXED_NEED = "أربع وحدات wheel units متشابهة — 4 × 25 mm"


def _page(lang):
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        if lang == "ar":
            c.post("/ui-language", data={"lang": "ar"})
        sid = _created(_compose(c, TIE_IDEA, focus=MECH))
        for name, function in (("Wheel", "Rolls the cart"), ("حامل التثبيت", "يثبّت كل شيء")):
            raw = c.get(f"/session/{sid}").get_data(as_text=True)
            sub = _html.unescape(re.search(r'name="component_submission" value="([^"]*)"', raw).group(1))
            c.post(f"/session/{sid}/declare-component", data={
                "component_submission": sub, "component_name": name, "component_function": function})
        raw = c.get(f"/session/{sid}").get_data(as_text=True)
        first = re.search(r'data-ci-need-form.*?name="component_id" value="([^"]*)"', raw, re.S).group(1)
        c.post(f"/session/{sid}/component-prototype-need", data={
            "component_id": first, "need_base": "", "need_action": "save",
            "need_text": LONG_NEED if lang == "en" else MIXED_NEED})
        return c.get(f"/session/{sid}").get_data(as_text=True)


def test_prototype_need_note_renders_beside_its_component_without_overflow_in_both_locales():
    pytest.importorskip("playwright.sync_api")
    from playwright.sync_api import sync_playwright
    exe = (glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome") or [None])[0]
    rendered = {lang: _page(lang) for lang in ("en", "ar")}
    with sync_playwright() as p:
        kw = {"headless": True, "args": ["--no-sandbox"]}
        if exe:
            kw["executable_path"] = exe
        browser = p.chromium.launch(**kw)
        try:
            for lang, session in rendered.items():
                expected = LONG_NEED if lang == "en" else MIXED_NEED
                for width in (390, 1280):
                    page = browser.new_page(viewport={"width": width, "height": 900})
                    page.set_content(session)
                    page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
                    sw, cw = page.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
                    assert sw <= cw, (lang, width, sw, cw)
                    block = page.locator("#component-inventory")
                    assert block.bounding_box()["width"] <= cw
                    items = block.locator("[data-ci-list] > li[data-ci-item]")
                    assert items.count() == 2
                    noted, plain = items.nth(0), items.nth(1)
                    text = noted.locator("[data-ci-need-text]")
                    assert text.inner_text() == expected and text.get_attribute("dir") == "auto"
                    assert text.bounding_box()["width"] <= cw
                    assert noted.locator("[data-ci-need-status]").is_visible()
                    assert noted.locator("[data-ci-need-form] button[value='clear']").is_visible()
                    assert plain.locator("[data-ci-need-text]").count() == 0
                    assert plain.locator("[data-ci-need-none]").inner_text() == ui_text.text(
                        "UI_CI_NEED_NOT_STATED", lang)
                    assert plain.locator("[data-ci-need-form] button[value='clear']").count() == 0
                    field = plain.locator("[data-ci-need-form] input[name='need_text']")
                    assert field.is_visible() and field.get_attribute("dir") == "auto"
                    field.type("x" * 125)
                    assert len(field.input_value()) == 120
                    hint = ui_text.text("UI_CI_NEED_HINT", lang)
                    assert hint in block.inner_text()
                    assert (page.locator("html").get_attribute("dir") == "rtl") == (lang == "ar")
                    page.close()
        finally:
            browser.close()
