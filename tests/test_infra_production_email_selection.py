"""SERIOUS-RELEASE-PRE-RELEASE-TRANCHE-01, Slice D — production email selection.

File: tests/test_infra_production_email_selection.py
Purpose: pin the ONE new behaviour this tranche introduces around email — WHICH
sender each runtime gets, and what the reachable account flows do when no sender
can deliver. The account-flow semantics themselves remain owned by
`test_p5_1_account_credential_foundation.py`,
`test_p5_2_auth_sessions_verification_recovery.py`,
`test_p5_3_project_ownership_authorization.py` and `test_a1_saved_journey_browser.py`;
token/log exposure remains owned by the two `test_email_h1_*` modules. Nothing
here duplicates them.

Input contract: `engine/email_sender.py` (`EmailSender`, `DevMemoryEmailSender`,
`UnconfiguredEmailSender`, `EmailNotConfigured`); `web/app.py`
(`_resolve_email_sender`, `_EMAIL_SENDER`, `_email_delivery_available`,
`_email_unavailable_response`, and the three email-dependent routes).
Output contract: development/test keep the in-memory sink and its
`.sent` / `.last_for()` / `.clear()` seam; production never receives that sink;
production boots without provider configuration; and each email-dependent action
refuses truthfully, mutating nothing, when delivery is unavailable.
Prohibited: sending real outbound email; asserting on a provider that has not
been selected; weakening the existing non-enumeration property to pass.
"""
from tests.csrf_client import csrf_client
import logging
import os
import sqlite3
import subprocess
import sys

import pytest

