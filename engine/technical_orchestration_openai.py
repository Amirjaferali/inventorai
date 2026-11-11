"""Autonomous Technical Orchestration — OpenAI evaluation adapter (synthetic only).

File path      : engine/technical_orchestration_openai.py
Purpose        : ONE bounded provider adapter for the synthetic shadow
                 evaluation: provider-neutral ``OrchestrationRequest`` → one
                 stateless OpenAI Responses API request → provider response →
                 provider-neutral ``OrchestrationResponse``. Nothing else.
Authority      : Owner decision D3 — OpenAI API / ``gpt-6-sol`` APPROVED FOR
                 SYNTHETIC EVALUATION ONLY. Not a production-provider decision
                 and not a permanent vendor selection.

OPERATIONALLY OFF
-----------------
No product path imports this module (machine-checked). The only caller is the
developer-run evaluation harness, and even there the adapter refuses to open a
connection unless it was constructed with ``allow_network=True`` and its
credential mode is satisfied. Hosted CI never reaches the network: tests inject a
fake transport.

REQUEST MODE (D2)
-----------------
A single stateless request: ``store`` is false; no tools, web / file search,
computer use, background mode, previous response, conversation, files, vector
store or provider memory; no reasoning summary is requested and none is kept.
Only the request's own plain-data view and the provider-neutral instructions
are sent — no project, account, record, requirement or question identity.

SECRET
------
Two credential modes, chosen explicitly and never falling back to each other:
``env`` (the default) takes the credential only from the caller or the
``OPENAI_API_KEY`` environment variable and sends it only in the
``Authorization`` header; ``managed_proxy`` reads no key, accepts no key and
sends no ``Authorization`` header at all — the managed environment's egress
proxy injects the credential outside this process, so the secret is never in
it. Either way the credential is never placed in a URL, a result, an error, a
repr or any output. This module does no logging.

ROUTE (managed mode)
--------------------
A request without an ``Authorization`` header (``managed_proxy`` mode) relies
on the managed environment's relay to inject the credential, so it may leave
ONLY through that relay. Before any socket is opened the default transport
validates the route named by ``HTTPS_PROXY`` / ``https_proxy``: a plain
``http://`` URL of a loopback host (``127.0.0.0/8``, ``::1`` or ``localhost``)
with an explicit port and no credentials, path, query or fragment, and no
``NO_PROXY`` / ``no_proxy`` entry that would send the approved host direct. The
opener is then pinned to that validated route and never reads the environment
or ``NO_PROXY`` again. A missing, conflicting, malformed, unsupported or
bypassed route raises ``ManagedRouteUnavailable`` and nothing is sent. This is
a routing guard only: it does not observe, test or prove credential injection.
``env`` mode (an ``Authorization`` header) is routed exactly as before.

FAILURE
-------
The default transport makes exactly one request to the approved endpoint and
follows no redirect. Every timeout, transport failure, non-200 status
(including any 3xx), incomplete or malformed response becomes ``ERROR`` with no proposals; ``last_error_kind`` names the
category only. A provider object never escapes this module. A provider refusal
is an ``ABSTAIN``.

DIAGNOSTICS (evaluation only; they change no outcome, retry or error kind)
-----------
For a non-2xx response the default transport returns the status and, in place
of the response body, ONE InventorAI diagnostic document built by
``http_error_diagnostic``: a validated request id, the provider error type and
code mapped onto closed lists, and presence-only origin indicators. The raw
body, every header value other than a validated request id, and any message
text stay inside the transport and are discarded. ``transport_failure_diagnostic``
maps a transport exception onto a closed category and its class names without
ever reading the exception's text (a refused proxy tunnel contributes only its
three-digit status). A provider-shaped error response is supporting evidence
about which layer answered, never proof of it.
"""
import http.client
import ipaddress
import json
import os
import re
import socket
import ssl
import urllib.error
import urllib.parse
import urllib.request

from engine.technical_orchestration_shadow import (
    ABSTAIN, ERROR, PROPOSAL_INSTRUCTIONS, PROPOSED, OrchestrationAdapter,
    OrchestrationRequest, OrchestrationResponse, Proposal,
)

