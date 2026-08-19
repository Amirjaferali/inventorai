"""P10-D3b — Account Deactivation (RED/GREEN).

Behaviour-based tests for the bounded gate defined by
``docs/governance/P10_D3B_ACCOUNT_DEACTIVATION_INCREMENT_CONTRACT.md``
(merged PR #512, authoritative).

ONE self-service account state transition — Deactivate Account — for a currently
authenticated account: POST-only, CSRF-protected, password re-entry required.
Consumes ONLY existing seams (``set_status``, ``increment_session_epoch``,
``verify_password``, ``_current_account``, ``_csrf_valid``/``_csrf_reject``).
It is DEACTIVATION, not deletion: no row in any table is removed; the account
row remains with ``status="deleted"`` and a stamped ``deleted_at``; sessions,
future logins, and API-credential authentication all fail through the EXISTING
status-gated denial machinery; append-only/audit history is untouched.

Real on-disk SQLite (autouse conftest isolation); real signed Flask sessions;
the real account/record stores and P7-I2 credential auth. The only mock is one
deliberate store-failure proxy for the fail-closed test.
"""
import os
import re

import pytest

import web.app as webapp
from web.app import app
from engine import account_credentials as _acct
from web.api_v1 import issue_api_credential

PW = "correct horse battery staple"
IDEA = ("An electronic circuit uses a sensor and a switch to cut the power when "
        "the current gets too high.")
FORM = {"idea": IDEA, "domain_confirm": "electronics_electrical"}

DEACTIVATE_PATH = "/account/deactivate"

# The 14 durable table families the contract §7 requires preserved.
PRESERVED_TABLES = (
    "accounts", "projects", "records", "email_tokens", "api_credentials",
    "commercial_assignments", "commercial_audit", "commercial_usage",
    "commercial_usage_idempotency", "subscription_lifecycle_events",
    "subscription_lifecycle_state", "provider_mapping", "provider_event_dedupe",
    "access_audit",
)


@pytest.fixture
def db_path():
    return os.environ["INVENTORAI_DB_PATH"]


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
    r = c.post("/login", data={"email": email, "password": PW})
    assert r.status_code == 302, r.status_code
    return c, aid


def _csrf(client):
    body = client.get("/account").get_data(as_text=True)
    m = re.search(r'name="csrf_token" value="([^"]+)"', body)
    assert m, "no csrf token on /account"
    return m.group(1)


def _start_project(client):
    r = client.post("/start", data=FORM)
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/session/", 1)[-1]


def _account_row(aid):
    return webapp._get_account_store().get_account_by_id(aid)


def _row_signature(aid):
    """Everything deactivation may NOT change on a failed guard."""
    row = _account_row(aid)
    return (row["status"], row["deleted_at"], row["session_epoch"],
            row["updated_at"])


def _deactivate(client, password=PW, csrf="__fetch__", extra=None):
    data = {"password": password}
    if csrf == "__fetch__":
        data["csrf_token"] = _csrf(client)
    elif csrf is not None:
        data["csrf_token"] = csrf
    if extra:
        data.update(extra)
    return client.post(DEACTIVATE_PATH, data=data, follow_redirects=False)


def _table_counts():
    store = webapp._get_account_store()
    return {t: store._conn.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0]
            for t in PRESERVED_TABLES}


def _bearer(credential_id, secret):
    return {"Authorization": "Bearer %s.%s" % (credential_id, secret)}


# ===========================================================================
# Guard failures: no mutation of any kind
# ===========================================================================
def test_anonymous_caller_cannot_deactivate(db_path):
    _client_for("d3b-bystander@example.com")   # unrelated existing account
    anon = _new_client()
    r = anon.post(DEACTIVATE_PATH, data={"password": PW}, follow_redirects=False)
    assert r.status_code == 302
    assert "/login" in r.headers["Location"]


def test_wrong_password_does_not_deactivate(db_path):
    client, aid = _client_for("d3b-wrongpw@example.com")
    before = _row_signature(aid)
    r = _deactivate(client, password="not the right password")
    assert r.status_code != 302 or DEACTIVATE_PATH in r.headers.get("Location", "")
    assert _row_signature(aid) == before          # byte-identical account row
    assert _account_row(aid)["status"] == "active"


def test_missing_csrf_does_not_deactivate(db_path):
    client, aid = _client_for("d3b-nocsrf@example.com")
    before = _row_signature(aid)
    r = _deactivate(client, csrf=None)
    assert r.status_code == 403
    assert _row_signature(aid) == before


