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
| `0f1404f09a24c57cf69863797d4d18629525cac8` | Focused re-review: **ACCEPT WITH NON-BLOCKING OBSERVATIONS**; U-1 PASS, U-2 PASS; one unsupported material claim raised (**O-1**) |
| `4978c969357200721199c811fede2d40d59e95ac` | **Owner-accepted exact SHA**, merged via **PR #552** → `d046b3e5…` |

No candidate was amended, rebased, squashed or recreated at any point in this lineage.

---

## §3. Defect dispositions

| ID | Class | Disposition |
|---|---|---|
| **B-1** | BLOCKING | **CLOSED.** Arabic causal surfaces matched by raw substring, so a 2-character surface fired from inside ordinary words and an answer whose only qualifying token was a common noun reached `REASONED` and CLOSED a gap while its faithful English counterpart did not. Repaired at the mechanism level: every causal surface now declares a `match_mode` and is matched through the same `_surface_matches` discipline as the concept surfaces, with the definite-article proclitics excluded for causal surfaces and the validator refusing at import any single-token causal or unknown surface declared PHRASE. |
| **B-2** | BLOCKING | **CLOSED.** Coverage probes were derived from a table derived from the object under test, so deleting a registered surface deleted its own test case. Repaired by `tests/fixtures/pvcg_r3i_frozen_expectations.py` — a frozen corpus of literal committed rows that imports nothing from the matcher it polices, with a both-directions parity test. |
| **U-1** | NON-BLOCKING (evidence precision) | **CLOSED.** A mis-scoped mutation harness mutated the wrong table for two surfaces that exist in both the concept and substance tables. Corrected; the figures now stand at the independently reproduced values in §5. |
| **U-2** | NON-BLOCKING (governance truth) | **CLOSED.** A comment claimed a 2-character causal surface still matched through a proclitic; it does not, being below the 3-character guard. Comment corrected to code truth, guard NOT weakened, and both sides of the boundary pinned by isolated assertions. |
| **O-1** | NON-BLOCKING (governance truth) | **CLOSED.** The same stale sentence survived in the live roadmap gate entry; corrected in place. |

---

## §4. Closure criteria — `PVCG_R3_C_SEMANTIC_STABILITY_CONTRACT.md` §19, item by item

| # | Criterion | Status | Basis |
|---|---|---|---|
| 1 | R3-C authoritative (merged, post-merge verified) | **MET** | PR #551, merge `7b7aa2f1…`, re-verified §1 |
| 2 | R3-I Owner-authorized, implemented, independently reviewed, Owner-accepted, merged, post-merge verified | **MET** | §2 lineage; PR #552, merge `d046b3e5…`, re-verified §1 |
| 3 | §7.3 GREEN over the published registered-class inventory | **MET** | re-measured on the merged tree: **313 registered-surface pairs compared, 0 material mismatches**; D-1 divergence **0/6** |
| 4 | every §10.1 property re-proven, every §10.2 category tested | **MET** | `TestAdversarialCategories`, `TestNegativeControls`, `TestCausalTokenBoundary` present and green in the 579-test R3-I suite on the merged tree |
| 5 | every §16 negative control holding | **MET** | `TestNegativeControls` green on the merged tree |
| 6 | §13.2 pin reconciliation exactly as specified, with packs, `domain_rules.py`, `path_n_questions.py` byte-identical | **MET** | live `engine/progression_loop.py` digest `3cbd76849c0f572191a552db1a41a8cd418d02fac1d59d9b8804c72883239a55` enforced green by the three P9 suites; `domain_rules.py` `0e47326a…`, `path_n_questions.py` `a1a682d3…` and all five `domains/*/domain.json` byte-identical |
| 7 | R1 26/26 GREEN with its test file byte-unchanged; R2 suites GREEN | **MET** | R1 **26 passed**, test file byte-unchanged; R2 behavioural **189 passed**; R2 marker coverage **566 passed**, file byte-unchanged |
| 8 | universal guardrail smoke PASS; full suite reconciled per §18 | **MET** | `UNIVERSAL GUARDRAIL SMOKE: PASS`; full suite **4355 passed / 3 skipped / 1 xfailed / 0 failed** under the §18 precondition (Python 3.11.15, Flask 3.1.3, SQLite 3.45.1, gunicorn 26.1.0 on `PATH`); reconciliation 3776 baseline **+579**, exactly the R3-I test file |
| 9 | the residual — unregistered wording in either language — stated truthfully as a known bound, not concealed | **MET** | stated in `engine/semantic_registry.py` module docstring and at the R3 hook in `engine/gap_relevance.py`, both as an explicit **KNOWN BOUND** |
| 10 | a formal closure record merged, exactly as R2 required | **PENDING — THIS RECORD**, effective only on merge and post-merge verification |

All ten criteria are resolved. Criteria 1–9 are MET and were **re-measured on the merged tree**, not
inherited. Criterion 10 is this record.

---

## §5. Evidence provenance, stated precisely

**Re-measured on the merged tree `d046b3e5…` this gate:** focused R3-I **579 passed**; PVCG-R1 **26
passed**; R2 behavioural **189 passed**; R2 marker coverage **566 passed**; P9 pin suites **54
passed**; `UNIVERSAL GUARDRAIL SMOKE: PASS`; full suite **4355 passed / 3 skipped / 1 xfailed / 0
failed**; §7.3 sweep **313 pairs / 0 mismatches**; D-1 **0/6**; the four watched engine digests and all
five pack digests.

**Carried, independently verified, NOT re-measured this gate:** the mutation sweep **257 processed /
254 KILLED / 0 SURVIVED / 3 LOADFAIL, restore 257/257 byte-identical**. It was measured on candidate
`0f1404f0…` and **independently reproduced by the Independent External Reviewer**, and it carries to
this tree because the merge tree `db87b7cb…` is identical to the accepted candidate tree and
`engine/semantic_registry.py` together with the frozen oracle are byte-identical across `0f1404f0…` →
`4978c969…` → the merge. The three LOADFAILs are the three concepts whose only Arabic surface is
removed by the mutation, where the registry's own import-time `RegistryError` refuses the mutant —
fail-closed by design, and correctly not counted as behavioural kills.

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
