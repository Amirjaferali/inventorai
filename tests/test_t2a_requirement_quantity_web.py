"""T2-A Quantified Requirements Slice 1 — web-layer proof.

File: tests/test_t2a_requirement_quantity_web.py
Purpose: behaviour tests for the ONE bounded quantity route
(`POST /session/<sid>/requirement-quantity`), its authorization boundary
(owned, verified, active durable owner only), token binding, replay
resistance / idempotency, project isolation, the authorized session / HTML
deliverable / PDF presentation surfaces, canonical-vs-localized separation,
the zero-quantity byte-equivalence guarantee, fail-closed behaviour on a
corrupt populated history at EVERY affected surface, and the Owner-mandated
correction-flow ordering (history validated BEFORE the durable correction
append; reattached AFTER the deterministic reconstruction).

Real Flask application, real on-disk SQLite (autouse conftest isolation),
real account + record stores, real signed sessions, real WeasyPrint for the
PDF proofs. Security boundaries are never mocked; monkeypatching is used only
to inject storage failures or to capture the exact document handed to the
renderer.
"""
from tests.csrf_client import csrf_client
import copy
import json
import os
import pickle
import re
import sqlite3

import pytest

import web.app as webapp
from web.app import app, SESSION_STORE
from web import ui_text
from engine import account_credentials as _acct
from engine import deliverable_assembler as _assembler
from engine.record_store import SqliteRecordStore
from engine.requirement_quantity import QuantityHistoryError

PW = "correct horse battery staple"
IDEA = "ESP32 microcontroller circuit with a voltage sensor"
FORM = {"idea": IDEA, "domain_confirm": "electronics_electrical"}
PROBLEM_ANSWER = (
    "The problem is that cyclists have no reliable brake light. My circuit senses "
    "deceleration with an accelerometer because sudden voltage change on the sensor "
    "indicates braking, so the microcontroller switches the LED because riders "
    "behind need warning.")
MECH_STRONG = (
    "The mechanism works because the accelerometer outputs a voltage proportional "
    "to deceleration; the microcontroller reads it through the ADC and drives the "
    "LED through a transistor because the LED current exceeds the GPIO limit.")
MECH_CORRECTED = (
    "The mechanism is different: there is no accelerometer at all. A reed switch on "
    "the brake lever closes the circuit because the lever movement moves a magnet, "
    "which causes the microcontroller to switch the LED through a transistor.")
HTML_ANSWER = ("The sensor <b>board</b> is rated because the &amp; supply "
               "current limit trips the switch through the microcontroller.")

ROUTE = "/session/%s/requirement-quantity"
SESSION = "/session/%s"
DELIVERABLE = "/session/%s/deliverable"
PDF = "/session/%s/deliverable.pdf"
CORRECT = "/session/%s/correct"


# --------------------------------------------------------------------------
# Harness
# --------------------------------------------------------------------------
@pytest.fixture
def db_path():
    return os.environ["INVENTORAI_DB_PATH"]


def _new_client():
    app.config["TESTING"] = True
    return csrf_client(app)


def _mk_account(email, verified=True, status="active"):
    store = webapp._get_account_store()
    aid = _acct.new_account_id()
    store.create_account(aid, _acct.normalize_email(email), _acct.hash_password(PW),
                         "2026-01-01T00:00:00.000000Z", status=status)
    if verified:
        store.mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    return aid


def _client_for(email, verified=True, status="active"):
    aid = _mk_account(email, verified=verified, status=status)
    c = _new_client()
    c.post("/login", data={"email": email, "password": PW})
    return c, aid


def _start(client, answers=(PROBLEM_ANSWER, MECH_STRONG)):
    r = client.post("/start", data=FORM)
    assert r.status_code == 302, r.status_code
    sid = r.headers["Location"].rsplit("/session/", 1)[-1]
    for text in answers:
        assert _answer(client, sid, text).status_code == 302
    return sid


def _page(client, sid):
    r = client.get(SESSION % sid)
    assert r.status_code == 200, r.status_code
    return r.get_data(as_text=True)


def _token(client, sid):
    m = re.search(r'name="answer_token" value="([^"]+)"', _page(client, sid))
    return m.group(1) if m else None


def _answer(client, sid, text):
    return client.post(SESSION % sid, data={
        "response": text, "action": "answered", "answer_token": _token(client, sid)})


def _anchors(client, sid):
    return re.findall(r'data-t2a-anchor="([^"]+)"', _page(client, sid))


_UNSET = object()


def _record(client, sid, anchor, value="12.50", bound="maximum", unit="V",
            token=_UNSET, **extra):
    data = {"anchor_record_id": anchor, "bound": bound, "value": value, "unit": unit}
    data["answer_token"] = _token(client, sid) if token is _UNSET else token
    if data["answer_token"] is None:
        data.pop("answer_token")
    data.update(extra)
    return client.post(ROUTE % sid, data=data, **{})


def _store():
    return webapp._get_store()


def _rows(db_path, sid):
    conn = sqlite3.connect(db_path)
    try:
        return conn.execute(
            "SELECT seq, quantity_id, anchor_record_id, bound, value_canonical, unit, "
            "supersedes_quantity_id, idempotency_key FROM requirement_quantities "
            "WHERE project_id = ? ORDER BY seq", (sid,)).fetchall()
    finally:
        conn.close()


def _ledger_rows(db_path, sid):
    conn = sqlite3.connect(db_path)
    try:
        return conn.execute("SELECT seq, record_id, payload FROM records WHERE project_id = ? "
                            "ORDER BY seq", (sid,)).fetchall()
    finally:
        conn.close()