import web.app as webapp
import web.ui_text as ui_text
from engine.email_sender import (
    DevMemoryEmailSender,
    EmailNotConfigured,
    EmailSender,
    UnconfiguredEmailSender,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL = "email-selection@example.com"
PASSWORD = "Str0ng-Passw0rd-Example"


@pytest.fixture
def client():
    webapp.app.config["TESTING"] = True
    with csrf_client(webapp.app) as c:
        yield c


def _register(client, email=EMAIL):
    return client.post("/register", data={"email": email,
                                          "password": PASSWORD,
                                          "password_confirm": PASSWORD})


# --- sender selection ---------------------------------------------------------

def test_development_selects_the_in_memory_sink(monkeypatch):
    monkeypatch.delenv("INVENTORAI_ENV", raising=False)
    assert isinstance(webapp._resolve_email_sender(), DevMemoryEmailSender)


def test_production_never_selects_the_development_sink(monkeypatch):
    """The defect this slice exists to prevent: an in-memory sink in production
    would accept every message, report success, and deliver nothing."""
    monkeypatch.setenv("INVENTORAI_ENV", "production")
    selected = webapp._resolve_email_sender()
    assert not isinstance(selected, DevMemoryEmailSender)
    assert isinstance(selected, UnconfiguredEmailSender)


def test_production_selection_is_case_and_whitespace_insensitive(monkeypatch):
    """`_is_production` normalizes the value; the sender must follow it exactly,
    so a `Production` value cannot quietly land on the development sink."""
    monkeypatch.setenv("INVENTORAI_ENV", "  Production  ")
    assert isinstance(webapp._resolve_email_sender(), UnconfiguredEmailSender)


def test_dev_test_seam_is_preserved(monkeypatch):
    """The repository-wide seam other modules depend on, asserted explicitly:
    `.sent`, `.last_for()` and `.clear()` on the active sender."""
    monkeypatch.delenv("INVENTORAI_ENV", raising=False)
    sender = webapp._resolve_email_sender()
    sender.send(to="seam@example.com", subject="s", body="b")
    assert sender.sent and sender.last_for("seam@example.com")["subject"] == "s"
    sender.clear()
    assert sender.sent == [] and sender.last_for("seam@example.com") is None


def test_active_sender_in_the_test_runtime_is_the_sink():
    """The suite itself runs on the sink, so every existing account-flow module
    keeps reading `webapp._EMAIL_SENDER.last_for(...)` unchanged."""
    assert isinstance(webapp._EMAIL_SENDER, DevMemoryEmailSender)
    assert webapp._email_delivery_available() is True


# --- capability declaration ---------------------------------------------------

def test_capability_flags_are_declared_on_the_boundary():
    assert EmailSender.can_deliver is True
    assert DevMemoryEmailSender.can_deliver is True
    assert UnconfiguredEmailSender.can_deliver is False


def test_unconfigured_sender_refuses_and_captures_nothing():
    sender = UnconfiguredEmailSender()
    with pytest.raises(EmailNotConfigured):
        sender.send(to=EMAIL, subject="Verify", body="raw-token-should-not-persist")
    assert not hasattr(sender, "sent")
    assert EMAIL not in repr(vars(sender))


# --- production boots without an email provider -------------------------------

def test_production_boots_without_email_configuration(tmp_path):
    """No startup deadlock: a real interpreter imports the application under
    production settings with no email provider configured, and `/health` answers.
    Run in a subprocess so this is a genuine cold boot, not a re-import."""
    env = dict(os.environ)
    env.update({"INVENTORAI_ENV": "production",
                "INVENTORAI_SECRET_KEY": "boot-probe-not-a-real-secret",
                "INVENTORAI_DB_PATH": str(tmp_path / "boot.sqlite"),
                "PYTHONWARNINGS": "ignore"})
    program = (
        "import json;"
        "from web.app import app, _EMAIL_SENDER;"
        "from engine.email_sender import UnconfiguredEmailSender, DevMemoryEmailSender;"
        "assert isinstance(_EMAIL_SENDER, UnconfiguredEmailSender);"
        "assert not isinstance(_EMAIL_SENDER, DevMemoryEmailSender);"
        "r = app.test_client().get('/health');"
        "print(json.dumps({'status': r.status_code}))"
    )
    result = subprocess.run([sys.executable, "-c", program], cwd=ROOT, env=env,
                            capture_output=True, text=True, timeout=180)
    assert result.returncode == 0, result.stderr[-2000:]
    assert '"status": 200' in result.stdout, result.stdout


# --- fail closed at point of use ---------------------------------------------

@pytest.mark.parametrize("path,data", [
    ("/register", {"email": EMAIL, "password": PASSWORD,
                   "password_confirm": PASSWORD}),
    ("/recover", {"email": EMAIL}),
])
def test_email_dependent_action_refuses_when_delivery_is_unavailable(
        client, monkeypatch, path, data):
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", UnconfiguredEmailSender())
    response = client.post(path, data=data)
    assert response.status_code == 503
    body = response.get_data(as_text=True)
    for claim in ("have been sent", "has been sent", "sent"):
        assert claim not in body.lower(), body


def test_refusal_is_identical_for_every_address_so_it_enumerates_nothing(
        client, monkeypatch):
    """The refusal must not become an account-existence oracle."""
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", DevMemoryEmailSender())
    _register(client, "known@example.com")
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", UnconfiguredEmailSender())
    known = client.post("/recover", data={"email": "known@example.com"})
    unknown = client.post("/recover", data={"email": "never-seen@example.com"})
    assert known.status_code == unknown.status_code == 503
    assert known.get_data() == unknown.get_data()


def test_refusal_mutates_nothing(client, monkeypatch):
    """Refused before any rate-limit write, account row or token: a later
    registration of the same address must still behave as a first registration."""
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", UnconfiguredEmailSender())
    assert _register(client).status_code == 503
    store = webapp._get_account_store()
    assert store.get_account_by_normalized_email(EMAIL) is None

    sink = DevMemoryEmailSender()
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", sink)
    assert _register(client).status_code == 200
    assert store.get_account_by_normalized_email(EMAIL) is not None
    assert sink.last_for(EMAIL) is not None


def test_user_visible_success_appears_only_after_sender_acceptance(client,
                                                                   monkeypatch):
    sink = DevMemoryEmailSender()
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", sink)
    accepted = _register(client)
    assert accepted.status_code == 200
    assert sink.last_for(EMAIL) is not None

    monkeypatch.setattr(webapp, "_EMAIL_SENDER", UnconfiguredEmailSender())
    refused = client.post("/recover", data={"email": EMAIL})
    assert refused.status_code == 503
    assert refused.get_data() != accepted.get_data()


def test_authenticated_resend_refuses_when_delivery_is_unavailable(client,
                                                                   monkeypatch):
    sink = DevMemoryEmailSender()
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", sink)
    assert _register(client).status_code == 200
    assert client.post("/login", data={"email": EMAIL,
                                       "password": PASSWORD}).status_code in (200, 302)
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", UnconfiguredEmailSender())
    response = client.post("/account/resend-verification", data={})
    assert response.status_code in (302, 503)
    if response.status_code == 503:
        assert "sent" not in response.get_data(as_text=True).lower()


# --- bounded failure of a CONFIGURED sender ----------------------------------

class _RaisingSender(EmailSender):
    """A configured provider that fails on this particular message."""

    def send(self, to, subject, body):
        raise RuntimeError("provider rejected the message")


def test_a_configured_sender_that_fails_is_bounded(client, monkeypatch):
    """Distinct from "no sender configured": delivery is available, so the
    request proceeds and a per-message failure must not surface a 500 or an
    internal detail."""
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", _RaisingSender())
    assert webapp._email_delivery_available() is True
    response = _register(client)
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Traceback" not in body and "provider rejected" not in body


# --- token secrecy ------------------------------------------------------------

def test_no_raw_token_reaches_the_logs_on_either_failure_path(client, monkeypatch,
                                                              caplog):
    """Neither a refusal nor a per-message failure may put a token, a recipient
    address or an internal message into the log stream."""
    with caplog.at_level(logging.DEBUG):
        monkeypatch.setattr(webapp, "_EMAIL_SENDER", UnconfiguredEmailSender())
        client.post("/register", data={"email": EMAIL, "password": PASSWORD,
                                       "password_confirm": PASSWORD})
        client.post("/recover", data={"email": EMAIL})
        monkeypatch.setattr(webapp, "_EMAIL_SENDER", _RaisingSender())
        _register(client)
    text = caplog.text
    assert EMAIL not in text
    assert "provider rejected the message" not in text
    assert "no production email provider is configured" not in text


def test_refusal_response_carries_no_token_recipient_or_internal_detail(
        client, monkeypatch):
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", UnconfiguredEmailSender())
    body = client.post("/recover", data={"email": EMAIL}).get_data(as_text=True)
    assert EMAIL not in body
    assert "provider" not in body.lower()
    assert "configur" not in body.lower()
    assert "Traceback" not in body


# =============================================================================
# OD-INFRA-6 — the production Resend adapter, the public base URL, and the
# failure semantics this tranche was authorized to fix.
#
# Nothing below performs a network request: the adapter takes a `transport`
# seam and every test supplies a local deterministic callable. No provider
# account, key or domain exists, and none is needed to run this file.
# =============================================================================
import json as _json

from engine.email_sender import (
    DEFAULT_TIMEOUT_SECONDS,
    EmailDeliveryFailed,
    RESEND_ENDPOINT,
    ResendEmailSender,
)

PROVIDER_KEY = "test-only-not-a-real-provider-key"
SENDER = "InventorAI <no-reply@example.test>"
BASE_URL = "https://app.example.test"


_ACCEPTED = {"id": "prov-msg-1"}
_UNSET = object()


class _RecordingTransport:
    """A local stand-in for the provider. Records the call, returns a scripted
    answer. Never opens a socket.

    `document` uses an explicit sentinel so that `document=None` means a real
    "the provider returned no JSON document" case rather than "use the default".
    """

    def __init__(self, status=200, document=_UNSET, raises=None):
        self.status = status
        self.document = _ACCEPTED if document is _UNSET else document
        self.raises = raises
        self.calls = []

    def __call__(self, url, headers, payload, timeout_seconds):
        self.calls.append({"url": url, "headers": dict(headers),
                           "payload": payload, "timeout": timeout_seconds})
        if self.raises is not None:
            raise self.raises
        return self.status, self.document


def _sender(transport=None, **kwargs):
    options = {"api_key": PROVIDER_KEY, "sender": SENDER,
               "transport": transport or _RecordingTransport()}
    options.update(kwargs)
    return ResendEmailSender(**options)


def _production_env(tmp_path, **overrides):
    env = {"INVENTORAI_ENV": "production",
           "INVENTORAI_EMAIL_PROVIDER": "resend",
           "INVENTORAI_RESEND_API_KEY": PROVIDER_KEY,
           "INVENTORAI_EMAIL_FROM": SENDER,
           "INVENTORAI_PUBLIC_BASE_URL": BASE_URL}
    env.update(overrides)
    return env


def _apply(monkeypatch, env):
    for name in ("INVENTORAI_ENV", "INVENTORAI_EMAIL_PROVIDER",
                 "INVENTORAI_RESEND_API_KEY", "INVENTORAI_EMAIL_FROM",
                 "INVENTORAI_PUBLIC_BASE_URL"):
        monkeypatch.delenv(name, raising=False)
    for name, value in env.items():
        monkeypatch.setenv(name, value)


# --- selection: complete configuration only -----------------------------------

def test_production_selects_resend_only_when_configuration_is_complete(
        monkeypatch, tmp_path):
    _apply(monkeypatch, _production_env(tmp_path))
    assert isinstance(webapp._resolve_email_sender(), ResendEmailSender)


@pytest.mark.parametrize("missing", [
    "INVENTORAI_EMAIL_PROVIDER", "INVENTORAI_RESEND_API_KEY",
    "INVENTORAI_EMAIL_FROM", "INVENTORAI_PUBLIC_BASE_URL"])
def test_partial_configuration_fails_closed_to_the_unconfigured_sender(
        monkeypatch, tmp_path, missing):
    """A PARTIAL configuration is the dangerous case: it must never be treated
    as "nearly configured" and it must never reach the development sink."""
    env = _production_env(tmp_path)
    env.pop(missing)
    _apply(monkeypatch, env)
    selected = webapp._resolve_email_sender()
    assert isinstance(selected, UnconfiguredEmailSender)
    assert not isinstance(selected, DevMemoryEmailSender)


@pytest.mark.parametrize("value", ["   ", "", "\t"])
def test_blank_provider_key_fails_closed(monkeypatch, tmp_path, value):
    _apply(monkeypatch, _production_env(tmp_path,
                                        INVENTORAI_RESEND_API_KEY=value))
    assert isinstance(webapp._resolve_email_sender(), UnconfiguredEmailSender)


@pytest.mark.parametrize("value", [
    "http://app.example.test",        # not HTTPS
    "app.example.test",               # not absolute
    "https://",                       # no host
    "https://u:p@app.example.test",   # embedded credentials
    "https://app.example.test?x=1",   # query
    "https://app.example.test#f",     # fragment
    "javascript:alert(1)",            # not a URL at all
])
def test_malformed_public_base_url_fails_closed(monkeypatch, tmp_path, value):
    _apply(monkeypatch, _production_env(tmp_path,
                                        INVENTORAI_PUBLIC_BASE_URL=value))
    assert isinstance(webapp._resolve_email_sender(), UnconfiguredEmailSender)


def test_unknown_provider_name_is_not_silently_accepted(monkeypatch, tmp_path):
    _apply(monkeypatch, _production_env(
        tmp_path, INVENTORAI_EMAIL_PROVIDER="some-other-provider"))
    assert isinstance(webapp._resolve_email_sender(), UnconfiguredEmailSender)


def test_development_is_unaffected_by_provider_configuration(monkeypatch,
                                                             tmp_path):
    """The dev/test sink is chosen by RUNTIME, not by the presence of provider
    configuration: a stray production variable must not change dev behaviour."""
    env = _production_env(tmp_path)
    env.pop("INVENTORAI_ENV")
    _apply(monkeypatch, env)
    assert isinstance(webapp._resolve_email_sender(), DevMemoryEmailSender)


def test_selection_never_raises_on_any_configuration_shape(monkeypatch,
                                                           tmp_path):
    """No startup deadlock: selection is import-time, so it must not raise for
    ANY value, however malformed."""
    for value in ("", "   ", "://", "https://[", "not a url", "%"):
        _apply(monkeypatch, _production_env(
            tmp_path, INVENTORAI_PUBLIC_BASE_URL=value))
        assert webapp._resolve_email_sender() is not None


# --- public base URL validation (the configuration owner) ---------------------

@pytest.mark.parametrize("value,expected", [
    ("https://app.example.test", "https://app.example.test"),
    ("https://app.example.test/", "https://app.example.test"),
    ("https://app.example.test///", "https://app.example.test"),
    ("  https://app.example.test  ", "https://app.example.test"),
    ("https://app.example.test:8443", "https://app.example.test:8443"),
])
def test_public_base_url_normalizes_trailing_slash_safely(value, expected):
    assert webapp._normalize_public_base_url(value) == expected


@pytest.mark.parametrize("value", [
    "https://app.example.test/base", "https://app.example.test/base/",
    "https://app.example.test/verify", "https://app.example.test/a/b",
])
def test_public_base_url_rejects_a_path_prefix(value):
    """A path prefix is well-formed but unusable: the application is served at
    the root, so `https://host/app` would generate `https://host/app/verify/...`
    and every emailed link would 404. Fail closed instead of shipping that."""
    assert webapp._normalize_public_base_url(value) is None


@pytest.mark.parametrize("value", [
    None, "", "   ", "http://app.example.test", "//app.example.test",
    "https://", "ftp://app.example.test", "https://u:p@app.example.test",
    "https://app.example.test?x=1", "https://app.example.test#f",
    "https://app example.test", "https://app.example.test:notaport",
    "\x00", "https://app.example.test\x00", 7, b"https://app.example.test",
])
def test_public_base_url_rejects_anything_unusable(value):
    assert webapp._normalize_public_base_url(value) is None


def test_public_base_url_is_never_derived_from_request_headers(client,
                                                              monkeypatch):
    """The whole point of a CONFIGURED base URL: a caller-supplied Host or
    forwarded header must not be able to mint a link at an attacker origin."""
    monkeypatch.setattr(webapp, "_PUBLIC_BASE_URL", BASE_URL)
    sink = DevMemoryEmailSender()
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", sink)
    address = "host-spoof-probe@example.com"
    # Only the forwarded headers are spoofed here. Overriding `Host` as well is
    # already rejected with 403 by the pre-existing request-integrity guard, so
    # it cannot reach the link-building code through this client at all — a
    # stronger outcome than this test needs, and unchanged by this tranche.
    client.post("/register",
                data={"email": address, "password": PASSWORD,
                      "password_confirm": PASSWORD},
                headers={"X-Forwarded-Host": "attacker.example",
                         "X-Forwarded-Proto": "http",
                         "X-Forwarded-For": "203.0.113.1"})
    captured = sink.last_for(address)
    assert captured is not None, "registration did not reach the sender"
    body = captured["body"]
    assert body.startswith("Use this link")
    assert BASE_URL + "/verify/" in body
    assert "attacker.example" not in body


# Source-text forwarded-header/ProxyFix absence is NOT re-asserted here: it is
# already owned by `test_no_proxyfix_or_forwarded_header_trust_introduced` in
# tests/test_infra_render_production_serving.py. The behavioural spoofing test
# above is this module's contribution and is the stronger guarantee.


# --- absolute links -----------------------------------------------------------

def test_verification_link_is_absolute_https_when_configured(monkeypatch):
    monkeypatch.setattr(webapp, "_PUBLIC_BASE_URL", BASE_URL)
    body = webapp._verification_body("raw-token-value")
    assert BASE_URL + "/verify/raw-token-value" in body
    assert "https://" in body


def test_reset_link_is_absolute_https_when_configured(monkeypatch):
    monkeypatch.setattr(webapp, "_PUBLIC_BASE_URL", BASE_URL)
    body = webapp._reset_body("raw-token-value")
    assert BASE_URL + "/reset/raw-token-value" in body


def test_links_stay_relative_in_development(monkeypatch):
    """Development behaviour is unchanged: no base URL, no absolute link."""
    monkeypatch.setattr(webapp, "_PUBLIC_BASE_URL", None)
    assert webapp._verification_body("t").endswith("/verify/t")
    assert webapp._reset_body("t").endswith("/reset/t")


def test_registration_and_resend_use_the_same_verification_body(monkeypatch):
    """They previously diverged: registration mailed a bare "code" that no
    surface accepts, while resend mailed a link. One body now serves both."""
    monkeypatch.setattr(webapp, "_PUBLIC_BASE_URL", BASE_URL)
    source = open(os.path.join(ROOT, "web", "app.py"), encoding="utf-8").read()
    assert "Use this code to verify" not in source
    assert source.count("Use this link to verify your email") == 1


# --- the adapter --------------------------------------------------------------

def test_adapter_posts_to_the_constant_https_provider_endpoint():
    transport = _RecordingTransport()
    _sender(transport).send(to=EMAIL, subject="s", body="b")
    assert transport.calls[0]["url"] == RESEND_ENDPOINT
    assert RESEND_ENDPOINT.startswith("https://")


@pytest.mark.parametrize("endpoint", [
    "http://api.resend.com/emails", "ftp://x", "api.resend.com", ""])
def test_adapter_refuses_a_non_https_endpoint(endpoint):
    with pytest.raises(ValueError):
        _sender(endpoint=endpoint)


def test_adapter_timeout_is_bounded_and_passed_to_the_transport():
    transport = _RecordingTransport()
    sender = _sender(transport)
    sender.send(to=EMAIL, subject="s", body="b")
    assert 0 < sender.timeout_seconds <= 60
    assert sender.timeout_seconds == DEFAULT_TIMEOUT_SECONDS
    assert transport.calls[0]["timeout"] == sender.timeout_seconds


@pytest.mark.parametrize("timeout", [0, -1, 61, 1000, "soon", None])
def test_adapter_refuses_an_unbounded_or_invalid_timeout(timeout):
    with pytest.raises(ValueError):
        _sender(timeout_seconds=timeout)


@pytest.mark.parametrize("status", [200, 201, 202, 299])
def test_provider_2xx_with_a_message_id_is_accepted(status):
    transport = _RecordingTransport(status=status)
    assert _sender(transport).send(to=EMAIL, subject="s", body="b") is True


@pytest.mark.parametrize("status", [400, 401, 403, 404, 422, 429, 500, 502, 503])
def test_provider_4xx_and_5xx_are_rejected(status):
    transport = _RecordingTransport(status=status)
    with pytest.raises(EmailDeliveryFailed) as raised:
        _sender(transport).send(to=EMAIL, subject="s", body="b")
    assert raised.value.reason_code == "provider_rejected"


@pytest.mark.parametrize("document", [None, {}, {"id": ""}, {"id": "   "},
                                      [], "ok", 7, {"error": "nope"}])
def test_malformed_or_id_less_provider_response_is_not_success(document):
    """A 2xx with no message id is NOT confirmed acceptance."""
    transport = _RecordingTransport(status=200, document=document)
    with pytest.raises(EmailDeliveryFailed) as raised:
        _sender(transport).send(to=EMAIL, subject="s", body="b")
    assert raised.value.reason_code == "provider_response_invalid"


@pytest.mark.parametrize("error", [
    TimeoutError("timed out"), OSError("connection reset"),
    ValueError("bad"), Exception("unknown")])
def test_transport_failure_becomes_a_bounded_delivery_failure(error):
    transport = _RecordingTransport(raises=error)
    with pytest.raises(EmailDeliveryFailed) as raised:
        _sender(transport).send(to=EMAIL, subject="s", body="b")
    assert raised.value.reason_code == "provider_unreachable"
    assert raised.value.__cause__ is None      # cause chain severed on purpose


def test_delivery_failure_carries_no_recipient_token_body_or_key():
    transport = _RecordingTransport(status=500)
    try:
        _sender(transport).send(to=EMAIL, subject="Verify",
                                body="token-abc /verify/token-abc")
    except EmailDeliveryFailed as exc:
        text = "%r %s" % (exc, exc)
        assert EMAIL not in text
        assert "token-abc" not in text
        assert PROVIDER_KEY not in text
    else:                                       # pragma: no cover
        raise AssertionError("a 500 must not be treated as delivered")


def test_adapter_repr_and_attributes_never_expose_the_provider_key():
    """`repr()` is what lands in a traceback or a debug log line, so it is the
    surface that matters. The key is held privately and never rendered."""
    sender = _sender()
    exposed = "%r %s %s %s" % (sender, sender, sender.endpoint, sender.sender)
    assert PROVIDER_KEY not in exposed
    assert "Bearer" not in exposed
    assert "api_key" not in repr(sender)


def test_authorization_header_is_sent_but_never_logged(caplog):
    transport = _RecordingTransport()
    with caplog.at_level(logging.DEBUG):
        _sender(transport).send(to=EMAIL, subject="s", body="b")
    assert transport.calls[0]["headers"]["Authorization"].startswith("Bearer ")
    assert PROVIDER_KEY not in caplog.text
    assert "Authorization" not in caplog.text
    assert EMAIL not in caplog.text


def test_adapter_emits_no_log_records_at_all(caplog):
    """The quietest guarantee: the production adapter writes nothing anywhere,
    on success or on failure, so no future log configuration can expose it."""
    with caplog.at_level(logging.DEBUG):
        _sender(_RecordingTransport()).send(to=EMAIL, subject="s", body="b")
        try:
            _sender(_RecordingTransport(status=500)).send(
                to=EMAIL, subject="s", body="b")
        except EmailDeliveryFailed:
            pass
    assert [r for r in caplog.records
            if "email_sender" in r.name] == []


def test_adapter_request_body_is_one_json_message_with_no_bulk_fields():
    transport = _RecordingTransport()
    _sender(transport).send(to=EMAIL, subject="Verify", body="link")
    payload = transport.calls[0]["payload"]
    assert payload["to"] == [EMAIL]           # exactly one recipient
    assert payload["from"] == SENDER
    assert payload["subject"] == "Verify"
    assert payload["text"] == "link"
    for absent in ("bcc", "cc", "attachments", "tags", "template",
                   "batch", "schedule"):
        assert absent not in payload
    assert _json.dumps(payload)               # serializable as one document
    assert transport.calls[0]["headers"]["Content-Type"] == "application/json"


def test_adapter_makes_exactly_one_attempt_with_no_retry():
    transport = _RecordingTransport(status=503)
    with pytest.raises(EmailDeliveryFailed):
        _sender(transport).send(to=EMAIL, subject="s", body="b")
    assert len(transport.calls) == 1


def test_adapter_declares_itself_capable_of_delivery():
    assert ResendEmailSender.can_deliver is True
    assert webapp._email_delivery_available() in (True, False)


# --- FALSE-SENT semantics + NON-ENUMERATION (both, simultaneously) ------------

def _register_body(client, email):
    return client.post("/register",
                       data={"email": email, "password": PASSWORD,
                             "password_confirm": PASSWORD}).get_data()


def test_no_user_visible_claim_of_completed_delivery_anywhere(monkeypatch):
    """The defect this section exists for: the product must not state as fact
    that a message was sent, because a configured provider can fail and that
    failure is deliberately invisible to the caller."""
    for message in (webapp.REGISTER_GENERIC_MESSAGE_EN,
                    webapp.RECOVER_GENERIC_MESSAGE_EN):
        lowered = message.lower()
        assert "have been sent" not in lowered, message
        assert "has been sent" not in lowered, message
        assert "we have tried to send" in lowered, message


def test_localized_surfaces_carry_the_same_attempt_truthful_claim():
    """The rendered surface lives in ui_text, so fixing only web/app.py would
    have left the false claim on screen."""
    for key in ("UI_A_MSG_REGISTER", "UI_A_MSG_RECOVER"):
        english = ui_text.text(key, "en").lower()
        assert "have been sent" not in english, key
        assert "has been sent" not in english, key
        assert "tried to send" in english, key
        assert ui_text.text(key, "ar") != ui_text.text(key, "en")
        assert "حاولنا" in ui_text.text(key, "ar"), key


@pytest.mark.parametrize("path,data", [
    ("/register", {"email": "fresh@example.com", "password": PASSWORD,
                   "password_confirm": PASSWORD}),
    ("/recover", {"email": "fresh@example.com"}),
])
def test_provider_failure_produces_no_false_sent_claim(client, monkeypatch,
                                                       path, data):
    monkeypatch.setattr(webapp, "_EMAIL_SENDER",
                        _sender(_RecordingTransport(status=500)))
    response = client.post(path, data=data)
    assert response.status_code == 200
    body = response.get_data(as_text=True).lower()
    assert "have been sent" not in body
    assert "has been sent" not in body
    assert "tried to send" in body


def test_registration_response_is_identical_whether_delivery_succeeds_or_fails(
        client, monkeypatch):
    """A. no false delivery claim, achieved WITHOUT B. an oracle: the response
    must not differ by provider outcome either, or the difference would leak
    whether a message was actually attempted for that address."""
    monkeypatch.setattr(webapp, "_EMAIL_SENDER",
                        _sender(_RecordingTransport(status=200)))
    accepted = _register_body(client, "accepted@example.com")
    monkeypatch.setattr(webapp, "_EMAIL_SENDER",
                        _sender(_RecordingTransport(status=500)))
    rejected = _register_body(client, "rejected@example.com")
    assert accepted == rejected


def test_recovery_response_is_identical_across_existence_and_provider_outcome(
        client, monkeypatch):
    """The full cross-product: known/unknown address x accepted/rejected/outage.
    All four responses must be byte-identical."""
    sink = DevMemoryEmailSender()
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", sink)
    _register_body(client, "known-oracle@example.com")

    bodies = []
    for transport in (_RecordingTransport(status=200),
                      _RecordingTransport(status=500),
                      _RecordingTransport(raises=TimeoutError("t"))):
        monkeypatch.setattr(webapp, "_EMAIL_SENDER", _sender(transport))
        for address in ("known-oracle@example.com", "never-seen@example.com"):
            response = client.post("/recover", data={"email": address})
            bodies.append((response.status_code, response.get_data()))
    assert len(set(bodies)) == 1, "recovery response varies by outcome"


def test_registration_still_commits_the_account_when_the_provider_fails(
        client, monkeypatch):
    """Fail-closed must not become fail-destructive: a provider outage may not
    cost the user their registration, because they can request a new message."""
    monkeypatch.setattr(webapp, "_EMAIL_SENDER",
                        _sender(_RecordingTransport(status=500)))
    assert client.post("/register",
                       data={"email": "committed@example.com",
                             "password": PASSWORD,
                             "password_confirm": PASSWORD}).status_code == 200
    store = webapp._get_account_store()
    assert store.get_account_by_normalized_email("committed@example.com")


def test_no_delivery_capability_still_refuses_before_any_mutation(client,
                                                                  monkeypatch):
    """The UnconfiguredEmailSender path is untouched by this tranche."""
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", UnconfiguredEmailSender())
    assert client.post("/register",
                       data={"email": "never@example.com",
                             "password": PASSWORD,
                             "password_confirm": PASSWORD}).status_code == 503
    store = webapp._get_account_store()
    assert store.get_account_by_normalized_email("never@example.com") is None


# --- authenticated resend: truthful, bounded ----------------------------------

def _signed_in(client, monkeypatch, email):
    sink = DevMemoryEmailSender()
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", sink)
    assert client.post("/register", data={"email": email, "password": PASSWORD,
                                          "password_confirm": PASSWORD}
                       ).status_code == 200
    assert client.post("/login", data={"email": email, "password": PASSWORD}
                       ).status_code in (200, 302)
    return sink


def test_authenticated_resend_is_truthful_when_the_provider_fails(client,
                                                                  monkeypatch):
    """A signed-in caller already knows their own address, so a truthful
    outcome here is not an enumeration oracle — and silence would be a lie."""
    _signed_in(client, monkeypatch, "resend-fail@example.com")
    monkeypatch.setattr(webapp, "_EMAIL_SENDER",
                        _sender(_RecordingTransport(status=500)))
    response = client.post("/account/resend-verification", data={})
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert ui_text.text("UI_A_MSG_RESEND_FAILED", "en") in body
    assert ui_text.text("UI_A_MSG_RESEND", "en") not in body


def test_authenticated_resend_reports_success_only_on_acceptance(client,
                                                                 monkeypatch):
    _signed_in(client, monkeypatch, "resend-ok@example.com")
    monkeypatch.setattr(webapp, "_EMAIL_SENDER",
                        _sender(_RecordingTransport(status=200)))
    body = client.post("/account/resend-verification",
                       data={}).get_data(as_text=True)
    assert ui_text.text("UI_A_MSG_RESEND", "en") in body
    assert ui_text.text("UI_A_MSG_RESEND_FAILED", "en") not in body


def test_authenticated_resend_failure_names_no_provider_or_reason(client,
                                                                  monkeypatch):
    _signed_in(client, monkeypatch, "resend-quiet@example.com")
    monkeypatch.setattr(webapp, "_EMAIL_SENDER",
                        _sender(_RecordingTransport(status=403)))
    body = client.post("/account/resend-verification",
                       data={}).get_data(as_text=True)
    for forbidden in ("api.resend.com", "403", "Traceback",
                      "provider_rejected", "provider_unreachable",
                      "EmailDeliveryFailed", PROVIDER_KEY):
        assert forbidden.lower() not in body.lower(), forbidden


def test_authenticated_resend_does_not_claim_a_message_it_never_attempted(
        client, monkeypatch):
    """A rate-limited resend sent nothing. The old code still showed the success
    notice, which was the same false claim in a different place."""
    _signed_in(client, monkeypatch, "resend-throttle@example.com")
    monkeypatch.setattr(webapp, "_EMAIL_SENDER",
                        _sender(_RecordingTransport(status=200)))
    monkeypatch.setattr(webapp, "_rate_ok", lambda *a, **k: False)
    body = client.post("/account/resend-verification",
                       data={}).get_data(as_text=True)
    assert ui_text.text("UI_A_MSG_RESEND_FAILED", "en") in body
    assert ui_text.text("UI_A_MSG_RESEND", "en") not in body


# --- token secrecy across the new paths ---------------------------------------

def test_raw_token_never_reaches_a_log_on_any_provider_outcome(client,
                                                               monkeypatch,
                                                               caplog):
    monkeypatch.setattr(webapp, "_PUBLIC_BASE_URL", BASE_URL)
    with caplog.at_level(logging.DEBUG):
        for transport in (_RecordingTransport(status=200),
                          _RecordingTransport(status=500),
                          _RecordingTransport(raises=OSError("down"))):
            sender = _sender(transport)
            monkeypatch.setattr(webapp, "_EMAIL_SENDER", sender)
            client.post("/register",
                        data={"email": "log-probe@example.com",
                              "password": PASSWORD,
                              "password_confirm": PASSWORD})
            client.post("/recover", data={"email": "log-probe@example.com"})
            for call in transport.calls:
                token = call["payload"]["text"].rsplit("/", 1)[-1]
                assert token and token not in caplog.text
    assert "log-probe@example.com" not in caplog.text
    assert PROVIDER_KEY not in caplog.text


def test_tokens_remain_hash_only_at_rest(client, monkeypatch):
    """The raw token goes into the message body and nowhere else — the store
    keeps only its hash. Unchanged by this tranche, asserted because the body
    construction moved."""
    monkeypatch.setattr(webapp, "_PUBLIC_BASE_URL", BASE_URL)
    transport = _RecordingTransport(status=200)
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", _sender(transport))
    client.post("/register", data={"email": "hash-only@example.com",
                                   "password": PASSWORD,
                                   "password_confirm": PASSWORD})
    assert transport.calls, "no message was attempted"
    raw = transport.calls[0]["payload"]["text"].rsplit("/", 1)[-1]
    with sqlite3.connect(webapp._resolve_db_path()) as connection:
        rows = connection.execute("SELECT * FROM email_tokens").fetchall()
    assert rows, "no token row was written"
    flat = " ".join(str(value) for row in rows for value in row)
    assert raw not in flat
    assert "hash-only@example.com" not in flat


def test_the_email_module_has_no_logging_seam_at_all():
    """Source-level companion to the caplog tests: the production adapter cannot
    log, because the module imports no logging machinery. Nothing a future log
    configuration does can expose a key, a recipient or a token from here."""
    source = open(os.path.join(ROOT, "engine", "email_sender.py"),
                  encoding="utf-8").read()
    for forbidden in ("import logging", "logging.", "getLogger", "print(",
                      "warnings.warn"):
        assert forbidden not in source, forbidden


def test_the_default_transport_refuses_a_non_https_url_itself():
    """The adapter checks the endpoint at construction, so this guard inside the
    real transport would otherwise never be exercised. Belt and braces: the
    function that actually opens a socket refuses a plaintext URL on its own."""
    from engine.email_sender import _https_json_post
    with pytest.raises(ValueError):
        _https_json_post("http://api.resend.com/emails", {}, {"a": 1}, 1.0)
    with pytest.raises(ValueError):
        _https_json_post("api.resend.com", {}, {"a": 1}, 1.0)


# =============================================================================
# CORRECTIVE PASS (independent-review defect set B-1, N-1, N-2).
#
# The redirect tests below run a REAL local HTTP server and drive the REAL
# default transport, because the defect lived in urllib's default redirect
# behaviour and a fake transport cannot reproduce it. No external network is
# touched: the server is 127.0.0.1 on an ephemeral port.
# =============================================================================
import http.server
import socket
import threading

from engine.email_sender import (
    _NoRedirectHandler,
    _build_https_only_opener,
    _https_json_post,
)


class _RedirectingProvider:
    """A local origin that answers the first request with a redirect and records
    every request it sees, including the headers."""

    def __init__(self, status, location_builder, final_body=b'{"id": "attacker"}'):
        self.status = status
        self.location_builder = location_builder
        self.final_body = final_body
        self.requests = []
        probe = socket.socket()
        probe.bind(("127.0.0.1", 0))
        self.port = probe.getsockname()[1]
        probe.close()
        recorder = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def _record(self):
                recorder.requests.append(
                    {"method": self.command, "path": self.path,
                     "authorization": self.headers.get("Authorization")})

            def _answer(self):
                length = int(self.headers.get("Content-Length") or 0)
                if length:
                    self.rfile.read(length)
                self._record()
                if self.path == "/emails":
                    self.send_response(recorder.status)
                    self.send_header("Location",
                                     recorder.location_builder(recorder.port))
                    self.end_headers()
                    return
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(recorder.final_body)))
                self.end_headers()
                self.wfile.write(recorder.final_body)

            do_POST = _answer
            do_GET = _answer
            do_PUT = _answer

            def log_message(self, *args):
                pass

        self._server = http.server.HTTPServer(("127.0.0.1", self.port), Handler)

    def __enter__(self):
        threading.Thread(target=self._server.serve_forever, daemon=True).start()
        return self

    def __exit__(self, *exc):
        self._server.shutdown()
        self._server.server_close()
        return False

    @property
    def url(self):
        return "http://127.0.0.1:%d/emails" % self.port


