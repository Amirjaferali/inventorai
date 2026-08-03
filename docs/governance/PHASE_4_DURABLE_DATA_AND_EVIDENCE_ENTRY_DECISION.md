# Phase 4 — Durable Data and Evidence Foundation — Canonical Entry Decision

**Working gate label:** G-P4-DOC-01 — Phase 4 Canonical Entry Contract and Deferred-Boundary Recording.
This is a **documentation-only** governance record and the **single canonical source of truth** for the accepted
Phase 4 entry direction. Other governance documents must **reference** this record concisely and must **not**
duplicate its scope, matrix, decisions, or obligation register.

**Disambiguation (binding):** "Phase 4" here means the **Product-Foundation Phase 4 — Durable Data and Evidence
Foundation** defined in `PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md §5`. It is **distinct** from
the separate Path-N execution-lane "Phase 4 runtime integration" recorded in `PHASE_4_PATH_N_RUNTIME_INTEGRATION_*`.
This record concerns durable-data foundations only.

**Status:** `PHASE 4 ENTRY DIRECTION ACCEPTED` · `PHASE 4 IMPLEMENTATION NOT AUTHORIZED` ·
`P4-0 IMPLEMENTATION NOT AUTHORIZED` · `PHASE 5–7 NOT AUTHORIZED` · `WS17 NOT AUTHORIZED` · `STG NOT AUTHORIZED` ·
`NEXT IMPLEMENTATION GATE NOT AUTHORIZED`.

This record grants **no** implementation authority. It authorizes no code, test, database, schema, migration, enum,
datastore/ORM/vendor selection, Supabase adoption, prompt, UI, provider, Phase 4/5/6/7, WS17, STG, exact UX,
release, or deployment. It defines **no** final schema, SQL, columns, enums, migrations, ORM, datastore, API,
routes, UI, retention periods, or legal deletion policy.

---

## 1. Gate identity

