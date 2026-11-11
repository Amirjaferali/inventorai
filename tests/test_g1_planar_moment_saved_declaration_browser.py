# -*- coding: utf-8 -*-
"""G1-PLANAR-MOMENT-SAVED-DECLARATION-01 - the saved configurations in a real browser, EN / AR.

The moment page with (a) the save form under an admitted result and (b) a saved configuration in each state the
inventor can reach (CURRENT and, after a component correction, NEEDS RECONFIRMATION) renders without horizontal
overflow at 390 and 1280 px in both locales, Arabic right-to-left, with the inventor's own Arabic text shown
direction-isolated and NO number on a configuration that needs reconfirmation. Synthetic data only.
"""
import glob
import html as _html

import pytest

import web.app as webapp
from tests.test_cap12_form_mockup_advisory import _client_for, _start, SEED
from tests.test_component_inventory_correct_withdraw import _correct as _correct_component
from tests.test_component_inventory_declare_list import _declare
from tests.test_g1_planar_moment_saved_declaration import _evaluate, _save, URL
from web import ui_text

POINT_AR = "محور المفصل عند الحافة السفلية للغطاء"
FORCE_AR = "يد تضغط على الزاوية البعيدة للغطاء"


def _pages(lang):
    c, _aid = _client_for("pm-browser-%s@example.com" % lang)
    if lang == "ar":
        c.post("/ui-language", data={"lang": "ar"})
    sid = _start(c, {"idea": SEED, "domain_confirm": "mechanical"})
    _declare(c, sid, name="غطاء قابل للطي", function="يغطي الفتحة")
    _declare(c, sid, name="Second flap with a rather long component name to wrap",
             function="Covers the other opening")
    result = _evaluate(c, sid)
    assert _save(c, sid, result, point=POINT_AR, force=FORCE_AR).status_code == 200
    current = c.get(URL % sid).get_data(as_text=True)
    store = webapp._get_store()
    comp = store.load_component_inventory_record(sid)[1].records[0]
    _correct_component(store, sid, comp.component_id, 0, "غطاء قابل للطي، أطول")
    stale = c.get(URL % sid).get_data(as_text=True)
    return {"result": result, "current": current, "stale": stale}


def test_saved_configurations_render_in_both_locales_without_overflow():
    pytest.importorskip("playwright.sync_api")
    from playwright.sync_api import sync_playwright
    exe = (glob.glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome") or [None])[0]
    rendered = {lang: _pages(lang) for lang in ("en", "ar")}
    with sync_playwright() as p:
        kw = {"headless": True, "args": ["--no-sandbox"]}
        if exe:
            kw["executable_path"] = exe
        browser = p.chromium.launch(**kw)
        try:
            for lang, pages in rendered.items():
                for width in (390, 1280):
                    for name, html in pages.items():
                        page = browser.new_page(viewport={"width": width, "height": 900})
                        page.set_content(html)
                        sw, cw = page.evaluate(
                            "[document.documentElement.scrollWidth, window.innerWidth]")
                        assert sw <= cw, (lang, width, name, sw, cw)
                        assert (page.locator("html").get_attribute("dir") == "rtl") == (lang == "ar")
                        saved = page.locator("[data-pm-saved]")
                        assert saved.is_visible() and saved.bounding_box()["width"] <= cw
                        assert ui_text.text("UI_PM_LIMIT_NOTE", lang) in saved.inner_text()
                        if name == "result":
                            form = page.locator("[data-pm-save-form]")
                            assert form.is_visible() and form.bounding_box()["width"] <= cw
                            assert page.locator("[data-pm-target] option").count() == 3  # placeholder + 2
                        else:
                            item = page.locator("[data-pm-item]")
                            assert item.count() == 1
                            point = item.locator("[data-pm-point-text]")
                            assert point.inner_text() == POINT_AR
                            assert point.get_attribute("dir") == "auto"
                            state = item.locator("span.pm-state").get_attribute("data-pm-state")
                            if name == "current":
                                assert state == "CURRENT"
                                assert item.locator("[data-pm-result-value]").is_visible()
                            else:
                                assert state == "NEEDS_RECONFIRMATION"
                                assert item.locator("[data-pm-result-value]").count() == 0
                                assert item.locator("[data-pm-issues]").is_visible()
                            assert item.locator("[data-pm-withdraw-form]").is_visible()
                        page.close()
        finally:
            browser.close()
    assert _html.unescape(rendered["ar"]["stale"]).count(POINT_AR) >= 1
