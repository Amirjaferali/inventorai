# Increment 2 — Truthful Gap and Evidence State — Bounded Implementation Contract

Status:
`DRAFT — NOT AUTHORIZED FOR IMPLEMENTATION`

This contract expressly relies on the separate authority-rulings document
`docs/governance/INCREMENT_2_AUTHORITY_RULINGS.md`
(`OWNER-RATIFIED AUTHORITY RULINGS — DRAFT — NOT YET COMMITTED`). It defines
bounded behavior only. It is not an implementation design and prescribes no
schema, field name, API, or UI.

## 1. Authoritative baseline

- Authoritative branch `origin/feature/atomic-json-session-persistence` at tip
  `2ec983b52a29e90aebf237f95ac61caf71ecd2c7`.
- Remote `main` `0e89e4636399760965c9ff8086b465c90dbadf8e`.
- Frozen persistence worktree `/home/user/inventorai` at
  `aec9cf6409efc18e125b6745762002f59e529654`, seven paused paths, untouched.

## 2. Objective

Correct the truthful representation of evidence source, validation, owner
disposition, current readiness, gap resolution rationale, and deliverable
certainty, while:

- preserving the six owner actions;
- preserving deterministic one-question-per-iteration behavior;
- preserving the stored forward-only gap lifecycle (WPS-001 INV-004);
- preserving the existing evidence-quality classification (ADR-003);
- preserving stored maturity transitions in the first contract;
- preserving WPS-001 and benchmark parity;
- remaining persistence-independent.

## 3. Stored behavioral requirements (no schema, no field names)

The implementation must require durable representation of:

1. provenance/source for each evidence or assertion record;
2. an explicit validation status independent of source and of evidence quality;
3. durable interaction disposition for all six owner actions;
4. explicit responsibility ONLY when created by an owner action (otherwise
   responsibility remains derived per the existing display behavior);
5. append-only evidence and disposition history;
6. stable coexistence of multiple source records for the same gap or question;
7. a contradiction-relationship capability;
8. a supersession-relationship capability without history deletion;
9. resolution rationale and the responsible source for any gap resolution;
10. backward-compatible defaults for legacy records (existing keyword
    construction and dataclass round-trips must keep working);
11. no provenance inference from text, quality, or technical vocabulary;
12. no automatic validation promotion.

## 4. Derived behavioral requirements

The implementation must derive, by pure deterministic recomputation:

- current readiness;
- current adequacy;
- blocking effect;
- truthful resolved/unresolved presentation;
- user-visible certainty;
- deliverable verdict;
- recommendation strength;
- eligibility presentation.

Derived results must:

- be recomputable on demand;
- never be stored as permanent truth;
- be capable of decreasing;
- never reverse the stored forward-only lifecycle;
- account for provisional, unknown, deferred, pending, contradicted, superseded,
  unvalidated, and validated states;
- never equate `REASONED` with verified;
- never equate `CLOSED` with universal technical truth.

## 5. Six-action behavioral contract

The six owner actions are preserved exactly: `answered`, `unknown`, `deferred`,
`provisional_assumption`, `specialist_requested`, `evidence_requested`. No
seventh action, no rename, no interaction redesign, no change to labels, purpose,
question wording, or routing.

For the first contract:

- `answered`: content may be stored with source and validation truth but is NOT
  automatically verified;
- `unknown`: durable and unresolved;
- `deferred`: durable, distinct from `unknown`, unresolved;
- `provisional_assumption`: durable, explicitly provisional, not verified;
- `specialist_requested`: durable specialist-pending state;
- `evidence_requested`: durable evidence-pending state.

## 6. Deliverable and presentation contract

Require truthful correction of:

- `REASONED` presentation where it currently implies technical substantiation
  beyond stored evidence;
- `PROCEED`;
- `PROCEED WITH CAUTION`;
- eligibility / "No unresolved items" semantics;
- evidence summaries;
- resolved presentation where validation or unresolved conflict does not support
  readiness;
- recommendation strength;
- source and validation labeling where displayed.

Preserve:

- factual stored open-gap counts;
- stored maturity levels;
- existing action labels;
- question wording and routing;
- the existing deliverable structure, except for truthful labeling and verdict
  derivation.

No broader UI or deliverable redesign is authorized.

## 7. Contradiction / supersession first-contract boundary

Mandatory:

- coexistence of multiple records;
- an explicit unresolved-conflict state;
- no destructive overwrite;
- history retention;
- a relationship compatibility seam;
- derived readiness accounts for unresolved conflicts.

Deferred (separate later authority):

- conflict-resolution workflow;
- source ranking;
- automated selection of a winning source;
- specialist collaboration;
- conflict-management UI.

