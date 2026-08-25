# W2-B / RVR-6a — Authorization & Implementation Contract Candidate

**Status:** CANDIDATE — awaiting Independent External Review and Owner
exact-SHA acceptance. This document AUTHORIZES NOTHING by itself.
**`W2-B AUTHORIZED: NO`** until this contract completes its lifecycle
(review → Owner exact-SHA acceptance → merge → post-merge verification),
and even then W2-B IMPLEMENTATION start remains governed by §N's state
model. No runtime code, test, schema, route, or UI was modified by the
gate that created this file.

**Authoritative base:** `21ce0ff843682068c0bc29a73d4506de51e581fa`
(Merge PR #572; parents `216cdc8e…` + `dda867bb…`; tree `64b0b09d…`) —
verified from Git at creation; the Cross-Layer Execution Assurance
Standard and its governance sync are authoritative at this base.

**Lineage:** fresh same-base sibling replacing
`0448e36aec377942cba1f9baa955dfb2048be00c` — REJECTED by Independent
External Review (`REJECT — BOUNDED REPAIR REQUIRED`; blockers D-1
digest-pin allowlist incomplete, D-2 consumer inventory incomplete) and
preserved unamended as immutable rejected evidence. This sibling carries
the contract plus exactly the bounded repairs D-1/D-2 and the
non-blocking cleanups N-1 (§N attribution), N-2 (health wording), N-3
(multi-trigger determinism), N-4 (two explicit negative paths), each
independently re-verified from repository truth before adoption.

**Classification legend:** `[REPO]` verified in the tree at the base;
`[EXEC]` executed probe; `[OWNER]` Owner decision/authority;
`[PROPOSED]` a contract term proposed here for freeze;
`[HYPOTHESIS]` a claim W2-B's own RED evidence must confirm or falsify.

---

## A. Source map (reconstructed before authoring)

| Proposition | Authoritative source |
|---|---|
| W2-B = the Wave-2 executable slice implementing RVR-6a (bounded adaptive routing / register core) | `WAVE_2_BOUNDED_IMPLEMENTATION_CONTRACT_CANDIDATE.md` §H `[REPO :269-284]`; §N sequencing; register §3 row `[REPO :105]` |
| RVR-6 architecture: Tier-1 STATE-ADAPTIVE only; capabilities A–F; evidence-weighted reversible register calibration with deterministic hysteresis; W/M Owner-approvable | OD-R5, `OWNER_DECISION_REGISTER.md` `[REPO :1237]`; recorded from `WAVE_1_REMEDIATION_FORMAL_CLOSURE_RECORD.md` §7 |
| Register evidence basis: architecture A — deterministic recomputation from stored answer content via existing pure assessors; per-answer `quality` field is a STATE-LEVEL AGGREGATE and MUST NOT be used as an answer-local signal | Wave-2 contract §G `[REPO :238-268]` |
| W/M values: "proposed and frozen inside the W2-B candidate/evidence pack; accepted through Owner exact-SHA acceptance of W2-B. (The prior OD-W2-WM pre-gate is WITHDRAWN as circular.)" | Wave-2 contract §P `[REPO :443-445]`; §B row "W/M precondition circular" `[REPO :64]` |
| Tier-2 fence: MEANING-ADAPTIVE questioning = OD-PDVG-10, undecided, untouched | Wave-2 §H; register §3 T2-G row |
| WS10 completion state arrives only with W2-C; W1-N3 is a W2-C item | Wave-2 §H "(+ WS10 completion state after W2-C)", §I, §J `[REPO]` |
| MG-8: W2-B/W2-C evidence packs diagnose/measure; any semantics change separately authorized | register §3 MG-8 row `[REPO]` |
| Cross-Layer Standard mandatory for this candidate class; O-1/O-2 binding interpretation | `CROSS_LAYER_EXECUTION_ASSURANCE_STANDARD.md` (authoritative, PR #571); ODR acceptance row (PR #572 sync) |
| Routing seam + consumers | `engine/progression_loop.py:99` `select_next_gap`; SEVEN runtime call sites — `progression_loop.py:1045,:1143`, `web/app.py:2457,:2939,:3324,:3410`, **`scripts/run_cli.py:152`** (the governed minimal CLI — a live user-reachable consumer, import at `:151`); non-call references: import `web/app.py:29`, comments `web/app.py:3319`/`progression_loop.py:921`; 16 test files `[EXEC — repair-gate sweep, method in §F]` |
| Question identity | `engine/path_n_questions.py:78` `ServedQuestion` `[REPO]` |

## B. W2-B definition (recovered, not inferred) `[REPO — Wave-2 §H]`

W2-B implements RVR-6a: **bounded adaptive routing / register core**,
Tier-1 STATE-ADAPTIVE only:

1. **Domain-aware routing** through the existing domain-aware seams and
   content gates — no new domain-owner system.
2. **Prior-answer-aware suppression** derived from canonical state + gap
   state + governed evidence + dispositions + `ServedQuestion.question_id`
   (WS10 completion state joins only after W2-C — W2-B must consume it
   ADDITIVELY later, never require it now).
3. **State-aware ordering**: ONE bounded deterministic policy layer over
   the `select_next_gap` core; it may promote exactly: a critical
   unresolved gap; a lapsed acceptance; newly comparable decision state;
   a completed-intent skip. **Multi-trigger determinism (added per
   review N-3):** the repository defines the closed four-trigger set but
   NO precedence among simultaneously firing triggers `[EXEC — Wave-2 §H
   orders nothing among them]`; therefore the implementation candidate
   MUST define ONE deterministic precedence/tie-break policy, state it
   explicitly in its evidence pack as a PROPOSAL subject to Owner
   exact-SHA acceptance (never presented as pre-existing fact), and
   prove: same canonical state → same ordering; simultaneous-trigger
   composition tested; starvation risk tested; and no fifth implicit
   trigger appears. No trigger is added or removed here.
4. **Unknown-aware rerouting**: accepted risks are not re-asked; a
   visible governed cue explains why; reopening happens ONLY through a
   correction lapse (consuming the existing W2-D lapse machinery — R4-C
   semantics untouched).
5. **Evidence-weighted reversible register calibration with
   deterministic hysteresis** (§C/§D below) — the "register core".
6. All selection/derivation logic = pure functions of committed content +
   canonical state (deterministic, replayable, reversible; no persona, no
   hidden profile, no model inference, no permanent expert flag; NEUTRAL
   on insufficient/conflicting evidence).

**RVR-6a ↔ W2-B relationship:** W2-B is the implementation slice OF
RVR-6a; RVR-6b (WS10 content + intent-aware completion + W1-N3) is W2-C,
separately authorized later.

## C. W/M — recovered semantics and the governed value-freeze procedure

**Recovered definition `[REPO]`:** W and M are the **bounded deterministic
hysteresis parameters of the evidence-weighted reversible register
calibration** (OD-R5). The repository consistently uses them as the pair
"W/M hysteresis values"; it does NOT define individual letter expansions
or an enumerated allowed-value space — that absence is stated here as a
fact, not papered over.

**Recovered constraints on any future values `[REPO — OD-R5 + §G]`:**
bounded; deterministic (same evidence stream → same register trajectory);
Owner-approvable; REVERSIBLE (the calibration must be able to lower —
no permanent flag, so the lowering parameter must be finite and
effective); hysteretic (raise and lower thresholds are distinct so the
register cannot flap on single data points); NEUTRAL on
insufficient/conflicting evidence (no value may force a non-neutral
posture without qualifying evidence).

**Value-freeze procedure — frozen here, values deliberately NOT set here
`[PROPOSED, enacting Wave-2 §P verbatim]`:** the exact W/M values are
**proposed and frozen inside the future W2-B implementation
candidate/evidence pack** — justified there against the RED evidence that
produces them — and become fixed through **Owner exact-SHA acceptance of
that W2-B implementation candidate**. Proposing numbers at THIS
authorization gate would recreate the OD-W2-WM pre-gate that Wave-2 §P
explicitly WITHDREW AS CIRCULAR ("the values are produced by W2-B
evidence"). Status-surface wording "W/M values fixed at its acceptance"
is hereby reconciled to exactly this §P meaning: acceptance OF THE
IMPLEMENTATION CANDIDATE, not of this contract. The implementation
candidate MUST present the proposal as:
`FIELD | DEFINITION | CONSTRAINT CHECK | EVIDENCE | PROPOSED VALUE |
CONSEQUENCE` — with every value classified `FACT`-grounded (derived from
its own RED evidence) or explicitly `OWNER PREMISE`, never silent.

**Owner decision isolated:** the ONLY Owner decision this gate requires
is acceptance of this contract itself. No separate W/M decision exists
now — by the frozen §P design.

**Carried synchronization obligation (recorded here, executed ONLY at
the later post-acceptance status-sync gate — those surfaces are
deliberately untouched by this one-file candidate):** the current
ODR/roadmap/CPS/AIC wording family "W/M values at its acceptance
(Wave-2 contract §H)" miscites the operative source — Wave-2 §H
contains no W/M text; the operative source-owner rule is **§P** — and
the phrase "at its acceptance" must be disambiguated there to "at
Owner exact-SHA acceptance of the W2-B IMPLEMENTATION candidate."

## D. Register core — evidence basis rules `[REPO §G, frozen forward]`

- Architecture **A**: deterministic recomputation from stored
  `AssertionRecord.content` via the EXISTING pure assessors
  (`_structured_technical_form` and companions; `addresses_gap`); no new
  persistent fields `[HYPOTHESIS — confirmed or falsified by W2-B's RED
  tests; if recomputation proves semantically insufficient, option B (a
  separately governed record-schema addition) requires its OWN gate and
  is NOT pre-authorized]`.
- The stored `quality` field is a state-level leading-evidence aggregate
  (`app.py` area per §G) and **MUST NOT be consumed as an answer-local
  signal** anywhere in W2-B; the W2-B evidence pack MUST restate this
  disclosure. Changing what the route records is a record-semantics
  change OUTSIDE this contract.
- The register is DERIVED — recomputed from the ledger — never a second
  persisted canonical model; reconstruction/replay must reproduce the
  identical register state (byte-equivalent where serialized).
- Decision-capture state (W2-A) may be CONSUMED read-only ("newly
  comparable decision state" promotion); W2-B never mints, alters, or
  supersedes decision-action records.

## E. Scope — exact, and exact non-goals

**IN scope (the §B capabilities, and nothing else):** the routing policy
layer over `select_next_gap`; the derived register core; suppression;
unknown-aware rerouting with its governed visible cue; the EN/AR catalog
entries for W2-B's own new cues; the RED/GREEN evidence pack (incl. W/M
value proposal and MG-8 diagnosis §K.6).

**NON-GOALS (explicit):** W2-C / RVR-6b; WS10 content authoring or
loader-contract decision (OD-W2-WS10-SCOPE, before W2-C freeze); W1-N3;
OD-PDVG-12 "Why this matters" render (`NOT AUTHORIZED`); Tier-2
meaning-adaptive questioning (OD-PDVG-10 undecided); RVR-7 Arabic parity
(Wave 3); RVR-8; second S2 run; FCORA execution; R4-C semantic change;
any record-schema/disposition change; decision-capture changes; DW
Path-T; CAP-12/CAP-13/IoT/Drones/Renewable activation; persistence or
export expansion; deployment/production/release/paid activation; repair
of the `derived_readiness` or withdrawn-note residuals.

## F. Cross-Layer Execution Assurance Standard application `[PROPOSED, per the authoritative Standard]`

- **Change class: C2 + C4** (material cross-layer: engine policy → route
  → rendered cues; user-facing composition change), **with §6.1
  State-Transition Matrix applicable** (question-serving transitions are
  altered: suppression, promotion, rerouting, lapse-reopening) and
  **§6.5 reload/reconstruction verification applicable** (derived
  register + routing must be reconstruction-stable). **§6.3
  Intent-vs-Payload/Retry Matrix: NOT applicable as scoped** — W2-B adds
  no mutating route; if implementation adds ANY mutating route/action,
  the class escalates to C3 and §6.3 becomes mandatory (this exclusion is
  reviewable, per the Standard).
- **O-1 respected:** this C-classification is a separate axis; the Lean
  classification for the implementation remains LEVEL 2 / DEPTH per the
  standing model, and review tier is set by the risk model — neither is
  downgraded by the C-class.
- **Consumer Propagation Sweep (O-2): REQUIRED.** Seed inventory
  `[EXEC — re-run at this repair gate; reproducible method: GNU grep,
  `grep -rn "select_next_gap" --include="*.py"` over the ENTIRE worktree
  at the authoritative base (no path exclusions except `__pycache__`),
  results classified into runtime call sites / imports / comments /
  tests]`: **SEVEN runtime call sites** — `progression_loop.py:1045`
  (completion), `:1143` (serving), `web/app.py:2457` (render), `:2939`
  (accept-risk gate), `:3324` (evidence record), `:3410` (targeted gap),
  and **`scripts/run_cli.py:152`** — the governed minimal CLI (import at
  `:151`), a live USER-REACHABLE consumer that must not be omitted
  merely because it is not the primary web journey: the implementation
  must adjudicate the policy layer's effect on the CLI exactly like the
  web consumers. Non-call references (classified, not consumers): the
  import at `web/app.py:29`; comments at `web/app.py:3319` and
  `progression_loop.py:921`. Sixteen test files reference the seam and
  are adjudicated by the implementation-time sweep. The implementation
  candidate MUST re-run and record the sweep with its reproducible
  method (terms, scope, tool style, categories, resulting inventory) —
  because future code may change this seed — and adjudicate EVERY
  consumer against the new policy layer (each: verified-contained /
  verified-updated / escalated).
- **Requirement vs Behavioral Composition Coverage:** reported
  separately; composition flows MUST include at least: answer → suppress
  → correct → lapse → reopen; accept-risk → reroute → cue → correction
  lapse → re-ask; register raise → contrary evidence → reversible lower;
  reconstruction mid-journey → identical routing; W2-A decision state →
  "newly comparable" promotion; legacy project (no decision records) →
  unchanged behavior where no trigger applies.
- **Both Grills** (Compliance + Break-the-Product) + substantive
  self-invalidation, per the Standard.
- **Continuous Traceability chain:** OD-R5/Wave-2 §H (governance) → this
  contract (requirement) → the §G implementation surfaces → the session
  cues (user-reachable) → the §K/§L evidence → register-row disposition.

## G. Implementation surfaces — anticipated allowlist (revalidate at implementation)

| Path | Bounded purpose |
|---|---|
| `engine/progression_loop.py` | the ONE bounded deterministic policy layer over `select_next_gap`; unknown-aware rerouting; suppression consumption. The W2-D `substantive_attempt_recorded` gate, `accept_gap_risk` writer, and replay semantics stay byte-unchanged |
| NEW `engine/adaptive_register.py` (name indicative) | the derived evidence-weighted register (pure recomputation; hysteresis; NEUTRAL default) — a NEW bounded module because no existing owner computes register calibration (adjudicated §I); never persisted |
| `web/app.py` | render context for the governed cues; NO new mutating route within this scope |
| `web/templates/session.html` | the visible governed cue(s) (accepted-risk not-re-asked; rerouting explanation) |
| `web/ui_text.py` | governed EN/AR pairs for every new W2-B cue |
| focused W2-B test modules under `tests/` | the §L inventory |

**Forbidden surfaces:** `engine/idea_state.py` and
`engine/record_contract.py` (no schema/disposition change);
`engine/decision_workspace.py` / `engine/decision_composition.py` (W2-A
surfaces untouched); `engine/derived_readiness.py`;
`engine/deliverable_assembler.py`; `engine/requirement_landscape.py`;
export/read services; domain packs; anything outside the allowlist —
outside-allowlist need ⇒ STOP and scope adjudication.

**Digest-pin bounded conditional allowance (repaired per Independent
External Review D-1; independently re-verified at this repair gate
`[EXEC]`):** exactly THREE enforcing test files pin
`engine/progression_loop.py` by SHA-256 —
`tests/test_p9_mech_i3_signal_quality.py`,
`tests/test_p9_mech_i4_boundary_corpus.py`, and
`tests/test_p9_mech_i5_question_sufficiency.py` — all currently at
`756e524adc681906f20eb64a0ae28e3abb56cadf7ade07424b7bf237d4adbcb4`,
which equals the authoritative base digest of the file (`sha256sum`
verified). ALL THREE are covered by this bounded conditional allowance:
ONLY if `engine/progression_loop.py` changes under authorized W2-B
implementation; ONLY the mechanical digest re-freeze via the
established disclosed lineage-comment mechanism; NO behavioral edit of
any kind in these test files; NO unrelated P9 scope expansion; any
behavioral change in them requires separate scope authority. This
completes the allowance so a mechanically foreseeable pin failure
cannot force a mid-implementation authorization STOP (the IG-17
mid-lifecycle-extension cost precedent), while the integrity fence
stays intact.

## H. Determinism / compatibility / reachability requirements

- Same committed ledger + canonical state → identical routing decision,
  identical register state, identical cues (byte-equivalent where
  serialized); insertion-order independence; no timestamps/randomness in
  any canonical W2-B computation.
- Reconstruction parity: cold reload reproduces routing + register + cues.
- Legacy compatibility: a project with no qualifying evidence and no
  decision records routes EXACTLY as today (the policy layer is
  behavior-preserving when no trigger fires — RED-tested).
- User reachability: the rerouting/suppression cues render in the
  existing session journey; no new page, no second journey; EN/AR per
  the existing single-language policy (no RVR-7 expansion).
- Provenance: W2-B mints no records; every consumed signal's provenance
  is the existing ledger truth; the register derivation cites which
  records fed it (evaluator-facing evidence, not UI claims).

## I. Ownership adjudication (both directions)

| Capability | Current owner | Fit | Action |
|---|---|---|---|
| Routing policy over `select_next_gap` | `engine/progression_loop.py` | EXACT | extend in place (bounded layer) |
| Register calibration | none exists `[EXEC — no module computes evidence-weighted calibration]` | NONE | NEW bounded module under this contract (not a duplicate; not force-fit into progression_loop, which owns lifecycle, or derived_readiness, which owns verification) |
| Suppression identity | `ServedQuestion.question_id` (`path_n_questions.py`) | EXACT | consume, never re-mint |
| Cues UI | session template + ui_text | EXACT | extend |
| Lapse/reopen signals | W2-D reconstruction outcomes | EXACT | consume read-only |

No duplicate owner created; no false reuse found.

## J. Before-W2-B obligation sweep (register at this base)

| ID | Status | Owner | Trigger | Due now? | Evidence | Disposition |
|---|---|---|---|---|---|---|
| Cross-Layer Standard row | CLOSED — evidence verified | Standard doc | — | satisfied | PR #571/#572 | prerequisite for W2-B execution MET |
| RVR-6a row (`:105`) | OPEN — NOT AUTHORIZED YET | Wave-2 §H/OD-R5 | W2-B authorization | **THIS GATE** | this contract | remains OPEN until implementation merges with register/suppression/ordering tests green |
| MG-8 | OPEN — CONDITIONAL | locus progression/intake; owner NONE | W2-B/W2-C evidence packs diagnose/measure | at W2-B EXECUTION (not before authorization) | register row | carried into §K.6 as a W2-B evidence-pack obligation; any semantics change stays separately Owner-authorized |
| OD-W2-WS10-SCOPE | OPEN | Owner | before W2-C freeze | NO (W2-C) | Wave-2 §P.4 | untouched |
| W1-N3 | OPEN | W2-C | W2-C contract freeze | NO | register | untouched |
| `derived_readiness` residual | OPEN — CONDITIONAL | its row | validation-status writes becoming reachable | NO (W2-B adds none) | register | untouched |
| R4-C | OPEN | Owner | adjudication before serious release | NO (W2-B consumes lapse outcomes read-only; semantics untouched) | register | boundary preserved |
| Release-value set (T1-A′/T1-C′/TTV/Differentiation), RVR-7/RVR-8, §4/§5 buckets | OPEN per rows | per rows | later gates | NO | register | untouched |

**No blocker-before-authorization remains.**

## K. Acceptance criteria (implementation candidate, future gate)

1. All §L RED requirements GREEN, non-vacuous (mutation probes on the
   suppression, promotion, hysteresis, and cue mechanisms).
2. Negative paths: no suppression without qualifying active evidence; no
   promotion without its exact trigger; register NEUTRAL on
   insufficient/conflicting evidence; reopening ONLY via correction
   lapse; a suppressed question's cue never claims resolution.
   **Added per review N-4:** (a) **all candidates suppressed** —
   deterministic outcome; no silent false resolution; no fabricated
   answer; governed user-visible behavior where applicable; no crash or
   undefined routing; (b) **multiple promotion triggers firing
   simultaneously** — deterministic precedence/tie-break (§B.3);
   repeatable across reload; no starvation and no hidden fifth policy;
   same canonical state → same result.
3. Behavior-preservation: trigger-free projects route byte-identically
   (full legacy suite green; frozen-behavior RED tests).
4. W/M values proposed per §C's table with evidence; constraints checked.
5. Consumer sweep re-run and recorded per O-2.
6. Evidence pack includes: the §D `quality`-aggregate disclosure; the
   MG-8 diagnosis/measurement (register §3 row); Requirement vs
   Composition coverage reported separately; State-Transition Matrix;
   reconstruction-parity evidence; full suite with every delta explained
   against the prior authoritative baseline.
7. Both Grills PASS; the §F composition flows exercised through the real
   journey.

## L. RED inventory (categories; exact tests frozen at implementation-contract detail level)

`W2B-ROUTE-*` ordering/promotion (each §B.3 trigger + no-trigger
preservation + **simultaneous-trigger precedence determinism +
starvation + all-candidates-suppressed outcome**, per §K.2 a/b);
`W2B-SUPP-*` suppression (active-set discipline;
superseded/withdrawn answers do not suppress; question-id scoping);
`W2B-REG-*` register (hysteresis raise/lower; reversibility; NEUTRAL;
determinism; no persistence); `W2B-REROUTE-*` unknown-aware rerouting +
cue + lapse-reopen composition; `W2B-DET-*` byte-determinism +
insertion-order + reconstruction parity; `W2B-COMPAT-*` legacy
preservation + full suite; `W2B-LANG-*` EN/AR cues; `W2B-CONS-*` one
adjudication test per swept consumer.

## M. Product / user-value basis (falsified, §Q-anchored `[REPO]`)

Solves: repetitive questioning (answered/accepted things re-asked);
non-responsive ordering; invisible unknown-handling. Omission cost: the
Wave-2 §Q product-value claims (prior-answer responsiveness, reduced
repetition, perceived responsiveness) remain undeliverable. Shallow-
implementation risk: a suppression layer that hides questions without the
governed cue would REDUCE truthfulness — hence the cue + negative-path
criteria are acceptance-blocking, not cosmetic. No existing workstream
owns this (adjudicated §I). Value claims stay evaluator-facing; T1-A′/
T1-C′/TTV/Differentiation remain OPEN — nothing here is release-value
proof.

## N. Lifecycle states (preserved exactly)

1. THIS candidate accepted+merged ⇒ `W2-B CONTRACT AUTHORITATIVE`.
   `[REPO]` Wave-2 §M defines the exact-SHA serialized lifecycle.
   `[DERIVED — attribution corrected per review N-1]` That contract
   acceptance constitutes the Owner gate the roadmap/ODR name
   "`W2-B AUTHORIZATION`" follows from COMPOSITION of: the authoritative
   next-gate naming on the current status surfaces; the W2-A lifecycle
   precedent (contract acceptance at PR #567 preceded a SEPARATE
   implementation-start authorization); and the Wave-2 serialized
   lifecycle structure — §M itself does not state the equivalence, and
   no new Owner decision is invented here. The distinctions
   `CONTRACT AUTHORITATIVE` ≠ `IMPLEMENTATION AUTHORIZED` ≠
   `IMPLEMENTATION AUTHORITATIVE` stand unweakened;
2. implementation proceeds ONLY under a subsequent explicit Owner
   implementation-start instruction (the W2-A precedent);
3. `W2-B IMPLEMENTATION AUTHORITATIVE` only at Owner exact-SHA
   acceptance + merge of the implementation candidate (which also
   freezes W/M per §C);
4. register RVR-6a row closes only on that implementation evidence.

## O. Repository & integration health coverage (bounded check, no new owner)

Route integrity/500s/reachability: ALREADY COVERED (existing suites +
UG1 smoke + Standard §6.6). Dormant/orphan detection: ALREADY COVERED
(Standard traceability + future FCORA). Workflow/verification health:
**the repository has NO CI workflows** (no `.github/` directory exists
at the base `[EXEC]`) — coverage comes from the lifecycle's own
mechanisms: local full-suite verification at every implementation gate,
the Universal Guardrail / UG1 smoke, exact-SHA publication/merge
discipline with empty candidate→merge diffs, and post-merge
verification; stated as such, ALREADY COVERED by those mechanisms, and
this contract creates NO CI requirement or owner (absence of CI is not
a blocker under any authoritative governance). Dependency pins: ALREADY
COVERED (pinned requirements + the O-5 environment note). Merge
safety/post-merge smoke: ALREADY COVERED (lifecycle + UG1). TRUE GAP:
none found relevant to this authorization.

## P. Self-invalidation record `[EXEC]`

Evidence that would invalidate this candidate was actively sought:
a repository definition of individual W/M letter meanings or an
enumerated value space (none exists — stated as fact); an authority
fixing W/M at THIS gate (contradicted by Wave-2 §P's withdrawal of the
circular pre-gate — reconciliation recorded §C); an existing register
owner (none); a Before-W2-B blocker (sweep §J — none); a W2-B mutating
route that would force C3 (none in scope; escalation rule frozen §F);
contradictions across CPS/AIC/roadmap/ODR/register/Wave-2/Standard
(one ambiguity found and resolved: "W/M fixed at its acceptance" = §P's
implementation-candidate acceptance; no other contradiction). None
invalidated the candidate.
