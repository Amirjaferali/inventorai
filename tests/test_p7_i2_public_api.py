"""P7-I2 — Versioned Read/Export Public API + first-public-exposure security
baseline (RED/GREEN).

Behaviour-based tests for the ESTABLISHED P7-I2 bounded increment contract
(``docs/governance/P7_I2_VERSIONED_READ_EXPORT_PUBLIC_API_INCREMENT_CONTRACT.md``,
merged PR #405) covering its §16 RED plan including the A–E additions: machine
credential authentication (distinct from the browser session), owner-bound
authorization through the established P7-I1 seam, the single ``project:read``
scope, API + export version identity, the stable non-enumerating error envelope,
correlation identity (malformed caller value replaced), durable access audit
(fail-closed), two-tier protective rate limiting (pre-auth bounded-subject +
authenticated ``api_read``; both fail-closed), credential lifecycle
(revocation / expiry / rotation / inactive bound account / hash-only storage),
the schema-initialization boundary (no handler DDL, proven via connection trace
instrumentation), non-mutation, and the read-only route surface.

Real on-disk SQLite (autouse conftest isolation); the real record + account
stores; real Flask test clients. The API module is imported lazily inside
helpers so, before implementation, each test fails on the ABSENT BEHAVIOUR
(missing routes / missing store capability), not on collection-time import.
No broad ``pytest.raises(Exception)``; existing tests unchanged.
"""
import hashlib
import importlib
import json
import logging
import os

import pytest

import web.app as webapp
from web.app import app
from engine import account_credentials as _acct
from engine import read_export_service as _seam

PW = "correct horse battery staple"
IDEA = ("An electronic circuit uses a sensor and a switch to cut the power when "
        "the current gets too high.")
FORM = {"idea": IDEA, "domain_confirm": "electronics_electrical"}

READ_PATH = "/api/v1/projects/{pid}"
EXPORT_PATH = "/api/v1/projects/{pid}/export"


# ---------------------------------------------------------------------------
# helpers (real accounts, real owned projects, real credentials)
# ---------------------------------------------------------------------------
def _api():
    """Import the P7-I2 API module lazily so pre-implementation RED fails on the
    absent capability inside each test, not at collection."""
    return importlib.import_module("web.api_v1")


def _new_client():
    app.config["TESTING"] = True
    return app.test_client()


def _mk_account(email, verified=True, status="active"):
    store = webapp._get_account_store()
    aid = _acct.new_account_id()
    store.create_account(aid, _acct.normalize_email(email), _acct.hash_password(PW),
                         "2026-01-01T00:00:00.000000Z", status=status)
    if verified:
        store.mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    return aid


def _client_for(email):
    aid = _mk_account(email)
    c = _new_client()
    c.post("/login", data={"email": email, "password": PW})
    return c, aid


def _start_project(client):
    r = client.post("/start", data=FORM)
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/session/", 1)[-1]


def _owned_project(email="owner@example.com"):
    """A real verified account + a real durable owned project; returns
    (account_id, project_id, browser_client)."""
    c, aid = _client_for(email)
    pid = _start_project(c)
    return aid, pid, c


def _issue(owner_account_id, scopes=None, expires_at=None):
    api = _api()
    return api.issue_api_credential(
        webapp._get_account_store(), owner_account_id,
        scopes=scopes, expires_at=expires_at)


def _bearer(credential_id, secret):
    return {"Authorization": "Bearer %s.%s" % (credential_id, secret)}


def _err(resp):
    body = resp.get_json()
    assert body is not None, "public error must be the stable JSON envelope"
    return body["error"]


# ===========================================================================
# Authentication denials (RED 1–9)
# ===========================================================================
def test_no_credential_denied():
    _aid, pid, _c = _owned_project()
    r = _new_client().get(READ_PATH.format(pid=pid))
    assert r.status_code == 401
    assert _err(r)["code"] == "unauthenticated"


def test_malformed_credential_denied():
    _aid, pid, _c = _owned_project()
    r = _new_client().get(READ_PATH.format(pid=pid),
                          headers={"Authorization": "Bearer no-dot-in-here"})
    assert r.status_code == 401
    assert _err(r)["code"] == "unauthenticated"