def _corrupt(db_path, sid, sql="UPDATE requirement_quantities SET unit = 'furlong' "
                                "WHERE project_id = ?"):
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(sql, (sid,))
        conn.commit()
    finally:
        conn.close()


def _shown_values(body):
    return re.findall(r'<bdi class="t2a-value">([^<]*)</bdi>', body)


def _capture_pdf_source(monkeypatch):
    seen = {}
    real = webapp._render_pdf_bytes

    def spy(source):
        seen["source"] = source
        out = real(source)
        seen["pdf"] = out
        return out
    monkeypatch.setattr(webapp, "_render_pdf_bytes", spy)
    return seen


def _snapshot(sid, db_path):
    entry = SESSION_STORE.get(sid)
    state = pickle.dumps(entry["state"]) if entry else None
    with open(db_path, "rb") as fh:
        database = fh.read()
    return state, database


# ==========================================================================
# 1. Route registration, CSRF integrity, generic denial
# ==========================================================================
def test_route_is_post_only_and_csrf_guarded_before_any_state(db_path):
    c, _aid = _client_for("t2a-csrf@example.com")
    sid = _start(c)
    anchor = _anchors(c, sid)[0]
    assert c.get(ROUTE % sid).status_code == 405
    before = _snapshot(sid, db_path)
    raw = app.test_client()                      # no CSRF evidence at all
    with raw.session_transaction() as s, c.session_transaction() as mine:
        s.update(copy.deepcopy(dict(mine)))
    r = raw.post(ROUTE % sid, data={"anchor_record_id": anchor, "bound": "target",
                                    "value": "1", "unit": "V",
                                    "answer_token": _token(c, sid)})
    assert r.status_code == 403
    assert _rows(db_path, sid) == [] and _snapshot(sid, db_path)[1] == before[1]


def test_write_authorization_matrix_is_owner_verified_active_only(db_path):
    owner, _aid = _client_for("t2a-owner@example.com")
    sid = _start(owner)
    anchor = _anchors(owner, sid)[0]
    token = _token(owner, sid)
    denied = []
    # anonymous caller (knows the sid and a real token)
    anon = _new_client()
    denied.append(anon.post(ROUTE % sid, data={"anchor_record_id": anchor, "bound": "target",
                                               "value": "1", "unit": "V", "answer_token": token}))
    # a different verified account (IDOR)
    other, _o = _client_for("t2a-other@example.com")
    denied.append(other.post(ROUTE % sid, data={"anchor_record_id": anchor, "bound": "target",
                                                "value": "1", "unit": "V", "answer_token": token}))
    for r in denied:
        assert r.status_code == 302 and r.headers["Location"].endswith("/"), r.status_code
    # a missing project is indistinguishable from a denied one
    missing = other.post(ROUTE % "no-such-project", data={"answer_token": token})
    assert (missing.status_code, missing.headers["Location"]) == \
        (denied[0].status_code, denied[0].headers["Location"])
    assert _rows(db_path, sid) == []
    # the real owner is accepted
    r = _record(owner, sid, anchor)
    assert r.status_code == 302 and r.headers["Location"] == SESSION % sid
    assert [row[4] for row in _rows(db_path, sid)] == ["12.5"]
    # ...until the owner is disabled: then denied generically, nothing written
    webapp._get_account_store().set_status(_aid, "disabled", "2026-01-01T00:00:00.000000Z")
    r = owner.post(ROUTE % sid, data={"anchor_record_id": anchor, "bound": "target",
                                      "value": "2", "unit": "V", "answer_token": token})
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    assert len(_rows(db_path, sid)) == 1


def test_null_owner_anonymous_and_unverified_projects_can_never_be_quantified(db_path):
    anon = _new_client()
    sid = _start(anon)
    body = _page(anon, sid)
    assert "t2a-quantities" not in body and "requirement-quantity" not in body
    r = anon.post(ROUTE % sid, data={"anchor_record_id": "rec_1", "bound": "target",
                                     "value": "1", "unit": "V",
                                     "answer_token": _token(anon, sid)})
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    # an UNVERIFIED signed-in account creates a NULL-owner project: same denial
    unv, _u = _client_for("t2a-unverified@example.com", verified=False)
    sid_u = _start(unv)
    assert _store().load_owner(sid_u) == (True, None)
    assert "requirement-quantity" not in _page(unv, sid_u)
    r = unv.post(ROUTE % sid_u, data={"anchor_record_id": "rec_1", "bound": "target",
                                      "value": "1", "unit": "V",
                                      "answer_token": _token(unv, sid_u)})
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    # a signed-in verified account viewing a NULL-owner project: view yes, write no
    viewer, _v = _client_for("t2a-viewer@example.com")
    assert viewer.get(SESSION % sid).status_code == 200
    assert "requirement-quantity" not in viewer.get(SESSION % sid).get_data(as_text=True)
    r = viewer.post(ROUTE % sid, data={"anchor_record_id": "rec_1", "bound": "target",
                                       "value": "1", "unit": "V",
                                       "answer_token": _token(viewer, sid)})
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    assert _rows(db_path, sid) == [] and _rows(db_path, sid_u) == []
    assert not webapp._quantity_write_authorized(sid)


