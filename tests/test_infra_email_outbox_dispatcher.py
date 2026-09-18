"""OD-INFRA-6 — durable email outbox + ONE bounded in-process dispatcher.

File: tests/test_infra_email_outbox_dispatcher.py
Purpose: pin the architecture decision that resolves the anonymous timing
oracle - the request RECORDS the message and returns; delivery happens later on
one dispatcher thread - and pin every boundary the decision drew: no queue
library, one thread, thread-confined connections, bounded retry, delivered rows
deleted, exhausted rows scrubbed, nothing logged, production boots without a
provider and starts no loop, dev/test stay deterministic.

Input contract: `engine/account_store.py` (outbox methods), `engine/email_dispatcher.py`,
`web/app.py` (`_EMAIL_DISPATCHER`, `_EMAIL_INLINE_DISPATCH`, `_open_dispatcher_store`).
Prohibited: real network; real provider; background nondeterminism in these tests
(every thread started here is stopped here).
"""
import logging
import os
import re
import statistics
import subprocess
import sys
import threading
import time

import pytest

import web.app as webapp
from engine.account_store import (
    OUTBOX_FAILED,
    OUTBOX_PENDING,
    SqliteAccountStore,
)
from engine.email_dispatcher import (
    DEFERRED,
    DELIVERED,
    EXHAUSTED,
    EmailDispatcher,
    RETRY_LATER,
    SKIPPED,
)
from engine.email_sender import (
    DevMemoryEmailSender,
    EmailDeliveryFailed,
    EmailSender,
    UnconfiguredEmailSender,
)
from tests.csrf_client import csrf_client

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASSWORD = "Str0ng-Passw0rd-Example"


@pytest.fixture
def client():
    webapp.app.config["TESTING"] = True
    with csrf_client(webapp.app) as c:
        yield c


class _ScriptedSender(EmailSender):
    """A configured provider stand-in with scripted latency/outcome. Records
    every call; never opens a socket."""
    can_deliver = True

    def __init__(self, latency=0.0, fail=False, accept=True):
        self.latency, self.fail, self.accept = latency, fail, accept
        self.calls = []

    def send(self, to, subject, body):
        self.calls.append({"to": to, "subject": subject, "body": body})
        if self.latency:
            time.sleep(self.latency)
        if self.fail:
            raise EmailDeliveryFailed("provider_rejected")
        return self.accept


def _store():
    return webapp._get_account_store()


def _register(client, email):
    return client.post("/register", data={"email": email, "password": PASSWORD,
                                          "password_confirm": PASSWORD})


# =============================================================================
# The outbox (store layer)
# =============================================================================

