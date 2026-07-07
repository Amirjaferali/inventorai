# LAYER-1 FEEDBACK WORDING / GAP-TYPE-AWARE GUIDANCE — INCREMENT CONTRACT (POST-PR #114)

## 1. Status

`INCREMENT CONTRACT PROPOSAL ONLY — LAYER-1 FEEDBACK WORDING / GAP-TYPE-AWARE
GUIDANCE — NO IMPLEMENTATION STARTED — NO SCORING CHANGE AUTHORIZED`

This document is a **contract proposal only**. It defines the bounded scope, the
non-goals, the design constraints, the required tests, and the required demo
verification for a **future, separately-authorized, display-only implementation**
of improved WARN / More Detail Needed wording and gap-type-aware guidance
prompts. It is **not** implementation authorization. No implementation, code,
test, schema, UI, template, runtime, session, scoring, persistence, or domain
change is authorized or begun by this document. Implementation may begin only
after this contract itself passes independent review and an owner-gated true
merge, and then only under a **separate** owner implementation authorization
(§8).

File-creation record (per `CLAUDE.md` File Creation Rules):
- File path: `docs/governance/LAYER1_FEEDBACK_WORDING_GAP_TYPE_GUIDANCE_INCREMENT_CONTRACT.md`
- Purpose: governance contract artifact defining a future display-only Layer-1
  increment's exact scope, boundaries, tests, and demo requirements.
- Input contract: the PR #113 Layer-1 owner scope decision
  (`LAYER1_FEEDBACK_WORDING_GAP_TYPE_GUIDANCE_SCOPE_DECISION_POST_PR112.md`), the
  PR #114 read-only Scoring-Behavior Review evidence artifact
  (`SCORING_BEHAVIOR_REVIEW_READ_ONLY_FINDINGS_POST_PR112.md`), and the merged
  PR #108/#110/#111/#112/#113/#114 record.
- Output contract: a single bounded increment contract (§4–§9) and its final
  authorization classification (§11); nothing executable, nothing activating.
- Prohibited behaviors: this file must never be read as implementation
  authorization, scoring authorization, an owner implementation authorization,
  or roadmap content; it authorizes no code, test, or scoring change; it starts
  no implementation.

