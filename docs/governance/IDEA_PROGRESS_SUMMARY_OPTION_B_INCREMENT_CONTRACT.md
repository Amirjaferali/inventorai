# Idea Progress Summary — Option B Increment Contract

Status: DRAFT FOR INDEPENDENT REVIEW — INCREMENT CONTRACT ONLY — DOCS-ONLY —
OPTION B NARROWED DELTA ONLY — NO IMPLEMENTATION AUTHORIZED

## 1. Contract identity and authority

This document is the owner-gated **Increment Contract** for the narrowed
(Option B) first increment of the **Idea Progress Summary** candidate. It
follows, in order, the governed lifecycle steps already completed:

1. Scope decision — `docs/governance/IDEA_PROGRESS_SUMMARY_SCOPE_DECISION.md`,
   true-merged via PR #160 (merge commit
   `cb1f6d43d3f4da8e20971a5b186d18f83896a1a0`).
2. Roadmap synchronization recording that scope decision — PR #161 (merge
   commit `236cbcdc8f948db78eaeb6691b1c405564f6a99c`).
3. Owner-gated read-only source review, completed at authoritative tip
   `236cbcdc8f948db78eaeb6691b1c405564f6a99c`.

This contract is subordinate to `MVP_SCOPE_FREEZE.md`, the Level 0 owner
amendment `docs/governance/OWNER_PRODUCT_IDENTITY_CORRECTION.md`, the merged
scope decision, and the committed roadmap. It authorizes **documentation
acceptance only**: no source, template, test, schema, engine, scoring,
persistence, transcript, deliverable, or runtime change is authorized by this
document or by its merge. Authoring context: branch
`feature/atomic-json-session-persistence`; tip
`236cbcdc8f948db78eaeb6691b1c405564f6a99c` (publication-time metadata only; the
live authoritative tip is always resolved from Git).

## 2. Source Review result (controlling input)

The completed read-only source review classified:

> SOURCE REVIEW COMPLETE — PARTIAL SESSION DELTA RELIABLY DERIVABLE —
> OPTION B RECOMMENDED — NO IMPLEMENTATION AUTHORIZED

Its controlling findings, adopted by this contract:

- A truthful, deterministic session delta **is** derivable from current
  committed state **without** schema or persistence changes — but only from a
  verified subset of fields (§7).
- `IterationLog.gaps_changed` and `IterationLog.gap_targeted` are
  **semantically defective** and must never be consumed (§8).
- Bare "Established" overstates current semantics: a CLOSED gap means the
  inventor's answer was heuristically classified REASONED; the repository's own
  committed status label for CLOSED is "Answered (not yet validated)", and
  `validation_status` defaults to `UNVALIDATED` and is never auto-promoted.
- The normal completion branch requires maturity ≥ 2 AND no open gaps, so the
  completion-stage "still open" category is normally empty (§9).
- An eligibility-aware deliverable link already exists at the top of the
  session page; the completion bridge is a relocation/repetition of an existing
  navigation action, not a new capability (§13).

## 3. Product objective

At the completion stage of an idea session, show the inventor one concise,
factual, deterministic summary of **what was recorded and what changed during
this idea session** — derived entirely from already-committed state — so that
completion is not a dead end and the honest idea-state (recorded / changed /
unknown) is visible, consistent with
`OWNER_PRODUCT_IDENTITY_CORRECTION.md §6` (success is measured by the honesty
and completeness of what is established and what is preserved as unknown) and
the `OWNER_PRODUCT_IDENTITY_CORRECTION.md §3` "the idea is the subject"
framing. `ACTIVE_EXECUTION_ROADMAP.md §9`'s prohibition of inventor-development
and idea-growth claims is binding: no growth, achievement, readiness, or
improvement claim may be made.

## 4. Truthful user-facing title

The unqualified feature title `What You've Established & What Changed` is
**retired** for user-facing use: the completed source review determined that
"Established" overstates current semantics.

The user-facing working title for this increment is:

**Idea Progress Summary — What You've Recorded & What Changed**

A different title may be substituted at implementation time only if it is
equally or more truthful and remains within Option B. The user-facing title
and all summary copy must not imply: validation; verification; proof; design
completion; engineering readiness; idea improvement; commercial readiness;
manufacturing readiness; patentability; safety; or regulatory compliance.

## 5. User-visible value

- The inventor sees, at completion, a single factual account of the session:
  where maturity started and where it is now; which question areas were opened
  and which were addressed (not yet validated); what they recorded through the
  six response actions; and what remains preserved as unknown.
- Completion stops being a dead end: the summary block carries the existing
  navigation action to the deliverable.
- Nothing is invented, praised, scored, or inferred; every displayed item is
  traceable to committed state.

## 6. Authorized scope (future implementation lane, separately gated)

The future implementation increment — which this contract does NOT authorize —
is bounded to:

1. One new pure, deterministic, import-clean display helper that derives the
   summary from the already-loaded `IdeaState` alone.
2. One derived render-context variable supplied by the existing session view.
3. One completion-stage template integration that **replaces or extends** the
   existing completion summary block (the checkmark line and the
   "Areas you have addressed" list) rather than adding a second competing
   completion panel.
4. One template-level navigation link to the already-existing deliverable
   route inside the completion block (§13).
5. Dedicated deterministic tests (§19), written only under the later
   implementation authorization.

## 7. Permitted data sources (binding Option B boundary)

The increment may derive display data **only** from this reliable subset,
confirmed by the source review:

1. `IdeaState.maturity_level`
2. `IterationLog.maturity_before`
3. `IterationLog.maturity_after`
4. `Gap.opened_at`
5. `Gap.closed_at`
6. Current `Gap.status`
7. The append-only interaction/assertion ledger (`IdeaState.assertions`)
8. The ledger's reliable `gap_context` (captured pre-iteration for answered
   records)
9. `IdeaState.acknowledged_unknowns`
10. Existing friendly gap-label helpers (`web/gap_labels.py` —
    `GAP_LABELS`, `GAP_DISPLAY_NAMES` / `friendly_gap_name`, `MATURITY_LABELS`)
11. Existing deliverable route availability, for navigation only (§13)

No other field, store, log, file, or inference may be used as a truth source.

## 8. Explicitly prohibited data sources

The following MUST NOT be used as truth sources, in any form:

1. **`IterationLog.gaps_changed`** — PROHIBITED. It does not reliably
   represent the gap that actually changed: it is populated from the iteration
   result's `gap_targeted` value, which holds the **next cascade-opened gap or
   `None`**, not the gap whose status changed. It must not be used to
   construct any historical gap-change account.
2. **`IterationLog.gap_targeted`** — PROHIBITED for the same reason: in the
   normal answer path it records the next cascade-opened gap (usually `None`),
   not the gap the answer addressed. The reliable per-answer gap attribution
   is the ledger record's `gap_context`.

Additionally, **`IterationLog.response_summary` MUST NOT be displayed** as the
inventor's answer or as verbatim inventor-authored text, because: it is
truncated (100 characters); it is not the authoritative verbatim answer; and
saved answers and inventor-authored content must remain verbatim. Where
inventor text is shown at all, only verbatim sources (the ledger record
content or acknowledged-unknown verbatim) may be used.

Repairing, reinterpreting, or backfilling the defective iteration-log fields
is out of scope and a stop condition (§20); under the repository refactor
governance contract, any such engine change requires its own classification
and authorization.

## 9. Category semantics (permitted delta categories)

### 9.A Maturity delta

Permitted: a comparison derived from the reliable maturity history — maturity
at the start of the idea session (`iteration_log[0].maturity_before`, which is
0 by construction, or the constructor default when no log exists), current
`maturity_level`, and whether maturity changed or remained unchanged, rendered
with the existing approved `MATURITY_LABELS`. Maturity movement must be
presented as a factual stage change, never as proof that the idea improved.
A no-change session must say so plainly and must not fabricate movement.