def test_outbox_lives_in_the_canonical_database_not_a_second_datastore():
    store = _store()
    tables = {r[0] for r in store._conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    assert "email_outbox" in tables
    assert "accounts" in tables and "email_tokens" in tables   # same file
    assert store._path == webapp._resolve_db_path()


def test_token_and_outbox_message_are_created_atomically(monkeypatch):
    """Either both exist or neither: a token can never be issued whose message
    was lost. Proven by making the outbox insert fail inside the transaction."""
    store = _store()
    store.create_account("acc-1", "atomic@example.com", "h", "2026-01-01T00:00:00.000000Z")
    tokens_before = store._conn.execute("SELECT COUNT(*) FROM email_tokens").fetchone()[0]

    def boom(*args, **kwargs):
        raise RuntimeError("outbox insert refused")
    monkeypatch.setattr(store, "_outbox_insert", boom)
    with pytest.raises(RuntimeError):
        store.create_email_token_and_enqueue(
            "tok-1", "acc-1", "verification", "hash-1", "2026-01-02T00:00:00.000000Z",
            "2026-01-01T00:00:00.000000Z", "msg-1", "atomic@example.com", "s", "b")
    tokens_after = store._conn.execute("SELECT COUNT(*) FROM email_tokens").fetchone()[0]
    assert tokens_after == tokens_before                 # rolled back together
    assert store.count_outbox() == 0


def test_delivered_rows_are_deleted_and_exhausted_rows_are_scrubbed():
    store = _store()
    store.enqueue_email("m-ok", "verification", "a@example.com", "s",
                        "link RAW-TOKEN-A", "2026-01-01T00:00:00.000000Z")
    store.enqueue_email("m-bad", "reset", "b@example.com", "s",
                        "link RAW-TOKEN-B", "2026-01-01T00:00:00.000000Z")
    assert store.mark_email_delivered("m-ok") == 1
    assert store.get_outbox_message("m-ok") is None      # gone, not archived
    for _ in range(3):
        status = store.mark_email_attempt_failed("m-bad", "2026-01-01T00:01:00.000000Z", 3)
    assert status == OUTBOX_FAILED
    row = store.get_outbox_message("m-bad")
    assert row["status"] == OUTBOX_FAILED and row["attempt_count"] == 3
    assert row["recipient"] is None and row["subject"] is None and row["body"] is None
    flat = " ".join(str(v) for v in store._conn.execute(
        "SELECT * FROM email_outbox").fetchall()[0])
    assert "RAW-TOKEN" not in flat and "example.com" not in flat


def test_outbox_counts_never_return_contents():
    store = _store()
    store.enqueue_email("m-1", "verification", "a@example.com", "s", "RAW", "2026-01-01T00:00:00.000000Z")
    assert store.count_outbox() == 1
    assert store.count_outbox(OUTBOX_PENDING) == 1
    assert store.count_outbox(OUTBOX_FAILED) == 0


# =============================================================================
# The dispatcher
# =============================================================================

def _dispatcher(sender, **kwargs):
    options = {"open_store": webapp._open_dispatcher_store,
               "resolve_sender": lambda: sender}
    options.update(kwargs)
    return EmailDispatcher(**options)


def test_dispatch_pending_delivers_and_deletes(client):
    monkeypatch_inline = webapp._EMAIL_INLINE_DISPATCH
    assert monkeypatch_inline is True                    # dev/test default
    sink = DevMemoryEmailSender()
    d = _dispatcher(sink)
    _store().enqueue_email("m-1", "verification", "x@example.com", "Verify",
                           "link RAW", "2026-01-01T00:00:00.000000Z")
    counts = d.dispatch_pending()
    assert counts[DELIVERED] == 1
    assert sink.last_for("x@example.com")["body"] == "link RAW"
    assert _store().count_outbox() == 0


def test_dispatch_fails_closed_with_no_capable_sender():
    """Production without a configured provider: nothing is sent, nothing is
    mutated, messages simply wait."""
    _store().enqueue_email("m-1", "verification", "x@example.com", "s", "RAW",
                           "2026-01-01T00:00:00.000000Z")
    d = _dispatcher(UnconfiguredEmailSender())
    assert d.dispatch_pending()[SKIPPED] == 1
    assert d.dispatch_one("m-1") == SKIPPED
    assert _store().get_outbox_message("m-1")["attempt_count"] == 0


def test_bounded_retry_then_exhaustion_with_scrub():
    sender = _ScriptedSender(fail=True)
    d = _dispatcher(sender, max_attempts=3)
    _store().enqueue_email("m-1", "reset", "x@example.com", "s", "RAW-TOKEN",
                           "2026-01-01T00:00:00.000000Z")
    assert d.dispatch_one("m-1") == RETRY_LATER
    assert d.dispatch_one("m-1") == RETRY_LATER
    assert d.dispatch_one("m-1") == EXHAUSTED
    assert d.dispatch_one("m-1") == SKIPPED              # no longer pending
    row = _store().get_outbox_message("m-1")
    assert row["status"] == OUTBOX_FAILED and row["body"] is None
    assert len(sender.calls) == 3                        # exactly the budget


def test_backoff_defers_a_recently_failed_message():
    import datetime
    sender = _ScriptedSender(fail=True)
    d = _dispatcher(sender, max_attempts=5, base_backoff_seconds=60.0)
    _store().enqueue_email("m-1", "reset", "x@example.com", "s", "RAW",
                           "2026-01-01T00:00:00.000000Z")
    assert d.dispatch_pending()[RETRY_LATER] == 1
    assert d.dispatch_pending()[DEFERRED] == 1            # too soon
    assert len(sender.calls) == 1
    later = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=61)
    assert d.dispatch_pending(now=later)[RETRY_LATER] == 1
    assert len(sender.calls) == 2
    assert d.backoff_seconds(0) == 0.0
    assert d.backoff_seconds(1) == 60.0 and d.backoff_seconds(2) == 120.0
    assert d.backoff_seconds(50) == d._max_backoff        # capped


