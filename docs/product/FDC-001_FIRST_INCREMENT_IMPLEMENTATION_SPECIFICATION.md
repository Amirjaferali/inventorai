# FDC-001 First Increment — Implementation Specification

STATUS: OWNER-AUTHORIZED IMPLEMENTATION SPECIFICATION — NON-ACTIVATING
EXECUTION_AUTHORITY: NONE
LANE_STATUS: PROPOSED / INACTIVE
IMPLEMENTATION_STATUS: NOT STARTED
BENCHMARK_STATUS: NOT RUN
PERSISTENCE_STATUS: PRESERVE UNMODIFIED AND PAUSE

This document is a planning specification only. It:

- does not activate the commercial-differentiation lane;
- does not authorize code or any working-tree change beyond this one document;
- does not perform Commit B (the committed Roadmap §§4–7 lane-activation update);
- does not modify Roadmap §§4–7, any anchor, contract, hold, or closed state;
- does not run the bicycle brake-light competitive benchmark;
- does not use, deliver, repair, or modify session persistence.

A later, separate, explicit owner implementation authorization (and the §12.D /
Commit B lane activation it depends on) is required before any code change. This
specification is authored on `worktree/post-pr14-clean-baseline` at HEAD
`bc1234edb59b4a7eefb8f3315c24b1b9dae9f850` and traces to, without inheriting
execution authority from, the non-authorizing strategic records S1
(`docs/governance/INVENTORAI_COMMERCIAL_DIFFERENTIATION_DIRECTION.md`) and S2
(`docs/benchmarks/BICYCLE_BRAKE_LIGHT_COMPETITIVE_BENCHMARK.md`).

---

## 0. Canonical vocabulary (used consistently throughout)

Two orthogonal axes describe every recorded input. They are never collapsed: an
input's `provenance` (where it came from) never determines its `claim_class` (what
kind of truth-status it carries).

`claim_class` (what the input asserts):

- `observed_fact` — a directly observed, non-controversial fact about the world.
- `owner_requirement` — something the owner/inventor wants or requires (a goal or
  constraint), not a verified fact about a candidate.
- `operator_reported_result` — a result the operator says they obtained
  (e.g. a bench/field/calibration outcome); recorded as reported, not verified.
- `assumption` — an unconfirmed supposition.
- `external_reference` — a citation/pointer the operator supplied; not fetched or
  verified by the platform.
- `unsupported_claim` — text that cannot be grounded in an operator input or a
  deterministic rule.
- `missing_information` — a named thing that is not yet known (lives as a `Gap`).
- `constraint` — a recorded constraint with a strength (see `Constraint`).

`provenance` (where the input came from):

- `seeded_owner_context` — pre-seeded from the owner's stated case context.
- `operator_entered` — typed in by the operator during the session.
- `platform_proposed` — proposed by the platform for operator confirmation
  (never auto-confirmed).
- `derived_by_rule` — produced by a deterministic governance rule.

A `provenance` value (e.g. `operator_entered`) is NOT a truth classification and
never, by itself, makes an input verified, a fact, or evidence.

## 1. Purpose and user-visible value

**User problem.** An inventor working the bicycle automatic-brake-light idea must
choose a `braking-detection architecture` but cannot yet — the choice depends on
installation requirements, false-positive tolerance on rough roads, and physical
evidence the inventor does not have. A general AI will emit a plausible paragraph
and move on, leaving the inventor to re-establish the same context next time and
to mistake fluent prose for a grounded decision.

**Visible outcome.** The first increment gives the inventor a **Technical Decision
Workspace**: a single, structured, exportable record for one bounded decision that
holds the candidate architectures, what is actually known, what the owner requires,
what is assumed, what is operator-reported, what is still missing, and an honest
readiness state. During the active in-memory session the governed state is
**consistently re-rendered** on each view from the same in-memory record, rather
than regenerating fresh prose. The differentiating value (per S1 §3, referenced not
as authority) is that InventorAI **structures and evolves one traceable technical
decision state**: the inventor sees the decision advance from
`insufficient_information` toward `decision_ready_for_owner_review` as inputs are
added, with every recorded input tagged by `claim_class` and `provenance` and every
gap named. The increment demonstrates value by completing the structuring work the
inventor would otherwise do by hand and by refusing to fabricate a selection the
evidence does not support.

