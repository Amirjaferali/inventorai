# Increment 2 — Truthful Gap and Evidence State — Authority Rulings

Status:
`OWNER-RATIFIED AUTHORITY RULINGS — DRAFT — NOT YET COMMITTED`

## 1. Title and status

This document records the binding owner rulings that result from the completed
read-only Increment 2 readiness assessment and implementation-contract
assessment. It is a documentation draft. It is owner-ratified in content but is
NOT yet committed authority until it is reviewed, committed, and integrated into
the authoritative branch. Until then it authorizes nothing.

These rulings govern the companion draft
`docs/governance/INCREMENT_2_IMPLEMENTATION_CONTRACT.md`.

## 2. Authoritative repository baseline

- Authoritative remote branch: `origin/feature/atomic-json-session-persistence`.
- Authoritative tip at drafting: `2ec983b52a29e90aebf237f95ac61caf71ecd2c7`
  (PR #35 true-merge; ordered parents
  `68f7dcbe4f0ff9b53f9acd6ce33c5c00708274e9` then
  `25d43afdd56868444910d1a37111b78c26284907`).
- Remote `main`: `0e89e4636399760965c9ff8086b465c90dbadf8e`.
- Authoritative roadmap at the tip: `docs/governance/ACTIVE_EXECUTION_ROADMAP.md`
  (713 lines, 65965 bytes,
  SHA-256 `4b6a6e0c19fabe41c14b6f13ee7874262ad38395e4762a68e5b1ddd921d25853`).
- Frozen persistence worktree `/home/user/inventorai` at
  `aec9cf6409efc18e125b6745762002f59e529654`, seven paused paths, untouched.

## 3. Purpose

To record the owner rulings required before the Increment 2 implementation
contract can be bounded, and to fix the exact authority interpretation under
which a later, separately authorized implementation may proceed. This document
resolves the authority questions raised by the implementation-contract
assessment; it does not authorize implementation.

## 4. Evidence basis

These rulings rest on the completed read-only assessments, re-verified against
committed source at the authoritative tip:

- owner text alone may currently classify as `REASONED`, advance stored
  maturity, and partially or fully address a gap with no source or validation
  provenance (`engine/progression_loop.py`: `assess_response`,
  `integrate_response`, `evaluate_transition`);
- the deliverable may present stronger certainty than stored evidence supports
  (`engine/deliverable_assembler.py`: quality labels, `_RECOMMENDATION_A`,
  resolved-gap reporting, eligibility);
- the five non-answer owner actions are recorded only as ephemeral session-dict
  metadata and are not durably represented in `IdeaState` (`web/app.py`
  `submit_answer`);
- evidence quality (ADR-003 `ASSERTED`/`REASONED`/`DEMONSTRATED`) is a
  reasoning-structure axis only; it is not provenance and not validation;
- the six visible owner actions are closed Increment 1 behavior;
- the session `IdeaState` is in memory and is not serialized to disk, so
  Increment 2 is persistence-independent;
- contradiction and supersession are within the committed epistemic direction
  (`EPISTEMIC_FOUNDATION_DESIGN_DECISION.md` §5.4, §7);
- the WPS-001 forward-only stored gap lifecycle (INV-004) and deterministic gate
  behavior (INV-007) must remain intact;
- current readiness and verdict must be derived rather than treated as permanent
  stored truth (`EPISTEMIC_FOUNDATION_DESIGN_DECISION.md` §6).

Governing authority, in order: `MVP_SCOPE_FREEZE.md`; the active anchors and
`STRATEGIC_PRODUCT_VISION.md` §7; `CLAUDE.md`; `EPISTEMIC_FOUNDATION_DESIGN_DECISION.md`;
`docs/adr/ADR-003-evidence-quality-model.md`;
`INVENTORAI_PRODUCT_VALUE_CORRECTION_PLAN.md`; WPS-001 invariants
(`tests/test_wps001_invariants.py`); `ACTIVE_EXECUTION_ROADMAP.md`.

## 5. Scope-freeze interpretation ruling (Ruling 2)

Increment 2 is classified as:

`A CONFORMANCE FIX WITHIN THE EXISTING MVP SCOPE FREEZE`

Recorded explicitly:

- it corrects truthfulness inside already-authorized idea-development, gap,
  maturity, recommendation, and deliverable behavior;
- it does not introduce a new product mode or capability;
- provenance and validation status are NOT the frozen uncertainty model
  identified in `MVP_SCOPE_FREEZE.md` as `UNVERIFIABLE` / `HYPOTHETICAL`;
