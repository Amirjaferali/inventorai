# Workstream 10 — Question Intent Registry: Increment Contract

**Record type:** documentation-only Increment Contract for **Workstream 10 — Question Intent Registry**.
**Status:** docs-only governance record. Authorizes no implementation, no BASE RED, no tests, no registry
artifact, no loader code, and no status canonicalization. Prepared under the risk-based execution and review
model (PR #220), on authoritative tip `228f1115eff2894443c2990436128af35f20e8ee` (Merge PR #241, Workstream 9
formal closure). This is the first Workstream 10 gate
(Contract → status canonicalization → BASE RED → implementation → HEAD GREEN → evidence → independent
reviews → owner closure); each later gate requires its own separate owner authorization.

---

## 0. Grounding (committed repository evidence only)

Authored only from committed evidence and current normative governance records:

- Stage 2 serving seam `engine/path_n_questions.py` — `get_path_n_question(gap_type, iterations_open)`,
  load-once, fail-loud, no fallback (b3a5fba §5).
- Stage 2 committed content artifact
  `docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json` — entries are
  `{question_id, text}` only; served positionally by `iterations_open`.
- Gap and record model `engine/idea_state.py` — `Gap{gap_type,status,iterations_open}`,
  `IterationLog{gap_targeted,gaps_changed}`, `AssertionRecord{gap_context,…}`,
  `AcknowledgedUnknown{gap_context}`.
- Registry convention `engine/domain_registry.py` — `load_registry` → immutable `MappingProxyType`,
  `schema_version` gate, required-field + `governance{source,license,owner,review_date,version,
  deprecation_status}` validation, semver/ISO-date checks, fail-loud `RegistryLoadError`.
- Workstream 8 closure `docs/governance/WORKSTREAM_8_NO_VALID_RED_DISPOSITION_AND_FORMAL_CLOSURE.md`
  §4/§6 — expressed-intent objectives deferred to WS9/10/11/14; a successor must not encode expressed
  user intent from `gap_targeted`/`gaps_changed`/`gap_context`/engine-selected gap/fixtures/transcripts.
- Workstream 9 contract/evidence/closure — `WORKSTREAM_9_SINGLE_INTENT_QUESTION_DESIGN_INCREMENT_CONTRACT.md`
  (§2/§3/§5/§12) and `docs/governance/evidence/workstream9_single_intent_question_design/`; WS9 §15 status
  `CLOSED — BASE RED, GREEN, EVIDENCE, AND FINAL ACCEPTANCE COMPLETE`. WS9 recorded a **conceptual** primary
  intent only and explicitly deferred the "registry / taxonomy / identifier system / persistent mapping" to
  Workstream 10.

Where any later inspection conflicts with these committed records, the committed record controls.

## 1. Problem statement

There is no single, governed, machine-readable **source of truth** that declares, per committed Stage 2
question, its **design-time intent** — the one thing the question is built to elicit — with a **stable
identity**, **validation**, and **versioning**. Stage 2 Path N entries carry only `{question_id, text}` and
no declared intent, answer objective, or completion condition; they are served purely positionally.
Workstream 9 guaranteed single-intent question *content* but recorded each question's intent only as prose,
not as durable, queryable, validated data. Consequently no canonical registry exists for governed downstream
behavior (Workstream 11 question-aware evaluation, and later workstreams) to consume when it must reason
about *what a question is designed to elicit*.

Workstream 10 defines the registry that makes each committed Stage 2 question's design-time intent explicit,
identity-bearing, versioned, and validated — as a read-only descriptive layer over already-committed content —
without changing question text, serving order, evaluation, persistence, or user-facing behavior.

## 2. Initial scope (owner decision 1 — Stage 2 only)

Workstream 10 v1 is limited to **Stage 2 Path N committed questions only**
(`electronics_electrical_path_n_questions.json`, gaps MECHANISM_COMPLETENESS / PHYSICAL_FEASIBILITY /
BOUNDARY_AMBIGUITY).

**Stage 3 is NOT included** in this first registry increment. Its existing `Q-ID` / `Question Type` /
`Primary Evidence Target` model (`STAGE3_QUESTION_SET.md`) is recorded here as a **future compatibility
reference only** (§13). This contract does not edit, validate, migrate, or register any Stage 3 question, and
does not touch `STAGE3_QUESTION_SET.md` or `engine/progression_loop.py`.

## 3. Semantic boundary — design-time intent vs user-expressed intent (owner decision 4)

