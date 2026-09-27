"""Real Chromium + the existing Flask server: CAP-09 SLICE 4, the Owner-defined
Test Variable / Condition on the existing planning page and in report
Section 11 (EN/AR).

Synthetic invention data only. A REAL saved project is started and answered
through the browser; the inventor then records variables / conditions for
several experiments together with the other three planning entries in ONE
Save, edits one, clears one, meets a whole-submission rejection with all four
drafts preserved, and reads the result in the report — at desktop and phone
width.
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
    """The committed planning entries, through a SEPARATE connection."""
    store = SqliteRecordStore(os.environ["INVENTORAI_DB_PATH"])
    try:
        return {"variables": dict(store.load_test_variables(sid)),
                "hypotheses": dict(store.load_test_hypotheses(sid)),
                "criteria": dict(store.load_success_criteria(sid)),
                "methods": dict(store.load_measurement_methods(sid))}
    finally:
        store.close()


def _box(page, prefix, eid):
    return page.locator('textarea[name="%s__%s"]' % (prefix, eid))


def _save(page):
    page.locator('form[action$="/success-criteria"] button[type=submit]').click()
    page.wait_for_load_state()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_variable_create_edit_clear_reject_and_report(server, _browser, lang):
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
        expect(page.locator(".intro")).to_contain_text(text("UI_SC_VARIABLE_INTRO", lang))
        for eid in ids:                                   # one field per experiment
            field = _box(page, "variable", eid)
            expect(field).to_be_visible()
            assert field.get_attribute("dir") == "auto"
            label = page.locator('label[for="%s"]' % field.get_attribute("id"))
            expect(label).to_have_text(text("UI_SC_VARIABLE_LABEL", lang))
            # card order: criterion -> hypothesis -> variable -> method
            ys = [_box(page, p, eid).bounding_box()["y"]
                  for p in ("criterion", "hypothesis", "variable", "method")]
            assert ys == sorted(ys), ys
        guidance = page.locator("#" + _box(page, "variable", ids[0]).get_attribute("id")
                                .replace("variable-", "variable-guidance-"))
        expect(guidance).to_contain_text(text("UI_SC_VARIABLE_NOT_RESULT", lang))

        # create: all four planning entries for one experiment + a second
        # variable (Arabic, verbatim) in ONE save
        _box(page, "criterion", ids[0]).fill("visible at 50 m")
        _box(page, "hypothesis", ids[0]).fill("Brighter LEDs are seen further")
        _box(page, "variable", ids[0]).fill("Compare 1 W and 3 W LEDs")
        _box(page, "method", ids[0]).fill("Tape measure at dusk")
        _box(page, "variable", ids[1]).fill("قارن بين مسافتين للحساس")
        _save(page)
        assert page.url.endswith("/deliverable")
        d = _durable(sid)
        assert d["variables"] == {ids[0]: "Compare 1 W and 3 W LEDs",
                                  ids[1]: "قارن بين مسافتين للحساس"}
        assert d["hypotheses"] == {ids[0]: "Brighter LEDs are seen further"}
        assert d["criteria"] == {ids[0]: "visible at 50 m"}
        assert d["methods"] == {ids[0]: "Tape measure at dusk"}
        shown = page.locator("[data-test-variable] .user-variable")
        expect(shown).to_have_count(2)
        assert sorted(shown.all_inner_texts()) == sorted(d["variables"].values())
        assert shown.first.get_attribute("dir") == "auto"
        expect(page.locator("[data-test-variable]").first).to_contain_text(
            text("UI_DELIV_VARIABLE_DEFINED", lang))
        expect(page.locator("[data-test-variable-absent]")).to_have_count(len(ids) - 2)
        expect(page.locator("[data-test-variable-absent]").first).to_contain_text(
            text("UI_DELIV_VARIABLE_ABSENT", lang))

        # edit one, clear the other; the other three concepts stay unchanged
        page.goto(server + "/session/%s/success-criteria" % sid)
        expect(_box(page, "variable", ids[0])).to_have_value("Compare 1 W and 3 W LEDs")
        _box(page, "variable", ids[0]).fill("Compare 1 W, 3 W and 5 W LEDs")
        _box(page, "variable", ids[1]).fill("")
        _save(page)
        after = _durable(sid)
        assert after["variables"] == {ids[0]: "Compare 1 W, 3 W and 5 W LEDs"}
        for key in ("hypotheses", "criteria", "methods"):
            assert after[key] == d[key], key

        # rejection: an over-limit variable refuses the WHOLE submission and
        # every typed draft of all four concepts stays in the form, unsaved
        page.goto(server + "/session/%s/success-criteria" % sid)
        _box(page, "variable", ids[2]).evaluate("e => e.removeAttribute('maxlength')")
        _box(page, "variable", ids[2]).fill("x" * 1001)
        drafts = {"criterion": "draft c", "hypothesis": "draft h",
                  "variable": "draft v", "method": "draft m"}
        for prefix, value in drafts.items():
            _box(page, prefix, ids[1]).fill(value)
        _save(page)
        expect(page.locator(".error")).to_have_text(text("UI_SC_ERR_VARIABLE_TOO_LONG", lang))
        expect(page.locator("#draft-unsaved")).to_be_visible()
        for prefix, value in drafts.items():
            expect(_box(page, prefix, ids[1])).to_have_value(value)
        assert _durable(sid) == after                      # nothing saved

        # phone width: the planning page and the report stay coherent, RTL on AR
        page.set_viewport_size({"width": 390, "height": 900})
        for url in ("/session/%s/success-criteria" % sid, "/session/%s/deliverable" % sid):
            page.goto(server + url)
            width = page.evaluate("document.documentElement.clientWidth")
            assert page.evaluate("document.documentElement.scrollWidth") <= width + 1, url
            if lang == "ar":
                assert page.locator("html").get_attribute("dir") == "rtl"
        page.goto(server + "/session/%s/success-criteria" % sid)
        box = _box(page, "variable", ids[0]).bounding_box()
        assert box["width"] <= 390 and box["x"] >= 0
        assert not errors
    finally:
        context.close()
