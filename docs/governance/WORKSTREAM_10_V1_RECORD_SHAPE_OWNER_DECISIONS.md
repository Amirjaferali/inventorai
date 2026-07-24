# Workstream 10 v1 — Question Intent Registry Record-Shape: Owner Decisions

**Record type:** documentation-only owner-decision record for **Workstream 10 — Question Intent Registry (v1)**.
**Status:** docs-only governance record. Authorizes no registry artifact, loader, schema, test, BASE RED,
implementation, question-content change, serving change, persistence change, status canonicalization,
roadmap/remediation-plan/contract amendment, or any later Workstream. Prepared under the risk-based execution
and review model (PR #220), on authoritative base `49d26ed9d7bdf9914bf6bd7d0ff41f8ae7e9163d` (Merge PR #243,
WS10 contract status canonicalization).

This record captures the owner-approved D1–D17 record-shape decisions for WS10 v1. It defines the approved
**future** public registry and loader contract; it does **not** implement either. BASE RED remains a separate,
later, separately-authorized gate.

---

## 0. Verified inventory facts (basis for these decisions)

From the owner-accepted WS10 Stage 2 inventory and its raw-evidence completion, on this same authoritative base:

- **11** committed Stage 2 Path N questions in **one** governed content artifact
  `docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json`.
- Gap counts: `MECHANISM_COMPLETENESS` 4, `PHYSICAL_FEASIBILITY` 4, `BOUNDARY_AMBIGUITY` 3.
- Every `question_id` is unique; no duplicate texts; no empty IDs; no empty texts; no malformed records; each
  record has exactly the fields `{question_id, text}`.
- Every question has a directly evidenced **design-gap** association through its committed JSON parent key.
- `question_id` is **not** used by runtime serving; only `text` is served.
- Within-gap question selection is deterministic by `iterations_open`
  (`index = min(iterations_open, len(variants) - 1)`).
- Gap-family selection is **fixed-priority** in the current committed implementation
  (`select_next_gap` over `GAP_PRIORITY = [MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY]`),
  confirmed by `tests/test_workstream_9_single_intent_question_design.py:277`.
- `_STALL_REFRAME` is a non-artifact **display substitution** and is **not** one of the 11 committed questions.
- **Path N ↔ Stage 2** is supported by committed governance (`WORKSTREAM_9_SINGLE_INTENT_QUESTION_DESIGN_INCREMENT_CONTRACT.md`
  §4) and code comments (`engine/progression_loop.py:253,270`), but **`stage` is not a field in the source
  question records** (the artifact `metadata` has `path` but no `stage`).
- **No sufficient behavioral BASE RED seam existed before these owner decisions** — the earlier verdict was
  `NO SUFFICIENT BEHAVIORAL BASE RED SEAM YET — OWNER RECORD-SHAPE DECISIONS REQUIRED`. These decisions supply
  the public contract that later makes deterministic BASE RED seams valid (§D17).

## 1. Owner-approved decisions (D1–D17)

### D1 — Cardinality — APPROVED
- Exactly **one** registry record per committed Stage 2 Path N `question_id`.
- Exactly **one** unique `intent_id` per registry record.
- Intents are **not** shared between questions in WS10 v1.
- **No** separate intent taxonomy or mapping table in v1.

### D2 — Identity semantics — APPROVED
- `question_id` is the committed identity of the question in the governed question artifact.
- `intent_id` is the unique identifier of its design-time intent record; it is **not** a reusable
  intent-taxonomy identifier in WS10 v1.
- Deterministic format: **`intent_id == "QI-" + question_id`** (example: `QI-N-PF-1`).
- Identity changes and migration mechanics beyond the minimum rules (D10) remain **deferred**.

### D3 — Required v1 record shape — APPROVED
Required fields, exactly:
`question_id`, `intent_id`, `design_gap_id`, `primary_intent`, `answer_objective`, `completion_condition`,
`source_reference`.
- Do **not** add `stage` or `status` to individual records.
- Do **not** add runtime user-state, evaluation, persistence, scoring, sequencing, transcript, or
  user-intent fields.

### D4 — Stage representation — APPROVED
- Store `stage: 2` **once** in registry metadata; do **not** repeat it per record.
- Explicitly recorded: Stage 2 is established through committed governance and code evidence, **not** through
  a `stage` field in the source question records.

