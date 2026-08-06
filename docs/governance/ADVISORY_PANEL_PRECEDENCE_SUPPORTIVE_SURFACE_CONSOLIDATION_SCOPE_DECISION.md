# ADVISORY PANEL PRECEDENCE — SUPPORTIVE SURFACE CONSOLIDATION — OWNER SCOPE DECISION (POST-PR #138)

## 0. Status

`DOCS-ONLY SCOPE DECISION — ADVISORY PANEL PRECEDENCE / SUPPORTIVE SURFACE
CONSOLIDATION ADMITTED AS FUTURE OWNER-GATED DISPLAY-ONLY CANDIDATE — NO
IMPLEMENTATION AUTHORIZED`

This document admits a future, separately-authorized, **display-only** increment
— **Advisory Panel Precedence — Supportive Surface Consolidation** — to prevent
cognitive overload from stacked advisory panels around a single question. It
records an owner scope decision only. It authorizes NO implementation, code,
test, schema, UI, route, template, runtime, session, scoring, maturity,
readiness, criticality, persistence, deliverable, report, or domain change; no
Increment Contract in this step; no roadmap change; no `main` synchronization;
and no MVP activation of any kind.

File-creation record (per `CLAUDE.md` File Creation Rules):
- File path: `docs/governance/ADVISORY_PANEL_PRECEDENCE_SUPPORTIVE_SURFACE_CONSOLIDATION_SCOPE_DECISION.md`
- Purpose: record an owner admission decision for a future display-only advisory
  panel precedence / consolidation increment, with hard anti-drift boundaries.
