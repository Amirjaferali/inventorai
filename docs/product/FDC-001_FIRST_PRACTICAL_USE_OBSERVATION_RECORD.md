# FDC-001 First Increment — Practical-Use Observation & Closure Record

STATUS: PRACTICAL-USE OBSERVATION RECORD — COMPLETE
EXECUTION_AUTHORITY: NONE
RECORD_TYPE: OBSERVATION / CLOSURE (DOCUMENTATION ONLY)
IMPLEMENTATION_STATUS: FIRST INCREMENT IMPLEMENTED, MERGED, ACTIVE ON AUTHORITATIVE BRANCH
PRODUCT_VALUE: VISIBLE VALUE CONFIRMED
FINAL_TECHNICAL_SELECTION: NONE
BENCHMARK_STATUS: NOT RUN
PERSISTENCE_STATUS: PRESERVE UNMODIFIED AND PAUSE

This record documents one controlled practical-use exercise of the merged FDC-001
Technical Decision Workspace. It is evidence-only. It authorizes nothing: no
application-code or test change, no persistence activation, no benchmark run, no
second implementation increment, no roadmap phase transition, no anchor amendment,
and no final technical selection.

---

## 1. Title and status

FDC-001 first-increment practical-use observation and closure record. The first
controlled practical-use exercise is COMPLETE and product value is CONFIRMED. This
is a documentation record only; it carries no execution authority.

## 2. Authoritative repository identity

- Authoritative branch: `feature/atomic-json-session-persistence`
- Authoritative remote SHA: `ed302a48eb97e559a172581ff52c3468c5cfa112`
- Merged PR: `#17` (true merge commit `ed302a48…`; parents `fb3d1de2…` then `fbd2992…`)
- Implementation head: `fbd2992977a23b34b2ceca0f68e5d56302ddb426`
- Practical-use runtime source: `ed302a48…`, run from a clean isolated worktree.
  The frozen original worktree (`/home/user/inventorai`, `aec9cf6…`) was not used,
  read into, or modified.

## 3. Exercise purpose

Run the merged FDC-001 Technical Decision Workspace as a real user would, for the
bounded bicycle automatic brake-light decision, to determine whether the first
increment creates visible, useful idea-development value — using only truthful
inputs and explicitly marked uncertainty, fabricating no evidence and making no
technical selection.

## 4. Practical-use actions

Decision: *Which braking-detection architecture should the bicycle automatic brake
light use?* Three fixed candidates remained: `wired_brake_lever_switch`,
`accelerometer_inference`, `wheel_speed_inference`.

Through the existing UI only:

- entered owner requirements and three decision-relevant inputs (one per
  candidate), preserving separate `claim_class` and `provenance` and unverified
  status where applicable;
- recorded three constraints: one **confirmed mandatory** ("no wire to the brake
  lever") truthfully scoped to `wired_brake_lever_switch`, one **soft** ("low
  power draw") scoped to `accelerometer_inference`, and one **preference** ("no
  per-bike calibration");
- applied a **contextual elimination** of `wired_brake_lever_switch` with basis
  `incompatible_with_recorded_requirement` (not a verdict of technical
  invalidity);
- **reclassified** the false-positive gap to non-blocking with an explicit owner
  risk-acceptance rationale; the change history preserves the previous and new
  blocking state plus rationale;
- set an **owner preference** (accelerometer inference), explicitly preference-only;
- attempted an **invalid** disposition (non-active status with no basis): rejected
  with an HTTP 400 bounded validation error and **no** state change;
- **exported** the canonical JSON decision record as a downloadable attachment.

No physical test, calibration result, false-positive measurement, benchmark score,
verified external evidence, production-readiness claim, or final selection was
invented.

## 5. Readiness progression

`insufficient_information` → `blocked_by_evidence_gap`.

The exercise did **not** truthfully reach `comparison_in_progress` or
`decision_ready_for_owner_review`, because physical/calibration evidence was
genuinely unavailable. Remaining blocker: `missing_physical_or_calibration_information`.
This is correct governance behavior — the workspace refused to assert readiness
without supporting evidence.

## 6. Final candidate state

- `wired_brake_lever_switch`: `eliminated`, basis `incompatible_with_recorded_requirement`
- `accelerometer_inference`: `active`
- `wheel_speed_inference`: `active`
- Owner preference: accelerometer inference — explicitly preference only, held
  separate from technical selection. No candidate carries any prohibited
  final-selection status.

## 7. Confirmed value

`VISIBLE VALUE CONFIRMED`. The workspace enabled structured and auditable progress
on a real invention decision while correctly preventing unsupported readiness or
technical-selection claims, and while rejecting an invalid mutation without state
corruption.

Artifact evidence (referenced, not copied into the repository):
`/tmp/FDC001_FIRST_PRACTICAL_USE.json` — 10846 bytes, sha256
`61cd8619a53acc7c118954d3f61001197e8ed02e099813320b614038020a85a0`; valid JSON;
exactly one `generated_at`; served as a downloadable attachment; candidates,
inputs, constraints, gaps, blockers, history, readiness, owner preference,
change-impact summary, and limitations all present; no benchmark result; no
prohibited final-selection status; no persistence claim other than explicit
negative limitations (e.g. "in-memory only; not durable", "restart restoration not
supported").

## 8. Observed friction

1. Export filename duplication: `fdc001-decision-decision-<id>.json` (the decision
   id already begins with `decision-`).
2. The remaining blocker explains what is missing but not what evidence or action
   would clear it.
3. Input update/remove behavior exists in the domain model but is not exposed in
   the current UI.
4. The current UI lacks a direct, explicit workflow connecting a physical/operator
   result to resolution of the corresponding evidence gap.

## 9. Capability classification

Needed for the next serious practical use:

- truthful recording of physical/operator evidence against a gap;
- concise "what clears this blocker" guidance.

Can wait:

- UI input update/remove;
- friendlier export filename.

Explicitly out of scope:

- persistence; benchmark; final technical selection; multi-decision management;
  generalized administration.

## 10. Preserved prohibitions

This exercise and this record changed no application or test code, activated no
persistence, ran no benchmark, selected no architecture, transitioned no roadmap
phase, and amended no anchor. The frozen original worktree (`/home/user/inventorai`,
`aec9cf6…`) and its seven paused persistence paths remain exactly preserved and
were not synchronized.

## 11. Closure statement

The first controlled practical-use exercise of the FDC-001 first increment is
COMPLETE. Product value is CONFIRMED. The decision truthfully remained
`blocked_by_evidence_gap`; the remaining physical/calibration evidence gap is real
and unresolved.

## 12. Next-action boundary

This record authorizes no next implementation. It is observation only. Following
this record, the owner must separately decide between exactly one of:

- one bounded usability correction;
- one second implementation increment focused on truthful physical/operator
  evidence capture;
- continued practical use without code change.

No alternative is selected or begun by this record.
