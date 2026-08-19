"""P10-SEC1 — Security Headers & Provider-Neutral Hardening (RED/GREEN).

Behaviour-based tests for the Owner-authorized bounded Phase-10 implementation
gate `P10-SEC1`: one centralized response-hardening seam applying, to EVERY
response (HTML, JSON, redirects, 4xx/5xx, static files, `/health`):

  * `Content-Security-Policy` — the smallest safe policy supported by the
    verified CSP compatibility inventory: `default-src 'none'` deny-by-default;
    `script-src 'self'` (the only script is the same-origin static
    `local_draft.js`; ZERO inline script bodies exist); `style-src
    'unsafe-inline'` (narrowly justified: every template styles itself through
    inline <style> blocks/attributes and no external stylesheet exists);
    `frame-ancestors 'none'`; `base-uri 'none'`; `form-action 'self'`.
    No `'unsafe-eval'`. No wildcard or scheme-broad sources.
  * `X-Content-Type-Options: nosniff`.
  * `X-Frame-Options: DENY` (no legitimate framing exists; consistent with
    `frame-ancestors 'none'`).
  * `Referrer-Policy: strict-origin-when-cross-origin` (no external links
    exist today; deny-leakage-by-default posture).

HSTS is DEFERRED (no TLS termination or trusted-proxy semantics exist in the
repository; sending it locally would be untruthful) — proven absent here.

The seam must not break anything: auth/CSRF/forms, export attachment headers,
the /health surface, and static-JS loading are re-proven with headers active.
"""
import json
import re

import pytest

import web.app as webapp
from web.app import app
from engine import account_credentials as _acct

PW = "correct horse battery staple"
NOW = "2026-01-01T00:00:00.000000Z"
IDEA = ("An electronic circuit uses a sensor and a switch to cut the power "
        "when the current gets too high.")

REQUIRED_DIRECTIVES = {
    "default-src": "'none'",
    "script-src": "'self'",
    "style-src": "'unsafe-inline'",
    "frame-ancestors": "'none'",
    "base-uri": "'none'",
    "form-action": "'self'",
}


def _new_client():
    app.config["TESTING"] = True
    return app.test_client()


def _mk_account(email):
    store = webapp._get_account_store()
    aid = "sec1-" + email.split("@")[0]
    store.create_account(aid, _acct.normalize_email(email),
                         _acct.hash_password(PW), NOW)
    store.mark_email_verified(aid, NOW)
    return aid


def _login(email):
    _mk_account(email)
    c = _new_client()
    r = c.post("/login", data={"email": email, "password": PW})
    assert r.status_code == 302
    return c


def _csp(response):
    header = response.headers.get("Content-Security-Policy")
    assert header, "Content-Security-Policy header missing"
    directives = {}
    for part in header.split(";"):
        part = part.strip()
        if part:
            name, _, value = part.partition(" ")
            directives[name] = value.strip()
    return header, directives


def _assert_hardened(response):
    """The complete P10-SEC1 header set, on any response."""
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert (response.headers.get("Referrer-Policy")
            == "strict-origin-when-cross-origin")
    _, directives = _csp(response)
    for name, value in REQUIRED_DIRECTIVES.items():
        assert directives.get(name) == value, (name, directives.get(name))


# ==========================================================================
# Header presence and content across every response class
# ==========================================================================
def test_html_landing_page_hardened():
    r = _new_client().get("/")
    assert r.status_code == 200
    _assert_hardened(r)


def test_auth_html_routes_hardened():
    client = _new_client()
    for path in ("/login", "/register", "/recover"):
        r = client.get(path)
        assert r.status_code == 200
        _assert_hardened(r)


def test_json_health_response_hardened():
    r = _new_client().get("/health")
    assert r.mimetype == "application/json"
    _assert_hardened(r)


def test_health_error_503_hardened(monkeypatch, tmp_path):
    bad = tmp_path / "corrupt.sqlite"
    bad.write_bytes(b"not a database" * 50)
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(bad))
    r = _new_client().get("/health")
    assert r.status_code == 503
    _assert_hardened(r)


def test_redirect_hardened():
    # POST /start without an idea redirects to the index — a real 302
    r = _new_client().post("/start", data={"idea": ""})
    assert r.status_code == 302
    _assert_hardened(r)


def test_404_hardened():
    r = _new_client().get("/no-such-path-p10-sec1")
    assert r.status_code == 404
    _assert_hardened(r)


