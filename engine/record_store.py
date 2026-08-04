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
from typing import List, Protocol, runtime_checkable

from engine.record_contract import ProjectRecordContract, assertion_to_dict


class StoreError(Exception):
    """Base class for durable-store failures."""


class ProjectNotFound(StoreError):
    """Raised when a project id is not present in the store."""


@runtime_checkable
class RecordStore(Protocol):
    """Datastore-neutral durable record-store interface (the abstraction
    boundary). The SQLite adapter below is one concrete implementation; a future
    PostgreSQL/other adapter can implement the same protocol without redesign."""

    def create_project(self, contract: ProjectRecordContract, project_id: str = ...) -> str: ...
    def append_record(self, project_id: str, record) -> None: ...
    def load_contract(self, project_id: str) -> ProjectRecordContract: ...
    def project_ids(self) -> List[str]: ...
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
        self._conn = sqlite3.connect(path)
        self._conn.execute("PRAGMA foreign_keys = ON")
        with self._conn:
            for stmt in _SCHEMA:
                self._conn.execute(stmt)

    # --- identifiers --------------------------------------------------------
    def new_record_id(self) -> str:
        """A durability-safe, collision-safe identifier for a NEWLY created
        durable record (distinct from the P4-0 sequence form `rec_{n}`)."""
        return "rec-" + uuid.uuid4().hex

    # --- writes (atomic) ----------------------------------------------------
    def create_project(self, contract: ProjectRecordContract, project_id: str = None) -> str:
        """Atomically persist a project envelope + its accepted-input records.
        Existing serialized record identifiers are preserved exactly. A failure
        (e.g. a duplicate record_id) rolls back the whole write — no partial
        project or record survives. Records are persisted verbatim; validation
        is enforced on load (fail-closed), matching the record contract."""
        pid = project_id or uuid.uuid4().hex
        with self._conn:   # single transaction: commit on success, rollback on error
            self._conn.execute(
                "INSERT INTO projects (project_id, idea_id, contract_version) "
                "VALUES (?, ?, ?)",
                (pid, contract.idea_id, contract.contract_version),
            )
            for seq, record in enumerate(contract.assertions):
                self._conn.execute(
                    "INSERT INTO records (project_id, seq, record_id, payload) "
                    "VALUES (?, ?, ?, ?)",
                    (pid, seq, record.record_id,
                     json.dumps(assertion_to_dict(record), sort_keys=True)),
                )
        return pid

    def append_record(self, project_id: str, record) -> None:
        """Atomically append one accepted-input record to an existing project,
        preserving its identifier exactly and its append order (seq)."""
        with self._conn:
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
                "INSERT INTO records (project_id, seq, record_id, payload) "
                "VALUES (?, ?, ?, ?)",
                (project_id, seq, record.record_id,
                 json.dumps(assertion_to_dict(record), sort_keys=True)),
            )

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

    def project_ids(self) -> List[str]:
        return [row[0] for row in
                self._conn.execute("SELECT project_id FROM projects").fetchall()]

    # --- lifecycle ----------------------------------------------------------
    def close(self) -> None:
        self._conn.close()