Authoritative context (evidence-locked at authorship):
- Repository: `Amirjaferali/inventorai`
- Authoritative branch: `feature/atomic-json-session-persistence`
- Authoritative tip: `03e2bf041c42beb052ed49095db3cdb0cc29dc43` (PR #114 merge)
- Latest merged PR: #114
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

- **PR #108** delivered the current display-only More Detail Needed / Guided
  Answer Scaffolding surface (`web/scaffolding_guidance.py`,
  `web/templates/session.html`, render-context wiring in `web/app.py`): bounded,
  deterministic, render-time guidance shown when the engine has ALREADY returned
  a WARN-class insufficiency. Scoring was deliberately unchanged.
- **PR #110** recorded a `MANUAL DEMO VERIFICATION PASS` for that implementation
  and re-stated the remaining limitation (feedback-clarity improvement only;
  scoring unchanged).
- **PR #111** admitted the Scoring-Behavior Review candidate for a future,
  separately-authorized **read-only review only**, with the mandatory four-layer
  separation: (1) feedback wording, (2) scoring threshold, (3) evidence
  classification, (4) gap-closure logic — layers 2–4 HIGH-RISK/benchmark-
  affecting.
- **PR #112** synchronized the roadmap for PR #110 and PR #111.
- **PR #113** admitted the **Layer-1 Feedback Wording / Gap-Type-Aware Guidance**
  candidate for a future, separately-authorized Increment Contract only.
- **PR #114** committed the completed read-only Scoring-Behavior Review evidence
  artifact (`SCORING_BEHAVIOR_REVIEW_READ_ONLY_FINDINGS_POST_PR112.md`) and
  recorded PR #113 in the roadmap.

The read-only Scoring-Behavior Review found:
1. Current scoring behavior (the `assess_response` ASSERTED/REASONED heuristic,
   the generic-verb trap, and the never-close-a-gap-on-a-first-answer rule) is
   intentional, characterized, and **test-locked** by
   `tests/test_assess_response_replay.py` and
   `tests/test_assess_response_adversarial.py`; it **must not be changed now**.
2. A WARN after a first `REASONED` answer can imply a quality deficiency even
   when the answer met the quality bar and the deterministic gate merely requires
   a second answer to close the gap.
3. The current PR #108 guidance prompts are mechanism-shaped and identical across
   all gap types.
4. Boundary/feasibility/safety-style gaps need better display guidance than the
   mechanism-shaped prompts.
5. Layers 2–4 remain high-risk and blocked pending future evidence (PR #111 §9).

This contract addresses **findings 2, 3, and 4 only**, strictly as a Layer-1
display-only increment. It does not touch findings 1 and 5.

---

## 3. Factual anchors (confirmed from code at the authoritative tip)

- The WARN `reason` strings that drive the current guidance are produced by
  `engine.progression_loop.integrate_response` (e.g.
  "`{gap} partially addressed — needs more depth`" for a first `REASONED`
  answer setting the gap `PARTIAL`; "`{gap} asserted only — reasoning required`"
  for an asserted-only answer). These strings are **load-bearing**: the PR #108
  surface classifies on their substrings, and they sit adjacent to
  replay/fixture surfaces.
- `assess_response`, `integrate_response`, `evaluate_transition`, and the
  causal-structure / generic-verb logic all live in `engine/progression_loop.py`.
  These are the Layer-2/Layer-4 surfaces this contract must NOT change.
- The current display surface is `web/scaffolding_guidance.py`
  (`get_scaffolding_guidance(last_result, gap_type)` → a bounded dict or `None`)
  plus its additive block in `web/templates/session.html` and the render-context
  wiring in `web/app.py`. This is the Layer-1 surface this contract governs.
- Gap type/category context is available to the web layer as `gap_type` (the
  current gap id), already accepted by `get_scaffolding_guidance` as display
  context only.

---

## 4. Authorized future implementation boundary

If, and only if, this contract is independently reviewed and owner-merged, and a
**separate** owner implementation authorization is then issued (§8), the future
implementation is bounded to:

- **Web-layer display mapping only.** All wording is derived at render time by
  mapping the already-computed `last_result` reason (and the available
  `gap_type` / gap category) to display text — the pattern PR #108 established in
  `web/scaffolding_guidance.py`. No new engine call, no AI/generative call, no
  network, no persistence, no stored state.
- **Gap-type-aware guidance prompts.** Boundary/feasibility/limitation/safety-
  style gaps receive prompts about limits, operating conditions, boundaries, and
  supporting evidence, rather than the fixed mechanism-shaped set; mechanism-
  style gaps keep mechanism-appropriate prompts.
- **User-facing wording that honestly distinguishes three cases**, using only
  the already-computed outcome:
  a) a **first accepted / `REASONED` answer** whose gap is `PARTIAL` — the answer
     met the quality bar and one more specific answer on the same topic is needed
     to close the gap (must NOT read as a quality judgment);
  b) an **asserted-only answer** — the answer states what happens but not how or
     why; reasoning is needed;
  c) a **boundary / feasibility / limitation answer** — clarification of limits,
     operating conditions, or supporting evidence is needed.
- **Deterministic guidance text only.** Fixed, bounded, content-free wording
  selected by classification of the existing outcome; no generated prose.
- **Strictly excluded from the surface:** no AI generation; no answer rewriting;
  no answer-improvement flow; no user-approved-answer flow; no stored-answer
  mutation.

The future increment's **only** permitted effect is different *display text* for
outcomes the engine already computed. It must never change any PASS/WARN/BLOCK
outcome, any gap status, any maturity level, any stored answer, or any Evidence
record.

---

## 5. Explicit non-goals

This contract, and any implementation it may later authorize, does NOT authorize
and must NOT perform:

- any scoring change (`assess_response` or otherwise);
- any threshold change (length, classification, or numeric);
- adding causal tokens (e.g. `because`, `since`) to
  `_CAUSAL_STRUCTURE_PATTERNS` or any token list — that is a Layer-2 scoring
  change, not wording;