MODEL = "gpt-6-sol"
ENDPOINT = "https://api.openai.com/v1/responses"
CREDENTIAL_ENV = "OPENAI_API_KEY"
CREDENTIAL_MODE_ENV = "env"
CREDENTIAL_MODE_MANAGED_PROXY = "managed_proxy"
CREDENTIAL_MODES = (CREDENTIAL_MODE_ENV, CREDENTIAL_MODE_MANAGED_PROXY)
TIMEOUT_SECONDS = 90
MAX_OUTPUT_TOKENS = 4000

# Error categories (never a message, never provider text, never the key).
ERR_NETWORK_NOT_ALLOWED = "network_not_allowed"
ERR_MISSING_CREDENTIAL = "missing_credential"
ERR_CREDENTIAL_MODE = "credential_mode"
ERR_TRANSPORT = "transport"
ERR_HTTP_STATUS = "http_status"
ERR_INCOMPLETE = "incomplete"
ERR_MALFORMED = "malformed"

# ─── evaluation diagnostics: allowlisted fields only ─────────────────────────
DIAGNOSTIC_VERSION = 1
DIAGNOSTIC_UNAVAILABLE = "UNAVAILABLE"
DIAGNOSTIC_OTHER = "OTHER"
HTTP_DIAGNOSTIC_KEY = "inventorai_http_diagnostic"
MAX_ERROR_BODY_BYTES = 16384        # an error body beyond this is not parsed at all
# OpenAI request ids ("req_" plus an opaque token); anything else is not kept.
_REQUEST_ID = re.compile(r"req_[A-Za-z0-9]{8,64}\Z")
_CLASS_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]{0,63}\Z")
_TUNNEL_STATUS = re.compile(r"Tunnel connection failed: ([1-5][0-9][0-9])(?![0-9])")
# Closed lists of provider error types / codes. A value outside them is recorded
# only as OTHER, so no provider-chosen text is ever stored.
KNOWN_ERROR_TYPES = frozenset({
    "invalid_request_error", "authentication_error", "permission_error",
    "not_found_error", "rate_limit_error", "insufficient_quota", "server_error",
    "api_error", "tokens", "requests"})
KNOWN_ERROR_CODES = frozenset({
    "invalid_api_key", "invalid_organization", "invalid_project",
    "insufficient_quota", "rate_limit_exceeded", "model_not_found",
    "unsupported_country_region_territory", "account_deactivated",
    "invalid_authentication", "server_error"})
# Closed categories of a transport failure.
TF_TIMEOUT = "timeout"
TF_TUNNEL_REFUSED = "tunnel_refused"
TF_CONNECTION_REFUSED = "connection_refused"
TF_REMOTE_DISCONNECTED = "remote_disconnected"
TF_CONNECTION_RESET = "connection_reset"
TF_CONNECTION_ABORTED = "connection_aborted"
TF_INCOMPLETE_READ = "incomplete_read"
TF_TLS = "tls"
TF_DNS = "dns"
TF_PROTOCOL = "protocol"
TF_OTHER = "other"
TF_MANAGED_ROUTE_REFUSED = "managed_route_refused"   # refused locally; nothing was sent
TRANSPORT_FAILURE_CATEGORIES = (
    TF_TIMEOUT, TF_TUNNEL_REFUSED, TF_CONNECTION_REFUSED, TF_REMOTE_DISCONNECTED,
    TF_CONNECTION_RESET, TF_CONNECTION_ABORTED, TF_INCOMPLETE_READ, TF_TLS, TF_DNS,
    TF_PROTOCOL, TF_OTHER, TF_MANAGED_ROUTE_REFUSED)
# The managed relay route (see ROUTE above) and the closed reasons it is refused for.
MANAGED_ROUTE_ENV = ("HTTPS_PROXY", "https_proxy")
MANAGED_ROUTE_BYPASS_ENV = ("NO_PROXY", "no_proxy")
ROUTE_MISSING = "missing"
ROUTE_CONFLICTING = "conflicting"
ROUTE_MALFORMED = "malformed"
ROUTE_UNSUPPORTED = "unsupported"
ROUTE_BYPASSED = "bypassed"
MANAGED_ROUTE_REASONS = (ROUTE_MISSING, ROUTE_CONFLICTING, ROUTE_MALFORMED,
                         ROUTE_UNSUPPORTED, ROUTE_BYPASSED)
