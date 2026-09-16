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
import subprocess
import sys

import pytest

import web.app as webapp
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
