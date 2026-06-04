# PRE_ILT002_BASELINE_FREEZE

**Document ID:** PRE_ILT002_BASELINE_FREEZE
**Type:** Pre-Validation Baseline Record
**Status:** COMPLETE
**Date:** 2026-06-04
**Author:** Governance Manager
**Purpose:** Frozen baseline before ILT-002 first inventor-development
validation session. All future ILT-002 findings are attributable to
the platform as it exists at this baseline.

---

## SECTION 1 — REPOSITORY BASELINE

### 1.1 HEAD and origin alignment

HEAD:         140ad16
origin/main:  140ad16
Alignment:    SYNCHRONIZED

Commit: governance: record owner decision — current_stage=2 is intentional MVP scope

### 1.2 Working tree state

Untracked scratch files only (STEP2_INVENTORY_RAW.txt, write_handover.py, write_sr001.py).
No staged changes. No unstaged changes to tracked files.
Working tree is clean with respect to committed content.

### 1.3 Test suite status at baseline

WPS001:
  20 passed, 1 skipped, 3 warnings, 0 failed

Cascade regression suite:
  7 passed, 1 warning, 0 failed

Stage 3 evaluator suite:
  41 passed, 0 failed

Full test suite (python -m pytest tests/):
  196 passed, 31 FAILED, 1 skipped
  FAILED: tests/test_domain_registry.py (31 failures — see Section 1.4)

### 1.4 CRITICAL FINDING — test_domain_registry.py: 31 pre-existing failures

CODE TRUTH — PRE-EXISTING, NOT INTRODUCED IN CURRENT SESSION

Running tests/test_domain_registry.py in isolation produces 31 failures.
These failures were not visible in WPS001 because WPS001 runs only
tests/test_wps001_invariants.py.

Root Cause A (schema mismatch):
test_domain_registry.py expects iot_electronics as a registry key and
a schema with governance.source, governance.license, governance.owner, etc.
The actual registry contains electronics_electrical with a different schema.
The test file was written against an older schema version.

Root Cause B (validation rules not implemented):
Tests expect load_registry() to raise errors on missing governance fields,
invalid version formats, empty capability_id, etc.
The actual load_registry() loads permissively without these validations.

Governance status:
These are pre-existing test failures that existed before this baseline session.
They are not regressions introduced by the current work.
WPS001 was the official benchmark and it remains passing.

ILT-002 impact: NONE.
ILT-002 validates inventor development behavior, not domain registry schema.
These failures do not affect run_iteration(), question delivery, gap progression,
or any behavior ILT-002 observes.

Post-ILT-002 action required: Owner decision on whether test_domain_registry.py
should be updated to match current schema, or whether domain registry validation
should be implemented to satisfy the tests.
These 31 failures are classified as post-ILT-002 technical debt.

---

## SECTION 2 — FUNCTIONAL SCOPE BASELINE

### 2.1 Active capabilities (available to an inventor today)

Problem establishment (maturity_level=0): ACTIVE
Stage 2 gap cascade (MECH -> PF -> BA): ACTIVE
Stage 3 gap cascade (PMF -> AI -> EGA): ACTIVE
Generic fallback questions Stage 2: ACTIVE
Generic fallback questions Stage 3: ACTIVE (added 9b994b8)
Domain-specific questions electronics_electrical Stage 2: ACTIVE
AI advisor question augmentation: ACTIVE (advisory)
Response quality assessment assess_response(): ACTIVE
Gap status progression OPEN->PARTIAL->CLOSED: ACTIVE
Maturity advancement 0->1->2: ACTIVE
Stall detection: ACTIVE
Iteration logging IterationLog: ACTIVE
Domain detection infer_domain(): ACTIVE
Stage 3 evaluation observation-only stage3_evaluator.py: IMPLEMENTED, NOT INTEGRATED

### 2.2 Capabilities in governance but not implemented

Stage 3 evaluation integrated into run_iteration: NOT INTEGRATED
Conditional probes PMF-Q1-P1 etc: NOT IMPLEMENTED
Coherence questions COH-Q1/2/3: NOT IMPLEMENTED
Stage 3 exit criteria runtime check: NOT IMPLEMENTED
Transition Authorization OA-1 Hybrid: NOT IMPLEMENTED
Multi-session persistence: NOT IMPLEMENTED
Stage 3 domain-specific questions: NOT PRESENT in registry
Stage 1 as distinct current_stage value: INTENTIONALLY DEFERRED
Mode B archetype: NOT AUTHORIZED
Stage 4+: NOT AUTHORIZED

### 2.3 Implemented capabilities not exercised by ILT-002

stage3_evaluator.py: Not integrated into run_iteration()
deliverable_assembler.py: Not part of ILT-002 observation protocol
scoring.py: Not part of ILT-002 observation protocol
ai_advisor.py AI question generation: ILT-002 observes delivered questions not origin
infer_domain() domain detection: ILT-002 uses fixed domain per idea archetype

---

## SECTION 3 — CLAIM BASELINE

### 3.1 Can claim — supported by evidence

Deterministic progression architecture: evaluation gates are computed not AI-driven.
Domain-agnostic core engine: progression_loop.py contains no domain-specific branching.
Governance-controlled development process: 50 governance artifacts admitted.
Stage 2 complete end-to-end: problem establishment through boundary definition.
Stage 3 structurally reachable: cascade routing, question delivery, gap tracking functional.
Observation capability: stage3_evaluator.py can assess Stage 3 responses (not integrated).
Test coverage: WPS001 (20), cascade regression (7), evaluator suite (41) all passing.

