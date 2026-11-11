"""R2 TRANSPORT DIAGNOSTIC CAPTURE — allowlisted failure diagnostics only.

The evaluation transport (``engine/technical_orchestration_openai.py``) and the
harness's measured call (``scripts/run_msnl_eval.py``) now keep, for a failed
request, only allowlisted fields: for a non-2xx response a validated request id,
the provider error type / code mapped onto closed lists and presence-only origin
indicators; for a transport exception a closed category and class names; for
every request a UTC send time and latency. Nothing here changes an error kind,
an outcome, the retry / timeout / transport / authentication policy, the frozen
evaluation inputs or the recorded runs.

Everything is offline: a real local socket server (and a local fake proxy) drives
urllib's own HTTP, redirect, error and tunnel code; the remaining exception
classes are synthetic. No provider is contacted.
"""
import http.client
import json
import re
import socket
import ssl
import threading
import time
import urllib.error
import urllib.request

import pytest

from engine import technical_orchestration_openai as toa
from tests.test_msnl_context_history_evaluation import Fake, _expected, _wrap, manifest  # noqa: F401
from tests.test_msnl_llm_eval_harness import h

SECRET_KEY = "sk-proj-SYNTHETICSECRET0123456789abcdef"
SECRET_ORG = "org-SYNTHETICORGSECRET"
SECRET_COOKIE = "SYNTHETICCOOKIESECRET"
CASE_TEXT = "SYNTHETIC CASE TEXT that must never be diagnosed"
REQUEST_ID = "req_0123456789abcdef0123456789abcdef"
OPENAI_401 = json.dumps({"error": {
    "message": "Incorrect API key provided: %s. You can find your API key at ..." % SECRET_KEY,
    "type": "invalid_request_error", "param": None, "code": "invalid_api_key"}}).encode("utf-8")
UTC = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z\Z")
FORBIDDEN = (SECRET_KEY, "sk-proj", SECRET_ORG, SECRET_COOKIE, "Incorrect API key", "realm",
             CASE_TEXT, "Authorization", "Bearer")


def _clean(text):
    for needle in FORBIDDEN:
        assert needle not in text, needle


# ─── a real local server (one scripted behaviour per connection) ─────────────

class _Server:
    """``relay=True``: acknowledges the managed relay's CONNECT (kept in ``tunnels``)
    and applies ``behave`` to the request inside the tunnel; ``relay=False``:
    applies ``behave`` to the first request it receives, the CONNECT included."""

    def __init__(self, behave, relay=False):
        self.behave, self.requests, self.relay, self.tunnels = behave, [], relay, []
        self.sock = socket.socket()
        self.sock.bind(("127.0.0.1", 0))
        self.sock.listen(4)
        self.port = self.sock.getsockname()[1]
        self.thread = threading.Thread(target=self._serve, daemon=True)
        self.thread.start()

    def _serve(self):
        try:
            conn, _ = self.sock.accept()
        except OSError:
            return
        with conn:
            conn.settimeout(5)
            try:
                head, rest = self._read(conn, b"")
                if self.relay and head.startswith(b"CONNECT "):
                    self.tunnels.append(head)
                    conn.sendall(b"HTTP/1.1 200 Connection established\r\n\r\n")
                    head, rest = self._read(conn, rest)
                self.requests.append(head + b"\r\n\r\n" + rest)
                self.behave(conn)
            except OSError:
                pass

    @staticmethod
    def _read(conn, data):
        while b"\r\n\r\n" not in data:
            chunk = conn.recv(65536)
            if not chunk:
                break
            data += chunk
        head, _, rest = data.partition(b"\r\n\r\n")
        length = re.search(rb"(?i)content-length:\s*(\d+)", head)
        while length and len(rest) < int(length.group(1)):
            rest += conn.recv(65536)
        return head, rest

    def close(self):
        self.sock.close()


def _response(status, reason, headers, body):
    lines = ["HTTP/1.1 %d %s" % (status, reason)] + ["%s: %s" % kv for kv in headers]
    lines.append("Content-Length: %d" % len(body))
    lines.append("Connection: close")
    return ("\r\n".join(lines) + "\r\n\r\n").encode("latin-1") + body


