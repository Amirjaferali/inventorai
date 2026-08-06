# SHARED EPISTEMIC-FOUNDATION DESIGN DECISION

Status:
APPROVED ARCHITECTURAL DESIGN DECISION
— IMPLEMENTATION NOT AUTHORIZED
— INCREMENT-SPECIFIC AUTHORIZATION REQUIRED

Decision date:
2026-06-28

Decision state:
APPROVED ARCHITECTURAL DIRECTION — NOT IMPLEMENTED

Companion to:
`docs/governance/INVENTORAI_PRODUCT_VALUE_CORRECTION_PLAN.md`

Authoritative base:
committed repository at `b0e557cd5494f52e8382ac7694f253538e6781e9`
(the PR #25 true-merge of `origin/feature/atomic-json-session-persistence`;
ordered parents `91eff27f9342ee865a449ab8cd5127f2c57006be` then
`fb02ec7ab2dc36fc19660845a1d93a731fbbcb96`).

## 1. Purpose and authority

This document records the owner-approved architectural direction for the shared
epistemic foundation underlying Product-Value Correction Increments 1 and 2. It is
a DESIGN DECISION RECORD, not implementation authority. It authorizes no code,
test, template, persistence, runtime, benchmark, scoring, gate, maturity, gap-
closure, or deliverable change. It does not amend any anchor, ADR, roadmap, policy,
or scope-freeze document. Each increment named here requires its own separate,
explicit, repository-grounded owner authorization for its exact scope before any
implementation-related repository write or any repository change that
relies on this decision.

## 2. Problem being corrected

The accepted owner-observed validation findings
(`docs/validation/OWNER_OBSERVED_PRODUCT_VALIDATION_FINDINGS_2026-06-27.md`)
established, against committed code, that the general idea-development "session"
lane:

- demands specialist engineering values a non-specialist owner cannot supply, with
  no structured way to defer, record an assumption, or route to a specialist
  (Finding A);
- collapses answered / described / assumed / reasoned content into a single
  "resolved" state, and closes gaps on reasoned **text** alone because the
  `DEMONSTRATED` verification tier is deferred in the MVP (Finding B);
- reports a confident `PROCEED` verdict and `Gaps total/open/resolved` counts that
  overstate the true epistemic state (Findings B, E12).

The defining diagnosis is governance-to-runtime conformance: the governing
principles already exist in committed governance; the runtime does not yet conform.
The root structural cause is that the session lane models only one axis — evidence
**quality** (`ASSERTED`/`REASONED`/`DEMONSTRATED`, ADR-003) — and overloads it to
stand in for source, responsibility, validation, and readiness, which are in fact
independent concepts.

## 3. Approved architecture direction

APPROVED:

> Additive orthogonal epistemic metadata for the session lane, with structured
> owner actions and derived stage readiness.

The session lane gains independent, additive metadata axes (provenance,
responsibility, interaction disposition, and — when Increment 2 is authorized —
validation status and evidence relationships), each defaulted for backward
compatibility. Stage readiness, blocking effect, and deliverable verdict are
DERIVED from those axes rather than stored, so no stale stored judgment can
contradict current evidence. The approach is informed by — but does not blindly
copy — the existing FDC-001/FDC-002 decision-workspace model, which already
separates claim class, provenance, verification status, and a derived readiness
status.

## 4. Rejected alternatives

The following are explicitly rejected for the current MVP design boundary:

- extending `EvidenceQuality` (the ADR-003 ladder) into one large linear enum —
  this re-encodes the false-single-ladder defect by overloading quality with
  unrelated concepts;
- treating `CLOSED` as universal technical truth. In the future epistemic
  contract, `CLOSED` must not be interpreted as universal technical truth. It may
  remain meaningful for owner-authoritative descriptive gaps, while technical,
  safety, compliance, and performance readiness must be derived from their required
  validation conditions. This future-contract limitation is not claimed to be
  implemented in the current runtime;
