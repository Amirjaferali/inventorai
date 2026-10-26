"""Real Chromium: T6-PRELIMINARY-COMPOSITION-PROJECTION-01 — Slice 1 (EN and AR, 390 and 1280 px).

Synthetic data only. Pages are rendered by the real application (Flask test client) and loaded into Chromium. The
inventor follows the ONE link on the Parts, Components & Interactions page and traces ONE declared component through
its recorded participation in ONE declared interaction to the notes saved for that exact (interface_id,
component_id) pair. Removing and re-adding the participation shows those notes only as EARLIER / NOT RECONFIRMED; a
withdrawn component disappears with its notes; a corrupt record shows nothing but the unavailable notice. The page
carries its own preliminary / unvalidated / non-binding disclosure, is distinguishable from the report (its own
markers, no report section, no form), has no horizontal overflow and renders RTL in Arabic.
"""
import glob
import html as _html
import re

import pytest

import web.app as appmod
from tests.csrf_client import csrf_client
from tests.test_component_interface_participation import _form as _icp_form, _post as _icp_post, _raw, _web_project
from tests.test_component_inventory_correct_withdraw import _withdraw
from tests.test_component_participation_verification_preparation import (
    _forms as _ppv_forms, _page as _prep_page, _post as _ppv_post)
from web import ui_text

NOTE = {"en": "Hinge opens in 2 s", "ar": "تُفتح المفصلة خلال ثانيتين"}


def _pages(lang):
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        if lang == "ar":
            c.post("/ui-language", data={"lang": "ar"})
        sid = _web_project(c)
        form = _icp_form(c, sid)
        ids = [i for i, _c in form["options"]]
        _icp_post(c, sid, form, ids[:1])
        _ppv_post(c, sid, _ppv_forms(_prep_page(c, sid))[0], NOTE[lang], "Stopwatch")
        pages = {"pci": c.get(f"/session/{sid}/parts-components-interactions").get_data(as_text=True),
                 "current": c.get(f"/session/{sid}/preliminary-composition").get_data(as_text=True),
                 "report": c.get(f"/session/{sid}/deliverable").get_data(as_text=True)}
        _icp_post(c, sid, _icp_form(c, sid), ())
        _icp_post(c, sid, _icp_form(c, sid), ids[:1])
        pages["earlier"] = c.get(f"/session/{sid}/preliminary-composition").get_data(as_text=True)
        _withdraw(appmod._get_store(), sid, ids[0], 0)
        pages["withdrawn"] = c.get(f"/session/{sid}/preliminary-composition").get_data(as_text=True)
        _raw("INSERT INTO subsystem_participation_preparations VALUES (?, ?, ?, ?, ?, ?)",
             (sid, form["interface"], "cmp-" + "9" * 32, "orphan", None, 0), fk=False)
        pages["unavailable"] = c.get(f"/session/{sid}/preliminary-composition").get_data(as_text=True)
        return sid, ids, form["interface"], pages


def test_trace_component_to_its_exact_pair_notes_in_both_locales():
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
            for lang, (sid, ids, ifc, pages) in rendered.items():
                t = lambda key: ui_text.text(key, lang)  # noqa: E731
                for width in (390, 1280):
                    page = browser.new_page(viewport={"width": width, "height": 900})

                    # the ONE entry point, on the Parts, Components & Interactions page
                    page.set_content(pages["pci"])
                    entry = page.locator("[data-t6-link-entry]")
                    assert entry.count() == 1 and entry.inner_text() == t("UI_T6_LINK")
                    assert entry.get_attribute("href") == f"/session/{sid}/preliminary-composition"

                    # the trace: component -> participation -> notes of that exact pair
                    page.set_content(pages["current"])
                    assert page.locator("h1").inner_text() == t("UI_T6_TITLE")
                    assert t("UI_T6_PRELIMINARY") in page.locator("[data-t6-intro]").inner_text()
                    assert page.locator("[data-t6-boundary]").inner_text() == t("UI_T6_BOUNDARY")
                    first = page.locator("[data-t6-component]").first
                    assert first.get_attribute("data-t6-component-id") == ids[0]
                    link = first.locator("[data-t6-link]")
                    assert link.count() == 1
                    assert link.get_attribute("data-t6-pair") == f"{ifc} {ids[0]}"
                    assert link.get_attribute("data-t6-status") == "CURRENT"
                    note = link.locator("[data-t6-note=expected_contribution]")
                    assert note.inner_text() == NOTE[lang] and note.get_attribute("dir") == "auto"
                    others = page.locator("[data-t6-component]")
                    assert others.count() == len(ids)
                    for i in range(1, others.count()):                 # no participation: nothing invented
                        assert others.nth(i).locator("[data-t6-link]").count() == 0
                        assert others.nth(i).locator("[data-t6-no-participation]").count() == 1
                    body = page.locator("body").inner_text()
                    assert ids[0] not in body and ifc not in body       # identities never visible text
                    assert page.locator("[data-t6-composition] form, [data-t6-composition] input").count() == 0
                    assert page.locator("[data-vp-preparation], #vp-heading").count() == 0   # not a report section

                    # the report does not carry the composition
                    page.set_content(pages["report"])
                    assert page.locator("[data-t6-composition], [data-t6-intro]").count() == 0

                    # removed and re-added: earlier notes, never current
                    page.set_content(pages["earlier"])
                    link = page.locator("[data-t6-component]").first.locator("[data-t6-link]")
                    assert link.get_attribute("data-t6-status") == "EARLIER_NOT_RECONFIRMED"
                    assert link.locator("[data-t6-status-label]").inner_text() == t("UI_T6_STATUS_EARLIER")
                    assert page.locator("[data-t6-status=CURRENT]").count() == 0

                    # withdrawn: the component and its notes are gone
                    page.set_content(pages["withdrawn"])
                    assert page.locator(f"[data-t6-component-id='{ids[0]}']").count() == 0
                    assert NOTE[lang] not in page.locator("body").inner_text()

                    # unreadable: the whole composition is unavailable, nothing partial
                    page.set_content(pages["unavailable"])
                    assert page.locator("[data-t6-composition]").count() == 0
                    assert page.locator("[data-t6-notice]").inner_text() == t("UI_T6_UNAVAILABLE")

                    for html in (pages["current"], pages["earlier"]):
                        page.set_content(html)
                        sw, cw = page.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
                        assert sw <= cw, (lang, width, sw, cw)
                        assert (page.locator("html").get_attribute("dir") == "rtl") == (lang == "ar")
                    page.close()
        finally:
            browser.close()


def test_the_rendered_pages_used_by_the_browser_test_are_well_formed():
    """Runs everywhere (no browser): the same synthetic journey yields the expected markers."""
    sid, ids, ifc, pages = _pages("en")
    assert f'data-t6-pair="{ifc} {ids[0]}"' in pages["current"]
    assert 'data-t6-status="EARLIER_NOT_RECONFIRMED"' in pages["earlier"]
    assert ids[0] not in pages["withdrawn"]
    assert "data-t6-composition" not in pages["unavailable"]
    assert _html.unescape(pages["current"]).count(NOTE["en"]) >= 1
    assert re.search(r"data-t6-link-entry", pages["pci"])
