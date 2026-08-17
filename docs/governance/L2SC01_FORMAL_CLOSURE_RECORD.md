# L2SC-01 — Substance-Signal Plural-Alias Domain-Completeness — FORMAL CLOSURE RECORD (Candidate; MATERIAL CORRECTION of rejected candidate `360f541`, defect MD-C1)

**Status of THIS record:** governance/documentation-only **FORMAL CLOSURE RECORD CANDIDATE**. It implements
nothing, changes no runtime/test/pack/registry/activation/schema/persistence file, and closes NOTHING else. **The
closure statements in §9 become authoritative ONLY if/when this exact candidate is merged (create-a-merge-commit)
and post-merge verified** through the governed lifecycle (Mandatory Grill → independent external exact-candidate
review → Owner acceptance → SHA-preserving publication → PR → pre/post-merge verification). **`OWNER_DECISION_
REGISTER.md` UNCHANGED** (closure-gate convention — no new Owner decision is required merely to close an
already-accepted implementation).

**MD-C1 correction (this candidate).** The first closure-record candidate,
`360f541caa075a3fd899bfd41ee48304e965f491`, was independently **REJECTED** (verdict: CLOSURE INVALID — MATERIAL
CORRECTION REQUIRED, defect **MD-C1**): its §10 residual-obligations list stale-copied an older closure-record
template's framing and incorrectly claimed `CF-6` and `CF-2`/the ILT-002 public-message question remained live
"OPEN" residuals — contradicting both the authoritative current status (`CF-6 = FULLY DISCHARGED`, `CF-2 =
FORMALLY CLOSED`, both already correctly stated elsewhere in that same record) and this record's own §9 closure
statements. The reviewer independently confirmed L2SC-01 itself is closure-ready and that every other part of the
record — the runtime implementation, MD-A correction, tests, mutation probes, architecture exit criteria, and
closure prerequisites — is correct; only the residual-list contradiction required correction. That candidate is
preserved **immutable, unpushed, unamended** at `refs/rejected/l2sc01-formal-closure-360f541`. THIS candidate
corrects §10 only (see the MD-C1 note there and in §7.C) and is otherwise identical.

## §1. Closure basis and fresh verification

Base: `b8e1274c027707a38a85216b0ef7b43a1eda5e1c` (PR #497 — SHA-preserving merge of the accepted L2SC-01 runtime
implementation MATERIAL CORRECTION candidate `9399f9d179a547bc6a9cc3ea25f8d2a6b1c2c490` onto
`c1cb421d73c53d24cc381ca9238e29613ca7e996`; merge tree `6c6aac98156985286a1d802b6c2d3e0e522795a9` == candidate
tree; candidate→merge diff EMPTY — independently re-verified this gate via `git diff`, `git rev-parse
b8e1274^{tree}`, and `git rev-parse 9399f9d^{tree}`, all matching exactly; freshly re-fetched this gate; working
tree clean).

**Fresh verification at THIS base (this gate, not assumed from a prior report):**
- `engine.domain_rules.get_substance_signal_plural_aliases("mechanical") == {"pistons": "piston", "valves":
  "valve", "actuators": "actuator"}` — exactly 3, matching contract §4's authorized set exactly, no more, no
  fewer.
- `engine.domain_rules.get_substance_signal_plural_aliases("electronics_electrical")` == the 8 historical pairs
  (`sensors`/`relays`/`resistors`/`batteries`/`capacitors`/`motors`/`leds`/`ics`), unchanged from the retired
  engine-hardcoded map.
- `engine.domain_activation._ACTIVATED_DOMAINS == frozenset({"electronics_electrical"})` — unchanged.
- Focused L2SC-01 file (`tests/test_l2sc01_substance_signal_plural_alias.py`): **60 passed**.
- Updated causal-connective file (`tests/test_causal_connective_substance_gate.py`): **178 passed**.
- Full governed suite: **2677 passed / 3 skipped / 1 xfailed / 0 failed** (prior authoritative baseline, before
  the MD-A material correction, `2653 passed / 3 skipped / 1 xfailed / 0 failed`; broader pre-L2SC-01 baseline
  `2616 passed / 3 skipped / 1 xfailed / 0 failed`, already governed at the L2SC-01 contract gate).

## §2. Lineage (nothing reopened)

Contract lineage: first contract candidate `219f7c10c4ba23f795f0461dd831f71052469e65` independently REJECTED
(defect MD-1: insufficient alias-safety screening) and preserved immutable at `refs/rejected/l2sc01-plural-alias-
contract-219f7c1` → corrected contract `021da23` accepted and merged (PR #496, base
`c8e7af24adf2cee31104abc9c810d38e05569c52`; this is the exact 3-pair Mechanical authorized set: `piston`,
`valve`, `actuator`) → runtime implementation candidate `714d538fca7b22cb84e3b18802dcf27aa42e5707` created from
that exact base, independently reviewed, and **REJECTED** (defect MD-A: the mandated MD-1 recurrence guard was
not load-bearing — in 10 of 12 rejected-alias adversarial sentences the alias word sat on the wrong directional
side of its connective, never inspected by the Layer-2 gate, so those guards passed regardless of alias state;
mutation probe 5 was reported CAUGHT only via map-equality assertions, never a behavioral guard). That candidate
is preserved immutable, unpushed, unamended at `refs/rejected/l2sc01-runtime-impl-714d538` — **it is rejected
evidence, never authoritative implementation.**

A corrected candidate, `9399f9d179a547bc6a9cc3ea25f8d2a6b1c2c490`, was created from the exact same authoritative
parent `c1cb421d73c53d24cc381ca9238e29613ca7e996` — **not built on the rejected SHA.** It reapplied the runtime
and domain-pack data from `714d538` **byte-identically** (independently verified via `sha256sum` for all 5
runtime/data files: `engine/domain_registry.py`, `engine/domain_rules.py`, `engine/progression_loop.py`,
`domains/electronics_electrical/domain.json`, `domains/mechanical/domain.json` — zero diff) and corrected ONLY
`tests/test_l2sc01_substance_signal_plural_alias.py`: all 10 vacuous rejected-alias sentences replaced with
direction-correct constructions, individually verified free of `_CAUSAL_STRUCTURE_PATTERNS` confounds and free of
any other canonical substance word in the supporting clause; a new explicit three-way differential proof added
for all 12 excluded signals (clean map → `ASSERTED` / poisoned map with exactly the rejected pair → `REASONED`,
via `unittest.mock.patch` / neutral-control map with an unrelated alias → `ASSERTED`); §12.C tests renamed/re-
documented honestly as sentence-boundary/directional-discipline guards, not plural-specific false-positive
guards. This candidate was independently re-reviewed, accepted, published SHA-preserving, and merged (PR #497,
**this base** `b8e1274`; merge tree == candidate tree). **The runtime implementation itself was never found
defective at any point in this lineage** — only test/probe evidence was corrected.

## §3. Contract exit-criteria matrix (§15 of the frozen contract)

