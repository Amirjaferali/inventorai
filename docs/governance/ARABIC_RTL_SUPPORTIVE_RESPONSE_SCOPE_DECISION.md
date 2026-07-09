# Arabic / RTL Supportive Response — Scope Decision

Status: SCOPE DECISION ONLY — FUTURE OWNER-GATED CANDIDATE — NO IMPLEMENTATION AUTHORIZED

## 1. Purpose

This document admits a future candidate increment — **Arabic / RTL Supportive
Response** — arising from a documented demo-readiness finding. It is a
governance scope decision only. It authorizes no implementation, no source
change, no test change, no template change, no roadmap sync, and no merge of
any code. It records what the candidate is, why it is worth considering, what
it would and would not cover, and the separately owner-gated sequence any
future work must follow.

## 2. Evidence basis

- A strict **read-only demo-readiness / user-journey integrity check** was
  performed after the closure of the Advisory Panel Precedence / Supportive
  Surface Consolidation lineage (latest merged PR #145; authoritative tip
  `cfd7d48afae1d350ae55898619bf6b3b1e5ed98b`).
- That check found the consolidated supportive UX **demo-ready within stated
  limitations**: the one-primary-panel precedence holds per state, truthful
  surfaces are preserved, answers are saved verbatim, the six honest actions
  are intact, and the electronics/electrical domain gate holds. **No BLOCKER or
  HIGH issue was found.**
- One **MEDIUM** finding was recorded: Arabic uncertainty text such as
  "لا أعرف" is **detected correctly** and **triggers the uncertainty support
  panel**, but the supportive **response copy renders in English and the page
  layout remains LTR**, with **no `dir="rtl"` and no `lang="ar"`**. An
  Arabic-speaking inventor who signals uncertainty in Arabic is met with an
  English, left-to-right supportive response.
- This is **not a demo blocker**. It is an acceptable, documented limitation
  under the current official state `DEMO_READY_WITH_LIMITATIONS`.
- Addressing it would require this separately owner-gated scope decision before
  any implementation may be considered.

## 3. Product rationale

- Arabic / RTL support for the supportive response would improve **trust and
  usability** for Arabic-speaking inventors, meeting them in their own language
  and reading direction at the exact moment they express uncertainty.
- It directly supports the established **supportive, non-exam UX principle**:
  the product should feel like a supportive idea-development assistant, not an
  exam-like evaluator, and should not become a dead end when an inventor is
  unsure.
- It should be treated as a **deliberate i18n / supportive-response candidate**,
  scoped and reviewed on its own merits — **not** as a quick wording patch to
  the existing English template, because directionality, localized copy, and
  input-conditioned rendering are architectural concerns that warrant their own
  review.

## 4. Scope admitted as a FUTURE candidate only (NOT authorized)

The following are recorded as the possible future scope of this candidate.
Recording them here **does not authorize any of them**; each remains subject to
the sequence in Section 6.

- Arabic supportive-response **copy** for the uncertainty support surface.
- **RTL rendering** where Arabic input or Arabic-derived state is active.
- Arabic-facing **labels / help** where directly tied to the supportive
  uncertainty response.
- **Preservation of user authorship** and the **verbatim saved answer** in all
  cases (a non-negotiable boundary carried into any future work).

## 5. Explicitly OUT OF SCOPE

The following are explicitly excluded from this candidate and from any future
increment derived from it:

- Full product **localization**.
- Broad **translation of all pages**.
- A general **multilingual framework**.
- **Answer Clarification / Improve Wording** (remains separate and inactive).
- **Answer rewriting**.
- **Generated Arabic answer suggestions**.
- Any **save / approve / apply clarified-answer flow**.
- **Schema / scoring / persistence / session transcript / deliverable / report**
  behavior changes.
- **Safety Signals** reopening.
- **Domain expansion** beyond electronics/electrical.
- **Production-readiness** claims.

## 6. Required future sequence

Any implementation of this candidate would require, in order, each as a
separate, explicit, owner-gated step:

1. Separate owner authorization.
2. Read-only source review.
3. Increment contract.
4. Implementation PR.
5. Independent review.
6. Owner-gated true merge.
7. Manual demo evidence.
8. Roadmap sync.

This document performs **none** of these steps and authorizes **none** of them.

## 7. Boundary preservation

- Official state remains `DEMO_READY_WITH_LIMITATIONS`.
- MVP remains **electronics/electrical-only**.
- **Answer Clarification / Improve Wording** remains inactive.
- **Safety Signals** remain closed.
- **Saved answers** must remain **verbatim**.
- The **inventor remains the sole author** of any saved answer.
- `main` remains `0e89e4636399760965c9ff8086b465c90dbadf8e` and is not
  synchronized by this decision; the frozen persistence lane remains
  `PRESERVE UNMODIFIED AND PAUSE` at
  `aec9cf6409efc18e125b6745762002f59e529654`; the quarantined scratch branch
  remains untouched at `02586747c902d5e1ebb78adde54ddd4ecd1c174a`.

## 8. Final classification

`ARABIC / RTL SUPPORTIVE RESPONSE SCOPE DECISION CREATED — FUTURE CANDIDATE ONLY — NO IMPLEMENTATION AUTHORIZED`
