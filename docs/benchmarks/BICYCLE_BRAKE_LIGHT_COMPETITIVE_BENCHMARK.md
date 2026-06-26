# Bicycle Brake-Light Competitive Benchmark

STATUS: GOVERNING COMPETITIVE BENCHMARK — NON-ACTIVATING EVALUATION RECORD

## 0. Non-Authorization Boundary

This record defines a repeatable competitive evaluation. It authorizes no
implementation; activates no lane; opens no MVP carve-out; creates no technical
selection; and creates no verification, test, or demonstration claim. It changes
no roadmap, anchor, hold, or closed state, and cannot be relied upon as execution
authorization.

Benchmark results measure product value. They do not create authority. A
favourable result authorizes nothing. An unfavourable result may prevent a
benchmark `PASS`, but it does not independently create a repository authorization
block or change any governed state.

## 1. Purpose and Benchmark Disambiguation

This is a competitive product-value benchmark comparing InventorAI's user-visible
performance against general-purpose AI assistance on the same case.

It is explicitly distinct from `benchmark/run_benchmark_v1.py` and from any
historical replay/regression benchmark already in the repository:
- the historical benchmark = replay/regression assessment of engine scoring
  behaviour;
- this benchmark = a repeatable commercial and product-value comparison of
  user-visible capability;
- neither substitutes for the other, and a result from one is not a result of the
  other.

## 2. Frozen Case Definition

Frozen benchmark case:
- product concept: bicycle automatic brake light;
- bounded technical decision: `braking-detection architecture`;
- user context: the inventor wants automatic brake indication without relying on
  manually pressing a light control;
- installation concern: avoiding or minimizing a physical wire connection to the
  brake lever;
- environmental concern: rough roads and vibration may produce false braking
  indications;
- required outcome: a bounded, evidence-classified technical-decision-readiness
  record, or a truthful blocked outcome.

The frozen case must not be silently changed between benchmark runs. Any
authorized case revision must record: a benchmark-case version; a reason; a date;
and an explicit comparison-impact note.

## 3. Bounded Candidate Set

Benchmark candidate set:
1. wired brake-lever switch;
2. accelerometer-based inference;
3. wheel-speed-based inference.

This set is a **bounded benchmark candidate set supplied by the authorized
decision specification**. It is NOT an exhaustive technical search; NOT proof that
the alternatives are compatible; NOT an externally verified catalog; NOT final
component selection; NOT `technically_selected`; and NOT `frozen`. Provenance and
vocabulary follow S1 and the controlling contracts: candidates carry
`artifact_origin_status=inferred` (provenance = the authorized decision
specification), `source_type=explicit_platform_inference`, and
`evidence_status=advisory`; each begins `option_status=active`.

## 4. Representative Benchmark Inputs

Stable representative input set (at least):
- known problem;
- known mechanism or proposed operating concept;
- explicit installation preference or constraint;
- rough-road / high-vibration condition;
- unknown acceptable false-positive rate;
- missing calibration or physical-test evidence;
- owner preference where applicable;
- evidence-quality distinctions.

Each input must be classified, keeping these distinct: owner requirement;
preference; soft constraint; mandatory constraint; user observation; platform
inference; missing evidence; physical test result. No physical result is invented;
where a physical/calibration result is absent it is recorded as missing evidence,
never fabricated.

## 5. Owner-Approved Evaluation Criteria

A benchmark run must assess all of the following:
1. exact difficult work completed by the platform;
2. work still delegated to the inventor;
3. requirements, preferences, and constraints correctly distinguished;
4. evidence and provenance visible for every material claim;
5. alternatives bounded and truthfully classified;
6. elimination or qualification reasons explicit;
7. bounded recommendation or truthful blocked outcome;
8. minimum next required input identified;
9. decision record version preserved;
10. normalized direct-input snapshot preserved;
11. response to a changed requirement;
12. affected prior decision marked internally with `validity_status=stale`;
13. `REVIEW REQUIRED` displayed only as a user-facing label;
14. exact change reason shown;
15. standalone export understandable without the conversation;
16. no prohibited technical-finality or verification claim;
17. user-visible improvement over the existing assessment-only FDC-001 output;
18. user-visible improvement over a generic AI report.

These criteria are owner-approved benchmark criteria. **Future benchmark results
are not automatically owner-approved.**

## 6. Mandatory Core Success Gate

An increment does not pass merely because one dimension improves. For the first
Technical Decision Workspace increment, ALL of these core outcomes must be
demonstrated:
- difficult work completed by the platform;
- evidence and provenance visibility;
- bounded recommendation or truthful block;
- versioned decision continuity;
- explicit stale / review-required behaviour after a relevant input change;
- standalone exportable value.

Failure of any one core outcome prevents a full-pass conclusion. Partial results
must be recorded truthfully and labelled `PARTIAL` or `FAIL` — never reported as
successful.

