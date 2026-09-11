"""T2-A Quantified Requirements Slice 1 — web-layer proof (two-stage flow).

File: tests/test_t2a_requirement_quantity_web.py
Purpose: behaviour tests for the two security-sensitive POST routes
(`/session/<sid>/quantity/propose` and `/session/<sid>/quantity/confirm`):
propose performs no durable write; the confirm form carries only
csrf_token, confirmation_token and quantity_action; exact confirmation
succeeds once; nonce replay, altered action/content, expiry (899 accepted,
900 expired), tampering, session-binding change, owner change, every
material-field mutation, cross-session, cross-project and cross-owner tokens
cannot write; anonymous, NULL-owner, unverified, inactive and non-owner
denial; stale anchor and stale quantity head between propose and confirm;
corrupt history detected inside the transaction; the per-project cap through
the web flow; correction/supersession history; the canonical package shape;
replaced-value and withdrawn-anchor rendering on the session page, the HTML
deliverable and the PDF source; Arabic/English chrome parity with
never-localized value text; zero-row package / HTML / PDF-source
equivalence; the Owner-mandated correction-flow ordering; and no API /
export / adapter change.

Real Flask application, real on-disk SQLite (autouse conftest isolation),
real account + record stores, real signed sessions, real WeasyPrint for the
PDF proofs. Security boundaries are never mocked; monkeypatching is used only
to inject storage failures, to drive the clock, or to capture the exact
document handed to the renderer.
"""
from tests.csrf_client import csrf_client
import contextlib
import copy
import json
import os
import pickle
import re
import sqlite3

import jinja2
import pytest

import web.app as webapp
from web.app import app, SESSION_STORE
from web import ui_text
from engine import account_credentials as _acct
from engine import deliverable_assembler as _assembler
from engine.requirement_quantity import (
    CANONICAL_ROW_FIELDS, QUANTITY_KINDS, QuantityHistoryError,
    MAX_REQUIREMENT_QUANTITIES_PER_PROJECT, MAX_VALUE_TEXT_CHARS,
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
KIND = "target_value"
KIND2 = "maximum_value"

PROPOSE = "/session/%s/quantity/propose"
CONFIRM = "/session/%s/quantity/confirm"
SESSION = "/session/%s"
DELIVERABLE = "/session/%s/deliverable"
PDF = "/session/%s/deliverable.pdf"
CORRECT = "/session/%s/correct"
MATERIAL_FIELDS = ("anchor_record_id", "requirement_id", "quantity_kind", "value_text",
                   "supersedes_quantity_id", "nonce", "issued_at", "expires_at")


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
            "value_text, supersedes_quantity_id, event_key, recorded_iteration, recorded_at "
            "FROM requirement_quantities WHERE project_id = ? ORDER BY quantity_seq", (sid,)
        ).fetchall()
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


def _package(sid):
    with app.test_request_context():
        return webapp._deliverable_context(sid)[1]


T2A_BLOCK_BEGIN = "  {#- T2A-BLOCK-BEGIN"
T2A_BLOCK_END = "T2A-BLOCK-END #}\n"
_TEMPLATES = os.path.join(os.path.dirname(__file__), "..", "web", "templates")


def _template_source(name):
    with open(os.path.join(_TEMPLATES, name), encoding="utf-8") as fh:
        return fh.read()


def base_deliverable_source():
    """The report template with the T2-A addition textually REMOVED — the base
    source this slice must stay byte-equivalent to when no quantity exists.
    Reconstructed from the two sentinels in the template itself, so it needs no
    fixture file, no VCS checkout and no `.git` directory."""
    text = _template_source("deliverable.html")
    start = text.index(T2A_BLOCK_BEGIN)
    end = text.index(T2A_BLOCK_END, start) + len(T2A_BLOCK_END)
    stripped = text[:start] + text[end:]
    assert "t2a" not in stripped.lower(), "the base source still carries T2-A text"
    return stripped


@contextlib.contextmanager
def _base_deliverable_template():
    """Serve the BASE report source for `deliverable.html` while keeping the
    real route, the real context and every other template unchanged."""
    original = app.jinja_env.loader
    app.jinja_env.loader = jinja2.ChoiceLoader(
        [jinja2.DictLoader({"deliverable.html": base_deliverable_source()}), original])
    app.jinja_env.cache.clear()
    try:
        yield
    finally:
        app.jinja_env.loader = original
        app.jinja_env.cache.clear()


# ==========================================================================
# 1. Routes, CSRF integrity, no durable write on propose
# ==========================================================================
def test_both_routes_are_post_only_and_csrf_guarded_before_any_state(db_path):
    c, _aid = _client_for("t2a-csrf@example.com")
    sid = _start(c)
    for path in (PROPOSE % sid, CONFIRM % sid):
        assert c.get(path).status_code == 405
    before = _snapshot(sid, db_path)
    raw = app.test_client()
    with raw.session_transaction() as s, c.session_transaction() as mine:
        s.update(copy.deepcopy(dict(mine)))
    r = raw.post(PROPOSE % sid, data={"anchor_record_id": "rec_1", "quantity_kind": KIND,
                                      "value_text": "1 V"})
    assert r.status_code == 403
    r = raw.post(CONFIRM % sid, data={"confirmation_token": "x.y", "quantity_action": "confirm"})
    assert r.status_code == 403
    assert _rows(db_path, sid) == [] and _snapshot(sid, db_path)[1] == before[1]
    assert "quantity_proposal" not in SESSION_STORE[sid]


