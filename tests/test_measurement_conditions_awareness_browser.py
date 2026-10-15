"""Real Chromium: MEASUREMENT-CONDITIONS-AWARENESS-01 — on an Electronics project's
measurement-planning page the conditions note is visible without a click (title, text
and boundary), sits after the C1 guidance and before the collapsed PR #816 reference
panel, its source / adaptation / no-endorsement notice is collapsed and opens from its
summary, in EN and AR (RTL), and nothing overflows at 390 or 1280 px.
Synthetic data only.
"""
import pytest

pytest.importorskip("playwright.sync_api")

from tests.cap01_measurement_conditions_addition import MCOND_SLUG, MCOND_STEM  # noqa: E402
from tests.test_28t1_measurement_planning_reference_browser import _owned_project  # noqa: E402
from tests.test_draft_l2_local_continuity import _browser, page, server  # noqa: E402,F401
from tests.test_stage19_durable_success_criteria import PW  # noqa: E402
from web import ui_text  # noqa: E402

EMAIL = "mcond-browser@example.com"


def _fits(pg, lang):
    width = pg.evaluate("document.documentElement.clientWidth")
    assert pg.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert pg.locator("[data-measurement-conditions]").bounding_box()["width"] <= width
    assert pg.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert pg.locator("html").get_attribute("dir") == "rtl"


def test_measurement_conditions_note_is_visible_its_source_opens_and_it_fits(server, page, monkeypatch):  # noqa: F811
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
            block = page.locator("[data-measurement-conditions]")
            assert block.count() == 1
            assert block.get_attribute("data-measurement-conditions") == MCOND_SLUG
            assert block.locator("[data-mcond-title]").is_visible()
            assert block.locator("[data-mcond-title]").inner_text().strip() == \
                ui_text.text(MCOND_STEM + "TITLE", lang)
            assert block.locator("[data-mcond-item-text]").is_visible()
            assert block.locator("[data-mcond-boundary]").is_visible()
            source = block.locator("[data-mcond-source]")
            assert source.evaluate("el => el.open") is False
            assert not block.locator("[data-mcond-source-text]").is_visible()
            _fits(page, lang)
            source.locator("summary").click()
            assert source.evaluate("el => el.open") is True
            assert block.locator("[data-mcond-source-text]").is_visible()
            _fits(page, lang)
            guide = page.locator("[data-measurement-guidance]")
            panel = page.locator("[data-measurement-reference]")
            assert guide.count() == 1 and panel.count() == 1 and panel.evaluate("el => el.open") is False
            assert guide.bounding_box()["y"] < block.bounding_box()["y"] < panel.bounding_box()["y"]
