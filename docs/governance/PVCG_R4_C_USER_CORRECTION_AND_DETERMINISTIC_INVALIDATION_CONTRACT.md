# PVCG-R4-C — User Correction and Deterministic Invalidation — CONFORMANCE CONTRACT (Candidate)

**Status of THIS record:** governance/documentation-only **CONTRACT CANDIDATE**. It implements nothing,
changes no runtime, test, fixture, pack, registry, generator, evidence, schema or persistence file, and
authorizes no code. It becomes authoritative **ONLY if/when this exact candidate is merged and
post-merge verified**, and even then it authorizes **no implementation**: PVCG-R4-I requires its own
separate, explicit Owner execution authorization, exactly as R2-I and R3-I did.

**`OWNER_DECISION_REGISTER.md` UNCHANGED** — this candidate records no new Owner decision. The Owner
rulings **OD-R4-01 … OD-R4-10** governing this gate were issued as a directive and are reproduced here
as **[OWNER]**, not as repository fact.

**Base:** `18a90f9b0aa85d05317bed5aaa596e19716c6557` — the live authoritative tip of
`origin/feature/atomic-json-session-persistence`, independently re-fetched and re-verified this gate
(PR #553; first parent `d046b3e5449f5f91f5f719686e7e207ceda2f06c`, second parent
`0fa8fbd83ee2b3a8de165eaaa1a9fd0d4e64c290`, merge tree `5101c167c91a87184e701e3236f1aa62be8be376`
identical to the accepted candidate tree, candidate→merge diff EMPTY, zero later commits, clean tree)
**[REPO]**.

---

## §0. Evidence-class legend (binding on every statement below)

| Class | Meaning |
|---|---|
| **[REPO]** | Authoritative repository fact, citable to a committed file and location at the base SHA. |
| **[EXEC]** | **Creator-local executed diagnostic evidence** produced by a read-only probe in this session against the base tree. Reproducible by re-running the same probe at the same SHA, but **NOT** promoted to permanent repository fact by being recorded here. PVCG-R4-I must re-measure independently. |
| **[OWNER]** | An Owner decision or directive. Not a repository fact. |
| **[OPEN]** | Unresolved; owed to a later gate. |

Nothing in this record may be read as a repository fact unless marked **[REPO]**.

**Execution-environment disclosure, stated before any evidence claim.** The container that produced this
candidate has **Python 3.11.15 but neither `pytest` nor `flask` installed** **[EXEC]**. **No test suite
was executed for this candidate and no suite figure is claimed anywhere in it.** Every **[EXEC]** fact
below is either a direct `python3` probe against `engine/` (which imports without Flask) or a verbatim
reproduction of a committed test's own logic, labelled as such. Web-layer findings are source-read
**[REPO]** citations, not executed behaviour. See §23.

---

## §1. WHY THIS GATE EXISTS — AND WHAT IT IS NOT

**§1.1 PVCG-R4 is a conformance gate, not a capability owner [OWNER: OD-R4-01].** Its subject is *user
correction + deterministic invalidation through full re-evaluation*. Its purpose is to verify that the
**already-owned** correction / revision / stale-state obligations are implemented and conform to the
PVCG truthfulness and determinism requirements.

```
PVCG-R4 = CONFORMANCE / ASSURANCE GATE
PVCG-R4 ≠ PARALLEL CAPABILITY OWNER
```

**§1.2 Implementation ownership is unchanged [OWNER: OD-R4-02].** It remains with the repository's
existing canonical owners — **FPC-02 + P4-2**, together with the accepted supporting decisions and
obligations (**D17 / D-AISR-06 / D-P4-05** where applicable). This contract **consumes and verifies**
that implementation. It must not reproduce it under a second architecture or a second state model.

| Role | Owner |
|---|---|
| **IMPLEMENTATION OWNER** | **FPC-02 / P4-2** |
| **PVCG CONFORMANCE OWNER** | **PVCG-R4** |

**§1.3 The duplication rulings this gate preserves [REPO].**
`ACTIVE_EXECUTION_ROADMAP.md` §"Future Product Capability Integration Map", **FPC-02 — Revision
Difference and Stale-Output Handling**, classifies the capability as *"CANONICAL PRODUCT REQUIREMENT —
ALREADY OWNED BY P4-2 + D17 + PHASE-3C. This is **not** a new capability"*, and names its missing
elements as *"a **P4-2 implementation contract** for durable revision/output relationships,
stale-output invalidation, updated deterministic output, and full replay; and the accepted in-session
**'What changed?'** presentation increment"* **[REPO]**. Ratified as **`D-FPC-MAP-02` (ACCEPTED)** in
`OWNER_DECISION_REGISTER.md` **[REPO]**. The governing duplication ruling **`D-FPC-MAP-06` (ACCEPTED)**
states, for every overlap including P4-2, D17 and the Phase-3C revision UX: ***"DO NOT CREATE A NEW
PARALLEL MODEL — EXTEND OR CONSUME THE EXISTING CANONICAL MODEL"*** **[REPO]**.

**This contract is written to satisfy both.** It creates no new state model, no new record type, no new
persistence schema, no second replay engine, and no second dependency model.

**§1.4 The repository-side reason a conformance gate is nonetheless needed.** The obligations exist and
are assigned; **the conforming behaviour does not exist in the runtime**. Committed governance says so
in its own words: `PHASE_4_DURABLE_DATA_AND_EVIDENCE_ENTRY_DECISION.md` records *"Engine-only
supersession/contradiction primitives (`mark_supersession`/`mark_contradiction`), **not route-exposed**
[code-exists; runtime-unreachable from UI]"* and *"**No full user-invocable replay/re-evaluation path**
exists"* **[REPO]**. Both statements were independently reproduced from source in the read-only R4
diagnosis before that passage was located, and they agree exactly **[EXEC]**.

R4 exists to make that conformance provable, and nothing wider.

---

## §2. OWNERSHIP AND CLASSIFICATION MAP (binding)

Every element in R4's subject area carries exactly one classification. **No element may be reassigned
to R4 merely because the wording differs.**

### §2.1 ALREADY OWNED — R4 verifies; R4 does not build