HTTP_DIAGNOSTIC_FIELDS = (
    "version", "status", "request_id", "request_id_header", "provider_error_object",
    "error_type", "error_code", "openai_headers", "server_cloudflare", "www_authenticate")


def _closed(value, known):
    """A provider value from a closed list, OTHER for any other string, else UNAVAILABLE."""
    if not isinstance(value, str):
        return DIAGNOSTIC_UNAVAILABLE
    return value if value in known else DIAGNOSTIC_OTHER


def _header_pairs(headers):
    """(lower-case name, value) pairs of a header mapping; nothing on any surprise."""
    try:
        return [(str(k).lower(), v) for k, v in headers.items()]
    except Exception:
        return []


def http_error_diagnostic(status, headers, body):
    """The allowlisted diagnostic of ONE non-2xx response: never the body, a
    message, a header value other than a validated request id, or a Location.

    ``provider_error_object`` says the body was a JSON object whose ``error``
    object carries a string ``type`` or ``message`` (OpenAI's documented shape);
    with ``openai_headers`` / ``server_cloudflare`` / ``request_id`` it is
    supporting evidence about which layer produced the response, not proof."""
    pairs = _header_pairs(headers)
    names = {name for name, _value in pairs}
    raw_id = next((v for name, v in pairs if name == "x-request-id"), None)
    server = next((v for name, v in pairs if name == "server"), None)
    diag = {"version": DIAGNOSTIC_VERSION,
            "status": status if isinstance(status, int) and not isinstance(status, bool)
            else DIAGNOSTIC_UNAVAILABLE,
            "request_id": raw_id if isinstance(raw_id, str) and _REQUEST_ID.match(raw_id)
            else DIAGNOSTIC_UNAVAILABLE,
            "request_id_header": "x-request-id" in names,
            "provider_error_object": False,
            "error_type": DIAGNOSTIC_UNAVAILABLE, "error_code": DIAGNOSTIC_UNAVAILABLE,
            "openai_headers": any(name.startswith("openai-") for name in names),
            "server_cloudflare": isinstance(server, str) and server.strip().lower() == "cloudflare",
            "www_authenticate": "www-authenticate" in names}
    if isinstance(body, (bytes, bytearray)) and len(body) <= MAX_ERROR_BODY_BYTES:
        try:
            data = json.loads(bytes(body).decode("utf-8"))
        except Exception:
            data = None
        error = data.get("error") if isinstance(data, dict) else None
        if isinstance(error, dict) and (isinstance(error.get("type"), str)
                                        or isinstance(error.get("message"), str)):
            diag["provider_error_object"] = True
            diag["error_type"] = _closed(error.get("type"), KNOWN_ERROR_TYPES)
            diag["error_code"] = _closed(error.get("code"), KNOWN_ERROR_CODES)
    return diag


def http_diagnostic_document(status, headers, body):
    """The bytes the default transport returns for a non-2xx response."""
    return json.dumps({HTTP_DIAGNOSTIC_KEY: http_error_diagnostic(status, headers, body)},
                      sort_keys=True).encode("utf-8")


def read_http_diagnostic(raw):
    """The diagnostic carried by ``raw`` when it is EXACTLY a document of
    ``http_diagnostic_document`` (every field present with its allowed shape),
    else None. Anything else a transport returned is never interpreted."""
    try:
        data = json.loads(raw.decode("utf-8"))
    except Exception:
        return None
    diag = data.get(HTTP_DIAGNOSTIC_KEY) if isinstance(data, dict) and len(data) == 1 else None
    if not isinstance(diag, dict) or tuple(sorted(diag)) != tuple(sorted(HTTP_DIAGNOSTIC_FIELDS)):
        return None
    flags = ("request_id_header", "provider_error_object", "openai_headers",
             "server_cloudflare", "www_authenticate")
    ok = (diag["version"] == DIAGNOSTIC_VERSION
          and (diag["status"] == DIAGNOSTIC_UNAVAILABLE
               or (isinstance(diag["status"], int) and not isinstance(diag["status"], bool)))
          and (diag["request_id"] == DIAGNOSTIC_UNAVAILABLE
               or (isinstance(diag["request_id"], str) and _REQUEST_ID.match(diag["request_id"])))
          and diag["error_type"] in KNOWN_ERROR_TYPES | {DIAGNOSTIC_OTHER, DIAGNOSTIC_UNAVAILABLE}
          and diag["error_code"] in KNOWN_ERROR_CODES | {DIAGNOSTIC_OTHER, DIAGNOSTIC_UNAVAILABLE}
          and all(diag[f] is True or diag[f] is False for f in flags))
    return dict(diag) if ok else None


