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

    # --- lifecycle ----------------------------------------------------------
    def close(self) -> None:
        with self._lock:
            self._conn.close()
