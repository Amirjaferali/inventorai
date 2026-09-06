"""P5-1 — Account & Credential Foundation (RED/GREEN).

Behaviour-based tests for the Phase 5 Option A account foundation (gate
G-P5-1-ACCOUNT-CREDENTIAL-FOUNDATION-IMPLEMENTATION-01; formal contract
G-P5-FORMAL-CONTRACT-AND-CONTINUING-AUTHORIZATION-01). Additive account
persistence, immutable UUID account_id, deterministic normalized-email
uniqueness, Werkzeug scrypt hashing, typed verification-token issuance (hash
stored, 24h TTL), a development email sink, a generic non-enumerating
registration response, and a bounded rate-limit foundation.

SCOPE GUARD — these tests assert the FOUNDATION ONLY. They deliberately prove
the ABSENCE of out-of-scope behaviour: registration never signs a user in,
never sets an authenticated cookie, never creates a project, and never reveals
whether an email already exists (including disabled/deleted accounts). Login,
authenticated sessions, CSRF, verification COMPLETION, password reset, project
ownership, and route-ownership are NOT implemented here and are not tested as
present.

Real on-disk SQLite under pytest ``tmp_path`` (via the autouse conftest DB
isolation); the Flask ``test_client``; the real credential helpers, account
store, and dev email sink. No ``:memory:`` DB, no mocks of the store, no
file-existence-only assertions.
"""
import os
from datetime import datetime

import pytest

import web.app as webapp
from web.app import app
from engine import account_credentials as _acct
from engine.account_store import (
    SqliteAccountStore, AccountStoreError, EmailExistsError,
    ACCOUNT_STATUSES, VERIFICATION,
)
from engine.email_sender import DevMemoryEmailSender
from engine.record_store import SqliteRecordStore
from engine.record_contract import ProjectRecordContract

VALID_PASSWORD = "correct horse battery staple"   # 28 chars, >= 12
VALID_PASSWORD_2 = "another sufficiently long secret"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture
def db_path():
    """Single governed DB path for this test (set by the autouse conftest)."""
    return os.environ["INVENTORAI_DB_PATH"]


def _register(client, email, password=VALID_PASSWORD, confirm=None):
    return client.post("/register", data={
        "email": email, "password": password,
        "password_confirm": password if confirm is None else confirm,
    })


def _acct_store():
    """The one app-scoped account store (same INVENTORAI_DB_PATH the route uses)."""
    return webapp._get_account_store()


def _captured_raw_token(email_normalized):
    """Pull the raw verification token out of the dev email sink message body."""
    msg = webapp._EMAIL_SENDER.last_for(email_normalized)
    assert msg is not None, "expected a dev-sink verification message"
    return msg["body"].rsplit(": ", 1)[-1].strip()


def _parse_iso(value):
    return datetime.fromisoformat(value.rstrip("Z"))


# --- Group A: RED baseline — route + modules exist -------------------------
def test_register_get_route_exists(client):
    """GET /register renders the registration page (absent on the parent)."""
    resp = client.get("/register")
    assert resp.status_code == 200


def test_account_modules_present():
    """The additive engine modules exist and expose the P5-1 surface."""
    assert hasattr(_acct, "normalize_email")
    assert hasattr(_acct, "hash_password")
    assert callable(SqliteAccountStore)
    assert isinstance(DevMemoryEmailSender(), DevMemoryEmailSender)


# --- Group B: account creation ---------------------------------------------
def test_valid_registration_creates_one_account(client):
    resp = _register(client, "person@example.com")
    assert resp.status_code == 200
    store = _acct_store()
    assert store.count_accounts() == 1
    acct = store.get_account_by_normalized_email("person@example.com")
    assert acct is not None
    assert acct["email_normalized"] == "person@example.com"
    assert acct["status"] == "active"
    assert acct["email_verified"] is False


def test_account_id_is_immutable_uuid_not_email(client):
    _register(client, "id-check@example.com")
    acct = _acct_store().get_account_by_normalized_email("id-check@example.com")
    account_id = acct["account_id"]
    # A durable UUID-shaped id, NEVER the email.
    assert account_id.startswith("acct_")
    assert "id-check@example.com" not in account_id
    assert account_id != "id-check@example.com"
    # Re-lookup by id returns the SAME immutable id (no reassignment path).
    assert _acct_store().get_account_by_id(account_id)["account_id"] == account_id


