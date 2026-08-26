# W2-B / RVR-6a Implementation Evidence Pack

**Authority for this file:** Contract Amendment 1 §8.3 (authoritative via
PR #575) — the exactly-one committed evidence-pack file, created and
populated by the implementation candidate inside its exact candidate tree.
This pack records everything truthfully knowable BEFORE the candidate is
frozen; per the anti-circular Candidate Identity Binding model it
deliberately does NOT embed its own final candidate SHA or tree SHA — those
are recorded EXTERNALLY after freeze (gate report, SHA-preserving bundle,
independent verification), and Owner exact-SHA acceptance binds this pack
automatically as a blob inside the accepted candidate's exact tree.

Classification legend: `[REPO]` verified in the tree at the base; `[EXEC]`
executed probe/test at the base; `[OWNER-PREMISE]` Owner-ratified premise;
`[DERIVED]` conclusion derived from repository evidence; `[PROPOSAL]`
subject to Owner exact-SHA acceptance.

## 1. Candidate Identity Binding

- **Exact authoritative implementation BASE / sole parent:**
  `346f8e8a3b1532a6c52750fe20bc76668db06956` (Merge PR #575; parents
  `ad70723e8fdb34493ac9e53d7a9a3ceb80850708` +
  `6bb8f9e34c289953f2003de49c68210f9d2706ac`) `[REPO]` — verified live at
  implementation start; carries the authoritative Contract Amendment 1
  byte-identical to accepted candidate `6bb8f9e3…`.
- **Authority chain:** Wave-2 contract (PR #563) → W2-B implementation
  contract (PR #573, `48017ec0…`) → Contract Amendment 1 (PR #575,
  accepted candidate `6bb8f9e34c…`) → the NEW Owner implementation-start
  authorization for the amended contract `[OWNER-PREMISE]` → this
  candidate.
- **Rejected-evidence lineage (inspected as lessons only, not parents):**
  `7e0174ac…` (Creator-Grill failed) and `91c5de53…` (Independent-Review
  rejected), both preserved via SHA-preserving bundles; neither is a parent
  or wholesale-cherry-picked source of this candidate.
- Final candidate SHA / tree: **recorded externally after freeze** (binding
  chain: base → frozen tree containing this pack → exact SHA recorded after
  freeze → bundle/independent verification → Owner exact-SHA acceptance).

## 2. Exact changed-path inventory

| Path | Status | Purpose |
|---|---|---|
| `engine/adaptive_register.py` | NEW | derived two-level register, W/M-parameterized fold |
| `engine/progression_loop.py` | M (purely additive section 7; 0 deletions) | the Option-C serving policy (`compute_serving_decision`) |
| `web/app.py` | M | render-only policy consumption in `show_session` |
| `web/templates/session.html` | M | served-question override arrives via the question slot; cues, risk note, primary-action block, decision-section anchor id |
| `web/ui_text.py` | M | six governed `UI_W2B_*` EN/AR pairs |
| `docs/governance/W2_B_RVR6A_IMPLEMENTATION_EVIDENCE_PACK.md` | NEW | this pack (Amendment §8.3) |
| `tests/test_w2b_amc_register_calibration.py` | NEW | register + W/M falsification battery |
| `tests/test_w2b_amc_serving_policy.py` | NEW | triggers, real consequences, precedence, fail-closed |
| `tests/test_w2b_amc_decision_transition.py` | NEW | trigger-3 transition + FDC-001 fence |
| `tests/test_w2b_amc_web_serving.py` | NEW | real-journey serving behavior, EN/AR, truthfulness |
| `tests/test_w2b_amc_matrix_parity_mg8.py` | NEW | transition matrix, reconstruction parity, MG-8 |
| `tests/test_w2b_amc_consumers.py` | NEW | consumer adjudication, replay containment, digest revalidation |
| `tests/test_p9_mech_i{3,4,5}_*.py` | M | mechanical digest re-freeze only (`756e524a…` → `3b531cc8…`), disclosed lineage comment (base contract §G allowance) |

Forbidden surfaces untouched (idea_state, record_contract,
decision_workspace, decision_composition, derived_readiness,
deliverable_assembler, requirement_landscape, session_reconstruction,
export/read services, domain packs, `scripts/run_cli.py`) `[EXEC — diff]`.

## 3. Six-capability traceability

| Capability (contract §B as amended) | Implementation | Evidence |
|---|---|---|
| 1 Domain-aware routing through existing seams | the policy routes through `get_question`/`get_path_n_question` with the canonical domain; artifact domains (electronics, mechanical — both fully artifact-covered `[EXEC]`) defer to RVR-2; the generic surface is the adaptation class | serving-policy artifact-deferral tests; web no-false-fire test |
| 2 Prior-answer-aware suppression | `completed_intent_skip`: clamp + ACTIVE W2-D attempt + ELEVATED register → governed exit vocabulary served instead of the verbatim repeat | engine + real stage-3 web journey (baseline asserted first) |
| 3 State-aware next-question/action prioritization WITHIN the canonical gap (Amendment §4) | `compute_serving_decision`: question-slot overrides (governed texts actually served) + the decision-evidence action slot; `select_next_gap` untouched as sole gap owner | the whole serving-policy suite; behavioral floor tests (same gap + different history → different served text) |
| 4 Unknown-aware rerouting | accepted risks not re-asked (canonical) + governed transparency note + reopening only via correction lapse + reopened-lapse cue | real accept-risk + real correction-lapse journeys |
| 5 Register core | `engine/adaptive_register.py` (derived, two-level, hysteretic, reversible, never persisted, quality-field never consumed) | calibration suite + purity/parity tests |
| 6 Purity/determinism | pure functions of ledger + canonical state; no persisted adaptive state, no fired-flags, no timestamps/randomness; idle re-render idempotent | determinism/shuffle/idempotence tests; grill sweep of the diff |

## 4. Four-trigger table (exactly four; no fifth) `[PROPOSAL per Amendment §5]`

| Trigger | Authoritative input | Type | Reachable today | Serving consequence | Fail-closed |
|---|---|---|---|---|---|
| `critical_unresolved_gap` | level-1 transition blocker (structural mirror of `evaluate_transition`, truth-linked by test) ∧ stalled (`iterations_open >= STALL_THRESHOLD`) ∧ generic-verbatim surface | state predicate | **state class constructible; ROUTE-LIMITED today** — activated domains (electronics, mechanical) are fully artifact-covered, so stage-2 exhaustion is RVR-2's governed surface and stage 3 has no level-1 blocker `[EXEC]`; becomes route-live the moment an artifact-less domain activates. Declared per the Amendment §5 honesty rule — NOT fabricated | serves `_STALL_REFRAME` (first stalled serve) / `_EXHAUSTED_EXIT_PROMPT` (afterwards) instead of the verbatim repeat | artifact surface or below threshold ⇒ existing behavior |
| `lapsed_acceptance` | active `risk_accepted` record ∧ gap absent/OPEN/PARTIAL again ∧ NOT re-engaged since the acceptance (ledger-derived) | state+ledger predicate | lapse + transparency cue fully route-reachable (real `/correct` journey, tested); the stale-index QUESTION OVERRIDE class is constructible but current replay dynamics land reachable lapses at a fresh index where the canonical serving ALREADY re-asks the area's primary question (the correct re-resolution) — declared, not fabricated | serves the area's PRIMARY governed question instead of a stale clamped variant; expires on re-engagement (never loops) | acceptance holds / record superseded / no serving delta ⇒ no fire |
| `multiple_decision_alternatives_declared` | the ledger's LATEST record is a declared alternative whose addition crossed its context < 2 → >= 2 active alternatives (TRUE TRANSITION; refine never fires; withdrawal never fires; re-crossing fires again; any subsequent record ends it; no persisted flag; idempotent re-render) | ledger transition | fully route-reachable (live W2-A declare routes, tested end-to-end) | the DECISION-EVIDENCE action block is prioritized as the primary governed next action (actionable anchor to the existing decision section); the question slot untouched; NO comparability claim | not the latest event / count not crossing ⇒ no fire |
| `completed_intent_skip` | generic clamp ∧ ACTIVE substantive attempt (W2-D gate; superseded never counts) ∧ ELEVATED register | state+ledger predicate | fully route-reachable (stage-3 clamp, real journey) | governed exit vocabulary served instead of the verbatim repeat; truthfully reverses when the register lowers | register NEUTRAL / no clamp / no active attempt ⇒ existing behavior |

## 5. Real serving consequences (baseline vs triggered; cues never counted)

- **Skip (route-proven):** baseline = `QUESTIONS[PMF][-1]` verbatim repeat;
  triggered = `_EXHAUSTED_EXIT_PROMPT`; same canonical gap; different
  truthful text; reverses after two contrary weak answers (M=2).
- **Critical (engine-proven, route-limited declared):** baseline =
  `QUESTIONS[PF][-1]` verbatim repeat at k=3; triggered = `_STALL_REFRAME`
  (k=3) / exit prompt (k>3); same canonical gap.
- **Lapse (transparency route-proven; override engine-proven):** stale
  baseline = clamped variant; triggered = the area's primary question; the
  reachable lapse journey lands where canonical serving already re-asks the
  primary question — asserted with NO false override and NO false cue.
- **Alternatives (route-proven):** baseline = no action block; triggered =
  the decision-evidence action block with an actionable anchor; expires
  after the next governed interaction; W2-A readiness note co-renders with
  zero contradiction.

## 6. Precedence evidence `[PROPOSAL]`

`W2B_QUESTION_SLOT_PRECEDENCE = (lapsed_acceptance, completed_intent_skip,
critical_unresolved_gap)`; the action slot belongs to the alternatives
transition alone (the slots never compete). REAL competition proven: at
k = STALL_THRESHOLD with active attempt + elevated register, critical wants
`_STALL_REFRAME` while skip wants `_EXHAUSTED_EXIT_PROMPT` — the winner
determines the actually-served text (tested both with and without the
competing condition); the triple-competition state (lapsed + skip +
critical) serves the primary question. Deterministic across recomputation,
ledger shuffle, and deep-copy reload; starvation impossible (all governed
exits remain live — proven by accepting the risk mid-suppression); no
fifth trigger.

## 7. Register model and level count `[PROPOSAL]`

Two levels (NEUTRAL/ELEVATED) — the bounded minimum; the only
register-gated behavior (the skip) is a binary gate, so a third level would
be unconsumed scope; no repository authority enumerates levels `[REPO]`.
Derived-only, never persisted; contributions cited per record; stored
`quality` never consumed (mutation-probe tested).

## 8. W/M proposal table `[PROPOSAL — NOT Owner-accepted, NOT frozen]`

| FIELD | DEFINITION | CONSTRAINT CHECK | EVIDENCE | PROPOSED VALUE | CONSEQUENCE |
|---|---|---|---|---|---|
| W | consecutive STRONG signals raising NEUTRAL→ELEVATED | bounded ✓ deterministic ✓ no single-point posture (OD-R5) ✓ | W=1 elevates on one data point (forbidden flap, tested); W=3 starves EVERY realistic mixed shape (SSW/SSWS/SSNS/(SSW)×4 never elevate, §9) while honest on SSS | **2** `FACT-grounded` | lower: constraint-forbidden flap; higher: calibration effectively unreachable on real mixed journeys |
| M | contrary WEAK signals lowering ELEVATED→NEUTRAL | bounded ✓ reversible-effective ✓ hysteretic ✓ | M=1: 8 flips / 12 answers on (SSW)×4 + noise-flapping (prior proposal OVERTURNED); M=2: 1 flip, still lowers on SSWW at latency 2; M=3 holds through TWO contrary weaks (degraded truthful lowering, rejected) | **2** `FACT-grounded` | lower: churn + suppression toggling; higher: contrary evidence ignored too long |

Reversibility has a second, M-independent channel: supersession/correction
recomputation lowers instantly (tested both directions). The calibration
tests exercise W∈{1,2,3}, M∈{1,2,3} on the real fold — no constant-assert
is cited as calibration (Amendment §8.2).

## 9. W/M calibration traces `[EXEC — regenerated at this base]`

Per-answer level trace (N=NEUTRAL, E=ELEVATED), f = level flips, e =
elevation latency:

| SEQ | W2M1 | W2M2 | W2M3 | W3M1 | W3M2 |
|---|---|---|---|---|---|
| S | `N` f=0 e=- | `N` f=0 e=- | `N` f=0 e=- | `N` f=0 e=- | `N` f=0 e=- |
| SS | `NE` f=1 e=2 | `NE` f=1 e=2 | `NE` f=1 e=2 | `NN` f=0 e=- | `NN` f=0 e=- |
| SSS | `NEE` f=1 e=2 | `NEE` f=1 e=2 | `NEE` f=1 e=2 | `NNE` f=1 e=3 | `NNE` f=1 e=3 |
| SWSWSW | `NNNNNN` f=0 | `NNNNNN` f=0 | `NNNNNN` f=0 | `NNNNNN` f=0 | `NNNNNN` f=0 |
| SSW | `NEN` f=2 | `NEE` f=1 | `NEE` f=1 | `NNN` f=0 | `NNN` f=0 |
| SSWS | `NENN` f=2 | `NEEE` f=1 | `NEEE` f=1 | `NNNN` f=0 | `NNNN` f=0 |
| SSWW | `NENN` f=2 | `NEEN` f=2 | `NEEE` f=1 (holds!) | `NNNN` f=0 | `NNNN` f=0 |
| (SSW)×4 | f=**8** | f=**1** | f=1 | never elevates | never elevates |
| SNSNS | all-N | all-N | all-N | all-N | all-N |
| SSNS | `NEEE` f=1 | `NEEE` f=1 | `NEEE` f=1 | `NNNN` f=0 | `NNNN` f=0 |
| NWNNWN (novice) | all-N | all-N | all-N | all-N | all-N |
| SSSSWSSS (technical) | f=3 | f=1 | f=1 | f=3 e=3 | f=1 e=3 |
| SSWWWW (degrading) | lowers at W#1 | lowers at W#2 | lowers at W#3 | — | — |

Supersession probes: withdraw contributing STRONG → instant NEUTRAL;
withdraw the WEAK → ELEVATED restored (both at M∈{1,2}). Shuffle/replay
equivalence holds. Suppression stability: at M=1 the skip toggles with
every noise answer; at M=2 it is stable and reverses on a genuine contrary
run — the user consequence favoring M=2.

## 10. MG-8 diagnosis (measurement only; semantics unchanged) `[EXEC]`

Phenomenon pair through the REAL `/start` route: the seed idea text is
durably recorded (`reconstruction_inputs.seed_idea_text`, verbatim) while
`known_problem` AND `idea_summary` stay unpopulated for a below-REASONED
seed, and the seed is never a ledger record; a REASONED-assessable control
seed is captured and summarized (capture-gated, not storage-gated). Cause
isolation: the seed traverses the LEVEL-0 establishment branch whose guard
is `quality >= REASONED` ALONE (no relevance conjunct); the in-gap sibling
guard additionally requires relevance (both measured through real
`run_iteration` paths). Proximate cause: representative problem-prose
seeds assess ASSERTED (5/5 committed corpus vectors `[EXEC]`) — problem
statements rarely carry causal/structural/substance form, so the pair is
the rule, not an edge case. Cold reconstruction reproduces the pair
deterministically. No MG-8 locus was modified (the progression_loop diff
is purely additive; the level-0 branch is byte-unchanged).

## 11. Serving-decision state-transition matrix `[EXEC — tested]`

10 rows through one engine journey plus the disposition transition
(tests/test_w2b_amc_matrix_parity_mg8.py): fresh → strong#1/2 (register
raises at 2) → attempts (clamp at k=3 → skip override while ELEVATED) →
weak#1 (M=2 hysteresis holds, skip persists) → weak#2 (register lowers;
the stalled-blocker critical serving truthfully remains — never back to
verbatim repeats) → alternatives-cross (action slot fires; question slot
independent) → post-decision answer (transition expires) → accept-risk
(reroute, no override on the fresh gap). Persistence column: derived-only
(no new state key on IdeaState; deep-copy reload derives identically).
Covered: no-trigger, each trigger, simultaneous triggers, <2→>=2 crossing,
idle re-render, repeated render, correction lapse, register raise/lower,
suppression eligible/lapsing, reconstruction, legacy path.

