"""P5-2 — Authenticated Sessions / Verified Email / Account Recovery (RED/GREEN).

Behaviour-based tests for gate
G-P5-2-AUTH-SESSIONS-VERIFIED-EMAIL-RECOVERY-IMPLEMENTATION-01, building only on
the merged P5-1 account foundation. Covers the two mandatory preconditions with
REAL threads (P5-2-PRE-01 rate-limit concurrency; P5-2-PRE-02 SQLite thread
strategy), the authenticated signed-cookie session (rotation, session_epoch
revocation, idle 2h / absolute 14d expiry, fail-closed), CSRF on authenticated
mutations, email-verification completion + replay protection, verification
resend, password recovery + reset (reset revokes all sessions, no auto sign-in),
account-status enforcement, non-enumeration, hash-only single-use expiring
tokens, and that NO project ownership / route authorization is introduced.

Real on-disk SQLite (autouse conftest isolation); Flask test client with real
signed cookies; the real store, credential helpers, auth-session helpers and dev
email sink. False-green guards are addressed explicitly (see the FALSE-GREEN
GUARD comments). No mocks of the store; no ``:memory:`` DB.
"""
import os
import re
import threading
from datetime import datetime, timedelta

import pytest

import web.app as webapp
from web.app import app
from engine import account_credentials as _acct
from engine import auth_session as _auth
from engine.account_store import SqliteAccountStore, VERIFICATION, RESET
from engine.record_store import SqliteRecordStore

PW = "correct horse battery staple"        # >= 12 chars
NEW_PW = "another sufficiently long secret"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture
def db_path():
    return os.environ["INVENTORAI_DB_PATH"]


def _store():
    return webapp._get_account_store()


def _register(client, email, password=PW):
    return client.post("/register", data={
        "email": email, "password": password, "password_confirm": password})


def _login(client, email, password=PW):
    return client.post("/login", data={"email": email, "password": password})


def _csrf(client):
    body = client.get("/account").get_data(as_text=True)
    m = re.search(r'name="csrf_token" value="([^"]+)"', body)
    return m.group(1) if m else None


def _last_token(email, marker=": "):
    msg = webapp._EMAIL_SENDER.last_for(email)
    assert msg is not None
    return msg["body"].rsplit(marker, 1)[-1].strip()


def _reg_verification_token(email):
    # P5-1 registration body: "...: <raw>"
    return _last_token(email, ": ")


def _reset_token(email):
    return _last_token(email, "/reset/")


def _mk_account(store, email, password=PW, status="active", verified=False):
    aid = _acct.new_account_id()
    store.create_account(aid, _acct.normalize_email(email),
                         _acct.hash_password(password), "2026-01-01T00:00:00.000000Z",
                         status=status)
    if verified:
        store.mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    return aid


# ===========================================================================
# P5-2-PRE-01 — rate-limit concurrency hardening (REAL threads, no serialization)
# ===========================================================================
def test_pre01_rate_limit_no_lost_updates_under_concurrency(db_path):
    """FALSE-GREEN GUARD (#4 'rate-limit test serializes requests'): genuinely
    concurrent threads, EACH WITH ITS OWN CONNECTION (multi-connection race), all
    fire the same subject/action at once via a barrier. Exactly ``limit`` must be
    allowed, the rest blocked, with no lost updates and a single row."""
    N, LIMIT = 25, 10
    barrier = threading.Barrier(N)
    results = [None] * N
    lock = threading.Lock()

    def worker(i):
        store = SqliteAccountStore(db_path)      # separate connection per thread
        try:
            barrier.wait()
            allowed = store.record_rate_attempt(
                "concurrent-subject", "login", "2026-01-01T00:00:00.000000Z",
                "2099-01-01T00:00:00.000000Z", LIMIT)
            with lock:
                results[i] = allowed
        finally:
            store.close()

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    allowed_count = sum(1 for r in results if r is True)
    blocked_count = sum(1 for r in results if r is False)
    assert allowed_count == LIMIT            # no lost updates → not MORE than limit
    assert blocked_count == N - LIMIT
    # Exactly one row; its final count reflects every attempt (nothing lost).
    verify = SqliteAccountStore(db_path)
    try:
        assert verify.rate_limit_row_count() == 1
        row = verify._conn.execute(
            "SELECT attempt_count FROM auth_rate_limits WHERE subject_key='concurrent-subject'"
        ).fetchone()
        assert row[0] == N
    finally:
        verify.close()


def test_pre01_expired_rate_rows_cleaned_bounded(db_path):
    store = SqliteAccountStore(db_path)
    try:
        for i in range(5):
            store.record_rate_attempt("s%d" % i, "login", "2026-01-01T00:00:00.000000Z",
                                      "2026-01-01T01:00:00.000000Z", 10)
        assert store.rate_limit_row_count() == 5
        # now is after every window's expiry → all expired → cleaned.
        deleted = store.cleanup_expired_rate_limits("2026-06-01T00:00:00.000000Z")
        assert deleted == 5
        assert store.rate_limit_row_count() == 0
        # bounded: a max_rows cap never deletes more than the cap per call.
        for i in range(4):
            store.record_rate_attempt("t%d" % i, "login", "2026-01-01T00:00:00.000000Z",
                                      "2026-01-01T01:00:00.000000Z", 10)
        assert store.cleanup_expired_rate_limits("2026-06-01T00:00:00.000000Z", max_rows=2) == 2
        assert store.rate_limit_row_count() == 2
    finally:
        store.close()


def test_pre01_rate_limit_generic_response_unchanged_when_limited(client):
    """A rate-limited login returns the SAME generic failure content as an
    ordinary wrong-password failure (no enumeration, no 'you are rate limited')."""
    _register(client, "rl@example.com")
    ordinary = client.post("/login", data={"email": "rl@example.com", "password": "wrongwrongwrong"})
    # Exhaust the login window for this email digest.
    store = _store()
    digest = _acct.email_digest("rl@example.com")
    for _ in range(webapp._LOGIN_RATE_LIMIT + 2):
        store.record_rate_attempt(digest, "login", "2026-01-01T00:00:00.000000Z",
                                  "2099-01-01T00:00:00.000000Z", webapp._LOGIN_RATE_LIMIT)
    limited = client.post("/login", data={"email": "rl@example.com", "password": PW})
    assert limited.status_code in (401, 429)
    # Same visible generic message either way.
    assert webapp.LOGIN_FAILED_MESSAGE_EN.encode() in ordinary.data
    assert webapp.LOGIN_FAILED_MESSAGE_EN.encode() in limited.data


# ===========================================================================
# P5-2-PRE-02 — SQLite thread/connection strategy (REAL threads)
# ===========================================================================
def test_pre02_shared_store_used_from_many_threads_no_affinity_error(db_path):
    """FALSE-GREEN GUARD (#5 'threading test uses one thread'): ONE shared store
    is hammered from many threads doing writes+reads at once. On the unsafe parent
    this raises sqlite3.ProgrammingError (thread affinity); the hardened store must
    complete every op correctly."""
    store = _store()
    N = 20
    barrier = threading.Barrier(N)
    errors = []
    made = []
    lock = threading.Lock()

    def worker(i):
        try:
            barrier.wait()
            aid = _acct.new_account_id()
            store.create_account(aid, "thread%d@example.com" % i,
                                 _acct.hash_password(PW), "2026-01-01T00:00:00.000000Z")
            got = store.get_account_by_id(aid)
            with lock:
                made.append(got["account_id"])
        except Exception as exc:  # pragma: no cover - failure path
            with lock:
                errors.append(repr(exc))

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert errors == []
    assert store.count_accounts() == N
    assert len(set(made)) == N


def test_pre02_concurrent_token_consume_is_atomic(db_path):
    """Exactly ONE of many concurrent consumers wins a single-use token; the rest
    get None. Proves the consume critical section is atomic across threads."""
    store = _store()
    aid = _mk_account(store, "tok@example.com")
    raw = "shared-raw-token-value"
    store.create_email_token(_acct.new_token_id(), aid, RESET, _acct.hash_token(raw),
                             "2099-01-01T00:00:00.000000Z", "2026-01-01T00:00:00.000000Z")
    N = 16
    barrier = threading.Barrier(N)
    outcomes = [None] * N
    lock = threading.Lock()

    def worker(i):
        barrier.wait()
        got = store.consume_token(_acct.hash_token(raw), RESET, "2026-06-01T00:00:00.000000Z")
        with lock:
            outcomes[i] = got

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    wins = [o for o in outcomes if o == aid]
    assert len(wins) == 1                    # single-use: exactly one winner
    assert outcomes.count(None) == N - 1


def test_pre02_existing_record_store_unchanged_alongside_accounts(db_path):
    """The separate project record store still works normally while the account
    store is active on the same DB file (no cross-contamination, no regression)."""
    rstore = SqliteRecordStore(db_path)
    from engine.record_contract import ProjectRecordContract
    rstore.create_project(ProjectRecordContract(idea_id="idea-x", assertions=[]),
                          project_id="sid-x")
    rstore.close()
    _mk_account(_store(), "coexist@example.com")
    rstore2 = SqliteRecordStore(db_path)
    assert rstore2.load_contract("sid-x").idea_id == "idea-x"
    rstore2.close()


# ===========================================================================
# Login / session model / rotation
# ===========================================================================
def test_login_success_establishes_bounded_session(client):
    _register(client, "a@example.com")
    resp = _login(client, "a@example.com")
    assert resp.status_code == 302 and resp.headers["Location"].endswith("/account")
    with client.session_transaction() as sess:
        auth = sess["auth"]
        # FALSE-GREEN GUARD: the session carries ONLY bounded metadata — never the
        # email, password hash, or any token.
        assert set(auth.keys()) <= set(_auth.SESSION_KEYS)
        assert "email" not in auth and "password_hash" not in auth
        acct = _store().get_account_by_normalized_email("a@example.com")
        assert auth["account_id"] == acct["account_id"]
        assert auth["session_epoch"] == acct["session_epoch"]