| Element | Canonical owner | Citation |
|---|---|---|
| Stale-output invalidation | **P4-2** | `engine/record_contract.py` and `engine/record_store.py` scope-boundary headers, both live runtime code: *"**P4-2 owns** full deterministic rebuild/replay from accepted source inputs, deterministic output records, and stale-output invalidation"* **[REPO]** |
| Durable output records; source→output binding | **`P4-OBL-OUTPUT-01`** (Owner: Phase 4; Earliest: P4-2; Sep-auth: required) | `PHASE_4_…ENTRY_DECISION.md` deferred-obligations **[REPO]** |
| Deterministic rebuild + full re-evaluation from accepted inputs | **`P4-OBL-REEVAL-01`**, **`D-P4-05`** | same **[REPO]** |
| Revision-difference visibility / "What changed?" UX | **Phase-3C** + FPC-02 | FPC-02 map entry **[REPO]** |
| Contradiction and supersession **data model** | **Increment 2 — IMPLEMENTED** | `engine/idea_state.py` `mark_contradiction`, `mark_supersession` (acyclic, cycle-rejecting, atomic, non-destructive) **[REPO]** |
| Durable serialization **and load-validation** of supersession edges | **P4-0 — IMPLEMENTED** | `engine/record_contract.py` `_ASSERTION_FIELDS` includes `contradicts`, `supersedes`, `superseded_by`; `validate()` rejects unknown references, self-supersession, and supersession cycles **[REPO]** |
| Active-set filtering of derived state | **Increment 2/3/4 — IMPLEMENTED and CONSUMED** | `superseded_by is None` consumed by `engine/derived_readiness.py`, `engine/requirement_landscape.py`, `engine/idea_development_outputs.py`, `engine/validation_plan.py`, `engine/safety_signal.py` **[REPO]** |
| Deterministic full replay engine | **P4-2 Level-1 — IMPLEMENTED, MERGED, CLOSED (PR #369)** | `engine/session_reconstruction.py` replays the seed then accepted answers in `seq` order through the **unchanged** `progression_loop.run_iteration` **[REPO]** |
| Readiness permitted to decrease on supersession | **Increment 2 — IMPLEMENTED** | `engine/derived_readiness.py` `_is_active`; `tests/test_increment_2_truthful_state.py::test_verified_readiness_false_when_verified_superseded_by_unvalidated` **[REPO]** |
| Recompute-on-read of all derived artifacts | **IMPLEMENTED** | deliverable assembled fresh per request; `keep-snapshot` *"NEVER serializes/duplicates/versions"*; readiness *"never serialized … always re-derived"* **[REPO]** |
| Forward-only gap lifecycle | **WPS-001 INV-004** | `EPISTEMIC_FOUNDATION_DESIGN_DECISION.md`: *"The forward-only gap lifecycle (WPS-001 INV-004) is preserved: stored gap status … never backward"* **[REPO]** |

### §2.2 TRUE R4 CONFORMANCE RESIDUALS — what R4 must cause to become true

| ID | Residual | Evidence |
|---|---|---|
| **R4-RES-1** | **Correction is not expressible.** No route, form, template or API accepts a correction, retraction or replacement of previously accepted material. `web/app.py` declares **40 routes carrying only `GET` (17) and `POST` (24) — zero `PATCH`, `PUT` or `DELETE`** — and `web/api_v1.py` declares none **[EXEC]**. The sole correction-shaped surface, `criticality_correction`, is a UI routing flag that **stores nothing** and returns the inventor to the ordinary free-text answer path **[REPO]** |
| **R4-RES-2** | **The invalidation machinery is unreachable.** `mark_supersession` and `mark_contradiction` have **zero** runtime callers; the only ledger mutator reachable from a route is `record_interaction`, whose signature carries **no `supersedes` parameter**. The five-module active-set filter is therefore a permanent no-op in production — every record is always active **[REPO]** |
| **R4-RES-3** | **Progression state carries no invalidation concept at all.** `Gap`, `Evidence`, `known_problem`, `known_mechanism` and `maturity_level` have no supersession field. `maturity_level` is only ever `+= 1`; `known_mechanism` is replaced only when `quality >= existing.quality`; `known_problem` only when `is None` **[REPO]** |
| **R4-RES-4** | **No user-invocable replay.** `reconstruct_review_state` exists and is deterministic, but nothing invokes it to replace live state after a change to the accepted-source stream **[REPO]**; committed governance states the same **[REPO]** |
| **R4-RES-5** | **No withdrawal marker.** No surface anywhere states that a prior basis was withdrawn (§3.2) **[EXEC]** |
| **R4-RES-6** | **Latent CLOSED-gap hazard** (§10) **[EXEC]** |
| **R4-RES-7** | **The only dedicated INV-004 test is vacuous on its own corpus** (§10.3) **[EXEC]** |

### §2.3 OUT OF SCOPE — exists elsewhere, not R4's to verify

Versioning, branching, rollback — *Phase 4 explicitly did not deliver them* **[REPO]**; sharing,
permissions, recipient identity, access revocation — **Phase 5** **[REPO]**; PDF and Email — **OD-U**
**[REPO]**; specialist-specific technical content — **STG/D13** **[REPO]**; domain expansion, new gap
types, scoring changes; the AI Coach (**WS17**); **TDVP**.

### §2.4 PROHIBITED — authoritatively forbidden, not merely unscoped

| Prohibition | Authority |
|---|---|
| **Targeted / partial / selective re-evaluation** | **`D-AISR-06` (ACCEPTED)**: *"Full deterministic re-evaluation mandatory after accepted material change; **targeted partial prohibited** (preserves D17)"* **[REPO]**; `PHASE_4_…ENTRY_DECISION.md` §12: *"**Targeted partial re-evaluation is prohibited** until a separately authorized and independently verified deterministic dependency model proves it safe (preserves D17 and D-AISR-06)"* **[REPO]**; reaffirmed **[OWNER: OD-R4-03]** |
| **Any dependency graph or targeted propagation model** | same **[REPO]**; **[OWNER: OD-R4-03]** |
| **A full contradiction engine**, free-form semantic contradiction detection, semantic conflict graph, probabilistic contradiction reasoning, LLM truth arbitration, autonomous intent inference, cross-project contradiction analysis | **[OWNER: OD-R4-04]** |
| **Destructive deletion or mutation of a prior accepted-source record** | `record_interaction` *"never mutates an existing record and never removes one"* **[REPO]**; the durable store contains **no `UPDATE` statement whatsoever** **[REPO]**; **[OWNER: OD-R4-06]** |
| **Reopening ordinary CLOSED gaps through the normal forward-answer path** | **WPS-001 INV-004** **[REPO]**; **[OWNER: OD-R4-07]** |

**§2.4.1 "Bounded" is defined, so it cannot drift [OWNER: OD-R4-03].** Everywhere in this contract and
in any successor R4 document, **"bounded" means bounded SCOPE and bounded AUTHORIZATION. It never means
targeted partial recomputation.**

### §2.5 DEFERRED — recorded, not repaired here

R3 residuals **N-2** (acknowledged-unknown length threshold) and **U-4** (a single Arabic connective in
English prose), each carried by `PVCG_R3_FORMAL_CLOSURE_RECORD.md` §6 with the explicit statement that
neither *"is PVCG-R4 authorization"* **[REPO]** — they are **not** admitted to R4 by this contract; the
in-session *"What changed?"* presentation increment (**Phase-3C / FPC-02**, a UX gate of its own)
**[REPO]**; durable output records and source→output binding (`P4-OBL-OUTPUT-01`), which R4 does
**not** require and which remain separately gated **[REPO]**; the R2-C/R3-C wording discrepancy of §19.4
**[OPEN]**.

---

## §3. THE PROVEN DEFECT (the exact narrow statement R4 must close)

**§3.1 Statement [OWNER: OD-R4-05, accepted on the diagnosis].**

> **A user who discovers that previously supplied accepted material was wrong has no explicit way to
> withdraw that source material. Submitting corrective or retraction language does not invalidate the
> earlier authoritative progression state. Consequently, previously derived conclusions may remain
> current even though their basis has been explicitly withdrawn.**

**§3.2 The measured demonstration [EXEC].** Driven **entirely through the runtime path** — `run_iteration`
only, Path-N, electronics/electrical, no direct engine mutation:

```
3 strong causal answers →  MECHANISM_COMPLETENESS  CLOSED (closed_at=3)
                           PHYSICAL_FEASIBILITY    CLOSED (closed_at=5)
                           BOUNDARY_AMBIGUITY      CLOSED (closed_at=7)
                           maturity_level = 2, current_stage = 3

then x4: "Actually I was wrong. There is no relay at all. I do not know how it works."

AFTER:   gaps unchanged — CLOSED / CLOSED / CLOSED
         known_mechanism still holds the ORIGINAL relay text at REASONED
         maturity_level still 2
         acknowledged_unknowns = 4          (R1 records the withdrawal)
         transition = "WARN", "not addressed"   (R2 denies it progression — correct)
```

The withdrawn mechanism text then appears in the assembled deliverable in **four** places as current
content **[EXEC]**:

```
.section_2_invention_summary.known_mechanism.content
.section_11_prototype_test_plan.items[1].source_basis
.section_11_prototype_test_plan.items[1].traceability.content
._session_meta.evidence_registry[1].content
```

**§3.3 Why it is materially unsafe.** The product proposes physical prototype experiments against a
mechanism the inventor has explicitly disowned.

**§3.4 The mitigations that DO hold, credited so the defect is not overstated [EXEC].**
`deliverable_eligible = False`; `derived_verified_ready = False`; all four acknowledged unknowns are
surfaced in the package; a readiness caveat is rendered. **This is a truthfulness-of-basis defect, not a
false-readiness defect**, and R4 must not be argued as though the product currently claims verified
readiness. It does not.

**§3.5 A false signal, disclosed rather than relied on [EXEC].** A substring search of the assembled
package matches the token `contradicted`. Isolating it shows generic readiness boilerplate — *"recorded
supporting evidence remains unvalidated, provisional, pending, or contradicted"* — which is **not** a
statement about this mechanism. **There is no withdrawal, retraction or supersession marker anywhere in
the package.** Any R4-I evidence that relies on a substring match for a withdrawal marker is invalid.

**§3.6 The problem must not be broadened [OWNER: OD-R4-05].** R4 closes exactly §3.1. It does not become
general contradiction reasoning, conflict resolution, or truth arbitration.

---

## §4. WHAT IS **NOT** A DEFECT — negative diagnosis (equally binding)

R4-I must **not** treat any of the following as a defect to repair. Each was checked and found sound.

1. **R2's fail-closed refusal of the retraction is correct.** `"WARN — not addressed"` is the authorized
   behaviour: the retraction carries no registered surface for the served gap, so it may not influence
   that gap's satisfaction **[REPO]**. Making retraction punitive, or letting it bypass
   `addresses_gap`, is a **rejection condition**.
2. **R1 recording the retraction is correct.** It is preserved as an acknowledged unknown and in the
   append-only ledger **[EXEC]**.
3. **Recompute-on-read is a strength, not a staleness source.** No derived artifact is cached,
   snapshotted, versioned or persisted as authority; `keep-snapshot` explicitly *"NEVER
   serializes/duplicates/versions"* **[REPO]**. **There is no stale *output*. There is a stale
   *conclusion*.** R4-I must not invent an output-cache invalidation problem that does not exist.
4. **Determinism is intact.** Reload replays the accepted stream through unchanged `run_iteration`;
   Path-N bypasses the AI advisor, so no network, model or clock enters the path **[REPO]**.
5. **Bilingual behaviour is symmetric.** An EN correction and its AR counterpart produced identical
   state transitions and identical resulting state **[EXEC]**. **R3 holds across the correction seam**;
   there is no bilingual defect to repair, only a bilingual property to preserve (§13).
6. **Absence of versioning/sharing is not a defect.** Those capabilities are owned elsewhere and were
   explicitly not delivered by Phase 4 **[REPO]**.
7. **`REGRESSING` being unused is disclosed, not repaired.** `engine/idea_state.py` defines it and
   `engine/progression_loop.py` imports it; it is **never assigned** **[REPO]**. R4 does **not**
   authorize activating a regression direction axis.

---

## §5. THE R4 PRODUCT TRUTH (frozen by this contract)

> **When an inventor explicitly withdraws a previously accepted source input, the withdrawal is durably
> recorded without destroying history; the complete current project state is recomputed by full
> deterministic replay of the amended accepted-source stream; and no conclusion whose basis was
> withdrawn continues to be presented as current without being either removed by that replay or
> truthfully marked as resting on withdrawn material.**

Everything in §§6–15 is a constraint on realising exactly that sentence. Nothing wider is authorized.

---

## §6. USER CORRECTION SEMANTICS (binding)

**C-1 — Explicit and targeted-at-a-record, never inferred.** A correction MUST be an explicit user
action naming a **specific prior accepted source input** by its stable `record_id` **[OWNER: OD-R4-06]**.
It MUST NOT be inferred from wording, from retraction phrases, from sentiment, or from any semantic
classifier. "The user typed *actually I was wrong*" is **not** a correction and must never be treated as
one.

**C-2 — Non-destructive.** The prior record MUST NOT be deleted, overwritten, renumbered, or mutated.
This is not merely a policy: `record_interaction` *"never mutates an existing record and never removes
one"* **[REPO]**, and the durable store contains **no `UPDATE` statement at all** — `append_record`
issues a single `INSERT` **[REPO]**.

**C-3 — Forward-edge expression, because the store is INSERT-only.** Since no `UPDATE` path exists and
adding one would be a destructive-history hazard, the supersession relationship MUST be expressed on the
**new** record (`supersedes = [prior_record_id]`), with the inverse (`prior.superseded_by`) **derived
deterministically on load**. R4-I MUST NOT introduce an `UPDATE` to a persisted record in order to set
`superseded_by`.

**C-4 — The minting seam is a named residual.** `IdeaState.record_interaction` currently accepts
`action, content, gap_context, iteration, provenance, validation_status, quality, responsibility` and
**no `supersedes` argument** **[REPO]**. R4-I must extend the minting seam **additively and
backward-compatibly**, defaulting to today's behaviour when no correction is expressed.

**C-5 — Fail-closed.** A correction naming an unknown, already-superseded, or non-existent record, or
one that would create a supersession cycle, MUST be refused with **nothing stored and nothing
acknowledged**. The existing load-time validation already rejects unknown references, self-supersession
and cycles **[REPO]**; R4-I MUST NOT weaken it.

**C-6 — Persist-before-acknowledge.** A correction follows the proven answered-path shape: mint against
a throwaway view, commit durably with its own idempotency identity, and only then publish to live
memory. On any durable failure, live memory is unchanged and nothing is acknowledged **[REPO]**.

**C-7 — Idempotent.** Re-submitting the same correction (refresh, retry, double-submit) MUST produce no
second durable record, no second supersession edge, and no second replay.

**C-8 — Bounded free-text hardening applies** exactly as it does to the existing answered and
non-answer paths **[REPO]**.

---

## §7. SUPERSESSION WITH RETENTION (binding)

**S-1** The superseded record REMAINS in the durable stream and in the ledger, verbatim, forever.
Historical evidence remains auditable **[OWNER: OD-R4-06]**.

**S-2** `record_id` (`rec_N`) is never reused, renumbered, or re-minted. The existing max-based
derivation must be preserved **[REPO]**.

**S-3** The supersession graph remains **acyclic**, enforced both at mint time and on load **[REPO]**.

**S-4** A superseded record is **deactivated for current evaluation only** — the semantics already
implemented and already consumed by the five derived modules **[REPO]**. R4 introduces **no new
active-set concept**; it makes the existing one reachable.

**S-5 — No schema migration.** `contradicts`, `supersedes` and `superseded_by` are already in
`_ASSERTION_FIELDS`, already serialized losslessly into the row payload, and already validated on load
**[REPO]**. R4-I MUST NOT add a persistence column, table, migration, or datastore. This satisfies
**[OWNER: OD-R4-08]**'s prohibition on unrelated persistence redesign.

**S-6** Supersession is a relationship between **accepted source inputs**. It is **not** applied to
`Gap`, `Evidence`, `known_problem`, `known_mechanism`, or `maturity_level` — those are recomputed by
replay (§8), never edge-marked.

---

## §8. FULL DETERMINISTIC REPLAY, LIVE-STATE REPLACEMENT, AND PERMITTED DECREASE (binding)

**RP-1 — Full replay only [OWNER: OD-R4-03].** After an accepted correction, the complete current project
state MUST be recomputed by replaying the **entire amended accepted-source stream** — seed first, then
the active accepted answers in authoritative `seq` order — through the **unchanged**
`progression_loop.run_iteration`, exactly as `engine/session_reconstruction.py` already does **[REPO]**.

**RP-2 — Definition adopted verbatim from committed governance [REPO].** *"Full re-evaluation =
reconstructing complete current project state from accepted source inputs and running the full
deterministic logic to produce a new output bound to the exact inputs, invalidating stale outputs while
preserving prior outputs, and permitting readiness/evaluation to decrease. It is NOT re-reading cached
state or cached output, and it is NOT the current `derive_readiness` readiness re-derivation alone."*

**RP-3 — No targeted recomputation, no dependency graph.** Restated as a binding prohibition; see §2.4.

**RP-4 — Live-state replacement [OWNER: OD-R4-06].** The reconstructed result BECOMES the current live
state. R4-I MUST NOT reach into live state and adjust `gap.status`, `known_mechanism`, `known_problem`,
`maturity_level` or `current_stage` directly. **Every progression-state change must arrive through
replay.** Direct mutation is a rejection condition.

**RP-5 — Decrease is permitted and must be provable [OWNER: OD-R4-06].** Where the corrected stream no
longer supports a prior conclusion, gap status, maturity, readiness and evaluation MUST be free to be
**lower** than before. R4-I MUST demonstrate at least one measured case in which `maturity_level`,
`known_mechanism`, or a gap status is strictly weaker after replay than before the correction. A design
in which nothing can ever decrease does not satisfy this contract.

**RP-6 — Derived outputs recompose from the reconstructed state**, using the existing
recompute-on-read path. No new caching, snapshotting or output store is authorized.

**RP-7 — Prior outputs preserved, never overwritten** (`D-P4-05` clause 6) **[REPO]**.

**RP-8 — Determinism.** Identical amended streams MUST produce byte-identical state and byte-identical
assembled packages. No clock, randomness, network, model call or iteration-order dependence may enter
the replay path. Path-N already bypasses the AI advisor inside `run_iteration` **[REPO]**.

**RP-9 — Replay bound.** The existing replay limit (500) and its fail-closed boundary behaviour are
preserved; a correction must not become a way to exceed or disable it **[REPO]**.

---

## §9. DETERMINISTIC FAILURE AND ROLLBACK BEHAVIOUR (binding)

**F-1** If the durable append of a correction fails, **nothing** changes: no supersession edge, no
replay, no live-state change, no acknowledgement **[REPO]** (the proven answered-path shape).

**F-2** If replay fails after a correction has been durably committed, live state MUST NOT be left
partially replaced. R4-I MUST publish the reconstructed state **atomically** or not at all, exactly as
the answered path stages on a clone and publishes only after durable success **[REPO]**.

**F-3** A replay failure MUST fail closed and MUST NOT be reported as a successful correction, MUST NOT
produce a 500 or traceback to the user, and MUST NOT fabricate a reconstruction claim **[REPO]**.

**F-4** After any failure the durable stream remains valid and re-loadable; the next load must not raise
`ContractError` because of a half-written correction.

**F-5** "Rollback" here means **transactional rollback of a failed operation only**. It is **not** user
-facing undo, version rollback, or branch restoration — all out of scope (§2.3).

---

## §10. CLOSED-GAP SAFETY PRECONDITION (binding, and required BEFORE any reprocessing)

**§10.1 The hazard, measured [EXEC].** Called directly with an already-`CLOSED` gap,
`integrate_response` at `REASONED` quality falls to its `else` branch and overwrites `CLOSED` with
`PARTIAL` **while leaving `closed_at` set** — an impossible mixed state:

```
BEFORE: status=CLOSED   closed_at=0   evaluate_transition -> "PHYSICAL_FEASIBILITY not yet opened"
AFTER : status=PARTIAL  closed_at=0   evaluate_transition -> "MECHANISM_COMPLETENESS not yet closed"
INCONSISTENT PAIR (status == PARTIAL while closed_at is set): True
```

It fires on a **third identical answer** — no correction is required to trigger it.

**§10.2 It is NOT a live defect today, and this contract says so plainly [EXEC].**
`integrate_response` has exactly **one** runtime caller — inside `run_iteration` — whose `gap_type`
comes from `select_next_gap`, which returns only gaps with status in `(OPEN, PARTIAL)` **[REPO]**. **A
CLOSED gap is never re-served.** The runtime is protected by the caller's filter, **not** by
`integrate_response` itself. Driven through the runtime path, four retraction iterations moved no gap
backward **[EXEC]**.

**§10.3 The only dedicated INV-004 test is vacuous on its own corpus [EXEC].**
`tests/test_wps001_invariants.py::TestWPS001_INV004_GapLifecycle::test_closed_gap_does_not_reopen`
begins `if not closed: pytest.skip(...)`. Reproducing its exact five-input corpus, **no gap reaches
`CLOSED`**, so the test skips and its final assertion loop is vacuous. Driving gaps to `CLOSED` with a
stronger corpus, the invariant was verified to hold non-vacuously **[EXEC]** — but the committed test
does not establish it. This is the **T-1 / T-1b coverage-adequacy class** the R2/R3 lineage already
ruled binding **[REPO]**.

**§10.4 Binding requirements [OWNER: OD-R4-07].**

* **G-1** Before any correction capability can cause prior material to be reprocessed, `integrate_response`
  MUST be hardened so that an already-`CLOSED` gap can never end in `status = PARTIAL` with `closed_at`
  set. **The impossible mixed state must be unreachable by construction, not merely unreached.**
* **G-2** The fix MUST NOT be to let ordinary `CLOSED` gaps reopen through the normal forward-answer
  path. **WPS-001 INV-004 and the ordinary forward-only journey are preserved unchanged.**
* **G-3** Replay is the authorized way a gap may legitimately end in a weaker status: replay starts from
  a **fresh** `IdeaState` and rebuilds forward, so no gap ever moves backward **within** a run. The
  weaker outcome is a property of the *new* run, not a backward transition in the old one. R4-I MUST
  state this distinction explicitly in its evidence.
* **G-4** `closed_at` MUST be consistent with `status` in every reachable state: set if and only if the
  gap is `CLOSED`.
* **G-5 — Non-vacuous regression coverage is mandatory.** R4-I MUST commit an INV-004 test that
  **provably reaches `CLOSED`** (no skip, no vacuous `all()` over an empty set) and then asserts the
  invariant, plus an explicit `closed_at`/`status` consistency assertion. R4-I MUST report the corpus it
  used and demonstrate that the test **fails** if the guard is removed.

---

## §11. R1 PRESERVATION (binding) [OWNER: OD-R4-10]

`PVCG-R1 — Durable Epistemic Memory` is authoritative (PR #547) **[REPO]**.

* The five governed non-answer dispositions (`unknown`, `deferred`, `provisional_assumption`,
  `specialist_requested`, `evidence_requested`) MUST keep persisting and reconstructing with their
  recorded meaning **[REPO]**.
* The ledger remains **append-only and non-destructive**. A correction is an **append**, never a delete.
* `tests/test_pvcg_r1_durable_epistemic_memory.py` MUST remain **byte-unchanged**, and the R1 focused
  suite MUST be reported GREEN on the exact frozen R4-I candidate.
* No change to `engine/record_contract.py` `_ASSERTION_FIELDS` **semantics**, no schema change, no
  migration (§7 S-5).
* Reconstruction MUST continue to restore the **full** durable ledger verbatim — including the non-answer
  dispositions — as it does today **[REPO]**; a correction must not cause any disposition to be dropped
  from the restored ledger.

**Rejection conditions:** any destructive edit, removal, renumbering or reuse of `rec_N`; dropping
non-answer dispositions from the amended stream; editing the R1 test file.

---

## §12. R2 PRESERVATION (binding) [OWNER: OD-R4-10]

R2 is authoritatively closed **[REPO]**. R4 sits on top of it.

* **Fail-closed relevance is intact.** An answer — corrective or not — that does not address the served
  gap may not influence that gap's satisfaction, no matter how much generic technical substance, domain
  vocabulary or causal language it carries **[REPO]**. A correction MUST NOT bypass `addresses_gap`.
* **Correction is never punitive.** Ineligibility never becomes `BLOCK`, a contradiction, or an
  input-validation failure; the answer is still recorded and its assessed quality is unchanged
  **[REPO]**. A refused or ineligible correction MUST return the existing non-punitive shape.
* **Repetition cannot manufacture closure**, proven by
  `tests/test_pvcg_r2i_gap_relevance.py::TestRed3RepetitionCannotManufactureSatisfaction::test_five_repetitions_of_an_irrelevant_answer_never_close`
  and non-punitiveness by `::TestFailClosedIsNotPunitive::test_irrelevant_answer_never_returns_block`
  **[REPO]**. Repeated corrections MUST NOT become an accumulation channel that manufactures
  progression.
* The R2 behavioural suite and the R2 marker-coverage suite MUST be reported GREEN on the frozen
  candidate, and R4-I MUST state explicitly whether either file changed and why.
* The English marker tables MUST NOT be reopened (R2-C §14) **[REPO]**.

---

## §13. R3 PRESERVATION AND EN/AR CORRECTION EQUIVALENCE (binding) [OWNER: OD-R4-10]

`PVCG-R3` is formally closed and authoritative (PR #553) **[REPO]**.

* **E-1 — Correction must be bilingual and deterministic.** The correction affordance, its refusal
  behaviour, its withdrawal marker, and the resulting replayed state MUST be **equivalent for English
  and Arabic** over registered surfaces, proven by R3-style paired tests. A language-asymmetric
  correction path is a **rejection condition**.
* **E-2 — Measured baseline [EXEC].** At the base tip, an EN correction and its faithful AR counterpart
  produced identical transitions and identical resulting state. **R4-I must not worsen this, and must
  state truthfully whether it changes.**
* **E-3 — No widening.** R4 registers no new concept, surface, causal marker or acknowledged-unknown
  surface, and does not widen English while touching Arabic (R3-C N-3) **[REPO]**.
* **E-4 — The declared R3 bound is unchanged.** Unregistered wording in either language remains
  not governed-equivalent. A correction expressed in unregistered wording is governed by that same bound
  — which is precisely why **C-1** requires an explicit record-targeted action rather than semantic
  detection of retraction language.
* **E-5 — Zero pin and pack drift.** See §16.

---

## §14. PERSISTENCE AND RELOAD BEHAVIOUR (binding)

**P-1** Only the `answered` subset is loaded as accepted-answer evidence for replay **[REPO]**; the full
ledger is separately restored verbatim **[REPO]**. R4-I MUST preserve both behaviours and MUST state
which stream a correction joins.

**P-2** After a correction and a process restart, reload MUST reproduce the **corrected** state, not the
pre-correction state, and MUST do so deterministically.

**P-3** A superseded record MUST remain durably present after reload and MUST remain excluded from the
active set — proven, not assumed.

**P-4** Load-time validation (unknown references, self-supersession, cycles) MUST remain in force and
MUST NOT be relaxed to accommodate corrections **[REPO]**.

**P-5** The cold-load and read-only reconstruction paths MUST continue to fail closed exactly as today
(Level-0 fallback, `ContractError`, replay-limit, store unavailability) — never a 500, never a false
reconstruction claim **[REPO]**.

**P-6** No new durable artifact, column, table, index, migration or datastore (§7 S-5).

---

## §15. TRUTHFUL WITHDRAWAL MARKER AND STALE-BASIS HANDLING (binding)

**M-1 — Where replay removes the conclusion, no marker is owed.** If the amended stream no longer
produces the conclusion, the truthful outcome is its absence. R4 does **not** require a marker for
material that replay has already removed.

**M-2 — Where material legitimately survives replay but rests on withdrawn input, it MUST be marked.**
The marker MUST be explicit, MUST identify that a prior basis was withdrawn, and MUST NOT be inferable
only from generic boilerplate (§3.5).

**M-3 — Surface-and-retain is the established idiom, and R4 follows it.** The repository already
implements two staleness mechanisms of exactly this shape — `stale_criteria` with its notice, and
`stale_criticality_confirmations` counts — both of which **surface and retain**, never delete **[REPO]**.
R4-I MUST consume this idiom rather than invent a third.

**M-4 — Truthfulness ceiling.** The marker states only what is known: that an identified prior input was
withdrawn by the inventor. It MUST NOT assert that the conclusion is false, that a contradiction exists,
or that any engineering judgement has been made.

**M-5 — Bilingual.** The marker is subject to §13 E-1.

**M-6 — The four demonstrated locations are the minimum evidence surface.** R4-I MUST show, for the §3.2
scenario, what happens at each of the four locations measured there — by removal via replay (M-1) or by
marker (M-2). A design that leaves any of them silently presenting withdrawn material as current fails
this contract.

---

## §16. PIN, PACK AND DOMAIN-NEUTRALITY IMPACT ANALYSIS (binding)

Measured at the base SHA **[REPO]** / **[EXEC]**:

| File | Live digest / state | Pinned in |
|---|---|---|
| `engine/progression_loop.py` | `3cbd76849c0f572191a552db1a41a8cd418d02fac1d59d9b8804c72883239a55` | **3 ENFORCING** locations: `tests/test_p9_mech_i3_signal_quality.py`, `tests/test_p9_mech_i4_boundary_corpus.py`, `tests/test_p9_mech_i5_question_sufficiency.py` |
| `engine/domain_rules.py` | `0e47326ad92a6e5b0a63eb06db9e3ad96ae72c9aaf64471dd21621265b1db1ab` | the same 3 files |
| `engine/path_n_questions.py` | `a1a682d38293defd4b351e6238aeb870b4f765eaf3fc0f105c4932f75286ce7f` | I5 |
| all five `domains/*/domain.json` | `_FROZEN_PACK_SHA256` in I3/I4 | I3 pins 4, I4 pins all 5 |

**§16.1 Pack and domain-rule drift: PROHIBITED.** `PACK DELTA: 0`. `engine/domain_rules.py` and
`engine/path_n_questions.py` MUST be **byte-identical**. No domain pack, no new gap type, no scoring
change, no domain activation change. Correction semantics MUST be **domain-neutral**: nothing in the
correction path may branch on the confirmed domain.

**§16.2 Pin movement.** `engine/progression_loop.py` is pinned in three ENFORCING locations. **§10's
`CLOSED`-gap guard lands in that file**, so R4-I will move that digest. This is disclosed here in
advance rather than discovered at review. If and only if the guard is implemented, R4-I MUST perform pin
reconciliation **exactly** as `PVCG_R3_C_SEMANTIC_STABILITY_CONTRACT.md` §13.2a specifies — updating the
three **ENFORCING** locations, synchronizing **ACTIVE CURRENT-TRUTH** governance surfaces, and leaving
**HISTORICAL append-only** records unrewritten **[REPO]**. **No other pin may move.** A candidate that
moves a pin without that disclosed reconciliation is rejected.

**§16.3** No `benchmark/`, evidence-tree, generator, CI, deployment or Render path may be touched.

---

## §17. REQUIRED PVCG-R4-I RED / GREEN SHAPE (binding)

**RED first, on the authoritative base, before any source change.** R4-I MUST commit tests that are
**demonstrably RED at the base tip** for at least:

1. an explicit correction of a named prior accepted record is expressible and durably recorded;
2. the superseded record is retained and excluded from the active set;
3. full replay of the amended stream replaces live state;
4. a conclusion whose basis was withdrawn is no longer presented as current, or is marked (§15 M-6);
5. `maturity_level` / gap status / `known_mechanism` **decreases** in at least one measured case (§8 RP-5);
6. the `CLOSED`-gap guard: the impossible `PARTIAL` + `closed_at` state is unreachable (§10 G-1, G-5);
7. a non-vacuous INV-004 test that provably reaches `CLOSED` (§10 G-5);
8. EN/AR correction equivalence (§13 E-1);
9. reload after correction reproduces the corrected state (§14 P-2);
10. a malformed / unknown-record / cycle-forming correction stores nothing (§6 C-5);
11. correction idempotency (§6 C-7);
12. replay determinism: identical amended streams produce byte-identical state and package (§8 RP-8).

**GREEN.** Every item above passes; R1 26/26 with its file byte-unchanged; the R2 behavioural and marker
suites GREEN; the R3 focused suite GREEN; the three P9 pin suites GREEN under §16.2 reconciliation;
universal guardrail smoke PASS; full suite reconciled per §20.

**Coverage adequacy — the T-1 / T-1b lesson is binding [REPO].** Probes MUST NOT be derived from the
object under test. Any corpus-dependent assertion MUST be shown non-vacuous. A mutation or
guard-removal check MUST be reported for the §10 guard. A finite corpus never establishes equivalence.

---

## §18. NEGATIVE CONTROLS (binding — "correction" must not become "anything can change anything")

1. **A non-correction answer changes nothing about supersession.** Ordinary answers must behave exactly
   as today; no supersession edge may appear spontaneously.
2. **Retraction *language* alone is inert.** "Actually I was wrong" with no explicit correction action
   must produce today's behaviour exactly (recorded, `WARN`, nothing invalidated) — proving §6 C-1.
3. **A correction cannot close a gap it does not address.** R2 fail-closed relevance still governs.
4. **A correction cannot raise anything it should not.** Correction must not be usable to manufacture
   satisfaction, closure, maturity, or readiness.
5. **Repeated corrections do not accumulate progression.** §12.
6. **A correction naming a foreign project's record is refused**, with project-scoped isolation intact
   and no cross-project disclosure **[REPO]**.
7. **An unregistered-wording correction in either language gains nothing** — the declared R3 bound holds
   (§13 E-4).
8. **No ordinary CLOSED gap reopens through the forward path** (§10 G-2).
9. **Replay with no correction is a fixed point:** replaying an unamended stream must reproduce the
   identical state.

---

## §19. EXPLICIT NON-GOALS AND PROHIBITIONS — NOT AUTHORIZED BY THIS CONTRACT

**§19.1 Prohibited (authoritatively forbidden — §2.4).** Targeted / partial / selective re-evaluation;
any dependency graph or propagation model; a full contradiction engine; free-form semantic contradiction
detection; a semantic conflict graph; probabilistic contradiction reasoning; LLM truth arbitration;
autonomous intent inference; cross-project contradiction analysis; destructive deletion or mutation of
accepted-source history; reopening ordinary CLOSED gaps through the forward path.

**§19.2 Out of scope.** Versioning, branching, rollback, user-facing undo; sharing, permissions,
recipient identity, access revocation; PDF, Email; durable output records and source→output binding;
the in-session "What changed?" UX increment; domain expansion; new gap types; scoring changes; WS17;
**TDVP**; deployment.

**§19.3 No downstream activation.** Nothing here opens FPC-01, FPC-03, FPC-04, Phase 5–7, STG, ACV, or
any successor gate. Naming a workstream authorizes nothing.

**§19.4 A recorded governance discrepancy, disclosed and NOT silently rewritten [REPO] / [OPEN].**
`PVCG_R2_C_GAP_RELEVANCE_HARDENING_CONTRACT.md` §5 lists *"a full **contradiction engine** (PVCG-R4)"*,
equating R4 with a contradiction engine, while `PVCG_R3_C_SEMANTIC_STABILITY_CONTRACT.md` §17 lists
*"**PVCG-R4** (user correction / deterministic invalidation) and any contradiction engine"*, treating
the engine as **additional to** R4. **[OWNER: OD-R4-04] rules that the older R2 framing is
historical/ambiguous and does not govern this contract.** Per the same ruling, **no historical record is
rewritten**: `PVCG_R2_C` is untouched by this candidate. This section is the bounded current-truth
clarification. Whether a formal supersession statement should be recorded in a later governance gate
remains **[OPEN]**.

---

## §20. FULL-SUITE RECONCILIATION RULE (binding on PVCG-R4-I)

R4-I MUST report the full suite on its own frozen candidate under a declared environment precondition,
and MUST reconcile the count explicitly: `baseline + <new tests> = <total>`, naming which files
contributed. An unexplained delta in either direction is a rejection condition. R4-I MUST NOT inherit or
carry forward a suite figure measured on an earlier lineage without stating the carry-over argument and
why it holds.

---

## §21. CLOSURE CRITERIA FOR PVCG-R4

R4 is closable only when **all** hold:

1. **R4-C is authoritative** (merged, post-merge verified);
2. **R4-I is Owner-authorized separately**, implemented, independently reviewed, Owner-accepted, merged
   and post-merge verified;
3. the §3.1 defect is closed and demonstrated closed on the §3.2 scenario, with all four locations of
   §3.2 dispositioned per §15 M-6;
4. every §6 correction-semantics requirement (C-1…C-8) proven;
5. every §7 supersession-with-retention requirement (S-1…S-6) proven, **with no schema migration**;
6. every §8 replay requirement (RP-1…RP-9) proven, **including at least one measured decrease** (RP-5)
   and byte-identical determinism (RP-8);
7. every §9 failure/rollback requirement (F-1…F-5) proven;
8. the §10 `CLOSED`-gap guard implemented (G-1…G-4) **and** non-vacuous INV-004 coverage committed (G-5);
9. §11 R1, §12 R2 and §13 R3 preservation all proven, with the R1 test file byte-unchanged and EN/AR
   correction equivalence demonstrated;
10. §14 persistence/reload behaviour (P-1…P-6) proven;
11. §16 satisfied: `PACK DELTA: 0`, `domain_rules.py` and `path_n_questions.py` byte-identical, and any
    `progression_loop.py` pin movement reconciled exactly per R3-C §13.2a in all three ENFORCING
    locations;
12. every §18 negative control holding;
13. universal guardrail smoke PASS and the full suite reconciled per §20;
14. every residual stated truthfully as a known bound, not concealed;
15. **a formal closure record merged**, exactly as R2 and R3 required.

**Closing R4 closes only R4.** It does not satisfy PVCG, does not establish or freeze the Minimum
Launch-Conformance Set, and authorizes no deployment.

**PVCG relationship [OWNER: OD-R4-09].** `PVCG-R4 REQUIRED BEFORE PVCG SATISFIED: YES`.
`FULL REPOSITORY-DEFINED MLC ESTABLISHED BY THIS DECISION: NO` — the full MLC definition and
classification remain a later PVCG-final reconciliation task. Consistent with `PVCG_R3_C` §1.2, **no
committed document defines PVCG or enumerates the Minimum Launch-Conformance Set** **[REPO]**, so R4's
membership in that Set is **[OWNER]**, not **[REPO]**, and this contract classifies it that way.

---

## §22. STATUS LEDGER PRESERVED BY THIS GATE

```
PVCG-R1 AUTHORITATIVE: YES
PVCG-R2 AUTHORITATIVELY CLOSED: YES
PVCG-R3-C AUTHORITATIVE: YES
PVCG-R3-I AUTHORITATIVE: YES
PVCG-R3 FORMALLY CLOSED: YES
PVCG-R4-C CONTRACT CANDIDATE: FROZEN / NOT AUTHORITATIVE UNTIL MERGED
PVCG-R4 IMPLEMENTATION STARTED: NO
FPC-02 / P4-2 REMAINS IMPLEMENTATION OWNER: YES
TARGETED PARTIAL INVALIDATION AUTHORIZED: NO
DEPENDENCY GRAPH AUTHORIZED: NO
FULL CONTRADICTION ENGINE AUTHORIZED: NO
PHASE 4 REOPENED GENERALLY: NO
VERSIONING / BRANCHING / ROLLBACK / SHARING AUTHORIZED: NO
PERSISTENCE SCHEMA MIGRATION AUTHORIZED: NO
FULL ADAPTIVE QUESTIONING ACTIVATED: NO
LLM/NLP SUBSYSTEM ADDED: NO
EMBEDDINGS ADDED: NO
EXTERNAL NLP SERVICE ADDED: NO
PROBABILISTIC SEMANTIC CLASSIFIER ADDED: NO
RUNTIME MODIFIED: NO
TESTS MODIFIED: NO
PACK / DOMAIN-RULE DRIFT: NO
PIN MOVED BY THIS CANDIDATE: NO
RENDER REOPENED: NO
MAIN RECONCILIATION STARTED: NO
TDVP IMPLEMENTATION STARTED: NO
PVCG SATISFIED: NO
FULL MLC DEFINITION FROZEN: NO
MINIMUM LAUNCH-CONFORMANCE SET SATISFIED: NO
DEPLOYMENT AUTHORIZED: NO
```

WS10, WS11 and WS12 remain dormant and unwired; no LLM or NLP subsystem exists; the six governed gap
types remain frozen in the engine; no domain is activated, recognised differently, or re-scoped.

**§22.1 Phase 4 [OWNER: OD-R4-08].** Phase 4 remains **FORMALLY CLOSED within its previously implemented
boundary** **[REPO]**. This gate does **not** reopen Phase 4 generally. The Owner has authorized a
**narrowly bounded post-closure P4-2 extension** solely because repository authority already assigned
FPC-02's missing revision / stale-output implementation obligation to P4-2, limited to the
implementation necessary for the R4 conformance obligation — and **not** other Phase 4 deferred items,
broad durable-output redesign, versioning, branching, rollback, sharing, unrelated persistence redesign,
or infrastructure changes.

---

## §23. REVIEW PATH AND EVIDENCE PROVENANCE

LEVEL 2 governance-only under the LEAN §5B risk-based review model. **Zero executable bytes change in
this candidate** — expected `RUNTIME DELTA: 0`, `TEST DELTA: 0`, `PACK DELTA: 0`, `PIN DELTA: 0` — so
§5B.1's full-suite Creator-evidence trigger is not met by an implementation change.

**Full-suite provenance, stated without back-dating.** The Creator **did not execute any test suite for
this candidate**, and nothing in this record may be read as claiming otherwise. The container has
Python 3.11.15 but **neither `pytest` nor `flask`** **[EXEC]**, so the §18-class execution precondition
used by R3-I is **not satisfied here**. This is a **Creator-environment limitation** — it is not a
product defect, not a governance defect, and not a failure of any criterion — and it is recorded rather
than worked around. **PVCG-R4-I must measure everything independently on its own frozen state (§20).**

**Every [EXEC] finding** in §3, §4, §10 and §13 was produced by read-only `python3` probes against
`engine/` at the base tree that modified no repository file and added no fixture. A reviewer should
**re-measure them independently** rather than accept them as repository fact. Specifically re-measurable:
the §3.2 end-to-end scenario and its four deliverable locations; the §3.5 false-positive disclosure; the
§10.1 impossible mixed state and its §10.2 unreachability; the §10.3 vacuous-skip reproduction; and the
§13 E-2 EN/AR parity result.

**Independent-review scope for this candidate (bounded, per protocol §5):**
(1) Does this contract create a parallel implementation model, or does it consume FPC-02/P4-2?
(2) Is targeted partial invalidation excluded everywhere, including by implication?
(3) Is a contradiction engine excluded everywhere, including by implication?
(4) Is any history-destructive operation authorized anywhere?
(5) Are R1, R2 and R3 protections complete and correctly cited?
(6) Is Phase 4 reopened beyond OD-R4-08's bounded extension?
(7) Is any claim unsupported by its cited location?
(8) Is any closure criterion unverifiable as written?
