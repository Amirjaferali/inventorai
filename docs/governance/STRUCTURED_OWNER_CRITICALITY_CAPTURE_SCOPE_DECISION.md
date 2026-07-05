# Structured Owner Criticality Capture — Owner Scope Decision Record

## 1. Status

`COMMITTED OWNER SCOPE DECISION RECORD — FUTURE NON-ACTIVATING MVP CANDIDATE ADMITTED; NOT ACTIVATED`

No implementation is authorized by this record. This record is documentation-only
and non-activating. It admits *Structured Owner Criticality Capture* as a future
candidate only; it does not activate an implementation lane, does not amend the MVP
scope freeze as an activating expansion, and does not create or imply any downstream
authorization. See §7 for the explicit non-authorization clause.

Authoritative baseline at drafting:
`5f8ce10b6bc51dbba30b76440f7ee7a426bc1471` (feature/atomic-json-session-persistence
tip; PR #96 roadmap-sync two-parent merge, parents `9fcef3a` then `07d3e25`). The
live tip is always resolved from Git; this SHA is a publication baseline, not a
permanent live-tip assertion.

## 2. Source governance (authority order; this record is subordinate to all)

Read in the CLAUDE.md-ordered authority set. Where any of these and this record
could differ, they control:

- `ILT-002_GOVERNANCE_ANCHOR.md`, `OWNER_PRODUCT_IDENTITY_CORRECTION.md`,
  `STRATEGIC_PRODUCT_VISION.md`, `PATH_N_CURRENT_EXECUTION_ANCHOR.md`,
  `DUAL_PATH_PRODUCT_ANCHOR.md`, `ACTIVE_EXECUTION_ROADMAP.md`;
- the merged Increment 4 authority/design/contract
  (`INCREMENT_4_AUTHORITY_RULINGS.md` — C4-R4/C4-R5/C4-R6; `INCREMENT_4_DESIGN.md`
  — D-4/D-5; `INCREMENT_4_IMPLEMENTATION_CONTRACT.md` §9.7); Increment 5;
- `MVP_SCOPE_FREEZE.md` — ACTIVE FREEZE, authority rank 1; this record does NOT
  amend or expand it and does not satisfy its REVISION PROTOCOL;
- `docs/governance/STRUCTURED_OWNER_CRITICALITY_CAPTURE_DESIGN.md` (PR #95) — the
  non-activating design this record dispositions;
- precedent artifact type: `MVP_SCOPE_REVISION_DECISION_RECORD.md`,
  `SINGLE_ARCHETYPE_SCOPE_DECISION.md` (documentation-only owner scope decisions).

## 3. Decision

**Structured Owner Criticality Capture is ADMITTED ONLY AS A FUTURE CANDIDATE — NOT
as an active implementation lane.** The owner records that the feature (per the
PR #95 design) is an acceptable *future* direction to consider, and nothing more.

1. **Future candidate only.** The feature is recorded as a candidate for a future
   owner-confirmed, structured-only criticality signal. It is not an active lane and
   confers no execution authority.
2. **Non-activating until all future gates are satisfied.** It remains
   NON-ACTIVATING until every gate in §4 is complete.
3. **The current MVP freeze remains ACTIVE.** This record does not expand the
   frozen scope and does not satisfy the freeze's REVISION PROTOCOL (which requires
   real-usage evidence — 3 real ideas through LEVEL 0-2, ≥1 genuine BLOCK understood
   by the inventor, ≥1 idea reaching LEVEL 2 with documented clarity improvement, a
   missing gap/rule identified through real usage, not anticipation).
4. **Current runtime behavior is unchanged.** Criticality remains
   `UNDETERMINED (system-derived)` unless and until a future, separately-approved
   structured owner signal exists. No deliverable output changes by this record.

## 4. Gates that MUST be satisfied before any implementation (all required, in order)

Implementation remains **BLOCKED** pending ALL of:

1. **MVP scope authority** — either the `MVP_SCOPE_FREEZE.md` REVISION PROTOCOL
   evidence is satisfied, OR an explicit later owner-approved scope amendment admits
   the feature into active scope. (This record is neither.)
2. **A separate Increment Contract** — a sibling to Increment 4/5 fixing exact
   semantics, the structured field, category mapping, rendering, backward-compatible
   defaults, and test obligations (tests-first authority is granted there, not here).
3. **Tests** — the contract's required test package.
4. **Independent review** — strict read-only review of the implementation.
5. **Owner-authorized true merge** — a two-parent merge, then post-merge
   verification, per the discipline used for prior increments and PRs #91–#96.

No step above is authorized by this record.

## 5. Boundaries the feature MUST preserve if ever implemented

If (and only if) a future contract implements it, the feature MUST remain:

- **structured owner selection only** (a discrete owner choice, never free text
  parsed for meaning);
- **owner-confirmed only** (C4-R5 authority `owner-confirmed`, sourced solely from
  the discrete owner selection);
- **advisory only**;
- **not technically validated**;
- **not safety validated**;
- **not build-ready**;
- **not certification-ready**;
- **not market-ready**.

Default behavior stays `Criticality: UNDETERMINED (system-derived)` when no
structured owner signal exists.

## 6. Explicit prohibitions (carried from the PR #95 design; binding on any future work)

- no free-text criticality extraction;
- no keyword detection;
- no semantic parsing of prose;
- no LLM / heuristic inference of criticality from free text;
- no automatic risk generation (from prose or otherwise); `_s6` remains unchanged
  (D-5/C4-R6);
- no system inference shown as `owner-confirmed` (C4-R5);
- no new active criticality category without separate C4-R4 approval (the governed
  vocabulary remains `FEASIBILITY-THREATENING / VALUE-ENHANCING / REFINEMENT /
  UNDETERMINED`);
- no persistence work;
- no `main` synchronization.

## 7. Explicit non-authorization clause

This document does **not** authorize:

- implementation;
- MVP scope activation or an activating freeze expansion;
- an Increment Contract;
- schema, session-state, UI/question-flow, template, or test changes;
- any runtime behavior change (criticality output is unchanged);
- a PR merge;
- a `main` sync.

This record is an owner disposition only. It confers no authority by implication,
does not create or imply downstream authorization, and is subordinate to every
document in §2. Absent a separate, fully-approved Increment Contract and the
applicable authorizations, the current Increment 4 behavior
(`UNDETERMINED (system-derived)`) remains the only conformant output, and the MVP
freeze remains fully effective.