def _post_through_the_real_redirect_policy(url):
    """Drive the REAL `_NoRedirectHandler` against a real local server.

    The production opener has no HTTP handler at all, so it cannot reach a local
    plaintext test server - that is a separate, stronger property, asserted on
    its own below. To exercise the REDIRECT POLICY against genuine 3xx responses
    from a real socket, this opener adds `HTTPHandler` (and disables proxies, so
    the loopback request is direct) while using the SAME production redirect
    handler. The handler under test is the shipped one, not a copy.
    """
    import urllib.request
    opener = urllib.request.OpenerDirector()
    for handler in (urllib.request.ProxyHandler({}),
                    urllib.request.HTTPHandler(),
                    urllib.request.HTTPSHandler(),
                    urllib.request.UnknownHandler(),
                    _NoRedirectHandler(),
                    urllib.request.HTTPDefaultErrorHandler(),
                    urllib.request.HTTPErrorProcessor()):
        opener.add_handler(handler)
    request = urllib.request.Request(
        url, data=b'{"a": 1}',
        headers={"Authorization": "Bearer " + PROVIDER_KEY,
                 "Content-Type": "application/json"},
        method="POST")
    return opener.open(request, timeout=10)


@pytest.mark.parametrize("status", [301, 302, 303, 307, 308])
def test_no_redirect_status_is_ever_followed(status):
    """B-1. Every redirect class is refused. Before the repair, urllib followed
    these AND copied the Authorization header to the new target, then accepted
    that target's body as proof of delivery."""
    import urllib.error
    with _RedirectingProvider(
            status, lambda port: "http://127.0.0.1:%d/stolen" % port) as provider:
        with pytest.raises(urllib.error.HTTPError) as raised:
            _post_through_the_real_redirect_policy(provider.url)
        assert raised.value.code == status
        assert len(provider.requests) == 1, provider.requests
        assert provider.requests[0]["path"] == "/emails"