def test_only_confirmed_acceptance_counts_as_delivered():
    """A sender returning anything but `True` is not a delivery."""
    for value in (None, 1, "ok", {}, False):
        sender = _ScriptedSender(accept=value)
        d = _dispatcher(sender, max_attempts=5)
        mid = "m-%r" % (value,)
        _store().enqueue_email(mid, "reset", "x@example.com", "s", "RAW",
                               "2026-01-01T00:00:00.000000Z")
        assert d.dispatch_one(mid) == RETRY_LATER, value
        assert _store().get_outbox_message(mid)["status"] == OUTBOX_PENDING


def test_a_provider_exception_never_escapes_the_dispatcher():
    class Explodes(EmailSender):
        can_deliver = True
        def send(self, to, subject, body):
            raise RuntimeError("socket on fire")
    d = _dispatcher(Explodes(), max_attempts=5)
    _store().enqueue_email("m-1", "reset", "x@example.com", "s", "RAW",
                           "2026-01-01T00:00:00.000000Z")
    assert d.dispatch_pending()[RETRY_LATER] == 1        # no raise


def test_dispatcher_policy_is_bounded():
    with pytest.raises(ValueError):
        _dispatcher(DevMemoryEmailSender(), poll_interval_seconds=0)
    with pytest.raises(ValueError):
        _dispatcher(DevMemoryEmailSender(), poll_interval_seconds=10_000)
    with pytest.raises(ValueError):
        _dispatcher(DevMemoryEmailSender(), max_attempts=0)
    with pytest.raises(ValueError):
        _dispatcher(DevMemoryEmailSender(), max_attempts=1000)
    d = _dispatcher(DevMemoryEmailSender(), batch_limit=10_000)
    assert d._batch_limit == 100


def test_nothing_is_logged_by_the_outbox_or_dispatcher(caplog):
    sender = _ScriptedSender(fail=True)
    d = _dispatcher(sender, max_attempts=2)
    with caplog.at_level(logging.DEBUG):
        _store().enqueue_email("m-1", "reset", "secret-recipient@example.com", "Reset",
                               "https://app.example.test/reset/RAW-TOKEN-XYZ",
                               "2026-01-01T00:00:00.000000Z")
        d.dispatch_one("m-1")
        d.dispatch_one("m-1")
    for forbidden in ("secret-recipient", "RAW-TOKEN-XYZ", "provider_rejected",
                      "Authorization"):
        assert forbidden not in caplog.text, forbidden
    for path in ("engine/email_dispatcher.py",):
        source = open(os.path.join(ROOT, path), encoding="utf-8").read()
        for forbidden in ("import logging", "logging.", "getLogger", "print("):
            assert forbidden not in source, (path, forbidden)


def test_no_queue_library_and_no_second_datastore():
    source = open(os.path.join(ROOT, "engine", "email_dispatcher.py"),
                  encoding="utf-8").read()
    for forbidden in ("redis", "celery", "rq", "kombu", "pika", "boto", "sqs",
                      "multiprocessing", "concurrent.futures", "asyncio"):
        assert re.search(r"\bimport %s\b|\bfrom %s\b" % (forbidden, forbidden),
                         source) is None, forbidden
    requirements = open(os.path.join(ROOT, "requirements.txt"), encoding="utf-8").read().lower()
    for forbidden in ("redis", "celery", "rq", "kombu", "pika"):
        assert forbidden not in requirements, forbidden


# =============================================================================
# ONE thread, thread-confined connections, process safety
# =============================================================================

def _dispatcher_threads():
    return [t for t in threading.enumerate() if t.name == "inventorai-email-dispatcher"]