def test_second_distinct_email_creates_second_account(client):
    _register(client, "a@example.com")
    _register(client, "b@example.com")
    assert _acct_store().count_accounts() == 2


# --- Group C: normalization & uniqueness -----------------------------------
def test_email_normalization_is_deterministic():
    assert _acct.normalize_email("  Foo@Bar.COM ") == "foo@bar.com"
    assert _acct.normalize_email("foo@bar.com") == "foo@bar.com"
    assert _acct.normalize_email(None) == ""


def test_registration_normalizes_before_storing(client):
    _register(client, "  MixedCase@Example.COM ")
    store = _acct_store()
    assert store.get_account_by_normalized_email("mixedcase@example.com") is not None
    assert store.count_accounts() == 1


def test_duplicate_normalized_email_single_account(client):
    _register(client, "dup@example.com")
    _register(client, " DUP@Example.com ")   # same normalized address
    assert _acct_store().count_accounts() == 1


def test_store_duplicate_raises_email_exists(db_path):
    store = SqliteAccountStore(db_path)
    store.create_account(_acct.new_account_id(), "u@example.com",
                         _acct.hash_password(VALID_PASSWORD), "2026-01-01T00:00:00Z")
    with pytest.raises(EmailExistsError):
        store.create_account(_acct.new_account_id(), "u@example.com",
                             _acct.hash_password(VALID_PASSWORD), "2026-01-01T00:00:01Z")
    assert store.count_accounts() == 1
    store.close()


def test_concurrent_duplicate_yields_one_account(db_path):
    """Two racing inserts of the same normalized email: the UNIQUE constraint
    guarantees the second fails closed, so only ONE account can ever exist."""
    store = SqliteAccountStore(db_path)
    created = 0
    for i in range(2):
        try:
            store.create_account(_acct.new_account_id(), "race@example.com",
                                 _acct.hash_password(VALID_PASSWORD),
                                 "2026-01-01T00:00:0%d" % i)
            created += 1
        except EmailExistsError:
            pass
    assert created == 1
    assert store.count_accounts() == 1
    store.close()


# --- Group D: non-enumeration ----------------------------------------------
def test_new_vs_existing_response_identical(client):
    first = _register(client, "enum@example.com")
    second = _register(client, "enum@example.com")
    assert first.status_code == second.status_code == 200
    assert first.data == second.data          # byte-identical: no enumeration


def test_disabled_account_no_enumeration_or_reactivation(client):
    _register(client, "disabled@example.com")
    store = _acct_store()
    acct = store.get_account_by_normalized_email("disabled@example.com")
    # Put the account into a non-active state directly (no public status route).
    store._conn.execute("UPDATE accounts SET status='disabled' WHERE account_id=?",
                        (acct["account_id"],))
    store._conn.commit()
    baseline = _register(client, "unseen@example.com").data  # a fresh generic ack
    resp = _register(client, "disabled@example.com")
    assert resp.status_code == 200
    assert resp.data == baseline               # identical to an ordinary generic ack
    after = store.get_account_by_normalized_email("disabled@example.com")
    assert after["status"] == "disabled"       # NOT reactivated
    assert store.count_accounts() == 2         # no second account for the same email


# --- Group E: password handling --------------------------------------------
def test_password_not_stored_plaintext(client):
    _register(client, "pw@example.com", password=VALID_PASSWORD)
    acct = _acct_store().get_account_by_normalized_email("pw@example.com")
    assert acct["password_hash"] != VALID_PASSWORD
    assert VALID_PASSWORD not in acct["password_hash"]


def test_password_hash_uses_scrypt(client):
    _register(client, "scrypt@example.com")
    acct = _acct_store().get_account_by_normalized_email("scrypt@example.com")
    assert acct["password_hash"].startswith("scrypt:")


def test_password_verifies_correct_and_rejects_wrong():
    h = _acct.hash_password(VALID_PASSWORD)
    assert _acct.verify_password(h, VALID_PASSWORD) is True
    assert _acct.verify_password(h, "wrong password value") is False
    assert _acct.verify_password("", VALID_PASSWORD) is False


def test_password_below_minimum_rejected(client):
    resp = _register(client, "short@example.com", password="short")
    assert resp.status_code == 400
    assert _acct_store().count_accounts() == 0


def test_password_confirm_mismatch_rejected(client):
    resp = _register(client, "mismatch@example.com",
                     password=VALID_PASSWORD, confirm="different but long enough")
    assert resp.status_code == 400
    assert _acct_store().count_accounts() == 0