### 9.B Gap opening and addressing

Permitted: gaps opened during the idea session (`opened_at`); gaps currently
OPEN or PARTIAL, where applicable to the rendering state; gaps currently
CLOSED with their reliable `opened_at`/`closed_at`. Every CLOSED gap must be
described with a qualification equivalent to:

> Addressed in your answers — not yet validated

CLOSED must never be presented as: validated; verified; proven; completed;
solved; engineering-ready; or "established" without qualification. Every gap
reference must pass through an approved friendly-label mapping; raw internal
tokens (e.g. `MECHANISM_COMPLETENESS`, `rec_1`) must never be primary text.

### 9.C Recorded interaction dispositions

Permitted: bounded counts or factual summaries from the append-only ledger for
the six committed dispositions — answered; marked unknown; deferred;
provisional assumption (always qualified as not verified); specialist
requested; evidence requested. These are activity facts only: they must not be
converted into scoring, readiness, praise, progress framing, or idea-growth
claims, and must not imply maturity movement.

### 9.D Acknowledged unknowns

Permitted: deterministic reference to `acknowledged_unknowns` as the
"preserved as unknown" account. The same verbatim unknown text must not be
duplicated across multiple panels when an existing panel (the session page's
"What You Have Marked as Not Yet Known") already presents it: the summary must
prefer counts, short references, or cross-references over duplicate full-text
rendering. Where unknown text is shown, it remains verbatim and unrewritten.

## 10. Session definition

"This session" means exactly:

> the lifetime of the current in-memory IdeaState / idea session, beginning
> when the user starts the idea

It must not imply: a persistent cross-device session; a browser-login session;
restored history after server restart; durable persistence; or historical
reconstruction across separately created ideas. Server restart destroys the
current session because persistence is not active; this limitation is part of
`DEMO_READY_WITH_LIMITATIONS` and must not be "fixed" within this increment.
Because the session is the idea's whole lifetime, wording equivalent to
"since you started this idea" is the honest framing of the delta.

## 11. Completion-stage placement

The first implementation increment is **completion-stage-first**: the summary
renders only in the completion branch of the session view (the state where
maturity ≥ 2 and no open gaps). PROHIBITED: always-visible placement;
after-every-answer placement; persistent dashboard placement; and adding
another advisory panel during active questioning. The new surface must replace
or extend the existing completion summary block rather than create a second
competing completion panel.

### 11.A Open-gap reality at completion

Because the completion branch requires maturity ≥ 2 AND no open gaps, the
completion-stage "still open" section will normally be empty. The
implementation must NOT render a misleading empty "Still open" section merely
to preserve the original four-category concept. Honest behavior is required:
either omit the section when empty, or state minimally and factually that no
open question areas remain **in the current demo assessment state** — wording
that must not imply validation or completion of the invention. The source
review found that the existing "Areas still open" markup inside the completion
branch is unreachable under the current predicate; correcting unrelated dead
code is NOT part of this increment unless strictly necessary for the
authorized implementation surface.

## 12. Existing-surface non-duplication

The summary must remain distinct from, and must not duplicate: the **Gap
Board** (current per-gap status chips); **Plain-Language Result Feedback**
(latest single result); **Scaffolding Guidance** (WARN-state help for the
current question); **Uncertainty Guidance**; the **Co-Authoring advisory**;
the **Next Development Step** callout (single forward-looking action); the
**Deliverable** (full artifact — the summary must stay concise and
session-level, not re-implement deliverable sections 3/8); and the existing
completion message (which it replaces/extends per §11). Acceptance requires
demonstrable distinct delta value beyond a rewording of these surfaces (§15
gate 13, §20 stop condition 12).

## 13. Deliverable navigation boundary

Recorded facts: the deliverable route already exists
(`/session/<sid>/deliverable`); an eligibility-aware deliverable link already
exists at the top of the session page (its wording already distinguishes the
eligible deliverable from the in-progress snapshot); the completion bridge is
therefore a **relocation or repetition of an existing navigation action**, not
a new deliverable capability.

