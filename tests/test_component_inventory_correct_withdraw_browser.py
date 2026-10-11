"""Real Chromium: COMPONENT-INVENTORY-CORRECT-WITHDRAW-01 — the session page's component inventory with a corrected
component, its earlier versions, the correction / withdrawal forms and a withdrawn component, and the Parts,
Components & Interactions view (EN and AR, 390 and 1280 px).

Synthetic data only. The pages are rendered by the real application (Flask test client) and loaded into Chromium with
every disclosure open; at every width there is no horizontal overflow, the withdrawn component appears only in its
own history list (never in the current list), inventor text is direction-isolated (``dir="auto"``) and Arabic renders
RTL.
"""
import glob
import html as _html
import re

import pytest

import web.app as appmod
from tests.csrf_client import csrf_client
from tests.test_stage15_integrated_invention_entry import MECH, TIE_IDEA, _compose, _created
from web import ui_text

LONG = "G" * 80


def _forms(raw, action):
    return [{"submission": _html.unescape(s), "id": i, "revision": r}
            for s, i, r in re.findall(
                r'action="/session/[^/]+/' + action + r'-component".*?'
                r'name="component_revision_submission" value="([^"]*)".*?'
                r'name="component_id" value="([^"]*)".*?'
                r'name="component_revision" value="([^"]*)"', raw, re.S)]


def _pages(lang):
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        if lang == "ar":
            c.post("/ui-language", data={"lang": "ar"})
        sid = _created(_compose(c, TIE_IDEA, focus=MECH))
        for name, function in (("Motor", "Turns"), ("حامل التثبيت", "يثبّت كل شيء")):
            raw = c.get(f"/session/{sid}").get_data(as_text=True)
            sub = _html.unescape(re.search(r'name="component_submission" value="([^"]*)"', raw).group(1))
            parts = re.findall(r'name="component_part" value="([^"]*)"', raw)
            c.post(f"/session/{sid}/declare-component", data={
                "component_submission": sub, "component_name": name,
                "component_function": function, "component_part": parts})
        raw = c.get(f"/session/{sid}").get_data(as_text=True)
        corr = _forms(raw, "correct")[0]
        c.post(f"/session/{sid}/correct-component", data={
            "component_revision_submission": corr["submission"], "component_id": corr["id"],
            "component_revision": corr["revision"], "correction_name": LONG,
            "correction_function": "Turns the arm — يدير الذراع"})
        raw = c.get(f"/session/{sid}").get_data(as_text=True)
        wd = _forms(raw, "withdraw")[1]
        c.post(f"/session/{sid}/withdraw-component", data={
            "component_revision_submission": wd["submission"], "component_id": wd["id"],
            "component_revision": wd["revision"], "withdraw_confirm": "yes"})
        session = c.get(f"/session/{sid}").get_data(as_text=True)
        view = c.get(f"/session/{sid}/parts-components-interactions").get_data(as_text=True)
    return session, view


def test_correction_history_and_withdrawn_list_render_without_overflow_in_both_locales():
    pytest.importorskip("playwright.sync_api")
    from playwright.sync_api import sync_playwright
    exe = (glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome") or [None])[0]
    rendered = {lang: _pages(lang) for lang in ("en", "ar")}
    with sync_playwright() as p:
        kw = {"headless": True, "args": ["--no-sandbox"]}
        if exe:
            kw["executable_path"] = exe
        browser = p.chromium.launch(**kw)
        try:
            for lang, (session, view) in rendered.items():
                for width in (390, 1280):
                    page = browser.new_page(viewport={"width": width, "height": 900})
                    page.set_content(session)
                    page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
                    sw, cw = page.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
                    assert sw <= cw, (lang, width, "session", sw, cw)
                    block = page.locator("#component-inventory")
                    current = block.locator("[data-ci-list] > li[data-ci-item]")
                    assert current.count() == 1
                    name = current.nth(0).locator("[data-ci-name]")
                    assert name.inner_text() == LONG and name.get_attribute("dir") == "auto"
                    assert current.nth(0).locator("[data-ci-corrected]").is_visible()
                    assert current.nth(0).locator("[data-ci-version]").count() == 1
                    assert current.nth(0).locator("[data-ci-correct-form]").is_visible()
                    assert current.nth(0).locator("[data-ci-withdraw-form]").is_visible()
                    withdrawn = block.locator("[data-ci-withdrawn] [data-ci-withdrawn-item]")
                    assert withdrawn.count() == 1
                    assert withdrawn.nth(0).locator("[data-ci-withdrawn-name]").inner_text() == "حامل التثبيت"
                    assert ui_text.text("UI_CI_WITHDRAWN_NOTE", lang) in block.inner_text()
                    assert block.bounding_box()["width"] <= cw
                    assert (page.locator("html").get_attribute("dir") == "rtl") == (lang == "ar")
                    page.close()
                    page = browser.new_page(viewport={"width": width, "height": 900})
                    page.set_content(view)
                    sw, cw = page.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
                    assert sw <= cw, (lang, width, "view", sw, cw)
                    section = page.locator("[data-pci-components]")
                    assert section.locator("[data-pci-component]").count() == 1
                    assert section.locator("[data-pci-withdrawn-item]").count() == 1
                    assert section.locator("[data-pci-component-name]").inner_text() == LONG
                    assert (page.locator("html").get_attribute("dir") == "rtl") == (lang == "ar")
                    page.close()
        finally:
            browser.close()
