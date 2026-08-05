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

## P4-1b-2a owner decisions — REV1 (G-P4-1B-2-DOC-01-REV1) — HISTORICAL PRE-IMPLEMENTATION contract-definition decisions (P4-1b-2a is now IMPLEMENTED / MERGED / CLOSED — see "P4-1b-2a implementation acceptance & closure" below)

**Decision status:** ACCEPTED / RECORDED — NO IMPLEMENTATION AUTHORITY. REV1 corrects the independent-review verdict
**C** blocking findings B1/B2/B3 against the original DOC-01 candidate `0e2a5cec24d71462eadbffa193e3467d40d506a0`
(**preserved intact, unmerged, NOT PUBLISHABLE, NOT amended**). A separately-claimed `518cfdfe…` candidate/bundle is
**not an established repository artifact**. Recorded on live tip `25dacb00295bcd3d34fd2cb5f789e9eae390ae11`.

**Base decisions carried forward (re-affirmed from the preserved original candidate, unchanged):** **D-P4-1B-2-01**
append-only accepted-input **event** ledger authoritative (event-versus-snapshot is one authoritative decision);
**-02** accepted input (2a) = an answered submission producing one `AssertionRecord`; **-03** persist→memory→acknowledge;
**-04** server-issued web-layer submission token (outside `engine/idea_state.py` absent a separate amendment); **-05**
duplicate retry = idempotent no-op (no second event/progression); **-06** stable record-id requirement; **-07** ledger
authoritative / readiness+progression+deliverable derived; **-08** restart guarantees ledger + fresh readiness only;
**-09** replay is P4-2; **-10** cold-load stays on `show_session`; **-11** Keep/Refine excluded; **-12** retention/
deletion + local-dev permission hardening deferred; **-13** P4-1b-2a/2b split (2b not authorized); **-14** truthful
product wording.

| ID | Subject | Decision | Impl. authority | Evidence / boundary |
|---|---|---|---|---|
| D-P4-1B-2-REV1-B1 | Mandatory token + affected existing tests | ACCEPTED | NONE | token mandatory for every answered submission; **no tokenless fallback**; enumerated ~21 answered-producing existing test files updated **only** to obtain/submit a real token; **no weakened assertion, no skipped behaviour, no conftest token auto-injection**; unidentified answered path → STOP — CONTRACT AMENDMENT REQUIRED |
| D-P4-1B-2-REV1-B2 | Token transport on every answered-producing form | ACCEPTED | NONE | covers the **main answer form** and the **criticality-correction free-text form** (no `action` → treated as `answered`) in `web/templates/session.html`; inventory/route-form regression proves **no answered-producing form bypasses** the token |
| D-P4-1B-2-REV1-B3 | Downstream `evt-*` semantic consequences | **RESOLVED — OPTION A SELECTED** (was CONTRACT AMENDMENT / OWNER DECISION REQUIRED) | NONE | `evt-*` ids materially change `engine/idea_development_outputs.py::_record_sort_key` (rec_N lead-0 precedence lost) and `engine/requirement_landscape.py` (derived requirement ids `req:assertion:<record_id>`, anchor/rationale, pair ordering); require mixed-id deterministic-output regressions; **must not be silently normalized**. **SUPERSEDED BY `D-P4-1B-2A-B3-01` (G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01):** owner SELECTED **Option A** — `record_id` stays `rec_N`, a **separate durable idempotency identity** is introduced, `evt-*` is **NOT** adopted as `record_id`, derived engines **unchanged**; Options (b)/(c) REJECTED |
| D-P4-1B-2-REV1-C1 | Web-layer staging | ACCEPTED | NONE | clone IdeaState → evaluate + build record on staged copy → set event id → durable append → publish staged state/transcript/last_result ONLY after durable success; on failure discard staged copy, live memory unchanged |
| D-P4-1B-2-REV1-C2 | Duplicate retry | ACCEPTED | NONE | no second event/progression/reconstructed last_result; no claim of reproducing prior response; no-op with `show_session` redirect when truthful else generic |
| D-P4-1B-2-REV1-C3 | IntegrityError handling | ACCEPTED | NONE | never auto-classify IntegrityError as duplicate; reload durable contract and confirm exact event id + same project + same logical content; **same token, different content fails closed**; unrelated integrity failures = generic store failures |
| D-P4-1B-2-REV1-C4 | Concurrency boundary | ACCEPTED | NONE | relies on existing `threaded=False` single-process/single-thread topology; store PK is the durable duplicate backstop; multi-thread/worker out of scope |
| D-P4-1B-2-REV1-C5 | Canonical token/event-id model | ACCEPTED — **AMENDED by `D-P4-1B-2A-B3-01`** (was "subject to B3") | NONE | cryptographically strong server-issued token; URL/form-safe bounded encoding; exact-match; hidden-form transport only; never in URLs/logs/user errors; token hashed not stored raw; `sid` included → project-bound. **AMENDED:** under Option A this token-derived, project-bound digest is the **SEPARATE durable idempotency identity**, **NOT** the engine `record_id` and **NOT** an `evt-*` `record_id`; `record_id` stays `rec_N`. Exact raw-vs-hash-vs-HMAC form + encoding/truncation remain an **implementation-gate decision** |
| D-P4-1B-2-REV1-C6 | Durable-success / memory-failure | ACCEPTED | NONE | durable ledger authoritative; invalidate temporary session entry; redirect safely; no continue-from-partial; no re-append; no replay/exact-resume claim |
| D-P4-1B-2-REV1-C7 | Pre-append scanning | ACCEPTED | NONE | full-ledger `load_contract(sid)` scan acceptable for MVP; recorded **O(n)**; no `project_ids()` exposure; direct-record lookup deferred |
| D-P4-1B-2-REV1-C8 | Mixed-id state | ACCEPTED | NONE | durable `evt-*` answered records may coexist with legacy/volatile `rec_N` non-answer records; protected regressions must cover this (feeds B3) |

