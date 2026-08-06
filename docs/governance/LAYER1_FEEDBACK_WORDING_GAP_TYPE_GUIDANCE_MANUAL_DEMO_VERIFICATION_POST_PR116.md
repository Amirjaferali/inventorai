# LAYER-1 FEEDBACK WORDING / GAP-TYPE-AWARE GUIDANCE — MANUAL DEMO VERIFICATION (POST-PR #116)

## 1. Status

`MANUAL DEMO VERIFICATION PASS — PR #116 LAYER-1 FEEDBACK WORDING / GAP-TYPE-AWARE
GUIDANCE — NO SCORING CHANGE — NO ANSWER CLARIFICATION`

This document is a **documentation-only evidence record**. It reports a
read-only / runtime-only manual demo (smoke) verification of the merged PR #116
Layer-1 Feedback Wording / Gap-Type-Aware Guidance implementation, performed
against the authoritative tip. It changes no code, tests, runtime, scoring,
engine, domain, persistence, schema, template, or deliverable behavior; it
authorizes no implementation; and it makes no roadmap change.

File-creation record (per `CLAUDE.md` File Creation Rules):
- File path: `docs/governance/LAYER1_FEEDBACK_WORDING_GAP_TYPE_GUIDANCE_MANUAL_DEMO_VERIFICATION_POST_PR116.md`
- Purpose: governance evidence artifact recording the manual demo verification of
  the merged PR #116 implementation.
- Input contract: the merged PR #116 implementation
  (`web/scaffolding_guidance.py`), the merged PR #115 Increment Contract, and a
  runtime observation via the Flask test client.
- Output contract: per-scenario inputs, observed outputs, and pass/fail results
  (§4), plus the confirmations (§5); nothing executable, nothing activating.
- Prohibited behaviors: this file must never be read as implementation
  authorization, scoring authorization, or roadmap content; it records evidence
  only.