def test_invalid_csrf_does_not_deactivate(db_path):
    client, aid = _client_for("d3b-badcsrf@example.com")
    before = _row_signature(aid)
    r = _deactivate(client, csrf="forged-token-value")
    assert r.status_code == 403
    assert _row_signature(aid) == before


# ===========================================================================
# Successful deactivation: bounded status transition only
# ===========================================================================
def test_correct_password_and_csrf_deactivates(db_path):
    client, aid = _client_for("d3b-success@example.com")
    r = _deactivate(client)
    assert r.status_code == 302, (r.status_code, r.get_data(as_text=True)[:200])
    assert _account_row(aid)["status"] == "deleted"


def test_account_row_remains_physically_present(db_path):
    client, aid = _client_for("d3b-rowkept@example.com")
    _deactivate(client)
    row = _account_row(aid)
    assert row is not None
    assert row["account_id"] == aid


def test_status_becomes_deleted_and_deleted_at_stamped(db_path):
    client, aid = _client_for("d3b-stamp@example.com")
    assert _account_row(aid)["deleted_at"] is None
    _deactivate(client)
    row = _account_row(aid)
    assert row["status"] == "deleted"
    assert row["deleted_at"] is not None


# ===========================================================================
# Session invalidation (proved behaviourally, not asserted from epoch)
# ===========================================================================
def test_current_session_unusable_after_deactivation(db_path):
    client, _aid = _client_for("d3b-cursession@example.com")
    _deactivate(client)
    r = client.get("/account", follow_redirects=False)
    assert r.status_code == 302
    assert "/login" in r.headers["Location"]


def test_second_preexisting_session_unusable_after_deactivation(db_path):
    email = "d3b-twosessions@example.com"
    first, _aid = _client_for(email)
    second = _new_client()                      # a second, independent browser
    assert second.post("/login", data={"email": email, "password": PW}
                       ).status_code == 302
    assert second.get("/account").status_code == 200   # usable before

    _deactivate(first)

    r = second.get("/account", follow_redirects=False)
    assert r.status_code == 302
    assert "/login" in r.headers["Location"]


def test_future_login_denied_after_deactivation(db_path):
    email = "d3b-relogin@example.com"
    client, _aid = _client_for(email)
    _deactivate(client)
    fresh = _new_client()
    r = fresh.post("/login", data={"email": email, "password": PW},
                   follow_redirects=False)
    assert r.status_code == 401                 # the generic login failure


# ===========================================================================
# API credential behaviour (load-bearing): unusable but RETAINED
# ===========================================================================
def test_api_credential_unusable_after_deactivation_but_row_present(db_path):
    email = "d3b-apicred@example.com"
    client, aid = _client_for(email)
    pid = _start_project(client)
    cred_id, secret = issue_api_credential(webapp._get_account_store(), aid)

    api = _new_client()
    before = api.get("/api/v1/projects/%s" % pid, headers=_bearer(cred_id, secret))
    assert before.status_code == 200            # valid before deactivation

    _deactivate(client)

    after = api.get("/api/v1/projects/%s" % pid, headers=_bearer(cred_id, secret))
    assert after.status_code == 401             # bound account non-active

    row = webapp._get_account_store().get_api_credential(cred_id)
    assert row is not None                      # NOT deleted
    assert row["status"] == "active"            # NOT individually revoked
    assert row["revoked_at"] is None


# ===========================================================================
# Data preservation: nothing is physically deleted anywhere
# ===========================================================================
def test_full_data_preservation_across_all_fourteen_tables(db_path):
    email = "d3b-preserve@example.com"
    # register through the real route so email_tokens rows exist
    client = _new_client()
    client.post("/register", data={"email": email, "password": PW,
                                   "password_confirm": PW})
    aid = webapp._get_account_store().get_account_by_normalized_email(
        _acct.normalize_email(email))["account_id"]
    webapp._get_account_store().mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    assert client.post("/login", data={"email": email, "password": PW}
                       ).status_code == 302

    pid = _start_project(client)
    # durable record row via the real answer path (server-issued answer token)
    session_html = client.get("/session/%s" % pid).get_data(as_text=True)
    token = re.search(r'name="answer_token" value="([^"]+)"', session_html).group(1)
    client.post("/session/%s" % pid,
                data={"response": "The sensor measures current and opens the switch.",
                      "answer_token": token})
    cred_id, secret = issue_api_credential(webapp._get_account_store(), aid)
    api = _new_client()
    assert api.get("/api/v1/projects/%s" % pid,
                   headers=_bearer(cred_id, secret)).status_code == 200  # audit rows

    before = _table_counts()
    assert before["accounts"] >= 1 and before["projects"] >= 1
    assert before["records"] >= 1 and before["email_tokens"] >= 1
    assert before["api_credentials"] >= 1 and before["access_audit"] >= 1

    r = _deactivate(client)
    assert r.status_code == 302

    after = _table_counts()
    assert after == before, (before, after)     # zero rows deleted anywhere

    exists, owner = webapp._get_store().load_owner(pid)
    assert exists and owner == aid              # owned project row intact