**Durability boundary (corrected).** This is an in-memory, export-oriented
increment:

- the governed state is consistently re-rendered during the active in-memory
  session;
- outside that session it survives only through the explicit export artifact (§8)
  the operator chooses to save;
- restart/reopen restoration is NOT supported (session persistence remains paused).

The workspace must never imply that reopening the application restores a prior
decision; only the exported artifact carries state beyond the session.

## 2. First-increment user flow

Smallest usable flow, open → export:

1. **Open workspace** for the fixed first decision: question = "Which
   braking-detection architecture should the bicycle automatic brake light use?"
   The three candidate architectures are pre-listed (§6).
2. **Review pre-seeded owner context**, each item shown with both its `claim_class`
   and `provenance` and never labelled a verified fact. The inventor's stated
   context seeds, for example: `owner_requirement` "automatic brake indication
   without manually pressing a control"; `owner_requirement` "avoid or minimize a
   wire to the brake lever"; `owner_requirement`/`assumption` "rough roads and
   vibration are a concern" (recorded as the owner's stated concern, not an observed
   fact). Each carries `provenance = seeded_owner_context`.
3. **Add inputs** via plain-language fields, each classified at entry (§0/§7): an
   observed fact, an owner requirement, an operator-reported result, an assumption,
   an external reference, a constraint (with strength), or an owner preference.
   Nothing is auto-promoted to a stronger `claim_class`.
4. **See the recomputed readiness state** and the per-candidate comparison update
   deterministically after each accepted input (§5, §6). Unresolved gaps and
   blockers are listed explicitly.
5. **Export** a standalone decision-readiness record (§8) — a single artifact the
   inventor can read without the conversation, capturing candidates, classified
   inputs, gaps, blockers, readiness, revision id, generated-at, and explicit
   limitations.

The flow is complete when an export is produced. No step writes durable state; the
only state that survives the session is the export the operator chooses to save.

## 3. Technical Decision Workspace layout

Minimum visible areas (single screen acceptable; ordering is a UI choice):

- **Decision question** — the fixed question string and the decision identity/revision.
- **Candidate architectures** — the three candidates (§6), each with its current
  comparison rows and `option_status`.
- **Classified inputs** — observed facts, owner requirements, operator-reported
  results, assumptions, and external references, each visibly tagged by
  `claim_class` and `provenance` and visually separated by truth-status.
- **Unresolved gaps** — named missing information; readiness-blocking gaps are
  marked distinctly from non-blocking gaps.
- **Blockers** — current `blocking_reasons` with affected scope.
- **Readiness state** — current `readiness_status` plus the user-facing label
  (e.g. `REVIEW REQUIRED` only as a label, never as a stored status).
- **Change-impact summary** — the latest change and what it affected (§9).
- **Export action** — produces the §8 artifact.

## 4. Canonical data model

Implementation-ready field model (names are normative; types indicative). All
in-memory for this increment.