def test_password_bounds_unit():
    assert _acct.validate_password("short")[0] is False
    assert _acct.validate_password("")[0] is False
    assert _acct.validate_password("x" * 12)[0] is True
    assert _acct.validate_password("x" * (_acct.MAX_PASSWORD_LENGTH + 1))[0] is False


# --- Group F: verification tokens ------------------------------------------
def test_registration_issues_verification_token_hash_only(client):
    _register(client, "tok@example.com")
    store = _acct_store()
    acct = store.get_account_by_normalized_email("tok@example.com")
    raw = _captured_raw_token("tok@example.com")
    token_hash = _acct.hash_token(raw)
    row = store.get_email_token_by_hash(token_hash)
    assert row is not None
    assert row["token_type"] == VERIFICATION
    assert row["account_id"] == acct["account_id"]        # linked to the account
    # The RAW token is NEVER stored: no row's token_hash equals the raw value.
    stored = [r[0] for r in store._conn.execute(
        "SELECT token_hash FROM email_tokens").fetchall()]
    assert raw not in stored
    assert token_hash in stored


def test_verification_token_has_24h_expiry(client):
    _register(client, "ttl@example.com")
    store = _acct_store()
    raw = _captured_raw_token("ttl@example.com")
    row = store.get_email_token_by_hash(_acct.hash_token(raw))
    delta = _parse_iso(row["expires_at"]) - _parse_iso(row["created_at"])
    assert abs(delta.total_seconds() - 24 * 60 * 60) < 1.0


def test_new_token_issuance_supersedes_old(db_path):
    store = SqliteAccountStore(db_path)
    acct_id = _acct.new_account_id()
    store.create_account(acct_id, "super@example.com",
                         _acct.hash_password(VALID_PASSWORD), "2026-01-01T00:00:00Z")
    store.create_email_token(_acct.new_token_id(), acct_id, VERIFICATION,
                             _acct.hash_token("raw-1"), "2026-01-02T00:00:00Z",
                             "2026-01-01T00:00:00Z")
    store.create_email_token(_acct.new_token_id(), acct_id, VERIFICATION,
                             _acct.hash_token("raw-2"), "2026-01-02T00:00:00Z",
                             "2026-01-01T00:01:00Z")
    assert store.active_verification_tokens(acct_id) == 1   # old one superseded
    store.close()


def test_dev_sink_receives_message_with_token(client):
    _register(client, "sink@example.com")
    msg = webapp._EMAIL_SENDER.last_for("sink@example.com")
    assert msg is not None
    assert msg["to"] == "sink@example.com"
    raw = _captured_raw_token("sink@example.com")
    assert raw and raw in msg["body"]


def test_raw_token_not_in_logs(client, caplog):
    import logging
    caplog.set_level(logging.DEBUG)
    _register(client, "nolog@example.com")
    raw = _captured_raw_token("nolog@example.com")
    assert raw not in caplog.text


def test_response_body_has_no_raw_token(client):
    resp = _register(client, "noleak@example.com")
    raw = _captured_raw_token("noleak@example.com")
    assert raw.encode() not in resp.data


# --- Group G: bounded rate-limit foundation --------------------------------
def test_rate_limit_boundary_store_level(db_path):
    store = SqliteAccountStore(db_path)
    digest = _acct.email_digest("rl@example.com")
    results = [store.record_rate_attempt(digest, "register", "2026-01-01T00:00:00Z",
                                         "2026-01-01T01:00:00Z", 10) for _ in range(11)]
    assert results[:10] == [True] * 10
    assert results[10] is False
    store.close()


def test_rate_limit_blocks_registration_with_generic_response(client):
    store = _acct_store()
    digest = _acct.email_digest("blocked@example.com")
    # Exhaust the window BEFORE the registration attempt. The window must still be
    # OPEN when the route runs (real "now"), so use a far-future expiry — otherwise
    # the route would see an expired window and start a fresh one.
    for _ in range(webapp._REGISTER_RATE_LIMIT):
        store.record_rate_attempt(digest, "register", "2026-01-01T00:00:00Z",
                                  "2099-01-01T00:00:00Z", webapp._REGISTER_RATE_LIMIT)
    generic = client.get("/register")  # baseline page for comparison of the ack later
    resp = _register(client, "blocked@example.com")
    assert resp.status_code == 200
    # No account was created because the attempt was rate-limited before create.
    assert store.get_account_by_normalized_email("blocked@example.com") is None
    assert store.count_accounts() == 0
    del generic


