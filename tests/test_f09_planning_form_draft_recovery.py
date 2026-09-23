"""F-09 — bounded planning-form recovery (Stage-19 planning page).

File-creation contract:
  Path: tests/test_f09_planning_form_draft_recovery.py
  Purpose: prove that a refused planning submission never discards what the
    inventor just typed (the rejected SuccessCriterion / MeasurementMethod
    drafts are re-shown, escaped and explicitly UNSAVED, and nothing is
    written), that the 1000-character limit is truthful about line breaks
    (a browser submits each as CRLF, and the guidance says so), and that the
    existing durable text semantics are UNCHANGED: no line-ending
    canonicalization, exact preservation, legacy CRLF and LF rows keep their
    bytes, and an untouched value is never rewritten merely because the page
    was saved.
  Input contract: the live web app, the conftest per-test on-disk SQLite
    database, REAL /start -> answer journeys, and (for the browser case) the
    existing single-thread live server fixture with JavaScript DISABLED.
  Output contract: pass/fail evidence only.
  Prohibited behaviors: no activation doubles; no fabricated results; no
    production JavaScript; no change to stored text semantics.
"""
import copy
import html
import os
import sqlite3

import pytest
from playwright.sync_api import expect

import web.app as webapp
from web.app import app, SESSION_STORE
from web.ui_text import text
from engine.record_store import SqliteRecordStore
from tests.csrf_client import csrf_client
from tests.test_stage19_durable_success_criteria import (
    PREFIX, _journey, _restart, _live_ids, _reopened_items, _criteria_page,
    _durable, _db_path)
from tests.test_draft_l2_local_continuity import server, _browser  # noqa: F401 (fixtures)
from tests.test_success_criteria_workflow_browser import _browser_project

METHOD = "method__"
LIMIT = 1000
TOO_LONG_CRITERION = "A criterion exceeds the 1000-character limit. No changes were saved."
TOO_LONG_METHOD = webapp.SC_METHOD_TOO_LONG_MESSAGE


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return csrf_client(app)


def _post(client, sid, criteria=None, methods=None):
    data = {PREFIX + k: v for k, v in (criteria or {}).items()}
    data.update({METHOD + k: v for k, v in (methods or {}).items()})
    return client.post("/session/%s/success-criteria" % sid, data=data)


def _methods(sid):
    return dict(webapp._get_store().load_measurement_methods(sid))


def _multiline(visible, lines, eol="\r\n", fill="a"):
    """A value of exactly ``visible`` non-line-break characters spread over
    ``lines`` lines, joined by ``eol`` — i.e. what a browser shows as
    ``visible + lines - 1`` characters and SUBMITS (eol=CRLF) as
    ``visible + 2 * (lines - 1)`` characters."""
    base, extra = divmod(visible, lines)
    parts = [fill * (base + (1 if i < extra else 0)) for i in range(lines)]
    return eol.join(parts)


def _textarea(body, name):
    """The raw (still escaped) content of the named textarea."""
    start = body.index('name="%s"' % name)
    open_end = body.index(">", start) + 1
    return body[open_end:body.index("</textarea>", open_end)]


def _insert_raw_row(table, column, sid, eid, value):
    """Test-only legacy-row injection: a value written by another client (LF),
    bypassing the browser, exactly as a pre-existing durable row would exist."""
    con = sqlite3.connect(_db_path())
    try:
        con.execute("INSERT INTO %s (project_id, experiment_id, %s) VALUES (?, ?, ?)"
                    % (table, column), (sid, eid, value))
        con.commit()
    finally:
        con.close()


def _raw_value(table, column, sid, eid):
    con = sqlite3.connect(_db_path())
    try:
        row = con.execute("SELECT %s FROM %s WHERE project_id = ? AND experiment_id = ?"
                          % (column, table), (sid, eid)).fetchone()
        return None if row is None else row[0]
    finally:
        con.close()