```
DecisionRecord:
  schema_version: string                    # see §11
  decision_id: string                       # stable id for this decision
  decision_question: string                 # fixed first-case question
  revision: integer                         # monotonic; increments on each accepted change
  candidates: [Candidate]
  inputs: [ClaimItem]                        # observed facts, owner requirements,
                                             # operator-reported results, assumptions,
                                             # external references, unsupported claims
  constraints: [Constraint]
  gaps: [Gap]
  risks: [Risk]
  owner_preference: OwnerPreference | null
  readiness_status: enum (see §5)
  blocking_reasons: [BlockingReason]
  history: [ChangeEvent]                     # ordered; one entry per accepted change
  change_impact_summary: ChangeImpactSummary | null   # derived from latest ChangeEvent (§9)
  export_metadata: ExportMetadata
  # NOTE: there is exactly one authoritative timestamp in the record, and it lives
  # in ExportMetadata.generated_at (stamped at export). DecisionRecord holds no
  # second authoritative timestamp.

ClaimItem:                                   # replaces the former Fact / Assumption split;
  claim_id: string                           # one model, classified by claim_class
  text: string
  claim_class: enum {                        # see §0
    observed_fact, owner_requirement, operator_reported_result,
    assumption, external_reference, unsupported_claim, constraint }
  provenance: enum {                         # see §0
    seeded_owner_context, operator_entered, platform_proposed, derived_by_rule }
  confirmed: boolean                         # for platform_proposed/assumption: false until
                                             # operator confirms; never auto-true
  source_label: string | null               # for external_reference: what was cited (not fetched)
  candidate_ids: [string]                    # which candidates this input bears on (may be empty)
  decision_relevant: boolean

Candidate:
  candidate_id: string
  name: enum { wired_brake_lever_switch, accelerometer_inference, wheel_speed_inference }
  option_status: enum { active, eliminated, deferred, blocked }
  disposition_reason: string | null          # required when not active
  disposition_basis: enum {                   # required when not active; see §13
    incompatible_with_recorded_requirement, deferred_pending_input,
    blocked_by_evidence_gap } | null
  comparison_rows: [ComparisonRow]            # see §6

Constraint:
  constraint_id: string
  text: string
  constraint_strength: enum { preference, soft_constraint, mandatory_constraint }
  provenance: enum { seeded_owner_context, operator_entered, platform_proposed, derived_by_rule }
  confirmed: boolean                          # mandatory constraints act only when confirmed

Gap:
  gap_id: string
  text: string                                # the missing information, named
  blocks_readiness: boolean                   # readiness-blocking vs. non-blocking
  reclassification_rationale: string | null   # required to move blocking -> non-blocking (§6/§9)

Risk:
  risk_id: string
  text: string
  candidate_ids: [string]

OwnerPreference:
  candidate_id: string
  rationale: string | null
  # owner_preferred records preference ONLY; it never sets technically_selected.

BlockingReason:
  code: enum (see §5)
  text: string
  affected_scope: enum { decision, candidate }
  affected_candidate_id: string | null

ChangeEvent:
  event_id: string
  revision: integer
  change_type: enum {                         # see §10 for full coverage
    input_added, input_updated, input_removed,
    constraint_added, constraint_updated, constraint_removed,
    gap_resolved, gap_reclassified, conflict_resolved,
    owner_preference_set, owner_preference_cleared,
    candidate_status_changed }
  target_id: string | null                    # the claim/constraint/gap/candidate affected
  summary: string
  prior_readiness_status: string
  new_readiness_status: string

ChangeImpactSummary:                          # derived deterministically from latest ChangeEvent (§9)
  changed_item: string
  affected_candidates: [string]
  affected_gaps_or_blockers: [string]
  prior_readiness: string
  new_readiness: string

ExportMetadata:
  schema_version: string                      # see §11
  export_format: enum { json }                # JSON is the authoritative export (§11)
  export_revision: integer
  generated_at: ISO-8601 string               # the single authoritative timestamp
  limitations: [string]                       # explicit; see §8
```

Invariant (must be enforced and visible): **`owner_preferred != technically_selected`.**
`owner_preference` records preference only and never sets, implies, or upgrades a
technical selection, validity, compatibility, or safety claim. The first increment
MUST NOT produce a `technically_selected` value at all.

There is exactly one authoritative timestamp (`ExportMetadata.generated_at`); the
record holds no duplicate authoritative `generated_at`.

## 5. Readiness model

`readiness_status` is computed deterministically from the recorded inputs after
each accepted change. Evaluation uses the exact ordered decision table below.
Definitions used by the table:

- "minimum comparison context" = at least 2 candidates are `active` AND each has at
  least one `decision_relevant` classified input or constraint populating a
  comparison dimension.
