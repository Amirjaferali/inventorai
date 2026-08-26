# W2-C / RVR-6b — Implementation Evidence Pack

**Status:** committed evidence artifact of the W2-C/RVR-6b implementation
candidate. NOT a status surface; NOT self-certifying — every claim is
re-checkable from this tree's code, content, and tests.

**Candidate Identity Binding (anti-circular, per the authoritative contract
§P):** BASE = `6b4629d75b58690eb0a40a754e747ba79f265447` (PR #580 — the
authoritative post-W2-C-contract sync merge; verified live at this gate:
0 commits after; parents `d796b0cd…` + exact accepted sync candidate
`21c6076…`). AUTHORITY = the authoritative W2-C/RVR-6b contract
(`W2_C_RVR6B_IMPLEMENTATION_CONTRACT_CANDIDATE.md`, PR #579, accepted
candidate `455cb502…`) + the exercised OD-W2-WS10-SCOPE decision (ODR
Wave-2 §A row) + the Owner's separate W2-C implementation-start
authorization. This file records the candidate's base, authority, changed
paths, and evidence INSIDE the tree; the candidate's own final commit
SHA/tree are recorded EXTERNALLY post-freeze (gate report + SHA-preserving
bundle) and become bound to this file only through Owner exact-SHA
acceptance.

## 1. Changed paths (complete; classification per contract §26)

| Path | Class | Why |
|---|---|---|
| `docs/governance/path_n_content_config/electronics_electrical_question_intent_registry.json` (new) | CONTRACT-REQUIRED | the electronics per-domain WS10 registry instance (11 ids) |
| `docs/governance/path_n_content_config/mechanical_question_intent_registry.json` (new) | CONTRACT-REQUIRED | the mechanical per-domain WS10 registry instance (10 ids) |
| `engine/intent_serving.py` (new) | CONTRACT-REQUIRED | the W2-C module: registry access, paired marker sets, coverage, serving law, W1-N3 supplement |
| `engine/progression_loop.py` | EXISTING-OWNER INTEGRATION | ONE purely additive hunk after the canonical `addresses_gap` consultation: the fail-closed W1-N3 supplement (§6) |
| `web/app.py` | EXISTING-OWNER INTEGRATION | ONE render-only hunk in `show_session` after the W2-B block: the W2-C question-slot law under the composed precedence (§5) |
| `tests/test_w2c_rvr6b_registry.py`, `_serving.py`, `_w1n3.py`, `_web.py` (new) | TEST / EVIDENCE | 48 focused tests (14 + 14 + 11 + 9, mechanically collected per module) |
| `tests/test_p9_mech_i3_signal_quality.py`, `_i4_boundary_corpus.py`, `_i5_question_sufficiency.py` | EXISTING-OWNER INTEGRATION (digest re-pin) | the three enforcing pins for `engine/progression_loop.py`, re-pinned under the contract §M bounded allowance (§9) |
| `docs/governance/W2_C_RVR6B_IMPLEMENTATION_EVIDENCE_PACK.md` (new) | TEST / EVIDENCE | this pack |

UNRELATED changed paths: **0**. No loader change; no domain/schema/
dependency/deployment change; no combined registry; no new identities.

## 2. Exact 21-id registry source map `[EXEC]`

Both registries validate through the byte-unchanged D11/D19 loader
(`engine/question_intent_registry.py`) against their committed source
artifacts with exact ID-set equality; record order = committed artifact
order; every record carries intent metadata (primary_intent /
answer_objective / completion_condition) and a consistent source_reference.

| Source id (domain) | Loader result | Runtime consumer | Reload |
|---|---|---|---|
| `N-MC-1 … N-MC-4`, `N-PF-1 … N-PF-4`, `N-BA-1 … N-BA-3` (electronics_electrical, 11) | validated, ordered | `engine.intent_serving` (coverage gate + per-id identity check) | deterministic (load-once of committed content; failure NOT cached) |
| `mechanical:MECHANISM_COMPLETENESS:Q1…Q4`, `mechanical:PHYSICAL_FEASIBILITY:Q1…Q2`, `mechanical:BOUNDARY_AMBIGUITY:Q1…Q4` (mechanical, 10) | validated, ordered | same | same |

Total 21; no invented/placeholder/decision identities. Tests:
`test_w2c_rvr6b_registry.py` (exact id lists asserted; marker-table keys ==
exactly the 21 committed ids; every marker entry EN/AR-paired and
non-empty).