@pytest.fixture
def local(monkeypatch):
    """Routes the default transport's ONE https request to a local plain-HTTP
    socket, through urllib's real handler chain (no network). A managed-mode
    request may leave only through a validated loopback relay
    (R2-MANAGED-EGRESS-FAIL-CLOSED-01), so the route is always set: the local
    server acknowledges its CONNECT and answers inside the tunnel, unless
    ``proxy=True`` asks it to answer the CONNECT itself."""
    for name in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy",
                 "ALL_PROXY", "all_proxy", "NO_PROXY", "no_proxy"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("HTTPS_PROXY", "http://127.0.0.1:1")     # a valid relay route
    servers = []

    def route(port):
        def https_open(handler, req):
            def connect(host, timeout=None, **_kw):
                return http.client.HTTPConnection("127.0.0.1", port, timeout=timeout)
            return handler.do_open(connect, req)
        monkeypatch.setattr(urllib.request.HTTPSHandler, "https_open", https_open)

    def start(behave, proxy=False):
        server = _Server(behave, relay=not proxy)
        servers.append(server)
        route(server.port)
        monkeypatch.setenv("HTTPS_PROXY", "http://127.0.0.1:%d" % server.port)
        return server
    start.route = route
    yield start
    for server in servers:
        server.close()


def _send(timeout=5):
    return toa._urllib_transport(toa.ENDPOINT, {"Content-Type": "application/json"},
                                 json.dumps({"input": CASE_TEXT}).encode("utf-8"), timeout)


# ─── HTTP failures: only the allowlisted diagnostic leaves the transport ──────

def test_an_openai_shaped_401_keeps_only_allowlisted_fields(local):
    headers = [("Content-Type", "application/json"), ("x-request-id", REQUEST_ID),
               ("openai-processing-ms", "12"), ("openai-organization", SECRET_ORG),
               ("Server", "cloudflare"), ("WWW-Authenticate", 'Bearer realm="OpenAI"'),
               ("Set-Cookie", "__cf_bm=%s" % SECRET_COOKIE)]
    server = local(lambda conn: conn.sendall(_response(401, "Unauthorized", headers, OPENAI_401)))
    status, raw = _send()
    assert status == 401
    assert json.loads(raw) == {toa.HTTP_DIAGNOSTIC_KEY: {
        "version": 1, "status": 401, "request_id": REQUEST_ID, "request_id_header": True,
        "provider_error_object": True, "error_type": "invalid_request_error",
        "error_code": "invalid_api_key", "openai_headers": True, "server_cloudflare": True,
        "www_authenticate": True}}
    _clean(raw.decode("utf-8"))
    sent = server.requests[0].decode("utf-8")       # managed mode: no credential sent
    assert "authorization" not in sent.lower() and CASE_TEXT in sent
    assert server.tunnels[0].startswith(b"CONNECT api.openai.com:")   # through the relay only


def test_a_proxy_shaped_401_is_told_apart_but_not_attributed(local):
    local(lambda conn: conn.sendall(_response(401, "Unauthorized",
                                              [("Content-Type", "text/plain")], b"Unauthorized")))
    status, raw = _send()
    diag = toa.read_http_diagnostic(raw)
    assert status == 401 and diag["status"] == 401
    assert (diag["provider_error_object"], diag["openai_headers"], diag["server_cloudflare"],
            diag["request_id_header"], diag["request_id"]) == (False, False, False, False,
                                                              toa.DIAGNOSTIC_UNAVAILABLE)
    assert diag["error_type"] == diag["error_code"] == toa.DIAGNOSTIC_UNAVAILABLE


def test_a_redirect_is_still_refused_and_its_location_is_never_kept(local):
    local(lambda conn: conn.sendall(_response(
        302, "Found", [("Location", "https://another-host.invalid/%s" % SECRET_KEY)], b"")))
    status, raw = _send()
    assert status == 302 and toa.read_http_diagnostic(raw)["status"] == 302
    _clean(raw.decode("utf-8"))
    assert "another-host" not in raw.decode("utf-8")


@pytest.mark.parametrize("value", [
    "req_short", "req_../../etc/passwd0", SECRET_KEY, "req_" + "a" * 65, "req_abc def12345",
    "req_0123456789abcdef\n"])
def test_a_request_id_that_is_not_strictly_valid_is_never_kept(value):
    diag = toa.http_error_diagnostic(401, {"X-Request-Id": value}, b"")
    assert diag["request_id"] == toa.DIAGNOSTIC_UNAVAILABLE and diag["request_id_header"] is True
    _clean(json.dumps(diag))


