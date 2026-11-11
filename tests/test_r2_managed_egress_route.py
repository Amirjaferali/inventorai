# -*- coding: utf-8 -*-
"""R2-MANAGED-EGRESS-FAIL-CLOSED-01 — a managed-mode request leaves only through the validated relay.

Offline: simulated environments and urllib's real handler chain stopped at a fake https handler or a
local socket. What is pinned:
  * the route is HTTPS_PROXY / https_proxy, a plain http:// loopback URL (127.0.0.0/8, ::1 or
    localhost) with an explicit port and nothing else; any address or port inside that rule passes;
  * a missing, conflicting, malformed, unsupported or NO_PROXY-bypassed route is refused BEFORE any
    socket or handler is reached, keeps the existing ERR_TRANSPORT kind, gets its own closed
    diagnostic category and is journaled by the MSNL harness as NOT sent;
  * the opener is pinned to the validated route: it never re-reads the environment or NO_PROXY;
  * env-key mode (an Authorization header), the endpoint lock, redirect refusal and no-retry are
    unchanged. Nothing here observes or proves credential injection.
"""
import json
import socket
import urllib.error
import urllib.request

import pytest

from engine import technical_orchestration_openai as toa
from tests.test_msnl_llm_eval_harness import h

ROUTE_NAMES = ("HTTPS_PROXY", "https_proxy", "NO_PROXY", "no_proxy", "HTTP_PROXY", "http_proxy",
               "ALL_PROXY", "all_proxy")
MANAGED_HEADERS = {"Content-Type": "application/json"}
SECRET = "sk-proj-SYNTHETICSECRET0123456789abcdef"


@pytest.fixture
def env(monkeypatch):
    for name in ROUTE_NAMES:
        monkeypatch.delenv(name, raising=False)

    def setenv(**values):
        for name, value in values.items():
            monkeypatch.setenv(name, value)
    return setenv


@pytest.fixture
def wire(monkeypatch):
    """Records what reaches urllib's https handler; refuses any real socket."""
    seen = []

    def https_open(handler, req):
        import http.client
        import io
        import urllib.response
        seen.append({"via": req.host, "tunnel": getattr(req, "_tunnel_host", None),
                     "url": req.full_url, "headers": dict(req.header_items())})
        msg = http.client.parse_headers(io.BytesIO(b"Content-Type: application/json\r\n\r\n"))
        resp = urllib.response.addinfourl(io.BytesIO(b"{}"), msg, req.full_url, 200)
        resp.msg = "synthetic"
        return resp

    def no_socket(*_a, **_k):
        raise AssertionError("a socket was opened")
    monkeypatch.setattr(urllib.request.HTTPSHandler, "https_open", https_open)
    monkeypatch.setattr(socket.socket, "connect", no_socket)
    monkeypatch.setattr(socket, "create_connection", no_socket)
    return seen


def _send(headers=MANAGED_HEADERS):
    return toa._urllib_transport(toa.ENDPOINT, headers, b"{}", 5)


# ─── the validated route ─────────────────────────────────────────────────────

@pytest.mark.parametrize("value, route", [
    ("http://127.0.0.1:43739", "http://127.0.0.1:43739"),
    ("http://127.0.0.1:8080/", "http://127.0.0.1:8080"),
    ("  http://127.9.8.7:1  ", "http://127.9.8.7:1"),
    ("http://[::1]:5000", "http://[::1]:5000"),
    ("http://localhost:3128", "http://localhost:3128"),
])
def test_any_loopback_relay_with_an_explicit_port_is_accepted(env, value, route):
    env(HTTPS_PROXY=value)
    assert toa.managed_proxy_route() == route
    assert toa.managed_proxy_route({"https_proxy": value}) == route


