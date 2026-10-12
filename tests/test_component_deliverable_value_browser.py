"""Real Chromium + the existing Flask server: COMPONENT-DELIVERABLE-VALUE-01 (EN and AR).

Synthetic invention data only. An Electronics project is started through the real forms; three
components are declared and one is withdrawn through the component owner on this thread's own store
connection to the same database (the server thread keeps its own). The report then shows the
"Components you have declared" section with the two CURRENT components in declaration order — inventor
text direction-isolated, the boundary, provenance and history lines visible, no interactive control
inside it — and never the withdrawn one. At phone width there is no horizontal overflow; in Arabic the
page is RTL.
"""
import os

import pytest
from playwright.sync_api import expect

from engine import subsystem_model as sm
from engine.record_store import SqliteRecordStore
from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap01_electrical_energy_time_reference_browser import _start_electronics


def _declare(store, sid, name, function, key):
    item = sm.declared_component((), name, function, ())
    store.append_project_component(sid, item, key)
    return item


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_declared_components_section_renders_and_fits_phone_width(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_electronics(page, server, lang)
    store = SqliteRecordStore(os.environ["INVENTORAI_DB_PATH"])
    try:
        _declare(store, sid, "Thermal fuse TF-1", "Cuts power when the board overheats", "b-1")
        gone = _declare(store, sid, "Old relay", "Was replaced", "b-2")
        _declare(store, sid, "حساس حرارة NTC-10k", "يقيس درجة حرارة اللوحة", "b-3")
        _subs, inv = store.load_component_inventory_record(sid)
        store.append_component_revision(
            sid, sm.withdrawn_component_revision(inv, gone.component_id, 0), "b-w")
    finally:
        store.close()

    page.goto(f"{server}/session/{sid}/deliverable")
    section = page.locator("[data-declared-components]")
    expect(section).to_have_count(1)
    expect(section).to_be_visible()
    expect(section.locator("h2")).to_have_text(text("UI_CI_HEADING", lang))
    items = section.locator("[data-dc-item]")
    expect(items).to_have_count(2)
    expect(items.nth(0).locator("[data-dc-name]")).to_have_text("Thermal fuse TF-1")
    expect(items.nth(1).locator("[data-dc-name]")).to_have_text("حساس حرارة NTC-10k")
    expect(items.nth(1).locator("[data-dc-function]")).to_have_text("يقيس درجة حرارة اللوحة")
    for i in range(2):
        assert items.nth(i).locator("[data-dc-name]").evaluate("e => e.tagName") == "BDI"
        assert items.nth(i).locator("[data-dc-name]").get_attribute("dir") == "auto"
        expect(items.nth(i).locator("[data-dc-provenance]")).to_have_text(text("UI_DC_PROVENANCE", lang))
    expect(section.locator("[data-dc-boundary]")).to_have_text(text("UI_CI_BOUNDARY", lang))
    expect(section.locator("[data-dc-history]")).to_have_text(text("UI_DC_HISTORY", lang))
    expect(section).not_to_contain_text("Old relay")
    assert section.locator("a, button, form, input, select, textarea").count() == 0

    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert section.bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
