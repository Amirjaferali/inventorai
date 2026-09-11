"""P4-1a — Durable-Store Proof (datastore-neutral record store + SQLite adapter).

A minimal, datastore-neutral durable record store with a Python standard-library
`sqlite3` reference adapter. It persists and restores the P4-0 record contract
(`engine.record_contract.ProjectRecordContract`) durably — surviving an explicit
connection close and reopen — with atomic writes, rollback, project-scoped
isolation, durability-safe identifiers for newly created records, verbatim
provenance, and fail-closed validation on load.

Governed by the merged P4-1a Increment Contract in
`docs/governance/ACTIVE_INCREMENT_CONTRACT.md` (G-P4-1A-DOC-01, PR #355).

Scope boundary (binding):
  * P4-1a (here): durable-store proof only — datastore/adapter/transactions/
    isolation/ids/close-reopen. Reuses the P4-0 record contract as the ONLY
    serialization/validation authority; it does not duplicate the domain model,
    create a competing schema, rewrite existing identifiers, manufacture
    accepted inputs, persist readiness as authoritative, or invent AI provenance.
  * P4-1b (NOT here): Flask/runtime integration (session creation/retrieval/
    submission/Keep-Refine, generic unavailable-session behaviour).
  * P4-2 (NOT here): deterministic replay, durable output records, stale-output
    invalidation, full re-evaluation.
  * Phase 5 (NOT here): accounts, authentication, ownership, authorization.

Provider-free and network-free. Introduces no new runtime dependency (stdlib
`sqlite3`). Capability/project identifiers are unpredictable lookup capabilities,
NOT authentication, ownership, or authorization.
"""
import dataclasses
import json
import sqlite3
import uuid
from contextlib import contextmanager
from typing import List, Protocol, runtime_checkable

from engine.record_contract import ProjectRecordContract, assertion_to_dict
from engine.idea_state import DISPOSITION_ANSWERED
from engine.requirement_quantity import (
    RequirementQuantity, validate_quantity_history, validate_new_quantity,
    active_quantities, classify_ledger_anchor, ANCHOR_ACTIVE,
    MAX_REQUIREMENT_QUANTITIES_PER_PROJECT,
    QUANTITY_INSERTED, QUANTITY_EXACT_REPLAY, QUANTITY_EVENT_IDENTITY_FIELDS,
)
# T2-E Option B: the owner-recorded, explicitly UNVERIFIED evidence reference.
# A separate durable row type, deliberately NOT an assertion record: assertion
# records are replayed as inventor answers by `engine.session_reconstruction`,
# and a reference must never be.
from engine.evidence_reference import (
    EvidenceReference, validate_reference_history, validate_new_reference,
    active_reference_for_anchor, REFERENCE_INSERTED, REFERENCE_EXACT_REPLAY,
    REFERENCE_EVENT_IDENTITY_FIELDS, MAX_EVIDENCE_REFERENCES_PER_PROJECT,
)


class StoreError(Exception):
    """Base class for durable-store failures."""


class ProjectNotFound(StoreError):
    """Raised when a project id is not present in the store."""


class ReferenceChainConflict(StoreError):
    """T2-E: the ONE-ACTIVE-CHAIN rule was violated — a root was proposed for
    an anchor that already has an active reference, a supersession named a row
    that is not this anchor's current head (a STALE HEAD between stage and
    confirm), or the stable event key already names a DIFFERENT event. An
    established refusal, decided before any row is written."""


class ReferenceCapExceeded(StoreError):
    """T2-E: the per-project evidence-reference cap was reached."""


class QuantityChainConflict(StoreError):
    """T2-A: a requirement-quantity append would violate the ONE-ACTIVE-CHAIN
    rule against the durable truth inside the write transaction (a second
    active row for an anchor, a supersession of a row that is absent, of
    another anchor, or already superseded — i.e. a stale quantity head).
    Nothing is written."""


class QuantityAnchorIneligible(StoreError):
    """T2-A: a NEW requirement-quantity event names an anchor that the DURABLE
    ledger does not currently hold as an eligible answered assertion anchor —
    it is withdrawn, invalid or inconsistent right now, whatever a retained
    live session still believes. Raised inside the write transaction; nothing
    is written. An exact replay of an already recorded event is resolved
    BEFORE this check and stays idempotent."""


class QuantityCapExceeded(StoreError):
    """T2-A: the project already holds MAX_REQUIREMENT_QUANTITIES_PER_PROJECT
    durable quantity rows. Enforced inside the write transaction; nothing is
    written."""


@runtime_checkable
class RecordStore(Protocol):
    """Datastore-neutral durable record-store interface (the abstraction
    boundary). The SQLite adapter below is one concrete implementation; a future
    PostgreSQL/other adapter can implement the same protocol without redesign."""

    def create_project(self, contract: ProjectRecordContract, project_id: str = ..., reconstruction_inputs: dict = ..., owner_account_id: str = ...) -> str: ...
    def append_record(self, project_id: str, record, idempotency_key: str = ...) -> None: ...
    def load_contract(self, project_id: str) -> ProjectRecordContract: ...
    def load_accepted_answer_evidence(self, project_id: str) -> tuple: ...
    def load_reconstruction_inputs(self, project_id: str) -> dict: ...
    def load_owner(self, project_id: str): ...
    def project_ids(self) -> List[str]: ...
    def project_ids_for_owner(self, owner_account_id: str) -> List[str]: ...
    def new_record_id(self) -> str: ...
    def ping(self) -> None: ...
    def close(self) -> None: ...
    # T2-A Quantified Requirements Slice 1 (additive; see the table note below).
    def new_quantity_id(self) -> str: ...
    def append_requirement_quantity(self, project_id: str, quantity) -> str: ...
    def load_requirement_quantities(self, project_id: str) -> tuple: ...
    def requirement_quantity_for_event_key(self, project_id: str, event_key: str): ...
    # T2-E Option B (additive; see the evidence_references table note below).
    def new_reference_id(self) -> str: ...
    def append_evidence_reference(self, project_id: str, reference) -> str: ...
    def load_evidence_references(self, project_id: str) -> tuple: ...
    def evidence_reference_for_event_key(self, project_id: str, event_key: str): ...