# --- Group H: additive migration & isolation from project data -------------
def test_migration_from_pre_p5_database(db_path):
    """Opening the account store on a pre-P5 database with existing project data
    only ADDS the new tables; the project data is fully preserved."""
    rstore = SqliteRecordStore(db_path)
    rstore.create_project(ProjectRecordContract(idea_id="idea-legacy", assertions=[]),
                          project_id="legacy-sid")
    rstore.close()

    astore = SqliteAccountStore(db_path)   # migration: adds accounts/token/rate tables
    assert astore.count_accounts() == 0
    astore.create_account(_acct.new_account_id(), "mig@example.com",
                          _acct.hash_password(VALID_PASSWORD), "2026-01-01T00:00:00Z")
    astore.close()

    rstore2 = SqliteRecordStore(db_path)
    contract = rstore2.load_contract("legacy-sid")   # legacy project still intact
    assert contract.idea_id == "idea-legacy"
    assert "legacy-sid" in rstore2.project_ids()
    rstore2.close()


def test_migration_is_idempotent(db_path):
    a1 = SqliteAccountStore(db_path)
    a1.create_account(_acct.new_account_id(), "idem@example.com",
                      _acct.hash_password(VALID_PASSWORD), "2026-01-01T00:00:00Z")
    a1.close()
    a2 = SqliteAccountStore(db_path)   # re-open: CREATE IF NOT EXISTS, no error
    assert a2.count_accounts() == 1
    assert a2.get_account_by_normalized_email("idem@example.com") is not None
    a2.close()


def test_existing_projects_unchanged_after_account_activity(db_path):
    rstore = SqliteRecordStore(db_path)
    rstore.create_project(ProjectRecordContract(idea_id="idea-keep", assertions=[]),
                          project_id="keep-sid")
    before = rstore.load_contract("keep-sid").to_dict()
    rstore.close()

    astore = SqliteAccountStore(db_path)
    astore.create_account(_acct.new_account_id(), "keep@example.com",
                          _acct.hash_password(VALID_PASSWORD), "2026-01-01T00:00:00Z")
    astore.close()

    rstore2 = SqliteRecordStore(db_path)
    assert rstore2.load_contract("keep-sid").to_dict() == before
    rstore2.close()


def test_corrupted_database_fails_safely(tmp_path):
    """A non-SQLite / corrupted file must fail closed on open, not silently
    swallow the corruption."""
    bad = tmp_path / "corrupt.sqlite"
    bad.write_bytes(b"this is not a sqlite database file at all" * 8)
    with pytest.raises(Exception):
        SqliteAccountStore(str(bad))


# --- Group I: status validation --------------------------------------------
def test_account_statuses_constant():
    assert ACCOUNT_STATUSES == frozenset({"active", "disabled", "deleted"})


def test_create_account_rejects_invalid_status(db_path):
    store = SqliteAccountStore(db_path)
    with pytest.raises(AccountStoreError):
        store.create_account(_acct.new_account_id(), "bad@example.com",
                             _acct.hash_password(VALID_PASSWORD),
                             "2026-01-01T00:00:00Z", status="bogus")
    assert store.count_accounts() == 0
    store.close()


# --- Group J: bounded — no project, no sign-in, no auth cookie -------------
def test_registration_creates_no_project(client, db_path):
    rstore = SqliteRecordStore(db_path)
    before = len(rstore.project_ids())
    rstore.close()
    _register(client, "noproj@example.com")
    rstore2 = SqliteRecordStore(db_path)
    assert len(rstore2.project_ids()) == before   # unchanged: no project created
    rstore2.close()


def test_registration_does_not_sign_in_or_set_auth_cookie(client):
    resp = _register(client, "nosignin@example.com")
    # Stays on the registration acknowledgement (no redirect to an authed area).
    assert resp.status_code == 200
    # No Flask session cookie is established (flask.session is never touched).
    set_cookie = resp.headers.get("Set-Cookie", "")
    assert "session=" not in set_cookie


