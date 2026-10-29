"""Real Chromium + the existing Flask server: MTE-TEMPERATURE-CHANGE-DISCOVERABILITY-01
(Increment C), EN and AR.

Synthetic invention data only. On an integrated Mechanical + Electrical /
Electronics project the session page offers the one general free-expansion
link. After the inventor states that the Mechanical part experiences a
temperature change, the relevance explanation appears beside that statement
and the one link moves there; following it opens the method page with nothing
filled in. Withdrawing restores the general link. Arabic is RTL; at phone width
there is no horizontal overflow.
"""

import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import _start_integrated


def _links(page, sid):
    return page.locator(f'a[href="/session/{sid}/thermal-expansion"]')


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_relevance_moves_the_one_link_beside_the_statement(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_integrated(page, server, lang, "electronics_electrical")
    expect(_links(page, sid)).to_have_count(1)
    expect(page.locator("[data-mte-link]")).to_have_count(1)
    expect(page.locator("[data-mte-tc-relevance]")).to_have_count(0)

    page.locator("[data-part-tc-form=declare] input[name=tc_confirm]").check()
    page.locator("[data-part-tc-form=declare] button[type=submit]").click()
    page.wait_for_load_state()
    block = page.locator("[data-part-tc]")
    expect(block.locator("[data-mte-tc-relevance]")).to_have_text(
        text("UI_MTE_TC_RELEVANCE", lang))
    expect(_links(page, sid)).to_have_count(1)
    expect(block.locator("[data-mte-link-context]")).to_have_text(text("UI_MTE_LINK_TEXT", lang))
    expect(page.locator("[data-mte-link]")).to_have_count(0)

    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert block.bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"

    block.locator("[data-mte-link-context]").click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/thermal-expansion")
    expect(page.locator("[data-mte-form]")).to_have_count(1)
    for field in page.locator("[data-mte-form] input[type=text]").all():
        assert field.input_value() == ""
    assert page.locator("[data-mte-form] input[type=radio]:checked").count() == 0

    page.goto(f"{server}/session/{sid}")
    page.locator("[data-part-tc-form=withdraw] button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-mte-tc-relevance]")).to_have_count(0)
    expect(_links(page, sid)).to_have_count(1)
    expect(page.locator("[data-mte-link]")).to_have_count(1)
    assert not errors