def test_authorization_header_never_reaches_a_redirect_target():
    """B-1, stated as the leak it was: the bearer key must not be transmitted to
    any origin other than the one the request was addressed to."""
    import urllib.error
    with _RedirectingProvider(
            302, lambda port: "http://127.0.0.1:%d/stolen" % port) as provider:
        with pytest.raises(urllib.error.HTTPError):
            _post_through_the_real_redirect_policy(provider.url)
    forwarded = [r for r in provider.requests if r["path"] == "/stolen"]
    assert forwarded == [], "the provider key reached a redirect target"
    assert len(provider.requests) == 1
    assert provider.requests[0]["authorization"] == "Bearer " + PROVIDER_KEY


def test_https_to_http_downgrade_redirect_is_refused():
    """B-1. A redirect naming a plaintext origin is refused like any other."""
    import urllib.error
    with _RedirectingProvider(
            302, lambda port: "http://127.0.0.1:%d/downgrade" % port) as provider:
        with pytest.raises(urllib.error.HTTPError) as raised:
            _post_through_the_real_redirect_policy(provider.url)
        assert raised.value.code == 302
    assert [r["path"] for r in provider.requests] == ["/emails"]


def test_cross_host_redirect_is_refused():
    """B-1. A different host, even over HTTPS, is a different origin."""
    import urllib.error
    with _RedirectingProvider(
            307, lambda port: "https://evil.example/emails") as provider:
        with pytest.raises(urllib.error.HTTPError) as raised:
            _post_through_the_real_redirect_policy(provider.url)
        assert raised.value.code == 307
    assert len(provider.requests) == 1


