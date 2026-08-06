# DEMO EVIDENCE FINDINGS — POST-PR #97

Status: `DOCUMENTATION-ONLY EVIDENCE RECORD — NON-ACTIVATING`
Scope: records owner-observed demo findings and future non-activating candidates.
Authorizes: NOTHING. No implementation, Increment Contract, MVP activation, or
repository change of any kind is authorized by this document.

This record exists so future agents do not lose the owner-observed demo
findings, the distinction between existing question-level clarification and the
missing answer-level clarification feature, and the current improvement
priorities. It records evidence and candidates only.

---

## 1. Current official state

- Repository: `Amirjaferali/inventorai`
- Authoritative branch: `feature/atomic-json-session-persistence`
- Verified official tip: `9fc30f0cca4aaea41a248a190db4197118f8ae0f`
- Latest merged PR: #97
- Official state: `DEMO_READY_WITH_LIMITATIONS`
- No implementation authorized.
- No Increment Contract authorized.
- No `main` synchronization authorized.
- Structured Owner Criticality Capture remains a FUTURE NON-ACTIVATING MVP
  candidate only (see §6.I).

---

## 2. Existing clarification material (preserve — do not overwrite)

The repository already contains clarification material, and it is
**question-level clarification only**. It helps the owner understand the
current question *before* answering; it does not rewrite, improve, or approve
owner answers.

Implemented through:

- `web/clarification_labels.py` — `get_clarification(gap_type)` → deterministic,
  display-only per-gap explanation of the current question
  (`label`, `plain_language`, `information_needed`, `answer_shape`,
  `support_hint`).
- `web/responsibility_labels.py` — `get_responsibility(gap_type)`, advisory,
  display-only per-gap responsibility guidance.
- `web/templates/session.html` — the "Help me understand this question"
  expander that renders the clarification content, plus the responsibility
  guidance block.
- `web/app.py` — render-time wiring only (`current_clarification`,
  `current_responsibility`); never stored, never affects scoring, maturity,
  gates, the transcript, the deliverable, or persistence.
- Increment 1B tests: `tests/test_increment_1b_clarification_routing.py`,
  `tests/test_increment_1b_responsibility_guidance.py`.

Character of the existing material:

- It is display-oriented question guidance.
- It does NOT rewrite, suggest, or approve owner answers.
- It must be **preserved and not semantically overwritten** by any future
  answer-level feature. Any new answer-clarification concept must be clearly
  distinguished from this Increment 1B question-level clarification and must
  inherit its established boundaries (display-only, no LLM, never inventing owner
  answers, no scoring/gate/maturity/persistence effect).

---

## 3. Missing owner-proposed feature — Inventor Answer Clarification / Improve Wording Assistant

Status: FUTURE NON-ACTIVATING CANDIDATE — BACKLOG-DOCUMENTED, NOT IMPLEMENTED,
NOT ACTIVATED. Not authorized.

A strict read-only diagnostic confirmed this feature does NOT exist as
implemented runtime behavior, schema/session state, UI flow, tests, or activated
product capability (no answer clarification assistant, no improve-wording
assistant, no rewrite/rephrase answer feature, no pre-save assistant, and no
`original_user_answer` / `suggested_clarified_answer` / `user_approved_answer` /
`clarification_status` fields or owner-approved clarified-answer flow in the
runtime, schema, session, or UI).

A pre-existing product backlog note DOES exist and is preserved:
`docs/product/INVENTOR_ANSWER_CLARIFICATION_FEATURE_BACKLOG.md`. This PR #98
evidence record does NOT replace that backlog; it preserves the post-PR97 demo
evidence and reclassifies/prioritizes the concept as a future non-activating
candidate based on the observed demo issues, adding governance prioritization
only. The feature remains NOT authorized and requires a separate owner scope
decision, Increment Contract, tests, review, and owner-authorized true merge
before any implementation.

Three states must be kept distinct and not conflated:

- existing Increment 1B **question-level** clarification — implemented,
  display-only (see §2);
- the pre-existing **answer-clarification backlog documentation**
  (`docs/product/INVENTOR_ANSWER_CLARIFICATION_FEATURE_BACKLOG.md`) — a
  documentation note only, not a runtime capability;