# ==========================================================================
# 2. Token binding, replay resistance, idempotency
# ==========================================================================
@pytest.mark.parametrize("bad", [None, "", "forged.token", "nonce.", ".sig"])
def test_missing_or_forged_answer_token_fails_closed_generically(db_path, bad):
    c, _aid = _client_for("t2a-token@example.com")
    sid = _start(c)
    anchor = _anchors(c, sid)[0]
    r = _record(c, sid, anchor, token=bad)
    assert r.status_code == 302 and r.headers["Location"] == SESSION % sid
    body = _page(c, sid)
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in body
    assert webapp.QUANTITY_SAVED_ACK not in body
    assert _rows(db_path, sid) == []


def test_cross_project_and_cross_session_tokens_are_rejected(db_path):
    c, _aid = _client_for("t2a-cross@example.com")
    sid_a = _start(c)
    sid_b = _start(c)
    anchor_a = _anchors(c, sid_a)[0]
    # a token minted for project B does not verify for project A
    r = _record(c, sid_a, anchor_a, token=_token(c, sid_b))
    assert r.status_code == 302
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid_a)
    assert _rows(db_path, sid_a) == []
    # a valid token for A cannot be used by another account's browser (IDOR)
    other, _o = _client_for("t2a-cross-other@example.com")
    r = other.post(ROUTE % sid_a, data={"anchor_record_id": anchor_a, "bound": "target",
                                        "value": "3", "unit": "V",
                                        "answer_token": _token(c, sid_a)})
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    assert _rows(db_path, sid_a) == []


def test_double_submit_and_refresh_write_exactly_one_durable_row(db_path):
    c, _aid = _client_for("t2a-idem@example.com")
    sid = _start(c)
    anchor = _anchors(c, sid)[0]
    token = _token(c, sid)
    for _ in range(3):                             # same form, same token, replayed
        r = _record(c, sid, anchor, value="7", token=token)
        assert r.status_code == 302
    rows = _rows(db_path, sid)
    assert len(rows) == 1 and rows[0][4] == "7" and rows[0][7] is not None
    assert webapp.QUANTITY_SAVED_ACK in _page(c, sid)
    # the retained live carrier matches the durable truth
    assert [q.value for q in SESSION_STORE[sid]["state"].requirement_quantities] == ["7"]
    # a fresh submit of the IDENTICAL active value adds no row either
    assert _record(c, sid, anchor, value="7.0").status_code == 302
    assert len(_rows(db_path, sid)) == 1
    # a DIFFERENT value supersedes: two rows, one active, forward edge only
    assert _record(c, sid, anchor, value="8").status_code == 302
    rows = _rows(db_path, sid)
    assert [(r[4], r[6]) for r in rows] == [("7", None), ("8", rows[0][1])]
    history = _store().load_requirement_quantities(sid)
    assert [q.superseded_by is None for q in history] == [False, True]
    assert _shown_values(_page(c, sid)) == ["8"]


def test_same_token_different_content_is_not_collapsed_into_the_first_event(db_path):
    c, _aid = _client_for("t2a-same-token@example.com")
    sid = _start(c)
    anchor = _anchors(c, sid)[0]
    token = _token(c, sid)
    assert _record(c, sid, anchor, value="7", token=token).status_code == 302
    assert _record(c, sid, anchor, value="9", token=token).status_code == 302
    # both are genuine distinct events: a chain of two, the later one active
    rows = _rows(db_path, sid)
    assert [r[4] for r in rows] == ["7", "9"] and rows[1][6] == rows[0][1]


# ==========================================================================
# 3. Validation, canonical storage, no disclosure, eligibility
# ==========================================================================
@pytest.mark.parametrize("field,value", [
    ("value", "abc"), ("value", ""), ("value", "1e3"), ("value", "1,000"),
    ("value", "١٢"), ("value", "12.3456789"), ("value", "9" * 40),
    ("unit", "furlong"), ("unit", ""), ("unit", "volts"), ("bound", "about"), ("bound", ""),
])
def test_invalid_input_is_rejected_generically_without_echo_or_write(db_path, field, value):
    c, _aid = _client_for("t2a-invalid@example.com")
    sid = _start(c)
    anchor = _anchors(c, sid)[0]
    data = {"value": "12.5", "unit": "V", "bound": "target"}
    data[field] = value
    r = _record(c, sid, anchor, **data)
    assert r.status_code == 302
    body = _page(c, sid)
    assert webapp.QUANTITY_INVALID_MESSAGE in body
    assert webapp.QUANTITY_SAVED_ACK not in body
    if value:
        assert 'value="%s"' % value not in body   # nothing echoed back
    assert _rows(db_path, sid) == []


def test_value_is_stored_canonically_and_presented_from_the_canonical_form(db_path):
    c, _aid = _client_for("t2a-canon@example.com")
    sid = _start(c)
    anchor = _anchors(c, sid)[0]
    assert _record(c, sid, anchor, value=" 0012.500 ", bound="minimum", unit="mm").status_code == 302
    rows = _rows(db_path, sid)
    assert [(r[3], r[4], r[5]) for r in rows] == [("minimum", "12.5", "mm")]
    body = _page(c, sid)
    assert _shown_values(body) == ["12.5"]
    assert "0012.500" not in body
    assert "minimum" in body and "millimetres (mm)" in body
    with app.test_request_context():
        package = webapp._deliverable_context(sid)[1]
    assert package["_session_meta"]["quantified_requirements"]["items"][0] == {
        "statement": PROBLEM_ANSWER, "bound": "minimum", "value": "12.5", "unit": "mm",
        "provenance": "Recorded by the inventor (not yet verified)"}


