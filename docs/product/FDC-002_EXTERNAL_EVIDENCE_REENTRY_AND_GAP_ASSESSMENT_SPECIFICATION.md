# FDC-002 — External Evidence Re-Entry and Gap Assessment (Implementation Specification)

STATUS: REVIEW DRAFT — IMPLEMENTATION NOT AUTHORIZED
EXECUTION_AUTHORITY: NONE
PRODUCT_LANE: ADAPTIVE IDEA ORCHESTRATION
CONTENT_SCOPE: FDC-001 BICYCLE BRAKING-DETECTION DECISION ONLY
PERSISTENCE_STATUS: PRESERVE UNMODIFIED AND PAUSE
BENCHMARK_STATUS: NOT RUN
FINAL_TECHNICAL_SELECTION: NONE

This is a planning specification only. It authorizes no code, test, or working-tree
change beyond this single document. A later, separate, explicit, repository-grounded
owner implementation authorization (naming exact files and a named acceptance-test
set) is required before any implementation begins.

---

## 1. Status and authority

1. FDC-002 implementation is **not authorized** by this specification itself.
2. The current lane authorization
   (`docs/governance/FIRST_LANE_AUTHORIZATION_ADAPTIVE_IDEA_ORCHESTRATION.md` §3,
   §4, §7) **already permits recording externally-produced evidence returned
   through an authorized re-entry path**, recorded with provenance, method,
   version, and verification status, where the lane performs and generates no
   verification.
3. **No anchor amendment is required.** Product/epistemic anchors
   (`DUAL_PATH_PRODUCT_ANCHOR.md`, `ILT-002_GOVERNANCE_ANCHOR.md`) and the lane
   decision-state boundary are unchanged.
4. **No lane re-activation is required.** The Adaptive Idea Orchestration first
   lane is already ACTIVE (roadmap §4/§6).
5. A **separate owner implementation authorization is required after this
   specification is approved**, mirroring the FDC-001 first-increment gate.
6. **Roadmap synchronization, if later required, is a separate governed action**
   (roadmap §11: "a phase implementation is committed"), not part of this drafting
   or of implementation scope.
7. The **bicycle automatic brake-light decision remains the only authorized
   content scope.** FDC-002 adds no second case, domain, or decision.
8. The **lane records evidence but does not perform or verify physical testing,
   calibration, bench testing, or field testing** (lane authorization §7).
9. **Clearing the `missing_physical_or_calibration_information` blocker is a
   user-facing-surface rule, not a domain-method change.** The prohibition on
   clearing that blocker through bare text entry is enforced at the Flask route
   and form surface. The legacy first-increment `resolve_gap()` /
   `reclassify_gap()` domain methods remain behaviorally unchanged solely to
   preserve the previously accepted FDC-001 internal/programmatic contract and
   its frozen acceptance tests; they are not modified to universally reject any
   gap, and this preservation creates no user-facing clearing path for the
   physical/calibration blocker (§7.2, §8, §9, §10).

This document does not create a new product lane, roadmap phase, governance
program, anchor, generic laboratory or test-plan subsystem, persistence subsystem,
or final technical-selection authority.

## 2. Authoritative repository identity

- Branch: `feature/atomic-json-session-persistence`
- Authoritative SHA: `38b5d81e319d585c74182dca245886b4bd8520b3`
- FDC-001 first increment merged at PR #17 (`fbd2992…`); observation record merged
  at PR #18 (`dd17fcdb…`); authoritative tip is the PR #18 merge `38b5d81…`.
- FDC-002 builds on the committed FDC-001 domain model
  (`engine/decision_workspace.py`), Flask surface (`web/app.py`,
  `web/templates/decision_workspace.html`), and acceptance set
  (`tests/test_fdc001_first_increment.py`, 32 tests). The frozen worktree
  `/home/user/inventorai` (`aec9cf6…`, paused persistence draft) is not used or
  modified.

## 3. Product problem

The first practical-use exercise ended truthfully at `blocked_by_evidence_gap`,
remaining blocker `missing_physical_or_calibration_information`. The current
workspace records decision inputs, constraints, gaps, dispositions, and owner
preference, but lacks a direct workflow to:

