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
**Status:** ACTIVE CONTRACT-OF-RECORD = **P4-1b-2a Increment Contract Candidate — REV1** (gate
**G-P4-1B-2-DOC-01-REV1**, defined in the "P4-1b-2a Increment Contract Candidate — REV1" section below) —
**CORRECTED CONTRACT CANDIDATE — NOT YET MERGED · IMPLEMENTATION NOT AUTHORIZED · P4-1b-2a NOT STARTED**. REV1 corrects
independent-review blocking findings **B1** (mandatory token + affected existing tests), **B2** (token transport on
every answered-producing form), and **B3** (downstream `evt-*` semantic consequences). **The original DOC-01 candidate
`0e2a5cec24d71462eadbffa193e3467d40d506a0` carries independent-review verdict `C — REVISE AND RE-REVIEW`; it is
PRESERVED (unmerged) and NOT PUBLISHABLE, and is NOT amended.** A separately-claimed candidate
`518cfdfe0eca3fb0f52c88c5baea46c643d3c288` / bundle `p4_1b2_doc01_rev1_518cfdf.bundle` is **NOT an established
repository artifact and must not be relied upon**. **B3 determination (corrected):** a token-derived `evt-*`
answered-record id **materially changes deterministic output** in `engine/idea_development_outputs.py` and
`engine/requirement_landscape.py`, so **CONTRACT AMENDMENT / OWNER DECISION is REQUIRED** before P4-1b-2a implementation
(the earlier "feasibility PASS, no amendment" is superseded). **P4-1b-2b, P4-2, and Phase 5 remain NOT AUTHORIZED / NOT
STARTED.**

**P4-1b-1 is FULLY CLOSED** (implementation MERGED and POST-MERGE VERIFIED via PR #360; governance closure COMPLETE via
PR #361 `25dacb00295bcd3d34fd2cb5f789e9eae390ae11`). *(Preserved observation: the closure section below still reads
"pending its own merge", now satisfied by PR #361.)* The bounded P4-1b-1 (Runtime Store
Construction and Durable Project Create/Load) contract (gate **G-P4-1B-1-DOC-01**, corrected by **G-P4-1B-1-AMEND-01**)
is retained below as the fulfilled contract-of-record. *(The next paragraph's "GOVERNANCE CLOSURE is PENDING" wording is
historical and superseded by this status line.)* **P4-1b-1 implementation is MERGED and POST-MERGE VERIFIED
(technically COMPLETE); its GOVERNANCE CLOSURE is PENDING** until the G-P4-1B-1-CLOSURE-SYNC-01 candidate below is
itself separately reviewed, published, PR-created, merged, and post-merge verified. The bounded P4-1b-1 (Runtime Store
Construction and Durable Project Create/Load) contract (gate **G-P4-1B-1-DOC-01**, corrected by **G-P4-1B-1-AMEND-01**)
was fulfilled by the merged correction candidate `3179cd556673e5c5b6b596a052b0744bddab011a` (independent verdict
**B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**; **PR #360**, merge `cbd0ce3046b24631c23e482dadd413aaa42dea05`; changed
exactly `web/app.py`, `tests/test_p4_1b1_runtime_project_persistence.py`, `tests/conftest.py`; 3 files / 497 insertions
/ 2 deletions). The superseded first candidate `1eced7d280449b9c0842355a1882a9d3b731a633` (verdict C) remains preserved
intact and unmerged as superseded review evidence. **P4-1b-2, P4-2, and Phase 5 remain NOT AUTHORIZED / NOT STARTED**;
**P4-1b READ-ONLY DISCOVERY is COMPLETE** (owner decision package delivered) and authorizes nothing further.
**Product-truth boundary (unchanged):** P4-1b-1 proves durable **new-project** create/restart-survival/cold-load only;
the live application does **not** durably persist accepted answers, outputs, or complete ideas — that remains P4-1b-2.
See the **"P4-1b-1 Governance Closure Sync (G-P4-1B-1-CLOSURE-SYNC-01)"** section below for the merge, post-merge
verification, preserved observations, and the recorded procedural deviation. The P4-1b-1 contract and its
G-P4-1B-1-AMEND-01 amendment below are retained as the fulfilled contract-of-record and MUST NOT be interpreted as an
active authorization for further work.

