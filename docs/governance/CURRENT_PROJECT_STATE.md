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
    `3a802fd84055f475feafcd55893da301af45c67d` (Merge PR #427 — P8-I4-I1 Provider-Neutral Payment Boundary Foundation;
    two-parent merge of `fccd8955afdfdd5167c4b7a4f0dbe6c14d00127b` (base, PR #426 P8-I4-C) + `6f83e496ac236a798598d393d8dd79b9f9dfaf8d`
    (candidate), tree `191709299943f8a87ec2ee8c287caf77a850e2f9`, post-merge verified) — always re-resolve the live tip from
    Git per the rule above. (Prior pin `d37caef` (PR #421, P8-I2 formal closure) is superseded; the authoritative branch has
    since merged the corrected P8-I3-C contract (PR #423), the P8-I3 implementation + formal closure (PR #424, merge
    `cef9a52`), the P8-I4-C contract (merge PR #426, `fccd895`), and P8-I4-I1 (PR #427, `3a802fd`).)
  - **Prior recorded tip (historical):** `d37caef8cfc0e4c5e53275e6e126ec8247a26219` (Merge PR #421 — P8-I2 Commercial Usage
    Quotas formal closure / current-truth sync; two-parent merge of `e3c65af` (base) + `7e3f17b` (candidate), tree
    `d1a8208bb3efe401d9a9797d8cafd1a64703c83c`, post-merge verified); superseded as the live tip by the P8-I3-C/P8-I3/P8-I4-C/
    P8-I4-I1 merges (PRs #423–#427).
  - **Prior recorded tip (historical):** `402727a557edd7dbea3e92f477bf9cbefe74ea3e` (Merge PR #377 — P5-2 Authenticated
    Sessions / Verified Email / Account Recovery implementation + FORMAL CLOSURE; two-parent merge of `f84c87d` +
    `87c85c7`, tree `375db689`); superseded as the live tip by PR #378 (P5-2 closure sync) and PR #379 (P5-3
    implementation + Phase 5 final closure).
  - **Prior recorded tip (historical):** `65a2c0e258bf9635921046ad27f8a886cce78218` (Merge PR #375 — P5-1 Account &
    Credential Foundation implementation + FORMAL CLOSURE; two-parent merge of `e84526d` + `6be86f5`, tree `128b2d4`);
    superseded as the live tip by PR #376 (P5-1 closure sync) and PR #377 (P5-2 implementation).
  - **Prior recorded tip (historical):** `276e89681e6008ec859383771b845833321b5552` (Merge PR #369 — P4-2 Level-1
    deterministic read-only reconstructed review-state implementation + Phase 4 FORMALLY CLOSED; two-parent merge of
    `2cde586` + `e66ae3a`, tree `1f6babf`); superseded as the live tip by the intervening documentation/implementation
    merges PR #372 (Draft Level 2 implementation + closure), PR #373 (Phase 5 identity/ownership discovery), PR #374
    (Phase 5 formal contract + continuing authorization), and PR #375 (P5-1 implementation).
  - **Prior recorded tip (historical):** `1c9dff7962a428cfd32ab577dbbbb84ce21909b3` (Merge PR #367 — P4-1b-2b read-only
    accepted-answer evidence reconstruction implementation, post-merge verified, owner accepted, and CLOSED); superseded
    as the live tip by PR #369 (P4-2 Level-1).
  - **Prior recorded tip (historical):** `77bd10cc55a731b18d4e35ea262b55342a9f847f` (Merge PR #365 — P4-1b-2a durable
    idempotent accepted-answer persistence implementation, post-merge verified, owner accepted, and CLOSED); superseded
    as the live tip by PR #367 (P4-1b-2b).
  - **Prior recorded tip (historical):** `dfa082af0e6f9c09222608ca47d088dc7e2df6a8` (Merge PR #356 — P4-1a durable-store
    proof implementation, post-merge verified and formally closed); superseded by the P4-1b-1 and P4-1b-2a gates
    (PRs #358–#365).
  - **Prior recorded tip (historical):** `286b83ffbd6916086c834658f9e16411ef4de4fe` (Merge PR #353 — P4-0
    implementation closure); superseded by PR #354 (governance sync), PR #355 (P4-1a contract), and PR #356 (P4-1a
    implementation).
  - **Prior recorded tip (historical):** `62ebf8f1a07e3c0f48e4637029d641d19c3f9b9e` (Merge PR #337 —
    Phase 3D governance-record synchronization); superseded by PRs #338–#348 (see the Phase-and-gate section).
  - **Historical verified evidence tip:** `0330273b0d8b15fc66a285bcb9b866c6aa81b8e5`
    (PR #327 merge) — **historical evidence only; not the current tip.**
- **`main`:** `0e89e4636399760965c9ff8086b465c90dbadf8e` — STALE / UNRECONCILED / NOT authority.


## Master Obligation Index (routing layer — pointer-only)

Added by the owner-authorized governance-only **Master Obligation Index** gate (gate authorization recorded
in `OWNER_DECISION_REGISTER.md` and the append-only `ACTIVE_EXECUTION_ROADMAP.md`). It is a concise
**routing layer**, not a second roadmap and not a ledger: it names which obligation LAYERS exist, where each
is authoritatively tracked, and **where current status is determined** — so an owner or agent can reach the
source of truth without reconstructing state. **Status-ownership rule: status is owned by the referenced
authoritative tracker. This Index does not recompute, duplicate, or independently maintain obligation
status**, holds **no current per-item status values of its own**, and creates no new tracker (**D-FPC-MAP-06**
— consume/extend the existing canonical model). For any actual status, read the referenced tracker.

| Obligation layer | Authoritative source | What that source owns | Where CURRENT status is determined |
|---|---|---|---|
| 1. Deliverable-Stabilization workstreams (WS1–WS17) | `DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md` §15 *Workstream status table* | Per-WS status + closure evidence, including **deferred / post-gate** entries (e.g. WS17 / AI Coach) | That tracker (§15) |
| 2. Product-Foundation / Commercial-Readiness phase **structure** (Phase 0–10) | `PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md` §4 objectives / §5 sequence & dependencies | Objectives, intended phase **structure**, sequence/dependencies, remediation intent — **NOT** current execution status | **Layer 3** (roadmap + formal closure records) — **NOT** this plan's header/adoption/status text |
| 3. Active phase/sub-gate **execution status** (P4 / P5 / P6 — e.g. P6-1, D-P6-18) | `ACTIVE_EXECUTION_ROADMAP.md` (§4 live status + append-only tail) + formal closure records, subject to `ACTIVE_INCREMENT_CONTRACT.md` + `OWNER_DECISION_REGISTER.md` | Current lane / holds / authorized next action / phase-execution status | The latest authoritative roadmap entry (+ closure records) |
| 4. Owner-added capability inventory (CAP-01…CAP-18) | `INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md` | Recorded capabilities — all `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION` (**registration ≠ authorization**). Range corrected to CAP-01…CAP-18 under G-MPR-01-D D6 (the register extends through CAP-18; CAP-15…CAP-18 are equally tracked; earlier "CAP-01…CAP-14" enumerations are superseded as index range). | That register |
| 5. Owner decisions & authorization state (OD-/D- numbers) | `OWNER_DECISION_REGISTER.md` | Owner decisions + separate-authorization requirements (**a recorded proposal is NOT execution authorization**) | That register |

**Product-Foundation status caveat (important).** The Product-Foundation plan (Layer 2) is authoritative for
objectives / intended phase **structure** / sequence — it is **not** the owner of current execution status.
Its historical document-status and adoption-note text may **lag** later execution and **must not** be read as
current project status or override newer authoritative closure evidence. Current phase-execution status is
owned by **Layer 3** (the live `ACTIVE_EXECUTION_ROADMAP.md` and the formal closure records — e.g. Phase 4 and
Phase 5 are formally closed, Phase 6 is partially executed and not complete). Refreshing that plan's stale
status text is a **separate, owner-authorized documentation-synchronization gate** — this Index does not
synchronize it (see the retained observation in the roadmap authorization entry).

**Current critical-path pointer.** The current next-eligible action is determined by the **latest authoritative
entry in `ACTIVE_EXECUTION_ROADMAP.md`**, subject to `ACTIVE_INCREMENT_CONTRACT.md` and the authorization state
in `OWNER_DECISION_REGISTER.md`. Do **not** hard-code any capability, workstream, or phase as the permanent
next action — **WS17 is not "next", Phase 7 is not "next", the Question Translation Assistant is not "next"**;
the roadmap owns future changes.

**Mandatory displacement guard.** Before authorizing any new proposal, enhancement, capability, or successor
gate, check the layers above and ask:
> "Is there an unfinished original remediation obligation, and would this new addition displace it from the
> critical path?"
Interpretation — so the guard does **not** over-block:
- **`NOT STARTED` alone does not make an item a blocker.**
- **`DEFERRED` / `RESERVED` / **post-gate** / separately-gated capabilities do not automatically block new
  work** — e.g. WS17 / AI Coach (Layer 1 §15, post-gate), D13 / STG (Structured Technical Guidance), Patent
  Export, WS-PFV-001, Domain Registry validation hardening (D-P6-14), the **Output-Language override
  capability** (the deferred *implementation* contemplated by the D-P6-17 three-layer language-model decision —
  D-P6-17 is the accepted decision, not the capability), ACV, PDF/download, output email, and CAP-01…CAP-14.
- An item is **displacement-relevant only** when live authoritative governance places it **on or ahead of the
  current critical path**, or the owner **explicitly** prioritizes it. The current critical path is owned by
  the latest authoritative `ACTIVE_EXECUTION_ROADMAP.md` entry (subject to `ACTIVE_INCREMENT_CONTRACT.md` +
  `OWNER_DECISION_REGISTER.md`).
- **If YES:** record/defer the new proposal in the appropriate **existing** register (no new tracker —
  D-FPC-MAP-06); do not execute it merely because it is attractive or newly requested; preserve the
  higher-priority obligation unless the owner **explicitly** reprioritizes it.
- **If NO:** a **separate** owner authorization is still required.

This Index authorizes nothing and triggers no automatic execution. Standing rules: **DEFERRED ≠ current
blocker; RECORDED ≠ AUTHORIZED; NOT STARTED ≠ automatic critical-path blocker.** Owner-added capabilities
remain inventory unless authorized; deferred items remain deferred until separately authorized; the existing
canonical trackers remain authoritative; **D-FPC-MAP-06** applies before creating any new tracker/register/
framework; and any new finding during a gate is classified using the existing repository vocabulary —
**BLOCKER**, **NON-BLOCKING OBSERVATION**, or **FUTURE / DEFERRED** — rather than automatically expanding
scope. The **Question Translation Assistant remains NOT AUTHORIZED / NOT STARTED**; this Master Obligation
Index gate is governance/documentation only and starts **no** successor implementation.


## HISTORICAL SNAPSHOT — POST-PR #353 (SUPERSEDED BY THE POST-PR #365 CURRENT-TRUTH SECTION)

*Superseded historical snapshot — do not read as present authority. Its "current" wording and the "P4-1 / P4-2: NOT
AUTHORIZED / NOT STARTED" / "no durable datastore" statements were accurate at PR #353 only. Current truth is the
"Post-PR #365 boundary" section below: P4-1 (P4-1a/P4-1b-1/P4-1b-2a) is implemented/merged/closed through PR #365
(`77bd10c`); a durable store and durable accepted-answer append now exist; P4-1b-2b / P4-2 / Phase 5 remain separately
gated.*

- **P4-0 — Readiness and Storage-Contract Proof:** COMPLETE AND FORMALLY CLOSED.
- **Technical evidence:** PR #353; merge commit `286b83ffbd6916086c834658f9e16411ef4de4fe`; bounded paths
  `engine/record_contract.py` and `tests/test_p4_0_record_contract.py`.
- **Current active implementation contract:** NONE.
- **P4-1 / P4-2:** NOT AUTHORIZED / NOT STARTED. A separate owner-authorized discovery and contract gate is
  required before any later implementation.
- **Runtime truth remains unchanged by P4-0:** no durable datastore, migration, accounts, authentication,
  ownership, replay, or production persistence was implemented by P4-0.
- **This synchronization is documentation-only:** it records completed history and grants no new authority.

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

## AISR capability direction (Post-Output AI-Assisted Specialist Refinement)

- **G-AISR-MATERIAL-DECISION:** COMPLETED AND ACCEPTED (owner verdict **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**).
- **G-AISR-DOC-01:** documentation-only gate recording owner decisions D-AISR-01 … D-AISR-10.
- **Capability:** `ACCEPTED FUTURE PRODUCT DIRECTION`. **Implementation:** `NOT AUTHORIZED`.
- **Canonical source of truth:** `docs/governance/POST_OUTPUT_AI_ASSISTED_SPECIALIST_REFINEMENT_CANONICAL_DECISION.md`
  (governs; not duplicated here). Indexed in the Owner Decision Register; concise reference in the Capability
  Enrichment Register; append-only roadmap entry.
- **Dependency model:** four numbered phases (Phase 4–7) + two protected workstreams (WS17, STG) + one cross-cutting
  integration lane (post-output refinement) = **seven distinct owners**; obligation groups
  `AISR-OBL-P4/P5/P6/P7/WS17/STG/REFINE` (post-output refinement is not a substitute for any of the six owners).
- **Deferred:** Phase 4 (persistence/records/provenance/re-evaluation foundations) — NOT AUTHORIZED; Phase 5
  (accounts/ownership/access) — NOT AUTHORIZED; Phase 6 (domain specialization / truthful specialist labeling) — NOT
  AUTHORIZED; Phase 7 (AI-provider integration / privacy / cost / rate limits / failure) — NOT AUTHORIZED.
- **WS17:** NOT AUTHORIZED (functional scope undefined; not defined by this record). **STG:** NOT AUTHORIZED / NOT
  EXPANDED. **Provider:** NOT SELECTED / NOT AUTHORIZED. **Exact UX:** NOT AUTHORIZED — **Phase 3E artifact recovery
  is required before any exact UX amendment** (D-AISR-09). Decision **D17** is preserved. **Next implementation gate:
  NOT AUTHORIZED.**

## Post-PR #356 synchronized boundary — P4-1a durable-store proof CLOSED

- **P4-1a — Durable-Store Proof:** `COMPLETED / MERGED / POST-MERGE VERIFIED / FORMALLY CLOSED`.
- **Authorization chain (distinct steps):** P4-1a contract candidate merged (PR #355) → **separate explicit owner
  implementation authorization** (the contract merge did **not** grant implementation authority) → implementation →
  independent review (verdict **B**, 0 blocking) → publication → merge (**PR #356**, merge
  `dfa082af0e6f9c09222608ca47d088dc7e2df6a8`; candidate `faf5730`) → post-merge verification → formal closure.
- **Technical evidence:** changed exactly `engine/record_store.py` + `tests/test_p4_1a_record_store.py` (2 files, 426
  insertions, 0 deletions); focused post-merge 11 passed; full governed suite 1681 passed / 1 skipped / 1 xfailed /
  0 xpassed / exit 0; no prohibited path changed; no new runtime dependency (stdlib `sqlite3`).
- **Product-truth boundary (binding):** P4-1a proves only a **durable-store adapter capability**. It does **not** mean
  the application currently saves user ideas durably. Because **P4-1b runtime integration has not started**, `web/app.py`
  still uses the existing temporary in-memory session behaviour; **no user-facing "saved", "recoverable", or
  durable-project claim is permitted**; existing in-memory sessions remain unrecoverable and unmigrated.
- **Preserved non-blocking observations (recorded, not fixed):** (1) durable supersession/contradiction mutation
  behaviour is decided in the future P4-1b contract; (2) `project_ids()` must not be exposed through runtime/API/UI/
  user-facing surfaces (it enumerates project capability identifiers); (3) `new_record_id()` exists and is bounded but
  is not yet connected to runtime record creation (P4-1b); (4) SQLite exception translation may be considered in later
  runtime integration if the future contract requires it; (5) minor test-connection hygiene observations remain
  non-blocking; (6) SQLite remains a reference/MVP adapter, not a permanent production-datastore commitment.
- **Current active implementation contract:** NONE. **P4-1b / P4-2 / Phase 5:** NOT AUTHORIZED / NOT STARTED.
- **Next eligible gate (owner consideration only, not authorized here):** **P4-1b — READ-ONLY DISCOVERY AND
  CONTRACT-DEFINITION PREPARATION** — `ELIGIBLE FOR SEPARATE OWNER CONSIDERATION ONLY`. Decision **D17** and the AISR
  seven-owner model are preserved.

## Post-PR #357 governance boundary — P4-1b discovery complete; P4-1b-1 contract candidate defined

- **Live tip:** `e4f9cd97e1b4329b98f1678412a6a36b9d7238bf` (Merge PR #357 — G-P4-1A-CLOSE-SYNC-01 governance
  synchronization; always re-resolve from Git). The "last independently verified tip" pointer above
  (`dfa082a`, PR #356) is unchanged by this documentation gate.
- **P4-1b — READ-ONLY DISCOVERY AND CONTRACT-DEFINITION PREPARATION:** `COMPLETE`. The owner decision package
  (runtime data-flow map, P4-1a API suitability, lifecycle, source-of-truth model, supersession/contradiction options,
  retrieval/error behaviour, Keep/Refine boundary, migration/isolation, security/config, path/RED-GREEN/test feasibility,
  risk register, 14 owner decisions, split recommendation) was delivered. Discovery authorizes nothing further.
- **D-P4-1B-01 split (RECORDED):** P4-1b = **P4-1b-1** (Runtime Store Construction + Durable Project Create/Load) +
  **P4-1b-2** (Accepted-Input Append + Keep/Refine Runtime Integration), each separately gated.
- **P4-1b-1 contract candidate (G-P4-1B-1-DOC-01):** `CONTRACT CANDIDATE ONLY — IMPLEMENTATION NOT AUTHORIZED —
  P4-1b-1 NOT STARTED`. Decisions **D-P4-1B-01 … D-P4-1B-11** recorded (see `OWNER_DECISION_REGISTER.md`); the bounded
  contract is defined in `ACTIVE_INCREMENT_CONTRACT.md` (active contract-of-record). Authorized future scope: construct
  the merged P4-1a store at startup; resolve `INVENTORAI_DB_PATH` safely; durably create a **new** project at `/start`;
  **use the `sid` as the durable `project_id`** (one unified pre-account capability — corrected per BF-1); cold-load
  after memory loss via **`load_contract(sid)`** (no mapping table, no `project_ids()` scan); translate storage errors at
  the web boundary; prove real restart/cold-load — via `web/app.py` + one new focused test only.
- **Product-truth boundary (binding, unchanged):** P4-1b-1 may prove durable **new-project** create / restart-survival /
  cold-load only. It must **not** claim accepted answers are durably persisted, that Keep/Refine is durably recorded,
  durable output/version history, recovery of existing temporary sessions, or that user ideas are fully saved — **full
  accepted-input durability requires P4-1b-2**. Until P4-1b-1 is authorized, implemented, and merged, the live
  application still uses temporary in-memory sessions and durably saves nothing.
- **Current active implementation contract:** NONE (a candidate is not an authorization). **P4-1b-1 implementation,
  P4-1b-2, P4-2, Phase 5:** NOT AUTHORIZED / NOT STARTED. Decision **D17** and the AISR seven-owner model are preserved.

## P4-1b-1 implementation review + contract amendment (G-P4-1B-1-AMEND-01) — DOC-ONLY

- **Implementation candidate `1eced7d280449b9c0842355a1882a9d3b731a633`** (P4-1b-1 runtime store construction +
  durable project create/load, on unmerged branch `feat/p4-1b1-runtime-project-persistence`) received independent
  verdict **C — REVISE AND RE-REVIEW** with two blocking findings: **B1** shared single `sqlite3` connection is
  incompatible with Flask's default threaded serving; **B2** governed tests outside the focused file wrote envelopes to
  the shared default DB instead of pytest temp paths. The candidate is **preserved intact as superseded evidence and is
  NOT amended**; it is **not merged** (authoritative tip has no runtime store integration).
- **G-P4-1B-1-AMEND-01 (documentation-only) — RECORDED:** owner decisions **D-P4-1B-1-AMEND-01 … -04** — (1) explicit
  single-threaded MVP serving `threaded=False` (bounded MVP, **not** a production-architecture claim; no
  `record_store.py`/`check_same_thread` change); (2) `tests/conftest.py` authorized ONLY for a pytest isolated-DB
  fixture (unique `tmp_path`, safe store close/reset, no repo/`:memory:`/mock/order-dependence); (3) a threading/run-mode
  regression proof; (4) a truthful local-dev DB boundary (persists until OS cleanup; holds only capability identifiers;
  pytest must never use it; P4-1b-2 re-evaluates retention/permissions/deletion). Amended future implementation paths:
  `web/app.py` + `tests/test_p4_1b1_runtime_project_persistence.py` + `tests/conftest.py`; existing tests only to adopt
  the fixture without weakening assertions; engine store remains prohibited.
- **Correction implementation is NOT authorized here** — it is a separate future authorization that keeps `1eced7d`
  as superseded evidence, starts from the then-live tip, and undergoes a new independent review.
- **Current active implementation contract:** NONE. **P4-1b-1 correction implementation, P4-1b-2, P4-2, Phase 5:**
  NOT AUTHORIZED / NOT STARTED. The live application still uses temporary in-memory sessions and durably saves nothing.

## Post-PR #360 boundary — P4-1b-1 implementation merged & technically complete; governance closure pending (G-P4-1B-1-CLOSURE-SYNC-01)

- **Live tip:** `cbd0ce3046b24631c23e482dadd413aaa42dea05` (Merge PR #360 — P4-1b-1 correction implementation; always
  re-resolve from Git).
- **P4-1b-1 implementation:** `MERGED AND POST-MERGE VERIFIED`. **P4-1b-1 technical status:** `COMPLETE`.
  The **corrected** candidate `3179cd556673e5c5b6b596a052b0744bddab011a` (independent verdict **B — ACCEPT WITH
  NON-BLOCKING OBSERVATIONS**) was merged via **PR #360**; changed exactly `web/app.py`,
  `tests/test_p4_1b1_runtime_project_persistence.py`, `tests/conftest.py` (3 files, 497 insertions, 2 deletions);
  post-merge verification passed (candidate-ancestor exit 0; `threaded=False` present; pytest DB isolation via
  `INVENTORAI_DB_PATH` present; no engine change; no accepted-input persistence; no P4-1b-2 behaviour). The superseded
  first candidate `1eced7d280449b9c0842355a1882a9d3b731a633` (verdict C) remains **preserved intact and unmerged**.
- **P4-1b-1 governance closure:** `PENDING` — completes only after this **G-P4-1B-1-CLOSURE-SYNC-01** documentation
  candidate is itself separately reviewed, published, PR-created, merged, and post-merge verified.
- **Procedural deviation (recorded truthfully):** **PR #360 was merged before a separate explicit merge authorization
  was issued in the conversation.** This is a governance-process deviation; it does not invalidate the independently
  reviewed candidate or the technical post-merge verification, is not a security incident or technical defect, and must
  not be normalized as precedent. Future gates must keep publication, PR-creation, merge, and post-merge-closure
  authorizations separate. No retroactive claim of prior merge authorization is made; the owner **later** authorized
  this closure sync.
- **Product-truth boundary (binding):** P4-1b-1 proves durable **new-project** create / restart-survival / cold-load
  only. The live application does **not** durably persist accepted answers, outputs, or complete ideas; Keep/Refine are
  not durable; lost temporary sessions are not recoverable. **Full accepted-input durability requires P4-1b-2.**
- **Preserved non-blocking observations (recorded, not fixed):** authorization-record lag; `1eced7d` unavailable to the
  reviewer for byte-level checks; author 82 vs reviewer 83 protected-regression set composition; RED-against-`1eced7d`
  not independently reproducible (base RED used); a helper's zero-on-SQLite-error minor false-green risk neutralized by
  external inspection; RED-B2 path-string proof weak alone but backed by behavioural proof; local-dev DB permissions +
  retained capability identifiers deferred to P4-1b-2; harmless `runpy` RuntimeWarning; legacy ILT demo start routes
  remain memory-only; cold-load coverage limited to `show_session`.
- **Current active implementation contract:** NONE. **P4-1b-2, P4-2, Phase 5:** NOT AUTHORIZED / NOT STARTED. Decision
  **D17** and the AISR seven-owner model are preserved.

## Post-PR #361 boundary — P4-1b-1 fully closed; P4-1b-2a contract candidate REV1 (G-P4-1B-2-DOC-01-REV1) — HISTORICAL SNAPSHOT (superseded by the "Post-PR #365 boundary" section below: P4-1b-2a is now IMPLEMENTED / MERGED / CLOSED)

- **Live tip:** `25dacb00295bcd3d34fd2cb5f789e9eae390ae11` (Merge PR #361; always re-resolve from Git).
- **P4-1b-1:** `FULLY CLOSED` (implementation merged/post-merge-verified via PR #360; governance closure complete via
  PR #361). *(Preserved observation: merged closure prose still reads "pending its own merge", satisfied by PR #361;
  plus the non-material tree-attribution note, stale "current" wording, and authorization-record lag — preserved for a
  later documentation gate.)*
- **P4-1b-2a DOC-01 original candidate `0e2a5cec24d71462eadbffa193e3467d40d506a0`:** independent-review verdict
  **C — REVISE AND RE-REVIEW**; **PRESERVED (unmerged), NOT PUBLISHABLE, NOT amended.** A previously claimed
  `518cfdfe0eca3fb0f52c88c5baea46c643d3c288` candidate/bundle is **NOT an established repository artifact and must not be
  relied upon.**
- **P4-1b-2a contract candidate REV1 (G-P4-1B-2-DOC-01-REV1):** `CORRECTED CONTRACT CANDIDATE — NOT YET MERGED —
  IMPLEMENTATION NOT AUTHORIZED — P4-1b-2a NOT STARTED`. Corrects B1 (mandatory token; ~21 enumerated answered-producing
  existing tests updated only to submit a real token; no conftest auto-injection), B2 (token transport on both the main
  answer form and the criticality-correction form), and B3 (downstream `evt-*` semantic consequences). Records
  clarifications C1–C8 (web-layer staging; idempotent retry; IntegrityError confirm-by-reload; `threaded=False`
  concurrency backstop; canonical `evt-`+truncated-SHA-256(`sid`‖token) hashed project-bound id; durable-success/
  memory-failure invalidation; O(n) pre-append scan; mixed-id regressions). See `ACTIVE_INCREMENT_CONTRACT.md` +
  `OWNER_DECISION_REGISTER.md`.
- **B3 determination (binding) — RESOLVED, OPTION A SELECTED (G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01):** a token-derived
  `evt-*` answered-record id **materially changes deterministic output** in
  `engine/idea_development_outputs.py::_record_sort_key` and `engine/requirement_landscape.py` (derived requirement ids,
  ordering, rationale); the earlier "feasibility PASS / no amendment" is **superseded** and the change must not be
  silently normalized. The owner has now **SELECTED OPTION A:** the engine **`record_id` stays `rec_N` (unchanged)** and
  a **SEPARATE durable idempotency identity** (server-issued-token-derived) is introduced; the `evt-*` scheme is **NOT**
  adopted as `record_id`, so the derived-output engines are **unchanged**. Option B (order-equivalent embedded event id)
  and Option C (idempotency key derived from `rec_N`) are **REJECTED**. Correction: stable idempotency is **NOT a
  web-layer-only change** — Option A **requires a bounded, additive `engine/record_store.py` storage amendment** (a
  separate future implementation authorization). See `ACTIVE_INCREMENT_CONTRACT.md` (amendment `A0…A14`) +
  `OWNER_DECISION_REGISTER.md` (`D-P4-1B-2A-B3-01…06`).
- **Product-truth boundary (unchanged):** P4-1b-2a would make **accepted-answer evidence** durable + readiness
  re-derivable only; it does **not** durably restore progression, the deliverable, outputs, Keep/Refine, or enable full
  session resume (progression = P4-2 replay). No claim of a saved project, fully saved idea, durable outputs, or
  account-owned records.
- **Current active implementation contract:** NONE. The B3 owner decision is now **RESOLVED (Option A)** via the
  documentation-only amendment `G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01`; **P4-1b-2a implementation remains NOT AUTHORIZED /
  NOT STARTED** (the amendment grants no implementation authority and still requires independent review + merge + a
  separate explicit implementation authorization). **P4-1b-2b, P4-2, Phase 5:** NOT AUTHORIZED / NOT STARTED. Decision
  **D17** and the AISR seven-owner model are preserved.

## HISTORICAL SNAPSHOT — POST-PR #365 boundary — P4-1b-2a IMPLEMENTED, MERGED, VERIFIED, ACCEPTED, CLOSED (SUPERSEDED by the Post-PR #369 boundary — current truth)

*Superseded historical snapshot — accurate as of the PR #365 boundary only; do not read as present authority. Its
"Current active implementation contract: NONE / P4-1b-2b … NOT AUTHORIZED / NOT STARTED" wording and its
"governance-sync record status" were current at PR #365. **Current truth is the "Post-PR #369 boundary" current-truth
section: P4-1b-2a, P4-1b-2b, and P4-2 Level-1 are all IMPLEMENTED / MERGED / VERIFIED / ACCEPTED / FORMALLY CLOSED and
Phase 4 is FORMALLY CLOSED (live tip `276e896`, PR #369); writable continuation, Phase 5, and every FPC remain NOT
AUTHORIZED / NOT STARTED.***

- **Live tip:** `77bd10cc55a731b18d4e35ea262b55342a9f847f` (Merge PR #365; two-parent merge of `4a31ece` + `0b5f757`,
  tree `c8808be`; always re-resolve from Git).
- **P4-1b-2a:** **IMPLEMENTED, MERGED, VERIFIED, ACCEPTED, AND CLOSED** (owner verdict **B — ACCEPT WITH NON-BLOCKING
  OBSERVATIONS**). It is no longer a candidate, pending review, or awaiting merge. Superseded original candidate
  `b1eb91e` (first independent-review verdict **C**, four blocking findings BF1–BF4); corrected REV1 `0b5f757`
  (re-review verdict **B**, all four blockers verified CLOSED). Merged scope **21 files / +1048 / −96**; disallowed
  paths **NONE**; source branch and SHA-preserving bundle **PRESERVED** (bundle sha-256 `621b9546…a6a9b`). Full governed
  suite **1726 passed, 1 skipped, 1 xfailed**. See the roadmap entry and `OWNER_DECISION_REGISTER.md`
  (`D-P4-1B-2A-IMPL-01…`).
- **Delivered behaviour (OPTION A):** durable accepted-answer append persist-before-ack; additive nullable
  `idempotency_key` + partial uniqueness; server-issued token on both answered-producing forms (no tokenless fallback);
  `HMAC-SHA-256(INVENTORAI_SECRET_KEY, sid‖token)` ≥128-bit durable idempotency identity (raw token not stored/logged);
  same-token idempotent retry / different-content fail-closed; validation-error token retention; the three legacy
  `start_ilt002_*` routes durably backed (usable, unlinked). **`record_id` remains `rec_N`; no deterministic-output
  engine changed; no `evt-*` engine identifier.**
- **Product-truth boundary (unchanged):** P4-1b-2a makes **accepted-answer evidence** durable + readiness re-derivable
  only; it does **not** restore progression/deliverable/outputs/Keep-Refine or enable "resume exactly where you left
  off" (that is P4-2). A new answer on a cold-loaded session fails closed generically (no resume).
- **Current active implementation contract:** NONE. **P4-1b-2b, P4-2, Phase 5:** NOT AUTHORIZED / NOT STARTED; every FPC
  remains NOT AUTHORIZED / NOT STARTED. Decision **D17** and the AISR seven-owner model are preserved.
- **Governance-sync record status:** the P4-1b-2a **implementation** closure above is **final and unchanged**; only the
  post-merge **documentation-only governance-synchronization record** is under owner-gated correction. **No
  governance-sync candidate has been published, merged, owner-accepted-as-final, or made authoritative.** Lineage:
  `571229e` (independent review **B**; owner reclassified to **C**; not published) → REV1 `1575c80` (independent review
  **B**; owner rejected / reclassified to **C**; not published) → REV2 `a92f75c` (independent review **C**; owner
  accepted the verdict; not published) → REV3 `c2bb542` (independent review **C**; owner accepted the verdict; not
  published) → **REV4** (this documentation-only candidate; **pending independent review only**). See the roadmap
  "governance-synchronization review lineage" and `OWNER_DECISION_REGISTER.md` (`D-P4-1B-2A-GSYNC-01…05`).

## Post-PR #369 boundary — P4-2 Level-1 IMPLEMENTED, MERGED, VERIFIED, ACCEPTED, CLOSED + PHASE 4 FORMALLY CLOSED (Phase 4 closure remains authoritative; as the live-tip / next-eligible pointer this section is SUPERSEDED by the P5-1-CLOSED current-truth section below)

- **Live tip:** `276e89681e6008ec859383771b845833321b5552` (Merge PR #369; two-parent merge of `2cde586` (base) +
  `e66ae3a` (candidate), tree `1f6babf`, equal to the candidate tree; always re-resolve from Git).
- **P4-2 Level-1 — Deterministic Read-Only Reconstruction of Review State (OPTION A):** **IMPLEMENTED, MERGED,
  POST-MERGE VERIFIED, OWNER ACCEPTED, AND FORMALLY CLOSED** (owner verdict **B — ACCEPT WITH NON-BLOCKING
  OBSERVATIONS**). No longer a candidate, pending review, pending publication, not-authorized, or not-started.
  Authorization chain: discovery gate **G-P4-2-DISCOVERY-CONTRACT-01** (Option A / Level 1 recommended) → separate
  implementation authorization **G-P4-2-LEVEL1-IMPLEMENTATION-01** (Option A / Level 1; Path-N only; additive nullable
  envelope inputs; version constant; replay limit) → implementation (candidate `e66ae3a`, base `2cde586`, tree
  `1f6babf`) → independent review verdict **B** → merge **PR #369** (`276e896`) → post-merge verification (ancestry
  PASS; scope **4 files / +795 / −13**; disallowed paths **NONE**) → owner acceptance and closure.
- **Delivered (Option A / Level 1):** `engine.session_reconstruction.reconstruct_review_state(store, sid)` — a
  deterministic, **read-only** reconstruction for a durably recorded **Path-N** session. It additively persists the
  reconstruction inputs (`seed_idea_text`, `confirmed_domain`, `recon_path`, `engine_contract_version`) at project
  creation, loads accepted-answer evidence in authoritative `seq` order, builds a **fresh** canonical `IdeaState`,
  replays the seed then the answer contents through the **unchanged** `progression_loop.run_iteration`, and returns an
  **immutable** `ReconstructedReviewState`. Version `p4-2-level1-recon-v1`; replay limit **500**.
- **Does NOT provide (explicit boundary):** a resumed session; writable continuation; `SESSION_STORE` rehydration;
  answer submission from reconstructed state; full runtime restoration; durable version history / branching / rollback;
  account ownership; **Phase 5** capability; **FPC-02** stale-output implementation. Legacy / missing-metadata /
  unsupported-path / version-mismatch fail closed to Level-0 evidence (no AI, no network); malformed history raises the
  canonical `ContractError`; the replay boundary+1 fails closed; **no DB / `SESSION_STORE` mutation**; **no UI**; **no
  prior-output validity claim**. The seed idea is never logged or duplicated into an `AssertionRecord`.
- **Evidence:** permitted paths exactly `engine/record_store.py`, `engine/session_reconstruction.py` (new), `web/app.py`
  (persist inputs at creation only), `tests/test_p4_2_session_reconstruction.py` (new). Source branch
  `feat/p4-2-level1-readonly-reconstruction` and the SHA-preserving bundle `p4_2_level1_e66ae3a.bundle` (SHA-256
  `d1aae8f16239a8ffe2088ec9a8e197b4dc6b329f73d760f8f6cab7213dec9b25`) **PRESERVED**. Tests: focused **28 passed**; full
  governed suite **1769 passed, 1 skipped, 1 xfailed**.
- **Accepted non-blocking observations (preserved, not fixed):** (1) SQLite column `recon_path` maps to the logical
  field `path`; (2) the literal replay boundary 500/501 was independently verified; (3) a genuine pre-change-schema
  migration was independently verified but is not a committed focused test; (4) returned `AssertionRecord` elements are
  mutable local deserialized copies but cannot mutate durable storage or live sessions.
- **PHASE 4 (Durable Data and Evidence Foundation): FORMALLY CLOSED** within its implemented boundary — durable
  accepted-answer append (P4-1b-2a) + separate durable idempotency identity (P4-1b-2a) + accepted-answer evidence
  loading (P4-1b-2b) + deterministic Level-1 read-only reconstruction (P4-2) + additive legacy-safe project
  reconstruction metadata + no false session-resume claim. Phase 4 did **NOT** deliver writable continuation, accounts /
  authentication / ownership, version history / branching / rollback, output email / download, ACV, an AI Coach, or any
  FPC implementation. **NEXT ELIGIBLE PHASE: Phase 5 — Accounts / Authentication / Ownership / Verified Email
  Foundations — NOT STARTED / NOT AUTHORIZED.**
- **Current active implementation contract:** NONE. **Writable continuation, P4-2 beyond Level-1 read-only, Phase 5–7,
  WS17, STG, ACV, PDF, Email, and every FPC (FPC-01…FPC-04) remain NOT AUTHORIZED / NOT STARTED.** Decision **D17** and
  the AISR seven-owner model are preserved.

## PHASE 6 — DOMAIN SPECIALIZATION / TRUTHFUL SPECIALIST LABELING (executed lane, Option A): FORMALLY ACCEPTED AND CLOSED (current truth)

- **Executed Phase 6 lane — Domain Specialization / Truthful Specialist Labeling, Option A — Truthful Domain Labeling
  Foundation: FORMALLY ACCEPTED AND CLOSED** (owner gate **G-PHASE-6-DOMAIN-SPECIALIZATION-FORMAL-CLOSURE-01**; dedicated
  record `docs/governance/PHASE_6_DOMAIN_SPECIALIZATION_FORMAL_CLOSURE_RECORD.md`; append-only roadmap closure entry; owner
  decision **D-P6-CLOSE** in `OWNER_DECISION_REGISTER.md`). Closure basis tip `9665413` (PR #390). Grounded in: discovery
  `G-P6-DOMAIN-SPECIALIZATION-DISCOVERY-01` accepted; **D-P6-00 … D-P6-15** adopted; **Option A** selected (**D-P6-01**);
  **P6-1** closed (PR #385/#386); **D-P6-18** closed (PR #388/#389); **no required original Option-A implementation
  obligation remains** (`ACTIVE_INCREMENT_CONTRACT.md` records no active contract-of-record).
- **Distinct future program — NOT closed by this gate:** the Product-Foundation §5 **"Multi-Domain and Technology
  Capability Foundation"** is a **DISTINCT FUTURE PROGRAM** — **FUTURE / DISTINCT / NOT AUTHORIZED** by this closure and not
  renamed into the executed lane (naming seam per **D-P6-00**; the registry-parity "Phase 6" track is also distinct —
  neither lane authorizes the other).
- **No successor authorized.** This closure authorizes **no** successor gate or capability. **Question Translation
  Assistant** remains **NOT AUTHORIZED / NOT STARTED**; **Domain Registry hardening (D-P6-14)** is a separate prerequisite
  before any future new-domain activation; **Output-Language** override remains DEFERRED / NOT IMPLEMENTED / NOT AUTHORIZED
  (D-P6-17 is the accepted decision, not the capability); **WS17** post-gate/deferred; **STG** reserved/inactive; **ACV**
  future/separately gated; **PDF/download**, **output email** deferred; **CAP-01…CAP-14** RECORDED ≠ AUTHORIZED; **Phase 7**
  separate future phase NOT AUTHORIZED; **new domain activation** NOT AUTHORIZED. The next-eligible action is read from the
  live `ACTIVE_EXECUTION_ROADMAP.md` + Master Obligation Index + `OWNER_DECISION_REGISTER.md` and requires **separate
  explicit owner authorization**.
- **§5 Multi-Domain Foundation — contract defined; §5-I1 CLOSED:** the distinct future §5 program has a
  governance/documentation-only **contract of record §5-C1** (`docs/governance/PRODUCT_FOUNDATION_S5_MULTI_DOMAIN_FOUNDATION_CONTRACT.md`;
  owner decisions **D-S5-C1** / **D-S5-01…D-S5-09**). Its first implementation increment **§5-I1 — Domain Registry
  Validation Hardening (D-P6-14)** is now **IMPLEMENTED / INDEPENDENTLY REVIEWED (B, zero blockers) / MERGED (PR #393
  `9d5e3bf`) / FORMALLY ACCEPTED AND CLOSED** (`docs/governance/S5_I1_DOMAIN_REGISTRY_HARDENING_FORMAL_CLOSURE_RECORD.md`;
  **D-S5-I1-CLOSE**). It hardened the **existing** canonical Domain Registry only (no new registry; D-FPC-MAP-06); no
  domain activated; electronics-only activation unchanged. **§5-I2 — Activation-status policy + explicit unsupported-domain
  model** is now **IMPLEMENTED / INDEPENDENTLY REVIEWED (B + delta B, zero blockers) / MERGED (PR #396 `e224215`) /
  FORMALLY ACCEPTED AND CLOSED** (`docs/governance/S5_I2_ACTIVATION_STATUS_POLICY_FORMAL_CLOSURE_RECORD.md`;
  **D-S5-I2-CLOSE**) — explicit engine activation policy (three support states; electronics-only; pack-status ≠ activation;
  web admission bound to the policy); no domain activated; no persistence/domain-pack/user-copy change. **§5-I3 — Subsystem
  + cross-domain project model foundation** is now **IMPLEMENTED / INDEPENDENTLY REVIEWED (B, zero blockers) / MERGED (PR
  #398 `dac5696`) / FORMALLY ACCEPTED AND CLOSED** (`docs/governance/S5_I3_SUBSYSTEM_CROSS_DOMAIN_MODEL_FORMAL_CLOSURE_RECORD.md`;
  **D-S5-I3-CLOSE**) — additive in-memory subsystem foundation (one project → zero-or-more subsystems → each may reference a
  canonical domain as metadata; support-state via the §5-I2 policy); scalar root domain + all persistence preserved; durable
  subsystem persistence / identity / display-name / subsystem-grain evidence-risk-validation remain **future / NOT
  delivered**. **§5-I4 — EVIDENCE GATE NOT MET → SKIP at current evidence** (no Technology Capability Registry). The owner's
  integration-ready clarification (structured-output transfer + future result-return via governed adapters) is recorded
  **against the existing Phase 7 — API and Integration Foundation** requirement, not as a new decision (D-FPC-MAP-06;
  non-implementing; Phase 7 NOT AUTHORIZED). **Product-Foundation §5 — Multi-Domain and Technology Capability Foundation is
  now FORMALLY ACCEPTED AND CLOSED** (gate **G-S5-CLOSE-PRODUCT-FOUNDATION-FORMAL-CLOSURE-01**; **D-S5-CLOSE**; dedicated
  record `docs/governance/PRODUCT_FOUNDATION_S5_FORMAL_CLOSURE_RECORD.md`; authoritative if/when its governance candidate is
  merged) after §5-C1 + §5-I1 + §5-I2 + §5-I3 + the §5-I4 evidence-gate decision and GAP-1…GAP-4 reconciliation; ORIGINAL §5
  unfinished material obligation = NONE; POST-§5 material implementation gap = NONE; no new domain activated. **NEXT ELIGIBLE
  PHASE: Phase 7 — API and Integration Foundation.** Phase 7 is now the **active phase** under a **Standing Owner
  Authorization**. **Contract-of-record published: P7-C — Formal Phase-7 Contract & Acceptance Criteria**
  (`docs/governance/PHASE_7_API_AND_INTEGRATION_FOUNDATION_P7C_CONTRACT.md`; owner gate
  **G-P7C-FORMAL-PHASE-7-CONTRACT-PUBLICATION-01**; **D-P7C-01**) formalizing the frozen P7-A/P7-B decisions
  (read/export-first v1; Lean internal read/export service seam; distinct least-privilege machine/API identity;
  first-public-exposure security baseline; outbound canonical→adapter boundary; untrusted-by-default inbound-result
  invariant; deferred subsystem-durable-identity/async/write-import/inbound-persistence/vendor-integration; §18
  obligation register with closure classification reserved for a mandatory §25 Phase-7 exit-criteria review). **The
  P7-C contract itself confers no implementation authorization; a distinct later Standing Phase-7 Authorization
  (`D-P7-STANDING-01`) grants continuation through the remaining Phase-7 gates and formal closure, subject to the
  contract boundaries, per-gate bounded scope, evidence triggers, tests, independent review where required, and the
  §25 exit review.** Standing authorization ≠ active increment: **current active implementation = NONE.** The **P7-I1 — Internal
  Read/Export Service Boundary** increment (P7-C §8 first slice; bounded contract merged PR #402) is now
  **IMPLEMENTED / INDEPENDENTLY REVIEWED (A) / MERGED (PR #403, merge `94ccccd`; parents `0041097`+`8f30f4f`; merged
  tree `fba951e`) / POST-MERGE VERIFIED / FORMALLY ACCEPTED AND CLOSED** (increment closure under `D-P7-STANDING-01`;
  dedicated record `docs/governance/P7_I1_INTERNAL_READ_EXPORT_SERVICE_BOUNDARY_FORMAL_CLOSURE_RECORD.md`; authoritative
  if/when this governance candidate is merged). It delivered one Flask-free internal seam
  `engine/read_export_service.py` (authorized durable Project Read; distinct deterministic Structured Export composed
  from durable record data + canonical domain support-state) consuming `store.load_owner`/`load_contract`/
  `load_reconstruction_inputs` + explicit caller identity, fail-closed, no `web/app.py`/persistence/domain change, no
  public API, no mutation; focused 22 / regression 69 / full 2047 passed, 0 failed; superseded candidate `acf0c46` is
  evidence only. **P7-I1 closure is an increment closure only — Phase 7 is NOT closed, no public API exists, and no
  later Phase-7 obligation is satisfied** (§25 exit review reserved before P7-CLOSE). **P7-I2 — Versioned Read/Export Public API + first-public-exposure security baseline** is now
  **CONTRACT ESTABLISHED / MERGED (PR #405) / IMPLEMENTED / INDEPENDENTLY REVIEWED (A) / OWNER ACCEPTED / MERGED
  (PR #406, merge `5971b7a`; parents `7abdd06`+`cd46c7f`; merged tree `a299bce`) / POST-MERGE VERIFIED / FORMALLY ACCEPTED
  AND CLOSED** (increment closure under `D-P7-STANDING-01`; dedicated record
  `docs/governance/P7_I2_VERSIONED_READ_EXPORT_PUBLIC_API_FORMAL_CLOSURE_RECORD.md`; authoritative if/when this governance
  candidate is merged). It delivered a versioned read-only public API (`GET /api/v1/projects/<id>` + `/export`;
  `web/api_v1.py` mounted in `web/app.py`) consuming the P7-I1 seam, with a distinct machine/API principal
  (Authorization-header credential, never the browser session; bound to one `owner_account_id`; token-style hash-only;
  issuance/revocation/expiry/rotation/account-status), a single `project:read` scope, API + export version identity, a
  stable non-enumerating error envelope, correlation id, durable minimal access audit (fail-closed), and two-tier
  fail-closed rate limiting (pre-auth bounded-subject + post-auth `api_read`) reusing the hardened `record_rate_attempt`;
  additive `api_credentials`/`access_audit` tables in the existing store schema lifecycle (no handler DDL); no
  writes/import/adapters/P7-I3; no project-state mutation. Reproduced at merged tip: P7-I2 focused 36 / regressions 52 /
  full 2083 passed, 0 failed. Retained non-blocking observations (post-auth limiter after scope check; unknown-id
  micro-timing; inert `API_CREDENTIAL_STATUSES`; `access_audit` retention NOT solved). **P7-I2 closure is an increment
  closure only — Phase 7 remains OPEN; no remaining Phase-7 obligation is satisfied; the §25 exit review remains reserved
  before P7-CLOSE.** **P7-I3 — Canonical Export + Local/Reference Adapter Proof (outbound-only, non-mutating)** is now
  **CONTRACT ESTABLISHED / MERGED (PR #408) / IMPLEMENTED / INDEPENDENTLY REVIEWED (A) / OWNER ACCEPTED / MERGED
  (PR #409, merge `2ee60ec`; parents `c66a219`+`27e3104`; merged tree `76ce600`) / POST-MERGE VERIFIED / FORMALLY
  ACCEPTED AND CLOSED** (increment closure under `D-P7-STANDING-01`; dedicated record
  `docs/governance/P7_I3_CANONICAL_EXPORT_LOCAL_REFERENCE_ADAPTER_PROOF_FORMAL_CLOSURE_RECORD.md`; authoritative if/when
  this governance candidate is merged). It delivered one local/deterministic/network-free/vendor-neutral reference
  adapter (`engine/export_adapter.py`) consuming the canonical P7-I1 Structured Export → distinct flattened DTO →
  independent semantic validation (non-empty preservation floor + integrity/tamper detection); outbound-only,
  non-mutating, UNTRUSTED BY DEFAULT; no vendor/network/public-API/domain-activation. The P7-I2 amendment strengthened
  (not weakened) the adapter-import boundary (allowlist + all security tests preserved). Reproduced at merged tip:
  P7-I3 focused 21 / P7-I2 37 / combined 102 / full 2105 passed, 0 failed. Superseded candidates `51b8fc6` (contract)
  and `8ee0551` (impl) are evidence only (remote tag not verified/present). **P7-I3 closure is an increment closure
  only — Phase 7 remains OPEN; no remaining Phase-7 obligation is satisfied.** P7-I3 formal closure MERGED (PR #410,
  merge `7fda709`; parents `2ee60ec`+`24dbe0f`; merged tree `e77d475`) / POST-MERGE VERIFIED. **The mandatory §25
  Phase-7 Remaining-Obligation / Exit-Criteria Review is now PERFORMED as a governance-only REVIEW CANDIDATE**
  (`docs/governance/PHASE_7_REMAINING_OBLIGATION_EXIT_CRITERIA_REVIEW.md`; authoritative if/when reviewed, Owner-accepted,
  merged). All **35 P7-C §18 obligations** classified: **18 DELIVERED AND VERIFIED / 17 INTENTIONALLY DEFERRED WITH
  OWNER-REASON-TRIGGER (each trigger unfired) / 0 NOT APPLICABLE / 0 STILL REQUIRED** → **PHASE-7 EXIT VERDICT: PASS —
  ELIGIBLE FOR A SEPARATE FORMAL PHASE-7 CLOSURE GATE** (eligibility only, NOT production readiness; monitoring / broad
  abuse controls / audit retention / partner sandbox / write-import / inbound / subsystem durable identity /
  async-webhook / real-vendor remain preserved trigger-deferred obligations). Reproduced live at `7fda709`: focused 80 /
  full 2105 passed, 0 failed. **The §25 review does NOT close Phase 7 and creates NO formal closure record — Phase 7
  remains OPEN.** The §25 review is now **AUTHORITATIVE / MERGED (PR #411, merge `1a8d4c7`; parents `7fda709`+`dbe54e1`;
  merged tree `909d7bf`) / POST-MERGE VERIFIED**. **P7-CLOSE — Formal Phase-7 Closure is now PERFORMED as a
  governance-only CLOSURE CANDIDATE** (`docs/governance/PHASE_7_FORMAL_CLOSURE_RECORD.md`) under `D-P7-STANDING-01`,
  preserving the authoritative §25 result verbatim (35 obligations: **18 DELIVERED AND VERIFIED / 17 INTENTIONALLY
  DEFERRED WITH OWNER-REASON-TRIGGER / 0 NOT APPLICABLE / 0 STILL REQUIRED**; EXIT PASS). Reproduced live at `1a8d4c7`
  (code byte-identical to the §25 tip): focused 80 / full 2105 passed, 0 failed. **Phase-7 closure is CANDIDATE ONLY
  until independently reviewed, Owner-accepted, merged, and post-merge verified; only then is Phase 7 FORMALLY CLOSED.**
  Closure makes NO production/security/operations-readiness claim; the 17 deferred obligations remain future governed
  obligations with accepted triggers (Monitoring / broad abuse controls / partner sandbox / write-import / inbound /
  subsystem durable identity / async-webhook / real-vendor NOT delivered; access_audit retention = unresolved
  operational observation, not a closure obligation). **Phase 7 is now FORMALLY CLOSED**
  (P7-CLOSE MERGED PR #412, merge `c15b7e7`; parents `1a8d4c7`+`db09fe4`; merged tree `5b25ccb`; POST-MERGE VERIFIED).
  **PSRR — Production Security & Release Readiness — GOVERNANCE REGISTRATION is now MERGED / POST-MERGE VERIFIED /
  AUTHORITATIVE** (PR #413, merge `6c0626e3ca659f90133a7df865e2a439f7b74f73`; parents `c15b7e7`+`a569f4b`; merged tree
  `4f1780ce` == accepted candidate tree) (`docs/governance/PSRR_PRODUCTION_SECURITY_RELEASE_READINESS_REGISTRATION.md`;
  durable Owner decision **D-PSRR-01 — AUTHORITATIVE**), registered as the named release gate operationalizing **OD-P /
  Phase-10** ownership (D-FPC-MAP-06: existing owner extended — no competing framework). **PSRR: MANDATORY BEFORE PUBLIC
  PRODUCTION; GOVERNANCE REGISTRATION AUTHORITATIVE. PSRR EXECUTION: NOT STARTED. Public Production: BLOCKED until PSRR =
  GO/PASS + the governing separate deployment gate + explicit Owner deployment authorization** (NO-GO/FAIL leaves the
  block). Current active implementation: NONE; next development work is NOT automatically activated by this synchronization.
  No vendor selected; no production-readiness claim. **Phase-8 privacy/legal entry boundary CLARIFIED** (Owner decision
  **D-P8-PL-01**, governance-only, candidate): §340 "privacy and legal prerequisites accepted" = bounded **entry-level
  design/architecture/legal-scope** rules accepted before a Phase-8 contract proceeds (provider-neutral commercial model:
  plans/subscriptions/entitlements/quotas/commercial-data, cancellation/refund state-model interfaces) — it does NOT require
  the final Phase-10 public legal artifacts (Privacy Policy / Terms / payment terms / refund policy / consent) merely to
  DEFINE the commercial model; **Phase 10 retains ownership** of those. Building Phase-8 mechanics authorizes **NO public
  paid activation** — blocked until applicable Phase-10 legal/readiness + PSRR = GO/PASS + governing Deployment Gate +
  explicit Owner deployment authorization. **OD-I/OD-N unchanged.** Activates no Phase-10/PSRR/billing work. The **Phase-8
  Formal Contract (P8-C) is now DEFINED by a governance-only CONTRACT CANDIDATE**
  (`docs/governance/PHASE_8_SUBSCRIPTION_BILLING_ENTITLEMENTS_P8C_CONTRACT.md`; authoritative if/when reviewed/accepted/
  merged/post-merge verified): canonical plan/subscription/entitlement architecture (hybrid entitlement via one Flask-free
  fail-closed `evaluate_entitlement` seam consuming the existing account foundation — D-FPC-MAP-06, no new registry/manager/
  adapter), the critical distinctions (security rate-limit ≠ commercial quota; API scope ≠ paid entitlement; plan access ≠
  domain activation; subscription active ≠ production authorization; payment success ≠ technical progression; billing audit ≠
  security monitoring), plan-neutral core (OD-N), data preserved on entitlement decrease (OD-O), provider neutrality (**no
  provider selected; no prices set**), and the increment decomposition (**P8-I1 Plan & Entitlement Foundation [first, no
  payment provider]** → P8-I2 Quotas → P8-I3 Lifecycle → P8-I4 Payment Provider Boundary → P8-CLOSE). **Phase 8 P8-C is ACCEPTED /
  MERGED (PR #416, merge `5db47a2`; parent 2 = accepted candidate `1aed84a`; merged tree `d3ae4a5`) / POST-MERGE
  VERIFIED.** The first Phase-8 increment **P8-I1 — Plan & Entitlement Foundation** is now **DEFINED by a governance-only
  BOUNDED IMPLEMENTATION-CONTRACT CANDIDATE (CORRECTED — verdict-B remediation)**
  (`docs/governance/PHASE_8_I1_PLAN_ENTITLEMENT_FOUNDATION_INCREMENT_CONTRACT.md`; supersedes prior candidate `2a4b65b`,
  evidence only; authoritative if/when reviewed/accepted/merged/post-merge verified): smallest provider-neutral proof of
  Account → Commercial Plan Identity → Entitlement Evaluation → Governed Capability Access (code-resident versioned plan
  catalog + additive durable `commercial_assignments` [plan-identity only] + minimal atomic-with-audit `commercial_audit` +
  one Flask-free fail-closed derived-entitlement seam + one neutral governed-capability proof; NO payment provider/checkout/
  charges/invoices/tax/quota/lifecycle/proration/UI). Records an explicit, Owner-acceptance-conditional **bounded refinement
  of P8-C** (catalog code-resident vs DB-durable; P8-I1 assignment = plan identity only, lifecycle states/period boundaries
  deferred to P8-I3; honest future schema-evolution — no `ALTER TABLE` framework) — NOT a silent supersession; P8-C history
  preserved. Fail-closed six-state model (legacy/default absence → default; unknown/malformed/catalog-error/missing-account/
  disabled-deleted → fail closed; missing account NOT defaulted) using existing Phase-5 `ACCOUNT_STATUSES`; additive
  idempotent migration existing+fresh DBs, rollback-safe. OD-N enforced by an engine-wide inverted-allowlist static import
  guard + behavioral guard; assignment+audit atomic in one transaction; credential revocation plan-independent; internal
  identifiers not publicly exposed; security rate-limit ≠ commercial quota; API scope ≠ paid entitlement; plan entitlement ≠
  domain activation. Genuinely-RED 15-test matrix; full-suite verification mandatory for the implementation candidate.
  The corrected P8-I1-C contract is now **ACCEPTED / MERGED (PR #417, merge `29f3aeb`; parent 2 = accepted candidate `b14396b`;
  merged tree `7f36a13`) / POST-MERGE VERIFIED**, and **P8-I1 is now IMPLEMENTED as a governance-only IMPLEMENTATION
  CANDIDATE (RED → GREEN)**: `engine/plan_catalog.py` (code-resident versioned declarative catalog; internal technical
  default; neutral proof capability — not publicly exposed) + `engine/entitlement_service.py` (single Flask-free fail-closed
  `evaluate_entitlement` derived-not-snapshot seam) + additive `engine/account_store.py` `commercial_assignments`/
  `commercial_audit` (atomic assignment+audit) + `tests/test_p8_i1_plan_entitlement_foundation.py`. Genuine RED first, then
  GREEN: **focused 17 / regressions 164 / full suite 2122 passed, 0 failed** (2105 baseline + 17). OD-N proven behaviorally +
  engine-wide static import guard; fail-closed for unknown/malformed/catalog-error/missing/non-active account; valid active
  account with no assignment → technical default; credential revocation plan-independent; NO payment/provider/quota/lifecycle/
  proration/UI/domain-activation/public-paid-activation/real-paywall; changed paths exactly the REQUIRED allowlist.
  **P8-I1 is now IMPLEMENTED / MERGED (PR #418, merge
  `2bf389d`; parent 2 = accepted impl `f55ce02`; merged tree `814d15d`) / POST-MERGE VERIFIED** (full suite 2122 passed).
  The next increment **P8-I2 — Commercial Usage Quotas / Limits** is now **DEFINED by a governance-only BOUNDED
  IMPLEMENTATION-CONTRACT CANDIDATE** (`docs/governance/PHASE_8_I2_COMMERCIAL_USAGE_QUOTAS_INCREMENT_CONTRACT.md`;
  authoritative if/when reviewed/accepted/merged/post-merge verified): provider-neutral usage-limit foundation — quota
  subject **(account_id, meter)** (account principal, not browser/credential); declarative versioned quota policy in the
  P8-I1 catalog (derived, no per-account snapshot); smallest technical window (lifetime/fixed-seconds; NOT final billing
  cadence — P8-I3 owns that); new Flask-free fail-closed `engine/quota_service.py` seam with atomic evaluate-and-consume
  (no oversubscription) + optional idempotency key; additive `commercial_usage`/`commercial_usage_idempotency` tables.
  Binding: security rate-limit ≠ commercial quota (`record_rate_attempt` security-only); quota ≠ entitlement; API scope ≠
  quota; credential revocation plan/quota-independent; domain entitlement ≠ activation. **HIGH-PRIORITY anti-lock-in:**
  quotas never block reading/exporting/deleting existing Owner data; quota reduction is fail-safe/non-destructive. OD-N
  engine-wide static + dynamic-import + behavioral guards; no lower quality for free users; no overage/provider/lifecycle/
  proration/UI/public-surface/public-paid-activation. True prior-schema migration convention + genuinely-RED 21-test matrix.
  The P8-I2-C contract is now **ACCEPTED / MERGED (PR #419, merge `d3e950c`; parent 2 = accepted candidate `1f42714`; merged
  tree `7c09f10`) / POST-MERGE VERIFIED**, and **P8-I2 is now IMPLEMENTED as a governance-only IMPLEMENTATION CANDIDATE
  (RED → GREEN; verdict-B CORRECTED replacement candidate — supersedes the invalidated prior candidate `1490548`, evidence
  only, NOT merged)**: new Flask-free fail-closed `engine/quota_service.py` + declarative versioned `quota_policy` in
  `engine/plan_catalog.py` (derived, no per-account snapshot) + additive `engine/account_store.py` `commercial_usage`/
  `commercial_usage_idempotency` tables with atomic evaluate-and-consume in one `BEGIN IMMEDIATE` + `tests/test_p8_i2_commercial_quota.py`
  (P8-I1 OD-N guard extended). **Verdict-B corrections: R1 read-only `evaluate_quota` no longer fails open at exhaustion
  (finite `used >= limit`, incl. zero-limit → `denied_quota_exhausted`/`allowed=False`/`remaining=0`, no mutation; UNLIMITED
  unchanged); R2 accurate `consume_quota` docstring (QuotaError also for missing/invalid fixed-window time); + cleanups
  (no `"None"` timestamp; idempotency across-windows documented).** RED-first: R1 tests FAIL on the invalid impl, PASS after
  fix. GREEN: **focused 32 / regressions 141 / full suite 2123 passed / 3 skipped / 1 xfailed / 0 failed** (same-environment
  base 2091 + 32, no regression). Re-verified unchanged: security rate-limit ≠ quota; entitlement ≠ quota; atomic hard-cap;
  idempotency + same-key/different-amount conflict; anti-lock-in; OD-N static/behavioral/dynamic-import; revocation
  independence; API scope unchanged; no domain activation; no public surface / no paywall / no provider/lifecycle/UI.
  **P8-I2 — Commercial Usage Quotas / Limits is now IMPLEMENTED / INDEPENDENTLY REVIEWED (initial B → corrected candidate
  re-reviewed A) / OWNER-ACCEPTED / MERGED (PR #420, merge `e3c65afcee1127d3dd75e4860ccb9480f7223f16`; parent 1 `d3e950c`;
  parent 2 = accepted corrected candidate `6f269acb2ebda129d220d0387693a659db48bd1a`; merged tree
  `65d1a660b61f975d5d9614452aeefc97f300212e` == accepted candidate tree) / POST-MERGE VERIFIED / FORMALLY ACCEPTED AND
  CLOSED** (increment closure only; dedicated record `docs/governance/P8_I2_COMMERCIAL_USAGE_QUOTAS_FORMAL_CLOSURE_RECORD.md`;
  **DOCUMENTED NO-VALID-RED** — governance/documentation-only closure after an already-tested merged implementation; closure
  authoritative if/when this governance candidate is merged). The invalidated prior candidate `1490548` (verdict B,
  fail-open `evaluate_quota`) remains EVIDENCE-ONLY / NOT MERGED. Post-merge evidence reproduced at `e3c65af`: focused 32
  passed; full suite 2123 passed / 3 skipped / 1 xfailed / 0 failed. **Process-deviation recorded truthfully:** PR #420 was
  merged BEFORE the planned pre-merge safety check ran (the check did NOT occur; not claimed to have occurred), mitigated by
  an expanded post-merge identity verification (exact parents; merged-tree == accepted-candidate-tree; exactly the changed
  paths; diffstat 897/−8; clean diff-check; post-merge tests green). **P8-I2 closure is an increment closure only — it does
  NOT close Phase 8, does NOT start P8-I3/P8-I4, does NOT enable public paid activation, and registers/executes no PSRR.**
  **MANDATORY next governance gate: `G-MPR-01` — Master Phase & Roadmap Completeness Review (read-only) — REGISTERED / NOT
  YET EXECUTED; execution STOPS before P8-I3. P8-I3 — Subscription Lifecycle: NOT STARTED. P8-I4 — Payment Provider Boundary:
  NOT STARTED. P8-CLOSE: NOT STARTED. Phase 8 remains OPEN.** Preserved for G-MPR-01: the recurring `iot_electronics`
  domain-pack skipped-warning (`schema_version=None`; NOT fixed here) and the prior P8-I1 closure-record ambiguity (P8-I1
  closed via current-truth/roadmap sync without a dedicated formal closure record). Public paid activation stays blocked
  until Phase-10 legal/readiness + PSRR = GO/PASS + Deployment Gate + explicit Owner deployment authorization.
  Owner/business decisions (plan names, prices, quota values/cadence,
  trial/refund/grandfathering/enterprise/tax/overage/proration/provider policies) remain deferred/REQUIRED; none blocks the
  closed P8-I2.
  **G-MPR-01 — Master Phase & Roadmap Completeness Review (read-only) is now COMPLETE** (read-only master audit; no repository
  change), and **G-MPR-01-D — Findings Disposition & Roadmap Registration** now durably registers its accepted findings
  (governance-only candidate; dedicated record `docs/governance/G_MPR_01_D_FINDINGS_DISPOSITION_AND_ROADMAP_REGISTRATION.md`;
  authoritative if/when independently reviewed, Owner-accepted, merged). **Finding F1 RESOLVED:** **P8-I1 — Plan & Entitlement
  Foundation is now FORMALLY CLOSED via a dedicated late-registered formal closure record**
  (`docs/governance/P8_I1_PLAN_ENTITLEMENT_FOUNDATION_FORMAL_CLOSURE_RECORD.md`) — closure-record documentation gap only; NO
  P8-I1 implementation reopened; historical evidence cited not fabricated (implemented RED→GREEN, full suite 2122; merged
  PR #418 `2bf389d`, merged tree `814d15d` == accepted impl tree; post-merge verified; independent-review letter-verdict
  provenance disclosed per the PR #341 honesty precedent). **G-MPR-01-D dispositions registered (D1–D10):** D2 P8-I3
  additive/backward-compatible lifecycle-persistence rule (contract constraint only); D3 mandatory **pre-Phase-9 Core
  Domain-Neutrality Prerequisite Gate** (safety_signal / path_n_questions / web-admission literals / domain tie-break — future,
  NOT before P8-I3); D4 future **Cross-Domain / Multi-Disciplinary Engineering Integration** gate (reference ≠ activation ≠
  cross-domain evaluation; requires ≥2 activated domains; re-homes the stale "deferred to Phase 6" pointer); D5 re-homed
  deferred capabilities (QTA + Output-Language implementation = ADD live homes; ACV / PDF / Email = MOVE off closed Phase-3/4/5
  anchors; all NOT AUTHORIZED; UI≠Input≠Output Language≠QTA preserved); D6 CAP index range CAP-01…CAP-18; D7 real-vendor vs
  CAP-15 (provider abstraction) vs async/webhook vs export adapters kept distinct; D8 `iot_electronics` legacy status registered
  and **guarded (no deletion/migration/normalization/activation/repurposing without a separate gate)** — supersession vs
  future-IoT-seed vs benchmark-only-legacy reserved to a later Owner decision; D9 OD-Q `main` reconciliation = mandatory future
  gate before production (NOT before P8-I3); D10 governance-hygiene scoped corrections (this pinned-tip refresh; CAP range;
  stale active-contract header) with history preserved. **With P8-I1 formally closed, the P8-I3 lifecycle-persistence rule
  registered, and the G-MPR-01 findings durably registered, `P8-I3 — Subscription Lifecycle` is ELIGIBLE FOR OWNER
  CONSIDERATION — NOT AUTHORIZED / NOT STARTED** (a separate Owner-authorized P8-I3 bounded implementation-contract gate is
  required; eligibility ≠ authorization). Phase 8 remains OPEN; P8-I4 / P8-CLOSE NOT STARTED; Phase 9 / Phase 10 NOT AUTHORIZED;
  PSRR EXECUTION NOT STARTED; public paid activation / production BLOCKED / NOT AUTHORIZED.
  **P8-I3 — Subscription Lifecycle is now DEFINED by a governance-only CORRECTED CONTRACT CANDIDATE (P8-I3-C — verdict-B
  remediation)** (dedicated contract `docs/governance/PHASE_8_I3_SUBSCRIPTION_LIFECYCLE_INCREMENT_CONTRACT.md`; base `0a19daf`
  (PR #422); authoritative if/when independently re-reviewed, Owner-accepted, merged, post-merge verified). It **supersedes the
  prior candidate `ead186d`**, which received independent review **verdict B — ACCEPT WITH REQUIRED PRE-MERGE CORRECTIONS** and
  is **INVALIDATED / NOT MERGEABLE / EVIDENCE-ONLY / NOT MERGED** (preserved as evidence, not deleted). **Corrections applied:**
  **RC-1** lifecycle `none` is **ENTITLEMENT-NEUTRAL** — it preserves the existing P8-I1 resolution unchanged (assigned plan if
  a valid assignment exists, else `default_plan_identity()`); **no silent legacy downgrade/reassignment/rewrite**; only terminal
  `canceled`/`expired` project to default (TECHNICAL BACKWARD-COMPATIBILITY RULE — NOT commercial policy; RED R22/R30). **RC-2**
  canonical `past_due` exits — `subscription_expired` (→expired) and `subscription_cancelled` (→canceled); grace-exhaustion is a
  `reason` field, not a pseudo-event (RED R34). **RC-3** unique cancellation mapping — `cancellation_requested` is the single
  request event, `subscription_cancelled` the effective transition, `subscription_change_scheduled` reserved for PLAN changes
  only (no aliasing; RED R19/R21). **Clarification 1** due-scheduled transitions materialize only via an authorized lifecycle
  operation (one `BEGIN IMMEDIATE`); read/projection never silently writes; event log stays source of truth (RED R31/R36).
  **Clarification 2** equal-`effective_at` tie-break by durable event sequence (RED R35). All accepted properties preserved
  (5 states + implicit `none`; additive append-only event log + derived cache; no `ALTER TABLE`/back-fill/destructive rewrite;
  atomicity; idempotency/replay; injectable clock; provider neutrality; P8-I2 sole quota authority + no silent reset;
  anti-lockout; P8-I4 owns real provider mapping; business policy Owner-owned). The corrected P8-I3-C contract is
  **ACCEPTED / MERGED (PR #423, merge `09743b91b764e5ac2956401d7a88c91df48d3d8b`) / POST-MERGE VERIFIED**, and **P8-I3 —
  Subscription Lifecycle is now IMPLEMENTED as a governance-only IMPLEMENTATION CANDIDATE (RED → GREEN; verdict-B CORRECTED
  replacement — supersedes the invalidated prior implementation candidate `4385a33`, EVIDENCE-ONLY / NOT MERGED)**:
  `engine/subscription_lifecycle_service.py` (NEW seam; 5-state machine + implicit `none`; canonical provider-neutral events;
  injectable clock; `apply_event`/`get_state` [read-only, §10 fail-closed]/`materialize_due` [authorized]/`rebuild_from_events`
  [full reconstruction from the log]/`project_effective_entitlement`) + additive `engine/account_store.py` lifecycle tables
  (append-only event log carrying the scheduled target plan + derived cache with `scheduled_event_id`; one-`BEGIN IMMEDIATE`
  atomicity with **in-transaction** stale-effective_at guard, **in-transaction** pending-schedule exclusivity guard, and the
  optimistic from-state guard; imports no commercial module) + `tests/test_p8_i3_subscription_lifecycle.py` (45 tests) + the
  OD-N guard extension in the P8-I1/P8-I2 guards. **Verdict-B corrections implemented & mutation-proven:** RC-I1 atomic
  pending-schedule exclusivity (in-txn; two concurrent scheduling events → exactly one durable, no silent loss); RC-I2 stale
  `effective_at` checked IN-transaction against the latest committed state; RC-I3 causal coverage of the different-transition
  conflict guard (deterministic cancel-vs-expire two-thread race); RC-I4 scheduled target plan persisted in the append-only
  event log and reconstructable from the log alone; RC-I5 materialization idempotency bound to the durable scheduling
  `event_id` (cross-epoch same-`effective_at` materializes separately; no old-event replay wedge); RC-I6 lifecycle READ seam
  fails closed for missing/disabled/deleted accounts. Non-blocking: idempotency-key replay returns the prior result without
  payload-equality validation (documented in `find_lifecycle_event` for future P8-I4 mapping). RED (behavioral: the six
  reviewed defects reproduced) → GREEN: **P8-I3 focused 45 passed; Phase-8 94 passed; full suite 2168 passed / 3 skipped /
  1 xfailed / 0 failed** (2123 baseline + 45). Six correction mutation probes each turned a targeted test RED and were fully
  restored (byte-identical, no mutation remains); two-thread races confirmed deterministic across repeated runs. Preserved:
  additive schema (no `ALTER TABLE`/back-fill/destructive rewrite); event-log source-of-truth; one-txn atomic rollback;
  durable idempotency/replay; equal-`effective_at` `event_id` tie-break; injected clock; read/projection never writes; `none`
  entitlement-neutral (no legacy downgrade); canonical `past_due` exits; unique cancellation mapping; P8-I2 sole quota authority
  + no reset; anti-lockout; provider neutrality; OD-N. **P8-I3 — Subscription Lifecycle is now INDEPENDENTLY REVIEWED
  (initial B → corrected candidate re-reviewed A) / OWNER-ACCEPTED / MERGED (PR #424, merge
  `cef9a522dfae53493ceb1b47bd9faf409617e13e`; parent 1 `09743b9`; parent 2 = accepted corrected candidate
  `8e600c0674bfeb7be96fd6875b68de1da02eae2f`; merged tree `3d1586e4076f3b2cbd3fe6e1ff1b7f9799085f7a` == accepted candidate
  tree) / POST-MERGE VERIFIED (Pre-Merge Safety Check PASS; Post-Merge Verification PASS) / FORMALLY ACCEPTED AND CLOSED**
  (increment closure only; dedicated record `docs/governance/P8_I3_SUBSCRIPTION_LIFECYCLE_FORMAL_CLOSURE_RECORD.md`;
  **DOCUMENTED NO-VALID-RED — GOVERNANCE-ONLY FORMAL CLOSURE GATE**; closure authoritative if/when this governance candidate
  is merged). Diffstat 8 files / 1416 insertions / 10 deletions; RC-I1…RC-I6 corrections merged; RED→GREEN focused 45 /
  Phase-8 94 / full suite 2168 passed / 3 skipped / 1 xfailed / 0 failed. The invalidated prior implementation candidate
  `4385a33` (verdict B) remains EVIDENCE-ONLY / NOT MERGED (absent from official ancestry; not rewritten as accepted history).
  Preserved non-blocking observations: idempotency-key replay returns the prior outcome without payload-equality validation
  (account-scoped; accepted under P8-I3; carried to P8-I4 for provider-event mapping); a future deterministic store-level
  stale-expected-state test may add coverage (do not reopen P8-I3). **P8-I3 closure is an increment closure only — it does
  NOT close Phase 8, does NOT start P8-I4, selects NO payment provider, and enables NO public paid activation.** **NEXT
  PHASE-8 GATE: `P8-I4` — Payment Provider Boundary — NOT STARTED (registered as next; no provider selected).**
  Phase 8 OPEN; P8-I4 / P8-CLOSE NOT STARTED; Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED; public paid
  activation / production BLOCKED / NOT AUTHORIZED.
  **P8-I4 — Payment Provider Boundary is now DEFINED by a governance-only CONTRACT CANDIDATE (P8-I4-C)** (dedicated contract
  `docs/governance/PHASE_8_I4_PAYMENT_PROVIDER_BOUNDARY_INCREMENT_CONTRACT.md`; base `f66ea96` (PR #425); authoritative if/when
  independently reviewed, Owner-accepted, merged, post-merge verified). It freezes the smallest provider-neutral payment
  boundary — an adapter port (`InventorAI Core → P8-I1/I2/I3 authorities → Canonical Payment Provider Boundary → Provider
  Adapter [UNTRUSTED] → External Provider`; core imports no provider module, OD-N); strict canonical↔provider vocabulary
  separation (a raw provider event name never becomes a lifecycle event — adapters map to canonical P8-I3 operations via the
  P8-I3 seam, preserving the cancellation-requested/effective and scheduled-plan-change distinctions; P8-I1/I2/I3 remain the
  authorities); opaque canonical identities; additive provider-mapping + durable provider-event-dedupe persistence (no
  `ALTER TABLE`/back-fill/destructive migration; no full payloads/secrets/card data); event-authenticity before canonical
  mutation + a hard secrets boundary (production secret mgmt → PSRR/Phase-10); **HIGH-PRIORITY strict provider-event
  idempotency — duplicate delivery = idempotent no-op, same `(provider, provider_event_id)` with a materially different payload
  FAILS CLOSED** (resolving the P8-I3 non-blocking observation; the weaker P8-I3 replay is NOT inherited for provider events;
  durable dedupe survives restart); one-transaction atomicity (dedupe + lifecycle mutation + mapping) where the SQLite model
  supports it; a fail-closed catalogue; outage/timeout never silently mutates + reconciliation (reserved, evidence-triggered);
  a **replaceability** acceptance property (Provider A→B changes only adapter/config/mapping, a fake second provider satisfies
  the port); PCI architectural avoidance with **no compliance claim**; a 30-item future RED matrix; and a **fake-adapter-first
  decomposition** (P8-I4-I1 port + fake/reference adapter + persistence → evidence-triggered verified-webhook seam →
  evidence-triggered reconciliation seam → real-provider selection/integration sub-gate → P8-I4-CLOSE). Distinct from CAP-15 AI
  Provider Abstraction (G-MPR-01-D D7). **NO provider selected** (Stripe/Paddle/PayPal/Apple/Google/other all unselected);
  provider selection is an OPEN Owner decision and a registered prerequisite for real adapter work. **P8-I4 remains a CONTRACT
  CANDIDATE ONLY — NOT started / NOT implemented / NOT authorized**; no runtime/test/Domain-Pack/schema/prompt/benchmark/web/CI/
  provider-config file changed; a separate Owner-authorized P8-I4 implementation gate is required. Phase 8 OPEN; P8-CLOSE NOT
  STARTED; Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED; public paid activation / production BLOCKED / NOT
  AUTHORIZED.
  The P8-I4-C contract is **ACCEPTED / MERGED (PR #426, merge `fccd8955afdfdd5167c4b7a4f0dbe6c14d00127b`) / POST-MERGE
  VERIFIED**, and **P8-I4-I1 — Provider-Neutral Payment Boundary Foundation is now IMPLEMENTED as a governance-only
  IMPLEMENTATION CANDIDATE (RED → GREEN)**: `engine/payment_provider_port.py` (NEW — provider-neutral `PaymentProviderPort` +
  `CanonicalOperation` + stdlib SHA-256 integrity fingerprint over a documented canonical field set [no raw payload/secrets]) +
  `engine/payment_fake_adapter.py` (NEW — two deterministic fakes A/B, different provider vocabularies → same canonical
  operations; no network/SDK/vendor) + `engine/payment_ingestion.py` (NEW — verify+parse → provider→canonical map → durable
  mapping resolution → the P8-I3 transition authority reused inside the store txn → atomic ingest) + additive
  `engine/account_store.py` (behavior-preserving `_apply_lifecycle_in_txn` refactor [P8-I3 unchanged] + two `CREATE TABLE IF NOT
  EXISTS` tables `provider_mapping` + `provider_event_dedupe` + `put_provider_mapping`/`get_provider_mapping_account`/
  `get_provider_event`/`ingest_provider_lifecycle_event` [provider-event dedupe + the SAME P8-I3 lifecycle mutation in ONE
  `BEGIN IMMEDIATE`]; imports no commercial/provider module) + `tests/test_p8_i4_i1_payment_provider_boundary.py` (30 tests) +
  the OD-N guard extension in the P8-I1/P8-I2 guards. Behavioral RED (seven boundary defects reproduced) → GREEN: **focused 30 /
  Phase-8 124 / full suite 2198 passed / 3 skipped / 1 xfailed / 0 failed** (2168 baseline + 30). Seven mutation probes each
  turned a targeted test RED and were fully restored (byte-identical); two-thread races deterministic. Verified: two fakes
  satisfy one port (replaceability; provider swap needs no P8-I1/I2/I3/Domain-Pack change); opaque external refs; additive
  mapping + durable `(provider, provider_event_id)` dedupe surviving restart; **strict idempotency** (exact duplicate replays;
  same identity + different fingerprint FAILS CLOSED; same event id under different providers independent); rejected
  pre-acceptance event can later succeed after correction; NO raw payload/secret/card persisted; deterministic content-sensitive
  fingerprint; adapter exception/timeout → no mutation; canonical-mapping-only (raw provider name never enters the P8-I3 log);
  invalid transition still rejected by P8-I3; **P8-I2 quota + P8-I1 entitlement authority unchanged**; atomic dedupe+lifecycle
  (forced rollback leaves neither); cross-account mapping isolation; OD-N (core imports no payment boundary; no provider/network
  import). **P8-I4-I1 is an IMPLEMENTATION CANDIDATE ONLY — NOT closed; NO real provider selected; NO provider SDK; NO webhook.**
  **P8-I4-I2 (verified webhook ingestion) NOT STARTED; P8-I4-I3 (reconciliation) NOT STARTED; real-provider selection/integration
  sub-gate NOT STARTED (separate Owner provider-selection decision required).** Candidate-only until independent implementation
  review → Owner acceptance → PR → pre-merge check → merge → post-merge verification → a dedicated P8-I4 closure gate. Phase 8
  OPEN; P8-CLOSE NOT STARTED; Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED; public paid activation / production
  BLOCKED / NOT AUTHORIZED.
  **P8-I4 — Payment Provider Boundary is now FORMALLY CLOSED (governance-only CLOSURE CANDIDATE; increment closure only —
  authoritative if/when merged).** The accepted P8-I4-I1 implementation (independent review **verdict A — ACCEPT**) is
  **MERGED (PR #427, merge `3a802fd84055f475feafcd55893da301af45c67d`; parents `fccd895` + `6f83e496…`; merged tree
  `191709299…`; exact diffstat 10 files / +1175 / −5; post-merge `git diff --check` PASS) / POST-MERGE VERIFIED**; full suite
  **2198 passed / 3 skipped / 1 xfailed / 0 failed** (cited, not re-run). **Evidence-triggered lanes deferred (NOT
  triggered):** P8-I4-I2 verified webhook ingestion — DEFERRED; P8-I4-I3 reconciliation — DEFERRED; real-provider integration
  — NOT STARTED; **provider selection — OPEN OWNER DECISION**; real payment collection — NOT ACTIVATED. Canonical record:
  `docs/governance/P8_I4_PAYMENT_PROVIDER_BOUNDARY_FORMAL_CLOSURE_RECORD.md`. **Mandatory handoff:** formal P8-I4 closure does
  **NOT** close Phase 8 — a separate cross-cutting obligation **`P8-AF` — Access, Licensing & Organization Foundation** is
  **REGISTERED as the required next Phase-8 foundation gate, mandatory before `P8-CLOSE` / NOT IMPLEMENTED / NOT ACTIVATED /
  NOT STARTED** (record: `docs/governance/P8_AF_ACCESS_LICENSING_ORGANIZATION_FOUNDATION_OBLIGATION.md`). `P8-AF` preserves
  **Authentication ≠ Authorization ≠ Account identity ≠ Data ownership ≠ Commercial entitlement ≠ Subscription lifecycle ≠
  Payment state ≠ Billing ownership** and **paying ≠ owning user data**; its registered (NON-ACTIVATED) future-readiness scope
  covers individual access, a **7-DAY** (NOT 14) per-account trial preserving durable data on trial→paid (**automatic day-7
  hard deletion NOT authorized**; 168h-vs-calendar semantics OPEN), a **global configurable promotional free period**
  administrable **without a source-code change**, **Owner/Admin non-billed access** as an explicit auditable
  authorization→entitlement grant (no bypass), **organization/institution licensing** with **named seats** (billing ownership
  ≠ data ownership; seat reassignment never transfers prior-member data), enterprise/custom compatibility, a deterministic
  **access-resolution precedence**, safe **quota composition** (P8-I2 remains the sole quota authority), and **no second
  lifecycle state machine** (P8-I3 remains canonical; D-FPC-MAP-06). **No premature implementation** (no organizations/
  memberships/seats/role/campaign table, admin UI, trial-duration constant, pricing, or SKUs). **Next gate: `P8-AF-C` —
  Access, Licensing & Organization Foundation Contract (governance contract first; NO implementation before it is
  independently reviewed and accepted).** **Phase 8 remains OPEN / NOT CLOSED; `P8-AF` / `P8-AF-C` / `P8-CLOSE` NOT STARTED;
  Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED; public paid activation / production BLOCKED / NOT
  AUTHORIZED.**
  **`P8-AF` is now DEFINED by a governance-only CONTRACT CANDIDATE (P8-AF-C)** (dedicated contract record:
  `docs/governance/P8_AF_ACCESS_LICENSING_ORGANIZATION_FOUNDATION_CONTRACT.md`; base `61ff4a85989dfc8d9881764597d5d7dc415da213`,
  PR #428 — which merged the P8-I4-CLOSE candidate `1da9d2d`). It defines the smallest canonical architecture — a
  provider-neutral, source-neutral **Access-Grant model** + a single deterministic **effective-access resolution seam** — that
  **composes** P8-I1 (entitlement) / P8-I2 (sole quota authority) / P8-I3 (canonical lifecycle, incl. `trialing`) / P8-I4
  (payment boundary) **without duplicating** any of them (D-FPC-MAP-06). Contracted (definition only): a single resolver (no
  scattering of access decisions), an access-grant with the invariant that **effective access is explainable/traceable to its
  source**, a **deterministic precedence rule** (access-availability / feature-entitlement / quota-authority / expiry-revocation
  / audit-provenance) preventing double quota / plan-identity corruption / accidental downgrade / hidden bypass / ambiguous
  revocation; a **7-day** trial reusing P8-I3 `trialing` (168h-vs-calendar OPEN; no runtime constant; trial→paid preserves data);
  a **global configurable promotional campaign** operable **without a source-code change** (deterministic activation/expiry;
  provider-free; no auto data deletion at end; coexists with paid; UTC-epoch); **Owner/Admin non-billed access** as
  authenticated-account → explicit authorization → entitlement grant (minimal role seam; no RBAC platform; no bypass);
  canonical **organization** + **membership** + **named-seat** capacity/assignment/reassignment (seat = entitlement, not an
  account/data-container; **reassignment never transfers prior-member data**; **billing ownership ≠ data ownership**);
  enterprise/custom compatibility and the Individual / Org-Named-Seats / Enterprise family without three account systems; safe
  **quota composition** and **lifecycle composition**; **audit/provenance + deterministic revocation** (removes access, never
  data); preserved **data ownership** (anti-lock-in + OD-O + Phase-4 privacy; **automatic day-7 hard deletion NOT authorized**;
  retention a separate policy; a recordable notice/consent capability without duplicating consent systems); the **smallest
  implementation increment** (likely access-grant model + resolver + provenance; org/seat/campaign/role seams
  contracted-but-deferred unless needed); a **12-item RED→GREEN acceptance matrix**; the **OPEN owner/business decisions** (kept
  OPEN); **P8-AF closure criteria**; and **explicit production/payment/Phase-9-10 blocks**. **P8-AF-C is a CONTRACT CANDIDATE
  ONLY — definition only; NOT started / NOT implemented / NOT authorized; NO provider selected; NO access model activated; NO
  organization/membership/seat/role/campaign/access-grant/pricing/enterprise-billing runtime code or schema created.** A
  separate Owner-authorized `P8-AF` implementation gate is required. **P8-I4 = CLOSED / AUTHORITATIVE; P8-AF-C = FORMAL CONTRACT
  CANDIDATE; P8-AF implementation = NOT STARTED; `P8-CLOSE` = NOT STARTED; Phase 8 = NOT CLOSED;** Phase 9 / Phase 10 NOT
  AUTHORIZED; PSRR EXECUTION NOT STARTED; public paid activation / production BLOCKED / NOT AUTHORIZED.
  The P8-AF-C contract is **ACCEPTED / MERGED (PR #429, merge `06683179f843b71f8d151f0c3c5647778b4b0acf`) / POST-MERGE
  VERIFIED**, and **P8-AF-I1 — Canonical Access-Grant + Access-Resolution Foundation is now IMPLEMENTED as a governance-only
  IMPLEMENTATION CANDIDATE (RED → GREEN)** — the FIRST and SMALLEST P8-AF increment, proving ONLY the canonical
  access-composition seam: `engine/access_grant.py` (NEW — a LEAF immutable, source-neutral, provider-neutral `AccessGrant`
  value object [`__slots__` forbid quota/provider/credential/pricing/data-ownership fields] built via a fail-closed
  `make_access_grant(...)`, plus pure `is_effective_at`/`exclusion_reason`; imports no engine module) + `engine/access_resolver.py`
  (NEW — the SINGLE deterministic, pure, read-only `resolve_access(grants, *, now)` → immutable `AccessResolution`; composes
  effective grants; **REFERENCES** the P8-I1 authority via `plan_catalog.entitlement_descriptor` to validate entitlement
  IDENTITY only — never reads capabilities, never redefines entitlement; imports only `access_grant` + `plan_catalog`) + the
  OD-N guard extension recognizing both as commercial seams. **Minimal safe precedence (P8-AF-C §6; no invented business
  priority):** zero effective grants → DENY; all-one-distinct-entitlement → GRANT that single entitlement (one quota-policy
  path, never additive); **competing distinct entitlements → FAIL CLOSED** (precedence deferred). Behavioral RED
  (import-absent + six mutation probes: remove expiry check / drop deterministic tie-break / invent precedence winner / add
  provider import / bypass malformed-input rejection / remove now-injection validation) → GREEN: **focused 30 / Phase-8 154 /
  full suite 2228 passed / 3 skipped / 1 xfailed / 0 failed** (2198 baseline + 30). Six mutation probes each turned a targeted
  test RED and were restored byte-identical. Verified: no double quota; provenance explains selection/exclusion; resolver
  mutates nothing and consumes NO quota/lifecycle/account/payment; entitlement REFERENCED not redefined; NO provider coupling;
  **NO authentication bypass** (a privileged-looking subject/source confers nothing; no hardcoded Owner); **NO data-ownership
  inference** (access ≠ ownership); injected epoch time only; order-independent determinism; fail-closed on malformed/ambiguous
  input; **no new persistence/schema**; P8-I1/I2/I3/I4 authorities unchanged. **P8-AF-I1 is an IMPLEMENTATION CANDIDATE ONLY —
  NOT closed; P8-AF NOT closed.** **Organization / membership / named seats — DEFERRED / NOT STARTED; campaign configuration —
  DEFERRED / NOT STARTED; Owner/Admin authorization seam — DEFERRED / NOT STARTED; trial activation — NOT STARTED.**
  Candidate-only until independent implementation review → Owner acceptance → PR → pre-merge check → merge → post-merge
  verification → subsequent P8-AF increments (only if a later gate proves a seam necessary) → a dedicated P8-AF closure gate →
  P8-CLOSE. **P8-AF-C = CLOSED / AUTHORITATIVE; P8-AF-I1 = IMPLEMENTATION CANDIDATE; P8-AF = NOT CLOSED; `P8-CLOSE` = NOT
  STARTED; Phase 8 = NOT CLOSED;** Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED; public paid activation /
  production BLOCKED / NOT AUTHORIZED.
  **P8-AF-I1 is now MERGED / POST-MERGE VERIFIED (PR #430, merge `1ac9c603b14a172a737f3577791e9f23a46533bd`), and the
  Remaining-Obligation / Closure-Eligibility Review returned verdict B** (one mandatory pre-closure correction: the
  contract-required uniform-subject invariant, P8-AF-C §5.1 "given an authenticated account"). **P8-AF-I2 — Subject-Scoped
  Access Resolution is now IMPLEMENTED as a governance-only CORRECTIVE IMPLEMENTATION CANDIDATE (RED → GREEN)**: the canonical
  resolver is now `resolve_access(grants, *, subject, now)` — a **required** authenticated `subject`; **subject scoping runs
  BEFORE entitlement composition**; a foreign-subject grant (`grant.subject != subject`) is excluded **INERTLY** (never
  contributes, never denies, never raises) with explicit `foreign_subject` provenance (the smallest-ambiguity behavior —
  raising would let another account deny/DoS this subject); an empty/missing subject is **NEVER** a wildcard (no `*`/`ALL`/
  `GLOBAL`); the post-filter precedence is UNCHANGED (zero → DENY; one distinct entitlement → GRANT; competing distinct → FAIL
  CLOSED). `AccessGrant` UNCHANGED (existing `subject` field sufficed); no persistence/schema; single runtime file changed
  (`engine/access_resolver.py`). Behavioral RED (mixed-subject composition demo against the merged I1 + 22 RED subject-scoped
  tests + six mutation probes: remove subject check / invert it / scope-after-composition / empty-subject-wildcard /
  first-grant-subject / drop provenance) → GREEN: **P8-AF-I2 focused 23 / P8-AF-I1+I2 53 / Phase-8 177 / full suite 2251
  passed / 3 skipped / 1 xfailed / 0 failed** (2228 baseline + 23); six probes each turned a test RED and were restored
  byte-identical. Verified: cross-account grants never compose; foreign grant cannot rescue a denied subject; **no
  authentication behavior introduced** (subject is an already-authenticated identity; no email/password/session inspection; no
  hardcoded Owner); **no data-ownership implication** (access ≠ ownership); order-independent; `[effective_from,
  effective_until)` FROZEN (from inclusive, until exclusive); P8-I1/I2/I3/I4 authorities unchanged; OD-N guards unweakened.
  **Deferred (Review classifications preserved): duplicate durable grant-identity rule = DEFERRED UNTIL FIRST PERSISTENCE
  INCREMENT; direct-`AccessGrant(...)` constructor hardening = DEFERRED BEFORE FIRST REAL RUNTIME CALLER; global/scope
  (campaign) grant semantics = NOT STARTED / DEFERRED (account-scoped resolution only).** **P8-AF-I2 is a CORRECTIVE
  IMPLEMENTATION CANDIDATE ONLY — uniform-subject isolation IMPLEMENTED IN CANDIDATE; P8-AF NOT closed.** Organization /
  membership / named seats — NOT STARTED / DEFERRED; campaign — NOT STARTED / DEFERRED; Owner/Admin seam — NOT STARTED /
  DEFERRED; trial activation — NOT STARTED. Candidate-only until independent review → Owner acceptance → PR → pre-merge check →
  merge → post-merge verification → the P8-AF formal closure gate → P8-CLOSE. **P8-AF-I1 = MERGED/POST-MERGE VERIFIED;
  P8-AF-I2 = CORRECTIVE IMPLEMENTATION CANDIDATE; P8-AF = NOT CLOSED; `P8-CLOSE` = NOT STARTED; Phase 8 = NOT CLOSED;** Phase 9
  / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED; public paid activation / production BLOCKED / NOT AUTHORIZED.
  **P8-AF-I2 is now MERGED / POST-MERGE VERIFIED (PR #431, merge `1132cfe8fde16a8c3a5784a2b1351a43620eda94`; independent review
  A), and `P8-AF` — Access, Licensing & Organization Foundation is now FORMALLY CLOSED as a governance-only CLOSURE CANDIDATE**
  (foundation-obligation closure only; authoritative if/when merged; dedicated record:
  `docs/governance/P8_AF_ACCESS_LICENSING_ORGANIZATION_FOUNDATION_FORMAL_CLOSURE_RECORD.md`). **All four P8-AF-C §22 closure
  criteria are satisfied:** (a) P8-AF-C reviewed/accepted/merged (PR #429)/post-merge verified; (b) the minimum increment(s)
  implemented with genuine RED→GREEN via **P8-AF-I1 + P8-AF-I2**, proving the architecture can represent and resolve the models
  safely without activating any (trial/campaign/persistence items N/A — evidence-triggered); (c) authority boundaries (§4) +
  binding invariants (§6/§13/§16/§17/§18) demonstrated and unweakened (account/data isolation now enforced; OD-N unweakened);
  (d) this closure record produced. **Delivered foundation (backend composition only; NO runtime activation):** canonical
  source-neutral `AccessGrant`; one deterministic read-only `resolve_access(grants, *, subject, now)` seam; provenance; P8-I1
  entitlement reuse; P8-I2 quota non-interference; P8-I3 lifecycle non-interference; P8-I4 provider independence;
  authenticated-subject-scoped resolution + cross-account grant isolation; fail-closed competing-entitlement ambiguity;
  deterministic injected-time; **`[effective_from, effective_until)` FROZEN** (from inclusive, until exclusive). **Deferred —
  remain deferred (no activation):** organization identity / membership / named seats / seat persistence / campaign config /
  global promotional-free-access runtime / Owner-Admin authorization seam / 7-day trial activation (automatic day-7 hard
  deletion NOT AUTHORIZED) / enterprise-custom billing / SSO-domain onboarding / concurrent licensing — ALL NOT STARTED /
  DEFERRED. **Future hardening/triggers preserved:** direct-`AccessGrant` constructor hardening BEFORE first real runtime
  caller; durable duplicate grant-identity rule BEFORE first persistence; separately governed precedence BEFORE a second real
  source; global/scope semantics separately governed; data ownership independent of billing/grant/access. **P8-AF-C = CLOSED /
  AUTHORITATIVE; P8-AF-I1 = CLOSED / AUTHORITATIVE; P8-AF-I2 = CLOSED / AUTHORITATIVE; P8-AF = FORMALLY CLOSED / AUTHORITATIVE
  (foundation-obligation closure only). Phase 8 = NOT CLOSED; next Phase-8 gate = the separate Phase-8 Remaining-Obligation /
  Exit-Criteria Review and `P8-CLOSE` = NOT STARTED;** Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED; public
  paid activation / production BLOCKED / NOT AUTHORIZED.
  **The Phase-8 Remaining-Obligation / Exit-Criteria Review returned A — ELIGIBLE FOR P8-CLOSE, and `Phase 8` — Subscription,
  Billing and Entitlements is now FORMALLY CLOSED as a governance-only CLOSURE CANDIDATE (P8-CLOSE)** — a **technical-foundation
  phase** closure (authoritative if/when merged; dedicated record: `docs/governance/PHASE_8_FORMAL_CLOSURE_RECORD.md`; base
  `e7f7bc7e1f17550dc83d658976a07462de434e17`, PR #432 — which merged the P8-AF closure `f3f509a`). **Obligation closure matrix
  (all CLOSED / AUTHORITATIVE, evidence-cited):** P8-C; P8-I1; P8-I2 (PR #421); P8-I3 (PR #424 `cef9a52`); P8-I4 (P8-I4-I1 PR
  #427 `3a802fd`; NO provider selected); P8-AF (PR #430 + #431 + closure PR #432 `e7f7bc7`). **All mandatory Phase-8 exit
  criteria PASS** (increments merged/verified; fail-closed entitlement+quota; plan-neutrality via OD-N; data-preservation on
  decrease; commercial audit distinct from `access_audit`; no regression — full suite 2251 passed / 3 skipped / 1 xfailed / 0
  failed; no provider lock-in; no PSRR/deployment/paid-activation overclaim); **N/A (contract-designed):** real provider =
  OWNER-SELECTION-TRIGGERED, verified webhook (P8-I4-I2) + reconciliation (P8-I4-I3) = EVIDENCE-TRIGGERED / DEFERRED, public
  paid activation = OUTSIDE Phase 8. **Delivered FOUNDATION ONLY (no commercial launch):** plan-identity/entitlement +
  quota/usage (sole quota authority) + subscription-lifecycle mechanics with data preservation + provider-neutral payment
  boundary (no provider) + access-grant/resolution + subject-scoped composition + fail-closed ambiguity; commercial audit
  separation; no degradation of deterministic technical truth across plan tiers. **Preserved OPEN / DEFERRED (none blocked
  closure):** all Owner business decisions (plan names / pricing / currency / cadence / trial policy / packaging / enterprise /
  grandfathering / refunds / tax / grace / over-limit-downgrade / provider selection / proration / cancellation timing) — remain
  OPEN, deferred to activation/provider-selection/launch; P8-AF future activation guards (constructor hardening before first
  runtime caller; durable duplicate-grant-id before first persistence; separately governed precedence before a second real
  source; global/scope semantics before a global grant; billing/access ≠ content ownership) — future triggers, NOT completed;
  trial / global promo / Owner-Admin / organization-named-seat / enterprise — architecture-ready, runtime NOT STARTED /
  DEFERRED (automatic day-7 hard deletion NOT AUTHORIZED; 168h-vs-calendar OPEN); deferred capability lanes (QTA/ACV/PDF/Email/
  WS17/STG) — OUTSIDE Phase 8. **PSRR = REGISTERED / MANDATORY BEFORE PUBLIC PRODUCTION / NOT EXECUTED** (Phase-8 closure ≠
  PSRR GO/PASS); `main` = stale/unreconciled, OD-Q reconciliation a separate pre-production gate (NOT a closure blocker, NOT
  performed). **Phase-8 closure authorizes NOTHING downstream** (no Phase 9/10, no real provider, no commercial launch, no
  pricing/trial/organization/seat/campaign/Owner-Admin activation, no PSRR execution, no main reconciliation, no deployment/
  production/public paid activation). **P8-C / P8-I1 / P8-I2 / P8-I3 / P8-I4 / P8-AF = CLOSED / AUTHORITATIVE; Phase 8 =
  FORMALLY CLOSED / AUTHORITATIVE (technical-foundation phase; no active increment remains) — P8-CLOSE merged PR #433
  (`00792af36e51808191690a4bf66f9b1a2644d477`);** Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED; public paid
  activation / production BLOCKED / NOT AUTHORIZED.
  **Pre-Phase-9 domain-neutrality (D3) — Owner-authorized CONTRACT CANDIDATE (fresh).** The Owner has now authorized ONE bounded
  governance-only D3 contract gate; that authorization begins with the current instruction. (A prior draft candidate
  `ed5eb14596a3f99e5d6febc90f3ba70a1e91f995` was **REJECTED — process/scope violation + correction required**; it is NOT
  Owner-authorized, NOT merged, must never be pushed/published/merged/amended, and is preserved only as historical evidence;
  this candidate is fresh with a new SHA + new tree and reuses only the independently-reviewed technical substance.) **D3 — Core
  Domain-Neutrality is now DEFINED by a governance-only CONTRACT CANDIDATE** (dedicated record:
  `docs/governance/D3_CORE_DOMAIN_NEUTRALITY_FORMAL_CONTRACT.md`) covering exactly **D3-A** (`engine/safety_signal.py`), **D3-B**
  (`engine/path_n_questions.py`), **D3-D** (`engine/domain_rules.py`), and explicitly **excluding D3-C** (independently verified
  remediated by §5-I2 `domain_activation.py` + P6-1 `domain_label.py`; `web/app.py` + `web/domain_label.py` unchanged absent
  fresh regression evidence). It **consumes — never duplicates** — the CLOSED canonical owners `engine/domain_registry.py`
  (§5-I1) + `engine/domain_activation.py` (§5-I2; `electronics_electrical` = the ONLY activated specialist domain; recognition ≠
  activation). Required meaning of neutrality: the core can safely support another governed domain (NOT "electronics content
  forbidden"). Frozen invariants (12); likely RED-driven boundary = the three engine modules + focused tests; prohibited:
  `web/app.py`, `web/domain_label.py`, `domains/iot_electronics/**`, new packs/activation/persistence/schema/commercial/router.
  ONE BOUNDED D3 INCREMENT; genuine RED→GREEN + load-bearing mutation probes + create-a-merge-commit + post-merge verification
  required at implementation. **DOCUMENTED NO-VALID-RED** for this contract gate. **D3 = CONTRACT CANDIDATE ONLY — it becomes
  the authoritative contract-of-record only if this exact accepted candidate is merged and post-merge verified; D3
  implementation = NOT started / NOT authorized by this gate; NO domain activated; D8 / `iot_electronics` = OPEN / Owner-reserved
  (blocks IoT activation only); Phase 8 = FORMALLY CLOSED / AUTHORITATIVE; Phase 9 / Phase 10 = NOT AUTHORIZED; PSRR = NOT
  EXECUTED; deployment / production = NOT AUTHORIZED.** Owner product/policy decisions required before D3 implementation: NONE —
  only explicit D3 implementation-gate authorization after contract acceptance.
  **The D3 contract is now ACCEPTED / MERGED (PR #434, merge `2dbde37a3c409356691a17fd868f90b087df417c`; merge tree = accepted
  candidate tree, post-merge verified), and `D3` — Core Domain-Neutrality is now IMPLEMENTED as a governance-only IMPLEMENTATION
  CANDIDATE (RED → GREEN)** — the three shared-core couplings corrected via minimum-path edits to exactly three existing engine
  seams + one new focused test: **D3-A** `engine/safety_signal.py` (the signal's `domain_context` reflects the actual §5-I2
  session domain and is no longer force-mapped to the electronics MVP for a non-electronics context; electronics-owned safety
  CUES unchanged); **D3-B** `engine/path_n_questions.py` (`get_served_question` / `get_path_n_question` gain an optional canonical
  `domain` identity; the Electronics-owned Path-N artifact is served only for the Electronics domain or the `None` default, and a
  recognized non-electronics identity is not silently served Electronics content — no parallel question framework); **D3-D**
  `engine/domain_rules.py` (`infer_domain` consumes the §5-I2 activation policy so an ACTIVATED domain wins a classification tie
  and a RECOGNIZED_NOT_ACTIVATED domain can never become effective activated routing/admission authority; prior priority kept
  only as a backward-compatible no-activated-tie fallback). Canonical owners **consumed, never duplicated** (`domain_registry.py`
  §5-I1 + `domain_activation.py` §5-I2; no new registry/activation/router/orchestrator/question framework). Behavioral RED (4
  seam defects, grounded in the real seams; no "delete the word electronics" tests) → GREEN: **D3 focused 7 / focused
  regressions 167 / web-admission consumers 87 (2 skipped) / full suite 2258 passed / 3 skipped / 1 xfailed / 0 failed** (2251
  baseline + 7); **three load-bearing mutation probes** each turned the targeted test RED and were restored byte-identical.
  **Scope invariants proven:** changed paths = the three engine seams + the new test only; `web/app.py` + `web/domain_label.py`
  (D3-C) UNCHANGED; `domains/iot_electronics/**` (D8) UNCHANGED; `activated_domains() == ['electronics_electrical']` (only);
  no persistence/schema/commercial/quota/AccessGrant/auth diff; OD-N + fail-closed preserved. **D3 = IMPLEMENTATION CANDIDATE
  ONLY — NOT closed** (D3 formal closure is a separate gate after this candidate is independently reviewed → Owner-accepted →
  merged (create-a-merge-commit) → post-merge verified → remaining-obligation review); **NO domain activated; D8 OPEN /
  Owner-reserved; Phase 8 = FORMALLY CLOSED; Phase 9 / Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment / production =
  NOT AUTHORIZED.**
  **The D3 implementation is now ACCEPTED / MERGED (PR #435, merge `e51eaf7eee001ef6012579852c8da7cbeda8e144`; merge tree =
  accepted candidate tree `f027c93`, post-merge verified; independent review ACCEPT WITH NON-BLOCKING OBSERVATIONS), and `D3` —
  Core Domain-Neutrality is now FORMALLY CLOSED as a governance-only CLOSURE CANDIDATE** (prerequisite closure only;
  authoritative if/when merged; dedicated record `docs/governance/D3_CORE_DOMAIN_NEUTRALITY_FORMAL_CLOSURE_RECORD.md`).
  Live-verified at `e51eaf7`: D3-A (mechanical `domain_context` = mechanical; electronics preserved), D3-B (foreign domain served
  None; electronics/None unchanged), D3-D (tie → electronics_electrical; recognition ≠ activation); fresh runs D3 focused 7 /
  full suite 2258 passed / 3 skipped / 1 xfailed / 0 failed. Canonical owners consumed not duplicated (domain_registry §5-I1 +
  domain_activation §5-I2); D3-C (`web/app.py`, `web/domain_label.py`) not reopened; D8 (`domains/iot_electronics/**`) untouched /
  Owner-reserved; `activated_domains() == ['electronics_electrical']` (only). **Three mandatory future prerequisites REGISTERED
  (not authorized here):** (1) **Path-N caller propagation** — `engine/progression_loop.py` must thread canonical domain identity
  into the Path-N caller chain **BEFORE ANY SECOND / NON-ELECTRONICS DOMAIN ACTIVATION** (non-blocking today: electronics is the
  only activated domain); (2) **multi-activated tie precedence** — a governed cross-activated-domain tie/conflict policy is
  required **BEFORE MORE THAN ONE SPECIALIST DOMAIN CAN BE ACTIVATED** (the current `sorted(activated_tied)[0]` is deterministic
  only with one activated domain); (3) **Phase-9 Capability Overlap & Preservation Audit** — required **BEFORE THE FIRST PHASE-9
  ACTIVATION CONTRACT** (classify proposed capabilities against existing canonical owners; likely a Phase-9 Technical Quality
  Standard). **D3 = FORMALLY CLOSED / AUTHORITATIVE (prerequisite closure only; no active D3 increment remains); Phase 9 remains
  INACTIVE / NOT AUTHORIZED (D3 closure does NOT auto-open a Phase-9 contract or activate any domain); Phase 10 = NOT AUTHORIZED;
  PSRR = NOT EXECUTED; deployment / production = NOT AUTHORIZED.**
  **Phase-9 preparation — Capability Overlap & Preservation Audit + Architecture/Extensibility Addendum COMPLETED (read-only), and
  the Phase-9 Technical Quality Standard is now DEFINED by a CORRECTED governance-only CONTRACT CANDIDATE (P9-QS).** The read-only
  audit + addendum (session-level **review/development inputs, not committed repository authority**) concluded that 5 of 6
  proposed Phase-9 capabilities reuse existing canonical owners and only a future deterministic-calculation capability is
  genuinely new, favoring one consolidated standard. **P9-QS** (record:
  `docs/governance/P9_QS_PHASE_9_TECHNICAL_QUALITY_STANDARD_CONTRACT.md`) is the corrected reissue that **supersedes the REJECTED
  prior candidate `6a3e25df79bfe2399474a1ecf9154ca3ccfbe307`** (which **remains historical rejected evidence only — NOT modified /
  NOT merged / NOT reused**); this is a NEW independent candidate from authoritative parent `99c0855`. Corrections applied:
  **B1** — the future deterministic-calculation capability is assigned **no CAP number** (unnumbered *future deterministic-calculation
  adapter gate*); `CAP-06` is repository-canonical for the *Multi-Axis Invention Readiness Dashboard* and MUST NOT be reused for
  it. **B2** — the **Output-Language override capability is DEFERRED / NOT IMPLEMENTED / NOT AUTHORIZED / separately governed
  (D-P6-17 is the accepted decision, not the capability) and is NOT a pre-new-domain activation prerequisite**; the actual
  repository-authoritative pre-new-domain prerequisite is the separate **Domain Registry validation hardening (D-P6-14 / §5-I1,
  already CLOSED)**. Non-blocking: **O1** audit-as-input wording; **O2** `P9-PREREQ-A/B` stated as convenient labels for the
  already-D3-registered obligations (not pre-existing canonical identifiers); **O3** a §4b reference to the existing **D13
  knowledge-governance / evidence-governance / licensing** family for future Domain-Pack knowledge sources (reference/reuse only,
  no new framework, no CAP-12/CAP-13/WS-PFV duplication). The standard expresses the Domain Capability Contract **through** the
  canonical Domain Registry (§5-I1; no second registry), preserves the activation-quality principle, and keeps all deferred items
  (deterministic-calculation adapter, Units, CAP-12/CAP-13/WS-PFV, D4, D8, Output-Language) as REFERENCE-ONLY / DEFERRED
  placeholders. **P9-QS = CONTRACT CANDIDATE ONLY — authoritative only if this exact accepted candidate is merged and post-merge
  verified; `OWNER_DECISION_REGISTER.md` unchanged; NO runtime/test/schema/prompt/benchmark/web diff; NO domain activated; the
  future deterministic-calculation capability remains UNNUMBERED / DEFERRED; Output-Language remains separately governed /
  DEFERRED and NOT an activation prerequisite; D8 Owner-reserved; Phase 9 remains INACTIVE / NOT AUTHORIZED (accepting the
  standard does NOT open a Phase-9 implementation contract); Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment /
  production = NOT AUTHORIZED.**
  **P9-QS is now AUTHORITATIVE (merged PR #437, tip `f08dd2e0319b2777c47dad9cdb49c05d106bc7a0` = two-parent merge of `99c0855` +
  the corrected P9-QS candidate `2f435c68`, post-merge verified), and Phase 9 has BEGUN — but only through the newly authorized
  bounded `P9-E1` / `P9-PREREQ-A` contract gate, now DEFINED by a governance-only IMPLEMENTATION CONTRACT CANDIDATE.** P9-E1
  (record: `docs/governance/P9_E1_PATH_N_CALLER_DOMAIN_PROPAGATION_CONTRACT.md`) closes the mandatory D3-registered Path-N
  production-caller domain-propagation prerequisite carried by P9-QS §16. **Live evidence (verified at `f08dd2e`): the prerequisite
  is STILL REQUIRED** — the Path-N seam is already domain-aware (`engine/path_n_questions.py`) but the production callers in
  `engine/progression_loop.py` drop the in-scope `domain` at three `get_path_n_question(...)` sites (line 232 in `get_question`;
  lines 269 and 273–274 in `get_display_question`), so a recognized-not-activated foreign-domain Path-N session
  (`get_question("mechanical", "MECHANISM_COMPLETENESS", 0, path="N")`) is served the Electronics artifact text while the seam
  already returns `None` for that domain; canonical domain identity is available at every caller (`web/app.py:1566`,
  `progression_loop.py:904/944/981`, `scripts/run_cli.py:79` pass `state.domain`), and those three seam calls are the complete
  production-caller set. **Bounded implementation (LATER, separate gate — NOT executed here):** thread `domain=domain` into those
  three sites only; no signature/seam/registry/activation/web/CLI change; Electronics/`None` behavior and stall reframe preserved
  and correctly suppressed for a foreign domain; behavioral RED→GREEN tests with the neutral `"mechanical"` fixture. **P9-E1 =
  IMPLEMENTATION CONTRACT CANDIDATE ONLY — authoritative only if this exact accepted candidate is merged and post-merge verified;
  the P9-E1 runtime + tests are a separate later gate, NOT authorized here; `OWNER_DECISION_REGISTER.md` unchanged; ZERO
  runtime/test/schema/prompt/benchmark/web diff; NO new domain activated (`activated_domains() == ['electronics_electrical']`); NO
  domain selected; P9-E2 / P9-PREREQ-B NOT implemented (separate future gate; `sorted(activated_tied)[0]` untouched); D4 NOT
  executed; D8 Owner-reserved; Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment / production = NOT AUTHORIZED.**
  **The P9-E1 contract is now AUTHORITATIVE (merged PR #438, tip `8fbc239c98ab89e596554a8c52c7e7b1c5b22ad5` = two-parent merge of
  `f08dd2e` + the P9-E1 contract candidate `3b485131`), and `P9-E1` / `P9-PREREQ-A` — Path-N Production Caller Domain Propagation
  is now IMPLEMENTED as an IMPLEMENTATION CANDIDATE (RED→GREEN).** The bounded runtime fix threads the canonical `domain` (already
  the first parameter of both callers) into the existing three `get_path_n_question(...)` calls in `engine/progression_loop.py`
  as `domain=domain` — `get_question` (path=="N") selection and the two `get_display_question` exhaustion reads
  (`current`/`previous`); `engine/path_n_questions.py` unchanged; no domain branching, no second router, no
  activation-policy/Registry/Domain-Pack/D8/P9-E2 change. Behavioral RED→GREEN via
  `tests/test_p9e1_path_n_caller_domain_propagation.py` (6 tests): baseline RED-1 (`get_question` foreign recognized domain served
  Electronics artifact text) + RED-2 (`get_display_question` foreign domain served the Electronics `_STALL_REFRAME`) both FAILED
  pre-edit → GREEN post-edit; guards preserve Electronics artifact text + stall reframe + the `domain=None` seam default, and
  assert the fixture `mechanical` is `recognized_not_activated`/not-activated. Per-site proof (honest): site-1 mutation
  individually caught; sites 2+3 jointly load-bearing (either domain-aware reframe read alone suppresses the erroneous foreign
  reframe — defense-in-depth), joint site-2+3 mutation (the original defect) caught by RED-2; no probe left in the candidate.
  **Full suite fresh: 2264 passed / 3 skipped / 1 xfailed / 0 failed** (2258 baseline + 6 new). **P9-E1 = IMPLEMENTATION CANDIDATE
  ONLY — authoritative only if this exact accepted candidate is merged and post-merge verified; formal P9-E1 closure is a separate
  subsequent gate; `OWNER_DECISION_REGISTER.md` unchanged; changed runtime/test paths = `engine/progression_loop.py` + the new
  test only (plus governance current-truth registration, per D3 implementation precedent); NO new domain activated
  (`activated_domains() == ['electronics_electrical']`); NO domain selected; P9-E2 NOT implemented; D4 NOT executed; D8
  Owner-reserved; Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment / production = NOT AUTHORIZED.**
  **The P9-E1 implementation is now AUTHORITATIVE (merged PR #439, tip `f22085066d8a0b2b1e90c04c6808f44f606316e6` = two-parent
  merge of base `8fbc239` + the accepted implementation candidate `8ebc1c1a`; merge tree `14c286ba` == candidate tree; 5 files /
  +251 / −5; `git diff --check` clean; independent review ACCEPT WITH NON-BLOCKING OBSERVATIONS), and `P9-E1` / `P9-PREREQ-A` —
  Path-N Production Caller Domain Propagation is now FORMALLY CLOSED / SATISFIED as a governance-only CLOSURE CANDIDATE**
  (prerequisite closure only; authoritative if/when merged; record
  `docs/governance/P9_E1_PATH_N_CALLER_DOMAIN_PROPAGATION_FORMAL_CLOSURE_RECORD.md`). Live-verified at `f220850`:
  `support_state("mechanical") == "recognized_not_activated"`; `activated_domains() == ['electronics_electrical']`; a foreign
  recognized-not-activated domain on the Path-N flow no longer receives the Electronics artifact text (`get_question` → generic)
  nor the Electronics `_STALL_REFRAME` at exhaustion (`get_display_question` → generic); Electronics + `domain=None` behavior
  intact; exactly the three production `get_path_n_question(...)` sites threaded with `domain=domain`; no hidden caller. RED→GREEN
  (RED parent `8fbc239`: RED-1 foreign artifact text + RED-2 foreign stall reframe → all 6 GREEN); independently reproduced
  mutation matrix (site 1 alone → RED; site 2 alone → GREEN; site 3 alone → GREEN; sites 2+3 jointly → RED; all 3 → RED — **sites
  2+3 jointly, not individually, load-bearing; recorded honestly**); fresh full suite **2264 passed / 3 skipped / 1 xfailed / 0
  failed** (2258 baseline + 6 new). Phase-9 completeness checklist for P9-E1: no APPLICABLE/GAP remains. **`engine/domain_rules.py`
  (P9-E2 tie-break), `engine/domain_activation.py` (activation policy), and `domains/iot_electronics/**` (D8) UNCHANGED
  base→merge.** **P9-E1 / P9-PREREQ-A = FORMALLY CLOSED / SATISFIED (authoritative if/when this closure candidate is merged and
  post-merge verified); `OWNER_DECISION_REGISTER.md` unchanged; ZERO runtime/test diff in the closure gate; NO new domain
  activated; NO domain selected; Electronics remains the only activated specialist domain; recognition ≠ activation; P9-E2 /
  P9-PREREQ-B = SEPARATE / UNSATISFIED / NOT STARTED; D4 = SEPARATE / UNEXECUTED; D8 Owner-reserved; Phase 10 = NOT AUTHORIZED;
  PSRR = NOT EXECUTED; deployment / production = NOT AUTHORIZED.** Closing P9-E1 does NOT auto-advance Phase 9; recommended next
  major gate = **P9-E2 / P9-PREREQ-B — Multi-Activated Domain Tie/Conflict Precedence** (separately governed; NOT started).
  **The P9-E1 formal closure is now AUTHORITATIVE (merged PR #440, tip `05184f9166fa3a9e45a3384be5bafccc86e05ebe` = two-parent
  merge of the P9-E1 implementation merge `f220850` + the closure candidate `6c3c65a6`; merge tree `b8b5462f` == closure tree), and
  the next bounded Phase-9 prerequisite `P9-E2` / `P9-PREREQ-B` — Multi-Activated Domain Tie/Conflict Precedence is now DEFINED by a
  governance-only CONTRACT CANDIDATE (contract-first).** P9-E2 (record:
  `docs/governance/P9_E2_MULTI_ACTIVATED_DOMAIN_TIE_PRECEDENCE_CONTRACT.md`) governs the deterministic, truthful behavior when two
  or more ACTIVATED specialist domains tie/conflict. **Live evidence (verified at `05184f91`): still required** —
  `engine/domain_rules.py::infer_domain` lines 31–33 pick `sorted(activated_tied)[0]` (incidental alphabetical precedence among
  ACTIVATED tied domains; plus the line-34 `priority` literal no-activated-tie fallback); reachable only when ≥2 specialist domains
  are activated and tie (unreachable today — only `electronics_electrical` activated). Behaviorally proven read-only
  (`_ACTIVATED_DOMAINS` monkeypatched then restored; NO real activation, NO file change): a clean `mechanical`+`medical_device`
  activated tie returns `mechanical` purely alphabetically. **Critical representation finding:** `infer_domain` returns `str |
  None`, which cannot honestly express an ambiguous tie / tied candidate set / no-governed-winner / genuine multi-domain (Case 4);
  the contract explicitly calls out a bounded, **separately-reviewed representation sub-gate `P9-E2-R`** rather than hiding it.
  Precedence policy: Case 1 (single winner) unchanged; Case 3 (tie, no governed precedence) → explicit ambiguous/unresolved outcome
  (safe default, no silent pick); Case 4 → surface D4 need truthfully; forbidden answers = alphabetical/file/registration/iteration/
  dict order, hardcoded Electronics preference, model guess, silent default. RED-1…RED-6 designed (not implemented); Phase-9
  completeness checklist fully dispositioned (no APPLICABLE/GAP); **first-new-domain implication (verified): Electronics is already
  activated, so the first new-domain activation creates a >1-activated state — P9-E2 is a MANDATORY prerequisite before the first
  actual new-domain activation.** **P9-E2 = CONTRACT CANDIDATE ONLY (contract-first) — authoritative only if this exact accepted
  candidate is merged and post-merge verified; the P9-E2 runtime, the P9-E2-R representation sub-gate, and their tests are separate
  later gates, NOT authorized here; `OWNER_DECISION_REGISTER.md` unchanged; ZERO runtime/test/domain/schema/prompt/benchmark/web
  diff; NO new domain activated (`activated_domains() == ['electronics_electrical']`); NO domain selected; P9-E1 remains FORMALLY
  CLOSED / SATISFIED; D4 = SEPARATE / UNEXECUTED; D8 Owner-reserved; Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment /
  production = NOT AUTHORIZED.**
  **The P9-E2 contract is AUTHORITATIVE (merged PR #441, tip `47fce397dfd21175a0012b652f8dde6548e31432`), and the bounded `P9-E2-R`
  — Ambiguity / Multi-Domain Result Representation sub-gate is now DEFINED by a CORRECTED governance-only CONTRACT CANDIDATE
  (contract-first) that supersedes the Grill-REJECTED prior candidate `1b817f06e7d86b3af6e44b298bcf7a31102e5e32`** (which remains
  **immutable historical evidence only — NOT amended / NOT merged / NOT reused**). The corrected candidate (record:
  `docs/governance/P9_E2_R_AMBIGUITY_MULTI_DOMAIN_RESULT_REPRESENTATION_CONTRACT.md`) incorporates all MATERIAL Mandatory Grill
  findings: legacy `infer_domain` wrapper **FAILS LOUD** (raises, never silent `None`) on AMBIGUOUS_TIE/MULTI_DOMAIN_NEEDS_D4 +
  RED-R9; **all six `web.app.infer_domain` monkeypatch surfaces migrated + load-bearing** (test_web_app.py 563/575/589/661/701/790);
  **architecture-guardrail reconciliation** (frozen `str | None` vs fail-loud richer kinds); `classify_domain` richer canonical
  entry with one classifier owner; **web + CLI dispatch by `result.kind`** (never truthiness/string comparison) + RED-R10
  (`/start × MULTI`) + RED-R11 (CLI bounded stop); **`state.domain` remains a resolved string**; strengthened invariants (unique
  ids, ≥2 candidates, all-activated, mutual exclusion, duplicate rejection, immutable); **deterministic non-LLM `reason`**;
  **defensive fail-loud type boundary** vs silent `DomainClassification` swallowing; **line-34 future Nth-domain fallthrough hazard
  registered** as a mandatory pre-Nth-domain obligation (no hazard today); future implementation **classified
  architecture-affecting / higher-governance**; D4 marker-only, no-analysis-implied wording. **Confirmed gap (verified at
  `47fce39`):** `infer_domain -> str | None` conflates the truths and `web/app.py /start` admits `domain is None` as an electronics
  session (lines 1393–1394); guardrail freezes the `str | None` signature; activated tie unreachable today (only electronics
  activated). Architecture retained (minimum-sufficient): `DomainResultKind {SINGLE, NONE, AMBIGUOUS_TIE, MULTI_DOMAIN_NEEDS_D4}` +
  immutable `DomainClassification` + canonical `classify_domain(...)` + legacy fail-loud `infer_domain` wrapper. Phase-9
  completeness checklist fully dispositioned (no acceptance-relevant APPLICABLE/GAP). **P9-E2-R = CORRECTED CONTRACT CANDIDATE ONLY
  (contract-first) — authoritative only if this exact accepted candidate is merged and post-merge verified; the P9-E2-R runtime +
  tests are a separate later architecture-affecting gate, NOT authorized here; the Grill-rejected `1b817f06` remains immutable
  historical evidence only; `OWNER_DECISION_REGISTER.md` unchanged; ZERO runtime/test/domain/web/CLI/schema diff; NO new domain
  activated (`activated_domains() == ['electronics_electrical']`); NO domain selected; P9-E2 tie precedence remains a separate later
  runtime gate; P9-E1 remains FORMALLY CLOSED / SATISFIED; D4 = SEPARATE / UNEXECUTED; D8 Owner-reserved; Phase 10 = NOT AUTHORIZED;
  PSRR = NOT EXECUTED; deployment / production = NOT AUTHORIZED.**
  **The corrected P9-E2-R contract is now AUTHORITATIVE (merged PR #442, tip `3434c2350b4c08cabcc362d175947a311070b493` = two-parent
  merge of `47fce397` + the corrected candidate `3cbb16b6`; merge tree `05831989` == candidate tree), and `P9-E2-R` — Ambiguity /
  Multi-Domain Result Representation is now IMPLEMENTED as an IMPLEMENTATION CANDIDATE (RED→GREEN; architecture-affecting).** The
  minimum-sufficient representation seam (NO tie-policy change): `engine/domain_rules.py` adds `DomainResultKind {SINGLE, NONE,
  AMBIGUOUS_TIE, MULTI_DOMAIN_NEEDS_D4}`, deterministic `DomainAmbiguityReason`, `AmbiguousDomainResultError`, and an immutable frozen
  `DomainClassification` (all invariants enforced at construction); canonical `classify_domain(...)` = single classifier owner (today
  SINGLE/NONE only, behavior-equivalent); legacy `infer_domain(...) -> str | None` = thin wrapper, total over SINGLE/NONE and
  FAIL-LOUD over richer kinds. `web/app.py` `/start` + `scripts/run_cli.py` migrated to dispatch by `result.kind` (never
  truthiness/string comparison): SINGLE byte-identical, NONE unchanged, AMBIGUOUS_TIE + MULTI_DOMAIN_NEEDS_D4 fail closed via an
  existing safe surface (no session / no electronics admission / no winner / no D4 / no new UX / no implied multi-domain analysis);
  `state.domain` stays a resolved string. `engine/domain_activation._resolve_pack_id` gains a defensive fail-loud `TypeError` for
  non-string domain ids. `ARCHITECTURE_GUARDRAILS.md` §9 reconciled (classify_domain richer canonical entry; infer_domain legacy /
  fail-loud; new admission callers must use classify_domain; one owner) — frozen `str | None` signature test NOT weakened. RED→GREEN
  via `tests/test_p9e2r_result_representation.py` (19) + 4 guardrail tests (RED-R1…R11 + invariants); six load-bearing mutation probes
  caught RED incl. the migrated-monkeypatch detachment (the six `web.app.infer_domain` monkeypatches migrated to
  `web.app.classify_domain`, proven load-bearing); **fresh full suite 2287 passed / 3 skipped / 1 xfailed / 0 failed** (2264 baseline
  + 23 new). Activated ties simulated with self-restoring `_ACTIVATED_DOMAINS` doubles (NO real activation). Phase-9 completeness
  checklist: no acceptance-relevant APPLICABLE/GAP. **P9-E2-R = IMPLEMENTATION CANDIDATE ONLY — authoritative only if this exact
  accepted candidate is merged and post-merge verified; formal closure (if precedent requires) is a separate subsequent gate;
  `OWNER_DECISION_REGISTER.md` unchanged; no persistence/schema/public-API/export/Domain-Pack change; NO P9-E2 tie-policy change; NO
  new domain activated (`activated_domains() == ['electronics_electrical']`); NO domain selected; P9-E2 tie precedence remains a
  separate later runtime gate; P9-E1 remains FORMALLY CLOSED / SATISFIED; D4 = SEPARATE / UNEXECUTED; D8 Owner-reserved; Phase 10 =
  NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment / production = NOT AUTHORIZED.**
  **The authoritative repository parent remains `b42a3e6c246b98d425460f80d91d8de12d554039` (PR #443; P9-E2-R implementation
  authoritative), and `P9-E2-R` — Ambiguity / Multi-Domain Result Representation is now FORMALLY CLOSED / SATISFIED as a
  governance-only CLOSURE CANDIDATE** (record:
  `docs/governance/P9_E2_R_AMBIGUITY_MULTI_DOMAIN_RESULT_REPRESENTATION_FORMAL_CLOSURE_RECORD.md`). **The closure candidate is NOT
  yet authoritative and NOT yet merged; the candidate SHA is not a live authoritative tip** — closure becomes authoritative only
  after Mandatory Grill → independent external exact-candidate review → Owner exact-candidate acceptance → SHA-preserving
  publication → PR → pre-merge verification → CREATE A MERGE COMMIT → post-merge verification. P9-E2-R established the representation
  seam only — it **did NOT implement the P9-E2 tie policy** (`classify_domain` constructs SINGLE/NONE only; richer kinds
  representable/consumable but classifier-produced only via the separate later P9-E2 runtime; `sorted(activated_tied)[0]` +
  priority fallback unchanged; no multi-domain analysis). Fresh closure evidence at `b42a3e6`: full suite 2287 passed / 3 skipped /
  1 xfailed / 0 failed; focused 37 passed; six load-bearing mutation probes all CAUGHT RED. **NO new domain activation**
  (`activated_domains() == ['electronics_electrical']`); **NO domain selected.** **The Retrospective Adversarial Architecture Audit
  is now REGISTERED by this candidate as a future PRE-ACTIVATION obligation (A/B/C/D/E classification; material C/D/E
  dispositioned/independently validated BEFORE first new-domain activation) — NOT executed.** Carry-forward: CF-1 P9-E2 runtime tie
  policy still pending; CF-2 shared AMBIGUOUS/MULTI public message NON-BLOCKING (carried to P9-E2); CF-3 non-activated priority
  fallback (`engine/domain_rules.py` line 142) — no reachable defect today, MANDATORY before first Nth-domain
  registration/activation; CF-4 D4 remains separate. **`OWNER_DECISION_REGISTER.md` unchanged; ZERO runtime/test/domain/web/CLI/
  schema/guardrail diff in the closure gate; P9-E2 tie precedence remains a separate later runtime gate; P9-E1 remains FORMALLY
  CLOSED / SATISFIED; D4 = SEPARATE / UNEXECUTED; D8 Owner-reserved; Phase 10 = NOT AUTHORIZED; PSRR = REGISTERED / NOT EXECUTED;
  deployment / production = NOT AUTHORIZED.**
  **`P9-E2` / `P9-PREREQ-B` — Multi-Activated Domain Tie/Conflict Precedence is now IMPLEMENTED as a CORRECTED IMPLEMENTATION
  CANDIDATE**, built fresh from the authoritative parent `c11482db7240b5ac628e77cd061f8d5de6df40ee` (live tip re-verified; 0 newer),
  and it **supersedes the REJECTED prior candidate `3255c4ba1ca6ae50e0c3f20d7f0d4c8ef1fa223c`** (Mandatory Grill `GRILL FAIL —
  MATERIAL CONTRACT CORRECTION REQUIRED`: sound runtime, but a FALSE `/start` strong-unsupported "masked for all real ties"
  reachability claim, an omitted achievable distinguishing RED-E2-10, and a misdescribed multi-activation `/start` delta). `3255c4ba`
  is immutable rejected evidence — NOT reused/amended/rebased/built upon. Bounded runtime change via the canonical `classify_domain`
  seam (CF-1): `len(activated_tied) == 0` → unchanged priority fallback; `== 1` → `SINGLE`; **`>= 2` → `AMBIGUOUS_TIE(selected=None,
  candidates=canonical activated tied set, reason=EQUAL_SCORE)`** — no arbitrary/alphabetical/Electronics/LLM winner;
  `MULTI_DOMAIN_NEEDS_D4` NOT manufactured (D4 separate); only ACTIVATED domains in the set (D3-D). **CORRECTED reachability truth:**
  `/start` calls `classify_domain` FIRST and fails an `AMBIGUOUS_TIE` closed to UNSUPPORTED (200, no session) BEFORE the separate
  `_has_strong_unsupported_evidence` gate, which is an independent later layer over SINGLE/NONE inputs only; a multi-activated tie
  therefore fails closed via the ambiguity branch regardless of strong-unsupported token membership (verified against source:
  `strong("circuit and hinge") == strong("hinge and app") == False`). **RED→GREEN:** NEW
  `tests/test_p9e2_multi_activated_tie_precedence.py` (20 tests) — 12 distinguishing RED on parent incl. **E2-10 a REAL `/start`
  production-path RED** (`circuit and hinge` under an elec+mech double → parent ADMITS an electronics session (302); candidate fails
  closed 200 UNSUPPORTED, no session), **E2-10b** (`hinge and app` mech+sw → parent GUIDANCE; candidate UNSUPPORTED), **E2-11**
  (`gear and catheter` mech+med → CLI bounded stop) + 8 honest GREEN GUARDS; **9 load-bearing mutation probes all CAUGHT RED**
  (bytecode-isolated), incl. NEW probe 9 (neutralize real `/start` AMBIGUOUS branch → E2-10/10b RED). **Full suite 2307 passed /
  3 skipped / 1 xfailed / 0 failed** (= 2287 parent + 20). **Scope:** `engine/domain_rules.py` (tie branch + corrected docstring) +
  the NEW test + governance current-truth (roadmap + `ACTIVE_INCREMENT_CONTRACT.md` + this file); **`web/app.py` ZERO diff** (runtime
  found safe); ZERO diff `scripts/run_cli.py`, `engine/domain_activation.py`, `ARCHITECTURE_GUARDRAILS.md`,
  `OWNER_DECISION_REGISTER.md`, `domains/**`, `schemas/**`, `database/**`. **Backward-compat (truthful):** electronics-only activation
  today → ≥2 activated tie production-unreachable → ZERO current production delta; under a FUTURE governed second-domain activation,
  non-intercepted ties change OLD incidental-SINGLE/possible-admission → NEW AMBIGUOUS_TIE/fail-closed — an INTENDED future
  correction, not a regression; `/start` is NOT universally "unchanged" under future multi-activation. **Carry-forwards:** CF-2 &
  CF-3 retained; CF-5 Retrospective Adversarial Architecture Audit remains a future pre-activation obligation; **NEW CF-6 — Web
  pre-classifier / strong-unsupported reachability & admission interaction (distinct from CF-2), a FUTURE
  PRE-SECOND-DOMAIN-ACTIVATION obligation, NOT executed here.** **`OWNER_DECISION_REGISTER.md` UNCHANGED. P9-E2 = CORRECTED
  IMPLEMENTATION CANDIDATE ONLY — NOT closed / NOT authoritative; NO domain activated (`activated_domains() ==
  ['electronics_electrical']`); NO domain selected; MULTI_DOMAIN_NEEDS_D4 NOT manufactured; D4 = SEPARATE / UNEXECUTED; D8
  Owner-reserved; Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment / production = NOT AUTHORIZED.** Next required gate: a
  **NEW Mandatory Grill on this exact new candidate** (any material finding rejects it as-is — NEW SHA/tree/bundle/Grill/independent
  review, no amendment).
  **The P9-E2 implementation is now AUTHORITATIVE (merged PR #445, tip `f33663710d6edf506a082b1bfa2f02e9c3fef7ac` = two-parent merge
  of `c11482db…` + the accepted corrected candidate `85fda813…`; merge tree `0bffe3f7…` == candidate tree; scope 5 files / +546 /
  −17; `git diff --check` CLEAN; 0 newer), and `P9-E2` / `P9-PREREQ-B` — Multi-Activated Domain Tie/Conflict Precedence is now
  FORMALLY CLOSED / SATISFIED as a governance-only CLOSURE CANDIDATE** (record:
  `docs/governance/P9_E2_MULTI_ACTIVATED_DOMAIN_TIE_PRECEDENCE_FORMAL_CLOSURE_RECORD.md`). **The closure candidate is NOT yet
  authoritative and NOT yet merged; the candidate SHA is not a live authoritative tip** — closure becomes authoritative only after
  Mandatory Grill → independent external exact-candidate review → Owner exact-candidate acceptance → SHA-preserving publication → PR
  → pre-merge verification → CREATE A MERGE COMMIT → post-merge verification. Accepted implementation review chain: rejected
  candidate `3255c4ba` (Grill FAIL — never published/accepted/merged; not an ancestor) → accepted corrected candidate `85fda813`
  (built from `c11482d`) → Grill PASS WITH NON-BLOCKING HARDENING (blocking NONE) → independent review ACCEPT WITH NON-BLOCKING
  OBSERVATIONS (blocking NONE) → Owner-accepted → published → PR #445 → post-merge verified. Bounded tie-precedence policy via the
  canonical `classify_domain` seam (CF-1 SATISFIED): 0 activated tied → non-activated priority fallback unchanged; 1 → SINGLE; ≥2 →
  AMBIGUOUS_TIE(selected=None, complete canonical activated set, EQUAL_SCORE); no arbitrary/alphabetical/Electronics/LLM winner;
  MULTI_DOMAIN_NEEDS_D4 NOT fabricated (D4 separate); only ACTIVATED domains (D3-D). Fresh closure evidence reproduced at `f336637`:
  full suite **2307 passed / 3 skipped / 1 xfailed / 0 failed**; focused **57 passed**; **nine load-bearing mutation probes all
  CAUGHT RED**, bytes restored. Canonical-owner reconciliation: `classify_domain` = canonical owner; `infer_domain` = legacy
  fail-loud wrapper (later authoritative P9-E2-R architecture governs the name evolution; old P9-E2 contract NOT rewritten/amended).
  **Carry-forward:** CF-1 SATISFIED by this gate's subject; **CF-2** shared AMBIGUOUS/MULTI public message PENDING; **CF-3**
  non-activated priority fallback PENDING (retained for backward compatibility; before first Nth-domain registration/activation);
  CF-4 D4 separate; **CF-5** Retrospective Adversarial Architecture Audit PENDING (MANDATORY before first new-domain activation);
  **CF-6** Web pre-classifier / strong-unsupported reachability & admission interaction PENDING (PRE-SECOND-SPECIALIST-DOMAIN
  ACTIVATION; distinct from CF-2). Independent-review/Grill non-blocking observations carried forward, not discarded: NB-1
  stale/layered P9-E2-R wording (reconciled below); NB-2 substring signal matching (`led`/`web`; pre-existing/unchanged; carried to
  P9-QS / Retrospective Audit / CF-3/CF-6); NB-3 one mutation probe partly caught by construction invariants (non-blocking
  test-hardening; tests unchanged); NB-4 strong-unsupported vocabulary vs future activated domains (CF-6; Web unchanged); NB-5
  `domains/iot_electronics/domain.json` schema warning/skip (D8/IoT Owner-reserved; `domains/iot_electronics/**` untouched).
  **`OWNER_DECISION_REGISTER.md` UNCHANGED; ZERO runtime/test/domain/Registry/activation/web/CLI/schema/guardrail diff in this
  closure gate.** **NO new domain activated (`activated_domains() == ['electronics_electrical']`); NO domain selected; P9-E2-R
  remains FORMALLY CLOSED / SATISFIED; P9-E1 remains FORMALLY CLOSED / SATISFIED; D4 = SEPARATE / UNEXECUTED; D8 Owner-reserved;
  Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment / production = NOT AUTHORIZED.** The next required gate is the
  **Mandatory Grill on this exact immutable closure candidate**.
  **NB-1 present-truth reconciliation (P9-E2-R):** the earlier P9-E2-R block above (authored before PR #444) describes P9-E2-R
  formal closure as a governance-only closure candidate "NOT yet authoritative and NOT yet merged." That historical wording is
  **retained as legitimate history**; the **present, current truth is that the P9-E2-R formal closure is now AUTHORITATIVE** — its
  closure candidate `6bf749db` was merged via **PR #444** into `c11482db…` (the P9-E2 implementation parent), so `P9-E2-R` is
  FORMALLY CLOSED / AUTHORITATIVE at the live authoritative tip. No historical evidence is rewritten; only the present status is made
  unambiguous.
  **P9-E2 formal closure is now AUTHORITATIVE (merged PR #446, tip `54a5565bdcdfa37ff247ceb9e806bd5b2b42cb9d` = two-parent merge of
  `f336637` + the accepted P9-E2 closure candidate `23f746fa`; merge tree `cf4198c5` == closure candidate tree; 0 newer), so
  `P9-E2` / `P9-PREREQ-B` is FORMALLY CLOSED / SATISFIED / AUTHORITATIVE. The next governed step (Phase-9 pre-activation sequencing
  Gate 0) is the mandatory `CF-5` Retrospective Adversarial Architecture Audit, which is now DEFINED by a governance-only
  CONTRACT / ENTRY CANDIDATE** (record: `docs/governance/CF5_RETROSPECTIVE_ADVERSARIAL_ARCHITECTURE_AUDIT_CONTRACT.md`). CF-5 was
  registered (P9-E2-R closure §5; re-affirmed P9-E2 closure §7) and is MANDATORY before first new-domain activation; it is generic
  to inherited architecture and requires no selected domain to enter. The candidate defines Audit entry, minimum scope
  (shared-core; Registry; activation; classifier ownership `classify_domain`; scoring/signals; hardcoded fallback (CF-3); Web
  strong-unsupported (CF-6); public-message truthfulness (CF-2); Web/CLI/core consistency; persistence; domain isolation;
  schema/version; extensibility; hidden Electronics assumptions; test architecture; reachable-on-activation debt), the preserved
  A/B/C/D/E finding taxonomy (no new taxonomy), the independent-validation requirement for C/D/E before reopening closed
  architecture, the correction-gate policy (C → pre-trigger prerequisite; D → bounded corrective gate; E → STOP for
  architecture/Owner decision), and Audit completion criteria. **It does NOT execute the Audit, produce findings, or
  select/qualify/activate any domain.** Separation preserved (none discharged): P9-QS AUTHORITATIVE (per-domain qualification
  separate, selection-first); CF-6 PENDING PRE-SECOND-SPECIALIST-DOMAIN ACTIVATION; CF-2 / CF-3 separate trigger-bound; D8
  Owner-reserved; D4 separate. Recommended partial-order: CF-5 → domain selection → per-domain P9-QS → CF-6/CF-2/CF-3 → explicit
  Owner activation authorization. **`OWNER_DECISION_REGISTER.md` UNCHANGED; ZERO runtime/test/domain/Registry/activation/web/CLI/
  schema/guardrail diff in this contract gate.** **CF-5 = CONTRACT/ENTRY CANDIDATE ONLY — Audit NOT executed; execution NOT yet
  authorized; the candidate does not claim the Audit is ACTIVE/COMPLETE/PASSED. NO new domain activated (`activated_domains() ==
  ['electronics_electrical']`); NO domain selected; first new-domain activation remains BLOCKED behind CF-5 completion, per-domain
  P9-QS qualification, CF-6, CF-2, CF-3, D8 (if IoT), and explicit Owner activation authorization.** The next required gate is the
  **Mandatory Grill on this exact immutable CF-5 contract candidate**.
  **The CF-5 Audit contract is now AUTHORITATIVE (merged PR #447, tip `8c38812086cfd3c17bc61ad47bba94e8b7a9de8d`; 0 newer), the CF-5
  Retrospective Adversarial Architecture Audit (Execution Gate 1) was RUN read-only producing four material findings (CF5-F001
  shared-core electronics-specific `safety_signal`; CF5-F002 Web `/start` electronics-only admission / CF-6; CF5-F003 classifier
  substring false positives; CF5-F004 hardcoded non-activated priority fallback / CF-3), and CF5-F003 was independently validated
  D — Material current issue, reachable now.** A first CF5-F003 corrective contract candidate `9857ba3e21a8bbd8d73bcde83cb85b7744d0f85b`
  was **REJECTED by Mandatory Grill (BF-1: its strict exact-whole-token / no-plural-inference rule would regress ~76 signals' plural
  forms and flip `a system of gears and levers` Mechanical→Software).** **The corrected CF5-F003 corrective contract is now DEFINED
  by a governance-only CORRECTED CORRECTIVE CONTRACT CANDIDATE** (record:
  `docs/governance/CF5_F003_CLASSIFIER_MATCHING_SEMANTICS_CORRECTIVE_CONTRACT.md`), built fresh from `8c38812` (rejected `9857ba3e`
  NOT an ancestor). It replaces the rejected rule with a **bounded plural-preserving whole-token matcher** (tokenize on `[a-z0-9]+`;
  single-word signal matches a token equal to the signal or its bounded plural `+"s"`/`+"es"`, nothing else; multi-word = contiguous
  whole-token sequence, bounded plural on the final token only). Collision guard validated (false positives `controlled`/`compiled`/
  `patriotic`/`concurrent`/`hearth` stay false — whole-token, not substring); plural inventory reproduced (76 single-word + 5
  multi-word signals; `diagnosis` sibilant irregular-plural not caught today → no obligation; no cross-pack `+s`/`+es` collision).
  Mandatory GREEN preservation explicitly repairs BF-1 (`LEDs`/`sensors`/`circuits`/`resistors`/`PCBs`; `gears`/`levers`;
  `catheters`; `apps`/`databases`/`APIs`; `a system of gears and levers` stays Mechanical) plus RED (real Web/CLI reproductions) and
  mutation probes (over-broad plural rule → RED). **It implements NOTHING**; scope = `engine/domain_rules.py` matching only; it does
  NOT solve F001/F002/F004, does NOT close CF-5, activates no domain. **CF5-F003 = VALIDATED D / corrective gate OPEN; prior
  `9857ba3e` = REJECTED (BF-1); CF5-F001 / CF5-F002 / CF5-F004 remain UNCHANGED open C findings; CF-5 remains OPEN.** **`OWNER_
  DECISION_REGISTER.md` UNCHANGED; ZERO runtime/test/domain/schema/web/CLI/guardrail diff; `activated_domains() ==
  ['electronics_electrical']`; NO domain selected; first new-domain activation remains BLOCKED.** **CF5-F003 corrected corrective
  contract = CANDIDATE ONLY; IMPLEMENTATION NOT STARTED.** The next required gate is the **Mandatory Grill on this exact immutable
  corrected CF5-F003 contract candidate**.
  **The corrected CF5-F003 corrective contract v2 is now AUTHORITATIVE (merged PR #448, tip
  `cfdc58cc798d02b8d9f50030b627a8302e0de889`; 0 newer). A CF5-F003 implementation candidate
  `a29789a948829133812d1a80b297e9b5b907cdc1` (whole-token + bounded `+s`/`+es` plural; Creator Grill PASS WITH NON-BLOCKING
  HARDENING) was subsequently REJECTED by Independent External Review — MATERIAL CORRECTION REQUIRED, blocking finding
  CONTAINMENT-LOSS TIE FLIPS**: whole-token matching drops same-domain containment reinforcement, so `an implantable sensor` (parent
  medical_device) flipped to `SINGLE(electronics_electrical)` (medical loses `implant`⊂`implantable`, ties electronics, activated
  precedence flips it; untruthful CLI electronics inference downstream); likewise `an application with a sensor` (software →
  electronics via `app`⊂`application`). `a29789a9` is immutable rejected evidence (NOT published/merged/reused). **The contract-level
  gap is corrected by a governance-only CONTRACT AMENDMENT 01 CANDIDATE** (record:
  `docs/governance/CF5_F003_CLASSIFIER_MATCHING_SEMANTICS_CORRECTIVE_CONTRACT_AMENDMENT_01.md`), built fresh from `cfdc58cc` (rejected
  `a29789a9` NOT an ancestor). Complete containment inventory: 5 pairs — SAME-domain `implant`⊂`implantable`(med) +
  `app`⊂`application`(soft) [regressions → preserve], `monitoring`⊂`patient_monitoring` [neutral]; CROSS-domain `sensor`⊂`biosensor`
  [improvement, do NOT restore], `neural`⊂`neural network` [neutral]. **Amended semantics — Design A (bounded same-domain
  registered-signal containment preservation, AT-MOST-ONCE, PLURAL-CONTAINER AWARE):** retain whole-token + `+s`/`+es` PLUS — when a
  registered container `Y` of domain D is present via ANY authorized base form (exact `Y` / `Y+"s"` / `Y+"es"`, or a multi-word `Y`'s
  token sequence) — credit same-domain single-word signals contained in `Y`, scored as a **set union (each signal counted at most
  once — a signal already matched as a standalone base token is NOT credited again)**; verified to restore `implantable sensor` →
  medical and `application`+sensor → software AND their plural-container forms (`applications with a sensor` → software; `implantables
  in a sensor` → medical) without restoring arbitrary substrings (controlled/knowledge/ecosystem stay false) or cross-domain leakage
  (`biosensor`/`biosensors` stay medical), and without inflating a parent tie (`an implant that is implantable in a sensor circuit`
  stays electronics — medical scores 2 not 3). P9-E2 tie policy / fallback / semantics UNCHANGED; no Domain-Pack edit; **no Owner
  product-policy decision required (ODR UNCHANGED)**.
  **Containment-credit invariant (M2 — narrow, replaces a withdrawn over-broad claim):** the containment contribution of a signal is
  set-based/at-most-once, cannot duplicate a base contribution, cannot be cross-domain, cannot arise from a non-registered container,
  and cannot exceed the single boolean contribution the same signal could have supplied via parent substring matching. The earlier
  global claim "a domain's score never exceeds parent on any input" is **FALSE and WITHDRAWN** — authorized phrase/tokenization
  recognition legitimately produces new matches, so the complete classifier score may exceed parent; only the containment
  contribution is bounded. TWO earlier amendment drafts were REJECTED: `0f48df20` (unqualified increment → A3-OVER-CREDIT /
  CONTAINMENT DOUBLE-COUNT) and `5ebc927d` (EXACT-token-only container trigger → **M1 plural-container containment loss**
  `applications with a sensor` → electronics; and **M2 over-broad global invariant**) — both immutable rejected evidence, neither an
  ancestor. The underscore-signal reviewer observation (`clinical_trial`/`patient_monitoring` "unmatchable") was mechanically
  **DISPROVED** (same `[a-z0-9]+` tokenizer applies to signal and input → matched); contract NOT modified to accommodate it.
  Strengthened evidence required of the future implementation: singular- AND plural-container GREEN cases + at-most-once parity cases
  (singular and plural); original REDs preserved; genuinely executed 0/1/2/3+ activation coverage (the rejected impl overstated it) +
  Web session cleanup; containment mutation probes incl. non-idempotent double-count AND exact-token-only container match
  (plural-container loss). **CF5-F003 = VALIDATED D / OPEN; impl `a29789a9` REJECTED; amendment drafts `0f48df20` and `5ebc927d`
  REJECTED; CF5-F001 / CF5-F002 / CF5-F004 remain UNCHANGED open C; CF-5 remains OPEN; NO domain activated/selected; first new-domain
  activation remains BLOCKED.** **`OWNER_DECISION_REGISTER.md` UNCHANGED; ZERO runtime/test/domain/schema/web/CLI/guardrail diff in
  this amendment gate; `activated_domains() == ['electronics_electrical']`.** **Amendment 01 = AMENDMENT CANDIDATE ONLY;
  implementation NOT started.** This exact candidate has passed the Creator Mandatory Grill; the next required gate is **independent
  external exact-candidate review of this exact immutable CF5-F003 amendment candidate**.
  **CF5-F003 Amendment 01 is now AUTHORITATIVE (merged PR #449; live tip `107d2eb08e9cdf14dade12a46693cf5dd2dd1533`; two-parent merge
  of `cfdc58cc` + Amendment 01 candidate `c26f676c`; merge tree `fcc00cd5` == candidate tree; 0 newer). A bounded CF5-F003
  IMPLEMENTATION CANDIDATE now implements the base corrective contract v2 + Amendment 01 in `engine/domain_rules.py::classify_domain`:
  raw-substring scoring is replaced by deterministic whole-token matching over `[a-z0-9]+` tokens (exact / bounded `+s` / `+es`),
  contiguous multi-word phrase matching (bounded plural on the final token only), and same-domain registered containment preservation
  credited AT-MOST-ONCE / set-membership, fired when the container is present via ANY authorized base form (incl. its bounded plural —
  plural-container aware), never cross-domain and never inside a non-registered word (`_TOKEN_RE` + `_single_word_matches` /
  `_phrase_matches` / `_present_signal_count`; `import re`). Tie policy / fallback / `DomainClassification` semantics / fail-loud
  `infer_domain` / D3-D UNCHANGED. RED→GREEN: NEW `tests/test_cf5_f003_classifier_matching_semantics.py` (74 tests) — 8 RED (false
  positives controlled/compiled/knowledge→led, patriotic→iot, concurrent→current, hearth→heart; real Web `/start` bypass; real CLI
  incorrect-confirmation) fail on pre-fix `107d2eb`, pass after; GREEN preservation (singular+plural, multi-word/punctuation,
  containment singular + plural-container, cross-domain non-leakage biosensor/biosensors→medical, at-most-once parity singular+plural,
  genuinely executed 0/1/2/3+ activation + Web session cleanup, Web/CLI parity). Full suite: **2381 passed / 3 skipped / 1 xfailed /
  0 failed** (2307 baseline + 74 new; no regression). Mutation suite (8, all CAUGHT RED, bytecode-isolated, bytes restored):
  substring-restore / `+s` removal / `+es` removal / punctuation regression / containment removal / cross-domain+non-registered
  containment leak / non-idempotent double-count / exact-token-only container (plural-container M1). Adversarial differential sweep:
  281-input corpus, 20 categorized deltas, **0 UNEXPLAINED**. Scope = `engine/domain_rules.py` (matching/scoring) + the new focused
  test + this current-truth sync; ZERO diff to web/CLI/safety-signal/activation/registry/Domain-Pack/schemas/persistence/API/
  guardrails/`OWNER_DECISION_REGISTER.md`. `activated_domains() == ['electronics_electrical']`; no activation change.
  **IMPLEMENTATION CANDIDATE ONLY — CF5-F003 NOT closed** (closure is a later gate after independent review → Owner acceptance →
  merge → post-merge verification). CF5-F001 / CF5-F002 / CF5-F004 remain UNCHANGED open C; CF-5 remains OPEN; first new-domain
  activation remains BLOCKED. Next required gate: **Mandatory Grill of this exact implementation candidate.**
  **CF5-F003 is now FORMALLY CLOSED.** The implementation is AUTHORITATIVE via **PR #450 → tip
  `0563843445c55ab1d3b5dcf2bd1e995d131b419f`** (two-parent create-a-merge-commit of `107d2eb` + exact Grill-passed implementation
  candidate `6cd1fbbf532a57c4b7fa40ea7732d85ea3469273`; **authoritative tree `5d3f0a40bf422f570848e050e1664a4d8616b14e` ==
  implementation-candidate tree** — post-merge content byte-identical; 0 newer). The VALIDATED **D** defect (raw-substring classifier
  false positives) is corrected in the authoritative runtime (whole-token `[a-z0-9]+` exact/`+s`/`+es`; contiguous multi-word;
  at-most-once plural-container-aware same-domain containment; no cross-domain leakage). Closure evidence: full suite **2381 passed /
  3 skipped / 1 xfailed / 0 failed**; 8 RED→GREEN; 8 mutation probes caught; differential sweep 281 inputs / 0 unexplained; Mandatory
  Grill PASS; Independent External Review ACCEPT WITH NON-BLOCKING OBSERVATIONS; Owner acceptance; SHA-preserving publication; PR #450;
  post-merge verification PASS. `activated_domains() == ['electronics_electrical']`; P9-E2 tie/fallback + `DomainClassification`
  unchanged. **Non-blocking carry-forward (registered once in ACTIVE_EXECUTION_ROADMAP; NOT F003 obligations):** (NMF-1) phrase-
  contiguity mutation-coverage gap (runtime CORRECT — `delivery drug`→NONE, `machines learning`→NONE; committed mutation suite lacks
  reorder/intermediate-plural negatives) → bounded TEST-HARDENING follow-up; (stale `SUBSTRINGS` comment in
  `web/app.py::_admit_specialist_domain`, Web runtime zero-diff) → bounded DOCUMENTATION/COMMENT-HYGIENE follow-up in the CF5-F002 /
  CF-6 Web-admission lane; the `iot_electronics` schema/load warning is UNRELATED and keeps its existing owner. Rejected evidence
  preserved immutable: `a29789a9` (impl — containment-loss tie flips), `0f48df20` (amendment — double-count), `5ebc927d` (amendment —
  plural-container gap + over-broad invariant). **CF5-F001 / CF5-F002 / CF5-F004 remain OPEN C; CF-5 remains OPEN (F003 closure does
  NOT close CF-5); first new-domain activation remains BLOCKED.** This closure gate is governance-only: ZERO runtime / test / domain /
  Web / CLI / `OWNER_DECISION_REGISTER.md` diff.
  **CF5-F002 is now INDEPENDENTLY VALIDATED by a governance-only VALIDATION CANDIDATE** (record:
  `docs/governance/CF5_F002_WEB_START_ADMISSION_INDEPENDENT_VALIDATION_RECORD.md`; parent `e5f7d42c5a2c7ff6590816a87cd9f5ca3f650da0`,
  PR #451; audit-contract §7 — validation separated from remediation; VALIDATION ONLY, remediation NOT authorized). Validated defect:
  the Web `/start` admission surface hardcodes a single-activated-domain (electronics-only) admission architecture (constant consent /
  admitted domain `DOMAIN_CONFIRM_VALUE`; hardcoded `domain != "electronics_electrical"` branch + static conflict set; static
  strong-unsupported vocabulary; "electronics only" public copy). **Classification C RETAINED ON EVIDENCE**: real production `/start`
  probes (isolated DB, self-restoring activation doubles, session cleanup PASS) show every currently-reachable outcome correct and
  truthful under `['electronics_electrical']`, while an elec+mech activation double mechanically demonstrates the post-trigger defect —
  activation state has zero effect on admission outcomes; activated-domain signals refused as "unsupported"; a
  SINGLE(mechanical)-classified idea ADMITTED as an `electronics_electrical` session (cross-domain mislabeling); no consent path for
  any second domain. Trigger (narrowed): the first moment `activated_domains() != ['electronics_electrical']` (extensionally =
  second-specialist-domain activation today); NOT registration, NOT recognition. CF-6 partly owns the pre-classifier facets (single
  "CF5-F002 / CF-6 Web-admission lane" validated; no duplicate framework); CF-2 separate, co-triggered, no message defect reachable
  today. Stale `SUBSTRINGS` comment (`web/app.py:870-884`): partly stale, comment-only, zero runtime consequence, F002/CF-6 lane owner
  CONFIRMED, NOT edited. **Remediation required NOW: NO; a binding pre-trigger CF5-F002 / CF-6 Web-admission corrective gate is
  REQUIRED before any activation gate changes the activation set; Owner multi-domain consent/admission UX policy is required at that
  future gate (none now).** CF5-F003 remains CLOSED; CF5-F001 / CF5-F004 remain OPEN C; CF-5 remains OPEN; first new-domain activation
  remains BLOCKED; `OWNER_DECISION_REGISTER.md` UNCHANGED; ZERO runtime/test/Web/CLI/domain/activation diff this gate. Next required
  gate: **Mandatory Grill on this exact validation candidate**.
  **CF5-F002 / CF-6 corrective implementation contract is now DEFINED (governance-only candidate) and Owner decisions D1/D2 are
  recorded** (`OWNER_DECISION_REGISTER.md` **D-CF5-F002-01**; record `docs/governance/CF5_F002_CF6_WEB_ADMISSION_CORRECTIVE_CONTRACT.md`)
  on base `8d8dc1541568b7debedb51e094b15004964c333f` (PR #452; 0 newer). CF5-F002 = VALIDATED **C** (present defect NONE; exact
  trigger `activated_domains() != ['electronics_electrical']`). **D1** = confirm classifier-selected activated domain (no auto-admit;
  persist classified+confirmed); **D2** = `NONE` under >1 activated domain → explicit user choice among activated domains (no silent
  fallback), `['electronics_electrical']` backward-compat preserved; **D3** = Electronics-absent derives from the activation set (no
  special case, no HTTP 500). The contract fences the later implementation to `web/app.py` (`/start` admission) + a focused test,
  defines the RED→GREEN matrix (A backward-compat; B elec+one-additional; C non-electronics-only; D 3+; E truthful messaging; F
  session-domain integrity; G UI-language independence), dispositions the CF-6 shared-surface facets (CF-6 NOT auto-closed) and the
  co-triggered CF-2 messaging facet (CF-2 NOT closed), includes bounded stale-comment hygiene, 10 mutation probes, and a
  0-unexplained-delta differential sweep. Forbidden: classifier/activation-policy/Domain-Pack change, domain activation, D4, D8, broad
  engine/CLI/UI work. This is a bounded portion of the Pre-Phase-9 Core Domain-Neutrality gate **D-GMPR-01-D-D3** (Web-admission
  literals only; safety_signal=CF5-F001, tie-break=CF5-F004 not discharged). **CORRECTIVE CONTRACT CANDIDATE ONLY — CF5-F002 / CF-6 /
  CF-2 / CF-5 NOT closed; no domain activated; `activated_domains() == ['electronics_electrical']`; first new-domain activation
  remains BLOCKED.** The only production-relevant record this gate is the D1/D2 ODR entry; ZERO runtime/test/Web/CLI/domain/activation
  diff. Next required gate: **Mandatory Grill on this exact corrective-contract candidate**; then, once authoritative, the bounded
  CF5-F002/CF-6 implementation.
  **CF5-F002 / CF-6 corrective contract is now AMENDED (Amendment 01, §14).** The implementation gate correctly STOPPED (§2): the
  `web/app.py`-only allowlist cannot implement a user-complete D1/D2 flow (`web/templates/index.html:26` hardcodes `domain_confirm
  value="electronics_electrical"` — the sole consent control; no D2 chooser exists). Amendment 01 widens the production allowlist to
  the minimum mechanically required — `web/app.py` (+ bounded two-step `/start` seam if needed) + `web/templates/index.html` (dynamic
  consent control) + one bounded D2 domain-choice template ONLY IF evidence requires + focused tests — and extends the acceptance
  matrix with real rendered-UI GREEN (U1 present classifier-selected activated domain; U2 NONE + ≥2 activated → present only activated
  domains for explicit choice+confirm; U3 ratified NONE + exactly-one activated → explicit confirmation; U4 rendered backward-compat;
  U5 UI-language independence) + mutation probes m11/m12. **D1/D2 and the ratified single-domain NONE case are PRESERVED EXACTLY**
  (policy unchanged; only implementation scope + acceptance evidence widened). Still forbidden: classifier/activation-policy/set
  change, domain activation, Domain-Pack change, D4, D8, broad engine/CLI/unrelated-UI work, schema/persistence change,
  implementation-gate ODR change. `OWNER_DECISION_REGISTER.md` UNCHANGED. **AMENDMENT CANDIDATE ONLY — CF5-F002 / CF-6 / CF-2 / CF-5
  NOT closed; no domain activated; `activated_domains() == ['electronics_electrical']`; first new-domain activation remains BLOCKED.**
  ZERO runtime/test/Web/CLI/domain/activation/ODR diff this gate. Next required gate: **Mandatory Grill of this amendment candidate**;
  then, once authoritative, the CF5-F002/CF-6 implementation re-runs against the amended §14.1 allowlist + §4/§14.2 matrix.
  **CF5-F002 / CF-6 bounded corrective implementation CANDIDATE now exists** (fresh from authoritative parent `2861f548`, amended
  allowlist §14.1): `web/app.py` `/start` derives admission from the canonical activation set + classifier (D1 present-for-confirm;
  D2 explicit activated-domain choice on NONE + ≥2 activated; D3 no Electronics special case / no 500; activation-aware
  strong-unsupported vocabulary; truthful activation-derived copy; §7 comment hygiene); `web/templates/index.html` generalizes the
  consent control and carries the bounded D2 chooser (no separate template — minimum-path); NEW
  `tests/test_cf5_f002_web_admission_multidomain.py` (34 tests) + bounded fail-closed-assertion adjustments to three existing tie
  tests. Evidence: RED r1–r6 on the parent; GREEN 34/34; mutations 13/13 CAUGHT (m1–m12 + m11b), bytes restored; differential sweep
  396 cases / 0 unexplained (all 66 electronics-only cases unchanged); full suite 2415 passed / 3 skipped / 1 xfailed / 0 failed;
  ODR/engine/schema/dependency diff ZERO. **IMPLEMENTATION CANDIDATE ONLY — Mandatory Grill → independent external exact-candidate
  review → Owner acceptance → SHA-preserving publication → PR → pre/post-merge verification still required; CF5-F002 / CF-6 / CF-2 /
  CF-5 NOT closed; `activated_domains() == ['electronics_electrical']`; NO domain activated; first new-domain activation remains
  BLOCKED.**
  **CF5-F002 implementation MERGED and post-merge verified; FORMAL CLOSURE CANDIDATE recorded.** PR #455 → tip `9683f64b`
  (SHA-preserving merge of the Grill-passed, independently-reviewed, Owner-accepted exact candidate `34103a26`; merge tree ==
  candidate tree; post-merge suite 2415/3/1/0; boot OK). All contract §11 criteria verified → **CF5-F002 = FORMALLY CLOSED over
  the authoritative runtime** (authoritative if/when the closure candidate is merged and post-merge verified). CF-6 facets
  (i)–(iv) discharged; remaining CF-6 (Web/CLI pre-classifier consistency beyond `/start`; legacy ILT-002 fixed-domain routes)
  and CF-2 (non-`/start` public copy; generalized-copy localization) remain OPEN and separately gated; CF-5 remains OPEN.
  Follow-ups registered once: FU-1 empty-activation defensive test (CF-5 lane); FU-2 non-electronics label quality/localization
  (CF-2/Arabic lane). `activated_domains() == ['electronics_electrical']`; NO domain activated; first new-domain activation
  remains BLOCKED behind the remaining pre-trigger prerequisites (CF5-F001, CF5-F004, remaining CF-6, CF-2, CF-3, per-domain
  P9-QS, D8 if IoT, explicit Owner activation authorization).
  **CF5-F001 INDEPENDENTLY VALIDATED (record candidate).** Independent validation (separate session) returned **ACCEPT WITH
  NON-BLOCKING OBSERVATIONS** (NB-R1 electronics-only live-vs-cold-load detection divergence via the `engine/safety_signal.py:272`
  missing-domain fallback — preserved as a mandatory corrective-contract disposition item; NB-R2 equivalent-trigger binding;
  NB-R3 cues legitimately electronics-owned, defect = placement/exposure/no seam; NB-R4 legacy electronics cold-load after
  hypothetical electronics deactivation). **CF5-F001 = OPEN C — INDEPENDENTLY VALIDATED**; no presently reachable
  non-electronics manifestation; multi-domain defect latent Class C; remediation NOT required now; the bounded pre-trigger
  corrective prerequisite remains unless explicitly re-dispositioned by a governed, recorded Owner decision (which cannot
  silently waive the activation blocker or CF-5 completion). Binding trigger: before the first point a non-electronics-domain
  session can be produced by a production surface and reach the safety-signal derivation (activation-set broadening = current
  enabler; import/write/migration/continuation/reconstruction = equivalent future enablers; registration alone and empty
  activation are NOT triggers). Architecture selection OPEN (frozen only in the corrective-contract gate). FU-1 remains a
  separate CF-5-lane follow-up. Canonical record: `CF5_F001_SAFETY_SIGNAL_INDEPENDENT_VALIDATION_RECORD.md`. Next gate:
  Mandatory Grill on that exact candidate; then the bounded CF5-F001 corrective contract (separately governed).
  **CF5-F001 validation record MERGED (PR #457, tip `17ff20cd`); CORRECTIVE CONTRACT CANDIDATE recorded.** Direction
  **PARAMETERIZE** (evidence-settled, D3-B pattern; electronics cues byte-preserved; domain-identity keying = NB-R4
  disposition; no new Owner decision; family-before-activation preserved as an open P9-QS input). **NB-R1 mechanically
  located and dispositioned**: `web/app.py::_cold_load_entry` → `record_contract.to_state()` restores no domain; the
  contract mandates restoring `domain`/`domain_signal` from the already-persisted `confirmed_domain` (legacy/NULL envelopes
  fail-safe; no schema/migration). Allowlist: `engine/safety_signal.py` seam + bounded `_cold_load_entry` + bounded `_s15`
  truthful capability-scope statement + focused tests. Required evidence: electronics live differential parity (zero
  deltas), NB-R1 elimination, family-less-domain truthful behavior, RED r1–r4, mutations m1–m6, differentials d1–d3 (0
  unexplained), full suite. **CONTRACT CANDIDATE ONLY — CF5-F001 = OPEN C — INDEPENDENTLY VALIDATED; implementation NOT
  authorized; ODR unchanged; first new-domain activation remains BLOCKED.** Canonical record:
  `CF5_F001_SAFETY_SIGNAL_CORRECTIVE_CONTRACT.md`. Next gate: Mandatory Grill on that exact contract candidate.
  **CF5-F001 contract MERGED (PR #458, tip `b06ae404`); BOUNDED IMPLEMENTATION CANDIDATE recorded.** Domain-keyed
  cue/context-family seam implemented (electronics byte-preserved; domain-identity keying; capability query); truthful
  capability-scope statement for family-less domains (electronics output unchanged); NB-R1 cold-load restoration from
  persisted `confirmed_domain` — **restored on `domain_signal` ONLY (disclosed mechanically-forced §4 narrowing:
  `state.domain` is the committed P4-1b-2a non-resume guard anchor; restoring it re-enabled resume-answering)**; one
  load-bearing-proved D3-A pin reconciliation. Evidence: RED r1–r4; GREEN 13/13; mutations 7/7 CAUGHT; differentials d1=0
  deltas / d2 NB-R1-only / d3 45/45 family-seam, 0 unexplained; full suite 2428/3/1/0. IMPLEMENTATION CANDIDATE ONLY —
  Grill → independent review (attention: §4 narrowing + D3-A reconciliation) → Owner acceptance → publication → PR →
  verification still required; CF5-F001 NOT closed; first new-domain activation remains BLOCKED.
  **CF5-F001 implementation MERGED and post-merge verified; FORMAL CLOSURE CANDIDATE recorded.** PR #459 → tip `9af877c4`
  (SHA-preserving merge of the Grill-passed, independently-reviewed, Owner-accepted exact candidate `d5edd1a3`; merge tree
  == candidate tree; post-merge suite 2428/3/1/0; boot OK). All contract §9 criteria verified → **CF5-F001 = FORMALLY
  CLOSED over the authoritative runtime** (authoritative if/when the closure candidate is merged and post-merge verified).
  NB-R1 eliminated via the accepted `domain_signal`-only narrowing (P4 non-resume preserved, pinned both directions);
  NB-R2/R3/R4 dispositioned; D-GMPR-01-D-D3 `safety_signal` coupling DISCHARGED; observations memorialized without new
  obligations; FU-1 unchanged (CF-5 lane). **CF5-F004 / CF-5 / CF-6 / CF-2 / CF-3 remain OPEN; `activated_domains() ==
  ['electronics_electrical']`; NO domain activated; first new-domain activation remains BLOCKED** behind CF5-F004,
  remaining CF-6, CF-2, CF-3, per-domain P9-QS, D8 (if IoT), and explicit Owner activation authorization.
  **CF5-F001 closure MERGED (PR #460, tip `e39f667a`) → CF5-F001 = FORMALLY CLOSED. CF5-F004 INDEPENDENTLY VALIDATED
  (record candidate).** Verdict ACCEPT WITH NON-BLOCKING OBSERVATIONS. **CF5-F004 = OPEN C — INDEPENDENTLY VALIDATED**: the
  un-owned non-activated priority fallback literal (`classify_domain` Case 0); failure arms = omitted-pack sole-top →
  silent NONE, omitted-pack tie → silent legacy-member award; dangerous chain = omitted pack → NONE → sole-electronics
  `/start` consent → possible electronics-labeled session; not reachable today (registry == literal). **Trigger = first
  successful recognized-registry-set change — registration IS the trigger; activation is NOT and is too late.** F004/CF-3
  distinct, both discharge only at F004 formal closure; architecture OPEN; remediation trigger-bound; Owner questions
  (schema-work binding; precedence preserve-vs-replace; CF-3 timing) preserved for the contract gate. Canonical record:
  `CF5_F004_PRIORITY_FALLBACK_INDEPENDENT_VALIDATION_RECORD.md`. Next gate: Mandatory Grill on that exact candidate.
  **CF5-F004 validation record MERGED (PR #461, tip `5dc50557`); CORRECTIVE CONTRACT CANDIDATE + D-CF5-F004-01
  recorded.** Owner decisions: OD1 remediation binds before any registry-set-changing pack-schema/provenance WORK; OD2
  legacy 4-domain precedence preserved (differential lock) + no invented winner / no silent erasure for future domains;
  OD3 CF-3 + D-GMPR-01-D-D3 discharge only at F004 formal closure. Architecture selected: registry-derived membership +
  bounded legacy-compatibility layer + arm-A SINGLE(sole top) + arm-B NEW fail-closed `UNRESOLVED_NON_ACTIVATED_TIE`
  (AMBIGUOUS_TIE untouched) + bounded `/start`/CLI fail-closed dispatch; `infer_domain` unchanged-and-pinned. Evidence
  contract: RED R1–R7, GREEN + determinism probe, mutations m1–m6, d1 ZERO deltas / d2 categorized, full suite. CONTRACT
  CANDIDATE ONLY — implementation NOT authorized; CF5-F004/CF-3 NOT closed; first new-domain activation remains BLOCKED.
  Canonical record: `CF5_F004_PRIORITY_FALLBACK_CORRECTIVE_CONTRACT.md`. Next gate: Mandatory Grill on that exact
  candidate.
  **CF5-F004 contract MERGED (PR #462, tip `0e4312e5`); BOUNDED IMPLEMENTATION CANDIDATE recorded.** Registry-derived
  zero-activated membership + bounded legacy-four compatibility layer (OD2); arm-A truthful SINGLE(sole top); arm-B NEW
  `UNRESOLVED_NON_ACTIVATED_TIE` (complete set; no winner; AMBIGUOUS_TIE untouched); bounded `/start`/CLI fail-closed
  dispatch; `infer_domain` unchanged-and-pinned; MULTI_DOMAIN_NEEDS_D4 non-reuse recorded. Evidence: RED R1/R2/R7/R8 +
  pins R3–R6; GREEN 14/14 (determinism probe; vocabulary-clean Web dispatch test — M5 masking caught in-gate and
  corrected, disclosed); mutations 7/7 CAUGHT; D1 ZERO deltas / D2 categorized (3 arm-A + 4 arm-B, 0 unexplained); full
  suite 2442/3/1/0; ZERO ODR diff. IMPLEMENTATION CANDIDATE ONLY — Grill → independent review → Owner acceptance →
  publication → PR → verification still required; CF5-F004 / CF-3 NOT closed (OD3); first new-domain activation remains
  BLOCKED (OD1 binds earlier).
  **CF5-F004 implementation MERGED and post-merge verified; FORMAL CLOSURE CANDIDATE recorded.** PR #463 → tip
  `80e5d78d` (SHA-preserving merge of accepted candidate `3f5f54f8`; merge tree == candidate tree; post-merge re-verified
  this gate: suite 2442/3/1/0, focused 14/14, boot OK). **CF5-F004 = FORMALLY CLOSED over the authoritative runtime;
  CF-3 = DISCHARGED/RESOLVED; D-GMPR-01-D-D3 hard-coded tie-break coupling = DISCHARGED** (per OD3; each conditional on
  the closure candidate's own merge + verification; the `path_n_questions.py` D-GMPR coupling remains OPEN).
  **Retrospective RED-narrative correction (non-destructive):** frozen focused file = 9 failed / 5 passed on the clean
  parent (mechanically re-verified); earlier 8/6 narrative measured the pre-M5-strengthening file; no change to
  implementation correctness, candidate identity, or the ACCEPT verdict. **No over-closure: CF-5 / CF-6 / CF-2 remain
  OPEN; closing F004/CF-3 authorizes NO registration/activation; first new-domain activation remains BLOCKED; D4/D8/
  Phase 10/PSRR/deployment unchanged.**
  **CF5-F004 closure MERGED (PR #464, tip `fcc9e37e`) → CF5-F004 = FORMALLY CLOSED; CF-3 = DISCHARGED (F004 surface
  only); D-GMPR tie-break coupling = DISCHARGED. CF-5 UMBRELLA FORMAL CLOSURE CANDIDATE recorded.** Finding matrix
  terminal (F001/F002/F004 FORMALLY CLOSED; F003 CLOSED; no E findings); audit §9 criteria verified with the honestly
  recorded summary-level-run-record limitation (reliance flagged for the independent reviewer); fresh verification: boot
  OK, activation unchanged, suite 2442/3/1/0. **Disposition: `CF-5 = FORMALLY CLOSED` — authoritative ONLY after the
  closure candidate's own merge + post-merge verification.** Surviving carry-forwards preserved: CF-6 remainder OPEN;
  CF-2 OPEN; `path_n_questions` D-GMPR coupling OPEN; NMF-1 + FU-1 re-homed as pre-activation test-hardening; P9-QS
  separate; D4/D8/Phase 10/PSRR/deployment unchanged; **CF-5 closure authorizes NO domain registration/activation —
  first new-domain activation remains BLOCKED.** Canonical record:
  `CF5_RETROSPECTIVE_ADVERSARIAL_ARCHITECTURE_AUDIT_FORMAL_CLOSURE_RECORD.md`. Next gate: Mandatory Grill on that exact
  candidate.
  **CF-5 closure MERGED (PR #465, tip `bb7e73264d484561c8e1b3f264d2eceefc0cf394`; merge tree == closure-candidate tree)
  → `CF-5 = FORMALLY CLOSED` is AUTHORITATIVE. D-GMPR-01-D-D4 — Amendment 01 CANDIDATE recorded (bounded
  governance-only scope-meaning clarification; NOT a new gate; NON-ACTIVATING).** Canonical substance:
  `OWNER_DECISION_REGISTER.md` "Substance (D-GMPR-01-D-D4 — Amendment 01)" block + row pointer (same decision identity;
  no new owner/document/workstream — anti-duplication per D-FPC-MAP-06, following a read-only discovery verdict
  `ALREADY RECORDED — PARTIALLY COVERED`). It clarifies that D4's registered shared-constraint propagation / conflicts /
  unified assessment includes governed **system-level engineering compatibility across participating domains** (mutual
  compatibility as ONE product/system, not mere multi-domain presence detection); that **per-domain PASS ≠ system-level
  PASS** (future D4 surfaces incompatibilities, unresolved interface assumptions, contradictions, unowned/orphan
  requirements, and explicit Known Unknowns); Owner examples ILLUSTRATIVE ONLY / NON-BINDING; **no defect-free-product
  guarantee** (truthful Known-Unknowns route to WS-PFV-001-lineage physical/specialist validation); five-way distinction
  preserved (recognition ≠ qualification ≠ activation ≠ cross-domain evaluation ≠ physical validation); future-domain
  extensibility without hardcoded composition authority; **no implementation architecture / pipeline committed**.
  **Non-effects:** D4 stays REGISTERED (future gate) / NOT AUTHORIZED with unchanged sequencing (≥2 activated domains);
  NO domain registration/activation; NOT a prerequisite expansion (adds no blocker to and does not delay the Phase-9
  next-domain decision or Mechanical P9-QS); CF-6 / CF-2 / `path_n_questions` coupling / NMF-1 / FU-1 unchanged;
  `activated_domains() == ['electronics_electrical']`; first new-domain activation remains BLOCKED. **The next Owner
  gate is unchanged: the Phase-9 next-domain selection decision.** Authoritative ONLY if/when this exact candidate is
  merged + post-merge verified. Next required gate: Mandatory Grill on this exact candidate.
  **D4 Amendment 01 MERGED (PR #466, tip `c4abe0207c34f15e89438cc931c114db9d2e6225`; merge tree == candidate tree) →
  Amendment 01 AUTHORITATIVE; D4 remains REGISTERED / NOT AUTHORIZED. P9-MECH-QC CANDIDATE recorded: Owner selection
  `D-P9-MECH-01` (`mechanical` = next Phase-9 P9-QS qualification target) + the Mechanical P9-QS Qualification
  Contract** (canonical record: `P9_MECHANICAL_DOMAIN_QUALIFICATION_CONTRACT.md`; selection recorded inside the
  contract gate — no standalone selection gate). **Selection ≠ qualification ≠ activation; registry UNCHANGED;
  Mechanical NOT qualified, NOT activated.** Verified qualification gaps the contract binds: degenerate rule nuances;
  missing coverage declaration; substance depth 17 vs electronics 53; no safety-cue family; no Tier-1 public label;
  pack-question sufficiency unproven; dormant classifier `weight` metadata requiring truthfulness disposition (the
  advisory "electronics-specific plural alias in shared core" claim NOT verified — the F003 matcher is domain-generic).
  **OPEN Owner decision OD-M2: Mechanical safety-cue-family timing (before qualification vs before activation vs other
  governed treatment) — surfaced, not decided; qualification cannot be declared until decided.** Boundaries preserved:
  CF-6 OPEN; CF-2 OPEN; D-GMPR `path_n_questions` coupling OPEN (pack-content sufficiency is in-contract; seam
  remediation stays in the D-GMPR lane); NMF-1/FU-1 unchanged; D4/D8/Phase 10/PSRR/deployment unchanged;
  qualification-extensibility claim ONLY (no registration-extensibility / fifth-domain / universal-scalability claim);
  `activated_domains() == ['electronics_electrical']`; first new-domain activation remains BLOCKED. The contract does
  not authorize its own implementation — every future increment needs separate explicit Owner authorization.
  Authoritative ONLY if/when this exact candidate is merged + post-merge verified. Next required gate: Mandatory Grill
  on this exact candidate.
  Phase-7 §25 deferred security/ops items (Monitoring; broad Abuse Controls; `access_audit` retention; production secrets
  operations) remain NOT delivered / NOT solved — PSRR may reassess, not auto-implement. Phases 8/9/10, deployment, and
  separately governed capabilities remain NOT AUTHORIZED. (The now-superseded §5-open wording below is retained as history.) **Product-Foundation
  §5 as a whole is NOT complete** — §5-I1, §5-I2, and §5-I3 are closed. Next-eligible gate: **§5-CLOSE (§5 formal closure +
  GAP-1…GAP-4 governance reconciliation)** under continuing owner authorization — **NOT STARTED**; Phase 7 NOT AUTHORIZED.

## PHASE 6 — P6-1 TRUTHFUL DOMAIN LABELING FOUNDATION: FORMALLY ACCEPTED AND CLOSED (implemented / independently reviewed B / merged PR #385 / post-merge verified / governance-sync merged PR #386 / owner-accepted) — increment record within the now-CLOSED executed Phase-6 lane (see the closure banner above)

- **P6-1 — Truthful Domain Labeling Foundation (Option A):** **IMPLEMENTED / INDEPENDENTLY REVIEWED / MERGED / POST-MERGE
  VERIFIED.** Lineage: implementation gate **G-P6-1-TRUTHFUL-DOMAIN-LABELING-FOUNDATION-IMPLEMENTATION-01** → candidate
  `ddaf4357e91f3c1d9443135b903871fdb3bd554a` (parent `df9e6ab`, tree `c50d791`) → independent review **B — ACCEPT WITH
  NON-BLOCKING OBSERVATIONS** (zero blockers) → merge **PR #385** (`a8b874be5c994687e02d64b6e84404b641ab501e`, tree
  `c50d791`, parents `df9e6ab` + `ddaf435`, scope **5 files / +259 / −2**, source branch
  `publish/p6-1-truthful-domain-labeling` PRESERVED). Recorded by
  **G-P6-1-TRUTHFUL-DOMAIN-LABELING-POST-MERGE-CLOSURE-SYNC-01**. Focused **23 passed**; full suite green in both
  environments (owner Codespace **1885 passed / 3 skipped / 1 xfailed** with test-only Playwright absent;
  independent-review environment **1916 passed / 1 skipped / 1 xfailed**) — the additional skips are Playwright/browser
  TEST-ENVIRONMENT dependent (documented in `tests/requirements-draft-l2.txt`), **not** a P6-1 regression.
- **P6-1 delivered (electronics-only; presentation-only):** one central server-side public-domain-label resolver
  (`web/domain_label.py::public_domain_label`, registered Jinja filter); truthful Tier-1 labeling bound to trusted
  server-resolved domain state; internal `electronics_electrical` **not** exposed as the public capability/domain label;
  approved EN and AR canonical variants; neutral **General idea review** fallback (unknown/missing/unsupported never
  silently electronics); no Tier-2/3/4 professional/specialist/certification claim; no new domain activation; no
  deterministic-engine / domain-pack change; no schema/migration; no localization framework; no global language selector.
- **Owner language decisions (RESUME-01), canonical (see `OWNER_DECISION_REGISTER.md` D-P6-16 / D-P6-17 / D-P6-18):**
  (A) **D-P6-16** — EN and AR MUST NOT render simultaneously for the same public/UI label; both remain canonical
  internally, the user sees the selected-UI-language variant; the earlier EN+AR-together rendering is **REJECTED**.
  (B) **D-P6-17** — three-layer model: **UI Language** (explicit user choice, applies across all pages, never auto-changed
  by typed content), **Input Language** (free-form AR/EN/mixed; technical English terms — ESP32, Bluetooth Low Energy,
  LiDAR, API, CAN Bus, Python — preserved; never auto-switches UI), **Output Language** (defaults to UI Language; future
  independent selection NOT authorized here). (C) **D-P6-18** — a **global UI language selector** (persistent
  shared-header control applied consistently across all pages) was recorded here (RESUME-01) as a FUTURE,
  independently-authorized requirement. **UPDATE: subsequently owner-authorized, implemented, independently reviewed
  (B — ACCEPT, zero blockers), MERGED (PR #388 `b47bf4bb57446956c47488283248cfbacd603e85`, parents `a0426cb`+`62818a8`,
  tree `f6ed63d`), and FORMALLY ACCEPTED AND CLOSED** (gate `G-DP6-18-GLOBAL-UI-LANGUAGE-FORMAL-CLOSURE-01`; dedicated
  record `docs/governance/D_P6_18_GLOBAL_UI_LANGUAGE_FORMAL_CLOSURE_RECORD.md`).
- **P6-1-era surface truth — SUPERSEDED by D-P6-18 (historical, not current):** *at P6-1 time* the `session` and
  `deliverable` shells were `<html lang="en">` (LTR) with no canonical UI-language-selection signal, so P6-1 rendered the
  **English** variant on those surfaces only and the Arabic variants were canonical but then unrendered — this was **NOT**
  global localization completion. **This is no longer current:** D-P6-18 (merge PR #388 `b47bf4b`) added the global UI
  language selector and the `ui_lang`-driven shell, so the selected UI language (including the Arabic RTL shell) now
  applies across active application UI chrome and the P6-1 labels follow it. PR #148 Arabic/RTL supportive-response
  semantics remain preserved (its three formerly-conflicting RTL tests pass with files UNCHANGED).
- **P6-1 FORMAL CLOSURE:** **DONE** — **FORMALLY ACCEPTED AND CLOSED** by owner gate
  **G-P6-1-TRUTHFUL-DOMAIN-LABELING-FORMAL-CLOSURE-01** (dedicated record
  `docs/governance/P6_1_TRUTHFUL_DOMAIN_LABELING_FORMAL_CLOSURE_RECORD.md`; append-only roadmap closure entry). *(Current
  truth — SUPERSEDED at the lane level by the closure banner above: the executed Domain Specialization / Truthful
  Specialist Labeling Phase-6 lane is now **FORMALLY ACCEPTED AND CLOSED** (**D-P6-CLOSE**); the "Phase 6 as a whole is NOT
  complete" wording below was accurate at P6-1-closure time and reflected that D-P6-18 was then still pending — it is
  retained as historical increment-record context. The Product-Foundation §5 Multi-Domain program remains DISTINCT /
  FUTURE / NOT AUTHORIZED.)* At P6-1-closure time, Phase 6 as
  a whole was **NOT** yet complete. **NEXT ELIGIBLE OWNER GATE:** read from the live `ACTIVE_EXECUTION_ROADMAP.md` — **ELIGIBLE
  FOR OWNER CONSIDERATION, NOT AUTHORIZED** (not assumed to be P6-2 from numbering). The Output-Language override
  (**D-P6-17**) and Domain Registry validation hardening (**D-P6-14**) remain SEPARATE FUTURE increments; **no** later
  Phase-6 increment is started by P6-1's closure. (The global UI language selector **D-P6-18** was subsequently authorized,
  implemented, and **FORMALLY CLOSED** — merge PR #388 `b47bf4b`; its closure authorizes no successor capability, and the
  **Question Translation Assistant remains NOT AUTHORIZED / NOT STARTED**. The next eligible governance step is the
  **Master Obligation Index** gate, which **REQUIRES SEPARATE OWNER AUTHORIZATION** — documentation reconciliation only,
  **ELIGIBLE FOR OWNER CONSIDERATION, NOT AUTHORIZED / NOT STARTED** — not the implementation of any new capability.) Multi-domain, AI/model/agent changes, new output types, schema/migration,
  registry hardening, Draft Level 3, WS17, STG, ACV, PDF/download, and output email remain **NOT AUTHORIZED / NOT
  STARTED**. Phase 5 remains FORMALLY CLOSED; P4-2 Level-1, Draft Level 2, P5-1, P5-2, P5-3 remain CLOSED. Decision
  **D17** and the AISR seven-owner model are preserved.

## PHASE 5 FORMALLY CLOSED (P5-1 → P5-2 → P5-3); PHASE 6 discovery COMPLETED and the P6-1 Truthful Domain Labeling Foundation contract DEFINED — implementation NOT YET AUTHORIZED (SUPERSEDED by the P6-1 IMPLEMENTED / MERGED current-truth section above)

- **PHASE 5 — Accounts / Authentication / Ownership / Verified Email:** **IMPLEMENTED / INDEPENDENTLY REVIEWED / MERGED /
  POST-MERGE VERIFIED / OWNER ACCEPTED / FORMALLY CLOSED** across all three increments (**P5-1 → P5-2 → P5-3**). Final
  closure recorded by **G-P5-FINAL-CLOSURE-SYNC-01** (live tip `d9f888b`, Merge PR #379).
- **P5-3 — Project Ownership & Route Authorization:** **FORMALLY CLOSED** (independent review
  **G-P5-3-PROJECT-OWNERSHIP-ROUTE-AUTHORIZATION-INDEPENDENT-REVIEW-01**, verdict **B — ACCEPT WITH NON-BLOCKING
  OBSERVATIONS**, PUBLISH). Lineage: gate **G-P5-3-PROJECT-OWNERSHIP-ROUTE-AUTHORIZATION-IMPLEMENTATION-01** → candidate
  `a0997c3` (tree `e6a03ab`, parent `b14c931`) → merge **PR #379** (`d9f888b`, tree `e6a03ab`, parents `b14c931` +
  `a0997c3`, ancestry PASS, scope **6 files / +562 / −15**, source branch `feat/p5-3-project-ownership-authorization`
  PRESERVED). Focused **19 passed**; full suite **1893 passed, 1 skipped, 1 xfailed**.
- **Phase 5 delivered:** accounts; credentials; registration; login/logout; authenticated signed-cookie sessions
  (distinct from the project `sid`); email verification; account recovery/reset; session revocation via `session_epoch`;
  additive nullable `projects.owner_account_id`; atomic verified-account owned-project creation; central server-side
  route authorization; cross-account isolation; generic non-enumerating denial; legacy/anonymous NULL-owner
  compatibility; Draft L2 account+project isolation. No new runtime dependency.
- **Phase 5 did NOT deliver (all remain NOT AUTHORIZED / NOT STARTED):** Draft Level 3; writable continuation; anonymous
  project claiming; ownership transfer / multiple owners / collaboration / sharing / teams / organizations; production
  email delivery; output email delivery; ACV; AI Coach; STG; provider selection; and later commercial-readiness
  capabilities.
- **Preserved Phase 5 observations:** **OBS-P5-3-01** (authorization's `sid in SESSION_STORE` in-memory fallback must be
  replaced with caller/session-scoped authorization before any project-deletion / broader in-memory access / session
  restoration is added); **OBS-P5-2-01** (email-link tokens in URL paths — revisit before production email/reverse-proxy);
  **OBS-P5-2-02** (make password reset a single atomic store operation when `account_store` is next touched). The P5-1
  rate-limit-concurrency and SQLite-threading preconditions were RESOLVED in P5-2. Full detail in the roadmap P5-3/Phase-5
  closure entry and `OWNER_DECISION_REGISTER.md` (`D-P5-3-*`).
- **PHASE 6 — Domain Specialization / Truthful Specialist Labeling (authoritative ACTIVE_EXECUTION_ROADMAP lane):**
  discovery **G-P6-DOMAIN-SPECIALIZATION-DISCOVERY-01** is **COMPLETED / OWNER-ACCEPTED**; owner adopted recommendations
  and decisions **D-P6-00 … D-P6-15** and selected **Option A — Truthful Domain Labeling Foundation**. The first Phase 6
  **contract-of-record P6-1** is **DEFINED** by the documentation-only gate
  **G-P6-1-TRUTHFUL-DOMAIN-LABELING-FOUNDATION-CONTRACT-01** (recorded in `ACTIVE_INCREMENT_CONTRACT.md`; owner decisions
  in `OWNER_DECISION_REGISTER.md` `D-P6-*`; append-only roadmap entry). **NO Phase 6 implementation is active.** Only
  `electronics_electrical` is runtime-operated; no new domain is activated; labels are capped at Tier 0–1 (Tier 3/4
  prohibited); no schema/engine/AI change; registry validation hardening remains a SEPARATE prerequisite increment.
  ⚠️ Two distinct "Phase 6" numberings exist (this execution lane vs a registry-parity lane in
  `docs/GOVERNANCE_DOCUMENTS.md`); per `PRODUCT_ARCHITECTURE_AND_CREDIBILITY_ROADMAP.md`, **neither authorizes the other**
  (D-P6-00).
- **NEXT ELIGIBLE GATE: G-P6-1-TRUTHFUL-DOMAIN-LABELING-FOUNDATION-IMPLEMENTATION-01** — eligible **only after the P6-1
  contract is merged and post-merge verified**. **Multi-domain, AI/model/agent changes, new domain activation, new
  output types, registry hardening, and Draft Level 3 remain NOT AUTHORIZED / NOT STARTED.** Phase 4 remains FORMALLY
  CLOSED; P4-2 Level-1, Draft Level 2, P5-1, P5-2, and P5-3 remain CLOSED. Decision **D17** and the AISR seven-owner model
  are preserved.

## HISTORICAL SNAPSHOT — P5-2 Authenticated Sessions / Verified Email / Recovery FORMALLY CLOSED; P5-3 is the next eligible implementation increment (SUPERSEDED by the PHASE-5-CLOSED current-truth section above)

- **P5-2 — Authenticated Sessions, Verified Email & Account Recovery:** **IMPLEMENTED / INDEPENDENTLY REVIEWED / MERGED /
  POST-MERGE VERIFIED / OWNER ACCEPTED / FORMALLY CLOSED** (independent review
  **G-P5-2-AUTH-SESSIONS-VERIFIED-EMAIL-RECOVERY-INDEPENDENT-REVIEW-01**, verdict **B — ACCEPT WITH NON-BLOCKING
  OBSERVATIONS**, PUBLISH). Lineage: gate **G-P5-2-AUTH-SESSIONS-VERIFIED-EMAIL-RECOVERY-IMPLEMENTATION-01** → candidate
  `87c85c7` (tree `375db689`, parent `f84c87d`) → merge **PR #377** (`402727a`, tree `375db689`, parents `f84c87d` +
  `87c85c7`, ancestry PASS, scope **13 files / +1712 / −78**, source branch
  `feat/p5-2-auth-sessions-verification-recovery` PRESERVED). The two mandatory P5-1-closure preconditions were satisfied
  first — **P5-2-PRE-01** (rate-limit concurrency: `BEGIN IMMEDIATE` proven race-free under real threads + bounded
  cleanup) and **P5-2-PRE-02** (SQLite thread strategy: `check_same_thread=False` + re-entrant lock + immediate
  transactions, proven under real multi-thread tests). Focused **40 passed**; full suite **1874 passed, 1 skipped, 1
  xfailed**.
- **P5-2 capability:** login and logout; logout-all via `session_epoch`; an authenticated signed-cookie session distinct
  from the project `sid`; two-hour idle expiry; fourteen-day absolute expiry; session rotation on login; CSRF protection
  on authenticated mutations; email-verification completion; verification resend; recovery request; password-reset
  completion; reset revokes existing sessions; disabled/deleted account denial; generic non-enumerating responses;
  hardened concurrency-safe rate limiting; SQLite thread/connection hardening; Draft Level 2 account-switch isolation;
  bilingual and accessible account UX. No new runtime dependency.
- **P5-2 does NOT provide (deferred to P5-3):** `projects.owner_account_id`; project ownership; project route
  authorization; anonymous project claim; collaboration or sharing; P5-3; Draft Level 3; writable continuation; output
  email delivery; a production email provider.
- **Preserved non-blocking observations (P5-2 not reopened):** **OBS-P5-2-01** email-link raw tokens appear in URL paths
  (mitigated: hash-only at rest, single-use, short expiry, no app logging, no third-party resources on result pages;
  revisit before a production email-provider / reverse-proxy deployment — access-log redaction, browser-history
  exposure, POST-based/interstitial alternatives where Lean); **OBS-P5-2-02** password reset uses sequential
  transactions (consume → set-password → `session_epoch` bump → supersede) — accepted resilience debt, evaluate a single
  atomic operation when `account_store` is next modified for a related security increment. Full detail in the roadmap
  P5-2 closure entry and `OWNER_DECISION_REGISTER.md` (`D-P5-2-*`).
- **NEXT ELIGIBLE INCREMENT: P5-3 — Project Ownership and Route Authorization** — authorized under the continuing Phase 5
  owner authorization **only after this closure sync is merged and post-merge verified**. **Draft Level 3: NOT
  AUTHORIZED.** Phase 4 remains **FORMALLY CLOSED**; P4-2 Level-1, Draft Level 2, P5-1, and now **P5-2** remain
  **CLOSED**. The Phase 5 formal contract remains **MERGED / VERIFIED / ACCEPTED**. Decision **D17** and the AISR
  seven-owner model are preserved.

## HISTORICAL SNAPSHOT — P5-1 Account & Credential Foundation FORMALLY CLOSED; P5-2 is the next eligible implementation increment (SUPERSEDED by the P5-2-CLOSED current-truth section above)

- **P5-1 — Account & Credential Foundation:** **IMPLEMENTED / INDEPENDENTLY REVIEWED / MERGED / POST-MERGE VERIFIED /
  OWNER ACCEPTED / FORMALLY CLOSED** (independent review **G-P5-1-ACCOUNT-CREDENTIAL-FOUNDATION-INDEPENDENT-REVIEW-01**,
  verdict **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**, PUBLISH). Lineage: gate
  **G-P5-1-ACCOUNT-CREDENTIAL-FOUNDATION-IMPLEMENTATION-01** → candidate `6be86f5` (tree `128b2d4`, parent `e84526d`)
  → merge **PR #375** (`65a2c0e`, tree `128b2d4`, parents `e84526d` + `6be86f5`, ancestry PASS, scope **7 files /
  +1024**, source branch `feat/p5-1-account-credential-foundation` PRESERVED). Focused **35 passed**; full suite
  **1834 passed, 1 skipped, 1 xfailed**.
- **P5-1 capability (foundation only):** additive accounts persistence; immutable UUID-based `account_id` (never email);
  normalized + unique email; Werkzeug scrypt password hashing; active/disabled/deleted account status; `session_epoch`
  foundation; registration route + bilingual accessible form; generic non-enumerating public response; verification-token
  hash-only persistence; 24-hour verification-token expiry; verification-token supersession; development `EmailSender`
  abstraction + memory sink; bounded store-backed rate-limit foundation; additive idempotent legacy-safe migration; no
  plaintext password storage; no raw verification-token storage or logging.
- **P5-1 does NOT provide (deferred to P5-2/P5-3):** login; logout; authenticated Flask sessions; authentication
  cookies; CSRF protection for authenticated mutations; verification completion; resend route; password recovery/reset;
  project ownership; `projects.owner_account_id`; route authorization; anonymous project claim; Draft Level 3; P5-3;
  output email delivery; production email provider. Registration does **not** sign the user in, does **not** create a
  project, and does **not** establish project ownership.
- **Mandatory P5-2 preconditions (engineering, not optional):** **P5-2-PRE-01 — rate-limit concurrency hardening**
  (eliminate the multi-connection lost-update race; atomic SQL increment or explicit immediate write transaction; prove
  the limit under genuine concurrency; keep responses non-enumerating; add bounded expired-row cleanup) and
  **P5-2-PRE-02 — SQLite thread/connection strategy** (resolve the module-cached connection + thread-affinity issue;
  define a safe per-request or bounded connection strategy; prove behaviour under a threaded WSGI environment; preserve
  transaction safety and fail-closed; do not merely set `check_same_thread=False` without proving locking/transaction
  correctness). Both must be addressed within the first P5-2 implementation candidate before login/session security is
  accepted. Other recorded non-blocking observations (expired rate-limit cleanup, sequential-vs-concurrent duplicate
  test, rate-limit generic-response test strengthening, full Set-Cookie assertion in P5-2, password-too-long message,
  keyed email digest, dev sink retention, regression-narrative naming, pinned Playwright for full-suite count) are
  captured in the roadmap P5-1 closure entry and `OWNER_DECISION_REGISTER.md`.
- **NEXT ELIGIBLE INCREMENT: P5-2 — Authenticated Sessions, Verified Email, and Recovery** — authorized under the
  continuing Phase 5 owner authorization **only after this closure sync is merged and post-merge verified**. **P5-3: NOT
  STARTED.** **Draft Level 3: NOT AUTHORIZED.** Phase 4 remains **FORMALLY CLOSED**; P4-2 Level-1, Draft Level 2, and
  now **P5-1** remain **CLOSED**. The Phase 5 formal contract remains **MERGED / VERIFIED / ACCEPTED**. Decision **D17**
  and the AISR seven-owner model are preserved.

## HISTORICAL SNAPSHOT — Draft Level 2 FORMALLY CLOSED; Phase 5 FORMALLY PLANNED (P5-1 → P5-2 → P5-3); P5-1 is the next eligible implementation gate (SUPERSEDED by the P5-1-CLOSED current-truth section above)

- **Draft Level 2 — Same-Device Unsubmitted-Text Recovery (Local Draft Recovery):** **IMPLEMENTED / REMEDIATED /
  INDEPENDENTLY REVIEWED / MERGED / POST-MERGE VERIFIED / OWNER ACCEPTED / FORMALLY CLOSED** (re-review verdict
  **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**). Lineage: discovery **G-P5-DISCOVERY-AND-DRAFT-CONTINUITY-ASSESSMENT-01**
  (overlap **D — NOT FOUND**; current level was **Draft Level 0**; **Option B**) → contract
  **G-DRAFT-L2-LOCAL-CONTINUITY-CONTRACT-01** (PR #371, merge `e84845d`) → implementation
  **G-DRAFT-L2-LOCAL-CONTINUITY-IMPLEMENTATION-01** (candidate `9138f96`, independent review **C — REJECT**, blockers
  B1/B2/B3) → remediation **G-DRAFT-L2-LOCAL-CONTINUITY-REMEDIATION-01** (candidate `4696567`, re-review **B**, PUBLISH)
  → merge **PR #372** (`43223dd`, tree `83dbf36`, ancestry PASS, scope **8 files / +981 / −6**, disallowed paths
  **NONE**). Focused **30 passed**; full suite **1799 passed, 1 skipped, 1 xfailed**. **B1/B2/B3 all FIXED.**
- **Capability (local-only):** same-device `localStorage` recovery of unfinished typed text; 7-day TTL; seed + main-answer
  + bounded criticality-correction; debounced save + pagehide/visibilitychange; explicit Restore/Discard (never silent
  overwrite); stale/expired/corrupt/mismatch rejection; truthful device-only wording; a11y + bilingual (EN/AR); no-JS
  Level-0 fallback; failed & ambiguous submission retention; matching-draft cleanup only after truthful acceptance;
  multi-tab preservation + newer-copy awareness.
- **Does NOT provide:** server-side draft persistence; account-linked/cross-device drafts; accounts; authentication;
  project ownership; authorization; collaborative editing; multi-device conflict resolution; writable continuation;
  durable version history; any `AssertionRecord`/evaluation/maturity/gap/output effect from drafts; Phase 5 capability;
  Draft Level 3. Local draft data stays semantically separate from accepted answers and durable project records. No
  engine/schema/migration/account/server-draft change; production `requirements.txt` unchanged.
- **Phase 5 — Accounts / Authentication / Project Ownership / Authorization / Verified Email:** discovery
  **G-P5-IDENTITY-OWNERSHIP-DISCOVERY-CONTRACT-01** is **COMPLETED / ACCEPTED** (verdict **B**); the owner selected
  **Identity Option A (application-managed email + password; Werkzeug scrypt; no new runtime dependency)** and structure
  **P5-1 → P5-2 → P5-3**, and granted a **continuing authorization** through formal Phase 5 closure under mandatory
  per-increment RED/GREEN + independent-review + publication + post-merge-verification controls. The **formal Phase 5
  contract-of-record** and owner decisions `D-P5-01…15` are recorded in `ACTIVE_INCREMENT_CONTRACT.md` /
  `OWNER_DECISION_REGISTER.md` (gate **G-P5-FORMAL-CONTRACT-AND-CONTINUING-AUTHORIZATION-01**); an append-only roadmap
  entry is recorded. **NO Phase 5 implementation is active.**
- **NEXT ELIGIBLE GATE: P5-1 — Account & Credential Foundation** — eligible only **after this formal contract is merged
  and post-merge verified**. **P5-2 and P5-3: NOT STARTED.** Phase 5 must not reimplement/replace Draft Level 2 (consumed,
  not replaced). **Server-side Draft Level 3, writable continuation, output email delivery, and every FPC remain NOT
  AUTHORIZED / NOT STARTED.** Phase 4 remains **FORMALLY CLOSED**; P4-2 Level-1 and Draft Level 2 remain **CLOSED**.
  Decision **D17** and the AISR seven-owner model are preserved.

## HISTORICAL SNAPSHOT — Post-PR #367 boundary — P4-1b-2b IMPLEMENTED, MERGED, VERIFIED, ACCEPTED, CLOSED (SUPERSEDED by the Post-PR #369 boundary above)

*Superseded historical snapshot — accurate as of the PR #367 boundary only; do not read as present authority. Its
"P4-2 … NOT AUTHORIZED / NOT STARTED" wording was current at PR #367. **Current truth is the "Post-PR #369 boundary"
section above: P4-2 Level-1 is IMPLEMENTED / MERGED / VERIFIED / ACCEPTED / FORMALLY CLOSED and Phase 4 is FORMALLY
CLOSED (PR #369, live tip `276e896`); Phase 5, writable continuation, and every FPC remain NOT AUTHORIZED / NOT
STARTED.***

- **Live tip:** `1c9dff7962a428cfd32ab577dbbbb84ce21909b3` (Merge PR #367; two-parent merge of `7d88951` (base) +
  `945f4a3` (candidate), tree `bff45ada`; always re-resolve from Git).
- **P4-1b-2b — Read-Only Accepted-Answer Evidence Reconstruction (OPTION A):** **IMPLEMENTED, MERGED, POST-MERGE
  VERIFIED, OWNER ACCEPTED, AND FORMALLY CLOSED** (owner verdict **B — ACCEPT WITH BINDING CONTRACT REFINEMENTS**,
  refinements satisfied). It is **no longer** a candidate, pending review, pending publication, not-authorized, or
  not-started. Authorization chain (distinct steps): discovery gate **G-P4-1B-2B-DISCOVERY-CONTRACT-01** (Option A
  recommended) → separate implementation authorization **G-P4-1B-2B-IMPLEMENTATION-01** (Option A selected; binding API
  contract; two permitted paths; required RED set; RED→GREEN) → implementation (candidate `945f4a3`, base `7d88951`,
  tree `bff45ada`) → independent review verdict **B** → merge **PR #367** (`1c9dff7`) → post-merge verification
  (ancestry PASS; scope **2 files / +367 / −0**; disallowed paths **NONE**) → owner acceptance and closure.
- **Delivered behaviour (OPTION A):** a bounded, **read-only** `SqliteRecordStore.load_accepted_answer_evidence(sid)`
  returning an **immutable `tuple`** of the `answered`-disposition `AssertionRecord`s in the authoritative persisted
  order (store `seq`, via the existing project-scoped `load_contract`); `record_id` preserved as `rec_N` (non-contiguous
  values expected/valid); unknown/absent `sid` → `()` (same as an empty project; no existence leak); malformed /
  unsupported-version / invalid-reference / cyclic content → canonical `ContractError` propagates (fail closed, no
  partial evidence); legacy NULL-`idempotency_key` rows load unchanged. No write/append/repair/rehydration/progression;
  no runtime/UI/route; no change to `record_id`/`rec_N`, the deterministic-output engines, or the P4-1b-2a idempotency
  identity.
- **Does NOT provide (explicit boundary):** no resumable session or "resume exactly where you left off"; no
  reconstructed next question, gaps, maturity, domain/path, transcript, `last_result`, or progression; no full
  deterministic replay or durable output (that is **P4-2**); no accounts/ownership/authorization (that is **Phase 5**);
  no mutation and no UI/runtime surface change.
- **Evidence:** permitted paths exactly `engine/record_store.py` (+38) and
  `tests/test_p4_1b2b_accepted_answer_evidence.py` (+329); source branch `feat/p4-1b2b-accepted-answer-evidence` and the
  SHA-preserving bundle `p4_1b2b_impl_945f4a3.bundle` (SHA-256
  `b04f07688804d27f0cafd7c1e7cc7136da705c3e14efc275e2587ecfef4d365f`) **PRESERVED**. Tests: focused **15 passed**;
  P4-1b-2a regression **60 passed**; protected **227 passed**; full governed suite **1741 passed, 1 skipped, 1 xfailed**.
- **Accepted non-blocking observations (preserved, not fixed):** (1) governance-tree authorization lag — the P4-1b-2b
  gates were reviewed/merged/verified before the committed governance tree recorded them; this synchronization closes the
  lag; (2) protected-regression set composition (226 vs 227) — bookkeeping only; both green; (3) `seq` ordering confirmed
  by manual experiment and by reuse of the proven `load_contract` `ORDER BY seq ASC` read (no isolated in-suite
  ordering-only assertion); (4) plain-`tuple` return and a single `SESSION_STORE`-unchanged no-mutation assertion —
  stylistic/polish only. Honest value note: the net-new capability is modest (it exposes, read-only, evidence P4-1b-2a
  already persists); correct and within scope.
- **Current active implementation contract:** NONE. **P4-2, Phase 5–7, WS17, STG, ACV, PDF, Email, and every FPC
  (FPC-01…FPC-04) remain NOT AUTHORIZED / NOT STARTED.** Decision **D17** and the AISR seven-owner model are preserved.
- **Product-truth boundary (unchanged):** durable **accepted-answer evidence** append (P4-1b-2a) plus its read-only
  reconstruction (P4-1b-2b) exist; full session state / progression / deliverable / outputs are **not** durably restored,
  and "resume exactly where you left off" is not implemented (that is P4-2 / Phase 5). The live working session state
  otherwise remains in-memory (`SESSION_STORE`).

## Future product capabilities pointer (G-FPC-MAP-01)

Preserved future-product capability classifications and missing-elements-only mapping for **FPC-01 … FPC-04** are
recorded in the **Active Execution Roadmap** (Future Product Capability Integration Map) and the **Owner Decision
Register** (D-FPC-MAP-01 … -10) under **G-FPC-MAP-01**. **FPC-01 through FPC-04 remain: PRESERVED — NOT AUTHORIZED FOR
IMPLEMENTATION.** `ACTIVE_INCREMENT_CONTRACT.md` was **unchanged by G-FPC-MAP-01**; **no FPC gate has been activated.** (This is a pointer
only — see the roadmap/register for the full map.) **[Current status:]** the B3 blocker that was historically
`CONTRACT AMENDMENT / OWNER DECISION REQUIRED` was **RESOLVED (Option A)**, and **P4-1b-2a is now IMPLEMENTED / MERGED /
POST-MERGE VERIFIED / OWNER ACCEPTED / CLOSED** (PR #365, merge `77bd10c`). **P4-1b-2a implementation status no longer
controls or blocks the FPC mapping.** Independently of that, **FPC-01, FPC-02, FPC-03, FPC-04A, and FPC-04B remain
PRESERVED in their approved future sequencing — NOT AUTHORIZED FOR IMPLEMENTATION / NOT STARTED.** The historical
G-FPC-MAP-01 decision lineage (and its now-superseded P4-1b-2a boundary, see `OWNER_DECISION_REGISTER.md` D-FPC-MAP-10,
labelled HISTORICAL / SUPERSEDED) is preserved.

## Phase 4 entry direction (Durable Data and Evidence Foundation) — ENTRY HISTORY (Phase 4 is now FORMALLY CLOSED; see the Post-PR #369 boundary above)

*The entry-direction statements below (including "Phase 4 implementation: NOT AUTHORIZED / Next implementation gate: NOT
AUTHORIZED") record the Phase-4 ENTRY decision and were accurate before the phase was executed. **Current truth: Phase 4
is FORMALLY CLOSED within its implemented boundary** (P4-0 record contract; P4-1a durable store; P4-1b-1 runtime store;
P4-1b-2a durable answered append + idempotency; P4-1b-2b accepted-answer evidence; P4-2 Level-1 read-only reconstruction)
— see the "Post-PR #369 boundary" current-truth section above. Phase 4 delivered no writable continuation, accounts,
version history, output email/download, ACV, AI Coach, or FPC. **NEXT ELIGIBLE PHASE: Phase 5 — NOT STARTED / NOT
AUTHORIZED.***

- **G-P4-ENTRY-DEFINITION:** COMPLETED AND ACCEPTED (owner verdict **B**). **G-P4-DOC-01:** documentation-only gate
  recording owner decisions D-P4-01 … D-P4-10.
- **Phase 4 entry direction:** `ACCEPTED` (Lean minimum durable-data & evidence foundations). **Phase 4
  implementation:** `NOT AUTHORIZED`. **P4-0 implementation:** `NOT AUTHORIZED`. **Active implementation contract:**
  NONE. **Next implementation gate:** NOT AUTHORIZED.
- **Canonical source of truth:** `docs/governance/PHASE_4_DURABLE_DATA_AND_EVIDENCE_ENTRY_DECISION.md` (governs; not
  duplicated here). Concerns the Product-Foundation Phase 4, distinct from the Path-N lane "Phase 4 runtime
  integration". Obligation groups `P4-OBL-DATA/PROV/REEVAL/OUTPUT/LIFE/DELETE/MIGRATE/SEC` (Phase 4) plus deferred
  `P4-OBL-P5/P6/P7/WS17/STG/UX/FUTURE`.
- **Boundary:** Phase 4 = foundation owner only. **Phase 5** (accounts/ownership/access), **Phase 6** (domain),
  **Phase 7** (provider), **WS17**, **STG** remain NOT AUTHORIZED; provider NOT SELECTED; exact UX NOT AUTHORIZED
  (Phase 3E artifact recovery required first). Decision **D17** and the AISR seven-owner model are preserved.

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
- **Durable accepted-answer persistence (P4-1b-2a, PR #365):** a durable project envelope + accepted-answer evidence
  ledger, with a **separate durable idempotency identity** and **persist-before-acknowledge** append for accepted
  answers. The live working session state otherwise remains **in-memory (`SESSION_STORE`)** — `SESSION_STORE` itself is
  **not** durable; only the accepted-answer evidence is persisted.
- **Read-only accepted-answer evidence reconstruction (P4-1b-2b, PR #367):** a bounded, read-only
  `SqliteRecordStore.load_accepted_answer_evidence(sid)` returning an immutable `tuple` of the `answered`-disposition
  `AssertionRecord`s in persisted (`seq`) order, reusing the project-scoped `load_contract` read. It is **evidence
  reconstruction only** — no mutation, no runtime/UI/route, no session resume, and **not** full deterministic replay
  (that is P4-2).
- **Deterministic read-only reconstructed review state (P4-2 Level-1, PR #369):**
  `engine.session_reconstruction.reconstruct_review_state(store, sid)` — for a durably recorded **Path-N** session it
  additively persists the reconstruction inputs (`seed_idea_text`, `confirmed_domain`, `recon_path`,
  `engine_contract_version`) at creation, loads accepted-answer evidence in `seq` order, builds a **fresh** canonical
  `IdeaState`, replays the seed then answer contents through the **unchanged** `run_iteration`, and returns an
  **immutable** `ReconstructedReviewState` (maturity, stage, open gaps, next question, ordered evidence). Version
  `p4-2-level1-recon-v1`; replay limit **500**. **Read-only** — no mutation, no UI, no AI/network, no session resume,
  no writable continuation; legacy/missing-metadata/unsupported-path/version-mismatch fail closed to Level-0 evidence;
  malformed history raises `ContractError`; no prior-output validity claim.
- **Bounded UX accessibility & disclosure baseline (post-Phase-3 gates #342–#345):** a shared application
  shell (viewport, `<main>` landmark, skip-to-content link, persistent "Temporary session" header disclosure);
  a static informational Data & Session trust surface at `GET /data-and-session` with a header "Learn more"
  link (S15); an entry-surface alignment (idea-field `<label>` + one temporary-session intake-disclosure line);
  and a guided-session answer-field `<label>`. These are **presentation/accessibility-only, behavior-preserving**
  additions — no route, session, engine, validation, persistence, account, or ownership change. The full Phase 3E
  nine-step journey (including the S01 "Step 1 of 9" stepper) is **NOT** implemented and remains deferred.

## Not implemented / not authorized

- **Full durable session persistence / writable continuation** — full live session resume, complete runtime-session
  restoration, writable continuation from reconstructed state, progression restoration/replay into a live editable
  session, and durable ownership-linked session continuation (separately gated: **writable continuation / Phase 5**).
  *(Note: durable accepted-answer evidence append IS implemented under P4-1b-2a; its read-only evidence reconstruction
  IS implemented under P4-1b-2b; and deterministic **read-only** reconstructed review state IS implemented under P4-2
  Level-1 — see "Implemented capabilities" above. This line is about WRITABLE full-session durability / resume, which is
  NOT implemented: P4-2 Level-1 is read-only review reconstruction only — it cannot continue, submit, or rehydrate a
  live session.)* Accounts; authentication; authorization; billing/subscription.
- ACV (Approximate Concept Visualization); Direct Output Download (PDF); Email Delivery.
- Sponsors/themes; administrative notice; privacy-control implementation; full Arabic/RTL;
  accessibility; multi-domain runtime; Path T / FORM T (BLOCKED).
- Structured Technical Guidance — RESERVED / INACTIVE / separately authorized.

## Accepted limitations (honest, not waived)

End-to-end runtime invocation not certified; `main` stale/unreconciled; `/tmp` transcript
handling (Phase 4 remediation); `iot_electronics` latent/legacy (not loaded; future
separately authorized domain-activation workstream); **durable persistence is bounded: durable
accepted-answer evidence append IS implemented and merged (P4-1b-2a, PR #365) — durable project
envelope + accepted-answer ledger — and its read-only evidence reconstruction IS implemented and
merged (P4-1b-2b, PR #367); but full session state / progression / deliverable / outputs
are NOT durably restored and "resume exactly where you left off" is not implemented (that is
P4-2 / Phase 5, separately gated); the live working session state otherwise remains in-memory**;
narrow Arabic/RTL. Full register: OD-T and the
canonical plan. (The former `tests/test_domain_registry.py` ~31 failing baseline is RESOLVED
— DISC-007 CLOSED via the current bounded remediation program; suite `0 failed`, XPASS `0`;
deferred Domain Registry v1.0 hardening rules remain FORMALLY DEFERRED — NOT IMPLEMENTED —
NOT SOLVED; see the Remediation Program Formal Closure Record.)

## Active holds / forbidden work now

No implementation contract is active. P4-0 is closed; P4-1/P4-2 and every later gate require separate explicit owner authorization. No implementation, UI, runtime, engine, schema, database, prompt/AI, tests-as-gates,
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
