# Increment 3 — Visible Next Development Step — Owner Authority Rulings

Status:
`OWNER-RATIFIED AND MERGED AUTHORITY RULINGS (R-1–R-4)`
`PROPOSED CORRECTION DRAFT (R-5–R-6) — NOT YET COMMITTED — NON-OPERATIVE UNTIL INDEPENDENTLY REVIEWED, COMMITTED, AND MERGED`

This document records the owner's binding rulings that resolve the conditional
disposition of the completed read-only Increment 3 readiness assessment
(`INCREMENT 3 READINESS CONDITIONAL — OWNER RULING REQUIRED`). It is the
repository authority for bounding Increment 3. It authorizes the companion
bounded implementation contract `INCREMENT_3_IMPLEMENTATION_CONTRACT.md` to be
drafted; it does NOT authorize source or test implementation.

## 0. Authoritative baseline

- Authoritative branch `origin/feature/atomic-json-session-persistence` at tip
  `408385f3a7461393e8e9dc0b9f4e1c6433a0f5ce` (PR #39 roadmap-synchronization
  true-merge; ordered parents `66415d41515f5a6bf379549f0e4547a5b15ce127` then
  `1c79c701ecb684b14b93e8cb4cee9db0c0d99435`).
- Increment 2 — Truthful Gap and Evidence State — is IMPLEMENTED, TRUE-MERGED
  (PR #38, merge `66415d41515f5a6bf379549f0e4547a5b15ce127`), POST-MERGE VERIFIED,
  and CLOSED FOR IMPLEMENTED SCOPE; the roadmap is synchronized.
- Remote `main` `0e89e4636399760965c9ff8086b465c90dbadf8e` is outside this lane.
- Frozen persistence worktree `/home/user/inventorai` at
  `aec9cf6409efc18e125b6745762002f59e529654`, seven paused paths,
  `CONTINUE PRESERVE UNMODIFIED AND PAUSE`.

## 1. Product purpose

Increment 3 converts Increment 2's truthful evidence and readiness state into one
visible and actionable next development step for the user's idea. Increment 3
develops the IDEA, not the inventor. It adds no new truth; it makes the existing
truthful state visible and actionable.

## 2. Rulings

### R-1 — Unified scope

Increment 3 is one coherent user-visible capability: `NEXT DEVELOPMENT STEP`.
It combines, as typed outputs of a single derived guidance flow:

- one prioritized next action;
- gap-specific evidence-request guidance;
- structured specialist-handoff preparation;
- contradiction-resolution guidance.

These are typed outputs of ONE derived guidance flow, not separate feature
programs. Stronger general deliverable redesign and broad
technical-recommendation generation are OUTSIDE Increment 3.

### R-2 — Deterministic presentation priority

The system presents exactly ONE primary unresolved issue, selected by this
deterministic presentation ordering (highest first):

1. active contradiction;
2. pending evidence request;
3. pending specialist request;
4. provisional assumption;
5. owner-provided but unvalidated answer;
6. open gap;
7. remaining maturity deficiency.

This ordering is PRESENTATION prioritization only. It must NOT: adjudicate truth;
select a contradiction winner; change stored lifecycle or maturity; mutate
assertion state; delete or supersede records; or introduce scoring. The output
MAY state that other unresolved items remain, but must NOT present a ranked
multi-item program in Increment 3.

(Within-level tie-breaking among multiple active candidates at the selected level
is fixed deterministically by R-6.)

### R-3 — User-visible surfaces

One shared derived output is rendered on two surfaces:

1. a complete `Next Development Step` section in the deliverable;
2. a compact session-screen callout showing the primary issue and the immediate
   user action.

The derivation logic exists in the ENGINE layer only. Templates may render the
result but must NOT independently determine priority or truth state.

(The session callout's payload routing and the six-path scope correction needed to
deliver it are fixed by R-5.)

### R-4 — Truthfulness and scope boundary

The implementation may only reorganize and explain ALREADY-RECORDED facts,
assertions, provenance, validation state, gaps, contradictions, pending requests,
and derived readiness. It must NOT:

- fabricate domain-specific technical requirements;
- claim technical verification;
- imply expert validation;
- generate unsupported engineering recommendations;
- automatically resolve contradictions;
- select a winner between assertions;
- delete history;
- modify scoring;
- redesign the complete deliverable;
- create specialist-collaboration infrastructure;
- create a professional workspace;
- implement persistence;
- expand domains;
- alter the active anchor.

A "technical recommendation" may be displayed ONLY when it is a truthful
restatement or organization of already-recorded content, shown with explicit
uncertainty and validation caveats.

### R-5 — Session payload routing and six-path scope correction

The completed read-only implementation-authorization review (disposition
`INCREMENT 3 IMPLEMENTATION CONTRACT REQUIRES CORRECTION BEFORE AUTHORIZATION`)
found that the merged five-path scope cannot deliver the R-3 session callout: the
`show_session` route in `web/app.py` is the sole owner of the session render
context, and `web/templates/session.html` (presentation-only) cannot obtain the
engine-selected payload without it. This ruling resolves that blocking defect and
supplements R-3.

1. Both Increment 3 visible surfaces remain REQUIRED: the full deliverable
   `Next Development Step` section and the compact session-screen callout. The
   session callout is NOT removed and O-2 is NOT deferred.
2. Both surfaces MUST render the SAME payload selected by the SAME pure engine
   derivation — one selection, two renderings.
3. The bounded future implementation scope is expanded from five paths to exactly
   SIX paths by adding `web/app.py`.
4. Modifying `web/app.py` is permitted ONLY within the later, separately
   authorized implementation, and ONLY to:
   - the `show_session` route or its direct render-context construction;
   - call the shared pure Increment 3 derivation with the already-loaded
     in-memory `IdeaState`;
   - pass the resulting payload to `web/templates/session.html`.
5. The `web/app.py` change MUST NOT: change routing behavior; add a route; change
   request methods; mutate state; change session storage; invoke persistence;
   write files; alter scoring; alter progression; change authentication or
   authorization; modify database behavior; change stage transitions; introduce a
   second priority implementation; import paused persistence code; or reconcile or
   reuse the frozen persistence worktree.
6. `web/templates/session.html` remains presentation-only — it renders the passed
   payload and MUST NOT determine priority or truth state.
7. This six-path correction is a SCOPE boundary only. It does NOT authorize
   tests-first work or source implementation.

### R-6 — Within-level deterministic tie-break

After applying the R-2 seven-level priority order, if more than one ACTIVE
candidate exists within the selected level, the derivation chooses EXACTLY ONE
using this fixed tie-break:

1. lowest numeric `record_id` when record ids follow the existing `rec_N` form;
2. otherwise the earliest recorded `iteration` when available;
3. otherwise stable original source order (first-encountered).

Superseded or otherwise inactive records are EXCLUDED before tie-breaking (per the
Increment 2 active-set rule). Tie-breaking is PRESENTATION only: it must NOT
adjudicate truth, rank quality, select a contradiction winner, mutate state,
introduce scoring, delete history, or apply any free-form heuristic. Identical
state MUST always yield the same primary issue. (`record_id`'s monotonic `rec_N`
append order is the existing stable ledger ordering; no new sorting axis is
introduced.)

## 3. Authorization state

- Owner rulings R-1 through R-4 are APPROVED, committed, and merged (binding).
- Owner rulings R-5 and R-6 are PROPOSED by this bounded correction draft. They
  are NOT yet committed or merged and are NON-OPERATIVE until independently
  reviewed, committed, and merged. Until then, the merged R-1–R-4 and the merged
  Increment 3 implementation contract (five-path) remain the binding authority;
  because that merged five-path scope is insufficient to deliver the session
  callout, NO Increment 3 implementation may be authorized under it.
- Contract drafting (the companion `INCREMENT_3_IMPLEMENTATION_CONTRACT.md`) is
  AUTHORIZED; the six-path correction in that contract is the product of this
  ruling and remains a proposed draft.
- Source implementation is NOT yet authorized.
- Tests-first or source work requires a separate, explicit, repository-grounded
  owner authorization.
- This document was independently reviewed, committed in
  `6a11cb2ad389c318ea8f19ea18d95b06c04f59f6`, merged through PR #40, and
  incorporated into the authoritative branch by the documentation-only true-merge
  `429e4b6b88a3fb3d7cece522a0386ec424cf8a1e`. Rulings R-1 through R-4 are now
  operative as binding Increment 3 boundary authority. The companion
  `INCREMENT_3_IMPLEMENTATION_CONTRACT.md` is likewise committed and merged and is
  operative as a binding boundary, but remains `DRAFT — NOT AUTHORIZED FOR
  IMPLEMENTATION`. Operative as a binding boundary is NOT the same as authorized
  for implementation.

## 4. Non-authorization

This rulings record:

- is a committed and merged governance authority document (rulings R-1 through
  R-4 are operative as binding Increment 3 boundaries);
- does not authorize Increment 3 implementation, code, or test changes;
- does not authorize tests-first or source work, an implementation worktree, or
  any product-code change;
- does not authorize persistence, scoring, progression-loop, domain, or anchor
  changes;
- does not authorize a `main` merge;
- does not begin Increment 4, 5, or 6.