def test_unknown_credential_denied():
    _aid, pid, _c = _owned_project()
    r = _new_client().get(READ_PATH.format(pid=pid),
                          headers=_bearer("apic_" + "0" * 32, "wrong-secret"))
    assert r.status_code == 401
    assert _err(r)["code"] == "unauthenticated"


def test_invalid_secret_denied():
    aid, pid, _c = _owned_project()
    cred_id, _secret = _issue(aid)
    r = _new_client().get(READ_PATH.format(pid=pid),
                          headers=_bearer(cred_id, "not-the-real-secret"))
    assert r.status_code == 401
    assert _err(r)["code"] == "unauthenticated"


def test_revoked_credential_denied():
    aid, pid, _c = _owned_project()
    cred_id, secret = _issue(aid)
    webapp._get_account_store().revoke_api_credential(
        cred_id, "2026-01-02T00:00:00.000000Z")
    r = _new_client().get(READ_PATH.format(pid=pid), headers=_bearer(cred_id, secret))
    assert r.status_code == 401
    assert _err(r)["code"] == "unauthenticated"


def test_expired_credential_denied():
    aid, pid, _c = _owned_project()
    cred_id, secret = _issue(aid, expires_at="2000-01-01T00:00:00.000000Z")
    r = _new_client().get(READ_PATH.format(pid=pid), headers=_bearer(cred_id, secret))
    assert r.status_code == 401
    assert _err(r)["code"] == "unauthenticated"


@pytest.mark.parametrize("account_status", ["disabled", "deleted"])
def test_inactive_bound_account_denied(account_status):
    aid, pid, _c = _owned_project()
    cred_id, secret = _issue(aid)
    webapp._get_account_store().set_status(aid, account_status,
                                           "2026-01-02T00:00:00.000000Z")
    r = _new_client().get(READ_PATH.format(pid=pid), headers=_bearer(cred_id, secret))
    assert r.status_code == 401
    assert _err(r)["code"] == "unauthenticated"


def test_insufficient_scope_denied():
    aid, pid, _c = _owned_project()
    cred_id, secret = _issue(aid, scopes=("other:scope",))
    r = _new_client().get(READ_PATH.format(pid=pid), headers=_bearer(cred_id, secret))
    assert r.status_code == 403
    assert _err(r)["code"] == "forbidden"


def test_browser_session_alone_does_not_authenticate_api():
    """A fully logged-in browser client (signed session cookie, no machine
    credential) must NOT authenticate the public API."""
    _aid, pid, browser = _owned_project()
    # the browser session works on the web surface
    assert browser.get("/session/%s" % pid).status_code == 200
    r = browser.get(READ_PATH.format(pid=pid))
    assert r.status_code == 401
    assert _err(r)["code"] == "unauthenticated"


# ===========================================================================
# Authorized success paths (RED 10–11, 14–15)
# ===========================================================================
def test_authorized_project_read_succeeds_data_minimized():
    aid, pid, _c = _owned_project()
    cred_id, secret = _issue(aid)
    r = _new_client().get(READ_PATH.format(pid=pid), headers=_bearer(cred_id, secret))
    assert r.status_code == 200
    body = r.get_json()
    assert body["api_version"] == "v1"
    assert body["request_id"]
    project = body["project"]
    # resource identity == the durable record's idea_id (the sid/project_id is
    # the routing capability; the durable contract carries its own idea_id)
    assert project["idea_id"] == webapp._get_store().load_contract(pid).idea_id
    # data-minimized projection — NOT a blind ProjectRecordContract.to_dict()
    assert set(project.keys()) == {"idea_id", "assertion_count"}
    assert isinstance(project["assertion_count"], int)


def test_authorized_structured_export_succeeds():
    aid, pid, _c = _owned_project()
    cred_id, secret = _issue(aid)
    r = _new_client().get(EXPORT_PATH.format(pid=pid), headers=_bearer(cred_id, secret))
    assert r.status_code == 200
    body = r.get_json()
    assert body["api_version"] == "v1"
    assert body["export_contract_version"] == "1"
    assert body["request_id"]
    export = body["export"]
    assert export["idea_id"] == webapp._get_store().load_contract(pid).idea_id
    assert "domain_support_state" in export
    assert "assertion_count" in export