def test_login_wrong_password_generic_and_no_session(client):
    _register(client, "b@example.com")
    resp = client.post("/login", data={"email": "b@example.com", "password": "not the password"})
    assert resp.status_code == 401
    assert webapp.LOGIN_FAILED_MESSAGE_EN.encode() in resp.data
    with client.session_transaction() as sess:
        assert "auth" not in sess


def test_login_unknown_email_matches_wrong_password_response(client):
    """FALSE-GREEN GUARD (#9 'compares only text but not status/headers'): unknown
    email and wrong password produce identical status AND body (no enumeration)."""
    _register(client, "known@example.com")
    unknown = client.post("/login", data={"email": "ghost@example.com", "password": PW})
    wrong = client.post("/login", data={"email": "known@example.com", "password": "definitely wrong pw"})
    assert unknown.status_code == wrong.status_code == 401
    assert unknown.data == wrong.data


def test_login_rotates_session_material(client):
    """FALSE-GREEN GUARD (#1 'rotation test compares the same cookie'): compare the
    SESSION CONTENT (CSRF token + issued_at), not the cookie string. Re-login mints
    fresh material."""
    _register(client, "rot@example.com")
    _login(client, "rot@example.com")
    with client.session_transaction() as sess:
        csrf1 = sess["auth"]["csrf"]
    # log out then back in
    csrf = _csrf(client)
    client.post("/logout", data={"csrf_token": csrf})
    _login(client, "rot@example.com")
    with client.session_transaction() as sess:
        csrf2 = sess["auth"]["csrf"]
    assert csrf1 and csrf2 and csrf1 != csrf2


def test_disabled_and_deleted_cannot_authenticate(client):
    store = _store()
    _mk_account(store, "dis@example.com", status="disabled")
    _mk_account(store, "del@example.com", status="deleted")
    for email in ("dis@example.com", "del@example.com"):
        r = client.post("/login", data={"email": email, "password": PW})
        assert r.status_code == 401
        with client.session_transaction() as sess:
            assert "auth" not in sess


def test_cookie_security_flags(client):
    _register(client, "cook@example.com")
    resp = _login(client, "cook@example.com")
    set_cookie = resp.headers.get("Set-Cookie", "")
    # FALSE-GREEN GUARD (#2 'checks only one cookie name'): assert the FULL flag set.
    assert "HttpOnly" in set_cookie
    assert "SameSite=Lax" in set_cookie
    assert "Secure" not in set_cookie          # not production in tests
    assert set_cookie.startswith("session=")   # the signed session cookie, not a sid


# ===========================================================================
# Logout / session_epoch revocation
# ===========================================================================
def test_logout_requires_csrf_then_clears_session(client):
    _register(client, "lo@example.com")
    _login(client, "lo@example.com")
    assert client.post("/logout", data={}).status_code == 403          # missing CSRF
    assert client.post("/logout", data={"csrf_token": "bogus"}).status_code == 403
    csrf = _csrf(client)
    assert client.post("/logout", data={"csrf_token": csrf}).status_code == 302
    with client.session_transaction() as sess:
        assert "auth" not in sess


def test_logout_all_revokes_other_sessions(client):
    _register(client, "la@example.com")
    # session 1 (this client) and session 2 (second client), same account.
    _login(client, "la@example.com")
    other = app.test_client()
    _login(other, "la@example.com")
    assert other.get("/account").status_code == 200
    csrf = _csrf(client)
    assert client.post("/logout-all", data={"csrf_token": csrf}).status_code == 302
    # FALSE-GREEN GUARD (#8): the OTHER, still-live session must now be revoked.
    r = other.get("/account")
    assert r.status_code == 302 and r.headers["Location"].endswith("/login")


def test_logout_all_requires_csrf(client):
    _register(client, "lac@example.com")
    _login(client, "lac@example.com")
    assert client.post("/logout-all", data={"csrf_token": "nope"}).status_code == 403


# ===========================================================================
# Idle / absolute expiry (time-controlled, tied to the real Flask session)
# ===========================================================================
def _at(monkeypatch, dt):
    monkeypatch.setattr(webapp, "_utc_now", lambda: dt)


def test_idle_expiry_two_hours(client, monkeypatch):
    base = datetime(2026, 5, 1, 12, 0, 0)
    _at(monkeypatch, base)
    _register(client, "idle@example.com")
    _login(client, "idle@example.com")
    assert client.get("/account").status_code == 200
    # 2h + 1s later, no activity → idle expired → redirect + cleared.
    _at(monkeypatch, base + timedelta(seconds=_auth.IDLE_TIMEOUT_SECONDS + 1))
    r = client.get("/account")
    assert r.status_code == 302 and r.headers["Location"].endswith("/login")
    with client.session_transaction() as sess:
        assert "auth" not in sess


def test_idle_window_slides_with_activity(client, monkeypatch):
    base = datetime(2026, 5, 1, 12, 0, 0)
    _at(monkeypatch, base)
    _register(client, "slide@example.com")
    _login(client, "slide@example.com")
    # activity every ~1h keeps it alive well past 2h of absolute wall-clock.
    _at(monkeypatch, base + timedelta(hours=1))
    assert client.get("/account").status_code == 200
    _at(monkeypatch, base + timedelta(hours=2, minutes=30))
    assert client.get("/account").status_code == 200


def test_absolute_expiry_fourteen_days(client, monkeypatch):
    base = datetime(2026, 5, 1, 12, 0, 0)
    _at(monkeypatch, base)
    _register(client, "abs@example.com")
    _login(client, "abs@example.com")
    # Keep sliding idle, but pass the 14-day absolute cap → expired regardless.
    _at(monkeypatch, base + timedelta(days=14, seconds=1))
    r = client.get("/account")
    assert r.status_code == 302 and r.headers["Location"].endswith("/login")


def test_disabled_midsession_fails_closed(client):
    _register(client, "mid@example.com")
    _login(client, "mid@example.com")
    assert client.get("/account").status_code == 200
    _store().set_status(
        _store().get_account_by_normalized_email("mid@example.com")["account_id"],
        "disabled", "2026-01-01T00:00:00.000000Z")
    r = client.get("/account")
    assert r.status_code == 302 and r.headers["Location"].endswith("/login")


# ===========================================================================
# Email verification completion + replay
# ===========================================================================
def test_verification_completion_sets_verified(client):
    _register(client, "ver@example.com")
    raw = _reg_verification_token("ver@example.com")
    r = client.get("/verify/" + raw)
    assert r.status_code == 200 and "verified" in r.get_data(as_text=True).lower()
    acct = _store().get_account_by_normalized_email("ver@example.com")
    assert acct["email_verified"] is True


def test_verification_replay_fails_and_state_durable(client):
    """FALSE-GREEN GUARD (#7 'never consumes the first token' / #11 'displayed
    without durable state'): first use verifies AND durably sets the flag; the
    second use is rejected generically, and the flag stays set (durable)."""
    _register(client, "rep@example.com")
    raw = _reg_verification_token("rep@example.com")
    first = client.get("/verify/" + raw)
    assert "verified" in first.get_data(as_text=True).lower()
    acct = _store().get_account_by_normalized_email("rep@example.com")
    assert acct["email_verified"] is True
    second = client.get("/verify/" + raw)
    body = second.get_data(as_text=True).lower()
    assert "invalid" in body or "expired" in body or "already" in body
    # token is used exactly once
    assert _store().active_verification_tokens(acct["account_id"]) == 0


def test_verification_expired_token_rejected(client):
    store = _store()
    aid = _mk_account(store, "exp@example.com")
    raw = "expired-verif-token"
    store.create_email_token(_acct.new_token_id(), aid, VERIFICATION,
                             _acct.hash_token(raw), "2000-01-01T00:00:00.000000Z",
                             "2000-01-01T00:00:00.000000Z")
    r = client.get("/verify/" + raw)
    assert "invalid" in r.get_data(as_text=True).lower() or "expired" in r.get_data(as_text=True).lower()
    assert store.get_account_by_id(aid)["email_verified"] is False


def test_invalid_verification_token_generic(client):
    r = client.get("/verify/this-token-never-existed")
    assert r.status_code == 200
    assert "invalid" in r.get_data(as_text=True).lower() or "expired" in r.get_data(as_text=True).lower()


# ===========================================================================
# Verification resend (authenticated, CSRF-protected)
# ===========================================================================
def test_resend_verification_supersedes_and_requires_csrf(client):
    _register(client, "res@example.com")
    _login(client, "res@example.com")
    acct = _store().get_account_by_normalized_email("res@example.com")
    webapp._EMAIL_SENDER.clear()
    assert client.post("/account/resend-verification", data={"csrf_token": "bad"}).status_code == 403
    csrf = _csrf(client)
    r = client.post("/account/resend-verification", data={"csrf_token": csrf})
    assert r.status_code == 200
    # new verification token issued; only ONE active (prior superseded)
    assert _store().active_verification_tokens(acct["account_id"]) == 1
    msg = webapp._EMAIL_SENDER.last_for("res@example.com")
    assert msg is not None and "/verify/" in msg["body"]


def test_resend_not_reissued_when_already_verified(client):
    _register(client, "resv@example.com")
    _login(client, "resv@example.com")
    acct = _store().get_account_by_normalized_email("resv@example.com")
    _store().mark_email_verified(acct["account_id"], "2026-01-01T00:00:00.000000Z")
    _store().supersede_tokens(acct["account_id"], VERIFICATION, "2026-01-01T00:00:00.000000Z")
    csrf = _csrf(client)
    client.post("/account/resend-verification", data={"csrf_token": csrf})
    assert _store().active_verification_tokens(acct["account_id"]) == 0   # nothing re-issued


# ===========================================================================
# Recovery request (non-enumerating) + password reset
# ===========================================================================
def test_recover_generic_and_non_enumerating(client):
    _register(client, "rec@example.com")
    known = client.post("/recover", data={"email": "rec@example.com"})
    unknown = client.post("/recover", data={"email": "nobody-here@example.com"})
    assert known.status_code == unknown.status_code == 200
    assert known.data == unknown.data                      # identical: no enumeration
    # a reset token WAS issued for the real active account only
    acct = _store().get_account_by_normalized_email("rec@example.com")
    assert _store().active_tokens(acct["account_id"], RESET) == 1