def _class_name(exc):
    name = type(exc).__name__
    return name if _CLASS_NAME.match(name) else DIAGNOSTIC_OTHER


def transport_failure_diagnostic(exc):
    """The closed category and class names of ONE transport exception. The
    exception's text is never stored; a refused proxy tunnel contributes only
    the three-digit status of its fixed "Tunnel connection failed" form."""
    cause = exc
    for _ in range(3):                      # urllib wraps socket-level errors in URLError
        reason = getattr(cause, "reason", None)
        if isinstance(cause, urllib.error.URLError) and isinstance(reason, BaseException):
            cause = reason
        else:
            break
    tunnel = DIAGNOSTIC_UNAVAILABLE
    if isinstance(cause, ManagedRouteUnavailable):
        category = TF_MANAGED_ROUTE_REFUSED
    elif isinstance(cause, (socket.timeout, TimeoutError)):
        category = TF_TIMEOUT
    elif isinstance(cause, ssl.SSLError):
        category = TF_TLS
    elif isinstance(cause, socket.gaierror):
        category = TF_DNS
    elif isinstance(cause, http.client.RemoteDisconnected):
        category = TF_REMOTE_DISCONNECTED
    elif isinstance(cause, ConnectionRefusedError):
        category = TF_CONNECTION_REFUSED
    elif isinstance(cause, ConnectionResetError):
        category = TF_CONNECTION_RESET
    elif isinstance(cause, (ConnectionAbortedError, BrokenPipeError)):
        category = TF_CONNECTION_ABORTED
    elif isinstance(cause, http.client.IncompleteRead):
        category = TF_INCOMPLETE_READ
    elif isinstance(cause, http.client.HTTPException):
        category = TF_PROTOCOL
    else:
        category = TF_OTHER
        first = cause.args[0] if isinstance(cause, OSError) and cause.args else None
        found = _TUNNEL_STATUS.match(first) if isinstance(first, str) else None
        if found:
            category, tunnel = TF_TUNNEL_REFUSED, int(found.group(1))
    return {"version": DIAGNOSTIC_VERSION, "category": category,
            "exception_class": _class_name(exc),
            "cause_class": _class_name(cause) if cause is not exc else DIAGNOSTIC_UNAVAILABLE,
            "tunnel_status": tunnel}


def _schema(request):
    """The strict JSON schema for this one request: kinds, gap and handles are
    the request's own closed sets. The local adjudicator re-checks every one."""
    proposal = {
        "type": "object",
        "properties": {
            "kind": {"type": "string", "enum": list(request.allowed_proposal_kinds)},
            "text": {"type": "string"},
            "source_handles": {"type": "array",
                               "items": {"type": "string",
                                         "enum": sorted(request.handles())}},
            "gap_type": {"type": "string", "enum": [request.gap_type]},
        },
        "required": ["kind", "text", "source_handles", "gap_type"],
        "additionalProperties": False,
    }
    return {
        "type": "object",
        "properties": {
            "outcome": {"type": "string", "enum": [PROPOSED, ABSTAIN]},
            "proposals": {"type": "array", "items": proposal},
        },
        "required": ["outcome", "proposals"],
        "additionalProperties": False,
    }


def build_payload(request, model=MODEL):
    """The exact provider request body. Only these keys are ever sent."""
    if not isinstance(request, OrchestrationRequest):
        raise ValueError("build_payload needs an OrchestrationRequest")
    return {
        "model": model,
        "instructions": PROPOSAL_INSTRUCTIONS,
        "input": json.dumps(request.as_payload(), ensure_ascii=False,
                            sort_keys=True),
        "store": False,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "text": {"format": {"type": "json_schema",
                            "name": "orchestration_proposals",
                            "strict": True,
                            "schema": _schema(request)}},
    }


