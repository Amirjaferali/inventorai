"""Real Chromium: T6-PART-ASSOCIATION-TRACE-01 (EN and AR, 390 and 1280 px).

Synthetic data only. Pages are rendered by the real application (Flask test client) and loaded into Chromium. Each
component shows the inventor-declared names of exactly its own linked parts, in order, with the ids only in data
attributes; an unlinked component keeps "not linked"; a stale part reference shows only the unavailable notice. No
horizontal overflow; RTL in Arabic.
"""
import glob

import pytest

import web.app as appmod
from tests.csrf_client import csrf_client
from tests.test_component_interface_participation import _raw, _store, _web_project
from tests.test_component_inventory_declare_list import _declare as _declare_component
from web import ui_text


def _pages(lang):
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        if lang == "ar":
            c.post("/ui-language", data={"lang": "ar"})
        sid = _web_project(c, names=("Battery pack",))
        subs = _store().load_project_subsystems(sid)
        _declare_component(c, sid, name="Hinge motor", function="Turns the hinge", parts=(subs[0].subsystem_id,))
        _declare_component(c, sid, name="Main board", function="Controls it", parts=[s.subsystem_id for s in subs])
        pages = {"current": c.get(f"/session/{sid}/preliminary-composition").get_data(as_text=True)}
        _raw("UPDATE project_components SET subsystem_ids = ? WHERE project_id = ? AND display_name = ?",
             ('["sub-' + "0" * 32 + '"]', sid, "Hinge motor"), fk=False)
        pages["stale"] = c.get(f"/session/{sid}/preliminary-composition").get_data(as_text=True)
        return subs, pages


def _component(page, name):
    return page.locator("[data-t6-component]").filter(
        has=page.locator("[data-t6-component-name]", has_text=name))


def test_each_component_names_exactly_its_own_parts_in_both_locales():
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
            for lang, (subs, pages) in rendered.items():
                t = lambda key: ui_text.text(key, lang)  # noqa: E731
                for width in (390, 1280):
                    page = browser.new_page(viewport={"width": width, "height": 900})
                    page.set_content(pages["current"])
                    hinge = _component(page, "Hinge motor").locator("[data-t6-part-name]")
                    assert hinge.all_inner_texts() == [subs[0].display_name]
                    assert hinge.first.get_attribute("data-t6-part-id") == subs[0].subsystem_id
                    board = _component(page, "Main board").locator("[data-t6-part-name]")
                    assert board.all_inner_texts() == [s.display_name for s in subs]
                    line = _component(page, "Main board").locator("[data-t6-component-parts]").inner_text()
                    assert line.startswith(t("UI_T6_PARTS_COUNT")) and t("UI_T6_PARTS_SEPARATOR").strip() in line
                    battery = _component(page, "Battery pack")
                    assert battery.locator("[data-t6-part-name]").count() == 0
                    assert battery.locator("[data-t6-component-parts]").inner_text() == t("UI_T6_PARTS_NONE")
                    body = page.locator("body").inner_text()
                    assert all(s.subsystem_id not in body for s in subs)
                    sw, cw = page.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
                    assert sw <= cw, (lang, width, sw, cw)
                    assert (page.locator("html").get_attribute("dir") == "rtl") == (lang == "ar")

                    page.set_content(pages["stale"])
                    assert page.locator("[data-t6-composition], [data-t6-part-name]").count() == 0
                    assert page.locator("[data-t6-notice]").inner_text() == t("UI_T6_UNAVAILABLE")
                    page.close()
        finally:
            browser.close()


def test_the_rendered_pages_used_by_the_browser_test_are_well_formed():
    """Runs everywhere (no browser): the same synthetic journey yields the expected markers."""
    subs, pages = _pages("en")
    assert pages["current"].count("data-t6-part-name") == 3
    assert f'data-t6-part-id="{subs[0].subsystem_id}"' in pages["current"]
    assert "data-t6-composition" not in pages["stale"]