Authoritative context (evidence-locked):
- Repository: `Amirjaferali/inventorai`
- Authoritative branch: `feature/atomic-json-session-persistence`
- Current tip verified: `6b6d2ef7632e4be4a7c794893e0f1d8f119279f1` (PR #116 merge)
- PR #116 merge commit: `6b6d2ef7632e4be4a7c794893e0f1d8f119279f1`, exactly two
  ordered parents — base `d6de1b404dc7a1177f12f555543f942c019117dd` (PR #115
  contract merge) then head `7e5df1d0246a647ce72a76415e7490e1e66b14ea` (accepted
  implementation head).
- Changed files from PR #116 (exactly two): `web/scaffolding_guidance.py`
  (+133/−24, display-only helper) and `tests/test_layer1_feedback_wording.py`
  (+240, new tests). No engine/scoring/persistence/schema/domain/deliverable/
  template file changed.
- Current official state remains: `DEMO_READY_WITH_LIMITATIONS`
- The MVP remains electronics/electrical-only (`MVP_SCOPE_FREEZE.md`).
- `main` remains separate and unchanged
  (`0e89e4636399760965c9ff8086b465c90dbadf8e`).
- The frozen persistence worktree remains paused and untouched
  (`aec9cf6409efc18e125b6745762002f59e529654`); the quarantined scratch branch
  remains untouched (`02586747c902d5e1ebb78adde54ddd4ecd1c174a`).

---

## 2. Verification method

- **Test/client path used:** the in-process Flask WSGI test client
  (`web.app.app.test_client()`), driving the real `GET /session/<sid>` render
  path and the real `POST /start` domain-gate path. Session state was seeded
  directly into `web.app.SESSION_STORE` (the same store the routes read), using
  `engine.idea_state.IdeaState`, so the rendered output is produced by the real
  application code at the verified tip.
- **Read-only:** no route that mutates persisted repository state was exercised;
  the verification created only in-memory sessions (popped after each scenario)
  and made no file, index, or branch change. Post-run `git status --short` in the
  verification worktree was empty (no repository mutation).
- The observed guidance text below is the deterministic output of
  `web.scaffolding_guidance.get_scaffolding_guidance(last_result, gap_type)` as
  rendered into the session page.

---

## 3. Guidance text observed at the verified tip (reference)

Asserted-only (case b) and first-accepted/PARTIAL (case a) leads, per gap family:

- **MECHANISM_COMPLETENESS**
  - asserted lead: "Your answer says what happens, but not how or why it works.
    Add the missing mechanism or reasoning — describe what makes it work."
  - partial lead: "Good — this answer was accepted and counts toward this point.
    The system needs one more specific answer about how it works before it can
    close, so add one more concrete detail — a part, a trigger condition, or what
    it senses."
  - prompts: physical part/mechanism; trigger condition; sense/detect; output/
    response; supporting evidence.
- **BOUNDARY_AMBIGUITY**
  - asserted lead: "Your answer names a limit or scope, but not the reasoning
    behind it. Explain why that boundary holds — the conditions or assumptions
    that set it."
  - partial lead: "Good — this answer was accepted and counts toward this point.
    The system needs one more specific answer about scope or limits before it can
    close, so add one more concrete detail — what it does not do, or a condition
    where it stops applying."
  - prompts: in scope / what it deliberately does NOT do; limits/boundaries of
    where it applies; operating conditions or assumptions; edge cases or
    exceptions; supporting evidence for the limits.
- **PHYSICAL_FEASIBILITY**
  - asserted lead: "Your answer states that it works, but not the reasoning.
    Explain the conditions, limits, or constraints that make it work."
  - partial lead: "Good — this answer was accepted and counts toward this point.
    The system needs one more specific answer about the physical limits or
    conditions before it can close, so add one more concrete detail — a
    constraint or operating range."
  - prompts: physical limits/operating range; conditions or constraints that must
    hold; environmental assumptions; what could physically prevent it; supporting
    evidence that it can work.

---

## 4. Scenarios, inputs, observed outputs, results

**Scenario 1 — normal WARN / More Detail Needed renders guidance.**
Input: session with `last_result` = WARN, reason
`MECHANISM_COMPLETENESS asserted only — reasoning required`.
Observed: the guidance panel rendered (heading "What kind of detail to add"), and
the lead asked for the missing reasoning. **PASS.**

**Scenario 2 — first accepted/REASONED answer still WARN, honest wording.**
Input: session with stored answer "the plug senses current and cuts power" and
`last_result` = WARN, reason
`MECHANISM_COMPLETENESS partially addressed — needs more depth`.
Observed lead: "Good — this answer was accepted and counts toward this point. The
system needs one more specific answer about how it works before it can close, so
add one more concrete detail — a part, a trigger condition, or what it senses."
Checks: guidance shown while outcome is still WARN; the wording says the answer
was **accepted / counts toward this point**; it says **one more** specific answer
is needed; it says the gap can **close** only after that (gap not closed yet); it
contains **no** quality-slur term (weak / poor / insufficient / inadequate /
deficient); the stored answer was byte-for-byte unchanged. **PASS.**

**Scenario 3 — boundary / feasibility guidance is not mechanism-only.**
Inputs: WARN sessions with reasons `BOUNDARY_AMBIGUITY asserted only — reasoning
required` and `PHYSICAL_FEASIBILITY asserted only — reasoning required`.
Observed: boundary guidance asked about scope / limits and "what it does not do";
feasibility guidance asked about operating range / constraints and "what could
prevent it from working". Both differed from the mechanism prompt set. **PASS.**

**Scenario 4 — original submitted answer unchanged (byte-for-byte).**
Input: WARN session with stored answer "The sensor detects current; the MCU opens
the relay." rendered once.
Observed: the stored transcript compared equal to a pre-render deep copy
(byte-for-byte identical). **PASS.**

**Scenario 5 — no Answer Clarification / Improve Wording flow.**
Input: WARN (asserted-only) session rendered.
Observed: rendered body contained none of the clarification-flow markers
("Improve Wording", "Approve this answer", `suggested_clarified_answer`,
`user_approved_answer`). **PASS.**

**Scenario 6 — forbidden fields do not appear.**
Input: rendered WARN sessions (scenarios 2/4/5).
Observed: none of `suggested_clarified_answer` / `user_approved_answer` /
`original_user_answer` / `clarification_status` was present on the `IdeaState`
object, in the session-store record, or in the rendered body. **PASS.**

**Scenario 7 — PASS renders no More Detail Needed guidance.**
Input: session with `last_result` = PASS (reason "good", direction "PROGRESSING").
Observed: the guidance heading "What kind of detail to add" was absent from the
rendered body. **PASS.**

**Scenario 8 — unsupported-domain rejection still works.**
Inputs: `POST /start` with "a gearbox with a rotating shaft and bearing torque"
(domain-confirmed) and with "ESP32 microcontroller circuit with a voltage sensor".
Observed: the gearbox idea returned HTTP 200 with the unsupported-domain message
and created no session; the ESP32 idea returned HTTP 302 into a session. **PASS.**

**Scenario 9 — scoring behavior unchanged from PR #116 claims.**
Basis: PR #116 changed only `web/scaffolding_guidance.py` (display) and a test
file; `engine/progression_loop.py` (which holds `assess_response`,
`integrate_response`, `evaluate_transition`, the generic-verb trap, and the
gap-closure logic) was not changed. The locked scoring suites
`tests/test_assess_response_replay.py` and
`tests/test_assess_response_adversarial.py` pass unchanged at the verified tip.
No scoring / threshold / causal-token / generic-verb / gap-closure /
evidence-classification change occurred. **PASS.**

**Scenario 10 — no engine/scoring/persistence/schema/domain/deliverable/template
behavior changed.**
Basis: the PR #116 merge diff versus its base parent changed exactly two files
(`web/scaffolding_guidance.py`, `tests/test_layer1_feedback_wording.py`); no
`engine/*`, persistence, schema, domain, deliverable-generation, or template file
was changed, and the guidance dict shape `{heading, lead, prompts, note}` is
unchanged (no template edit required). **PASS.**

Summary: **10 / 10 scenarios PASS.**

---

## 5. Confirmations

- **Original answers remained unchanged** — stored transcripts were byte-for-byte
  identical before and after rendering (Scenarios 2 and 4).
- **No Answer Clarification / Improve Wording flow appeared** — no clarification
  markers and no forbidden fields in state, session store, or rendered body
  (Scenarios 5 and 6).
- **No repository mutation occurred during verification** — the run created only
  in-memory sessions; post-run `git status --short` in the verification worktree
  was empty.
- **No scoring change and no Answer Clarification** — engine/scoring code
  untouched; locked scoring suites pass; no forbidden field or flow introduced.
- The app remains electronics/electrical-only for the MVP, and the current
  official state remains `DEMO_READY_WITH_LIMITATIONS`.

---

## 6. Roadmap handling (proposed only)

A roadmap entry recording PR #116 and this evidence note is **proposed only** and
is NOT made by this document. Per repository governance, roadmap synchronization
is a separate, owner-gated documentation step performed after (and if) this
evidence note is merged. This document changes no roadmap file.

---

## 7. Final classification

`MANUAL DEMO VERIFICATION PASS — PR #116 LAYER-1 FEEDBACK WORDING / GAP-TYPE-AWARE
GUIDANCE — NO SCORING CHANGE — NO ANSWER CLARIFICATION`
