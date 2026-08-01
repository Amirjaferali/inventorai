# InventorAI — Current Project State

**Purpose:** the concise current-state entry point for every agent. It is **not** a second
roadmap. For detail, see the canonical plan
(`docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`), the
append-only `ACTIVE_EXECUTION_ROADMAP.md`, and the accepted owner-decision evidence indexed
by `docs/governance/OWNER_DECISION_REGISTER.md`.
**Keep concise; refresh at each phase/increment boundary.**

---

## Authoritative pointers

- **Authoritative branch:** `feature/atomic-json-session-persistence`.
- **Live tip:** resolve from Git each session
  (`git rev-parse origin/feature/atomic-json-session-persistence`). Do **not** trust a
  prose-pinned SHA.
  - **Current authoritative branch tip (last independently verified):**
    `62ebf8f1a07e3c0f48e4637029d641d19c3f9b9e` (Merge PR #337 — Phase 3D governance-record
    synchronization) — the base on which the Phase 3E–3F governance-record synchronization candidate is
    prepared (candidate not yet reviewed/merged).
  - **Historical verified evidence tip:** `0330273b0d8b15fc66a285bcb9b866c6aa81b8e5`
    (PR #327 merge) — **historical evidence only; not the current tip.**
- **`main`:** `0e89e4636399760965c9ff8086b465c90dbadf8e` — STALE / UNRECONCILED / NOT authority.

## Phase and gate

- **Phase 1:** FORMALLY CLOSED. **Phase 2:** FORMALLY CLOSED (PR #325) and status-synchronized (PR #326).
- **Phase 3 (Product UX/UI foundation) — product-decision lane:** **Phase 3A FORMALLY CLOSED**;
  **Phase 3B product-decision scope FORMALLY COMPLETE AND CLOSED** (Phase 3B-1 D1–D4 and Phase 3B-2
  D5–D17 accepted and closed; the **Project Technology Profile** decision — the final proved residual —
  accepted; all 32 agenda items + owner notes A–F dispositioned). These were **owner-accepted decisions
  delivered outside the repository and not previously committed**; their accepted summaries and provenance
  are recorded (by reference/hash) in
  `docs/governance/evidence/phase3_owner_decisions/PHASE_3B_PRODUCT_DECISION_FORMAL_CLOSURE.md`
  (synchronized to committed governance via **PR #335**, merged and post-merge verified).
- **Phase 3C (low-fidelity, non-production UX direction): PRODUCT/UX DECISION FORMALLY ACCEPTED AND CLOSED**
  (owner verdict A; D1–D17 and PTP-D1…D12 preserved, not reopened); recorded in
  `docs/governance/evidence/phase3_owner_decisions/PHASE_3C_LOW_FIDELITY_UX_FORMAL_ACCEPTANCE_AND_CLOSURE.md`
  and synchronized to committed governance via **PR #336** (merged and post-merge verified).
- **Phase 3D (independent usability & accessibility review): INDEPENDENT REVIEW ACCEPTED AND CLOSED**
  (reviewer verdict B — passes with non-blocking observations; owner verdict A; zero blocking findings; no Phase 3C
  surface returned for correction). Findings P3D-N1…P3D-N9 adopted as **Phase 3E acceptance criteria** (P3D-N1 the
  Phase 3E entry criterion); P3D-N10 is governance housekeeping resolved by that synchronization. Recorded in
  `docs/governance/evidence/phase3_owner_decisions/PHASE_3D_INDEPENDENT_UX_REVIEW_FORMAL_ACCEPTANCE_AND_CLOSURE.md`
  and synchronized to committed governance via **PR #337** (merged and post-merge verified).
- **Phase 3E (owner acceptance of the exact UX design): EXACT UX DESIGN FORMALLY ACCEPTED AND CLOSED**
  (owner verdict A). Accepted implementation-neutral design of record: external package
  `inventorai_phase3e_exact_ux_design_package_corrected_v3.md`, SHA-256
  `52e6522e9e842e3e9a3250c1b0ba1e21d99b9d400099c0324da2f61cb0fab0cf` (v3 supersedes all earlier Phase 3E packages).
  Nine-step journey (revision as the post-Refine loop returning to Step 8, not a tenth step); 24 screens/patterns
  (29-field schema each); 69 transitions T01–T69 (17-field schema each; field 12 = Back from the resulting screen);
  44×44 CSS-px minimum interactive target; 768-px breakpoint with 320-px minimum comparison-panel width; Entry shows
  "Step 1 of 9" (P3D-N9=A); P3D-N1…P3D-N9 satisfied; PTP idea-level CORE-content/OPTIONAL-screen and FDC-001
  outside-output boundaries preserved. Authorized **exact design only** — no implementation, runtime, or tests.
  Recorded in `docs/governance/evidence/phase3_owner_decisions/PHASE_3E_EXACT_UX_DESIGN_FORMAL_ACCEPTANCE_AND_CLOSURE.md`.
- **Phase 3F (independent review of the Phase 3E exact UX design — review-only): INDEPENDENT REVIEW ACCEPTED AND
  FORMALLY CLOSED** (reviewer verdict B; owner verdict B — accept with non-blocking observations and close; **zero
  blocking findings**; accepted Phase 3E package SHA `52e6522e…` unchanged). The OWNER adopted Phase 3F as the
  independent review of the Phase 3E design; the canonical plan's earlier "Phase 3F — Bounded Implementation
  Increments" wording is reconciled by an append-only supersedence note (implementation increments remain a **separate
  future authorization**). Six non-blocking observations recorded (none blocking; no reopening; no SHA change):
  **P3F-NB1** committed-governance lag (resolved by this synchronization); **P3F-NB2** "no session created" terminology
  ambiguity; **P3F-NB3** unnamed S12 proceed CTA; **P3F-NB4** T24 net-effect / T65 host-surface notation;
  **P3F-NB5** dangling §8 reference; **P3F-NB6** earlier external artifact bodies unavailable in that session
  (session-specific inspection limitation only; hashes recorded; artifacts exist). P3F-NB2…NB5 are **not** silently
  fixed in the accepted package. Recorded in
  `docs/governance/evidence/phase3_owner_decisions/PHASE_3F_INDEPENDENT_EXACT_UX_REVIEW_FORMAL_ACCEPTANCE_AND_CLOSURE.md`.
  **IMPLEMENTATION / PHASE 3F IMPLEMENTATION INCREMENTS / PHASE 4: NOT AUTHORIZED / NOT STARTED** (each requires a
  separate explicit owner authorization).
- **Phases 4–10:** NOT STARTED / NOT AUTHORIZED.
- **Completed gate:** Audit-Disposition & Handover-Gap Canonicalization + Lean-Governance
  adoption — **FORMALLY CLOSED** (merged via PR #327, merge `0330273b`; independent review
  `B — PASS WITH NON-BLOCKING OBSERVATIONS`; owner ACCEPTED AS-IS; post-merge PASS).
- **Latest completed gate:** the current bounded **remediation program** — **FORMALLY
  CLOSED** (executable track COMPLETE; G-R01 CLOSED via PR #329/#330; DISC-007 CLOSED via
  PR #331 test reconciliation + PR #332 v1.0 validation hardening; last verified tip
  `239557e1` (PR #332 merge); repository-wide XPASS `0`; one governed ADR-003 xfail retained;
  deferred Domain Registry v1.0 rules FORMALLY DEFERRED — NOT SOLVED). This closes only the
  remediation program; **Phase 3 remains NOT AUTHORIZED**. See
  `docs/governance/evidence/phase3_owner_decisions/REMEDIATION_PROGRAM_FORMAL_CLOSURE.md`.
- **Lean Governance and Agent Continuity Protocol:** **MERGED AND EFFECTIVE** on the
  authoritative branch (this document, the Owner Decision Register, the Active Increment
  Contract, and the Handover Template are now the binding continuity inputs).
- **Current active work:** the **Phase 3E–3F governance-record synchronization** documentation candidate
  (the two closure records above + these status updates + the plan Phase-3F supersedence note + the append-only
  roadmap records) — **PENDING bounded independent review (Lean §5) and owner acceptance; no push/PR/merge performed
  or authorized**. (The Phase 3B, 3C, and 3D synchronizations are complete — merged via PR #335, PR #336, and PR #337
  respectively, all post-merge verified.) No implementation authority.
- **Next proposed gate (not started, not authorized here):** after this Phase 3E–3F synchronization is reviewed and
  accepted, any move toward **Phase 3F bounded implementation increments** (or Phase 4, WS17, or a Structured Technical
  Guidance workstream) requires a **separate explicit owner authorization** with separately bounded, tested, reviewed,
  accepted, merged, and verified contracts. **NEXT IMPLEMENTATION OR POST-PHASE-3 GATE: NOT AUTHORIZED / REQUIRES
  SEPARATE OWNER DECISION.** No implementation, exact/production build, runtime, or tests are authorized here.

## Product / runtime distinction

- **Product identity:** multi-domain and cross-domain idea-development platform.
- **Current experimental MVP runtime:** Electronics/Electrical only.
- **Product state:** `DEMO_READY_WITH_LIMITATIONS`. **Production ready:** NO. **Deployment authority:** NONE.
- **Historical implementation:** MATERIALLY CONFORMING (independent audit verdict
  `B — MATERIAL CONFORMANCE WITH DOCUMENTATION DRIFT`; see OD-T).

## Implemented capabilities (current)

- Deterministic engine (scoring, progression, gaps, safety signals) — transport-free core.
- Flask app; Path N guided journey; electronics/electrical admission gate; decision workspace;
  success-criteria; deliverable view; FDC-001 narrow canonical-JSON decision-record export.
- In-memory `SESSION_STORE` only.

## Not implemented / not authorized

- Durable persistence; accounts; authentication; authorization; billing/subscription.
- ACV (Approximate Concept Visualization); Direct Output Download (PDF); Email Delivery.
- Sponsors/themes; administrative notice; privacy-control implementation; full Arabic/RTL;
  accessibility; multi-domain runtime; Path T / FORM T (BLOCKED).
- Structured Technical Guidance — RESERVED / INACTIVE / separately authorized.

## Accepted limitations (honest, not waived)

End-to-end runtime invocation not certified; `main` stale/unreconciled; `/tmp` transcript
handling (Phase 4 remediation); `iot_electronics` latent/legacy (not loaded; future
separately authorized domain-activation workstream); durable persistence not implemented —
runtime remains in-memory (G-R02; Phase 4); narrow Arabic/RTL. Full register: OD-T and the
canonical plan. (The former `tests/test_domain_registry.py` ~31 failing baseline is RESOLVED
— DISC-007 CLOSED via the current bounded remediation program; suite `0 failed`, XPASS `0`;
deferred Domain Registry v1.0 hardening rules remain FORMALLY DEFERRED — NOT IMPLEMENTED —
NOT SOLVED; see the Remediation Program Formal Closure Record.)

## Active holds / forbidden work now

No implementation, UI, runtime, engine, schema, database, prompt/AI, tests-as-gates,
domain activation, ACV/Download/Email, sponsors/notice/privacy implementation, Arabic/RTL,
accessibility, Structured Technical Guidance, exact/production build, Phase 3F implementation increments, Phase 4,
WS17, main reconciliation, or PR merge is authorized by the current gate. (Phase 3A/3B product decisions, the
Phase 3C low-fidelity UX direction, the Phase 3D independent review, the Phase 3E exact UX design, and the Phase 3F
independent review of that design are all closed; the accepted Phase 3E design is implementation-neutral and
authorizes no build; any implementation increment requires a separate explicit owner authorization.)

## Open owner decisions

None blocking the current gate. The Phase 3B owner UX/product decisions staged in
`docs/governance/evidence/phase3_owner_decisions/PHASE_3B_OWNER_DECISION_AGENDA.md` are now **DECIDED and
CLOSED** (all 32 items + owner notes A–F dispositioned; D1–D17 + the Project Technology Profile accepted);
see `PHASE_3B_PRODUCT_DECISION_FORMAL_CLOSURE.md`. The Phase 3C low-fidelity UX direction is **ACCEPTED and CLOSED**
(see `PHASE_3C_LOW_FIDELITY_UX_FORMAL_ACCEPTANCE_AND_CLOSURE.md`), the Phase 3D independent review is **ACCEPTED and
CLOSED** (see `PHASE_3D_INDEPENDENT_UX_REVIEW_FORMAL_ACCEPTANCE_AND_CLOSURE.md`; P3D-N1…P3D-N9 adopted as Phase 3E
acceptance criteria), the Phase 3E exact UX design is **ACCEPTED and CLOSED** (see
`PHASE_3E_EXACT_UX_DESIGN_FORMAL_ACCEPTANCE_AND_CLOSURE.md`), and the Phase 3F independent review of that design is
**ACCEPTED and CLOSED** (see `PHASE_3F_INDEPENDENT_EXACT_UX_REVIEW_FORMAL_ACCEPTANCE_AND_CLOSURE.md`). The only open
owner decision is whether to authorize the next gate — **Phase 3F bounded implementation increments** (or a later
Phase 4 / WS17 / Structured Technical Guidance workstream) — which is **not** authorized here and requires a separate
explicit owner decision.