class _RefuseRedirects(urllib.request.HTTPRedirectHandler):
    """Refuses every redirect (301 / 302 / 303 / 307 / 308) before any
    follow-up request is built, so the credential, the body and the synthetic
    source text can never reach a ``Location`` target — same host or not,
    HTTPS or not. The redirect then surfaces as an ``HTTPError`` carrying its
    3xx status, which the adapter reports as ``ERROR``."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class ManagedRouteUnavailable(Exception):
    """The managed relay route could not be established; nothing was sent.
    ``reason`` is one of ``MANAGED_ROUTE_REASONS``; no environment value is
    ever stored in it."""

    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


def _loopback(host):
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def managed_proxy_route(environ=None):
    """The ONE validated relay route a managed-mode request may use, as a
    normalized ``http://host:port`` URL, or ``ManagedRouteUnavailable``. Reads
    only ``HTTPS_PROXY`` / ``https_proxy`` and ``NO_PROXY`` / ``no_proxy``;
    opens no socket. No address or port is assumed beyond the loopback rule."""
    env = os.environ if environ is None else environ
    values = {env.get(name).strip() for name in MANAGED_ROUTE_ENV
              if isinstance(env.get(name), str) and env.get(name).strip()}
    if not values:
        raise ManagedRouteUnavailable(ROUTE_MISSING)
    if len(values) > 1:
        raise ManagedRouteUnavailable(ROUTE_CONFLICTING)
    raw = values.pop()
    try:
        parts = urllib.parse.urlsplit(raw)
        host, port = parts.hostname, parts.port
    except ValueError:
        raise ManagedRouteUnavailable(ROUTE_MALFORMED) from None
    if parts.scheme != "http":
        raise ManagedRouteUnavailable(ROUTE_UNSUPPORTED)
    if (not host or port is None or parts.username is not None or parts.password is not None
            or parts.path not in ("", "/") or parts.query or parts.fragment):
        raise ManagedRouteUnavailable(ROUTE_MALFORMED)
    if not _loopback(host):
        raise ManagedRouteUnavailable(ROUTE_UNSUPPORTED)
    target = urllib.parse.urlsplit(ENDPOINT).hostname
    for name in MANAGED_ROUTE_BYPASS_ENV:
        value = env.get(name)
        if isinstance(value, str) and value.strip() and \
                urllib.request.proxy_bypass_environment(target, {"no": value}):
            raise ManagedRouteUnavailable(ROUTE_BYPASSED)
    return "http://%s:%d" % ("[%s]" % host if ":" in host else host, port)


class _PinnedRelayHandler(urllib.request.ProxyHandler):
    """Sends the https request through ONE already-validated relay route. It
    never reads the environment and never consults ``NO_PROXY``, so the route
    used is exactly the route that was validated."""

    def __init__(self, route):
        super().__init__({"https": route})
        self._hostport = urllib.parse.urlsplit(route).netloc

    def proxy_open(self, req, proxy, type):
        req.set_proxy(self._hostport, "http")
        return None


def _opener(route=None):
    """A private opener for one call. It is never installed globally, so
    urllib's module-level state is untouched. With a managed relay ``route``
    the opener is pinned to it in place of urllib's environment proxy lookup."""
    if route is None:
        return urllib.request.build_opener(_RefuseRedirects)
    return urllib.request.build_opener(_PinnedRelayHandler(route), _RefuseRedirects)


