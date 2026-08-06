# Increment 6 — Deliverable Redesign — Bounded Design (FOR OWNER REVIEW)

> STATUS: DRAFT — DESIGN-ONLY — NOT AUTHORIZED FOR IMPLEMENTATION.
> This document is a bounded design proposal prepared under an owner-ratified
> DESIGN-ONLY authorization. It authors no source, no tests, no template
> change, and no engine change. It creates no implementation authority. Tests,
> source, PR, and merge each require their own separate, explicit, owner
> authorization.

- Authoritative integration branch: `feature/atomic-json-session-persistence`
- Authoritative integration tip at authoring time: `860d578c32a683a4aef9410e87ce1ce5c9cf3524`
- This document was authored on a fresh docs branch created from that exact commit.
- `origin/main` (unchanged, out of scope): `0e89e4636399760965c9ff8086b465c90dbadf8e`
- Increment 6 identity: **Deliverable Redesign** — the last product-value increment
- Classification (owner-ratified): presentation/conformance, bounded by C6-R1…C6-R10
- Freeze finding (owner-ratified): no MVP freeze amendment required within these bounds

---

## File-creation contract (per CLAUDE.md)

- **Path:** `docs/governance/INCREMENT_6_DELIVERABLE_REDESIGN_DESIGN.md`
- **Purpose:** record a bounded, presentation-only redesign design for the
  inventor-facing deliverable, for owner review, before any tests/source
  authorization.
- **Input contract:** the already-produced Increment 1–5 deliverable outputs
  as they exist at the authoritative integration tip
  (`engine/deliverable_assembler.py`, `web/templates/deliverable.html`),
  verified at `860d578c32a683a4aef9410e87ce1ce5c9cf3524`.
- **Output contract:** a design description only. No code, no tests, no template
  edits, no engine edits, no persistence, no `main` change.
- **Prohibited behaviors:** new generation, new truth, new external documents,
  domain/Stage/maturity/scoring expansion, professional-mode expansion,
  persistence touch, scope inference from roadmap sequence, or treating this
  document as implementation authority.

---

## 1. Design purpose and product-value rationale

Increments 1–5 corrected the platform's source semantics and outputs: owner vs
expert question separation (Increment 1), truthful gap/evidence state
(Increment 2), visible idea-development outputs (Increment 3), atomic
requirements and criticality-aware risk (Increment 4), and concrete
validation-plan generation (Increment 5). Those corrections now feed the
deliverable, but they accreted **section by section, additively** — each
increment appended a section (`section_12`, `section_13`, `section_14`) or
adjusted a label without reorganizing the whole. The result is correct in
content but not yet coherent in presentation for a non-technical inventor.

Increment 6 is intentionally last (per `INVENTORAI_PRODUCT_VALUE_CORRECTION_PLAN.md`)
precisely so the redesign presents corrected sources and corrected outputs,
rather than re-encoding earlier defects. Its product value is the highest-
visibility remaining improvement: the deliverable is the single artifact the
inventor receives at the end of a session. A coherent, honest, provenance-
preserving presentation is the culmination of the whole correction program.

This design keeps the redesign strictly to **how already-produced outputs are
arranged and presented** — never what is produced. It adds no new truth.

## 2. Ratified authority rulings (governing constraints)

These are the owner-ratified constraints. This design is subordinate to them;
any conflict is resolved in favor of the ruling.

- **C6-R1 — Surface boundary.** Increment 6 is limited to the inventor-facing
  deliverable surface: `assemble_deliverable` / `deliverable.html`. No
  professional workspace surface, no domain expansion, no Stage 4–7, no
  persistence.
- **C6-R2 — Improvement Not Generation.** No new synthesized/generated content
  or new truth. Every rendered value must trace to an existing Increment 1–5
  derivation.
- **C6-R3 — Pure-derivation / additive discipline.** Any new arrangement must be
  a pure function of existing state/package outputs, adding no new truth and
  changing no prior section's meaning.
