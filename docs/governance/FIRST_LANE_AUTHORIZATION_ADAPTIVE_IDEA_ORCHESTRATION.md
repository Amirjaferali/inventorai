# FIRST LANE AUTHORIZATION — ADAPTIVE IDEA ORCHESTRATION

Lane: "Adaptive Idea Orchestration — Capability Disclosure, Requirement
Translation, Decision Preparation, and Bounded Recommendation"

STATUS: APPROVED AND FINAL (per-lane authorization) — NON-ACTIVATING. The lane described here remains PROPOSED and INACTIVE and activates only upon the separate committed roadmap §§4–7 activation action. This finalization records no active-lane state and authorizes no implementation.
AUTHORITY LEVEL: per-lane authorization under
docs/governance/TECHNICAL_REALIZATION_ANCHOR_COMPANION.md, the MVP_SCOPE_FREEZE
Amendment 1 carve-out, and the bounded roadmap amendment (§12).
DEPENDS ON (approval order): anchor companion → MVP_SCOPE_FREEZE Amendment 1 →
handoff contract → supported-technology/source-of-truth contract →
evidence/artifact model → roadmap amendment → this document.

ACTIVATION: approval and commit of this document alone do NOT activate the lane.
The lane activates only via the complete sequence defined by the Anchor Companion
§0 and Roadmap §12: all prerequisite authority and architecture documents in
their required non-DRAFT final status and committed; the MVP freeze carve-out
approved and committed; this per-lane authorization approved and committed; all
declared activation prerequisites satisfied; no unresolved governance or
authority blocker; and the roadmap §§4–7 update committed to record the lane as
active. Until all conditions are met, the lane remains inactive.

---

## 1. Mode, domain, and bounded invocation unit

Orchestrated Idea Mode (internal "Path N"); single domain: electronics.
**One bounded decision scope per authorized lane invocation** (governance scope
is not bound to an HTTP request, browser visit, or full session; an invocation
identifier or equivalent architectural reference may be recorded later without
implementing it now). If activated, the lane will convert plain-language input into structured
technical requirements, disclose capability, prepare one decision, and issue a
bounded recommendation when evidence is sufficient — otherwise remaining
truthfully unresolved.

Representative bounded decision: the bicycle-tail-light braking-detection method.

## 2. Required user-visible outcomes

1. Capability disclosure carrying both `support_status` and
   `authorization_status` (scoped per capability/operation/technology+version/
   lane) — the lane may state it can perform a capability now only when it is both
   supported and `authorized_for_execution` for the exact
   technology/version/capability/operation record within this lane (see Supported
   Technology and Source-of-Truth Contract §8.1) and its source/tool prerequisites
   are satisfied. Absence of a verified support record never defaults to supported;
   `support_status` = `stale`, `unknown`, or `unsupported` must not be presented as
   supported; `partially_supported` must disclose its exact supported/unsupported
   boundary and is not full support; `authorization_status` = `blocked` or
   `not_authorized` is not available for the affected operation.
2. Plain-language, task-appropriate requirement capture (questions that do not
   require unsupported specialist knowledge; the participant may be technically
   knowledgeable yet use this mode).
3. A versioned decision-readiness artifact (§4).

Plain-language questions are outcome-oriented, e.g.: "Can the device physically
connect to the brake lever?"; "Must it work without wiring to the bike
controls?"; "Should it work on different bicycle types?"; "Is avoiding false
braking alerts more important than maximum sensitivity?"; "Will it be used on
rough roads?"; "Is simple installation important?"

## 3. Acceptance example (must be reproduced behaviourally)

| Plain-language input | Translation (+ constraint_strength) | Consequence |
|---|---|---|
| "I don't want wires to the brake lever." | installation_constraint = no_physical_brake_control_connection; classify strength (preference / soft_constraint / mandatory_constraint) and confirm | only a CONFIRMED mandatory_constraint eliminates the wired brake-lever switch (option_status=eliminated, disposition_reason=requirement_conflict); a preference/soft_constraint only qualifies or defers it |
| "Often used on rough roads." | environmental_constraint = high_vibration_and_road_shock | accelerometer method stays a candidate but gains false-positive/calibration risk; it cannot reach technically_selected (which this lane may not issue — see §7) |

Artifact outcome: depending on confirmed constraint strength, the wired
brake-lever switch is eliminated (only on confirmed mandatory constraint) or
qualified; accelerometer = `decision_status=recommended`,
`conditions=[calibration_required, physical_test_required]`; wheel-speed =
candidate only if mounting/sensing inputs available; decision = unresolved or
conditionally recommended; next required evidence = installation constraints,
acceptable false-positive rate, physical calibration/test result. Such
calibration/physical-test evidence is **externally produced** (no calibration,
bench test, or field test is performed by this lane), **returned later through an
authorized re-entry path**, and recorded with provenance, method, version, and
verification status.

## 4. First-lane artifact: `adaptive-decision-readiness-v1`

Mode-neutral, shared-project; does NOT imply a separate Path-N schema or artifact
store. Fields (aligned with the evidence/artifact model dimensions): artifact_id;
current_session_id; future_project_identity_ref (FUT); capability_disclosure
{support_status, authorization_status}; decision_question; plain_language_answers;
translated_requirements; constraints{constraint_strength}; candidate_alternatives[]
with per-option {option_status, disposition_reason, evidence_reference};
evidence_per_alternative; missing_evidence; readiness_status (`not_ready` ·
`ready_for_decision_preparation` · `ready_for_bounded_technical_realization`, per
the Handoff Contract §3); blocking_reasons[]; risks;
safety_considerations; decision_status; currency_status; validity_status;
artifact_origin_status; verification_stage; verification_outcome; conditions[]
(when recommended); confirmation_records[]; approval_requirements[];
approval_records[]; approval_record_references[]; next_required_input;
downstream_dependency; provenance;
artifact_version.

