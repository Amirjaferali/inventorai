"""OD-INFRA-5 — the ONE bounded in-process daily off-provider backup scheduler.

File path: ``engine/offsite_backup_scheduler.py``
Purpose:   make the Owner-decided DAILY off-provider backup happen by itself,
           from inside the ONE production web-service process, because that
           process is the only place the persistent disk holding the canonical
           SQLite database is mounted. A separate cron job, worker or one-off
           job cannot be assumed to share that disk, so the schedule lives here.

The pipeline is the existing one and only one, composed - never re-implemented:

    canonical live SQLite database (read-only)
      -> engine/backup_service.py  backup_database()   (the ONE backup engine)
        -> validated temporary artifact
          -> engine/r2_object_upload.py  put_object()  (the ONE transport)
            -> create-only R2 object
              -> temporary artifact removed, in every outcome

What this is NOT:
  * NOT a second backup engine and NOT a second transport. This module has no
    SQLite call of its own beyond the scheduler-state rows below, no copy
    logic, no validation logic and no signing logic.
  * NOT a retention manager. There is no delete, expire, rotate or list path:
    retention is unresolved in the privacy/legal lane and the create-only
    upload never replaces an object. Objects accumulate until a governed
    retention decision exists.
  * NOT a queue library, a worker service, a second process or a second
    datastore. ONE daemon thread inside the ONE Gunicorn worker; its state is
    one row in the one canonical SQLite file.
  * NOT thread-per-backup and NOT a busy loop. One thread, ``Event.wait``
    pacing, one bounded check per poll, at most one backup per check.
  * NOT exact cron. "Approximately once per 24 hours": a run becomes eligible
    when the persisted last success is at least one interval old.

Duplicate prevention across restarts and redeploys: eligibility is decided from
the PERSISTED state (``offsite_backup_state`` in the canonical database), never
from an in-memory timestamp alone, and a run is CLAIMED in one atomic
``BEGIN IMMEDIATE`` check-and-write before any upload begins. A quick
succession of restarts after a success therefore produces no second backup,
two briefly overlapping processes (a redeploy) cannot both win the same run,
and a process killed mid-upload does not re-run the moment it comes back - it
waits the bounded failure-retry interval.

Failure model: a failed run is recorded (counted, categorised by a stable
reason code) and the next eligible moment is one failure-retry interval later,
measured in HOURS. A provider outage therefore costs a handful of attempts per
day, never dozens per hour. A failure never mutates the live database, never
removes any remote object, and is never reported as success.

Secrecy: this module never imports ``logging`` and never prints. The optional
``emit`` callback receives only bounded operational facts - an event name, a
component/outcome token, a stable failure code and a byte count. No access
key, secret, signature, authorization header, row value or file content is
ever passed to it, because none of that is returned to this layer.
"""
import datetime
import os
import shutil
import tempfile
import threading

from engine.backup_service import BackupError, backup_database
from engine.r2_object_upload import R2UploadError, put_object

# Bounded scheduling policy. Small, fixed, deliberately unremarkable.
DEFAULT_POLL_INTERVAL_SECONDS = 300.0          # one bounded wake-up per 5 min
DEFAULT_INTERVAL_SECONDS = 24 * 60 * 60.0      # approximately daily
DEFAULT_FAILURE_RETRY_SECONDS = 6 * 60 * 60.0  # hours, not seconds
DEFAULT_UPLOAD_TIMEOUT_SECONDS = 120.0

_MIN_POLL_SECONDS = 0.05
_MAX_POLL_SECONDS = 3600.0
_MIN_INTERVAL_SECONDS = 60.0
_MAX_INTERVAL_SECONDS = 30 * 24 * 60 * 60.0

# The one persisted schedule this process runs.
SCHEDULE_NAME = "daily"
THREAD_NAME = "inventorai-offsite-backup-scheduler"

