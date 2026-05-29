# ADR-005: Stall Detection Must Include PARTIAL Gap Status

**Status:** Accepted
**Date:** 2026-05-29
**Author:** InventorAI Architecture Review
**Depends on:** ADR-001, ADR-002, ADR-003, ADR-004
**Applies to:** engine/progression_loop.py (update_direction, run_iteration iteration counter)

---

## 1. Context

Validation campaign Session D (disclosure validation, 2026-05-29) demonstrated that
submitting three identical weak responses produced no stall signal. state.direction
remained PROGRESSING throughout. This is finding D-006 in the validation ledger.

Root cause investigation confirmed a structural mismatch between the gap lifecycle
as implemented and the stall detection model as designed.

The gap lifecycle in integrate_response():
- Any response (ASSERTED or REASONED) transitions gap.status from OPEN to PARTIAL or CLOSED
- ASSERTED response: gap.status = PARTIAL
- REASONED on OPEN: gap.status = PARTIAL (first attempt)
- REASONED on PARTIAL: gap.status = CLOSED

The stall detection model assumed a gap could remain OPEN across multiple weak responses
and accumulate an iteration count. In practice, the first response of any quality
immediately sets gap.status = PARTIAL.

Two coupled defects:

1. Iteration counter (run_iteration, line ~344):
   if g.status == OPEN:
       g.iterations_open += 1
   Counter freezes at 0 after the first response because the gap is no longer OPEN.

2. Stall detection check (update_direction, line ~323):
   if g.status == OPEN and g.iterations_open >= STALL_THRESHOLD
   Check requires OPEN status, which is never true after the first response.
   Counter never reaches STALL_THRESHOLD. Stall never fires.

The iterations_open lifecycle was confirmed clean:
- Initialized to 0 on Gap creation (idea_state.py line 46)
- Never reset anywhere in the codebase
- Per-gap: each Gap object has its own independent counter
- Cross-gap contamination is impossible: new gaps start at 0

---

## 2. Decision

Both the iteration counter and the stall detection check are extended to include
PARTIAL status alongside OPEN.

Counter change:
  FROM: if g.status == OPEN:
  TO:   if g.status in (OPEN, PARTIAL):

Stall detection change:
  FROM: if g.status == OPEN and g.iterations_open >= STALL_THRESHOLD
  TO:   if g.status in (OPEN, PARTIAL) and g.iterations_open >= STALL_THRESHOLD

No new fields. No IdeaState schema changes. No new counters. STALL_THRESHOLD unchanged.

---

## 3. Consequences

**Positive:**
- Stall detection fires correctly after STALL_THRESHOLD iterations on a gap that
  has received only ASSERTED responses.
- state.direction correctly reflects STALLED when an inventor is stuck.
- Governance Principle 2 (Improvement Not Generation) is restored: the platform
  can now guide inventors who are stuck rather than silently reporting PROGRESSING.
- D-006 is resolved.

**Unchanged:**
- STALL_THRESHOLD = 3 — threshold value correct, mechanism for reaching it was broken
- assess_response() — not modified
- integrate_response() — not modified; PARTIAL assignment is correct and relied upon
- evaluate_transition() — not modified
- _eligible() — not modified
- assemble_deliverable() — not modified
- GAP_PRIORITY — not modified
- IdeaState schema — no new fields
- Gap types — not modified
- GD-001 three-stage journey — not affected

**Interaction with ADR-004 (D-005 fix):**
These changes are orthogonal. ADR-004 governs evaluate_transition() maturity
advancement. ADR-005 governs update_direction() stall signalling. Neither touches
the other's function or contract.

---

## 4. Governance Compliance

- Governance Principle 1 (Inventor Ownership): preserved — stall fires on
  participation without quality, which correctly signals insufficient demonstration
- Governance Principle 2 (Improvement Not Generation): restored — platform now
  signals when inventor is stuck
- GD-001: Stage Two gap architecture unchanged
- ADR-004: D-005 fix untouched

---

## 5. Evidence

- Finding D-006, validation ledger, INVENTORAI_PROJECT_STATE_FREEZE_v1.2.md Section 4
- Session D screenshot evidence, 2026-05-29: three identical weak responses,
  no stall detection, Direction: PROGRESSING throughout
- Root cause trace: engine/progression_loop.py lines 323 and 344-346, confirmed 2026-05-29
- iterations_open lifecycle confirmed: no reset exists, per-gap isolation confirmed