@pytest.mark.parametrize("values, reason", [
    ({}, toa.ROUTE_MISSING),
    ({"HTTPS_PROXY": "   "}, toa.ROUTE_MISSING),
    ({"HTTPS_PROXY": "http://127.0.0.1:1", "https_proxy": "http://127.0.0.1:2"}, toa.ROUTE_CONFLICTING),
    ({"HTTPS_PROXY": "http://127.0.0.1"}, toa.ROUTE_MALFORMED),
    ({"HTTPS_PROXY": "http://127.0.0.1:notaport"}, toa.ROUTE_MALFORMED),
    ({"HTTPS_PROXY": "http://127.0.0.1:99999"}, toa.ROUTE_MALFORMED),
    ({"HTTPS_PROXY": "http://user:pw@127.0.0.1:8080"}, toa.ROUTE_MALFORMED),
    ({"HTTPS_PROXY": "http://127.0.0.1:8080/relay"}, toa.ROUTE_MALFORMED),
    ({"HTTPS_PROXY": "http://127.0.0.1:8080?x=1"}, toa.ROUTE_MALFORMED),
    ({"HTTPS_PROXY": "http://127.0.0.1:8080#f"}, toa.ROUTE_MALFORMED),
    ({"HTTPS_PROXY": "127.0.0.1:8080"}, toa.ROUTE_UNSUPPORTED),
    ({"HTTPS_PROXY": "https://127.0.0.1:8080"}, toa.ROUTE_UNSUPPORTED),
    ({"HTTPS_PROXY": "socks5://127.0.0.1:1080"}, toa.ROUTE_UNSUPPORTED),
    ({"HTTPS_PROXY": "http://10.0.0.1:8080"}, toa.ROUTE_UNSUPPORTED),
    ({"HTTPS_PROXY": "http://proxy.example.com:8080"}, toa.ROUTE_UNSUPPORTED),
    ({"HTTPS_PROXY": "http://127.0.0.1:8080", "NO_PROXY": "*"}, toa.ROUTE_BYPASSED),
    ({"HTTPS_PROXY": "http://127.0.0.1:8080", "NO_PROXY": "api.openai.com"}, toa.ROUTE_BYPASSED),
    ({"HTTPS_PROXY": "http://127.0.0.1:8080", "no_proxy": ".openai.com"}, toa.ROUTE_BYPASSED),
    ({"HTTPS_PROXY": "http://127.0.0.1:8080", "NO_PROXY": "example.com, OpenAI.com"}, toa.ROUTE_BYPASSED),
])
def test_an_unusable_route_is_refused_with_its_closed_reason(env, values, reason):
    env(**values)
    with pytest.raises(toa.ManagedRouteUnavailable) as caught:
        toa.managed_proxy_route()
    assert caught.value.reason == reason and reason in toa.MANAGED_ROUTE_REASONS
    for value in values.values():
        if value.strip():
            assert value not in str(caught.value)              # no environment value is kept


def test_an_unrelated_no_proxy_list_does_not_bypass(env):
    env(HTTPS_PROXY="http://127.0.0.1:8080", NO_PROXY="localhost,127.0.0.1,.internal.example")
    assert toa.managed_proxy_route() == "http://127.0.0.1:8080"


# ─── the transport: refusal before any socket, pinned route otherwise ────────

@pytest.mark.parametrize("values", [
    {}, {"HTTPS_PROXY": "http://10.0.0.1:8080"},
    {"HTTPS_PROXY": "http://127.0.0.1:8080", "NO_PROXY": "api.openai.com"},
])
def test_a_managed_request_with_no_usable_route_never_reaches_a_handler(env, wire, values):
    env(**values)
    with pytest.raises(toa.ManagedRouteUnavailable):
        _send()
    assert wire == []                                           # nothing escaped


def test_a_managed_request_goes_through_the_validated_relay_only(env, wire, monkeypatch):
    env(HTTPS_PROXY="http://127.0.0.1:43739")
    # the opener is pinned: urllib's own environment lookup and bypass are never consulted
    monkeypatch.setattr(urllib.request, "getproxies", lambda: {"https": "http://203.0.113.9:1"})
    monkeypatch.setattr(urllib.request, "proxy_bypass", lambda host: True)
    assert _send() == (200, b"{}")
    assert len(wire) == 1
    sent = wire[0]
    assert (sent["via"], sent["tunnel"], sent["url"]) == ("127.0.0.1:43739", "api.openai.com",
                                                          toa.ENDPOINT)
    assert sent["headers"]["Host"] == "api.openai.com"
    assert not any(name.lower() == "authorization" for name in sent["headers"])