## 12. Behavioral composition flows (all real seams)

A. substantive answer → prior-intent detection → skip override → correction
(real `/correct`) → truthful re-eligibility (attempt-gate lapse). B. accept
risk → no repeat + governed note → correction lapse → reopened area with
truthful cue and canonical primary re-ask. C. register raise → skip →
contrary evidence ×2 → register lowers → verbatim question truthfully
returns. D. alternatives <2→>=2 → decision-evidence action prioritized →
no comparability claim → FDC-001 readiness byte-unchanged → idle re-render
idempotent → next interaction expires it. E. cold reconstruction → identical
(register, ServingDecision). F. trigger-free journey → zero W2-B markup,
canonical question byte-identical. REQUIREMENT COVERAGE and BEHAVIORAL
COMPOSITION COVERAGE reported separately; both PASS.

## 13. Consumer propagation `[EXEC — fresh sweep at this base]`

Method: `grep -rn "select_next_gap" --include="*.py"` over the whole
worktree, `__pycache__` excluded; classified into direct calls / imports /
comments / tests; plus the module-import indirect consumer. Inventory:
SEVEN runtime call sites — `engine/progression_loop.py:1045` (completion,
CONTAINED), `:1143` (serving/integration, CONTAINED), `web/app.py`
render (UPDATED — consumes the policy), accept-risk gate (CONTAINED —
consent compares against the canonical served gap, which the policy never
overrides), evidence-record labeling (CONTAINED), answered targeting
(CONTAINED), `scripts/run_cli.py:152` (OUT-OF-SCOPE BY CONTRACT —
Amendment §12: W2-B behavior is scoped to the governed web session
journey; the CLI is byte-unchanged and non-adaptive — stated, not
implied); indirect: `engine/session_reconstruction.py:55` module import
(CONTAINED — replay proven never to consult the policy or register, by
monkeypatch and source scan); 16 pre-existing test files re-adjudicated
unaffected; 3 P9 digest-pin files mechanically re-frozen under the §G
allowance. No consumer MISSED.