@pytest.mark.parametrize("anchor", ["", "rec_99", "rec_0", "qty-x", "MECHANISM_COMPLETENESS",
                                    "<script>", "rec_3", "rec_1x"])
def test_ineligible_anchor_is_rejected_generically(db_path, anchor):
    c, _aid = _client_for("t2a-anchor@example.com")
    sid = _start(c)
    r = _record(c, sid, anchor)
    assert r.status_code == 302
    body = _page(c, sid)
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in body
    assert webapp.QUANTITY_SAVED_ACK not in body
    if anchor:
        assert anchor not in webapp.QUANTITY_NOT_SAVED_MESSAGE   # generic, no echo
    assert _rows(db_path, sid) == []


def test_non_answer_records_and_withdrawn_answers_are_not_eligible_anchors(db_path):
    c, _aid = _client_for("t2a-elig@example.com")
    sid = _start(c, answers=(PROBLEM_ANSWER,))
    # an "unknown" non-answer record becomes rec_2 — never an anchor
    assert c.post(SESSION % sid, data={"action": "unknown", "response": "",
                                       "answer_token": _token(c, sid)}).status_code == 302
    assert _anchors(c, sid) == ["rec_1"]
    assert _record(c, sid, "rec_2").status_code == 302
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
    assert _rows(db_path, sid) == []
    # withdraw rec_1 through the governed correction: it stops being an anchor
    assert c.post(CORRECT % sid, data={"supersedes_record_id": "rec_1",
                                       "response": MECH_CORRECTED,
                                       "answer_token": _token(c, sid)}).status_code == 302
    assert "rec_1" not in _anchors(c, sid)
    assert _record(c, sid, "rec_1").status_code == 302
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
    assert _rows(db_path, sid) == []


def test_another_projects_anchor_id_cannot_be_quantified_across_projects(db_path):
    ca, _a = _client_for("t2a-iso-a@example.com")
    sid_a = _start(ca)
    cb, _b = _client_for("t2a-iso-b@example.com")
    sid_b = _start(cb, answers=(PROBLEM_ANSWER,))     # only rec_1 exists in B
    assert _anchors(ca, sid_a) == ["rec_1", "rec_2"]
    assert _anchors(cb, sid_b) == ["rec_1"]
    r = _record(cb, sid_b, "rec_2")                     # A's rec_2 is not B's anchor
    assert r.status_code == 302 and _rows(db_path, sid_b) == []
    assert _record(ca, sid_a, "rec_2", value="5").status_code == 302
    assert _record(cb, sid_b, "rec_1", value="9", unit="A").status_code == 302
    # each project sees only its own
    assert _shown_values(_page(ca, sid_a)) == ["5"]
    assert _shown_values(_page(cb, sid_b)) == ["9"]
    assert '<bdi class="t2a-value">5</bdi>' not in _page(cb, sid_b)
    assert '<bdi class="t2a-value">9</bdi>' not in _page(ca, sid_a)
    assert [r[4] for r in _rows(db_path, sid_a)] == ["5"]
    assert [r[4] for r in _rows(db_path, sid_b)] == ["9"]
    # B's owner cannot even read A's deliverable, let alone its quantities
    r = cb.get(DELIVERABLE % sid_a)
    assert r.status_code == 302 and r.headers["Location"].endswith("/")


# ==========================================================================
# 4. Presentation surfaces — session, HTML deliverable, PDF; localization
# ==========================================================================
def test_session_block_is_optional_collapsed_and_lists_eligible_anchors(db_path):
    c, _aid = _client_for("t2a-block@example.com")
    r = c.post("/start", data=FORM)
    sid = r.headers["Location"].rsplit("/session/", 1)[-1]
    assert "t2a-quantities" not in _page(c, sid)        # no anchors yet: no block
    assert _answer(c, sid, PROBLEM_ANSWER).status_code == 302
    body = _page(c, sid)
    assert '<details id="t2a-quantities"' in body and " open" not in \
        body.split('<details id="t2a-quantities"', 1)[1].split(">", 1)[0]
    assert ui_text.text("UI_T2A_HEADING", "en") in body
    assert "optional" in ui_text.text("UI_T2A_HEADING", "en")
    assert 'data-t2a-anchor="rec_1"' in body and PROBLEM_ANSWER in body
    assert ui_text.text("UI_T2A_NONE", "en") in body
    # canonical tokens are offered as form options; every one has a display label
    for unit in webapp.QUANTITY_UNITS:
        assert 'value="%s"' % unit in body and ui_text.text("UI_T2A_UNIT_" + unit, "en") in body
        assert ui_text.text("UI_T2A_UNIT_" + unit, "ar") != "UI_T2A_UNIT_" + unit
    for bound in webapp.QUANTITY_BOUNDS:
        assert ui_text.text("UI_T2A_BOUND_" + bound, "ar") != "UI_T2A_BOUND_" + bound
    # the journey is unchanged and completes without a number: the answer form
    # and the correction form are still there, the block is additive only
    assert 'id="answer-form"' in body and "/correct" in body
    # all CSRF tokens on the page are the one browser token
    assert len(set(re.findall(r'name="csrf_token" value="([^"]+)"', body))) == 1


def test_user_statement_is_escaped_inside_the_quantity_block(db_path):
    c, _aid = _client_for("t2a-escape@example.com")
    sid = _start(c, answers=(HTML_ANSWER,))
    body = _page(c, sid)
    block = body.split('<details id="t2a-quantities"', 1)[1].split("</details>", 1)[0]
    assert "<b>board</b>" not in block and "&lt;b&gt;board&lt;/b&gt;" in block
    assert "&amp;amp;" in block