- any generic-verb trap change;
- any gap-closure logic change (`integrate_response` semantics,
  `evaluate_transition`, the two-`REASONED`-answers-per-gap close requirement,
  mechanism-completeness expectations);
- any evidence-classification change (Increment 2 truthful-state model);
- any edit to engine reason strings
  (`engine/progression_loop.integrate_response`) — **default disposition:
  engine untouched.** Only a future, separate authorization that explicitly
  proves such a change safe (with regression and replay/fixture evidence) could
  ever touch them; if implementation finds it cannot proceed without editing
  them, it must STOP and escalate for separate authority (§7);
- any persistence/schema change;
- any stored-answer modification — the inventor's answer text remains
  byte-for-byte untouched;
- activation of the Inventor Answer Clarification / Improve Wording Assistant, or
  introduction of any of `suggested_clarified_answer` / `user_approved_answer` /
  `original_user_answer` / `clarification_status` (or any equivalent);
- any domain expansion;
- any deliverable-generation change;
- any change to WPS001 benchmark behavior, golden fixtures, or replay baselines;
- any `main` synchronization;
- any modification of the frozen persistence worktree or use of the quarantined
  scratch branch.

---

## 6. Required implementation design constraints

A future implementation authorized under this contract MUST satisfy:

1. **Web-layer mapping/helper.** Wording is produced by a pure, deterministic
   web-layer mapping/helper (extending or paralleling
   `web/scaffolding_guidance.py`) that translates the existing `last_result`
   reason plus the available `gap_type` / gap category into display text. No
   engine, scoring, persistence, or network dependency.
2. **Engine reason strings unchanged by default.** The existing
   `engine/progression_loop.integrate_response` reason strings must remain
   unchanged. If the implementation cannot meet its goals without editing them,
   it must BLOCK implementation and escalate for separate owner authority rather
   than editing them.
3. **Outcomes byte-for-byte equivalent.** PASS/WARN/BLOCK outcomes must remain
   byte-for-byte equivalent for the tested cases before and after the change.
4. **No state effects.** Maturity level, gap status, stored user answers, session
   persistence behavior, and deliverables must remain unchanged.
5. **Clarification, not authorship.** Guidance must ask the user for
   clarification but must NOT provide invented components, numbers, claims,
   validation statements, readiness statements, or suggested final answers.
6. **Deterministic and content-free.** Guidance must remain deterministic and
   content-free enough that it cannot become Answer Clarification by stealth —
   category-level, neutral, non-mutating prompts only.
7. **Honest truth preserved.** Improved wording must keep the truthful WARN state
   visible: a first-`REASONED`/`PARTIAL` WARN is still WARN; the display must
   explain it accurately without implying the gap is closed or the idea approved.

---

## 7. Escalation / stop condition

If, during a future implementation, any required behavior appears to demand a
change outside §4 (for example, editing an engine reason string, changing a
classification, or touching gap-closure logic), the implementation MUST STOP,
leave the engine and scoring untouched, and report the blocker for a separate
owner authorization. Wording work must never silently become scoring or
gap-closure work.

---

## 8. Required tests for the future implementation

A future implementation authorized under this contract MUST include tests that
prove:

1. **Scoring output unchanged** — `assess_response` results are identical for
   representative inputs before/after the change.
2. **Transition outcome unchanged** — PASS/WARN/BLOCK transitions are identical
   for the tested cases.
3. **Stored answer unchanged** — the inventor's stored answer text is
   byte-for-byte unchanged after rendering.
4. **No forbidden Answer-Clarification fields** — none of
   `suggested_clarified_answer` / `user_approved_answer` / `original_user_answer`
   / `clarification_status` exists on state, session store, or rendered body.
5. **First `REASONED`/`PARTIAL` display wording** — the honest first-accepted
   wording (case 4.a) is rendered for a first `REASONED` answer whose gap is
   `PARTIAL`, and does not read as a quality-deficiency judgment.
