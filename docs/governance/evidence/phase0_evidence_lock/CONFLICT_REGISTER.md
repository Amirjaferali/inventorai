# Phase 0 — Conflict Register

**Phase:** Phase 0 — Evidence Lock and Governance Reconciliation.
**Official tip:** `1d1385f2140be4e8ab1612ce07596a2170cfa0a0`.
**Mode:** Read-only. **No conflict is resolved here.** Each entry separates
`FACT` (repository-verifiable), `INFERENCE` (reviewer reasoning), and
`RECOMMENDATION` (options only — not an owner decision).

Severity legend: `CRITICAL · HIGH · MEDIUM · LOW · INFO`.
Summary: CRITICAL 0 · HIGH 0 · MEDIUM 2 (CR-2, CR-3) · LOW 2 (CR-1, CR-4) · INFO 3 (CR-5, CR-6, CR-7).

---

## CR-1 — Electronics-only authority vs domain-classification code — **LOW**

- **Source A:** `MVP_SCOPE_FREEZE.md` (`d63e783…`) — electronics/electrical-only, "Multi-domain orchestration" OUT OF SCOPE — FROZEN; `DOMAIN_SCOPE_OWNER_RESOLUTION_OPTION_B.md` (`653692279…`) L22–29 (preserve infra, restrict runtime to electronics until separately authorized).
- **Source B:** `engine/domain_rules.py` (`02374a2…`) L12–21 — `infer_domain` priority `["medical_device","electronics_electrical","mechanical","software"]`; `web/app.py` (`df4836b…`) L9 imports it; `DOMAIN_SCOPE_GOVERNANCE_INCONSISTENCY_REPORT.md` (`13264cd…`) L119–126 asserts the generic `/start` "assigns the result to `state.domain`" and a user "may be routed into `mechanical`/medical/software."
- **Runtime/code evidence (FACT):** `web/app.py` `/start` L383–447 — explicit `domain_confirm == DOMAIN_CONFIRM_VALUE` required (else `CONFIRMATION_REQUIRED_MESSAGE`, L391–392); `_has_strong_unsupported_evidence` → `UNSUPPORTED_DOMAIN_MESSAGE`, no session (branch L402; return L407); conflicting supported domain without sufficient lay-electrical corroboration → `MECHANISM_GUIDANCE_MESSAGE`, no session (L409–422); unknown classifier value → refuse (L423–426); on admission `state.domain = DOMAIN_CONFIRM_VALUE` (electronics_electrical, L434) — never the inferred non-electronics value. `tests/test_domain_gate_entry_ux.py` was inspected but not run. Existing committed tests support rejection-path behavior. No test-count claim is relied upon for CR-1.
- **INFERENCE:** `infer_domain`'s multi-domain values function only as a rejection/conflict signal; the active runtime admits only electronics_electrical sessions. This is **documentation-/stale-report-vs-latent-code**, not documentation-vs-active-runtime. The inconsistency report (Source B) describes a *superseded* `/start` and is itself now stale (see Stale Register).
- **Affected phase:** Phase 2 (governance/architecture reconciliation) and Phase 6 (multi-domain).
- **Blocks Phase 1?** No.
- **Owner decision required?** Yes (documentation/latent-code disposition).
- **RECOMMENDATION (options; not an owner decision):** (a) retain latent code, supersede the stale inconsistency report + add a clarifying code comment; (b) prune/guard the latent multi-domain priority list; (c) supersede ADR-001 to authorize multi-domain. Recommended: (a) in Phase 2; defer (b)/(c) to the multi-domain phase.

## CR-2 — Stale architecture document vs in-memory runtime — **MEDIUM**

- **Source A (FACT):** `docs/ARCHITECTURE_DECISION.md` (`cce03b3…`) L4 "Last Updated: 2025-05-17"; L277 "Database | Supabase (PostgreSQL + RLS)"; L278 "Auth | Supabase Auth … JWT, password reset — no custom auth"; L161 "All events are append-only."
- **Source B (FACT):** `web/app.py` (`df4836b…`) L4 "SESSION_STORE: in-memory, non-production, temporary"; L40 `SESSION_STORE = {}`; 20 `@app.route` decorators, none auth/DB.
- **INFERENCE:** the architecture document describes a Supabase/DB/Auth system that is not built; it contradicts the committed in-memory Flask runtime.
- **Affected phase:** Phase 2 (target-architecture definition), Phase 4 (persistence), Phase 5 (auth).
- **Blocks Phase 1?** No.
- **Owner decision required?** Yes.
- **RECOMMENDATION (options):** (a) mark `ARCHITECTURE_DECISION.md` HISTORICAL/SUPERSEDED; (b) rewrite to the current target architecture in Phase 2. Not resolved here.