# --- Group K: language-switchable + accessible registration surface ---------
def test_register_page_language_switch_and_accessible(client):
    body = client.get("/register").get_data(as_text=True)
    # D-P6-18 (D-P6-16): one UI language at a time; both languages remain reachable
    # via the global UI-language selector (English | العربية) on every page.
    assert '/ui-language' in body
    assert "العربية" in body and 'lang="ar"' in body
    assert 'autocomplete="email"' in body
    assert 'autocomplete="new-password"' in body
    assert 'for="email"' in body and 'for="password"' in body   # labelled inputs
    assert "required" in body


# ===========================================================================
# F-01/F-02 v2.1 — shared ``_write()`` transaction-owner hardening (D-02 Option A)
# Contract §§9-10 and the §14 dependency-bounded shared-helper sweep.
# ===========================================================================
import sqlite3 as _sqlite3
import threading as _threading

from engine.account_store import (
    AccountStoreCommitError, AccountStoreInvariantError,
    AccountStoreConnectionUnsafeError, RESET,
    DURABLE_CONFIRMED_UNCHANGED, DURABLE_INDETERMINATE,
)


class _ConnProxy:
    """Test-only proxy over the real ``sqlite3.Connection``. ``sqlite3`` connection
    objects reject attribute assignment, so failure injection replaces the store's
    ``_conn`` reference instead. ``execute`` goes through the hook; every other
    attribute — including ``in_transaction`` — forwards unchanged."""

    def __init__(self, real, hook):
        object.__setattr__(self, "_real_conn", real)
        object.__setattr__(self, "_hook", hook)

    def execute(self, sql, *args, **kwargs):
        return object.__getattribute__(self, "_hook")(
            object.__getattribute__(self, "_real_conn"), sql, *args, **kwargs)

    def __getattr__(self, name):
        return getattr(object.__getattribute__(self, "_real_conn"), name)


def _patch_conn(monkeypatch, store, hook):
    monkeypatch.setattr(store, "_conn", _ConnProxy(store._conn, hook))


def _inject_exec(monkeypatch, store, prefixes, mode="raise"):
    prefixes = tuple(p.upper() for p in prefixes)
    state = {"hits": 0}

    def hook(real, sql, *a, **k):
        if sql.strip().upper().startswith(prefixes):
            state["hits"] += 1
            if mode == "commit_then_raise":
                real.execute(sql, *a, **k)
            raise _sqlite3.OperationalError("injected failure")
        return real.execute(sql, *a, **k)
    _patch_conn(monkeypatch, store, hook)
    return state


def _mk(store, email="w@example.com", status="active"):
    aid = _acct.new_account_id()
    store.create_account(aid, _acct.normalize_email(email),
                         _acct.hash_password(VALID_PASSWORD),
                         "2026-01-01T00:00:00.000000Z", status=status)
    return aid


def test_write_remains_the_single_transaction_owner(db_path):
    """§10.1-2 — ``_write()`` acquires the lock, issues BEGIN IMMEDIATE and yields
    the connection. No parallel F-02 transaction mechanism is introduced."""
    store = SqliteAccountStore(db_path)
    src = open(store.__class__.__module__.replace(".", "/") + ".py", encoding="utf-8").read()
    assert src.count('execute("BEGIN IMMEDIATE")') == 2      # constructor + _write only
    assert "def _write" in src
    with store._write() as c:
        assert store._conn.in_transaction is True
        assert c is store._conn
    assert store._conn.in_transaction is False


def test_write_body_exception_rolls_back_and_propagates_original(db_path):
    """§10.3 — a body exception rolls back where the transaction is still open and
    propagates the ORIGINAL failure unchanged."""
    store = SqliteAccountStore(db_path)
    aid = _mk(store, "wbody@example.com")
    sentinel = RuntimeError("original body failure")
    with pytest.raises(RuntimeError) as ei:
        with store._write() as c:
            c.execute("UPDATE accounts SET session_epoch = 99 WHERE account_id = ?", (aid,))
            raise sentinel
    assert ei.value is sentinel                               # original, not wrapped
    assert store._conn.in_transaction is False
    assert store.get_account_by_id(aid)["session_epoch"] == 0  # rolled back