- **Capability:** Product-Foundation Phase 4 — Durable Data and Evidence Foundation (entry direction).
- **Repository:** `Amirjaferali/inventorai`. **Authoritative branch:** `feature/atomic-json-session-persistence`.
- **Recorded on live tip:** `f99b8a24c03230ea46eaffba08667e01583b98df` (Merge PR #350). Always re-resolve the live
  tip from Git.
- **Origin gates:** `G-P4-ENTRY-DEFINITION` (read-only planning package) → this `G-P4-DOC-01` documentation-only
  recording. Governing closed gate: `G-AISR-DOC-01` (PR #350, merged, post-merge verified).

## 2. Owner verdict

- **G-P4-ENTRY-DEFINITION:** COMPLETED AND ACCEPTED — owner verdict **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**.
- **G-P4-DOC-01:** documentation-only gate authorized to record owner decisions **D-P4-01 … D-P4-10** and the Phase 4
  deferred-boundary. No implementation is authorized by that acceptance.

## 3. Status

`PHASE 4 ENTRY DIRECTION ACCEPTED` · `PHASE 4 IMPLEMENTATION NOT AUTHORIZED` · `P4-0 IMPLEMENTATION NOT AUTHORIZED` ·
`ACTIVE IMPLEMENTATION CONTRACT: NONE` · `NEXT IMPLEMENTATION GATE: NOT AUTHORIZED`.

## 4. Authority and scope

The authoritative Phase 4 definition is `PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md §5 "Phase 4
— Durable Data and Evidence Foundation"`. This record adopts a **Lean minimum entry** within that authoritative
ceiling and records the accepted owner decisions and deferred-boundary. It is subordinate to the committed anchors,
the remediation plan, `ACTIVE_EXECUTION_ROADMAP.md`, and the merged AISR canonical decision
(`POST_OUTPUT_AI_ASSISTED_SPECIALIST_REFINEMENT_CANONICAL_DECISION.md`). Decision **D17** and all AISR obligations
are preserved and not rewritten.

## 5. Non-goals (binding)

Phase 4 does not implement: accounts/authentication/authorization/roles/ownership enforcement (Phase 5); AI
proposals, provider data, or live AI (WS17/Phase 7); domain specialization or specialist labels (Phase 6); technical
guidance (STG); exact UX, side-by-side comparison, or revision-difference UI (Phase 3E-recovery + UX gate);
user-facing durable restoration or alternative branching (FUTURE RESERVED, D17); PDF/email/ACV; sponsors/themes/
admin-notice; API/billing; targeted partial re-evaluation; `main` reconciliation; release/deployment. The plan's
"user/project relationship model" and "ownership-claims model" are modeled in Phase 4 only as **data/provenance
records**; authentication, authorization, and enforcement remain Phase 5.

## 6. Owner decisions D-P4-01 … D-P4-10 (as recorded)

- **D-P4-01 — Minimum Phase 4 scope.** ADOPTED: **LEAN MINIMUM SCOPE** — establish the minimum safe durable-data and
  evidence foundations without implementing the full Phase 4 ceiling in the first increment. Does not authorize
  execution.
- **D-P4-02 — Project record and lifecycle foundation.** ADOPTED: immutable project identity; project lifecycle
  state; current-working-snapshot reference; deterministic output linkage; durable records. **Project identity is a
  data identity only** — not account identity, account ownership, authorization, legal ownership, patent ownership,
  or user access control (those are Phase 5 or later).
- **D-P4-03 — Accepted inputs and supersession.** ADOPTED: append-only accepted source-input records; origin and
  validation state; timestamps and sequence; contradiction relationships; supersession relationships; immutable
  retention of prior accepted records; deactivation of superseded records from current evaluation; no silent
  mutation; no silent overwrite; no deletion of history merely to represent correction. Any future route/UI exposing
  correction or supersession requires its own authorized implementation gate.
- **D-P4-04 — Provenance model.** ADOPTED DIRECTIONALLY: implement an extensible provenance foundation. Target
  vocabulary: `USER_ORIGINATED`, `AI_PROPOSED`, `USER_MODIFIED_AI_PROPOSAL`, `USER_ACCEPTED`, `ENGINE_DERIVED`,
  `EXTERNAL_EVIDENCE`, `UNRESOLVED`, `REJECTED`, `FUTURE_OPPORTUNITY`. Phase 4 implements **only** values required by
  current deterministic, user, evidence, and accepted-content behavior; **`AI_PROPOSED` and
  `USER_MODIFIED_AI_PROPOSAL` must not be populated during Phase 4**; the model remains forward-compatible for WS17
  and Phase 7. No final schema, enum, migration, prompt, provider integration, or runtime AI authorized.
- **D-P4-05 — Full deterministic re-evaluation foundation.** ADOPTED: Phase 4 must eventually establish the ability
  to (1) read accepted source inputs; (2) reconstruct the complete current project state; (3) run the full
  deterministic logic; (4) produce a new deterministic output; (5) invalidate stale outputs; (6) preserve prior
  outputs; (7) allow readiness/evaluation to decrease; (8) bind each output to the exact accepted inputs used.
  **Current `derive_readiness` behavior alone is not sufficient proof of full re-evaluation; reloading cached state
  or cached output is not full re-evaluation; targeted partial re-evaluation remains prohibited** unless a separately
  authorized deterministic dependency model is established.
- **D-P4-06 — Retention, deletion, and tombstone direction.** ADOPTED DIRECTIONALLY: define deletion behavior by
  data type — distinguishing logical deletion, tombstone, hard deletion, cascade behavior, audit retention, privacy
  deletion, evidence deletion, output deletion, project deletion, and retention periods. **No single deletion method
  may be applied automatically to every data type; auditability must not become unjustified over-retention.** Legal/
  policy wording belongs to Phase 10 and remains deferred.
- **D-P4-07 — Migration and backward compatibility.** ADOPTED: preserve schema versioning; forward migration;
  rollback of migration where safe; integrity verification before and after migration; backward compatibility for
  accepted records; honest treatment of legacy and temporary data; additive forward compatibility for Phase 5–7.
  **Existing temporary in-memory sessions must not be described as recoverable, saved, or migrated if they were
  never durably stored. The dormant `database/supabase_schema.sql` must not be adopted as the authoritative Phase 4
  schema without separate analysis and authorization.**
- **D-P4-08 — Security, isolation, transactions, and failure handling.** ADOPTED: minimum datastore/persistence
  safety — project-level data isolation; least-privilege service access; environment-sourced datastore secrets;
  production fail-fast; transaction boundaries; partial-write prevention; stale-current-pointer prevention; safe
  persistence/re-evaluation failure behavior; audit events; logging controls; observability; backup/recovery
  boundaries. **Phase 4 must not introduce user accounts, authentication, account authorization, user-role
  enforcement, or ownership enforcement (Phase 5).**
- **D-P4-09 — Phased implementation direction.** ADOPTED DIRECTIONALLY: current Lean sequence P4-0 … P4-4 (§17).
  Planning direction only; authorizes no increment. Exact labels, paths, split, and scope of each increment must be
  defined in a separate authorized increment contract. A smaller split or bounded consolidation may be approved only
  after evidence proves it is safer and Leaner.
- **D-P4-10 — Next action.** ADOPTED: the authorized next action is **G-P4-DOC-01** (this documentation-only
  recording). Not P4-0 implementation, Phase 4 implementation, schema/migration/test/database/code/route/UI changes,
  Phase 5–7, WS17, STG, provider selection, exact UX, or release/deployment.

## 7. Current-state summary (designed / code-exists / runtime-active / owner-authorized)

- Temporary in-memory `SESSION_STORE` (`web/app.py:80`), sid = uuid4 [runtime-active; durable-authorized ✗].
- Append-only `IdeaState` interaction ledger (`record_interaction` "never mutates … never removes"; provenance
  `OWNER_STATED`/`LEGACY_UNSPECIFIED`; `validation_status=UNVALIDATED`) [runtime-active].
- Engine-only supersession/contradiction primitives (`mark_supersession`/`mark_contradiction`), **not
  route-exposed** [code-exists; runtime-unreachable from UI].
- No durable output records; `derive_readiness` re-derives readiness read-only (can decrease; honors supersession),
  but is **not** a full progression re-run and is not user-invocable [runtime-active, read-only].
- **No full user-invocable replay/re-evaluation path** exists.
- Orphaned legacy `database/supabase_schema.sql` (tables `ideas`, `event_log`, `prompt_versions`,
  `gate_rule_versions`, `benchmark_runs`) — **never imported**; reference only, not authoritative [designed-only].
- No migrations; no durable retention/deletion; no accounts/auth. R6/R16 corrected historically (G-SC0); live gaps:
  no rate-limiting, no logging/observability, no backup/restore, residual `/tmp` deferred to Phase 4.

## 8. Authoritative Phase 4 ceiling

Per plan §5 (verbatim "Must include"): persistent project storage; user/project relationship model; evidence model;
provenance model; contribution model; ownership-claims model; version history; append-only/tamper-evident audit
history; file hashing; secure file storage; save/recovery; conflict handling; retention; deletion; export; backup;
restore; disaster recovery; encryption & secret handling; privacy-aware data lifecycle; migration from the in-memory
model; backward compatibility for accepted records; rollback; integrity verification before and after migration.
**Hard rule:** paid subscription activation prohibited until Phase 4 is formally closed and independently verified.

## 9. Lean minimum Phase 4 entry

The first Phase 4 work implements only: durable project identity + accepted-input records + provenance (implemented
subset) + deterministic-output records + snapshot/lifecycle state + full-re-evaluation-from-accepted-inputs
foundation + retention/deletion distinctions + migration-from-in-memory + data isolation/secret handling +
observability/failure/rollback. Ceiling items beyond this (file hashing/secure file storage, export beyond the data
layer, backup/disaster-recovery tooling, user-facing version-history UI) are **staged later within Phase 4 or
forward-compat-reserved**, not first-increment.

## 10. Mandatory Phase 4 foundations

(1) Durable project identity (data-only); (2) append-only accepted source inputs; (3) content-origin provenance
(implemented subset, §11); (4) deterministic output records (bound to exact inputs; no overwrite; current vs
historical); (5) snapshot & lifecycle (working/accepted/superseded/abandoned + retention/deletion status; no durable
restoration/branching); (6) full-re-evaluation foundation (reconstruct from accepted inputs; deterministic; stale
invalidation; readiness may decrease; targeted partial prohibited); (7) retention & deletion (by data type;
audit-preserving); (8) migration & backward compatibility (from in-memory; versioned; rollback; integrity); (9)
security & isolation (per-project separation; least privilege; no account authz); (10) observability & failure
(transactions; partial-write & stale-pointer prevention; audit events; safe failure).

## 11. Provenance — implemented-now vs forward-compatible-only

- **Implement now (Phase 4):** `USER_ORIGINATED`, `USER_ACCEPTED`, `ENGINE_DERIVED`, `EXTERNAL_EVIDENCE`,
  `UNRESOLVED`, `REJECTED`, `FUTURE_OPPORTUNITY`.
- **Reserve forward-compatible only (do NOT populate in Phase 4):** `AI_PROPOSED`, `USER_MODIFIED_AI_PROPOSAL` (no AI
  content is generated until Phase 7/WS17). Records must be additive and origin-tagged.

## 12. Full deterministic re-evaluation — definition

Full re-evaluation = reconstructing complete current project state **from accepted source inputs** and running the
full deterministic logic to produce a new output bound to the exact inputs, invalidating stale outputs while
preserving prior outputs, and permitting readiness/evaluation to decrease. **It is NOT** re-reading cached state or
cached output, and it is **NOT** the current `derive_readiness` readiness re-derivation alone. **Targeted partial
re-evaluation is prohibited** until a separately authorized and independently verified deterministic dependency
model proves it safe (preserves D17 and D-AISR-06).

## 13. Retention / deletion distinctions

Phase 4 must distinguish logical deletion, tombstone, hard deletion, cascade behavior, audit retention, privacy
deletion, evidence deletion, output deletion, project deletion, and retention periods. No single method is applied
automatically to every data type; audit-preservation must not become unjustified over-retention; legal/policy
wording is deferred to Phase 10.

## 14. Migration and backward-compatibility direction

Schema versioning from v1; forward-only migration; rollback where safe; integrity verification before/after;
backward compatibility for accepted records; **honest treatment of ephemeral sessions (never claimed saved/
migrated)**; additive forward-compat for Phase 5–7; the dormant legacy schema is reference-only and not adopted
without separate analysis/authorization.

## 15. Security, isolation, transaction, and failure direction

Per-project isolation; least-privilege service credential; environment-sourced datastore secret with production
fail-fast (extends G-SC0); transaction boundaries; partial-write prevention; atomic current-snapshot-pointer update
(stale-pointer prevention); safe persistence/re-evaluation failure behavior; audit events; logging controls;
observability; backup/recovery boundaries. **No accounts/authentication/authorization/role/ownership enforcement
(Phase 5).**

## 16. Phase 4 / future-phase boundary matrix

Legend: **A** must implement in Phase 4 · **B** Phase 4 forward-compat reserve · **C** Phase 5 · **D** Phase 6 ·
**E** Phase 7 · **F** WS17 · **G** STG · **H** exact-UX / FUTURE RESERVED.

| Item | Classification |
|---|---|
| Durable project records | A |
| Accepted source inputs | A |
| Immutable record identifiers | A |
| Provenance (implemented subset) | A |
| Provenance `AI_PROPOSED` / `USER_MODIFIED_AI_PROPOSAL` | B (reserve; not populated) |
| Validation status | A |
| Supersession | A |
| Contradiction links | A |
| Deterministic output records | A |
| Full re-evaluation foundation | A |
| Stale-output invalidation | A |
| Snapshot lifecycle | A |
| Retention | A |
| Deletion | A |
| Tombstone | A |
| Hard deletion | A (defined per data type) |
| Migration | A |
| Rollback | A |
| Integrity verification | A |
| Transaction safety | A |
| Isolation | A |
| Observability | A |
| Project-origin relationship | B (reserve field) |
| New-project creation | B (record foundation) / C (ownership) |
| Selective copying | B (reserve) / C (ownership) |
| Accounts | C |
| Authentication | C |
| Authorization | C |
| Ownership | C |
| Cross-device access | C |
| Domain specialization | D |
| Specialist labels | D |
| AI proposals | E (generated) / F (created) |
| Provider data | E |
| Conversations (durable) | B (reserve) / E / F |
| WS17 (advisory experience) | F |
| STG (technical guidance) | G |
| Revision difference | H |
| Side-by-side comparison | H (3E-recovery) |
| Branching | H (FUTURE RESERVED) |
| Restoration | H (FUTURE RESERVED) |
| PDF | H (separate gate; P4 secure PDF later) |
| Email | H (separate gate) |
| ACV | H (separate gate) |
| Sponsors / themes / administrative notices | H |
| API | H (Phase 7) |
| Billing | H (Phase 8) |
| Release | H (Phase 10) |

**Forward compatibility does not mean implementation.** No deferred item is moved into Phase 4 merely because a
field or future relationship may later be useful.

## 17. Directional Lean sequence (P4-0 … P4-4)

- **P4-0** — Readiness and storage-contract proof (deterministic, no datastore yet).
- **P4-1** — Durable project records, accepted inputs, provenance subset, supersession, and validation.
- **P4-2** — Deterministic output records and full re-evaluation-from-accepted-inputs foundation.
- **P4-3** — Retention, deletion, migration, rollback, and integrity verification.
- **P4-4** — Security, isolation, observability, failure handling, and formal Phase 4 closure.

Planning direction only. Dependencies: P4-0 → P4-1 → P4-2; P4-3 depends on P4-1/P4-2; P4-4 last. **Authorizes no
increment.** Exact labels/paths/split/scope are defined in a separate authorized increment contract; a smaller split
or bounded consolidation may be approved only after evidence proves it is safer and Leaner.

## 18. Deferred-obligation register (stable IDs)

Each is `IMPLEMENTATION NOT AUTHORIZED` until its owning gate is separately authorized. Fields: description; owner;
reason; prerequisite; earliest safe point; separate authorization; prohibited early interpretation; completion
evidence.

- **P4-OBL-DATA-01** — Durable project + accepted-input foundation. Owner: Phase 4. Reason: no durable store today.
  Prereq: Phase 4 entry contract. Earliest: P4-1. Sep-auth: required. Prohibited early: claiming durable save exists.
  Evidence: durable append-only records survive restart + review.
- **P4-OBL-PROV-01** — Provenance & validation foundation (implemented subset; reserve AI values). Owner: Phase 4.
  Reason: no AI_PROPOSED/USER_ACCEPTED provenance today. Prereq: P4-OBL-DATA-01. Earliest: P4-1. Sep-auth: required.
  Prohibited early: populating AI provenance. Evidence: provenance invariants + tests.
- **P4-OBL-REEVAL-01** — Deterministic rebuild and full re-evaluation from accepted inputs. Owner: Phase 4. Reason:
  no replay path exists. Prereq: P4-OBL-DATA-01/PROV-01. Earliest: P4-2. Sep-auth: required. Prohibited early:
  targeted partial re-eval; treating cached reload as re-eval. Evidence: replay reproduces identical state/output.
- **P4-OBL-OUTPUT-01** — Deterministic output records and stale-output lifecycle. Owner: Phase 4. Reason: no output
  records today. Prereq: P4-OBL-REEVAL-01. Earliest: P4-2. Sep-auth: required. Prohibited early: overwriting prior
  output. Evidence: output bound to inputs; stale invalidation tests.
- **P4-OBL-LIFE-01** — Snapshot and project lifecycle. Owner: Phase 4. Reason: no durable lifecycle. Prereq:
  P4-OBL-DATA-01. Earliest: P4-1/P4-2. Sep-auth: required. Prohibited early: durable restoration/branching.
  Evidence: lifecycle-state tests.
- **P4-OBL-DELETE-01** — Retention and deletion distinctions. Owner: Phase 4. Reason: no retention/deletion. Prereq:
  P4-OBL-DATA-01. Earliest: P4-3. Sep-auth: required. Prohibited early: single blanket deletion; legal wording.
  Evidence: per-type deletion + audit tests.
- **P4-OBL-MIGRATE-01** — Migration, rollback, and integrity. Owner: Phase 4. Reason: no migration. Prereq:
  P4-OBL-DATA-01. Earliest: P4-3. Sep-auth: required. Prohibited early: claiming ephemeral sessions were saved.
  Evidence: migration + rollback + integrity verification.
- **P4-OBL-SEC-01** — Security, isolation, transactions, and failure. Owner: Phase 4. Reason: no isolation/
  observability. Prereq: P4-OBL-DATA-01. Earliest: P4-4. Sep-auth: required. Prohibited early: accounts/auth.
  Evidence: isolation + partial-write + stale-pointer + audit tests.
- **P4-OBL-P5-01** — Deferred account/ownership obligations. Owner: Phase 5. Reason: ownership needs accounts.
  Prereq: Phase 4 closure. Earliest: Phase 5. Sep-auth: required. Prohibited early: any auth/ownership enforcement.
  Evidence: Phase 5 contract.
- **P4-OBL-P6-01** — Deferred domain obligations. Owner: Phase 6. Reason: specialist depth needs domain foundation.
  Prereq: Phase 4. Earliest: Phase 6. Sep-auth: required. Prohibited early: "specialist" claims. Evidence: Phase 6.
- **P4-OBL-P7-01** — Deferred provider obligations. Owner: Phase 7. Reason: runtime AI needs provider. Prereq:
  Phases 4–6. Earliest: Phase 7. Sep-auth: required (+ provider selection). Prohibited early: any live AI. Evidence:
  Phase 7 contract + security/privacy review.
- **P4-OBL-WS17-01** — Deferred assistant obligations. Owner: WS17. Reason: WS17 undefined/post-gate. Prereq: WS17
  definition + Phases 4–7. Earliest: after WS17 defined. Sep-auth: required. Prohibited early: defining/embedding
  WS17. Evidence: WS17 gate.
- **P4-OBL-STG-01** — Deferred technical-guidance obligations. Owner: STG. Reason: STG reserved/inactive. Prereq:
  Phase 6 + STG authorization. Earliest: after STG authorization. Sep-auth: required (hard stop). Prohibited early:
  any STG surface. Evidence: STG gate.
- **P4-OBL-UX-01** — Deferred exact UX and Phase 3E artifact dependency. Owner: UX gate. Reason: 3E artifact
  external/unrecovered. Prereq: Phase 3E artifact recovery + foundations. Earliest: UX gate. Sep-auth: required.
  Prohibited early: exact UX/comparison/difference UI. Evidence: UX gate + review.
- **P4-OBL-FUTURE-01** — Deferred branching, restoration, and other future-reserved capabilities. Owner: FUTURE
  RESERVED. Reason: D17 reserves durable restoration/branching. Prereq: separate owner decision. Earliest: future.
  Sep-auth: required. Prohibited early: implying restoration/branching. Evidence: future decision.

## 19. AISR non-forgetting mapping

This Phase 4 record preserves and references the AISR canonical decision
(`POST_OUTPUT_AI_ASSISTED_SPECIALIST_REFINEMENT_CANONICAL_DECISION.md`): the AISR obligation group **AISR-OBL-P4-***
is realized by the Phase 4 obligations above (P4-OBL-DATA/PROV/REEVAL/OUTPUT/LIFE/DELETE/MIGRATE/SEC). The **seven
distinct AISR owners** are preserved: **Phase 4 = foundation owner only**; **Phase 5 = ownership/access owner**;
**Phase 6 = domain owner**; **Phase 7 = provider owner**; **WS17 = advisory-experience owner**; **STG = bounded
technical-guidance owner**; **post-output refinement = the cross-cutting change-application lane.**

**POST-OUTPUT REFINEMENT IS NOT A SUBSTITUTE FOR PHASE 4, PHASE 5, PHASE 6, PHASE 7, WS17, OR STG.** **Phase 4 must
not absorb obligations belonging to the other six owners** (`AISR-OBL-P5/P6/P7/WS17/STG/REFINE-*` remain with their
owners).

## 20. Future Phase 4 increment checklist (reusable)

Every future P4 increment must answer: (1) which D-P4 decision governs it? (2) which P4 obligation IDs are in scope?
(3) what is explicitly out of scope? (4) implementation or forward-compatibility only? (5) preserves append-only
accepted-input history? (6) prevents silent overwrite? (7) preserves D17? (8) implements full re-evaluation or merely
persists cached output? (9) invalidates stale outputs? (10) can readiness decrease after replay? (11) distinguishes
project identity from account ownership? (12) avoids implementing Phase 5–7, WS17, STG? (13) avoids targeted partial
re-evaluation? (14) preserves privacy deletion and avoids unjustified over-retention? (15) defines migration and
rollback? (16) prevents partial writes and stale pointers? (17) preserves project isolation? (18) requires exact UX
or Phase 3E artifact recovery? (19) what RED proof exists? (20) what GREEN evidence proves completion? (21) what
false-green risks remain? (22) what remains deferred? (23) is formal independent review required? (24) what is the
explicit stop gate?

## 21. Independent-review requirements

This record and every subsequent Phase 4 implementation increment require **formal Lean §5 independent review in a
genuinely separate session**. A subagent inside the authoring session does not qualify.

## 22. Separate authorization requirements

Separate explicit owner authorization (and independent review) is required for: the Phase 4 entry increment contract
(P4-0); each of P4-1 … P4-4; datastore/ORM/vendor selection; any schema/migration; Phase 5; Phase 6; Phase 7 (+
provider selection); WS17 definition; STG activation; the exact-UX gate (after Phase 3E artifact recovery); and any
targeted-partial-re-evaluation dependency model. Recording future work authorizes nothing.

## 23. Exact prohibitions

No code/test/database/schema/migration/enum/ORM/datastore/vendor/Supabase/prompt/UI/config/CI change; no runtime
execution; no implementation-path creation; no Phase 4 or P4-0 implementation; no Phase 5–7; no WS17/STG; no provider
integration; no exact UX; no release/deployment; no push/PR/merge without separate authorization; no final retention
periods or legal deletion policy; no implementation estimates; no code-level contract.

## 24. Explicit status

`PHASE 4 ENTRY DIRECTION ACCEPTED` · `PHASE 4 IMPLEMENTATION NOT AUTHORIZED` · `P4-0 IMPLEMENTATION NOT AUTHORIZED` ·
`PHASE 5–7 NOT AUTHORIZED` · `WS17 NOT AUTHORIZED` · `STG NOT AUTHORIZED` · `PROVIDER NOT SELECTED / NOT AUTHORIZED` ·
`EXACT UX NOT AUTHORIZED (Phase 3E artifact recovery required first)` · `NEXT IMPLEMENTATION GATE NOT AUTHORIZED`.
Decision D17 preserved. AISR seven-owner model preserved. This record activates no phase and grants no implementation
authority.
