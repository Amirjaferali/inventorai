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
