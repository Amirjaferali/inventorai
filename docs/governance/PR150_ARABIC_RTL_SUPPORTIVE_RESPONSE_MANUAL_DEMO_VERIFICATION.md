# PR #150 — Arabic / RTL Supportive Response — Manual Demo Verification

## 1. Evidence state

- **Repository:** `Amirjaferali/inventorai`
- **Authoritative branch:** `feature/atomic-json-session-persistence`
- **Starting authoritative SHA (at time of demo):** `c4a309fc688b99284f2c9270f606306b4190e492`
- **PR number:** `#150`
- **PR #150 merge commit:** `c4a309fc688b99284f2c9270f606306b4190e492`
- **Ordered parents:**
  - First parent: `5822199c08a78670a38c2fa483e821cc0bfa1942`
  - Second parent: `44760732abb8ea3f2f80f84d7dad00cf5816a354`
- **Implemented increment:** Arabic / RTL Supportive Response (display-only, contract-bounded)
- **Official state:** `DEMO_READY_WITH_LIMITATIONS`
- **MVP scope:** electronics/electrical-only

## 2. Method used

Runtime exercise of the **merged, committed** Flask application via the Flask
test client (the repository's established manual-demo verification pattern for
display-only web changes — see PR #130 / PR #137 / PR #143 evidence records).
The app was imported and driven inside a **read-only detached worktree** checked
out at the merge tip `c4a309fc688b99284f2c9270f606306b4190e492`, exercising the
committed session route (`POST /start`, `POST`/`GET /session/<sid>`). The demo
observed the rendered HTML and the in-memory session state only.

- **No source, test, or template change** was made to perform the demo.
- **No artifact** was created during the demo step itself.
- The temporary worktree was **removed afterward**.

This document records observed behavior of the committed merge; it reimplements,
re-derives, and re-scores nothing.

## 3. Demo scenarios and observed results

### Scenario 1 — Arabic uncertainty input (`لا أعرف`)
- Uncertainty support panel renders: **yes**.
- Panel uses the pinned Arabic copy (eyebrow `اختياري — بدون ضغط`, heading `لا بأس — لنأخذها خطوة بخطوة.`): **yes**.
- Panel container has `lang="ar"` and `dir="rtl"`: **yes**.
- Page shell remains `<html lang="en">`: **yes**.
- English eyebrow (`Optional — no pressure`) absent for Arabic: **yes**.

### Scenario 2 — English uncertainty input (`I don't know`)
- Uncertainty support panel renders: **yes**.
- English copy retained (eyebrow `Optional — no pressure`): **yes**.
- Panel container has `lang="en"` and `dir="ltr"`: **yes**.
- Page shell remains `<html lang="en">`: **yes**.
- No `dir="rtl"` anywhere on the page: **yes**.

### Scenario 3 — Mixed-language uncertainty input (`I don't know لا أعرف`)
- Arabic wins the tie-break (Arabic copy renders): **yes**.
- Panel container has `lang="ar"` and `dir="rtl"`: **yes**.
- English eyebrow absent: **yes**.

### Scenario 4 — Non-uncertainty input
- A normal answer (`It opens a relay when current exceeds a threshold.`) renders
  **no** uncertainty guidance panel: **yes**.

### Scenario 5 — Precedence (Arabic uncertainty in a forced WARN state)
- Uncertainty is the single primary supportive panel (`primaries == ["uncertainty"]`);
  scaffolding/WARN and co-authoring do **not** compete: **yes**.
- Exactly six honest actions present (`name="action"` count = 6): **yes**.
- Exactly one `dir="rtl"` in the whole page (RTL scoped to the panel only): **yes**.

### Scenario 6 — Verbatim save
- Arabic user answer (`لا أعرف كيف يعمل الحساس بعد.`) saved verbatim in the transcript: **yes**.
- Guidance/prompt text is **not** persisted as answer content: **yes**.
- English user answer (`The ESP32 reads the sensor and opens a relay above 5V.`) saved verbatim: **yes**.

### Scenario 7 — Forbidden behavior (none present)
- No Answer Clarification / Improve Wording or approve/apply/save-clarified flow: **absent**.
- No hidden clarified-answer fields in HTML (`original_user_answer` / `suggested_clarified_answer` / `user_approved_answer` / `clarification_status`): **absent**.
- No such fields on the IdeaState: **absent**.
- No validation / safety / compliance / patent-readiness claim: **absent**.
- No full-page RTL and no full product localization (page stays `<html lang="en">`, ≤1 `dir="rtl"`): **confirmed**.

## 4. Pass/fail table

| # | Scenario | Result |
|---|----------|--------|
| 1 | Arabic uncertainty → Arabic copy, `lang="ar"`/`dir="rtl"`, shell `lang="en"` | PASS |
| 2 | English uncertainty → English copy, `lang="en"`/`dir="ltr"`, no page RTL | PASS |
| 3 | Mixed input → Arabic wins, `lang="ar"`/`dir="rtl"` | PASS |
| 4 | Non-uncertainty → no uncertainty panel | PASS |
| 5 | Precedence → uncertainty sole primary; six actions; one RTL (panel-scoped) | PASS |
| 6 | Verbatim save (Arabic + English); guidance not persisted | PASS |
| 7 | No clarification flow / hidden fields / readiness claim / full-page RTL | PASS |

All scenarios: **PASS**.

## 5. Explicit limitations

- **Partial localization by design.** Only the uncertainty support panel is
  localized to Arabic and flipped to RTL. The page shell, badges, gaps,
  directions, action labels, and all other chrome remain English and LTR. This
  is the contract-defined scope, not full product localization.
- The RTL treatment is scoped to the uncertainty panel container only; the page
  remains `<html lang="en">` LTR.
- Uncertainty detection remains the existing curated, conservative English +
  Arabic cue set; this increment adds the Arabic **response** and RTL rendering,
  not broader language detection.

## 6. Boundary confirmations

- **No source/test/runtime/schema/scoring/persistence/transcript/deliverable/report/domain-gate behavior changed** by this demo step (read-only; the merged behavior was observed, not altered). `web/app.py` was not changed by PR #150.
- **Answer Clarification / Improve Wording remains inactive** (no such flow or fields observed).
- **Safety Signals remain closed** (`engine/safety_signal.py` untouched by PR #150; no safety surface reopened).
- **No roadmap sync occurred** in this step (`ACTIVE_EXECUTION_ROADMAP.md` not modified).
- Official state remains `DEMO_READY_WITH_LIMITATIONS`; MVP remains electronics/electrical-only.
- `main` remains `0e89e4636399760965c9ff8086b465c90dbadf8e`; the frozen persistence lane remains `PRESERVE UNMODIFIED AND PAUSE` at `aec9cf6409efc18e125b6745762002f59e529654`; the quarantined scratch branch remains untouched at `02586747c902d5e1ebb78adde54ddd4ecd1c174a`.

## 7. Final classification

`PR #150 MANUAL DEMO VERIFICATION — ARABIC / RTL SUPPORTIVE RESPONSE VERIFIED — DOCS-ONLY EVIDENCE — NO IMPLEMENTATION AUTHORIZED — ROADMAP SYNC STILL REQUIRED`