**Boundary (HISTORICAL — as written at contract-definition time; now superseded).** These decisions authorized no
implementation and recorded that P4-1b-2a implementation was BLOCKED pending the B3 amendment/owner decision and a
separate explicit implementation authorization. **That state is superseded:** the B3 decision (Option A) was made, the
amendment merged, and P4-1b-2a is now **IMPLEMENTED / MERGED / VERIFIED / ACCEPTED / CLOSED** (owner verdict B; PR #365 —
see "P4-1b-2a implementation acceptance & closure" below). **P4-1b-2b, P4-2, Phase 5 remain NOT AUTHORIZED / NOT
STARTED.** The original `0e2a5ce` candidate (verdict C) and the superseded `1eced7d` remain preserved; all P4-1b-1 and
post-closure observations are preserved, not fixed. Decision **D17** and the AISR seven-owner model are preserved.

## P4-1b-2a B3 contract amendment (G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01) — OPTION A SELECTED — documentation-only, NO IMPLEMENTATION AUTHORITY

**Decision status:** ACCEPTED / RECORDED — NO IMPLEMENTATION AUTHORITY. Records the owner's binding B3 decision and
amends the merged P4-1b-2a REV1 contract to correctly incorporate it. Supersedes only the B3 `DETERMINATION`, the C5
event-id parenthetical, and the paths NOTE in REV1 (each flagged inline); the full REV1 candidate, `C1…C8`, verdict-C
history, and all prior observations are preserved. Recorded on the authoritative live tip resolved from Git.