def test_provider_values_outside_the_closed_lists_are_recorded_only_as_other():
    body = json.dumps({"error": {"type": "free text %s" % SECRET_KEY,
                                 "code": "brand_new_code", "message": "x"}}).encode("utf-8")
    diag = toa.http_error_diagnostic(500, {}, body)
    assert (diag["provider_error_object"], diag["error_type"], diag["error_code"]) == \
        (True, toa.DIAGNOSTIC_OTHER, toa.DIAGNOSTIC_OTHER)
    nulls = json.dumps({"error": {"message": "m", "type": "server_error", "code": None}})
    diag = toa.http_error_diagnostic(500, {}, nulls.encode("utf-8"))
    assert (diag["error_type"], diag["error_code"]) == ("server_error", toa.DIAGNOSTIC_UNAVAILABLE)
    _clean(json.dumps(diag))


def test_an_oversized_or_strange_error_body_or_headers_yield_no_attribution():
    big = json.dumps({"error": {"type": "server_error", "pad": "x" * toa.MAX_ERROR_BODY_BYTES}})
    assert toa.http_error_diagnostic(500, None, big.encode("utf-8"))["provider_error_object"] is False
    for body in (b"\xff\xfe", b"[]", b'{"error": "text"}', b"null", None, "text"):
        diag = toa.http_error_diagnostic(503, object(), body)
        assert diag["provider_error_object"] is False and diag["openai_headers"] is False
    assert toa.http_error_diagnostic(True, {}, b"")["status"] == toa.DIAGNOSTIC_UNAVAILABLE


def test_only_an_exact_diagnostic_document_is_ever_read_back():
    good = toa.http_diagnostic_document(401, {"x-request-id": REQUEST_ID}, OPENAI_401)
    assert toa.read_http_diagnostic(good)["request_id"] == REQUEST_ID
    doc = json.loads(good)
    for mutate in (
            lambda d: d[toa.HTTP_DIAGNOSTIC_KEY].update(error_type="free text"),
            lambda d: d[toa.HTTP_DIAGNOSTIC_KEY].update(request_id=SECRET_KEY),
            lambda d: d[toa.HTTP_DIAGNOSTIC_KEY].update(extra="x"),
            lambda d: d[toa.HTTP_DIAGNOSTIC_KEY].pop("status"),
            lambda d: d[toa.HTTP_DIAGNOSTIC_KEY].update(openai_headers="yes"),
            lambda d: d[toa.HTTP_DIAGNOSTIC_KEY].update(version=2),
            lambda d: d.update(error={"message": SECRET_KEY})):
        bad = json.loads(json.dumps(doc))
        mutate(bad)
        assert toa.read_http_diagnostic(json.dumps(bad).encode("utf-8")) is None
    for raw in (OPENAI_401, b"", b"\xff", b"[]"):
        assert toa.read_http_diagnostic(raw) is None


# ─── transport failures: a closed category, never the exception's text ────────

def _closed_conn(conn):
    conn.shutdown(socket.SHUT_RDWR)


def _slow(conn):
    time.sleep(1.5)


def _short_body(conn):
    conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 100\r\nConnection: close\r\n\r\n0123456789")
    conn.shutdown(socket.SHUT_RDWR)


@pytest.mark.parametrize("behave, timeout, category, cls, cause", [
    (_closed_conn, 5, toa.TF_REMOTE_DISCONNECTED, "RemoteDisconnected", toa.DIAGNOSTIC_UNAVAILABLE),
    (_slow, 0.3, toa.TF_TIMEOUT, "TimeoutError", toa.DIAGNOSTIC_UNAVAILABLE),
    (_short_body, 5, toa.TF_INCOMPLETE_READ, "IncompleteRead", toa.DIAGNOSTIC_UNAVAILABLE),
])
def test_real_transport_failures_from_a_local_server_are_classified(local, behave, timeout,
                                                                   category, cls, cause):
    local(behave)
    with pytest.raises(Exception) as caught:          # the transport still raises, as before
        _send(timeout)
    diag = toa.transport_failure_diagnostic(caught.value)
    assert (diag["category"], diag["exception_class"], diag["cause_class"]) == (category, cls, cause)
    assert diag["tunnel_status"] == toa.DIAGNOSTIC_UNAVAILABLE


def test_a_refused_connection_is_classified_through_urllibs_wrapper(local):
    probe = socket.socket()
    probe.bind(("127.0.0.1", 0))
    port = probe.getsockname()[1]
    probe.close()                                      # nothing listens on that port
    local.route(port)
    with pytest.raises(urllib.error.URLError) as caught:
        _send()
    assert toa.transport_failure_diagnostic(caught.value) == {
        "version": 1, "category": toa.TF_CONNECTION_REFUSED, "exception_class": "URLError",
        "cause_class": "ConnectionRefusedError", "tunnel_status": toa.DIAGNOSTIC_UNAVAILABLE}