def test_api_version_identity_on_both_surfaces():
    aid, pid, _c = _owned_project()
    cred_id, secret = _issue(aid)
    for path in (READ_PATH, EXPORT_PATH):
        r = _new_client().get(path.format(pid=pid), headers=_bearer(cred_id, secret))
        assert r.get_json()["api_version"] == "v1"


# ===========================================================================
# Non-enumeration (RED 12–13)
# ===========================================================================
def test_cross_owner_and_missing_project_indistinguishable():
    aid_a, pid_a, _ca = _owned_project("owner-a@example.com")
    aid_b = _mk_account("owner-b@example.com")
    cred_id, secret = _issue(aid_b)
    missing_pid = "does-not-exist-0000"

    responses = []
    for pid in (pid_a, missing_pid):
        for path in (READ_PATH, EXPORT_PATH):
            r = _new_client().get(path.format(pid=pid),
                                  headers=_bearer(cred_id, secret))
            responses.append(r)

    normalized = set()
    for r in responses:
        assert r.status_code == 404
        err = _err(r)
        assert err["code"] == "not_available"
        assert err["request_id"]
        body = r.get_json()
        body["error"]["request_id"] = "X"
        normalized.add((r.status_code, json.dumps(body, sort_keys=True)))
    # identical status + identical body shape/message for cross-owner and missing
    assert len(normalized) == 1


# ===========================================================================
# Error envelope + correlation identity (RED 16–18)
# ===========================================================================
def test_stable_error_envelope_shape():
    _aid, pid, _c = _owned_project()
    r = _new_client().get(READ_PATH.format(pid=pid))
    body = r.get_json()
    assert set(body.keys()) == {"error"}
    assert set(body["error"].keys()) == {"code", "message", "request_id"}
    # no internal detail leaks
    text = json.dumps(body)
    for needle in ("Traceback", "sqlite", "Exception", "SELECT"):
        assert needle not in text


def test_request_id_present_on_success_and_error():
    aid, pid, _c = _owned_project()
    cred_id, secret = _issue(aid)
    ok = _new_client().get(READ_PATH.format(pid=pid), headers=_bearer(cred_id, secret))
    assert ok.get_json()["request_id"]
    denied = _new_client().get(READ_PATH.format(pid=pid))
    assert _err(denied)["request_id"]


def test_valid_supplied_request_id_is_echoed():
    aid, pid, _c = _owned_project()
    cred_id, secret = _issue(aid)
    headers = dict(_bearer(cred_id, secret))
    headers["X-Request-Id"] = "caller-supplied-0001"
    r = _new_client().get(READ_PATH.format(pid=pid), headers=headers)
    assert r.get_json()["request_id"] == "caller-supplied-0001"


def test_malformed_supplied_request_id_replaced():
    aid, pid, _c = _owned_project()
    cred_id, secret = _issue(aid)
    malformed = "bad id!!<script>%s" % ("x" * 200)
    headers = dict(_bearer(cred_id, secret))
    headers["X-Request-Id"] = malformed
    r = _new_client().get(READ_PATH.format(pid=pid), headers=headers)
    rid = r.get_json()["request_id"]
    assert rid != malformed
    assert "<" not in rid and " " not in rid and "!" not in rid
    import re
    assert re.fullmatch(r"[A-Za-z0-9-]{1,64}", rid)


# ===========================================================================
# Audit (RED 19–20)
# ===========================================================================
def test_audit_event_recorded_for_served_and_denied():
    aid, pid, _c = _owned_project()
    cred_id, secret = _issue(aid)
    store = webapp._get_account_store()

    ok = _new_client().get(READ_PATH.format(pid=pid), headers=_bearer(cred_id, secret))
    rid_ok = ok.get_json()["request_id"]
    denied = _new_client().get(READ_PATH.format(pid=pid))
    rid_denied = _err(denied)["request_id"]

    events = store.list_access_audit()
    by_rid = {e["request_id"]: e for e in events}
    served = by_rid[rid_ok]
    assert served["outcome"] == "served"
    assert served["credential_id"] == cred_id
    assert served["surface"] == "project_read"
    assert served["project_id"] == pid
    assert served["created_at"]
    deny = by_rid[rid_denied]
    assert deny["outcome"].startswith("denied")
    assert deny["credential_id"] is None
    # the secret never appears in any audit field
    for e in events:
        assert secret not in json.dumps(e, default=str)