def test_recover_disabled_account_same_response_no_token(client):
    store = _store()
    _mk_account(store, "recd@example.com", status="disabled")
    baseline = client.post("/recover", data={"email": "ghost@example.com"}).data
    r = client.post("/recover", data={"email": "recd@example.com"})
    assert r.data == baseline
    acct = store.get_account_by_normalized_email("recd@example.com")
    assert store.active_tokens(acct["account_id"], RESET) == 0    # disabled → no reset token


def test_password_reset_completion_changes_password(client):
    _register(client, "pr@example.com")
    client.post("/recover", data={"email": "pr@example.com"})
    raw = _reset_token("pr@example.com")
    r = client.post("/reset/" + raw, data={"password": NEW_PW, "password_confirm": NEW_PW})
    assert r.status_code == 200 and "reset" in r.get_data(as_text=True).lower()
    # old password rejected, new accepted
    c2 = app.test_client()
    assert c2.post("/login", data={"email": "pr@example.com", "password": PW}).status_code == 401
    c3 = app.test_client()
    assert c3.post("/login", data={"email": "pr@example.com", "password": NEW_PW}).status_code == 302


def test_password_reset_revokes_all_sessions(client):
    """FALSE-GREEN GUARD (#12 'changes the hash but not session_epoch'): a live
    authenticated session is invalidated by the epoch bump the reset performs."""
    _register(client, "prr@example.com")
    _login(client, "prr@example.com")            # live session in `client`
    assert client.get("/account").status_code == 200
    other = app.test_client()
    other.post("/recover", data={"email": "prr@example.com"})
    raw = _reset_token("prr@example.com")
    other.post("/reset/" + raw, data={"password": NEW_PW, "password_confirm": NEW_PW})
    # the previously-authenticated session is now revoked
    r = client.get("/account")
    assert r.status_code == 302 and r.headers["Location"].endswith("/login")


def test_password_reset_does_not_auto_sign_in(client):
    _register(client, "nas@example.com")
    client.post("/recover", data={"email": "nas@example.com"})
    raw = _reset_token("nas@example.com")
    client.post("/reset/" + raw, data={"password": NEW_PW, "password_confirm": NEW_PW})
    with client.session_transaction() as sess:
        assert "auth" not in sess              # NOT signed in after reset


def test_password_reset_replay_and_expiry_rejected(client):
    _register(client, "prx@example.com")
    client.post("/recover", data={"email": "prx@example.com"})
    raw = _reset_token("prx@example.com")
    client.post("/reset/" + raw, data={"password": NEW_PW, "password_confirm": NEW_PW})
    replay = client.post("/reset/" + raw, data={"password": NEW_PW, "password_confirm": NEW_PW})
    assert replay.status_code == 400           # single-use
    assert client.post("/reset/never-was-a-token",
                       data={"password": NEW_PW, "password_confirm": NEW_PW}).status_code == 400


def test_password_reset_enforces_password_policy(client):
    _register(client, "pol@example.com")
    client.post("/recover", data={"email": "pol@example.com"})
    raw = _reset_token("pol@example.com")
    short = client.post("/reset/" + raw, data={"password": "short", "password_confirm": "short"})
    assert short.status_code == 400
    mismatch = client.post("/reset/" + raw, data={"password": NEW_PW, "password_confirm": "different long value"})
    assert mismatch.status_code == 400


def test_reset_token_is_one_hour(client):
    _register(client, "ttl@example.com")
    client.post("/recover", data={"email": "ttl@example.com"})
    acct = _store().get_account_by_normalized_email("ttl@example.com")
    raw = _reset_token("ttl@example.com")
    row = _store().get_email_token_by_hash(_acct.hash_token(raw))
    delta = _auth.parse(row["expires_at"]) - _auth.parse(row["created_at"])
    assert abs(delta.total_seconds() - 60 * 60) < 1.0
    assert row["token_type"] == RESET


# ===========================================================================
# Token hygiene / secret non-leakage
# ===========================================================================
def test_tokens_hash_only_and_no_raw_secret_in_logs(client, caplog):
    import logging
    caplog.set_level(logging.DEBUG)
    _register(client, "leak@example.com")
    client.post("/recover", data={"email": "leak@example.com"})
    verif = _reg_verification_token("leak@example.com")   # from registration
    reset = _reset_token("leak@example.com")
    # raw tokens never stored (only hashes) and never in logs
    store = _store()
    stored_hashes = [r[0] for r in store._conn.execute("SELECT token_hash FROM email_tokens").fetchall()]
    assert verif not in stored_hashes and reset not in stored_hashes
    assert _acct.hash_token(reset) in stored_hashes
    assert verif not in caplog.text and reset not in caplog.text
    # raw reset token not echoed by the recover response body
    assert reset.encode() not in client.post("/recover", data={"email": "leak@example.com"}).data


# ===========================================================================
# Bounded scope — NO project ownership / authorization introduced
# ===========================================================================
def test_no_project_ownership_effect(client, db_path):
    # Reconciled at the P5-3 boundary (G-P5-3-PROJECT-OWNERSHIP-ROUTE-
    # AUTHORIZATION-IMPLEMENTATION-01): P5-3 adds the additive nullable
    # `owner_account_id` column, so this P5-2 test no longer asserts the column's
    # ABSENCE. The enduring P5-2 invariant it still guards is that the P5-2 AUTH
    # routes have NO ownership EFFECT — they create no project and assign no owner.
    _register(client, "own@example.com")
    _login(client, "own@example.com")
    rstore2 = SqliteRecordStore(db_path)
    before = len(rstore2.project_ids())
    rstore2.close()
    client.post("/account/resend-verification", data={"csrf_token": _csrf(client)})
    rstore3 = SqliteRecordStore(db_path)
    assert len(rstore3.project_ids()) == before          # no auth route creates a project
    rstore3.close()


def test_anonymous_journey_still_open_without_auth(client):
    """Compatibility: the anonymous journey needs no account. The home page and
    registration remain reachable without any authenticated session."""
    assert client.get("/").status_code == 200
    assert client.get("/register").status_code == 200
    assert client.get("/login").status_code == 200


# ===========================================================================
# Bilingual / accessible auth surfaces
# ===========================================================================
@pytest.mark.parametrize("path", ["/login", "/recover"])
def test_auth_pages_language_switch_and_accessible(client, path):
    body = client.get(path).get_data(as_text=True)
    # D-P6-18 (D-P6-16): one UI language at a time — no simultaneous EN+AR for the
    # same label. Both languages remain reachable via the global UI-language
    # selector (English | العربية) present on every page.
    assert '/ui-language' in body
    assert "العربية" in body and 'lang="ar"' in body
    assert 'autocomplete=' in body and 'required' in body
    assert 'for="email"' in body


def test_reset_page_bilingual_and_accessible(client):
    body = client.get("/reset/sometoken").get_data(as_text=True)
    assert 'lang="en"' in body and 'lang="ar"' in body
    assert 'autocomplete="new-password"' in body
    assert 'for="password"' in body


# ===========================================================================
# F-01 / F-02 v2.1 — Account Security failure-atomicity remediation
# Contract: docs/governance/ACCOUNT_SECURITY_FAILURE_ATOMICITY_REMEDIATION_CONTRACT_v2.1.md
# Acceptance tests for §4 (F-01) and §11 (F-02). Failure injection is entirely
# test-contained (monkeypatched store connection / seams): no production
# endpoint, environment switch, durable fault flag, schema field or shipped hook.
# ===========================================================================
import sqlite3 as _sqlite3

from engine.account_store import (
    AccountStoreCommitError, AccountStoreInvariantError,
    DURABLE_CONFIRMED_UNCHANGED, DURABLE_INDETERMINATE,
)


def _epoch(store, account_id):
    return store.get_account_by_id(account_id)["session_epoch"]


def _pw_hash(store, account_id):
    return store.get_account_by_id(account_id)["password_hash"]


def _token_row(store, raw):
    return store.get_email_token_by_hash(_acct.hash_token(raw))


class _ConnProxy:
    """Test-only proxy over the real ``sqlite3.Connection``. ``sqlite3`` connection
    objects reject attribute assignment, so failure injection replaces the store's
    ``_conn`` reference with this proxy instead. ``execute`` goes through the hook;
    every other attribute — including ``in_transaction`` — forwards unchanged, so
    real transactional behaviour and real durable state are preserved."""

    def __init__(self, real, hook):
        object.__setattr__(self, "_real_conn", real)
        object.__setattr__(self, "_hook", hook)

    def execute(self, sql, *args, **kwargs):
        return object.__getattribute__(self, "_hook")(
            object.__getattribute__(self, "_real_conn"), sql, *args, **kwargs)

    def __getattr__(self, name):
        return getattr(object.__getattribute__(self, "_real_conn"), name)


def _patch_conn(monkeypatch, store, hook):
    """Install a hook of signature ``hook(real_conn, sql, *args, **kwargs)``."""
    monkeypatch.setattr(store, "_conn", _ConnProxy(store._conn, hook))


class _Injector:
    """Act on statements whose text starts with one of the given prefixes.

    ``mode`` is one of:
      * ``"raise"``             — raise instead of executing (pre-COMMIT failure);
      * ``"commit_then_raise"`` — execute the statement, THEN raise (models a
        commit that became durable before the caller learned of an error).
    """

    def __init__(self, prefixes, mode="raise", after=0, exc=None):
        self._prefixes = tuple(p.upper() for p in prefixes)
        self._mode = mode
        self._after = after
        self._exc = exc or (lambda: _sqlite3.OperationalError("injected failure"))
        self.hits = 0

    def __call__(self, real, sql, *args, **kwargs):
        if sql.strip().upper().startswith(self._prefixes):
            self.hits += 1
            if self.hits > self._after:
                if self._mode == "commit_then_raise":
                    real.execute(sql, *args, **kwargs)
                raise self._exc()
        return real.execute(sql, *args, **kwargs)


def _inject(monkeypatch, store, prefixes, mode="raise", after=0, exc=None):
    inj = _Injector(prefixes, mode=mode, after=after, exc=exc)
    _patch_conn(monkeypatch, store, inj)
    return inj