| Requirement (contract §15) | Authoritative evidence | Status |
|---|---|---|
| Registry field + accessor + engine consumption implemented exactly per the frozen §4 3-pair set (never a larger one without fresh review) | §1 fresh verification: `get_substance_signal_plural_aliases("mechanical")` returns exactly `{pistons→piston, valves→valve, actuators→actuator}`; `engine/domain_registry.py` fail-closed validation; `engine/domain_rules.py` accessor; `engine/progression_loop.py` consumes it, no second live source | **PASS** |
| Electronics behavior byte/behavior-identical (proven, not assumed) | `test_green_electronics_plural_alias_registry_derived_byte_identical`, `test_green_electronics_plural_alias_map_lives_in_registry_not_engine` (focused suite, passing); electronics runtime/data byte-identical to the pre-migration state at every gate in this lineage | **PASS** |
| Exact WARN-vs-PASS divergence proven closed for the authorized pairs | `test_green_outcome_sensitivity_plural_now_closes_gap_like_singular` — real two-turn gap-closure state machine (`integrate_response`), plural-only and singular-only both reach `PASS` | **PASS** |
| Every §12/§13 test and probe passes | §12 A–H fully implemented (60 focused tests, all passing); §13 all 5 mutation probes re-run this lineage, all CAUGHT, probe 5 now behaviorally load-bearing (see §5 below) | **PASS** |
| Full suite green | `2677 passed / 3 skipped / 1 xfailed / 0 failed` | **PASS** |
| Independent review accepts the exact frozen SHA | Candidate `9399f9d` independently re-reviewed and accepted per the review record that authorized PR #497; the corrected test/probe evidence (§12.C naming, §12.D direction-correctness, §13 probe 5 behavioral proof) was the explicit subject of that acceptance | **PASS** |
| Owner accepts | Evidenced by the completed governed lifecycle: PR #497 merged (create-a-merge-commit, `b8e1274`), which per this repository's own established §14 lifecycle sequence (independent review → **Owner exact-SHA acceptance** → SHA-preserving publication → PR → pre-merge verification → merge → post-merge verification) requires Owner acceptance as the precondition immediately preceding publication/PR. This session did not independently witness a separate, distinguishable "Owner accepts" transcript event apart from the completed merge; the merge's existence is treated as the evidence of record, consistent with how every prior gate in this lineage (CF-2, P9-MECH-SF, the L2SC-01 contract gate) recorded Owner acceptance | **PASS** (evidenced by completed merge lifecycle) |

All in-scope §15 criteria are satisfied. The contract explicitly states it "does NOT claim the alias set is
linguistically complete — only that the authorized subset is safe" (§15) — closure here makes the identical,
narrower claim: the authorized 3-pair subset is implemented and proven safe, not that Mechanical plural-alias
coverage is exhaustive (the 12 excluded signals remain explicitly, permanently excluded absent a future,
separately-authorized, fresh alias-safety review).

## §4. MD-A / MD-1 closure evidence

**MD-A STATUS: FULLY CORRECTED.** Verified this gate directly against the merged test file (not assumed from a
prior report):
- All 12 rejected-alias adversarial sentences (`seal/verb`, `spring/verb`, `bearing/idiom`, `gear/idiom`,
  `lever/idiom`, `hydraulic/field-noun`, `pneumatic/field-noun`, `pressure/idiom`, `compression/idiom`,
  `friction/idiom`, `torque/rejected`, `mechanism/generic`) place the alias word in the clause the Layer-2 gate's
  directional-segment logic actually inspects — confirmed via direct calls to
  `engine.progression_loop._connective_whole_word_substance_gate` at both the correction gate and re-confirmed at
  this closure gate: `gate_base=False` (clean map) for all 12, `gate_poison=True` (map poisoned with exactly the
  rejected pair) for all 12.
- No independent `_CAUSAL_STRUCTURE_PATTERNS` substring confound and no other canonical substance word present in
  any of the 12 supporting clauses — verified programmatically.
- Three-way differential proof present and passing in the merged suite for all 12: clean map → `ASSERTED`;
  poisoned map with exactly the rejected pair → `REASONED`; neutral-control map with an unrelated alias →
  `ASSERTED`.
- Mutation probe 5 (inject `"seals": "seal"` into the real, live `domains/mechanical/domain.json`) is caught by a
  genuine behavioral guard — `test_red_mechanical_rejected_alias_never_grants_reasoned[seal/verb-The joint stays
  tight because the gasket seals the mating surface completely.]` — not merely by map-equality/inventory
  assertions (those additionally go RED too, but are no longer the sole protection).

## §5. Mutation/adversarial probe evidence summary (contract §13)

All 5 probes were re-run fresh during the MD-A correction gate (not merely reported from the original,
since-rejected `714d538` gate), each with `__pycache__` cleared before, byte-verified restoration after:

1. **Remove `pistons` alias** → `test_green_mechanical_approved_alias_parity[piston-pistons-...]` RED
   (`AssertionError: pistons`). CAUGHT. Restored, byte-identical.
