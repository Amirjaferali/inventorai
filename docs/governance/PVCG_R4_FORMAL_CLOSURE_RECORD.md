# PVCG-R4 — User Correction and Deterministic Invalidation — FORMAL CLOSURE RECORD (Candidate)

**Status of THIS record:** governance/documentation-only **FORMAL CLOSURE RECORD CANDIDATE**. It
implements nothing, changes no runtime, test, fixture, pack, registry, generator, evidence, schema or
persistence file, and closes NOTHING beyond PVCG-R4. **The closure statements in §8 become authoritative
ONLY if/when this exact candidate is merged and post-merge verified** through the governed lifecycle.
**`OWNER_DECISION_REGISTER.md` UNCHANGED** — closure-gate convention: no new Owner decision is required
merely to close an already-accepted, already-merged implementation.

**This record does NOT deliver rendered correction UX, does not open any successor gate, and does not
start TDVP.**

**Why this record exists.** `PVCG_R4_C_USER_CORRECTION_AND_DETERMINISTIC_INVALIDATION_CONTRACT.md`
(AUTHORITATIVE, merged PR #554) §21 lists fifteen criteria and requires as criterion **15** *"**a formal
closure record merged**, exactly as R2 and R3 required."* **`CLOSURE REQUIRED BY CONTRACT: YES`.** R4 is
therefore NOT closed by the R4-I implementation merge alone. This is the required instrument, following
the `<GATE>_FORMAL_CLOSURE_RECORD.md` convention set by `PVCG_R2_FORMAL_CLOSURE_RECORD.md` and
`PVCG_R3_FORMAL_CLOSURE_RECORD.md`.

---

## §1. Closure basis — the authoritative R4-I merge, verified live

Live tip re-fetched from `origin/feature/atomic-json-session-persistence` this gate and independently
verified — not assumed, not copied from a directive:

| Fact | Verified value | Method |
|---|---|---|
| Live tip | `5ed09180c7b3bc1809785ed425d4820d5ffc71b7` | `git fetch` + `git rev-parse origin/…` |
| Commits after the tip | **0** | `git rev-list --count` |
| Working tree | clean | `git status --porcelain` empty |

**PVCG-R4-I merge (PR #555)** — `git cat-file -p 5ed09180`:

```
tree   506b2dd4a8994ced79ada0215e0f389db92b4e53   PASS
parent c3d9e2d98ba7b6c9b3a9d9d316e6d572122d8a8e   PASS  (first parent / prior authoritative base)
parent 2bb472a07f9ac9177070c131c5c7f13ee3cd718a   PASS  (second parent / exact Owner-accepted candidate)
accepted candidate tree : 506b2dd4a8994ced79ada0215e0f389db92b4e53   == merge tree
candidate -> merge diff : EMPTY                   PASS
git diff --check        : PASS
subject                 : Merge pull request #555 from Amirjaferali/pvcg-r4i-publish-2bb472a0
```

`PVCG-R4-C AUTHORITATIVE: YES` — merged PR #554, merge `c3d9e2d98ba7b6c9b3a9d9d316e6d572122d8a8e`,
first parent `18a90f9b…`, second parent `d5286de7…` (the exact Owner-accepted R4-C candidate), merge
tree `968ff38c…`, empty candidate→merge diff; both `c3d9e2d9…` and the R3-closure merge `18a90f9b…` are
confirmed ancestors of the live tip — re-verified from repository lineage this gate.

---

## §2. Governed review and acceptance lineage (all SHAs preserved, none rewritten)

| SHA | Disposition |
|---|---|
| `c03386dfd301b1a63d751422ea53a477a68173b3` | **REJECTED BY THE CREATOR'S OWN GRILL** on **CG-1** (EN/AR asymmetry at the actual render path); preserved unchanged, never published |
| `4dc7c3290a8bf9b72a87ad017e1e94181f6b9799` | Independent External Review: **ACCEPT WITH NON-BLOCKING OBSERVATIONS**; `UNSUPPORTED MATERIAL CLAIMS = 0`; `SAFE FOR OWNER EXACT-SHA ACCEPTANCE: YES`; observations **NB-1 … NB-4**. Owner withheld acceptance pending a bounded child |
| `fc45d029926d7842bbea5440339c4bac9625613a` | NB-1 / NB-2 microrepair. Ultra-focused Independent Review: **ACCEPT WITH NON-BLOCKING OBSERVATIONS**; `UNSUPPORTED MATERIAL CLAIMS = 0`; `SAFE FOR OWNER EXACT-SHA ACCEPTANCE: YES`. Owner withheld acceptance pending a final microgate |
| `2bb472a07f9ac9177070c131c5c7f13ee3cd718a` | **Owner-accepted exact SHA**, merged via **PR #555** → `5ed09180…` |

No candidate was amended, rebased, squashed or recreated at any point in this lineage. Every rejected
and superseded SHA remains immutable evidence.

---

## §3. Defect dispositions

| ID | Class | Disposition |
|---|---|---|
| **CG-1** | CREATOR-GRILL REJECT (EN/AR) | **CLOSED.** All three correction messages were registered in `_MESSAGE_KEYS`, which serves `localize_message` — but `show_session` renders `_interaction_ack` through `localize_deep`, a DIFFERENT map, so the success acknowledgement reached an Arabic reader in English while a test exercising only `localize_message` passed. Repaired by registering it in `_DEEP_AR`, and by replacing the convenient test with two that exercise the real path, including end-to-end through the live client. |
| **NB-1** | NON-BLOCKING (user-facing truthfulness) | **CLOSED, in two stages.** The post-durable replay-failure path said *"Nothing was changed"*, which is false once the append has committed. Stage one replaced it with a dedicated message. The ultra-focused review then proved the replacement's *"will be applied the next time this project loads"* is itself false at the replay-bound crossing; stage two made the clause **conditional**. |
| **NB-2** | NON-BLOCKING (security parity) | **CLOSED.** `POST /session/<sid>/correct` mutates accepted durable state but did not take the `answer_token` its closest functional peer `submit_answer` requires. It now takes the SAME token through the SAME canonical `_valid_answer_token`, validated FIRST in the route — before parsing, minting, the durable append and the replay. |
| **NB-3** | NON-BLOCKING | **NOT ADDRESSED — deliberately.** Outside the Owner-authorized repair scope for every child in this lineage. Carried forward openly (§7). |
| **NB-4** | NON-BLOCKING | **NOT ADDRESSED — deliberately.** Same. Carried forward openly (§7). |

---

## §4. USER REACHABILITY — the material distinction, stated without softening

This section is binding on every later reader and summary.

```
R4 correction mechanism / explicit route : IMPLEMENTED
Rendered correction UX                   : NOT DELIVERED IN THIS GATE
Rendered correction UX remains deferred to: Phase-3C / FPC-02
```

**What IS delivered.** `POST /session/<sid>/correct` — an explicit, record-targeted correction endpoint
carrying the canonical `answer_token`, guarded by `_project_authorized`, fail-closed on every invalid
input, and driving durable supersession plus full deterministic replay. It is reachable by an HTTP
client. **It is NOT reachable by clicking anything in the product.**

**What is NOT delivered.** No form, no template, no button, no link. `web/templates/` is byte-unchanged
across the entire R4-I lineage **[EXEC]**. **No statement anywhere may claim that users can now correct
prior answers through the product UI.** Until the deferred UX gate runs, an inventor using the product
normally cannot invoke this capability.

**Why that is contract-conformant rather than a shortfall — determined from authoritative text, each
clause verified verbatim in the merged contract [REPO]:**

| Clause | Text | Force |
|---|---|---|
| §2.2 R4-RES-1 | *"No **route, form, template or API** accepts a correction"* | the residual is **disjunctive**, so a route closes it |
| §17 RED item 1 | *"an explicit correction of a named prior accepted record is **expressible** and durably recorded"* | expressible, **not** rendered |
| §2.5 DEFERRED | *"presentation increment (**Phase-3C / FPC-02**, a UX gate of its own)"* | the UX increment is deferred to another gate |
| §19.2 Out of scope | *"the in-session 'What changed?' UX increment"* | explicitly out of scope for R4 |
| §21 | no criterion names rendered / template / affordance / user interface | no closure criterion requires UI |
| §13 E-1 | *"The correction **affordance** … MUST be **equivalent for English and Arabic**"* | constrains whatever affordance exists; does not create a rendered-UI requirement |

The contract additionally has **no** user-visible-behaviour section, unlike `PVCG_R3_C` §8. Seven
committed tests in `tests/test_pvcg_r4i_correction_and_invalidation.py::TestUserReachabilityClassificationA`
pin this reading to the contract text so it cannot be silently re-interpreted.

**Owner-facing consequence, stated plainly.** Closing R4 does **not** put correction in an inventor's
hands. It makes correction exist, correct, durable, deterministic and truthful. Putting it in their
hands is the deferred Phase-3C / FPC-02 UX gate, which remains **NOT STARTED / NOT AUTHORIZED**.

---

## §5. Closure criteria — `PVCG_R4_C…CONTRACT.md` §21, item by item

Every figure below was **re-measured on the merged tree `5ed09180…` this gate** unless the row says
otherwise. Test locations are in `tests/test_pvcg_r4i_correction_and_invalidation.py` unless named.

| # | Criterion | Status | Basis |
|---|---|---|---|
| 1 | R4-C authoritative (merged, post-merge verified) | **MET** | PR #554, merge `c3d9e2d9…`, tree `968ff38c…` == candidate tree, empty candidate→merge diff; ancestor of the live tip — re-verified §1 |
| 2 | R4-I Owner-authorized, implemented, independently reviewed, Owner-accepted, merged, post-merge verified | **MET** | §2 lineage; two independent reviews, both ACCEPT WITH NON-BLOCKING OBSERVATIONS / UMC 0; PR #555, merge `5ed09180…`, re-verified §1 |
| 3 | §3.1 defect closed and demonstrated on the §3.2 scenario, all four §3.2 locations dispositioned per §15 M-6 | **MET** | See **§5.1** — measured both halves live on the merged tree |
| 4 | every §6 correction-semantics requirement (C-1…C-8) proven | **MET** | `TestAExplicitCorrection` (C-1, C-5), `TestBSupersessionWithRetention` (C-2, C-3), `TestKR2PreservationAndNoInference::test_retraction_wording_alone_is_inert_without_an_explicit_action` (C-1 negative), `TestNB2CorrectionTokenParity` (C-6 ordering), `TestMDeterminism::test_resubmitting_the_same_correction_is_an_idempotent_no_op` (C-7); C-4 by the additive `supersedes=` seam in `engine/idea_state.py`; C-8 by the shared `_free_text_error` call |
| 5 | every §7 supersession-with-retention requirement (S-1…S-6) proven, **with no schema migration** | **MET** | `TestBSupersessionWithRetention` (S-1, S-2), `TestTNeutralityAndStructure` (S-3 acyclicity, S-5 derivation), `TestCPersistenceAndReload` (S-4 active set). **No migration:** `engine/record_store.py` is byte-unchanged across the whole R4-I lineage and contains no `UPDATE` statement **[EXEC]** |
| 6 | every §8 replay requirement (RP-1…RP-9) proven, **including a measured decrease** (RP-5) and byte-identical determinism (RP-8) | **MET** | `TestDFullReplay` (RP-1, RP-3), `TestEWithdrawnBasisAndDecrease::test_evaluation_is_free_to_decrease_after_a_withdrawal` (RP-5), `TestMDeterminism::test_identical_amended_streams_reconstruct_identically` (RP-8), `TestNB1cReplayBoundTruth::test_the_replay_bound_itself_is_untouched` (RP-9) |
| 7 | every §9 failure/rollback requirement (F-1…F-5) proven | **MET** | `TestIReplayFailureRollback` (F-2 by object identity, F-3, F-4 re-loadability); F-1 by the `StoreError` guard preceding any live change |
| 8 | §10 `CLOSED`-gap guard implemented (G-1…G-4) **and** non-vacuous INV-004 coverage committed (G-5) | **MET** | `TestNClosedGapGuard` (G-1, G-4), `TestOInv004NonVacuous` (G-5, with an explicit non-vacuity assertion that the corpus reaches `CLOSED` before the invariant is checked); G-2 by the untouched forward journey — `tests/test_wps001_invariants.py` **20 passed / 1 skipped**, file byte-unchanged |
| 9 | §11 R1, §12 R2, §13 R3 preservation, R1 test file byte-unchanged, EN/AR correction equivalence | **MET** | R1 **26 passed**, `tests/test_pvcg_r1_durable_epistemic_memory.py` byte-unchanged vs BOTH `18a90f9b…` and `c3d9e2d9…`; R2 **189** + **566 passed**, both files byte-unchanged; R3 **579 passed**, byte-unchanged; EN/AR by `TestJBilingualEquivalence` on the real render path |
| 10 | §14 persistence/reload behaviour (P-1…P-6) proven | **MET** | `TestCPersistenceAndReload` (P-2, P-3), `TestTNeutralityAndStructure` (P-4 validation not relaxed); P-6 by the byte-unchanged store |
| 11 | §16 satisfied: `PACK DELTA: 0`, `domain_rules.py` / `path_n_questions.py` byte-identical, pin movement reconciled per R3-C §13.2a in all three ENFORCING locations | **MET** | See **§6** |
| 12 | every §18 negative control holding | **MET** | Controls 1–9 mapped to committed tests, each re-run green this gate (§5.2) |
| 13 | universal guardrail smoke PASS and the full suite reconciled per §20 | **MET** | `UNIVERSAL GUARDRAIL SMOKE: PASS`; full suite **4418 passed / 3 skipped / 1 xfailed / 0 failed**; reconciliation **4355 + 63 = 4418** |
| 14 | every residual stated truthfully as a known bound, not concealed | **MET** | §7 — the replay-bound behaviour, NB-3/NB-4, the token semantics and the deferred UX are all recorded openly, none silently repaired |
| 15 | a formal closure record merged, exactly as R2 and R3 required | **PENDING — THIS RECORD**, effective only on merge and post-merge verification |

All fifteen criteria are resolved. Criteria 1–14 are MET and were **re-measured on the merged tree**,
not inherited. Criterion 15 is this record.

### §5.1 Criterion 3 — both halves, measured, with the distinction preserved

`PVCG_R4_C` §15 M-6 requires that, for the §3.2 scenario, each location be dispositioned *"by removal
via replay (M-1) or by marker (M-2)"*, and that no design *"leaves any of them **silently** presenting
withdrawn material as current"*.

**(A) The §3.2 scenario exactly as written** — strong causal answers, then retraction wording submitted
as ORDINARY answers. Measured on the merged tree **[EXEC]**: the material is still present and the
withdrawal marker reads **0**. **This is correct and is not the defect.** §6 C-1 forbids inferring a
correction from wording, so no withdrawal was ever expressed — nothing was withdrawn, therefore nothing
is "withdrawn material" being presented. A committed test
(`test_retraction_wording_alone_is_inert_without_an_explicit_action`) pins exactly this.

**(B) The same project, using the governed correction path.** Measured on the merged tree **[EXEC]**:
every field path carrying the withdrawn basis drops to **0**, and the marker reads **1** with its note
present — removal by replay (M-1) plus the truthful marker (M-2).

**A precision the contract did not anticipate, disclosed rather than smoothed over.** §3.2 recorded
**four** locations. A live re-measurement on the merged tree found **seven** distinct field paths
carrying the withdrawn basis for this scenario — the four §3.2 fields
(`section_2_invention_summary.known_mechanism`, `section_11_prototype_test_plan` `source_basis` and
`traceability.content`, `_session_meta.evidence_registry`) **plus three more**
(`section_13_requirement_landscape`, `section_14_validation_plan`,
`_session_meta.requirement_landscape_synthesis`). **All seven are cleared by replay**, so the criterion
is satisfied for a strict superset of what it named. The §3.2 count of four is **not** rewritten; it
remains the historical measurement of a different (retraction-style) corpus.

**§3.1 as written is closed:** *"A user who discovers that previously supplied accepted material was
wrong has no explicit way to withdraw that source material."* There is now an explicit way. §4 states
without softening what that way is and is not.

### §5.2 Criterion 12 — the §18 negative controls

| §18 control | Committed proof | Re-run |
|---|---|---|
| 1 — a non-correction answer changes nothing about supersession | `test_retraction_wording_alone_is_inert_without_an_explicit_action` | green |
| 2 — retraction wording alone is inert | same | green |
| 3 — a correction cannot close a gap it does not address | `test_an_irrelevant_correction_cannot_manufacture_closure` | green |
| 4 — a correction cannot raise anything it should not | same + `TestEWithdrawnBasisAndDecrease` | green |
| 5 — repeated corrections do not accumulate progression | `test_resubmitting_the_same_correction_is_an_idempotent_no_op` | green |
| 6 — a foreign-project record is refused, isolation intact | `test_unknown_or_already_superseded_target_stores_nothing`, `test_cross_session_token_fails_closed` | green |
| 7 — unregistered wording in either language gains nothing | R3 declared bound, `TestJBilingualEquivalence` | green |
| 8 — no ordinary CLOSED gap reopens through the forward path | `TestNClosedGapGuard`, `TestOInv004NonVacuous` | green |
| 9 — replay with no correction is a fixed point | `test_identical_amended_streams_reconstruct_identically` | green |

---

## §6. Pin, pack and domain-neutrality — criterion 11, verified on the merged tree

| File | Live digest on `5ed09180…` | Status |
|---|---|---|
| `engine/progression_loop.py` | `c268cd6380129170da19f3ba03158eebd9a5480711b43e39280e8ce9e74f63f8` | **RECONCILED BY PVCG-R4-I** — was `3cbd76849c0f572191a552db1a41a8cd418d02fac1d59d9b8804c72883239a55` |
| `engine/domain_rules.py` | `0e47326ad92a6e5b0a63eb06db9e3ad96ae72c9aaf64471dd21621265b1db1ab` | **byte-identical** |
| `engine/path_n_questions.py` | `a1a682d38293defd4b351e6238aeb870b4f765eaf3fc0f105c4932f75286ce7f` | **byte-identical** |
| all five `domains/*/domain.json` | `_FROZEN_PACK_SHA256` in I3/I4 | **byte-identical** — `PACK DELTA: 0` |

`git diff 18a90f9b 5ed09180 -- domains/ engine/domain_rules.py engine/path_n_questions.py` → **0 files
changed [EXEC]**.

**The pin movement was reconciled exactly per `PVCG_R3_C` §13.2a, and the reconciliation holds on the
merged tree [EXEC]:**

* **Kind (1) ENFORCING — all three carry the NEW digest and a disclosed note PRESERVING the prior one:**
  `tests/test_p9_mech_i3_signal_quality.py`, `tests/test_p9_mech_i4_boundary_corpus.py`,
  `tests/test_p9_mech_i5_question_sufficiency.py`. P9 pin suites **54 passed**.
* **Kind (2) ACTIVE CURRENT-TRUTH — synchronized:** the R4-C §16 table (the precedent by which R3-I
  synchronized R3-C §13), the roadmap gate entry, and the two status surfaces.
* **Kind (3) HISTORICAL — left byte-unchanged:** `PVCG_R3_C` §13, `PVCG_R3_FORMAL_CLOSURE_RECORD.md`
  §4, `PVCG_R2_C`, `PVCG_R2_FORMAL_CLOSURE_RECORD.md`, and the R3-I / R3-closure append-only roadmap
  gate entries.

The reason for the movement is disclosed and bounded: the §10.4 G-1 CLOSED-gap guard is **one branch**
in `integrate_response`. Question selection, gap priority, scoring thresholds, maturity, stall
behaviour, the six governed gap types and the ordinary forward-only journey are untouched.

---

## §7. Residuals and non-blocking observations carried forward — OPEN, NOT REPAIRED, NOT R5 AUTHORIZATION

None of the following appears in any of the fifteen §21 closure criteria, and none blocks this closure.
**Recording a residual here authorizes no work on it.**

* **The replay bound at `MAX_ACCEPTED_ANSWER_REPLAY = 500` — PRE-EXISTING, NOT REPAIRED.** A project
  already at the bound crosses it when a correction append takes the durable stream to limit + 1, after
  which **every** subsequent reconstruction raises `ReconstructionReplayLimitError` and the correction
  is never applied. Independently reproduced before any edit **[EXEC]**, and pinned by
  `TestNB1cReplayBoundTruth`. The bound is checked against the FULL persisted stream **on purpose**
  (§8 RP-9: a correction must never become a way to get UNDER the limit), so the behaviour is
  contract-correct. **The repair applied was to the MESSAGE, never to the bound**: the user-facing
  wording is conditional — *"The saved correction will be reflected whenever this project can be rebuilt
  successfully"* — which is true under both a transient replay failure and the bound crossing. The bound
  itself remains a **separately recorded pre-existing observation, unassigned by this gate**.
* **Stateless canonical answer-token semantics.** R4 reuses `_valid_answer_token` unchanged; its
  stateless HMAC design and single-use-for-acceptance lifecycle are pre-existing and untouched. Recorded,
  not repaired.
* **NB-3 and NB-4** from the Independent External Review of `4dc7c329…` — **NOT ADDRESSED**, outside
  every Owner-authorized repair scope in this lineage. They remain open, non-blocking observations.
* **Bundle extra-ref hygiene** — a review-process observation about transport artifacts, not a
  repository defect. Recorded, not repaired.
* **Rendered correction UX** — **NOT DELIVERED**; deferred to **Phase-3C / FPC-02**, which remains
  NOT STARTED / NOT AUTHORIZED (§4).
* **R3 residuals N-2 and U-4** — carried by `PVCG_R3_FORMAL_CLOSURE_RECORD.md` §6, which states
  explicitly that neither is PVCG-R4 authorization. They were not admitted to R4 and are not admitted
  to anything by this record.

---

## §8. Closure statements (authoritative ONLY if/when this candidate is merged and post-merge verified)

```
PVCG-R1 AUTHORITATIVE: YES
PVCG-R2 AUTHORITATIVELY CLOSED: YES
PVCG-R3 FORMALLY CLOSED: YES
PVCG-R4-C AUTHORITATIVE: YES
PVCG-R4-I AUTHORITATIVE: YES
PVCG-R4 FORMALLY CLOSED: YES
PVCG-R4 AUTHORITATIVELY SATISFIED: YES
FPC-02 / P4-2 REMAINS IMPLEMENTATION OWNER: YES
PVCG-R4 REMAINS CONFORMANCE OWNER ONLY: YES
RENDERED CORRECTION UX DELIVERED: NO
RENDERED CORRECTION UX OWNER: PHASE-3C / FPC-02 (NOT STARTED / NOT AUTHORIZED)
TARGETED PARTIAL INVALIDATION AUTHORIZED: NO
DEPENDENCY GRAPH ADDED: NO
FULL CONTRADICTION ENGINE AUTHORIZED: NO
SEMANTIC CORRECTION INFERENCE ADDED: NO
VERSIONING / BRANCHING / ROLLBACK / SHARING ADDED: NO
PERSISTENCE SCHEMA MIGRATION: NO
PHASE 4 REOPENED GENERALLY: NO
REPLAY BOUND REPAIRED: NO
FULL ADAPTIVE QUESTIONING ACTIVATED: NO
LLM/NLP SUBSYSTEM ADDED: NO
EMBEDDINGS ADDED: NO
TDVP IMPLEMENTATION STARTED: NO
PVCG SATISFIED: NO
FULL MLC DEFINITION FROZEN: NO
MINIMUM LAUNCH-CONFORMANCE SET SATISFIED: NO
DEPLOYMENT AUTHORIZED: NO
```

**Closing R4 closes ONLY R4.** It does not satisfy PVCG, does not establish or freeze the Minimum
Launch-Conformance Set, and authorizes no deployment — stated verbatim in the governing contract's §21
and repeated here without weakening. R1, R2, R3 and R4 are cumulative: closing R4 neither weakens nor
supersedes any of them.

**PVCG relationship [OWNER: OD-R4-09].** `PVCG-R4 REQUIRED BEFORE PVCG SATISFIED: YES`;
`FULL REPOSITORY-DEFINED MLC ESTABLISHED BY THIS DECISION: NO`. Consistent with `PVCG_R3_C` §1.2 and
`PVCG_R4_C` §21, **no committed document defines PVCG or enumerates the Minimum Launch-Conformance
Set** **[REPO]**, so R4's membership in that Set is **[OWNER]**, not **[REPO]**, and this record
classifies it that way. Whether the Set should be committed as its own document remains **[OPEN]**.

**No successor gate is opened by this record.** Naming Phase-3C / FPC-02, or any later PVCG lane,
authorizes nothing.

---

## §9. Evidence provenance, stated precisely

**Re-measured on the merged tree `5ed09180…` this gate [EXEC]:** focused R4-I **63 passed**; PVCG-R1
**26 passed**; R2 behavioural **189 passed**; R2 marker coverage **566 passed**; R3 focused **579
passed**; P9 pin suites **54 passed**; WPS-001 **20 passed / 1 skipped**;
`UNIVERSAL GUARDRAIL SMOKE: PASS`; full suite **4418 passed / 3 skipped / 1 xfailed / 0 failed**; the
§5.1 defect scenario in both halves; the four watched engine digests; and the three ENFORCING pin
locations. **Nothing in this record is a carried figure restated as fresh.**

**Execution precondition, declared.** All figures above were produced under Python 3.11.15, Flask
3.1.3, SQLite 3.45.1 and gunicorn 26.1.0 on `PATH` — the §18-class precondition the R3 lineage
declared. `pytest` is 9.1.1; the precondition does not pin a pytest version, and this is disclosed
rather than left implicit.

**§20 reconciliation, with the baseline's provenance stated exactly.** **4355 + 63 = 4418.**

* The **4418** total is a **fresh measurement on the merged tree `5ed09180…` this gate [EXEC]**.
* The **63** is a fresh measurement of `tests/test_pvcg_r4i_correction_and_invalidation.py`, the single
  new test file, on the same tree **[EXEC]**.
* The **4355** baseline was measured **on `c3d9e2d98ba7b6c9b3a9d9d316e6d572122d8a8e`** — the PVCG-R4-C
  merge tip — at the start of the PVCG-R4-I implementation gate **[EXEC]**. **It was NOT measured on the
  R3-closure merge `18a90f9b…`, and this record does not claim otherwise.** It carries back to
  `18a90f9b…` only by argument, not by measurement: PR #554 was **governance-documentation only**
  (`RUNTIME DELTA: 0`, `TEST DELTA: 0`), so it added no test between the two tips. That is the same
  carry-over discipline `PVCG_R3_C` §21 used, and it is stated here rather than left implicit.

No file other than the one new R4-I test file contributed a test.

---

## §10. Scope of this gate

Governance/documentation only — this new closure record plus one append-only roadmap entry and the two
status surfaces. No `engine/`, `web/`, `tests/`, `domains/`, `scripts/`, evidence-tree, generator,
deployment or Render path is touched; no pin moves (`PIN DELTA: 0`); `PACK DELTA: 0`; `main` is not
reconciled; and `OWNER_DECISION_REGISTER.md` is UNCHANGED.
