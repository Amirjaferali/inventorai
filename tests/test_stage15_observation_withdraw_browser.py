"""Real Chromium + the existing Flask server: STAGE15-OBSERVATION-WITHDRAW-01
on the interface preparation page (EN / AR, desktop and phone width).

Synthetic invention data only. An integrated Mechanical + Electrical /
Electronics invention is started through the real composition form and ONE
interaction is declared; the inventor records two checks, meets the required
confirmation, withdraws one, and sees it kept as labelled history with no
further control while the status counts the one CURRENT check.
"""
import os

import pytest
from playwright.sync_api import expect

from engine import interface_observation as io
from engine import subsystem_model as sm
from engine.record_store import SqliteRecordStore
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import _start_integrated
from web.ui_text import text


def _store():
    return SqliteRecordStore(os.environ["INVENTORAI_DB_PATH"])


def _declare_interface(sid):
    store = _store()
    try:
        subs = store.load_project_subsystems(sid)
        item = sm.declared_interface(subs, subs[0].subsystem_id, subs[1].subsystem_id,
                                     "The motor drives the hinge arm.")
        store.append_subsystem_interface(sid, item, "browser-ifc")
        return item.interface_id
    finally:
        store.close()


def _events(sid):
    store = _store()
    try:
        return store.load_interface_observations(sid)
    finally:
        store.close()


def _record(page, text_value):
    form = page.locator("form[data-obs-record]")
    form.locator("textarea[name=observation_text]").fill(text_value)
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()


@pytest.mark.parametrize("lang,width", [("en", 1280), ("ar", 390)])
def test_withdraw_one_check_keeps_history_and_counts_current(server, page, lang, width):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.set_viewport_size({"width": width, "height": 900})
    sid = _start_integrated(page, server, lang, "mechanical")
    _declare_interface(sid)
    url = server + "/session/%s/interface-preparation" % sid
    page.goto(url)
    _record(page, "The arm opened in 2 s on the first check.")
    page.goto(url)
    _record(page, "إعادة الفحص: فُتح الذراع في كل مرة")
    first, _second = _events(sid)

    page.goto(url)
    chain = page.locator("[data-obs-chain]").first
    withdraw = chain.locator("[data-obs-withdraw]")
    withdraw.locator("summary").click()
    expect(withdraw).to_contain_text(text("UI_S15_OBS_WITHDRAW_NOTE", lang))
    button = withdraw.locator("button[type=submit]")
    expect(button).to_have_text(text("UI_S15_OBS_WITHDRAW_BUTTON", lang))
    button.click()                                   # the browser requires the confirmation
    assert len(_events(sid)) == 2
    withdraw.locator("input[name=withdraw_confirm]").check()
    button.click()
    page.wait_for_load_state()
    expect(page.locator(".notice").first).to_contain_text(
        text("UI_S15_OBS_MSG_WITHDRAW_SAVED", lang))
    events = _events(sid)
    assert len(events) == 3 and io.is_withdrawal(events[2])
    assert events[2].supersedes_observation_id == first.observation_id

    page.goto(url)
    withdrawn = page.locator("[data-obs-chain-withdrawn]")
    expect(withdrawn).to_have_count(1)
    expect(withdrawn).to_contain_text(text("UI_S15_OBS_WITHDRAWN", lang))
    expect(withdrawn).to_contain_text("The arm opened in 2 s on the first check.")
    expect(withdrawn.locator("form")).to_have_count(0)
    expect(page.locator("[data-obs-withdraw]")).to_have_count(1)
    expect(page.locator("[data-status-checks]")).to_contain_text(
        text("UI_S15_ST_CHECKS_COUNT", lang).format(count=1))
    assert io.WITHDRAWAL_MARKER not in page.content()

    viewport = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= viewport + 1
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors
