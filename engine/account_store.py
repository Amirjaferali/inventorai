"""P5-1 — Account & Credential Foundation: durable account/token/rate-limit store.

A bounded, datastore-neutral account store with a Python stdlib ``sqlite3``
reference adapter, mirroring the ``engine.record_store.SqliteRecordStore`` pattern
(gate G-P5-1-ACCOUNT-CREDENTIAL-FOUNDATION-IMPLEMENTATION-01, Option A). It is
SEPARATE from the project record store (its own tables + connection) so account
data and project data stay cleanly isolated. It shares the same
``INVENTORAI_DB_PATH`` file.

Persisted (additive; created idempotently; legacy/pre-P5 databases simply gain
the new tables — no existing ``projects``/``records`` row is read, rewritten, or
destroyed):
  * ``accounts``       — the canonical account model (immutable UUID id; NEVER
                          email as the primary key; scrypt password_hash only).
  * ``email_tokens``   — typed (``verification``|``reset``) token records storing
                          only the token HASH; P5-1 issues only ``verification``.
  * ``auth_rate_limits``— a bounded store-backed counter foundation.

No plaintext passwords, no raw tokens, and no session tokens are ever stored.
All mutations are single atomic transactions (commit on success, full rollback
on error). Timestamps are caller-provided (deterministic, testable).
"""
import sqlite3
from typing import Optional

VERIFICATION = "verification"
RESET = "reset"                       # reserved future type; P5-1 does NOT implement reset
_TOKEN_TYPES = frozenset({VERIFICATION, RESET})

ACCOUNT_STATUSES = frozenset({"active", "disabled", "deleted"})


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
    """Reference/MVP durable adapter over Python stdlib ``sqlite3`` for the P5-1
    account foundation. Additive and idempotent: constructing it on any existing
    (pre-P5) database creates only the new tables and never touches project data."""

    def __init__(self, path: str):
        self._path = path
        self._conn = sqlite3.connect(path)
        self._conn.execute("PRAGMA foreign_keys = ON")
        with self._conn:
            for stmt in _SCHEMA:
                self._conn.execute(stmt)

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
            with self._conn:
                self._conn.execute(
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

    def get_account_by_id(self, account_id: str):
        row = self._conn.execute(
            "SELECT account_id, email_normalized, email_verified, status, "
            "password_hash, session_epoch, created_at, updated_at, deleted_at "
            "FROM accounts WHERE account_id = ?", (account_id,)).fetchone()
        return self._row_to_account(row)

    def get_account_by_normalized_email(self, email_normalized: str):
        row = self._conn.execute(
            "SELECT account_id, email_normalized, email_verified, status, "
            "password_hash, session_epoch, created_at, updated_at, deleted_at "
            "FROM accounts WHERE email_normalized = ?", (email_normalized,)).fetchone()
        return self._row_to_account(row)

    def count_accounts(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]

    # --- email tokens (P5-1: verification issuance foundation only) ---------
    def create_email_token(self, token_id: str, account_id: str, token_type: str,
                          token_hash: str, expires_at: str, created_at: str) -> str:
        """Atomically issue one typed token, storing only its HASH. Before
        inserting a new ``verification`` token, any still-active (unused,
        unexpired) verification token for the account is superseded (marked used)
        so a re-issue safely invalidates the prior one. P5-1 accepts only the
        ``verification`` type."""
        if token_type not in _TOKEN_TYPES:
            raise AccountStoreError("invalid token_type: %r" % (token_type,))
        with self._conn:
            self._conn.execute(
                "UPDATE email_tokens SET used_at = ? "
                "WHERE account_id = ? AND token_type = ? AND used_at IS NULL",
                (created_at, account_id, token_type),
            )
            self._conn.execute(
                "INSERT INTO email_tokens (token_id, account_id, token_type, "
                "token_hash, expires_at, used_at, created_at) "
                "VALUES (?, ?, ?, ?, ?, NULL, ?)",
                (token_id, account_id, token_type, token_hash, expires_at, created_at),
            )
        return token_id

    def get_email_token_by_hash(self, token_hash: str):
        """Read-only lookup by token hash (foundation for P5-2 completion; P5-1
        does NOT consume/complete tokens)."""
        row = self._conn.execute(
            "SELECT token_id, account_id, token_type, token_hash, expires_at, "
            "used_at, created_at FROM email_tokens WHERE token_hash = ?",
            (token_hash,)).fetchone()
        if row is None:
            return None
        return {"token_id": row[0], "account_id": row[1], "token_type": row[2],
                "token_hash": row[3], "expires_at": row[4], "used_at": row[5],
                "created_at": row[6]}

    def active_verification_tokens(self, account_id: str) -> int:
        return self._conn.execute(
            "SELECT COUNT(*) FROM email_tokens WHERE account_id = ? "
            "AND token_type = ? AND used_at IS NULL", (account_id, VERIFICATION)
        ).fetchone()[0]

    # --- bounded rate-limit foundation --------------------------------------
    def record_rate_attempt(self, subject_key: str, action: str, now_iso: str,
                            window_reset_iso: str, limit: int) -> bool:
        """Bounded store-backed counter. Increments the attempt count for
        (subject_key, action) within the current window; starts a fresh window
        when the stored one has expired (``now_iso >= expires_at``). Returns True
        when the attempt is WITHIN the limit, False when it exceeds it. Stores no
        raw password/token and no raw email (the caller passes a privacy digest)."""
        with self._conn:
            row = self._conn.execute(
                "SELECT window_start, attempt_count, expires_at FROM auth_rate_limits "
                "WHERE subject_key = ? AND action = ?", (subject_key, action)).fetchone()
            if row is None or now_iso >= row[2]:
                self._conn.execute(
                    "INSERT INTO auth_rate_limits (subject_key, action, window_start, "
                    "attempt_count, expires_at) VALUES (?, ?, ?, 1, ?) "
                    "ON CONFLICT(subject_key, action) DO UPDATE SET "
                    "window_start = excluded.window_start, attempt_count = 1, "
                    "expires_at = excluded.expires_at",
                    (subject_key, action, now_iso, window_reset_iso))
                return 1 <= limit
            new_count = row[1] + 1
            self._conn.execute(
                "UPDATE auth_rate_limits SET attempt_count = ? "
                "WHERE subject_key = ? AND action = ?", (new_count, subject_key, action))
            return new_count <= limit

    # --- lifecycle ----------------------------------------------------------
    def close(self) -> None:
        self._conn.close()
