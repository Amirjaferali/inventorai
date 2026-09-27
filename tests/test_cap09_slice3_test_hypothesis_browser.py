"""Real Chromium + the existing Flask server: CAP-09 SLICE 3, the Owner-defined
Test Hypothesis on the existing planning page and in report Section 11 (EN/AR).

Synthetic invention data only. A REAL saved project is started and answered
through the browser; the inventor then records hypotheses for several
experiments, edits one, clears one, meets a whole-submission rejection with
the drafts preserved, and reads the result in the report — at desktop and
phone width.
"""
import os

import pytest
from playwright.sync_api import expect

from engine.record_store import SqliteRecordStore
from tests.test_draft_l2_local_continuity import server, _browser  # noqa: F401
from tests.test_success_criteria import _ids
from tests.test_success_criteria_workflow_browser import _browser_project
from web.ui_text import text


def _durable(sid):
    """The committed hypotheses, through a SEPARATE connection."""
    store = SqliteRecordStore(os.environ["INVENTORAI_DB_PATH"])
    try:
        return (dict(store.load_test_hypotheses(sid)),
                dict(store.load_success_criteria(sid)),
                dict(store.load_measurement_methods(sid)))
    finally:
        store.close()


def _hyp(page, eid):
    return page.locator('textarea[name="hypothesis__%s"]' % eid)


def _save(page):
    page.locator('form[action$="/success-criteria"] button[type=submit]').click()
    page.wait_for_load_state()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_hypothesis_create_edit_clear_reject_and_report(server, _browser, lang):
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
        ids = _ids(state)
        assert len(ids) >= 3
        page.goto(server + "/session/%s/success-criteria" % sid)
        assert page.locator("html").get_attribute("lang") == lang
        expect(page.locator(".intro")).to_contain_text(text("UI_SC_HYPOTHESIS_INTRO", lang))
        for eid in ids:                                   # one field per experiment
            field = _hyp(page, eid)
            expect(field).to_be_visible()
            assert field.get_attribute("dir") == "auto"
            label = page.locator('label[for="%s"]' % field.get_attribute("id"))
            expect(label).to_have_text(text("UI_SC_HYPOTHESIS_LABEL", lang))

        # create: two hypotheses (one Arabic, verbatim) and a criterion, ONE save
        _hyp(page, ids[0]).fill("The lamp lights within 1 s")
        _hyp(page, ids[1]).fill("أتوقع أن يعمل الحساس ليلًا")
        page.locator('textarea[name="criterion__%s"]' % ids[0]).fill("visible at 50 m")
        _save(page)
        assert page.url.endswith("/deliverable")
        hyps, crits, methods = _durable(sid)
        assert hyps == {ids[0]: "The lamp lights within 1 s",
                        ids[1]: "أتوقع أن يعمل الحساس ليلًا"}
        assert crits == {ids[0]: "visible at 50 m"} and methods == {}
        shown = page.locator("[data-test-hypothesis] .user-hypothesis")
        expect(shown).to_have_count(2)
        assert sorted(shown.all_inner_texts()) == sorted(hyps.values())
        assert shown.first.get_attribute("dir") == "auto"
        expect(page.locator("[data-test-hypothesis]").first).to_contain_text(
            text("UI_DELIV_HYPOTHESIS_DEFINED", lang))
        expect(page.locator("[data-test-hypothesis-absent]")).to_have_count(len(ids) - 2)

        # edit one, clear the other
        page.goto(server + "/session/%s/success-criteria" % sid)
        expect(_hyp(page, ids[0])).to_have_value("The lamp lights within 1 s")
        _hyp(page, ids[0]).fill("The lamp lights within 0.5 s")
        _hyp(page, ids[1]).fill("")
        _save(page)
        hyps, crits, _ = _durable(sid)
        assert hyps == {ids[0]: "The lamp lights within 0.5 s"}
        assert crits == {ids[0]: "visible at 50 m"}              # untouched

        # rejection: an over-limit hypothesis refuses the WHOLE submission and
        # every typed draft stays in the form, marked unsaved
        page.goto(server + "/session/%s/success-criteria" % sid)
        _hyp(page, ids[2]).evaluate("e => e.removeAttribute('maxlength')")
        _hyp(page, ids[2]).fill("x" * 1001)
        _hyp(page, ids[0]).fill("draft that must not be saved")
        page.locator('textarea[name="method__%s"]' % ids[1]).fill("draft method")
        _save(page)
        expect(page.locator(".error")).to_have_text(
            text("UI_SC_ERR_HYPOTHESIS_TOO_LONG", lang))
        expect(page.locator("#draft-unsaved")).to_be_visible()
        expect(_hyp(page, ids[0])).to_have_value("draft that must not be saved")
        expect(page.locator('textarea[name="method__%s"]' % ids[1])).to_have_value(
            "draft method")
        assert _durable(sid) == ({ids[0]: "The lamp lights within 0.5 s"},
                                 {ids[0]: "visible at 50 m"}, {})

        # phone width: the planning page and the report stay coherent, RTL on AR
        page.set_viewport_size({"width": 390, "height": 900})
        for url in ("/session/%s/success-criteria" % sid, "/session/%s/deliverable" % sid):
            page.goto(server + url)
            width = page.evaluate("document.documentElement.clientWidth")
            assert page.evaluate("document.documentElement.scrollWidth") <= width + 1, url
            if lang == "ar":
                assert page.locator("html").get_attribute("dir") == "rtl"
        page.goto(server + "/session/%s/success-criteria" % sid)
        box = _hyp(page, ids[0]).bounding_box()
        assert box["width"] <= 390 and box["x"] >= 0
        assert not errors
    finally:
        context.close()