- "readiness-blocking gap" = a `Gap` with `blocks_readiness = true`.
- "all candidates accounted for" = every one of the three candidates is either
  fully comparable on the recorded decision-relevant dimensions OR explicitly
  `eliminated` / `deferred` / `blocked` with a recorded `disposition_basis` (§7).
- "unresolved conflict" = an open `unresolved_evidence_conflict` /
  `owner_preference_conflicts_with_readiness` blocker.

Ordered decision table (first matching row wins):

```
1. if NOT minimum comparison context:
       -> insufficient_information
2. else if any readiness-blocking gap exists
        OR a confirmed mandatory_constraint cannot be evaluated against any active
           candidate for lack of information:
       -> blocked_by_evidence_gap
3. else if NOT all candidates accounted for
        OR any decision-relevant non-blocking gap remains
        OR any unresolved conflict exists:
       -> comparison_in_progress
4. else:
       -> decision_ready_for_owner_review
```

Consequences of the ordering (corrected):

- `insufficient_information` is the genuine initial/default state. Pre-seeded gaps
  do NOT force the initial state to `blocked_by_evidence_gap`, because rule 1 fires
  first whenever minimum comparison context is absent (which is the case at open).
- `blocked_by_evidence_gap` can only be reached AFTER minimum comparison context
  exists and a readiness-blocking gap (or an unevaluable confirmed mandatory
  constraint) remains.
- `decision_ready_for_owner_review` is terminal for this increment and means "ready
  for the **owner** to decide" — never a platform technical selection. It requires
  all three candidates accounted for (§7).

Prohibited status values in this increment (require separate authorization and real
evidence): `technically_selected`, `approved`, `validated`, `certified`,
`production_ready`, `frozen`.

Exact `blocking_reasons` codes:

- `missing_installation_constraint` — whether a wire to the brake lever is
  acceptable is unknown/unconfirmed.
- `missing_false_positive_tolerance` — acceptable false-braking-alert rate unknown.
- `missing_physical_or_calibration_information` — no operator-reported calibration /
  bench / field result exists where the comparison needs one.
- `unresolved_evidence_conflict` — two recorded inputs about the same candidate
  dimension disagree (§9).
- `owner_preference_conflicts_with_readiness` — an owner preference names a candidate
  that is `eliminated`/`blocked` or contradicted by a confirmed mandatory
  requirement (§9).
- `candidate_not_yet_comparable` — a specific candidate lacks the inputs needed to
  place it in the comparison (scope = candidate).

## 6. Candidate comparison model and gap discipline

Exactly three candidates, fixed: `wired_brake_lever_switch`,
`accelerometer_inference`, `wheel_speed_inference`. The comparison renders rows per
decision-relevant dimension and **never declares a winner**.

Comparison dimensions (minimum): installation impact (wire-to-lever required?),
sensitivity vs. false-positive behavior on rough roads, information available,
inputs/mounting required, open gaps. Each `ComparisonRow` carries `claim_class` and
`provenance` (the same two axes as §0), not a single merged class:

```
ComparisonRow:
  dimension: string
  candidate_id: string
  value_text: string
  claim_class: enum {                         # see §0
    observed_fact, owner_requirement, operator_reported_result,
    assumption, external_reference, unsupported_claim, missing_information, constraint }
  provenance: enum {                          # see §0
    seeded_owner_context, operator_entered, platform_proposed, derived_by_rule }
```

Rules:

- Every cell is explicitly tagged with both `claim_class` and `provenance`; the UI
  must visually separate stronger truth-status (`observed_fact`,
  `operator_reported_result`) from weaker (`assumption`, `unsupported_claim`,
  `missing_information`). `provenance = operator_entered` does not make a cell a
  fact.
- A confirmed `mandatory_constraint` (an `owner_requirement` of strength
  `mandatory_constraint`) may move a candidate to `option_status=eliminated` with a
  recorded `disposition_reason` and `disposition_basis =
  incompatible_with_recorded_requirement` (§13) — e.g. a confirmed "no wire to brake
  lever" mandatory requirement eliminates `wired_brake_lever_switch`. A
  `preference`/`soft_constraint` may only `defer`/qualify, never eliminate.
