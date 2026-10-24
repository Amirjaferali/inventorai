"""Real Chromium: PATHN-CONSTRAINT-DECLARATION-01 — the session page's project constraints (a corrected current
constraint with its earlier version, the correction / withdrawal forms and a withdrawn constraint), the report section
with its safety-scope note, and the v3 disclosure HTML (EN and AR, 390 and 1280 px).

Synthetic data only. The pages are rendered by the real application (Flask test client) and the real disclosure HTML
owner, then loaded into Chromium with every disclosure open; at every width there is no horizontal overflow, the
withdrawn constraint appears only in its own history list, inventor text is direction-isolated (``dir="auto"``) and
Arabic renders RTL.
"""
import glob
import html as _html
import re

import pytest

import web.app as appmod
from engine import disclosure_export as dx
from tests.csrf_client import csrf_client
from tests.test_stage35_disclosure_html import _render
from tests.test_stage35_disclosure_projection import _rich_sources
from web import ui_text

LONG = "W" * 120


def _submission(c, sid):
    raw = c.get(f"/session/{sid}").get_data(as_text=True)
    return _html.unescape(re.search(r'name="constraint_submission" value="([^"]*)"', raw).group(1))


def _post(c, sid, **form):
    form.update(constraint_submission=_submission(c, sid), constraint_confirm="yes")
    c.post(f"/session/{sid}/constraint", data=form)


def _heads(sid):
    return [r.record_id for r in appmod.SESSION_STORE[sid]["state"].assertions
            if r.disposition == "constraint_declared" and r.superseded_by is None]


def _pages(lang):
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        if lang == "ar":
            c.post("/ui-language", data={"lang": "ar"})
        r = c.post("/start", data={"idea": "a folding ramp with a spring latch for a wheelchair",
                                   "domain_confirm": "mechanical"})
        sid = r.headers["Location"].rsplit("/", 1)[-1]
        _post(c, sid, constraint_action="declare", constraint_text="Under 40 dollars",
              constraint_strength="preference")
        _post(c, sid, constraint_action="declare", constraint_text="يجب أن يعمل بالبطاريات",
              constraint_strength="mandatory_constraint")
        first, second = _heads(sid)
        _post(c, sid, constraint_action="correct", constraint_target=second,
              constraint_text=LONG + " — يعمل بالبطاريات", constraint_strength="soft_constraint")
        _post(c, sid, constraint_action="withdraw", constraint_target=first)
        session = c.get(f"/session/{sid}").get_data(as_text=True)
        report = c.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    return session, report


def _export(lang):
    sources = _rich_sources()
    sources.state.record_constraint_action("declare", LONG, "mandatory_constraint")
    sources.state.record_constraint_action("declare", "الوزن أقل من 2 كغ", "preference")
    content = dx.compose_projection(sources)
    return _render(dx.export_document(content, "2026-10-24T00:00:00Z", dx.HTML_FORMAT_VERSION), lang)


def test_constraints_render_without_overflow_in_both_locales():
    pytest.importorskip("playwright.sync_api")
    from playwright.sync_api import sync_playwright
    exe = (glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome") or [None])[0]
    rendered = {lang: _pages(lang) + (_export(lang),) for lang in ("en", "ar")}
    with sync_playwright() as p:
        kw = {"headless": True, "args": ["--no-sandbox"]}
        if exe:
            kw["executable_path"] = exe
        browser = p.chromium.launch(**kw)
        try:
            for lang, (session, report, export) in rendered.items():
                for width in (390, 1280):
                    page = browser.new_page(viewport={"width": width, "height": 900})
                    page.set_content(session)
                    page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
                    sw, cw = page.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
                    assert sw <= cw, (lang, width, "session", sw, cw)
                    block = page.locator("#project-constraints")
                    current = block.locator("[data-pcn-list] > li[data-pcn-item]")
                    assert current.count() == 1
                    text = current.nth(0).locator("[data-pcn-text]")
                    assert text.inner_text().startswith(LONG) and text.get_attribute("dir") == "auto"
                    assert current.nth(0).locator("[data-pcn-corrected]").is_visible()
                    assert current.nth(0).locator("[data-pcn-version]").count() == 1
                    assert current.nth(0).locator("[data-pcn-correct-form]").is_visible()
                    assert current.nth(0).locator("[data-pcn-withdraw-form]").is_visible()
                    assert ui_text.text("UI_PCN_STRENGTH_SOFT", lang) in current.nth(0).inner_text()
                    withdrawn = block.locator("[data-pcn-withdrawn] [data-pcn-withdrawn-item]")
                    assert withdrawn.count() == 1 and "Under 40 dollars" in withdrawn.inner_text()
                    assert block.locator("[data-pcn-form]").is_visible()
                    assert ui_text.text("UI_PCN_SAFETY", lang) in block.inner_text()
                    assert block.bounding_box()["width"] <= cw
                    assert (page.locator("html").get_attribute("dir") == "rtl") == (lang == "ar")
                    page.close()

                    page = browser.new_page(viewport={"width": width, "height": 900})
                    page.set_content(report)
                    sw, cw = page.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
                    assert sw <= cw, (lang, width, "report", sw, cw)
                    section = page.locator("#project-constraints-report")
                    assert section.locator("[data-pcn-report-item]").count() == 1
                    assert "Under 40 dollars" not in section.inner_text()
                    assert page.locator("[data-ss-constraint-scope]").inner_text().strip() == \
                        ui_text.text("UI_SS_CONSTRAINT_SCOPE", lang)
                    assert (page.locator("html").get_attribute("dir") == "rtl") == (lang == "ar")
                    page.close()

                    page = browser.new_page(viewport={"width": width, "height": 900})
                    page.set_content(export)
                    sw, cw = page.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
                    assert sw <= cw, (lang, width, "export", sw, cw)
                    field = page.locator("#field-project_constraints")
                    items = field.locator('article[data-kind="constraint"]')
                    assert items.count() == 2
                    value = items.nth(0).locator('[data-slot="text"] .value')
                    assert value.inner_text() == LONG and value.get_attribute("dir") == "auto"
                    assert field.locator("[data-constraints-clarification]").is_visible()
                    assert (page.locator("html").get_attribute("dir") == "rtl") == (lang == "ar")
                    page.close()
        finally:
            browser.close()