def test_write_commit_exception_never_reports_success(db_path, monkeypatch):
    """§10.4-5 — on a COMMIT exception the helper never reports success; it rolls
    back while transactional and raises with the original failure preserved."""
    store = SqliteAccountStore(db_path)
    aid = _mk(store, "wcommit@example.com")
    state = _inject_exec(monkeypatch, store, ["COMMIT"])
    with pytest.raises(AccountStoreCommitError) as ei:
        with store._write() as c:
            c.execute("UPDATE accounts SET session_epoch = 99 WHERE account_id = ?", (aid,))
    monkeypatch.undo()
    assert ei.value.durable_outcome == DURABLE_CONFIRMED_UNCHANGED
    assert isinstance(ei.value.original, Exception)
    assert ei.value.__cause__ is ei.value.original
    assert state["hits"] == 1                                  # no silent retry
    assert store.get_account_by_id(aid)["session_epoch"] == 0


def test_write_rollback_failure_retains_original_and_marks_unsafe(db_path, monkeypatch):
    """§10.6 — when the defensive rollback also fails, the original failure is
    retained, an operational failure propagates and the connection is treated as
    unsafe for blind continuation."""
    store = SqliteAccountStore(db_path)
    aid = _mk(store, "wrbf@example.com")
    _inject_exec(monkeypatch, store, ["COMMIT", "ROLLBACK"])
    with pytest.raises(AccountStoreCommitError) as ei:
        with store._write() as c:
            c.execute("UPDATE accounts SET session_epoch = 99 WHERE account_id = ?", (aid,))
    monkeypatch.undo()
    assert ei.value.original is not None and ei.value.rollback_error is not None
    assert ei.value.durable_outcome == DURABLE_INDETERMINATE
    assert store._connection_unsafe is True
    with pytest.raises(AccountStoreConnectionUnsafeError):     # no blind continuation
        with store._write():
            pass


def test_write_does_not_silently_retry_any_statement(db_path, monkeypatch):
    """§10.7 — no automatic retry of BEGIN, the body, COMMIT or ROLLBACK."""
    store = SqliteAccountStore(db_path)
    counts = {}

    def counting(real, sql, *a, **k):
        key = sql.strip().upper().split()[0]
        counts[key] = counts.get(key, 0) + 1
        if key == "COMMIT":
            raise _sqlite3.OperationalError("injected")
        return real.execute(sql, *a, **k)
    _patch_conn(monkeypatch, store, counting)
    with pytest.raises(AccountStoreCommitError):
        with store._write() as c:
            c.execute("SELECT 1")
    monkeypatch.undo()
    assert counts["BEGIN"] == 1 and counts["COMMIT"] == 1 and counts.get("ROLLBACK", 0) == 1


def test_write_exposes_no_sensitive_database_detail_in_its_message(db_path, monkeypatch):
    """§10.8 — the raised operational failure carries no schema/SQL/credential
    detail of its own; the web boundary maps it to a generic response anyway."""
    store = SqliteAccountStore(db_path)
    _inject_exec(monkeypatch, store, ["COMMIT"])
    with pytest.raises(AccountStoreCommitError) as ei:
        with store._write() as c:
            c.execute("SELECT 1")
    monkeypatch.undo()
    msg = str(ei.value)
    for leak in ("accounts", "email_tokens", "password_hash", "SELECT", "UPDATE",
                 "INSERT", store._path):
        assert leak not in msg


# --- §14 dependency-bounded shared-helper sweep ----------------------------
def test_sweep_no_public_method_nests_a_second_write_transaction(db_path):
    """§7/§14 — no reset path calls a public method that owns another ``_write()``
    transaction, and no nested transaction is introduced anywhere."""
    store = SqliteAccountStore(db_path)
    depth = {"max": 0, "cur": 0}
    real_write = SqliteAccountStore._write

    import contextlib

    @contextlib.contextmanager
    def counting_write(self):
        depth["cur"] += 1
        depth["max"] = max(depth["max"], depth["cur"])
        try:
            with real_write(self) as c:
                yield c
        finally:
            depth["cur"] -= 1

    aid = _mk(store, "sweepnest@example.com")
    raw = _acct.new_raw_token()
    store.create_email_token(_acct.new_account_id(), aid, RESET, _acct.hash_token(raw),
                             "2099-01-01T00:00:00.000000Z", "2026-01-01T00:00:00.000000Z")
    try:
        SqliteAccountStore._write = counting_write
        assert store.complete_password_reset(_acct.hash_token(raw), "nh",
                                             "2026-01-01T00:00:00.000000Z") == aid
        depth["max"] = 0
        store.increment_session_epoch(aid, "2026-01-01T00:00:01.000000Z")
    finally:
        SqliteAccountStore._write = real_write
    assert depth["max"] == 1                       # never more than one open at a time