# Outcome tokens of one check.
SUCCESS = "success"
FAILURE = "failure"
NOT_DUE = "not_due"
SKIPPED = "skipped"            # no complete configuration: fail closed, touch nothing

EVENT_SUCCESS = "offsite_backup.scheduled_success"
EVENT_FAILURE = "offsite_backup.scheduled_failure"

# Stable failure categories that are not a provider reason code.
FAILURE_BACKUP = "backup_error"
FAILURE_UNEXPECTED = "unexpected_error"

REQUIRED_SETTINGS = ("INVENTORAI_R2_ACCOUNT_ID", "INVENTORAI_R2_BUCKET",
                     "INVENTORAI_R2_ACCESS_KEY_ID",
                     "INVENTORAI_R2_SECRET_ACCESS_KEY")


def _utc_now():
    return datetime.datetime.now(datetime.timezone.utc)


def _iso(moment):
    return moment.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _parse_iso(value):
    return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
        tzinfo=datetime.timezone.utc)


# --- configuration (shared with the operator CLI) ----------------------------

def resolve_settings(environ=None):
    """Read the provider configuration from the environment. Fail closed.

    Raises ``R2UploadError('missing_configuration', <NAME>)`` naming only the
    VARIABLE that is absent - never a value, and never a partial value.
    """
    source = environ if environ is not None else os.environ
    resolved = {}
    for name in REQUIRED_SETTINGS:
        value = (source.get(name) or "").strip()
        if not value:
            raise R2UploadError("missing_configuration", name)
        resolved[name] = value
    resolved["INVENTORAI_R2_PREFIX"] = (
        source.get("INVENTORAI_R2_PREFIX") or "").strip().strip("/")
    return resolved


def configuration_complete(environ=None):
    """True only when every required variable is present and non-blank."""
    try:
        resolve_settings(environ)
    except R2UploadError:
        return False
    return True


def object_key(prefix, filename):
    """Compose the destination object key. No timestamp parsing, no collision
    handling that could overwrite silently - the caller supplies a unique name."""
    return "%s/%s" % (prefix, filename) if prefix else filename


def artifact_filename(moment):
    """The UTC-stamped artifact name shared by the scheduler and the CLI."""
    return "inventorai-%s.sqlite" % moment.strftime("%Y%m%dT%H%M%SZ")


# --- the one pipeline (shared with the operator CLI) -------------------------

def perform_offsite_backup(source_path, settings, filename=None, key=None,
                           timeout_seconds=DEFAULT_UPLOAD_TIMEOUT_SECONDS,
                           transport=None, now=None):
    """Consistent backup -> validate -> upload -> remove the temporary copy.

    The live database is only ever read (the service opens the source
    read-only and uses the SQLite online-backup API), so this is safe against
    the serving database. The temporary backup is removed in every outcome,
    including failure, so a repeating schedule cannot fill the disk. Returns
    ``{"backup": <service report>, "upload": <transport report>, "key": key}``
    on CONFIRMED provider acceptance; every other outcome raises
    ``BackupError`` or ``R2UploadError``.
    """
    moment = now or _utc_now()
    filename = filename or artifact_filename(moment)
    key = key or object_key(settings["INVENTORAI_R2_PREFIX"], filename)
    workspace = tempfile.mkdtemp(prefix="inventorai-offsite-")
    try:
        staged = os.path.join(workspace, filename)
        backup_report = backup_database(source_path, staged)
        upload_report = put_object(
            source_path=staged, bucket=settings["INVENTORAI_R2_BUCKET"],
            object_key=key, account_id=settings["INVENTORAI_R2_ACCOUNT_ID"],
            access_key_id=settings["INVENTORAI_R2_ACCESS_KEY_ID"],
            secret_access_key=settings["INVENTORAI_R2_SECRET_ACCESS_KEY"],
            timeout_seconds=timeout_seconds, transport=transport)
        return {"backup": backup_report, "upload": upload_report, "key": key}
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


