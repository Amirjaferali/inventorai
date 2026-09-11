"""R-05: real raw clients, signed cookies and storage; no CSRF-aware test client."""
import copy
import os
import pickle
import re
import sqlite3

import pytest
from werkzeug.datastructures import MultiDict

import web.app as webapp
from engine import account_credentials as credentials
from engine import auth_session


# Explicit browser mutation inventory: a new route requires a coverage decision.
MUTATIONS = (
    "/ui-language", "/register", "/login", "/account/deactivate", "/logout",
    "/logout-all", "/account/resend-verification", "/verify/<token>",
    "/recover", "/reset/<token>", "/start", "/start_ilt002_water_leak",
    "/start_ilt002_combination_lock", "/start_ilt002_combination_lock_path_n",
    "/session/<sid>/resume", "/session/<sid>/correct", "/session/<sid>/accept-risk",
    "/session/<sid>/decision/declare-context", "/session/<sid>/decision/declare-alternative",
    "/session/<sid>/decision/refine-alternative", "/session/<sid>/decision/withdraw-alternative",
    "/session/<sid>/keep-snapshot", "/session/<sid>/success-criteria", "/session/<sid>",
    "/session/<sid>/deliverable.pdf",
    # T2-A Quantified Requirements Slice 1: one new state-changing session
    # route, covered by the same missing/invalid-evidence matrix below.
    "/session/<sid>/requirement-quantity",
    "/decision-workspace", "/decision-workspace/<did>/input",
    "/decision-workspace/<did>/constraint", "/decision-workspace/<did>/gap",
    "/decision-workspace/<did>/evidence", "/decision-workspace/<did>/gap-assessment",
    "/decision-workspace/<did>/preference", "/decision-workspace/<did>/candidate",
)


def token_from(response):
    assert response.status_code == 200
    tokens = re.findall(r'name="csrf_token" value="([^"]+)"', response.get_data(as_text=True))
    assert tokens and len(set(tokens)) == 1
    return tokens[0]


@pytest.fixture
def browser(monkeypatch):
    webapp.app.config["TESTING"] = True
    monkeypatch.setattr(webapp, "FDC001_DECISIONS", {})
    monkeypatch.setattr(webapp, "FDC001_DECISION_OWNERS", {})
    return webapp.app.test_client()


def snapshot(client):
    with client.session_transaction() as session:
        cookie = copy.deepcopy(dict(session))
    with sqlite3.connect(os.environ["INVENTORAI_DB_PATH"]) as connection:
        database = list(connection.iterdump())
    memory = pickle.dumps((webapp.SESSION_STORE, webapp.FDC001_DECISIONS,
                           webapp.FDC001_DECISION_OWNERS))
    return cookie, database, memory


def test_inventory_covers_every_registered_unsafe_browser_route():
    actual = {rule.rule for rule in webapp.app.url_map.iter_rules()
              if rule.methods - {"GET", "HEAD", "OPTIONS"}}
    assert actual == set(MUTATIONS)


@pytest.mark.parametrize("route", MUTATIONS)
@pytest.mark.parametrize("authenticated", [False, True])
def test_missing_and_invalid_evidence_never_enters_route_or_mutates(browser, monkeypatch, route, authenticated):
    webapp._get_store()
    webapp._get_account_store()
    token = token_from(browser.get("/"))
    if authenticated:
        with browser.session_transaction() as session:
            session["auth"] = auth_session.build_session("r05-account", 0, webapp._utc_now())
            token = session["auth"]["csrf"]
    rule = next(rule for rule in webapp.app.url_map.iter_rules() if rule.rule == route and "POST" in rule.methods)

    def forbidden_view(**kwargs):
        pytest.fail("Invalid request entered protected view code")

    monkeypatch.setitem(webapp.app.view_functions, rule.endpoint, forbidden_view)
    before = snapshot(browser)
    path = route.replace("<token>", "r05-mail-token").replace("<sid>", "r05-project").replace("<did>", "r05-decision")
    for data in ({}, {"csrf_token": "wrong"}, {"csrf_token": "غير صالح"},
                 MultiDict([("csrf_token", token), ("csrf_token", token)])):
        response = browser.post(path, data=data)
        assert response.status_code == 403
        assert response.headers["Cache-Control"] == "no-store"
        assert snapshot(browser) == before


