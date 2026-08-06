# INVENTOR-STATED SAFETY SIGNALS — INCREMENT CONTRACT DRAFT (POST-PR #119)

## 0. Status

`INCREMENT CONTRACT DRAFT ONLY — INVENTOR-STATED SAFETY SIGNALS — ADDITIVE
ADVISORY SURFACE — NO IMPLEMENTATION AUTHORIZED`

This document is a **contract draft only**. It defines the bounded scope, the
non-goals, the recommended implementation boundary, the candidate output model,
the detection boundary, the wording guardrails, the required tests, and the
regression requirements for a **future, separately-authorized** first increment
of the Safety-Aware Criticality & Inventor-Stated Risk Derivation candidate
(admitted by PR #118, roadmap-synchronized by PR #119). It is **not**
implementation authorization. No code, test, schema, UI, template, runtime,
session, scoring, maturity, readiness, persistence, or report change is
authorized or begun by this document. Implementation may begin only after this
contract itself passes independent review and an owner-gated true merge, and then
only under a **separate** owner implementation authorization (§12).

This first increment is **not** a rewrite of criticality, **not** a scoring
change, and **not** a risk-engine replacement. It is an **additive read-only
derivation/display layer** that elevates inventor-stated safety-relevant
assumptions, failure conditions, and consequences that are **already present** in
stored answers.

File-creation record (per `CLAUDE.md` File Creation Rules):
- File path: `docs/governance/SAFETY_AWARE_INVENTOR_STATED_SAFETY_SIGNALS_INCREMENT_CONTRACT.md`
- Purpose: governance contract draft defining a future additive, read-only
  "Inventor-Stated Safety Signals" increment's exact scope, boundaries, output
  model, detection boundary, tests, and regression requirements.
- Input contract: the PR #118 Safety-Aware scope decision
  (`SAFETY_AWARE_CRITICALITY_INVENTOR_STATED_RISK_DERIVATION_SCOPE_DECISION_POST_PR117.md`),
  the completed read-only technical review, and the merged PR #116–#119 record.
- Output contract: a single bounded increment-contract draft (§3–§12) and its
  final classification (§13); nothing executable, nothing activating.
- Prohibited behaviors: this file must never be read as implementation
  authorization, scoring authorization, an owner implementation authorization, a
  persistence/schema authorization, or roadmap content; it authorizes no code,
  test, or behavior change; it starts no implementation.

Authoritative context (evidence-locked at authorship):
- Repository: `Amirjaferali/inventorai`
- Authoritative branch: `feature/atomic-json-session-persistence`
- Authoritative tip: `1531098c506a68c63a0a25c953f7f775c23a6bdc` (PR #119 merge)
- Latest merged PR: #119
- Current official state remains: `DEMO_READY_WITH_LIMITATIONS`
- The MVP remains electronics/electrical-only (`MVP_SCOPE_FREEZE.md`).
- `main` remains separate and unchanged
  (`0e89e4636399760965c9ff8086b465c90dbadf8e`); no `main` sync occurred or is
  authorized.
- The frozen persistence worktree remains paused and untouched
  (`aec9cf6409efc18e125b6745762002f59e529654`); the quarantined scratch branch
  remains untouched (`02586747c902d5e1ebb78adde54ddd4ecd1c174a`).

---

## 1. Background

- **PR #118** admitted Safety-Aware Criticality & Inventor-Stated Risk Derivation
  as a **future candidate only** (docs-only scope decision; no implementation
  authorized).
- **PR #119** synchronized the roadmap recording PR #116/#117/#118.
- The completed **read-only technical review** found:
  - `engine/requirement_landscape.py::derive_requirement_landscape` hardcodes
    every requirement `criticality = UNDETERMINED` with
    `criticality_authority = system-derived` and returns **zero grounded risks**
    (`RequirementLandscape.risks = ()`) — this is the frozen Increment-4 MVP-1
    behavior;
  - Section 6 risks are generated in `engine/deliverable_assembler.py::_s6` from
    **maturity level, overall evidence class (ASSERTED/REASONED), and open gaps**
    — not from answer semantics;
  - inventor-stated safety text currently appears only as raw/stored answer
    content, or as Section 5 assumptions / `acknowledged_unknowns` (Section 8),
    but is **never elevated** into a visible safety/risk/criticality advisory
    surface;
  - the observed live-demo issue — a user-stated electrical **insulation** safety
    condition that was not elevated as a visible safety signal — occurs because
    **no current code path lifts inventor-stated safety-critical content into a
    clear safety signal**.

---

## 2. Problem statement

Inventor-stated safety-critical assumptions can be **buried in narrative
sections**. The report can show `Criticality: UNDETERMINED` even when the
inventor explicitly stated a safety-critical failure condition (e.g. "if
insulation cannot be safely achieved, the device should not be used because it
could create a safety risk"). This first increment must **improve visibility** of
such inventor-stated signals **without** making any final safety, compliance,
certification, engineering, patent, or legal claim.

---

## 3. Non-goals

This contract, and any implementation it may later authorize, does NOT authorize
and must NOT perform:

- any scoring change;
- any maturity change;
- any readiness change (`engine/derived_readiness.py` behavior unchanged);
- any persistence/session schema change;
- any domain expansion (electronics/electrical-only preserved);
- any Guided Answer Co-Authoring work;
- any Answer Clarification / Improve Wording activation;
- any compliance / certification / legal / patent advice;
- any final claim that an invention is safe or unsafe;
- any change to the Increment-4 `criticality` field behavior
  (`derive_requirement_landscape` and its `criticality` /
  `criticality_authority` / `criticality_rationale` outputs unchanged);
- any population of `RequirementLandscape.risks` (it remains `()`);
- any replacement of, or change to, the Section 6 risk generator (`_s6`);
- any modification of thresholds, the generic-verb trap, causal tokens, evidence
  classification, or gap-closure logic
  (`assess_response` / `integrate_response` / `evaluate_transition` unchanged);
- any `main` synchronization;
- any modification of the frozen persistence worktree or use of the quarantined
  scratch branch;
- any implementation — this contract draft authorizes NO implementation.

---

## 4. Recommended implementation boundary

If, and only if, this contract is independently reviewed and owner-merged, and a
**separate** owner implementation authorization is then issued (§12), the future
increment is bounded to:

- A **new pure helper/module**, likely `engine/safety_signal.py`.
- **Pure, deterministic derivation** from existing `IdeaState` content;
  **read-only and non-mutating** (never rewrites, stores, or improves the
  inventor's answer).
- **Imports only** safe local state/domain structures (e.g. `engine.idea_state`
  and, if needed, read-only domain context) — no scoring, persistence, web, or
  Increment-3 dependency; no engine mutation.
- Derives **only** from **inventor-stated or clearly inventor-grounded content**
  already recorded (answers/evidence, Section 5 assumptions,
  `acknowledged_unknowns`).
- Outputs an **additive advisory structure** (candidate model, §5).
- Adds **one high-visibility deliverable surface/section** for "Inventor-Stated
  Safety Signals" (mirroring the additive `_s13`/`_s14` discipline — a new
  additive section that changes no prior section and adds no new stored truth).
- **Optionally** adds validation-plan wording stating that **independent
  validation is required** for any surfaced safety signal.
- **Does not change stored answers**, the Increment-4 `criticality` field,
  `RequirementLandscape.risks`, or the Section 6 risk generator.

The increment's only permitted effect is a new, clearly-labelled advisory
**display/derivation** over content the system already recorded.

---

## 5. Candidate output model (conceptual, not implemented schema)

Candidate fields for the additive advisory structure — conceptual only; a future
implementation authorization would fix the exact shape. These describe a
**runtime/deliverable** structure and do **not** imply any persistence/session
schema change unless separately authorized:

- `signal_id`
- `source`
- `provenance = inventor_stated`
- `safety_subject`
- `failure_condition`
- `possible_consequence`
- `domain_context`
- `validation_status = requires_independent_validation`
- `display_label`
- `caution_text`

Clarification: these are **candidate runtime/deliverable structures only**. They
do not add a persisted `IdeaState` field; the inventor-stated content they derive
from is already stored. Any change to the persisted session schema is out of
scope for this first increment and would require separate authorization. (Note:
adding a new **deliverable output section** affects the deliverable JSON output
shape / canonical-section contract; the future Increment Contract implementation
must treat that as an explicit, tested additive change and must not alter the
persisted session schema.)

---

## 6. Detection boundary

Detection must be **conservative** and based on a **combination** of cues, not
any single one:

- an explicit **failure or invalid-use condition** stated by the inventor;
- a **safety-relevant subject**;
- a **consequence cue** (harm, risk, unsafe use, missed/late warning, etc.);
- **electronics/electrical context**;
- **inventor-stated provenance**.

**Bare keyword matching is explicitly rejected as sufficient.** A term such as
"safety" alone must never trigger a signal; the failure/invalid-use condition,
the consequence cue, and the safety-relevant subject must co-occur, with
conservative negation handling.

Examples (illustrative; a future contract fixes the exact bounded cue set):

Positive (should surface a signal):
- "If insulation cannot be safely achieved inside the plug housing, the device
  should not be used because it could create a safety risk."

Negative (must NOT surface a signal):
- "Safety is important."
- "This improves safety."
- "There are no safety concerns."
- A generic, non-electrical business risk statement.

---

## 7. Required wording guardrails

The future feature **may** say:
- "Inventor-stated safety signal"
- "Requires independent validation"
- "Potential safety-critical assumption"
- "Failure condition stated by inventor"

The future feature **must NOT** say:
- "The invention is unsafe."
- "The invention is safe."
- "Certified."
- "Compliant."
- "Approved."
- "Patent-ready."
- "Engineering-validated."

Every surfaced signal must carry `provenance = inventor_stated` and
`validation_status = requires_independent_validation`, and must never present a
final safety determination.

---

## 8. Required tests

Proposed test files:
- `tests/test_safety_signal.py` (the new pure module);
- additive deliverable/report tests (added to, or alongside, existing deliverable
  tests) if the existing structure supports them;
- validation-plan wording tests if the validation-plan note is included.

Required test categories:
1. **Positive** — an inventor-stated electrical safety condition surfaces a
   signal (with provenance and required-independent-validation status).
2. **Negative** — a non-safety statement surfaces no signal.
3. **Negation guard** — "safety is not a concern" / "no safety concerns" surfaces
   no signal.
4. **Non-electrical generic risk** — does not over-trigger.
5. **No scoring change regression** — `assess_response` results unchanged (locked
   suites).
6. **No maturity/readiness change regression** — maturity transitions and
   `derive_readiness` unchanged.
7. **Existing Section 6 risks unchanged** — `_s6` output identical for the same
   state.
8. **Existing Section 13 criticality unchanged** — `derive_requirement_landscape`
   criticality field and `risks=()` identical.
9. **Report includes the safety signal with provenance** — the additive section
   renders the signal, source, and independent-validation status.
10. **Validation plan includes independent-validation wording** (if that note is
    included).
11. **No persistence/schema mutation** — the persisted `IdeaState` shape is
    unchanged after derivation/rendering.

---

## 9. Regression requirements

A future implementation authorized under this contract MUST prove:
- the **locked scoring suites** (`tests/test_assess_response_replay.py`,
  `tests/test_assess_response_adversarial.py`) remain unchanged;
- **maturity/readiness transitions** remain unchanged;
- **`derive_requirement_landscape` behavior** remains unchanged (criticality
  field and empty risk register bit-identical);
- **Section 6 risk behavior** (`_s6`) remains unchanged;
- the **official state** remains `DEMO_READY_WITH_LIMITATIONS`;
- the **MVP** remains electronics/electrical-only;
- the full suite shows **zero new failures** beyond the known pre-existing
  `tests/test_domain_registry.py` baseline.

---

## 10. Governance decision (path selection)

This contract **explicitly chooses the additive advisory-surface path** for the
first increment: a new pure `engine/safety_signal.py` derivation plus one
additive high-visibility deliverable section (and an optional validation-plan
note), leaving the Increment-4 `criticality` field and `RequirementLandscape.risks`
untouched.

This contract **explicitly rejects an Increment-4 criticality-field amendment**
for this first increment. Overwriting the frozen `criticality` field (e.g.
writing `ESSENTIAL — SAFETY`) or populating `RequirementLandscape.risks` would
breach the merged Increment-4 contract
(`INCREMENT_4_AUTHORITY_RULINGS.md` / `INCREMENT_4_DESIGN.md` /
`INCREMENT_4_IMPLEMENTATION_CONTRACT.md`) and is out of scope here.

A **future, later** increment **could** revisit criticality-field semantics
(e.g. a safety-aware criticality category on the requirement itself) — but **only
through a separate, owner-gated Increment-4 governance amendment**, never as a
side effect of this first additive increment.

---

## 11. Risks

A future review/implementation must address at least:
- **Scoring contamination** — any leak of the derivation into
  `assess_response` / gap-closure / maturity; mitigated by §3/§4 (separate pure
  module, engine untouched) and §9 regression proof.
- **Report overclaiming** — presenting a signal as a final safety determination;
  mitigated by §7 guardrails.
- **Compliance/certification implication** — drift into legal/patent/engineering
  approval; mitigated by §3/§7 non-goals and forbidden wording.
- **Keyword false positives** — bare-keyword triggering; mitigated by §6
  combination-cue detection.
- **Negation fragility** — "no safety concerns" false-firing; mitigated by §6
  negation handling and §8 negation-guard tests.
- **Hiding safety signals in long text** — the very problem; mitigated by a
  distinct, high-visibility, ordered deliverable surface (§4).
- **Accidental coupling to Guided Answer Co-Authoring** — kept separate (§3).
- **Accidental schema/persistence expansion** — mitigated by §4/§5 (read-only
  derivation over already-stored content; no persisted field added) and §8/§9
  no-mutation tests.
- **Breach of the Increment-4 contract if criticality is overwritten** —
  mitigated by §10 (additive path chosen; criticality-field amendment rejected).

---

## 12. Implementation readiness

Based on the read-only review, the first increment **appears feasible without any
persistence/session schema change, and without any scoring, maturity, or
readiness change** — it is a purely additive, read-only derivation plus an
additive deliverable surface over already-stored inventor-stated content. (One
explicit nuance to resolve at implementation time: adding a new **deliverable
output section** is an additive change to the deliverable JSON output shape /
canonical-section contract; it must be treated as a tested additive change and
must not alter the persisted session schema.)

**Implementation is NOT authorized by this contract draft PR.** Implementation
may begin only if the owner later authorizes it, after this contract is
independently reviewed and owner-merged, under a separate implementation
authorization. Any subsequent work must proceed, in order, through: this
Increment Contract (draft) → independent review → owner-gated true merge of the
contract → a separate owner implementation authorization → implementation →
tests → independent review → owner-gated true merge → separate manual demo
verification → separate roadmap synchronization.

Roadmap handling: a roadmap entry recording this contract is **proposed only** as
a **later, separate, owner-gated** step; this document changes no roadmap file.

---

## 13. Final classification

`INCREMENT CONTRACT DRAFT ONLY — INVENTOR-STATED SAFETY SIGNALS — ADDITIVE
ADVISORY SURFACE — NO IMPLEMENTATION AUTHORIZED`