def test_propose_stages_one_bounded_proposal_and_performs_no_durable_write(db_path, monkeypatch):
    c, _aid = _client_for("t2a-propose@example.com")
    sid = _start(c)
    base = 1_700_000_000
    monkeypatch.setattr(webapp, "_quantity_clock", lambda: base)
    monkeypatch.setattr(webapp, "_quantity_recorded_at", lambda: "2026-09-11T12:00:00+00:00")
    db_before = _snapshot(sid, db_path)[1]
    r = _propose(c, sid, "rec_1", "  12.5   V ", KIND)
    assert r.status_code == 302 and r.headers["Location"].endswith("#t2a-confirm")
    assert _rows(db_path, sid) == [] and _snapshot(sid, db_path)[1] == db_before
    staged = SESSION_STORE[sid]["quantity_proposal"]
    assert set(staged) == {"nonce", "issued_at", "expires_at", "account_id", "session_binding",
                           "anchor_record_id", "requirement_id", "quantity_kind", "value_text",
                           "supersedes_quantity_id", "recorded_iteration", "recorded_at"}
    assert re.fullmatch(r"[0-9a-f]{16}", staged["session_binding"])
    assert staged["anchor_record_id"] == "rec_1"
    assert staged["requirement_id"] == "req:assertion:rec_1"
    assert staged["quantity_kind"] == KIND and staged["value_text"] == "12.5   V"
    assert staged["supersedes_quantity_id"] is None and staged["account_id"] == _aid
    assert staged["issued_at"] == base
    assert staged["expires_at"] == base + webapp.QUANTITY_CONFIRMATION_TTL_SECONDS
    assert staged["recorded_iteration"] == SESSION_STORE[sid]["state"].iteration
    assert staged["recorded_at"] == "2026-09-11T12:00:00+00:00"
    body = _page(c, sid)
    assert 'id="t2a-confirm"' in body and _ctoken(body)
    assert '<bdi class="t2a-proposed" dir="auto">12.5   V</bdi>' in body
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
# 2. Exact confirmation once; replay; altered content; discard; exact replay
# ==========================================================================
def test_exact_confirmation_succeeds_once_and_nonce_replay_cannot_write_twice(db_path):
    c, aid = _client_for("t2a-once@example.com")
    sid = _start(c)
    assert _propose(c, sid, "rec_1", "7 V").status_code == 302
    staged = dict(SESSION_STORE[sid]["quantity_proposal"])
    token = _ctoken(_page(c, sid))
    with c.session_transaction() as s:
        csrf = s["auth"]["csrf"]
    # the rendered token is exactly the §7 construction under the live binding
    with app.test_request_context():
        from flask import session as flask_session
        flask_session["auth"] = {"csrf": csrf}
        digest = webapp._quantity_material_digest(sid, aid, webapp._quantity_session_binding(), staged)
        expected = webapp._quantity_confirmation_token(sid, digest, staged["nonce"])
        expected_event_key = webapp._quantity_event_key(sid, staged["nonce"], digest)
    assert token == expected and len(token.split(".")[1]) == 32
    r = _confirm(c, sid, token)
    assert r.status_code == 302 and r.headers["Location"] == SESSION % sid
    body = _page(c, sid)
    assert webapp.QUANTITY_SAVED_ACK in body and _values(body) == ["7 V"]
    rows = _rows(db_path, sid)
    assert [(x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]) for x in rows] == [
        ("rec_1", "req:assertion:rec_1", KIND, "7 V", None, expected_event_key,
         staged["recorded_iteration"], staged["recorded_at"])]
    assert "quantity_proposal" not in SESSION_STORE[sid]
    for _ in range(3):
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
    for extra in ({"value_text": "999 V"}, {"anchor_record_id": "rec_2"},
                  {"quantity_kind": KIND2}, {"answer_token": "x"}):
        assert _confirm(c, sid, token, **extra).status_code == 302
        assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
        assert _rows(db_path, sid) == []
    assert _confirm(c, sid, token, action="apply").status_code == 302
    assert _rows(db_path, sid) == [] and "quantity_proposal" not in SESSION_STORE[sid]
    assert _confirm(c, sid, token).status_code == 302
    assert _rows(db_path, sid) == []
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
    assert _confirm(c, sid, token).status_code == 302
    assert _rows(db_path, sid) == []


def test_exact_replay_of_the_same_event_is_idempotent_through_the_event_key(db_path, monkeypatch):
    """CR-4: the stable event key is resolved BEFORE chain position, so an
    exact replay is EXACT_REPLAY — not a new-write conflict. The proof consumes
    the original success notice first, so it can never pass on stale flash
    state, and it asserts that exactly ONE durable row remains."""
    c, _aid = _client_for("t2a-event@example.com")
    sid = _start(c)
    assert _propose(c, sid, "rec_1", "7 V").status_code == 302
    staged = dict(SESSION_STORE[sid]["quantity_proposal"])
    token = _ctoken(_page(c, sid))
    assert _confirm(c, sid, token).status_code == 302
    rows = _rows(db_path, sid)
    assert len(rows) == 1
    # CONSUME the original success notice: render once and clear both slots, so
    # the assertion below can only observe a notice the REPLAY itself produced.
    assert webapp.QUANTITY_SAVED_ACK in _page(c, sid)
    SESSION_STORE[sid].pop("_interaction_ack", None)
    SESSION_STORE[sid].pop("_answer_error", None)
    assert webapp.QUANTITY_SAVED_ACK not in _page(c, sid)
    store = _store()
    real_append = store.append_requirement_quantity
    calls = []

    def tracking(pid, q):
        outcome = real_append(pid, q)
        calls.append((q.event_key, outcome))
        return outcome
    monkeypatch.setattr(store, "append_requirement_quantity", tracking)
    # the SAME staged event presented again (same nonce, same material) resolves
    # to the stored event under the UNIQUE event key
    SESSION_STORE[sid]["quantity_proposal"] = dict(staged)
    assert _confirm(c, sid, token).status_code == 302
    assert calls == [(rows[0][7], "EXACT_REPLAY")]
    assert SESSION_STORE[sid].get("_answer_error") is None
    assert SESSION_STORE[sid].get("_interaction_ack") == webapp.QUANTITY_SAVED_ACK
    assert webapp.QUANTITY_SAVED_ACK in _page(c, sid)
    assert _rows(db_path, sid) == rows and len(_rows(db_path, sid)) == 1


