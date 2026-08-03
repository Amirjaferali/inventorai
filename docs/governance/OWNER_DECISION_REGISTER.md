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
| G-GOV-SYNC-01 — post-Phase-3 governance currency synchronization (documentation-only) | #346 | `6b375121648e08b882fcc2b475a5986f6a9508ef` | B (with non-blocking observation RR-1) | MERGED / POST-MERGE VERIFIED / CLOSED | NONE |
| G-UX-ANSWER-VALIDATION — guided empty-answer validation experience | #347 | `722cf1c5d9b1756503ba92b34d0938fca3d1b695` | B (non-blocking F-1, F-2) | MERGED / POST-MERGE VERIFIED / CLOSED | NONE |
| G-UX-SNAPSHOT-DECISION — temporary-session Keep/Refine post-output decision (classification A — entry-point-only refinement) | #348 | `115239ffc4b4f2f1a108aae498cb1bbf016bbf08` | B (owner + independent; 0 blocking; no code correction) | MERGED / POST-MERGE VERIFIED / CLOSED | NONE |

These gates are bounded, behavior-preserving readiness/security/governance and UX accessibility-and-disclosure
increments. No UX increment is currently active; the next gate requires **separate explicit owner authorization**.
**Phase 4, WS17, and STG remain NOT AUTHORIZED / NOT STARTED.** Source branches were preserved (not deleted) per
each gate's authorization.

## Post-Output AI-Assisted Specialist Refinement (AISR) owner decisions — ACCEPTED PRODUCT DIRECTION / IMPLEMENTATION NOT AUTHORIZED

Owner decisions **D-AISR-01 … D-AISR-10** were accepted (G-AISR-MATERIAL-DECISION, owner verdict **B**) and recorded
documentation-only via **G-AISR-DOC-01**. The **single canonical source of truth** is
`docs/governance/POST_OUTPUT_AI_ASSISTED_SPECIALIST_REFINEMENT_CANONICAL_DECISION.md` (which governs; this row does
not duplicate it). Summary: AISR is an `ACCEPTED FUTURE PRODUCT DIRECTION` only — `IMPLEMENTATION NOT AUTHORIZED`.
It grants **no** implementation authority and activates **no** phase or workstream.

| ID | Subject | Status | Impl. authority | Evidence |
|---|---|---|---|---|
| D-AISR-01 | Capability direction (Post-Output AI-Assisted Specialist Refinement) | ACCEPTED PRODUCT DIRECTION | NONE | AISR canonical record §4 |
| D-AISR-02 | Responsibility model (WS17 umbrella / STG bounded / refinement lane / engine authority / Phase 4–7) — directional; WS17 not defined, STG not expanded | ACCEPTED (directional) | NONE | AISR canonical record §4–§5 |
| D-AISR-03 | Material identity change → new independent project record (directional) | ACCEPTED (directional) | NONE | AISR canonical record §4, §7 |
| D-AISR-04 | Content-origin target vocabulary (9 values) — conceptual only | ACCEPTED (vocabulary) | NONE | AISR canonical record §4, §8 |
| D-AISR-05 | Open-ended refinement within operational/security/cost/lifecycle/provider controls | ACCEPTED | NONE | AISR canonical record §4, §9 |
| D-AISR-06 | Full deterministic re-evaluation mandatory after accepted material change; targeted partial prohibited (preserves D17) | ACCEPTED | NONE | AISR canonical record §4, §10 |
| D-AISR-07 | Phased dependency map — four numbered phases (Phase 4–7) + two protected workstreams (WS17, STG) + one cross-cutting integration lane (post-output refinement); seven distinct owners; governing map only | ACCEPTED (map only) | NONE | AISR canonical record §11 |
| D-AISR-08 | Non-forgetting governance model (one canonical record + matrix + minimal references) | ACCEPTED | NONE | AISR canonical record §14 |
| D-AISR-09 | Phase 3E artifact recovery required before exact UX amendment | ACCEPTED | NONE | AISR canonical record §16 |
| D-AISR-10 | Next action = G-AISR-DOC-01 documentation-only recording (not Phase 4 / WS17 / STG / provider / UX / code) | ACCEPTED | NONE | AISR canonical record §4 |

