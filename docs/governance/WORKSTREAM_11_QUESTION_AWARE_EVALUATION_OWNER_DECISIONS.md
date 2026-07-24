# Workstream 11 — Question-Aware Evaluation: Owner Decisions and Increment Contract

**Record type:** documentation-only owner-decision and increment-contract record for
**Workstream 11 — Question-Aware Evaluation (v1)**.
**Status:** docs-only governance record. Authorizes no production code, no RED tests, no
protected-guard amendment, no status canonicalization, no persistence/runtime/UI/prompt/AI change,
and no later workstream. Prepared under the risk-based execution and review model (PR #220), on
authoritative base `03591abc153bfcb0b7c5371085e2e0093501d535` (Merge PR #256, WS10 Behavioral GREEN
canonicalization and formal WS10 closure).

This record fixes the **future** WS11 v1 behavioral scope, production seam, data propagation,
precedence, failure policy, backward compatibility, auditability, and non-goals. It does **not**
implement any of them. Every implementation, test, and status gate remains separately owner-authorized.
It builds on, and does not alter, the merged WS10 Increment Contract, the WS10 v1 Record-Shape Owner
Decisions (D1–D17), or the WS10 Loader-Interface and BASE RED Sequence Owner Decisions (D18–D33).

**Terminology discipline.** This document does not use "smart evaluation", "semantic understanding",
"appropriate answer", "good response", or "intent alignment" as behavioral definitions. Where a
judgment is required it is defined by a deterministic, observable rule or explicitly **deferred** as a
blocker. WS11 v1 introduces no AI, LLM, NLP, or prompt behavior.

---

## 0. Repository-grounded baseline (established facts)

These are facts read from the repository at the authoritative base. They are the basis for the
decisions in §1 and are separated here from decisions and recommendations.

- **F1.** `engine/path_n_questions.py::get_path_n_question(gap_type, iterations_open)` returns only the
  question **text** (`entry.get("text")`, lines 60–61) and **discards `question_id`**.
- **F2.** `engine/progression_loop.py::assess_response(response, domain)` (line 615) receives only the
  response text and the domain; it returns a deterministic quality tier `ASSERTED | REASONED |
  DEMONSTRATED`. It receives no `gap_type`, no `question_id`, and no registry record.
- **F3.** `engine/progression_loop.py::integrate_response(state, gap_type, question, response)` (line
  690) receives the `gap_type` and the served question **text**, but forwards only `(response,
  state.domain)` to `assess_response`; it holds no `question_id` and no registry record.
- **F4.** `engine/progression_loop.py::evaluate_transition(state)` (line 764) is deterministic and
  gap/state based; it requires all Stage-Two gaps CLOSED and involves no AI.
- **F5.** `question_id` does not currently exist in `IdeaState`, `Gap`, `Evidence`, `IterationLog`,
  `AssertionRecord`, or any runtime state outside the WS10 registry module (grep of `engine/` source =
  0 outside `engine/question_intent_registry.py`).
- **F6.** The merged WS10 registry (`engine/question_intent_registry.py`) provides, per committed
  question, the immutable fields: `question_id`, `intent_id`, `design_gap_id`, `primary_intent`,
  `answer_objective`, `completion_condition`, and `source_reference{artifact_path, question_id}`,
  loaded by `load_question_intent_registry(registry_path, source_artifact_path)` and read through
  `QuestionIntentRegistry.get(question_id)` / `list_records()`.
- **F7.** WS10 already performs all registry reading, JSON parsing, structural/metadata/source-reference
  validation, duplicate detection, source-ID-set equality, `_STALL_REFRAME` exclusion, and fail-loud
  no-fallback behavior. This must be **reused**, not duplicated.
- **F8.** The merged protected guard
  `tests/test_workstream_9_single_intent_question_design.py::test_PROTECTED_no_workstream_10_to_14_capability_introduced`
  (line 301) currently asserts `engine.question_aware_evaluation` raises `ModuleNotFoundError`, i.e. it
  requires that WS11 module to remain **absent**.

Additional governing facts:

- **F9.** The WS10 Increment Contract §D6 / §11 states that answer scoring, correctness judgments,
  evaluation rubrics, evaluator mappings, adaptive sequencing, and runtime user-intent inference are
  **outside WS10**, and that WS11's authoritative scope and activation conditions must be confirmed
  separately before WS11 begins. This document is that confirmation.
- **F10.** WS10 §D3 forbids adding `question_id`/`intent_id` to `IterationLog`, `AssertionRecord`,
  session persistence, resume state, or analytics, and states such persistence is **not** automatically
  assigned to WS11.
- **F11.** `engine/scoring.py::score_case` is the historical benchmark scorer, governed by the
  repository "Reporting Integrity Rules"; it is out of scope for WS11.

---

## 1. Owner decisions (D1–D18)

Each decision records: **Repository fact**, **Owner decision**, **Rationale**, **Implementation
consequence**, **Test consequence**, **Non-goals**, and **Change-control rule**.

### D1 — WS11 behavioral purpose — APPROVED (Option A: observation only)

- **Repository fact:** Evaluation today (`assess_response`, `evaluate_transition`) is deterministic and
  question-agnostic (F2–F4); no component consults per-question intent.
- **Owner decision:** WS11 v1 produces a **deterministic, auditable question-intent evaluation
  observation only**. It MUST NOT independently close gaps, mutate `Gap`/`Evidence`, alter
  `evaluate_transition`, or override existing deterministic domain and safety protections.
- **Rationale:** An observation-only layer adds question-awareness without changing any merged
  deterministic verdict, mirroring the established "observations only; authorization separate" pattern
  in `engine/stage3_evaluator.py`.
- **Implementation consequence:** WS11 output is a returned value; no state mutation.
- **Test consequence:** RED/GREEN assert the returned observation only; protected transition/quality
  tests remain unchanged and green.
- **Non-goals:** No gap closure, no transition change, no scoring change.
- **Change-control rule:** Changing WS11 from observation-only to verdict-changing requires a new
  separately-authorized workstream increment.

### D2 — Production architecture — APPROVED (Option A: new pure module) with comparison

- **Repository fact:** The stale guard names `engine.question_aware_evaluation` (F8); `assess_response`
  and the transition logic are protected by the WS9 / Path-N suites.
- **Owner decision:** Introduce a **new pure deterministic module `engine/question_aware_evaluation.py`**.
  It is chosen for isolation, NOT merely because the guard names it.
  - *Alternative A (selected) — new pure module:* leaves `assess_response`, `integrate_response`, and
    `evaluate_transition` unmodified; WS11 logic is fully isolated and independently testable.
  - *Alternative B (rejected) — modify existing `progression_loop` functions:* would edit protected,
    merged, deterministic functions, increasing regression risk to the WS9 / Path-N protected suites and
    coupling WS11 to the transition/quality logic that D1/D8 require to stay authoritative.
  - *Why A is safer:* it confines WS11 to additive code behind a pure boundary; the only protected-suite
    interaction is the absence guard (handled by D16), not the evaluation/transition logic.
- **Rationale:** Isolation preserves every merged deterministic protection.
- **Implementation consequence:** exactly one new production file
  `engine/question_aware_evaluation.py`; `progression_loop.py` may later gain only a **transient,
  additive** call site that passes inputs and discards the returned observation into an audit channel
  (a separate, minimal, later-authorized change — see D4/D18).
- **Test consequence:** RED targets the new module's public seam; a controlled missing-module RED is
  acceptable (D17).
- **Non-goals:** No edit to `assess_response`, `evaluate_transition`, or `scoring.py`.
- **Change-control rule:** Any future need to modify existing evaluation functions requires separate
  authorization and its own protected-regression proof.

### D3 — Public seam — APPROVED (pure, no I/O)

- **Repository fact:** WS10 loading is already a separate concern (F6/F7); the registry object is
  read-only.
- **Owner decision:** The single public callable is:
  ```python
  def evaluate_question_intent(
      question_id: str,
      base_quality: str,            # ASSERTED | REASONED | DEMONSTRATED, from the UNCHANGED assess_response
      served_design_gap_id: str,    # the design-gap under which the question was served this turn
      registry: QuestionIntentRegistry,
  ) -> QuestionIntentEvaluation
  ```
  - It receives a **`QuestionIntentRegistry` object** (already loaded) plus a `question_id`; it does
    **not** receive raw `QuestionIntentRecord` (it resolves the record via `registry.get`, reusing WS10).
  - It receives the deterministic `base_quality` tier (computed by the caller through the existing
    unchanged `assess_response`), **not** the raw response text, and no domain — raw response content is
    not consumed in v1 (see D5/D7).
  - It performs **no file, registry, or network I/O**; loading remains outside via the WS10 loader.
  - The caller MUST source `question_id` and `served_design_gap_id` from the **same** immutable
    `ServedQuestion` instance (D4), so the two identity inputs cannot drift apart.
- **Rationale:** A pure function with an injected registry is deterministic, trivially testable, and
  cannot duplicate WS10 I/O or validation.
- **Implementation consequence:** The evaluator imports only `engine.question_intent_registry` public
  symbols; it opens no files.
- **Test consequence:** RED/GREEN construct a `QuestionIntentRegistry` via the WS10 loader on temporary
  fixtures and call the seam directly.
- **Non-goals:** No I/O, no loader duplication, no domain/`assess_response` re-implementation.
- **Change-control rule:** Adding inputs (e.g. raw response text for content matching) requires the
  deferred D7.2 decision.

### D4 — Atomic question-identity propagation — APPROVED (transient; no persistence; atomic binding)

- **Repository fact:** `get_path_n_question` returns only the served **text** and discards `question_id`
  (F1); no state field carries `question_id` (F5); WS10 §D3 forbids adding it to persistence (F10).
- **Owner decision:** Propagate an **atomically bound** served-question identity **transiently** through
  the WS11-aware serving → integration call chain. Identity, text, and design-gap MUST originate from a
  single immutable source record and never be recombined by a second lookup or reconstructed from text.
  - **D4.1 — Frozen `ServedQuestion` value object.** Introduce a **frozen immutable** internal value
    object `ServedQuestion` containing **at minimum** `question_id: str`, `text: str`, and
    `design_gap_id: str`. It is produced in **one** read step from the **same** committed source entry
    (the entry at the deterministic index `min(iterations_open, len(variants) - 1)` under the served
    gap), so its three fields are guaranteed to describe the same physical record. A new pure read-only
    producer (e.g. `get_served_question(gap_type, iterations_open) -> ServedQuestion`) reads `question_id`,
    `text`, and the parent gap key from that single entry in one pass.
  - **D4.2 — Single source of truth for the WS11 path.** The WS11-aware serving/integration path uses the
    `ServedQuestion` object end to end. The WS11 seam's `question_id` and `served_design_gap_id` (D3)
    MUST be taken from the **same** `ServedQuestion` instance that produced the displayed `text`; deriving
    either field from a separate call is prohibited.
  - **D4.3 — Backward-compatible text wrapper.** `get_path_n_question(gap_type, iterations_open)` is
    **retained only as a backward-compatible wrapper** whose return equals `get_served_question(...).text`
    for the same inputs. Its existing signature and string return type are unchanged (Path-N protected),
    but it is no longer an independent identity source.
  - **D4.4 — Prohibited bindings.** It is prohibited to (a) reconstruct or infer `question_id` from the
    question **text**; (b) perform a separate `question_id` lookup that could bind an identity to a
    different served text (e.g. an index/gap drift between two calls); (c) construct a `ServedQuestion`
    from fields sourced from more than one entry.
    **Normative:** `question_id` MUST NOT be reconstructed, inferred, derived, parsed, or matched from
    question text. The only valid `question_id` is the identifier carried by the same immutable
    `ServedQuestion` instance that supplied the served text and `design_gap_id`. Textual equality,
    normalization, translation, fuzzy matching, hashing, or reverse lookup from question text MUST NEVER
    be used to recover question identity.
  - **D4.5 — Deterministic binding invariant.** For every `(gap_type, iterations_open)` the invariant
    `get_path_n_question(gap_type, iterations_open) == get_served_question(gap_type, iterations_open).text`
    holds, and the `ServedQuestion`'s `question_id`/`design_gap_id` are the committed identity/parent-gap
    of that exact entry. This invariant is enforced by a **public test seam** (D4 RED, R10) that reads the
    committed artifact and proves ID/text/gap co-origin.
  - **D4.6 — No persistence.** The `ServedQuestion` and its `question_id` are passed transiently; they are
    **NOT** stored in `IdeaState`, `Gap`, `Evidence`, `IterationLog`, `AssertionRecord`, session, resume
    state, or persistence.
- **Rationale:** A single-read frozen value object makes ID/text/gap **atomic by construction**, removing
  any window in which a separate accessor could bind an identity to a different served text, while keeping
  the protected `get_path_n_question` return shape and touching no persistence.
- **Implementation consequence:** one new pure producer in `engine/path_n_questions.py` (its own
  later-authorized change) returning the frozen `ServedQuestion`; `get_path_n_question` becomes a thin
  wrapper over it; no separate ID-only accessor that could drift is introduced.
- **Test consequence:** RED proves the D4.5 invariant through the public seam — same `(gap_type,
  iterations_open)` yields a `ServedQuestion` whose `text` equals the wrapper's return and whose
  `question_id`/`design_gap_id` are the committed identity and parent gap of the same entry; and that no
  path reconstructs `question_id` from text.
- **Non-goals:** No persistence field, no state mutation, no change to `get_path_n_question`'s string
  return type, no ID-from-text reconstruction, no multi-entry identity assembly.
- **Change-control rule:** Persisting `question_id`/`ServedQuestion` (e.g. for history/audit durability)
  requires a separate owner-authorized persistence increment, per WS10 §D3; changing `ServedQuestion`'s
  minimum fields requires amending this decision.

### D5 — Registry fields used by evaluation — APPROVED

- **Repository fact:** The record exposes seven fields (F6).
- **Owner decision:**
  - **Determinism-influencing in v1:** `question_id` (identity/lookup) and `design_gap_id`
    (design-gap consistency check, D7.1).
  - **Audit-carried, reserved for the deferred content layer (D7.2):** `primary_intent`,
    `answer_objective`, `completion_condition` — carried into the result as audit metadata but **not**
    used to compute the v1 outcome.
  - **Audit metadata only:** `intent_id` and `source_reference` — traceability, never influencing the
    outcome.
- **Rationale:** Only identity and design-gap are deterministically checkable now; the free-text intent
  strings cannot deterministically judge a free-text response without the deferred D7.2 rules.
- **Implementation consequence:** The result carries the intent strings verbatim for audit; the outcome
  is not derived from them in v1.
- **Test consequence:** RED asserts audit fields are surfaced unchanged and that `intent_id`/
  `source_reference` never alter the outcome.
- **Non-goals:** No content matching against `answer_objective`/`completion_condition` in v1.
- **Change-control rule:** Promoting any audit-carried field to determinism-influencing requires D7.2.

### D6 — Evaluation result model — APPROVED (frozen, auditable)

- **Repository fact:** WS10 uses immutable frozen dataclasses (D21) with no free-form text.
- **Owner decision:** WS11 returns a **frozen immutable dataclass** `QuestionIntentEvaluation` with
  exactly:
  - `question_id: str`
  - `intent_id: str`
  - `design_gap_id: str`
  - `base_quality: str` — passthrough of the unchanged `assess_response` tier
  - `outcome: str` — one of the ratified vocabulary in D7
  - `matched_objectives: tuple[str, ...]` — **empty in v1** (reserved for D7.2)
  - `unmet_objectives: tuple[str, ...]` — **empty in v1** (reserved for D7.2)
  - `reason_code: str | None` — a stable code for `INVALID_INPUT`/deferred cases; `None` on a normal
    structural observation
  - Any explanatory text is a **fixed deterministic string**, never model-generated.
- **Rationale:** A frozen, enumerated result is auditable and cannot smuggle free-form AI reasoning.
- **Implementation consequence:** immutable dataclass, tuples not lists; no mutable public API.
- **Test consequence:** RED asserts frozenness, field set, empty objective tuples in v1, and enumerated
  `outcome`/`reason_code` values only.
- **Non-goals:** No free-form/AI explanation; no per-objective content verdicts in v1.
- **Change-control rule:** Adding fields or populating the objective tuples requires D7.2.

### D7 — Deterministic evaluation semantics — APPROVED (structural now; content DEFERRED as a blocker)

- **Repository fact:** `answer_objective`, `completion_condition`, and `primary_intent` are free text
  and may be bilingual (AR/EN); `assess_response` already yields a deterministic tier (F2). No
  deterministic content-matching rule exists in the artifacts.
- **Owner decision — D7.1 (defined now, deterministic):** WS11 v1 defines these deterministic, observable
  outcomes:
  - **`INVALID_INPUT`** — resolution/integrity failure (raised as a typed error per D9; not a silent
    outcome): missing/empty `question_id`; `question_id` unknown to the registry; `served_design_gap_id`
    not equal to the record's `design_gap_id`; `base_quality` not in `{ASSERTED, REASONED,
    DEMONSTRATED}`.
  - Otherwise a **structural observation** whose `outcome` is a deterministic function of the unchanged
    `base_quality` tier alone:
    - **`SATISFIED`** ≡ `base_quality == DEMONSTRATED`;
    - **`PARTIALLY_SATISFIED`** ≡ `base_quality == REASONED`;
    - **`NOT_SATISFIED`** ≡ `base_quality == ASSERTED`.
  - These outcomes describe the deterministic quality tier **bound to the specific committed question and
    its intent record** (question-aware provenance), and reuse — never re-derive or override — the
    authoritative `assess_response` classification.
- **Owner decision — D7.1.T (truthful meaning of v1 outcomes — MANDATORY):** WS11 v1 is a **question-bound
  structural evaluation observation**, not a semantic-content evaluation. The outcome vocabulary carries a
  strictly structural meaning:
  - **`SATISFIED` means only** that the existing generic response-quality tier reached `DEMONSTRATED` for
    an **authentic identified question** (a resolved `question_id` whose served `design_gap_id` matches
    the record). It **does NOT prove** semantic fulfillment of `answer_objective` or `completion_condition`,
    and it is **not** a claim that the answer's content addresses the question's objective.
  - `PARTIALLY_SATISFIED` / `NOT_SATISFIED` are likewise structural quality-tier statements
    (`REASONED` / `ASSERTED`) bound to an authentic identified question, **not** content-objective verdicts.
  - `primary_intent`, `answer_objective`, and `completion_condition` are **audit-carried metadata only**
    in v1 and MUST NOT influence the outcome unless a separately ratified deterministic rule (D7.2 / WS11.2)
    explicitly consumes them.
  - **No content-intent alignment claim** derived from these fields may be exposed to runtime, UI, logs, or
    governance evidence in v1. Any surfacing of the outcome must preserve this structural meaning (see D14).
- **Owner decision — D7.2 (DEFERRED — explicit blocker):** Deterministic **content-level** matching of a
  free-text response against `answer_objective` / `completion_condition` (populating
  `matched_objectives`/`unmet_objectives`) is **NOT definable from the current artifacts** without
  introducing NLP/AI or a new deterministic bilingual keyword/marker contract. It is therefore
  **explicitly deferred and blocked**: WS11 v1 MUST NOT emit content-derived verdicts, and
  `matched_objectives`/`unmet_objectives` remain empty. Bilingual / free-text content-intent validation
  remains deferred pending **separately ratified deterministic rules** (a later WS11.2 owner-decisions
  gate) defined **before** any implementation. **No AI, LLM, embeddings, keyword approximation, or silent
  language-specific fallback is authorized** to satisfy this — none of these may be introduced as a
  substitute for the deferred deterministic rules (D15).
- **Rationale:** This yields a genuinely deterministic, question-aware v1 observation while refusing to
  fabricate semantic judgment the artifacts cannot support deterministically.
- **Implementation consequence:** The evaluator computes `outcome` from `base_quality` and the
  design-gap consistency check only; it never inspects free-text intent content for the verdict.
- **Test consequence:** RED asserts the three tier→outcome mappings, the raised `INVALID_INPUT` cases,
  and that objective tuples stay empty; no RED asserts content matching.
- **Non-goals:** No semantic/NLP matching; no bilingual content rules in v1.
- **Change-control rule:** Enabling D7.2 requires a separate WS11.2 owner-decisions gate.

### D8 — Precedence and safety — APPROVED

- **Repository fact:** `evaluate_transition` and the `ASSERTED/REASONED/DEMONSTRATED` classification are
  deterministic and protected (F2/F4).
- **Owner decision (ratified invariants):** WS11 intent evaluation (a) **never** overrides domain safety
  rules; (b) **never** bypasses feasibility gates; (c) **never** overrides `evaluate_transition`; (d)
  leaves the existing `ASSERTED/REASONED/DEMONSTRATED` classification authoritative unless a later,
  separately-approved workstream changes it; (e) a positive intent outcome (`SATISFIED`) alone **cannot**
  close a gap or authorize a transition.
- **Rationale:** WS11 is observational (D1); deterministic protections remain the sole authority for
  progression.
- **Implementation consequence:** WS11 returns a value and mutates nothing; no call into WS11 alters
  gap/transition state.
- **Test consequence:** A protected test asserts that producing a `SATISFIED` observation does not change
  `Gap.status` or `evaluate_transition`'s result.
- **Non-goals:** No transition/gap/safety influence.
- **Change-control rule:** Any precedence change requires a new workstream authorization.

### D9 — Load and lookup failures — APPROVED (fail-loud, typed, no fallback)

- **Repository fact:** WS10 is fail-loud with typed errors and raises `QuestionIntentNotFoundError` for
  unknown IDs (F6/F7).
- **Owner decision:**
  - **Registry load failure** occurs outside the evaluator (WS10 loader) and already raises
    `QuestionIntentRegistryLoadError`; WS11 does not catch or mask it.
  - **Unknown `question_id`**: `registry.get(question_id)` raises `QuestionIntentNotFoundError` (WS10);
    WS11 propagates it, does not fabricate a record.
  - **Design-gap mismatch** (`served_design_gap_id != record.design_gap_id`) and **missing/empty active
    `question_id`**: WS11 raises a new typed `QuestionIntentEvaluationError` exposing a stable
    `reason_code` (e.g. `DESIGN_GAP_MISMATCH`, `MISSING_ACTIVE_QUESTION_ID`, `INVALID_BASE_QUALITY`).
  - No fabricated question ID, no silent fallback to generic intent, no partial-success result.
- **Rationale:** Matches WS10's strict no-fallback contract; keeps failures observable.
- **Implementation consequence:** one new typed exception; reuse WS10 exceptions unchanged.
- **Test consequence:** RED asserts each failure raises the specific typed error / `reason_code`.
- **Non-goals:** No fallback, no partial result, no swallowed exceptions.
- **Change-control rule:** New reason codes require a documented amendment to this contract.

### D10 — Backward compatibility — APPROVED

- **Repository fact:** Historical sessions carry no `question_id` (F5/F10); legacy generic evaluation
  works without it.
- **Owner decision:** The existing generic evaluation path (`assess_response`/`integrate_response`)
  remains **unchanged** for legacy/callers that have no authentic `question_id`. The WS11 seam requires an
  authentic committed `question_id` and MUST NOT pretend to be question-aware without one (it raises
  `MISSING_ACTIVE_QUESTION_ID` rather than inventing a default). Any compatibility adapter must be
  explicit and auditable (no hidden default record).
- **Rationale:** Preserves all historical behavior; prevents silent question-awareness fabrication.
- **Implementation consequence:** WS11 is only invoked when a genuine served `question_id` exists.
- **Test consequence:** RED asserts that absence of `question_id` yields the typed error, never a
  fabricated observation.
- **Non-goals:** No implicit default question, no legacy-path behavior change.
- **Change-control rule:** Any adapter for legacy inputs requires explicit documentation here.

### D11 — Audit and observability — APPROVED (no persistence in v1)

- **Repository fact:** WS10 §D3 bars new persistence for registry identity (F10).
- **Owner decision:** WS11 v1 introduces **no persistence or schema change**. The immutable
  `QuestionIntentEvaluation` result is returned to the caller; `question_id` and `intent_id` are
  traceable **within that returned result**. The **raw user response is NOT duplicated** into the result
  (only the derived `base_quality` tier is carried). No new persistence field is authorized.
- **Rationale:** Keeps WS11 stateless and within the WS10 persistence boundary.
- **Implementation consequence:** result object only; any logging is the caller's transient concern, not
  a persisted schema.
- **Test consequence:** RED asserts the result carries `question_id`/`intent_id` and does not embed the
  raw response.
- **Non-goals:** No DB, no session/resume/analytics field, no raw-response storage.
- **Change-control rule:** Persisted WS11 audit requires a separate owner-authorized persistence gate.

### D12 — Language scope — APPROVED (structural v1; bilingual semantics deferred)

- **Repository fact:** MVP is electronics/electrical; question/answer content may be Arabic while intent
  strings and code heuristics are English; no deterministic bilingual matching rule exists.
- **Owner decision:** WS11 v1 is limited to **structural/provenance determinism** (identity, design-gap
  consistency, tier passthrough — D7.1), which is language-agnostic. **Deterministic bilingual
  content-semantic matching is deferred** (tied to the D7.2 blocker). No assumption is made that
  keyword rules in one language generalize to the other.
- **Rationale:** Prevents unsound cross-language keyword inference.
- **Implementation consequence:** v1 never inspects free-text content for the verdict, so no language
  rules are needed.
- **Test consequence:** RED uses language-agnostic fixtures; no content-language assertions.
- **Non-goals:** No AR/EN content matching, no translation, no bilingual parity in v1.
- **Change-control rule:** Bilingual content rules require the D7.2 / WS11.2 decision.

### D13 — Registry responsibility boundary — APPROVED

- **Repository fact:** WS10 owns all registry parsing/validation (F7).
- **Owner decision:** WS11 (a) **consumes** a `QuestionIntentRegistry` object; (b) does **not** re-read or
  re-parse registry JSON; (c) does **not** duplicate WS10 metadata, source-equality, duplicate-ID, or
  source-reference validation; (d) creates **no second registry truth source**.
- **Rationale:** Single source of truth; no drift or double-validation.
- **Implementation consequence:** the evaluator only calls `registry.get` / `list_records`.
- **Test consequence:** RED asserts WS11 performs no file I/O and no re-validation.
- **Non-goals:** No JSON parsing, no schema, no re-validation.
- **Change-control rule:** Any WS11 read of the artifact directly is prohibited without amendment.

### D14 — Output and integration boundary — APPROVED (observation only)

- **Repository fact:** Progression state and outputs are produced by `progression_loop`/`idea_state` (F3–F5).
- **Owner decision:** WS11 v1 **only returns an observation**. It does **not** annotate user-facing
  output, change gap status, change `Evidence`, or change transition decisions. Whether/where a caller
  consumes the observation (e.g. a transient audit line) is a **minimal, separately-authorized**
  additive call site (D18), and even then it must not mutate progression state (D8).
- **Owner decision — D14.T (truthful surfacing — MANDATORY):** Any surfacing of the WS11 result MUST
  preserve its **structural** meaning (D7.1.T). No **content-intent alignment claim** — i.e. any assertion
  that the answer semantically fulfils `answer_objective`/`completion_condition` — may be exposed to
  runtime, UI, logs, or governance evidence in v1. A surfaced `SATISFIED` must be read only as "generic
  quality tier `DEMONSTRATED` for an authentic identified question", never as objective fulfilment.
- **Rationale:** Confines v1 to a pure, side-effect-free observation and prevents a structural tier from
  being mis-reported as semantic answer-correctness.
- **Implementation consequence:** the seam returns a value; the (later) call site discards it into a
  non-persisted audit channel only.
- **Test consequence:** RED/GREEN assert no state mutation and no output change.
- **Non-goals:** No UI/web, persistence, gap/Evidence mutation, or transition change.
- **Change-control rule:** Any consumption that changes user-facing output or state requires a new
  workstream authorization.

### D15 — Non-goals — APPROVED

- **Owner decision:** WS11 v1 explicitly excludes: no AI or LLM judgment; no prompt changes; no UI/web
  change; no database or persistence change; no question-content rewrite; no adaptive follow-up (WS14);
  no question reordering; no guided-answer support (WS13); no WS13/WS14 capability; **no modification to
  `engine/scoring.py`**; and no weakening of the WS9 or Path-N protections.
- **Change-control rule:** Any of these requires its own separately-authorized workstream.

### D16 — Protected-guard prerequisite — APPROVED (record only; do not amend now)

- **Repository fact:** F8 — the WS9 guard requires `engine.question_aware_evaluation` to remain absent.
- **Owner decision:** Because D2 selects `engine/question_aware_evaluation.py`, the stale WS9 absence
  guard MUST be amended in a **separate, test-only, owner-authorized gate before GREEN**. That later
  amendment removes **only** `engine.question_aware_evaluation` and **preserves**
  `engine.guided_answer_support` (WS13) and `engine.adaptive_follow_up` (WS14). The guard is **not**
  amended in this gate.
- **Rationale:** Mirrors the WS10 "Option B" separate guard-amendment gate (PR #250); avoids a red
  protected regression at GREEN.
- **Test consequence:** BASE RED (D17) does not create the module, so it does not trip the guard;
  GREEN must be preceded by the amendment gate.
- **Change-control rule:** The amendment scope is fixed to the single WS11 entry.

### D17 — RED boundary — APPROVED (seam defined; no tests written now)

- **Repository fact:** WS10's Interface-Contract / Behavioral RED discipline requires controlled failures
  (D31/D33).
- **Owner decision:** The exact observable public seam future BASE RED will exercise is
  `engine.question_aware_evaluation.evaluate_question_intent(question_id, base_quality,
  served_design_gap_id, registry)` returning a `QuestionIntentEvaluation` (D3/D6). Each future RED must
  fail through this seam, produce controlled failures (decision-tagged assertions or a single ratified
  missing-module contract failure), avoid uncontrolled import/fixture/collection errors, and leave the
  WS10 and protected suites green. **No test is written in this gate.**
- **Proposed deterministic RED matrix (design only):**

  | # | Test (proposed) | Setup | Seam exercised | Current failure | Future behavior | Governing decision |
  |---|---|---|---|---|---|---|
  | R1 | `test_module_and_seam_contract_exists` | import module, inspect signature | module + `evaluate_question_intent` | controlled missing-module RED | module + exact 4-param seam exist | D2/D3 |
  | R2 | `test_result_is_frozen_with_exact_fields` | build registry, call seam | result dataclass | controlled RED | frozen result, exact field set, empty objective tuples | D6 |
  | R3 | `test_tier_maps_to_outcome` (param DEMONSTRATED/REASONED/ASSERTED) | valid record + each `base_quality` | seam | controlled RED | SATISFIED/PARTIALLY_SATISFIED/NOT_SATISFIED | D7.1 |
  | R4 | `test_unknown_question_id_raises_not_found` | id absent from registry | `registry.get` via seam | controlled RED | `QuestionIntentNotFoundError` | D9 |
  | R5 | `test_design_gap_mismatch_raises` | served gap ≠ record gap | seam | controlled RED | `QuestionIntentEvaluationError(DESIGN_GAP_MISMATCH)` | D9 |
  | R6 | `test_missing_active_question_id_raises` | empty/None id | seam | controlled RED | `MISSING_ACTIVE_QUESTION_ID` | D9/D10 |
  | R7 | `test_invalid_base_quality_raises` | tier not in the three | seam | controlled RED | `INVALID_BASE_QUALITY` | D7.1/D9 |
  | R8 | `test_seam_performs_no_io` | audit-hook import/call probe | module import + call | controlled RED | no file/registry I/O | D3/D13 |
  | R9 | `test_observation_does_not_mutate_state` | call seam; inspect gap/transition | seam + `evaluate_transition` | controlled RED | no state/transition change | D1/D8/D14 |
  | R10 | `test_served_question_binds_id_text_gap_atomically` | `get_served_question(gap_type, iterations_open)` vs `get_path_n_question` for same inputs | `ServedQuestion` producer + wrapper | controlled RED | `ServedQuestion.text == get_path_n_question(...)`; `question_id`/`design_gap_id` are the committed identity/parent-gap of the same entry; no ID-from-text reconstruction (D4.5) | D4 |
  | R11 | `test_objective_tuples_deferred_empty` | valid call | seam | controlled RED | `matched/unmet_objectives` empty (D7.2 deferred) | D5/D7.2 |
  | R12 | `test_v1_exposes_no_content_intent_alignment_claim` | valid call; inspect result + any surfacing | seam | controlled RED | outcome is structural only; no `answer_objective`/`completion_condition` fulfilment claim surfaced (D7.1.T/D14.T) | D7.1.T/D14.T |

- **Change-control rule:** The RED matrix is a design; the authorized RED gate may refine test names but
  not the ratified seam or outcomes without amendment.

### D18 — Gate sequence — APPROVED (lean; single RED, single GREEN)

- **Owner decision — ratified WS11 sequence (each a separate explicit owner authorization):**
  1. **this owner-decisions and increment-contract document** (this gate);
  2. independent review, owner acceptance, and merge;
  3. decisions-status canonicalization (remediation plan §15 + roadmap, docs-only);
  4. **protected-guard amendment** (test-only) — only because D2 selects the new module (D16);
  5. **deterministic BASE RED** (one new test file for the D17 seam);
  6. independent review and merge;
  7. RED status canonicalization (docs-only);
  8. **one production GREEN gate** (create `engine/question_aware_evaluation.py`; the minimal transient
     accessor/call-site per D4/D14 may be included only if it remains additive and non-mutating);
  9. post-merge verification;
  10. final status synchronization and **formal WS11 closure**.
- **Rationale:** WS11 v1 has a **single behavioral surface** (a pure deterministic observation seam) — the
  genuinely independent second surface (content-semantic matching) is deferred to a future WS11.2
  increment (D7.2). Therefore **separate interface and behavioral RED/GREEN tracks are NOT created**;
  one RED and one GREEN suffice. Governance gates (1–3, 7, 10) are never merged with implementation
  gates (5, 8).
- **Change-control rule:** Splitting into two RED/GREEN tracks is authorized only if a future contract
  proves two genuinely independent surfaces exist (e.g. once D7.2 is ratified).

---

## 2. Approved vs deferred

**Approved for WS11 v1:** D1 observation-only; D2 new pure module `engine/question_aware_evaluation.py`;
D3 pure 4-parameter seam, no I/O; D4 atomic `ServedQuestion` identity binding (`question_id`+`text`+
`design_gap_id` from one immutable source entry; `get_path_n_question` retained as a text wrapper; no
ID-from-text reconstruction), transient, no persistence; D5 identity + design-gap influence, intent
strings audit-only; D6 frozen result contract; D7.1 deterministic tier→outcome + integrity failures, with
D7.1.T structural-only truthful meaning of outcomes; D8 precedence/safety invariants; D9 fail-loud typed
errors, no fallback; D10 unchanged legacy path; D11 no persistence, no raw-response duplication; D12
structural language-agnostic v1; D13 registry consumption only; D14 observation-only integration with
D14.T truthful (structural-only) surfacing; D15 non-goals; D16 recorded guard prerequisite; D17 RED seam +
matrix; D18 lean single-RED/single-GREEN sequence.

**Deferred (require separate owner authorization):** D7.2 deterministic content-level matching of
`answer_objective`/`completion_condition` (WS11.2); bilingual content-semantic rules (D12); any
persistence of WS11 results or `question_id` (D11/D4, WS10 §D3); any consumption that changes user-facing
output, gap status, `Evidence`, or transition decisions (D14); guided-answer (WS13), adaptive follow-up
(WS14), question reordering, and any change to `engine/scoring.py`.

## 3. Non-authorization (restated)

This document records decisions only. It authorizes no production code, no RED tests, no protected-guard
amendment, no status canonicalization, and no persistence/runtime/UI/prompt/AI/question-content change.
Workstream 11 remains **NOT STARTED** in the authoritative status files until its own status
canonicalization gate. Workstream 10 remains **formally closed**. `engine/scoring.py`, the WS10 registry,
`path_n_questions.py`, `progression_loop.py`, `stage3_evaluator.py`, and all tests are unchanged. Official
product state remains `DEMO_READY_WITH_LIMITATIONS`; MVP scope remains electronics/electrical-only; the AI
Coach (WS17) remains BLOCKED until Workstreams 1–16 are owner-closed. The Phase A branch remains fixed at
`57e2fac8`; PR #167 and PR #162 remain untouched. The next gate (independent review and merge of this
document, then decisions-status canonicalization) requires separate explicit owner authorization.
