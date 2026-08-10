"""P5-1/P5-2 — durable account / token / rate-limit store.

A bounded, datastore-neutral account store with a Python stdlib ``sqlite3``
reference adapter, mirroring the ``engine.record_store.SqliteRecordStore`` pattern.
It is SEPARATE from the project record store (its own tables) so account data and
project data stay cleanly isolated; it shares the same ``INVENTORAI_DB_PATH`` file.

P5-1 (gate G-P5-1-…): the accounts / email-token / rate-limit foundation.
P5-2 (gate G-P5-2-AUTH-SESSIONS-VERIFIED-EMAIL-RECOVERY-IMPLEMENTATION-01) adds,
additively and behaviour-preservingly:

  * a thread/connection strategy (**precondition P5-2-PRE-02**): a single
    connection opened ``check_same_thread=False`` and guarded by a re-entrant
    lock so it can be shared safely across threads under a threaded WSGI server
    WITHOUT thread-affinity errors, and every write runs inside an explicit
    ``BEGIN IMMEDIATE`` … ``COMMIT`` transaction (foreign keys enforced,
    fail-closed rollback). This is not a bare ``check_same_thread=False``: access
    is serialised by the lock and each write takes the SQLite RESERVED lock
    immediately, so a read-modify-write can never interleave — even across
    separate connections/instances.
  * a **concurrency-safe** rate-limit counter (**precondition P5-2-PRE-01**): the
    read-modify-write runs inside ``BEGIN IMMEDIATE``, eliminating the prior
    multi-connection lost-update race, plus bounded cleanup of expired rows.
  * atomic, replay-safe token consumption; password update; ``session_epoch``
    increment (session revocation); email-verified marking; account status
    changes; token supersession.

P7-I2 (established contract
``docs/governance/P7_I2_VERSIONED_READ_EXPORT_PUBLIC_API_INCREMENT_CONTRACT.md``)
adds, additively (contract §12 schema-initialization boundary — the new tables
live in this EXISTING constructor-owned idempotent schema lifecycle; no API
route handler performs DDL/migration):

  * ``api_credentials`` — durable machine/API credentials: hash-only secret
    storage (mirroring ``email_tokens``), one bound ``owner_account_id``,
    explicit scopes, revocation and optional expiry.
  * ``access_audit`` — the minimal durable access/security audit event store
    (audit ≠ monitoring; no monitoring platform).

No plaintext passwords, no raw tokens, and no session cookies are ever stored.
All mutations are single atomic transactions. Timestamps are caller-provided
(deterministic, testable) and MUST be canonical fixed-width ISO-8601 UTC strings
so lexicographic comparison (window/expiry checks) is monotonic.
"""
import sqlite3
import threading
from contextlib import contextmanager

VERIFICATION = "verification"
RESET = "reset"
_TOKEN_TYPES = frozenset({VERIFICATION, RESET})

ACCOUNT_STATUSES = frozenset({"active", "disabled", "deleted"})

# P7-I2: machine/API credential lifecycle states (credential lifecycle only —
# NOT account states; canonical account states above are unchanged).
API_CREDENTIAL_STATUSES = frozenset({"active", "revoked"})

# How long a blocked writer waits for the SQLite write lock before giving up.
_BUSY_TIMEOUT_SECONDS = 30.0


class AccountStoreError(Exception):
    """Base class for account-store failures."""


class EmailExistsError(AccountStoreError):
    """Raised when a normalized email is already registered. The web layer maps
    this to the SAME generic response as success (no account enumeration)."""