### D5 — Design-gap representation — APPROVED
- Canonical `design_gap_id` values only: `MECHANISM_COMPLETENESS`, `PHYSICAL_FEASIBILITY`,
  `BOUNDARY_AMBIGUITY`.
- Each record's `design_gap_id` must match the exact committed JSON parent key containing its `question_id`.
- **No aliases** permitted in v1.

### D6 — Source-reference (correction recorded) — APPROVED
The earlier package recommendation of **path plus array-index JSON Pointer is NOT approved.**
Approved `source_reference` shape:
```json
{
  "artifact_path": "docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json",
  "question_id": "<committed question_id>"
}
```
Reason: array-index JSON pointers are unstable under question reordering; `question_id` is the durable
committed locator; structural validation must resolve the question **by ID** and verify its committed parent
gap. Do **not** store an array index, a JSON array pointer, or a source commit hash in every record.

### D7 — Artifact format and location — APPROVED (records the future target only)
- One JSON registry file.
- Explicit future governed path:
  `docs/governance/question_intent_registry/electronics_electrical_question_intent_registry_v1.json`.
- No file-per-gap split; no YAML; no database representation.
- This records the future target path only; the registry JSON is **not** created in this gate.

### D8 — Registry metadata — APPROVED
Minimum metadata fields: `schema_version`, `registry_version`, `owner`, `source_artifact`, `review_date`,
`stage`, `language`. Approved initial intended values:
| Field | Value |
|---|---|
| `schema_version` | `1.0.0` |
| `registry_version` | `1.0.0` |
| `owner` | `InventorAI Owner` |
| `source_artifact` | `docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json` |
| `stage` | `2` |
| `language` | `en` |
| `review_date` | the actual owner-approval date recorded during the later registry-artifact authoring gate |

Do **not** add license, deprecation, or lifecycle metadata unless an existing binding repository rule requires
it and the exact evidence is cited.

### D9 — Status lifecycle — APPROVED
- No per-record `status` field in WS10 v1.
- `active`, `retired`, and `superseded` lifecycle states are **deferred**.
- No deletion or lifecycle machinery is authorized now.

### D10 — Minimum change rules — APPROVED
- Question wording may change while retaining the same `question_id`.
- When wording changes, the semantic registry fields must be **reviewed again** (D12).
- A new or changed `question_id` requires registry coverage reconciliation and a `registry_version` change.
- Removed or replacement questions must be exposed through exact **source-to-registry ID-set equality**.
- No registry record may remain silently orphaned.
- Detailed migration, retirement, replacement-history, and deletion mechanisms remain **deferred**.

### D11 — Structural validation boundary — APPROVED (machine-checkable only)
- Valid registry JSON structure; required metadata present; required record fields present.
- Unique and non-empty `question_id`; unique and non-empty `intent_id`.
- Deterministic `intent_id == "QI-" + question_id`.
- **Exact set equality** between registry question IDs and the committed 11 source question IDs; no missing
  records; no orphan records.
- Valid canonical `design_gap_id`, matching the source artifact parent key containing the question.
- `source_reference.artifact_path` equals the approved source artifact path; `source_reference.question_id`
  equals the record's `question_id`; every source reference resolves successfully.
- Prohibited runtime/user-state fields **absent** — including: `user_intent`, `gap_targeted`, `gap_context`,
  transcripts, user answers, persistence state, scoring, evaluation results, serving sequence, runtime
  selection state.
- **Semantic correctness must not be decided by the structural validator.**

### D12 — Semantic governance review — APPROVED (human/owner boundary)
Reviews: fidelity of `primary_intent` to the committed question text; accuracy of `answer_objective`;
adequacy and testability of `completion_condition`; compliance with the WS9 single-intent rule;
appropriateness of `design_gap_id`; absence of user-expressed-intent inference. The reviewer must inspect: the
exact committed question text; the source gap; the applicable WS9 single-intent governance definition; and the
proposed semantic fields.

### D13 — Future loader public behavior — APPROVED (not implemented here)
- Load the governed registry **read-only**; expose all records; deterministic lookup by `question_id`;
  return the matching immutable/read-only record.
- Unknown `question_id` → explicit lookup failure; malformed or structurally invalid registry → fail during
  load; no silent `None` success; no generic fallback; caching permitted but not required; internal classes
  and implementation mechanisms remain **undecided**. This gate does not authorize creating the loader.

