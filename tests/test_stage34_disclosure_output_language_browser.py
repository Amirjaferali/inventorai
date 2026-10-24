"""Real Chromium: STAGE34-OUTPUT-LANGUAGE-01 — the disclosure pre-download page
offers an English and an Arabic HTML control in either UI language, each control
downloads the HTML document in its own language (lang / dir), the file name and
substantive values are the same for both, and neither the page nor either
document overflows at 390 or 1280 px. Synthetic data only.
"""
import re

import pytest

pytest.importorskip("playwright.sync_api")

import web.app as webapp  # noqa: E402
from tests.csrf_client import csrf_client  # noqa: E402
from tests.test_draft_l2_local_continuity import _browser, page, server  # noqa: E402,F401
from tests.test_stage19_durable_success_criteria import PW, _journey, _mk_account  # noqa: E402
from web import ui_text  # noqa: E402

EMAIL = "s34-browser-owner@example.com"


def _owned_project():
    """Create the owner and ONE project in this thread, then release the cached
    stores so the single-thread live server opens its own (supported topology)."""
    _mk_account(EMAIL)
    c = csrf_client(webapp.app)
    assert c.post("/login", data={"email": EMAIL, "password": PW}).status_code == 302
    sid = _journey(c)
    webapp.SESSION_STORE.clear()
    for name in ("_STORE", "_ACCOUNT_STORE"):
        store = getattr(webapp, name)
        if store is not None:
            store.close()
        setattr(webapp, name, None)
    return sid


def _no_overflow(pg):
    sw, cw = pg.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
    assert sw <= cw, (sw, cw)


def test_output_language_controls_download_each_language(server, page):  # noqa: F811
    sid = _owned_project()
    page.goto(server + "/login")
    page.fill("#email", EMAIL)
    page.fill("#password", PW)
    page.click("main button[type=submit]")
    page.wait_for_load_state()
    url = server + "/account/projects/%s/disclosure-export" % sid
    documents = {}
    for ui in ("en", "ar"):
        if ui == "ar":
            page.goto(server + "/")
            page.get_by_role("button", name="العربية", exact=True).click()
            page.wait_for_load_state()
        for width in (390, 1280):
            page.set_viewport_size({"width": width, "height": 900})
            page.goto(url)
            assert page.locator("html").get_attribute("lang") == ui
            _no_overflow(page)
            controls = page.locator(".disclosure-controls a[data-output-lang]")
            assert controls.count() == 2
            for lang in ("en", "ar"):
                control = page.locator('.disclosure-controls a[data-output-lang="%s"]' % lang)
                assert control.inner_text().strip() == \
                    ui_text.text("UI_S35_HTML_CONTROL_" + lang.upper(), ui)
                box = control.bounding_box()
                assert box["x"] >= 0 and box["x"] + box["width"] <= width
                with page.expect_download() as info:
                    control.click()
                download = info.value
                assert download.suggested_filename == "inventorai-disclosure-export-v3.html"   # v3 (PATHN-CONSTRAINT-DECLARATION-01)
                body = open(download.path(), encoding="utf-8").read()
                direction = "rtl" if lang == "ar" else "ltr"
                assert '<html lang="%s" dir="%s">' % (lang, direction) in body
                documents.setdefault(lang, body)
            assert page.locator("html").get_attribute("lang") == ui   # UI language unchanged
    values = {lang: re.findall(r'<div class="value"[^>]*>.*?</div>', body, re.S)
              for lang, body in documents.items()}
    assert values["en"] and values["en"] == values["ar"]
    viewer = page.context.new_page()
    try:
        for lang, body in documents.items():
            for width in (390, 1280):
                viewer.set_viewport_size({"width": width, "height": 900})
                viewer.set_content(body)
                assert viewer.evaluate("getComputedStyle(document.body).direction") == \
                    ("rtl" if lang == "ar" else "ltr")
                _no_overflow(viewer)
    finally:
        viewer.close()
