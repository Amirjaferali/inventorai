# LAYER-1 FEEDBACK WORDING / GAP-TYPE-AWARE GUIDANCE — OWNER SCOPE DECISION (POST-PR #112)

## 1. Status

`OWNER SCOPE DECISION — LAYER-1 FEEDBACK WORDING / GAP-TYPE-AWARE GUIDANCE
CANDIDATE; ADMISSION DECISION ONLY; NO IMPLEMENTATION AUTHORIZED; NO SCORING
CHANGE AUTHORIZED`

This document decides only whether a future **Layer-1 feedback-wording /
gap-type-aware guidance** increment should be admitted as a candidate for a
later, separately-authorized Increment Contract. It records an owner scope
decision only. It authorizes NO implementation, code, test, schema, UI,
template, runtime, session, scoring, persistence, or domain change; no
increment contract in this step; no roadmap change beyond a proposed entry
(§10); no `main` synchronization; and no MVP activation of any kind.

File-creation record (per `CLAUDE.md` File Creation Rules):
- File path: `docs/governance/LAYER1_FEEDBACK_WORDING_GAP_TYPE_GUIDANCE_SCOPE_DECISION_POST_PR112.md`
- Purpose: governance evidence artifact recording an owner admission decision.
- Input contract: the read-only Scoring-Behavior Review findings and the merged
  PR #108/#110/#111/#112 record.
- Output contract: a single admission decision (§8) and its boundaries; nothing
  executable, nothing activating.
- Prohibited behaviors: this file must never be read as implementation
  authorization, scoring authorization, an increment contract, or roadmap
  content.

