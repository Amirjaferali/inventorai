"""OD-INFRA-6 — ONE bounded in-process email dispatcher over the durable outbox.

File path: ``engine/email_dispatcher.py``
Purpose:   move the provider network call OFF the anonymous request path. The
           registration and recovery requests only record a pending message in
           the outbox (``engine/account_store.py``, canonical database); this
           dispatcher delivers it later, from its own thread, through the
           existing ``EmailSender`` boundary.

Why: with delivery inline, the provider round trip happened only on the branch
where an account was eligible for a message, so anonymous request latency
revealed account existence (~1 provider round trip, measured at ~200 ms vs
~2 ms). With delivery deferred, the request path does the same work on every
branch, and the provider's latency, success or failure can no longer be
observed through it.

What this is NOT:
  * NOT a queue library, a worker service, a second process or a second
    datastore - the outbox is a table in the one canonical SQLite file, and
    this is ONE daemon thread inside the ONE Gunicorn worker.
  * NOT thread-per-message. One thread, one bounded poll, one bounded batch.
  * NOT a retry framework. A small fixed attempt budget with a bounded backoff;
    an exhausted message is recorded as ``failed`` with its token-bearing body
    scrubbed, never reported as delivered.

Thread confinement: this thread never touches the request thread's store.
It opens its OWN ``SqliteAccountStore`` (own connection) inside its own thread
and closes it on exit. ``dispatch_pending`` can also be driven synchronously by
the caller - development/test use that for determinism - and then opens a
temporary store in the CALLING thread, so no connection ever crosses threads.

Secrecy: nothing here logs. No recipient, subject, body, token, key,
authorization header or provider detail is written anywhere; a delivery
failure is a counted attempt and nothing more. No provider exception can
propagate out of the loop, so none can take the web process down.
"""
import datetime
import threading

# Bounded delivery policy. Small, fixed, deliberately unremarkable.
DEFAULT_POLL_INTERVAL_SECONDS = 2.0
DEFAULT_MAX_ATTEMPTS = 5
DEFAULT_BATCH_LIMIT = 20
DEFAULT_BASE_BACKOFF_SECONDS = 2.0
DEFAULT_MAX_BACKOFF_SECONDS = 300.0

DELIVERED = "delivered"
RETRY_LATER = "retry_later"
EXHAUSTED = "exhausted"
DEFERRED = "deferred"          # not yet eligible under the backoff
SKIPPED = "skipped"            # no capable sender: fail closed, touch nothing


def _utc_now():
    return datetime.datetime.now(datetime.timezone.utc)


def _iso(moment):
    return moment.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _parse_iso(value):
    return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
        tzinfo=datetime.timezone.utc)