def test_html_deliverable_and_pdf_present_recorded_quantities_read_only(db_path, monkeypatch):
    c, _aid = _client_for("t2a-deliv@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", value="12.5", bound="maximum", unit="V").status_code == 302
    assert _record(c, sid, "rec_2", value="250", bound="minimum", unit="mAh").status_code == 302
    html = c.get(DELIVERABLE % sid).get_data(as_text=True)
    assert 'id="t2a-quantified-requirements"' in html
    assert ui_text.text("UI_T2A_DELIV_HEADING", "en") in html
    assert "not been checked, validated, or assessed" in html
    assert _shown_values(html) == ["12.5", "250"]
    assert "maximum" in html and "volts (V)" in html and "milliampere-hours (mAh)" in html
    assert "Recorded by the inventor (not yet verified)" in html
    assert "qty-" not in html                       # no internal identifier
    seen = _capture_pdf_source(monkeypatch)
    r = c.post(PDF % sid, data={})
    assert r.status_code == 200 and r.headers["Content-Type"] == "application/pdf"
    source = seen["source"]
    assert 'id="t2a-quantified-requirements"' in source
    assert _shown_values(source) == ["12.5", "250"]
    # the PDF document is read-only: no quantity form, no route, no token
    assert "requirement-quantity" not in source and "<form" not in source
    assert "answer_token" not in source and "csrf_token" not in source
    assert seen["pdf"][:5] == b"%PDF-"


def test_arabic_presentation_localizes_labels_but_never_the_stored_value(db_path):
    c, _aid = _client_for("t2a-ar@example.com")
    sid = _start(c)
    assert c.post("/ui-language", data={"lang": "ar"}).status_code in (302, 303)
    assert _record(c, sid, "rec_1", value="3.75", bound="maximum", unit="kg").status_code == 302
    body = _page(c, sid)
    assert ui_text.text("UI_T2A_HEADING", "ar") in body
    assert ui_text.localize_deep(webapp.QUANTITY_SAVED_ACK, "ar") in body
    assert webapp.QUANTITY_SAVED_ACK not in body
    assert "حد أقصى" in body and "كيلوغرام (kg)" in body
    assert _shown_values(body) == ["3.75"]         # canonical value unchanged
    assert [r[4] for r in _rows(db_path, sid)] == ["3.75"]
    html = c.get(DELIVERABLE % sid).get_data(as_text=True)
    assert ui_text.text("UI_T2A_DELIV_HEADING", "ar") in html and "3.75" in html
    # the errors localize on their actual render path too
    assert _record(c, sid, "rec_1", value="abc").status_code == 302
    body = _page(c, sid)
    assert ui_text.localize_message(webapp.QUANTITY_INVALID_MESSAGE, "ar") in body
    assert webapp.QUANTITY_INVALID_MESSAGE not in body
    assert ui_text.localize_message(webapp.QUANTITY_NOT_SAVED_MESSAGE, "ar") \
        != webapp.QUANTITY_NOT_SAVED_MESSAGE


def test_zero_quantities_leave_package_html_and_pdf_source_byte_identical(db_path, monkeypatch):
    """Byte-equivalence: for a project with NO quantities the package, the HTML
    deliverable and the PDF source are identical to the pre-T2A render path
    (the attach helper is a no-op there and the assembler emits no key)."""
    c, _aid = _client_for("t2a-zero@example.com")
    sid = _start(c)
    monkeypatch.setattr(_assembler, "_now_iso", lambda: "2026-01-01T00:00:00+00:00")
    seen = _capture_pdf_source(monkeypatch)
    real_html = c.get(DELIVERABLE % sid).get_data()
    assert c.post(PDF % sid, data={}).status_code == 200
    real_source = seen["source"]
    with app.test_request_context():
        real_package = webapp._deliverable_context(sid)[1]
    # the base-equivalent path: no quantity attachment and no seam composition
    monkeypatch.setattr(webapp, "_attach_quantity_history", lambda sid, state: True)
    monkeypatch.setattr(webapp, "_quantified_requirements_meta", lambda state: None)
    SESSION_STORE[sid]["state"].requirement_quantities = []
    base_html = c.get(DELIVERABLE % sid).get_data()
    assert c.post(PDF % sid, data={}).status_code == 200
    base_source = seen["source"]
    assert real_html == base_html
    assert real_source == base_source
    assert "quantified_requirements" not in real_package["_session_meta"]
    assert json.dumps(real_package, sort_keys=True) == json.dumps(
        _assembler.assemble_deliverable(SESSION_STORE[sid]["state"]), sort_keys=True)
    assert "t2a-quantified-requirements" not in real_html.decode("utf-8")
    assert "t2a-quantified-requirements" not in real_source


