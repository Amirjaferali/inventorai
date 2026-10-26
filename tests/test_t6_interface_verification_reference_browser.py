"""Real Chromium: T6-INTERFACE-VERIFICATION-REFERENCE-01 (EN and AR, 390 and 1280 px).

Synthetic data only. Pages are rendered by the real application (Flask test client) and loaded into Chromium. One
component takes part in one declared interaction; the inventor saved notes for that exact pair and, separately, one of
the interaction's own preparation inputs. The page shows the two levels in separate blocks (the pair's notes, then the
interaction itself), every interaction input as recorded or "not recorded", the Validation Plan reference as
unresolved, and no claim of a check, compatibility or validation. A withdrawn component shows neither level; a
corrupt interaction-preparation record shows only the unavailable notice. No horizontal overflow; RTL in Arabic.
"""
import glob
import html as _html

import pytest

import web.app as appmod
from engine import subsystem_model as sm
from tests.csrf_client import csrf_client
from tests.test_component_interface_participation import _form as _icp_form, _post as _icp_post, _raw, _web_project
from tests.test_component_inventory_correct_withdraw import _withdraw
from tests.test_component_participation_verification_preparation import (
    _forms as _ppv_forms, _page as _prep_page, _post as _ppv_post)
from tests.test_stage15_interface_preparation import _save as _ifc_save
from web import ui_text

F_C, F_A, F_E = sm.PREPARATION_FIELDS
PAIR = {"en": "Hinge opens in 2 s", "ar": "تُفتح المفصلة خلال ثانيتين"}
CRIT = {"en": "The hinge reaches 90 degrees", "ar": "تصل المفصلة إلى 90 درجة"}


def _pages(lang):
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        if lang == "ar":
            c.post("/ui-language", data={"lang": "ar"})
        sid = _web_project(c)
        form = _icp_form(c, sid)
        ids = [i for i, _c in form["options"]]
        ifc = form["interface"]
        _icp_post(c, sid, form, ids[:1])
        _ppv_post(c, sid, _ppv_forms(_prep_page(c, sid))[0], PAIR[lang], "Stopwatch")
        _ifc_save(c, sid, {(F_A, ifc): CRIT[lang]})
        pages = {"current": c.get(f"/session/{sid}/preliminary-composition").get_data(as_text=True)}
        _withdraw(appmod._get_store(), sid, ids[0], 0)
        pages["withdrawn"] = c.get(f"/session/{sid}/preliminary-composition").get_data(as_text=True)
        _raw("INSERT INTO subsystem_interface_preparations VALUES (?, ?, ?, ?, ?)",
             (sid, "ifc-" + "8" * 32, "orphan", None, None), fk=False)
        pages["unavailable"] = c.get(f"/session/{sid}/preliminary-composition").get_data(as_text=True)
        return sid, ids, ifc, pages


def test_the_inventor_can_tell_the_pair_level_from_the_interaction_level_in_both_locales():
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
            for lang, (_sid, ids, ifc, pages) in rendered.items():
                t = lambda key: ui_text.text(key, lang)  # noqa: E731
                for width in (390, 1280):
                    page = browser.new_page(viewport={"width": width, "height": 900})
                    page.set_content(pages["current"])
                    comp = page.locator(f"[data-t6-component-id='{ids[0]}']")
                    link = comp.locator("[data-t6-link]")
                    assert link.count() == 1 and link.get_attribute("data-t6-interface-id") == ifc
                    # 1. the component and its recorded interaction
                    assert link.locator("[data-t6-interaction]").inner_text() == "Motor turns the hinge"
                    # 2. the notes of that exact pair, in their own block
                    pair = link.locator("[data-t6-pair-prep]")
                    assert pair.locator("h4").inner_text() == t("UI_T6_PAIR_TITLE")
                    assert pair.locator("[data-t6-note=expected_contribution]").inner_text() == PAIR[lang]
                    assert CRIT[lang] not in pair.inner_text()
                    # 3. the interaction's own inputs, in a separate block
                    inter = link.locator("[data-t6-interface-prep]")
                    assert inter.get_attribute("data-t6-interface-prep-id") == ifc
                    assert inter.locator("h4").inner_text() == t("UI_T6_IFC_TITLE")
                    assert PAIR[lang] not in inter.inner_text()
                    assert inter.locator(f"[data-t6-interface-field={F_A}]").inner_text() == CRIT[lang]
                    # 4. missing and unresolved
                    for name in (F_C, F_E):
                        cell = inter.locator(f"[data-t6-interface-field={name}]")
                        assert cell.get_attribute("data-t6-interface-field-status") == "NOT_RECORDED"
                        assert cell.inner_text() == t("UI_T6_IFC_NOT_RECORDED")
                    ref = inter.locator("[data-t6-vp-ref]")
                    assert ref.get_attribute("data-t6-vp-ref") == "UNRESOLVED"
                    assert ref.inner_text() == t("UI_T6_VP_UNRESOLVED")
                    assert t("UI_T6_IFC_NOTE") in inter.inner_text()
                    text = inter.inner_text().lower()
                    for claim in ("is compatible", "verified", "check passed", "is safe", "validated design"):
                        assert claim not in text
                    assert ifc not in page.locator("body").inner_text()
                    sw, cw = page.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
                    assert sw <= cw, (lang, width, sw, cw)
                    assert (page.locator("html").get_attribute("dir") == "rtl") == (lang == "ar")

                    # withdrawn: neither level appears for that component
                    page.set_content(pages["withdrawn"])
                    assert page.locator(f"[data-t6-component-id='{ids[0]}']").count() == 0
                    assert page.locator(f"[data-t6-interface-prep-id='{ifc}']").count() == 0

                    # unreadable: nothing partial, only the notice
                    page.set_content(pages["unavailable"])
                    assert page.locator("[data-t6-composition], [data-t6-interface-prep]").count() == 0
                    assert page.locator("[data-t6-notice]").inner_text() == t("UI_T6_UNAVAILABLE")
                    page.close()
        finally:
            browser.close()


def test_the_rendered_pages_used_by_the_browser_test_are_well_formed():
    """Runs everywhere (no browser): the same synthetic journey yields the expected markers."""
    _sid, ids, ifc, pages = _pages("en")
    current = _html.unescape(pages["current"])
    assert f'data-t6-interface-prep-id="{ifc}"' in current and CRIT["en"] in current
    assert 'data-t6-vp-ref="UNRESOLVED"' in current
    assert ids[0] not in pages["withdrawn"] and "data-t6-interface-prep" not in pages["withdrawn"]
    assert "data-t6-composition" not in pages["unavailable"]
