"""EMAIL-H1 — OBS-P5-2-01 bounded application-controlled token-exposure hardening.

File: tests/test_email_h1_token_link_exposure_hardening.py
Purpose: pin the APPLICATION-CONTROLLED portion of OBS-P5-2-01 (raw
verification/reset tokens appear in URL paths). This gate hardens only what the
application governs: token-bearing responses must send
``Referrer-Policy: no-referrer`` and ``Cache-Control: no-store``, the reset page
must not reflect the raw token into rendered HTML, token-bearing pages must load
no third-party resources, and the Flask/Python application logger must not emit
the raw token. The REPOSITORY-CONTROLLED Gunicorn access log is a DISTINCT
surface covered by `tests/test_email_h1_access_log_token_redaction.py`; a
provider/reverse-proxy access log is a THIRD surface that remains OPEN.
Input contract: ``web/app.py`` routes ``/verify/<token>`` and ``/reset/<token>``;
``web/templates/reset.html``; ``web/templates/verify_result.html``;
``web/observability.py`` operational logger.
Output contract: the two token routes carry the hardened headers on every
rendered path (success, failure, validation error); the global security-header
baseline is unchanged for non-token routes; no raw token appears in rendered
HTML or in application logs.
Prohibited: weakening the global baseline to pass; changing token hashing, TTL,
single-use semantics, session revocation, or the URL-token architecture.
Scope note: PROVIDER/REVERSE-PROXY ACCESS-LOG BEHAVIOUR IS OUT OF SCOPE HERE and
remains OPEN — it is not provable from this repository.
"""
import importlib
import logging
import os
import re

import pytest

RAW_TOKEN = "e" * 43 + "Z"          # token-shaped; never a real issued token


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_SECRET_KEY", "email-h1-test-secret")
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "eh1.sqlite"))
    monkeypatch.delenv("INVENTORAI_ENV", raising=False)
    webapp = importlib.import_module("web.app")
    webapp.app.config["TESTING"] = True
    return webapp.app.test_client()


def _token_pages(client):
    """Every token-bearing response path this gate governs."""
    return {
        "verify": client.get("/verify/%s" % RAW_TOKEN),
        "reset_get": client.get("/reset/%s" % RAW_TOKEN),
        "reset_post_invalid_password": client.post(
            "/reset/%s" % RAW_TOKEN,
            data={"password": "short", "password_confirm": "short"}),
        "reset_post_mismatch": client.post(
            "/reset/%s" % RAW_TOKEN,
            data={"password": "AAAaaa111!!!xyz", "password_confirm": "different111!!"}),
        "reset_post_bad_token": client.post(
            "/reset/%s" % RAW_TOKEN,
            data={"password": "AAAaaa111!!!xyz", "password_confirm": "AAAaaa111!!!xyz"}),
    }


# --- Referrer-Policy on token-bearing responses -------------------------------

def test_verify_page_sends_no_referrer(client):
    response = client.get("/verify/%s" % RAW_TOKEN)
    assert response.headers.get("Referrer-Policy") == "no-referrer"


def test_reset_page_sends_no_referrer(client):
    response = client.get("/reset/%s" % RAW_TOKEN)
    assert response.headers.get("Referrer-Policy") == "no-referrer"


def test_every_token_bearing_path_sends_no_referrer(client):
    for name, response in _token_pages(client).items():
        assert response.headers.get("Referrer-Policy") == "no-referrer", name


# --- Cache-Control on token-bearing responses ---------------------------------

def test_verify_page_is_not_stored(client):
    response = client.get("/verify/%s" % RAW_TOKEN)
    assert "no-store" in (response.headers.get("Cache-Control") or "")


def test_every_token_bearing_path_is_not_stored(client):
    for name, response in _token_pages(client).items():
        assert "no-store" in (response.headers.get("Cache-Control") or ""), name


# --- raw-token reflection in rendered HTML ------------------------------------

def test_reset_page_does_not_reflect_the_raw_token(client):
    """The reset form must post to the current URL rather than echoing the raw
    token into the HTML body (the URL-token architecture is unchanged)."""
    body = client.get("/reset/%s" % RAW_TOKEN).get_data(as_text=True)
    assert RAW_TOKEN not in body


def test_reset_error_pages_do_not_reflect_the_raw_token(client):
    for name, response in _token_pages(client).items():
        if not name.startswith("reset"):
            continue
        assert RAW_TOKEN not in response.get_data(as_text=True), name


def test_verify_result_does_not_reflect_the_raw_token(client):
    """RED exposure FIXED by EMAIL-H1 — not preserved pre-existing behaviour.

    `verify_result.html` itself never rendered the token, but the shared shell
    built its language-switch links with ``next=request.path``, which reflected
    the RAW token into an anchor href on this page. This test FAILS at the base
    commit and passes only with the ``lang_switch_next`` fix."""
    body = client.get("/verify/%s" % RAW_TOKEN).get_data(as_text=True)
    assert RAW_TOKEN not in body


# --- no third-party resources on token-bearing pages --------------------------

def test_token_pages_load_no_third_party_resources(client):
    """Preserved behaviour guard: no absolute external src/href on these pages."""
    pattern = re.compile(r'(?:src|href)\s*=\s*["\'](?:https?:)?//', re.I)
    for name, response in _token_pages(client).items():
        assert not pattern.search(response.get_data(as_text=True)), name


# --- global baseline must NOT be weakened -------------------------------------

def test_global_security_headers_still_present_on_token_pages(client):
    for name, response in _token_pages(client).items():
        assert "Content-Security-Policy" in response.headers, name
        assert response.headers.get("X-Content-Type-Options") == "nosniff", name
        assert response.headers.get("X-Frame-Options") == "DENY", name


def test_non_token_routes_keep_the_global_referrer_policy(client):
    """The global default must remain unchanged: only token-bearing responses
    are tightened to no-referrer."""
    for path in ("/", "/login", "/recover", "/data-and-session"):
        response = client.get(path)
        assert response.headers.get("Referrer-Policy") == \
            "strict-origin-when-cross-origin", path


def test_ordinary_route_language_switch_still_returns_to_that_route(client):
    """NB-1: the token-path fix must NOT collapse every route's language-switch
    target to `/`. An ordinary page must still offer a return link to ITSELF."""
    body = client.get("/login").get_data(as_text=True)
    assert "next=%2Flogin" in body or "next=/login" in body


def test_token_routes_language_switch_does_not_carry_the_token_path(client):
    """The complement of the guard above: on token-bearing pages the switch
    target must be the safe landing path, never the token path."""
    for path in ("/verify/%s" % RAW_TOKEN, "/reset/%s" % RAW_TOKEN):
        body = client.get(path).get_data(as_text=True)
        assert RAW_TOKEN not in body, path
        assert 'next=/"' in body, path


def test_non_token_routes_are_not_forced_to_no_store(client):
    """No accidental global cache-policy change."""
    response = client.get("/")
    assert "no-store" not in (response.headers.get("Cache-Control") or "")


def test_no_hsts_introduced(client):
    for name, response in _token_pages(client).items():
        assert "Strict-Transport-Security" not in response.headers, name


# --- application must not log the raw token -----------------------------------

def test_application_does_not_log_the_raw_token(client, caplog):
    with caplog.at_level(logging.DEBUG):
        client.get("/verify/%s" % RAW_TOKEN)
        client.get("/reset/%s" % RAW_TOKEN)
        client.post("/reset/%s" % RAW_TOKEN,
                    data={"password": "AAAaaa111!!!xyz",
                          "password_confirm": "AAAaaa111!!!xyz"})
    assert RAW_TOKEN not in caplog.text