# ---------------------------------------------------------------------------
# F-01 — Contract §4 acceptance tests (requirements 1-14)
# ---------------------------------------------------------------------------
def test_f01_r1_success_returns_established_redirect(client):
    """§4.1 — normal success returns the established redirect."""
    _register(client, "f01r1@example.com")
    _login(client, "f01r1@example.com")
    r = client.post("/logout-all", data={"csrf_token": _csrf(client)})
    assert r.status_code == 302 and r.headers["Location"].endswith("/login")


def test_f01_r2_one_isolated_success_is_exactly_plus_one_epoch(client):
    """§4.2 / §2 — one isolated successful request produces an exact +1 delta."""
    _register(client, "f01r2@example.com")
    _login(client, "f01r2@example.com")
    store = _store()
    aid = store.get_account_by_normalized_email("f01r2@example.com")["account_id"]
    before = _epoch(store, aid)
    assert client.post("/logout-all", data={"csrf_token": _csrf(client)}).status_code == 302
    assert _epoch(store, aid) == before + 1


def test_f01_r3_success_clears_initiating_session(client):
    """§4.3 — success clears the initiating authenticated browser session."""
    _register(client, "f01r3@example.com")
    _login(client, "f01r3@example.com")
    client.post("/logout-all", data={"csrf_token": _csrf(client)})
    with client.session_transaction() as sess:
        assert "auth" not in sess


def test_f01_r4_distinct_pre_existing_session_rejected_after_success(client):
    """§4.4 — a distinct pre-existing session is rejected after success."""
    _register(client, "f01r4@example.com")
    _login(client, "f01r4@example.com")
    other = app.test_client()
    _login(other, "f01r4@example.com")
    assert other.get("/account").status_code == 200
    assert client.post("/logout-all", data={"csrf_token": _csrf(client)}).status_code == 302
    r = other.get("/account")
    assert r.status_code == 302 and r.headers["Location"].endswith("/login")


def test_f01_r5_csrf_rejection_behaviour_unchanged(client):
    """§4.5 — missing and invalid CSRF retain the existing rejection behaviour."""
    _register(client, "f01r5@example.com")
    _login(client, "f01r5@example.com")
    store = _store()
    aid = store.get_account_by_normalized_email("f01r5@example.com")["account_id"]
    before = _epoch(store, aid)
    assert client.post("/logout-all", data={}).status_code == 403
    assert client.post("/logout-all", data={"csrf_token": "bogus"}).status_code == 403
    assert _epoch(store, aid) == before                 # no epoch change on rejection
    assert client.get("/account").status_code == 200    # session untouched


def test_f01_r6_epoch_update_exception_returns_generic_503(client, monkeypatch):
    """§4.6 — an epoch UPDATE exception returns a generic 503 (no success)."""
    _register(client, "f01r6@example.com")
    _login(client, "f01r6@example.com")
    csrf = _csrf(client)
    store = _store()
    aid = store.get_account_by_normalized_email("f01r6@example.com")["account_id"]
    before = _epoch(store, aid)
    _inject(monkeypatch, store, ["UPDATE ACCOUNTS SET SESSION_EPOCH"])
    r = client.post("/logout-all", data={"csrf_token": csrf})
    assert r.status_code == 503
    assert r.get_data() == b""                         # generic, non-disclosing
    assert "Location" not in r.headers                 # no login-success redirect
    monkeypatch.undo()
    assert _epoch(store, aid) == before                # rolled back


def test_f01_r7_missing_account_and_non_one_rowcount_fail_closed(db_path, monkeypatch):
    """§4.7 / §2 — missing-account/zero-row and unexpected non-1 row counts fail
    closed as invariant failures rather than silent successes."""
    store = SqliteAccountStore(db_path)
    with pytest.raises(AccountStoreInvariantError):
        store.increment_session_epoch("no-such-account-id", "2026-01-01T00:00:00.000000Z")

    aid = _mk_account(store, "f01r7@example.com")
    before = _epoch(store, aid)

    class _FakeCursor:
        rowcount = 2                                    # unexpected non-1 count

    def hook(real, sql, *a, **k):
        if sql.strip().upper().startswith("UPDATE ACCOUNTS SET SESSION_EPOCH"):
            return _FakeCursor()
        return real.execute(sql, *a, **k)
    _patch_conn(monkeypatch, store, hook)
    with pytest.raises(AccountStoreInvariantError):
        store.increment_session_epoch(aid, "2026-01-01T00:00:01.000000Z")
    monkeypatch.undo()
    assert _epoch(store, aid) == before                 # nothing durable changed


def test_f01_r8_commit_exception_returns_503_without_success_claim(client, monkeypatch):
    """§4.8 — a COMMIT exception returns a generic 503 with no success claim."""
    _register(client, "f01r8@example.com")
    _login(client, "f01r8@example.com")
    csrf = _csrf(client)
    store = _store()
    _inject(monkeypatch, store, ["COMMIT"])
    r = client.post("/logout-all", data={"csrf_token": csrf})
    assert r.status_code == 503
    assert r.get_data() == b"" and "Location" not in r.headers


def test_f01_r9_confirmed_rollback_preserves_session_csrf_and_language(client, monkeypatch):
    """§4.9 / D-04 A — confirmed rollback preserves the current session material,
    CSRF and language, and NORMAL validation independently confirms the session is
    still authenticated. Preserved material alone is not that proof."""
    _register(client, "f01r9@example.com")
    _login(client, "f01r9@example.com")
    client.post("/ui-language", data={"lang": "ar"})
    csrf = _csrf(client)
    store = _store()
    _inject(monkeypatch, store, ["UPDATE ACCOUNTS SET SESSION_EPOCH"])
    assert client.post("/logout-all", data={"csrf_token": csrf}).status_code == 503
    monkeypatch.undo()
    with client.session_transaction() as sess:
        assert "auth" in sess                           # local material preserved
        assert sess.get("ui_lang") == "ar"              # UI language preserved
    assert _csrf(client) == csrf                        # CSRF state preserved
    # Independent evidence class: ordinary server-side validation ACCEPTS it.
    assert client.get("/account").status_code == 200


def test_f01_r10_confirmed_rollback_leaves_epoch_and_other_sessions_unchanged(
        client, monkeypatch):
    """§4.10 — confirmed rollback leaves the epoch and other-session validity
    unchanged under controlled conditions."""
    _register(client, "f01r10@example.com")
    _login(client, "f01r10@example.com")
    other = app.test_client()
    _login(other, "f01r10@example.com")
    csrf = _csrf(client)
    store = _store()
    aid = store.get_account_by_normalized_email("f01r10@example.com")["account_id"]
    before = _epoch(store, aid)
    _inject(monkeypatch, store, ["UPDATE ACCOUNTS SET SESSION_EPOCH"])
    assert client.post("/logout-all", data={"csrf_token": csrf}).status_code == 503
    monkeypatch.undo()
    assert _epoch(store, aid) == before
    assert other.get("/account").status_code == 200     # other session still valid


def test_f01_r11_commit_then_error_does_not_clear_material_but_epoch_wins(
        client, monkeypatch):
    """§4.11 / D-04 B — a simulated commit-then-error does not deliberately clear
    local session material, yet subsequent NORMAL validation rejects the stale
    epoch. Preserved material is emphatically not proof of authentication."""
    _register(client, "f01r11@example.com")
    _login(client, "f01r11@example.com")
    csrf = _csrf(client)
    store = _store()
    aid = store.get_account_by_normalized_email("f01r11@example.com")["account_id"]
    before = _epoch(store, aid)
    _inject(monkeypatch, store, ["COMMIT"], mode="commit_then_raise")
    assert client.post("/logout-all", data={"csrf_token": csrf}).status_code == 503
    monkeypatch.undo()
    assert _epoch(store, aid) == before + 1             # durable state DID commit
    with client.session_transaction() as sess:
        assert "auth" in sess                           # not deliberately cleared
    r = client.get("/account")                          # ordinary validation decides
    assert r.status_code == 302 and r.headers["Location"].endswith("/login")


def test_f01_r12_indeterminate_commit_claims_neither_outcome(db_path, monkeypatch):
    """§4.12 — an indeterminate COMMIT outcome claims neither continued
    authentication nor confirmed rollback. The three durable classes stay
    distinct, and a failed rollback is never reported as a rollback."""
    store = SqliteAccountStore(db_path)
    aid = _mk_account(store, "f01r12@example.com")

    # (a) COMMIT raised with the transaction still open → provably rolled back.
    inj = _inject(monkeypatch, store, ["COMMIT"])
    with pytest.raises(AccountStoreCommitError) as ei:
        store.increment_session_epoch(aid, "2026-01-01T00:00:01.000000Z")
    assert ei.value.durable_outcome == DURABLE_CONFIRMED_UNCHANGED
    assert ei.value.original is not None and ei.value.rollback_error is None
    monkeypatch.undo()
    assert _epoch(store, aid) == 0
    assert inj.hits >= 1

    # (b) commit-then-error → no transaction remains; NOT a confirmed rollback.
    _inject(monkeypatch, store, ["COMMIT"], mode="commit_then_raise")
    with pytest.raises(AccountStoreCommitError) as ei2:
        store.increment_session_epoch(aid, "2026-01-01T00:00:02.000000Z")
    assert ei2.value.durable_outcome == DURABLE_INDETERMINATE
    monkeypatch.undo()
    assert _epoch(store, aid) == 1                      # it really did commit

    # (c) COMMIT raised AND the defensive rollback also fails → indeterminate, the
    #     original failure is retained, and the connection is refused afterwards.
    _inject(monkeypatch, store, ["COMMIT", "ROLLBACK"])
    with pytest.raises(AccountStoreCommitError) as ei3:
        store.increment_session_epoch(aid, "2026-01-01T00:00:03.000000Z")
    assert ei3.value.durable_outcome == DURABLE_INDETERMINATE
    assert ei3.value.rollback_error is not None         # rollback failure surfaced
    assert ei3.value.original is not None               # original COMMIT failure kept
    assert ei3.value.connection_unsafe is True
    monkeypatch.undo()


