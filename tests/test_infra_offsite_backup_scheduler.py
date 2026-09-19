"""OD-INFRA-5 — ONE bounded in-process daily off-provider backup scheduler.

File: tests/test_infra_offsite_backup_scheduler.py
Purpose: pin the architecture decision that the daily off-provider backup runs
from inside the one production web-service process (the only place the
persistent disk is mounted), and pin every boundary that keeps it bounded:
one thread, idempotent start, `Event.wait` pacing, eligibility decided from
PERSISTED state so restarts/redeploys never duplicate a backup, hours-scale
retry after failure, the existing backup engine and transport composed and
never re-implemented, create-only uploads, temporary artifacts removed in
every outcome, the live database never written, nothing logged that could
carry a credential, no remote delete/retention, production boots without
configuration and starts no thread, dev/test never start a thread.

Input contract: `engine/offsite_backup_scheduler.py`, the `offsite_backup_state`
methods of `engine/account_store.py`, and the `web/app.py` lifecycle wiring
(`_OFFSITE_BACKUP_SCHEDULER`, `_open_offsite_backup_store`,
`_start_offsite_backup_scheduler_if_production`).
Prohibited: real network; real provider; a real R2 upload; background
nondeterminism (every thread started here is stopped here).
"""
import datetime
import hashlib
import io
import logging
import os
import re
import sqlite3
import subprocess
import sys
import threading
import time

import pytest

import web.app as webapp
from engine.account_store import SqliteAccountStore
from engine.backup_service import validate_sqlite_database
from engine.offsite_backup_scheduler import (
    DEFAULT_FAILURE_RETRY_SECONDS,
    DEFAULT_INTERVAL_SECONDS,
    DEFAULT_POLL_INTERVAL_SECONDS,
    EVENT_FAILURE,
    EVENT_SUCCESS,
    FAILURE,
    NOT_DUE,
    EVENT_STALE,
    OffsiteBackupScheduler,
    SCHEDULE_NAME,
    SKIPPED,
    STALE,
    SUCCESS,
    THREAD_NAME,
    configuration_complete,
    live_instance,
    new_claim_id,
    perform_offsite_backup,
    resolve_settings,
)
from engine.r2_object_upload import R2UploadError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEDULER_SOURCE = os.path.join(ROOT, "engine", "offsite_backup_scheduler.py")

# Test-only values. Not credentials: nothing here reaches any provider.
SETTINGS = {"INVENTORAI_R2_ACCOUNT_ID": "testaccount",
            "INVENTORAI_R2_BUCKET": "inventorai-backups-test",
            "INVENTORAI_R2_ACCESS_KEY_ID": "TESTONLYACCESSKEYID",
            "INVENTORAI_R2_SECRET_ACCESS_KEY": "test-only-secret-not-a-real-key",
            "INVENTORAI_R2_PREFIX": "daily"}

T0 = datetime.datetime(2026, 9, 20, 3, 0, 0, tzinfo=datetime.timezone.utc)
HOUR = datetime.timedelta(hours=1)
DAY = datetime.timedelta(days=1)


class _RecordingTransport:
    """A local stand-in for R2: records every signed request, answers a
    scripted status (optionally per call), never opens a socket."""

    def __init__(self, status=200, statuses=None, raises=None):
        self.status, self.statuses, self.raises = status, list(statuses or []), raises
        self.calls = []

    def __call__(self, url, headers, path, size, timeout_seconds):
        with open(path, "rb") as handle:
            body = handle.read()
        self.calls.append({"url": url, "headers": dict(headers), "path": path,
                           "size": size, "timeout": timeout_seconds,
                           "body_sha256": hashlib.sha256(body).hexdigest(),
                           "body_bytes": len(body), "body": body,
                           "thread": threading.get_ident()})
        if self.raises is not None:
            raise self.raises
        return (self.statuses.pop(0) if self.statuses else self.status), b"<ok/>"


class _Clock:
    def __init__(self, moment=T0):
        self.moment = moment

    def __call__(self):
        return self.moment

    def advance(self, delta):
        self.moment = self.moment + delta


class _Emitted:
    def __init__(self):
        self.events = []

    def __call__(self, event, level="info", **fields):
        self.events.append({"event": event, "level": level, "fields": dict(fields)})


@pytest.fixture
def live_database(tmp_path):
    """A small real SQLite database standing in for the serving database,
    holding the account-store schema plus recognisable content."""
    path = str(tmp_path / "live.sqlite")
    SqliteAccountStore(path).close()
    with sqlite3.connect(path) as connection:
        connection.execute("CREATE TABLE records (id TEXT, payload TEXT)")
        connection.execute("INSERT INTO records VALUES ('r1', 'invention text')")
    return path


def _scheduler(live_database, transport=None, clock=None, emit=None,
               settings=SETTINGS, **kwargs):
    options = {"open_store": lambda: SqliteAccountStore(live_database),
               "source_path": live_database,
               "resolve_settings": lambda: dict(settings),
               "transport": transport or _RecordingTransport(),
               "clock": clock or _Clock(), "emit": emit}
    options.update(kwargs)
    return OffsiteBackupScheduler(**options)


def _state(live_database):
    store = SqliteAccountStore(live_database)
    try:
        return store.get_offsite_backup_state(SCHEDULE_NAME)
    finally:
        store.close()


