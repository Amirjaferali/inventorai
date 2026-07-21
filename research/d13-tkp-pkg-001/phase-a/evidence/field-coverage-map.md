# Phase A Output 1 — Field-Coverage Map

**Purpose (bounded).** Map the fields the existing InventorAI application-state and analysis-output structures capture,
assessed for relevance to the `D13-TKP-PKG-001` concept class: single-signal sensor→microcontroller interfacing guidance
(analog voltage / single-ended digital / pulse-frequency; low-voltage; non-safety-critical). Read-only observation of
repository structure only. No engineering fact is asserted; presence/absence refers to whether the repository defines a
**structured field**, not to any user's data. No journey/personal/production data was accessed.

**Legend.** Present = a structured field exists in the repository. Absent = no structured field exists (may be captured
only as free text, or not at all). "Validation state" = whether the field carries an explicit validation axis.

| Field identifier | Current location | User journey stage | Present/Absent | Data type | Required/Optional | Validation state | Downstream dependency | Evidence reference | Limitation |
|---|---|---|---|---|---|---|---|---|---|
| `IdeaState.idea_id` | `engine/idea_state.py` | Capture (session init) | Present | str | Required | none (identity) | keys all session state | idea_state.py IdeaState | identity only; not interfacing-relevant |
| `IdeaState.domain_signal` | `engine/idea_state.py` | Capture / classification | Present | Optional[str] | Optional | none | domain routing (`domain_registry`) | idea_state.py; domains/electronics_electrical/domain.json | signal string, not a typed sensor/interface descriptor |
| `IdeaState.maturity_level` | `engine/idea_state.py` | Progression (Stage 2) | Present | int (0–2) | Required | derived from evidence/gaps | transition gating | idea_state.py | coarse 0–2; not interface-specific |
| `IdeaState.current_stage` | `engine/idea_state.py` | Progression | Present | int (2\|3) | Required | none | stage routing | idea_state.py | Stage 2/3 only |
| `IdeaState.known_problem` | `engine/idea_state.py` | Capture / Stage 2 | Present | Optional[Evidence] | Optional | via `Evidence.validation_status` | maturity, gap eval | idea_state.py Evidence | free-form content; no structured problem parameters |
| `IdeaState.known_mechanism` | `engine/idea_state.py` | Capture / Stage 2 | Present | Optional[Evidence] | Optional | via `Evidence.validation_status` | maturity, gap eval | idea_state.py Evidence | free-form; mechanism not decomposed into sensor/interface elements |
| `IdeaState.idea_summary` | `engine/idea_state.py` | Capture | Present | Optional[str] | Optional | none | deliverable, output summary | idea_state.py | free text; no structured signal-chain fields |
| `Evidence.quality` | `engine/idea_state.py` | Stage 2/3 | Present | enum ASSERTED\|REASONED\|DEMONSTRATED | Required (on Evidence) | separate from validation | scoring, maturity | idea_state.py Evidence | quality ≠ electrical correctness |
| `Evidence.provenance` | `engine/idea_state.py` | Stage 2/3 | Present | enum (5) | defaulted LEGACY_UNSPECIFIED | n/a | responsibility display | idea_state.py | capture origin only |
| `Evidence.validation_status` | `engine/idea_state.py` | Stage 2/3 | Present | enum (4) | defaulted UNVALIDATED | this IS the axis | derived readiness | idea_state.py | never auto-promoted; no interface-parameter validation |
| `Gap.gap_type` | `engine/idea_state.py` | Stage 2/3 | Present | enum (6 taxonomy) | Required | n/a | question selection | idea_state.py STAGE_2/3_GAP_TYPES | taxonomy is abstract (feasibility/boundary/mechanism); not an electrical-parameter gap |
| `Gap.status` | `engine/idea_state.py` | Stage 2/3 | Present | enum OPEN\|PARTIAL\|CLOSED\|ACCEPTED_RISK | Required | n/a | transition, direction | idea_state.py | "CLOSED" = addressed-in-answers, not validated |
| `AssertionRecord.disposition` | `engine/idea_state.py` | Interaction ledger | Present | enum (6 owner actions) | Required | separate axis | ledger, responsibility | idea_state.py INTERACTION_DISPOSITIONS | records the action, not interface content |
| `AcknowledgedUnknown.gap_context` / `.verbatim` | `engine/idea_state.py` | Parallel track | Present | str / str | Optional | none | display only (no progression) | idea_state.py AcknowledgedUnknown | free text; no typed unknown-parameter |
| `CriticalityConfirmation.category` | `engine/idea_state.py` | Workstream 4 | Present | enum (3) | Optional | none | session-bounded history | idea_state.py | feasibility/value/refinement; not electrical |
| `SuccessCriterion.criterion` | `engine/idea_state.py` | Prototype planning | Present | str | Optional | none | planning metadata only | idea_state.py | never graded; free text |
| `output.observations.apparent_components_ar[]` | `schemas/iot_electronics_output.schema.json` | Analysis output | Present | array{component_ar, basis_ar, component_specificity} | Optional | `component_specificity` distinguishes stated/implied | output rendering | schema v1.1 | component *type* only; "not a BOM"; no electrical parameters |
| `output.observations.power_observations_ar` | `schemas/...schema.json` | Analysis output | Present | str\|null | Optional | none | output | schema v1.1 | "no assumed values"; free text, not a voltage/current field |
| `output.observations.connectivity_observations_ar` | `schemas/...schema.json` | Analysis output | Present | str\|null | Optional | none | output | schema v1.1 | free text; not a typed interface/protocol field |
| `output.identified_concerns.items[].severity` | `schemas/...schema.json` | Analysis output | Present | enum MINOR\|NOTABLE\|SIGNIFICANT | Optional | none | gate signal | schema v1.1 | qualitative; not parameter-derived |
| `output.missing_information.items[]` | `schemas/...schema.json` | Analysis output | Present | array | Required | none | dominates output when input sparse | schema v1.1 | free-text gaps; not a structured interface-field checklist |
| `output.feasibility.feasibility_signal` | `schemas/...schema.json` | Analysis output | Present | enum (5) | Required | platform converts to PASS/WARN/BLOCK | gate engine | schema v1.1 | preliminary signal; explicitly "not a determination" |
| **Sensor output type** (analog-voltage / single-ended-digital / pulse-frequency) | — | (interfacing) | **Absent** (structured) | — | — | — | RQ-01 | — | captured only as free text in components/description; no typed field |
| **Sensor output voltage range** | — | (interfacing) | **Absent** (structured) | — | — | — | RQ-02, RQ-03 | — | no field for min/max output voltage |
| **MCU input logic family / ADC reference / input range** | — | (interfacing) | **Absent** (structured) | — | — | — | RQ-05, RQ-06 | — | no field for target MCU input characteristics |
| **Signal pulse/frequency characteristics** | — | (interfacing) | **Absent** (structured) | — | — | — | RQ-07 | — | no typed pulse/frequency field |
| **Source/load impedance context** | — | (interfacing) | **Absent** (structured) | — | — | — | RQ-04 | — | no impedance/loading field |
| **Datasheet-parameter presence indicator** | — | (interfacing) | **Absent** (structured) | — | — | — | RQ-09 | — | no field recording whether governing parameters are available |

**Bounding note.** Rows for `IdeaState.iteration`, `iteration_log[]` (`gap_targeted`, `question_asked`, `response_summary`,
`gaps_changed`, `maturity_before/after`), `path`, `direction`, and the remaining `output.*` fields (`schema_version`,
`domain`, `analysis_language`, `input_assessment.*`, `idea_summary.*`, `disclaimer_ar`) were inspected and are Present as
session/journey/output-formatting fields but are not directly interfacing-parameter-bearing; they are omitted from the
table for brevity and noted here for completeness. This map is representative for the concept class, not an exhaustive
enumeration of every repository field (see `unresolved-issues.md`, UI-1).
