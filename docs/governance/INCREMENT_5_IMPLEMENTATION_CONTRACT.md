# Increment 5 Implementation Contract — Concrete Validation-Plan Generation

Status:
`DRAFT IMPLEMENTATION CONTRACT — NOT TESTS-FIRST OR SOURCE AUTHORIZATION`

Authoritative baseline at drafting:
`606f325fd4fafceb189de4dab9d7f182c3c33949` (PR #57 roadmap-synchronization
true-merge; ordered parents `0c96c3fc88d9f1faa18860a3046b6d4df4a2b49a` then
`4380fd8e9f0a758893851887dd9e060a21d69613`). Product-execution tip
`f1734285162915ac577c93a37b30e7babd68586e` (PR #54 Increment 4 SOURCE merge).
The live tip is always resolved from Git; this SHA is a document-publication
baseline, not a permanent live-tip assertion.

## 1. Authority lineage

This document is the bounded, owner-gated IMPLEMENTATION CONTRACT DRAFT for
Increment 5 — Concrete Validation-Plan Generation, the fifth increment of the
committed Product-Value Correction Plan (dependency order 3 → 4 → **5** → 6). It
translates the already-merged Increment 5 bounded design into exact, independently
testable implementation obligations, invariants, names, and acceptance criteria.

Its authority is bounded by and subordinate to, in this exact order (where any of
the following and this contract could differ, the following controls):

1. `MVP_SCOPE_FREEZE.md` and the active governance anchors
   (`ILT-002_GOVERNANCE_ANCHOR.md`, `OWNER_PRODUCT_IDENTITY_CORRECTION.md`,
   `STRATEGIC_PRODUCT_VISION.md`, `PATH_N_CURRENT_EXECUTION_ANCHOR.md`,
   `DUAL_PATH_PRODUCT_ANCHOR.md`);
2. `GOVERNANCE_MODEL.md`;
3. the merged Increment 5 bounded design
   `docs/governance/INCREMENT_5_DESIGN.md` (338 lines, 20023 bytes, SHA-256
   `bb2708af10538f59706733f415756500577414cfc35c76904e1a1b717fdb953b`, blob
   `067c5753deff2fe8af5e2f3ec347f85e6fe28067`) — including its ten owner rulings
   (§0 ratification, §18 traceability) and design clauses §1–§19;
4. the synchronized `docs/governance/ACTIVE_EXECUTION_ROADMAP.md`
   (1146 lines, 127157 bytes, SHA-256
   `72de6af07586b029563ec957d363f1efa453b32b08d986f98d9adcac4ba3924e`, blob
   `2c9da286eefe485d43f8769d55db39807ab147fa`);
5. `docs/governance/GOVERNED_EXECUTION_EFFICIENCY_PROTOCOL.md` (subordinate
   operational protocol; overrides no anchor, freeze, hold, or authorization);
6. the closed Increment 3 authority (`INCREMENT_3_IMPLEMENTATION_CONTRACT.md`,
   `R-1`..`R-6`) and the closed Increment 4 authority
   (`INCREMENT_4_AUTHORITY_RULINGS.md` `C4-R1`..`C4-R13`, `INCREMENT_4_DESIGN.md`
   `D-1`..`D-7`, `INCREMENT_4_IMPLEMENTATION_CONTRACT.md`).

Distinctions this contract preserves:
- **Committed authority:** items 1–6 above and the ten Increment 5 owner rulings.
- **Historical precedent:** the Increment 2/3/4 lifecycle shape and file-naming
  convention. Precedent informs but does not itself gate.
- **Candidate implementation detail:** exact private helper names, internal
  decomposition, and non-public structure remain candidate until source.
- **Downstream authority not yet granted:** tests-first, source, template
  implementation, staging, commit, push, PR, review, merge — none is granted by
  this contract (see §2, §24).

The separate owner authorization to author this contract is the roadmap-recorded
`OWNER-GATED AUTHORING OF THE INCREMENT 5 IMPLEMENTATION CONTRACT`.

This contract does not reopen the ten owner rulings, does not redesign the merged
design, and adds no authority beyond faithfully realizing them. Every name it
fixes is a contract-selected label over a design-required fact, never a new
product signal.

## 2. Contract status and non-authorization

This document:
- is an IMPLEMENTATION CONTRACT only;
- does NOT authorize tests-first creation;
- does NOT authorize source or template implementation;
- does NOT authorize staging, commit, push, PR creation, review, or merge (of
  this contract or of any later artifact);
- does NOT authorize persistence, the paused persistence worktree, the domain
  registry, domain packs, scoring, `engine/progression_loop.py`, a professional
  workspace, Increment 6, roadmap mutation, or anchor mutation;
- creates no product behavior and changes no source, template, test, roadmap,
  anchor, or ruling by its existence.

Its mere existence, once merged, authorizes nothing to be built. Every downstream
step is a separate, explicit, owner-gated authorization (§24).

## 3. Exact implementation scope

IN SCOPE (MVP-1), when a later separate authorization permits source:
- a pure, deterministic, read-only derivation of a **validation plan** from an
  already-recorded `IdeaState`, expressed as a structural, generic sequence of
  proposed validation steps;
- exactly ONE additive deliverable section rendering the plan;
- exactly ONE additive machine-package key carrying the JSON-safe plan;
- deterministic derivation, identity, deduplication, and organizational ordering.

EXCLUDED (MUST NOT), in MVP-1 and by this contract:
- any session-UI change; any `web/app.py` change; any `web/templates/session.html`
  change;
- any persistence, paused-persistence-worktree, domain-registry, domain-pack, or
  professional-workspace change or dependency;
- any scoring; any `engine/scoring.py` or `engine/progression_loop.py` change;
- any modification of `_s4`, `_s6`, the Increment 3 next-development-step section
  (`_s12` / `section_12_next_development_step`), or the Increment 4 requirement-
  landscape section (`_s13` / `section_13_requirement_landscape`);
- generating external validation documents;
- inventing or prescribing ungrounded standards, equipment, thresholds,
  measurements, test values, acceptance values, jurisdictions, regulatory
  requirements, or domain-specific professional procedures;
- claiming feasibility, safety, compliance, testing, verification, market-
  readiness, implementation-readiness, or risk-freeness (§13).

## 4. Input contract

- **Entry point:** a single pure function `derive_validation_plan(state)` where
  `state` is an `engine.idea_state.IdeaState`.
- **Primary committed input:** the Increment 4 derivation
  `engine.requirement_landscape.derive_requirement_landscape(state)`, whose
  immutable `RequirementLandscape.requirements` tuple (each a frozen
  `DerivedRequirement`) is the sole structural feed for validation steps. Each
  `DerivedRequirement` supplies: `requirement_id`, `statement`, `primary_anchor`
  (`ProvenanceAnchor{anchor_kind, anchor_reference, display_label}`),
  `source_status`, `criticality`, `criticality_authority`, `resolving_action`
  (`ResolvingAction{action_kind, statement, source_reference}` or `None`), and
  `linked_risk_ids`.
- **Increment 2 axes (read-only, via `engine.idea_state` only):** where a step's
  classification consults record truth, it MAY read `AssertionRecord` fields
  already carried on the ledger — `disposition`, `provenance`, `validation_status`,
  `superseded_by` — reachable through `engine.idea_state` (no third import). Active-
  set and supersession handling are inherited: only records with
  `superseded_by is None` participate, exactly as the Increment 4 derivation
  already enforces on `state.assertions` and `state.get_open_gaps()`.
- **Import boundary (frozen invariant):** the Increment 5 engine module MAY import,
  among project modules, ONLY `engine.idea_state` and the Increment 4 requirement-
  landscape module. It MUST NOT import or depend on scoring, progression,
  persistence, session, `web/app.py`, the domain registry/packs, the AI advisor,
  or `engine.idea_development_outputs`.
- **Closed Increment-3 ruling (frozen invariant, F-INC5-1):** Increment 5 does NOT
  read `derive_next_development_step`, does NOT read the Increment 3 next-
  development-step output, and does NOT import `engine.idea_development_outputs`.
- **Authoritative input fields:** the derivation invents no recorded signal; every
  emitted artifact is grounded in a `DerivedRequirement` (itself grounded in a
  `rec_N` record, an order-normalized `rec_N|rec_N` contradiction pair, or a
  `gap_type`).
- **Missing / malformed inputs → truthful outcome (not error):**
  - if `derive_requirement_landscape(state)` yields zero requirements → `EMPTY`
    (§12);
  - if requirements exist but none can support a truthful step → `BLOCKED` (§12);
  - a malformed individual `DerivedRequirement` (e.g. `resolving_action is None`
    or a missing anchor) is skipped or converted to a blocked item per §8/§12; it
    never fabricates content and never raises.
- **No new `IdeaState` field is added or required.**

## 5. Output contract

`derive_validation_plan(state)` returns one immutable value, `ValidationPlan`.
All payloads are frozen dataclasses; all collections are tuples; equality is
structural (reusing the Increment 4 immutability discipline). No field may state
or imply supplied evidence or a verified result (§13).

`ValidationPlan`:
| field | type | required | allowed values | empty/null | source of truth | epistemic meaning | JSON-safe form |
|---|---|---|---|---|---|---|---|
| `outcome` | str | required | `PLAN`, `EMPTY`, `BLOCKED` (§6) | never null | derived (§6) | which plan state holds | the exact token |
| `steps` | tuple[`ValidationStep`] | required | 0..N ordered, deduplicated | `()` | §8 | proposed validation actions | JSON array |
| `blocked_items` | tuple[`BlockedValidationItem`] | required | 0..N ordered | `()` | §8/§12 | recorded signals that cannot yet form a step | JSON array |

`ValidationStep` (carries ONLY the following):
| field | type | required | allowed values | empty/null | source of truth | epistemic meaning | JSON-safe form |
|---|---|---|---|---|---|---|---|
| `step_id` | str | required | `vstep:` + the supporting `requirement_id` (§9) | never empty | Increment 4 stable key | stable identity, never positional | string |
| `statement` | str | required | the supporting `resolving_action.statement`, verbatim | never empty | Increment 4 `ResolvingAction.statement` | what must be validated (proposed) | string |
| `responsibility` | str | required | one of the five classes (§7) | never null | deterministic mapping (§7) | who must perform the action | the exact token |
| `evidence_category` | str | required | one bounded generic label (§7) | never empty | deterministic mapping (§7) | category of evidence that would close the step | string label |
| `closure_condition` | str | required | fixed template (§13) | never empty | template over `evidence_category` | what would close the step (required, not supplied) | string |
| `provenance` | `ProvenanceRef` | required | structurally addressable (§9) | never null | Increment 4 `primary_anchor` | authorized recorded source | nested object (label rendered; §16) |
| `confidence` | str | required | `UNDETERMINED` (MVP-1) (§14) | never null | §14 | truthful structural confidence | the exact token |

`ProvenanceRef` (structural provenance, mirrors the design's provenance concept):
| field | type | required | meaning |
|---|---|---|---|
| `anchor_kind` | str | required | Increment 4 `anchor_kind` (routing enum; NOT rendered, §15) |
| `reference` | str | required | Increment 4 `anchor_reference` (`rec_N`, `rec_N|rec_N`, or `gap_type`) |
| `display_label` | str | required | Increment 4 `display_label` (the only user-visible provenance text) |

`BlockedValidationItem`:
| field | type | required | meaning |
|---|---|---|---|
| `item_id` | str | required | `vblock:` + supporting `requirement_id` |
| `reason` | str | required | fixed, generic statement of why no truthful step can form |
| `missing` | str | required | the missing evidence, authority, or input category (bounded, generic) |
| `responsibility` | str | required | one of the five classes (or `UNDETERMINED`) |
| `provenance` | `ProvenanceRef` | required | as above |

A `ValidationStep` has NO `result`, `verdict`, `validated`, `supplied`, `passed`,
or `verified` field. MVP-1 introduces no supplied-evidence and no verified-result
field anywhere (§13).

## 6. Exact plan-level outcome representation (resolves PR56-O2)

Internal allowed `outcome` values (exact, uppercase tokens): `PLAN`, `EMPTY`,
`BLOCKED`. These are a bounded status vocabulary.

Deterministic selection:
- `EMPTY` — `derive_requirement_landscape(state).requirements` is empty (no active
  provenance-anchored requirement exists). `steps == ()` and `blocked_items == ()`.
- `PLAN` — at least one `ValidationStep` is emitted (`len(steps) >= 1`).
- `BLOCKED` — at least one requirement exists but zero steps are emitted because
  every candidate is ineligible (§8); `blocked_items` is non-empty and `steps ==
  ()`. (In the current MVP-1 corpus every Increment 4 anchor kind maps to an
  eligible, truthful step, so `BLOCKED` is expected to be unreachable in practice;
  it is defined and testable for completeness and must never be silently omitted.)

Machine-package representation: the `outcome` is emitted in the machine package as
its exact token string (`"PLAN"` / `"EMPTY"` / `"BLOCKED"`). Raw bounded-status
tokens ARE permitted in the machine package, consistent with the merged Increment 4
precedent where `_s13` emits `criticality = "UNDETERMINED"` and
`criticality_authority = "system-derived"` as tokens. This applies to the bounded
status fields `outcome`, `responsibility`, and `confidence`.

Human-visible representation: rendered user-facing output MUST NOT show any raw
`outcome`/`responsibility`/`confidence` token, any `anchor_kind`, `action_kind`,
`requirement_id`, `step_id`, or `item_id`. Each outcome renders as a fixed human
sentence (§15): a PLAN renders the ordered steps; an EMPTY renders the empty
statement; a BLOCKED renders the blocked items with their generic missing-input
text. No raw enum token leaks into rendered output (mirrors Increment 4 §7.3).

## 7. Responsibility semantics

The five responsibility classes are frozen, exactly: `OWNER_EXECUTABLE`,
`SYSTEM_DERIVABLE`, `SPECIALIST_REQUIRED`, `EMPIRICAL_EVIDENCE_REQUIRED`,
`UNDETERMINED`. Each names WHO must perform or resolve the validation action —
never the fact that the system generated the plan.

Deterministic, structural selection (keyed on the supporting requirement's
Increment 4 `primary_anchor.anchor_kind` and `resolving_action.action_kind`; never
on free text, keywords, or LLM judgment):

| anchor_kind | action_kind | responsibility | evidence_category |
|---|---|---|---|
| `active_contradiction` | `reconcile_recorded_contradiction` | `OWNER_EXECUTABLE` | `reconciliation of conflicting records` |
| `pending_evidence` | `provide_requested_evidence` | `EMPIRICAL_EVIDENCE_REQUIRED` | `empirical evidence` |
| `pending_specialist` | `obtain_requested_specialist_input` | `SPECIALIST_REQUIRED` | `specialist input` |
| `assertion` | `validate_recorded_answer` | `OWNER_EXECUTABLE` | `owner confirmation` |
| `gap` | `address_open_gap` | `UNDETERMINED` | `owner clarification` |

Rules:
- exactly ONE responsibility class per step (no multi-class steps in MVP-1);
- the mapping is total over the five Increment 4 anchor kinds and is the single
  precedence source — no additional structural signal is consulted, so no
  precedence conflict can arise;
- `gap` maps to `UNDETERMINED` deliberately: a `gap_type` carries no structural
  signal identifying an actor, and inferring one (e.g. reading
  `EXPERTISE_GAP_AWARENESS` as "specialist") would invent domain meaning and is
  prohibited;
- `SYSTEM_DERIVABLE` is part of the frozen vocabulary but NO MVP-1 anchor kind maps
  to it; the source must not manufacture a `SYSTEM_DERIVABLE` step, and in
  particular must never assign it merely because the system produced the plan
  (prohibition/eligibility is separate from actor class — §8);
- an anchor kind or action kind outside the table above is treated as unsupported:
  the candidate is ineligible and yields a blocked item (§8), never a guessed
  class.

## 8. Eligibility and emission rules

Prohibition is modelled as an emission-eligibility decision, distinct from the
responsibility class (design §5). Deterministic rules:
- **Step emitted** when the supporting `DerivedRequirement` has a non-`None`
  `resolving_action`, a well-formed `primary_anchor`, and an `anchor_kind` present
  in the §7 mapping. Exactly one step per eligible requirement.
- **Blocked item emitted** when a requirement exists and is structurally anchored
  but cannot support a truthful step (e.g. `resolving_action is None`, or an
  `anchor_kind` outside the §7 mapping). The blocked item names the missing
  input/authority generically and retains provenance. No step is fabricated to
  fill the gap.
- **Nothing emitted** for that requirement only when it is malformed beyond
  structural addressability (e.g. missing `primary_anchor`/`requirement_id`); such
  a record is skipped independently (per-record degradation, mirroring Increment 4
  §9.10.6) and never aborts the derivation.
- **Superseded / inactive exclusion** is inherited from the Increment 4 derivation
  (only `superseded_by is None` records and open/partial gaps feed the landscape);
  Increment 5 adds no records and re-derives nothing that the landscape excluded.
- **Unsupported content is rejected, not inferred:** the source must never
  synthesize a standard, threshold, procedure, measurement, or actor that is not
  present as a structural signal.

## 9. Identity and provenance

- **Step identity:** `step_id = "vstep:" + requirement_id`, where `requirement_id`
  is the Increment 4 stable anchor key (`req:assertion:{rec_N}`,
  `req:evidence:{rec_N}`, `req:specialist:{rec_N}`,
  `req:contradiction:{lo}|{hi}`, or `req:gap:{gap_type}`). Blocked-item identity:
  `item_id = "vblock:" + requirement_id`.
- **Identity inputs are stable keys only.** Identity MUST NOT derive from list
  position, iteration order, or wall-clock. Increment 5 introduces no new anchor
  kinds and reuses Increment 4's stable keys.
- **Provenance** is structurally addressable via `ProvenanceRef` carrying the
  Increment 4 `anchor_kind`, `anchor_reference`, and `display_label`. Every step
  and every blocked item MUST retain such provenance; none may exist without it.
- **Single-source mapping:** one step maps one-to-one to exactly one supporting
  `DerivedRequirement` (which is itself one-to-one with a record, a contradiction
  pair, or a gap type). Increment 5 invents NO causal relationship between
  independent records and composes none (§10).
- **Deterministic provenance:** the `anchor_reference` for a contradiction pair is
  the Increment 4 order-normalized `lo|hi`; Increment 5 reuses it unchanged.

## 10. Deduplication and composition

- **Deduplication key:** `step_id` (equivalently the supporting `requirement_id`).
  Blocked items dedupe by `item_id`.
- **Participating fields:** the key only; two steps with the same `step_id` are the
  same step. Because Increment 4 already guarantees unique `requirement_id`s per
  active anchor, deduplication is a defensive invariant (it must hold, and a
  duplicate key is a failure condition — §21).
- **No composition in MVP-1:** multiple requirements MUST NOT be merged into one
  step, and one requirement MUST NOT yield multiple steps. One requirement ⇒ at
  most one step or one blocked item.
- **Collision handling:** a duplicate `step_id` must not silently drop or merge
  information; it is a determinism defect (§21).
- **Information preservation:** every eligible requirement is represented exactly
  once; no requirement is silently discarded except the per-record malformed skip
  of §8, which the source must be able to surface in testing.

## 11. Ordering

- **Ordering follows the Increment 4 landscape order.** The Increment 4 derivation
  already returns `requirements` in a deterministic, organizational-only order
  (its `_order_key`: precedence `active_contradiction → pending_evidence →
  pending_specialist → assertion → gap`, then order-normalized `rec_N` / `gap_type`
  within kind). Increment 5 emits steps in that same order and re-ranks nothing.
- Ordering is deterministic and equivalent-state order-independent: the same
  `IdeaState` (regardless of input record insertion order) yields an equal
  `ValidationPlan` with identical step order.
- Ordering is ORGANIZATIONAL ONLY. It MUST NOT imply, and no field or rendered
  string may present it as, severity, urgency, business priority, safety priority,
  or criticality. (All criticality is `UNDETERMINED` and grounded risk is empty in
  the current corpus.) No committed structural signal authorizes any ranking
  meaning in MVP-1.
- `blocked_items` are ordered by the same key over their supporting requirements.

## 12. Empty, blocked, partial, malformed, and degraded outcomes

| condition | outcome | steps | blocked_items | rendered |
|---|---|---|---|---|
| no active provenance-anchored requirement | `EMPTY` | `()` | `()` | fixed empty statement |
| ≥1 eligible requirement | `PLAN` | ordered steps | ineligible-only items (usually `()`) | ordered steps |
| ≥1 requirement, all ineligible | `BLOCKED` | `()` | ordered blocked items | blocked items + generic missing text |
| a single malformed requirement among valid ones | outcome unaffected | valid steps continue | optionally one blocked item | unaffected |
| total derivation failure | MUST NOT occur | — | — | derivation must not raise; degrade instead |
| duplicate-only input | deduped (§10) | one step per unique key | — | as PLAN |
| zero grounded risk | not a plan state | — | — | never presented as safe/verified/risk-free |

- The `EMPTY` statement is idea-development-framed (not an error), analogous to the
  Increment 4 `_REQUIREMENT_LANDSCAPE_EMPTY` wording; the source selects an
  Increment-5-specific empty statement of the same character.
- A `BLOCKED` outcome truthfully identifies the missing evidence, authority, or
  input and names the responsibility class and provenance; it never invents a step.
- Malformed data never fabricates fallback content and never crashes derivation or
  deliverable assembly (mirrors Increment 4 §9.10.6).
- Zero grounded risk (inherited: Increment 4 emits none in MVP-1) MUST NEVER be
  presented as "risk-free", safe, or verified (§13).

## 13. Epistemic truth and non-claims

Four epistemic levels are distinguished: (1) proposed validation action; (2)
required evidence category; (3) evidence actually supplied; (4) verified result.
**MVP-1 generates ONLY levels 1 and 2.** It never represents levels 3–4 and never
implies them.

- `statement` is a level-1 proposed action (the Increment 4 resolving-action
  statement, verbatim — no invented content).
- `evidence_category` is a level-2 required category.
- `closure_condition` is the truthful level-2 statement of what WOULD close the
  step, using the fixed template: `"Closed when {evidence_category} is provided and
  recorded; no such evidence is recorded yet."` It must read as "evidence
  required", never "evidence supplied" or "passed".
- No field, label, ordering, or rendered string may state or imply that evidence
  was supplied, a step passed, the plan was executed, or the idea is feasible,
  safe, compliant, tested, verified, market-ready, implementation-ready, or
  risk-free. Any such wording is a blocking defect (§21).

## 14. Confidence

- Allowed MVP-1 `confidence` value: `UNDETERMINED` (only). Every emitted step and
  blocked item carries `confidence = UNDETERMINED`, because no structural
  confidence-elevation signal exists in the current corpus (all Increment 4
  criticality is `UNDETERMINED`; grounded risk is empty).
- `confidence` MUST NOT be inferred from language quality, keyword matching, free
  text, LLM judgment, absence of contradictory evidence, or domain assumptions
  (mirrors Increment 4 §9.7.3 / §9.8.1).
- The representation is a bounded token; the vocabulary may later widen only under a
  separate authority with a proven structural signal — not in MVP-1.

## 15. Rendering contract

- Exactly ONE additive deliverable section titled `Validation Plan`, rendered in
  `web/templates/deliverable.html`, placed additively (it changes no existing
  section and no existing key).
- Per step it shows human-readable fields ONLY: `statement`, a human label for
  `responsibility`, `evidence_category`, `closure_condition`, the provenance
  `display_label`, and a human label for `confidence`. It MUST NOT render any raw
  token (`outcome`, `responsibility`, `confidence`), `anchor_kind`, `action_kind`,
  `requirement_id`, `step_id`, or `item_id` (mirrors Increment 4 §7.3).
- Human labels for the bounded tokens are fixed, e.g.: `OWNER_EXECUTABLE` → "Owner
  can perform"; `SPECIALIST_REQUIRED` → "Specialist input required";
  `EMPIRICAL_EVIDENCE_REQUIRED` → "Empirical evidence required";
  `SYSTEM_DERIVABLE` → "System can derive"; `UNDETERMINED` → "Responsibility
  undetermined" (for responsibility) / "Confidence undetermined" (for confidence).
  The exact label strings are contract-selected presentation over the frozen
  tokens and may be finalized in source, but a raw token must never be shown.
- It renders the `EMPTY` and `BLOCKED` outcomes truthfully (empty statement;
  blocked items with generic missing-input text).
- It MUST present steps as PROPOSED, never as completed/passed/verified, and MUST
  NOT imply feasibility, safety, compliance, testing, verification, market-
  readiness, or implementation-readiness.
- Jinja autoescape MUST remain enabled for all rendered fields (injection safety,
  design §14); no `|safe` on record-derived or plan-derived text.
- When an optional value is absent, render nothing for it rather than a raw
  `None`/token.
- NO `web/app.py` and NO `web/templates/session.html` change.

## 16. Machine-package contract

- Exactly ONE additive package key: `section_14_validation_plan`, produced by a
  section builder `_s14(state)` in `engine/deliverable_assembler.py` and added to
  the assembled package dict. `section_14` is contract-authoritative: it is the
  next integer after the current highest key `section_13_requirement_landscape`
  (verified: existing keys run `section_10`..`section_13`), following the committed
  additive numbering; `_s14` mirrors the `_s12`/`_s13` naming and conversion
  discipline.
- `_s14` converts the immutable `ValidationPlan` to plain JSON-safe
  dicts/lists/strings WITHOUT mutating the engine payload. It contains only the
  human-semantic fields of §5 plus the bounded `outcome`.
- Deterministic list ordering: `steps` and `blocked_items` follow §11 order.
- Null vs absent vs empty-array: absent optional scalars are emitted as `null`;
  empty collections are emitted as `[]` (never `null`); `outcome` is always a
  present non-null token.
- Bounded status tokens (`outcome`, `responsibility`, `confidence`) MAY appear as
  their exact tokens in the package (precedent: `_s13` `criticality`); routing
  enums (`anchor_kind`, `action_kind`) and internal identifiers (`step_id`,
  `item_id`) are internal and are NOT required package fields — and none of them,
  nor any token, may leak into rendered user-facing output (§15).
- Provenance in the package is the human-readable `display_label` (mirroring `_s13`
  `provenance`); the structural `reference` MAY additionally be carried as a
  machine field but is never rendered.
- No serialization dependency beyond plain `dict`/`list`/`str`/`bool`/`None`; no
  circular import; no mutation of the immutable engine payload.

## 17. Backward compatibility

- No `IdeaState` schema change is made or required.
- No mutation of any Increment 1–4 output: `_s4`, `_s6`, `_s12`
  (`section_12_next_development_step`), and `_s13`
  (`section_13_requirement_landscape`) remain byte/behaviour-identical; the
  Increment 4 `derive_requirement_landscape` and `derive_next_development_step` are
  read (the former) or untouched (the latter) but never modified.
- No existing deliverable section, key, or value changes; the change is purely
  additive (`section_14_validation_plan` and one new template section).
- No persistence, session, or `web/app.py` behavior changes.
- No domain-registry dependency; the known `tests/test_domain_registry.py`
  failures remain a separate, unauthorized baseline and must be neither relied upon
  nor "fixed" here.
- Existing test arithmetic outside the new Increment 5 tests must remain unchanged
  (no non-additive regression); Increments 3 and 4 remain closed.

## 18. Allowed and prohibited implementation paths

Contract-authorized CANDIDATE paths (which a later, separately authorized tests-
first and source step MAY touch):
- NEW `engine/validation_plan.py` — pure `derive_validation_plan(state)` and the
  frozen payloads of §5; imports ONLY `engine.idea_state` and
  `engine.requirement_landscape`.
- MODIFIED `engine/deliverable_assembler.py` — add ONE section builder `_s14(state)`
  and ONE package key `section_14_validation_plan`; no other change; `_s4`, `_s6`,
  `_s12`, `_s13` untouched.
- MODIFIED `web/templates/deliverable.html` — add ONE additive `Validation Plan`
  section; no other change.
- NEW `tests/test_increment_5_validation_plan.py` — the future tests-first package.

PROHIBITED paths (MUST remain unchanged): `engine/idea_development_outputs.py`,
`engine/requirement_landscape.py` (its behavior), `engine/idea_state.py` schema,
`engine/scoring.py`, `engine/progression_loop.py`, `_s4`/`_s6` bodies,
`web/app.py`, `web/templates/session.html`, persistence paths, domain-registry
paths, domain packs, active anchors, `CLAUDE.md`, `MVP_SCOPE_FREEZE.md`, and the
roadmap. Listing a candidate path grants NO source-implementation authority; §24
governs.

## 19. Tests-first obligations

A later, separately authorized tests-first package MUST cover at least (behavioral
and boundary obligations — not incidental internal structure):
- pure / read-only / no-mutation of `state`;
- active-set filtering and supersession exclusion (inherited);
- deterministic, equivalent-state order-independent `step_id`s and plan equality;
- deterministic, severity-neutral ordering and repeated-run stability;
- the five responsibility classes and their exact structural mapping (§7),
  including `gap → UNDETERMINED` and the absence of any MVP-1 `SYSTEM_DERIVABLE`
  mapping;
- evidence-category correctness (bounded, generic, never a specific test/value);
- provenance presence on every step and blocked item, and no raw-enum/identifier
  leak into rendered output;
- `confidence == UNDETERMINED` for all MVP-1 steps;
- the four-level truth model: no `result`/`supplied`/`passed`/`verified` field or
  wording anywhere;
- `EMPTY`, `PLAN`, and `BLOCKED` selection (including a constructed `BLOCKED` case)
  and malformed-per-record degradation without raising;
- deduplication invariant (unique `step_id`);
- Increment-3 non-dependency: `derive_next_development_step` not called and
  `engine.idea_development_outputs` not imported;
- import-boundary enforcement (only `engine.idea_state` and
  `engine.requirement_landscape` imported among project modules);
- no domain-registry / domain-pack dependency; no invented domain content;
- the additive `section_14_validation_plan` machine package: JSON-safety,
  deterministic ordering, `[]`-vs-`null` rules, and the `outcome` token behavior;
- rendered raw-token leakage prevention and Jinja autoescape preserved;
- additive backward compatibility: `_s4`, `_s6`, `_s12`, `_s13`, and existing
  sections unchanged; Increments 1–4 non-regression;
- non-claim wording (no feasible/safe/compliant/verified/tested/market-ready/
  implementation-ready/risk-free).

Tests must be plain pre-source failing tests (Increment 3/4 precedent) and must
invent no product decision.

## 20. Source implementation obligations

A later, separately authorized source implementation MUST:
- realize §4–§17 exactly, using only the authorized candidate paths (§18);
- keep `derive_validation_plan` pure, deterministic, read-only, and within the
  import boundary;
- add exactly one machine-package key and one deliverable section, additively;
- make all payloads frozen and all collections tuples.

It MUST NOT: modify prior increments' behavior, widen the import boundary, touch
prohibited paths, introduce nondeterminism, invent domain content, or emit any
level-3/level-4 claim. Source is NOT implemented in this operation.

## 21. Failure conditions (block later staging / acceptance)

Any of the following blocks acceptance of a later tests-first or source artifact:
- generation of unsupported content (invented standard/threshold/procedure/
  measurement/actor/relationship);
- nondeterminism or order-dependence in identity, ordering, or plan equality;
- loss or absence of provenance on any step or blocked item;
- responsibility ambiguity (more than one class, or a guessed class for an
  unsupported anchor);
- assigning `SYSTEM_DERIVABLE` because the system generated the plan;
- any raw enum/token/identifier leak into rendered user-facing output;
- any domain-registry / domain-pack dependency or import;
- reading `derive_next_development_step` or importing
  `engine.idea_development_outputs`;
- widening the import boundary beyond `engine.idea_state` +
  `engine.requirement_landscape`;
- altering any prior output (`_s4`/`_s6`/`_s12`/`_s13`/existing sections) or any
  `IdeaState` field;
- mutating `state` during derivation;
- a malformed / non-JSON-safe machine package, or a duplicate `step_id`;
- any false or implied validation/feasibility/safety/verification/risk-free claim;
- a change to any path outside §18's authorized candidates.

## 22. Exact acceptance criteria

This contract is realized (by a later authorized artifact) only when, objectively:
1. `derive_validation_plan(state)` is pure and returns a frozen `ValidationPlan`
   with the exact §5 schema and field types;
2. `outcome ∈ {PLAN, EMPTY, BLOCKED}` selected exactly per §6;
3. every step has a `vstep:`-prefixed `step_id` derived from a stable Increment 4
   `requirement_id`, never positional; deduped per §10;
4. responsibility and evidence_category follow the §7 table exactly for all five
   anchor kinds;
5. every step and blocked item retains a `ProvenanceRef`;
6. `confidence == UNDETERMINED` for all MVP-1 steps and blocked items;
7. steps and blocked items are ordered per §11 and are equivalent-state order-
   independent (verified by shuffling input record order and asserting equality);
8. no `result`/`supplied`/`passed`/`verified` field or wording exists anywhere;
9. `EMPTY`, `PLAN`, and a constructed `BLOCKED` case each behave per §12, and
   malformed-per-record input degrades without raising;
10. the machine package `section_14_validation_plan` is JSON-safe, deterministically
    ordered, uses `[]`-vs-`null` per §16, and renders no raw token to the user;
11. `_s4`, `_s6`, `_s12`, `_s13`, and all existing sections are unchanged; the full
    suite shows no new non-baseline failures (the 31 `test_domain_registry.py`
    baseline failures excepted);
12. the import boundary and Increment-3 non-dependency hold exactly.

No acceptance criterion relies on unverifiable wording ("high quality",
"appropriate", "robust", "user friendly", "sufficient") without the measurable
definition given above.

## 23. Traceability

| Contract clause | Ten rulings | Design clause | Higher authority / resolution |
|---|---|---|---|
| §3 scope / exclusions | 1, 7, 8, 10 | §2 | MVP_SCOPE_FREEZE |
| §4 input + import boundary + Inc-3 non-dependency | 2, 8 | §3, §12 (F-INC5-1) | merged design F-INC5-1 |
| §5 output model | 2, 3, 4, 5 | §4 | — |
| §6 outcome representation | 4, 9 | §4, §11 | **contract-level resolution of PR56-O2** |
| §7 responsibility | 3 | §5 | — |
| §8 eligibility/emission | 3, 9 | §5, §9 | — |
| §9 identity/provenance | 5, 6 | §6, §8 | Increment 4 stable keys |
| §10 dedup/composition | 2, 6 | §8 | — |
| §11 ordering | 6 | §8 | — |
| §12 empty/blocked/malformed | 9, 4 | §9 | Increment 4 §9.10.6 |
| §13 epistemic non-claims | 4, 10 | §7, §13 | — |
| §14 confidence | 5 | §6 | — |
| §15 rendering | 4, 6, 7, 10 | §10 | Increment 4 §7.3 |
| §16 machine package | 4, 8 | §11 | **PR56-O2 resolution**; `_s13` precedent |
| §17 backward compatibility | 7, 8 | §12 | — |
| §18 paths | 1, 7, 8 | §15 | — |
| §19 tests-first obligations | all | §16 | Increment 3/4 precedent |
| §20 source obligations | all | §17 | — |
| §21 failure conditions | 4, 6, 8, 9, 10 | §13, §14 | — |
| §22 acceptance | all | §17 | — |

Contract-level choices explicitly identified: (a) the machine-package `outcome`
token representation and the "bounded tokens allowed in package / never in rendered
output" rule (§6, §16 — resolves PR56-O2); (b) the fixed `section_14_validation_plan`
/ `_s14` names (§16); (c) the `vstep:`/`vblock:` identifier prefixes (§9); (d) the
`gap → UNDETERMINED` responsibility and the no-MVP-1-`SYSTEM_DERIVABLE` mapping
(§7); (e) the fixed `closure_condition` template (§13). None reopens a ruling or
redesigns the merged design.

## 24. Lifecycle boundary

After this contract is independently reviewed and (separately) merged:
- tests-first authoring STILL requires a separate, explicit owner authorization;
- source implementation STILL requires a later, separate, explicit owner
  authorization;
- staging, commit, push, PR creation, independent review, and merge remain
  SEPARATE owner authorizations for every artifact (contract, tests-first,
  source, and any roadmap synchronization);
- the roadmap is NOT automatically updated by this contract;
- no held lane is resumed: persistence remains `PRESERVE UNMODIFIED AND PAUSE`;
  domain-registry cleanup, compact/session-summary, and Increment 6 remain
  separately gated; no synchronization with `main` is authorized.

This contract is implementation-ready but is NOT an implementation. It fixes exact
names only where required for public schema, package compatibility, deterministic
identifiers, imports, or testable lifecycle boundaries; it deliberately leaves
private helper names and internal decomposition to source.
