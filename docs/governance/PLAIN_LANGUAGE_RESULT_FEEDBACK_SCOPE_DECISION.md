# Plain-Language Result Feedback — Scope Decision

Status: SCOPE DECISION ONLY — FUTURE OWNER-GATED CANDIDATE — NO IMPLEMENTATION AUTHORIZED

## 1. Decision

Admit **Plain-Language Result Feedback** as a **future candidate only**. This is a
governance scope decision; it authorizes no implementation, no source change, no
test change, no template change, no roadmap sync, and no merge of any code.

## 2. Problem statement

A read-only current product / demo gap diagnostic (performed at authoritative tip
`808f8de953285147ca90553d9e9940e58593a814`, after PR #152) found one MEDIUM
user-facing gap: the current session feedback can expose **raw engine-internal
reason text** to the user, for example:

    MECHANISM_COMPLETENESS asserted only — reasoning required

The diagnostic traced this to:

- `engine/progression_loop.py` producing raw engine/scoring reason text of the
  form `"{gap_type} asserted only — reasoning required"`; and
- `web/templates/session.html` rendering `last_result.get('reason')` directly to
  the user (the primary WARN/PASS/BLOCK feedback line).

This weakens the supportive, non-exam demo experience because the user sees
internal scoring vocabulary (an all-caps gap-type token) instead of a
plain-language explanation. It affects all users, not a language subset.

## 3. Product rationale

This candidate supports the owner's primary objective: **development of the idea,
not development of the inventor.** It should make feedback easier to understand —
without writing answers for the user, without changing the score, and without
hiding the truth. It is a supportive-UX clarity improvement, not a scoring or
content change.

## 4. Scope (future candidate — NOT authorized)

Future work may introduce a **display-only helper / presentation layer** that maps
raw result reasons into user-friendly explanation text for the **visible session
feedback line**. Recording this scope here authorizes none of it; each step
remains subject to the governance path in Section 12.

## 5. Required preservation

The **raw authoritative engine/scoring reason must remain preserved and available
internally.** The friendly text must be **display-only** and must **not** replace
the raw reason in scoring, persistence, reporting, benchmark, replay, transcript,
or deliverable logic unless a later, separately authorized contract explicitly
allows it.

## 6. Required boundaries

- Display-only future candidate.
- Raw engine/scoring reason must remain preserved.
- No change to `score_case()`.
- No change to scoring criteria.
- No change to stage transitions.
- No change to gap detection.
- No change to domain gate.
- No change to persistence / session store.
- No change to transcript behavior.
- No change to deliverable / report behavior.
- No hiding of WARN / PASS / BLOCK.
- No hiding of failed criteria.
- No false softening that implies readiness, validation, safety, compliance,
  feasibility, or patent-readiness.
- No Answer Clarification / Improve Wording.
- No answer rewriting.
- No generated answer suggestions.
- No Safety Signals reopening.
- No full localization / i18n.
- Saved user answers remain verbatim.
- The inventor remains the sole author.
- Official state remains `DEMO_READY_WITH_LIMITATIONS`.
- MVP remains electronics/electrical-only.

## 7. Why this is higher priority than more localization

Arabic / RTL Supportive Response has just been closed as a narrow
uncertainty-panel improvement. The current higher-value issue is **not** language
coverage; it is the raw engine/scoring jargon appearing in the **main feedback
line for all users**.

## 8. Why this is safer than Answer Clarification

Answer Clarification is answer-adjacent and could risk rewriting or influencing
the user's answer. Plain-Language Result Feedback is safer because it **only
explains system feedback in friendlier wording** while preserving the raw score
reason and keeping user answers verbatim. It never touches, suggests, or rewrites
the inventor's answer.

## 9. Why this starts as a scope decision

The feedback line is connected to **authoritative scoring output.** Therefore,
governance must first define the boundary between display-friendly explanation and
raw scoring truth **before** any source review, increment contract, or
implementation. This scope decision establishes that the raw scoring reason is
preserved and that WARN/PASS/BLOCK and failed criteria are never hidden or falsely
softened, consistent with the repository's Reporting Integrity Rules.

## 10. Explicit non-goals

- Do not change engine scoring.
- Do not change stage progression.
- Do not change gap logic.
- Do not change persistence.
- Do not change reports or deliverables.
- Do not activate Answer Clarification.
- Do not reopen Safety Signals.
- Do not generate or rewrite inventor answers.
- Do not claim readiness, feasibility, compliance, safety, or patentability.
- Do not expand domain scope.
- Do not sync `main`.

## 11. Expected future governance path

Each step is separately owner-gated; this scope decision performs and authorizes
none of them:

1. Scope decision PR (this document).
2. Roadmap sync PR.
3. Read-only source review.
4. Increment contract PR.
5. Roadmap sync PR.
6. Implementation PR.
7. Independent implementation review.
8. Owner-gated true merge.
9. Manual demo evidence PR.
10. Roadmap sync PR.

## 12. Boundary preservation

- Official state remains `DEMO_READY_WITH_LIMITATIONS`.
- MVP remains electronics/electrical-only.
- Answer Clarification remains inactive.
- Safety Signals remain closed.
- Saved answers remain verbatim; the inventor remains the sole author.
- **No implementation is authorized by this scope decision PR.**
- `main` remains `0e89e4636399760965c9ff8086b465c90dbadf8e` and is not
  synchronized; the frozen persistence lane remains PRESERVE UNMODIFIED AND PAUSE
  at `aec9cf6409efc18e125b6745762002f59e529654`; the quarantined scratch branch
  remains untouched at `02586747c902d5e1ebb78adde54ddd4ecd1c174a`.

## 13. Final classification

`PLAIN-LANGUAGE RESULT FEEDBACK SCOPE DECISION CREATED — FUTURE CANDIDATE ONLY — NO IMPLEMENTATION AUTHORIZED`