## 7. Comparison Baselines

At least three baselines:
- **Baseline A — Existing FDC-001 Assessment:** measure what the current
  assessment-only output completes and what it still delegates.
- **Baseline B — General-Purpose AI Response:** measure a general conversational
  response that may suggest alternatives and next steps but lacks governed
  persistent technical continuity. Do not name or disparage a vendor unless
  supported by a dated, reproducible benchmark run.
- **Baseline C — InventorAI Current Increment:** measure the actual committed
  user-visible increment under evaluation. Do not credit planned or documented
  capabilities that are not implemented and observable.

## 8. Repeatable Evaluation Protocol

Each benchmark run must record: run ID; benchmark record version; frozen case
version; evaluated commit SHA; evaluated branch or release identifier; execution
date;
evaluator; environment; exact user inputs; exact generated outputs or artifact
references; evidence sources used; unsupported or missing evidence;
criteria-by-criteria result; core success-gate result; regressions; limitations;
and the final comparison conclusion.

Screenshots, exports, logs, or artifacts should be referenced where available. No
benchmark result may claim a test, demonstration, compatibility, or safety finding
unless that evidence actually exists.

## 9. Result Vocabulary

Benchmark-evaluation labels (these do NOT alter or substitute for any committed
product or authority enum):
- `PASS`: criterion demonstrably satisfied by committed observable behaviour;
- `PARTIAL`: some observable value exists but the criterion is incomplete;
- `FAIL`: criterion is absent, contradicted, or delegated without sufficient
  platform work;
- `NOT EVALUATED`: evidence was unavailable or the run did not assess it.

These are evaluation labels only — NOT decision statuses, readiness statuses,
evidence statuses, authorization statuses, or verification outcomes. They must
never be written into product artifacts as those enums.

## 10. Versioned Benchmark Run Template

Reusable template (one per run):
- Run ID:
- Benchmark version:
- Case version:
- Evaluated commit:
- Date:
- Evaluator:
- Baseline compared:
- Inputs:
- Platform outputs:
- Difficult work completed:
- Work delegated:
- Evidence/provenance result:
- Decision-readiness result:
- Change-impact result:
- Export result:
- Prohibited-claim check:
- Criteria table (1–18, each `PASS`/`PARTIAL`/`FAIL`/`NOT EVALUATED`):
- Core-gate conclusion:
- Limitations:
- Overall conclusion:

`NO BENCHMARK RUN EXECUTED IN THIS RECORD VERSION.` (The template above is empty;
no run has been executed and no result is recorded in this version. A completed
run must not be fabricated.)

## 11. Result Approval and Interpretation

- Benchmark criteria and protocol may be owner-approved;
- individual benchmark results are evidentiary records, not owner approvals;
- a result does not activate a lane or authorize implementation;
- a positive benchmark does not prove production readiness;
- a negative benchmark must not be concealed;
- results must remain linked to the evaluated commit;
- a later product change does not rewrite an earlier result;
- later runs supersede conclusions only for their own evaluated versions, not the
  historical facts of earlier runs.

## 12. Update Rules

A new versioned benchmark run is required after: a major user-visible increment; a
relevant decision-workspace behaviour change; a change to evidence classification;
a change to versioning or stale-detection behaviour; a change to standalone export;
or a regression fix affecting any mandatory criterion.

A governance-only documentation change does NOT trigger a product-value benchmark
run unless it changes user-visible behaviour.

## 13. Preserved Scope and Holds

This record does not authorize: Commit B; lane activation; code; external-source
integration; persistence delivery; final component selection; `technically_selected`;
`frozen`; BOM; wiring; firmware; compilation; simulation; physical testing;
demonstration claims; certification; production readiness; Path T; or multi-domain
expansion.

Preserved: `PRESERVE UNMODIFIED AND PAUSE`; Roadmap §§4–7 unchanged; lane INACTIVE;
and all existing holds and closed states (R2=HELD · FORM T=BLOCKED ·
S-6=UNCLASSIFIED · AA-3/AA-4/AA-5=BLOCKED · Phase 5/6=UNAUTHORIZED · ILT-002
evidence collection=NOT AUTHORIZED · Path T=BLOCKED · Phase 4=CLOSED ·
Gate 8=CLOSED · runtime_integrated=TRUE).

## 14. Relationship to S1 and Future S3

See `docs/governance/INVENTORAI_COMMERCIAL_DIFFERENTIATION_DIRECTION.md`.
- S1 defines the strategic commercial direction;
- S2 (this record) defines the repeatable evaluation mechanism;
- S2 does not amend or override S1;
- both remain non-activating;
- mandatory agent reading-order enforcement will be added only through the
  separately authorized S3 edit to `CLAUDE.md`.