- **C6-R4 — Truth/provenance preservation.** Increment 2 evidence-quality vs
  validation separation, evidence-state labels, `validation_status`, confidence,
  and provenance must be preserved exactly. Presentation must never equate owner
  text/length with verification and must never upgrade a gap to verified.
- **C6-R5 — Scope-freeze classification.** Bounded by C6-R1…C6-R4, Increment 6 is
  a presentation/conformance fix defensible under the existing MVP freeze; no
  freeze amendment is required within these bounds. Any generative/expansion
  deviation is a capability addition requiring a separate owner scope decision /
  freeze amendment before design.
- **C6-R6 — Persistence fence.** No touch, recovery, reconciliation, or
  dependence on the paused persistence lane or `aec9cf6…`. The deliverable
  remains render-time/ephemeral as today.
- **C6-R7 — Backward compatibility.** Existing sessions render unchanged in
  meaning. Deliverable-package keys remain backward-compatible or additively
  extended. No truthful fields may be removed.
- **C6-R8 — Protected boundaries.** No change to `score_case` / WPS-001 parity,
  progression semantics, domain registry, or `_s6` semantics beyond
  presentation. `main` remains untouched.
- **C6-R9 — Lifecycle gate.** Ratifying these rulings authorized only the
  DESIGN-ONLY step that produced this document. It authorizes no tests, no
  source, no PR, no merge. Each later step requires separate explicit owner
  authorization.
- **C6-R10 — Acceptance gates.** Future closure must require user-visible
  behavior, truth/provenance, tests, backward compatibility, failure conditions,
  and documentation closure gates, specified in the design and contract.

## 3. Existing deliverable surface and current structure (verified at tip)

Verified read-only against `engine/deliverable_assembler.py` and
`web/templates/deliverable.html` at `860d578c32a683a4aef9410e87ce1ce5c9cf3524`.
This is descriptive, not a change specification.

**Assembler — `engine/deliverable_assembler.py`.** Public entry
`assemble_deliverable(state: IdeaState) -> dict` builds a `package` dict from
pure per-section helpers and a `_session_meta` block. The package keys and their
producing helpers, exactly as assembled:

| Package key | Helper | Role (verified) |
|-------------|--------|-----------------|
| `section_1_disclaimer` | `_s1` | Fixed disclaimer text. |
| `section_2_invention_summary` | `_s2` | Maturity label, assessment completeness, known problem/mechanism (with absent-data note branches). |
| `section_3_assessment_overview` | `_s3` | Capabilities assessed. |
| `section_4_requirements` | `_s4` | Requirements list. |
| `section_5_assumptions` | `_s5` | Assumptions and inventor-stated unknowns. |
| `section_6_risks` | `_s6` | Risks (protected semantics — presentation only). |
| `section_7_recommendations` | `_s7` | Proceed/revise verdict + rationale. |
| `section_8_unresolved_items` | `_s8` | Open gaps (`OPEN-nnn`) plus acknowledged inventor unknowns (`UNKNOWN-nnn`); cross-capability conflict detection is explicitly **deferred to Phase 6** (empty list today). |
| `section_9_stage3_reasoning` | `_s9` | Each Stage 3 gap with label, status/status_label, captured accepted evidence, or an honest `missing_evidence_statement`; carries the note that captured evidence "is not validation, feasibility confirmation, completeness, or expert review." Empty for Stage-2-only sessions. |
| `section_10_recommended_next_steps` | `_s10` | Steps synthesized ONLY from already-computed state (unresolved gaps, sub-Level-2 maturity, inventor unknowns, REASONED-not-DEMONSTRATED evidence-strength); each step names its source; de-duplicated; honest empty statement when none. |
| `section_11_prototype_test_plan` | `_s11` | At most three traceable PROPOSED experiments reorganizing captured evidence; never invents specifications/thresholds/results/feasibility/validation; success criteria are owner-provided verbatim or "Owner-defined criterion required." Additive presentation-only `shared_required_expertise` field; per-experiment `required_expertise_or_tools` retained for schema `fdc-001-mvp-v1` backward-compat. |
| `section_12_next_development_step` | `_s12` | **Increment 3** additive: renders the shared next-development-step derivation (`derive_next_development_step`) as a presentation dict; the SAME shared derivation feeds the session callout (O-2). `actionable=False` with all-null fields when nothing actionable — no problem invented. |
| `section_13_requirement_landscape` | `_s13` | **Increment 4** additive: provenance-anchored Requirement Landscape; human-readable only; "adds no new truth and changes no prior section." |
| `section_14_validation_plan` | `_s14` | **Increment 5** additive: proposed validation actions and blocked items; human-readable only; proposes nothing verified; changes no prior section. |
| `_session_meta` | (inline) | Iteration/gap counts, maturity level/label, direction, domain signal, evidence quality, idea summary, `deliverable_eligible`, and (Increment 2) `derived_verified_ready` presented **separately** from stored maturity/lifecycle — recomputed, never overriding stored state. |