def test_token_is_browser_bound_and_not_accepted_from_query_or_json(browser):
    token = token_from(browser.get("/"))
    other = webapp.app.test_client()
    other_token = token_from(other.get("/"))
    assert token != other_token
    for response in (
        browser.post("/decision-workspace", data={"csrf_token": other_token}),
        other.post("/decision-workspace", data={"csrf_token": token}),
        browser.post("/decision-workspace?csrf_token=" + token),
        browser.post("/decision-workspace", json={"csrf_token": token}),
    ):
        assert response.status_code == 403
    before = len(webapp.FDC001_DECISIONS)
    response = browser.post("/decision-workspace", data={"csrf_token": token})
    assert response.status_code == 302
    assert len(webapp.FDC001_DECISIONS) == before + 1


def test_workspace_get_head_and_language_get_cannot_change_user_state(browser):
    token_from(browser.get("/"))
    before = pickle.dumps((webapp.FDC001_DECISIONS, webapp.FDC001_DECISION_OWNERS))
    for method in (browser.get, browser.head):
        assert method("/decision-workspace").status_code == 200
    assert pickle.dumps((webapp.FDC001_DECISIONS, webapp.FDC001_DECISION_OWNERS)) == before
    assert browser.get("/ui-language?lang=ar").status_code == 405
    with browser.session_transaction() as session:
        assert "ui_lang" not in session and "fdc001_created" not in session


def test_verification_get_does_not_consume_and_post_keeps_single_use(browser):
    from tests.test_p5_2_auth_sessions_verification_recovery import _mk_account
    from engine.account_store import VERIFICATION
    store = webapp._get_account_store()
    account_id = _mk_account(store, "r05-verify@example.com")
    raw = "r05-verification-secret"
    store.create_email_token("r05-email", account_id, VERIFICATION,
                             credentials.hash_token(raw), "2099-01-01T00:00:00.000000Z",
                             "2026-01-01T00:00:00.000000Z")
    token = token_from(browser.get("/verify/" + raw))
    before = snapshot(browser)
    assert browser.head("/verify/" + raw).status_code == 200
    assert snapshot(browser) == before
    assert browser.post("/verify/" + raw).status_code == 403
    assert snapshot(browser) == before
    assert not store.get_account_by_id(account_id)["email_verified"]
    response = browser.post("/verify/" + raw, data={"csrf_token": token})
    assert response.status_code == 200
    assert store.get_account_by_id(account_id)["email_verified"]
    replay = browser.post("/verify/" + raw, data={"csrf_token": token})
    assert b'result bad' in replay.data
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert raw not in response.get_data(as_text=True)


def test_login_rotates_anonymous_token_and_logout_revokes_authenticated_token(browser):
    from tests.test_p5_2_auth_sessions_verification_recovery import _mk_account, PW
    _mk_account(webapp._get_account_store(), "r05-login@example.com")
    anonymous = token_from(browser.get("/login"))
    assert browser.post("/login", data={"email": "r05-login@example.com", "password": PW,
                                       "csrf_token": anonymous}).status_code == 302
    authenticated = token_from(browser.get("/account"))
    assert anonymous != authenticated
    assert browser.post("/logout", data={"csrf_token": anonymous}).status_code == 403
    assert browser.post("/logout", data={"csrf_token": authenticated}).status_code == 302
    assert browser.post("/decision-workspace", data={"csrf_token": authenticated}).status_code == 403
    assert token_from(browser.get("/")) not in (anonymous, authenticated)


def test_arabic_rejection_and_form_headers_without_token_url_or_log(browser, caplog):
    token = token_from(browser.get("/"))
    assert browser.post("/ui-language", data={"lang": "ar", "next": "/login", "csrf_token": token}).location == "/login"
    response = browser.post("/decision-workspace")
    assert "رمز أمان الجلسة" in response.get_data(as_text=True)
    assert token not in response.get_data(as_text=True) and token not in caplog.text
    page = browser.get("/login")
    assert page.headers["Cache-Control"] == "no-store"
    assert '<html lang="ar" dir="rtl">' in page.get_data(as_text=True)
    assert not re.search(r'(?:href|action)="[^"]*' + re.escape(token), page.get_data(as_text=True))


def test_health_and_routing_failures_preserve_read_semantics(browser):
    response = browser.get("/health")
    assert response.status_code == 200 and "Set-Cookie" not in response.headers
    assert "no-store" not in response.headers.get("Cache-Control", "")
    assert browser.post("/route-that-does-not-exist").status_code == 404
    assert browser.post("/health").status_code == 405