def test_start_is_idempotent_and_creates_exactly_one_thread():
    d = _dispatcher(DevMemoryEmailSender(), poll_interval_seconds=0.05)
    before = len(_dispatcher_threads())
    try:
        assert d.start() is True
        assert d.start() is False                         # second call: nothing
        assert d.start() is False
        assert len(_dispatcher_threads()) == before + 1
        assert d.running and d.thread_name == "inventorai-email-dispatcher"
        assert d._thread is not threading.current_thread()
        assert d._thread.daemon is True
    finally:
        d.stop()
    assert not d.running
    assert len(_dispatcher_threads()) == before


def test_dispatcher_store_is_opened_and_closed_in_its_own_thread():
    """Each SQLite connection is thread-confined by construction: the store the
    loop uses is created in the loop's thread, and it is never the request
    store."""
    seen = {}
    request_store = _store()

    def open_store():
        seen["ident"] = threading.get_ident()
        store = webapp._open_dispatcher_store()
        seen["store"] = store
        return store

    d = EmailDispatcher(open_store=open_store,
                        resolve_sender=lambda: DevMemoryEmailSender(),
                        poll_interval_seconds=0.05)
    try:
        d.start()
        deadline = time.time() + 5
        while "store" not in seen and time.time() < deadline:
            time.sleep(0.01)
        assert seen["ident"] == d._thread.ident
        assert seen["ident"] != threading.get_ident()
        assert seen["store"] is not request_store
    finally:
        d.stop()


def test_inline_dispatch_uses_a_temporary_store_in_the_calling_thread():
    opened = []
    real = webapp._open_dispatcher_store

    def spy():
        store = real()
        opened.append(store)
        return store
    d = EmailDispatcher(open_store=spy, resolve_sender=lambda: DevMemoryEmailSender())
    _store().enqueue_email("m-1", "reset", "x@example.com", "s", "RAW",
                           "2026-01-01T00:00:00.000000Z")
    d.dispatch_pending()
    assert len(opened) == 1 and opened[0] is not _store()
    # Closed after the call: a further use of that connection is refused.
    with pytest.raises(Exception):
        opened[0]._conn.execute("SELECT 1")


def test_loop_survives_a_store_fault_and_keeps_its_pace():
    calls = {"n": 0}

    def flaky_open():
        calls["n"] += 1
        if calls["n"] <= 2:
            raise RuntimeError("database unavailable")
        return webapp._open_dispatcher_store()
    d = EmailDispatcher(open_store=flaky_open,
                        resolve_sender=lambda: DevMemoryEmailSender(),
                        poll_interval_seconds=0.05)
    try:
        d.start()
        deadline = time.time() + 5
        while d.cycles < 2 and time.time() < deadline:
            time.sleep(0.02)
        assert d.running
        assert d.loop_faults >= 1
        assert d.cycles >= 2
    finally:
        d.stop()


def test_gunicorn_stays_one_worker_one_thread():
    conf = open(os.path.join(ROOT, "gunicorn.conf.py"), encoding="utf-8").read()
    assert re.search(r"^workers\s*=\s*1\s*$", conf, re.M)
    assert re.search(r"^threads\s*=\s*1\s*$", conf, re.M)


def test_the_request_path_never_reuses_the_dispatcher_store():
    assert webapp._open_dispatcher_store() is not webapp._get_account_store()
    assert webapp._open_dispatcher_store() is not webapp._open_dispatcher_store()


# =============================================================================
# Startup / shutdown semantics
# =============================================================================

def _cold_boot(extra_env, program):
    env = dict(os.environ)
    env.update({"INVENTORAI_ENV": "production",
                "INVENTORAI_SECRET_KEY": "boot-probe-not-a-real-secret",
                "PYTHONWARNINGS": "ignore"})
    env.update(extra_env)
    return subprocess.run([sys.executable, "-c", program], cwd=ROOT, env=env,
                          capture_output=True, text=True, timeout=180)


def test_production_boots_without_email_config_and_starts_no_loop(tmp_path):
    result = _cold_boot(
        {"INVENTORAI_DB_PATH": str(tmp_path / "boot.sqlite")},
        "import threading, web.app as w;"
        "assert w._EMAIL_DISPATCHER_STARTED is False;"
        "assert not w._EMAIL_DISPATCHER.running;"
        "assert w._EMAIL_INLINE_DISPATCH is False;"
        "assert not [t for t in threading.enumerate() if 'dispatcher' in t.name];"
        "print(w.app.test_client().get('/health').status_code)")
    assert result.returncode == 0, result.stderr[-2000:]
    assert result.stdout.strip() == "200"