**Design-time question intent** is what a *committed question* is intended to elicit. It is authored **only**
from: the committed final question text; the Workstream 9 single-intent definition; the question's committed
**design gap**; and current normative governance documents.

Design-time intent MUST NOT be derived from, or conflated with, **user-expressed intent**. The registry MUST
NOT derive any value from `gap_targeted`, runtime `gap_context`, engine-selected gaps, fixtures, transcripts,
interaction history, or user answers. User-expressed-intent capture and all intent-aware runtime behavior
remain **deferred** and separately owner-gated (WS8 §6; WS11/WS14). This contract neither reopens nor
re-scopes Workstream 8 or Workstream 9.

The authored intent taxonomy is **new normative data** and requires owner review before any BASE RED or
implementation.

## 4. Single design-time intent definition

Consistent with Workstream 9 §3, a registered question has exactly one design-time intent: one primary user
decision or information request; one answer objective; one observable completion condition; one committed
design gap context; and no hidden secondary task. The registry records this as data; it does not re-derive,
re-open, or alter WS9's single-intent content.

## 5. Registry identity and minimum record shape (owner decision 8)

The registry is keyed by the committed Stage 2 `question_id`. Each record MUST define, at minimum:

| Field | Meaning |
|-------|---------|
| `question_id` | stable identity of the committed Stage 2 question (e.g. `N-PF-1`); immutable |
| `intent_id` | stable identity of the design-time intent record |
| `stage` | journey stage; `2` for WS10 v1 |
| `design_gap_id` | the question's committed **design** gap (e.g. PHYSICAL_FEASIBILITY) — a design-time label, deliberately named `design_gap_id` (NOT `gap_context`) to prevent confusion with runtime/persisted user-state fields |
| `primary_intent` | the single decision/information the question is designed to elicit |
| `answer_objective` | what a complete answer provides |
| `completion_condition` | the observable "done" condition |
| `source_reference` | provenance to the committed question text / normative source |
| `status` | record lifecycle status (e.g. `active`) |

The registry record MUST NOT include: `user_intent`; `gap_targeted`; any transcript-derived data; evaluation
rules; scoring; persistence mappings; or adaptive sequencing.

The schema MUST remain **extensible for future language variants** (owner decision 5) without requiring any
Arabic content or translation work in this increment.

## 6. Source-of-truth and ownership boundaries (owner decisions 2, 4)

- The **new, separate governed registry location** is `docs/governance/question_intent_registry/`.
- The existing Path N question-content JSON (`electronics_electrical_path_n_questions.json`) is **NOT**
  annotated or modified; it remains the source of truth for question **text and serving order**.
- The new registry is the source of truth **only for design-time question intent**.
- Ownership is governance-owned; the registry artifact carries a `governance{source, license, owner,
  review_date, version, deprecation_status}` block mirroring `engine/domain_registry.py`'s
  `_GOVERNANCE_REQUIRED`.

## 7. Versioning and validation principles

Mirroring the committed `engine/domain_registry.py` convention:

- top-level `schema_version` gate (as domain registry gates `"1.0"`);
- semver `governance.version`, ISO-8601 `governance.review_date`, enumerated `deprecation_status`;
- a future read-only loader returns an **immutable** mapping (`MappingProxyType`);
- validation is **fail-loud**: missing/duplicate `question_id` or `intent_id`, missing required fields, or a
  single-intent violation raises an error at load time.

## 8. No-fallback / fail-loud rule

There is **no semantic fallback**. Absence of a registry record for a committed served Stage 2 question, a
malformed record, or a coverage mismatch is a **hard validation failure**, never a silent default
(consistent with `path_n_questions.py` "fail loudly, no fallback" and `domain_registry.RegistryLoadError`).

## 9. Compatibility and language extensibility

- Additive only: the registry must not require any change to `path_n_questions.py`, the Path N JSON artifact,
  `STAGE3_QUESTION_SET.md`, or `progression_loop.py`.
- The domain registry and its known pre-existing **31-failure** `tests/test_domain_registry.py` baseline are
  untouched (neither fixed nor worsened).
- The record shape is extensible for future language variants (owner decision 5); no Arabic content or
  translation is authorized here. Arabic/English parity remains conditional while no committed Arabic
  variants exist.

## 10. Persistence exclusion (owner decision 3)