def test_a_proxy_refusing_the_tunnel_keeps_only_its_status(local):
    server = local(lambda conn: conn.sendall(
        b"HTTP/1.1 503 Service Unavailable %s\r\nContent-Length: 0\r\n\r\n" % SECRET_KEY.encode()),
        proxy=True)
    with pytest.raises(urllib.error.URLError) as caught:
        _send()
    # the tunnel is requested for the approved host (the port is the test's plain connection's)
    assert server.requests[0].startswith(b"CONNECT api.openai.com:")
    diag = toa.transport_failure_diagnostic(caught.value)
    assert diag == {"version": 1, "category": toa.TF_TUNNEL_REFUSED, "exception_class": "URLError",
                    "cause_class": "OSError", "tunnel_status": 503}
    _clean(json.dumps(diag))


@pytest.mark.parametrize("exc, category, tunnel", [
    (ssl.SSLError("certificate verify failed %s" % SECRET_KEY), toa.TF_TLS, None),
    (urllib.error.URLError(ssl.SSLCertVerificationError(1, SECRET_KEY)), toa.TF_TLS, None),
    (socket.gaierror(-2, "Name or service not known %s" % SECRET_KEY), toa.TF_DNS, None),
    (ConnectionResetError(104, "reset %s" % SECRET_KEY), toa.TF_CONNECTION_RESET, None),
    (BrokenPipeError(32, SECRET_KEY), toa.TF_CONNECTION_ABORTED, None),
    (ConnectionAbortedError(SECRET_KEY), toa.TF_CONNECTION_ABORTED, None),
    (http.client.BadStatusLine(SECRET_KEY), toa.TF_PROTOCOL, None),
    (urllib.error.URLError(OSError("Tunnel connection failed: 407 Proxy %s" % SECRET_KEY)),
     toa.TF_TUNNEL_REFUSED, 407),
    (urllib.error.URLError(OSError("boom Tunnel connection failed: 503 %s" % SECRET_KEY)),
     toa.TF_OTHER, None),
    (OSError("Tunnel connection failed: 5030"), toa.TF_OTHER, None),
    (urllib.error.URLError("plain reason %s" % SECRET_KEY), toa.TF_OTHER, None),
    (ValueError(SECRET_KEY), toa.TF_OTHER, None),
])
def test_every_exception_maps_to_a_closed_category_without_its_text(exc, category, tunnel):
    diag = toa.transport_failure_diagnostic(exc)
    assert diag["category"] == category and diag["category"] in toa.TRANSPORT_FAILURE_CATEGORIES
    assert diag["tunnel_status"] == (toa.DIAGNOSTIC_UNAVAILABLE if tunnel is None else tunnel)
    assert set(diag) == {"version", "category", "exception_class", "cause_class", "tunnel_status"}
    _clean(json.dumps(diag))


def test_an_unusual_exception_class_name_is_never_recorded():
    weird = type("Weird-Name sk", (Exception,), {})
    assert toa.transport_failure_diagnostic(weird())["exception_class"] == toa.DIAGNOSTIC_OTHER


# ─── the harness keeps them; error kinds, outcome and retry are unchanged ─────

def _adapter(transport):
    return h.OpenAIMsnlAdapter(allow_network=True, transport=transport)


def _raise(exc):
    def transport(url, headers, body, timeout):
        raise exc
    return transport


def test_the_measured_call_records_a_transport_failure_and_keeps_the_error_kind():
    adapter = _adapter(_raise(urllib.error.URLError(OSError("Tunnel connection failed: 503 x"))))
    reply, meta = h._measured_call(adapter, {"input": CASE_TEXT})
    assert reply is None and adapter.last_error_kind == toa.ERR_TRANSPORT
    assert meta["transport_failure"]["category"] == toa.TF_TUNNEL_REFUSED
    assert meta["transport_failure"]["tunnel_status"] == 503
    assert meta["http_diagnostic"] is None and meta["http_status"] == "UNAVAILABLE"
    assert isinstance(meta["latency_ms"], int) and UTC.match(meta["sent_at_utc"])
    _clean(json.dumps(meta))


