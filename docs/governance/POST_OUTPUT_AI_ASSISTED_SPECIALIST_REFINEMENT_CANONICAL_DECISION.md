# Post-Output AI-Assisted Specialist Refinement (AISR) — Canonical Capability Decision

**Working gate label:** G-AISR-DOC-01 — Canonical Capability Decision and Deferred-Dependency Recording.
This is a **documentation-only** governance record. It is the **single canonical source of truth** for the
Post-Output AI-Assisted Specialist Refinement (AISR) product direction. Other governance documents must **reference**
this record concisely and must **not** duplicate its full content.

**Status:** `ACCEPTED PRODUCT DIRECTION` · `IMPLEMENTATION NOT AUTHORIZED`.

This record grants **no** implementation authority. It authorizes **no** code, schema, prompt, UI, test, provider,
domain, persistence, account, Phase 4/5/6/7, WS17, or STG work. It defines **no** final database schema, API, route,
prompt, or exact UX. It does **not** finally define WS17 and does **not** expand or activate STG. It does **not**
reopen Phase 3 and does **not** authorize Phase 4.

---

## 1. Title and identity

- **Capability:** Post-Output AI-Assisted Specialist Refinement (AISR).
- **Repository:** `Amirjaferali/inventorai`.
- **Authoritative branch:** `feature/atomic-json-session-persistence`.
- **Recorded on live tip:** `687b71010f12c630eda8fb5eeb84adc941e02edd` (Merge PR #349). Always re-resolve the live tip
  from Git (`git rev-parse origin/feature/atomic-json-session-persistence`); do not trust a prose-pinned SHA.
- **Origin gates:** `G-AISR-MATERIAL-DECISION` (read-only material-product-change decision package) → this
  `G-AISR-DOC-01` documentation-only recording.

## 2. Owner acceptance verdict

- **G-AISR-MATERIAL-DECISION:** COMPLETED AND ACCEPTED — owner verdict **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**.
- **G-AISR-DOC-01:** documentation-only gate authorized to record owner decisions **D-AISR-01 through D-AISR-10**
  (below) and their deferred dependencies. No implementation is authorized by that acceptance.

## 3. Scope and non-goals

**Scope of the capability (as an accepted future direction only):** an optional, post-journey experience in which,
after the user has completed the governed idea journey and received the current truthful output, an AI advisory layer
— linked to that project's accepted inputs, current output, gaps, risks, missing evidence, supported domain, and
prior accepted decisions — may discuss the output and propose improvements. Every AI proposal is advisory; the user
is the final decision-maker; accepted proposals become structured, reviewable changes that are then re-evaluated by
the deterministic engine, never by the AI.

**Non-goals (binding):** not a general-purpose chatbot; not an engine bypass (AI never sets maturity, readiness,
gaps, risks, or final conclusions); not silent application of proposals; not targeted partial re-evaluation (see
D-AISR-06); not durable versioning, restoration, or branching now; not project derivation, persistence, accounts,
domain activation, or provider integration now; not a redefinition of WS17 or an expansion of STG.

## 4. Owner decisions D-AISR-01 … D-AISR-10 (as recorded)

- **D-AISR-01 — Capability direction.** ADOPTED AS `ACCEPTED FUTURE PRODUCT DIRECTION`: Post-Output AI-Assisted
  Specialist Refinement. Does not authorize implementation, runtime AI, provider selection, WS17 activation, STG
  activation, schema design, UX implementation, or Phase 4.
- **D-AISR-02 — Responsibility model.** ADOPTED DIRECTIONALLY: (1) WS17 may later become the user-facing advisory and
  conversational umbrella; (2) STG remains a separate, bounded technical-guidance capability that WS17 may invoke
  where separately authorized; (3) post-output refinement remains the governed change-application lane; (4) the
  deterministic engine remains the sole authority for maturity, readiness, gaps, risks, and final output conclusions;
  (5) Phase 4–7 provide persistence, ownership, domain, and provider foundations. Does **not** finally define WS17 and
  does **not** expand or activate STG.
- **D-AISR-03 — Material project-identity change.** ADOPTED DIRECTIONALLY: a limited enhancement preserving core
  problem, target user, primary outcome, core value proposition, essential solution identity, and supported domain
  may remain in the current project and undergo full re-evaluation; a change that materially changes project identity
  should require a new independent project record, a new full governed journey, preservation of the original project,
  explicit user-approved selective copying only, no transfer of stale engine conclusions, and full fresh deterministic
  evaluation. Future implementation must combine deterministic strong signals, explicit user confirmation, and a safe
  default toward a new project where material identity is ambiguous. Does **not** authorize branching, restoration,
  project derivation, or project-creation implementation now.
- **D-AISR-04 — Content-origin model.** ADOPTED AS TARGET FUTURE GOVERNANCE VOCABULARY ONLY: `USER_ORIGINATED`,
  `AI_PROPOSED`, `USER_MODIFIED_AI_PROPOSAL`, `USER_ACCEPTED`, `ENGINE_DERIVED`, `EXTERNAL_EVIDENCE`, `UNRESOLVED`,
  `REJECTED`, `FUTURE_OPPORTUNITY`. Authorizes recording the conceptual provenance model only — no final database
  schema, migrations, code enums, prompts, AI integration, or runtime storage changes.
- **D-AISR-05 — Refinement rounds.** ADOPTED: refinement should be open-ended within truthful operational, security,
  cost, data-lifecycle, project-lifecycle, and provider controls; no arbitrary product cap (e.g. three, five, or ten
  rounds) without a justified operational reason. Does not authorize unlimited live AI usage before required controls
  exist.
- **D-AISR-06 — Re-evaluation.** ADOPTED: full deterministic re-evaluation is mandatory after every accepted material
  change; targeted partial re-evaluation remains prohibited unless a separately authorized and independently verified
  deterministic dependency model proves it safe. This preserves accepted decision D17.
- **D-AISR-07 — Phased dependency map.** ADOPTED AS A GOVERNING DEPENDENCY MAP ONLY (see §11). Phase 4 is **not**
  automatically expanded to implement WS17, STG, live AI, final UX, provider integration, the full new-project user
  experience, project branching, restoration, exact comparison UI, or every AISR obligation; Phase 4 may implement
  only the foundations explicitly authorized by a future separate Phase 4 contract.
- **D-AISR-08 — Non-forgetting governance model.** ADOPTED (see §14): one canonical non-authorizing record; one phased
  dependency matrix within it; minimal cross-references; deferred-obligation entries for every unimplemented
  obligation; an AISR entry checklist before each affected future gate; explicit deferred statuses. Full capability
  text must not be duplicated across documents.
- **D-AISR-09 — Phase 3E artifact.** ADOPTED: recovery of the accepted full Phase 3E implementation-level artifact is
  required before exact WS17/AISR screen design, exact UX amendment, or any claim that a proposed screen duplicates or
  replaces the accepted 3E design. The artifact is **not** required to record this product direction and dependency
  model. The missing Phase 3E artifact must not be reconstructed from summaries.
- **D-AISR-10 — Next action.** ADOPTED: the next action is this `G-AISR-DOC-01` documentation-only canonical decision
  recording — not Phase 4 implementation, not a Phase 4 entry-contract, not WS17, not STG, not AI-provider selection,
  not schema design, not final UX, not code or test implementation.

## 5. Accepted responsibility model — six future owners plus one cross-cutting integration lane

Per D-AISR-02: the required dependency model is **not** "three phases." It consists of **four numbered phases, two
protected workstreams, and one cross-cutting governed integration lane — seven distinct owners in total** — over
which AISR obligations are mapped separately (§11, §13). **No owner is omitted, merged away, or treated as implied by
another.** Above all seven, the deterministic engine remains the sole evaluation authority.

**Sole evaluation authority (above all owners):**
- **Deterministic engine** — the only authority for maturity, readiness, gaps, risks, and final output conclusions.
  Unchanged by this record; AISR never lets AI set any of these.

**Four numbered phase owners (foundations):**
1. **Phase 4 — Durable data, records, provenance, lifecycle, retention, deletion, snapshots, supersession, and
   re-evaluation foundations.**
2. **Phase 5 — Accounts, authentication, authorization, private access, project access control, ownership
   boundaries, and cross-session continuity.**
3. **Phase 6 — Domain capability foundation, truthful specialist labelling, domain routing, registry hardening, and
   unsupported-domain behaviour.**
4. **Phase 7 — AI-provider integration, context transfer, consent, privacy, provider retention/deletion, failure
   handling, cost, rate limits, abuse prevention, fallback, and observability.**

**Two protected workstream owners:**
5. **WS17 — AI Coach (user-facing advisory):** user-facing advisory experience, output discussion, challenge,
   alternatives, proposal creation, and user interaction control. **Functional scope remains undefined and is not
   defined here.**
6. **STG (D13 / CAP-01) — bounded technical guidance:** bounded structured technical guidance, domain evidence,
   assumptions, trade-offs, research direction, specialist category, and explicit technical limits. **Reserved and
   inactive; not expanded here.**

**One cross-cutting governed integration lane:**
7. **Post-output refinement:** application of user-accepted changes, change classification, same-project vs
   new-project routing, full deterministic re-evaluation, updated output, and change visibility. **Post-output
   refinement is NOT a substitute for any of the six phase/workstream owners; it coordinates their outputs and
   applies user-accepted changes through the deterministic engine.**

**Distinction preserved (binding):** foundation (Phase 4) ≠ ownership (Phase 5) ≠ domain (Phase 6) ≠ provider
(Phase 7) ≠ advisory (WS17) ≠ technical guidance (STG) ≠ change-application (post-output refinement). No obligation
may be assigned only to a generic "later phase," and no obligation may be lost by treating WS17, STG, or refinement
as equivalent to another owner.

## 6. Change-type model (planning only)

Six proposed change types, each requiring later separate authorization to implement:
(1) **USER DATA CORRECTION** — corrects an existing accepted input; same project; full re-evaluation; not feasible
today (no edit/supersession route). (2) **GAP RESOLUTION** — supplies evidence closing an open gap; same project;
full re-evaluation. (3) **LIMITED ENHANCEMENT** — additive improvement preserving identity; same project; full
re-evaluation. (4) **SCOPE EXPANSION** — broadens scope with identity intact-but-stressed; same project with review,
or new project if borderline. (5) **MATERIAL PROJECT-IDENTITY CHANGE** — changes core problem/user/value/solution/
domain; new independent project; original preserved (see §8). (6) **FUTURE OPPORTUNITY** — recorded, not applied.

## 7. Project-identity direction (planning only)

Per D-AISR-03: distinguish preserved identity from material identity change using **deterministic strong signals**
where possible (e.g. change of supported domain, safety class, regulatory context, primary operating environment) +
**explicit user-confirmation points** for signals that are not reliably deterministic (core problem, target user,
primary outcome, core value proposition, essential solution concept, commercial model, intended evidence/success
criteria) + a **safe default**: on material ambiguity, do not silently mutate the original; treat as material →
prefer a new project (or explicit user confirmation to remain same-project); full re-evaluation always. Adopted rule:
**material identity change → new independent project record + new full governed journey + original preserved +
user-approved selective copying only + no stale engine conclusions + full fresh deterministic evaluation.** Deferred
to Phase 4 (records) and Phase 5 (ownership/access).

## 8. Content-origin target vocabulary (planning only)

Per D-AISR-04, the target future provenance vocabulary is: `USER_ORIGINATED`, `AI_PROPOSED`,
`USER_MODIFIED_AI_PROPOSAL`, `USER_ACCEPTED`, `ENGINE_DERIVED`, `EXTERNAL_EVIDENCE`, `UNRESOLVED`, `REJECTED`,
`FUTURE_OPPORTUNITY`. Only `USER_ACCEPTED` (and `USER_ORIGINATED`/`EXTERNAL_EVIDENCE`) content may enter deterministic
re-evaluation; `AI_PROPOSED`/`USER_MODIFIED_AI_PROPOSAL` do not affect project truth until explicitly accepted;
`ENGINE_DERIVED` is authoritative output. This is a **conceptual** model only — no code enums, schema, or migrations
are authorized. Today the runtime records only `OWNER_STATED` / `LEGACY_UNSPECIFIED` with `UNVALIDATED` validation;
the target vocabulary is additive and belongs to Phase 4 (with provider-sourced `AI_PROPOSED` content gated to
Phase 7).

## 9. Open-ended refinement rule

Per D-AISR-05: refinement is open-ended within truthful operational, security, cost, data-lifecycle,
project-lifecycle, and provider controls; no arbitrary numeric round cap without a justified operational reason.
Open-ended live AI is not authorized before the required Phase 7 controls exist.

## 10. Full re-evaluation rule

Per D-AISR-06: full deterministic re-evaluation is mandatory after every accepted material change. Targeted partial
re-evaluation remains prohibited unless a separately authorized and independently verified deterministic dependency
model proves it safe. This preserves accepted decision D17.

## 11. Phased dependency matrix (governing dependency map — D-AISR-07)

The matrix maps obligations across the **seven distinct owners**: four numbered phases (**Phase 4, Phase 5, Phase 6,
Phase 7**), two protected workstreams (**WS17, STG**), and one cross-cutting governed integration lane (**post-output
refinement**). Every obligation names a specific owner; **none is assigned to a generic "later phase," and none is
merged into or implied by another owner.** All seven obligation groups are present and distinct: `AISR-OBL-P4-*`,
`AISR-OBL-P5-*`, `AISR-OBL-P6-*`, `AISR-OBL-P7-*`, `AISR-OBL-WS17-*`, `AISR-OBL-STG-*`, `AISR-OBL-REFINE-*`. The
additional `AISR-OBL-UX-01` row is a cross-cutting UX obligation dependent on the post-output-refinement lane and
Phase 3E artifact recovery — it is **not** a separate owner and does not substitute for any of the seven groups.

| Obligation ID | Obligation (grouped) | Responsible phase / workstream | Prerequisite | Earliest safe point | Status | Separate owner auth required | Implementation prohibited before | Future acceptance evidence |
|---|---|---|---|---|---|---|---|---|
| AISR-OBL-P4-01 | Durable project records; accepted source inputs; immutable record identifiers; provenance compatibility; supersession and retention foundations; snapshot lifecycle; deletion/retention; auditability; forward-compatibility for future AI-proposal/acceptance records | Phase 4 | AISR direction (this record) | Phase 4 entry contract | FOUNDATION DEFERRED TO PHASE 4 | Yes (Phase 4 contract) | Any AISR runtime, WS17, STG, or provider work | Phase 4 contract + independent review + post-merge verification |
| AISR-OBL-P4-02 | Full deterministic re-evaluation rebuilt entirely from accepted source inputs (no reliance on cached conclusions) | Phase 4 (deterministic) | AISR-OBL-P4-01 | Phase 4 | FOUNDATION DEFERRED TO PHASE 4 | Yes | Targeted partial re-evaluation (prohibited per D-AISR-06) | Deterministic tests + independent review |
| AISR-OBL-P4-03 | Project-identity classification foundation; new independent project-record foundation; original-project preservation | Phase 4 (records) / Phase 5 (ownership) | AISR-OBL-P4-01 | Phase 4 (record) | FOUNDATION DEFERRED TO PHASE 4 | Yes | Provider/AI-driven classification | Phase 4/5 contracts + review |
| AISR-OBL-P5-01 | Accounts; authentication; authorization; private-by-default project access; project ownership and access control; original/new-project access; cross-session and cross-device continuity | Phase 5 | Phase 4 closure | Phase 5 | OWNERSHIP DEFERRED TO PHASE 5 | Yes | — | Phase 5 contract + review |
| AISR-OBL-P6-01 | Domain capability foundation; truthful specialist labeling; domain routing; unsupported-domain behavior; domain-registry hardening dependencies | Phase 6 | Phase 4 | Phase 6 | DOMAIN DEFERRED TO PHASE 6 | Yes | Any "specialist" claim without domain depth | Phase 6 contract + review |
| AISR-OBL-P7-01 | AI-provider integration; context transfer and consent; provider retention/deletion; privacy and confidentiality; provider failure behavior; rate limits; abuse prevention; cost controls; fallback; observability | Phase 7 | Phases 4–6 | Phase 7 | PROVIDER DEFERRED TO PHASE 7 | Yes (+ provider selection) | Any runtime AI | Phase 7 contract + security/privacy review |
| AISR-OBL-WS17-01 | User-facing advisory experience: output discussion, challenge, alternatives, proposal creation, user control, interaction experience | WS17 | WS17 functional definition + Phases 4–7 | After WS17 defined and foundations exist | WS17 NOT AUTHORIZED | Yes (WS17 gate) | Embedding advisory AI into UX; defining WS17 scope | WS17 definition gate + review |
| AISR-OBL-STG-01 | Bounded structured technical guidance: domain evidence, assumptions, trade-offs, research direction, specialist category, explicit limits | STG (D13 / CAP-01) | Domain foundation (Phase 6) + STG authorization | After STG separate authorization | STG NOT AUTHORIZED | Yes (STG hard-stop) | Any solution-generation or STG surface | STG authorization gate + review |
| AISR-OBL-REFINE-01 | Application of user-accepted changes; change classification; same-project vs new-project routing; full re-evaluation; updated output; change visibility | Post-output refinement | AISR-OBL-P4-01/02/03 | Phase 4 (deterministic core) | FOUNDATION DEFERRED TO PHASE 4 | Yes | AI-driven application of changes | Deterministic tests + review |
| AISR-OBL-UX-01 | Exact UX: screens, flows, accessibility (WCAG baseline), RTL/LTR bilingual | UX (post-3E) | Phase 3E artifact recovery (D-AISR-09) | After artifact recovery + foundations | IMPLEMENTATION NOT AUTHORIZED | Yes | Any exact UX design without 3E artifact | UX gate + independent review |

## 12. Phase 4 forward-compatibility obligations

Phase 4 (when separately authorized) must preserve, at minimum: project identity; immutable record identifiers;
accepted-input records (append-only); supersession relationships; deterministic-output records; current-working
snapshot; lifecycle status; retention/deletion status; and the ability to **rebuild and fully re-evaluate from
accepted source inputs** with **no silent copying of engine conclusions**. It must reserve (without populating)
forward-compatible fields for AI-proposal records, user-acceptance records, an optional project-origin/derivation
reference, and evidence references. Records must be additive and origin-tagged so Phase 5 (ownership), Phase 6
(domain specialization), and Phase 7 (provider data) attach without destructive redesign; no schema may assume a
single session or fuse AI and user content.

## 13. Deferred obligations

Each obligation below is `IMPLEMENTATION NOT AUTHORIZED` until its owning phase/workstream is separately authorized.

- **AISR-OBL-P4-01** — Durable project/record foundations (see §11). Owner: Phase 4. Reason for deferral: no durable
  persistence exists (runtime is in-memory). Prerequisite: Phase 4 entry contract. Separate owner authorization:
  required. Prohibited early interpretation: that any durable save, version, or history exists. Completion evidence
  required: Phase 4 contract, independent review, post-merge verification.
- **AISR-OBL-P4-02** — Deterministic full re-evaluation from accepted source inputs. Owner: Phase 4. Reason: no
  user-invocable full re-scoring exists today. Prerequisite: AISR-OBL-P4-01. Separate owner authorization: required.
  Prohibited early interpretation: that targeted partial re-evaluation is permitted (it is not — D-AISR-06).
  Completion evidence: deterministic tests + review.
- **AISR-OBL-P4-03** — Project-identity classification + new-project-record foundation. Owner: Phase 4/5. Reason: no
  committed project-record or derivation model exists. Prerequisite: AISR-OBL-P4-01. Separate owner authorization:
  required. Prohibited early interpretation: that project derivation, branching, or restoration exists. Completion
  evidence: Phase 4/5 contracts + review.
- **AISR-OBL-P5-01** — Accounts, ownership, and access. Owner: Phase 5. Reason: no accounts/auth exist; no role is
  legal proof of ownership (OD-E/OD-J). Prerequisite: Phase 4 closure. Separate owner authorization: required.
  Prohibited early interpretation: that ownership or access control exists. Completion evidence: Phase 5 contract.
- **AISR-OBL-P6-01** — Domain specialization + truthful specialist labeling. Owner: Phase 6. Reason: MVP runtime is
  electronics/electrical only; registry hardening is deferred. Prerequisite: Phase 4. Separate owner authorization:
  required. Prohibited early interpretation: calling the assistant "specialist" without domain depth. Completion
  evidence: Phase 6 contract.
- **AISR-OBL-P7-01** — Provider integration + privacy/security/cost/failure controls. Owner: Phase 7. Reason: runtime
  AI is disabled; no provider integration or rate/cost controls exist. Prerequisite: Phases 4–6. Separate owner
  authorization: required (plus provider selection). Prohibited early interpretation: that any live AI is available.
  Completion evidence: Phase 7 contract + security/privacy review.
- **AISR-OBL-WS17-01** — User-facing advisory experience. Owner: WS17. Reason: WS17 functional scope is undefined and
  post-gate. Prerequisite: WS17 functional-definition gate + Phases 4–7. Separate owner authorization: required.
  Prohibited early interpretation: that WS17 is defined or may embed into UX now. Completion evidence: WS17 gate.
- **AISR-OBL-STG-01** — Bounded structured technical guidance. Owner: STG (D13/CAP-01). Reason: STG is reserved and
  inactive (hard stop). Prerequisite: Phase 6 domain foundation + STG authorization. Separate owner authorization:
  required. Prohibited early interpretation: that STG is expanded, activated, or made solution-generating. Completion
  evidence: STG authorization gate.
- **AISR-OBL-REFINE-01** — Governed change-application lane. Owner: post-output refinement. Reason: only the
  entry-point-only Refine (PR #348, classification A) exists; no change-application, routing, or full re-evaluation
  flow exists. Prerequisite: AISR-OBL-P4-01/02/03. Separate owner authorization: required. Prohibited early
  interpretation: that accepted-change application exists. Completion evidence: deterministic tests + review.
- **AISR-OBL-UX-01** — Exact UX (accessibility/RTL). Owner: UX gate. Reason: the full Phase 3E artifact is not in the
  repository (D-AISR-09). Prerequisite: Phase 3E artifact recovery + foundations. Separate owner authorization:
  required. Prohibited early interpretation: that any exact AISR/WS17 screen is designed or approved. Completion
  evidence: UX gate + independent review.

## 14. Non-forgetting model

Per D-AISR-08, the minimum safe structure is: (1) this **one canonical non-authorizing record**; (2) the **phased
dependency matrix** (§11) inside it; (3) **minimal, concise cross-references** from affected phases and workstreams
(no full-text duplication); (4) the **deferred-obligation entries** (§13) for every unimplemented obligation; (5) the
**future-gate AISR entry checklist** (§15); (6) explicit statuses: `ACCEPTED PRODUCT DIRECTION`,
`FOUNDATION DEFERRED TO PHASE 4`, `OWNERSHIP DEFERRED TO PHASE 5`, `DOMAIN DEFERRED TO PHASE 6`,
`PROVIDER DEFERRED TO PHASE 7`, `WS17 NOT AUTHORIZED`, `STG NOT AUTHORIZED`, `IMPLEMENTATION NOT AUTHORIZED`.

## 15. Required future-gate AISR entry checklist

Every affected future gate must answer, before proceeding: (1) Does this gate own an AISR obligation (§11/§13)?
(2) Is the obligation in scope now, or forward-compatibility only? (3) Is separate owner authorization required?
(4) Does implementation preserve decision D17? (5) Does it distinguish user-originated, AI-proposed, user-accepted,
and engine-derived content? (6) Does it preserve the original project? (7) Does it avoid stale engine conclusions?
(8) Does it require full re-evaluation? (9) Does it require Phase 3E artifact recovery? (10) Does it affect privacy,
deletion, retention, ownership, domain, provider, accessibility, RTL, security, cost, or failure behavior? (11) What
remains deferred? (12) What evidence proves completion?

## 16. Phase 3E artifact-recovery condition

Per D-AISR-09, recovery of the accepted full Phase 3E implementation-level artifact (recorded external; SHA-256
`52e6522e9e842e3e9a3250c1b0ba1e21d99b9d400099c0324da2f61cb0fab0cf`) is required before exact WS17/AISR screen design,
exact UX amendment, or any claim that a proposed screen duplicates or replaces the accepted 3E design. It is not
required for this direction/dependency record. The missing artifact must not be reconstructed from summaries.

## 17. Separate authorization requirements

Each of the following requires its own separate explicit owner authorization (and, per Lean §5, independent review):
Phase 4 entry contract; Phase 5; Phase 6; Phase 7 (plus provider selection); WS17 functional definition; STG
activation; the deterministic dependency model that would be a precondition for any targeted partial re-evaluation;
the exact-UX gate (after Phase 3E artifact recovery). No entry here authorizes any of these; recording future work
authorizes nothing.

## 18. Explicit implementation prohibitions

This record authorizes no product implementation, code, test, schema, prompt, UI/template, provider selection, AI
integration, persistence, accounts/authentication, domain activation, release, or deployment; no Phase 4/5/6/7
implementation; no WS17 activation or definition beyond the accepted directional relationship; no STG activation or
expansion; no Phase 3 reopening; no exact UX design; and no merge without separate owner authorization.

## 19. Compatibility, retention, deletion, rollback, and legacy boundaries

- **Compatibility:** the existing append-only interaction ledger and read-only whole-idea re-derivation are
  forward-compatible with a future proposal/provenance model **only if** new origin values are additive and do not
  mutate existing records.
- **Retention/deletion:** conversation, AI-proposal, and accepted-change retention/deletion are undefined and belong
  to Phase 4 (lifecycle) and Phase 10 (legal wording); no retention/deletion capability exists today.
- **Rollback:** no runtime rollback/undo exists (runtime state is ephemeral, in-memory). Decision D17's
  non-silent-replacement is the only rollback-adjacent guarantee; durable restoration and branching are FUTURE
  RESERVED.
- **Legacy:** disabled/orphan/latent code (the disabled AI-advisory layer, the unimported persistence schema file,
  the latent legacy domain pack, and engine-only supersession/edit primitives) are potential future foundations but
  are **not** wired into the runtime and are **not** authorized by this record.

## 20. Status

`ACCEPTED PRODUCT DIRECTION` · `IMPLEMENTATION NOT AUTHORIZED`.

Phase 4: NOT AUTHORIZED / NOT STARTED. Phase 5/6/7: NOT AUTHORIZED / NOT STARTED. WS17: NOT AUTHORIZED (scope
undefined). STG: NOT AUTHORIZED / NOT EXPANDED. Provider: NOT SELECTED / NOT AUTHORIZED. Exact UX: NOT AUTHORIZED
(Phase 3E artifact recovery required first). Next implementation gate: NOT AUTHORIZED — requires separate explicit
owner authorization. Decision D17 is preserved and not rewritten. This record activates no phase and grants no
implementation authority.