# ==========================================================================
# 2 / 4 — multiline boundary: refused truthfully, draft kept, nothing written
# ==========================================================================
@pytest.mark.parametrize("concept", ["criterion", "method"])
def test_browser_counted_multiline_value_over_the_submitted_limit_keeps_the_draft(
        client, concept):
    """What the browser counted as 1000 characters (990 letters + 10 line
    breaks) is SUBMITTED as 1010 (each break = CRLF): refused, never reported
    as saved, re-shown exactly as typed, and the durable value is unchanged."""
    sid = _journey(client)
    ids = _live_ids(sid)
    eid = ids[0]
    _post(client, sid, criteria={eid: "durable criterion"},
          methods={eid: "durable method"})
    live = SESSION_STORE[sid]["state"]
    memory_before = (copy.deepcopy(live.success_criteria),
                     copy.deepcopy(live.measurement_methods))
    draft = _multiline(990, 11)                       # 990 + 10 CRLF = 1010 submitted
    assert len(draft.replace("\r\n", "\n")) == 1000 and len(draft) == 1010
    if concept == "criterion":
        r = _post(client, sid, criteria={eid: draft}, methods={eid: "durable method"})
        field, expected_error = PREFIX + eid, TOO_LONG_CRITERION
    else:
        r = _post(client, sid, criteria={eid: "durable criterion"}, methods={eid: draft})
        field, expected_error = METHOD + eid, TOO_LONG_METHOD
    raw = r.get_data(as_text=True)
    body = html.unescape(raw)
    assert r.status_code == 400                       # refused, not a redirect
    assert expected_error in body
    assert text("UI_SC_DRAFT_UNSAVED", "en") in body   # explicitly UNSAVED
    assert webapp.SC_SAVED_NOT_SHOWN_MESSAGE not in body
    assert html.unescape(_textarea(raw, field)) == draft          # draft, as typed
    assert _durable(sid) == {eid: "durable criterion"}            # nothing written
    assert _methods(sid) == {eid: "durable method"}
    assert (live.success_criteria, live.measurement_methods) == memory_before


@pytest.mark.parametrize("concept", ["criterion", "method"])
def test_valid_submitted_boundary_saves_exactly_and_survives_restart(client, concept):
    """Exactly 1000 SUBMITTED characters (CRLF counted as two) is accepted and
    stored byte-for-byte — CRLF kept, nothing canonicalized."""
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    value = _multiline(980, 11)                       # 980 + 10 CRLF = 1000 submitted
    assert len(value) == LIMIT and "\r\n" in value
    payload = {"criteria": {eid: value}} if concept == "criterion" else {"methods": {eid: value}}
    r = _post(client, sid, **payload)
    assert r.status_code == 302 and r.headers["Location"].endswith("/deliverable")
    stored = _durable(sid)[eid] if concept == "criterion" else _methods(sid)[eid]
    assert stored == value
    _restart()
    item = _reopened_items(sid)[eid]
    key = "success_criterion" if concept == "criterion" else "measurement_method"
    assert item[key] == value


@pytest.mark.parametrize("concept", ["criterion", "method"])
def test_one_submitted_character_over_the_limit_is_refused_and_kept(client, concept):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    value = _multiline(981, 11)                       # 1001 submitted
    assert len(value) == LIMIT + 1
    payload = {"criteria": {eid: value}} if concept == "criterion" else {"methods": {eid: value}}
    r = _post(client, sid, **payload)
    raw = r.get_data(as_text=True)
    assert r.status_code == 400
    field = (PREFIX if concept == "criterion" else METHOD) + eid
    assert html.unescape(_textarea(raw, field)) == value
    assert _durable(sid) == {} and _methods(sid) == {}


# ==========================================================================
# 5 — NUL stays refused; the draft never re-introduces it
# ==========================================================================
@pytest.mark.parametrize("lang", ["en", "ar"])
def test_nul_is_still_refused_and_never_echoed(client, lang):
    sid = _journey(client)
    ids = _live_ids(sid)
    client.post("/ui-language", data={"lang": lang})
    r = _post(client, sid, criteria={ids[0]: "keep this draft"},
              methods={ids[0]: "mid\x00dle"})
    raw = r.get_data(as_text=True)
    assert r.status_code == 400
    assert webapp._free_text_error("mid\x00dle", lang) in html.unescape(raw)
    assert "\x00" not in raw                                   # never echoed
    assert html.unescape(_textarea(raw, METHOD + ids[0])) == "middle"
    assert html.unescape(_textarea(raw, PREFIX + ids[0])) == "keep this draft"
    assert text("UI_SC_DRAFT_UNSAVED", lang) in html.unescape(raw)
    assert _durable(sid) == {} and _methods(sid) == {}         # nothing entered state
    client.post("/ui-language", data={"lang": "en"})


