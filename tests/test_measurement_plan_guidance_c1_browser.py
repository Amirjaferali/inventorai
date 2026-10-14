"""Real Chromium: MEASUREMENT-PLAN-GUIDANCE-01 (C1) — on an Electronics project's
measurement-planning page the measurement-planning guidance is visible without a
click (title, guidance text and boundary), its source / adaptation / no-endorsement
notice is collapsed and opens from its summary, the PR #816 reference panel still
follows it collapsed, in EN and AR (RTL), and nothing overflows at 390 or 1280 px.
Synthetic data only.
"""
import pytest

pytest.importorskip("playwright.sync_api")

from tests.cap01_measurement_guidance_addition import MGUIDE_SLUG, MGUIDE_STEM  # noqa: E402
from tests.test_28t1_measurement_planning_reference_browser import _owned_project  # noqa: E402
from tests.test_draft_l2_local_continuity import _browser, page, server  # noqa: E402,F401
from tests.test_stage19_durable_success_criteria import PW  # noqa: E402
from web import ui_text  # noqa: E402

EMAIL = "c1-mguide-browser@example.com"


def _fits(pg, lang):
    width = pg.evaluate("document.documentElement.clientWidth")
    assert pg.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert pg.locator("[data-measurement-guidance]").bounding_box()["width"] <= width
    assert pg.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert pg.locator("html").get_attribute("dir") == "rtl"


def test_measurement_guidance_is_visible_its_source_opens_and_it_fits(server, page, monkeypatch):  # noqa: F811
    import tests.test_28t1_measurement_planning_reference_browser as ref
    monkeypatch.setattr(ref, "EMAIL", EMAIL)
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
            block = page.locator("[data-measurement-guidance]")
            assert block.count() == 1
            assert block.get_attribute("data-measurement-guidance") == MGUIDE_SLUG
            # Visible without any click: title, guidance text and boundary.
            assert block.locator("[data-mguide-title]").is_visible()
            assert block.locator("[data-mguide-title]").inner_text().strip() == \
                ui_text.text(MGUIDE_STEM + "TITLE", lang)
            assert block.locator("[data-mguide-item-text]").is_visible()
            assert block.locator("[data-mguide-boundary]").is_visible()
            # The source notice is collapsed, then opens from its summary.
            source = block.locator("[data-mguide-source]")
            assert source.evaluate("el => el.open") is False
            assert not block.locator("[data-mguide-source-text]").is_visible()
            _fits(page, lang)
            source.locator("summary").click()
            assert source.evaluate("el => el.open") is True
            assert block.locator("[data-mguide-source-text]").is_visible()
            _fits(page, lang)
            # The guidance precedes the (still collapsed) PR #816 reference panel.
            panel = page.locator("[data-measurement-reference]")
            assert panel.count() == 1 and panel.evaluate("el => el.open") is False
            assert block.bounding_box()["y"] < panel.bounding_box()["y"]
