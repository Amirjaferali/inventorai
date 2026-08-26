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

## P4-2 Level-1 — Deterministic Read-Only Reconstructed Review State: discovery, implementation acceptance & closure + PHASE 4 FORMAL CLOSURE (G-P4-2-DISCOVERY-CONTRACT-01 + G-P4-2-LEVEL1-IMPLEMENTATION-01) — owner-accepted, MERGED & CLOSED

**Decision status:** ACCEPTED AND CLOSED — owner verdict **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**. Records the
read-only discovery gate, the separate implementation authorization (Option A / Level 1), the independent review, the
merge through **PR #369** (merge commit `276e89681e6008ec859383771b845833321b5552`, two-parent merge of
`2cde5868249f5e2b135b13fb33adff5dd5e4a816` (base) + `e66ae3a7d95994b32dd590000b1bd1e95c499c64` (reviewed candidate),
tree `1f6babf08ca6aae04677739d6c945581ed90db56` — equal to the candidate tree; candidate ancestry PASS), post-merge
verification, owner acceptance, formal closure, and the **formal closure of Phase 4**. Documentation-only; grants no new
implementation authority. Recorded on the authoritative live tip resolved from Git (`276e896`).

**Supersession clause.** This section supersedes earlier register wording **only where that wording states that P4-2 was
not authorized, not started, pending, a candidate, or awaiting review/publication** (e.g. the historical "P4-2 … remain
NOT AUTHORIZED / NOT STARTED" statements in the P4-1b-2a/2b closure and FPC-map sections, and "Phase 4 implementation:
NOT AUTHORIZED" in the Phase-4 entry rows). Those statements were accurate as of their PR #365/#367-era authoring and
**remain historical context, not current status**. Current status: **P4-2 Level-1 is IMPLEMENTED / MERGED / POST-MERGE
VERIFIED / OWNER ACCEPTED / FORMALLY CLOSED, and Phase 4 is FORMALLY CLOSED.** No prior history is rewritten.

| ID | Subject | Decision | Impl. authority | Evidence / boundary |
|---|---|---|---|---|
| D-P4-2-DISC-01 | Read-only discovery & contract definition (G-P4-2-DISCOVERY-CONTRACT-01) | ACCEPTED / RECORDED | NONE | Discovery found current durable records insufficient for any continuation beyond Level 0 (seed idea, confirmed domain, path, engine version not persisted). Recommended **Option A** — deterministic read-only reconstruction to **Level 1** (read-only reconstructed review state) via canonical engine replay, additively persisting the missing inputs. Discovery authorized nothing further |
| D-P4-2-L1-IMPL-01 | P4-2 Level-1 implementation authorized (Option A / Level 1) & accepted, closed | ACCEPTED — **verdict B**; **IMPLEMENTED / MERGED / VERIFIED / ACCEPTED / CLOSED** | NONE (closure) | Separate explicit implementation authorization **G-P4-2-LEVEL1-IMPLEMENTATION-01** (Option A / Level 1; Path-N only; additive nullable envelope inputs; version constant; bounded replay limit; four permitted paths; RED→GREEN). Delivered: read-only `engine.session_reconstruction.reconstruct_review_state(store, sid)` — persists `seed_idea_text`/`confirmed_domain`/`recon_path`/`engine_contract_version` at creation; loads accepted-answer evidence in `seq` order; builds a fresh canonical `IdeaState`; replays seed then answer contents through the **unchanged** `progression_loop.run_iteration`; returns an **immutable** `ReconstructedReviewState`. Version `p4-2-level1-recon-v1`; replay limit **500**. Merged scope **4 files / +795 / −13** (`engine/record_store.py`, `engine/session_reconstruction.py`, `web/app.py`, `tests/test_p4_2_session_reconstruction.py`); disallowed paths **NONE**; source branch `feat/p4-2-level1-readonly-reconstruction` + bundle **PRESERVED** (`p4_2_level1_e66ae3a.bundle`, SHA-256 `d1aae8f16239a8ffe2088ec9a8e197b4dc6b329f73d760f8f6cab7213dec9b25`); tests focused **28 passed** / full **1769 passed, 1 skipped, 1 xfailed** |
| D-P4-2-L1-IMPL-02 | Capability boundary — explicit "does NOT provide" | RECORDED | NONE | P4-2 Level-1 is **read-only review reconstruction only**. It does **NOT** provide: a resumed session; writable continuation; `SESSION_STORE` rehydration; answer submission from reconstructed state; full runtime restoration; durable version history / branching / rollback; account ownership (**Phase 5**); **FPC-02** stale-output implementation. Fail-closed to Level-0 on legacy/missing-metadata/unsupported-path/version-mismatch (no AI, no network); malformed history raises canonical `ContractError`; replay boundary+1 fails closed; **no DB / `SESSION_STORE` mutation, no UI, no prior-output validity claim**; the seed idea is never logged or duplicated into an `AssertionRecord` |
| D-P4-2-L1-IMPL-03 | Accepted non-blocking observations | RECORDED | NONE | (1) SQLite column `recon_path` maps to the logical field `path`; (2) the literal replay boundary 500/501 was independently verified; (3) a genuine pre-change-schema migration was independently verified but is not a committed focused test; (4) returned `AssertionRecord` elements are mutable local deserialized copies but cannot mutate durable storage or live sessions. Recorded, not reopened |
| D-P4-2-L1-IMPL-04 | Later-scope exclusion (unchanged) | NONE — NOT AUTHORIZED | NONE | **Writable continuation, P4-2 beyond Level-1 read-only, Phase 5+, WS17, STG, and every FPC (FPC-01…FPC-04) remain NOT AUTHORIZED / NOT STARTED**; closing P4-2 Level-1 activates nothing downstream. Decision **D17** and the AISR seven-owner model preserved |
| D-PHASE4-CLOSE-01 | Phase 4 (Durable Data and Evidence Foundation) formal closure | **FORMALLY CLOSED** within the implemented boundary | NONE | Phase 4 delivered: durable accepted-answer append (P4-1b-2a); a separate durable idempotency identity (P4-1b-2a); accepted-answer evidence loading (P4-1b-2b); deterministic Level-1 read-only reconstruction (P4-2); additive legacy-safe project reconstruction metadata; truthful wording with **no false session-resume claim**. Phase 4 did **NOT** deliver writable continuation, accounts / authentication / ownership, version history / branching / rollback, output email / download, ACV, an AI Coach, or any FPC implementation. **NEXT ELIGIBLE PHASE: Phase 5 — Accounts / Authentication / Ownership / Verified Email Foundations — NOT STARTED / NOT AUTHORIZED by this gate** |

**Boundary.** Closure grants no downstream authorization. All prior decisions, candidates, verdicts, and observations are
preserved; no history is rewritten. **P4-2 Level-1 is IMPLEMENTED / MERGED / POST-MERGE VERIFIED / OWNER ACCEPTED /
FORMALLY CLOSED (PR #369, merge `276e896`); Phase 4 is FORMALLY CLOSED.** **Writable continuation, Phase 5, and every FPC
remain NOT AUTHORIZED / NOT STARTED.**

## Draft Level 2 — Same-Device Unsubmitted-Text Recovery — contract-definition decisions (G-DRAFT-L2-LOCAL-CONTINUITY-CONTRACT-01) — CONTRACT CANDIDATE / IMPLEMENTATION NOT AUTHORIZED

**Decision status:** ACCEPTED / RECORDED — NO IMPLEMENTATION AUTHORITY. Documentation-only gate recording the accepted
discovery outcome and defining the bounded **Draft Level 2 — Same-Device Unsubmitted-Text Recovery** increment-contract
**CANDIDATE**. The full contract text is the "Draft Level 2 …" section of `ACTIVE_INCREMENT_CONTRACT.md` (which governs;
this index does not duplicate it). Recording these decisions and the candidate grants **no** implementation,
client-JavaScript, `localStorage`/IndexedDB, template, `web/app.py`, schema, migration, dependency, account, or Phase 5
authority. Recorded on the authoritative live tip resolved from Git (`ca19390`).

**Accepted discovery facts (G-P5-DISCOVERY-AND-DRAFT-CONTINUITY-ASSESSMENT-01, COMPLETED / ACCEPTED):** overlap **D — NOT
FOUND**; current **Draft Level 0**; current unsent-text protection **NONE**; selected **Option B**; first capability
**Draft Level 2 — Same-Device Unsubmitted-Text Recovery**; later capability **Draft Level 3 — Account-Linked Server Draft
Recovery after Phase 5**; sequence **Draft Level 2 → Phase 5 identity foundation → Draft Level 3**.

| ID | Subject | Decision | Impl. authority | Evidence / boundary |
|---|---|---|---|---|
| D-DRAFT-L2-01 | Capability & canonical name | ACCEPTED | NONE | **Same-Device Unsubmitted-Text Recovery** (short: **Local Draft Recovery**); stores a literal copy of user-typed text; **never** authors/rewrites/accepts/submits, creates an `AssertionRecord`, runs evaluation, closes a gap, changes maturity, or alters outputs. "autosave" avoided standalone (existing answer-auto-authoring prohibition preserved) |
| D-DRAFT-L2-02 | First-increment surfaces | ACCEPTED | NONE | REQUIRED = seed idea (`index.html`) + main answer (`session.html`); CONDITIONAL = criticality-correction free-text; DEFERRED = clarify rationale, success-criteria; PROHIBITED = FDC-001 Decision Workspace / legacy-unlinked |
| D-DRAFT-L2-03 | Storage mechanism | ACCEPTED | NONE | **`localStorage`** (Lean; small text; ≤64 KB/draft cap); no IndexedDB / service worker / third-party lib; failure/quota/private-mode → **fail closed to Level 0**, never blocks; **no client-encryption claim** |
| D-DRAFT-L2-04 | Draft identity key | ACCEPTED | NONE | `inventorai:draft:v1:<scope>:<field>:<context-id>:<context-version>`; scope = `sid` (session) or `__seed__` (pre-`/start`); raw text never in the key; stale/wrong context never restored; no account ownership |
| D-DRAFT-L2-05 | Save behavior | ACCEPTED | NONE | debounced ~800 ms + `pagehide`/`visibilitychange` flush; `beforeunload` avoided as primary; **no network** for a Level-2 save; not per-keystroke |
| D-DRAFT-L2-06 | Recovery behavior | ACCEPTED | NONE | **explicit** low-emphasis non-modal prompt; Restore / Discard / continue-without; **never** silently overwrite newer text; stale/mismatched/expired/malformed rejected; bilingual EN/AR + RTL; last-saved time shown |
| D-DRAFT-L2-07 | Product-truth messages | ACCEPTED | NONE | truthful device-only wording; **must NOT** claim account/server/other-device/permanent save; "Draft saved on this device" only after a save event; low-emphasis |
| D-DRAFT-L2-08 | Successful-submit cleanup | ACCEPTED | NONE | clear the matching draft **only** on a truthful accepted signal (minimal `web/app.py` render flag); never clear on validation/token/CSRF/store-unavailable/timeout/ambiguous/error; **existing idempotency preserved**; no second submission/retry model; ambiguous case retains the draft, idempotency prevents duplicates |
| D-DRAFT-L2-09 | Privacy | ACCEPTED | NONE | disclosure at/before first save via the **existing Data & Session Notice** + one scoped sentence (no new privacy system); shared-device/profile/sync/private-mode risks; explicit discard; expiry; cleanup; **no raw draft text** in logs/analytics/exceptions/URLs/history/telemetry |
| D-DRAFT-L2-10 | Retention / TTL | ACCEPTED (recommendation) | NONE | options 24 h / **7 days (RECOMMENDED)** / 30 days; lazy cleanup on load + on submit + explicit discard; **TTL RECOMMENDED contract-fixed at 7 days but REQUIRES OWNER CONFIRMATION at the implementation-authorization gate**; not runtime-configurable in the first increment |
| D-DRAFT-L2-11 | Failure / fallback & multi-tab | ACCEPTED | NONE | every failure fails closed to Level 0; a draft failure never blocks submission; multi-tab = **last-write-wins by timestamp** + `storage`-event awareness note; no cross-tab lock / no conflict merge / no multi-device (Level 4 excluded) |
| D-DRAFT-L2-12 | Accessibility & security | ACCEPTED | NONE | EN/AR + RTL, keyboard, `aria-live` polite, non-color-only, accessible controls, non-modal, focus handling; DOM via `.value`/`textContent` only (no `innerHTML`), no third-party scripts, CSP-compatible first-party file, size cap, malformed ignored, no ownership/authz from local data, restored text is untrusted client input (server validation authoritative) |
| D-DRAFT-L2-13 | Paths, schema, testing, structure | ACCEPTED | NONE | REQUIRED future paths = `index.html`, `session.html`, one new `web/static/js/` file, focused tests; CONDITIONAL = minimal `web/app.py` render flag + Data-&-Session disclosure + static-folder wiring; PROHIBITED = the 8 engine files + schema/migration + server draft store + auth/CI; **schema/migration NONE**; testing = **pytest + Playwright (Python) / headless Chromium** (test-only `playwright` dep justified; pre-installed browser); **ONE implementation increment** |
| D-DRAFT-L2-14 | Authorization boundary | NONE — NOT AUTHORIZED | NONE | Draft Level 2 is local-only; **no** cross-device/server/accounts/writable-continuation/accepted-answer-change; this gate authorizes **no** implementation. **Phase 5 is the next step immediately after this bounded increment — NOT STARTED / NOT AUTHORIZED.** Server Draft Level 3, writable continuation, and every FPC remain NOT AUTHORIZED / NOT STARTED |

**Boundary.** No decision above grants implementation authority. Draft Level 2 implementation requires a **separate
explicit owner authorization** after independent review of this candidate. Decision **D17** and the AISR seven-owner
model are preserved; Phase 4 remains FORMALLY CLOSED; P4-2 Level-1 remains CLOSED.

## Draft Level 2 — Same-Device Unsubmitted-Text Recovery: implementation acceptance & closure (G-DRAFT-L2-LOCAL-CONTINUITY-IMPLEMENTATION-01 + REMEDIATION-01) — owner-accepted, MERGED & CLOSED

**Decision status:** ACCEPTED AND CLOSED — focused re-review verdict **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**.
Records the implementation, the independent review (verdict **C — REJECT**), the remediation of the three confirmed
blockers, the focused re-review (verdict **B**, PUBLISH), the merge through **PR #372** (merge commit
`43223dd6ab6ad169eefd64e37dee211f8bc306b9`, two-parent merge of `e84845de46c886b58d1e9cd04ed8bd4dffe84254` (base) +
`4696567683e242edd8f51587797487814d573421` (reviewed remediation candidate), tree
`83dbf367d0754d1b59f53ba85db0867672c3f543` — equal to the candidate tree; candidate ancestry PASS), post-merge
verification, owner acceptance, and formal closure. Documentation-only; grants no new implementation authority. Recorded
on the authoritative live tip resolved from Git (`43223dd`).

**Supersession clause.** This section supersedes the "Draft Level 2 … contract-definition decisions" wording **only where
it states that Draft Level 2 was a CONTRACT CANDIDATE / IMPLEMENTATION NOT AUTHORIZED / NOT STARTED**. That state was
accurate at the contract gate (PR #371) and **remains historical context, not current status**. Current status:
**Draft Level 2 is IMPLEMENTED / REMEDIATED / INDEPENDENTLY REVIEWED / MERGED / POST-MERGE VERIFIED / OWNER ACCEPTED /
FORMALLY CLOSED.** No prior history is rewritten.

| ID | Subject | Decision | Impl. authority | Evidence / boundary |
|---|---|---|---|---|
| D-DRAFT-L2-IMPL-01 | Draft Level 2 implemented, remediated, accepted & closed | ACCEPTED — **verdict B (re-review)**; **IMPLEMENTED / MERGED / VERIFIED / ACCEPTED / CLOSED** | NONE (closure) | Original impl candidate `9138f96` (independent review **C — REJECT**, blockers B1/B2/B3) → remediation candidate `4696567` (re-review **B**, PUBLISH) → **PR #372** merge `43223dd`. Merged scope **8 files / +981 / −6**; disallowed paths **NONE**; source branch `fix/draft-l2-local-continuity-remediation` + bundle **PRESERVED** (`draft_l2_remediation_4696567.bundle`, SHA-256 `895459d9dcff36fbef1a05c692c59ee1db234c501bb810e5ee9cfe6fceb15b6e`); focused **30 passed** / full **1799 passed, 1 skipped, 1 xfailed** |
| D-DRAFT-L2-IMPL-02 | Confirmed remediation of the three blockers | RECORDED — **B1/B2/B3 FIXED** | NONE | **B1** seed cleanup gated on a truthful one-shot `data-seed-accepted` (set only at successful `/start`); unrelated session render never clears an unsent seed draft. **B2** pagehide/visibilitychange flush only SAVES non-empty; never deletes on an empty/untouched field. **B3** empty sibling tab never deletes another tab's draft; storage-event handling shows a low-emphasis newer-copy awareness for a non-empty field and never overwrites visible text or deletes the newer stored draft. Each proven by a real-browser test that FAILED on `9138f96` and passes on `4696567` |
| D-DRAFT-L2-IMPL-03 | Capability now implemented | RECORDED | NONE | same-device localStorage recovery; 7-day TTL; seed + main-answer + bounded criticality-correction; debounced save + pagehide/visibilitychange; explicit Restore/Discard (no silent overwrite); stale/expired/corrupt/mismatch rejection; truthful device-only wording; a11y + bilingual (EN/AR); no-JS Level-0 fallback; failed & ambiguous submission retention; matching-draft cleanup only after truthful acceptance; multi-tab preservation + newer-copy awareness |
| D-DRAFT-L2-IMPL-04 | Exact capability boundary — "does NOT provide" | RECORDED | NONE | NO server-side draft persistence; account-linked drafts; cross-device/browser recovery; accounts; authentication; project ownership; authorization; collaborative editing; multi-device conflict resolution; writable continuation; durable version history; `AssertionRecord`/evaluation/maturity/gap/output effects from drafts; Phase 5 capability; Draft Level 3. Local draft data stays semantically separate from accepted answers and durable project records |
| D-DRAFT-L2-IMPL-05 | Non-blocking observations (NOT fixed here) | RECORDED | NONE | (1) stale `session.html` comment about seed acceptance (cleanup is correctly signal-gated); (2) `local_draft.js` `userEdited` assigned-not-read; (3) narrow one-shot-signal staleness edge if the success redirect render is never received; (4) the "Related: 146 passed" narrative was not one exact file set (all subsets + exact full suite green); (5) one multi-tab test uses synthetic event dispatch (reviewer also used real browser probes). Recorded, not reopened; the accepted candidate is not modified |
| D-DRAFT-L2-IMPL-06 | Phase 5 relationship | RECORDED | NONE | Draft Level 2 is local-only and account-independent; **Phase 5 must not reimplement/replace it**. Phase 5 discovery assesses only Draft-Level-3 integration boundaries (stable account/ownership identity; authorization on every future server-draft op; no ownership from `sid` alone; account-switch/logout for local drafts on shared devices; semantic separation of local draft / server draft / accepted answer / project; additive Draft Level 3 compatibility) — **not** authorization to implement server drafts |
| D-DRAFT-L2-IMPL-07 | Formal closure & next gate | **DRAFT LEVEL 2 FORMALLY CLOSED** | NONE | **NEXT ELIGIBLE GATE: Phase 5 — Accounts / Authentication / Ownership / Verified Email — DISCOVERY AND CONTRACT DEFINITION** (G-P5-IDENTITY-OWNERSHIP-DISCOVERY-CONTRACT-01). **Phase 5 IMPLEMENTATION NOT AUTHORIZED by this closure gate.** Server-side Draft Level 3, writable continuation, and every FPC remain NOT AUTHORIZED / NOT STARTED |

**Boundary.** Closure grants no downstream authorization. All prior decisions, candidates, verdicts, and observations are
preserved; no history is rewritten. **Draft Level 2 is FORMALLY CLOSED (PR #372, merge `43223dd`).** Decision **D17** and
the AISR seven-owner model are preserved; Phase 4 remains FORMALLY CLOSED; P4-2 Level-1 remains CLOSED.

## Phase 5 — Identity / Ownership / Verified-Email formal contract & continuing authorization (G-P5-FORMAL-CONTRACT-AND-CONTINUING-AUTHORIZATION-01) — documentation-only

**Decision status:** ACCEPTED / RECORDED — NO PHASE 5 IMPLEMENTATION AUTHORITY IN THIS GATE. The owner accepted the
discovery **G-P5-IDENTITY-OWNERSHIP-DISCOVERY-CONTRACT-01** (verdict **B — ACCEPT WITH NON-BLOCKING RISKS**), selected
**Identity Option A** and the structure **P5-1 → P5-2 → P5-3**, and granted a **continuing authorization** to complete
all three bounded increments through formal Phase 5 closure under the RED/GREEN + independent-review + publication +
post-merge-verification controls in `ACTIVE_INCREMENT_CONTRACT.md`. The full formal contract text is the "Phase 5 …
FORMAL CONTRACT-OF-RECORD" section of `ACTIVE_INCREMENT_CONTRACT.md` (which governs; this index does not duplicate it).
Recording this grants **no** implementation, code, test, schema, migration, dependency, CI, or push/PR/merge authority.
**P5-1 becomes the next eligible implementation gate only after this formal contract is merged and post-merge verified.**
Recorded on live tip `3b231936c5d01d2af9a1c0eca2dfd39d39161cff` (Merge PR #373). *(Superseded for current truth by the
P5-1 and P5-2 implementation-acceptance & closure sections below: **P5-1 (PR #375) and P5-2 (PR #377) are both MERGED
and FORMALLY CLOSED, and P5-3 — Project Ownership and Route Authorization — is the next eligible increment.**)*

| ID | Subject | Decision | Impl. authority | Evidence / boundary |
|---|---|---|---|---|
| D-P5-01 | Discovery acceptance | ACCEPTED — **verdict B** | NONE | G-P5-IDENTITY-OWNERSHIP-DISCOVERY-CONTRACT-01 accepted; existing account/auth/ownership/verified-email foundation = **NONE**; reusable primitives recorded (configured `app.secret_key`, Werkzeug scrypt, itsdangerous, stdlib, SQLite adapter); `flask.session` unused; CSRF absent; `projects` has no owner column; `sid` ≠ identity; `sid` possession ≠ ownership |
| D-P5-02 | Identity approach | ACCEPTED — **Option A (email + password)** | NONE | immutable UUID `account_id` (never email) PK; normalized-email uniqueness; **Werkzeug scrypt** hashes; no plaintext passwords; no raw verification/reset/session tokens stored; **no new runtime dependency** |
| D-P5-03 | Implementation structure & continuing authorization | ACCEPTED — **P5-1 → P5-2 → P5-3**; continuing authorization granted | NONE (per-gate controls apply) | move P5-1→P5-2→P5-3 without a new owner authorization **provided** each increment passes: bounded contract → genuine RED → minimum GREEN → focused/related/security/full-suite tests → adversarial self-review → SHA-preserving bundle → independent adversarial review (**A or B, no blockers**) → merge → post-merge verification → governance sync where material. STOP-and-return on: material blocker; live repo contradicting discovery; scope outside Phase 5; new unresolved product-policy decision; independent review **C**; security not provably fail-closed |
| D-P5-04 | Unverified-account policy | ACCEPTED | NONE | unverified MAY register / sign in / verify / recover / access basic account surfaces; MAY NOT create an account-owned durable project, claim an anonymous project, or use future sensitive delivery |
| D-P5-05 | Verified-account policy | ACCEPTED | NONE | **email verification required before creating & owning a durable account-linked project**; verified email ≠ authorization to any other project |
| D-P5-06 | Anonymous-project policy | ACCEPTED | NONE | anonymous projects keep `owner_account_id = NULL`; **not auto-claimable**; `sid` possession never assigns ownership; anonymous-to-account claim **deferred** to a separate future increment |
| D-P5-07 | Session policy | ACCEPTED | NONE | **idle 2h / absolute 14d**; cookie HttpOnly + SameSite=Lax + Secure(prod), **not** the project `sid`; `session_epoch` revocation; **password reset revokes all sessions**; current-session logout + bounded logout-all via epoch rotation |
| D-P5-08 | Account-deletion policy | ACCEPTED | NONE | **disable** (reversible) + **delete** (tombstone); sessions/tokens invalidated; login blocked as applicable; ownership links **not silently transferred**; accepted-answer data **not automatically destroyed**; final legal/commercial retention periods **outside this contract**, not invented |
| D-P5-09 | Legacy-project policy | ACCEPTED | NONE | legacy projects remain `owner_account_id = NULL`, capability-accessible under the existing truthful boundary; not auto-claimable/convertible |
| D-P5-10 | Email policy | ACCEPTED | NONE | dev = local file/console sink; prod = provider adapter behind an `EmailSender` abstraction; **verification token 24h; reset token 1h**; tokens random, hashed at rest, single-use, expiring, rate-limited, never logged raw; scope = verification / recovery / future email change only (**no** output/marketing/notification email) |
| D-P5-11 | Draft Level 2 integration policy | ACCEPTED | NONE | Phase 5 consumes but does not replace Draft L2; on logout/account-switch a local draft must not show under another account/project; preserve truthful device-only wording; do not upload the draft; **do not implement Draft Level 3** |
| D-P5-12 | Canonical models (account / token / ownership) | ACCEPTED | NONE | account fields per contract; typed token table; additive nullable `projects.owner_account_id` (no separate ownership table for the single-owner MVP unless proven insufficient); ownership checked **server-side** on every protected op; templates/JS never the authorization boundary |
| D-P5-13 | Security requirements | ACCEPTED | NONE | scrypt; anti-enumeration; session rotation + `session_epoch` revocation; HttpOnly/Secure/SameSite; **CSRF** on authenticated mutations; hashed single-use expiring tokens; server-side ownership incl. legacy routes; generic denial; brute-force/resend rate limits; no raw secret logging; disabled/deleted fail-closed; **no `sid`-based ownership claim** |
| D-P5-14 | Non-blocking risks | RECORDED | NONE | (1) production Secure-cookie depends on confirmed HTTPS/reverse-proxy; (2) no rate-limit primitive — use a small bounded store-backed counter, not a new platform/dependency; (3) production email deliverability is operational — begin with the dev sink, preserve the provider abstraction |
| D-P5-15 | Authorization boundary | NONE — NOT AUTHORIZED (this gate) | NONE | documentation-only; **P5-1 next eligible implementation gate after this contract is merged & post-merge verified**; P5-2/P5-3 NOT STARTED; Draft Level 3, writable continuation, output email delivery, PDF, ACV, AI Coach/WS17, STG, collaboration/sharing/teams/orgs, subscriptions, social login/SSO, admin dashboard, and every FPC remain NOT AUTHORIZED / NOT STARTED |

**Boundary.** No decision above grants Phase 5 implementation authority in this gate. Decision **D17** and the AISR
seven-owner model are preserved; Phase 4 remains FORMALLY CLOSED; P4-2 Level-1 and Draft Level 2 remain CLOSED.

## P5-1 — Account & Credential Foundation: implementation acceptance & closure (G-P5-1-ACCOUNT-CREDENTIAL-FOUNDATION-IMPLEMENTATION-01 + INDEPENDENT-REVIEW-01 + G-P5-1-CLOSURE-SYNC-01) — owner-accepted, MERGED & CLOSED

Recorded by the documentation-only closure sync **G-P5-1-CLOSURE-SYNC-01** (authoritative base
`65a2c0e258bf9635921046ad27f8a886cce78218`, Merge PR #375). The first bounded Phase 5 increment under the continuing
authorization (`D-P5-03`) was implemented RED-first, independently reviewed, published, merged, and post-merge verified.

| ID | Subject | Status | Impl. authority | Evidence / notes |
|---|---|---|---|---|
| D-P5-1-IMPL-01 | P5-1 implementation, review, merge & closure | **IMPLEMENTED / INDEPENDENTLY REVIEWED / MERGED / POST-MERGE VERIFIED / OWNER ACCEPTED / FORMALLY CLOSED** | NONE (closing P5-1 activates nothing downstream) | Gate G-P5-1-ACCOUNT-CREDENTIAL-FOUNDATION-IMPLEMENTATION-01; candidate `6be86f5` (tree `128b2d4`, parent `e84526d`); independent review G-P5-1-ACCOUNT-CREDENTIAL-FOUNDATION-INDEPENDENT-REVIEW-01 = **verdict B — ACCEPT WITH NON-BLOCKING OBSERVATIONS / PUBLISH**; merge **PR #375** `65a2c0e` (parents `e84526d` + `6be86f5`, tree `128b2d4`, ancestry PASS); scope **7 files / +1024**; source branch `feat/p5-1-account-credential-foundation` PRESERVED; focused **35 passed**, full suite **1834 passed, 1 skipped, 1 xfailed** |
| D-P5-1-IMPL-02 | Implemented capability (foundation only) | RECORDED | NONE | additive `accounts` persistence; immutable UUID `account_id` (never email); normalized + unique email; **Werkzeug scrypt** hashing; active/disabled/deleted status; `session_epoch` foundation; registration route + bilingual accessible form; **generic non-enumerating** public response; verification-token **hash-only** persistence; **24h** verification-token expiry; verification-token **supersession**; development `EmailSender` abstraction + memory sink; bounded store-backed **rate-limit foundation**; additive idempotent **legacy-safe migration**; **no plaintext password**; **no raw verification-token storage or logging** |
| D-P5-1-IMPL-03 | Capability boundary — explicit "does NOT provide" | RECORDED | NONE | P5-1 does **NOT** implement: login; logout; authenticated Flask sessions; authentication cookies; CSRF for authenticated mutations; verification completion; resend route; password recovery/reset; project ownership; `projects.owner_account_id`; route authorization; anonymous project claim; Draft Level 3; P5-3; output email delivery; production email provider. Registration does **not** sign in, does **not** create a project, and does **not** establish ownership |
| D-P5-2-PRE-01 | Rate-limit concurrency hardening (mandatory P5-2 precondition) | RECORDED — **BINDING for P5-2** | NONE | Before the rate-limit primitive backs login/verification-resend/password-recovery or other auth-sensitive controls: eliminate the proven multi-connection lost-update race; use an **atomic SQL increment or explicit immediate write transaction**; prove the limit under **genuine concurrent requests**; keep the public response **non-enumerating**; add **bounded cleanup of expired rate-limit rows**. Must be addressed within the first P5-2 implementation candidate before login/session security is accepted |
| D-P5-2-PRE-02 | SQLite thread/connection strategy (mandatory P5-2 precondition) | RECORDED — **BINDING for P5-2** | NONE | Before authenticated-session routes are treated as production-capable: resolve the **module-cached SQLite connection + thread-affinity** issue; define a safe **per-request or bounded connection strategy**; prove behaviour under a **threaded WSGI** environment; preserve transaction safety and fail-closed behaviour; do **not** merely set `check_same_thread=False` without proving locking and transaction correctness. Must be addressed within the first P5-2 implementation candidate before login/session security is accepted |
| D-P5-1-OBS-03 | Other non-blocking observations (recorded, do not reopen P5-1) | RECORDED | NONE | (1) expired `auth_rate_limits` rows have no cleanup sweep yet; (2) the "concurrent duplicate registration" test is sequential, though the reviewer independently proved true concurrent uniqueness; (3) the focused rate-limit generic-response test carries unused baseline logic and should be strengthened; (4) P5-2 cookie tests should assert absence/presence of **every** `Set-Cookie` header, not only a named cookie; (5) the password-too-long validation message should distinguish the maximum-length failure; (6) the unkeyed truncated SHA-256 email digest permits offline guessed-email confirmation if the DB is exposed — assess a **keyed** digest when touching the primitive; (7) `DevMemoryEmailSender` should have bounded retention in long-lived dev processes; (8) the exact targeted-regression narrative was not reproducible as one named test set, but all relevant subsets and the full suite were green; (9) the exact full-suite count requires the already-authorized pinned Playwright test-only dependencies |
| D-P5-1-NEXT-04 | Next eligible increment | RECORDED | NONE — **not authorized by this closure sync** | **P5-2 — Authenticated Sessions, Verified Email, and Recovery** is the next eligible increment under the continuing Phase 5 owner authorization (`D-P5-03`), eligible **only after this closure sync is merged and post-merge verified**; **P5-3: NOT STARTED**; **Draft Level 3: NOT AUTHORIZED**. Supersedes the forward-looking "P5-1 next eligible" wording in `D-P5-15` |

**Boundary.** This closure sync is documentation-only; it grants no implementation, code, test, schema, dependency, CI,
or push/PR/merge authority and begins no P5-2 work. P5-1 is FORMALLY CLOSED; closing it activates nothing downstream.
Decision **D17** and the AISR seven-owner model are preserved; Phase 4 remains FORMALLY CLOSED; P4-2 Level-1, Draft
Level 2, and now **P5-1** remain CLOSED; the Phase 5 formal contract remains MERGED / VERIFIED / ACCEPTED.

## P5-2 — Authenticated Sessions, Verified Email & Account Recovery: implementation acceptance & closure (G-P5-2-AUTH-SESSIONS-VERIFIED-EMAIL-RECOVERY-IMPLEMENTATION-01 + INDEPENDENT-REVIEW-01 + G-P5-2-CLOSURE-SYNC-01) — owner-accepted, MERGED & CLOSED

Recorded by the documentation-only closure sync **G-P5-2-CLOSURE-SYNC-01** (authoritative base
`402727a557edd7dbea3e92f477bf9cbefe74ea3e`, Merge PR #377). The second bounded Phase 5 increment under the continuing
authorization (`D-P5-03`) was implemented RED-first, satisfied the two mandatory P5-1-closure preconditions, was
independently reviewed, published, merged, and post-merge verified.

| ID | Subject | Status | Impl. authority | Evidence / notes |
|---|---|---|---|---|
| D-P5-2-IMPL-01 | P5-2 implementation, review, merge & closure | **IMPLEMENTED / INDEPENDENTLY REVIEWED / MERGED / POST-MERGE VERIFIED / OWNER ACCEPTED / FORMALLY CLOSED** | NONE (closing P5-2 activates nothing downstream) | Gate G-P5-2-AUTH-SESSIONS-VERIFIED-EMAIL-RECOVERY-IMPLEMENTATION-01; candidate `87c85c7` (tree `375db689`, parent `f84c87d`); independent review G-P5-2-AUTH-SESSIONS-VERIFIED-EMAIL-RECOVERY-INDEPENDENT-REVIEW-01 = **verdict B — ACCEPT WITH NON-BLOCKING OBSERVATIONS / PUBLISH**; merge **PR #377** `402727a` (parents `f84c87d` + `87c85c7`, tree `375db689`, ancestry PASS); scope **13 files / +1712 / −78**; source branch `feat/p5-2-auth-sessions-verification-recovery` PRESERVED; focused **40 passed**, full suite **1874 passed, 1 skipped, 1 xfailed** |
| D-P5-2-PRE-01-MET | Rate-limit concurrency hardening precondition | **SATISFIED** | NONE | `record_rate_attempt` read-modify-write runs inside `BEGIN IMMEDIATE`; proven race-free under REAL concurrent multi-connection threads (exactly `limit` allowed, stored count == N, one row); bounded expired-row cleanup added; privacy-digest subject keys; generic responses unchanged when limited |
| D-P5-2-PRE-02-MET | SQLite thread/connection strategy precondition | **SATISFIED** | NONE | one connection `check_same_thread=False` guarded by a re-entrant lock, every write in an explicit `BEGIN IMMEDIATE` transaction (foreign keys on, fail-closed rollback); proven under REAL multi-thread tests (no thread-affinity error; concurrent token consume atomic; record-store unchanged); NOT a bare `check_same_thread` override |
| D-P5-2-IMPL-02 | Implemented capability | RECORDED | NONE | login/logout; logout-all via `session_epoch`; signed-cookie authenticated session distinct from the project `sid`; idle **2h** / absolute **14d** expiry; session rotation on login; **CSRF** on authenticated mutations; email-verification completion + resend; recovery request + password-reset completion (**reset revokes all sessions**, no auto sign-in); disabled/deleted denial; generic non-enumerating responses; hardened concurrency-safe rate limiting; SQLite thread hardening; Draft L2 account-switch isolation; bilingual accessible UX; hash-only single-use expiring tokens (verification 24h / reset 1h); no `sid`-based identity/ownership; no new runtime dependency |
| D-P5-2-IMPL-03 | Capability boundary — explicit "does NOT provide" | RECORDED | NONE | P5-2 does **NOT** implement: `projects.owner_account_id`; project ownership; project route authorization; anonymous project claim; collaboration/sharing; P5-3; Draft Level 3; writable continuation; output email delivery; production email provider |
| D-P5-2-OBS-01 | Email-link tokens in URL paths | RECORDED — non-blocking | NONE | Verification/reset raw tokens appear in URL paths. Accepted mitigation: hash-only at rest; single-use; short expiry; no application logging; no third-party resources on result pages. Required future review before a production email-provider/reverse-proxy deployment: confirm access-log redaction; assess browser-history exposure; consider POST-based completion or fragment/interstitial alternatives where Lean |
| D-P5-2-OBS-02 | Password-reset transaction atomicity | RECORDED — non-blocking resilience debt | NONE | Reset performs sequential transactions (consume reset token → update password hash → increment `session_epoch` → supersede remaining reset tokens). When `account_store` is next modified for a related security increment: evaluate one atomic store operation; ensure password update and session revocation cannot partially commit; preserve single-use and fail-closed behaviour. The accepted P5-2 candidate is NOT changed by this closure gate |
| D-P5-2-NEXT-03 | Next eligible increment | RECORDED | NONE — **not authorized by this closure sync** | **P5-3 — Project Ownership and Route Authorization** is the next eligible increment under the continuing Phase 5 owner authorization (`D-P5-03`), eligible **only after this closure sync is merged and post-merge verified**; **Draft Level 3: NOT AUTHORIZED**. Supersedes the forward-looking "P5-2 next eligible" wording in `D-P5-1-NEXT-04` |

**Boundary.** This closure sync is documentation-only; it grants no implementation, code, test, schema, dependency, CI,
or push/PR/merge authority and begins no P5-3 work. P5-2 is FORMALLY CLOSED; closing it activates nothing downstream.
Decision **D17** and the AISR seven-owner model are preserved; Phase 4 remains FORMALLY CLOSED; P4-2 Level-1, Draft
Level 2, P5-1, and now **P5-2** remain CLOSED; the Phase 5 formal contract remains MERGED / VERIFIED / ACCEPTED.

## P5-3 — Project Ownership & Route Authorization: implementation acceptance & closure + FINAL FORMAL CLOSURE OF PHASE 5 (G-P5-3-PROJECT-OWNERSHIP-ROUTE-AUTHORIZATION-IMPLEMENTATION-01 + INDEPENDENT-REVIEW-01 + G-P5-FINAL-CLOSURE-SYNC-01) — owner-accepted, MERGED & CLOSED

Recorded by the documentation-only final closure sync **G-P5-FINAL-CLOSURE-SYNC-01** (authoritative base
`d9f888bd0def7b3275cd04860dfa2e8cc1504111`, Merge PR #379). The third and final bounded Phase 5 increment under the
continuing authorization (`D-P5-03`) was implemented RED-first, independently reviewed, published, merged, and post-merge
verified — and with it **Phase 5 is formally closed as a whole**.

| ID | Subject | Status | Impl. authority | Evidence / notes |
|---|---|---|---|---|
| D-P5-3-IMPL-01 | P5-3 implementation, review, merge & closure | **IMPLEMENTED / INDEPENDENTLY REVIEWED / MERGED / POST-MERGE VERIFIED / OWNER ACCEPTED / FORMALLY CLOSED** | NONE (closing P5-3 activates nothing downstream) | Gate G-P5-3-PROJECT-OWNERSHIP-ROUTE-AUTHORIZATION-IMPLEMENTATION-01; candidate `a0997c3` (tree `e6a03ab`, parent `b14c931`); independent review G-P5-3-…-INDEPENDENT-REVIEW-01 = **verdict B — ACCEPT WITH NON-BLOCKING OBSERVATIONS / PUBLISH**; merge **PR #379** `d9f888b` (parents `b14c931` + `a0997c3`, tree `e6a03ab`, ancestry PASS); scope **6 files / +562 / −15**; source branch `feat/p5-3-project-ownership-authorization` PRESERVED; focused **19 passed**, full suite **1893 passed, 1 skipped, 1 xfailed** |
| D-P5-3-IMPL-02 | Implemented capability | RECORDED | NONE | additive nullable `projects.owner_account_id` (indexed, idempotent legacy-safe migration); atomic verified-account owned-project creation (ownership immutable; no transfer); one central fail-closed server-side route-authorization helper (ownership from durable state + the validated session, NEVER the `sid`/cookie/template/client) on every protected `/session/<sid>` GET/POST route; cross-account + anonymous denial for owned projects; generic missing/not-authorized equivalence; disabled/deleted denial; owner-scoped project list; legacy/anonymous NULL-owner compatibility; Draft L2 account+project isolation; no new runtime dependency |
| D-P5-3-IMPL-03 | Capability boundary — explicit "does NOT provide" | RECORDED | NONE | P5-3 does **NOT** implement: anonymous project claim; ownership transfer; multiple owners; collaboration; sharing; teams; organizations; Draft Level 3; writable continuation; output email delivery; ACV; AI Coach; STG |
| D-P5-3-OBS-01 | In-memory session fallback | RECORDED — non-blocking | NONE | The `sid in SESSION_STORE` authorization fallback is accepted only because owned projects always have durable rows, no project-delete route exists, and production-owned data cannot reach the fallback. Before any future project-deletion capability, broader in-memory project access, or session-restoration expansion, replace it with caller/session-scoped authorization. P5-3 is not reopened here |
| D-PHASE5-CLOSE-01 | Phase 5 (Accounts / Authentication / Ownership / Verified Email) formal closure | **FORMALLY CLOSED** | NONE | Phase 5 delivered accounts; credentials; registration; login/logout; authenticated sessions; email verification; recovery/reset; session revocation; project ownership; route authorization; cross-account isolation (P5-1 → P5-2 → P5-3). Phase 5 did **NOT** deliver Draft Level 3, writable continuation, anonymous project claiming, collaboration/sharing, production/output email delivery, ACV, AI Coach, STG, or later commercial-readiness capabilities — all remain NOT AUTHORIZED / NOT STARTED. Closing Phase 5 activates nothing downstream |
| D-PHASE5-NEXT-02 | Next eligible gate | RECORDED | NONE — **not authorized; owner consideration only** | Per the authoritative roadmap phase map, the phase after Phase 5 is **Phase 6 — domain specialization / truthful specialist labeling**, recorded as **NEXT ELIGIBLE FOR OWNER CONSIDERATION / NOT STARTED / NOT AUTHORIZED**. The roadmap does NOT designate Phase 6 as "Post-Output Refinement Orchestration"; post-output refinement / AISR is a recorded cross-cutting capability DIRECTION (IMPLEMENTATION NOT AUTHORIZED), not a numbered next phase. Supersedes the forward-looking "P5-3 next eligible" wording in `D-P5-2-NEXT-03`. **Draft Level 3: NOT AUTHORIZED** |

**Boundary.** This final closure sync is documentation-only; it grants no implementation, code, test, schema, dependency,
CI, or push/PR/merge authority and begins no Phase 6, Draft Level 3, or any later phase. P5-1, P5-2, P5-3, and PHASE 5
are FORMALLY CLOSED; closing them activates nothing downstream. Decision **D17** and the AISR seven-owner model are
preserved; Phase 4 remains FORMALLY CLOSED; P4-2 Level-1 and Draft Level 2 remain CLOSED.

## Phase 6 — Truthful Domain Labeling Foundation (Option A): discovery acceptance & owner decisions D-P6-00…15 + P6-1 contract-of-record (G-P6-DOMAIN-SPECIALIZATION-DISCOVERY-01 + G-P6-1-TRUTHFUL-DOMAIN-LABELING-FOUNDATION-CONTRACT-01) — documentation-only

Recorded by the documentation-only contract-definition gate **G-P6-1-TRUTHFUL-DOMAIN-LABELING-FOUNDATION-CONTRACT-01**
(authoritative base `3703b4ff3a74ff735964e9f16be135f17834dc17`, Merge PR #380). The owner accepted the read-only Phase 6
discovery **G-P6-DOMAIN-SPECIALIZATION-DISCOVERY-01** and adopted decisions **D-P6-00 … D-P6-15**, selecting
**Option A — Truthful Domain Labeling Foundation**. The full formal contract text is the "P6-1 — Truthful Domain Labeling
Foundation" section of `ACTIVE_INCREMENT_CONTRACT.md` (which governs; this index does not duplicate it). Recording this
grants **no** implementation, code, test, schema, migration, dependency, CI, prompt, agent, model, route, UI,
domain-activation, or push/PR/merge authority.

| ID | Subject | Decision | Impl. authority | Evidence / boundary |
|---|---|---|---|---|
| D-P6-00 | Phase 6 naming disambiguation | ACCEPTED | NONE | The `ACTIVE_EXECUTION_ROADMAP` Phase 6 lane (Domain Specialization / Truthful Specialist Labeling) is authoritative for this execution gate; the registry-parity "Phase 6" (`docs/GOVERNANCE_DOCUMENTS.md`, 23/23 parity) is a distinct historical/registry-reconciliation track; per `PRODUCT_ARCHITECTURE_AND_CREDIBILITY_ROADMAP.md` neither lane authorizes the other |
| D-P6-01 | First outcome | ACCEPTED — **Option A** | NONE | Truthful Domain Labeling Foundation; no new domain engine; no new domain activation |
| D-P6-02 | Allowed label tiers | ACCEPTED | NONE | Tier 0 (General idea review) and Tier 1 (Domain-informed review) allowed now; **Tier 2** not until real domain-specific questions/rules/output/tests exist; **Tier 3 (Specialist) and Tier 4 (Licensed/professional) PROHIBITED** under the current product identity |
| D-P6-03 | Domain selection (this increment) | ACCEPTED | NONE | Preserve the current electronics confirmation gate; NO recommendation, AI inference, confidence scoring, or multi-domain UX |
| D-P6-04 | Future user override | ACCEPTED — deferred | NONE | When >1 domain is later supported, users may reject a recommendation and pick General/Uncertain; NOT implemented now |
| D-P6-05 | Low confidence | ACCEPTED | NONE | Low-confidence/unsupported cases remain General/Uncertain; never a specialist label |
| D-P6-06 | Multi-domain | ACCEPTED — NOT supported | NONE | Not supported in the first Phase 6 increment |
| D-P6-07 | Active domain | ACCEPTED | NONE | No new domain activated; the only runtime-operated domain remains `electronics_electrical` |
| D-P6-08 | Evidence bar for "domain-specific" | ACCEPTED | NONE | A future label may be called domain-specific only after repo evidence proves domain-specific questions + deterministic rules + output wording + behavioral tests + cross-domain isolation + safe unknown-domain fallback |
| D-P6-09 | First increment scope | ACCEPTED | NONE | Truthful labeling + truthful scope messaging + disclaimer preservation + behavioral truthfulness tests only; NO new deterministic domain rules |
| D-P6-10 | Data model | ACCEPTED — NONE | NONE | No schema or migration change; `confirmed_domain`/`domain_signal` unchanged; no confidence/secondary-domain/label-history/provenance/override fields |
| D-P6-11 | High-risk domains | ACCEPTED | NONE | Medical, regulated, structural, and other high-risk domains remain unsupported/restricted; not activated or labeled specialized in this increment |
| D-P6-12 | Claims policy | ACCEPTED | NONE | Preserve non-professional-advice / non-certification boundaries; do not claim specialist/professional-engineering review, certification, feasibility/regulatory approval, implementation readiness, or licensed advice |
| D-P6-13 | Future domain changes | ACCEPTED — deferred | NONE | A material future domain change must trigger full re-evaluation or a new project record; no silent reinterpretation of prior outputs; NOT implemented now |
| D-P6-14 | Registry hardening | ACCEPTED — **separate prerequisite increment** | NONE | Deferred Domain Registry validation gaps (version-format, date fields, allowed status values, classification/substance completeness, gap_type_mappings + rule_nuances completeness/element types, provenance/governance metadata, pack-id collision detection, alias resolution) are a SEPARATE bounded increment and a prerequisite before any new domain activation; NOT fixed in this contract gate or the first labeling implementation |
| D-P6-15 | Explicit deferrals | ACCEPTED | NONE | Deferred: new domain activation; multi-domain orchestration; AI-assisted recommendation; model/provider routing; new agents; new prompts; new output types; deterministic domain-rule activation; registry hardening; post-output refinement; WS17 AI Coach; STG; ACV; PDF/download; output email delivery; production email provider |
| D-P6-1-CONTRACT | P6-1 contract-of-record defined | **DEFINED → SUPERSEDED by D-P6-1-IMPL (implemented & merged)** | NONE | Full contract in `ACTIVE_INCREMENT_CONTRACT.md`. Public label map (`electronics_electrical` → EN "Electronics-informed review" / AR "مراجعة مستنيرة بمجال الإلكترونيات"; unknown/invalid → EN "General idea review" / AR "مراجعة عامة للفكرة"; fallback never silently electronics; server-side resolution, never client input); RED-01…07; behavioral runtime-truthfulness test (not source grep); exact permitted/prohibited paths; independent review A/B + C-mandatory triggers; rollback; Lean justification; completion criteria; stop conditions. The implementation gate has since COMPLETED and MERGED — see **D-P6-1-IMPL** |
| D-P6-1-IMPL | P6-1 implementation completed & merged | **IMPLEMENTED / REVIEWED (B) / MERGED / POST-MERGE VERIFIED** | NONE (closure only) | Candidate `ddaf4357e91f3c1d9443135b903871fdb3bd554a` (parent `df9e6ab`, tree `c50d791`) → **PR #385** merge `a8b874be5c994687e02d64b6e84404b641ab501e` (parents `df9e6ab`+`ddaf435`, merge tree `c50d791`, 5 files / +259 / −2). Independent review **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**, zero blockers. Focused **23 passed**; full suite green in both environments (owner Codespace **1885 passed / 3 skipped / 1 xfailed** with test-only Playwright absent; review env **1916 passed / 1 skipped / 1 xfailed**) — the extra skips are Playwright/browser test-environment dependent, not a P6-1 regression. Central resolver `web/domain_label.py::public_domain_label` (Jinja filter); EN/AR canonical; neutral General fallback (never electronics); internal `electronics_electrical` not exposed as public label; no Tier 2/3/4; no schema/engine/domain-pack change. Full record in the `ACTIVE_EXECUTION_ROADMAP` P6-1 post-merge closure-sync entry. **Superseded by D-P6-1-CLOSE (formally closed)** |
| D-P6-1-CLOSE | P6-1 formally accepted & closed | **FORMALLY ACCEPTED AND CLOSED** | NONE | Owner gate **G-P6-1-TRUTHFUL-DOMAIN-LABELING-FORMAL-CLOSURE-01**. Dedicated record `docs/governance/P6_1_TRUTHFUL_DOMAIN_LABELING_FORMAL_CLOSURE_RECORD.md` + append-only roadmap formal-closure entry. Closes **P6-1 only**; Phase 6 as a whole is NOT complete. Language decisions D-P6-16 / D-P6-17 / D-P6-18 preserved unchanged; PR #148 RTL/LTR boundary preserved; no localization / global language selector / Output-Language override / new domain / registry hardening / schema / engine change. **NEXT ELIGIBLE OWNER GATE: read from live `ACTIVE_EXECUTION_ROADMAP.md` — ELIGIBLE FOR OWNER CONSIDERATION, NOT AUTHORIZED; not assumed P6-2 from numbering; no later Phase-6 increment started by this closure** |
| D-P6-16 | No simultaneous bilingual UI rendering | ACCEPTED (RESUME-01) | NONE | For the same public-domain/UI label, EN and AR MUST NOT display simultaneously; both variants remain canonical internally; the user sees the variant of the selected UI language/context. The earlier P6-1 EN+AR-together rendering is **REJECTED** |
| D-P6-17 | Three-layer language model (UI / Input / Output) | ACCEPTED (RESUME-01) | NONE | (1) **UI Language** — explicit user choice, applies consistently across all pages, governs UI labels/buttons/messages/navigation, never auto-changed by typed content; (2) **Input Language** — free-form AR/EN/mixed, technical English terms (ESP32, Bluetooth Low Energy, LiDAR, API, CAN Bus, Python) accepted/preserved, mixed input never auto-switches UI Language; (3) **Output Language** — defaults to UI Language, a future independent selection (e.g. Arabic UI + English deliverable) is NOT authorized here and not conflated with UI Language |
| D-P6-18 | Global UI language selector | **IMPLEMENTED / INDEPENDENTLY REVIEWED (B) / MERGED (PR #388) / FORMALLY CLOSED** | NONE (closure only) | A global explicit English/Arabic UI-language selection (default English), applied consistently across active application UI chrome (Arabic RTL / English LTR), one language at a time. Originally recorded (RESUME-01) as a FUTURE requirement; subsequently OWNER-AUTHORIZED and implemented under **G-DP6-18-GLOBAL-UI-LANGUAGE-IMPLEMENTATION-01**. Accepted lineage `98c47d5` → `8920f46` → `62818a8` (SHA-preserving); merge **PR #388** `b47bf4bb57446956c47488283248cfbacd603e85` (parents `a0426cb`+`62818a8`, tree `f6ed63d`). Canonical actual questions remain English; non-question chrome follows UI Language; generated output outside scope; PR #148 Input Language separate; Question Translation Assistant NOT implemented. **Superseded by D-P6-18-CLOSE (formally closed)** |
| D-P6-18-CLOSE | D-P6-18 Global UI Language formally accepted & closed | **FORMALLY ACCEPTED AND CLOSED** | NONE | Owner gate **G-DP6-18-GLOBAL-UI-LANGUAGE-FORMAL-CLOSURE-01**. Dedicated record `docs/governance/D_P6_18_GLOBAL_UI_LANGUAGE_FORMAL_CLOSURE_RECORD.md` + append-only roadmap formal-closure entry. Independent final verdict **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**, zero blockers. Post-merge evidence: independent **1944 passed / 1 skipped / 1 xfailed / 0 failed** + Playwright **31 passed**; owner Codespace on `b47bf4b` **1913 passed / 3 skipped / 1 xfailed / 0 failed** (the 31-test delta is the browser subset not run in that Codespace — environmental, not a regression). Three non-blocking observations retained (criticality clarification kept English as an actual ask + gap-label headings localized as framing; `localize_deep` exact-match echo-collision negligible/cosmetic; six `session.html` criticality literals redundantly present via `t()` and `_DEEP_AR`). Closes **D-P6-18 only**; Phase 6 as a whole is NOT complete. This closure authorizes **no** successor: **Question Translation Assistant remains NOT AUTHORIZED / NOT STARTED**, and no Output-Language override / new domain / registry hardening / schema / engine / dependency change. **NEXT ELIGIBLE GOVERNANCE STEP: the Master Obligation Index gate, which REQUIRES SEPARATE OWNER AUTHORIZATION (documentation reconciliation only) — ELIGIBLE FOR OWNER CONSIDERATION, NOT AUTHORIZED / NOT STARTED; not the implementation of any new capability** |
| D-MOI-01 | Master Obligation Index governance-only gate | **AUTHORIZED — governance/documentation reconciliation only** | NONE (authorizes no implementation) | The owner explicitly authorized the **Master Obligation Index** governance-only gate. It adds a concise **pointer-only** routing layer to `docs/governance/CURRENT_PROJECT_STATE.md` (obligation layer → authoritative source → what it owns → where current status is determined) plus a displacement guard; it recomputes/duplicates **no** status, creates **no** new tracker/roadmap/matrix/taxonomy (D-FPC-MAP-06), and modifies **no** implementation/tests/engine/domains/schema/dependencies/CI and **not** the Product-Foundation plan. This authorization does **NOT** authorize any successor implementation, the **Question Translation Assistant** (remains NOT AUTHORIZED / NOT STARTED), **WS17**, any **Phase 7+** phase, any **CAP** item, or any new capability. Retained observation (NOT fixed here): `PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md` carries stale Phase-2-era document-status text (later phases marked NOT STARTED) that lags live execution (Phase 4 & 5 formally closed; Phase 6 partial) — a future, separately-authorized documentation-synchronization gate owns that fix; current execution status is read from `ACTIVE_EXECUTION_ROADMAP.md` + closure records |
| D-P6-CLOSE | Phase 6 (executed Domain Specialization / Truthful Specialist Labeling lane, Option A) formally accepted & closed | **FORMALLY ACCEPTED AND CLOSED** | NONE (governance/documentation-only) | Owner gate **G-PHASE-6-DOMAIN-SPECIALIZATION-FORMAL-CLOSURE-01**. Dedicated record `docs/governance/PHASE_6_DOMAIN_SPECIALIZATION_FORMAL_CLOSURE_RECORD.md` + append-only roadmap formal-closure entry. Closes the **executed Phase-6 lane** — Domain Specialization / Truthful Specialist Labeling, **Option A — Truthful Domain Labeling Foundation** — grounded in: discovery `G-P6-DOMAIN-SPECIALIZATION-DISCOVERY-01` accepted; **D-P6-00 … D-P6-15** adopted; **Option A** selected (D-P6-01); **P6-1** closed (**D-P6-1-CLOSE**; PR #385/#386); **D-P6-18** closed (**D-P6-18-CLOSE**; PR #388/#389); no required original Option-A implementation obligation remains (`ACTIVE_INCREMENT_CONTRACT.md` records no active contract-of-record). The Product-Foundation §5 **"Multi-Domain and Technology Capability Foundation"** is a **DISTINCT FUTURE PROGRAM** — NOT closed / NOT marked complete / NOT authorized by this closure, and not renamed into the executed lane (naming seam per **D-P6-00**). This closure authorizes **no** successor: **Question Translation Assistant** remains **NOT AUTHORIZED / NOT STARTED**; **Domain Registry hardening (D-P6-14)** remains a separate prerequisite before future new-domain activation; **Output-Language** override remains DEFERRED / NOT IMPLEMENTED / NOT AUTHORIZED (D-P6-17 is the accepted decision, not the capability); **WS17** post-gate/deferred; **STG** reserved/inactive; **ACV** future/separately gated; **PDF/download** deferred; **output email** deferred; **CAP-01…CAP-14** RECORDED ≠ AUTHORIZED; **Phase 7** separate future phase NOT AUTHORIZED; **new domain activation** NOT AUTHORIZED. **NO SUCCESSOR GATE IS AUTOMATICALLY AUTHORIZED** — the next action is read from the live `ACTIVE_EXECUTION_ROADMAP.md` + Master Obligation Index + this register and requires separate explicit owner authorization. Retained observation: the stale `PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md` status text is a future separately-authorized doc-sync (not remediated here). No implementation/tests/engine/domains/schema/dependencies/CI change; no new tracker/roadmap/matrix/taxonomy (D-FPC-MAP-06) |

| D-S5-C1 | Product-Foundation §5 Multi-Domain & Technology Capability Foundation — contract-definition + owner-decision gate | **CONTRACT OF RECORD — DEFINITION ONLY; AUTHORIZES NO IMPLEMENTATION** | NONE | Owner gate **G-S5-C1-MULTI-DOMAIN-FOUNDATION-CONTRACT-01** (governance/documentation-only). Dedicated contract `docs/governance/PRODUCT_FOUNDATION_S5_MULTI_DOMAIN_FOUNDATION_CONTRACT.md` (basis tip `a9bead4`, PR #391). Follows the accepted §5 read-only discovery. Scopes the **distinct future** Product-Foundation §5 program (NOT the closed executed Phase-6 lane). Records owner decisions **D-S5-01 … D-S5-09**, a formalized backward-compatible domain-pack contract, a capability-references-now / registry-later policy, the D-P6-14 sequencing (§5-I1 first implementation), the no-core-domain-name-branching migration principle, the Phase-7 resource-boundary handoff, and a bounded 5-increment plan (**§5-I1 … §5-CLOSE**, each RECORDED — NOT AUTHORIZED). Activates no domain; no engine/web/domains/schema/migration/tests/dependencies/CI change; no new tracker/roadmap/matrix/taxonomy (D-FPC-MAP-06). Authorizes **no** implementation and **no** successor — §5-I1 becomes eligible only after this contract is owner-accepted and merged and still needs separate explicit owner authorization |
| D-S5-01 | §5 registry authority model | **ACCEPTED — Option C** | NONE | One canonical **Domain Registry** (`engine/domain_registry.py`) stays the runtime domain authority; capability definitions live **inside domain packs** (reserved reference slot); **no** separate global capability registry now; promotion to a separate registry remains an additive, reversible future step gated by D-S5-02 |
| D-S5-02 | §5 Technology Capability model | **ACCEPTED — references now, registry later (evidence-gated)** | NONE | Capabilities represented as a thin normalized reference vocabulary referenced by packs; a separate Technology Capability Registry / capability packs are built **only** when a second activated domain genuinely reuses a capability. No capability ontology built now (capability-pack policy: optional/future) |
| D-S5-03 | §5 activation-status semantics | **ACCEPTED — Option A + separate activation policy** | NONE | Pack `status` = loader/lifecycle validity only (`registered` / `deprecated`), **not** user activation. Runtime activation becomes an explicit, separate, server-side policy (allowlist); `mechanical` / `medical_device` / `software` remain **registered-but-not-user-active**; the current electronics-only behavior **must not be silently broadened** |
| D-S5-04 | §5 cross-domain project model | **ACCEPTED — Option D** | NONE | Project stays generic with the single primary `confirmed_domain` preserved (default/back-compat); **multi-domain lives at the subsystem grain** (D-S5-05); implemented additively. Multiple peer root domains (Option C) REJECTED (breaks deterministic single-domain evaluation; no evidenced need) |
| D-S5-05 | §5 subsystem model | **ACCEPTED (required by D-S5-04) — conceptual contract only** | NONE | Subsystem = `{ immutable system-generated subsystem_id, user-defined display name, parent project, one primary domain, optional capability references, own evidence/gaps/risks/validation }`; both immutable id + display name; deterministic id. No schema/code in this gate |
| D-S5-06 | §5 unsupported/partial domain behavior | **ACCEPTED — preserve + formalize truthfully** | NONE | not-registered → General idea review fallback; registered-but-not-activated → General review + truthful "not yet supported for specialized review" notice (capture allowed, no specialist claim); experimental/partial/missing-capability → bounded general analysis, never a specialist/professional claim; preserves non-certifier identity and P6-1 "never silently electronics" |
| D-S5-07 | §5 specialist-category model | **ACCEPTED — pack metadata + presentation** | NONE | Specialist category = domain-pack metadata consumed by the presentation layer (reuse P6-1 `web/domain_label.py`); **no** separate specialist registry; **Tier 3 / Tier 4 remain PROHIBITED**; Tier 0–1 only |
| D-S5-08 | §5 Phase-7 handoff boundary | **ACCEPTED — resource-boundary contracts, not endpoints** | NONE | §5 must stabilize accepted resource-boundary contracts for project / domain / capability-reference / subsystem identity, evidence, gaps, risks, validation requirements, activation/support status, and unsupported-domain states before Phase 7 may freeze public API contracts. §5 defines **no** endpoints and does **not** start Phase 7 |
| D-S5-09 | §5 Phase-6 naming seam | **ACCEPTED — smallest supersession/context labels; no history rewrite** | NONE | Bounded future documentation-sync: add explicit supersession/context labels where the three "Phase 6" concepts (closed executed lane / §5 Multi-Domain program / registry-parity track) could be confused — the Product-Foundation plan (§5 header + stale §11/§12) and `docs/GOVERNANCE_DOCUMENTS.md`. Not a broad plan rewrite; history preserved |
| D-S5-I1-CLOSE | §5-I1 Domain Registry Validation Hardening (D-P6-14) formally accepted & closed | **FORMALLY ACCEPTED AND CLOSED** | NONE (governance/documentation-only) | Owner gate **G-S5-I1-DOMAIN-REGISTRY-HARDENING-FORMAL-CLOSURE-01**. Dedicated record `docs/governance/S5_I1_DOMAIN_REGISTRY_HARDENING_FORMAL_CLOSURE_RECORD.md` + append-only roadmap closure entry. Closes the **first §5 implementation increment** per §5-C1 §18. Base `3da1e03` → candidate `7920a73` → post-review remediation (test-only) `5d518f4` → **PR #393** merge `9d5e3bf1870d9f59def8bcd0d686a5b682886c8a` (parents `3da1e03`+`5d518f4`, merged tree `a62f46f`, 2 files / +401 / −1, changed paths `engine/domain_registry.py` + `tests/test_s5_i1_domain_registry_hardening.py` only). Hardened the **existing** canonical Domain Registry (no new registry; D-FPC-MAP-06): lifecycle-status + version-format + provenance-coverage (canonical `domains/domain_provenance.json`) + gap_type_mappings + rule_nuances structural validation + duplicate pack_id rejection + cross-pack alias collision rejection + authoritative provenance-manifest guard. Independent review **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS** (RED 15 failed/16 passed; focused 31 → 34 passed after remediation; full suite 1978 passed/1 skipped/1 xfailed/0 failed); delta review **B — ACCEPT DELTA**; **false-green closure CLOSED**; **BLOCKERS: NONE**. Accepted decisions: legacy `status:"active"` accepted as a transitional lifecycle-compat value (lifecycle only, NOT activation; migration to `registered` NOT claimed complete); `version:"1.0"` remains valid (no pack migration); provenance validated against the canonical manifest (§5-C1 §8 embedded-block wording = a NON-BLOCKING governance-sync obligation before §5-CLOSE). No new domain activated; electronics-only activation unchanged; legacy `iot_electronics` skipped/unchanged. **Product-Foundation §5 as a whole is NOT complete** — only §5-I1 is closed. **NEXT ELIGIBLE INCREMENT: §5-I2 (activation-status policy + unsupported-domain model) — ELIGIBLE FOR OWNER CONSIDERATION, NOT AUTHORIZED / NOT STARTED**; no successor gate automatically authorized. §5-I3 / §5-I4 / Phase 7 / QTA / WS17 / Output-Language / STG / ACV / PDF-email NOT STARTED; CAP-01…CAP-14 RECORDED ≠ AUTHORIZED |
| D-S5-I2-CLOSE | §5-I2 Activation-status policy + explicit unsupported-domain model formally accepted & closed | **FORMALLY ACCEPTED AND CLOSED** | NONE (governance/documentation-only) | Owner gate **G-S5-I2-ACTIVATION-STATUS-POLICY-FORMAL-CLOSURE-01**. Dedicated record `docs/governance/S5_I2_ACTIVATION_STATUS_POLICY_FORMAL_CLOSURE_RECORD.md` + append-only roadmap closure entry. Closes the **second §5 implementation increment** per §5-C1 §18. Product base `4770244` → reviewed foundation `d32ca5d` → completion `56afc7a` → **PR #396** merge `e224215228b52a53bb2a0cba8eacbdfc19e1ed78` (parents `4770244`+`56afc7a`, merged tree `1576c9c`, **3 files / +346 / −9**, changed paths `engine/domain_activation.py` + `tests/test_s5_i2_domain_activation.py` + `web/app.py` only). Delivered (D-S5-03): explicit runtime activation/support policy `engine/domain_activation.py` (no new registry; D-FPC-MAP-06); three support states **ACTIVATED / RECOGNIZED_NOT_ACTIVATED / UNKNOWN_OR_UNSUPPORTED**; pack lifecycle status separate from runtime activation; `electronics_electrical` the only activated specialist domain; mechanical/medical_device/software recognized-but-not-activated; unknown fail-closed; aliases cannot grant activation; `activated_domains()` constrained to recognized domains (ACTIVATED ⊆ RECOGNIZED); all web specialist-admission sites bound to the policy via `_admit_specialist_domain` (no competing web activation decision); consent semantics + classifier behavior preserved; **no user-facing copy / persistence / domain-pack change**. Independent foundation review **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**; completion delta review **B — ACCEPT DELTA** (§5-I2 IMPLEMENTATION COMPLETE: YES); **BLOCKERS: NONE**. Test evidence: RED **7 failed / 24 passed** on `d32ca5d`; focused **31 passed**; web regression **27 passed**; prior domain regression **138 passed**; Playwright Draft-L2 **30 passed**; full suite **2009 passed / 1 skipped / 1 xfailed / 0 failed**. A false-green risk (broad `pytest.raises(Exception)`) was identified and corrected to specific `DomainNotActivatedError` semantics **before** final delivery; accepted RED = 7 failed / 24 passed. Retained NON-BLOCKING observations: per-route bypass-mutation not directly test-detectable; helper stores passed value (not pack_id canonicalized); registry loads per admission; legacy iot pack skipped. No new domain activated; no CAP-16. **Product-Foundation §5 as a whole is NOT complete** — only §5-I2 is closed. **NEXT ELIGIBLE INCREMENT: §5-I3 (subsystem + cross-domain project model) — ELIGIBLE FOR OWNER CONSIDERATION, NOT AUTHORIZED / NOT STARTED**; no successor gate automatically authorized. §5-I4 / §5-CLOSE / Phase 7 / new-domain activation NOT AUTHORIZED; CAP-01…CAP-18 RECORDED ≠ AUTHORIZED |
| D-S5-I3-CLOSE | §5-I3 Subsystem + cross-domain project model foundation formally accepted & closed | **FORMALLY ACCEPTED AND CLOSED** (authoritative if/when this closure candidate is merged) | NONE (governance/documentation-only) | Owner gate **G-S5-I3-SUBSYSTEM-CROSS-DOMAIN-MODEL-FORMAL-CLOSURE-01**. Dedicated record `docs/governance/S5_I3_SUBSYSTEM_CROSS_DOMAIN_MODEL_FORMAL_CLOSURE_RECORD.md` + append-only roadmap closure entry. Closes the **third §5 implementation increment** per §5-C1 §18 (D-S5-04 / D-S5-05). Product base `04a9c4d` → candidate `0a7f135` → **PR #398** merge `dac5696ebcf9c9814b2adb66887a535e089a6c85` (parents `04a9c4d`+`0a7f135`, merged tree `63a63e3`, **3 files / +246 / −0**, changed paths `engine/idea_state.py` + `engine/subsystem_model.py` + `tests/test_s5_i3_subsystem_model.py` only). **Delivered now:** canonical `IdeaState` extended additively with one in-memory, persistence-independent `subsystems` field; minimum subsystem descriptor + operations (`engine/subsystem_model.py`); one project → zero-or-more subsystems → each may reference a canonical domain as **metadata only** (never activates, never changes the scalar root domain / `confirmed_domain`); support-state integration with the §5-I2 policy (unknown never silently electronics); no peer-root `domains` list (D-S5-04); canonical Domain Registry reused (D-FPC-MAP-06). **NOT delivered (future):** durable subsystem persistence; immutable/deterministic subsystem identity; display-name; subsystem-grain evidence/gaps/risks/validation — governance must not claim these were implemented (GAP-3). Independent review **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**; **BLOCKERS: NONE**. Test evidence: RED ImportError on base (valid); focused **16 passed**; model/domain regression **153 passed**; persistence regression **55 passed**; full suite **2025 passed / 1 skipped / 1 xfailed / 0 failed**; independent browser **31 passed** (no web surface changed). Retained NON-BLOCKING observations **OBS-1…OBS-7** (durable persistence future; D-S5-05 conceptual delta; duplicate subsystem ids; alias canonicalization before persistence; object mutability; implementation-path reconciliation = accepted minimum-path; persistence-envelope hardening future). **§5-I4 NECESSITY EVIDENCE: NONE → EVIDENCE GATE NOT MET → SKIP at current evidence** (no Technology Capability Registry created/started; not permanently forbidden — revisit only if new evidence emerges before §5-CLOSE). No new domain activated; no persistence/schema migration; no web/UI; no CAP-16; no §5-I4/§5-CLOSE/Phase 7. **Pre-§5-CLOSE governance obligations retained: GAP-1** (§5-C1 §8 provenance wording ↔ §5-I1 manifest validation), **GAP-2** (D-S5-09 Phase-6 naming seam), **GAP-3** (D-S5-05 conceptual-vs-delivered wording), **GAP-4** (roadmap sync). **Product-Foundation §5 as a whole is NOT complete** — §5-I1/§5-I2/§5-I3 closed. **NEXT ELIGIBLE GATE: §5-CLOSE (Product-Foundation §5 formal closure + GAP-1…GAP-4 reconciliation)** under continuing owner authorization — NOT STARTED; no successor gate automatically authorized. Phase 7 NOT AUTHORIZED / NOT STARTED; CAP-01…CAP-18 RECORDED ≠ AUTHORIZED |
| D-S5-CLOSE | Product-Foundation §5 (Multi-Domain and Technology Capability Foundation) formally accepted & closed | **FORMALLY ACCEPTED AND CLOSED** (authoritative if/when this closure candidate is merged) | NONE (governance/documentation-only) | Owner gate **G-S5-CLOSE-PRODUCT-FOUNDATION-FORMAL-CLOSURE-01**. Dedicated record `docs/governance/PRODUCT_FOUNDATION_S5_FORMAL_CLOSURE_RECORD.md` + append-only roadmap closure entry. Closes the **Product-Foundation §5 program lane** after: **§5-C1** contract accepted; **§5-I1** closed (D-S5-I1-CLOSE); **§5-I2** closed (D-S5-I2-CLOSE); **§5-I3** closed (D-S5-I3-CLOSE); **§5-I4 EVIDENCE GATE NOT MET → SKIPPED at current evidence** (fresh live check: no `capability_refs` in any active v1.0 pack, no capability token reused across packs, one activated domain — no Technology Capability Registry created/started; not permanently forbidden). **Material result (verified live at `0e2206f`):** canonical hardened Domain Registry; explicit activation/support-state policy (electronics-only activated; pack-status ≠ activation; ACTIVATED ⊆ RECOGNIZED); truthful unsupported-domain handling; additive in-memory subsystem/cross-domain foundation with scalar root `confirmed_domain` preserved (no peer-root domains); Phase-7-safe resource/model boundaries at model level only (no APIs). **Four governance gaps RECONCILED:** GAP-1 (§5-C1 §8 embedded-provenance wording superseded by the accepted §5-I1 manifest-based coverage validation as the authoritative interpretation; history preserved, validation not weakened); GAP-2 (authoritative disambiguation — the lane closed now is Product-Foundation §5 Multi-Domain, DISTINCT from the closed executed Domain-Specialization Phase-6 lane and the registry-parity "Phase 6" track; residual stale plan §11/§12 + `GOVERNANCE_DOCUMENTS.md` text remains a bounded non-blocking future doc-sync, already superseded by the MOI + closure records); GAP-3 (D-S5-05 future semantics — durable subsystem persistence/identity/display-name/subsystem-grain evidence-risk-validation/UI — recorded as future-gated, NOT claimed delivered); GAP-4 (roadmap/current-truth synchronized). **ORIGINAL §5 UNFINISHED MATERIAL OBLIGATION: NONE; POST-§5 MATERIAL IMPLEMENTATION GAP: NONE.** No second domain registry / project root-model; no Technology Capability Registry; no new domain activated; no duplicate Integration-Ready decision (existing **Phase 7 — API and Integration Foundation** authority reused per D-FPC-MAP-06; owner outbound-transfer + future inbound-result clarification preserved against that existing requirement; Wokwi example-only). No implementation/test/domain-pack change; historical records preserved (clarification/supersession only). **NEXT ELIGIBLE PHASE: Phase 7 — API and Integration Foundation — ELIGIBLE FOR OWNER CONSIDERATION, NOT AUTHORIZED / NOT STARTED**; no successor auto-authorized; Phases 8/9/10, new-domain activation, CAP-01…CAP-18, QTA, WS17, STG, ACV, Output-Language, PDF/email remain NOT AUTHORIZED |
| D-P7C-01 | Phase 7 — API and Integration Foundation formal contract & acceptance criteria (P7-C) published as contract-of-record | **CONTRACT OF RECORD — DEFINITION ONLY; THE CONTRACT ITSELF CONFERS NO IMPLEMENTATION AUTHORIZATION** | NONE (from the contract itself) | Owner gate **G-P7C-FORMAL-PHASE-7-CONTRACT-PUBLICATION-01** (governance/documentation-only). Dedicated contract `docs/governance/PHASE_7_API_AND_INTEGRATION_FOUNDATION_P7C_CONTRACT.md` (basis tip `f82b18b`). Formalizes the owner-accepted, frozen **P7-A** discovery + **P7-B** architecture decisions (plus the accepted **P7-B correction addendum** and **P7-C contract correction addendum**, which govern on conflict): initial independently-addressable product surface = **Project read representation + Versioned Structured Output/Export only** (Domain support-state, Evidence/Provenance carried within, not standalone v1 resources; "two" is the current minimal surface, not a permanent numeric invariant; transport/security metadata is not a product resource); Lean **internal read/export service seam** before public exposure (first slice = authorized project read + governed versioned export; no mutation/progression/write; no mandatory web-route migration); **read/export-first** (no public state mutation; no privileged path around ownership/progression/evidence/Keep-Refine/full re-evaluation); distinct **machine/API principal** via canonical authorization/ownership, least privilege, revocation/expiration/rotation/auditability, never browser-session reuse, principal↔account taxonomy + credential format DEFERRED; **first-public-exposure security baseline** (authn, authz, public/export version identity, stable errors, request/correlation identity, basic access/security audit, basic protective rate-limit, provenance where applicable); outbound **InventorAI canonical → adapter → vendor** boundary (InventorAI central context authority; no Integration Orchestrator / routing engine / vendor-shaped core); **external results untrusted by default** (governed review/acceptance required before any authorized project-state effect; exact trust-state taxonomy + persistence schema/location/retention/deletion/record-type NOT frozen; never auto-mutate progression / prove feasibility-safety / satisfy validation / activate a domain / become trusted evidence / replace review); **subsystem** public API/durable identity DEFERRED; **async/job** model DEFERRED (no ExternalProcessingRequest/Result/Job/Task reserved); **first integration proof** = outbound-only, non-mutating, vendor-neutral local/reference adapter with semantic no-project-state-mutation evidence (**Wokwi NOT SELECTED**). **Audit ≠ Monitoring; basic rate-limit ≠ all Abuse Controls; Reference/Test Harness ≠ Partner/External-Integration Sandbox** — each a distinct preserved original obligation. **§18 obligation register:** every original Phase-7 obligation preserved with owner/reason/trigger; **no deferred obligation pre-judged as a closure blocker/non-blocker — final closure classification RESERVED EXCLUSIVELY for the mandatory §25 PHASE-7 REMAINING-OBLIGATION / EXIT-CRITERIA REVIEW; a successful first proof never auto-authorizes P7-CLOSE.** Separate ownership preserved (D-FPC-MAP-06): CAP-15…18, AISR, Project Technology Profile, WS-PFV-001, WS17, STG, ACV, QTA, PDF Download, Email Delivery, Output Language, Phase-9 Domain Activation — reusability authorizes none; no second Domain Registry / Technology Capability Registry / Integration Orchestrator / AI routing / tool-recommendation engine. No engine/web/domains/schema/migration/tests/dependencies/CI change; no new tracker/roadmap/matrix/taxonomy (D-FPC-MAP-06). **This decision records contract acceptance only; it does NOT itself authorize implementation — implementation authority is the separate D-P7-STANDING-01** |
| D-P7-STANDING-01 | Standing Owner Authorization to complete all remaining Phase-7 work through formal Phase-7 closure | **STANDING PHASE-7 AUTHORIZATION — GRANTED (distinct later owner decision; not conferred by the P7-C contract)** | **GRANTED for the remainder of Phase 7, subject to contract boundaries, evidence gates, triggers, tests, independent review where required, and exit criteria** | A distinct, later owner decision issued after the authorization state reflected in the superseded unpublished candidate `8001d7f`. **Substance:** (1) the standing authorization covers remaining Phase-7 work through formal closure — publication/commit of the accepted P7-C contract, **P7-I1** and subsequent Phase-7 implementation increments, evidence-triggered Phase-7 sub-gates when their accepted triggers are actually met, the mandatory Remaining-Obligation / Exit-Criteria Review, and **P7-CLOSE only if all closure criteria are satisfied**; (2) **no repeated top-level owner authorization is required at each intermediate Phase-7 gate**; (3) each gate still requires bounded scope, a correct verified live base, acceptance criteria, evidence, tests where applicable, Lean minimum-path compliance, and independent review where required; (4) evidence-triggered gates may execute **only when their accepted trigger is actually met**; (5) P7-CLOSE requires the mandatory §25 review and satisfaction of closure criteria. **All frozen P7-B/P7-C architectural constraints remain binding.** **Standing authorization ≠ active implementation increment:** before P7-I1 implementation begins the repository must establish the bounded P7-I1 increment contract/scope from the accepted P7-C governance model and verify its live base. **NOT authorized by this standing grant:** Phase 8; Phase 9; Phase 10; deployment/release; separately governed CAP-15…18; AISR; QTA; ACV; WS17; STG; PDF/Email delivery; Output Language; domain activation outside authorized Phase-7 scope; any evidence-triggered Phase-7 capability before its accepted trigger is actually satisfied. **Current state at this record:** current active implementation = NONE; bounded P7-I1 increment contract = NOT YET ESTABLISHED; P7-I1 implementation = NOT STARTED |

**Boundary.** No decision above grants Phase 6 implementation authority in this gate. Only `electronics_electrical` is
runtime-operated; no new domain is activated; labels are capped at Tier 0–1; there is no schema/engine/AI/model/agent
change. Decision **D17** and the AISR seven-owner model are preserved; Phase 5 remains FORMALLY CLOSED; P4-2 Level-1,
Draft Level 2, P5-1, P5-2, and P5-3 remain CLOSED.


## PSRR — Production Security & Release Readiness (cross-phase release gate)

| Decision | Summary | Status | Owner / phase | Change | Source |
|---|---|---|---|---|---|
| D-PSRR-01 | **Public Production Deployment is PROHIBITED until a formal PSRR — Production Security & Release Readiness gate is executed, independently verified where required, formally accepted, and recorded GO / PASS.** PSRR is a durable, cross-phase, evidence-based **release gate** (trigger: **before first public production deployment**), registered here by name/scope/GO-NO-GO/hard-block only. It **operationalizes** the existing **OD-P** (production-readiness/deployment criteria defined & evaluated in **Phase 10** only; separate deployment gate + explicit owner deployment authorization REQUIRED; deferred until Phases 4–9 formally completed) within the canonical **Phase 10 — Commercial, Legal, Security and Operational Readiness** ownership (D-FPC-MAP-06: **existing owner extended — no competing framework**). It moves no OD-P/Phase-10 ownership, completes no Phase, selects no vendor, and claims no production readiness. | **ACCEPTED — REGISTRATION AUTHORITATIVE** (independently reviewed, Owner-accepted, MERGED PR #413, merge `6c0626e3ca659f90133a7df865e2a439f7b74f73`; parents `c15b7e7`+`a569f4b`; merged tree `4f1780ce` == accepted candidate tree; POST-MERGE VERIFIED — the "authoritative if/when reviewed/accepted/merged/post-merge-verified" condition is now satisfied) | Phase 10 (consumed cross-phase); consistent with & subordinate to OD-P | NONE (governance/documentation-only) | `docs/governance/PSRR_PRODUCTION_SECURITY_RELEASE_READINESS_REGISTRATION.md` |

**Substance (D-PSRR-01).** Public production is BLOCKED until **PSRR = GO**; **PSRR = NO-GO / FAIL** leaves the block in force. No agent may infer production authorization from "phase complete", "tests green", or "a security baseline exists". Minimum future PSRR **execution** scope (registration only — none implemented/evaluated now): application/API security; authentication; authorization; ownership isolation; machine/API credential handling; revocation/rotation/expiry; secrets/config management; production configuration; TLS/secure transport; security headers; dependency/vulnerability scanning; third-party dependency review; database/data security; data retention/deletion; privacy/data-lifecycle; backup + restore + disaster-recovery; audit logging; **monitoring**; **alerting**; **broad abuse controls**; rate-limit review; distributed/credential-abuse review; **audit-retention operational policy**; incident-response; production logging/sensitive-data handling; external-integration & vendor-integration security where applicable; infrastructure/deployment configuration; environment/secrets separation; security testing; penetration testing where risk warrants; release evidence package; independent security/release review where required; formal GO/NO-GO. PSRR is evidence-based and must include independent verification where material security/release claims require it (existing InventorAI independent-review governance). **No security/cloud/scanner/CI/hosting/monitoring/deployment vendor is selected.** The Phase-7 §25 deferred security/operations items (Monitoring; broad Abuse Controls; `access_audit` retention/cleanup; production secrets operations) remain **NOT delivered / NOT solved** — PSRR **may reassess** them but does **NOT** auto-implement them; their §25 classification is unchanged. **PSRR EXECUTION: NOT STARTED.** This decision reopens no Phase 7 and authorizes no Phase 8/9/10 work and no deployment/release.


## Phase-8 privacy / legal entry boundary (clarification)

| Decision | Summary | Status | Owner / phase | Change | Source |
|---|---|---|---|---|---|
| D-P8-PL-01 | **Phase-8 privacy/legal entry-boundary clarification.** Authoritatively interprets the canonical Phase-8 entry prerequisite "privacy and legal prerequisites accepted" (remediation plan §340) **without** pulling Phase-10 work forward and **without** weakening Phase-10/OD-P ownership. It distinguishes four bounded classes (A/B/C/D below): Phase-8 **entry-level** privacy/legal *design/architecture* prerequisites (A) that must be accepted before a Phase-8 contract/implementation proceeds; Phase-10 **final public** legal/release artifacts (B) that remain Phase-10-owned and MUST NOT become Phase-8 deliverables merely to satisfy entry; the **public-paid-activation** hard gate (C); and the preserved **OD-I/OD-N** substance (D). Governance/documentation-only; starts no Phase 8 implementation, activates no Phase-10/PSRR work, selects no provider, authorizes no paid activation, and provides no legal advice. Extends existing owners (ODR + remediation-plan §340/§363–367 + OD-I/OD-N/OD-P + D-PSRR-01) per D-FPC-MAP-06 — **no new privacy/legal/commercial framework.** | **ACCEPTED — CLARIFICATION (candidate; authoritative if/when independently reviewed, Owner-accepted, merged, and post-merge verified)** | Phase 8 (entry boundary); Phase-10/OD-P ownership preserved | NONE (governance/documentation-only) | this register + remediation plan §340 / §363–367 (interpreted, not rewritten) |

**Substance (D-P8-PL-01).**

**A. PHASE-8 ENTRY-LEVEL PRIVACY/LEGAL PREREQUISITES (design/architecture/legal-scope only — must be accepted before a Phase-8 contract/implementation proceeds).** The bounded rules needed to safely *define* and later *implement* a provider-neutral commercial model: plans; subscriptions; entitlements; quotas; commercial access controls; billing-domain data model; account↔commercial-state relationships; data-handling boundaries for commercial data (consistent with OD-O privacy-by-default and OD-E legal boundary); cancellation/refund **state-model interfaces** (internal model shape, not public policy text); and provider-neutral commercial architecture reusing existing seams (D-FPC-MAP-06). These are **design/scope acceptances**, not public legal documents.

**B. PHASE-10 FINAL PUBLIC LEGAL/RELEASE ARTIFACTS (remain Phase-10-owned; MUST NOT be pulled into Phase 8 to satisfy entry).** Final public **Privacy Policy**; final **Terms of Service**; final **payment terms**; final **refund policy**; final **consent/legal notices**; trademark / final brand clearance; production legal readiness; production privacy/security review; operational release readiness; deployment authorization. These are **not** Phase-8 deliverables and their completion is **not** required merely to *define* the Phase-8 commercial model (remediation plan §363–367; OD-P).

**C. PUBLIC PAID ACTIVATION (hard gate — unchanged).** Even if Phase 8 later implements billing/subscription/entitlement mechanics, **NO public paid activation is authorized** until all applicable **Phase-10 legal/readiness requirements**, **PSRR = GO/PASS** (D-PSRR-01), the **governing separate Deployment Gate**, and **explicit Owner deployment authorization** (OD-P) are satisfied. Building Phase-8 mechanics authorizes no public paid activation.

**D. OD-I / OD-N PRESERVED (substance unchanged).** **OD-I:** no paid subscription/billing **activation** before durable persistence (Phase 4 — CLOSED) and account/authorization (Phase 5 — CLOSED) foundations; no paid plan on in-memory storage. **OD-N:** plan/subscription/commercial status must never alter technical evaluation, safety gates, evidence requirements, technical conclusions, or invention-progression decisions (plan-neutral by construction — verified: engine scoring/progression/safety references no plan/tier/price). This clarification alters no OD-I/OD-N substance.

**Resulting authoritative interpretation.** (1) Phase 8 may proceed to **CONTRACT DEFINITION** once the bounded class-A entry-level privacy/legal *design* prerequisites are accepted. (2) Phase 8 does **not** require completion of the final Phase-10 public legal documents (class B) merely to define its commercial model. (3) **Phase 10 retains ownership** of final public legal/commercial/security/operational readiness. (4) Building Phase-8 mechanics does **not** authorize public paid activation (class C). (5)–(7) This clarification activates **no** Phase-10 work, **no** PSRR work, and **no** billing implementation. **DOCUMENTED NO-VALID-RED** (governance/documentation-only). Remediation-plan §340 prerequisite text is **preserved (not rewritten)** and authoritatively interpreted by this decision.

## G-MPR-01-D — Findings Disposition & Roadmap Registration (durable owner dispositions from the accepted G-MPR-01 master review)

Governance/documentation-only registration; base `d37caef8cfc0e4c5e53275e6e126ec8247a26219`. Canonical record:
`docs/governance/G_MPR_01_D_FINDINGS_DISPOSITION_AND_ROADMAP_REGISTRATION.md`. Registers **future obligations only** — no
implementation, no phase activation, no domain activation, no provider selection, no production authorization. Phase-8 order
preserved (P8-I1 → P8-I2 → G-MPR-01/disposition → P8-I3 → P8-I4 → P8-CLOSE). **DOCUMENTED NO-VALID-RED.**

| Decision | Summary | Status | Impl. authority | Blocks P8-I3? | Source |
|---|---|---|---|---|---|
| D-GMPR-01-D-D1 | **P8-I1 formal closure gap (F1) — ADD dedicated record.** P8-I1 formally closed via a late-registered dedicated closure record; documentation gap only; no implementation reopened; historical evidence cited not fabricated (impl RED→GREEN full suite 2122; merged PR #418 `2bf389d`, merged tree `814d15d` == accepted impl tree; post-merge verified; independent-review letter-verdict provenance disclosed per the PR #341 precedent). | RESOLVED | NONE | Resolve as part of this disposition | `P8_I1_..._FORMAL_CLOSURE_RECORD.md` |
| D-GMPR-01-D-D2 | **P8-I3 lifecycle-persistence rule.** P8-I3 MUST use a bounded additive backward-compatible strategy (additive lifecycle table(s) or a justified additive extension); preserve account identity / entitlement (P8-I1) / quota (P8-I2) / existing durable records; idempotent evolution; existing DBs remain readable; NO destructive migration / NO implicit rewrite; rollback/recovery reasoning MUST be in the P8-I3 contract. No schema designed/implemented here. | REGISTERED (contract constraint) | NONE | Binding on the future P8-I3 contract | G-MPR-01 §N; F-matrix |
| D-GMPR-01-D-D3 | **Pre-Phase-9 Core Domain-Neutrality Prerequisite Gate (MANDATORY future gate).** Before the first non-electronics Phase-9 activation, remove/govern electronics-core couplings: `engine/safety_signal.py` (`_MVP_DOMAIN`, electrical-only cues, label forcing), `engine/path_n_questions.py` (electronics-pinned, domain-blind), scattered web-admission literals, hard-coded domain tie-break. MANDATORY before first additional domain activation; NOT before P8-I3; not implemented now. | REGISTERED (future gate) | NONE — LEVEL 1 | **No** | G-MPR-01 §H/§J; F2/F3 |
| D-GMPR-01-D-D4 | **Cross-Domain / Multi-Disciplinary Engineering Integration (future gate; NOT AUTHORIZED).** One invention across multiple domains with domain-specific truth preserved: multiple subsystems; dependency representation; conflicts; trade-offs; shared-constraint propagation; unified assessment; no silent cross-domain truth overwrite; canonical cross-domain output. **DOMAIN REFERENCE ≠ DOMAIN ACTIVATION ≠ CROSS-DOMAIN EVALUATION.** Placement: after Phase-9 activation maturity (≥2 activated domains) or as a governed successor to skipped §5-I4; not before P8-I3. Re-homes the stale runtime "deferred to Phase 6" pointer (code comment correction deferred to a future authorized code gate). **[Scope MEANING clarified by Amendment 01 — see the "Substance (D-GMPR-01-D-D4 — Amendment 01)" block below this table. Clarifying-only / NON-ACTIVATING: same decision identity (no second owner); D4 remains REGISTERED (future gate) / NOT AUTHORIZED; sequencing unchanged; the amendment adds NO new blocker to the Phase-9 next-domain decision or Mechanical P9-QS qualification.]** | REGISTERED (future gate) | NONE | **No** | G-MPR-01 §I; F4/F14 |
| D-GMPR-01-D-D5 | **Deferred-capability re-homing (all remain NOT AUTHORIZED).** QTA + Output-Language implementation = ADD live future homes (previously un-homed); ACV / PDF Download / Email Delivery = MOVE off their now-closed Phase-3/4/5 anchors to live successor gates; existing prerequisite sequencing preserved. Distinctions preserved: **UI Language ≠ Input Language ≠ Output Language ≠ QTA** (do not collapse). | REGISTERED (re-homed) | NONE | **No** | G-MPR-01 §C; OD-U/OD-T; D-P6-17 |
| D-GMPR-01-D-D6 | **CAP index range alignment (F8).** Register range is **CAP-01…CAP-18**; master-obligation/index "CAP-01…CAP-14" references corrected to CAP-01…CAP-18. No capability deleted/renumbered/changed in substance. | RESOLVED | NONE | **No** | `INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md`; F8 |
| D-GMPR-01-D-D7 | **Real-vendor vs CAP-15 distinction (F9).** Keep distinct (not merged): A provider abstraction/replaceability (CAP-15); B actual real-vendor integration activation (P7 §25 trigger-deferred; no vendor selected); C async/webhook (P7 §25 rows 32/34); D external export/integration adapters (P7-I3 boundary). Different triggers/owners; avoid duplicate tracking. | CLARIFIED | NONE | **No** | G-MPR-01 §C/§K; F9 |
| D-GMPR-01-D-D8 | **`iot_electronics` legacy disposition (guarded).** Registered as historical/legacy benchmark artifact; invalid under v1.0 pack schema (`schema_version=None`); intentionally registry-skipped; not activated; benchmark-linked evidence important. **Semantic disposition (superseded vs future-IoT-seed vs benchmark-only-legacy) reserved to a later Owner decision before Phase-9 IoT activation.** **Guard: NO deletion/migration/schema-normalization/activation/repurposing of `iot_electronics` (or its benchmark schema/prompt) without a separately authorized gate.** Left untouched. | REGISTERED + **OWNER DECISION RESERVED** | NONE | **No** | G-MPR-01 §D/§F/§G; OD-G |
| D-GMPR-01-D-D9 | **OD-Q `main` reconciliation = mandatory future gate before production.** Reconcile authoritative history with `main`; establish trustworthy release branch/lineage; preserve governance/merge provenance; no uncontrolled rebase/squash/history replacement; release automation must not use stale `main`. MUST precede real production release; does NOT block P8-I3; not executed now (no `main` merge/push/branch here). | REGISTERED (future gate) | NONE — LEVEL 1 | **No** | OD-Q; G-MPR-01 §S; F17 |
| D-GMPR-01-D-D10 | **Governance hygiene (scoped).** Correct only material readability contradictions; preserve history. Corrected here: stale pinned tip → `d37caef`; CAP range (D6); stale "Active contract" header still labeled D-P6-18 → current-truth pointer. Registered-as-known append-only staleness (preserved): §5 CLOSED-vs-not-complete + Phase-6 lane wordings; stale P4-1a template tail; runtime "deferred to Phase 6" comment (re-homed by D4). | REGISTERED + scoped correction | NONE | **No** | G-MPR-01 §Q; F10–F14/F16 |

**Effect.** With D1 (P8-I1 formally closed), D2 (P8-I3 persistence rule), and D3–D10 (findings durably registered), the three
required P8-I3-entry governance changes are satisfied. **`P8-I3 — Subscription Lifecycle` is ELIGIBLE FOR OWNER CONSIDERATION —
NOT AUTHORIZED / NOT STARTED** (a separate Owner-authorized P8-I3 bounded implementation-contract gate is required; eligibility
≠ authorization). Phase 8 OPEN; P8-I4 / P8-CLOSE NOT STARTED; Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED;
public paid activation / production BLOCKED / NOT AUTHORIZED. All production blockers (Phase-10 legal/readiness, PSRR = GO/PASS,
Deployment Gate, explicit Owner deployment authorization) preserved and unweakened.

**Substance (D-GMPR-01-D-D4 — Amendment 01 — scope-meaning clarification; clarifying-only; NON-ACTIVATING; same decision identity).**
Bounded governance-only amendment extending the existing canonical owner `D-GMPR-01-D-D4` per D-FPC-MAP-06 — it creates
**no new gate, no new canonical owner, no second Owner-decision identity, no new workstream/roadmap/tracker, and no
competing composition authority**. Basis: a read-only repository-first discovery established the Owner's cross-domain
engineering-compatibility intent as `ALREADY RECORDED — PARTIALLY COVERED` with `D-GMPR-01-D-D4` as canonical owner.

**A. Core scope meaning (clarified, not broadened).** D4's registered "shared-constraint propagation; conflicts;
trade-offs; unified assessment" **includes governed system-level engineering compatibility across the participating
domains** — evaluating whether the participating engineering domains are mutually compatible as ONE product/system —
**not merely detecting that multiple domains are present** in one invention.

**B. Per-domain PASS ≠ system-level PASS.** Individually acceptable specialist-domain outputs do **NOT** automatically
imply that the combined product/system is acceptable. Future D4 must **surface** cross-domain incompatibility,
unresolved subsystem/interface assumptions, dependency inconsistencies, contradictions, system-level conflicts,
unowned/orphan requirements (requirements assigned to no participating subsystem/domain), and explicit Known Unknowns —
rather than silently treating independent per-domain PASS states as a system-level PASS (consistent with the already
registered "no silent cross-domain truth overwrite").

**C. Considered where applicable (semantic classes, requirement level only):** cross-domain constraints;
subsystem/interface assumptions; dependency consistency; contradiction detection; shared constraints; unowned or orphan
requirements; engineering-interface verification; system-level conflicts; explicit Known Unknowns; and matters
requiring later simulation, prototype, laboratory testing, certification, or specialist review.

**D. Illustrative examples — ILLUSTRATIVE ONLY, NON-EXHAUSTIVE, NON-BINDING.** These preserve the Owner's intended
meaning and **MUST NOT be read as a frozen checklist, fixed rules, or the future D4 contract's scope**: electrical
power/current/voltage capability versus mechanical load/demand; dimensional, packaging, weight, mounting, or
physical-fit compatibility; thermal limits across subsystems; sensor/control-loop timing compatibility;
communication/data-rate/latency assumptions; hardware/software interface compatibility; material/environmental
assumptions; one discipline depending on an assumption contradicted by another; safety requirements or constraints
conflicting across disciplines; requirements not assigned to any participating subsystem/domain; and
manufacturing/assembly implications created by cross-domain choices.

**E. Truthful limitation (no correctness guarantee).** D4 does **NOT** guarantee a defect-free design or manufactured
product. Its purpose is to **reduce the chance that a major/root engineering incompatibility goes unnoticed** merely
because each specialist domain independently produced an acceptable result. Where evidence cannot be established in
software, future D4 must preserve truthful Known-Unknown status and route to the separately governed physical-validation
paths (WS-PFV-001 lineage: simulation / prototype / laboratory / certification / specialist review) instead of asserting
system-level acceptability.

**F. Five-way distinction preserved (extends the registered tri-distinction; collapses nothing):** domain
**recognition** ≠ domain **qualification** (per-domain P9-QS) ≠ domain **activation** (§5-I2) ≠ **cross-domain
evaluation/composition** (D4) ≠ **prototype/simulation/laboratory/certification/specialist validation** (WS-PFV-001
lineage). Supporting owners (§5-I3 subsystem-model foundation; the P9-QS D4 placeholder / composition-authority
separation; WS-PFV-001) remain unchanged, un-absorbed, and non-owning.

**G. Future extensibility.** The future composition model must **not** assume only the currently known domains: future
specialist domains and technologies must be able to participate in the **same governed composition model** without core
redesign and without domain-specific hardcoding becoming the composition authority.

**H. No implementation architecture defined.** This amendment stays at the requirement/semantic level. It commits **no**
implementation mechanism and **no** pipeline shape (in particular, no `Specialist Domain Analysis → Canonical Domain
Outputs → Cross-Domain Review → System Result` pipeline — that shape is not authoritative repository truth and is not
made so here). Architecture is decided only at the future, separately governed D4 contract/implementation gates.

**I. Non-effects (all preserved verbatim).** D4 remains **REGISTERED (future gate) / NOT AUTHORIZED**; its sequencing is
unchanged (after Phase-9 activation maturity / ≥2 activated domains, or as a governed successor to skipped §5-I4; not
before P8-I3); it remains a separately governed future gate. This amendment authorizes **NO** D4 implementation, **NO**
domain registration or activation (including `mechanical`), **NO** `iot_electronics` change (D-GMPR-01-D-D8 guard
untouched; D8 Owner-reserved), **NO** Phase 10, **NO** PSRR execution, and **NO** deployment. It is **NOT** a
prerequisite expansion: it adds **no new blocker** to, and does not delay or absorb, the Phase-9 next-domain decision or
Mechanical P9-QS qualification, and it leaves CF-6, CF-2, and the `path_n_questions` D-GMPR coupling in their existing
lanes. First new-domain activation remains BLOCKED behind its existing, unchanged prerequisites.

## P8-I3-C — Subscription Lifecycle Contract (CORRECTED — verdict-B remediation; supersedes `ead186d`; contract candidate; no new accepted decision; lifecycle Owner decisions remain OPEN)

Governance/documentation-only **corrected** contract candidate; base `0a19daf74c344f2f497ccebac2440dd1f9d42b2d` (PR #422).
Canonical record: `docs/governance/PHASE_8_I3_SUBSCRIPTION_LIFECYCLE_INCREMENT_CONTRACT.md`. **Supersedes the prior candidate
`ead186d88747a33ff04d69768041efdcb51615bb`** (independent review verdict **B — ACCEPT WITH REQUIRED PRE-MERGE CORRECTIONS**;
**INVALIDATED / NOT MERGEABLE / EVIDENCE-ONLY / NOT MERGED**; review history preserved). Corrections: **RC-1** `none`
entitlement-neutral (no silent legacy downgrade — TECHNICAL BACKWARD-COMPATIBILITY RULE, not commercial policy); **RC-2**
canonical `past_due` exits (`subscription_expired`/`subscription_cancelled`; grace-exhaustion = reason field); **RC-3** unique
cancellation-request mapping (`subscription_change_scheduled` = PLAN changes only, no aliasing); + due-scheduled-transition
materialization and equal-`effective_at` tie-break clarifications. **This register entry records NO new accepted Owner
decision** and **does not duplicate P8-C §8** — it enumerates the still-OPEN lifecycle Owner decisions and the non-commercial
TECHNICAL SAFETY / BACKWARD-COMPATIBILITY defaults. **DOCUMENTED NO-VALID-RED — CONTRACT-CORRECTION-ONLY GATE.** P8-I3 remains
NOT STARTED / NOT IMPLEMENTED / NOT AUTHORIZED; no provider selected.

| Item | Status | Impl. authority | Source |
|---|---|---|---|
| P8-I3-C corrected contract candidate (lifecycle state model + additive persistence + entitlement/quota/account boundaries + provider-neutral event boundary) | CONTRACT CANDIDATE (definition only); supersedes `ead186d` (evidence-only) | **NONE** (separate Owner-authorized P8-I3 implementation gate required) | P8-I3-C record; P8-C §6; G-MPR-01-D D2 |
| Cancellation timing (immediate vs period-end), grace length & during-grace entitlement, proration, downgrade/upgrade effective timing, trial availability/duration, grandfathering, over-limit-on-downgrade behavior | **OPEN — REQUIRED OWNER/BUSINESS DECISION** (subordinate to P8-C §8; not duplicated) | NONE | P8-I3-C §9; P8-C §8 |
| Payment-provider selection | **OPEN** (P8-I4 boundary; not selected) | NONE | P8-I3-C §8/§15; P8-C §6 |
| TCR-0 (`none` = existing P8-I1 entitlement preserved; no silent downgrade) + TSD-2…5 (past_due retains until explicit effective transition; cancellation defaults to requested/scheduled effective; over-limit-on-downgrade = preserve+block-new; terminal canceled/expired never block existing-data read/export/delete) | **RECORDED — NOT COMMERCIAL POLICY** (non-destructive / no-lockout / backward-compatible technical defaults; Owner sets actual policy) | NONE | P8-I3-C §6/§9 |

**Boundary.** This entry authorizes no implementation, starts no increment, selects no provider, and weakens no production
block. Owner business policy (P8-C §8 + the lifecycle refinements above) remains unresolved and must not be silently decided by
the technical implementation. Public paid activation / production remain BLOCKED / NOT AUTHORIZED.

## P8-I4-C — Payment Provider Boundary Contract (contract candidate; no new accepted decision; provider selection + commercial decisions remain OPEN)

Governance/documentation-only contract candidate; base `f66ea96c77e64deea8ebc1b4bb9766df985e703e` (PR #425). Canonical record:
`docs/governance/PHASE_8_I4_PAYMENT_PROVIDER_BOUNDARY_INCREMENT_CONTRACT.md`. **This register entry records NO new accepted
Owner decision** (a contract candidate carries none) and **does not duplicate P8-C §8 / P8-I3-C §9** — it registers, truthfully,
the OPEN provider-selection dependency and the OPEN commercial decisions the technical provider-boundary contract deliberately
does **not** decide. **DOCUMENTED NO-VALID-RED — CONTRACT-ONLY GOVERNANCE GATE.** P8-I4 remains NOT STARTED / NOT IMPLEMENTED /
NOT AUTHORIZED; **no payment provider selected**. P8-I4 (commercial payment-provider boundary) is DISTINCT from CAP-15 AI
Provider Abstraction (G-MPR-01-D D7).

| Item | Status | Impl. authority | Source |
|---|---|---|---|
| P8-I4-C contract candidate (provider-neutral port + adapter boundary + canonical mapping + additive mapping/dedupe persistence + authenticity/secrets boundary + strict provider-event idempotency + atomicity + replaceability) | CONTRACT CANDIDATE (definition only) | **NONE** (separate Owner-authorized P8-I4 implementation gate required; starting with the fake/reference-adapter P8-I4-I1) | P8-I4-C record; P8-C §6; P8-I3-C |
| **Payment-provider selection** (Stripe / Paddle / PayPal / Apple / Google / other) | **OPEN — REQUIRED OWNER DECISION**; **NO provider selected**; registered as a **prerequisite for real (non-fake) adapter work** | NONE | P8-I4-C §10/§18 |
| Marketed plan names; prices; currency; billing cadence; trial; grace; proration; refunds; tax/jurisdictions; cancellation timing; grandfathering; enterprise billing; over-limit-downgrade; invoice requirements; payment methods; dunning | **OPEN — REQUIRED OWNER/BUSINESS DECISION** (subordinate to P8-C §8 / P8-I3-C §9; not duplicated) | NONE | P8-I4-C §18; P8-C §8 |
| Strict provider-event idempotency (conflicting duplicate payload fails closed) | **RECORDED — TECHNICAL BOUNDARY DECISION (not commercial policy)**; resolves the P8-I3 idempotency-payload non-blocking observation for provider events | NONE | P8-I4-C §7 |

**Boundary.** This entry authorizes no implementation, starts no increment, selects no provider, integrates no provider, and
weakens no production block. Real-provider work is BLOCKED pending a separate Owner provider-selection decision. Public paid
activation / production remain BLOCKED / NOT AUTHORIZED.

## P8-I4 formal closure + `P8-AF` mandatory-obligation registration (increment closure records no new commercial decision; the P8-AF mandate is a genuinely-absent explicit Owner direction — NON-ACTIVATING)

Registered by the OWNER-AUTHORIZED governance-only **P8-I4-CLOSE** gate; base `3a802fd84055f475feafcd55893da301af45c67d`
(PR #427; parents `fccd895` + `6f83e496…`; tree `191709299…`). Canonical records:
`docs/governance/P8_I4_PAYMENT_PROVIDER_BOUNDARY_FORMAL_CLOSURE_RECORD.md` and
`docs/governance/P8_AF_ACCESS_LICENSING_ORGANIZATION_FOUNDATION_OBLIGATION.md`. **The P8-I4 increment closure records NO new
accepted Owner commercial decision** (consistent with the P8-I1/I2/I3 increment-closure precedent — evidentiary closure leaves
the ODR's commercial rows unchanged; provider selection and all commercial policy remain OPEN under the P8-I4-C / P8-I3-C
entries above). This entry records ONLY the **genuinely-absent, explicit Owner direction** that a separate Phase-8
architectural-foundation obligation, **`P8-AF` — Access, Licensing & Organization Foundation**, is **mandatory before
`P8-CLOSE`**, and its **directional / NON-ACTIVATING** future-readiness preferences. **DOCUMENTED — GOVERNANCE-ONLY
REGISTRATION; NO IMPLEMENTATION AUTHORITY; NO ACTIVATION.**

| Item | Status | Impl. authority | Source |
|---|---|---|---|
| **P8-I4 — Payment Provider Boundary** (P8-I4-C contract merged PR #426; P8-I4-I1 implementation review verdict A, merged PR #427, post-merge verified) | **FORMALLY CLOSED** (increment closure only; authoritative if/when this governance candidate is merged) | NONE | P8-I4 closure record; roadmap P8-I4-CLOSE entry |
| P8-I4-I2 (verified webhook ingestion) / P8-I4-I3 (reconciliation) / real-provider integration | **NOT TRIGGERED / DEFERRED / NOT STARTED** (evidence-triggered; a deferred lane is not unfinished mandatory work) | NONE | P8-I4-C decomposition; closure record §6 |
| **Payment-provider selection** (Stripe / Paddle / PayPal / Apple / Google / other) | **OPEN — REQUIRED OWNER DECISION**; NO provider selected (unchanged) | NONE | P8-I4-C §10/§18 |
| Real payment collection | **NOT ACTIVATED** | NONE | P8-I4 closure record §7 |
| **`P8-AF` — Access, Licensing & Organization Foundation** = **mandatory Phase-8 foundation gate before `P8-CLOSE`** (explicit Owner direction; genuinely absent before this entry) | **REGISTERED / REQUIRED / NOT IMPLEMENTED / NOT ACTIVATED / NOT STARTED** | NONE (next gate is `P8-AF-C` — contract first) | P8-AF obligation record; this gate |
| `P8-AF` core principle — **Authentication ≠ Authorization ≠ Account identity ≠ Data ownership ≠ Commercial entitlement ≠ Subscription lifecycle ≠ Payment state ≠ Billing ownership**; **paying ≠ owning user data** | **RECORDED — BINDING ARCHITECTURAL PRINCIPLE (not commercial policy)** | NONE | P8-AF record §2 |
| `P8-AF` directional preferences — **7-DAY** (NOT 14) per-account trial preserving durable data on trial→paid; **automatic day-7 hard deletion NOT authorized** (separate retention policy); trial 168h-vs-calendar semantics **OPEN**; **global configurable promotional free access** administrable **without a source-code change**; **Owner/Admin non-billed access** as explicit auditable authorization→entitlement (no bypass); **organization/named-seat licensing** with billing-ownership ≠ data-ownership and safe seat reassignment; enterprise/custom compatibility; deterministic **access-resolution precedence**; safe **quota composition** (P8-I2 sole quota authority); **no second lifecycle machine** (P8-I3 canonical; D-FPC-MAP-06) | **REGISTERED — NON-ACTIVATING future-readiness DIRECTION; NO commercial policy / price / provider / schema decided** | NONE | P8-AF record §3–§5 |

**Boundary.** This entry authorizes no implementation, starts no increment, selects/integrates no provider, activates no
trial / promotional / Owner-Admin / organization / enterprise access, creates no role/organization/seat/campaign schema, sets
no trial-duration constant, implements no automatic trial-data deletion, and weakens no production block. `P8-AF` /
`P8-AF-C` / `P8-CLOSE` — NOT STARTED. Phase 8 remains OPEN / NOT CLOSED. Phase 9 / Phase 10 — NOT AUTHORIZED; PSRR EXECUTION —
NOT STARTED; public paid activation / production — BLOCKED / NOT AUTHORIZED. Prior ODR rows and evidence are unchanged; the
still-OPEN commercial/provider decisions remain governed by the P8-I3-C / P8-I4-C entries above.

---

## CF5-F002 / CF-6 — Bounded Web `/start` Multi-Domain Consent/Admission Policy (pre-trigger corrective prerequisite)

Governance/documentation-only registration of a bounded Owner decision needed to freeze the CF5-F002 / CF-6 pre-trigger corrective
implementation contract. Canonical evidence: `docs/governance/CF5_F002_CF6_WEB_ADMISSION_CORRECTIVE_CONTRACT.md` and the CF5-F002
independent validation record `docs/governance/CF5_F002_WEB_START_ADMISSION_INDEPENDENT_VALIDATION_RECORD.md` (PR #452). **Scope
guard:** this resolves ONLY the bounded `/start` consent/admission behavior required for the pre-trigger correction; it authorizes
**no** general multi-domain orchestration, **no** domain selection/registration/activation, **no** D4, **no** D8, and **no** unrelated
UX expansion. It does **not** rewrite or erase the earlier decisions that deferred multi-domain consent/admission (**OD-F/G/H**,
**D-P6-03/06/15**, **D-S5-04**) — those remain historically valid; this decision supplies the narrow policy they explicitly left to
the pre-trigger gate.

| ID | Subject | Status | Impl. authority | Blocks first new-domain activation? | Evidence |
|---|---|---|---|---|---|
| D-CF5-F002-01 | **Bounded multi-domain `/start` consent/admission policy.** **D1 — consent model = "Confirm classifier-selected domain":** when the canonical classifier resolves exactly one **activated** specialist domain, `/start` presents that domain, the user explicitly confirms/declines, no auto-admit, and the persisted session-domain equals the classified+confirmed domain; no manual selection when the classifier already resolved one valid activated domain; `AMBIGUOUS_TIE` fail-closed unless separately governed. **D2 — NONE under multi-domain activation = "Require explicit user choice":** when classification is `NONE` and **>1** specialist domain is activated, present only currently activated domains, the user explicitly chooses one and confirms, persist chosen+confirmed; **no silent Electronics/default fallback**. **Backward compatibility:** under `['electronics_electrical']`, preserve the current governed `NONE`→Electronics explicit-consent behavior unchanged. **D3 (mechanical consequence, not a new decision):** Electronics-absent activation derives behavior from the canonical activated-domain set — no Electronics special case, no accidental `DomainNotActivatedError`/HTTP 500. **Derived corner:** `NONE` with exactly one activated domain (any) → offer that sole domain under explicit consent (domain-neutral generalization of today's behavior). | **ACCEPTED — bounded consent/admission policy for the CF5-F002/CF-6 pre-trigger corrective contract** (authoritative if/when this governance candidate is independently reviewed, Owner-accepted, merged, and post-merge verified) | NONE (contract-only; the corrective **implementation** is a separate later gate) | **Yes** — the CF5-F002/CF-6 corrective implementation is a mandatory pre-trigger prerequisite before `activated_domains() != ['electronics_electrical']` | `CF5_F002_CF6_WEB_ADMISSION_CORRECTIVE_CONTRACT.md` §2; validation record; D-GMPR-01-D-D3 |

**Boundary.** This entry records a bounded consent/admission product policy and authorizes no implementation, no runtime/Web/test
change, no domain selection/registration/activation, no D4/D8, and no CF5-F002 / CF-6 / CF-2 / CF-5 closure. It is a bounded portion
of the mandatory Pre-Phase-9 Core Domain-Neutrality gate **D-GMPR-01-D-D3** (the Web-admission literals), and does not discharge that
gate's other couplings (`engine/safety_signal.py` = CF5-F001; `engine/path_n_questions.py`; hard-coded tie-break = CF5-F004/CF-3).
`activated_domains() == ['electronics_electrical']`; first new-domain activation remains BLOCKED.

---

## CF5-F004 — Non-Activated Fallback Extensibility Policy (pre-trigger corrective prerequisite)

Governance/documentation-only registration of the bounded Owner decisions needed to freeze the CF5-F004 corrective
implementation contract. Canonical evidence: `docs/governance/CF5_F004_PRIORITY_FALLBACK_CORRECTIVE_CONTRACT.md` §2 and the
merged independent-validation record `docs/governance/CF5_F004_PRIORITY_FALLBACK_INDEPENDENT_VALIDATION_RECORD.md`
(PR #461). **Scope guard:** these decisions resolve ONLY the bounded fallback-extensibility policy required for the
pre-trigger correction; they authorize NO domain registration/activation, NO pack-schema work, NO D4/D8, and NO change to
the closed D3-D / P9-E2 / CF5-F003 / CF5-F002 behavior.

| ID | Subject | Status | Impl. authority | Evidence |
|---|---|---|---|---|
| D-CF5-F004-01 | **Bounded fallback-extensibility policy.** **OD1 — pre-trigger binding (safer sequencing):** F004 remediation MUST be complete before any pack-schema/provenance work whose successful result could change the recognized-registry set (earlier than actual registration). **OD2 — legacy precedence:** current legacy precedence outcomes for the existing four recognized domains (`medical_device > electronics_electrical > mechanical > software`, zero-activated) are preserved — no change to current user-visible classification/guidance flavor; for FUTURE registered domains no new arbitrary winner rule may be invented, and a registered top-scoring domain must never be silently erased or displaced merely because its id is absent from a hardcoded list. **OD3 — CF-3 discharge timing:** CF-3 and the D-GMPR-01-D-D3 hard-coded tie-break coupling discharge only at eventual F004 formal closure. | **ACCEPTED — bounded policy for the CF5-F004 corrective contract** (authoritative if/when this governance candidate completes the review/acceptance/merge lifecycle) | NONE (contract-only; the corrective implementation is a separate later gate with ZERO ODR diff) | Contract §2; validation record §10 |

**Boundary.** This entry records bounded policy and authorizes no implementation, no runtime/test change, no domain
registration/activation, no pack-schema work, and no CF5-F004 / CF-3 / CF-5 / CF-6 / CF-2 closure.
`activated_domains() == ['electronics_electrical']`; first new-domain activation remains BLOCKED.

---

## P9-MECH-QC — Mechanical Domain Selection & P9-QS Qualification Contract (selection recorded inside the contract gate)

Governance/documentation-only registration recorded by the Mechanical P9-QS Qualification Contract gate (canonical
record: `docs/governance/P9_MECHANICAL_DOMAIN_QUALIFICATION_CONTRACT.md`; base `c4abe0207c34f15e89438cc931c114db9d2e6225`).
Per repository precedent (D-CF5-F002-01 / D-CF5-F004-01), the Owner decision is recorded inside the contract gate that
operates under it — **no standalone selection gate exists or is implied**. **Scope guard:** this decision authorizes
Mechanical qualification planning/governance ONLY; it authorizes NO qualification completion, NO activation, NO domain
registration, NO recognized-registry change, NO D4 execution, NO D8, NO CF-6/CF-2/D-GMPR closure, NO Phase 10, NO PSRR,
NO deployment.

| ID | Subject | Status | Impl. authority | Evidence |
|---|---|---|---|---|
| D-P9-MECH-01 | **Phase-9 next-domain selection: `mechanical`.** The Owner SELECTS `mechanical` (an ALREADY-RECOGNIZED §5-I1 pack) as the next specialist domain to pursue through Phase-9 P9-QS qualification. **Binding separations:** selection ≠ qualification (this decision does not declare or schedule qualification completion); qualification ≠ activation (even successful qualification does NOT activate `mechanical`; activation remains a separate, explicitly-Owner-authorized §5-I2 gate behind ALL existing prerequisites — remaining CF-6, CF-2, the open D-GMPR `path_n_questions` coupling, NMF-1/FU-1 disposition, D8 if implicated, and explicit Owner activation authorization); the recognized-registry set is UNCHANGED by this decision. **Extensibility-claim boundary:** a future successful Mechanical qualification proves ONLY qualification-extensibility for an already-recognized domain; it does NOT prove registration-extensibility for future fifth/sixth/new domains — independent future testing of genuinely-new-domain registration extensibility is explicitly preserved. **Preserved boundaries:** D4 REGISTERED / NOT AUTHORIZED (Amendment 01 semantics untouched); D8 Owner-reserved; CF-6 OPEN; CF-2 OPEN; D-GMPR `path_n_questions` coupling OPEN; Phase 10 NOT AUTHORIZED; PSRR NOT EXECUTED; deployment NOT AUTHORIZED. `activated_domains() == ['electronics_electrical']`. | **ACCEPTED — selection + qualification-planning authorization only** (authoritative if/when this contract candidate completes the review/acceptance/merge lifecycle) | NONE (contract-only; every future Mechanical qualification implementation increment requires its own separate explicit Owner authorization) | Contract §2; the read-only sequencing determination preceding this gate |

**Open Owner decision surfaced by this contract (NOT decided here):** **OD-M2** — safety-cue-family timing for
Mechanical qualification: (a) governed Mechanical safety-cue family REQUIRED before qualification; (b) qualification may
complete with the truthful empty-family state but a governed family is REQUIRED before activation (the registered
pre-activation input made concrete); or (c) another explicitly governed treatment. Recorded OPEN in contract §11; no
Mechanical qualification declaration may be made until OD-M2 is decided. **[SUPERSEDED — OD-M2 is now RESOLVED by the
Owner as Option B-hardened, Mechanical-specific: see `D-P9-MECH-02` in the P9-MECH-I1 section below. This annotation
changes no history; contract §11's arm (b) is the decided arm, with the three binding hardening clauses recorded in
D-P9-MECH-02.]**

**Boundary.** This entry records the selection decision and authorizes no implementation, no runtime/test/pack/registry
change, no qualification declaration, and no activation. First new-domain activation remains BLOCKED.

---

## P9-MECH-I1 — OD-M2 Resolution + First Mechanical Increment Contract (recorded inside the contract gate)

Governance/documentation-only registration recorded by the P9-MECH-I1 increment-contract gate (canonical record:
`docs/governance/P9_MECH_I1_TRUTHFUL_CAPABILITY_COVERAGE_DECLARATION_CONTRACT.md`; base
`90b1b00f0bd384911735a55340ee15829a77bbad` — PR #467 merge, P9-MECH-QC AUTHORITATIVE). Per repository precedent, the
Owner decision is recorded inside the contract gate that operates under it — **no standalone OD-M2 gate**. **Scope
guard:** this entry resolves ONLY the OD-M2 timing policy and defines the bounded P9-MECH-I1 increment; it authorizes NO
implementation in this candidate (the P9-MECH-I1 implementation requires its own separate explicit Owner authorization),
NO qualification declaration, NO activation, NO registry change, NO safety-family implementation, NO D4/D8, NO
CF-6/CF-2/D-GMPR closure, NO Phase 10 / PSRR / deployment.

| ID | Subject | Status | Impl. authority | Evidence |
|---|---|---|---|---|
| D-P9-MECH-02 | **OD-M2 RESOLVED — Mechanical safety-cue-family timing: Option B-hardened (Mechanical-specific).** A governed Mechanical safety-cue family is **NOT required** for `mechanical` to be declared P9-QS QUALIFIED, PROVIDED ALL of: **(1)** the Mechanical capability and coverage declarations explicitly declare inventor-stated safety-signal derivation **NOT COVERED** pending a governed Mechanical safety-cue family; **(2)** any Mechanical qualification record prominently records the absent family as an outstanding **ACTIVATION BLOCKER** for `mechanical` — no unannotated or misleading "QUALIFIED" claim; **(3)** a governed Mechanical safety-cue family — via the existing `engine/safety_signal.py` F001 per-domain seam, with provenance-tagged hazard vocabulary, focused tests, negative tests, mutation/adversarial tests, and electronics non-degradation evidence — is **REQUIRED and MUST be complete, merged, and post-merge verified BEFORE any Owner activation authorization for `mechanical`** (a separate future evidence-bearing gate; NOT implemented by P9-MECH-I1). **Mechanical-only:** creates/waives/predetermines NO safety-cue-family policy for any other current or future domain; modifies/closes NOTHING of P9-QS, F001, CF-6, CF-2, D-GMPR, D4, D8, Phase 10, PSRR, deployment. | **ACCEPTED — RESOLVED (authoritative if/when this contract candidate completes the review/acceptance/merge lifecycle)** | NONE (policy only; the safety-family gate and P9-MECH-I1 implementation each need separate authorization) | Contract §2; P9-MECH-QC §11; the read-only OD-M2 analysis preceding this gate |

**Boundary.** This entry records the OD-M2 resolution and the increment-contract registration only.
`activated_domains() == ['electronics_electrical']`; Mechanical NOT qualified, NOT activated; first new-domain
activation remains BLOCKED (now explicitly including OD-M2 clause 3 for `mechanical`).

---

## Mechanical Activation Execution Gate — explicit Owner activation authorization (recorded inside this gate)

Governance/documentation-only registration recorded by the Mechanical Activation Execution Gate itself (canonical
record: `docs/governance/MECHANICAL_ACTIVATION_EXECUTION_RECORD.md`; base
`18a97da735e68763c7fab6488613cde1dff4675f` — PR #502 merge, Tier-1 EN/AR Mechanical public label AUTHORITATIVE).
Per repository precedent (`D-P9-MECH-01`, `D-P9-MECH-02`), the Owner decision is recorded inside the gate that
executes under it — no standalone pre-gate. ID follows the existing `D-P9-MECH-<NN>` sequencing (next after
`D-P9-MECH-02`); no new ID format invented.

| ID | Subject | Status | Impl. authority | Evidence |
|---|---|---|---|---|
| D-P9-MECH-03 | **Explicit Owner Mechanical activation authorization — §5-I2 allowlist execution.** The Owner explicitly authorizes activating `mechanical` via the sole canonical §5-I2 mechanism (`engine/domain_activation.py::_ACTIVATED_DOMAINS`), satisfying the last remaining prerequisite named in `D-P9-MECH-01`/`D-P9-MECH-02` ("explicit Owner activation authorization... a separate, explicitly-Owner-authorized §5-I2 gate"). Owner statement (verbatim): "I explicitly approve activation of the Mechanical domain within InventorAI and authorize proceeding to the Mechanical activation execution gate." **Scope guard:** authorizes ONLY the bounded allowlist change (`_ACTIVATED_DOMAINS = frozenset({"electronics_electrical", "mechanical"})`) and its necessary test-suite reconciliation; authorizes NO classifier/admission/scoring/progression/persistence/security/Tier-1-label change, NO third domain, NO D4, NO Phase 10, NO PSRR, NO deployment. Mechanical P9-QS qualification itself remains a SEPARATE, still-unauthorized future gate (activation ≠ qualification, per `D-P9-MECH-01`'s own binding separation, preserved unchanged). *Governance-truth note (added by `D-P9-MECH-04`): the "still-unauthorized future gate" clause in this row's original text was found stale — see `D-P9-MECH-04` below; this row's authorization scope itself is unchanged.* | **ACCEPTED — EXECUTED** (authoritative if/when this candidate completes the review/acceptance/merge lifecycle) | NONE beyond this gate's own bounded scope (any future third-domain activation requires its own separate explicit Owner authorization; see `D-P9-MECH-04` regarding Mechanical P9-QS qualification, which does not require this row to be reopened) | This record; `MECHANICAL_ACTIVATION_EXECUTION_RECORD.md` §1/§4/§5/§13 |
| D-P9-MECH-04 | **Governance-truth clarification of `D-P9-MECH-03` (no new Owner authorization) — Mechanical P9-QS qualification status.** Corrects a stale clause in `D-P9-MECH-03` and in derivative summaries (`ACTIVE_EXECUTION_ROADMAP.md`, `ACTIVE_INCREMENT_CONTRACT.md`, `CURRENT_PROJECT_STATE.md`) asserting Mechanical P9-QS qualification "remains a SEPARATE, still-unauthorized future gate." That clause predates, and did not account for, evidence already merged before `D-P9-MECH-03` was written. Distinguishes three separate facts, none of which alter `D-P9-MECH-03`'s own authorization scope: **(A)** what `D-P9-MECH-03` itself authorized — ONLY the bounded §5-I2 allowlist execution (activation), nothing about qualification; **(B)** what was already independently evidenced BEFORE `D-P9-MECH-03` existed — `P9_MECH_QUALIFICATION_RECORD.md` (commit `dd7b487`) and `P9_MECH_SF_FORMAL_CLOSURE_RECORD.md` (commit `c25c843`) jointly declared `MECHANICAL = P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS`, naming exactly six named activation blockers; **(C)** what is true now — all six named blockers are independently confirmed discharged (Mechanical safety-cue family; Tier-1 EN/AR public label, commit `e635c9f`; CF-6 full-scope closure; CF-2 full-scope closure; NMF-1+FU-1 test hardening; and `D-P9-MECH-03` itself as the sixth, explicit Owner activation authorization), so on the live activated runtime Mechanical qualification is **SATISFIED**, per P9-QS's own binding separations in `P9_QS_PHASE_9_TECHNICAL_QUALITY_STANDARD_CONTRACT.md` §2 (activation and qualification are distinct, and neither retroactively creates the other). This clarification implies NO new implementation, NO retroactive broadening of `D-P9-MECH-03`'s authorization, NO Phase 9 closure, NO Phase 10 authorization, NO PSRR, NO deployment. Full basis: `MECHANICAL_P9QS_QUALIFICATION_STATUS_RECORD.md`. | **CLARIFIED — GOVERNANCE-TRUTH CORRECTION** (no new Owner authorization event; corrects a factual/currency defect in prior governance text only) | NONE (governance/documentation-only; does not authorize implementation, activation, third-domain composition, Phase 10, PSRR, or deployment) | This record; `MECHANICAL_P9QS_QUALIFICATION_STATUS_RECORD.md`; `P9_MECH_QUALIFICATION_RECORD.md`; `P9_MECH_SF_FORMAL_CLOSURE_RECORD.md`; `MECHANICAL_ACTIVATION_EXECUTION_RECORD.md` |

**Boundary.** `activated_domains() == ['electronics_electrical', 'mechanical']` (real, verified live). Mechanical
P9-QS qualification is SATISFIED on the live activated runtime, per `D-P9-MECH-04` (governance-truth
clarification; no new Owner authorization). Phase 9 remains OPEN (qualification of one domain does not close
Phase 9; a Remaining-Obligation / Exit-Criteria Review remains the next gate). Phase 10 / PSRR / deployment
remain NOT AUTHORIZED. D4 / D8 unaffected.

---

## THERM — Future Thermal Capability Preservation (Owner-directed register amendment; recorded inside this gate)

Governance/documentation-only registration on base `f7ed74484234ae1e85f3db35ebfac7ebeb847288` (P9-MECH-I1
implementation merged and post-merge verified; Mechanical NOT qualified / NOT activated). Canonical substance:
`docs/governance/INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md` section **`THERM-01`** (Owner-approved R7 amendment;
deliberately NON-NUMERIC designation so no pre-existing numeric register cross-reference — including the six
historical CAP-12/CAP-13/CAP-14 section-6 feasibility-gate references, left byte-untouched — can resolve to it; NO new
CAP entry — CAP-01…CAP-18 unchanged per D-GMPR-01-D-D6). A prior candidate `247cb6b9b4c311c3f42b78e3030c049d86b70229`
was independently REJECTED for a section-designation collision (its `§6` heading silently captured those historical
references) and is preserved as immutable rejected evidence; this candidate is a fresh correction from the same
authoritative parent with the reviewed substantive content preserved. **Scope guard:** anti-forgetting registration
only; authorizes NO thermal implementation, NO solver/CFD/FEA work, NO Mechanical qualification/activation, NO
registry/pack/runtime change, NO CF-6/CF-2/D-GMPR closure, NO D4/D8, NO Phase 10 / PSRR / deployment.

| ID | Subject | Status | Impl. authority | Evidence |
|---|---|---|---|---|
| D-THERM-01 | **Future Thermal Analysis / Thermal Simulation Capability — governed future path preserved (anti-forgetting).** The truthful P9-MECH-I1 NOT-COVERED thermal exclusion MUST NOT become an accidental permanent omission. **Four-way distinction preserved (never conflated):** (1) thermal consideration/advisory — existing owner **CAP-13** (heat assumption inputs; Heat-and-pressure warning category; `UNABLE TO RECOMMEND`), consumer only, never a solver; (2) **thermal analysis** (heat-generation/heat-transfer reasoning; temperature-rise/thermal-margin estimation) — producer capability owned by NO existing record, preserved as a future feasibility subject riding the existing P9-QS §13 deterministic-calculation adapter gate lineage + §12 units integrity (no second calculation framework; §1A exclusion 2's narrow-bounded-deterministic rule stands); (3) **thermal simulation** (CFD/conjugate/spatial/transient) — REMAINS inside the §1A legacy exclusions as a risk control, excluded by default; §1A already carried a GENERIC revisit permission (separate evidence + contract + owner authorization), and D-THERM-01 adds the EXPLICIT thermal-specific preservation/feasibility path through which alone that permission may ever be exercised for thermal simulation, preserved as a feasibility question DISTINCT from analysis; (4) physical validation — existing owner **WS-PFV-001** (software-evidence producer vs physical validator never merged). **Consumers referenced, nothing absorbed:** CAP-13 advisory consumer; CAP-12 materials/manufacturing/prototype consumer; **D4** eventual system-level cross-domain consumer/coordinator (referenced only; NOT AUTHORIZED); ADR-002's `THERMAL_MANAGEMENT` noted as a future gap-taxonomy concept only — NOT a thermal-analysis owner. **Truthfulness binding:** current InventorAI performs NO governed thermal simulation/analysis/prediction; registration creates no runtime capability, qualifies nothing, activates nothing; no thermal result may be presented as certified engineering truth without future evidence/validation; no CFD/FEA/solver implied. **Mandatory future thermal feasibility/contract gate** (method class; problem classes; inputs; units; property sources incl. licensing; boundary conditions; coefficients; geometry; uncertainty; validation datasets; error bounds; specialist review; regulatory/safety; CFD-justification; cost; external-tool security; UNABLE-TO-DETERMINE behavior) required before ANY implementation; no architecture pre-authorized. | **ACCEPTED — Owner-directed registration (authoritative if/when this candidate completes the review/acceptance/merge lifecycle)** | NONE | Register THERM-01 section; P9-MECH-I1 declaration; P9-QS §12/§13; CAP-12/CAP-13; WS-PFV-001; D-GMPR-01-D-D4 Amendment 01; ADR-002 |

**Boundary.** `activated_domains() == ['electronics_electrical']`; Mechanical NOT qualified / NOT activated; first
new-domain activation remains BLOCKED. This entry authorizes no implementation of any kind.

---

## CF-6 / CF-2 — ILT-002 Fixed-Domain Protocol Decision (resolves the reconstruction-flagged classifier-consistency ambiguity)

Governance/documentation-only registration of the Owner's explicit decision resolving the ambiguity flagged by
`docs/governance/CF6_CF2_ILT002_FACET_RECONSTRUCTION_AND_CORRECTION_RECORD.md` (merge
`6524e792786644d3053aeac650bdfa7888ad0653` → `0587c7b6` → PR #489, authoritative tip
`3570863ef9519f123c76fb1f165452e4935365e3`): that record's mandatory hidden-surface sweep found the three
`start_ilt002_*` legacy routes' hardcoded `electronics_electrical` domain selection is governed, intentional, and
tested (`tests/test_web_app.py::test_governed_ilt002_routes_remain_electronics_pinned_after_restriction` and its
companion pin) — but stopped short of implementation, determining that any further ILT-002 gate required an
explicit Owner decision on whether that fixed-domain design should ever change. **Scope guard:** this entry
resolves ONLY the narrow question the reconstruction record raised — whether ILT-002 domain-selection is a
classifier defect requiring remediation. It authorizes **no** implementation, **no** runtime/Web/CLI/test/domain/
activation/schema/persistence change, **no** E-2 tooling change, **no** Mechanical activation, **no** Tier-1
label work, and **no** global closure of CF-6 or CF-2 (each remains OPEN — see Boundary).

| ID | Subject | Status | Impl. authority | Evidence |
|---|---|---|---|---|
| D-CF6CF2-ILT002-01 | **ILT-002 fixed-domain design is a governed protocol invariant, not a classifier defect.** The Owner decides: **(1)** the three `start_ilt002_*` routes remain intentionally fixed-domain scenario/evidence routes; **(2)** their hardcoded `electronics_electrical` domain selection is a governed protocol invariant, not a classifier defect — it is NOT to be treated as CF-6 technical-remediation debt; **(3)** they continue to pass through canonical activation enforcement via `_admit_specialist_domain()` (`domain_activation.is_activated`) exactly as today, unchanged; **(4)** no classifier-driven routing is to be introduced into these routes unless a future explicit Owner decision changes the protocol itself; **(5)** no duplicate activation checks are to be added to them; **(6)** existing ILT-002 evidence-ledger semantics, the separate Owner-authorized E-2 Path N smoke-evidence procedure (`scripts/e2_path_n_smoke_runner.sh`), and all current persistence meaning (the durably-stored `confirmed_domain`, downstream NB-R1 cold-load restoration, and the domain-specific question-text pin) are preserved unchanged; **(7)** the prior CF-6 ambiguity over whether ILT-002 must classify submitted text is RESOLVED in favor of the fixed-domain protocol — the ILT-002 classifier-remediation item is narrowly removed from CF-6's technical-remediation list (nothing else in CF-6's open-ended remainder is affected); **(8)** this decision does NOT globally close CF-6, does NOT globally close CF-2, does NOT waive CF-6's unrelated remainder, does NOT waive CF-2's Arabic-localization or non-`/start` public-message remainder, does NOT activate Mechanical, does NOT authorize Tier-1, and does NOT close Phase 9. **CF-2 residual preserved, not discharged:** the independent-review-identified question — whether a generic session/public label could display "electronics" for arbitrary text posted to an unlinked fixed-domain route — remains an OPEN question for CF-2's own future full-scope/public-message sweep; this decision does not answer it and does not claim it is resolved. | **ACCEPTED — RESOLVED (authoritative if/when this governance candidate completes the review/acceptance/merge lifecycle)** | NONE (decision-only; any future ILT-002 protocol change requires its own separate explicit Owner authorization and its own governed implementation gate) | `CF6_CF2_ILT002_FACET_RECONSTRUCTION_AND_CORRECTION_RECORD.md` §3/§9 (the reconstruction that raised this question); `tests/test_web_app.py::test_governed_ilt002_routes_remain_electronics_pinned_after_restriction`; `web/app.py::_admit_specialist_domain`; D-S5-03 |

**Boundary.** `activated_domains() == ['electronics_electrical']`; Mechanical NOT qualified / NOT activated; first
new-domain activation remains BLOCKED. **CF-6 remains OPEN** — narrowed by removing the ILT-002 classifier-
remediation item, but not closed: its open-ended "full stated scope" confirmation (per the CF-5 Audit contract
§13) is unaffected and still requires CF-6's own future closing gate. **CF-2 remains OPEN** — the ILT-002 route-
copy item stays under CF-2's residual list pending the truthfulness question above; Arabic localization and the
non-`/start` template sweep are entirely untouched. This entry authorizes no implementation of any kind.

## Phase 10 — Jurisdiction & Data-Rights owner decisions OD-J1 / OD-J2 (ACCEPTED; recorded under the merged P10 gate)

Accepted under the authoritative `P10_JURISDICTION_AND_DATA_RIGHTS_OWNER_DECISION_GATE.md` (merged PR #514,
tip `022e5b75cb0e7bc9ee248f20aed5df7da1368989`), which had registered both as unresolved. **Identifier
disambiguation:** these Phase-10 Jurisdiction & Data-Rights decisions **OD-J1 / OD-J2 are distinct from the
earlier Phase-1 accepted decision OD-J** ("Product role model", row above); the historical Phase-1 decision is
not modified. **OD-DR1, OD-DR2, and OD-CJ1 remain REGISTERED AND UNRESOLVED** in the P10 gate; OD-A continues
to govern the brand/name dependency.

| ID | Subject | Status | Phase/WS | Impl. authority | Evidence |
|---|---|---|---|---|---|
| OD-J1 | **Launch markets / user-residence and user scope** — GCC-first commercial *marketing* sequencing only; **NOT geo-restricted at launch**: users outside the GCC may access, register, and use the product from launch (subject only to later lawfully-required restrictions established through separate legal/governance processes); intended usable worldwide (GCC, Middle East, Europe, Asia, Africa, North America, South America, Oceania); intended for both INDIVIDUAL and INSTITUTIONAL use (public, inventors, researchers, students, companies, universities, authorities, institutions, organizations) — product/market intent only, NOT a legal clearance conclusion, and NO institutional tenancy/enterprise-administration/organizational-contract/B2B/institutional-pricing/compliance feature is activated. Canonical statement: *GCC-first commercial marketing; globally open user availability from launch; global-ready product from the outset.* | ACCEPTED | Phase 10 | NONE | phase10_owner_decisions/OD-J1_OD-J2_JURISDICTION_AND_HOSTING.md |
| OD-J2 | **Hosting / data-location strategy** — *minimum practical infrastructure now, clean expansion seams later*: may begin with a practical single production hosting region; architecture must preserve future flexibility (provider migration, additional regions, regional data residency, jurisdiction-driven or customer-specific hosting, global expansion) and avoid permanent coupling to one provider/region/country/jurisdiction-specific storage assumption. **NOT decided:** any provider (AWS/Azure/Google Cloud/other) or any production region (Bahrain/UAE/Saudi Arabia/Europe/US/other) — initial provider+region selection is **DELEGATED TO A LATER, SEPARATELY AUTHORIZED INFRASTRUCTURE GATE** (an accepted delegation, not an ambiguity). GCC-focused rollout does NOT mean GCC hosting; no data-location commitment inside or outside the GCC is made. "Global-ready" does NOT mean multi-region/active-active/sharding/multi-provider now — avoid architectural foreclosure without over-engineering the first release. | ACCEPTED AT STRATEGY LEVEL | Phase 10 | NONE (infrastructure gate separately authorized) | phase10_owner_decisions/OD-J1_OD-J2_JURISDICTION_AND_HOSTING.md |

**Legal boundary.** OD-J1/OD-J2 are business/product/technical intent for later legal analysis; they decide NO
privacy-regime applicability (GDPR / any GCC or other national PDPL / EU or other law), no lawful basis, no
consent/cookie requirement, no retention/erasure/portability requirement, and no tax treatment — all remain
subject to the gate's external legal-input register. **D3b stat correction carried in this same candidate:**
the previously recorded P10-D3b diff stat `+487/-1` is superseded by the repository-verified `+487/-3`
(candidate `a751cb3b…`, merge `07389b24…`; numeric correction only — P10-D3b not reopened).

## Phase 10 — OD-DR1 accepted at strategy level (physical deletion / erasure position)

Accepted under the authoritative `P10_JURISDICTION_AND_DATA_RIGHTS_OWNER_DECISION_GATE.md`, which had
registered OD-DR1 as unresolved. **OD-DR2 and OD-CJ1 remain REGISTERED AND UNRESOLVED**; OD-J1/OD-J2 remain
accepted and unchanged (PR #515); OD-A continues to govern brand/name; **P10-D3b is preserved** (Account
Deactivation ≠ Physical Deletion).

| ID | Subject | Status | Phase/WS | Impl. authority | Evidence |
|---|---|---|---|---|---|
| OD-DR1 | **Physical deletion / erasure product position** — current authorized account-exit capability remains **Account Deactivation** (P10-D3b; a tombstone/non-active `"deleted"` status that retains all data and is NOT erasure); physical deletion/erasure is **DEFERRED PENDING EXTERNAL LEGAL DETERMINATION AND SEPARATE OWNER AUTHORIZATION**; no current retention behavior changes. Future capability principles only (no authorization): explicit user request; identity re-verification; pending-deletion state; configurable grace/recovery and notice schedule (Owner's ~1-month/~1-week/~1-day notice preference recorded as NON-BINDING future UX preference — not a legal requirement, retention period, or compliance proof; notices are user protection/transparency/recovery/process evidence and must NOT be described as liability waiver or waiver of statutory rights); cancellation before finalization; conditional truthful export opportunity ("where legally and operationally appropriate" — does not resolve/expand OD-DR2); truthful final-state communication; **minimum necessary, non-content-bearing deletion-processing evidence** (must not contain or permit reconstruction of erased content, must not become a hidden backup; legal basis/duration undetermined). Future deletion must NOT assume delete-every-row — data must first be classifiable (erasable / lawfully retained / requires legal determination / append-only audit / commercial-accounting / security-fraud evidence). **Deferral does NOT suspend existing legal obligations** — a legally binding erasure/data-subject request received before the capability exists must be escalated to the Owner + external counsel as an exception; OD-DR1 is not grounds for refusal/delay (escalation rule, not a regime-applicability conclusion). Subscription expiry/non-renewal/non-payment and account inactivity are NOT deletion requests and trigger nothing automatically. Institutional deletion authority reserved to a later institutional/legal gate. Any future implementation requires a separate **technical deletion-impact gate** inventorying all stores incl. backups/replicas/derived copies. | ACCEPTED AT STRATEGY LEVEL | Phase 10 | NONE (deletion implementation additionally requires the future impact gate + external legal determination + separate Owner authorization) | phase10_owner_decisions/OD-DR1_PHYSICAL_DELETION_ERASURE_POSITION.md |

## Phase 10 — OD-DR2 accepted at strategy level (account-wide data access / export position)

Accepted under the authoritative `P10_JURISDICTION_AND_DATA_RIGHTS_OWNER_DECISION_GATE.md`, which had
registered OD-DR2 as unresolved. **OD-CJ1 remains REGISTERED AND UNRESOLVED**; OD-DR1 remains accepted and
unchanged (PR #516); OD-J1/OD-J2 remain authoritative; OD-A governs brand/name; P10-D3a, P10-D3b, and the
Decision Workspace export are preserved exactly as merged.

| ID | Subject | Status | Phase/WS | Impl. authority | Evidence |
|---|---|---|---|---|---|
| OD-DR2 | **Account-wide data access / export position** — account-wide self-service export is **DEFERRED PENDING EXTERNAL LEGAL DETERMINATION AND SEPARATE OWNER AUTHORIZATION**; the only currently authorized P10-D3a self-service export remains **PROJECT-SCOPED EXPORT** under its truthful-label contract (never described as final-output/account/"Export my data"/account-wide export); FDC-001 Decision Workspace export preserved unchanged; no export surface expanded. **Owner future product priority (direction only): USEFUL OUTPUT PORTABILITY OF FINAL PROJECT OUTPUTS / RESULTS** (final results/decisions/conclusions/structured outputs/artifacts) — creates no surface, modifies nothing, selects no format. **Product Export ≠ Legal Data Access/Portability** — a narrow product export never proves legal-access satisfaction; a broader legal request never silently redefines the product export; no regime-applicability conclusion. **No-foreclosure principle** (architecture preservation ONLY — not build/prepare/pre-implement/schema/routes/jobs/bulk infrastructure). **Deferral does NOT suspend legally applicable data-access/portability obligations** — binding requests escalate to Owner + external counsel; OD-DR2 is not grounds for refusal/delay (escalation rule only). Does NOT modify/reopen OD-DR1, reinterpret P10-D3b, delete data, or alter retention; OD-DR1's conditional export opportunity neither expanded nor foreclosed. **Normal product-export exclusion defaults** (not legal conclusions): no automatic exposure of password hashes, credential secrets/hashes/records, verification/reset tokens, session/security metadata, fraud/abuse indicators, rate-limit records, internal operational metadata, provider internals, third-party confidential data, another user's data, or unauthorized institution-owned data; `subscription_lifecycle_events`/`commercial_audit`/`provider_event_dedupe`/`access_audit`/backups/replicas/derived copies classified separately, never auto-exposed. localStorage drafts are client-only — server export must not claim completeness over them (no collection mechanism created). Future strong identity/authorization verification principle recorded (ownership, compromised-session, exfiltration, institutional/administrator authority) — workflow not designed. **NO INSTITUTIONAL EXPORT AUTHORITY; NO INSTITUTIONAL FEATURE** (reserved to a later institutional/legal gate). Third-party/other-user data never exposed merely because technically reachable. **Format-neutral** — no PDF/email/cloud/vendor delivery, connector, adapter, or integration authorized. Preserves the authoritative architecture `InventorAI Core → Canonical Output Model (P7-I1 Structured Export) → Integration/Export Layer (P7-I3 adapter boundary) → External Tools`; no second canonical model. **`user export = dump every database row` explicitly REJECTED** — useful output portability, not database dump. | ACCEPTED AT STRATEGY LEVEL | Phase 10 | NONE (any future export capability requires separate Owner authorization; broader legal handling stays with Owner + external counsel) | phase10_owner_decisions/OD-DR2_ACCOUNT_WIDE_DATA_ACCESS_EXPORT_POSITION.md |

## Phase 10 — OD-CJ1 accepted at strategy level (commercial jurisdiction / tax scope)

Accepted under the authoritative `P10_JURISDICTION_AND_DATA_RIGHTS_OWNER_DECISION_GATE.md`, which had
registered OD-CJ1 as unresolved. With this acceptance, all five gate-registered decisions (OD-J1, OD-J2,
OD-DR1, OD-DR2, OD-CJ1) carry accepted rows; OD-A continues to govern brand/name. The Phase-10 external
legal-input register remains OPEN, and the P8C §5 / P8-I4 deferred business registers are CONSUMED BY, NOT
CLOSED BY, OD-CJ1.

| ID | Subject | Status | Phase/WS | Impl. authority | Evidence |
|---|---|---|---|---|---|
| OD-CJ1 | **Commercial jurisdiction / tax scope** — records **KUWAIT AS THE CURRENT INTENDED COMMERCIAL STARTING JURISDICTION**, strictly as A COMMERCIAL STARTING-POSITION INTENT FACT for later external legal/tax analysis; the tax-scope component remains **DEFERRED PENDING EXTERNAL LEGAL/TAX DETERMINATION AND SEPARATE OWNER AUTHORIZATION**. Kuwait is NOT a final legal-entity/incorporation/tax-nexus/VAT-GST-sales-tax/Merchant-of-Record/invoicing/withholding-reverse-charge answer. **Paid-activation hard gate preserved (load-bearing):** public paid activation remains BLOCKED / NOT AUTHORIZED under `D-P8-PL-01 class C`; Phase-10 legal/readiness items, external legal/tax input, payment/refund/subscription terms, `PSRR = GO/PASS` (`D-PSRR-01`), the separate Deployment Gate, and explicit Owner deployment authorization (`OD-P`) all remain independently required — none satisfied by OD-CJ1. Commercial customer eligibility includes BOTH **B2C individuals and B2B companies/organizations** (cross-referencing OD-J1 §2.3 as the user-type-scope authority, not duplicated) with the rule **COMMERCIAL CUSTOMER ELIGIBILITY ≠ ENTERPRISE FEATURE ACTIVATION** — no enterprise tenancy/workspaces/administration/user-management/administrator controls/negotiated contracts/institutional-enterprise pricing/purchase orders/procurement/company invoicing/tax-exemption/reverse-charge/withholding/enterprise-support workflows activated or decided. Commercial model direction: **RECURRING SUBSCRIPTION with AUTOMATIC RECURRING PAYMENT COLLECTION** — direction only; billing frequency/price/trials/grace/retries/failed-payment/suspension/renewal/cancellation/refunds/chargebacks/card-storage/tokenization/provider-specific billing all undecided and unauthorized. References the EXISTING **P8-I4 Payment Provider Boundary** (`InventorAI commercial domain → canonical provider-neutral PaymentProviderPort` — `engine/payment_provider_port.py` — `→ external payment provider`) without creating/renaming/duplicating/expanding it; **payment-provider neutral** (no Stripe/PayPal/Adyen/Paddle/Apple/Google/local-Kuwait/bank/other vendor); **tax-provider and Merchant-of-Record neutral** (direct-merchant vs MoR vs provider-calculated vs external tax service all open; NO-FORECLOSURE / ARCHITECTURE-PRESERVATION PRINCIPLES ONLY — explicitly not build/prepare/pre-implementation/schema/route/job/infrastructure instructions); **USD decided as the INITIAL / BASE COMMERCIAL PRICING AND BILLING CURRENCY** (strategy level; a commercial pricing/billing starting decision ONLY — it infers NO US commercial/legal-entity/tax jurisdiction, NO US hosting, NO US-only customers, NO US payment provider, and satisfies NO future local-currency display / invoice-currency / consumer-protection / accounting / tax-display requirement, which remain subject to external legal/tax/accounting determination); **multi-currency remains DEFERRED / NOT ACTIVATED** (no-foreclosure/architecture-preservation only — no additional currencies, currency conversion, FX-rate logic, currency selector, regional currency mapping, multi-currency settlement/accounting, or currency-specific tax logic; future currencies require a separately governed commercial decision/gate). **Jurisdiction separation rule:** USER RESIDENCE ≠ CUSTOMER LOCATION ≠ COMMERCIAL ENTITY JURISDICTION ≠ HOSTING LOCATION ≠ PAYMENT-PROVIDER LOCATION ≠ TAX JURISDICTION ≠ COMMERCIAL CURRENCY — Kuwait-start ≠ Kuwait-only users/companies/hosting; GCC-first ≠ GCC-only tax; OD-J1/OD-J2 unchanged. **Escalation rule:** deferral suspends no legally applicable obligation — binding commercial/payment/tax/accounting requirements escalate to Owner + external legal counsel + external tax/accounting adviser; no conclusion that any VAT/GST/sales-tax/withholding/reverse-charge/registration/invoicing requirement currently applies. **Payment-method compatibility direction (Owner decision; PAYMENT METHOD ≠ PAYMENT PROVIDER, load-bearing):** intended commercial payment-method compatibility includes Visa/major cards, Mastercard/major cards, Apple Pay, and KNET where commercially and technically applicable to the Kuwait starting market — DIRECTION ONLY, nothing implemented or activated; Apple Pay intent does NOT select Apple as provider, Visa/Mastercard compatibility does NOT select them as gateway/provider, KNET compatibility does NOT select KNET or any Kuwait gateway as provider and carries NO lock-in (not Kuwait-only customers/capability/provider, no permanent KNET dependency, no assumption KNET supports every recurring-billing use case); Google Pay/additional wallets/local/regional/international methods are FUTURE NO-FORECLOSURE ONLY; payment-method recurring-subscription support (initial payment, renewal, authorization/consent, saved-payment token, method update, failed-payment handling, retries, cancellation, refunds) must be verified at the future provider implementation/selection gate — no method guaranteed now; consistent with the EXISTING P8-I4 §15 PCI architectural-avoidance principle (hosted/provider-tokenized checkout keeps raw PAN/CVV off-platform; NO PCI-compliance claim; no tokenization designed; no card data stored; referenced, not duplicated); the P8-I4 deferred `payment methods` register is CONSUMED BUT NOT CLOSED. | ACCEPTED AT STRATEGY LEVEL | Phase 10 | NONE (billing/tax/provider/MoR/pricing/paid activation each require separate future authorization under P8C/P8-I4/D-P8-PL-01/D-PSRR-01/OD-P) | phase10_owner_decisions/OD-CJ1_COMMERCIAL_JURISDICTION_TAX_SCOPE.md |

## PDVG-01 — OD-PDVG-11(a) and OD-PDVG-01(a) — bounded S2 extension scope + one future release-candidate run (ACCEPTED; contract candidate — extension NOT yet authoritative)

Accepted against authoritative PDVG-01 (`docs/governance/PDVG_01_PRE_RELEASE_PRODUCT_DEPTH_AND_VALUE_GATE_RECORD.md`,
accepted candidate `df941501…`, merged `a9b9d53cb15165ec9ed0b35962577449750ff663`, PR #559), which surfaced
**14 actionable Owner decisions and recorded none as made**. **Exactly two are now decided.** The other
twelve — OD-PDVG-02, 03, 04, 05, 06, 07, 08a, 08b, 09, 10, 12, 13 — remain **REGISTERED AND UNDECIDED**;
no approval of any of them is implied by adjacency to these two. **`MLC DEFINITION FROZEN: NO`**;
OD-PDVG-07 remains a separate undecided decision; and the authoritative correction **OD-PDVG-10 does NOT
block MLC definition** (PDVG-01 §4A.5) is preserved. PDVG-01's §11 lines
`OWNER DECISIONS RECORDED AS MADE: 0` and `S2 EXTENSION AUTHORIZED: NO` are superseded by these two rows
(→ `2` and → `YES, scope approved / run not executed`); **every other PDVG-01 §11 line stands unchanged**,
and PDVG-01 itself is not edited.

| ID | Subject | Status | Phase/WS | Impl. authority | Evidence |
|---|---|---|---|---|---|
| OD-PDVG-11 | **Approve the bounded S2 extension scope — OPTION (a)** (the T1-A′ minimum extension). Approves, for the **existing** owner `docs/benchmarks/BICYCLE_BRAKE_LIGHT_COMPETITIVE_BENCHMARK.md`: one **mechanical** frozen case (M-1) alongside the unchanged electronics case (E-1); **EN and AR** as an evaluated dimension of the release-relevant Path-N experience, not translation-string existence; **novice** and **experienced-technical** *evaluation perspectives* (an evaluation instrument — **never** describable as real-user research); added criteria `P1…P6` for question quality, critical missing gaps, unsafe assumptions, prohibited/unsupported claims, specialist escalation, and deliverable usefulness; and explicit **`NOT APPLICABLE`** classification — never `FAIL` — for criteria structurally bound to the paused Technical Decision Workspace lane. **Binding constraint:** criterion 12's stale-marking is `NOT APPLICABLE` and must **never** be satisfied by introducing `validity_status`, stale-marking, or targeted-partial-invalidation semantics into the main product; `D17`, `D-AISR-06` and PVCG-R4 semantics are **unchanged**. **`NOT APPLICABLE` is reserved to criteria 12 and 13 and the S2 §6 core gate as written** — a criterion the product could satisfy but does not is a `FAIL`/`PARTIAL`. **NO second benchmark owner, no parallel reasoning-quality programme, no duplicate framework, no new domain activation, no product implementation.** | ACCEPTED — OPTION (a) | PDVG-01 T1-A′ / S2 | NONE | pdvg_owner_decisions/OD-PDVG-11_OD-PDVG-01_S2_BOUNDED_EXTENSION_ACTIVATION.md; `docs/benchmarks/BICYCLE_BRAKE_LIGHT_COMPETITIVE_BENCHMARK.md` §§15–17 |
| OD-PDVG-01 (revised) | **Authorize the bounded S2 extension and one subsequent run — OPTION (a).** Authorizes the bounded extension **and**, only **after that extension has itself become authoritative** through the full high-assurance lifecycle (candidate → exact-SHA freeze → Mandatory Creator Grill → Independent External Review → Owner exact-SHA acceptance → SHA-preserving publication → PR → merge commit → post-merge identity verification), **exactly one** S2 run against the **exact release-candidate commit**, with every result bound to that SHA. Option (b) — running S2 unchanged — is **not** taken. **`S2 BENCHMARK RUN EXECUTED: NO`; no run is authorized now**; contract creation and benchmark execution must not be combined in one candidate; any further run needs separate Owner authorization. **Epistemic boundary (load-bearing):** one run may support only that *on the frozen cases, at the exact commit, against the governed baselines, using the approved criteria, the evaluated Path-N journey and deliverable did or did not meet the defined S2 release-value criteria* — and **never** all-user behaviour, market success, real-user usability, real-world novice/expert fit, production readiness, security, operational or commercial readiness, universal superiority over general-purpose AI, or generalization beyond the frozen cases. **T1-A′ does not substitute for T1-C′**, whose ILT-style real-user round remains independently required. A favourable result **authorizes nothing** (S2 §0). | ACCEPTED — OPTION (a); run authorization CONDITIONAL and NOT YET EXERCISABLE | PDVG-01 T1-A′ / S2 | NONE — the extension grants no implementation authority, and the run grants none regardless of result | pdvg_owner_decisions/OD-PDVG-11_OD-PDVG-01_S2_BOUNDED_EXTENSION_ACTIVATION.md; `docs/benchmarks/BICYCLE_BRAKE_LIGHT_COMPETITIVE_BENCHMARK.md` §§15–17 |

**Non-authorization boundary.** These two decisions authorize **none** of: the S2 run in this candidate;
rendered correction UX; ILT real-user execution; T1-D disclosure; WS6 Quantified Requirements; WS10
content; WS11 activation; WS16 extension; evidence-writer implementation; ordering-defect repair; semantic
adaptive-questioning implementation; CAP-12; CAP-13; new workstreams; new domains; AI activation; PSRR GO;
deployment; production; or paid activation. Executable product-code delta and test delta are **0**.

**Two binding architectural protections, both carried by OD-PDVG-11(a).** (1) **Criterion 12** is
`NOT APPLICABLE` and must never be satisfied by introducing stale-marking into the product. (2) The
**domain gate** is protected the same way. `engine.domain_rules.classify_domain` is **wording-sensitive**:
measured at the base commit, **neither case's bare product concept resolves**, and the **electronics**
case E-1 resolves to **`mechanical`** when stated with its own §3 candidate 1
(`bicycle automatic brake light with a wired brake-lever switch`). Because wording steers the outcome the
contract **freezes the English seed text** under one outcome-independent construction applied identically
to both cases — *product-concept line, then user-context sentence, verbatim, em-dash joined* — whose
measured results are **`NONE`** for E-1 and **`SINGLE` → `mechanical`** for M-1; **that asymmetry is
recorded, not corrected.** The **Arabic** seeds freeze **at first use**, admissible only because an Arabic
seed cannot resolve a domain at all. Each run records the **exact seed text** per case and per language; **rewording a case to
change a gate outcome is prohibited** (any seed change is a §2 case revision); **`engine/domain_rules.py`,
the domain registry, the activation set and the `/start` admission policy are never changed to admit a
benchmark case**; and a resolved domain is **never** asserted to be the case's "correct" domain. A
blocked, mis-classified, or consent-routed frozen case is a **truthful reportable result**. The **Arabic
dimension** carries the same protection: `engine/domain_rules.py` and every domain pack under `domains/`
contain **no Arabic text**, so an Arabic-only seed **cannot** resolve a domain (measured `NONE` for both
Arabic seeds) and an Arabic run reaches the classifier-miss / admission path for **both** cases — a
property to be evaluated, with **no** addition of Arabic (or any other language's) classifier,
domain-pack, or admission vocabulary authorized. **One run is countable: 2 cases × 2 languages × 2 perspectives = 8
evaluation records**, reported separately with no aggregate, never split into additional "runs".
Baseline B is an **evaluator activity outside the product**: no product AI call, `AI_ADVISORY_ENABLED`
unchanged, and **no benchmark artifact may be fed back into the product**.

**Disclosed narrowing (recorded, not silently applied).** PDVG-01 T1-A′ anticipated marking *"the
decision-workspace-only criteria (9–14, and the §6 core gate as written)"* NOT APPLICABLE. Direct source
reconstruction narrows the set to **{12, 13}**: criteria 9, 10, 11 and 14 each have a real Path-N
counterpart (`contract_version` / `engine_contract_version` and `seed_idea_text` in `engine/record_store.py`;
full deterministic re-evaluation; `CORRECTION_APPLIED_ACK` with `withdrawn_source_records`), so excusing
them would understate what the instrument can legitimately judge. T1-A′'s **rule** is applied unchanged;
its parenthetical **enumeration** is the only divergence, and it narrows what the extension excuses.

## Wave-1 remediation — Owner decisions consumed (OD-R1, OD-R2, OD-PDVG-02 decided; OD-R3, OD-R5, OD-R4 accepted in principle, implementation Owner-gated)

Recorded at the Wave-1 authoritative closure/synchronization gate. Chain of authority, each step
separately verified from Git: the bounded S2 extension became **AUTHORITATIVE** at merge
`e119d60450f40b1633433625ae6a011eec112b79` (PR #560); the **one** authorized S2 Path-N
release-candidate run (`S2-PATHN-RUN-001`, 2026-08-23) was executed against that exact RC SHA and
**no record achieved a full pass** (per-record core gate: R1 PARTIAL · R2–R4 FAIL · R5 PARTIAL ·
R6–R8 FAIL; evidence-only commit `ebf243db83d880f75c2febc3d33d6a52a76ceab7`, preserved as
`refs/evidence/s2run-ebf243db`, parent `e119d604…`, not on the branch); the Owner adjudicated
`ACCEPT EVIDENCE — REMEDIATION REQUIRED`, froze the **Final Remediation Contract**
(RVR-1…RVR-8), and authorized **Wave 1 only** (RVR-1, RVR-2, RVR-3, RVR-5), merged via **PR #561**,
merge `93be682a34c1221f0af7f7018af9023a9b6c5b2c` (see
`docs/governance/WAVE_1_REMEDIATION_FORMAL_CLOSURE_RECORD.md` and
`docs/governance/WAVE_1_REMEDIATION_IMPLEMENTATION_CONTRACTS.md`).

**Supersession of the S2-extension section above (stated, not hidden).** That section's
"the other twelve — 02, 03, 04, 05, 06, 07, 08a, 08b, 09, 10, 12, 13 — remain REGISTERED AND
UNDECIDED" enumeration is preserved as authority-at-that-time. Current authority is this section:
**OD-PDVG-02 is now DECIDED — OPTION (a)** and consumed by Wave-1 (RVR-5/T1-B); the remaining
**eleven** — OD-PDVG-03, 04 (partially promoted in principle only, below), 05, 06, 07, 08a, 08b,
09, 10, 12, 13 — remain **REGISTERED AND UNDECIDED** as their own decisions. Likewise, the
**OD-PDVG-01(a) one-run authorization is now EXERCISED AND CONSUMED** by `S2-PATHN-RUN-001`; a
second S2 run requires separate Owner authorization (`SECOND S2 RUN AUTHORIZED: NO`), and a result
authorizes nothing (S2 §0).

| ID | Subject | Status | Phase/WS | Impl. authority | Evidence |
|---|---|---|---|---|---|
| OD-R1 | **Truthful unknown progression & completion semantics** — governed `risk_accepted` ledger disposition; `ACCEPTED_RISK` gap status via the sole writer `accept_gap_risk` (never MECHANISM_COMPLETENESS); completion semantics accept CLOSED-or-ACCEPTED_RISK for feasibility/boundary; explicit owner action, truthful labels, replay-stable, deliverable-visible (accepted ≠ resolved) | ACCEPTED — CONSUMED BY WAVE-1 (RVR-1 merged, PR #561) | Remediation / RVR-1 | NONE beyond the merged RVR-1 increment | WAVE_1_REMEDIATION_IMPLEMENTATION_CONTRACTS.md §RVR-1; WAVE_1_REMEDIATION_FORMAL_CLOSURE_RECORD.md §2 |
| OD-R2 | **Deterministic structured-substance assessment** — Layer-3 STRUCTURED-TECHNICAL gate in `assess_response` + MG-5 `provenance=OWNER_STATED` Evidence stamping + T2-F ordering guard tests (the ordering REPAIR itself remains OD-PDVG-08b, not performed) | ACCEPTED — CONSUMED BY WAVE-1 (RVR-3 merged, PR #561) | Remediation / RVR-3 | NONE beyond the merged RVR-3 increment | WAVE_1_REMEDIATION_IMPLEMENTATION_CONTRACTS.md §RVR-3; WAVE_1_REMEDIATION_FORMAL_CLOSURE_RECORD.md §2 |
| OD-PDVG-02 | **Rendered correction UX (T1-B)** — OPTION (a): render the correction affordance over the byte-unchanged PVCG-R4-C `/session/<sid>/correct` route; deliverable renders the withdrawn-history aggregate; R4-C semantics unchanged | DECIDED — OPTION (a); CONSUMED BY WAVE-1 (RVR-5 merged, PR #561) | PDVG-01 T1-B / RVR-5 | NONE beyond the merged RVR-5 increment | WAVE_1_REMEDIATION_IMPLEMENTATION_CONTRACTS.md §RVR-5; WAVE_1_REMEDIATION_FORMAL_CLOSURE_RECORD.md §2 |
| OD-R3 | **RVR-4 — generalize the FDC-001 `DecisionRecord` (Architecture D)** as the sole decision-semantics owner, with a bounded lift of the DW-lane hold for exactly that composition | ACCEPTED IN PRINCIPLE — IMPLEMENTATION NOT AUTHORIZED (Wave 2+, separate Owner authorization) | Remediation / RVR-4 | NONE | Owner freeze-and-Wave-1 authorization (recorded in WAVE_1_REMEDIATION_FORMAL_CLOSURE_RECORD.md §7) |
| OD-R5 | **RVR-6 — bounded adaptive interaction, Tier-1 STATE-ADAPTIVE only** (capabilities A–F; evidence-weighted reversible register calibration with deterministic hysteresis, W/M Owner-approvable; register-variant content gate; semantic-equivalence invariant; partial promotion of OD-PDVG-04(a) WS10 content authoring into Tier-1); Tier-2 meaning-adaptive questioning remains OD-PDVG-10, unchanged and unauthorized | ACCEPTED IN PRINCIPLE — IMPLEMENTATION NOT AUTHORIZED (Wave 2+, separate Owner authorization) | Remediation / RVR-6 | NONE | Owner freeze-and-Wave-1 authorization (recorded in WAVE_1_REMEDIATION_FORMAL_CLOSURE_RECORD.md §7) |
| OD-R4 | **RVR-7 — substantive Arabic parity program** (after content stabilizes; W1-N2/W1-N3 are mandatory inputs) | ACCEPTED IN PRINCIPLE — IMPLEMENTATION NOT AUTHORIZED (Wave 3, separate Owner authorization) | Remediation / RVR-7 | NONE | Owner freeze-and-Wave-1 authorization (recorded in WAVE_1_REMEDIATION_FORMAL_CLOSURE_RECORD.md §7) |

**Boundaries carried.** `WAVE-2 AUTHORIZED: NO`; RVR-4 / RVR-6 / RVR-7 / RVR-8 each require their own
future Owner authorization (RVR-8's verification-run authorization is entirely future); the intended
sequence `RVR-4 ∥ RVR-6a → RVR-6b → RVR-7 → RVR-8` is planning direction only. `T1-A′ CLOSED: NO`;
`MLC DEFINITION FROZEN: NO`; the five Wave-1 follow-ups (W1-S2, W1-N1, W1-N2, W1-N3, W1-N4) are
recorded, owned, and NOT implemented (closure record §4). Accepting these rows activates nothing.

## Wave-2 — committed decisions and authorization lineage (post-W2-ID synchronization)

Recorded at the post-W2-ID status-sync + deferred-register gate. The Wave-1 section's
`WAVE-2 AUTHORIZED: NO` boundary line above is authority-at-that-time; current authority follows.

**A. Committed Owner decision.**

| ID | Subject | Status | Phase/WS | Impl. authority | Evidence |
|---|---|---|---|---|---|
| OD-W2ID-LEDGER | **Decision-capture carrier ARCHITECTURE** — the existing `AssertionRecord` ledger is approved as the bounded durable carrier for decision-capture owner actions; FDC-001 `DecisionRecord` remains the SOLE canonical decision-semantics owner; `AssertionRecord` remains a carrier/provenance/history object and is never presented as the decision itself; implementation — including any disposition-value or field change — is separately authorized only in W2-A | **APPROVED — ARCHITECTURE DECIDED; IMPLEMENTATION/ENACTMENT DEFERRED TO W2-A** (the deferred enactment items are now FROZEN by the authoritative W2-A contract, PR #567 — implementation still separately authorized) | Wave-2 / W2-ID → RVR-4 | NONE now (implementation authorized only at the W2-A implementation gate) | `docs/governance/W2_ID_DECISION_CAPTURE_IDENTITY_RECORDING_CANDIDATE.md` §B (authoritative via PR #565, merge `516a1842…`) |
| OD-W2-DW-LIFT | **Bounded DW-lane-hold-lift EXERCISED** — the Owner exercise recorded in the authoritative W2-A contract §5 grants ONLY: (1) reuse of the FDC-001 `DecisionRecord` class by the Path-N deterministic decision-composition seam; (2) default-preserving constructor generalization only where required for deterministic injected identities (incl. the bounded seed-suppression / `decision_question`-injection scope the contract derives and flags); (3) reuse of the class vocabulary the bounded composition seam requires. It authorizes NO code in the contract gate, does NOT lift the broader DW Path-T hold, and preserves the full forbidden list (no second journey; no live DW behavior/endpoint/UI change; no persistence expansion; no second canonical decision model); the S2 §13 `PRESERVE UNMODIFIED AND PAUSE` boundary remains intact | **EXERCISED (bounded) — via Owner exact-SHA acceptance of the W2-A contract** | Wave-2 §P item 3 → W2-A | W2-A implementation gate (for the lifted permission's code) | `docs/governance/W2_A_RVR4_IMPLEMENTATION_CONTRACT_CANDIDATE.md` §5 (authoritative via PR #567, merge `82758cb2…`, accepted candidate `b778cfe7…`); Deferred Obligations Register §2 row CLOSED |
| OD-W2-WS10-SCOPE | **Corrected WS10 scope EXERCISED** — the Owner exercise recorded in the authoritative W2-C contract §D selects EXACTLY: **two per-domain WS10 intent registry instances** — electronics registry covering the existing 11 committed ids, mechanical registry covering the existing 10 committed ids, total 21 existing committed ids — each loaded through the **existing unmodified D11/D19 loader contract** (one registry validated against one `source_artifact_path`, exact ID-set equality per artifact); **OD-PDVG-04(a) exercised bounded to exactly those 21 ids**; **combined-source reconciliation REJECTED** (not deferred); no new placeholder/question/decision identities authorized; no broader WS10 scope authorized. **Wave-2 §P.4 timing interpretation (Owner-ratified, durable):** the source wording "before W2-C freeze" is resolved for this lifecycle as — the Creator's freeze of the governance contract candidate is NOT the Owner decision exercise; the **Owner's exact-SHA acceptance of the frozen contract candidate IS the binding Owner exercise** (the OD-W2-DW-LIFT precedent); that acceptance occurred before any W2-C implementation authorization, implementation-candidate freeze, or implementation execution — so `EXERCISED BEFORE OWNER ACCEPTANCE: NO` and `EXERCISED BY OWNER EXACT-SHA ACCEPTANCE: YES`. Historical Wave-2 §P.4 source text is not rewritten. Recording this exercised decision authorizes NO implementation | **EXERCISED — via Owner exact-SHA acceptance of the W2-C contract** (`455cb502aba03cdc3ae14fb04c7116b9e1ffe6ab`) | Wave-2 §P item 4 → W2-C | W2-C implementation gate (for the registries/content themselves; implementation start still requires its own separate Owner authorization) | `docs/governance/W2_C_RVR6B_IMPLEMENTATION_CONTRACT_CANDIDATE.md` §D (authoritative via PR #579, merge `d796b0cd385d8ad2071088d58a89612715aad888`, accepted candidate `455cb502…`) |

**B. Authorization lineage — recorded without retroactive invention.** The following lifecycle
authorizations were exercised through the full high-assurance lifecycle (candidate → Grill →
Independent External Review → Owner exact-SHA acceptance → merge commit → post-merge verification)
but carry no dedicated register entry of their own. Classification for each:
`AUTHORIZATION EXERCISE EVIDENCED BY AUTHORITATIVE MERGED EXECUTION; DEDICATED REGISTER ENTRY
ABSENT`. No OD identifier, decision date, or approval wording is invented; the merged execution is
the evidence.

| Exercise | Accepted candidate (exact SHA) | Merge | Effect |
|---|---|---|---|
| Wave-2 bounded implementation contract authorization | `84b165a894a771ff2775a993d8f08f38e6ba46a6` | PR #563, `58e92e09cc7e6d36cb9c939cf9958e8a294f88ce` | Wave-2 contract CONTRACT AUTHORITATIVE (1 governance sub-gate + 4 executable slices; RVR-7 = Wave 3; RVR-8 separate) |
| W2-D implementation acceptance (W1-S2 + W1-N4) | `528b45199892aaa4ce6b2f0db2452f525b963c0b` | PR #564, `91475e456cbe8ff21bfa8e7bf2fb3e6dd801f762` | W2-D IMPLEMENTATION AUTHORITATIVE; W1-S2 and W1-N4 CLOSED with evidence |
| W2-ID acceptance (v3 after focused re-Grill + narrow repair; v1 `f2cfe745…`/v2 `538d57fa…` immutable reviewed evidence) | `a92d4fa4dcea32009b3020b083c08dc8028772d5` | PR #565, `516a184231f3e19fad6e8f6f3301b5b9c4ad9820` | W2-ID GOVERNANCE MINI-GATE AUTHORITATIVE; OD-W2ID-LEDGER committed |
| Post-W2-ID status sync + permanent Deferred Obligations Register acceptance | `3910e86c29e569680be8ac8c728acd6e94453ab6` | PR #566, `557548db2bb37b21b6b57f893afc2ae1af64744f` | Status surfaces synchronized; `DEFERRED_OBLIGATIONS_REGISTER.md` AUTHORITATIVE (Master Obligation Index layer 6) |
| W2-A / RVR-4 contract-freeze acceptance (final sibling after Independent External Review `NARROW REPAIR REQUIRED` + Creator re-Grill; `f4d0552…` reviewed / `f0f6663…` Grill-failed siblings preserved as immutable evidence) | `b778cfe7fd31c82c583d7d97e5f73394e6bfda65` | PR #567, `82758cb2d06a7b91d30acfaa83a3d836df103186` | **W2-A CONTRACT-FREEZE AUTHORITATIVE** (V2 vocabulary; `decision_context_root`; bounded legacy load rule; fail-closed carrier mint; `OWNER_STATED` provenance; OW-6 incl. corrected requirement-landscape containment; frozen allowlist + RED inventory); OD-W2-DW-LIFT EXERCISED (bounded, §5); **W2-A IMPLEMENTATION NOT AUTHORIZED / NOT STARTED** |
| Post-W2-A-contract status sync acceptance | `6f592779790f35e0641fa800b603e52cc227c74b` | PR #568, `894861c9ef78c9affe927f22dfa497de68050e96` | Status surfaces + register reconciled to the contract-freeze; OD-W2-DW-LIFT and the two post-W2-ID sync rows CLOSED; enactment/RVR-4 kept OPEN per contract §21 |
| **W2-A implementation authorization exercise** — explicit Owner authorization of W2-A/RVR-4 implementation under the frozen contract (its allowlist/RED inventory/STOP conditions), followed mid-lifecycle by the **explicit bounded Owner allowlist extension** (`engine/deliverable_assembler.py`, `_withdrawn_source_meta` class-bounded containment only) granted to repair the Creator-escalated IG-17 defect | authorization exercised through the full lifecycle (no single candidate SHA — see the acceptance row below) | evidenced by the PR #569 chain | W2-A implementation STARTED and executed strictly inside the frozen contract + one bounded extension; no adjacent scope |
| **W2-A / RVR-4 implementation acceptance** — final fresh same-base sibling after Creator-Grill-failed `b3ada80b26de75379c3a4f5fedf27d6c438c8dd8` (IG-17) and externally reviewed N-2-material-rejected `614a0c78b6e43f4f6abbc139bee7c0f33c9ac925`, BOTH preserved as REMOTE evidence branches (`evidence/w2a-impl-grillfail-b3ada80`, `evidence/w2a-impl-reviewed-614a0c7` — verified at their exact SHAs) | `d8c5aef988a00a8b342b26816afd6186e4262c42` | PR #569, `e17ca1477e55b49298b92ac5ec8db711e208496e` (second parent = the exact candidate; merge tree `4c1739ae…` identical; empty candidate→merge diff; merged 2026-08-25T13:56:35Z) | **W2-A / RVR-4 IMPLEMENTATION AUTHORITATIVE** — bounded decision capture live in the existing journey (carrier mint validation; 15-field contract + bounded legacy load; deterministic composition; OW-6 containment incl. IG-17; N-2 retry-vs-new-intent repair; EN/AR); register rows "W2-A enactment set" and "RVR-4" CLOSED on this evidence; **release-value gates NOT touched** |
| Post-W2-A-implementation status sync + FCORA recording acceptance (fresh sibling replacing superseded-before-review `e36a4d5…`) | `007f08ea637f14e163d23773944393c5d93c1e70` | PR #570, `e2b50120e5d2e4a1c156bff7cb5184c4efc4eb5b` | Enactment/RVR-4 closures authoritative; FCORA + Cross-Layer-Standard directions recorded (§D) |
| **Cross-Layer Execution Assurance Standard acceptance** — accepted after Independent External Review with non-blocking observations, carried forward here as BINDING interpretation of the authoritative standard: **O-1** — the standard's C0–C4 applicability classes do NOT replace the Lean LEVEL/DEPTH classification or the review-tier classification; they are separate axes (C-class selects which assurance MECHANISMS apply; Lean LEVEL/DEPTH/review tier continues to govern review intensity and authorization discipline under its existing owner — no duplicate classification ownership); **O-2** — whenever a Consumer Propagation Sweep applies, the candidate evidence records the REPRODUCIBLE search method (search terms; path/scope; tool/command style; categories inspected; resulting consumer inventory) so an independent reviewer can re-run it — without mandating any one shell command; **O-3** — the KFP identifiers remain bounded lessons, never a second obligations registry; **O-4** — the route-idempotency finding is referenced as `W2-A N-2` wherever ambiguity is possible; **O-5** — the reviewer's initial smoke BLOCK was an environment/dependency artifact (passed with pinned dependencies) and is NOT a project defect | `015a8534fbecef7e790f87cb42c087f28807d86e` | PR #571, `216cdc8e61eea141940de072105aa03a4cd801bb` (second parent = the exact candidate; merge tree `611d3da4…` identical; empty candidate→merge diff) | **`CROSS-LAYER EXECUTION ASSURANCE STANDARD: AUTHORITATIVE`** — its Continuous Traceability Rule and proportionality model are MANDATORY current process for future applicable candidates (prospective only); register Cross-Layer row CLOSED on this evidence; the W2-B-execution prerequisite is satisfied while **W2-B remains `AUTHORIZED: NO`** |
| Post-Cross-Layer-Standard status sync acceptance | `dda867bbd22f61ad4bc8f954f743d83d124c83a6` | PR #572, `21ce0ff843682068c0bc29a73d4506de51e581fa` | Status surfaces + register reconciled; Standard row CLOSED; O-1…O-5 carried as binding interpretation |
| **W2-B / RVR-6a implementation-contract acceptance** — repaired fresh same-base sibling after Independent External Review rejected `0448e36aec377942cba1f9baa955dfb2048be00c` (`REJECT — BOUNDED REPAIR REQUIRED`: D-1 digest-pin allowlist covered one of THREE enforcing pin tests; D-2 the `[EXEC]` consumer seed omitted the governed CLI consumer `scripts/run_cli.py:152`); the rejected SHA is preserved, un-rewritten, as rejected evidence. Non-blocking review observations carried forward as implementation-time obligations UNDER THE CONTRACT (no new registry): (A) the implementation Consumer Propagation Sweep must explicitly classify the module-level `progression_loop` import at `engine/session_reconstruction.py:55` even though it is not a direct `select_next_gap` call site today; (B) the deterministic simultaneous-trigger precedence/tie-break proposal is frozen in the implementation evidence pack per the contract; (C) the seven-consumer seed is historical — the reproducible sweep MUST be re-run at implementation; (D) the three-pin enforcing set is current evidence, not a permanent count — revalidate before any mechanical re-freeze | `5e91fd9cbc27b784c8b398ac48366b84dd73cceb` | PR #573, `48017ec0259e5fc7bcb105e0b018f6d447057bda` (second parent = the exact candidate; merge tree `c5c2590c…` identical; empty candidate→merge diff; merged 2026-08-25T21:15:58Z) | **`W2-B / RVR-6a IMPLEMENTATION CONTRACT: AUTHORITATIVE`** — the contract-acceptance authorization boundary the roadmap/ODR named "W2-B AUTHORIZATION" is COMPLETED (per the contract's own §N `[DERIVED]` composition); **`W2-B IMPLEMENTATION START AUTHORIZED: NO`** (a separate explicit Owner instruction is required); **`W2-B IMPLEMENTATION AUTHORITATIVE: NO`**; **W/M numeric values NOT frozen** (Wave-2 §P: proposed/frozen inside the future implementation candidate, fixed at its Owner exact-SHA acceptance); RVR-6a register row remains OPEN |
| Post-W2-B-contract status sync acceptance | `12267d94bce32ce6fae203c7fa5e6305d0f1f66a` | PR #574, `ad70723e8fdb34493ac9e53d7a9a3ceb80850708` | Status surfaces + register reconciled to the W2-B contract; §H→§P W/M citation corrected on live surfaces; lifecycle-state separation preserved |
| **W2-B FIRST implementation lifecycle (pre-amendment) — exercised, REJECTED, escalated.** The Owner's explicit implementation-start authorization under the pre-amendment contract was issued OUTSIDE the repository workflow (OWNER-RATIFIED PREMISE — durably recorded at this sync; the intervening `AUTHORIZED: NO` status lines were authority-at-their-time against an unsynchronized premise). The lifecycle produced Creator-Grill-failed `7e0174ac838f21680521951d074a6b56a88aecc6` and externally REJECTED `91c5de53f1d6f4bb0a4d9cfe857a5e9511415250` (`REJECT — MATERIAL RECONSTRUCTION / OWNER ESCALATION REQUIRED`: capability-3 gap-level promotion structurally vacuous under the singleton-open-gap architecture; the decision trigger contradicted FDC-001 comparability truth), both preserved as immutable rejected evidence via SHA-preserving bundles; a strictly read-only material-reconstruction gate returned the architecture options and calibration evidence (M=1 OVERTURNED by oscillation evidence) | no accepted candidate (rejected lineage) | no merge (rejected evidence only) | Escalation input to the Owner Architecture Resolution; NOTHING from this lifecycle is current authority |
| **W2-B Contract Amendment 1 acceptance — the Owner ARCHITECTURE RESOLUTION enacted**: OPTION C (state-aware next-question/next-action prioritization WITHIN the canonical gap; Options A/B not authorized; `select_next_gap` sole canonical gap owner; no cascade/replay/reconstruction change); trigger replacement (`newly_comparable_decision_state` REMOVED; `multiple_decision_alternatives_declared` ADDED as a true `<2→>=2` ledger transition — never a standing predicate, never a comparability claim; FDC-001 sole comparability/readiness owner; `len>=2` forbidden as a proxy); cue-only adaptation insufficient (behavioral floor frozen); exactly one committed evidence-pack file with ANTI-CIRCULAR Candidate Identity Binding; W/M falsification duty + anti-hard-coding rule (W=2/M=2 then the Owner-PERMITTED proposal, not accepted); MG-8 diagnosis-only; **lifecycle reset — the prior implementation-start authorization did NOT carry across the amendment**. Rejected sibling `2bcf15a7255128d81c06b73d4da4a4cd8eaf6164` (self-referential evidence-pack identity) preserved as rejected evidence | `6bb8f9e34c289953f2003de49c68210f9d2706ac` | PR #575, `346f8e8a3b1532a6c52750fe20bc76668db06956` (second parent = the exact accepted candidate; content byte-verified in the merged tree) | **`W2-B CONTRACT AMENDMENT 1: AUTHORITATIVE`** — supersedes the named base-contract clauses; base contract preserved as historical lineage |
| **W2-B / RVR-6a implementation acceptance under Contract Amendment 1** — a NEW explicit Owner implementation-start authorization for the AMENDED contract (OWNER-RATIFIED PREMISE) was exercised through the full lifecycle to the accepted candidate: Option-C serving policy (`compute_serving_decision`; purely additive `progression_loop` section; four amended triggers with REAL serving consequences, declared route-reachability limits, question-slot precedence proposal over real competing served texts); derived two-level register; committed evidence pack inside the exact tree; MG-8 diagnosed only; C2+C4 assurance; full suite `4662/3/1/0` (delta = exactly the 67 new tests), independently reproduced. **At this exact-SHA acceptance the Owner ALSO ACCEPTED AND FROZE `W = 2`, `M = 2`** — exactly the Wave-2 §P mechanism as amended (values produced by implementation evidence, fixed at acceptance of the implementation candidate) | `6cf0958205681d1f476ecb8a9258bbebfb365059` | PR #576, `ac9c01ea1caaca18306a99039cea3a4224216e8a` (first parent `346f8e8a…`; second parent = the exact accepted candidate; merge tree `f2b0004b…` identical; EMPTY candidate→merge diff) | **`W2-B IMPLEMENTATION: AUTHORITATIVE`**; **`W/M OWNER-ACCEPTED: YES; FROZEN: YES (W=2, M=2)`**; `RVR-6A CLOSED: NO` (formal closure is a separate gate); accepted non-blocking observations carried in the register's RVR-6a row |
| Post-W2-B-implementation status sync acceptance (repaired sibling after Owner-adjudicated `REJECTED — BOUNDED GOVERNANCE REPAIR` of `8b455a0bc8b88435f68abd8d64408eeb6873aeaa` — two structural defects; preserved as rejected evidence) | `3aa985ed72cacc4482dcc7c18092f33dbda6f962` | PR #577, `eb23cbf2b1b3b4d81908942ea9231756c90d8d94` | Status surfaces + register reconciled to the implementation; W/M freeze recorded on all current surfaces; next eligible gate named `RVR-6a FORMAL CLOSURE` |
| **RVR-6a formal-closure acceptance** — Owner authorized STARTING the closure lifecycle only; the Creator's closure gate reconstructed the closure contract from precedent, adjudicated a 13-row evidence matrix, swept the complete Deferred Obligations Register (closure blocker count 0; MG-8 non-blocking), and froze the conditional, non-circular closure record; the Owner then accepted the exact SHA and merged | `31eb87f6762c3dddc0a183ebc96674535546636d` | PR #578, `1a9eb55656b52f635804647fe77412a7987a591e` (second parent = the exact accepted candidate; merge tree `55c2d25b…` identical; empty candidate→merge diff; post-merge identity-verified) | **`RVR-6A FORMALLY CLOSED: YES`** — the closure record's §9 conditional statement is satisfied; the register's RVR-6a row records `CLOSED — evidence verified` at the post-W2-C-contract sync per that row's own conditional wording; W2-C remained NOT AUTHORIZED by the closure |
| **W2-C / RVR-6b contract acceptance** — repaired fresh same-base sibling after Lead adjudication REJECTED `706917cb66d4d7d6386f97a46fee58cd8c0ff2ac` pre-acceptance (primary defect: a false "tree unchanged by PR #578" Git proposition; plus six bounded hardening repairs R2–R7: OD-W2-WS10-SCOPE timing explicitness, W1-N3 deferral durable ownership, Amendment-1 §6 binding for the future combined precedence proposal, mandatory lapse revalidation, explicit EN/AR pack evidence, post-contract sync duties); rejected SHA preserved as evidence, not an ancestor of the accepted sibling. The contract freezes the six Tier-1 W2-C capabilities, consumes W1-N3 (`ATTEMPT BOUNDED CLOSURE; EVIDENCED FALLBACK = DEFER AS SAFE FALSE-NEGATIVE` — `DEFERRED ≠ SATISFIED`), excludes OD-PDVG-12 by default, and records the OD-W2-WS10-SCOPE exercise consummated by this very acceptance (section-A row above) | `455cb502aba03cdc3ae14fb04c7116b9e1ffe6ab` | PR #579, `d796b0cd385d8ad2071088d58a89612715aad888` (second parent = the exact accepted candidate; merge tree `816c39a5…` identical; empty candidate→merge diff; post-merge identity-verified) | **`W2-C / RVR-6b CONTRACT: AUTHORITATIVE`**; **`OD-W2-WS10-SCOPE: EXERCISED`** at this exact-SHA acceptance; **`W2-C RUNTIME IMPLEMENTATION AUTHORIZED: NO`** (a separate explicit Owner start instruction is required — the W2-A/W2-B precedent); `W2-C IMPLEMENTED: NO`; `RVR-6B FORMALLY CLOSED: NO` |
| Post-W2-C-contract status sync acceptance | `21c6076917754959c5f7c0c0cffde1f84a9c162e` | PR #580, `6b4629d75b58690eb0a40a754e747ba79f265447` (second parent = the exact accepted candidate; merge tree `8d620676…` identical; empty candidate→merge diff) | Status surfaces + registers reconciled to PR #578/PR #579; OD-W2-WS10-SCOPE decision row durable; RVR-6a register row CLOSED per its own conditional wording; W2-C implementation still NOT AUTHORIZED at that gate |
| **W2-C implementation-start authorization exercise** — AFTER the PR #580 sync became authoritative (which truthfully recorded `W2-C RUNTIME IMPLEMENTATION AUTHORIZED: NO` at its gate — that line is authority-at-its-time, not rewritten), the Owner explicitly authorized the bounded W2-C runtime implementation lifecycle from exact base `6b4629d75b58690eb0a40a754e747ba79f265447` (OWNER-RATIFIED PREMISE issued in the governed lifecycle outside the committed sync; durably recorded at THIS sync — the W2-A/W2-B chronology precedent). The authorization was bounded to the authoritative contract (PR #579) + the exercised OD-W2-WS10-SCOPE option | authorization exercised through the full lifecycle (no single candidate SHA — see the acceptance row below) | evidenced by the PR #581 chain | W2-C implementation STARTED and executed strictly inside the authoritative contract; no adjacent scope |
| **W2-C / RVR-6b implementation acceptance** — final fresh same-base sibling after TWO evidence-integrity rejections, BOTH preserved as immutable rejected evidence and NEITHER an ancestor of the accepted candidate: **#1** `1249dbbdf69bfc23a7b35f6e302478e995c8319f` (Lead-rejected: affected-family methodology conflated "18 modules"/"1443" with the enumerated 22-module manifest) and **#2** `cf77c33dfd560fc2026bc5fe0024ab2f6288ea8d` (Independent External Review IR-I84: focused per-module split recorded 13/15/11/9 vs the mechanically collected 14/14/11/9; runtime NOT rejected — reviewer independently reproduced focused 48/0, affected family 22 modules 1637/0/0/0, full suite 4710/3/1/0, W1-N3 truthful bounded closure, lapse NOT AFFECTED, EN/AR PASS). Accepted content: two per-domain WS10 registries (11+10 = the existing 21 committed ids) through the byte-unchanged D11/D19 loader; `engine/intent_serving.py` (EN/AR-paired question-id-scoped markers; derived never-persisted intent coverage; the deterministic within-gap serving law; decision-aware deference; the W1-N3 supplement with the replay-parity canonical scope); ONE additive `integrate_response` hunk; ONE render-only `show_session` hunk; three digest pins mechanically re-frozen with disclosed lineage; the committed evidence pack. **At this exact-SHA acceptance the Owner ALSO ACCEPTED the exact W2-B × W2-C composed precedence:** (1) W2-B question-slot overrides LAPSED > SKIP > CRITICAL always first; (2) W2-B alternatives transition — the W2-C question slot defers and the decision-evidence action remains the one primary CTA; (3) the W2-C intent-coverage law applies only over the plain canonical Path-N variant (stall-reframe / exhausted-exit / generic surfaces never overridden); (4) canonical serving remains the baseline and universal fail-closed target | `1bc0690d9bc9e7317d267d1c0be5ab8f5fcdd0a1` | PR #581, `b749c8873533ca6c48ebcf9be0c4023aa10cdd09` (first parent `6b4629d7…`; second parent = the exact accepted candidate; merge tree `14b54d7e…` identical; EMPTY candidate→merge diff; merged 2026-08-26T22:30:52Z; post-merge identity verified) | **`W2-C IMPLEMENTATION: AUTHORITATIVE`**; **`W2-C IMPLEMENTED: YES`**; **`PRECEDENCE OWNER-ACCEPTED: YES`** (as accepted above — not Full Adaptive Questioning; no second adaptive engine); **W1-N3 `CLOSED WITH EVIDENCE` — bounded authoritative scope** (the recorded M-1 experienced-technical MECHANISM residual; other relevance-precision residuals stay RVR-2/RVR-7-owned); `RVR-6B FORMALLY CLOSED: NO` (formal closure is a separate gate) |

**C. Current open boundary** (each prior boundary paragraph here was authority-at-that-time; the
enactment items were frozen by PR #567, the implementation-authorization requirement was satisfied
through PR #569, and the D-1 Cross-Layer-Standard gate completed via PR #571). Current truth:
`W2-A / RVR-4 IMPLEMENTATION AUTHORITATIVE: YES` (PR #569);
`CROSS-LAYER EXECUTION ASSURANCE STANDARD: AUTHORITATIVE` (PR #571, acceptance row above — its
Continuous Traceability Rule and C0–C4 model are MANDATORY current process for future applicable
candidates; per O-1 the C-classes are a separate axis from the Lean LEVEL/DEPTH and review-tier
classifications, which keep their existing owner);
`W2-B / RVR-6a IMPLEMENTATION CONTRACT: AUTHORITATIVE` (PR #573, acceptance row above — the
contract-acceptance authorization boundary is COMPLETED; the prior wording here that the W2-B
authorization "must also fix the W/M values at its acceptance (Wave-2 contract §H)" was
authority-at-that-time AND carried a citation defect: the operative W/M timing source is
**Wave-2 contract §P** — no individual W or M expansion and no numeric/enumerated value space is
authoritative; the earlier pre-gate value-fixing approach was withdrawn as circular; the values
are produced by W2-B implementation evidence, proposed/frozen inside the future implementation
candidate/evidence pack, and become fixed through Owner exact-SHA acceptance of THAT
implementation candidate — contract acceptance froze NO numbers; that mechanism has since been
EXECUTED — see below). Current truth after the Amendment-1 and implementation acceptance rows
above: **`W2-B CONTRACT AMENDMENT 1: AUTHORITATIVE`** (PR #575);
**`W2-B IMPLEMENTATION: AUTHORITATIVE`** (PR #576, accepted candidate `6cf09582…` — Option C;
`select_next_gap` sole canonical gap owner; FDC-001 sole comparability/readiness owner; exactly
four triggers; the alternatives trigger a deterministic ledger transition, no persisted
fired-state); **`W/M OWNER-ACCEPTED AND FROZEN: W = 2, M = 2`** (at the exact-SHA acceptance of
`6cf09582…`, per the §P mechanism as amended — the prior "NOT frozen" boundary language here is
authority-at-that-time). The prior boundary line here `RVR-6A CLOSED: NO` was
authority-at-its-time — **`RVR-6A FORMALLY CLOSED: YES`** via PR #578 (acceptance row above; the
closure record's conditional statement satisfied and post-merge verified). Current truth after
the W2-C contract acceptance row above: **`W2-C / RVR-6b CONTRACT: AUTHORITATIVE`** (PR #579);
**`OD-W2-WS10-SCOPE: EXERCISED`** (section-A row — two per-domain registries over the existing
21 committed ids through the unmodified loader; §P.4 timing interpretation recorded there);
the prior boundary line here "`W2-C RUNTIME IMPLEMENTATION AUTHORIZED: NO` … which this register
does not record" was authority-at-its-time — the separate Owner implementation-start
authorization was SUBSEQUENTLY issued and exercised, and the implementation was accepted and
merged (the two rows above): **`W2-C IMPLEMENTATION: AUTHORITATIVE — W2-C IMPLEMENTED: YES`**
(PR #581, accepted candidate `1bc0690d…`; rejected evidence-integrity siblings `1249dbbd…` and
`cf77c33d…` preserved, neither an ancestor); **`PRECEDENCE OWNER-ACCEPTED: YES`** (the exact
four-level W2-B × W2-C composition recorded in the acceptance row); **W1-N3 `CLOSED WITH
EVIDENCE` (bounded authoritative scope — other relevance-precision residuals stay
RVR-2/RVR-7-owned)**; **`RVR-6B FORMALLY CLOSED: NO`** — formal RVR-6b closure is the next
eligible gate and remains a SEPARATE lifecycle requiring its own Owner authorization;
OD-PDVG-12 UNEXERCISED; MG-8 Owner adjudication OPEN (no semantic repair authorized); WS11
dormant; Tier-2 meaning-adaptive and full adaptive questioning NOT ACTIVATED; the carried
non-blocking implementation observations (registry CWD/path binding; registry-prose ↔
`_INTENT_MARKERS` divergence surface) live in the Deferred Obligations Register RVR-6b row.
`RVR-7 / RVR-8: NOT AUTHORIZED`;
`SECOND S2 RUN AUTHORIZED: NO`; `FCORA: RECORDED, NOT EXECUTED` (after RVR-8, before Serious
Release; pass = `UNACCOUNTED / ORPHAN = 0`); R4-C / T1-A′ / T1-C′ / Time-to-Value /
Differentiation: OPEN. Cross-cutting deferred obligations are tracked in
`docs/governance/DEFERRED_OBLIGATIONS_REGISTER.md` (Master Obligation Index layer 6); this
register remains decision-only.

**D. Owner process directions — recorded at the post-W2-A-implementation sync (no OD identifiers
minted; none were issued).**

**D-1 — Cross-Layer Execution Assurance Standard.** The Owner/Lead Agent directed that a durable
**Cross-Layer Execution Assurance Standard**, derived from the W2-A lifecycle lessons, be
documented AFTER W2-A and BEFORE W2-B proceeds, through its own full lifecycle (Creator → Grill →
Independent Review → Owner acceptance → publication → merge). This record is the direction ONLY:
the standard is NOT created here, its contents are NOT pre-defined here, and nothing in this
record authorizes W2-B or any implementation. Obligation tracking: the Deferred Obligations
Register's dedicated row (CURRENT EXECUTION BLOCKER for W2-B execution). The future standard is
expected to establish continuous traceability practices that make the later FCORA gate (D-2)
easier and more reliable — a sequencing relationship only; the FCORA procedure is not embedded
in the standard by this record.

**D-2 — FCORA (Full Capability & Obligation Reconciliation Audit).** The Owner explicitly adopted
FCORA as a **MANDATORY, release-blocking future gate positioned after RVR-8 and before Serious
Release / Production Readiness**: every historically recorded capability, feature, obligation,
deferred item, future item, or implementation must resolve to an authoritative disposition
(`IMPLEMENTED & VERIFIED` / `DEFERRED & OWNED` / `SUPERSEDED` / `REJECTED` / `BLOCKED`); anything
without a defensible disposition is `UNACCOUNTED / ORPHAN`; the **Owner-required pass condition is
`Unaccounted / Orphan capability count = 0`**; reconciliation is BIDIRECTIONAL
(governance/docs ↔ implementation) and must detect omitted, partial, renamed/split/superseded and
dormant capabilities, deferred items without a durable owner, and runtime capabilities without a
governance owner. **FCORA is an audit gate, never a duplicate owner**: existing owners
(capabilities, workstreams, domain activation, deferred obligations, release-value gates, Owner
decisions) remain authoritative; FCORA audits them. Duplication was adjudicated before recording
(no existing gate owns this residual — see the register's FCORA row). This record is the
direction and obligation ONLY: FCORA is NOT executed here, its detailed contract (incl.
refinements such as partial-implementation ambiguity handling) is a future gate's own lifecycle
work. Obligation tracking: the Deferred Obligations Register §3 FCORA row (FRB).