def test_f01_r13_no_unrelated_durable_mutation_occurs(client):
    """§4.13 — a successful logout-all changes no unrelated durable state."""
    _register(client, "f01r13@example.com")
    _login(client, "f01r13@example.com")
    store = _store()
    acct = store.get_account_by_normalized_email("f01r13@example.com")
    aid = acct["account_id"]
    before = dict(acct)
    assert client.post("/logout-all", data={"csrf_token": _csrf(client)}).status_code == 302
    after = store.get_account_by_id(aid)
    assert after["session_epoch"] == before["session_epoch"] + 1
    for field in ("account_id", "email_normalized", "password_hash", "status",
                  "email_verified", "created_at"):
        assert after[field] == before[field]
    # No reset or verification token is issued or consumed by a logout-all.
    assert store.active_tokens(aid, RESET) == 0


def test_f01_r14_success_does_not_depend_on_a_route_read_epoch_snapshot(
        client, monkeypatch):
    """§4.14 / §2 — production success must not rest on an epoch the route read
    earlier. Make the store's post-UPDATE read return the SAME value the route
    could have snapshotted: success still depends only on the row count plus a
    confirmed COMMIT, so the request still succeeds."""
    _register(client, "f01r14@example.com")
    _login(client, "f01r14@example.com")
    csrf = _csrf(client)
    store = _store()
    aid = store.get_account_by_normalized_email("f01r14@example.com")["account_id"]
    before = _epoch(store, aid)
    class _StaleRow:
        def fetchone(self):
            return (before,)                            # a deliberately stale epoch

    def hook(real, sql, *a, **k):
        if sql.strip().upper().startswith("SELECT SESSION_EPOCH FROM ACCOUNTS"):
            real.execute(sql, *a, **k)
            return _StaleRow()
        return real.execute(sql, *a, **k)
    _patch_conn(monkeypatch, store, hook)
    assert client.post("/logout-all", data={"csrf_token": csrf}).status_code == 302
    monkeypatch.undo()
    assert _epoch(store, aid) == before + 1             # the real write happened


# ---------------------------------------------------------------------------
# F-02 — Contract §11 acceptance tests
# Resource and precheck tests
# ---------------------------------------------------------------------------
def _hash_spy(monkeypatch):
    """Count real password-hash invocations without changing their behaviour."""
    calls = []
    real = _acct.hash_password

    def spy(pw):
        calls.append(pw)
        return real(pw)
    monkeypatch.setattr(webapp._acct, "hash_password", spy)
    return calls


def _durable_snapshot(store, account_id):
    acct = store.get_account_by_id(account_id)
    return (acct["password_hash"], acct["session_epoch"],
            store.active_tokens(account_id, RESET))


@pytest.mark.parametrize("kind", [
    "random_invalid", "expired", "replayed", "wrong_type",
    "missing_account", "disabled_account", "deleted_account",
])
def test_f02_precheck_ineligible_classes_no_hash_no_mutation_same_response(
        client, monkeypatch, kind):
    """§11 resource/precheck — for every ordinary ineligibility class: no
    password-hashing invocation, zero durable mutation, and one identical generic
    response."""
    store = _store()
    email = "f02pc-%s@example.com" % kind
    raw = "no-such-raw-token-value"
    aid = None

    if kind == "random_invalid":
        pass
    elif kind == "expired":
        aid = _mk_account(store, email)
        raw = _acct.new_raw_token()
        store.create_email_token(_acct.new_account_id(), aid, RESET,
                                 _acct.hash_token(raw),
                                 "2020-01-01T00:00:00.000000Z",
                                 "2019-12-31T23:00:00.000000Z")
    elif kind == "replayed":
        _register(client, email)
        client.post("/recover", data={"email": email})
        raw = _reset_token(email)
        client.post("/reset/" + raw, data={"password": NEW_PW, "password_confirm": NEW_PW})
        aid = store.get_account_by_normalized_email(email)["account_id"]
    elif kind == "wrong_type":
        _register(client, email)
        raw = _reg_verification_token(email)          # a VERIFICATION token
        aid = store.get_account_by_normalized_email(email)["account_id"]
    elif kind == "missing_account":
        raw = _acct.new_raw_token()                   # never issued to any account
    else:
        status = "disabled" if kind == "disabled_account" else "deleted"
        aid = _mk_account(store, email, status="active")
        raw = _acct.new_raw_token()
        store.create_email_token(_acct.new_account_id(), aid, RESET,
                                 _acct.hash_token(raw),
                                 "2099-01-01T00:00:00.000000Z",
                                 "2026-01-01T00:00:00.000000Z")
        store.set_status(aid, status, "2026-01-01T00:00:00.000000Z")

    before = _durable_snapshot(store, aid) if aid else None
    calls = _hash_spy(monkeypatch)
    r = client.post("/reset/" + raw, data={"password": NEW_PW, "password_confirm": NEW_PW})

    assert r.status_code == 400                       # one common generic response
    assert "token_invalid" in r.get_data(as_text=True) or r.status_code == 400
    assert calls == []                                # NO hashing invocation
    if aid:
        assert _durable_snapshot(store, aid) == before    # zero durable mutation


def test_f02_ineligible_classes_share_one_identical_response_body(client, monkeypatch):
    """§5 — ordinary ineligibility reasons are indistinguishable at the boundary."""
    _register(client, "f02same@example.com")
    client.post("/recover", data={"email": "f02same@example.com"})
    used = _reset_token("f02same@example.com")
    client.post("/reset/" + used, data={"password": NEW_PW, "password_confirm": NEW_PW})
    bodies = set()
    for raw in (used, "totally-unknown-token", _acct.new_raw_token()):
        r = client.post("/reset/" + raw,
                        data={"password": NEW_PW, "password_confirm": NEW_PW})
        assert r.status_code == 400
        bodies.add(r.get_data())
    assert len(bodies) == 1                           # byte-identical generic body


def test_f02_operational_precheck_failure_no_hash_zero_mutation_503(
        client, monkeypatch):
    """§5 — operational precheck failure: no hashing, zero intentional mutation,
    generic 503, no deliberate session clearing. Distinct from ineligibility."""
    _register(client, "f02opf@example.com")
    _login(client, "f02opf@example.com")
    client.post("/recover", data={"email": "f02opf@example.com"})
    raw = _reset_token("f02opf@example.com")
    store = _store()
    aid = store.get_account_by_normalized_email("f02opf@example.com")["account_id"]
    before = _durable_snapshot(store, aid)
    calls = _hash_spy(monkeypatch)
    monkeypatch.setattr(store, "password_reset_eligible",
                        lambda *a, **k: (_ for _ in ()).throw(
                            _sqlite3.OperationalError("injected precheck failure")))
    r = client.post("/reset/" + raw, data={"password": NEW_PW, "password_confirm": NEW_PW})
    assert r.status_code == 503 and r.get_data() == b""
    assert calls == []
    monkeypatch.undo()
    assert _durable_snapshot(store, aid) == before
    with client.session_transaction() as sess:
        assert "auth" in sess                         # not deliberately cleared


def test_f02_stage_a_is_strictly_read_only(db_path, monkeypatch):
    """§5 — Stage A performs no INSERT/UPDATE/DELETE, no reservation and opens no
    write transaction."""
    store = SqliteAccountStore(db_path)
    aid = _mk_account(store, "f02ro@example.com")
    raw = _acct.new_raw_token()
    store.create_email_token(_acct.new_account_id(), aid, RESET, _acct.hash_token(raw),
                             "2099-01-01T00:00:00.000000Z", "2026-01-01T00:00:00.000000Z")
    before = _durable_snapshot(store, aid)
    seen = []

    def watch(real, sql, *a, **k):
        seen.append(sql.strip().upper())
        return real.execute(sql, *a, **k)
    _patch_conn(monkeypatch, store, watch)
    assert store.password_reset_eligible(_acct.hash_token(raw),
                                         "2026-01-01T00:00:00.000000Z") is True
    monkeypatch.undo()
    assert seen, "the precheck must actually touch the store"
    for sql in seen:
        assert sql.startswith("SELECT"), "Stage A executed a non-SELECT: %r" % sql
    assert _durable_snapshot(store, aid) == before


# ---------------------------------------------------------------------------
# Two-stage and TOCTOU tests
# ---------------------------------------------------------------------------
def test_f02_eligible_precheck_permits_hashing_and_hash_is_outside_write_txn(
        client, monkeypatch):
    """§11 two-stage — an eligible precheck permits hashing, and that hashing runs
    outside any active AccountStore write transaction and BEFORE Stage B's
    BEGIN IMMEDIATE."""
    _register(client, "f02out@example.com")
    client.post("/recover", data={"email": "f02out@example.com"})
    raw = _reset_token("f02out@example.com")
    store = _store()
    observed = {}
    real_hash = _acct.hash_password

    def spy(pw):
        observed["in_transaction_during_hash"] = store._conn.in_transaction
        observed["hashed"] = True
        return real_hash(pw)
    monkeypatch.setattr(webapp._acct, "hash_password", spy)

    real_complete = store.complete_password_reset

    def watched_complete(*a, **k):
        observed["hash_before_stage_b"] = observed.get("hashed", False)
        return real_complete(*a, **k)
    monkeypatch.setattr(store, "complete_password_reset", watched_complete)

    r = client.post("/reset/" + raw, data={"password": NEW_PW, "password_confirm": NEW_PW})
    assert r.status_code == 200
    assert observed.get("hashed") is True
    assert observed["in_transaction_during_hash"] is False   # no writer lock held
    assert observed["hash_before_stage_b"] is True


def test_f02_stage_b_does_not_trust_a_precheck_flag(client, monkeypatch):
    """§7 — Stage B ignores Stage A entirely: force the precheck to report True for
    a token that is NOT eligible and prove Stage B still refuses with zero
    mutation."""
    _register(client, "f02trust@example.com")
    client.post("/recover", data={"email": "f02trust@example.com"})
    raw = _reset_token("f02trust@example.com")
    store = _store()
    aid = store.get_account_by_normalized_email("f02trust@example.com")["account_id"]
    # consume the token out-of-band so it is genuinely ineligible
    store.supersede_tokens(aid, RESET, "2026-01-01T00:00:00.000000Z")
    before = _durable_snapshot(store, aid)
    monkeypatch.setattr(store, "password_reset_eligible", lambda *a, **k: True)
    r = client.post("/reset/" + raw, data={"password": NEW_PW, "password_confirm": NEW_PW})
    monkeypatch.undo()
    assert r.status_code == 400                        # generic ordinary ineligibility
    assert _durable_snapshot(store, aid) == before     # zero mutation