| ID | Subject | Decision | Impl. authority | Evidence / boundary |
|---|---|---|---|---|
| D-P4-1B-2A-B3-01 | B3 resolution — **OPTION A SELECTED** (separate durable idempotency identity from the deterministic engine `record_id`) | ACCEPTED — **OPTION A** | NONE | engine `record_id` **stays `rec_N` (unchanged)** in value/format/creation-site/ordering/derived-identifier consumers; a **SEPARATE durable idempotency identity** (server-issued-token-derived) is stored **separately** and used **only** as the durable idempotency/duplicate backstop — **never** consumed by derived-output engines, **never** an `evt-*` `record_id`. **Option B REJECTED** (order-equivalent embedded event id enlarges deterministic-engine blast radius / risks silent drift); **Option C REJECTED** (deriving the idempotency key from `rec_N` conflates positional identity with request-idempotency and gives no unpredictable request-bound guarantee). Corrects any "web-layer-only / no-amendment" implication: Option A **requires a bounded, additive `engine/record_store.py` storage amendment** (evaluate: additive nullable column + partial/nullable UNIQUE `(project_id, idempotency_key)`, **or** sibling table — schema NOT locked here) |
| D-P4-1B-2A-B3-02 | Token/security & rejection contract | ACCEPTED | NONE | server-issued, cryptographically strong/unpredictable, bounded length, URL/form-safe; bound to project/session (`sid`) + the answered operation; single-use for acceptance; hidden-form transport only; **never** in URLs/logs/analytics/user errors; defined lifecycle/expiration; **raw-vs-hash-vs-HMAC storage form remains a REQUIRED implementation-gate decision**; **missing / malformed / expired / cross-session / cross-project → fail closed**, no durable append, no acceptance; **no tokenless fallback** |
| D-P4-1B-2A-B3-03 | Uniqueness & payload binding | ACCEPTED | NONE | durable uniqueness scoped to **(project + idempotency identity + operation)** bound to a **normalized accepted-request fingerprint**; same token + same request → return prior result (idempotent no-op, no second event/progression); same token + different request → **fail closed** (retains C3 confirm-by-reload, never auto-classify IntegrityError as duplicate); enforced **durably** at the storage layer, not web-layer only |
| D-P4-1B-2A-B3-04 | Storage amendment + migration/rollback | ACCEPTED | NONE | additive-only amendment to `engine/record_store.py` (no `rec_N` rewrite, no column drop/type change); pre-amendment + legacy/volatile `rec_N` rows carry **NULL** idempotency identity and stay valid (mixed-state, retains C8); a **real forward migration** against the live SQLite schema (idempotent on existing DBs) + a **defined rollback safe on populated DBs** (preserve `records`/`rec_N`; disable-and-ignore where physical drop is unsafe — **not** "just drop the column"); exact shape/constraint = implementation-gate decision |
| D-P4-1B-2A-B3-05 | RED contract, false-green prohibitions, logging | ACCEPTED | NONE | RED-first behavior-based: tokenless answered POST fails closed; inventory/route-form regression (both answered-producing forms — retains B2); same-token+same/different-request idempotency + fail-closed; **durable** uniqueness proven at storage layer; **mixed-id stability** — `rec_N` ordering / `req:assertion:rec_N` identifiers / pair ordering **unchanged** (Option A leaves derived engines untouched); **prohibited false-green:** no conftest token auto-injection, no weakened/skipped B1-test assertions, no `SESSION_STORE`/replay simulation of durability; token + raw user content **excluded from logs/errors/analytics/URLs** |
| D-P4-1B-2A-B3-06 | Exclusions (unchanged scope walls) | NONE — NOT AUTHORIZED | NONE | no change to `record_id`/`rec_N`; no `evt-*` as `record_id`; no P4-1b-2b, P4-2, Phase 5+; no FPC-01…04; no PDF/Email/STG/WS17/ACV; no event-bus / general-idempotency abstraction; no retention/deletion/permission hardening; multi-thread/multi-worker out of scope (C4 `threaded=False` retained). Documentation-only; grants no push/PR/merge/implementation; closing this gate activates nothing |

**Boundary (HISTORICAL PRE-IMPLEMENTATION BOUNDARY — SUPERSEDED).** **This paragraph is preserved as history and is no
longer current.** As written at amendment-preparation time it stated that no implementation authority was granted and
that P4-1b-2a implementation still required this amendment to be independently reviewed and merged, a separate explicit
implementation authorization, and RED-first behavior-based proof. **That state is superseded:** the B3 amendment was
independently reviewed and merged; **Option A was selected**; **P4-1b-2a implementation was separately authorized**;
the **REV1 implementation was independently accepted with verdict B**; **PR #365 was merged**; **post-merge verification
passed**; and the **owner accepted and CLOSED P4-1b-2a** — current closure evidence is merge
`77bd10cc55a731b18d4e35ea262b55342a9f847f`. **P4-1b-2b, P4-2, Phase 5+ remain NOT AUTHORIZED / NOT STARTED.** Decision
**D17** and the AISR seven-owner model, the original `0e2a5ce` candidate (verdict C), the superseded `1eced7d`, the full
REV1 candidate, and all prior observations are preserved.

