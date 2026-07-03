# Increment 6 — Deliverable Redesign — Implementation Contract (FOR OWNER REVIEW)

> STATUS: DRAFT — CONTRACT / DOCS-ONLY — NOT AUTHORIZED FOR IMPLEMENTATION.
> This contract is a bounding document authored under an owner-ratified
> DOCS-ONLY authorization. It authors no tests, no source, no template change,
> and no engine change. It grants no downstream authority. Tests-first, source,
> PR, and merge each require their own separate, explicit, owner authorization.

- Authoritative integration branch: `feature/atomic-json-session-persistence`
- Authoritative integration tip at authoring time: `ad012be3d91aafaf2344f0e021007e6a97360a70`
- This document was authored on a fresh docs branch created from that exact commit.
- `origin/main` (unchanged, out of scope): `0e89e4636399760965c9ff8086b465c90dbadf8e`
- Companion design (active): `docs/governance/INCREMENT_6_DELIVERABLE_REDESIGN_DESIGN.md`
- Owner edit-surface selection: **TEMPLATE-ONLY** default (see §c)

---

## File-creation contract (per CLAUDE.md)

- **Path:** `docs/governance/INCREMENT_6_IMPLEMENTATION_CONTRACT.md`
- **Purpose:** bound the future Increment 6 implementation to a template-only,
  presentation-only edit surface with an explicit tests-first matrix and
  acceptance gates, for owner review, before any tests/source authorization.
- **Input contract:** the ratified authority rulings C6-R1…C6-R10 and the active
  Increment 6 design document, plus the deliverable surface verified at
  `ad012be3d91aafaf2344f0e021007e6a97360a70`.
- **Output contract:** a bounding contract description only. No code, no tests,
  no template edits, no engine edits, no persistence, no `main` change.
- **Prohibited behaviors:** authorizing or performing tests/source; new
  generation, new truth; scope/domain/Stage/maturity/scoring expansion;
  persistence touch; `main` synchronization; treating this contract as
  implementation authority.

---

## a. Increment 6 purpose and link to the active design

Increment 6 — Deliverable Redesign — is the last product-value increment. It
re-presents the already-produced Increment 1–5 deliverable outputs in a coherent
inventor-facing reading order, adding no new truth. The governing design is
`docs/governance/INCREMENT_6_DELIVERABLE_REDESIGN_DESIGN.md` (active on the
authoritative integration branch). This contract bounds how a future,
separately-authorized implementation of that design must be scoped; it does not
begin that implementation.

## b. Ratified constraints (C6-R1 through C6-R10)

This contract is subordinate to the ratified rulings; any conflict resolves in
favor of the ruling.

- **C6-R1 — Surface boundary.** Inventor-facing deliverable surface only
  (`assemble_deliverable` / `deliverable.html`). No professional workspace,
  domain expansion, Stage 4–7, or persistence.
- **C6-R2 — Improvement Not Generation.** No new synthesized/generated content or
  new truth; every rendered value traces to an existing Increment 1–5 derivation.
- **C6-R3 — Pure-derivation / additive discipline.** Any new arrangement is a pure
  function of existing state/package outputs; no new truth; no change to a prior
  section's meaning.
- **C6-R4 — Truth/provenance preservation.** Increment 2 evidence-quality vs
  validation separation, evidence-state labels, `validation_status`, confidence,
  and provenance preserved exactly; never equate owner text/length with
  verification; never upgrade a gap to verified.
- **C6-R5 — Scope-freeze classification.** Presentation/conformance fix defensible
  under the existing MVP freeze; no freeze amendment required within these
  bounds; any generative/expansion deviation requires a separate owner scope
  decision / freeze amendment before design.
- **C6-R6 — Persistence fence.** No touch, recovery, reconciliation, or dependence
  on the paused persistence lane or `aec9cf6…`; deliverable stays
  render-time/ephemeral.
- **C6-R7 — Backward compatibility.** Existing sessions render unchanged in
  meaning; package keys remain backward-compatible or additively extended; no
  truthful field removed.
- **C6-R8 — Protected boundaries.** No change to `score_case` / WPS-001 parity,
  progression semantics, domain registry, or `_s6` semantics beyond presentation;
  `main` untouched.
- **C6-R9 — Lifecycle gate.** Each downstream step requires separate explicit
  owner authorization; this contract authorizes none.
- **C6-R10 — Acceptance gates.** Future closure requires the six gates in §h.

## c. Exact preferred future edit surface (owner-selected: TEMPLATE-ONLY)

The single default future edit surface for Increment 6 implementation is:

- **`web/templates/deliverable.html`** — presentation restructuring only
  (reading order, grouping, headings, layout of the existing fourteen
  `section_1…section_14` keys and `_session_meta`-derived fields).

The template renders from `package.*` only and synthesizes no content today; the
redesign must preserve that property. Every value rendered must remain a value
already present in the assembled `package`.

