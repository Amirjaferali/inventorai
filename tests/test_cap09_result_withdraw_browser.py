"""Real Chromium + the existing Flask server: CAP-09 RESULT WITHDRAW-01 on the
planning page and in report Section 11 (EN / AR).

Synthetic invention data only. A REAL saved project is started and answered
through the browser; the inventor records two executions of one experiment,
meets the required confirmation, withdraws one, sees it kept as labelled
history with no further control, and reads the report counting the one
CURRENT execution — at desktop and phone width.
"""
import os

import pytest
from playwright.sync_api import expect

from engine import experiment_result as er
from engine.record_store import SqliteRecordStore
from tests.test_draft_l2_local_continuity import server, _browser  # noqa: F401
from tests.test_success_criteria import _ids
from tests.test_success_criteria_workflow_browser import _browser_project
from web.app import S11_EXECUTION_TEXT
from web.ui_text import text


def _events(sid):
    store = SqliteRecordStore(os.environ["INVENTORAI_DB_PATH"])
    try:
        return store.load_result_events(sid)
    finally:
        store.close()


def _record(page, eid, value):
    form = page.locator('form[data-result-record]:has(input[name="experiment_id"][value="%s"])' % eid)
    form.locator('input[name="result_text"]').fill(value)
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_withdraw_one_execution_keeps_history_and_counts_current(server, _browser, lang):
    context = _browser.new_context(viewport={"width": 1280, "height": 900})
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    try:
        if lang == "ar":
            page.goto(server + "/")
            page.get_by_role("button", name="العربية", exact=True).click()
            page.wait_for_load_state()
        sid, state = _browser_project(page, server)
        eid = _ids(state)[0]
        url = server + "/session/%s/success-criteria" % sid
        page.goto(url)
        _record(page, eid, "First run: the lid opened in 3 s")
        page.goto(url)
        _record(page, eid, "تشغيل ثانٍ: فُتح الغطاء في كل مرة")
        first, second = _events(sid)

        page.goto(url)
        chain = page.locator("[data-result-chain]").first
        withdraw = chain.locator("[data-result-withdraw]")
        withdraw.locator("summary").click()
        expect(withdraw).to_contain_text(text("UI_R_WITHDRAW_NOTE", lang))
        button = withdraw.locator("button[type=submit]")
        expect(button).to_have_text(text("UI_R_WITHDRAW_BUTTON", lang))
        button.click()                                   # the browser requires the confirmation
        assert page.url == url and len(_events(sid)) == 2
        withdraw.locator('input[name="withdraw_confirm"]').check()
        button.click()
        page.wait_for_load_state()
        expect(page.locator(".notice")).to_contain_text(text("UI_R_MSG_WITHDRAW_SAVED", lang))
        events = _events(sid)
        assert len(events) == 3 and er.is_withdrawal(events[2])
        assert events[2].supersedes_result_event_id == first.result_event_id

        page.goto(url)
        withdrawn = page.locator("[data-result-chain-withdrawn]")
        expect(withdrawn).to_have_count(1)
        expect(withdrawn).to_contain_text(text("UI_R_WITHDRAWN", lang))
        expect(withdrawn).to_contain_text("First run: the lid opened in 3 s")
        expect(withdrawn.locator("form")).to_have_count(0)
        expect(page.locator("[data-result-withdraw]")).to_have_count(1)   # the other chain only
        assert er.WITHDRAWAL_MARKER not in page.content()

        page.goto(server + "/session/%s/deliverable" % sid)
        expect(page.locator("body")).to_contain_text(S11_EXECUTION_TEXT["recorded"].format(n=1))

        page.set_viewport_size({"width": 390, "height": 900})
        for path in ("/session/%s/success-criteria" % sid, "/session/%s/deliverable" % sid):
            page.goto(server + path)
            width = page.evaluate("document.documentElement.clientWidth")
            assert page.evaluate("document.documentElement.scrollWidth") <= width + 1, path
            if lang == "ar":
                assert page.locator("html").get_attribute("dir") == "rtl"
        assert not errors
    finally:
        context.close()
