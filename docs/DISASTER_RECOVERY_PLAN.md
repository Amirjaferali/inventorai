# Disaster Recovery Plan
Status: APPROVED

## Scenario 1 - Codespace Reset
RTO: 30min | RPO: Last commit
1. Reopen Codespace
2. git log --oneline -5
3. Run F-011 gate
4. Re-generate lost untracked files
Prevention: Commit benchmark/results_20260520_074904.json (R-004)

## Scenario 2 - Claude API Unavailable
RTO: 0 (graceful) | RPO: N/A
1. Web layer catches HTTP errors
2. Return WARN verdict
3. No state changes during outage

## Scenario 3 - Broken Authoritative Branch
RTO: 15min
Authoritative branch: `feature/atomic-json-session-persistence` (NOT `main` —
`main` is stale/unreconciled per repository governance).
1. git revert SHA on the authoritative branch
2. Run F-011 gate
3. Run parity suite

## Scenario 4 - Session Store Corruption
RTO: Immediate
The in-memory SESSION_STORE (live progression sessions only) is ephemeral by
design: restart Flask.
Durable data is NOT ephemeral: accounts, projects, records, and audit/commercial
tables live in the SQLite database at INVENTORAI_DB_PATH and are NOT recovered
by a restart. For durable-database loss/corruption see Scenario 7.

## Scenario 5 - Corrupt Replay Fixture
RTO: 1 hour
git checkout SHA -- tests/replay/cases/TC.json

## Scenario 6 - Deprecated Model F-013
RTO: 1 day
Do NOT use v1 benchmark. Use v2 exclusively.
F-013 requires owner approval.

## Scenario 7 - Durable SQLite Database Loss / Corruption (P10-BR1)
RTO: minutes (local restore) | RPO: last backup taken
Primary persistence: one SQLite file (INVENTORAI_DB_PATH) holding every durable
table (accounts/auth/audit/commercial scaffolding + projects/records; inventory
derived live from sqlite_master, never assumed).
Capability (implemented, P10-BR1): `engine/backup_service.py`
- backup_database(source, dest): SQLite online-backup API; source opened
  read-only; fail-closed on missing/invalid source; NEVER a raw copy of a
  live database file; validated before finalization.
- validate_sqlite_database(path): PRAGMA quick_check + schema inventory,
  fail-closed.
- restore_database(backup, target): validates the backup first, restores to a
  SEPARATE explicit target; overwrite is explicit and guarded (no silent
  overwrite of an existing database).
- database_parity_report(a, b): full schema-object + per-table row-count
  parity (names/counts only, never contents).
Procedure:
1. Validate the most recent backup (validate_sqlite_database).
2. Restore to a NEW target path — never onto the live file blindly.
3. Verify: database_parity_report + open via the normal repository stores.
4. Point INVENTORAI_DB_PATH at the restored file only after verification.
Verified by: automated suite `tests/test_p10_br1_backup_restore.py` and the
evidenced local restore drill
`docs/governance/evidence/phase10_p10_br1/P10_BR1_RESTORE_DRILL_EVIDENCE.md`.
Boundaries: LOCAL, provider-neutral capability + drill ONLY. No production
backup scheduling, no offsite/cloud backup, no retention policy, no
encryption-at-rest redesign — those remain future, separately governed
infrastructure/legal-gated work. A verified local drill is NOT a production
backup posture.