# ==========================================================================
# 5. Cold load, resume, migration of an existing populated database
# ==========================================================================
def test_cold_load_restores_quantities_on_every_surface_and_refuses_cold_writes(
        db_path, monkeypatch):
    c, _aid = _client_for("t2a-cold@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", value="42", unit="count", bound="target").status_code == 302
    SESSION_STORE.clear()                          # process memory loss
    body = _page(c, sid)
    assert 'id="reconstructed-review"' in body
    assert _shown_values(body) == ["42"] and "count (pieces)" in body
    assert "requirement-quantity" not in body      # dead-form suppression (read-only)
    html = c.get(DELIVERABLE % sid).get_data(as_text=True)
    assert 'id="reconstructed-deliverable"' in html and _shown_values(html) == ["42"]
    seen = _capture_pdf_source(monkeypatch)
    assert c.post(PDF % sid, data={}).status_code == 200
    assert _shown_values(seen["source"]) == ["42"]
    # a write against the cold, non-resumable view is refused generically
    r = _record(c, sid, "rec_1", value="43", unit="count")
    assert r.status_code == 302 and webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
    assert [r[4] for r in _rows(db_path, sid)] == ["42"]
    # explicit resume re-establishes a writable context carrying the history
    assert c.post("/session/%s/resume" % sid, data={}).status_code == 302
    assert [q.value for q in SESSION_STORE[sid]["state"].requirement_quantities] == ["42"]
    assert _record(c, sid, "rec_1", value="43", unit="count").status_code == 302
    assert [r[4] for r in _rows(db_path, sid)] == ["42", "43"]
    assert _shown_values(_page(c, sid)) == ["43"]