_SCHEMA = (
    """
    CREATE TABLE IF NOT EXISTS projects (
        project_id       TEXT PRIMARY KEY,
        idea_id          TEXT NOT NULL,
        contract_version TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS records (
        project_id TEXT NOT NULL,
        seq        INTEGER NOT NULL,
        record_id  TEXT NOT NULL,
        payload    TEXT NOT NULL,
        PRIMARY KEY (project_id, record_id),
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
    )
    """,
)

# P4-1b-2a (G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01, OPTION A): the SEPARATE durable
# idempotency identity. This is NOT the engine record_id (which stays the
# positional rec_N and is untouched here); it is an additive, nullable column
# plus a partial UNIQUE index that is the durable duplicate backstop for accepted
# answered submissions. Legacy/pre-amendment rows and every non-answer record
# carry a NULL idempotency_key and remain valid (mixed-state). Additive only: no
# column drop, no type change, no record_id rewrite.
_IDEMPOTENCY_COLUMN = "idempotency_key"
_IDEMPOTENCY_INDEX = (
    "CREATE UNIQUE INDEX IF NOT EXISTS records_idempotency_key_uq "
    "ON records (project_id, idempotency_key) "
    "WHERE idempotency_key IS NOT NULL"
)

# P4-2 Level-1 (G-P4-2-LEVEL1-IMPLEMENTATION-01, OPTION A): additive, nullable
# project-envelope reconstruction inputs, persisted ONLY at project creation and
# never mutated afterwards. They are the deterministic inputs a later read-only
# reconstruction needs (`engine.session_reconstruction`): the seed idea text, the
# confirmed domain, the path, and the exact supported engine/contract version.
# Legacy/pre-amendment projects carry NULL in all four columns and remain valid
# (mixed-state); reconstruction fails closed to Level-0 evidence for them.
# Additive only: no column drop, no type change, no rewrite of existing rows.
_RECONSTRUCTION_COLUMNS = (
    "seed_idea_text", "confirmed_domain", "recon_path", "engine_contract_version",
)

# P5-3 (G-P5-3-PROJECT-OWNERSHIP-ROUTE-AUTHORIZATION-IMPLEMENTATION-01): the
# accepted MINIMUM additive ownership model — a single nullable
# ``owner_account_id`` column on ``projects`` plus an index. Legacy/anonymous
# projects carry NULL (unowned, capability-accessed as before); an owned project
# carries the immutable ``account_id`` of its owner, assigned ATOMICALLY in the
# same INSERT that creates the project row (never a create-then-assign step). A
# hard SQLite FOREIGN KEY to ``accounts(account_id)`` is deliberately NOT added
# via ``ALTER TABLE ADD COLUMN`` (SQLite cannot add an inline FK that way, and the
# ``accounts`` table is owned by a SEPARATE store that may not exist when this
# store initialises) — the relationship is enforced at the application layer
# (ownership is only ever assigned from a validated authenticated ``account_id``).
# Additive only: no column drop, no type change, no existing row rewritten;
# rollback is disable-and-ignore. Single-owner MVP: no owner-transfer, no
# collaborators, no ownership table.
_OWNER_COLUMN = "owner_account_id"
_OWNER_INDEX = (
    "CREATE INDEX IF NOT EXISTS projects_owner_account_id_idx "
    "ON projects (owner_account_id)"
)

# T2-A Quantified Requirements Slice 1 (Owner-authorized bounded candidate): the
# ADDITIVE durable requirement-quantity history — the frozen Slice-1 data
# contract, one row per recorded quantity. It is a SEPARATE, project-scoped,
# INSERT-only history table, NOT a second ledger: it carries no disposition and
# no payload; each row names the accepted answered ledger record it quantifies
# (composite FOREIGN KEY to ``records``) and, on a correction, the quantity row
# it supersedes (composite self-referential FOREIGN KEY; forward edge only —
# prior rows are never rewritten). Every row carries the unique ``event_key``
# (the durable exact-replay identity) and the recording facts
# ``recorded_iteration`` / ``recorded_at`` (never part of identity). Relational
# integrity is enforced by SQLite (``PRAGMA foreign_keys = ON`` on every
# connection); the partial UNIQUE ``chain_root_uq`` allows exactly one chain
# root per anchor and ``supersedes_uq`` forbids forks, so a rooted, fork-free
# chain has exactly one active row per anchor at the database layer. The
# migration is ``CREATE ... IF NOT EXISTS`` — idempotent on a fresh and on an
# existing populated database, no column drop, no rewrite of any existing row;
# rollback is disable-and-ignore.
_QUANTITY_TABLE = "requirement_quantities"
_QUANTITY_SCHEMA = (
    """
    CREATE TABLE IF NOT EXISTS requirement_quantities (
        project_id             TEXT NOT NULL,
        quantity_seq           INTEGER NOT NULL,
        quantity_id            TEXT NOT NULL,
        anchor_record_id       TEXT NOT NULL,
        requirement_id         TEXT NOT NULL,
        quantity_kind          TEXT NOT NULL,
        value_text             TEXT NOT NULL,
        supersedes_quantity_id TEXT,
        event_key              TEXT NOT NULL,
        recorded_iteration     INTEGER NOT NULL,
        recorded_at            TEXT NOT NULL,
        PRIMARY KEY (project_id, quantity_id),
        FOREIGN KEY (project_id) REFERENCES projects(project_id),
        FOREIGN KEY (project_id, anchor_record_id)
            REFERENCES records(project_id, record_id),
        FOREIGN KEY (project_id, supersedes_quantity_id)
            REFERENCES requirement_quantities(project_id, quantity_id)
    )
    """,
    "CREATE UNIQUE INDEX IF NOT EXISTS requirement_quantities_event_key_uq "
    "ON requirement_quantities (project_id, event_key)",
    "CREATE UNIQUE INDEX IF NOT EXISTS requirement_quantities_seq_uq "
    "ON requirement_quantities (project_id, quantity_seq)",
    "CREATE UNIQUE INDEX IF NOT EXISTS requirement_quantities_supersedes_uq "
    "ON requirement_quantities (project_id, supersedes_quantity_id) "
    "WHERE supersedes_quantity_id IS NOT NULL",
    "CREATE UNIQUE INDEX IF NOT EXISTS requirement_quantities_chain_root_uq "
    "ON requirement_quantities (project_id, anchor_record_id) "
    "WHERE supersedes_quantity_id IS NULL",
    "CREATE INDEX IF NOT EXISTS requirement_quantities_anchor_idx "
    "ON requirement_quantities (project_id, anchor_record_id)",
)

