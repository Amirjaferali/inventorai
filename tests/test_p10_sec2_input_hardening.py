"""P10-SEC2 — Bounded Input-Hardening (RED/GREEN).

Behaviour-based tests for the Owner-authorized bounded Phase-10 gate
`P10-SEC2 — Bounded Input-Hardening Increment`:

  1. one transport bound — Flask ``MAX_CONTENT_LENGTH`` (128 KiB) → HTTP 413
     for pathological request bodies on every surface;
  2. one semantic free-text bound — ``MAX_FREE_TEXT_CHARS`` (20,000 chars) on
     the two primary free-text surfaces (`/start` idea text and the
     `/session/<sid>` answer/action text), rejected EXPLICITLY (form error
     page 400 at /start per its existing error convention; the existing
     plain-text-tuple 400 convention at the session route) — NEVER silently
     truncated;
  3. NUL policy: REJECT — a ``\\x00`` byte in these free-text fields is not
     valid product content and is rejected with the same explicit semantics
     (never stripped, never normalized, never a 500).

Load-bearing preservation proven here: legitimate Arabic / Unicode /
multiline / punctuation-rich input is untouched; exactly-at-limit input is
accepted; rejected input causes NO durable mutation; auth/CSRF semantics are
unchanged; every rejection (including 413) carries the authoritative
P10-SEC1 security headers and no HSTS.

JSON/API-body hardening is JUSTIFIED N/A: the public API (web/api_v1.py) is
GET-only — no JSON or file-upload input surface exists in the application.
"""
import hashlib
import os
import re

import pytest

import web.app as webapp
from web.app import app
from engine import account_credentials as _acct

from test_p4_1b2a_durable_answer_append import answered_post

PW = "correct horse battery staple"
NOW = "2026-01-01T00:00:00.000000Z"
IDEA = ("An electronic circuit uses a sensor and a switch to cut the power "
        "when the current gets too high.")
LIMIT = 20000          # must equal webapp.MAX_FREE_TEXT_CHARS once implemented
ARABIC = ("دائرة إلكترونية تستخدم حسّاسًا ومفتاحًا لقطع التيار عند ارتفاعه؛ "
          "يتضمن التصميم مقاومة ومكثفًا،\nوسطرًا ثانيًا للوصف.")


@pytest.fixture
def db_path():
    return os.environ["INVENTORAI_DB_PATH"]


def _new_client():
    app.config["TESTING"] = True
    return app.test_client()


def _login(email):
    store = webapp._get_account_store()
    aid = "sec2-" + hashlib.sha256(email.encode()).hexdigest()[:10]
    store.create_account(aid, _acct.normalize_email(email),
                         _acct.hash_password(PW), NOW)
    store.mark_email_verified(aid, NOW)
    c = _new_client()
    r = c.post("/login", data={"email": email, "password": PW})
    assert r.status_code == 302
    return c


def _start(client, idea=IDEA):
    return client.post("/start",
                       data={"idea": idea,
                             "domain_confirm": "electronics_electrical"})


def _sid(client, idea=IDEA):
    r = _start(client, idea)
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/session/", 1)[-1]


def _pad_idea(total_chars):
    return IDEA + "x" * (total_chars - len(IDEA))


def _file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def _assert_hardened(response):
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("Content-Security-Policy")
    assert "Strict-Transport-Security" not in response.headers


# ==========================================================================
# Field bound — /start idea text
# ==========================================================================
def test_idea_exactly_at_limit_accepted():
    client = _login("sec2-a@example.com")
    r = _start(client, _pad_idea(LIMIT))
    assert r.status_code == 302          # admitted normally


def test_idea_over_limit_rejected_explicitly_no_truncation():
    client = _login("sec2-b@example.com")
    over = _pad_idea(LIMIT + 1)
    r = _start(client, over)
    assert r.status_code == 400          # explicit rejection, never a session
    assert "/session/" not in r.headers.get("Location", "")
    _assert_hardened(r)
    # no silent truncation: no project was created for this account
    store = webapp._get_store()
    assert store.project_ids() == []


def test_idea_null_byte_rejected():
    client = _login("sec2-c@example.com")
    r = _start(client, IDEA + "\x00tail")
    assert r.status_code == 400
    _assert_hardened(r)
    assert webapp._get_store().project_ids() == []


def test_idea_rejection_does_not_echo_raw_input():
    client = _login("sec2-d@example.com")
    marker = "ZZUNIQUEMARKERZZ"
    r = _start(client, _pad_idea(LIMIT + 50).replace("xxxx", marker, 1))
    assert r.status_code == 400
    assert marker not in r.get_data(as_text=True)