- introducing a standalone epistemic ledger at the current MVP stage — deferred as
  a possible future evolution, not adopted now;
- adding `schema_version` before durable session persistence exists — the session
  `IdeaState` is not serialized to disk today, so a version field has no consumer
  yet;
- changing scoring, maturity, gates, gap closure, benchmark, golden fixtures, or
  verdict behavior in Increment 1.

## 5. Final terminology

These vocabularies are the approved design vocabulary. They are NOT implemented.
The four axes are orthogonal and must not be merged into one enum.

### 5.1 Provenance — source of a content/evidence record

- `OWNER_STATED`
- `SYSTEM_INFERRED`
- `EXPERT_SUPPLIED`
- `EXTERNAL_EVIDENCE`
- `LEGACY_UNSPECIFIED`  (default; backward-compatible value for pre-existing data)

### 5.2 Responsibility — the required source or contributor for resolving or advancing a question/gap

- `OWNER_INPUT`
- `SYSTEM_ANALYSIS`
- `SPECIALIST_INPUT`
- `EMPIRICAL_EVIDENCE`
- `UNDETERMINED`  (default; must never auto-promote — see Increment 1B)

Responsibility is an attribute of the question/gap, not of evidence quality.

Responsibility identifies the required contribution source for a question or
gap. It does not describe evidence quality or guarantee resolution.

### 5.3 Interaction disposition — structured owner action on a question/gap

- `ANSWERED`
- `UNKNOWN`
- `DEFERRED`
- `PROVISIONAL_ASSUMPTION`
- `SPECIALIST_REQUESTED`
- `EVIDENCE_REQUESTED`

These are structured actions, recorded explicitly. They must never be inferred
from free text alone.

### 5.4 Validation status — validation tier of an evidence record (Increment 2)

- `UNVALIDATED`  (default)
- `SPECIALIST_REVIEWED`
- `EMPIRICALLY_DEMONSTRATED`
- `INDEPENDENTLY_VERIFIED`

