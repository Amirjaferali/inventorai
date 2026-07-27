# Phase 0 — Canonical Source Register

**Phase:** Phase 0 — Evidence Lock and Governance Reconciliation (of
`docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`).
**Repository:** `Amirjaferali/inventorai`
**Authoritative branch:** `feature/atomic-json-session-persistence`
**Official tip:** `1d1385f2140be4e8ab1612ce07596a2170cfa0a0` (PR #290 merge).
**Status:** `PHASE 0 OPEN — READ-ONLY DISCOVERY COMPLETED — REGISTER DOCUMENTATION PREPARED — NOT YET MERGED OR FORMALLY CLOSED`
**Mode:** Read-only discovery record. This register records repository truth; it
resolves no conflict, makes no owner decision, and activates no downstream work.

"Last relevant commit" = the last commit on official history (`1d1385f2…`) that
touched the path (`git log -1 --format=%H <tip> -- <path>`). Line ranges are
verified where a numeric range is given; `§-level` = governing section cited
(exact line not individually captured this gate).

| # | Path | Title | Doc ID | Authority | Status | Governing subject | Applicability | Superseding source | Last relevant commit | Conflicts/deps | Must-read | Section/lines |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `CLAUDE.md` | Current Repository Execution Authority + Refactor Governance Contract | — | Boot | ACTIVE | Boot order; engineering rules | Current | — | `4251e9977d96626b837d999e0b119f541decd752` | CR-4 (path drift); depends on all anchors | YES | L6–25 (boot list); L301–307 (Document Authority Order) |
| 2 | `docs/governance/ILT-002_GOVERNANCE_ANCHOR.md` | ILT-002 Governance Anchor | ILT-002 | Boot/epistemic | ACTIVE | No state reconstruction; absence=UNKNOWN | Current | — | `86d6839e4da7f3bf85275030fe2167bb9a1b2bdb` | — | YES | §0 L3–12; §7 L73–79 |
| 3 | `docs/governance/OWNER_PRODUCT_IDENTITY_CORRECTION.md` | Owner Product Identity Correction | Level 0 Owner Amendment | Level 0 | AMBIGUOUS (effective vs proposed) | Product identity (idea-development; cross-domain) | Treated operative | — | `5768d315e8bdf11eac8b639576dcd0232b88c514` | CR-3 | YES | §1 L16–26; §5 L163–170; §11 L331–354 |
| 4 | `docs/governance/STRATEGIC_PRODUCT_VISION.md` | Strategic Product Vision | v1.0 Final | Level 0 | CANONICAL (§1/2/3/5A governing-effect amended by #3) | Identity; MVP freeze; evidence/ownership; commercial preservation | Current | `OWNER_PRODUCT_IDENTITY_CORRECTION.md` (partial) | `6c2277ff95204d57f5c73e32540498d46f044b10` | CR-3 | YES | §1 banner L46–47; §8 L288–299; §10 L342–356; §11 L360–382 |
| 5 | `docs/governance/PATH_N_CURRENT_EXECUTION_ANCHOR.md` | Path N Current Execution Anchor | — | Level 1 anchor | ACTIVE | Path N state; §13 Deliverable-Stabilization gate | Current | — | `5f61bc4fa524c46555be717aac99970a089a3494` | — | YES | §7 L114–118; §13 L190–226 |
| 6 | `docs/governance/DUAL_PATH_PRODUCT_ANCHOR.md` | Dual Path Product Anchor | — | Consolidation | ACTIVE | Path N/T interpretation | Current | — | `31b34d89debcc9209c92c13c83e2767c2abb1b7a` | — | YES | §3 L27–59; §7 L101–109 |
| 7 | `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` | Active Execution Roadmap | — | Level 2 | ACTIVE (append-only) | Lane/status continuity | Current | — | `4251e9977d96626b837d999e0b119f541decd752` | CR-4 | YES | §2 L13–19; §3 L21–29; §4 (branch/main) |
| 8 | `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md` | Product Foundation and Commercial Readiness Remediation Plan | v2 | Governance plan | CANONICAL (merged PR #289; status-synced PR #290) | Phase 0–10 remediation sequence | Current | — | `4251e9977d96626b837d999e0b119f541decd752` | CR-5 (provenance) | YES | status L10–11; §5 phases L214–339; §14 L633–680 |
| 9 | `docs/governance/INVENTORAI_COMMERCIAL_DIFFERENTIATION_DIRECTION.md` | InventorAI Commercial Differentiation Direction | — | Strategic | ACTIVE — NON-ACTIVATING | Product direction (Technical Decision Workspace) | Current | — | `b4c5e8d4f23671d6d99d5295fa4e8db937e7f137` | — | YES | §0 (non-auth); §5 (first capability) |
| 10 | `docs/benchmarks/BICYCLE_BRAKE_LIGHT_COMPETITIVE_BENCHMARK.md` | Bicycle Brake-Light Competitive Benchmark | — | Evaluation | ACTIVE — NON-ACTIVATING (no run) | Product-value eval protocol | Current | — | `1b8e299979cc0059d8b73626e225d9442f50974f` | — | YES | §5–§6 |
| 11 | `docs/governance/DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md` | Deliverable Stabilization Remediation Plan | — | Governance plan | CANONICAL — CLOSED PROGRAM (WS1–16) | WS1–16 lifecycle (§15) | Historical/closed | — | `811258df4753b879482c8fa8f5c4a5d7ff965824` | — | Referenced | §15 rows L358–374 |
| 12 | `MVP_SCOPE_FREEZE.md` (repo root) | MVP Scope Freeze | — | Hard constraint | ACTIVE FREEZE | Electronics/electrical-only; in-memory storage | Current | — | `d63e783070991d42753ced2047b2da9fbb2dcd2e` | CR-1 | YES (authority order) | §-level (IN/OUT scope) |
| 13 | `GOVERNANCE_MODEL.md` (repo root) | Governance Model | — | Authority hierarchy | ACTIVE | Tiers/violations | Current | — | `51bbbf7046a256664945d3a393c32c7ca64263a5` | CR-4 (path drift) | YES (authority order) | §-level |
| 14 | `DECISION_PROGRESSION_MODEL.md` (repo root) | Decision Progression Model | — | Proposal | PROPOSED (not implemented) | Progression engine | Not implemented | — | `51bbbf7046a256664945d3a393c32c7ca64263a5` | — | Named | §-level |
| 15 | `ARCHITECTURE_GUARDRAILS.md` (repo root) | Architecture Guardrails | — | Level 1 | ACTIVE | No core domain branching; registry/packs | Current | — | `32f4e71c5cb3d1e40be9bd67d281b3a916bce7f7` | supports CR-1 refutation | Recommended | §1–§5 L11–104 |
| 16 | `docs/WORKFLOW_PROTECTION_STANDARD.md` | Workflow Protection Standard | — | Standard | ACTIVE | Protected workflow | Current | — | `79c9c5edce620adc548429316aa5670e0c963414` | — | Recommended | §-level |
| 17 | `docs/governance/DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md` | Domain Pack Governance Standard v1 | Level 1 | Level 1 | ACTIVE | Domain-pack extensibility | Current | — | `8beed12d1f0863dc3f048fe948262cc93f7d7b55` | CR-1 | For domain work | §1 L38–47; §7 gates |
| 18 | `docs/governance/DOMAIN_SCOPE_OWNER_RESOLUTION_OPTION_B.md` | Domain Scope Owner Resolution (Option B) | — | Owner decision | ACTIVE — IMPLEMENTATION NOT YET AUTHORIZED | Reserve infra; restrict runtime to electronics | Current | — | `653692279cb297d936df3a4b13b13cb72dc78697` | CR-1 | For domain work | L22–29; L73–77; L101–103 |
| 19 | `docs/governance/DOMAIN_SCOPE_GOVERNANCE_INCONSISTENCY_REPORT.md` | Domain Scope Governance Inconsistency Report | — | Report | STALE re runtime (see CR-1) | Reports superseded `/start` behavior | Historical | current `/start` gate (`web/app.py`) | `13264cd6339647789990afce2c0abf52d129ce7b` | CR-1 | Caution | L105 (date-only sequencing); L119–126 (old /start claim) |
| 20 | `docs/adr/ADR-001-domain-assignment-and-multi-domain-strategy.md` | Domain Assignment and Multi-Domain Strategy | ADR-001 | ADR | ACCEPTED — deferred indefinitely | Multi-domain deferral | Current until superseded | — | `a12791de7f3e826b2c62e7ed3c6e31f020b5dab0` | CR-1 | For domain work | §-level (deferral; preconditions) |
| 21 | `docs/ARCHITECTURE_DECISION.md` | Architecture Decision | — | Architecture | STALE / HISTORICAL (see CR-2) | Supabase DB/Auth FSM (unbuilt) | Does NOT match runtime | in-memory Flask reality (`web/app.py`) | `cce03b3589cc8227dbec8e30ad7f81ac273f7a7f` | CR-2 | Caution | L4 (date 2025-05-17); L161; L277–278 |
| 22 | `docs/governance/TECHNICAL_REALIZATION_EVIDENCE_AND_ARTIFACT_MODEL.md` | Technical Realization Evidence and Artifact Model | Level 2 contract | Level 2 contract | CANONICAL — APPROVED AND FINAL | Provenance/artifact axes | Current | — | `1ec35a617a1789e4bc1f8c3f5f3cc2b2273d2f0a` | — | For evidence work | §-level |
| 23 | `docs/governance/SUPPORTED_TECHNOLOGY_AND_SOURCE_OF_TRUTH_CONTRACT.md` | Supported Technology and Source-of-Truth Contract | Level 2 contract | Level 2 contract | CANONICAL — APPROVED AND FINAL | Promotion rules; attribution | Current | — | `1ec35a617a1789e4bc1f8c3f5f3cc2b2273d2f0a` | — | For evidence work | §4–§6; §8 L128–141 |
| 24 | `docs/governance/INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md` | InventorAI Capability Enrichment Register | CAP-05/08/10/11/12/13/14 | Register | CANONICAL — all entries RECORDED, NOT AUTHORIZED | Future capabilities | Current | — | `cb2ceb78fb3ee7423e68a4f378f7e14859c908bf` | — | For capability work | CAP entries (§3) |
| 25 | `docs/governance/STRUCTURED_INVENTION_DISCLOSURE_AND_PATENT_EXPORT_OWNER_DECISION.md` | Structured Invention Disclosure and Patent Export | Owner Decision | Owner decision | RESERVED — non-activating | Patent/disclosure export | Future | — | `313243fc539f9e0b9fd7ec129210343e10347809` | — | For Patent Export | binding non-claims (§-level) |
| 26 | `web/app.py` | InventorAI Web Interface | — | Runtime (Level 4 evidence) | ACTIVE (in-memory, non-production) | Routes; domain gate; session store | Current | — | `df4836bf1864e1abf84ee37ea80339115c17a0a2` | CR-1, CR-2 | Implementation truth | `SESSION_STORE` L4,L40; `/start` gate L383–447 |
| 27 | `engine/domain_rules.py` | Domain Rules / infer_domain | — | Runtime (Level 4 evidence) | ACTIVE | Domain inference; active rules | Current | — | `02374a2c8b698aa5e7ef5ce36bf035f22348bcfe` | CR-1 | Implementation truth | `infer_domain` L12–21 |
| 28 | `engine/domain_registry.py` | Domain Registry loader | — | Runtime (Level 4 evidence) | ACTIVE | Domain-pack registry load | Current | — | `7707de19aee300d66f6dfca4821e0e91af243cfc` | CR-1 | Implementation truth | `load_registry` §-level |
| 29 | `START_HERE` (any path) | — | — | — | **ABSENT — SOURCE NOT FOUND** | — | — | — | LAST RELEVANT COMMIT NOT APPLICABLE (path never existed at tip) | named in review scope | — | not present at `1d1385f2` |
| 30 | `ARCHITECTURE_INDEX` (any path) | — | — | — | **ABSENT — SOURCE NOT FOUND** | — | — | — | LAST RELEVANT COMMIT NOT APPLICABLE (path never existed at tip) | named in review scope | — | not present at `1d1385f2` |

All last-relevant commits are resolved to exact 40-character SHAs on official
history except rows 29–30, which are `ABSENT` (the paths do not exist at the
official tip; a last-relevant commit is therefore not applicable, stated
explicitly rather than approximated).