def test_production_with_provider_starts_exactly_one_dispatcher_thread(tmp_path):
    result = _cold_boot(
        {"INVENTORAI_DB_PATH": str(tmp_path / "boot.sqlite"),
         "INVENTORAI_EMAIL_PROVIDER": "resend",
         "INVENTORAI_RESEND_API_KEY": "probe-key-not-real",
         "INVENTORAI_EMAIL_FROM": "InventorAI <no-reply@example.test>",
         "INVENTORAI_PUBLIC_BASE_URL": "https://app.example.test"},
        "import threading, web.app as w;"
        "assert w._EMAIL_DISPATCHER_STARTED is True;"
        "assert w._EMAIL_DISPATCHER.running;"
        "assert w._EMAIL_INLINE_DISPATCH is False;"
        "names=[t.name for t in threading.enumerate() if t.name=='inventorai-email-dispatcher'];"
        "assert names==['inventorai-email-dispatcher'], names;"
        "assert w._start_email_dispatcher_if_production() is False;"   # idempotent
        "print(w.app.test_client().get('/health').status_code)")
    assert result.returncode == 0, result.stderr[-2000:]
    assert result.stdout.strip() == "200"


def test_dev_and_test_runtime_dispatches_inline_and_starts_no_thread():
    assert webapp._EMAIL_INLINE_DISPATCH is True
    assert webapp._EMAIL_DISPATCHER_STARTED is False
    assert not webapp._EMAIL_DISPATCHER.running
    assert isinstance(webapp._EMAIL_SENDER, DevMemoryEmailSender)


def test_dev_memory_sender_behaviour_is_preserved_end_to_end(client):
    """The repository-wide seam: the sink holds the message the moment the
    response returns, exactly as before the outbox existed."""
    sink = DevMemoryEmailSender()
    webapp._EMAIL_SENDER = sink
    try:
        assert _register(client, "sink-seam@example.com").status_code == 200
        message = sink.last_for("sink-seam@example.com")
        assert message and "/verify/" in message["body"]
        assert _store().count_outbox() == 0             # delivered -> deleted
    finally:
        webapp._EMAIL_SENDER = DevMemoryEmailSender()


# =============================================================================
# THE TIMING ORACLE - adversarial, with simulated provider latency
# =============================================================================

LATENCY = 0.5          # simulated provider round trip, seconds
SAMPLES = 5


def _median_ms(client, path, data_for):
    samples = []
    for i in range(SAMPLES):
        started = time.perf_counter()
        client.post(path, data=data_for(i))
        samples.append((time.perf_counter() - started) * 1000)
    return statistics.median(samples)