Contradiction and supersession are RELATIONSHIPS between evidence records (append-
only edges referencing another record's id), not values of this enum.

### 5.5 ADR-003 evidence quality — unchanged and separate

- `ASSERTED`
- `REASONED`
- `DEMONSTRATED`

These remain the reasoning-quality axis defined by ADR-003. They must not be
overloaded with provenance, responsibility, validation authority, or stage
readiness. `DEMONSTRATED` remains deferred-not-deleted per ADR-003; the validation
axis (5.4) deliberately uses distinct names (`EMPIRICALLY_DEMONSTRATED`) to avoid
overloading the ADR-003 token.

## 6. Stored versus derived contract

STORE only historical or explicitly asserted facts:

- responsibility (per question/gap);
- provenance (per content/evidence record);
- structured interaction disposition (append-only);
- validation status — only when Increment 2 is authorized;
- contradiction / supersession relationships — only when Increment 2 is authorized.

DERIVE rather than store (recomputed from current inputs each time):

- stage readiness;
- blocking effect;
- deliverable verdict;
- current adequacy of evidence.

`CAPTURED` is defined precisely as:

> information exists in the record, without implying adequacy, verification,
> readiness, or closure.

`CAPTURED` is an informational record condition, not proof of stage readiness.
A gap may be captured and still be blocking or not ready.

Blocking effect must NOT be defined from responsibility alone. It is eventually
derived (in Increment 2, not now) from at least:

- gap category;
- lifecycle stage;
- responsibility;
- validation requirement;
- criticality;
- the current transition rule.

This derivation is not implemented in this decision and is not authorized here.

## 7. Execution split

Each item below is FUTURE SCOPE and requires its own separate authorization.

### Increment 1A — Structured owner actions

- add the structured owner actions of 5.3;
- ensure only `ANSWERED` enters the existing assessment path;
- ensure `UNKNOWN`, `DEFERRED`, `PROVISIONAL_ASSUMPTION`, `SPECIALIST_REQUESTED`,
  and `EVIDENCE_REQUESTED` must not: score; close a gap; increase maturity; or
  satisfy a transition gate;
- but these actions may allow the user journey to continue to another eligible
  question or stage-appropriate interaction, without being treated as an answer or
  gap resolution. Journey navigation is distinct from maturity/gate advancement:
  these actions perform no maturity or gate advancement, while still permitting the
  journey to move on;
- preserve all existing gates, maturity, gap closure, and deliverable behavior.

### Increment 1B — Responsibility metadata

- add question/gap responsibility (5.2);
- default to `UNDETERMINED`;
- add clarification-first routing (attempt plain-language translation / "what
  information would you need?" before escalating);
- do not auto-promote every unknown to specialist-required.

### Increment 1C — Provenance metadata (optional until proven necessary)

- add provenance (5.1) without changing truth or readiness;
- adding the enum authorizes no system-inference behavior.

### Increment 2 — Truthful readiness, closure, and deliverable semantics

- validation status (5.4);
- contradiction / supersession relationships;
- derived stage readiness;
- truthful gap and deliverable reporting;
- revision of `PROCEED`, resolved counts, and `No unresolved items`;
- any closure or gate semantics.

Increment 2 changes closure/scoring/verdict surfaces and therefore requires a
parity proof (behavior preservation plus WPS-001 / golden / replay parity) per
the CLAUDE.md refactor-governance contract, and may require a separate scope-freeze
decision, before any authorization.

## 8. Compatibility constraints

- All new fields are additive and MUST carry defaults, so existing keyword
  construction and dataclass round-trips (`Gap(**legacy)`, `Evidence(**e)`) keep
  working; `LEGACY_UNSPECIFIED` and `UNDETERMINED` are the backward-compatible
  defaults.
- The session `IdeaState` is held in memory and is not serialized to disk today;
  the only persisted JSON is the fixed ILT-002 transcript record, which does not
  include gaps/evidence and is therefore unaffected by these axes.
- No `schema_version` is introduced now; versioning is deferred until durable
  session persistence exists.
- Increment 1 must not modify the bodies of the deterministic gate functions
  (`assess_response`, `integrate_response`, `evaluate_transition`) and must not
  introduce any dependence on the AI advisor (WPS-001 INV-007).
- The forward-only gap lifecycle (WPS-001 INV-004) is preserved: stored gap status
  is never moved backward; truth that can decrease lives in DERIVED readiness, not
  in stored gap status.
- Golden fixtures, replay, benchmark, and `score_case()` semantics are unchanged in
  Increment 1.

## 9. Protected states

This decision changes nothing and preserves:

- persistence `PRESERVE UNMODIFIED AND PAUSE` (frozen worktree `/home/user/inventorai`
  at `aec9cf6…`, seven paused paths, untouched);
- benchmark `NOT RUN`;
- final technical selection `NONE`;
- R2 HELD; FORM T BLOCKED; S-6 UNCLASSIFIED; AA-3/AA-4/AA-5 BLOCKED;
  Phase 5/6 UNAUTHORIZED;
- the currently committed FDC-001/FDC-002 governance states and recorded closure
  classifications; this document neither reopens nor reinterprets them.

This decision does not amend ADR-003 evidence-quality semantics or any WPS-001
invariant. Any future identified conflict requires separate evidence, review,
and explicit authorization; no implicit override is permitted.

## 10. Explicit non-authorization

This document authorizes no implementation. It does not begin Increment 1A, 1B, 1C,
or Increment 2; it does not change code, tests, fixtures, templates, persistence,
benchmark, scoring, gates, maturity, gap closure, or deliverable behavior; it does
not amend any anchor, ADR, roadmap, policy, or scope-freeze document; it does not
run a benchmark or make a final technical selection. The terminology and contracts
recorded here are design decisions only. Any implementation requires separate,
explicit, repository-grounded owner authorization for that exact scope.