def test_405_hardened():
    r = _new_client().get("/logout")     # POST-only route
    assert r.status_code == 405
    _assert_hardened(r)


def test_static_js_served_and_hardened():
    r = _new_client().get("/static/js/local_draft.js")
    assert r.status_code == 200
    assert "javascript" in r.mimetype
    _assert_hardened(r)


def test_authenticated_account_page_hardened():
    client = _login("sec1-acct@example.com")
    r = client.get("/account")
    assert r.status_code == 200
    _assert_hardened(r)


# ==========================================================================
# CSP content boundaries
# ==========================================================================
def test_csp_no_unsafe_eval_anywhere():
    header, _ = _csp(_new_client().get("/"))
    assert "unsafe-eval" not in header


def test_csp_no_wildcard_or_scheme_broad_sources():
    header, directives = _csp(_new_client().get("/"))
    assert "*" not in header
    for value in directives.values():
        for token in value.split():
            # only quoted keywords are permitted source expressions today —
            # no host, scheme, http:, https:, data:, or blob: sources
            assert token.startswith("'") and token.endswith("'"), token


def test_csp_scripts_never_unsafe_inline():
    _, directives = _csp(_new_client().get("/"))
    assert "unsafe-inline" not in directives["script-src"]


def test_hsts_absent_on_local_http():
    client = _new_client()
    for path in ("/", "/health", "/login"):
        r = client.get(path)
        assert "Strict-Transport-Security" not in r.headers, path
    # HSTS is DEFERRED: no TLS termination or trusted-proxy semantics exist
    # in the repository, so emitting it anywhere would be untruthful.


# ==========================================================================
# Compatibility: the CSP matches what the pages actually do
# ==========================================================================
def test_rendered_pages_have_no_inline_script_bodies_or_handlers():
    client = _login("sec1-scan@example.com")
    pages = [client.get(p).get_data(as_text=True)
             for p in ("/", "/login", "/register", "/recover", "/account")]
    for body in pages:
        for match in re.finditer(r"<script\b[^>]*>", body):
            assert "src=" in match.group(0), match.group(0)  # src-only scripts
        assert not re.search(r"\son(click|load|submit|change|input|key\w*)=",
                             body)
        assert "javascript:" not in body


def test_script_and_form_sources_are_same_origin():
    body = _new_client().get("/").get_data(as_text=True)
    for match in re.finditer(r'<script\b[^>]*src="([^"]+)"', body):
        assert match.group(1).startswith("/static/"), match.group(1)
    for match in re.finditer(r'<form\b[^>]*action="([^"]+)"', body):
        assert match.group(1).startswith("/"), match.group(1)


def test_auth_flow_functional_with_headers_active():
    email = "sec1-flow@example.com"
    client = _login(email)                      # register+login round trip
    r = client.get("/account")
    assert r.status_code == 200
    body = r.get_data(as_text=True)
    assert 'name="csrf_token"' in body          # CSRF form machinery intact
    r = client.post("/logout", data={"csrf_token": re.search(
        r'name="csrf_token" value="([^"]+)"', body).group(1)})
    assert r.status_code == 302
    _assert_hardened(r)


def test_export_attachment_headers_not_clobbered():
    client = _login("sec1-export@example.com")
    r = client.post("/start", data={"idea": IDEA,
                                    "domain_confirm": "electronics_electrical"})
    assert r.status_code == 302
    sid = r.headers["Location"].rsplit("/session/", 1)[-1]
    r = client.get("/account/projects/%s/export" % sid)
    assert r.status_code == 200
    assert r.headers["Content-Disposition"].startswith("attachment;")
    assert r.mimetype == "application/json"
    json.loads(r.get_data(as_text=True))
    _assert_hardened(r)


def test_headers_do_not_override_route_set_values():
    """The seam must be additive (setdefault semantics): if a response already
    carries one of the hardening headers, the seam must not overwrite it.
    Exercised directly on the registered after_request hook."""
    from flask import Response

    resp = Response("x")
    resp.headers["X-Frame-Options"] = "SAMEORIGIN"
    hardened = webapp._apply_security_headers(resp)
    assert hardened.headers.get("X-Frame-Options") == "SAMEORIGIN"
    assert hardened.headers.get("X-Content-Type-Options") == "nosniff"
    assert hardened.headers.get("Content-Security-Policy")
    # and the hook is actually registered with the Flask app
    assert any(f is webapp._apply_security_headers
               for funcs in app.after_request_funcs.values() for f in funcs)
