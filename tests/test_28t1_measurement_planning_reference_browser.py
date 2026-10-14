"""Real Chromium: 28-T1-MEASUREMENT-PLANNING-REFERENCE-01 — on an Electronics
project's measurement-planning page the reference panel is collapsed by default,
opens from its summary to show the two existing groups (sensing; accuracy and
resolution) in order, in EN and AR (RTL), and neither state overflows at 390 or
1280 px. Synthetic data only.
"""
import pytest

pytest.importorskip("playwright.sync_api")

import web.app as webapp  # noqa: E402
from tests.csrf_client import csrf_client  # noqa: E402
from tests.test_draft_l2_local_continuity import _browser, page, server  # noqa: E402,F401
from tests.test_stage19_durable_success_criteria import PW, _journey, _mk_account  # noqa: E402
from web import ui_text  # noqa: E402

EMAIL = "s28t1-mref-browser@example.com"
GROUPS = ["sensing-value-threshold-reference-v1", "measurement-accuracy-resolution-reference-v1"]


def _owned_project():
    """Create the owner and ONE Electronics project in this thread, then release
    the cached stores so the single-thread live server opens its own."""
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


def _fits(pg, lang):
    width = pg.evaluate("document.documentElement.clientWidth")
    assert pg.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert pg.locator("[data-measurement-reference]").bounding_box()["width"] <= width
    assert pg.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert pg.locator("html").get_attribute("dir") == "rtl"


def test_measurement_reference_panel_collapses_opens_and_fits(server, page):  # noqa: F811
    sid = _owned_project()
    page.goto(server + "/login")
    page.fill("#email", EMAIL)
    page.fill("#password", PW)
    page.click("main button[type=submit]")
    page.wait_for_load_state()
    for lang in ("en", "ar"):
        if lang == "ar":
            page.goto(server + "/")
            page.get_by_role("button", name="العربية", exact=True).click()
            page.wait_for_load_state()
        for width in (390, 1280):
            page.set_viewport_size({"width": width, "height": 900})
            page.goto(server + "/session/%s/success-criteria" % sid)
            panel = page.locator("[data-measurement-reference]")
            assert panel.count() == 1
            assert panel.evaluate("el => el.open") is False            # collapsed by default
            assert not page.locator("[data-measurement-reference] section").first.is_visible()
            _fits(page, lang)
            summary = panel.locator("summary")
            assert summary.inner_text().strip() == ui_text.text("UI_SC_MREF_SUMMARY", lang)
            summary.click()
            assert panel.evaluate("el => el.open") is True
            sections = panel.locator("section")
            assert [sections.nth(i).get_attribute("data-cap01-fundamentals")
                    for i in range(sections.count())] == GROUPS
            assert sections.first.is_visible()
            _fits(page, lang)