**No persistence changes are permitted in WS10 v1.** No `question_id`, `intent_id`, or related field is added
to `IterationLog`, `AssertionRecord`, `AcknowledgedUnknown`, session persistence, resume state, or analytics.
Resumed-session determinism (`get_path_n_question` indexed by `iterations_open`) is unchanged. Any future
persistence requirement is deferred to WS11 or another separately owner-authorized increment.

## 11. WS11 evaluation boundary (owner decision 6)

Workstream 10 may declare and validate design-time intent **identity and coverage** only. Workstream 10 MUST
NOT define or implement: answer scoring; evaluation rubrics; correctness judgments; evaluator mappings;
adaptive sequencing; question reordering; or user-intent inference. Question-aware evaluation remains
**exclusively deferred to Workstream 11**, which remains NOT STARTED and is not authorized or started by this
contract.

## 12. Protected behavior from Workstreams 1–9 (must not regress)

- WS1 Evidence Lock immutability; WS2 safety-signal extraction; WS3 deliverable hygiene; WS4 structured
  criticality; WS5 unified risk/safety presentation; WS6 requirement landscape; WS7 actionable validation plan.
- WS8: must not reconstruct or encode user-expressed intent from `gap_targeted`/`gaps_changed`/`gap_context`/
  engine-selected gap/fixtures/transcripts; must not reopen WS8.
- WS9: single-intent question content unchanged (final N-PF-1/N-PF-2/N-BA-1 texts and all preserved N-MC/
  N-PF/N-BA questions remain byte-verbatim); deterministic index serving unchanged; must not reopen WS9.
- The 31 `tests/test_domain_registry.py` failures remain the known pre-existing baseline. Official product
  state remains `DEMO_READY_WITH_LIMITATIONS`; MVP scope remains electronics/electrical-only; the AI Coach
  (WS17) remains BLOCKED until Workstreams 1–16 are owner-closed.

## 13. Future Stage 3 extension (compatibility reference — not authorized)

Stage 3 questions already declare `Q-ID`, `Question Type` (PRIMARY / CONDITIONAL_PROBE), and a
`Primary Evidence Target` (unique within question type, VR-2) in `STAGE3_QUESTION_SET.md`. A future,
separately authorized WS10 increment could extend the registry to Stage 3 by transcribing each question's
`Primary Evidence Target` verbatim as its design-time intent. This is recorded as a **compatibility
reference only**; no Stage 3 registration, validation, or editing is authorized by this contract.

## 14. Candidate BASE RED seams (NOT AUTHORIZED — no tests created here)

Recorded as future design intent only; **no test is created, and BASE RED is not authorized**:

- **S1** loader / registry artifact absent → import/assertion fails;
- **S2 (coverage)** every committed Stage 2 `question_id` has exactly one registry record and vice versa
  (parity swept against the committed Path N artifact);
- **S3 (single intent)** each record declares exactly one `primary_intent`;
- **S4 (identity)** registry `question_id` set equals the committed content id set; no orphan/missing;
- **S5 (no user-intent)** no field is sourced from persisted answer/selection state;
- **S6 (protected serving)** `get_path_n_question` output is unchanged with the registry present.

## 15. Risks and unknowns (owner review required before BASE RED)

- Faithful authoring of `primary_intent`/`answer_objective`/`completion_condition` from committed text + WS9
  definition without drift (the taxonomy is new normative data — §3).
- Future Stage 3 extension scope and its interaction with WS8-protected Stage 3 territory (§13).
- Future loader placement `engine/question_intent_registry.py` (§16) — a future BASE RED/GREEN artifact, not
  created here.
- Language-variant extensibility remaining conditional until committed Arabic variants exist.

## 16. Future loader location (owner decision 7 — not created here)

A future, separately authorized increment may place the read-only loader at
`engine/question_intent_registry.py`, mirroring `engine/domain_registry.py`. **No loader file, registry
artifact, test, or implementation is created under this authorization.**

## 17. Explicit non-authorization clause

This contract is documentation-only and authorizes **no** downstream action. It does not authorize: status
canonicalization; BASE RED; tests; registry JSON creation; loader code; implementation; question-content
changes; Stage 3 changes; UI; schema/database; persistence; evaluator; prompts or AI logic; analytics; or
Workstream 11-or-later work. Workstream 10 implementation and BASE RED remain **UNAUTHORIZED**; Workstream 11
remains **NOT STARTED**. Each later Workstream 10 gate requires its own separate explicit owner authorization.
The Phase A branch remains fixed at `57e2fac8`; PR #167 and PR #162 remain untouched.