### 3.2 Cannot yet claim — requires ILT-002 evidence

InventorAI improves inventors (requires ILT-002 S-1 + S-2 evidence)
Longitudinal inventor growth (requires multi-session evidence)
Cross-idea reasoning transfer (requires ILT-002 S-6 evidence)
Implementation orientation capability development (requires Stage 3 session evidence)
Unknown awareness development (requires AI-E3 session evidence)
Inventor Development Platform as operational reality (governance claim established;
  operational evidence is what ILT-002 will produce or fail to produce)

### 3.3 Claims requiring qualification

Stage 3 is operational: QUALIFIED ONLY.
  Stage 3 is structurally reachable and questions are delivered.
  However: evaluation not integrated, exit criteria not checked,
  transition authorization not implemented.

AI is advisory only: TRUE for progression decisions.
  assess_response() and evaluate_transition() are deterministic.
  ai_advisor.py influences question delivery text — boundary not tested end-to-end.

---

## SECTION 4 — RISK REGISTER REFRESH

### Technical Risks

TR-1 (HIGH): test_domain_registry.py 31 pre-existing failures
  Unclassified — stale tests or unimplemented validation logic.
  Action required post-ILT-002.

TR-2 (MEDIUM): stage3_evaluator.py not integrated
  Limits depth of ILT-002 Stage 3 evidence.
  Human annotation of SR-001 dimensions required without evaluator output.

TR-3 (LOW): iot_electronics schema_version=None
  Pre-existing. 1 skipped test in WPS001. Not a runtime blocker.

### Measurement Risks

MR-1 (HIGH): Observer bias without behavioral anchors
  Documented in ILT-002A. Self-correction, ownership depth, transfer of
  reasoning, and S-6 all require human judgment.
  Mitigation: ILT-002A evidence controls mandatory before execution.

MR-2 (MEDIUM): No persistence infrastructure
  Multi-session continuity requires manual session logs.
  SR-001 longitudinal dimensions cannot be measured from engine state alone.

MR-3 (LOW): assess_response() heuristic limitations
  Sophisticated vocabulary without causal reasoning could classify as REASONED.
  Creates ceiling on what engine can objectively confirm.

### Strategic Risks

SR-1 (HIGH): Platform may be Hybrid System not Inventor Development Platform
  ILT-002 is designed to test this directly.
  The risk is not campaign failure — it is honest Hybrid System evidence
  requiring strategic remediation.

SR-2 (MEDIUM): Stage 3 evaluation gap creates measurement ceiling
  stage3_evaluator.py not integrated limits precision of Stage 3 findings.
  SR-001 dimensions are observable without evaluator but with less structure.

SR-3 (LOW): Domain expansion pressure post-ILT-002
  After results, pressure to expand domains as response to Hybrid System finding.
  Domain expansion does not address inventor development capability.

---

## SECTION 5 — VALIDATION READINESS STATEMENT

Single biggest reason ILT-002 could fail to produce trustworthy conclusion:

OBSERVER BIAS WITHOUT BEHAVIORAL ANCHORS (MR-1)

Evidence: ILT-002's most important signals — self-correction, transfer of
reasoning, and S-6 — are all reviewer-dependent. Without behavioral anchors
(Revision Marker Protocol, Emergence Timing Protocol, Specificity Test,
Newness Marker Protocol from ILT-002A), two reviewers observing the same
sessions could reach different verdicts.

A single reviewer without anchors is vulnerable to confirmation bias.
The reviewer already knows the platform's intended identity.
Ambiguous evidence could be classified as positive by a believing reviewer.

This is the documented failure mode of outcome measurement in educational
technology research.

Mitigation available and not yet implemented:
ILT-002A Section 3.2 behavioral anchors.
ILT-002A Section 6 hardening protocols.
These must be documented in the execution guide before any session begins.

Second-largest risk: TR-2 — stage3_evaluator.py not integrated.
This limits Stage 3 evidence precision but does not invalidate the campaign.

---

## SECTION 6 — FROZEN BASELINE SUMMARY

Baseline commit:    140ad16
Baseline date:      2026-06-04
WPS001:             20 passed / 0 failed
Cascade suite:      7 passed / 0 failed
Evaluator suite:    41 passed / 0 failed
Full suite:         196 passed / 31 failed (test_domain_registry pre-existing debt)
Governance artifacts: 50 committed in docs/governance/
Stage 3 questions:  Admitted and active
Stage 3 evaluator:  Implemented, not integrated
Transition auth:    Governance only, not implemented
ILT-002 readiness:  READY WITH EVIDENCE CONTROLS (per ILT-002A)
Pre-existing debt:  test_domain_registry.py 31 failures — post-ILT-002 action required

Attestation:
This baseline represents the repository state as of 2026-06-04 HEAD 140ad16.
Any ILT-002 findings are attributable to the platform as it exists at this commit.
Future modifications to engine behavior, question content, or progression logic
require a new baseline freeze before additional validation sessions.

---

*This document is produced to be accurate, not reassuring.*
*The 31 test_domain_registry.py failures are recorded as known pre-existing debt, not concealed.*
*The platform is ready for ILT-002 execution with the evidence controls defined in ILT-002A.*