# ==========================================================================
# 3. Token binding: expiry, tampering, session binding, owner, material fields
# ==========================================================================
def test_token_expiry_899_accepted_900_expired(db_path, monkeypatch):
    c, _aid = _client_for("t2a-expiry@example.com")
    sid = _start(c)
    base = 1_700_000_000
    monkeypatch.setattr(webapp, "_quantity_clock", lambda: base)
    assert webapp.QUANTITY_CONFIRMATION_TTL_SECONDS == 900
    assert _propose(c, sid, "rec_1", "7 V").status_code == 302
    token = _ctoken(_page(c, sid))
    monkeypatch.setattr(webapp, "_quantity_clock", lambda: base + 900)
    assert 'id="t2a-confirm"' not in _page(c, sid)           # dropped at render
    assert _confirm(c, sid, token).status_code == 302
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
    assert _rows(db_path, sid) == []
    monkeypatch.setattr(webapp, "_quantity_clock", lambda: base)
    assert _propose(c, sid, "rec_1", "7 V").status_code == 302
    token = _ctoken(_page(c, sid))
    monkeypatch.setattr(webapp, "_quantity_clock", lambda: base + 899)
    assert 'id="t2a-confirm"' in _page(c, sid)
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
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in body and token not in body
    assert _rows(db_path, sid) == []


def test_session_binding_change_is_rejected(db_path):
    c, _aid = _client_for("t2a-binding@example.com")
    sid = _start(c)
    assert _propose(c, sid, "rec_1", "7 V").status_code == 302
    token = _ctoken(_page(c, sid))
    with c.session_transaction() as s:
        s["auth"]["csrf"] = "rotated-session-token-value"
    r = c.post(CONFIRM % sid, data={"confirmation_token": token, "quantity_action": "confirm",
                                    "csrf_token": "rotated-session-token-value"})
    assert r.status_code == 302 and r.headers["Location"] == SESSION % sid
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
    assert _rows(db_path, sid) == []
    # CR-3: refused BEFORE nonce consumption — a rotated/foreign session never
    # spends the staging session's proposal, and never gets a usable token.
    assert SESSION_STORE[sid]["quantity_proposal"]["value_text"] == "7 V"
    assert _ctoken(_page(c, sid)) is None


def test_owner_change_is_rejected(db_path):
    c, aid = _client_for("t2a-ownerchange@example.com")
    sid = _start(c)
    other, aid_b = _client_for("t2a-ownerchange-b@example.com")
    assert _propose(c, sid, "rec_1", "7 V").status_code == 302
    token = _ctoken(_page(c, sid))
    # the staged owner is forged to another account: the live owner no longer matches
    SESSION_STORE[sid]["quantity_proposal"]["account_id"] = aid_b
    assert _confirm(c, sid, token).status_code == 302
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
    assert _rows(db_path, sid) == []
    # the other account presenting the owner's valid token is denied generically
    assert _propose(c, sid, "rec_1", "7 V").status_code == 302
    token = _ctoken(_page(c, sid))
    r = _confirm(other, sid, token)
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    assert _rows(db_path, sid) == []


@pytest.mark.parametrize("field", MATERIAL_FIELDS)
def test_every_material_field_mutation_is_rejected(db_path, field):
    c, _aid = _client_for("t2a-material@example.com")
    sid = _start(c)
    assert _propose(c, sid, "rec_1", "7 V").status_code == 302
    token = _ctoken(_page(c, sid))
    staged = SESSION_STORE[sid]["quantity_proposal"]
    mutated = {"anchor_record_id": "rec_2", "requirement_id": "req:assertion:rec_2",
               "quantity_kind": KIND2, "value_text": "8 V", "supersedes_quantity_id": "qty-x",
               "nonce": staged["nonce"] + "x", "issued_at": staged["issued_at"] - 1,
               "expires_at": staged["expires_at"] + 1}[field]
    staged[field] = mutated
    assert _confirm(c, sid, token).status_code == 302
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
    assert _rows(db_path, sid) == []