`approval_requirements[]` records future-compatible approval requirements. The
first lane may record requirements but MUST NOT create or satisfy technical,
safety, regulatory, or freeze approval; `approval_records[]` are populated only
by separately authorized authorities. `confirmation_records[]` capture
participant confirmation (with type, subject/reference, confirmer role, timestamp,
scope, revocability, approval effect) — a participant confirmation is NOT a
technical, safety, regulatory, or freeze approval. The first lane need not
implement unused future fields, but the schema must not contradict the governing
evidence/artifact model and must not duplicate incompatible vocabularies.

Field availability classification (each field is exactly one of:
`required_in_first_lane`; `optional_if_applicable`;
`future_compatible_not_implemented`; `prohibited_to_populate_by_this_lane`):
- `future_project_identity_ref` is `future_compatible_not_implemented`;
- `approval_records[]` is `prohibited_to_populate_by_this_lane`: the first lane
  must not create, alter, or populate `approval_records[]`; it may carry
  `approval_record_references[]` supplied by separately authorized authorities, if
  applicable, and a reference to an external approval record is not an approval
  created by the lane;
- `approval_record_references[]` is `optional_if_applicable`: it carries
  references only to approval records supplied by separately authorized
  authorities; it does not contain an approval created by the first lane; it does
  not permit the first lane to create, alter, or populate the referenced
  `approval_records[]`; it must preserve the authority reference, approval-record
  identifier/version, scope, and provenance required to resolve the referenced
  record; and it is not a substitute for the authoritative approval record itself;
- `verification_stage` and `verification_outcome` are `optional_if_applicable`,
  only for recording externally produced evidence returned through an authorized
  re-entry path, unless a separately authorized verification capability later
  exists; recording an externally returned stage/outcome does not imply the lane
  performed the verification, and the lane does not generate external verification
  evidence;
- `downstream_dependency` is `future_compatible_not_implemented`.
Future-compatible fields do not become implementation scope, and the schema must
not imply implementation authority.

## 5. Acceptance criteria (measurable; tests authored separately)

The lane is accepted only if it: asks only plain-language, task-appropriate
questions (zero engineering-parameter demands); converts answers into ≥1
structured requirement the participant did not phrase; surfaces ≥1 piece of
information the participant did not know to request; emits an explicit
capability-disclosure map (support_status + authorization_status); produces a
reusable versioned artifact with provenance; is not reducible to restating input
(adds alternatives, translation, disposition, disclosure); advances the idea (a
`recommended` with conditions, or a truthful unresolved state via
readiness/blocking structures); is reproducible under controlled context (same
structured inputs, rule/schema version, registry snapshot, model/tool version,
configuration, recorded provenance — deterministic governance transforms, schema
validation, status assignment, and prohibition rules reproduce exactly;
model-generated explanatory language may vary, but materially equivalent
conclusions, constraints, blockers, and evidence references remain reviewable and
attributable); overstates no evidence; remains bounded to electronics.

Grounding: any structured requirement or item of information added beyond the
participant's exact phrasing must be grounded in authorized deterministic rules,
verified sources, or explicit bounded inference with recorded provenance. The lane
must not invent additional requirements or information merely to satisfy these
acceptance metrics.

## 6. Structured stop effects (differentiated; not one generic stop)

Each stop records: `stop_effect`; `blocking_reason`; `affected_scope`;
`next_allowed_action`; `resume_condition`. A stop affecting one operation must NOT
stop the whole session or lane unless the governing rule requires it.
- missing input → `stop_effect=decision_pause`: pause the affected decision,
  continue plain-language elicitation;
- safety conflict → `stop_effect=hard_stop_for_affected_action`: hard-stop the
  unsafe affected action while allowing explanation and safe alternatives;
- authority missing → block the affected execution operation while allowing
  capability disclosure and explanation;
- unresolved source conflict → prevent recommendation or selection while allowing
  evidence collection.

## 7. Bounded decision-state boundary (binding)

The general architecture defines `technically_selected` and `frozen`, but **this
first lane MUST NOT issue** `technically_selected`, `frozen`, final technical
selection, or any downstream baseline status, and MUST NOT perform physical
calibration, bench testing, or field testing. The lane may issue only the bounded
outcomes it can evidence: `candidate`; `recommended` (with structured
`conditions[]`); `owner_preferred` (among currently eligible, non-disqualified,
non-blocked alternatives — recording preference, not technical validity, and not
a final recommendation/selection/baseline); and unresolved (via readiness_status
/ blocking_reasons[]). `technically_selected` and `frozen` are downstream target
states requiring separately authorized capabilities, evidence gates, and
approvals. The lane may only reference externally produced evidence returned
through an authorized re-entry path.

The lane MUST NOT produce: part numbers, final component selection, calculations,
BOM, wiring, pin map, firmware, simulation, or any tested/demonstrated claim.

## 8. Explicit non-authorizations

This authorization authorizes no code until separately approved and committed. It does
not authorize generation (firmware/BOM/wiring/calculation/simulation/component
selection), multi-domain orchestration, accounts/collaboration, artifact-store
implementation, persistence changes, Path T, or any hold/closed-state change.

## 9. Preserved states

R2=HELD · FORM T=BLOCKED · S-6=UNCLASSIFIED · AA-3/AA-4/AA-5=BLOCKED ·
Phase 5/6=UNAUTHORIZED · ILT-002 evidence collection=NOT AUTHORIZED ·
Path T=BLOCKED · Phase 4=CLOSED · Gate 8=CLOSED · runtime_integrated=TRUE.
