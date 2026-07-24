# Workstream 10 — Loader Interface and BASE RED Sequence: Owner Decisions

**Record type:** documentation-only owner-decision record for **Workstream 10 — Question Intent Registry**
loader interface (D18–D30) and BASE RED sequencing (D31–D33).
**Status:** docs-only governance record. Authorizes no test creation, no Interface-Contract BASE RED
execution, no production module / registry JSON / loader / dataclass / exception / schema creation, no runtime,
persistence, UI, prompt/AI, GREEN, or WS11 work. Prepared under the risk-based execution and review model
(PR #220), on authoritative base `116334e4ae3d448c1646ea890d0db00c7ae2c8e2` (Merge PR #245, WS10 post-decisions
status canonicalization).

This record supersedes the "candidate" status of the loader path and the unresolved interface items from the
read-only BASE RED behavioral-design analysis. It fixes the loader interface contract and the RED/GREEN
sequence. **No implementation, registry artifact, schema, test, or BASE RED is authorized by this document.**

Accepted review verdict: **B — REPORT ACCEPTED WITH ONE MATERIAL SEQUENCING CORRECTION.** Accepted finding:
there is currently no truthful existing behavioral seam for WS10 Behavioral BASE RED because no registry
artifact, loader, schema, or public loader interface exists. Rejected recommendation: do **not** create a
functional loader or registry artifact before RED. **Required sequence:**
1. record and merge the owner-approved loader-interface decisions (this document);
2. Interface-Contract BASE RED;
3. Minimal Interface GREEN;
4. Behavioral Validation BASE RED;
5. Behavioral GREEN.

---

## Loader interface decisions

### D18 — Loader module path
The final WS10 v1 loader module path is `engine/question_intent_registry.py`. It is **no longer a candidate
path**.

### D19 — Public load function
The public loading interface is:
```python
load_question_intent_registry(
    registry_path: Path,
    source_artifact_path: Path,
) -> QuestionIntentRegistry
```
Both paths are explicit **required** parameters. **No registry loading may occur during module import.**

### D20 — Registry public API
`QuestionIntentRegistry` exposes only:
```python
get(question_id: str) -> QuestionIntentRecord
list_records() -> tuple[QuestionIntentRecord, ...]
```
No public mutation API is authorized.

### D21 — Immutable return types
The public types are **immutable dataclasses**: `QuestionIntentRecord`, `QuestionIntentRegistryMetadata`,
`QuestionIntentRegistry`. The public API must **not** return mutable dictionaries as registry records.

### D22 — Exception types
Use `QuestionIntentRegistryLoadError` and `QuestionIntentNotFoundError`.
- `QuestionIntentRegistryLoadError` covers file reading, JSON parsing, structural validation, metadata
  validation, source-reference validation, and source-ID-set validation failures.
- `QuestionIntentNotFoundError` is raised only by `get(question_id)` for an unknown committed question ID.

### D23 — Validation timing
All registry and source-artifact validation occurs during `load_question_intent_registry(...)`. Unknown-ID
validation occurs during `QuestionIntentRegistry.get(question_id)`.

### D24 — Path injection and test isolation
`registry_path` and `source_artifact_path` are explicit required parameters in v1. **No module-level
production path constant is part of the required loader interface.** Tests must use temporary files through
explicit path injection.

### D25 — Caching policy
The WS10 v1 loader performs **no** module-level or global caching. Every explicit load call reads and
validates the supplied files. No cache-reset hook is required.

### D26 — Stable error contract
Tests assert **exception type and stable `reason_code`**, not complete human-readable error text.
`QuestionIntentRegistryLoadError` exposes a `reason_code`. Approved initial reason codes:
`MISSING_REQUIRED_FIELD`, `DUPLICATE_QUESTION_ID`, `DUPLICATE_INTENT_ID`, `INVALID_DESIGN_GAP_ID`,
`INVALID_METADATA`, `SOURCE_ID_SET_MISMATCH`, `SOURCE_REFERENCE_MISMATCH`, `INVALID_SOURCE_ARTIFACT_PATH`,
`INVALID_JSON`, `FILE_READ_ERROR`. This list may be extended only through a later owner-approved decision.

