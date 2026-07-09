# ADVISORY PANEL PRECEDENCE — SUPPORTIVE SURFACE CONSOLIDATION — INCREMENT CONTRACT

## 0. Status

`DOCS-ONLY INCREMENT CONTRACT — ADVISORY PANEL PRECEDENCE / SUPPORTIVE SURFACE
CONSOLIDATION — DISPLAY-ONLY FUTURE IMPLEMENTATION BOUNDARY — NO IMPLEMENTATION
AUTHORIZED`

This document defines the **display-only future implementation boundary** for the
**Advisory Panel Precedence / Supportive Surface Consolidation** increment,
derived from the merged scope decision
(`ADVISORY_PANEL_PRECEDENCE_SUPPORTIVE_SURFACE_CONSOLIDATION_SCOPE_DECISION.md`,
PR #139; roadmap-recorded by PR #140). It is **contract documentation only**. It
authorizes NO implementation, code, test, schema, UI, route, template, runtime,
session, scoring, maturity, readiness, criticality, persistence, deliverable,
report, or domain change; no source review in this step; no roadmap change; no
`main` synchronization; and no MVP activation of any kind.

File-creation record (per `CLAUDE.md` File Creation Rules):
- File path: `docs/governance/ADVISORY_PANEL_PRECEDENCE_SUPPORTIVE_SURFACE_CONSOLIDATION_INCREMENT_CONTRACT.md`
- Purpose: define the smallest, display-only future Advisory Panel Precedence
  increment and its hard boundaries, so a later — separately authorized —
  implementation has an evidence-grounded, anti-drift contract to build against.
- Input contract: the merged scope decision (PR #139), the merged Guided
  Uncertainty Support Increment Contract (`GUIDED_UNCERTAINTY_SUPPORT_INCREMENT_CONTRACT.md`),
  the merged Guided Answer Co-Authoring Increment Contract
  (`GUIDED_ANSWER_COAUTHORING_INCREMENT_CONTRACT.md`), the merged Inventor
  Supportive Guidance & Non-Exam UX principle (PR #132), and the committed
  product identity (`OWNER_PRODUCT_IDENTITY_CORRECTION.md`,
  `STRATEGIC_PRODUCT_VISION.md`).
- Output contract: a single future-implementation contract (§11 classification)
  with its purpose, scope, precedence model, prior-contract reconciliation,
  boundaries, required future tests, manual-demo expectations, stop conditions,
  and governance path; nothing executable, nothing activating.
- Prohibited behaviors: this file must never be read as implementation
  authorization, source-review authorization, scoring authorization, activation
  of the Inventor Answer Clarification / Improve Wording feature, a roadmap
  update, or a `main`/frozen/quarantined branch change.

Authoritative context (evidence-locked):
- Repository: `Amirjaferali/inventorai`; authoritative branch
  `feature/atomic-json-session-persistence`; authoritative tip
  `b6814437eb9e9b9a320477387951a21e03c52033` (PR #140 merge); latest merged PR
  #140.
- Official state: `DEMO_READY_WITH_LIMITATIONS`; MVP electronics/electrical-only
  (`MVP_SCOPE_FREEZE.md`).
- `main` remains separate and unchanged
  (`0e89e4636399760965c9ff8086b465c90dbadf8e`); the frozen persistence worktree
  remains paused and untouched (`aec9cf6409efc18e125b6745762002f59e529654`); the
  quarantined scratch branch remains untouched
  (`02586747c902d5e1ebb78adde54ddd4ecd1c174a`).

---

## 1. Purpose

Prevent cognitive overload from stacked advisory / support panels by allowing **at
most one primary advisory panel per user state**, while keeping InventorAI
**supportive, calm, non-exam-like, and user-authored**. The value is
idea-development clarity — a non-technical inventor sees a single clear next step,
not a stack of competing surfaces. The inventor remains the sole author of any
saved answer.

---

## 2. Scope

A future — separately authorized — implementation may **only adjust render-time
display precedence among already-existing advisory surfaces**. It must **not**
alter engine logic, scoring, session state, persistence, saved answers,
deliverable semantics, or domain scope. It reuses the existing helpers' outputs;
it changes *which* advisory surface is shown as primary in a given render state,
nothing more.

---

## 3. Required precedence model

At render time, at most one **primary** advisory panel is shown, by this
deterministic precedence:

1. **Uncertainty state** (the inventor's most recent text expresses uncertainty,
   English or Arabic): **Guided Uncertainty Support is the primary advisory
   panel.**
2. **WARN scaffolding state and not uncertainty**: **scaffolding guidance is the
   primary advisory panel.**
3. **No uncertainty and no WARN scaffolding**: **Guided Answer Co-Authoring may be
   the primary advisory panel.**
4. **Plain-language clarification** remains available as **collapsed / on-demand
   help** ("Help me understand this question").
5. The **Next Development Step** callout may remain as the **single persistent
   forward-looking callout**.
6. **Responsibility Guidance** may be **compacted, merged, or demoted**, but
   **must not be removed entirely when it carries truthful responsibility
   information** (e.g. "a specialist may help" / "evidence or a test may be
   needed").
7. **No truthful state, gap, warning, acknowledgement, uncertainty, or
   responsibility information may be hidden** — only *competing advisory* surfaces
   are reduced.

---

## 4. Mandatory reconciliation with the Guided Uncertainty Support contract (§7)

This contract is explicitly reconciled with
`GUIDED_UNCERTAINTY_SUPPORT_INCREMENT_CONTRACT.md` **§7** ("Boundary with Guided
Answer Co-Authoring"), which requires that Guided Uncertainty Support **must not
remove, degrade, or duplicate the existing Co-Authoring surface**.

Reconciliation:
- The future implementation **may suppress Co-Authoring as a competing OPEN
  primary panel in a specific render state** (specifically the uncertainty and
  WARN-scaffolding states, per §3).
- It **must NOT remove, degrade, or duplicate the Co-Authoring surface as a
  capability.** Co-Authoring **must remain available** in the appropriate
  **non-uncertainty / non-WARN** states, where it is the primary panel (§3.3).
- Suppression must be **state-specific, render-only, and reversible by state**: it
  must not delete the feature, alter `web/answer_coauthoring_prompts.py` or its
  content, weaken its wording, or persistently disable it. When the state changes
  back to a non-uncertainty / non-WARN state, the Co-Authoring panel renders again
  unchanged.
- This is a **presentation-precedence** relationship between two preserved
  surfaces, not a removal of either. Guided Uncertainty Support and Guided Answer
  Co-Authoring both remain distinct, present capabilities; precedence only governs
  which is shown *as the single primary panel* per state.

---

## 5. Hard boundaries

A future implementation **must not**:

- perform any non-**display-only** change;
- change **schema**;
- change **scoring** (`assess_response` / `integrate_response` /
  `evaluate_transition` / thresholds / generic-verb trap / causal tokens);
- change **maturity / readiness / criticality**;
- change **persistence / session / transcript**;
- change **saved-answer behavior** (the answer stays the inventor's verbatim
  text);
- change **`submit_answer`** — unless a later read-only source review proves there
  is no display-only alternative AND the owner separately authorizes it;
- change **`run_iteration`**;
- change **`record_interaction`**;
- change **deliverable / report semantics**;
- introduce **answer rewriting**;
- **activate Answer Clarification / Improve Wording**;
- introduce an **approval / save clarified-answer flow**;
- introduce **hidden fields for generated guidance**;
- introduce `original_user_answer` / `suggested_clarified_answer` /
  `user_approved_answer` / `clarification_status` fields (or any equivalent);
- **reopen Safety Signals**;
- **expand the domain** beyond the electronics/electrical MVP;
- make any **validation, feasibility, readiness, patent, safety, or
  engineering-certainty** claim.

The **user remains the sole author** of answers.

---

## 6. Expected future implementation surface (planning only — inspect only)

Candidate surfaces for a later **read-only source review** (named from present
repository evidence, not prescribed as edit targets):

- **Primary likely surface:** `web/templates/session.html` (precedence guards
  around the already-computed advisory panels).
- **Optional:** a small **pure selector/helper** — only if a later read-only
  source review recommends it.
- **Optional:** a minimal `show_session` **render-context selector** in
  `web/app.py` — only if a later source review recommends it (read-only signal;
  no persistence/scoring effect).
- **Existing helpers must be REUSED, not altered:**
  `web/uncertainty_guidance.py`, `web/answer_coauthoring_prompts.py`,
  `web/clarification_labels.py`, `web/scaffolding_guidance.py`,
  `web/responsibility_labels.py`.
- **Must NOT touch** engine / scoring / persistence / session-transcript / report
  / deliverable behavior.

The exact, minimal change set must be established by that later read-only source
review, not assumed here.

---

## 7. Required future tests

A future implementation must include tests proving:

1. **Exactly one** primary advisory panel renders per state.
2. **Uncertainty** wins over scaffolding / co-authoring (English AND Arabic).
3. **WARN scaffolding** wins when not uncertainty.
4. **Co-authoring** appears as primary only when neither uncertainty nor WARN
   scaffolding is primary.
5. **Clarification** remains available as collapsed / on-demand help.
6. **Responsibility guidance** truthful content is preserved in compact / merged /
   demoted form and is **not removed entirely** when applicable.
7. **Co-Authoring capability** is not removed, degraded, duplicated, or
   persistently disabled (it renders unchanged in its appropriate states).
8. The **six honest answer actions** remain unchanged; **no seventh action**.
9. The **saved answer remains verbatim**.
10. Guidance is **not persisted as answer content**.
11. **No schema / scoring / persistence / session-transcript / deliverable**
    behavior change (locked scoring suites and the Increment-6 top-level contract
    remain green).
12. **Safety Signals** unchanged and not reopened.
13. **Answer Clarification** remains inactive.
14. The **electronics/electrical domain gate** is preserved.
15. Existing **baseline failures remain confined to
    `tests/test_domain_registry.py`** (zero new failures) unless newer evidence
    proves otherwise.

---

## 8. Required future manual demo evidence

A future manual demo should show:

- an **English** journey where the uncertainty state shows **one primary advisory
  panel** and **no five-panel stack**;
- an **Arabic** uncertainty input such as "لا أعرف" showing the correct
  **uncertainty-primary** behavior;
- a **WARN-not-uncertain** state showing **scaffolding primary** without a
  competing co-authoring block;
- a **fresh-question** state showing **co-authoring primary** when appropriate;
- **clarification** remaining available on demand;
- **responsibility guidance truth preserved** (compacted/merged/demoted, not
  hidden when applicable);
- the **user remaining the sole author**;
- **no answer rewriting**;
- **no exam-like wording** ("wrong" / "failed" / "insufficient" absent);
- **no readiness / validation / feasibility claims**.

---

## 9. Stop conditions

Stop and report if the future implementation would require:

- schema / scoring / persistence / session-transcript / deliverable behavior
  changes;
- hiding truthful states or responsibility information;
- deleting or degrading the Co-Authoring capability;
- writing or rewriting the user answer;
- activating Answer Clarification / Improve Wording;
- reopening Safety Signals;
- expanding the MVP;
- adding a seventh session action;
- changing official state; or
- touching `main`, the frozen persistence worktree, or the quarantined scratch
  branch.

---

## 10. Governance path

`Increment Contract → independent review → owner-gated true merge → read-only
source review → implementation PR → independent review → owner-gated merge →
manual demo evidence → roadmap sync.`

**Do not collapse these gates.** Any implementation must be separately owner-gated
and preceded by a read-only source review. No step beyond this Increment Contract
is authorized here, and none may be inferred (roadmap §8.1–§8.2). A roadmap entry
recording this contract is proposed only and is NOT made by this document.

---

## 11. Final classification

`DOCS-ONLY INCREMENT CONTRACT — ADVISORY PANEL PRECEDENCE / SUPPORTIVE SURFACE
CONSOLIDATION — DISPLAY-ONLY FUTURE IMPLEMENTATION BOUNDARY — NO IMPLEMENTATION
AUTHORIZED`