def test_anonymous_requests_perform_no_provider_call_and_show_no_branch_latency(
        client, monkeypatch):
    """The defect: with inline delivery the provider round trip happened only on
    the account-eligible branch, so /recover answered in ~205 ms for a known
    address and ~2 ms for an unknown one (200 ms simulated provider). With the
    outbox the request never contacts the provider: every branch returns well
    before the provider delay could appear in it, and the branches differ by
    far less than that delay. Then the deferred dispatch proves the calls were
    only postponed, not skipped - exactly the eligible messages go out."""
    monkeypatch.setattr(webapp, "_EMAIL_INLINE_DISPATCH", False)   # production shape
    sender = _ScriptedSender(latency=LATENCY)
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", sender)

    # Seed: a known active account and a disabled one (via the sink, no latency).
    seed = DevMemoryEmailSender()
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", seed)
    monkeypatch.setattr(webapp, "_EMAIL_INLINE_DISPATCH", True)
    _register(client, "known-active@example.com")
    _register(client, "known-disabled@example.com")
    store = _store()
    disabled = store.get_account_by_normalized_email("known-disabled@example.com")
    store.set_status(disabled["account_id"], "disabled", "2026-01-01T00:00:00.000000Z")
    monkeypatch.setattr(webapp, "_EMAIL_INLINE_DISPATCH", False)
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", sender)
    assert sender.calls == []

    timings = {
        "register/new": _median_ms(client, "/register", lambda i: {
            "email": "timing-new-%d@example.com" % i, "password": PASSWORD,
            "password_confirm": PASSWORD}),
        "register/existing": _median_ms(client, "/register", lambda i: {
            "email": "known-active@example.com", "password": PASSWORD,
            "password_confirm": PASSWORD}),
        "recover/unknown": _median_ms(client, "/recover", lambda i: {
            "email": "never-seen-%d@example.com" % i}),
        "recover/known-active": _median_ms(client, "/recover", lambda i: {
            "email": "known-active@example.com"}),
        "recover/disabled": _median_ms(client, "/recover", lambda i: {
            "email": "known-disabled@example.com"}),
    }
    # 1. No provider call happened inside ANY anonymous request.
    assert sender.calls == [], "the request path contacted the provider"
    # 2. Every branch returns before the provider delay could dominate it.
    for name, ms in timings.items():
        assert ms < LATENCY * 1000 * 0.5, (name, ms, timings)
    # 3. No material provider-latency-correlated branch difference.
    tolerance = LATENCY * 1000 * 0.25
    recover = [timings[k] for k in timings if k.startswith("recover/")]
    assert max(recover) - min(recover) < tolerance, timings
    assert abs(timings["register/new"] - timings["register/existing"]) < tolerance, timings

    # 4. The calls were deferred, not dropped: exactly the eligible messages.
    counts = webapp._EMAIL_DISPATCHER.dispatch_pending()
    assert counts[DELIVERED] == SAMPLES + SAMPLES        # new registrations + known-active recoveries
    recipients = sorted(c["to"] for c in sender.calls)
    assert recipients.count("known-active@example.com") == SAMPLES
    assert "known-disabled@example.com" not in recipients
    assert not any(r.startswith("never-seen") for r in recipients)
    assert _store().count_outbox() == 0


def test_provider_slowness_or_failure_cannot_reach_the_request(client, monkeypatch):
    monkeypatch.setattr(webapp, "_EMAIL_INLINE_DISPATCH", False)
    seed = DevMemoryEmailSender()
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", seed)
    monkeypatch.setattr(webapp, "_EMAIL_INLINE_DISPATCH", True)
    _register(client, "outage-known@example.com")
    monkeypatch.setattr(webapp, "_EMAIL_INLINE_DISPATCH", False)

    failing_slow = _ScriptedSender(latency=LATENCY, fail=True)
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", failing_slow)
    known = _median_ms(client, "/recover", lambda i: {"email": "outage-known@example.com"})
    unknown = _median_ms(client, "/recover", lambda i: {"email": "nobody-%d@example.com" % i})
    assert failing_slow.calls == []
    assert known < LATENCY * 1000 * 0.5 and unknown < LATENCY * 1000 * 0.5
    assert abs(known - unknown) < LATENCY * 1000 * 0.25
    # Deferred delivery then fails, bounded, and claims nothing.
    counts = webapp._EMAIL_DISPATCHER.dispatch_pending()
    assert counts[RETRY_LATER] == SAMPLES and counts[DELIVERED] == 0
    assert _store().count_outbox(OUTBOX_PENDING) == SAMPLES


def test_anonymous_response_bodies_remain_identical_under_the_outbox(client, monkeypatch):
    monkeypatch.setattr(webapp, "_EMAIL_INLINE_DISPATCH", False)
    monkeypatch.setattr(webapp, "_EMAIL_SENDER", _ScriptedSender())
    seed_ok = client.post("/register", data={"email": "same-body@example.com",
                                             "password": PASSWORD,
                                             "password_confirm": PASSWORD}).get_data()
    dup = client.post("/register", data={"email": "same-body@example.com",
                                         "password": PASSWORD,
                                         "password_confirm": PASSWORD}).get_data()
    assert seed_ok == dup
    known = client.post("/recover", data={"email": "same-body@example.com"}).get_data()
    unknown = client.post("/recover", data={"email": "no-such@example.com"}).get_data()
    assert known == unknown
    assert b"has been sent" not in known and b"queued for delivery" in known