def test_audit_write_failure_fails_closed(monkeypatch):
    aid, pid, _c = _owned_project()
    cred_id, secret = _issue(aid)
    store = webapp._get_account_store()

    def _boom(*a, **k):
        raise RuntimeError("audit store unavailable")

    monkeypatch.setattr(store, "record_access_audit", _boom)
    r = _new_client().get(READ_PATH.format(pid=pid), headers=_bearer(cred_id, secret))
    assert r.status_code == 500
    assert _err(r)["code"] == "internal_error"
    # the project payload is NOT served without its audit event
    assert "project" not in (r.get_json() or {})


# ===========================================================================
# Rate limiting — pre-auth tier (RED 21–24)
# ===========================================================================
def test_preauth_limiter_counts_unknown_credentials(monkeypatch):
    _aid, pid, _c = _owned_project()
    api = _api()
    monkeypatch.setattr(api, "_PREAUTH_RATE_LIMIT", 3)
    c = _new_client()
    headers = _bearer("apic_" + "f" * 32, "junk-secret")
    for _ in range(3):
        assert c.get(READ_PATH.format(pid=pid), headers=headers).status_code == 401
    r = c.get(READ_PATH.format(pid=pid), headers=headers)
    assert r.status_code == 429
    assert _err(r)["code"] == "rate_limited"


def test_preauth_limiter_counts_invalid_secret_and_runs_before_verification(monkeypatch):
    """Invalid-secret attempts consume the same presented-id bucket, and once the
    threshold is exceeded even the CORRECT secret is throttled — proving the
    limiter runs before secret verification."""
    aid, pid, _c = _owned_project()
    cred_id, secret = _issue(aid)
    api = _api()
    monkeypatch.setattr(api, "_PREAUTH_RATE_LIMIT", 3)
    c = _new_client()
    for _ in range(3):
        r = c.get(READ_PATH.format(pid=pid), headers=_bearer(cred_id, "wrong"))
        assert r.status_code == 401
    r = c.get(READ_PATH.format(pid=pid), headers=_bearer(cred_id, secret))
    assert r.status_code == 429
    assert _err(r)["code"] == "rate_limited"


def test_oversized_junk_identifier_never_stored_raw_as_limiter_subject():
    _aid, pid, _c = _owned_project()
    junk = "A" * 8192
    r = _new_client().get(READ_PATH.format(pid=pid),
                          headers={"Authorization": "Bearer %s.junk" % junk})
    assert r.status_code == 401
    store = webapp._get_account_store()
    with store._read() as conn:
        subjects = [row[0] for row in
                    conn.execute("SELECT subject_key FROM auth_rate_limits").fetchall()]
    assert subjects, "the pre-auth attempt must consume the limiter"
    for s in subjects:
        assert len(s) <= 64, "limiter subject must be a bounded fixed-size digest"
        assert junk not in s


# ===========================================================================
# Rate limiting — authenticated tier + store failure (RED 25–26)
# ===========================================================================
def test_authenticated_api_read_limiter_enforced(monkeypatch):
    aid, pid, _c = _owned_project()
    cred_id, secret = _issue(aid)
    api = _api()
    monkeypatch.setattr(api, "_API_READ_RATE_LIMIT", 2)
    c = _new_client()
    for _ in range(2):
        assert c.get(READ_PATH.format(pid=pid),
                     headers=_bearer(cred_id, secret)).status_code == 200
    r = c.get(READ_PATH.format(pid=pid), headers=_bearer(cred_id, secret))
    assert r.status_code == 429
    assert _err(r)["code"] == "rate_limited"