def test_same_origin_redirect_is_also_refused():
    """B-1. No redirect is accepted AT ALL - same-origin included - so there is
    no case left where the response body comes from an unintended path."""
    import urllib.error
    with _RedirectingProvider(
            302, lambda port: "http://127.0.0.1:%d/emails-v2" % port) as provider:
        with pytest.raises(urllib.error.HTTPError) as raised:
            _post_through_the_real_redirect_policy(provider.url)
        assert raised.value.code == 302
    assert [r["path"] for r in provider.requests] == ["/emails"]


def test_a_refused_redirect_is_a_delivery_failure_at_the_adapter():
    """End to end at the adapter: a 3xx is never confirmed acceptance, and the
    redirect target's body can never become the message id."""
    for status in (301, 302, 303, 307, 308):
        transport = _RecordingTransport(status=status,
                                        document={"id": "attacker-controlled"})
        with pytest.raises(EmailDeliveryFailed) as raised:
            _sender(transport).send(to=EMAIL, subject="s", body="b")
        assert raised.value.reason_code == "provider_rejected", status


def test_the_opener_has_no_redirect_or_plaintext_handler():
    """Structural companion: exactly one redirect handler, ours; and no HTTP,
    file, ftp or data handler exists, so a downgrade cannot be opened at all
    rather than merely being string-checked."""
    opener = _build_https_only_opener()
    kinds = [type(handler).__name__ for handler in opener.handlers]
    assert kinds.count("_NoRedirectHandler") == 1
    assert sum("Redirect" in kind for kind in kinds) == 1
    for absent in ("HTTPHandler", "FileHandler", "FTPHandler", "DataHandler"):
        assert absent not in kinds, absent
    assert "HTTPSHandler" in kinds
    assert _NoRedirectHandler().redirect_request(
        None, None, 302, "Found", {}, "https://evil.example") is None