**P4-1a closure boundary (post-PR #356):** the **P4-1a — Durable-Store Proof** increment was: recorded as a contract
candidate (merged PR #355); **separately and explicitly authorized for implementation by the owner** (a distinct
authorization — the PR #355 contract merge did **not** by itself grant implementation authority); implemented;
independently reviewed (verdict **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**, 0 blocking); published; merged through
**PR #356** (merge commit `dfa082af0e6f9c09222608ca47d088dc7e2df6a8`; candidate `faf57300121a74d3493e88fc1e9a9631f6ab5815`,
tree `415aee66eb92c6c3fd6683c36deb70756af6cb36`; changed exactly `engine/record_store.py` and
`tests/test_p4_1a_record_store.py`; 2 files, 426 insertions, 0 deletions); post-merge verified (candidate-ancestor
PASS; focused post-merge tests 11 passed; no prohibited path changed; no new runtime dependency); and **FORMALLY
CLOSED**. The "P4-1a Increment Contract Candidate" block retained later in this file is now a **historical
contract-of-record** and MUST NOT be interpreted as the currently active contract. **Product-truth boundary:** P4-1a
proves only a durable-store adapter capability; because P4-1b runtime integration has not started, the application
still uses the existing temporary in-memory session behaviour, no user-facing "saved"/"recoverable"/durable-project
claim is permitted, and existing in-memory sessions remain unrecoverable and unmigrated. Current live tip
`dfa082af0e6f9c09222608ca47d088dc7e2df6a8` (Merge PR #356 — P4-1a implementation closure; always re-resolve from Git).
The "Verified authoritative tip (synchronized closure pointer)" value below records an earlier closure merge and is
not re-synchronized by this entry.

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

## P4-1b-2a Increment Contract Candidate — REV1 — G-P4-1B-2-DOC-01-REV1 (CORRECTED CONTRACT CANDIDATE — NOT YET MERGED · IMPLEMENTATION NOT AUTHORIZED)

**0. Provenance & preservation.** REV1 supersedes the original P4-1b-2a contract candidate
`0e2a5cec24d71462eadbffa193e3467d40d506a0` (gate G-P4-1B-2-DOC-01), which received independent-review verdict
**C — REVISE AND RE-REVIEW** and is **PRESERVED intact, unmerged, NOT PUBLISHABLE, and NOT amended**. A previously
claimed `518cfdfe0eca3fb0f52c88c5baea46c643d3c288` candidate/bundle is **not an established repository artifact** and is
not relied upon. REV1 is a **new** candidate created from live tip `25dacb00295bcd3d34fd2cb5f789e9eae390ae11`.

**1. Gate identity & status.** P4-1b-2a — Durable Answered-Event Append and Web-Layer Idempotency. Gate
**G-P4-1B-2-DOC-01-REV1**. **Status:** `CORRECTED CONTRACT CANDIDATE — NOT YET MERGED` · `IMPLEMENTATION NOT AUTHORIZED`
· `P4-1b-2a NOT STARTED`. **P4-1b-2b, P4-2, Phase 5 remain NOT AUTHORIZED / NOT STARTED.** Owner decisions govern
`D-P4-1B-2-01 … -14` (unchanged) plus the REV1 corrections `D-P4-1B-2-REV1-B1/B2/B3` and clarifications
`D-P4-1B-2-REV1-C1 … C8` in `OWNER_DECISION_REGISTER.md`.

**2. Objective (unchanged).** Prove durable accepted-answer evidence: durably append each answered-submission
accepted-input event exactly once, persist-before-acknowledge, with mandatory web-layer idempotency — no full session/
progression/deliverable/output/Keep-Refine/account durability, no replay (P4-2).

**B1 — Mandatory token & affected existing tests (correction).** A server-issued token is **mandatory for every
answered submission**; **no tokenless fallback** is permitted (a POST resolving to `answered` without a valid token
fails closed, generic behaviour, no acceptance). The future implementation MUST enumerate and update **only** the
existing test files that genuinely POST answered submissions, **solely to obtain and submit a real valid token**, with
**no weakened assertion, no skipped behaviour, and no conftest auto-injection of tokens** (auto-injection would create a
false-green path and is prohibited). **Enumerated affected test paths (evidence, live tip):** `test_web_app.py`,
`test_p4_1b1_runtime_project_persistence.py`, `test_security_containment_r6_r16.py`, `test_increment_1a_actions.py`,
`test_structured_criticality.py`, `test_success_criteria.py`, `test_gux_snapshot_decision.py`,
`test_s04_guided_answer_validation.py`, `test_actionable_validation_plan.py`, `test_advisory_panel_precedence.py`,
`test_deliverable_hygiene.py`, `test_domain_gate_entry_ux.py`, `test_guided_answer_coauthoring_increment_1.py`,
`test_guided_uncertainty_support.py`, `test_layer1_feedback_wording.py`, `test_more_detail_needed_scaffolding.py`,
`test_plain_language_result_feedback.py`, `test_requirement_landscape_synthesis.py`,
`test_unified_risk_safety_presentation.py`, `test_acknowledged_unknown_fragment_capture.py`,
`test_causal_connective_substance_gate.py` (final set re-verified at the implementation gate). **Any answered-producing
test path not identified by evidence → STOP — CONTRACT AMENDMENT REQUIRED.**

**B2 — Token transport on every answered-producing form (correction).** Token transport MUST cover **every** form whose
POST resolves to `answered`. Verified answered-producing forms (`web/templates/session.html`): (i) the **main answer
form** (`name="response"` + `action=answered`); (ii) the **criticality-correction free-text form**, whose POST carries
**no `action` field** and is therefore treated as `answered` by the legacy-compatibility rule in
`web/app.py::submit_answer`. Both MUST carry a hidden server-issued token. The contract REQUIRES an **inventory/route-form
regression** proving **no answered-producing form bypasses the token requirement** (fail closed if any does).

**B3 — Downstream `evt-*` semantic consequences (correction; CONTRACT AMENDMENT / OWNER DECISION REQUIRED).** A
token-derived event id (`evt-*`) replacing the positional `rec_N` on an accepted answered record is **NOT semantically
neutral**. Static evidence at the live tip:
  * `engine/idea_development_outputs.py::_record_sort_key` (`_REC_ID_RE = ^rec_(\d+)$`): `rec_N` ids receive tuple lead
    **0** (numeric order) and **always precede** non-`rec_N` ids (lead 1/2). An `evt-*` answered record therefore sorts
    differently, **changing which record `_select_record` picks** for the deterministic next-development-step output.
  * `engine/requirement_landscape.py`: mirrors the same `rec_N` sort key (`_rec_sort_key`) **and embeds `record_id` into
    derived identifiers and metadata** — `requirement_id = _record_id_prefix(kind) + record.record_id` (e.g.
    `req:assertion:rec_3` → `req:assertion:evt-…`), `anchor_reference`, `ResolvingAction`, and contradiction-pair
    ordering (`_order_pair`). `evt-*` ids therefore **change derived requirement identifiers, rationale metadata, and
    pair ordering** — deterministic outputs.
The contract REQUIRES **protected regression tests for mixed `rec_N` / `evt-*` ledgers and deterministic output
behaviour**. **Because static inspection already demonstrates a material change, this contract does NOT authorize the
`evt-*` id scheme for implementation.** **DETERMINATION: CONTRACT AMENDMENT / OWNER DECISION REQUIRED** before P4-1b-2a
implementation — the owner must choose one of: **(a)** explicitly accept the changed deterministic output (owner
decision + regenerated golden expectations); **(b)** authorize a **bounded engine amendment** so durable event ids are
order-equivalent to `rec_N` and embed acceptably in `idea_development_outputs.py`/`requirement_landscape.py`; or
**(c)** adopt an idempotency design that keeps `rec_N` as the identifier consumed by the derived-output engines. **The
semantic change must NOT be silently normalized or accepted.** *(This corrects the original candidate's erroneous
"STABLE RECORD-ID FEASIBILITY: PASS — no amendment".)*

**Clarification C1 — Web-layer staging (D-P4-1B-2-REV1-C1).** On an answered submission the implementation MUST: clone
the live `IdeaState`; run evaluation and create the `AssertionRecord` on the **staged copy**; set the canonical event
id; **append durably**; and **only after durable success** publish staged state, transcript, and `last_result` into
`SESSION_STORE`. On append failure it MUST discard the staged copy and leave live memory unchanged (persist-before-ack;
no partial publication).

**Clarification C2 — Duplicate retry (D-P4-1B-2-REV1-C2).** A duplicate valid-token retry MUST cause: no second durable
event; no second progression; no reconstructed `last_result`; no claim of reproducing the prior response; a no-op with a
`show_session` redirect where truthful, otherwise a generic redirect.

**Clarification C3 — IntegrityError handling (D-P4-1B-2-REV1-C3).** No `sqlite3.IntegrityError` may be **automatically**
classified as a duplicate. On IntegrityError the runtime MUST reload the durable contract and confirm the **exact event
id, same project, and same logical accepted content** before treating it as an idempotent duplicate. **Same token with
different content fails closed.** Unrelated integrity failures remain **generic store failures** (fail closed).

**Clarification C4 — Concurrency boundary (D-P4-1B-2-REV1-C4).** The bounded MVP relies on the existing
`threaded=False` single-process/single-thread serving topology (G-P4-1B-1-AMEND-01); the store **primary key is the
durable duplicate backstop**; multi-thread/multi-worker behaviour is **out of scope**.

**Clarification C5 — Canonical token/event-id model (D-P4-1B-2-REV1-C5).** A **cryptographically strong** server-issued
token; **URL/form-safe bounded** encoding; **exact-match** validation; **hidden-form transport only**; **never** placed
in URLs, logs, or user-facing errors. **One precise digest model is chosen: the canonical durable event id is
`evt-` + hex SHA-256 of (`sid` ‖ separator ‖ raw token), truncated to a bounded length** — i.e. the raw token is
**hashed, not stored raw**, and **`sid` is included in the canonical derivation** so the event id is project-bound.
*(This id scheme is subject to the B3 amendment/owner decision above before implementation.)*

**Clarification C6 — Durable-success / memory-failure (D-P4-1B-2-REV1-C6).** If the durable append succeeds but the
in-memory publish fails: the durable ledger remains authoritative; the temporary `SESSION_STORE` entry is invalidated;
the runtime redirects safely; it does **not** continue from partially published progression, does **not** append again,
and does **not** claim replay or exact resume.

**Clarification C7 — Pre-append scanning (D-P4-1B-2-REV1-C7).** A full-ledger `load_contract(sid)` load/scan is
acceptable for this bounded MVP and is recorded as **O(n)**; **no `project_ids()` exposure**; a direct-record lookup
optimization is **deferred**.

**Clarification C8 — Mixed-id state (D-P4-1B-2-REV1-C8).** Durable `evt-*` answered records may coexist with legacy or
volatile `rec_N` non-answer records; **protected regressions MUST cover this mixed-id state** (feeds directly into B3).

**Ordering / failure / reconciliation / restart / product-truth (unchanged from DOC-01, retained):** store `seq`
ordering, one accepted event per token, no cross-project append; the ten-case failure model with generic non-disclosing
errors and no raw SQLite/user-content logs; durable-authoritative reconciliation; restart guarantees ledger + fresh
readiness only (no progression/deliverable restore — P4-2); product may claim only **durable accepted-answer evidence**
and must not claim saved project / fully saved idea / durable outputs / "resume exactly where you left off" / complete
session resume / Keep-Refine durability / account-owned records.

**Permitted paths (future implementation).** `web/app.py`; `web/templates/session.html` (hidden token field on **both**
answered-producing forms — B2); ONE focused test module `tests/test_p4_1b2a_durable_answer_append.py` (new);
`tests/conftest.py` (reuse only — **no token auto-injection**); and the **enumerated B1 existing test files** updated
**only** to obtain/submit a real token without weakening assertions. **Prohibited (unless a separately reviewed
amendment authorizes):** `engine/idea_state.py`, `engine/record_store.py`, `engine/record_contract.py`,
`engine/derived_readiness.py`, `engine/idea_development_outputs.py`, `engine/requirement_landscape.py`,
`engine/deliverable_assembler.py`, `requirements.txt`, `pytest.ini`, `database/`, `schemas/`, migrations; accounts/
auth/ownership; outputs; replay; durable Keep/Refine; retention/deletion; local-dev permission hardening; P4-1b-2b;
P4-2; Phase 5. **NOTE:** the B3 resolution may require an authorized amendment touching
`engine/idea_development_outputs.py` and/or `engine/requirement_landscape.py`; that is a **separate** authorization, not
granted here.

**RED / GREEN (corrected).** RED-1…11 (DOC-01) **plus**: RED-B1 an answered POST without a valid token **fails closed**
(no acceptance); RED-B2 an inventory/route-form test proves **no answered-producing form** (main + criticality-correction)
bypasses the token; RED-B3 mixed `rec_N`/`evt-*` ledger **deterministic-output** regressions (next-development-step
selection + derived requirement identifiers) — these are **gating**: if they demonstrate a material change (as static
analysis indicates), implementation STOPS pending the B3 amendment/owner decision; RED-C3 IntegrityError is **not**
auto-classified as duplicate (same-token-different-content fails closed). GREEN additionally requires: real token
lifecycle end-to-end; staging (C1) with persist-before-publish; idempotent retry (C2) with no second event/progression;
IntegrityError confirmation-by-reload (C3); no false-green via conftest/`SESSION_STORE`; protected regressions incl.
mixed-id (C8) pass **only** under an owner-approved B3 resolution; full governed suite green.

**Preserved (unchanged by REV1):** decision **D17**; the **AISR seven-owner model**; the original `0e2a5ce` candidate and
its verdict-C history; all P4-1b-1 implementation-review and post-closure documentation observations (closure
"pending its own merge" now satisfied by PR #361; non-material tree-attribution note; stale "current" wording;
authorization-record lag) — recorded, not fixed here. **P4-1b-2b, P4-2, Phase 5–7, WS17, STG** remain **NOT
AUTHORIZED**.

---

## P4-1b-1 Increment Contract Candidate (CONTRACT CANDIDATE ONLY — IMPLEMENTATION NOT AUTHORIZED)

**1. Gate identity & status.** P4-1b-1 — Runtime Store Construction and Durable Project Create/Load (the first
runtime-integration sub-increment of P4-1b, itself the first runtime half of P4-1). Produced under gate
**G-P4-1B-1-DOC-01** on live tip `e4f9cd97e1b4329b98f1678412a6a36b9d7238bf` (Merge PR #357; always re-resolve from Git).
**Status:** `CONTRACT CANDIDATE ONLY` · `IMPLEMENTATION NOT AUTHORIZED` · `P4-1b-1 NOT STARTED`. This block authorizes
no `web/app.py` change, no test, no database creation/opening, no dependency, and no runtime work. It governs the
future P4-1b-1 increment only after independent review (Lean §5, genuinely separate session), owner acceptance,
publication, merge, post-merge verification, and a **separate explicit P4-1b-1 implementation authorization**.

**2. Authorized objective (future implementation).** Prove, through the application boundary, that a **new project is
durably created at `/start`, survives a real process/store restart, and is cold-loaded back into runtime** from the
merged P4-1a durable store (`engine.record_store.SqliteRecordStore`) via the P4-0 record contract — while preserving
the existing generic unavailable behaviour and R6/R16 containment. The future implementation may ONLY: construct the
store at application startup; resolve the SQLite path safely; create a durable empty/new project during `/start`;
use the **`sid` as the durable `project_id`** (one unified capability); load a durable project after memory loss via
**`load_contract(sid)`**; rebuild minimum runtime state; preserve generic unavailable behaviour; translate storage
errors at the web boundary; and prove real restart/cold-load behaviour. Nothing else.

**3. Owner decisions (recorded; governs D-P4-1B-01 … D-P4-1B-11 in `OWNER_DECISION_REGISTER.md`).**
- **D-P4-1B-01 Split:** P4-1b = **P4-1b-1** (Runtime Store Construction + Durable Project Create/Load) + **P4-1b-2**
  (Accepted-Input Append + Keep/Refine Runtime Integration). Each requires a separate contract, separate implementation
  authorization, RED/GREEN evidence, independent review, owner publication decision, owner merge decision, post-merge
  verification, and formal closure. **P4-1b-2 is NOT authorized by this gate.**
- **D-P4-1B-02 Runtime state model:** for the current MVP, `SESSION_STORE` remains the active in-memory state during a
  live process; **SQLite is the durable mirror and cold-reload source**; when memory is absent and a durable project
  exists, state may be rebuilt from `load_contract(sid).to_state()` (the `sid` IS the durable `project_id`);
  **readiness must always be derived again**;
  **no cache framework or invalidation platform is authorized**. If durable persistence fails, the application must not
  present the in-memory state as successfully durable.
- **D-P4-1B-03 Store lifecycle:** **one application-scoped `SqliteRecordStore` instance** for the current
  single-process MVP. Explicitly defer multi-worker topology, connection pools, per-request connection architecture,
  WAL tuning, production database selection, and provider-managed databases. SQLite remains a reference/MVP adapter.
- **D-P4-1B-04 Configuration:** use **`INVENTORAI_DB_PATH`**. Local/test execution may use a safe explicit file path;
  **pytest must use test-managed temporary directories**; **no repository-tracked `.db`/`.sqlite`/user-data file is
  permitted**; **production must fail fast** when the path is missing, unusable, or unsafe; **no new runtime
  dependency**. The exact local default must be specified truthfully and must not write user content to an uncontrolled
  `/tmp` transcript path (R6).
- **D-P4-1B-05 Durability start policy:** P4-1b-1 durability applies to **newly created projects only**. Existing lost
  in-memory sessions are **not recoverable, not migratable, and must not be claimed restorable**. Promotion of
  already-live pre-integration sessions is **excluded** from the first increment.
- **D-P4-1B-06 Unified pre-account capability identifier (correction, BF-1):** for P4-1b-1, **`sid` and the durable
  `project_id` are the SAME `uuid4` value** — one unguessable pre-account capability used for route/session lookup,
  durable project lookup, and cold-load after process restart. The route capability IS the durable project key:
  **cold-load calls `load_contract(sid)`**; **no separate `sid`→`project_id` mapping table, no scan through
  `project_ids()`, and no derived/reversible mapping layer is introduced**. It is **lookup only** — not authentication,
  ownership, account authorization, or verified identity. **`project_ids()` must never be exposed** through route, API,
  template, UI, or user-facing runtime behaviour. This capability model is temporary before Phase 5 (which may later
  introduce account ownership and a separately governed external/public identifier model). P4-1b-1 does **not** use
  `new_record_id()` (accepted-input record creation is P4-1b-2). **No modification to `engine/record_store.py` or
  `engine/record_contract.py` is required by this model** (`create_project(contract, project_id=sid)` and
  `load_contract(sid)` are already supported by the merged P4-1a store).
- **D-P4-1B-07 Project creation order:** (1) validate the `/start` request; (2) generate **one** `uuid4` capability
  value used as **both** `sid` and `project_id`, plus an `idea_id`; (3) construct the initial `IdeaState`; (4) create
  the durable project through the store **with `project_id = sid`**; (5) **only after durable creation succeeds**,
  create the `SESSION_STORE[sid]` entry; (6) redirect to the session. On durable-creation failure: do not advertise or
  retain a successful live session; fail closed; show one generic unavailable response; log no user content.
- **D-P4-1B-08 Cold-load behaviour:** when a valid capability (`sid`) is presented and `SESSION_STORE` has no live
  entry: attempt **`load_contract(sid)`** (the `sid` IS the durable `project_id`); validate through the existing P4-0
  record contract; reconstruct `IdeaState` from the contract; derive readiness freshly; create only the minimum
  temporary runtime entry needed; **do not restore transcript or cached `last_result` as authoritative**. No
  `sid`→`project_id` mapping lookup and no `project_ids()` scan is used.
- **D-P4-1B-09 Error translation:** translate storage errors **at the web integration boundary**; **do not modify
  `engine/record_store.py` by default**. Minimum categories: `ProjectNotFound` → generic unavailable; malformed/
  unsupported contract → generic unavailable, fail closed; database unavailable/locked/path error → generic temporarily
  unavailable; unknown SQLite error → generic unavailable, fail closed. Permitted internal logging: error class,
  operation, non-content technical identifier when safe. Prohibited logging: idea text, answers, assertion payloads,
  serialized records, transcript content.
- **D-P4-1B-10 Generic non-disclosure:** the user-facing result must not reveal whether a project never existed, a
  capability was wrong, a project was deleted/unavailable, the database failed, the contract was malformed, or the
  contract version was unsupported. Use **one generic unavailable behaviour** consistent with existing session handling.
- **D-P4-1B-11 Product-truth boundary:** P4-1b-1 may prove durable creation of a **new** project, process-restart
  survival of that created project, and cold loading into runtime. It must **not** claim: accepted answers are durably
  persisted; Keep creates a durable snapshot; Refine is durably recorded; durable output exists; version history
  exists; recovery of existing temporary sessions; or that user ideas are fully saved. **Full accepted-input durability
  requires P4-1b-2.**

**4. Authorized paths for future implementation.** `web/app.py` (store construction at startup; `INVENTORAI_DB_PATH`
resolution; durable project creation in `/start`; `sid`↔`project_id` association; cold-load of a durable project;
minimum runtime-state rebuild; web-boundary storage-error translation; preserved generic unavailable behaviour;
**explicit single-threaded MVP serving mode `threaded=False` — G-P4-1B-1-AMEND-01 / D-P4-1B-1-AMEND-01**);
ONE focused test module — **`tests/test_p4_1b1_runtime_project_persistence.py`** (new); and, per
**G-P4-1B-1-AMEND-01 / D-P4-1B-1-AMEND-02**, **`tests/conftest.py`** (new) — authorized ONLY for a minimal pytest
isolated-DB fixture (see the "P4-1b-1 Contract Amendment" section below).

**5. Conditional paths.** A small new **configuration helper** (e.g. a `web/`-side path resolver) **only if** inline
configuration would make `web/app.py` unsafe or untestable — env-sourced with production fail-fast, mirroring the
existing `INVENTORAI_*` pattern; default is inline resolution and **no** new file. Existing tests
(`tests/test_web_app.py`, `tests/test_security_containment_r6_r16.py`) may be updated **only** to inject a temporary DB
safely; existing assertions must not be weakened.

**6. Prohibited paths (by default).** `engine/record_store.py`, `engine/record_contract.py`, `engine/idea_state.py`,
`engine/derived_readiness.py`, `requirements.txt`, `database/` (incl. dormant `supabase_schema.sql`), `schemas/`,
`pytest.ini`, templates/static files, `prompts/`, `domains/`, `scripts/`, `benchmark/`, CI/`.github/`/deployment files,
and any Phase 5 / P4-2 / P4-1b-2 / FDC-001 / provider path. **No new `sid`→`project_id` mapping module and no new
database table/schema are introduced** (the unified capability makes both unnecessary — D-P4-1B-06; the merged P4-1a
schema is reused unchanged). If implementation genuinely requires a prohibited or unlisted path → **STOP — CONTRACT
AMENDMENT REQUIRED**.

**7. Store lifecycle.** One app-scoped `SqliteRecordStore` constructed at startup over a real on-disk SQLite file
resolved from `INVENTORAI_DB_PATH`; single-process MVP; `close()` on teardown where applicable. Multi-worker/pooling/
WAL/production-datastore topology is explicitly deferred (D-P4-1B-03).

**8. Configuration rules.** `INVENTORAI_DB_PATH` env-sourced; safe explicit local/test path; pytest uses `tmp_path`;
**no repository-tracked database file**; production fail-fast on missing/unusable/unsafe path; **no new dependency**
(stdlib `sqlite3`); no uncontrolled `/tmp` user-content write (R6).

**9. Project creation ordering.** Exactly D-P4-1B-07 (validate → **one `uuid4` used as both `sid` and `project_id`**
(+ `idea_id`) → IdeaState → **durable create with `project_id = sid`** → `SESSION_STORE[sid]` entry → redirect),
durable-create as the commit point; fail closed with one generic response and no live session on failure.

**10. Cold-load behaviour.** Exactly D-P4-1B-08: **`load_contract(sid)`** (the `sid` IS the durable `project_id`) →
P4-0 validation → `to_state()` → fresh `derive_readiness` → minimum runtime entry; transcript and cached `last_result`
are never restored as authority; no mapping lookup or `project_ids()` scan.

**11. Source-of-truth model.** SESSION_STORE = active working cache within a live process; SQLite = durable mirror and
cold-reload source (keyed by the `sid`=`project_id` capability); readiness always re-derived; no cache-invalidation
framework and **no `sid`→`project_id` mapping module or table** (D-P4-1B-02, D-P4-1B-06). This is not P4-2 replay.

**12. Capability-isolation boundary.** A **single** unguessable `uuid4` used as both `sid` and `project_id` (no separate
identifier, no mapping); project-scoped store access; lookup/isolation only — **not** authentication/ownership/
authorization (Phase 5). `project_ids()` never exposed; cross-project isolation proved with two distinct capabilities.

**13. Error translation.** Exactly D-P4-1B-09 — at the web boundary; `record_store.py` unmodified by default; storage
errors mapped to generic user-facing responses; non-content technical logging only.

**14. Generic unavailable behaviour.** Exactly D-P4-1B-10 — one generic unavailable response consistent with the
existing missing-session redirect; never discloses project existence, capability validity, deletion, DB failure, or
contract/version state.

**15. Product-truth boundary.** Exactly D-P4-1B-11 — P4-1b-1 proves durable **new-project** create/restart-survival/
cold-load only; **no accepted-answer persistence, Keep/Refine durability, durable output, version history, session
recovery, or full-save claim** (all P4-1b-2 or later).

**16. RED criteria (behaviour-based; not written in this gate).** Each RED states its expected current failure, the
genuine missing capability, a false-RED control, and the prohibited shortcut.
- **RED-1** `/start` does **not** currently create a durable project. *Current failure:* no store call exists (grep-proven
  unwired). *Missing capability:* durable project creation at the boundary. *False-RED control:* assert a real row via a
  reopened store, not an in-memory dict. *Prohibited shortcut:* asserting only `SESSION_STORE` contents.
- **RED-2** a project does **not** survive clearing `SESSION_STORE` and reconstructing the app. *Failure:* in-memory
  state is lost on restart. *Missing:* durable persistence. *False-RED control:* **preserve only the route `sid` value**
  across restart; real store close + a new store on the same file; discard the original app/store/SESSION_STORE/
  IdeaState objects. *Shortcut:* reusing a module-global or stale memory.
- **RED-3** a cold request **cannot** currently load durable state. *Failure:* missing-sid redirects with nothing to
  load. *Missing:* cold-load path. *Control:* clear SESSION_STORE; create a fresh runtime/store; call the route with the
  **same `sid`**; prove **`load_contract(sid)`** restores the correct project. *Shortcut:* same-object reuse, a mapping
  table, or a `project_ids()` scan.
- **RED-4** failed project creation must **not** leave a live `SESSION_STORE` entry. *Failure:* no durable step, so no
  fail-closed ordering. *Missing:* create-before-advertise ordering + compensation. *Control:* inject a durable-write
  failure; assert no live entry and one generic response. *Shortcut:* swallowing the error.
- **RED-5** unknown project capability must remain **generic**. *Failure/known-good:* generic redirect exists; guard
  against regression. *Missing:* durable-missing path kept generic. *Control:* assert identical generic response.
  *Shortcut:* leaking existence.
- **RED-6** malformed or unsupported stored contract must **fail closed**. *Failure:* no load-validation path yet.
  *Missing:* fail-closed cold-load. *Control:* store a bad `contract_version`; assert generic unavailable, no traceback.
  *Shortcut:* 500/traceback or silent repair.
- **RED-7** database-unavailable behaviour must remain **generic**. *Failure:* no DB path/handling yet. *Missing:*
  boundary translation. *Control:* point at an unusable path; assert generic temporarily-unavailable. *Shortcut:* raw
  `sqlite3` error to the user.
- **RED-8** cross-project capability isolation must hold. *Failure:* project scoping not exercised at runtime. *Missing:*
  project-scoped cold-load. *Control:* create two projects; assert neither loads the other. *Shortcut:* shared id.
- **RED-9** readiness must be **freshly derived** after cold load. *Failure:* no reload path. *Missing:* re-derivation.
  *Control:* compare `derive_readiness` of the cold-loaded `to_state()` against a fresh derivation; never a stored value.
  *Shortcut:* persisting/restoring a readiness value.
- **RED-10** transcript and cached `last_result` must **not** be restored as authoritative. *Failure:* nothing durable
  yet. *Missing:* authoritative-input boundary. *Control:* assert the cold entry carries no restored transcript/
  last_result authority. *Shortcut:* persisting transcript (violates R6).
- **RED-11** **no repository-tracked database file** may be created. *Failure/guard.* *Missing:* safe path discipline.
  *Control:* assert the SQLite file lives only under `tmp_path`; `git status` clean of DB artifacts. *Shortcut:* writing
  a DB into the repo tree or uncontrolled `/tmp`.

**17. GREEN criteria (future implementation).** Real SQLite file in a pytest-managed temporary directory; `/start`
durably creates a new project keyed by the `sid`=`project_id` capability; the store connection and original runtime
objects are discarded; a **new** runtime/store instance opens the **same** database; `SESSION_STORE` begins empty; a
cold request **presenting the same `sid`** reconstructs the correct `IdeaState` via **`load_contract(sid)`** (no mapping
table, no `project_ids()` scan, no stale memory); readiness is newly derived; no transcript or cached result becomes
authoritative; failed durable creation creates no live session; unknown/malformed/unavailable conditions produce
**one** generic response; two capabilities cannot cross-load each other; **no `project_ids()` exposure**; **no new
dependency**; **no P4-1b-2 behaviour**; **full governed suite remains green**.

**18. False-RED & false-GREEN controls.** RED must fail for missing **behaviour**, not import/file absence, and must
not be satisfiable by an empty stub. **False-green is prohibited through:** reused `SESSION_STORE`; a reused `app`
instance when restart behaviour is claimed; a reused store connection; a reused `IdeaState` object; a mocked/fake
datastore; `:memory:` SQLite for restart proof; database-file-existence-only assertions; direct insertion of expected
state into `SESSION_STORE`; bypassing route behaviour by calling store methods only; **a `sid`→`project_id` mapping
table, a `project_ids()` scan, or any stale-memory substitute for `load_contract(sid)`**; or weakening existing
missing-session or security assertions. GREEN must exercise the **route** through Flask `test_client`, preserve **only
the `sid` value** across restart, actually close and reopen a **real** SQLite file, discard originals, and assert
reconstructed field equality.

**19. Security & privacy preservation.** Preserve **R6** (no transcript/user-content disk or log write) and **R16**
(env-sourced debug/secret, no hard-coded values, production fail-fast); no repository-tracked DB; generic
non-disclosure; project-scoped store access; malformed-record fail-closed on load; no provider/network call; no
auth/ownership overclaim. Deletion/retention, backup exposure, permissions hardening, and oversized-content DoS caps
are **deferred** (Phase 5 / production hardening) and out of P4-1b-1 scope.

**20. P4-1b-1 / P4-1b-2 / P4-2 / Phase 5 separation.** **P4-1b-1:** store construction + durable **new-project**
create/load + cold-load + web-boundary error translation — no accepted-input append. **P4-1b-2:** `append_record`
integration in `submit_answer`, durable accepted-input mutation, duplicate/retry handling, Keep/Refine runtime
integration. **P4-2:** deterministic replay, durable output records, stale-output invalidation, full re-evaluation.
**Phase 5:** accounts, authentication, ownership, verified email, account-linked authorization. All beyond P4-1b-1
remain separately gated and NOT AUTHORIZED.

**20a. Decision-trace clarification.** The P4-1b READ-ONLY DISCOVERY package identified **14** owner decisions. This
P4-1b-1 contract records only the decisions required for P4-1b-1 (D-P4-1B-01 … D-P4-1B-11 as corrected here). The
remaining discovery decisions — accepted-input append/write-path, duplicate/retry & idempotency,
supersession/contradiction mutation strategy, failure/compensation on the write path, and the Keep/Refine *durable*
behaviour — are **deferred to P4-1b-2 or later, not dropped**; they remain open and will be recorded when their gate is
authorized. Nothing here resolves or discards them.

**21. Test sequence (future implementation gate).** (1) focused P4-1b-1 RED tests; (2) focused GREEN tests;
(3) existing web-route tests (`tests/test_web_app.py`); (4) P4-1a store tests (`tests/test_p4_1a_record_store.py`);
(5) P4-0 record-contract tests (`tests/test_p4_0_record_contract.py`); (6) R6/R16 tests
(`tests/test_security_containment_r6_r16.py`); (7) protected regression tests; (8) full governed suite. No exact future
count is predicted; existing tests may be updated only to inject a temporary DB safely, without weakening assertions.

**22. Evidence-package requirements (future implementation gate).** Candidate SHA/parent/tree; changed paths; diffstat;
RED evidence (failing for the right reason, incl. a stub-still-fails demonstration); GREEN evidence (real restart/
cold-load round-trip through the route); full governed-suite result; no-new-dependency proof (`requirements.txt`
unchanged); `record_store.py`/`record_contract.py`/`idea_state.py`/`derived_readiness.py`-untouched proof; no
repository-tracked DB proof; bundle + sha256; §5A self-review.

**23. Independent-review requirement.** This candidate and the future P4-1b-1 implementation each require **formal Lean
§5 independent review in a genuinely separate session**; same-session self-review/subagents do not qualify.

**24. Owner publication & merge boundary.** Publication/PR/merge are owner-side (this environment's writes are
org-policy blocked). No push/PR/merge in this gate; the candidate stops at delivery.

**25. Mandatory stop.** On completion of this documentation candidate, stop; do not write RED tests or implementation
code; do not modify `web/app.py`; do not create/open a database; do not add a dependency; do not start P4-1b-1,
P4-1b-2, P4-2, or Phase 5.

### Reusable contract-template rendering
```
INCREMENT CONTRACT — P4-1b-1 Runtime Store Construction & Durable Project Create/Load   [CANDIDATE — NOT AUTHORIZED]
Objective:                Construct the merged P4-1a store at startup; durably create a NEW project at /start; survive
                          a real process/store restart; cold-load it back into runtime via the P4-0 contract — no
                          accepted-input append, no Keep/Refine durability.
Owner authorization:      G-P4-1B-1-DOC-01 (documentation-only candidate); implementation NOT authorized.
Risk level:               LEVEL 2 (bounded web/app.py runtime wiring + focused test; no engine/schema/dependency change).
Allowed paths:            web/app.py; tests/test_p4_1b1_runtime_project_persistence.py (new);
                          conditional web-side config helper only if inline config is unsafe/untestable;
                          existing web/security tests updated only to inject a temporary DB (no assertion weakening).
Forbidden paths:          engine/record_store.py, engine/record_contract.py, engine/idea_state.py,
                          engine/derived_readiness.py, requirements.txt, pytest.ini, database/, schemas/, templates/,
                          static/, prompts/, domains/, scripts/, benchmark/, CI/.github, P4-1b-2/P4-2/Phase 5 paths.
Expected behavior:        Durable new-project creation surviving restart; cold-load reconstruction; fresh readiness;
                          generic unavailable non-disclosure; R6/R16 preserved; no project_ids() exposure.
Non-goals:                Accepted-input append; Keep/Refine durability; duplicate/retry; relationship mutation;
                          transcript/last_result/output/readiness persistence; migration; accounts/auth; replay.
Acceptance criteria:      GREEN criteria (§17); false-RED/false-GREEN controls (§18); full-suite non-regression.
Required tests:           RED-1..RED-11 → GREEN; real restart/cold-load via Flask test_client; real tmp_path SQLite.
Tests not required:       Any provider/network/server-process test; exact future baseline count.
Dependencies:             P4-1a store (merged PR #356) + P4-0 contract (merged PR #353); stdlib sqlite3; NO new dep.
Unresolved decisions:     Whether a separate config helper is proved necessary (default: no).
Stop conditions:          Any need to modify a forbidden path or add P4-1b-2 behaviour → STOP — CONTRACT AMENDMENT REQUIRED.
Independent-review scope: Per §5; plus real restart/cold-load; no fake durability; create-before-advertise ordering;
                          generic non-disclosure; capability ≠ authorization; readiness never authoritative;
                          no accepted-input append; no P4-1b-2/P4-2/Phase 5 work.
Merge authority:          Owner, separately (not by the execution agent).
```

**Preserved (unchanged by this candidate):** decision **D17**; the **AISR seven-owner model**; **P4-1b-2, P4-2,
Phase 5–7, WS17, STG**, provider selection, and exact UX all remain **NOT AUTHORIZED**. The merged P4-1a and P4-0
artifacts are unchanged; this candidate wires nothing and creates no database.

---

## P4-1b-1 Contract Amendment — G-P4-1B-1-AMEND-01 (Threading & Pytest DB Isolation) — AMENDMENT CANDIDATE ONLY

**Status:** `AMENDMENT CANDIDATE ONLY` · `CORRECTION IMPLEMENTATION NOT AUTHORIZED` · `P4-1b-1 CORRECTION NOT STARTED`.
This is a **documentation-only** amendment to the P4-1b-1 Increment Contract above. It responds to the independent
review of implementation candidate `1eced7d280449b9c0842355a1882a9d3b731a633` (verdict **C — REVISE AND RE-REVIEW**)
and records the owner-approved contract corrections. It authorizes **no** edit to candidate `1eced7d`, `web/app.py`,
tests, runtime, dependency, database, publication, or a replacement implementation. The corrected implementation is a
**separate** future authorization (see "Correction-implementation boundary" below). Recorded on live tip
`b22f82ef1f7d08ce802ecbc52d68706d358fadb5` (Merge PR #358; always re-resolve from Git).

**Blocking findings addressed (contract-level only).**
- **B1 — Threading.** The merged P4-1a `SqliteRecordStore` owns one application-scoped `sqlite3` connection. Flask's
  built-in dev server is threaded by default, so serving requests through that shared connection across request threads
  is unsafe (`sqlite3` objects are thread-bound). The prior contract did not pin the serving mode.
- **B2 — Pytest DB isolation.** Governed tests outside the focused P4-1b-1 file that reach `/start` write project
  envelopes to the shared local-development default database instead of a pytest-managed temporary path.

**Owner decisions (recorded; govern D-P4-1B-1-AMEND-01 … D-P4-1B-1-AMEND-04 in `OWNER_DECISION_REGISTER.md`).**
- **D-P4-1B-1-AMEND-01 — Explicit single-threaded MVP serving mode.** For the bounded P4-1b-1 SQLite reference
  implementation, the Flask development/runtime entry point MUST explicitly use **`threaded=False`**, because the merged
  P4-1a `SqliteRecordStore` owns one application-scoped `sqlite3` connection that must not be used across request
  threads. The implementation MUST NOT rely on Flask's default threaded mode. **No change to `engine/record_store.py`;
  no `check_same_thread=False`; no connection pool, per-thread store, or per-request connection model.** Multi-threaded,
  multi-worker, and production-topology redesign remain deferred. **`threaded=False` is a bounded MVP decision, not a
  claim that Flask's built-in server is a production deployment architecture.**
- **D-P4-1B-1-AMEND-02 — Governed pytest database isolation.** All governed pytest execution that can reach P4-1b-1
  runtime-store creation MUST use test-managed isolated database files. This authorizes **`tests/conftest.py`** ONLY for
  a minimal fixture that: assigns `INVENTORAI_DB_PATH` to a unique pytest-managed `tmp_path`; prevents tests from writing
  to the shared local-development database; resets `SESSION_STORE`; **safely closes** an existing app-scoped store before
  replacing/resetting it; restores environment and runtime state after each test; introduces no production behaviour;
  weakens no existing assertion. The fixture MUST NOT: use a repository-tracked DB; use `:memory:` SQLite for
  durability/restart tests; expose `project_ids()`; persist transcripts or accepted-answer content; hide failures by
  mocking the store globally; or make tests order-dependent. **Focused restart tests continue using a real on-disk
  SQLite file under pytest-managed temporary storage.**
- **D-P4-1B-1-AMEND-03 — Threading regression proof.** The corrected implementation MUST include a focused regression
  proving the single-threaded serving boundary is explicitly configured and cannot silently regress to Flask's threaded
  default. The proof may use a narrowly bounded helper or run-entry test, but MUST NOT claim that `test_client` alone
  proves cross-thread safety. The evidence must also reproduce the reviewer's scenario (or an equivalent check)
  demonstrating that the corrected selected execution mode no longer serves requests through a shared SQLite connection
  across threads.
- **D-P4-1B-1-AMEND-04 — Local-development DB boundary.** The local-development default MAY remain under the system
  temporary directory ONLY for non-test, non-production development. Recorded truthfully: it **persists across local
  application runs until OS/user cleanup**; it **may contain durable project capability identifiers**; it is **not an
  account or ownership store**; **pytest must never use it**; and **P4-1b-2 must re-evaluate retention, permissions,
  deletion, and user-content implications** before adding accepted-input persistence. **Production still requires an
  explicit `INVENTORAI_DB_PATH` with fail-fast behaviour.**

**Amended implementation paths (supersede §4/§5 for the corrected P4-1b-1 implementation).**
- **Required / permitted:** `web/app.py`; `tests/test_p4_1b1_runtime_project_persistence.py`; **`tests/conftest.py`**
  (new — pytest isolated-DB fixture per D-P4-1B-1-AMEND-02 only).
- **Conditionally permitted:** narrowly necessary existing test files, ONLY when their setup must be adapted to the
  global isolated-DB fixture, **without weakening assertions**.
- **Remain prohibited:** `engine/record_store.py`, `engine/record_contract.py`, `engine/idea_state.py`,
  `engine/derived_readiness.py`, `requirements.txt`, `database/`, `schemas/`, `templates/`, `static/`, CI/deployment
  files. **Any engine-store threading redesign still requires a separate contract amendment.**

**Correction-implementation boundary (NOT authorized by this amendment).** After this documentation amendment is
independently reviewed, accepted, published, merged, and post-merge verified, a **separate** correction authorization
may permit a replacement implementation candidate that: (1) keeps candidate `1eced7d` intact as superseded evidence;
(2) starts from the then-live authoritative tip; (3) explicitly configures the Flask run entry as single-threaded;
(4) introduces the minimal `tests/conftest.py` isolated-DB fixture; (5) closes/resets stores safely in tests; (6) adds a
threading/run-mode regression; (7) re-runs RED/GREEN, protected regressions, and the full suite; (8) creates a new
commit and bundle; (9) undergoes a new independent review. **This amendment itself authorizes none of those changes.**

**Preserved observations (recorded, not expanded by this gate).** Cold-load route coverage is currently limited to the
normal session route (non-blocking for this increment); the restart proof was accepted as sufficient module-level
reconstruction under the current contract; explicit production-grade connection topology remains deferred; P4-1b-2
remains responsible for accepted-input append and related retention implications.

**Preserved (unchanged by this amendment):** decision **D17**; the **AISR seven-owner model**; the unified
`sid`==`project_id` model (D-P4-1B-06); candidate `1eced7d` is **preserved intact as superseded review evidence and is
NOT amended**; **P4-1b-2, P4-2, Phase 5–7, WS17, STG** remain **NOT AUTHORIZED**.

---

## P4-1b-1 Governance Closure Sync — G-P4-1B-1-CLOSURE-SYNC-01 (documentation-only) — GOVERNANCE CLOSURE CANDIDATE — NOT YET MERGED

**Status:** `GOVERNANCE CLOSURE CANDIDATE — NOT YET MERGED`. This documentation-only sync records the completed P4-1b-1
correction implementation, its independent review, merge, and post-merge verification, preserves the non-blocking
observations, and records a procedural deviation truthfully. It authorizes **no** code, test, runtime, dependency,
schema, database, UI, CI, release, deployment, or later-phase work. Recorded on live tip
`cbd0ce3046b24631c23e482dadd413aaa42dea05` (Merge PR #360; always re-resolve from Git).

**What was completed (evidence-first).**
- The P4-1b-1 **correction** implementation (threading + pytest DB isolation) was **separately owner-authorized** and
  built as candidate `3179cd556673e5c5b6b596a052b0744bddab011a` from authoritative base
  `ccb1f23fdd9f5cb1a318ec3cec1ca05248c04bae` (tree `f3ec086d845577a0b5befae019b4ebebdb2f7fcf`).
- The superseded first candidate `1eced7d280449b9c0842355a1882a9d3b731a633` (independent verdict C) **remains preserved
  intact and unmerged** as superseded evidence.
- Independent review of `3179cd5` returned **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**.
- **PR #360** merged the **exact reviewed candidate**; merge commit `cbd0ce3046b24631c23e482dadd413aaa42dea05`
  (parents `ccb1f23` + `3179cd5`).
- **Post-merge verification (independently reproduced):** candidate-ancestor check exit 0; changed exactly
  `web/app.py`, `tests/test_p4_1b1_runtime_project_persistence.py`, `tests/conftest.py`; diffstat **3 files / 497
  insertions / 2 deletions**; explicit **`threaded=False`** present in `web/app.py`; **pytest DB isolation via
  `INVENTORAI_DB_PATH`** present in `tests/conftest.py`; no engine path changed; no accepted-input persistence; no
  P4-1b-2 behaviour.
- **P4-1b-1 implementation:** MERGED AND POST-MERGE VERIFIED. **P4-1b-1 technical status:** COMPLETE.

**Procedural deviation (recorded truthfully, neutral language).** PR #360 was **merged before a separate explicit merge
authorization was issued in the conversation**. This was a **governance-process deviation**. It does **not** invalidate
the independently reviewed candidate or the successful technical post-merge verification, and repository evidence does
not indicate a security incident or technical defect. It **must not be normalized as precedent**: future gates must
preserve the separation among **publication authorization**, **PR-creation authorization**, **merge authorization**,
and **post-merge closure**. No wording in this record states or implies that a separate merge authorization existed
before the PR #360 merge; the owner **later** authorized this governance closure sync (G-P4-1B-1-CLOSURE-SYNC-01).

**Preserved non-blocking observations (recorded, not fixed).** (1) Committed authorization-record lag: the separate
correction-implementation authorization was owner-issued in conversation and is being recorded here at closure. (2) The
superseded candidate `1eced7d` was unavailable to the independent reviewer for byte-level verification. (3) The
author's protected-regression count (82) differed from the reviewer's equivalent set (83) due to set composition, not a
substantive discrepancy. (4) RED against `1eced7d` was not independently reproducible; base RED was used. (5) The test
helper returning zero on a SQLite error was a minor false-green risk, neutralized by external SQLite inspection. (6) The
RED-B2 path-string proof is weak alone but is backed by behavioural proof. (7) Local-development DB file permissions and
retained capability identifiers remain deferred to P4-1b-2. (8) A harmless `runpy` `RuntimeWarning` remains. (9) Legacy
ILT demo `/start` routes remain memory-only. (10) Cold-load route coverage remains limited to `show_session`. None is
silently deleted or marked resolved.

**Closure boundary.** **P4-1b-1 governance closure is PENDING** and becomes complete only after this
G-P4-1B-1-CLOSURE-SYNC-01 candidate is itself separately reviewed, published, PR-created, merged, and post-merge
verified. **P4-1b-2, P4-2, and Phase 5 remain NOT AUTHORIZED / NOT STARTED.** No durable claim about accepted answers,
outputs, or complete ideas is made. Decision **D17** and the AISR seven-owner model are preserved.

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

## P4-1a Historical Increment Contract Record — SUPERSEDED AS ACTIVE AUTHORITY

**Current interpretation:** the text below is preserved as the pre-implementation P4-1a contract candidate and
historical execution record. P4-1a has since been separately owner-authorized for implementation, implemented,
independently reviewed, merged through PR #356, post-merge verified, and **FORMALLY CLOSED**. Nothing in the
historical wording below reopens P4-1a or authorizes P4-1b, P4-2, or Phase 5.

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
