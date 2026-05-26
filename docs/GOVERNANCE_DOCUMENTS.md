# Governance Documents - Master Index
Status: APPROVED

## Governing Principles
P-01: Evidence Before Action. No production change without finding or ADR.
P-02: Regression Gate First. F-011 must pass before any production path commit.
P-03: Quarantine Do Not Delete. Unverifiable data is QUARANTINED not deleted.
P-04: Untracked Is Risk. Every session ends with git status review.
P-05: Scope Freeze Respect. DR-003 MVP Scope Freeze is active.
P-06: Domain-Agnostic Core. engine/ must remain domain-agnostic.
P-07: Honest Status. Never claim completion without git commit evidence.
P-08: Base64 Write Scripts Only. heredoc cat is prohibited.
P-09: Arabic Safety. Arabic strings must not appear in files processed by eval().
P-10: Phase Order Enforcement. Phase 6 cannot start until Phase 5 approved.

## Workflow Invariants Reference
See WORKFLOW_PROTECTION_STANDARD.md for full definitions.
INV-001 through INV-010 defined there.

## Domain Registry Contract
engine/domain_registry.py (Phase 6) must satisfy:
domains/<id>/domain.json
domains/<id>/system_prompt.md
domains/<id>/output_schema.json
Must produce identical output to hardcoded implementation for 23 non-quarantined fixtures.

## Change Control
Production path changes require:
1. Finding or ADR committed
2. F-011 gate 10/10 PASS
3. Parity suite 23/23 PASS
4. Commit message includes document reference

Phase gates:
Phase 4 to 5: Governance documents committed (this commit)
Phase 5 to 6: Migration Plan approved by owner
Phase 6 to 7: Registry passes 23/23 parity
Phase 7 to 8: Second domain added and tested

## Document Registry
WPS-001 docs/WORKFLOW_PROTECTION_STANDARD.md APPROVED
DRP-001 docs/DISASTER_RECOVERY_PLAN.md APPROVED
OBS-001 docs/OBSERVABILITY_ARCHITECTURE.md APPROVED
SEC-001 docs/SECURITY_ARCHITECTURE.md APPROVED
DRE-001 docs/DATA_RETENTION_POLICY.md APPROVED
CGP-001 docs/COST_GOVERNANCE_PLAN.md APPROVED
GOV-001 docs/GOVERNANCE_DOCUMENTS.md APPROVED
