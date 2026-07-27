# Phase 0 — Open Owner Decisions Register

**Phase:** Phase 0 — Evidence Lock and Governance Reconciliation.
**Official tip:** `1d1385f2140be4e8ab1612ce07596a2170cfa0a0`.
**Mode:** Read-only. Every recommendation below is marked
`RECOMMENDATION — NOT OWNER DECISION`. **No recommendation is converted into an
accepted decision.** Recording that a decision is "the first decision inside
Phase 1" is **sequencing only** and does not begin Phase 1.

---

### OD-A — Final public product name
- **Question:** What is the final public product name, given possible market/IP conflict?
- **Source basis:** `PLAN §3.1` L130–137; implementation evidence — 369 "InventorAI" occurrences across 139 tracked files (14 in `web/`; 0 in `engine/`; 287 in `docs/`).
- **Options / risks:** keep "InventorAI" (IP/market risk) · rename now (broad churn across ~14 web/ hits + docs) · defer + add branding indirection (low risk).
- **Dependencies:** OD-B. **Blocking phase:** Phase 1.
- `RECOMMENDATION — NOT OWNER DECISION`: defer final name; add centralized branding indirection.

### OD-B — Centralized branding indirection
- **Question:** Adopt `PRODUCT_NAME`/`PRODUCT_SHORT_NAME`/… indirection?
- **Source basis:** `PLAN §3.1` L137; no branding constant or base template exists (`web/templates/` has no `base.html`).
- **Options / risks:** adopt in Phase 3 (low) · later (rework across templates).
- **Dependencies:** OD-A. **Blocking phase:** Phase 3.
- `RECOMMENDATION — NOT OWNER DECISION`: adopt as a Phase 3 foundation.

### OD-C — Ratify product-identity correction effective status
- **Question:** Is `OWNER_PRODUCT_IDENTITY_CORRECTION.md` EFFECTIVE or still PROPOSED (CR-3)?
- **Source basis:** identity-corr §1 L18–21 / §11 L331–354; SPV L46–47 ("active"); CLAUDE.md L11; branch evidence main `0e89e463…` ≠ official `1d1385f2…`.
- **Options / risks:** ratify effective (removes ambiguity) · amend §11 to feature-branch model · keep PROPOSED (ambiguity persists).
- **Dependencies:** none. **Blocking phase:** Phase 1 (identity).
- `RECOMMENDATION — NOT OWNER DECISION`: treat as **B — THE FIRST OWNER DECISION INSIDE PHASE 1** (ratify / amend §11). Sequencing only; does not begin Phase 1.

### OD-D — Evidence/Provenance/Contribution/Ownership-Claims Register scope
- **Question:** Epistemic register only, or durable register; which capabilities?
- **Source basis:** `SPV §10` L342–356; FDC evidence model (`engine/decision_workspace.py`); `CAP-05/08/10/11` RECORDED-not-authorized; `PLAN §3.5` L162–170.
- **Options / risks:** epistemic-only (low) · durable (needs Phase 4 persistence).
- **Dependencies:** Phase 4. **Blocking phase:** Phase 1 → 4.
- `RECOMMENDATION — NOT OWNER DECISION`: epistemic register; durable form gated to Phase 4.

### OD-E — Legal-ownership / patentability disclaimers
- **Question:** Confirm the product documents claims but does not legally determine ownership/patentability.
- **Source basis:** `PLAN §3.5` L170; `SPV §5B`.
- **Options / risks:** confirm disclaimers (low) · weaken (legal exposure — reject).
- **Dependencies:** OD-D. **Blocking phase:** Phase 1.
- `RECOMMENDATION — NOT OWNER DECISION`: confirm "documents claims; no legal determination."

### OD-F — Multi-domain / cross-domain activation
- **Question:** Keep multi-domain deferred, or authorize?
- **Source basis:** `SPV` Principle 3; `ADR-001` (deferred indefinitely); `DOMAIN_SCOPE_OWNER_RESOLUTION_OPTION_B.md`; `PLAN §3.2`.
- **Options / risks:** keep deferred (low) · authorize (scope/safety risk; requires freeze amendment + replacement ADR + gates + tests + benchmark).
- **Dependencies:** CR-1. **Blocking phase:** Phase 6/9.
- `RECOMMENDATION — NOT OWNER DECISION`: keep deferred; design-for extensibility only.

### OD-G — IoT as domain and capability
- **Question:** Confirm IoT modeled as both a domain and a cross-domain capability.
- **Source basis:** `PLAN §3.4` L154–160.
- **Options / risks:** confirm dual model · shallow single category (rejected by plan).
- **Dependencies:** OD-F. **Blocking phase:** Phase 6/9.
- `RECOMMENDATION — NOT OWNER DECISION`: dual model; no shallow category.