- record externally-produced physical/operator evidence against a specific gap;
- assess whether that evidence supports, partially addresses, contradicts, or
  remains insufficient for the gap;
- make an explicit, separate resolution decision;
- explain what evidence or action could clear a blocker.

FDC-002 solves only this verified problem.

## 4. Objective and bounded scope

Enable a user to:

1. select an existing evidence gap;
2. record externally-produced operator/physical evidence;
3. preserve `claim_class`, `provenance`, `verification_status`, candidate scope,
   `method`/`source_label`, and limitations;
4. explicitly link the evidence to the selected gap;
5. assess the evidence as one of `supports_resolution`, `partially_addresses`,
   `contradicts_assumption`, `insufficient`;
6. make a separate explicit gap decision: `resolved`, `remains_blocking`,
   `reclassified_nonblocking`;
7. ensure evidence entry alone changes no readiness;
8. ensure assessment alone changes no readiness;
9. change readiness only after a valid explicit resolution decision;
10. preserve atomic mutations, complete history, canonical export, and bounded
    errors;
11. show concise blocker-clearing guidance;
12. emit no final technical selection.

Out of objective: anything beyond this evidence-re-entry / gap-assessment workflow.

## 5. Preserved prohibitions

FDC-002 implementation, when later authorized, must preserve every FDC-001
prohibition and add none of the following:

- no persistence (no `engine.session_store` import; no durable write; in-memory
  only);
- no benchmark run or benchmark-result representation;
- no `technically_selected`, `approved`, `validated`, `certified`,
  `production_ready`, or `frozen` status, and no final technical selection;
- no platform-performed or platform-generated verification; recorded evidence is
  operator-reported / external and explicitly unverified;
- no second decision case, no domain expansion beyond the bicycle
  braking-detection decision;
- no JavaScript (unless committed evidence later proves it necessary);
- no generic laboratory or test-plan subsystem; no artifact upload; no
  multi-decision management; no generalized administration.

## 6. User workflow (from `blocked_by_evidence_gap`)

1. The workspace renders each blocking reason with **clearing guidance** (§9).
2. **Record evidence** (distinct step): operator selects a gap, enters an
   observation/result, selects `claim_class` (restricted, §7), optionally records
   `method`, `source_label`, `evidence_version`, `limitations`, candidate scope,
   and a decision-relevant flag. `verification_status` is **not** an input field;
   it is set by the system to `unverified`. *No readiness change.*
3. **Assess the gap** (distinct step): operator selects the gap and one or more of
   its linked evidence items, selects an `assessment` value, and supplies a
   required rationale. *No readiness change.*
4. **Resolution decision** (part of the same assess step's submission, but a
   distinct field): operator chooses `resolved` / `remains_blocking` /
   `reclassified_nonblocking` with a resolution rationale. Only a valid `resolved`
   or `reclassified_nonblocking` decision changes `gap.blocks_readiness` and
   triggers deterministic readiness recompute.

This preserves the strict separation in §7/§9: evidence entry ≠ verification ≠
relevance ≠ assessment ≠ resolution ≠ readiness ≠ owner preference ≠ technical
selection.

For a gap whose blocking reason is `missing_physical_or_calibration_information`,
this assess-and-decide workflow is the **only** user-facing path that can clear
it; the workspace's pre-existing bare-text gap-resolution control does not clear
that blocker (§7.2, §10).

## 7. Domain / data model

Prefer **extension** of the existing model; do not create a parallel subsystem and
do not duplicate incompatible vocabularies. Reuse existing constants
(`OPERATOR_REPORTED_RESULT`, `EXTERNAL_REFERENCE`, `OPERATOR_ENTERED`,
`DERIVED_BY_RULE`, `MISSING_PHYSICAL_OR_CALIBRATION_INFORMATION`), helpers
(`_validate_candidate_ids`, `_gap`, `_candidate`, `_record`), `ChangeEvent.details`,
`BlockingReason`, and the readiness ordered table.

### 7.1 `EvidenceItem` (new dataclass; in-memory list `evidence`)

