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


## P4-0 implementation closure and governance-currency synchronization

**Decision status:** ACCEPTED COMPLETED HISTORY / NO NEW IMPLEMENTATION AUTHORITY.

The owner accepted the independently reviewed and corrected P4-0 implementation, its merge through PR #353,
post-merge verification, and formal closure. The authoritative merge commit recorded for this completed gate is
`286b83ffbd6916086c834658f9e16411ef4de4fe`. This row supersedes earlier register wording only where that wording
states that P4-0 was not authorized or not started; those statements remain historical context, not current status.

| ID | Subject | Status | Implementation authority | Evidence |
|---|---|---|---|---|
| D-P4-0-CLOSE-01 | P4-0 contract and implementation | COMPLETE AND FORMALLY CLOSED | NONE — closed history only | PR #352 contract; PR #353 implementation merge and accepted post-merge verification |
| D-P4-0-CLOSE-02 | Current active implementation contract | NONE | NONE | `ACTIVE_INCREMENT_CONTRACT.md` synchronized status |
| D-P4-0-CLOSE-03 | P4-1 and P4-2 | NOT AUTHORIZED / NOT STARTED | NONE | Separate owner decision and contract required |
| D-P4-0-CLOSE-04 | Governance synchronization | DOCUMENTATION-ONLY | NONE | Four bounded governance paths; no runtime/product change |

**Preserved boundaries:** P4-0 did not implement durable storage, adapters, transactions, migration, runtime
integration, deterministic replay, output invalidation, full re-evaluation, accounts, authentication, ownership,
verified email, ACV, PDF, Email Delivery, WS17, STG, release, or deployment. Full re-evaluation remains the safe
default after accepted material revision; targeted partial re-evaluation remains prohibited absent a separately
authorized deterministic dependency model.

**Future/deferred requirements:** prior accepted future requirements remain preserved under their existing canonical
records and timing. This synchronization does not redesign, activate, or implement them. Any requirement found only
in chat or a handover remains non-canonical until separately owner-decided and committed.

## P4-1 owner decisions (P4-1a / P4-1b split) — CONTRACT CANDIDATE / IMPLEMENTATION NOT AUTHORIZED

Owner decisions **D-P4-1-01 … D-P4-1-10** were accepted and recorded documentation-only via **G-P4-1A-DOC-01**,
together with the **P4-1a — Durable-Store Proof** increment-contract **CANDIDATE**. The canonical contract text is the
"P4-1a Increment Contract Candidate" section of `docs/governance/ACTIVE_INCREMENT_CONTRACT.md` (which governs; this
index does not duplicate it). Summary: P4-1a is a datastore-neutral durable-store proof using a stdlib SQLite
reference adapter — `IMPLEMENTATION NOT AUTHORIZED`; no code/test/database/dependency/`web/app.py` change; P4-1b,
P4-2, and Phase 5 remain separate and NOT AUTHORIZED.

| ID | Subject | Status | Impl. authority | Evidence |
|---|---|---|---|---|
| D-P4-1-01 | Split P4-1 into P4-1a (durable-store proof) + P4-1b (runtime integration), each separately gated | ACCEPTED | NONE | P4-1a contract candidate §3 |
| D-P4-1-02 | Datastore-neutral store abstraction + stdlib SQLite reference adapter (reference/MVP, not permanent production commitment; PostgreSQL/others possible via the abstraction) | ACCEPTED | NONE | §3, §7, §8 |
| D-P4-1-03 | No new runtime dependency; stdlib `sqlite3` only (no SQLAlchemy/psycopg/Supabase/provider/server) | ACCEPTED | NONE | §3 |
| D-P4-1-04 | Existing in-memory sessions not recoverable / not migrated; durability future-facing | ACCEPTED | NONE | §3 |
| D-P4-1-05 | Durability-safe UUID ids for new records; existing serialized ids preserved exactly on load | ACCEPTED | NONE | §3, §10 |
| D-P4-1-06 | Pre-account isolation via unguessable capability ids + project-scoped reads/writes; not authentication/ownership/authorization | ACCEPTED | NONE | §3, §12 |
| D-P4-1-07 | Exclude FDC-001 persistence, P4-2 (replay/output/stale-invalidation/full re-eval), Phase 5, providers, ACV, PDF, Email, production deployment | ACCEPTED | NONE | §3, §6, §20 |
| D-P4-1-08 | P4-1a must not modify `web/app.py`; runtime wiring is P4-1b | ACCEPTED | NONE | §3, §5 |
| D-P4-1-09 | Required proof set (durable create/round-trip/close-reopen/atomic append/rollback/append-only/isolation/stable-ids/provenance/unknown-version/malformed-ref/no-authoritative-readiness/no-replay-claim) | ACCEPTED | NONE | §9, §14, §15 |
| D-P4-1-10 | No additional governance-sync gate required before defining P4-1a; this gate records decisions + candidate | ACCEPTED | NONE | §3 |