def test_the_production_opener_cannot_open_a_plaintext_url_at_all():
    """The stronger property the test opener above deliberately sets aside: the
    SHIPPED opener has no HTTP handler, so a downgrade is unopenable rather than
    merely string-checked, and it fails as a clean URLError."""
    import urllib.error
    with pytest.raises(urllib.error.URLError) as raised:
        _build_https_only_opener().open("http://127.0.0.1:1/x", timeout=5)
    assert "unknown url type" in str(raised.value.reason)
    for scheme in ("file:///etc/passwd", "ftp://127.0.0.1/x",
                   "data:text/plain,x"):
        with pytest.raises(urllib.error.URLError):
            _build_https_only_opener().open(scheme, timeout=5)


def test_the_real_transport_still_refuses_a_non_https_url_by_contract():
    with pytest.raises(ValueError):
        _https_json_post("http://api.resend.com/emails", {}, {"a": 1}, 1.0)


# --- N-2: the message id must be a genuine string ----------------------------

@pytest.mark.parametrize("identifier", [
    True, False, 123, 0, 1.5, [], ["x"], {}, {"a": 1}, None, "", "   ", b"x"])
def test_a_non_string_message_id_is_not_confirmed_acceptance(identifier):
    """N-2. `str(value or "")` previously coerced `true`, `123` and `[1]` into
    truthy text, so a value that is not a message identifier at all satisfied
    the success bar."""
    transport = _RecordingTransport(status=200, document={"id": identifier})
    with pytest.raises(EmailDeliveryFailed) as raised:
        _sender(transport).send(to=EMAIL, subject="s", body="b")
    assert raised.value.reason_code == "provider_response_invalid"


