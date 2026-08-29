# S2 Path-N Release-Evaluation Run Record — S2-PATHN-RUN-003 (post-G-3 T1-A′ re-verification)

STATUS: EVIDENTIARY RUN RECORD — NOT AN OWNER APPROVAL (S2 §11). NON-ACTIVATING.
A result authorizes nothing (S2 §0). This is the ONE Owner-authorized post-G-3 T1-A′
re-verification run. **It closes nothing. `T1-A′ CLOSED: NOT ASSERTED BY THIS RUN`.**

## §10 template (with the §15.9 additional axes)

- **Run ID:** `S2-PATHN-RUN-003`
- **Benchmark version:** S2 §§0–14 + Path-N Release-Evaluation Extension v1 (§§15–17), byte-unchanged
  since run 001 and run 002.
- **Benchmark authoritative SHA:** `5a392f0cfd7d6b19874382441f78fee61cee1a26`
- **Evaluated product SHA (exact, authorized):** `5a392f0cfd7d6b19874382441f78fee61cee1a26`
  — the PR #600 merge of the G-3 implementation; parents `f96c1900…` / `7a887a42…`, tree `0ce806c3…`
  (identical to the accepted candidate's tree — EMPTY candidate→merge diff).
  **All 8 records used this one SHA — MIXED-SHA RUN: NO.**
- **Case versions:** `E-1 v1`, `M-1 v1` — unchanged; frozen seeds byte-identical to runs 001/002.
- **Date:** 2026-08-29
- **Evaluator:** the Creator/Executor agent. Evaluation perspectives per §15.4 — **not real users**;
  no real-user claim is made anywhere in this record.
- **Environment:** in-process Flask test client against the committed application at the evaluated
  tree; `INVENTORAI_DB_PATH` bound to a dedicated run store outside the repository;
  `AI_ADVISORY_ENABLED = False` (asserted at import); no product AI call occurred; CWD = repository root.
- **Answer policy (comparability):** the run-001 frozen answer corpus replayed verbatim per gap type,
  perspective and language — the same corpus run 002 replayed. No new gap type was encountered in any
  record, so the disclosed evaluator honest-unknown fallback was never used. The corpus deliberately
  exercises NO structured disposition action, NO correction and NO risk acceptance, exactly as before.

## Frozen-instrument / corpus comparability proof (§3 preflight)

- **Instrument.** The whole `docs/benchmarks/` tree is the SAME Git object
  `61f2bb458c7e4b53c766c018c7c73baebcea30da` at the run-002 authoritative SHA `1f3d9d14…` and at the
  evaluated SHA; the instrument blob is `4e64b5906596ed538d45bb9192ba32ed6a84ad1e` at both.
  **INSTRUMENT DELTA: 0.**
- **Corpus.** The seeds/answer corpus was read from the committed run-001 evidence blob
  `0ddd1644afe1f5b57ca5b396fae51a69080e8de3`
  (sha256 `0750f3e41a1d8489353c52abbcbda79f32f445d33ace3561bf2422f656ce7fce`), verified byte-identical
  to the local copy the harness read. **CORPUS DELTA: 0.** Cardinality 2×2×2 = **8 records**, exactly
  as run 002.
- **Harness.** The preserved run-002 harness
  (sha256 `9bac68f79bd565de6a54c371d192cdb8a5911d9abe5e97384c6b4257f6d52696`) with **six changed lines
  only** — evidence output directory, `RC_SHA` constant, local secret-key and db-path names, the
  `run_id` label and one boolean label. No admission, answering, interaction-bound, capture or
  evaluation logic changed. This is disclosed rather than asserted; the harness is not the instrument,
  and its identity across the two runs is stated as measured, not as a guarantee.
- No corpus extension, answer rewriting, translation rewriting, benchmark repair, criterion
  reinterpretation, threshold change, scoring change, prompt tuning or product modification occurred.

## The eight records (separate; never merged)

| Rec | Case | Lang | Perspective | Classifier | Confirmed domain | Interactions | Ledger | Deliverable eligible | Stage | Maturity | Core gate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R1 | E-1 | EN | novice | `NONE` | `electronics_electrical` | 24 | 24 | false | none | 1 | PARTIAL |
| R2 | E-1 | EN | expert | `NONE` | `electronics_electrical` | 24 | 24 | false | none | 1 | PARTIAL |
| R3 | E-1 | AR | novice | `NONE` | `electronics_electrical` | 24 | 24 | false | none | 1 | FAIL |
| R4 | E-1 | AR | expert | `NONE` | `electronics_electrical` | 24 | 24 | false | none | 1 | PARTIAL |
| R5 | M-1 | EN | novice | `SINGLE` | `mechanical` | 24 | 24 | false | none | 1 | PARTIAL |
| R6 | M-1 | EN | expert | `SINGLE` | `mechanical` | 24 | 24 | false | none | 1 | FAIL |
| R7 | M-1 | AR | novice | `NONE` | `mechanical` | 24 | 24 | false | none | 1 | PARTIAL |
| R8 | M-1 | AR | expert | `NONE` | `mechanical` | 24 | 24 | false | none | 1 | FAIL |

**Full Pass count: 0.** Core-gate distribution: **5 PARTIAL / 3 FAIL / 0 PASS** — identical to run 002.
Zero execution anomalies in all 8 records. No retry, no restart, no aborted attempt.

## The decisive measurement — criteria 5 and 6

**Criterion 5 (alternatives bounded and truthfully classified): FAIL on all 8 records.**
**Criterion 6 (elimination or qualification reasons explicit): FAIL on all 8 records.**
**Both UNCHANGED from run 002.**

Measured cause, taken from this run's own captured HTML rather than inferred:

| Rec | decision-capture section served | decision contexts declared | alternatives rendered | G-3 governed strings present | deliverable decision section |
|---|---|---|---|---|---|
| R1–R8 | yes (all 8) | **0** | **0** | **0 of 8 strings** | absent (all 8) |

The frozen corpus answers questions; it never posts to the governed
`/session/<sid>/decision/declare-context` or `declare-alternative` routes. With no declared context
there is no candidate set, so the G-3 bounded rendered set, the withdrawal state, the withdrawal
reason, the evidence state and the not-comparable reason **all have no subject on this corpus** and are
rendered zero times. The run-002 basis — *"no elimination or qualification reasons exist because no
comparison happens"* — still holds verbatim.

**This is the residual the frozen corpus cannot exercise. It is NOT a measurement that the G-3
implementation failed, and it is NOT a measurement that it succeeded.** Per the Owner's §6 fence, the
withdrawal-history behaviours, the withdrawal-reason paths and the redeclaration-after-withdrawal edge
cases were implementation-tested separately and are outside what this corpus can truthfully measure.

## Run 002 → run 003 (measured change, stated before any interpretation)

| Measured surface | RUN-002 | POST-G-3 RUN-003 | Change |
|---|---|---|---|
| Full Pass count | 0 | 0 | **none** |
| Core-gate distribution | 5 PARTIAL / 3 FAIL | 5 PARTIAL / 3 FAIL | **none** |
| Per-record core gate | R1 P · R2 P · R3 F · R4 P · R5 P · R6 F · R7 P · R8 F | identical | **none** |
| Criterion 5 | FAIL ×8 | FAIL ×8 | **none** |
| Criterion 6 | FAIL ×8 | FAIL ×8 | **none** |
| Deliverable eligibility | false ×8 | false ×8 | **none** |
| Stage 3 reachability | not reached ×8 | not reached ×8 | **none** |
| Final maturity | 1 ×8 | 1 ×8 | **none** |
| Accepted ledger records | 24 ×8 | 24 ×8 | **none** |
| Gap end-state per record | — | identical in all 8 | **none** |
| Question sequence, text, answers, lang/dir | — | identical in all 8 | **none** |
| AR question rendering | `lang="ar" dir="rtl"` ×24 in R3/R4/R7/R8 | identical | **none** |
| Correction affordance on session surface | present ×8 | present ×8 | **none** |
| Deliverable meta and section set | — | identical in all 8 | **none** |
| Baseline A (E-1) | export 200 | export 200, semantically identical after volatile-id/timestamp normalization | **none** |
| Baseline A (M-1) | unobtainable → criterion 17 NOT EVALUATED | unobtainable → NOT EVALUATED | **none** |
| Captured HTML | — | all 24 pages differ **only** in per-run session/idea UUIDs, the CSRF-style answer token and the deliverable generation timestamp | **no substantive change** |

**MEASURED CHANGE:** none, on every surface this instrument and corpus can measure.

**INTERPRETATION (kept separate, and deliberately narrow):** the G-3 implementation changes the served
Path-N surface only where a decision context and alternatives exist. This corpus creates neither, so
the absence of measured change is the expected consequence of the corpus, not evidence about G-3's
behaviour in either direction. No measured change is attributed to G-3, and no measured non-change is
presented as a G-3 failure.

## Persisting findings, re-measured and unchanged

1. **Arabic generated-output values remain English under Arabic labels** (G-4, its own DOR row) — the
   AR chrome, questions and reader-facing structure render `lang="ar" dir="rtl"` throughout, as at run
   002; the registered generated-output parity obligation is unchanged. **Reproduced, not repaired.**
2. **Perspective inversion persists on M-1** — the practitioner answers still never close MECHANISM in
   24 interactions (R6, R8), and the E-1 Arabic-novice path still does not close it (R3).
3. **Deliverable eligibility and Stage 3 unchanged** — no record reached `deliverable_eligible=true`
   or Stage 3; `PHYSICAL_FEASIBILITY` never closes on the corpus-replayed path.
4. **G-5**: no new material generated-output observation beyond finding 1 surfaced in this run.
5. **Envelope capture limitation, carried unchanged from run 002**: the harness's read-only contract
   capture reports `seed_idea_text_matches=false` and `engine_contract_version=null` in **both** runs.
   This is a capture-shape artifact of the harness, identical across the two runs and therefore
   comparability-neutral; it is recorded here rather than silently omitted, and it is **not** presented
   as a product regression.

## Limitations (§15.11, in full)

One evaluator; frozen synthetic cases; evaluation perspectives, not users; a 24-interaction bound per
record; Baseline A unobtainable for M-1; Baseline B authored once (run 001) and reused; corpus-replay
answer policy with structured dispositions, corrections and risk acceptance deliberately unexercised.
**Additionally and decisively for this run: the frozen corpus does not exercise the decision-capture
path at all**, so criteria 5/6 measure the corpus-replayed journey and nothing about the G-3
decision surfaces. This run must not be described as user research, market evidence, production
readiness, or generalization beyond the frozen cases. T1-A′ and T1-C′ remain separate.

## One-run accounting

`AUTHORIZED FOR THIS GATE: ONE post-G-3 T1-A′ re-verification run` · `RUNS EXECUTED IN THIS GATE: 1` —
exactly 8 evaluation records, no ninth record, **no retries, no reruns, no aborted attempt** ·
`THIRD S2 RUN CONSUMED: YES` · `FOURTH RUN AUTHORIZED: NO` ·
`PRODUCT DELTA: 0` · `INSTRUMENT DELTA: 0` · `CORPUS DELTA: 0` · `RUNTIME REPAIR DURING RUN: 0`.

## T1-A′

`T1-A′ CLOSURE EVIDENCE MET: NO` — criteria 5 and 6 remain FAIL on all eight records and no record
achieved a full pass. **`T1-A′ CLOSED: NOT ASSERTED BY THIS RUN`.** Owner adjudication is separate;
this record closes nothing and authorizes nothing.