- The model produces, at most, a bounded recommendation framing ("ready for owner
  review with these trade-offs") or a truthful block — never a
  `technically_selected` candidate.

Gap discipline (corrected — no silent waiver):

- A non-blocking gap may be acknowledged and left open without blocking readiness.
- A readiness-blocking gap **cannot be waived**. It may only be reclassified to
  non-blocking through an explicit recorded `reclassification_rationale`, captured
  as a `gap_reclassified` `ChangeEvent`.
- Both the original gap and any reclassification remain visible in `history` and in
  the export. Missing material information must never disappear from the record.

## 7. Evidence, claims, and provenance rules

Each recorded input has exactly one `claim_class` and one `provenance` (§0). The
platform verifies nothing in this increment.

- `observed_fact` / `owner_requirement` / `operator_reported_result` / `assumption`
  / `external_reference` / `unsupported_claim` / `constraint` are the truth-status
  classes; `missing_information` is recorded only as a `Gap` (never as a stored
  input claiming content).
- An owner statement (e.g. avoiding a brake-lever wire, or rough-road concern) is an
  `owner_requirement` or `assumption` with `provenance = seeded_owner_context` or
  `operator_entered`. It is **never** recorded or displayed as a verified
  `observed_fact`.
- `operator_reported_result` and `external_reference` are explicitly **unverified**
  in this increment (see §12): they are labelled `operator_reported_unverified` and
  `external_reference_unverified` respectively and neither advances to "verified
  evidence."
- `unsupported_claim` is excluded from readiness advancement.
- **Fabricated / prohibited content** MUST NOT be produced: no invented physical
  results, no invented calibration/bench/field data, no invented external sources.
  Absent information is recorded only as a `Gap` (and, where applicable, a
  `BlockingReason`), never as an input asserting content.

No benchmark result may be represented anywhere in the workspace or export: **no
benchmark run has occurred** (S2 §10). Model-generated explanatory text may vary,
but classifications, gaps, blockers, and readiness must be deterministic and
attributable. Only deterministic recorded classifications affect readiness, subject
to the §5 blocking rules.

## 8. Export artifact

The authoritative export artifact is a **canonical JSON `DecisionRecord`** (§11).
An optional human-readable Markdown rendering MAY be generated from that same JSON
record but is never a second independent source of truth.

The exported JSON MUST preserve and clearly label:

- `schema_version`, `export_format`, decision identity, `decision_question`, and
  `revision`;
- the three candidates with `option_status`, `disposition_reason`, and
  `disposition_basis` where applicable;
- all classified inputs (`claim_class` + `provenance`), with `operator_reported_unverified`
  / `external_reference_unverified` labelling where applicable;
- owner requirements (as `owner_requirement` inputs/constraints), never as facts;
- unresolved gaps, with blocking/non-blocking status and any
  `reclassification_rationale`;
- blockers (`blocking_reasons` with affected scope);
- `readiness_status` (and the user-facing label, e.g. `REVIEW REQUIRED`, marked as a
  label not a stored status);
- `owner_preference` if set, explicitly marked as preference, not selection;
- `change_impact_summary` for the latest accepted change (§9);
- `export_metadata` with the single `generated_at` and `export_revision`;
- an explicit `limitations` block stating at minimum: in-memory only / not durable /
  restart restoration not supported; no benchmark run; no external retrieval; no
  physical testing; no verified evidence; no final technical selection; advisory
  only.

The export MUST be understandable without the conversation and MUST NOT require
persistence delivery. Saving the exported file is an operator action, not a platform
persistence feature.

## 9. Change-impact model

`change_impact_summary` is a deterministic derived value computed from the latest
accepted `ChangeEvent` (it is not independently authored). It MUST contain:

- the changed item (`target_id` and a short description);
- the affected candidate(s);
- the affected gap(s) or blocker(s);
- the prior `readiness_status`;
- the new `readiness_status`.

It is recomputed on every accepted change and shown in the workspace and export.

## 10. Error and boundary behavior

User-visible handling:

- **No usable inputs** → `readiness_status=insufficient_information`; the workspace
  lists named gaps; no candidate is recommended.
- **Conflict** → record both inputs, raise `unresolved_evidence_conflict` (scope as
  applicable), hold readiness below `decision_ready_for_owner_review`, and resolve
  only via an explicit `conflict_resolved` `ChangeEvent`; never silently pick one.
- **Owner preference conflicts with readiness** → keep the preference recorded, raise
  `owner_preference_conflicts_with_readiness`, display both; never auto-resolve by
  upgrading the preferred candidate.
- **Required constraints missing** → raise `missing_installation_constraint` /
  `missing_false_positive_tolerance` and keep affected candidates
  `candidate_not_yet_comparable`.
- **A candidate cannot yet be compared** → flag `candidate_not_yet_comparable`
  (scope=candidate); continue comparing the others; readiness cannot reach
  `decision_ready_for_owner_review` until that candidate is accounted for (§7).
- **A final answer requested prematurely** → return the current bounded state and an
  explicit truthful block; never emit a `technically_selected` or
  production/readiness claim.

## 11. Export format and schema

- `export_format = json` is the single canonical, authoritative artifact.
- `schema_version` is present on `DecisionRecord` and `ExportMetadata` and is
  incremented when the export shape changes.
- Markdown rendering is OPTIONAL and is generated deterministically from the JSON
  record; it is a view, not a source of truth, and must not contain fields absent
  from the JSON.

## 12. Evidence labels are explicitly unverified

This increment performs no verification. Operator-reported and external inputs use
labels that cannot imply platform verification:

- `operator_reported_unverified`;
- `external_reference_unverified`.

Neither advances to "verified evidence" in this increment. Only deterministic
recorded classifications may affect readiness, subject to the §5 blocking rules.

## 13. Candidate elimination is contextual, not a validity verdict

When a confirmed mandatory owner requirement removes a candidate, the result MUST be
expressed as `disposition_basis = incompatible_with_recorded_requirement` — NOT as
`technically_invalid`. The candidate is incompatible with a recorded requirement in
this decision context, not proven technically invalid in general. The `Candidate`
carries `disposition_basis` (§4), and the UI and export must preserve the contextual
nature of every disposition (e.g. "eliminated because it conflicts with the recorded
'no wire to brake lever' requirement", reversible if that requirement changes).

## 14. Acceptance criteria (for the later implementation; tests authored separately)

Testable criteria the later implementation must satisfy:

1. **Workspace behavior** — opening the fixed decision renders all §3 areas with the
   three candidates pre-listed and the fixed question.
2. **Candidate rendering** — exactly the three candidates appear; none is labeled a
   winner; eliminated/deferred/blocked candidates show `disposition_reason` and a
   contextual `disposition_basis` (§13).
3. **Claim/provenance separation** — every input carries both `claim_class` and
   `provenance`; an owner statement is never shown as `observed_fact`; `provenance`
   alone never upgrades truth-status.
4. **No missing-as-evidence** — missing information appears only as a `Gap` (and
   `BlockingReason`), never as a stored input asserting content.
5. **Readiness determinism** — `readiness_status` follows the §5 ordered table
   exactly; identical inputs yield identical status; pre-seeded gaps do not force an
   initial `blocked_by_evidence_gap`; only §5 values can appear.
6. **All three candidates accounted for** — `decision_ready_for_owner_review` is
   unreachable while any candidate is neither fully comparable nor explicitly
   disposed with a valid basis (§7).
7. **No blocking-gap waiver** — a readiness-blocking gap can only become non-blocking
   via a recorded `gap_reclassified` rationale; the original gap and the
   reclassification remain in `history` and export.
8. **Blocker display** — every active `blocking_reason` shows code and affected
   scope; resolving the underlying input clears it deterministically.
9. **Change-impact** — every accepted add/update/remove/resolve increments
   `revision`, appends the appropriate §10 `ChangeEvent`, and recomputes
   `change_impact_summary` and readiness consistently.
10. **Export correctness** — the canonical JSON export contains `schema_version`,
    `export_format`, every required field, the single `generated_at`, and the
    `limitations` block (including "restart restoration not supported"); it is
    readable without the conversation; any Markdown is a faithful render of it.
11. **No persistence coupling** — the increment functions with session persistence
    absent/paused; no code path requires `engine/session_store.py` or writes durable
    session state; tests pass without any persistence module.
12. **No fabricated content** — no test fixture or runtime path invents physical,
    calibration, external, or benchmark results.
13. **No false final-selection claim** — no output yields `technically_selected`,
    `approved`, `validated`, `certified`, `production_ready`, or `frozen`;
    `owner_preference` never sets selection.
14. **Single authoritative timestamp** — exactly one `generated_at` exists, in
    `ExportMetadata`.

## 15. Anticipated implementation surface (informational only — authorizes no edits)

Read-only inspection of the committed tree at `bc1234e` indicates a later
implementation may need to inspect (NOT yet modify) the following existing paths.
This list is informational; it grants no edit authority and may be revised when an
implementation authorization is issued:

- `engine/idea_state.py` — current `IdeaState` model; a new decision-record model
  would live alongside it, not replace it.
- `engine/deliverable_assembler.py` — existing `assemble_deliverable(state)` and its
  section builders show the established "assemble a structured record" pattern an
  export could follow.
- `engine/enums.py` — existing enum conventions to align with (without contradicting
  the committed vocabularies).
- `web/app.py` — Flask routes/session handling; a workspace route would be added
  here. Note: `web/app.py` is one of the seven paused persistence paths in the
  ORIGINAL worktree and is frozen there; this increment must not couple to that
  persistence work.
- `web/templates/deliverable.html`, `web/templates/session.html`,
  `web/templates/success_criteria.html` — existing template patterns for a new
  workspace template.
- `engine/path_n_questions.py`, `engine/progression_loop.py` — existing
  plain-language question / progression patterns to reuse rather than reinvent.

No new domains, modules, or paths are asserted to exist beyond those observed above.

## 16. Explicit non-goals

This increment does NOT include and MUST NOT perform:

- no persistence modification; no session restoration/durability;
- no live external-source retrieval;
- no simulation;
- no physical benchmark run; no execution of the bicycle brake-light competitive
  benchmark;
- no patent output;
- no BOM finalization;
- no wiring or firmware verification;
- no final architecture selection (`technically_selected`/`frozen`);
- no multi-domain expansion (electronics only);
- no Path T;
- no Phase 5 or Phase 6 action;
- no commercial-differentiation lane activation;
- no Commit B (no Roadmap §§4–7 change);
- no change to any hold or closed state.

## 17. Later implementation authorization gate

Before any code is written for this increment, ALL of the following must hold (this
section creates no new governance program; it lists preconditions and creates no
bypass of the committed activation sequence):

1. **Lane activation via the committed sequence.** Commit B and the committed Roadmap
   §12.D activation sequence must be completed before implementation. The ONLY
   alternative to that sequence is a prior controlled amendment to the controlling
   roadmap or anchor that is explicitly approved, committed, and verified before any
   implementation relies on it. A bounded owner message alone does NOT bypass the
   committed roadmap activation sequence.
2. **This spec accepted** — this document is owner-reviewed and accepted (or its
   accepted revision identified) as the implementation target.
3. **Explicit scope grant** — a separate, explicit owner authorization (required in
   addition to, and after, activation) names the exact files the implementation may
   create/modify, on the clean worktree, with the holds in §16 preserved.
4. **Test plan reference** — acceptance criteria (§14) are turned into a named test
   set the implementation must pass, with no persistence coupling and no fabricated
   content.

Until all four are met, this specification remains non-activating planning only and
authorizes no code.