2. **Bypass accessor, restore hardcoded-electronics-only map** → all 3 Mechanical parity cases RED. CAUGHT.
   Restored, byte-identical.
3. **Reintroduce generic `-s` suffix stripping** → **all 12** rejected-alias baseline tests went RED (versus only
   2 of 12 under the since-rejected `714d538` candidate — direct evidence the MD-A correction fixed the vacuous
   guards). CAUGHT. Restored, byte-identical.
4. **Point an alias at a nonexistent canonical signal** → real registry load fails closed at import time with the
   exact expected `RegistryLoadError`. CAUGHT. Restored, byte-identical.
5. **Inject `"seals": "seal"` into the authorized map** → CAUGHT via the genuine behavioral guard identified in
   §4 above, resolving the exact weakness MD-A identified. Restored, byte-identical.

This gate did not re-run any destructive mutation (per the closure gate's own instruction — closure evidence was
unambiguous from the correction gate's fresh re-run plus this gate's independent re-derivation of the direction-
correctness/confound-freedom proof in §4).

## §6. Architectural exit check

1. **Is Domain Registry still the canonical structural validator?** YES — `engine/domain_registry.py`'s
   `_validate_domain_v1()` is the sole validator; no second validator introduced.
2. **Is alias ownership pack-scoped?** YES — `substance_signal_plural_aliases` lives inside each domain pack's
   own `domain.json`, mirroring the existing top-level `aliases` (pack-id) precedent.
3. **Is the shared engine domain-neutral?** YES — `engine/progression_loop.py` retired its hardcoded electronics-
   only `_SUBSTANCE_PLURAL_ALIASES` map; it now reads whichever domain's own map via
   `get_substance_signal_plural_aliases(domain)`, with no domain-specific vocabulary remaining in the engine.
4. **Is there exactly one live alias source?** YES — confirmed via grep: the only place plural-alias data is
   defined is each pack's `substance_signal_plural_aliases` field; no parallel/shadow map exists anywhere in
   `engine/*.py`.
5. **Can future domain packs add explicit aliases without shared-engine vocabulary edits?** YES — any pack may
   add its own `substance_signal_plural_aliases` field; the engine requires no code change to consume it.
6. **Is there any automatic morphology?** NO — no suffix stripping, stemming, or derivation exists anywhere;
   confirmed structurally (code review) and behaviorally (mutation probe 3, §5 above).
7. **Is there any cross-domain leakage?** NO — `test_green_mechanical_alias_does_not_leak_into_electronics`,
   `test_green_electronics_alias_does_not_leak_into_mechanical`, and
   `test_green_mechanical_plural_does_not_match_as_electronics_substance` all pass; each pack's alias map is
   consulted only when `domain` equals that pack.
8. **Did the increment alter classifier/admission/activation behavior?** NO — `engine/domain_activation.py` is
   untouched by this lineage (confirmed: not present in any diff across the whole L2SC-01 lineage);
   `_ACTIVATED_DOMAINS` unchanged.
9. **Did it create any new duplicate registry/ownership seam?** NO — `substance_signal_plural_aliases` mirrors
   the existing `aliases` (pack-id) structural precedent exactly; no new parallel ownership concept introduced.
10. **Did hash-pin reconciliation weaken an existing freeze boundary?** NO — the MD-A correction gate required
    ZERO hash-pin reconciliation (runtime/data were byte-identical to the already-correctly-reconciled `714d538`
    pins); the original implementation gate's reconciliation (5 `tests/test_p9_mech_i*.py` files, limited to the
    4 intentionally-changed files' pins) was disclosed, scoped, and did not touch or weaken any other pack's or
    file's pin (`medical_device`, `software`, `iot_electronics`, `engine/path_n_questions.py` all verified
    byte-unchanged throughout).

No material "yes" to an architecture defect. No STOP condition triggered.

## §7. Residual-obligation review

Searched all governance documents for: `L2SC-01`, `substance_signal_plural_aliases`, `plural alias`, `MD-A`,
`MD-1`, "Layer-2 scoring completeness", "remaining obligation", "pending", "residual", "deferred".