Increment 2 module notes confirm the evidence **QUALITY** axis (ADR-003) is
separated from **validation**; `REASONED` no longer implies technical
confirmation, and `validation_status` is surfaced separately on each evidence
view.

**Template — `web/templates/deliverable.html`.** Verified to render all fourteen
`section_1…section_14` keys plus `_session_meta`-derived fields. Values are
rendered from `package.*` only; the template synthesizes no content, and it
carries absent-data branches (e.g. `known_problem` vs `known_problem_note`).

## 4. Proposed presentation architecture (bounded, presentation-only)

The redesign proposes a coherent **reading order and grouping** over the
fourteen existing sections, so the inventor reads a single narrative arc rather
than a flat list of accreted sections. No section's content is generated or
altered in meaning; only ordering, grouping, headings, and layout are proposed.

Proposed inventor-facing grouping (every existing section mapped once; none
dropped):

1. **What your idea is** — `section_1_disclaimer` + `section_2_invention_summary`.
2. **What we assessed** — `section_3_assessment_overview`.
3. **What it needs** — `section_4_requirements` + `section_13_requirement_landscape`
   (Increment 4).
4. **What is assumed vs still unknown** — `section_5_assumptions` +
   `section_8_unresolved_items` (open gaps + acknowledged unknowns), preserving
   deferred/unknown state (Increments 1–2).
5. **What could go wrong** — `section_6_risks`, preserving criticality ordering
   (Increment 4) and `_s6` semantics unchanged.
6. **The reasoning behind it** — `section_9_stage3_reasoning`, preserving the
   Increment 2 evidence-quality-vs-validation honesty.
7. **What we recommend and what to do next** — `section_7_recommendations` +
   `section_12_next_development_step` (Increment 3) +
   `section_10_recommended_next_steps` + `section_11_prototype_test_plan` +
   `section_14_validation_plan` (Increment 5).

The `_session_meta` honest signals (maturity label, and the Increment 2
`derived_verified_ready` shown **separately** from stored maturity) are surfaced
as a small honest status strip, never merged into a single "resolved/verified"
impression.

**Co-location caveat (improvement B).** Group 7 places recommendations, the
next-development-step, recommended next steps, the prototype/test plan, and the
validation plan near one another **for reading flow only**. This co-location
creates **no new causal, evidentiary, or derivational link** between them: the
recommendation does not become "validated" by sitting beside the validation
plan, the validation plan does not become "recommended/verified" by sitting
beside the recommendation, and no ordering implies dependency or proof. Each
value retains exactly the truth state and provenance its own producing helper
assigned it.

**Grouping-metadata caveat (improvement D).** Any ordering or grouping construct
introduced to express this arrangement is **pure presentation metadata**: it is
a deterministic function of the existing `package`, it is **not stored truth**,
**not a new deliverable fact**, **not scored**, and **not persisted**. It carries
no evidence state, cannot upgrade any claim, and must be reconstructable purely
from the already-assembled package with no additional input.

The grouping is a **pure function of the existing `package`** (C6-R3): it reads
existing keys and arranges them; it introduces no computed truth.

## 5. Mapping from Increment 1–5 outputs to redesigned deliverable sections