def test_cross_session_cross_project_and_cross_owner_tokens_are_refused(db_path):
    ca, aid_a = _client_for("t2a-x-a@example.com")
    sid_a = _start(ca)
    sid_a2 = _start(ca)
    cb, aid_b = _client_for("t2a-x-b@example.com")
    sid_b = _start(cb)
    assert _propose(ca, sid_a2, "rec_1", "7 V").status_code == 302     # cross-project
    tok_a2 = _ctoken(_page(ca, sid_a2))
    assert _propose(ca, sid_a, "rec_1", "7 V").status_code == 302
    assert _confirm(ca, sid_a, tok_a2).status_code == 302
    assert _rows(db_path, sid_a) == [] and _rows(db_path, sid_a2) == []
    assert _propose(ca, sid_a, "rec_1", "7 V").status_code == 302     # cross-owner
    tok_a = _ctoken(_page(ca, sid_a))
    r = _confirm(cb, sid_a, tok_a)
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    assert _rows(db_path, sid_a) == []
    # cross-session: the SAME owner in a SECOND browser session cannot confirm
    # a proposal staged under the first session's binding
    ca2 = _new_client()
    ca2.post("/login", data={"email": "t2a-x-a@example.com", "password": PW})
    assert _confirm(ca2, sid_a, tok_a).status_code == 302
    assert SESSION_STORE[sid_a].get("_answer_error") == webapp.QUANTITY_NOT_SAVED_MESSAGE
    assert _rows(db_path, sid_a) == []
    assert _propose(cb, sid_b, "rec_1", "9 A", KIND2).status_code == 302
    assert _confirm(cb, sid_b, tok_a).status_code == 302
    assert _rows(db_path, sid_b) == []


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
    assert _confirm(owner, sid, token).status_code == 302
    assert [x[5] for x in _rows(db_path, sid)] == ["7 V"]
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
# 5. Validation, exact storage, eligibility, staleness
# ==========================================================================
@pytest.mark.parametrize("field,value", [
    ("value_text", ""), ("value_text", "   "), ("value_text", "a" * 121),
    ("value_text", "5\tV"), ("value_text", "5\nV"), ("value_text", "5\x7fV"),
    ("quantity_kind", "bogus"), ("quantity_kind", ""), ("quantity_kind", "tolerance"),
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


def test_value_text_is_stored_exactly_never_parsed_normalized_or_localized(db_path):
    c, _aid = _client_for("t2a-exact@example.com")
    sid = _start(c)
    raw = "  0.5   mm ± 0.1  "
    assert _record(c, sid, "rec_1", raw, KIND2).status_code == 302
    rows = _rows(db_path, sid)
    assert [(x[4], x[5]) for x in rows] == [(KIND2, "0.5   mm ± 0.1")]   # internal spaces kept
    body = _page(c, sid)
    assert _values(body) == ["0.5   mm ± 0.1"] and 'maxlength="120"' in body
    assert c.post("/ui-language", data={"lang": "ar"}).status_code in (302, 303)
    body = _page(c, sid)
    assert _values(body) == ["0.5   mm ± 0.1"]
    assert ui_text.text("UI_T2A_KIND_MAXIMUM_VALUE", "ar") in body
    exactly_120 = "1" * MAX_VALUE_TEXT_CHARS
    assert _record(c, sid, "rec_2", " " + exactly_120 + " ").status_code == 302
    assert [x[5] for x in _rows(db_path, sid)][-1] == exactly_120
    assert _propose(c, sid, "rec_2", "1" * 121).status_code == 302
    assert ui_text.localize_message(webapp.QUANTITY_INVALID_MESSAGE, "ar") in _page(c, sid)


def test_package_rows_are_canonical_with_no_labels_or_prose(db_path):
    c, _aid = _client_for("t2a-package@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "5 V").status_code == 302
    assert _record(c, sid, "rec_1", "6 V", KIND2).status_code == 302
    meta = _package(sid)["_session_meta"]["requirement_quantities"]
    assert set(meta) == {"total", "rows"} and meta["total"] == 2
    assert [set(r) for r in meta["rows"]] == [set(CANONICAL_ROW_FIELDS) | {"active", "anchor_active"}] * 2
    assert [(r["quantity_seq"], r["quantity_kind"], r["value_text"], r["active"], r["anchor_active"],
             r["validation_status"], r["provenance"]) for r in meta["rows"]] == [
        (0, KIND, "5 V", False, True, "UNVALIDATED", "OWNER_STATED"),
        (1, KIND2, "6 V", True, True, "UNVALIDATED", "OWNER_STATED")]
    assert meta["rows"][1]["supersedes_quantity_id"] == meta["rows"][0]["quantity_id"]
    blob = json.dumps(meta)
    for forbidden in ("title", "note", "label", "statement", "Recorded by", "Target value",
                      "replaced", "withdrawn", PROBLEM_ANSWER[:20]):
        assert forbidden not in blob
    assert json.loads(blob) == meta


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
    assert 'id="t2a-confirm"' not in _page(c, sid)
    assert _confirm(c, sid, token).status_code == 302
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
    assert _rows(db_path, sid) == []


def test_stale_quantity_head_between_propose_and_confirm_is_refused_in_the_transaction(db_path):
    c, aid = _client_for("t2a-stale-head@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "5 V").status_code == 302
    assert _propose(c, sid, "rec_1", "6 V").status_code == 302
    entry = SESSION_STORE[sid]
    stale = dict(entry["quantity_proposal"])
    stale_token = _ctoken(_page(c, sid))
    assert _record(c, sid, "rec_1", "7 V").status_code == 302
    entry["quantity_proposal"] = stale
    assert _confirm(c, sid, stale_token).status_code == 302
    # An established refusal decided before any row was written: it may say
    # that nothing changed, and it says WHY rather than only "not saved".
    assert webapp.QUANTITY_CONFLICT_MESSAGE in _page(c, sid)
    assert [x[5] for x in _rows(db_path, sid)] == ["5 V", "7 V"]
    assert _values(_page(c, sid)) == ["7 V"]


def test_identical_value_to_the_active_head_stages_nothing(db_path):
    c, _aid = _client_for("t2a-same@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "7 V").status_code == 302
    assert _propose(c, sid, "rec_1", " 7 V ").status_code == 302
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
    assert len({x[7] for x in rows}) == 3
    body = _page(c, sid)
    assert _values(body) == ["9 V"] and _replaced(body) == ["7 V", "8 V"]
    assert ui_text.text("UI_T2A_REPLACED", "en") in body
    html = c.get(DELIVERABLE % sid).get_data(as_text=True)
    assert _values(html) == ["9 V"] and _replaced(html) == ["7 V", "8 V"]


def test_another_projects_anchor_and_history_are_isolated(db_path):
    ca, _a = _client_for("t2a-iso-a@example.com")
    sid_a = _start(ca)
    cb, _b = _client_for("t2a-iso-b@example.com")
    sid_b = _start(cb, answers=(PROBLEM_ANSWER,))
    assert _propose(cb, sid_b, "rec_2").status_code == 302
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
        key = "UI_T2A_KIND_" + kind.upper()
        assert 'value="%s"' % kind in body and ui_text.text(key, "en") in body
        assert ui_text.text(key, "ar") != key and ui_text.text(key, "en") != key
    assert 'id="answer-form"' in body and "/correct" in body
    assert len(set(re.findall(r'name="csrf_token" value="([^"]+)"', body))) == 1
    block = body.split('<details id="t2a-quantities"', 1)[1].split("</details>", 1)[0]
    for word in ("feasib", "attainab", "validated", "verified", "safe", "compliant"):
        if word in block.lower():
            assert "not" in block.lower()


def test_user_statement_and_value_text_are_escaped_inside_the_quantity_block(db_path):
    c, _aid = _client_for("t2a-escape@example.com")
    sid = _start(c, answers=(HTML_ANSWER,))
    assert _record(c, sid, "rec_1", "<b>5</b> V").status_code == 302
    body = _page(c, sid)
    block = body.split('<details id="t2a-quantities"', 1)[1].split("</details>", 1)[0]
    assert "<b>board</b>" not in block and "&lt;b&gt;board&lt;/b&gt;" in block
    assert "<b>5</b>" not in block and "&lt;b&gt;5&lt;/b&gt; V" in block
    html = c.get(DELIVERABLE % sid).get_data(as_text=True)
    assert "<b>5</b>" not in html and "&lt;b&gt;5&lt;/b&gt; V" in html


def test_html_deliverable_and_pdf_present_current_replaced_and_withdrawn_read_only(
        db_path, monkeypatch):
    c, _aid = _client_for("t2a-deliv@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "12.5 V").status_code == 302
    assert _record(c, sid, "rec_1", "14 V").status_code == 302
    assert _record(c, sid, "rec_2", "3 to 5 A", "range").status_code == 302
    assert c.post(CORRECT % sid, data={"supersedes_record_id": "rec_2",
                                       "response": MECH_CORRECTED,
                                       "answer_token": _token(c, sid)}).status_code == 302
    html = c.get(DELIVERABLE % sid).get_data(as_text=True)
    assert 'id="t2a-requirement-quantities"' in html
    for key in ("UI_T2A_DELIV_HEADING", "UI_T2A_DISCLAIMER", "UI_T2A_STATUS_UNVALIDATED",
                "UI_T2A_REPLACED", "UI_T2A_WITHDRAWN_ANCHOR", "UI_T2A_WITHDRAWN_NOTE",
                "UI_T2A_KIND_TARGET_VALUE", "UI_T2A_KIND_RANGE"):
        assert ui_text.text(key, "en") in html, key
    assert PROBLEM_ANSWER in html and MECH_STRONG in html      # statements (withdrawn one retained)
    assert _values(html) == ["14 V"] and _replaced(html) == ["12.5 V"]
    assert _withdrawn(html) == ["3 to 5 A"]
    for forbidden in ("qty-", "anchor_withdrawn", "req:assertion", "UNVALIDATED", "OWNER_STATED",
                      "event_key", "recorded_at"):
        assert forbidden not in html, forbidden
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
    meta = _package(sid)["_session_meta"]["requirement_quantities"]
    assert meta["total"] == 3
    assert [(r["active"], r["anchor_active"]) for r in meta["rows"]] == [
        (False, True), (True, True), (True, False)]


def test_arabic_and_english_chrome_parity_with_never_localized_value_text(db_path):
    c, _aid = _client_for("t2a-ar@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "3.75 kg", KIND2).status_code == 302
    en = _page(c, sid)
    assert c.post("/ui-language", data={"lang": "ar"}).status_code in (302, 303)
    ar = _page(c, sid)
    for key in ("UI_T2A_HEADING", "UI_T2A_EXPLAIN", "UI_T2A_CURRENT", "UI_T2A_KIND_LABEL",
                "UI_T2A_VALUE_LABEL", "UI_T2A_REPLACE_BUTTON", "UI_T2A_STATUS_UNVALIDATED",
                "UI_T2A_KIND_MAXIMUM_VALUE"):
        assert ui_text.text(key, "en") in en and ui_text.text(key, "ar") in ar, key
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
    assert ui_text.text("UI_T2A_REPLACED", "ar") in ar and _replaced(ar) == ["3.75 kg"]
    html = c.get(DELIVERABLE % sid).get_data(as_text=True)
    assert ui_text.text("UI_T2A_DELIV_HEADING", "ar") in html and "4 kg" in html
    assert ui_text.text("UI_T2A_DISCLAIMER", "ar") in html
    assert _propose(c, sid, "rec_1", "").status_code == 302
    ar = _page(c, sid)
    assert ui_text.localize_message(webapp.QUANTITY_INVALID_MESSAGE, "ar") in ar
    assert webapp.QUANTITY_INVALID_MESSAGE not in ar
    assert ui_text.localize_deep(webapp.QUANTITY_DISCARDED_ACK, "ar") != webapp.QUANTITY_DISCARDED_ACK


def test_zero_rows_leave_package_html_and_pdf_source_byte_identical(db_path, monkeypatch):
    """CR-5: with zero quantity rows the candidate's HTML and PDF source are
    byte-identical to the BASE source — the report template with the T2-A
    addition textually removed — not to the candidate with its helpers turned
    off. The only permitted volatile field, ``generated_at``, is pinned."""
    c, _aid = _client_for("t2a-zero@example.com")
    sid = _start(c)
    monkeypatch.setattr(_assembler, "_now_iso", lambda: "2026-01-01T00:00:00+00:00")
    seen = _capture_pdf_source(monkeypatch)
    candidate_html = c.get(DELIVERABLE % sid).get_data()
    assert c.post(PDF % sid, data={}).status_code == 200
    candidate_source = seen["source"]
    candidate_package = _package(sid)
    # Render the SAME route, the SAME context and the SAME data through the base
    # report source: only the template text differs, and it differs by exactly
    # the T2-A addition between the two sentinels.
    with _base_deliverable_template():
        base_html = c.get(DELIVERABLE % sid).get_data()
        assert c.post(PDF % sid, data={}).status_code == 200
        base_source = seen["source"]
    assert candidate_html == base_html
    assert candidate_source == base_source
    assert "requirement_quantities" not in candidate_package["_session_meta"]
    assert json.dumps(candidate_package, sort_keys=True) == json.dumps(
        _assembler.assemble_deliverable(SESSION_STORE[sid]["state"]), sort_keys=True)
    assert "t2a-requirement-quantities" not in candidate_html.decode("utf-8")
    assert "t2a-requirement-quantities" not in candidate_source
    # The same base source DOES differ once a quantity exists — proving the
    # comparison above is a real equivalence, not a vacuous one.
    assert _record(c, sid, _anchors(c, sid)[0], "5 V").status_code == 302
    with_rows = c.get(DELIVERABLE % sid).get_data()
    with _base_deliverable_template():
        assert c.get(DELIVERABLE % sid).get_data() != with_rows


# ==========================================================================
# 8. Cold load, resume, migration
# ==========================================================================
def test_cold_load_restores_history_on_every_surface_and_refuses_cold_writes(db_path, monkeypatch):
    c, _aid = _client_for("t2a-cold@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "42 pieces", "count").status_code == 302
    assert _record(c, sid, "rec_1", "43 pieces", "count").status_code == 302
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
    assert _propose(c, sid, "rec_1", "44 pieces", "count").status_code == 302
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in _page(c, sid)
    assert [x[5] for x in _rows(db_path, sid)] == ["42 pieces", "43 pieces"]
    assert c.post("/session/%s/resume" % sid, data={}).status_code == 302
    assert [q.value_text for q in SESSION_STORE[sid]["state"].requirement_quantities] == [
        "42 pieces", "43 pieces"]
    assert _record(c, sid, "rec_1", "44 pieces", "count").status_code == 302
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
        idx = {r[1] for r in conn.execute("PRAGMA index_list(requirement_quantities)")}
        assert {"requirement_quantities_chain_root_uq", "requirement_quantities_anchor_idx",
                "requirement_quantities_event_key_uq", "requirement_quantities_seq_uq",
                "requirement_quantities_supersedes_uq"} <= idx
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
    assert _confirm(c, sid, token).status_code == 302
    assert SESSION_STORE[sid].get("_answer_error") == webapp.QUANTITY_NOT_SAVED_MESSAGE
    assert _rows(db_path, sid) == before_rows
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
    from engine.requirement_quantity import RequirementQuantity
    head = None
    for i in range(MAX_REQUIREMENT_QUANTITIES_PER_PROJECT - 1):
        q = RequirementQuantity(store.new_quantity_id(), -1, "rec_1", "req:assertion:rec_1",
                                KIND, "v %d" % i, head, "%032x" % i, 1,
                                "2026-09-11T12:00:00+00:00")
        store.append_requirement_quantity(sid, q)
        head = q.quantity_id
    assert len(_rows(db_path, sid)) == 199
    assert _record(c, sid, "rec_1", "row 200").status_code == 302
    assert webapp.QUANTITY_SAVED_ACK in _page(c, sid)
    assert len(_rows(db_path, sid)) == 200
    assert _record(c, sid, "rec_1", "row 201").status_code == 302
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
    meta = _package(sid)["_session_meta"]["requirement_quantities"]
    assert [(i["value_text"], i["active"], i["anchor_active"]) for i in meta["rows"]] == [
        ("5 V", True, True), ("7 A", True, False)]
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
# 10b. CR-1 — anchor integrity: an unresolvable anchor is never withdrawn history
# ==========================================================================
def _repoint_anchor(db_path, sid, anchor):
    """Durable corruption injection: repoint the stored anchor. A plain
    connection has foreign keys OFF, which is exactly how a real corrupted or
    partially restored database can carry a row no constraint would accept."""
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("UPDATE requirement_quantities SET anchor_record_id = ?, "
                     "requirement_id = ? WHERE project_id = ?",
                     (anchor, "req:assertion:" + anchor, sid))
        conn.commit()
    finally:
        conn.close()


def test_unresolvable_anchor_never_renders_as_withdrawn_history(db_path):
    """CR-1: a quantity whose anchor does not resolve to a valid answered
    assertion record must FAIL CLOSED through the established generic recovery
    behaviour on every affected surface — never appear as a legitimate
    withdrawn-answer value, which is how a real withdrawal is presented."""
    c, _aid = _client_for("t2a-anchor-invalid@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "5 V").status_code == 302
    _repoint_anchor(db_path, sid, "rec_99")
    corrupted = _rows(db_path, sid)
    SESSION_STORE.clear()
    with pytest.raises(QuantityHistoryError):
        _store().load_requirement_quantities(sid)
    for verb, path in (("get", SESSION % sid), ("get", DELIVERABLE % sid), ("post", PDF % sid)):
        r = getattr(c, verb)(path, data={})
        assert r.status_code == 302 and r.headers["Location"].endswith("/"), (verb, path)
        text = r.get_data(as_text=True)
        assert "5 V" not in text and "rec_99" not in text and "qty-" not in text
        assert "withdrawn" not in text.lower() and "sqlite" not in text.lower()
    assert _rows(db_path, sid) == corrupted       # retained, never repaired or deleted
    # A GENUINE withdrawal, by contrast, still presents as withdrawn history.
    _repoint_anchor(db_path, sid, "rec_2")
    repointed = _rows(db_path, sid)
    SESSION_STORE.clear()
    assert _values(_page(c, sid)) == ["5 V"]
    token = webapp._issue_answer_token(sid)
    assert c.post(CORRECT % sid, data={"supersedes_record_id": "rec_2",
                                       "response": MECH_CORRECTED,
                                       "answer_token": token}).status_code == 302
    assert _withdrawn(_page(c, sid)) == ["5 V"]
    assert _rows(db_path, sid) == repointed


def test_an_unresolvable_anchor_never_leaks_across_projects(db_path):
    """CR-1: anchor resolution is project-scoped — another owner's project is
    untouched by a corrupt anchor and keeps working normally."""
    ca, _a = _client_for("t2a-anchor-iso-a@example.com")
    cb, _b = _client_for("t2a-anchor-iso-b@example.com")
    sid_a, sid_b = _start(ca), _start(cb)
    assert _record(ca, sid_a, "rec_1", "5 V").status_code == 302
    assert _record(cb, sid_b, "rec_1", "9 A").status_code == 302
    _repoint_anchor(db_path, sid_a, "rec_99")
    SESSION_STORE.pop(sid_a, None)
    assert ca.get(SESSION % sid_a).status_code == 302          # A fails closed
    assert _values(_page(cb, sid_b)) == ["9 A"]                # B is unaffected
    assert _record(cb, sid_b, "rec_2", "4 V", KIND2).status_code == 302
    assert sorted(_values(_page(cb, sid_b))) == ["4 V", "9 A"]
    assert len(_rows(db_path, sid_b)) == 2 and len(_rows(db_path, sid_a)) == 1


# ==========================================================================
# 10c. CR-3 — propose-time session binding
# ==========================================================================
def test_a_second_session_of_the_same_owner_cannot_obtain_or_use_a_token(db_path):
    """CR-3: the binding is recorded at PROPOSE time and the token is built
    from it, so a different browser session of the SAME account is neither
    handed a valid token nor able to spend the staged proposal. Zero durable
    writes, and the staging session's proposal survives intact."""
    first, _aid = _client_for("t2a-second-session@example.com")
    sid = _start(first)
    assert _propose(first, sid, "rec_1", "7 V").status_code == 302
    staged = dict(SESSION_STORE[sid]["quantity_proposal"])
    good_token = _ctoken(_page(first, sid))
    assert good_token
    second = _new_client()                       # same account, new browser session
    second.post("/login", data={"email": "t2a-second-session@example.com", "password": PW})
    body = _page(second, sid)
    # No confirmation block, and therefore no token, is offered to session B.
    assert _ctoken(body) is None and 'id="t2a-confirm"' not in body
    # Even handed session A's token, session B cannot confirm and consumes nothing.
    assert _confirm(second, sid, good_token).status_code == 302
    assert SESSION_STORE[sid].get("_answer_error") == webapp.QUANTITY_NOT_SAVED_MESSAGE
    assert _rows(db_path, sid) == []
    assert SESSION_STORE[sid]["quantity_proposal"] == staged
    # The staging session still completes normally — nothing was spent.
    assert _confirm(first, sid, good_token).status_code == 302
    assert [r[5] for r in _rows(db_path, sid)] == ["7 V"]
    assert SESSION_STORE[sid].get("_interaction_ack") == webapp.QUANTITY_SAVED_ACK


# ==========================================================================
# 10d. CR-2 — truthful durable write outcomes (fault injection)
# ==========================================================================
def _staged_confirm(client, sid, value="7 V", anchor="rec_1"):
    assert _propose(client, sid, anchor, value).status_code == 302
    token = _ctoken(_page(client, sid))
    assert token
    return token


def test_failure_before_commit_reports_an_established_non_write(db_path, monkeypatch):
    """The write never reached the database: the durable absence is PROVEN, so
    saying that nothing was changed is truthful."""
    c, _aid = _client_for("t2a-precommit@example.com")
    sid = _start(c)
    token = _staged_confirm(c, sid)
    store = _store()
    monkeypatch.setattr(store, "append_requirement_quantity",
                        lambda pid, q: (_ for _ in ()).throw(
                            sqlite3.OperationalError("database is locked")))
    assert _confirm(c, sid, token).status_code == 302
    assert SESSION_STORE[sid].get("_answer_error") == webapp.QUANTITY_NOT_SAVED_MESSAGE
    assert _rows(db_path, sid) == []
    monkeypatch.undo()
    assert _values(_page(c, sid)) == []


def test_a_durable_append_followed_by_an_exception_is_reported_as_saved(db_path, monkeypatch):
    """CR-2: a COMPLETED write must never be reported as a non-write. The
    outcome is resolved through the stable event key before anything is said."""
    c, _aid = _client_for("t2a-postcommit@example.com")
    sid = _start(c)
    token = _staged_confirm(c, sid)
    store = _store()
    real = store.append_requirement_quantity

    def append_then_fail(pid, q):
        real(pid, q)                                   # the row IS committed
        raise sqlite3.OperationalError("connection lost after commit")
    monkeypatch.setattr(store, "append_requirement_quantity", append_then_fail)
    assert _confirm(c, sid, token).status_code == 302
    assert [r[5] for r in _rows(db_path, sid)] == ["7 V"]
    assert SESSION_STORE[sid].get("_answer_error") is None
    assert SESSION_STORE[sid].get("_interaction_ack") == webapp.QUANTITY_SAVED_ACK
    monkeypatch.undo()
    body = _page(c, sid)
    assert _values(body) == ["7 V"]
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE not in body


def test_a_genuinely_unknown_commit_outcome_reports_uncertainty(db_path, monkeypatch):
    """CR-2: when the durable outcome cannot be determined at all, the message
    asserts NEITHER a rollback nor a non-write — it says only what is known."""
    c, _aid = _client_for("t2a-unknown@example.com")
    sid = _start(c)
    token = _staged_confirm(c, sid)
    store = _store()
    real = store.append_requirement_quantity

    real_lookup = store.requirement_quantity_for_event_key
    committed = {"done": False}

    def append_then_fail(pid, q):
        real(pid, q)                                   # the row IS committed
        committed["done"] = True
        raise sqlite3.OperationalError("disk I/O error")

    def unreadable(pid, key):
        if committed["done"]:                          # the RESOLUTION attempt
            raise sqlite3.OperationalError("disk I/O error")
        return real_lookup(pid, key)
    monkeypatch.setattr(store, "append_requirement_quantity", append_then_fail)
    monkeypatch.setattr(store, "requirement_quantity_for_event_key", unreadable)
    assert _confirm(c, sid, token).status_code == 302
    message = SESSION_STORE[sid].get("_answer_error")
    assert message == webapp.QUANTITY_OUTCOME_UNKNOWN_MESSAGE
    assert "Nothing was changed" not in message and "not saved" not in message
    assert [r[5] for r in _rows(db_path, sid)] == ["7 V"]       # it WAS committed
    monkeypatch.undo()
    assert _values(_page(c, sid)) == ["7 V"]


def test_stable_event_key_resolution_proves_absence_before_claiming_one(db_path, monkeypatch):
    """CR-2: resolution through the stable project/event key distinguishes a
    proven absence from an undetermined outcome, and reads only this project."""
    c, _aid = _client_for("t2a-resolve@example.com")
    sid = _start(c)
    token = _staged_confirm(c, sid)
    store = _store()
    seen = []
    real_lookup = store.requirement_quantity_for_event_key

    def watching(pid, key):
        seen.append(pid)
        return real_lookup(pid, key)
    monkeypatch.setattr(store, "requirement_quantity_for_event_key", watching)
    monkeypatch.setattr(store, "append_requirement_quantity",
                        lambda pid, q: (_ for _ in ()).throw(RuntimeError("opaque")))
    assert _confirm(c, sid, token).status_code == 302
    # The resolution ran, read only this project, proved absence, and the
    # message reports the proven non-write rather than an unknown outcome.
    assert seen == [sid]
    assert SESSION_STORE[sid].get("_answer_error") == webapp.QUANTITY_NOT_SAVED_MESSAGE
    assert _rows(db_path, sid) == []


def test_commit_then_reload_failure_says_saved_but_not_shown(db_path, monkeypatch):
    """CR-7: persistence succeeded and reattachment failed. The wording is
    quantity-specific and truthful — never the answer-correction message."""
    c, _aid = _client_for("t2a-reload@example.com")
    sid = _start(c)
    token = _staged_confirm(c, sid)
    store = _store()
    def gone(pid):                             # armed for the post-commit reload
        raise sqlite3.OperationalError("gone after commit")
    monkeypatch.setattr(store, "load_requirement_quantities", gone)
    assert _confirm(c, sid, token).status_code == 302
    message = SESSION_STORE[sid].get("_answer_error")
    assert message == webapp.QUANTITY_SAVED_NOT_SHOWN_MESSAGE
    assert message != webapp.CORRECTION_SAVED_NOT_YET_APPLIED_MESSAGE
    assert message != webapp.QUANTITY_NOT_SAVED_MESSAGE
    assert "saved" in message and "Nothing was changed" not in message
    assert [r[5] for r in _rows(db_path, sid)] == ["7 V"]       # durably saved
    assert ui_text.localize_message(message, "ar") != message   # Arabic exists
    assert ui_text.localize_message(message, "en") == message
    monkeypatch.undo()
    SESSION_STORE.clear()
    assert _values(_page(c, sid)) == ["7 V"]                    # visible next load


@pytest.mark.parametrize("message_attr", [
    "QUANTITY_NOT_SAVED_MESSAGE", "QUANTITY_INVALID_MESSAGE",
    "QUANTITY_CONFLICT_MESSAGE", "QUANTITY_OUTCOME_UNKNOWN_MESSAGE",
    "QUANTITY_SAVED_NOT_SHOWN_MESSAGE",
])
def test_every_outcome_message_is_bilingual_and_non_disclosing(message_attr):
    """CR-2 / CR-7: every outcome message exists in English and Arabic and
    never exposes SQL text, a path, a token, an identifier or a raw value."""
    message = getattr(webapp, message_attr)
    assert ui_text.localize_message(message, "en") == message
    arabic = ui_text.localize_message(message, "ar")
    assert arabic != message and arabic.strip()
    for forbidden in ("SELECT", "INSERT", "sqlite", "Traceback", "/", "qty-", "rec_",
                      "event_key", "Exception", "None"):
        assert forbidden not in message, (message_attr, forbidden)


def test_page_state_and_outcome_message_never_contradict_each_other(db_path, monkeypatch):
    """CR-2: whatever is shown and whatever is said must agree. A saved value is
    never accompanied by a non-write claim, and a proven non-write never shows a
    value the project does not hold."""
    c, _aid = _client_for("t2a-consistent@example.com")
    sid = _start(c)
    # 1. saved -> the value is shown and nothing claims a non-write
    assert _record(c, sid, "rec_1", "5 V").status_code == 302
    body = _page(c, sid)
    assert _values(body) == ["5 V"]
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE not in body
    assert webapp.QUANTITY_OUTCOME_UNKNOWN_MESSAGE not in body
    # 2. proven non-write -> the page still shows only what the project holds
    token = _staged_confirm(c, sid, "6 V")
    store = _store()
    monkeypatch.setattr(store, "append_requirement_quantity",
                        lambda pid, q: (_ for _ in ()).throw(
                            sqlite3.OperationalError("database is locked")))
    assert _confirm(c, sid, token).status_code == 302
    monkeypatch.undo()
    body = _page(c, sid)
    assert webapp.QUANTITY_NOT_SAVED_MESSAGE in body
    assert _values(body) == ["5 V"] and "6 V" not in body
    assert [r[5] for r in _rows(db_path, sid)] == ["5 V"]


# ==========================================================================
# 11. Boundary: routes, no API / export / adapter change
# ==========================================================================
def test_route_inventory_and_untouched_api_export_adapter_surfaces():
    rules = {r.rule: r.methods - {"HEAD", "OPTIONS"} for r in app.url_map.iter_rules()
             if "quantity" in r.rule}
    assert rules == {"/session/<sid>/quantity/propose": {"POST"},
                     "/session/<sid>/quantity/confirm": {"POST"}}
    assert not webapp._quantity_write_authorized("no-such-project")
    # CR-6: repository-independent source inspection — no `git`, no subprocess
    # and no `.git` directory, so this proof holds in a plain source archive as
    # well as in a checkout.
    root = os.path.join(os.path.dirname(__file__), "..")
    for path in ("engine/read_export_service.py", "engine/export_adapter.py", "web/api_v1.py",
                 "tests/test_p7_i2_public_api.py", "engine/deliverable_assembler.py"):
        text = open(os.path.join(root, path), encoding="utf-8").read()
        assert "requirement_quantit" not in text and "quantity_kind" not in text, path
        assert "t2a" not in text.lower() and "quantity" not in text.lower(), path


def test_recorded_quantities_never_reach_the_api_export_or_adapter_surfaces(db_path):
    """CR-6: the changed-surface guarantee proved on LIVE data rather than on a
    diff — a project that really holds quantities exposes none of them through
    the canonical read/export seam, the export adapter or the public API."""
    from engine import export_adapter as _adapter
    from engine import read_export_service as _read_export
    c, aid = _client_for("t2a-surface@example.com")
    sid = _start(c)
    assert _record(c, sid, "rec_1", "12.5 V").status_code == 302
    assert _values(_page(c, sid)) == ["12.5 V"]                 # really recorded
    assert [r[5] for r in _rows(db_path, sid)] == ["12.5 V"]
    state = SESSION_STORE[sid]["state"]
    assert state.requirement_quantities                          # carrier populated
    store = _store()
    read = _read_export.get_authorized_project_read(store, sid, aid)
    export = _read_export.produce_project_export(store, sid, aid)
    adapted = _adapter.ReferenceExportAdapter().transform(export)
    payloads = [json.dumps(x, sort_keys=True, default=str)
                for x in (read, export, adapted,
                          _assembler.assemble_deliverable(state))]
    browser = c.get("/account/projects/%s/export" % sid)
    assert browser.status_code == 200, browser.status_code
    payloads.append(browser.get_data(as_text=True))
    for payload in payloads:
        assert "12.5 V" not in payload
        assert "requirement_quantit" not in payload
        assert "quantity_kind" not in payload