### OD-H — Priority order of future domains
- **Question:** Confirm IoT → drone → renewable → other.
- **Source basis:** `PLAN §3.3` / §9 L320–333.
- **Options / risks:** confirm order · reorder.
- **Dependencies:** OD-F. **Blocking phase:** Phase 9.
- `RECOMMENDATION — NOT OWNER DECISION`: confirm as listed.

### OD-I — Persistence-before-paid-subscription sequencing
- **Question:** Confirm subscription is prohibited until durable persistence is formally closed.
- **Source basis:** `PLAN` Phase 8 entry prereq L312–318; Phase 4 hard rule.
- **Options / risks:** confirm hard rule (low) · relax (data-loss/commercial risk — reject).
- **Dependencies:** Phase 4/5. **Blocking phase:** Phase 8.
- `RECOMMENDATION — NOT OWNER DECISION`: confirm hard sequencing.

### OD-J — Account vs project vs claimed-inventor ownership model
- **Question:** Confirm the role model and that no role = legal ownership.
- **Source basis:** `PLAN` Phase 5 L280–286; `SPV` Principle 1.
- **Options / risks:** confirm role model · conflate roles with legal ownership (reject).
- **Dependencies:** Phase 5. **Blocking phase:** Phase 5.
- `RECOMMENDATION — NOT OWNER DECISION`: confirm; role ≠ legal ownership.

### OD-K — API exposure model + authentication/scopes
- **Question:** Confirm core→internal-service→versioned-API→adapter separation.
- **Source basis:** `PLAN §3.7` L180–186; Phase 7.
- **Options / risks:** confirm separation · couple external apps to core (reject).
- **Dependencies:** Phase 6. **Blocking phase:** Phase 7.
- `RECOMMENDATION — NOT OWNER DECISION`: confirm core→adapter separation.

### OD-L — Path N / Path T user exposure
- **Question:** Confirm UX targets Path N only; Path T (FORM T) stays blocked.
- **Source basis:** `PATH_N_CURRENT_EXECUTION_ANCHOR.md` (`runtime_integrated=false`); FORM T BLOCKED.
- **Options / risks:** Path N only (low) · expose Path T (blocked — reject).
- **Dependencies:** none. **Blocking phase:** Phase 3.
- `RECOMMENDATION — NOT OWNER DECISION`: Path N only; keep Path T blocked.

### OD-M — Unsupported-domain UX
- **Question:** Confirm honest reject/disclose for unsupported domains.
- **Source basis:** committed domain-gate (`web/app.py` L406–426); domain-gate increment.
- **Options / risks:** confirm reject/disclose · present unsupported as available (reject).
- **Dependencies:** OD-F. **Blocking phase:** Phase 3.
- `RECOMMENDATION — NOT OWNER DECISION`: confirm reject/disclose.

### OD-N — Commercial plan boundaries + non-interference
- **Question:** Confirm scoring/technical decisions stay independent of plan level.
- **Source basis:** `SPV §11` L360–382; `PLAN` L319 ("Progression scoring and technical decisions must remain independent of commercial plan level").
- **Options / risks:** confirm independence · let commerce influence scoring (reject).
- **Dependencies:** Phase 8. **Blocking phase:** Phase 8.
- `RECOMMENDATION — NOT OWNER DECISION`: confirm independence.

### OD-O — Evidence confidentiality & sharing
- **Question:** Confirm private-by-default + transcript lifecycle.
- **Source basis:** `PLAN §5A.2` L377–390; WS16-IR-104 (`/tmp` transcript, SP-2).
- **Options / risks:** private-by-default (low) · public/default-open (privacy risk — reject).
- **Dependencies:** Phase 4/5. **Blocking phase:** Phase 4/5.
- `RECOMMENDATION — NOT OWNER DECISION`: private-by-default + transcript lifecycle.

### OD-P — Production-readiness criteria
- **Question:** Define production-readiness/deployment criteria.
- **Source basis:** `PLAN` Phase 10 L335–339; WS16 registers (`DEMO_READY_WITH_LIMITATIONS`).
- **Options / risks:** define at Phase 10 (low) · earlier (premature).
- **Dependencies:** Phases 4–9. **Blocking phase:** Phase 10.
- `RECOMMENDATION — NOT OWNER DECISION`: define at Phase 10.

### OD-Q — Branch strategy / main reconciliation
- **Question:** Keep `main` intentionally behind, or reconcile?
- **Source basis:** CR-4; roadmap §4; main `0e89e463…` vs official `1d1385f2…`.
- **Options / risks:** keep behind (status quo) · governed reconciliation (coordination risk).
- **Dependencies:** none. **Blocking phase:** any future push-to-main / release.
- `RECOMMENDATION — NOT OWNER DECISION`: decide a governed reconciliation policy.

---

**Note:** OD-A…OD-Q are open questions for the owner. This register neither
answers them nor begins Phase 1. CR-3/OD-C is recorded as the recommended first
Phase 1 decision (sequencing only).
