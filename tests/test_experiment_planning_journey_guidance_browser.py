"""Real Chromium: EXPERIMENT-PLANNING-JOURNEY-GUIDANCE-01 — the Project Compass planning step on a finished
single-domain journey with unplanned proposed experiments (EN and AR, 390 and 1280 px).

Synthetic data only. The session page is rendered by the real application (Flask test client) and loaded into
Chromium: the ONE primary action is the planning step and is visible, the handoff link stays visible beside it,
there is no horizontal overflow and Arabic renders RTL.
"""
import glob

import pytest

import web.app as appmod
from tests.csrf_client import csrf_client
from tests.test_experiment_planning_journey_guidance import _finished
from web import ui_text


def _page(lang):
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        sid = _finished(c, lang=lang)
        return sid, c.get(f"/session/{sid}").get_data(as_text=True)


def test_planning_step_renders_as_the_one_primary_action_in_both_locales():
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
            for lang, (sid, html) in rendered.items():
                for width in (390, 1280):
                    page = browser.new_page(viewport={"width": width, "height": 900})
                    page.set_content(html)
                    sw, cw = page.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
                    assert sw <= cw, (lang, width, sw, cw)
                    primary = page.locator("[data-pc-row='do'] [data-primary-action]")
                    assert primary.count() == 1
                    assert primary.get_attribute("data-epg-action") is not None
                    assert primary.get_attribute("href") == f"/session/{sid}/success-criteria"
                    assert primary.is_visible() and primary.inner_text() == ui_text.text("UI_EPG_CTA", lang)
                    assert primary.bounding_box()["width"] <= cw
                    handoff = page.locator("[data-epg-handoff] a")
                    assert handoff.is_visible() and handoff.get_attribute("href") == f"/session/{sid}/deliverable"
                    assert page.locator("[data-epg-note]").is_visible()
                    assert (page.locator("html").get_attribute("dir") == "rtl") == (lang == "ar")
                    page.close()
        finally:
            browser.close()