## CR-3 — Product-identity correction activation ambiguity — **MEDIUM**

- **Source A (FACT):** `OWNER_PRODUCT_IDENTITY_CORRECTION.md` (`5768d31…`) L18–21 "PROPOSED until all activation conditions in §11 are satisfied. EFFECTIVE only upon … HEAD = origin/main and ahead/behind = 0 0"; §11 L331–354.
- **Source B (FACT):** `STRATEGIC_PRODUCT_VISION.md` (`6c2277f…`) L46–47 "GOVERNING EFFECT AMENDED … amended by the **active** Level 0 Owner Amendment"; `CLAUDE.md` (`4251e99…`) L11 lists it as mandatory read #2.
- **Branch evidence (FACT):** authoritative branch `feature/atomic-json-session-persistence` = `1d1385f2…`; `origin/main` = `0e89e4636399760965c9ff8086b465c90dbadf8e`; so `HEAD = origin/main` never holds on the feature branch.
- **INFERENCE:** later/higher sources treat the amendment as operative although its own literal §11 EFFECTIVE condition is unsatisfiable under the current feature-branch authority model — a genuine effective-vs-proposed ambiguity.
- **Affected phase:** Phase 1 (Owner Product Decisions — product identity).
- **Blocks Phase 1?** Does not block read-only Phase 0; Phase 1 identity decisions depend on it — recorded as **B — THE FIRST OWNER DECISION INSIDE PHASE 1** (sequencing only; see Open Owner Decisions OD-C).
- **Owner decision required?** Yes.
- **RECOMMENDATION (options):** (a) ratify effective status; (b) amend §11 to the current branch model; (c) formally keep PROPOSED. Not resolved here.

## CR-4 — Official vs main divergence + CLAUDE.md path drift — **LOW**

- **Source A (FACT):** `origin/feature/atomic-json-session-persistence` = `1d1385f2…`. **Source B (FACT):** `origin/main` = `0e89e4636399760965c9ff8086b465c90dbadf8e` (299 remote heads total). Roadmap §4 (`4251e99…`) records reconciliation as "a separate governed question."
- **Path-drift sub-item (FACT):** `CLAUDE.md` (`4251e99…`) "Document Authority Order" (heading L301; entries L304–307) names `MVP_SCOPE_FREEZE.md`/`GOVERNANCE_MODEL.md`/`DECISION_PROGRESSION_MODEL.md` by bare name (they resolve at repo root); `START_HERE` and `ARCHITECTURE_INDEX` (named in the review scope) are ABSENT at the tip.
- **INFERENCE:** main is intentionally behind; the path-drift is cosmetic/discoverability, not a functional break (files resolve at root).
- **Affected phase:** branch-strategy decision (OD-Q); path-drift → Phase 2.
- **Blocks Phase 1?** No.
- **Owner decision required?** Yes (branch strategy).
- **RECOMMENDATION (options):** (a) keep main intentionally behind; (b) plan a governed main reconciliation. Path drift corrected in Phase 2. Not resolved here.

## CR-5 — Plan header "candidate" vs CANONICAL status — **INFO**

- **FACT:** `PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md` (`4251e99…`) L3 "Draft revision: `v2 — owner review candidate`" coexists with L10 "Document status: `CANONICAL GOVERNANCE PLAN …`".
- **INFERENCE:** L3 is provenance (which revision), not a status claim; harmless.
- **Blocks Phase 1?** No. **RECOMMENDATION:** optional cleanup in a future doc pass. Not resolved here.

## CR-6 — Plan internal sequencing — **INFO (no conflict found)**

- **FACT:** `PLAN` §5 sequences persistence (Phase 4) before subscription (Phase 8 entry prereq L312–318) and Phase 6 (Multi-Domain) before Phase 7 (API, entry dependency L303). Internally consistent.
- **INFERENCE:** no conflict. Recorded as confirmed. **RECOMMENDATION:** none.

## CR-7 — Canonical plan vs higher anchors — **INFO (no conflict found)**

- **FACT:** `PLAN` §0.1 records subordination to higher anchors; no statement contradicts SPV/identity-correction/MVP-freeze.
- **INFERENCE:** plan is subordinate and consistent. **RECOMMENDATION:** none.
