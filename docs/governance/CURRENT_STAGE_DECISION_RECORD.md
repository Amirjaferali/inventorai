# CURRENT_STAGE_DECISION_RECORD

**Document ID:** CURRENT_STAGE_DECISION_RECORD
**Type:** Owner Decision Record
**Governance Level:** Level 3
**Status:** ACTIVE
**Date:** 2026-06-04
**Author:** Governance Manager
**Decision issued by:** Owner
**Analysis basis:** CURRENT_STAGE_POSITION_ANALYSIS.md

---

## 1. SUBJECT

```python
# engine/idea_state.py line 76
current_stage : int = 2  # 2 = Stage 2, 3 = Stage 3
```

Why is `current_stage` initialized to 2?
Is this intentional? Is Stage 1 bypassed?

---

## 2. REPOSITORY EVIDENCE

**CODE TRUTH at HEAD 8f994d9:**

`current_stage` was introduced in commit `7acf4c0` (Phase 1).
The inline comment names only two valid values: 2 and 3.
No `current_stage = 1` path exists anywhere in the engine.

`STAGE3_GAP_PRIORITY` and `GAP_PRIORITY` exist.
No `STAGE1_GAP_PRIORITY` exists.
No Stage 1 gap type constants exist.

`evaluate_transition()` operates on `maturity_level` (0, 1, 2),
not on `current_stage`. The `maturity_level = 0` path in
`run_iteration()` handles problem establishment and idea capture —
the functional equivalent of Stage 1 behavior.

---

## 3. GOVERNANCE EVIDENCE

SA-001A defines a three-stage journey:

- Stage 1: Situational Orientation (idea capture, problem articulation)
- Stage 2: Mechanism Knowledge Assessment
- Stage 3: Deliverable Reflection

Stage 1 is a valid governance and journey concept. It is not
deprecated. It describes the inventor's entry experience.

However, no governance artifact defines Stage 1 gap types,
Stage 1 questions, or Stage 1 runtime behavior. Stage 1 function
in the current engine is served by `maturity_level = 0` — the
path that establishes `known_problem` and captures `idea_summary`.

No implementation authorization for `current_stage = 1` has
been issued at any point in the project governance chain.

---

## 4. OWNER DECISION

**Decision Date:** 2026-06-04

**Decision:**

For MVP, Stage 1 is represented by `maturity_level = 0`.

`current_stage = 2` is intentional and remains unchanged.

`current_stage = 1` is not used in current runtime behavior.

Stage 1 remains a valid governance and journey concept,
but not a distinct runtime stage value in MVP.

**This is an MVP Scope Decision, not a Product Boundary Decision.**

Stage 1 is not absent from the product. It is served by the
existing `maturity_level = 0` path. The `current_stage` field
tracks Stage 2 / Stage 3 routing only, because those are the
stages that require active gap cascade routing logic.

---

## 5. IMPLICATIONS

### 5.1 Current runtime behavior

A new inventor begins at `maturity_level = 0, current_stage = 2`.

The `maturity_level = 0` path in `run_iteration()` handles:
- Idea summary capture (R-007: captured once)
- `known_problem` establishment
- First response quality assessment

This is the Stage 1 experience per SA-001A: the inventor
articulates their idea and problem for the first time.

Once `known_problem` is established with REASONED quality,
`evaluate_transition()` advances to `maturity_level = 1` and
the Stage 2 gap cascade begins (MECHANISM_COMPLETENESS opens).

The `current_stage` field becomes relevant at Stage 3:
when all Stage 2 gaps close and `current_stage == 3`,
the `STAGE3_GAP_PRIORITY` cascade activates.

### 5.2 What this decision does NOT change

- No code change required or authorized
- `current_stage = 2` default remains unchanged
- `maturity_level = 0` path remains the Stage 1 runtime equivalent
- Stage 1 governance concepts in SA-001A remain valid

### 5.3 Audit trail note

The `current_stage` field does not log Stage 1 activity
separately. Stage 1 activity is recorded in `iteration_log`
entries where `maturity_before = 0`.

---

## 6. NON-AUTHORIZED ALTERNATIVES

The following alternatives were considered and explicitly
not authorized at this time:

**Alternative A — Add `current_stage = 1` as a runtime value:**
Not authorized. Requires explicit governance authorization,
implementation design, and regression review.

**Alternative B — Add Stage 1 gap types and cascade:**
Not authorized. Requires STAGE1_GAP_TAXONOMY, question design,
and full governance chain equivalent to Stage 2 / Stage 3 work.

**Alternative C — Change `current_stage` default to 1:**
Not authorized. Would break Stage 2 cascade routing without
governance basis.

**Alternative D — Remove `current_stage` field:**
Not authorized. Field is required for Stage 3 routing (Phase 2).

---

## 7. FUTURE AUTHORIZATION PATH

If `current_stage = 1` is introduced in a future version:

1. Explicit governance authorization artifact required
2. Stage 1 gap type definition (if Stage 1 gaps are introduced)
3. Stage 1 question design (following same process as Stage 3)
4. Implementation design review
5. Regression review against WPS001 and cascade test suite
6. Owner authorization before commit

This path remains open. It is not foreclosed by this decision.

---

## 8. DECISION CLASSIFICATION

This is an **MVP Scope Decision**, consistent with the
classification of the single-archetype decision recorded in
`SINGLE_ARCHETYPE_SCOPE_DECISION.md`.

It records what is intentionally deferred, not what is
permanently excluded.

---

*This document is produced to be accurate, not reassuring.*
*No code was modified to produce this record.*
*Owner decision recorded as stated. No implementation authorized.*