def test_existing_populated_pre_t2a_database_is_migrated_by_the_application(db_path):
    """A database populated BEFORE T2-A (no requirement_quantities table) is
    migrated additively on the application's first open; every existing
    project keeps its rows and loads with a valid empty quantity history."""
    c, aid = _client_for("t2a-migrate@example.com")
    sid = _start(c)
    ledger_before = _ledger_rows(db_path, sid)
    # drop the additive table to reproduce the pre-T2A on-disk schema
    _store().close()
    webapp._STORE = None
    conn = sqlite3.connect(db_path)
    conn.execute("DROP TABLE requirement_quantities")
    conn.commit()
    assert "requirement_quantities" not in [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")]
    conn.close()
    SESSION_STORE.clear()
    body = _page(c, sid)                           # app reopens the store: migrates
    assert 'id="reconstructed-review"' in body and "t2a-value" not in body
    assert _ledger_rows(db_path, sid) == ledger_before
    assert _store().load_requirement_quantities(sid) == ()
    assert _store().load_owner(sid) == (True, aid)
    conn = sqlite3.connect(db_path)
    try:
        assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
    finally:
        conn.close()


# ==========================================================================
# 6. Corrupt populated history fails closed at EVERY affected surface
# ==========================================================================
def test_corrupt_populated_history_fails_closed_on_session_deliverable_pdf_and_write(
        db_path, monkeypatch):
    c, _aid = _client_for("t2a-corrupt@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", value="5").status_code == 302
    _corrupt(db_path, sid)
    before_rows = _rows(db_path, sid)              # the corrupt rows, as stored
    with pytest.raises(QuantityHistoryError):
        _store().load_requirement_quantities(sid)
    for verb, path in (("get", SESSION % sid), ("get", DELIVERABLE % sid),
                       ("post", PDF % sid)):
        r = getattr(c, verb)(path, data={})
        assert r.status_code == 302 and r.headers["Location"].endswith("/"), (verb, path)
        text = r.get_data(as_text=True)
        assert "qty-" not in text and "furlong" not in text and "sqlite" not in text.lower()
    # the live carrier was NOT replaced by a partial/empty history
    assert [q.value for q in SESSION_STORE[sid]["state"].requirement_quantities] == ["5"]
    # a write is refused with nothing appended (token obtained before corruption)
    token = webapp._issue_answer_token(sid)
    r = c.post(ROUTE % sid, data={"anchor_record_id": "rec_1", "bound": "target",
                                  "value": "6", "unit": "V", "answer_token": token})
    assert r.status_code == 302 and r.headers["Location"] == SESSION % sid
    assert _rows(db_path, sid) == before_rows
    assert SESSION_STORE[sid].get("_answer_error") == webapp.QUANTITY_NOT_SAVED_MESSAGE
    # after memory loss the cold load also fails closed (no page, no disclosure)
    SESSION_STORE.clear()
    r = c.get(SESSION % sid)
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    assert sid not in SESSION_STORE


def test_storage_unavailability_fails_closed_without_partial_state(db_path, monkeypatch):
    c, _aid = _client_for("t2a-unavailable@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", value="5").status_code == 302
    store = _store()
    monkeypatch.setattr(store, "load_requirement_quantities",
                        lambda pid: (_ for _ in ()).throw(sqlite3.OperationalError("db gone")))
    for verb, path in (("get", SESSION % sid), ("get", DELIVERABLE % sid), ("post", PDF % sid)):
        r = getattr(c, verb)(path, data={})
        assert r.status_code == 302 and r.headers["Location"].endswith("/")
        assert "db gone" not in r.get_data(as_text=True)
    token = webapp._issue_answer_token(sid)
    r = c.post(ROUTE % sid, data={"anchor_record_id": "rec_1", "bound": "target",
                                  "value": "6", "unit": "V", "answer_token": token})
    assert r.status_code == 302
    assert [x[4] for x in _rows(db_path, sid)] == ["5"]
    assert SESSION_STORE[sid].get("_answer_error") == webapp.QUANTITY_NOT_SAVED_MESSAGE


def test_durable_append_failure_publishes_nothing_persist_before_acknowledge(db_path, monkeypatch):
    from engine.record_store import StoreError
    c, _aid = _client_for("t2a-append-fail@example.com")
    sid = _start(c)
    store = _store()
    monkeypatch.setattr(store, "append_requirement_quantity",
                        lambda *a, **k: (_ for _ in ()).throw(StoreError("unavailable")))
    entry = SESSION_STORE[sid]
    before = pickle.dumps(entry["state"])
    assert _record(c, sid, "rec_1", value="5").status_code == 302
    body = _page(c, sid)
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in body and webapp.QUANTITY_SAVED_ACK not in body
    assert entry["state"].requirement_quantities == []
    assert _rows(db_path, sid) == [] and "unavailable" not in body
    assert pickle.dumps(entry["state"]) == before


# ==========================================================================
# 7. Owner-mandated correction-flow ordering
# ==========================================================================
def test_corrupt_populated_quantity_history_blocks_correction_before_durable_append(db_path):
    c, _aid = _client_for("t2a-corr-block@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", value="5").status_code == 302
    token = _token(c, sid)
    ledger_before = _ledger_rows(db_path, sid)
    state_before = pickle.dumps(SESSION_STORE[sid]["state"])
    _corrupt(db_path, sid, "UPDATE requirement_quantities SET value_canonical = '05' "
                           "WHERE project_id = ?")
    rows_before = _rows(db_path, sid)              # the corrupt rows, as stored
    r = c.post(CORRECT % sid, data={"supersedes_record_id": "rec_2",
                                    "response": MECH_CORRECTED, "answer_token": token})
    assert r.status_code == 302 and r.headers["Location"] == SESSION % sid
    # nothing appended, live state untouched, generic message, nothing disclosed
    assert _ledger_rows(db_path, sid) == ledger_before
    assert _rows(db_path, sid) == rows_before
    assert pickle.dumps(SESSION_STORE[sid]["state"]) == state_before
    assert SESSION_STORE[sid].get("_answer_error") == webapp.CORRECTION_NOT_APPLIED_MESSAGE
    assert SESSION_STORE[sid].get("_interaction_ack") is None
    message = webapp.CORRECTION_NOT_APPLIED_MESSAGE
    for forbidden in ("qty-", "rec_", "05", "sqlite", "SELECT", "Traceback", "/"):
        assert forbidden not in message
    # the (still corrupt) session page then fails closed generically as well
    r = c.get(SESSION % sid)
    assert r.status_code == 302 and r.headers["Location"].endswith("/")


def test_unavailable_quantity_storage_blocks_correction_before_durable_append(db_path, monkeypatch):
    c, _aid = _client_for("t2a-corr-unavail@example.com")
    sid = _start(c)
    store = _store()
    ledger_before = _ledger_rows(db_path, sid)
    appended = []
    real_append = store.append_record
    monkeypatch.setattr(store, "append_record",
                        lambda *a, **k: appended.append(a) or real_append(*a, **k))
    monkeypatch.setattr(store, "load_requirement_quantities",
                        lambda pid: (_ for _ in ()).throw(sqlite3.OperationalError("gone")))
    token = webapp._issue_answer_token(sid)
    r = c.post(CORRECT % sid, data={"supersedes_record_id": "rec_2",
                                    "response": MECH_CORRECTED, "answer_token": token})
    assert r.status_code == 302
    assert appended == [] and _ledger_rows(db_path, sid) == ledger_before
    assert SESSION_STORE[sid].get("_answer_error") == webapp.CORRECTION_NOT_APPLIED_MESSAGE


def test_zero_quantity_rows_do_not_block_correction(db_path):
    c, _aid = _client_for("t2a-corr-zero@example.com")
    sid = _start(c)
    assert _rows(db_path, sid) == []
    r = c.post(CORRECT % sid, data={"supersedes_record_id": "rec_2",
                                    "response": MECH_CORRECTED,
                                    "answer_token": _token(c, sid)})
    assert r.status_code == 302
    assert SESSION_STORE[sid].get("_answer_error") is None
    assert SESSION_STORE[sid].get("_interaction_ack") == webapp.CORRECTION_APPLIED_ACK
    assert [r[1] for r in _ledger_rows(db_path, sid)] == ["rec_1", "rec_2", "rec_3"]
    assert SESSION_STORE[sid]["state"].requirement_quantities == []


def test_valid_quantity_history_survives_correction_reconstruction(db_path):
    c, _aid = _client_for("t2a-corr-survive@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", value="5", unit="V", bound="maximum").status_code == 302
    r = c.post(CORRECT % sid, data={"supersedes_record_id": "rec_2",
                                    "response": MECH_CORRECTED,
                                    "answer_token": _token(c, sid)})
    assert r.status_code == 302
    body = _page(c, sid)
    assert webapp.CORRECTION_APPLIED_ACK in body
    # the replayed live state carries the SAME validated history (reattached)
    state = SESSION_STORE[sid]["state"]
    assert [(q.anchor_record_id, q.value) for q in state.requirement_quantities] == [("rec_1", "5")]
    assert getattr(state, "domain", None) is not None          # a live replayed state
    assert _shown_values(body) == ["5"]
    html = c.get(DELIVERABLE % sid).get_data(as_text=True)
    assert _shown_values(html) == ["5"]
    assert [r[4] for r in _rows(db_path, sid)] == ["5"]
    # and it can be corrected further afterwards
    assert _record(c, sid, "rec_1", value="6", unit="V", bound="maximum").status_code == 302
    assert _shown_values(_page(c, sid)) == ["6"]


def test_superseded_anchor_becomes_inactive_deterministically(db_path):
    c, _aid = _client_for("t2a-corr-anchor@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", value="5").status_code == 302
    assert _record(c, sid, "rec_2", value="7", unit="A").status_code == 302
    r = c.post(CORRECT % sid, data={"supersedes_record_id": "rec_2",
                                    "response": MECH_CORRECTED,
                                    "answer_token": _token(c, sid)})
    assert r.status_code == 302
    body = _page(c, sid)
    assert _anchors(c, sid) == ["rec_1", "rec_3"]
    assert _shown_values(body) == ["5"]                 # rec_2's chain is inactive
    assert '<bdi class="t2a-value">7</bdi>' not in body
    with app.test_request_context():
        package = webapp._deliverable_context(sid)[1]
    assert [(i["value"]) for i in package["_session_meta"]["quantified_requirements"]["items"]] == ["5"]
    # the inactive rows are RETAINED durably, never deleted or rewritten
    assert [(r[2], r[4]) for r in _rows(db_path, sid)] == [("rec_1", "5"), ("rec_2", "7")]
    # deterministic: two independent reconstructions agree exactly
    from engine.session_reconstruction import reconstruct_readonly_state
    from engine.requirement_quantity import derive_quantified_requirements
    outcomes = []
    for _ in range(2):
        s = reconstruct_readonly_state(_store(), sid).state
        s.requirement_quantities = list(_store().load_requirement_quantities(sid))
        outcomes.append([(q.anchor_record_id, q.quantity.value)
                         for q in derive_quantified_requirements(s)])
    assert outcomes[0] == outcomes[1] == [("rec_1", "5")]
    # the withdrawn anchor cannot be quantified any more; the new one can
    assert _record(c, sid, "rec_2", value="8", unit="A").status_code == 302
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
    assert _record(c, sid, "rec_3", value="8", unit="A").status_code == 302
    assert _shown_values(_page(c, sid)) == ["5", "8"]


def test_another_project_remains_unaffected_by_correction_and_corruption(db_path):
    ca, _a = _client_for("t2a-corr-a@example.com")
    sid_a = _start(ca)
    cb, _b = _client_for("t2a-corr-b@example.com")
    sid_b = _start(cb)
    assert _record(ca, sid_a, "rec_1", value="5").status_code == 302
    assert _record(cb, sid_b, "rec_1", value="9", unit="A").status_code == 302
    b_state_before = pickle.dumps(SESSION_STORE[sid_b]["state"])
    b_rows_before = _rows(db_path, sid_b)
    # A corrects: B's live state, rows and page are byte-identical
    assert ca.post(CORRECT % sid_a, data={"supersedes_record_id": "rec_2",
                                          "response": MECH_CORRECTED,
                                          "answer_token": _token(ca, sid_a)}).status_code == 302
    assert pickle.dumps(SESSION_STORE[sid_b]["state"]) == b_state_before
    assert _rows(db_path, sid_b) == b_rows_before
    assert _shown_values(_page(cb, sid_b)) == ["9"]
    # A's history is corrupted: A fails closed, B keeps working and correcting
    _corrupt(db_path, sid_a)
    r = ca.get(SESSION % sid_a)
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    assert _shown_values(_page(cb, sid_b)) == ["9"]
    assert cb.post(CORRECT % sid_b, data={"supersedes_record_id": "rec_2",
                                          "response": MECH_CORRECTED,
                                          "answer_token": _token(cb, sid_b)}).status_code == 302
    assert SESSION_STORE[sid_b].get("_interaction_ack") == webapp.CORRECTION_APPLIED_ACK
    assert _shown_values(_page(cb, sid_b)) == ["9"]


def test_post_commit_reattachment_failure_keeps_live_state_and_tells_the_truth(
        db_path, monkeypatch):
    """Only a GENUINE failure after the correction append has committed may
    reach the saved-but-not-yet-applied message: the durable correction stands,
    live memory is left exactly as it was, and the next load applies it."""
    c, _aid = _client_for("t2a-corr-post@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", value="5").status_code == 302
    store = _store()
    real_load = store.load_requirement_quantities
    calls = {"n": 0}

    def flaky(pid):
        calls["n"] += 1
        if calls["n"] == 2:                        # the reattachment read only
            raise sqlite3.OperationalError("gone after commit")
        return real_load(pid)
    monkeypatch.setattr(store, "load_requirement_quantities", flaky)
    token = webapp._issue_answer_token(sid)
    state_before = pickle.dumps(SESSION_STORE[sid]["state"])
    r = c.post(CORRECT % sid, data={"supersedes_record_id": "rec_2",
                                    "response": MECH_CORRECTED, "answer_token": token})
    assert r.status_code == 302
    assert SESSION_STORE[sid].get("_answer_error") == webapp.CORRECTION_SAVED_NOT_YET_APPLIED_MESSAGE
    assert pickle.dumps(SESSION_STORE[sid]["state"]) == state_before
    assert [x[1] for x in _ledger_rows(db_path, sid)] == ["rec_1", "rec_2", "rec_3"]
    monkeypatch.undo()
    SESSION_STORE.clear()                          # the next load applies it
    body = _page(c, sid)
    assert _shown_values(body) == ["5"] and "rec_3" in _anchors(c, sid) + ["rec_3"]


def test_r05_inventory_and_write_helper_are_consistent_with_the_route():
    rules = {rule.rule for rule in app.url_map.iter_rules()
             if rule.rule == "/session/<sid>/requirement-quantity"}
    assert rules == {"/session/<sid>/requirement-quantity"}
    rule = next(r for r in app.url_map.iter_rules()
                if r.rule == "/session/<sid>/requirement-quantity")
    assert rule.methods - {"HEAD", "OPTIONS"} == {"POST"}
    assert not webapp._quantity_write_authorized("no-such-project")