No P4-1 decision grants implementation authority. **P4-1a implementation, P4-1b, P4-2, and Phase 5 remain NOT
AUTHORIZED.** Decision **D17** and the **AISR seven-owner model** are preserved. SQLite is recorded as a reference/MVP
adapter only, not a permanent production-datastore commitment.

## P4-1a durable-store proof — implementation authorization, merge, and formal closure

**Decision status:** ACCEPTED COMPLETED HISTORY / NO NEW IMPLEMENTATION AUTHORITY. The owner **separately and
explicitly authorized P4-1a implementation** (distinct from the PR #355 contract-candidate merge, which did not by
itself grant implementation authority). The implementation was executed, independently reviewed
(**B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**, 0 blocking), published, merged through **PR #356** (merge
`dfa082af0e6f9c09222608ca47d088dc7e2df6a8`; candidate `faf57300121a74d3493e88fc1e9a9631f6ab5815`, tree
`415aee66eb92c6c3fd6683c36deb70756af6cb36`), post-merge verified, and **FORMALLY CLOSED**.

| ID | Subject | Status | Impl. authority | Evidence |
|---|---|---|---|---|
| D-P4-1a-CLOSE-01 | P4-1a implementation authorization (separate from the PR #355 contract merge) | ACCEPTED | NONE beyond the bounded P4-1a increment | Owner implementation authorization; PR #356 merge |
| D-P4-1a-CLOSE-02 | P4-1a durable-store proof implementation | COMPLETE / MERGED / POST-MERGE VERIFIED / FORMALLY CLOSED | NONE | PR #356 (`dfa082af0e6f9c09222608ca47d088dc7e2df6a8`); paths `engine/record_store.py` + `tests/test_p4_1a_record_store.py`; 2 files / 426 insertions / 0 deletions; focused post-merge 11 passed; full suite 1681 passed / 1 skip / 1 xfail / exit 0 |
| D-P4-1a-CLOSE-03 | Current active implementation contract | NONE | NONE | `ACTIVE_INCREMENT_CONTRACT.md` synchronized status |
| D-P4-1a-CLOSE-04 | P4-1b / P4-2 / Phase 5 | NOT AUTHORIZED / NOT STARTED | NONE | Separate owner decision + contract required |
| D-P4-1a-CLOSE-05 | Product-truth boundary | RECORDED | NONE | P4-1a is a durable-store adapter capability only; no user-facing durable-save claim; runtime still temporary until P4-1b |

**Preserved non-blocking observations (recorded, not fixed):** durable supersession/contradiction mutation behaviour
decided in the future P4-1b contract; `project_ids()` must not be exposed through runtime/API/UI/user-facing surfaces;
`new_record_id()` exists but is not yet connected to runtime record creation (P4-1b); SQLite exception translation may
be considered during later runtime integration; minor test-connection hygiene remains non-blocking; SQLite remains a
reference/MVP adapter, not a permanent production-datastore commitment.

**Next eligible gate (owner consideration only):** P4-1b — READ-ONLY DISCOVERY AND CONTRACT-DEFINITION PREPARATION,
`ELIGIBLE FOR SEPARATE OWNER CONSIDERATION ONLY`. This synchronization authorizes nothing further. Decision **D17**
and the AISR seven-owner model are preserved; Phase 5 / WS17 / STG separation is preserved.

## P4-1b-1 owner decisions (G-P4-1B-1-DOC-01) — contract candidate, IMPLEMENTATION NOT AUTHORIZED

**Decision status:** ACCEPTED / RECORDED — NO IMPLEMENTATION AUTHORITY. The owner authorized a **documentation-only**
gate to record the P4-1b decisions and define the bounded **P4-1b-1 — Runtime Store Construction and Durable Project
Create/Load** contract candidate. **P4-1b READ-ONLY DISCOVERY is COMPLETE** (owner decision package delivered). Recording
these decisions and the candidate grants **no** implementation, code, test, database, dependency, or runtime authority;
P4-1b-1 implementation requires a **separate explicit owner authorization** after independent review and owner
acceptance. **P4-1b-2, P4-2, and Phase 5 remain NOT AUTHORIZED / NOT STARTED.** Recorded on live tip
`e4f9cd97e1b4329b98f1678412a6a36b9d7238bf` (Merge PR #357; always re-resolve from Git).

| ID | Subject | Decision | Impl. authority | Evidence / boundary |
|---|---|---|---|---|
| D-P4-1B-01 | Split P4-1b into P4-1b-1 (store construction + durable project create/load) + P4-1b-2 (accepted-input append + Keep/Refine), each separately gated | ACCEPTED | NONE | P4-1b discovery package §18; P4-1b-2 NOT authorized by this gate |
| D-P4-1B-02 | Runtime state model | ACCEPTED | NONE | SESSION_STORE = active in-memory cache; SQLite = durable mirror + cold-reload; rebuild via `load_contract(sid).to_state()` (the `sid` IS the durable `project_id`); readiness always re-derived; **no cache framework**; failed durability must not be presented as durable |
| D-P4-1B-03 | Store lifecycle | ACCEPTED | NONE | one app-scoped `SqliteRecordStore`, single-process MVP; multi-worker/pool/per-request/WAL/production-DB/provider deferred; SQLite = reference/MVP adapter |
| D-P4-1B-04 | Configuration | ACCEPTED | NONE | `INVENTORAI_DB_PATH`; safe local/test path; pytest `tmp_path`; **no repo-tracked `.db`/`.sqlite`/user-data file**; production fail-fast on missing/unusable/unsafe path; no new dependency; no uncontrolled `/tmp` user-content write (R6) |
| D-P4-1B-05 | Durability start policy | ACCEPTED | NONE | new projects only; existing lost in-memory sessions not recoverable/migratable/claimable; live-session promotion excluded from first increment |
| D-P4-1B-06 | Unified pre-account capability identifier (corrected — resolves BF-1) | ACCEPTED | NONE | **`sid` and durable `project_id` are the SAME `uuid4` value**; the route capability IS the durable project key; cold-load calls **`load_contract(sid)`**; **no separate `sid`→`project_id` mapping table, no `project_ids()` scan, no reversible mapping layer**; `project_ids()` remains prohibited from runtime/API/UI; temporary before Phase 5 (which may add account ownership + a separately governed external identifier); `new_record_id()` unused in P4-1b-1; **no change to `engine/record_store.py` or `engine/record_contract.py`** |
| D-P4-1B-07 | Project creation order | ACCEPTED | NONE | validate → **one `uuid4` used as both `sid` and `project_id`** (+ `idea_id`) → IdeaState → **durable create with `project_id = sid`** → **then** `SESSION_STORE[sid]` entry → redirect; on failure fail closed, one generic response, no live session, no user-content log |
| D-P4-1B-08 | Cold-load behaviour | ACCEPTED | NONE | request presents `sid`; SESSION_STORE empty → **`load_contract(sid)`** → P4-0 validation → `to_state()` → fresh `derive_readiness` → minimum runtime entry; no mapping lookup / `project_ids()` scan; transcript/`last_result` never restored as authoritative |
| D-P4-1B-09 | Error translation | ACCEPTED | NONE | translate at the web boundary; `record_store.py` unmodified by default; `ProjectNotFound`/malformed-contract/DB-unavailable/unknown-SQLite → generic; log class/operation/non-content id only; never log content/payloads/transcript |
| D-P4-1B-10 | Generic non-disclosure | ACCEPTED | NONE | one generic unavailable behaviour; never reveals non-existence, wrong capability, deletion, DB failure, malformed/unsupported contract |
| D-P4-1B-11 | Product-truth boundary | ACCEPTED / RECORDED | NONE | P4-1b-1 may prove durable **new-project** create/restart-survival/cold-load only; must NOT claim accepted-answer persistence, Keep/Refine durability, durable output, version history, session recovery, or full save — those require P4-1b-2 |

**BF-1 correction (independent-review verdict C — revise and re-review).** The original candidate `095e969` required
`sid` and `project_id` to be **separate** UUIDs while routes continued to receive only `sid` — with no durable mechanism
to resolve `project_id` from `sid` after restart, making cold-load infeasible within the authorized paths. Owner
correction (recorded above as the corrected D-P4-1B-06 / D-P4-1B-07 / D-P4-1B-08): **`sid` and `project_id` are the same
`uuid4` value**, so cold-load is simply `load_contract(sid)`. No mapping table, `project_ids()` scan, or reversible
mapping layer is introduced; `engine/record_store.py` and `engine/record_contract.py` are unchanged. The original
candidate `095e969` is **not amended** — this correction is a **new** candidate.

**Decision-trace clarification.** The P4-1b READ-ONLY DISCOVERY package identified **14** owner decisions. This P4-1b-1
contract records only the decisions required for P4-1b-1 (D-P4-1B-01 … D-P4-1B-11). Decisions concerning accepted-input
append, duplicate/retry & idempotency, supersession/contradiction mutation, write-path failure/compensation, and
Keep/Refine *durable* behaviour are **deferred to P4-1b-2 or later — not dropped**; they remain open.

No P4-1b-1 decision grants implementation authority. **P4-1b-1 implementation, P4-1b-2, P4-2, and Phase 5 remain NOT
AUTHORIZED.** Decision **D17** and the **AISR seven-owner model** are preserved. SQLite is recorded as a reference/MVP
adapter only, not a permanent production-datastore commitment. The live application still uses temporary in-memory
sessions and durably saves nothing until P4-1b implementation lands.

## P4-1b-1 contract amendment (G-P4-1B-1-AMEND-01) — threading & pytest DB isolation — DOC-ONLY

**Decision status:** ACCEPTED / RECORDED — NO IMPLEMENTATION AUTHORITY. Documentation-only amendment recorded after
the independent review of implementation candidate `1eced7d280449b9c0842355a1882a9d3b731a633` returned verdict
**C — REVISE AND RE-REVIEW** with two blocking findings: **B1** the shared single `sqlite3` connection is incompatible
with Flask's default threaded serving mode; **B2** governed tests outside the focused P4-1b-1 file write project
envelopes to the shared default database instead of pytest-managed temp paths. Recorded on live tip
`b22f82ef1f7d08ce802ecbc52d68706d358fadb5` (Merge PR #358). Candidate `1eced7d` is **preserved intact and NOT amended**;
the corrected implementation is a **separate** future authorization.

| ID | Subject | Decision | Impl. authority | Evidence / boundary |
|---|---|---|---|---|
| D-P4-1B-1-AMEND-01 | Explicit single-threaded MVP serving mode (B1) | ACCEPTED | NONE | Flask entry MUST use **`threaded=False`**; the app-scoped `sqlite3` connection must not cross request threads; **no `engine/record_store.py` change, no `check_same_thread=False`, no pool/per-thread/per-request model**; multi-thread/worker/production topology deferred; `threaded=False` is a bounded MVP decision, **not** a production-architecture claim |
| D-P4-1B-1-AMEND-02 | Governed pytest database isolation (B2) | ACCEPTED | NONE | authorizes **`tests/conftest.py`** ONLY for a minimal fixture: unique `tmp_path` `INVENTORAI_DB_PATH`; blocks writes to the shared dev DB; resets `SESSION_STORE`; **safely closes** the app-scoped store before reset; restores env/runtime after each test; no production behaviour; no weakened assertion; no repo-tracked DB; no `:memory:` for restart proofs; no `project_ids()`/transcript/answer exposure; no global store mock; not order-dependent |
| D-P4-1B-1-AMEND-03 | Threading regression proof | ACCEPTED | NONE | corrected impl must include a focused regression proving `threaded=False` is explicitly configured and cannot silently regress; may use a bounded helper/run-entry test; MUST NOT claim `test_client` alone proves cross-thread safety; must reproduce the reviewer scenario (or equivalent) showing requests no longer served through a shared SQLite connection across threads |
| D-P4-1B-1-AMEND-04 | Local-development DB boundary | ACCEPTED / RECORDED | NONE | dev default MAY stay under the system temp dir for non-test/non-production only; persists across local runs until OS/user cleanup; may hold durable project capability identifiers; **not** an account/ownership store; **pytest must never use it**; **P4-1b-2 must re-evaluate retention/permissions/deletion/user-content** before accepted-input persistence; production still requires explicit `INVENTORAI_DB_PATH` + fail-fast |

**Amended implementation paths (future correction).** Required/permitted: `web/app.py`;
`tests/test_p4_1b1_runtime_project_persistence.py`; **`tests/conftest.py`** (new, isolation fixture only).
Conditionally permitted: narrowly necessary existing test files, only to adopt the global isolated-DB fixture without
weakening assertions. Prohibited (unchanged): `engine/record_store.py`, `engine/record_contract.py`,
`engine/idea_state.py`, `engine/derived_readiness.py`, `requirements.txt`, `database/`, `schemas/`, `templates/`,
`static/`, CI/deployment. Any engine-store threading redesign requires a separate amendment.

**Correction-implementation boundary (NOT authorized here).** A separate future authorization may permit a replacement
candidate that keeps `1eced7d` as superseded evidence, starts from the then-live tip, sets `threaded=False`, adds the
`tests/conftest.py` fixture, closes/resets stores safely in tests, adds a threading/run-mode regression, re-runs
RED/GREEN + protected regressions + full suite, and undergoes a new independent review. **This amendment authorizes none
of it.** **P4-1b-1 correction implementation, P4-1b-2, P4-2, and Phase 5 remain NOT AUTHORIZED.** Decision **D17** and
the AISR seven-owner model are preserved.

## P4-1b-1 governance closure sync (G-P4-1B-1-CLOSURE-SYNC-01) — DOC-ONLY — CLOSURE CANDIDATE NOT YET MERGED

**Decision status:** ACCEPTED / RECORDED — NO IMPLEMENTATION AUTHORITY. Documentation-only closure sync recording the
merged, post-merge-verified, technically complete P4-1b-1 correction implementation and a procedural deviation.
Recorded on live tip `cbd0ce3046b24631c23e482dadd413aaa42dea05` (Merge PR #360). **P4-1b-1 governance closure is
PENDING** until this closure candidate is itself separately reviewed, published, PR-created, merged, and post-merge
verified.

| ID | Subject | Decision | Impl. authority | Evidence / boundary |
|---|---|---|---|---|
| D-P4-1B-1-CLOSE-01 | Independent-review verdict on correction candidate `3179cd5` | ACCEPTED — **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS** | NONE | Separate-session review of `3179cd5` |
| D-P4-1B-1-CLOSE-02 | Publication authorization for the exact candidate `3179cd5` | ACCEPTED (owner-issued) | NONE | Owner publication-only authorization; branch `fix/p4-1b1-threading-pytest-isolation` |
| D-P4-1B-1-CLOSE-03 | PR-creation authorization → **PR #360** | ACCEPTED (owner-issued) | NONE | Owner PR-creation-only authorization |
| D-P4-1B-1-CLOSE-04 | Factual merge of **PR #360** | RECORDED (factual event) | NONE | Merge `cbd0ce3046b24631c23e482dadd413aaa42dea05`; parents `ccb1f23` + `3179cd5`; exact reviewed candidate |
| D-P4-1B-1-CLOSE-05 | Post-merge verification acceptance | ACCEPTED | NONE | Ancestor check exit 0; exactly 3 authorized paths; 3 files / 497 insertions / 2 deletions; `threaded=False` present; pytest DB isolation present; no engine change; no accepted-input persistence; no P4-1b-2 behaviour |
| D-P4-1B-1-CLOSE-06 | Procedural deviation acknowledgment | RECORDED | NONE | **PR #360 merged before a separate explicit merge authorization was issued in the conversation** — a governance-process deviation; not a security incident or technical defect; must not be normalized as precedent; no retroactive merge-authorization claim is made |
| D-P4-1B-1-CLOSE-07 | P4-1b-1 technical completion | RECORDED | NONE | Implementation MERGED AND POST-MERGE VERIFIED; technical status COMPLETE |
| D-P4-1B-1-CLOSE-08 | Preservation of the ten non-blocking observations | RECORDED | NONE | See the closure section in `ACTIVE_INCREMENT_CONTRACT.md`; none deleted or marked resolved |
| D-P4-1B-1-CLOSE-09 | Later-gate exclusion | NOT AUTHORIZED / NOT STARTED | NONE | **P4-1b-2, P4-2, and Phase 5** remain unauthorized; separate owner decision + contract required |
| D-P4-1B-1-CLOSE-10 | This governance closure sync | ACCEPTED (owner later authorized) | NONE | Owner authorized G-P4-1B-1-CLOSURE-SYNC-01; **governance closure is PENDING until this candidate is itself merged and post-merge verified** |

**Truthfulness boundary.** No decision above states or implies that a separate merge authorization preceded the PR #360
merge; the owner **later** authorized this documentation closure sync. The superseded candidate `1eced7d` remains
preserved intact and unmerged. Decision **D17** and the AISR seven-owner model are preserved. The live application does
not durably persist accepted answers, outputs, or complete ideas (that remains P4-1b-2).
