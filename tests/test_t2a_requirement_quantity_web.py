"""T2-A Quantified Requirements Slice 1 — web-layer proof (two-stage flow).

File: tests/test_t2a_requirement_quantity_web.py
Purpose: behaviour tests for the two security-sensitive POST routes
(`/session/<sid>/quantity/propose` and `/session/<sid>/quantity/confirm`):
propose performs no durable write; the confirm form carries only
csrf_token, confirmation_token and quantity_action; exact confirmation
succeeds once; replay, altered content, expiry, tampering, cross-session,
cross-project and cross-owner tokens cannot write; anonymous, NULL-owner,
unverified, inactive and non-owner denial; stale anchor and stale quantity
head between propose and confirm; corrupt history detected inside the
transaction; correction/supersession history; replaced-value and
withdrawn-anchor rendering on the session page, the HTML deliverable and the
PDF source; Arabic/English chrome parity with never-localized value text;
zero-row package / HTML / PDF-source equivalence; the Owner-mandated
correction-flow ordering; and no API / export / adapter change.

Real Flask application, real on-disk SQLite (autouse conftest isolation),
real account + record stores, real signed sessions, real WeasyPrint for the
PDF proofs. Security boundaries are never mocked; monkeypatching is used only
to inject storage failures, to drive the clock, or to capture the exact
document handed to the renderer.
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
from engine.requirement_quantity import (
    QUANTITY_KINDS, QuantityHistoryError, MAX_REQUIREMENT_QUANTITIES_PER_PROJECT,
)

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
KIND = QUANTITY_KINDS[0]
KIND2 = QUANTITY_KINDS[1]

PROPOSE = "/session/%s/quantity/propose"
CONFIRM = "/session/%s/quantity/confirm"
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


def _ctoken(body):
    m = re.search(r'name="confirmation_token" value="([^"]+)"', body)
    return m.group(1) if m else None


def _answer(client, sid, text):
    return client.post(SESSION % sid, data={
        "response": text, "action": "answered", "answer_token": _token(client, sid)})


def _anchors(client, sid):
    return re.findall(r'data-t2a-anchor="([^"]+)"', _page(client, sid))


def _propose(client, sid, anchor, value_text="12.5 V", kind=KIND, **extra):
    data = {"anchor_record_id": anchor, "quantity_kind": kind, "value_text": value_text}
    data.update(extra)
    return client.post(PROPOSE % sid, data=data)


def _confirm(client, sid, token, action="confirm", **extra):
    data = {"confirmation_token": token, "quantity_action": action}
    data.update(extra)
    return client.post(CONFIRM % sid, data=data)


def _record(client, sid, anchor, value_text="12.5 V", kind=KIND):
    """Full two-stage journey: propose, read the token, confirm exactly."""
    r = _propose(client, sid, anchor, value_text, kind)
    assert r.status_code == 302, r.status_code
    token = _ctoken(_page(client, sid))
    assert token, "no confirmation token was rendered"
    return _confirm(client, sid, token)


def _store():
    return webapp._get_store()


def _rows(db_path, sid):
    conn = sqlite3.connect(db_path)
    try:
        return conn.execute(
            "SELECT quantity_seq, quantity_id, anchor_record_id, requirement_id, quantity_kind, "
            "value_text, supersedes_quantity_id, event_key FROM requirement_quantities "
            "WHERE project_id = ? ORDER BY quantity_seq", (sid,)).fetchall()
    finally:
        conn.close()


def _ledger_rows(db_path, sid):
    conn = sqlite3.connect(db_path)
    try:
        return conn.execute("SELECT seq, record_id, payload FROM records WHERE project_id = ? "
                            "ORDER BY seq", (sid,)).fetchall()
    finally:
        conn.close()


def _corrupt(db_path, sid, sql="UPDATE requirement_quantities SET quantity_kind = 'bogus' "
                                "WHERE project_id = ?"):
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(sql, (sid,))
        conn.commit()
    finally:
        conn.close()


def _values(body):
    return re.findall(r'<bdi class="t2a-value" dir="auto">([^<]*)</bdi>', body)


def _replaced(body):
    return re.findall(r'<bdi class="t2a-replaced-value" dir="auto">([^<]*)</bdi>', body)


def _withdrawn(body):
    return re.findall(r'<bdi class="t2a-withdrawn-value" dir="auto">([^<]*)</bdi>', body)


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
# 1. Routes, CSRF integrity, no durable write on propose
# ==========================================================================
def test_both_routes_are_post_only_and_csrf_guarded_before_any_state(db_path):
    c, _aid = _client_for("t2a-csrf@example.com")
    sid = _start(c)
    for path in (PROPOSE % sid, CONFIRM % sid):
        assert c.get(path).status_code == 405
    before = _snapshot(sid, db_path)
    raw = app.test_client()                      # no CSRF evidence at all
    with raw.session_transaction() as s, c.session_transaction() as mine:
        s.update(copy.deepcopy(dict(mine)))
    r = raw.post(PROPOSE % sid, data={"anchor_record_id": "rec_1", "quantity_kind": KIND,
                                      "value_text": "1 V"})
    assert r.status_code == 403
    r = raw.post(CONFIRM % sid, data={"confirmation_token": "x.y", "quantity_action": "confirm"})
    assert r.status_code == 403
    assert _rows(db_path, sid) == [] and _snapshot(sid, db_path)[1] == before[1]
    assert "quantity_proposal" not in SESSION_STORE[sid]


def test_propose_stages_one_bounded_proposal_and_performs_no_durable_write(db_path):
    c, _aid = _client_for("t2a-propose@example.com")
    sid = _start(c)
    db_before = _snapshot(sid, db_path)[1]
    r = _propose(c, sid, "rec_1", "  12.5   V ", KIND)
    assert r.status_code == 302 and r.headers["Location"].endswith("#t2a-confirm")
    assert _rows(db_path, sid) == [] and _snapshot(sid, db_path)[1] == db_before
    staged = SESSION_STORE[sid]["quantity_proposal"]
    assert staged["anchor_record_id"] == "rec_1"
    assert staged["requirement_id"] == "req:assertion:rec_1"
    assert staged["quantity_kind"] == KIND and staged["value_text"] == "12.5 V"
    assert staged["supersedes_quantity_id"] is None and len(staged["event_key"]) == 32
    body = _page(c, sid)
    assert 'id="t2a-confirm"' in body and _ctoken(body)
    assert '<bdi class="t2a-proposed" dir="auto">12.5 V</bdi>' in body
    # a second proposal replaces the first (one bounded proposal per session)
    assert _propose(c, sid, "rec_2", "3 A", KIND2).status_code == 302
    assert SESSION_STORE[sid]["quantity_proposal"]["anchor_record_id"] == "rec_2"
    assert _rows(db_path, sid) == []


def test_confirm_form_carries_only_the_three_fields_and_no_material_data(db_path):
    c, _aid = _client_for("t2a-form@example.com")
    sid = _start(c)
    assert _propose(c, sid, "rec_1", "12.5 V").status_code == 302
    body = _page(c, sid)
    form = re.search(r'<form method="POST" action="/session/[^"]+/quantity/confirm"(.*?)</form>',
                     body, re.S).group(1)
    names = set(re.findall(r'name="([^"]+)"', form))
    assert names == {"csrf_token", "confirmation_token", "quantity_action"}
    assert "rec_1" not in form and "12.5 V" not in form and "anchor_record_id" not in form
    assert 'value="confirm"' in form and 'value="discard"' in form


# ==========================================================================
# 2. Exact confirmation once; replay; altered content; discard
# ==========================================================================
def test_exact_confirmation_succeeds_once_and_replay_cannot_write_twice(db_path):
    c, _aid = _client_for("t2a-once@example.com")
    sid = _start(c)
    assert _propose(c, sid, "rec_1", "7 V").status_code == 302
    token = _ctoken(_page(c, sid))
    r = _confirm(c, sid, token)
    assert r.status_code == 302 and r.headers["Location"] == SESSION % sid
    body = _page(c, sid)
    assert webapp.QUANTITY_SAVED_ACK in body and _values(body) == ["7 V"]
    rows = _rows(db_path, sid)
    assert [(x[2], x[3], x[4], x[5], x[6]) for x in rows] == [
        ("rec_1", "req:assertion:rec_1", KIND, "7 V", None)]
    assert "quantity_proposal" not in SESSION_STORE[sid]
    for _ in range(3):                                   # replay of the spent token
        assert _confirm(c, sid, token).status_code == 302
        body = _page(c, sid)
        assert webapp.QUANTITY_NOT_SAVED_MESSAGE in body and webapp.QUANTITY_SAVED_ACK not in body
    assert _rows(db_path, sid) == rows
    assert [q.value_text for q in SESSION_STORE[sid]["state"].requirement_quantities] == ["7 V"]


def test_same_token_with_altered_action_or_content_cannot_write(db_path):
    c, _aid = _client_for("t2a-altered@example.com")
    sid = _start(c)
    assert _propose(c, sid, "rec_1", "7 V").status_code == 302
    token = _ctoken(_page(c, sid))
    # altered content (extra material fields) is refused outright
    for extra in ({"value_text": "999 V"}, {"anchor_record_id": "rec_2"},
                  {"quantity_kind": KIND2}, {"answer_token": "x"}):
        assert _confirm(c, sid, token, **extra).status_code == 302
        assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
        assert _rows(db_path, sid) == []
    # an unknown action consumes the token and writes nothing
    assert _confirm(c, sid, token, action="apply").status_code == 302
    assert _rows(db_path, sid) == [] and "quantity_proposal" not in SESSION_STORE[sid]
    assert _confirm(c, sid, token).status_code == 302   # spent
    assert _rows(db_path, sid) == []
    # a duplicated field is refused too
    from werkzeug.datastructures import MultiDict
    assert _propose(c, sid, "rec_1", "7 V").status_code == 302
    token = _ctoken(_page(c, sid))
    r = c.post(CONFIRM % sid, data=MultiDict([("confirmation_token", token),
                                              ("quantity_action", "confirm"),
                                              ("quantity_action", "confirm")]))
    assert r.status_code == 302 and _rows(db_path, sid) == []


def test_discard_consumes_the_proposal_and_saves_nothing(db_path):
    c, _aid = _client_for("t2a-discard@example.com")
    sid = _start(c)
    assert _propose(c, sid, "rec_1", "7 V").status_code == 302
    token = _ctoken(_page(c, sid))
    assert _confirm(c, sid, token, action="discard").status_code == 302
    body = _page(c, sid)
    assert webapp.QUANTITY_DISCARDED_ACK in body and 'id="t2a-confirm"' not in body
    assert _rows(db_path, sid) == []
    assert _confirm(c, sid, token).status_code == 302   # cannot confirm afterwards
    assert _rows(db_path, sid) == []


def test_exact_replay_of_the_same_event_is_idempotent_through_the_event_key(db_path, monkeypatch):
    c, _aid = _client_for("t2a-event@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "7 V").status_code == 302
    rows = _rows(db_path, sid)
    # simulate a repeated durable attempt of the identical event: the UNIQUE
    # event key raises and confirm-by-reload recognises the same event
    store = _store()
    real_append = store.append_requirement_quantity
    calls = []

    def tracking(pid, q):
        calls.append(q.event_key)
        return real_append(pid, q)
    monkeypatch.setattr(store, "append_requirement_quantity", tracking)
    entry = SESSION_STORE[sid]
    entry["quantity_proposal"] = {
        "nonce": "n", "issued_at": webapp._quantity_clock(),
        "expires_at": webapp._quantity_clock() + 60, "account_id": _aid,
        "anchor_record_id": "rec_1", "requirement_id": "req:assertion:rec_1",
        "quantity_kind": KIND, "value_text": "7 V", "supersedes_quantity_id": None,
        "event_key": rows[0][7]}
    token = webapp._quantity_confirmation_token(sid, entry["quantity_proposal"])
    assert _confirm(c, sid, token).status_code == 302
    assert calls == [rows[0][7]]
    assert webapp.QUANTITY_SAVED_ACK in _page(c, sid)       # idempotent no-op
    assert _rows(db_path, sid) == rows


# ==========================================================================
# 3. Token binding: expiry, tampering, cross-session/project/owner
# ==========================================================================
def test_expired_token_is_refused_and_the_proposal_dropped(db_path, monkeypatch):
    c, _aid = _client_for("t2a-expiry@example.com")
    sid = _start(c)
    base = webapp._quantity_clock()
    monkeypatch.setattr(webapp, "_quantity_clock", lambda: base)
    assert _propose(c, sid, "rec_1", "7 V").status_code == 302
    token = _ctoken(_page(c, sid))
    assert token
    monkeypatch.setattr(webapp, "_quantity_clock",
                        lambda: base + webapp.QUANTITY_CONFIRMATION_TTL_SECONDS)
    assert 'id="t2a-confirm"' not in _page(c, sid)           # dropped at render
    assert _confirm(c, sid, token).status_code == 302
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
    assert _rows(db_path, sid) == []
    # a fresh proposal confirmed just BEFORE expiry still works
    monkeypatch.setattr(webapp, "_quantity_clock", lambda: base)
    assert _propose(c, sid, "rec_1", "7 V").status_code == 302
    token = _ctoken(_page(c, sid))
    monkeypatch.setattr(webapp, "_quantity_clock",
                        lambda: base + webapp.QUANTITY_CONFIRMATION_TTL_SECONDS - 1)
    assert _confirm(c, sid, token).status_code == 302
    assert _values(_page(c, sid)) == ["7 V"]


@pytest.mark.parametrize("mutate", [
    lambda t: "", lambda t: "forged.token", lambda t: t.split(".")[0],
    lambda t: t.split(".")[0] + ".", lambda t: "." + t.split(".")[1],
    lambda t: t[:-1] + ("0" if t[-1] != "0" else "1"),
    lambda t: "x" + t[1:], lambda t: t + "0", lambda t: t.upper(),
])
def test_tampered_or_missing_token_is_refused_generically(db_path, mutate):
    c, _aid = _client_for("t2a-tamper@example.com")
    sid = _start(c)
    assert _propose(c, sid, "rec_1", "7 V").status_code == 302
    token = _ctoken(_page(c, sid))
    bad = mutate(token)
    if bad == token:
        pytest.skip("mutation produced the same token")
    assert _confirm(c, sid, bad).status_code == 302
    body = _page(c, sid)
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in body
    assert token not in body                                  # consumed, never re-shown
    assert _rows(db_path, sid) == []


def test_cross_session_cross_project_and_cross_owner_tokens_are_refused(db_path):
    ca, aid_a = _client_for("t2a-x-a@example.com")
    sid_a = _start(ca)
    sid_a2 = _start(ca)
    cb, aid_b = _client_for("t2a-x-b@example.com")
    sid_b = _start(cb)
    # token minted for project A2 is not accepted on project A (cross-project)
    assert _propose(ca, sid_a2, "rec_1", "7 V").status_code == 302
    tok_a2 = _ctoken(_page(ca, sid_a2))
    assert _propose(ca, sid_a, "rec_1", "7 V").status_code == 302
    assert _confirm(ca, sid_a, tok_a2).status_code == 302
    assert _rows(db_path, sid_a) == [] and _rows(db_path, sid_a2) == []
    # cross-owner: B presents A's valid token on A's project → generic denial
    assert _propose(ca, sid_a, "rec_1", "7 V").status_code == 302
    tok_a = _ctoken(_page(ca, sid_a))
    r = _confirm(cb, sid_a, tok_a)
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    assert _rows(db_path, sid_a) == []
    # cross-session: a different browser of the SAME owner (no staged
    # proposal in that entry? the entry is per project, so simulate by
    # re-staging under B's own project and presenting A's token there)
    assert _propose(cb, sid_b, "rec_1", "9 A", KIND2).status_code == 302
    assert _confirm(cb, sid_b, tok_a).status_code == 302
    assert _rows(db_path, sid_b) == []
    # a token staged under A but whose staged owner is forged to B fails the
    # owner binding even when presented by B
    SESSION_STORE[sid_a]["quantity_proposal"]["account_id"] = aid_b
    forged = webapp._quantity_confirmation_token(sid_a, SESSION_STORE[sid_a]["quantity_proposal"])
    r = _confirm(cb, sid_a, forged)
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    assert _rows(db_path, sid_a) == []


# ==========================================================================
# 4. Authorization matrix
# ==========================================================================
def test_write_authorization_matrix_on_both_routes(db_path):
    owner, aid = _client_for("t2a-owner@example.com")
    sid = _start(owner)
    assert _propose(owner, sid, "rec_1", "7 V").status_code == 302
    token = _ctoken(_page(owner, sid))
    anon = _new_client()
    other, _o = _client_for("t2a-other@example.com")
    for client in (anon, other):
        for path, data in ((PROPOSE % sid, {"anchor_record_id": "rec_1", "quantity_kind": KIND,
                                            "value_text": "1 V"}),
                           (CONFIRM % sid, {"confirmation_token": token,
                                            "quantity_action": "confirm"})):
            r = client.post(path, data=data)
            assert r.status_code == 302 and r.headers["Location"].endswith("/"), path
    missing = other.post(PROPOSE % "no-such-project", data={})
    assert (missing.status_code, missing.headers["Location"]) == (302, r.headers["Location"])
    assert _rows(db_path, sid) == []
    # the owner's exact confirmation is accepted
    assert _confirm(owner, sid, token).status_code == 302
    assert [x[5] for x in _rows(db_path, sid)] == ["7 V"]
    # disabled owner: both routes denied generically, nothing written
    assert _propose(owner, sid, "rec_1", "8 V").status_code == 302
    token = _ctoken(_page(owner, sid))
    webapp._get_account_store().set_status(aid, "disabled", "2026-01-01T00:00:00.000000Z")
    for path, data in ((PROPOSE % sid, {"anchor_record_id": "rec_1", "quantity_kind": KIND,
                                        "value_text": "9 V"}),
                       (CONFIRM % sid, {"confirmation_token": token, "quantity_action": "confirm"})):
        r = owner.post(path, data=data)
        assert r.status_code == 302 and r.headers["Location"].endswith("/")
    assert len(_rows(db_path, sid)) == 1


def test_null_owner_anonymous_and_unverified_projects_can_never_be_quantified(db_path):
    anon = _new_client()
    sid = _start(anon)
    assert "t2a-quantities" not in _page(anon, sid) and "quantity/propose" not in _page(anon, sid)
    r = anon.post(PROPOSE % sid, data={"anchor_record_id": "rec_1", "quantity_kind": KIND,
                                       "value_text": "1 V"})
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    unv, _u = _client_for("t2a-unverified@example.com", verified=False)
    sid_u = _start(unv)
    assert _store().load_owner(sid_u) == (True, None)
    assert "quantity/propose" not in _page(unv, sid_u)
    r = unv.post(PROPOSE % sid_u, data={"anchor_record_id": "rec_1", "quantity_kind": KIND,
                                        "value_text": "1 V"})
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    viewer, _v = _client_for("t2a-viewer@example.com")
    assert viewer.get(SESSION % sid).status_code == 200
    assert "quantity/propose" not in viewer.get(SESSION % sid).get_data(as_text=True)
    r = viewer.post(PROPOSE % sid, data={"anchor_record_id": "rec_1", "quantity_kind": KIND,
                                         "value_text": "1 V"})
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    assert _rows(db_path, sid) == [] and _rows(db_path, sid_u) == []
    assert not webapp._quantity_write_authorized(sid)


# ==========================================================================
# 5. Validation, canonical storage, eligibility, staleness
# ==========================================================================
@pytest.mark.parametrize("field,value", [
    ("value_text", ""), ("value_text", "   "), ("value_text", "x" * 81),
    ("value_text", "5\nV"), ("quantity_kind", "bogus"), ("quantity_kind", ""),
    ("quantity_kind", KIND.upper()),
])
def test_invalid_input_is_rejected_generically_without_echo_or_staging(db_path, field, value):
    c, _aid = _client_for("t2a-invalid@example.com")
    sid = _start(c)
    data = {"value_text": "12.5 V", "quantity_kind": KIND}
    data[field] = value
    r = _propose(c, sid, "rec_1", **data)
    assert r.status_code == 302
    body = _page(c, sid)
    assert webapp.QUANTITY_INVALID_MESSAGE in body
    assert 'id="t2a-confirm"' not in body and "quantity_proposal" not in SESSION_STORE[sid]
    if value.strip():
        assert value not in body
    assert _rows(db_path, sid) == []


def test_value_text_is_stored_normalized_never_interpreted_or_localized(db_path):
    c, _aid = _client_for("t2a-canon@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "  0.5   mm ± 0.1 ", KIND2).status_code == 302
    rows = _rows(db_path, sid)
    assert [(x[4], x[5]) for x in rows] == [(KIND2, "0.5 mm ± 0.1")]
    body = _page(c, sid)
    assert _values(body) == ["0.5 mm ± 0.1"]
    assert c.post("/ui-language", data={"lang": "ar"}).status_code in (302, 303)
    body = _page(c, sid)
    assert _values(body) == ["0.5 mm ± 0.1"]                # never localized
    assert ui_text.text("UI_T2A_KIND_" + KIND2, "ar") in body
    with app.test_request_context():
        package = webapp._deliverable_context(sid)[1]
    assert package["_session_meta"]["requirement_quantities"]["items"][0] == {
        "statement": PROBLEM_ANSWER, "status": "current", "anchor_active": True,
        "kind": KIND2, "value_text": "0.5 mm ± 0.1",
        "provenance": "Recorded by the inventor (not yet verified)", "replaced": []}


@pytest.mark.parametrize("anchor", ["", "rec_99", "rec_0", "qty-x", "MECHANISM_COMPLETENESS",
                                    "<script>", "rec_3", "rec_1x"])
def test_ineligible_anchor_is_rejected_generically(db_path, anchor):
    c, _aid = _client_for("t2a-anchor@example.com")
    sid = _start(c)
    assert _propose(c, sid, anchor).status_code == 302
    body = _page(c, sid)
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in body and 'id="t2a-confirm"' not in body
    if anchor:
        assert anchor not in webapp.QUANTITY_NOT_SAVED_MESSAGE
    assert _rows(db_path, sid) == []


def test_non_answer_records_and_withdrawn_answers_are_not_eligible_anchors(db_path):
    c, _aid = _client_for("t2a-elig@example.com")
    sid = _start(c, answers=(PROBLEM_ANSWER,))
    assert c.post(SESSION % sid, data={"action": "unknown", "response": "",
                                       "answer_token": _token(c, sid)}).status_code == 302
    assert _anchors(c, sid) == ["rec_1"]
    assert _propose(c, sid, "rec_2").status_code == 302
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
    assert c.post(CORRECT % sid, data={"supersedes_record_id": "rec_1",
                                       "response": MECH_CORRECTED,
                                       "answer_token": _token(c, sid)}).status_code == 302
    assert "rec_1" not in _anchors(c, sid)
    assert _propose(c, sid, "rec_1").status_code == 302
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
    assert _rows(db_path, sid) == []


def test_stale_anchor_between_propose_and_confirm_is_refused(db_path):
    c, _aid = _client_for("t2a-stale-anchor@example.com")
    sid = _start(c)
    assert _propose(c, sid, "rec_2", "3 A").status_code == 302
    token = _ctoken(_page(c, sid))
    assert c.post(CORRECT % sid, data={"supersedes_record_id": "rec_2",
                                       "response": MECH_CORRECTED,
                                       "answer_token": _token(c, sid)}).status_code == 302
    assert 'id="t2a-confirm"' not in _page(c, sid)           # dropped at render
    assert _confirm(c, sid, token).status_code == 302
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
    assert _rows(db_path, sid) == []


def test_stale_quantity_head_between_propose_and_confirm_is_refused_in_the_transaction(db_path):
    c, _aid = _client_for("t2a-stale-head@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "5 V").status_code == 302
    # proposal A (supersedes the 5 V head) is staged, then the head moves on
    assert _propose(c, sid, "rec_1", "6 V").status_code == 302
    entry = SESSION_STORE[sid]
    stale = dict(entry["quantity_proposal"])
    stale_token = webapp._quantity_confirmation_token(sid, stale)
    assert _record(c, sid, "rec_1", "7 V").status_code == 302     # head is now 7 V
    entry["quantity_proposal"] = stale                             # re-present A
    assert _confirm(c, sid, stale_token).status_code == 302
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
    assert [x[5] for x in _rows(db_path, sid)] == ["5 V", "7 V"]
    assert _values(_page(c, sid)) == ["7 V"]


def test_identical_value_to_the_active_head_stages_nothing(db_path):
    c, _aid = _client_for("t2a-same@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "7 V").status_code == 302
    assert _propose(c, sid, "rec_1", " 7  V ").status_code == 302
    body = _page(c, sid)
    assert webapp.QUANTITY_SAVED_ACK in body and 'id="t2a-confirm"' not in body
    assert len(_rows(db_path, sid)) == 1


# ==========================================================================
# 6. Correction / supersession history; project isolation
# ==========================================================================
def test_replacement_builds_a_forward_edge_chain_with_one_active_head(db_path):
    c, _aid = _client_for("t2a-chain@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "7 V").status_code == 302
    assert _record(c, sid, "rec_1", "8 V", KIND2).status_code == 302
    assert _record(c, sid, "rec_1", "9 V").status_code == 302
    rows = _rows(db_path, sid)
    assert [(x[0], x[5], x[6]) for x in rows] == [
        (0, "7 V", None), (1, "8 V", rows[0][1]), (2, "9 V", rows[1][1])]
    assert len({x[7] for x in rows}) == 3                    # distinct event keys
    body = _page(c, sid)
    assert _values(body) == ["9 V"] and _replaced(body) == ["7 V", "8 V"]
    assert ui_text.text("UI_T2A_REPLACED_LABEL", "en") in body
    html = c.get(DELIVERABLE % sid).get_data(as_text=True)
    assert _values(html) == ["9 V"] and _replaced(html) == ["7 V", "8 V"]


def test_another_projects_anchor_and_history_are_isolated(db_path):
    ca, _a = _client_for("t2a-iso-a@example.com")
    sid_a = _start(ca)
    cb, _b = _client_for("t2a-iso-b@example.com")
    sid_b = _start(cb, answers=(PROBLEM_ANSWER,))
    assert _propose(cb, sid_b, "rec_2").status_code == 302   # A's rec_2 is not B's anchor
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(cb, sid_b)
    assert _record(ca, sid_a, "rec_2", "5 V").status_code == 302
    assert _record(cb, sid_b, "rec_1", "9 A", KIND2).status_code == 302
    assert _values(_page(ca, sid_a)) == ["5 V"] and _values(_page(cb, sid_b)) == ["9 A"]
    assert [x[5] for x in _rows(db_path, sid_a)] == ["5 V"]
    assert [x[5] for x in _rows(db_path, sid_b)] == ["9 A"]
    r = cb.get(DELIVERABLE % sid_a)
    assert r.status_code == 302 and r.headers["Location"].endswith("/")


# ==========================================================================
# 7. Presentation surfaces — session, HTML deliverable, PDF; localization
# ==========================================================================
def test_session_block_is_optional_collapsed_and_lists_eligible_anchors(db_path):
    c, _aid = _client_for("t2a-block@example.com")
    r = c.post("/start", data=FORM)
    sid = r.headers["Location"].rsplit("/session/", 1)[-1]
    assert "t2a-quantities" not in _page(c, sid)
    assert _answer(c, sid, PROBLEM_ANSWER).status_code == 302
    body = _page(c, sid)
    head = body.split('<details id="t2a-quantities"', 1)[1].split(">", 1)[0]
    assert " open" not in head
    assert ui_text.text("UI_T2A_HEADING", "en") in body and "optional" in ui_text.text("UI_T2A_HEADING", "en")
    assert 'data-t2a-anchor="rec_1"' in body and PROBLEM_ANSWER in body
    assert ui_text.text("UI_T2A_NONE", "en") in body
    for kind in QUANTITY_KINDS:
        assert 'value="%s"' % kind in body and ui_text.text("UI_T2A_KIND_" + kind, "en") in body
        assert ui_text.text("UI_T2A_KIND_" + kind, "ar") != "UI_T2A_KIND_" + kind
    assert 'id="answer-form"' in body and "/correct" in body
    assert len(set(re.findall(r'name="csrf_token" value="([^"]+)"', body))) == 1
    for word in ("feasib", "attainab", "validated", "verified", "safe", "compliant"):
        block = body.split('<details id="t2a-quantities"', 1)[1].split("</details>", 1)[0]
        if word in block.lower():
            assert "not" in block.lower()                # only ever negated


def test_user_statement_and_value_text_are_escaped_inside_the_quantity_block(db_path):
    c, _aid = _client_for("t2a-escape@example.com")
    sid = _start(c, answers=(HTML_ANSWER,))
    assert _record(c, sid, "rec_1", "<b>5</b> V").status_code == 302
    body = _page(c, sid)
    block = body.split('<details id="t2a-quantities"', 1)[1].split("</details>", 1)[0]
    assert "<b>board</b>" not in block and "&lt;b&gt;board&lt;/b&gt;" in block
    assert "<b>5</b>" not in block and "&lt;b&gt;5&lt;/b&gt; V" in block


def test_html_deliverable_and_pdf_present_current_replaced_and_withdrawn_read_only(
        db_path, monkeypatch):
    c, _aid = _client_for("t2a-deliv@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "12.5 V").status_code == 302
    assert _record(c, sid, "rec_1", "14 V").status_code == 302
    assert _record(c, sid, "rec_2", "3 to 5 A", KIND2).status_code == 302
    assert c.post(CORRECT % sid, data={"supersedes_record_id": "rec_2",
                                       "response": MECH_CORRECTED,
                                       "answer_token": _token(c, sid)}).status_code == 302
    html = c.get(DELIVERABLE % sid).get_data(as_text=True)
    assert 'id="t2a-requirement-quantities"' in html
    assert ui_text.text("UI_T2A_DELIV_HEADING", "en") in html
    assert "not been checked, validated, or assessed" in html
    assert _values(html) == ["14 V"] and _replaced(html) == ["12.5 V"]
    assert _withdrawn(html) == ["3 to 5 A"]
    assert ui_text.text("UI_T2A_WITHDRAWN_LABEL", "en") in html
    assert ui_text.text("UI_T2A_WITHDRAWN_NOTE", "en") in html
    assert "Recorded by the inventor (not yet verified)" in html
    assert "qty-" not in html and "anchor_withdrawn" not in html and "req:assertion" not in html
    seen = _capture_pdf_source(monkeypatch)
    r = c.post(PDF % sid, data={})
    assert r.status_code == 200 and r.headers["Content-Type"] == "application/pdf"
    source = seen["source"]
    assert 'id="t2a-requirement-quantities"' in source
    assert _values(source) == ["14 V"] and _replaced(source) == ["12.5 V"]
    assert _withdrawn(source) == ["3 to 5 A"]
    assert "quantity/" not in source and "<form" not in source
    assert "confirmation_token" not in source and "csrf_token" not in source
    assert "qty-" not in source and seen["pdf"][:5] == b"%PDF-"
    with app.test_request_context():
        meta = webapp._deliverable_context(sid)[1]["_session_meta"]["requirement_quantities"]
    assert meta["total"] == 2 and meta["active_total"] == 1 and meta["withdrawn_total"] == 1


def test_arabic_and_english_chrome_parity_with_never_localized_value_text(db_path):
    c, _aid = _client_for("t2a-ar@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "3.75 kg", KIND2).status_code == 302
    en = _page(c, sid)
    assert c.post("/ui-language", data={"lang": "ar"}).status_code in (302, 303)
    ar = _page(c, sid)
    for key in ("UI_T2A_HEADING", "UI_T2A_EXPLAIN", "UI_T2A_CURRENT", "UI_T2A_KIND_LABEL",
                "UI_T2A_VALUE_LABEL", "UI_T2A_REPLACE_BUTTON", "UI_T2A_DELIV_PROVENANCE",
                "UI_T2A_KIND_" + KIND2):
        assert ui_text.text(key, "en") in en and ui_text.text(key, "ar") in ar
        assert ui_text.text(key, "ar") != ui_text.text(key, "en")
    assert _values(en) == _values(ar) == ["3.75 kg"]
    assert [x[5] for x in _rows(db_path, sid)] == ["3.75 kg"]
    assert _propose(c, sid, "rec_1", "4 kg").status_code == 302
    ar = _page(c, sid)
    for key in ("UI_T2A_CONFIRM_HEADING", "UI_T2A_CONFIRM_EXPLAIN", "UI_T2A_CONFIRM_REPLACES",
                "UI_T2A_CONFIRM_BUTTON", "UI_T2A_DISCARD_BUTTON"):
        assert ui_text.text(key, "ar") in ar
    assert _confirm(c, sid, _ctoken(ar)).status_code == 302
    ar = _page(c, sid)
    assert ui_text.localize_deep(webapp.QUANTITY_SAVED_ACK, "ar") in ar
    assert webapp.QUANTITY_SAVED_ACK not in ar
    assert ui_text.text("UI_T2A_REPLACED_LABEL", "ar") in ar and _replaced(ar) == ["3.75 kg"]
    html = c.get(DELIVERABLE % sid).get_data(as_text=True)
    assert ui_text.text("UI_T2A_DELIV_HEADING", "ar") in html and "4 kg" in html
    assert _propose(c, sid, "rec_1", "").status_code == 302
    ar = _page(c, sid)
    assert ui_text.localize_message(webapp.QUANTITY_INVALID_MESSAGE, "ar") in ar
    assert webapp.QUANTITY_INVALID_MESSAGE not in ar
    assert ui_text.localize_deep(webapp.QUANTITY_DISCARDED_ACK, "ar") != webapp.QUANTITY_DISCARDED_ACK


def test_zero_rows_leave_package_html_and_pdf_source_byte_identical(db_path, monkeypatch):
    c, _aid = _client_for("t2a-zero@example.com")
    sid = _start(c)
    monkeypatch.setattr(_assembler, "_now_iso", lambda: "2026-01-01T00:00:00+00:00")
    seen = _capture_pdf_source(monkeypatch)
    real_html = c.get(DELIVERABLE % sid).get_data()
    assert c.post(PDF % sid, data={}).status_code == 200
    real_source = seen["source"]
    with app.test_request_context():
        real_package = webapp._deliverable_context(sid)[1]
    monkeypatch.setattr(webapp, "_attach_quantity_history", lambda sid, state: True)
    monkeypatch.setattr(webapp, "_requirement_quantities_meta", lambda state: None)
    SESSION_STORE[sid]["state"].requirement_quantities = []
    base_html = c.get(DELIVERABLE % sid).get_data()
    assert c.post(PDF % sid, data={}).status_code == 200
    assert real_html == base_html and real_source == seen["source"]
    assert "requirement_quantities" not in real_package["_session_meta"]
    assert json.dumps(real_package, sort_keys=True) == json.dumps(
        _assembler.assemble_deliverable(SESSION_STORE[sid]["state"]), sort_keys=True)
    assert "t2a-requirement-quantities" not in real_html.decode("utf-8")
    assert "t2a-requirement-quantities" not in real_source


# ==========================================================================
# 8. Cold load, resume, migration
# ==========================================================================
def test_cold_load_restores_history_on_every_surface_and_refuses_cold_writes(db_path, monkeypatch):
    c, _aid = _client_for("t2a-cold@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "42 pieces").status_code == 302
    assert _record(c, sid, "rec_1", "43 pieces").status_code == 302
    SESSION_STORE.clear()
    body = _page(c, sid)
    assert 'id="reconstructed-review"' in body
    assert _values(body) == ["43 pieces"] and _replaced(body) == ["42 pieces"]
    assert "quantity/propose" not in body
    html = c.get(DELIVERABLE % sid).get_data(as_text=True)
    assert 'id="reconstructed-deliverable"' in html and _values(html) == ["43 pieces"]
    seen = _capture_pdf_source(monkeypatch)
    assert c.post(PDF % sid, data={}).status_code == 200
    assert _values(seen["source"]) == ["43 pieces"]
    assert _propose(c, sid, "rec_1", "44 pieces").status_code == 302
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
    assert [x[5] for x in _rows(db_path, sid)] == ["42 pieces", "43 pieces"]
    assert c.post("/session/%s/resume" % sid, data={}).status_code == 302
    assert [q.value_text for q in SESSION_STORE[sid]["state"].requirement_quantities] == [
        "42 pieces", "43 pieces"]
    assert _record(c, sid, "rec_1", "44 pieces").status_code == 302
    assert _values(_page(c, sid)) == ["44 pieces"]


def test_existing_populated_pre_t2a_database_is_migrated_by_the_application(db_path):
    c, aid = _client_for("t2a-migrate@example.com")
    sid = _start(c)
    ledger_before = _ledger_rows(db_path, sid)
    _store().close()
    webapp._STORE = None
    conn = sqlite3.connect(db_path)
    conn.execute("DROP TABLE requirement_quantities")
    conn.commit()
    conn.close()
    SESSION_STORE.clear()
    body = _page(c, sid)
    assert 'id="reconstructed-review"' in body and "t2a-value" not in body
    assert _ledger_rows(db_path, sid) == ledger_before
    assert _store().load_requirement_quantities(sid) == ()
    assert _store().load_owner(sid) == (True, aid)
    conn = sqlite3.connect(db_path)
    try:
        assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
        fks = conn.execute("PRAGMA foreign_key_list(requirement_quantities)").fetchall()
        assert {fk[2] for fk in fks} == {"projects", "records", "requirement_quantities"}
    finally:
        conn.close()


# ==========================================================================
# 9. Corrupt history fails closed at EVERY affected surface; cap via the web
# ==========================================================================
def test_corrupt_populated_history_fails_closed_on_every_surface(db_path, monkeypatch):
    c, _aid = _client_for("t2a-corrupt@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "5 V").status_code == 302
    assert _propose(c, sid, "rec_1", "6 V").status_code == 302
    token = _ctoken(_page(c, sid))
    _corrupt(db_path, sid)
    before_rows = _rows(db_path, sid)
    with pytest.raises(QuantityHistoryError):
        _store().load_requirement_quantities(sid)
    for verb, path in (("get", SESSION % sid), ("get", DELIVERABLE % sid), ("post", PDF % sid)):
        r = getattr(c, verb)(path, data={})
        assert r.status_code == 302 and r.headers["Location"].endswith("/"), (verb, path)
        text = r.get_data(as_text=True)
        assert "qty-" not in text and "bogus" not in text and "sqlite" not in text.lower()
    assert [q.value_text for q in SESSION_STORE[sid]["state"].requirement_quantities] == ["5 V"]
    # confirm on the corrupt history: refused INSIDE the store transaction
    assert _confirm(c, sid, token).status_code == 302
    assert SESSION_STORE[sid].get("_answer_error") == webapp.QUANTITY_NOT_SAVED_MESSAGE
    assert _rows(db_path, sid) == before_rows
    # propose on the corrupt history: refused, nothing staged
    r = c.post(PROPOSE % sid, data={"anchor_record_id": "rec_1", "quantity_kind": KIND,
                                    "value_text": "7 V"})
    assert r.status_code == 302 and "quantity_proposal" not in SESSION_STORE[sid]
    SESSION_STORE.clear()
    r = c.get(SESSION % sid)
    assert r.status_code == 302 and r.headers["Location"].endswith("/") and sid not in SESSION_STORE


def test_storage_unavailability_fails_closed_without_partial_state(db_path, monkeypatch):
    c, _aid = _client_for("t2a-unavailable@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "5 V").status_code == 302
    assert _propose(c, sid, "rec_1", "6 V").status_code == 302
    token = _ctoken(_page(c, sid))
    store = _store()
    monkeypatch.setattr(store, "load_requirement_quantities",
                        lambda pid: (_ for _ in ()).throw(sqlite3.OperationalError("db gone")))
    for verb, path in (("get", SESSION % sid), ("get", DELIVERABLE % sid), ("post", PDF % sid)):
        r = getattr(c, verb)(path, data={})
        assert r.status_code == 302 and r.headers["Location"].endswith("/")
        assert "db gone" not in r.get_data(as_text=True)
    monkeypatch.setattr(store, "append_requirement_quantity",
                        lambda *a, **k: (_ for _ in ()).throw(sqlite3.OperationalError("db gone")))
    assert _confirm(c, sid, token).status_code == 302
    assert SESSION_STORE[sid].get("_answer_error") == webapp.QUANTITY_NOT_SAVED_MESSAGE
    assert [x[5] for x in _rows(db_path, sid)] == ["5 V"]
    assert _propose(c, sid, "rec_1", "7 V").status_code == 302
    assert SESSION_STORE[sid].get("_answer_error") == webapp.QUANTITY_NOT_SAVED_MESSAGE


def test_durable_append_failure_publishes_nothing_persist_before_acknowledge(db_path, monkeypatch):
    from engine.record_store import StoreError
    c, _aid = _client_for("t2a-append-fail@example.com")
    sid = _start(c)
    assert _propose(c, sid, "rec_1", "5 V").status_code == 302
    token = _ctoken(_page(c, sid))
    store = _store()
    monkeypatch.setattr(store, "append_requirement_quantity",
                        lambda *a, **k: (_ for _ in ()).throw(StoreError("unavailable")))
    entry = SESSION_STORE[sid]
    before = pickle.dumps(entry["state"])
    assert _confirm(c, sid, token).status_code == 302
    body = _page(c, sid)
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in body and webapp.QUANTITY_SAVED_ACK not in body
    assert entry["state"].requirement_quantities == [] and _rows(db_path, sid) == []
    assert "unavailable" not in body and pickle.dumps(entry["state"]) == before


def test_project_cap_is_enforced_through_the_web_flow_at_200(db_path):
    c, _aid = _client_for("t2a-cap@example.com")
    sid = _start(c)
    store = _store()
    # fill to 199 durable rows directly through the canonical store seam
    from engine.requirement_quantity import RequirementQuantity
    head = None
    for i in range(MAX_REQUIREMENT_QUANTITIES_PER_PROJECT - 1):
        q = RequirementQuantity(sid, -1, store.new_quantity_id(), "rec_1",
                                "req:assertion:rec_1", KIND, "v %d" % i, head, "%032x" % i)
        store.append_requirement_quantity(sid, q)
        head = q.quantity_id
    assert len(_rows(db_path, sid)) == 199
    assert _record(c, sid, "rec_1", "row 200").status_code == 302     # 200th succeeds
    assert webapp.QUANTITY_SAVED_ACK in _page(c, sid)
    assert len(_rows(db_path, sid)) == 200
    assert _record(c, sid, "rec_1", "row 201").status_code == 302     # 201st refused
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
    assert len(_rows(db_path, sid)) == 200 and _values(_page(c, sid)) == ["row 200"]


# ==========================================================================
# 10. Owner-mandated correction-flow ordering
# ==========================================================================
def test_corrupt_populated_quantity_history_blocks_correction_before_durable_append(db_path):
    c, _aid = _client_for("t2a-corr-block@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "5 V").status_code == 302
    token = _token(c, sid)
    ledger_before = _ledger_rows(db_path, sid)
    state_before = pickle.dumps(SESSION_STORE[sid]["state"])
    _corrupt(db_path, sid, "UPDATE requirement_quantities SET value_text = ' 5 V' "
                           "WHERE project_id = ?")
    rows_before = _rows(db_path, sid)
    r = c.post(CORRECT % sid, data={"supersedes_record_id": "rec_2",
                                    "response": MECH_CORRECTED, "answer_token": token})
    assert r.status_code == 302 and r.headers["Location"] == SESSION % sid
    assert _ledger_rows(db_path, sid) == ledger_before and _rows(db_path, sid) == rows_before
    assert pickle.dumps(SESSION_STORE[sid]["state"]) == state_before
    assert SESSION_STORE[sid].get("_answer_error") == webapp.CORRECTION_NOT_APPLIED_MESSAGE
    assert SESSION_STORE[sid].get("_interaction_ack") is None
    for forbidden in ("qty-", "rec_", "5 V", "sqlite", "SELECT", "Traceback", "/"):
        assert forbidden not in webapp.CORRECTION_NOT_APPLIED_MESSAGE
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
    assert r.status_code == 302 and appended == []
    assert _ledger_rows(db_path, sid) == ledger_before
    assert SESSION_STORE[sid].get("_answer_error") == webapp.CORRECTION_NOT_APPLIED_MESSAGE


def test_zero_quantity_rows_do_not_block_correction(db_path):
    c, _aid = _client_for("t2a-corr-zero@example.com")
    sid = _start(c)
    assert _rows(db_path, sid) == []
    r = c.post(CORRECT % sid, data={"supersedes_record_id": "rec_2",
                                    "response": MECH_CORRECTED, "answer_token": _token(c, sid)})
    assert r.status_code == 302
    assert SESSION_STORE[sid].get("_answer_error") is None
    assert SESSION_STORE[sid].get("_interaction_ack") == webapp.CORRECTION_APPLIED_ACK
    assert [x[1] for x in _ledger_rows(db_path, sid)] == ["rec_1", "rec_2", "rec_3"]
    assert SESSION_STORE[sid]["state"].requirement_quantities == []


def test_valid_quantity_history_survives_correction_reconstruction(db_path):
    c, _aid = _client_for("t2a-corr-survive@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "5 V").status_code == 302
    r = c.post(CORRECT % sid, data={"supersedes_record_id": "rec_2",
                                    "response": MECH_CORRECTED, "answer_token": _token(c, sid)})
    assert r.status_code == 302
    body = _page(c, sid)
    assert webapp.CORRECTION_APPLIED_ACK in body
    state = SESSION_STORE[sid]["state"]
    assert [(q.anchor_record_id, q.value_text) for q in state.requirement_quantities] == [("rec_1", "5 V")]
    assert getattr(state, "domain", None) is not None
    assert _values(body) == ["5 V"]
    assert _values(c.get(DELIVERABLE % sid).get_data(as_text=True)) == ["5 V"]
    assert _record(c, sid, "rec_1", "6 V").status_code == 302
    assert _values(_page(c, sid)) == ["6 V"] and _replaced(_page(c, sid)) == ["5 V"]


def test_superseded_anchor_becomes_inactive_deterministically(db_path):
    c, _aid = _client_for("t2a-corr-anchor@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "5 V").status_code == 302
    assert _record(c, sid, "rec_2", "7 A").status_code == 302
    r = c.post(CORRECT % sid, data={"supersedes_record_id": "rec_2",
                                    "response": MECH_CORRECTED, "answer_token": _token(c, sid)})
    assert r.status_code == 302
    body = _page(c, sid)
    assert _anchors(c, sid) == ["rec_1", "rec_3"]
    assert _values(body) == ["5 V"] and _withdrawn(body) == ["7 A"]
    assert ui_text.text("UI_T2A_WITHDRAWN_NOTE", "en") in body
    with app.test_request_context():
        meta = webapp._deliverable_context(sid)[1]["_session_meta"]["requirement_quantities"]
    assert [(i["value_text"], i["anchor_active"]) for i in meta["items"]] == [("5 V", True), ("7 A", False)]
    assert [(x[2], x[5]) for x in _rows(db_path, sid)] == [("rec_1", "5 V"), ("rec_2", "7 A")]
    from engine.session_reconstruction import reconstruct_readonly_state
    from engine.requirement_quantity import quantity_chains
    outcomes = []
    for _ in range(2):
        s = reconstruct_readonly_state(_store(), sid).state
        s.requirement_quantities = list(_store().load_requirement_quantities(sid))
        outcomes.append([(ch.anchor_record_id, ch.active.value_text, ch.anchor_active)
                         for ch in quantity_chains(s)])
    assert outcomes[0] == outcomes[1] == [("rec_1", "5 V", True), ("rec_2", "7 A", False)]
    assert _propose(c, sid, "rec_2", "8 A").status_code == 302
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
    assert _record(c, sid, "rec_3", "8 A").status_code == 302
    assert _values(_page(c, sid)) == ["5 V", "8 A"]


def test_another_project_remains_unaffected_by_correction_and_corruption(db_path):
    ca, _a = _client_for("t2a-corr-a@example.com")
    sid_a = _start(ca)
    cb, _b = _client_for("t2a-corr-b@example.com")
    sid_b = _start(cb)
    assert _record(ca, sid_a, "rec_1", "5 V").status_code == 302
    assert _record(cb, sid_b, "rec_1", "9 A").status_code == 302
    b_state_before = pickle.dumps(SESSION_STORE[sid_b]["state"])
    b_rows_before = _rows(db_path, sid_b)
    assert ca.post(CORRECT % sid_a, data={"supersedes_record_id": "rec_2",
                                          "response": MECH_CORRECTED,
                                          "answer_token": _token(ca, sid_a)}).status_code == 302
    assert pickle.dumps(SESSION_STORE[sid_b]["state"]) == b_state_before
    assert _rows(db_path, sid_b) == b_rows_before and _values(_page(cb, sid_b)) == ["9 A"]
    _corrupt(db_path, sid_a)
    r = ca.get(SESSION % sid_a)
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    assert _values(_page(cb, sid_b)) == ["9 A"]
    assert cb.post(CORRECT % sid_b, data={"supersedes_record_id": "rec_2",
                                          "response": MECH_CORRECTED,
                                          "answer_token": _token(cb, sid_b)}).status_code == 302
    assert SESSION_STORE[sid_b].get("_interaction_ack") == webapp.CORRECTION_APPLIED_ACK
    assert _values(_page(cb, sid_b)) == ["9 A"]


def test_post_commit_reattachment_failure_keeps_live_state_and_tells_the_truth(db_path, monkeypatch):
    c, _aid = _client_for("t2a-corr-post@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "5 V").status_code == 302
    store = _store()
    real_load = store.load_requirement_quantities
    calls = {"n": 0}

    def flaky(pid):
        calls["n"] += 1
        if calls["n"] == 2:
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
    SESSION_STORE.clear()
    assert _values(_page(c, sid)) == ["5 V"]


# ==========================================================================
# 11. Boundary: routes, no API / export / adapter change
# ==========================================================================
def test_route_inventory_and_untouched_api_export_adapter_surfaces():
    rules = {r.rule: r.methods - {"HEAD", "OPTIONS"} for r in app.url_map.iter_rules()
             if "quantity" in r.rule}
    assert rules == {"/session/<sid>/quantity/propose": {"POST"},
                     "/session/<sid>/quantity/confirm": {"POST"}}
    assert not webapp._quantity_write_authorized("no-such-project")
    import subprocess
    root = os.path.join(os.path.dirname(__file__), "..")
    for path in ("engine/read_export_service.py", "engine/export_adapter.py", "web/api_v1.py",
                 "tests/test_p7_i2_public_api.py", "engine/deliverable_assembler.py"):
        text = open(os.path.join(root, path), encoding="utf-8").read()
        assert "requirement_quantit" not in text and "quantity_kind" not in text, path
    out = subprocess.run(["git", "diff", "--name-only",
                          "9f883956bc54dd960ec33a502259e353e6db20f3", "--",
                          "engine/read_export_service.py", "engine/export_adapter.py",
                          "web/api_v1.py", "tests/test_p7_i2_public_api.py"],
                         capture_output=True, text=True, cwd=root)
    assert out.returncode == 0 and out.stdout.strip() == ""