**Declared limitation (registry path binding):** the ratified loader
equality checks (D8 metadata.source_artifact; D6 record
source_reference.artifact_path) bind to the exact path STRING passed at
load. The committed registries record repository-relative paths, so runtime
loading requires the process working directory to be the repository root
(true for the test suite and the governed web entrypoint). Elsewhere the
accessor fails closed and canonical serving proceeds unchanged — a truthful
degradation, mechanically tested (`test_accessor_fails_closed_*`,
`test_fail_closed_registry_outage_serves_canonical`).

## 3. Intent-coverage state

Derived per-variant coverage: a committed variant is covered iff at least
one ACTIVE `answered` ledger record of the SAME gap carries the variant's
committed intent vocabulary (EN substring on lowered text, or the paired
Arabic surface). Pure function of canonical state + committed content;
never persisted; reversible (superseding the contributing record removes
coverage — tested); insertion-order independent (canonical `rec_N` sort —
tested); reconstruction recomputes it identically (tested live-vs-recon).
Coverage is a SUPPRESSION/ORDERING INPUT ONLY — no WS11 verdict, no
SATISFIED, no gap completion, no user-facing progress claim, no persistence.

## 4. Serving law (suppression + within-gap ordering), route-live

Law (render-time, current gap only): canonical index-law variant uncovered
→ inert (canonical serves verbatim); covered → the next later uncovered
variant, else the earliest uncovered (recovery of a missed intent), else
inert (all covered — the governed clamp/stall-reframe/exit machinery is
never overridden). Decision-aware deference: while the W2-B alternatives
transition is active, the question slot stays canonical.

**Route-live evidence** (`test_w2c_rvr6b_web.py`, real client through
`/start` → answer → render): mechanical covered-intent suppression (a
recorded "force path" answer makes the Q2 turn serve Q3 — the covered
intent is not re-asked); the identical adjustment from the paired ARABIC
answer; electronics covered-intent suppression (N-MC-2 → N-MC-3);
uncovered journeys byte-canonical; stall-reframe/exit surfaces untouched at
exhaustion; registry outage → canonical (fail-closed); Arabic UI renders
the same adjusted committed variant (UI-language independent of coverage).
Zero new user-facing strings (suppression is silent journey improvement —
no completion badge, no progress claim); one primary CTA preserved by
construction (one served question/action per stage, unchanged).

## 5. Exact W2-B × W2-C composed precedence (PROPOSED here; Owner-accepted only at exact-SHA acceptance)

```
1. W2-B question-slot overrides — W2B_QUESTION_SLOT_PRECEDENCE
   (LAPSED > SKIP > CRITICAL) — always win the question slot (the web
   consumption applies W2-C ONLY under `question_override is None`).
2. W2-B alternatives transition (action slot): W2-C question adjustment
   DEFERS (canonical question; decision-evidence action block is the one
   primary CTA). Read-only decision awareness; FDC-001 untouched.
3. W2-C intent-coverage law — applies only when the displayed question IS
   the plain canonical Path-N variant (checked verbatim against
   `get_question`), so the RVR-2 stall reframe, the exhausted exit prompt,
   and the generic fallthrough are never overridden.
4. Canonical serving — baseline and the universal fail-closed target.
```

Amendment-1 §6 discipline evidence: real served consequence (§4 route
tests); same-state determinism + insertion-order independence + reload
parity (serving suite); starvation analysis — the canonical index still
advances on the canonical schedule and the reframe/exit machinery fires at
exactly the canonical iterations (guard 3 excludes those surfaces), so no
governed surface is starved and W2-C is inert on plain journeys; fail-closed
(every guard + exception path → canonical, tested at module and route
level); one-primary-CTA (no stacking: W2-C never fires alongside any W2-B
override — structurally enforced by guard 1/2); interaction with ALL W2-B
triggers (LAPSED: live correction-lapse journey test — the reopened gap
serves its truthful committed question and the governed cue; SKIP/CRITICAL:
route-limited per the accepted RVR-6a disclosures — their overrides
structurally precede W2-C via guard 1, and the reframe/exit exclusion is
route-proven at exhaustion); suppression/ordering/decision interaction
(serving suite incl. deference-expiry); no unilateral W2-B reorder (W2-B
sources byte-unchanged except the single additive integrate hunk — see §9);
no cross-gap promotion (`select_next_gap` never consulted — poisoned-owner
fence test).

## 6. W1-N3 bounded attempt — **OUTCOME: CLOSED WITH EVIDENCE (bounded)**