## 14. Reconstruction / reload `[EXEC — tested]`

Real durable journey (answers + decision records, sqlite store) → cold
`reconstruct_readonly_state` → identical `(RegisterState, ServingDecision)`
including the active alternatives transition. No persisted adaptive state
anywhere; replay is ledger-less and byte-unchanged (`session_reconstruction`
untouched; canonical paths monkeypatch-proven policy-free).

## 15. Cross-Layer classification

**C2 + C4** re-verified against the implementation (engine policy → serving
consumer → user-visible composition): no durable write, no idempotency or
supersession change, no canonical transition change, NO new mutating route
`[EXEC — zero new `@app.route` in the diff]` ⇒ NOT C3; §6.3 retry matrix
not applicable; escalation rule honored (nothing needed it). Applied union:
traceability chain (§3 of this pack), coverage separation (§12),
composition matrix (§11/§12), consumer sweep (§13), adversarial grill,
UI↔engine parity (§16).

## 16. UI ↔ engine parity and truthfulness

The rendered cue set is derived from the SAME `ServingDecision` that
replaced the question: only the question-slot WINNER's cue renders (a cue
never appears without its actual serving change), plus the capability-4
lapse-transparency duty and the accepted-risk note. String bans tested: no
"served first", no "comparable"/"ready to compare"/positive
"comparison started", no "resolved"/"completed" claims; the decision action
text explicitly discloses "No comparison has started yet." EN/AR pairs for
all six strings; single-language rendering verified in Arabic mode; the
canonical question text remains English per the D-P6-18 boundary.