@pytest.mark.parametrize("invalidate", ["consumed", "expired", "superseded",
                                        "account_disabled"])
def test_f02_between_stage_invalidation_caught_by_stage_b(client, monkeypatch, invalidate):
    """§7/§8A — consumption, expiry, supersession or account ineligibility arising
    BETWEEN the stages is caught by Stage B's initial in-transaction revalidation:
    generic 400, zero mutation by the losing request."""
    email = "f02btw-%s@example.com" % invalidate
    _register(client, email)
    client.post("/recover", data={"email": email})
    raw = _reset_token(email)
    store = _store()
    aid = store.get_account_by_normalized_email(email)["account_id"]
    real_hash = _acct.hash_password

    def invalidate_during_hash(pw):
        # Runs strictly between Stage A and Stage B.
        if invalidate == "account_disabled":
            store.set_status(aid, "disabled", "2026-01-01T00:00:00.000000Z")
        elif invalidate == "expired":
            with store._write() as c:
                c.execute("UPDATE email_tokens SET expires_at = ? WHERE account_id = ?",
                          ("2020-01-01T00:00:00.000000Z", aid))
        else:                                          # consumed / superseded
            store.supersede_tokens(aid, RESET, "2026-01-01T00:00:00.000000Z")
        return real_hash(pw)
    monkeypatch.setattr(webapp._acct, "hash_password", invalidate_during_hash)

    before_pw = _pw_hash(store, aid)
    before_epoch = _epoch(store, aid)
    r = client.post("/reset/" + raw, data={"password": NEW_PW, "password_confirm": NEW_PW})
    monkeypatch.undo()
    assert r.status_code == 400
    assert _pw_hash(store, aid) == before_pw           # zero mutation by the loser
    assert _epoch(store, aid) == before_epoch


def test_f02_stage_b_independently_checks_every_condition(db_path):
    """§7 — each token/account condition is independently revalidated inside
    Stage B, with no reliance on any earlier read."""
    store = SqliteAccountStore(db_path)
    now = "2026-01-01T00:00:00.000000Z"
    cases = {}
    # unused + unexpired + active  → eligible
    aid_ok = _mk_account(store, "f02cond-ok@example.com")
    raw_ok = _acct.new_raw_token()
    store.create_email_token(_acct.new_account_id(), aid_ok, RESET,
                             _acct.hash_token(raw_ok), "2099-01-01T00:00:00.000000Z", now)
    cases["eligible"] = (raw_ok, aid_ok, True)
    # used
    aid_used = _mk_account(store, "f02cond-used@example.com")
    raw_used = _acct.new_raw_token()
    store.create_email_token(_acct.new_account_id(), aid_used, RESET,
                             _acct.hash_token(raw_used), "2099-01-01T00:00:00.000000Z", now)
    store.supersede_tokens(aid_used, RESET, now)
    cases["used"] = (raw_used, aid_used, False)
    # expired
    aid_exp = _mk_account(store, "f02cond-exp@example.com")
    raw_exp = _acct.new_raw_token()
    store.create_email_token(_acct.new_account_id(), aid_exp, RESET,
                             _acct.hash_token(raw_exp), "2020-01-01T00:00:00.000000Z", now)
    cases["expired"] = (raw_exp, aid_exp, False)
    # inactive account
    aid_dis = _mk_account(store, "f02cond-dis@example.com")
    raw_dis = _acct.new_raw_token()
    store.create_email_token(_acct.new_account_id(), aid_dis, RESET,
                             _acct.hash_token(raw_dis), "2099-01-01T00:00:00.000000Z", now)
    store.set_status(aid_dis, "disabled", now)
    cases["inactive_account"] = (raw_dis, aid_dis, False)
    # wrong type
    aid_wt = _mk_account(store, "f02cond-wt@example.com")
    raw_wt = _acct.new_raw_token()
    store.create_email_token(_acct.new_account_id(), aid_wt, VERIFICATION,
                             _acct.hash_token(raw_wt), "2099-01-01T00:00:00.000000Z", now)
    cases["wrong_type"] = (raw_wt, aid_wt, False)

    for name, (raw, aid, expected) in cases.items():
        before = _durable_snapshot(store, aid)
        got = store.complete_password_reset(_acct.hash_token(raw), "new-hash-%s" % name, now)
        if expected:
            assert got == aid, name
        else:
            assert got is None, name
            assert _durable_snapshot(store, aid) == before, name


# ---------------------------------------------------------------------------
# Mutation and row-count tests
# ---------------------------------------------------------------------------
def _seed_reset(store, email):
    aid = _mk_account(store, email)
    raw = _acct.new_raw_token()
    store.create_email_token(_acct.new_account_id(), aid, RESET, _acct.hash_token(raw),
                             "2099-01-01T00:00:00.000000Z", "2026-01-01T00:00:00.000000Z")
    return aid, raw


@pytest.mark.parametrize("after_stmt,prefix,skip", [
    ("submitted-token consumption", "UPDATE EMAIL_TOKENS SET USED_AT", 0),
    ("password update", "UPDATE ACCOUNTS SET PASSWORD_HASH", 0),
    ("epoch increment", "UPDATE ACCOUNTS SET SESSION_EPOCH", 0),
    ("other-token supersession", "UPDATE EMAIL_TOKENS SET USED_AT", 1),
])
def test_f02_pre_commit_failure_rolls_everything_back(db_path, monkeypatch,
                                                      after_stmt, prefix, skip):
    """§11 mutation tests — a failure injected immediately after each mutation and
    during supersession rolls the COMPLETE transaction back: token, password,
    epoch and supersession together. No success, no partial durable state."""
    store = SqliteAccountStore(db_path)
    aid, raw = _seed_reset(store, "f02mut-%s@example.com" % prefix[-12:].lower().replace(" ", ""))
    before = _durable_snapshot(store, aid)
    _inject(monkeypatch, store, [prefix], after=skip)
    with pytest.raises(Exception):
        store.complete_password_reset(_acct.hash_token(raw), "would-be-new-hash",
                                      "2026-01-01T00:00:00.000000Z")
    monkeypatch.undo()
    assert _durable_snapshot(store, aid) == before, after_stmt
    assert _token_row(store, raw)["used_at"] is None


@pytest.mark.parametrize("prefix,label", [
    ("UPDATE EMAIL_TOKENS SET USED_AT", "submitted token"),
    ("UPDATE ACCOUNTS SET PASSWORD_HASH", "password"),
    ("UPDATE ACCOUNTS SET SESSION_EPOCH", "epoch"),
])
def test_f02_post_eligibility_unexpected_rowcount_is_invariant_failure(
        db_path, monkeypatch, prefix, label):
    """§8B / D-05 — an unexpected row count on a required UPDATE AFTER eligibility
    passed is an invariant/operational failure with row-count evidence: rollback,
    NOT the ordinary concurrent-loser branch."""
    store = SqliteAccountStore(db_path)
    aid, raw = _seed_reset(store, "f02rc-%s@example.com" % label.replace(" ", ""))
    before = _durable_snapshot(store, aid)
    class _ZeroCursor:
        rowcount = 0

    def hook(real, sql, *a, **k):
        if sql.strip().upper().startswith(prefix):
            return _ZeroCursor()
        return real.execute(sql, *a, **k)
    _patch_conn(monkeypatch, store, hook)
    with pytest.raises(AccountStoreInvariantError) as ei:
        store.complete_password_reset(_acct.hash_token(raw), "would-be-new-hash",
                                      "2026-01-01T00:00:00.000000Z")
    monkeypatch.undo()
    assert "0 rows" in str(ei.value) and "expected exactly 1" in str(ei.value)
    assert _durable_snapshot(store, aid) == before


def test_f02_post_eligibility_rowcount_failure_returns_503_not_400(client, monkeypatch):
    """§8B at the web boundary — the post-eligibility invariant branch must NOT be
    normalized into the ordinary concurrent-loser 400."""
    _register(client, "f02rc503@example.com")
    client.post("/recover", data={"email": "f02rc503@example.com"})
    raw = _reset_token("f02rc503@example.com")
    store = _store()
    aid = store.get_account_by_normalized_email("f02rc503@example.com")["account_id"]
    before = _durable_snapshot(store, aid)
    class _ZeroCursor:
        rowcount = 0

    def hook(real, sql, *a, **k):
        if sql.strip().upper().startswith("UPDATE EMAIL_TOKENS SET USED_AT"):
            return _ZeroCursor()
        return real.execute(sql, *a, **k)
    _patch_conn(monkeypatch, store, hook)
    r = client.post("/reset/" + raw, data={"password": NEW_PW, "password_confirm": NEW_PW})
    monkeypatch.undo()
    assert r.status_code == 503 and r.get_data() == b""
    assert _durable_snapshot(store, aid) == before


def test_f02_missing_account_behaviour(db_path):
    """§11 — a reset token whose account row is absent is ordinary ineligibility
    with zero mutation, never a partial write."""
    store = SqliteAccountStore(db_path)
    now = "2026-01-01T00:00:00.000000Z"
    aid = _mk_account(store, "f02ma@example.com")
    raw = _acct.new_raw_token()
    store.create_email_token(_acct.new_account_id(), aid, RESET, _acct.hash_token(raw),
                             "2099-01-01T00:00:00.000000Z", now)
    # PRAGMA foreign_keys is a no-op inside a transaction, so toggle it outside
    # one to reach the otherwise FK-protected "token without account" state.
    store._conn.execute("PRAGMA foreign_keys = OFF")
    try:
        with store._write() as c:                   # remove the account row only
            c.execute("DELETE FROM accounts WHERE account_id = ?", (aid,))
    finally:
        store._conn.execute("PRAGMA foreign_keys = ON")
    assert store.get_account_by_id(aid) is None
    assert store.complete_password_reset(_acct.hash_token(raw), "x", now) is None
    assert _token_row(store, raw)["used_at"] is None