_SCHEMA = (
    """
    CREATE TABLE IF NOT EXISTS accounts (
        account_id      TEXT PRIMARY KEY,
        email_normalized TEXT NOT NULL UNIQUE,
        email_verified  INTEGER NOT NULL DEFAULT 0,
        status          TEXT NOT NULL DEFAULT 'active',
        password_hash   TEXT NOT NULL,
        session_epoch   INTEGER NOT NULL DEFAULT 0,
        created_at      TEXT NOT NULL,
        updated_at      TEXT NOT NULL,
        deleted_at      TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS email_tokens (
        token_id    TEXT PRIMARY KEY,
        account_id  TEXT NOT NULL,
        token_type  TEXT NOT NULL,
        token_hash  TEXT NOT NULL,
        expires_at  TEXT NOT NULL,
        used_at     TEXT,
        created_at  TEXT NOT NULL,
        FOREIGN KEY (account_id) REFERENCES accounts(account_id)
    )
    """,
    "CREATE INDEX IF NOT EXISTS email_tokens_account_type_idx "
    "ON email_tokens (account_id, token_type)",
    "CREATE UNIQUE INDEX IF NOT EXISTS email_tokens_hash_uq ON email_tokens (token_hash)",
    """
    CREATE TABLE IF NOT EXISTS auth_rate_limits (
        subject_key   TEXT NOT NULL,
        action        TEXT NOT NULL,
        window_start  TEXT NOT NULL,
        attempt_count INTEGER NOT NULL,
        expires_at    TEXT NOT NULL,
        PRIMARY KEY (subject_key, action)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS api_credentials (
        credential_id    TEXT PRIMARY KEY,
        secret_hash      TEXT NOT NULL,
        owner_account_id TEXT NOT NULL,
        scopes           TEXT NOT NULL,
        status           TEXT NOT NULL DEFAULT 'active',
        expires_at       TEXT,
        revoked_at       TEXT,
        created_at       TEXT NOT NULL,
        FOREIGN KEY (owner_account_id) REFERENCES accounts(account_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS access_audit (
        event_id      INTEGER PRIMARY KEY,
        request_id    TEXT NOT NULL,
        credential_id TEXT,
        surface       TEXT NOT NULL,
        outcome       TEXT NOT NULL,
        project_id    TEXT,
        created_at    TEXT NOT NULL
    )
    """,
    # P8-I1: commercial plan-identity assignment (one per account; plan identity
    # ONLY — no lifecycle-state column and no period boundaries; those are
    # deferred to P8-I3 per the accepted P8-I1 refinement). Additive/idempotent.
    """
    CREATE TABLE IF NOT EXISTS commercial_assignments (
        account_id    TEXT PRIMARY KEY,
        plan_id       TEXT NOT NULL,
        plan_version  TEXT NOT NULL,
        assigned_at   TEXT NOT NULL,
        updated_at    TEXT NOT NULL,
        FOREIGN KEY (account_id) REFERENCES accounts(account_id)
    )
    """,
    # P8-I1: minimal, append-only commercial audit (assignment set/change only).
    # DISTINCT from the security ``access_audit`` above; NOT a generic
    # billing-event framework.
    """
    CREATE TABLE IF NOT EXISTS commercial_audit (
        event_id    INTEGER PRIMARY KEY,
        account_id  TEXT NOT NULL,
        event_type  TEXT NOT NULL,
        from_plan   TEXT,
        to_plan     TEXT,
        created_at  TEXT NOT NULL
    )
    """,
    # P8-I2: canonical commercial usage counter (one row per subject+window).
    # This is the SINGLE authoritative enforcement source; NOT a financial ledger.
    """
    CREATE TABLE IF NOT EXISTS commercial_usage (
        account_id  TEXT NOT NULL,
        meter       TEXT NOT NULL,
        window_key  TEXT NOT NULL,
        used_count  INTEGER NOT NULL DEFAULT 0,
        updated_at  TEXT NOT NULL,
        PRIMARY KEY (account_id, meter, window_key),
        FOREIGN KEY (account_id) REFERENCES accounts(account_id)
    )
    """,
    # P8-I2: auxiliary retry-safety keys, transactionally consistent with the
    # counter (no competing truth source). ``amount`` pins same-key replays.
    """
    CREATE TABLE IF NOT EXISTS commercial_usage_idempotency (
        account_id      TEXT NOT NULL,
        meter           TEXT NOT NULL,
        idempotency_key TEXT NOT NULL,
        amount          INTEGER NOT NULL,
        consumed_at     TEXT NOT NULL,
        PRIMARY KEY (account_id, meter, idempotency_key),
        FOREIGN KEY (account_id) REFERENCES accounts(account_id)
    )
    """,
    # P8-I3: append-only subscription-lifecycle event log — the SOURCE OF TRUTH
    # and the lifecycle audit (distinct from access_audit and commercial_audit).
    # ``event_id`` is the durable monotonic sequence and the equal-effective_at
    # tie-break authority. ``reason`` carries provenance (e.g. 'grace_exhausted')
    # and is NEVER an event type. ``external_reference`` is opaque/provider-neutral
    # (no provider payload). Additive; existing tables are untouched.
    """
    CREATE TABLE IF NOT EXISTS subscription_lifecycle_events (
        event_id             INTEGER PRIMARY KEY,
        account_id           TEXT NOT NULL,
        event_type           TEXT NOT NULL,
        from_state           TEXT,
        to_state             TEXT NOT NULL,
        effective_at         TEXT NOT NULL,
        recorded_at          TEXT NOT NULL,
        reason               TEXT,
        source               TEXT,
        external_reference   TEXT,
        idempotency_key      TEXT,
        sched_effective_at   TEXT,
        target_plan_id       TEXT,
        target_plan_version  TEXT,
        UNIQUE (account_id, idempotency_key),
        FOREIGN KEY (account_id) REFERENCES accounts(account_id)
    )
    """,
    # P8-I3: derived current-state cache (one row per account). ALWAYS a
    # deterministic function of the event log (the log stays authoritative). A
    # single pending scheduled transition may be recorded here.
    """
    CREATE TABLE IF NOT EXISTS subscription_lifecycle_state (
        account_id             TEXT PRIMARY KEY,
        current_state          TEXT NOT NULL,
        current_since          TEXT NOT NULL,
        scheduled_to_state     TEXT,
        scheduled_effective_at TEXT,
        scheduled_event_type   TEXT,
        scheduled_plan_id      TEXT,
        scheduled_plan_version TEXT,
        scheduled_event_id     INTEGER,
        updated_at             TEXT NOT NULL,
        FOREIGN KEY (account_id) REFERENCES accounts(account_id)
    )
    """,
    # P8-I4-I1: provider-neutral account↔provider mapping. External references are
    # OPAQUE strings; no provider id is an internal primary identity. Uniquely
    # keyed by (provider, external_subscription_ref) so the same subscription ref
    # can never map to two accounts (cross-account isolation). Additive; no secrets;
    # no card data; no raw provider payload.
    """
    CREATE TABLE IF NOT EXISTS provider_mapping (
        provider                  TEXT NOT NULL,
        external_subscription_ref TEXT NOT NULL,
        account_id                TEXT NOT NULL,
        external_customer_ref     TEXT,
        created_at                TEXT NOT NULL,
        updated_at                TEXT NOT NULL,
        PRIMARY KEY (provider, external_subscription_ref),
        FOREIGN KEY (account_id) REFERENCES accounts(account_id)
    )
    """,
    # P8-I4-I1: durable provider-event dedupe / integrity. Identity is
    # (provider, provider_event_id) — the same event id under a different provider
    # is a DISTINCT identity. ``fingerprint`` is a bounded deterministic digest of
    # the canonicalized event fields (NEVER the raw payload; NO secrets). An exact
    # re-delivery replays the prior outcome; a same-identity + different-fingerprint
    # delivery FAILS CLOSED. Records ACCEPTED events only.
    """
    CREATE TABLE IF NOT EXISTS provider_event_dedupe (
        provider              TEXT NOT NULL,
        provider_event_id     TEXT NOT NULL,
        fingerprint           TEXT NOT NULL,
        account_id            TEXT NOT NULL,
        canonical_event_type  TEXT NOT NULL,
        outcome_state         TEXT,
        lifecycle_event_id    INTEGER,
        created_at            TEXT NOT NULL,
        PRIMARY KEY (provider, provider_event_id),
        FOREIGN KEY (account_id) REFERENCES accounts(account_id)
    )
    """,
)


