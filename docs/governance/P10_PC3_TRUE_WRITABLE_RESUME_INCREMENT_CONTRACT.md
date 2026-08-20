# P10-PC3 — True Writable Resume Increment Contract

**Document ID:** P10_PC3_TRUE_WRITABLE_RESUME_INCREMENT_CONTRACT
**Status:** CONTRACT CANDIDATE (governance-only). This document AUTHORIZES NO
implementation. It becomes the canonical implementation contract only if/when
this exact candidate is merged and post-merge verified, and implementation
starts only under a SEPARATE explicit Owner implementation authorization
(§14 review tier: LEVEL 1).
**Introduced by:** Owner directive "P10-PC3-C — TRUE WRITABLE RESUME CONTRACT"
(create + freeze + Grill only; NO IMPLEMENTATION), issued after P10-PC2
became authoritative (merge `aed5cb79f53e47c5e36e0fce6228288bfae8c014`,
PR #533).
**Subordinate to:** `LEAN_GOVERNANCE_AND_AGENT_CONTINUITY_PROTOCOL.md`
(binding), the committed anchors, `ACTIVE_EXECUTION_ROADMAP.md`,
`ACTIVE_INCREMENT_CONTRACT.md`, and
`INVENTORAI_UNIVERSAL_CORE_GUARDRAIL_SMOKE_STANDARD.md`.

---

## 1. The authoritative non-resume boundary this contract governs crossing

Reconstructed from source at base `aed5cb79…` (strict source-of-truth mode;
supersession checked against the live tree — none of these has been
superseded):

| # | Fact | Authoritative source |
|---|---|---|
| B1 | P4-2 Level-1 reconstruction is READ-ONLY and "NOT a resumed session"; it explicitly does NOT provide writable continuation, SESSION_STORE rehydration, or answer submission from reconstructed state | `engine/session_reconstruction.py` module docstring ("Hard boundaries"); roadmap §"P4-2 Level-1 … PHASE 4 FORMAL CLOSURE" ("Capability boundary — Does NOT provide") |
| B2 | The committed cold-load marker is `state.domain is None`; `submit_answer` refuses any new answer on a cold-loaded session ("continuing to answer it is complete session resume (P4-2), which is out of scope") and `_cold_load_entry` deliberately restores identity onto `domain_signal` ONLY, because "Restoring `state.domain` would silently re-enable resume-answering across restarts — a governed-boundary violation" | `web/app.py` `submit_answer` cold-guard branch; `web/app.py` `_cold_load_entry` CF5-F001 NB-R1 narrowing comment |
| B3 | The guard is test-pinned: a cold page offers no answer form/token and a forged POST fails closed with no second durable event | `tests/test_p4_1b2a_durable_answer_append.py::test_obs_b_restart_durability_new_context`; `tests/test_p10_pc1_reconstructed_review_ui.py::test_non_resume_guard_untouched` |
| B4 | The Universal Guardrail blocking guard UG-CORE-08 ("Reconstructed views are READ-ONLY … writable resume stays deactivated") composes exactly those tests; removing/weakening it un-governed fails the suite (UG-META-01) and the runner BLOCKs | `tests/universal_guardrail_manifest.py` UG-CORE-08; `tests/test_p10_ug1_universal_guardrail_framework.py::test_core_blocking_inventory_pinned` |
| B5 | Durable today (per project): the project envelope incl. reconstruction inputs (`seed_idea_text`, `confirmed_domain`, `recon_path`, `engine_contract_version`); the append-only accepted-answer ledger (`AssertionRecord`s, disposition `answered`, `rec_N` preserved, authoritative `seq` order); a SEPARATE durable answer-idempotency identity per accepted answer; account/auth/ownership tables (P5) | `engine/record_store.py` (`load_reconstruction_inputs`, `load_accepted_answer_evidence`, schema); `web/app.py` `_reconstruction_inputs`, P4-1b-2a append path |
| B6 | Memory-only today (lost on restart): `SESSION_STORE` entries — live `IdeaState` runtime object, `transcript`, `last_result`, `answer_token`, criticality UI stage, non-answer `interaction_actions`, `success_criteria`, snapshot acks | `web/app.py` SESSION_STORE usage; `engine/record_contract.py::to_state` ("Rebuild a minimal IdeaState carrying the restored append-only ledger … NOT full deterministic replay") |
| B7 | After restart the canonical single replay (`_reconstruct`) deterministically rebuilds: maturity, current stage, gaps (incl. `iterations_open`/`opened_at`), next question, domain/path (from persisted inputs), and — since P10-PC2 — the verbatim persisted ledger on the fresh state; PC1/PC2 render this READ-ONLY (session page and deliverable) under the exact authorized claim | `engine/session_reconstruction.py` `_reconstruct` / `reconstruct_readonly_state`; PC1/PC2 roadmap entries and suites |
| B8 | NOT currently safe to reconstruct into a writable session (never durable; must never be fabricated): the historical `transcript`, cached `last_result` provenance, non-answer disposition actions, criticality UI stage, success criteria, prior `answer_token` entry state | B5/B6 above; `_cold_load_entry` docstring ("transcript and cached last_result are NOT restored as authoritative") |
| B9 | POST safety model today: stateless sid-bound answer token (`nonce.sig`, sig = HMAC(`INVENTORAI_SECRET_KEY`, "p4-1b2a-answer-token"‖sid‖nonce)); token retained per entry until an accepted answer consumes it (rotated at acceptance); durable idempotency key = HMAC(secret, sid‖token) stored on the record; content fingerprint (sid, target gap, action, exact content) with confirm-by-reload C3 (same-token+same-content retry = idempotent no-op; same-token+different-content fails closed); persist-before-acknowledge staging on a deep-copied state | `web/app.py` `_issue_answer_token`/`_answer_token_for`/`_valid_answer_token`/`_answer_idempotency_key`/`_answer_fingerprint`; `submit_answer` C1/C3 comments |
| B10 | Ownership: `_project_authorized` gates every session/deliverable route; verified-owner binding is server-side; NULL-owner (legacy/anonymous) preservation rules committed; non-owner/anonymous/sid-possession denial test-pinned (UG-CORE-09) | `web/app.py` `_project_authorized`; `tests/test_p5_3_project_ownership_authorization.py` |

**Product-problem confirmation (directive §4):** repository truth confirms the
gap exactly as stated — a returning user can VIEW truthful reconstructed state
(PC1) and the truthful deliverable (PC2) but cannot CONTINUE ANSWERING
(B2/B3). No repository evidence contradicts the gap.

---

## 2. Objective (BEFORE / AFTER)

- **BEFORE:** after a process restart the user can inspect the truthful
  read-only reconstructed session view and deliverable, but every attempt to
  continue answering fails closed by design.
- **AFTER (once separately authorized and implemented under this contract):**
  the user may explicitly resume an ELIGIBLE durable project and continue the
  SAME governed deterministic journey from the deterministically reconstructed
  next step — without re-answering prior questions, without duplicating
  history, and without any weakening of ownership, anti-forgery, fail-closed,
  or deterministic-progression guarantees.

---

## 3. Canonical resume semantics (binding definitions)

1. **Project identity:** the durable `project_id` (== the URL `sid`) is the
   sole continuity identity. Resume continues a PROJECT, never a process
   session.
2. **Session vs project:** a resumed interaction receives a NEW transient
   runtime context (a fresh `SESSION_STORE` entry, fresh answer token, fresh
   presentation state) bound to the SAME durable project. The prior process
   session is gone and is never claimed to be restored.
3. **Authoritative records:** the durable envelope + append-only accepted-
   answer ledger + durable idempotency identities (B5) are the ONLY
   authoritative history.
4. **Derived runtime state:** the writable context's `IdeaState` is produced
   EXCLUSIVELY by the canonical single replay (`_reconstruct` lineage:
   seed first, then accepted answers in `seq` order, ledger restored
   verbatim). No other derivation path is permitted.
5. **Regenerable transient fields:** answer token; presentation/UI state;
   draft-context ids; language state; readiness recomputation.
6. **Fields that must NEVER be fabricated:** transcript entries;
   `last_result` for iterations that were not run in this context; non-answer
   disposition actions; criticality confirmations/UI stage; success criteria;
   any `AssertionRecord`. Absent-by-truth stays absent.
7. **Current question:** determined ONLY by the canonical replay's
   `select_next_gap`/display-question path on the reconstructed state — never
   cached, never stored, never trusted from the client.
8. **Maturity / domain:** determined ONLY by the replay (maturity) and the
   persisted `confirmed_domain` (domain). The writable context MAY set
   `state.domain` (the governed crossing) ONLY at explicit establishment
   (§5), never on GET, never on plain cold-load.
9. **Restoring prior answers:** verbatim ledger attachment (P10-PC2
   mechanism) — restored records are runtime copies of durable truth and are
   NEVER re-appended, re-scored as new inputs, re-fingerprinted, or assigned
   new ids.
10. **New answers:** exactly the existing accepted-answer pipeline
    (token → staged clone → `run_iteration` → `record_interaction` →
    durable append with idempotency key → publish; persist-before-acknowledge
    unchanged). "Resume after N accepted answers, then submit answer N+1
    exactly once" is the contract's core acceptance scenario: the new record
    appends after the last valid durable `seq`, exactly once.
11. **Conflict rule:** if any stored datum conflicts with deterministic
    replay (corrupt ledger → `ContractError`; replay-limit exceeded;
    inconsistent envelope), writable resume is REFUSED (fail closed) and only
    the existing truthful read-only surfaces remain. Replay truth is never
    "repaired" to match stored expectations, and storage is never mutated to
    match replay.

## 4. Token / idempotency contract

- REUSE the existing canonical owners (B9). No cryptographic redesign, no new
  secret, no token-format change is authorized by this contract.
- A writable resumed context MUST mint a FRESH token at establishment; the
  token remains sid-bound and single-use-for-acceptance (rotation on accept,
  unchanged).
- Tokens issued before a restart, being stateless, may still verify
  cryptographically; they MUST NOT enable a submission that bypasses
  establishment: an answered POST against a project with no established
  writable context fails closed exactly as today (B2/B3), regardless of token
  validity.
- Duplicate-submit protection across restarts rests on the DURABLE
  idempotency identity + content fingerprint (B9): a retry of an
  already-accepted answer remains an idempotent no-op; a same-token
  different-content submission remains fail-closed; these guarantees must be
  test-pinned across a restart boundary.
- Question binding stays via the existing fingerprint's target-gap component;
  project binding stays via the sid-bound signature and sid-scoped durable
  key; ownership binding stays via `_project_authorized` BEFORE any token
  logic; language/UI state must have no authorization effect (as today).
- No accepted answer may ever be persisted twice (DB-level idempotency
  uniqueness remains the floor).

## 5. SESSION_STORE rehydration contract (writable-context establishment)

Writable resume MAY populate `SESSION_STORE` — ONLY through an EXPLICIT,
ownership-checked establishment step (a deliberate user action delivered as a
POST; never a side effect of GET, never automatic on cold-load). Field
sources at establishment:

| Field | Source |
|---|---|
| `state` (full `IdeaState`) | canonical replay output (§3.4), ledger restored verbatim |
| `state.domain` | persisted `confirmed_domain` — set ONLY here (the governed crossing); plain cold-loads keep today's `domain_signal`-only narrowing |
| `answer_token` | freshly minted at establishment |
| `transcript`, `last_result`, `interaction_actions`, criticality stage | EMPTY / None — never fabricated (§3.6) |
| presentation flags (acks, draft context) | fresh defaults |

Binding rules: rehydration itself performs ZERO durable writes; reconstructed
state never becomes durable truth by entering memory; the FIRST durable write
after establishment must correspond only to a valid NEW user action; a
re-restart after establishment simply repeats the cycle (resume must be
re-establishable, idempotently, any number of times). This prevents "cold
reconstructed state accidentally becoming a fabricated historical session."

## 6. Replay-then-continue guarantee (canonical sequence)

`DURABLE PROJECT → DETERMINISTIC RECONSTRUCTION (canonical single replay) →
VALIDATE (Level-1 only; ContractError/limit/inputs checks) → ESTABLISH SAFE
WRITABLE CONTEXT (explicit, owned, non-durable) → PRESENT CURRENT QUESTION →
RECEIVE ONE VALID NEW ANSWER → APPEND NEW DURABLE RECORD (exactly once) →
RUN NORMAL DETERMINISTIC PROGRESSION`.

PROHIBITED: any parallel second progression engine; resume-only progression
logic; resume-specific domain classifier or scoring; a duplicate FSM; any
bypass of the canonical `engine/progression_loop.py`,
`engine/session_reconstruction.py`, `engine/record_store.py`, or
`web/app.py submit_answer` owners.

## 7. Ownership / auth contract

- `_project_authorized` (and the P5-3 semantics behind it) remains the sole
  gate, evaluated BEFORE establishment and BEFORE every subsequent action.
  Resume NEVER increases access rights; no authentication redesign.
- Required outcomes: authenticated owner → may establish; different
  authenticated user → generic denial (non-enumerating, as today); anonymous
  visitor on an owned project → denial; anonymous NULL-owner project → exactly
  the committed preservation rules (resumable only where authorization is
  already granted today, e.g. the creating browser's signed cookie);
  deleted/invalid/malformed project id → the existing generic redirect;
  stale browser after restart → read-only view (PC1/PC2) until explicit
  establishment; direct bookmarks keep working read-only.

## 8. Read-only vs writable modes (PC1/PC2 preserved)

The read-only reconstructed VIEW (PC1 session page, PC2 deliverable — exact
authorized claim, form suppressed, zero durable writes on GET) is PRESERVED
UNCHANGED as the default post-restart surface and as the universal fallback.
A WRITABLE RESUMED CONTEXT exists only after §5 establishment and must be
visibly distinct (EN/AR): the user must never be misled about mode. If
establishment fails for any reason, the surface falls back to the truthful
read-only view — never to a false writable state. Approved wording direction:
"Resumed project — reconstructed continuation"; PROHIBITED wording: "restored
original session" (technically false), any claim that the prior session,
transcript, or non-durable actions were recovered.

## 9. Durable history integrity

Historical accepted answers immutable; `rec_N` ids and `seq` order canonical;
no replayed record re-appended; new records append after the last valid
durable `seq`; reconstructed runtime assertions are not new durable
assertions; deterministic replay mutates no persistence; every GET remains
read-only (test-pinned today by UG-CORE-08's no-durable-write pins, which
must survive in successor form — §12).

## 10. Concurrency / multi-tab / retry (minimum safe behavior)

Current architecture (single Flask process, SQLite durable store with a
unique idempotency identity) requires NO distributed locking, and this
contract authorizes none. Required deterministic outcomes:

- Two tabs resume the same project: both may establish; the durable ledger is
  the single truth; the durable idempotency key + fingerprint arbitrate.
- Two submissions against the same current question: exactly one durable
  append; the second is an idempotent no-op (same token+content) or a
  fail-closed "not saved" outcome (different content / consumed token) — as
  the existing C3 semantics already provide.
- Browser/network retry of a POST: idempotent no-op (existing behavior,
  re-pinned across the resume boundary).
- A stale page submitting after another page advanced the project: MUST NOT
  duplicate evidence and MUST NOT silently corrupt progression — the
  fingerprint's target-gap binding plus fail-closed rejection satisfy this;
  the implementation must prove it under test (§13 RED 11).

## 11. Failure / recovery contract (fail closed; read-only fallback)

| Condition | Required outcome |
|---|---|
| Replay fails (`ContractError`) / evidence incomplete / replay limit exceeded / Level-0 metadata (legacy, version-mismatch, non-Path-N) | writable resume REFUSED; truthful read-only surfaces (or the existing generic behavior) remain; never a 500 |
| Domain cannot be resolved / deactivated or unsupported domain | REFUSED (fail closed); read-only view remains; no resume-specific admission path |
| Current question cannot be determined (e.g. completed project: maturity 2, no open gaps) | no writable question flow is offered; truthful completion/deliverable surfaces remain |
| Internally inconsistent persisted data | REFUSED; never repaired silently (§3.11) |
| Storage unavailable | fail closed exactly as the existing persist-before-acknowledge paths |
| Stale establishment context after another restart | re-establishment required; never a fabricated continuation |
| Deliverable already generated | unchanged — the deliverable remains derivable at any time; resume neither requires nor invalidates it |

## 12. Universal Guardrail integration (required future governed change)

P10-UG1 remains authoritative; smoke MUST pass pre- and post-implementation;
no guard may be weakened to make resume pass. Because UG-CORE-08's canonical
tests pin the CURRENT total prohibition (B3/B4), the implementation candidate
MUST include — as a governed framework change per the UG standard §6/§7
(HIGH-SENSITIVITY), with the pinned inventory updated in the SAME candidate —
answer **C. both**: a SUCCESSOR guard replacing UG-CORE-08's canonical tests
while preserving the full safety intent, asserting at minimum: (a) an
un-established cold view remains unanswerable and offers no form/token;
(b) establishment is explicit, ownership-checked, and performs no durable
write; (c) GET never writes durably; (d) forged/stale submissions without an
established context fail closed with no durable event — PLUS a NEW blocking
guard for resume integrity (exactly-once append after resume; no historical
re-append; no fabricated transient state). The old prohibition may be
superseded ONLY by this stronger successor pair; plain deletion is forbidden.
This CONTRACT candidate changes no guardrail file.

## 13. Required future RED evidence (implementation prerequisites)

RED must prove, at the current base behavior: (1) a cold project cannot
continue answering; and then GREEN must prove: (2) a resumed project
continues exactly at the deterministic next question; (3) prior answers are
not re-written; (4) a new answer appends exactly once; (5) stale/duplicate
submission fails safely (idempotent no-op or fail-closed, never a second
record); (6) forged cross-project submission fails; (7) cross-account resume
fails; (8) maturity/domain/gap parity with pre-restart truth holds;
(9) PC1/PC2 read-only behavior remains intact; (10) restart-after-resume can
resume again safely; (11) a multi-tab stale submit does not duplicate
evidence; (12) EN/AR public truth is correct on every new surface.

**Required adversarial/mutation probes:** remove duplicate-submit protection;
re-append reconstructed history; alter reconstructed maturity; alter domain;
bypass ownership; accept a stale question binding; inject SESSION_STORE state
inconsistent with replay; remove a fail-closed reconstruction check; make a
cold GET write persistence. Each must be caught by the gate's tests or the
Universal Guardrail suite.

## 14. Review-tier classification

**LEVEL 1 — HIGH-RISK / STRATEGIC** for the implementation
(`LEAN_GOVERNANCE_AND_AGENT_CONTINUITY_PROTOCOL.md` §4: LEVEL 1 includes
authentication/authorization-adjacent and architecture-level change; crossing
a committed governed fail-closed guarantee is a strategic boundary change,
not a DEPTH-2/3 increment). Therefore implementation requires: (i) this
merged contract; (ii) a SEPARATE explicit Owner implementation authorization;
(iii) formal Independent External Review per protocol §5 (separate-session
independence). Nothing in P10-UG1 is used to weaken this. This contract
candidate itself is a governance-only document produced under the Owner's
P10-PC3-C directive.

## 15. Contract success criteria

Implementation may be accepted only with ALL of: deterministic reconstruction
parity; safe explicit writable-context establishment; no historical rewrite;
exactly-once new-answer persistence under the current architecture;
stale/duplicate failure behavior; ownership preservation; EN/AR public truth;
PC1 preserved; PC2 preserved; P4-2 reconstruction preserved (superseded only
where §12 authorizes the governed successor guards); `UNIVERSAL GUARDRAIL
SMOKE: PASS` pre and post; full suite PASS; all §13 probes PASS; governance
truth sweep UNSUPPORTED MATERIAL CLAIMS = 0.

## 16. Architectural boundaries and exclusions

Reuse-only: canonical owners named in §6. NOT authorized: new persistence
subsystem; new progression/domain engine; vendor session service;
Redis/cloud/provider dependency; background workers; event-sourcing redesign;
schema redesign (if a genuinely necessary additive schema change emerges, it
is a separate HIGH-SENSITIVITY implementation decision requiring explicit
evidence first). OUT OF SCOPE: account-history redesign; subscription/trial/
payment; email provider; enterprise tenancy; multi-device sync beyond durable
truth; collaborative editing; offline; push; PSRR; deployment; monitoring
redesign; unrelated hardening; new domain activation; D4; D8; Decision
Workspace integration; unrelated technical debt.

---

## 17. Reviewer corrections O1–O4 (append-only; carried forward at the P10-PC3 implementation gate)

Accepted as NON-BLOCKING by the Owner at P10-PC3-C exact-SHA acceptance and
incorporated here without amending the accepted contract SHA (this section was
appended by the P10-PC3 implementation candidate):

- **O1 — Guard attribution:** in §1, `test_obs_b_restart_durability_new_context`
  belongs to **UG-CORE-07** (persistence durability + forged-POST fail-closed),
  while **UG-CORE-08** composes `test_cold_render_makes_no_durable_write` +
  `test_non_resume_guard_untouched`. Disposition executed by the
  implementation: UG-CORE-07 PRESERVED UNCHANGED (its assertions remain true —
  un-established cold pages stay formless and forged POSTs fail closed);
  UG-CORE-08 superseded IN PLACE by its establishment-boundary successor plus
  the new UG-CORE-16 resume-integrity guard.
- **O2 — Anonymous access:** the current NULL-owner authorization rule is
  sid-capability access, not a signed-cookie binding; §7's illustration is
  corrected accordingly. No narrowing of access semantics is authorized.
- **O3 — LEAN citations:** risk LEVEL definitions are in protocol **§3**;
  **§4** concerns review depth; **§5** concerns independent-review policy.
  §14's citation reads accordingly (LEVEL 1 per §3; depth per §4; formal
  independence per §5).
- **O4 — Evidence labeling:** §13 comprises **1 RED base-prohibition item**
  (cold project cannot continue answering) plus **11 future GREEN items**,
  not 12 RED items.