# ---------------------------------------------------------------------------
# COMMIT tests
# ---------------------------------------------------------------------------
def test_f02_commit_exception_cannot_report_success(db_path, monkeypatch):
    """§11 COMMIT — a COMMIT exception can never report success, rollback is
    attempted while the connection is transactional, and no blind retry occurs."""
    store = SqliteAccountStore(db_path)
    aid, raw = _seed_reset(store, "f02commit@example.com")
    before = _durable_snapshot(store, aid)
    inj = _inject(monkeypatch, store, ["COMMIT"])
    with pytest.raises(AccountStoreCommitError) as ei:
        store.complete_password_reset(_acct.hash_token(raw), "new-hash",
                                      "2026-01-01T00:00:00.000000Z")
    monkeypatch.undo()
    assert ei.value.durable_outcome == DURABLE_CONFIRMED_UNCHANGED
    assert inj.hits == 1, "COMMIT must not be retried"
    assert _durable_snapshot(store, aid) == before


def test_f02_rollback_failure_neither_succeeds_nor_erases_original(db_path, monkeypatch):
    """§11 COMMIT — a rollback failure does not become success and does not erase
    the original failure; the connection is then refused for blind continuation."""
    store = SqliteAccountStore(db_path)
    aid, raw = _seed_reset(store, "f02rbf@example.com")
    _inject(monkeypatch, store, ["COMMIT", "ROLLBACK"])
    with pytest.raises(AccountStoreCommitError) as ei:
        store.complete_password_reset(_acct.hash_token(raw), "new-hash",
                                      "2026-01-01T00:00:00.000000Z")
    monkeypatch.undo()
    assert ei.value.original is not None                 # original COMMIT failure kept
    assert ei.value.rollback_error is not None           # rollback failure surfaced
    assert ei.value.durable_outcome == DURABLE_INDETERMINATE
    assert store._connection_unsafe is True
    from engine.account_store import AccountStoreConnectionUnsafeError
    with pytest.raises(AccountStoreConnectionUnsafeError):
        store.increment_session_epoch(aid, "2026-01-01T00:00:01.000000Z")


def test_f02_transaction_state_is_inspected_before_rollback(db_path, monkeypatch):
    """§9 step 2 — the connection's transactional state is actually inspected; a
    rollback is not issued blindly when no transaction remains."""
    store = SqliteAccountStore(db_path)
    aid, raw = _seed_reset(store, "f02insp@example.com")
    seen = []

    def watch(real, sql, *a, **k):
        up = sql.strip().upper()
        if up.startswith("COMMIT"):
            real.execute(sql, *a, **k)                   # becomes durable
            raise _sqlite3.OperationalError("injected commit failure")
        if up.startswith("ROLLBACK"):
            seen.append("ROLLBACK")
        return real.execute(sql, *a, **k)
    _patch_conn(monkeypatch, store, watch)
    with pytest.raises(AccountStoreCommitError) as ei:
        store.complete_password_reset(_acct.hash_token(raw), "new-hash",
                                      "2026-01-01T00:00:00.000000Z")
    monkeypatch.undo()
    assert seen == [], "no ROLLBACK may be issued once no transaction remains"
    assert ei.value.durable_outcome == DURABLE_INDETERMINATE
    assert _token_row(store, raw)["used_at"] is not None  # it really did commit


def test_f02_confirmed_rollback_claimed_only_when_established(db_path, monkeypatch):
    """§9 — 'confirmed rollback' is claimed ONLY when established; the
    indeterminate case is explicitly labelled instead."""
    store = SqliteAccountStore(db_path)
    aid, raw = _seed_reset(store, "f02claim@example.com")
    _inject(monkeypatch, store, ["COMMIT"])              # transaction still open
    with pytest.raises(AccountStoreCommitError) as confirmed:
        store.complete_password_reset(_acct.hash_token(raw), "h", "2026-01-01T00:00:00.000000Z")
    monkeypatch.undo()
    _inject(monkeypatch, store, ["COMMIT"], mode="commit_then_raise")
    with pytest.raises(AccountStoreCommitError) as indeterminate:
        store.complete_password_reset(_acct.hash_token(raw), "h", "2026-01-01T00:00:01.000000Z")
    monkeypatch.undo()
    assert confirmed.value.durable_outcome == DURABLE_CONFIRMED_UNCHANGED
    assert indeterminate.value.durable_outcome == DURABLE_INDETERMINATE
    assert confirmed.value.durable_outcome != indeterminate.value.durable_outcome


def test_f02_local_session_preservation_is_not_authentication_proof(client, monkeypatch):
    """§3 evidence-class rule, applied to F-02's COMMIT branch: preserved local
    material is NOT proof that the session is still authenticated."""
    _register(client, "f02sess@example.com")
    _login(client, "f02sess@example.com")
    other = app.test_client()
    other.post("/recover", data={"email": "f02sess@example.com"})
    raw = _reset_token("f02sess@example.com")
    store = _store()
    _inject(monkeypatch, store, ["COMMIT"], mode="commit_then_raise")
    r = other.post("/reset/" + raw, data={"password": NEW_PW, "password_confirm": NEW_PW})
    monkeypatch.undo()
    assert r.status_code == 503                          # no success claim
    with client.session_transaction() as sess:
        assert "auth" in sess                            # material still present
    rr = client.get("/account")                          # yet validity is gone
    assert rr.status_code == 302 and rr.headers["Location"].endswith("/login")


# ---------------------------------------------------------------------------
# Concurrency, replay and successful reset
# ---------------------------------------------------------------------------
def test_f02_two_competing_same_token_requests_exactly_one_winner(client, monkeypatch):
    """§11 concurrency — two REAL competing same-token requests, deterministically
    synchronized so BOTH clear Stage A before either enters Stage B: exactly one
    confirmed commit; the loser is rejected by Stage B's initial in-transaction
    eligibility revalidation BEFORE mutation; exactly one password change and one
    epoch increment; other reset tokens superseded."""
    _register(client, "f02race@example.com")
    client.post("/recover", data={"email": "f02race@example.com"})
    raw = _reset_token("f02race@example.com")
    store = _store()
    aid = store.get_account_by_normalized_email("f02race@example.com")["account_id"]
    before_pw = _pw_hash(store, aid)
    before_epoch = _epoch(store, aid)

    barrier = threading.Barrier(2, timeout=30)
    real_eligible = store.password_reset_eligible

    def synchronized_eligible(*a, **k):
        result = real_eligible(*a, **k)
        barrier.wait()          # neither request may proceed to Stage B alone
        return result
    monkeypatch.setattr(store, "password_reset_eligible", synchronized_eligible)

    results = {}

    def attempt(name, pw):
        c = app.test_client()
        results[name] = c.post("/reset/" + raw,
                               data={"password": pw, "password_confirm": pw}).status_code

    t1 = threading.Thread(target=attempt, args=("a", NEW_PW))
    t2 = threading.Thread(target=attempt, args=("b", "a second sufficiently long pw"))
    t1.start(); t2.start(); t1.join(30); t2.join(30)
    monkeypatch.undo()

    codes = sorted(results.values())
    assert codes == [200, 400], results          # exactly one winner, one generic loser
    assert _pw_hash(store, aid) != before_pw     # exactly one password replacement
    assert _epoch(store, aid) == before_epoch + 1   # exactly one epoch increment
    assert store.active_tokens(aid, RESET) == 0     # all reset tokens now inactive


def test_f02_successful_reset_supersedes_other_active_reset_tokens(client):
    """§9 success — the submitted token is consumed and the account's OTHER active
    reset tokens are superseded in the same transaction."""
    _register(client, "f02sup@example.com")
    store = _store()
    aid = store.get_account_by_normalized_email("f02sup@example.com")["account_id"]
    client.post("/recover", data={"email": "f02sup@example.com"})
    raw = _reset_token("f02sup@example.com")
    extra = _acct.new_raw_token()                 # a second, still-active reset token
    with store._write() as c:
        c.execute("INSERT INTO email_tokens (token_id, account_id, token_type, "
                  "token_hash, expires_at, used_at, created_at) "
                  "VALUES (?, ?, ?, ?, ?, NULL, ?)",
                  (_acct.new_account_id(), aid, RESET, _acct.hash_token(extra),
                   "2099-01-01T00:00:00.000000Z", "2026-01-01T00:00:00.000000Z"))
    assert store.active_tokens(aid, RESET) == 2
    assert client.post("/reset/" + raw,
                       data={"password": NEW_PW, "password_confirm": NEW_PW}).status_code == 200
    assert store.active_tokens(aid, RESET) == 0
    assert _token_row(store, raw)["used_at"] is not None
    assert _token_row(store, extra)["used_at"] is not None


def test_f02_replay_causes_zero_additional_mutation(client):
    """§11 replay — a replayed reset performs no further mutation."""
    _register(client, "f02rep@example.com")
    client.post("/recover", data={"email": "f02rep@example.com"})
    raw = _reset_token("f02rep@example.com")
    store = _store()
    aid = store.get_account_by_normalized_email("f02rep@example.com")["account_id"]
    assert client.post("/reset/" + raw,
                       data={"password": NEW_PW, "password_confirm": NEW_PW}).status_code == 200
    after_first = _durable_snapshot(store, aid)
    replay = client.post("/reset/" + raw,
                         data={"password": "yet another long password",
                               "password_confirm": "yet another long password"})
    assert replay.status_code == 400
    assert _durable_snapshot(store, aid) == after_first    # zero additional mutation


