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

FAILURE
-------
The default transport makes exactly one request to the approved endpoint and
follows no redirect. Every timeout, transport failure, non-200 status
(including any 3xx), incomplete or malformed response becomes ``ERROR`` with no proposals; ``last_error_kind`` names the
category only. A provider object never escapes this module. A provider refusal
is an ``ABSTAIN``.
"""
import json
import os
import urllib.error
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


def _opener():
    """A private opener for one call. It is never installed globally, so
    urllib's module-level state is untouched."""
    return urllib.request.build_opener(_RefuseRedirects)


def _urllib_transport(url, headers, body, timeout):
    """The default transport: ONE HTTPS POST to the approved endpoint and no
    follow-up request of any kind. Returns (status, body bytes)."""
    if url != ENDPOINT:
        raise ValueError("the orchestration adapter posts to its approved endpoint only")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with _opener().open(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, b""


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