* **Reproduction** `[EXEC + test]`: on the frozen S2 fixture
  (`tests/fixtures/s2_run_001_answer_maps.json`), the M-1 expert MECHANISM
  answer #2 ("Force path: wheelchair load through the deployed ramp into
  the retention mechanism at the hinge line; manual actuation…") is judged
  NOT addressing by the byte-unchanged family test — the exact recorded
  W1-N3 residual (one honest restatement before MECHANISM closed).
* **Bounded closure**: the question-id-scoped supplement (consulted by
  `integrate_response` only after the family test says "not addressing")
  recognizes the answer through the displayed variant's committed paired
  vocabulary ("force path" / "مسار القوة"), and the answer then advances
  MECHANISM exactly like a family-relevant answer (known_mechanism captured,
  gap PARTIAL) — EN and AR identically. End-to-end tested through
  `integrate_response` in both languages.
* **No false positives**: the family test (`gap_relevance`) is
  byte-unchanged; the supplement is scoped to ONE variant's committed
  vocabulary per serving; weak refusals never gain relevance; the full
  PVCG-R2/R2-marker/RVR-2 relevance suites and the PVCG-R3
  semantic-stability suite (including the differential EN/AR adversarial
  categories) pass unchanged. During implementation the first marker draft
  DID trip the R3 differential gate (the committed "spring tension" example
  vocabulary — exactly the historically measured leak class); the sets were
  narrowed to question-distinctive phrases and the gate now passes — the
  falsification discipline worked and is recorded here, not hidden.
* **Replay-parity scope rule (deliberate)**: the supplement's scope is the
  CANONICAL index-law variant, never the ledger-dependent adjusted display,
  because reconstruction replays `run_iteration` over an initially empty
  ledger (restored verbatim only after the replay loop) — a
  ledger-dependent scope would diverge live-vs-replay (the W2-B
  ledger-less-replay lesson). Under an adjusted display a supplemental
  match for the adjusted variant is deliberately NOT consulted — a safe
  false-negative. Live-vs-reconstruction parity is proven on a real durable
  journey that exercised the supplement (`test_reconstruction_parity_*`).
* **Remaining KNOWN BOUND (declared, unchanged ownership)**: the fixture
  also shows family false-negatives outside the recorded W1-N3 case
  (e.g. the expert BOUNDARY "Must hold:…" and PROBLEM_MECHANISM_FIT
  answers, the novice EXPERTISE answer). These are the pre-existing
  R2/R3 declared residual — NOT W1-N3 (whose authoritative definition is
  the M-1 MECHANISM restatement), NOT newly created, and NOT silently
  repaired: `gap_relevance` / the RVR-2 family remains their owner and
  RVR-7 remains the mandatory downstream input (OD-R4).
