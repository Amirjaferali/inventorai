# InventorAI — Active Increment Contract

**Purpose:** the single, fixed location where the currently active phase/increment contract
is declared, plus the reusable contract template. Future agents discover the active contract
here (referenced from `CLAUDE.md` and `CURRENT_PROJECT_STATE.md`). Only one contract is
"active" at a time. When a new increment is authorized, replace the "Active contract"
section (append-only history is kept in the roadmap, not here).

---

## Declaration rule

- The **active contract** is whatever is recorded in the "Active contract" section below.
- An increment is authorized only by committed owner authorization; a contract here without
  such authorization is a template/placeholder, not an authorization.
- A contract governs bounded work at DEPTH 2/LEVEL 2 (and DEPTH 3/LEVEL 3 maintenance inside
  it). LEVEL 1 changes always need separate explicit owner authorization regardless of any
  contract.

## Reusable contract template

```
INCREMENT CONTRACT — <name>
Objective:                <what this increment achieves>
Owner authorization:      <reference to the committed owner authorization>
Risk level:               <LEVEL 1 | LEVEL 2 | LEVEL 3>
Allowed paths:            <exact paths that may change>
Forbidden paths:          <exact paths that must not change; default: engine/, web/, tests/,
                           domains/, database/, schemas/, prompts/, scripts/, CI, runtime/deploy,
                           main, accepted evidence>
Expected behavior:        <observable outcome>
Non-goals:                <explicitly out of scope>
Acceptance criteria:      <testable/verifiable gates>
Required tests:           <tests that must pass; or "none — documentation-only">
Tests not required:       <what is deliberately not tested>
Dependencies:             <prior gates, decisions, foundations>
Unresolved decisions:     <owner decisions still open, if any>
Stop conditions:          <when to stop and escalate>
Independent-review scope: <bounded reviewer questions per protocol §5>
Merge authority:          <who authorizes merge; default: owner, separately>
```

## Active contract
**Status:** NO ACTIVE (authorized) IMPLEMENTATION CONTRACT. A documentation-only **P4-1a — Durable-Store Proof**
increment-contract **CANDIDATE** (implementation **NOT authorized**) is recorded in the section **"P4-1a Increment
Contract Candidate (CONTRACT CANDIDATE ONLY — IMPLEMENTATION NOT AUTHORIZED)"** at the end of this file; it becomes an
active contract only after independent review, owner acceptance, merge, post-merge verification, and a separate
explicit P4-1a implementation authorization. Current live tip
`06be080e1a12108a5f4cd84060b756f9ba7c1878` (Merge PR #354 — post-P4-0 governance-currency synchronization; always
re-resolve from Git). The "Verified authoritative tip (synchronized closure pointer)" value below records the P4-0
closure merge and is not re-synchronized by this candidate.