Permitted: a template-level navigation link in the completion block, using the
already-existing route, existing eligibility behavior, and existing honest
link wording. PROHIBITED: route changes; eligibility changes; automatic
redirect; new generation logic; new deliverable content; readiness
implications in or around the link; and any change to
`engine/deliverable_assembler.py`.

## 14. Authorship and verbatim-answer boundary

1. The inventor remains the **sole author**.
2. Saved answers remain **verbatim**.
3. The summary is **system-derived display metadata**, not inventor-authored
   content.
4. The summary must not be inserted into: saved answers; the inventor
   transcript as if written by the inventor; inventor-authored deliverable
   sections; or assertion text attributed to the inventor.
5. No generated wording may replace, rewrite, clarify, improve, or approve an
   inventor answer.
6. Answer Clarification remains inactive and must not be used as a dependency
   or shortcut.

## 15. Closed and frozen governance states (preserved)

This increment preserves, and may not reopen: official state
`DEMO_READY_WITH_LIMITATIONS`; MVP `electronics/electrical-only`; Answer
Clarification **inactive**; Safety Signals **closed**; persistence **frozen
and paused**; the inventor as **sole author**; saved answers **verbatim**;
`main` (`0e89e4636399760965c9ff8086b465c90dbadf8e`) **unsynchronized**; the
frozen persistence lane at `aec9cf6409efc18e125b6745762002f59e529654`
**untouched**; and the quarantined scratch branch
(`02586747c902d5e1ebb78adde54ddd4ecd1c174a`) **untouched**.

## 16. Prohibited changes

Explicitly prohibited: implementation under the contract-writing
authorization; source-code changes; template changes; test creation or
modification; runtime behavior changes; schema changes; persistence changes;
session restoration; scoring changes; maturity-transition changes;
gap-transition changes; transcript changes; ledger changes; assertion-model
changes; deliverable-assembler changes; LLM calls; Answer Clarification work;
Safety Signals work; correction of `IterationLog.gaps_changed`; correction of
`IterationLog.gap_targeted`; and refactoring unrelated dead or vestigial code.
This contract describes future test requirements (§19), but no tests may be
written under this authorization.

## 17. Future architecture boundary (anticipated, not binding on symbols)

The future implementation is expected to take approximately this narrow shape,
governed by behavior rather than pinned symbols: one pure deterministic
display helper; input limited to the already-loaded `IdeaState`; reuse of the
existing friendly-label helpers; no state mutation; no transition evaluation;
no scoring recomputation; no persistence access; no transcript write; no LLM;
no deliverable-assembler change; one derived render-context variable; one
completion-stage template integration; and dedicated deterministic tests under
the later implementation authorization. The helper must not import engine
transition/scoring/persistence/Safety-Signals/domain-gate modules.

## 18. Acceptance gates (testable, binding on the future implementation)

1. No output consumes `IterationLog.gaps_changed`.
2. No output consumes `IterationLog.gap_targeted`.
3. No inventor answer is rendered from `IterationLog.response_summary`.
4. Every gap label is passed through an approved friendly-label mapping.
5. Every CLOSED gap is qualified as not yet validated.
6. No unqualified "Established" appears in the user-facing surface.
7. No idea-improvement or readiness claim appears.
8. No mutation occurs while deriving the summary.
9. No scoring or transition logic is called.
10. No persistence is read or written.
11. No transcript or assertion is written.
12. No LLM is invoked.
13. Completion rendering does not duplicate an existing panel without adding
    distinct delta value.
14. A malformed or incomplete history produces a safe reduced summary rather
    than invented data.
15. A no-maturity-change session does not fabricate progress.
16. Non-answer actions are summarized only from reliable ledger dispositions
    and do not imply maturity progress.