| Source increment | Existing output (verified key) | Redesigned placement | New truth? |
|------------------|-------------------------------|----------------------|------------|
| Increment 1 — Owner–Expert Question Boundary | Deferred/unknown items preserved: `section_5_assumptions` (inventor unknowns), `section_8_unresolved_items` (acknowledged unknowns) | Group 4 | No |
| Increment 2 — Truthful Gap & Evidence State | Evidence-state labels, `validation_status`, `status_label`, `missing_evidence_statement` (`section_9`); `_session_meta.derived_verified_ready` shown separately | Labels beside every claim in all groups; honest status strip | No |
| Increment 3 — Visible Idea-Development Outputs | `section_12_next_development_step` (`_s12`), the shared derivation feeding the session callout (O-2) | Group 7 | No |
| Increment 4 — Atomic Requirements & Criticality-Aware Risk | `section_13_requirement_landscape` (`_s13`); criticality-ordered `section_6_risks` | Group 3 and Group 5 | No |
| Increment 5 — Concrete Validation-Plan Generation | `section_14_validation_plan` (`_s14`) | Group 7 | No |

Every cell in the "New truth?" column is **No** by design and by C6-R2/C6-R3.

## 6. What is explicitly NOT changed

- No new section carrying new derivation or new truth.
- No change to `score_case` / WPS-001 parity, progression semantics
  (`assess_response` / `integrate_response` / `evaluate_transition`), the domain
  registry, or `_s6` risk semantics beyond where a value is placed (C6-R8).
- No new external documents (patent, business plan, BOM, wiring/pin map,
  firmware), no generation, no LLM prose (C6-R2, MVP freeze OUT-OF-SCOPE).
- No domain expansion, multi-domain orchestration, maturity levels 3–5, scoring,
  uncertainty model, or Stage 4–7 (MVP freeze).
- No professional/workspace surface, accounts, collaboration, or artifact store.
- No persistence, no session resumption, no touch of `aec9cf6…` (C6-R6).
- No `main` synchronization (C6-R8).
- The Phase-6-deferred cross-capability conflict detection in `section_8` stays
  deferred and empty; the redesign does not implement or imply it.

## 7. Truth / provenance and evidence-state preservation

- Evidence **QUALITY** (ADR-003 reasoning-structure axis) and **validation**
  remain separated exactly as Increment 2 established; the redesign never merges
  them into a single "resolved" impression (C6-R4).
- `validation_status`, evidence-state labels, `status_label`, confidence, and
  provenance travel **with** each claim into its redesigned group; a value may
  never appear stripped of its state label.
- `section_9`'s `missing_evidence_statement` and its "not validation" note are
  preserved verbatim in meaning.
- `_session_meta.derived_verified_ready` remains presented separately from stored
  maturity/`deliverable_eligible`; presentation never lets stored CLOSED / high
  maturity read as verified.
- No gap may be presented as verified/demonstrated from presentation, ordering,
  owner text, or answer length alone (C6-R4).
- The Increment 3 single shared derivation (O-2) continues to feed both the
  session callout and the deliverable; the redesign does not fork them.

## 8. Backward-compatibility requirements

- Existing sessions and stored data render with unchanged meaning (C6-R7).
- All fourteen deliverable-package keys plus `_session_meta` remain
  backward-compatible; any new key is additive and optional, defaulting to
  today's behavior when absent.
- The `section_11` schema `fdc-001-mvp-v1` output contract (including the
  per-experiment `required_expertise_or_tools` field) is not altered.
- No truthful field is removed or renamed in a way that drops information.
- Absent-data branches already present in the template (e.g., `known_problem`
  vs `known_problem_note`) must be preserved.

## 9. Failure conditions and prohibited outputs

The future implementation must be considered failing if any of these occur:

1. Any rendered value cannot be traced to an existing Increment 1–5 derivation /
   existing `package` key.
2. Any evidence appears without its evidence-state / `validation_status` /
   `status_label` label.
3. Any gap is presented as verified/resolved from presentation alone.
4. Any new generated content, narrative synthesis, or external document appears.
5. Any change to `score_case` / WPS-001 parity, progression semantics, domain
   registry, or `_s6` risk semantics.