# ===========================================================================
# UI / i18n truthfulness
# ===========================================================================
_FORBIDDEN_EN = ("delete account", "delete all my data", "erase account data",
                 "permanent erasure", "permanently delete", "right to erasure",
                 "data deleted")
_FORBIDDEN_AR = ("حذف الحساب", "حذف كل بياناتي", "مسح بيانات الحساب")


def _account_page(client, lang):
    r = client.post("/ui-language", data={"lang": lang})
    assert r.status_code == 302
    page = client.get("/account")
    assert page.status_code == 200
    return page.get_data(as_text=True)


def test_english_label_truthful_and_no_forbidden_wording(db_path):
    client, _aid = _client_for("d3b-label-en@example.com")
    html = _account_page(client, "en")
    assert "Deactivate Account" in html
    lowered = html.lower()
    for bad in _FORBIDDEN_EN:
        assert bad not in lowered, bad


def test_arabic_label_truthful_and_no_forbidden_wording(db_path):
    client, _aid = _client_for("d3b-label-ar@example.com")
    html = _account_page(client, "ar")
    assert "تعطيل الحساب" in html
    for bad in _FORBIDDEN_AR:
        assert bad not in html, bad


def test_success_response_makes_no_erasure_claim(db_path):
    client, _aid = _client_for("d3b-notice@example.com")
    r = _deactivate(client)
    assert r.status_code == 302
    landing = client.get(r.headers["Location"]).get_data(as_text=True).lower()
    for bad in ("data deleted", "erased", "permanently deleted"):
        assert bad not in landing, bad


# ===========================================================================
# Fail-closed on unexpected internal failure
# ===========================================================================
def test_unexpected_internal_failure_fails_closed(db_path, monkeypatch):
    client, aid = _client_for("d3b-failclosed@example.com")
    real_store = webapp._get_account_store()

    class _BoomStore:
        """Delegates everything except the mutation, which fails."""

        def __getattr__(self, name):
            return getattr(real_store, name)

        def set_status(self, *a, **kw):
            raise RuntimeError(
                "SECRET-INTERNAL-DETAIL: UPDATE accounts SET status")

    csrf = _csrf(client)                       # fetch BEFORE patching
    monkeypatch.setattr(webapp, "_get_account_store", lambda: _BoomStore())
    r = client.post(DEACTIVATE_PATH,
                    data={"password": PW, "csrf_token": csrf},
                    follow_redirects=False)
    monkeypatch.undo()

    assert r.status_code != 302 and r.status_code != 200
    for leak in (b"SECRET-INTERNAL-DETAIL", b"Traceback", b"RuntimeError",
                 b"UPDATE accounts"):
        assert leak not in r.data, leak
    assert _account_row(aid)["status"] == "active"   # nothing mutated


# ===========================================================================
# Route shape and existing invariants
# ===========================================================================
def test_no_get_mutation_route(db_path):
    client, aid = _client_for("d3b-noget@example.com")
    r = client.get(DEACTIVATE_PATH)
    assert r.status_code == 405
    assert _account_row(aid)["status"] == "active"

    matching = [rule for rule in app.url_map.iter_rules()
                if str(rule) == DEACTIVATE_PATH]
    assert len(matching) == 1
    assert matching[0].methods - {"HEAD", "OPTIONS"} == {"POST"}


def test_existing_route_invariants_unchanged():
    api_rules = {str(rule) for rule in app.url_map.iter_rules()
                 if str(rule).startswith("/api/")}
    assert api_rules == {"/api/v1/projects/<project_id>",
                         "/api/v1/projects/<project_id>/export"}
    all_rules = {str(rule) for rule in app.url_map.iter_rules()}
    assert "/logout" in all_rules and "/logout-all" in all_rules
    assert "/account/projects/<project_id>/export" in all_rules   # P10-D3a intact
    assert not any("draft" in r.lower() for r in all_rules)
