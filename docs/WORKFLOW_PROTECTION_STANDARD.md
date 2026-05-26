# Workflow Protection Standard
Status: APPROVED

## Invariants
- INV-001: Level 0->1 requires REASONED evidence (F-011 gate)
- INV-002: BLOCK prevents all transitions
- INV-003: WARN allows transition, surfaced to user
- INV-004: Gap status forward-only OPEN->PARTIAL->RESOLVED
- INV-005: Every iteration produces audit log
- INV-006: assess/integrate/evaluate chain is atomic
- INV-007: Domain detection is stateless
- INV-008: Schema validation before state update
- INV-009: Read-only endpoints never mutate state
- INV-010: Production path import firewall

## Parity Suite
- Runner: PYTHONPATH=. python3 scripts/run_replay_benchmark_v2.py
- Excluded: TC-12 TC-16 (DR-006 QUARANTINED)
- Pass threshold: 23/23

## Rollback
1. git revert HEAD
2. Run F-011 gate
3. Run parity suite
4. File finding document