No AISR entry grants authorization beyond documentation recording. **Phase 4, Phase 5, Phase 6, Phase 7, WS17, and
STG remain NOT AUTHORIZED / NOT STARTED**; provider selection is NOT AUTHORIZED; exact UX is NOT AUTHORIZED (Phase 3E
artifact recovery required first). Each future obligation carries a stable identifier (`AISR-OBL-*`) in the canonical
record's dependency matrix and deferred-obligations section.

## Phase 4 (Durable Data and Evidence Foundation) entry owner decisions — PHASE 4 ENTRY DIRECTION ACCEPTED / IMPLEMENTATION NOT AUTHORIZED

Owner decisions **D-P4-01 … D-P4-10** were accepted (G-P4-ENTRY-DEFINITION, owner verdict **B**) and recorded
documentation-only via **G-P4-DOC-01**. The **single canonical source of truth** is
`docs/governance/PHASE_4_DURABLE_DATA_AND_EVIDENCE_ENTRY_DECISION.md` (which governs; this row does not duplicate it).
Summary: the Phase 4 entry direction (Lean minimum durable-data & evidence foundations) is **ACCEPTED** —
`PHASE 4 IMPLEMENTATION NOT AUTHORIZED`, `P4-0 IMPLEMENTATION NOT AUTHORIZED`. This concerns the Product-Foundation
Phase 4, distinct from the Path-N execution-lane "Phase 4 runtime integration".

| ID | Subject | Status | Impl. authority | Evidence |
|---|---|---|---|---|
| D-P4-01 | Minimum Phase 4 scope — Lean minimum | ACCEPTED | NONE | Phase 4 entry record §6 |
| D-P4-02 | Project-record & lifecycle foundation (project identity = data identity only, not account/ownership) | ACCEPTED | NONE | Phase 4 entry record §6 |
| D-P4-03 | Accepted-input & supersession (append-only; no silent overwrite; correction/supersession UI needs its own gate) | ACCEPTED | NONE | Phase 4 entry record §6 |
| D-P4-04 | Provenance model (extensible; implement subset now; AI_PROPOSED/USER_MODIFIED_AI_PROPOSAL not populated) | ACCEPTED (directional) | NONE | Phase 4 entry record §6, §11 |
| D-P4-05 | Full deterministic re-evaluation foundation (targeted partial prohibited; cached reload ≠ re-eval) | ACCEPTED | NONE | Phase 4 entry record §6, §12 |
| D-P4-06 | Retention/deletion/tombstone by data type (no blanket method; no over-retention) | ACCEPTED (directional) | NONE | Phase 4 entry record §6, §13 |
| D-P4-07 | Migration & backward compatibility (ephemeral sessions never claimed saved; legacy schema not adopted) | ACCEPTED | NONE | Phase 4 entry record §6, §14 |
| D-P4-08 | Security/isolation/transactions/failure minimums (no accounts/auth — Phase 5) | ACCEPTED | NONE | Phase 4 entry record §6, §15 |
| D-P4-09 | Phased P4-0…P4-4 direction (planning only; authorizes no increment) | ACCEPTED (directional) | NONE | Phase 4 entry record §6, §17 |
| D-P4-10 | Next action = G-P4-DOC-01 documentation-only recording (not P4-0 / Phase 4 / schema / migration / code) | ACCEPTED | NONE | Phase 4 entry record §6 |

No Phase 4 entry decision grants implementation authority. **Phase 4 implementation, P4-0, Phase 5, Phase 6, Phase 7,
WS17, STG, provider selection, and exact UX remain NOT AUTHORIZED.** Phase 4 obligations carry stable identifiers
(`P4-OBL-*`) in the canonical entry record. The AISR seven-owner model and decision D17 are preserved.

**Not-yet-canonical rule:** any capability or decision appearing only in a handover or chat —
not in committed owner-decision evidence — is `NOT CANONICAL — REQUIRES OWNER DECISION` and
must be added here with evidence before implementation.