## d. Engine file is NOT in the default future source scope

`engine/deliverable_assembler.py` is **NOT** part of the default future source
scope. The template-only default requires **zero** change to
`engine/deliverable_assembler.py`. The assembler's `assemble_deliverable` output
(the fourteen sections plus `_session_meta`) is treated as a fixed input to the
presentation layer.

## e. Conditional fallback rule (NOT authorized now)

An **additive, pure** assembler grouping helper in
`engine/deliverable_assembler.py` — one that reads the already-assembled
`package` and emits presentation-only grouping metadata (per design §4: not
stored truth, not a new deliverable fact, not scored, not persisted) — MAY be
**considered** only if a future contract review or tests-first planning step
proves the template-only approach infeasible, and only under a **separate,
explicit owner authorization** for that exact deviation. No existing helper's
output may change meaning and no new truth may be introduced. This fallback is
**NOT authorized for implementation now** and its mere description here confers
no authority.

## f. Exact prohibited source surfaces

The future implementation MUST NOT change any of the following:

- `score_case` / WPS-001 scoring parity (no scoring change of any kind);
- progression semantics (`assess_response` / `integrate_response` /
  `evaluate_transition`);
- the domain registry;
- `_s6` risk semantics (beyond where a value is placed for presentation);
- persistence / session-store / any persistence path; no `aec9cf6…`;
- `main` (no synchronization).

## g. Tests-first matrix (to be authored later — NO tests now)

The following matrix specifies what a future, separately-authorized tests-first
phase must cover. **No tests are authored by this contract.**

- **Traceability tests:** every rendered deliverable value maps to an existing
  `package` key / Increment 1–5 derivation (guards C6-R2/C6-R3).
- **Label-preservation tests:** evidence-state, `validation_status`, and
  `status_label` labels present next to each claim across all redesigned groups
  (guards C6-R4).
- **No-upgrade tests:** a long/causal owner answer without verification still
  cannot render as verified/resolved; `derived_verified_ready` renders separately
  from stored maturity (Increment 2 parity, guards C6-R4).
- **Backward-compatibility tests:** existing session fixtures render with
  unchanged meaning; absent-data branches and the `fdc-001-mvp-v1` `section_11`
  contract preserved (guards C6-R7).
- **Protected-boundary tests:** `score_case` / WPS-001 parity and `_s6` semantics
  unchanged; progression semantics and domain registry untouched; the known
  pre-existing `tests/test_domain_registry.py` failures remain the only failures
  (guards C6-R8).
- **No-persistence tests:** no persistence write, no session-resumption behavior,
  no reference to `aec9cf6…` (guards C6-R6).
- **No-new-truth / no-generation tests:** no new generated content, narrative
  synthesis, external document, or new-truth section appears; co-located sections
  imply no new causal/evidentiary/derivational link (guards C6-R2 and design §4
  improvement B).

## h. Future source acceptance gates (C6-R10)

Future Increment 6 closure requires ALL of:

1. **User-visible behavior** — a coherent, grouped inventor-facing deliverable
   presenting the existing sections in the design's reading order.
2. **Truth/provenance preservation** — every evidence-state / `validation_status`
   / `status_label` / confidence / provenance value preserved; separation of
   quality vs validation intact.
3. **Tests** — the §g tests-first matrix authored, passing, and merged before
   source per lifecycle.
4. **Backward compatibility** — existing sessions render unchanged in meaning;
   package-key and `section_11` contracts preserved.
5. **Failure conditions** — none of the design §9 failure conditions occur.
6. **Documentation closure** — an Increment 6 closure record / roadmap
   synchronization, per prior-increment precedent.

## i. Lifecycle statement

This contract authorizes **no** tests, **no** source, **no** template edit,
**no** engine edit, **no** PR, **no** merge, **no** persistence, and **no** `main`
synchronization. It grants **no downstream authority** of any kind. The ordered
future lifecycle (each a separate, explicit owner authorization) is:

1. Independent read-only review of this contract for scope-freeze / C6 adherence.
2. Owner authorization of a tests-first phase (author the §g matrix; tests-first,
   no source).
3. Owner authorization of source (template-only per §c/§d; fallback only under
   the separate authorization required by §e).
4. Independent source review, then owner-gated PR and true-merge.
5. Documentation closure / roadmap synchronization.

Until each gate is satisfied in order under its own authorization, no tests,
source, PR, or merge is authorized.

---

## Prohibited actions (restated)

No tests; no source; no template edit; no engine edit; no persistence; no use or
recovery of `aec9cf6…`; no `main` sync; no PR; no merge; no Increment 6
implementation; no tests-first authoring; no scope expansion beyond
presentation/reorganization; no generated content or new truth; no change to
`score_case`, progression semantics, domain registry, or `_s6` semantics; no
inference of authority from roadmap sequence, the design, or this contract.