def test_a_genuine_string_message_id_is_accepted():
    transport = _RecordingTransport(status=200, document={"id": "  msg-1  "})
    assert _sender(transport).send(to=EMAIL, subject="s", body="b") is True


# --- N-1: public base URL authority confusion --------------------------------

@pytest.mark.parametrize("value", [
    "https://good.example\\\\@evil.example",      # backslash authority confusion
    "https://good.example\\\\evil.example",
    "https://good.example%2f@evil.example",     # encoded slash in the authority
    "https://good.example%2F.evil.example",
    "https://good.example%5c.evil.example",     # encoded backslash
    "https://good.example%5C@evil.example",
    "https://app.example.test%23fragment",      # smuggled fragment
    "https://app.example.test%40evil.example",  # smuggled userinfo
    "https://app.example.test%00",              # smuggled NUL
    "https://\\u0430pp.example.test",                # cyrillic homoglyph host
    "https://app_example.test",                 # underscore is not a DNS label
    "https://-app.example.test",                # leading hyphen
    "https://app.example.test.",                # trailing dot
    "https://localhost",                        # single label, no dot
    "https://[::1]",                            # bracketed literal
])
def test_public_base_url_rejects_authority_confusion(value):
    assert webapp._normalize_public_base_url(value) is None


@pytest.mark.parametrize("value", [
    "https://xn--e1afmkfd.xn--p1ai",            # punycode IS the stable form
    "https://a-b.example.test",
    "https://app.example.test:8443",
])
def test_public_base_url_accepts_a_stable_ascii_origin(value):
    """Deliberate accept decisions, recorded so a later reader does not mistake
    them for oversights. Punycode is the STABLE ASCII form of an
    internationalized domain - rejecting it would break a legitimate production
    domain, and it needs no normalization to become an origin."""
    assert webapp._normalize_public_base_url(value) == value