def test_sweep_existing_write_callers_preserve_behaviour(db_path):
    """§14 — registration, account status, email verification, token
    issuance/consumption, rate-limit atomicity and commercial-assignment storage
    all keep their existing behaviour on the hardened helper. No commercial
    feature is activated."""
    store = SqliteAccountStore(db_path)
    now = "2026-01-01T00:00:00.000000Z"
    aid = _mk(store, "sweepcallers@example.com")
    assert store.get_account_by_id(aid)["status"] == "active"
    with pytest.raises(EmailExistsError):
        store.create_account(_acct.new_account_id(),
                             _acct.normalize_email("sweepcallers@example.com"),
                             "h", now)
    assert store.set_password_hash(aid, "another-hash", now) == 1
    assert store.mark_email_verified(aid, now) == 1
    assert store.set_status(aid, "disabled", now) == 1
    assert store.set_status(aid, "active", now) == 1
    raw = _acct.new_raw_token()
    store.create_email_token(_acct.new_account_id(), aid, VERIFICATION,
                             _acct.hash_token(raw), "2099-01-01T00:00:00.000000Z", now)
    assert store.consume_token(_acct.hash_token(raw), VERIFICATION, now) == aid
    assert store.consume_token(_acct.hash_token(raw), VERIFICATION, now) is None  # replay
    assert store.record_rate_attempt("subj", "login", now, "2099-01-01T00:00:00.000000Z", 3)
    assert store.supersede_tokens(aid, RESET, now) == 0


def test_sweep_no_caller_depends_on_suppressed_commit_failure(db_path, monkeypatch):
    """§14 — no AccountStore caller may keep depending on a suppressed COMMIT
    failure or continue on an unsafe connection: every write seam now surfaces it."""
    store = SqliteAccountStore(db_path)
    aid = _mk(store, "sweepsupp@example.com")
    now = "2026-01-01T00:00:00.000000Z"
    seams = [
        lambda: store.set_password_hash(aid, "h2", now),
        lambda: store.increment_session_epoch(aid, now),
        lambda: store.mark_email_verified(aid, now),
        lambda: store.set_status(aid, "disabled", now),
        lambda: store.supersede_tokens(aid, RESET, now),
    ]
    for seam in seams:
        state = _inject_exec(monkeypatch, store, ["COMMIT"])
        with pytest.raises(AccountStoreCommitError):
            seam()
        assert state["hits"] == 1
        monkeypatch.undo()


def test_sweep_epoch_password_and_reset_token_callers_inspected(db_path):
    """§14 — the epoch, password and reset-token callers are inspected together:
    authentication validation input, deactivation, reset replay and concurrency
    remain correct after the hardening."""
    store = SqliteAccountStore(db_path)
    now = "2026-01-01T00:00:00.000000Z"
    aid = _mk(store, "sweepepoch@example.com")
    assert store.get_account_by_id(aid)["session_epoch"] == 0
    assert store.increment_session_epoch(aid, now) == 1        # login-validation input
    store.set_status(aid, "disabled", now)                     # deactivation path
    assert store.increment_session_epoch(aid, now) == 2        # still exactly +1
    store.set_status(aid, "active", now)
    raw = _acct.new_raw_token()
    store.create_email_token(_acct.new_account_id(), aid, RESET, _acct.hash_token(raw),
                             "2099-01-01T00:00:00.000000Z", now)
    assert store.complete_password_reset(_acct.hash_token(raw), "nh", now) == aid
    assert store.complete_password_reset(_acct.hash_token(raw), "nh2", now) is None  # replay
    assert store.get_account_by_id(aid)["session_epoch"] == 3


def test_sweep_concurrent_writers_still_serialised_after_hardening(db_path):
    """§14 / P5-2-PRE-02 — the hardened helper keeps real concurrent writers
    serialised with no lost update and no thread-affinity error."""
    store = SqliteAccountStore(db_path)
    aid = _mk(store, "sweepconc@example.com")
    errors = []

    def bump():
        try:
            for _ in range(10):
                store.increment_session_epoch(aid, "2026-01-01T00:00:00.000000Z")
        except Exception as exc:                    # pragma: no cover - failure path
            errors.append(exc)

    threads = [_threading.Thread(target=bump) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(60)
    assert errors == []
    assert store.get_account_by_id(aid)["session_epoch"] == 40   # no lost updates
