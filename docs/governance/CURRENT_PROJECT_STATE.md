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
    `115239ffc4b4f2f1a108aae498cb1bbf016bbf08` (Merge PR #348 — G-UX-SNAPSHOT-DECISION, the latest closed
    bounded post-Phase-3 implementation gate) — always re-resolve the live tip from Git per the rule above.
  - **Prior recorded tip (historical):** `62ebf8f1a07e3c0f48e4637029d641d19c3f9b9e` (Merge PR #337 —
    Phase 3D governance-record synchronization); superseded by PRs #338–#348 (see the Phase-and-gate section).
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
  deferred Domain Registry v1.0 rules FORMALLY DEFERRED — NOT SOLVED). See
  `docs/governance/evidence/phase3_owner_decisions/REMEDIATION_PROGRAM_FORMAL_CLOSURE.md`.
- **Post-Phase-3 bounded implementation gates — ALL MERGED, POST-MERGE VERIFIED, AND FORMALLY CLOSED**
  (each separately owner-authorized, merged via "Create a merge commit", post-merge verified, and formally closed;
  separate-session independent review is recorded in the respective owner authorizations for these gates, **except
  PR #341 — G-PDSR** — for which merge, post-merge verification, and owner closure are verified, but a separate-session
  independent-review record and a letter verdict were not independently located from inspectable PR evidence):
  **PR #338** Phase 3E–3F governance-record synchronization (merge `a7a141ce7f25eab261e29a3e44930b76a9e7c1f4`);
  **PR #339** G-IRB Implementation-Readiness Baseline (merge `fa054abe8979d9f1fe63fe9ca3122d9ce9df7078`);
  **PR #340** G-SC0 Bounded Security Containment R6/R16 (merge `94b6b9df61d655a9005599e1e18fe19de26e7338`);
  **PR #341** G-PDSR Lean §5A pre-delivery adversarial self-review amendment (merge `745aaaf77aaad838d418f597710194f61db3c98e`);
  **PR #342** G-UX-SHELL shared application shell & accessibility/disclosure baseline (merge `43453ceb87936d3a041e6edcccc0e7a8f16237a7`);
  **PR #343** G-UX-TRUST temporary-session Data & Session trust surface S15 (merge `cc71ab7acb39d9f772dbb1a347c78bc53f86beae`);
  **PR #344** G-UX-ENTRY existing entry-surface alignment (merge `41e51ba070c71e9a1ca1c351a680abb73d72204e`);
  **PR #345** G-UX-GUIDED-LABEL guided-answer-field label (merge `82cf45f94cf6a9701e10ad02c2f2d557add1ed55`);
  **PR #346** G-GOV-SYNC-01 post-Phase-3 governance currency synchronization — documentation-only (merge `6b375121648e08b882fcc2b475a5986f6a9508ef`);
  **PR #347** G-UX-ANSWER-VALIDATION guided empty-answer validation experience (merge `722cf1c5d9b1756503ba92b34d0938fca3d1b695`);
  **PR #348** G-UX-SNAPSHOT-DECISION temporary-session Keep/Refine post-output decision — classification A, entry-point-only refinement (merge `115239ffc4b4f2f1a108aae498cb1bbf016bbf08`).
  These are **bounded, behavior-preserving** readiness/security/governance and UX accessibility-and-disclosure
  increments only. They do **not** activate Phase 3F bounded implementation broadly, Phase 4, WS17, or STG, and add
  no persistence, accounts, ownership, or later capability. Enumerated with full evidence in
  `docs/governance/evidence/phase3_owner_decisions/POST_PHASE_3_UX_IMPLEMENTATION_GATES_FORMAL_CLOSURE.md`.
  **No UX implementation increment is currently active; the next gate is NOT AUTHORIZED and requires a separate
  explicit owner decision. Phase 4, WS17, and STG remain NOT AUTHORIZED / NOT STARTED.**
- **Lean Governance and Agent Continuity Protocol:** **MERGED AND EFFECTIVE** on the
  authoritative branch (this document, the Owner Decision Register, the Active Increment
  Contract, and the Handover Template are now the binding continuity inputs).
- **Current active work:** **NONE — no UX implementation increment is active.** The Phase 3E–3F
  governance-record synchronization is **MERGED and CLOSED (PR #338, merge `a7a141ce`)**, and the subsequent bounded
  post-Phase-3 gates (PRs #339–#348) are all **merged, post-merge verified, and formally closed** (see the
  Phase-and-gate section). The **last formally closed implementation gate is G-UX-SNAPSHOT-DECISION (PR #348, merge
  `115239ffc4b4f2f1a108aae498cb1bbf016bbf08`)**. The `ACTIVE_INCREMENT_CONTRACT.md` correctly records **NO ACTIVE
  CONTRACT**; the repository awaits the next separately owner-authorized gate. No implementation authority is presently granted.
- **Governance-currency synchronization history:** the earlier currency lag (#338–#345 unrecorded) was resolved by
  **G-GOV-SYNC-01 (PR #346, merge `6b375121648e08b882fcc2b475a5986f6a9508ef`), MERGED and CLOSED** — so it is no longer
  a pending candidate. The subsequent lag (PR #346, PR #347 G-UX-ANSWER-VALIDATION, and PR #348 G-UX-SNAPSHOT-DECISION
  unrecorded; older tip pointer) is **proposed to be resolved by the G-GOV-SYNC-02 documentation-only candidate**; that
  lag becomes **resolved only after G-GOV-SYNC-02 is independently reviewed (where required), owner-accepted, merged,
  and post-merge verified**.
- **Next proposed gate (not started, not authorized here):** any move toward **Phase 3F bounded implementation
  increments** (or Phase 4, WS17, or a Structured Technical Guidance workstream) requires a **separate explicit owner
  authorization** with separately bounded, tested, reviewed, accepted, merged, and verified contracts. **NEXT
  UX-INCREMENT / POST-PHASE-3 GATE: NOT AUTHORIZED / REQUIRES SEPARATE OWNER DECISION.**

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
- **Bounded UX accessibility & disclosure baseline (post-Phase-3 gates #342–#345):** a shared application
  shell (viewport, `<main>` landmark, skip-to-content link, persistent "Temporary session" header disclosure);
  a static informational Data & Session trust surface at `GET /data-and-session` with a header "Learn more"
  link (S15); an entry-surface alignment (idea-field `<label>` + one temporary-session intake-disclosure line);
  and a guided-session answer-field `<label>`. These are **presentation/accessibility-only, behavior-preserving**
  additions — no route, session, engine, validation, persistence, account, or ownership change. The full Phase 3E
  nine-step journey (including the S01 "Step 1 of 9" stepper) is **NOT** implemented and remains deferred.

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