def test_rate_limit_store_failure_fails_closed(monkeypatch):
    aid, pid, _c = _owned_project()
    cred_id, secret = _issue(aid)
    store = webapp._get_account_store()

    def _boom(*a, **k):
        raise RuntimeError("rate-limit store unavailable")

    monkeypatch.setattr(store, "record_rate_attempt", _boom)
    r = _new_client().get(READ_PATH.format(pid=pid), headers=_bearer(cred_id, secret))
    assert r.status_code == 500
    assert _err(r)["code"] == "internal_error"
    assert "project" not in (r.get_json() or {})


# ===========================================================================
# Credential lifecycle — rotation + hash-only storage (RED 27–29)
# ===========================================================================
def test_rotation_old_denied_new_accepted():
    aid, pid, _c = _owned_project()
    old_id, old_secret = _issue(aid)
    assert _new_client().get(READ_PATH.format(pid=pid),
                             headers=_bearer(old_id, old_secret)).status_code == 200
    new_id, new_secret = _issue(aid)
    webapp._get_account_store().revoke_api_credential(
        old_id, "2026-01-02T00:00:00.000000Z")
    assert _new_client().get(READ_PATH.format(pid=pid),
                             headers=_bearer(old_id, old_secret)).status_code == 401
    assert _new_client().get(READ_PATH.format(pid=pid),
                             headers=_bearer(new_id, new_secret)).status_code == 200


def test_secret_stored_hash_only():
    aid, _pid, _c = _owned_project()
    cred_id, secret = _issue(aid)
    store = webapp._get_account_store()
    row = store.get_api_credential(cred_id)
    assert row["secret_hash"] == _acct.hash_token(secret)
    assert row["secret_hash"] != secret
    with store._read() as conn:
        raw = conn.execute("SELECT * FROM api_credentials WHERE credential_id = ?",
                           (cred_id,)).fetchone()
    for value in raw:
        assert value is None or secret not in str(value)


def test_secret_not_leaked_in_logs_or_responses(caplog):
    aid, pid, _c = _owned_project()
    with caplog.at_level(logging.DEBUG):
        cred_id, secret = _issue(aid)
        ok = _new_client().get(READ_PATH.format(pid=pid),
                               headers=_bearer(cred_id, secret))
        bad = _new_client().get(READ_PATH.format(pid=pid),
                                headers=_bearer(cred_id, "wrong-secret"))
    assert secret not in caplog.text
    assert secret not in ok.get_data(as_text=True)
    assert secret not in bad.get_data(as_text=True)


# ===========================================================================
# P7-I1 seam reuse (RED 30)
# ===========================================================================
def test_p7_i1_seam_is_consumed(monkeypatch):
    aid, pid, _c = _owned_project()
    cred_id, secret = _issue(aid)
    calls = {"read": [], "export": []}

    real_read = _seam.get_authorized_project_read
    real_export = _seam.produce_project_export

    def spy_read(store, project_id, account_id):
        calls["read"].append((project_id, account_id))
        return real_read(store, project_id, account_id)

    def spy_export(store, project_id, account_id):
        calls["export"].append((project_id, account_id))
        return real_export(store, project_id, account_id)

    monkeypatch.setattr(_seam, "get_authorized_project_read", spy_read)
    monkeypatch.setattr(_seam, "produce_project_export", spy_export)

    assert _new_client().get(READ_PATH.format(pid=pid),
                             headers=_bearer(cred_id, secret)).status_code == 200
    assert _new_client().get(EXPORT_PATH.format(pid=pid),
                             headers=_bearer(cred_id, secret)).status_code == 200
    assert calls["read"] == [(pid, aid)]
    assert calls["export"] == [(pid, aid)]


