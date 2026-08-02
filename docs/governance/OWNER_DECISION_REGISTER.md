# InventorAI — Central Owner Decision Register

**Purpose:** a concise index of current owner decisions and active separate-authorization
requirements. It does **not** duplicate full decision evidence — each row points to the
committed evidence, which governs. Where a row and its evidence conflict, the evidence
governs. Append or supersede rows as owner decisions are accepted and committed.

`Impl. authority` = whether the decision grants implementation authority now (almost always
NONE at this stage). `Status` = current governing status. `Supersession` noted where applicable.

---

## Phase 1 owner decisions (all RESOLVED / ACCEPTED / MERGED; FORMALLY CLOSED)

| ID | Subject | Status | Phase/WS | Impl. authority | Evidence |
|---|---|---|---|---|---|
| OD-A | Final public product name deferred; `InventorAI` temporary working name | ACCEPTED | Brand gate | NONE | phase1_owner_decisions/OD-A_OD-B_NAMING_AND_BRANDING.md |
| OD-B | Centralized branding indirection (future Phase 3 foundation) | ACCEPTED | Phase 3 | NONE | phase1_owner_decisions/OD-A_OD-B_NAMING_AND_BRANDING.md |
| OD-C | Ratify substantive product identity; §11 amended to official-branch model | ACCEPTED | Phase 2 (RW-2) | NONE | phase1_owner_decisions/OD-C_PRODUCT_IDENTITY_RATIFICATION.md |
| OD-D / OD-E | Epistemic evidence register; no legal-ownership/patentability determination | ACCEPTED | Phase 4 | NONE | phase1_owner_decisions/OD-D_OD-E_EVIDENCE_REGISTER_AND_LEGAL_BOUNDARY.md |
| OD-F / OD-G / OD-H | Multi-domain deferred; MVP electronics-only; IoT→drone→renewable priority | ACCEPTED | Phase 6/9 | NONE | phase1_owner_decisions/OD-F_OD-G_OD-H_MULTI_DOMAIN_IOT_PRIORITY.md |
| OD-L / OD-M | Path N only exposed; unsupported domains honestly blocked | ACCEPTED | Phase 3 | NONE | phase1_owner_decisions/OD-L_OD-M_UX_EXPOSURE_AND_UNSUPPORTED_DOMAIN.md |
| OD-J / OD-O | Product role model; projects/evidence private by default | ACCEPTED | Phase 5/4 | NONE | phase1_owner_decisions/OD-J_OD-O_ACCOUNTS_AND_EVIDENCE_CONFIDENTIALITY.md |
| OD-I / OD-N | Persistence before paid subscription; plan-neutral evaluation | ACCEPTED | Phase 4/8 | NONE | phase1_owner_decisions/OD-I_OD-N_COMMERCIAL_SEQUENCING_AND_NON_INTERFERENCE.md |
| OD-K | Core/service/versioned-API/adapter separation | ACCEPTED | Phase 7 | NONE | phase1_owner_decisions/OD-K_API_EXPOSURE_MODEL.md |
| OD-Q | Authoritative branch remains feature/…; `main` stale/unreconciled | ACCEPTED | Main gate | NONE | phase1_owner_decisions/OD-Q_BRANCH_STRATEGY_MAIN_RECONCILIATION.md |
| OD-P | Production-readiness/deployment defined in Phase 10 only | ACCEPTED | Phase 10 | NONE | phase1_owner_decisions/OD-P_PRODUCTION_READINESS_CRITERIA.md |

## Phase 2 owner decisions (DURABLY AND FULLY FORMALLY CLOSED)

| ID | Subject | Status | Phase/WS | Impl. authority | Evidence |
|---|---|---|---|---|---|
| OD-R | Cross-application boundaries: sponsor recognition (A); administrative notice (B); privacy/trust (C) — boundaries only | ACCEPTED / durably closed | Phase 3+ | NONE | phase2_owner_decisions/OD-R_CROSS_APPLICATION_COMMUNICATION_SPONSORSHIP_PRIVACY_TRUST_BOUNDARIES.md |
| OD-S | Finite 12-condition Phase 2 closure criteria | ACCEPTED / durably closed | Phase 2 | NONE | phase2_owner_decisions/OD-S_PHASE_2_CLOSURE_CRITERIA.md |

## Phase 3-preparation owner decisions (ACCEPTED and MERGED via PR #327, merge `0330273b`)