- Increment 2 adds no scoring system;
- `engine/scoring.py:score_case()` and its benchmark role remain unchanged;
- no scope-freeze amendment is required;
- this ruling is an interpretation of the existing freeze, not an expansion of
  it. It is consistent with `INVENTORAI_PRODUCT_VALUE_CORRECTION_PLAN.md` §9,
  which classifies "Increments 1 and 2 [as enforcing] committed governance" —
  the most defensible posture under the freeze — and with §13, which records that
  no standalone anchor amendment is required.

## 6. WPS-001 / `CLOSED` interpretation ruling (Ruling 3)

The following interpretation is authorized:

- stored gap lifecycle remains forward-only;
- stored `CLOSED` is a historical lifecycle state;
- stored `CLOSED` does NOT mean universal technical truth, verified evidence, or
  permanent current adequacy;
- derived readiness may present below stored `CLOSED` or stored maturity where
  current evidence is unvalidated, provisional, pending, contradicted, or
  superseded;
- derived readiness may decrease without reversing stored lifecycle;
- user-visible verdict, readiness, certainty, and recommendation must use current
  derived truth;
- WPS-001 invariants and deterministic gate behavior remain preserved.

This is a dedicated owner interpretation ruling. It edits no WPS-001 test and no
existing ADR. It is consistent with `EPISTEMIC_FOUNDATION_DESIGN_DECISION.md` §4
("`CLOSED` must not be interpreted as universal technical truth") and §6 (derive
stage readiness, blocking effect, deliverable verdict, current adequacy).

## 7. Selected bounded alternative (Ruling 1)

Selected:

`BOUNDED ALTERNATIVE D WITH A MANDATORY C-COMPATIBLE RELATIONSHIP SEAM`

Meaning:

- implement the smallest truthful correction;
- include minimum provenance, validation, durable disposition, resolution
  rationale, and derived readiness semantics;
- include a stable coexistence capability for contradiction and supersession;
- defer a full contradiction-resolution workflow, source-priority algorithm,
  collaboration workflow, and related UI.

Full Alternative C is NOT selected for the first contract. A minimal Alternative
D that lacks relationship compatibility is NOT selected.

## 8. Maturity-boundary ruling (Ruling 4)

Selected:

`PRESENTATION-AND-VERDICT CORRECTION ONLY FOR THE FIRST CONTRACT`

Therefore for the first contract:

- leave `assess_response()` unchanged;
- leave `integrate_response()` unchanged;
- leave `evaluate_transition()` unchanged;
- leave stored maturity transitions unchanged;
- do NOT gate stored maturity on validation in the first contract;
- introduce and use derived readiness for user-visible adequacy, verdicts,
  recommendations, and truthful labels;
- any future change to `evaluate_transition()` requires separate
  protected-function authorization and parity evidence (ADR-003 §4 Rule 4;
  `EPISTEMIC_FOUNDATION_DESIGN_DECISION.md` §8).

## 9. Provenance / Increment 1C ruling (Ruling 5)

The minimum provenance required for Increment 2 is authorized inside Increment 2
itself. Recorded:

- Increment 1C is NOT activated as a separate execution increment;
- the committed identity of Increment 1C
  (`EPISTEMIC_FOUNDATION_DESIGN_DECISION.md` §7, "Provenance metadata, optional
  until proven necessary") is acknowledged;
- provenance has now been proven necessary for Increment 2 truthfulness (to
  separate owner assertion from verified, and specialist-provided from
  specialist-confirmed);
- including minimum provenance in Increment 2 does NOT reopen Increment 1 and
  does NOT create a separate Increment 1C implementation;
- Increment 2 remains independently named and governed.

## 10. Contradiction/supersession ruling (Ruling 6)

Required in the first contract:

- multiple source records may coexist;
- contradictory records may coexist without silent overwriting;
- superseded records retain history;
- a stable compatibility seam exists for contradiction and supersession
  relationships;
- unresolved conflicts prevent derived verified/ready presentation where
  relevant.

Deferred (each requires separate later authority):

- resolution workflow;
- source-ranking algorithm;
- automated conflict reconciliation;
- specialist collaboration UI;
- "which source wins" automation.

## 11. Responsibility ruling (Ruling 7)

Required:

- responsibility remains derived by default for existing display behavior
  (the current advisory render-time labels);
- explicit responsibility becomes durable only when an owner action creates a
  durable fact;
- `specialist_requested` creates durable specialist-pending responsibility;
- `evidence_requested` creates durable evidence-pending responsibility;
- default responsibility remains undetermined;
- responsibility never implies that the requested source has provided or
  confirmed information.

No storage field names are specified by this ruling.

## 12. Transcript/audit ruling (Ruling 8)

Required durable state history for:

- selected interaction disposition;
- actor/source;
- original evidence or assertion;
- validation event;
- contradiction;
- supersession;
- resolution rationale and source.

Classification:

- durable state history is mandatory;
- transcript projection is optional;
- transcript redesign is out of scope.

## 13. Parity ruling (Ruling 9)

The parity-proof plan is approved:

- baseline capture occurs before source changes;
- parity is rerun after implementation;
- WPS-001 invariants remain unchanged;
- `score_case()` remains unchanged;
- golden and replay behavior remains unchanged;
- Increment 1A, Increment 1B, Path N, and Owner–Expert question behavior remain
  unchanged;
- domain-registry failures remain isolated to the accepted baseline
  (`tests/test_domain_registry.py`);
- zero new non-baseline full-suite failures are allowed.

Accepted full-suite baseline: `633 passed, 31 failed, 1 skipped, 1 xfailed,
24 xpassed`, with all 31 failures confined to `tests/test_domain_registry.py`.

## 14. Persistence ruling (Ruling 10)

Increment 2 remains persistence-independent. No persistence file, frozen overlay
path, session-store implementation, database, migration, or reconciliation work
is permitted. Future persistence must later serialize the committed Increment 2
semantics under separate authority. The frozen persistence worktree remains under
`CONTINUE PRESERVE UNMODIFIED AND PAUSE`.

## 15. Protected states

These rulings change nothing and preserve, without reopening:

- Increment 1A CLOSED;
- Increment 1B responsibility guidance CLOSED;
- Increment 1B clarification display CLOSED FOR IMPLEMENTED DISPLAY SCOPE;
- Increment 1 Owner–Expert Question Boundary CLOSED FOR ENFORCED QUESTION-LAYER
  SCOPE;
- Increment 1C not separately activated;
- clarification interaction unauthorized;
- system analysis unauthorized;
- persistence `CONTINUE PRESERVE UNMODIFIED AND PAUSE`;
- benchmark NOT RUN;
- final technical selection NONE;
- R2 HELD; FORM T BLOCKED; S-6 UNCLASSIFIED; AA-3/AA-4/AA-5 BLOCKED;
  Phase 5/6 unauthorized;
- FDC-001 / FDC-002 committed closure facts;
- WPS-001 authority;
- the active anchors.

## 16. Non-authorizations

This document:

- is a documentation draft only;
- is not yet committed authority;
- does not authorize Increment 2 implementation;
- does not authorize code or test changes;
- does not authorize staging, committing, pushing, or PR creation;
- does not authorize persistence;
- does not activate Increment 1C;
- does not authorize a maturity-transition change;
- does not authorize a specialist workspace or collaboration mode.

## 17. Relationship to the implementation contract

These rulings are the authority basis for
`docs/governance/INCREMENT_2_IMPLEMENTATION_CONTRACT.md`. That contract is a
bounded behavioral contract and expressly relies on this document. Neither file
authorizes implementation. The contract may later be reviewed for a separate,
explicit implementation authorization.

## 18. Owner decision summary

| # | Ruling | Decision |
|---|--------|----------|
| 1 | Implementation direction | Bounded Alternative D with a mandatory C-compatible relationship seam |
| 2 | Scope-freeze | Conformance fix within the existing MVP scope freeze (interpretation, not amendment) |
| 3 | WPS-001 / `CLOSED` | Stored lifecycle forward-only; derived readiness may present below stored `CLOSED`/maturity |
| 4 | Maturity boundary | Presentation-and-verdict correction only; `evaluate_transition()` unchanged |
| 5 | Provenance / 1C | Minimum provenance authorized inside Increment 2; 1C not separately activated |
| 6 | Contradiction/supersession | Coexistence + seam required; resolution workflow deferred |
| 7 | Responsibility | Derived by default; durable only when an owner action creates a fact |
| 8 | Transcript/audit | Durable state history mandatory; transcript projection optional; redesign out of scope |
| 9 | Parity | Baseline before, rerun after; WPS-001/score_case/golden/replay/Increment-1/Path-N unchanged; zero new non-baseline failures |
| 10 | Persistence | Persistence-independent; no persistence work permitted |