| field | type | allowed values | required | source | validation | export | history |
|---|---|---|---|---|---|---|---|
| `evidence_id` | str | `ev-<hex>` | yes | system | unique | yes | `target_id` |
| `linked_gap_id` | str | an existing gap id | yes | user | must reference an existing gap | yes | in `details` |
| `text` | str | non-blank | yes | user | reject blank/whitespace-only | yes | — |
| `claim_class` | str | `operator_reported_result` \| `external_reference` ONLY | yes | user | reject any other value (incl. `observed_fact`) | yes | — |
| `provenance` | str | `operator_entered` \| `derived_by_rule` | yes | user | must be in `PROVENANCES` | yes | — |
| `verification_status` | str | `unverified` ONLY | yes | **system** | system-set; never user-supplied (§7.4) | yes | — |
| `method` | str \| None | free text | optional | user | trimmed; blank → `None` | yes | — |
| `source_label` | str \| None | free text | optional | user | trimmed; blank → `None` | yes | — |
| `evidence_version` | str \| None | free text | optional | user | trimmed; blank → `None` | yes | in `details` where applicable |
| `limitations` | str \| None | free text | optional | user | trimmed; blank → `None` | yes | in `details` where applicable |
| `candidate_ids` | list[str] | known candidate ids | optional | user | `_validate_candidate_ids` | yes | `affected_candidates` |
| `decision_relevant` | bool | true/false | optional (default false) | user | `bool()` | yes | — |

Notes:
- `verification_status` is fixed and system-derived (§7.4); it records only that
  the evidence was recorded, never that the platform verified it. An
  `EvidenceItem` is not a `ClaimItem` and is not added to `inputs`; it lives in a
  separate `evidence` list so the first-increment input semantics remain unchanged.
- `evidence_version` is **operator-entered source metadata** — e.g. an
  external-reference version, prototype/board revision, test-procedure version, or
  calibration-setup version. It is recorded verbatim and never implies the
  platform verified the version, the evidence, or the source.
- `limitations` is **operator-entered** text describing the bounds of the recorded
  observation (e.g. "single bench sample, indoor, no vibration"). It is recorded
  and exported as stated; it does not affect verification or readiness
  automatically and never upgrades or downgrades the evidence's truth-status.

### 7.2 `GapAssessment` (new dataclass; in-memory list `gap_assessments`)

| field | type | allowed values | required | validation |
|---|---|---|---|---|
| `assessment_id` | str | `ga-<hex>` | yes (system) | unique |
| `gap_id` | str | an existing gap id | yes | validated |
| `evidence_ids` | list[str] | ids of evidence linked to that gap | yes (≥1) | each must exist and have `linked_gap_id == gap_id` |
| `assessment` | str | `supports_resolution` \| `partially_addresses` \| `contradicts_assumption` \| `insufficient` | yes | enum |
| `rationale` | str | non-blank | yes | reject blank |
| `resolution_decision` | str | `resolved` \| `remains_blocking` \| `reclassified_nonblocking` | yes | enum |
| `resolution_rationale` | str | non-blank when decision ≠ `remains_blocking` | conditional | reject blank when required |

Resolution rule: a gap may transition to non-blocking (`resolved` or
`reclassified_nonblocking`) **only** when `assessment == supports_resolution` and
≥1 valid linked evidence item is present. `partially_addresses`,
`contradicts_assumption`, and `insufficient` **cannot** resolve the gap and leave
`blocks_readiness` unchanged. `remains_blocking` records the assessment without
changing gap state.