## 8. Acceptance-test contract (mandatory first-contract)

The implementation, when later authorized, must satisfy acceptance tests for:

1. owner assertion is not verified;
2. owner assertion cannot independently justify verified readiness;
3. provisional assumption remains provisional;
4. unknown remains unresolved;
5. deferred remains distinct and unresolved;
6. specialist-requested remains pending;
7. evidence-requested remains pending;
8. specialist-provided differs from specialist-confirmed;
9. system suggestion differs from evidence;
10. documentary evidence differs from verbal assertion;
11. contradictory records coexist and remain unresolved;
12. superseded records retain history;
13. resolution records source and rationale;
14. derived readiness may decrease without reversing the stored lifecycle;
15. deliverables do not overstate certainty;
16. the six owner actions remain exact;
17. Increment 1 question behavior remains unchanged;
18. WPS-001, golden, replay, and `score_case()` parity is preserved outside
    intentionally changed truth semantics;
19. persistence is not required;
20. zero new non-baseline full-suite failures.

In addition, strict expected-failure tests reproducing the currently confirmed
defects (owner-text-becomes-REASONED-advances-maturity; deliverable over-claim;
non-durable dispositions) must be added BEFORE any production-source change. No
tests are written in this draft.

## 9. Allowed implementation surfaces to propose

Subject to a separate implementation authorization after source review, the
contract may propose later modification of only the minimum necessary surfaces,
expected to include:

- `engine/idea_state.py`;
- a new pure derived-readiness module (or a narrowly bounded equivalent);
- `engine/deliverable_assembler.py`;
- `web/app.py` only for the durable backend consequences of the existing six
  actions;
- narrowly necessary presentation templates for truthful labels only;
- new Increment 2 acceptance tests;
- narrowly necessary existing deliverable-test updates.

Exact allowed paths remain subject to separate implementation authorization after
source review.

## 10. Prohibited implementation surfaces

Explicitly prohibited:

- `engine/scoring.py`;
- `assess_response()` logic;
- `integrate_response()` logic;
- `evaluate_transition()` logic;
- golden/replay fixtures;
- domain packs;
- named ILT routes;
- the six-action set;
- question selection or display behavior;
- professional mode;
- specialist workspace;
- specialist marketplace;
- dynamic questionnaires;
- conversational clarification;
- LLM-generated follow-up;
- system analysis;
- persistence files;
- frozen persistence paths;
- database or migration work;
- domain expansion;
- Increment 1C as a separate execution lane;
- Increment 3 or later increments;
- Phase 5 or Phase 6;
- benchmark execution;
- final technical selection;
- reopening R2, FORM T, S-6, or AA-3/4/5.

## 11. Parity and test sequencing (for any later implementation authorization)

Required order:

1. create a dedicated implementation worktree from the then-current authoritative
   tip;
2. verify frozen persistence integrity;
3. capture baseline tests before source modification;
4. add strict expected-failure and acceptance tests first;
5. verify expected failures are confined to Increment 2 truthfulness;
6. implement only the authorized source scope;
7. rerun targeted tests;
8. rerun WPS-001 / golden / replay / Increment-1 / Path-N regressions;
9. run the full suite;
10. confirm zero new non-baseline failures;
11. source review;
12. staging;
13. commit;
14. push;
15. PR;
16. independent implementation review;
17. conditional true merge;
18. dedicated closure record and roadmap synchronization.

This draft authorizes none of these execution steps.

## 12. Protected states

Preserved without reopening: Increment 1A CLOSED; Increment 1B responsibility
guidance CLOSED; Increment 1B clarification display CLOSED FOR IMPLEMENTED DISPLAY
SCOPE; Increment 1 Owner–Expert Question Boundary CLOSED FOR ENFORCED
QUESTION-LAYER SCOPE; Increment 1C not separately activated; clarification
interaction unauthorized; system analysis unauthorized; persistence
`CONTINUE PRESERVE UNMODIFIED AND PAUSE`; benchmark NOT RUN; final technical
selection NONE; R2 HELD; FORM T BLOCKED; S-6 UNCLASSIFIED; AA-3/4/5 BLOCKED;
Phase 5/6 unauthorized; FDC-001 / FDC-002; WPS-001 authority; the active anchors.

## 13. Non-authorization

This contract:

- is a documentation draft only;
- is not yet committed authority;
- does not authorize Increment 2 implementation;
- does not authorize code or test changes;
- does not authorize staging, committing, pushing, or PR creation;
- does not authorize persistence;
- does not activate Increment 1C;
- does not authorize a maturity-transition change;
- does not authorize a specialist workspace or collaboration mode.

Any implementation requires a separate, explicit, repository-grounded owner
authorization for the exact scope, after source review of this contract.
