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
import json
import sqlite3
import uuid
from contextlib import contextmanager
from typing import List, Protocol, runtime_checkable

from engine.record_contract import ProjectRecordContract, assertion_to_dict
from engine.idea_state import DISPOSITION_ANSWERED


class StoreError(Exception):
    """Base class for durable-store failures."""


class ProjectNotFound(StoreError):
    """Raised when a project id is not present in the store."""


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
    def close(self) -> None: ...


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

    def project_ids(self) -> List[str]:
        return [row[0] for row in
                self._conn.execute("SELECT project_id FROM projects").fetchall()]

    # --- lifecycle ----------------------------------------------------------
    def close(self) -> None:
        self._conn.close()