### D14 — Fail-loud and no-fallback behavior — APPROVED
Registry **load** must fail for: missing registry file; malformed JSON; invalid registry structure; duplicate
`question_id`; duplicate `intent_id`; invalid deterministic `intent_id`; missing source-question coverage;
orphan registry records; invalid design-gap mapping; invalid or unresolvable source reference; prohibited
fields. **Lookup** must fail explicitly for unknown `question_id`. No generic intent, fallback intent, default
record, or silent recovery may be returned.

### D15 — `_STALL_REFRAME` — APPROVED
- Exclude `_STALL_REFRAME` entirely from the WS10 v1 registry.
- It is a display intervention, not one of the 11 governed Path N questions.
- Do not assign it a normal question record or a normal intent record.
- Any future cataloguing requires a separate owner decision and a distinct record type.

### D16 — Language extensibility — APPROVED (minimum-only)
- Registry metadata records `language: "en"`.
- A future language variant may preserve the logical `question_id`.
- No multilingual record structure, translation mapping, language parity mechanism, or language
  fallback/selection architecture is authorized in WS10 v1.

### D17 — BASE RED readiness — APPROVED (design deferred to a separate authorization)
After these decisions are durably recorded, independently reviewed, owner-accepted, merged, and post-merge
verified, the following BASE RED seams **may be designed under a separate authorization** (no test is
authorized here):
- exact coverage of all 11 question IDs; deterministic lookup by `question_id`; rejection of missing records;
  rejection of orphan records; rejection of duplicate IDs; rejection of prohibited fields; validation of the
  deterministic `intent_id`; validation of design-gap consistency; validation of source-reference consistency;
  fail-loud registry-load behavior; explicit unknown-ID lookup failure; no silent fallback; protected
  preservation of existing question text; protected preservation of existing serving order and behavior.

## 2. Approved vs deferred

**Approved for WS10 v1:** D1 cardinality; D2 identity + `QI-<question_id>`; D3 seven-field record shape; D4
metadata-level `stage`; D5 canonical gap values; D6 ID-based `source_reference`; D7 single-JSON future path;
D8 minimum metadata; D11 structural validation; D12 semantic-review boundary; D13 loader public behavior; D14
fail-loud/no-fallback; D15 `_STALL_REFRAME` exclusion; D16 minimum language rule; D17 recorded BASE-RED-readiness.

**Deferred (require separate owner authorization):** per-record `status` and lifecycle states (D9); intent
reuse / taxonomy / mapping table (D1); detailed migration, retirement, replacement-history, and deletion
mechanics (D10); multilingual record structure / translation / parity / language-selection (D16); `_STALL_REFRAME`
cataloguing (D15); the registry JSON artifact (D7); the loader implementation (D13); the BASE RED tests (D17);
status canonicalization and any roadmap/remediation-plan/contract amendment.

## 3. Approved future public contract (recorded, not implemented)

**Registry (future artifact):** one JSON file at
`docs/governance/question_intent_registry/electronics_electrical_question_intent_registry_v1.json`, with
`metadata{schema_version, registry_version, owner, source_artifact, review_date, stage:2, language:"en"}` and
11 records `{question_id, intent_id, design_gap_id, primary_intent, answer_objective, completion_condition,
source_reference{artifact_path, question_id}}` under the D11 structural rules and D12 semantic review.

**Loader (future implementation):** read-only load; list all records; deterministic `get(question_id)`;
unknown-ID → explicit failure; malformed/invalid registry → fail at load; fail-loud, no fallback (D13/D14).

## 4. Non-authorization (restated)

BASE RED still requires separate authorization. Registry artifact creation remains **unauthorized**. Loader
implementation remains **unauthorized**. Workstream 11 remains **NOT STARTED**. `_STALL_REFRAME` is excluded
from WS10 v1. No status lifecycle or multilingual architecture is authorized in v1. Status canonicalization is
out of scope for this gate; `ACTIVE_EXECUTION_ROADMAP.md`, `DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md`, and
the existing WS10 increment contract are unchanged. Official product state remains `DEMO_READY_WITH_LIMITATIONS`;
MVP scope remains electronics/electrical-only; the AI Coach (WS17) remains BLOCKED until Workstreams 1–16 are
owner-closed. The Phase A branch remains fixed at `57e2fac8`; PR #167 and PR #162 remain untouched.