class SqliteAccountStore:
    """Reference/MVP durable adapter over Python stdlib ``sqlite3``. Additive and
    idempotent: constructing it on any existing (pre-P5) database creates only the
    new tables and never touches project data.

    Thread strategy (P5-2-PRE-02): one connection, ``check_same_thread=False``,
    guarded by a re-entrant lock; every write is an explicit ``BEGIN IMMEDIATE``
    transaction. Safe to share across threads. ``self._conn`` remains a real,
    stable connection object for backward compatibility."""

    def __init__(self, path: str):
        self._path = path
        self._lock = threading.RLock()
        # isolation_level=None → autocommit mode, so WE control transactions with
        # explicit BEGIN IMMEDIATE/COMMIT (required for the atomic rate-limit and
        # token critical sections). check_same_thread=False + the lock below make
        # the single shared connection safe under a threaded WSGI server.
        self._conn = sqlite3.connect(
            path, timeout=_BUSY_TIMEOUT_SECONDS, isolation_level=None,
            check_same_thread=False)
        with self._lock:
            self._conn.execute("PRAGMA foreign_keys = ON")
            self._conn.execute("BEGIN IMMEDIATE")
            try:
                for stmt in _SCHEMA:
                    self._conn.execute(stmt)
                self._conn.execute("COMMIT")
            except BaseException:
                self._conn.execute("ROLLBACK")
                raise

    # --- transaction helpers -----------------------------------------------
    @contextmanager
    def _write(self):
        """Serialise in-process access to the shared connection AND take the
        SQLite RESERVED lock immediately, so a concurrent writer (even from
        another connection/instance/process) can never interleave a
        read-modify-write. Commits on success, rolls back and re-raises on any
        error (fail closed)."""
        with self._lock:
            self._conn.execute("BEGIN IMMEDIATE")
            try:
                yield self._conn
            except BaseException:
                self._conn.execute("ROLLBACK")
                raise
            else:
                self._conn.execute("COMMIT")

    @contextmanager
    def _read(self):
        with self._lock:
            yield self._conn

    # --- accounts -----------------------------------------------------------
    def create_account(self, account_id: str, email_normalized: str,
                       password_hash: str, created_at: str,
                       status: str = "active") -> str:
        """Atomically create one account. The immutable ``account_id`` is the
        durable key; ``email_normalized`` carries a UNIQUE constraint so a
        duplicate (even under concurrency) can never create a second account —
        it raises ``EmailExistsError`` and the whole write rolls back. Stores the
        scrypt ``password_hash`` only; never a plaintext or reversible password."""
        if status not in ACCOUNT_STATUSES:
            raise AccountStoreError("invalid status: %r" % (status,))
        try:
            with self._write() as c:
                c.execute(
                    "INSERT INTO accounts (account_id, email_normalized, "
                    "email_verified, status, password_hash, session_epoch, "
                    "created_at, updated_at, deleted_at) "
                    "VALUES (?, ?, 0, ?, ?, 0, ?, ?, NULL)",
                    (account_id, email_normalized, status, password_hash,
                     created_at, created_at),
                )
        except sqlite3.IntegrityError as exc:
            # The UNIQUE(email_normalized) (or PK) constraint fired. Do NOT leak
            # which; the caller returns the same generic response either way.
            raise EmailExistsError("email already registered") from exc
        return account_id

    def _row_to_account(self, row):
        if row is None:
            return None
        return {
            "account_id": row[0], "email_normalized": row[1],
            "email_verified": bool(row[2]), "status": row[3],
            "password_hash": row[4], "session_epoch": row[5],
            "created_at": row[6], "updated_at": row[7], "deleted_at": row[8],
        }

    _ACCOUNT_COLS = ("account_id, email_normalized, email_verified, status, "
                     "password_hash, session_epoch, created_at, updated_at, deleted_at")

    def get_account_by_id(self, account_id: str):
        with self._read() as c:
            row = c.execute(
                "SELECT " + self._ACCOUNT_COLS + " FROM accounts WHERE account_id = ?",
                (account_id,)).fetchone()
        return self._row_to_account(row)

    def get_account_by_normalized_email(self, email_normalized: str):
        with self._read() as c:
            row = c.execute(
                "SELECT " + self._ACCOUNT_COLS + " FROM accounts WHERE email_normalized = ?",
                (email_normalized,)).fetchone()
        return self._row_to_account(row)

    def count_accounts(self) -> int:
        with self._read() as c:
            return c.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]

    def set_password_hash(self, account_id: str, password_hash: str, now_iso: str) -> int:
        """Update the scrypt hash for a non-deleted account. Returns the number of
        rows changed (0 if the account is missing or deleted). Never stores or
        logs the plaintext."""
        with self._write() as c:
            cur = c.execute(
                "UPDATE accounts SET password_hash = ?, updated_at = ? "
                "WHERE account_id = ? AND status != 'deleted'",
                (password_hash, now_iso, account_id))
            return cur.rowcount

    def increment_session_epoch(self, account_id: str, now_iso: str):
        """Atomically bump ``session_epoch`` (revokes every existing authenticated
        session for the account). Returns the new epoch, or None if missing."""
        with self._write() as c:
            c.execute(
                "UPDATE accounts SET session_epoch = session_epoch + 1, updated_at = ? "
                "WHERE account_id = ?", (now_iso, account_id))
            row = c.execute("SELECT session_epoch FROM accounts WHERE account_id = ?",
                            (account_id,)).fetchone()
        return row[0] if row else None

    def mark_email_verified(self, account_id: str, now_iso: str) -> int:
        """Set ``email_verified = 1`` for an ACTIVE account. Returns rows changed
        (0 if missing or not active)."""
        with self._write() as c:
            cur = c.execute(
                "UPDATE accounts SET email_verified = 1, updated_at = ? "
                "WHERE account_id = ? AND status = 'active'", (now_iso, account_id))
            return cur.rowcount

    def set_status(self, account_id: str, status: str, now_iso: str) -> int:
        """Set account status (active / disabled / deleted). ``deleted`` stamps
        ``deleted_at``. Bounded lifecycle primitive (no public admin route in
        P5-2). Returns rows changed."""
        if status not in ACCOUNT_STATUSES:
            raise AccountStoreError("invalid status: %r" % (status,))
        deleted_at = now_iso if status == "deleted" else None
        with self._write() as c:
            cur = c.execute(
                "UPDATE accounts SET status = ?, deleted_at = ?, updated_at = ? "
                "WHERE account_id = ?", (status, deleted_at, now_iso, account_id))
            return cur.rowcount

    # --- commercial assignment (P8-I1: plan identity ONLY) ------------------
    def get_commercial_assignment(self, account_id: str):
        """Return the durable commercial plan-identity assignment for
        ``account_id`` as a dict, or ``None`` when there is no assignment. A
        ``None`` result is the legitimate legacy/default state — NOT an error;
        the entitlement seam resolves it to the technical default. Carries plan
        identity only (no lifecycle state / no period boundaries — deferred to
        P8-I3)."""
        with self._read() as c:
            row = c.execute(
                "SELECT account_id, plan_id, plan_version, assigned_at, updated_at "
                "FROM commercial_assignments WHERE account_id = ?",
                (account_id,)).fetchone()
        if row is None:
            return None
        return {"account_id": row[0], "plan_id": row[1], "plan_version": row[2],
                "assigned_at": row[3], "updated_at": row[4]}

    def _append_commercial_audit(self, c, account_id, event_type, from_plan,
                                 to_plan, now_iso):
        """Append one minimal, append-only commercial-audit event on the SAME
        open write connection ``c`` (so it commits/rolls back atomically with the
        assignment mutation). Distinct from the security ``access_audit``."""
        c.execute(
            "INSERT INTO commercial_audit "
            "(account_id, event_type, from_plan, to_plan, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (account_id, event_type, from_plan, to_plan, now_iso))

    def set_commercial_assignment(self, account_id: str, plan_id: str,
                                  plan_version: str, now_iso: str):
        """Upsert the commercial plan-identity assignment for ``account_id`` AND
        append its commercial-audit event in the SAME ``BEGIN IMMEDIATE``
        transaction — so a crash can never leave an unaudited or partial
        commercial mutation. Stores plan identity only; validates nothing against
        the catalog (unknown/malformed identities fail closed later at the
        entitlement seam). Returns the stored ``(plan_id, plan_version)``."""
        with self._write() as c:
            prior = c.execute(
                "SELECT plan_id, plan_version FROM commercial_assignments "
                "WHERE account_id = ?", (account_id,)).fetchone()
            if prior is None:
                from_plan, event_type = None, "assigned"
                c.execute(
                    "INSERT INTO commercial_assignments "
                    "(account_id, plan_id, plan_version, assigned_at, updated_at) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (account_id, plan_id, plan_version, now_iso, now_iso))
            else:
                from_plan, event_type = "%s@%s" % (prior[0], prior[1]), "changed"
                c.execute(
                    "UPDATE commercial_assignments SET plan_id = ?, "
                    "plan_version = ?, updated_at = ? WHERE account_id = ?",
                    (plan_id, plan_version, now_iso, account_id))
            self._append_commercial_audit(
                c, account_id, event_type, from_plan,
                "%s@%s" % (plan_id, plan_version), now_iso)
        return (plan_id, plan_version)

    def list_commercial_audit(self, account_id: str):
        """Return the append-only commercial-audit events for ``account_id`` in
        insertion order (assignment set/change only)."""
        with self._read() as c:
            rows = c.execute(
                "SELECT event_id, account_id, event_type, from_plan, to_plan, "
                "created_at FROM commercial_audit WHERE account_id = ? "
                "ORDER BY event_id", (account_id,)).fetchall()
        return [{"event_id": r[0], "account_id": r[1], "event_type": r[2],
                 "from_plan": r[3], "to_plan": r[4], "created_at": r[5]}
                for r in rows]

    # --- subscription lifecycle (P8-I3: append-only event log + derived state) --
    #
    # This store layer is a purely MECHANICAL, atomic, fail-closed primitive:
    # account existence/active check + durable idempotency + optimistic
    # from-state guard + append-event + upsert-derived-state (+ optional
    # coordinated plan-assignment change) in ONE ``BEGIN IMMEDIATE``. It holds NO
    # lifecycle state-machine policy (that lives in
    # ``engine.subscription_lifecycle_service``) and imports no commercial module,
    # preserving the OD-N dependency direction.

    def get_lifecycle_state_row(self, account_id: str):
        """Return the derived current-state row for ``account_id`` as a dict, or
        ``None`` when no lifecycle row exists (the implicit ``none`` state).
        Low-level and account-UNAWARE (deterministic rebuild primitive); §10
        account fail-closed is enforced at the service boundary, not here."""
        with self._read() as c:
            row = c.execute(
                "SELECT account_id, current_state, current_since, "
                "scheduled_to_state, scheduled_effective_at, scheduled_event_type, "
                "scheduled_plan_id, scheduled_plan_version, scheduled_event_id, "
                "updated_at FROM subscription_lifecycle_state WHERE account_id = ?",
                (account_id,)).fetchone()
        if row is None:
            return None
        return {"account_id": row[0], "current_state": row[1],
                "current_since": row[2], "scheduled_to_state": row[3],
                "scheduled_effective_at": row[4], "scheduled_event_type": row[5],
                "scheduled_plan_id": row[6], "scheduled_plan_version": row[7],
                "scheduled_event_id": row[8], "updated_at": row[9]}

    def list_lifecycle_events(self, account_id: str):
        """Return the append-only lifecycle events for ``account_id`` in durable
        sequence order (``event_id``). Read-only; the log is the source of truth
        and carries the scheduled target plan (RC-I4). Low-level/account-unaware."""
        with self._read() as c:
            rows = c.execute(
                "SELECT event_id, account_id, event_type, from_state, to_state, "
                "effective_at, recorded_at, reason, source, external_reference, "
                "idempotency_key, sched_effective_at, target_plan_id, "
                "target_plan_version FROM subscription_lifecycle_events "
                "WHERE account_id = ? ORDER BY event_id", (account_id,)).fetchall()
        return [{"event_id": r[0], "account_id": r[1], "event_type": r[2],
                 "from_state": r[3], "to_state": r[4], "effective_at": r[5],
                 "recorded_at": r[6], "reason": r[7], "source": r[8],
                 "external_reference": r[9], "idempotency_key": r[10],
                 "sched_effective_at": r[11], "target_plan_id": r[12],
                 "target_plan_version": r[13]}
                for r in rows]

    def find_lifecycle_event(self, account_id: str, idempotency_key: str):
        """Return the prior lifecycle event for (account, idempotency_key) as a
        dict, or ``None``. Durable replay lookup (account-scoped), so a duplicate
        event is recognised before any transition re-validation.

        NOTE (idempotency-payload semantics — see P8-I4 mapping): replay is keyed
        by (account_id, idempotency_key) identity ONLY; it returns the prior
        recorded outcome and does NOT validate payload equality. The accepted
        P8-I3-C contract permits prior-result replay; a future payload-consistency
        check (if any) is a P8-I4 concern and must not silently change this."""
        if idempotency_key is None:
            return None
        with self._read() as c:
            row = c.execute(
                "SELECT event_id, event_type, to_state FROM "
                "subscription_lifecycle_events WHERE account_id = ? AND "
                "idempotency_key = ?", (account_id, idempotency_key)).fetchone()
        if row is None:
            return None
        return {"event_id": row[0], "event_type": row[1], "to_state": row[2]}

    def _upsert_lifecycle_state(self, c, account_id, current_state, current_since,
                                updated_at, scheduled_to_state,
                                scheduled_effective_at, scheduled_event_type,
                                scheduled_plan_id, scheduled_plan_version,
                                scheduled_event_id):
        """Upsert the derived current-state row on the open write connection ``c``
        (so it commits/rolls back atomically with the event append). ``current_since``
        is passed pre-computed by the caller (advances to the event effective time
        on every applied transition; preserved for a scheduling event)."""
        prior = c.execute(
            "SELECT account_id FROM subscription_lifecycle_state WHERE account_id = ?",
            (account_id,)).fetchone()
        if prior is None:
            c.execute(
                "INSERT INTO subscription_lifecycle_state "
                "(account_id, current_state, current_since, scheduled_to_state, "
                "scheduled_effective_at, scheduled_event_type, scheduled_plan_id, "
                "scheduled_plan_version, scheduled_event_id, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (account_id, current_state, current_since, scheduled_to_state,
                 scheduled_effective_at, scheduled_event_type, scheduled_plan_id,
                 scheduled_plan_version, scheduled_event_id, updated_at))
        else:
            c.execute(
                "UPDATE subscription_lifecycle_state SET current_state = ?, "
                "current_since = ?, scheduled_to_state = ?, scheduled_effective_at = ?, "
                "scheduled_event_type = ?, scheduled_plan_id = ?, "
                "scheduled_plan_version = ?, scheduled_event_id = ?, updated_at = ? "
                "WHERE account_id = ?",
                (current_state, current_since, scheduled_to_state,
                 scheduled_effective_at, scheduled_event_type, scheduled_plan_id,
                 scheduled_plan_version, scheduled_event_id, updated_at, account_id))

    def apply_lifecycle_event(self, account_id, *, event_type, expected_from_state,
                              new_current_state, event_to_state, effective_at,
                              recorded_at, reason=None, source=None,
                              external_reference=None, idempotency_key=None,
                              is_scheduling=False, require_no_pending=False,
                              event_sched_effective_at=None, target_plan_id=None,
                              target_plan_version=None, scheduled_to_state=None,
                              scheduled_effective_at=None, scheduled_event_type=None,
                              scheduled_plan_id=None, scheduled_plan_version=None,
                              assignment=None):
        """Atomically (one ``BEGIN IMMEDIATE``): fail-closed account check → durable
        idempotency → **in-transaction** stale-effective_at guard (RC-I2) →
        **in-transaction** pending-schedule exclusivity guard (RC-I1) → optimistic
        ``expected_from_state`` guard → append the lifecycle event (carrying the
        scheduled target plan, RC-I4) → optionally coordinate a P8-I1 assignment
        change → upsert the derived current state (recording ``scheduled_event_id``,
        RC-I5). ``current_since`` advances to ``effective_at`` on every applied
        transition (a scheduling event preserves it). Returns ``(status,
        current_state, event_id)``: ``"applied"`` / ``"idempotent_replay"`` /
        ``"conflict_stale"`` / ``"account_missing"`` / ``"account_inactive"``. Any
        error rolls the whole mutation back."""
        with self._write() as c:
            return self._apply_lifecycle_in_txn(
                c, account_id, event_type=event_type,
                expected_from_state=expected_from_state,
                new_current_state=new_current_state, event_to_state=event_to_state,
                effective_at=effective_at, recorded_at=recorded_at, reason=reason,
                source=source, external_reference=external_reference,
                idempotency_key=idempotency_key, is_scheduling=is_scheduling,
                require_no_pending=require_no_pending,
                event_sched_effective_at=event_sched_effective_at,
                target_plan_id=target_plan_id,
                target_plan_version=target_plan_version,
                scheduled_to_state=scheduled_to_state,
                scheduled_effective_at=scheduled_effective_at,
                scheduled_event_type=scheduled_event_type,
                scheduled_plan_id=scheduled_plan_id,
                scheduled_plan_version=scheduled_plan_version, assignment=assignment)

    def _apply_lifecycle_in_txn(self, c, account_id, *, event_type,
                                expected_from_state, new_current_state,
                                event_to_state, effective_at, recorded_at,
                                reason=None, source=None, external_reference=None,
                                idempotency_key=None, is_scheduling=False,
                                require_no_pending=False,
                                event_sched_effective_at=None, target_plan_id=None,
                                target_plan_version=None, scheduled_to_state=None,
                                scheduled_effective_at=None, scheduled_event_type=None,
                                scheduled_plan_id=None, scheduled_plan_version=None,
                                assignment=None):
        """The P8-I3 lifecycle write body on an ALREADY-OPEN write connection ``c``
        (inside a caller's ``BEGIN IMMEDIATE``). Identical guards/semantics to
        :meth:`apply_lifecycle_event`; extracted (behavior-preserving) so the P8-I4
        provider ingest can compose the SAME lifecycle mutation atomically with the
        provider-event dedupe record in one transaction. Holds NO provider
        knowledge."""
        if True:
            acct = c.execute("SELECT status FROM accounts WHERE account_id = ?",
                             (account_id,)).fetchone()
            if acct is None:
                return ("account_missing", None, None)
            if acct[0] != "active":
                return ("account_inactive", None, None)
            if idempotency_key is not None:
                prior = c.execute(
                    "SELECT to_state FROM subscription_lifecycle_events "
                    "WHERE account_id = ? AND idempotency_key = ?",
                    (account_id, idempotency_key)).fetchone()
                if prior is not None:
                    return ("idempotent_replay", prior[0], None)
            row = c.execute(
                "SELECT current_state, current_since, scheduled_effective_at "
                "FROM subscription_lifecycle_state WHERE account_id = ?",
                (account_id,)).fetchone()
            actual_from = row[0] if row is not None else "none"
            prior_since = row[1] if row is not None else None
            prior_pending = row[2] if row is not None else None
            # RC-I2 — in-transaction stale guard against the latest committed state.
            if prior_since is not None and int(effective_at) < int(prior_since):
                return ("conflict_stale", actual_from, None)
            # RC-I1 — in-transaction pending-schedule exclusivity: a second
            # scheduling event conflicting with an already-committed pending
            # schedule fails closed (no silent overwrite / silent loss).
            if require_no_pending and prior_pending is not None:
                return ("conflict_stale", actual_from, None)
            # Optimistic from-state guard (different-transition race → one wins).
            if actual_from != expected_from_state:
                return ("conflict_stale", actual_from, None)
            cur = c.execute(
                "INSERT INTO subscription_lifecycle_events "
                "(account_id, event_type, from_state, to_state, effective_at, "
                "recorded_at, reason, source, external_reference, idempotency_key, "
                "sched_effective_at, target_plan_id, target_plan_version) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (account_id, event_type, expected_from_state, event_to_state,
                 effective_at, recorded_at, reason, source, external_reference,
                 idempotency_key, event_sched_effective_at, target_plan_id,
                 target_plan_version))
            event_id = cur.lastrowid
            if assignment is not None:
                plan_id, plan_version = assignment
                prior_a = c.execute(
                    "SELECT plan_id, plan_version FROM commercial_assignments "
                    "WHERE account_id = ?", (account_id,)).fetchone()
                if prior_a is None:
                    from_plan, ev = None, "assigned"
                    c.execute(
                        "INSERT INTO commercial_assignments "
                        "(account_id, plan_id, plan_version, assigned_at, updated_at) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (account_id, plan_id, plan_version, recorded_at, recorded_at))
                else:
                    from_plan, ev = "%s@%s" % (prior_a[0], prior_a[1]), "changed"
                    c.execute(
                        "UPDATE commercial_assignments SET plan_id = ?, "
                        "plan_version = ?, updated_at = ? WHERE account_id = ?",
                        (plan_id, plan_version, recorded_at, account_id))
                self._append_commercial_audit(
                    c, account_id, ev, from_plan,
                    "%s@%s" % (plan_id, plan_version), recorded_at)
            if is_scheduling:
                # State unchanged; preserve current_since; record the scheduling
                # event's id so materialization idempotency is epoch-unique (RC-I5).
                since = prior_since if prior_since is not None else effective_at
                sched_eid = event_id
            else:
                # A concrete transition advances current_since and clears any
                # pending schedule (scheduled_* left None by the caller).
                since = effective_at
                sched_eid = None
            self._upsert_lifecycle_state(
                c, account_id, new_current_state, since, recorded_at,
                scheduled_to_state, scheduled_effective_at, scheduled_event_type,
                scheduled_plan_id, scheduled_plan_version, sched_eid)
            return ("applied", new_current_state, event_id)

    # --- payment provider boundary (P8-I4-I1: mapping + event dedupe) --------
    #
    # Provider-neutral persistence + the ATOMIC provider-event ingest. Holds NO
    # provider vocabulary and imports no provider adapter — adapters live in the
    # isolated ``engine.payment_*`` boundary and never touch this store's tables
    # directly; the P8-I4 coordinator passes only canonical, already-mapped values.

    def put_provider_mapping(self, account_id, *, provider, external_subscription_ref,
                             external_customer_ref, now_iso):
        """Durably record/refresh an account↔provider mapping. Fail-closed:
        missing/disabled/deleted account → denied; a blank/non-string external
        subscription ref → denied; a (provider, external_subscription_ref) already
        bound to a DIFFERENT account → cross-account conflict (no remap). Returns
        ``"created"`` / ``"exists"`` / ``"account_missing"`` / ``"account_inactive"``
        / ``"malformed_ref"`` / ``"cross_account_conflict"``."""
        if (not isinstance(external_subscription_ref, str)
                or not external_subscription_ref.strip()
                or not isinstance(provider, str) or not provider.strip()):
            return "malformed_ref"
        with self._write() as c:
            acct = c.execute("SELECT status FROM accounts WHERE account_id = ?",
                             (account_id,)).fetchone()
            if acct is None:
                return "account_missing"
            if acct[0] != "active":
                return "account_inactive"
            row = c.execute(
                "SELECT account_id FROM provider_mapping WHERE provider = ? AND "
                "external_subscription_ref = ?",
                (provider, external_subscription_ref)).fetchone()
            if row is not None:
                if row[0] != account_id:
                    return "cross_account_conflict"           # fail closed; no remap
                c.execute(
                    "UPDATE provider_mapping SET external_customer_ref = ?, "
                    "updated_at = ? WHERE provider = ? AND external_subscription_ref = ?",
                    (external_customer_ref, now_iso, provider, external_subscription_ref))
                return "exists"
            c.execute(
                "INSERT INTO provider_mapping (provider, external_subscription_ref, "
                "account_id, external_customer_ref, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (provider, external_subscription_ref, account_id,
                 external_customer_ref, now_iso, now_iso))
            return "created"

    def get_provider_mapping_account(self, provider, external_subscription_ref):
        """Return the mapped ``account_id`` for (provider, external_subscription_ref)
        or ``None``. Read-only lookup used by the coordinator; a blank ref → None."""
        if (not isinstance(external_subscription_ref, str)
                or not external_subscription_ref.strip()
                or not isinstance(provider, str) or not provider.strip()):
            return None
        with self._read() as c:
            row = c.execute(
                "SELECT account_id FROM provider_mapping WHERE provider = ? AND "
                "external_subscription_ref = ?",
                (provider, external_subscription_ref)).fetchone()
        return row[0] if row is not None else None

    def get_provider_event(self, provider, provider_event_id):
        """Return the durable dedupe record for (provider, provider_event_id) or
        ``None``. Read-only."""
        with self._read() as c:
            row = c.execute(
                "SELECT provider, provider_event_id, fingerprint, account_id, "
                "canonical_event_type, outcome_state, lifecycle_event_id, created_at "
                "FROM provider_event_dedupe WHERE provider = ? AND provider_event_id = ?",
                (provider, provider_event_id)).fetchone()
        if row is None:
            return None
        return {"provider": row[0], "provider_event_id": row[1], "fingerprint": row[2],
                "account_id": row[3], "canonical_event_type": row[4],
                "outcome_state": row[5], "lifecycle_event_id": row[6],
                "created_at": row[7]}

    def ingest_provider_lifecycle_event(self, account_id, *, provider,
                                        provider_event_id, fingerprint,
                                        canonical_event_type, now_iso, transition_fn,
                                        effective_at, recorded_at, reason=None,
                                        source=None, external_reference=None,
                                        idempotency_key=None):
        """ATOMIC (one ``BEGIN IMMEDIATE``): provider-event dedupe + the SAME P8-I3
        lifecycle mutation, so a provider event is never half-applied (dedupe without
        lifecycle, or lifecycle without dedupe). The lifecycle STATE MACHINE stays
        with the caller: ``transition_fn(from_state) -> to_state | None`` is invoked
        INSIDE the transaction against the committed in-transaction state (so a
        duplicate is recognised BEFORE any transition is attempted, and a genuine
        non-duplicate computes its transition from a consistent state). ``None`` →
        invalid transition, fail closed. Dedupe records ACCEPTED events ONLY (a
        pre-acceptance rejection persists no dedupe row, so a corrected redelivery
        can still succeed). Returns ``(status, current_state, lifecycle_event_id)``;
        ``status`` adds ``"provider_duplicate"`` (exact replay), ``"provider_conflict"``
        (same identity, different fingerprint → FAIL CLOSED) and ``"invalid_transition"``
        to the lifecycle statuses. The store imports no commercial module."""
        with self._write() as c:
            acct = c.execute("SELECT status FROM accounts WHERE account_id = ?",
                             (account_id,)).fetchone()
            if acct is None:
                return ("account_missing", None, None)
            if acct[0] != "active":
                return ("account_inactive", None, None)
            prior = c.execute(
                "SELECT fingerprint, outcome_state, lifecycle_event_id FROM "
                "provider_event_dedupe WHERE provider = ? AND provider_event_id = ?",
                (provider, provider_event_id)).fetchone()
            if prior is not None:
                if prior[0] == fingerprint:
                    return ("provider_duplicate", prior[1], prior[2])   # exact replay
                return ("provider_conflict", None, None)               # fail closed
            row = c.execute(
                "SELECT current_state FROM subscription_lifecycle_state "
                "WHERE account_id = ?", (account_id,)).fetchone()
            from_state = row[0] if row is not None else "none"
            to_state = transition_fn(from_state)           # caller's state machine
            if to_state is None:
                return ("invalid_transition", from_state, None)        # not recorded
            status, state, event_id = self._apply_lifecycle_in_txn(
                c, account_id, event_type=canonical_event_type,
                expected_from_state=from_state, new_current_state=to_state,
                event_to_state=to_state, effective_at=str(effective_at),
                recorded_at=recorded_at, reason=reason, source=source,
                external_reference=external_reference,
                idempotency_key=idempotency_key, is_scheduling=False)
            if status != "applied":
                # pre-acceptance rejection → do NOT record dedupe (allow corrected
                # redelivery). Nothing lifecycle was written (guards precede insert).
                return (status, state, event_id)
            c.execute(
                "INSERT INTO provider_event_dedupe (provider, provider_event_id, "
                "fingerprint, account_id, canonical_event_type, outcome_state, "
                "lifecycle_event_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (provider, provider_event_id, fingerprint, account_id,
                 canonical_event_type, state, event_id, now_iso))
            return ("applied", state, event_id)

    # --- commercial usage quota (P8-I2: counter + retry idempotency) --------
    def get_commercial_usage(self, account_id: str, meter: str, window_key: str) -> int:
        """Return the canonical durable used-count for (account, meter, window),
        or 0 when there is no row. Read-only; the counter is the single
        authoritative enforcement source."""
        with self._read() as c:
            row = c.execute(
                "SELECT used_count FROM commercial_usage "
                "WHERE account_id = ? AND meter = ? AND window_key = ?",
                (account_id, meter, window_key)).fetchone()
        return row[0] if row else 0

    def _insert_quota_idempotency(self, c, account_id, meter, idempotency_key,
                                  amount, now_iso):
        """Insert one retry-idempotency key on the SAME open write connection so it
        commits/rolls back atomically with the counter mutation."""
        c.execute(
            "INSERT INTO commercial_usage_idempotency "
            "(account_id, meter, idempotency_key, amount, consumed_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (account_id, meter, idempotency_key, amount, now_iso))

    def consume_commercial_quota(self, account_id, meter, window_key, unlimited,
                                 limit, amount, now_iso, idempotency_key):
        """Atomic evaluate-and-consume (one ``BEGIN IMMEDIATE`` critical section).
        Commercial-layer-agnostic: takes primitive policy values and returns a
        status string — this persistence layer imports NO commercial module.

        Returns ``(status, used_count)`` where status is one of:
        ``"allowed"`` (counter incremented), ``"allowed_idempotent_replay"`` (an
        identical prior key → no second increment), ``"exhausted"`` (hard cap →
        NO increment), or ``"conflict"`` (same key, different amount → NO
        increment). ``used_count`` is the counter value AFTER any increment.
        Concurrent final-slot writers serialise on the RESERVED lock, so a hard
        cap can never be oversubscribed."""
        with self._write() as c:
            if idempotency_key is not None:
                prior = c.execute(
                    "SELECT amount FROM commercial_usage_idempotency "
                    "WHERE account_id = ? AND meter = ? AND idempotency_key = ?",
                    (account_id, meter, idempotency_key)).fetchone()
                if prior is not None:
                    row = self._read_usage_row(c, account_id, meter, window_key)
                    used = row[0] if row else 0
                    if prior[0] != amount:
                        return ("conflict", used)          # same key, different amount
                    return ("allowed_idempotent_replay", used)
            row = self._read_usage_row(c, account_id, meter, window_key)
            used = row[0] if row else 0
            if not unlimited and used + amount > limit:
                return ("exhausted", used)                 # hard cap → no write
            new_used = used + amount
            if row is None:
                c.execute(
                    "INSERT INTO commercial_usage "
                    "(account_id, meter, window_key, used_count, updated_at) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (account_id, meter, window_key, new_used, now_iso))
            else:
                c.execute(
                    "UPDATE commercial_usage SET used_count = ?, updated_at = ? "
                    "WHERE account_id = ? AND meter = ? AND window_key = ?",
                    (new_used, now_iso, account_id, meter, window_key))
            if idempotency_key is not None:
                self._insert_quota_idempotency(c, account_id, meter,
                                               idempotency_key, amount, now_iso)
            return ("allowed", new_used)

    @staticmethod
    def _read_usage_row(c, account_id, meter, window_key):
        return c.execute(
            "SELECT used_count FROM commercial_usage "
            "WHERE account_id = ? AND meter = ? AND window_key = ?",
            (account_id, meter, window_key)).fetchone()

    # --- email tokens -------------------------------------------------------
    def create_email_token(self, token_id: str, account_id: str, token_type: str,
                          token_hash: str, expires_at: str, created_at: str) -> str:
        """Atomically issue one typed token, storing only its HASH. Before
        inserting, any still-active (unused) token of the SAME type for the
        account is superseded (marked used) so a re-issue invalidates the prior
        one. Accepts ``verification`` or ``reset``."""
        if token_type not in _TOKEN_TYPES:
            raise AccountStoreError("invalid token_type: %r" % (token_type,))
        with self._write() as c:
            c.execute(
                "UPDATE email_tokens SET used_at = ? "
                "WHERE account_id = ? AND token_type = ? AND used_at IS NULL",
                (created_at, account_id, token_type),
            )
            c.execute(
                "INSERT INTO email_tokens (token_id, account_id, token_type, "
                "token_hash, expires_at, used_at, created_at) "
                "VALUES (?, ?, ?, ?, ?, NULL, ?)",
                (token_id, account_id, token_type, token_hash, expires_at, created_at),
            )
        return token_id

    def get_email_token_by_hash(self, token_hash: str):
        """Read-only lookup by token hash."""
        with self._read() as c:
            row = c.execute(
                "SELECT token_id, account_id, token_type, token_hash, expires_at, "
                "used_at, created_at FROM email_tokens WHERE token_hash = ?",
                (token_hash,)).fetchone()
        if row is None:
            return None
        return {"token_id": row[0], "account_id": row[1], "token_type": row[2],
                "token_hash": row[3], "expires_at": row[4], "used_at": row[5],
                "created_at": row[6]}

    def consume_token(self, token_hash: str, token_type: str, now_iso: str):
        """Atomically consume a token: mark it used IFF it exists, is of the given
        type, is unused, is unexpired, and belongs to an ACTIVE account. Returns
        the ``account_id`` on success, else None. Replay-safe: the SELECT→UPDATE
        runs inside ``BEGIN IMMEDIATE``, so a second concurrent consume sees the
        already-used token and returns None."""
        if token_type not in _TOKEN_TYPES:
            raise AccountStoreError("invalid token_type: %r" % (token_type,))
        with self._write() as c:
            row = c.execute(
                "SELECT token_id, account_id, expires_at, used_at FROM email_tokens "
                "WHERE token_hash = ? AND token_type = ?", (token_hash, token_type)).fetchone()
            if row is None:
                return None
            token_id, account_id, expires_at, used_at = row
            if used_at is not None:
                return None
            if now_iso >= expires_at:
                return None
            acct = c.execute("SELECT status FROM accounts WHERE account_id = ?",
                             (account_id,)).fetchone()
            if acct is None or acct[0] != "active":
                return None
            c.execute("UPDATE email_tokens SET used_at = ? WHERE token_id = ? AND used_at IS NULL",
                      (now_iso, token_id))
            return account_id

    def supersede_tokens(self, account_id: str, token_type: str, now_iso: str) -> int:
        """Mark every still-active token of a type for an account as used. Returns
        the number superseded."""
        if token_type not in _TOKEN_TYPES:
            raise AccountStoreError("invalid token_type: %r" % (token_type,))
        with self._write() as c:
            cur = c.execute(
                "UPDATE email_tokens SET used_at = ? "
                "WHERE account_id = ? AND token_type = ? AND used_at IS NULL",
                (now_iso, account_id, token_type))
            return cur.rowcount

    def active_tokens(self, account_id: str, token_type: str) -> int:
        with self._read() as c:
            return c.execute(
                "SELECT COUNT(*) FROM email_tokens WHERE account_id = ? "
                "AND token_type = ? AND used_at IS NULL", (account_id, token_type)).fetchone()[0]

    def active_verification_tokens(self, account_id: str) -> int:
        return self.active_tokens(account_id, VERIFICATION)

    # --- bounded, concurrency-safe rate-limit foundation --------------------
    def record_rate_attempt(self, subject_key: str, action: str, now_iso: str,
                            window_reset_iso: str, limit: int) -> bool:
        """Concurrency-safe bounded counter (P5-2-PRE-01). The read-modify-write
        runs inside ``BEGIN IMMEDIATE``, so concurrent attempts — even from
        separate connections — serialise and never lose an update. Increments the
        attempt count for (subject_key, action) within the current window; starts
        a fresh window when the stored one has expired (``now_iso >= expires_at``).
        Returns True when the attempt is WITHIN the limit, False when it exceeds
        it. Stores no raw password/token and no raw email (the caller passes a
        privacy digest)."""
        with self._write() as c:
            row = c.execute(
                "SELECT window_start, attempt_count, expires_at FROM auth_rate_limits "
                "WHERE subject_key = ? AND action = ?", (subject_key, action)).fetchone()
            if row is None or now_iso >= row[2]:
                c.execute(
                    "INSERT INTO auth_rate_limits (subject_key, action, window_start, "
                    "attempt_count, expires_at) VALUES (?, ?, ?, 1, ?) "
                    "ON CONFLICT(subject_key, action) DO UPDATE SET "
                    "window_start = excluded.window_start, attempt_count = 1, "
                    "expires_at = excluded.expires_at",
                    (subject_key, action, now_iso, window_reset_iso))
                return 1 <= limit
            new_count = row[1] + 1
            c.execute(
                "UPDATE auth_rate_limits SET attempt_count = ? "
                "WHERE subject_key = ? AND action = ?", (new_count, subject_key, action))
            return new_count <= limit

    def cleanup_expired_rate_limits(self, now_iso: str, max_rows: int = 1000) -> int:
        """Bounded deletion of expired rate-limit rows (``expires_at <= now``),
        capped at ``max_rows`` per call so a cleanup can never scan/delete the
        whole table unbounded. Returns the number deleted."""
        with self._write() as c:
            cur = c.execute(
                "DELETE FROM auth_rate_limits WHERE rowid IN "
                "(SELECT rowid FROM auth_rate_limits WHERE expires_at <= ? LIMIT ?)",
                (now_iso, max_rows))
            return cur.rowcount

    def rate_limit_row_count(self) -> int:
        with self._read() as c:
            return c.execute("SELECT COUNT(*) FROM auth_rate_limits").fetchone()[0]

    # --- P7-I2: machine/API credentials (hash-only at rest) -----------------
    def create_api_credential(self, credential_id: str, secret_hash: str,
                              owner_account_id: str, scopes: str,
                              created_at: str, expires_at: str = None) -> str:
        """Persist one machine/API credential: the caller supplies ONLY the
        one-way ``secret_hash`` (mirroring ``email_tokens.token_hash``); the raw
        secret is never seen or stored here. Bound to exactly one existing
        ``owner_account_id``; ``scopes`` is a space-separated scope string;
        ``expires_at`` (optional) is a canonical ISO-8601 UTC string."""
        with self._write() as c:
            c.execute(
                "INSERT INTO api_credentials (credential_id, secret_hash, "
                "owner_account_id, scopes, status, expires_at, revoked_at, "
                "created_at) VALUES (?, ?, ?, ?, 'active', ?, NULL, ?)",
                (credential_id, secret_hash, owner_account_id, scopes,
                 expires_at, created_at))
        return credential_id

    _API_CREDENTIAL_COLS = ("credential_id, secret_hash, owner_account_id, "
                            "scopes, status, expires_at, revoked_at, created_at")

    def get_api_credential(self, credential_id: str):
        """Read-only lookup by public ``credential_id``; None when unknown."""
        with self._read() as c:
            row = c.execute(
                "SELECT " + self._API_CREDENTIAL_COLS +
                " FROM api_credentials WHERE credential_id = ?",
                (credential_id,)).fetchone()
        if row is None:
            return None
        return {"credential_id": row[0], "secret_hash": row[1],
                "owner_account_id": row[2], "scopes": row[3], "status": row[4],
                "expires_at": row[5], "revoked_at": row[6], "created_at": row[7]}

    def revoke_api_credential(self, credential_id: str, now_iso: str) -> int:
        """Durably revoke a credential (idempotent). Returns rows changed
        (0 when unknown or already revoked)."""
        with self._write() as c:
            cur = c.execute(
                "UPDATE api_credentials SET status = 'revoked', revoked_at = ? "
                "WHERE credential_id = ? AND status = 'active'",
                (now_iso, credential_id))
            return cur.rowcount

    # --- P7-I2: minimal durable access/security audit -----------------------
    def record_access_audit(self, request_id: str, surface: str, outcome: str,
                            created_at: str, credential_id: str = None,
                            project_id: str = None) -> None:
        """Append one durable access/security audit event. Stores identifiers
        and outcome classes only — never a secret, secret hash, or payload.
        Raises on failure so the caller can fail closed (a public decision is
        not served without its audit event)."""
        with self._write() as c:
            c.execute(
                "INSERT INTO access_audit (request_id, credential_id, surface, "
                "outcome, project_id, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (request_id, credential_id, surface, outcome, project_id,
                 created_at))

    def list_access_audit(self, limit: int = 100):
        """Bounded newest-first read of audit events (test/operator evidence;
        not a monitoring surface)."""
        with self._read() as c:
            rows = c.execute(
                "SELECT event_id, request_id, credential_id, surface, outcome, "
                "project_id, created_at FROM access_audit "
                "ORDER BY event_id DESC LIMIT ?", (int(limit),)).fetchall()
        return [{"event_id": r[0], "request_id": r[1], "credential_id": r[2],
                 "surface": r[3], "outcome": r[4], "project_id": r[5],
                 "created_at": r[6]} for r in rows]

    # --- lifecycle ----------------------------------------------------------
    def close(self) -> None:
        with self._lock:
            self._conn.close()