**Compatibility rule (physical/calibration blocker — user-facing surface).** The
legacy first-increment `resolve_gap()` / `reclassify_gap()` domain methods remain
behaviorally unchanged. They are preserved solely to keep the previously accepted
FDC-001 internal/programmatic contract and its frozen acceptance tests valid; they
are **not** modified to universally reject any gap. The prohibition on clearing a
gap whose blocking reason is `missing_physical_or_calibration_information` through
bare text entry is therefore enforced at the **user-facing surface**, not inside
the legacy domain methods: the Flask routes and forms must not clear that blocker
through the legacy bare-text gap-resolution workflow. The FDC-002
evidence-assessment workflow — a linked-evidence `GapAssessment` with
`assessment == supports_resolution`, ≥1 valid linked evidence item, an explicit
`resolved` or `reclassified_nonblocking` resolution decision, and the required
rationale — is the **sole authorized user-facing path** for clearing that blocker.
This compatibility preservation does **not** authorize the web application, any
future UI, or the FDC-002 routes to invoke the legacy methods to clear the
physical/calibration blocker, and **no automatic fallback or hidden readiness
bypass is permitted**. For non-physical gaps, any pre-existing user-facing
gap-resolution behavior is unchanged.

### 7.3 Separation of concepts (binding)

The specification distinguishes, and the implementation must keep distinct:
evidence entry; verification status; evidence relevance; gap assessment; gap
resolution; readiness transition; owner preference; technical selection. The
implementation must make these statements true:

- evidence entry does not clear a blocker;
- `verification_status` does not mean verified fact (it is always `unverified`);
- owner preference does not mean technical selection;
- readiness does not mean approval, validation, certification, or production
  readiness.

### 7.4 `verification_status` boundary (binding API design)

`verification_status` is never a caller-controllable input. The chosen, coherent
API design is:

- the public domain mutation is `add_evidence(...)` with **no** `verification_status`
  parameter and no form field for it; the value is set internally to the constant
  `unverified` (`EVIDENCE_VERIFICATION_UNVERIFIED = "unverified"`);
- callers cannot request any other status; there is no path by which a UI form,
  route, or external caller supplies it;
- defensively, if a later revision adds an optional keyword argument, the method
  must reject any value other than `unverified` with `DecisionError` **before**
  any mutation;
- because the recommended design exposes no such argument, the acceptance set
  must prove behaviorally that no caller-controlled verification-status input
  exists (a posted `verification_status` field is ignored) and that the stored and
  exported value is always `unverified`.

### 7.5 `provenance` semantics (binding interpretation)

`derived_by_rule` does **not** mean the system derived, performed, or verified the
physical observation itself. Binding interpretation:

- the evidence `claim_class` always remains `operator_reported_result` or
  `external_reference`;
- `derived_by_rule` may describe only system-derived **metadata, classification,
  linkage, or scope** about the recorded evidence (e.g. a rule-assigned linkage or
  label), never the substance of the observation;
- it must never convert the evidence into `observed_fact`, verified evidence, or
  platform-generated test evidence, and never changes `verification_status` away
  from `unverified`.

## 8. Validation and atomicity

All FDC-002 mutations are **validate-before-mutate** and atomic, mirroring the
FDC-001 `dispose_candidate`/`update_input` corrections. On any validation failure,
the operation raises `DecisionError` and leaves unchanged: the `evidence` list,
`gap_assessments` list, gap state, `revision`, `history`, `readiness_status`,
`blocking_reasons`, and `change_impact_summary`.

Required validation cases (each → `DecisionError`, no mutation):

- invalid `linked_gap_id` / `gap_id`;
- invalid `candidate_id` (via `_validate_candidate_ids`);
- invalid `evidence_id` referenced in an assessment;
- blank evidence `text`;
- unsupported `claim_class` (anything other than the two allowed; `observed_fact`
  specifically rejected);
- unsupported verification claim — per §7.4 there is no caller-controlled
  `verification_status` input; a posted `verification_status` field is ignored, and
  any defensive optional argument carrying a non-`unverified` value is rejected
  before mutation;
- evidence referenced in an assessment that is linked to a different gap;
- empty evidence set in an assessment;
- assessment without rationale;
- resolution without evidence;
- resolution using `insufficient` or `contradicts_assumption` (or
  `partially_addresses`) evidence;
- duplicate resolution of an already non-blocking gap.

`evidence_version` and `limitations` are optional and normalized (trimmed; blank →
`None`); they are never required, never affect validation outcome, and never
change verification or readiness.