def test_the_measured_call_reads_only_an_exact_diagnostic_document():
    doc = toa.http_diagnostic_document(401, {"x-request-id": REQUEST_ID}, OPENAI_401)
    adapter = _adapter(lambda *a: (401, doc))
    reply, meta = h._measured_call(adapter, {"input": CASE_TEXT})
    assert reply is None and adapter.last_error_kind == toa.ERR_HTTP_STATUS
    assert meta["http_diagnostic"] == toa.read_http_diagnostic(doc)
    assert meta["transport_failure"] is None and meta["http_status"] == 401
    # a transport that hands back a raw provider body is never interpreted
    adapter = _adapter(lambda *a: (401, OPENAI_401))
    reply, meta = h._measured_call(adapter, {"input": CASE_TEXT})
    assert meta["http_diagnostic"] == "UNAVAILABLE" and adapter.last_error_kind == toa.ERR_HTTP_STATUS
    _clean(json.dumps(meta))


def test_a_successful_call_carries_no_failure_diagnostic(manifest):
    case = h.ch_ordered(manifest)[0]
    adapter = _adapter(lambda *a: _wrap(_expected(case)))
    reply, meta = h._measured_call(adapter, h.ch_payload(manifest, case, adapter._model))
    assert reply is not None and meta["http_status"] == 200
    assert meta["http_diagnostic"] is None and meta["transport_failure"] is None
    assert UTC.match(meta["sent_at_utc"]) and isinstance(meta["latency_ms"], int)


def _run_until(manifest, n, failure, tmp_path):
    """Correct replies for the first ``n`` cases in frozen order, then ``failure``."""
    order = [c["case_id"] for c in h.ch_ordered(manifest)]

    def decide(case):
        if order.index(case["case_id"]) < n:
            return _expected(case)
        return failure()
    fake = Fake(manifest, decide)
    adapter = _adapter(fake)
    path = tmp_path / "journal.jsonl"
    with open(path, "x", encoding="utf-8") as journal:
        stop, rows, spend = h.context_history_run(adapter, manifest, journal)
    events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    return h.context_history_report(manifest, stop, rows, spend), events, fake


def test_a_401_mid_run_is_journaled_with_its_diagnostic_and_stops_invalid_once(manifest, tmp_path):
    doc = toa.http_diagnostic_document(401, {"x-request-id": REQUEST_ID}, OPENAI_401)
    report, events, fake = _run_until(manifest, 3, lambda: (401, doc), tmp_path)
    assert report["outcome"] == h.CH_INVALID and report["stop"]["reason"] == toa.ERR_HTTP_STATUS
    assert len(fake.bodies) == 4                                   # no retry
    attempts = [e for e in events if e["event"] == "attempt"]
    assert [a["http_diagnostic"] is None for a in attempts] == [True, True, True, False]
    last = attempts[-1]
    assert last["http_diagnostic"]["request_id"] == REQUEST_ID
    assert last["http_diagnostic"]["error_code"] == "invalid_api_key"
    assert last["transport_failure"] is None and last["http_status"] == 401
    assert all(UTC.match(a["sent_at_utc"]) and isinstance(a["latency_ms"], int) for a in attempts)
    assert report["rows"][-1]["attempt"]["http_diagnostic"] == last["http_diagnostic"]
    _clean(json.dumps(events) + json.dumps(report))


def test_a_transport_failure_mid_run_is_journaled_and_stops_invalid_once(manifest, tmp_path):
    def fail():
        raise urllib.error.URLError(TimeoutError("timed out %s" % SECRET_KEY))
    report, events, fake = _run_until(manifest, 2, fail, tmp_path)
    assert report["outcome"] == h.CH_INVALID and report["stop"]["reason"] == toa.ERR_TRANSPORT
    assert len(fake.bodies) == 3
    last = [e for e in events if e["event"] == "attempt"][-1]
    assert last["transport_failure"] == {"version": 1, "category": toa.TF_TIMEOUT,
                                         "exception_class": "URLError",
                                         "cause_class": "TimeoutError",
                                         "tunnel_status": toa.DIAGNOSTIC_UNAVAILABLE}
    assert last["http_diagnostic"] is None and last["http_status"] == "UNAVAILABLE"
    _clean(json.dumps(events) + json.dumps(report))


def test_the_gate_stays_closed_and_both_recorded_runs_are_untouched():
    from tests.test_msnl_context_history_evaluation import (
        test_every_recorded_run_is_pinned_distinct_and_the_gate_is_closed as _runs_pinned)
    _runs_pinned()                         # runs 01-03 byte for byte; the gate is closed
    assert toa.TIMEOUT_SECONDS == 90 and toa.ENDPOINT == "https://api.openai.com/v1/responses"