- the **missing runtime implementation / activation** of the answer-level
  assistant — not present as runtime behavior, schema/session state, UI flow,
  tests, or activated product capability.

### Description

An optional pre-save assistant that helps the inventor clarify their **own**
answer after drafting it and before saving it. It operates on the user's answer
(distinct from Increment 1B, which explains the question).

### Required behavior (future design boundaries)

- It may identify missing dimensions in the drafted answer.
- It may ask targeted follow-up clarification questions.
- It may suggest a clearer wording of the user's own answer.
- It must preserve the user's original meaning.
- It must require user approval before any clarified wording is saved.
- It must never silently replace the original answer.

### Required prohibitions

- Must not add new facts.
- Must not add new components.
- Must not add numbers.
- Must not add engineering certainty.
- Must not add validation, readiness, safety, feasibility, patentability, or
  buildability claims.
- Must not generate risks from prose.
- Must not infer criticality.
- Must not convert uncertainty into certainty.
- Must not act as invention completion.

### Future data separation (illustrative — not a schema authorization)

- `original_user_answer`
- `suggested_clarified_answer`
- `user_approved_answer`
- `clarification_status`

### Allowed future clarification statuses (illustrative)

- `original_saved`
- `clarification_suggested`
- `owner_approved`
- `owner_rejected`
- `needs_more_owner_input`

### Governance status

- Future candidate only.
- Not implemented.
- Not authorized.
- Requires a separate owner scope decision, Increment Contract, tests, review,
  and owner-authorized true merge before any implementation.

---

## 4. Demo evidence summary

### Demo 1 — Smart Livestock Collar

- Reached Level 2.
- Demonstrated idea-clarity value.
- Preserved advisory / "not technically verified" framing.
- Exposed observations: report length, repeated references, criticality
  undetermined, and test-plan repetition.

### Demo 2 — Gas Cylinder Low-Level Warning Device

- Reached Level 2.
- Demonstrated value for transforming a plain household problem into structured
  invention reasoning.
- Preserved plain-language mechanism wording such as "small thinking part" and
  "holder feels the weight."
- Exposed the need for owner-confirmed engineering vocabulary suggestions.

### Demo 3A — Elderly appliance-left-on alert device (natural lay wording)

- Rejected by the domain gate on the official tip.
- An explicit electronics/electrical idea was refused despite the owner's
  confirmation checkbox.
- A read-only diagnostic confirmed a deterministic classifier limitation:
  - the word "monitoring" matched a `medical_device` classification signal;
  - the natural lay wording contained no electronics component signal
    (e.g. circuit, sensor, voltage, current, microcontroller);
  - the explicit confirmation checkbox did not override a conflicting
    supported-domain classification (by design: `infer_domain` returned
    `medical_device`, which is in the conflicting supported set, so `/start`
    refused with the unsupported-domain message).
- Classification: **Domain Gate / Entry UX Limitation.**

### Demo 3B — Same idea with mechanism-explicit wording

- Passed the domain gate only after adding technical terms such as
  "current sensor," "microcontroller," and "wifi alert."
- This workaround must be documented separately from the natural lay wording
  case (3A): needing specialist-style keywords to enter is itself the limitation
  for a non-specialist (Path N) owner.
- After entering the session flow, the app repeatedly returned
  "More detail needed" after detailed owner answers to:
  1. step-by-step mechanism;
  2. safe working conditions / needed confirmation;
  3. boundaries / when it should and should not work.
- Deterministic cause (read-only diagnostic): `assess_response` scores
  plain-language answers as `ASSERTED` (the generic-verb trap penalizes natural
  verbs such as "detects"/"sends" unless paired with a fixed causal-structure
  keyword), so gaps remain `PARTIAL`; this is compounded by a two-`REASONED`
  answers-per-gap close requirement, and the "More detail needed" (WARN) message
  does not name the missing dimension.
- Classification: **Repeated More Detail Needed Loop / Feedback UX Limitation.**

---

## 5. Owner-observed critical finding

The current app can block a non-specialist user before value is delivered:

- first at the domain gate, because natural wording lacks technical keywords; and
- then inside the session, because "More detail needed" does not explain the
  missing answer dimension.

This finding is preserved as valid demo evidence about the current product's
non-specialist (Path N) entry and feedback experience. It authorizes no fix.

---

## 6. Required improvement candidates (future, non-activating only)

None of the following is authorized. Each is a candidate for a future,
separately owner-authorized scope decision and Increment Contract.

### A. Domain Gate / Entry UX Improvement

- Valid electronics/electrical ideas should not be rejected only because the
  owner uses lay wording.
- The relationship between explicit owner confirmation and classifier conflict
  needs future design review.
- Ambiguous generic words such as "monitoring" should not overpower explicit
  owner intent without clearer guidance.
- No fix is authorized by this document.

### B. More Detail Needed Feedback / Guided Answer Scaffolding

- "More detail needed" should explain what is missing.
- Possible missing dimensions: mechanism sequence; part/function mapping;
  operating boundary; assumption; unknown; evidence; safety limitation.
- Future guidance may include short checklists, but no implementation is
  authorized now.

### C. Inventor Answer Clarification / Improve Wording Assistant

- New future candidate (see §3 for full description, behavior, prohibitions, and
  data separation).
- Must be distinguished from the existing Increment 1B question-level
  clarification.
- Must preserve `original_user_answer` and require owner approval before saving
  any clarified answer.

### D. Owner-Confirmed Engineering Translation Layer

- Future feature only.
- Suggests possible engineering vocabulary for plain-language wording.
- Must preserve original wording.
- Must require owner confirmation.
- Must not treat suggestions as verified facts.

### E. Deliverable Readability / Reference Compaction

- Reduce repeated long text in the Requirement Landscape.
- Use references such as `EV-001`, `UNK-001`, `ASM-001` where appropriate.
- Preserve traceability.

### F. EV Summary Ellipsis / Apparent Truncation Diagnostic

- Determine whether the ellipsis is an intended summary, UI truncation, a copy
  artifact, or an actual data edge issue.

### G. Prototype & Test Plan Diversity

- Improve coverage across stated unknowns, essential assumptions, and leading
  mechanism claims.
- Do not turn proposals into validation results.

### H. Risks Section / Owner-Stated Risk Capture

- The current risks section can be weak or generic.
- Do not generate risks from prose automatically.
- Future safer path: ask the owner what could go wrong, then record
  owner-stated risks.

### I. Structured Owner Criticality Capture

- Remains a FUTURE NON-ACTIVATING MVP candidate only.
- Do not implement or infer criticality from prose.
- Any future version must ask the owner explicitly whether a requirement is
  Essential, Adjustable, Optional, or Unknown.

### J. Registry Hygiene

- Observed runtime warning:
  `domain_registry: skipping domains/iot_electronics/domain.json
  (schema_version=None, expected '1.0')`.
- The diagnostic found this was NOT the direct cause of the Demo 3A rejection
  (that was the `medical_device` classification), but it remains a registry
  hygiene issue: a domain pack with an invalid `schema_version` is silently
  excluded from the registry.

---

## 7. Priority recommendation (by current demo evidence)

1. Domain Gate / Entry UX Improvement
2. More Detail Needed Feedback / Guided Answer Scaffolding
3. Inventor Answer Clarification / Improve Wording Assistant
4. Deliverable Readability / Reference Compaction
5. EV Summary Ellipsis Diagnostic
6. Prototype & Test Plan Diversity
7. Owner-Confirmed Engineering Translation Layer
8. Owner-Stated Risk Capture
9. Structured Owner Criticality Capture
10. Registry Hygiene

This ranking is advisory evidence-based prioritization only. It authorizes no
work and confers no scope.

---

## 8. Governance status

- This document records evidence and candidates only.
- It does not authorize implementation.
- It does not authorize MVP activation.
- It does not authorize an Increment Contract.
- It does not authorize code, schema, UI, runtime, template, persistence, or
  test changes.
- Any future implementation must proceed through, in order:
  1. owner scope decision;
  2. Increment Contract;
  3. implementation branch;
  4. tests;
  5. review;
  6. owner-authorized true merge.