# ===========================================================================
# Schema-initialization boundary (RED 31) + non-mutation (RED 32)
# ===========================================================================
def test_public_routes_execute_no_ddl(monkeypatch):
    """Call-boundary instrumentation (contract §16.D): with both stores already
    constructed, trace every SQL statement executed during public API request
    processing and assert none is DDL/migration."""
    aid, pid, _c = _owned_project()
    cred_id, secret = _issue(aid)
    account_store = webapp._get_account_store()
    record_store = webapp._get_store()

    statements = []
    account_store._conn.set_trace_callback(statements.append)
    record_store._conn.set_trace_callback(statements.append)
    try:
        c = _new_client()
        assert c.get(READ_PATH.format(pid=pid),
                     headers=_bearer(cred_id, secret)).status_code == 200
        assert c.get(EXPORT_PATH.format(pid=pid),
                     headers=_bearer(cred_id, secret)).status_code == 200
        assert c.get(READ_PATH.format(pid=pid)).status_code == 401
    finally:
        account_store._conn.set_trace_callback(None)
        record_store._conn.set_trace_callback(None)

    assert statements, "instrumentation must have captured request-time SQL"
    for sql in statements:
        upper = sql.upper()
        for forbidden in ("CREATE TABLE", "CREATE INDEX", "ALTER TABLE",
                          "DROP TABLE", "PRAGMA "):
            assert forbidden not in upper, "handler executed DDL/migration: %s" % sql


def test_public_reads_do_not_mutate_project_state():
    aid, pid, _c = _owned_project()
    cred_id, secret = _issue(aid)
    before = webapp._get_store().load_contract(pid).to_json()
    c = _new_client()
    assert c.get(READ_PATH.format(pid=pid),
                 headers=_bearer(cred_id, secret)).status_code == 200
    assert c.get(EXPORT_PATH.format(pid=pid),
                 headers=_bearer(cred_id, secret)).status_code == 200
    after = webapp._get_store().load_contract(pid).to_json()
    assert before == after


# ===========================================================================
# Route surface: read-only, exactly two, no P7-I3 (RED 33–34)
# ===========================================================================
def test_no_write_methods_on_api_routes():
    aid, pid, _c = _owned_project()
    cred_id, secret = _issue(aid)
    c = _new_client()
    for path in (READ_PATH.format(pid=pid), EXPORT_PATH.format(pid=pid)):
        for method in ("post", "put", "patch", "delete"):
            r = getattr(c, method)(path, headers=_bearer(cred_id, secret))
            assert r.status_code == 405, (method, path, r.status_code)


def test_exactly_two_public_api_routes_registered():
    _api()  # ensure the module is importable/mounted
    api_rules = {str(rule) for rule in app.url_map.iter_rules()
                 if str(rule).startswith("/api/")}
    assert api_rules == {"/api/v1/projects/<project_id>",
                         "/api/v1/projects/<project_id>/export"}
    for rule in app.url_map.iter_rules():
        if str(rule).startswith("/api/"):
            methods = rule.methods - {"HEAD", "OPTIONS"}
            assert methods == {"GET"}


def test_no_p7_i3_adapter_or_outbound_vendor_code():
    """The API module imports only the bounded allowlist (stdlib + Flask + the
    existing engine/web modules) — no outbound HTTP client, no vendor SDK — and
    no P7-I3 adapter module entered the engine."""
    import ast
    api = _api()
    with open(api.__file__, "r", encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module or "")
    allowed_tops = {"hashlib", "hmac", "re", "uuid", "flask", "engine", "web"}
    for mod in imported:
        assert mod.split(".")[0] in allowed_tops, mod
    engine_dir = os.path.join(os.path.dirname(os.path.dirname(api.__file__)),
                              "engine")
    assert not [n for n in os.listdir(engine_dir) if "adapter" in n.lower()]


# ===========================================================================
# Issuance path invariants
# ===========================================================================
def test_issuance_binds_owner_scope_and_stable_credential_id():
    aid, _pid, _c = _owned_project()
    cred_id, secret = _issue(aid)
    row = webapp._get_account_store().get_api_credential(cred_id)
    assert row["owner_account_id"] == aid
    assert row["scopes"] == "project:read"
    assert row["status"] == "active"
    assert row["expires_at"] is None
    assert cred_id.startswith("apic_")
    assert len(secret) >= 32


def test_preauth_subject_is_fixed_size_digest():
    api = _api()
    a = api._presented_subject("apic_" + "1" * 32)
    b = api._presented_subject("Z" * 5000)
    assert len(a) == len(b) == 32
    assert a != b
    assert all(ch in "0123456789abcdef" for ch in a + b)
