# S2 Path-N Release-Evaluation Run Record — S2-PATHN-RUN-002 (RVR-8)

STATUS: EVIDENTIARY RUN RECORD — NOT AN OWNER APPROVAL (S2 §11). NON-ACTIVATING.
A result authorizes nothing (S2 §0). This is the RVR-8 verification run — the "1 verification"
of the Owner-frozen Final Remediation Contract — executed under the separate Owner RVR-8 run
authorization. RVR-8 formal closure is a separate later gate; this record closes nothing.

## §10 template (with the §15.9 additional axes)

- **Run ID:** `S2-PATHN-RUN-002`
- **Benchmark version:** S2 §§0–14 + Path-N Release-Evaluation Extension v1 (§§15–17), byte-unchanged since run 001
- **Benchmark authoritative SHA:** `1f3d9d14b3b645df9595889861140910d63b918c`
- **Evaluated commit (exact RVR-8 EVALUATED RC SHA):** `1f3d9d14b3b645df9595889861140910d63b918c`
  — parents `12a94580…` / `2411f1d5…`, tree `97702884…`. RC basis: product paths `engine/ web/ domains/`
  byte-identical from the last product-changing merge `22c26881` (PR #589, RVR-7) through this tip;
  exactly one committed Path-N product state exists, and this is the only commit whose tree also
  carries every authoritative contract. **All 8 records used this one SHA — MIXED-SHA RUN: NO.**
- **Case versions:** `E-1 v1` (unchanged), `M-1 v1` (unchanged §15.2); frozen seeds byte-identical to run 001,
  Arabic seeds reused unchanged per §15.3.
- **Date:** 2026-08-28
- **Evaluator:** the Creator/Executor agent. Evaluation perspectives per §15.4 — not real users;
  no real-user claim is made anywhere in this record. Evaluator judgement is not deterministic and is
  not presented as such; agreement between evaluators is not claimed.
- **Environment:** in-process Flask test client against the committed application at the RC tree;
  `INVENTORAI_DB_PATH` bound to a dedicated run store (outside the repository);
  `AI_ADVISORY_ENABLED = False` throughout (asserted at import); no product AI call occurred.
- **Baselines:** A — FDC-001 decision-workspace export re-obtained live at the RC (status 200) for E-1;
  unobtainable for M-1 (workspace hard-coded to the bicycle case) → criterion 17 `NOT EVALUATED` with
  reason, per §15.8. B — the run-001 general-purpose one-shot responses reused BYTE-IDENTICAL
  (same frozen seeds ⇒ same baseline input; assistant named in the file; an evaluator activity outside
  the product; sha256 recorded in `baselineB_provenance.json`). C — the committed increment as executed.
- **Answer policy (comparability):** the run-001 frozen answer corpus replayed verbatim per
  gap type, perspective and language (`answer_maps.json`); no new gap type was encountered, so the
  disclosed evaluator fallback was never used. The corpus deliberately exercises NO structured
  disposition action, NO correction, and NO risk acceptance — identical to run 001, so every delta
  below is product behaviour, not answer-policy drift.
- **Harness defect disclosure:** a first harness attempt omitted the mandatory server-issued
  `answer_token`; the committed P4-1b-2a guard refused every answer fail-closed and NOTHING was
  evaluated (0 accepted answers in all 8 ledgers). Preserved as `run002_ABORTED_HARNESS_ATTEMPT/`;
  the evaluation itself executed exactly once after the harness supplied the token the page serves.
- **Core-gate conclusion (§15.7), per record:** R1 PARTIAL · R2 PARTIAL · R3 FAIL · R4 PARTIAL ·
  R5 PARTIAL · R6 FAIL · R7 PARTIAL · R8 FAIL. **No record achieved a full pass.**
  (Run 001: 2×PARTIAL / 6×FAIL → run 002: 5×PARTIAL / 3×FAIL; labels are per-record; no aggregate.)
- **Overall conclusion:** on the frozen cases, at this exact commit, against the governed baselines,
  using the approved criteria, the evaluated Path-N journey and deliverable **did not meet** the
  defined S2 release-value criteria in full on any of the eight records. The Wave-1…RVR-7 remediations
  are measurably live on the served surface (below); the bounded-decision core (candidate comparison)
  and the M-1 practitioner / E-1 Arabic-novice mechanism paths remain short of a full pass.

## The eight records (separate; never merged)

| Rec | Case | Lang | Perspective | Classifier on seed | Admission | Confirmed domain | Core gate |
|---|---|---|---|---|---|---|---|
| R1 | E-1 | EN | novice | `NONE` | NONE → explicit confirm | `electronics_electrical` | PARTIAL |
| R2 | E-1 | EN | expert | `NONE` | NONE → explicit confirm | `electronics_electrical` | PARTIAL |
| R3 | E-1 | AR | novice | `NONE` | NONE → explicit confirm | `electronics_electrical` | FAIL |
| R4 | E-1 | AR | expert | `NONE` | NONE → explicit confirm | `electronics_electrical` | PARTIAL |
| R5 | M-1 | EN | novice | `SINGLE` | classifier SINGLE → explicit confirm | `mechanical` | PARTIAL |
| R6 | M-1 | EN | expert | `SINGLE` | classifier SINGLE → explicit confirm | `mechanical` | FAIL |
| R7 | M-1 | AR | novice | `NONE` | NONE → explicit confirm | `mechanical` | PARTIAL |
| R8 | M-1 | AR | expert | `NONE` | NONE → explicit confirm | `mechanical` | FAIL |

## Remediation measurements (each vs the run-001 finding it answers; all traceable to raw evidence)

1. **Arabic substantive parity (RVR-7) — MEASURED LIVE.** All 24 questions in all four AR records
   rendered `lang="ar" dir="rtl"` (run 001: `lang="en" dir="ltr"` inside the RTL shell). The
   exhausted-gap reframe and the deliverable reader-facing structure (headings, labels, guidance) are
   fully Arabic. Persisting, registered, NOT a regression: generated substantive VALUES (verdict
   token, rationale, next-development-step text) remain English under Arabic labels — the
   generated-output language-parity obligation the Owner excluded from RVR-7 (its own DOR row).
2. **Honest exhaustion & dispositions (RVR-1/RVR-2) — MEASURED LIVE.** The reframe now states the
   honest options (add new information · unknown · deferred · provisional assumption · specialist ·
   evidence · accept as known risk) and the session serves those actions as first-class controls,
   including "Accept as known risk". The frozen corpus does not exercise them (by design, for
   comparability), so the journey still reaches the 24-interaction bound — reaching it is a finding
   about the corpus-replayed path, not a truncation.
3. **Perspective inversion (run-001 headline 3) — RESOLVED for E-1, PERSISTS on M-1.** The identical
   frozen practitioner answers that never closed E-1 MECHANISM in run 001 now close it at
   interaction 1 (R2, and Arabic R4) — the deterministic structured-substance assessment (RVR-3)
   measured working. M-1 practitioner answers still never close MECHANISM in 24 (R6, R8), and the
   E-1 Arabic-novice path still never closes it (R3).
4. **Correction reachability (run-001 headline 7 / T1-B / RVR-5) — REMEDIATED.** The correction
   ("withdraw and replace") affordance is rendered on the session surface in all 8 records
   (run 001: unreachable from every rendered surface). Correction semantics were not exercised by the
   frozen corpus; criteria 11/14 are PARTIAL with exactly that reason — no route-level claim.
5. **Provenance display divergence (run-001 headline 6) — RESOLVED.** No "pre-provenance session"
   text anywhere; the deliverable displays Owner-stated / not-validated consistent with the durable
   `OWNER_STATED` ledger (verified per record via the store's read API).
6. **Question repetition (run-001 headline 2) — PERSISTS, now honest.** The exhaustion reframe still
   repeats 17–19× per record; prepared question wording is identical across perspectives (register-
   adaptive wording NOT observed in this run); question SEQUENCE does adapt to answer content
   (R3 diverges from R4 at interaction 2 on identical banks).
7. **Deliverable eligibility — UNCHANGED.** No record reached `deliverable_eligible=true` or Stage 3;
   maturity ends at Level 1 in all 8; PHYSICAL_FEASIBILITY never closes on the corpus-replayed path.
8. **Truthfulness held everywhere — UNCHANGED.** REVISE verdicts with basis; explicit disclaimers
   ("nothing here has been built, tested, demonstrated, validated, certified, or shown feasible");
   no fabricated specifics; envelope carries `contract_version` / `engine_contract_version` /
   verbatim `seed_idea_text`; a 24-record append-only ledger per record.

## Known-failure-surface examinations (Owner authorization §11; observations only, no repairs)

1. *Increment-3 English constants in Arabic records:* CONFIRMED PRESENT (finding 1 above); registered
   obligation; measured cost carried by criteria 15/18/P6 in the AR records.
2. *Registry CWD/path binding:* the run executed with CWD = repository root (the binding's assumed
   layout); registry-served intent content loaded normally in all 8 records; the registered
   CONDITIONAL row's concern is deployment-layout, not this run — no effect on run validity observed.
3. *MG-8 / seed capture:* the seed is preserved verbatim in `seed_idea_text`; no `known_problem`
   seeding behaviour was claimed or measured; no journey-value anomaly attributable to it surfaced
   beyond the registered row.
4. *Served-route reachability:* every surface evaluated was reached through served routes
   (/ui-language, /start, /session/<sid>, /session/<sid>/deliverable); the one introspective capture
   (state/gap snapshots, assemble_deliverable meta, store read API) is capture, not evaluation surface.
5. *State reconstruction:* not exercised (no restart mid-record); envelope reconstruction inputs
   verified present per record (`engine_contract_version p4-2-level1-recon-v1`).
6. *Canonical-state consistency:* durable ledger count 24/24 per record; append-only; no divergence
   between displayed provenance and stored provenance (finding 5).
7. *Deterministic replay:* one pass per §15.9; repeatability was not separately re-executed (a
   re-execution would not be a retry of a divergent result — none diverged — and the one-run boundary
   was not spent on it); the determinism expectation remains an expectation, tested to the extent above.
8. *Fail-safe / fail-closed:* live evidence — the harness's own token omission was refused fail-closed
   with no state change and no disclosure (harness defect disclosure above).
9. *Product-value outcome:* carried per record by the criteria matrix and core gates; no full pass.
10. *Regression vs run 001:* NO CRITERION REGRESSED on any record. Movements: 4 FAIL→PARTIAL-or-PASS
    families (11 basis, 14, 15-AR, P5), provenance 4 PARTIAL→PASS, P1/P6 improvements on R2/R3/R4/R7,
    core gate 2×PARTIAL/6×FAIL → 5×PARTIAL/3×FAIL. Everything else unchanged.

## Limitations (§15.11, in full)

One evaluator; frozen synthetic cases; evaluation perspectives, not users; a 24-interaction bound per
record; Baseline A unobtainable for M-1; Baseline B authored once (run 001) by the named
evaluator-assistant and reused byte-identically; corpus-replay answer policy (structured dispositions,
corrections and risk acceptance deliberately unexercised). This run must not be described as
user research, market evidence, production readiness, or generalization beyond the frozen cases.
T1-A′ and T1-C′ remain separate; neither substitutes for the other.

## One-run accounting

`AUTHORIZED FOR THIS GATE: ONE second Path-N release-candidate run (separate Owner authorization; `
`OD-PDVG-01(a) previously EXERCISED AND CONSUMED by run 001)` · `RUNS EXECUTED IN THIS GATE: 1` —
exactly 2 cases × 2 languages × 2 perspectives = **8 evaluation records**, no ninth record, no
retries, no reruns (the aborted harness attempt evaluated nothing and is preserved as such) ·
`SECOND S2 RUN CONSUMED: YES` · `FURTHER RUN AUTHORIZED: NO`.
