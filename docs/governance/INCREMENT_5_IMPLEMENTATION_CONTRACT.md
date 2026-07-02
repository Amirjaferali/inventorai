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
  already carried on the ledger — `responsibility`, `disposition`, `provenance`,
  `validation_status`, `superseded_by` — reachable through `engine.idea_state` (no
  third import). The explicit `AssertionRecord.responsibility` field, when present
  and a valid member of the responsibility vocabulary, is the PRIMARY structural
  responsibility signal (§7); `disposition` and `provenance` are fallback
  structural evidence. Active-
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
never the fact that the system generated the plan. A definite actor class is
assigned ONLY when affirmative structural evidence supports it; otherwise the
truthful value is `UNDETERMINED`.

**Responsibility precedence (deterministic; keyed only on committed structural
fields — never on free text, keywords, prose confidence, or LLM judgment):**
1. the explicit `AssertionRecord.responsibility` field, when present and a
   RECOGNIZED ledger token — **translated** through the ledger→ValidationStep table
   in §7-T below (NEVER copied verbatim); `None`, an unrecognized/invalid token, or
   structurally insufficient responsibility evidence does not resolve a definite
   actor and falls through to the next step;
2. otherwise, a `disposition`/`provenance`-supported mapping (table below);
3. otherwise, an `action_kind`-supported mapping, but ONLY where the action kind
   affirmatively identifies an actor (`provide_requested_evidence`,
   `obtain_requested_specialist_input`, `reconcile_recorded_contradiction`);
4. otherwise, `UNDETERMINED`.

**§7-T Ledger-to-ValidationStep responsibility translation (precedence 1 —
resolves C-1).** The ledger `AssertionRecord.responsibility` vocabulary is DISTINCT
from the frozen `ValidationStep.responsibility` vocabulary; a recognized explicit
ledger token is TRANSLATED through this exact table and is NEVER copied verbatim
into `ValidationStep.responsibility`:

| Ledger `AssertionRecord.responsibility` | ValidationStep responsibility |
|---|---|
| `OWNER_INPUT` | `OWNER_EXECUTABLE` |
| `SYSTEM_ANALYSIS` | `SYSTEM_DERIVABLE` |
| `SPECIALIST_INPUT` | `SPECIALIST_REQUIRED` |
| `EMPIRICAL_EVIDENCE` | `EMPIRICAL_EVIDENCE_REQUIRED` |
| `UNDETERMINED` | `UNDETERMINED` |

Translation rules:
- a recognized explicit ledger token resolves the class via this table (precedence
  1) and is never copied verbatim;
- `None`, an unrecognized/invalid ledger token, or structurally insufficient
  responsibility evidence does NOT produce a definite actor — the source continues
  to the `disposition`/`provenance` mapping (precedence 2), then action-kind
  evidence (precedence 3) only where it affirmatively identifies the actor, then
  `UNDETERMINED` (precedence 4);
- system generation of a step MUST NEVER imply `SYSTEM_DERIVABLE`; only an explicit
  `SYSTEM_ANALYSIS` ledger token (translated here) yields `SYSTEM_DERIVABLE`;
- `LEGACY_UNSPECIFIED` provenance alone remains insufficient for a definite actor;
- no ledger-vocabulary token (`OWNER_INPUT`, `SYSTEM_ANALYSIS`, `SPECIALIST_INPUT`,
  `EMPIRICAL_EVIDENCE`) may appear in the frozen `ValidationStep.responsibility`
  vocabulary, the machine package, or rendered output.

This translation is a **contract-level implementation refinement within merged
design §5** and invents no new owner ruling.

The Increment 4 `anchor_kind` already encodes the requesting disposition
(`pending_evidence` ← `evidence_requested`; `pending_specialist` ←
`specialist_requested`; `active_contradiction`), while the `assertion` anchor
COLLAPSES the dispositions `answered`, `unknown`, `deferred`, and
`provisional_assumption`. Because that collapse loses actor-relevant information,
for the `assertion` anchor the source MUST consult the underlying record's
`disposition` and `provenance` (read-only, via `engine.idea_state`; §4); it must
NOT classify from `anchor_kind` alone.