class EmailDispatcher:
    """One bounded dispatcher. Construct once per process; ``start()`` is
    idempotent and never creates a second thread."""

    def __init__(self, open_store, resolve_sender,
                 poll_interval_seconds=DEFAULT_POLL_INTERVAL_SECONDS,
                 max_attempts=DEFAULT_MAX_ATTEMPTS,
                 batch_limit=DEFAULT_BATCH_LIMIT,
                 base_backoff_seconds=DEFAULT_BASE_BACKOFF_SECONDS,
                 max_backoff_seconds=DEFAULT_MAX_BACKOFF_SECONDS,
                 clock=None):
        if not callable(open_store) or not callable(resolve_sender):
            raise ValueError("open_store and resolve_sender must be callables")
        poll = float(poll_interval_seconds)
        if not 0.05 <= poll <= 300:
            raise ValueError("poll interval must be bounded")
        if not 1 <= int(max_attempts) <= 20:
            raise ValueError("max attempts must be a small bounded number")
        self._open_store = open_store
        self._resolve_sender = resolve_sender
        self._poll = poll
        self._max_attempts = int(max_attempts)
        self._batch_limit = max(1, min(int(batch_limit), 100))
        self._base_backoff = float(base_backoff_seconds)
        self._max_backoff = float(max_backoff_seconds)
        self._clock = clock or _utc_now
        self._thread = None
        self._stop = threading.Event()
        self._lifecycle = threading.Lock()
        self.cycles = 0                    # completed poll cycles (evidence only)
        self.loop_faults = 0               # exceptions swallowed by the loop

    # --- eligibility ---------------------------------------------------------

    def backoff_seconds(self, attempt_count):
        """Bounded exponential backoff after `attempt_count` failed attempts."""
        if attempt_count <= 0:
            return 0.0
        return min(self._max_backoff,
                   self._base_backoff * (2 ** (attempt_count - 1)))

    def _eligible(self, message, now):
        if message["attempt_count"] <= 0 or not message["last_attempt_at"]:
            return True
        try:
            last = _parse_iso(message["last_attempt_at"])
        except ValueError:
            return True
        return (now - last).total_seconds() >= self.backoff_seconds(
            message["attempt_count"])

    # --- one message ---------------------------------------------------------

    def _deliver(self, store, sender, message, now):
        """Attempt ONE message. Returns an outcome token; never raises for a
        provider failure, and never records success on anything but a confirmed
        acceptance from the sender."""
        try:
            accepted = sender.send(to=message["recipient"],
                                   subject=message["subject"],
                                   body=message["body"])
        except Exception:
            accepted = False
        if accepted is True:
            store.mark_email_delivered(message["message_id"])
            return DELIVERED
        status = store.mark_email_attempt_failed(
            message["message_id"], _iso(now), self._max_attempts)
        return EXHAUSTED if status == "failed" else RETRY_LATER

    # --- one cycle -----------------------------------------------------------

    def dispatch_pending(self, store=None, now=None):
        """Deliver every currently eligible pending message, bounded by the
        batch limit. Synchronous and deterministic: this is the seam tests and
        development use. Opens a temporary store in the CALLING thread when none
        is supplied, so no connection is shared across threads.

        Fails closed at the delivery-capability level: with no capable sender
        (production without a configured provider) nothing is sent and nothing
        is mutated - messages simply stay pending.
        """
        sender = self._resolve_sender()
        if sender is None or not getattr(sender, "can_deliver", False):
            return {SKIPPED: 1, DELIVERED: 0, RETRY_LATER: 0, EXHAUSTED: 0,
                    DEFERRED: 0}
        moment = now or self._clock()
        counts = {DELIVERED: 0, RETRY_LATER: 0, EXHAUSTED: 0, DEFERRED: 0,
                  SKIPPED: 0}
        own_store = store is None
        active = self._open_store() if own_store else store
        try:
            for message in active.pending_emails(limit=self._batch_limit):
                if not self._eligible(message, moment):
                    counts[DEFERRED] += 1
                    continue
                counts[self._deliver(active, sender, message, moment)] += 1
        finally:
            if own_store:
                try:
                    active.close()
                except Exception:
                    pass
        return counts

    def dispatch_one(self, message_id, store=None, now=None):
        """Deliver exactly one named message regardless of backoff. Test seam."""
        sender = self._resolve_sender()
        if sender is None or not getattr(sender, "can_deliver", False):
            return SKIPPED
        own_store = store is None
        active = self._open_store() if own_store else store
        try:
            message = active.get_outbox_message(message_id)
            if message is None or message["status"] != "pending":
                return SKIPPED
            return self._deliver(active, sender, message, now or self._clock())
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
            store = self._open_store()
        except Exception:
            store = None
        try:
            # `Event.wait` is the pacing: never a tight loop. The first cycle
            # runs after one interval, not immediately at import.
            while not self._stop.wait(self._poll):
                try:
                    if store is None:
                        store = self._open_store()
                    self.dispatch_pending(store=store)
                    self.cycles += 1
                except Exception:
                    # A provider or store fault is counted and swallowed. The
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
        """Start the ONE dispatcher thread. Idempotent: a second call while the
        thread is alive returns False and creates nothing."""
        with self._lifecycle:
            if self._thread is not None and self._thread.is_alive():
                return False
            self._stop.clear()
            self._thread = threading.Thread(
                target=self._run, name="inventorai-email-dispatcher",
                daemon=True)
            self._thread.start()
            return True

    def stop(self, timeout_seconds=5.0):
        with self._lifecycle:
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