* `W1-N3 SATISFIED (bounded scope): YES — CLOSED WITH EVIDENCE`;
  `DEFERRED: NO`; no ambiguous "completed" claim; the DOR row's closure
  criterion ("W2-C RED test vs frozen S2 R6 fixture passing without new
  false positives") is exactly the committed test set above.

## 7. Mandatory lapsed-acceptance / stale-index revalidation — **OUTCOME: B. NOT AFFECTED (mechanical proof + live leg)**

Mechanical proof: (1) `w2c_served_question` has exactly ONE consumer —
the `show_session` render block (`git grep` census) — and mutates nothing:
the lapse reopen/landing index is engine-side state the render never
touches; (2) the only state-affecting W2-C surface (the supplement) is
ledger-independent (§6 scope rule) and runs identically live and in
reconstruction replay, so the reopened/lapsed landing behavior recomputes
identically; (3) guard 3 (§5) excludes every non-canonical-variant surface,
so the reopened gap's canonical re-ask is only ever replaced by a truthful
committed variant of the SAME gap under positive coverage evidence. Live
leg: the full correction-lapse journey (risk-accept → correct → re-close →
reopen) runs with W2-C active and the reopened area serves a truthful
committed PF question with the governed lapse cue
(`test_w2b_lapse_flow_and_revalidation_live_leg`), and the entire W2-B web
suite (including its lapse test) passes unchanged. RVR-6a is not reopened;
no lapse repair invented.

## 8. EN / AR evidence

EN behavior: §4/§6 route + engine tests. AR behavior: the paired-surface
coverage/suppression route test (Arabic answer → identical adjustment) and
the AR fixture supplement/integration tests. Semantic equivalence: every
marker entry is EN/AR-paired by construction (asserted for all 21 ids);
the W1-N3 EN/AR pair produces identical outcomes end-to-end; the PVCG-R3
differential adversarial suite passes (no NEW off-diagonal EN/AR
divergence). UI-language/input-language separation: the Arabic-UI page
serves the same adjusted committed variant (test). No new user-facing
strings were added at all, so no simultaneous EN+AR label display can
arise from W2-C (mechanically: zero `ui_text` delta, zero template delta).

## 9. Digest re-pin (bounded allowance) + W2-B surface integrity

`engine/progression_loop.py` before:
`3b531cc8e5126b956ba9ce6ba103dafb83677f8077992a166e3e7f8d26ff2a08`; after:
`a7e8bd62b9ab76aaba5889ce52b5f32ee646b2817ba1c790ed7a231d259fa41f` — the
delta is exactly ONE additive comment+guard hunk (the fail-closed W1-N3
supplement consultation); no existing line semantics changed; the three
enforcing pin tests re-pinned to the new digest and passing. The W2-B
section (register import surface, four triggers, precedence tuple,
`compute_serving_decision`) is byte-unchanged; the entire 67-test W2-B
suite passes unchanged.

## 10. Canonical ownership audit

`select_next_gap` sole gap owner (poisoned-owner fence test; no W2-C read);
`gap_relevance` sole relevance owner (byte-unchanged; supplement is
widening-only composition at the single consultation site);
FDC-001/DecisionRecord sole readiness owner (read-only deference; no
decision write/claim; W2-B decision suite unchanged); `AssertionRecord`
carrier role unchanged (read-only ledger consumption via the W2-B canonical
pattern); `semantic_registry` untouched; WS11 dormant (module untouched;
still zero non-test consumers); WS12 untouched; W=2/M=2 untouched
(`adaptive_register` byte-unchanged; no hidden coefficient — the W2-C law
has NO numeric tuning parameter); MG-8 semantics untouched (the level-0
intake seam and `known_problem`/`idea_summary` guards are byte-unchanged;
the supplement widens in-gap relevance exactly as any relevance outcome
feeds the pre-existing conditional logic — no intake-seam change, no MG-8
repair); full adaptive questioning remains OFF; Tier-2 remains OFF;
OD-PDVG-12 remains unexercised (no explainability render — zero template
delta proves it mechanically).

## 11. Negative / fail-closed matrix (all tested)

missing registry; malformed registry (INVALID_JSON); unknown question id
(match-nothing + registry.get gate); duplicate question id (loader);
cross-domain id leakage (per-id marker scope test); partial registry
coverage (loader SOURCE_ID_SET_MISMATCH — no partial registry ever
returned); duplicate intent id (loader); stale/reconstructed state
(parity test); already-covered intent (suppression + all-covered inert);
conflicting W2-B trigger (deference + guard-1 structure + live lapse
journey); no decision state (plain journeys byte-canonical);
incomplete decision state (single alternative — no deference, no fire);
bilingual input/UI mismatch (AR answer under EN UI; EN content under AR
UI); reload parity; no current gap; malformed/unmapped gap type;
lapsed/reopened state (live leg §7). Every failure direction is inert/
canonical — no silent semantic invention.

## 12. Test truth `[EXEC at this exact tree]`

* Focused W2-C suites: **48 passed** (registry 14, serving 14, W1-N3 11,
  web 9 — per-module counts mechanically collected with
  `pytest --collect-only` per exact module, then executed).
* Affected family (methodology in §13): **1637 passed / 0 failed /
  0 skipped / 0 xfailed** across the 22-module unique manifest enumerated
  there, executed as ONE deduplicated pytest invocation at this exact tree.
* Full suite: **4710 passed / 3 skipped / 1 xfailed / 0 failed** —
  baseline 4662/3/1/0 (PR #577-era, re-verified at the RVR-6a closure
  gate); delta = exactly the 48 new W2-C tests. The 3 skips / 1 xfail are
  the pre-existing environment-conditional baseline, unchanged.
* Mutation differential `[EXEC]`: emptying the marker table reverts
  suppression AND the supplement to canonical/False (the tests measure the
  implementation, not incidental state); restoring restores.
* During-implementation RED evidence: the R3 differential gate genuinely
  REJECTED the first marker draft (§6) — the guarding suites demonstrably
  bite.

## 13. Affected-family methodology (defined before counting)

INCLUDED — the exact deduplicated 22-module manifest (raw enumeration 22,
unique 22, duplicates 0), by category:
4 new W2-C suites (`test_w2c_rvr6b_registry`, `_serving`, `_w1n3`, `_web`);
6 W2-B suites (`test_w2b_amc_register_calibration`, `_serving_policy`,
`_decision_transition`, `_web_serving`, `_matrix_parity_mg8`,
`_consumers` — same serving surface, ledger reads, precedence);
3 relevance owners (`test_pvcg_r2i_gap_relevance`,
`test_pvcg_r2i_marker_coverage`, `test_wave1_rvr2_flow_and_relevance`);
1 EN/AR equivalence owner (`test_pvcg_r3i_semantic_stability`);
2 WS10 owner suites (interface contract + behavioral validation);
1 WS11 dormancy suite (base RED);
2 Path-N serving owners (`test_phase2_path_n_selection`,
`test_dgmpr_d3_path_n_domain_neutral_service`);
3 digest-pin suites (`test_p9_mech_i3/i4/i5`).
4+6+3+1+2+1+2+3 = 22. EXCLUDED: everything not consuming the serving
surface, relevance, WS10 content, or the pinned file — outside W2-C's
contract ownership and runtime dependency set (broader indirect consumers
of `integrate_response` — the wider journey/reconstruction suites — are
deliberately left to the FULL suite, which remains the authoritative net;
the family is a declared bounded owner/direct-consumer set, not an
exhaustive dependency closure). WHY: the changed runtime paths are exactly
`intent_serving` (new), one `progression_loop` relevance hunk, one
`show_session` render hunk, and committed WS10 content; these 22 modules
are their owners and direct consumers.
RESULT (one deduplicated invocation of exactly these 22 paths at this
tree): **1637 passed / 0 failed / 0 skipped / 0 xfailed**.
**Evidence-integrity correction lineage (recorded, not hidden — neither
mistake is erased):**
*Rejected candidate #1* (`1249dbbdf69bfc23a7b35f6e302478e995c8319f`,
preserved as rejected evidence) stated "18 modules" with "1443 passed"
against this same enumeration.
*Rejected candidate #2* (`cf77c33dfd560fc2026bc5fe0024ab2f6288ea8d`,
preserved as rejected evidence — Independent External Review IR-I84)
repaired that defect but carried a second one: the FOCUSED per-module
split was recorded as 13/15/11/9 while the mechanically collected
distribution is 14/14/11/9 (total 48 was correct); this candidate records
the collected truth. Root cause of #1: three different runs were conflated — the
"18" was the module count of a pre-narrowing PARTIAL affected-family
command (the 18 non-W2-C paths, which then collected 1589 with the one
genuine R3 differential failure later repaired by marker narrowing); the
"1443" was a separate 8-module post-narrowing verification rerun (R3 +
the 3 relevance owners + the 4 W2-C suites); neither number described the
enumerated 22-module methodology. The corrected figures above come from
executing the exact unique 22-path manifest in one invocation.
This count is the CURRENT methodology's number only — the historical 467
(Creator family) and 484 (reviewer-closest reconstruction) remain
different historical evidence-family measurements, NOT reconciled, NOT
rewritten (the full suite remains the authoritative reproduction).