**Deterministic mapping (applied when precedence 1 does not resolve the class):**

| anchor_kind | disposition / provenance | responsibility | evidence_category |
|---|---|---|---|
| `active_contradiction` | (`reconcile_recorded_contradiction`) | `OWNER_EXECUTABLE` | `reconciliation of conflicting records` |
| `pending_evidence` | (`evidence_requested`) | `EMPIRICAL_EVIDENCE_REQUIRED` | `empirical evidence` |
| `pending_specialist` | (`specialist_requested`) | `SPECIALIST_REQUIRED` | `specialist input` |
| `assertion` | `answered` with owner-stated provenance | `OWNER_EXECUTABLE` | `owner confirmation` |
| `assertion` | `unknown` | `UNDETERMINED` | `clarifying information` |
| `assertion` | `deferred` | `UNDETERMINED` | `clarifying information` |
| `assertion` | `provisional_assumption` without sufficient actor evidence | `UNDETERMINED` | `clarifying information` |
| `assertion` | `LEGACY_UNSPECIFIED` provenance (no other affirmative signal) | `UNDETERMINED` | `clarifying information` |
| `gap` | (`address_open_gap`) | `UNDETERMINED` | `clarifying information` |

Rules:
- exactly ONE responsibility class per step (no multi-class steps in MVP-1); the
  precedence order is total and yields a single class, so no contradictory
  combination can arise;
- `OWNER_EXECUTABLE` is RESERVED for affirmatively supported owner-executable cases
  — an `answered` record with owner-stated provenance, or structurally supported
  contradiction reconciliation; it MUST NOT be assigned to `unknown`, `deferred`,
  or provisional/legacy records lacking affirmative actor evidence;
- a `LEGACY_UNSPECIFIED` provenance is INSUFFICIENT to assign a definite actor: such
  a record maps to `UNDETERMINED` unless a valid explicit `responsibility` field
  (precedence 1) or another affirmative structural signal applies; no
  `LEGACY_UNSPECIFIED` record receives `OWNER_EXECUTABLE` without such a signal;
- `SPECIALIST_REQUIRED`, `EMPIRICAL_EVIDENCE_REQUIRED`, and `SYSTEM_DERIVABLE` are
  assigned ONLY when structural evidence supports them; `SYSTEM_DERIVABLE` has NO
  default MVP-1 anchor mapping and MUST NEVER be assigned merely because the system
  generated the step (prohibition/eligibility is separate from actor class — §8);
- `gap` maps to `UNDETERMINED`: a `gap_type` carries no structural signal
  identifying an actor, and inferring one (e.g. reading `EXPERTISE_GAP_AWARENESS`
  as "specialist") would invent domain meaning and is prohibited;
- whenever responsibility resolves to `UNDETERMINED`, `evidence_category` is the
  generic `clarifying information` (never a specific test/value);
- an anchor kind or action kind outside this mapping is treated as unsupported: the
  candidate is ineligible and yields a blocked item (§8), never a guessed class.

**§7-P Auto-populated vs. explicitly supplied responsibility (precedence-1
sufficiency; resolves readiness M-1).** An `AssertionRecord.responsibility` value
that was populated automatically from default provenance or disposition logic is
not, by itself, affirmative actor evidence. For a `provisional_assumption` record,
an auto-populated `OWNER_INPUT` value MUST NOT resolve the `ValidationStep`
responsibility to `OWNER_EXECUTABLE`. Unless a separate explicit responsibility
signal was supplied by an authorized actor, the record falls through to the
`provisional_assumption` disposition rule and the `ValidationStep` responsibility is
`UNDETERMINED`. Concretely:
- explicitly supplied responsibility and internally inferred/defaulted
  responsibility are NOT equivalent evidence;
- precedence 1 (the §7-T translation) applies ONLY when the recognized ledger token
  represents an explicit, structurally sufficient responsibility signal;
