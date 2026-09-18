"""P5-1 — Account & Credential Foundation: narrow EmailSender boundary.

A minimal provider boundary so a future production adapter (P5-2+/ops) can drop
in without touching call sites. P5-1 ships ONLY a development sink. The interface
is deliberately tiny (verification / recovery / email-change transactional
messages) — it is NOT output/marketing/notification delivery, has no queue, no
retry worker, and no bulk sending, and it adds NO runtime dependency.

The raw verification token appears ONLY inside a captured/sink message body — it
is never written to the application logs.

SUPERSEDED IN PART (not rewritten): "P5-1 ships ONLY a development sink" is the
truth of P5-1 at its own gate. Under OD-INFRA-6 this module now ALSO carries the
production adapter (`ResendEmailSender`, bottom of this file). The boundary,
call sites and the no-runtime-dependency property are unchanged — the adapter is
exactly the drop-in the first paragraph anticipated.
"""


class EmailNotConfigured(Exception):
    """Raised when an email is requested and no sender can actually deliver it.

    This exists so a caller FAILS CLOSED AT POINT OF USE rather than reporting a
    delivery that cannot happen. It carries no address, token or message body.
    """


class EmailSender:
    """Abstract boundary. Subclasses implement ``send``.

    ``can_deliver`` states whether this sender is capable of delivering at all.
    It is a capability declaration, not a promise that any individual send will
    succeed: a configured provider can still fail per-message. A future
    production adapter inherits ``True`` and needs no change here.
    """

    can_deliver = True

    def send(self, to, subject, body):  # pragma: no cover - interface
        raise NotImplementedError


class DevMemoryEmailSender(EmailSender):
    """Development / test sink: captures messages in memory (never sends over a
    network, never writes to the application logs). Tests read ``.sent``; manual
    dev may inspect it. A production adapter is a SEPARATE, later concern."""

    def __init__(self):
        self.sent = []

    def send(self, to, subject, body):
        self.sent.append({"to": to, "subject": subject, "body": body})
        return True

    def last_for(self, to):
        for msg in reversed(self.sent):
            if msg["to"] == to:
                return msg
        return None

    def clear(self):
        self.sent.clear()


class UnconfiguredEmailSender(EmailSender):
    """The PRODUCTION sender used until a transactional-email provider is
    selected and configured.

    It exists so production can never silently fall back to
    ``DevMemoryEmailSender``: an in-memory sink in production would accept every
    message, report success, and deliver nothing — the application would tell a
    user that verification instructions had been sent when nothing could send
    them. This sender refuses instead, so the caller fails closed and can answer
    truthfully.

    It captures nothing: no address, subject or body is stored or logged here,
    so a refused send leaks no recipient and no token anywhere.
    """

    can_deliver = False

    def send(self, to, subject, body):
        raise EmailNotConfigured(
            "no production email provider is configured")


# ---------------------------------------------------------------------------
# OD-INFRA-6 — production transactional email (Resend, HTTPS API, stdlib only).
#
# This is the "future production adapter" the module docstring above anticipated.
# It drops in behind the SAME `EmailSender` boundary and changes no call site:
# `DevMemoryEmailSender` still serves development and test, and
# `UnconfiguredEmailSender` still serves production whenever the provider
# configuration is absent or invalid. No SDK is introduced — the transport is
# `urllib.request` from the standard library, so `requirements.txt` is unchanged
# and the existing dependency-family guard (which forbids a `resend` package)
# keeps holding.
# ---------------------------------------------------------------------------

import json as _json
import urllib.error as _urllib_error
import urllib.request as _urllib_request

# The provider endpoint is a CONSTANT, not configuration: an operator cannot
# redirect transactional mail (with its raw tokens) to another host by setting an
# environment variable. `send` additionally refuses any non-HTTPS endpoint.
RESEND_ENDPOINT = "https://api.resend.com/emails"

# One bounded request timeout. A hung provider must never hold a request thread
# open indefinitely — this process runs ONE worker and ONE thread.
DEFAULT_TIMEOUT_SECONDS = 10.0

# The provider response is read up to a bound; a pathological body can neither
# exhaust memory nor be echoed anywhere.
_MAX_RESPONSE_BYTES = 64 * 1024