**Current synchronized boundary (post-PR #353):** P4-0 — Readiness and Storage-Contract Proof was separately
authorized, implemented, independently reviewed, corrected, merged through PR #353, post-merge verified, and
formally closed by the owner. The authoritative merge commit recorded for that closure is
`286b83ffbd6916086c834658f9e16411ef4de4fe`. This synchronization records completed history only; it does not
activate or authorize P4-1, P4-2, any other Phase 4 increment, repository implementation, testing, runtime work,
publication, merge, release, or deployment. The P4-0 candidate block retained later in this file is a historical
contract-of-record and MUST NOT be interpreted as the currently active contract. Any next gate requires separate
explicit owner authorization.

**Verified authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified authoritative tip (synchronized closure pointer):** `286b83ffbd6916086c834658f9e16411ef4de4fe`
(Merge PR #353 — P4-0 implementation closure; always re-resolve the live tip from Git). Since the PR #327 gate, the bounded **remediation program** was
authorized and is now **FORMALLY CLOSED** (executable track COMPLETE): G-R01 CLOSED via PR #329/#330; DISC-007
CLOSED via PR #331 (Domain Registry v1.0 test reconciliation) and PR #332 (v1.0 validation hardening); tip at that
closure `239557e1` (PR #332 merge); repository-wide XPASS `0`; deferred Domain Registry v1.0 rules FORMALLY DEFERRED
— NOT IMPLEMENTED — NOT SOLVED. See `docs/governance/evidence/phase3_owner_decisions/REMEDIATION_PROGRAM_FORMAL_CLOSURE.md`.
**Since then, the following bounded gates have been separately owner-authorized, executed, merged, post-merge
verified, and FORMALLY CLOSED** (separate-session independent review is recorded in the respective owner
authorizations for these gates, except **PR #341 — G-PDSR**, for which merge, post-merge verification, and owner
closure are verified but a separate-session independent-review record and a letter verdict were not independently
located from inspectable PR evidence) (full merge SHAs; enumerated in
`docs/governance/evidence/phase3_owner_decisions/POST_PHASE_3_UX_IMPLEMENTATION_GATES_FORMAL_CLOSURE.md`):
PR #338 Phase 3E–3F governance sync (`a7a141ce7f25eab261e29a3e44930b76a9e7c1f4`); PR #339 G-IRB
(`fa054abe8979d9f1fe63fe9ca3122d9ce9df7078`); PR #340 G-SC0 (`94b6b9df61d655a9005599e1e18fe19de26e7338`);
PR #341 G-PDSR (`745aaaf77aaad838d418f597710194f61db3c98e`); PR #342 G-UX-SHELL
(`43453ceb87936d3a041e6edcccc0e7a8f16237a7`); PR #343 G-UX-TRUST (`cc71ab7acb39d9f772dbb1a347c78bc53f86beae`);
PR #344 G-UX-ENTRY (`41e51ba070c71e9a1ca1c351a680abb73d72204e`); PR #345 G-UX-GUIDED-LABEL
(`82cf45f94cf6a9701e10ad02c2f2d557add1ed55`); PR #346 G-GOV-SYNC-01 governance currency synchronization —
documentation-only (`6b375121648e08b882fcc2b475a5986f6a9508ef`); PR #347 G-UX-ANSWER-VALIDATION
(`722cf1c5d9b1756503ba92b34d0938fca3d1b695`); PR #348 G-UX-SNAPSHOT-DECISION — classification A, entry-point-only
refinement (`115239ffc4b4f2f1a108aae498cb1bbf016bbf08`). The **last formally closed implementation gate is
G-UX-SNAPSHOT-DECISION (PR #348)**. Current active work: **NONE** — no implementation work is presently
authorized; the next gate requires **separate explicit owner authorization**. Phase 3F bounded implementation
broadly, **Phase 4, Phase 5, WS17, and STG remain NOT AUTHORIZED / NOT STARTED**. The block below is retained as the prior
completed contract of record (Audit-Disposition & Lean-Governance gate, PR #327).

```
INCREMENT CONTRACT — Audit Disposition & Handover-Gap Canonicalization + Lean-Governance Adoption   [CLOSED — PR #327]
Objective:                Documentation-only canonicalization of the historical audit
                          disposition, the handover-to-repository gaps (DISC-001…018), the
                          deferred output/visualization capabilities (ACV/Download/Email), the
                          Phase 3B owner-decision agenda, stale-document clarification, and the
                          Lean Governance & Agent Continuity Protocol with its registers.
Owner authorization:      Owner messages "AUDIT DISPOSITION AND HANDOVER-GAP CANONICALIZATION"
                          and "LEAN GOVERNANCE AND AGENT CONTINUITY ADOPTION" (this gate).
Risk level:               Documentation-only (no code risk level; governance change).
Allowed paths:            docs/governance/** (new phase3_owner_decisions/ records; protocol,
                          state, register, contract, handover; append-only STALE_DOCUMENT_REGISTER,
                          plan, roadmap); CLAUDE.md (bounded boot-section); MVP_SCOPE_FREEZE.md
                          (append-only bounded allowance); root banners on NEXT_SESSION.md,
                          FUTURE_ARCHITECTURE_NOTES.md, VALIDATION_LOG.md, GOVERNANCE_MODEL.md.
Forbidden paths:          engine/, web/, tests/, domains/, database/, schemas/, prompts/,
                          scripts/, CI/workflow, runtime/deploy config, main, raw outputs
                          (incl. replay_debug.txt), accepted owner-decision/closure evidence
                          except the append-only edits listed above.
Expected behavior:        No runtime/product change. Governance clarity and lean continuity only.
Non-goals:                No Phase 3 activation; no Phase 3B decisions; no ACV/Download/Email/
                          sponsor/notice/privacy/Arabic-RTL/accessibility/STG design or impl.
Acceptance criteria:      Exact scope; forbidden paths unchanged; roadmap append-only; banners
                          do not overstate; phase allocations consistent; no capability described
                          as implemented; owner notes carried forward; no later gate activated.
Required tests:           None — documentation-only; DOCUMENTED NO-VALID-RED.
Tests not required:       Application/pytest execution (forbidden here).
Dependencies:             Phase 1 & 2 formally closed; OD-R/OD-S; live tip verification.
Unresolved decisions:     Phase 3B UX choices remain open (agenda-staged, not decided here).
Stop conditions:          Any forbidden-path change; base drift; a Level-1 need; a material
                          contradiction — stop and escalate.
Independent-review scope: Per protocol §5, plus: banners accurate; carve-out bounded; no
                          implementation authority granted; roadmap prefix preserved.
Merge authority:          Owner, separately (not by the execution agent).
```

---

## P4-0 Historical Increment Contract Record — SUPERSEDED AS ACTIVE AUTHORITY

**Current interpretation:** the text below is preserved as the pre-implementation P4-0 contract candidate and
historical execution record. P4-0 has since been completed and formally closed through PR #353. Nothing in the
historical wording below reopens P4-0 or authorizes P4-1/P4-2.

## P4-0 Increment Contract Candidate (CONTRACT CANDIDATE ONLY — IMPLEMENTATION NOT AUTHORIZED)

**Gate identity:** P4-0 — Readiness and Storage-Contract Proof (first, provider-free proof increment of Phase 4).
**Status:** `CONTRACT CANDIDATE ONLY` · `IMPLEMENTATION NOT AUTHORIZED` · `P4-0 NOT STARTED`. This block is a
documentation-only candidate produced under gate **G-P4-0-DOC-01**; it authorizes no code, tests, contract module,
datastore, schema, migration, dependency, or runtime work. It governs the *future* P4-0 increment only after
independent review (Lean §5), owner acceptance, merge, post-merge verification, and a **separate explicit P4-0
implementation authorization**.

**Governing evidence (cross-reference, not duplicated):**
`docs/governance/PHASE_4_DURABLE_DATA_AND_EVIDENCE_ENTRY_DECISION.md` (Phase 4 entry decision; obligations
`P4-OBL-DATA-01`, `P4-OBL-PROV-01`, `P4-OBL-REEVAL-01`, `P4-OBL-OUTPUT-01`, `P4-OBL-LIFE-01`);
`POST_OUTPUT_AI_ASSISTED_SPECIALIST_REFINEMENT_CANONICAL_DECISION.md` (AISR seven-owner model; `AISR-OBL-P4-*`);
decision **D17** (full re-evaluation is the safe default; targeted partial re-evaluation prohibited); the accepted
planning gate **G-P4-0-CONTRACT-DEFINITION** and owner decisions **D-P4-0-01 … D-P4-0-10** recorded below.

### 1. Purpose
Establish and validate the minimum **provider-free, datastore-neutral record contract** able to represent the
accepted Phase 4 durable records and prove **lossless round-trip fidelity + invariants** before any datastore is
chosen. A proof increment — not persistence.

### 2. Non-goals (D-P4-0-01)
No real datastore; no durable persistence; no database integration; no migrations; no runtime wiring; no Phase 4
generally; no P4-1; no P4-2; no SQL/ORM/Supabase/Postgres/SQLite/Redis/object/cloud storage/credentials; no
`web/app.py`/route/session-migration; no accounts/auth/ownership; no file storage/backup/restore/DR;
no retention/deletion execution; no AI/provider/WS17/STG/domain/exact-UX/PDF/email/ACV/API/billing/deploy. The
dormant `database/supabase_schema.sql` is reference-only and must not be adopted or modified.

### 3. Governing owner decisions (as recorded)
- **D-P4-0-01** provider-free, datastore-neutral contract proof (non-goals above).
- **D-P4-0-02** representation: Python dataclasses + explicit `to_dict`/`from_dict` + JSON-compatible dicts + stdlib
  `json`; no external serialization library; no ORM/datastore model; minimal, reversible naming/organization.
- **D-P4-0-03** a `contract_version` identifier is required; unsupported versions **fail explicitly**; no silent
  acceptance/coercion/downgrade.
- **D-P4-0-04** distinguish (A) authoritative accepted source data that must survive round-trip exactly from (B)
  derived/cached data that must not be treated as source truth; derived readiness/deterministic conclusions must not
  be restored as authoritative facts.
- **D-P4-0-05** preserve current runtime provenance verbatim (`OWNER_STATED`, `LEGACY_UNSPECIFIED`); mapping to the
  future Phase 4 vocabulary is adapter-only and deferred to P4-1; P4-0 must not rewrite provenance, populate
  `AI_PROPOSED`/`USER_MODIFIED_AI_PROPOSAL`, or create a final migration mapping.
- **D-P4-0-06** prove contract-level invariants (round-trip fidelity, stable-id preservation, append-only
  preservation, provenance/validation preservation, valid supersession/contradiction references, rejection of
  unknown references / self-supersession / cyclic supersession, explicit unknown-version failure); no durable
  enforcement/storage.
- **D-P4-0-07** RED proves missing capabilities (RED-1…RED-6 below), not missing files.
- **D-P4-0-08** GREEN (14 criteria below) with the scope limit that **P4-0 does not prove full deterministic replay
  from accepted source inputs** (that is P4-2); P4-0 only proves readiness-relevant contract data survives round-trip
  and can seed a fresh `derive_readiness` call.
- **D-P4-0-09** authorized/prohibited paths (below); if implementation proves `idea_state.py` must change, STOP and
  request a contract amendment.
- **D-P4-0-10** next action = this documentation-only contract candidate; P4-0 implementation remains unauthorized
  until candidate complete → adversarial self-review → separate-session independent review → owner acceptance →
  publish/merge → post-merge verification → separate implementation authorization.

### 4. Exact proposed implementation paths (selected by convention; confirmed at the implementation gate)
- **AUTHORIZED PATH 1 (new):** one datastore-neutral engine contract module — proposed `engine/record_contract.py`
  (snake_case, consistent with `engine/*.py`).
- **AUTHORIZED PATH 2 (new):** one focused test module — proposed `tests/test_p4_0_record_contract.py`.
- **CONDITIONAL PATH:** one minimal package export (e.g. an `engine/__init__.py` line) **only if** direct-import
  conventions prove it necessary — evidence to date shows engine modules are imported directly
  (`from engine.<mod> import ...`), so **no export is expected or authorized** unless proved.

### 5. Prohibited paths (must remain untouched in P4-0)
`engine/idea_state.py`; `engine/derived_readiness.py`; `engine/decision_workspace.py`; `web/app.py`; `database/`;
`schemas/`; `migrations/`; `requirements.txt`; `pytest.ini`; `prompts/`; `templates/`; `static/`;
CI/configuration; `ACTIVE_EXECUTION_ROADMAP.md` (except later closure recording); any Phase 5–7, WS17, or STG path.
Any need outside AUTHORIZED PATH 1/2 (or a proved CONDITIONAL export) triggers: **STOP — CONTRACT AMENDMENT
REQUIRED.**

### 6. RED design (D-P4-0-07 — behavior-based; not written in this gate)
For each: name · intended API under test · expected pre-implementation failure · why it is a genuine missing
capability · false-RED control · DB-free · AI-free · prohibited workaround.
- **RED-1 `test_accepted_input_roundtrip_is_lossless`** — API: `record_contract.from_dict(to_dict(record))`.
  Expected failure: no lossless accepted-input round-trip capability exists (no `from_dict` today). Genuine: core
  accepted-source truth cannot be serialized/restored. False-RED control: assert the *behavior* (deep equality) via
  the intended API, not module import. DB-free ✓ / AI-free ✓. Prohibited workaround: satisfying it via
  `decision_workspace` export-only `to_dict`.
- **RED-2 `test_provenance_and_validation_preserved_through_roundtrip`** — provenance/validation not preserved by any
  canonical round-trip. Genuine: no serializer preserves them. Control: assert exact values, not presence.
- **RED-3 `test_supersession_and_contradiction_validated_after_restore`** — links not validated post-restore.
  Genuine: no reload path. Control: include valid+invalid link fixtures.
- **RED-4 `test_readiness_relevant_state_supports_fresh_derivation_after_restore`** — readiness-relevant state cannot
  be serialized/restored and fed to a fresh `derive_readiness`. Genuine: no serializer. Control: re-run
  `derive_readiness` on restored state; never restore a cached readiness value.
- **RED-5 `test_unknown_fields_governed_by_versioned_contract`** — unknown/unsupported fields not governed. Genuine:
  no versioned contract. Control: assert explicit handling (reject/segregate), not silent drop.
- **RED-6 `test_unknown_contract_version_is_rejected`** — unknown version not rejected. Genuine: no version handling.
  Control: assert explicit error on an unknown version string.

### 7. GREEN criteria (D-P4-0-08 — scope-limited)
(1) datastore-neutral versioned contract exists; (2) authoritative fields serialize to JSON-compatible data;
(3) authoritative fields restore losslessly (**deep equality + explicit field-coverage assertion**);
(4) stable identifiers preserved (not regenerated); (5) append-only history preserved; (6) provenance/validation
preserved verbatim; (7) supersession/contradiction references validated; (8) invalid references and cycles fail
safely; (9) unsupported versions fail explicitly; (10) unknown fields handled explicitly (not silently dropped);
(11) derived/cached conclusions not restored as authoritative; (12) **readiness freshly derived from restored
readiness-relevant state (no cached-readiness restoration)**; (13) no database/ORM/driver/provider/external
dependency introduced; (14) existing governed suite does not regress. GREEN must not require or permit a real
durable store, adapter, transaction, migration, or runtime wiring. Fixtures must be **non-trivial** (multiple
records, multiple provenance/validation values, at least one supersession and one contradiction).

### 8. P4-0 / P4-1 / P4-2 boundary
**P4-0 PROVES:** contract representation; version behavior; JSON-compatible round-trip; authoritative-field
fidelity; identifier preservation; relationship validation; datastore neutrality; fresh readiness derivation from
restored readiness-relevant state.
**P4-0 DOES NOT IMPLEMENT:** a durable repository; transactions; datastore adapters; runtime persistence;
session-to-project creation; durable migration; persistence isolation; persistence failure handling; full
deterministic replay from accepted source inputs.
**P4-1 OWNS:** real durable project + accepted-input storage; repository/store behavior; datastore adapter;
transactions; runtime integration; durable supersession behavior; actual migration; persistent isolation;
durability-safe identifier strategy (the current sequence-based `record_id = f"rec_{n}"` is not collision-safe
across reload/concurrency — P4-1 resolves this); provenance migration/mapping.
**P4-2 OWNS:** deterministic rebuild/replay from accepted source inputs; deterministic output records;
stale-output invalidation; complete full re-evaluation; proof that readiness/output can decrease or change after an
accepted revision.

### 9. Authoritative-vs-derived, provenance, versioning, identifier, and relationship rules
- **Authoritative (round-trip exact):** `idea_id`; the append-only `assertions` ledger (all `AssertionRecord`
  fields incl. `contradicts`/`supersedes`/`superseded_by`); `criticality_confirmations`; `success_criteria`;
  owner-stated Evidence. **Derived (recompute / non-authoritative):** `maturity_level`, `gaps[].status`,
  `derive_readiness` output, `last_result`.
- **Provenance:** preserved verbatim; mapping adapter-only and deferred (D-P4-0-05).
- **Versioning:** `contract_version` present; unknown versions rejected explicitly (D-P4-0-03).
- **Identifiers:** preserved exactly, never regenerated on restore; sequence-id durability risk documented for P4-1.
- **Relationships:** supersession/contradiction references validated; unknown refs, self-supersession, and cycles
  rejected (mirrors the engine's existing acyclic O-2 / F-5 guards, at contract level only).

### 10. Non-trivial fixture requirement & false-green controls
The contract must explicitly guard against: shape-only dictionary tests; silently dropped fields; empty-only
fixtures; regenerated identities; cached-readiness comparison; unvalidated relationship strings; silently accepted
unknown versions; silently ignored unknown fields; hidden database imports; datastore-specific models;
implementation inside `idea_state.py` without amendment; accidental P4-1 work; and any claim of full deterministic
replay.

### 11. Dependency rule
Python standard library and existing project dependencies only (`json`, `dataclasses`, `typing`). **No** new
external dependency, DB driver, ORM, schema-generation library, or provider SDK. Any proposed new dependency is
**prohibited** for P4-0.

### 12. Rollback / reversibility
P4-0 writes no durable data. Rollback = revert the single bounded implementation commit; remove the new contract
module + focused test (+ any proved-necessary minimal export); **no data migration, no runtime-state recovery, no
persisted-record cleanup.**

### 13. Security statement
P4-0 introduces no credentials, no datastore, no network, no provider, and no persisted user data. Pure in-memory
value objects + deterministic tests.

### 14. Validation commands (for the future implementation gate)
Changed-path check; forbidden-path check (esp. `idea_state.py` untouched); no-new-dependency check
(`requirements.txt` unchanged); deterministic RED (fails for behavior) then GREEN; full governed suite must not
regress (`pytest`), DB-free and AI-free.

### 15. Required evidence package (future implementation gate)
Candidate SHA/parent/tree; changed paths; diffstat; RED evidence (failing for the right reason) and GREEN evidence;
suite result; no-dependency proof; `idea_state.py`-untouched proof; bundle + sha256; adversarial self-review.

### 16. Independent review · publication · merge · post-merge verification · stop gate
This candidate and the future P4-0 implementation each require **formal Lean §5 independent review in a genuinely
separate session** (same-session subagents do not qualify). Publication/PR/merge are owner-side (this environment's
writes are org-policy blocked). After merge, read-only post-merge verification is required. **Mandatory stop:** on
completion of this documentation candidate, stop; do not write RED tests or implementation code; do not create the
contract module; do not modify engine code; do not select a datastore or add a dependency; do not start P4-0/P4-1/
P4-2, Phase 5–7, WS17, or STG.

### Reusable contract-template rendering
```
INCREMENT CONTRACT — P4-0 Readiness and Storage-Contract Proof   [CANDIDATE — NOT AUTHORIZED]
Objective:                Provider-free, datastore-neutral record-contract proof with lossless round-trip + invariants.
Owner authorization:      G-P4-0-DOC-01 (documentation-only candidate); implementation NOT authorized.
Risk level:               LEVEL 2 (new isolated engine module + focused test; no runtime/persistence).
Allowed paths:            engine/record_contract.py (new); tests/test_p4_0_record_contract.py (new);
                          conditional minimal engine/__init__.py export only if proved necessary.
Forbidden paths:          engine/idea_state.py, engine/derived_readiness.py, engine/decision_workspace.py, web/,
                          database/, schemas/, migrations/, requirements.txt, pytest.ini, prompts/, templates/,
                          static/, CI/config, ACTIVE_EXECUTION_ROADMAP.md (except closure), Phase 5–7/WS17/STG.
Expected behavior:        Contract serialize/restore round-trip + invariant enforcement; no durable persistence.
Non-goals:                Durable store, adapter, transactions, migration, runtime wiring, full replay (P4-1/P4-2).
Acceptance criteria:      GREEN criteria 1–14 (§7); scope limit (no full deterministic replay).
Required tests:           RED-1…RED-6 → GREEN; deterministic, DB-free, AI-free; no suite regression.
Tests not required:       Any durable-store/datastore/provider test.
Dependencies:             stdlib + existing deps only; no new dependency.
Unresolved decisions:     Exact module name; whether a minimal export is needed (default: no).
Stop conditions:          Any need to modify idea_state.py or any forbidden path → STOP — CONTRACT AMENDMENT REQUIRED.
Independent-review scope: Per §5; plus: RED behavior-based; GREEN not P4-1/P4-2; readiness re-derived not cached;
                          provenance verbatim; no datastore/dependency; identifier + relationship invariants.
Merge authority:          Owner, separately (not by the execution agent).
```

**Preserved (unchanged by this candidate):** decision **D17**; the **AISR seven-owner model** (post-output
refinement is not a substitute for Phase 4/5/6/7/WS17/STG); Phase 4 implementation, P4-1, P4-2, Phase 5–7, WS17,
STG, provider selection, and exact UX all remain **NOT AUTHORIZED**.

---

## P4-1a Increment Contract Candidate (CONTRACT CANDIDATE ONLY — IMPLEMENTATION NOT AUTHORIZED)

**1. Gate identity & status.** P4-1a — Durable-Store Proof (first sub-increment of P4-1: a datastore-neutral durable
record store proved without runtime/web integration). Produced under gate **G-P4-1A-DOC-01**.
**Status:** `CONTRACT CANDIDATE ONLY` · `IMPLEMENTATION NOT AUTHORIZED` · `P4-1a NOT STARTED`. This block authorizes
no code, tests, database creation/opening/migration, dependency, or runtime work. It governs the future P4-1a
increment only after independent review (Lean §5), owner acceptance, merge, post-merge verification, and a **separate
explicit P4-1a implementation authorization**.

**2. Exact purpose.** Prove a **datastore-neutral repository/store abstraction with a Python standard-library SQLite
reference adapter** that durably persists and restores the accepted-source record set (the P4-0 record contract),
surviving an explicit store **close-and-reopen**, with atomic writes, rollback, project-scoped isolation,
durability-safe identifiers, provenance preservation, and validation — **without** any runtime/`web/` integration.

**3. Owner decisions (recorded; governs D-P4-1-01 … D-P4-1-10 in `OWNER_DECISION_REGISTER.md`).**
- **D-P4-1-01 Split:** P4-1 = P4-1a (durable-store proof) + P4-1b (runtime integration), each separately gated.
- **D-P4-1-02 Datastore:** datastore-neutral repository/store abstraction + a **stdlib SQLite reference adapter**;
  SQLite is a reference/MVP adapter, **not a permanent production commitment**; future PostgreSQL/other adapters
  remain possible through the abstraction.
- **D-P4-1-03 Dependencies:** **no new runtime dependency**; stdlib `sqlite3` only; no SQLAlchemy/psycopg/Supabase/
  provider SDK/server dependency.
- **D-P4-1-04 Existing sessions:** current in-memory sessions are **not recoverable and will not be migrated**;
  durability is future-facing (post-P4-1b). Do not imply existing temporary sessions can be restored.
- **D-P4-1-05 Identifiers:** new durable records use **durability-safe UUID-based identifiers**; **existing serialized
  identifiers are preserved exactly on load**; no adapter regenerates or silently rewrites existing record ids.
- **D-P4-1-06 Pre-account isolation:** unguessable capability identifiers; all reads/writes **scoped by project**;
  generic unavailable-project/session behavior preserved. **This is not authentication, ownership, or authorization**;
  no accounts or user ownership.
- **D-P4-1-07 Exclusions:** exclude FDC-001 persistence; P4-2 replay / durable output records / stale-output
  invalidation / full re-evaluation; Phase 5 accounts/authentication/ownership; providers; ACV; PDF; Email;
  production deployment.
- **D-P4-1-08 No web integration:** P4-1a must not modify `web/app.py`; runtime creation/retrieval/answer-submission/
  Keep-Refine/unavailable-session wiring is **P4-1b**.
- **D-P4-1-09 Required proof:** durable project creation; durable accepted-input round-trip; close-and-reopen
  persistence; atomic append; rollback with no partial write; append-only history preservation; cross-project
  isolation; stable identifier preservation; provenance preservation + allowed mapping; unknown-contract-version
  rejection; malformed-reference validation; readiness never persisted/accepted as authoritative; no P4-2 replay
  claim.
- **D-P4-1-10 Governance currency:** no additional governance-synchronization gate is required before defining P4-1a;
  this gate records the decisions and the P4-1a contract candidate.

**4. Authorized paths for future implementation.** ONE new datastore-neutral store module — proposed
`engine/record_store.py` (repository/store protocol + SQLite reference adapter + mapping to/from the P4-0 record
contract; exact name confirmed at the implementation gate); ONE focused test module — proposed
`tests/test_p4_1a_record_store.py`. CONDITIONAL: a minimal config/env helper for the SQLite file path **only if
proved necessary** and env-sourced with production fail-fast (mirroring the existing `INVENTORAI_*` pattern) — default
is to accept an explicit path/`:memory:`-then-reopen argument and add **no** config path.

**5. Prohibited & conditional paths.** PROHIBITED: `web/app.py` (D-P4-1-08); `engine/idea_state.py`,
`engine/record_contract.py`, `engine/derived_readiness.py`, `engine/decision_workspace.py`; `database/` (including the
dormant `supabase_schema.sql`); `schemas/`; `migrations/`; `requirements.txt`; `pytest.ini`; `prompts/`, `templates/`,
`static/`, `domains/`, `scripts/`, `benchmark/`; CI/`.github/`; governance docs except a later closure recording;
any Phase 5 / P4-2 / FDC-001 / provider path. CONDITIONAL: the config helper above. Any need beyond the authorized/
conditional set → **STOP — CONTRACT AMENDMENT REQUIRED**.

**6. Product & technical non-goals.** No runtime/web integration; no migration of current temporary sessions; no
general migration framework; no accounts/authentication/ownership; no replay/output persistence/stale-invalidation/
full re-evaluation; no retention-policy implementation, backup service, encryption-key management, deletion UI, or
production operations; no new dependency; no datastore server.

**7. Storage abstraction boundary.** A repository/store **protocol/interface** (responsibilities: create a project;
append an accepted-input record; record supersession/contradiction links; load a project's records; scoped lookup)
that is **datastore-agnostic**, so a future PostgreSQL/other adapter can be added without redesign. The store persists
and restores exactly the **P4-0 record-contract shape** (reuse `record_contract.to_dict`/`from_dict`); it introduces
no parallel schema authority and performs no evaluation.

**8. SQLite adapter boundary.** A stdlib `sqlite3` reference adapter behind the protocol: real on-disk (or explicit
file) SQLite; explicit **connection close and reopen**; project-scoped tables/rows keyed by project id; no ORM; no
server; single-file backup semantics are noted but backup/restore tooling is out of scope.

**9. Transaction & rollback rules.** Each mutation (project creation; accepted-input append with its link updates;
supersession edge; contradiction edges) is **atomic** (single transaction). A failed write **rolls back with no
partial record**. Loads validate the restored set via the record contract (reject invalid references / cycles /
unknown version) and **fail closed** — never silently repair.

**10. Identifier rules.** New durable records receive **durability-safe UUID-based** identifiers; **existing serialized
identifiers (`sid`, `idea_id`, `record_id`) are preserved exactly on load and never regenerated or rewritten**. The
P4-0 sequence-based `record_id` collision risk is resolved for **new** records only; previously serialized ids are
honored verbatim.

**11. Provenance rules.** Provenance/validation values are preserved **verbatim** (`OWNER_STATED`,
`LEGACY_UNSPECIFIED`, and the existing validation vocabulary). Any allowed mapping to the future target vocabulary is
**adapter-only**; **`AI_PROPOSED` / `USER_MODIFIED_AI_PROPOSAL` must not be populated** in P4-1a.

**12. Project-isolation rules.** All reads/writes are **scoped by project id**; one project's records must never be
returned for another. Identifiers are unguessable capability tokens (uuid). **This is lookup/isolation, not
authentication or authorization** (Phase 5).

**13. Unknown-version & malformed-record handling.** On load, an unknown/unsupported `contract_version` is rejected
explicitly (via the P4-0 record contract); malformed or invalid-reference records are rejected and never silently
coerced, dropped, or repaired.

**14. RED criteria (behavior-based; not written in this gate).** RED-1 accepted-input data does **not** survive store
**close/reopen** (impossible today — in-memory). RED-2 atomic **rollback is absent** (a failing multi-write leaves
partial state). RED-3 **project isolation is absent** (cross-project read). RED-4 an unknown persisted
`contract_version` is **not rejected through the future store**. RED-5 **append-only** records are not preserved after
reload. RED-6 **stable ids and provenance** do not survive durable round-trip.

**15. GREEN criteria.** Actual SQLite persistence; connection **close and reopen**; deterministic durable round-trip;
transaction rollback with **no partial records**; cross-project isolation; **stable ids preserved**; append-only
preserved; provenance preserved (+ allowed mapping, no AI values); unknown-version rejection; malformed-reference
rejection; **no persisted or cached readiness accepted as authority** (readiness re-derived from restored records via
the existing engine, never stored as a value); **provider-free and network-free** execution; **no runtime/web
integration claim**; **full governed-suite non-regression** after implementation.

**16. False-RED & false-GREEN controls.** RED must fail for missing **behavior**, not file/import absence, and must
not be satisfiable by an empty/`NotImplementedError` stub. **Fake durability is prohibited:** module-level
dictionaries; process-lifetime caches; reusing the same in-memory object; mocks that never close/reopen a real SQLite
connection; assertions based only on file existence. GREEN must **actually close and reopen** a real SQLite connection
and read the data back, use **non-trivial fixtures** (multiple records, multiple provenance/validation values, a
supersession, a contradiction, ≥2 projects), assert deep field equality, and re-derive readiness rather than compare a
cached value.

**17. Security & privacy preservation.** Persist only accepted-source records (the contract already excludes derived/
cached). Datastore file path/credential env-sourced with production fail-fast if adopted. No content logging. Validate
all loaded (potentially untrusted) serialized data via the record contract. Prevent cross-project leakage by scoping.
No backup exposure surface introduced (backup tooling out of scope). Preserve the **generic unavailable behavior**
(never disclose whether a project exists) — enforced at P4-1b, and P4-1a must not introduce a leak.

**18. R6/R16 preservation.** No `/tmp`/transcript disk write is introduced (R6); any datastore secret/path is
env-sourced with production fail-fast and no hard-coded secret (R16). The security-containment tests remain green
(non-regression).

**19. No cached readiness as authority.** Readiness is **never** serialized, persisted, or restored as an authoritative
value; it is always re-derived from restored accepted-source records by the existing engine. (Preserves D17 and the
P4-0 boundary.)

**20. P4-1a / P4-1b / P4-2 / Phase 5 separation.** **P4-1a:** durable store + SQLite adapter + mapping + transactions
+ durable ids + isolation + close/reopen + rollback/validation — **no web change**. **P4-1b:** runtime integration in
`web/app.py` (create/retrieve/answer-submission/Keep-Refine/unavailable-session), future-facing migration. **P4-2:**
deterministic replay, durable output records, stale-output invalidation, full re-evaluation. **Phase 5:** accounts,
authentication, ownership, verified email, account-linked authorization. All remain separately gated and NOT
AUTHORIZED.

**21. Evidence-package requirements (future implementation gate).** Candidate SHA/parent/tree; changed paths; diffstat;
RED evidence (failing for the right reason, incl. a stub-still-fails demonstration); GREEN evidence (real close/reopen
round-trip); full governed-suite result; no-new-dependency proof (`requirements.txt` unchanged); `web/app.py`- and
`idea_state.py`-untouched proof; bundle + sha256; §5A self-review.

**22. Independent-review requirement.** This candidate and the future P4-1a implementation each require **formal Lean
§5 independent review in a genuinely separate session**; same-session self-review/subagents do not qualify.

**23. Owner publication & merge boundary.** Publication/PR/merge are owner-side (this environment's writes are
org-policy blocked). No push/PR/merge in this gate; the candidate stops at delivery.

**24. Mandatory stop.** On completion of this documentation candidate, stop; do not write RED tests or implementation
code; do not create the store module; do not create/open/migrate a database; do not add a dependency; do not modify
`web/app.py`; do not start P4-1a/P4-1b/P4-2 or Phase 5.

### Reusable contract-template rendering
```
INCREMENT CONTRACT — P4-1a Durable-Store Proof   [CANDIDATE — NOT AUTHORIZED]
Objective:                Datastore-neutral durable record store + stdlib SQLite reference adapter, proved by
                          close/reopen round-trip + transactions + isolation, with no runtime/web integration.
Owner authorization:      G-P4-1A-DOC-01 (documentation-only candidate); implementation NOT authorized.
Risk level:               LEVEL 2 (new isolated engine module + focused test; no runtime/web/schema change).
Allowed paths:            engine/record_store.py (new); tests/test_p4_1a_record_store.py (new);
                          conditional minimal config/env helper only if proved necessary.
Forbidden paths:          web/app.py, engine/idea_state.py, engine/record_contract.py, engine/derived_readiness.py,
                          engine/decision_workspace.py, database/, schemas/, migrations/, requirements.txt,
                          pytest.ini, prompts/, templates/, static/, domains/, scripts/, benchmark/, CI/.github,
                          governance docs (except later closure), Phase 5 / P4-2 / FDC-001 / provider paths.
Expected behavior:        Durable SQLite persistence surviving close/reopen; atomic writes + rollback; project
                          isolation; durable-safe ids; provenance verbatim; validate-on-load; no readiness persisted.
Non-goals:                Runtime/web integration; session migration; accounts/auth/ownership; replay/output
                          persistence; retention policy; backup service; encryption key mgmt; deletion UI; provider.
Acceptance criteria:      GREEN criteria (§15); false-RED/false-GREEN controls (§16); full-suite non-regression.
Required tests:           RED-1..RED-6 → GREEN; deterministic, provider-free, network-free; real close/reopen.
Tests not required:       Any server/provider/web-route test.
Dependencies:             stdlib sqlite3 + existing deps only; NO new dependency.
Unresolved decisions:     Exact module name; whether a config helper is proved necessary (default: no).
Stop conditions:          Any need to modify web/app.py or any forbidden path → STOP — CONTRACT AMENDMENT REQUIRED.
Independent-review scope: Per §5; plus real close/reopen durability; no fake durability; ids/provenance preserved;
                          isolation not authorization; readiness never authoritative; no P4-1b/P4-2/Phase 5 work.
Merge authority:          Owner, separately (not by the execution agent).
```

**Preserved (unchanged by this candidate):** decision **D17**; the **AISR seven-owner model**; P4-1b, P4-2, Phase 5–7,
WS17, STG, provider selection, and exact UX all remain **NOT AUTHORIZED**.
