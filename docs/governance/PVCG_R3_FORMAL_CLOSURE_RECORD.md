# PVCG-R3 — Semantic Stability — FORMAL CLOSURE RECORD (Candidate)

**Status of THIS record:** governance/documentation-only **FORMAL CLOSURE RECORD CANDIDATE**. It
implements nothing, changes no runtime, test, fixture, pack, registry, generator, evidence, schema or
persistence file, and closes NOTHING beyond PVCG-R3. **The closure statements in §7 become authoritative
ONLY if/when this exact candidate is merged and post-merge verified** through the governed lifecycle.
**`OWNER_DECISION_REGISTER.md` UNCHANGED** — closure-gate convention: no new Owner decision is required
merely to close an already-accepted, already-merged implementation.

**This record does NOT open PVCG-R4.** Naming R4 as the next workstream authorizes nothing.

**Why this record exists.** `PVCG_R3_C_SEMANTIC_STABILITY_CONTRACT.md` §19 (AUTHORITATIVE, merged PR
#551) lists ten criteria and requires as criterion **10** *"a formal closure record merged, exactly as R2
required."* R3 is therefore NOT closed by the R3-I implementation merge alone. This is the required
instrument, following the established `<GATE>_FORMAL_CLOSURE_RECORD.md` convention set by
`PVCG_R2_FORMAL_CLOSURE_RECORD.md`.

---

## §1. Closure basis — the authoritative R3-I merge, verified live

Live tip re-fetched from `origin/feature/atomic-json-session-persistence` this gate and independently
verified — not assumed, not copied from a directive:

| Fact | Verified value | Method |
|---|---|---|
| Live tip | `d046b3e5449f5f91f5f719686e7e207ceda2f06c` | `git fetch` + `git rev-parse origin/…` |
| Commits after the tip | **0** | `git rev-list --count d046b3e5..origin/…` |
| Working tree | clean | `git status --porcelain` empty |

**PVCG-R3-I merge (PR #552)** — `git cat-file -p d046b3e5`:

```
tree   db87b7cbdc5c681d10e8e905b5d81a9f2c29cd7c   PASS
parent 7b7aa2f12a7429fbb309c2f4a7e13d7b83ebdd60   PASS  (first parent / prior authoritative base)
parent 4978c969357200721199c811fede2d40d59e95ac   PASS  (second parent / exact Owner-accepted candidate)
accepted candidate tree : db87b7cbdc5c681d10e8e905b5d81a9f2c29cd7c   == merge tree
candidate -> merge diff : EMPTY                   PASS
git diff --check        : PASS
```

`PVCG-R3-C AUTHORITATIVE: YES` — merged PR #551, merge `7b7aa2f12a7429fbb309c2f4a7e13d7b83ebdd60`,
first parent `ca98099e…`, second parent `6bdf2669…` (the exact Owner-accepted R3-C candidate), merge
tree `c707281a…`, empty candidate→merge diff; re-verified from repository lineage this gate.

---

## §2. Governed review and acceptance lineage (all SHAs preserved, none rewritten)

| SHA | Disposition |
|---|---|
| `52a25182c151c3edaa0c5fecd00631de5c528968` | Creator-Grill evidence, preserved unchanged |
| `1ce9ef340c7cb908da37ae8b4b304b1ee9ae30bc` | **REJECTED** by Independent External Review on blocking defects **B-1** and **B-2**; preserved unchanged as immutable review evidence, never published |
| `3f08e727e1ea58a08cccbc0816820e63cb1ce857` | Focused re-review: **ACCEPT WITH NON-BLOCKING OBSERVATIONS**; B-1 PASS, B-2 PASS; two unsupported material claims raised (**U-1**, **U-2**) |
| `0f1404f09a24c57cf69863797d4d18629525cac8` | Focused re-review: **ACCEPT WITH NON-BLOCKING OBSERVATIONS**; U-1 PASS, U-2 PASS; one unsupported material claim raised (**R3-I-O1**, recorded as `O-1` in the merged PVCG-R3-I history — see §3.1) |
| `4978c969357200721199c811fede2d40d59e95ac` | **Owner-accepted exact SHA**, merged via **PR #552** → `d046b3e5…` |

No candidate was amended, rebased, squashed or recreated at any point in this lineage.

### §2.1 Closure-gate candidate lineage (unpublished; none amended, rebased, squashed or recreated)

| SHA | Disposition |
|---|---|
| `a477ead76d5d57c61da2f15eb1ff1eadfbd8da5e` | Independent closure review: **ACCEPT WITH NON-BLOCKING OBSERVATIONS**; `UNSUPPORTED MATERIAL CLAIMS = 0`; observations **CLOSURE-O1**, **CLOSURE-O2**, **CLOSURE-O3** |
| `ebd94ab0ebaba224b93aea4e16b9e72ea89d52bc` | Governance-precision child carrying the CLOSURE-O1/O2/O3 repairs. Independent closure **re-review**: **ACCEPT WITH NON-BLOCKING OBSERVATIONS**; `UNSUPPORTED MATERIAL CLAIMS = 0`; CLOSURE-O1 **PASS**, CLOSURE-O2 **PASS**, CLOSURE-O3 **PASS**; findings **N-P1**, **N-P2**, **N-P3**, **N-P4** raised |
| *this candidate* | N-P1 / N-P2 / N-P3 micro-precision child of `ebd94ab0…`; governance prose only; **not yet independently re-reviewed** — see §5.1 |

---

## §3. Defect dispositions

| ID | Class | Disposition |
|---|---|---|
| **B-1** | BLOCKING | **CLOSED.** Arabic causal surfaces matched by raw substring, so a 2-character surface fired from inside ordinary words and an answer whose only qualifying token was a common noun reached `REASONED` and CLOSED a gap while its faithful English counterpart did not. Repaired at the mechanism level: every causal surface now declares a `match_mode` and is matched through the same `_surface_matches` discipline as the concept surfaces, with the definite-article proclitics excluded for causal surfaces and the validator refusing at import any single-token causal or unknown surface declared PHRASE. |
| **B-2** | BLOCKING | **CLOSED.** Coverage probes were derived from a table derived from the object under test, so deleting a registered surface deleted its own test case. Repaired by `tests/fixtures/pvcg_r3i_frozen_expectations.py` — a frozen corpus of literal committed rows that imports nothing from the matcher it polices, with a both-directions parity test. |
| **U-1** | NON-BLOCKING (evidence precision) | **CLOSED.** A mis-scoped mutation harness mutated the wrong table for two surfaces that exist in both the concept and substance tables. Corrected; the figures now stand at the independently reproduced values in §5. |
| **U-2** | NON-BLOCKING (governance truth) | **CLOSED.** A comment claimed a 2-character causal surface still matched through a proclitic; it does not, being below the 3-character guard. Comment corrected to code truth, guard NOT weakened, and both sides of the boundary pinned by isolated assertions. |
| **R3-I-O1** | NON-BLOCKING (governance truth) | **CLOSED.** The same stale sentence survived in the live roadmap gate entry; corrected in place. Recorded as `O-1` in the merged PVCG-R3-I history — see §3.1. |

### §3.1 Label namespace — disambiguated, with no history rewritten

Two independent review rounds each numbered their observations from `O-1`, in **different** namespaces:
one against the PVCG-R3-I implementation, one against this closure gate. Reading `O-1` therefore required
knowing which round was meant. The collision is removed by explicit prefixes:

| Disambiguated label | Namespace | Label as originally issued | Where the original label remains |
|---|---|---|---|
| **R3-I-O1** | PVCG-R3-I implementation lineage — raised by the focused re-review of candidate `0f1404f0…` | `O-1` | the merged PVCG-R3-I entries in `ACTIVE_EXECUTION_ROADMAP.md` (PR #552, merge `d046b3e5…`) — **preserved verbatim; NOT rewritten** |
| **CLOSURE-O1 / CLOSURE-O2 / CLOSURE-O3** | this PVCG-R3 closure gate — raised by the independent closure review of candidate `a477ead7…` | `O-1` / `O-2` / `O-3` | this gate's own unmerged surfaces only; no merged document carries them |

Merged history is authoritative for what it says. Renaming a merged document is forbidden and was not
done: the prefixes are applied only where the collision is live — this record and the three current
status surfaces. No disposition, verdict, count or status changes as a result.

**Closure-gate observations (against `a477ead7…`), and how each was repaired:**

| ID | Class | Disposition |
|---|---|---|
| **CLOSURE-O1** | NON-BLOCKING (evidence provenance) | **CLOSED — completed at this candidate.** The criterion-4 evidence locator did not account for every §10.1 property. The repair at `ebd94ab0…` split the evidence into two groups but still named only **four** of the **eight**; the independent re-review recorded that as **N-P1**. §4.1 now maps all eight, each to a named test. Criterion 4 status was, and remains, **MET**. |
| **CLOSURE-O2** | NON-BLOCKING (evidence precision) | **CLOSED.** The §7.3 wording could be read as an exhaustive-pair claim. Corrected to state Σ(n−1) = **313 executed** anchor comparisons with the every-pair property following **transitively**, and the **1,174** exhaustive unordered pairs explicitly **NOT** executed. |
| **CLOSURE-O3** | NON-BLOCKING (verdict provenance) | **CLOSED.** `UNSUPPORTED MATERIAL CLAIMS` is an independent-reviewer field, not a Creator self-award. Creator and reviewer findings are now stated separately and attributed to the exact SHA each was issued against — §5.1. |

**Closure re-review findings (against `ebd94ab0…`), and how each is disposed here:**

| ID | Class | Disposition |
|---|---|---|
| **N-P1** | NON-BLOCKING (evidence provenance) | **CLOSED.** Criterion-4 locator completed to all eight §10.1 properties — **§4.1**. The two previously uncited properties (repetition protection, non-punitive rejection) were already proven green; what was missing was the citation. **Criterion 4 status unchanged: MET.** |
| **N-P2** | NON-BLOCKING (governance truth) | **CLOSED.** The `O-1` namespace collision is removed by the `R3-I-O1` / `CLOSURE-O1` prefixes above, with merged history preserved verbatim — §3.1. |
| **N-P3** | NON-BLOCKING (governance truth) | **CLOSED.** The review-status statement is rewritten per-SHA and dated to submission, so it records that `ebd94ab0…` **was** reviewed while this child has **not** been — §5.1. |
| **N-P4** | **NOT A DEFECT — reviewer-environment limitation** | **NO REPAIR MADE, AND NONE IS OWED.** The reviewer could not re-execute the application suites because Flask was unavailable in the reviewer's environment. This is a property of that environment, not of the product, the candidate, or any §19 criterion — §5.1. |

---

## §4. Closure criteria — `PVCG_R3_C_SEMANTIC_STABILITY_CONTRACT.md` §19, item by item

| # | Criterion | Status | Basis |
|---|---|---|---|
| 1 | R3-C authoritative (merged, post-merge verified) | **MET** | PR #551, merge `7b7aa2f1…`, re-verified §1 |
| 2 | R3-I Owner-authorized, implemented, independently reviewed, Owner-accepted, merged, post-merge verified | **MET** | §2 lineage; PR #552, merge `d046b3e5…`, re-verified §1 |
| 3 | §7.3 GREEN over the published registered-class inventory | **MET** | re-measured on the merged tree: **313 anchor comparisons over the published registered-class inventory** (56 concepts, 369 registered surfaces), **0 material mismatches**; D-1 divergence **0/6**. Stated precisely: the suite compares each remaining surface of a concept against a common anchor surface — Σ(n−1) = **313 executed comparisons** — and the every-pair property §7.3 requires follows **transitively** from equality against that anchor. The exhaustive unordered pair count would be **1,174**; those 1,174 pairs were **NOT** executed and are not claimed. |
| 4 | every §10.1 property re-proven, every §10.2 category tested | **MET** | **Complete property-by-property evidence map in §4.1** — all **eight** §10.1 properties and all **eleven** §10.2 categories carry a named proof locator, in two evidence groups because the R3-I classes alone are **not** the full §10.1 basis. All named suites were measured green on the merged tree (§5, criteria 7–8). Status unchanged: **MET**. |
| 5 | every §16 negative control holding | **MET** | `TestNegativeControls` green on the merged tree |
| 6 | §13.2 pin reconciliation exactly as specified, with packs, `domain_rules.py`, `path_n_questions.py` byte-identical | **MET** | live `engine/progression_loop.py` digest `3cbd76849c0f572191a552db1a41a8cd418d02fac1d59d9b8804c72883239a55` enforced green by the three P9 suites; `domain_rules.py` `0e47326a…`, `path_n_questions.py` `a1a682d3…` and all five `domains/*/domain.json` byte-identical |
| 7 | R1 26/26 GREEN with its test file byte-unchanged; R2 suites GREEN | **MET** | R1 **26 passed**, test file byte-unchanged; R2 behavioural **189 passed**; R2 marker coverage **566 passed**, file byte-unchanged |
| 8 | universal guardrail smoke PASS; full suite reconciled per §18 | **MET** | `UNIVERSAL GUARDRAIL SMOKE: PASS`; full suite **4355 passed / 3 skipped / 1 xfailed / 0 failed** under the §18 precondition (Python 3.11.15, Flask 3.1.3, SQLite 3.45.1, gunicorn 26.1.0 on `PATH`); reconciliation 3776 baseline **+579**, exactly the R3-I test file |
| 9 | the residual — unregistered wording in either language — stated truthfully as a known bound, not concealed | **MET** | stated in `engine/semantic_registry.py` module docstring and at the R3 hook in `engine/gap_relevance.py`, both as an explicit **KNOWN BOUND** |
| 10 | a formal closure record merged, exactly as R2 required | **PENDING — THIS RECORD**, effective only on merge and post-merge verification |

All ten criteria are resolved. Criteria 1–9 are MET and were **re-measured on the merged tree**, not
inherited. Criterion 10 is this record.

### §4.1 Criterion 4 — complete evidence locators (all EIGHT §10.1 properties, all ELEVEN §10.2 categories)

`PVCG_R3_C_SEMANTIC_STABILITY_CONTRACT.md` §10.1 lists **eight** preserved R2 properties. Earlier
statements of criterion 4 named only **four** of them explicitly and left the remaining four to be
inferred from the phrase *"the §16 controls"*, which is a category, not a locator. This section repairs
**evidence provenance only**. **Criterion 4 status is unchanged: MET** — no property was ever unproven;
each proof was already green in a committed suite, and what was missing was the citation.

Two evidence groups: **(A)** the focused R3-I suite `tests/test_pvcg_r3i_semantic_stability.py`
(**579 passed**); **(B)** other authoritative suites, already reported green under criteria 7 and 8.

| # | §10.1 property | Proof locator | Group |
|---|---|---|---|
| 1 | Gap-specific relevance | `tests/test_pvcg_r2i_gap_relevance.py::test_each_genuine_answer_closes_only_its_own_gap` — the authoritative 6×6 **closure** control — together with `TestNegativeControls::test_1_diagonal_behaviour_is_identical_across_languages`, which asserts the EN and AR diagonals are step-for-step identical over three deliveries per gap | B + A |
| 2 | Cross-gap protection (differential, *no new leakage*) | `TestAdversarialCategories::test_8_cross_gap_reuse_creates_no_off_diagonal_closure`, parametrized over all six served gaps, plus `TestNegativeControls::test_8_pre_existing_english_breadth_is_MIRRORED_not_narrowed`, which pins the Arabic side to the pre-existing English breadth rather than to an unsound zero-eligibility property (§16.1) | A |
| 3 | **Repetition protection** | `tests/test_pvcg_r2i_gap_relevance.py::TestRed3RepetitionCannotManufactureSatisfaction::test_five_repetitions_of_an_irrelevant_answer_never_close` — `times=5`, parametrized over every gap × every off-topic answer, asserting the served gap never reaches `CLOSED` | B |
| 4 | Fail-closed | `TestNegativeControls::test_2_unregistered_arabic_is_not_eligible`, `::test_3_unregistered_english_paraphrase_still_not_eligible`, `::test_4_empty_and_whitespace_not_eligible`, `::test_5_off_topic_answer_to_served_gap_in_both_languages`, `::test_6_near_miss_under_an_unauthorized_normalization` | A |
| 5 | **Non-punitive rejection** | `tests/test_pvcg_r2i_gap_relevance.py::TestFailClosedIsNotPunitive::test_irrelevant_answer_never_returns_block` — parametrized over every gap × every off-topic answer, asserting the transition is `WARN` and never `BLOCK` | B |
| 6 | Determinism (§6.1) | `TestDeterminismAndProhibitions::test_decision_is_deterministic_over_repetitions` — identical outcome over 12 evaluations per gap | A |
| 7 | R1 durable epistemic memory (§11) | `tests/test_pvcg_r1_durable_epistemic_memory.py` — **26 passed**, test file byte-unchanged | B |
| 8 | P9-MECH-I3/I4/I5 pins (§13) | `tests/test_p9_mech_i3_signal_quality.py`, `tests/test_p9_mech_i4_boundary_corpus.py`, `tests/test_p9_mech_i5_question_sufficiency.py` — **54 passed**, enforcing the reconciled `3cbd7684…` digest | B |

**§10.2 categories 1–11** are exercised one-for-one by `TestAdversarialCategories::test_1…test_11`, with
category 10 (substring / token ambiguity) additionally pinned by the dedicated `TestCausalTokenBoundary`
class. **§16 negative controls 1–7** are exercised by `TestNegativeControls::test_1…test_7`; `test_8` in
that class is the additional disclosed mirrored-breadth control, not one of the seven.

**Evidence status of rows 1, 3, 5, 7 and 8 — stated exactly.** All five locators live in suites whose
green results on the merged tree (**189** for `tests/test_pvcg_r2i_gap_relevance.py`, **26** for the R1
suite, **54** for the three P9 pin suites) are already recorded in §5 and under criteria 7 and 8. They
are **carried forward here as already-established evidence and were NOT re-run for this locator
repair**, which changes governance prose only and leaves every executable file byte-identical.

---

## §5. Evidence provenance, stated precisely

**Re-measured on the merged tree `d046b3e5…` this gate:** focused R3-I **579 passed**; PVCG-R1 **26
passed**; R2 behavioural **189 passed**; R2 marker coverage **566 passed**; P9 pin suites **54
passed**; `UNIVERSAL GUARDRAIL SMOKE: PASS`; full suite **4355 passed / 3 skipped / 1 xfailed / 0
failed**; §7.3 **313 anchor comparisons / 0 mismatches** (56 concepts, 369 surfaces; every-pair equality
follows transitively — the 1,174 exhaustive pairs were not executed); D-1 **0/6**; the four watched engine digests and all
five pack digests.

**Carried, independently verified, NOT re-measured this gate:** the mutation sweep **257 processed /
254 KILLED / 0 SURVIVED / 3 LOADFAIL, restore 257/257 byte-identical**. It was measured on candidate
`0f1404f0…` and **independently reproduced by the Independent External Reviewer**, and it carries to
this tree because the merge tree `db87b7cb…` is identical to the accepted candidate tree and
`engine/semantic_registry.py` together with the frozen oracle are byte-identical across `0f1404f0…` →
`4978c969…` → the merge. The three LOADFAILs are the three concepts whose only Arabic surface is
removed by the mutation, where the registry's own import-time `RegistryError` refuses the mutant —
fail-closed by design, and correctly not counted as behavioural kills.

### §5.1 Review provenance — stated per SHA, and durable

`UNSUPPORTED MATERIAL CLAIMS` is an **independent-reviewer** field. It is not a verdict the Creator may
self-award, so Creator findings and reviewer findings are kept separate, and every count is attributed to
the exact candidate it was issued against. Written this way the statement stays true as the lineage
grows, instead of silently going stale the moment a new child is created — the defect recorded as
**N-P3**.

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

THIS candidate — the N-P1 / N-P2 / N-P3 micro-precision child of ebd94ab0…
  INDEPENDENTLY REVIEWED      = NO, as at the time of its submission
```

**Stated without drift.** `ebd94ab0…` **was** independently reviewed; that review returned ACCEPT WITH
NON-BLOCKING OBSERVATIONS, confirmed all three predecessor observations PASS, and counted zero
unsupported material claims. **This child candidate carries only the N-P1 / N-P2 / N-P3 governance-prose
repairs and has NOT itself received a focused re-review.** It must not be described, cited or summarised
as reviewed.

**N-P4 — classification, stated exactly and not converted into something it is not.** The reviewer could
not re-execute the application suites because **Flask was unavailable in the reviewer's environment**.
That is a **reviewer-environment limitation**. It is **not** a product defect, **not** a closure defect,
**not** a failure of any §19 criterion, and **not** evidence that the recorded suite results are
unreliable: `PVCG_R3_C_SEMANTIC_STABILITY_CONTRACT.md` §18 declares the execution precondition (Python
3.11.15, Flask 3.1.3, SQLite 3.45.1, gunicorn 26.1.0 on `PATH`), and every suite result recorded in §5
was measured in an environment satisfying it. **No repair is made for N-P4, and none is owed.** Recording
it here neither weakens the evidence nor creates work.

---

## §6. Residuals carried forward — OPEN, NON-BLOCKING, and NOT R4 authorization

Neither residual appears in any of the ten §19 closure criteria, and both were classified NON-BLOCKING
by the Independent External Reviewer. They do not block this closure.

* **N-2 — acknowledged-unknown length threshold.** `_MIN_ACKNOWLEDGED_UNKNOWN_LENGTH = 40` is
  language-neutral as a rule but not in effect, because Arabic is more compact: an equivalent EN/AR pair
  can straddle it. **Pre-existing**, byte-unchanged by R3, **fail-closed in direction** (Arabic receives
  less recording, never more), and outside the §7.3 quantifier, which ranges over registered surfaces
  rather than free-form sentences. Redesigning the threshold was not authorized by R3-C and was not done.
* **U-4 — a single Arabic connective inside otherwise-English prose grants causal structure.** Correct by
  design and symmetric with the mixed-language characterisation R3-C §10.2/9 makes mandatory.
* **The declared R3 bound** — unregistered wording in either language is not governed-equivalent and
  gains nothing. R3 delivers a registered bilingual concept mapping: not language understanding, not
  arbitrary paraphrase stabilisation, not translation, and not a third language.

**Recording a residual here authorizes no work on it.** Neither N-2 nor U-4 nor the declared bound is
PVCG-R4 authorization, and none of them starts any successor gate.

---

## §7. Closure statements (authoritative ONLY if/when this candidate is merged and post-merge verified)

```
PVCG-R1 AUTHORITATIVE: YES
PVCG-R2 AUTHORITATIVELY CLOSED: YES
PVCG-R3-C AUTHORITATIVE: YES
PVCG-R3-I AUTHORITATIVE: YES
PVCG-R3 FORMALLY CLOSED: YES
PVCG-R3 AUTHORITATIVELY SATISFIED: YES
PVCG-R4 IMPLEMENTATION STARTED: NO
FULL ADAPTIVE QUESTIONING ACTIVATED: NO
LLM/NLP SUBSYSTEM ADDED: NO
EMBEDDINGS ADDED: NO
EXTERNAL NLP SERVICE ADDED: NO
PROBABILISTIC SEMANTIC CLASSIFIER ADDED: NO
TDVP IMPLEMENTATION STARTED: NO
PVCG SATISFIED: NO
MINIMUM LAUNCH-CONFORMANCE SET SATISFIED: NO
DEPLOYMENT AUTHORIZED: NO
```

**Closing R3 closes ONLY R3.** It does not satisfy PVCG, does not satisfy the Minimum
Launch-Conformance Set, and authorizes no deployment — stated verbatim in the governing contract's §19
and repeated here without weakening. R1, R2 and R3 are cumulative: closing R3 neither weakens nor
supersedes R1 or R2.

**PVCG-R4 — correction / invalidation — remains NOT STARTED** and is opened only by the Owner through
the established workflow. Naming it here authorizes nothing.

---

## §8. Scope of this gate

Governance/documentation only — this new closure record plus one append-only roadmap entry and the two
status surfaces. No `engine/`, `web/`, `tests/`, `domains/`, `scripts/`, evidence-tree, generator,
deployment or Render path is touched; no pin moves (`PIN DELTA: 0`); `main` is not reconciled; and
`OWNER_DECISION_REGISTER.md` is UNCHANGED.