| ID | Subject | Status | Phase/WS | Impl. authority | Evidence |
|---|---|---|---|---|---|
| OD-T | Audit disposition + handover-gap canonicalization (DISC-001…018) | ACCEPTED / MERGED (PR #327) | Phase 3 prep | NONE | phase3_owner_decisions/OD-T_AUDIT_DISPOSITION_AND_HANDOVER_GAP_CANONICALIZATION.md |
| OD-U | Deferred output & visualization: ACV, Direct Output Download, Email Delivery | ACCEPTED / MERGED (PR #327) | Phase 3/4/5+ | NONE | phase3_owner_decisions/OD-U_DEFERRED_OUTPUT_AND_VISUALIZATION_CAPABILITIES.md |

## Canonicalized future capabilities & active separate-authorization requirements

| Capability | Governing status | Phase allocation | Impl. authority | Evidence |
|---|---|---|---|---|
| Approximate Concept Visualization (ACV) | CANONICAL / carve-out; NOT implemented | Phase 3 UX (after auth); Phase 4/5 foundations; separate later impl. WS | NONE — LEVEL 1 | OD-U; MVP_SCOPE_FREEZE.md (bounded allowance); OD-T |
| Direct Output Download (PDF) | CANONICAL named capability; NOT implemented (distinct from FDC-001 JSON export) | Phase 3 UX; Phase 4 impl. | NONE | OD-U; OD-T |
| Email Delivery | CANONICAL named capability; NOT implemented | Phase 3 UX; Phase 4 persistence; Phase 5 accounts/verified email | NONE | OD-U; OD-T |
| Sponsor recognition / multiple sponsors / themes / colors | Boundary recorded (OD-R-A); design/impl deferred | Phase 3 design + separately authorized impl. | NONE | OD-R (A); PHASE_3B agenda |
| Administrative notice (configurable) | Boundary recorded (OD-R-B) | Phase 3 UX; Phase 4/5 for per-user/version | NONE | OD-R (B); PHASE_3B agenda |
| Privacy/confidentiality/user-trust communication + "idea" terminology (scoped) | Boundary recorded (OD-R-C) | Phase 3 layered UX; Phase 10 legal wording | NONE | OD-R (C); PHASE_3B agenda |
| Multi-domain / cross-domain identity | Identity accepted; runtime deferred | Phase 3 honest UX; Phase 6 foundation; Phase 9 activation | NONE | OD-F/G/H; PHASE_3B agenda |
| Structured Technical Guidance | RESERVED / INACTIVE | Separate explicit owner authorization required before any work | NONE — LEVEL 1 | CLAUDE.md; anchors |
| `main` reconciliation | PROHIBITED without a separate gate | Dedicated future gate | NONE — LEVEL 1 | OD-Q |

## Post-Phase-3 bounded implementation-gate owner decisions (each separately authorized, merged, post-merge verified, and formally closed)

The **Owner verdict** column records the letter verdict where it is directly evidenced in the gate's owner
authorization; where a letter verdict is not independently re-verified from inspectable PR evidence, the cell records
the verified closure status instead (see the PR #341 row).

Full merge SHAs verified directly from Git first-parent history on `feature/atomic-json-session-persistence`;
enumerated with full evidence in `phase3_owner_decisions/POST_PHASE_3_UX_IMPLEMENTATION_GATES_FORMAL_CLOSURE.md`.
No entry grants authorization beyond its own bounded gate.

| Gate | PR | Merge commit (full) | Owner verdict | Status | Impl. authority beyond the gate |
|---|---|---|---|---|---|
| Phase 3E–3F governance-record synchronization (documentation-only) | #338 | `a7a141ce7f25eab261e29a3e44930b76a9e7c1f4` | Accepted (letter not re-verified in this synchronization's evidence chain) | MERGED / POST-MERGE VERIFIED / CLOSED | NONE |
| G-IRB — Implementation-Readiness Baseline | #339 | `fa054abe8979d9f1fe63fe9ca3122d9ce9df7078` | B | MERGED / POST-MERGE VERIFIED / CLOSED | NONE |
| G-SC0 — Bounded Security Containment (R6/R16) | #340 | `94b6b9df61d655a9005599e1e18fe19de26e7338` | B | MERGED / POST-MERGE VERIFIED / CLOSED | NONE |
| G-PDSR — Lean §5A pre-delivery adversarial self-review amendment | #341 | `745aaaf77aaad838d418f597710194f61db3c98e` | Owner closure verified; letter verdict not independently re-verified from inspectable PR evidence; separate-session independent-review record not independently located | MERGED / POST-MERGE VERIFIED / CLOSED | NONE |
| G-UX-SHELL — shared application shell & accessibility/disclosure baseline | #342 | `43453ceb87936d3a041e6edcccc0e7a8f16237a7` | B | MERGED / POST-MERGE VERIFIED / CLOSED | NONE |
| G-UX-TRUST — temporary-session Data & Session trust surface (S15) | #343 | `cc71ab7acb39d9f772dbb1a347c78bc53f86beae` | B | MERGED / POST-MERGE VERIFIED / CLOSED | NONE |
| G-UX-ENTRY — existing entry-surface alignment | #344 | `41e51ba070c71e9a1ca1c351a680abb73d72204e` | B | MERGED / POST-MERGE VERIFIED / CLOSED | NONE |
| G-UX-GUIDED-LABEL — guided-answer-field label | #345 | `82cf45f94cf6a9701e10ad02c2f2d557add1ed55` | B | MERGED / POST-MERGE VERIFIED / CLOSED | NONE |

These gates are bounded, behavior-preserving readiness/security/governance and UX accessibility-and-disclosure
increments. No UX increment is currently active; the next gate requires **separate explicit owner authorization**.
**Phase 4, WS17, and STG remain NOT AUTHORIZED / NOT STARTED.** Source branches were preserved (not deleted) per
each gate's authorization.

**Not-yet-canonical rule:** any capability or decision appearing only in a handover or chat —
not in committed owner-decision evidence — is `NOT CANONICAL — REQUIRES OWNER DECISION` and
must be added here with evidence before implementation.