- an internally defaulted `OWNER_INPUT` for a `provisional_assumption` record (for
  example, where `record_interaction` defaulted provenance to `OWNER_STATED` and
  thereby auto-populated ledger responsibility `OWNER_INPUT`) is structurally
  INSUFFICIENT for assigning a definite actor;
- `provisional_assumption` + auto-populated `OWNER_INPUT` → `UNDETERMINED`;
- `provisional_assumption` + a separately and explicitly supplied authorized
  responsibility signal → precedence 1 applies per the existing §7-T translation
  table (unchanged);
- this clarification MUST NOT alter the treatment of `answered` records with
  owner-stated provenance, where precedence 1 and the disposition rule already
  converge on `OWNER_EXECUTABLE`.
This clarification closes readiness finding M-1 and permits a later authorized test
to assert the auto-default provisional outcome as `UNDETERMINED`. It narrows only
what counts as "affirmative actor evidence"/"structurally sufficient responsibility
evidence" for precedence 1; it changes none of the five §7-T mappings, no outcome,
no test seam, no data structure, and no public API, and it grants no test or source
authority.

This mapping is a **contract-level refinement implementing design §5** (which
authorizes deriving responsibility "from the supporting record's
disposition/provenance and the Increment 4 resolving-action kind"). It introduces
no new owner ruling and reads only already-permitted committed fields (§4); it does
not widen the import boundary.

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

- **Plan identity:** MVP-1 defines no separate plan-level identifier. A
  `ValidationPlan` is identified by deterministic structural equality of its frozen
  fields. No `plan_id` field exists in MVP-1. Equivalent input states produce
  structurally equal plans, and input record order does not affect plan equality;
  step and blocked-item identifiers remain stable and non-positional (below).
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
| ≥1 eligible requirement, no ineligible ones | `PLAN` | ordered steps | `()` | ordered steps |
| ≥1 eligible requirement AND ≥1 ineligible requirement (mixed) | `PLAN` | ordered steps | ordered blocked items | steps + a separate blocked-items block |
| ≥1 requirement, all ineligible | `BLOCKED` | `()` | ordered blocked items | blocked items + generic missing text |
| a single malformed requirement among valid ones (mixed) | `PLAN` | valid steps continue | one blocked item for the malformed one | steps + blocked-items block |
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
- **Mixed state (no `PARTIAL` outcome):** when at least one requirement is eligible
  AND at least one is ineligible/malformed, the plan is `outcome = PLAN` with
  non-empty `steps` AND non-empty `blocked_items`. No `PARTIAL` outcome exists; the
  two arrays together represent the mixed state truthfully and without loss. Blocked
  items are surfaced whenever `blocked_items` is non-empty, regardless of the plan
  outcome (§15). The machine package preserves BOTH arrays (§16).
- **Unreachable non-empty/no-output state (§12-C; clarifies C-2).** Under the real
  authorized Increment 4 feed every emitted requirement is structurally addressable
  (each carries a `primary_anchor`, and for the five anchor kinds a
  `resolving_action`); therefore a NON-EMPTY real landscape that produces neither a
  step nor a blocked item is UNREACHABLE BY CONSTRUCTION in MVP-1. Crafted malformed
  tests (the §19 test seam) MUST produce a `BlockedValidationItem` for an ineligible
  requirement rather than silently dropping every requirement. The contract defines
  and authorizes NO fourth outcome; `PLAN` / `EMPTY` / `BLOCKED` remain unchanged.
  This is a clarification, not a new owner ruling.

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
- **Mixed state:** whenever `blocked_items` is non-empty — including a `PLAN`
  outcome that also carries blocked items — the section renders BOTH the actionable
  validation steps AND the blocked items in a separate, user-visible blocked-items
  subsection (or equivalent block). Blocked items render whenever `blocked_items`
  is non-empty, regardless of the plan `outcome`. The blocked-items block preserves
  the generic missing-input wording and MUST NOT imply failure, danger,
  infeasibility, invalidity, or validation completion. Raw machine tokens
  (`outcome`, `responsibility`, `confidence`, `anchor_kind`, `action_kind`,
  `requirement_id`, `step_id`, `item_id`) MUST NOT appear in the rendered mixed
  output, and Jinja autoescape remains mandatory for every blocked-item field.
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
- **Both arrays always preserved:** the package always emits both `steps` and
  `blocked_items` (each `[]` when empty), regardless of `outcome`; a mixed `PLAN`
  state (non-empty `steps` AND non-empty `blocked_items`) is represented losslessly
  by both arrays. No information is dropped or merged.
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
- plan-level identity: no `plan_id` field exists; a `ValidationPlan` is identified
  by deterministic structural equality; equivalent input states (including shuffled
  input record order) produce structurally equal plans; step and blocked-item
  identifiers remain stable and non-positional;
- deterministic, severity-neutral ordering and repeated-run stability;
- the five responsibility classes and the §7 precedence, including the §7-T
  ledger→ValidationStep translation (`OWNER_INPUT→OWNER_EXECUTABLE`,
  `SYSTEM_ANALYSIS→SYSTEM_DERIVABLE`, `SPECIALIST_INPUT→SPECIALIST_REQUIRED`,
  `EMPIRICAL_EVIDENCE→EMPIRICAL_EVIDENCE_REQUIRED`, `UNDETERMINED→UNDETERMINED`;
  a recognized ledger token is translated, never copied verbatim; an
  invalid/unknown ledger token continues the precedence, ultimately `UNDETERMINED`;
  no ledger token leaks into the frozen ValidationStep vocabulary, package, or
  rendered output): an explicit recognized `AssertionRecord.responsibility` is
  translated first; then the `disposition`/`provenance`
  mapping; `answered` + owner-stated → `OWNER_EXECUTABLE`; `unknown`, `deferred`,
  provisional-without-support, and `LEGACY_UNSPECIFIED` → `UNDETERMINED`;
  `evidence_requested` → `EMPIRICAL_EVIDENCE_REQUIRED`; `specialist_requested` →
  `SPECIALIST_REQUIRED`; `gap → UNDETERMINED`; no `LEGACY_UNSPECIFIED` record
  receives `OWNER_EXECUTABLE` without an affirmative signal; and the absence of any
  default MVP-1 `SYSTEM_DERIVABLE` mapping (never assigned because the system
  generated the step);
- evidence-category correctness (bounded, generic, never a specific test/value);
- provenance presence on every step and blocked item, and no raw-enum/identifier
  leak into rendered output;
- `confidence == UNDETERMINED` for all MVP-1 steps;
- the four-level truth model: no `result`/`supplied`/`passed`/`verified` field or
  wording anywhere;
- `EMPTY`, `PLAN`, and `BLOCKED` selection (including a constructed `BLOCKED` case)
  and malformed-per-record degradation without raising;
- the mixed state — at least one eligible requirement AND at least one
  ineligible/malformed requirement — asserting `outcome == PLAN`, non-empty `steps`,
  non-empty `blocked_items`, both arrays present in the machine package, both
  rendered (steps + a separate blocked-items block), no `PARTIAL` token, and no
  validation-completion or risk claim;
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

**Authorized pre-source test seam (resolves T-1).** The `BLOCKED`-only, mixed
`PLAN + blocked_items`, and malformed-per-record degradation states are not
reachable through the real Increment 4 feed (§12-C), so tests MAY monkeypatch the
symbol `engine.validation_plan.derive_requirement_landscape` at the Increment 5
import site to return a crafted `RequirementLandscape` containing bounded malformed
or ineligible requirements. This is a TEST SEAM ONLY: (1) it is test-only; (2) it
creates no public production API; (3) it does not authorize modifying Increment 4;
(4) it does not authorize a new source helper solely for testing; (5) it does not
authorize persistence fixtures; (6) it does not widen the runtime import boundary;
(7) it permits deterministic construction of the `BLOCKED`-only, mixed
`PLAN + blocked_items`, and malformed-per-record degradation cases; (8) crafted
requirements MUST use the committed Increment 4 payload types (`RequirementLandscape`
/ `DerivedRequirement` / `ResolvingAction` / `ProvenanceAnchor`); (9) tests MUST
monkeypatch only the Increment 5 import-site symbol and MUST NOT mutate global
repository state; and (10) production behavior remains driven by the real
`derive_requirement_landscape(state)`.

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
4. responsibility follows the §7 precedence exactly (a recognized explicit
   `AssertionRecord.responsibility` ledger token first, TRANSLATED through the §7-T
   ledger→ValidationStep table — `OWNER_INPUT→OWNER_EXECUTABLE`,
   `SYSTEM_ANALYSIS→SYSTEM_DERIVABLE`, `SPECIALIST_INPUT→SPECIALIST_REQUIRED`,
   `EMPIRICAL_EVIDENCE→EMPIRICAL_EVIDENCE_REQUIRED`, `UNDETERMINED→UNDETERMINED` —
   never copied verbatim, and no ledger-vocabulary token leaking into the frozen
   `ValidationStep.responsibility` vocabulary, the machine package, or rendered
   output; a `None`/unrecognized/invalid ledger token continues to the
   `disposition`/`provenance` mapping;
   `unknown`/`deferred`/provisional-without-support/`LEGACY_UNSPECIFIED` →
   `UNDETERMINED`; no `LEGACY_UNSPECIFIED` → `OWNER_EXECUTABLE` without an
   affirmative signal; no default `SYSTEM_DERIVABLE`), and `evidence_category`
   follows the §7 mapping (generic `clarifying information` whenever responsibility
   is `UNDETERMINED`);
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
12. the import boundary and Increment-3 non-dependency hold exactly;
13. no `plan_id` field exists; a `ValidationPlan` is identified by deterministic
    structural equality, and shuffled-input-order states produce structurally equal
    plans;
14. the mixed state yields `outcome == PLAN` with non-empty `steps` and non-empty
    `blocked_items`; the machine package contains both arrays; the rendered output
    displays both (steps + a separate blocked-items block); no `PARTIAL` token
    appears; and no validation-completion or risk claim is present;
15. the constructed `BLOCKED`-only, mixed `PLAN + blocked_items`, and
    malformed-per-record degradation cases are exercised through the §19 pre-source
    test seam (monkeypatching the Increment 5 import-site symbol
    `engine.validation_plan.derive_requirement_landscape` to return a crafted
    `RequirementLandscape`): a non-empty landscape containing an ineligible or
    malformed requirement yields a `BlockedValidationItem` for that requirement (never
    a silently dropped requirement and never a fourth outcome — §12-C), the seam
    creates no production API and does not drive production behavior, and no ledger
    token or raw identifier leaks into the rendered output.

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
| §7 responsibility | 3, 5 | §5 | **contract-level refinement implementing design §5** — responsibility precedence reads `AssertionRecord.responsibility` / `disposition` / `provenance`; the §7-T ledger→ValidationStep translation table (resolves readiness C-1) refines design §5 and invents no ruling |
| §8 eligibility/emission | 3, 9 | §5, §9 | — |
| §9 identity/provenance | 5, 6 | §6, §8 | Increment 4 stable keys; **contract-level resolution of design §8 "stable plan identity, if required" — no `plan_id`; structural equality** |
| §10 dedup/composition | 2, 6 | §8 | — |
| §11 ordering | 6 | §8 | — |
| §12 empty/blocked/mixed/malformed | 9, 4 | §9 | Increment 4 §9.10.6; **mixed-state = `PLAN` + non-empty `blocked_items` (contract-level; no `PARTIAL`)**; §12-C unreachable non-empty/no-output clarification (resolves readiness C-2) — no fourth outcome |
| §13 epistemic non-claims | 4, 10 | §7, §13 | — |
| §14 confidence | 5 | §6 | — |
| §15 rendering | 4, 6, 7, 10 | §10 | Increment 4 §7.3 |
| §16 machine package | 4, 8 | §11 | **PR56-O2 resolution**; `_s13` precedent |
| §17 backward compatibility | 7, 8 | §12 | — |
| §18 paths | 1, 7, 8 | §15 | — |
| §19 tests-first obligations | all | §16 | Increment 3/4 precedent; **authorized pre-source test seam (resolves readiness T-1)** — monkeypatch the Increment 5 import-site `derive_requirement_landscape` symbol; test-only, no production API |
| §20 source obligations | all | §17 | — |
| §21 failure conditions | 4, 6, 8, 9, 10 | §13, §14 | — |
| §22 acceptance | all | §17 | — |

Contract-level choices explicitly identified: (a) the machine-package `outcome`
token representation and the "bounded tokens allowed in package / never in rendered
output" rule (§6, §16 — resolves PR56-O2); (b) the fixed `section_14_validation_plan`
/ `_s14` names (§16); (c) the `vstep:`/`vblock:` identifier prefixes (§9); (d) the
`gap → UNDETERMINED` responsibility and the no-MVP-1-`SYSTEM_DERIVABLE` mapping
(§7); (e) the fixed `closure_condition` template (§13); (f) the responsibility
precedence and the `assertion`-by-`disposition`/`provenance` mapping — including
`unknown`/`deferred`/provisional/`LEGACY_UNSPECIFIED` → `UNDETERMINED` — as a
refinement implementing design §5 (§7); (g) the plan-level identity resolution — no
`plan_id`; deterministic structural equality — resolving design §8's "stable plan
identity, if required" (§9); (h) the mixed-state representation — `outcome = PLAN`
with non-empty `steps` and non-empty `blocked_items`, both arrays preserved in the
package and both rendered, with no `PARTIAL` outcome (§12, §15, §16); (i) the §7-T
ledger→ValidationStep responsibility translation table — a recognized explicit
`AssertionRecord.responsibility` ledger token is translated (never copied verbatim)
and no ledger-vocabulary token enters the frozen `ValidationStep` vocabulary, the
package, or rendered output — a refinement implementing design §5 that resolves
readiness finding C-1 (§7, §7-T); (j) the §19 authorized pre-source test seam —
tests MAY monkeypatch the Increment 5 import-site symbol
`engine.validation_plan.derive_requirement_landscape` to construct the
`BLOCKED`-only, mixed, and malformed-per-record cases; test-only, creates no
production API, does not drive production behavior — resolving readiness finding T-1
(§19); (k) the §12-C clarification that a non-empty real landscape producing neither
a step nor a blocked item is unreachable by construction, that crafted malformed
tests must yield a `BlockedValidationItem`, and that no fourth outcome exists —
resolving readiness finding C-2 (§12). None reopens a ruling or redesigns the merged
design.

## 24. Lifecycle boundary

After this contract is independently reviewed and (separately) merged:
- tests-first authoring STILL requires a separate, explicit owner authorization;
- source implementation STILL requires a later, separate, explicit owner
  authorization;
- staging, commit, push, PR creation, independent review, and merge remain
  SEPARATE owner authorizations for every artifact (contract, tests-first,
  source, and any roadmap synchronization);
- the roadmap is NOT automatically updated by this contract;
- the §19 authorized pre-source test seam is a TESTS-FIRST-ONLY construct: it is
  usable only inside a later, separately authorized tests-first package, grants NO
  source or production API, authorizes NO Increment 4 modification and NO new source
  helper created solely for testing, and does not itself authorize the tests-first
  package (which still requires its own separate owner authorization);
- no held lane is resumed: persistence remains `PRESERVE UNMODIFIED AND PAUSE`;
  domain-registry cleanup, compact/session-summary, and Increment 6 remain
  separately gated; no synchronization with `main` is authorized.

This contract is implementation-ready but is NOT an implementation. It fixes exact
names only where required for public schema, package compatibility, deterministic
identifiers, imports, or testable lifecycle boundaries; it deliberately leaves
private helper names and internal decomposition to source.
