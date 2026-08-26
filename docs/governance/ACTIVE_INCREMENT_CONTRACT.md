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
**Status (current — POST-W2-C-IMPLEMENTATION GOVERNANCE / STATUS SYNCHRONIZATION;
governance-only write-gate candidate).** Base:
**`b749c8873533ca6c48ebcf9be0c4023aa10cdd09`** — verified from Git at this gate as the **live
authoritative tip** of `feature/atomic-json-session-persistence` (**0 commits after it**;
**PR #581** — the W2-C/RVR-6b implementation merge; first parent `6b4629d7…` (PR #580 — the
authoritative post-W2-C-contract sync merge); second parent `1bc0690d…` — the exact
Owner-accepted implementation candidate (evidence-integrity rejected siblings `1249dbbd…` and
`cf77c33d…` preserved as rejected evidence, neither an ancestor); merge tree `14b54d7e…`
identical to the candidate tree; EMPTY candidate→merge diff; merged 2026-08-26T22:30:52Z;
post-merge identity verified).

**Current authoritative truth (verified from Git, not prose):**
**`W2-C IMPLEMENTATION: AUTHORITATIVE` — `W2-C IMPLEMENTED: YES`** (PR #581; the Owner's
implementation-start authorization was issued AFTER the PR #580 sync — recorded as fulfilled
chronology, the prior sync's `AUTHORIZED: NO` line being authority-at-its-time) ·
**`PRECEDENCE OWNER-ACCEPTED: YES`** (the exact four-level W2-B × W2-C composition, accepted
with the exact-SHA acceptance of `1bc0690d…` — ODR acceptance row) · **W1-N3 `CLOSED WITH
EVIDENCE` (bounded authoritative scope; the relevance-precision residual stays
RVR-2/RVR-7-owned)** · lapse revalidation `NOT AFFECTED` · `W/M: 2/2 OWNER-ACCEPTED AND
FROZEN` · **`RVR-6B FORMALLY CLOSED: NO`** — implementation authority is not formal closure;
the next eligible gate is the separate `RVR-6b FORMAL CLOSURE` lifecycle (its own Owner
authorization required). Carried non-blocking observations (register RVR-6b row): registry
CWD/path binding; registry-prose ↔ `_INTENT_MARKERS`. `OD-PDVG-12 EXERCISED: NO`; MG-8 OPEN
(no repair); WS11 dormant; Tier-2 and full adaptive questioning OFF; `RVR-7 / RVR-8 / FCORA:
NOT AUTHORIZED`; CAP-12/CAP-13/IoT/Drones/Renewable, deployment, production, Serious Release,
Paid Activation: NOT AUTHORIZED.

```
INCREMENT CONTRACT — Post-W2-C-Implementation Status Synchronization (governance only)
Objective:                Bring the live status surfaces and the registers to current repository
                          truth after the PR #581 implementation merge: record the
                          implementation as authoritative with the truthful
                          authorization-after-sync chronology; record the Owner-accepted
                          W2-B × W2-C precedence; close the W1-N3 row on its bounded evidence
                          (history preserved); carry the CWD-binding and prose↔marker
                          observations durably; update the RVR-6b row without closing it;
                          rotate this contract.
Owner authorization:      the Owner's post-W2-C-implementation governance synchronization gate
                          instruction (following Owner exact-SHA acceptance of 1bc0690d… and
                          the PR #581 merge)
Risk level:               LEVEL 2 — governance/documentation only (Standard change class: C0/C1)
Allowed paths:            docs/governance/CURRENT_PROJECT_STATE.md;
                          docs/governance/ACTIVE_EXECUTION_ROADMAP.md (append-only);
                          docs/governance/ACTIVE_INCREMENT_CONTRACT.md (this rotation);
                          docs/governance/OWNER_DECISION_REGISTER.md (lineage + boundary);
                          docs/governance/DEFERRED_OBLIGATIONS_REGISTER.md (row updates +
                          header)
Forbidden paths:          engine/, web/, tests/, scripts/, domains/, schemas, digest pins, the
                          merged contract/evidence-pack records, historical records,
                          preserved/rejected evidence
Expected behavior:        status surfaces state current lifecycle truth (implemented ≠ RVR-6b
                          closed); nothing else changes
Non-goals:                RVR-6b formal closure; RVR-7/RVR-8/FCORA; MG-8 adjudication/repair;
                          OD-PDVG-12; any runtime change; repair of the carried observations
Acceptance criteria:      the sync Grill S01…S38 (merge identity verified; chronology truthful;
                          precedence recorded; W1-N3 bounded closure exact; observations
                          durable; no premature RVR-6b closure; minimal changed-file set)
Required tests:           none — documentation-only (zero runtime delta verified mechanically)
Tests not required:       product tests — no product path changes
Dependencies:             PR #581 authoritative merge; the committed evidence pack; the
                          Independent Review + focused re-review record
Unresolved decisions:     RVR-6b formal-closure authorization; MG-8 adjudication; OD-PDVG-12;
                          the CWD-binding and prose↔marker future decisions; the open Owner
                          decisions tracked in the register
Stop conditions:          any merge-identity mismatch; any pressure to close RVR-6b, authorize
                          RVR-7+, repair observations, or rewrite history
Independent-review scope: factual accuracy; chronology truthfulness; bounded-closure scope
                          fidelity; observation durability; no self-certification
Merge authority:          owner, separately (candidate is NOT published, PR'd, or merged by the
                          Creator)
```

---

**Superseded (retained as history) — POST-W2-C-CONTRACT GOVERNANCE / STATUS SYNCHRONIZATION;
MERGED AND AUTHORITATIVE via PR #580, merge `6b4629d75b58690eb0a40a754e747ba79f265447`.** Its
"W2-C RUNTIME IMPLEMENTATION AUTHORIZED: NO / next eligible gate = W2-C IMPLEMENTATION-START
AUTHORIZATION" lines are authority-at-that-time — the Owner subsequently issued that separate
authorization and the implementation lifecycle completed via PR #581 (see the active block
above). Base: **`d796b0cd385d8ad2071088d58a89612715aad888`** — verified from
Git at that gate as the **live authoritative tip** of
`feature/atomic-json-session-persistence` (**0 commits after it**; **PR #579** — the W2-C/RVR-6b
contract merge; first parent `1a9eb556…` (PR #578 — the authoritative RVR-6a formal-closure
merge); second parent `455cb502…` — the exact Owner-accepted repaired contract candidate
(Lead-rejected sibling `706917cb…` preserved as rejected evidence); merge tree `816c39a5…`
identical to the candidate tree; EMPTY candidate→merge diff).

**Current authoritative truth (verified from Git, not prose):**
**`RVR-6A FORMALLY CLOSED: YES`** (PR #578 — the closure record's conditional statement
satisfied and post-merge verified) · **`W2-C / RVR-6b CONTRACT: AUTHORITATIVE`** (PR #579) ·
**`OD-W2-WS10-SCOPE: EXERCISED`** at the Owner's exact-SHA acceptance of `455cb502…` (two
per-domain registry instances over the existing 21 committed ids through the unmodified D11/D19
loader; OD-PDVG-04(a) bounded to those ids; combined-source rejected) · `W/M OWNER-ACCEPTED AND
FROZEN: W = 2, M = 2` · **`W2-C RUNTIME IMPLEMENTATION AUTHORIZED: NO`** — the next eligible
gate is a SEPARATE explicit Owner implementation-start instruction (the W2-A/W2-B precedent);
`W2-C IMPLEMENTED: NO`; `RVR-6B FORMALLY CLOSED: NO`; `OD-PDVG-12 EXERCISED: NO`; MG-8 Owner
adjudication OPEN (no semantic repair); WS11 dormant; Tier-2 and full adaptive questioning OFF;
`RVR-7 / RVR-8: NOT AUTHORIZED`; `FCORA: RECORDED, NOT EXECUTED`;
CAP-12/CAP-13/IoT/Drones/Renewable, deployment, production, Serious Release, Paid Activation:
NOT AUTHORIZED.

```
INCREMENT CONTRACT — Post-W2-C-Contract Status Synchronization (governance only)
Objective:                Bring the live status surfaces and the registers to current repository
                          truth after PR #578 (RVR-6a formal closure) and PR #579 (W2-C/RVR-6b
                          contract): record the closure as authoritative and close the register's
                          RVR-6a row per its own conditional wording; record the contract as
                          authoritative; record OD-W2-WS10-SCOPE as EXERCISED with the exact
                          selected option and the durable Wave-2 §P.4 timing interpretation;
                          record the W1-N3 contract disposition; normalize the "21-id registry"
                          wording; rotate this contract.
Owner authorization:      the Owner's post-W2-C-contract governance synchronization gate
                          instruction (following Owner exact-SHA acceptance of 455cb502… and the
                          PR #579 merge)
Risk level:               LEVEL 2 — governance/documentation only (Standard change class: C0/C1)
Allowed paths:            docs/governance/CURRENT_PROJECT_STATE.md;
                          docs/governance/ACTIVE_EXECUTION_ROADMAP.md (append-only);
                          docs/governance/ACTIVE_INCREMENT_CONTRACT.md (this rotation);
                          docs/governance/OWNER_DECISION_REGISTER.md (decision row + lineage +
                          boundary);
                          docs/governance/DEFERRED_OBLIGATIONS_REGISTER.md (row updates + header)
Forbidden paths:          engine/, web/, tests/, scripts/, domains/, schemas, digest pins, the
                          merged contract/closure/evidence records, historical records,
                          preserved/rejected evidence; no WS10 registry authoring; no loader
                          change
Expected behavior:        status surfaces state current lifecycle truth (closure authoritative;
                          contract authoritative; decision exercised; implementation NOT
                          authorized); nothing else changes
Non-goals:                W2-C implementation or its authorization; OD-PDVG-12 decision; MG-8
                          adjudication/repair; RVR-7/RVR-8/FCORA; any runtime change
Acceptance criteria:      the sync Grill S01…S93 (merge identities verified; lifecycle states not
                          collapsed; decision recorded exactly; obligations durable, no
                          duplicates; minimal changed-file set)
Required tests:           none — documentation-only (zero runtime delta verified mechanically)
Tests not required:       product tests — no product path changes
Dependencies:             PR #578 and PR #579 authoritative merges; the authoritative W2-C
                          contract §D/§E/§O; the OD-W2-DW-LIFT exercise precedent
Unresolved decisions:     the separate Owner W2-C implementation-start authorization; OD-PDVG-12;
                          MG-8 adjudication; the open Owner decisions tracked in the register
Stop conditions:          any merge-identity mismatch; any pressure to authorize/start W2-C
                          implementation, author WS10 registries, or rewrite history
Independent-review scope: factual accuracy; lifecycle-state vocabulary; decision-recording
                          exactness (option + timing); obligation durability; no
                          self-certification
Merge authority:          owner, separately (candidate is NOT published, PR'd, or merged by the
                          Creator)
```

---

**Superseded (retained as history) — RVR-6a FORMAL CLOSURE governance-only closure-gate
candidate; MERGED AND AUTHORITATIVE via PR #578, merge
`1a9eb55656b52f635804647fe77412a7987a591e` — its conditional closure statement is thereby
satisfied and post-merge verified: RVR-6a is FORMALLY CLOSED (see the active block above; the
W2-C/RVR-6b contract, PR #579, followed it).** Base:
**`eb23cbf2b1b3b4d81908942ea9231756c90d8d94`** — verified from Git at that gate as the **live
authoritative tip** of `feature/atomic-json-session-persistence` (**0 commits after it**;
**PR #577** — the post-W2-B-implementation governance-sync merge; first parent `ac9c01ea…`
(PR #576 — the authoritative W2-B/RVR-6a implementation merge); second parent `3aa985ed…` — the
exact Owner-accepted repaired sync candidate; merge tree `003035c8…` identical to the candidate
tree; EMPTY candidate→merge diff).

**Current authoritative truth (verified from Git, not prose):**
`W2-B CONTRACT: AUTHORITATIVE` (PR #573) · `W2-B CONTRACT AMENDMENT 1: AUTHORITATIVE` (PR #575)
· `W2-B IMPLEMENTATION: AUTHORITATIVE` (PR #576) · `POST-W2-B GOVERNANCE SYNC: AUTHORITATIVE`
(PR #577) · **`W/M OWNER-ACCEPTED AND FROZEN: W = 2, M = 2`**. The Owner authorized **STARTING
the RVR-6a formal-closure lifecycle only** (closure NOT pre-decided). This gate reconstructed
the closure contract from repository sources, swept the complete Deferred Obligations Register
(**closure blocker count 0**; MG-8 correctly NON-BLOCKING with its adjudication OPEN and its
gate unmoved), and created the closure instrument
`docs/governance/RVR_6A_FORMAL_CLOSURE_RECORD.md` with the non-circular conditional statement:
**`RVR-6A CLOSED: NO` until this exact closure candidate is Owner-accepted at exact SHA,
merged, and post-merge identity-verified.** `OWNER EXACT CLOSURE-SHA ACCEPTED: NO`.
`W2-C / RVR-6b / RVR-7 / RVR-8: NOT AUTHORIZED`; `FCORA: RECORDED, NOT EXECUTED`;
CAP-12/CAP-13/IoT/Drones/Renewable, deployment, production, Serious Release, Paid Activation:
NOT AUTHORIZED.

```
INCREMENT CONTRACT — RVR-6a Formal Closure (governance only)
Objective:                Execute the Owner-authorized RVR-6a formal-closure lifecycle: verify
                          the authority chain live; reconstruct the closure contract from
                          repository precedent; adjudicate the closure-requirement matrix on
                          [REPO]+[EXEC] evidence; sweep the complete Deferred Obligations
                          Register; create the conditional, non-circular formal-closure record
                          and the minimal status-surface synchronization.
Owner authorization:      the Owner's RVR-6a formal-closure lifecycle START authorization
                          (start only — closure itself requires the Owner's later exact-SHA
                          acceptance + merge + post-merge verification)
Risk level:               LEVEL 2 — governance/documentation only (Standard change class: C0/C1)
Allowed paths:            docs/governance/RVR_6A_FORMAL_CLOSURE_RECORD.md (new);
                          docs/governance/CURRENT_PROJECT_STATE.md;
                          docs/governance/ACTIVE_EXECUTION_ROADMAP.md (append-only);
                          docs/governance/ACTIVE_INCREMENT_CONTRACT.md (this rotation);
                          docs/governance/DEFERRED_OBLIGATIONS_REGISTER.md (RVR-6a row + header)
Forbidden paths:          engine/, web/, tests/, scripts/, domains/, schemas, digest pins,
                          OWNER_DECISION_REGISTER.md (closure-gate convention — no new Owner
                          decision), the merged contract/amendment/evidence-pack records,
                          historical records, preserved/rejected evidence
Expected behavior:        closure evidence adjudicated truthfully; RVR-6a reported CLOSED only
                          through the conditional merge-gated statement; nothing else changes
Non-goals:                W2-C/RVR-6b/RVR-7/RVR-8 authorization; FCORA execution; MG-8
                          adjudication or repair; any runtime change; release-value closure
Acceptance criteria:      the Closure Grill R6C-01…R6C-105 (identity, evidence-backing,
                          non-circularity, zero blockers, boundary preservation, bundle +
                          isolated fetch-back)
Required tests:           none — documentation-only (zero runtime delta; the [EXEC] probes and
                          full-suite re-run are evidence, not new tests)
Tests not required:       product tests — no product path changes
Dependencies:             PR #573/#575/#576/#577 authoritative merges; the committed evidence
                          pack; the Deferred Obligations Register RVR-6a row
Unresolved decisions:     Owner exact-SHA acceptance of the closure candidate; MG-8 Owner
                          adjudication; the open Owner decisions tracked in the register
Stop conditions:          any merge-identity mismatch; insufficient closure evidence (do NOT
                          manufacture a closure candidate); any pressure to activate W2-C or
                          later gates, adjudicate MG-8, or rewrite history
Independent-review scope: closure-evidence sufficiency; non-circular conditional wording;
                          DOR-sweep completeness; MG-8/observation disposition fidelity;
                          boundary preservation; no self-certification
Merge authority:          owner, separately (candidate is NOT published, PR'd, or merged by the
                          Creator)
```

---

**Superseded (retained as history) — POST-W2-B-IMPLEMENTATION GOVERNANCE SYNCHRONIZATION;
MERGED AND AUTHORITATIVE via PR #577, merge `eb23cbf2b1b3b4d81908942ea9231756c90d8d94`.** Its
"next eligible gate is the separate `RVR-6a FORMAL CLOSURE` lifecycle" line completed — the
Owner authorized the closure-lifecycle START and the closure gate executed (see the active
block above); its base pin `ac9c01ea…` is authority-at-that-time (superseded as the live tip by
PR #577). Base: **`ac9c01ea1caaca18306a99039cea3a4224216e8a`** — verified from Git
at this gate as the **live authoritative tip** of `feature/atomic-json-session-persistence`
(**0 commits after it**; **PR #576** — the W2-B/RVR-6a implementation merge under Contract
Amendment 1; first parent `346f8e8a3b1532a6c52750fe20bc76668db06956` (PR #575 — the authoritative
Contract Amendment 1 merge, accepted candidate `6bb8f9e34c…`); second parent
`6cf0958205681d1f476ecb8a9258bbebfb365059` — the exact Owner-accepted implementation candidate;
merge tree `f2b0004b…` identical to the candidate tree; EMPTY candidate→merge diff; the committed
implementation evidence pack is inside this exact tree).

**Current authoritative truth (verified from Git, not prose):**
`W2-B CONTRACT: AUTHORITATIVE` (PR #573) · **`W2-B CONTRACT AMENDMENT 1: AUTHORITATIVE`**
(PR #575 — Option C; trigger replacement; FDC-001 sole comparability/readiness owner; lifecycle
reset) · **`W2-B IMPLEMENTATION: AUTHORITATIVE`** (PR #576) · **`W/M OWNER-ACCEPTED AND FROZEN:
W = 2, M = 2`** (at the exact-SHA acceptance of `6cf09582…`, per the Wave-2 §P mechanism as
amended — no current surface may describe these as proposals; historical proposal wording is
authority-at-its-time). **`RVR-6A CLOSED: NO`** — implementation authority is not formal closure;
the next eligible gate is the separate `RVR-6a FORMAL CLOSURE` lifecycle. `W2-C / RVR-6b / RVR-7 /
RVR-8: NOT AUTHORIZED`; `FCORA: RECORDED, NOT EXECUTED`; CAP-12/CAP-13/IoT/Drones/Renewable,
deployment, production, Serious Release, Paid Activation: NOT AUTHORIZED. The entry-below's
"next eligible gate = W2-B IMPLEMENTATION-START AUTHORIZATION" line is authority-at-that-time —
that gate (and the full amended-contract implementation lifecycle) completed.

```
INCREMENT CONTRACT — Post-W2-B-Implementation Status Synchronization (governance only)
Objective:                Bring the live status surfaces and the Deferred Obligations Register to
                          current repository truth after the PR #575 (Contract Amendment 1) and
                          PR #576 (implementation) merges: record Amendment 1 and the
                          implementation as authoritative; record the W/M Owner acceptance/freeze
                          (W=2, M=2); record the previously unsynchronized implementation-start
                          premises and the rejected first-implementation lineage; carry the
                          accepted non-blocking observations to their existing owners; update the
                          RVR-6a and MG-8 register rows; rotate this contract.
Owner authorization:      the Owner's post-W2-B-implementation governance synchronization gate
                          instruction (following Owner exact-SHA acceptance of 6cf09582… and the
                          PR #576 merge)
Risk level:               LEVEL 2 — governance/documentation only (Standard change class: C0/C1)
Allowed paths:            docs/governance/CURRENT_PROJECT_STATE.md;
                          docs/governance/ACTIVE_EXECUTION_ROADMAP.md (append-only);
                          docs/governance/ACTIVE_INCREMENT_CONTRACT.md (this rotation);
                          docs/governance/OWNER_DECISION_REGISTER.md (append/boundary);
                          docs/governance/DEFERRED_OBLIGATIONS_REGISTER.md (row wording)
Forbidden paths:          engine/, web/, tests/, scripts/, domains/, schemas, the merged
                          contract/amendment/evidence-pack records, historical records,
                          preserved/rejected evidence
Expected behavior:        status surfaces state current lifecycle truth (implementation
                          authoritative; W/M frozen; RVR-6a NOT closed); nothing else changes
Non-goals:                RVR-6a formal closure; W2-C/RVR-6b/RVR-7/RVR-8 authorization; FCORA
                          execution; any runtime change; any new implementation authorization
Acceptance criteria:      the sync Grill GS-01…GS-73 (merge identity verified; lifecycle states
                          not collapsed; W/M freeze recorded with correct epistemics; observations
                          carried without duplicate obligations; minimal changed-file set)
Required tests:           none — documentation-only (zero runtime delta verified mechanically)
Tests not required:       product tests — no product path changes
Dependencies:             PR #575 and PR #576 authoritative merges; Amendment 1 §14 lifecycle;
                          the committed implementation evidence pack
Unresolved decisions:     RVR-6a formal closure (next eligible gate); MG-8 Owner adjudication;
                          the open Owner decisions tracked in the register
Stop conditions:          any merge-identity mismatch; any pressure to close RVR-6a, authorize
                          W2-C, or rewrite history
Independent-review scope: factual accuracy; lifecycle-state vocabulary; W/M epistemic treatment;
                          observation ownership; no self-certification
Merge authority:          owner, separately (candidate is NOT published, PR'd, or merged by the
                          Creator)
```

---

**Superseded (retained as history) — POST-W2-B-CONTRACT GOVERNANCE SYNCHRONIZATION;
MERGED AND AUTHORITATIVE via PR #574, merge `ad70723e8fdb34493ac9e53d7a9a3ceb80850708`.** Its
"next eligible gate = W2-B IMPLEMENTATION-START AUTHORIZATION" and
`W2-B IMPLEMENTATION START AUTHORIZED: NO` / `W/M NOT frozen` lines are
authority-at-that-time — the implementation-start premises, Contract Amendment 1 (PR #575), the
implementation (PR #576), and the W/M freeze completed since (see the active block above).
Base: **`48017ec0259e5fc7bcb105e0b018f6d447057bda`** — verified from Git at this
gate as the **live authoritative tip** of `feature/atomic-json-session-persistence`
(**0 commits after it**; **PR #573** — the W2-B/RVR-6a implementation-contract merge; first
parent `21ce0ff843682068c0bc29a73d4506de51e581fa` (PR #572, post-Cross-Layer sync), second
parent `5e91fd9cbc27b784c8b398ac48366b84dd73cceb` — the exact Owner-accepted REPAIRED contract
candidate (first candidate `0448e36…` externally REJECTED for D-1/D-2 and preserved as rejected
evidence); merge tree `c5c2590c…` identical to the candidate tree; empty candidate→merge diff;
merged 2026-08-25T21:15:58Z).

**Current authoritative truth (verified from Git, not prose):**
**`W2-B / RVR-6a IMPLEMENTATION CONTRACT: AUTHORITATIVE`** — the contract-acceptance
authorization boundary is COMPLETED, while **`W2-B IMPLEMENTATION START AUTHORIZED: NO`**
(a separate explicit Owner instruction is required, per the contract §N and the W2-A precedent)
and `W2-B IMPLEMENTATION AUTHORITATIVE: NO`; `RVR-6A CLOSED: NO`. **W/M numeric values are NOT
frozen** — operative timing source **Wave-2 contract §P** (corrected from the propagated §H
miscitation): values are proposed inside the future implementation candidate/evidence pack and
fixed at Owner exact-SHA acceptance of that candidate. The entry-below's "next eligible gate =
W2-B AUTHORIZATION" line is authority-at-that-time — that gate completed.

```
INCREMENT CONTRACT — Post-W2-B-Contract Status Synchronization (governance only)
Objective:                Bring the live status surfaces and the Deferred Obligations Register to
                          current repository truth after the PR #573 contract merge: record the
                          contract as authoritative with the lifecycle-state separation intact;
                          correct the propagated W/M citation (§H → §P) and disambiguate
                          "at W2-B acceptance"; carry the review lineage (rejected 0448e36) and
                          observations A–D; rotate this contract.
Owner authorization:      the Owner's post-W2-B-contract governance synchronization gate
                          instruction (following Owner exact-SHA acceptance of 5e91fd9c… and the
                          PR #573 merge)
Risk level:               LEVEL 2 — governance/documentation only (Standard change class: C0/C1)
Allowed paths:            docs/governance/CURRENT_PROJECT_STATE.md;
                          docs/governance/ACTIVE_EXECUTION_ROADMAP.md (append-only);
                          docs/governance/ACTIVE_INCREMENT_CONTRACT.md (this rotation);
                          docs/governance/OWNER_DECISION_REGISTER.md (append/boundary);
                          docs/governance/DEFERRED_OBLIGATIONS_REGISTER.md (row wording)
Forbidden paths:          engine/, web/, tests/, scripts/, domains/, schemas, the merged W2-B
                          contract record, historical records, preserved/rejected evidence
Expected behavior:        status surfaces state current lifecycle truth; no numeric W/M value
                          appears anywhere; nothing else changes
Non-goals:                W2-B implementation or implementation-start authorization; numeric W/M
                          values; W2-C/RVR-6b/RVR-7/RVR-8; FCORA execution; residual repair;
                          any runtime change
Acceptance criteria:      the sync Grill PCS-01…PCS-52 (merge identity verified; lifecycle states
                          not collapsed; citation corrected on live surfaces only; historical
                          entries preserved; minimal changed-file set)
Required tests:           none — documentation-only (zero runtime delta verified mechanically)
Tests not required:       product tests — no product path changes
Dependencies:             PR #573 authoritative merge; the W2-B contract §C/§N; Wave-2 §P
Unresolved decisions:     the W2-B implementation-start authorization (separate Owner
                          instruction); the open Owner decisions tracked in the register
Stop conditions:          any merge-identity mismatch; any pressure to authorize implementation
                          start, freeze W/M numbers, or rewrite history
Independent-review scope: factual accuracy; lifecycle-state vocabulary; citation-correction
                          fidelity; no self-certification
Merge authority:          owner, separately (candidate is NOT published, PR'd, or merged by the
                          Creator)
```

**Disposition: `POST-W2-B-CONTRACT SYNC — GOVERNANCE CANDIDATE; NOT AUTHORITATIVE UNTIL MERGED
AND POST-MERGE VERIFIED`.** After it merges, the next eligible gate is the
**`W2-B IMPLEMENTATION-START AUTHORIZATION`** — a separate explicit Owner instruction.
**`W2-B IMPLEMENTATION START AUTHORIZED: NO`; `W2-C AUTHORIZED: NO`; `RVR-7 AUTHORIZED: NO`;
`RVR-8 AUTHORIZED: NO`.**

---

**Superseded (retained as history) — POST-CROSS-LAYER-STANDARD GOVERNANCE SYNCHRONIZATION;
MERGED AND AUTHORITATIVE via PR #572, merge `21ce0ff843682068c0bc29a73d4506de51e581fa`.** Its
"next eligible gate = W2-B AUTHORIZATION" line is authority-at-that-time — that gate completed
via PR #573 (see the active block above; its "(Wave-2 contract §H)" W/M citation is corrected
there). Base: **`216cdc8e61eea141940de072105aa03a4cd801bb`** — verified from Git
at this gate as the **live authoritative tip** of `feature/atomic-json-session-persistence`
(**0 commits after it**; **PR #571** — the Cross-Layer Execution Assurance Standard merge; first
parent `e2b50120e5d2e4a1c156bff7cb5184c4efc4eb5b` (PR #570, post-W2-A-implementation sync +
FCORA recording), second parent `015a8534fbecef7e790f87cb42c087f28807d86e` — the exact
Owner-accepted Standard candidate; merge tree `611d3da4…` identical to the candidate tree; empty
candidate→merge diff).

**Current authoritative truth (verified from Git, not prose):**
**`CROSS-LAYER EXECUTION ASSURANCE STANDARD: AUTHORITATIVE`**
(`docs/governance/CROSS_LAYER_EXECUTION_ASSURANCE_STANDARD.md`, PR #571, accepted with
non-blocking review observations O-1…O-5 carried as binding interpretation in the ODR acceptance
row). Its Continuous Traceability Rule and C0–C4 proportional assurance mechanisms are MANDATORY
current process for every future applicable candidate (prospective only; per O-1 the C-classes
are a separate axis from the Lean LEVEL/DEPTH and review-tier classifications). The register's
Cross-Layer row is CLOSED on the PR #571 evidence (this candidate). FCORA remains RECORDED, NOT
EXECUTED. The entry-below's "next eligible gate = CROSS-LAYER EXECUTION ASSURANCE STANDARD" line
is authority-at-that-time — that gate completed.

```
INCREMENT CONTRACT — Post-Cross-Layer-Standard Status Synchronization (governance only)
Objective:                Bring the live status surfaces and the Deferred Obligations Register to
                          current repository truth after the PR #571 Standard merge: record the
                          Standard as authoritative and now-mandatory (prospective); close its
                          register row on the merge evidence; carry review observations O-1…O-5
                          as binding interpretation; rotate this contract.
Owner authorization:      the Owner's post-Cross-Layer-Standard governance synchronization gate
                          instruction (following Owner exact-SHA acceptance of 015a8534… and the
                          PR #571 merge)
Risk level:               LEVEL 2 — governance/documentation only (Standard change class: C0/C1)
Allowed paths:            docs/governance/CURRENT_PROJECT_STATE.md;
                          docs/governance/ACTIVE_EXECUTION_ROADMAP.md (append-only);
                          docs/governance/ACTIVE_INCREMENT_CONTRACT.md (this rotation);
                          docs/governance/OWNER_DECISION_REGISTER.md (append/boundary);
                          docs/governance/DEFERRED_OBLIGATIONS_REGISTER.md (row closure)
Forbidden paths:          engine/, web/, tests/, domains/, schemas, the merged Standard document,
                          historical records, preserved evidence
Expected behavior:        status surfaces state current truth; the Standard row closes on prior
                          external merge evidence only; nothing else changes
Non-goals:                W2-B authorization or W/M values; W2-C/RVR-6/RVR-7/RVR-8; FCORA
                          execution; residual-observation repair; any runtime change
Acceptance criteria:      the sync Grill SG-1…SG-30 (merge identity verified; minimal changed-file
                          set; no self-certification; observations carried without bloat)
Required tests:           none — documentation-only (zero runtime delta verified mechanically)
Tests not required:       product tests — no product path changes
Dependencies:             PR #571 authoritative merge; the register row's frozen closure criterion
Unresolved decisions:     the W2-B authorization (separate Owner decision, W/M at acceptance);
                          the open Owner decisions tracked in the register
Stop conditions:          any merge-identity mismatch; any pressure to authorize W2-B, execute
                          FCORA, or rewrite history
Independent-review scope: factual accuracy; closure-criterion discipline; observation carry
                          fidelity; no stale "future Standard" wording on live surfaces
Merge authority:          owner, separately (candidate is NOT published, PR'd, or merged by the
                          Creator)
```

**Disposition: `POST-CROSS-LAYER-STANDARD SYNC — GOVERNANCE CANDIDATE; NOT AUTHORITATIVE UNTIL
MERGED AND POST-MERGE VERIFIED`.** After it merges, the next eligible gate is the
**`W2-B AUTHORIZATION`** — a separate Owner decision (W/M values fixed at its acceptance).
**`W2-B AUTHORIZED: NO`; `W2-C AUTHORIZED: NO`; `RVR-7 AUTHORIZED: NO`; `RVR-8 AUTHORIZED: NO`.**

---

**Superseded (retained as history) — POST-W2-A-IMPLEMENTATION GOVERNANCE SYNCHRONIZATION;
MERGED AND AUTHORITATIVE via PR #570, merge `e2b50120e5d2e4a1c156bff7cb5184c4efc4eb5b` (the
accepted candidate was the FCORA-reconciled fresh sibling `007f08ea…`; prior sibling `e36a4d5…`
preserved as superseded-before-review evidence).** Its "next eligible gate = CROSS-LAYER
EXECUTION ASSURANCE STANDARD" line is authority-at-that-time — that gate completed via PR #571
(see the active block above). Base: **`e17ca1477e55b49298b92ac5ec8db711e208496e`** — verified from Git
at this gate as the **live authoritative tip** of `feature/atomic-json-session-persistence`
(**0 commits after it**; **PR #569** — the W2-A/RVR-4 implementation merge; first parent
`894861c9ef78c9affe927f22dfa497de68050e96` (PR #568, post-W2-A-contract sync), second parent
`d8c5aef988a00a8b342b26816afd6186e4262c42` — the exact Owner-accepted implementation candidate
(final fresh same-base sibling after Grill-failed `b3ada80…` (IG-17) and externally reviewed
N-2-rejected `614a0c7…`, both preserved as REMOTE evidence branches
`evidence/w2a-impl-grillfail-b3ada80` / `evidence/w2a-impl-reviewed-614a0c7`); merge tree
`4c1739ae9f98c422812e4a8f3561d28105974522` identical to the candidate tree; empty
candidate→merge diff; merged 2026-08-25T13:56:35Z).

**Current authoritative truth (verified from Git and by execution, not prose):**
**W2-A / RVR-4 IMPLEMENTATION IS AUTHORITATIVE** — bounded decision capture live in the existing
journey under the frozen contract, with the full RED inventory + IG-17 + N-2 tests GREEN in the
merged tree (`[EXEC] 62 passed at this tip`; candidate full suite `4595/3/1/0`). The register's
"W2-A enactment set" and "RVR-4" rows are CLOSED on that prior external evidence (this
candidate). The Owner has directed a **Cross-Layer Execution Assurance Standard** be documented
BEFORE W2-B proceeds (recorded in ODR §D; NOT created here). The entry-below's "next eligible
gate = W2-A IMPLEMENTATION AUTHORIZATION" line is authority-at-that-time — that gate completed.

```
INCREMENT CONTRACT — Post-W2-A-Implementation Status Synchronization (governance only)
Objective:                Bring the live status surfaces and the Deferred Obligations Register to
                          current repository truth after the PR #569 implementation merge: record
                          the implementation as authoritative; close the enactment set and RVR-4
                          on their exact prior-evidence criteria; record the Owner's Cross-Layer
                          Execution Assurance Standard direction and the two implementation
                          residuals; rotate this contract.
Owner authorization:      the Owner's post-W2-A-implementation read-only-reconstruction + bounded
                          status/Deferred-Obligations synchronization gate instruction (following
                          Owner exact-SHA acceptance of d8c5aef… and the PR #569 merge)
Risk level:               LEVEL 2 — governance/documentation only
Allowed paths:            docs/governance/CURRENT_PROJECT_STATE.md;
                          docs/governance/ACTIVE_EXECUTION_ROADMAP.md (append-only);
                          docs/governance/ACTIVE_INCREMENT_CONTRACT.md (this rotation);
                          docs/governance/OWNER_DECISION_REGISTER.md (append/boundary/direction);
                          docs/governance/DEFERRED_OBLIGATIONS_REGISTER.md (row transitions)
Forbidden paths:          engine/, web/, tests/, schemas, export code, the W2-A contract record,
                          historical closure records, preserved/remote evidence branches
Expected behavior:        status surfaces state current truth; closures rest ONLY on prior
                          external evidence; the standard is directed but NOT created; nothing
                          else changes
Non-goals:                W2-B/W2-C/RVR-6/RVR-7/RVR-8 implementation or authorization; the
                          Cross-Layer Execution Assurance Standard's content; any runtime change;
                          release-value closure; deployment/production/paid activation
Acceptance criteria:      the governance Grill SG-1…SG-30 (merge identity verified; every changed
                          path truth-owned; exact-criterion closures only; no self-certification;
                          READY/ELIGIBLE/AUTHORIZED preserved)
Required tests:           none — documentation-only (zero runtime delta verified mechanically;
                          the W2-A inventory was re-executed read-only at the tip as closure
                          evidence: 62 passed)
Tests not required:       product tests — no product path changes
Dependencies:             PR #569 authoritative merge; W2-A contract §21; the register's frozen
                          row criteria; the remote evidence branches
Unresolved decisions:     W2-B authorization (incl. W/M values); the Cross-Layer Execution
                          Assurance Standard gate; the open Owner decisions tracked in the
                          Deferred Obligations Register (R4-C, OD-PDVG-10/12/13, T2-D, MG-8 …)
Stop conditions:          any merge-identity mismatch; any pressure to authorize W2-B, create the
                          standard's content here, close release-value gates, or rewrite history
Independent-review scope: factual accuracy; exact-criterion closure discipline; no obligation
                          silently dropped or falsely kept alive; direction recorded without
                          invention
Merge authority:          owner, separately (candidate is NOT published, PR'd, or merged by the
                          Creator)
```

**Disposition: `POST-W2-A-IMPLEMENTATION SYNC — GOVERNANCE CANDIDATE; NOT AUTHORITATIVE UNTIL
MERGED AND POST-MERGE VERIFIED`.** After it merges, the next eligible gate is the
**`CROSS-LAYER EXECUTION ASSURANCE STANDARD` governance gate** (its own full lifecycle), and only
after that the **`W2-B AUTHORIZATION`** — a separate Owner decision. ELIGIBLE is not AUTHORIZED:
**`W2-B AUTHORIZED: NO`; `W2-C AUTHORIZED: NO`; `RVR-7 AUTHORIZED: NO`; `RVR-8 AUTHORIZED: NO`.**

---

**Superseded (retained as history) — POST-W2-A-CONTRACT GOVERNANCE SYNCHRONIZATION; MERGED AND
AUTHORITATIVE via PR #568, merge `894861c9ef78c9affe927f22dfa497de68050e96`.** Its in-block "next
eligible gate = `W2-A IMPLEMENTATION AUTHORIZATION GATE`" line and its `W2-A IMPLEMENTATION
AUTHORIZED: NO / STARTED: NO` lines are authority-at-that-time — the authorization was granted
and the implementation completed via PR #569 (see the active block above). Base:
**`82758cb2d06a7b91d30acfaa83a3d836df103186`** — verified from Git at this
gate as the **live authoritative tip** of `feature/atomic-json-session-persistence` (**0 commits
after it**; **PR #567** — the W2-A/RVR-4 contract-freeze merge; first parent
`557548db2bb37b21b6b57f893afc2ae1af64744f` (PR #566, post-W2-ID sync + Deferred Obligations
Register), second parent `b778cfe7fd31c82c583d7d97e5f73394e6bfda65` — the exact Owner-accepted
contract candidate (final sibling after Independent External Review `NARROW REPAIR REQUIRED` +
Creator re-Grill; `f4d0552…`/`f0f6663…` preserved as immutable sibling evidence); merge tree
`7b56a5e19f2a3b1f3bdba00203aa119772b5b1ca` identical to the candidate tree; empty candidate→merge
diff; merged 2026-08-25T11:23:16Z).

**Current authoritative truth (verified from Git, not prose):** the **W2-A / RVR-4 implementation
contract is CONTRACT-FREEZE AUTHORITATIVE** (`docs/governance/W2_A_RVR4_IMPLEMENTATION_CONTRACT_CANDIDATE.md`
via PR #567): V2 decision-action vocabulary; `decision_context_root`; bounded legacy load rule;
fail-closed carrier mint; `OWNER_STATED` decision-action provenance; FDC-001 sole ownership;
deterministic projection formulas; ID-11; OW-6 on the corrected requirement-landscape baseline;
frozen implementation allowlist + RED inventory. **OD-W2-DW-LIFT is EXERCISED (bounded)** per
contract §5 — the broader DW Path-T hold stands. **W2-A IMPLEMENTATION remains NOT AUTHORIZED and
NOT STARTED** (contract §23 requires a separate explicit Owner authorization). The entry-below's
"next eligible gate = W2-A AUTHORIZATION / CONTRACT-FREEZE GATE" line is authority-at-that-time —
that gate has completed.

```
INCREMENT CONTRACT — Post-W2-A-Contract Status Synchronization (governance only)
Objective:                Bring the live status surfaces and the Deferred Obligations Register to
                          current repository truth after the PR #567 W2-A contract-freeze merge:
                          record the freeze as authoritative; close OD-W2-DW-LIFT and the two
                          post-W2-ID sync/lineage rows on their own evidence; keep the W2-A
                          enactment set and RVR-4 implementation OPEN per contract §21.
Owner authorization:      the Owner's post-W2-A-contract read-only-reconstruction + bounded
                          status/Deferred-Obligations synchronization gate instruction (following
                          Owner exact-SHA acceptance of b778cfe7… and the PR #567 merge)
Risk level:               LEVEL 2 — governance/documentation only
Allowed paths:            docs/governance/CURRENT_PROJECT_STATE.md;
                          docs/governance/ACTIVE_EXECUTION_ROADMAP.md (append-only);
                          docs/governance/ACTIVE_INCREMENT_CONTRACT.md (this rotation);
                          docs/governance/OWNER_DECISION_REGISTER.md (append/boundary update);
                          docs/governance/DEFERRED_OBLIGATIONS_REGISTER.md (row transitions)
Forbidden paths:          engine/, web/, tests/, schemas, export code, WS implementation files,
                          historical closure records, the W2-A contract record, the W2-ID record,
                          the Wave-2 contract record, preserved evidence
Expected behavior:        status surfaces state current truth; obligations transition only on
                          row-specific evidence; nothing else changes
Non-goals:                W2-A/RVR-4 runtime implementation; any schema/runtime/test/UI change;
                          Path-T activation; persistence/export expansion; W2-B/W2-C; RVR-7/RVR-8;
                          serious-release or paid-activation closure; unrelated cleanup
Acceptance criteria:      the sync Grill SG-1…SG-30 (merge identity verified; every changed path
                          governance-only and necessary; row-specific closure evidence; enactment
                          and release-value obligations remain OPEN; no self-certified closure)
Required tests:           none — documentation-only (zero runtime delta verified mechanically)
Tests not required:       product tests — no product path changes
Dependencies:             PR #567 authoritative merge; the W2-A contract §21 transition plan;
                          PR #566 (register + ODR Wave-2 section)
Unresolved decisions:     the W2-A implementation authorization (separate Owner decision); the
                          open Owner decisions tracked in the Deferred Obligations Register
                          (R4-C, OD-PDVG-10/12/13, OD-PDVG-08b, T2-D ownership, MG-8, OD-A …)
Stop conditions:          any merge-identity mismatch; any pressure to authorize or start W2-A
                          implementation here, to close release-value gates, or to rewrite
                          historical records
Independent-review scope: factual accuracy of the synchronization; row-specific closure evidence;
                          no obligation silently dropped or falsely kept alive; no reviewed-sound
                          contract semantic changed via status text
Merge authority:          owner, separately (candidate is NOT published, PR'd, or merged by the
                          Creator)
```

**Disposition: `POST-W2-A-CONTRACT SYNC — GOVERNANCE CANDIDATE; NOT AUTHORITATIVE UNTIL MERGED
AND POST-MERGE VERIFIED`.** After it merges, the next eligible gate is the
**`W2-A IMPLEMENTATION AUTHORIZATION GATE`** — a separate explicit Owner decision (READY is not
AUTHORIZED). **`W2-A IMPLEMENTATION AUTHORIZED: NO`; `W2-A IMPLEMENTATION STARTED: NO`.**

---

**Superseded (retained as history) — POST-W2-ID STATUS-SURFACE SYNCHRONIZATION + PERMANENT
DEFERRED OBLIGATIONS REGISTER; MERGED AND AUTHORITATIVE via PR #566, merge
`557548db2bb37b21b6b57f893afc2ae1af64744f`.** Its in-block "next eligible gate =
`W2-A AUTHORIZATION / CONTRACT-FREEZE GATE`" line is authority-at-that-time — that gate completed
via PR #567 (see the active block above). Base: **`516a184231f3e19fad6e8f6f3301b5b9c4ad9820`**
— re-verified as the **live authoritative tip** of `feature/atomic-json-session-persistence`
(**0 commits after it**; **PR #565** — the W2-ID v3 merge; first parent `91475e456cbe8ff21bfa8e7bf2fb3e6dd801f762`
(PR #564, W2-D implementation), second parent `a92d4fa4dcea32009b3020b083c08dc8028772d5` — the exact
Owner-accepted W2-ID v3 candidate; merge tree `f5e452ed43c69d6492ca8de611ebeeb547d9c5aa` identical to
the candidate tree; empty candidate→merge diff).

**Current authoritative truth (verified from Git, not prose):** the Wave-2 bounded implementation
contract is **CONTRACT AUTHORITATIVE** (PR #563, merge `58e92e09…`); **W2-D is IMPLEMENTATION
AUTHORITATIVE** (PR #564 — W1-S2 attempt gate + W1-N4 lapse transparency, both follow-ups CLOSED
with evidence); **W2-ID is GOVERNANCE-MINI-GATE AUTHORITATIVE** (PR #565 — identity/recording model
+ the committed Owner decision `OD-W2ID-LEDGER — APPROVED`: AssertionRecord ledger = bounded
decision-capture carrier architecture; FDC-001 `DecisionRecord` = sole canonical decision-semantics
owner; implementation deferred to W2-A). The Wave-1-era `WAVE-2 AUTHORIZED: NO` /
`NEXT GATE: WAVE-2 OWNER AUTHORIZATION` lines retained in the superseded block below are
authority-at-that-time.

```
INCREMENT CONTRACT — Post-W2-ID Status Synchronization + Deferred Obligations Register (governance only)
Objective:                Bring the four live status surfaces to current repository truth
                          (PR #563/#564/#565 arc) and create the permanent
                          DEFERRED_OBLIGATIONS_REGISTER.md seeded from the read-only
                          retrospective reconstruction.
Owner authorization:      the Owner's bounded status-sync + deferred-register write-gate
                          instruction (following the read-only gate's READY disposition) and the
                          Owner's permanent Deferred-Obligations-Register rule
Risk level:               LEVEL 2 — governance/documentation only
Allowed paths:            docs/governance/CURRENT_PROJECT_STATE.md;
                          docs/governance/ACTIVE_EXECUTION_ROADMAP.md (append-only);
                          docs/governance/ACTIVE_INCREMENT_CONTRACT.md (this rotation);
                          docs/governance/OWNER_DECISION_REGISTER.md (append);
                          docs/governance/DEFERRED_OBLIGATIONS_REGISTER.md (new)
Forbidden paths:          engine/, web/, tests/, schemas, export code, WS implementation files,
                          historical closure records, PDVG/TDVP/PVCG records, the W2-ID record,
                          the Wave-2 contract record, W2-D implementation
Expected behavior:        status surfaces state current truth; the permanent register exists;
                          nothing else changes
Non-goals:                W2-A/RVR-4 implementation; any product/runtime/test change; any
                          disposition/field enactment; RVR-6/7/8; deployment/production/paid
Acceptance criteria:      the write-gate Grill G1–G45 (allowlist exact; zero product delta;
                          truthful lineage without retroactive invention; register contract and
                          seeded buckets complete; no self-certified closure)
Required tests:           none — documentation-only
Tests not required:       product tests — no product path changes
Dependencies:             PR #563 / #564 / #565 authoritative merges; the read-only
                          reconstruction (navigation evidence only — repository truth revalidated)
Unresolved decisions:     W2-A authorization (incl. OD-W2A-LEDGER enactment items); the open
                          Owner decisions tracked in the Deferred Obligations Register
Stop conditions:          any merge-identity mismatch; any pressure to authorize W2-A here, to
                          invent retroactive Owner decisions, or to rewrite historical records
Independent-review scope: factual accuracy of the synchronization; register completeness vs the
                          retrospective reconstruction; no obligation silently dropped or falsely
                          kept alive
Merge authority:          owner, separately (candidate is NOT published, PR'd, or merged by the
                          Creator)
```

**Disposition: `POST-W2-ID SYNC + DEFERRED REGISTER — GOVERNANCE CANDIDATE; NOT AUTHORITATIVE
UNTIL MERGED AND POST-MERGE VERIFIED`.** After it merges, the next eligible gate is the
**`W2-A AUTHORIZATION / CONTRACT-FREEZE GATE`** — a separately Owner-authorized gate that must name
the OD-W2A-LEDGER enactment items (exact decision-action disposition vocabulary; explicit
context-attachment representation incl. any exact bounded `AssertionRecord` field proposal; the
frozen RVR-4 implementation contract). **`W2-A IMPLEMENTATION AUTHORIZED: NO`;
`W2-A IMPLEMENTATION STARTED: NO`.**

---

**Superseded (retained as history) — WAVE-1 REMEDIATION AUTHORITATIVE CLOSURE / SYNCHRONIZATION;
MERGED AND AUTHORITATIVE via PR #562, merge `e02d175b93556213e22e6af0decd66f12966ff7f`.** Its
in-block `WAVE-2 AUTHORIZED: NO` and `NEXT GATE: WAVE-2 OWNER AUTHORIZATION` lines are
authority-at-that-time — superseded by the PR #563/#564/#565 arc recorded in the active block
above. Base: **`93be682a34c1221f0af7f7018af9023a9b6c5b2c`** — re-verified at that gate as
the **live authoritative tip** of `feature/atomic-json-session-persistence` (**0 commits after it**;
**PR #561** — the Wave-1 remediation merge; first parent
`e119d60450f40b1633433625ae6a011eec112b79` (PR #560, the authoritative S2 extension), second parent
`cd7ed9451ec33886e1e032c9ae6c2016be80949b` — the exact Owner-accepted Wave-1 candidate; merge tree
`666e75ec7fc6d93307f7ac3e86d97f2d09c6dfda` identical to the candidate tree; empty candidate→merge
diff). **Supersession check: the superseded S2-extension block below is retained as history** with its
banner naming exactly which of its lines are authority-at-that-time.

```
INCREMENT CONTRACT — Wave-1 Remediation Authoritative Closure / Synchronization (governance only)
Objective:                Record Wave-1 (RVR-1/2/3/5 + continuation repair) as IMPLEMENTED /
                          AUTHORITATIVE at merge 93be682a (PR #561); synchronize the governance
                          surfaces; record the Owner decisions consumed; carry the five follow-ups
                          (W1-S2, W1-N1, W1-N2, W1-N3, W1-N4) without implementing any.
Owner authorization:      the Owner Wave-1 closure/sync gate instruction, following Owner exact-SHA
                          acceptance of cd7ed945… and the PR #561 merge
Risk level:               LEVEL 2 — governance/documentation only
Allowed paths:            docs/governance/WAVE_1_REMEDIATION_FORMAL_CLOSURE_RECORD.md (new);
                          docs/governance/OWNER_DECISION_REGISTER.md;
                          docs/governance/ACTIVE_EXECUTION_ROADMAP.md;
                          docs/governance/ACTIVE_INCREMENT_CONTRACT.md;
                          docs/governance/CURRENT_PROJECT_STATE.md
Forbidden paths:          engine/, web/, tests/, domains/, database/, schemas/, prompts/, scripts/,
                          benchmark/, CI, runtime/deploy, main, accepted evidence, the S2 run
                          evidence (refs/evidence/s2run-ebf243db), the merged Wave-1 chain
Expected behavior:        governance surfaces state current truth; nothing else changes
Non-goals:                Wave-2 work; RVR-4/6/7/8; any S2 rerun; T1-A' closure; MLC freeze;
                          implementing any W1 follow-up; editing any historical record
Acceptance criteria:      Grill checklist of the gate instruction (base identity; changed-path
                          allowlist exact; zero product/test delta; per-environment test truth;
                          all five follow-up IDs present; no stale pre-merge Wave-1 status in the
                          changed surfaces; no duplicate owner; no contradiction)
Required tests:           none — documentation-only (product suite untouched at the merged tree)
Tests not required:       product tests — no product path changes
Dependencies:             PR #560 (S2 extension authoritative, e119d604…); S2-PATHN-RUN-001 evidence
                          (ebf243db…); the Owner-frozen Final Remediation Contract (RVR-1…RVR-8);
                          PR #561 (93be682a…)
Unresolved decisions:     Wave-2 authorization; OD-PDVG-03, 04, 05, 06, 07, 08a, 08b, 09, 10, 12, 13
Stop conditions:          any merge-identity mismatch; any pressure to overstate Wave-1 into
                          release-value closure or to authorize Wave-2/S2-rerun from this record
Independent-review scope: faithfulness of the closure record to Git and preserved evidence;
                          correctness of the supersession statements; boundary preservation
Merge authority:          owner, separately (this candidate is NOT published, PR'd, or merged by
                          the Creator)
```

**Disposition: `WAVE-1 CLOSURE / SYNC — GOVERNANCE CANDIDATE; NOT AUTHORITATIVE UNTIL MERGED AND
POST-MERGE VERIFIED`.** Record: `docs/governance/WAVE_1_REMEDIATION_FORMAL_CLOSURE_RECORD.md`.
Authoritative facts it records (verified from Git/probes, never memory): Wave-1
`RVR-1 / RVR-2 / RVR-3 / RVR-5: IMPLEMENTED, AUTHORITATIVE` and
`POST-DISPOSITION CONTINUATION REPAIR: AUTHORITATIVE` at merge `93be682a…`; test truth per-environment
(Creator `4512 passed / 3 skipped / 1 xfailed / 0 failed`; Independent Reviewer `4511 passed /
4 skipped / 1 xfailed / 0 failed` — environment-conditional skip, not a regression); the five
follow-ups W1-S2, W1-N1, W1-N2, W1-N3, W1-N4 recorded and NOT implemented; Owner decisions OD-R1,
OD-R2, OD-PDVG-02(a) consumed and OD-R3 / OD-R5 / OD-R4 accepted in principle (register Wave-1
section). **Boundaries:** `WAVE-1 RELEASE-VALUE CLOSED: NO`; `T1-A′ CLOSED: NO`; `S2 PASSED: NO
CLAIM`; `SECOND S2 RUN AUTHORIZED: NO`; `WAVE-2 AUTHORIZED: NO`; `RVR-4 / RVR-6 / RVR-7 / RVR-8: NOT
AUTHORIZED`; `TIER-2 MEANING-ADAPTIVE QUESTIONING: NOT AUTHORIZED`; `MLC DEFINITION FROZEN: NO`;
`ILT ROUND AUTHORIZED: NO`; `AI ACTIVATED: NO`; `PSRR GO: NO`; `DEPLOYMENT AUTHORIZED: NO`;
`PRODUCTION AUTHORIZED: NO`; `PAID ACTIVATION AUTHORIZED: NO`.
**`NEXT GATE: WAVE-2 OWNER AUTHORIZATION`.**

---

**Superseded (retained as history) — OWNER DECISION ACTIVATION / BOUNDED S2 EXTENSION GATE; MERGED
AND AUTHORITATIVE via PR #560, merge `e119d60450f40b1633433625ae6a011eec112b79`.** Since that merge:
the block's `S2 BENCHMARK RUN EXECUTED: NO` lines are authority-at-that-time — the one authorized run
`S2-PATHN-RUN-001` has since been **EXECUTED** (evidence `ebf243db…`, ref `refs/evidence/s2run-ebf243db`;
no record achieved a full pass; the OD-PDVG-01(a) run authorization is **EXERCISED AND CONSUMED**) —
and its "twelve … remain UNDECIDED" lines are likewise authority-at-that-time: **OD-PDVG-02 is now
DECIDED — OPTION (a)** and consumed by Wave-1 RVR-5 (see the Wave-1 section of
`OWNER_DECISION_REGISTER.md`). Everything else in the block stands as written.
Base: `a9b9d53cb15165ec9ed0b35962577449750ff663` — re-verified at that gate as the
**live authoritative tip** of `feature/atomic-json-session-persistence` (**0 commits after it**; PR #559;
first parent `1295ed08…`, second parent `df941501…` — the exact Owner-accepted PDVG-01 candidate — merge
tree `c726bd15…` identical to the candidate tree; empty candidate→merge diff). **Supersession check:
NONE.** PDVG-01 is **AUTHORITATIVE** and is **not reopened, not re-adjudicated, and not edited here.**

```
INCREMENT CONTRACT — Bounded S2 Path-N Release-Evaluation Extension (governance/contract only)
Objective:                Record Owner decisions OD-PDVG-11(a) and OD-PDVG-01(a), and define the
                          bounded S2 extension contract that makes PDVG-01 T1-A' executable.
Owner authorization:      Owner Decision Activation / Bounded S2 Extension Gate, recorded at
                          docs/governance/evidence/pdvg_owner_decisions/
                          OD-PDVG-11_OD-PDVG-01_S2_BOUNDED_EXTENSION_ACTIVATION.md
Risk level:               LEVEL 2 — governance/documentation only
Allowed paths:            docs/benchmarks/BICYCLE_BRAKE_LIGHT_COMPETITIVE_BENCHMARK.md (SS15-17 only);
                          docs/governance/evidence/pdvg_owner_decisions/ (new record);
                          docs/governance/OWNER_DECISION_REGISTER.md;
                          docs/governance/ACTIVE_EXECUTION_ROADMAP.md;
                          docs/governance/ACTIVE_INCREMENT_CONTRACT.md;
                          docs/governance/CURRENT_PROJECT_STATE.md
Forbidden paths:          engine/, web/, tests/, domains/, database/, schemas/, prompts/, scripts/,
                          benchmark/, CI, runtime/deploy, main, accepted evidence, PDVG-01 record,
                          BICYCLE_BRAKE_LIGHT_COMPETITIVE_BENCHMARK.md SS0-14
Expected behavior:        The extension contract exists and is complete; nothing is executed.
Non-goals:                running S2; any product implementation; any lane/domain/phase activation;
                          freezing the MLC; deciding any other OD-PDVG decision
Acceptance criteria:      SS13 required contract properties all present; NOT APPLICABLE set derived
                          from source, not memory; criterion-12 protection binding; single owner
                          preserved; executable delta 0
Required tests:           none — documentation-only
Tests not required:       product tests — no product path changes
Dependencies:             PDVG-01 (authoritative); S2 SS2 and SS11 amendment mechanisms;
                          D-AISR-06 / D17 / PVCG-R4 (criterion-12 protection)
Unresolved decisions:     OD-PDVG-02, 03, 04, 05, 06, 07, 08a, 08b, 09, 10, 12, 13 — ALL STILL OPEN
Stop conditions:          any contradiction between the approved S2 scope and authoritative
                          repository truth; any pressure to alter the product to satisfy a criterion
Independent-review scope: legitimacy of extending S2 rather than duplicating it; sufficiency and
                          boundedness of the approved scope; correctness of the NOT APPLICABLE set;
                          criterion-12 architectural safety; MLC non-freeze; no unauthorized execution
Merge authority:          owner, separately
```

**Disposition: `S2 BOUNDED EXTENSION — CONTRACT CANDIDATE; NOT AUTHORITATIVE UNTIL MERGED AND
POST-MERGE VERIFIED`.** Contract: `docs/benchmarks/BICYCLE_BRAKE_LIGHT_COMPETITIVE_BENCHMARK.md`
**§§15–17** (*Path-N Release-Evaluation Extension v1*); **§§0–14 unchanged**. Owner-decision evidence:
`docs/governance/evidence/pdvg_owner_decisions/OD-PDVG-11_OD-PDVG-01_S2_BOUNDED_EXTENSION_ACTIVATION.md`.
Authorizes **NO** implementation and **NO** benchmark run.

**Owner decisions recorded: 2 of 14.** `OD-PDVG-11` — OPTION (a) (approve the bounded extension scope);
`OD-PDVG-01` (revised) — OPTION (a) (authorize the extension **and**, once it is authoritative, **one**
run against the exact release candidate). **The other twelve — 02, 03, 04, 05, 06, 07, 08a, 08b, 09, 10,
12, 13 — remain UNDECIDED**, and no approval of any of them is implied by adjacency.
`OWNER_DECISION_REGISTER.md` **CHANGED** — two accepted rows added; the twelve open decisions named.

**Single owner preserved.** The extension is made under S2's **own** mechanisms — §2 (authorized case
revision: version, reason, date, comparison-impact note — all four supplied) and §11 (*"Benchmark
criteria and protocol may be owner-approved"*). **NO second benchmark owner, no "Golden Reasoning
Benchmark", no parallel evaluation programme, no duplicate reasoning-quality framework.**

**Approved scope.** Two frozen cases: **E-1** electronics (existing §2 case, **unchanged**) and **M-1**
mechanical (foldable wheelchair ramp; `folded-position retention architecture`; three bounded candidates,
each `artifact_origin_status=inferred`, `evidence_status=advisory`). **EN + AR** on the release-relevant
Path-N experience, not translation-string existence. **Novice + experienced-technical evaluation
perspectives**, recorded separately — an **evaluation instrument**, never describable as real-user
research. Added criteria **`P1…P6`**; evidence visibility, provenance and truthful-block/bounded-
recommendation carried by **existing** criteria 4 and 7, not duplicated. **No new domain activation; no
third case.**

**`NOT APPLICABLE` = exactly two: criteria 12 and 13**, plus the §6 core gate as written (scoped verbatim
*"For the first Technical Decision Workspace increment"*). **Disclosed narrowing:** T1-A′ anticipated
`(9–14)`; source reconstruction narrows it to `{12, 13}` — criteria 9, 10, 11 and 14 each have a real
Path-N counterpart. **T1-A′'s rule is applied unchanged; only its parenthetical enumeration diverges, and
the divergence narrows what is excused.** `NOT APPLICABLE` is **never** a substitute for `FAIL`.

**Rejected evidence — enumerated once, elsewhere.** The single authoritative enumeration of this gate's
rejected candidates — every SHA, each rejection reason — is **§9 of the Owner-decision evidence record**
(`docs/governance/evidence/pdvg_owner_decisions/OD-PDVG-11_OD-PDVG-01_S2_BOUNDED_EXTENSION_ACTIVATION.md`).
This surface deliberately restates **neither the SHAs, nor the reasons, nor a count** — a copy of that
list goes stale the moment the list grows. Each rejected candidate is preserved as a local ref matching
`refs/rejected/s2ext-<short-sha>` (one per §9 row) and carried in the SHA-preserving bundle; **none
published, none amended, rebased, or squashed**; each surviving candidate is a **sibling from the
authoritative base**.

**Domain-gate protection is binding.** `classify_domain` is **wording-sensitive** **[EXEC]** — neither
case's bare concept resolves, and the **electronics** case E-1 resolves to **`mechanical`** when stated
with its own §3 candidate 1 — so the contract **freezes the English seed text** under one
outcome-independent construction applied to both cases (*product-concept line, then user-context sentence,
verbatim, em-dash joined*), measured as **`NONE`** for E-1 and **`mechanical`** for M-1, **recorded not
corrected**; the **Arabic** seeds freeze **at first use**, admissible only because an Arabic seed cannot
resolve a domain at all. Each
run records the exact seed text per case and per language; **rewording a case to change a gate outcome is
prohibited** (any seed change is a §2 case revision); **`engine/domain_rules.py`, the registry, the
activation set and the `/start` admission policy are never changed to admit a benchmark case**; and a
resolved domain is **never** asserted to be the case's "correct" domain. A blocked or consent-routed
frozen case is a **truthful reportable result**. **The Arabic dimension carries the same protection:**
`domain_rules.py` and every domain pack contain **no Arabic text** **[EXEC]**, so an Arabic-only seed
**cannot** resolve a domain (measured `NONE` for both) and an Arabic run reaches the classifier-miss path
for **both** cases — a property to evaluate, with **no** Arabic classifier/pack/admission vocabulary
authorized. **One run = 2 cases × 2 languages × 2 perspectives = 8
evaluation records**, reported separately, no aggregate, never split into extra "runs". Baseline B is an
**evaluator activity outside the product**; `AI_ADVISORY_ENABLED` unchanged.

**Criterion-12 protection is binding.** `validity_status` occurs in **no** Python file **[EXEC]**;
targeted partial invalidation is **PROHIBITED** (`D-AISR-06` full deterministic re-evaluation, preserving
`D17`; PVCG-R4) **[REPO]**. It must **never** be satisfied by introducing stale-marking into the product.
**`D17` / `D-AISR-06` / PVCG-R4 semantics UNCHANGED.**

**MLC boundary.** `MLC DEFINITION FROZEN: NO`; `MINIMUM LAUNCH-CONFORMANCE SET SATISFIED: NO`;
**OD-PDVG-07 remains separate and undecided.** Approving the S2 scope discharges only reason (ii) of the
two PDVG-01 gave for making no recommendation on OD-PDVG-07; reason (i) — no independent review of the
corrected Tier-1 set — **stands**. **`OD-PDVG-10 BLOCKS MLC DEFINITION: NO`** and **`OD-PDVG-10 BLOCKS
FIRST SERIOUS RELEASE: NO`** are preserved (§4A.5).

**Superseded PDVG-01 §11 lines — stated, not hidden.** `OWNER DECISIONS RECORDED AS MADE: 0` → **2**;
`S2 EXTENSION AUTHORIZED: NO` → **YES (scope approved; contract defined; run not executed)**. Every other
PDVG-01 §11 line stands unchanged, and PDVG-01 is not edited. The same supersession applies to the
`Recorded as made: 0` and `S2 EXTENSION AUTHORIZED: NO` lines in the superseded PDVG-01 block below,
which are retained as authority-at-that-time.

**Scope.** Governance/documentation ONLY. `EXECUTABLE/TEST/PIN/PACK/DOMAIN-RULE DELTA: 0`; `main` not
reconciled; no historical record rewritten. `S2 BENCHMARK RUN EXECUTED: NO`; `S2 BENCHMARK RUN AUTHORIZED
NOW: NO`; `SECOND BENCHMARK OWNER CREATED: NO`; `NEW WORKSTREAMS CREATED: 0`; `NEW OWNERS CREATED: 0`;
`NEW DOMAINS ACTIVATED: NO`; `WS16 EXTENSION AUTHORIZED: NO`; `ILT ROUND AUTHORIZED: NO`;
`TIER-1 IMPLEMENTATION AUTHORIZED GENERALLY: NO`; `AI ACTIVATED: NO`; `PSRR GO: NO`;
`DEPLOYMENT AUTHORIZED: NO`; `PRODUCTION AUTHORIZED: NO`; `PAID ACTIVATION AUTHORIZED: NO`;
`T1-C′ STILL INDEPENDENTLY REQUIRED: YES`.

**Verdict provenance, kept distinct.** `UNSUPPORTED MATERIAL CLAIMS` is an INDEPENDENT-REVIEWER field:

```
Creator Grill unsupported-material-claim finding (this candidate) : 0
Independent review of THIS candidate                             : NOT YET PERFORMED,
                                                                   as at the time of submission
```

---

**Superseded (retained as history) — PDVG-01: PRE-RELEASE PRODUCT DEPTH & VALUE GATE; MERGED AND
AUTHORITATIVE via PR #559, merge `a9b9d53cb15165ec9ed0b35962577449750ff663`.** Base:
`1295ed08ec902f2fcc21934eac3622548a44719b` — re-verified this gate as the **live authoritative tip** of
`feature/atomic-json-session-persistence` (0 commits after it; PR #558; first parent `2da8a6a3…`, second
parent `1f5989b5…`; merge tree `bdb6e6b9…`; empty candidate→merge diff; clean tree). TDVP Outcome A and
`PVCG FORMALLY CLOSED / SATISFIED: YES` stand unchanged and are not reopened.

**Disposition: `PDVG-01 CLASSIFICATION CANDIDATE — NOT AUTHORITATIVE UNTIL MERGED`.** Record:
`docs/governance/PDVG_01_PRE_RELEASE_PRODUCT_DEPTH_AND_VALUE_GATE_RECORD.md`. Classifies product-depth work in four kinds —
**adequately owned**, **partially owned**, **dormant/planned**, and **independently proven ownership
gaps**; **two §9 rows have no current owner** (semantic adaptive questioning; user-feedback capture).
**NEW WORKSTREAMS: 0; NEW OWNERS: 0; no new numbering for existing workstreams** — a proven gap is
surfaced, never resolved here. Authorizes NO implementation.

**Rejected evidence: ELEVEN candidates, none published to `origin`.** `da8c1fd8…` (Creator Grill CG-1/CG-2),
`5974baf7…` (CG-3), `fd7de207…` (**Independent External Review REJECT** — truthfulness rated HIGH;
rejected on ownership architecture and release classification), `d6d55db0…` (Re-Grill RG-1),
`97233ad9…` (RG-2), `8cddcda3…` (Instruction-to-Result Audit P1–P5), `fa93acef…` (post-Grill audit —
stale rejected-evidence aggregate), **`ecc9bde9…` (substantive Independent External Review REJECT —
F-1 governance consistency)**, and **`1a9cdad7…` (reviewer micro-repair directive — §12.1a
historical-reference precision)**, **`b287c4b6…` (pre-review audit B24)**, and **`615fcb8e…` (Creator
pre-freeze self-check — B24-F2 recurrence)**. **All eleven are retained as local refs and included in
the SHA-preserving bundle; none amended, rebased, or published.** Count derived per the §12.3 rule. Each of
the Independent Review's **three blocking findings** was **independently re-proved from source**, not
accepted on the reviewer's authority.

**TRUE OWNERSHIP GAP RECORDED.** Semantic adaptive questioning is owned by **no** workstream, capability
or phase: WS10 contract L71, WS11 D14, and WS14 L59/L227 each exclude it in their own text;
`gap_relevance` is *"LEXICAL … not a semantic component"*; **WS11.2 has no contract, file or §15 row**;
and **WS4 §17 records the capability as wanted and ownerless by explicit disclaimer**. The merged TDVP
`TRUE RESIDUAL GAP COUNT: 0` is **preserved as authority-at-that-time and NOT rewritten**; current truth
is restated as `UNOWNED CAPABILITY GAP COUNT (PDVG-01 reconstruction): 1` pending **OD-PDVG-10**. Class:
**Tier 2 (T2-G)** — SHOULD before first release under a binding no-implied-adaptivity condition, **MUST
before paid activation**; **not** force-fitted into WS14 or WS11.

**Corrections carried.** **T1-A′** — S2 is scoped to the Technical Decision Workspace lane (core gate
verbatim; `validity_status` occurs in no Python file; 8 dimensions at zero coverage), so T1-A becomes a
**bounded S2 extension under the existing owner, then one run**; no second benchmark owner; §8 row 2
re-marked PARTIAL. **T2-C′** — WS16 is read-only and electronics-only, ~6 of 14 dimensions, so unchanged
re-execution is replaced by a **bounded WS16 extension** under the existing §15 row; **PSRR not
expanded**. **Evidence ladder re-tiered** into T1-D (truthful disclosure), T2-E (writer mapping) and
T2-F (ordering repair **+ mandatory guard test**). **WS10/display split** — the render is excluded by
WS10 L71; the adequate owner is **Phase 3 Product UX/UI**, the same lane as T1-B. **WS11 two axes** —
activation blocked, **importance HIGH**. **ILT** requires **≥1 experienced technical participant**.
**Tier 4 relabelled** `STRATEGICALLY PRESERVED / NOT RELEASE-SEQUENCED`. **Longitudinal** — a timestamp
is **not required**.

**Tier classification groups** (§5 entries, not literal item counts): **4 / 7 / 4 / 6**; **exact §9
matrix rows: 4 / 8 / 5 / 8, total 25**, no ambiguous tier. **Contradiction ledger (§10A): 7 rows.**
`MLC DEFINITION FROZEN: NO` — the Tier-1 set is **not** proposed as the MLC, for two evidenced reasons:
it has not itself been independently reviewed, and **T1-A′'s scope is undefined pending OD-PDVG-11**.
**OD-PDVG-10 does NOT gate MLC definition and does NOT block first serious release** (§4A.5): an unowned
**Tier-2** item is not a member of the launch-conformance set. *"First serious release"* remains
undefined as a repository fact.

**Scope.** Governance/documentation ONLY. `EXECUTABLE/TEST/PIN/PACK/DOMAIN-RULE DELTA: 0`; `main` not
reconciled; `OWNER_DECISION_REGISTER.md` UNCHANGED; no historical record rewritten.
`PDVG-01 IMPLEMENTATION STARTED: NO`; `TIER-1 IMPLEMENTATION AUTHORIZED: NO`; `S2 EXTENSION AUTHORIZED:
NO`; `ILT ROUND EXECUTED: NO`; `NEW DOMAINS ACTIVATED: NO`; `PSRR GO: NO`; `DEPLOYMENT AUTHORIZED: NO`;
`PRODUCTION AUTHORIZED: NO`; `PAID ACTIVATION AUTHORIZED: NO`.

**Verdict provenance, kept distinct.** `UNSUPPORTED MATERIAL CLAIMS` is an INDEPENDENT-REVIEWER field:

```
Creator Grill unsupported-material-claim finding (this repair candidate) : 0
Independent review of the PRIOR candidate fd7de207                      : REJECT on ownership
                                                                          architecture and release
                                                                          classification; truthfulness
                                                                          rated HIGH
Independent review of THIS repair candidate                             : NOT YET PERFORMED,
                                                                          as at the time of submission
```

**Owner decisions surfaced: 14** — 01, 02, 03, 04, 05, 06, 07, **08a**, **08b**, 09, 10, 11, 12, 13
(08a/08b independently actionable, counted separately; no plain OD-PDVG-08). **Recorded as made: 0.**

---

**Superseded (retained as history) — TDVP: POST-PVCG RECONCILIATION; MERGED AND AUTHORITATIVE via
PR #558, merge `1295ed08…`.** Base:
`2da8a6a3bb832bf3326c4cb7cc9e1dc8a99499e7` (PR #557 merge — PVCG FINAL FORMAL CLOSURE, AUTHORITATIVE;
live tip re-fetched and independently re-verified: first parent `ca9fb4be…`, second parent `106d3b52…`
— the exact Owner-accepted candidate — merge tree `cdbf4c36…` identical to the candidate tree, empty
candidate→merge diff, zero later commits, clean tree). `PVCG FORMALLY CLOSED: YES`;
`PVCG SATISFIED: YES` (bounded R1–R4 scope) — unchanged and not reopened.

**Disposition: `TDVP RECONCILIATION CANDIDATE — NOT AUTHORITATIVE UNTIL MERGED`.** Record:
`docs/governance/TDVP_POST_PVCG_RECONCILIATION_RECORD.md`. Discharges the merged PVCG closure record's
§7.4 clause (TDVP *"subject to post-PVCG reconciliation"*). Authorizes NO implementation.

**Outcome A — NO NEW PROGRAM REQUIRED.** All ten provisional TDVP topics eliminated as new-workstream
candidates by duplicate/overlap/supersession reconciliation against current ownership: WS6 Requirements
(quantified fields = extension residual, not a second model); domain rules + P9-QS + STG-deferred
depth; `GroundedRisk` linkage with state-engine propagation still PROHIBITED (D17/D-AISR-06/R4-C);
Increment-2 evidence axes + CAP-11; WS7 + prototype & test plan + FPC-01; D13 + AISR + FPC-04 +
WS-PFV-001; P9-QS + registry (active set unchanged: electronics_electrical + mechanical); deliverable +
P7-I1 + FPC-04A; P7-I1/P7-I3 vendor-neutral export (one-way — never to be labelled round-trip; inbound
ingestion directionally AISR/STG); WS8–WS17 question/journey family with WS10/WS11 built-dormant and
the `FULL ADAPTIVE QUESTIONING ACTIVATED: NO` fence in eight committed documents. **TRUE RESIDUAL GAP
COUNT: 0**; every surviving residual fact is owned; **one optional Owner decision surfaced** (admit the
quantified-requirements WS6 extension as a future bounded increment), none recorded. **The provisional
TDVP program name is RETIRED effective on merge**; no numbering carried forward; every disposition is
`PLANNED / GOVERNED — NOT YET IMPLEMENTATION-AUTHORIZED` unless a cited owner already carries its own
authorization. Preserved without drift: R4 correction route IMPLEMENTED; rendered correction UX NOT
DELIVERED (Phase-3C / FPC-02, NOT STARTED / NOT AUTHORIZED, not absorbed into TDVP).

**Scope.** Governance/documentation ONLY. `RUNTIME/TEST/PIN/PACK/DOMAIN-RULE DELTA: 0`; `main` not
reconciled; `OWNER_DECISION_REGISTER.md` UNCHANGED. `TDVP IMPLEMENTATION STARTED: NO`;
`NEW DOMAINS ACTIVATED: NO`; `PSRR GO: NO`; `DEPLOYMENT AUTHORIZED: NO`; `PRODUCTION AUTHORIZED: NO`.

**Verdict provenance, kept distinct.** `UNSUPPORTED MATERIAL CLAIMS` is an INDEPENDENT-REVIEWER field:

```
Creator Grill unsupported-material-claim finding (this candidate) : 0
Independent review of this reconciliation candidate              : NOT YET PERFORMED,
                                                                   as at the time of its submission
```

---

**Superseded (retained as history) — PVCG: AUTHORITATIVE CLOSURE OF THE R1–R4 PROGRAM; MERGED AND
AUTHORITATIVE via PR #557, merge `2da8a6a3…`.** Base: `ca9fb4be818f62a7e78a72ce6c97c707bba9807c` (PR #556 merge — PVCG-R4 FORMAL CLOSURE,
AUTHORITATIVE; live tip re-fetched and independently re-verified: first parent `5ed09180…`, second
parent `713a48fd…` — the exact Owner-accepted R4 closure candidate — merge tree `eb105e95…` identical
to the candidate tree, empty candidate→merge diff, zero later commits, clean tree).

**Disposition: `PVCG CLOSURE CANDIDATE — NOT AUTHORITATIVE UNTIL MERGED`.** Closure statements live in
`docs/governance/PVCG_FORMAL_CLOSURE_RECORD.md` and take effect only on merge and post-merge
verification.

**Authority, reconstructed honestly.** No committed document defines PVCG or PVCG-wide closure
criteria (re-confirmed fresh); the two master remediation plans and `OWNER_DECISION_REGISTER.md`
contain zero PVCG mentions. Closure is therefore NOT required by repository contract; it is AUTHORIZED
by the Owner's PVCG FINAL directive, and the record fixes the scope as an **[OWNER]** definition —
*PVCG = the R1–R4 conformance program, nothing wider*.

**Matrix: 14 MET / 1 PENDING (the record) / 0 NOT MET.** R1 authoritative (PR #547 `c70bad19…`,
ancestor), R2/R3/R4 formally closed (merges `ca98099e…` / `18a90f9b…` / `ca9fb4be…`, all verified from
lineage). **All behavioral evidence FRESH on `ca9fb4be…`:** R1 **26**; R2 **189** + **566**; R3
**579**; R4 **63**; P9 **54**; WPS-001 **20/1**; smoke **PASS**; full suite **4418 / 3 / 1 / 0**; plus
a 15/15 integrated cross-capability probe (EN+AR journey, R1 disposition, R2 fail-closed, UI language
not switching on Arabic input, R4 tokened correction, withdrawn basis absent from the whole package,
marker exactly 1, restart-reconstruction reproducing the corrected state with full ledger and
retained-inactive superseded record, deterministic, no fabricated contradiction). Pins and packs
re-measured, all matching; protected test files byte-identical to the R3-closure baseline through the
R4 lineage.

**MLC:** name + status lines + one `[OWNER]` membership sentence only; **no definition exists and none
is invented**; `MINIMUM LAUNCH-CONFORMANCE SET SATISFIED: NO`; `FULL MLC DEFINITION FROZEN: NO`;
committing a definition remains an OPEN Owner decision that does not block this closure.

**R4 clarification preserved:** `R4 correction route: IMPLEMENTED`; `Rendered correction UX: NOT
DELIVERED` (owner Phase-3C / FPC-02, NOT STARTED / NOT AUTHORIZED); zero templates claim a correction
feature; no statement may imply UI correction exists.

**Residuals:** PVCG-internal OPEN/NON-BLOCKING (replay bound 500 unrepaired/unassigned, token
semantics, NB-3/NB-4, N-2/U-4, bundle-ref hygiene) vs outside-PVCG open release items (OBS-P5-2-01
provider portion, no HSTS, email provider, Render, PSRR GO, legal/tax, payment, OD-A, `main`
reconciliation, future domains) — none suppressed, none absorbed. **TDVP: provisional candidate only;
nothing created, promoted or activated.**

**Scope.** Governance/documentation ONLY. `RUNTIME DELTA: 0`; `TEST DELTA: 0`; `PIN DELTA: 0`;
`PACK DELTA: 0`; `DOMAIN-RULE DELTA: 0`; `main` not reconciled; `OWNER_DECISION_REGISTER.md`
UNCHANGED. `RENDERED CORRECTION UX DELIVERED: NO`; `TDVP STARTED: NO`; `PSRR GO: NO`;
`DEPLOYMENT AUTHORIZED: NO`; `PRODUCTION AUTHORIZED: NO`. Closing PVCG closes only PVCG as scoped.

**Verdict provenance, kept distinct.** `UNSUPPORTED MATERIAL CLAIMS` is an INDEPENDENT-REVIEWER field:

```
Creator Grill unsupported-material-claim finding (this candidate) : 0
Independent review of this closure candidate                     : NOT YET PERFORMED,
                                                                   as at the time of its submission
```

---

**Superseded (retained as history) — PVCG-R4: AUTHORITATIVE CLOSURE; MERGED AND AUTHORITATIVE via
PR #556, merge `ca9fb4be…`.** Base:
`5ed09180c7b3bc1809785ed425d4820d5ffc71b7` (PR #555 merge — PVCG-R4-I, AUTHORITATIVE; live tip
re-fetched from `origin/feature/atomic-json-session-persistence` and independently re-verified: first
parent `c3d9e2d98ba7b6c9b3a9d9d316e6d572122d8a8e`, second parent
`2bb472a07f9ac9177070c131c5c7f13ee3cd718a` — the exact Owner-accepted candidate — merge tree
`506b2dd4a8994ced79ada0215e0f389db92b4e53` identical to the candidate tree, empty candidate→merge diff,
zero later commits, working tree clean).

**Disposition: `PVCG-R4 CLOSURE CANDIDATE — NOT AUTHORITATIVE UNTIL MERGED`.**
`PVCG-R4-C AUTHORITATIVE: YES` (PR #554). `PVCG-R4-I AUTHORITATIVE: YES` (PR #555). The closure
statements live in `docs/governance/PVCG_R4_FORMAL_CLOSURE_RECORD.md` and take effect only on merge and
post-merge verification.

**Why this gate exists, cited.** `PVCG_R4_C…CONTRACT.md` §21 requires as criterion **15** *"**a formal
closure record merged**, exactly as R2 and R3 required"*, so the implementation merge alone does not
close R4. **`CLOSURE REQUIRED BY CONTRACT: YES`.**

**THE MATERIAL DISTINCTION.** `R4 correction mechanism / explicit route: IMPLEMENTED`.
`Rendered correction UX: NOT DELIVERED IN THIS GATE`. `Deferred to: Phase-3C / FPC-02 (NOT STARTED /
NOT AUTHORIZED)`. `POST /session/<sid>/correct` is reachable by an HTTP client but **NOT by clicking
anything in the product** — `web/templates/` is byte-unchanged across the whole R4-I lineage. **No
statement may claim users can now correct prior answers through the product UI.** Contract-conformant
per §2.2 (disjunctive residual), §17 (*"expressible"*), §2.5 and §19.2 (UX increment deferred and out of
scope), §21 (no rendered criterion) and §13 E-1 (constrains the affordance, does not create one).

**All fifteen §21 criteria resolved; 1–14 re-measured on the merged tree.** Focused R4-I **63**; R1
**26** (file byte-unchanged vs both `18a90f9b…` and `c3d9e2d9…`); R2 **189** + **566** (byte-unchanged);
R3 **579** (byte-unchanged); P9 **54**; WPS-001 **20 passed / 1 skipped** (byte-unchanged); smoke
**PASS**; full suite **4418 passed / 3 skipped / 1 xfailed / 0 failed**; §20 reconciliation
**4355 + 63 = 4418** — the **4418** and **63** measured fresh on this merged tree, the **4355** baseline
measured on `c3d9e2d9…` (the R4-C merge tip), **not** on `18a90f9b…`, carrying back only because PR #554
was governance-only. Criterion 3 measured in both halves: the §3.2 scenario as written is unchanged
**by design** (§6 C-1 forbids inferring a correction from wording — a committed test pins it), while the
governed correction path clears **all seven** measured withdrawn-basis field paths — a strict superset
of the four §3.2 named — and surfaces the marker. The §3.2 count of four is **not** rewritten.

**Pin / pack.** `progression_loop.py` `3cbd7684…` → `c268cd63…`, all THREE ENFORCING locations carrying
the new digest with disclosed notes preserving the prior one; kind (2) synchronized; kind (3) historical
untouched (`PVCG_R2_C`, `PVCG_R2_FORMAL_CLOSURE_RECORD.md`, `PVCG_R3_C`,
`PVCG_R3_FORMAL_CLOSURE_RECORD.md` all **0 files changed**). `PACK DELTA: 0`; `domain_rules.py`,
`path_n_questions.py` and all five packs byte-identical; `record_store.py` byte-unchanged with **no
`UPDATE` statement at all** — no schema migration.

**Residuals OPEN / NON-BLOCKING, none silently repaired:** the **replay bound** (`MAX_ACCEPTED_ANSWER_
REPLAY = 500`) — pre-existing, **NOT repaired**, reproduced before any edit and pinned by test; the fix
was to the MESSAGE (now conditional), never to the bound, which stays a separately recorded unassigned
observation; stateless answer-token semantics (reused unchanged); **NB-3 and NB-4 deliberately NOT
addressed**; bundle extra-ref hygiene; the deferred rendered UX; and R3's N-2 / U-4, never admitted.

**Scope.** Governance/documentation ONLY. `RUNTIME DELTA: 0`, `TEST DELTA: 0`, `PACK DELTA: 0`,
`PIN DELTA: 0`; `main` not reconciled; `OWNER_DECISION_REGISTER.md` UNCHANGED.
`RENDERED CORRECTION UX DELIVERED: NO`; `TDVP STARTED: NO`; `PVCG SATISFIED: NO`;
`FULL MLC DEFINITION FROZEN: NO`; `DEPLOYMENT AUTHORIZED: NO`. **No successor gate is opened.**

**Verdict provenance, kept distinct.** `UNSUPPORTED MATERIAL CLAIMS` is an INDEPENDENT-REVIEWER field:

```
Creator Grill on the first frozen closure candidate 08561f9e6eeee9f720994815a56875ca35cd460b:
  VERDICT = REJECTED BY CREATOR GRILL
  Defect  = CG-2, unsupported material claim: the 4355 baseline was attributed to a
            re-measurement on 18a90f9b (the R3-closure merge). No suite was ever run
            on that tip; it was measured on c3d9e2d9, the R4-C merge tip.
  SHA preserved unchanged and unpublished as immutable evidence.

Creator Grill on THIS candidate (the CG-2 child):
  unsupported-material-claim finding = 0

Independent review of this closure candidate : NOT YET PERFORMED,
                                               as at the time of its submission
```

The rejected SHA was never amended, rebased, squashed or recreated. CG-2 is repaired by stating each
figure's provenance separately, saying explicitly that the baseline was NOT measured on `18a90f9b…`, and
giving the carry-over argument (PR #554 was governance-only, `TEST DELTA: 0`) rather than leaving it
implicit. The arithmetic was correct throughout; the claim about where it came from was not.

---

**Superseded (retained as history) — PVCG-R4-I: bounded FPC-02 / P4-2 IMPLEMENTATION; MERGED AND
AUTHORITATIVE via PR #555, merge `5ed09180…`.** Base: `c3d9e2d98ba7b6c9b3a9d9d316e6d572122d8a8e` (PR #554 merge — PVCG-R4-C,
AUTHORITATIVE; live tip re-fetched and independently re-verified on all four merge criteria before any
edit: first parent `18a90f9b0aa85d05317bed5aaa596e19716c6557`, second parent
`d5286de76109e9dd8be52f49d72e59b063e2c823` — the exact Owner-accepted candidate — merge tree
`968ff38cbe689526b8d97a7b9533be631e4ee1a7` identical to the candidate tree, empty candidate→merge diff,
zero later commits, clean tree). **`PVCG-R4-C AUTHORITATIVE: YES`.**

**Disposition: `PVCG-R4-I IMPLEMENTATION CANDIDATE — NOT AUTHORITATIVE UNTIL MERGED`.**
`PVCG-R4 AUTHORITATIVELY SATISFIED: NO` until merged, post-merge verified and formally closed by its
own closure record.

**Ownership enforced structurally.** `IMPLEMENTATION OWNER: FPC-02 / P4-2`;
`PVCG CONFORMANCE OWNER: PVCG-R4`. Every mechanism is an EXISTING canonical model — the Increment-2
supersession primitive, the P4-0 record contract, the P4-1a INSERT-only store, the P4-2 Level-1
reconstruction replay, and the one canonical active-set rule already consumed by five derived modules.
No parallel state model, no second replay engine, no dependency model, no schema change, no migration
(`D-FPC-MAP-02` / `D-FPC-MAP-06` preserved).

**Delivered — exactly seven paths:** `engine/record_contract.py` (`reconcile_supersession_edges`,
deriving the inverse edge on load because the store is INSERT-only; additive, idempotent, and it
REJECTS contradictory or double supersession rather than repairing it), `engine/idea_state.py`
(additive `supersedes=`, fail-closed before any append), `engine/progression_loop.py` (the ONE §10.4
G-1 CLOSED-gap guard), `engine/session_reconstruction.py` (AMENDED-stream replay + additive
`withdrawn_source_records`), `engine/deliverable_assembler.py` (the truthful withdrawn-source marker,
counts and note only, on the existing surface-and-retain idiom), `web/app.py`
(`POST /session/<sid>/correct`), `web/ui_text.py` (`UI_B_CORRECT_001…003`, EN/AR).

**Contract clauses proven.** Explicit record-targeted correction, never inferred (§6 C-1 — a committed
test shows retraction wording alone still withdraws nothing); retention with no destructive mutation and
no `rec_N` reuse (§6 C-2/C-3, §7 S-1/S-2); FULL replay of the amended stream through the unchanged
`run_iteration` (§8 RP-1); atomic live-state replacement with no direct progression mutation (§8 RP-4);
measured decrease (§8 RP-5); replay-failure rollback leaving live memory byte-identical (§9 F-2/F-3);
persistence/reload reproducing the corrected state (§14 P-2/P-3); EN/AR equivalence (§13 E-1);
withdrawn basis absent from the recomposed deliverable (§15 M-1) with an explicit counts-only marker
(§15 M-2/M-3/M-4).

**Pin reconciliation (§16.2 under R3-C §13.2a), exhaustive.** Old `3cbd76849c0f572191a552db1a41a8cd418d02fac1d59d9b8804c72883239a55` → new `c268cd6380129170da19f3ba03158eebd9a5480711b43e39280e8ce9e74f63f8`.
**Kind (1) ENFORCING — all THREE updated together:** `test_p9_mech_i3_signal_quality.py`,
`test_p9_mech_i4_boundary_corpus.py`, `test_p9_mech_i5_question_sufficiency.py`, each with a disclosed
note preserving the prior digest. **Kind (2) ACTIVE CURRENT-TRUTH — synchronized:** the R4-C §16 table
(the precedent by which R3-I synchronized R3-C §13) plus the roadmap entry and the two status surfaces.
**Kind (3) HISTORICAL — left byte-unchanged:** R3-C §13, the R3 formal closure record §4, the R3-I and
R3-closure roadmap gate entries, the retained R3-I blocks here and in `CURRENT_PROJECT_STATE.md`.
**`PACK DELTA: 0`** — `domain_rules.py`, `path_n_questions.py` and all five packs byte-identical; the
correction path is domain-neutral, asserted by test.

**Verification on the frozen candidate — measured, not carried.** Focused R4-I **63 passed**; R1
**26** (file byte-unchanged); R2 **189** + **566** (both byte-unchanged); R3 **579** (byte-unchanged);
P9 **54**; `UNIVERSAL GUARDRAIL SMOKE: PASS`; full suite **4418 passed / 3 skipped / 1 xfailed /
0 failed** under the §18 precondition (Python 3.11.15, Flask 3.1.3, SQLite 3.45.1, gunicorn 26.1.0).
**§20 reconciliation: 4355 baseline + 63 = 4418**, exactly the one new test file — and the baseline was
itself re-measured on this candidate's own base in this session.

**Scope.** `FPC-02 / P4-2 REMAINS IMPLEMENTATION OWNER: YES`; `PVCG-R4 REMAINS CONFORMANCE OWNER ONLY:
YES`; `TARGETED PARTIAL INVALIDATION AUTHORIZED: NO`; `DEPENDENCY GRAPH ADDED: NO`;
`FULL CONTRADICTION ENGINE AUTHORIZED: NO`; `VERSIONING / BRANCHING / ROLLBACK / SHARING ADDED: NO`;
`PERSISTENCE SCHEMA MIGRATION: NO`; `PHASE 4 REOPENED GENERALLY: NO`; `main` not reconciled;
`OWNER_DECISION_REGISTER.md` UNCHANGED. `TDVP STARTED: NO`; `PVCG SATISFIED: NO`;
`FULL MLC DEFINITION FROZEN: NO`; `DEPLOYMENT AUTHORIZED: NO`.

**Verdict provenance, kept distinct.** `UNSUPPORTED MATERIAL CLAIMS` is an INDEPENDENT-REVIEWER field:

```
Independent External Review — candidate 4dc7c3290a8bf9b72a87ad017e1e94181f6b9799
  VERDICT                     = ACCEPT WITH NON-BLOCKING OBSERVATIONS
  UNSUPPORTED MATERIAL CLAIMS = 0
  SAFE FOR OWNER EXACT-SHA ACCEPTANCE = YES
  Observations raised         = NB-1, NB-2, NB-3, NB-4
  Owner disposition           = acceptance WITHHELD pending a bounded child
                                repairing NB-1 and NB-2 ONLY

Ultra-focused Independent Review — candidate fc45d029926d7842bbea5440339c4bac9625613a
  VERDICT                     = ACCEPT WITH NON-BLOCKING OBSERVATIONS
  UNSUPPORTED MATERIAL CLAIMS = 0
  SAFE FOR OWNER EXACT-SHA ACCEPTANCE = YES
  Owner disposition           = acceptance WITHHELD pending a final microgate
                                on the next-load promise + user reachability

THIS candidate — the final truthfulness / reachability microchild of fc45d029…
  NB-1 = REPAIRED (NB-1/NB-2 stage)   NB-2 = REPAIRED (NB-1/NB-2 stage)
  NB-3 = NOT ADDRESSED   NB-4 = NOT ADDRESSED (out of the authorized scope)
  false next-load promise     = REPAIRED, wording only
  replay bound                = NOT repaired (pre-existing; unassigned)
  USER-REACHABILITY           = CLASSIFICATION A (route/API sufficient; no UI added)
  Creator Grill unsupported-material-claim finding = 0
  INDEPENDENTLY RE-REVIEWED   = NO, as at the time of its submission
```

`4dc7c329…` is preserved unchanged and unpublished as immutable review evidence (branch
`pvcg-r4i-reviewed-4dc7c329`); it was never amended, rebased, squashed or recreated.

---

**Superseded (retained as history) — PVCG-R4-C: USER CORRECTION AND DETERMINISTIC INVALIDATION —
CONFORMANCE CONTRACT; MERGED AND AUTHORITATIVE via PR #554, merge `c3d9e2d9…`.** Base: `18a90f9b0aa85d05317bed5aaa596e19716c6557` — the live
authoritative tip of `origin/feature/atomic-json-session-persistence`, independently re-fetched and
re-verified on all four merge criteria before drafting (PR #553; first parent
`d046b3e5449f5f91f5f719686e7e207ceda2f06c`; second parent `0fa8fbd83ee2b3a8de165eaaa1a9fd0d4e64c290` —
the exact Owner-accepted R3 closure candidate; merge tree `5101c167c91a87184e701e3236f1aa62be8be376`
identical to the candidate tree; candidate→merge diff EMPTY; zero later commits; clean tree).
**`PVCG-R3 FORMALLY CLOSED: YES`.**

**Disposition: `PVCG-R4-C CONTRACT CANDIDATE — NOT AUTHORITATIVE UNTIL MERGED`.** Governance-only; it
authorizes no code. Even on merge it authorizes **no implementation** — PVCG-R4-I requires its own
separate explicit Owner execution authorization, as R2-I and R3-I did. The contract lives at
`docs/governance/PVCG_R4_C_USER_CORRECTION_AND_DETERMINISTIC_INVALIDATION_CONTRACT.md`.

**PVCG-R4 is a CONFORMANCE GATE, not a capability owner (OD-R4-01 / OD-R4-02).**
`IMPLEMENTATION OWNER: FPC-02 / P4-2` (with D17 / D-AISR-06 / D-P4-05); `PVCG CONFORMANCE OWNER:
PVCG-R4`. No parallel state model, record type, persistence schema, replay engine or dependency model is
created — preserving `D-FPC-MAP-02` and `D-FPC-MAP-06` (*"DO NOT CREATE A NEW PARALLEL MODEL — EXTEND OR
CONSUME THE EXISTING CANONICAL MODEL"*).

**Frozen defect (§3).** A user who discovers previously supplied accepted material was wrong cannot
withdraw it; corrective/retraction language does not invalidate the earlier authoritative progression
state; conclusions therefore stay current although their basis was withdrawn. Demonstrated through the
runtime path: three Stage-2 gaps CLOSED at maturity 2 / stage 3, then four retraction iterations change
nothing, and the withdrawn mechanism appears in **four** deliverable locations including the prototype &
test plan. Mitigations credited: `deliverable_eligible=False`, `derived_verified_ready=False`, unknowns
surfaced — a truthfulness-of-basis defect, not a false-readiness defect.

**Required semantics.** Explicit record-targeted correction (never inferred from wording);
non-destructive supersession with retention, expressed as a forward `supersedes` edge because the durable
store has **no `UPDATE` statement at all**, inverse derived on load; **full deterministic replay** of the
amended accepted-source stream through the unchanged `run_iteration`; live-state replacement only via
replay; readiness/maturity/evaluation **permitted to decrease** with at least one measured decrease
required; atomic deterministic failure/rollback; truthful withdrawal marker on the established
surface-and-retain idiom; **no schema migration** (`contradicts`/`supersedes`/`superseded_by` already in
`_ASSERTION_FIELDS`, already serialized and already validated on load).

**Prohibited, not merely unscoped.** Targeted/partial/selective re-evaluation (`D-AISR-06`; Phase-4 entry
decision §12; OD-R4-03); any dependency graph; a full contradiction engine (OD-R4-04); destructive
history mutation; reopening ordinary CLOSED gaps through the forward path (OD-R4-07). **"Bounded" is
defined as bounded SCOPE and bounded AUTHORIZATION — never targeted partial recomputation.**

**CLOSED-gap precondition (§10).** `integrate_response` called on an already-CLOSED gap yields
`status=PARTIAL` with `closed_at` still set. **Not a live defect** — its sole runtime caller is inside
`run_iteration`, whose `gap_type` comes from `select_next_gap`, which returns only OPEN/PARTIAL. The
contract requires it be made unreachable by construction before any reprocessing, preserving WPS-001
INV-004, and mandates non-vacuous INV-004 coverage because the only dedicated test skips on its own
corpus.

**R1/R2/R3 protection (OD-R4-10)** is specified clause by clause in §§11–13, including EN/AR correction
equivalence — measured at this base, EN and AR corrections produced identical transitions and identical
resulting state.

**Phase 4 (OD-R4-08).** Remains FORMALLY CLOSED within its implemented boundary and is **NOT reopened
generally**; the Owner authorized only a narrowly bounded post-closure P4-2 extension limited to the R4
conformance obligation.

**Creator evidence provenance.** **No test suite was executed for this candidate and no suite figure is
claimed.** The drafting container has Python 3.11.15 but neither `pytest` nor `flask`, so the §18-class
precondition is not satisfied here — a Creator-environment limitation, recorded rather than worked
around. All `[EXEC]` findings are read-only `engine/` probes the reviewer should re-measure. R4-I must
measure independently on its own frozen state.

**Scope.** Governance/documentation ONLY. `RUNTIME DELTA: 0`, `TEST DELTA: 0`, `PACK DELTA: 0`,
`PIN DELTA: 0`; no `engine/`, `web/`, `tests/`, `domains/`, `scripts/`, evidence-tree, generator,
deployment or Render path; `main` not reconciled; `OWNER_DECISION_REGISTER.md` UNCHANGED.
`PVCG-R4 IMPLEMENTATION STARTED: NO`; `FPC-02 / P4-2 REMAINS IMPLEMENTATION OWNER: YES`;
`TARGETED PARTIAL INVALIDATION AUTHORIZED: NO`; `FULL CONTRADICTION ENGINE AUTHORIZED: NO`;
`TDVP STARTED: NO`; `PVCG SATISFIED: NO`; `FULL MLC DEFINITION FROZEN: NO`;
`MINIMUM LAUNCH-CONFORMANCE SET SATISFIED: NO`; `DEPLOYMENT AUTHORIZED: NO`.

**Verdict provenance, kept distinct.** `UNSUPPORTED MATERIAL CLAIMS` is an INDEPENDENT-REVIEWER field and
is not a verdict the Creator may self-award:

```
Creator Grill on first frozen candidate c19ecd72c3d040125a008131a5af18314074a0fe:
  VERDICT  = REJECTED BY CREATOR GRILL
  Defects  = CG-1 (quote mis-attributed to engine/record_store.py),
             CG-2 (WPS-001 INV-004 citation truncated, hiding the clause governing decrease),
             CG-3 ("record-targeted" undisambiguated from prohibited "targeted" recomputation)
  SHA preserved unchanged and unpublished as immutable evidence.

Creator Grill on THIS candidate (the CG-1/CG-2/CG-3 child):
  unsupported-material-claim finding = 0

Independent review of this candidate : NOT YET PERFORMED,
                                       as at the time of its submission
```

The rejected SHA was never amended, rebased, squashed or recreated. CG-1 is repaired by quoting the two
runtime headers separately; CG-2 by quoting WPS-001 INV-004 in full and adding **§8.1**, which resolves
the apparent conflict with the decrease requirement (replay builds a FRESH state forward and replaces the
prior state wholesale, so a weaker outcome is a property of the NEW run, never a backward transition;
lowering a stored status in place is a rejection condition); CG-3 by adding **§2.4.2**, which separates
"record-targeted correction" (REQUIRED — which input is withdrawn) from "targeted re-evaluation"
(PROHIBITED — how much is recomputed) and states that a record-targeted correction is ALWAYS followed by
a full replay of the entire amended stream.

---

**Superseded (retained as history) — PVCG-R3: AUTHORITATIVE CLOSURE; governance-only closure gate;
MERGED AND AUTHORITATIVE via PR #553, merge `18a90f9b…`.** Base:
`d046b3e5449f5f91f5f719686e7e207ceda2f06c` (PR #552 merge — PVCG-R3-I, AUTHORITATIVE; live tip
re-fetched from `origin/feature/atomic-json-session-persistence` and independently re-verified: first
parent `7b7aa2f12a7429fbb309c2f4a7e13d7b83ebdd60`, second parent
`4978c969357200721199c811fede2d40d59e95ac` — the exact Owner-accepted candidate — merge tree
`db87b7cbdc5c681d10e8e905b5d81a9f2c29cd7c` identical to the candidate tree, empty candidate→merge diff,
zero later commits, working tree clean).

**Disposition: `PVCG-R3 CLOSURE CANDIDATE — NOT AUTHORITATIVE UNTIL MERGED`.**
`PVCG-R3-C AUTHORITATIVE: YES` (PR #551). `PVCG-R3-I AUTHORITATIVE: YES` (PR #552). The closure
statements live in `docs/governance/PVCG_R3_FORMAL_CLOSURE_RECORD.md` and take effect only on merge and
post-merge verification.

**Why this gate exists, cited.** `PVCG_R3_C_SEMANTIC_STABILITY_CONTRACT.md` §19 requires as criterion
**10** *"a formal closure record merged, exactly as R2 required"*, so the implementation merge alone does
not close R3. Supersession check: no competing closure rule exists in committed governance, and no
`PVCG_R3_FORMAL_CLOSURE_RECORD.md` previously existed.

**All ten §19 criteria resolved; 1–9 re-measured on the merged tree.** §7.3 **313 registered-surface
anchor comparisons / 0 material mismatches** — each remaining surface of a concept compared against a
common anchor, Σ(n−1) = 313 executed over 56 concepts and 369 surfaces, with §7.3's every-pair property
following transitively; the 1,174 exhaustive pairs were NOT executed; D-1 **0/6**. §10.2 categories 1–11
and the §16 controls are exercised by `TestAdversarialCategories`, `TestNegativeControls` and
`TestCausalTokenBoundary` in the 579-test R3-I suite. **All eight §10.1 properties carry a named
locator** — the complete map is closure record **§4.1**; earlier statements named only four. Inside the
R3-I suite: cross-gap protection by `TestAdversarialCategories::test_8_cross_gap_reuse_creates_no_off_diagonal_closure`
with `TestNegativeControls::test_8`, fail-closed by `TestNegativeControls::test_2`–`::test_6`, and
determinism by `TestDeterminismAndProhibitions`. In other authoritative suites: gap-specific relevance by
the 6×6 closure control, **repetition protection** by
`TestRed3RepetitionCannotManufactureSatisfaction::test_five_repetitions_of_an_irrelevant_answer_never_close`
and **non-punitive rejection** by `TestFailClosedIsNotPunitive::test_irrelevant_answer_never_returns_block`
— all three in `tests/test_pvcg_r2i_gap_relevance.py` — plus R1 durable memory by the R1 suite and the
P9-MECH pins by the three P9 suites. **Criterion 4 status unchanged: MET**; the two newly cited
properties were already green and only the citation was missing. Pin `3cbd7684…` enforced green by the three P9 suites with `domain_rules.py`,
`path_n_questions.py` and all five packs byte-identical; R1 **26** (file byte-unchanged); R2 **189** +
**566** (file byte-unchanged); P9 **54**; smoke **PASS**; full suite **4355 passed / 3 skipped /
1 xfailed / 0 failed**, §18 reconciliation 3776 **+579**. The mutation sweep **257 / 254 KILLED /
0 SURVIVED / 3 LOADFAIL, restore 257/257** is recorded as **carried, independently reviewer-reproduced**
evidence from `0f1404f0…`, not re-measured this gate — the merge tree equals the accepted candidate tree
and the registry and frozen oracle are byte-identical across that lineage.

**Defect dispositions (PVCG-R3-I implementation lineage): B-1 CLOSED, B-2 CLOSED, U-1 CLOSED, U-2
CLOSED, R3-I-O1 CLOSED.** Rejected candidate `1ce9ef34…` and every superseded SHA preserved unchanged
and unpublished.

**Closure-gate dispositions (this gate): CLOSURE-O1 CLOSED, CLOSURE-O2 CLOSED, CLOSURE-O3 CLOSED;
N-P1 CLOSED, N-P2 CLOSED, N-P3 CLOSED; N-P4 NO REPAIR OWED.**

**Label namespace — disambiguated, no merged history rewritten.** Two review rounds each numbered from
`O-1`, in different namespaces. The implementation-lineage observation is written **R3-I-O1**; the
closure-gate observations are written **CLOSURE-O1 / CLOSURE-O2 / CLOSURE-O3**. The merged PVCG-R3-I
entries retained below keep the original `O-1` label **verbatim** — merged history is authoritative for
what it says and was not renamed. Full mapping: closure record §3.1.

**Residuals carried forward, OPEN / NON-BLOCKING, and NOT R4 authorization:** **N-2** (the 40-character
acknowledged-unknown threshold — pre-existing, byte-unchanged, fail-closed in direction, outside the
§7.3 quantifier) and **U-4** (a single Arabic connective in English prose granting causal structure —
by design under §10.2/9). Neither appears in any §19 criterion.

**Scope.** Governance/documentation ONLY. No `engine/`, `web/`, `tests/`, `domains/`, `scripts/`,
evidence-tree, generator, deployment or Render path; `PIN DELTA: 0`; `main` not reconciled;
`OWNER_DECISION_REGISTER.md` UNCHANGED. R3 closure closes ONLY R3: `PVCG-R4 NOT STARTED`,
`FULL ADAPTIVE QUESTIONING ACTIVATED: NO`, `TDVP IMPLEMENTATION STARTED: NO`, `PVCG SATISFIED: NO`,
`MINIMUM LAUNCH-CONFORMANCE SET SATISFIED: NO`, `DEPLOYMENT AUTHORIZED: NO`.

**Verdict provenance, kept distinct.** `UNSUPPORTED MATERIAL CLAIMS` is an INDEPENDENT-REVIEWER field and
is not a verdict the Creator may self-award. Stated separately:

```
Creator Grill unsupported-material-claim finding (this candidate)  : 0

Independent closure review — candidate a477ead76d5d57c61da2f15eb1ff1eadfbd8da5e
  VERDICT                     = ACCEPT WITH NON-BLOCKING OBSERVATIONS
  UNSUPPORTED MATERIAL CLAIMS = 0
  Observations raised         = CLOSURE-O1, CLOSURE-O2, CLOSURE-O3

Independent closure RE-REVIEW — candidate ebd94ab0ebaba224b93aea4e16b9e72ea89d52bc
  VERDICT                     = ACCEPT WITH NON-BLOCKING OBSERVATIONS
  UNSUPPORTED MATERIAL CLAIMS = 0
  CLOSURE-O1 = PASS   CLOSURE-O2 = PASS   CLOSURE-O3 = PASS
  Findings raised             = N-P1, N-P2, N-P3, N-P4

THIS candidate — N-P1 / N-P2 / N-P3 micro-precision child of ebd94ab0…
  INDEPENDENTLY REVIEWED      = NO, as at the time of its submission
```

Each count is attributed to the exact SHA it was issued against, so the statement does not go stale as
the lineage grows — the defect recorded as **N-P3**. `a477ead7…` carried the CLOSURE-O1 (criterion-4
locator), CLOSURE-O2 (anchor-comparison wording) and CLOSURE-O3 (provenance separation) observations;
its child **`ebd94ab0…` WAS itself independently re-reviewed**, returning ACCEPT WITH NON-BLOCKING
OBSERVATIONS with all three confirmed PASS and four further findings N-P1…N-P4. **This candidate carries
only the N-P1/N-P2/N-P3 governance-prose repairs and has NOT itself received a focused re-review; it
must not be cited as reviewed.**

**N-P4 — reviewer-environment limitation, not a defect.** The reviewer could not re-execute the
application suites because **Flask was unavailable in the reviewer's environment**. Not a product
defect, not a closure defect, not a §19 criterion failure. R3-C §18 declares the execution precondition
(Python 3.11.15, Flask 3.1.3, SQLite 3.45.1, gunicorn 26.1.0 on `PATH`) and every recorded suite result
was measured in an environment satisfying it. **No repair is made and none is owed.**

**This micro-precision repair is governance prose only:** `RUNTIME DELTA: 0`, `TEST DELTA: 0`,
`PACK DELTA: 0`, `PIN DELTA: 0`; no `engine/`, `web/`, `tests/`, `domains/` or `scripts/` file changed,
so the previously established suite evidence carries forward unchanged and is **not** re-run or
re-claimed.

---

**Superseded (retained as history) — PVCG-R3-I (REPAIR): focused repair after Independent External
Review REJECT; MERGED AND AUTHORITATIVE via PR #552, merge `d046b3e5…`.**
Base: `7b7aa2f12a7429fbb309c2f4a7e13d7b83ebdd60` (PR #551 merge — PVCG-R3-C, AUTHORITATIVE;
re-resolved live and independently re-verified on all four merge criteria before any repair work).

**Disposition: `PVCG-R3-I REPAIR CANDIDATE — NOT AUTHORITATIVE UNTIL MERGED`.**
**Rejected predecessor `1ce9ef340c7cb908da37ae8b4b304b1ee9ae30bc` is preserved UNCHANGED as immutable
review evidence** (never amended, rebased, squashed or published), together with its Creator-Grill
parent `52a25182…`. **The rejected candidate's `UNSUPPORTED MATERIAL CLAIMS: 0` is WITHDRAWN.**

**B-1 repaired — Arabic causal substring bleed.** Causal surfaces matched by raw substring, so the
2-character `ثم` fired from inside `ثمن` (price), `عثمان`, `ثمانية`, `استثمار` — 19/19 measured false
positives — and an Arabic answer whose only qualifying token was the noun `ثمن` reached `REASONED` and
CLOSED a gap while the synonym `سعر` and the faithful English counterpart stayed `ASSERTED`/`PARTIAL`.
Each causal surface now declares an explicit `match_mode` and goes through the same `_surface_matches`
discipline as concept surfaces (36 WORD / 6 PHRASE), with the definite-article proclitics excluded for
causal surfaces only. After repair: **0/19 false positives, 10/10 legitimate causal usage preserved, and
the `ثمن` / `سعر` / English outcomes identical.** **U-2 correction:** a comment claimed `وثم` still
matches; it does NOT — `ثم` is 2 characters, below `_MIN_PROCLITIC_SURFACE_LEN = 3`, so it is reached
only as a bare token. The runtime is therefore MORE conservative than the comment described; the
comment is corrected to the code's actual behaviour, the guard is unchanged, and the proclitic boundary
is now pinned by isolated assertions (`وحين`/`فتدور`/`وتدور` match; `وثم`/`فثم` do not). The validator now refuses at import any single-token
causal or unknown surface declared PHRASE.

**B-2 repaired — circular mutation evidence.** Probes were parametrized over `DECLARED_INVENTORY`
(derived from `CONCEPTS`), so deleting a surface deleted its own test: focused 453→451 and full
4229→4227, both with ZERO failures. **The `163/163 KILLED` result is WITHDRAWN.** Coverage adequacy now
runs off `tests/fixtures/pvcg_r3i_frozen_expectations.py` — **257 rows of literal committed data**
importing nothing from the object under test (AST-verified), with a both-directions parity test.
Deleting one entry from each of the four classes now turns the suite RED.

**Corrected sweep:** **257 processed / 254 KILLED / 0 SURVIVED / 3 LOADFAIL**, restore **257/257**
byte-identical, 0 anchor misses. The **3** LOADFAILs are exactly `MC-LATCH: مزلاج`, `PF-ENERGY: طاقة`
and `PF-FREQUENCY: تردد` — the three concepts whose ONLY Arabic surface was removed, where the
registry's own `RegistryError` refuses the mutant (fail-closed by design) — reported as LOADFAIL,
**not** counted as kills. **The earlier `252 / 5` split is WITHDRAWN as a HARNESS defect** (the
substance remover hit the first file-wide occurrence of a surface that also exists in the concept
table, mutating the wrong table); `battery` and `frequency` are genuinely KILLED. `0 SURVIVED` and the
`257/257` restore are unchanged and were reproduced independently by the reviewer and the Creator.

**Structural shadowing — prior "0 shadowed" was WRONG.** Two genuine shadows found (`مما يسبب` behind
the WORD surface `يسبب`; `لست متاكدا` behind the prefix `لست متاكد`) and REMOVED, with the removals
recorded. Causal is now **42** and acknowledged-unknown **8**. The re-audited zero is earned.

**N-1 corrected:** **38 pack SIGNALS carrying 44 Arabic SURFACES** (the earlier "38 substance surfaces"
was wrong). **N-3 corrected:** the negative control no longer skips the case it names. **N-2 recorded as
OPEN / NON-BLOCKING:** the 40-character acknowledged-unknown threshold is language-neutral in rule but
not in effect (EN 43 detected / AR 27 not); pre-existing, byte-unchanged, fail-closed in direction, not
redesigned here. **N-5 classified:** R3-C §2.5's "English-only" wording is overstated (`localize_deep`
did localize the base fallback); an observation about the authoritative contract, not an R3-I defect —
R3-C history is NOT rewritten.

**Preserved gains.** D-1 **0/6**; D-2 trajectories identical; D-3 unknown recorded and never
satisfaction; D-4 specific and genuinely localized; English not widened by one token.
`engine/progression_loop.py` **byte-unchanged by this repair** (`3cbd7684…`), so no pin moved again.

**Verification on the frozen repair candidate.** Focused R3-I **579 passed**; R1 **26/26** byte-unchanged;
R2 **189** + **566** byte-unchanged; P9 **54**; smoke **PASS**; full suite **4355 passed / 3 skipped /
1 xfailed / 0 failed**; §18 reconciliation 3776 **+579**, exactly the R3-I test file.

**Scope.** `PVCG-R3 AUTHORITATIVELY SATISFIED: NO`; `PVCG-R4 IMPLEMENTATION STARTED: NO`;
`FULL ADAPTIVE QUESTIONING ACTIVATED: NO`; `TDVP IMPLEMENTATION STARTED: NO`; `LLM/EMBEDDINGS/VECTOR
STORE/EXTERNAL NLP/PROBABILISTIC CLASSIFIER ADDED: NO`; no pack edit, no domain change, no new gap type;
`main` not reconciled; `OWNER_DECISION_REGISTER.md` UNCHANGED. `PVCG SATISFIED: NO`;
`MINIMUM LAUNCH-CONFORMANCE SET SATISFIED: NO`; `DEPLOYMENT AUTHORIZED: NO`.
`UNSUPPORTED MATERIAL CLAIMS: 0`.

---

**Superseded (retained as history) — PVCG-R3-I: SEMANTIC STABILITY IMPLEMENTATION; REJECTED by
Independent External Review as `1ce9ef34…` on defects B-1 and B-2; preserved unchanged as immutable
review evidence. Its claims below are HISTORICAL and several were false — see the repair entry above.**
Base: `7b7aa2f12a7429fbb309c2f4a7e13d7b83ebdd60` (PR #551 merge — PVCG-R3-C, AUTHORITATIVE; live tip
re-fetched from `origin/feature/atomic-json-session-persistence` and independently re-verified on all
four merge criteria: first parent `ca98099e29f6729c29e7612d67f9187dbd0dccb6`, second parent
`6bdf2669ef0826d2f06e2a54722954e3d49958c1`, merge tree
`c707281acccf1751a0d48bb65fa917879f2c5909`, empty candidate→merge diff; zero commits after the tip;
working tree clean).

**Disposition: `PVCG-R3-I IMPLEMENTED / CANDIDATE — NOT AUTHORITATIVE UNTIL MERGED`.**
`PVCG-R3-C AUTHORITATIVE: YES` (PR #551). This candidate implements ONLY the bounded R3 capability the
authoritative contract defines; it closes **R3 only**. `PVCG-R3 AUTHORITATIVELY SATISFIED: NO` until
merged, post-merge verified and formally closed by its own closure record.

**Delivered.** One new unpinned module `engine/semantic_registry.py` — the governed bilingual concept
registry: **56 concepts / 163 declared Arabic surfaces**, each concept carrying all five §5.1 fields
(stable `concept_id`, exactly ONE owning gap, governed-question provenance, EN + AR surface sets, a
declared `match_mode` per surface); plus the two required structural classes — **43** Arabic
causal-structure surfaces mirroring the English `_CAUSAL_STRUCTURE_PATTERNS` role and **38** Arabic
substance surfaces (15 mechanical + 23 electronics) one-to-one with ALREADY-COMMITTED pack signals, with
the **30** signals deliberately given no Arabic surface recorded and justified — and **9** Arabic
acknowledged-unknown surfaces mirroring the English markers one-for-one. Four seams consult it:
`gap_relevance.addresses_gap` (D-1), `progression_loop._has_causal_structure` and the substance check
(D-2), `progression_loop._detect_acknowledged_unknown` (D-3), and `web/result_feedback.py` +
`web/ui_text.py` for the §8.1 truthful, both-language not-addressed disclosure (D-4).

**Boundaries held as facts of the delivered code.** `LLM ADDED: NO`; `EMBEDDINGS ADDED: NO`;
`VECTOR STORE ADDED: NO`; `EXTERNAL NLP SERVICE ADDED: NO`;
`PROBABILISTIC SEMANTIC CLASSIFIER ADDED: NO`; `MODEL-BASED ADJUDICATION ADDED: NO`. No network, clock,
randomness, filesystem access at decision time, stemming, lemmatization, fuzzy matching, edit distance
or transliteration. The registry depends only on stdlib `re` and `unicodedata`. **English is not
widened by one token** — every registered English surface is machine-checked to be an existing intent
marker of the SAME gap family. Normalization is exactly the authorized set (NFC, tatweel, harakat,
alef-variant folding), each demonstrated necessary by execution; **teh marbuta, yeh/alef-maqsura and
Arabic-Indic digits are NOT folded**, and hamza-carrier letter identity is preserved and pinned by test.

**Pin reconciliation (§13.2/§13.2a) — the one authorized engine pin moved.** Old
`07c9bff500662de54ac0f7388c1f2e13a721549c6f4943cde865b98a22c525d6` → new
`3cbd76849c0f572191a552db1a41a8cd418d02fac1d59d9b8804c72883239a55`. All THREE ENFORCING locations
updated together (`test_p9_mech_i3_signal_quality.py`, `test_p9_mech_i4_boundary_corpus.py`,
`test_p9_mech_i5_question_sufficiency.py`), each with a disclosed reconciliation note preserving the
prior digest as historical evidence; all ACTIVE CURRENT-TRUTH governance references synchronized in this
same candidate; all HISTORICAL append-only occurrences deliberately left byte-unchanged.
`engine/domain_rules.py` (`0e47326a…`), `engine/path_n_questions.py` (`a1a682d3…`) and all five pack
digests are byte-identical. RED was established at the authoritative base BEFORE any pin was touched.

**Evidence, measured on the frozen candidate.** RED at the base: D-1 **6/6** gaps materially diverge;
D-2 Arabic `OPEN` for eight iterations while the English control `CLOSED` at iteration 2; D-3 the Arabic
unknown undetected; D-4 the not-addressed reason falling to the unknown-reason fallback, English-only.
GREEN: **0/6** divergence, Arabic and English closure trajectories identical, the Arabic unknown
recorded with a truthful basis, the disclosure specific and localized. Complete single-entry mutation
sweep over every declared Arabic surface: **163 processed / 163 KILLED / 0 SURVIVED / 0 LOADFAIL**,
restore **163/163** byte-identical. Focused R3-I **453 passed**; PVCG-R1 **26/26** with its test file
**byte-unchanged**; R2 behavioural **189 passed**; R2 marker coverage **566 passed**; P9 pin suites
**54 passed**; `UNIVERSAL GUARDRAIL SMOKE: PASS`; full suite **4229 passed / 3 skipped / 1 xfailed /
0 failed** under the §18 precondition (Python 3.11.15, Flask 3.1.3, SQLite 3.45.1, gunicorn on `PATH`).
Reconciliation against the 3776 baseline: **+453**, exactly the new R3-I test file, no other delta.

**One R2 test file changed, disclosed rather than hidden (§12).**
`tests/test_pvcg_r2i_gap_relevance.py::TestDeclaredLexicalBounds::
test_non_english_paraphrase_is_not_recognised_r3_bound` asserted the R2 KNOWN BOUND that an Arabic
mechanism answer is NOT recognised — the bound R3-C §1.3/§4 exists to close, and whose own docstring
named it "PVCG-R3 territory". It is updated to current truth and still asserts the residual:
unregistered Arabic remains fail-closed. `tests/test_pvcg_r2i_marker_coverage.py` is
**byte-unchanged**.

**Creator-Grill findings, disclosed.** (a) `أعتقد`/`أتوقع` make ordinary Arabic prose eligible for
`ASSUMPTION_INVENTORY` — the English `believe`/`expect` markers behave identically at the base, so this
is PRE-EXISTING English breadth (§14 residual 1) mirrored faithfully; narrowing Arabic would create a
new divergence. Pinned by test. (b) The first RED probe hard-coded the repo path and mis-measured the
base tree; corrected, and RED re-verified at `7b7aa2f1…` with the registry file confirmed absent from
that tree.

**Residual, stated as a known bound and not concealed.** The §7.3 guarantee holds ONLY over the
published registered-class inventory. Unregistered wording in either language is not governed-equivalent
and gains nothing. R3 is a registered bilingual concept mapping, not language understanding, not
paraphrase stabilisation, and not a third language.

**Scope.** `PVCG-R3 AUTHORITATIVELY SATISFIED: NO`; `PVCG-R4 IMPLEMENTATION STARTED: NO`;
`FULL ADAPTIVE QUESTIONING ACTIVATED: NO`; `TDVP IMPLEMENTATION STARTED: NO`; no domain activated,
recognised differently or re-scoped; no pack edited; no new gap type; no next-question-selection change;
no `stage3_evaluator` or WS10/WS11/WS12 integration; `main` not reconciled; Render not reopened;
`OWNER_DECISION_REGISTER.md` UNCHANGED. `PVCG SATISFIED: NO`;
`MINIMUM LAUNCH-CONFORMANCE SET SATISFIED: NO`; `DEPLOYMENT AUTHORIZED: NO`.
`UNSUPPORTED MATERIAL CLAIMS: 0`.

---

**Superseded (retained as history) — PVCG-R3-C: SEMANTIC STABILITY CONTRACT / DIAGNOSIS GATE; governance-only; MERGED AND AUTHORITATIVE via PR #551, merge `7b7aa2f1…`.** Base:
`ca98099e29f6729c29e7612d67f9187dbd0dccb6` (PR #550 merge — PVCG-R2 formal closure; live tip re-fetched
from `origin/feature/atomic-json-session-persistence` and independently re-verified on all four merge
criteria: first parent `1ce2c89630b9bdbfdedb15ee85eafa410a03632a`, second parent
`25cf419c3b21201fc6403d4a53301281af7a2071`, merge tree `9bd7a1169072598b3804e16ee3bc04dea4faa313`,
empty candidate→merge diff; zero commits after the tip; working tree clean).

**Disposition: `PVCG-R3-C CONTRACT CANDIDATE — NOT AUTHORITATIVE UNTIL MERGED`.**
`PVCG-R2 AUTHORITATIVELY CLOSED: YES` (PR #550). The R3 contract lives at
`docs/governance/PVCG_R3_C_SEMANTIC_STABILITY_CONTRACT.md` and authorizes nothing until it is merged
and post-merge verified; `PVCG-R3-I` additionally requires a separate explicit Owner execution
authorization.

**Defect proven before the contract was written** (Creator-local executed evidence at the base tree;
R3-I must re-measure independently): **D-1** eligibility diverges in **6 of 6** governed gaps between
materially equivalent EN/AR answers from an identical starting state (served gap stays `OPEN` instead
of `PARTIAL`); **D-2**, the decisive finding, every causal-structure pattern and every mechanical and
electronics substance signal is ASCII, so `assess_response` returns `ASSERTED` unconditionally for pure
Arabic and — because a gap closes only on `REASONED`/`DEMONSTRATED` and `DEMONSTRATED` is unreachable in
the MVP — **an Arabic-only inventor can never close a gap** (eight iterations `OPEN`, English control
`CLOSED` at iteration 2); **D-3** the ASCII-only acknowledged-unknown markers mean an Arabic-stated
unknown is never recorded, a hidden side-effect divergence; **D-4** the R2 "not addressed" reason falls
to the conservative unknown-reason `result_feedback` fallback and is English-only, so the divergence is
not even disclosed. Recorded negative diagnosis: EN normalization is already stable (8/8) and R3 adds
none; AR-internal normalization is not a divergence source today (7/7) and becomes material only once an
Arabic surface is registered; unregistered EN paraphrase remaining ineligible is expected lexical
boundedness, not a defect.

**Pin impact.** `engine/gap_relevance.py` is **not byte-pinned anywhere**; `engine/progression_loop.py`
(`07c9bff5…`) is pinned in three P9-MECH suites and cannot be avoided when closing D-2. The contract
permits exactly one engine pin to move, reconciled in all three ENFORCING pin locations in the same
candidate — and synchronized across the active current-truth governance surfaces that record the digest,
per §13.2a, which also bars rewriting append-only historical entries — with RED
first, and requires `engine/domain_rules.py`, `engine/path_n_questions.py` and all five pack digests to
remain byte-identical. **Pin delta in this candidate: 0.**

**Scope.** Governance/documentation ONLY — one new contract plus the roadmap append and the two status
surfaces. No `engine/`, `web/`, `tests/`, `domains/`, `scripts/`, evidence-tree, generator, CI,
deployment or Render path; `main` not reconciled; `OWNER_DECISION_REGISTER.md` UNCHANGED.
`PVCG-R1 AUTHORITATIVE: YES`; `PVCG-R2 AUTHORITATIVELY CLOSED: YES`; `PVCG-R3 IMPLEMENTATION STARTED:
NO`; `PVCG-R4 IMPLEMENTATION STARTED: NO`; `LLM/NLP SUBSYSTEM ADDED: NO`; `RUNTIME MODIFIED: NO`;
`TESTS MODIFIED: NO`; `PVCG SATISFIED: NO`; `MINIMUM LAUNCH-CONFORMANCE SET SATISFIED: NO`;
`DEPLOYMENT AUTHORIZED: NO`. `UNSUPPORTED MATERIAL CLAIMS: 0`.

---

**Superseded (retained as history) — PVCG-R2: AUTHORITATIVE CLOSURE; governance-only closure gate;
MERGED AND AUTHORITATIVE via PR #550, merge `ca98099e…`.** Base:
`1ce2c89630b9bdbfdedb15ee85eafa410a03632a` (PR #549 merge — PVCG-R2-I, AUTHORITATIVE; re-resolved live
from `origin/feature/atomic-json-session-persistence` and independently re-verified: first parent
`4d746d15…`, second parent `60cc5f48…`, merge tree `476629b6…`, empty candidate→merge diff, zero later
commits).

**Disposition: `PVCG-R2 AUTHORITATIVELY CLOSED: YES`** — the closure candidate
`25cf419c3b21201fc6403d4a53301281af7a2071` was Owner-accepted and merged via PR #550, merge
`ca98099e29f6729c29e7612d67f9187dbd0dccb6`, post-merge verified on all four criteria (first parent
`1ce2c896…`, second parent `25cf419c…`, merge tree `9bd7a116…` == candidate tree, empty
candidate→merge diff; authoritative scope 4 governance files / +332 / -1).
`PVCG-R2-C AUTHORITATIVE: YES`. `PVCG-R2-I AUTHORITATIVE: YES`. The closure statements live in
`docs/governance/PVCG_R2_FORMAL_CLOSURE_RECORD.md` §9 and are now in force.

**Scope.** Governance/documentation ONLY. No `engine/`, `web/`, `tests/`, `domains/`, `scripts/`,
evidence-tree, generator, deployment or Render path; `main` not reconciled;
`OWNER_DECISION_REGISTER.md` UNCHANGED. R2 closure closes ONLY R2: `PVCG-R3 NOT STARTED`,
`PVCG-R4 NOT STARTED`, `PVCG SATISFIED: NO`, `MINIMUM LAUNCH-CONFORMANCE SET SATISFIED: NO`,
`DEPLOYMENT AUTHORIZED: NO`. R1 and R2 are cumulative: `PVCG-R1 AUTHORITATIVE: YES`,
`PVCG-R1 REGRESSION: GREEN` (26/26, test file byte-unchanged). Final coverage truth re-measured from
the merged tree: 262 operative / 2 structurally shadowed / 0 non-equivalent surviving single-marker
mutants. `UNSUPPORTED MATERIAL CLAIMS: 0`.

---

**Superseded (retained as history) — PVCG-R2-I (T-1b REPAIR): STRUCTURAL-OPERATIVITY CLASSIFICATION
REPAIR; ACCEPTED as `60cc5f48…` and MERGED AND AUTHORITATIVE via PR #549, merge `1ce2c896…`.** Parent:
`58ef39714630455c9713fb045bc66c3490eb4bf8` — the rejected T-1 repair candidate, preserved unchanged as
immutable reviewed evidence, itself a child of the rejected R2-I candidate
`2f2897ce40c119ea202d6519e59e2d887c3fb7c1`, also preserved unchanged.

**Blocking finding repaired: T-1b.** The prior structural non-operativity proof was unsound for 9 of
11 excluded phrases. Root cause: phrase markers match by **substring**, word markers by **token**, so
phrase → word containment does NOT establish universal behavioural shadowing. Withdrawn, not defended.
All nine were re-measured at the rejected SHA — each flips `addresses_gap` when removed — and are now
OPERATIVE with isolated probes that preserve the phrase substring while dissolving the companion token.
Corrected split, re-measured from repository execution: **262 operative / 2 structurally shadowed**,
the two being genuine PHRASE → PHRASE containments, independently re-verified structurally and by
execution. Coverage-classification and governance-truth repair only — **NOT a runtime defect**.

**Runtime and pins untouched:** `engine/gap_relevance.py` and `engine/progression_loop.py`
byte-identical to the parent; digest still
`07c9bff500662de54ac0f7388c1f2e13a721549c6f4943cde865b98a22c525d6`; all three P9 pin files
byte-identical; `SECOND PIN RECONCILIATION: NO`. Sweep: 264 processed / 264 KILLED / 0 SURVIVED / 0
LOADFAIL / restore 264/264. Prior survivors M8b and M9b remain KILLED. Marker coverage 566; R2-I 189;
R1 26/26 byte-unchanged; P9 pins 54; targeted 1321; smoke PASS; full suite 3776 / 3 / 1 / 0 with
gunicorn on PATH. `UNSUPPORTED MATERIAL CLAIMS: 0`.

---

**Superseded (retained as history) — PVCG-R2-I (T-1 REPAIR): MUTATION-ADEQUACY REPAIR OF THE MARKER
TABLES; frozen as `58ef3971…` and REJECTED on finding T-1b; preserved unchanged.** Parent:
`2f2897ce40c119ea202d6519e59e2d887c3fb7c1` — the rejected R2-I candidate, preserved unchanged as
immutable reviewed evidence (not amended, rebased or squashed). Authoritative R2-C base:
`4d746d15a3025802d0ad601b4501473e06b1140b` (PR #548).

**Disposition: `PVCG-R2-I IMPLEMENTED / CANDIDATE — NOT AUTHORITATIVE UNTIL MERGED`.**
`PVCG-R2-C AUTHORITATIVE: YES`. `PVCG-R2-I AUTHORITATIVE: NO`.

**Defect repaired.** Independent External Review returned `REJECT` on ONE blocking defect class,
**T-1 — mutation adequacy / governance truth**, while confirming the runtime implementation itself
substantively correct. The prior record called two surviving supplementary mutants EQUIVALENT MUTANTS
on 10×6 corpus evidence and inferred family redundancy; **both claims are withdrawn as unsound** — a
finite corpus cannot establish equivalence over the input space. The Creator independently reproduced
the reviewer's finding at the rejected SHA: removing `actuates`/`actuate` flips the live seam from
`PASS`/`CLOSED` to `WARN`/`OPEN`, and removing `not cover` flips `PARTIAL` to `OPEN`, both with the
189-test R2-I suite still fully green.

**Repair (tests + governance truth only).** New `tests/test_pvcg_r2i_marker_coverage.py` pins a
DECLARED MARKER INVENTORY and generates probes from that declaration rather than from the live tables,
so deleting a marker leaves its probe in place to fail. One machine-isolated positive probe per
independently operative entry, a cross-family exclusivity probe for each, collection-time failure if
any probe is not isolated (with a validator self-test), and negative guards against domain vocabulary
or causal connectives ever acting as universal relevance signals. 264 declared entries: 253
independently operative and 11 structurally non-operative — **that split is WITHDRAWN and CORRECTED
(T-1b)**: the universal proof was unsound for the nine PHRASE → WORD cases because phrase markers match
by SUBSTRING while word markers match by TOKEN, so phrase → word containment does not establish
universal shadowing. Re-measured from repository execution the split is **262 operative / 2
structurally shadowed**, the two being genuine PHRASE → PHRASE containments
(`power requirements` → `power requirement`, `physical limits` → `physical limit`). The nine
reclassified phrases now carry isolated positive probes. Coverage-classification and governance-truth
repair only — NOT a runtime defect. Complete single-marker sweep: **264 processed / 264 KILLED / 0 SURVIVED / 0
skipped**, restore byte-identical; an earlier 255/255 pass with 9 harness-skips was discarded as a
stale-bytecode measurement artifact and re-run clean. Both prior survivors are named from retained
Creator-local evidence and are now KILLED.

**Implementation and pin untouched.** `engine/gap_relevance.py` and `engine/progression_loop.py` are
byte-identical to the rejected SHA; the progression-loop digest stays
`07c9bff500662de54ac0f7388c1f2e13a721549c6f4943cde865b98a22c525d6` and the P9-MECH-I3 pin was NOT
reconciled again. No fixture, generator, evidence artifact or `OWNER_DECISION_REGISTER.md` change;
`ASSERTION-TARGET CHANGES: 0` still holds. `UNSUPPORTED MATERIAL CLAIMS: 0`.

---

**Superseded (retained as history) — PVCG-R2-I: GAP-RELEVANCE / MANUFACTURED-SATISFACTION HARDENING
IMPLEMENTATION, frozen as `2f2897ce…` and REJECTED by Independent External Review on defect class T-1
(mutation adequacy / governance truth); preserved unchanged as immutable reviewed evidence and repaired
by the current gate above.**
Owner-authorized IMPLEMENTATION gate under the now-AUTHORITATIVE PVCG-R2-C contract. Base:
`4d746d15a3025802d0ad601b4501473e06b1140b` (PR #548 merge — PVCG-R2-C, AUTHORITATIVE; re-resolved live
from `origin/feature/atomic-json-session-persistence` and independently re-verified: first parent
`c70bad19…`, second parent `e394f962…`, merge tree `b8441675…`, empty candidate→merge diff, zero later
commits).

**Disposition: `PVCG-R2-I IMPLEMENTED / CANDIDATE — NOT AUTHORITATIVE UNTIL MERGED`.**
`PVCG-R2-C AUTHORITATIVE: YES`. PVCG-R3 NOT STARTED; PVCG-R4 NOT STARTED; PVCG SATISFIED: NO; MINIMUM
LAUNCH-CONFORMANCE SET SATISFIED: NO. No release-readiness or deployment claim.

**Governing authority.** `docs/governance/PVCG_R2_C_GAP_RELEVANCE_HARDENING_CONTRACT.md` §4 (product
truth), §2.4/§2.5 (one bounded pin reconciliation), §3.2–§3.7 (defect-dependent fixture correction,
five-part scope test, eleven-field ledger, evidence-tree default freeze, generator classification,
truthful provenance comments), §5 (non-goals), §6 (implementation bounds and progression isolation),
§8 (RED/GREEN shape) and §9 (full-suite reconciliation rule). Nothing beyond it was built.

**Implementation.** One new pure deterministic module `engine/gap_relevance.py` (`re` only; no state,
I/O, clock, randomness, network or model call) exposing `addresses_gap(response, gap_type)` and
`GOVERNED_GAP_TYPES`, plus ONE narrow call at the EXISTING answer→gap seam `integrate_response`. The
mechanism is **LEXICAL and deterministic**, derived from the vocabulary of the six governed questions,
with bare domain vocabulary and bare causal connectives deliberately excluded. It makes **no semantic,
meaning-level or cross-language claim**; the Arabic-paraphrase bound is asserted in the test record.
Fail-closed means *not eligible to satisfy or close* — never BLOCK, contradiction, validation failure
or quality downgrade. Eligibility is not quality.

**Evidence.** RED re-measured at the authoritative base: 123 failed / 66 passed (112 behavioural, 11
module-absent); GREEN 189/189. Pin `a8e1ffdf…` → `07c9bff5…` reconciled in all three pin locations with
disclosed comments preserving the prior digest; the byte-freeze guard is unchanged and green.
Twelve test files corrected under the five-part scope test with `ASSERTION-TARGET CHANGES: 0`; the
eleven-field ledger is recorded in `ACTIVE_EXECUTION_ROADMAP.md`. Committed WS1–WS7 evidence trees
REMAIN FROZEN (zero regenerated); all seven generator/harness scripts classified HISTORICAL-ONLY /
FROZEN and none modified. Smoke PASS; targeted 19-file suite 755 passed; PVCG-R1 26/26 with its test
file byte-unchanged; full suite 3210 passed / 3 skipped / 1 xfailed / 0 failed with gunicorn 26.1.0 on
PATH; 12 mandatory behavioural mutations KILLED / 0 SURVIVED. The two supplementary probes that
survived were recorded as EQUIVALENT MUTANTS on corpus evidence; **that claim is WITHDRAWN as
unsound** (a finite corpus cannot establish equivalence) — see the PVCG-R2-I (T-1 repair) status
block above for the corrected mutation truth.
`OWNER_DECISION_REGISTER.md` UNCHANGED. `UNSUPPORTED MATERIAL CLAIMS: 0`.

---

**Superseded (retained as history) — PVCG-R2-C: GAP-RELEVANCE HARDENING CONTRACT / RECONCILIATION GATE;
MERGED AND AUTHORITATIVE via PR #548, merge `4d746d15a3025802d0ad601b4501473e06b1140b`.**
Owner-authorized GOVERNANCE-ONLY gate under the Owner's Option-B decision on the PVCG-R2 dependency
conflict. Base: `c70bad196de73fc27c21a3e1bd8438f1eab41958` (PR #547 merge — PVCG-R1, AUTHORITATIVE;
re-resolved live and independently re-verified: first parent `9d2b6515…`, second parent `5d563203…`,
merge tree `24b57a2f…`, empty candidate→merge diff).

**Historical disposition as recorded at the time (superseded — this contract is now AUTHORITATIVE and
PVCG-R2-I is the current gate): `PVCG-R2-C GOVERNANCE CANDIDATE — NOT AUTHORITATIVE UNTIL MERGED`.**
**PVCG-R2-I IMPLEMENTATION: NOT STARTED / NOT AUTHORIZED** (as recorded then) — it required this
contract to be authoritative AND a separate Owner execution authorization, both of which have since
been satisfied. PVCG-R3 NOT STARTED; PVCG-R4 NOT STARTED;
PVCG SATISFIED: NO; MINIMUM LAUNCH-CONFORMANCE SET SATISFIED: NO. No release-readiness claim.

**Objective.** A bounded PVCG-R2 implementation was attempted and STOPPED before freeze on two
governance dependencies. This gate governs exactly those two and freezes the R2 product truth, without
implementing anything.

* **DEP-1 — byte-pin reconciliation.** `engine/progression_loop.py` is SHA-256 byte-pinned at
  `tests/test_p9_mech_i3_signal_quality.py:75-78` and enforced by `test_engine_files_byte_frozen`
  (line 313) under the authoritative P9-MECH-I3 contract. The pin is recorded LIVE and is **NOT
  weakened, relaxed, or removed**. R2-I receives ONE BOUNDED reconciliation: update the pinned digest
  only as part of the authorized R2 change, re-freeze the exact post-R2 digest, prove no unrelated
  progression-loop behaviour changed, and preserve the guard. Precedent is established from repository
  history, not prose, with corrected precision: the `progression_loop.py` digest was introduced at
  `32165ca` and **reconciled ONCE, at `9399f9d`** (L2SC-01); the later `41bf30c` (P10-DBT1) update
  changed **`domain_rules.py` only** and left `progression_loop.py` UNCHANGED. That still establishes
  per-key digest reconciliation under explicit later governance as an established mechanism.
* **DEP-2 — defect-dependent fixture correction.** Only fixtures whose INPUT encodes manufactured
  satisfaction may be corrected, and only by replacing that input with a gap-appropriate answer while
  the assertion target and test purpose are preserved. The prior authority is named exactly
  (`STRUCTURED_CRITICALITY_CAPTURE_INCREMENT_CONTRACT.md` §11 / §12 / F4 and
  `tests/test_structured_criticality.py:69`) and **explicitly superseded for R2-I only, and only for
  proven defect-dependent inputs, to the minimum extent necessary**; it remains historical evidence and
  this is not general permission to rewrite fixtures. A five-part fixture-scope test applies per
  fixture; the differential ledger carries **eleven fields** including **CROSS-FILE / EVIDENCE
  IMPACT**; **`ASSERTION-TARGET CHANGES: 0`** with a STOP for Owner review otherwise. Committed WS1–WS7
  evidence trees **remain frozen by default** (no silent regeneration; materially-false artifacts force
  a STOP and a separate authorization), every affected generator/harness is **classified only** and
  none is modified, and any resulting false "byte-identical / untouched / do not edit" comment must be
  corrected truthfully with provenance preserved.

**Frozen R2 product truth.** A response may influence gap satisfaction only when it is sufficiently
relevant to the specific served gap/question context; generic substance, domain vocabulary, causal
language or signal density alone is insufficient for an unrelated gap; the decision is deterministic
and fail-closed — `uncertain relevance ≠ satisfied` — and is never converted into BLOCK, a
contradiction, or an input-validation failure.

**Evidence discipline.** Every diagnostic figure is labelled EXECUTED EVIDENCE reproducible at the
NON-CANDIDATE diagnostic SHA `5154bcf40673e19805410d3199f86089da2c810a` (preserved, not in this
candidate's lineage, never to be published) and is NOT promoted to repository fact. This candidate
changes zero executable bytes; smoke PASS; full suite 3021 passed / 3 skipped / 1 xfailed / 0 failed
re-run at this base; `UNSUPPORTED MATERIAL CLAIMS: 0`.

**Superseded (retained as history) — PVCG-R1: DURABLE EPISTEMIC MEMORY; MERGED AND AUTHORITATIVE via
PR #547.** Base:
`9d2b651588dc6879948e89aac3ec43c8c7c873d7` (PR #546 merge — EMAIL-H1, AUTHORITATIVE; re-resolved live
from `origin/feature/atomic-json-session-persistence` and independently re-verified: first parent
`602ccd39…`, second parent `f4ee27d1…`, merge tree `2aa371a1…`, empty candidate→merge diff).

**Disposition: `PVCG-R1 IMPLEMENTED / CANDIDATE — NOT AUTHORITATIVE UNTIL MERGED`.** PVCG itself is
NOT closed; R2 (gap relevance), R3 (semantic stability) and R4 (correction/invalidation) remain
PENDING and unimplemented. This gate makes **no** release-readiness claim of any kind.

**Objective.** Route the five already-governed NON-ANSWER epistemic dispositions — `unknown`,
`deferred`, `provisional_assumption`, `specialist_requested`, `evidence_requested` — through the
EXISTING canonical durable seam so they survive a process restart and reconstruct with their recorded
meaning. PVCG established (and this gate re-verified from the live repository) that these were
accepted in-session but lost across restart, while `answered` already persisted.

**No schema change and no migration were required.** `engine/record_contract.py` `_ASSERTION_FIELDS`
already carries `disposition`, `content`, `gap_context`, `iteration`, `provenance`,
`validation_status`, `quality`, `pending`, `responsibility`, `resolves_gap`, `contradicts`,
`supersedes`, `superseded_by`; `SqliteRecordStore.append_record` / `load_contract` are
disposition-agnostic. Only `load_accepted_answer_evidence` filters to `answered`, and it is unchanged.

**Delivered (three runtime surfaces + one test file).**
* `web/app.py` — the non-answer branch now mints its record against a throwaway ledger view, computes
  a content-derived idempotency identity (`_interaction_idempotency_key`, same HMAC construction and
  same `idempotency_key` column as the answered path, own domain-separator label), appends through
  `append_record`, and publishes the single ledger delta to live memory ONLY after the durable append
  commits (persist-before-acknowledge). On `IntegrityError` it confirms by reload before treating a
  retry as an idempotent no-op; on any durable failure live memory is unchanged and nothing is
  acknowledged. A separate `INTERACTION_NOT_SAVED_MESSAGE` is used so a deferred / "I don't know"
  action is never misdescribed as an answer.
* `engine/session_reconstruction.py` — the ledger is restored from the FULL validated durable contract
  (one existing read, already performed for `idea_id`) instead of the answered-only subset. **The
  replay still consumes ONLY the answered subset**, so progression is byte-identically unchanged and a
  non-answer record is never replayed, assessed, or allowed to move a gap, maturity, or the stage.
* `web/ui_text.py` — the new message registered under a FREE key (`UI_B_SESSION_049`) with EN + AR.
* `tests/test_pvcg_r1_durable_epistemic_memory.py` — 26 integrated tests whose restart half runs in a
  SEPARATE interpreter against the real on-disk SQLite store.

**Derived state stays derived (no second truth source).** `AcknowledgedUnknown` is deterministically
re-derived by the existing replay from durable answered content — proven, and pinned by a test that
also asserts it is never written as a durable record. `pending` (evidence / specialist) is an existing
field ON the assertion record and therefore persists with it, not beside it. Readiness, gaps, maturity
and stage remain derived. The durable store still holds exactly two tables (`projects`, `records`).

**Backward compatibility.** Answered-only projects reconstruct identically (maturity, open gaps,
ledger, empty acknowledged-unknowns); no new required field; no old row invalidated; missing
historical non-answer records are NEVER fabricated — historical loss stays historical loss.

**Superseded (retained as history) — EMAIL-H1 REPAIR 2: OBS-P5-2-01 bounded token-exposure hardening
+ B-1 guard-truth correction; MERGED AND AUTHORITATIVE via PR #546.** Base:
`602ccd39da59c1d93aa0f99afa2df5f662896503` (PR #545 merge — INFRA-G1-P1, authoritative; re-verified
live from `origin/feature/atomic-json-session-persistence`). Supersedes TWO rejected candidates, both
preserved unchanged and neither merged: `3cea988e41afbc32dfb7e91eee150d6947c2796e` (first) and
`687a626b1312a0fc073fb76cea56bb4db5050a84` (second). This candidate is built FRESH from the
authoritative base; neither rejected SHA was amended, rebased, reused, or published.

**Objective.** Re-apply the independently confirmed EMAIL-H1 hardening and remediate the ONE blocking
finding of the second review, without reopening EMAIL-H1 architecture or Gunicorn logging design:

* **B-1 (the only blocking finding).** The superseded repair excluded ALL docstrings from the
  INFRA-G1-R2 forbidden-term check and described that as "strictly stronger" / "removes no
  protection". That claim was FALSE: terms such as `api_key` and `password` inside an ordinary
  function docstring were caught by the previous guard and passed the superseded one. Reproduced here
  before correcting. The corrected guard restores docstring term-scanning with exactly one narrowly
  authorized waiver (`token`), keeps the operative-string check unchanged, and keeps the
  credential-shaped-literal scan as ADDITIVE coverage. All "strictly stronger" / "removes no
  protection" wording is removed and replaced with the factual description.

Independently confirmed and NOT disturbed (carried through unchanged from the superseded repair):
(BLOCKING-1) the repository-controlled Gunicorn access log wrote raw verification/reset tokens —
fixed by a `logging.Filter` on `gunicorn.access` installed in `post_fork` that redacts the path
segment after `/verify/` or `/reset/` while PRESERVING ordinary access logging (no global disable, no
dropped records, topology unchanged); (BLOCKING-2) the false "already true before this gate" docstring
corrected; NB-1 ordinary-route language-switch guard. Allowed paths: `gunicorn.conf.py`, `web/app.py`,
`web/templates/{reset,base}.html`, `tests/test_email_h1_token_link_exposure_hardening.py`,
`tests/test_email_h1_access_log_token_redaction.py`,
`tests/test_infra_render_production_serving.py` (one conflicting guard corrected — see the roadmap
entry for the exact, non-overstated net effect), and three governance surfaces. Forbidden: provider
integration, Render reopening, ProxyFix, HSTS, schema/TTL/hashing change, topology change. Reviewer
non-blocking findings NB-A…NB-E are CARRIED FORWARD, not expanded.

**Evidence (all re-run fresh on THIS candidate).** EMAIL-H1 RED at the authoritative base with the
final tests: access-log **7 failed / 1 passed**, hardening **9 failed / 7 passed** → GREEN **8/8** and
**16/16** (including a real `gunicorn` boot). Guard RED: the previous INFRA-G1-R2 guard against the
truthful recreated configuration = **1 failed / 17 passed** → corrected guard GREEN **20/20**.
**Differential guard matrix: 15 cases, all as intended** — 1 permitted (`token` alone in a function
docstring), 14 rejected, of which **7 were wrongly allowed by the superseded rejected guard**.
**10 mutation probes, all killed**, every mutated file sha256-verified byte-restored. Targeted
regressions **72 passed** (serving + EMAIL-H1 + RL-1 + architecture guardrails) and **333 passed /
1 skipped** (auth / session / security / localization / reconstruction). `UNIVERSAL GUARDRAIL SMOKE:
PASS`. Full suite **2995 passed / 3 skipped / 1 xfailed / 0 failed** (2994 lineage + the one new
docstring-term guard). `git diff --check` clean.

**Disposition (binding, three surfaces).** FLASK/PYTHON APPLICATION LOGS: no raw token.
REPOSITORY-CONTROLLED GUNICORN ACCESS LOG: HARDENED / VERIFIED. PROVIDER/REVERSE-PROXY ACCESS-LOG
BEHAVIOR: OPEN — MUST BE VERIFIED AT THE FUTURE PROVIDER-DEPENDENT GATE. Browser-history exposure
inherent and open. **OBS-P5-2-01 IS NOT FULLY CLOSED.**

**Boundaries:** no email provider; Render not reopened; no deployment; PSRR COMPLETE: NO; PSRR GO
ELIGIBLE: NO; PAID ACTIVATION AUTHORIZED: NO. `OWNER_DECISION_REGISTER.md` UNCHANGED. Authoritative
ONLY if/when this exact candidate is merged and post-merge verified. Next required step: **Independent
External Re-Review of this exact SHA + bundle**.

**Immediately prior (INFRA-G1-P1 RENDER PROVISIONING & NON-PUBLIC VERIFICATION CONTRACT:
Owner-authorized GOVERNANCE-ONLY candidate; MERGED via PR #545; retained as history):** Base: `5e68a59cefe8fa47b5fbc201387b1e785820a86a`
(PR #544 merge — INFRA-G1-R2, authoritative; independently re-verified live: first parent
`306f3499…`, second parent `5326481955…`, merge tree `4bdbaa06…` = accepted candidate tree, empty
candidate→merge diff).

**Objective.** ONE governance-only candidate creating
`docs/governance/INFRA_G1_P1_RENDER_PROVISIONING_NON_PUBLIC_VERIFICATION_CONTRACT.md` — the
provisioning SPECIFICATION for the first real Render resource plus the post-provision verification
PROCEDURE, creating and configuring NOTHING (a separate Owner execution authorization is required
before any resource exists). Includes: fixed OD-INFRA-1/2 decisions carried unchanged; the
authoritative runtime posture re-read at this base; the PSRR provider/production mapping re-derived
from PSRR-C1 §5.2 and the application-layer record (no item closed); a 22-row provisioning
specification with every provider mechanic classified OWNER CONFIGURATION REQUIRED or TO BE CONFIRMED
DURING PROVISIONING (official Render documentation is unreachable from this environment — nothing is
promoted to verified); a 10-point BLOCKING SQLite persistence contract; backup, monitoring, email and
public-access boundaries; AUTO-DEPLOY OFF; the secret matrix with no values; and a 20-step non-public
verification procedure. Allowed paths: the new contract + `ACTIVE_EXECUTION_ROADMAP.md` +
`CURRENT_PROJECT_STATE.md` + `ACTIVE_INCREMENT_CONTRACT.md` ONLY. Forbidden: all runtime/test/schema/
guardrail paths; `OWNER_DECISION_REGISTER.md`; any resource creation, DNS, TLS, secret, email,
payment, or deployment action.

**Evidence.** Governance-only docs diff; smoke PASS at base and re-verified at candidate; §5B.1
determination recorded openly (zero executable bytes — not an implementation candidate; no §5B.6
trigger; the authoritative full-suite truth 2969/3/1/0 stands from the merged INFRA-G1-R2 lineage and
its independent reproduction); adversarial governance truth sweep UNSUPPORTED MATERIAL CLAIMS: 0.

**Boundaries:** RENDER RESOURCE CREATED: NO; PERSISTENT DISK CREATED: NO; DNS CONFIGURED: NO;
PRODUCTION SECRETS CONFIGURED: NO; PRODUCTION EMAIL CONFIGURED: NO; PUBLIC DEPLOYMENT STARTED: NO;
OPS-SM1 EXECUTED: NO; PSRR COMPLETE: NO; PSRR GO ELIGIBLE: NO; DEPLOYMENT AUTHORIZED: NO; PAID
ACTIVATION AUTHORIZED: NO; no runtime/database change; no future-domain work.
`OWNER_DECISION_REGISTER.md` UNCHANGED. Authoritative ONLY if/when this exact candidate is merged and
post-merge verified. Next required step: **Independent External Review of this exact SHA + bundle**
(§5B.13 incl. mandatory independent smoke).

**Immediately prior (INFRA-G1-R2 — repair candidate `5326481955…` Owner-accepted at that exact SHA and
MERGED via PR #544, tip `5e68a59cefe8fa47b5fbc201387b1e785820a86a`; now AUTHORITATIVE; the earlier
`36eb4102…` remains superseded evidence and must not be published; retained as history):** Base: `306f3499a2bd51e9d7047c9ffd5c4f091d2ca696`
(PR #543 merge — INFRA-G1-R1, authoritative; independently re-verified live: first parent
`9b3bc28e…`, second parent `458c1316…`, merge tree `b5df6a4a…` = accepted candidate tree, empty
candidate→merge diff).

**Objective.** Implement ONLY the INFRA-G1-R1 §4/§13 production-serving scope: a diagnosed production
WSGI server (**Gunicorn**, selected on measured evidence over Waitress — see the roadmap entry), a
provider-neutral `gunicorn.conf.py` pinning workers=1 / threads=1 / `preload_app=False` /
`reload=False` / `bind=0.0.0.0:$PORT`, a pinned `gunicorn==26.1.0` dependency, a `.python-version`
pin (`3.11`), and 18 AST/behaviour tests proving the WSGI target, the single-worker/single-thread
invariant, PORT consumption, dev-server separation, and the security non-regressions. No `render.yaml`
(dashboard configuration suffices; provider coupling avoided). Allowed paths: `gunicorn.conf.py`,
`.python-version`, `requirements.txt`, `tests/test_infra_render_production_serving.py`,
`tests/test_p10_rl1_release_readiness_checklist.py` (synchronized guardrail strengthening),
`PHASE_10_RELEASE_READINESS_CHECKLIST.md`, `ACTIVE_EXECUTION_ROADMAP.md`, `CURRENT_PROJECT_STATE.md`,
`ACTIVE_INCREMENT_CONTRACT.md`. Forbidden: `web/`, `engine/`, `domains/`, schemas, provisioning, DNS,
TLS, secrets, `OWNER_DECISION_REGISTER.md`.

**Evidence.** RED reconstructed at the exact base with the final test file — 14 failed / 4 passed
(reviewer-reproduced; the earlier “15/3” figure is withdrawn as non-reproducible) → GREEN 18/18; live end-to-end gunicorn serve (200 on `/health`
and `/`; CSP present; HSTS absent; 1 worker; worker thread count 1); 12 mutation probes killed; fresh
dependency audit ZERO known findings; targeted regressions 159 passed; smoke PASS pre+post; **full
suite 2969 passed / 3 skipped / 1 xfailed / 0 failed**; adversarial implementation truth sweep
UNSUPPORTED MATERIAL CLAIMS: 0.

**Boundaries:** development path unchanged; no ProxyFix/HSTS/forwarded-header trust; no SQLite/schema/
ORM change; no email/monitoring/payment dependency; INFRASTRUCTURE PROVISIONED: NO; PUBLIC DEPLOYMENT
STARTED: NO; OPS-SM1 EXECUTED: NO; PSRR COMPLETE: NO; PSRR GO ELIGIBLE: NO; DEPLOYMENT AUTHORIZED: NO;
PAID ACTIVATION AUTHORIZED: NO. `OWNER_DECISION_REGISTER.md` UNCHANGED. Authoritative ONLY if/when this
exact candidate is merged and post-merge verified. Next required step: **Independent External Review of
this exact SHA + bundle** (LEVEL 1 implementation path — reviewer full suite mandatory under §5B).

**Immediately prior (INFRA-G1-R1 — governance-only candidate `458c1316…` Owner-accepted at that exact
SHA and MERGED via PR #543, tip `306f3499a2bd51e9d7047c9ffd5c4f091d2ca696`; now AUTHORITATIVE;
OD-INFRA-1 RENDER / OD-INFRA-2 FRANKFURT durably recorded; retained as history):** Base:
`9b3bc28ebeea68963b836bb508141dc3228092f7` (PR #542 merge — INFRA-G1-C, authoritative; independently
re-verified live: first parent `88c5f4d5…`, second parent `e79a2300…`, merge tree `3c1a48cb…` =
accepted candidate tree, empty candidate→merge diff).

**Objective.** ONE governance-only candidate creating
`docs/governance/INFRA_G1_R1_HOSTING_REGION_SELECTION_AND_RENDER_DEPLOYMENT_PREPARATION_CONTRACT.md`
that (A) durably records the Owner selections under INFRA-G1-C §2 — **OD-INFRA-1 HOSTING: RENDER;
OD-INFRA-2 REGION: FRANKFURT** (Fly.io = fallback only; no legal/tax/residency/commercial conclusion;
OD-INFRA-3…6 remain OPEN) — and (B) defines the bounded future Render deployment-preparation
contracts: SQLite/persistent-disk (SUPPORTED; no migration; env-only; provisioning verification
duties); production serving/WSGI (built-in server not acceptable publicly; future
single-worker/single-thread posture; no dependency pre-authorized; implementation NOT authorized
here); infrastructure artifacts (version pin REQUIRED, start declaration REQUIRED, render.yaml
OPTIONAL — none created); trusted-proxy/TLS truth (no forwarded trust; ProxyFix NO; HSTS
reassessment-only); production-config matrix (no secret values); health-check acceptance;
backup/restore duties (snapshots never sufficient alone; governed backup + off-provider + restore
drill; retention policy-open); monitoring/logging (items 21–22/26/28 OPEN; logs not durable); email
separation (needed before public release, not before provisioning); OPS-SM1 registered-only; the
exact next implementation-gate scope + exclusions and the future provisioning scope (neither
authorized); PSRR mapping with nothing PASS. Allowed paths: the new record +
`ACTIVE_EXECUTION_ROADMAP.md` + `CURRENT_PROJECT_STATE.md` + `ACTIVE_INCREMENT_CONTRACT.md` ONLY.
Forbidden: all runtime/test/schema/guardrail paths; `OWNER_DECISION_REGISTER.md`; any dependency/
artifact creation; any provisioning/DNS/TLS/secrets; any provider selection beyond recording the two
Owner selections.

**Evidence.** Governance-only docs diff; smoke PASS at base and re-verified at candidate; §5B.1
determination recorded openly (zero executable bytes — not an implementation candidate; no §5B.6
trigger; authoritative full-suite truth 2951/3/1/0 stands on this lineage); adversarial governance
truth sweep UNSUPPORTED MATERIAL CLAIMS: 0.

**Boundaries:** INFRASTRUCTURE PROVISIONED: NO; RUNTIME IMPLEMENTATION AUTHORIZED: NO; OPS-SM1
EXECUTED: NO; PSRR COMPLETE: NO; PSRR GO ELIGIBLE: NO; DEPLOYMENT AUTHORIZED: NO; PAID ACTIVATION
AUTHORIZED: NO; no email/payment selection; no future-domain work. `OWNER_DECISION_REGISTER.md`
UNCHANGED. Authoritative ONLY if/when this exact candidate is merged and post-merge verified. Next
required step: **Independent External Review of this exact SHA + bundle** (§5B.13 incl. mandatory
independent smoke).

**Immediately prior (INFRA-G1-C PRODUCTION INFRASTRUCTURE & PROVIDER SELECTION CONTRACT —
governance-only candidate `e79a2300…` Owner-accepted at that exact SHA and MERGED via PR #542, tip
`9b3bc28ebeea68963b836bb508141dc3228092f7`; now AUTHORITATIVE; retained as history):** Base:
`88c5f4d5d3d3a5afb508b5f26852fd9e13d7ece9`
(PR #541 merge — PSRR application-layer recording, authoritative; independently re-verified live:
first parent `274652a5…`, second parent `382d6733…`, merge tree `9452481f…` = accepted candidate tree,
empty candidate→merge diff).

**Objective.** ONE governance-only candidate creating
`docs/governance/INFRA_G1_C_PRODUCTION_INFRASTRUCTURE_PROVIDER_SELECTION_CONTRACT.md`: the OD-J2 §3.2
delegated gate's contract (core preserved exactly — hosting provider + production region; OD-J2 not
rewritten/expanded) plus selection/configuration coordination criteria for TLS/proxy, monitoring/
alerting, backup/restore, email, and secrets/logging operations with all canonical boundary owners
preserved (P10-SEC1, P10-OB1, P10-BR1, email boundary, RL-C1/PSRR §8); per-surface selection criteria,
evidence-before-acceptance obligations, portability/lock-in requirements, per-surface separate future
Owner selection decisions, hosting-first sequencing; seven possible-code diagnostic gates (each:
DIAGNOSIS REQUIRED BEFORE CODE / SEPARATE OWNER IMPLEMENTATION AUTHORIZATION REQUIRED); OPS-SM1
registered (not executed; nothing built); policy/legal separation (substance consumed, never created);
PSRR dependency mapping with state preserved (no item PASS from contract existence); free-vs-paid
separation preserved; payment/MoR/pricing/tax/deployment authorization excluded. Allowed paths: the
new contract + `ACTIVE_EXECUTION_ROADMAP.md` + `CURRENT_PROJECT_STATE.md` +
`ACTIVE_INCREMENT_CONTRACT.md` ONLY. Forbidden: all runtime/test/schema/guardrail paths;
`OWNER_DECISION_REGISTER.md`; any provider naming/evaluation/selection; any provisioning.

**Evidence.** Governance-only docs diff; smoke PASS at base and re-verified at candidate; §5B.1
determination recorded openly (zero executable bytes — not an implementation candidate; no §5B.6
trigger; authoritative full-suite truth 2951/3/1/0 stands from the Creator + Independent runs at the
application-layer tranche on this lineage); adversarial governance truth sweep UNSUPPORTED MATERIAL
CLAIMS: 0.

**Boundaries:** PROVIDER SELECTED: NO; RUNTIME IMPLEMENTATION STARTED: NO; OPS-SM1 EXECUTED: NO; PSRR
COMPLETE: NO; PSRR GO ELIGIBLE: NO; DEPLOYMENT AUTHORIZED: NO; PAID ACTIVATION AUTHORIZED: NO
(`D-P8-PL-01 class C`); no future-domain work. `OWNER_DECISION_REGISTER.md` UNCHANGED. Authoritative
ONLY if/when this exact candidate is merged and post-merge verified. Next required step: **Independent
External Review of this exact SHA + bundle** (§5B.13 incl. mandatory independent smoke).

**Immediately prior (PSRR APPLICATION-LAYER TRANCHE EXECUTION RECORD — governance-only candidate
`382d6733…` Owner-accepted at that exact SHA and MERGED via PR #541, tip
`88c5f4d5d3d3a5afb508b5f26852fd9e13d7ece9`; now AUTHORITATIVE — APPLICATION-LAYER TRANCHE:
AUTHORITATIVE EVIDENCE; retained as history):** Base: `274652a51c2132500c8c6b79e5666932f4ba77da`
(PR #540 merge — PSRR-C1, authoritative; independently re-verified live: first parent `aab8f365…`,
second parent `2b694597…`, merge tree `be57a33a…` = accepted candidate tree, empty candidate→merge
diff).

**Objective.** ONE governance-only recording candidate creating
`docs/governance/PSRR_APPLICATION_LAYER_TRANCHE_EXECUTION_RECORD.md`: the Owner-accepted,
independently reviewed PSRR application-layer tranche recorded as EXECUTED (scope owner = PSRR-C1
§5.1; grouped-rows-vs-items precision per reviewer OBS-5: 17 grouped execution rows / 19 contract line
entries / 21 distinct PSRR item numbers; registered PSRR minimum remains 37); reviewed evidence
recorded faithfully (Creator targeted 207 passed; Creator AND Independent full suites both 2951/3/1/0
— the independent rerun escalated under GOV-RBR1 after an environment-caused smoke BLOCK that was NOT
a candidate defect; smokes PASS; fresh dependency audit zero known findings, point-in-time; zero
runtime modification during execution; RUNTIME IMPLEMENTATION REQUIRED: NO); reviewer observations
OBS-1…OBS-5 dispositioned (OBS-1 CSRF claim-accuracy correction recorded — resume does NOT use the
answer-flow HMAC mechanism; OBS-5 resolved in-record; OBS-2/3/4 carried forward non-blocking, nothing
implemented); PSRR-C1 N1/N2/N3 preserved; remaining PSRR work enumerated (provider tranche, production
halves, policy substance, items 35–37) with PSRR GO ELIGIBLE: NO and PSRR COMPLETE: NO. Allowed paths:
the new record + `ACTIVE_EXECUTION_ROADMAP.md` + `CURRENT_PROJECT_STATE.md` +
`ACTIVE_INCREMENT_CONTRACT.md` + `PHASE_10_RELEASE_READINESS_CHECKLIST.md` (RL-G4 partial-execution
truth only, pins preserved). Forbidden: all runtime/test/schema/guardrail paths;
`OWNER_DECISION_REGISTER.md`; implementing any observation; additional PSRR execution; INFRA-G1;
provider selection.

**Evidence.** Governance-only docs diff; smoke PASS at base and re-verified at candidate; RL1
structural suite green at candidate; §5B.1 determination recorded openly (zero executable bytes — not
an implementation candidate; no §5B.6 trigger; the authoritative full-suite truth 2951/3/1/0 stands
from BOTH the Creator tranche run and the Independent Reviewer rerun at this exact tip); adversarial
governance truth sweep UNSUPPORTED MATERIAL CLAIMS: 0.

**Boundaries:** records execution state only — PSRR NOT COMPLETE; NO GO; DEPLOYMENT AUTHORIZED: NO;
PAID ACTIVATION AUTHORIZED: NO; no provider selection; no observation implemented; no additional
tranche executed; no future-domain work. `OWNER_DECISION_REGISTER.md` UNCHANGED. Authoritative ONLY
if/when this exact candidate is merged and post-merge verified. Next required step: **Independent
External Review of this exact SHA + bundle** (§5B.13 incl. mandatory independent smoke).

**Immediately prior (PSRR-C1 PSRR EXECUTION CONTRACT — governance-only candidate `2b694597…`
Owner-accepted at that exact SHA and MERGED via PR #540, tip
`274652a51c2132500c8c6b79e5666932f4ba77da`; now AUTHORITATIVE; retained as history):**
Base: `aab8f365f1bd37523dbbbf970533f8e5ecf3ce42` (PR #539 merge — Phase-10 Formal Closure,
authoritative; independently re-verified live: first parent `adfe203a…`, second parent `3ac06dca…`,
merge tree `4d76957f…` = accepted candidate tree, empty candidate→merge diff). **PHASE 10 FORMALLY
CLOSED — OPTION 2 AUTHORITATIVE.**

**Objective.** ONE governance-only candidate creating
`docs/governance/PSRR_C1_PSRR_EXECUTION_CONTRACT.md`: the PSRR 37-item registered minimum scope
instantiated into an item-by-item execution contract (application-layer / provider-dependent /
policy-legal / final-evidence / decision tranches; per-item evidence, method, dependency, owner,
start-now, GO-blocking, deployment-blocking, and outstanding-risk treatment); first durable recording
of `OD-FR1` (deployment intent = YES — PSRR §4 trigger FACT only) and of the Owner tax-governance
foundation (no speculative tax implementation; configuration-driven future treatment as no-foreclosure
only; TQ registers preserved OPEN with amended resolution pathway); infrastructure-gate relationship
with OD-J2 §3.2 kept to its exact scope (hosting + region) and the INFRA-G1 selection-gate governance
gap named (nothing opened or selected); GO/NO-GO model preserved verbatim; execution / deployment /
paid-activation separations intact. Allowed paths: the new contract +
`ACTIVE_EXECUTION_ROADMAP.md` + `CURRENT_PROJECT_STATE.md` + `ACTIVE_INCREMENT_CONTRACT.md` +
`PHASE_10_RELEASE_READINESS_CHECKLIST.md` (RL-G3 trigger-truth sync only, pins preserved). Forbidden:
all runtime/test/schema/guardrail paths; `OWNER_DECISION_REGISTER.md`; any provider selection; any tax
implementation; starting PSRR execution.

**Evidence.** Governance-only docs diff; smoke PASS at base and re-verified at candidate; RL1
structural suite green at candidate; §5B.1 Creator full-suite determination recorded openly (zero
executable bytes — not an implementation candidate; no §5B.6 trigger; authoritative full-suite truth
2951/3/1/0 stands from the Phase-10 closure gate and its independent reproduction); adversarial
governance truth sweep UNSUPPORTED MATERIAL CLAIMS: 0.

**Boundaries:** PSRR EXECUTION NOT AUTHORIZED / NOT STARTED (requires separate Owner authorization
against the frozen contract); DEPLOYMENT AUTHORIZED: NO (OD-P two-part preserved); PAID ACTIVATION
AUTHORIZED: NO (`D-P8-PL-01 class C` preserved); SPECULATIVE TAX IMPLEMENTATION REQUIRED NOW: NO; no
provider/vendor/tool selection; no legal/tax conclusion; no future-domain work.
`OWNER_DECISION_REGISTER.md` UNCHANGED. Authoritative ONLY if/when this exact candidate is merged and
post-merge verified. Next required step: **Independent External Review of this exact SHA + bundle**
(§5B.13 path incl. the mandatory independent smoke).

**Immediately prior (PHASE 10 FORMAL CLOSURE RECORD — governance-only candidate `3ac06dca…`
Owner-accepted at that exact SHA and MERGED via PR #539, tip
`aab8f365f1bd37523dbbbf970533f8e5ecf3ce42`; now AUTHORITATIVE — PHASE 10 FORMALLY CLOSED, OPTION 2
STRUCTURE AUTHORITATIVE; retained as history):**
Base: `adfe203a84a66028b7a1f943920084108f6cc48c` (PR #538 merge — P10-CL0, authoritative; independently
re-verified live: first parent `2f77e8e8…`, second parent `deeb046e…`, merge tree `2b62bf57…` = accepted
candidate tree, empty candidate→merge diff).

**Objective.** Create `docs/governance/PHASE_10_FORMAL_CLOSURE_RECORD.md` — the separately authorized
Phase-10 formal-closure instrument (P10-C §11 is increment-closure only, per P10-CL0-NB2) — declaring
**PHASE 10 FORMALLY CLOSED** under the Owner-accepted `OD-P10-CL0-STRUCTURE` OPTION 2, with: the final
obligation disposition matrix re-verified LIVE at this base (no `UNRESOLVED — CLOSURE BLOCKING` row; no
deferred item converted to COMPLETE); complete gate lineage (PRs #508–#538); explicit closure meaning
and non-meaning; all P10-CL0 NB1–NB11 dispositioned (none dropped); and the next permitted gate
identified but NOT opened (FR-GS1 — First-Release Post-Phase-10 Gate Selection; PSRR NOT triggered by
closure). Allowed paths: the new closure record + `ACTIVE_EXECUTION_ROADMAP.md` +
`CURRENT_PROJECT_STATE.md` + `ACTIVE_INCREMENT_CONTRACT.md` + `PHASE_10_RELEASE_READINESS_CHECKLIST.md`
+ ONE narrowly justified pinned-line update in `tests/test_p10_rl1_release_readiness_checklist.py`
(the "PHASE 10 CLOSURE ELIGIBLE NOW: NO" pin is factually superseded by the Owner-accepted P10-CL0
eligibility determination + Option-2 decision; the replacement pin preserves the test's protective
purpose). Forbidden: all runtime/schema/guardrail paths; `OWNER_DECISION_REGISTER.md`.

**Evidence.** Governance-only diff + the one-line test-pin update; smoke PASS at base and re-verified at
candidate; RL1 structural suite green at candidate; FULL SUITE run at the candidate (conservative §5B
posture because a test file changed); adversarial governance truth sweep UNSUPPORTED MATERIAL CLAIMS: 0.

**Boundaries:** closure ≠ legal/tax/commercial readiness ≠ PSRR ≠ deployment ≠ paid activation; PSRR
remains REGISTERED / NOT TRIGGERED / NOT EXECUTED; OD-P two-part deployment control preserved;
`D-P8-PL-01 class C` preserved; no provider selection; no pricing/refund/trial/dunning decision; no
brand clearance (OD-A in force); no future-domain work (DOMEX-D1 deferred until after first release).
`OWNER_DECISION_REGISTER.md` UNCHANGED. Authoritative ONLY if/when this exact candidate is merged and
post-merge verified. Next required step: **Independent External Review of this exact SHA + bundle**.

**Immediately prior (P10-CL0 PHASE-10 CLOSURE-PRECONDITION CONSOLIDATION & OPEN-OBLIGATION DISPOSITION
GATE — governance-only candidate `deeb046e…` Owner-accepted at that exact SHA and MERGED via PR #538,
tip `adfe203a84a66028b7a1f943920084108f6cc48c`; now AUTHORITATIVE; Owner decision at acceptance:
`OD-P10-CL0-STRUCTURE` = OPTION 2 — ACCEPTED; retained as history):** Base:
`2f77e8e8b633497adee6ea32a6002a7c5860979e` (PR #537 merge — GAP-SYNC-01, authoritative; independently
re-verified live: first parent `38da08da…`, second parent `087c1d18…`, merge tree `0d337986…` equal to
the accepted candidate tree, empty candidate→merge diff).

**Objective.** ONE governance-only candidate that: (1) synchronizes authoritative statuses (GOV-RBR1
PR #536; GAP-SYNC-01 PR #537; Owner-accepted Product Completion diagnosis — CORE PRODUCT FUNCTIONALLY
COMPLETE: YES / NEW CORE IMPLEMENTATION REQUIRED NOW: NO); (2) durably records the read-only SPACE-D1
and Domain Expansion Strategy Reconstruction diagnoses with the explicit deferral (DOMEX-D1 DEFERRED
UNTIL AFTER FIRST RELEASE; no SPACE-C1/IOT-C1/Renewable/Drone contract; NO current future-domain
implementation authorized; OD-H planning priority order unchanged); (3) registers GAP-SYNC-01-NB1/NB2/
NB3 (non-blocking; NB3 gate-prefixed namespacing adopted); (4) refreshes the P10-RL1 checklist
point-in-time facts without changing any gate status (RL-A1 suite counts from a fresh live run at this
base — 2951 passed / 3 skipped / 1 xfailed / 0 failures; new RL-A10 product-completion row; all pinned
invariants preserved and the structural suite green); (5) builds the complete Phase-10
closure-disposition matrix over every P10-C §4 obligation row with only authoritative named destination
lanes (PSRR / deployment gate / OD-J2 infrastructure gate / external legal-tax intake / commercial
activation gate / brand-trademark gate); (6) isolates the single Owner structure decision
`OD-P10-CL0-STRUCTURE` (Option 1 hold-open vs Option 2 close-with-dispositions); and (7) determines
PHASE 10 CLOSURE ELIGIBLE AFTER OWNER ACCEPTANCE: YES, conditional on that decision. The formal
Phase-10 closure record is NOT created (separate future gate per P10-C §11). Allowed paths: the new
gate document + `ACTIVE_EXECUTION_ROADMAP.md` + `CURRENT_PROJECT_STATE.md` +
`ACTIVE_INCREMENT_CONTRACT.md` + `PHASE_10_RELEASE_READINESS_CHECKLIST.md` ONLY. Forbidden: all
runtime/test/schema/guardrail paths; `OWNER_DECISION_REGISTER.md`.

**Evidence.** Governance-only diff (five documentation surfaces); smoke PASS at base and re-verified at
candidate; fresh full-suite live run at base 2951/3/1/0 (evidence for the RL-A1 refreshed fact; §5B.1
Creator full-suite obligation NOT triggered — zero executable bytes change, recorded openly); P10-RL1
structural invariant suite green at candidate; adversarial governance truth sweep UNSUPPORTED MATERIAL
CLAIMS: 0.

**Boundaries:** no runtime implementation; no PSRR trigger/execution; no deployment; no paid activation
(`D-P8-PL-01 class C` preserved); no provider selection; no legal/tax conclusion; no future-domain
implementation (no DOMEX-D1/SPACE-C1/IOT-C1/Renewable contract); no formal Phase-10 closure record; no
new closure standard (P10-C §4 remains the obligation owner; P10-RL1 remains the truth surface).
`OWNER_DECISION_REGISTER.md` UNCHANGED. Authoritative ONLY if/when this exact candidate is merged and
post-merge verified. Next required step: **Independent External Review of this exact SHA + bundle**
(governance-only path per §5B.13 incl. the mandatory independent smoke).

**Immediately prior (GAP-SYNC-01 GOVERNANCE/WORDING TRUTH SYNCHRONIZATION — governance-only candidate
`087c1d18…` Owner-accepted at that exact SHA and MERGED via PR #537, tip
`2f77e8e8b633497adee6ea32a6002a7c5860979e`; now AUTHORITATIVE; retained as history):** Base:
`38da08dae389f74279082e1341e220dbc0f80851` (PR #536 merge — GOV-RBR1,
authoritative; independently re-verified: parents `bf7fe7ce…` / `1759b148…`, merge tree `1aa5c469…` equal
to the accepted candidate tree, empty candidate→merge diff). First gate operating under authoritative
LEAN §5B. Owner-accepted diagnosis stands: CORE PRODUCT FUNCTIONALLY COMPLETE: YES; NEW CORE
IMPLEMENTATION REQUIRED NOW: NO.

**Objective.** Synchronize the six confirmed wording/truth residuals with ZERO executable behavior
change: GOV-RBR1 reviewer O1 (§5B.1 lifecycle attribution: §5A obligation PLUS the established per-gate
lifecycle), O2 (§5B.13↔§5B.3: independent smoke NOT optional where Independent Review is required), O3
(§5B.3(9) "where meaningful" = probe-design judgment only; removes nothing mandatory), O4 (§5B.6
qualitative triggers stay conservative because the catch-all + unconditional escalation remain
controlling), O5 (§5B.15: local-only rejected-evidence artifacts never described as independently
remote-verifiable), and PC3-O2 (the stale "never rehydrated into SESSION_STORE" inline comment in
`engine/session_reconstruction.py` corrected to the narrow sole-authorized-consumer rule — COMMENT-ONLY,
AST proven identical). Canonical LEAN owner amended in place; no new standard; no duplicate authority.

**Evidence.** AST identity proof for the code file; targeted reconstruction+framework suites 79 passed;
smoke PASS; conservative full suite 2951 passed / 3 skipped / 1 xfailed / 0 failures (identical to
baseline; §5B.1 full-suite-obligation determination recorded openly: not an implementation candidate,
run anyway because a runtime file's bytes changed); truth sweep UNSUPPORTED MATERIAL CLAIMS: 0.

**Boundaries:** zero behavior; no rule weakening (all clarifications conservative-direction); no product
feature; no new domain; paid activation BLOCKED; PSRR NOT TRIGGERED; DEPLOYMENT NOT AUTHORIZED; legal/tax
registers OPEN. `OWNER_DECISION_REGISTER.md` UNCHANGED. Review tier: LEVEL 2 (Owner-directed; not
downgraded). Authoritative ONLY if/when this exact candidate is merged and post-merge verified. Next
required step: **Independent External Review of this exact SHA + bundle** (§5B.13 governance-only path
incl. mandatory independent smoke).

**Immediately prior (GOV-RBR1 RISK-BASED INDEPENDENT REVIEW & EVIDENCE REUSE — governance-only candidate
`1759b148…` Owner-accepted at that exact SHA and MERGED via PR #536, tip
`38da08dae389f74279082e1341e220dbc0f80851`; now AUTHORITATIVE; retained as history):** Base:
`bf7fe7ce1b180ecfe78c1d790b6c4e6eb63ce159` (PR #535 merge —
P10-PC3 True Writable Resume repair implementation, authoritative; independently re-verified: parents
`cfad3feb…` / `be8bba16…`, merge tree `c3876b5a…` equal to the accepted candidate tree, empty
candidate→merge diff).

**Objective.** Amend the CANONICAL review-policy owner in place —
`LEAN_GOVERNANCE_AND_AGENT_CONTINUITY_PROTOCOL.md` new **§5B** — to reduce duplicative review execution
without reducing any mandatory review: Creator obligations unchanged (full lifecycle incl. mandatory
Creator full suite); evidence reuse only after independent exact-identity verification and never as blind
trust; an 11-item universal review minimum never replaced by Creator evidence; LEVEL 1 Reviewer full
suite mandatory; LEVEL 2 conditional reuse (conjunctive conditions A–H) with 15 explicit full-suite
triggers plus unconditional reviewer escalation; conservative repair-after-REJECT rule; bounded Universal
Smoke role; no-duplicate-testing rule with recorded substitution; reviewer value shifted to novel
adversarial work (PC3/B1 lesson codified truthfully); mandatory auditable evidence-reporting table;
governance-only review optimization; no silent review downgrade; explicit quality floor; performance
objective without artificial SLA. No overlapping standard created; UG standard untouched. P10-PC3
reviewer O1–O4 dispositioned (O2 — the stale `session_reconstruction` inline comment — DEFERRED to the
next code-touching synchronization; this candidate touches no code).

**Evidence.** Governance-only diff (protocol §5B + three governance surfaces); baseline smoke PASS at
base and re-verified at candidate; full suite re-verified unchanged at candidate; adversarial governance
truth sweep UNSUPPORTED MATERIAL CLAIMS: 0.

**Boundaries:** no runtime implementation; no product change; no guardrail change; no review waiver;
§12's non-weakening guarantee applies to this amendment itself; paid activation BLOCKED; PSRR NOT
TRIGGERED; DEPLOYMENT NOT AUTHORIZED; legal/tax registers OPEN; no provider/commercial decision; no new
domain. `OWNER_DECISION_REGISTER.md` UNCHANGED. Authoritative ONLY if/when this exact candidate is merged
and post-merge verified. Next required step: **Independent External Review of this exact SHA + bundle**.

**Immediately prior (P10-PC3 TRUE WRITABLE RESUME IMPLEMENTATION, REPAIR — candidate `be8bba16…`
Owner-accepted at that exact SHA and MERGED via PR #535, tip
`bf7fe7ce1b180ecfe78c1d790b6c4e6eb63ce159`; now AUTHORITATIVE; the earlier rejected candidate
`ee8a0dad…` remains immutable rejected evidence; retained as history):** Base:
`cfad3febdcb886a5efa316a023d31b31d31568ac` (PR #534 merge — P10-PC3-C contract,
authoritative; independently re-verified). Governed by the merged
`P10_PC3_TRUE_WRITABLE_RESUME_INCREMENT_CONTRACT.md` (reviewer O1–O4 incorporated as its append-only
§17). **Prior implementation candidate `ee8a0dad…` REJECTED by Independent External Review — blocking
defect B1 (record-id collision after resume with interleaved non-answer history: the length-derived
ledger mint could re-mint a persisted `rec_N`, making the N+1 durable append fail permanently);
preserved unamended on `p10-pc3-rejected-evidence` as immutable rejected evidence. This repair
candidate's parent is the exact authoritative base.**

**Objective.** All rejected-candidate behavior preserved (explicit establishment POST; zero durable
writes at establishment; GET read-only; ownership first; canonical replay only; fresh transient context;
no fabricated history; token/idempotency reused wholesale; completed/deactivated refusals; PC1/PC2
preserved; EN/AR wording; UG-CORE-07 preserved; UG-CORE-08 successor; UG-CORE-16) PLUS the B1 repair:
the canonical ledger mint (`engine/idea_state.py record_interaction`) now derives the next id from the
ledger's MAX existing numeric `rec_N` (+1) — byte-identical for every live contiguous ledger
(max == len; equivalence test-pinned), collision-free for reconstructed sparse ledgers (the ledger max
IS the durable max). No schema change; no resume-only allocator; no renumbering. UG-CORE-16
STRENGTHENED with the two interleaved-history tests; N3 docstrings state the narrow sole-consumer
rehydration rule; N2 recorded as reviewer-checklist residual only.

**Evidence.** B1 RED 3/4 at the defective implementation (reviewer's exact class reproduced live);
GREEN 22/22; mutations m8 (defective allocator restored → B1 tests fail) and m9 (max-id reuse →
equivalence pin fails) killed; m4 re-verified; sparse duplicate-retry probe exactly-once
(`rec_1, rec_3, rec_4`); pre/post smoke PASS (17+1 guards, 76+1 items, 4.9s); ledger-lane regression
104 passed; full suite 2951 passed / 3 skipped / 1 xfailed / 0 failures (prior 2929 + 22 new).

**Boundaries:** unchanged binding set; paid activation BLOCKED; PSRR NOT TRIGGERED; DEPLOYMENT NOT
AUTHORIZED; legal/tax registers OPEN; no provider/commercial decision; no new domain.
`OWNER_DECISION_REGISTER.md` UNCHANGED. Review tier: **LEVEL 1** — formal Independent External Review
required. Authoritative ONLY if/when this exact candidate is merged and post-merge verified.

**Immediately prior (P10-PC3-C TRUE WRITABLE RESUME CONTRACT — governance-only candidate `783becf2…`
Owner-accepted at that exact SHA and MERGED via PR #534, tip `cfad3feb…`; AUTHORITATIVE as the canonical
contract; retained as history):** Base: `aed5cb79f53e47c5e36e0fce6228288bfae8c014` (PR #533 merge —
P10-PC2 cold-load
deliverable fidelity, authoritative; independently re-verified: parents `edae7f30…` / `4218ed0b…`, merge
tree `77fc4b81…` equal to the accepted candidate tree, empty candidate→merge diff).

**Objective.** Create the canonical governance contract for TRUE WRITABLE RESUME —
`docs/governance/P10_PC3_TRUE_WRITABLE_RESUME_INCREMENT_CONTRACT.md` — WITHOUT implementing anything:
source-cited non-resume boundary reconstruction; binding resume semantics (project-identity continuity in
a NEW transient context; canonical-replay-only state; never-fabricated transients; exactly-once N+1
append); token/idempotency reuse contract; explicit non-durable SESSION_STORE establishment contract;
replay-then-continue sequence with prohibited parallel engines; ownership/mode/failure/eligibility/
concurrency rules; the REQUIRED future governed Universal-Guardrail evolution (successor guard pair for
UG-CORE-08 + new resume-integrity guard — executed only inside the future implementation candidate); 12
mandatory RED items + 9 adversarial probes; success criteria; exclusions. Review tier for implementation:
**LEVEL 1** (LEAN protocol §4/§5) — separate explicit Owner implementation authorization AND formal
Independent External Review required. Baseline smoke on the base: PASS (7.5s; zero observations).

**Evidence.** Governance-only diff (contract + the three governance surfaces; zero runtime/test/guardrail
change); adversarial governance truth sweep UNSUPPORTED MATERIAL CLAIMS: 0; full suite unchanged by
construction (no test/code paths touched) and re-verified at candidate.

**Boundaries:** NO implementation; writable resume remains NOT AUTHORIZED; the committed non-resume guard
fully in force; no guardrail change; paid activation BLOCKED; PSRR NOT TRIGGERED; DEPLOYMENT NOT
AUTHORIZED; legal/tax registers OPEN; no provider/commercial decision. `OWNER_DECISION_REGISTER.md`
UNCHANGED. Authoritative as CONTRACT only if/when this exact candidate is merged and post-merge verified.
Next required step: **Independent External Review of this exact SHA + bundle**.

**Immediately prior (P10-PC2 COLD-LOAD DELIVERABLE FIDELITY — candidate `4218ed0b…` Owner-accepted at
that exact SHA and MERGED via PR #533, tip `aed5cb79f53e47c5e36e0fce6228288bfae8c014`; now
AUTHORITATIVE; retained as history):** Base: `edae7f30cf512773ab06022376d0ddc7011570a9` (PR #532 merge —
P10-UG1 Universal Core
Guardrail & Smoke Framework, authoritative; independently re-verified: parents `da4e7a47…` /
`c12671ee…`, merge tree `52a43240…` equal to the accepted candidate tree, empty candidate→merge diff).
Executed under the Owner's second Product Completion Reconstruction directive.

**Objective.** Make the deliverable — the product's primary output — truthful after a restart. BEFORE
(live-evidenced): a direct deliverable bookmark to a saved project redirected away, and the rehydrated
cold deliverable was FALSE in ten sections (claimed the problem was never established, HIGH Level-0 risk,
zero gaps/requirements/assumptions, lost prototype plan). AFTER: `show_deliverable` cold-loads via the
existing `_cold_load_entry` and assembles the package from the Level-1 deterministic READ-ONLY
reconstruction — the cold package equals the pre-restart live package modulo the wall-clock stamp
(STRONG test-pinned parity) — under the exact authorized claim banner (EN/AR; UI_B_SESSION_041/042),
fail-closed on every failure path. Canonical extension only: `_reconstruct` extraction (verbatim; the
merged `reconstruct_review_state` review is byte-identical, test-pinned) + additive
`reconstruct_readonly_state` returning the frozen review+state pair with binding read-only obligations +
VERBATIM restoration of the durably persisted interaction ledger (persisted `AssertionRecord`s, `rec_N`
preserved; no re-derivation; non-durable non-answer dispositions honestly not synthesized). Writable
continuation remains OUT (HIGH-VALUE BUT REQUIRES OWNER CONTRACT; guard intact and test-pinned).

**Evidence.** Baseline universal smoke PASS (9.1s) and post-implementation smoke PASS (6.0s; zero
observations; no guard touched). Honest RED 7/10 at base; GREEN 10/10; mutations m1 (drop ledger
restore → parity test dies) and m2 (suppress banner → EN+AR claim tests die), both reverted; real user
path verified live (direct cold bookmark → 200 truthful report, EN+AR banners); targeted regression 192
passed; full suite 2929 passed / 3 skipped / 1 xfailed / 0 failures (prior 2919 + 10 new).

**Boundaries:** no resume; no progression/schema change; no Guardrail change; paid activation BLOCKED;
PSRR NOT TRIGGERED; DEPLOYMENT NOT AUTHORIZED; legal/tax registers OPEN; no provider/commercial decision.
`OWNER_DECISION_REGISTER.md` UNCHANGED. Review tier: LEVEL 2 / DEPTH 2 (LEAN protocol §4). Authoritative
ONLY if/when this exact candidate is merged and post-merge verified. Next required step: **Independent
External Review of this exact SHA + bundle**.

**Immediately prior (P10-UG1 UNIVERSAL CORE GUARDRAIL & SMOKE FRAMEWORK — candidate `c12671ee…`
Owner-accepted at that exact SHA and MERGED via PR #532, tip
`edae7f30cf512773ab06022376d0ddc7011570a9`; now AUTHORITATIVE; retained as history):** Base:
`da4e7a474df7c245e69f1f8e529f04abf5e60444` (PR #531 merge — P10-PC1
user-visible reconstructed review state, authoritative; independently re-verified: parents `f0843878…` /
`eb196210…`, merge tree `79beb341…` equal to the accepted candidate tree, empty candidate→merge diff).

**Objective.** One durable, repository-enforced universal safety layer for ALL future candidates:
(a) `tests/universal_guardrail_manifest.py` — machine-checkable inventory of 17 guards (16 BLOCKING
UG-CORE-01…15 + UG-META-01; 1 OBSERVATION UG-OBS-01) composing EXISTING canonical tests by node id (zero
duplication; zero existing tests modified or moved); (b) `scripts/run_universal_smoke.py` — the one
canonical command with inventory-integrity collect check (missing canonical test = always BLOCK),
blocking semantics (failure/error/skip = BLOCK with guard/invariant/owner/remedy attribution),
observation semantics (reported, never blocks), and the standardized verdict
`UNIVERSAL GUARDRAIL SMOKE: PASS` / `: BLOCK` (PASS means ONLY: CORE INVARIANTS PRESERVED UNDER THIS
SUITE — never secure/production-ready/legally-compliant/PSRR-complete/deployment-approved/bug-free);
(c) `docs/governance/INVENTORAI_UNIVERSAL_CORE_GUARDRAIL_SMOKE_STANDARD.md` — the governance standard
(categories, extension process, review escalation subordinate to LEAN protocol §4/§5, prohibited
interpretations, relationships); (d) `tests/test_p10_ug1_universal_guardrail_framework.py` — 9 framework
guards incl. the PINNED blocking inventory (self-protection: guard removal/downgrade fails the governed
full suite) and hermetic runner-semantics tests. Review-tier truth recorded: LEVEL-1/DEPTH-2 independent
review stays mandatory; DEPTH-3 lighter path already exists in the standing protocol; any re-tiering is
PROPOSED FUTURE REVIEW-TIER AMENDMENT: OWNER DECISION REQUIRED — nothing weakened here.

**Evidence.** RED 9/9 at base + three grep-proven framework gaps; GREEN 9/9; smoke 68+1 canonical test
items in 4.8–7.2s (≈2.4% of the 2919-test suite; strict subset); probes P1 (real violation → BLOCK with
correct attribution), P2 (observation failure → PASS, no false BLOCK), P3 (guard deletion → pinned
inventory fails the suite); full suite 2919 passed / 3 skipped / 1 xfailed / 0 failures (prior 2910 + 9
new).

**Boundaries:** smoke PASS has no release semantics; paid activation BLOCKED; PSRR NOT TRIGGERED;
DEPLOYMENT NOT AUTHORIZED; legal/tax registers OPEN; no provider/commercial decision; no new domain
activation; no next product capability. `OWNER_DECISION_REGISTER.md` UNCHANGED. Authoritative ONLY
if/when this exact candidate is merged and post-merge verified. Next required step: **Independent
External Review of this exact SHA + bundle**.

**Immediately prior (P10-PC1 USER-VISIBLE RECONSTRUCTED REVIEW STATE — candidate `eb196210…`
Owner-accepted at that exact SHA and MERGED via PR #531, tip
`da4e7a474df7c245e69f1f8e529f04abf5e60444`; now AUTHORITATIVE; retained as history):** Base:
`f0843878794ae9c0f4647cadf8fa8a323ea4af9d` (PR #530 merge —
P10-DBT1 Phase-9 registered-debt remediation, authoritative; independently re-verified: parents
`8626a3e5…` / `41bf30c7…`, merge tree `69c0efea…` equal to the accepted candidate tree, empty
candidate→merge diff). Executed under the Owner's Product Completion Reconstruction directive (one bounded
product gate; advisers still not engaged; their items truthfully OPEN/DEFERRED).

**Objective.** Surface the merged-but-invisible P4-2 Level-1 deterministic READ-ONLY reconstruction
(`engine.session_reconstruction.reconstruct_review_state` — merged PR #369 with "no UI" as that gate's
recorded boundary and an exact authorized product claim; ZERO production call sites before this gate) on
the cold-loaded session page. BEFORE: after any server restart a saved project rendered a FALSE display
(generic domain label, reset level-0 maturity, no gaps, no question) plus an answer form whose every
submission failed with a "try again" message. AFTER: the page renders the TRUE reconstructed review state —
Tier-1 domain label (display-only from the persisted confirmed domain; `state.domain` stays absent and the
committed P4-1b-2a non-resume guard is preserved and STRENGTHENED), true maturity label/progress, localized
open gaps, the read-only current question, and the accepted-answer count — under the EXACT authorized claim
("… This is not a resumed session."), bilingual EN/AR (ui_text keys UI_B_SESSION_041–046), with the
dead-end form suppressed and every failure path (Level-0 fallback, exceptions, store unavailability)
fail-closed to the prior page. Writable continuation remains OUT — the registered next product step
requiring its own Owner-authorized contract.

**Evidence.** Honest RED 7/10 at base; GREEN 10/10; mutations m1/m2/m3 each killed exactly the right tests
(reverted); real user-path dump EN + AR matched the live pre-restart state (maturity 1,
PHYSICAL_FEASIBILITY open, 3 answers replayed); one disclosed reconciliation
(`test_obs_b_restart_durability_new_context` now asserts the strengthened no-form/no-token cold page and
the unchanged forged-POST fail-closed guarantee); targeted session-surface regression 223 passed / 1 skipped; full
suite 2910 passed / 3 skipped / 1 xfailed / 0 failures (prior 2900 + 10 new).

**Boundaries:** paid activation BLOCKED; PSRR NOT TRIGGERED; DEPLOYMENT NOT AUTHORIZED; legal/tax registers
OPEN; no provider/commercial decision; no engine/schema change; no resume. `OWNER_DECISION_REGISTER.md`
UNCHANGED. Authoritative ONLY if/when this exact candidate is merged and post-merge verified. Next required
step: **Independent External Review of this exact SHA + bundle**.

**Immediately prior (P10-DBT1 PHASE-9 REGISTERED-DEBT REMEDIATION — candidate `41bf30c7…` Owner-accepted
at that exact SHA and MERGED via PR #530, tip `f0843878794ae9c0f4647cadf8fa8a323ea4af9d`; now
AUTHORITATIVE; retained as history):** Base: `8626a3e59b6efbd6d976143f23e5a7f3da26b096` (PR #529 merge —
P10-SEC4 error-echo bounding, authoritative; independently re-verified: parents `19fca422…` /
`5829dcb2…`, merge tree `7d88fd5c…` equal to the accepted candidate tree, empty candidate→merge diff).
Executed under the Owner's technical-continuation direction (advisers still not engaged; their items
truthfully OPEN/DEFERRED; unrelated technical work continues).

**Objective.** Remediate the post-Phase-9 debts registered in `PHASE_9_FORMAL_CLOSURE_RECORD.md` §5
(items 1, 2, 4, 5; item 3 excluded — separately dispositioned by `L10N_RH01_FORMAL_CLOSURE_RECORD.md`).
Preconditions verified live: Mechanical is really activated, so the registered stale claims are genuinely
false and the missing real-state tests are a live gap on an active user-facing domain. Delivered:
(§5(4)) the single REAL admission→Tier-1-render E2E chain test for Mechanical — no activation/session
doubles anywhere: real classification → real `/start` consent offer → real confirmed admission →
`state.domain == "mechanical"` → real session render of the Tier-1 EN label (AR absent per the
single-language rule; no raw-id leak; never mislabeled electronics); (§5(5)) the real-activation CLI
banner pin ("Electronics Electrical or Mechanical, Level 0-2" against the REAL state); (§5(1)) a
DOCSTRING-ONLY truth repair of `classify_domain` (AST proven identical modulo docstrings) with the three
byte-pin evidence anchors (i3/i4/i5) re-frozen under the disclosed-reconciliation convention; (§5(2)) the
four registered stale comments repaired to explicit historical framing (recorded verdicts preserved
verbatim; the tie-precedence file's self-contradiction fixed; `test_p6_1` forward-points to the real
chain). Five truth guards prevent regression, and one guard pins the §5 register itself untouched.
Residuals dispositioned this cycle: criticality rationale remains BLOCKED/DEFERRED; legacy ILT-002 routes
untouched; non-DW error surfaces swept — all fixed-copy, residual CLOSED, no SEC4 generalization.

**Evidence.** Honest RED split: 5 truth guards failed at base precisely against the stale text; 5
real-state pins gap-filling with mutation-proven honesty (m1 deactivate-mechanical and m2 corrupt-label
each kill the right tests; reverted). Touched + adjacent regression 263 passed; full suite 2900 passed /
3 skipped / 1 xfailed / 0 failures (prior 2890 + 10 new; zero regressions). Zero runtime-behavior diff
(docstring/comment/hash-pin/test changes only).

**Boundaries:** paid activation BLOCKED; PSRR NOT TRIGGERED; DEPLOYMENT NOT AUTHORIZED; legal/tax registers
OPEN (nothing here needed their answers); no provider/commercial decision. `OWNER_DECISION_REGISTER.md`
UNCHANGED. Authoritative ONLY if/when this exact candidate is merged and post-merge verified. Next required
step: **Independent External Review of this exact SHA + bundle**.

**Immediately prior (P10-SEC4 DECISION-WORKSPACE ENGINE-ERROR ECHO BOUNDING — candidate `5829dcb2…`
Owner-accepted at that exact SHA and MERGED via PR #529, tip
`8626a3e59b6efbd6d976143f23e5a7f3da26b096`; now AUTHORITATIVE; retained as history):** Base:
`19fca422d90a84baef2d312ac3b3a247bf41e3f4` (PR #528 merge —
P10-SEC3 free-text hardening, authoritative; independently re-verified: parents `e031ecdd…` /
`91e48c20…`, merge tree `0ce1ae8d…` equal to the accepted candidate tree, empty candidate→merge diff).
Executed under the Owner's technical-continuation direction (advisers still not engaged; their items
truthfully OPEN/DEFERRED; unrelated technical work continues).

**Objective.** Bound the USER-REFLECTED copy of deterministic engine diagnostics in the Decision Workspace
400 error convention. Confirmed base behavior (source + live probe): ~15 `DecisionError` sites in
`engine/decision_workspace.py` legitimately `%r`-echo the offending enum/id value; those fields are
user-controlled and deliberately NOT free-text-guarded (ids/enums, not content), so a pathological value up
to the 128 KiB transport bound was reflected VERBATIM into the 400 page (autoescaped — no markup executes,
proven — but a 50,000-char probe produced a 62 KB reflected error page). Fix: web-layer ONLY — one helper
`_dw_bounded_error(prefix, exc)` (`_DW_ERROR_ECHO_BOUND` = 300 chars + explicit " … [diagnostic truncated]"
marker, never silent) replacing the seven `"<X> rejected: %s" % exc` call sites. Engine seam untouched:
exception messages remain byte-complete (test-pinned); short legitimate diagnostics render verbatim
(test-pinned); autoescape, P10-SEC3 guard precedence, and P10-SEC1 headers preserved (test-pinned).
Reviewer residuals dispositioned: criticality rationale remains BLOCKED/DEFERRED (honest RED/GREEN needs
the heavyweight ws1-completed flow — disproportionate); legacy ILT-002 start routes confirmed from source
as deliberately preserved legacy/evidence-compat surfaces — NOT modified.

**Evidence.** RED 6/11 failed at base precisely for the absent bounding (5 deliberate preservation guards
green; one test-order expectation corrected pre-freeze — the engine validates `gap_id` first, so the junk
belongs in the first-checked field). GREEN 11/11; SEC1+SEC2+SEC3+SEC4 combined 59 passed; full suite 2890
passed / 3 skipped / 1 xfailed / 0 failures (prior 2879 + 11 new; zero regressions). Zero engine/schema/
dependency/template diff; checklist unchanged (no row overclaimed; RL-A6 remains truthful).

**Boundaries:** paid activation BLOCKED; PSRR NOT TRIGGERED; DEPLOYMENT NOT AUTHORIZED; legal/tax registers
OPEN (nothing here needed their answers); no provider/commercial decision. `OWNER_DECISION_REGISTER.md`
UNCHANGED. Authoritative ONLY if/when this exact candidate is merged and post-merge verified. Next required
step: **Independent External Review of this exact SHA + bundle**.

**Immediately prior (P10-SEC3 DECISION-WORKSPACE FREE-TEXT HARDENING RESIDUAL EXTENSION — candidate
`91e48c20…` Owner-accepted at that exact SHA and MERGED via PR #528, tip
`19fca422d90a84baef2d312ac3b3a247bf41e3f4`; now AUTHORITATIVE; retained as history):** Base:
`e031ecddb390577988041fa2f3214b78fbf34211` (PR #527 merge — P10-RL1 release-readiness checklist,
authoritative; independently re-verified: parents `b1a0196a…` / `01650517…`, merge tree `4f3646d2…` equal
to the accepted candidate tree, empty candidate→merge diff). Executed under the Owner's
technical-continuation direction: development continues where repository truth permits; adviser-dependent
items stay truthfully OPEN/DEFERRED.

**Objective.** Close the largest documented P10-SEC2 residual (authoritative checklist row RL-A6:
"criticality/decision-workspace free text are transport-bounded ONLY") by extending the CANONICAL P10-SEC2
guard — no new subsystem, no redesign: one helper `_dw_free_text_reject` reusing `_free_text_error`
(20,000-char cap + NUL rejection; explicit rejection, never truncation/stripping; Arabic/Unicode/multiline
untouched) applied to ALL SEVEN Decision Workspace POST surfaces (`/input` text+provenance; `/constraint`
text+provenance; `/gap` rationale; `/evidence` text/provenance/method/source_label/evidence_version/
limitations; `/gap-assessment` rationale+resolution_rationale; `/preference` rationale; `/candidate`
disposition_reason+disposition_basis), using the route family's EXISTING error convention
(`_render_decision_workspace(..., status=400)`), running AFTER the non-enumerating ownership denial and
BEFORE any engine call (zero mutation on rejection; engine semantics unmasked). Remaining residuals stay
truthfully documented: the legacy fixed-domain ILT-002 start routes and the criticality rationale remain
transport-bounded ONLY (RL-A6 row updated accordingly; still NOT "all inputs fully hardened").

**Evidence.** RED 10/15 failed at base for the absent guard (5 deliberate preservation guards green; two
harness realities corrected pre-implementation: seeded DecisionRecord inputs → delta-based mutation checks;
engine id/enum 400s → guard-message assertions so every RED fails for the right reason and guard precedence
is proven). GREEN 15/15. Checklist/SEC2/RL1 invariant suites green post-sync. Full suite green (exact
counts in the roadmap entry). Zero schema/dependency diff; no legal/tax/commercial/provider assumption
encoded.

**Boundaries:** paid activation BLOCKED; PSRR NOT TRIGGERED; DEPLOYMENT NOT AUTHORIZED; legal/tax registers
OPEN (deferred pending advisers — this gate needs none of their answers). `OWNER_DECISION_REGISTER.md`
UNCHANGED. MERGED via PR #528 (tip `19fca422…`) and post-merge verified — AUTHORITATIVE.

**Immediately prior (P10-RL1 RELEASE-READINESS CHECKLIST FOUNDATION — candidate `01650517…` Owner-accepted
at that exact SHA and MERGED via PR #527, tip `e031ecddb390577988041fa2f3214b78fbf34211`; now
AUTHORITATIVE; retained as history; RUNTIME CODE REQUIRED: NO):** Base:
`b1a0196aaf1f6892996c618c69cb341872ecaf52` (PR #526 merge — P10-DEP1 dependency-audit foundation,
authoritative; independently re-verified: parents `8563320b…` / `ec0795d9…`, merge tree `96cf5857…` equal
to the accepted candidate tree, empty candidate→merge diff).

**Objective.** The smallest deterministic release-readiness TRUTH SURFACE:
`docs/governance/PHASE_10_RELEASE_READINESS_CHECKLIST.md` — 58 source-traced readiness items (RL-A1…RL-G8)
across technical/operational/security-infrastructure/legal-privacy/commercial-tax/provider/gates, using
the bounded status vocabulary (`IMPLEMENTED LOCAL FOUNDATION` / `OPEN` / `DEFERRED — EXTERNAL ADVISER
REQUIRED` / `PROVIDER-DEPENDENT` / `COMMERCIAL DECISION REQUIRED` / `PSRR-TIME` / `DEPLOYMENT-TIME` /
`BLOCKED`, each precisely defined; no vague statuses). Banner (binding): `RELEASE READINESS CHECKLIST
FOUNDATION ≠ RELEASE APPROVAL`; PSRR GO/NO-GO remains a separate future gate. Canonical-owner check
performed: NO prior release/launch/go-live checklist existed; the artifact is a truth INDEX that owns no
decision (PSRR scope/trigger/GO → PSRR registration; obligation inventory → P10-C §4 + remediation plan;
authorization gates → ODR `OD-P`/`D-PSRR-01`/`D-P8-PL-01`; foundations → their merged gate records).
All seven local foundations (BR1/OB1/SEC1/IR1/DOC1/SEC2/DEP1) verified LIVE at this base (files, runtime
markers, and the PR #520–#526 first-parent merge chain) — never copied from summaries. Load-bearing
nuances preserved and TEST-ENFORCED: foundations ≠ production readiness; SEC2 residual gaps visible
(legacy ILT-002 routes + criticality/decision-workspace text transport-bounded ONLY; never "all inputs
fully hardened"); DEP1 point-in-time-only + no continuous scanning + no auto-remediation + the
`tests/requirements-draft-l2.txt` TEST-ONLY declaration (playwright pins) recorded as NOT covered by the
P10-DEP1 audit run; local backup ≠ production backup; local observability ≠ production monitoring;
internal IR ≠ customer support/SLAs; HSTS deferred; PSRR registered ≠ triggered ≠ executed ≠ GO (this
checklist triggers nothing); deployment authorization distinct; paid activation BLOCKED; adviser-dependent
items never marked implemented; provider items all NOT SELECTED (no provider invented).

**Validation.** `tests/test_p10_rl1_release_readiness_checklist.py` — 10 structural invariants (single
canonical artifact; not-an-approval banner; bounded status vocabulary with no vague statuses; per-row
source traceability across all 58 rows; PSRR four-state distinction + untriggered; deployment/paid-
activation/closure-NO lines; no readiness overclaims; SEC2/DEP1 nuances; negation-aware provider check).
Structural RED: 10/10 fail with the checklist absent; GREEN 10/10 (two pre-freeze precision fixes: two
rows' "same"-shorthand sources made explicit — the doc fixed to satisfy the invariant; one test regex made
negation-aware for "NOT SELECTED"). Full suite green (exact counts in the roadmap entry). MERGED via PR
#527 (tip `e031ecdd…`) and post-merge verified — AUTHORITATIVE.

**Phase-10 closure assessment:** `PHASE 10 CLOSURE ELIGIBLE NOW: NO` (source-backed blockers indexed in
the checklist's blocking summary). **Boundaries:** zero runtime/schema/dependency diff; no legal/tax
conclusion; no provider selection; no commercial policy; PAID ACTIVATION AUTHORIZED: NO; PSRR TRIGGERED:
NO; DEPLOYMENT AUTHORIZED: NO. `OWNER_DECISION_REGISTER.md` UNCHANGED. Authoritative ONLY if/when this
exact candidate is merged and post-merge verified. Next required step: **Independent External Review of
this exact SHA + bundle**.

**Immediately prior (P10-DEP1 LOCAL DEPENDENCY-AUDIT FOUNDATION — candidate `ec0795d9…` Owner-accepted at
that exact SHA and MERGED via PR #526, tip `b1a0196aaf1f6892996c618c69cb341872ecaf52`; now AUTHORITATIVE;
retained as history):** Base: `8563320b626b8590f10cbf252c9eba0a03b6fbd6` (PR #525 merge — P10-SEC2 input
hardening, authoritative; independently re-verified: parents `9d6bf3d9…` / `516128b7…`, merge tree
`c3626080…` equal to the accepted candidate tree, empty candidate→merge diff).

**Objective.** The smallest provider-neutral LOCAL dependency-audit foundation. Dependency-model truth
(verified at base): `requirements.txt` is the SINGLE authoritative dependency source (pinned Flask==3.1.3
+ pytest==9.1.1, runtime+test, sha256 `e0707b64…`); no pyproject/lockfiles/Pipfile/setup/Docker/workflow/
pip-install scripts exist; the Codespace's 46 globally installed packages are ENVIRONMENT packages, not
project dependencies. Selected mechanism: **pip-audit** (local CLI over OSV/PyPI advisories — local
execution, machine-readable output, non-zero exit on findings/errors, PSRR-reusable, zero runtime
coupling; no hosted vendor). Delivered: `scripts/run_dependency_audit.py` (repo-root resolution from any
cwd; evidence header with repo SHA + input SHA-256 + UTC timestamp + tool identity; clear `TOOL MISSING`
exit 3; missing-input exit 2; tool exit status preserved VERBATIM — findings and advisory-network failures
never converted into a clean PASS; no secret echo; no remediation capability) + 9 deterministic tooling
tests (offline fake-tool simulation via the documented `INVENTORAI_AUDIT_TOOL_MODULE` tooling seam; RED
8/9 with the wrapper absent — the passer is the already-true no-runtime-contamination guard; GREEN 9/9) +
the immutable POINT-IN-TIME evidence record
(`docs/governance/evidence/phase10_p10_dep1/P10_DEP1_POINT_IN_TIME_AUDIT_EVIDENCE.md`).

**Live audit (network AVAILABLE at execution):** pip-audit 2.10.1 against `requirements.txt` @ base SHA —
exit 0; 2 direct + 9 transitive = 11 packages scanned; findings 0 → `POINT-IN-TIME AUDIT: ZERO KNOWN
FINDINGS AT EXECUTION TIME` (2026-08-19T21:24:47Z; NEVER "secure", NEVER permanent). `pip check`: "No
broken requirements found." `DEPENDENCY REMEDIATION REQUIRED: NO` at this instant. pip-audit installed as
ENVIRONMENT TOOLING only — not added to `requirements.txt`, imported by no application module
(test-enforced).

**Boundaries (binding):** no auto-remediation/upgrade/pin change; no hosted vendor/continuous-scanning/CI-
enforcement/Dependabot/Snyk claim; `LOCAL AUDIT FOUNDATION: IMPLEMENTED` ≠ `FORMAL PRODUCTION
DEPENDENCY/VULNERABILITY REVIEW: PSRR-TIME` (items 12–13 unsatisfied); zero runtime/schema diff; PAID
ACTIVATION AUTHORIZED: NO; PSRR TRIGGERED: NO; DEPLOYMENT AUTHORIZED: NO. `OWNER_DECISION_REGISTER.md`
UNCHANGED. MERGED via PR #526 (tip `b1a0196a…`) and post-merge verified — AUTHORITATIVE.

**Immediately prior (P10-SEC2 BOUNDED INPUT-HARDENING INCREMENT — candidate `516128b7…` Owner-accepted at
that exact SHA and MERGED via PR #525, tip `8563320b626b8590f10cbf252c9eba0a03b6fbd6`; now AUTHORITATIVE;
retained as history):** Base: `9d6bf3d9753585f3f825f6b30b045657bdfc8195` (PR #524 merge — P10-DOC1 truth
repair, authoritative; independently re-verified: parents `18165123…` / `ed7c5405…`, merge tree
`b2fa5498…` equal to the accepted candidate tree, empty candidate→merge diff).

**Objective.** The smallest input-hardening protecting against unbounded/pathological input, grounded in a
full input-surface inventory: (A) ONE transport bound — `MAX_CONTENT_LENGTH` = 128 KiB (standard Werkzeug
413; covers a worst-case 4-byte-UTF-8 at-limit free-text field ≈ 80 KiB plus form overhead) applying to
every surface; (B) ONE semantic free-text bound — `MAX_FREE_TEXT_CHARS` = 20,000 characters (justified
from PRESENT product behavior: an order of magnitude above every legitimate description in repository
evidence; deliberately NOT the stale documented 10,000 figure) plus NUL-byte REJECTION, on the two primary
free-text surfaces only: `/start` idea text (400 via this surface's existing form-error convention,
bilingual EN/AR fixed copy, no input echo) and `/session/<sid>` answer/action text (400 via that route's
existing plain-text-tuple convention), enforced BEFORE any classification, session creation, or durable
write. `NULL BYTE POLICY: REJECT` (silent stripping could change user intent). NO silent truncation, NO
general control-character sanitizer, NO ASCII-only rule — Arabic/Unicode/multiline/punctuation pass
untouched (test-proven end-to-end verbatim storage). Legacy fixed-domain ILT-002 start routes remain
transport-bounded only (historical evidence surfaces, behavior preserved). Auth fields (email/password/
tokens) deliberately unchanged (normalized/hashed/rate-limited already; MIN_PASSWORD_LENGTH intact);
success criteria already capped (1000); API v1 is GET-only → JSON-body hardening JUSTIFIED N/A; no file
upload exists.

**Evidence.** RED 9/15 failed at base for the absent protections (6 preservation guards deliberately
green; one harness fix — a false-pass from an unrecognized action name — corrected before implementation).
GREEN 15/15. Manual probes: normal/at-limit 302; over-limit/NUL 400 with headers, EN and AR localized, no
echo; 413 with headers; HSTS still absent. Relevant regression 288 passed. Full suite green (exact counts
in the roadmap entry). `docs/SECURITY_ARCHITECTURE.md` truthfully updated (bounds = robustness controls
only; NOT WAF/DoS-prevention/proxy-limit/OWASP/complete-abuse-prevention; PSRR item 1 still reassesses).

**Boundaries (binding):** no auth/CSRF/session/export/deactivation semantic change (test-proven); P10-SEC1
headers on all rejections incl. 413, values unchanged, HSTS still deferred; P10-OB1/BR1/IR1/DOC1
untouched; no new log events, no raw-input logging; no dependency/provider/schema change. PAID ACTIVATION
AUTHORIZED: NO; PSRR TRIGGERED: NO; DEPLOYMENT AUTHORIZED: NO. `OWNER_DECISION_REGISTER.md` UNCHANGED.
MERGED via PR #525 (tip `8563320b…`) and post-merge verified — AUTHORITATIVE.

**Immediately prior (P10-DOC1 DATA-RETENTION & COST-GOVERNANCE TRUTH REPAIR — candidate `ed7c5405…`
Owner-accepted at that exact SHA and MERGED via PR #524, tip `9d6bf3d9753585f3f825f6b30b045657bdfc8195`;
now AUTHORITATIVE; retained as history; RUNTIME CODE REQUIRED: NO):** Base:
`1816512326bae32f072c3816b78ab56fbb657b2e` (PR #523 merge — P10-IR1 incident-response foundation,
authoritative; independently re-verified: parents `ee933718…` / `fb7a0313…`, merge tree `a4378a7a…` equal
to the accepted candidate tree, empty candidate→merge diff).

**Objective.** Repair the last two P10-C §9-registered stale documents to current truth (both verified
byte-unchanged since their original generation commit `79c9c5e`):
`docs/DATA_RETENTION_POLICY.md` — current data inventory (durable SQLite accounts/tokens/credentials/
projects/records/audit + in-memory live progression state + client-only localStorage 7-day TTL + stream-only
operational logs); what actually happens (indefinite durable retention, deactivation-tombstone-only exit,
the sole automatic deletion = expired auth-rate-limit cleanup, local backups inherit everything, no
retention/erasure lifecycle); superseded claims kept as labeled history ("No PII collected" — accounts
exist and the GDPR/PDPL-review trigger FIRED, now commissioned as OPEN LQ-04…LQ-11; "in-memory only";
"Anthropic API receives descriptions" — NO live external transfer, `AI_ADVISORY_ENABLED = False`); and the
banner `RETENTION POLICY SUBSTANCE: OPEN — EXTERNAL LEGAL/TAX INPUT REQUIRED` with NO invented duration.
`docs/COST_GOVERNANCE_PLAN.md` — current cost reality (NO live paid usage; dormant disabled AI path with
`max_tokens: 150` and no API key; no kill switch / spending ceiling / cost accumulator / iteration hard
stop — each prior claim individually labeled NOT IMPLEMENTED; commercial tables = scaffolding, no live
billing; paid activation BLOCKED `D-P8-PL-01 class C`); historical controls retained as
PLANNED / NOT IMPLEMENTED design input; provider costs PROVIDER-DEPENDENT/deferred.

**Validation.** `tests/test_p10_doc1_retention_cost_truth.py` (11 doc-invariant checks, whitespace-
normalized; superseded claims must stay labeled; no prescriptive retention duration; retention substance
OPEN; controls never claimed active; doc truth tied to source truth — kill-switch absence, disabled AI
path, rate-limit-only deletion, real 7-day TTL). Structural RED: 9/11 fail against the unrepaired
documents; GREEN 11/11. Full suite green (exact counts in the roadmap entry).

**Boundaries (binding):** no retention/deletion/erasure rule created; no legal/tax conclusion; no legal
duration; zero runtime/schema diff; deactivation ≠ erasure preserved; OD-DR1/OD-DR2 unaltered; PAID
ACTIVATION AUTHORIZED: NO; PSRR TRIGGERED: NO; DEPLOYMENT AUTHORIZED: NO. `OWNER_DECISION_REGISTER.md`
UNCHANGED. MERGED via PR #524 (tip `9d6bf3d9…`) and post-merge verified — AUTHORITATIVE.

**Immediately prior (P10-IR1 TECHNICAL INCIDENT RESPONSE FOUNDATION — candidate `fb7a0313…`
Owner-accepted at that exact SHA and MERGED via PR #523, tip `1816512326bae32f072c3816b78ab56fbb657b2e`;
now AUTHORITATIVE; retained as history; RUNTIME CODE REQUIRED: NO):** Base:
`ee93371808803c488eeba59bf83fcfbb20fccc2a` (PR #522 merge — P10-SEC1 security headers, authoritative;
independently re-verified: parents `9e46e75b…` / `cb950881…`, merge tree `98076d4e…` equal to the accepted
candidate tree, empty candidate→merge diff).

**Objective.** The smallest provider-neutral INTERNAL technical incident-response foundation:
`docs/governance/PHASE_10_INTERNAL_TECHNICAL_INCIDENT_RESPONSE_RUNBOOK.md` — narrow incident definition;
SEV-1…SEV-4 severity model (each with triggers/examples/action/escalation/closure; qualitative urgency
only — no SLA, no response-time clock, no customer commitment); truthful role semantics (Owner + governed
execution agents; no invented staff); the flow `DETECT → CLASSIFY → CONTAIN → PRESERVE EVIDENCE → DIAGNOSE
→ RECOVER → VERIFY → CLOSE / ESCALATE`; real-signals-only detection (P10-OB1 `/health` + logging seam,
audit tables, tests, human reports — with an explicit does-NOT-exist list: no metrics/alerts/paging/
external monitoring); existing-mechanism containment (epoch revocation, status gating, SHA/state
preservation, DB-copy isolation — NO new kill switch); database path tied to authoritative P10-BR1
(isolate → validate → restore-to-new-target → parity → Owner-authorized repoint); availability path tied
to P10-OB1 (truthful ok/uninitialized/error semantics; data-minimization holds during incidents); security
path tied to P10-SEC1 + existing auth controls; the MANDATORY legal/privacy boundary (`ESCALATE TO OWNER +
QUALIFIED EXTERNAL COUNSEL WHEN AVAILABLE`; technical team does NOT determine legal applicability; no
legal deadline; no automatic notification; LQ register stays OPEN); `CUSTOMER COMMUNICATION:
OWNER-APPROVED ONLY` (no final templates, no promises); minimal evidence-record template + `IR-YYYYMMDD-NN`
IDs (file-based, no new table/schema); closure criteria (technical closure ≠ legal closure) and reopen
rule; IR/DR boundary (IR coordinates, `DISASTER_RECOVERY_PLAN.md` recovers — no duplication). Structural
invariants enforced by `tests/test_p10_ir1_incident_runbook_structure.py` (9 checks; structural RED: 9/9
fail with the runbook absent; GREEN 9/9).

**Truth classification:** `INTERNAL TECHNICAL INCIDENT RESPONSE: IMPLEMENTED` (internal foundation) —
while `CUSTOMER-FACING SUPPORT MODEL: OPEN` and `LEGAL/PRIVACY INCIDENT NOTICE RULES: OPEN — EXTERNAL
COUNSEL REQUIRED` (never collapsed). PSRR item 27 is informed, not satisfied. PAID ACTIVATION AUTHORIZED:
NO; PSRR TRIGGERED: NO; DEPLOYMENT AUTHORIZED: NO. `OWNER_DECISION_REGISTER.md` UNCHANGED. MERGED via PR
#523 (tip `18165123…`) and post-merge verified — AUTHORITATIVE.

**Immediately prior (P10-SEC1 SECURITY HEADERS & PROVIDER-NEUTRAL HARDENING INCREMENT — candidate
`cb950881…` Owner-accepted at that exact SHA and MERGED via PR #522, tip
`ee93371808803c488eeba59bf83fcfbb20fccc2a`; now AUTHORITATIVE; retained as history):** Base:
`9e46e75b283a7a451bd19106861a7ac3de01a8dc` (PR #521 merge — P10-OB1 observability foundation,
authoritative; independently re-verified: parents `571cede0…` / `9048c132…`, merge tree `2b501cec…` equal
to the accepted candidate tree, empty candidate→merge diff).

**Objective.** One centralized provider-neutral response-hardening seam (`after_request`, setdefault
semantics) applying to every response: the smallest inventory-supported CSP (`default-src 'none';
script-src 'self'; style-src 'unsafe-inline'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'`
— no `'unsafe-eval'`, no wildcard/host/scheme sources, no reporting endpoint), `X-Content-Type-Options:
nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`. **HSTS DEFERRED —
REQUIRES TRUSTED PRODUCTION HTTPS CONTEXT** (no TLS termination/trusted-proxy truth exists; no forwarded-
header trust added; no ProxyFix). Grounded in the mandatory pre-RED CSP compatibility inventory: zero
inline script bodies/handlers; only same-origin static `local_draft.js`; inline-styles-only styling (the
sole, narrowly justified `'unsafe-inline'`, style-src only); zero external origins/fetch/frames/base/
data:/javascript: URLs; same-origin form actions.

**Owner authorization:** explicit, verbatim, scoped to `RECONSTRUCTION → CSP INVENTORY → RED → IMPLEMENT →
GREEN → REGRESSION → FULL SUITE → FREEZE → TRUTH SWEEP → CREATOR GRILL → BUNDLE`; no
push/PR/merge/deploy/PSRR. **Allowed paths:** the `_SECURITY_HEADERS` seam in `web/app.py`,
`tests/test_p10_sec1_security_headers.py` (new), `docs/SECURITY_ARCHITECTURE.md` (truth-labeling), and the
three active governance surfaces. **Forbidden:** everything else — zero schema diff; zero change to
auth/session/CSRF semantics, observability, backup/restore, payment/legal/tax, deployment, providers;
zero template/static changes were needed (the inventory proved none required).

**Boundaries (binding):** headers ≠ security review, ≠ PSRR execution (item 11 remains future PSRR
verification), ≠ TLS posture, ≠ compliance claim. PAID ACTIVATION AUTHORIZED: NO; PSRR TRIGGERED: NO;
DEPLOYMENT AUTHORIZED: NO. `OWNER_DECISION_REGISTER.md` UNCHANGED. MERGED via PR #522 (tip `ee933718…`)
and post-merge verified — AUTHORITATIVE.

**Immediately prior (P10-OB1 PROVIDER-NEUTRAL OBSERVABILITY FOUNDATION INCREMENT — candidate `9048c132…`
Owner-accepted at that exact SHA and MERGED via PR #521, tip `9e46e75b283a7a451bd19106861a7ac3de01a8dc`;
now AUTHORITATIVE; retained as history):** Base: `571cede0fdaec297319c95ba5c6042733767f811` (PR #520 merge
— P10-BR1 backup/restore increment, authoritative; independently re-verified: parents `56ba1044…` /
`5736150…`, merge tree `b9c3dbf5…` equal to the accepted candidate tree, empty candidate→merge diff).

**Objective.** The smallest provider-neutral observability foundation: ONE truthful health/readiness surface
(`GET /health` — deterministic, unauthenticated, session-free, side-effect-free, data-minimized; 200 with
`database: ok|uninitialized`, 503 only on real local dependency failure; probe never creates a
file/schema/row) plus the smallest structured operational-logging seam (`web/observability.py`, stdlib
`logging` only: JSON lines, strict field ALLOWLIST `component/outcome/error_class/detail_code/count/
duration_ms`, per-field value grammars rejecting emails, free-form text, paths, IPs, session identifiers,
and common secret shapes; `emit()` never raises). Selected by the Owner from the P10-RV1 revalidation (the
P10-C §4 monitoring/observability row was NOT STARTED).

**Owner authorization:** explicit, verbatim, scoped to `RECONSTRUCTION → RED → IMPLEMENT → GREEN →
REGRESSION → FULL SUITE → FREEZE → TRUTH SWEEP → CREATOR GRILL → BUNDLE`; no push/PR/merge/deploy/PSRR.
**Allowed paths:** `web/observability.py` (new), the `/health` route + `_database_health()` probe in
`web/app.py`, `tests/test_p10_ob1_observability_foundation.py` (new), `docs/OBSERVABILITY_ARCHITECTURE.md`
(truth-labeling), and the three active governance surfaces. **Forbidden:** everything else — zero
schema/migration diff; zero change to payment/subscription/account/deactivation/export/legal/tax semantics,
backup/restore (P10-BR1), or security headers (P10-SEC1 remains a separate future gate).

**Data-minimization boundary (load-bearing, test-proven):** no IP, user-agent, device/network metadata,
geography, email, user/project content, password, token, session ID, or API credential is newly collected,
emitted, or exposed; no analytics, behavioral tracking, third-party telemetry, or provider SDK; log
destination/retention/rotation/aggregation NOT decided. The durable audit tables remain the separate
security/commercial evidence layer — preserved, not duplicated.

**Truthful P10-C §4 classification after this gate:** monitoring/observability =
`PARTIAL — PROVIDER-NEUTRAL FOUNDATION IMPLEMENTED` (live production monitoring/alerting/dashboards still
absent and provider-dependent; PSRR items remain future verification). PAID ACTIVATION AUTHORIZED: NO; PSRR
TRIGGERED: NO; DEPLOYMENT AUTHORIZED: NO. `OWNER_DECISION_REGISTER.md` UNCHANGED. MERGED via PR #521 (tip
`9e46e75b…`) and post-merge verified — AUTHORITATIVE.

**Immediately prior (P10-BR1 DURABLE-DATABASE BACKUP & RESTORE DRILL INCREMENT — candidate `5736150…`
Owner-accepted at that exact SHA and MERGED via PR #520, tip `571cede0fdaec297319c95ba5c6042733767f811`; now
AUTHORITATIVE; retained as history):** Base: `56ba10446626af1d8c2e188b2f8982b1265a5078` (PR #519 merge —
P10-LT1 commissioning gate, authoritative; independently re-verified: parents `5dfc35e3…` / `aead7fcc…`,
merge tree `a694c08d…`, empty candidate→merge diff).

**Objective.** The smallest provider-neutral, filesystem-local, SQLite-consistent backup + restore +
validation + parity capability for the durable datastore (`INVENTORAI_DB_PATH`; all durable tables of both
stores — inventory derived live from `sqlite_master`, 15 at authoring, never hard-coded), plus one evidenced
local restore drill. Selected by the Owner from the P10-RV1 read-only technical revalidation (the
"backup/restore drills" P10-C §4 row was NOT STARTED and the durable DB had no recovery path).

**Owner authorization:** explicit, verbatim, scoped to `RECONSTRUCTION → RED → IMPLEMENT → GREEN → FOCUSED →
FULL SUITE → RESTORE DRILL → FREEZE → TRUTH SWEEP → CREATOR GRILL → BUNDLE`; no push/PR/merge/deploy.
**Allowed paths:** `engine/backup_service.py` (new), `tests/test_p10_br1_backup_restore.py` (new),
`docs/DISASTER_RECOVERY_PLAN.md` (bounded truth repair), the P10-BR1 drill evidence record, and the three
active governance surfaces. **Forbidden:** everything else — zero schema/migration diff; zero change to
account/export/deactivation/retention semantics, web UX, API behavior, payment/commercial logic.

**Delivered behavior (tested):** `backup_database` (SQLite online-backup API — never a raw live-file copy;
read-only source; fail-closed on missing/invalid source; no silent empty-DB creation; explicit guarded
overwrite; no partial output), `validate_sqlite_database` (`PRAGMA quick_check` + schema inventory,
fail-closed), `restore_database` (validated restore to a SEPARATE explicit target), `database_parity_report`
(schema + per-table row-count parity; names/counts only). 21 focused tests (RED-first), full suite green,
and a PASSED 12-point local restore drill
(`docs/governance/evidence/phase10_p10_br1/P10_BR1_RESTORE_DRILL_EVIDENCE.md`).

**Non-goals / boundaries (binding):** NO production backup scheduling, offsite/cloud backup, retention or
deletion policy (legal-gated; OD-DR1/OD-DR2 untouched), encryption redesign, provider/hosting selection,
monitoring, security headers, PSRR execution, or deployment. Local verified drill ≠ production backup
posture. External legal/tax registers remain OPEN (deferred pending adviser availability). PAID ACTIVATION
AUTHORIZED: NO; PSRR TRIGGERED: NO; DEPLOYMENT AUTHORIZED: NO. `OWNER_DECISION_REGISTER.md` UNCHANGED
(implementation authorization, not a new strategy decision). MERGED via PR #520 (tip `571cede0…`) and
post-merge verified — AUTHORITATIVE.

**Immediately prior (P10-LT1 EXTERNAL LEGAL & TAX INPUT COMMISSIONING GATE — accepted and MERGED via PR
#519, tip `56ba10446626af1d8c2e188b2f8982b1265a5078`; now AUTHORITATIVE; retained as history; commissions
questions, answers nothing; authorizes nothing):** Base:
`5dfc35e34bbfc9a8681d575a7e26613a5038c674` (PR #518 merge — OD-CJ1 acceptance candidate #3 `ec2ff7f0…`,
authoritative; independently re-verified: parents `b98561b8…` / `ec2ff7f0…`, merge tree `76b05623…` equal to
the accepted candidate tree, empty candidate→merge diff). Full detail:
`docs/governance/P10_LT1_EXTERNAL_LEGAL_TAX_INPUT_COMMISSIONING_GATE.md`.

**Purpose.** Operationalizes the Jurisdiction & Data-Rights gate §5 external-input register (not duplicated,
not closed): defines the 27-item external LEGAL question register (LQ-01…LQ-27), the 13-item TAX/ACCOUNTING
register (TQ-01…TQ-13), a fully cited repository-authoritative adviser fact pack, bounded adviser
qualifications (no firm/person selected), the mandatory 14-field structured answer format, the intake
protocol (`EXTERNAL RESPONSE → SOURCE VERIFICATION → INTERNAL MAPPING → OWNER REVIEW → GOVERNANCE CANDIDATE →
CREATOR GRILL → INDEPENDENT REVIEW → OWNER ACCEPTANCE`; advice = EVIDENCE/INPUT, never automatic authority),
and the conflict/supersession rule. **No question is answered; no regime is claimed applicable; no legal/tax
conclusion is made; no legal artifact is drafted.**

**Sync carried.** OD-CJ1 acceptance MERGED/AUTHORITATIVE via PR #518 (identity above, independently
re-verified; superseded candidates `7fe33ebb…`/`00e7f249…` preserved as evidence). All five gate-registered
decisions (OD-J1, OD-J2, OD-DR1, OD-DR2, OD-CJ1) are accepted and merged; a read-only remaining-obligations
reconstruction at this tip returned `PHASE 10 STATUS: OPEN` and selected P10-LT1 as the next smallest
sufficient governed step.

**Boundaries.** No legal-artifact drafting; no commercial-policy decisions (counsel-needed assumptions
register as OWNER INPUT REQUIRED); no payment/tax-provider, MoR, hosting, or region selection (OD-J2
delegated gate separate); PAID ACTIVATION AUTHORIZED: NO (`D-P8-PL-01 class C` unsatisfied by this gate);
PSRR TRIGGERED: NO; DEPLOYMENT AUTHORIZED: NO; P8C §5 / P8-I4 deferred registers open; OD decisions
unaltered. Governance-only; zero runtime/test diff; no auto-activated successor (P10-C §10). MERGED via PR
#519 (tip `56ba1044…`) and post-merge verified — AUTHORITATIVE.

**Immediately prior (OD-CJ1 acceptance — corrected candidate #3 `ec2ff7f0`, accepted and MERGED via PR #518,
tip `5dfc35e34bbfc9a8681d575a7e26613a5038c674`; now AUTHORITATIVE; retained as history):** Base:
`b98561b847884557cc90c7c6600644ae23abf4c5` (PR #517 merge — OD-DR2 acceptance,
authoritative; independently re-verified: parents `46756528…` / `a9b3aee2…`, merge tree `8654270e…` equal to
the accepted candidate tree). Full detail:
`docs/governance/evidence/phase10_owner_decisions/OD-CJ1_COMMERCIAL_JURISDICTION_TAX_SCOPE.md` and the new
OD-CJ1 section of `OWNER_DECISION_REGISTER.md`.

**OD-CJ1 — ACCEPTED AT STRATEGY LEVEL.** Records KUWAIT AS THE CURRENT INTENDED COMMERCIAL STARTING
JURISDICTION — a commercial starting-position intent fact only, for later external legal/tax analysis; the
tax-scope component remains DEFERRED pending external legal/tax determination + separate Owner authorization.
Kuwait ≠ final entity/incorporation/tax-nexus/VAT/MoR/invoicing/withholding answer. **Paid activation remains
BLOCKED / NOT AUTHORIZED under `D-P8-PL-01 class C`** — Phase-10 legal/readiness items, external legal/tax
input, payment/refund/subscription terms, `PSRR = GO/PASS` (`D-PSRR-01`), the separate Deployment Gate, and
Owner deployment authorization (`OD-P`) all remain independently required. External legal/tax register OPEN.
B2C + B2B commercial eligibility recorded (OD-J1 §2.3 cross-referenced, not duplicated); COMMERCIAL CUSTOMER
ELIGIBILITY ≠ ENTERPRISE FEATURE ACTIVATION — no enterprise/B2B feature, workflow, or pricing activated.
Recurring-subscription + automatic-collection direction only — every billing parameter except the USD
base currency undecided. EXISTING
P8-I4 boundary referenced (commercial domain → provider-neutral `PaymentProviderPort` → external provider) —
not created/renamed/duplicated/expanded; payment-provider, tax-provider, and Merchant-of-Record neutrality
preserved (no-foreclosure principles only — never build instructions); **USD decided as the initial/base commercial pricing and billing currency (strategy level)** — a
commercial starting decision only, inferring NO US jurisdiction/hosting/tax/customers/provider and
satisfying no future local-currency/invoice/consumer-protection/accounting/tax-display requirement;
multi-currency remains DEFERRED / NOT ACTIVATED (no-foreclosure only; no FX/conversion/selector/
mapping/settlement/accounting/currency-tax logic; future currencies need a separate gate). **P8C §5 / P8-I4 deferred decisions CONSUMED, NOT CLOSED.**
Jurisdiction separation rule preserved (user residence ≠ customer location ≠ entity jurisdiction ≠ hosting ≠
provider location ≠ tax jurisdiction ≠ commercial currency; Kuwait-start ≠ Kuwait-only anything; OD-J1/OD-J2 unchanged).
Escalation rule only — no VAT/GST/sales-tax/withholding/registration/invoicing conclusion.

**Payment-method direction (PAYMENT METHOD ≠ PAYMENT PROVIDER).** Intended compatibility:
Visa/Mastercard/major cards, Apple Pay, KNET (Kuwait starting market, no lock-in) — direction only, nothing
implemented; Apple Pay ≠ Apple as provider, Visa/Mastercard ≠ gateway selection, KNET ≠ provider selection;
Google Pay/wallets/other methods future no-foreclosure only; recurring-capability per method verified at
the future provider gate; consistent with the EXISTING P8-I4 §15 PCI architectural-avoidance principle
(hosted/tokenized; raw PAN/CVV off-platform; NO compliance claim; referenced, not duplicated); the P8-I4
deferred `payment methods` register is CONSUMED, NOT CLOSED.

**Milestone.** All five gate-registered decisions (OD-J1, OD-J2, OD-DR1, OD-DR2, OD-CJ1) now carry accepted
rows; the gate's external legal-input register remains OPEN.

**Boundary / status.** Governance-only; zero runtime/test diff. No billing/tax implementation, no provider or
MoR selection, no paid activation, no enterprise feature, no legal/tax drafting, no infrastructure, no PSRR
trigger, no deployment authority; no auto-activated successor (P10-C §10). Authoritative ONLY if/when this
exact candidate is merged and post-merge verified. Next required step: **Independent External Review of this
exact SHA + bundle**.

**Immediately prior (OD-DR2 acceptance — candidate `a9b3aee2`, accepted and MERGED via PR #517, tip
`b98561b847884557cc90c7c6600644ae23abf4c5`; now AUTHORITATIVE; retained as history):** Base:
`46756528509beebefc86ee399f331a796cbae6f2` (PR #516 merge — OD-DR1 acceptance,
authoritative; independently re-verified: parents `f35a3999…` / `13c9f7d1…`, merge tree `5a02ad1c…` equal to
the accepted candidate tree). Full detail:
`docs/governance/evidence/phase10_owner_decisions/OD-DR2_ACCOUNT_WIDE_DATA_ACCESS_EXPORT_POSITION.md` and the
new OD-DR2 section of `OWNER_DECISION_REGISTER.md`.

**OD-DR2 — ACCEPTED AT STRATEGY LEVEL.** Account-wide self-service export is **DEFERRED PENDING EXTERNAL
LEGAL DETERMINATION AND SEPARATE OWNER AUTHORIZATION**. Current export truth exact: P10-D3a remains
PROJECT-SCOPED EXPORT under its truthful-label contract (never described as final-output/account/"Export my
data"/account-wide); Decision Workspace and P7-I2 exports unchanged; no surface expanded; no secrets exposed.
Future product priority (direction only): **USEFUL OUTPUT PORTABILITY OF FINAL PROJECT OUTPUTS / RESULTS** —
no surface created, no format selected. Product Export ≠ Legal Data Access/Portability (neither substitutes
for the other; no regime conclusion). No-foreclosure = architecture preservation ONLY (not a build
instruction). Deferral does NOT suspend legal obligations — binding data-access/portability requests escalate
to Owner + external counsel. OD-DR1/P10-D3b untouched. Normal product-export exclusion defaults registered
(secrets/credentials/tokens/security metadata/other-user/institutional data never auto-exposed; append-only
stores + backups/replicas/derived copies classified separately). localStorage drafts are client-only truth.
Future strong identity/authorization principle recorded, not designed. NO institutional export authority or
feature. Format-neutral — no PDF/email/cloud/vendor delivery, connector, adapter, or integration. P7-I3
architecture referenced (Core → Canonical Output Model → Integration/Export Layer → External Tools); no
second canonical model. **Database-dump assumption explicitly REJECTED.**

**Preserved.** OD-CJ1 remains REGISTERED AND UNRESOLVED; OD-J1/OD-J2 and OD-DR1 accepted and unchanged; OD-A
governs brand/name.

**Boundary / status.** Governance-only; zero runtime/test diff. No export implementation, no
connector/delivery mechanism, no institutional functionality, no legal drafting, no infrastructure, no PSRR
trigger, no deployment authority; no auto-activated successor (P10-C §10). Authoritative ONLY if/when this
exact candidate is merged and post-merge verified. Next required step: **Independent External Review of this
exact SHA + bundle**.

**Immediately prior (OD-DR1 acceptance — candidate `13c9f7d1`, accepted and MERGED via PR #516, tip
`46756528509beebefc86ee399f331a796cbae6f2`; now AUTHORITATIVE; retained as history):** Base:
`f35a399960b131e79f390c8eff2a6e95b29726a0` (PR #515 merge — OD-J1/OD-J2
acceptance, authoritative; independently re-verified: parents `022e5b75…` / `aed0cdf2…`, merge tree
`25d839f0…` equal to the accepted candidate tree). Full detail:
`docs/governance/evidence/phase10_owner_decisions/OD-DR1_PHYSICAL_DELETION_ERASURE_POSITION.md` and the new
OD-DR1 section of `OWNER_DECISION_REGISTER.md`.

**OD-DR1 — ACCEPTED AT STRATEGY LEVEL.** Current authorized account-exit capability remains **Account
Deactivation** (P10-D3b preserved; the `"deleted"` status is a tombstone/non-active marker, NOT physical
erasure; a future true erasure capability must use distinct terminology/state). **Physical deletion/erasure is
DEFERRED PENDING EXTERNAL LEGAL DETERMINATION AND SEPARATE OWNER AUTHORIZATION** — no implementation, no
retention-behavior change. Future principles recorded non-authorizingly (explicit request, identity
re-verification, pending state, configurable grace/notice — the ~1-month/~1-week/~1-day preference is a
NON-BINDING future UX preference and never a liability waiver — cancellation before finalization, conditional
export opportunity that does NOT touch OD-DR2, truthful final-state communication, minimum necessary
non-content-bearing processing evidence that can never reconstruct erased content). Delete-every-row is
explicitly NOT assumed (six-way classifiability requirement). **Deferral does NOT suspend existing legal
obligations** — binding erasure/data-subject requests escalate to Owner + external counsel as exceptions.
Subscription expiry/non-payment and inactivity are NOT deletion requests. Institutional deletion authority
reserved. A separate future **technical deletion-impact gate** (all stores incl. backups/replicas/derived
copies) is prerequisite to any implementation authorization.

**Preserved.** OD-DR2 and OD-CJ1 remain REGISTERED AND UNRESOLVED; OD-J1/OD-J2 authoritative and unchanged;
OD-A governs brand/name; project-scoped export (P10-D3a) remains the only authoritative export; P10-D3b not
reopened.

**Boundary / status.** Governance-only; zero runtime/test diff. No deletion implementation, retention logic,
account-wide export, institutional functionality, legal drafting, infrastructure, PSRR trigger, or deployment
authority; no auto-activated successor (P10-C §10). Authoritative ONLY if/when this exact candidate is merged
and post-merge verified. Next required step: **Independent External Review of this exact SHA + bundle**.

**Immediately prior (OD-J1 + OD-J2 acceptance — candidate `aed0cdf2`, accepted and MERGED via PR #515, tip
`f35a399960b131e79f390c8eff2a6e95b29726a0`; now AUTHORITATIVE; retained as history):** Base:
`022e5b75cb0e7bc9ee248f20aed5df7da1368989` (PR #514 merge — Jurisdiction & Data-Rights
Owner-Decision Gate, authoritative; independently re-verified: parents `07389b24…` / `ca4956c2…`, merge tree
`39e2ee43…` equal to the accepted candidate tree). Full detail:
`docs/governance/evidence/phase10_owner_decisions/OD-J1_OD-J2_JURISDICTION_AND_HOSTING.md` and the new
Phase-10 section of `OWNER_DECISION_REGISTER.md`.

**OD-J1 — ACCEPTED.** Canonical statement: *GCC-first commercial marketing; globally open user availability
from launch; global-ready product from the outset.* GCC-first is marketing SEQUENCING only (not GCC-only, not
Kuwait-only, not a geographic or architectural restriction); **non-GCC users may access, register, and use the
product from launch** (subject only to later lawfully-required restrictions via separate legal/governance
processes); intended worldwide; intended for both INDIVIDUAL and INSTITUTIONAL use with NO institutional
feature activation (no tenancy, enterprise admin, org contracts, Layer 5, Stage 6, B2B implementation,
institutional pricing, or compliance features). Product/market intent only — NOT a legal clearance conclusion.

**OD-J2 — ACCEPTED AT STRATEGY LEVEL.** *Minimum practical infrastructure now, clean expansion seams later*:
single practical production region permitted initially; future flexibility preserved (provider migration,
regions, residency, jurisdiction/customer-driven hosting, global expansion); no permanent coupling to one
provider/region/country/storage-jurisdiction assumption. **No provider and no region is selected** — initial
provider+region choice is DELEGATED to a later, separately authorized infrastructure gate (accepted
delegation). GCC rollout does NOT imply GCC hosting; no data-location commitment either way. "Global-ready" ≠
multi-region/active-active/sharding/multi-provider now.

**Identifier disambiguation.** P10 OD-J1/OD-J2 (Jurisdiction & Data-Rights) are DISTINCT from Phase-1's
accepted OD-J ("Product role model"); the historical decision is untouched; identifiers unchanged.

**D3b stat correction (numeric only).** Prior recorded P10-D3b stat `+487/-1` superseded by repository-verified
`+487/-3` (candidate `a751cb3b…`, merge `07389b24…`, `5 files changed, 487 insertions(+), 3 deletions(-)`);
the merged gate file is deliberately NOT byte-edited; live surfaces corrected; D3b NOT reopened.

**Preserved unresolved.** OD-DR1, OD-DR2, OD-CJ1 remain REGISTERED AND UNRESOLVED; OD-A continues to govern
brand/name; the gate's external legal-input register remains open — NO privacy-regime applicability, lawful
basis, consent/cookie requirement, retention/erasure/portability requirement, or tax treatment is decided.

**Boundary / status.** Governance-only; zero runtime/test diff. No infrastructure implementation, no
geo-restriction mechanism, no institutional feature, no legal drafting, no PSRR trigger, no deployment
authority, no auto-activated successor (P10-C §10). Authoritative ONLY if/when this exact candidate is merged
and post-merge verified. Next required step: **Independent External Review of this exact SHA + bundle**.

**Immediately prior (Jurisdiction & Data-Rights Owner-Decision Gate — candidate `ca4956c2`, accepted and
MERGED via PR #514, tip `022e5b75cb0e7bc9ee248f20aed5df7da1368989`; now AUTHORITATIVE; retained as history):**
Base at gate drafting: `07389b24ce9c4a606526315f2c19118f292f04db` (PR #513 merge — P10-D3b Account
Deactivation implementation, authoritative; independently re-verified: parents `46c80714…` / `a751cb3b…`, tree
`886d06f605bf08b36b765a96a528bd42047af0de`, empty candidate→merge diff). Full detail:
`docs/governance/P10_JURISDICTION_AND_DATA_RIGHTS_OWNER_DECISION_GATE.md`.

**Authorization scope (Owner-granted, strictly bounded).** ONE governance-candidate session: `RECONSTRUCT →
CREATE GOVERNANCE CANDIDATE → FREEZE EXACT SHA → GOVERNANCE TRUTH SWEEP → CREATOR GRILL → SHA-PRESERVING
BUNDLE`. **No legal drafting (Privacy Policy / Terms / consent / cookie notice / payment terms / IP terms), no
deletion/erasure workflow, no account-wide export, no PSRR, no deployment, no payment-provider selection, no
monitoring/backup/security implementation.** Allowed paths for THIS candidate: `docs/governance/` only.

**Purpose.** Repository evidence is INSUFFICIENT to determine legal-regime applicability (no registered launch
country, user-residence scope, commercial jurisdiction, or hosting/data-location assumption; the P10-C §9
GDPR/PDPL open question is triggered and unresolved). This gate REGISTERS the blocking Owner decisions
(OD-J1 launch markets; OD-J2 hosting/data location; OD-DR1 deletion/erasure position; OD-DR2 account-wide
access/export position; OD-CJ1 commercial jurisdiction/tax scope; OD-B1 referencing the EXISTING OD-A brand
authority) and the external legal-input requests (GDPR/PDPL applicability if any; policy/terms/consent/cookie
requirements; data-subject-rights scope; user-content/IP terms; payment/refund terms) — answering none of
them. `OWNER_DECISION_REGISTER.md` UNCHANGED (it indexes accepted decisions only).

**Sync carried.** Records `P10-D3b IMPLEMENTATION AUTHORITATIVE: YES` (PR #513, tip `07389b24…`, identity
independently re-verified) without reopening or modifying D3b. Account Deactivation ≠ Physical Deletion;
P10-D3a project-scoped export unchanged.

**Boundary / status.** Governance-only; zero runtime/test diff. No auto-activated successor gate — the next
step depends on actual Owner answers, each separately authorized (P10-C §10). No PSRR trigger; no deployment
authority. Authoritative ONLY if/when this exact candidate is merged and post-merge verified. Next required
step: **Independent External Review of this exact SHA + bundle**.

**Immediately prior (P10-D3b — contract candidate `e5e27f38`, accepted and MERGED via PR #512, tip
`46c80714a35e5c6cf289b4d807d6f7a31d17cf5d`; implementation candidate `a751cb3b`, accepted and MERGED via PR
#513, tip `07389b24ce9c4a606526315f2c19118f292f04db`; both now AUTHORITATIVE; retained as history):** Base at
contract drafting: `d649a4df5889cf037096014ce69d362adb2fb00b` (PR #511 merge — P10-D3a Self-Service Project
Export implementation, authoritative; independently re-verified: parents `1a87bf58…` / `4c5f325f…`, tree
`acd8c16ab3012904505d6c5be31255f51595bd09`, empty candidate→merge diff). Full detail:
`docs/governance/P10_D3B_ACCOUNT_DEACTIVATION_INCREMENT_CONTRACT.md`.

**Authorization scope (Owner-granted, strictly bounded).** ONE governance-candidate session: `VERIFY → CREATE
P10-D3b CONTRACT CANDIDATE → FREEZE EXACT SHA → CREATOR GRILL → SHA-PRESERVING BUNDLE`. **No runtime code, no
account-behavior change, no push, no PR, no PSRR, no deployment.** Allowed paths for THIS candidate:
`docs/governance/` only.

**Technically truthful framing (binding).** Account DEACTIVATION only: the existing bounded store primitive
`set_status(account_id, "deleted", now_iso)` gains a reachable self-service authenticated trigger (POST +
CSRF + password re-entry). Explicitly NOT physical deletion, NOT data erasure, NOT retention cleanup, NOT legal
"right to erasure" compliance. No row deleted anywhere; all 14 durable table families preserved; append-only
stores untouched; Phase-7 §25 consumed as fact only. No reactivation path defined.

**Verified foundation.** At the base tip: `validate_session` fails closed on any non-active status (primary
session-invalidation mechanism); login requires `status == "active"` (generic 401); `web/api_v1.py` requires
the credential's bound account to be `"active"` — so API access already dies with deactivation and
per-credential revocation is excluded as unnecessary; `verify_password` + `_csrf_valid()`/`_csrf_reject()` are
the reused seams; `increment_session_epoch` is defense-in-depth only. All nine registered stop conditions
probed; none triggered.

**Boundary / status.** Governance-only; zero runtime/test diff. `OWNER_DECISION_REGISTER.md` UNCHANGED.
Creating or merging this contract **does NOT authorize implementation**; implementation needs separate explicit
Owner authorization. No automatic successor (no P10-D3c). No PSRR trigger. No deployment authority. No
physical-deletion authority. Authoritative ONLY if/when this exact candidate is merged and post-merge verified.
Next required gate: **Mandatory Creator Grill on this exact candidate**, then Independent External Review.

**Immediately prior (P10-D3a — contract candidate `452b9ded`, accepted and MERGED via PR #510, tip
`1a87bf58b892b2924a91727a7b3fc4425d909db7`; implementation candidate `4c5f325f`, accepted and MERGED via PR
#511, tip `d649a4df5889cf037096014ce69d362adb2fb00b`; both now AUTHORITATIVE; retained as history):** Base at
contract drafting: `bc85424afc0c90e8e1bfb17dd413c326f7a3ff69` (PR #509 merge — P10-D2 Decision Workspace
Access-Control Remediation, authoritative). Full detail:
`docs/governance/P10_D3A_SELF_SERVICE_PROJECT_EXPORT_INCREMENT_CONTRACT.md`.

**Authorization scope (Owner-granted, strictly bounded).** ONE governance-candidate session: `VERIFY → CREATE
CONTRACT CANDIDATE → FREEZE EXACT SHA → CREATOR GRILL → SHA-PRESERVING BUNDLE`. **No runtime code, no
`web/app.py` change, no implementation tests, no PSRR, no deployment.** Allowed paths for THIS candidate:
`docs/governance/` only.

**Corrective lineage.** The Independent External Reviewer rejected the earlier combined `P10-D3` proposal on two
material grounds only: (1) self-service export and account deactivation must be **separate increments**; (2)
`P10-D3a` requires **its own committed candidate contract** before implementation authorization. This contract
answers both. **`P10-D3b — Account Deactivation` remains a separate future increment — NOT authorized, NOT
scoped, NOT started.**

**Subject.** Define the boundary for one browser/session-authenticated self-service **project** export surface in
`web/app.py` consuming the existing canonical seam `engine.read_export_service.produce_project_export` with the
identity from the existing `_current_account()` seam. Evidence at base: `web/app.py` does not consume the seam at
all; the only shipped consumer (`web/api_v1.py`, P7-I2) demands a machine Bearer credential whose issuance helper
has no shipped call site; `/session/<sid>/deliverable` is a distinct surface requiring a live in-memory session.
The increment would add **reachability**, not a new capability.

**Truthful label required.** Project-scoped wording only (`Export project` / `Export project data`); `Export my
data` / `Export account` / `Export all my data` / legal subject-access framing explicitly prohibited, in `en` and
`ar` alike.

**Phase-7 §25 PRESERVED.** No browser-surface `access_audit` write; the closed disposition is consumed as fact,
never reopened or reclassified. Recorded as a deliberate, truthful limitation.

**Boundary / status.** Governance-only; zero runtime/test diff. `OWNER_DECISION_REGISTER.md` UNCHANGED. Creating
or merging this contract **does NOT authorize implementation**; implementation needs separate explicit Owner
authorization. No automatic successor gate. No PSRR trigger. No deployment authority (`OD-P`'s separate
deployment gate **and** explicit Owner deployment authorization both remain independently required and
unsatisfied). Authoritative ONLY if/when this exact candidate is merged and post-merge verified. Next required
gate: **Mandatory Creator Grill on this exact candidate**, then Independent External Review.

**Immediately prior (Phase 10 P10-C entry contract — candidate `36145016`, accepted and MERGED via PR #508, tip
`3f92d57e49a8d6b01b0c6a7184ec7b1442b87e8a`; now AUTHORITATIVE — and P10-D2 implementation — candidate
`871135d1`, accepted and MERGED via PR #509, tip `bc85424a`; now AUTHORITATIVE; both retained as history):**
Base at P10-C drafting: `f91a82565dce0cbeae323be89dedd6a68c55e61d` (PR #507 merge — Post-Phase-9 Next Governed
State review, authoritative). Full detail: `docs/governance/PHASE_10_COMMERCIAL_LEGAL_SECURITY_OPERATIONAL_
READINESS_P10C_CONTRACT.md`.

**Authorization scope (Owner-granted, strictly bounded).** `CREATE → FREEZE EXACT SHA → CREATOR GRILL` only; no
implementation beyond this candidate. Follows the established P7C/P8C phase-entry-contract convention.
**Coordinates/consolidates existing governance only** — `OD-P`, `D-PSRR-01`, `P8C` §5 item 25, and the
remediation plan remain the canonical owners; every obligation is retained via `D-FPC-MAP-06` consume/extend
classification, none deleted or superseded.

**Entry criteria.** Phases 4–9 formally closed, independently reconfirmed (Phase-6 lane closure `0254240`/PR
#391 + distinct Product-Foundation §5 closure `afdcf7f`, both confirmed ancestors of this base). Satisfaction
of entry criteria does NOT itself authorize implementation; `OD-P`'s separate deployment gate + explicit Owner
deployment authorization remain independently required.

**PSRR relationship unmoved.** Consumed within Phase-10 ownership; execution NOT required at Phase-10 entry;
mandatory before first public production deployment.

**No frozen future sequence.** Registers obligation dependencies, triggers, and a gate-selection rule
(evidence-based, smallest sufficient, Owner-selected) — no successor sub-increment is named or automatically
authorized.

**Proposition-level revalidation only.** Three specific superseded propositions registered (Security
Architecture's stale auth-state claim; Disaster Recovery Scenario-3's `main`-branch premise; Data Retention's
"in-memory only" claim) — no architecture document declared stale in whole.

**Boundary / status.** Governance-only; zero runtime/test/classifier/scoring/progression/persistence/security
diff. `OWNER_DECISION_REGISTER.md` UNCHANGED. Does NOT authorize Phase-10 implementation, PSRR execution,
deployment, legal-artifact drafting, payment-provider work, auth/commercial/trial changes,
monitoring/observability or security-hardening implementation, D4, D8, IoT, domain activation, or Phase-9 debt
cleanup. Does NOT declare Phase 10 complete or entered beyond this governance layer. Authoritative ONLY if/when
this exact candidate is merged and post-merge verified. Next required gate: **Mandatory Creator Grill on this
exact candidate**, then Independent External Review.

**Immediately prior (Phase 9 Formal Closure, candidate `8874d08` — accepted and merged via PR #506 `833f657`;
retained as history):** governance-only; PHASE 9 = FORMALLY CLOSED / AUTHORITATIVE. Base:
`833f657d24d0d8d6d679cd3935ab9fb84c1f50ec` (PR #506 merge — Fresh Phase 9 Remaining-Obligation / Exit-Criteria
Review, authoritative; verdict ELIGIBLE, zero MUST-FIX, zero material conflict). Full detail:
`docs/governance/PHASE_9_FORMAL_CLOSURE_RECORD.md`.

**Reconfirmation at this exact tip.** MUST-FIX count = 0; material conflict count = 0; former vacuous
picker-test blocker remains discharged; no new evidence invalidates eligibility; `activated_domains() ==
['electronics_electrical', 'mechanical']` verified live; full suite unchanged 2696/3/1/0; safety/determinism
sweep re-run this gate with no regression.

**What Phase 9 delivered.** The Mechanical domain-activation workstream: D3, P9-E1/P9-PREREQ-A, P9-E2/
P9-PREREQ-B, P9-E2-R, Mechanical P9-QS qualification (zero open/blocked criteria), the Mechanical safety-cue
family, L2SC-01, L10N-RH-01, the Tier-1 EN/AR Mechanical public label, explicit Owner-authorized Mechanical
activation, and the vacuous-picker-test corrective gate — all CLOSED/DISCHARGED/AUTHORITATIVE. `Mechanical =
ACTIVE. Mechanical P9-QS = SATISFIED.` Five known non-blocking debts (stale `classify_domain` docstring, 4
historical test-file comments, `UI_B_START_024` wording, missing real E2E Tier-1 chain test, CLI real-banner
coverage) remain explicitly preserved, live, post-Phase-9 debt — NOT claimed fixed. D4, D8, IoT/drone/renewable/
other future domains, Phase 10, PSRR, and deployment remain explicitly outside/deferred — none authorized,
started, or implied by this closure.

**Boundary / status.** Governance-only; zero runtime/test/classifier/scoring/progression/persistence/security
diff. `OWNER_DECISION_REGISTER.md` UNCHANGED — formal closure of an already-authorized, already-executed,
already-qualified phase, not a new Owner decision (Phase 8 formal-closure precedent). Governance truth sweep:
STALE/UNSUPPORTED live-current count = 0. Authoritative ONLY if/when this exact candidate is merged and
post-merge verified. Next required gate: **Mandatory Grill on this exact candidate**, then the governed
lifecycle. After this merges, no further Phase 9 gate is expected; Phase 10, PSRR, deployment, and any future
domain-activation workstream each require their own separate, explicit Owner authorization.

**Immediately prior (Fresh Phase 9 Remaining-Obligation / Exit-Criteria Review, candidate `c513293` — accepted
and merged via PR #506 `833f657`; retained as history):** post-correction reassessment; read-only; returned
**PHASE 9 CLOSURE ELIGIBILITY: ELIGIBLE**; Phase 9 remained OPEN (not closed by that record). Base:
`1a0f6ee8d1af91e7e078aaa96e7c63782fc9a3c2` (PR #505 merge — Phase 9 vacuous picker test corrective
implementation, authoritative). Full detail:
`docs/governance/P9_REMAINING_OBLIGATION_EXIT_CRITERIA_REVIEW_ELIGIBLE_RECORD.md`.

**Result.** The prior sole MUST-FIX (vacuous picker test) independently reconfirmed genuinely discharged on the
merged tip — old test gone; corrected `test_start_domain_picker_offers_only_activated_domains` uses a real
`POST /start` flow, re-proven load-bearing via a fresh mutation probe this gate (RED → byte-identical restoration
→ GREEN). Complete Phase 9 obligation matrix rebuilt fresh: D3, P9-QS, P9-E1, P9-E2, P9-E2-R, Mechanical
qualification, safety-cue family, L2SC-01, L10N-RH-01, Tier-1 label, Mechanical activation, corrected P9-QS
governance, vacuous-picker corrective gate — all DISCHARGED. Five known non-blocking debts unchanged. D4, D8,
IoT/drone/renewable future domains confirmed OUTSIDE this Phase 9's closure scope. Fresh stale-truth sweep:
STALE/UNSUPPORTED live-current count = 0. Safety/determinism sweep PASS, no regression. Full suite unchanged:
2696/3/1/0.

**Boundary / status.** Per this gate's own governing instructions, an eligibility finding does NOT close Phase 9.
**Phase 9 remains OPEN.** No formal closure performed, authorized, or implied. Phase 10 / PSRR / deployment
remain NOT AUTHORIZED. No third domain activated or implied; D4/D8 untouched. `OWNER_DECISION_REGISTER.md`
UNCHANGED. Governance-only; zero runtime/test/classifier/scoring/progression/persistence/security diff.
Authoritative ONLY if/when this exact candidate is merged and post-merge verified. Next required gate:
**Mandatory Grill on this exact candidate**, then the governed lifecycle. After this merges, the next eligible
step is a separate, Owner-authorized **Phase 9 formal closure** gate — not authorized or performed here.

**Immediately prior (Phase 9 Vacuous Picker Test Corrective Implementation, candidate `3f3b598` — accepted and
merged via PR #505 `1a0f6ee`; retained as history):** LOW-RISK; test-only; ZERO production diff; corrected the
sole MUST-FIX blocker from the prior Remaining-Obligation / Exit-Criteria Review. Base:
`48b81773f9ee68ca9d897931a43271609c3bdeac`

**Preceding review (read-only, no candidate created).** A Phase 9 Remaining-Obligation / Exit-Criteria Review on
this same base independently reconfirmed the full Phase 9 obligation matrix DISCHARGED/AUTHORITATIVE (D3, P9-QS,
P9-E1, P9-E2, P9-E2-R, Mechanical qualification, safety-cue family, L2SC-01, L10N-RH-01, Tier-1 label, Mechanical
activation, corrected P9-QS governance) and returned **PHASE 9 CLOSURE ELIGIBILITY: NOT YET ELIGIBLE**, naming
exactly ONE MUST-FIX blocker: a vacuous test. All other known debts remained NON-BLOCKING / OUTSIDE PHASE 9. D4,
D8, and IoT/drone/renewable future domains confirmed outside this Phase 9's closure scope (Mechanical is the sole
domain-activation workstream this repository's Phase 9 was executed against).

**Defect and correction.** `tests/test_p6_1_truthful_domain_labeling.py::
test_mechanical_not_offered_in_start_domain_picker` called `client.get("/start")` — `/start` is POST-only, so this
received Flask's generic 405 page and the assertions passed vacuously regardless of real picker content; its
premise was also stale (Mechanical is now correctly activated and IS offered). Renamed to
`test_start_domain_picker_offers_only_activated_domains`; rewritten to POST a real NONE-classifying idea to
`/start` (the real D2 picker path, `choice_domains=activated` at `web/app.py:1753`) and assert the offered
`domain_choice` set equals `activated_domains()` exactly. Mutation-proved load-bearing: removing `mechanical` from
the allowlist → RED; adding an unintended `software` → RED; both restored byte-identically.

**Boundary / status.** **Changed file: `tests/test_p6_1_truthful_domain_labeling.py` only** — zero production/
classifier/scoring/progression/persistence/security/schema/registry diff (confirmed via `git diff --stat` and
`sha256sum` on the mutation-probed file after restoration). Focused: 32 passed (net count unchanged). Relevant
suite: 138 passed. Full governed suite: **2696 passed / 3 skipped / 1 xfailed / 0 failed** — unchanged.
`OWNER_DECISION_REGISTER.md` UNCHANGED. **Phase 9 remains OPEN** — this candidate does NOT declare closure-
eligibility. Phase 10 / PSRR / deployment remain NOT AUTHORIZED. No third domain activated or implied; D4/D8
untouched. Authoritative ONLY if/when this exact candidate is merged and post-merge verified. Next required gate:
**Mandatory Grill on this exact candidate**, then the governed lifecycle. After this merges, the next eligible
step is a fresh **Phase 9 Remaining-Obligation / Exit-Criteria Review** — not authorized or performed here.

**Immediately prior (CORRECTED Mechanical P9-QS Qualification Governance Candidate, candidate `f01e2a5` —
accepted and merged via PR #504 `48b8177`; retained as history):** MATERIAL CORRECTION of rejected candidate
`c63724b` (preserved immutable, unpushed, unamended at `refs/rejected/mechanical-p9qs-status-c63724b`). Base:
`5a1d2c15ad680b8b80304b51a3885fac42e32f56`
(PR #503 merge — Mechanical activation, authoritative). The prior qualification-status candidate,
`c63724b3e7f8e5fa5e5ada8739f3d80f8319efb7`, was independently **REJECTED** (verdict: MATERIAL CORRECTION
REQUIRED — MD-1: `OWNER_DECISION_REGISTER.md` row `D-P9-MECH-03` was left asserting qualification "remains a
SEPARATE, still-unauthorized future gate," contradicting the already-merged qualification evidence; MD-2: the
candidate falsely cited `MECHANICAL_ACTIVATION_EXECUTION_RECORD.md` §15 as the source of that stale claim, which
contains no such text). The reviewer explicitly confirmed the substantive qualification determination itself was
correct — the rejection was governance-truth/attribution only. That candidate is preserved **immutable, unpushed,
unamended** at `refs/rejected/mechanical-p9qs-status-c63724b`. This corrected candidate returns to the exact
authoritative parent (not the rejected candidate) and corrects both defects: `D-P9-MECH-04` clarifies
`D-P9-MECH-03` without retroactively broadening its authorization scope, and the disclosure now cites the actual
four stale-text locations (`ACTIVE_EXECUTION_ROADMAP.md`, this file, `CURRENT_PROJECT_STATE.md`,
`OWNER_DECISION_REGISTER.md`'s own `D-P9-MECH-03` row). Full detail:
`docs/governance/MECHANICAL_P9QS_QUALIFICATION_STATUS_RECORD.md`.

**Determination (independently reconstructed from primary sources, not carried forward from the rejected
candidate's summary):** `P9_MECH_QUALIFICATION_RECORD.md` (commit `dd7b487`) and
`P9_MECH_SF_FORMAL_CLOSURE_RECORD.md` (commit `c25c843`) — both merged BEFORE Mechanical activation — jointly
declared `MECHANICAL = P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS`, naming six blockers. All six are independently
reconfirmed discharged: (1) Mechanical safety-cue family; (2) Tier-1 EN/AR public label (commit `e635c9f`); (3)
CF-6 full-scope closure; (4) CF-2 full-scope closure; (5) NMF-1+FU-1 test hardening; (6) explicit Owner activation
authorization (`D-P9-MECH-03`, ACCEPTED — EXECUTED). Per P9-QS §2's own binding separations (activation ≠
qualification, neither retroactively creates the other), the correct current determination is **Mechanical P9-QS
qualification = SATISFIED** on the live activated runtime. `activated_domains() ==
['electronics_electrical', 'mechanical']`, verified live. This implies NO new implementation, NO Phase 9 closure,
NO Phase 10 authorization, NO PSRR, NO deployment. **Phase 9 remains OPEN** — the next gate is a Phase 9
Remaining-Obligation / Exit-Criteria Review (per repository precedent: Phase 7 §25, Phase 8's own review, D3's
closure + Remaining-Obligation Review), not automatically Phase 9 formal closure.

**Correction scope:** governance-only (ODR, this file, roadmap, CPS, the dedicated status record). Zero
runtime/test/classifier/scoring/progression/persistence/security diff. Full governed suite re-verified unchanged
at the same baseline as the rejected candidate's parent. **Changed paths:** `OWNER_DECISION_REGISTER.md` (new row
`D-P9-MECH-04` + non-destructive annotation on `D-P9-MECH-03`), `ACTIVE_EXECUTION_ROADMAP.md` (appended corrective
note), this file, `CURRENT_PROJECT_STATE.md` (appended corrective note),
`MECHANICAL_P9QS_QUALIFICATION_STATUS_RECORD.md` (rewritten fresh). Authoritative ONLY if/when this exact
candidate is merged and post-merge verified. Next required gate: **Mandatory Grill on this exact candidate**, then
the governed lifecycle.

**Immediately prior (Mechanical Activation Execution Gate, candidate `ca6575f` — accepted and merged via PR #503
`5a1d2c1`; retained as history):** Owner-authorized, HIGH-ASSURANCE runtime-state change. Owner authorization
(verbatim): "I explicitly approve activation of the Mechanical domain within InventorAI and authorize proceeding
to the Mechanical activation execution gate." Canonical mechanism: `engine/domain_activation.py::
_ACTIVATED_DOMAINS`, changed to `frozenset({"electronics_electrical", "mechanical"})` (one line + docstring
truthfulness update). Real user-flow + Tier-1 real-surface verification passed live; L10N-RH-01 residual
reachability Classification A (non-blocking). Test-suite reconciliation: 113 pre-existing tests individually
triaged (none blindly relaxed); full governed suite **2696 passed / 3 skipped / 1 xfailed / 0 failed**. All 4
required mutations RED→restored, full suite GREEN after restoration. **Boundary / status as originally recorded
at this gate:** `activated_domains() == ['electronics_electrical', 'mechanical']` — Mechanical ACTIVE. *(Note: this
gate's original text additionally asserted "Mechanical NOT qualified (P9-QS remains a separate future gate)" —
that clause is corrected by the current active contract above and by `D-P9-MECH-04`; it was accurate as a
forward-looking statement at the time but did not account for already-merged qualification evidence. This
gate's activation scope and authorization are otherwise unchanged.)* `OWNER_DECISION_REGISTER.md` — new row
`D-P9-MECH-03` (explicit Owner activation authorization + execution). Full detail:
`docs/governance/MECHANICAL_ACTIVATION_EXECUTION_RECORD.md`.

**Immediately prior (Tier-1 EN/AR Mechanical public label gate, candidate `e635c9f` — accepted and merged via PR
#502 `18a97da`; retained as history):** activation-readiness edge; implemented contract §13/Requirement 9; added
a truthful Tier-1 Mechanical public label to `web/domain_label.py::_PUBLIC_DOMAIN_LABELS` —
`"Mechanical-informed review"` / `"مراجعة مستنيرة بمجال الميكانيكا"`; no-activation-leak independently traced and
proven (the `/start` picker never reads this dict); `activated_domains()` unchanged
(`['electronics_electrical']`) at that gate. Full suite then: 2691 passed / 3 skipped / 1 xfailed / 0 failed.

**Immediately prior (L10N-RH-01 formal closure gate, candidate `0b5e238` — accepted and merged via PR #501
`7cb5b6e`; retained as history):** governance-only, implemented nothing; `L10N-RH-01` = FORMALLY CLOSED /
DISCHARGED; closure eligibility independently proven from the registration's own non-authorization clause (a
bounded remediation gate was required — merged and verified in the tree) and fresh re-verification
(`tests/test_l10n_rh01_remediation.py`: 7 passed; `web/ui_text.py`'s `UI_B_START_024` confirmed corrected). All 3
registered observations confirmed REMEDIATED: (1) `UI_B_START_026` negative-semantic-guard gap; (2)
`SERVICE_UNAVAILABLE` localization-path regression-guard gap (both call sites); (3) present-confirm Arabic
checkbox wording (`start_present_confirm_label`/`UI_B_START_024`). No fourth observation; "transport wording
precision" reconfirmed not a registered item; `UI_B_START_030` reconfirmed byte-unchanged. Two non-blocking
residual observations preserved (`UI_B_START_024` dual-surface consumption; Observation #1's test-assertion
precision — the negative assertion is the one that actually catches the registered mutation). Governance/
documentation-only — zero runtime/test/pack/registry/activation/schema/persistence diff. Full suite unchanged:
2684 passed / 3 skipped / 1 xfailed / 0 failed.

**Immediately prior (L10N-RH-01 bounded remediation gate, candidate `783571f` — accepted and merged via PR #500
`c163a9d`; retained as history):** LOW-RISK CONTROLLED; implemented the 3 registered observations; `L10N-RH-01` =
IMPLEMENTED / READY FOR FORMAL CLOSURE (not itself claimed FORMALLY CLOSED at that gate). Risk classification
LOW-RISK CONTROLLED, confirmed by the actual implementation: exactly one data-only string changed
(`web/ui_text.py`'s `UI_B_START_024`); `web/app.py` and `engine/domain_activation.py` byte-unchanged.

**Observation #1 (`UI_B_START_026`) = REMEDIATED** — new load-bearing test using independently hardcoded literal
content checks; mutation proof (false electronics-only claim injected → RED; restored → GREEN).
**Observation #2 (`SERVICE_UNAVAILABLE` seam) = REMEDIATED** — new parametrized test exercises BOTH authoritative
production call sites (`web/app.py:1802`, `web/app.py:1842`) via a forced durable-store failure; mutation proof
(both call sites bypassed → RED for both; restored → GREEN). **Observation #3 (present-confirm wording) =
REMEDIATED at the corrected surface** — `start_present_confirm_label`/`UI_B_START_024` (broadened-activation
branch), NOT `UI_B_START_030`/`start_confirm_label`; rewritten from prompt/instruction style to a domain-neutral
first-person consent affirmation matching `UI_B_START_030`'s already-accepted register; `UI_B_START_023` and
`UI_B_START_030` confirmed byte-unchanged; mutation proof (reverted to old wording → RED; restored → GREEN).

**Suite:** focused file 7 passed; relevant localization/web tests 76 passed; full governed suite **2684 passed /
3 skipped / 1 xfailed / 0 failed** (baseline 2677/3/1/0; delta +7 passed, 0 regressions). `activated_domains()`
(the real function — a sorted list) returns `['electronics_electrical']`, verified before/after every probe —
Mechanical remains NOT ACTIVATED. No Tier-1 label implemented; `web/domain_label.py` untouched. `L2SC-02`
remains registration-only, outside activation-readiness. **Changed paths:** `web/ui_text.py` (one data-only
entry), the new focused test file, the new dedicated remediation record, and this AIC/roadmap/CPS/capability-
register sync. `OWNER_DECISION_REGISTER.md` UNCHANGED. **Phase 9 remains OPEN.** Authoritative ONLY if/when this
exact candidate is merged and post-merge verified. Next required gate: **Mandatory Grill on this exact
candidate** → independent external exact-candidate review → Owner acceptance → SHA-preserving publication → PR →
pre/post-merge verification. After this merges, the eligible next steps are a separate `L10N-RH-01` formal
closure gate and/or the **Tier-1 EN/AR Mechanical public label** gate — neither authorized or performed here.

**Immediately prior (L10N-RH-01 reassessment gate, MATERIAL CORRECTION of rejected candidate `7e810e6` — accepted
and merged via PR #499 `585d1f8`; retained as history):** The first reassessment-record candidate,
`7e810e6be88234cf2a0508167770307130a8a1d1`, was independently **REJECTED** (verdict: MATERIAL CORRECTION
REQUIRED — Observation #3 misidentified `UI_B_START_030` (`start_confirm_label`) as the defective surface and
"generic vs. domain-specific wording" as the defect class; neither is authoritative). Every other finding —
Observations #1/#2, the overall determination, the activation-readiness matrix, and all protected boundaries —
was independently confirmed correct. That candidate is preserved **immutable, unpushed, unamended** at
`refs/rejected/l10n-rh01-reassessment-7e810e6`. The corrected candidate `2833268` returned to the exact
authoritative parent `3b7783f19d7b1ee9f6618342a00ed47362b35ac4` and corrected Observation #3's identification to
`UI_B_START_024`/`start_present_confirm_label` (broadened-activation branch), with defect class prompt/
instruction wording vs. first-person consent — retargeting the remediation proposal accordingly, explicitly
ruling out domain-specific Tier-1 translation work. Independently re-reviewed, accepted, published SHA-preserving,
and merged (PR #499, base `585d1f8`; merge tree == candidate tree).

A prior gate correctly STOPPED before implementing the Tier-1 EN/AR Mechanical public label, citing
`P9_MECHANICAL_DOMAIN_QUALIFICATION_CONTRACT.md` §13's explicit precondition — the label may replace the neutral
Tier-0 fallback "only when the label becomes truthful (i.e. not before activation-readiness)." This gate performs
the next prerequisite: reassessing `L10N-RH-01` and determining Mechanical's overall activation-readiness.

**`L10N-RH-01` reassessment: all 3 originally-registered observations reconfirmed STILL PRESENT** via fresh,
byte-restored mutation probes this gate: (1) the broadened-activation Arabic negative-semantic-guard gap
(`UI_B_START_026`) — 31/31 tests still passed against an injected false electronics-only claim, since the only
existing assertion compares against the same dict being mutated; (2) the `SERVICE_UNAVAILABLE`
`localize_message()` bypass at `web/app.py`'s two call sites — the full governed suite (2677/2677) still passed
against a bypassed call site; (3) the present-confirm Arabic checkbox wording (`start_present_confirm_label`,
broadened-activation branch, `UI_B_START_024`) — prompt/instruction style rather than first-person consent-
affirmation style, unlike its English sibling — unchanged, still not production-reachable under today's
single-domain activation (`UI_B_START_030`/`start_confirm_label` is a different, unaffected template variable).
Both probed files (`web/ui_text.py`, `web/app.py`) verified `sha256sum`-identical to their pre-probe state after
restoration; full suite reconfirmed green throughout. **`L10N-RH-01` = STILL PRESENT / NOT DISCHARGED.**
Remediation NOT performed here — the registration itself requires "its own separately authorized, bounded gate";
a bounded remediation proposal (retargeting `UI_B_START_024`'s wording register only, domain-neutral, no Tier-1
translation work) is recorded for that future gate, not executed.

**Mechanical activation-readiness matrix (13 PASS / 1 OPEN / 1 outside scope / 1 Owner-decision-required):** D3,
P9-MECH-SF safety-cue family, CF-2, CF-6, ILT-002, L2SC-01, Path-N/domain-threading (`D-GMPR-D3-PN`), the
hard-coded electronics tie-break coupling (`D-GMPR-01-D-D3`/CF5-F004), CF5-F001/F002/F003 classifier/admission
boundaries, and NMF-1+FU-1 are all independently re-verified **PASS** this gate against their own closure/
discharge records. `L10N-RH-01` is **OPEN**. `L2SC-02` confirmed **OUTSIDE ACTIVATION-READINESS** (its own
registration: "NOT a Mechanical-activation blocker"). Explicit Owner Mechanical activation authorization is
**OWNER DECISION REQUIRED** — not requested, implied, or made by this record; the eventual decision needed is a
separate, explicit Owner authorization to add `"mechanical"` to `_ACTIVATED_DOMAINS`, governed by the existing
§5-I2 allowlist gate pattern. **Tier-1 EN/AR label = WAITING ON ACTIVATION-READINESS** — not yet "ready to
implement next," since `L10N-RH-01` remains the one open item before every other technical/governance readiness
condition is satisfied.

**Boundary / status.** Read-only reassessment; both mutation probes byte-verified reverted; `git diff --name-only`
confirms only `docs/governance/*.md` paths changed. Does NOT reopen `CF-2` (`FORMALLY CLOSED` stands), `CF-6`
(`FULLY DISCHARGED` stands), or `L2SC-01` (`FORMALLY CLOSED` stands); does NOT expand `L2SC-02` (still
registration-only); does NOT implement the Tier-1 label; does NOT activate Mechanical —
`activated_domains() == ['electronics_electrical']` unchanged, verified before and after every probe. **Phase 9
remains OPEN.** `OWNER_DECISION_REGISTER.md` UNCHANGED. Authoritative ONLY if/when this exact candidate is merged
and post-merge verified. Next required gate: a bounded, separately authorized `L10N-RH-01` remediation gate (or
an explicit Owner decision to defer its observations past activation) — the Tier-1 EN/AR label gate becomes
eligible only after that.

**Immediately prior (L2SC-01 formal closure gate, MATERIAL CORRECTION of rejected closure candidate `360f541`,
defect MD-C1 — accepted and merged via PR #498 `3b7783f`; retained as history):** The first closure-record
candidate,
`360f541caa075a3fd899bfd41ee48304e965f491`, was independently **REJECTED** (verdict: CLOSURE INVALID — MATERIAL
CORRECTION REQUIRED, defect **MD-C1** — its residual-obligations list incorrectly claimed `CF-6` and `CF-2`/the
ILT-002 public-message question remained live "OPEN" residuals, contradicting the authoritative current status
(`CF-6 = FULLY DISCHARGED`, `CF-2 = FORMALLY CLOSED`) and the same record's own closure statements). The reviewer
independently confirmed L2SC-01 itself is closure-ready and every other part of the record correct. That
candidate is preserved **immutable, unpushed, unamended** at `refs/rejected/l2sc01-formal-closure-360f541`. THIS
candidate returns to the exact authoritative parent `b8e1274c027707a38a85216b0ef7b43a1eda5e1c` and corrects only
the closure record's residual list — full detail in `docs/governance/L2SC01_FORMAL_CLOSURE_RECORD.md` §10/§7.C.

Base `b8e1274c027707a38a85216b0ef7b43a1eda5e1c` (PR #497 —
SHA-preserving merge of the accepted L2SC-01 runtime implementation MATERIAL CORRECTION candidate
`9399f9d179a547bc6a9cc3ea25f8d2a6b1c2c490` onto `c1cb421d73c53d24cc381ca9238e29613ca7e996`; merge tree ==
candidate tree; candidate→merge diff EMPTY — independently re-verified this gate). A full Remaining-Obligation /
Exit-Criteria Review was performed against the frozen contract's §15 closure criteria — full detail in the
dedicated closure record `docs/governance/L2SC01_FORMAL_CLOSURE_RECORD.md`. **Determination: CLOSURE JUSTIFIED.**
All in-scope criteria satisfied: registry field + accessor + engine consumption implemented exactly per the
frozen 3-pair Mechanical set (`piston`/`valve`/`actuator`); Electronics byte/behavior-identical (8 historical
pairs); the WARN-vs-PASS divergence proven closed for the authorized pairs through the real gap-closure state
machine; every §12/§13 test and probe passes, including the now-genuinely-behavioral MD-1/MD-A recurrence guard
(mutation probe 5 caught via `test_red_mechanical_rejected_alias_never_grants_reasoned[seal/verb-...]`, not
map-equality alone); full suite green (**2677 passed / 3 skipped / 1 xfailed / 0 failed**, fresh-verified this
gate); independent review accepted the exact frozen SHA; Owner acceptance evidenced by the completed merge
lifecycle. Architectural exit check found no defect (Domain Registry remains the sole structural validator,
alias ownership is pack-scoped, the shared engine is domain-neutral, exactly one live alias source exists, no
morphology, no cross-domain leakage, no classifier/admission/activation change, no new duplicate ownership seam,
no hash-pin weakening). Residual-obligation review found no in-scope item still open — `L2SC-02`, Tier-1 EN/AR,
and `L10N-RH-01` are confirmed separate, unaffected obligations.

**`L2SC-01` — Substance-Signal Plural-Alias Domain-Completeness — is now FORMALLY CLOSED**, effective on this
candidate's own merge and post-merge verification. Rejected candidates
`714d538fca7b22cb84e3b18802dcf27aa42e5707`, `219f7c10c4ba23f795f0461dd831f71052469e65`, and closure candidate
`360f541caa075a3fd899bfd41ee48304e965f491` (defect MD-C1) all remain immutable rejected evidence at their
respective `refs/rejected/*` — never authoritative implementation, not erased, not amended. **Changed paths:**
the corrected closure record, this AIC/roadmap/CPS sync, and a closure note in the
capability register's `L2SC-01` entry — **ZERO runtime/test/pack/registry/activation/schema/persistence diff**
(verified via `git diff --name-only`). `OWNER_DECISION_REGISTER.md` UNCHANGED (no new Owner decision required).
**Boundary:** does NOT reopen `CF-2` (`FORMALLY CLOSED` stands) or `CF-6` (`FULLY DISCHARGED` stands); does NOT
touch `D-CF6CF2-ILT002-01`; does NOT expand `L2SC-02` (still registration-only); does NOT implement Tier-1 (still
pending); does NOT perform the `L10N-RH-01` reassessment (still pending); does NOT activate Mechanical
(`activated_domains() == ['electronics_electrical']` unchanged); no D4/D8/THERM-01/Phase 10/PSRR/deployment.
**Phase 9 remains OPEN** — later roadmap obligations remain. Authoritative ONLY if/when this exact candidate is
merged and post-merge verified. Next required gate: **Mandatory Grill on this exact candidate** → independent
external exact-candidate review → Owner acceptance → SHA-preserving publication → PR → pre/post-merge
verification. After this closure merges, the next roadmap item is the **Tier-1 EN/AR Mechanical public label** —
not authorized or performed here.

**Immediately prior (L2SC-01 runtime implementation MATERIAL CORRECTION gate, candidate `9399f9d` — accepted and
merged via PR #497 `b8e1274`; retained as history):** independent external review REJECTED the runtime
implementation candidate `714d538fca7b22cb84e3b18802dcf27aa42e5707` (verdict: MATERIAL CORRECTION REQUIRED,
defect **MD-A** — the mandated MD-1 recurrence guard was not load-bearing: in 10 of 12 rejected-alias adversarial
sentences the alias word sat on the wrong directional side of its connective, never inspected by the gate, so
those guards passed regardless of alias state). The reviewer independently reconfirmed the runtime implementation
itself correct — Domain Registry validation, accessor ownership, single alias source, Electronics migration, the
exact 3-pair Mechanical set, absence of rejected aliases/morphology, cross-domain isolation, and end-to-end
parity all stand. That candidate is preserved **immutable, unpushed, unamended** at
`refs/rejected/l2sc01-runtime-impl-714d538`. The corrected candidate `9399f9d` returned to the exact authoritative
parent `c1cb421d73c53d24cc381ca9238e29613ca7e996` and reapplied the runtime/data changes from `714d538`
**byte-identically** (verified via `sha256sum` for all 5 runtime/data files — zero diff) — only
`tests/test_l2sc01_substance_signal_plural_alias.py` changed. All 10 vacuous sentences replaced with
direction-correct constructions, individually verified free of `_CAUSAL_STRUCTURE_PATTERNS`/other-substance
confounds; a new explicit three-way differential proof (clean map ASSERTED / poisoned map REASONED / neutral-
control map ASSERTED) added for all 12 excluded signals via `unittest.mock.patch`; §12.C tests renamed/re-
documented honestly as sentence-boundary/directional-discipline guards (not plural-specific false-positive
guards). **Hash-pin reconciliation: NONE required** — runtime/data byte-identical to `714d538`, whose pins
remained valid unchanged. **Suite:** focused L2SC-01 file 60 passed (was 36; +24); full governed suite 2677
passed / 3 skipped / 1 xfailed / 0 failed (prior baseline 2653/3/1/0; delta +24 passed, 0 regressions). All 5
mutation probes re-run CAUGHT; probe 5 independently, behaviorally provable via the poisoned-map differential
tests, not inferred from map-content assertions alone. Independently re-reviewed, accepted, published
SHA-preserving, and merged (PR #497, base `b8e1274`; merge tree == candidate tree).

**Immediately prior (L2SC-01 runtime implementation gate, candidate `714d538` — REJECTED by independent review,
defect MD-A; preserved immutable at `refs/rejected/l2sc01-runtime-impl-714d538`; retained as history):**
Owner-authorized runtime implementation of the frozen
`docs/governance/L2SC01_SUBSTANCE_SIGNAL_PLURAL_ALIAS_INCREMENT_CONTRACT.md`. Base
`c1cb421d73c53d24cc381ca9238e29613ca7e996` (PR #496). Implemented Option B exactly as frozen across
`engine/domain_registry.py`, `engine/domain_rules.py`, `engine/progression_loop.py`, both domain packs, a new
36-test focused file, and disclosed byte-freeze reconciliation across 5 `test_p9_mech_i*.py` files. Full suite at
that gate: 2653 passed / 3 skipped / 1 xfailed / 0 failed, all 5 mutation probes reported CAUGHT. Independent
review later found probe 5 and the §12.D adversarial guards were not genuinely load-bearing (defect MD-A, see
current status above) — the runtime implementation itself was NOT found defective and is carried forward
byte-identically into the corrected candidate above.

**Immediately prior (L2SC-01 bounded contract gate, MATERIAL CORRECTION of rejected candidate `219f7c1` —
governance-only, implements nothing; retained as history):** independent external review **REJECTED** the first bounded contract
candidate `219f7c10c4ba23f795f0461dd831f71052469e65` (verdict: MATERIAL CORRECTION REQUIRED, defect **MD-1** —
it authorized 9 Mechanical plural aliases using only "is this the grammatically normal plural?", without
screening for verb-form/idiom/meaning-shift false-positive risk; demonstrated examples: "the gasket seals the
joint", "the latch springs open", "the operator loses their bearings", "the plant gears up"). That candidate is
preserved **immutable, unpushed, unamended** at `refs/rejected/l2sc01-plural-alias-contract-219f7c1`. This gate
returns to the exact authoritative parent `c8e7af24adf2cee31104abc9c810d38e05569c52` (PR #495, parents `6c168a6`
+ accepted CF-2 closure candidate `4b45a3e`; merge tree == candidate tree) and creates a corrected candidate —
what independent review already accepted (the reconstruction, the domain-generic finding, Option B's selection,
electronics migration, `L2SC-02`) is NOT reopened or re-derived. **Corrected alias set — narrower than before:
3 of 15 Mechanical signals authorized** (`piston`, `valve`, `actuator` — no verb form, no idiom found; each
empirically re-verified to still reproduce the original `WARN`-vs-`PASS` divergence in a clean qualifying
sentence); **12 of 15 excluded** (`spring`/`seal`/`gear` — common-verb collision, reviewer-demonstrated;
`bearing` — idiom "loses their bearings", reviewer-demonstrated; `lever` — "levers of power/influence" idiom;
`hydraulic`/`pneumatic` — adjectival field-noun shift; `pressure`/`torque`/`friction` — mass/non-count nouns +
idiomatic shift; `compression` — re-evaluated under a corrected, pack-scoping-independent rationale, "chest
compressions" remains a real intra-session ambiguity; `mechanism` — RECLASSIFIED to excluded, its singular
already carries a pre-existing `AB-006` low-specificity flag and its plural is prone to generic non-substantive
usage). **Governance-text corrections beyond the alias table:** alias-map direction now stated consistently as
`alias → canonical signal` everywhere; the rejected candidate's inaccurate duplicate-JSON-key claim withdrawn
and replaced with a truthful, scoped description (`json.load`'s pre-existing last-value-wins behavior; raw
duplicate-key detection explicitly classified OUTSIDE this bounded increment); the contract now states
truthfully that structural validation proves only that an alias target EXISTS, never that the pairing is
SEMANTICALLY correct; migration-safety strengthened with independently re-verified evidence that none of the 8
existing electronics plural-alias singulars appears in `mechanical`/`medical_device`/`software`. **Corrected
test/mutation contracts:** new required authorized-alias false-positive guards and rejected-alias negative
guards; a new 5th mandatory mutation probe (introduce a known-ambiguous excluded alias into the authorized map
→ must go RED) directly protecting against MD-1 recurring. **Suite:** re-verified unchanged, 2616 passed / 3
skipped / 1 xfailed / 0 failed. **Changed paths:** the revised contract (same file path, corrected content, new
SHA), the `L2SC-01` amendment (now citing the rejected SHA) + `L2SC-02` registration in the capability register,
and this AIC/roadmap/CPS sync — **ZERO runtime/test/pack/registry/activation/schema/persistence diff**.
`OWNER_DECISION_REGISTER.md` UNCHANGED. **Boundary:** does NOT reopen `CF-2` (`FORMALLY CLOSED` stands) or
`CF-6` (`FULLY DISCHARGED` stands); does NOT touch `D-CF6CF2-ILT002-01`; does NOT touch `L10N-RH-01`; does NOT
expand `L2SC-02`; does NOT implement Tier-1; does NOT activate Mechanical
(`activated_domains() == ['electronics_electrical']` unchanged); no D4/D8/THERM-01/Phase 10/PSRR/deployment; no
P9 closure. Authoritative ONLY if/when this exact candidate is merged and post-merge verified. Next required
gate: **Mandatory Grill on this exact candidate** → independent external exact-candidate review → Owner
acceptance → SHA-preserving publication → PR → pre/post-merge verification; thereafter the separately-
authorized, HIGH-RISK `L2SC-01` bounded implementation gate (its own full create→freeze→Grill→independent-
review→Owner-acceptance→publication→PR→pre/post-merge-verification lifecycle — Fast Track explicitly NOT
authorized for that future gate).

**Immediately prior (CF-2 Full-Scope Formal Closure gate — MERGED via PR #495 `c8e7af24`; retained as
history):** the CF-2 Arabic Localization Remainder Fast Track candidate is **MERGED and post-merge verified**
(PR #494 → authoritative base
`6c168a62df4754c0ecea7e99ff6316b66c6dfdb7`, parents `cccbf30` + accepted candidate `c2a08dc`, merge tree ==
candidate tree; candidate→merge diff EMPTY) — full governed suite at that gate 2616 passed / 3 skipped / 1
xfailed / 0 failed, independently reviewed (ACCEPT WITH NON-BLOCKING OBSERVATIONS, SAFE FOR OWNER ACCEPTANCE
UNCHANGED: YES). This gate closes CF-2 using the authoritative evidence already accumulated across the CLI
remediation (PR #492/#493) and Arabic-localization remediation (PR #494) gates — it does NOT reconstruct or
reimplement either. **Canonical record:** `docs/governance/CF2_FULL_SCOPE_FORMAL_CLOSURE_RECORD.md`. **ILT-002
open question resolved:** `D-CF6CF2-ILT002-01` preserved an explicitly OPEN CF-2 question (whether a generic
session label could display "electronics" for arbitrary text on a fixed-domain route); this closure cites the
already-existing evidence (`CF2_CLI_REMAINDER_TRUTHFULNESS_CONTRACT.md` §6) that answered it — `state.domain` on
ILT-002 routes is ALWAYS `electronics_electrical` by fixed-domain design, never derived from posted text, so the
label describes the kind of review conducted, not a classification claim. TRUTHFUL; no CF-2 remediation surface;
`D-CF6CF2-ILT002-01` itself not reopened, altered, or reinterpreted. **Deferred-surface determination restated
(not re-litigated):** `decision_workspace.html` and `api_v1.py::_ERROR_MESSAGES` remain OUTSIDE CF-2 (no domain-
support claim; general localization-completeness, not CF-2 truthfulness). **Anti-forgetting registration:** one
new consolidated, non-numeric entry **`L10N-RH-01`** in `INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md`,
consolidating the Arabic gate's three independent-review non-blocking observations (broadened-activation
negative-semantic-guard test gap; `SERVICE_UNAVAILABLE` regression-guard test gap; present-confirm Arabic
checkbox wording, not production-reachable today) — registration only, NOT implemented, NOT framed as an
unresolved CF-2 defect, none of the three blocked this closure. **Changed paths:** this new closure record + the
new `L10N-RH-01` register section + `ACTIVE_EXECUTION_ROADMAP.md`/`ACTIVE_INCREMENT_CONTRACT.md`/
`CURRENT_PROJECT_STATE.md` sync — ZERO runtime/test/pack/registry/activation/schema/persistence diff.
`OWNER_DECISION_REGISTER.md` UNCHANGED. **Boundary:** does NOT reopen `CF-6` (`FULLY DISCHARGED` stands); does
NOT touch `D-CF6CF2-ILT002-01` or the ILT-002 routes; does NOT resolve or implement `L2SC-01`; does NOT
implement Tier-1; does NOT activate Mechanical; no D4/D8/THERM-01/Phase 10/PSRR/deployment; no P9 closure.
`activated_domains() == ['electronics_electrical']` unchanged. Authoritative ONLY if/when this exact candidate is
merged and post-merge verified. Next required gate: **Mandatory Grill on this exact candidate** → independent
external exact-candidate review → Owner acceptance → SHA-preserving publication → PR → pre/post-merge
verification; thereafter, in order: `L2SC-01`; the Tier-1 EN/AR label; `L10N-RH-01` reassessment as applicable;
explicit Owner Mechanical activation authorization; Mechanical activation + verification; Phase 9 formal
closure.

**Immediately prior (CF-2 Arabic Localization Remainder (Fast Track) implementation gate — MERGED via PR #494
`6c168a62`; retained as history):** the CF-2 CLI remainder implementation
candidate is **MERGED and post-merge verified** (PR #493 → authoritative base
`cccbf30cf6a851b0c7291c95c159f74520105d99`, parents `de85d101` + accepted candidate `23064fe`, merge tree ==
candidate tree) — this Fast Track gate combines reconstruction → implementation → tests → governance sync →
freeze → self-Grill into one candidate. **Fresh sweep:** confirmed and extended the known Arabic residual — five
raw `/start`-flow message constants (`UNSUPPORTED_DOMAIN_MESSAGE`, `CONFIRMATION_REQUIRED_MESSAGE`,
`MECHANISM_GUIDANCE_MESSAGE`, `DOMAIN_CHOICE_MESSAGE`, `SERVICE_UNAVAILABLE_MESSAGE`) bypassed
`ui_text.localize_message()` entirely; `_present_confirm_message()` and the six `_render_start_page`
generalized-context strings were always raw English regardless of `ui_lang`; the two `save_success_criteria`
`_reject()` messages had the same bypass shape. `domain_label.py`/ILT-002 reconfirmed truthful (no defect;
`D-CF6CF2-ILT002-01` unchanged) — a stale/inaccurate *comment* at `session.html:101-107` named as evidence only,
not edited. **Exact change:** the five static messages now route through `localize_message()`/`_MESSAGE_KEYS`
(new keys `UI_B_START_010..014`, `UI_B_SC_007..008`); the three dynamic producer functions and the generalized-
context block gained a `lang` parameter defaulting to `"en"` (every existing caller byte-identical to before;
Arabic uses new fixed catalogue keys `UI_B_START_020..031`, deliberately domain-neutral for any broadened-
activation state — no new Tier-1 label translation). **Tests:** 31 new focused tests in new file
`tests/test_cf2_arabic_localization_remainder.py`. **Mutation probes:** all 4 required probes CAUGHT (raw-
English-path reintroduction; catalogue-key removal; canonical-helper bypass; present-confirm byte-identity
corruption — this last probe initially exposed a genuine test-quality gap, a looser assertion masked by the
separately-rendered checkbox label, fixed by tightening to the isolated error paragraph and re-confirmed CAUGHT),
each reverted with SHA-256-verified byte-identical restoration. **Suite:** 2616 passed / 3 skipped / 1 xfailed /
0 failed (2585 baseline + 31 new; 0 regressions). **Scope:** changed paths `web/app.py`, `web/ui_text.py`, the
one new test file, governance sync only; every classifier/activation/persistence/routing/admission surface
byte-verified untouched. `OWNER_DECISION_REGISTER.md` UNCHANGED. **Two NEW residuals named/evidenced/deferred,
OUTSIDE CF-2's own scope:** `web/templates/decision_workspace.html` (standalone, zero localization wiring — a
materially larger separate undertaking) and `web/api_v1.py`'s `_ERROR_MESSAGES` (JSON surface, no `ui_lang`
concept) — neither asserts a domain-support claim, so neither is CF-2's specific truthfulness risk. **CF-2
closure assessment:** CF-2's own reconstructed scope has NO remaining residuals found this gate — CF-2
implementation obligations appear fully discharged, pending a separate concise formal closure step (NOT declared
here). **Boundary:** does NOT close CF-2 (a future closure gate confirms the decision_workspace.html/api_v1.py
scope-boundary judgment); does NOT reopen CF-6 (`CF-6 = FULLY DISCHARGED` stands); does NOT touch
`D-CF6CF2-ILT002-01`; does NOT touch the Tier-1 label; does NOT activate Mechanical; no D4/D8/THERM-01/Phase
10/PSRR/deployment; no P9 closure. `activated_domains() == ['electronics_electrical']` unchanged. Authoritative
ONLY if/when this exact candidate is merged and post-merge verified. Next required gate: **Mandatory Grill on
this exact candidate** → independent external exact-candidate review → Owner acceptance → SHA-preserving
publication → PR → pre/post-merge verification; thereafter the separately-authorized CF-2 concise formal closure
gate.

**Immediately prior (CF-2 CLI remainder truthfulness implementation gate — MERGED via PR #493 `cccbf30c`;
retained as history):** the CF-2 CLI remainder contract candidate is **MERGED and post-merge verified** (PR
#492 → authoritative base `de85d1010df8aaff8a67fb6f3d4a7ab5c93936bb`, parents `5355ed54` + accepted candidate
`27af00b5`, merge tree == candidate tree) — this gate implemented ONLY
`docs/governance/CF2_CLI_REMAINDER_TRUTHFULNESS_CONTRACT.md` §8: `activated = domain_activation.activated_domains()`
computed once at the top of `scripts/run_cli.py::run_cli()`, reused across the startup banner, the richer-kind
(`AMBIGUOUS_TIE`/`MULTI_DOMAIN_NEEDS_D4`/`UNRESOLVED_NON_ACTIVATED_TIE`) bounded-stop message, and the pre-
existing Step-3 admission check — byte-identical under `['electronics_electrical']`; truthful generalized copy
under a broader activation set; truthful no-domain-available copy under the empty-activation edge case. 8 new
focused tests in `tests/test_cf5_f003_classifier_matching_semantics.py`; all 4 required mutation probes CAUGHT.
Suite: 2585 passed / 3 skipped / 1 xfailed / 0 failed (2577 baseline + 8 new). Discharged ONLY its own narrow
two-defect increment — did NOT close CF-2 overall.

**Immediately prior (CF-2 public-message truthfulness full-remainder reconstruction & bounded CLI implementation
contract gate — MERGED via PR #492 `de85d101`; retained as history):** the CF-6 full-scope closure candidate is
**MERGED and post-merge verified** (PR #491 → authoritative base `5355ed54cbba17c16b5716865c1dc82e8b141941`,
parents `1fe05e09` + accepted candidate `11d9450f`, merge tree `8d6aeb75` == candidate tree) — `CF-6 = FULLY
DISCHARGED` authoritative; CF-2 remains OPEN. This gate performed the mandatory CF-2 full-remainder
reconstruction (canonical record: `docs/governance/CF2_CLI_REMAINDER_TRUTHFULNESS_CONTRACT.md`). **Reconstructed
CF-2 scope:** AMBIGUOUS_TIE/MULTI_DOMAIN_NEEDS_D4 user-facing treatment; generic unsupported messaging; future
public reachability; misleading domain claims; CLI copy; ILT-002 route copy; non-`/start` templates; Arabic
localization; any other public electronics-only assertion. **Full repository-wide sweep** (prose search beyond
the bare identifier + personal re-verification of every match): every `web/app.py` `/start`-flow message-CONTENT
truthfulness concern already correctly gated (the discharged F002 pattern); all 13 templates swept (12 clean;
`index.html`'s 5 occurrences bilingual + activation-gated). **Two confirmed CF-2 defects, both
`scripts/run_cli.py`:** the unconditional startup banner (`:39-41`) and the richer-kind bounded-stop message
(`:64-70`) — both outside the already-merged CLI facet's scope, verified at exact current content. **One
deferred CF-2-class item (materially different responsibility):** all five `/start`-flow error-path messages
bypass localization entirely (English-only regardless of language) — broader/more precise than the prior
"electronics-only-state-only" characterization (corrected here as a later clarification). **ILT-002
presentation:** TRUTHFUL (session "Review type" label describes the actual review conducted, not a
classification claim) — `D-CF6CF2-ILT002-01` unchanged. **`engine/progression_loop.py:415`:** classified
OUTSIDE CF-2/CF-6 (Owner-authorized internal scoring logic, not public copy) — registered as NEW anti-forgetting
entry **`L2SC-01`** (THERM-01 precedent; non-numeric; no CAP entry; no implementation). **Determination:
governance-only BOUNDED IMPLEMENTATION CONTRACT created** (not closure, not implementation) — §8 bounds a future
CLI-only remediation increment (byte-identical electronics-only output; truthful generalized/empty-activation
copy; richer-kind dispatch logic untouched; full test/mutation enumeration). Arabic gap and `L2SC-01` explicitly
NOT folded into this increment. **ZERO runtime/test/pack/registry/activation diff.** `CF-6 = FULLY DISCHARGED`
unchanged, not reopened; `MECHANICAL = P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS; NOT ACTIVATED` unchanged;
`activated_domains() == ['electronics_electrical']`; Tier-1 label untouched.

**Immediately prior (CF-6 full-scope closure gate — MERGED via PR #491 `5355ed54`; retained as history):**
**Status (prior — CF-6 FULL-SCOPE FORMAL CLOSURE CANDIDATE — `CF-6 = FULLY DISCHARGED` conditional on merge; CF-2
remains OPEN; Tier-1 untouched; Mechanical NOT ACTIVATED; ODR UNCHANGED):** the CF-6/CF-2 ILT-002 Owner-decision
candidate is **MERGED and post-merge verified** (PR #490 → authoritative base
`1fe05e098c5ecf53b63088e12e71549635ead70b`, parents `3570863e` + accepted candidate `a3e4300d`, merge tree
`bcb012b1` == candidate tree) — `D-CF6CF2-ILT002-01` authoritative. This gate performs the mandatory CF-6
full-scope confirming closure (canonical record: `docs/governance/CF6_FULL_SCOPE_FORMAL_CLOSURE_RECORD.md`).
**Reconstructed CF-6 scope** (adopted from `P9_E2_MULTI_ACTIVATED_DOMAIN_TIE_PRECEDENCE_FORMAL_CLOSURE_RECORD.md`
§7, the fullest earliest authoritative statement): Web `/start` strong-unsupported heuristics × canonical-
classifier reachability × activated-domain admission × ambiguity handling × Web/CLI/core consistency × (shared
with CF-2) public-message truthfulness. **Full-scope adversarial sweep** (independent read-only Explore-agent
discovery + personal classification of every match, six-category scheme): exhaustively covered every
`"electronics_electrical"` literal, every classifier/activation/admission call site, second-registry search,
template copy, cold-load/persistence seams, question-selection branching, every session-creation-capable script,
and every `infer_domain` reference across `web/* engine/* scripts/*`. **Result: ZERO `SHARED-CONSUMER — DEFECT`
items.** Every match resolved to canonical behavior (single classifier, single activation source, activation-
derived copy/templates, generic domain propagation, fail-closed cold-load restore, every session-creation site
tracing to `_admit_specialist_domain` or verbatim persisted-domain restoration), a governed exception (the
F002-reviewed weak-conflict branch at `web/app.py:1639`, explicitly comment-tagged "CF5-F002 (CF-6 facet)"; the
three ILT-002 routes; the E-2/ILT-002 tooling), an already-closed separate tracker (`D-GMPR-01-D-D3`; `CF5-F001`;
`CF-3`/`CF5-F004`), legitimate domain-specific scoring content, or genuinely out-of-scope material (`DOMAIN_
CONFIRM_VALUE` — zero production readers, confirmed; `scripts/run_summary_demo.py` — never touches the
classifier/activation/admission chain; a stale test-file comment). **CLI facet: DISCHARGED** (merge `6524e792…`).
**ILT-002 facet: RESOLVED BY OWNER DECISION, not a defect** (merge `1fe05e09…`). **Determination: `CF-6 = FULLY
DISCHARGED` for its authoritative reconstructed scope**, conditional on merge + post-merge verification. Full
suite **2577 passed / 3 skipped / 1 xfailed / 0 failed** (fresh, unchanged; ZERO runtime/test/pack/registry/
activation/schema/persistence diff this candidate — no mutation probes needed, no new behavior asserted).
**CF-2 remains globally OPEN** (own full-scope sweep, ILT-002 residual truthfulness question, Arabic
localization, non-`/start` sweep all untouched). Tier-1 label untouched; **Mechanical remains NOT ACTIVATED**;
`activated_domains() == ['electronics_electrical']`; Phase 9 remains OPEN. No D4/D8/THERM-01/Phase 10/PSRR/
deployment. Authoritative ONLY if/when this exact candidate is merged and post-merge verified. Next required
gate: **Mandatory Grill on this exact candidate** → independent external exact-candidate review → Owner
acceptance → SHA-preserving publication → PR → pre/post-merge verification.

**Immediately prior (CF-6/CF-2 ILT-002 Owner-decision gate — MERGED via PR #490 `1fe05e09`; retained as history):**
**Status (prior — CF-6/CF-2 ILT-002 FIXED-DOMAIN PROTOCOL — OWNER DECISION RECORDED (`D-CF6CF2-ILT002-01`) —
governance-only; classifier-consistency ambiguity RESOLVED; CF-6/CF-2 remain OPEN; Tier-1 untouched; Mechanical
NOT ACTIVATED):** the CF-6/CF-2 ILT-002 reconstruction & correction candidate is **MERGED and post-merge
verified** (PR #489 → authoritative base `3570863ef9519f123c76fb1f165452e4935365e3`, parents `6524e792` +
accepted corrected reconstruction candidate `0587c7b6`, merge tree `d3bab7fd` == candidate tree). This gate
records the Owner's explicit decision resolving that record's flagged ambiguity, per repository precedent (the
D-CF5-F002-01/D-P9-MECH-02/D-THERM-01 ODR-entry pattern — no duplicate governance framework):
`OWNER_DECISION_REGISTER.md` entry **`D-CF6CF2-ILT002-01`**. **Owner decision (all eight points, exact):** the
three `start_ilt002_*` routes remain intentional fixed-domain scenario/evidence routes; their hardcoded
`electronics_electrical` selection is a governed protocol invariant, NOT a classifier defect; activation
enforcement via `_admit_specialist_domain()` continues unchanged; no classifier-driven routing without a future
explicit Owner decision; no duplicate activation checks; existing ILT-002/E-2 evidence semantics and persistence
meaning preserved unchanged; the prior CF-6 classifier-consistency ambiguity is RESOLVED in favor of the
fixed-domain protocol (the ILT-002 classifier-remediation item narrowly removed from CF-6's technical-remediation
list); explicitly NOT a global closure of CF-6 or CF-2, NOT a waiver of either tracker's unrelated remainder, NOT
Mechanical activation, NOT Tier-1 authorization, NOT Phase 9 closure. **CF-6 effect:** the ILT-002 item is
removed from its technical-remediation list; **CF-6 remains OPEN** (open-ended full-scope confirmation
unaffected, own future closing gate required). **CF-2 effect:** the independent-review-identified truthfulness
question (whether a generic session/public label could display "electronics" for arbitrary text on an unlinked
fixed-domain route) is explicitly PRESERVED, unresolved, for CF-2's own future full-scope sweep; **CF-2 remains
OPEN** (ILT-002 route-copy item stays on its residual list; Arabic localization + non-`/start` sweep untouched).
**ZERO runtime/test/pack/registry/activation/schema/persistence diff** — no ILT-002 route, `_admit_specialist_
domain`, E-2 tooling, engine, or test file touched. `activated_domains() == ['electronics_electrical']`;
**Mechanical remains NOT ACTIVATED**; Tier-1 label untouched. No D4/D8/THERM-01/Phase 10/PSRR/deployment; no P9
closure. Authoritative ONLY if/when this exact candidate is merged and post-merge verified. Next required gate:
**Mandatory Grill on this exact candidate** → independent external exact-candidate review → Owner acceptance →
SHA-preserving publication → PR → pre/post-merge verification.

**Immediately prior (CF-6/CF-2 ILT-002 reconstruction & correction gate — MERGED via PR #489 `3570863e`; retained
as history):**
**Status (prior — CF-6/CF-2 ILT-002 SHARED-FACET RECONSTRUCTION & CORRECTION — CORRECTED CANDIDATE (first
candidate `cad135c5` self-rejected, preserved) — governance-only; NO implementation authorized; Owner decision
required before any further ILT-002 gate; Tier-1 untouched; Mechanical NOT ACTIVATED; ODR UNCHANGED):** the
CF-6/CF-2 CLI shared-facet implementation is **MERGED and post-merge verified** (PR #488 → authoritative base
`6524e792786644d3053aeac650bdfa7888ad0653`, parents `305961ae` + accepted CLI implementation candidate `6f1ad899`,
merge tree `4b8b191f` == candidate tree) — CF-6's and CF-2's CLI facets are DISCHARGED; both trackers remain
globally OPEN. **Lineage:** first reconstruction candidate `cad135c5` self-Grilled and self-REJECTED — a
post-freeze re-sweep found two consumer-tooling files (`scripts/e2_exact_matcher.py`,
`scripts/e2_path_n_smoke_runner.sh`) the frozen candidate's hidden-surface table had omitted, even though
including them only strengthens the same conclusion — preserved immutable; this corrected candidate from the SAME
parent completes the sweep table. This gate performs the mandatory ILT-002 hidden-surface reconstruction
(canonical record:
`docs/governance/CF6_CF2_ILT002_FACET_RECONSTRUCTION_AND_CORRECTION_RECORD.md`) and finds a **CRITICAL
CORRECTION**: the ILT-002 legacy routes' hardcoded `"electronics_electrical"` domain selection is GOVERNED,
INTENTIONAL, TESTED behavior — `tests/test_web_app.py::test_governed_ilt002_routes_remain_electronics_pinned_
after_restriction` explicitly asserts these routes must stay electronics-pinned regardless of submitted content;
a companion test pins the exact downstream domain-specific question text; commit-history and the separate
ILT-002 evidence-ledger governance apparatus confirm these are fixed-domain scenario routes whose transcripts
depend on the fixed domain — NOT a technical-debt bug analogous to the CLI facet. **Corrected-candidate finding:**
a SECOND, independent, Owner-authorized "E-2 Path N smoke runner" (`scripts/e2_path_n_smoke_runner.sh`) also
depends on this exact route's fixed domain via a verbatim fixed-response/exact-match evidence procedure —
further corroborating the governed design. Activation enforcement already fully exists
(`_admit_specialist_domain` → `is_activated`, per D-S5-03, unchanged from the prior gate's finding). Exhaustive
hidden-surface sweep: three routes confirmed exhaustive (no fourth); a fresh repo-wide `ilt002` reference sweep
across `web/ engine/ scripts/` found exactly the routes plus the two consumer-tooling scripts (both OUT OF SCOPE);
the nine previously-identified test files individually classified, none requiring change; persisted
`confirmed_domain` and the question-text pin confirmed load-bearing; zero hash/snapshot pins exist; the P4-1b-2a
durability coupling confirmed out of scope and not reopened; zero template/copy surface found (CF-2's "route
copy" item reassessed likely moot, not closed). **Determination: NO implementation gate created or authorized**
— any further ILT-002 work requires an explicit Owner decision on whether the fixed-domain design should ever
change. **CF-6 remains globally OPEN** (ILT-002 item now Owner-input-pending); **CF-2 remains globally OPEN**
(ILT-002 item reassessed likely moot but not closed; Arabic localization + non-`/start` sweep fully outstanding).
Tier-1 label untouched. **Mechanical remains NOT ACTIVATED**; `activated_domains() ==
['electronics_electrical']`. ZERO runtime/test/pack/registry/activation/ODR diff. Authoritative ONLY if/when this
exact candidate is merged and post-merge verified. Next required gate: **Mandatory Grill on this exact
candidate** → independent external exact-candidate review → Owner acceptance → SHA-preserving publication → PR →
pre/post-merge verification. No further ILT-002 gate should be attempted until the Owner reviews this record.

**Immediately prior (CF-6/CF-2 CLI shared-facet implementation gate — MERGED via PR #488 `6524e792`; retained as
history):**
**Status (prior — CF-6/CF-2 CLI SHARED-FACET IMPLEMENTATION CANDIDATE — facet DISCHARGED for both trackers
conditional on merge; ILT-002 deferred; Tier-1 untouched; Mechanical NOT ACTIVATED; ODR UNCHANGED):** the corrected
CF-6/CF-2 CLI shared-facet scoping contract is **MERGED and post-merge verified** (PR #487 → authoritative base
`305961aefe70056e94fa7d6f3260eb6bfc08840d`, parents `2b985844` + accepted corrected scoping candidate `f496d731`,
merge tree `20a10ca2` == candidate tree). This gate DELIVERS the contract's §4 bounded increment exactly:
`scripts/run_cli.py`'s hardcoded `if domain != "electronics_electrical":` replaced with activation-derived
admissibility (`domain_activation.activated_domains()`, reused unchanged; no new admission mechanism); two local
presentation helpers mirroring `web/app.py`'s shape WITHOUT importing it; Electronics-only refusal/confirmation
copy byte-identical (explicit conditional branch); truthful multi-domain and empty-activation copy added;
classifier-dispatch richer-kind branches untouched. Four new pinned tests in the SAME contract-named reconciliation
file (`tests/test_cf5_f003_classifier_matching_semantics.py`). **ILT-002 (`web/app.py`, incl.
`_admit_specialist_domain`), `web/domain_label.py`, every engine file, every domain pack, and every other test are
byte-unchanged** (diff confirms exactly 2 files touched). Evidence: fresh exhaustive sweep confirmed the same six
pre-existing CLI tests, zero flips; focused **134** (130 + 4 new); full suite **2577 passed / 3 skipped / 1
xfailed / 0 failed** (base 2573 + 4, zero regressions); mutations m1–m6 (hardcode reintroduction; activation-truth
bypass; unactivated-domain acceptance; stale copy; silent Electronics fallback; confirmation-copy mishandling) ALL
CAUGHT with byte-verified restoration. **CF-6's CLI facet = DISCHARGED; CF-2's CLI facet = DISCHARGED** — neither
tracker closed as a whole: **CF-6 remains OPEN** (ILT-002 + open-ended remainder); **CF-2 remains OPEN** (ILT-002,
Arabic localization, non-`/start` sweep). ILT-002 NOT touched, NOT discharged, NOT implied discharged — its own
future joint gate, unchanged. **Mechanical NOT ACTIVATED**; `activated_domains() == ['electronics_electrical']`;
Tier-1 label untouched. No D4/D8/THERM-01/Phase 10/PSRR/deployment; no P9 closure. Authoritative ONLY if/when this
exact candidate is merged and post-merge verified. Next required gate: **Mandatory Grill on this exact
candidate** → independent external exact-candidate review → Owner acceptance → SHA-preserving publication → PR →
pre/post-merge verification.

**Immediately prior (CF-6/CF-2 CLI scoping-contract gate — MERGED via PR #487 `305961ae`; retained as history):**
**Status (prior — CF-6/CF-2 CLI SHARED-FACET SCOPING CONTRACT — CORRECTED CANDIDATE (first candidate `71c16d53`
REJECTED, preserved) — governance-only; implementation NOT started; ILT-002 facet deferred; Tier-1 label untouched;
Mechanical NOT ACTIVATED; ODR UNCHANGED):** the CF-5 NMF-1/FU-1 test-hardening candidate is **MERGED and
post-merge verified** (PR #486 → authoritative base `2b985844f093b2730fa6618e6ee2d29e32c87af8`, parents `91f4e5c6`
+ accepted candidate `1ea78443`, merge tree `2d43c53e` == candidate tree) — NMF-1/FU-1 DISCHARGED; three non-Owner
blockers remain (Tier-1 label; CF-6; CF-2). **Lineage:** first scoping candidate `71c16d53` independently REJECTED
— a fabricated/misattributed quotation (falsely attributed to `CF5_F002_CF6_WEB_ADMISSION_CORRECTIVE_CONTRACT.md`
§5; the real text is in `P9_MECHANICAL_DOMAIN_QUALIFICATION_CONTRACT.md` §12, an unrelated D-GMPR/Mechanical
context) and a technical mischaracterization of the ILT-002 routes as bypassing activation (`_admit_specialist_
domain` DOES enforce `domain_activation.is_activated`, verified; only classification/domain-selection is
bypassed, consistent with `OWNER_DECISION_REGISTER.md` D-S5-03) — preserved immutable; this corrected candidate
from the SAME parent removes the fabricated quote (replaced with an explicitly-labeled inference from the F002
precedent's actual behavior), corrects the ILT-002 characterization, and reconciles the P9-MECH-SF contract's
"one CLI-literal facet" summary as INCOMPLETE (not invalid). Dependency graph unchanged in substance: label
correctly last; CF-6/CF-2 share TWO code-level facets — the CLI's hardcoded electronics-only check (a genuine
activation-truth bypass — the CLI never consults `activated_domains()`) and the ILT-002 routes' hardcoded domain
selection (activation-BOUND via `_admit_specialist_domain`; only classification is bypassed). One joint gate
naming both owners may operate on a shared facet without closing either lane (inference from the F002/CF-6
precedent's behavior). **Scoped to the CLI facet only** (4 touching test files vs. ILT-002's 9, a
durability/persistence-adjacent P4-1b-2a surface) — ILT-002 explicitly DEFERRED to its own future joint gate,
technically corrected, with an explicit instruction that its future gate must NOT add a duplicate activation
check. Delivers (governance only): the bounded future CLI-facet implementation's exact definition; a preliminary
six-test/four-file reconciliation sweep; explicit non-effects. **Expected discharge effect of THIS contract:
NONE** — it fences the future implementation only. **ZERO runtime/test/pack/registry/activation diff.**
Implementation NOT authorized by this contract. `MECHANICAL = P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS; NOT
ACTIVATED` unchanged; `activated_domains() == ['electronics_electrical']`. Authoritative ONLY if/when this exact
candidate is merged and post-merge verified. Next required gate: **Mandatory Grill on this exact candidate** →
independent external exact-candidate review → Owner acceptance → SHA-preserving publication → PR → pre/post-merge
verification; thereafter the separately-authorized CLI-facet implementation gate.

**Immediately prior (CF-5 NMF-1/FU-1 test-hardening gate — MERGED via PR #486 `2b985844`; retained as history):**
**Status (prior — CF-5 NMF-1/FU-1 BOUNDED TEST-HARDENING EXECUTION CANDIDATE — both DISCHARGED conditional on
merge; Mechanical NOT ACTIVATED; ODR UNCHANGED):** the P9-MECH-SF formal closure is **MERGED and post-merge
verified** (PR #485 → authoritative base `91f4e5c6ad69964d01328e1502ab04d1d76aa0c0`, parents `1a23552b` +
accepted closure candidate `c25c8438`, merge tree `36e2c030` == candidate tree) — OD-M2 clause 3 is DISCHARGED;
Mechanical remains `P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS; NOT ACTIVATED` with four non-Owner blockers
remaining (Tier-1 EN/AR label; CF-6; CF-2; NMF-1/FU-1 disposition). This gate reconstructs their dependency graph
(all mutually independent; label correctly LAST — P9-MECH-QC §13 truthful only at activation-readiness; CF-6/CF-2
each broad not-yet-scoped lanes with separate owners, sharing one CLI-literal facet dischargeable together per
the F002 precedent but needing their own future scoping contract; **NMF-1/FU-1 = the smallest, already-fully-
specified, lowest-risk item — no further scoping needed**) and DELIVERS the "bounded standalone test-only
hardening gate" the CF-5 Audit closure record named as their earliest gate (canonical record:
`docs/governance/CF5_NMF1_FU1_TEST_HARDENING_DISPOSITION_RECORD.md`). Delivered: NMF-1 — 3 new pinned tests in
`tests/test_cf5_f003_classifier_matching_semantics.py` (reorder rejection; intermediate-token-pluralization
rejection; the permitted final-token contrast); FU-1 — 1 new pinned test in `tests/
test_cf5_f002_web_admission_multidomain.py` (empty-activation-set fail-closed boundary via the file's existing
`activate()` double). **ZERO engine/web/CLI/domain/pack/provenance/registry/activation/schema/persistence diff**
— runtime required no change. Evidence: focused 112 (108 + 4 new); full suite **2573 passed / 3 skipped / 1
xfailed / 0 failed** (base 2569 + 4, zero regressions); mutation probes (reorder tolerance; intermediate-token
pluralization tolerance; wrong refusal message) ALL CAUGHT with byte-verified restoration. **NMF-1 = DISCHARGED
(executed); FU-1 = DISCHARGED (executed)** — conditional on this candidate's merge + post-merge verification;
Mechanical's own blocker set unchanged by this gate (NMF-1/FU-1 are CF-5-lane items, not Mechanical-lane items).
Remaining activation blockers after this gate: Tier-1 EN/AR label; CF-6; CF-2; explicit Owner activation
authorization. No Tier-1/CF-6/CF-2 work performed; `scripts/run_cli.py` untouched; no D4/D8/THERM-01/Phase
10/PSRR/deployment; no P9 closure; no activation change. `activated_domains() == ['electronics_electrical']`.
Authoritative ONLY if/when this exact candidate is merged and post-merge verified. Next required gate:
**Mandatory Grill on this exact candidate** → independent external exact-candidate review → Owner acceptance →
SHA-preserving publication → PR → pre/post-merge verification.

**Immediately prior (P9-MECH-SF formal closure gate — MERGED via PR #485 `91f4e5c6`; retained as history):**
**Status (prior — P9-MECH-SF FORMAL CLOSURE CANDIDATE — OD-M2 clause-3 activation blocker = DISCHARGED
conditional on this candidate's own merge; Mechanical NOT ACTIVATED; ODR UNCHANGED):** the P9-MECH-SF
implementation is **MERGED and post-merge verified** (PR #484 → authoritative base
`1a23552b75d68fac3741876651669e6192180b50`, parents `d1b79ef4` + accepted implementation candidate `2269d2d4`,
merge tree `85a920e6` == candidate tree) — the governed Mechanical safety-cue family EXISTS and is authoritative.
This gate records the **formal closure candidate** (canonical record:
`docs/governance/P9_MECH_SF_FORMAL_CLOSURE_RECORD.md`): fresh verification at this base (family True; focused
suites 23/18/17/18/20/16 + F001 **13** [the accurate count, correcting the Creator report's transcription error
per the independent review] + D3 7 + D-GMPR 15; full suite **2569/3/1/0**; cascade complete; signal inventory
unchanged `860ce084…`/`c14ae2d5…`; pack anchors `a8a56450…`; PR005 present; `activated_domains() ==
['electronics_electrical']`; `support_state("mechanical") == "recognized_not_activated"`) → conditional on this
candidate's merge + post-merge verification, **OD-M2 clause 3 (D-P9-MECH-02) is DISCHARGED** — evidence discharge
only; NO activation authorization granted, implied, or advanced. Status unchanged in kind: **`MECHANICAL = P9-QS
QUALIFIED — WITH ACTIVATION BLOCKERS; NOT ACTIVATED`** (the blocker set shrinks by exactly one). Five reviewer
observations preserved as observations (F001 count; context_terms shape-parity/unreachable; PR002 origin vs PR005
cascade lineage; inherited conservative-miss/negation semantics; additive governance note) — none converted into a
blocker. Remaining activation blockers (none waived/combined/executed here): Tier-1 EN/AR label; CF-6; CF-2;
NMF-1/FU-1 disposition (due no later than the pre-activation readiness review); explicit Owner activation
authorization. Governance-only: ZERO runtime/test/pack/provenance/registry/activation/ODR diff. Authoritative ONLY
if/when this exact candidate is merged and post-merge verified. Next required gate: **Mandatory Grill on this
exact candidate** → independent external exact-candidate review → Owner acceptance → SHA-preserving publication →
PR → pre/post-merge verification.

**Immediately prior (P9-MECH-SF implementation gate — MERGED via PR #484 `1a23552b`; retained as history):**
**Status (prior — P9-MECH-SF IMPLEMENTATION CANDIDATE — the governed Mechanical safety-cue family EXISTS in this
candidate (OD-M2 clause 3 executed as contracted); Mechanical NOT ACTIVATED; ODR UNCHANGED):** the corrected
P9-MECH-SF contract is **MERGED and post-merge verified** (PR #483 → authoritative base
`d1b79ef4548211dc5e6c881f8c27d994827a4591`, parents `cac658d7` + corrected contract candidate `349856de`, merge
tree `a1d11991` == candidate tree; first contract candidate `cfab650f` remains preserved immutable rejected
evidence). This gate DELIVERS the contract's ONE bounded increment exactly: the additive governed `mechanical`
F001-seam family in `engine/safety_signal.py` (electronics-precedent shape; provenance-tagged hazard vocabulary
54/44/45/23 cues under §3 — hazard-class grounded, lay-accessible, detection-scoped ONLY, equality-pinned, zero
electronics-identity collision, zero thermal vocabulary; electronics family/constants/None-default
byte-preserved); the MANDATORY same-increment declaration truthfulness cascade in the mechanical pack (the two
"NOT COVERED pending…" statements → the truthful detection-scoped boundary statement; covered detection entry +
supported category added; "safety determination" stays NOT COVERED; I1 lexicon guard passes; signals/gap
types/nuances/aliases byte-frozen by canonical-hash proof); NEW 23-test evidence file
`tests/test_p9_mech_safety_cue_family.py`; additive `mechanical:PR005`; and EXACTLY the §4 reconciliations in
EXACTLY the seven permitted files (I1–I4 absence pins flipped; F001 capability-query + r1 reconciled with
`software` as the family-less example; I1 declaration pins re-pinned; I2/I3 declaration hashes re-frozen
b5452a99…/9dd7a4cc…; I4 AND I5 pack anchors re-frozen a8a56450… under the ONE signal-inventory-unchanged proof, no
corpus rebuild; the four vocabulary-conditional derive-() pins verified UN-flipped with disclosed premise
comments). Evidence: RED/GREEN; 24/24 electronics + None derivation-corpus byte-parity; full suite **2569 / 3 / 1
/ 0** (baseline 2546 + 23 new, zero regressions); mutations m1–m10 ALL CAUGHT right-reason (pycache discipline;
byte-verified restoration); flip sweep grep-proven clean; scope exactly the contract set. DETECTION only — never a
safety determination; THERM-01 untouched; admission untouched; **Mechanical NOT ACTIVATED**; `activated_domains()
== ['electronics_electrical']`. OD-M2 clause-3 blocker discharge happens ONLY at the lane closure after this
candidate merges + post-merge verifies. Authoritative ONLY if/when this exact candidate is merged and post-merge
verified. Next required gate: **Mandatory Grill on this exact candidate** → independent external exact-candidate
review → Owner acceptance → SHA-preserving publication → PR → pre/post-merge verification.

**Immediately prior (P9-MECH-SF corrected contract gate — MERGED via PR #483 `d1b79ef4`; retained as history):**
**Status (prior — P9-MECH-SF: GOVERNED MECHANICAL SAFETY-CUE FAMILY CONTRACT — CORRECTED CANDIDATE (first
candidate `cfab650f` REJECTED, preserved) — OD-M2 CLAUSE 3; governance-only; implementation NOT started; Mechanical
NOT ACTIVATED; ODR UNCHANGED):** the terminal qualification record is **MERGED and post-merge verified** (PR #482 →
authoritative tip `cac658d70b841772b1a496b60b65a2da4309814a`, parents `ac8ac2d9` + accepted candidate `dd7b4878`,
merge tree `178c5dbb` == candidate tree → **`MECHANICAL = P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS; NOT
ACTIVATED`** authoritative; qualification blockers NONE; the six activation blockers recorded). This gate records
the **P9-MECH-SF contract — CORRECTED candidate** (canonical record:
`docs/governance/P9_MECH_SAFETY_CUE_FAMILY_CONTRACT.md`) — the FIRST activation-blocker gate per the qualification
record's own ordering. **Lineage:** first candidate `cfab650f` independently REJECTED (sole material defect: the
"exhaustive" §4 flip inventory missed the CERTAIN I5 full-pack hash flip —
`test_pack_bytes_frozen_incl_i4_validity_anchor` byte-pins the mechanical pack, which the mandatory declaration
cascade changes — and omitted `tests/test_p9_mech_i5_question_sufficiency.py` from the permitted reconciliation
files) and preserved immutable; this corrected candidate from the SAME parent fixes exactly that plus the
non-blocking precision clarifications (F001 `test_red_r1` = CERTAIN, mechanical being its family-less example; the
four vocabulary-conditional F001/D3 derive-() pins named explicitly; the I1 forbidden-covered lexicon guard
restated as an implementation constraint). Dependency graph (unchanged): the five non-Owner blockers are mutually
independent; safety family first (the only Mechanical-lane engineering-content item); label last
(activation-readiness edge); CF-6/CF-2 separate shared-surface lanes (shared CLI facet dischargeable per the F002
facet precedent); NMF-1/FU-1 disposition due no later than the pre-activation readiness review;
hidden-prerequisite sweep clean. Contract: ONE bounded implementation — the additive F001-seam `mechanical` family
(electronics-precedent shape; objective vocabulary criteria — hazard-class relevant, lay-accessible,
detection-scoped, no electronics collision, no thermal claim, I1-lexicon-guard compatible) PLUS the mandatory
declaration truthfulness cascade in the same increment + new evidence file + additive provenance + the CORRECTED
EXHAUSTIVE reconciliation set: 6 certain family-presence flips (I1/I2/I3/I4 absence pins + F001 capability-query +
F001 `test_red_r1`); 5 certain declaration surfaces (I1 declaration pins; I2/I3 frozen-field hashes; BOTH
mechanical full-pack anchors — I4 corpus validity anchor AND the I5 pack-bytes pin — re-frozen under ONE
signal-inventory-unchanged proof, no corpus rebuild unless the actual signal inventory changes); 4
vocabulary-conditional derive-() pins (D3-A; F001 `test_red_r2`; the F001 family-less-loop MECH branch; the F001
MECH-envelope cold-load pin); an EXACT permitted-reconciliation-file list (7 files); mandatory pre-freeze
flip-sweep; anything beyond = STOP. **Implementation NOT authorized by this contract.** On the future lane
closure, OD-M2 clause-3 = DISCHARGED with the remaining blockers (label, CF-6, CF-2, NMF-1/FU-1, Owner
authorization) restated — none moved here. Mechanical NOT ACTIVATED; Electronics unaffected; no
D4/D8/THERM-01/Phase 10/PSRR/deployment; no P9 closure. Governance-only: ZERO
runtime/test/pack/registry/activation/ODR diff. `activated_domains() == ['electronics_electrical']`; first
new-domain activation remains BLOCKED. Authoritative ONLY if/when this exact candidate is merged and post-merge
verified. Next required gate: **Mandatory Grill on this exact candidate** → independent external exact-candidate
review → Owner acceptance → SHA-preserving publication → PR → pre/post-merge verification.

**Immediately prior (P9-MECH terminal qualification gate — record MERGED via PR #482 `cac658d7`; retained as
history):**
**Status (prior — P9-MECH TERMINAL §15/§16 QUALIFICATION RECORD CANDIDATE — governance-only; MECHANICAL = P9-QS
QUALIFIED WITH ACTIVATION BLOCKERS conditional on merge; NOT ACTIVATED; ODR UNCHANGED):** the D-GMPR-D3-PN **formal
closure** is **MERGED and post-merge verified** (merge `ac8ac2d9fd17135befb990890dd57e838c24b671`, parents
`17a4aca4` + accepted closure candidate `be40cc90`, merge tree `9a2da541` == candidate tree → **D-GMPR-01-D-D3 =
FULLY DISCHARGED authoritative**; §12(b) unblocked). This gate records the **terminal qualification record
candidate** (canonical record: `docs/governance/P9_MECH_QUALIFICATION_RECORD.md`): every P9-MECH-QC §15 criterion
evidence-proven with exact SHAs (I1 `f595fb60`; I2 `3d51bb1c`; I3 `32165caf`; I4 `3fe23a8c`; I5 `baee2542`; D-GMPR
impl `add3561f`); fresh verification at this base — 104 mechanical evidence tests + full suite 2546/3/1/0; **§12(b)
NOW RECORDED COMPLETE** (dependency fully discharged; service factual); **§8.4 CONFIRMED** (annotation stands;
weight unread; cross-pack residual with its shared-core owner); OD-M2 per B-hardened (clause 1 = I1 declarations;
clause 2 = the record's PROMINENT header annotation — no unannotated QUALIFIED claim; clause 3 = ACTIVATION-ONLY,
not executed). Determination, authoritative ONLY after this candidate's own merge + post-merge verification:
**`MECHANICAL = P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS`**, declared relative to the truthful declared
concept-level scope. **OUTSTANDING ACTIVATION BLOCKERS (none waived): OD-M2 clause-3 safety-cue family; Tier-1
EN/AR label; CF-6; CF-2; NMF-1/FU-1; explicit Owner activation authorization.** Qualification ≠ authorization ≠
activation; `activated_domains() == ['electronics_electrical']`; Mechanical NOT ACTIVATED; first new-domain
activation remains BLOCKED. Separate owners unaffected (weight residual; progression_loop comment hygiene; THERM-01;
CAP-12/13; WS-PFV-001; D4; D8; Phase 10; PSRR; deployment). Governance-only: ZERO runtime/test/pack/registry/
activation/schema/persistence/ODR diff. Authoritative ONLY if/when this exact candidate is merged and post-merge
verified. Next required gate: **Mandatory Grill on this exact candidate** → independent external exact-candidate
review → Owner acceptance → SHA-preserving publication → PR → pre/post-merge verification; thereafter the next Owner
decisions are the activation-blocker gates (safety-family first among them), each separately authorized.

**Immediately prior (D-GMPR-D3-PN closure gate — closure MERGED via `ac8ac2d9`; retained as history):**
**Status (prior — D-GMPR-D3-PN FORMAL CLOSURE CANDIDATE — governance-only; path_n_questions coupling DISCHARGED /
D-GMPR-01-D-D3 FULLY DISCHARGED conditional on this candidate's merge; §12(b) UNBLOCKED not closed; Mechanical NOT
qualified / NOT activated; ODR UNCHANGED):** the D-GMPR-D3-PN **implementation** is **MERGED and post-merge
verified** (merge `17a4aca421752ddcd9004a1e929f3d2506438c75`, parents `96559534` + accepted implementation candidate
`add3561f`, merge tree `7852244d` == candidate tree → the domain-neutral canonical Path-N seam, the verbatim
mechanical artifact, the 15-test evidence file, and EXACTLY the five enumerated reconciliations are AUTHORITATIVE;
electronics byte-identical 34/34; suite 2546/3/1/0). This gate records the **FORMAL CLOSURE candidate** (canonical
record: `docs/governance/DGMPR_D3_PATH_N_DOMAIN_NEUTRAL_SERVICE_FORMAL_CLOSURE_RECORD.md`): (1) implementation
AUTHORITATIVE; (2) the `path_n_questions` coupling of `D-GMPR-01-D-D3` DISCHARGED — the LAST open coupling, so
**D-GMPR-01-D-D3 = FULLY DISCHARGED** for its registered scope (web-admission/safety_signal/tie-break discharged by
F002/F001/F004); (3) **P9-MECH §12(b) UNBLOCKED and factually served — UNBLOCKED ≠ CLOSED** (recorded complete only
at the Mechanical lane's terminal §15/§16 gate); (4) Mechanical NOT QUALIFIED (terminal §15/§16 outstanding incl.
§12(b) recording, §8.4 confirmation, OD-M2 clause-2 duty) and NOT ACTIVATED (OD-M2 clause 3 safety family, Tier-1
label, CF-6, CF-2, NMF-1/FU-1, P9-QS completion, explicit Owner activation authorization outstanding); (5)
Electronics preserved. Reviewer observations preserved as NON-BLOCKING observations: structural/hash-guard-backed
bounded resolution; stale `progression_loop.py` comments deferred to a future bounded comment-hygiene gate (file was
byte-frozen); inherited entry-level malformed-artifact serve-time semantics. Governance-only: ZERO
runtime/test/pack/registry/activation/schema/persistence/ODR diff. `activated_domains() ==
['electronics_electrical']`; first new-domain activation remains BLOCKED. Authoritative ONLY if/when this exact
candidate is merged and post-merge verified. Next required gate: **Mandatory Grill on this exact closure candidate**
→ independent external exact-candidate review → Owner acceptance → SHA-preserving publication → PR → pre/post-merge
verification. After this closure merges, the Mechanical lane's next gate is the TERMINAL §15/§16 evidence-package/
closure contract (separately authorized).

**Immediately prior (D-GMPR-D3-PN corrected contract — MERGED via `96559534`; implementation MERGED via `17a4aca4`;
retained as history):**
**Status (prior — D-GMPR-D3-PN: PATH-N DOMAIN-NEUTRAL SERVICE REMEDIATION CONTRACT CANDIDATE (CORRECTED;
supersedes rejected `4d6e4785`) — shared-core D-GMPR gate; governance-only; implementation NOT started;
D-GMPR-01-D-D3 NOT discharged; Mechanical NOT qualified / NOT activated; ODR UNCHANGED):** the P9-MECH-I5
**implementation** is **MERGED and post-merge verified** (merge `0dca782e5d4f32d403ad79c64ba469f07e46e600`, merge
tree `cb95fc97` == candidate tree → §12(a) question-content sufficiency evidence AUTHORITATIVE; §12(b) formally
D-GMPR-blocked; suite 2531/3/1/0). **Correction lineage:** the prior D-GMPR-D3-PN candidate `4d6e4785` was
independently **REJECTED** (enumerated only three of the FIVE existing-test flips its end-state forces — omitting
the D3-B seam-identity pin (`test_d3b_seam_honors_non_electronics_domain_identity`, mechanical→None) and the P9-E1
RED1 generic-fallback equality (`result == generic_text`), and falsely stating RED1 would keep passing); preserved
as immutable rejected evidence. This gate records the **CORRECTED contract candidate** (canonical record:
`docs/governance/DGMPR_D3_PATH_N_DOMAIN_NEUTRAL_SERVICE_CONTRACT.md`): architecture preserved exactly (one
canonical seam; unchanged signatures; domain-keyed committed artifacts; electronics + None default byte-identical;
artifact-less/unknown domains fail-safe None; verbatim-projection mechanical artifact with EXPLICIT metadata-key
shape; bounded canonical-identity domain→artifact resolution — no raw-string file paths; no wrapper; no
progression_loop/domain_rules change); reconciliation set corrected to the EXACT FIVE flips (I5 blocker pin; I5
path_n hash; P9-E1 RED2; D3-B seam-identity pin; P9-E1 RED1), each reconciled with disclosure while preserving the
anti-Electronics load-bearing truths, re-proven by a broad pin search (all nine other seam-consuming test files use
only the None/electronics default; the sole path_n hash pin is I5's); anything beyond the five = STOP. Allowed
reconciliation paths now include `tests/test_d3_core_domain_neutrality.py`. I4 terminal corpus: NO revalidation.
**Implementation NOT authorized by this contract.** D-GMPR-01-D-D3 discharged only at this lane's own closure (then
unblocking §12(b)). Mechanical NOT qualified / NOT activated; §15/§16 open; boundaries unchanged. Governance-only:
ZERO runtime/test/pack diff; `OWNER_DECISION_REGISTER.md` UNCHANGED. `activated_domains() ==
['electronics_electrical']`; first new-domain activation remains BLOCKED. Authoritative ONLY if/when this exact
candidate is merged and post-merge verified. Next required gate: **Mandatory Grill on this exact corrected
candidate** → independent external exact-candidate review → Owner acceptance → SHA-preserving publication → PR →
pre/post-merge verification.

**Immediately prior (P9-MECH-I5 contract gate — contract MERGED via `8ec39acf`; implementation MERGED via
`0dca782e`; retained as history):**
**Status (prior — P9-MECH-I5: §12 QUESTION-SUFFICIENCY EVIDENCE + D-GMPR DEPENDENCY DISPOSITION INCREMENT CONTRACT
CANDIDATE — governance-only; implementation NOT started; D-GMPR NOT absorbed; Mechanical NOT qualified / NOT
activated; ODR UNCHANGED):** the P9-MECH-I4 **implementation** is **MERGED and post-merge verified** (merge
`c7c9e413ac142a919b68868280cdddc5af8dce39`, parents `64145819` + accepted implementation candidate `3fe23a8c`, merge
tree `8f321993` == candidate tree → the TERMINAL §9 boundary corpus is AUTHORITATIVE: 20 evidence pins incl. five
score-parity-proven ties and a three-way, the corrected eight-text legacy corpus verbatim, and inventory-anchored
terminality; suite 2515/3/1/0; zero runtime change). This gate records the **P9-MECH-I5 increment CONTRACT
candidate** (canonical record: `docs/governance/P9_MECH_I5_QUESTION_SUFFICIENCY_EVIDENCE_CONTRACT.md`). Decisive
verified basis: the D-GMPR blocker is REAL (`path_n_questions.py` still returns None for non-electronics; remediation
= the OPEN D-GMPR-01-D-D3 gate, itself mandatory pre-activation), BUT the canonical pack-question path
(`get_domain_question`, runtime-consumed by `progression_loop`) is domain-generic and serves mechanical today —
**§12 splits: §12(a) pack-content sufficiency EXECUTABLE NOW; §12(b) non-specialist Path-N service D-GMPR-BLOCKED,
disposition-only**. I5 = ONE new evidence-only test file (coverage/progression/calibration/wording/provenance/
fail-safe pins; the seam pinned AS the recorded blocker; engine hashes incl. path_n_questions; five pack hashes;
determinism; mutations m1–m6) + the formal §12(b) disposition in closure governance surfaces — NO pack bytes touched
(the mechanical hash is the I4 corpus validity anchor); any evidence-forced content change = separate future gate
with corpus re-validation. After I5 closure the qualification lane reduces to the TERMINAL §15/§16 package/closure.
**The implementation is NOT authorized by this contract.** Mechanical NOT qualified / NOT activated; D-GMPR / CF-6 /
CF-2 / safety family / label / weight-residual / THERM-01 / D4 / D8 / Phase 10 / PSRR / deployment unchanged.
Governance-only: ZERO runtime/test/pack/registry/Web/CLI diff; `OWNER_DECISION_REGISTER.md` UNCHANGED.
`activated_domains() == ['electronics_electrical']`; first new-domain activation remains BLOCKED. Authoritative ONLY
if/when this exact candidate is merged and post-merge verified. Next required gate: **Mandatory Grill on this exact
candidate** → independent external exact-candidate review → Owner acceptance → SHA-preserving publication → PR →
pre/post-merge verification.

**Immediately prior (P9-MECH-I4 contract gate — contract MERGED via `64145819`; implementation MERGED via
`c7c9e413`; retained as history):**
**Status (prior — P9-MECH-I4: TERMINAL CROSS-DOMAIN BOUNDARY-EVIDENCE CORPUS (§9) INCREMENT CONTRACT CANDIDATE —
governance-only; implementation NOT started; Mechanical NOT qualified / NOT activated; ODR UNCHANGED):** the
P9-MECH-I3 **implementation** is **MERGED and post-merge verified** (merge
`b0be35bb8771aea6ed7edbebcf13b5d106227dbc`, parents `b99dd2f6` + accepted implementation candidate `32165caf`, merge
tree `551a03e1` == candidate tree → the evidence-based signal-quality dispositions are AUTHORITATIVE: `mechanism`
removed from classification; `locking` → multi-word `locking mechanism` (PR004); `force`/`bar` removed from substance;
all retentions evidence-recorded; suite 2495/3/1/0; bounded categorized differential with zero unexplained deltas;
engine byte-frozen). This gate records the **P9-MECH-I4 increment CONTRACT candidate** (canonical record:
`docs/governance/P9_MECH_I4_TERMINAL_BOUNDARY_CORPUS_CONTRACT.md`): the unique remaining UNBLOCKED qualification-lane
obligation — the TERMINAL §9 boundary corpus, now buildable because I3 froze the signal inventory (the I3 contract's
own deferral condition). Scope: ONE new deterministic focused test file, EVIDENCE ONLY, zero runtime change; corpus
validity bound to the exact I3 inventory; required classes incl. positive journeys, per-sibling hard cases, EXPLICIT
ties proven by score-parity construction, mixed-domain (classification only, no D4), NONE/unknown/ambiguity,
adversarial synonyms with honest recall labels, the corrected EIGHT-text legacy corpus verbatim, and sibling/engine/
activation invariance anchors; no parent-RED (evidence-only) — integrity via truthful-label justification rules and
mutation probes m1–m6; expected prior-freeze reconciliation = NONE (any existing-test conflict → STOP). Deferred, NOT
absorbed: §12 question sufficiency (blocked-side, open D-GMPR); §15/§16 terminal package/closure; §11 safety family +
§13 label (PRE-ACTIVATION per OD-M2); dormant-weight cross-pack residual (shared-core owner); THERM-01 future-only.
**The implementation is NOT authorized by this contract.** Mechanical NOT qualified / NOT activated; classifier
semantics and tie policy untouched; CF-6 / CF-2 / D-GMPR / D4 / D8 / Phase 10 / PSRR / deployment unchanged.
Governance-only: ZERO runtime/test/pack/registry/Web/CLI diff; `OWNER_DECISION_REGISTER.md` UNCHANGED.
`activated_domains() == ['electronics_electrical']`; first new-domain activation remains BLOCKED. Authoritative ONLY
if/when this exact candidate is merged and post-merge verified. Next required gate: **Mandatory Grill on this exact
candidate** → independent external exact-candidate review → Owner acceptance → SHA-preserving publication → PR →
pre/post-merge verification.

**Immediately prior (P9-MECH-I3 contract gate — contract MERGED via `b99dd2f6`; implementation MERGED via
`b0be35bb`; retained as history):**
**Status (prior — P9-MECH-I3: SIGNAL-QUALITY / AB-006 EVIDENCE & DISPOSITION INCREMENT CONTRACT CANDIDATE —
governance-only; implementation NOT started; Mechanical NOT qualified / NOT activated; ODR UNCHANGED):** the
P9-MECH-I2 **implementation** is **MERGED and post-merge verified** (merge
`4037a67d037287c3244129a41ba2b14dba139a0d`, parents `6881db34` + accepted implementation candidate `3d51bb1c`, merge
tree `5f2860b3` == candidate tree → the qualification-grade mechanical rule nuances are AUTHORITATIVE; suite
2477/3/1/0; runtime differential zero; accessor outputs unchanged for every pack). This gate records the **P9-MECH-I3
increment CONTRACT candidate** (canonical record:
`docs/governance/P9_MECH_I3_SIGNAL_QUALITY_AB006_DISPOSITION_CONTRACT.md`): the smallest coherent next qualification
increment = evidence-based disposition of the recorded AB-006 mechanical signal-quality flags (`mechanism`, `force`,
`bar`, `bracket`, `fastener`, `locking`) + evidence verification of the declared cross-domain context ownerships
(`valve`, `pressure`, `compression`, `actuator`), driven by a mandatory parent-RED difficult-case corpus proving REAL
defects (future-keyword assertion tests forbidden), with per-signal outcomes (retain-with-evidence / narrow / replace
/ remove / add-discriminative / reclassify / no-safe-correction) derived at implementation — nothing pre-decided.
Verified basis: `classify_domain` consumes ONLY `classification_signals[].signal` (cardinality scoring; F003/F004/
D3-D untouched and byte-hash-pinned); `substance_signals` separately consumed by `assess_response` (latent for
mechanical); dormant `weight` is cross-pack shared-schema metadata — its Mechanical §8.4 truthfulness share is
already discharged by the merged I1 annotation and its cross-pack residual belongs to a separate shared-core gate
(NOT absorbed; A-vs-B-vs-C decided: two separate responsibilities). Expected runtime differential: BOUNDED and
CATEGORIZED with ZERO unexplained deltas; hard invariants: electronics/software/medical single-domain corpora
byte-identical; NONE stays NONE; tie architecture + OD2 legacy-precedence rule untouched (contradiction → STOP —
OWNER DECISION REQUIRED); anti-win-rate rule binding (inventory equality-pinned; no keyword stuffing). Deferred, NOT
absorbed: terminal §9 boundary corpus (after I3 freezes content); §12 questions (blocked-side, open D-GMPR); §13
label + §11 safety family (PRE-ACTIVATION per OD-M2); §15/§16 package + closure; dormant-weight cross-pack residual
(shared owner). **The implementation is NOT authorized by this contract.** Mechanical NOT qualified / NOT activated;
CF-6 / CF-2 / D-GMPR / THERM-01 / CAP-12 / CAP-13 / WS-PFV-001 / D4 / D8 / Phase 10 / PSRR / deployment unchanged.
Governance-only: ZERO runtime/test/pack/registry/Web/CLI diff; `OWNER_DECISION_REGISTER.md` UNCHANGED.
`activated_domains() == ['electronics_electrical']`; first new-domain activation remains BLOCKED. Authoritative ONLY
if/when this exact candidate is merged and post-merge verified. Next required gate: **Mandatory Grill on this exact
candidate** → independent external exact-candidate review → Owner acceptance → SHA-preserving publication → PR →
pre/post-merge verification.

**Immediately prior (P9-MECH-I2 contract gate — contract MERGED via `6881db34`; implementation MERGED via
`4037a67d`; retained as history):**
**Status (prior — P9-MECH-I2: QUALIFICATION-GRADE RULE NUANCES INCREMENT CONTRACT CANDIDATE — governance-only;
implementation NOT started; Mechanical NOT qualified / NOT activated; ODR UNCHANGED):** the corrected D-THERM-01
candidate is **MERGED and post-merge verified** (merge `a52656d1ce78e67641685d86fa7a946cd92d2ff4`, parents `f7ed7448`
+ accepted corrected candidate `3c2ee0bc`, merge tree `ba3a18dc` == candidate tree → **D-THERM-01 / register section
THERM-01 AUTHORITATIVE** — future-path preservation only; the rejected `247cb6b9` remains immutable rejected
evidence). This gate records the **P9-MECH-I2 increment CONTRACT candidate** (canonical record:
`docs/governance/P9_MECH_I2_QUALIFICATION_GRADE_RULE_NUANCES_CONTRACT.md`): the smallest coherent next Mechanical
qualification increment after I1 = truthful full-shape enrichment of the three degenerate mechanical `rule_nuances`
IN PLACE — exact modifier_value strings/order/count preserved so the sole runtime read
(`get_active_rules`, mechanically verified to have **ZERO callers**; nuances are runtime-inert beyond that accessor
seam for EVERY pack incl. electronics) stays byte-identical for all four packs; electronics-parity shape with
TRUTHFUL modifier_type semantics (governed active-gap-rule markers, not a false copy of electronics' requirement-
marker semantic); descriptions grounded only in existing gap-type content + I1 declared scope (no unsupported
expertise; no thermal claim — THERM-01 untouched); provenance via the existing manifest; mandatory
no-downstream-consumer disclosure (P9-MECH-QC §6(d) "observable effect" truthfully bound to the accessor seam —
divergence disclosed; any future consumption = separate shared-core gate, NOT authorized). Expected runtime
differential ZERO; evidence = parent RED, focused GREEN pins (incl. exact-content description equality), negative
tests, mutations m1–m9, differential sweep, full suite, `git diff --check`. Deferred and NOT absorbed: §8
signal-quality/AB-006 + dormant-`weight` disposition (LATER; classifier-consumed fields); §9 boundary evidence
(LATER); §12 questions (LATER / partially blocked behind the OPEN D-GMPR coupling); §13 label + §11 safety family
(PRE-ACTIVATION only per OD-M2); §15/§16 package+closure (terminal). **The implementation is NOT authorized by this
contract.** Mechanical NOT qualified / NOT activated; CF-6 / CF-2 / D-GMPR coupling / NMF-1 / FU-1 / D4 / D8 /
Phase 10 / PSRR / deployment unchanged. Governance-only: ZERO runtime/test/pack/registry/Web/CLI diff;
`OWNER_DECISION_REGISTER.md` UNCHANGED. `activated_domains() == ['electronics_electrical']`; first new-domain
activation remains BLOCKED. Authoritative ONLY if/when this exact candidate is merged and post-merge verified. Next
required gate: **Mandatory Grill on this exact candidate** → independent external exact-candidate review → Owner
acceptance → SHA-preserving publication → PR → pre/post-merge verification.

**Immediately prior (D-THERM-01 corrected candidate — MERGED via `a52656d1`; retained as history):**
**Status (prior — D-THERM-01: FUTURE THERMAL CAPABILITY PRESERVATION CANDIDATE (CORRECTED; supersedes rejected
`247cb6b9`) — governance-only register amendment; NON-ACTIVATING; Mechanical NOT qualified / NOT activated):** the
P9-MECH-I1 **implementation** is **MERGED and post-merge verified** (merge
`f7ed74484234ae1e85f3db35ebfac7ebeb847288`, parents `89985218` + accepted implementation candidate `f595fb60`, merge
tree `1f9b9579` == candidate tree → the truthful Mechanical capability/coverage declaration incl. the OD-M2 clause-1
NOT-COVERED safety statement is AUTHORITATIVE; suite 2460/3/1/0; runtime behavior byte-unchanged; Mechanical remains
NOT QUALIFIED / NOT ACTIVATED). **Correction lineage:** the prior thermal-preservation candidate `247cb6b9` was
independently **REJECTED** (sole material defect: its `## 6.` register heading silently captured the six historical
CAP-12/CAP-13/CAP-14 section-6 feasibility-gate cross-references) and is preserved as immutable rejected evidence;
this fresh candidate from the same parent preserves the reviewed substance under the deliberately NON-NUMERIC register
designation **`THERM-01`** (globally unique; the six historical references stay byte-identical and un-re-bound). This
gate records the **Owner-directed anti-forgetting registration `D-THERM-01`** — a bounded R7 amendment (register
section `THERM-01`) to `INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md` preserving a governed FUTURE path for thermal
capability (**no new CAP entry**; CAP-01…CAP-18 unchanged): four-way distinction never conflated (advisory = CAP-13,
consumer only; thermal ANALYSIS = future producer riding P9-QS §13 deterministic-calculation lineage + §12 units
integrity; thermal SIMULATION = still §1A-excluded by default — §1A's pre-existing GENERIC revisit permission
(evidence + contract + owner authorization) is now exercisable for thermal ONLY through the explicit mandatory thermal
feasibility/contract gate; physical validation = WS-PFV-001); consumers referenced not absorbed (CAP-12, CAP-13, D4 as
eventual system-level coordinator — NOT AUTHORIZED; ADR-002 `THERMAL_MANAGEMENT` = gap-taxonomy concept only); future
MAY-include boundary recorded as feasibility subjects, not promises; binding truthfulness (no governed thermal
capability exists today; P9-MECH-I1 NOT-COVERED unchanged; registration ≠ capability/qualification/activation; no
certified-truth thermal claims; no CFD/FEA/solver implied); mandatory feasibility-gate checklist before ANY
implementation; no architecture pre-authorized. Governance-only: ZERO runtime/test/pack/registry/Web/CLI diff.
`activated_domains() == ['electronics_electrical']`; first new-domain activation remains BLOCKED. Authoritative ONLY
if/when this exact candidate is merged and post-merge verified. Next required gate: **Mandatory Grill on this exact
candidate** → independent external exact-candidate review → Owner acceptance → SHA-preserving publication → PR →
pre/post-merge verification.

**Immediately prior (P9-MECH-I1 contract gate — contract MERGED via the `89985218` merge; implementation MERGED via
`f7ed7448`; retained as history):**
**Status (prior — P9-MECH-I1: OD-M2 RESOLVED + TRUTHFUL CAPABILITY & COVERAGE DECLARATION INCREMENT CONTRACT
CANDIDATE — governance-only; implementation NOT started; Mechanical NOT qualified / NOT activated):** the P9-MECH-QC
contract is **MERGED and post-merge verified** (PR #467 → authoritative tip
`90b1b00f0bd384911735a55340ee15829a77bbad`; merge tree == candidate tree `0147109e` → **P9-MECH-QC AUTHORITATIVE**;
`mechanical` SELECTED via D-P9-MECH-01). This gate records **OD-M2 = RESOLVED** (`D-P9-MECH-02`, Owner-approved
**Option B-hardened, Mechanical-specific**: no family required for qualification PROVIDED the declarations state
safety-signal derivation NOT COVERED, every qualification record marks the absent family an ACTIVATION BLOCKER, and a
governed family through the F001 seam with full evidence lands before any Owner activation authorization for
`mechanical`; Mechanical-only; nothing else modified/closed) and the **P9-MECH-I1 increment CONTRACT** (canonical
record: `docs/governance/P9_MECH_I1_TRUTHFUL_CAPABILITY_COVERAGE_DECLARATION_CONTRACT.md`): smallest coherent first
increment = the truthful declaration foundation — Mechanical capability contract + coverage declaration as ONE
additive pack-metadata artifact (electronics-parity shape; concept-level claims only; mandatory NOT-COVERED list incl.
the OD-M2 clause-1 statement; provenance-tagged; loader-safety mechanically verified: §5-I1 validation is
required-fields-only and electronics already carries `coverage_declaration`) + focused tests (parent RED proof; GREEN
shape/truthfulness/OD-M2 pins; negative tests; mutations m1–m6; classification-corpus byte-identity differentials;
full suite; `git diff --check`). Deferred to later increments: rule nuances; signal-quality/AB-006 + dormant-`weight`
disposition; boundary tests; question sufficiency; label; safety family (pre-activation gate). **The implementation is
NOT authorized by this contract** — separate explicit Owner authorization + governed lifecycle required. Boundaries
preserved: no qualification claim; no activation; registry membership unchanged; CF-6 / CF-2 / D-GMPR coupling /
NMF-1 / FU-1 / D4 / D8 / Phase 10 / PSRR / deployment untouched. Governance-only: ZERO
runtime/test/pack/registry/Web/CLI/activation/schema/persistence diff. `activated_domains() ==
['electronics_electrical']`; first new-domain activation remains BLOCKED (for `mechanical` incl. OD-M2 clause 3).
Authoritative ONLY if/when this exact candidate is merged and post-merge verified. Next required gate: **Mandatory
Grill on this exact candidate** → independent external exact-candidate review → Owner acceptance → SHA-preserving
publication → PR → pre/post-merge verification.

**Immediately prior (P9-MECH-QC — MERGED via PR #467; retained as history):**
**Status (prior — P9-MECH-QC: MECHANICAL SELECTION + P9-QS QUALIFICATION CONTRACT CANDIDATE — governance-only;
Mechanical NOT qualified / NOT activated; registry UNCHANGED):** the D-GMPR-01-D-D4 Amendment 01 is **MERGED and
post-merge verified** (PR #466 → authoritative tip `c4abe0207c34f15e89438cc931c114db9d2e6225`; merge tree ==
candidate tree `2694a424` → **Amendment 01 AUTHORITATIVE**; D4 remains REGISTERED / NOT AUTHORIZED). This gate records
the **Mechanical P9-QS Qualification Contract candidate** (canonical record:
`docs/governance/P9_MECHANICAL_DOMAIN_QUALIFICATION_CONTRACT.md`) and, inside it, the Owner selection **`D-P9-MECH-01`**
(`mechanical` = next Phase-9 qualification target; selection ≠ qualification ≠ activation; registry unchanged;
qualification-extensibility claim only — NO registration-extensibility claim; no standalone selection gate, per the
D-CF5-F002-01/D-CF5-F004-01 recording precedent). Contract defines the exact future evidence required before
`mechanical` may be declared P9-QS QUALIFIED: truthful capability declaration via existing §5-I1 ownership; real
(non-placeholder) rule nuances; coverage declaration at electronics governance parity; signal-quality evidence (AB-006
candidate flags reused; truthful plural-matching behavior; **verified dormant `weight` metadata** truthfulness
disposition); mechanical↔electronics boundary tests with binding D4 separation; electronics non-degradation
(full-suite + byte-parity differentials); pack-question sufficiency (the `path_n_questions.py` seam stays in the OPEN
D-GMPR lane); truthful Tier-1 EN/AR label at a future authorized gate (CF-2 NOT over-closed); output truthfulness with
WS-PFV-001 routing (referenced only); exact §15 qualification-evidence package. **OPEN Owner decision OD-M2 surfaced,
NOT decided: Mechanical safety-cue-family timing (before qualification vs before activation vs other governed
treatment) — no qualification declaration until decided.** The contract does NOT qualify or activate Mechanical, does
NOT authorize its own implementation (each increment needs separate Owner authorization), and preserves CF-6 / CF-2 /
D-GMPR coupling / NMF-1 / FU-1 / D4 / D8 / Phase 10 / PSRR / deployment boundaries unchanged. Governance-only: ZERO
runtime/test/Web/CLI/domain-pack/registry/activation/schema/persistence diff. `activated_domains() ==
['electronics_electrical']`; first new-domain activation remains BLOCKED. Authoritative ONLY if/when this exact
candidate is merged and post-merge verified. Next required gate: **Mandatory Grill on this exact candidate** →
independent external exact-candidate review → Owner acceptance → SHA-preserving publication → PR → pre/post-merge
verification.

**Immediately prior (D-GMPR-01-D-D4 Amendment 01 — MERGED via PR #466; retained as history):**
**Status (prior — D-GMPR-01-D-D4 AMENDMENT 01 CANDIDATE — bounded governance-only scope-meaning clarification; NOT a
new gate; NON-ACTIVATING; NO domain activated):** the CF-5 umbrella formal closure is **MERGED and post-merge verified**
(PR #465 → authoritative tip `bb7e73264d484561c8e1b3f264d2eceefc0cf394`; merge tree == closure-candidate tree →
**`CF-5 = FORMALLY CLOSED` is AUTHORITATIVE**; carry-forwards preserved: CF-6 remainder OPEN; CF-2 OPEN;
`path_n_questions` D-GMPR coupling OPEN; NMF-1 + FU-1 re-homed as pre-activation test-hardening; P9-QS separate). This
gate records a **bounded clarification amendment to the existing canonical owner `D-GMPR-01-D-D4`** (Cross-Domain /
Multi-Disciplinary Engineering Integration): canonical substance in `docs/governance/OWNER_DECISION_REGISTER.md`
("Substance (D-GMPR-01-D-D4 — Amendment 01)" block + row pointer annotation; **same decision identity — no new decision
ID/document/workstream**), synchronized append-only in `ACTIVE_EXECUTION_ROADMAP.md` and in
`CURRENT_PROJECT_STATE.md`. Substance: D4's registered shared-constraint propagation / conflicts / unified assessment
**includes governed system-level engineering compatibility across participating domains** (mutual compatibility as ONE
product/system, not mere multi-domain presence detection); **per-domain PASS ≠ system-level PASS** (future D4 surfaces
incompatibilities, unresolved interface assumptions, contradictions, unowned/orphan requirements, and explicit Known
Unknowns rather than silently composing PASS states); Owner examples preserved **ILLUSTRATIVE ONLY / NON-BINDING**;
**no defect-free-product guarantee** (truthful Known-Unknowns route to WS-PFV-001-lineage physical/specialist
validation); five-way distinction preserved (recognition ≠ qualification ≠ activation ≠ cross-domain evaluation ≠
physical validation); future-domain extensibility without core redesign or domain-specific hardcoded composition
authority; **no implementation architecture / no pipeline committed**. **Non-effects:** D4 remains REGISTERED (future
gate) / NOT AUTHORIZED, sequencing unchanged; NO domain registration/activation (incl. `mechanical`); NO
`iot_electronics` change; NO D8 / Phase 10 / PSRR / deployment; **NOT a prerequisite expansion — adds no new blocker to
and does not delay the Phase-9 next-domain decision or Mechanical P9-QS qualification** (the next Owner gate is
unchanged: Phase-9 next-domain selection). Governance-only: ZERO
runtime/test/Web/CLI/domain/registry/activation/schema/persistence diff. Authoritative ONLY if/when this exact candidate
is merged and post-merge verified. Next required gate: **Mandatory Grill on this exact candidate** → independent
external exact-candidate review → Owner acceptance → SHA-preserving publication → PR → pre/post-merge verification.

**Immediately prior (CF-5 umbrella formal closure — MERGED via PR #465; retained as history):**
**Status (prior — CF-5 FORMAL CLOSURE CANDIDATE; governance-only; CF-6 / CF-2 / path_n_questions coupling NOT closed; NO
domain activated):** the CF5-F004 formal closure is **MERGED and post-merge verified** (PR #464 → authoritative tip
`fcc9e37ec4ef981f30d5a2009fa5244cfb3b040d`; merge tree == closure-candidate tree → **CF5-F004 = FORMALLY CLOSED; CF-3 =
DISCHARGED (F004 surface only); D-GMPR-01-D-D3 tie-break coupling = DISCHARGED**). This gate records the **CF-5 umbrella
FORMAL CLOSURE candidate** (canonical record:
`docs/governance/CF5_RETROSPECTIVE_ADVERSARIAL_ARCHITECTURE_AUDIT_FORMAL_CLOSURE_RECORD.md`): finding matrix terminal
(F001/F002/F004 FORMALLY CLOSED; F003 CLOSED; no E findings; nothing reopened); all audit §9 completion criteria verified
— including the honestly recorded limitation that the committed audit-run record is summary-level (ratified through PRs
#448–#464; per-area §10-depth artifact not separately committed; reliance flagged for the independent reviewer); fresh
verification this gate (boot OK; activation unchanged; full suite **2442 passed / 3 skipped / 1 xfailed / 0 failed**).
**Disposition: `CF-5 = FORMALLY CLOSED` — authoritative ONLY after this candidate's own merge + post-merge
verification.** Carry-forwards preserved (CF-6 remainder; CF-2; `path_n_questions` D-GMPR coupling; NMF-1 + FU-1
re-homed as pre-activation test-hardening; fenced observations retain owners; P9-QS separate; durable Owner decisions
unaffected). **No over-closure: CF-5 closure authorizes NO domain registration/activation; first new-domain activation
remains BLOCKED; D4/D8/Phase 10/PSRR/deployment unchanged.** Governance-only: ZERO
runtime/test/Web/CLI/domain/registry/activation/schema/persistence/ODR diff. Next required gate: **Mandatory Grill on
this exact closure candidate** → independent external exact-candidate review → Owner acceptance → SHA-preserving
publication → PR → pre/post-merge verification.

**Immediately prior (CF5-F004 formal closure — MERGED via PR #464; retained as history):**
**Status (prior — CF5-F004 FORMAL CLOSURE CANDIDATE; governance-only; CF-5 / CF-6 / CF-2 NOT closed; NO domain
activated):** the CF5-F004 bounded corrective implementation is **MERGED and post-merge verified** — PR #463 →
authoritative tip `80e5d78dd4e1b2128ba84fa24726fa9b89ea1a75`, a SHA-preserving two-parent merge of `0e4312e5` + the
Grill-passed, independently-reviewed (ACCEPT), Owner-accepted exact candidate `3f5f54f890df9a53db5e3212401aeda35da49b0e`;
merge tree `25ca8a51` == candidate tree; post-merge verification re-run this gate (boot OK; full suite **2442 passed / 3
skipped / 1 xfailed / 0 failed**; focused 14/14). All contract §8 closure criteria verified → **this candidate records
CF5-F004 = FORMALLY CLOSED over the authoritative runtime, CF-3 = DISCHARGED/RESOLVED, and the D-GMPR-01-D-D3 hard-coded
tie-break coupling = DISCHARGED** (all per OD3; each conditional on this closure candidate's own merge + post-merge
verification; the `engine/path_n_questions.py` D-GMPR coupling remains OPEN). **Retrospective RED-narrative correction
(non-destructive):** the frozen focused test file measures **9 failed / 5 passed** on the clean parent (re-verified
mechanically this gate) — the earlier "8 failed / 6 passed" narrative measured the pre-M5-strengthening file; the
correction changes no implementation correctness, no candidate identity, no reimplementation need, and no ACCEPT verdict.
Architecture truth carried: registry-derived membership; bounded legacy-four compatibility layer; sole-top SINGLE;
`UNRESOLVED_NON_ACTIVATED_TIE` complete-set fail-closed kind (no activation requirement); AMBIGUOUS_TIE untouched
activated-only; MULTI_DOMAIN_NEEDS_D4 not reused; `infer_domain` unchanged fail-loud; bounded Web/CLI dispatch.
Governance-only: ZERO runtime/test/Web/CLI/domain/registry/activation/schema/persistence/ODR diff. **No over-closure:
CF-5 / CF-6 / CF-2 remain OPEN; closing F004/CF-3 authorizes NO registration or activation; first new-domain activation
remains BLOCKED; D4/D8/Phase 10/PSRR/deployment unchanged.** Next required gate: **Mandatory Grill on this exact closure
candidate** → independent external exact-candidate review → Owner acceptance → SHA-preserving publication → PR →
pre/post-merge verification.

**Immediately prior (CF5-F004 bounded corrective implementation — MERGED via PR #463; retained as history):**
**Status (prior — CF5-F004 BOUNDED CORRECTIVE IMPLEMENTATION CANDIDATE; CF5-F004 / CF-3 NOT closed; NO domain
activated):** the CF5-F004 corrective contract is **MERGED and post-merge verified** (PR #462 → authoritative tip
`0e4312e50a2d166465c4ce17819b47711d720785`; merge tree == contract-candidate tree; D-CF5-F004-01 authoritative) and its
bounded implementation was executed fresh from that parent. Changed paths: `engine/domain_rules.py` (registry-derived
zero-activated membership; bounded `_LEGACY_ZERO_ACTIVATED_PRECEDENCE` compatibility layer among the legacy four only —
OD2; arm-A truthful SINGLE(sole top scorer); arm-B NEW `UNRESOLVED_NON_ACTIVATED_TIE` kind — complete canonical set, no
winner, no activation requirement, AMBIGUOUS_TIE activated-only invariant untouched; MULTI_DOMAIN_NEEDS_D4 non-reuse
recorded), `web/app.py` (bounded `/start` fail-closed dispatch addition only), `scripts/run_cli.py` (bounded-stop tuple
addition only), NEW `tests/test_cf5_f004_priority_fallback_extensibility.py` (14 tests; in-process registry doubles;
vocabulary-clean packs). `infer_domain` unchanged-and-pinned. Evidence: RED R1/R2/R7/R8 on the clean parent (incl. the
real NONE→electronics-admission chain) with pins R3–R6 green both sides; GREEN 14/14 incl. determinism probe and the
strengthened vocabulary-clean Web dispatch test (M5 initially survived via "gear" strong-vocab masking — caught in-gate,
test corrected, disclosed); mutations M1–M7 7/7 CAUGHT, bytes restored; differentials D1 = ZERO deltas (real registry,
classification + /start + guidance flavor) and D2 = 3 arm-A + 4 arm-B categorized corrections / 0 unexplained; full suite
**2442 passed / 3 skipped / 1 xfailed / 0 failed** (baseline 2428/3/1 + 14). ZERO ODR diff. **IMPLEMENTATION CANDIDATE
ONLY — still requires Mandatory Grill → independent external exact-candidate review → Owner acceptance → SHA-preserving
publication → PR → pre/post-merge verification; CF5-F004 / CF-3 NOT closed (OD3); first new-domain activation remains
BLOCKED (and OD1 binds earlier).**

**Immediately prior (CF5-F004 corrective contract + D-CF5-F004-01 — MERGED via PR #462; retained as history):**
**Status (prior — CF5-F004 CORRECTIVE IMPLEMENTATION CONTRACT CANDIDATE + D-CF5-F004-01; governance-only; implementation
NOT started; NO domain activated):** the CF5-F004 independent validation record is **MERGED and post-merge verified**
(PR #461 → authoritative tip `5dc5055746eaeabc5c92550b1dc10ac66860d7cc`; merge tree == candidate tree → **CF5-F004 = OPEN
C — INDEPENDENTLY VALIDATED**). This gate records the bounded corrective contract candidate
(`docs/governance/CF5_F004_PRIORITY_FALLBACK_CORRECTIVE_CONTRACT.md`) and the Owner decisions **D-CF5-F004-01**
(OD1 pre-trigger binding before any registry-set-changing pack-schema/provenance WORK; OD2 legacy 4-domain precedence
preserved + no invented winner / no silent erasure for future domains; OD3 CF-3 + D-GMPR-01-D-D3 discharge only at F004
formal closure). Architecture selected (§3): registry-derived membership + explicit bounded legacy-compatibility layer +
arm-A SINGLE(sole top scorer) + arm-B NEW fail-closed `UNRESOLVED_NON_ACTIVATED_TIE` kind (mechanical necessity proven;
AMBIGUOUS_TIE untouched) + bounded `/start`/CLI fail-closed dispatch additions; `infer_domain` unchanged-and-pinned.
Allowlist/forbidden per contract §4; evidence R1–R7 / GREEN+determinism / m1–m6 / d1 ZERO-delta + d2 categorized / full
suite per §5–§6. Governance-only: ZERO runtime/test/Web/CLI/domain/registry/activation/schema/persistence diff; ODR change
= D-CF5-F004-01 ONLY (implementation gate = ZERO ODR). **CONTRACT CANDIDATE ONLY — CF5-F004 / CF-3 NOT closed;
implementation NOT authorized; first new-domain activation remains BLOCKED (and OD1 binds earlier).** Next required gate:
**Mandatory Grill on this exact contract candidate**; then independent external exact-candidate review → Owner acceptance
→ SHA-preserving publication → PR → pre/post-merge verification; after authoritative, the bounded CF5-F004 implementation
gate.

**Immediately prior (CF5-F004 independent validation — MERGED via PR #461; retained as history):**
**Status (prior — CF5-F004 INDEPENDENT VALIDATION RECORD CANDIDATE; governance-only; validation only, no remediation; NO
domain activated):** the CF5-F001 formal closure is **MERGED and post-merge verified** (PR #460 → authoritative tip
`e39f667a934f0702301ab71d5b17a6b1121a4ecf`; merge tree == closure-candidate tree → **CF5-F001 = FORMALLY CLOSED**). This
gate records the completed CF5-F004 independent validation (genuinely separate session; verdict **ACCEPT WITH NON-BLOCKING
OBSERVATIONS**, blocking NONE) in a governance-only candidate. Canonical record:
`docs/governance/CF5_F004_PRIORITY_FALLBACK_INDEPENDENT_VALIDATION_RECORD.md`. **CF5-F004 = OPEN C — INDEPENDENTLY
VALIDATED**: the un-owned, registry-unsynchronized non-activated priority fallback literal
(`engine/domain_rules.py::classify_domain` Case 0); failure arms = omitted-pack sole-top → silent NONE, and omitted-pack
tie → silent legacy-member award; dangerous chain = omitted pack → NONE → sole-electronics `/start` consent → possible
electronics-labeled session; not reachable today (registry set == literal set). Trigger = first successful
recognized-registry-set change (registration IS trigger; activation NOT trigger/too late; empty activation NOT trigger).
F004 and CF-3 distinct; both discharge only at F004 formal closure. Closed D3-D/P9-E2/CF5-F003/CF5-F002 behavior not
reopened; canonical owners unchanged; 4-domain outputs + determinism + `infer_domain` contract locked; architecture OPEN;
remediation trigger-bound; corrective contract required only after this record is authoritative; Owner questions (schema-
work binding; precedence preserve-vs-replace; CF-3 discharge timing) preserved OPEN. Governance-only: ZERO
runtime/test/Web/CLI/domain/Registry/activation/schema/persistence/ODR diff. First new-domain activation remains BLOCKED;
the F004 pre-trigger obligation additionally binds before any first registry-set change. Next required gate: **Mandatory
Grill on this exact validation-record candidate**; then independent external exact-candidate review → Owner acceptance →
SHA-preserving publication → PR → pre/post-merge verification; after authoritative, the bounded CF5-F004 corrective
contract gate.

**Immediately prior (CF5-F001 formal closure — MERGED via PR #460; retained as history):**
**Status (prior — CF5-F001 FORMAL CLOSURE CANDIDATE; governance-only; F004 / CF-5 / CF-6 / CF-2 / CF-3 NOT closed; NO
domain activated):** the CF5-F001 bounded corrective implementation is **MERGED and post-merge verified** — PR #459 →
authoritative tip `9af877c405fcb637ff9b040573be0e26c87e46bf`, a SHA-preserving two-parent merge of `b06ae404` + the
Grill-passed, independently-reviewed (ACCEPT — incl. the disclosed §4 `domain_signal`-only narrowing and the D3-A pin
reconciliation), Owner-accepted exact candidate `d5edd1a39a26e3041eb417012951e2c7dab116d0`; merge tree `e98034ee` ==
candidate tree; post-merge full suite 2428 passed / 3 skipped / 1 xfailed / 0 failed; boot OK. All contract §9 closure
criteria verified mechanically (see the roadmap CLOSURE entry) → **this candidate records CF5-F001 = FORMALLY CLOSED over
the authoritative runtime** (authoritative if/when this closure candidate is merged and post-merge verified). NB-R1
eliminated with the accepted narrowing (P4 non-resume preserved); NB-R2/R3/R4 dispositioned; the D-GMPR-01-D-D3
`safety_signal` coupling DISCHARGED (its other couplings remain governed by their own records); observations memorialized
without new obligations; FU-1 unchanged (CF-5 lane). Governance-only: ZERO runtime / test / Web / CLI / domain /
activation / schema / persistence / ODR diff. No push / PR / merge / activation / D4 / D8 / F004 / CF-5 / CF-6 / CF-2 /
CF-3 closure is authorized by this candidate. Next required gate: **Mandatory Grill on this exact closure candidate** →
independent external exact-candidate review → Owner acceptance → SHA-preserving publication → PR → pre/post-merge
verification.

**Immediately prior (CF5-F001 bounded corrective implementation — MERGED via PR #459; retained as history):**
**Status (prior — CF5-F001 BOUNDED CORRECTIVE IMPLEMENTATION CANDIDATE; CF5-F001 NOT closed; NO domain activated):** the
CF5-F001 corrective contract is **MERGED and post-merge verified** (PR #458 → authoritative tip
`b06ae40460dce987024fd224610554fdbbcaabc3`; merge tree == contract-candidate tree) and its bounded implementation was
executed fresh from that parent. Changed paths: `engine/safety_signal.py` (governed domain-keyed cue/context-family seam —
PARAMETERIZE; electronics family byte-preserved sole entry; domain-identity keying = NB-R4; additive
`has_governed_safety_cue_family`), `engine/deliverable_assembler.py` (bounded `_s15` truthful capability-scope statement,
electronics output byte-unchanged), `web/app.py` (bounded `_cold_load_entry` NB-R1 restoration from persisted
`confirmed_domain`), NEW `tests/test_cf5_f001_safety_signal_domain_seam.py` (13 tests), one load-bearing-proved D3-A pin
reconciliation. **Disclosed §4 narrowing (mechanically forced; reviewer attention):** identity restored on `domain_signal`
ONLY — `state.domain` is the committed P4-1b-2a non-resume guard anchor and restoring it re-enabled resume-answering
(caught by the governed restart-durability test); the narrowing is a strict subset, pinned in both directions.
`deliverable.html` untouched (existing surface sufficed). Evidence: RED r1–r4 on the clean parent (4 + 3 dependent fail;
5 pins pass); GREEN 13/13; mutations 7/7 CAUGHT (m1–m6 + m5b), bytes restored; differentials d1 = ZERO live-electronics
deltas, d2 = only NB-R1 corrections (resume blocked in both trees), d3 = 45/45 family-seam corrections, 0 unexplained;
full suite **2428 passed / 3 skipped / 1 xfailed / 0 failed** (baseline 2415/3/1 + 13). No dependency / pack / classifier /
activation / schema / Path-N / CAP-13 / D4 / D8 / ODR diff; WS2/Increment-6 frozen surfaces preserved. **IMPLEMENTATION
CANDIDATE ONLY — still requires Mandatory Grill → independent external exact-candidate review → Owner acceptance →
SHA-preserving publication → PR → pre/post-merge verification; CF5-F001 NOT closed; first new-domain activation remains
BLOCKED.**

**Immediately prior (CF5-F001 corrective contract — MERGED via PR #458; retained as history):**
**Status (prior — CF5-F001 CORRECTIVE IMPLEMENTATION CONTRACT CANDIDATE; governance-only; implementation NOT started; NO
domain activated):** the CF5-F001 independent validation record is **MERGED and post-merge verified** (PR #457 → authoritative
tip `17ff20cd18267b71ed2ce615ae144d4e94729ab3`, SHA-preserving merge of accepted candidate `23eb12b5`; merge tree ==
candidate tree). This gate records the bounded **corrective implementation contract candidate**
(`docs/governance/CF5_F001_SAFETY_SIGNAL_CORRECTIVE_CONTRACT.md`): direction **PARAMETERIZE** (evidence-settled via the
merged D3-B pattern; electronics cue vocabulary byte-preserved as the sole family; seam keys on domain identity — NB-R4
disposition; no new Owner decision — the §8 policy question is settled by committed truthfulness authority, wording =
implementation detail; the family-before-activation question is an explicitly-preserved open P9-QS input); **NB-R1
dispositioned mechanically** (cold-load seam `web/app.py::_cold_load_entry` restores `domain`/`domain_signal` from the
already-persisted creation-validated `confirmed_domain`; legacy/NULL envelopes fail-safe unchanged; no schema/migration);
allowlist = `engine/safety_signal.py` + bounded `_cold_load_entry` + bounded `_s15` scope statement + focused tests
(+ template only if mechanically required); forbidden = second framework, pack schema/data, classifier/activation,
store schema, Path-N, CAP-13, D4/D8, ODR, de-electronicsifying cues. Evidence: GREEN A–F incl. electronics live
differential parity (d1 = ZERO deltas) and NB-R1 elimination; RED r1–r4 (STOP if irreproducible); mutations m1–m6 CAUGHT;
differentials d1–d3 with 0 unexplained; full suite green. Governance-only: ZERO runtime/test/Web/CLI/domain/activation/
schema/persistence/ODR diff this gate. **CONTRACT CANDIDATE ONLY — CF5-F001 NOT closed; implementation NOT authorized;
first new-domain activation remains BLOCKED.** Next required gate: **Mandatory Grill on this exact contract candidate**;
then independent external exact-candidate review → Owner acceptance → SHA-preserving publication → PR → pre/post-merge
verification; after authoritative, the bounded CF5-F001 implementation gate.

**Immediately prior (CF5-F001 independent validation — MERGED via PR #457; retained as history):**
**Status (prior — CF5-F001 INDEPENDENT VALIDATION RECORD CANDIDATE; governance-only; validation only, no remediation; NO
domain activated):** the completed CF5-F001 independent validation (genuinely separate session; verdict **ACCEPT WITH
NON-BLOCKING OBSERVATIONS**, NB-R1…NB-R4, blocking NONE) is recorded by a governance-only candidate on authoritative base
`2daf5c70d8fd86a3b63001fce675eeac252495ed` (PR #456 merge; 0 newer). Canonical record:
`docs/governance/CF5_F001_SAFETY_SIGNAL_INDEPENDENT_VALIDATION_RECORD.md`. **CF5-F001 = OPEN C — INDEPENDENTLY VALIDATED**:
residual shared-core electronics coupling in `engine/safety_signal.py` (`_MVP_DOMAIN`; electronics-gated
`_has_electrical_context`; shared-core electronics context/cue families; no per-domain seam; the `:272` missing-domain
fallback as a contract-time examination item); the corrected D3-A history is NOT reopened. No presently reachable
non-electronics manifestation (multi-domain defect latent Class C); **NB-R1** (presently reachable electronics-only
live-vs-cold-load detection divergence via the `:272` fallback) preserved as a MANDATORY corrective-contract disposition
item, not overturning Class C. Binding trigger (precision-corrected): before the first point a non-electronics-domain
session can be produced by a production surface and reach the safety-signal derivation — current enabler = activation-set
broadening; equivalent future enablers per NB-R2; registration alone and empty activation are NOT triggers (the trigger is
deliberately NOT `activated_domains() != ['electronics_electrical']`). Architecture selection OPEN (PARAMETERIZE = leading
candidate only; frozen in the later corrective-contract gate); backward compatibility = behavioral/differential electronics
parity + the WS2/Increment-6 frozen surfaces; NB-R3/NB-R4 preserved; CF-2 / CF-3(F004) / CF-6 / CAP-13 / Path-N / Domain
Packs / WS2 / anti-duplication fenced; FU-1 outside F001 (registered once, CF-5 lane); Owner re-disposition only via an
explicit governed, recorded Owner decision that cannot silently waive the pre-trigger blocker or CF-5 completion.
Governance-only: ZERO runtime / test / Web / CLI / domain / activation / schema / persistence / ODR diff. **Remediation NOT
required now; the bounded pre-trigger corrective prerequisite remains; first new-domain activation remains BLOCKED.** No
push / PR / merge / corrective contract / remediation / activation / D4 / D8 is authorized by this candidate. Next required
gate: **Mandatory Grill on this exact validation-record candidate**; after authoritative, the bounded CF5-F001 corrective
contract is the subsequent separately governed gate.

**Immediately prior (CF5-F002 formal closure — MERGED via PR #456; retained as history):**
**Status (prior — CF5-F002 FORMAL CLOSURE CANDIDATE; governance-only; CF-6 facets (i)–(iv) discharged; CF-6 / CF-2 / CF-5 NOT
closed; NO domain activated):** the CF5-F002/CF-6 bounded corrective implementation is **MERGED and post-merge verified** —
PR #455 → authoritative tip `9683f64b8467705f3bb1715c4b86b7a14a96f397`, a SHA-preserving two-parent merge of `2861f548` + the
Grill-passed, independently-reviewed (ACCEPT WITH NON-BLOCKING OBSERVATIONS), Owner-accepted exact candidate
`34103a2600200d0cc671510bd494739a107f929d`; merge tree `88aaba3a` == candidate tree; post-merge full suite 2415 passed / 3
skipped / 1 xfailed / 0 failed; boot OK; `activated_domains() == ['electronics_electrical']`. All contract §11 closure criteria
verified mechanically (see the roadmap CLOSURE entry) → **this candidate records CF5-F002 = FORMALLY CLOSED over the
authoritative runtime** (authoritative if/when this closure candidate is merged and post-merge verified). CF-6 facets (i)–(iv)
discharged; remaining CF-6 (general Web/CLI pre-classifier consistency beyond `/start`; legacy fixed-domain ILT-002 routes) and
CF-2 (all non-`/start`-flow public copy; localization of the generalized copy) remain OPEN and separately gated. Follow-ups
registered once: FU-1 empty-activation-branch defensive test (CF-5 lane); FU-2 human-quality/localized non-electronics labels
(CF-2/Arabic lane). Governance-only: ZERO runtime / test / Web / CLI / domain / activation / schema / persistence / ODR diff.
No push / PR / merge / activation / D4 / D8 / CF-6 / CF-2 / CF-5 closure is authorized by this candidate. Next required gate:
**Mandatory Grill on this exact closure candidate** → independent external exact-candidate review → Owner acceptance →
SHA-preserving publication → PR → pre/post-merge verification.

**Immediately prior (CF5-F002/CF-6 bounded corrective implementation — MERGED via PR #455; retained as history):**
**Status (prior — CF5-F002 / CF-6 BOUNDED CORRECTIVE IMPLEMENTATION CANDIDATE (amended contract §14); NO domain activated;
F002 / CF-6 / CF-2 / CF-5 NOT closed):** the bounded CF5-F002/CF-6 **implementation** was executed fresh from the authoritative
parent `2861f5488aac438648af5f2a06d113d0b1720858` (PR #454 made Amendment 01 authoritative; 0 newer) against the amended §14.1
allowlist and the §4 A–G + §14.2 U1–U5 acceptance matrix. Changed paths: `web/app.py` (activation-set-derived `/start` admission:
D1 confirm-classifier-selected-activated-domain with a bounded two-step presentation seam; D2 explicit choice among ONLY activated
domains on NONE + ≥2 activated; D3 no Electronics special case / no 500; activation-aware strong-unsupported vocabulary; truthful
activation-derived copy; §7 stale-comment hygiene), `web/templates/index.html` (generalized consent control + bounded D2 chooser;
NO separate `domain_choice.html` — minimum-path), NEW `tests/test_cf5_f002_web_admission_multidomain.py` (34 tests), and
mechanically-justified fail-closed-assertion adjustments to three existing Web-admission tie tests (message-identity → the
activation-derived truthful refusal seam; load-bearing fail-closed/no-session assertions unchanged). Evidence: RED r1–r6 fail on
the parent for the validated defect reasons (incl. the Electronics-absent 500) while all 17 electronics-only backward-compat pins
pass on the parent; GREEN 34/34; mutation probes m1–m12 (+ supplementary m11b) 13/13 CAUGHT, bytes sha256-restored; differential
sweep parent-vs-implementation 396 cases, all deltas categorized (100 unchanged incl. ALL 66 electronics-only cases; 31
activated-second-domain correction; 42 strong-unsupported activation-awareness; 215 messaging truthfulness; 8 Electronics-absent
graceful), 0 unexplained; full governed suite 2415 passed / 3 skipped / 1 xfailed / 0 failed; no dependency / engine / CLI /
domain / Registry / activation / schema / persistence / API / guardrail / ODR diff. CF-6 facets (i)–(iv) implemented at candidate
level; CF-6 / CF-2 NOT closed; residuals recorded in the roadmap entry. **IMPLEMENTATION CANDIDATE ONLY — still requires Mandatory
Grill on this exact candidate → independent external exact-candidate review → Owner exact-candidate acceptance → SHA-preserving
publication → PR → pre/post-merge verification.** `activated_domains() == ['electronics_electrical']`; NO domain activated; first
new-domain activation remains BLOCKED; no push / PR / merge / activation / D4 / D8 / ODR change / closure is authorized by this
candidate.

**Immediately prior (CF5-F002/CF-6 Amendment 01 — AUTHORITATIVE via PR #454; retained as history):**
**Status (prior — CF5-F002 / CF-6 CORRECTIVE CONTRACT AMENDMENT 01 (scope re-scope) CANDIDATE; governance-only; implementation NOT
started; NO domain activated):** **`CF5-F002` / `CF-6` corrective contract is AMENDED (Amendment 01, §14)** on authoritative base
`0124ac336c654caaa6f89b44e3d55a947e6bb2c6` (PR #453 made the corrective contract authoritative; 0 newer). The prior implementation
gate correctly **STOPPED (§2)**: the `web/app.py`-only allowlist cannot implement a user-complete D1/D2 flow — `web/templates/
index.html:26` hardcodes `domain_confirm value="electronics_electrical"` (the sole consent control) and no D2 chooser exists.
Amendment 01 widens the production allowlist to the **minimum mechanically required** — `web/app.py` (incl. a bounded two-step
`/start` presentation seam if needed) + `web/templates/index.html` (dynamic consent control) + one bounded D2 domain-choice template
ONLY IF evidence requires + focused tests — and extends the acceptance matrix with **real rendered-UI GREEN** (U1 present
classifier-selected activated domain for confirmation; U2 NONE + ≥2 activated → present only activated domains for explicit
choice+confirm; U3 ratified NONE + exactly-one activated → explicit confirmation; U4 rendered backward-compat; U5 UI-language
independence) + mutation probes m11/m12. **D1/D2 and the ratified single-domain NONE case are PRESERVED EXACTLY** (policy unchanged;
only implementation scope + acceptance evidence widened). `OWNER_DECISION_REGISTER.md` UNCHANGED (D-CF5-F002-01 already authoritative;
no new Owner decision). Still forbidden: classifier/activation-policy/set change, domain activation, Domain-Pack change, D4, D8, broad
engine/CLI/unrelated-UI-framework work, schema/persistence change, implementation-gate ODR change. **AMENDMENT CANDIDATE ONLY —
CF5-F002 / CF-6 / CF-2 / CF-5 NOT closed; no domain activated; `activated_domains() == ['electronics_electrical']`; first new-domain
activation remains BLOCKED.** ZERO runtime/test/Web/CLI/domain/activation/ODR diff this gate. Next required gate: **Mandatory Grill of
this amendment candidate**; then, once authoritative, the CF5-F002/CF-6 implementation re-runs against the amended §14.1 allowlist +
§4/§14.2 matrix.

**Immediately prior (CF5-F002/CF-6 corrective implementation contract + D1/D2 — AUTHORITATIVE via PR #453; retained as history;
implementation gate STOPPED at §2, prompting Amendment 01 above):**
**Status (prior — CF5-F002 / CF-6 CORRECTIVE IMPLEMENTATION CONTRACT CANDIDATE + Owner decisions D1/D2 recorded; governance-only;
implementation NOT started; NO domain activated):** **`CF5-F002` / `CF-6` — Web `/start` multi-domain admission is DEFINED by a
bounded governance-only CORRECTIVE IMPLEMENTATION CONTRACT CANDIDATE** (record:
`docs/governance/CF5_F002_CF6_WEB_ADMISSION_CORRECTIVE_CONTRACT.md`) on authoritative base
`8d8dc1541568b7debedb51e094b15004964c333f` (PR #452 — CF5-F002 validation merge; 0 newer). CF5-F002 is VALIDATED **C** (present
defect NONE; exact trigger `activated_domains() != ['electronics_electrical']`). This gate **records Owner decisions D1/D2** in
`OWNER_DECISION_REGISTER.md` as **D-CF5-F002-01** — **D1** consent = "confirm classifier-selected activated domain" (no auto-admit;
persist classified+confirmed); **D2** `NONE` under >1 activated domain = "require explicit user choice" among activated domains (no
silent fallback), with `['electronics_electrical']` backward-compat preserved; **D3** Electronics-absent derives from the activation
set (no special case, no 500) — bounded consent/admission policy only (no multi-domain orchestration / activation / D4 / D8). The
contract fences the later implementation to `web/app.py` (`/start` admission) + a focused test, defines the full RED→GREEN matrix
(A electronics-only backward-compat; B elec+one-additional; C non-electronics-only; D 3+; E truthful messaging; F session-domain
integrity; G UI-language independence), the CF-6 shared-surface facets (strong-unsupported activation-awareness, no hidden
electronics admission, no AMBIGUOUS_TIE bypass — CF-6 NOT auto-closed), the co-triggered CF-2 messaging facet (CF-2 NOT closed),
bounded stale-comment hygiene (`SUBSTRINGS` + SINGLE/NONE-only), 10 mutation probes, and a 0-unexplained-delta differential sweep.
**Forbidden:** classifier semantic change, activation-set change, domain activation, Domain-Pack change, D4, D8, broad engine/CLI/UI
work. **CORRECTIVE CONTRACT CANDIDATE ONLY — CF5-F002 / CF-6 / CF-2 / CF-5 NOT closed; no domain activated;
`activated_domains() == ['electronics_electrical']`.** ZERO runtime/test/Web/CLI/domain/activation diff this gate (the only
production-relevant record is the D1/D2 ODR entry). Next required gate: **Mandatory Grill of this exact contract candidate**; then,
once authoritative, the bounded CF5-F002/CF-6 implementation.

**Immediately prior (CF5-F002 independent validation — AUTHORITATIVE via PR #452; retained as history):**
**Status (prior — CF5-F002 INDEPENDENT VALIDATION CANDIDATE; governance-only; VALIDATION ONLY — NO remediation authorized;
NO domain activated):** **`CF5-F002` — Web `/start` Electronics-Only Admission is INDEPENDENTLY VALIDATED by a governance-only
VALIDATION CANDIDATE** (record: `docs/governance/CF5_F002_WEB_START_ADMISSION_INDEPENDENT_VALIDATION_RECORD.md`) on
authoritative parent `e5f7d42c5a2c7ff6590816a87cd9f5ca3f650da0` (PR #451 made CF5-F003 formal closure AUTHORITATIVE; 0 newer),
per audit-contract §7 (validation separated from remediation). **Validated defect:** the `/start` admission surface hardcodes a
single-activated-domain (electronics-only) admission architecture — consent + admitted domain are the constant
`DOMAIN_CONFIRM_VALUE` (`web/app.py:837`, `:1420`); hardcoded `domain != "electronics_electrical"` branch + static
`CONFLICTING_SUPPORTED_DOMAINS` (`:1391`, `:845`); static strong-unsupported vocabulary encoding registered domains' signals as
permanently unsupported (`:897-919`; CF-6/NB-4); "electronics and electrical ideas only" public copy (CF-2). **Classification
C RETAINED ON EVIDENCE** (real production `/start` probes, isolated DB + self-restoring activation doubles, session cleanup
PASS): today every probed outcome is correct and truthful (activated-electronics admission; NONE fallback under explicit
confirmation; recognized-but-not-activated refused; real AMBIGUOUS_TIE production-unreachable; UI-language independent);
under an elec+mech double the surface fails four ways — activation state has zero effect on outcomes; activated-domain signals
refused as "unsupported"; **`a hinge that you plug in` → SINGLE(mechanical) [ACTIVATED] yet ADMITTED as an
`electronics_electrical` session (cross-domain mislabeling)**; no consent path for any second domain. **Trigger (narrowed):**
first moment `activated_domains() != ['electronics_electrical']` (extensionally = second-specialist-domain activation today);
NOT registration, NOT recognition. **CF-6:** partly owned; single "CF5-F002 / CF-6 Web-admission lane" validated; no duplicate
framework. **CF-2:** separate, co-triggered; no message defect reachable today. **Stale `SUBSTRINGS` comment
(`web/app.py:870-884`):** partly stale, comment-only, zero runtime consequence, owner F002/CF-6 lane CONFIRMED, NOT edited.
**Remediation required NOW: NO; pre-trigger corrective gate: YES (binding C obligation before any activation gate changes the
activation set); Owner multi-domain consent/admission UX policy required at that future gate, NONE now.**
**CF5-F003 remains CLOSED; CF5-F001 / CF5-F004 remain OPEN C; CF-5 remains OPEN; first new-domain activation remains
BLOCKED.** `OWNER_DECISION_REGISTER.md` UNCHANGED; ZERO runtime/test/domain/schema/web/CLI/guardrail diff;
`activated_domains() == ['electronics_electrical']`. **VALIDATION CANDIDATE ONLY — remediation NOT authorized; corrective
contract NOT created.** Next required gate: **Mandatory Grill on this exact validation candidate.**

**Immediately prior (CF5-F003 formal closure — retained as history):**
**Status (prior — CF5-F003 FORMALLY CLOSED; governance-only closure sync; NO domain activated):** **`CF5-F003` — Classifier
Matching Semantics is FORMALLY CLOSED.** The VALIDATED **D** defect (raw-substring classifier false positives) is corrected in the
AUTHORITATIVE runtime: `engine/domain_rules.py::classify_domain` performs deterministic whole-token matching (`[a-z0-9]+`; exact /
bounded `+s` / `+es`), contiguous multi-word phrase matching (bounded plural on the final token only), and at-most-once /
set-membership same-domain registered containment preservation fired on any authorized container base form (plural-container aware),
with no cross-domain leakage and no non-registered-word credit. **Authoritative implementation merge PR #450 → tip
`0563843445c55ab1d3b5dcf2bd1e995d131b419f`** (two-parent create-a-merge-commit of `107d2eb` + exact Grill-passed implementation
candidate `6cd1fbbf532a57c4b7fa40ea7732d85ea3469273`; **merge/authoritative tree `5d3f0a40bf422f570848e050e1664a4d8616b14e` ==
implementation-candidate tree** — post-merge content byte-identical to the accepted candidate; 0 newer). Evidence of record: 8 RED
(false positives + real Web `/start` + real CLI) RED-before/GREEN-after; GREEN preservation (singular+plural, multi-word/punctuation,
containment singular + plural-container, cross-domain non-leakage, at-most-once parity, genuinely executed 0/1/2/3+ activation + Web
session cleanup, Web/CLI parity); **full regression `2381 passed / 3 skipped / 1 xfailed / 0 failed`**; 8 mutation probes all caught
(bytecode-isolated, bytes restored); adversarial differential sweep 281 inputs / 20 categorized deltas / **0 unexplained**; Mandatory
Grill PASS; Independent External Review ACCEPT WITH NON-BLOCKING OBSERVATIONS; exact Owner acceptance; SHA-preserving publication; PR
#450; post-merge verification PASS. `activated_domains() == ['electronics_electrical']` (no activation change); P9-E2 tie/fallback
semantics and `DomainClassification` unchanged. **Non-blocking carry-forward (registered once in the roadmap; NOT F003 obligations):**
(NMF-1) phrase-contiguity mutation-coverage gap — runtime is CORRECT (`delivery drug`→NONE, `machines learning`→NONE), only the
committed mutation suite lacks reorder/intermediate-pluralization negatives → bounded TEST-HARDENING follow-up; (stale `SUBSTRINGS`
comment in `web/app.py::_admit_specialist_domain`) — Web runtime intentionally zero-diff → bounded DOCUMENTATION/COMMENT-HYGIENE
follow-up in the CF5-F002 / CF-6 Web-admission lane. The pre-existing `iot_electronics` schema/load warning is UNRELATED to F003 and
keeps its existing owner. **CF5-F001 / CF5-F002 / CF5-F004 remain OPEN C; CF-5 remains OPEN (F003 closure does NOT close CF-5); first
new-domain activation remains BLOCKED.** Rejected evidence preserved immutable: `a29789a9` (impl — containment-loss tie flips),
`0f48df20` (amendment — double-count), `5ebc927d` (amendment — plural-container gap + over-broad invariant). This closure gate is
**governance-only**: ZERO runtime / test / domain / Web / CLI / `OWNER_DECISION_REGISTER.md` diff.

**Immediately prior (CF5-F003 implementation candidate — now AUTHORITATIVE via PR #450 `0563843`; retained as history):**
**Status (prior — CF5-F003 IMPLEMENTATION CANDIDATE (base contract v2 + Amendment 01); RED→GREEN; NOT merged; CF5-F003 NOT
closed; NO domain activated):** **`CF5-F003` — Classifier Matching Semantics is IMPLEMENTED by a bounded IMPLEMENTATION CANDIDATE**
on authoritative base `107d2eb08e9cdf14dade12a46693cf5dd2dd1533` (live tip; two-parent merge of `cfdc58cc` + Amendment 01 candidate
`c26f676c`; merge tree `fcc00cd5` == Amendment 01 tree; 0 newer). The bounded runtime change replaces the raw-substring scoring in
`engine/domain_rules.py::classify_domain` with deterministic **whole-token** matching over `[a-z0-9]+` tokens (exact / bounded
`+s` / `+es`), **contiguous multi-word** phrase matching (bounded plural on the final token only), and **same-domain registered
containment preservation** credited **AT-MOST-ONCE / set-membership** and fired when the container is present via **any authorized
base form (incl. its bounded plural — plural-container aware, Amendment 01 §A3/§A3a)**; **no cross-domain containment leakage**; no
credit inside a non-registered word. New module-level `_TOKEN_RE` + `_single_word_matches` / `_phrase_matches` /
`_present_signal_count`; `import re` added. **Tie policy (0→fallback / 1→SINGLE / ≥2→AMBIGUOUS_TIE), the non-activated priority
fallback list, `DomainClassification` semantics, the P9-E2-R fail-loud `infer_domain` wrapper, and D3-D precedence are UNCHANGED.**
**RED→GREEN evidence:** NEW `tests/test_cf5_f003_classifier_matching_semantics.py` (74 tests) — 8 RED (false positives
`controlled`/`compiled`/`knowledge`→`led`, `patriotic`→`iot`, `concurrent`→`current`, `hearth`→`heart`; a real Web `/start`
guidance-bypass; a real CLI incorrect-confirmation) fail on the pre-fix parent `107d2eb` and pass after the fix; GREEN preservation
(singular+plural, multi-word/punctuation, containment singular + **plural-container**, cross-domain non-leakage `biosensor`/
`biosensors`→medical, **at-most-once parity** singular+plural, genuinely-executed **0/1/2/3+** activation with Web session cleanup,
Web/CLI parity). **Full regression:** `pytest -q` = **2381 passed / 3 skipped / 1 xfailed / 0 failed** (= 2307 parent baseline + 74
new; no existing-test regression; no deleted test; no new skip/xfail). **Mutation suite (8, all CAUGHT RED, bytecode-isolated, bytes
restored):** substring-restore; `+s` removal; `+es` removal; punctuation regression; containment removal; cross-domain/non-registered
containment leak; non-idempotent double-count; exact-token-only container (plural-container M1). **Adversarial differential sweep:**
281-input corpus, 20 parent-vs-candidate deltas ALL categorized (F003 false-positive/accepted-compound-loss; cross-domain-leakage
correction; authorized phrase/tokenization expansion), **0 UNEXPLAINED**. **Scope:** `engine/domain_rules.py` (matching/scoring only)
+ the new focused test + this governance current-truth sync. **ZERO diff:** `web/app.py`, `scripts/run_cli.py`,
`engine/safety_signal.py`, `engine/domain_activation.py`, Domain Registry, Domain-Pack signal data, tie policy, fallback priority,
`ARCHITECTURE_GUARDRAILS.md`, `OWNER_DECISION_REGISTER.md`, schemas, persistence, API. `activated_domains() ==
['electronics_electrical']`; NO activation change. **IMPLEMENTATION CANDIDATE ONLY — CF5-F003 NOT closed** (closure is a later gate
after independent review → Owner acceptance → merge → post-merge verification). CF5-F001 / CF5-F002 / CF5-F004 remain UNCHANGED open
C; CF-5 remains OPEN; first new-domain activation remains BLOCKED. Next required gate: **Mandatory Grill of this exact implementation
candidate.**

**Immediately prior (CF5-F003 Amendment 01 CONTRACT candidate — now AUTHORITATIVE via PR #449, merge `107d2eb`; retained as
history):**
**Status (prior — CF5-F003 CONTRACT AMENDMENT 01 CANDIDATE; governance-only; implementation NOT started; NO domain activated):**
**`CF5-F003` Amendment 01 — Same-Domain Containment Preservation is DEFINED by a governance-only CONTRACT AMENDMENT CANDIDATE**
(record: `docs/governance/CF5_F003_CLASSIFIER_MATCHING_SEMANTICS_CORRECTIVE_CONTRACT_AMENDMENT_01.md`) on authoritative base
`cfdc58cc798d02b8d9f50030b627a8302e0de889` (PR #448 made the corrected CF5-F003 corrective contract v2 AUTHORITATIVE; 0 newer). The
CF5-F003 implementation candidate `a29789a948829133812d1a80b297e9b5b907cdc1` (whole-token + bounded plural; Creator Grill PASS WITH
NON-BLOCKING HARDENING) was **REJECTED by Independent External Review — MATERIAL CORRECTION REQUIRED**, blocking finding
**CONTAINMENT-LOSS TIE FLIPS** (`an implantable sensor`: medical → electronics because whole-token drops the `implant`⊂`implantable`
same-domain reinforcement, ties electronics, and activated precedence flips it; likewise `application`+sensor → electronics via
`app`⊂`application`). `a29789a9` is immutable rejected evidence (NOT published/merged/reused; not an ancestor of this amendment).
The blocking finding is a **contract-level** gap; this amendment corrects the CONTRACT. **Complete containment inventory (5 pairs):**
SAME-domain `implant`⊂`implantable`(med) + `app`⊂`application`(soft) [regressions → preserve], `monitoring`⊂`patient_monitoring`
[neutral]; CROSS-domain `sensor`⊂`biosensor` [improvement — biosensor now correctly medical; do NOT restore], `neural`⊂
`neural network` [neutral]; the full graph was re-enumerated mechanically (exactly 5 pairs; no new relation after plural/phrase
normalization; no chained containment; no signal in >1 container). **Amended semantics — Design A (bounded same-domain
registered-signal containment preservation, AT-MOST-ONCE, plural-container aware):** retain the base whole-token + `+s`/`+es` rule
PLUS — when a registered container signal `Y` of domain `D` is present via ANY authorized base form (`Y` matched by the base rule:
exact `Y` / `Y+"s"` / `Y+"es"` for single-word, or a multi-word `Y`'s authorized token sequence), also credit same-domain registered
single-word signals `X` with `X` substring of `Y`; nothing else, counted as a set UNION (at most once). Verified this gate: restores
`an implantable sensor` → medical and `application`+sensor → software AND their plural-container forms (`applications with a sensor` →
software; `implantables in a sensor` → medical); does NOT restore arbitrary substrings (container must be a REGISTERED signal, so
controlled/knowledge/ecosystem stay false) or cross-domain containment (`biosensor`/`biosensors` stay medical). **P9-E2 tie policy,
priority fallback, `DomainClassification` semantics, D3-D UNCHANGED; no Domain-Pack edit.** Designs A–E evaluated; A recommended
(minimal, technical, domain-neutral, N-domain). The containment credit is **AT-MOST-ONCE / set-membership** (a signal already matched
as a standalone base token is NOT credited again). **Containment-credit invariant (M2 — narrow, replaces the withdrawn global
claim):** a signal's containment contribution is set-based/at-most-once, cannot duplicate a base contribution, cannot be cross-domain,
cannot arise from a non-registered container, and cannot exceed the single boolean contribution the same signal could have supplied
via parent substring matching. **The over-broad global claim "a domain's Design-A score never exceeds parent on any input" is FALSE
and WITHDRAWN** — authorized phrase/tokenization recognition (e.g. `clinical_trial` in `clinical trial`, `drug delivery` in
`drug-delivery`) legitimately produces new matches, so the COMPLETE classifier score may exceed parent; only the containment
contribution is bounded. **Two earlier drafts REJECTED:** `0f48df20` (unqualified score increment → A3-OVER-CREDIT / CONTAINMENT
DOUBLE-COUNT) and `5ebc927d` (EXACT-token-only container trigger → **M1 plural-container containment loss** `applications with a
sensor` → electronics; and **M2 over-broad global invariant**), both immutable rejected evidence, neither an ancestor. This candidate
triggers containment on any authorized container base form (incl. bounded plural) and states only the narrow invariant. The
underscore-signal reviewer observation (`clinical_trial`/`patient_monitoring` "unmatchable") was mechanically **DISPROVED** (same
tokenizer applies to signal and input → matched); contract NOT modified to accommodate it. **Owner-policy: NONE required** (technical
preservation; no new routing policy) → `OWNER_DECISION_REGISTER.md` UNCHANGED. Strengthened evidence required of the future
implementation: singular- AND plural-container GREEN cases + at-most-once parity cases (singular and plural: `an implant that is
implantable in a sensor circuit` / `implants implantables sensors circuits` → electronics, medical 2 not 3); original REDs preserved;
genuinely executed 0/1/2/3+ activation coverage + Web session cleanup; mutation probes for same-domain-containment removal /
cross-domain over-broadening / non-registered-word containment / non-idempotent double-count / **exact-token-only container match
(plural-container loss)**. **CF5-F003 = VALIDATED D / OPEN; impl `a29789a9` REJECTED (containment tie flips); amendment drafts
`0f48df20` REJECTED (double-count) and `5ebc927d` REJECTED (plural-container gap + over-broad invariant); CF5-F001 / CF5-F002 /
CF5-F004 remain UNCHANGED open C; CF-5 remains OPEN.** ZERO runtime/test/domain/schema/web/CLI/guardrail diff; `activated_domains() ==
['electronics_electrical']`; NO domain selected; first new-domain activation remains BLOCKED. **This amendment = AMENDMENT CANDIDATE
ONLY; implementation NOT started.** This exact candidate has passed the Creator Mandatory Grill; the next required gate is
**independent external exact-candidate review**; any material finding rejects it as-is (NEW SHA/tree/bundle — no in-place amendment).

**Immediately prior (CF5-F003 corrected corrective contract — retained as history; v2 merged AUTHORITATIVE via PR #448 `cfdc58cc`;
its whole-token-only rule superseded by Amendment 01 above after the implementation `a29789a9` was independently REJECTED):**
**Status (prior — CF5-F003 CORRECTED CORRECTIVE CONTRACT CANDIDATE; governance-only; implementation NOT started; NO active
runtime increment; NO domain activated):** **`CF5-F003` — Classifier Matching Semantics corrective gate is DEFINED by a corrected
governance-only CORRECTIVE CONTRACT CANDIDATE** (record: `docs/governance/CF5_F003_CLASSIFIER_MATCHING_SEMANTICS_CORRECTIVE_CONTRACT.md`)
on authoritative base `8c38812086cfd3c17bc61ad47bba94e8b7a9de8d` (PR #447 made the CF-5 Audit contract AUTHORITATIVE; 0 newer). The
CF-5 Audit (Execution Gate 1) ran read-only and produced four material findings (CF5-F001 shared-core electronics-specific
`safety_signal`; CF5-F002 Web `/start` electronics-only admission / CF-6; CF5-F003 classifier substring false positives; CF5-F004
hardcoded non-activated priority fallback / CF-3). **CF5-F003 was independently validated D — Material current issue, reachable
now** (`signal in text` substring scoring matches short signals inside unrelated words: `controlled`→`led`, `compiled`→`led`,
`patriotic`→`iot`, `concurrent`→`current`, `hearth`→`heart`; effects: incorrect classification, untruthful CLI confirmation, Web
`/start` bypass/admission). **The first CF5-F003 corrective contract candidate `9857ba3e21a8bbd8d73bcde83cb85b7744d0f85b` was
REJECTED by Mandatory Grill (BF-1: its strict exact-whole-token / no-plural-inference rule would regress ~76 signals' plural forms
and flip `a system of gears and levers` Mechanical→Software).** This corrected candidate replaces the rejected rule with a
**bounded plural-preserving whole-token matcher**: tokenize on `[a-z0-9]+`; a single-word signal matches a token equal to the
signal or its bounded plural `+"s"`/`+"es"` (nothing else — no stemming/fuzzy/substring/`+ies`); multi-word signals match a
contiguous whole-token sequence (bounded plural on the final token only). Collision guard validated (false positives stay false —
whole-token, not substring); plural inventory reproduced (76 single-word + 5 multi-word signals; only `diagnosis` sibilant, its
irregular plural not caught today → no obligation; no cross-pack `+s`/`+es` collision). Required GREEN preservation is MANDATORY and
explicitly repairs BF-1 (`LEDs`/`sensors`/`circuits`/`resistors`/`PCBs`; `gears`/`levers`; `catheters`; `apps`/`databases`/`APIs`;
`a system of gears and levers` stays Mechanical), plus RED (real Web/CLI reproductions) and mutation probes (incl. over-broad plural
rule → RED). **It implements NOTHING** and is scoped to `engine/domain_rules.py` matching only. **Forbidden:** Web admission redesign
(F002/CF-6), safety-signal redesign (F001), fallback-priority redesign (F004), activation, D4, D8, Domain-Pack signal-data edits.
Preservation: canonical `classify_domain` sole owner (Web/CLI consumers, no duplicate matcher); `DomainClassification` semantics;
P9-E2-R fail-loud wrapper; P9-E2 tie policy; D3-D precedence; recognized-not-activated; no new MULTI producer; no activation change.
**CF5-F003 = VALIDATED D / corrective gate OPEN; prior `9857ba3e` = REJECTED (BF-1); CF5-F001 / CF5-F002 / CF5-F004 remain UNCHANGED
open C; CF-5 remains OPEN.** **`OWNER_DECISION_REGISTER.md` UNCHANGED** (bounded technical matching rule; no new Owner
product-policy decision — D3/P9-QS/P9-E1/CF-5 precedent). ZERO runtime/test/domain/schema/web/CLI/guardrail diff;
`activated_domains() == ['electronics_electrical']`; NO domain selected; first new-domain activation remains BLOCKED. **CF5-F003
corrected corrective contract = CANDIDATE ONLY; IMPLEMENTATION NOT STARTED.** The next required gate is the **Mandatory Grill on this
exact immutable corrected CF5-F003 contract candidate**; any material Grill finding rejects it as-is (NEW SHA/tree/bundle/Grill/
independent review — no amendment).

**Immediately prior (CF-5 Audit contract/entry candidate — retained as history; merged AUTHORITATIVE via PR #447 `8c38812`; CF-5
Audit subsequently executed (Gate 1) producing CF5-F001..F004; superseded as CURRENT status by the corrected CF5-F003 corrective
contract candidate above):**
**Status (prior — CF-5 AUDIT CONTRACT/ENTRY CANDIDATE; governance-only; Audit NOT executed; NO active runtime increment; NO
domain activated):** **`CF-5` — Retrospective Adversarial Architecture Audit is DEFINED by a governance-only CONTRACT / ENTRY
CANDIDATE** (record: `docs/governance/CF5_RETROSPECTIVE_ADVERSARIAL_ARCHITECTURE_AUDIT_CONTRACT.md`) on authoritative base
`54a5565bdcdfa37ff247ceb9e806bd5b2b42cb9d` (PR #446 made P9-E2 formal closure AUTHORITATIVE; 0 newer). CF-5 was registered
(P9-E2-R closure §5, re-affirmed P9-E2 closure §7) and is MANDATORY before first new-domain activation; it is **generic to
inherited architecture and requires no selected domain to enter.** The candidate defines Audit entry, minimum scope (shared-core;
Registry; activation; classifier ownership; scoring/signals; hardcoded fallback (CF-3); Web strong-unsupported (CF-6);
public-message truthfulness (CF-2); Web/CLI/core consistency; persistence; domain isolation; schema/version; extensibility; hidden
Electronics assumptions; test architecture; reachable-on-activation debt), the **preserved A/B/C/D/E finding taxonomy** (no new
taxonomy), the **independent-validation requirement for C/D/E before reopening closed architecture**, the correction-gate policy
(C → pre-trigger prerequisite; D → bounded corrective gate; E → STOP for architecture/Owner decision), and Audit completion
criteria. **It does NOT execute the Audit, produce findings, or select/qualify/activate any domain.** Separation preserved (none
discharged): P9-QS AUTHORITATIVE (per-domain qualification separate, selection-first); CF-6 PENDING PRE-SECOND-SPECIALIST-DOMAIN
ACTIVATION; CF-2 / CF-3 separate trigger-bound; D8 Owner-reserved; D4 separate. Recommended partial-order: CF-5 → domain selection
→ per-domain P9-QS → CF-6/CF-2/CF-3 → explicit Owner activation authorization. **`OWNER_DECISION_REGISTER.md` UNCHANGED** (contract
candidate records no new accepted Owner product-policy decision — D3/P9-QS/P9-E1 precedent). ZERO runtime/test/domain/Registry/
activation/web/CLI/schema/guardrail diff; `activated_domains() == ['electronics_electrical']`; NO domain selected. **CF-5 =
CONTRACT/ENTRY CANDIDATE ONLY — Audit NOT executed; execution NOT yet authorized; the candidate does not claim the Audit is ACTIVE/
COMPLETE/PASSED.** The next required gate is the **Mandatory Grill on this exact immutable CF-5 contract candidate**; any material
Grill finding rejects it as-is (NEW SHA/tree/bundle/Grill/independent review — no amendment).

**Immediately prior (P9-E2 formal-closure candidate — retained as history; merged AUTHORITATIVE via PR #446 `54a5565`; P9-E2 now
FORMALLY CLOSED / AUTHORITATIVE; superseded as CURRENT status by the CF-5 contract candidate above):**
**`P9-E2` / `P9-PREREQ-B` — Multi-Activated Domain Tie/Conflict Precedence (bounded tie-precedence runtime
gate) is FORMALLY CLOSED / SATISFIED as a governance-only CLOSURE CANDIDATE** (record:
`docs/governance/P9_E2_MULTI_ACTIVATED_DOMAIN_TIE_PRECEDENCE_FORMAL_CLOSURE_RECORD.md`). Authoritative implementation parent
`f33663710d6edf506a082b1bfa2f02e9c3fef7ac` (PR #445; parent 1 `c11482db…` + parent 2 accepted candidate `85fda813…`; merge tree
`0bffe3f7…` == candidate tree; 0 newer). **This is a governance-only closure candidate — NOT yet authoritative and P9-E2 is NOT yet
formally closed; closure becomes authoritative only after: Mandatory Grill → independent external exact-candidate review → Owner
exact-candidate acceptance → SHA-preserving publication → PR → pre-merge verification → CREATE A MERGE COMMIT → post-merge
verification.** Implementation lineage: contract PR #441 (`47fce397`; candidate `1d29a26f`); rejected candidate `3255c4ba` (Grill
FAIL — never published/accepted/merged; not an ancestor) → accepted corrected candidate `85fda813` (built from `c11482d`) → Grill
**PASS WITH NON-BLOCKING HARDENING** (blocking NONE) → independent review **ACCEPT WITH NON-BLOCKING OBSERVATIONS** (blocking NONE)
→ Owner-accepted → published → PR #445 (5 files / +546 / −17; `git diff --check` CLEAN) → post-merge verified. **Bounded
tie-precedence policy via the canonical `classify_domain` seam (CF-1 SATISFIED):** `len(activated_tied) == 0` → non-activated
priority fallback retained unchanged; `== 1` → `SINGLE`; **`>= 2` → `AMBIGUOUS_TIE(selected=None, complete canonical activated tied
set, reason=EQUAL_SCORE)`** — no arbitrary/alphabetical/registration/dict winner, no Electronics preference, no LLM; `MULTI_DOMAIN_
NEEDS_D4` NOT fabricated (D4 separate); only ACTIVATED domains (D3-D). Fresh closure evidence reproduced at `f336637`: full suite
**2307 passed / 3 skipped / 1 xfailed / 0 failed**; focused **57 passed**; **nine load-bearing mutation probes all CAUGHT RED**,
bytes restored. Canonical-owner reconciliation: `classify_domain` = canonical owner, `infer_domain` = legacy fail-loud wrapper
(later authoritative P9-E2-R architecture governs the name evolution; the old P9-E2 contract is NOT rewritten/amended). **Carry-forward
(not erased):** CF-1 SATISFIED by this gate's subject; CF-2 shared AMBIGUOUS/MULTI public message PENDING; CF-3 non-activated
priority fallback PENDING (retained for backward compatibility; before first Nth-domain registration/activation); CF-4 D4 separate;
CF-5 Retrospective Adversarial Architecture Audit PENDING (MANDATORY before first new-domain activation); CF-6 Web
pre-classifier/strong-unsupported reachability & admission interaction PENDING (PRE-SECOND-SPECIALIST-DOMAIN ACTIVATION; distinct
from CF-2). Non-blocking observations NB-1…NB-5 carried forward (not discarded). **`OWNER_DECISION_REGISTER.md` UNCHANGED. There is
NO active runtime increment.** **NO new domain activated; NO domain selected; P9-E2-R remains FORMALLY CLOSED / SATISFIED; P9-E1
remains FORMALLY CLOSED / SATISFIED; D4 = SEPARATE / UNEXECUTED; D8 = Owner-reserved; Phase 10 = NOT AUTHORIZED; PSRR = NOT
EXECUTED; deployment / production = NOT AUTHORIZED.** The next required gate is the **Mandatory Grill on this exact immutable closure
candidate**; any material Grill finding rejects it as-is (NEW SHA/tree/bundle/Grill/independent review — no amendment).

**Immediately prior (P9-E2 implementation candidate — retained as history; merged AUTHORITATIVE via PR #445 `f336637`; superseded as
CURRENT status by the P9-E2 formal-closure candidate above):**
**`P9-E2` / `P9-PREREQ-B` — Multi-Activated Domain Tie/Conflict Precedence — was IMPLEMENTED as a CORRECTED IMPLEMENTATION CANDIDATE**
built fresh from authoritative parent `c11482db7240b5ac628e77cd061f8d5de6df40ee` (live tip re-verified; 0 newer). It **supersedes the
REJECTED prior candidate `3255c4ba1ca6ae50e0c3f20d7f0d4c8ef1fa223c`** (Mandatory Grill `GRILL FAIL — MATERIAL CONTRACT CORRECTION
REQUIRED`: sound runtime, but a FALSE `/start` strong-unsupported "masked for all real ties" reachability claim, an omitted
achievable distinguishing RED-E2-10, and a misdescribed multi-activation `/start` delta); `3255c4ba` remains immutable rejected
evidence and is NOT reused/amended/rebased/built upon. **Bounded runtime change (via the canonical `classify_domain` seam, CF-1):**
`len(activated_tied) == 0` → unchanged priority fallback; `== 1` → `SINGLE`; **`>= 2` → `AMBIGUOUS_TIE(selected_domain=None,
candidates=canonical activated tied set, reason=EQUAL_SCORE)`** — no arbitrary/alphabetical/registration/dict winner, no Electronics
preference, no LLM, `MULTI_DOMAIN_NEEDS_D4` NOT manufactured (D4 separate). Only ACTIVATED domains form the set (D3-D).
**CORRECTED reachability truth:** `/start` calls `classify_domain` FIRST and fails an `AMBIGUOUS_TIE` closed to `UNSUPPORTED`
(200, no session) BEFORE the separate `_has_strong_unsupported_evidence` gate; that gate is an independent later layer over
SINGLE/NONE inputs only, so a multi-activated tie fails closed via the ambiguity branch regardless of strong-unsupported token
membership (verified: `strong("circuit and hinge") == strong("hinge and app") == False`). **RED→GREEN:** NEW
`tests/test_p9e2_multi_activated_tie_precedence.py` (20 tests) — 12 distinguishing RED on parent (E2-1..9, **E2-10 a REAL `/start`
production-path RED**: `circuit and hinge` under an elec+mech double → parent ADMITS an electronics session (302), candidate fails
closed 200 UNSUPPORTED; **E2-10b** `hinge and app` mech+sw → parent GUIDANCE, candidate UNSUPPORTED; **E2-11** `gear and catheter`
mech+med → CLI bounded stop) + 8 honest GREEN GUARDS. **9 load-bearing mutation probes all CAUGHT RED** (incl. NEW probe 9:
neutralize the real `/start` AMBIGUOUS branch → E2-10/10b RED; probe 7: detach Web AMBIGUOUS/MULTI dispatch → P9-E2-R R2/R10 RED),
bytecode-isolated, bytes restored. **Full suite 2307 passed / 3 skipped / 1 xfailed / 0 failed** (= 2287 parent + 20). **Scope:**
`engine/domain_rules.py` (tie branch + corrected docstring) + the NEW test + governance current-truth (roadmap + this file +
`CURRENT_PROJECT_STATE.md`); **`web/app.py` ZERO diff** (runtime found safe; correction is evidence/governance + stronger tests);
ZERO diff `scripts/run_cli.py`, `engine/domain_activation.py`, `ARCHITECTURE_GUARDRAILS.md`, `OWNER_DECISION_REGISTER.md`,
`domains/**`, `schemas/**`, `database/**`. **Backward-compat (truthful):** current activation is electronics-only so ≥2 activated
tie is production-unreachable → ZERO current production delta; under a FUTURE governed second-domain activation, non-intercepted
ties change OLD incidental-SINGLE/possible-single-domain-admission → NEW AMBIGUOUS_TIE/fail-closed — an INTENDED future correction,
not a regression; `/start` is NOT universally "unchanged" under future multi-activation. **Carry-forwards:** CF-2 (public-message
truthfulness) retained; CF-3 (Nth-domain priority/fallback) retained; CF-5 (Retrospective Adversarial Architecture Audit) remains a
future pre-activation obligation; **NEW CF-6 — Web pre-classifier / strong-unsupported reachability & admission interaction
(distinct from CF-2), a FUTURE PRE-SECOND-DOMAIN-ACTIVATION obligation, NOT executed here.** **`OWNER_DECISION_REGISTER.md`
UNCHANGED.** **P9-E2 = CORRECTED IMPLEMENTATION CANDIDATE ONLY — NOT closed / NOT authoritative; NO domain activated; NO domain
selected; MULTI_DOMAIN_NEEDS_D4 NOT manufactured; D4 SEPARATE / UNEXECUTED; D8 Owner-reserved; Phase 10 NOT AUTHORIZED; PSRR NOT
EXECUTED; deployment/production NOT AUTHORIZED.** The next required gate is a **NEW Mandatory Grill on this exact new candidate**;
any material Grill finding rejects it as-is (NEW SHA/tree/bundle/Grill/independent review — no amendment).

**Immediately prior (P9-E2-R closure candidate — retained as history; superseded as CURRENT status by the P9-E2 implementation
candidate above; P9-E2-R closure evidence itself unchanged):** **`P9-E2-R` — Ambiguity / Multi-Domain Result Representation (bounded representation sub-gate)
is FORMALLY CLOSED / SATISFIED as a governance-only CLOSURE CANDIDATE** (record:
`docs/governance/P9_E2_R_AMBIGUITY_MULTI_DOMAIN_RESULT_REPRESENTATION_FORMAL_CLOSURE_RECORD.md`; authoritative pre-closure parent
`b42a3e6c246b98d425460f80d91d8de12d554039`, PR #443). **This is a governance-only closure candidate — it is NOT yet authoritative
and P9-E2-R is NOT yet formally closed; closure becomes authoritative only after: Mandatory Grill → independent external
exact-candidate review → Owner exact-candidate acceptance → SHA-preserving publication → PR → pre-merge verification → CREATE A
MERGE COMMIT → post-merge verification.** Implementation lineage: contract PR #442 (`3434c235`; candidate `3cbb16b6`) +
implementation PR #443 (`b42a3e6`; candidate `813bc5aa`; merge tree `35a58482` == candidate tree; diffstat 11 files / +725 / −48;
`git diff --check` CLEAN). **P9-E2-R established the representation seam only — it DID NOT implement the P9-E2 tie policy**
(`classify_domain` constructs SINGLE/NONE only; AMBIGUOUS_TIE / MULTI_DOMAIN_NEEDS_D4 representable/consumable but classifier-
produced only via the separate later P9-E2 runtime; `sorted(activated_tied)[0]` + priority fallback unchanged; no multi-domain
analysis). Fresh closure evidence reproduced at `b42a3e6`: full suite **2287 passed / 3 skipped / 1 xfailed / 0 failed**; focused
`test_p9e2r_result_representation.py` + `test_architecture_guardrails.py` **37 passed**; **six load-bearing mutation probes all
CAUGHT RED** (wrapper fail-loud; `/start` AMBIGUOUS; `/start` MULTI; defensive activation boundary; canonical order;
migrated-monkeypatch detachment), bytes restored. Closed acceptance behavior re-verified: one classifier owner; legacy wrapper
total over SINGLE/NONE + fail-loud over richer kinds; Web/CLI dispatch by kind; `state.domain` a resolved string; defensive
activation type boundary; canonical order ≠ precedence; no new framework / duplicate owner; `activated_domains() ==
['electronics_electrical']`. Phase-9 completeness checklist: no acceptance-relevant APPLICABLE/GAP. **Carry-forward (not erased):**
CF-1 P9-E2 runtime tie policy still pending; CF-2 shared AMBIGUOUS/MULTI public message NON-BLOCKING, carried to P9-E2; CF-3
non-activated priority fallback (`engine/domain_rules.py` line 142) — no reachable defect today, MANDATORY before first Nth-domain
registration/activation; CF-4 D4 separate owner for actual composition; **CF-5 Retrospective Adversarial Architecture Audit now
REGISTERED as a future PRE-ACTIVATION obligation (A/B/C/D/E classification; material C/D/E dispositioned/independently validated
BEFORE first new-domain activation) — NOT executed here.** **`OWNER_DECISION_REGISTER.md` UNCHANGED. There is NO active runtime
increment.** **NO new domain activated; NO domain selected; P9-E2 tie precedence remains a separate later runtime gate; P9-E1
remains FORMALLY CLOSED / SATISFIED; D4 = SEPARATE / UNEXECUTED; D8 = OPEN / Owner-reserved; Phase 8 = FORMALLY CLOSED; Phase 10 =
NOT AUTHORIZED; PSRR = REGISTERED / NOT EXECUTED; deployment / production = NOT AUTHORIZED.** The next required gate is the
**Mandatory Grill on this exact immutable closure candidate**; any material Grill finding rejects this candidate as-is (NEW
SHA/tree/bundle/Grill/independent review — no amendment).

**Immediately prior (retained as history — P9-E2-R IMPLEMENTATION CANDIDATE; merged AUTHORITATIVE via PR #443 `b42a3e6`):**
**`P9-E2-R` — Ambiguity / Multi-Domain Result Representation is now IMPLEMENTED as an IMPLEMENTATION CANDIDATE** on authoritative
base `3434c2350b4c08cabcc362d175947a311070b493` (PR #442 made the corrected P9-E2-R contract AUTHORITATIVE). Minimum-sufficient
representation seam (NO tie-policy change): `engine/domain_rules.py` gains `DomainResultKind {SINGLE, NONE, AMBIGUOUS_TIE,
MULTI_DOMAIN_NEEDS_D4}`, deterministic `DomainAmbiguityReason`, `AmbiguousDomainResultError`, and an immutable frozen
`DomainClassification` with all invariants enforced at construction (registry-valid SINGLE + empty candidates; NONE empty; tie/multi
no-winner + ≥2 unique registry-recognized canonical-sorted candidates + deterministic reason; AMBIGUOUS_TIE all-activated (D3-D);
mutual exclusion; canonical order ≠ precedence). Canonical `classify_domain(...)` is the single classifier owner (today SINGLE/NONE
only — behavior-equivalent, no tie detection); legacy `infer_domain(...) -> str | None` is a thin wrapper, **total over SINGLE/NONE
and FAIL-LOUD (`AmbiguousDomainResultError`) over richer kinds**. `web/app.py` `/start` and `scripts/run_cli.py` migrated to
**dispatch by `result.kind`** (never truthiness/string comparison of the object): SINGLE byte-identical, NONE unchanged,
AMBIGUOUS_TIE + MULTI_DOMAIN_NEEDS_D4 **fail closed** via an existing safe surface (no session/no electronics admission/no winner/no
D4/no new UX/no implied multi-domain analysis); `state.domain` remains a resolved string. `engine/domain_activation._resolve_pack_id`
gains a **defensive fail-loud `TypeError`** for non-string domain ids (a `DomainClassification` can never be silently swallowed;
None/empty preserved). `ARCHITECTURE_GUARDRAILS.md` §9 reconciled (classify_domain = richer canonical entry; infer_domain
legacy/fail-loud; new admission callers must use classify_domain; one owner) with deliberate guardrail tests; the frozen `str |
None` signature test is NOT weakened. **RED→GREEN** via new `tests/test_p9e2r_result_representation.py` (19) + 4 guardrail tests
(RED-R1…R11 + invariant/immutability/mutual-exclusion/duplicate/deterministic-reason/defensive-boundary), all GREEN; activated ties
simulated with self-restoring `_ACTIVATED_DOMAINS` doubles (NO real activation). **Six load-bearing mutation probes** all caught RED
(wrapper fail-loud; `/start` AMBIGUOUS; `/start` MULTI; defensive boundary; canonical-order; **migrated-monkeypatch detachment** —
the six `web.app.infer_domain` monkeypatches were migrated to `web.app.classify_domain` and proven still load-bearing), byte-restored.
**Fresh full suite: 2287 passed / 3 skipped / 1 xfailed / 0 failed** (2264 baseline + 23 new). **Scope:** the 8 runtime/test/guardrail
paths + governance current-truth registration (roadmap + this file + `CURRENT_PROJECT_STATE.md`, per D3 implementation precedent);
**`OWNER_DECISION_REGISTER.md` UNCHANGED**; no persistence/schema/public-API/export/Domain-Pack change; no P9-E2 tie-policy change;
`activated_domains() == ['electronics_electrical']`. Phase-9 completeness checklist: no acceptance-relevant APPLICABLE/GAP. **P9-E2-R
= IMPLEMENTATION CANDIDATE ONLY — NOT closed** (formal closure, if precedent requires, is a separate gate after independent review →
Owner acceptance → merge → post-merge verification); **NO new domain activated; NO domain selected; P9-E2 tie precedence remains a
separate later runtime gate; P9-E1 remains FORMALLY CLOSED / SATISFIED; D4 = SEPARATE / UNEXECUTED; D8 = OPEN / Owner-reserved; Phase
8 = FORMALLY CLOSED; Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment / production = NOT AUTHORIZED.** The next state is:
independent review of this exact implementation candidate → Owner acceptance → merge → post-merge verification → (if precedent
requires) a separate P9-E2-R formal-closure gate.

**Immediately prior (retained as history — P9-E2-R CONTRACT CANDIDATE, corrected; merged AUTHORITATIVE via PR #442 `3434c23`):**
**`P9-E2-R` — Ambiguity / Multi-Domain Result Representation (bounded sub-gate) is DEFINED by a CORRECTED
governance-only CONTRACT CANDIDATE** (record: `docs/governance/P9_E2_R_AMBIGUITY_MULTI_DOMAIN_RESULT_REPRESENTATION_CONTRACT.md`;
authoritative base `47fce397dfd21175a0012b652f8dde6548e31432`). It is the corrected reissue that **supersedes the Grill-REJECTED
prior candidate `1b817f06e7d86b3af6e44b298bcf7a31102e5e32`** (which remains **immutable historical evidence only — NOT amended /
NOT merged / NOT reused**); a NEW independent candidate from the current authoritative parent, incorporating all MATERIAL Mandatory
Grill findings. **Contract-first only — no runtime/test change, no domain activation, no domain selection.** Corrections applied
(contract §22 ledger): legacy `infer_domain` wrapper **FAILS LOUD** (raises a dedicated bounded exception, never silent
`None`/arbitrary domain) on AMBIGUOUS_TIE/MULTI_DOMAIN_NEEDS_D4, total over SINGLE/NONE (§4) + **RED-R9**; **all six
`web.app.infer_domain` monkeypatch surfaces migrated + proven load-bearing** (§7.3); **architecture-guardrail reconciliation** of
the frozen `str | None` vs fail-loud richer kinds (§4.1); `classify_domain` richer canonical entry, one classifier owner (§3);
**web + CLI dispatch by `result.kind`** (never truthiness/string comparison of the object) (§7) + **RED-R10** (`/start × MULTI`) +
**RED-R11** (CLI bounded stop); **`state.domain` remains a resolved string** (§10); strengthened invariants (unique ids, ≥2
candidates, all-activated, mutual exclusion, duplicate rejection, immutable) (§11); **deterministic non-LLM `reason`** (§12);
**defensive fail-loud type boundary** vs silent `DomainClassification` swallowing (§19); **line-34 future Nth-domain fallthrough
hazard registered** as a mandatory pre-Nth-domain obligation (§21); future implementation **classified architecture-affecting /
higher-governance** (§22); D4 marker-only, no-analysis-implied wording (§16/§18). **Confirmed gap (verified at `47fce39`):**
`infer_domain -> str | None` conflates the truths and `web/app.py /start` admits `domain is None` as an electronics session
(lines 1393–1394); guardrail freezes the `str | None` signature; activated tie unreachable today (only electronics activated).
**Architecture (retained, minimum-sufficient):** `DomainResultKind {SINGLE, NONE, AMBIGUOUS_TIE, MULTI_DOMAIN_NEEDS_D4}` +
immutable `DomainClassification` + canonical `classify_domain(...)` + legacy fail-loud `infer_domain` wrapper; no new
framework/router/registry/activation-engine/schema. RED-R1…R11 + additional invariant/mutation/monkeypatch-load-bearing/
type-boundary tests designed (not implemented). Phase-9 completeness checklist fully dispositioned (no acceptance-relevant
APPLICABLE/GAP). **Governance-only scope:** the new contract doc + append-only roadmap entry + this current-truth sync +
`CURRENT_PROJECT_STATE.md`; **`OWNER_DECISION_REGISTER.md` UNCHANGED; ZERO runtime/test/domain/web/CLI/schema/prompt/benchmark
diff.** **P9-E2-R = CONTRACT CANDIDATE ONLY — authoritative only if this exact accepted candidate is merged and post-merge
verified; the P9-E2-R runtime + tests are a separate later architecture-affecting gate, NOT authorized here; the Grill-rejected
`1b817f06` remains immutable historical evidence only; NO new domain activated (`activated_domains() == ['electronics_electrical']`);
NO domain selected; P9-E2 tie precedence remains a separate later runtime gate; P9-E1 remains FORMALLY CLOSED / SATISFIED; D4 =
SEPARATE / UNEXECUTED; D8 = OPEN / Owner-reserved; Phase 8 = FORMALLY CLOSED; Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED;
deployment / production = NOT AUTHORIZED.** The next state is: independent review of this exact corrected contract candidate →
Owner acceptance → merge → post-merge verification → a separate P9-E2-R implementation gate.

**Immediately prior (retained as history — P9-E2 CONTRACT CANDIDATE, definition only; merged AUTHORITATIVE via PR #441
`47fce39`):** **`P9-E2` / `P9-PREREQ-B` — Multi-Activated Domain Tie/Conflict Precedence is DEFINED by a governance-only CONTRACT
CANDIDATE**
(record: `docs/governance/P9_E2_MULTI_ACTIVATED_DOMAIN_TIE_PRECEDENCE_CONTRACT.md`; authoritative base
`05184f9166fa3a9e45a3384be5bafccc86e05ebe` — PR #440 made the P9-E1 formal closure AUTHORITATIVE). This is the mandatory
D3-registered prerequisite **P9-PREREQ-B** carried by the authoritative P9-QS §16; **contract-first only — no runtime/test change,
no domain activation, no domain selection.** **Live evidence (verified at `05184f91`): still required** —
`engine/domain_rules.py::infer_domain` lines 31–33 pick `sorted(activated_tied)[0]` (incidental alphabetical precedence among
ACTIVATED tied domains; plus the line-34 `priority` literal for the no-activated-tie fallback); reachable only when ≥2 specialist
domains are activated and tie. Behaviorally proven read-only (monkeypatched `_ACTIVATED_DOMAINS`, restored; no real activation): a
clean `mechanical`+`medical_device` activated tie returns `mechanical` purely alphabetically. **Critical representation finding:**
`infer_domain` returns `str | None`, which cannot honestly express an ambiguous tie / tied candidate set / no-governed-winner /
genuine multi-domain (Case 4) — so the contract explicitly calls out a bounded, **separately-reviewed representation sub-gate
`P9-E2-R`** rather than hiding it. Precedence policy: Case 1 (single winner) unchanged; Case 3 (tie, no governed precedence) →
explicit ambiguous/unresolved outcome (safe default, no silent pick); Case 4 → surface D4 need truthfully; forbidden answers =
alphabetical/file/registration/iteration/dict order, hardcoded Electronics preference, model guess, silent default. RED-1…RED-6
designed (not implemented); Phase-9 completeness checklist fully dispositioned (no APPLICABLE/GAP). **First-new-domain implication
(verified): Electronics is already activated, so the first new-domain activation creates a >1-activated state — P9-E2 is a
MANDATORY prerequisite before the first actual new-domain activation.** **Governance-only scope:** the new contract doc +
append-only roadmap entry + this current-truth sync + `CURRENT_PROJECT_STATE.md`; **`OWNER_DECISION_REGISTER.md` UNCHANGED; ZERO
runtime/test/domain/schema/prompt/benchmark/web diff.** **P9-E2 = CONTRACT CANDIDATE ONLY — authoritative only if this exact
accepted candidate is merged and post-merge verified; the P9-E2 runtime, the P9-E2-R representation sub-gate, and their tests are
separate later gates, NOT authorized here; NO new domain activated (`activated_domains() == ['electronics_electrical']`); NO domain
selected; P9-E1 remains FORMALLY CLOSED / SATISFIED; D4 = SEPARATE / UNEXECUTED; D8 = OPEN / Owner-reserved; Phase 8 = FORMALLY
CLOSED; Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment / production = NOT AUTHORIZED.** The next state is: independent
review of this exact contract candidate → Owner acceptance → merge → post-merge verification → a separate P9-E2 (+ P9-E2-R)
implementation gate.

**Immediately prior (retained as history — P9-E1 FORMALLY CLOSED / SATISFIED / AUTHORITATIVE via PR #440 `05184f91`):** **`P9-E1` /
`P9-PREREQ-A` — Path-N Production Caller Domain Propagation is FORMALLY CLOSED / SATISFIED** as a governance-only CLOSURE CANDIDATE
(prerequisite closure only; authoritative if/when merged; dedicated record
`docs/governance/P9_E1_PATH_N_CALLER_DOMAIN_PROPAGATION_FORMAL_CLOSURE_RECORD.md`; authoritative base
`f22085066d8a0b2b1e90c04c6808f44f606316e6`, PR #439). Implementation lineage: contract PR #438 (`8fbc239`; candidate `3b485131`) +
implementation PR #439 (`f220850`; candidate `8ebc1c1a`; merge tree `14c286ba` == candidate tree; diffstat 5 files / +251 / −5;
`git diff --check` CLEAN; independent review ACCEPT WITH NON-BLOCKING OBSERVATIONS). Live-verified at `f220850`:
`support_state("mechanical") == "recognized_not_activated"`; `activated_domains() == ['electronics_electrical']`; a foreign
recognized-not-activated domain on the Path-N flow no longer receives the Electronics artifact text (`get_question`) nor the
Electronics `_STALL_REFRAME` at exhaustion (`get_display_question`); Electronics + `domain=None` behavior intact; exactly the
three production `get_path_n_question(...)` sites threaded, no hidden caller. RED→GREEN (RED parent `8fbc239`: RED-1 foreign
artifact text + RED-2 foreign stall reframe → all 6 GREEN); independently reproduced mutation matrix (site 1 alone → RED; site 2
alone → GREEN; site 3 alone → GREEN; sites 2+3 jointly → RED; all 3 → RED — **sites 2+3 jointly, not individually, load-bearing;
recorded honestly**); fresh full suite **2264 passed / 3 skipped / 1 xfailed / 0 failed** (2258 baseline + 6 new). Phase-9
completeness checklist for P9-E1: no APPLICABLE/GAP remains (truthfulness / no-shared-core-coupling / Nth-domain extensibility /
end-to-end reasoning = PASS; knowledge-quality = NOT APPLICABLE; qualification / composition / materials / calculations /
knowledge-sources = DEFERRED to their governed gates). **`OWNER_DECISION_REGISTER.md` UNCHANGED. There is NO active increment.**
**P9-E1 / P9-PREREQ-A = FORMALLY CLOSED / SATISFIED / AUTHORITATIVE (prerequisite closure only); NO new domain activated; NO
domain selected; Electronics remains the only activated specialist domain; recognition ≠ activation; P9-E2 / P9-PREREQ-B =
SEPARATE / UNSATISFIED / NOT STARTED (`sorted(activated_tied)[0]` untouched); D4 = SEPARATE / UNEXECUTED; D8 = OPEN /
Owner-reserved; Phase 8 = FORMALLY CLOSED; Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment / production = NOT
AUTHORIZED.** The recommended next major gate is **P9-E2 / P9-PREREQ-B — Multi-Activated Domain Tie/Conflict Precedence**
(separately governed; NOT started; closing P9-E1 does NOT auto-advance to it or authorize any activation).

**Immediately prior (retained as history — P9-E1 IMPLEMENTATION CANDIDATE; merged AUTHORITATIVE via PR #439 `f220850`):**
**The `P9-E1` / `P9-PREREQ-A` — Path-N Production Caller Domain Propagation is now IMPLEMENTED as an IMPLEMENTATION
CANDIDATE** on authoritative base `8fbc239c98ab89e596554a8c52c7e7b1c5b22ad5` (PR #438 made the P9-E1 contract AUTHORITATIVE). The
bounded runtime fix threads the canonical `domain` (already the first parameter of both callers) into the existing three
`get_path_n_question(...)` calls in `engine/progression_loop.py` as `domain=domain` — (1) `get_question` (path=="N") selection,
(2) `get_display_question` exhaustion `current` read, (3) `get_display_question` exhaustion `previous` read; no signature change,
**`engine/path_n_questions.py` unchanged**, no domain branching, no second router, no activation-policy/Registry/Domain-Pack/D8/
P9-E2 change. **RED→GREEN** via the new behavioral `tests/test_p9e1_path_n_caller_domain_propagation.py` (6 tests): baseline RED-1
(`get_question` foreign recognized domain served Electronics artifact text) + RED-2 (`get_display_question` foreign domain served
the Electronics `_STALL_REFRAME`) both FAILED pre-edit and are GREEN post-edit; guards preserve Electronics artifact text, the
Electronics stall reframe, the `domain=None` seam default, and assert the fixture `mechanical` is `recognized_not_activated` /
not-activated. **Per-site proof (honest):** site-1 mutation is individually caught; sites 2+3 are *jointly* load-bearing (either
domain-aware reframe read alone suppresses the erroneous foreign reframe — defense-in-depth), and the joint site-2+3 mutation (the
original defect) is caught by RED-2; both threaded for a domain-consistent comparison per contract §3; no probe left in the
candidate. **Full suite fresh: 2264 passed / 3 skipped / 1 xfailed / 0 failed** (2258 baseline + 6 new). **Scope:**
`engine/progression_loop.py` + the new test + governance current-truth registration (this file + roadmap append +
`CURRENT_PROJECT_STATE.md`, per D3 implementation precedent); **`OWNER_DECISION_REGISTER.md` UNCHANGED;
`activated_domains() == ['electronics_electrical']`.** **P9-E1 = IMPLEMENTATION CANDIDATE ONLY — NOT closed** (formal closure is a
separate gate after independent review → Owner acceptance → merge (create-a-merge-commit) → post-merge verification); **NO new
domain activated; NO domain selected; P9-E2 NOT implemented; D4 NOT executed; D8 = OPEN / Owner-reserved; Phase 8 = FORMALLY
CLOSED; Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment / production = NOT AUTHORIZED.** The next state is: independent
review of this exact candidate → Owner acceptance → merge → post-merge verification → a separate bounded P9-E1 formal-closure gate.

**Immediately prior (retained as history — P9-E1 CONTRACT CANDIDATE, definition only; merged AUTHORITATIVE via PR #438 `8fbc239`):**
**The `P9-E1` / `P9-PREREQ-A` — Path-N Production Caller Domain Propagation implementation is DEFINED by a
governance-only CONTRACT CANDIDATE** (record: `docs/governance/P9_E1_PATH_N_CALLER_DOMAIN_PROPAGATION_CONTRACT.md`; authoritative
base `f08dd2e0319b2777c47dad9cdb49c05d106bc7a0` — PR #437 made P9-QS AUTHORITATIVE). This is the mandatory D3-registered
prerequisite **P9-PREREQ-A** now carried by the authoritative P9-QS §16; the Owner authorization **begins Phase 9 only at this
bounded contract gate.** **Live evidence (verified at `f08dd2e`): the prerequisite is STILL REQUIRED** — the Path-N seam is
already domain-aware (`engine/path_n_questions.py`), but the production callers in `engine/progression_loop.py` drop the in-scope
`domain` at three `get_path_n_question(...)` sites (line 232 in `get_question`; lines 269 and 273–274 in `get_display_question`),
so `get_question("mechanical", "MECHANISM_COMPLETENESS", 0, path="N")` returns the Electronics artifact text (domain-blind) while
the seam already yields `None` for `"mechanical"`. Canonical domain identity is available at every caller (`web/app.py:1566`,
`engine/progression_loop.py:904/944/981`, `scripts/run_cli.py:79` all pass `state.domain`); those three seam calls are the
complete production-caller set. **Bounded implementation (LATER, separate gate — NOT executed here):** thread `domain=domain` into
those three sites only; no signature/seam/registry/activation/web/CLI change; Electronics/`None` behavior and stall reframe
preserved exactly, correctly suppressed for a recognized-not-activated foreign domain. **RED design:** behavioral tests with the
neutral fixture `"mechanical"` on gap `MECHANISM_COMPLETENESS` (RED on baseline → GREEN after propagation) plus Electronics
GREEN-guards; not implemented in this gate. **Governance-only scope:** the new contract doc + append-only roadmap entry + this
current-truth sync + `CURRENT_PROJECT_STATE.md`; **`OWNER_DECISION_REGISTER.md` UNCHANGED; ZERO runtime/test/schema/prompt/
benchmark/web/CI diff.** **P9-E1 = IMPLEMENTATION CONTRACT CANDIDATE ONLY — authoritative only if this exact accepted candidate is
merged (create-a-merge-commit) and post-merge verified; the P9-E1 runtime + tests are a separate later gate, NOT authorized here;
NO new domain activated (`activated_domains() == ['electronics_electrical']`); NO domain selected; P9-E2 NOT implemented; D4 NOT
executed; D8 = OPEN / Owner-reserved; Phase 8 = FORMALLY CLOSED; Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment /
production = NOT AUTHORIZED.** Owner product/policy decisions required before P9-E1 acceptance: NONE — only independent review →
Owner acceptance → merge → post-merge verification, then a separate P9-E1 implementation gate. The next state is: P9-E1 contract
reviewed; if accepted+merged, a separate P9-E1 implementation gate performs the bounded propagation with RED→GREEN tests.

**Immediately prior (retained as history — P9-QS AUTHORITATIVE / merged PR #437 `f08dd2e`):**
**The `P9-QS` — Phase-9 Technical Quality Standard is DEFINED by a CORRECTED governance-only CONTRACT CANDIDATE** (record:
`docs/governance/P9_QS_PHASE_9_TECHNICAL_QUALITY_STANDARD_CONTRACT.md`; authoritative base
`99c08555351e031bd3cc11f536cf558c91dc0c32`). It is the corrected reissue that **supersedes the REJECTED prior candidate
`6a3e25df79bfe2399474a1ecf9154ca3ccfbe307`** (which remains **historical rejected evidence only — NOT modified / NOT merged /
NOT reused**); this is a NEW independent candidate from the current authoritative parent, not an amendment of the rejected SHA.
Corrections applied: **B1** — the future deterministic-calculation capability is assigned **no CAP number** (an unnumbered
*future deterministic-calculation adapter gate*); `CAP-06` is repository-canonical for the *Multi-Axis Invention Readiness
Dashboard* and MUST NOT be reused for it. **B2** — the **Output-Language override capability is DEFERRED / NOT IMPLEMENTED / NOT
AUTHORIZED / separately governed (D-P6-17 is the accepted decision, not the capability) and is NOT a pre-new-domain activation
prerequisite**; the actual repository-authoritative pre-new-domain prerequisite is the separate **Domain Registry validation
hardening (D-P6-14 / §5-I1, already CLOSED)**. Non-blocking O1 (audit/addendum/sweep = session-level review/development inputs,
not committed repository authority), O2 (`P9-PREREQ-A/B` are convenient labels for the already-D3-registered obligations, not
pre-existing canonical identifiers), and O3 (§4b references the existing **D13 knowledge-governance / evidence-governance /
licensing** family, reference/reuse only) also addressed. The standard expresses the Domain Capability Contract **through** the
canonical Domain Registry (§5-I1; no second registry), preserves the activation-quality principle, and keeps every deferred item
(deterministic-calculation adapter, Units, CAP-12/CAP-13/WS-PFV, D4, D8, Output-Language) as REFERENCE-ONLY / DEFERRED.
**Governance-only scope:** the new contract doc + append-only roadmap entry + this current-truth sync +
`CURRENT_PROJECT_STATE.md`; **`OWNER_DECISION_REGISTER.md` UNCHANGED; ZERO runtime/test/schema/prompt/benchmark/web/CI diff.**
**P9-QS = CONTRACT CANDIDATE ONLY — it becomes the authoritative contract-of-record only if this exact accepted candidate is
merged (create-a-merge-commit) and post-merge verified; there is NO active implementation increment; NO domain activated; the
future deterministic-calculation capability remains UNNUMBERED / DEFERRED; Output-Language remains separately governed / DEFERRED
and NOT an activation prerequisite; D8 = OPEN / Owner-reserved; Phase 8 = FORMALLY CLOSED; Phase 9 = INACTIVE / NOT AUTHORIZED
(accepting this standard does NOT open a Phase-9 implementation contract); Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED;
deployment / production = NOT AUTHORIZED.** Owner product/policy decisions required before P9-QS acceptance: NONE — only
independent review → Owner acceptance → merge → post-merge verification. The next state is: P9-QS reviewed; Phase 9 remains
inactive pending separate Owner authorization plus the Phase-9 entry gates (and, for a second/non-electronics domain, the
P9-PREREQ-A/B prerequisites and the already-CLOSED Domain Registry hardening D-P6-14 / §5-I1).

**Immediately prior (retained as history — D3 FORMALLY CLOSED):** **`D3` — Pre-Phase-9 Core Domain-Neutrality is FORMALLY CLOSED** as a governance-only CLOSURE CANDIDATE
(prerequisite closure only; authoritative if/when merged; dedicated record
`docs/governance/D3_CORE_DOMAIN_NEUTRALITY_FORMAL_CLOSURE_RECORD.md`; base `e51eaf7eee001ef6012579852c8da7cbeda8e144`, PR #435).
Contract PR #434 (`2dbde37`) + implementation PR #435 (`e51eaf7`; merge tree = accepted candidate tree `f027c93`, post-merge
verified; independent review ACCEPT WITH NON-BLOCKING OBSERVATIONS). D3-A/B/D live-verified; D3 focused 7 / full suite 2258
passed / 3 skipped / 1 xfailed / 0 failed. Canonical owners consumed not duplicated (domain_registry §5-I1 + domain_activation
§5-I2); D3-C not reopened; D8 untouched / Owner-reserved; `activated_domains() == ['electronics_electrical']` (only). **Three
mandatory future prerequisites REGISTERED (not authorized here):** Path-N caller propagation (before any second / non-electronics
domain activation); multi-activated tie precedence (before more than one specialist domain is activated); Phase-9 Capability
Overlap & Preservation Audit (before the first Phase-9 activation contract). **`OWNER_DECISION_REGISTER.md` UNCHANGED. There is
NO active implementation increment.** **D3 = FORMALLY CLOSED / AUTHORITATIVE (prerequisite closure only); Phase 8 = FORMALLY
CLOSED; Phase 9 = INACTIVE / NOT AUTHORIZED (D3 closure does NOT auto-open a Phase-9 contract or activate any domain); D8 = OPEN
/ Owner-reserved; Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment / production = NOT AUTHORIZED.** The next state is:
D3 prerequisite formally closed; Phase 9 remains inactive pending separate Owner authorization and the Phase-9 entry/audit
gates.

**Immediately prior (retained as history — D3 IMPLEMENTATION CANDIDATE):** The accepted **D3
contract is MERGED (PR #434, merge `2dbde37a3c409356691a17fd868f90b087df417c`; merge tree = accepted candidate tree, post-merge
verified)**, and **`D3` — Core Domain-Neutrality is now IMPLEMENTED as a governance-only IMPLEMENTATION CANDIDATE (RED →
GREEN)**: minimum-path corrections to exactly three existing engine seams + one new focused test — **D3-A**
`engine/safety_signal.py` (`domain_context` reflects the actual §5-I2 session domain, no longer force-mapped to the electronics
MVP for a non-electronics context; electronics safety cues unchanged); **D3-B** `engine/path_n_questions.py` (`get_served_question`
/ `get_path_n_question` honor an optional canonical `domain` identity; Electronics-owned artifact served only for Electronics /
`None`; a non-electronics identity is not silently served Electronics content); **D3-D** `engine/domain_rules.py` (`infer_domain`
consumes §5-I2 activation so an ACTIVATED domain wins a tie and a RECOGNIZED_NOT_ACTIVATED domain never becomes routing/admission
authority). Canonical owners consumed, never duplicated (`domain_registry.py` §5-I1 + `domain_activation.py` §5-I2). Behavioral
RED (4 seam defects) → GREEN: **D3 focused 7 / focused regressions 167 / web consumers 87 (2 skipped) / full suite 2258 passed /
3 skipped / 1 xfailed / 0 failed** (2251 baseline + 7); three load-bearing mutation probes each turned the targeted test RED and
were restored byte-identical. Scope invariants proven: only the three engine seams + the new test changed; D3-C (`web/app.py` +
`web/domain_label.py`) UNCHANGED; D8 (`domains/iot_electronics/**`) UNCHANGED; `activated_domains() == ['electronics_electrical']`
(only); no persistence/schema/commercial/quota/AccessGrant/auth diff. **D3 = IMPLEMENTATION CANDIDATE ONLY — NOT closed** (formal
closure is a separate gate after independent review → Owner acceptance → merge (create-a-merge-commit) → post-merge verification
→ remaining-obligation review); **NO domain activated; D8 OPEN / Owner-reserved; Phase 8 = FORMALLY CLOSED; Phase 9 / Phase 10 =
NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment / production = NOT AUTHORIZED.** There is no other active implementation
increment.

**Immediately prior (retained as history — D3 contract-of-record, definition only):** **`Phase 8` — Subscription, Billing and Entitlements is FORMALLY
CLOSED / AUTHORITATIVE** (technical-foundation phase; no active increment remains) — **P8-CLOSE merged PR #433
(`00792af36e51808191690a4bf66f9b1a2644d477`)**; dedicated record `docs/governance/PHASE_8_FORMAL_CLOSURE_RECORD.md`. **`D3` —
Core Domain-Neutrality is now DEFINED by a governance-only CONTRACT CANDIDATE** (Owner-authorized fresh gate; the Owner's
authorization begins with the current instruction — a prior draft `ed5eb14` was REJECTED / process-scope violation / NOT
authorized / NOT merged, preserved only as historical evidence; this candidate is fresh with a new SHA + new tree). Dedicated
record `docs/governance/D3_CORE_DOMAIN_NEUTRALITY_FORMAL_CONTRACT.md`; base `00792af…`. It covers exactly **D3-A**
(`engine/safety_signal.py`), **D3-B** (`engine/path_n_questions.py`), **D3-D** (`engine/domain_rules.py`); **excludes D3-C**
(independently verified remediated by §5-I2 + P6-1). It **consumes — never duplicates** — `engine/domain_registry.py` (§5-I1)
+ `engine/domain_activation.py` (§5-I2; `electronics_electrical` = the ONLY activated specialist domain; recognition ≠
activation). Frozen invariants (12); ONE BOUNDED D3 INCREMENT; likely RED-driven boundary = the three engine modules + focused
tests; prohibited: `web/app.py`, `web/domain_label.py`, `domains/iot_electronics/**`, new packs/activation/persistence/schema/
commercial/router. Genuine RED→GREEN + load-bearing mutation + create-a-merge-commit + post-merge verification required at
implementation; 23-item acceptance criteria frozen. **DOCUMENTED NO-VALID-RED** for this contract gate. **There is NO active
implementation increment.** Owner product/policy decisions required before D3 implementation: **NONE** (only explicit D3
implementation-gate authorization after contract acceptance). **D3 = CONTRACT CANDIDATE ONLY — becomes authoritative
contract-of-record only if this exact accepted candidate is merged (create-a-merge-commit) and post-merge verified; D3
implementation = NOT STARTED / NOT AUTHORIZED by this gate; NO domain activated; D8 / `iot_electronics` = OPEN / Owner-reserved
(blocks IoT activation only); Phase 8 = FORMALLY CLOSED / AUTHORITATIVE; Phase 9 / Phase 10 = NOT AUTHORIZED; PSRR = NOT
EXECUTED; deployment / production = NOT AUTHORIZED.**

**Immediately prior (retained as history — Phase 8 formal closure candidate status when written):** **`Phase 8` — Subscription,
Billing and Entitlements is FORMALLY CLOSED** as a governance-only CLOSURE CANDIDATE (P8-CLOSE; a technical-foundation phase
closure; authoritative if/when merged; dedicated record `docs/governance/PHASE_8_FORMAL_CLOSURE_RECORD.md`; base
`e7f7bc7e1f17550dc83d658976a07462de434e17`, PR #432). The Phase-8 Remaining-Obligation / Exit-Criteria Review returned **A —
ELIGIBLE FOR P8-CLOSE**. **Obligation closure matrix (all CLOSED / AUTHORITATIVE):** P8-C; P8-I1; P8-I2; P8-I3; P8-I4 (no
provider selected); P8-AF. **All mandatory Phase-8 exit criteria PASS**; N/A (contract-designed): real provider =
OWNER-SELECTION-TRIGGERED, P8-I4-I2 verified webhook + P8-I4-I3 reconciliation = EVIDENCE-TRIGGERED / DEFERRED, public paid
activation = OUTSIDE Phase 8. Delivered FOUNDATION ONLY (no commercial launch): plan-identity/entitlement + quota (sole
authority) + subscription-lifecycle mechanics + provider-neutral payment boundary + access-grant/resolution + subject-scoped
composition + fail-closed ambiguity; full suite 2251 passed / 3 skipped / 1 xfailed / 0 failed. **There is NO active
implementation increment.** Preserved OPEN/DEFERRED (none blocked closure): all Owner business decisions (plan names / pricing
/ currency / cadence / trial policy / packaging / enterprise / grandfathering / refunds / tax / grace / over-limit-downgrade /
provider selection / proration / cancellation timing); P8-AF future activation guards; trial / global-promo / Owner-Admin /
organization-named-seat / enterprise runtime; deferred capability lanes (QTA/ACV/PDF/Email/WS17/STG). PSRR = REGISTERED /
MANDATORY BEFORE PUBLIC PRODUCTION / NOT EXECUTED; `main`/OD-Q reconciliation = separate pre-production gate (not a blocker,
not performed). **Phase-8 closure authorizes nothing downstream.** **P8-C / P8-I1 / P8-I2 / P8-I3 / P8-I4 / P8-AF = CLOSED /
AUTHORITATIVE; Phase 8 = FORMAL CLOSURE CANDIDATE → FORMALLY CLOSED / AUTHORITATIVE if/when merged;** NO provider selected; NO
commercial model activated. **Next gate: separately authorized — Phase 9 is NOT AUTHORIZED and requires explicit Owner
authorization; no gate is auto-activated by Phase-8 closure.** Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED;
production / public paid activation BLOCKED / NOT AUTHORIZED.

**Immediately prior (retained as history — P8-AF FORMALLY CLOSED):** **`P8-AF` — Access, Licensing &
Organization Foundation is FORMALLY CLOSED** as a governance-only CLOSURE CANDIDATE (foundation-obligation closure only;
authoritative if/when merged). **P8-AF-I2** (uniform-subject correction) is **MERGED (PR #431, merge
`1132cfe8fde16a8c3a5784a2b1351a43620eda94`) / POST-MERGE VERIFIED** (independent review A); the P8-AF-C §22 closure criteria
are ALL satisfied: (a) P8-AF-C reviewed/accepted/merged (PR #429)/post-merge verified; (b) minimum increment(s) via P8-AF-I1 +
P8-AF-I2 with genuine RED→GREEN, proving the architecture can represent and resolve the models safely without activating any;
(c) authority boundaries (§4) + binding invariants (§6/§13/§16/§17/§18) demonstrated and unweakened; (d) dedicated closure
record produced (`docs/governance/P8_AF_ACCESS_LICENSING_ORGANIZATION_FOUNDATION_FORMAL_CLOSURE_RECORD.md`). Delivered
foundation (backend composition only; NO runtime activation): canonical source-neutral `AccessGrant`; one deterministic
read-only `resolve_access(grants, *, subject, now)` seam; provenance; P8-I1 entitlement reuse; P8-I2 quota non-interference;
P8-I3 lifecycle non-interference; P8-I4 provider independence; authenticated-subject-scoped resolution + cross-account grant
isolation; fail-closed competing-entitlement ambiguity; deterministic injected-time; **`[effective_from, effective_until)`
FROZEN**. **There is NO active implementation increment.** Deferred (remain deferred): organization / membership / named seats
/ seat persistence / campaign config / global promotional-free-access runtime / Owner-Admin authorization seam / 7-day trial
activation (automatic day-7 hard deletion NOT AUTHORIZED) / enterprise-custom billing / SSO-domain onboarding / concurrent
licensing — ALL NOT STARTED / DEFERRED; future hardening/triggers preserved (constructor hardening before first runtime
caller; durable duplicate-grant-id rule before first persistence; separately governed precedence before a second real source;
global/scope semantics separately governed; data ownership independent). **P8-AF-C = CLOSED / AUTHORITATIVE; P8-AF-I1 = CLOSED
/ AUTHORITATIVE; P8-AF-I2 = CLOSED / AUTHORITATIVE; P8-AF = FORMALLY CLOSED / AUTHORITATIVE; `P8-CLOSE` = NOT STARTED; Phase 8
= NOT CLOSED;** NO provider selected; NO access model activated. **Next Phase-8 gate: the separate Phase-8 Remaining-Obligation
/ Exit-Criteria Review and `P8-CLOSE` — NOT STARTED.** Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED;
production / public paid activation BLOCKED / NOT AUTHORIZED.

**Immediately prior (retained as history — P8-AF-I2 CORRECTIVE IMPLEMENTATION CANDIDATE):** **P8-AF-I1** is **MERGED (PR #430, merge
`1ac9c603b14a172a737f3577791e9f23a46533bd`) / POST-MERGE VERIFIED**; the Remaining-Obligation / Closure-Eligibility Review
returned **verdict B** (one mandatory pre-closure correction — the contract-required uniform-subject invariant, P8-AF-C §5.1
"given an authenticated account"). **P8-AF-I2 — Subject-Scoped Access Resolution is now IMPLEMENTED as a governance-only
CORRECTIVE IMPLEMENTATION CANDIDATE (RED → GREEN)**: the canonical resolver is now `resolve_access(grants, *, subject, now)`
(required authenticated `subject`); **subject scoping runs BEFORE entitlement composition**; a foreign-subject grant is
excluded **INERTLY** (never contributes/denies/raises) with explicit `foreign_subject` provenance (smallest-ambiguity — raising
would let another account deny/DoS this subject); an empty/missing subject is **NEVER** a wildcard; the post-filter precedence
is UNCHANGED (zero → DENY; one distinct entitlement → GRANT; competing distinct → FAIL CLOSED). `AccessGrant` UNCHANGED; single
runtime file changed (`engine/access_resolver.py`); no persistence/schema; no new dependency. Behavioral RED (mixed-subject
composition demo against merged I1 + 22 RED subject-scoped tests + six mutation probes) → GREEN: **focused 23 / P8-AF-I1+I2 53 /
Phase-8 177 / full suite 2251 passed / 3 skipped / 1 xfailed / 0 failed** (2228 baseline + 23); six probes each turned a test
RED and were restored byte-identical. Verified: cross-account grants never compose; foreign grant cannot rescue a denied
subject; **no authentication behavior** (subject already-authenticated; no email/password/session; no hardcoded Owner); **no
data-ownership implication** (access ≠ ownership); order-independent; `[effective_from, effective_until)` FROZEN; P8-I1/I2/I3/I4
authorities unchanged; OD-N unweakened. **Deferred (Review classifications): duplicate durable grant-identity rule = DEFERRED
UNTIL FIRST PERSISTENCE INCREMENT; direct-constructor hardening = DEFERRED BEFORE FIRST REAL RUNTIME CALLER; global/scope
(campaign) semantics = NOT STARTED / DEFERRED.** **P8-AF-I2 is a CORRECTIVE IMPLEMENTATION CANDIDATE ONLY — uniform-subject
isolation IMPLEMENTED IN CANDIDATE; P8-AF NOT closed.** Organization / membership / named seats — NOT STARTED / DEFERRED;
campaign — NOT STARTED / DEFERRED; Owner/Admin seam — NOT STARTED / DEFERRED; trial activation — NOT STARTED. **P8-AF-I1 =
MERGED/POST-MERGE VERIFIED; P8-AF-I2 = CORRECTIVE IMPLEMENTATION CANDIDATE; P8-AF = NOT CLOSED; `P8-CLOSE` = NOT STARTED;
Phase 8 = NOT CLOSED;** NO provider selected; NO access model activated. Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT
STARTED; production / public paid activation BLOCKED / NOT AUTHORIZED.

**Immediately prior (retained as history — P8-AF-I1 IMPLEMENTATION CANDIDATE):** The accepted **P8-AF-C** contract is **MERGED (PR #429, merge
`06683179f843b71f8d151f0c3c5647778b4b0acf`) / POST-MERGE VERIFIED**, and **P8-AF-I1 — Canonical Access-Grant +
Access-Resolution Foundation is now IMPLEMENTED as a governance-only IMPLEMENTATION CANDIDATE (RED → GREEN)** — the FIRST and
SMALLEST P8-AF increment, proving ONLY the canonical access-composition seam. `engine/access_grant.py` (NEW — a LEAF immutable,
source-neutral, provider-neutral `AccessGrant` value object whose fixed slots forbid quota/provider/credential/pricing/
data-ownership fields; fail-closed `make_access_grant(...)`; pure `is_effective_at`/`exclusion_reason`; imports no engine
module) + `engine/access_resolver.py` (NEW — the SINGLE deterministic, pure, read-only `resolve_access(grants, *, now)` →
immutable `AccessResolution`; **REFERENCES** the P8-I1 authority via `plan_catalog.entitlement_descriptor` for entitlement
IDENTITY validation only — never reads capabilities, never redefines entitlement; imports only `access_grant` + `plan_catalog`)
+ the OD-N guard extension recognizing both as commercial seams. **Minimal safe precedence (P8-AF-C §6; no invented business
priority):** zero effective grants → DENY; all-one-distinct-entitlement → GRANT that single entitlement (one quota path, never
additive); **competing distinct entitlements → FAIL CLOSED** (precedence deferred). Behavioral RED (import-absent + six
mutation probes) → GREEN: **focused 30 / Phase-8 154 / full suite 2228 passed / 3 skipped / 1 xfailed / 0 failed** (2198
baseline + 30); six probes each turned a test RED and were restored byte-identical. Verified: no double quota; explainable
provenance; resolver mutates nothing and consumes NO quota/lifecycle/account/payment; entitlement REFERENCED not redefined; NO
provider coupling; **NO authentication bypass** (no hardcoded Owner; privileged-looking subject/source confers nothing); **NO
data-ownership inference** (access ≠ ownership); injected epoch time only; order-independent determinism; fail-closed on
malformed/ambiguous input; **no new persistence/schema**; P8-I1/I2/I3/I4 authorities unchanged. **P8-AF-I1 is an IMPLEMENTATION
CANDIDATE ONLY — NOT closed; P8-AF NOT closed.** **Organization / membership / named seats — DEFERRED / NOT STARTED; campaign
configuration — DEFERRED / NOT STARTED; Owner/Admin authorization seam — DEFERRED / NOT STARTED; trial activation — NOT
STARTED.** **P8-AF-C = CLOSED / AUTHORITATIVE; P8-AF-I1 = IMPLEMENTATION CANDIDATE; P8-AF = NOT CLOSED; `P8-CLOSE` = NOT
STARTED; Phase 8 = NOT CLOSED;** NO provider selected; NO access model activated. Phase 9 / Phase 10 NOT AUTHORIZED; PSRR
EXECUTION NOT STARTED; production / public paid activation BLOCKED / NOT AUTHORIZED.

**Immediately prior (retained as history — contract-of-record = P8-AF-C, definition only):** **`P8-AF` — Access,
Licensing & Organization Foundation is now DEFINED by a governance-only CONTRACT CANDIDATE (P8-AF-C)** (dedicated record
`docs/governance/P8_AF_ACCESS_LICENSING_ORGANIZATION_FOUNDATION_CONTRACT.md`; base `61ff4a85989dfc8d9881764597d5d7dc415da213`,
PR #428). It defines the smallest canonical architecture — a provider-neutral, source-neutral **Access-Grant model** + a single
deterministic **effective-access resolution seam** — that **composes** P8-I1 (entitlement) / P8-I2 (sole quota authority) /
P8-I3 (canonical lifecycle, incl. `trialing`) / P8-I4 (payment boundary) **without duplicating** any of them (D-FPC-MAP-06),
preserving **Authentication ≠ Authorization ≠ Account identity ≠ Organization membership ≠ Seat assignment ≠ Data ownership ≠
Commercial entitlement ≠ Subscription lifecycle ≠ Payment state ≠ Billing ownership** and **paying ≠ owning user data**.
Contracted (definition only): a single resolver (no scattered access decisions); an access-grant traceable to its source; a
**deterministic precedence rule** (no double quota / plan-identity corruption / accidental downgrade / hidden bypass /
ambiguous revocation); a **7-day** trial reusing P8-I3 `trialing` (168h-vs-calendar OPEN; no runtime constant; trial→paid
preserves data); a **global configurable promotional campaign** operable **without a source-code change**; **Owner/Admin
non-billed access** as authorization→entitlement (no bypass; minimal role seam, no RBAC platform); canonical **organization /
membership / named-seat** capacity-assignment-reassignment (**reassignment never transfers prior-member data**; **billing
ownership ≠ data ownership**); enterprise/custom compatibility; safe **quota** + **lifecycle composition**; **audit/provenance +
deterministic revocation** (removes access, never data); preserved **data ownership** (**automatic day-7 hard deletion NOT
authorized**; retention a separate policy); the **smallest implementation increment**; a **12-item RED→GREEN acceptance
matrix**; the **OPEN owner/business decisions**; **P8-AF closure criteria**; and **explicit production/payment/Phase-9-10
blocks**. **There is NO active implementation contract** (P8-AF-C is definition only; a separate Owner-authorized `P8-AF`
implementation gate is required, and it must select only the smallest necessary seams). **P8-I4 = CLOSED / AUTHORITATIVE;
P8-AF-C = FORMAL CONTRACT CANDIDATE; P8-AF implementation = NOT STARTED; `P8-CLOSE` = NOT STARTED; Phase 8 = NOT CLOSED;** NO
provider selected; NO access model activated; NO organization/membership/seat/role/campaign/access-grant/pricing/
enterprise-billing runtime code or schema. Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED; production / public
paid activation BLOCKED / NOT AUTHORIZED.

**Immediately prior (retained as history — P8-I4 FORMAL CLOSURE / P8-AF REQUIRED NEXT):** **P8-I4 — Payment
Provider Boundary is FORMALLY CLOSED** as a governance-only CLOSURE CANDIDATE (increment closure only — authoritative if/when
merged). The accepted P8-I4-I1 implementation (independent review **verdict A — ACCEPT**) is **MERGED (PR #427, merge
`3a802fd84055f475feafcd55893da301af45c67d`; parents `fccd895` + `6f83e496…`; merged tree `191709299…`; exact diffstat 10
files / +1175 / −5) / POST-MERGE VERIFIED**; full suite **2198 passed / 3 skipped / 1 xfailed / 0 failed** (cited, not
re-run). Evidence-triggered lanes are **deferred / NOT triggered** (P8-I4-I2 verified webhook ingestion; P8-I4-I3
reconciliation; real-provider integration NOT STARTED; **provider selection OPEN OWNER DECISION**; real payment collection NOT
ACTIVATED). Canonical record: `docs/governance/P8_I4_PAYMENT_PROVIDER_BOUNDARY_FORMAL_CLOSURE_RECORD.md`. **Mandatory
handoff:** formal P8-I4 closure does **NOT** close Phase 8 — a separate cross-cutting obligation **`P8-AF` — Access, Licensing
& Organization Foundation** is **REGISTERED as the required next Phase-8 foundation gate, mandatory before `P8-CLOSE` / NOT
IMPLEMENTED / NOT ACTIVATED / NOT STARTED** (record:
`docs/governance/P8_AF_ACCESS_LICENSING_ORGANIZATION_FOUNDATION_OBLIGATION.md`; preserves **Authentication ≠ Authorization ≠
Account identity ≠ Data ownership ≠ Commercial entitlement ≠ Subscription lifecycle ≠ Payment state ≠ Billing ownership** and
**paying ≠ owning user data**; NON-ACTIVATED future-readiness scope = individual access, a **7-DAY** (NOT 14) per-account
trial preserving durable data on trial→paid [**automatic day-7 hard deletion NOT authorized**; 168h-vs-calendar semantics
OPEN], a **global configurable promotional free period** administrable **without a source-code change**, **Owner/Admin
non-billed access** as an explicit auditable authorization→entitlement grant [no bypass], **organization/named-seat
licensing** [billing ownership ≠ data ownership; seat reassignment never transfers prior-member data], enterprise/custom
compatibility, a deterministic **access-resolution precedence**, safe **quota composition** [P8-I2 remains the sole quota
authority], and **no second lifecycle state machine** [P8-I3 remains canonical; D-FPC-MAP-06]). **There is NO active
implementation contract.** **Expected next gate: `P8-AF-C` — Access, Licensing & Organization Foundation Contract (governance
contract first; NO implementation before it is independently reviewed and accepted).** **Phase 8 remains OPEN / NOT CLOSED;
`P8-AF` / `P8-AF-C` / `P8-CLOSE` NOT STARTED; NO real provider selected; NO provider SDK; NO webhook; NO trial/promotional/
Owner-Admin/organization access activated; NO roles/organizations/seats/campaign implemented; NO automatic trial-data
deletion.** Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED; production / public paid activation BLOCKED / NOT
AUTHORIZED.

**Immediately prior (retained as history — P8-I4-I1 IMPLEMENTATION CANDIDATE):** The accepted **P8-I4-C** contract is **MERGED (PR #426, merge
`fccd8955afdfdd5167c4b7a4f0dbe6c14d00127b`) / POST-MERGE VERIFIED**, and **P8-I4-I1 — Provider-Neutral Payment Boundary
Foundation is now IMPLEMENTED as a governance-only IMPLEMENTATION CANDIDATE (RED → GREEN)**: `engine/payment_provider_port.py`
(NEW port + canonical types + stdlib fingerprint) + `engine/payment_fake_adapter.py` (NEW two fakes A/B — replaceability) +
`engine/payment_ingestion.py` (NEW coordinator) + additive `engine/account_store.py` (`_apply_lifecycle_in_txn` refactor
[P8-I3 unchanged] + `provider_mapping` + `provider_event_dedupe` tables + mapping/ingest methods; atomic dedupe + P8-I3
lifecycle in ONE `BEGIN IMMEDIATE`) + `tests/test_p8_i4_i1_payment_provider_boundary.py` (30 tests) + the OD-N guard
extension. Behavioral RED (seven boundary defects) → GREEN: focused 30 / Phase-8 124 / **full suite 2198 passed / 3 skipped /
1 xfailed / 0 failed**; seven mutation probes each turned a test RED and were fully restored (byte-identical); two-thread races
deterministic. **NO real provider selected; NO provider SDK; NO webhook.** Preserved: canonical-mapping-only (raw provider name
never enters the P8-I3 log); strict provider-event idempotency (conflicting fingerprint fails closed); P8-I1/I2/I3 authorities
unchanged; anti-lockout; opaque refs; no raw payload/secret/card persisted; OD-N import isolation. **P8-I4-I1 is an
IMPLEMENTATION CANDIDATE ONLY — NOT closed; Phase 8 NOT complete / NOT paid-active**; candidate-only until independent
implementation review → Owner acceptance → PR → pre-merge check → merge → post-merge verification → a dedicated P8-I4 closure
gate. **P8-I4-I2 (verified webhook ingestion) / P8-I4-I3 (reconciliation) / real-provider selection sub-gate: NOT STARTED**
(real-provider work requires a separate Owner provider-selection decision). P8-CLOSE NOT STARTED; Phase 9 / Phase 10 NOT
AUTHORIZED; PSRR EXECUTION NOT STARTED; production / public paid activation BLOCKED.

**Immediately prior (retained as history — P8-I4-C CONTRACT CANDIDATE):** **Current contract-of-record (DEFINITION ONLY, no implementation
authority): P8-I4-C — Payment Provider Boundary — Bounded Contract & Architecture** (governance/documentation-only CONTRACT
CANDIDATE; base `f66ea96` (PR #425); dedicated contract
`docs/governance/PHASE_8_I4_PAYMENT_PROVIDER_BOUNDARY_INCREMENT_CONTRACT.md`; authoritative if/when independently reviewed,
Owner-accepted, merged, post-merge verified). It freezes the smallest provider-neutral payment boundary (adapter port;
canonical↔provider separation; opaque canonical identities; additive mapping/dedupe persistence; event-authenticity + hard
secrets boundary; **strict provider-event idempotency incl. conflicting-payload fail-closed** — resolving the P8-I3
non-blocking observation; atomicity; P8-I1/I2/I3 authority preserved with adapters mapping to the P8-I3 lifecycle seam;
fail-closed catalogue; outage/reconciliation rules; replaceability acceptance property; PCI architectural avoidance with no
compliance claim; a 30-item future RED matrix; fake-adapter-first decomposition). **NO provider selected** — provider
selection is an OPEN Owner decision and a registered prerequisite for real adapter work. **P8-I4-C confers NO implementation
authorization; P8-I4 remains NOT STARTED / NOT IMPLEMENTED / NOT AUTHORIZED** — a separate Owner-authorized P8-I4
implementation gate (starting with the fake/reference-adapter P8-I4-I1) is required. Immediately prior: **P8-I3 — Subscription
Lifecycle FORMALLY CLOSED** (PR #424 `cef9a52`). Phase 8 OPEN; P8-CLOSE NOT STARTED; Phase 9 / Phase 10 NOT AUTHORIZED; PSRR
EXECUTION NOT STARTED; production / public paid activation BLOCKED / NOT AUTHORIZED.

**Immediately prior (retained as history):** **P8-I3 — Subscription
Lifecycle is FORMALLY ACCEPTED AND CLOSED** (increment closure only): corrected implementation candidate
`8e600c0674bfeb7be96fd6875b68de1da02eae2f` (initial verdict B → corrected re-reviewed **A**) **MERGED (PR #424, merge
`cef9a522dfae53493ceb1b47bd9faf409617e13e`; parents `09743b9` + `8e600c0`; merged tree `3d1586e…` == accepted candidate tree)
/ POST-MERGE VERIFIED (Pre-Merge Safety Check PASS; Post-Merge Verification PASS)**; dedicated record
`docs/governance/P8_I3_SUBSCRIPTION_LIFECYCLE_FORMAL_CLOSURE_RECORD.md` (**DOCUMENTED NO-VALID-RED — GOVERNANCE-ONLY FORMAL
CLOSURE GATE**). RED→GREEN focused 45 / Phase-8 94 / full suite 2168 passed / 3 skipped / 1 xfailed / 0 failed; diffstat 8
files / 1416 / −10. The invalidated prior implementation candidate `4385a33` (verdict B) remains EVIDENCE-ONLY / NOT MERGED.
Non-blocking observations preserved (idempotency-payload replay carried to P8-I4; optional future store-level stale test — do
not reopen P8-I3). **P8-I3 closure is an increment closure only — it does NOT close Phase 8, does NOT start P8-I4, selects NO
payment provider, and enables NO public paid activation.** **NEXT PHASE-8 GATE: `P8-I4` — Payment Provider Boundary — NOT
STARTED / NOT AUTHORIZED to begin by this closure (no provider selected).** Phase 8 OPEN; P8-CLOSE NOT STARTED; Phase 9 /
Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED; production / public paid activation BLOCKED.

**Immediately prior (retained as history):** the P8-I3 IMPLEMENTATION CANDIDATE (CORRECTED). The accepted **corrected
P8-I3-C** contract is **MERGED
(PR #423, merge `09743b91b764e5ac2956401d7a88c91df48d3d8b`) / POST-MERGE VERIFIED**, and **P8-I3 — Subscription Lifecycle is
now IMPLEMENTED as a governance-only IMPLEMENTATION CANDIDATE (RED → GREEN; verdict-B CORRECTED — supersedes the invalidated
prior implementation candidate `4385a33`, EVIDENCE-ONLY / NOT MERGED)**: `engine/subscription_lifecycle_service.py` (NEW seam)
+ additive `engine/account_store.py` lifecycle tables/methods (append-only event log source-of-truth carrying the scheduled
target plan + derived cache; one-`BEGIN IMMEDIATE` atomicity with **in-transaction** stale-effective_at + pending-schedule
exclusivity + from-state guards) + `tests/test_p8_i3_subscription_lifecycle.py` (45 tests) + the OD-N guard extension.
Verdict-B corrections RC-I1..RC-I6 implemented and mutation-proven (pending-schedule exclusivity; in-txn stale check;
different-transition conflict guard causally tested; scheduled target plan in the event log + reconstructable; event-id-scoped
materialization idempotency; lifecycle reads fail closed for missing/disabled/deleted). Behavioral RED → GREEN: focused 45 /
Phase-8 94 / **full suite 2168 passed / 3 skipped / 1 xfailed / 0 failed**; six correction mutation probes each turned a test
RED and were fully restored (byte-identical); two-thread races deterministic. Preserved: `none` entitlement-neutral,
canonical `past_due` exits, unique cancellation mapping, P8-I2 sole quota authority + no reset, anti-lockout, provider
neutrality, OD-N. **P8-I3 is an IMPLEMENTATION CANDIDATE ONLY — NOT closed; Phase 8 NOT complete / NOT billing-live / NOT
paid-active**; no provider selected; candidate-only until independent re-review → Owner acceptance → PR → pre-merge check →
merge → post-merge verification → a dedicated formal P8-I3 closure gate. P8-I4 / P8-CLOSE NOT STARTED; Phase 9 / Phase 10 NOT
AUTHORIZED; PSRR EXECUTION NOT STARTED; production / public paid activation BLOCKED.

**Immediately prior (retained as history):** the corrected P8-I3-C contract-of-record (definition only) —
**P8-I3-C — Subscription Lifecycle — Bounded Implementation Contract (CORRECTED — verdict-B remediation)**
(governance/documentation-only CONTRACT CANDIDATE; base `0a19daf` (PR #422); dedicated contract
`docs/governance/PHASE_8_I3_SUBSCRIPTION_LIFECYCLE_INCREMENT_CONTRACT.md`; authoritative if/when independently re-reviewed,
Owner-accepted, merged, post-merge verified). It **supersedes the prior candidate `ead186d`** (independent review verdict
**B — ACCEPT WITH REQUIRED PRE-MERGE CORRECTIONS**; INVALIDATED / NOT MERGEABLE / EVIDENCE-ONLY / NOT MERGED; preserved as
evidence). Corrections applied: **RC-1** `none` entitlement-neutral (no silent legacy downgrade); **RC-2** canonical
`past_due` exits (`subscription_expired`/`subscription_cancelled`); **RC-3** unique cancellation-request mapping
(`subscription_change_scheduled` reserved for PLAN changes only); + due-scheduled-transition materialization and
equal-`effective_at` tie-break clarifications. It defines the smallest safe provider-neutral, additive, backward-compatible,
deterministic, auditable, account-scoped lifecycle state model + persistence/service boundaries (subordinate to P8-C §6 and
the closed P8-I1/P8-I2 foundations; honoring G-MPR-01-D D2). **There is NO active *implementation* contract-of-record;
P8-I3-C confers NO implementation authorization** — a separate Owner-authorized P8-I3 implementation gate is required.
**P8-I3 remains NOT STARTED / NOT IMPLEMENTED / NOT AUTHORIZED.** Immediately prior: G-MPR-01-D (findings disposition;
formally closed P8-I1; registered the P8-I3 persistence rule + future gates) — MERGED (PR #422). Phase 8 OPEN; P8-I4 /
P8-CLOSE NOT STARTED; Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED; production / public paid activation
BLOCKED. (Header note: this "Active contract"
section previously still labeled **D-P6-18 — Global UI Language** as the status line; that increment is
**FORMALLY ACCEPTED AND CLOSED** — see below — and is preserved as history, not the current active gate; the running current
truth is in the paragraph that follows and in `CURRENT_PROJECT_STATE.md` + `ACTIVE_EXECUTION_ROADMAP.md`.)

**Immediately prior (retained as history):** **D-P6-18 — Global UI Language (English | العربية) (Phase 6)** —
**IMPLEMENTED / INDEPENDENTLY REVIEWED (B — ACCEPT, zero blockers) / MERGED (PR #388, merge `b47bf4bb57446956c47488283248cfbacd603e85`; parents `a0426cbb6a188a366006d22472c875ec4e5e446b` + `62818a8c71a83be487928d8b2ccaa2feb4dd678d`; merged tree `f6ed63d94db15a5e84326f9e551a7c1eddd3dd34`) / POST-MERGE VERIFIED / FORMALLY ACCEPTED AND CLOSED (G-DP6-18-GLOBAL-UI-LANGUAGE-FORMAL-CLOSURE-01; dedicated record `docs/governance/D_P6_18_GLOBAL_UI_LANGUAGE_FORMAL_CLOSURE_RECORD.md`).**
Accepted lineage `98c47d5` → `8920f46` → `62818a8` (SHA-preserving); cumulative scope 27 files / +2012 / −337, entirely under `web/` + `tests/` (no engine/domains/schema/migration/dependency/CI). There is **no active contract-of-record**. Closing D-P6-18 authorizes **no** successor: the **Question Translation Assistant remains NOT AUTHORIZED / NOT STARTED**. **Current truth (synchronized):** the Master Obligation Index governance-only gate was subsequently OWNER-AUTHORIZED and MERGED (PR #390, tip `9665413`; **D-MOI-01** / **G-MOI-01**), and the **executed Phase 6 lane — Domain Specialization / Truthful Specialist Labeling, Option A — is now FORMALLY ACCEPTED AND CLOSED** (owner gate **G-PHASE-6-DOMAIN-SPECIALIZATION-FORMAL-CLOSURE-01**; **D-P6-CLOSE**; dedicated record `docs/governance/PHASE_6_DOMAIN_SPECIALIZATION_FORMAL_CLOSURE_RECORD.md`). The Product-Foundation §5 "Multi-Domain and Technology Capability Foundation" is a **DISTINCT FUTURE PROGRAM — NOT closed / NOT authorized** by that closure. **Current contract-of-record (definition only): §5-C1 — Product-Foundation §5 Multi-Domain & Technology Capability Foundation** — a governance/documentation-only contract-definition + owner-decision gate (**G-S5-C1-MULTI-DOMAIN-FOUNDATION-CONTRACT-01**; dedicated contract `docs/governance/PRODUCT_FOUNDATION_S5_MULTI_DOMAIN_FOUNDATION_CONTRACT.md`; owner decisions **D-S5-C1** / **D-S5-01…D-S5-09**). It records owner decisions, a formalized backward-compatible domain-pack contract, and a bounded 5-increment plan (§5-I1…§5-CLOSE), and **authorizes no implementation**. There is **no active *implementation* contract-of-record**. **§5-I1 — Domain Registry Validation Hardening (D-P6-14) is IMPLEMENTED / INDEPENDENTLY REVIEWED (B, zero blockers) / MERGED (PR #393, merge `9d5e3bf1870d9f59def8bcd0d686a5b682886c8a`; parents `3da1e03`+`5d518f4`; merged tree `a62f46f`) / FORMALLY ACCEPTED AND CLOSED** (gate **G-S5-I1-DOMAIN-REGISTRY-HARDENING-FORMAL-CLOSURE-01**; **D-S5-I1-CLOSE**; dedicated record `docs/governance/S5_I1_DOMAIN_REGISTRY_HARDENING_FORMAL_CLOSURE_RECORD.md`). It hardened the existing canonical Domain Registry only (no new registry; D-FPC-MAP-06); no domain activated; electronics-only activation unchanged. **§5-I2 — Activation-status policy + explicit unsupported-domain model is now IMPLEMENTED / INDEPENDENTLY REVIEWED (foundation B + completion-delta B, zero blockers) / MERGED (PR #396, merge `e224215228b52a53bb2a0cba8eacbdfc19e1ed78`; parents `4770244`+`56afc7a`; merged tree `1576c9c`) / FORMALLY ACCEPTED AND CLOSED** (gate **G-S5-I2-ACTIVATION-STATUS-POLICY-FORMAL-CLOSURE-01**; **D-S5-I2-CLOSE**; dedicated record `docs/governance/S5_I2_ACTIVATION_STATUS_POLICY_FORMAL_CLOSURE_RECORD.md`). It added an explicit engine activation policy (three support states; electronics-only activation, pack-status ≠ activation; web admission bound to the policy) with no domain activated and no persistence/domain-pack/user-copy change. **§5-I3 — Subsystem + cross-domain project model foundation is now IMPLEMENTED / INDEPENDENTLY REVIEWED (B, zero blockers) / MERGED (PR #398, merge `dac5696ebcf9c9814b2adb66887a535e089a6c85`; parents `04a9c4d`+`0a7f135`; merged tree `63a63e3`) / FORMALLY ACCEPTED AND CLOSED** (gate **G-S5-I3-SUBSYSTEM-CROSS-DOMAIN-MODEL-FORMAL-CLOSURE-01**; **D-S5-I3-CLOSE**; dedicated record `docs/governance/S5_I3_SUBSYSTEM_CROSS_DOMAIN_MODEL_FORMAL_CLOSURE_RECORD.md` — closure authoritative if/when its governance candidate is merged). It added an additive in-memory subsystem foundation (one project → zero-or-more subsystems → each may reference a canonical domain as metadata; support-state via the §5-I2 policy) with the scalar root domain and all persistence preserved; durable subsystem persistence / identity / display-name / subsystem-grain evidence-risk-validation remain **future / NOT delivered**. **§5-I4 — EVIDENCE GATE NOT MET → SKIP at current evidence** (no Technology Capability Registry). **Product-Foundation §5 — Multi-Domain and Technology Capability Foundation is now FORMALLY ACCEPTED AND CLOSED** (gate **G-S5-CLOSE-PRODUCT-FOUNDATION-FORMAL-CLOSURE-01**; **D-S5-CLOSE**; dedicated record `docs/governance/PRODUCT_FOUNDATION_S5_FORMAL_CLOSURE_RECORD.md`; closure authoritative if/when its governance candidate is merged) after §5-C1 + §5-I1 + §5-I2 + §5-I3 + the §5-I4 evidence-gate decision and the four governance-gap reconciliations (GAP-1…GAP-4); ORIGINAL §5 unfinished material obligation = NONE; POST-§5 material implementation gap = NONE. **Phase 7 — API and Integration Foundation** (canonical authority in `PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md` §5) is now the **active phase** under a **Standing Owner Authorization**. **Current contract-of-record: P7-C — Formal Phase-7 Contract & Acceptance Criteria** — an owner-accepted governance/documentation-only Phase-7 contract-of-record (owner gate **G-P7C-FORMAL-PHASE-7-CONTRACT-PUBLICATION-01**; **D-P7C-01**; dedicated contract `docs/governance/PHASE_7_API_AND_INTEGRATION_FOUNDATION_P7C_CONTRACT.md`) that formalizes the frozen P7-A discovery + P7-B architecture decisions (and both accepted P7-B/P7-C correction addenda) — read/export-first v1 (product surface = Project read + Versioned Structured Output/Export only); a Lean internal read/export service seam before public exposure; a distinct least-privilege machine/API identity separate from browser auth; a first-public-exposure security baseline (authn/authz/version-identity/stable-errors/correlation/audit/rate-limit/provenance); the outbound canonical→adapter→vendor boundary (InventorAI central context authority; no orchestrator); the untrusted-by-default inbound-result invariant; DEFERRED subsystem-durable-identity / async / write-import / inbound-persistence / vendor-integration; Audit≠Monitoring and rate-limit≠all-Abuse-Controls and Reference-Harness≠Partner-Sandbox as distinct preserved obligations; and a §18 obligation register whose closure classification is **RESERVED EXCLUSIVELY for a mandatory §25 Phase-7 Remaining-Obligation / Exit-Criteria Review (a successful first proof never auto-authorizes P7-CLOSE)**. **The P7-C contract itself confers no implementation authorization.** **A distinct, later owner decision — the Standing Phase-7 Authorization (`D-P7-STANDING-01`) — GRANTS continuation through the remaining Phase-7 gates and formal Phase-7 closure, subject to the contract boundaries, per-gate bounded scope, accepted evidence triggers, tests where applicable, Lean minimum-path, independent review where required, and the §25 exit review; no repeated top-level owner authorization is required at each intermediate gate, but no gate self-activates.** **Standing authorization ≠ active implementation increment:** **there is currently no active implementation increment.** The **P7-I1 — Internal Read/Export Service Boundary** increment (P7-C §8 first slice; bounded contract merged PR #402, merge `0041097`) is now **IMPLEMENTED / INDEPENDENTLY REVIEWED (A — ACCEPT; one required pre-merge correction applied and independently re-reviewed A) / MERGED (PR #403, merge `94ccccd4399847d5fc0fc477f24bed5145d9a7d3`; parents `0041097`+`8f30f4f`; merged tree `fba951ed86a269e2487352e206b3de65979e6e65` == accepted candidate tree) / POST-MERGE VERIFIED / FORMALLY ACCEPTED AND CLOSED** (increment closure under the Standing Phase-7 Authorization `D-P7-STANDING-01`; dedicated record `docs/governance/P7_I1_INTERNAL_READ_EXPORT_SERVICE_BOUNDARY_FORMAL_CLOSURE_RECORD.md`; closure authoritative if/when this governance candidate is merged). It delivered one thin Flask-free internal seam `engine/read_export_service.py` — authorized durable Project Read via `store.load_contract`, and a distinct deterministic Structured Export composed from durable record data + canonical domain support-state (`store.load_reconstruction_inputs` → `engine.domain_activation.support_state`) — consuming the existing `store.load_owner` ownership foundation + explicit caller identity, fail-closed (NULL-owner not auto-authorized; IR-5), with no `web/app.py` change (IR-3/IR-4), no datastore construction in the seam (IR-1), no `ProjectRecordContract`/`from_state(live_state)` use (IR-2), no frozen public/export version or field names (IR-6), no public API, no governed-state mutation; changed paths = exactly `engine/read_export_service.py` + `tests/test_p7_i1_read_export_service.py` (+448). Independently reproduced evidence: focused 22 passed; regression anchors 69 passed; full suite 2047 passed / 1 skipped / 1 xfailed / 0 failed. Superseded implementation candidate `acf0c46` is evidence only (NOT accepted). **P7-I1 closure is an increment closure only — it does NOT close Phase 7, creates NO public API, and satisfies NO later Phase-7 obligation** (API security/versioning/machine identity/scopes/rate-limits/audit/adapters/import-export remain governed by P7-C and later increments; the mandatory §25 Remaining-Obligation / Exit-Criteria Review remains reserved before P7-CLOSE). The **P7-I2 — Versioned Read/Export Public API + first-public-exposure security baseline** increment is now **CONTRACT ESTABLISHED (independently reviewed A + Owner-accepted; MERGED PR #405) / IMPLEMENTED / INDEPENDENTLY REVIEWED (A — ACCEPT) / OWNER ACCEPTED / MERGED (PR #406, merge `5971b7a1c35186aa6bdb425b6846bd633d5f8b11`; parents `7abdd06`+`cd46c7f`; merged tree `a299bce1cc6e58b873fb3e20a1e6f98a7b1ab1ae` == accepted candidate tree) / POST-MERGE VERIFIED / FORMALLY ACCEPTED AND CLOSED** (increment closure under the Standing Phase-7 Authorization `D-P7-STANDING-01`; dedicated record `docs/governance/P7_I2_VERSIONED_READ_EXPORT_PUBLIC_API_FORMAL_CLOSURE_RECORD.md`; closure authoritative if/when this governance candidate is merged). It delivered a versioned read-only public API (`GET /api/v1/projects/<id>` + `.../export`; `web/api_v1.py` blueprint mounted in `web/app.py` by registration only) that **consumes the P7-I1 seam** (no business-logic duplication) with the full first-public-exposure security baseline: a distinct machine/API principal (`Authorization`-header credential, never the browser session; bound to one `owner_account_id`; token-style hash-only secret; issuance/revocation/expiry/rotation + bound-account-status enforcement) with a single `project:read` scope; API + export version identity; a stable non-enumerating error envelope (cross-owner ≡ missing); request/correlation identity (malformed caller value replaced); a durable minimal access/security audit (`access_audit`, fail-closed on audit-write failure); and two-tier rate limiting reusing the hardened atomic `record_rate_attempt` (a pre-auth bounded-subject limiter before secret verification + a post-auth `api_read` limiter; both fail-closed). `api_credentials`/`access_audit` are additive tables in the existing `SqliteAccountStore` schema lifecycle with no handler-owned DDL/migration; no project-state mutation; no writes/import; no P7-I3/adapters. Changed paths = exactly `engine/account_store.py` + `web/api_v1.py` + `web/app.py` (mount) + `tests/test_p7_i2_public_api.py` (+1076). Independently reproduced evidence at the merged tip: P7-I2 focused 36 passed; P7-I1 + ownership + record-store regressions 52 passed; full suite 2083 passed / 1 skipped / 1 xfailed / 0 failed. Superseded pre-review contract candidate `4933c26` is evidence only (NOT accepted). Retained NON-BLOCKING observations: post-auth `api_read` limiter runs after the scope check; residual micro-timing on unknown credential id; `API_CREDENTIAL_STATUSES` currently inert/documentary; `access_audit` is append-only with no retention/cleanup path (later obligation — retention NOT solved). **P7-I2 closure is an increment closure only — it does NOT close Phase 7 and satisfies NO remaining Phase-7 obligation** (quotas, import/write, webhooks, adapters/P7-I3, partner sandbox, monitoring, broad abuse controls, audit retention remain governed by P7-C and later increments; the mandatory §25 Remaining-Obligation / Exit-Criteria Review remains reserved before P7-CLOSE). The **P7-I3 — Canonical Export + Local/Reference Adapter Proof (outbound-only, non-mutating)** increment is now **CONTRACT ESTABLISHED (independently reviewed A + Owner-accepted; MERGED PR #408) / IMPLEMENTED / INDEPENDENTLY REVIEWED (A — ACCEPT; one required pre-merge guard-hardening correction applied and independently re-reviewed A) / OWNER ACCEPTED / MERGED (PR #409, merge `2ee60ec018d3816c47ad20ac2136e61aa1f9d3b9`; parents `c66a219`+`27e3104`; merged tree `76ce6007aa4faffa9bb6bd8081d3616ade042dc6` == accepted candidate tree) / POST-MERGE VERIFIED / FORMALLY ACCEPTED AND CLOSED** (increment closure under the Standing Phase-7 Authorization `D-P7-STANDING-01`; dedicated record `docs/governance/P7_I3_CANONICAL_EXPORT_LOCAL_REFERENCE_ADAPTER_PROOF_FORMAL_CLOSURE_RECORD.md`; closure authoritative if/when this governance candidate is merged). It delivered one local, deterministic, network-free, vendor-neutral **reference** adapter `engine/export_adapter.py` that consumes the canonical P7-I1 Structured Export (no second output model; no invented export-version identity) → a structurally distinct flattened reference DTO → an independent semantic `validate_equivalence` enforcing a contract-owned non-empty preservation floor + integrity/tamper detection (changed-floor-field / missing / duplicate / `record_id`-collision / `assertion_count`·`validation_summary`·`provenance_summary` row-inconsistency / malformed all fail); outbound-only, non-mutating, UNTRUSTED BY DEFAULT; no store/network/Flask/vendor; no public-API/domain-activation change. Changed paths = exactly `engine/export_adapter.py` + `tests/test_p7_i3_export_adapter.py` + `tests/test_p7_i2_public_api.py` (+517/−11). The P7-I2 amendment strengthened (not weakened) the adapter-import boundary, preserving the P7-I2 import allowlist and all security tests (independently reviewed A). Independently reproduced evidence at the merged tip: P7-I3 focused 21 passed; P7-I2 suite 37 passed; combined regressions 102 passed; full suite 2105 passed / 1 skipped / 1 xfailed / 0 failed. Superseded pre-review candidates `51b8fc6` (contract) and `8ee0551` (implementation) are evidence only (NOT accepted; local evidence tags; remote tag not verified/present). **P7-I3 closure is an increment closure only — it does NOT close Phase 7 and satisfies NO remaining Phase-7 obligation.** There is **no active implementation increment**. P7-I3 formal closure was MERGED (PR #410, merge `7fda709209f9c97d67bdaf752de7bda3a951ce15`; parents `2ee60ec`+`24dbe0f`; merged tree `e77d475508f53c6360a5a1b990f3e974842e7455`) / POST-MERGE VERIFIED. The mandatory **§25 Phase-7 Remaining-Obligation / Exit-Criteria Review** is now **PERFORMED as a governance-only REVIEW CANDIDATE** (dedicated record `docs/governance/PHASE_7_REMAINING_OBLIGATION_EXIT_CRITERIA_REVIEW.md`; authoritative if/when independently reviewed, Owner-accepted, and merged). It classifies all **35 P7-C §18 obligations** — **18 DELIVERED AND VERIFIED**, **17 INTENTIONALLY DEFERRED WITH OWNER-REASON-TRIGGER** (each trigger unfired), **0 NOT APPLICABLE**, **0 STILL REQUIRED BEFORE PHASE-7 CLOSURE** — yielding **PHASE-7 EXIT VERDICT: PASS — ELIGIBLE FOR A SEPARATE FORMAL PHASE-7 CLOSURE GATE** (eligibility only; not production readiness; monitoring / broad abuse controls / audit retention / partner sandbox / write-import / inbound / subsystem durable identity / async-webhook / real-vendor remain preserved trigger-deferred obligations). **Phase 7 remains OPEN / IN PROGRESS; the §25 review does NOT close Phase 7 and creates NO formal closure record.** The §25 review is now **AUTHORITATIVE / MERGED (PR #411, merge `1a8d4c70acf05f7d787d5ae24c26b6323b51b7a7`; parents `7fda709`+`dbe54e1`; merged tree `909d7bf`) / POST-MERGE VERIFIED**. **P7-CLOSE — Formal Phase-7 Closure** is now **PERFORMED as a governance-only CLOSURE CANDIDATE** (dedicated record `docs/governance/PHASE_7_FORMAL_CLOSURE_RECORD.md`) under `D-P7-STANDING-01`: it closes the **accepted Phase-7 scope under P7-C**, preserving the authoritative §25 result verbatim (35 obligations: 18 DELIVERED AND VERIFIED / 17 INTENTIONALLY DEFERRED WITH OWNER-REASON-TRIGGER / 0 NOT APPLICABLE / 0 STILL REQUIRED; EXIT PASS). **Phase-7 formal closure is CANDIDATE ONLY until this governance candidate is independently reviewed, Owner-accepted, merged, and post-merge verified** — only then is **Phase 7: FORMALLY CLOSED**. Closure makes **NO** production/security/operations-readiness claim; the 17 deferred obligations remain **future governed obligations with their accepted triggers** (NOT delivered — Audit≠Monitoring, rate-limit floor≠broad abuse controls, reference harness≠partner sandbox all preserved; access_audit retention remains an unresolved operational observation, not a closure obligation). **Phase 7 is now FORMALLY CLOSED** (P7-CLOSE MERGED PR #412, merge `c15b7e72272951a8e32d3065d96e7a24ebd1a993`; parents `1a8d4c7`+`db09fe4`; merged tree `5b25ccb`; POST-MERGE VERIFIED). The current gate is **PSRR — Production Security & Release Readiness — GOVERNANCE REGISTRATION** (NOT PSRR execution): a governance-only registration of the Owner-mandated cross-phase release gate (dedicated record `docs/governance/PSRR_PRODUCTION_SECURITY_RELEASE_READINESS_REGISTRATION.md`; durable Owner decision **D-PSRR-01**), registered as the **named release gate operationalizing OD-P / Phase-10 ownership** (D-FPC-MAP-06: existing owner extended — no competing framework; Phase 10 owns production/release/security/operational readiness; OD-P defers evaluation to Phase 10 after Phases 4–9). **PSRR governance registration is now MERGED (PR #413, merge `6c0626e3ca659f90133a7df865e2a439f7b74f73`; parents `c15b7e7`+`a569f4b`; merged tree `4f1780ce` == accepted candidate tree) / POST-MERGE VERIFIED / AUTHORITATIVE; D-PSRR-01 is AUTHORITATIVE.** **PSRR EXECUTION: NOT STARTED** (no security scan / pen-test / config review / vendor selection performed; no production-readiness claim). **Trigger: before first public production deployment. Public Production: BLOCKED until PSRR = GO** (NO-GO/FAIL leaves the block; no inference from phase-complete / tests-green / security-baseline). Phase-7 §25 deferred security/ops items (Monitoring; broad Abuse Controls; `access_audit` retention; production secrets operations) remain **NOT delivered / NOT solved** — PSRR may reassess, not auto-implement. **Phases 8/9/10 remain NOT AUTHORIZED.** The **Phase-8 privacy/legal entry boundary is now clarified** (Owner decision **D-P8-PL-01**, governance-only): the §340 "privacy and legal prerequisites accepted" prerequisite means the bounded **entry-level design/architecture/legal-scope** rules (plans/subscriptions/entitlements/quotas/commercial-data model, provider-neutral commercial architecture, cancellation/refund **state-model interfaces**) are accepted before a Phase-8 contract proceeds — it does **NOT** require the final Phase-10 public legal artifacts (Privacy Policy, Terms, payment terms, refund policy, consent) merely to *define* the commercial model; **Phase 10 retains ownership** of those final public legal/commercial/security/operational-readiness artifacts. Building Phase-8 mechanics authorizes **no public paid activation** — public paid activation stays blocked until applicable Phase-10 legal/readiness + **PSRR = GO/PASS** + the governing separate Deployment Gate + explicit Owner deployment authorization. **OD-I/OD-N substance is unchanged** (persistence+accounts-before-activation; plan-neutrality). This clarification activates no Phase-10 work, no PSRR work, and no billing implementation; it is a candidate until independently reviewed, Owner-accepted, merged, and post-merge verified. The **Phase-8 Formal Contract & Acceptance Criteria (P8-C)** is now **DEFINED by a governance-only CONTRACT CANDIDATE** (dedicated contract `docs/governance/PHASE_8_SUBSCRIPTION_BILLING_ENTITLEMENTS_P8C_CONTRACT.md`; authoritative if/when independently reviewed, Owner-accepted, merged, and post-merge verified). It defines the canonical plan/subscription/entitlement architecture (hybrid entitlement: durable subscription-state + plan catalog, derived at evaluation via one Flask-free fail-closed `evaluate_entitlement` seam consuming the existing account foundation — D-FPC-MAP-06, no new registry/manager/adapter), the critical distinctions (security rate-limit ≠ commercial quota; API scope ≠ paid entitlement; plan access ≠ domain activation; subscription active ≠ production authorization; payment success ≠ technical progression; enterprise ≠ relaxed safety; billing audit ≠ security monitoring), the binding invariants (OD-I/OD-N/OD-O/D-P8-PL-01/OD-P/D-PSRR-01/OD-K; plan-neutral core; data preserved on entitlement decrease; fail-closed), provider neutrality (**no provider selected; no prices set**), the bounded increment decomposition (**P8-I1 Plan & Entitlement Foundation [recommended first, no payment provider]** → P8-I2 Usage Quotas → P8-I3 Subscription Lifecycle → P8-I4 Payment Provider Boundary → P8-CLOSE), acceptance criteria, and the Owner/business decisions REQUIRED (plan names, prices, trial/refund/grandfathering/enterprise/tax/provider-selection policies). **Phase 8 is CONTRACT CANDIDATE ONLY — NOT implementation-started, NOT billing-live, NOT paid-active; NOT AUTHORIZED.** No implementation begins until P8-C is independently reviewed, Owner-accepted, merged, post-merge verified, and a **separate P8 implementation authorization/gate** is granted. Public paid activation remains blocked until applicable Phase-10 legal/readiness + PSRR = GO/PASS + governing Deployment Gate + explicit Owner deployment authorization. **P8-C is now ACCEPTED / MERGED (PR #416, merge `5db47a2959507fa0cb8a4c717d32e617f23a08f0`; parent 2 = accepted candidate `1aed84a`; merged tree `d3ae4a5` == accepted candidate tree) / POST-MERGE VERIFIED.** The first Phase-8 increment **P8-I1 — Plan & Entitlement Foundation** is now **DEFINED by a governance-only BOUNDED IMPLEMENTATION-CONTRACT CANDIDATE (CORRECTED — verdict-B remediation)** (dedicated contract `docs/governance/PHASE_8_I1_PLAN_ENTITLEMENT_FOUNDATION_INCREMENT_CONTRACT.md`; supersedes prior candidate `2a4b65b`, evidence only; authoritative if/when independently reviewed, Owner-accepted, merged, post-merge verified). It bounds the smallest provider-neutral proof of **Account → Commercial Plan Identity → Entitlement Evaluation → Governed Capability Access** with NO payment provider/checkout/charges/invoices/tax/quota/lifecycle/proration/UI: a code-resident versioned plan catalog + additive durable `commercial_assignments` (plan-identity only) + minimal atomic-with-audit `commercial_audit` in the existing account-store schema lifecycle + one Flask-free fail-closed derived-entitlement seam (`evaluate_entitlement`; no stored snapshot; no `if plan==` branching) + one neutral internal governed-capability proof. It records an **explicit, bounded, Owner-acceptance-conditional REFINEMENT of P8-C** (catalog is code-resident versioned declarative data vs P8-C §18 DB-durable; P8-I1 assignment carries plan identity only — lifecycle states/period boundaries deferred to P8-I3; honest future schema-evolution path — no `ALTER TABLE` framework exists, so P8-I3 must separately choose an additive lifecycle table or a designed idempotent evolution mechanism) — **NOT a silent supersession**; the accepted P8-C history is preserved. **Backward-compatible:** valid active account with no commercial row = legitimate technical-default identity (NOT an error; default/free behavior preserved; derived not back-filled); unknown/malformed plan, catalog error, missing account, and disabled/deleted account all **fail closed** (missing account must NOT get the default identity); additive idempotent migration on existing+fresh DBs; rollback-safe; no `ALTER TABLE`. **OD-N** enforced by an **engine-wide inverted-allowlist static import guard** (no `engine/*.py` imports a commercial symbol except a minimal allowlist) + a behavioral guard (identical technical inputs under differing commercial identities → identical technical evaluation). Assignment mutation + its audit commit in ONE `BEGIN IMMEDIATE` transaction (no unaudited mutation). Credential revocation stays plan-independent; internal technical identifiers not exposed via public API/UI; security rate-limit ≠ commercial quota; API scope ≠ paid entitlement; plan entitlement ≠ domain activation; anti-lock-in (owner data preserved on future downgrade) carried forward. A genuinely-RED 15-test matrix is specified; full-suite verification mandatory for the implementation candidate. **No Owner/business decision blocks P8-I1** (plan names/prices/packaging/proration deferred, not invented). The corrected P8-I1-C contract is now **ACCEPTED / MERGED (PR #417, merge `29f3aebb93452015f2354e05f63a308c22726633`; parent 2 = accepted candidate `b14396b`; merged tree `7f36a13` == accepted contract tree) / POST-MERGE VERIFIED**, and P8-I1 is now **IMPLEMENTED as a governance-only IMPLEMENTATION CANDIDATE (RED → GREEN)** on the accepted contract: `engine/plan_catalog.py` (code-resident versioned declarative catalog; internal technical default `__default_technical__`; neutral internal proof capability — none exposed via public API/UI) + `engine/entitlement_service.py` (single Flask-free fail-closed `evaluate_entitlement` seam; derived-not-snapshot; fail-closed for unknown/malformed/catalog-error/missing/non-active account; valid active account with no assignment → technical default) + additive `engine/account_store.py` `commercial_assignments`/`commercial_audit` tables + `get_/set_commercial_assignment` (assignment+audit atomic in one `BEGIN IMMEDIATE`) + `tests/test_p8_i1_plan_entitlement_foundation.py`. Genuine RED first (ImportError: `plan_catalog` absent), then GREEN: **P8-I1 focused 17 passed; directly-impacted regressions 164 passed; full suite 2122 passed / 1 skipped / 1 xfailed / 0 failed** (2105 baseline + 17). OD-N proven behaviorally + by an engine-wide inverted-allowlist static import guard; credential revocation stays plan-independent; no payment/provider/checkout/quota/lifecycle/proration/UI; no domain activation; no public paid activation; no real user-facing paywall; changed paths exactly the REQUIRED allowlist (`engine/plan_catalog.py` + `engine/entitlement_service.py` + `engine/account_store.py` + the test). **P8-I1 — Plan & Entitlement Foundation is now IMPLEMENTED / INDEPENDENTLY REVIEWED / MERGED (PR #418, merge `2bf389ddaa16b6f92a9dd505e65987686f0531fa`; parent 2 = accepted impl `f55ce02`; merged tree `814d15d` == accepted impl tree) / POST-MERGE VERIFIED** (`engine/plan_catalog.py` + `engine/entitlement_service.py` + additive `engine/account_store.py` commercial tables + `tests/test_p8_i1_plan_entitlement_foundation.py`; full suite 2122 passed). The next increment **P8-I2 — Commercial Usage Quotas / Limits** is now **DEFINED by a governance-only BOUNDED IMPLEMENTATION-CONTRACT CANDIDATE** (dedicated contract `docs/governance/PHASE_8_I2_COMMERCIAL_USAGE_QUOTAS_INCREMENT_CONTRACT.md`; authoritative if/when independently reviewed, Owner-accepted, merged, post-merge verified). It bounds a provider-neutral usage-limit foundation: quota subject **(account_id, meter)** (the account principal — never browser session, never API credential); declarative **versioned quota policy in the P8-I1 catalog** (derived-at-evaluation, no per-account snapshot); a **smallest technical window** (lifetime or fixed-seconds; explicitly NOT final billing cadence — P8-I3 owns that); a new Flask-free fail-closed `engine/quota_service.py` seam (`consume_quota`/`evaluate_quota`) with **atomic evaluate-and-consume** in one `BEGIN IMMEDIATE` (no oversubscription of a hard cap); optional **idempotency key** (retry double-charge prevention); additive `commercial_usage` (canonical counter) + `commercial_usage_idempotency` tables; machine-level outcomes (`allowed`/`denied_not_entitled`/`denied_quota_exhausted`/`denied_invalid…`/`internal_fail_closed`). Binding separations: **security rate-limit ≠ commercial quota** (`record_rate_attempt` stays security-only; paid customers still rate-limited); **quota ≠ entitlement** (entitlement first, then quota); **API scope ≠ quota; credential ≠ quota subject; credential revocation plan/quota-independent**; **domain entitlement ≠ domain activation**. **HIGH-PRIORITY anti-lock-in:** commercial creation/consumption limits ≠ Owner data access/control — quotas never block reading/exporting/deleting existing Owner data; quota reduction below consumed usage is fail-safe/non-destructive. **OD-N:** engine-wide static import guard extended to `quota_service` + a commercial dynamic-import prohibition + behavioral guard; **no lower quality for free users**. No overage; no provider/lifecycle/proration; no pricing/usage UI; no public web/API surface; no public paid activation. A true prior-schema migration test convention is required; a genuinely-RED 21-test matrix is specified; **no Owner/business decision blocks P8-I2** (real quota values/cadence/packaging deferred, not invented). **The P8-I2-C contract is now **ACCEPTED / MERGED (PR #419, merge `d3e950cb5b34ee7fc0dd8522264fc412252236d3`; parent 2 = accepted candidate `1f42714`; merged tree `7c09f10` == accepted contract tree) / POST-MERGE VERIFIED**, and **P8-I2 — Commercial Usage Quotas / Limits is now IMPLEMENTED as a governance-only IMPLEMENTATION CANDIDATE (RED → GREEN; verdict-B CORRECTED replacement candidate — supersedes the invalidated prior candidate `1490548`, evidence only, NOT merged)**: a new Flask-free fail-closed `engine/quota_service.py` seam (`consume_quota`/`evaluate_quota` → `QuotaDecision`) reusing the P8-I1 entitlement seam (entitlement FIRST) + declarative versioned `quota_policy` in `engine/plan_catalog.py` (derived, no per-account snapshot) + additive `engine/account_store.py` `commercial_usage` (canonical counter) + `commercial_usage_idempotency` tables with atomic evaluate-and-consume in ONE `BEGIN IMMEDIATE` + `tests/test_p8_i2_commercial_quota.py` (P8-I1 engine-wide OD-N guard extended to the quota seam). **Verdict-B corrections applied: R1 — the read-only `evaluate_quota` no longer fails open at exhaustion (finite quota with `used >= limit`, including explicit zero-limit, now returns `denied_quota_exhausted`/`allowed=False`/`remaining=0`, no mutation; UNLIMITED unchanged); R2 — the `consume_quota` docstring now accurately describes fail-closed behavior + that `QuotaError` also arises from missing/invalid time for a fixed-window policy; plus two adjacent cleanups (lifetime `now=None` no longer persists the literal `"None"` timestamp; idempotency-key across-windows semantics documented — one logical consumption, keyed by (account,meter,key), no re-consume on later-window replay).** RED-first proof: the R1 discriminating tests FAIL against the invalid implementation (evaluate_quota allowed exhausted/zero-limit) and PASS after the fix. GREEN: **P8-I2 focused 32 passed; directly-impacted regressions 141 passed; full suite 2123 passed / 3 skipped / 1 xfailed / 0 failed (same-environment base 2091 + 32, no regression)**. Re-verified unchanged: security rate-limit ≠ commercial quota (`record_rate_attempt` untouched); entitlement ≠ quota; atomic hard-cap (no concurrent oversubscription); idempotency incl. same-key/different-amount conflict; anti-lock-in (existing Owner data read/export/account-delete when quota exhausted); OD-N behavioral + engine-wide static + dynamic-import guards; credential revocation plan/quota-independent; API scope unchanged; no domain activation; no public quota surface / no real paywall / no provider/payment/lifecycle/UI. Changed paths = the REQUIRED allowlist + the authorized guard extension. **P8-I2 — Commercial Usage Quotas / Limits is now IMPLEMENTED / INDEPENDENTLY REVIEWED (initial verdict B → corrected candidate re-reviewed A) / OWNER-ACCEPTED / MERGED (PR #420, merge `e3c65afcee1127d3dd75e4860ccb9480f7223f16`; parent 1 `d3e950cb5b34ee7fc0dd8522264fc412252236d3`; parent 2 = accepted corrected candidate `6f269acb2ebda129d220d0387693a659db48bd1a`; merged tree `65d1a660b61f975d5d9614452aeefc97f300212e` == accepted candidate tree) / POST-MERGE VERIFIED / FORMALLY ACCEPTED AND CLOSED** (increment closure only; dedicated record `docs/governance/P8_I2_COMMERCIAL_USAGE_QUOTAS_FORMAL_CLOSURE_RECORD.md`; DOCUMENTED NO-VALID-RED — governance/documentation-only closure after an already-tested merged implementation; closure authoritative if/when this governance candidate is merged). The invalidated prior candidate `1490548` (verdict B, fail-open `evaluate_quota`) remains EVIDENCE-ONLY / NOT MERGED. Post-merge evidence reproduced at `e3c65af`: P8-I2 focused 32 passed; full suite 2123 passed / 3 skipped / 1 xfailed / 0 failed. **Process-deviation recorded truthfully:** PR #420 was merged BEFORE the planned pre-merge safety check ran (the check did NOT occur; this record does NOT claim it did), mitigated by an expanded post-merge identity verification (exact parents, merged-tree == accepted-candidate-tree, exactly the changed paths, diffstat 897/−8, clean diff-check, post-merge tests green). **P8-I2 closure is an increment closure only — it does NOT close Phase 8, does NOT start P8-I3/P8-I4, does NOT enable public paid activation, and registers/executes no PSRR.** **The MANDATORY next governance gate is `G-MPR-01` — Master Phase & Roadmap Completeness Review (read-only) — REGISTERED / NOT YET EXECUTED; execution STOPS before P8-I3. P8-I3 — Subscription Lifecycle: NOT STARTED. P8-I4 — Payment Provider Boundary: NOT STARTED. P8-CLOSE: NOT STARTED. Phase 8 remains OPEN.** Preserved for G-MPR-01: the recurring `iot_electronics` domain-pack skipped-warning (`schema_version=None`; NOT fixed here) and the prior P8-I1 closure-record ambiguity (P8-I1 closed via current-truth/roadmap sync without a dedicated formal closure record). **G-MPR-01 (read-only master review) is now COMPLETE, and `G-MPR-01-D — Findings Disposition & Roadmap Registration` (governance-only; base `d37caef`) durably registers its accepted findings.** **P8-I1 — Plan & Entitlement Foundation is now FORMALLY CLOSED** via a dedicated late-registered closure record (`docs/governance/P8_I1_PLAN_ENTITLEMENT_FOUNDATION_FORMAL_CLOSURE_RECORD.md`; closure-record documentation gap only — NO implementation reopened; historical evidence cited: implemented RED→GREEN full suite 2122, merged PR #418 `2bf389d`, merged tree `814d15d` == accepted impl tree, post-merge verified; independent-review letter-verdict provenance disclosed per the PR #341 honesty precedent). **G-MPR-01-D dispositions D1–D10** registered (dedicated record `docs/governance/G_MPR_01_D_FINDINGS_DISPOSITION_AND_ROADMAP_REGISTRATION.md`; cross-registered in `OWNER_DECISION_REGISTER.md`): D2 P8-I3 additive/backward-compatible lifecycle-persistence rule (contract constraint only); D3 mandatory pre-Phase-9 **Core Domain-Neutrality Prerequisite Gate** (future; NOT before P8-I3); D4 future **Cross-Domain / Multi-Disciplinary Engineering Integration** gate (DOMAIN REFERENCE ≠ DOMAIN ACTIVATION ≠ CROSS-DOMAIN EVALUATION; ≥2 activated domains; re-homes the stale "deferred to Phase 6" pointer); D5 deferred-capability re-homing (QTA + Output-Language implementation = ADD live homes; ACV/PDF/Email = MOVE off closed Phase-3/4/5 anchors; all NOT AUTHORIZED); D6 CAP index range CAP-01…CAP-18; D7 real-vendor vs CAP-15 vs async/webhook vs export-adapters distinction; D8 `iot_electronics` legacy status registered + guarded (no deletion/migration/normalization/activation/repurposing without a separate gate; semantic disposition reserved to Owner); D9 OD-Q `main` reconciliation = mandatory future gate before production (NOT before P8-I3); D10 governance-hygiene scoped corrections. **`P8-I3 — Subscription Lifecycle` is ELIGIBLE FOR OWNER CONSIDERATION — NOT AUTHORIZED / NOT STARTED; Phase 8 OPEN; P8-I4/P8-CLOSE NOT STARTED; Phase 9/10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED; production / public paid activation BLOCKED.** Public paid activation remains blocked until applicable Phase-10 legal/readiness + PSRR = GO/PASS + governing Deployment Gate + explicit Owner deployment authorization. Public paid activation remains blocked until applicable Phase-10 legal/readiness + PSRR = GO/PASS + governing Deployment Gate + explicit Owner deployment authorization. Public paid activation remains blocked until applicable Phase-10 legal/readiness + PSRR = GO/PASS + governing Deployment Gate + explicit Owner deployment authorization. The mandatory §25 Phase-7 Remaining-Obligation / Exit-Criteria Review is now COMPLETE / AUTHORITATIVE (MERGED PR #411, post-merge verified) and **P7-CLOSE is COMPLETE — Phase 7 is FORMALLY CLOSED** (MERGED PR #412, merge `c15b7e7`, post-merge verified); **PSRR governance registration is now COMPLETE / AUTHORITATIVE** (MERGED PR #413, merge `6c0626e3ca659f90133a7df865e2a439f7b74f73`, post-merge verified). **Current active implementation: NONE; next development work is NOT automatically activated by this synchronization.** Public Production remains **BLOCKED until PSRR = GO/PASS + the governing separate deployment gate + explicit Owner deployment authorization**. **NOT authorized:** Phases 8/9/10, deployment/release, separately governed CAP-15…18 / AISR / QTA / ACV / WS17 / STG / PDF-Email / Output-Language, domain activation outside authorized Phase-7 scope, and any evidence-triggered Phase-7 capability before its accepted trigger is actually met. The next-eligible action is read from the live `ACTIVE_EXECUTION_ROADMAP.md` + Master Obligation Index + `OWNER_DECISION_REGISTER.md`.

**Immediately prior:** **P6-1 — Truthful Domain Labeling Foundation (Phase 6, Option A)** —
**IMPLEMENTED / INDEPENDENTLY REVIEWED (B — ACCEPT, zero blockers) / MERGED (PR #385, merge `a8b874be5c994687e02d64b6e84404b641ab501e`) / POST-MERGE VERIFIED / GOVERNANCE-SYNC MERGED (PR #386, merge `1a61ae5bca4b01b6c51be2c27c396016b676f2ee`) / FORMALLY ACCEPTED AND CLOSED (G-P6-1-TRUTHFUL-DOMAIN-LABELING-FORMAL-CLOSURE-01; dedicated record `docs/governance/P6_1_TRUTHFUL_DOMAIN_LABELING_FORMAL_CLOSURE_RECORD.md`).**
Implementation candidate `ddaf4357e91f3c1d9443135b903871fdb3bd554a` (parent `df9e6abc5e0fae1ff78c91bccfa88a2ccb34a27b`,
tree `c50d79110da61bd6d2ea5f2283660c0876b3853a`; 5 files / +259 / −2; central resolver `web/domain_label.py`). Per owner
decision **D-P6-16** (RESUME-01) a surface renders exactly ONE language variant — English and Arabic are never displayed
simultaneously; both EN and AR remain canonical in the resolver, and the current `<html lang="en">`/LTR session and
deliverable surfaces rendered the English variant only at P6-1 time (the Arabic variants were canonical but presently
unrendered because no global UI-language selector existed yet — that selector, **D-P6-18**, was then a FUTURE,
independently-authorized gate; it has SINCE been implemented and FORMALLY CLOSED (PR #388 `b47bf4b`), and the P6-1 labels
now follow the selected UI language). Originally defined (contract-of-record) by the documentation-only
contract-definition gate **G-P6-1-TRUTHFUL-DOMAIN-LABELING-FOUNDATION-CONTRACT-01** (authoritative base
`3703b4ff3a74ff735964e9f16be135f17834dc17`, Merge PR #380), on the owner-accepted Phase 6 discovery
**G-P6-DOMAIN-SPECIALIZATION-DISCOVERY-01** and owner decisions **D-P6-00 … D-P6-18**. The implementation gate
**G-P6-1-TRUTHFUL-DOMAIN-LABELING-FOUNDATION-IMPLEMENTATION-01** is COMPLETED and MERGED, and P6-1 is now **FORMALLY
ACCEPTED AND CLOSED**. There is **no active contract-of-record**; the next eligible owner gate is read from the live
`ACTIVE_EXECUTION_ROADMAP.md` and is **ELIGIBLE FOR OWNER CONSIDERATION, NOT AUTHORIZED** (Phase 6 as a whole is NOT
complete; no later Phase-6 increment is authorized or started by this closure). (The P6-1 CONTRACT-OF-RECORD body below is
retained as the definitional record.)

---

### P6-1 — Truthful Domain Labeling Foundation — CONTRACT-OF-RECORD (Phase 6, Option A; DEFINITION ONLY)

**Phase-6 naming (D-P6-00).** The authoritative Phase 6 lane for this execution is the `ACTIVE_EXECUTION_ROADMAP` lane —
**Domain Specialization / Truthful Specialist Labeling**. A separate registry-parity lane also historically called
"Phase 6" (`docs/GOVERNANCE_DOCUMENTS.md`, 23/23 parity) is a **distinct historical/registry-reconciliation track**;
`PRODUCT_ARCHITECTURE_AND_CREDIBILITY_ROADMAP.md` records that **neither lane authorizes the other**. This contract is
scoped to the execution lane only.

**Objective (D-P6-01, D-P6-09).** Give users truthful, human-readable information about the *limited* domain support
that actually exists, WITHOUT building a new domain engine, activating a new domain, changing deterministic behavior, or
overstating capability. Option A only: truthful labeling + truthful scope messaging + disclaimer preservation +
behavioral truthfulness tests. **No new deterministic domain rules.**

**Truthful user outcome (contract §4/§7).** Replace the raw internal identifier `electronics_electrical` on user-facing
domain/capability surfaces with a bounded **public Tier-1 label**:
- Internal id `electronics_electrical` → EN **"Electronics-informed review"**, AR **"مراجعة مستنيرة بمجال الإلكترونيات"**.
- Unknown / unsupported / missing / invalid domain → EN **"General idea review"**, AR **"مراجعة عامة للفكرة"**. The
  fallback MUST NOT silently label an unknown domain as electronics.
- State clearly the system provides **structured reasoning assistance, not professional specialist or licensed
  engineering review**; preserve truthful electronics-only scope; never imply `mechanical` / `medical_device` /
  `software` / `iot_electronics` are runtime-supported user domains. No new selection flow, dashboard, wizard,
  marketplace, multi-domain selector, or account-preference panel.

**Allowed label tiers (D-P6-02).** Tier 0 (General idea review) and Tier 1 (Domain-informed review) only. **Tier 2**
(domain-specific structured review) NOT authorized until a future increment proves real domain-specific
questions/rules/output/tests. **Tier 3 (Specialist) and Tier 4 (Licensed/professional) are PROHIBITED** under the
current product identity (`STRATEGIC_PRODUCT_VISION.md`: domain-agnostic reasoning-quality assessor, not an
implementation-readiness certifier).

**Exact technical capability (contract §5; DEFINITION — authorizes the future implementation to do ONLY):** (1) a
bounded central **public-domain-label map/policy** for the active runtime domain; (2) render that public label on the
current user-facing domain/capability surfaces; (3) truthful scope + disclaimer wording; (4) a **runtime-backed
truthfulness invariant** proving public-label ↔ actual runtime-operated domain capability; (5) **replace/supplement the
source-grep-only** runtime-integration evidence with BEHAVIORAL evidence; (6) tests preventing unsupported
Tier-2/3/4 labels; (7) bilingual EN/AR; (8) preserve accessibility + RTL/LTR. The label map MUST NOT itself activate a
domain and MUST be resolved **server-side from durable/validated runtime state** (`confirmed_domain` / validated
`state.domain`), **never from arbitrary client input**.

**Domain selection & scope (D-P6-03/04/05/06/07/11).** Preserve the current electronics confirmation gate unchanged; add
no recommendation, AI inference, confidence scoring, or multi-domain UX. The only runtime-operated domain remains
`electronics_electrical`. Low-confidence/unsupported → General/Uncertain, never a specialist label. Multi-domain NOT
supported. High-risk domains (medical, regulated, structural) remain unsupported/restricted and MUST NOT be activated or
labeled as specialized.

**Deterministic vs AI responsibility (D-P6-09; contract §14).** Presentation/labeling only. **No** change to deterministic
evaluation, gap selection, scoring, question generation, reconstruction, or the substance-signal logic. **No** AI,
model, provider, agent, or prompt change.

**Data model / migration (D-P6-10; contract §15).** Schema change NONE; migration NONE. `confirmed_domain` and
`domain_signal` unchanged. Do NOT add confidence, secondary-domain, label-history, provenance, or override fields
(future multi-domain increment).

**Claims policy (D-P6-12; contract §8).** Preserve the existing non-professional-advice / non-certification boundaries
and the deliverable forbidden-words guard. Prohibited public wording (unless a future separately-authorized capability
truly supports it): "Electronics Specialist", "Engineering Specialist Review", "Expert Review", "Professional Review",
"Certified Review", "Approved", "Feasible", "Safe to build", "Ready for implementation".

**Permitted implementation paths (contract §13 — the future gate may touch ONLY, and only those proven necessary by an
exact inventory):** one small public-domain-label helper/module; `web/app.py` (server-side label resolution/context
only); the current session/review/deliverable templates that today expose a raw domain/pack-id
(`web/templates/session.html`, the deliverable/review-snapshot template, entry-page domain wording, and a user-facing
export field ONLY if it exposes a raw pack id and truthfulness requires it); focused Phase-6 truthful-label tests; the
existing domain-gate / registry test files ONLY where required for behavioral proof; `tests/conftest.py` only if
necessary. The implementation contract MUST list exact file paths, not directories.

**Prohibited implementation paths (contract §14 — the future gate must NOT change):** `domains/*.json`;
`engine/domain_registry.py`; `engine/domain_rules.py`; `engine/progression_loop.py`; `engine/scoring.py`;
`engine/idea_state.py`; `engine/record_contract.py`; `engine/session_reconstruction.py`; `engine/path_n_questions.py`;
`engine/safety_signal.py`; `engine/requirement_landscape.py`; `engine/idea_development_outputs.py`; schemas; migrations;
dependencies; CI/deployment; prompts; provider adapters; agents/models. If an exact inventory proves a prohibited path
is genuinely necessary, the implementation gate MUST STOP and return to the owner rather than silently broaden scope.

**RED-first plan (contract §10).** Genuine RED on the exact live parent before GREEN:
- **RED-01** a user-facing surface exposes the raw internal pack id / inconsistent raw domain wording (evidence today:
  `web/templates/session.html` "Domain: {{ state.domain or 'electronics' }}"; the deliverable snapshot renders
  `Capability: {{ cap.capability_id }}` = the raw `electronics_electrical` pack id).
- **RED-02** no central enforced public-label tier policy exists.
- **RED-03** no behavioral test binds the public label to runtime-operated capability.
- **RED-04** the existing source-grep runtime-integration test (`tests/test_domain_registry.py::TestRuntimeIntegration`)
  can stay green even if runtime behavior is disconnected.
- **RED-05** no test prevents unsupported specialist/expert/professional labels being introduced.
- **RED-06** unknown/invalid domain label fallback is not behaviorally proved.
- **RED-07** bilingual public labels are not behaviorally proved.
For each RED test record: exact failure; why it is a real missing behavior; why it cannot false-green; expected GREEN;
exact path.

**GREEN plan (contract §11).** internal pack id not shown on user-facing surfaces; Tier-1 label renders (EN+AR);
fallback = General idea review / مراجعة عامة للفكرة; Tier-2/3/4 rejected/absent; disclaimer visible+truthful; no new
domain activated; existing electronics flow functional; unknown/invalid domain does not overclaim; current domain-gate
tests green; registry tests green; full suite green.

**Runtime truthfulness test (contract §9).** A genuine BEHAVIORAL test (NOT source grep / file existence / import /
string-presence): a real user session enters via the electronics gate → receives the validated electronics runtime
domain → reaches a current user-facing review/session surface → sees the Tier-1 public label → does NOT see the raw
pack id → does NOT see Tier-2/3/4 language → receives the safe fallback when domain state is missing/invalid. The exact
mechanism is defined from live repository evidence in the implementation gate.

**Independent review (contract §12).** A/B requires: no overclaim; no raw internal identifier leakage on current
user-facing surfaces; behavioral runtime-label proof; truthful fallback; disclaimer preservation; no new domain
activation; no deterministic-engine change; no schema change; no AI/model/agent change; no material false-green. **C is
mandatory** if: Tier-2/3/4 shown without supporting capability; unsupported domains appear active; label derives from
client input; unknown domain silently becomes electronics; runtime truthfulness proved only by source grep; disclaimers
weakened; deterministic evaluation changed; a new domain activated; or scope expands into registry hardening or
multi-domain work.

**Rollback (contract §16).** Revert the bounded label/helper/template/test commit; no DB rollback; no domain-pack
rollback; no project-data rewrite; no account/ownership effect; no output-contract change beyond user-facing
presentation.

**Observability (contract §17).** No analytics/external telemetry. Permitted evidence: deterministic tests,
rendered-template assertions, existing app logs without raw project/domain content. Do NOT log project text, raw tokens,
unnecessary account ids, or client-provided domain values as trusted labels.

**Registry hardening (D-P6-14).** The deferred Domain Registry validation gaps (version-format, date-field, allowed
status values, classification/substance signal completeness, gap_type_mappings completeness+element types, rule_nuances
completeness+element types, provenance/governance metadata, pack-id collision detection, alias resolution) remain a
**SEPARATE bounded increment and a prerequisite before any new domain activation** — NOT fixed in this contract gate or
in the first labeling implementation.

**Explicit deferrals (D-P6-15).** new domain activation; multi-domain orchestration; AI-assisted domain recommendation;
model/provider routing; new agents; new prompts; new output types; deterministic domain-rule activation; registry
hardening; post-output refinement; WS17 AI Coach; STG; ACV; PDF/download; output email delivery; production email
provider.

**Lean justification (contract §18).** Option A is the minimum safe next increment: current specialization is thin (only
`electronics_electrical` is runtime-operated; `rule_nuances` dead, `gap_type_mappings` inert in the shipped flow);
product identity forbids professional-specialist claims; raw/internal labels need truthful public mapping; behavioral
truthfulness evidence is missing; no new engine or schema is necessary; the increment is independently reviewable and
reversible. Do not broaden it to make Phase 6 look more substantial.

**Completion criteria (contract §19).** Complete only when: paths stay within contract; RED genuine; GREEN focused
tests pass; domain-gate tests pass; registry tests pass; UX/accessibility tests pass; full suite passes; no raw
active-domain pack id on current user-facing surfaces; Tier-1 label + fallback truthful; no Tier-2/3/4 overclaim;
disclaimers intact; no new domain active; no schema/engine/AI change; independent review A/B with no blockers;
bundle/commit/tree/parent/round-trip evidence passes.

**Stop conditions (contract §20).** Stop and return to the owner if truthful labeling requires modifying deterministic
engine behavior or domain packs; the user-facing output contract cannot be changed safely; a new domain must be
activated; multi-domain selection becomes necessary; a schema change becomes necessary; a material conflict appears
between the two Phase 6 numbering tracks; product-identity documents contradict the proposed labels; or scope cannot
remain bounded and Lean.

**Merge authority.** Owner, separately. **Independent-review scope:** the reviewer questions in "Independent review"
above. **This is a contract of record only — it authorizes no code, test, schema, dependency, CI, push, PR, merge, or
implementation.**

---

**Immediately prior status.** **THERE IS NO ACTIVE OPEN IMPLEMENTATION CONTRACT. PHASE 5 — Accounts / Authentication /
Ownership / Verified Email is FORMALLY CLOSED** across all three increments (**P5-1 → P5-2 → P5-3**), each IMPLEMENTED /
INDEPENDENTLY REVIEWED (verdict **B**, PUBLISH) / MERGED / POST-MERGE VERIFIED / OWNER ACCEPTED / FORMALLY CLOSED. Final
closure is recorded by **G-P5-FINAL-CLOSURE-SYNC-01** (authoritative base `d9f888bd0def7b3275cd04860dfa2e8cc1504111`,
Merge PR #379, tree `e6a03ab46d6d01ca4b95ee87d240ce6658eeb47c`). The most recently completed increment is **P5-3 —
Project Ownership and Route Authorization** (gate **G-P5-3-PROJECT-OWNERSHIP-ROUTE-AUTHORIZATION-IMPLEMENTATION-01**;
candidate `a0997c3`, tree `e6a03ab`, parent `b14c931`; merged via **PR #379** `d9f888b`, ancestry PASS; scope **6 files /
+562 / −15**; disallowed paths **NONE**; source branch `feat/p5-3-project-ownership-authorization` PRESERVED; focused
**19 passed**, full suite **1893 passed, 1 skipped, 1 xfailed**). **Delivered by P5-3:** additive nullable
`projects.owner_account_id` (indexed, idempotent legacy-safe migration); atomic verified-account owned-project creation
(ownership immutable, no transfer); one central fail-closed server-side route-authorization helper (ownership from
durable state + the validated session, never the `sid`/cookie/client) enforced on every protected `/session/<sid>`
GET/POST route; cross-account + anonymous denial for owned projects; generic missing/not-authorized equivalence;
disabled/deleted denial; owner-scoped project list; Draft L2 account+project isolation. **Does NOT implement** anonymous
project claim, ownership transfer, multiple owners, collaboration/sharing/teams/organizations, Draft Level 3, writable
continuation, output email delivery, ACV, AI Coach, or STG. **Preserved observations:** **OBS-P5-3-01** (replace the
`sid in SESSION_STORE` in-memory authorization fallback with caller/session-scoped authorization before any
project-deletion / broader in-memory access / session-restoration expansion); **OBS-P5-2-01** / **OBS-P5-2-02** (P5-2
email-link-tokens-in-URL and reset-atomicity, preserved). **NEXT ELIGIBLE GATE (owner consideration only — NOT started,
NOT authorized):** **Phase 6 — domain specialization / truthful specialist labeling** per the authoritative roadmap phase
map (the roadmap does NOT designate Phase 6 as "Post-Output Refinement Orchestration"). **Draft Level 3, writable
continuation, output email delivery, and every FPC remain NOT AUTHORIZED / NOT STARTED.** Decision **D17** and the AISR
seven-owner model are preserved.

The **immediately prior** contract-of-record was **P5-2 — Authenticated Sessions, Verified Email & Account Recovery
(Phase 5, Option A)**, now **IMPLEMENTED, INDEPENDENTLY REVIEWED, MERGED, POST-MERGE VERIFIED, OWNER ACCEPTED, AND
FORMALLY
CLOSED** (independent review **G-P5-2-AUTH-SESSIONS-VERIFIED-EMAIL-RECOVERY-INDEPENDENT-REVIEW-01**, verdict **B — ACCEPT
WITH NON-BLOCKING OBSERVATIONS**, PUBLISH). Gate **G-P5-2-AUTH-SESSIONS-VERIFIED-EMAIL-RECOVERY-IMPLEMENTATION-01**;
candidate `87c85c7` (tree `375db689`, parent `f84c87d`); merged via **PR #377** (merge commit
`402727a557edd7dbea3e92f477bf9cbefe74ea3e`, two-parent merge of `f84c87dc190b431ecb258b03aea699045d68a945` (base) +
`87c85c7bb2b2c41e4510377eac9ce0133061f61e` (reviewed candidate), tree `375db6895748d101905b44ca8e622128acb3f51b`, equal
to the candidate tree; ancestry PASS). Merged scope **13 files / +1712 / −78**; disallowed paths **NONE** (no
deterministic engine file, no `engine/record_store.py`, no `projects.owner_account_id`, no production
`requirements.txt`); source branch `feat/p5-2-auth-sessions-verification-recovery` PRESERVED. Focused **40 passed**; full
suite **1874 passed, 1 skipped, 1 xfailed**. The two mandatory P5-1-closure preconditions were satisfied first —
**P5-2-PRE-01** (rate-limit concurrency: `BEGIN IMMEDIATE` read-modify-write proven race-free under real concurrent
threads + bounded expired-row cleanup) and **P5-2-PRE-02** (SQLite thread strategy: one connection
`check_same_thread=False` + re-entrant lock + immediate transactions, proven under real multi-thread tests; not a bare
`check_same_thread` override). **Delivered:** login/logout; logout-all via `session_epoch`; a signed-cookie authenticated
session distinct from the project `sid`; idle 2h / absolute 14d expiry; session rotation on login; CSRF on authenticated
mutations; email-verification completion + resend; recovery request + password-reset completion (reset revokes all
sessions, no auto sign-in); disabled/deleted denial; generic non-enumerating responses; Draft L2 account-switch
isolation; bilingual accessible UX. **Does NOT implement** `projects.owner_account_id`, project ownership, project route
authorization, anonymous project claim, collaboration/sharing, P5-3, Draft Level 3, writable continuation, output email
delivery, or a production email provider. **Preserved non-blocking observations:** **OBS-P5-2-01** email-link raw tokens
in URL paths (hash-only, single-use, short expiry, not app-logged; revisit before production email/reverse-proxy) and
**OBS-P5-2-02** password-reset sequential-transaction atomicity (accepted resilience debt; evaluate one atomic operation
when `account_store` is next touched for a related security increment). **NEXT ELIGIBLE INCREMENT: P5-3 — Project
Ownership and Route Authorization**, authorized under the continuing Phase 5 owner authorization **only after this
closure sync is merged and post-merge verified**. **Draft Level 3, writable continuation, output email delivery, and
every FPC remain NOT AUTHORIZED / NOT STARTED.**

The **immediately prior** contract-of-record was **P5-1 — Account & Credential Foundation (Phase 5, Option A)**,
**IMPLEMENTED, INDEPENDENTLY REVIEWED, MERGED, POST-MERGE VERIFIED, OWNER ACCEPTED, AND FORMALLY CLOSED** (verdict
**B**, PUBLISH). Gate **G-P5-1-ACCOUNT-CREDENTIAL-FOUNDATION-IMPLEMENTATION-01**; candidate `6be86f5` (tree
`128b2d4`, parent `e84526d`); merged via **PR #375** (merge commit
`65a2c0e258bf9635921046ad27f8a886cce78218`, two-parent merge of `e84526d36e8518bea75da109c77f0851c0acf5c2` (base) +
`6be86f5853d84216d2bd0792c4ca98babadbfe31` (reviewed candidate), tree `128b2d415ace8a5fee2c0cff4c84aeeb28bcf5e6`, equal
to the candidate tree; ancestry PASS). Merged scope **7 files / +1024** (`engine/account_credentials.py`,
`engine/account_store.py`, `engine/email_sender.py`, `web/app.py`, `web/templates/register.html`,
`tests/test_p5_1_account_credential_foundation.py`, `tests/conftest.py`); disallowed paths **NONE**; source branch
`feat/p5-1-account-credential-foundation` PRESERVED. Focused **35 passed**; full suite **1834 passed, 1 skipped, 1
xfailed**. **Delivered (foundation only):** additive `accounts` persistence; immutable UUID `account_id` (never email);
normalized + unique email; Werkzeug **scrypt** hashing; active/disabled/deleted status; `session_epoch` foundation;
registration route + bilingual accessible form; generic non-enumerating response; verification-token **hash-only**
persistence with **24h** expiry and supersession; development `EmailSender` abstraction + memory sink; bounded
store-backed rate-limit foundation; additive idempotent legacy-safe migration; **no plaintext password** and **no raw
verification-token** storage or logging. **Does NOT implement** login/logout, authenticated Flask sessions,
authentication cookies, CSRF for authenticated mutations, verification completion, resend, password recovery/reset,
project ownership, `projects.owner_account_id`, route authorization, anonymous project claim, Draft Level 3, P5-3, output
email delivery, or a production email provider; registration does **not** sign in, create a project, or establish
ownership. **Mandatory P5-2 preconditions (binding, engineering):** **P5-2-PRE-01 rate-limit concurrency hardening** and
**P5-2-PRE-02 SQLite thread/connection strategy** — both must be addressed within the first P5-2 implementation
candidate before login/session security is accepted (full text in the §"Phase 5 increments" / roadmap P5-1 closure
entry and `OWNER_DECISION_REGISTER.md`). **NEXT ELIGIBLE INCREMENT: P5-2 — Authenticated Sessions, Verified Email, and
Recovery**, authorized under the continuing Phase 5 owner authorization **only after this closure sync is merged and
post-merge verified**. **P5-3: NOT STARTED. Draft Level 3, writable continuation, output email delivery, and every FPC
remain NOT AUTHORIZED / NOT STARTED.**

The **immediately prior** contract-of-record was **P4-2 Level-1 — Deterministic Read-Only Reconstruction of Review State
(OPTION A)**,
now **IMPLEMENTED, MERGED, POST-MERGE VERIFIED, OWNER ACCEPTED, AND FORMALLY CLOSED** (owner verdict
**B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**). Merged via **PR #369** (merge commit
`276e89681e6008ec859383771b845833321b5552`, two-parent merge of `2cde5868249f5e2b135b13fb33adff5dd5e4a816` (base) +
`e66ae3a7d95994b32dd590000b1bd1e95c499c64` (reviewed candidate), tree `1f6babf08ca6aae04677739d6c945581ed90db56`,
equal to the candidate tree; candidate ancestry PASS). **Delivered (Option A / Level 1):**
`engine.session_reconstruction.reconstruct_review_state(store, sid)` — a deterministic, **read-only** reconstruction for
a durably recorded **Path-N** session. It additively persists the reconstruction inputs (`seed_idea_text`,
`confirmed_domain`, `recon_path`, `engine_contract_version`) at project creation, loads accepted-answer evidence in
authoritative `seq` order, builds a **fresh** canonical `IdeaState`, replays the seed then answer contents through the
**unchanged** `progression_loop.run_iteration`, and returns an **immutable** `ReconstructedReviewState`. Version
`p4-2-level1-recon-v1`; replay limit **500**. Legacy / missing-metadata / unsupported-path / version-mismatch fail
closed to Level-0 evidence (no AI, no network); malformed history raises the canonical `ContractError`; **no DB /
`SESSION_STORE` mutation, no UI, no session resume, no writable continuation, no prior-output validity claim.** Merged
scope **4 files / +795 / −13** (`engine/record_store.py`, `engine/session_reconstruction.py`, `web/app.py`,
`tests/test_p4_2_session_reconstruction.py`); disallowed paths **NONE**. **P4-2 Level-1 is no longer a candidate,
pending review, pending publication, not-authorized, or not-started. PHASE 4 (Durable Data and Evidence Foundation) is
FORMALLY CLOSED within its implemented boundary** (P4-0 → P4-1a → P4-1b-1 → P4-1b-2a → P4-1b-2b → P4-2 Level-1);
**Draft Level 2 — Same-Device Unsubmitted-Text Recovery is FORMALLY CLOSED (PR #372).** **Phase 5 — Accounts /
Authentication / Ownership / Verified Email Foundations is now FORMALLY PLANNED (Option A; P5-1 → P5-2 → P5-3) under the
formal contract-of-record recorded below (gate G-P5-FORMAL-CONTRACT-AND-CONTINUING-AUTHORIZATION-01); NO Phase 5
implementation is active. P5-1 becomes the next eligible implementation gate only after this formal contract is merged
and post-merge verified.** Draft Level 3, writable continuation, output email delivery, and every FPC remain NOT
AUTHORIZED / NOT STARTED.**

The **immediately prior** contract-of-record **P4-1b-2b — Read-Only Accepted-Answer Evidence Reconstruction (OPTION A)**
remains **IMPLEMENTED, MERGED, POST-MERGE VERIFIED, OWNER ACCEPTED, AND FORMALLY CLOSED** (owner verdict
**B — ACCEPT WITH BINDING CONTRACT REFINEMENTS**, refinements satisfied). Merged via **PR #367** (merge commit
`1c9dff7962a428cfd32ab577dbbbb84ce21909b3`, two-parent merge of `7d8895122235a4da25a7f4d9d0d4d5e4bab20c6b` (base) +
`945f4a36a6a6eef5bcab1ea55e30ce1dfa468820` (reviewed candidate), tree `bff45ada35e8d3bb606bcf4e6bd80e3df33d449d`,
equal to the candidate tree; candidate ancestry PASS). **Delivered (Option A):** a bounded, **read-only**
`SqliteRecordStore.load_accepted_answer_evidence(sid)` returning an **immutable `tuple`** of the `answered`-disposition
`AssertionRecord`s in persisted (`seq`) order via the project-scoped `load_contract`; `record_id` preserved as `rec_N`;
unknown `sid` → `()`; corruption → canonical `ContractError` (fail closed); no mutation, no runtime/UI/route, no session
resume, and **not** full deterministic replay (P4-2). Merged scope **2 files / +367 / −0** (`engine/record_store.py`,
`tests/test_p4_1b2b_accepted_answer_evidence.py`); disallowed paths **NONE**. **P4-1b-2b is no longer a candidate,
pending review, pending publication, not-authorized, or not-started.** The **immediately prior** contract-of-record
**P4-1b-2a — Durable Answered-Event Append and Web-Layer Idempotency** remains **IMPLEMENTED / MERGED / VERIFIED /
ACCEPTED / CLOSED** (owner verdict **B**; PR #365, merge `77bd10cc55a731b18d4e35ea262b55342a9f847f`, tree `c8808be`;
`record_id` = `rec_N`; separate durable idempotency identity; no deterministic-output engine changed). **There is NO
active open implementation contract. Phase 4 is FORMALLY CLOSED; writable continuation, Phase 5, and every FPC remain
NOT AUTHORIZED / NOT STARTED.** The most recently completed increment is **Draft Level 2 — Same-Device Unsubmitted-Text
Recovery (Local Draft Recovery)**, now **IMPLEMENTED / REMEDIATED / INDEPENDENTLY REVIEWED / MERGED / POST-MERGE VERIFIED
/ OWNER ACCEPTED / FORMALLY CLOSED** (re-review verdict **B**; contract PR #371 → implementation **PR #372**, merge
`43223dd6ab6ad169eefd64e37dee211f8bc306b9`, tree `83dbf367d0754d1b59f53ba85db0867672c3f543`; local-only, same-device;
blockers **B1/B2/B3 fixed**; no engine/schema/account/server-draft change). The Draft Level 2 increment-contract section
retained below is a **fulfilled contract-of-record** (its "CONTRACT CANDIDATE / IMPLEMENTATION NOT AUTHORIZED / NOT
STARTED" wording is **superseded** by this status). **Phase 5 — Accounts / Authentication / Ownership / Verified Email
— DISCOVERY IS COMPLETE / ACCEPTED (verdict B) and the FORMAL Phase 5 CONTRACT is now recorded below (Option A; P5-1 →
P5-2 → P5-3; gate G-P5-FORMAL-CONTRACT-AND-CONTINUING-AUTHORIZATION-01). NEXT ELIGIBLE GATE: P5-1 — Account & Credential
Foundation, which becomes eligible only after this formal contract is merged and post-merge verified. Phase 5
implementation is NOT active in this gate.** (Documentation note: the historical "P4-1b-2a … REV1" and "Contract Amendment" sections
retained below, and any statement anywhere below that "P4-2 … / P4-1b-2b … remain NOT AUTHORIZED / NOT STARTED", were
accurate as of their PR #365/#367 boundary and are **superseded** by this status for current truth. **Further superseded
(P5-1 boundary):** this rolling narrative and the Phase 5 formal-contract section below predate the P5-1 merge; every
forward-looking phrase such as "NEXT ELIGIBLE GATE: P5-1", "P5-1 becomes the next eligible implementation gate", or
"Phase 5 … remain NOT AUTHORIZED / NOT STARTED" was accurate as of the PR #374 formal-contract boundary and is
**superseded by the leading "Status (current)" block**. **Further superseded (P5-2 boundary):** this rolling narrative
and every forward-looking phrase below such as "NEXT ELIGIBLE INCREMENT: P5-2", "P5-2 is the next eligible increment", or
"P5-3: NOT STARTED" was accurate as of the PR #375/#376 boundary and is superseded by the leading "Status (current)"
block. **Further superseded (Phase 5 final closure):** every forward-looking phrase anywhere below such as "P5-3 is the
next eligible increment", "P5-3 — Project Ownership and Route Authorization — is the next eligible increment", or "Draft
Level 3 … NOT AUTHORIZED / NOT STARTED" that treats P5-3 as pending is superseded by the leading "Status (current)"
block: **P5-1, P5-2, and P5-3 are ALL IMPLEMENTED / MERGED (PR #375, PR #377, PR #379) / FORMALLY CLOSED, PHASE 5 is
FORMALLY CLOSED, and the next eligible gate — for owner consideration only, NOT started / NOT authorized — is Phase 6
(domain specialization / truthful specialist labeling) per the authoritative roadmap phase map.**)

**Review lineage (HISTORICAL — for the record).** DOC-01 candidate `0e2a5cec24d71462eadbffa193e3467d40d506a0` carried
verdict `C — REVISE AND RE-REVIEW` (preserved, unmerged); a separately-claimed
`518cfdfe0eca3fb0f52c88c5baea46c643d3c288` candidate/bundle is **NOT** an established repository artifact and must not be
relied upon. The B3 finding that a token-derived `evt-*` id would change deterministic output — historically stated as
"CONTRACT AMENDMENT / OWNER DECISION REQUIRED" — was **resolved by selecting Option A** (that requirement is no longer
outstanding). The implementation candidate `b1eb91e6fb1b3cd60637e0808c9976c408cc090a` (verdict `C`, four blocking
findings) was superseded by REV1 `0b5f7577371e196e2f7e453afc720ca168544188` (verdict `B`, all four verified closed), which
is the merged implementation. The "P4-1b-2a Increment Contract Candidate — REV1" and "P4-1b-2a Contract Amendment"
sections below are retained as **HISTORICAL PRE-IMPLEMENTATION CONTRACT STATE**, not the current status.

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

## Draft Level 2 — Same-Device Unsubmitted-Text Recovery — Increment Contract (G-DRAFT-L2-LOCAL-CONTINUITY-CONTRACT-01) — FULFILLED CONTRACT-OF-RECORD (IMPLEMENTED / REMEDIATED / MERGED / FORMALLY CLOSED via PR #372)

> **[CLOSURE STATUS — G-DRAFT-L2-CLOSURE-SYNC-01.]** This contract is **FULFILLED**: Draft Level 2 is **IMPLEMENTED,
> REMEDIATED, INDEPENDENTLY REVIEWED, MERGED, POST-MERGE VERIFIED, OWNER ACCEPTED, AND FORMALLY CLOSED** — original impl
> candidate `9138f96` (independent review **C — REJECT**, blockers **B1/B2/B3**) → remediation candidate `4696567`
> (re-review **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**, PUBLISH) → **PR #372**, merge
> `43223dd6ab6ad169eefd64e37dee211f8bc306b9`, tree `83dbf367d0754d1b59f53ba85db0867672c3f543`. Merged scope **8 files /
> +981 / −6**; disallowed paths **NONE**; **B1/B2/B3 fixed**; focused **30 passed**, full suite **1799 passed, 1 skipped,
> 1 xfailed**. The candidate/contract text below is preserved as the fulfilled contract-of-record; its
> "CONTRACT CANDIDATE / IMPLEMENTATION NOT AUTHORIZED / NOT STARTED" wording is **superseded**. See
> `ACTIVE_EXECUTION_ROADMAP.md` and `OWNER_DECISION_REGISTER.md` (`D-DRAFT-L2-IMPL-01…07`). **NEXT ELIGIBLE GATE: Phase 5
> — Accounts / Authentication / Ownership / Verified Email — DISCOVERY AND CONTRACT DEFINITION (implementation NOT
> authorized).**

**Status (HISTORICAL — as written at the contract gate; SUPERSEDED by the closure status above):**
`CONTRACT CANDIDATE ONLY — IMPLEMENTATION NOT AUTHORIZED — DRAFT LEVEL 2 NOT STARTED`. Recording this
candidate grants **no** implementation, client-JavaScript, `localStorage`/IndexedDB, template, `web/app.py`, schema,
migration, dependency, account, or Phase 5 authority. Implementation requires a **separate explicit owner
authorization** after this candidate is independently reviewed and accepted. Follows the accepted discovery
**G-P5-DISCOVERY-AND-DRAFT-CONTINUITY-ASSESSMENT-01** (overlap **D — NOT FOUND**; current **Draft Level 0**; selected
**Option B**). Sequence of record: **Draft Level 2 (this) → Phase 5 identity foundation → Draft Level 3 (server,
account-linked)**.

**Canonical capability name:** **Same-Device Unsubmitted-Text Recovery** (short label: **Local Draft Recovery**). The
term "autosave" is avoided standalone to prevent confusion with the existing, still-binding prohibition against
automatically **authoring / rewriting / accepting / submitting** user answers (GUIDED_ANSWER_COAUTHORING; Guided
Uncertainty Support scope decision, PR #132). This capability stores a **literal copy of text the user typed** and does
**NOT** write on the user's behalf, rewrite text, accept or submit an answer, create an `AssertionRecord`, run
deterministic evaluation, close a gap, change maturity, or generate/alter outputs.

### 1. Objective & truthful user outcome
Protect unfinished user-entered text on the **same supported browser/device** against power/battery loss, tab/browser
closure, refresh, browser crash, temporary internet loss, and intentional pause — so the user can **explicitly** recover
the latest locally saved version on return. It is **local-only**: it does **NOT** provide cross-device recovery, server
persistence, accounts, writable continuation, or any change to accepted-answer semantics. It must **never** claim
recovery when browser storage is unavailable, data was cleared, private mode removed it, the user moved to another
device/browser, the draft expired, the context no longer matches, or the user explicitly discarded it.

### 2. First-increment surface scope (§6)
- **REQUIRED:** (1) **seed idea** input (`web/templates/index.html`, `textarea#idea`); (2) **main answer** input
  (`web/templates/session.html` `textarea#response`, the answered form). Highest data-loss + user-value.
- **CONDITIONAL (adopt only if the same primitive covers it at trivial cost):** the **criticality-correction free-text**
  textarea (`session.html`, the no-`action` answered-producing correction form).
- **DEFERRED:** the criticality **clarify rationale** (server-prefilled), **success-criteria** textareas.
- **PROHIBITED (this increment):** the **FDC-001 Decision Workspace** inputs (`decision_workspace.html`) and any
  legacy/unlinked surface — separate lane, in-memory, out of the minimum coherent experience.

### 3. Local storage decision (§7)
- **Selected mechanism: `localStorage`.** Minimum-Lean: synchronous simple key/value API, no schema, ubiquitous support;
  drafts are small text well under the ~5 MB origin quota. IndexedDB (async, heavier) is unnecessary for a few small
  text drafts; **no** service worker, offline app shell, or third-party library.
- **Per-draft size cap:** bounded (recommend **64 KB** per draft; oversized input is not stored — truthful "could not
  save" status, submission still allowed). **Failure/private-mode/quota:** wrap every access in try/catch; any failure
  **fails closed to Level 0** with a truthful *"Could not save a draft on this device"* and never blocks typing or
  submission. **Compatibility:** all supported evergreen browsers; unsupported/JS-disabled → Level 0.
- **No client-side encryption is claimed** (a client-held key adds no real protection); protection is by **disclosure +
  TTL + cleanup + explicit-restore**, not cryptography.

### 4. Draft identity contract (§8)
Local key (raw invention text is **never** part of the key):
`inventorai:draft:v1:<scope>:<field>:<context-id>:<context-version>` where
`v1` = draft-schema version; `<scope>` = the temporary-session/project `sid` for session surfaces, or the reserved
`__seed__` for the pre-submission seed-idea form (no `sid` yet); `<field>` = surface type (`idea` | `answer` |
`correction`); `<context-id>` = the current question/step identity where applicable; `<context-version>` = a
content/engine/question-context version stamp so a **stale** question/idea never restores. Before a stable `sid` exists
(seed-idea form), a single per-browser `__seed__` draft is used and is cleared once `/start` is confirmed accepted. **No
account ownership** is introduced.

### 5. Save behavior (§9)
Debounced save (**recommend ~800 ms** idle) on input, **plus** a flush on `pagehide` and on `visibilitychange`→hidden.
`beforeunload` is **avoided** as a primary trigger (unreliable/discouraged); `pagehide` is the interruption-flush path.
Stored record = `{ text, ts (local ISO), schema_version, key fields }`. **No network request** is made to save a Level-2
draft. Not every keystroke (debounced). Storage-write failure → truthful failure status; never blocks.

### 6. Recovery behavior (§10)
Recovery is **explicit and safe**. On load, a **matching** non-stale draft for the current key is detected; it is offered
only when the current field is empty (or holds only a server-prefilled value) via a **low-emphasis, non-modal** prompt
with **Restore / Discard** (ignoring = continue without restoring). It **never silently overwrites** newer current text.
Stale/mismatched drafts (wrong `sid`/project, wrong field, wrong `context-id`/`context-version`, expired, malformed) are
**rejected, not restored**. The last-saved time is shown; an optional truncated preview may be shown. Bilingual EN/AR +
correct RTL. Recommended wording — EN: *"Unsent text was found on this device."* AR:
*"تم العثور على نص غير مرسل محفوظ على هذا الجهاز."*  Actions — EN: *Restore / Discard*; AR: *استعادة / حذف*.

### 7. Product-truth messages (§11)
Exact truthful states: *Saving locally…* · *Draft saved on this device* · *Could not save a draft on this device* ·
*Unsent text found on this device* · *Draft restored* · *Draft discarded* · *Answer submitted*. The UI **must NOT** say
"saved to your account", "saved securely on the server", "available on another device", or "permanently saved" (Level 2
is local-only). *"Draft saved on this device"* appears **only after a save event** (low-emphasis, transient/inline —
never a persistent banner). The experience stays low-emphasis and non-disruptive.

### 8. Successful-submission cleanup (§12)
The matching local draft is deleted **only after the client receives truthful evidence that the corresponding submission
was accepted** — i.e., the Post/Redirect/Get lands on the session view showing acceptance (the just-submitted answer was
accepted and the journey advanced), **not** merely that a POST was sent. Because the answered path redirects to
`show_session` on both success and error, the client distinguishes acceptance via a **minimal server-provided truthful
accepted signal** on the redirected render (a per-submit render-context flag — the only conditional `web/app.py`
change). The draft is **NOT** cleared on client/server/CSRF/token validation failure, store-unavailable, timeout,
disconnect-before-confirmation, ambiguous result, or an error redirect. The existing **accepted-answer idempotency model
is preserved unchanged**; **no** second submission/retry model is introduced. **Ambiguous case** (server may have
committed but the browser missed confirmation): **retain the local draft**; the existing token idempotency guarantees a
same-token/same-content resubmission is an idempotent no-op (no duplicate accepted answer); truthful retry is offered;
the draft clears only once a confirmed-accepted signal is observed.

### 9. Privacy (§13)
Invention/idea text is **sensitive**. The contract requires: a **disclosure at/before the first local draft save**,
delivered by **extending the existing Data & Session Notice** (`/data-and-session`, `data_session.html`) with **one
narrowly-scoped local-draft sentence** (no new large privacy system) plus a brief inline note at the surface; disclosure
of shared-device, browser-profile, and browser-sync risks and private-mode limitations; **explicit discard**; **local
expiry**; **cleanup after successful submit** and when the user chooses to start over. **No raw draft text** may appear
in logs, analytics, exception messages, URLs, query strings, browser history, or third-party telemetry. (The draft never
leaves the browser as a draft; the server receives text only through the normal, already-governed submission path.)

### 10. Retention / TTL (§14)
Local TTL options: **(a) 24 h**, **(b) 7 days**, **(c) 30 days**. **RECOMMENDED: (b) 7 days** — balances "return later"
usefulness against shared-device exposure; enforced by **lazy cleanup on load** + cleanup on submit + explicit discard;
stale (past-TTL) drafts are ignored and purged, never restored. **TTL classification: RECOMMENDED contract-fixed at
7 days, but REQUIRES OWNER CONFIRMATION at the implementation-authorization gate** (it is a privacy tradeoff). Not
configurable at runtime in the first increment.

### 11. Failure & fallback (§15)
Fail-closed for: storage unavailable; quota exceeded; invalid/corrupted JSON; incompatible schema version; missing
project/question identity; stale question; mismatched project; malformed timestamp; expired draft; JavaScript disabled;
unsupported browser; private-browsing restriction; multiple tabs; successful submission with cleanup failure. **A draft
failure must never block normal answer submission**; the application remains fully usable at truthful **Level 0** whenever
local draft storage cannot operate.

### 12. Multi-tab boundary (§16)
Minimum Level-2 rule: **last-write-wins by local timestamp per key**, with a `storage`-event **awareness note** when a
newer same-browser draft appears in another tab (so an older tab does not silently clobber it on its next flush). **No**
cross-tab locking, **no** conflict merge, **no** multi-device conflict resolution (that is Level 4 — out of scope).

### 13. Accessibility & bilingual UX (§17)
Preserve Arabic + English with correct RTL/LTR; full keyboard operation; screen-reader announcements via `aria-live`
polite for save/restore status; **non-color-only** save/failure indication; accessible Restore/Discard controls; **no**
disruptive repeated modal (inline non-modal recovery prompt); clear focus handling after restoration. Follow the existing
Phase 3 bilingual and accessibility principles and the G-UX-SHELL baseline.

### 14. Security (§18)
DOM insertion via `.value`/`textContent` only — **never** `innerHTML`; **no** third-party scripts; a single first-party
static script compatible with a current/future **CSP** (external file, no inline handlers; nonce if required); enforce the
size cap; ignore malformed content; **never** trust draft metadata; **no** ownership or server-authorization decision is
derived from local data; local draft content is **never** treated as an accepted answer without an explicit submit; no
draft execution or HTML interpretation. On submission the restored text is **untrusted client input** — existing
server-side validation and idempotency remain authoritative.

### 15. Permitted / prohibited future paths (§19)
- **REQUIRED (future implementation):** `web/templates/index.html`, `web/templates/session.html` (script include via the
  `{% block head %}` hook + minimal markup hooks/data-attributes + the recovery-prompt region); **one new first-party
  static JS file** under a new `web/static/js/` (served by Flask's default static route, currently unused); new focused
  tests.
- **CONDITIONAL:** `web/app.py` (minimal render context **only**: the per-submit truthful accepted signal + the
  `context-id`/`context-version` + field/key identifiers passed to templates); `web/templates/base.html` /
  `web/templates/data_session.html` (the one-sentence local-draft disclosure); registration of the static assets folder
  if none is wired.
- **PROHIBITED (unchanged):** `engine/progression_loop.py`, `engine/scoring.py`, `engine/idea_state.py`,
  `engine/record_contract.py`, `engine/session_reconstruction.py`, `engine/path_n_questions.py`,
  `engine/requirement_landscape.py`, `engine/idea_development_outputs.py`; any schema/migration; any server-side draft
  store; any account/auth path; CI/deploy. **No schema or migration is required for Draft Level 2.**

### 16. RED test contract (§20) — 22 behaviour-first proofs (to be written in the implementation gate, not here)
Each fails on the live tip because **no draft mechanism exists** (typed text is lost on reload / never offered for
recovery) and **cannot false-green** because each asserts an observable browser-storage/DOM/submission outcome, not mere
existence: (1) seed idea survives reload; (2) main answer survives reload before submit; (3) main answer survives
temporary offline; (4) interruption preserves the latest saved local version; (5) a matching draft is offered for
**explicit** restoration; (6) a draft is **not** silently restored over newer current text; (7) wrong project/session
draft not restored; (8) wrong field/question draft not restored; (9) stale question/version draft not restored;
(10) expired draft not restored; (11) corrupted draft ignored safely; (12) storage failure → truthful status, submission
not blocked; (13) failed submission keeps the draft; (14) successful accepted submission clears **only** the matching
draft; (15) ambiguous network result keeps the draft and idempotency prevents a duplicate accepted answer; (16) draft
storage never creates an `AssertionRecord`; (17) never calls deterministic evaluation; (18) never changes maturity/gaps/
outputs; (19) explicit discard removes the matching draft; (20) no raw draft content in logs/URLs/analytics/errors;
(21) JavaScript-disabled behaviour remains valid Level 0; (22) existing P4-1b-2a / P4-1b-2b / P4-2 / submission /
idempotency tests remain green. Likely test file: `tests/test_draft_l2_local_continuity.py` (+ a Level-0/no-JS server
regression assertion in the existing Flask tests).

### 17. Testing approach (§21)
The app is server-rendered with **no** existing client-JS test framework, no `web/static`, and no `package.json`.
Proving client-side `localStorage` persistence across reload/close/offline requires a **real browser** — server-only
Flask tests cannot. The environment **pre-provisions Chromium + Playwright browser binaries** (`/opt/pw-browsers`,
`PLAYWRIGHT_BROWSERS_PATH`) and Node 22. **RECOMMENDED (single approach): `pytest` + Playwright (Python) driving headless
Chromium** — it integrates with the existing pytest suite and truthfully exercises localStorage/reload/offline/restore/
submit-cleanup end-to-end. This requires adding the **`playwright` Python package as a TEST-only dependency**, justified
because no existing method can prove client-side storage behaviour and the browser binaries are already present (no
download; `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`). A pure-function Node/jsdom unit test of the extracted key/staleness/
cleanup logic is an acceptable **complement** but is not sufficient alone (it cannot prove real reload/offline
lifecycle). No large frontend framework or heavyweight suite is introduced.

### 18. Implementation structure (§22) — ONE increment
**RECOMMENDED: a single implementation increment** (RED behavioural Playwright tests → the localStorage save/recovery
primitive → UX integration, successful-submit cleanup, privacy disclosure, accessibility → GREEN + regressions).
Rationale: splitting storage from cleanup/privacy would ship an **unsafe intermediate** (drafts stored with no cleanup or
disclosure = a privacy hazard). The surface is bounded (2–3 fields, one primitive), so one coherent increment is the Lean
and safe choice. Internal RED→GREEN order applies. **Rollback:** clear the `localStorage` keys and remove the script
include + template hooks + optional render flag; **no** server or schema state exists to roll back; fully reversible with
no data loss (drafts are ephemeral local copies).

### 19. Product-truth boundary (binding)
Draft Level 2 is **local-only, same-device, explicit-recovery**. It does **NOT** provide cross-device recovery, server/
account persistence, accounts, authentication, authorization, ownership, verified email, writable continuation, or any
change to accepted-answer / idempotency / deterministic-evaluation semantics. It authorizes **no** implementation. Phase 5
remains the next step **immediately after** this bounded increment and is **NOT STARTED / NOT AUTHORIZED**; server-side
Draft Level 3, writable continuation, and every FPC remain **NOT AUTHORIZED / NOT STARTED**.


## Phase 5 — Accounts / Authentication / Project Ownership / Authorization / Verified Email — FORMAL CONTRACT-OF-RECORD (G-P5-FORMAL-CONTRACT-AND-CONTINUING-AUTHORIZATION-01)

**Status:** `FORMAL PHASE 5 CONTRACT-OF-RECORD — DOCUMENTATION-ONLY — NO PHASE 5 IMPLEMENTATION ACTIVE IN THIS GATE`.
The owner accepted the discovery **G-P5-IDENTITY-OWNERSHIP-DISCOVERY-CONTRACT-01** (verdict **B — ACCEPT WITH
NON-BLOCKING RISKS**), selected **Identity Option A (application-managed email + password)** and the implementation
structure **P5-1 → P5-2 → P5-3**, and granted a **continuing authorization** to complete all three bounded increments
through formal Phase 5 closure under the controls in §"RED/GREEN and review controls" below. **P5-1 becomes the next
eligible implementation gate only after THIS formal contract is merged and post-merge verified.** Recorded on live tip
`3b231936c5d01d2af9a1c0eca2dfd39d39161cff` (Merge PR #373).

### Accepted current state (evidence)
Existing **account / authentication / ownership / verified-email** foundation: **NONE**. Reusable primitives (no new
runtime dependency needed for Option A): a configured Flask `app.secret_key` (from `INVENTORAI_SECRET_KEY`, production
fail-fast; ephemeral in dev); Werkzeug **scrypt** password hashing; `itsdangerous`; stdlib `secrets`/`hmac`/`hashlib`;
the `SqliteRecordStore` adapter + additive-migration pattern; the existing generic-unavailable behaviour. Recorded
explicitly: **`flask.session` is currently unused; CSRF protection is absent; `projects` has no owner column; `sid` is a
project capability, NOT user identity; `sid` possession alone is never ownership proof.**

### Owner decisions (binding)
- **Identity approach:** application-managed **email + password**. Immutable **UUID `account_id`** as the durable primary
  key (**never email**); **normalized email with uniqueness**; **Werkzeug scrypt** password hashes; **no** plaintext
  passwords; **no** raw verification/reset/session tokens stored.
- **Unverified-account policy:** an unverified user MAY register, sign in, request/complete verification, request
  recovery, and access basic account-management surfaces. An unverified user MAY NOT create an account-owned durable
  project, claim an anonymous project, or use future sensitive delivery capabilities.
- **Verified-account policy:** **email verification is required before creating and owning a durable account-linked
  project.** Verified email is **not** itself authorization to any other project.
- **Anonymous-project policy:** existing and future anonymous projects keep the current `sid`-capability behaviour where
  explicitly allowed; they remain **`owner_account_id = NULL`**; they are **not automatically claimable**; possession of
  `sid` alone must never permit ownership assignment; anonymous-to-account **claim is deferred** to a separate future
  increment.
- **Session policy:** **idle expiry 2 hours; absolute expiry 14 days**; cookie `HttpOnly` + `SameSite=Lax` + `Secure`
  (production) and **not** the project `sid`; **`session_epoch`** used for revocation; **password reset revokes all
  existing authenticated sessions**; current-session logout plus a bounded **logout-all** via epoch rotation.
- **Account-deletion policy:** support **disable** (reversible immediate access block) and **delete** (tombstoned
  account state). On disable/delete: authenticated sessions invalidated; verification/reset tokens invalidated; new
  login blocked as applicable; **project-ownership links must not be silently transferred**; **accepted-answer data must
  not be automatically destroyed.** Final legal/commercial retention periods remain **outside this contract** and must
  not be invented.
- **Legacy-project policy:** legacy projects remain **`owner_account_id = NULL`**, capability-accessible only under the
  existing truthful boundary; they cannot be automatically claimed or converted to account ownership.
- **Email policy:** development = a **local file/console sink**; production = a provider adapter behind an `EmailSender`
  abstraction. **Verification token expiry 24h; password-reset token expiry 1h.** Tokens are random, **hashed at rest**,
  single-use, expiring, rate-limited, **never logged raw**. Phase 5 email is limited to **verification, password
  recovery, and future email change** — it does **not** include output/marketing/notification delivery.
- **Draft Level 2 policy:** Phase 5 **consumes but does not replace** Draft Level 2. On logout / account switching, a
  local draft must not be shown under another account/project identity; preserve truthful local-device wording; do
  **not** upload the draft to the server; do **not** implement Draft Level 3.

### Canonical account model (minimum fields)
`account_id` (UUID PK) · `email_normalized` (UNIQUE) · `email_verified` (bool) · `status` (`active`|`disabled`|`deleted`)
· `password_hash` (scrypt) · `session_epoch` (int) · `created_at` · `updated_at` · `deleted_at` (nullable). **No raw
credentials or tokens stored.**

### Token model (bounded, typed)
`token_id` · `account_id` · `token_type` (`verification`|`reset`) · `token_hash` · `expires_at` · `used_at` (nullable) ·
`created_at`. Raw tokens exist only in outbound email content and the user's request. Token responses must not permit
account enumeration.

### Project-ownership model
Additive **nullable `projects.owner_account_id`** (no separate ownership table for the MVP unless implementation
evidence proves the nullable column cannot support the accepted **single-owner** model). The ownership check runs
**server-side** for every protected read, answer submission, reconstruction, output view, delete, export, future
download, future output email, and future server-draft operation. **Templates and JavaScript must not be the
authorization boundary.**

### Security requirements (fail-closed)
scrypt hashing; non-enumerating authentication/recovery responses; login/session rotation; `session_epoch` revocation;
`HttpOnly`/`Secure`/`SameSite` cookies; **CSRF on authenticated state-changing requests**; hashed single-use expiring
tokens; server-side ownership checks; generic denial; brute-force + resend rate limits; **no** raw password/token/secret
logging; disabled/deleted-account fail-closed behaviour; **legacy-route authorization coverage**; **no `sid`-based
ownership claim**.

### Phase 5 increments
**P5-1 — Account & Credential Foundation.** Scope: additive `accounts` schema; normalized-email uniqueness; immutable
`account_id`; registration; scrypt hashing; account status; email-token data model; development email sink; generic
registration response; foundational rate-limit storage; RED/GREEN tests. **Not** included: authenticated project
ownership; route authorization; Draft Level 3; output email; social login; live production email provider.

**P5-2 — Authenticated Sessions, Verified Email & Recovery.** Scope: login/logout; Flask signed authenticated cookie;
`session_epoch` revocation; idle + absolute expiry; CSRF; verification flow; resend behaviour; account recovery;
password reset; reset revokes sessions; generic non-enumerating responses; RED/GREEN tests. **Not** included: project
ownership enforcement; anonymous claiming; Draft Level 3.

**P5-3 — Project Ownership & Route Authorization.** Scope: additive nullable `projects.owner_account_id`; owner linkage
at **authenticated + verified** project creation; legacy NULL-owner compatibility; a central server-side ownership
check; the authorization matrix across protected project routes; generic 404/not-available; cross-account isolation;
disabled/deleted-account handling; Draft Level 2 logout/account-switch isolation; RED/GREEN tests. **Not** included:
collaboration; sharing; organization ownership; multiple owners; anonymous claiming; Draft Level 3; writable
continuation.

### RED/GREEN and review controls (each increment)
(1) define the bounded implementation contract; (2) produce genuine RED on the live parent; (3) implement the minimum
GREEN; (4) run focused + related + security + full-suite tests; (5) adversarial self-review; (6) one SHA-preserving
bundle; (7) stop before publication; (8) independent adversarial review; (9) publish only after **A or B without
blockers**; (10) merge via "Create a merge commit"; (11) post-merge verification; (12) governance synchronization
before the next increment where materially required. **The continuing owner authorization permits moving P5-1 → P5-2 →
P5-3 without a new owner authorization, provided all controls pass.** Stop and return to the owner only on: a material
blocker; live repository contradicting the accepted discovery; scope outside the accepted Phase 5 boundary; a new
product-policy decision not resolved above; an independent review returning **C**; or security that cannot be proved
fail-closed.

### Non-blocking risks (recorded)
(1) production `Secure`-cookie behaviour depends on confirmed HTTPS/reverse-proxy configuration; (2) no current
rate-limit primitive exists — use a small bounded store-backed counter, **not** a broad new platform/dependency; (3)
production email deliverability is an operational dependency — begin with the development sink and preserve the provider
abstraction. These do not block P5-1 contract definition.

### Permitted / prohibited future implementation paths
**REQUIRED (future):** `web/app.py`; new auth/account/session/token/ownership/email modules; new register/login/verify/
recover templates; additive schema/migration in the store adapter; new tests. **CONDITIONAL:** `engine/record_store.py`
— additive nullable `owner_account_id` column + migration + owner get/set + ownership-scoped read (additive-only,
mirroring the P4-1b-2a `idempotency_key` and P4-2 reconstruction-column precedent); a privacy-notice template update.
**PROHIBITED:** the deterministic engine — `engine/progression_loop.py`, `engine/scoring.py`, `engine/idea_state.py`,
`engine/record_contract.py`, `engine/session_reconstruction.py`, `engine/path_n_questions.py`,
`engine/requirement_landscape.py`, `engine/idea_development_outputs.py`; production `requirements.txt` (Option A needs
**no** new runtime dependency); CI/deploy; Draft Level 3; writable continuation; output/marketing email delivery;
PDF/ACV/AI-Coach/WS17/STG; collaboration/sharing/teams/orgs/subscriptions/social-login-SSO/admin dashboard; any later
phase. **Authorization logic must never live only in templates/JS.**

### Continuing authorization boundary
This is a **documentation-only** formal contract. It authorizes **no** production/test code, no schema/migration, no
dependency, no CI, no push/PR/merge in this gate. **P5-1 implementation is the next eligible gate, eligible only after
this formal contract is merged and post-merge verified.** **P5-2 and P5-3 are NOT STARTED. Draft Level 3, writable
continuation, output email delivery, and every FPC remain NOT AUTHORIZED / NOT STARTED.** Decision **D17** and the AISR
seven-owner model are preserved; Phase 4 remains FORMALLY CLOSED; P4-2 Level-1 and Draft Level 2 remain CLOSED.


## P4-1b-2a Increment Contract Candidate — REV1 — G-P4-1B-2-DOC-01-REV1 (HISTORICAL PRE-IMPLEMENTATION CONTRACT STATE — the increment is now IMPLEMENTED / MERGED / CLOSED via PR #365; see the closure banner and the "Active contract" status above)

> **[CLOSURE STATUS — G-P4-1B-2A-IMPLEMENTATION-01-REV1, owner verdict B.]** The increment defined by this contract (as
> amended for OPTION A by G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01) is now **IMPLEMENTED, MERGED, VERIFIED, ACCEPTED, AND
> CLOSED** — merged via **PR #365** (merge commit `77bd10cc55a731b18d4e35ea262b55342a9f847f`, parents `4a31ece` +
> `0b5f757`, tree `c8808be`; candidate ancestry PASS). `record_id` remains `rec_N`; a separate durable idempotency
> identity was implemented; no deterministic-output engine changed. The candidate/contract-definition text below is
> **preserved as historical record** and is no longer the pending state. **P4-1b-2b, P4-2, Phase 5+, and every FPC
> remain NOT AUTHORIZED / NOT STARTED.** See `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` and
> `OWNER_DECISION_REGISTER.md` (`D-P4-1B-2A-IMPL-01…04`).

**0. Provenance & preservation.** REV1 supersedes the original P4-1b-2a contract candidate
`0e2a5cec24d71462eadbffa193e3467d40d506a0` (gate G-P4-1B-2-DOC-01), which received independent-review verdict
**C — REVISE AND RE-REVIEW** and is **PRESERVED intact, unmerged, NOT PUBLISHABLE, and NOT amended**. A previously
claimed `518cfdfe0eca3fb0f52c88c5baea46c643d3c288` candidate/bundle is **not an established repository artifact** and is
not relied upon. REV1 is a **new** candidate created from live tip `25dacb00295bcd3d34fd2cb5f789e9eae390ae11`.

**1. Gate identity & status.** P4-1b-2a — Durable Answered-Event Append and Web-Layer Idempotency. Gate
**G-P4-1B-2-DOC-01-REV1**. **Status (HISTORICAL PRE-IMPLEMENTATION CONTRACT STATE):** at the time this contract was
defined it read `CORRECTED CONTRACT CANDIDATE — NOT YET MERGED · IMPLEMENTATION NOT AUTHORIZED · P4-1b-2a NOT STARTED`;
**that state is superseded — P4-1b-2a is now IMPLEMENTED / MERGED / VERIFIED / ACCEPTED / CLOSED (PR #365; see the
"Active contract" status above).** **P4-1b-2b, P4-2, Phase 5 remain NOT AUTHORIZED / NOT STARTED.** Owner decisions govern
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
>
> **[SUPERSEDED / RESOLVED — see “P4-1b-2a Contract Amendment — G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01” below.]** The
> owner has formally **SELECTED OPTION A**: the deterministic engine `record_id` **stays `rec_N` (unchanged)**, and a
> **SEPARATE durable idempotency identity** (distinct from `record_id`) is introduced. The `evt-*` scheme is therefore
> **NOT adopted as `record_id`**, and the derived-output engines (`engine/idea_development_outputs.py`,
> `engine/requirement_landscape.py`) are **NOT changed**. Options **(b)** and **(c)** above are recorded **REJECTED**
> (reasons in the amendment). This resolution introduces a **bounded `engine/record_store.py` storage amendment**, so
> stable idempotency is **NOT a web-layer-only change**.

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
> **[AMENDED — see G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01 below.]** Under the selected **Option A**, this hashed,
> project-bound, token-derived value is the **SEPARATE durable idempotency identity** — it is **NOT** the engine
> `record_id` and is **NOT** rendered as an `evt-*` `record_id`. The `record_id` remains the positional `rec_N`
> produced by `engine/idea_state.py`. The precise raw-vs-hash-vs-HMAC form, encoding, and truncation bound are refined
> by the amendment and remain an **implementation-gate decision**, not locked here.

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
> **[AMENDED — see G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01 below.]** Under the selected **Option A** the B3 resolution does
> **NOT** touch `engine/idea_development_outputs.py` or `engine/requirement_landscape.py` (the derived-output engines are
> left unchanged because `record_id` stays `rec_N`). Instead it introduces a **bounded, additive
> `engine/record_store.py` storage amendment** for the separate durable idempotency identity (evaluated — not locked — as
> an additive nullable column + uniqueness constraint, or a sibling table). That storage amendment is a **separate future
> implementation authorization**, not granted by this documentation-only gate.

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

## P4-1b-2a Contract Amendment — G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01 (B3 OWNER DECISION = OPTION A) — MERGED (HISTORICAL PRE-IMPLEMENTATION CONTRACT STATE; the Option-A decision below remains authoritative, but its "not authorized / not merged" status is superseded — P4-1b-2a is IMPLEMENTED / MERGED / CLOSED via PR #365)

**A0. Provenance & preservation.** This amendment amends the merged **P4-1b-2a REV1** contract candidate
(`G-P4-1B-2-DOC-01-REV1`, above) **only** to correctly incorporate the owner's B3 decision. The REV1 candidate and all
prior candidates, verdict-C history, clarifications `C1…C8`, and preserved observations remain **intact and preserved**;
this amendment supersedes **only** the specific B3 `DETERMINATION` (the "(a)/(b)/(c) owner-decision-required" outcome),
the C5 event-id parenthetical, and the Permitted/Prohibited paths NOTE — each flagged inline above. Authored on the
authoritative live tip resolved from Git (`origin/feature/atomic-json-session-persistence`); this gate mints its own
newly generated commit/tree/bundle SHAs and reports them honestly. A previously claimed
`518cfdfe0eca3fb0f52c88c5baea46c643d3c288` artifact remains **not an established repository artifact** and is not relied
upon.

**A1. Gate identity & status.** Gate **G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01**. **Type:** documentation-only contract
amendment preparation. **Status (HISTORICAL PRE-IMPLEMENTATION CONTRACT STATE):** at amendment-preparation time this read
`CONTRACT AMENDMENT CANDIDATE — NOT YET MERGED · IMPLEMENTATION NOT AUTHORIZED · P4-1b-2a NOT STARTED`; **that state is
superseded — the amendment is merged and P4-1b-2a is IMPLEMENTED / MERGED / CLOSED (PR #365).** The Option-A decision
recorded here remains authoritative. As authored, this gate recorded an owner decision and corrected the contract text; it authorized **no** push,
PR, merge, code/engine/schema/test/template change, or phase activation. **P4-1b-2b, P4-2, Phase 5+ remain NOT
AUTHORIZED / NOT STARTED.** Governing decision: `D-P4-1B-2A-B3-01` (Option A selection) plus the retained
`D-P4-1B-2-REV1-*` decisions in `OWNER_DECISION_REGISTER.md`.

**A2. B3 OWNER DECISION — OPTION A SELECTED (binding).** The owner formally **SELECTED OPTION A: SEPARATE THE DURABLE
IDEMPOTENCY IDENTITY FROM THE DETERMINISTIC ENGINE `record_id`.** Concretely:
  * The engine **`record_id` remains the positional `rec_N`** produced by `engine/idea_state.py`
    (`record_id = f"rec_{len(self.assertions)+1}"`). It is **unchanged** in value, format, creation site, ordering role,
    and every derived-identifier consumer.
  * A **SEPARATE durable idempotency identity** (the server-issued-token-derived value) is introduced and stored
    **separately** from `record_id`. It is the durable duplicate/idempotency backstop **only**; it is **never** consumed
    by the deterministic derived-output engines and is **never** rendered as an `evt-*` `record_id`.
  * **Option B REJECTED:** engineering a durable event id that is "order-equivalent to `rec_N`" and embeds acceptably in
    `idea_development_outputs.py`/`requirement_landscape.py` enlarges the deterministic-engine blast radius, couples the
    idempotency key to sort/derivation semantics, and risks silent semantic drift — contrary to the governance contract.
  * **Option C REJECTED:** "keep `rec_N` in the derived path" while still deriving the idempotency key **from** `rec_N`
    conflates two concerns (positional identity vs. request-idempotency) and provides no unpredictable, request-bound,
    replay-safe idempotency guarantee. Option A keeps `rec_N` in the derived path **and** gives idempotency its own
    identity — a strict superset of C's benefit with none of the conflation.

**A3. Correction of the "web-layer-only / no-amendment" implication (mandatory).** Any statement — in REV1 or earlier —
implying that stable/durable idempotency is a **web-layer-only** change, or that **no engine/storage amendment** is
required, is **INCORRECT and is hereby superseded.** Evidence at the live tip: `engine/record_store.py` `records` table
is `PRIMARY KEY (project_id, record_id)` with **no** idempotency/token column and no separate uniqueness constraint for a
request-idempotency identity. Storing a **separate** durable idempotency identity therefore **requires a bounded,
additive `engine/record_store.py` storage amendment.** Option A is **not** implementable in the web layer alone.

**A4. Two separate identity concepts (normative definitions).**
  * **Deterministic engine `record_id` (`rec_N`)** — positional, append-only, assigned by `engine/idea_state.py`;
    consumed by ordering (`_record_sort_key` / `_rec_sort_key` lead-0 precedence), derived requirement identifiers
    (`req:assertion:rec_N`), anchors, rationale metadata, contradiction-pair ordering, and other `record_id` consumers.
    **Unchanged by Option A.**
  * **Durable idempotency identity** — a separate, server-issued-token-derived value bound to a single accepted
    answered-submission request; its sole role is to make durable append **idempotent** (exactly-once) and to detect
    duplicate retries. It is **not** an engine identifier, **not** an ordering key, and **not** embedded in any derived
    output. It lives in the storage amendment (A9), not in `record_id`.

**A5. Token & security requirements (implementation-gate contract).** The idempotency token MUST be:
  * **server-issued** (never client-supplied as authority), **cryptographically strong / unpredictable**, of a
    **bounded, sufficient length**, and **URL/form-safe**;
  * **bound** to project/session (`sid`) and to the specific answered **operation** (one accepted answered submission);
  * **single-use for acceptance** — a valid token accepts at most one durable answered event;
  * transported **only** via a hidden server-issued form field on the answered-producing forms (A7); **never** placed in
    URLs, logs, analytics, or user-facing errors;
  * subject to a defined **lifecycle/expiration** (issued with the form render; consumed on acceptance; re-issued for a
    fresh legitimate submission);
  * **raw-vs-hash-vs-HMAC storage form is an explicit implementation-gate decision that remains REQUIRED** — the
    amendment records the requirement (do not store a reversible secret unnecessarily; prefer a one-way/keyed digest for
    the stored idempotency identity) but does **not** finalize the exact digest/keying here.
  * **Rejection contract (fail closed):** a **missing**, **malformed**, **expired**, **cross-session**, or
    **cross-project** token MUST cause a fail-closed, generic, non-disclosing rejection with **no** durable append and
    **no** acceptance. There is **no tokenless fallback** (retained from B1).

**A6. Uniqueness & payload binding.** The durable idempotency identity's uniqueness is scoped to
**(project + idempotency identity + operation)**. The durable record MUST bind the idempotency identity to a
**normalized fingerprint of the accepted-request content**, so that:
  * **same token + same normalized request** → return the **prior** durable result (no second event, no second
    progression, no reconstructed `last_result`, no replay claim) — an idempotent no-op (retains C2);
  * **same token + different request content** → **fail closed** (retains C3: never auto-classify an IntegrityError as a
    duplicate; confirm exact identity + same project + same logical content by reload before treating as duplicate);
  * uniqueness is enforced **durably** (storage-level constraint, A9), not only in the web layer.

**A7. Both answered-producing forms (retained B2).** The hidden idempotency token MUST be carried by **every**
answered-producing form in `web/templates/session.html`: (i) the **main answer form**; (ii) the **criticality-correction
free-text form** (which posts no `action` and is treated as `answered` by the legacy rule in `web/app.py`). An
inventory/route-form regression MUST prove **no** answered-producing form bypasses the token.

**A8. Persist-before-acknowledge ordering (retained C1/C6).** On an accepted answered submission the implementation MUST
stage evaluation on a cloned `IdeaState`, create the `AssertionRecord` (with its **`rec_N`** `record_id`) and the
**separate** durable idempotency identity, **append durably**, and **only after durable success** publish staged state /
transcript / `last_result` into `SESSION_STORE`. On append failure it discards the staged copy and leaves live memory
unchanged. Durable-success / memory-failure invalidation follows C6.

**A9. Storage amendment — likely-owner `engine/record_store.py` (evaluated, not locked).** The separate durable
idempotency identity requires a **bounded, additive** amendment to `engine/record_store.py`. Two shapes are recorded as
**candidates to evaluate at the implementation gate** — the schema is **NOT locked here**:
  * **(i)** an **additive nullable column** on `records` (e.g. an `idempotency_key` / `idempotency_fingerprint`) plus a
    **partial/nullable UNIQUE constraint** scoped to `(project_id, idempotency_key)` for non-null keys; **or**
  * **(ii)** a **sibling table** keyed by `(project_id, idempotency_key)` referencing the owning record, with its own
    UNIQUE constraint.
  In **both** shapes: the existing `PRIMARY KEY (project_id, record_id)` and `rec_N` semantics are **unchanged**;
  legacy/volatile `rec_N` non-answer records and pre-amendment rows carry a **NULL** idempotency identity and remain
  valid (mixed-state, retains C8); the change is **additive only** (no column drop, no type change, no `rec_N`
  rewrite). Selection between (i) and (ii) and the exact constraint form is a **separate implementation-gate decision**.

**A10. Migration & rollback (against the live DB mechanism).** Because a durable SQLite store already exists, the storage
amendment MUST specify a **real forward migration** against the live schema (additive column/constraint or new table,
applied idempotently to existing databases) and a **defined rollback** that is safe on populated databases — **not**
"just drop the column." Rollback MUST preserve existing `records`/`rec_N` data and MUST NOT corrupt or orphan durable
answered evidence; where a physical drop is unsafe, rollback is specified as **disable-and-ignore** (stop enforcing/
reading the idempotency identity) rather than destructive removal. Exact migration/rollback mechanics are an
implementation-gate deliverable.

**A11. RED test contract & false-green prohibitions (retained + extended).** The future implementation remains **RED-first
and behavior-based**. Required RED coverage: **RED-B1** answered POST without a valid token **fails closed**; **RED-B2**
inventory/route-form regression proves no answered-producing form bypasses the token; **RED-A6** same-token+same-request
→ idempotent no-op (one durable event), same-token+different-request → fail closed, duplicate retry produces no second
event/progression; **RED-A9** durable uniqueness is enforced at the storage layer (constraint proven, not only web-layer
guarded); **RED-C8/mixed-id** `rec_N` answered/non-answer records with NULL idempotency identity coexist with
idempotency-bearing records and deterministic derived output (**`rec_N` ordering, `req:assertion:rec_N` identifiers,
pair ordering**) is **unchanged** (this is now a *stability* assertion, since Option A leaves the derived engines
untouched). **Prohibited false-green paths:** no conftest token auto-injection; no weakened/skipped assertions in the
enumerated B1 existing tests; no reliance on `SESSION_STORE`/replay to simulate durability; no recomputation of
pass/fail outside real behavior. Replay greenness is not proof.

**A12. Logging & observability.** The idempotency token and any raw user answer content MUST NOT appear in logs, error
messages, analytics, or URLs. Observability is limited to non-sensitive, non-disclosing signals (e.g. accepted / duplicate
no-op / fail-closed **counts or generic markers**) sufficient to prove the idempotency behavior without leaking secrets or
user content.

**A13. Explicit exclusions (unchanged scope walls).** This amendment does **NOT** authorize: any change to the engine
`record_id` / `rec_N` scheme; adoption of the `evt-*` id as `record_id`; P4-1b-2b; P4-2 (replay / durable output /
stale-output / full session resume); Phase 5 (accounts, ownership, sharing, permissions); any FPC (FPC-01…FPC-04);
PDF / Email / STG / WS17 / ACV; any event-bus or general-idempotency abstraction; retention/deletion/permission
hardening; multi-thread/multi-worker concurrency (C4 `threaded=False` topology retained). No downstream activation is
implied; closing this gate activates nothing.

**A14. Product-truth boundary (unchanged).** Even after implementation, P4-1b-2a may claim only **durable accepted-answer
evidence** with re-derivable readiness; it does **not** restore progression, deliverable, outputs, or Keep/Refine, and
does not claim a saved project / fully saved idea / durable outputs / "resume exactly where you left off" / complete
session resume / account-owned records.

**Boundary.** This is a documentation-only contract amendment. **No implementation authority is granted.** P4-1b-2a
implementation still requires: this amendment independently reviewed and merged; a separate explicit implementation
authorization; and RED-first behavior-based proof. Append-only governance; prior candidate history preserved.

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
