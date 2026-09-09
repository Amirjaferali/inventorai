"""P10-OB1 — Provider-Neutral Observability Foundation (RED/GREEN).

Behaviour-based tests for the Owner-authorized bounded Phase-10 implementation
gate `P10-OB1 — Provider-Neutral Observability Foundation Increment`:

  1. ONE minimal truthful health/readiness surface — `GET /health` — answering
     "can this application process requests using its required local runtime
     dependencies?" with a deterministic, machine-readable, data-minimized
     JSON body: 200 `{"database": "ok"|"uninitialized", "status": "ok"}` or
     503 `{"database": "error", "status": "unavailable"}`. The probe is
     side-effect-free: it never creates a database file, schema, or row, and
     never mutates durable data.
  2. The smallest structured application-logging seam
     (`web/observability.py`, stdlib ``logging`` only): JSON-line events with
     a stable bounded schema, a strict field ALLOWLIST, and token-pattern
     value validation so emails, free-form user text, session identifiers,
     tokens, and secrets can never pass through the governed seam.

Load-bearing data-minimization boundary proven here: no IP address,
user-agent, device metadata, account email, project/user content, session ID,
token, or secret is collected, emitted, or exposed by either surface; no
third-party telemetry or provider dependency exists.
"""
import hashlib
import json
import logging
import os
import re
import sqlite3

import pytest

import web.app as webapp
from web.app import app

from web import observability as obs

PW = "correct horse battery staple"
IDEA = ("An electronic circuit uses a sensor and a switch to cut the power "
        "when the current gets too high.")
NOW = "2026-01-01T00:00:00.000000Z"

HEALTH_PATH = "/health"
HEALTHY_BODY = {"database": "ok", "status": "ok"}
UNINITIALIZED_BODY = {"database": "uninitialized", "status": "ok"}
ERROR_BODY = {"database": "error", "status": "unavailable"}


@pytest.fixture
def db_path():
    return os.environ["INVENTORAI_DB_PATH"]


def _new_client():
    app.config["TESTING"] = True
    return app.test_client()


def _init_db():
    """Initialize the isolated test DB through the real lazy store seam and
    return the account store (this is REAL application use, not the probe)."""
    store = webapp._get_account_store()
    from engine import account_credentials as _acct
    store.create_account("ob1-acct", _acct.normalize_email("ob1@example.com"),
                         _acct.hash_password(PW), NOW)
    return store


class _CaptureHandler(logging.Handler):
    """Captures the seam's FORMATTED JSON lines using the seam's own public
    formatter, independent of stream/handler wiring."""
    def __init__(self):
        super().__init__()
        self.lines = []
        self.setFormatter(obs.OperationalJsonFormatter())

    def emit(self, record):
        self.lines.append(self.format(record))


@pytest.fixture
def captured():
    handler = _CaptureHandler()
    logger = logging.getLogger(obs.OPERATIONAL_LOGGER_NAME)
    logger.addHandler(handler)
    yield handler.lines
    logger.removeHandler(handler)


def _file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


# ==========================================================================
# Health surface — existence, semantics, determinism
# ==========================================================================
def test_health_endpoint_exists_and_is_json():
    r = _new_client().get(HEALTH_PATH)
    assert r.status_code in (200, 503)
    assert r.mimetype == "application/json"
    json.loads(r.get_data(as_text=True))


def test_health_ok_when_database_initialized():
    _init_db()
    r = _new_client().get(HEALTH_PATH)
    assert r.status_code == 200
    assert json.loads(r.get_data(as_text=True)) == HEALTHY_BODY


def test_health_uninitialized_when_no_database_file(monkeypatch, tmp_path):
    monkeypatch.setenv("INVENTORAI_DB_PATH",
                       str(tmp_path / "never-created.sqlite"))
    r = _new_client().get(HEALTH_PATH)
    assert r.status_code == 200
    assert json.loads(r.get_data(as_text=True)) == UNINITIALIZED_BODY
    # the probe itself must NOT have created the file
    assert not os.path.exists(str(tmp_path / "never-created.sqlite"))


def test_health_error_is_deterministic_503_on_invalid_database(monkeypatch,
                                                               tmp_path):
    bad = tmp_path / "corrupt.sqlite"
    bad.write_bytes(b"this is not a sqlite database" * 40)
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(bad))
    client = _new_client()
    for _ in range(3):
        r = client.get(HEALTH_PATH)
        assert r.status_code == 503
        assert json.loads(r.get_data(as_text=True)) == ERROR_BODY