def test_env_key_mode_is_routed_exactly_as_before(env, wire):
    assert _send({"Authorization": "Bearer " + SECRET, **MANAGED_HEADERS}) == (200, b"{}")
    assert wire[0]["via"] == "api.openai.com" and wire[0]["tunnel"] is None   # direct, as before
    env(HTTPS_PROXY="http://10.0.0.1:8080")                    # env mode keeps urllib's own lookup
    _send({"Authorization": "Bearer " + SECRET})
    assert wire[1]["via"] == "10.0.0.1:8080"


def test_the_endpoint_lock_still_comes_first(env, wire):
    with pytest.raises(ValueError):
        toa._urllib_transport("https://another-host.invalid/v1/responses", MANAGED_HEADERS, b"{}", 5)
    assert wire == []


# ─── adapters, diagnostics and the harness journal ───────────────────────────

def test_both_adapters_keep_the_existing_transport_error_kind(env, wire):
    from engine import technical_orchestration_shadow as tos
    from tests.test_technical_orchestration_shadow import _request
    req, _ = _request()
    adapter = toa.OpenAIOrchestrationAdapter(allow_network=True,
                                             credential_mode=toa.CREDENTIAL_MODE_MANAGED_PROXY)
    res = tos.evaluate(req, adapter)
    assert (res.outcome, adapter.last_error_kind) == (tos.ERROR, toa.ERR_TRANSPORT)
    msnl = h.OpenAIMsnlAdapter(allow_network=True)
    assert msnl._call({"input": "synthetic"}) is None and msnl.last_error_kind == toa.ERR_TRANSPORT
    assert wire == []


def test_a_refused_route_has_its_own_closed_diagnostic_category():
    diag = toa.transport_failure_diagnostic(toa.ManagedRouteUnavailable(toa.ROUTE_BYPASSED))
    assert diag == {"version": 1, "category": toa.TF_MANAGED_ROUTE_REFUSED,
                    "exception_class": "ManagedRouteUnavailable",
                    "cause_class": toa.DIAGNOSTIC_UNAVAILABLE,
                    "tunnel_status": toa.DIAGNOSTIC_UNAVAILABLE}
    assert toa.TF_MANAGED_ROUTE_REFUSED in toa.TRANSPORT_FAILURE_CATEGORIES


def test_the_measured_call_journals_a_refused_route_as_not_sent(env, wire):
    adapter = h.OpenAIMsnlAdapter(allow_network=True)
    reply, meta = h._measured_call(adapter, {"input": "synthetic"})
    assert reply is None and adapter.last_error_kind == toa.ERR_TRANSPORT
    assert meta["sent"] is False and meta["sent_at_utc"] == "UNAVAILABLE"
    assert meta["transport_failure"]["category"] == toa.TF_MANAGED_ROUTE_REFUSED
    assert meta["http_status"] == "UNAVAILABLE" and wire == []
    assert SECRET not in json.dumps(meta)


def test_a_refused_route_stops_a_context_history_run_with_nothing_sent(env, wire, tmp_path):
    manifest = h.context_history_manifest()
    path = tmp_path / "journal.jsonl"
    with open(path, "x", encoding="utf-8") as journal:
        stop, rows, spend = h.context_history_run(h.OpenAIMsnlAdapter(allow_network=True),
                                                  manifest, journal)
    report = h.context_history_report(manifest, stop, rows, spend)
    assert report["outcome"] == h.CH_INVALID and report["stop"]["reason"] == toa.ERR_TRANSPORT
    assert spend["requests_sent"] == 0 and wire == []
    attempts = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines()
                if json.loads(l)["event"] == "attempt"]
    assert len(attempts) == 1 and attempts[0]["sent"] is False
    assert attempts[0]["transport_failure"]["category"] == toa.TF_MANAGED_ROUTE_REFUSED