**User-facing physical-blocker guard (route surface; bounded and atomic).** The
pre-existing user-facing gap-resolution route (the first-increment bare-text
resolve/reclassify control), when asked to clear a gap whose blocking reason is
`missing_physical_or_calibration_information`, rejects the request with a bounded
error (HTTP 400 via `_render_decision_workspace(record, error=…, status=400)`) and
performs **no** mutation — no change to gap state, `revision`, `history`,
`readiness_status`, `blocking_reasons`, or `change_impact_summary`, and no
`ChangeEvent`. This guard lives at the web route surface (§10); the legacy domain
methods themselves are not modified (§7.2), and the guard must not invoke them to
clear the physical/calibration blocker. Non-physical gaps are unaffected.

**History-event rule (exactly one event per successful submission):** every
successful FDC-002 mutation records exactly one `ChangeEvent` and one revision
increment via `_record`. Specifically:

- successful evidence entry records exactly one `evidence_added`;
- a successful assessment whose `resolution_decision == remains_blocking` records
  exactly one `gap_assessed`;
- a successful assessment that validly changes the gap to non-blocking (a
  `resolved` or `reclassified_nonblocking` decision backed by
  `supports_resolution` + ≥1 evidence item) records exactly one
  `gap_resolved_via_evidence`.

A single atomic assessment submission therefore emits **exactly one** of
`gap_assessed` or `gap_resolved_via_evidence` — **never both**. A
`gap_resolved_via_evidence` event's `details` carries the complete
assessment-and-resolution audit: `gap_id`, `evidence_ids`, `assessment`,
`rationale` (assessment rationale), `resolution_decision`, `resolution_rationale`,
`previous_blocks_readiness`, and `new_blocks_readiness`; the event's own
`prior_readiness_status` and `new_readiness_status` fields carry prior and new
readiness. A `gap_assessed` event's `details` carries `gap_id`, `evidence_ids`,
`assessment`, `rationale`, and `resolution_decision = remains_blocking`.

## 9. Readiness and blocker semantics

1. **Blocker guidance is system-derived from the blocker code** — a deterministic
   static map `BLOCKER_CLEARING_GUIDANCE[code] -> str`. Codes without an entry
   render no guidance (never invented text).
2. `missing_physical_or_calibration_information` guidance must state, in substance:
   "Record an externally-produced operator or physical observation/result against
   this gap, then make an explicit assessment and resolution decision. This lane
   performs no verification; recorded evidence is operator-reported and
   unverified."
3. **Evidence entry alone leaves readiness unchanged.**
4. Assessment values `partially_addresses`, `contradicts_assumption`, and
   `insufficient` **leave the gap blocking** (no readiness change).
5. **Only a valid explicit resolution decision** (`resolved` or
   `reclassified_nonblocking`, requiring `supports_resolution` + ≥1 evidence item)
   may change `blocks_readiness`.
6. The existing readiness ordered table (§5 of FDC-001) is **unchanged**; only the
   set of blocking gaps changes, then readiness recomputes deterministically.
7. **Unsupported readiness remains impossible**: nothing auto-resolves;
   `verification_status` is permanently `unverified`; through the user-facing
   surface a `missing_physical_or_calibration_information` gap cannot be cleared
   without an explicit, evidence-backed, rationale-carrying FDC-002 resolution
   decision, and the legacy bare-text gap-resolution route does not clear it
   (§7.2, §10). The legacy `resolve_gap()` / `reclassify_gap()` domain methods
   remaining available for the FDC-001 internal/programmatic contract create no
   user-facing bypass.
8. **No prohibited status may be emitted** (`PROHIBITED_STATUS_VALUES` never
   appears as an output status).

## 10. UI routes and forms (smallest; no JavaScript)

Extend `web/templates/decision_workspace.html` and add two narrow POST routes in
`web/app.py` (reusing `_render_decision_workspace(record, error=…, status=400)` for
bounded errors and PRG redirect on success). Native HTML only.

Render: each `blocking_reason` shows its `clearing_guidance` (when present).

**Form 1 — Record evidence** → `POST /decision-workspace/<did>/evidence`
Fields: gap (select of existing gaps); claim_class (select limited to
`operator_reported_result`, `external_reference`); observation/result text;
method (text); source_label (text); evidence_version (text); limitations (text);
candidate scope (select, optional, "(none)"); decision-relevant (checkbox).
`verification_status` is **not** a form field (system-set, §7.4); any posted
`verification_status` value is ignored. On success → redirect to the workspace
view; on `DecisionError` → 400 with a bounded message, no mutation.