def test_health_repeated_probes_deterministic_and_nonmutating(db_path):
    _init_db()
    client = _new_client()
    first = client.get(HEALTH_PATH)
    before = _file_sha256(db_path)
    for _ in range(10):
        r = client.get(HEALTH_PATH)
        assert r.status_code == first.status_code
        assert r.get_data() == first.get_data()
    assert _file_sha256(db_path) == before   # zero durable mutation


def test_health_probe_writes_no_rows(db_path):
    store = _init_db()
    counts_before = {
        t: store._conn.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]
        for (t,) in store._conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%'")}
    client = _new_client()
    for _ in range(5):
        client.get(HEALTH_PATH)
    counts_after = {
        t: store._conn.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]
        for t in counts_before}
    assert counts_after == counts_before


def test_health_response_data_minimized(db_path):
    _init_db()
    r = _new_client().get(HEALTH_PATH)
    body = json.loads(r.get_data(as_text=True))
    assert set(body.keys()) == {"status", "database"}
    assert body["status"] in ("ok", "unavailable")
    assert body["database"] in ("ok", "uninitialized", "error")
    text = r.get_data(as_text=True)
    assert db_path not in text                      # no DB path
    assert os.path.dirname(db_path) not in text     # no filesystem path
    assert "sqlite" not in text.lower()             # no engine/file details
    assert "traceback" not in text.lower()


def test_health_requires_no_authentication_and_no_session():
    client = _new_client()
    r = client.get(HEALTH_PATH)
    assert r.status_code in (200, 503)
    # a probe must not mint a session cookie
    assert "Set-Cookie" not in r.headers


# ==========================================================================
# Structured logging seam — bounded schema, allowlist, data minimization
# ==========================================================================
def test_emit_produces_bounded_json_event(captured):
    obs.emit("ob1.test_event", component="health", outcome="ok", count=3)
    assert len(captured) == 1
    line = json.loads(captured[0])
    assert line["event"] == "ob1.test_event"
    assert line["level"] == "INFO"
    assert line["component"] == "health"
    assert line["outcome"] == "ok"
    assert line["count"] == 3
    assert "ts" in line
    assert set(line.keys()) <= {"ts", "level", "event"} | obs.ALLOWED_FIELDS


def test_emit_levels_bounded(captured):
    obs.emit("ob1.warn_event", level="warning", component="health")
    obs.emit("ob1.error_event", level="error", component="health")
    levels = [json.loads(l)["level"] for l in captured]
    assert levels == ["WARNING", "ERROR"]


def test_emit_rejects_unsupported_fields(captured):
    obs.emit("ob1.test_event", component="health",
             email="user@example.com", idea_text="my secret invention",
             ip="203.0.113.7", user_agent="Mozilla/5.0")
    line = json.loads(captured[0])
    blob = captured[0]
    assert "email" not in line and "idea_text" not in line
    assert "ip" not in line and "user_agent" not in line
    assert "user@example.com" not in blob
    assert "secret invention" not in blob
    assert "203.0.113.7" not in blob and "Mozilla" not in blob


def test_emit_blocks_sensitive_values_even_in_allowed_fields(captured):
    obs.emit("ob1.test_event",
             component="user@example.com",          # email shape
             outcome="free text with spaces",       # free-form user text
             error_class="a" * 65,                  # over-long token/secret
             detail_code={"nested": "payload"})     # arbitrary object
    line = json.loads(captured[0])
    assert "component" not in line
    assert "outcome" not in line
    assert "error_class" not in line
    assert "detail_code" not in line
    assert "user@example.com" not in captured[0]
    assert "free text" not in captured[0]
    # secret-shaped token values (hyphenated / mixed-case credential formats)
    # must be rejected even inside allowed fields
    obs.emit("ob1.test_event",
             detail_code="sk-SECRET-VALUE-000",
             error_class="sk-SECRET-VALUE-000",
             component="AKIA0000EXAMPLEKEY",
             outcome="dGhpc0lzQmFzZTY0LWlzaA==")
    line2 = json.loads(captured[1])
    assert set(line2.keys()) == {"ts", "level", "event"}
    assert "SECRET" not in captured[1] and "AKIA" not in captured[1]