## 17. Deterministic replay / language / determinism

No timestamps, no randomness, no environment reads in any W2-B computation
`[EXEC — diff grep: matches are docstrings and seeded test shuffles only]`;
same ledger → same decision across recomputation, deep copy, and shuffle;
idle re-render idempotent (tested).

## 18. Test evidence (ACTUAL counts at this base)

- RED baseline: 4 of 6 focused modules fail at collection against the base
  (seams absent); the 2 collectable modules fail 10 behavioral tests —
  genuine RED→GREEN.
- Focused amended-contract suite: **67 passed / 0 failed** (6 modules).
- Affected regressions: **467 passed / 0 failed** (P9 pins ×3, W2-D ×2,
  RVR-1, RVR-2 flow, RVR-5, R4-C, DP6-18 ×2, cascade, 1B routing,
  W2-A ×5, FDC-001 ×4).
- UG1 universal smoke: **PASS** (77 canonical tests).
- Full repository suite: **4662 passed / 3 skipped / 1 xfailed / 0
  failed**; prior authoritative baseline (code-identical base) 4595 / 3 /
  1 / 0; **delta = +67 = exactly the six new W2-B modules**; no new skip,
  xfail, error, or deselection.

## 19. Material Gap Sweep and classifications

- Route-limited reachability of the critical trigger and of the
  lapse-override class: DECLARED (Amendment §5 honesty rule) — engine
  behavior implemented and proven; goes live with future domain activation
  / state classes; NOT fabricated. Classification: DISCLOSED LIMITATION,
  non-blocking by contract.
- CLI non-adaptive: OUT-OF-SCOPE BY CONTRACT (Amendment §12), stated.
- W/M values, precedence, register level count, trigger definitions:
  `[PROPOSAL]` — ratified only at Owner exact-SHA acceptance.
- Owner premises: the Option-C architecture decision, the trigger
  replacement, W=2/M=2 as the permitted current proposal, the new
  implementation-start authorization. Facts vs derived conclusions
  classified inline throughout this pack.
- No blocker found; no governance status surface modified by this
  candidate; `W2-B IMPLEMENTATION AUTHORITATIVE: NO` and
  `RVR-6A CLOSED: NO` until the full lifecycle completes.