**Form 2 — Assess gap & decide** → `POST /decision-workspace/<did>/gap-assessment`
Fields: gap (select); one or more linked evidence items (native multi-select of
that gap's evidence); assessment (select of the four values); assessment rationale
(text); resolution decision (select of the three values); resolution rationale
(text). On success → redirect; on `DecisionError` → 400 bounded error, no
mutation.

**Legacy gap-resolution route guard (physical/calibration blocker).** Any
pre-existing user-facing gap-resolution control (the first-increment bare-text
resolve/reclassify route) must reject an attempt to clear a gap whose blocking
reason is `missing_physical_or_calibration_information`, returning a bounded 400
via `_render_decision_workspace(record, error=…, status=400)` with no mutation
(§8). Form 2 (assess gap & decide) is the **sole** user-facing path that may clear
that blocker, and only via a valid evidence-backed resolution. The route guard
must not invoke the legacy domain methods (§7.2) to clear the physical blocker and
must provide no automatic fallback or hidden readiness bypass. Non-physical gaps
are unaffected.

Explicitly excluded from FDC-002: input update/remove controls; export-filename
correction; multi-decision management; generalized administration; test execution;
artifact upload; persistence.

## 11. Export and history

Canonical JSON (extending `to_record_dict` / `to_export_dict`) must include:

- `evidence` — list of `EvidenceItem` dicts; each dict includes `evidence_id`,
  `linked_gap_id`, `text`, `claim_class`, `provenance`, `verification_status`,
  `method`, `source_label`, `evidence_version`, `limitations`, `candidate_ids`,
  and `decision_relevant`. The per-item `evidence_version` and `limitations`
  (operator-entered, `None` when blank) are exported as stored;
- `gap_assessments` — list of `GapAssessment` dicts (incl. `gap_id`,
  `evidence_ids`, `assessment`, `rationale`, `resolution_decision`,
  `resolution_rationale`);
- per-`blocking_reason` `clearing_guidance`;
- `history` events for evidence and assessment (§8 history-event rule);
- the readiness impact (carried by each event's `prior_readiness_status` /
  `new_readiness_status` and the `change_impact_summary`);
- the record-level `export_metadata.limitations` disclaimer list (distinct from
  the per-evidence `limitations` field), extended with: "no verification performed
  by this lane; recorded evidence is operator-reported and unverified".

Required history `change_type` values are governed by the §8 history-event rule:
`evidence_added` (one per evidence entry), `gap_assessed` (one per assessment with
`resolution_decision == remains_blocking`), and `gap_resolved_via_evidence` (one
per assessment that validly changes blocking state — never emitted together with
`gap_assessed` for the same submission). The `gap_resolved_via_evidence`
`details` carry the complete audit (`gap_id`, `evidence_ids`, `assessment`,
`rationale`, `resolution_decision`, `resolution_rationale`,
`previous_blocks_readiness`, `new_blocks_readiness`).

The export must retain: exactly one canonical `generated_at` (in
`export_metadata`); no durable-storage claim; no restart-restoration claim; no
benchmark result; no final-selection status.

## 12. Acceptance-test specification

New file: `tests/test_fdc001_second_increment.py`, named set
`FDC002_SECOND_INCREMENT_ACCEPTANCE`. Behavioral tests (static inspection only for
prohibitions that cannot be observed behaviorally). Target **≈ 33** tests — one per
distinct behavioral guarantee below; fewer would leave a guarantee unverified. (The
target rose from ≈26 to ≈30 to add four guarantees: per-evidence `limitations`
preserved in export; `evidence_version` preserved in export; the one-event-per-
submission history rule; and the no-caller-controlled-verification-status rule. It
then rose from ≈30 to ≈33 under this compatibility amendment to add three
user-facing-surface guarantees: the legacy bare-text gap-resolution route rejects
clearing a physical/calibration blocker — bounded and atomic; the FDC-002
assess-and-decide route is the sole user-facing path that clears it, and only via a
valid evidence-backed resolution; and the compatibility-preserved legacy domain
methods are not exposed as a user-facing physical-blocker clearing path.)

1. valid operator-reported evidence entry;
2. valid external-reference evidence entry;
3. candidate-scoped evidence (validated ids);
4. decision-scoped evidence (no candidate);
5. `verification_status` is always `unverified` and is system-set (§7.4);
6. `observed_fact` rejected for evidence entry;
7. invalid gap reference rejected, no event;
8. invalid candidate reference rejected, no event;
9. blank evidence text rejected, no mutation;
10. evidence entry leaves readiness unchanged;
11. assessment with ≥1 linked evidence succeeds (records assessment);
12. `partially_addresses` leaves the gap blocking;
13. `insufficient` leaves the gap blocking;
14. `contradicts_assumption` leaves the gap blocking;
15. invalid evidence reference in assessment rejected, no event;
16. cross-gap evidence (evidence linked to another gap) rejected, no event;
17. resolution without evidence rejected;
18. resolution with insufficient evidence rejected;
19. resolution with contradictory evidence rejected;
20. successful explicit resolution (`supports_resolution` + evidence) clears the
    gap and recomputes readiness deterministically;
21. atomic failed mutation — full-state snapshot proves no partial change;
22. deterministic readiness before/after resolution (identical recompute);
23. blocker-clearing guidance present for
    `missing_physical_or_calibration_information` (live and export);
24. JSON export shape + audit history (evidence, gap_assessments, events,
    `gap_resolved_via_evidence` details recoverable);
25. prohibited statuses absent from export;
26. no `session_store` import, no benchmark result, bounded FDC-001 scope (three
    fixed candidates, fixed decision question) preserved;
27. **operator-entered `limitations` preserved in canonical export** (recorded
    verbatim; blank → `None`; does not affect verification or readiness);
28. **operator-entered `evidence_version` preserved in canonical export** (recorded
    verbatim; blank → `None`; no platform-verification implication);
29. **history-event rule**: an assessment with `resolution_decision ==
    remains_blocking` emits exactly one `gap_assessed` and no
    `gap_resolved_via_evidence`; a valid resolution emits exactly one
    `gap_resolved_via_evidence` (with complete audit `details`) and no
    `gap_assessed`; evidence entry emits exactly one `evidence_added`;
30. **no caller-controlled verification status**: a posted `verification_status`
    form value is ignored and the stored/exported value remains `unverified`
    (and, if a defensive optional argument exists, a non-`unverified` value is
    rejected before mutation);
31. **legacy user-facing gap-resolution route rejects the physical/calibration
    blocker (bounded and atomic)**: posting the first-increment bare-text
    resolve/reclassify request for a `missing_physical_or_calibration_information`
    gap returns a bounded 400 and changes nothing — the gap stays blocking, no
    `ChangeEvent` is recorded, and `revision`, `history`, `readiness_status`,
    `blocking_reasons`, and `change_impact_summary` are unchanged (§8, §10);
32. **FDC-002 assess-and-decide route is the sole user-facing clearing path**: the
    `missing_physical_or_calibration_information` gap clears only through Form 2
    with `supports_resolution` + ≥1 valid linked evidence item + an explicit
    `resolved`/`reclassified_nonblocking` decision + rationale; an otherwise
    equivalent user-facing attempt that lacks the evidence-backed assessment does
    not clear it (§6, §7.2);
33. **compatibility-preserved legacy methods are not a user-facing physical-blocker
    path (static/behavioral)**: the web route layer exposes no user-facing path
    that invokes the legacy `resolve_gap()` / `reclassify_gap()` methods to clear
    the physical/calibration blocker (the legacy guard is present and no automatic
    fallback exists), while the legacy methods remain callable programmatically and
    the frozen FDC-001 acceptance set that exercises them stays unedited (§7.2,
    §15).

The exact count may differ slightly only if the implementation explains why (e.g.
merging two guarantees that share one behavior, or splitting one that needs two
independent assertions).

The FDC-001 acceptance set (`tests/test_fdc001_first_increment.py`, 32 tests)
remains **frozen** and unedited; FDC-002 must not alter it.

## 13. Exact implementation file scope

When later authorized, implementation may modify **only**:

```text
engine/decision_workspace.py
web/app.py
web/templates/decision_workspace.html
tests/test_fdc001_second_increment.py
```

This specification document is the only file created by the drafting action:

```text
docs/product/FDC-002_EXTERNAL_EVIDENCE_REENTRY_AND_GAP_ASSESSMENT_SPECIFICATION.md
```

## 14. Risks and mitigations

- **Overclaiming evidence as verified** → `verification_status` permanently
  `unverified`; claim_class restricted to two unverified classes; no
  platform-performed verification.
- **Confusing operator observation with fact** → `observed_fact` disallowed for
  evidence entry; evidence kept in a separate `evidence` list, not `inputs`.
- **Clearing blockers too easily** → evidence entry ≠ resolution; resolution
  requires `supports_resolution` + ≥1 evidence item + explicit rationale; and the
  `missing_physical_or_calibration_information` blocker cannot be cleared through
  the legacy bare-text user-facing route at all — only through the FDC-002
  evidence-backed workflow (§7.2, §10). The legacy domain methods remain available
  solely for the frozen FDC-001 programmatic contract and create no user-facing
  bypass.
- **Drifting into a generic laboratory / test-plan system** → bounded to the
  existing three-candidate electronics decision; no test execution; no artifact
  upload; two forms only.
- **Persistence coupling** → in-memory only; no `session_store` import; no durable
  write.
- **FDC-001 scope expansion** → single bounded decision; no multi-decision/admin;
  frozen FDC-001 acceptance set.
- **Form complexity** → exactly two native-HTML forms; no JavaScript.

## 15. Non-goals

FDC-002 does not: perform or simulate any physical/calibration/bench/field test;
verify evidence; issue a final technical selection or any prohibited baseline
status; add a second decision case or domain; implement persistence or
restart-restoration; run or represent a benchmark; expose input edit/remove or
fix the export filename; add multi-decision management, generalized
administration, or artifact upload; modify governance anchors, `CLAUDE.md`, the
roadmap, `main`, or any frozen persistence file. FDC-002 also does **not** modify
or weaken the legacy `resolve_gap()` / `reclassify_gap()` domain methods'
programmatic contract, and does **not** expose those legacy methods as a
user-facing path for clearing the `missing_physical_or_calibration_information`
blocker (§7.2, §10); they are preserved unchanged solely for the frozen FDC-001
internal contract and acceptance tests.

Explicitly prohibited paths (must not change under any FDC-002 authorization):
`engine/session_store.py`, `tests/conftest.py`, `tests/test_session_persistence.py`,
`.gitignore`, `web/templates/session.html`, `web/templates/deliverable.html`, all
frozen uncommitted persistence files, governance anchors, `CLAUDE.md`, `main`,
benchmark-related implementation, and any domain-expansion or generic
test-plan/laboratory file.

## 16. Owner approval and implementation boundary

This specification is a REVIEW DRAFT and authorizes no implementation. After owner
approval, a **separate, explicit, repository-grounded owner implementation
authorization** is required, which must name: the exact four implementation files
above; the named acceptance-test set `FDC002_SECOND_INCREMENT_ACCEPTANCE`
(`tests/test_fdc001_second_increment.py`); a clean isolated worktree based on the
then-authoritative SHA; and explicit preservation of all holds, closed states, the
persistence pause, the benchmark-not-run state, and the no-final-selection
boundary. The implementation must also preserve the frozen FDC-001 acceptance set
byte-for-byte — the legacy `resolve_gap()` / `reclassify_gap()` domain methods stay
backward-compatible (§7.2) — and enforce the
`missing_physical_or_calibration_information` clearing prohibition at the
user-facing route surface (§10), never by modifying the legacy domain methods and
never by introducing an automatic fallback or hidden readiness bypass. Any later
roadmap synchronization is a separate governed action. Until that separate
authorization exists, no code, test, commit, push, or PR is permitted.