### D27 — Validation mechanism
WS10 v1 uses Python standard-library JSON parsing and explicit validation. No new schema-validation dependency
is authorized. No JSON Schema artifact is required for the initial loader implementation.

### D28 — Registry top-level shape
The future registry JSON top-level shape is:
```json
{
  "metadata": {},
  "records": []
}
```
Metadata appears once at the top level. Each question record appears once in `records`.

### D29 — Stable list ordering
`QuestionIntentRegistry.list_records()` returns records in the committed source-artifact order:
1. design-gap group order as committed in the source JSON;
2. question order inside each group.

The loader must reject source/registry ID-set mismatch but **may reorder** validated registry records into
source-artifact order for the immutable runtime representation.

### D30 — No-fallback meaning
On any registry read, parse, validation, source-reference, or source-ID-set failure, the loader raises
`QuestionIntentRegistryLoadError`. It must **not**: return an empty registry; return a default record;
silently skip invalid records; fall back to question text; use `_STALL_REFRAME`; load an alternative registry;
or continue with partially valid data.

## BASE RED sequencing decisions

### D31 — Interface-Contract BASE RED scope
The first separately authorized BASE RED gate will test only: the approved module contract; the approved
public load function; the immutable registry public API; the two approved exception types; the stable
`reason_code` contract; and the absence of implicit module-level loading. A controlled missing-module or
missing-symbol failure is acceptable **only** in this Interface-Contract RED gate. Malformed test setup or
unrelated import errors are **not** acceptable.

### D32 — Minimal Interface GREEN boundary
The later Minimal Interface GREEN gate may create only: `engine/question_intent_registry.py`; immutable
dataclasses; exception types; public function and method signatures; and deterministic fail-loud placeholder
behavior sufficient to close Interface-Contract RED. It must **not** create: the production registry JSON;
successful valid-registry loading; full structural validation; runtime integration; persistence; UI;
prompt or AI logic; or WS11 behavior.

### D33 — Behavioral Validation BASE RED scope
After Minimal Interface GREEN is merged and verified, a separate Behavioral Validation BASE RED gate will
cover at minimum:
1. valid registry load;
2. exact source-ID and registry-ID set equality;
3. deterministic `get(question_id)`;
4. unknown-ID typed failure;
5. missing required field rejection;
6. duplicate `question_id` rejection;
7. duplicate `intent_id` rejection;
8. invalid `design_gap_id` rejection;
9. invalid metadata rejection;
10. `source_reference.question_id` mismatch rejection;
11. invalid source artifact reference rejection;
12. `_STALL_REFRAME` exclusion;
13. no-fallback behavior;
14. stable `list_records` ordering;
15. semantic fields required as non-empty strings without automated semantic-quality judgment.

## Status and boundaries

This document records decisions only. It does **not** authorize: test creation; Interface-Contract BASE RED
execution; production module creation; registry JSON creation; loader implementation; dataclass
implementation; exception implementation; schema creation; runtime changes; persistence; UI; prompts or AI
logic; GREEN; or WS11. Workstream 10 remains **BASE RED NOT STARTED — IMPLEMENTATION NOT AUTHORIZED**.
Workstream 11 remains **NOT STARTED**. These decisions build on and do not alter the merged WS10 Increment
Contract or the WS10 v1 Record-Shape Owner Decisions (D1–D17). Official product state remains
`DEMO_READY_WITH_LIMITATIONS`; MVP scope remains electronics/electrical-only; the AI Coach (WS17) remains
BLOCKED until Workstreams 1–16 are owner-closed. The Phase A branch remains fixed at `57e2fac8`; PR #167 and
PR #162 remain untouched.
