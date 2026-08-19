# P10-BR1 — Local Restore Drill Evidence Record

**File path:** `docs/governance/evidence/phase10_p10_br1/P10_BR1_RESTORE_DRILL_EVIDENCE.md`
**Purpose:** durable evidence that one explicit, local, provider-neutral backup → validate → restore →
parity drill of the InventorAI durable SQLite datastore was executed and PASSED, with synthetic data only.
**Input contract:** none (evidence record; consumes `engine/backup_service.py` + both real stores).
**Output contract:** the 12 drill proof points below, faithfully recorded; no user data, no `.db` artifact.
**Prohibited:** this record must never be cited as production backup readiness, offsite backup, a retention
policy, or a substitute for the future infrastructure-gated production backup design.

**Gate:** `P10-BR1 — Durable-Database Backup & Restore Drill Increment` (Owner-authorized bounded
Phase-10 implementation gate). **Date:** 2026-08-19. **Base:** `56ba1044…` (PR #519 merge, authoritative).

## Drill protocol and result — PASS (12/12)

Executed in an isolated temporary directory, entirely outside the repository and outside the shared
local-development database path. Synthetic data only (`drill-user@example.test`). No generated `.db`
artifact was committed.

| # | Required proof | Result |
|---|---|---|
| 1 | Source test DB created at an explicit isolated path | PASS — `drill-source.sqlite` (fresh) |
| 2 | Representative durable data populated via REAL seams | PASS — 1 account (verified), 1 email token, 1 rate-limit row, commercial assignment + commercial-audit row, 1 owned project with records (created through the real web `/login` + `/start` routes) |
| 3 | Backup created | PASS — `backup_database()` (SQLite online-backup API) |
| 4 | Backup integrity verified | PASS — `PRAGMA quick_check` = `ok` |
| 5 | Source untouched | PASS — source file SHA-256 identical before/after backup |
| 6 | Restore target created separately | PASS — three distinct real paths (source / backup / target) |
| 7 | Restored DB integrity verified | PASS — `PRAGMA quick_check` = `ok` |
| 8 | Schema/table inventory matches | PASS — full `sqlite_master` parity; **15 durable tables** (derived live, not assumed): access_audit, accounts, api_credentials, auth_rate_limits, commercial_assignments, commercial_audit, commercial_usage, commercial_usage_idempotency, email_tokens, projects, provider_event_dedupe, provider_mapping, records, subscription_lifecycle_events, subscription_lifecycle_state |
| 9 | Row parity matches | PASS — per-table row counts equal for all 15 tables; `database_parity_report` mismatches = `[]` |
| 10 | Selected semantic records match | PASS — full account row (id/email-hash/status/epoch) equal; project owner tuple equal; accepted-answer evidence equal |
| 11 | Restored DB opens via normal repository stores | PASS — `SqliteAccountStore` + `SqliteRecordStore` opened on the restored file and served the reads above |
| 12 | No production/live path touched | PASS — drill used only its own isolated directory; the shared local-development DB file was neither created nor modified by the drill |

## Reproduction

The identical workflow is enforced continuously by the automated suite
`tests/test_p10_br1_backup_restore.py` (21 tests: creation, consistency-under-open-connections,
fail-closed missing/corrupt/same-path/collision handling, schema/row/semantic parity, repeatability,
empty-valid-DB roundtrip, no-data-exposure). The drill can be re-run at any time against any isolated
copy; it must never target the live application database as its restore destination.

## Boundaries (binding)

Local verified drill ONLY. This record creates and implies **no** production backup scheduling, offsite
storage, retention/deletion schedule, encryption design, provider selection, PSRR execution, or deployment
authorization. Production backup topology remains future, separately governed, infrastructure-dependent
work; backup handling under any data-rights/erasure regime remains subject to the open external legal
input (OD-DR1/OD-DR2 preserved unchanged).