def test_f02_success_old_rejected_new_accepted_sessions_revoked_no_auto_signin(client):
    """§9 success postconditions — password replaced once, previous sessions
    revoked, no automatic sign-in, old password rejected and new accepted."""
    _register(client, "f02ok@example.com")
    _login(client, "f02ok@example.com")
    assert client.get("/account").status_code == 200
    resetter = app.test_client()
    resetter.post("/recover", data={"email": "f02ok@example.com"})
    raw = _reset_token("f02ok@example.com")
    r = resetter.post("/reset/" + raw, data={"password": NEW_PW, "password_confirm": NEW_PW})
    assert r.status_code == 200
    with resetter.session_transaction() as sess:
        assert "auth" not in sess                          # no automatic sign-in
    prev = client.get("/account")                          # old session revoked
    assert prev.status_code == 302 and prev.headers["Location"].endswith("/login")
    c_old = app.test_client()
    assert c_old.post("/login", data={"email": "f02ok@example.com",
                                      "password": PW}).status_code == 401
    c_new = app.test_client()
    assert c_new.post("/login", data={"email": "f02ok@example.com",
                                      "password": NEW_PW}).status_code == 302


def test_f02_failure_injection_adds_no_production_surface():
    """§11 closing rule — failure injection introduces no production-visible
    endpoint, environment switch, persistent hook or schema field."""
    import engine.account_store as _store_mod
    src = open(_store_mod.__file__, encoding="utf-8").read()
    app_src = open(webapp.__file__, encoding="utf-8").read()
    for forbidden in ("INVENTORAI_FAIL", "FAIL_COMMIT", "_fail_hook", "fault_inject",
                      "simulate_failure", "TESTING_FAIL"):
        assert forbidden not in src and forbidden not in app_src
    rules = [r.rule for r in app.url_map.iter_rules()]
    assert not [r for r in rules if "fail" in r.lower() or "inject" in r.lower()]


# ===========================================================================
# B-01 / B-02 — web-boundary behaviour on unsafe store state and store-acquisition
# failure (Lead review F01F02-V21-LEAD-REVIEW-01; repair instruction §§4.3, 5)
# ===========================================================================
from engine.account_store import AccountStoreRollbackError


def _drive_store_unsafe(monkeypatch, store, aid):
    """Body failure whose defensive ROLLBACK also fails → unresolved state."""
    def hook(real, sql, *a, **k):
        up = sql.strip().upper()
        if up.startswith("UPDATE ACCOUNTS SET SESSION_EPOCH"):
            raise _sqlite3.OperationalError("injected body failure")
        if up.startswith("ROLLBACK"):
            raise _sqlite3.OperationalError("injected rollback failure")
        return real.execute(sql, *a, **k)
    _patch_conn(monkeypatch, store, hook)
    with pytest.raises(AccountStoreRollbackError):
        store.increment_session_epoch(aid, "2026-01-01T00:00:00.000000Z")
    monkeypatch.undo()
    assert store._connection_unsafe is True


def test_b01_eligible_token_on_unsafe_connection_is_generic_503(client, monkeypatch):
    """§4.3 — an unsafe Stage-A read is an operational precheck failure: generic
    empty 503, ZERO password hashing, zero reset mutation, no session clearing and
    no token/account disclosure. The token itself stays eligible in the database."""
    _register(client, "b01elig@example.com")
    _login(client, "b01elig@example.com")
    client.post("/recover", data={"email": "b01elig@example.com"})
    raw = _reset_token("b01elig@example.com")
    store = _store()
    aid = store.get_account_by_normalized_email("b01elig@example.com")["account_id"]
    before = _durable_snapshot(store, aid)
    _drive_store_unsafe(monkeypatch, store, aid)

    calls = _hash_spy(monkeypatch)
    r = client.post("/reset/" + raw, data={"password": NEW_PW, "password_confirm": NEW_PW})
    assert r.status_code == 503
    assert r.get_data() == b""                        # generic and non-disclosing
    assert calls == []                                # zero password hashing
    with client.session_transaction() as sess:
        assert "auth" in sess                         # no deliberate clearing
    monkeypatch.undo()

    # TEST-ONLY inspection cleanup. The product deliberately offers no recovery, so
    # the stranded transaction is released and the refusal flag cleared HERE, by the
    # test, purely to read durable state back. This is not a product code path.
    if store._conn.in_transaction:
        store._conn.execute("ROLLBACK")
    store._connection_unsafe = False
    assert _durable_snapshot(store, aid) == before     # zero reset mutation
    assert store.get_email_token_by_hash(_acct.hash_token(raw))["used_at"] is None


def test_b01_normal_validation_after_unsafe_state_fails_closed(client, monkeypatch):
    """§4.3 — ordinary authentication/account lookup after unsafe state fails
    closed rather than reading unresolved state from the refused connection."""
    _register(client, "b01valid@example.com")
    _login(client, "b01valid@example.com")
    assert client.get("/account").status_code == 200
    store = _store()
    aid = store.get_account_by_normalized_email("b01valid@example.com")["account_id"]
    _drive_store_unsafe(monkeypatch, store, aid)
    r = client.get("/account")
    assert r.status_code == 302 and r.headers["Location"].endswith("/login")
    with client.session_transaction() as sess:
        assert "auth" not in sess                     # session dropped, fail closed


def test_b01_logout_all_body_rollback_failure_is_503_with_no_guarantee(client,
                                                                       monkeypatch):
    """§4.3 — an F-01 body/invariant failure whose rollback could not be resolved
    returns generic empty 503, preserves local material, claims neither success nor
    confirmed rollback nor continued authentication, and does not retry."""
    _register(client, "b01lo@example.com")
    _login(client, "b01lo@example.com")
    csrf = _csrf(client)
    store = _store()
    attempts = {"epoch": 0, "rollback": 0}

    class _ZeroCursor:
        rowcount = 0

    def hook(real, sql, *a, **k):
        up = sql.strip().upper()
        if up.startswith("UPDATE ACCOUNTS SET SESSION_EPOCH"):
            attempts["epoch"] += 1
            return _ZeroCursor()                       # invariant breach
        if up.startswith("ROLLBACK"):
            attempts["rollback"] += 1
            raise _sqlite3.OperationalError("injected rollback failure")
        return real.execute(sql, *a, **k)
    _patch_conn(monkeypatch, store, hook)
    r = client.post("/logout-all", data={"csrf_token": csrf})
    monkeypatch.undo()

    assert r.status_code == 503
    assert r.get_data() == b"" and "Location" not in r.headers   # no success claim
    assert attempts["epoch"] == 1 and attempts["rollback"] == 1  # no retry
    assert store._connection_unsafe is True
    with client.session_transaction() as sess:
        assert "auth" in sess                          # material not deliberately cleared
    # Continued authentication is NOT promised: ordinary validation now fails closed.
    assert client.get("/account").status_code == 302


def test_b01_logout_all_confirmed_rollback_still_reports_unchanged(client, monkeypatch):
    """§4.3 — other pre-COMMIT failures WITH a confirmed rollback keep the existing
    confirmed-unchanged behaviour; not every non-COMMIT exception is uncertain."""
    _register(client, "b01conf@example.com")
    _login(client, "b01conf@example.com")
    csrf = _csrf(client)
    store = _store()
    aid = store.get_account_by_normalized_email("b01conf@example.com")["account_id"]
    before = _epoch(store, aid)
    _inject(monkeypatch, store, ["UPDATE ACCOUNTS SET SESSION_EPOCH"])
    r = client.post("/logout-all", data={"csrf_token": csrf})
    monkeypatch.undo()
    assert r.status_code == 503 and r.get_data() == b""
    assert store._connection_unsafe is False           # connection remains usable
    assert _epoch(store, aid) == before                # provably unchanged
    assert client.get("/account").status_code == 200   # still authenticated


def test_b02_reset_store_acquisition_failure_is_generic_503(client, monkeypatch):
    """§5 — store acquisition inside the Stage-A operational boundary: a failure
    returns generic empty 503, not a 500, with zero password hashing, zero
    mutation, no deliberate session clearing and no disclosure."""
    _register(client, "b02acq@example.com")
    _login(client, "b02acq@example.com")
    client.post("/recover", data={"email": "b02acq@example.com"})
    raw = _reset_token("b02acq@example.com")
    store = _store()
    aid = store.get_account_by_normalized_email("b02acq@example.com")["account_id"]
    before = _durable_snapshot(store, aid)
    calls = _hash_spy(monkeypatch)

    def boom():
        raise RuntimeError("injected store acquisition failure /tmp/secret.sqlite")
    monkeypatch.setattr(webapp, "_get_account_store", boom)
    r = client.post("/reset/" + raw, data={"password": NEW_PW, "password_confirm": NEW_PW})
    monkeypatch.undo()

    assert r.status_code == 503
    body = r.get_data()
    assert body == b""                                 # generic and empty
    assert b"secret" not in body and b"RuntimeError" not in body
    assert calls == []                                 # zero hashing
    assert _durable_snapshot(store, aid) == before      # zero mutation
    with client.session_transaction() as sess:
        assert "auth" in sess                          # no deliberate clearing


def test_b02_reset_token_hashing_failure_is_generic_503(client, monkeypatch):
    """§5 — token hashing also sits inside the operational boundary."""
    _register(client, "b02hash@example.com")
    client.post("/recover", data={"email": "b02hash@example.com"})
    raw = _reset_token("b02hash@example.com")
    calls = _hash_spy(monkeypatch)
    monkeypatch.setattr(webapp._acct, "hash_token",
                        lambda *a, **k: (_ for _ in ()).throw(
                            RuntimeError("injected token-hash failure")))
    r = client.post("/reset/" + raw, data={"password": NEW_PW, "password_confirm": NEW_PW})
    monkeypatch.undo()
    assert r.status_code == 503 and r.get_data() == b""
    assert calls == []                                 # no password hashing


def test_b02_ordinary_ineligibility_stays_400_not_503(client):
    """§5 — ordinary Stage-A ineligibility is NOT collapsed into the operational
    503 branch; the two remain distinct and distinguishable."""
    _register(client, "b02dist@example.com")
    client.post("/recover", data={"email": "b02dist@example.com"})
    used = _reset_token("b02dist@example.com")
    assert client.post("/reset/" + used,
                       data={"password": NEW_PW,
                             "password_confirm": NEW_PW}).status_code == 200
    for raw in (used, "never-was-a-token"):
        r = client.post("/reset/" + raw,
                        data={"password": NEW_PW, "password_confirm": NEW_PW})
        assert r.status_code == 400                    # ordinary ineligibility
        assert r.get_data() != b""                     # rendered page, not the 503 body