# --- the scheduler -----------------------------------------------------------

class OffsiteBackupScheduler:
    """One bounded scheduler. Construct once per process; ``start()`` is
    idempotent and never creates a second thread.

    ``open_store`` must return a NEW ``SqliteAccountStore`` each call; the
    scheduler opens it in whichever thread runs the check and closes it there,
    so no SQLite connection ever crosses a thread. ``source_path`` is the live
    database path or a callable returning it. ``resolve_settings`` returns the
    complete provider configuration or raises ``R2UploadError``. ``transport``
    and ``clock`` are test seams; ``emit`` is the optional bounded
    operational-event callback.
    """

    def __init__(self, open_store, source_path, resolve_settings,
                 poll_interval_seconds=DEFAULT_POLL_INTERVAL_SECONDS,
                 interval_seconds=DEFAULT_INTERVAL_SECONDS,
                 failure_retry_seconds=DEFAULT_FAILURE_RETRY_SECONDS,
                 upload_timeout_seconds=DEFAULT_UPLOAD_TIMEOUT_SECONDS,
                 transport=None, emit=None, clock=None):
        if not callable(open_store) or not callable(resolve_settings):
            raise ValueError("open_store and resolve_settings must be callables")
        poll = float(poll_interval_seconds)
        if not _MIN_POLL_SECONDS <= poll <= _MAX_POLL_SECONDS:
            raise ValueError("poll interval must be bounded")
        interval = float(interval_seconds)
        if not _MIN_INTERVAL_SECONDS <= interval <= _MAX_INTERVAL_SECONDS:
            raise ValueError("backup interval must be bounded")
        retry = float(failure_retry_seconds)
        if not _MIN_INTERVAL_SECONDS <= retry <= interval:
            raise ValueError(
                "failure retry must be bounded and no longer than the interval")
        self._open_store = open_store
        self._source_path = source_path
        self._resolve_settings = resolve_settings
        self._poll = poll
        self._interval = interval
        self._retry = retry
        self._timeout = float(upload_timeout_seconds)
        self._transport = transport
        self._emit = emit
        self._clock = clock or _utc_now
        self._thread = None
        self._stop = threading.Event()
        self._start_lock = threading.Lock()
        self.cycles = 0                    # completed poll cycles (evidence only)
        self.loop_faults = 0               # exceptions swallowed by the loop

    # --- eligibility ---------------------------------------------------------

    def _elapsed(self, stamp, now):
        """Seconds since ``stamp``; None when absent or unparseable (treated as
        'never', which makes a run eligible rather than silently blocked)."""
        if not stamp:
            return None
        try:
            return (now - _parse_iso(stamp)).total_seconds()
        except ValueError:
            return None

    def due(self, state, now):
        """Eligible iff the last SUCCESS is absent or at least one interval old,
        AND the last ATTEMPT (success or failure) is absent or at least one
        failure-retry interval old. The second clause is what bounds retries
        after a failure and after a run interrupted mid-upload."""
        if state is None:
            return True
        since_success = self._elapsed(state.get("last_success_at"), now)
        if since_success is not None and since_success < self._interval:
            return False
        since_attempt = self._elapsed(state.get("last_attempt_at"), now)
        if since_attempt is not None and since_attempt < self._retry:
            return False
        return True

    # --- one check -----------------------------------------------------------

    def _source(self):
        source = self._source_path
        return source() if callable(source) else source

    def _report(self, event, level, **fields):
        if self._emit is None:
            return
        try:
            self._emit(event, level=level, **fields)
        except Exception:
            pass

    def run_if_due(self, store=None, now=None):
        """Perform at most ONE backup if eligible. Synchronous and deterministic:
        this is the seam tests use. Opens a temporary store in the CALLING
        thread when none is supplied, so no connection is shared across threads.

        Fails closed at the configuration level: with an incomplete provider
        configuration nothing is uploaded and nothing is recorded.
        """
        try:
            settings = self._resolve_settings()
        except R2UploadError:
            return SKIPPED
        moment = now or self._clock()
        own_store = store is None
        active = self._open_store() if own_store else store
        try:
            # Cheap read first, so an ordinary poll takes no write lock.
            if not self.due(active.get_offsite_backup_state(SCHEDULE_NAME),
                            moment):
                return NOT_DUE
            # Then ONE atomic check-and-claim, recorded BEFORE the upload: two
            # briefly overlapping processes cannot both win, and an interrupted
            # run waits out the bounded retry interval instead of re-running
            # at the next boot.
            claimed = active.claim_offsite_backup_run(
                SCHEDULE_NAME, _iso(moment),
                _iso(moment - datetime.timedelta(seconds=self._retry)),
                _iso(moment - datetime.timedelta(seconds=self._interval)))
            if not claimed:
                return NOT_DUE
            try:
                report = perform_offsite_backup(
                    self._source(), settings, timeout_seconds=self._timeout,
                    transport=self._transport, now=moment)
            except R2UploadError as exc:
                code = exc.reason_code
            except BackupError:
                code = FAILURE_BACKUP
            except Exception:
                code = FAILURE_UNEXPECTED
            else:
                upload = report["upload"]
                active.record_offsite_backup_success(
                    SCHEDULE_NAME, _iso(moment), report["key"],
                    int(upload["bytes"]), upload["sha256"])
                self._report(EVENT_SUCCESS, "info", component="offsite_backup",
                             outcome="success", count=int(upload["bytes"]))
                return SUCCESS
            failures = active.record_offsite_backup_failure(
                SCHEDULE_NAME, _iso(moment), code)
            self._report(EVENT_FAILURE, "warning", component="offsite_backup",
                         outcome="failure", detail_code=code, count=failures)
            return FAILURE
        finally:
            if own_store:
                try:
                    active.close()
                except Exception:
                    pass

    def status(self, store=None):
        """Read-only operational status: the persisted state row (timestamps,
        counters, the last stored object's key/size/digest) or None. Carries no
        credential and no database content. Opens a temporary store in the
        calling thread when none is supplied."""
        own_store = store is None
        active = self._open_store() if own_store else store
        try:
            return active.get_offsite_backup_state(SCHEDULE_NAME)
        finally:
            if own_store:
                try:
                    active.close()
                except Exception:
                    pass

    # --- the one thread ------------------------------------------------------

    def _run(self):
        store = None
        try:
            # `Event.wait` is the pacing: never a tight loop. The first check
            # runs after one poll interval, not immediately at import.
            while not self._stop.wait(self._poll):
                try:
                    if store is None:
                        store = self._open_store()
                    self.run_if_due(store=store)
                    self.cycles += 1
                except Exception:
                    # A store or pipeline fault is counted and swallowed. The
                    # web process never sees it, and the loop keeps its pace.
                    self.loop_faults += 1
                    try:
                        if store is not None:
                            store.close()
                    except Exception:
                        pass
                    store = None
        finally:
            if store is not None:
                try:
                    store.close()
                except Exception:
                    pass

    def start(self):
        """Start the ONE scheduler thread. Idempotent: a second call while the
        thread is alive returns False and creates nothing."""
        with self._start_lock:
            if self._thread is not None and self._thread.is_alive():
                return False
            self._stop.clear()
            self._thread = threading.Thread(
                target=self._run, name=THREAD_NAME, daemon=True)
            self._thread.start()
            return True

    def stop(self, timeout_seconds=5.0):
        with self._start_lock:
            thread = self._thread
            if thread is None:
                return
            self._stop.set()
            thread.join(timeout_seconds)
            self._thread = None

    @property
    def running(self):
        thread = self._thread
        return bool(thread is not None and thread.is_alive())

    @property
    def thread_name(self):
        return None if self._thread is None else self._thread.name