def _snapshot(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest(), os.stat(path).st_mtime


# =============================================================================
# The shared pipeline (used by the CLI and the scheduler alike)
# =============================================================================

def test_pipeline_runs_the_existing_engine_then_uploads_then_cleans_up(
        live_database, tmp_path):
    transport = _RecordingTransport()
    before = sorted(os.listdir(tmp_path))
    report = perform_offsite_backup(live_database, SETTINGS, transport=transport,
                                    now=T0)
    assert report["upload"]["accepted"] is True
    assert report["upload"]["create_only"] is True
    assert report["key"] == "daily/inventorai-20260920T030000Z.sqlite"
    call = transport.calls[0]
    assert call["url"].endswith("/" + report["key"])
    assert call["headers"]["if-none-match"] == "*"
    assert call["body"].startswith(b"SQLite format 3\x00")
    assert call["body_sha256"] == report["upload"]["sha256"]
    assert call["body_bytes"] == report["upload"]["bytes"]
    # The artifact was produced by the existing service (validated, inventory
    # matched) and the temporary workspace is gone.
    assert report["backup"]["quick_check"] == "ok"
    assert "records" in report["backup"]["tables"]
    assert not os.path.exists(call["path"])
    assert not os.path.isdir(os.path.dirname(call["path"]))
    assert sorted(os.listdir(tmp_path)) == before


def test_pipeline_removes_the_temporary_artifact_when_the_upload_fails(
        live_database):
    transport = _RecordingTransport(status=500)
    with pytest.raises(R2UploadError):
        perform_offsite_backup(live_database, SETTINGS, transport=transport)
    assert not os.path.exists(transport.calls[0]["path"])
    assert not os.path.isdir(os.path.dirname(transport.calls[0]["path"]))


def test_pipeline_removes_the_temporary_artifact_when_the_backup_fails(tmp_path):
    corrupt = tmp_path / "corrupt.sqlite"
    corrupt.write_bytes(b"this is definitely not a sqlite database")
    transport = _RecordingTransport()
    from engine.backup_service import BackupError
    with pytest.raises(BackupError):
        perform_offsite_backup(str(corrupt), SETTINGS, transport=transport)
    assert transport.calls == []
    leftovers = [name for name in os.listdir(tmp_path)
                 if name.startswith("inventorai-offsite-")]
    assert leftovers == []


def test_settings_resolve_from_the_environment_and_fail_closed_by_name():
    assert resolve_settings(dict(SETTINGS))["INVENTORAI_R2_PREFIX"] == "daily"
    assert configuration_complete(dict(SETTINGS)) is True
    for name in ("INVENTORAI_R2_ACCOUNT_ID", "INVENTORAI_R2_BUCKET",
                 "INVENTORAI_R2_ACCESS_KEY_ID", "INVENTORAI_R2_SECRET_ACCESS_KEY"):
        partial = dict(SETTINGS)
        partial[name] = "   "
        assert configuration_complete(partial) is False
        with pytest.raises(R2UploadError) as raised:
            resolve_settings(partial)
        assert raised.value.reason_code == "missing_configuration"
        assert name in str(raised.value)
        assert SETTINGS[name] not in str(raised.value)
    assert configuration_complete({}) is False


# =============================================================================
# Scheduling semantics (driven synchronously through the seam)
# =============================================================================

def test_first_eligible_check_performs_exactly_one_backup(live_database):
    transport, clock, emitted = _RecordingTransport(), _Clock(), _Emitted()
    s = _scheduler(live_database, transport, clock, emitted)
    assert _state(live_database) is None                 # never attempted
    assert s.run_if_due() == SUCCESS
    assert len(transport.calls) == 1
    state = _state(live_database)
    assert state["last_success_at"] == "2026-09-20T03:00:00.000000Z"
    assert state["last_attempt_at"] == state["last_success_at"]
    assert state["last_success_object_key"] == "daily/inventorai-20260920T030000Z.sqlite"
    assert state["last_success_bytes"] == transport.calls[0]["body_bytes"]
    assert state["last_success_sha256"] == transport.calls[0]["body_sha256"]
    assert state["consecutive_failures"] == 0
    assert state["last_failure_at"] is None and state["last_failure_code"] is None


def test_an_immediate_second_check_does_not_duplicate_the_backup(live_database):
    transport, clock = _RecordingTransport(), _Clock()
    s = _scheduler(live_database, transport, clock)
    assert s.run_if_due() == SUCCESS
    assert s.run_if_due() == NOT_DUE
    clock.advance(5 * HOUR)
    assert s.run_if_due() == NOT_DUE
    clock.advance(DAY - 6 * HOUR)                         # 23h after success
    assert s.run_if_due() == NOT_DUE
    assert len(transport.calls) == 1


def test_a_restart_with_a_persisted_recent_success_does_not_re_backup(live_database):
    """The state lives in the database, not in the scheduler object: a brand
    new scheduler (a restarted process) reads the same row and stays quiet."""
    transport, clock = _RecordingTransport(), _Clock()
    assert _scheduler(live_database, transport, clock).run_if_due() == SUCCESS
    for _restart in range(5):
        clock.advance(datetime.timedelta(minutes=1))
        fresh = _scheduler(live_database, transport, clock)   # new object, same DB
        assert fresh.run_if_due() == NOT_DUE
    assert len(transport.calls) == 1


def test_elapsed_interval_makes_the_schedule_eligible_again(live_database):
    transport, clock = _RecordingTransport(), _Clock()
    s = _scheduler(live_database, transport, clock)
    assert s.run_if_due() == SUCCESS
    clock.advance(DAY)
    assert s.run_if_due() == SUCCESS
    assert s.run_if_due() == NOT_DUE
    assert len(transport.calls) == 2
    keys = [c["url"].rsplit("/", 1)[1] for c in transport.calls]
    assert keys == ["inventorai-20260920T030000Z.sqlite",
                    "inventorai-20260921T030000Z.sqlite"]   # unique per run


def test_resumes_safely_after_long_downtime(live_database):
    """Downtime longer than one interval yields ONE catch-up backup, not one
    per missed day."""
    transport, clock = _RecordingTransport(), _Clock()
    s = _scheduler(live_database, transport, clock)
    assert s.run_if_due() == SUCCESS
    clock.advance(9 * DAY)
    assert s.run_if_due() == SUCCESS
    assert s.run_if_due() == NOT_DUE
    assert len(transport.calls) == 2


def test_eligibility_is_decided_from_persisted_state_not_memory(live_database):
    """A scheduler that has never run in THIS process still defers to the row
    another process wrote - the exact restart/redeploy case."""
    store = SqliteAccountStore(live_database)
    try:
        claim = new_claim_id()
        assert store.claim_offsite_backup_run(
            SCHEDULE_NAME, claim, "2026-09-20T02:30:00.000000Z", "9", "9") is True
        assert store.record_offsite_backup_success(
            SCHEDULE_NAME, claim, "2026-09-20T02:30:00.000000Z",
            "daily/x.sqlite", 1, "0" * 64) is True
    finally:
        store.close()
    transport = _RecordingTransport()
    s = _scheduler(live_database, transport, _Clock(T0))      # 30 min later
    assert s.run_if_due() == NOT_DUE
    assert transport.calls == []


def test_the_claim_is_atomic_so_overlapping_processes_cannot_both_run(live_database):
    """Two schedulers (two briefly overlapping processes during a redeploy)
    both see the run as due; exactly ONE wins the atomic claim and uploads."""
    first_t, second_t = _RecordingTransport(), _RecordingTransport()
    clock = _Clock()
    a = _scheduler(live_database, first_t, clock)
    b = _scheduler(live_database, second_t, clock)
    store_a, store_b = SqliteAccountStore(live_database), SqliteAccountStore(live_database)
    try:
        assert a.due(store_a.get_offsite_backup_state(SCHEDULE_NAME), clock()) is True
        assert b.due(store_b.get_offsite_backup_state(SCHEDULE_NAME), clock()) is True
        # Both computed "due"; the claims are serialised by BEGIN IMMEDIATE.
        now = "2026-09-20T03:00:00.000000Z"
        threshold = "2026-09-19T21:00:00.000000Z"
        assert store_a.claim_offsite_backup_run(SCHEDULE_NAME, "claim-a", now, threshold, threshold) is True
        assert store_b.claim_offsite_backup_run(SCHEDULE_NAME, "claim-b", now, threshold, threshold) is False
        assert store_a.get_offsite_backup_state(SCHEDULE_NAME)["active_claim_id"] == "claim-a"
    finally:
        store_a.close(); store_b.close()
    # Through the full seam, in sequence: the loser sees NOT_DUE.
    assert a.run_if_due() == NOT_DUE      # the claim above already holds the slot
    clock.advance(6 * HOUR)
    assert a.run_if_due() == SUCCESS
    assert b.run_if_due() == NOT_DUE
    assert len(first_t.calls) == 1 and second_t.calls == []


def test_an_interrupted_run_waits_out_the_retry_interval(live_database):
    """The attempt is recorded BEFORE the upload. If the process dies during
    the upload, the next boot sees the attempt and does not immediately
    re-run; it waits the bounded failure-retry interval."""
    class _Dies(Exception):
        pass
    transport = _RecordingTransport(raises=_Dies("killed mid-upload"))
    clock = _Clock()
    s = _scheduler(live_database, transport, clock)
    # A transport that dies mid-upload surfaces as the uploader's bounded
    # `provider_unreachable` (the cause chain is severed there on purpose),
    # recorded as a failure by the scheduler - it never propagates.
    assert s.run_if_due() == FAILURE
    state = _state(live_database)
    assert state["last_attempt_at"] == "2026-09-20T03:00:00.000000Z"
    assert state["last_success_at"] is None
    assert state["last_failure_code"] == "provider_unreachable"
    restarted = _scheduler(live_database, _RecordingTransport(), clock)
    assert restarted.run_if_due() == NOT_DUE
    clock.advance(datetime.timedelta(seconds=DEFAULT_FAILURE_RETRY_SECONDS))
    assert restarted.run_if_due() == SUCCESS


# =============================================================================
# Failure behaviour: bounded, never crashing, never mutating, never claiming
# =============================================================================

def test_provider_failure_is_recorded_and_retried_after_hours_not_seconds(
        live_database):
    transport = _RecordingTransport(statuses=[503, 503, 200])
    clock, emitted = _Clock(), _Emitted()
    s = _scheduler(live_database, transport, clock, emitted)
    assert s.run_if_due() == FAILURE
    state = _state(live_database)
    assert state["last_success_at"] is None
    assert state["last_failure_at"] == "2026-09-20T03:00:00.000000Z"
    assert state["last_failure_code"] == "provider_rejected"
    assert state["consecutive_failures"] == 1
    # No tight loop: nothing for the next few hours, then ONE retry.
    for _ in range(50):
        assert s.run_if_due() == NOT_DUE
    clock.advance(HOUR)
    assert s.run_if_due() == NOT_DUE
    clock.advance(5 * HOUR)
    assert s.run_if_due() == FAILURE
    assert _state(live_database)["consecutive_failures"] == 2
    clock.advance(6 * HOUR)
    assert s.run_if_due() == SUCCESS
    state = _state(live_database)
    assert state["consecutive_failures"] == 0
    assert state["last_success_at"] == "2026-09-20T15:00:00.000000Z"
    assert state["last_failure_at"] == "2026-09-20T09:00:00.000000Z"  # history kept
    assert len(transport.calls) == 3
    assert [e["event"] for e in emitted.events] == [EVENT_FAILURE, EVENT_FAILURE,
                                                    EVENT_SUCCESS]


def test_at_most_a_handful_of_attempts_per_day_during_an_outage(live_database):
    transport, clock = _RecordingTransport(status=500), _Clock()
    s = _scheduler(live_database, transport, clock)
    for _minute in range(24 * 60):
        s.run_if_due()
        clock.advance(datetime.timedelta(minutes=1))
    assert len(transport.calls) == 24 * 3600 // int(DEFAULT_FAILURE_RETRY_SECONDS)
    assert len(transport.calls) <= 4


def test_failure_never_mutates_the_source_database(live_database):
    before = _snapshot(live_database)
    transport = _RecordingTransport(status=500)
    s = _scheduler(live_database, transport)
    assert s.run_if_due() == FAILURE
    # The scheduler's OWN state row lives in the scheduler-state store; here
    # the live database doubles as that store, so compare the user tables
    # rather than raw bytes.
    with sqlite3.connect(live_database) as connection:
        rows = connection.execute("SELECT * FROM records").fetchall()
    assert rows == [("r1", "invention text")]
    assert validate_sqlite_database(live_database)["quick_check"] == "ok"
    # And with a SEPARATE state database the live file is byte-identical.
    separate_state = live_database + ".state"
    s2 = OffsiteBackupScheduler(open_store=lambda: SqliteAccountStore(separate_state),
                                source_path=live_database,
                                resolve_settings=lambda: dict(SETTINGS),
                                transport=_RecordingTransport(status=500))
    before = _snapshot(live_database)
    assert s2.run_if_due() == FAILURE
    assert _snapshot(live_database) == before


def test_success_never_mutates_the_source_database_either(live_database):
    separate_state = live_database + ".state"
    s = OffsiteBackupScheduler(open_store=lambda: SqliteAccountStore(separate_state),
                               source_path=live_database,
                               resolve_settings=lambda: dict(SETTINGS),
                               transport=_RecordingTransport())
    before = _snapshot(live_database)
    assert s.run_if_due() == SUCCESS
    assert _snapshot(live_database) == before


def test_a_key_collision_is_a_failure_not_an_overwrite(live_database):
    """412 from the create-only PUT: nothing stored, nothing replaced, and the
    next eligible run composes a NEW key from a later timestamp."""
    transport = _RecordingTransport(statuses=[412, 200])
    clock = _Clock()
    s = _scheduler(live_database, transport, clock)
    assert s.run_if_due() == FAILURE
    assert _state(live_database)["last_failure_code"] == "object_already_exists"
    assert _state(live_database)["last_success_at"] is None
    clock.advance(6 * HOUR)
    assert s.run_if_due() == SUCCESS
    first, second = (c["url"].rsplit("/", 1)[1] for c in transport.calls)
    assert first != second
    assert all(c["headers"]["if-none-match"] == "*" for c in transport.calls)


def test_backup_engine_failure_is_a_bounded_failure_category(tmp_path):
    missing = str(tmp_path / "absent.sqlite")
    state_db = str(tmp_path / "state.sqlite")
    transport = _RecordingTransport()
    s = OffsiteBackupScheduler(open_store=lambda: SqliteAccountStore(state_db),
                               source_path=missing,
                               resolve_settings=lambda: dict(SETTINGS),
                               transport=transport)
    assert s.run_if_due() == FAILURE
    store = SqliteAccountStore(state_db)
    try:
        assert store.get_offsite_backup_state(SCHEDULE_NAME)["last_failure_code"] == "backup_error"
    finally:
        store.close()
    assert transport.calls == []
    assert not os.path.exists(missing)                    # never silently created


def test_incomplete_configuration_skips_and_records_nothing(live_database):
    transport = _RecordingTransport()
    s = OffsiteBackupScheduler(open_store=lambda: SqliteAccountStore(live_database),
                               source_path=live_database,
                               resolve_settings=lambda: resolve_settings(
                                   {"INVENTORAI_R2_BUCKET": "only-this"}),
                               transport=transport)
    assert s.run_if_due() == SKIPPED
    assert transport.calls == []
    assert _state(live_database) is None


def test_a_store_fault_during_a_check_never_escapes_the_loop(live_database):
    calls = {"n": 0}

    def flaky_open():
        calls["n"] += 1
        if calls["n"] <= 2:
            raise RuntimeError("database unavailable")
        return SqliteAccountStore(live_database)
    s = OffsiteBackupScheduler(open_store=flaky_open, source_path=live_database,
                               resolve_settings=lambda: dict(SETTINGS),
                               transport=_RecordingTransport(),
                               poll_interval_seconds=0.05)
    try:
        s.start()
        deadline = time.time() + 5
        while s.cycles < 2 and time.time() < deadline:
            time.sleep(0.02)
        assert s.running
        assert s.loop_faults >= 1
        assert s.cycles >= 2
    finally:
        s.stop()


def test_scheduler_policy_is_bounded():
    live = lambda: None  # noqa: E731
    base = {"open_store": live, "source_path": "x",
            "resolve_settings": lambda: dict(SETTINGS)}
    for bad in ({"poll_interval_seconds": 0}, {"poll_interval_seconds": 10_000},
                {"interval_seconds": 1}, {"interval_seconds": 10 ** 9},
                {"failure_retry_seconds": 1},
                {"failure_retry_seconds": DEFAULT_INTERVAL_SECONDS + 1}):
        with pytest.raises(ValueError):
            OffsiteBackupScheduler(**dict(base, **bad))
    with pytest.raises(ValueError):
        OffsiteBackupScheduler(open_store=None, source_path="x",
                               resolve_settings=lambda: {})
    assert DEFAULT_INTERVAL_SECONDS == 24 * 3600
    assert 3600 <= DEFAULT_FAILURE_RETRY_SECONDS <= 12 * 3600      # hours
    assert 60 <= DEFAULT_POLL_INTERVAL_SECONDS <= 3600


# =============================================================================
# ONE thread, idempotent start, no busy loop, thread-confined connections
# =============================================================================

def _scheduler_threads():
    return [t for t in threading.enumerate() if t.name == THREAD_NAME]


def test_start_is_idempotent_and_creates_exactly_one_thread(live_database):
    s = _scheduler(live_database, poll_interval_seconds=0.05)
    before = len(_scheduler_threads())
    try:
        assert s.start() is True
        assert s.start() is False
        assert s.start() is False
        assert len(_scheduler_threads()) == before + 1
        assert s.running and s.thread_name == THREAD_NAME
        assert s._thread is not threading.current_thread()
        assert s._thread.daemon is True
    finally:
        s.stop()
    assert not s.running
    assert len(_scheduler_threads()) == before


def test_the_loop_is_paced_by_a_bounded_wait_not_a_busy_loop(live_database):
    source = io.open(SCHEDULER_SOURCE, encoding="utf-8").read()
    assert "self._stop.wait(self._poll)" in source
    assert "time.sleep" not in source and "import time" not in source
    # Behavioural: over a short window the loop completes about
    # window / poll cycles, not thousands.
    s = _scheduler(live_database, poll_interval_seconds=0.05)
    try:
        s.start()
        time.sleep(0.5)
        assert 1 <= s.cycles <= 30
    finally:
        s.stop()


def test_the_scheduler_store_is_opened_and_used_only_on_its_own_thread(
        live_database):
    seen = {"opened": [], "upload_thread": None}
    request_store = webapp._get_account_store()
    transport = _RecordingTransport()

    def open_store():
        store = SqliteAccountStore(live_database)
        seen["opened"].append((threading.get_ident(), store))
        return store
    s = OffsiteBackupScheduler(open_store=open_store, source_path=live_database,
                               resolve_settings=lambda: dict(SETTINGS),
                               transport=transport, poll_interval_seconds=0.05)
    try:
        s.start()
        deadline = time.time() + 5
        while not transport.calls and time.time() < deadline:
            time.sleep(0.01)
        assert transport.calls, "the first cycle did not run"
        assert {ident for ident, _ in seen["opened"]} == {s._thread.ident}
        assert s._thread.ident != threading.get_ident()
        assert all(store is not request_store for _, store in seen["opened"])
        assert transport.calls[0]["thread"] == s._thread.ident
    finally:
        s.stop()


def test_a_synchronous_check_uses_a_temporary_store_in_the_calling_thread(
        live_database):
    opened = []

    def spy():
        store = SqliteAccountStore(live_database)
        opened.append(store)
        return store
    s = OffsiteBackupScheduler(open_store=spy, source_path=live_database,
                               resolve_settings=lambda: dict(SETTINGS),
                               transport=_RecordingTransport())
    assert s.run_if_due() == SUCCESS
    assert len(opened) == 1
    with pytest.raises(Exception):                        # closed after the call
        opened[0]._conn.execute("SELECT 1")
    assert s.status()["last_success_at"] is not None      # status opens its own
    assert len(opened) == 2


def test_the_web_wiring_never_reuses_the_request_store():
    assert webapp._open_offsite_backup_store() is not webapp._get_account_store()
    assert webapp._open_offsite_backup_store() is not webapp._open_offsite_backup_store()
    assert webapp._open_offsite_backup_store() is not webapp._open_dispatcher_store()


def test_scheduler_and_email_dispatcher_share_no_state():
    s, d = webapp._OFFSITE_BACKUP_SCHEDULER, webapp._EMAIL_DISPATCHER
    assert s is not d
    assert s._stop is not d._stop and s._start_lock is not d._lifecycle
    assert s._open_store is not d._open_store
    assert THREAD_NAME != "inventorai-email-dispatcher"


# =============================================================================
# Logging / status: bounded facts only, never a credential or content
# =============================================================================

def test_operational_events_carry_bounded_facts_and_no_credential(live_database):
    emitted = _Emitted()
    transport = _RecordingTransport(statuses=[500, 200])
    clock = _Clock()
    s = _scheduler(live_database, transport, clock, emitted)
    s.run_if_due()
    clock.advance(6 * HOUR)
    s.run_if_due()
    failure, success = emitted.events
    assert failure["event"] == EVENT_FAILURE and failure["level"] == "warning"
    assert failure["fields"] == {"component": "offsite_backup", "outcome": "failure",
                                 "detail_code": "provider_rejected", "count": 1}
    assert success["event"] == EVENT_SUCCESS and success["level"] == "info"
    assert success["fields"] == {"component": "offsite_backup", "outcome": "success",
                                 "count": transport.calls[1]["body_bytes"]}
    text = repr(emitted.events)
    for forbidden in (SETTINGS["INVENTORAI_R2_ACCESS_KEY_ID"],
                      SETTINGS["INVENTORAI_R2_SECRET_ACCESS_KEY"],
                      "Authorization", "AWS4-HMAC-SHA256", "invention text",
                      live_database):
        assert forbidden not in text, forbidden


def test_events_pass_through_the_real_observability_seam_intact(live_database, capsys):
    """Through `web.observability.emit` the same facts render as one bounded
    JSON line each; nothing outside the allowlist survives."""
    from web import observability as obs
    transport = _RecordingTransport(statuses=[503, 200])
    clock = _Clock()
    s = _scheduler(live_database, transport, clock, emit=obs.emit)
    s.run_if_due()
    clock.advance(6 * HOUR)
    s.run_if_due()
    lines = [line for line in capsys.readouterr().err.splitlines()
             if "offsite_backup" in line]
    assert len(lines) == 2
    import json
    first, second = (json.loads(line) for line in lines)
    assert first["event"] == EVENT_FAILURE and first["detail_code"] == "provider_rejected"
    assert second["event"] == EVENT_SUCCESS and second["count"] == transport.calls[1]["body_bytes"]
    for line in lines:
        assert set(json.loads(line)) <= {"ts", "level", "event"} | obs.ALLOWED_FIELDS
        for forbidden in (SETTINGS["INVENTORAI_R2_ACCESS_KEY_ID"],
                          SETTINGS["INVENTORAI_R2_SECRET_ACCESS_KEY"],
                          "Authorization", "example.com", "invention text"):
            assert forbidden not in line


def test_the_scheduler_module_itself_never_logs_or_prints(live_database, caplog):
    source = io.open(SCHEDULER_SOURCE, encoding="utf-8").read()
    for forbidden in ("import logging", "logging.", "getLogger", "print("):
        assert forbidden not in source, forbidden
    with caplog.at_level(logging.DEBUG):
        s = _scheduler(live_database, _RecordingTransport(status=500))
        s.run_if_due()                                     # no emit callback
    assert caplog.text == ""


def test_status_is_read_only_operational_fact(live_database):
    s = _scheduler(live_database, _RecordingTransport(statuses=[500, 200]),
                   clock := _Clock())
    assert s.status() is None
    s.run_if_due()
    status = s.status()
    assert status["consecutive_failures"] == 1 and status["last_success_at"] is None
    clock.advance(6 * HOUR)
    s.run_if_due()
    status = s.status()
    assert set(status) == {"name", "active_claim_id", "claimed_at",
                           "last_attempt_at", "last_success_at",
                           "last_success_object_key", "last_success_bytes",
                           "last_success_sha256", "last_failure_at",
                           "last_failure_code", "consecutive_failures"}
    assert status["consecutive_failures"] == 0
    assert re.fullmatch(r"[0-9a-f]{64}", status["last_success_sha256"])
    text = repr(status)
    for forbidden in (SETTINGS["INVENTORAI_R2_ACCESS_KEY_ID"],
                      SETTINGS["INVENTORAI_R2_SECRET_ACCESS_KEY"], "invention text"):
        assert forbidden not in text
    # Reading status changed nothing.
    assert s.status() == status
    assert s.run_if_due() == NOT_DUE


def test_health_contract_is_unchanged():
    client = webapp.app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert sorted(response.get_json()) == ["database", "status"]


# =============================================================================
# Boundaries: no remote management, no second engine, no second datastore
# =============================================================================

def test_no_remote_delete_list_or_retention_and_no_second_engine_in_scheduler():
    source = io.open(SCHEDULER_SOURCE, encoding="utf-8").read()
    for forbidden in ("redis", "celery", "kombu", "pika", "boto", "sqs",
                      "multiprocessing", "concurrent.futures", "asyncio",
                      "sqlite3", "subprocess", "schedule", "apscheduler", "cron"):
        assert re.search(r"\bimport %s\b|\bfrom %s\b" % (forbidden, forbidden),
                         source) is None, forbidden
    assert "from engine.backup_service import BackupError, backup_database" in source
    assert "from engine.r2_object_upload import R2UploadError, put_object" in source
    # Operative removals: only the one workspace `rmtree`. (Prose is scanned
    # by the operative-code guard in test_infra_offsite_backup_r2.py.)
    assert re.search(r"\bos\.(remove|unlink|rmdir)\(", source) is None
    assert source.count("shutil.rmtree(") == 1
    requirements = io.open(os.path.join(ROOT, "requirements.txt"),
                           encoding="utf-8").read().lower()
    for forbidden in ("schedule", "celery", "redis", "apscheduler", "boto"):
        assert forbidden not in requirements, forbidden


def test_the_state_row_lives_in_the_canonical_database_and_is_upserted(live_database):
    """Same file as every other durable table; no second datastore; no DELETE
    FROM anywhere in the state methods (the retention doc guard enumerates the
    only automatic deletions and this is not one of them)."""
    store = SqliteAccountStore(live_database)
    try:
        tables = {r[0] for r in store._conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
        assert {"offsite_backup_state", "accounts", "email_outbox"} <= tables
        assert store.get_offsite_backup_state(SCHEDULE_NAME) is None
        assert store.claim_offsite_backup_run(
            SCHEDULE_NAME, "c1", "2026-01-01T00:00:00.000000Z", "9", "9") is True
        assert store.record_offsite_backup_failure(
            SCHEDULE_NAME, "c1", "2026-01-01T00:00:01.000000Z", "x") == 1
        assert store.claim_offsite_backup_run(
            SCHEDULE_NAME, "c2", "2026-01-01T00:00:02.000000Z", "9", "9") is True
        assert store.record_offsite_backup_failure(
            SCHEDULE_NAME, "c2", "2026-01-01T00:00:02.000000Z", "y") == 2
        assert store.claim_offsite_backup_run(
            SCHEDULE_NAME, "c3", "2026-01-01T00:00:03.000000Z", "9", "9") is True
        assert store.record_offsite_backup_success(
            SCHEDULE_NAME, "c3", "2026-01-01T00:00:03.000000Z", "k", 7, "h") is True
        row = store.get_offsite_backup_state(SCHEDULE_NAME)
        assert row["consecutive_failures"] == 0 and row["last_failure_code"] == "y"
        assert row["active_claim_id"] is None and row["claimed_at"] is None
        assert store._conn.execute(
            "SELECT COUNT(*) FROM offsite_backup_state").fetchone()[0] == 1
    finally:
        store.close()
    import inspect
    for method in (SqliteAccountStore.get_offsite_backup_state,
                   SqliteAccountStore.claim_offsite_backup_run,
                   SqliteAccountStore._offsite_state_row,
                   SqliteAccountStore.read_offsite_backup_state,
                   SqliteAccountStore.record_offsite_backup_success,
                   SqliteAccountStore.record_offsite_backup_failure,
                   SqliteAccountStore._ensure_offsite_backup_row):
        body = inspect.getsource(method).upper()
        assert "DELETE" not in body, method.__name__


def test_the_cli_status_command_is_read_only_and_needs_no_credential(
        live_database, tmp_path, capsys):
    import importlib.util
    import json
    spec = importlib.util.spec_from_file_location(
        "inventorai_offsite_backup_status",
        os.path.join(ROOT, "scripts", "inventorai_offsite_backup.py"))
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    # Before any run: null, exit 0, no credential needed (environ empty).
    assert cli.main(["status", live_database], environ={}) == 0
    assert capsys.readouterr().out.strip().endswith("null")
    # After a run: the row, and the live file untouched by reading it.
    s = _scheduler(live_database, _RecordingTransport(), _Clock())
    assert s.run_if_due() == SUCCESS
    before = _snapshot(live_database)
    assert cli.main(["status", live_database], environ={}) == 0
    out = capsys.readouterr().out
    payload = json.loads(out[out.index("{"):])
    assert payload["last_success_object_key"] == "daily/inventorai-20260920T030000Z.sqlite"
    assert payload["consecutive_failures"] == 0
    assert _snapshot(live_database) == before
    for forbidden in (SETTINGS["INVENTORAI_R2_ACCESS_KEY_ID"],
                      SETTINGS["INVENTORAI_R2_SECRET_ACCESS_KEY"], "invention text"):
        assert forbidden not in out
    # A database without the table (pre-upgrade file) reads as null, and a
    # missing file is an error - never a silently created database.
    plain = tmp_path / "plain.sqlite"
    with sqlite3.connect(str(plain)) as connection:
        connection.execute("CREATE TABLE t (x)")
    assert SqliteAccountStore.read_offsite_backup_state(str(plain), "daily") is None
    with pytest.raises(sqlite3.Error):
        SqliteAccountStore.read_offsite_backup_state(str(tmp_path / "absent.sqlite"), "daily")
    assert not os.path.exists(tmp_path / "absent.sqlite")


def test_the_manual_cli_still_works_over_the_same_pipeline(live_database, capsys):
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "inventorai_offsite_backup",
        os.path.join(ROOT, "scripts", "inventorai_offsite_backup.py"))
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    transport = _RecordingTransport()
    assert cli.main(["daily", live_database], environ=dict(SETTINGS),
                    transport=transport) == 0
    assert '"accepted": true' in capsys.readouterr().out
    assert cli.main(["daily", live_database], environ={},
                    transport=_RecordingTransport()) == 4
    assert cli.perform_offsite_backup is perform_offsite_backup


# =============================================================================
# Startup semantics: production only, only when configured; never in dev/test
# =============================================================================

def _cold_boot(extra_env, program):
    env = dict(os.environ)
    for name in list(env):
        if name.startswith("INVENTORAI_R2_"):
            env.pop(name)
    env.update({"INVENTORAI_ENV": "production",
                "INVENTORAI_SECRET_KEY": "boot-probe-not-a-real-secret",
                "PYTHONWARNINGS": "ignore"})
    env.update(extra_env)
    return subprocess.run([sys.executable, "-c", program], cwd=ROOT, env=env,
                          capture_output=True, text=True, timeout=180)


def test_production_boots_without_r2_config_and_starts_no_scheduler(tmp_path):
    result = _cold_boot(
        {"INVENTORAI_DB_PATH": str(tmp_path / "boot.sqlite")},
        "import threading, web.app as w;"
        "assert w._OFFSITE_BACKUP_SCHEDULER_STARTED is False;"
        "assert not w._OFFSITE_BACKUP_SCHEDULER.running;"
        "assert not [t for t in threading.enumerate() if 'backup' in t.name];"
        "assert w._OFFSITE_BACKUP_SCHEDULER.run_if_due() == 'skipped';"
        "print(w.app.test_client().get('/health').status_code)")
    assert result.returncode == 0, result.stderr[-2000:]
    assert result.stdout.strip() == "200"


def test_production_with_partial_r2_config_starts_no_scheduler(tmp_path):
    partial = {k: v for k, v in SETTINGS.items()
               if k != "INVENTORAI_R2_SECRET_ACCESS_KEY"}
    partial["INVENTORAI_DB_PATH"] = str(tmp_path / "boot.sqlite")
    result = _cold_boot(
        partial,
        "import threading, web.app as w;"
        "assert w._OFFSITE_BACKUP_SCHEDULER_STARTED is False;"
        "assert not w._OFFSITE_BACKUP_SCHEDULER.running;"
        "print(w.app.test_client().get('/health').status_code)")
    assert result.returncode == 0, result.stderr[-2000:]
    assert result.stdout.strip() == "200"


def test_production_with_complete_r2_config_starts_exactly_one_scheduler_thread(
        tmp_path):
    """The thread exists and is paced by the default poll interval, so within
    this probe it has not run a cycle and no upload could have been attempted
    (the process exits long before the first 5-minute wake-up)."""
    env = dict(SETTINGS, INVENTORAI_DB_PATH=str(tmp_path / "boot.sqlite"))
    result = _cold_boot(
        env,
        "import threading, web.app as w;"
        "assert w._OFFSITE_BACKUP_SCHEDULER_STARTED is True;"
        "assert w._OFFSITE_BACKUP_SCHEDULER.running;"
        "names=[t.name for t in threading.enumerate() if t.name=='%s'];"
        "assert names==['%s'], names;"
        "assert w._start_offsite_backup_scheduler_if_production() is False;"
        "assert w._OFFSITE_BACKUP_SCHEDULER.cycles == 0;"
        "assert w._OFFSITE_BACKUP_SCHEDULER.status() is None;"
        "assert w._EMAIL_DISPATCHER_STARTED is False;"
        "print(w.app.test_client().get('/health').status_code)"
        % (THREAD_NAME, THREAD_NAME))
    assert result.returncode == 0, result.stderr[-2000:]
    assert result.stdout.strip() == "200"


def test_dev_and_test_runtime_never_starts_the_scheduler():
    assert webapp._OFFSITE_BACKUP_SCHEDULER_STARTED is False
    assert not webapp._OFFSITE_BACKUP_SCHEDULER.running
    assert _scheduler_threads() == []


def test_gunicorn_stays_one_worker_one_thread():
    conf = io.open(os.path.join(ROOT, "gunicorn.conf.py"), encoding="utf-8").read()
    assert re.search(r"^workers\s*=\s*1\s*$", conf, re.M)
    assert re.search(r"^threads\s*=\s*1\s*$", conf, re.M)
    assert re.search(r"^preload_app\s*=\s*False\s*$", conf, re.M)


# =============================================================================
# B1 — claim ownership: stale completion can never overwrite newer state
# =============================================================================

class _GatedTransport(_RecordingTransport):
    """A transport whose PUT blocks until released - a run that outlives its
    claim, or a stop() that must wait on a run in progress."""

    def __init__(self, status=200):
        super().__init__(status=status)
        self.entered = threading.Event()
        self.release = threading.Event()

    def __call__(self, url, headers, path, size, timeout_seconds):
        self.entered.set()
        assert self.release.wait(30), "gated transport was never released"
        return super().__call__(url, headers, path, size, timeout_seconds)


def _claim(store, claim_id, now_iso, window_iso="9"):
    return store.claim_offsite_backup_run(SCHEDULE_NAME, claim_id, now_iso,
                                          window_iso, window_iso)


def test_every_won_claim_has_a_unique_persisted_owner(live_database):
    ids = {new_claim_id() for _ in range(1000)}
    assert len(ids) == 1000
    assert all(re.fullmatch(r"[0-9a-f]{32}", i) for i in ids)
    store = SqliteAccountStore(live_database)
    try:
        assert _claim(store, "owner-1", "2026-09-20T03:00:00.000000Z") is True
        row = store.get_offsite_backup_state(SCHEDULE_NAME)
        assert row["active_claim_id"] == "owner-1"
        assert row["claimed_at"] == row["last_attempt_at"] == "2026-09-20T03:00:00.000000Z"
    finally:
        store.close()


def test_scenario_1_a_second_claim_before_expiry_is_rejected(live_database):
    store = SqliteAccountStore(live_database)
    try:
        assert _claim(store, "run-a", "2026-09-20T03:00:00.000000Z",
                      "2026-09-19T21:00:00.000000Z") is True
        # B tries 5h59m later: A's claim is younger than the 6h window.
        assert _claim(store, "run-b", "2026-09-20T08:59:00.000000Z",
                      "2026-09-20T02:59:00.000000Z") is False
        assert store.get_offsite_backup_state(SCHEDULE_NAME)["active_claim_id"] == "run-a"
    finally:
        store.close()


def test_scenario_2_stale_success_after_reclaim_is_rejected_and_b_state_stands(
        live_database):
    store = SqliteAccountStore(live_database)
    try:
        assert _claim(store, "run-a", "2026-09-20T03:00:00.000000Z",
                      "2026-09-19T21:00:00.000000Z") is True
        # A is abandoned: 6h+ later B reclaims, which replaces the owner.
        assert _claim(store, "run-b", "2026-09-20T09:30:00.000000Z",
                      "2026-09-20T03:30:00.000000Z") is True
        assert store.get_offsite_backup_state(SCHEDULE_NAME)["active_claim_id"] == "run-b"
        assert store.record_offsite_backup_success(
            SCHEDULE_NAME, "run-b", "2026-09-20T09:31:00.000000Z",
            "daily/b.sqlite", 222, "b" * 64) is True
        # A finally completes: rejected, nothing of B's is altered.
        before = store.get_offsite_backup_state(SCHEDULE_NAME)
        assert store.record_offsite_backup_success(
            SCHEDULE_NAME, "run-a", "2026-09-20T09:45:00.000000Z",
            "daily/a.sqlite", 111, "a" * 64) is False
        assert store.record_offsite_backup_failure(
            SCHEDULE_NAME, "run-a", "2026-09-20T09:45:00.000000Z", "provider_rejected") is None
        assert store.get_offsite_backup_state(SCHEDULE_NAME) == before
        assert before["last_success_at"] == "2026-09-20T09:31:00.000000Z"
        assert before["last_success_object_key"] == "daily/b.sqlite"
        assert before["consecutive_failures"] == 0
        assert before["active_claim_id"] is None
    finally:
        store.close()


def test_scenario_2b_stale_failure_cannot_touch_a_newer_failure_counter(live_database):
    store = SqliteAccountStore(live_database)
    try:
        assert _claim(store, "run-a", "2026-09-20T03:00:00.000000Z") is True
        assert _claim(store, "run-b", "2026-09-20T09:30:00.000000Z") is True   # reclaim
        assert store.record_offsite_backup_failure(
            SCHEDULE_NAME, "run-b", "2026-09-20T09:31:00.000000Z", "provider_rejected") == 1
        before = store.get_offsite_backup_state(SCHEDULE_NAME)
        assert store.record_offsite_backup_failure(
            SCHEDULE_NAME, "run-a", "2026-09-20T09:40:00.000000Z", "provider_unreachable") is None
        assert store.record_offsite_backup_success(
            SCHEDULE_NAME, "run-a", "2026-09-20T09:40:00.000000Z", "k", 1, "a" * 64) is False
        assert store.get_offsite_backup_state(SCHEDULE_NAME) == before
        assert before["consecutive_failures"] == 1
        assert before["last_failure_code"] == "provider_rejected"
    finally:
        store.close()


def test_scenarios_2_3_4_end_to_end_through_the_scheduler(live_database):
    """Run A's upload hangs past the claim window; run B reclaims and succeeds
    at 09:30; A then finishes and is STALE. Next eligibility is computed from
    B's success only: nothing at 18h after B, a backup at 24h after B."""
    gated = _GatedTransport()
    clock_a = _Clock(T0)
    a = _scheduler(live_database, gated, clock_a)
    worker = threading.Thread(target=lambda: results.append(a.run_if_due()),
                              daemon=True)
    results = []
    worker.start()
    assert gated.entered.wait(10)                          # A owns the claim, upload hung
    row = _state(live_database)
    assert row["active_claim_id"] is not None and row["last_success_at"] is None

    clock_b = _Clock(T0 + 6 * HOUR + datetime.timedelta(minutes=30))
    b_transport = _RecordingTransport()
    b = _scheduler(live_database, b_transport, clock_b)
    assert b.run_if_due() == SUCCESS                        # reclaim + success at 09:30
    b_state = _state(live_database)
    assert b_state["last_success_at"] == "2026-09-20T09:30:00.000000Z"
    assert b_state["active_claim_id"] is None

    clock_a.advance(7 * HOUR)                              # A completes at 10:00
    gated.release.set()
    worker.join(10)
    assert results == [STALE]
    assert a.stale_completions == 1
    assert _state(live_database) == b_state                # B's state untouched

    # Scenario 4: 18h after B's success nothing is eligible, for anyone.
    clock_b.advance(18 * HOUR)
    assert b.run_if_due() == NOT_DUE
    clock_a.moment = clock_b.moment
    assert a.run_if_due() == NOT_DUE
    assert len(b_transport.calls) == 1 and len(gated.calls) == 1
    # Scenario 3: 24h after B's success (not A's completion) it is eligible.
    clock_b.advance(6 * HOUR)
    assert b.run_if_due() == SUCCESS
    assert _state(live_database)["last_success_at"] == "2026-09-21T09:30:00.000000Z"


def test_stale_completion_emits_a_bounded_event_and_no_success(live_database):
    emitted = _Emitted()
    gated = _GatedTransport()
    a = _scheduler(live_database, gated, _Clock(T0), emitted)
    results = []
    worker = threading.Thread(target=lambda: results.append(a.run_if_due()), daemon=True)
    worker.start()
    assert gated.entered.wait(10)
    # Another run reclaims after the window and fails; A then completes.
    b = _scheduler(live_database, _RecordingTransport(status=500),
                   _Clock(T0 + 7 * HOUR), emitted)
    assert b.run_if_due() == FAILURE
    gated.release.set()
    worker.join(10)
    assert results == [STALE]
    assert [e["event"] for e in emitted.events] == [EVENT_FAILURE, EVENT_STALE]
    assert emitted.events[1]["fields"] == {"component": "offsite_backup", "outcome": "stale"}
    state = _state(live_database)
    assert state["last_success_at"] is None and state["consecutive_failures"] == 1
    assert state["last_failure_code"] == "provider_rejected"


def test_reclaim_is_only_possible_after_the_bounded_window(live_database):
    """The abandoned-claim rule is exactly the failure-retry window: not one
    second earlier, and a reclaim invalidates the prior claim id."""
    store = SqliteAccountStore(live_database)
    try:
        assert _claim(store, "run-a", "2026-09-20T03:00:00.000000Z") is True
    finally:
        store.close()
    clock = _Clock(T0 + datetime.timedelta(seconds=DEFAULT_FAILURE_RETRY_SECONDS - 1))
    b = _scheduler(live_database, _RecordingTransport(), clock)
    assert b.run_if_due() == NOT_DUE
    clock.advance(datetime.timedelta(seconds=1))
    assert b.run_if_due() == SUCCESS
    store = SqliteAccountStore(live_database)
    try:
        assert store.record_offsite_backup_success(
            SCHEDULE_NAME, "run-a", "2026-09-20T09:01:00.000000Z", "k", 1, "a" * 64) is False
    finally:
        store.close()


def test_a_completed_claim_is_released_and_cannot_complete_twice(live_database):
    s = _scheduler(live_database, _RecordingTransport(), _Clock())
    assert s.run_if_due() == SUCCESS
    row = _state(live_database)
    assert row["active_claim_id"] is None and row["claimed_at"] is None
    store = SqliteAccountStore(live_database)
    try:
        # No owner at all: a completion with any id is stale.
        assert store.record_offsite_backup_success(
            SCHEDULE_NAME, "anything", "2026-09-20T03:05:00.000000Z", "k", 1, "a" * 64) is False
        assert store.record_offsite_backup_failure(
            SCHEDULE_NAME, "anything", "2026-09-20T03:05:00.000000Z", "x") is None
        assert store.get_offsite_backup_state(SCHEDULE_NAME) == row
    finally:
        store.close()


def test_completion_time_is_the_finish_time_not_the_claim_time(live_database):
    """A long run's next eligibility is measured from when it finished."""
    clock = _Clock(T0)
    transport = _RecordingTransport()
    s = _scheduler(live_database, transport, clock)
    original = transport.__call__

    def slow(*args, **kwargs):
        clock.advance(2 * HOUR)                      # the upload "took" 2h
        return original(*args, **kwargs)
    s._transport = slow
    assert s.run_if_due() == SUCCESS
    row = _state(live_database)
    assert row["last_attempt_at"] == "2026-09-20T03:00:00.000000Z"
    assert row["last_success_at"] == "2026-09-20T05:00:00.000000Z"
    clock.advance(23 * HOUR)                          # 25h after claim, 23h after finish
    assert s.run_if_due() == NOT_DUE
    clock.advance(HOUR)
    assert s.run_if_due() == SUCCESS


# =============================================================================
# N1 — stop()/start() lifecycle: never two threads
# =============================================================================

def test_stop_timeout_keeps_the_thread_reference_and_start_refuses_a_second(
        live_database):
    gated = _GatedTransport()
    s = _scheduler(live_database, gated, poll_interval_seconds=0.05)
    try:
        assert s.start() is True
        assert gated.entered.wait(10)                   # a run is in progress
        assert s.stop(timeout_seconds=0.2) is False     # still alive after the wait
        assert s.running and s.stopping
        assert s._thread is not None
        assert s.start() is False                       # refused: prior thread alive
        assert len(_scheduler_threads()) == 1
        gated.release.set()
        deadline = time.time() + 10
        while s.running and time.time() < deadline:
            time.sleep(0.02)
        assert not s.running
        assert s.stop() is True                         # releases the dead reference
        assert s._thread is None
        # Only now may a start create exactly one new thread.
        assert s.start() is True
        assert len(_scheduler_threads()) == 1
    finally:
        s.stop()
    assert len(_scheduler_threads()) == 0


def test_restart_after_actual_thread_death_creates_exactly_one_thread(live_database):
    s = _scheduler(live_database, poll_interval_seconds=0.05)
    for _ in range(3):
        assert s.start() is True
        assert s.stop() is True
        assert not s.running
    assert len(_scheduler_threads()) == 0


# =============================================================================
# N2 — one live scheduler per process, across instances and module reloads
# =============================================================================

def test_only_one_scheduler_instance_may_run_per_process(live_database):
    a = _scheduler(live_database, poll_interval_seconds=0.05)
    b = _scheduler(live_database, poll_interval_seconds=0.05)
    try:
        assert a.start() is True
        assert live_instance() is a
        assert b.start() is False                       # another instance is live
        assert len(_scheduler_threads()) == 1
        assert a.stop() is True
        assert live_instance() is None
        assert b.start() is True                        # prior thread actually dead
        assert live_instance() is b
        assert len(_scheduler_threads()) == 1
    finally:
        a.stop(); b.stop()
    assert len(_scheduler_threads()) == 0


def test_module_reload_reuses_the_live_scheduler_and_adds_no_thread(tmp_path):
    """Production cold boot with a complete configuration, then the application
    module is reloaded twice in-process: the live instance is reused and the
    thread count stays at one. (Production never reloads - `reload = False` -
    this pins the invariant regardless.)"""
    env = dict(SETTINGS, INVENTORAI_DB_PATH=str(tmp_path / "boot.sqlite"))
    result = _cold_boot(
        env,
        "import importlib, threading, web.app as w;"
        "first = w._OFFSITE_BACKUP_SCHEDULER;"
        "assert w._OFFSITE_BACKUP_SCHEDULER_STARTED is True and first.running;"
        "importlib.reload(w); importlib.reload(w);"
        "assert w._OFFSITE_BACKUP_SCHEDULER is first, 'a second instance was built';"
        "assert w._OFFSITE_BACKUP_SCHEDULER_STARTED is False;"   # reused, not restarted
        "names=[t.name for t in threading.enumerate() if t.name=='%s'];"
        "assert names==['%s'], names;"
        "print(w.app.test_client().get('/health').status_code)"
        % (THREAD_NAME, THREAD_NAME))
    assert result.returncode == 0, result.stderr[-2000:]
    assert result.stdout.strip() == "200"


def test_dev_reload_builds_a_fresh_instance_when_none_is_live():
    """Outside production nothing runs, so a reload simply rebuilds the
    (never started) instance - and still starts no thread."""
    assert live_instance() is None
    assert not webapp._OFFSITE_BACKUP_SCHEDULER.running
    assert _scheduler_threads() == []
