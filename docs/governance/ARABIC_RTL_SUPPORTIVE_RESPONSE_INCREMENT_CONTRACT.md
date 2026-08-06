# Arabic / RTL Supportive Response — Increment Contract

Status: INCREMENT CONTRACT ONLY — DOCS-ONLY — NO IMPLEMENTATION AUTHORIZED

## 1. Purpose

This contract defines the display-only future implementation boundary for the
**Arabic / RTL Supportive Response** candidate admitted by the merged scope
decision (PR #146) and recorded in the roadmap (PR #147). It is a governance
document only. It authorizes no implementation, no source change, no test
change, no template change, no roadmap sync, and no merge of any code. It pins
the exact Arabic copy, the language/direction decision, the required behavior,
the untouched-files boundary, and the required tests, so that a future
separately-authorized implementation has a fixed, owner-ratified boundary.

## 2. Evidence basis

- **PR #146** admitted Arabic / RTL Supportive Response as a **future candidate
  only** (scope decision `docs/governance/ARABIC_RTL_SUPPORTIVE_RESPONSE_SCOPE_DECISION.md`).
- **PR #147** recorded the scope decision in `docs/governance/ACTIVE_EXECUTION_ROADMAP.md`.
- The **read-only source review** (authoritative tip
  `38cfce7fde648f6f3b500cc2dfecc0dee07ce45b`) found a **smallest safe,
  display-only path** (helper + template; `web/app.py` unchanged) and
  recommended **PROCEED TO INCREMENT CONTRACT**.
- **Current MEDIUM issue:** Arabic uncertainty such as "لا أعرف" is detected and
  triggers the uncertainty support panel, but the supportive response renders in
  **English and left-to-right**, with **no `dir="rtl"` and no `lang="ar"`**.

## 3. Objective

Implement **display-only** Arabic / RTL supportive response for **uncertainty
support only**, shown when Arabic uncertainty is detected. This must improve the
supportive UX for Arabic-speaking inventors **without changing** scoring,
persistence, saved answers, schema, transcript, deliverable, report, the domain
gate, or authorship. The inventor remains the sole author of any saved answer.

## 4. Smallest safe implementation boundary

If implementation is later separately authorized, the allowed **production**
files are limited to:

- `web/uncertainty_guidance.py`
- `web/templates/session.html`

The allowed **test** files are limited to:

- `tests/test_guided_uncertainty_support.py`
- `tests/test_advisory_panel_precedence.py`

`web/app.py` **must remain unchanged** unless a later source review proves that a
template/helper-only realization is impossible. (The reviewed design passes the
existing `current_uncertainty_guidance` dict through unchanged, so `web/app.py`
requires no change.)

## 5. Required Arabic copy pinned for owner approval

The following Arabic strings are pinned for owner approval and must be used
verbatim by any future implementation. They are **content-free supportive
guidance only**: they must not suggest an answer; must not add facts,
components, measurements, validation, feasibility, safety, compliance, patent,
or readiness claims; and must not rewrite the user's answer.

**Arabic uncertainty panel eyebrow:**

`اختياري — بدون ضغط`

**Arabic uncertainty heading:**

`لا بأس — لنأخذها خطوة بخطوة.`

**Arabic prompts:**

- `ما الجزء الذي أنت غير متأكد منه تحديدًا؟`
- `ما الذي تعرفه بالفعل عن هذه الفكرة، ولو كان بسيطًا؟`
- `ما المعلومة أو القياس أو المكوّن الذي تحتاج إلى التحقق منه لاحقًا؟`

**Arabic note:**

`يمكنك الإجابة بما تعرفه الآن فقط، وترك ما لا تعرفه واضحًا. هذا التوجيه لا يغيّر إجابتك ولا يُعد تحققًا هندسيًا أو موافقة سلامة أو امتثال أو براءة اختراع.`

## 6. Language / direction decision

- If an **Arabic-script uncertainty cue** is detected, render the uncertainty
  panel with `lang="ar"` and `dir="rtl"`.
- If **only English uncertainty** is detected, render `lang="en"` and
  `dir="ltr"`.
- **Mixed-language tie-break:** if an Arabic-script uncertainty cue is present,
  respond in Arabic and render the panel RTL.
- RTL must be **scoped to the uncertainty panel only**.
- The full page remains `<html lang="en">` and LTR for this increment.
- This **partial localization is an intentional, documented limitation**.

## 7. Required behavior

- English uncertainty still renders the existing English supportive response.
- Arabic uncertainty renders the pinned Arabic supportive response (§5).
- Non-uncertainty text returns **no** uncertainty panel.
- One-primary-panel precedence remains unchanged: **uncertainty > scaffolding/WARN > co-authoring**.
- Scaffolding and co-authoring remain suppressed as competing open primary panels
  when uncertainty is active.
- Six honest actions remain unchanged.
- Clarification remains collapsed / on-demand.
- Responsibility guidance remains truthful.
- WARN/PASS/BLOCK badge, reason/direction, gaps, acknowledged unknowns,
  interaction acknowledgement, and Next Development Step remain preserved where
  applicable.
- Saved answers remain verbatim.
- The user remains the sole author.

## 8. Explicitly out of scope

- full product localization;
- broad translation of all pages;
- general multilingual framework;
- translating all action labels;
- translating all badges / gaps / directions / page chrome;
- Answer Clarification / Improve Wording;
- answer rewriting;
- generated Arabic answer suggestions;
- approve / save / apply clarified-answer flow;
- hidden clarified-answer fields;
- schema changes;
- scoring changes;
- persistence changes;
- session transcript changes;
- deliverable / report behavior changes;
- Safety Signals reopening;
- domain expansion beyond electronics/electrical;
- production-readiness claims.

## 9. Files that must remain untouched

- `web/app.py`
- `engine/*`
- `scoring/*`
- `schemas/*`
- persistence / session store
- transcript behavior
- deliverable / report behavior
- domain gate behavior
- `engine/safety_signal.py`
- other display helpers:
  - `web/answer_coauthoring_prompts.py`
  - `web/scaffolding_guidance.py`
  - `web/clarification_labels.py`
  - `web/responsibility_labels.py`
  - `web/gap_labels.py`
- other templates
- `CLAUDE.md`
- governance anchors
- `ACTIVE_EXECUTION_ROADMAP.md` (except a later, separate roadmap sync)

## 10. Required tests for future implementation

- Arabic uncertainty "لا أعرف" renders Arabic copy with `lang="ar"` and `dir="rtl"` on the uncertainty panel.
- Arabic uncertainty "غير متأكد" renders Arabic copy with `lang="ar"` and `dir="rtl"`.
- Arabic uncertainty "لا أفهم" renders Arabic copy with `lang="ar"` and `dir="rtl"`.
- English uncertainty "I don't know" renders English copy with `lang="en"` / `dir="ltr"` or equivalent non-RTL state.
- English uncertainty "not sure" remains English/LTR.
- Mixed English+Arabic uncertainty chooses Arabic/RTL.
- Non-uncertainty text does not render uncertainty guidance.
- One-primary-panel precedence remains unchanged.
- Arabic uncertainty still suppresses scaffolding / co-authoring as competing open primary panels.
- Page shell remains `<html lang="en">`.
- Only the uncertainty panel gets Arabic/RTL treatment.
- No save/approve/apply control.
- No hidden clarified-answer fields.
- Saved answer remains verbatim.
- Six honest actions unchanged.
- Domain gate preserved.
- Safety Signals unchanged.
- Answer Clarification inactive.

## 11. Risks / edge cases

- Arabic translation quality and tone must remain **supportive**, not
  instructive or exam-like.
- Mixed-language input must use the deterministic **Arabic-script cue tie-break**.
- Partial localization may still leave surrounding page chrome in English; this
  is acceptable for this increment and **must be documented**.
- RTL punctuation / mixed Latin text may need careful rendering.
- Over-expansion into full localization **must be blocked**.

## 12. Required future sequence

Any implementation after this contract requires, in order, each as a separate,
explicit, owner-gated step:

1. independent review of this contract;
2. owner-gated true merge of this contract;
3. implementation authorization;
4. implementation PR;
5. independent implementation review;
6. owner-gated true merge;
7. manual demo evidence;
8. roadmap sync.

This document performs **none** of these steps and authorizes **none** of them.

## 13. Boundary preservation

- Official state remains `DEMO_READY_WITH_LIMITATIONS`.
- MVP remains **electronics/electrical-only**.
- Answer Clarification remains inactive.
- Safety Signals remain closed.
- Saved answers remain verbatim.
- The user remains the sole author.
- **No implementation is authorized by this contract PR.**
- `main` remains `0e89e4636399760965c9ff8086b465c90dbadf8e` and is not
  synchronized; the frozen persistence lane remains PRESERVE UNMODIFIED AND PAUSE
  at `aec9cf6409efc18e125b6745762002f59e529654`; the quarantined scratch branch
  remains untouched at `02586747c902d5e1ebb78adde54ddd4ecd1c174a`.

## 14. Final classification

`ARABIC / RTL SUPPORTIVE RESPONSE INCREMENT CONTRACT CREATED — DOCS-ONLY — NO IMPLEMENTATION AUTHORIZED`
