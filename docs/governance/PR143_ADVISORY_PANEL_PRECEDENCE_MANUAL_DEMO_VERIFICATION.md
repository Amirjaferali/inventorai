# PR #143 — Advisory Panel Precedence / Supportive Surface Consolidation — Manual Demo Verification

## 1. Evidence state

- **Repository:** `Amirjaferali/inventorai`
- **Authoritative branch:** `feature/atomic-json-session-persistence`
- **Authoritative tip at time of demo:** `57bf94021433de170042255d142e787bb389522b`
- **Latest merged PR:** `#143`
- **Merge commit:** `57bf94021433de170042255d142e787bb389522b`
- **Ordered parents:**
  - First parent: `fa5fb28463ea2952c64d0508a1ffcc72d3be919e`
  - Second parent: `98b1bd6a49f09ca9f2fe34747f860175d38dbf08`
- **Implemented increment:** Advisory Panel Precedence / Supportive Surface Consolidation
- **Official state:** `DEMO_READY_WITH_LIMITATIONS`
- **MVP scope:** electronics/electrical-only

## 2. Demo method

- Runtime exercise of the **merged, committed** Flask application via the Flask
  test client (no code path re-authored for the demo).
- Executed inside a **read-only detached worktree** checked out at the merge tip
  `57bf94021433de170042255d142e787bb389522b`.
- **No source, test, or template change** was made to perform the demo.
- **No artifact was created** during the demo step itself.
- The temporary worktree was **removed afterward**.

This document records the observed behavior only. It exercises the committed
merge; it does not reimplement, re-derive, or re-score anything.

## 3. Scenario evidence

### Scenario A — English uncertainty ("I don't know" / unknown action)
- **Result:** The **uncertainty** guidance panel is the single primary advisory
  surface. The **scaffolding** and **co-authoring** panels are suppressed only as
  *competing open primary panels* (not removed from the product).
- Truthful surfaces preserved: `last_result` badge/reason, acknowledged unknowns,
  gaps list, interaction acknowledgment, and the Next Development Step callout.
- The clarification expander remains **collapsed** (on-demand, not forced open).
- The form still exposes the **six** honest actions (no seventh action).

### Scenario B — WARN scaffolding primary when not uncertain
- **Result:** The **scaffolding** guidance panel is primary. The **uncertainty**
  panel is absent (no uncertainty cue), and **co-authoring** is suppressed as a
  competing open primary.
- The WARN badge, its reason, the development direction, and the gap surfaces are
  all preserved and visible.

### Scenario C — PASS / non-uncertainty / non-WARN
- **Result:** The **co-authoring** panel is primary. The **uncertainty** panel is
  absent and the **scaffolding** panel is absent.
- The co-authoring surface is **advisory only**: no save, no approve, no apply
  control is present.
- **No hidden clarified-answer fields** are emitted. The user remains the sole
  author of the answer.
- This confirms co-authoring suppression elsewhere is **reversible by state**, not
  a removal.

### Scenario D — Arabic uncertainty ("لا أعرف")
- **Result:** The **uncertainty** guidance panel is primary. The **co-authoring**
  and **scaffolding** panels are suppressed only as *competing open primary panels*.
- Arabic / RTL supportive behavior is acceptable.
- **Answer Clarification / Improve Wording is not activated** by the Arabic path.

### Scenario E — Unsupported non-electronics idea
- **Result:** The electronics/electrical MVP **domain gate is preserved**. The
  unsupported idea does not create a session and does not expand the supported
  domain.

## 4. Provenance / forbidden-behavior checklist

None of the following occurred during the demo or in the merged behavior observed:

- [none] answer rewriting
- [none] suggested clarified answer
- [none] approve / save / apply clarified-answer flow
- [none] hidden generated-guidance fields
- [none] schema change
- [none] scoring change
- [none] persistence change
- [none] session transcript change
- [none] deliverable / report behavior change
- [none] Safety Signals reopening
- [none] domain expansion
- [none] seventh action
- [none] `main` movement
- [none] frozen persistence movement
- [none] quarantined scratch movement

## 5. Protected refs (unchanged)

- `main`: `0e89e4636399760965c9ff8086b465c90dbadf8e`
- Frozen persistence worktree / commit: `aec9cf6409efc18e125b6745762002f59e529654`
- Quarantined scratch branch: `02586747c902d5e1ebb78adde54ddd4ecd1c174a`

## 6. Final classification

`MANUAL DEMO EVIDENCE COMPLETE — PR #143 ADVISORY PANEL PRECEDENCE VERIFIED — ROADMAP SYNC STILL REQUIRED`