- **A. Required before L2SC-01 closure:** none found — every requirement traced in §3's matrix is satisfied.
- **B. Separate registered obligations outside L2SC-01 (unaffected by this closure):**
  - `L2SC-02` (whole-word substance-matcher multi-word-signal limitation) — remains registration-only, not
    implemented, not expanded. `INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md`'s `L2SC-02` section is untouched by
    this closure (confirmed: will not be edited by this candidate).
  - **Tier-1 EN/AR Mechanical public label** — separate, next roadmap item (§9 below).
  - **L10N-RH-01** — separate reassessment gate, still pending.
  - **Explicit Owner Mechanical activation authorization** — never implied by this closure; Mechanical remains
    `NOT ACTIVATED`.
- **C. Stale/superseded wording needing governance sync:** none found in the pre-existing repository requiring
  correction beyond this closure's own additive entries. The live "Active contract" section of `ACTIVE_INCREMENT_
  CONTRACT.md` and the latest entries in `ACTIVE_EXECUTION_ROADMAP.md`/`CURRENT_PROJECT_STATE.md` already
  correctly state "`L2SC-01` remains OPEN" as of the MD-A correction gate — this closure candidate is precisely
  what transitions that status; no pre-existing document was found asserting L2SC-01 closed prematurely,
  `714d538` accepted, Mechanical activated, or Tier-1/L10N-RH-01 complete. Historical entries describing the
  state truthfully as of their own gate (e.g. the original implementation gate's "NOT formally closed by this
  candidate") are preserved unchanged, as required — they were true when written. **MD-C1 self-correction
  (disclosed):** the FIRST drafting of this closure record (candidate `360f541caa075a3fd899bfd41ee48304e965f491`,
  independently rejected) itself introduced exactly this class of defect — a stale-copied residual-list item
  claiming `CF-6`/`CF-2` remained live "OPEN" residuals, contradicting both the current authoritative status and
  this same record's own §9 closure statements. Corrected in §10 of THIS candidate; `360f541` preserved immutable
  rejected evidence at `refs/rejected/l2sc01-formal-closure-360f541`.

## §8. Scope separation (explicitly restated, not touched by this closure)

- **`L2SC-02`** remains registration-only / a separate obligation. NOT implemented here.
- **Tier-1 EN/AR** remains a separate next roadmap item. NOT implemented here.
- **`L10N-RH-01`** remains a separate reassessment gate. NOT performed here.
- **Mechanical activation** is NOT authorized by this closure. `L2SC-01` closure is a scoring-completeness
  implementation-lineage closure, not a domain-activation decision; it is one of several items in the
  activation-readiness sequence, not the sequence itself.

## §9. Closure statements (authoritative ONLY after this candidate's own merge + post-merge verification)

1. **The L2SC-01 runtime implementation is AUTHORITATIVE** (merge `b8e1274`; §1 fresh verification; §2 lineage).
2. **`L2SC-01` — Substance-Signal Plural-Alias Domain-Completeness — is FORMALLY CLOSED.** The frozen contract's
   §15 exit criteria (§3 above) are all satisfied; the MD-A defect is FULLY CORRECTED (§4); all 5 mutation probes
   are behaviorally CAUGHT (§5); the architecture exit check finds no defect (§6); no in-scope residual remains
   open (§7).
3. **The authorized alias set is exactly 3 of 15 Mechanical signals** (`piston`/`pistons`, `valve`/`valves`,
   `actuator`/`actuators`) — this closure does NOT claim linguistic completeness, only that this narrow,
   reviewed subset is safe and correctly implemented. The 12 excluded signals remain permanently excluded absent
   a future, separately-authorized, fresh alias-safety review.
4. **Electronics is preserved** — the 8 historical pairs, byte/behavior-identical, full suite green (2677/3/1/0).
5. **Rejected candidate `714d538fca7b22cb84e3b18802dcf27aa42e5707` remains immutable, rejected evidence** at
   `refs/rejected/l2sc01-runtime-impl-714d538` — never authoritative implementation, not erased, not amended.
   Rejected contract candidate `219f7c10c4ba23f795f0461dd831f71052469e65` likewise remains immutable at
   `refs/rejected/l2sc01-plural-alias-contract-219f7c1`.
6. **Mechanical remains NOT ACTIVATED**: `activated_domains() == ['electronics_electrical']`; no activation
   implied, granted, or advanced by this closure.
7. **`L2SC-02` remains registration-only** — unchanged, unexpanded, not touched by this closure.
8. **Tier-1 EN/AR and `L10N-RH-01` remain pending**, unimplemented, unreassessed.
9. **Phase 9 remains OPEN** — later roadmap obligations remain (§10 below).
10. **`OWNER_DECISION_REGISTER.md` is UNCHANGED** — no new Owner decision was required or made to close this
    already-accepted implementation.

## §10. Residual obligations after L2SC-01 closure (reconstructed from repository truth; none waived, combined, or executed here)

**MD-C1 correction (this candidate; independent-review rejection of closure candidate `360f541`):** the
originally-drafted version of this section stale-copied an older closure-record template's residual-list framing
that predated CF-2's and CF-6's own full-scope closures, and incorrectly listed a "CF-6 remainder — OPEN" item
and a "CF-2 remainder — the ILT-002 public-message question remains OPEN" item — directly contradicting this same
record's own §9 closure statements and every other section's correct restatement of the current, authoritative
status. **Authoritative status, verified this gate directly against the closure records of record:** `CF-6 =
FULLY DISCHARGED for its authoritative reconstructed scope` (`docs/governance/CF6_FULL_SCOPE_FORMAL_CLOSURE_
RECORD.md` §6); `CF-2 = FORMALLY CLOSED / FULLY DISCHARGED FOR ITS AUTHORITATIVE RECONSTRUCTED SCOPE`
(`docs/governance/CF2_FULL_SCOPE_FORMAL_CLOSURE_RECORD.md` §8), which explicitly resolved the ILT-002 route-copy
question as "RESOLVED, NOT A DEFECT" (§3.C) — superseding, without reopening or amending, `D-CF6CF2-ILT002-01`'s
earlier-recorded "CF-2 residual preserved, not discharged" framing (`OWNER_DECISION_REGISTER.md`), which remains
accurate ONLY as a historical statement of what was true at the time that decision was recorded, before the later
full-scope closure gates ran. Neither CF-2 nor CF-6 is a live residual obligation of any kind after L2SC-01
closure; both stand fully closed/discharged, unchanged and not reopened by this correction.

Before any Owner Mechanical activation authorization, all of the following remain outstanding (unaffected by this
closure, listed for continuity with the established qualification-record pattern):
1. **Tier-1 EN/AR Mechanical public label** — next roadmap item (§11 below).
2. **`L10N-RH-01`** reassessment — separate, pending.
3. **Explicit Owner Mechanical activation authorization** — never implied by qualification, family existence, or
   any prior or current closure.
Residuals with separate owners, unaffected: `L2SC-02`; D4 REGISTERED / NOT AUTHORIZED; D8 Owner-reserved; THERM-01
(future-only); Phase 10 / PSRR / deployment NOT AUTHORIZED; no P9 closure. `CF-2` and `CF-6` are NOT residuals —
both are fully closed/discharged (see correction note above).

## §11. Scope of THIS candidate and next gate

Governance/documentation only: this NEW closure record + `ACTIVE_EXECUTION_ROADMAP.md` (append-only) +
`ACTIVE_INCREMENT_CONTRACT.md` + `CURRENT_PROJECT_STATE.md` current-truth sync +
`INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md` `L2SC-01` entry closure note. **ZERO runtime/test/pack/registry/
activation/schema/persistence/ODR diff** (verified via `git diff --name-only` against base `b8e1274` — see the
governance-sync commit's own changed-path list). **Next required gate: Mandatory Grill on this exact candidate**,
then the governed lifecycle through Owner-side SHA-preserving publication, PR, and post-merge verification. After
this closure merges, the next roadmap item is the **Tier-1 EN/AR Mechanical public label** — not authorized or
performed here.