6. **ASSERTED-only display wording** — the reasoning-needed wording (case 4.b) is
   rendered for an asserted-only answer.
7. **Gap-type-aware guidance differences** — at least boundary/feasibility vs.
   mechanism-style gaps render distinct, appropriate prompt sets (case 4.c vs.
   mechanism).
8. **PASS renders no guidance** — a PASS outcome renders no More Detail Needed
   guidance.
9. **Unsupported-domain rejection unchanged** — the Domain Gate still rejects
   unsupported ideas and admits electronics/electrical ideas unchanged.

Test evidence must record any full-suite baseline (the known pre-existing
`tests/test_domain_registry.py` failures are the only permitted baseline
failures; zero new failures introduced).

---

## 9. Required demo verification for the future implementation

A future implementation authorized under this contract MUST pass a read-only /
runtime-only manual demo (smoke) verification showing:

1. A normal user WARN case renders the guidance surface.
2. A first accepted / `REASONED` answer still correctly WARNs, but with honest
   wording (not a quality-deficiency message).
3. Boundary/feasibility-style guidance is NOT mechanism-only (gap-type-aware).
4. The original answer remains unchanged (byte-for-byte).
5. No Answer Clarification / Improve Wording flow appears.

The demo evidence must be recorded as a separate governance evidence note (as in
PR #110), under its own separate authorization.

---

## 10. Governance and product risks

- **Wording-becomes-scoring risk.** Editing engine reason strings would ripple
  into PR #108 substring classification and replay/fixture surfaces — a wording
  change silently becoming an engine/benchmark-adjacent change. Mitigation: §4
  web-layer mapping only; §6.2 engine reason strings unchanged by default;
  §7 stop/escalate.
- **Guidance-becomes-answer-writing risk.** Gap-type-aware prompts could drift
  from bounded category-level questions into suggesting answer content — the
  (non-authorized) Answer Clarification feature by another name. Mitigation:
  §5 forbidden fields/flows; §6.5–§6.6 clarification-not-authorship, deterministic
  and content-free; §8.4 forbidden-field tests.
- **Over-softening risk.** Better wording must not make a user believe a gap is
  closed or the idea approved when it is not — against the Increment 2 truthful-
  state principle. Mitigation: §6.7 honest-truth constraint; §8.5 first-REASONED
  wording test.
- **Replay/fixture-breakage risk.** Editing engine reason strings could break
  replay and golden-fixture surfaces. Mitigation: §5/§6.2 engine untouched by
  default; §7 escalation.
- **Premature-Answer-Clarification risk.** This Layer-1 increment must never be
  bundled with, or expanded into, Answer Clarification / Improve Wording, or any
  Layer 2–4 (scoring/evidence/gap-closure) direction, per the PR #111 four-layer
  separation. Mitigation: §5 non-goals; independent review before merge.

---

## 11. Roadmap handling (proposed only)

A roadmap entry recording this Increment Contract is **proposed only** and is NOT
made by this document. Per repository governance, roadmap synchronization is a
separate, owner-gated documentation step performed after (and if) this contract
is merged. This document changes no roadmap file.

---

## 12. Authorization classification and required sequence

This contract may authorize a future implementation PR **only** if the contract
itself first passes **independent review** and an **owner-gated true merge**. The
contract document itself implements nothing. No implementation begins until after
this contract is independently reviewed and owner-merged, and then only under a
separate owner implementation authorization.

Any subsequent work must proceed, in order, through: this Increment Contract
(proposal only) → independent review → owner-gated true merge of the contract →
a separate owner implementation authorization → implementation → tests →
independent review → owner-gated true merge → separate manual demo verification →
separate roadmap synchronization. The app remains electronics/electrical-only for
the MVP, and the current official state remains `DEMO_READY_WITH_LIMITATIONS`,
until separate governed decisions state otherwise.

---

## 13. Final classification

`INCREMENT CONTRACT PROPOSAL ONLY — LAYER-1 FEEDBACK WORDING / GAP-TYPE-AWARE
GUIDANCE — NO IMPLEMENTATION STARTED — NO SCORING CHANGE AUTHORIZED`