## P4-1b-2a implementation acceptance & closure (G-P4-1B-2A-IMPLEMENTATION-01-REV1) — owner-accepted, MERGED & CLOSED

**Decision status:** ACCEPTED AND CLOSED — owner verdict **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**. Records the
owner's formal acceptance and closure of the P4-1b-2a implementation, merged into
`feature/atomic-json-session-persistence` via **PR #365** (merge commit `77bd10cc55a731b18d4e35ea262b55342a9f847f`,
two-parent merge of `4a31ece` + `0b5f757`, tree `c8808be`, candidate ancestry PASS). This is a documentation-only
closure record; it grants no new implementation authority.

| ID | Subject | Decision | Impl. authority | Evidence / boundary |
|---|---|---|---|---|
| D-P4-1B-2A-IMPL-01 | P4-1b-2a implementation accepted & closed | ACCEPTED — **verdict B**; **IMPLEMENTED / MERGED / VERIFIED / ACCEPTED / CLOSED** | NONE (closure) | OPTION A delivered: durable accepted-answer append persist-before-ack; additive nullable `idempotency_key` + partial uniqueness; server-issued token on **both** answered-producing forms (no tokenless fallback); `HMAC-SHA-256(INVENTORAI_SECRET_KEY, sid‖token)` ≥128-bit durable idempotency identity (raw token not stored/logged); same-token idempotent retry / different-content fail-closed; validation-error token retention; legacy `start_ilt002_*` routes durably backed (usable, unlinked). **`record_id` = `rec_N` preserved; separate durable idempotency identity; no deterministic-output engine changed; no `evt-*` engine identifier.** Merged scope **21 files / +1048 / −96**; disallowed paths **NONE**; source branch + bundle **PRESERVED** (bundle sha-256 `621b9546…a6a9b`); full suite **1726 passed, 1 skipped, 1 xfailed** |
| D-P4-1B-2A-IMPL-02 | Review lineage | RECORDED | NONE | superseded original candidate `b1eb91e` — first independent-review verdict **C — REVISE AND RE-REVIEW** (four blocking findings: **BF1** s04 tests reached token rejection not the empty-answer validation branch; **BF2** no direct real criticality-correction-form test; **BF3** token rejection only indirectly covered; **BF4** legacy `start_ilt002_*` routes lacked the durable envelope). Corrected REV1 candidate `0b5f757` — re-review verdict **B**, all four blockers independently verified CLOSED |
| D-P4-1B-2A-IMPL-03 | Accepted non-blocking observations | RECORDED | NONE | (1) RED not independently reproducible on the superseded candidate; reproduced on the authoritative parent; (2) the second focused legacy-route test module accepted as a justified corrective extension; (3) token rejection may write only bounded transient error state (no durable/progression/epistemic change); (4) CRLF-to-LF normalization not implemented (newline-only differences may fail closed); (5) durable-success / memory-publication-failure recovery **not claimed** (no reachable failure without artificial injection); (6) this governance synchronization records the post-merge history and closure; (7) `Optional[str]` typing and the current cold-load domain guard remain non-blocking observations |
| D-P4-1B-2A-IMPL-04 | Later-scope exclusion (unchanged) | NONE — NOT AUTHORIZED | NONE | **P4-1b-2b, P4-2, Phase 5+, and every FPC (FPC-01…FPC-04) remain NOT AUTHORIZED / NOT STARTED**; closing P4-1b-2a activates nothing downstream. Decision **D17** and the AISR seven-owner model preserved. **[SUPERSEDED for P4-1b-2b only, as of the PR #365 boundary: P4-1b-2b was subsequently discovered, authorized (Option A), implemented, independently reviewed (verdict B), merged (PR #367, `1c9dff7`), post-merge verified, owner accepted, and FORMALLY CLOSED — see "P4-1b-2b … discovery, implementation acceptance & closure" below. P4-2, Phase 5+, and every FPC remain NOT AUTHORIZED / NOT STARTED.]** |

**Boundary.** Closure grants no downstream authorization. All prior decisions, candidates, verdicts, and observations
are preserved; no history is rewritten.

### Governance-synchronization review lineage (documentation-only; chronology of the closure record itself)

The P4-1b-2a **implementation** closure above is final. The **documentation-only governance synchronization** that
records it went through owner-gated revision (no governance-sync candidate was published, merged, or accepted):

| ID | Subject | Owner decision | Impl. authority | Evidence / boundary |
|---|---|---|---|---|
| D-P4-1B-2A-GSYNC-01 | First governance-sync candidate `571229e` | **C — REVISE AND RE-REVIEW** (owner reclassified from the independent review's **B**) | NONE | reason: a material present-tense contradiction remained in `ACTIVE_INCREMENT_CONTRACT.md` (stale "NOT YET MERGED / IMPLEMENTATION NOT AUTHORIZED / P4-1b-2a NOT STARTED"). **Not published / not merged / not accepted.** |
| D-P4-1B-2A-GSYNC-02 | REV1 governance-sync candidate `1575c80` | **OWNER VERDICT: C — REVISE AND RE-REVIEW** / NOT ACCEPTED FOR PUBLICATION (independent review reported **B**; owner reclassified to **C**) | NONE | reason: `D-FPC-MAP-10` still carried a current-readable historical blocker and the governance-sync review lineage was under-recorded. **Not published / not merged / not accepted.** |
| D-P4-1B-2A-GSYNC-03 | REV2 governance-sync candidate `a92f75c` | **C — REVISE AND RE-REVIEW** (independent review returned C; owner accepted) | NONE | corrected D-FPC-MAP-10 ambiguity + recorded review lineage + refreshed the stale pointer/durable-persistence wording, but residual current-readable contradictions remained (FPC pointer, current capability surfaces, Post-PR #353 section, B3 boundary paragraph). **Not published / not merged / not accepted.** |
| D-P4-1B-2A-GSYNC-04 | REV3 governance-sync candidate `c2bb542` | **C — REVISE AND RE-REVIEW** (independent review returned C; owner accepted) | NONE | closed the four prior residual contradictions, but BF5 remained: `CURRENT_PROJECT_STATE.md` still named REV2 (not REV3) as the candidate pending review and omitted the updated GSYNC pointer range. **Not published / not merged / not accepted.** |
| D-P4-1B-2A-GSYNC-05 | REV4 governance-sync candidate (this candidate) | PENDING INDEPENDENT REVIEW | NONE | corrects BF5: current-state now names REV4 as the pending candidate and records the full REV1→REV4 lineage (REV2 and REV3 both verdict C); GSYNC pointer range updated. Documentation-only; grants no downstream authorization |

**Boundary.** These are chronology/decision records for the closure documentation only. **P4-1b-2a remains IMPLEMENTED /
MERGED / POST-MERGE VERIFIED / OWNER ACCEPTED / CLOSED (PR #365, merge `77bd10c`).** No governance-sync candidate is
claimed as published, merged, or accepted. **P4-2, Phase 5, and every FPC remain NOT AUTHORIZED / NOT STARTED.**
*(Historical note, as of the PR #365 boundary: this section's earlier "P4-1b-2b … remain NOT AUTHORIZED / NOT STARTED"
wording is **superseded** — P4-1b-2b is now IMPLEMENTED / MERGED / VERIFIED / ACCEPTED / FORMALLY CLOSED (PR #367,
`1c9dff7`); see "P4-1b-2b … discovery, implementation acceptance & closure" below.)*

## Future Product Capability classifications (G-FPC-MAP-01) — documentation-only, NON-AUTHORIZING

**Decision status:** ACCEPTED / RECORDED — NO IMPLEMENTATION AUTHORITY. Records the owner-accepted classifications and
boundaries for FPC-01…FPC-04 following the read-only assessment G-FPC-OVERLAP-01. Non-activating; consumes/cross-
references existing canonical models (Capability Enrichment Register, workstream/phase records); creates no parallel
model, no standalone document, and no `ACTIVE_INCREMENT_CONTRACT.md` change. Full map in `ACTIVE_EXECUTION_ROADMAP.md`
(Future Product Capability Integration Map). Recorded on live tip `7d489614b5535244f1116304db1c46c8639e836f`.

| ID | Subject | Decision | Impl. authority | Evidence / boundary |
|---|---|---|---|---|
| D-FPC-MAP-01 | FPC-01 Idea Validation Roadmap classification | ACCEPTED — **PARTIALLY CANONICAL / PARTIALLY DOCUMENTED** | NONE | missing = unified evidence-closure **roadmap UX + action-status only** (UX orchestration); consumes WS7 plan, CAP-04/09/11, WS12, merged evidence/provenance, P4-2 re-eval; **no** new gap/evidence/provenance/action-pack/validation-engine model |
| D-FPC-MAP-02 | FPC-02 Revision Difference & Stale-Output | ACCEPTED — **CANONICAL PRODUCT REQUIREMENT, already owned by P4-2 + D17 + Phase-3C; NOT a new capability; implementation contract & execution NOT YET AUTHORIZED / NOT complete** | NONE | missing = a **P4-2 implementation contract** (durable revision/output relationships, stale-output invalidation, updated output, full replay) + the accepted in-session **"What changed?"** UX increment; targeted re-eval prohibited pending a dependency model |
| D-FPC-MAP-03 | FPC-03 Decision & Assumption Ledger | ACCEPTED — **PARTIALLY CANONICAL**; no-rebuild boundary | NONE | missing = unified **Decision-and-Assumption UX** + complete **Decision Ledger** (owner, date, alternatives, rationale, evidence, affected gaps/outputs, retirement/supersession, source class); consumes CAP-05/07/08/10 + merged provenance/contradiction/supersession; **no** rebuild of provenance/assumption/contradiction/supersession/evidence-classification; identity/ownership/audit = **Phase 5** |
| D-FPC-MAP-04 | FPC-04 Specialist Handoff — **04A Assembly / 04B Delivery separation** | ACCEPTED — **PARTIALLY DOCUMENTED (assembly on existing foundations)** | NONE | **04A** missing = internal in-app **preview** + **durable handoff-package record** assembling current non-stale snapshot/evidence/gaps/contradictions/specialist-category/bounded questions. **04B (owned elsewhere, not bundled):** sharing/access/recipient/permissions/revocation = **Phase 5**; **PDF** = OD-U/Phase-4; **Email** = OD-U/Phase-5; specialist content = **STG/D13**; response ingestion = **AISR/STG**; stale-output awareness = **P4-2**. No new sharing/PDF/Email subsystem or duplicate specialist-category/STG workflow |
| D-FPC-MAP-05 | Governing phase/workstream assignments | ACCEPTED | NONE | as recorded in the roadmap map (P4-2; Phase 5; STG/D13; OD-U PDF/Email; Phase-3 UX lineage; Phase-4/P4 durable foundations) |
| D-FPC-MAP-06 | No-parallel-model duplication ruling | ACCEPTED | NONE | for every overlap (Phase 4/P4-0/P4-1a foundations, P4-2, CAP-04/05/07/08/09/10/11, WS12, D17, Phase-3C revision UX, D13 specialist-category, CAP-01/STG, OD-U PDF/Email, Phase-5): **DO NOT CREATE A NEW PARALLEL MODEL — EXTEND OR CONSUME THE EXISTING CANONICAL MODEL** |
| D-FPC-MAP-07 | Canonicalization Method D | ACCEPTED | NONE | roadmap integration map + owner-register rows + one current-state pointer; **no standalone document; no active-contract change; Capability Enrichment Register unchanged (cross-reference only)** |
| D-FPC-MAP-08 | Reminder policy | ACCEPTED | NONE | governance is source of truth; handovers carry a concise "Preserved Future Product Capabilities" section that **references** the map/register (no full re-listing); reminders only when contextually relevant; no long FPC reminder on every response; no reminder overrides merged governance; existing ACV/PDF/Email/sponsor-theme/Domain-Registry governance referenced, not re-listed |
| D-FPC-MAP-09 | FPC implementation authorization | NONE — **NOT AUTHORIZED / NOT STARTED** | NONE | FPC-01, FPC-02, FPC-03, FPC-04A, FPC-04B and every referenced future gate remain unauthorized; future-gate references are eligibility only |
| D-FPC-MAP-10 | Non-disturbance of active blocker | RECORDED — **HISTORICAL / SUPERSEDED** | NONE | G-FPC-MAP-01 does **not** disturb P4-1b-2a / B3 (CONTRACT AMENDMENT / OWNER DECISION REQUIRED remains the active technical blocker; Option A/B/C unselected); P4-1b-2b/P4-2/Phase 5 remain NOT AUTHORIZED / NOT STARTED. **[HISTORICAL / SUPERSEDED — this row records the pre-B3 state at G-FPC-MAP-01 authoring; the statement that a contract amendment/owner decision remained the active technical blocker with Option A/B/C unselected is NO LONGER CURRENT: Option A was subsequently selected, the B3 amendment was merged, and P4-1b-2a was IMPLEMENTED through REV1, independently accepted with verdict B, merged through PR #365, post-merge verified, owner accepted, and CLOSED. Current authoritative closure evidence = merge `77bd10cc55a731b18d4e35ea262b55342a9f847f`. D-FPC-MAP-10 must NOT be read as an active blocker. FPC-01…FPC-04A/04B remain in their approved future sequencing — NOT AUTHORIZED / NOT STARTED.]** |

**Boundary.** No FPC is authorized, active, started, or implemented; no specialist approval, AI authority, PDF/Email
delivery availability, saved-project, or full-resume capability is implied. Decision **D17** and the AISR seven-owner
model are preserved; all prior governance history and observations are preserved.

## P4-1b-2b — Read-Only Accepted-Answer Evidence Reconstruction: discovery, implementation acceptance & closure (G-P4-1B-2B-DISCOVERY-CONTRACT-01 + G-P4-1B-2B-IMPLEMENTATION-01) — owner-accepted, MERGED & CLOSED

**Decision status:** ACCEPTED AND CLOSED — owner verdict **B — ACCEPT WITH BINDING CONTRACT REFINEMENTS** (refinements
satisfied). Records the read-only discovery gate, the separate implementation authorization (Option A), the
independent review, the merge through **PR #367** (merge commit `1c9dff7962a428cfd32ab577dbbbb84ce21909b3`, two-parent
merge of `7d8895122235a4da25a7f4d9d0d4d5e4bab20c6b` (base) + `945f4a36a6a6eef5bcab1ea55e30ce1dfa468820` (reviewed
candidate), tree `bff45ada35e8d3bb606bcf4e6bd80e3df33d449d` — equal to the candidate tree; candidate ancestry PASS),
post-merge verification, owner acceptance, and formal closure. This is a documentation-only closure record; it grants no
new implementation authority. Recorded on the authoritative live tip resolved from Git (`1c9dff7`).

**Supersession clause.** This section supersedes earlier register wording **only where that wording states that
P4-1b-2b was not authorized, not started, pending, a candidate, or awaiting review/publication** (e.g. the historical
"P4-1b-2b … remain NOT AUTHORIZED / NOT STARTED" statements in the P4-1b-2a REV1 boundary, the B3 amendment exclusions,
the P4-1b-2a implementation-closure and governance-sync-lineage sections, and the D-FPC-MAP-10 row). Those statements
were accurate as of their PR #365-era authoring and **remain historical context, not current status**. Current status:
**P4-1b-2b is IMPLEMENTED / MERGED / POST-MERGE VERIFIED / OWNER ACCEPTED / FORMALLY CLOSED.** No prior history is
rewritten.

| ID | Subject | Decision | Impl. authority | Evidence / boundary |
|---|---|---|---|---|
| D-P4-1B-2B-DISC-01 | Read-only discovery & contract-definition preparation (G-P4-1B-2B-DISCOVERY-CONTRACT-01) | ACCEPTED / RECORDED | NONE | Discovery package delivered; recommended **Option A** — a bounded, read-only reconstruction of durably persisted accepted-answer evidence reusing the project-scoped `load_contract` read; no mutation, no session resume, no replay. Discovery authorized nothing further |
| D-P4-1B-2B-IMPL-01 | P4-1b-2b implementation authorized (Option A) & accepted, closed | ACCEPTED — **verdict B**; **IMPLEMENTED / MERGED / VERIFIED / ACCEPTED / CLOSED** | NONE (closure) | Separate explicit implementation authorization **G-P4-1B-2B-IMPLEMENTATION-01** (Option A; binding API contract; two permitted paths; required RED set; RED→GREEN). Delivered: read-only `SqliteRecordStore.load_accepted_answer_evidence(project_id) -> tuple` returning an **immutable `tuple`** of `answered`-disposition `AssertionRecord`s in persisted (`seq`) order via `load_contract`; `record_id` preserved as `rec_N` (non-contiguous expected/valid); unknown/absent `sid` → `()`; malformed/unsupported-version/invalid-reference/cyclic → canonical `ContractError` propagates (fail closed, no partial evidence); legacy NULL-`idempotency_key` rows load unchanged. Merged scope **2 files / +367 / −0** (`engine/record_store.py` +38; `tests/test_p4_1b2b_accepted_answer_evidence.py` +329); disallowed paths **NONE**; source branch `feat/p4-1b2b-accepted-answer-evidence` + bundle **PRESERVED** (`p4_1b2b_impl_945f4a3.bundle`, SHA-256 `b04f07688804d27f0cafd7c1e7cc7136da705c3e14efc275e2587ecfef4d365f`); tests focused **15** / P4-1b-2a regression **60** / protected **227** / full **1741 passed, 1 skipped, 1 xfailed** |
| D-P4-1B-2B-IMPL-02 | Capability boundary — explicit "does NOT provide" | RECORDED | NONE | P4-1b-2b is **evidence reconstruction only**. It does **NOT** provide: a resumable session / "resume exactly where you left off"; a reconstructed next question, gaps, maturity, domain/path, transcript, `last_result`, or progression; full deterministic replay or durable output (**P4-2**); accounts/ownership/authorization (**Phase 5**); any mutation/append/repair/state-advance; any UI, route, or runtime surface; any change to `record_id`/`rec_N`, the deterministic-output engines, or the P4-1b-2a durable idempotency identity |
| D-P4-1B-2B-IMPL-03 | Accepted non-blocking observations | RECORDED | NONE | (1) **Governance-tree authorization lag** — the P4-1b-2b gates were reviewed/merged/verified before the committed governance tree recorded them; this synchronization (G-P4-1B-2B-GOVERNANCE-SYNC-01) closes the lag; not a defect. (2) **Protected-regression set composition (226 vs 227)** — differs by one from a neighbouring gate's count purely by which modules are enumerated as "protected"; both green; bookkeeping only. (3) **`seq` ordering confirmed by manual experiment** and by reuse of the proven `load_contract` `ORDER BY seq ASC` read, rather than an isolated in-suite ordering-only assertion; behaviour correct. (4) **Plain-`tuple` return + single `SESSION_STORE`-unchanged assertion** — stylistic/polish only. Honest value note: net-new capability is modest (exposes, read-only, evidence P4-1b-2a already persists); no reachable memory-publication-failure recovery without artificial injection; correct and within scope |
| D-P4-1B-2B-IMPL-04 | Later-scope exclusion (unchanged) | NONE — NOT AUTHORIZED | NONE | **P4-2, Phase 5+, WS17, STG, and every FPC (FPC-01…FPC-04) remain NOT AUTHORIZED / NOT STARTED**; closing P4-1b-2b activates nothing downstream. Decision **D17** and the AISR seven-owner model preserved |

**Boundary.** Closure grants no downstream authorization. All prior decisions, candidates, verdicts, and observations are
preserved; no history is rewritten. **P4-1b-2b is IMPLEMENTED / MERGED / POST-MERGE VERIFIED / OWNER ACCEPTED / FORMALLY
CLOSED** (PR #367, merge `1c9dff7`). **P4-2, Phase 5, and every FPC remain NOT AUTHORIZED / NOT STARTED.**
