"""Real Chromium: STAGE35-COMPONENT-DISCLOSURE-EXPORT-01 — the v2 HTML disclosure document with declared components
(EN and AR, 390 and 1280 px).

Synthetic data only. The document is rendered by the real HTML owner from a real v2 projection that carries one
component linked to both parts (with a long unbroken name) and one project-level component; at every width the page
has no horizontal overflow, field 7 shows both components with their part links / project-level note, inventor text
is direction-isolated (``dir="auto"``) and Arabic renders RTL.
"""
import glob

import pytest

from engine import disclosure_export as dx
from engine import subsystem_model as sm
from tests.test_stage35_disclosure_html import _render
from tests.test_stage35_disclosure_projection import _rich_sources
from web import ui_text

LONG = "M" * 80


def _doc():
    sources = _rich_sources()
    subs = tuple(sources.state.subsystems)
    components = (
        sm.declared_component(subs, LONG, "Turns the arm — يدير الذراع",
                              tuple(s.subsystem_id for s in subs)),
        sm.declared_component(subs, "حامل التثبيت", "يثبّت كل شيء", ()),
    )
    content = dx.compose_projection(dx.MaterializedSources(
        state=sources.state, requirement_quantities=sources.requirement_quantities,
        planning_metadata=sources.planning_metadata,
        interface_dependencies=sources.interface_dependencies, result_events=sources.result_events,
        component_composition=subs, components=components))
    return dx.export_document(content, "2026-10-11T00:00:00Z", dx.HTML_FORMAT_VERSION)


def test_components_render_without_overflow_in_both_locales():
    pytest.importorskip("playwright.sync_api")
    from playwright.sync_api import sync_playwright
    doc = _doc()
    exe = (glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome") or [None])[0]
    with sync_playwright() as p:
        kw = {"headless": True, "args": ["--no-sandbox"]}
        if exe:
            kw["executable_path"] = exe
        browser = p.chromium.launch(**kw)
        try:
            for lang in ("en", "ar"):
                for width in (390, 1280):
                    page = browser.new_page(viewport={"width": width, "height": 900})
                    page.set_content(_render(doc, lang))
                    sw, cw = page.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
                    assert sw <= cw, (lang, width, sw, cw)
                    section = page.locator("#field-component_descriptions_beyond_parts")
                    items = section.locator('article[data-kind="component"]')
                    assert items.count() == 2
                    assert section.locator("[data-component-parts] a").count() == len(
                        _rich_sources().state.subsystems)
                    assert section.locator("[data-component-project-level]").inner_text().strip() == \
                        ui_text.text("UI_S35_COMPONENT_PROJECT_LEVEL", lang)
                    first = items.nth(0).locator('[data-slot="name"] .value')
                    assert first.inner_text() == LONG and first.get_attribute("dir") == "auto"
                    assert section.bounding_box()["width"] <= cw
                    assert page.locator("html").get_attribute("lang") == lang
                    assert (page.locator("html").get_attribute("dir") == "rtl") == (lang == "ar")
                    page.close()
        finally:
            browser.close()
