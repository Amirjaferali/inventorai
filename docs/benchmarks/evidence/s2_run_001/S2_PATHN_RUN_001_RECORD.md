# S2 Path-N Release-Evaluation Run Record — S2-PATHN-RUN-001

STATUS: EVIDENTIARY RUN RECORD — NOT AN OWNER APPROVAL (S2 §11). NON-ACTIVATING.
A result authorizes nothing (S2 §0). This record renders the run's evidence faithfully;
adjudication of findings belongs to the next, separately authorized gate.

## §10 template (with the §15.9 additional axes)

- **Run ID:** `S2-PATHN-RUN-001`
- **Benchmark version:** S2 §§0–14 + **Path-N Release-Evaluation Extension v1** (§§15–17)
- **Benchmark authoritative SHA:** `e119d60450f40b1633433625ae6a011eec112b79`
- **Case versions:** `E-1 v1` (unchanged §2 case), `M-1 v1` (§15.2)
- **Evaluated commit (exact Release Candidate SHA):** `e119d60450f40b1633433625ae6a011eec112b79`
  — parents `a9b9d53c…` / `a25c21ce…`, tree `0274c823…`. **RC basis:** §15.1 evaluates the governed
  Path-N journey *at one exact commit*; §15.8 Baseline C is the *actual committed* increment; product
  paths `engine/ web/ domains/` are byte-identical from the last product-changing commit
  `2bb472a0…` (PVCG-R4-I) through this tip (verified empty diff), so exactly one committed Path-N
  product state exists, and this is the only commit whose tree also carries the authoritative contract.
- **Date:** 2026-08-23
- **Evaluator:** the Creator/Executor agent. **Evaluation perspectives per §15.4 — not real users;
  no real-user claim is made anywhere in this record.**
- **Environment:** in-process Flask test client against the committed application at the RC tree;
  `INVENTORAI_DB_PATH` bound to a dedicated run store (outside the repository);
  `AI_ADVISORY_ENABLED = False` throughout; no product AI call occurred.
- **Baselines compared:** A (FDC-001 export — obtainable for E-1 only: the workspace is hard-coded to
  the bicycle case, so M-1 Baseline A is **NOT EVALUATED** with that reason, per §15.8);
  B (general-purpose AI one-shot responses, assistant named in `baselineB_generic_ai_responses.json` —
  an evaluator activity outside the product); C (the committed increment itself, as executed).
- **Inputs:** the two frozen §15.2 English seeds verbatim; Arabic seeds frozen at first use in
  `answer_maps.json` (faithful translations; classifier returns `NONE` for both, as §15.3 records);
  full verbatim answer sequences per record in `answer_maps.json` + `all_records.json`.
- **Platform outputs:** per-record session and deliverable captures — hashes in `SHA256SUMS.txt`;
  raw HTML pages, the run store (8 projects / 192 append-only records), and per-record JSON are in the
  external evidence package bound by those hashes.
- **Criteria table:** `criteria_matrix.json` — criteria 1–18 with dispositions (12, 13
  `NOT APPLICABLE`; 17 `NOT EVALUATED` for M-1 records with reason) plus `P1…P6`, per record.
- **Core-gate conclusion (§15.7), per record:** R1 PARTIAL · R2 FAIL · R3 FAIL · R4 FAIL ·
  R5 PARTIAL · R6 FAIL · R7 FAIL · R8 FAIL. **No record achieved a full pass.**
- **Limitations:** §15.11 applies in full — one evaluator; frozen synthetic cases; evaluation
  perspectives, not users; a 24-interaction bound per record (reaching it without completion is itself
  a finding, not a truncation of a completing journey); Baseline A unobtainable for M-1; Baseline B
  authored by the named evaluator-assistant.
