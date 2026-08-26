# W2-C / RVR-6b — Authorization & Implementation Contract Candidate

**Status:** CANDIDATE — awaiting Independent External Contract Review and Owner
exact-SHA acceptance. NOT AUTHORITATIVE until Owner-accepted at its exact frozen
SHA, merged through the established lifecycle ("Create a merge commit"; second
parent = the exact accepted candidate; empty candidate→merge diff), and
post-merge identity-verified. **This contract authorizes NO implementation:**
`W2-C RUNTIME IMPLEMENTATION AUTHORIZED: NO` — implementation start requires a
SEPARATE explicit Owner instruction after this contract becomes authoritative
(the W2-A / W2-B precedent, preserved exactly).

**Authoritative base:** `1a9eb55656b52f635804647fe77412a7987a591e` — verified
live from Git at this gate as the tip of
`feature/atomic-json-session-persistence` (**PR #578** — the RVR-6a
formal-closure merge; first parent `eb23cbf2…` (PR #577); second parent
`31eb87f6…` — the exact Owner-accepted closure candidate; merge tree
`55c2d25b…` identical to the candidate tree; empty candidate→merge diff;
0 commits after). `RVR-6A FORMALLY CLOSED: YES` — the closure record's §9
condition is satisfied and post-merge identity-verified at this gate.

**Candidate identity (anti-circular):** this file records its BASE and its
authority sources; the candidate's own final commit SHA / tree are recorded
EXTERNALLY post-freeze (gate report + SHA-preserving bundle), never inside this
file. Owner exact-SHA acceptance binds this file as a blob of the accepted tree.

**Classification legend:** `[REPO]` verified in the tree at the base; `[EXEC]`
probe executed at the base; `[OWNER]` Owner decision/authority; `[PROPOSED]`
frozen by this contract if accepted; `[FUTURE]` later gate, not authorized here.

---

## A. Source map (reconstructed before authoring — no fact inherited from chat)

| Source `[REPO]` | Authority | What it contributes |
|---|---|---|
| `WAVE_2_BOUNDED_IMPLEMENTATION_CONTRACT_CANDIDATE.md` §§H, I, J, N, P, Q, S (authoritative, PR #563) | Wave-2 governing contract | W2-C slice definition; WS10 corrected scope; W1-N3 reconciled disposition; sequencing (W2-B → W2-C); Owner-decision package (§P.4 OD-W2-WS10-SCOPE); product-value model |
| `WAVE_1_REMEDIATION_FORMAL_CLOSURE_RECORD.md` §4 (PR #562) | W1-N3 origin | the corrected W1-N3 factual statement (M-1 experienced-technical residual relevance false-negative; honest restatement before MECHANISM closed; ≈18 interactions) |
| `OWNER_DECISION_REGISTER.md` OD-R5 row; Wave-1 boundaries; OD-W2-DW-LIFT row | Owner authority | RVR-6 Tier-1 STATE-ADAPTIVE scope incl. "partial promotion of OD-PDVG-04(a) WS10 content authoring into Tier-1"; the `RVR-4 ∥ RVR-6a → RVR-6b → RVR-7 → RVR-8` sequence; the precedent that a "before W2-X" Owner decision is EXERCISED via Owner exact-SHA acceptance of the contract that records it |
| `DEFERRED_OBLIGATIONS_REGISTER.md` §3 rows: RVR-6b/W2-C, W1-N3, OD-PDVG-12, MG-8, T2 bucket | obligation status owner | return triggers landing at THIS gate; closure evidence ("W2-C merged; 21-id registry committed and loader-validated") |
| `W2_B_RVR6A_IMPLEMENTATION_CONTRACT_CANDIDATE.md` + Amendment 1 + evidence pack (PRs #573/#575/#576) | adjacent authoritative slice | W2-B non-goals naming W2-C; Option-C serving architecture W2-C composes with; evidence-pack/identity-binding pattern |
| `WORKSTREAM_10_*` records (D1–D33) + `engine/question_intent_registry.py` | WS10 loader owner | ratified record shape (D1–D17) and loader interface/validation contract (D18–D33): ONE registry validated against ONE `source_artifact_path`, exact ID-set equality (D11), fail-loud, no fallback |
| `engine/path_n_questions.py` + `docs/governance/path_n_content_config/*.json` `[EXEC]` | committed question content | the 21 committed Path-N ids: electronics 11 (`N-MC-1…N-BA-3`, 4/4/3) + mechanical 10 (`mechanical:<GAP>:Qn`, 4/2/4) in TWO per-domain artifacts with distinct id schemes |
| `engine/gap_relevance.py` `[EXEC]` | relevance owner (RVR-2 family) | measured cross-family EN/AR differential-leak evidence recorded in-code; the reason broad markers are prohibited |
| `engine/semantic_registry.py` + `tests/test_pvcg_r3i_semantic_stability.py` | EN/AR equivalence owner | the semantic-stability discipline any new relevance marker must satisfy |
| `tests/fixtures/s2_run_001_answer_maps.json` | frozen S2 evidence | the S2 answer maps (E-1/M-1 × novice/expert × en/ar) — regression evidence for the W1-N3 attempt |
| `engine/question_aware_evaluation.py` + DOR §5 WS11 entry `[EXEC]` | WS11 owner | WS11 is implemented but DORMANT (zero non-test consumers `[EXEC]`), TIER 4 — BLOCKED BY DEPENDENCY (T2-E + T2-F + own authorization); activating it today would regress truthfulness (SATISFIED unreachable) |
| `WORKSTREAM_12_CONTROLLED_UNKNOWN_PROGRESSION_INCREMENT_CONTRACT.md` | WS12 owner | WS12 FORMALLY CLOSED; unknown/accepted-risk semantics live with RVR-1/`evaluate_transition` |
| `CROSS_LAYER_EXECUTION_ASSURANCE_STANDARD.md` (PR #571) | process standard | Continuous Traceability Rule + C0–C4 proportionality, mandatory for the future implementation candidate |

## B. W2-C definition (recovered, not inferred) `[REPO — Wave-2 §N/§I/§J]`

W2-C is the fourth and final Wave-2 executable slice:

> "W2-C (RVR-6b WS10 bounded content + intent-aware suppression/ completion/
> ordering + decision-aware routing consuming W2-A state + W1-N3 bounded
> attempt; explainability render ONLY if OD-PDVG-12 separately decided)"

**RVR-6b ↔ W2-C relationship:** RVR-6 (OD-R5, ACCEPTED IN PRINCIPLE) was split
by the Owner-frozen remediation sequence into RVR-6a (routing/register core —
implemented by W2-B, PR #576; formally closed, PR #578) and **RVR-6b — the
remaining obligation** (WS10 content + intent-aware completion). **W2-C is the
implementation slice OF RVR-6b** — the same obligation↔slice relationship as
RVR-6a↔W2-B. Neither is a verification layer over the other; RVR-6b closes only
through its own future formal-closure gate after W2-C implementation (§O).

**Why this gate exists:** the DOR RVR-6b/W2-C row's return trigger is "W2-C
authorization (incl. corrected WS10 scope decision)" and the W1-N3 row's return
trigger is "W2-C contract freeze" — both land exactly here. The Owner
authorized beginning the W2-C/RVR-6b authorization-and-contract-reconstruction
lifecycle only.

## C. Current implementation truth this contract builds on `[EXEC at the base]`

1. **WS10 today = validated loader, NO content.** `load_question_intent_registry`
   implements the full D18–D33 contract but has **zero runtime consumers** and
   **no committed registry artifact exists** (`git ls-files` — none). WS10
   content authoring was promoted in principle (OD-R5 / OD-PDVG-04(a)) and never
   performed.
2. **21 committed Path-N ids** exist in two per-domain artifacts (11 + 10) with
   two distinct id schemes; the loader validates ONE registry against ONE source
   artifact with exact ID-set equality (D11).
3. **W2-B Option-C serving is authoritative**: `compute_serving_decision` +
   four triggers + `W2B_QUESTION_SLOT_PRECEDENCE`; `select_next_gap` sole
   canonical gap owner; FDC-001 sole comparability/readiness owner; W=2/M=2
   Owner-accepted and FROZEN (untouched here).
4. **Relevance today** (`addresses_gap`) is lexical whole-word/phrase markers
   per gap type with in-code measured-leak rationale; W1-N3's false negative is
   the recorded residual.
5. **WS11 dormant; WS12 closed** (§A rows above).
6. Full suite: **4662 passed / 3 skipped / 1 xfailed / 0 failed** `[EXEC —
   executed at the PR #577 base `eb23cbf2…`]`. Three facts, stated separately
   and never conflated: **GIT TREE FACT** — PR #578 DID change the repository
   tree (`003035c8…` → `55c2d25b…`) through exactly the five
   closure-governance files (the closure record + CPS + roadmap + AIC + DOR).
   **CANDIDATE→MERGE IDENTITY FACT** — the exact Owner-accepted RVR-6a
   closure candidate tree equals the PR #578 merge tree; the candidate→merge
   diff is empty. **RUNTIME DELTA FACT** — the closure lifecycle changed zero
   runtime/test/domain/schema files, so the runtime behavior the suite
   measures is identical at `1a9eb556…` and at the tested `eb23cbf2…` tree;
   "tree unchanged" is NOT used to mean "runtime unchanged".

## D. OD-W2-WS10-SCOPE — the corrected WS10 scope exercise `[PROPOSED → exercised at Owner exact-SHA acceptance]`

Wave-2 §P.4 requires, "before W2-C freeze": exercise OD-PDVG-04(a) for the 21
committed ids AND decide the loader-contract covering mechanism (§I.1).

**Timing — explicit and non-circular.** The source wording "before W2-C
freeze" is satisfied under the repository's established lifecycle
interpretation (the OD-W2-DW-LIFT precedent — ODR: "EXERCISED (bounded) — via
Owner exact-SHA acceptance of the W2-A contract"): the decision is RECORDED in
the contract candidate and EXERCISED by the Owner's exact-SHA acceptance of
that candidate — which necessarily precedes any W2-C implementation freeze.
Nothing here pretends the decision already happened:

- **Freezing this candidate does NOT exercise OD-W2-WS10-SCOPE.** The
  candidate freeze is a Creator act; the exercise is an Owner act.
- **Owner exact-SHA acceptance of this contract IS the decision exercise.**
- Until that acceptance: **`OD-W2-WS10-SCOPE EXERCISED: NO`**.
- After that acceptance: the Owner has selected EXACTLY the per-domain option
  below — two per-domain registry instances covering the existing 21 committed
  ids through the unmodified D11/D19 loader, with OD-PDVG-04(a) bounded to
  exactly those 21 ids — and no other scope.
- Even after that acceptance, **W2-C runtime implementation remains
  UNAUTHORIZED** (separate Owner start decision, §O).
- The post-contract governance synchronization must record the exercised
  decision under the established DW-LIFT-style precedent (§O sync duties).
- No `OWNER_DECISION_REGISTER.md` edit occurs in this candidate.

**Covering mechanism — evidence-backed proposal: PER-DOMAIN REGISTRY
INSTANCES.** One WS10 registry artifact per committed Path-N artifact
(electronics 11-id registry against the electronics artifact; mechanical 10-id
registry against the mechanical artifact), each loaded through the SAME
unmodified loader, each satisfying exact ID-set equality (D11) against its own
`source_artifact_path`. Evidence: the two artifacts exist with disjoint id
schemes `[EXEC]`; the loader contract is written for exactly this one-to-one
validation; a combined-source reconciliation would require changing the ratified
D11/D19 loader contract — a WS10-owner change with no benefit this slice needs.
**No loader-contract change is authorized.** The combined-source option is
REJECTED at this gate, not deferred.

**OD-PDVG-04(a) exercise scope:** content authoring for exactly the 21
committed question ids — intent metadata per the ratified D1–D17 record shape.
No new question ids; no decision-capture identities inserted (Wave-2 §I.2 —
that boundary was settled by W2-ID/FDC-001); no placeholder ids; content is
committed governance data validated by the loader, not runtime-generated.

## E. W1-N3 — full adjudication (independent, not assumed from its return gate)

- **Authoritative definition** `[REPO — Wave-1 closure §4]`: residual relevance
  false-negative — in the S2 M-1 experienced-technical case a genuinely
  gap-addressing answer was not recognized, forcing one honest restatement
  before MECHANISM closed (≈18 interactions). Owner: RVR-2 / relevance family.
- **Current status / row** `[REPO — DOR §3]`: OPEN; return trigger "W2-C
  contract freeze" (THIS gate); latest safe gate W2-C; CONDITIONAL; closure
  evidence "W2-C RED test vs frozen S2 R6 fixture passing without new false
  positives, or evidenced deferral record".
- **Frozen strategy** `[REPO — Wave-2 §J, authoritative]`: question-id-scoped
  supplemental relevance; broad markers prohibited (measured leaks recorded in
  `gap_relevance.py` `[EXEC-verified]`); frozen S2 fixture
  (`tests/fixtures/s2_run_001_answer_maps.json` `[EXEC-verified present]`) as
  regression evidence only; no semantic model judgment; mandatory
  false-positive guard (the R3 semantic-stability corpus discipline —
  EN/AR differential-leak prevention `[EXEC-verified in-code]`); **evidenced
  fallback = SAFE FALSE-NEGATIVE**. Dependency correction verified live: the
  scoping uses the EXISTING 21 committed ids — they exist `[EXEC]`; no new or
  placeholder identity; no W2-ID dependency.
- **Duplicate-owner / force-fit check:** the supplemental layer scopes to
  question ids and consumes W2-C-authored WS10 intent content; `gap_relevance`
  remains the relevance owner (the supplement composes, never forks a second
  relevance model); no WS11 activation (no evaluation verdict); no Tier-2
  meaning inference. Not force-fitted: the residual is real (recorded
  measurement), the mechanism is new content + a bounded scoped layer — a
  genuine W2-C responsibility, not a rename.
- **DISPOSITION: A — CONSUMED INTO W2-C CONTRACT**, carrying Wave-2 §J's own
  fallback verbatim: `ATTEMPT BOUNDED CLOSURE IN W2-C; EVIDENCED FALLBACK =
  DEFER AS SAFE FALSE-NEGATIVE`. W1-N3 blocks neither this contract nor future
  implementation; a failed bounded attempt at implementation resolves to an
  evidenced deferral record, never a forced semantic change.
- **Deferral has durable ownership — it can never float.** If the future
  bounded attempt does not close the residual, the implementation evidence
  pack MUST record ALL of: the failed/insufficient closure evidence itself;
  why the canonical fallback (safe false-negative) remains truthful; the exact
  deferred obligation; its continuing canonical relevance owner
  (`gap_relevance` / the RVR-2 family, as applicable — no new duplicate
  relevance owner); **RVR-7 as the mandatory downstream return/input**
  (the authoritative OD-R4 lineage names W1-N2/W1-N3 as mandatory RVR-7
  inputs); persistence of the obligation in the Deferred Obligations Register;
  re-examination at every applicable release-class gate (the register's
  release-closure rule); and FCORA zero-orphan coverage. **`DEFERRED ≠
  SATISFIED` and `DEFERRED ≠ CLOSED BY SUCCESS`** — the implementation must
  never count a fallback deferral as successful W1-N3 closure, and no report
  or surface may present it as one.

## F. Contracted capabilities (CONTRACTED NOW — implemented only after separate Owner implementation-start authorization)

All capabilities are **Tier-1 STATE-ADAPTIVE**: pure functions of committed
content + canonical recorded state. No model inference, no persona, no memory
outside canonical state.

1. **WS10 registry content (21 ids).** Author and commit per-domain registry
   artifacts per §D; loader-validated at test time; loader unmodified.
2. **Per-question intent-coverage state ("WS10 completion state").** A derived,
   deterministic, never-persisted state per served question id: whether that
   question's committed intent is already covered by canonical recorded
   answers/dispositions. It is a SUPPRESSION/ORDERING INPUT ONLY — it is never
   an evaluation verdict, never WS11 `SATISFIED`, never gap-level completion
   (which stays owned by `evaluate_transition`/RVR-1), and never a user-facing
   progress claim.
3. **Intent-aware suppression.** A question whose intent coverage is complete is
   not re-served verbatim within the same canonical gap; the canonical journey
   continues with the next truthful question/action. Composes with (never
   duplicates) the W2-B suppression surfaces: accepted-risk non-re-asking and
   the four W2-B triggers remain W2-B-owned. Fail-closed: if the registry, the
   coverage computation, or any input is unavailable or ambiguous, serving
   falls back to the unmodified canonical behavior — suppression never blocks a
   gap's primary question when nothing else can be truthfully served.
4. **Intent-aware ordering within the canonical gap.** Extends the Option-C
   policy layer: among the current canonical gap's remaining questions, order
   by committed intent metadata + canonical state. `select_next_gap` remains
   the sole canonical GAP owner (byte-unchanged semantics); ordering never
   promotes across gaps.
5. **Decision-aware routing (read-only consumption of W2-A state).** Ordering/
   suppression may READ FDC-001 decision-capture state (as W2-B's alternatives
   trigger already reads the ledger) to avoid serving an intent a recorded
   decision already resolves. FDC-001 remains the sole decision/comparability/
   readiness owner; no decision semantics are written, inferred, or claimed.
6. **W1-N3 bounded attempt** per §E.

**Multi-condition precedence:** deterministic composition with
`W2B_QUESTION_SLOT_PRECEDENCE` is REQUIRED; the exact combined precedence is a
[PROPOSED-at-implementation] item frozen in the future evidence pack (the W2-B
precedent) — W2-B triggers' existing precedence is not reordered by W2-C. The
future combined-precedence proposal is **bound to the full relevant
Amendment-1 §6 evidence discipline**: it stays a proposal through the Creator
implementation Grill → Independent Review → Owner exact-SHA acceptance, and
the implementation evidence must prove at minimum — actual served-interaction
consequence; deterministic behavior for identical canonical state;
reload/reconstruction parity; starvation analysis; fail-closed behavior;
one-primary-CTA preservation; interaction with ALL existing W2-B trigger
precedence; interaction with W2-C suppression; interaction with W2-C
within-gap ordering; decision-aware routing coexistence; no duplicate
action/question stacking; no unilateral reordering of the existing W2-B
precedence; no cross-gap promotion. The implementation Executor may propose
the exact combined order; the Executor may NOT weaken these evidence
requirements.

## G. ALREADY IMPLEMENTED / REUSED (W2-C relies on, does not own)

WS10 loader (D18–D33); the 21 committed Path-N artifacts;
`select_next_gap`; W2-B register + four triggers + precedence (W=2/M=2 frozen);
FDC-001 `DecisionRecord`; `AssertionRecord` carrier (W2-ID/W2-A);
`gap_relevance` markers; `semantic_registry` EN/AR equivalence; RVR-1
accepted-risk semantics (WS12 closed); reconstruction/replay
(`session_reconstruction`); the Path-N serving route and `show_session`.

## H. DEFERRED (valid future work, NOT required for W2-C)

OD-PDVG-12 render (unless separately decided — §I); RVR-7 Arabic parity
(Wave 3; W1-N2 input); RVR-8; T2-B′ display surface; T2-E evidence-writer
mapping; T2-F ordering repair; WS11 activation (Tier 4 — blocked by
T2-E/T2-F + own authorization); Tier-2 meaning-adaptive questioning
(OD-PDVG-10, unowned, undecided); MG-8 adjudication (Owner);
FCORA (after RVR-8).

## I. EXCLUDED (W2-C must NOT implement)

- **OD-PDVG-12 "Why this matters" render: NOT AUTHORIZED by this contract.**
  Per Wave-2 §I.3 and the DOR row, the Owner MAY separately decide OD-PDVG-12
  at/before acceptance of this candidate, in which case the render becomes a
  bounded W2-C display item under the Phase-3 UX display owner; absent that
  separate decision, W2-C ships WITHOUT it and the render stays with T2-B′
  (before serious release). This contract does not decide it.
- WS11 activation or any `SATISFIED`/evaluation-verdict surface.
- Any change to `select_next_gap`, FDC-001 semantics, `evaluate_transition`
  gap-completion semantics, record schemas, dispositions, or the W2-B register/
  triggers/W/M.
- Any MG-8 semantic change (§K). Any intake-seam change.
- New question ids; runtime content generation; model/LLM inference; broad
  (non-question-id-scoped) relevance markers; EN-only markers that fail the
  semantic-stability discipline.
- Full adaptive questioning (§J); chatbot-style free dialogue; question
  cascades (one primary served question/action per stage is preserved).
- Persistence/export/schema expansion; domain activation; deployment surfaces.

## J. Adaptive-questioning fence — exact current state, preserved

`STATE-ADAPTIVE = Tier-1` (Wave-2; W2-B implemented; W2-C is the remaining
Tier-1 slice). `MEANING-ADAPTIVE = Tier-2` — **OD-PDVG-10 undecided, unowned,
untouched**. W2-C is one bounded Tier-1 layer; after full W2-C implementation
**`FULL ADAPTIVE QUESTIONING ACTIVATED: NO` remains true** — any broader
activation requires the OD-PDVG-10 decision under a future owner/gate. This
contract must never be cited as adaptive-questioning activation authority.

## K. MG-8 boundary — no overlap, kept separate

MG-8 (diagnosis DELIVERED; Owner adjudication OPEN; semantics UNCHANGED; latest
safe gate "before serious release") lives at the intake seam (level-0
quality-only guard; envelope-only seed). W2-C's surfaces are served-question
suppression/ordering/content — **not the intake seam**. Adjudicated: NO
authorization conflict; W2-C does not touch, repair, or depend on MG-8-owned
behavior. Per Wave-2 §S-13 the future W2-C evidence pack MAY add measurement;
any semantics change remains separately Owner-authorized.

## L. No new tuning parameter; W/M untouched

W=2/M=2 are W2-B-owned, Owner-accepted, FROZEN — this contract neither reopens,
reuses, nor extends them. W2-C's semantics are content-deterministic (boolean
intent coverage from committed content + canonical state) and need **no
hysteresis and no numeric tuning parameter**. If implementation discovers a
genuine parameter need, that is a STOP-and-return contract question — not an
implementation choice and not a W/M reuse.

## M. Cross-Layer Execution Assurance Standard application

The future implementation candidate is a Standard-governed change (expected
class C2 + C4: multi-surface runtime + digest-pinned file). Requirements
carried: Continuous Traceability Rule; consumer sweep re-run at implementation
(every runtime consumer of serving/relevance surfaces classified; the governed
CLI's scope stated truthfully rather than assumed); **bounded digest-pin
allowance** — re-pinning permitted ONLY for the exact pinned files the
implementation legitimately changes, with before/after digests recorded in the
evidence pack (the W2-B precedent); genuine RED→GREEN discipline; no
constant-assert calibration.

## N. Determinism / reconstruction / EN-AR / UX contract

- **Determinism:** same committed content + same canonical state → same served
  question/action, coverage state, and ordering. No wall-clock, randomness, or
  session-local memory.
- **Reconstruction:** registry artifacts are committed content; coverage is
  recomputed from canonical state on reload — nothing persisted, replay parity
  preserved (the W2-B ledger-less-replay lesson applies; any replay-visible
  divergence is a defect).
- **EN/AR:** by default W2-C adds NO user-facing strings (intent metadata is
  evaluator/routing-facing). Any W1-N3 marker additions must satisfy the
  semantic-stability EN/AR differential-leak discipline. If OD-PDVG-12 is
  separately decided, its render ships EN/AR-paired through the established
  `ui_text` mechanism. UI-language/input-language separation unchanged.
- **UX truthfulness:** one primary CTA per stage; no misleading progress; no
  false comparison-readiness ("No comparison has started yet" style truth
  preserved); suppression is silent journey improvement, never a completion
  badge; nothing implies the system "understood" free-text meaning (Tier-2).

## O. Lifecycle states (preserved exactly; nothing self-authorizes)

```
THIS GATE:        contract candidate → freeze SHA → Contract Grill →
                  Independent External Contract Review → Owner exact-SHA
                  acceptance (constitutes the §D OD-W2-WS10-SCOPE exercise) →
                  Owner-lifecycle publication/PR/merge → post-merge verification
                  [→ post-contract governance sync, per PR #574 precedent]
THEN (separate):  Owner W2-C IMPLEMENTATION-START authorization   [FUTURE]
THEN:             implementation candidate lifecycle (RED-first; Grill;
                  Independent Review; Owner exact-SHA acceptance; merge;
                  post-merge verification; committed evidence pack)   [FUTURE]
THEN:             post-implementation governance sync                 [FUTURE]
THEN:             RVR-6b FORMAL-CLOSURE eligibility → its own closure
                  lifecycle (the RVR-6a closure precedent: dedicated
                  conditional closure record; Owner adjudication)     [FUTURE]
```

`CONTRACT AUTHORITATIVE` ≠ `IMPLEMENTATION AUTHORIZED` ≠ `IMPLEMENTED` ≠
`RVR-6B CLOSED`. Documenting a step never authorizes it.

**Post-contract synchronization duties (binding on that future sync gate; NO
status/governance surface other than this contract artifact changes in THIS
candidate — the one-file contract-gate precedent stands).** If this candidate
is Owner-accepted and merged, the post-contract governance synchronization
must record: (a) **OD-W2-WS10-SCOPE as EXERCISED through the Owner's
exact-SHA contract acceptance** (the DW-LIFT-style precedent), if and only if
that acceptance occurred; (b) the selected option — **two per-domain registry
instances covering the existing 21 committed ids through the unmodified
loader**; (c) a normalization of the Deferred Obligations Register's existing
closure-evidence wording "21-id registry" so future readers do not mistake
the singular phrase as requiring one combined registry — preserving the
semantic truth that registry CONTENT covers all 21 ids while the physical
governance/runtime representation is two per-domain registries; (d) the
W1-N3 contract disposition (§E); and (e) that W2-C implementation remains
NOT AUTHORIZED until a separate Owner start authorization.

## P. Future implementation evidence-pack contract (non-circular)

Exactly one committed pack file
(`docs/governance/W2_C_RVR6B_IMPLEMENTATION_EVIDENCE_PACK.md`) with the
Amendment-1 Candidate Identity Binding model (base/parent/authority/changed
paths/evidence INSIDE; final SHA/parent/tree EXTERNAL post-freeze). It must
prove: contract identity consumed; per-capability behavior with **route-live
vs route-dormant declared honestly** (the Amendment-1 §5 honesty rule);
real served-route evidence; composition evidence with W2-A state and the W2-B
triggers incl. the frozen combined precedence; suppression non-stacking;
fail-closed proofs; ownership boundaries (select_next_gap / FDC-001 /
evaluate_transition byte-level or fence-test evidence); reconstruction/replay
parity; W1-N3 attempt outcome (bounded closure evidence OR the evidenced
deferral record with the full §E durable-ownership content); the mandatory
lapsed-acceptance stale-index revalidation (§S — outcome A or B with its
evidence/proof); **explicit EN/AR evidence** — direct evidence of EN behavior;
direct evidence of AR behavior; semantic equivalence where applicable;
UI-language/input-language separation; proof of no bilingual divergence in
intent coverage, suppression, or ordering; and no simultaneous EN+AR display
of the same label where the existing product language policy prohibits it (no
new language semantics — evidence hardening only);
registry/loader validation evidence; digest before/after;
full-suite counts with the affected-family DEFINITION stated and **no false
reconciliation of family counts** (the 467/484 lesson: the full suite is the
authoritative reproduction); observations; deferred work. No claim rests on
Creator assertion where a probe or test can carry it.

## Q. Acceptance criteria (future implementation gate — evidence-derived, no pre-frozen test counts)

FUNCTIONAL: real served interactions change where state warrants (a covered
intent is not re-served; ordering reflects intent + state; the M-1-class
W1-N3 case recognizes the addressing answer or the deferral record exists).
TRUTHFULNESS: impossible claims stay impossible (no SATISFIED, no comparison
readiness outside FDC-001, no progress inflation, no Tier-2 claim).
OWNERSHIP: fence tests prove select_next_gap / FDC-001 / evaluate_transition /
W2-B surfaces unchanged in semantics. DETERMINISM & RECONSTRUCTION: §N proven
by tests incl. cold reconstruction. COMPOSITION/PRECEDENCE/SUPPRESSION: §F
proven, incl. no-stacking and idempotent re-render. BILINGUAL: §N proven.
REGRESSION: full suite green including the 67 W2-B tests, WS10 loader suites,
relevance/semantic-stability suites, UG1 smoke; RED inventory categories
(registry/content, coverage, suppression, ordering, decision-read, W1-N3,
fences, composition, web, reconstruction) frozen at implementation-contract
detail level — exact tests and counts at implementation, per C70 discipline.
EVIDENCE: §P pack complete.

## R. Before-W2-C obligation sweep (register read in full at this base)

| Row | Status at this base | This gate's disposition | Blocks contract / future impl |
|---|---|---|---|
| RVR-6b / W2-C (§3) | OPEN — NOT AUTHORIZED YET; trigger "W2-C authorization (incl. corrected WS10 scope decision)" | THIS contract + §D exercise; row remains OPEN until W2-C merges ("21-id registry committed and loader-validated") | NO / NO |
| W1-N3 (§3) | OPEN; trigger "W2-C contract freeze" | adjudicated §E: CONSUMED INTO W2-C CONTRACT with evidenced fallback | NO / NO |
| OD-PDVG-12 (§3) | OPEN; optional inclusion at W2-C freeze | offered per §I; undecided ⇒ EXCLUDED; fallback path (T2-B′) intact | NO / NO |
| MG-8 (§3) | OPEN — CONDITIONAL; Owner adjudication before serious release | no overlap (§K); pack may measure | NO / NO |
| RVR-6a row (§3) | CLOSED — evidence verified (PR #578 satisfied its conditional closure) | not reopened; carried observations checked §S | NO / NO |
| W1-N2 / RVR-7 (§3) | OPEN — Wave 3 | untouched; W2-C makes no Arabic-parity claim | NO / NO |
| RVR-8, T1-A′, T1-C′, T1-D, T2-G/OD-PDVG-10 (§3) | OPEN — later gates | untouched | NO / NO |
| W2-A residuals: `derived_readiness` `None`-context; withdrawn-note localization (§3) | OPEN — CONDITIONAL/NBF | W2-C adds no validation-status writes and (by default) no localized surfaces; if OD-PDVG-12 is included its render is `ui_text`-paired, unrelated to the withdrawn-note defect | NO / NO |
| Phase-9 debts; brand gate (§3) | OPEN — later triggers | untouched | NO / NO |
| §4 paid-activation rows; T2-A/T2-B′/T2-C′/T2-D | OPEN — later gates | T2-B′ CONTENT is partially covered by W2-C's WS10 authoring (per its own row wording) — cross-reference, not duplicate ownership: the display surface stays T2-B′ | NO / NO |
| §5 NBF rows (incl. WS11 Tier-4 block, CAP-12/13, future domains) | OPEN/NBF | untouched; WS11 stays dormant | NO / NO |
| §6 unowned (T2-D, T2-G, MG-8 owner) | OPEN | no force-fit; none touched | NO / NO |
| FCORA (§3) | OPEN — after RVR-8 | untouched | NO / NO |

**Contract blockers: 0. Future-implementation blockers beyond the required
Owner implementation-start decision and the §D exercise: 0.**

## S. RVR-6a carried observations — return check (neither pulled forward)

(a) **critical-trigger route-limited:** its return condition is future DOMAIN
ACTIVATION changing artifact coverage. W2-C authors content for the two
EXISTING activated domains' existing ids and activates no domain — the
reachability condition does NOT change ⇒ does NOT return now. (b)
**lapse-override stale-index class:** W2-C does not create the stale-index
lapse state class itself — it does NOT return as a contract item now — BUT
W2-C in-gap ordering plausibly CAN change which index a reopened/lapsed state
lands on, so this is not dismissible by assertion. **REVALIDATION REQUIRED:
YES** — the future implementation evidence pack MUST perform the
lapsed-acceptance stale-index / reopened-state revalidation on the composed
W2-C serving path and return exactly one of: **A. AFFECTED** — with the
evidence and resulting behavior recorded; or **B. NOT AFFECTED** — with
mechanical proof that the composed W2-C serving path cannot alter the
relevant landing/index behavior. The check may NOT be omitted on the ground
that the original state class was route-limited; the outcome may prove no
effect, but the check itself is mandatory. This neither reopens RVR-6a nor
blocks this contract. Neither observation is pulled forward; both remain
under their valid future rediscovery mechanism (DOR RVR-6a closed row +
evidence pack disclosures). (c) trigger-3 value
stays with T1-A′/RVR-8. (d) 467/484 looseness: preserved — the full suite is
the authoritative reproduction; W2-C's pack must not reconcile the numbers.

## T. Product / end-user value basis `[REPO — Wave-2 §Q; W1-N3 record]`

USER STATE today: questions are served from committed per-gap artifacts with
state-adaptive framing (W2-B), but the system cannot see QUESTION INTENT — a
user who already covered a question's substance while answering an adjacent
question is asked again verbatim; a genuinely addressing technical answer can
be missed (W1-N3: one forced restatement, ≈18 interactions to eligibility).
W2-C's delta: less repetition, fewer false negatives, intent-coherent ordering,
decision-aware skip — the Wave-2 §Q commitments "reduced repetitive
questioning", "prior-answer responsiveness", "technical-user respect".
MUST NOT claim: meaning understanding, completion, comparability, Arabic
parity, adoption/retention proof (T1-C′/RVR-8 own release value — 
`IMPLEMENTED ≠ RELEASE-VALUE CLOSED`). FAILURE/FALLBACK: registry or coverage
unavailable → canonical serving unchanged (fail-closed, §F.3); W1-N3 attempt
fails → evidenced safe-false-negative deferral. ONE-PRIMARY-CTA: preserved by
construction (§I). Simple Outside — Deep Inside: the depth is committed intent
content + deterministic state, never decorative annotation — the W2-B rejection
lesson (a cue is not adaptation) applies: **suppression/ordering must change
what is truthfully SERVED, not decorate it**.

## U. Self-invalidation record `[EXEC]`

Falsification attempts performed at this gate: (1) "W2-C is next" — verified
against Wave-2 §N sequencing + the closed RVR-6a lifecycle (PASS); (2) "W1-N3
returns now" — verified from its row's own trigger text (PASS); (3) "W2-B
already owns this" — refuted by W2-B contract NON-GOALS naming W2-C/WS10/W1-N3
`[REPO]`; (4) "WS10/WS11/WS12 already own it" — WS10 owns the LOADER (content
absent `[EXEC]`); WS11 dormant/Tier-4-blocked (zero consumers `[EXEC]`); WS12
closed (unknown semantics live with RVR-1) — none owns intent-aware serving;
(5) "a combined 21-id registry is already contract-valid" — refuted: D11/D19
one-source validation `[REPO]`, two artifacts `[EXEC]` ⇒ §D decision required,
exactly as Wave-2 §I.1 predicted; (6) "OD-W2-WS10-SCOPE was already exercised"
— refuted: absent from the ODR `[EXEC grep]`; (7) "MG-8 conflicts" — refuted
(§K, disjoint seams); (8) "W/M must extend to W2-C" — refuted (§L, no
hysteresis semantics); (9) "the carried observations return" — refuted (§S,
reachability conditions unchanged); (10) "W2-C activates full adaptive
questioning" — refuted (§J; Tier-2 remains undecided/unowned). No contradiction
survived. If the Independent Review finds one, this candidate must be rejected
rather than repaired by reinterpretation.

## V. What this contract does NOT authorize (exhaustive boundary)

W2-C runtime implementation (separate Owner start decision required);
RVR-7; RVR-8; FCORA execution; CAP-12; CAP-13; IoT/Drones/Renewable activation;
WS11 activation; OD-PDVG-10/Tier-2; OD-PDVG-12 (unless separately decided by
the Owner); MG-8 change; W/M change; any deployment/production/Serious-Release/
Paid-Activation step. Eligibility statements in this file are never
authorization.
