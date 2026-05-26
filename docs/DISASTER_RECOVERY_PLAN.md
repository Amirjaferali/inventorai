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

## Scenario 3 - Broken Main Branch
RTO: 15min
1. git revert SHA
2. Run F-011 gate
3. Run parity suite

## Scenario 4 - Session Store Corruption
RTO: Immediate
SESSION_STORE is ephemeral by design. Restart Flask.

## Scenario 5 - Corrupt Replay Fixture
RTO: 1 hour
git checkout SHA -- tests/replay/cases/TC.json

## Scenario 6 - Deprecated Model F-013
RTO: 1 day
Do NOT use v1 benchmark. Use v2 exclusively.
F-013 requires owner approval.