## 14. Product-value evidence (contract §T; instruction §21)

Real reachable deltas proven on the live route: (1) REPETITION — a user
whose recorded answer already carries a later question's committed intent
is not re-asked it (mechanical Q2 and electronics N-MC-2 suppressed on
real pages); (2) FALSE-NEGATIVE MISSES — the recorded W1-N3 expert answer
now advances MECHANISM instead of forcing a restatement (EN and AR);
(3) ORDER COHERENCE — the within-gap order follows committed intent
coverage instead of blind indexing, and recovers a missed earlier intent
before the clamp; (4) DECISION ROUTING — during a live alternatives
transition the question slot defers so the decision-evidence action stays
the single primary CTA. Simple Outside — Deep Inside: all depth is
committed content + canonical state; the user sees only committed
questions, one at a time; nothing decorative. Fail-closed rather than
invented truth throughout.

## 15. Anti-anchoring / contradiction sweep (executed)

Falsified during implementation and recorded: (a) "positional coverage
suffices" — DISPROVEN (it would have been structurally vacuous within the
serving window — the W2-B rejection lesson applied prospectively; the law
was redesigned to content-based coverage BEFORE freeze); (b) "the
supplement may scope to the displayed variant" — DISPROVEN by the
reconstruction replay ordering (ledger restored after replay), scope made
canonical (§6); (c) "committed example vocabulary is safe as markers" —
DISPROVEN by the R3 differential gate (§6), sets narrowed; (d) "the
loader can be consumed with absolute paths" — DISPROVEN by the D8/D6
string-equality contract; relative-path binding declared (§2); (e) the
contract's implementation assumptions (registry via unmodified loader;
Option-C composition seam; no new tuning parameter) — CONFIRMED against
the current code. No unresolved contradiction; nothing was made to fit.