17. Unknowns remain verbatim where shown and are not rewritten.
18. The deliverable action remains navigation-only.
19. Existing ineligible deliverable behavior remains unchanged.
20. Official state and MVP scope remain unchanged.

## 19. Future test strategy (described only — no tests under this authorization)

Deterministic future tests must cover, at minimum: initial assessment only;
no maturity change; maturity increase; gap opened; gap closed; multiple
iterations; non-answer actions; acknowledged unknowns; deferred response;
provisional assumption; specialist requested; evidence requested; no iteration
log; malformed or incomplete history; completed session; empty optional
categories; raw internal token leakage; no duplicate acknowledged-unknown
text; no unqualified "Established"; CLOSED-gap qualification; deliverable-link
visibility; unchanged deliverable eligibility; no mutation (state deep-equal
before/after derivation); no LLM; no persistence; and no transcript write.
Each test's expected behavior follows the corresponding acceptance gate in
§18 and the category semantics in §9.

## 20. Stop conditions (mandatory, non-waivable by the implementer)

Implementation must STOP — without broadening scope, and returning to the
owner for a new scope decision or a separate increment — if any of the
following becomes necessary:

1. Using `gaps_changed` or `gap_targeted`.
2. Reconstructing history not retained by current state.
3. Adding or changing persistence.
4. Adding schema fields.
5. Modifying progression, scoring, maturity, or gap-transition logic.
6. Repairing iteration-log defects.
7. Rewriting or summarizing inventor answers as inventor-authored text.
8. Reopening Answer Clarification.
9. Reopening Safety Signals.
10. Changing deliverable eligibility or assembly.
11. Adding an LLM dependency.
12. Duplicating existing surfaces without distinct user value.
13. Making claims of validation, readiness, improvement, or completion not
    supported by state.

## 21. Non-goals

This increment excludes: any Option A full-delta account; any always-visible
or per-question summary; cross-session continuity or resume; persistence work
of any kind; new scoring, maturity rules, gap types, or gap reprioritization;
recommendation generation; domain-specific technical advice; answer
clarification or rewriting; LLM-generated summaries; transcript rewriting;
deliverable-assembler changes or new report sections; validation/readiness
claims; gamification or celebratory progress claims; full localization; repair
of `IterationLog` defects; correction of unrelated dead template code; and
browser visual QA at the contract stage.

## 22. Files likely in a future implementation lane (non-binding)

Anticipated, subject to confirmation at implementation authorization and NOT
binding: one NEW pure display helper under `web/` (e.g.
`web/idea_progress_summary.py`); `web/app.py` ONLY for one derived
render-context variable in the session view; `web/templates/session.html` ONLY
within the completion branch (replacing/extending the existing completion
summary block and hosting the navigation-only deliverable link); and one NEW
dedicated test module under `tests/`. No other file is expected; any expansion
requires owner authorization.

## 23. Independent-review requirements

This Draft PR requires an independent review by a session that did not author
or correct it. Any correction requires a limited correction authorization.
After corrections, a fresh independent review must evaluate the exact new
head. Review must verify, at minimum: docs-only diff; conformance of every
section of this contract to the completed source review; the Option B data
boundary (§7–§8); the truthful-title requirement (§4); and the preserved
states (§15).

## 24. Owner-gated lifecycle

1. This PR is documentation-only.
2. Acceptance of this contract does not authorize implementation.
3. Independent review of this Draft PR (§23) precedes any merge.
4. Merge remains owner-gated.
5. The accepted and merged contract must then be recorded in the Active
   Execution Roadmap through a separate docs-only PR; that roadmap sync must
   itself be independently reviewed and owner-gated merged.
6. Only after that roadmap sync may a separate implementation authorization be
   considered.
7. Implementation must later receive: independent review; owner-gated merge;
   manual integrated demo evidence; and final roadmap synchronization.

## 25. Final contract classification

Idea Progress Summary Option B Increment Contract — DRAFTED FOR INDEPENDENT
REVIEW — OPTION B NARROWED DELTA ONLY — docs-only — implementation not
authorized.