def _urllib_transport(url, headers, body, timeout):
    """The default transport: ONE HTTPS POST to the approved endpoint and no
    follow-up request of any kind. Returns (status, body bytes). A managed-mode
    request (no ``Authorization`` header) goes only through the validated relay
    route, or raises ``ManagedRouteUnavailable`` before any socket is opened."""
    if url != ENDPOINT:
        raise ValueError("the orchestration adapter posts to its approved endpoint only")
    managed = not any(str(name).lower() == "authorization" for name in headers)
    route = managed_proxy_route() if managed else None
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with _opener(route).open(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        # The raw error body never leaves the transport: only its allowlisted
        # diagnostic is returned (the adapters treat any non-200 as ERROR anyway).
        try:
            body = exc.read(MAX_ERROR_BODY_BYTES + 1)
        except Exception:
            body = b""
        finally:
            try:
                exc.close()
            except Exception:
                pass
        return exc.code, http_diagnostic_document(exc.code, exc.headers, body)


def _output_text(data):
    """The single assistant output text, or ABSTAIN for a refusal. Anything
    else is malformed."""
    if not isinstance(data, dict) or data.get("status") != "completed":
        raise LookupError(ERR_INCOMPLETE)
    texts, refused = [], False
    for item in data.get("output") or ():
        if not isinstance(item, dict) or item.get("type") != "message":
            continue                     # e.g. a reasoning item: never kept
        for part in item.get("content") or ():
            if not isinstance(part, dict):
                raise ValueError(ERR_MALFORMED)
            if part.get("type") == "output_text":
                texts.append(part.get("text"))
            elif part.get("type") == "refusal":
                refused = True
    if refused and not texts:
        return ABSTAIN
    if len(texts) != 1 or not isinstance(texts[0], str):
        raise ValueError(ERR_MALFORMED)
    return texts[0]


def parse_response(body):
    """Provider response bytes → provider-neutral ``OrchestrationResponse``.
    Raises on anything malformed; the adapter turns that into ERROR."""
    data = json.loads(body.decode("utf-8"))
    text = _output_text(data)
    if text == ABSTAIN:
        return OrchestrationResponse(ABSTAIN)
    reply = json.loads(text)
    if not isinstance(reply, dict) or set(reply) != {"outcome", "proposals"}:
        raise ValueError(ERR_MALFORMED)
    outcome, items = reply["outcome"], reply["proposals"]
    if outcome not in (PROPOSED, ABSTAIN) or not isinstance(items, list):
        raise ValueError(ERR_MALFORMED)
    proposals = []
    for item in items:
        if not isinstance(item, dict) or set(item) != {
                "kind", "text", "source_handles", "gap_type"}:
            raise ValueError(ERR_MALFORMED)
        handles = item["source_handles"]
        if not isinstance(handles, list):
            raise ValueError(ERR_MALFORMED)
        proposals.append(Proposal(item["kind"], item["text"], tuple(handles),
                                  item["gap_type"]))
    return OrchestrationResponse(outcome, tuple(proposals))


class OpenAIOrchestrationAdapter(OrchestrationAdapter):
    """The OpenAI evaluation adapter. Off unless ``allow_network=True``."""

    name = "openai:" + MODEL

    def __init__(self, *, allow_network=False, api_key=None, transport=None,
                 model=MODEL, timeout=TIMEOUT_SECONDS,
                 credential_mode=CREDENTIAL_MODE_ENV):
        self._allow_network = allow_network is True
        self._api_key = api_key
        self._credential_mode = credential_mode
        self._transport = transport or _urllib_transport
        self._model = model
        self._timeout = timeout
        self.name = "openai:" + model
        self.last_error_kind = None

    def __repr__(self):
        return ("OpenAIOrchestrationAdapter(model=%r, allow_network=%r, "
                "credential_mode=%r)" % (self._model, self._allow_network,
                                         self._credential_mode))

    def _fail(self, kind):
        self.last_error_kind = kind
        return OrchestrationResponse(ERROR)

    def propose(self, request):
        self.last_error_kind = None
        if not self._allow_network:
            return self._fail(ERR_NETWORK_NOT_ALLOWED)
        if self._credential_mode == CREDENTIAL_MODE_MANAGED_PROXY:
            if self._api_key is not None:
                return self._fail(ERR_CREDENTIAL_MODE)
            headers = {"Content-Type": "application/json"}
        elif self._credential_mode == CREDENTIAL_MODE_ENV:
            key = self._api_key or os.environ.get(CREDENTIAL_ENV)
            if not key:
                return self._fail(ERR_MISSING_CREDENTIAL)
            headers = {"Authorization": "Bearer " + key,
                       "Content-Type": "application/json"}
        else:
            return self._fail(ERR_CREDENTIAL_MODE)
        try:
            body = json.dumps(build_payload(request, self._model),
                              ensure_ascii=False).encode("utf-8")
        except Exception:
            return self._fail(ERR_MALFORMED)
        try:
            status, raw = self._transport(ENDPOINT, headers, body, self._timeout)
        except Exception:
            return self._fail(ERR_TRANSPORT)
        if status != 200:
            return self._fail(ERR_HTTP_STATUS)
        try:
            return parse_response(raw)
        except LookupError:
            return self._fail(ERR_INCOMPLETE)
        except Exception:
            return self._fail(ERR_MALFORMED)