Authoritative context:
- Repository: `Amirjaferali/inventorai`
- Authoritative branch: `feature/atomic-json-session-persistence`
- Authoritative tip: `e755878f3af11f084dcf0627b6817d266100801b`
  (PR #112 roadmap-synchronization true merge)
- Latest merged PR: #112
- Current official state remains: `DEMO_READY_WITH_LIMITATIONS`
- The MVP remains electronics/electrical-only (`MVP_SCOPE_FREEZE.md`).
- `main` remains separate and unchanged
  (`0e89e4636399760965c9ff8086b465c90dbadf8e`); no `main` sync occurred or is
  authorized.
- The frozen persistence worktree remains paused and untouched
  (`aec9cf6409efc18e125b6745762002f59e529654`); the quarantined scratch branch
  remains untouched (`02586747c902d5e1ebb78adde54ddd4ecd1c174a`).

---

## 2. Background

- **PR #108** implemented the More Detail Needed / Guided Answer Scaffolding
  increment as a display-only / guidance-only surface (true-merged at
  `bb70c116a58449ee3e0398d2f986703de5f1fde1`): bounded, deterministic,
  render-time guidance shown when the engine has ALREADY returned a WARN-class
  insufficiency. Scoring was deliberately unchanged.
- **PR #110** recorded a `MANUAL DEMO VERIFICATION PASS` for that implementation
  (true-merged at `20c8a400572ef78fcf158a6271c16c66e694763c`) and explicitly
  re-stated the remaining limitation: the increment improves feedback clarity
  only; scoring behavior is unchanged.
- **PR #111** admitted the Scoring-Behavior Review candidate for a future,
  separately-authorized **read-only review only** (true-merged at
  `ae85171284d1dbcf2b2211bf0766a9814dcd1c99`), with the mandatory four-layer
  separation: (1) feedback wording, (2) scoring thresholds, (3) evidence
  classification, (4) gap-closure logic — layers 2–4 HIGH-RISK /
  benchmark-affecting.
- **PR #112** synchronized the roadmap to record PR #110 and PR #111
  (true-merged at `e755878f3af11f084dcf0627b6817d266100801b`).
- The **read-only Scoring-Behavior Review** (separately owner-authorized after
  PR #112; classification `READ-ONLY SCORING-BEHAVIOR REVIEW COMPLETE — NO
  IMPLEMENTATION PERFORMED — NO SCORING CHANGE AUTHORIZED`) found:
  - current scoring behavior (the `assess_response` ASSERTED/REASONED
    heuristic, the generic-verb trap, and the never-close-on-first-answer gap
    rule) is **intentional, test-locked, characterized behavior** — locked by
    `tests/test_assess_response_replay.py` and
    `tests/test_assess_response_adversarial.py` — and must not be changed now;
  - **Layer 1 (feedback wording)** is the now-eligible, low-risk next step;
  - no scoring change is authorized, and layers 2–4 remain blocked pending the
    PR #111 §9 evidence requirements.

This scope decision is the first governance step for that Layer-1 candidate.

---

## 3. Problem statement

Two user-facing wording problems were identified by the read-only review, both
purely presentational:

1. **First accepted answer mislabeled as deficient.** When a first `REASONED`
   answer is submitted for a gap, `integrate_response` sets the gap `PARTIAL`
   and returns WARN with the reason "`{gap} partially addressed — needs more
   depth`", and the PR #108 guidance lead says "Add more specific detail…". The
   answer, however, already met the quality bar; the deterministic gate simply
   requires a second answer before the gap can close. The current wording can
   mislead users into believing their answer was low-quality when it was
   accepted.
2. **Mechanism-shaped prompts applied to non-mechanism gaps.** The PR #108
   guidance prompts are a fixed, mechanism-shaped set of five, identical across
   all gap types. For `BOUNDARY_AMBIGUITY`, `PHYSICAL_FEASIBILITY`, and
   safety/boundary/limitation-oriented answers, prompts such as "What physical
   part or mechanism does this use?" are off-target and coach the user toward
   the wrong kind of answer.

Neither problem is a scoring defect. Scoring stays as it is; only what the user
is *told* about the already-computed outcome is in scope.

---

## 4. Candidate boundary (what a future Increment Contract WOULD and would NOT cover)

If admitted, the future increment would be **display-only**, in the web layer
only:

- **Display-only wording improvements** for the WARN / More Detail Needed
  surfaces (badge context, guidance lead lines, category prompts).
- **Gap-type-aware guidance prompt sets**, so boundary/feasibility/limitation
  gaps receive prompts about limits, conditions, boundaries, and evidence
  rather than mechanism-shaped prompts.
- An **honest three-way distinction** in the displayed wording between:
  a) a **first accepted/REASONED answer** — the answer met the quality bar and
     one more specific answer on the same topic is needed to close the gap;
  b) an **asserted-only answer** — the answer states what happens but not how
     or why; reasoning is needed;
  c) a **boundary/feasibility/limitation answer** — clarification of limits,
     operating conditions, or supporting evidence is needed.
- **Web-layer display mapping only**: wording is derived by mapping the
  already-computed `last_result` reason (and the current `gap_type`) to display
  text — the same pattern PR #108 established in `web/scaffolding_guidance.py`.
- **Engine untouched by default.** Engine reason strings
  (`engine/progression_loop.integrate_response`) are load-bearing — the PR #108
  surface classifies on their substrings, and they sit adjacent to
  replay/fixture surfaces. They must NOT be changed under this scope. Only a
  future contract that explicitly proves such a change safe (with regression
  and replay evidence) could ever touch them; the default disposition for this
  candidate is: engine reason strings unchanged.

The future increment's only permitted effect is different *display text* for
outcomes the engine already computed. It must never change any PASS/WARN/BLOCK
outcome, any gap status, any maturity level, any stored answer, or any
Evidence record.

---

## 5. Explicit non-goals

This scope decision, and any increment admitted by it, does NOT authorize and
must NOT perform:

- any scoring change (`assess_response` or otherwise);
- any threshold change (length, classification, or numeric);
- adding causal tokens (e.g. `because`, `since`) to
  `_CAUSAL_STRUCTURE_PATTERNS` or any token list — that is a Layer-2 scoring
  change, not wording;
- any generic-verb trap change;
- any gap-closure logic change (`integrate_response` semantics,
  `evaluate_transition`, the two-answer close requirement);
- any evidence-classification change (Increment 2 truthful-state model);
- any persistence/schema change;
- activation of the Inventor Answer Clarification / Improve Wording Assistant,
  or introduction of `suggested_clarified_answer` / `user_approved_answer` /
  `original_user_answer` / `clarification_status`;
- any stored-answer modification — the inventor's answer text remains
  byte-for-byte untouched;
- any domain expansion;
- any deliverable-generation change;
- any change to WPS001 benchmark behavior, golden fixtures, or replay
  baselines;
- any `main` synchronization;
- any modification of the frozen persistence worktree or use of the
  quarantined scratch branch;
- any implementation — this scope decision authorizes NO implementation.

---

## 6. Required future contract questions

A future Increment Contract (itself separately owner-gated) must answer, at
minimum:

1. Which gap types need distinct prompt sets, and what are the exact bounded,
   neutral, content-free prompts for each?
2. How should the UI distinguish the first REASONED/`PARTIAL` outcome from the
   ASSERTED-only outcome, using only the already-computed `last_result`?
3. Can all wording be mapped from `last_result` reason + `gap_type` in the web
   layer without changing engine reason strings? (Default answer must be yes;
   any "no" requires its own safety proof.)
4. What regression tests are required to prove PASS/WARN/BLOCK outcomes,
   maturity transitions, stored answers, gap statuses, and scoring
   (`assess_response` results) remain bit-identical before/after the change?
5. How will the forbidden Answer Clarification fields
   (`suggested_clarified_answer` / `user_approved_answer` /
   `original_user_answer` / `clarification_status`) be guarded (tests asserting
   absence, as in PR #108)?
6. How will the contract prove that no guidance text writes, rewrites,
   validates, approves, or improves the user's answer — i.e. that the surface
   remains category-level, content-free, and non-mutating?

---

## 7. Governance risks

- **Wording-becomes-scoring risk.** Editing engine reason strings would ripple
  into the PR #108 substring classification and replay/fixture surfaces — a
  wording change silently becoming an engine/benchmark-adjacent change. Hence
  the hard boundary: web-layer mapping only; engine reason strings untouched by
  default.
- **Advice-generation creep.** Gap-type-aware prompts could drift from bounded
  category-level questions into suggesting answer content — which would be the
  (non-authorized) Answer Clarification feature by another name. Prompts must
  remain content-free and deterministic.
- **Truth-masking risk.** Better wording must not hide the truthful WARN state.
  A first-REASONED WARN is still WARN; the display must keep the honest gap
  status visible while explaining it accurately.
- **State-effect risk.** Display-only improvements must not advance maturity,
  close gaps, create Evidence, or satisfy any transition gate. The PR #108
  boundaries carry forward unchanged.
- **Authority-conflation risk.** This Layer-1 candidate must never be bundled
  with any Layer 2–4 (scoring/evidence/gap-closure) direction in a single
  authorization, per the PR #111 four-layer separation.

---

## 8. Product UX risks

- **If nothing is done:** users who gave a useful, accepted first answer will
  continue to read "needs more depth" as a quality judgment and may feel
  punished for a good answer; boundary/feasibility answers will continue to
  receive mismatched mechanism-shaped coaching.
- **If wording is over-softened:** users may believe a gap is closed or the
  idea approved when it is not — against the Increment 2 truthful-state
  principle and the advisory-only framing. Wording must stay honest: WARN means
  the gap is still open.
- **If prompts remain mechanism-shaped:** non-mechanism gaps will keep coaching
  users toward the wrong answer kind, prolonging the More Detail Needed loop
  the PR #108 increment was meant to soften.

---

## 9. Decision

The **Layer-1 Feedback Wording / Gap-Type-Aware Guidance** candidate is
**ADMITTED FOR A FUTURE, SEPARATELY-AUTHORIZED INCREMENT CONTRACT ONLY**, on
condition that any such contract honors the candidate boundary (§4), the
non-goals (§5), and answers the required contract questions (§6).

Admission means only that the candidate may proceed to an Increment Contract
under a separate owner authorization. This decision does NOT:

- authorize implementation;
- start implementation;
- start any scoring change;
- start test-only characterization (that remains a separate candidate requiring
  its own owner authorization).

Any subsequent work must proceed, in order, through: this scope decision
(admission only); a separately authorized Increment Contract; a separate
implementation authorization; tests; independent review; and an owner-gated
true merge. The app remains electronics/electrical-only for the MVP, and the
current official state remains `DEMO_READY_WITH_LIMITATIONS`, until separate
governed decisions state otherwise.

---

## 10. Roadmap handling (proposed only)

A roadmap entry recording this scope decision is **proposed only** and is NOT
made by this document. Per repository governance, roadmap synchronization is a
separate, owner-gated documentation step performed after (and if) this scope
decision is merged. This document changes no roadmap file.

---

## 11. Final classification

`SCOPE DECISION ONLY — LAYER-1 FEEDBACK WORDING / GAP-TYPE-AWARE GUIDANCE
ADMITTED FOR FUTURE CONTRACT ONLY — NO IMPLEMENTATION AUTHORIZED — NO SCORING
CHANGE AUTHORIZED`