def test_emit_never_raises_on_bad_input():
    obs.emit("ob1.ok", component=object())          # unserializable value
    obs.emit("INVALID EVENT NAME !!", component="health")
    obs.emit("ob1.ok", **{"weird key": "x"})        # unsupported field name


def test_no_ip_or_user_agent_reaches_operational_logs(captured, monkeypatch,
                                                      tmp_path):
    bad = tmp_path / "corrupt.sqlite"
    bad.write_bytes(b"garbage-not-a-database" * 50)
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(bad))
    client = _new_client()
    r = client.get(HEALTH_PATH, headers={
        "X-Forwarded-For": "198.51.100.99",
        "User-Agent": "EvilProbe/9.9 (fingerprint)"})
    assert r.status_code == 503
    blob = "".join(captured)
    assert "198.51.100.99" not in blob
    assert "EvilProbe" not in blob
    assert str(bad) not in blob                    # no DB path in logs


def test_probe_failure_emits_safe_bounded_event(captured, monkeypatch,
                                                tmp_path):
    bad = tmp_path / "corrupt.sqlite"
    bad.write_bytes(b"garbage-not-a-database" * 50)
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(bad))
    _new_client().get(HEALTH_PATH)
    events = [json.loads(l) for l in captured]
    probe_events = [e for e in events if e["event"] == "health.db_probe_failed"]
    assert probe_events, "expected a health.db_probe_failed operational event"
    event = probe_events[0]
    assert event["level"] == "WARNING"
    # bounded, token-like error category only — never message text or a path
    assert re.match(r"^[A-Za-z0-9_.:-]{1,64}$", event["error_class"])
    assert set(event.keys()) <= {"ts", "level", "event"} | obs.ALLOWED_FIELDS


def test_seam_is_stdlib_only_no_provider_dependency():
    source = open(obs.__file__.replace(".pyc", ".py")).read()
    for forbidden in ("sentry", "datadog", "newrelic", "splunk",
                      "opentelemetry", "prometheus", "grafana", "cloudwatch",
                      "requests", "urllib3", "httpx", "socket", "pagerduty",
                      "webhook", "http://", "https://"):
        assert forbidden not in source.lower(), forbidden
    import web.observability
    assert web.observability.logging is logging   # stdlib logging seam


def test_health_route_uses_no_request_metadata():
    """The /health route and probe must not read IP/user-agent/device
    metadata from the request at all (source-level data-truth proof)."""
    import inspect
    source = inspect.getsource(webapp.health)
    source += inspect.getsource(webapp._database_health)
    for forbidden in ("remote_addr", "REMOTE_ADDR", "X-Forwarded-For",
                      "user_agent", "User-Agent", "headers"):
        assert forbidden not in source, forbidden


# ==========================================================================
# PERF-01 — bounded initialized-store health probes
#
# Proving the database is readable must not enumerate every project or count
# every account. These tests pin the DETERMINISTIC operation shape: which
# methods the health path invokes, which it must never invoke again, and that
# the probes stay bounded as the tables grow. Nothing here asserts elapsed time
# or claims theoretical O(1) database latency.
# ==========================================================================
def _record_store_with(n_projects):
    """Populate the app-scoped record store with `n_projects` real projects."""
    from engine.record_contract import ProjectRecordContract
    store = webapp._get_store()
    for i in range(n_projects):
        store.create_project(ProjectRecordContract(idea_id="perf01-%d" % i,
                                                   assertions=[]),
                             project_id="perf01-p%d" % i)
    return store


def _account_store_with(n_accounts):
    from engine import account_credentials as _acct
    store = webapp._get_account_store()
    for i in range(n_accounts):
        store.create_account("perf01-a%d" % i,
                             _acct.normalize_email("perf01-%d@example.com" % i),
                             _acct.hash_password(PW), NOW)
    return store


