# -*- coding: utf-8 -*-
"""G1-PLANAR-MOMENT-REPORT-HANDOFF-01 - the report section in a real browser, EN / AR.

The HTML report and the PDF source, each holding one CURRENT and one NEEDS RECONFIRMATION saved configuration,
render without horizontal overflow at 390 and 1280 px in both locales, Arabic right-to-left. The CURRENT item shows
its number with the full disclosure. The other item shows no number. The inventor's Arabic text stays
direction-isolated, and the section holds no form or control. Synthetic data only.
"""
import glob

import pytest

import web.app as webapp
from tests.test_cap12_form_mockup_advisory import _client_for, _start, SEED
from tests.test_component_inventory_correct_withdraw import _correct as _correct_component
from tests.test_component_inventory_declare_list import _declare
from tests.test_g1_planar_moment_saved_declaration import _evaluate, _save, _save_form
from web import ui_text

POINT_AR = "محور المفصل عند الحافة السفلية للغطاء"
FORCE_AR = "يد تضغط على الزاوية البعيدة للغطاء"


def _rendered(lang, monkeypatch):
    c, _aid = _client_for("pm-report-browser-%s@example.com" % lang)
    if lang == "ar":
        c.post("/ui-language", data={"lang": "ar"})
    sid = _start(c, {"idea": SEED, "domain_confirm": "mechanical"})
    _declare(c, sid, name="غطاء قابل للطي", function="يغطي الفتحة")
    _declare(c, sid, name="Second flap with a rather long component name to wrap",
             function="Covers the other opening")
    for _ in range(2):
        result = _evaluate(c, sid)
        target = _save_form(result)[1][0]          # an already-saved component is no longer offered
        assert _save(c, sid, result, target=target, point=POINT_AR, force=FORCE_AR).status_code == 200
    store = webapp._get_store()
    comp = store.load_component_inventory_record(sid)[1].records[1]
    _correct_component(store, sid, comp.component_id, 0, "Second flap, corrected")
    report = c.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    captured = {}
    monkeypatch.setattr(webapp, "_render_pdf_bytes",
                        lambda source: captured.setdefault("html", source) and b"%PDF-1.4\n")
    c.post(f"/session/{sid}/deliverable.pdf", data={})
    return {"report": report, "pdf": captured["html"]}


def test_the_report_section_renders_in_both_locales_without_overflow(monkeypatch):
    pytest.importorskip("playwright.sync_api")
    from playwright.sync_api import sync_playwright
    exe = (glob.glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome") or [None])[0]
    rendered = {lang: _rendered(lang, monkeypatch) for lang in ("en", "ar")}
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
                        section = page.locator("[data-pm-report]")
                        assert section.count() == 1, (lang, width, name)
                        box = section.bounding_box()
                        assert box["x"] >= -1 and box["x"] + box["width"] <= width + 1, (lang, width, name, box)
                        if name == "report":
                            sw, cw = page.evaluate(
                                "[document.documentElement.scrollWidth, window.innerWidth]")
                            assert sw <= cw, (lang, width, sw, cw)
                        assert (page.locator("html").get_attribute("dir") == "rtl") == (lang == "ar")
                        assert section.locator("form, button, input, a").count() == 0
                        items = section.locator("[data-pm-report-item]")
                        assert items.count() == 2
                        states = [items.nth(i).locator("span.pm-state").get_attribute("data-pm-state")
                                  for i in range(2)]
                        assert sorted(states) == ["CURRENT", "NEEDS_RECONFIRMATION"]
                        for i, state in enumerate(states):
                            item = items.nth(i)
                            point = item.locator("[data-pm-point-text]")
                            assert point.inner_text() == POINT_AR and point.get_attribute("dir") == "auto"
                            if state == "CURRENT":
                                assert item.locator("[data-pm-result-value]").is_visible()
                                assert item.locator("[data-pm-disclosure] li").count() == len(
                                    ui_text.text("UI_CAP13M_DISCLOSURE", lang).split("\n\n"))
                            else:
                                assert item.locator("[data-pm-result-value]").count() == 0
                                assert item.locator("[data-pm-issues]").is_visible()
                        assert ui_text.text("UI_PM_REPORT_HISTORICAL", lang) in section.inner_text()
                        page.close()
        finally:
            browser.close()