# ==========================================================================
# 6 — one combined submission: a refusal writes NEITHER concept
# ==========================================================================
def test_refused_combined_submission_is_not_partially_written(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post(client, sid, criteria={ids[1]: "c-before"}, methods={ids[1]: "m-before"})
    r = _post(client, sid,
              criteria={ids[0]: "a valid new criterion", ids[1]: "c-edited"},
              methods={ids[0]: _multiline(995, 6), ids[1]: "m-edited"})  # 1005 submitted
    raw = r.get_data(as_text=True)
    assert r.status_code == 400
    assert _durable(sid) == {ids[1]: "c-before"}
    assert _methods(sid) == {ids[1]: "m-before"}
    # every submitted draft of BOTH concepts is kept, not only the bad one
    assert html.unescape(_textarea(raw, PREFIX + ids[0])) == "a valid new criterion"
    assert html.unescape(_textarea(raw, PREFIX + ids[1])) == "c-edited"
    assert html.unescape(_textarea(raw, METHOD + ids[1])) == "m-edited"


# ==========================================================================
# Escaping, unknown ids, and truthful guidance
# ==========================================================================
def test_rejected_draft_is_escaped_never_reflected_as_markup(client):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    hostile = '</textarea><script>alert("x")</script><b>bold</b>' + "y" * LIMIT
    raw = _post(client, sid, methods={eid: hostile}).get_data(as_text=True)
    assert "<script>" not in raw and "<b>bold</b>" not in raw
    assert "&lt;/textarea&gt;&lt;script&gt;" in raw
    assert html.unescape(_textarea(raw, METHOD + eid)) == hostile
    assert _methods(sid) == {}


def test_unknown_experiment_refusal_also_keeps_the_current_drafts(client):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    rogue = "exp_v1_acknowledged_unknown_" + "9" * 32
    raw = _post(client, sid, criteria={eid: "typed criterion", rogue: "x"},
                methods={eid: "typed method"}).get_data(as_text=True)
    assert html.unescape(_textarea(raw, PREFIX + eid)) == "typed criterion"
    assert html.unescape(_textarea(raw, METHOD + eid)) == "typed method"
    assert rogue not in raw                              # never rendered as a field
    assert _durable(sid) == {} and _methods(sid) == {}


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_guidance_states_how_line_breaks_count_and_no_script_is_used(client, lang):
    sid = _journey(client)
    client.post("/ui-language", data={"lang": lang})
    r, body = _criteria_page(client, sid)
    client.post("/ui-language", data={"lang": "en"})
    assert r.status_code == 200
    guidance = text("UI_SC_LIMIT", lang).format(limit=LIMIT)
    assert body.count(guidance) == 2 * len(_live_ids(sid))   # every field, both concepts
    assert "<script" not in body                              # no JS is relied on
    assert 'maxlength="1000"' in body                         # the hard upper bound stays
    assert 'id="draft-unsaved"' not in body                   # only after a refusal


# ==========================================================================
# 1 / 7 — exact preservation and legacy rows: bytes are never rewritten
# ==========================================================================
def test_exact_internal_line_breaks_and_tabs_are_still_preserved(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    values = {ids[0]: "crlf one\r\ncrlf two", ids[1]: "lf one\nlf two\twith tab",
              ids[2]: "cr one\rcr two"}
    assert _post(client, sid, criteria=values, methods=values).status_code == 302
    assert _durable(sid) == values and _methods(sid) == values


def test_untouched_legacy_lf_row_is_not_rewritten_by_an_unrelated_edit(client):
    """A browser re-submits an untouched LF value as CRLF. Saving another field
    must not rewrite it (and must not refuse it for length)."""
    sid = _journey(client)
    ids = _live_ids(sid)
    lf_long = _multiline(990, 11, eol="\n")               # 1000 stored; 1010 as CRLF
    _insert_raw_row("prototype_measurement_methods", "measurement_method",
                    sid, ids[0], lf_long)
    _insert_raw_row("prototype_plan_metadata", "success_criterion",
                    sid, ids[0], "lf a\nlf b")
    r, body = _criteria_page(client, sid)
    assert r.status_code == 200                           # legacy LF loads & displays
    as_browser = {"criteria": {ids[0]: "lf a\r\nlf b", ids[1]: "a new criterion"},
                  "methods": {ids[0]: lf_long.replace("\n", "\r\n")}}
    r = _post(client, sid, **as_browser)
    assert r.status_code == 302                           # not refused for length
    assert _raw_value("prototype_measurement_methods", "measurement_method",
                      sid, ids[0]) == lf_long             # untouched: LF bytes kept
    assert _raw_value("prototype_plan_metadata", "success_criterion",
                      sid, ids[0]) == "lf a\nlf b"
    assert _durable(sid)[ids[1]] == "a new criterion"     # the real edit was saved
    _restart()
    items = _reopened_items(sid)
    assert items[ids[0]]["measurement_method"] == lf_long


def test_legacy_crlf_row_loads_edits_and_is_written_exactly_when_changed(client):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    _insert_raw_row("prototype_plan_metadata", "success_criterion", sid, eid,
                    "old one\r\nold two")
    r, body = _criteria_page(client, sid)
    assert r.status_code == 200 and "old one\r\nold two</textarea>" in body
    # unchanged resubmission: untouched
    assert _post(client, sid, criteria={eid: "old one\r\nold two"}).status_code == 302
    assert _durable(sid) == {eid: "old one\r\nold two"}
    # a genuine edit is written exactly as submitted (CRLF kept)
    assert _post(client, sid, criteria={eid: "new one\r\nnew two"}).status_code == 302
    assert _durable(sid) == {eid: "new one\r\nnew two"}
    _restart()
    assert _reopened_items(sid)[eid]["success_criterion"] == "new one\r\nnew two"


def test_clearing_an_existing_value_still_deletes_it(client):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    _post(client, sid, criteria={eid: "c"}, methods={eid: "m"})
    assert _post(client, sid, criteria={eid: " \r\n "}, methods={eid: ""}).status_code == 302
    assert _durable(sid) == {} and _methods(sid) == {}


# ==========================================================================
# 8 — real browser, JavaScript DISABLED: refuse, keep, correct, save, reopen
# ==========================================================================
def test_browser_multiline_refusal_keeps_the_draft_then_saves_after_correction(
        server, _browser):
    setup = _browser.new_context()
    try:
        sid, state = _browser_project(setup.new_page(), server)
    finally:
        setup.close()
    eid = [it["experiment_id"] for it in
           __import__("engine.deliverable_assembler", fromlist=["x"])
           .assemble_deliverable(state)["section_11_prototype_test_plan"]["items"]][0]
    context = _browser.new_context(java_script_enabled=False)
    page = context.new_page()
    try:
        page.goto(server + f"/session/{sid}/success-criteria")
        method = page.locator(f'[name="{METHOD}{eid}"]')
        criterion = page.locator(f'[name="{PREFIX}{eid}"]')
        typed = _multiline(990, 11, eol="\n")        # the browser counts 1000
        method.fill(typed)
        criterion.fill("line one\nline two")
        assert method.input_value() == typed            # maxlength allowed it
        page.locator('form[action$="/success-criteria"] button').click()
        page.wait_for_load_state()
        # refused (1010 submitted), explained, and NOTHING the user typed is lost
        expect(page.locator(".error")).to_contain_text("measurement method exceeds")
        expect(page.locator("#draft-unsaved")).to_be_visible()
        assert page.locator(f'[name="{METHOD}{eid}"]').input_value() == typed
        assert page.locator(f'[name="{PREFIX}{eid}"]').input_value() == "line one\nline two"
        store = SqliteRecordStore(os.environ["INVENTORAI_DB_PATH"])
        try:
            assert store.load_measurement_methods(sid) == ()
            assert store.load_success_criteria(sid) == ()
        finally:
            store.close()
        # correct it (drop 10 letters) and save: now 1000 as submitted
        corrected = _multiline(980, 11, eol="\n")
        page.locator(f'[name="{METHOD}{eid}"]').fill(corrected)
        page.locator('form[action$="/success-criteria"] button').click()
        page.wait_for_load_state()
        assert page.url.endswith("/deliverable")
        store = SqliteRecordStore(os.environ["INVENTORAI_DB_PATH"])   # a reopen
        try:
            assert dict(store.load_measurement_methods(sid)) == {
                eid: corrected.replace("\n", "\r\n")}    # exactly as the browser sent
            assert dict(store.load_success_criteria(sid)) == {
                eid: "line one\r\nline two"}
        finally:
            store.close()
        fresh = _browser.new_context(java_script_enabled=False).new_page()
        fresh.goto(server + f"/session/{sid}/success-criteria")
        assert fresh.locator(f'[name="{METHOD}{eid}"]').input_value() == corrected
        fresh.context.close()
    finally:
        context.close()