- Input contract: the completed read-only Demo Readiness / User Journey Integrity
  diagnostic (post-Guided Uncertainty Support), the committed product identity
  (`OWNER_PRODUCT_IDENTITY_CORRECTION.md`, `STRATEGIC_PRODUCT_VISION.md`,
  `DUAL_PATH_PRODUCT_ANCHOR.md`), the merged Inventor Supportive Guidance &
  Non-Exam UX principle (PR #132), and the merged Guided Answer Co-Authoring
  (PR #129) and Guided Uncertainty Support (PR #136) surfaces.
- Output contract: one admission decision (§10) and its boundaries; nothing
  executable, nothing activating.
- Prohibited behaviors: this file must never be read as implementation
  authorization, source/template/test authorization, scoring authorization, an
  Increment Contract, activation of the Inventor Answer Clarification / Improve
  Wording feature, a roadmap update, or a `main`/frozen/quarantined branch
  change.

Authoritative context (evidence-locked):
- Repository: `Amirjaferali/inventorai`
- Authoritative branch: `feature/atomic-json-session-persistence`
- Authoritative tip: `e125b60eaf73bcfbae5c1835ed08207041b37246` (PR #138 merge)
- Latest merged PR: #138
- Current official state remains: `DEMO_READY_WITH_LIMITATIONS`
- The MVP remains electronics/electrical-only (`MVP_SCOPE_FREEZE.md`).
- `main` remains separate and unchanged
  (`0e89e4636399760965c9ff8086b465c90dbadf8e`); no `main` sync occurred or is
  authorized.
- The frozen persistence worktree remains paused and untouched
  (`aec9cf6409efc18e125b6745762002f59e529654`); the quarantined scratch branch
  remains untouched (`02586747c902d5e1ebb78adde54ddd4ecd1c174a`).

---

## 1. Problem

On the current committed session page, up to **five** advisory / support panels
can render at once around a single scaffolding question:

- the **Next Development Step** callout;
- the **More Detail Needed** scaffolding guidance (WARN state);
- the **responsibility** guidance ("You can answer this" / "Specialist may
  help…");
- the **Guided Uncertainty Support** panel ("Optional — no pressure");
- the **Guided Answer Co-Authoring** panel ("Optional guidance — what you could
  include");

plus a collapsed **clarification** expander ("Help me understand this question")
and a transient **interaction acknowledgement**. In the **uncertainty + WARN**
state (the inventor typed "I don't know" / "لا أعرف" on a WARN outcome), several
of these open panels stack above the answer box simultaneously. Each panel is
individually correct, calm, and governance-clean, but the **aggregate** is
crowded and risks a cognitive-overload / exam-like feel for a non-technical
inventor — the exact experience the merged Inventor Supportive Guidance &
Non-Exam UX principle (PR #132) exists to prevent.

The three "what to add / who should answer" surfaces — **scaffolding**,
**responsibility**, and **co-authoring** — overlap heavily in purpose; the
**uncertainty** panel is emotionally distinct ("that's okay") yet currently
co-renders with the co-authoring checklist, mixing "it's okay not to know" with
"here is what to include."

---

## 2. Product objective

Keep InventorAI **supportive, calm, non-exam-like, and user-authored** by showing
**at most one primary advisory panel per state**, so a non-technical inventor
sees a single clear next step rather than a stack of competing surfaces. The
value is **idea-development clarity** (reducing overload and drop-off), not
inventor education, and not answer generation. The inventor remains the sole
author of any saved answer.

---

## 3. Proposed future display-only principle

If admitted, a future — separately gated — increment *could* apply a
deterministic, render-time precedence so at most one primary advisory panel shows
per state:

- **Uncertainty state** (the inventor expressed uncertainty): **uncertainty
  guidance is primary**; the co-authoring and scaffolding panels are suppressed
  for that render.
- **WARN / not-uncertain state**: **scaffolding guidance is primary**; the
  co-authoring panel is suppressed.
- **Fresh question / no WARN / no uncertainty**: **co-authoring guidance is
  primary**.
- **Plain-language help** remains available through the existing **collapsed
  clarification expander** ("Help me understand this question"), on demand.
- **Responsibility** guidance is **compacted or merged into the primary surface**
  (e.g. a single compact line), not a competing primary block.
- The **Next Development Step** callout may remain as the **single persistent
  forward-looking callout**.
- **Do not hide truthful states** — gaps, the honest interaction acknowledgement,
  and the truthful WARN/PASS/BLOCK state must remain visible; only *competing
  advisory* surfaces are reduced.

These are candidate possibilities only; none is implemented or authorized here.

---

## 4. Hard boundaries

This scope decision, and any increment it may later admit, does NOT authorize and
must NOT perform:

- any non-**display-only** change;
- any **schema** change;
- any **scoring** change (`assess_response` / `integrate_response` /
  `evaluate_transition` / thresholds / generic-verb trap / causal tokens);
- any **persistence / session / transcript** change;
- any **saved-answer behavior** change (the answer stays the inventor's verbatim
  text);
- **answer rewriting**;
- **Answer Clarification / Improve Wording** activation;
- an **approval / save clarified-answer flow**;
- introducing `original_user_answer` / `suggested_clarified_answer` /
  `user_approved_answer` / `clarification_status` fields (or any equivalent);
- **maturity / readiness / criticality** change;
- **Section 6** risk change or `RequirementLandscape.risks` population;
- **Increment-6** deliverable-structure change or Increment-5 validation-plan
  semantics change;
- **reopening Safety Signals**;
- **domain expansion** beyond the electronics/electrical MVP;
- any **validation, feasibility, readiness, safety, patent, or engineering
  certainty** claim.

The inventor remains the **sole author** of the answer.

---

## 5. Future governance path

This document is **only a scope decision**; it authorizes no implementation. If
accepted (independently reviewed and owner-gated true-merged), the future
sequence is:

scope decision merge → roadmap sync (separate, if required) → **separate
Increment Contract** → independent review → owner-gated true merge of the
contract → **read-only source review** → **separate implementation
authorization** → implementation PR → independent review → owner-gated true merge
→ **separate manual demo verification** → **separate roadmap synchronization**.

Any implementation must be **separately owner-gated**, and a read-only source
review must precede it. No step beyond this scope decision is authorized here,
and none may be inferred (roadmap §8.1–§8.2).

---

## 6. Expected later implementation surface (planning only — inspect only)

The following are **candidate surfaces to inspect during a later read-only source
review** — named from present repository evidence, not prescribed as edit
targets. No file below may be changed by this scope decision:

- **Primary likely surface:** `web/templates/session.html` (precedence guards
  around the existing, already-computed advisory panels).
- **Optional:** one small pure read-only selector/helper in `web/app.py`
  `show_session` (or a new pure helper) computing the "primary advisory surface"
  from existing context — only if template-only proves awkward.
- **Must NOT change:** `submit_answer` / `run_iteration` / `record_interaction`
  / session persistence / transcript; scoring / engine; the deliverable /
  report; the existing display helpers' *outputs* (`web/uncertainty_guidance.py`,
  `web/answer_coauthoring_prompts.py`, `web/clarification_labels.py`,
  `web/scaffolding_guidance.py`, `web/responsibility_labels.py`) are **reused,
  not altered**.

---

## 7. Expected future tests (planning only)

A future implementation must include tests proving:

- **Exactly one** primary advisory panel renders per state.
- **Uncertainty** wins over co-authoring / scaffolding when the inventor is
  uncertain (English AND Arabic).
- **WARN scaffolding** wins when a WARN state is present and the inventor is not
  uncertain.
- **Co-authoring** appears only when neither uncertainty nor WARN is primary.
- **Clarification** remains available as the collapsed expander.
- The **six honest actions** are unchanged (no seventh).
- The **saved answer remains verbatim**; no guidance persists as answer content.
- **No schema / scoring / persistence** change; Increment-6 top-level contract
  intact; the locked scoring suites remain green (baseline failures confined to
  `tests/test_domain_registry.py`; zero new).
- **Safety Signals** surface unchanged.
- The **electronics/electrical domain gate** is preserved.
- **No truthful state hidden** (gaps, honest ack, WARN/PASS/BLOCK remain
  visible).

---

## 8. Expected future manual demo evidence (planning only)

A future manual demo should show, in **English and Arabic**, a **calm,
single-primary-panel** journey at each state — no five-panel stack — with
user-authored answers, the clarification help available on demand, no exam-like
wording ("wrong" / "failed" / "insufficient" absent), and no answer written for
the user.

---

## 9. Stop conditions

Stop and report if the future increment (or any reading of this decision) would:

- require scoring / schema / persistence / transcript changes;
- **hide truthful gap / state information** (gaps, honest ack, WARN/PASS/BLOCK);
- write the user's answer or rewrite it;
- activate Answer Clarification / Improve Wording;
- introduce an approval/save clarified-answer flow or the forbidden clarification
  fields;
- reopen Safety Signals;
- expand MVP beyond electronics/electrical;
- add a seventh session action;
- change official state; or
- touch `main`, the frozen persistence worktree, or the quarantined scratch
  branch.

---

## 10. Decision

**Advisory Panel Precedence — Supportive Surface Consolidation** is classified as
a **FUTURE OWNER-GATED, DISPLAY-ONLY INCREMENT CANDIDATE — SCOPE DECISION ONLY —
NO IMPLEMENTATION AUTHORIZED**.

Admission means only that the candidate may proceed to a separately-authorized
Increment Contract under a separate owner authorization, on condition that any
such contract honors the hard boundaries (§4), the display-only precedence
principle (§3), the no-truthful-state-hiding rule (§3/§9), and the stop
conditions (§9). This decision does NOT authorize implementation, does NOT start
an Increment Contract, and does NOT make the Answer Clarification / Improve
Wording feature current. The app remains electronics/electrical-only for the MVP,
and the current official state remains `DEMO_READY_WITH_LIMITATIONS`, until
separate governed decisions state otherwise.

A roadmap entry recording this scope decision is **proposed only** and is NOT made
by this document; roadmap synchronization is a separate, owner-gated step
performed after (and if) this scope decision is merged. This document changes no
roadmap file.

---

## 11. Final classification

`DOCS-ONLY SCOPE DECISION — ADVISORY PANEL PRECEDENCE / SUPPORTIVE SURFACE
CONSOLIDATION ADMITTED AS FUTURE OWNER-GATED DISPLAY-ONLY CANDIDATE — NO
IMPLEMENTATION AUTHORIZED`