6. Any persistence write, session-resumption behavior, or reference to
   `aec9cf6…`.
7. Any existing session renders with altered meaning or dropped truthful fields.
8. Any co-location that implies a new causal/evidentiary/derivational link
   (violates the §4 improvement-B caveat).
9. Any `main` change.

## 10. Test strategy outline only (NO tests authored here)

Outline for a future, separately-authorized tests-first phase — not implemented
in this step:

- **Traceability tests:** every rendered deliverable value maps to an existing
  `package` key / Increment 1–5 derivation (guards C6-R2/C6-R3).
- **Label-preservation tests:** evidence-state, `validation_status`, and
  `status_label` labels are present next to each claim across all redesigned
  groups (guards C6-R4).
- **Separation tests:** `derived_verified_ready` renders separately from stored
  maturity; a long/causal owner answer without verification still cannot render
  as verified/resolved (Increment 2 parity).
- **No-implied-link tests:** co-located recommendation and validation plan do not
  set or imply any verified/validated cross-reference (guards §4 improvement B).
- **Backward-compat tests:** existing session fixtures render with unchanged
  meaning; absent-data branches and the `fdc-001-mvp-v1` `section_11` contract
  preserved (guards C6-R7).
- **Protected-boundary tests:** `score_case` / WPS-001 parity and `_s6` semantics
  unchanged; domain registry untouched (guards C6-R8).
- **Baseline:** the known pre-existing `tests/test_domain_registry.py` failures
  must remain the only failures; no new failures introduced.

## 11. Implementation-contract prerequisites and edit-surface options

Before any tests-first or source authorization, a separate bounded
implementation contract (e.g., `INCREMENT_6_IMPLEMENTATION_CONTRACT.md`, by
prior-increment precedent) must specify, and the owner must authorize, the exact
edit surface. Two options are presented for the owner to choose between
(improvement C); **neither is pre-authorized as source implementation here**:

- **Preferred, minimum-risk — template-only.** If the fourteen existing
  `package` keys already carry every value the redesigned grouping needs (initial
  inspection indicates they do), the entire redesign can be a presentation
  restructuring of `web/templates/deliverable.html` only, with **zero**
  `engine/deliverable_assembler.py` change. This keeps the protected-boundary
  surface (C6-R8) minimal.
- **Fallback — additive pure assembler grouping helpers.** Only if a purely
  presentational grouping cannot be expressed in the template alone, the contract
  may permit **additive, pure** grouping helper(s) in
  `engine/deliverable_assembler.py` that read the already-assembled `package` and
  emit presentation-only grouping metadata (per the §4 improvement-D caveat:
  not stored truth, not persisted, not scored). No existing helper's output may
  change meaning; no new truth may be introduced.

The contract must additionally specify: the exact additive package-key additions
(if any) and their pure-derivation definitions; the tests-first matrix
operationalizing §10; the protected-file boundaries (no
scoring/progression/registry/`_s6`/`main`); and the closure/acceptance gates
(§C6-R10). This design proposes these prerequisites; it does not satisfy or
authorize them.

## 12. Review gates before any tests/source authorization

1. Owner review and acceptance of this design.
2. Owner selection of the §11 edit-surface option (template-only preferred).
3. Owner-authorized, committed Increment 6 implementation contract (bounded edit
   set + tests-first matrix + protected boundaries).
4. Independent read-only review of the contract for scope-freeze conformance and
   C6-R1…C6-R10 adherence.
5. Separate explicit owner authorization for a tests-first phase, then a separate
   authorization for source, then independent review, then owner-gated PR and
   true-merge — each a distinct step.

Until every gate above is satisfied in order, no tests, source, PR, or merge is
authorized. This document is design-only and is not implementation authority.

---

## Prohibited actions (restated)

No tests; no source; no template edit; no engine edit; no persistence; no use or
recovery of `aec9cf6…`; no `main` sync; no PR; no merge; no scope expansion
beyond presentation/reorganization; no generated content or new truth; no change
to `score_case`, progression semantics, domain registry, or `_s6` semantics; no
inference of authority from roadmap sequence or from this document.