# ==========================================================================
# Field bound — /session/<sid> answer text
# ==========================================================================
def test_answer_exactly_at_limit_accepted(db_path):
    client = _login("sec2-e@example.com")
    sid = _sid(client)
    r = answered_post(client, sid, {"response": "y" * LIMIT})
    assert r.status_code in (200, 302)   # normal submission semantics


def test_answer_over_limit_rejected_no_mutation(db_path):
    client = _login("sec2-f@example.com")
    sid = _sid(client)
    before_hash = _file_sha256(db_path)
    before_iter = webapp.SESSION_STORE[sid]["state"].iteration
    r = answered_post(client, sid, {"response": "y" * (LIMIT + 1)})
    assert r.status_code == 400
    _assert_hardened(r)
    assert _file_sha256(db_path) == before_hash            # no durable write
    assert webapp.SESSION_STORE[sid]["state"].iteration == before_iter


def test_answer_null_byte_rejected_no_mutation(db_path):
    client = _login("sec2-g@example.com")
    sid = _sid(client)
    before_hash = _file_sha256(db_path)
    r = answered_post(client, sid, {"response": "valid\x00text"})
    assert r.status_code == 400
    assert _file_sha256(db_path) == before_hash


def test_non_answer_action_text_also_bounded(db_path):
    client = _login("sec2-h@example.com")
    sid = _sid(client)
    before_hash = _file_sha256(db_path)
    r = answered_post(client, sid, {"action": "deferred",   # real action
                                    "response": "y" * (LIMIT + 1)})
    assert r.status_code == 400
    assert _file_sha256(db_path) == before_hash


# ==========================================================================
# Transport bound — whole request body
# ==========================================================================
def test_oversized_request_body_rejected_413_with_headers():
    client = _login("sec2-i@example.com")
    r = client.post("/start", data={"idea": "x" * (256 * 1024),
                                    "domain_confirm": "electronics_electrical"})
    assert r.status_code == 413
    _assert_hardened(r)


def test_normal_requests_unaffected_by_transport_bound():
    client = _login("sec2-j@example.com")
    assert client.get("/").status_code == 200
    assert client.get("/health").status_code == 200
    assert client.get("/account").status_code == 200
    assert _start(client).status_code == 302


# ==========================================================================
# Unicode / Arabic / multiline preservation — MANDATORY
# ==========================================================================
def test_arabic_multiline_answer_preserved_verbatim(db_path):
    client = _login("sec2-k@example.com")
    sid = _sid(client)
    r = answered_post(client, sid, {"response": ARABIC})
    assert r.status_code in (200, 302)
    # stored verbatim in the durable accepted-answer evidence — no stripping,
    # no ASCII coercion, no newline loss
    evidence = webapp._get_store().load_accepted_answer_evidence(sid)
    blob = repr(evidence)
    assert "حسّاسًا" in blob or "\\u062d" in blob.encode(
        "unicode_escape").decode() or ARABIC[:20] in str(evidence)
    flat = str(evidence)
    assert "دائرة إلكترونية" in flat
    assert "وسطرًا ثانيًا" in flat            # second (multiline) segment kept


def test_validation_helper_accepts_legitimate_text_shapes():
    ok = webapp._free_text_error
    lang = "en"
    assert ok(ARABIC, lang) is None
    assert ok("Line one.\nLine two.\tTabbed, punctuated: 50% / #2!", lang) is None
    assert ok("y" * LIMIT, lang) is None
    assert ok("émoji ✅ und Ünïcode", lang) is None
    # and rejects exactly the two hardened conditions
    assert ok("y" * (LIMIT + 1), lang) is not None
    assert ok("bad\x00byte", lang) is not None


# ==========================================================================
# Auth / CSRF / semantics preservation
# ==========================================================================
def test_auth_and_csrf_flows_unchanged():
    client = _login("sec2-l@example.com")
    body = client.get("/account").get_data(as_text=True)
    token = re.search(r'name="csrf_token" value="([^"]+)"', body).group(1)
    r = client.post("/logout", data={"csrf_token": token})
    assert r.status_code == 302
    # login still enforces credentials
    c2 = _new_client()
    r = c2.post("/login", data={"email": "sec2-l@example.com",
                                "password": "wrong password entirely"})
    assert r.status_code in (401, 429)


def test_export_flow_unchanged(db_path):
    client = _login("sec2-m@example.com")
    sid = _sid(client)
    r = client.get("/account/projects/%s/export" % sid)
    assert r.status_code == 200
    assert r.headers["Content-Disposition"].startswith("attachment;")


def test_constants_exposed_and_coherent():
    assert webapp.MAX_FREE_TEXT_CHARS == LIMIT
    # transport bound comfortably covers a worst-case UTF-8 at-limit field
    assert app.config["MAX_CONTENT_LENGTH"] >= LIMIT * 4
    assert app.config["MAX_CONTENT_LENGTH"] == 128 * 1024