- **Overall conclusion:** on the frozen cases, at this exact commit, against the governed baselines,
  using the approved criteria, the evaluated Path-N journey and deliverable **did not meet** the
  defined S2 release-value criteria in full on any of the eight records; per-record outcomes are
  3 × PARTIAL (R1, R5 — and R7's mechanism strength noted inside its FAIL) and 5 × FAIL, reported
  separately with **no aggregate score**.

## The eight records (separate; never merged)

| Rec | Case | Lang | Perspective | Classifier on seed | Admission route | Confirmed domain | Core gate |
|---|---|---|---|---|---|---|---|
| R1 | E-1 | EN | novice | `NONE` | D2 choice → explicit confirm | `electronics_electrical` | PARTIAL |
| R2 | E-1 | EN | experienced | `NONE` | D2 choice → explicit confirm | `electronics_electrical` | FAIL |
| R3 | E-1 | AR | novice | `NONE` | D2 choice → explicit confirm | `electronics_electrical` | FAIL |
| R4 | E-1 | AR | experienced | `NONE` | D2 choice → explicit confirm | `electronics_electrical` | FAIL |
| R5 | M-1 | EN | novice | `SINGLE → mechanical` | classifier → explicit confirm | `mechanical` | PARTIAL |
| R6 | M-1 | EN | experienced | `SINGLE → mechanical` | classifier → explicit confirm | `mechanical` | FAIL |
| R7 | M-1 | AR | novice | `NONE` | D2 choice → explicit confirm | `mechanical` | FAIL |
| R8 | M-1 | AR | experienced | `NONE` | D2 choice → explicit confirm | `mechanical` | FAIL |

**Domain-coverage truthfulness (§6 of the execution directive):** only R5/R6 entered their specialist
domain via classification; R1–R4 and R7/R8 entered via the governed D2 **explicit user choice** after a
classifier miss — the case's subject domain was chosen by the evaluator as the inventor would choose
it, and this is recorded as user choice, never as classifier output. The E-1 English seed, constructed
by §15.2's frozen rule, classifies `NONE` — exactly as the contract measured and disclosed in advance.

## Headline measured facts (each traceable to raw evidence)

1. **No record reached deliverable eligibility** within the 24-interaction bound;
   `deliverable_eligible=false` in all 8; no record reached Stage 3.
2. **The exhausted-gap reframe repeated identically 18–20×** per record; later questions never used
   prior answers; honest "unknown" answers were acknowledged (UNK records) but never progressed or
   rerouted the journey.
3. **Perspective inversion:** EN novice phrasing closed MECHANISM_COMPLETENESS in 2–3 interactions;
   EN practitioner phrasing of the same case facts never closed it in 24 (PARTIAL throughout).
4. **Arabic asymmetry:** questions render with explicit `lang="en" dir="ltr"` inside the Arabic RTL
   shell; deliverable substantive values are English under Arabic labels — matching the committed
   scope (`/ui-language` "translates no question or output") while measuring its release-value cost.
   Arabic novice answers closed mechanical MECHANISM in 3 interactions but never closed electronics
   MECHANISM (24× PARTIAL).
5. **Truthfulness held everywhere:** REVISE verdicts with basis; explicit disclaimer; no fabricated
   specifics (the generic-AI baseline asserted unsupported figures); durable envelope carries
   `contract_version` / `engine_contract_version` / verbatim `seed_idea_text` and a 24-record
   append-only ledger per session (criteria 9/10 PASS on all records).
6. **Provenance display divergence:** the deliverable shows "Not recorded (pre-provenance session)"
   while the durable ledger records `provenance=OWNER_STATED` for the same answers.
7. **Correction path unreachable** from every rendered surface (criteria 11 PARTIAL / 14 FAIL) —
   live confirmation of PDVG-01 T1-B.

## One-run accounting

`AUTHORIZED RUN COUNT: 1` · `RUNS EXECUTED BEFORE THIS GATE: 0` (S2 §10 carried
`NO BENCHMARK RUN EXECUTED IN THIS RECORD VERSION`; no run evidence existed anywhere in the
repository) · `RUNS EXECUTED IN THIS GATE: 1` — exactly 2 cases × 2 languages × 2 perspectives
= **8 evaluation records**, no ninth record, no retries, no reruns; every record executed once in
a single pass · `FURTHER RUN AUTHORIZED: NO`.

## Material Gap & Improvement Sweep

`material_gap_sweep.json` — ten findings, each with evidence and a **proposed** tier
classification (`BLOCKING CANDIDATE` ×1, `TIER-1 CANDIDATE` ×5, `TIER-2 BEFORE PAID` ×1,
`OBSERVATION` ×2, `LATER STRATEGIC` ×1). **Review candidates only** — nothing is fixed,
reclassified, or activated by this record.

## No-fix confirmation

`PRODUCT CODE MODIFIED: NO` · `BENCHMARK CONTRACT MODIFIED: NO` · `CLASSIFIER MODIFIED: NO` ·
`DOMAIN PACK MODIFIED: NO` · `SECOND RUN EXECUTED: NO` · `MLC DEFINITION FROZEN: NO` ·
`PSRR GO: NO` · `DEPLOYMENT AUTHORIZED: NO` · `PRODUCTION AUTHORIZED: NO` ·
`PAID ACTIVATION AUTHORIZED: NO`