# T2-E Option B — the owner-recorded, explicitly UNVERIFIED evidence reference.
# Additive and idempotent on a fresh database AND on an existing populated
# pre-T2E database; touches no existing table, column or row. Rollback is
# disable-and-ignore (stop reading the table), never a destructive drop.
#
# SQLite does NOT accept an inline `UNIQUE (...) WHERE ...` table constraint
# (verified: "near \"WHERE\": syntax error"), so each CONDITIONAL uniqueness
# rule is expressed as a standalone partial `CREATE UNIQUE INDEX ... WHERE ...`
# exactly as the merged T2-A and P4-1b-2a indexes already do:
#   * evidence_references_chain_root_uq  — ONE active root per anchor;
#   * evidence_references_supersedes_uq  — ONE successor per reference.
_REFERENCE_TABLE = "evidence_references"
_REFERENCE_SCHEMA = (
    """
    CREATE TABLE IF NOT EXISTS evidence_references (
        project_id              TEXT    NOT NULL,
        reference_seq           INTEGER NOT NULL,
        reference_id            TEXT    NOT NULL,
        anchor_record_id        TEXT    NOT NULL,
        source_identity         TEXT    NOT NULL,
        occurred_on             TEXT    NOT NULL,
        scope_text              TEXT    NOT NULL,
        limitation_text         TEXT    NOT NULL,
        claim_status            TEXT    NOT NULL,
        withdrawn               INTEGER NOT NULL DEFAULT 0,
        supersedes_reference_id TEXT,
        event_key               TEXT    NOT NULL,
        recorded_iteration      INTEGER NOT NULL,
        recorded_at             TEXT    NOT NULL,
        PRIMARY KEY (project_id, reference_id),
        FOREIGN KEY (project_id) REFERENCES projects(project_id),
        FOREIGN KEY (project_id, anchor_record_id)
            REFERENCES records(project_id, record_id),
        FOREIGN KEY (project_id, supersedes_reference_id)
            REFERENCES evidence_references(project_id, reference_id)
    )
    """,
    "CREATE UNIQUE INDEX IF NOT EXISTS evidence_references_event_key_uq "
    "ON evidence_references (project_id, event_key)",
    "CREATE UNIQUE INDEX IF NOT EXISTS evidence_references_seq_uq "
    "ON evidence_references (project_id, reference_seq)",
    "CREATE UNIQUE INDEX IF NOT EXISTS evidence_references_supersedes_uq "
    "ON evidence_references (project_id, supersedes_reference_id) "
    "WHERE supersedes_reference_id IS NOT NULL",
    "CREATE UNIQUE INDEX IF NOT EXISTS evidence_references_chain_root_uq "
    "ON evidence_references (project_id, anchor_record_id) "
    "WHERE supersedes_reference_id IS NULL",
    "CREATE INDEX IF NOT EXISTS evidence_references_anchor_idx "
    "ON evidence_references (project_id, anchor_record_id)",
)