class EmailDeliveryFailed(Exception):
    """A CONFIGURED provider was asked to deliver ONE message and did not.

    Deliberately distinct from ``EmailNotConfigured`` (no provider exists at
    all): that one means the capability is absent, this one means the capability
    exists and this single delivery did not happen.

    It carries ONLY a short stable reason code. No recipient address, raw token,
    message body, API key, authorization header, endpoint or provider response
    text is stored on it, so neither a log line nor a traceback can leak one
    through this class.
    """

    def __init__(self, reason_code="delivery_failed"):
        super().__init__(reason_code)
        self.reason_code = reason_code


def _https_json_post(url, headers, payload, timeout_seconds):
    """POST one JSON document over HTTPS and return ``(status, parsed-or-None)``.

    The seam the adapter calls. Tests substitute a deterministic local callable
    for it, so no test ever performs a network request. A provider 4xx/5xx is a
    real answer and is returned with its status; a transport failure raises.
    """
    if not url.startswith("https://"):
        raise ValueError("refusing a non-HTTPS request")
    request = _urllib_request.Request(
        url, data=_json.dumps(payload).encode("utf-8"), headers=headers,
        method="POST")
    try:
        with _urllib_request.urlopen(request, timeout=timeout_seconds) as response:
            status, raw = response.getcode(), response.read(_MAX_RESPONSE_BYTES)
    except _urllib_error.HTTPError as error:
        # A rejection IS a provider answer: keep its status so the caller can
        # distinguish "rejected" from "unreachable".
        status, raw = error.code, error.read(_MAX_RESPONSE_BYTES) or b""
    try:
        document = _json.loads(raw.decode("utf-8"))
    except Exception:
        document = None
    return status, document


class ResendEmailSender(EmailSender):
    """The production sender: one transactional message per call, over HTTPS.

    Success is CONFIRMED PROVIDER ACCEPTANCE and nothing weaker — a 2xx status
    AND a JSON object carrying the provider's message id. Anything else (non-2xx,
    unparseable or id-less body, timeout, DNS/TLS/socket failure) raises
    ``EmailDeliveryFailed`` so the caller cannot report a delivery that did not
    happen.

    Deliberately absent: retries, queues, workers, bulk sending, templates,
    attachments, and any logging whatsoever. One message, one attempt, one
    bounded answer.
    """

    can_deliver = True

    def __init__(self, api_key, sender, endpoint=RESEND_ENDPOINT,
                 timeout_seconds=DEFAULT_TIMEOUT_SECONDS, transport=None):
        if not isinstance(api_key, str) or not api_key.strip():
            raise ValueError("a non-empty provider key is required")
        if not isinstance(sender, str) or not sender.strip():
            raise ValueError("a non-empty sender identity is required")
        if not isinstance(endpoint, str) or not endpoint.startswith("https://"):
            raise ValueError("the provider endpoint must be an https:// URL")
        try:
            timeout = float(timeout_seconds)
        except (TypeError, ValueError):
            raise ValueError("the timeout must be a number") from None
        if not 0 < timeout <= 60:
            raise ValueError("the timeout must be bounded and positive")
        self._api_key = api_key.strip()
        self._sender = sender.strip()
        self._endpoint = endpoint
        self._timeout_seconds = timeout
        self._transport = transport or _https_json_post

    @property
    def endpoint(self):
        """The endpoint in use (for configuration assertions). Not the key."""
        return self._endpoint

    @property
    def timeout_seconds(self):
        return self._timeout_seconds

    @property
    def sender(self):
        """The configured sender identity — the FROM address, never a secret."""
        return self._sender

    def __repr__(self):
        """A representation that cannot carry the key into a log or traceback."""
        return "<ResendEmailSender endpoint=%s>" % self._endpoint

    def send(self, to, subject, body):
        payload = {"from": self._sender, "to": [to], "subject": subject,
                   "text": body}
        headers = {"Authorization": "Bearer " + self._api_key,
                   "Content-Type": "application/json"}
        try:
            status, document = self._transport(
                self._endpoint, headers, payload, self._timeout_seconds)
        except Exception:
            # `from None` severs the cause chain deliberately: a propagating
            # urllib error would otherwise carry the endpoint (and, in some
            # failure shapes, request detail) into any traceback that is logged.
            raise EmailDeliveryFailed("provider_unreachable") from None
        try:
            code = int(status)
        except (TypeError, ValueError):
            raise EmailDeliveryFailed("provider_response_invalid") from None
        if not 200 <= code < 300:
            raise EmailDeliveryFailed("provider_rejected")
        if not isinstance(document, dict):
            raise EmailDeliveryFailed("provider_response_invalid")
        if not str(document.get("id") or "").strip():
            raise EmailDeliveryFailed("provider_response_invalid")
        return True