def test_perf01_health_uses_bounded_probes_and_never_enumerates(monkeypatch):
    """Initialized `/health` invokes each initialized store's bounded probe and
    calls neither `project_ids()` nor `count_accounts()`."""
    from engine.record_store import SqliteRecordStore
    from engine.account_store import SqliteAccountStore
    _init_db()
    _record_store_with(3)
    calls = []
    for cls, name in ((SqliteRecordStore, "ping"), (SqliteAccountStore, "ping"),
                      (SqliteRecordStore, "project_ids"),
                      (SqliteAccountStore, "count_accounts")):
        real = getattr(cls, name)
        label = "%s.%s" % (cls.__name__, name)

        def counting(self, _real=real, _label=label, *a, **k):
            calls.append(_label)
            return _real(self, *a, **k)
        monkeypatch.setattr(cls, name, counting)
    r = _new_client().get(HEALTH_PATH)
    assert r.status_code == 200
    assert json.loads(r.get_data(as_text=True)) == HEALTHY_BODY
    assert "SqliteRecordStore.ping" in calls
    assert "SqliteAccountStore.ping" in calls
    assert "SqliteRecordStore.project_ids" not in calls
    assert "SqliteAccountStore.count_accounts" not in calls


def test_perf01_health_probe_sql_is_bounded_as_tables_grow(monkeypatch):
    """The SQL the initialized health path emits is the same bounded
    `LIMIT 1` shape whatever the table sizes are: no whole-table COUNT and no
    unbounded project enumeration."""
    _init_db()
    seen = []

    class _ConnProxy:
        """Records the SQL each probe emits without changing behaviour
        (``sqlite3.Connection.execute`` is read-only, so the connection is
        wrapped rather than patched)."""
        def __init__(self, real):
            self._real = real

        def execute(self, sql, *a, **k):
            seen.append(" ".join(sql.split()).upper())
            return self._real.execute(sql, *a, **k)

        def __getattr__(self, name):
            return getattr(self._real, name)

    def _watch(store):
        monkeypatch.setattr(store, "_conn", _ConnProxy(store._conn))

    for size in (0, 5):
        seen.clear()
        _record_store_with(size)
        _account_store_with(size)
        _watch(webapp._get_store())
        _watch(webapp._get_account_store())
        r = _new_client().get(HEALTH_PATH)
        assert r.status_code == 200
        probes = [s for s in seen if s.startswith("SELECT")]
        assert probes == ["SELECT 1 FROM ACCOUNTS LIMIT 1",
                          "SELECT 1 FROM PROJECTS LIMIT 1"], (size, seen)
        assert not any("COUNT(" in s for s in seen), (size, seen)
        assert not any("SELECT PROJECT_ID FROM PROJECTS" in s for s in seen), \
            (size, seen)
        monkeypatch.undo()


def test_perf01_health_unchanged_for_uninitialized_corrupt_and_unavailable(
        monkeypatch, tmp_path, captured):
    """Response body/status and the safe error-event behaviour are unchanged for
    every non-initialized-store case the probes do not touch."""
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "absent.sqlite"))
    r = _new_client().get(HEALTH_PATH)
    assert r.status_code == 200
    assert json.loads(r.get_data(as_text=True)) == UNINITIALIZED_BODY
    monkeypatch.undo()

    bad = tmp_path / "corrupt2.sqlite"
    bad.write_bytes(b"not a sqlite database" * 50)
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(bad))
    r = _new_client().get(HEALTH_PATH)
    assert r.status_code == 503
    assert json.loads(r.get_data(as_text=True)) == ERROR_BODY
    monkeypatch.undo()

    # An initialized store whose probe raises: generic 503, and the operational
    # event carries the exception CLASS only — never a message, path or row.
    _init_db()
    captured.clear()

    def _boom(self):
        raise sqlite3.DatabaseError("probe failed with a secret path /tmp/x")
    monkeypatch.setattr(type(webapp._get_account_store()), "ping", _boom)
    r = _new_client().get(HEALTH_PATH)
    assert r.status_code == 503
    assert json.loads(r.get_data(as_text=True)) == ERROR_BODY
    events = [json.loads(line) for line in captured]
    failures = [e for e in events if e.get("event") == "health.db_probe_failed"]
    assert failures, captured
    for event in failures:
        assert event.get("error_class") == "DatabaseError"
        assert "secret" not in json.dumps(event)
        assert "/tmp/x" not in json.dumps(event)


def test_perf01_health_security_and_cache_headers_unchanged():
    """Header/caching semantics of the health surface are untouched by the
    probe change."""
    _init_db()
    baseline = _new_client().get(HEALTH_PATH)
    _record_store_with(4)
    after = _new_client().get(HEALTH_PATH)
    assert after.status_code == baseline.status_code
    assert after.get_data() == baseline.get_data()
    assert after.mimetype == "application/json"
    for header in ("Cache-Control", "Set-Cookie"):
        assert after.headers.get(header) == baseline.headers.get(header)
