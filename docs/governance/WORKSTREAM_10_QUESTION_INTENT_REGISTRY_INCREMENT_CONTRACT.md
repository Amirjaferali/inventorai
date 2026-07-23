# Workstream 10 — Question Intent Registry: Increment Contract

**Record type:** documentation-only Increment Contract for **Workstream 10 — Question Intent Registry**.
**Status:** docs-only governance record. Authorizes no implementation, no BASE RED, no tests, no registry
artifact, no loader code, no Stage 2 inventory execution, and no status canonicalization. Prepared under the
risk-based execution and review model (PR #220), on authoritative base
`228f1115eff2894443c2990436128af35f20e8ee` (Merge PR #241, Workstream 9 formal closure). This is the first
Workstream 10 gate (Contract → status canonicalization → BASE RED → implementation → HEAD GREEN → evidence →
independent reviews → owner closure); each later gate requires its own separate owner authorization.

**Provenance note (governance correction).** The initial recording of this contract
(commit `1cf2f007810d5301aa998589bae8fa5f68724ce1`) described eight scoping items as pre-existing "owner
decisions." That characterization was **not** accurate: those items were **proposals** pending owner review.
Following independent review of that commit, the owner **ratified** the decisions now stated in §1 and
directed the corrections applied in this follow-up commit. This contract therefore does **not** claim any
retroactive owner approval; it records owner-ratified decisions where the owner has ratified them, and marks
everything else as invariant, candidate, unresolved, or future proposal.

**How to read this contract — six categories.** Every substantive statement is classified as one of:
- **[RATIFIED]** — an owner-ratified decision (owner-approved after independent review; §1).
- **[INVARIANT]** — a binding WS10 contract requirement that follows directly from a ratified decision or a
  protected prior-workstream behavior.
- **[CANDIDATE]** — a proposed implementation choice, non-binding, subject to confirmation at a later gate.
- **[UNRESOLVED]** — an open item requiring inventory evidence and/or a separate owner decision before BASE
  RED or implementation.
- **[FUTURE]** — a proposal or reference for a later, separately authorized increment.
- **[CONTEXT]** — current program-status facts, true at authoring time, **not** permanent WS10 requirements.

---

## 1. Owner-ratified decisions (§1 of the ratification authorization) — [RATIFIED]

- **D1 — Initial scope.** WS10 v1 is limited to committed **Stage 2 Path N** questions only. Stage 3 is
  excluded from this first increment and remains deferred for separate analysis and owner authorization.
- **D2 — Separate registry boundary.** The Question Intent Registry must remain **separate** from the
  committed Path N question-content artifact. The existing question-content artifact remains the source of
  truth for question **text**, the **question identity already recorded there**, and **serving order**. The
  future registry will be the governed source of truth **only for question design-time intent**. The exact
  final artifact path and file format remain subject to confirmation before implementation.
- **D3 — No persistence in WS10 v1.** WS10 v1 introduces **no** persistence changes. No `question_id`,
  `intent_id`, or related registry data is added to `IterationLog`, `AssertionRecord`, `AcknowledgedUnknown`,
  session persistence, resume state, or analytics. Any future persistence requirement requires a separately
  owner-authorized increment and is **not** automatically assigned to WS11.
- **D4 — Design-time intent only.** WS10 defines only the **design-time intent** of a committed question —
  what the question was designed to elicit. WS10 must **not** infer, record, or reconstruct **user-expressed
  intent** from `gap_targeted`, `gap_context`, engine-selected gaps, interaction history, transcripts,
  fixtures, user answers, or persisted state.
- **D5 — Language boundary.** No Arabic question content, translation, or bilingual-parity implementation is
  authorized in WS10 v1. The future design must not unnecessarily prevent later language support, but no
  complete multilingual schema or localization architecture is designed under this contract gate.
- **D6 — Evaluation boundary.** WS10 may define and validate question design-intent identity, governed
  metadata, and coverage. WS10 must **not** implement or define answer scoring, correctness judgments,
  evaluation rubrics, evaluator mappings, adaptive sequencing, question reordering, or runtime user-intent
  inference. Question-aware evaluation remains outside WS10. The authoritative scope and activation
  conditions of WS11 must be confirmed separately from the remediation records before WS11 begins.
- **D7 — Future loader location.** `engine/question_intent_registry.py` may be recorded **only as a
  candidate** location; it is not an approved or binding implementation path. The final loader location and
  implementation mechanism are decided during a separately authorized implementation-design gate.
- **D8 — Minimum record concept.** The proposed minimum record concept may be retained (see §5), but the
  enumerated sub-items in §7 remain **unresolved** and must not be silently finalized by this contract.

## 2. Problem statement — [INVARIANT context of the problem]

There is no single, governed, machine-readable source of truth that declares, per committed Stage 2 question,
its **design-time intent** — the one thing the question is built to elicit — with governed identity,
provenance, and lifecycle. Stage 2 Path N entries carry only `{question_id, text}` and no declared intent,
answer objective, or completion condition; they are served positionally. Workstream 9 guaranteed single-intent
question *content* but recorded each question's intent only as prose, not as governed, queryable data. WS10
defines the registry that makes each committed Stage 2 question's design-time intent explicit, identity-bearing,
and governed — as a descriptive layer over already-committed content — without changing question text, serving
selection or order, evaluation, persistence, or user-facing behavior.

## 3. Semantic boundary — design-time intent vs user-expressed intent — [INVARIANT, from D4]

**Design-time question intent** is what a committed question is intended to elicit, authored **only** from the
committed final question text, the Workstream 9 single-intent definition, the question's committed design gap
where evidence supports it (§6/C11), and current normative governance documents. It MUST NOT be derived from or
conflated with **user-expressed intent**, and MUST NOT draw any value from `gap_targeted`, runtime
`gap_context`, engine-selected gaps, fixtures, transcripts, interaction history, user answers, or persisted
state (WS8 §6). User-expressed-intent capture and all intent-aware runtime behavior remain deferred and
separately owner-gated. This contract neither reopens nor re-scopes Workstream 8 or Workstream 9. The authored
intent taxonomy is **new normative data** requiring owner review before any BASE RED or implementation.

## 4. Single design-time intent definition — [INVARIANT, from WS9 §3]

Consistent with Workstream 9 §3, a registered question is expected to have exactly one design-time intent:
one primary user decision or information request; one answer objective; one observable completion condition;
one committed design-gap association where supported; and no hidden secondary task. Whether a specific
committed question satisfies this is a **semantic** determination (see §6), not solely a machine check.

## 5. Registry identity and proposed minimum record concept — [CANDIDATE + UNRESOLVED]

**[CANDIDATE]** The registry is proposed to be keyed by the committed Stage 2 `question_id`, with each record
proposing at minimum the following fields:

| Field | Proposed meaning | Classification |
|-------|------------------|----------------|
| `question_id` | stable cross-reference for a committed question **within the applicable registry version** (C8) | [CANDIDATE] |
| `intent_id` | identifier for the design-time intent — **semantics unresolved** (C9) | [UNRESOLVED] |
| `stage` | journey stage; `2` for WS10 v1 | [CANDIDATE] |
| `design_gap_id` | the question's committed design gap, recorded **only where directly supported** by the committed artifact or normative evidence (C11) | [CANDIDATE] |
| `primary_intent` | the single decision/information the question is designed to elicit | [CANDIDATE] |
| `answer_objective` | what a complete answer provides | [CANDIDATE] |
| `completion_condition` | the observable "done" condition | [CANDIDATE] |
| `source_reference` | provenance to the committed question text / normative source — **format deferred** (C12) | [CANDIDATE] |
| `status` | record lifecycle status — **allowed values/meanings/transitions unresolved** (C10) | [UNRESOLVED] |

**[INVARIANT]** Whatever the final shape, the registry record MUST NOT include `user_intent`, `gap_targeted`,
any transcript-derived data, evaluation rules, scoring, persistence mappings, or adaptive sequencing.

**[UNRESOLVED]** The following must not be silently finalized by this contract and require Stage 2 inventory
evidence and later owner decisions:
- **C8 — `question_id`:** it is the stable cross-reference **within the applicable registry version**; it is
  **not** asserted as absolutely immutable without lifecycle qualification. Rename, replacement, retirement,
  deletion, and migration rules remain unresolved owner decisions.
- **C9 — `intent_id`:** its semantics are unresolved. This contract does **not** decide whether it is
  one-to-one with a question, reusable across questions, a taxonomy identifier, or a record identifier; that
  is determined after the Stage 2 inventory.
- **C10 — `status`:** retained as a proposed field only; allowed values, meanings, and transitions are
  unresolved. `active` is **not** an approved lifecycle model.
- **C11 — `design_gap_id`:** it is **not** assumed that every question already has one unambiguous committed
  design-gap mapping. It may be recorded only where directly supported by the committed question artifact or
  normative governance evidence; ambiguous mappings must be surfaced for owner review and must never be
  inferred from runtime or user-state fields.
- **C12 — `source_reference`:** provenance is required, but the exact format is deferred (file path, JSON
  pointer, document section, commit reference, or multiple references — undecided here).

## 6. Structural validation vs semantic governance review — [INVARIANT boundary; mechanism UNRESOLVED]

WS10 distinguishes two separate concerns:
- **Structural validation** (machine-checkable) may include: missing required fields; malformed values;
  duplicate identifiers; missing or orphan question records; coverage mismatches.
- **Semantic governance review** (human/owner judgement) includes: whether the authored intent faithfully
  represents the question; whether the question has one primary design intent; whether `answer_objective` is
  accurate; whether `completion_condition` is appropriate; whether a design-gap association is justified.

This contract does **not** claim that all semantic violations can or must be detected automatically at loader
time. The exact validator architecture, exception types, and the timing of each check are **[UNRESOLVED]** and
deferred to the implementation-design gate.

## 7. No silent fallback — [INVARIANT principle; mechanism UNRESOLVED]

Missing or malformed required records MUST NOT silently fall back to a generic or default intent; such a
condition must be surfaced, not masked. The specific exception classes, validator architecture, and the exact
failure timing (load-time vs review-time) are **[UNRESOLVED]** and are not finalized under this contract.

## 8. Registry boundary, provenance, and versioning — [INVARIANT principles; specifics UNRESOLVED]

- **[INVARIANT, from D2]** The registry is a **separate** governed artifact from the Path N content JSON; the
  content JSON remains the source of truth for question text, recorded question identity, and serving order,
  and MUST NOT be annotated or modified. The registry is the governed source of truth only for design-time
  intent.
- **[CANDIDATE]** `docs/governance/question_intent_registry/` is recorded as a **candidate** location and file
  format, subject to confirmation before implementation; it is not an irreversible architectural commitment.
- **[INVARIANT principle, specifics UNRESOLVED — C3]** The registry must carry **governed provenance and
  lifecycle metadata in principle**. The exact governance-metadata field set and format (e.g. any
  `source/license/owner/review_date/version/deprecation_status` shape) are **not** binding and remain
  unresolved pending inventory and implementation design.
- **[INVARIANT principle, specifics UNRESOLVED — C4]** An **explicit versioning and lifecycle policy** must be
  defined and owner-approved before implementation. This contract imposes **no** binding requirement for a
  specific top-level `schema_version` model, semver, ISO-date validation, or enumerated deprecation values.
- **[INVARIANT principle, mechanism UNRESOLVED — C5]** Any future loader must expose **read-only** behavior to
  consumers; the implementation mechanism (for example `MappingProxyType`) is a non-binding candidate and is
  deferred.

## 9. Language extensibility — [INVARIANT, from D5]

No Arabic content or translation is authorized here; Arabic/English parity remains conditional while no
committed Arabic variants exist. The future design should not unnecessarily preclude later language support,
but no complete multilingual schema or localization architecture is designed under this gate. The concrete
language model is **[UNRESOLVED]**.

## 10. Persistence exclusion — [INVARIANT, from D3]

No persistence changes are permitted in WS10 v1 (see D3 for the exact excluded surfaces). Resumed-session
serving behavior is unchanged. Any future persistence requirement is a separately owner-authorized increment
and is not automatically assigned to WS11.

## 11. WS11 evaluation boundary — [INVARIANT, from D6]

Evaluation is outside WS10 (see D6). This contract does **not** finalize WS11 architecture or activation
conditions. **Workstream 11 remains NOT STARTED**, and its authoritative scope and activation conditions must
be confirmed from the authoritative remediation records before any WS11 authorization.

## 12. Protected behavior (behavior-level, not file-level) — [INVARIANT]

WS10 protects **behavior**, not a fixed list of untouchable implementation files. The following must not
regress:
- committed **question text**;
- **question identity** as already recorded in the content artifact;
- **serving selection** and **serving order**;
- **persistence behavior** (no change per D3);
- prior-Workstream behavior: WS1 Evidence Lock immutability; WS2 safety-signal extraction; WS3 hygiene; WS4
  criticality; WS5 unified risk/safety; WS6 requirement landscape; WS7 validation plan; WS8 no-user-intent
  reconstruction; WS9 single-intent content and deterministic serving.

Any future integration change **outside** the registry and its loader requires separate owner review and
justification; it is not authorized by this contract.

## 13. Future Stage 3 extension (reference only) — [FUTURE]

Stage 3 questions declare `Q-ID`, `Question Type` (PRIMARY / CONDITIONAL_PROBE), and a `Primary Evidence
Target` in `STAGE3_QUESTION_SET.md`. A future, separately authorized Stage 3 analysis **may use
`Primary Evidence Target` as one governed source** when authoring design-time intent; **equivalence must not
be assumed** (the Primary Evidence Target is not, by itself, the design-time intent). No Stage 3 registration,
validation, transcription, or editing is authorized by this contract.

## 14. Candidate BASE RED seams (NOT AUTHORIZED — no tests created) — [FUTURE]

Recorded as future design intent only; no test is created and BASE RED is not authorized. These are
**structural** seams (§6) and assume the §5/§7/§8 items are resolved first:
- **S1** loader / registry artifact absent → import/assertion fails;
- **S2 (coverage)** every committed Stage 2 `question_id` has exactly one registry record and vice versa;
- **S3 (single primary intent, structural)** each record declares exactly one `primary_intent` field;
- **S4 (identity)** registry `question_id` set equals the committed content id set; no orphan/missing;
- **S5 (no user-intent)** no field is sourced from persisted answer/selection/runtime state;
- **S6 (protected serving)** serving selection and order are unchanged with the registry present.

Semantic faithfulness (§6) is **not** claimed to be an automatable BASE RED assertion.

## 15. Risks and unresolved decisions (must be resolved before BASE RED / implementation) — [UNRESOLVED]

- complete **Stage 2 inventory** has not yet been performed (not authorized here);
- duplicate or missing question IDs have not yet been independently scanned;
- conditional-question behavior in Stage 2 has not yet been established;
- whether Stage 2 surfaces exist **outside Path N** has not yet been confirmed;
- `intent_id` semantics (C9);
- `status` lifecycle and allowed values (C10);
- `source_reference` format (C12);
- registry artifact format and exact path (D2/C2);
- versioning and lifecycle model (C4);
- governance-metadata shape (C3);
- `question_id` rename / retirement / deletion / migration policy (C8);
- structural-validation vs semantic-review split and validator mechanism/exception types/timing (C6/C7);
- future language model (D5/§9);
- Stage 3 `Primary Evidence Target` mapping and non-equivalence (C13);
- any future persistence requirements (D3).

## 16. Current-status context (NOT permanent WS10 requirements) — [CONTEXT]

The following are program-status facts true at authoring time and are recorded as context only; they are
**not** permanent WS10 schema or behavioral invariants:
- the current known **31-failure** `tests/test_domain_registry.py` baseline;
- official product state `DEMO_READY_WITH_LIMITATIONS`;
- current MVP scope (electronics/electrical-only);
- the AI Coach (WS17) is currently BLOCKED until Workstreams 1–16 are owner-closed;
- the Phase A branch is currently fixed at `57e2fac8`; PR #167 and PR #162 are currently untouched;
- the authoritative base for this contract is `228f1115` (Merge PR #241).

## 17. Explicit non-authorization clause — [INVARIANT]

This contract is documentation-only and authorizes **no** downstream action. It does not authorize: push;
Draft PR creation; merge; status canonicalization; Stage 2 inventory execution; BASE RED; tests; registry JSON
or any registry artifact; loader code; production code; schema/database changes; persistence; UI; evaluator;
prompts or AI logic; analytics; question-content changes; Stage 3 changes; Workstream 11 work; or any later
Workstream. Workstream 10 implementation and BASE RED remain **UNAUTHORIZED**; Stage 2 inventory remains
**UNAUTHORIZED**; status canonicalization remains **UNAUTHORIZED**; Workstream 11 remains **NOT STARTED**.
Each later Workstream 10 gate requires its own separate explicit owner authorization.