class SqliteRecordStore:
    """Reference/MVP durable adapter over Python stdlib `sqlite3`.

    Not a permanent production-datastore commitment; the abstraction keeps other
    adapters possible. All operations are project-scoped; each mutation is a
    single atomic transaction (commit on success, full rollback on failure).
    """

    def __init__(self, path: str):
        # `path` is a real SQLite database file (durable) or ":memory:" (which
        # does NOT survive close — durability tests use a real file path in a
        # pytest tmp_path). No repository-tracked database file is used.
        self._path = path
        # ``isolation_level=None`` puts the connection in autocommit mode so EVERY
        # write goes through the explicit ``_write()`` transaction below, which
        # opens with ``BEGIN IMMEDIATE``. Taking the RESERVED write lock up front
        # (instead of the sqlite3 default DEFERRED transaction, which takes a
        # SHARED read lock first and only tries to upgrade to RESERVED on the first
        # write) removes the read->write upgrade deadlock AND makes each additive
        # migration's check-then-``ALTER`` atomic across connections — so
        # concurrently constructing several stores on one fresh database can no
        # longer race into ``duplicate column name`` / ``database is locked``.
        # sqlite3's default busy timeout still lets a second writer wait for the
        # lock rather than erroring. Single-writer serialization is SQLite's
        # inherent model and matches the P4 threaded=False single-process design;
        # atomicity, rollback, and the additive schema are all unchanged.
        self._conn = sqlite3.connect(path, isolation_level=None)
        self._conn.execute("PRAGMA foreign_keys = ON")
        with self._write():
            for stmt in _SCHEMA:
                self._conn.execute(stmt)
            self._migrate_idempotency(self._conn)
            self._migrate_reconstruction_inputs(self._conn)
            self._migrate_owner(self._conn)
            self._migrate_requirement_quantities(self._conn)
            self._migrate_evidence_references(self._conn)

    # --- write transaction (serialized; BEGIN IMMEDIATE) --------------------
    @contextmanager
    def _write(self):
        """A single durable write transaction. ``BEGIN IMMEDIATE`` takes the
        RESERVED write lock at the start (not lazily on the first write like the
        sqlite3 default DEFERRED transaction), so concurrent same-process writers
        queue cleanly on SQLite's single-writer lock instead of deadlocking on a
        read->write upgrade, and a guarded additive ``ALTER TABLE`` never races a
        sibling into ``duplicate column name``. Commit on success; FULL rollback on
        any error — atomicity is unchanged (the owner is still written in the same
        INSERT, and a failed write leaves no partial project/record)."""
        self._conn.execute("BEGIN IMMEDIATE")
        try:
            yield
            self._conn.execute("COMMIT")
        except BaseException:
            # Any failure — including a COMMIT that itself raises (e.g. a busy
            # timeout at commit) — must leave NO write lock held on this
            # connection. Roll back defensively (ignoring "no active transaction"
            # if the failure already ended it) and re-raise the original error.
            try:
                self._conn.execute("ROLLBACK")
            except sqlite3.OperationalError:
                pass
            raise

    # --- migration (additive, idempotent, forward + safe rollback) ----------
    @staticmethod
    def _has_idempotency_column(conn) -> bool:
        cols = [row[1] for row in conn.execute("PRAGMA table_info(records)").fetchall()]
        return _IDEMPOTENCY_COLUMN in cols

    def _migrate_idempotency(self, conn) -> None:
        """P4-1b-2a forward migration against the LIVE schema: additively add the
        nullable ``idempotency_key`` column and its partial UNIQUE index. Applied
        idempotently to existing populated databases (existing rows keep a NULL
        key). Rollback for this additive change is disable-and-ignore (stop
        reading/enforcing the key) rather than a destructive column drop, so no
        durable ``records``/``rec_N`` data is ever lost."""
        if not self._has_idempotency_column(conn):
            conn.execute("ALTER TABLE records ADD COLUMN idempotency_key TEXT")
        conn.execute(_IDEMPOTENCY_INDEX)

    def _migrate_reconstruction_inputs(self, conn) -> None:
        """P4-2 Level-1 forward migration against the LIVE schema: additively add
        the four nullable ``projects`` reconstruction-input columns. Applied
        idempotently to existing populated databases (existing project rows keep
        NULL in every new column, so they stay valid and simply fail closed to
        Level-0 evidence at reconstruction time). Rollback is disable-and-ignore
        (stop reading the columns) rather than a destructive column drop, so no
        durable project/record data is ever lost. Never rewrites existing rows."""
        cols = [row[1] for row in
                conn.execute("PRAGMA table_info(projects)").fetchall()]
        for column in _RECONSTRUCTION_COLUMNS:
            if column not in cols:
                conn.execute(f"ALTER TABLE projects ADD COLUMN {column} TEXT")

    def _migrate_owner(self, conn) -> None:
        """P5-3 forward migration against the LIVE schema: additively add the
        nullable ``owner_account_id`` column and its index. Idempotent (safe to
        re-run on an already-migrated database) and legacy-safe (existing project
        rows keep NULL ownership, preserving the capability-access behaviour).
        Rollback is disable-and-ignore (stop reading/enforcing ownership) rather
        than a destructive column drop, so no durable project/record data is ever
        lost and old code can ignore the additive column."""
        cols = [row[1] for row in
                conn.execute("PRAGMA table_info(projects)").fetchall()]
        if _OWNER_COLUMN not in cols:
            conn.execute("ALTER TABLE projects ADD COLUMN owner_account_id TEXT")
        conn.execute(_OWNER_INDEX)

    def _migrate_evidence_references(self, conn) -> None:
        """T2-E forward migration against the LIVE schema: additively create the
        ``evidence_references`` table and its indexes, including the two PARTIAL
        unique indexes that carry the conditional uniqueness rules (one active
        root per anchor; one successor per reference). Idempotent (``IF NOT
        EXISTS``) on a fresh database and on an existing populated pre-T2E
        database; touches no existing table, column or row. Rollback is
        disable-and-ignore (stop reading the table), never a destructive drop."""
        for stmt in _REFERENCE_SCHEMA:
            conn.execute(stmt)

    def _migrate_requirement_quantities(self, conn) -> None:
        """T2-A forward migration against the LIVE schema: additively create the
        ``requirement_quantities`` table and its indexes. Idempotent (``IF NOT
        EXISTS``) on a fresh database and on an existing populated pre-T2A
        database; touches no existing table, column or row. Rollback is
        disable-and-ignore (stop reading the table), never a destructive drop."""
        for stmt in _QUANTITY_SCHEMA:
            conn.execute(stmt)

    # --- identifiers --------------------------------------------------------
    def new_record_id(self) -> str:
        """A durability-safe, collision-safe identifier for a NEWLY created
        durable record (distinct from the P4-0 sequence form `rec_{n}`)."""
        return "rec-" + uuid.uuid4().hex

    # --- writes (atomic) ----------------------------------------------------
    def create_project(self, contract: ProjectRecordContract, project_id: str = None,
                       reconstruction_inputs: dict = None,
                       owner_account_id: str = None) -> str:
        """Atomically persist a project envelope + its accepted-input records.
        Existing serialized record identifiers are preserved exactly. A failure
        (e.g. a duplicate record_id) rolls back the whole write — no partial
        project or record survives. Records are persisted verbatim; validation
        is enforced on load (fail-closed), matching the record contract.

        ``reconstruction_inputs`` (P4-2 Level-1, OPTION A) is an OPTIONAL, additive
        dict carrying the deterministic read-only reconstruction inputs
        ``seed_idea_text`` / ``confirmed_domain`` / ``path`` / ``engine_contract_version``.
        When ``None`` (the exact pre-amendment behaviour) all four columns stay
        NULL and the project remains a legacy/Level-0 project. These values are
        written ONCE here at creation and are never mutated afterwards. The seed
        idea is sensitive user content: it is stored only in this project column,
        never duplicated into an ``AssertionRecord`` and never logged."""
        pid = project_id or uuid.uuid4().hex
        ri = reconstruction_inputs or {}
        with self._write():   # single transaction: commit on success, rollback on error
            # P5-3: ``owner_account_id`` is written HERE, in the SAME atomic INSERT
            # that creates the project row — there is no create-then-assign step,
            # so no window exists for a claim/visibility race. NULL preserves the
            # exact pre-P5-3 anonymous/legacy behaviour. Ownership is immutable
            # after creation (no reassignment method is exposed).
            self._conn.execute(
                "INSERT INTO projects "
                "(project_id, idea_id, contract_version, "
                " seed_idea_text, confirmed_domain, recon_path, engine_contract_version, "
                " owner_account_id) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (pid, contract.idea_id, contract.contract_version,
                 ri.get("seed_idea_text"), ri.get("confirmed_domain"),
                 ri.get("path"), ri.get("engine_contract_version"),
                 owner_account_id),
            )
            for seq, record in enumerate(contract.assertions):
                self._conn.execute(
                    "INSERT INTO records (project_id, seq, record_id, payload) "
                    "VALUES (?, ?, ?, ?)",
                    (pid, seq, record.record_id,
                     json.dumps(assertion_to_dict(record), sort_keys=True)),
                )
        return pid

    def load_reconstruction_inputs(self, project_id: str) -> dict:
        """P4-2 Level-1 — return the additive project-envelope reconstruction
        inputs for ``project_id`` as a dict
        (``seed_idea_text`` / ``confirmed_domain`` / ``path`` /
        ``engine_contract_version``), or ``None`` when the project is absent OR
        carries NULL in every reconstruction column (a legacy/pre-amendment
        project). Project-scoped; reads nothing across projects; never mutates.
        The caller (``engine.session_reconstruction``) treats ``None`` and any
        missing individual field as a fail-closed Level-0 condition."""
        row = self._conn.execute(
            "SELECT seed_idea_text, confirmed_domain, recon_path, "
            "engine_contract_version FROM projects WHERE project_id = ?",
            (project_id,),
        ).fetchone()
        if row is None:
            return None
        seed, domain, path, version = row
        if seed is None and domain is None and path is None and version is None:
            return None
        return {
            "seed_idea_text": seed,
            "confirmed_domain": domain,
            "path": path,
            "engine_contract_version": version,
        }

    # --- P5-3 ownership reads (project-scoped; never mutate) -----------------
    def load_owner(self, project_id: str):
        """Return ``(exists, owner_account_id)`` for ``project_id``:
        ``(False, None)`` when the project row is absent; ``(True, None)`` when it
        exists but is unowned (legacy/anonymous NULL owner); ``(True, "<acct>")``
        when it is owned. This is the single durable source of truth for the
        central authorization helper — ownership is NEVER inferred from the ``sid``
        capability, the signed cookie, or any client input."""
        row = self._conn.execute(
            "SELECT owner_account_id FROM projects WHERE project_id = ?",
            (project_id,)).fetchone()
        if row is None:
            return (False, None)
        return (True, row[0])

    def project_ids_for_owner(self, owner_account_id: str) -> List[str]:
        """Return the project_ids durably owned by ``owner_account_id`` (empty for
        a falsy/None owner). Scoped strictly to that owner — it can never return
        another account's projects or any NULL-owner project."""
        if not owner_account_id:
            return []
        return [r[0] for r in self._conn.execute(
            "SELECT project_id FROM projects WHERE owner_account_id = ? "
            "ORDER BY project_id", (owner_account_id,)).fetchall()]

    def append_record(self, project_id: str, record, idempotency_key: str = None) -> None:
        """Atomically append one accepted-input record to an existing project,
        preserving its identifier exactly and its append order (seq).

        ``idempotency_key`` (P4-1b-2a, OPTION A) is the SEPARATE durable
        idempotency identity — NOT the engine ``record_id``. When provided it is
        stored in the additive column and is subject to the partial UNIQUE index;
        a duplicate key therefore raises ``sqlite3.IntegrityError`` and the whole
        append rolls back (the durable duplicate backstop). It is never derived
        from, and never overwrites, ``record_id`` (which stays ``rec_N``). A
        ``None`` key preserves the exact pre-amendment behaviour."""
        with self._write():
            row = self._conn.execute(
                "SELECT COUNT(*) FROM projects WHERE project_id = ?", (project_id,)
            ).fetchone()
            if not row or row[0] == 0:
                raise ProjectNotFound(project_id)
            seq = self._conn.execute(
                "SELECT COALESCE(MAX(seq), -1) + 1 FROM records WHERE project_id = ?",
                (project_id,),
            ).fetchone()[0]
            self._conn.execute(
                "INSERT INTO records (project_id, seq, record_id, payload, idempotency_key) "
                "VALUES (?, ?, ?, ?, ?)",
                (project_id, seq, record.record_id,
                 json.dumps(assertion_to_dict(record), sort_keys=True),
                 idempotency_key),
            )

    def record_payload_for_idempotency_key(self, project_id: str, idempotency_key: str):
        """Return the stored payload dict for the record carrying
        ``idempotency_key`` under ``project_id`` (or ``None`` if absent). Used by
        the runtime's confirm-by-reload check (C3): on a duplicate-key append the
        runtime reloads and compares the accepted content before treating a retry
        as an idempotent no-op — it never auto-classifies an IntegrityError as a
        duplicate. Project-scoped; reads nothing across projects."""
        if idempotency_key is None:
            return None
        row = self._conn.execute(
            "SELECT payload FROM records "
            "WHERE project_id = ? AND idempotency_key = ?",
            (project_id, idempotency_key),
        ).fetchone()
        if row is None:
            return None
        return json.loads(row[0])

    # --- reads (project-scoped; fail-closed validation) ---------------------
    def load_contract(self, project_id: str) -> ProjectRecordContract:
        """Load one project's records (scoped by project_id) and rebuild a
        validated ProjectRecordContract. Unknown contract versions, unknown
        fields, invalid references, and supersession cycles are rejected on load
        (via the record contract) — fail-closed, never silently repaired."""
        proj = self._conn.execute(
            "SELECT idea_id, contract_version FROM projects WHERE project_id = ?",
            (project_id,),
        ).fetchone()
        if proj is None:
            raise ProjectNotFound(project_id)
        idea_id, contract_version = proj
        rows = self._conn.execute(
            "SELECT payload FROM records WHERE project_id = ? ORDER BY seq ASC",
            (project_id,),
        ).fetchall()
        envelope = {
            "contract_version": contract_version,
            "idea_id": idea_id,
            "assertions": [json.loads(payload) for (payload,) in rows],
        }
        return ProjectRecordContract.from_dict(envelope)   # validates; fail-closed

    def load_accepted_answer_evidence(self, project_id: str) -> tuple:
        """P4-1b-2b — bounded, READ-ONLY reconstruction of the durably persisted
        accepted-answer evidence for ONE project/session (`project_id == sid`), in
        the authoritative persisted order (store `seq`).

        Returns an immutable ``tuple`` of the existing `AssertionRecord` values
        whose disposition is `answered`, exactly as persisted — `record_id`
        preserved as `rec_N` (non-contiguous values are expected and valid, since
        only accepted-answer interactions are durably appended), ordered by the
        `seq` order established by ``load_contract``. This is accepted-answer
        EVIDENCE, not a resumable session: it reconstructs no next question,
        gaps, maturity, domain/path, transcript, last_result, or progression, and
        is NOT full deterministic replay (that is P4-2).

        Failure behaviour (deterministic, fail-closed, non-disclosing):
          * unknown/absent `project_id` -> the empty tuple `()` — the SAME result
            an existing empty project returns (no existence leak, no mutation, no
            enumeration);
          * malformed / unsupported-version / invalid-reference / cyclic durable
            content -> the canonical ``ContractError`` propagates from
            ``load_contract`` (fail closed; NO partial evidence; corruption is
            never silently converted into a valid empty history).

        Read-only: performs no write, append, repair, rehydration, or state
        progression; reuses the project-scoped ``load_contract`` read (no
        cross-project read, no ``project_ids()``); bounded linear over the loaded
        contract; logs nothing."""
        try:
            contract = self.load_contract(project_id)
        except ProjectNotFound:
            return ()
        return tuple(
            record for record in contract.assertions
            if record.disposition == DISPOSITION_ANSWERED
        )

    # --- T2-A requirement-quantity history (project-scoped; INSERT-only) ------
    _QUANTITY_COLUMNS = ("quantity_seq, quantity_id, anchor_record_id, "
                         "requirement_id, quantity_kind, value_text, "
                         "supersedes_quantity_id, event_key, recorded_iteration, "
                         "recorded_at")

    @staticmethod
    def _quantity_row_dict(row):
        (seq, qid, anchor, requirement_id, kind, value_text, supersedes, event_key,
         recorded_iteration, recorded_at) = row
        return {"quantity_seq": seq, "quantity_id": qid, "anchor_record_id": anchor,
                "requirement_id": requirement_id, "quantity_kind": kind,
                "value_text": value_text, "supersedes_quantity_id": supersedes,
                "event_key": event_key, "recorded_iteration": recorded_iteration,
                "recorded_at": recorded_at}

    def new_quantity_id(self) -> str:
        """A durability-safe, collision-safe identifier for a NEW quantity row
        (``qty-`` + 32 hex). Distinct from ``rec_N`` and ``rec-<hex>``."""
        return "qty-" + uuid.uuid4().hex

    def _quantity_rows(self, project_id: str):
        return [self._quantity_row_dict(row) for row in self._conn.execute(
            "SELECT " + self._QUANTITY_COLUMNS + " FROM requirement_quantities "
            "WHERE project_id = ? ORDER BY quantity_seq ASC", (project_id,)).fetchall()]

    def _ledger_records(self, project_id: str):
        """This project's COMPLETE durable ledger records — the anchor truth a
        quantity row must resolve against.

        ALL records are returned, not only the answered ones, because proving a
        genuine supersession needs the successor record that carries the
        durable forward ``supersedes`` edge, and that successor is not
        necessarily an answered record. Project-scoped and read-only; an
        unknown project yields the empty tuple, exactly like
        ``load_accepted_answer_evidence``."""
        try:
            return tuple(self.load_contract(project_id).assertions)
        except ProjectNotFound:
            return ()

    def is_same_quantity_event(self, stored, quantity) -> bool:
        """True iff a STORED row is the exact canonical event of ``quantity``
        (canonical identity fields only; the recording facts are never part of
        event identity)."""
        if stored is None or not isinstance(quantity, RequirementQuantity):
            return False
        return all(stored[name] == getattr(quantity, name)
                   for name in QUANTITY_EVENT_IDENTITY_FIELDS)

    def append_requirement_quantity(self, project_id: str, quantity) -> str:
        """Atomically append ONE requirement-quantity row for ``project_id`` and
        return the TRUTHFUL durable outcome token.

        Returns ``QUANTITY_EXACT_REPLAY`` when this project already holds the
        exact canonical event under the same stable ``event_key`` (resolved
        FIRST, before any chain-position classification, so a replay of a
        recorded event is never mis-reported as a new-write conflict), and
        ``QUANTITY_INSERTED`` when this call committed the row.

        ONE serialized transaction (``BEGIN IMMEDIATE``); commit on success,
        FULL rollback on any failure — nothing partial survives. INSIDE the
        transaction, against the durable truth:
          * the project must exist (``ProjectNotFound``);
          * the stable ``(project_id, event_key)`` is resolved first: an
            existing row that is the exact same canonical event is an
            idempotent replay; an existing row under the same key that is a
            DIFFERENT event is a conflict, never a silent success;
          * the project's EXISTING history is loaded and validated against the
            project's durable ledger assertions (``QuantityHistoryError`` on
            corruption — a write is never possible on top of a corrupt
            history, and an anchor that is not a valid answered assertion
            record of THIS project is corruption);
          * the per-project cap holds (``QuantityCapExceeded`` at
            MAX_REQUIREMENT_QUANTITIES_PER_PROJECT rows);
          * the ONE-ACTIVE-CHAIN rule holds (``QuantityChainConflict``): with
            ``supersedes_quantity_id`` set, that row must be this anchor's
            CURRENT active head; without it, the anchor must have no active
            row — so a stale quantity head between propose and confirm is
            refused here;
          * the PROPOSED canonical row is validated TOGETHER with the existing
            history, exactly as the durable history will read after the insert
            (``validate_new_quantity``), so a direct store caller cannot commit
            an invalid kind, a malformed generated identity, an inconsistent
            requirement identity, an invalid anchor relationship or any other
            invalid canonical row;
          * the row's ``quantity_seq`` is assigned here (next in sequence);
            the caller's value is ignored; ``recorded_iteration`` and
            ``recorded_at`` are persisted as given (generated once per event
            by the caller; never part of identity);
          * SQLite enforces the composite foreign keys (anchor record of THIS
            project; supersedes row of THIS project) and the UNIQUE event key.
        The stored ``value_text`` is the caller's already-normalized text;
        this method never re-interprets, logs or rewrites it. Nothing here
        repairs, deletes or reinterprets an existing durable row."""
        if not isinstance(quantity, RequirementQuantity):
            raise StoreError("quantity must be a RequirementQuantity")
        with self._write():
            row = self._conn.execute(
                "SELECT COUNT(*) FROM projects WHERE project_id = ?", (project_id,)
            ).fetchone()
            if not row or row[0] == 0:
                raise ProjectNotFound(project_id)
            # CR-4: resolve the stable event key BEFORE classifying chain
            # position. A recorded event replayed exactly is idempotent, not a
            # new-write conflict; a different event under the same key is a
            # conflict and is never treated as a success.
            stored = self.requirement_quantity_for_event_key(project_id, quantity.event_key)
            if stored is not None:
                if self.is_same_quantity_event(stored, quantity):
                    return QUANTITY_EXACT_REPLAY
                raise QuantityChainConflict("event key already names a different event")
            existing_rows = self._quantity_rows(project_id)
            assertions = self._ledger_records(project_id)
            # R1: a NEW event must name an anchor the DURABLE ledger holds as
            # currently eligible, inside this same serialized transaction. A
            # retained live session that still offers a withdrawn anchor, and a
            # proposal-time eligibility result that has since been overtaken by
            # a governed correction, are both overruled here: durable truth
            # controls and nothing is written. Historical rows recorded while
            # their anchor was still active keep their validity below.
            if classify_ledger_anchor(
                    assertions, quantity.anchor_record_id) != ANCHOR_ACTIVE:
                raise QuantityAnchorIneligible(
                    "anchor is not currently an eligible answered assertion")
            history = validate_quantity_history(existing_rows, assertions=assertions)
            if len(history) >= MAX_REQUIREMENT_QUANTITIES_PER_PROJECT:
                raise QuantityCapExceeded("per-project quantity cap reached")
            head = active_quantities(history).get(quantity.anchor_record_id)
            if quantity.supersedes_quantity_id is None:
                if head is not None:
                    raise QuantityChainConflict("anchor already has an active quantity")
            else:
                if head is None or head.quantity_id != quantity.supersedes_quantity_id:
                    raise QuantityChainConflict("stale or invalid supersession target")
                if head.requirement_id != quantity.requirement_id:
                    raise QuantityChainConflict("requirement id changes within a chain")
            seq = (history[-1].quantity_seq + 1) if history else 0
            validate_new_quantity(
                existing_rows, dataclasses.replace(quantity, quantity_seq=seq),
                assertions=assertions)
            self._conn.execute(
                "INSERT INTO requirement_quantities (project_id, " + self._QUANTITY_COLUMNS + ") "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (project_id, seq, quantity.quantity_id, quantity.anchor_record_id,
                 quantity.requirement_id, quantity.quantity_kind, quantity.value_text,
                 quantity.supersedes_quantity_id, quantity.event_key,
                 quantity.recorded_iteration, quantity.recorded_at))
        return QUANTITY_INSERTED

    def load_requirement_quantities(self, project_id: str) -> tuple:
        """Load and VALIDATE one project's requirement-quantity history in
        stored ``quantity_seq`` order; return the immutable validated tuple.

        Zero rows (including an unknown project — the same non-disclosing
        empty result ``load_accepted_answer_evidence`` gives) return ``()``.
        Structural corruption raises ``engine.requirement_quantity
        .QuantityHistoryError`` with NO partial history (fail closed, never
        silently repaired); storage failure propagates as the SQL error.
        Every row is validated against the project's DURABLE ledger assertions
        as well as against the other quantity rows, so an anchor that does not
        resolve to a valid answered assertion record of this project is
        corruption and fails closed here.

        Read-only; project-scoped; logs nothing."""
        rows = self._quantity_rows(project_id)
        if not rows:
            return ()
        return validate_quantity_history(
            rows, assertions=self._ledger_records(project_id))

    def requirement_quantity_for_event_key(self, project_id: str, event_key: str):
        """Return the stored quantity row (dict) carrying ``event_key`` under
        ``project_id``, or ``None``. Used by the runtime's confirm-by-reload
        check after a duplicate-key ``IntegrityError``: a replayed exact event
        is treated as an idempotent no-op ONLY when the stored content
        matches. Project-scoped; reads nothing across projects."""
        if event_key is None:
            return None
        row = self._conn.execute(
            "SELECT " + self._QUANTITY_COLUMNS + " FROM requirement_quantities "
            "WHERE project_id = ? AND event_key = ?", (project_id, event_key)).fetchone()
        return None if row is None else self._quantity_row_dict(row)

    # --- T2-E Option B: owner-recorded, explicitly UNVERIFIED evidence references
    _REFERENCE_COLUMNS = (
        "reference_seq, reference_id, anchor_record_id, source_identity, "
        "occurred_on, scope_text, limitation_text, claim_status, withdrawn, "
        "supersedes_reference_id, event_key, recorded_iteration, recorded_at")

    @staticmethod
    def _reference_row_dict(row):
        return {
            "reference_seq": row[0], "reference_id": row[1],
            "anchor_record_id": row[2], "source_identity": row[3],
            "occurred_on": row[4], "scope_text": row[5],
            "limitation_text": row[6], "claim_status": row[7],
            "withdrawn": bool(row[8]), "supersedes_reference_id": row[9],
            "event_key": row[10], "recorded_iteration": row[11],
            "recorded_at": row[12],
        }

    def _reference_rows(self, project_id: str):
        return [self._reference_row_dict(row) for row in self._conn.execute(
            "SELECT " + self._REFERENCE_COLUMNS + " FROM evidence_references "
            "WHERE project_id = ? ORDER BY reference_seq ASC",
            (project_id,)).fetchall()]

    def new_reference_id(self) -> str:
        """A durability-safe, collision-safe identifier for a NEW reference."""
        return "evref-" + uuid.uuid4().hex

    def is_same_reference_event(self, stored, reference) -> bool:
        """True iff a STORED row is the exact canonical event of ``reference``
        (canonical identity fields only; the recording facts — seq, iteration,
        timestamp, generated id — are never part of event identity)."""
        if stored is None or not isinstance(reference, EvidenceReference):
            return False
        return all(stored[name] == getattr(reference, name)
                   for name in REFERENCE_EVENT_IDENTITY_FIELDS)

    def evidence_reference_for_event_key(self, project_id: str, event_key: str):
        """The stored reference row (dict) carrying ``event_key`` under
        ``project_id``, or ``None``. This is the runtime's confirm-by-reload
        seam: after a duplicate-key ``IntegrityError``, or after an uncertain
        commit, the durable truth for the stable key is read back and compared
        before any outcome is reported. Project-scoped; reads nothing across
        projects."""
        if event_key is None:
            return None
        row = self._conn.execute(
            "SELECT " + self._REFERENCE_COLUMNS + " FROM evidence_references "
            "WHERE project_id = ? AND event_key = ?",
            (project_id, event_key)).fetchone()
        return None if row is None else self._reference_row_dict(row)

    def append_evidence_reference(self, project_id: str, reference) -> str:
        """Atomically append ONE evidence reference and return the TRUTHFUL
        durable outcome token.

        ``REFERENCE_EXACT_REPLAY`` when this project already holds the exact
        canonical event under the same stable ``event_key`` (resolved FIRST, so
        a replay is never mis-reported as a new-write conflict);
        ``REFERENCE_INSERTED`` when this call committed the row.

        ONE serialized transaction (``BEGIN IMMEDIATE``); commit on success,
        FULL rollback on any failure — nothing partial survives. INSIDE the
        transaction, against the durable truth:
          * the project must exist (``ProjectNotFound``);
          * the stable ``(project_id, event_key)`` is resolved first — the same
            canonical event is an idempotent replay, a DIFFERENT event under the
            same key is a ``ReferenceChainConflict``, never a silent success;
          * the project's EXISTING history is loaded and structurally validated
            (``EvidenceReferenceHistoryError`` on corruption — a write is never
            possible on top of a corrupt history);
          * the anchor must resolve to a currently ACTIVE answered assertion of
            THIS project through the canonical merged anchor classifier;
          * the per-project cap holds (``ReferenceCapExceeded``);
          * the ONE-ACTIVE-CHAIN rule holds (``ReferenceChainConflict``): with
            ``supersedes_reference_id`` set, that row must be this anchor's
            CURRENT head — so a STALE HEAD between stage and confirm is refused
            HERE, inside the transaction, not only at the token; without it,
            the anchor must have no reference yet;
          * the proposed row is validated TOGETHER with the existing history
            exactly as the durable history will read after the insert, so a
            direct store caller cannot commit an invalid canonical row;
          * ``reference_seq`` is assigned here (next in sequence); the caller's
            value is ignored; ``recorded_iteration`` / ``recorded_at`` persist
            as given and are never part of identity;
          * SQLite enforces the composite foreign keys (anchor record of THIS
            project; superseded row of THIS project), the UNIQUE event key, and
            the two PARTIAL unique indexes carrying the conditional rules.

        There is NO update path on this table: a change is a superseding row and
        a withdrawal is a superseding row. Nothing here repairs, deletes,
        rewrites or reinterprets an existing durable row, and no stored text is
        re-normalized or logged."""
        if not isinstance(reference, EvidenceReference):
            raise StoreError("reference must be an EvidenceReference")
        with self._write():
            row = self._conn.execute(
                "SELECT COUNT(*) FROM projects WHERE project_id = ?", (project_id,)
            ).fetchone()
            if not row or row[0] == 0:
                raise ProjectNotFound(project_id)
            stored = self.evidence_reference_for_event_key(
                project_id, reference.event_key)
            if stored is not None:
                if self.is_same_reference_event(stored, reference):
                    return REFERENCE_EXACT_REPLAY
                raise ReferenceChainConflict(
                    "event key already names a different event")
            history = validate_reference_history(
                [self._reference_from_row(r) for r in self._reference_rows(project_id)])
            if len(history) >= MAX_EVIDENCE_REFERENCES_PER_PROJECT:
                raise ReferenceCapExceeded(
                    "evidence-reference cap reached for this project")
            if classify_ledger_anchor(
                    self._ledger_records(project_id),
                    reference.anchor_record_id) != ANCHOR_ACTIVE:
                raise ReferenceChainConflict(
                    "anchor is not an active answered assertion of this project")
            head = active_reference_for_anchor(
                history, reference.anchor_record_id)
            if reference.supersedes_reference_id is None:
                if head is not None:
                    raise ReferenceChainConflict(
                        "anchor already has an active evidence reference")
            elif head is None or head.reference_id != reference.supersedes_reference_id:
                raise ReferenceChainConflict(
                    "superseded reference is not this anchor's current head")
            validate_new_reference(history, reference)
            seq = self._conn.execute(
                "SELECT COALESCE(MAX(reference_seq), -1) + 1 FROM "
                "evidence_references WHERE project_id = ?", (project_id,)
            ).fetchone()[0]
            self._conn.execute(
                "INSERT INTO evidence_references (project_id, "
                + self._REFERENCE_COLUMNS + ") "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (project_id, seq, reference.reference_id,
                 reference.anchor_record_id, reference.source_identity,
                 reference.occurred_on, reference.scope_text,
                 reference.limitation_text, reference.claim_status,
                 1 if reference.withdrawn else 0,
                 reference.supersedes_reference_id, reference.event_key,
                 reference.recorded_iteration, reference.recorded_at))
        return REFERENCE_INSERTED

    @staticmethod
    def _reference_from_row(row):
        return EvidenceReference(
            reference_id=row["reference_id"],
            reference_seq=row["reference_seq"],
            anchor_record_id=row["anchor_record_id"],
            source_identity=row["source_identity"],
            occurred_on=row["occurred_on"],
            scope_text=row["scope_text"],
            limitation_text=row["limitation_text"],
            claim_status=row["claim_status"],
            withdrawn=bool(row["withdrawn"]),
            supersedes_reference_id=row["supersedes_reference_id"],
            event_key=row["event_key"],
            recorded_iteration=row["recorded_iteration"],
            recorded_at=row["recorded_at"])

    def load_evidence_references(self, project_id: str) -> tuple:
        """Load and VALIDATE one project's evidence-reference history in stored
        ``reference_seq`` order; return the immutable validated tuple.

        Zero rows (including an unknown project — the same non-disclosing empty
        result ``load_accepted_answer_evidence`` gives) return ``()``.
        Structural corruption raises ``engine.evidence_reference
        .EvidenceReferenceHistoryError`` with NO partial history (fail closed,
        never silently repaired); storage failure propagates as the SQL error.

        Read-only; project-scoped; logs nothing."""
        rows = self._reference_rows(project_id)
        if not rows:
            return ()
        return validate_reference_history(
            [self._reference_from_row(r) for r in rows])

    def project_ids(self) -> List[str]:
        return [row[0] for row in
                self._conn.execute("SELECT project_id FROM projects").fetchall()]

    def ping(self) -> None:
        """PERF-01 — bounded READ-ONLY readability probe for an already-opened
        store. Answers only "is this database readable right now?".

        Emits exactly one ``SELECT 1 FROM projects LIMIT 1`` and discards the
        single optional row, so the work and the result cardinality stay bounded
        as the table grows — unlike ``project_ids()``, which collects every
        project id. An EMPTY table returns no row and is still healthy: success
        is signalled ONLY by returning ``None``, failure ONLY by the SQL/storage
        exception propagating to the caller's existing boundary. Performs no
        write, schema creation, migration, repair, cleanup, file creation,
        enumeration, user-content logging, or provider/network call, and
        discloses nothing about any project."""
        self._conn.execute("SELECT 1 FROM projects LIMIT 1").fetchone()

    # --- lifecycle ----------------------------------------------------------
    def close(self) -> None:
        self._conn.close()
