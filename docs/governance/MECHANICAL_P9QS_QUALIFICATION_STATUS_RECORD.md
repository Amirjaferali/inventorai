# Mechanical P9-QS Qualification — Post-Activation Status Record (CORRECTED Candidate)

**Status of THIS record:** governance/documentation-only **STATUS RECORD CANDIDATE — MATERIAL CORRECTION** of
rejected candidate `c63724b3e7f8e5fa5e5ada8739f3d80f8319efb7`. It implements nothing, changes no
runtime/test/pack/registry/activation/schema/persistence file, and activates nothing further. Its determination
becomes authoritative ONLY if/when this exact candidate is merged (create-a-merge-commit) and post-merge verified.

**Correction of prior rejected candidate.** The immediately prior version of this record, candidate `c63724b`, was
independently **REJECTED** (verdict: MATERIAL CORRECTION REQUIRED). Two material defects were found, both
governance-truth only — the reviewer explicitly confirmed the substantive qualification determination itself was
correct:

- **MD-1 (ODR left stale/contradictory):** `OWNER_DECISION_REGISTER.md` row `D-P9-MECH-03` was left asserting
  Mechanical P9-QS qualification "remains a SEPARATE, still-unauthorized future gate" — contradicting this
  record's own determination. **Fixed:** a new row `D-P9-MECH-04` now clarifies `D-P9-MECH-03` (governance-truth
  correction, no new Owner authorization; `D-P9-MECH-03`'s own authorization scope is unchanged), and a
  non-destructive trailing note is appended to `D-P9-MECH-03`'s existing row text.
- **MD-2 (false source attribution):** the rejected candidate's §3 cited
  `MECHANICAL_ACTIVATION_EXECUTION_RECORD.md` §15 as the source of the stale "Mechanical NOT qualified" statement.
  Independently re-verified this gate: that file contains **zero** occurrences of "NOT qualified" or "separate
  future gate" anywhere; its §15 covers only activation/Tier-1/L10N-RH-01/Phase-9/Phase-10/third-domain
  boundaries, never qualification status. **Fixed:** §3 below cites the actual four locations where the stale
  claim exists.

The rejected candidate is preserved **immutable, unpushed, unamended** at
`refs/rejected/mechanical-p9qs-status-c63724b`.

## §1. Basis and fresh verification

Base: `5a1d2c15ad680b8b80304b51a3885fac42e32f56` (PR #503 — SHA-preserving merge of the accepted Mechanical
activation candidate `ca6575f6c71471dd2db146c4372b0374ca52d6fc` onto
`18a97da735e68763c7fab6488613cde1dff4675f`; merge tree `e6e270975c67eeb18f260c05350e7a6ea6e119bb` == candidate
tree; candidate→merge diff EMPTY; mandatory post-merge Mechanical activation verification already independently
PASSED as its own separate gate). Independently re-verified this gate (NOT from the rejected candidate — this
candidate starts fresh from the same authoritative parent): `git log -1 --format="%H %P %T"` confirms parents
`18a97da`+`ca6575f`; `origin/feature/atomic-json-session-persistence` confirmed at this exact tip; working tree
clean; no post-merge commit exists beyond the merge itself.

## §2. Primary determination — Outcome A: qualification already satisfied

**`MECHANICAL = P9-QS QUALIFIED`.** No runtime implementation is required. This record corrects the ODR (§3, via
`D-P9-MECH-04`) and the stale-text locations (§3), and documents the compliance matrix (§4) and residual quality
debts (§7), all governance-only.

## §3. Corrective disclosure — qualification-status contradiction found and resolved

Independently re-verified this gate, from fresh reads of the actually-merged files (not memory, and not carried
forward from the rejected candidate):

- `docs/governance/P9_MECH_QUALIFICATION_RECORD.md` (merged commit `dd7b487`, present at this tip) declares, in
  its own §3 Determination: **"`MECHANICAL = P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS`"** — every P9-MECH-QC
  qualification criterion (§5–§12, §15) evidence-proven with authoritative merged SHAs. Its §5 named exactly 6
  outstanding **activation** blockers (not qualification blockers): (1) the governed Mechanical safety-cue
  family, (2) the Tier-1 EN/AR public label, (3) CF-6, (4) CF-2, (5) NMF-1+FU-1, (6) explicit Owner activation
  authorization.
- `docs/governance/P9_MECH_SF_FORMAL_CLOSURE_RECORD.md` (merged commit `c25c843`, present at this tip) discharged
  blocker (1) and reaffirmed: **"the qualification status is unchanged in kind:
  `MECHANICAL = P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS; NOT ACTIVATED`"** — blocker set shrinks by one.
- Independently re-confirmed this gate that ALL SIX of those blockers are now separately, individually discharged
  and present in the current authoritative tip: (2) `TIER1_MECHANICAL_PUBLIC_LABEL_IMPLEMENTATION_RECORD.md`
  (merged, commit `e635c9f` present); (3) `CF6_FULL_SCOPE_FORMAL_CLOSURE_RECORD.md`:
  `"CF-6 = FULLY DISCHARGED FOR ITS AUTHORITATIVE SCOPE"`; (4) `CF2_FULL_SCOPE_FORMAL_CLOSURE_RECORD.md`:
  `"CF-2 = FORMALLY CLOSED / FULLY DISCHARGED..."`; (5) `CF5_NMF1_FU1_TEST_HARDENING_DISPOSITION_RECORD.md`:
  `"NMF-1 = DISCHARGED (executed). FU-1 = DISCHARGED (executed)."`; (6) `OWNER_DECISION_REGISTER.md`'s
  `D-P9-MECH-03`, executed, and `MECHANICAL_ACTIVATION_EXECUTION_RECORD.md` confirms live activation.

**Per P9-QS §2's own binding separations** (recognition ≠ qualification; qualification ≠ Owner authorization;
Owner authorization ≠ runtime activation), nothing in P9-QS or P9-MECH-QC states that activation reverses,
suspends, or un-does an already evidence-discharged qualification. The "WITH ACTIVATION BLOCKERS" qualifier
attached to the qualified state named exactly six items required before activation — all six are now discharged,
and activation has since occurred.

**Therefore, this record corrects a stale statement found in exactly four locations** (independently re-verified
by direct search this gate — NOT the rejected candidate's §15 attribution, which was false):
`docs/governance/ACTIVE_EXECUTION_ROADMAP.md` (its Mechanical-activation-gate entry's boundary/status line),
`docs/governance/ACTIVE_INCREMENT_CONTRACT.md` (its then-active-contract boundary/status line),
`docs/governance/CURRENT_PROJECT_STATE.md` (its Mechanical-activation entry), and — critically —
`docs/governance/OWNER_DECISION_REGISTER.md`'s own `D-P9-MECH-03` row, which itself asserted qualification
"remains a SEPARATE, still-unauthorized future gate." All four said, in substance: *"Mechanical NOT qualified
(P9-QS qualification remains a separate future gate)."* **This statement was factually incorrect at the time it
was written** — both `P9_MECH_QUALIFICATION_RECORD.md` and `P9_MECH_SF_FORMAL_CLOSURE_RECORD.md` were already
merged and authoritative before the Mechanical activation gate ran, and neither has ever been retracted or
superseded by any later document. The correct, evidence-backed statement — confirmed by this gate's own
independent compliance-matrix reconstruction (§4) and live verification (§5) — is: **Mechanical's qualification
work was already complete before activation; the "WITH ACTIVATION BLOCKERS" qualifier is now resolved because
every named blocker is discharged.** This is a CORRECTIVE DISCLOSURE, not a new qualification decision — no new
Owner authorization is implied, requested, or made by this correction. All four locations are corrected in this
candidate via annotation/append (preserving original historical text, per each file's own convention), plus a new
ODR row `D-P9-MECH-04` (§3 above; not a rewrite of `D-P9-MECH-03`'s original authorization scope).

## §4. Mechanical P9-QS compliance matrix (per P9-MECHANICAL_DOMAIN_QUALIFICATION_CONTRACT.md §5–§19)

| Req. | Subject | Status | Evidence |
|---|---|---|---|
| §5 | Capability Contract | **PASS — AUTHORITATIVE EVIDENCE EXISTS** | `P9_MECH_I1...CONTRACT.md` (merged); `capability_declaration` verified live this gate in `_REGISTRY["mechanical"]` (`known_unknowns` key present) |
| §6 | Real rule nuances | **PASS — AUTHORITATIVE EVIDENCE EXISTS** | `P9_MECH_I2...CONTRACT.md` (merged); `get_active_rules` byte pins, `tests/test_p9_mech_i2_rule_nuances.py` (17 passed, re-run this gate) |
| §7 | Coverage declaration | **PASS — AUTHORITATIVE EVIDENCE EXISTS + VERIFIED LIVE THIS GATE** | `coverage_declaration` keys `['covered_areas','known_limitations','not_covered_areas']` confirmed live in `_REGISTRY["mechanical"]` |
| §8 | Signal quality / AB-006 disposition | **PASS — AUTHORITATIVE EVIDENCE EXISTS** | `P9_MECH_I3...CONTRACT.md` (merged); `tests/test_p9_mech_i3_signal_quality.py` (18 passed, re-run this gate) |
| §9 | Cross-domain boundary testing | **PASS — AUTHORITATIVE EVIDENCE EXISTS + VERIFIED LIVE THIS GATE** | `P9_MECH_I4_TERMINAL_BOUNDARY_CORPUS_CONTRACT.md` (merged, 20 tests re-run); live adversarial sweep this gate (§5) reproduces boundary classes against the REAL activated runtime, not just the corpus's own doubles |
| §10 | Electronics non-degradation | **PASS — VERIFIED LIVE THIS GATE** | Real electronics admission unaffected (§5); full suite unchanged from the activation gate's own baseline |
| §11 | Safety-cue family | **PASS — AUTHORITATIVE EVIDENCE EXISTS + VERIFIED LIVE THIS GATE** | `P9_MECH_SF_FORMAL_CLOSURE_RECORD.md` (merged); `has_governed_safety_cue_family("mechanical")` confirmed `True` live this gate |
| §12 | Path-N / question content | **PASS — AUTHORITATIVE EVIDENCE EXISTS + VERIFIED LIVE THIS GATE** | §12(a) `P9_MECH_I5...CONTRACT.md` (merged); §12(b) `D-GMPR-01-D-D3` confirmed `FULLY DISCHARGED`, unblocking §12(b); `get_served_question(..., domain="mechanical")` confirmed live this gate returning a real served question |
| §13 | Public label / localization | **PASS — AUTHORITATIVE EVIDENCE EXISTS + VERIFIED LIVE THIS GATE** | `TIER1_MECHANICAL_PUBLIC_LABEL_IMPLEMENTATION_RECORD.md` (merged); real EN+AR surface rendering re-verified live this gate through an actual admitted session (§5) |
| §14 | Output truthfulness | **PASS — AUTHORITATIVE EVIDENCE EXISTS** | Truthful capability-scope statements embedded in §5/§7 declarations; no overclaim vocabulary found in any live-rendered surface this gate |
| §15 | Full qualification evidence package (10 items) | **PASS — AUTHORITATIVE EVIDENCE EXISTS** | `P9_MECH_QUALIFICATION_RECORD.md` §2 — all 10 items DISCHARGED with exact merged SHAs per increment |
| §16 | Activation separation | **PASS — VERIFIED LIVE THIS GATE** | `activated_domains() == ['electronics_electrical', 'mechanical']` confirmed live; qualification and activation independently, correctly tracked as separate states throughout (§3) |
| §17 | Future-extensibility claim boundary | **NOT APPLICABLE — WITH AUTHORITY** | Explicitly scoped non-precedent-setting by every P9-MECH-I* contract; unaffected by this gate |
| §18 | D4 Amendment 01 boundary | **NOT APPLICABLE — WITH AUTHORITY** | D4 remains REGISTERED / NOT AUTHORIZED, unaffected; confirmed no D4/composition logic touched anywhere in this lineage |
| §19 | Verified latent-risk register | **PASS — AUTHORITATIVE EVIDENCE EXISTS** | Referenced and carried by `P9_MECH_QUALIFICATION_RECORD.md`; no new latent risk surfaced by this gate's adversarial sweep |

**Zero OPEN / zero BLOCKED criteria.**

## §5. Live post-activation runtime qualification (verified this gate, real production paths, not test-doubles)

Fresh `app.test_client()` instances against the authoritative merged tip, no monkeypatching:

- **Mechanical-only idea** confirmed as `mechanical` → 302, `state.domain == "mechanical"`.
- **Electronics-only idea** confirmed as `electronics_electrical` → 302, `state.domain == "electronics_electrical"` (non-degradation, §10).
- **True Electronics/Mechanical tie** (`classify_domain("circuit and hinge")`) → `AMBIGUOUS_TIE`, candidates
  `('electronics_electrical', 'mechanical')`, no selected domain; real `/start` dispatch on the same input → 200,
  no session (fail-closed, deterministic).
- **Classifier-miss / explicit D2 choice flow**: NONE-classified idea + `domain_choice=electronics_electrical` →
  302, correctly admitted.
- **Unsupported `medical_device` idea** → 200, refused, no session, no internal pack-id leak.
- **Unsupported `software` idea** → 200, refused, no session, no internal pack-id leak.
- **Wrong-domain confirmation** (Mechanical idea confirmed as electronics) → 200, re-prompted for the correct
  domain, never cross-labeled.
- **Malformed/unknown domain value** (`domain_confirm=banana_domain`) → 200, refused, no session.
- **Mechanical safety cue**: `has_governed_safety_cue_family("mechanical")` → `True`.
- **Cross-domain safety cue**: `has_governed_safety_cue_family("electronics_electrical")` → `True` (both governed,
  no leakage between families observed).
- **Mechanical Path-N**: `get_served_question("MECHANISM_COMPLETENESS", 0, domain="mechanical")` → a real served
  question object (not `None`).
- **Mechanical terminal/boundary spot-checks**: `"a purely mechanical hand crank winch with a pulley"` →
  `mechanical`; `"a replacement heart valve"` → `mechanical` (D3-D, real activated-tie resolution); `"an
  artificial heart valve implant"` → `medical_device` (not a tie; unaffected) — all match the P9_MECH_I4 terminal
  corpus's documented, activation-reconciled expectations.
- **Mechanical rule-nuance / capability-coverage**: `_REGISTRY["mechanical"]`'s `coverage_declaration` and
  `capability_declaration` confirmed present and correctly shaped live.
- **EN Tier-1 real surface**: `public_domain_label("mechanical")` → `{"en": "Mechanical-informed review", "ar":
  "مراجعة مستنيرة بمجال الميكانيكا"}`; confirmed rendering on a real admitted session page.
- **AR Tier-1 real surface**: confirmed rendering on a real admitted session page under `ui_lang=ar`, with the
  English string absent (no simultaneous EN+AR leakage).

**No false admission, no silent precedence, no cross-domain leakage, no overclaim, no unsafe fallback, no domain
mismatch, and no stale inactive-state assumption were found anywhere in this sweep.**

## §6. Test totals (per-file enumeration — fixes Reviewer O1's unreproducible-aggregate defect)

Focused (P9-MECH qualification/safety/boundary + activation + admission + Tier-1), re-run individually this gate:

| File | Passed |
|---|---|
| `tests/test_p9_mech_i1_capability_coverage_declaration.py` | 18 |
| `tests/test_p9_mech_i2_rule_nuances.py` | 17 |
| `tests/test_p9_mech_i3_signal_quality.py` | 18 |
| `tests/test_p9_mech_i4_boundary_corpus.py` | 20 |
| `tests/test_p9_mech_i5_question_sufficiency.py` | 16 |
| `tests/test_p9_mech_safety_cue_family.py` | 23 |
| `tests/test_p9e1_path_n_caller_domain_propagation.py` | 6 |
| `tests/test_p9e2_multi_activated_tie_precedence.py` | 20 |
| `tests/test_p9e2r_result_representation.py` | 19 |
| `tests/test_s5_i2_domain_activation.py` | 31 |
| `tests/test_web_app.py` | 47 |
| `tests/test_domain_gate_entry_ux.py` | 28 |
| `tests/test_p6_1_truthful_domain_labeling.py` | 32 |
| **Sum** | **295** |

Sum reproduces the previously-stated aggregate exactly, now individually traceable/reproducible per file. Full
governed suite: **2696 passed / 3 skipped / 1 xfailed / 0 failed** — matches the expected accepted-candidate
baseline exactly; no discrepancy to investigate.

## §7. Prior non-blocking debts — reclassified against actual P9-QS/P9-MECH-QC clauses

1. **`UI_B_START_024` dual-surface wording** — the content is truthful and reads correctly for both its roles
   (error paragraph + checkbox consent); `L10N_RH01_FORMAL_CLOSURE_RECORD.md` §4 already dispositioned this as a
   non-blocking architectural-shape observation, not a defect. No P9-QS/P9-MECH-QC clause makes shared-string
   architecture a qualification criterion. **NON-BLOCKING QUALITY DEBT.** Retained obligation only.
2. **Stale docstrings/comments** describing Mechanical as inactive or `AMBIGUOUS_TIE` as production-unreachable —
   found in `engine/domain_rules.py`'s `classify_domain` docstring, a comment header in
   `tests/test_p6_1_truthful_domain_labeling.py`, and `scripts/run_cli.py`'s module docstring + two inline
   comments. These are documentation-only; the underlying code branches are correctly reachable and correctly
   tested (confirmed live this gate, §5). No P9-QS clause requires comment/docstring truthfulness as a
   qualification acceptance criterion — §8's prohibitions concern runtime behavior (silent fallback, fabricated
   results), not prose. **NON-BLOCKING QUALITY DEBT — OUTSIDE P9-QS.** Recommended for correction at or before the
   Phase 9 Remaining-Obligation / Exit-Criteria Review (§8), not fixed here (would require touching
   `engine/`/`scripts/`/`tests/` files, out of scope for a governance-only gate with no qualification deficiency
   to justify it).
3. **Vacuous `test_mechanical_not_offered_in_start_domain_picker`** — confirmed this gate: `/start` is POST-only;
   `GET /start` returns 405 with Flask's generic error page, so the test's assertions pass regardless of real
   picker behavior. Real picker/admission coverage genuinely exists elsewhere via actual `/start` POSTs
   (`tests/test_web_app.py::test_mechanical_idea_confirmed_as_mechanical_is_admitted` and
   `::test_mechanical_idea_confirmed_as_electronics_is_reprompted_not_admitted`;
   `tests/test_domain_gate_entry_ux.py::test_mechanical_idea_now_correctly_admitted_via_own_confirmation` and
   `::test_hand_powered_mechanical_idea_now_correctly_admitted_via_own_confirmation`) — this is NOT a coverage
   hole; only this one specific test's own assertion is vacuous, and it currently asserts nothing meaningful about
   real picker behavior. **Reclassified per independent reviewer instruction: MUST FIX BEFORE P9 CLOSURE.** Still
   not a P9-QS qualification blocker under any identified clause (qualification itself is unaffected — real
   coverage exists via the tests named above), but this is now recorded as a **live Remaining-Obligation item**
   that MUST be carried into the Phase 9 Remaining-Obligation / Exit-Criteria Review (§8) and MUST NOT be silently
   dropped or left unaddressed at that review. **NOT fixed in this gate** — fixing the test itself is out of scope
   for a governance-only correction candidate (would require touching `tests/`).
4. **No single automated test chains real `/start` admission → real `/session/<sid>` render → Tier-1 EN and AR
   string assertions** for Mechanical (only test-doubles do this for AR/EN separately; a real-admission test
   exists but stops short of asserting the rendered label). The underlying capability is independently, separately
   automatically tested at both layers (resolver-level: `test_resolver_maps_mechanical_to_tier1_bilingual`;
   admission-level: the real-POST tests above) and was independently live-verified in both the activation gate and
   this gate (§5). P9-QS's evidence requirement (§6/§7) is satisfied by objective qualification evidence, which
   this live verification is; ongoing ONE-TEST end-to-end regression coverage is a hardening enhancement, not a
   qualification criterion. **NON-BLOCKING QUALITY DEBT — OUTSIDE P9-QS.**
5. **No CLI test asserts the real (unmonkeypatched) broadened banner** — all `run_cli()` broadened-activation
   coverage in `tests/test_cf5_f003_classifier_matching_semantics.py` uses the file's own `activate()` double to
   simulate the 2-domain state rather than relying on the real current baseline. The underlying CLI logic is
   generic/activation-derived (verified by code read, not electronics-specific), and the doubles accurately model
   the real state. **NON-BLOCKING QUALITY DEBT — OUTSIDE P9-QS.**

**None of items 1, 2, 4, 5 are P9-QS blockers or MUST-FIX-BEFORE-P9-CLOSURE obligations under any clause
identified in the P9-QS or P9-MECH-QC contracts; item 3 is a MUST-FIX-BEFORE-P9-CLOSURE Remaining-Obligation item
(test-hygiene, not a qualification blocker).** All five are retained as tracking items for consideration at the
Phase 9 Remaining-Obligation / Exit-Criteria Review (§8) — consistent with how every prior phase's own
pre-closure review (Phase 7 §25, Phase 8, D3) has historically classified and carried forward this class of item.

## §8. Exact ordered next-gate sequence (verified from repository convention, not assumed)

The CF-2 closure gate's own roadmap entry named the sequence ending "...Mechanical activation + verification;
Phase 9 formal closure" — both of the named preceding items are now complete. This repository's own established,
repeatedly-applied convention for every other phase closure (Phase 7 §25 "Remaining-Obligation / Exit-Criteria
Review", Phase 8's own Remaining-Obligation / Closure-Eligibility Review, D3's "FORMAL CLOSURE + Remaining-
Obligation Review") requires a dedicated, read-only pre-closure review before any formal phase closure. No
document exempts Phase 9 from this convention. Verified exact ordered sequence:

1. **Mechanical P9-QS qualification — COMPLETE** (this record confirms; no new work required).
2. **Phase 9 Remaining-Obligation / Exit-Criteria Review** — NOT started; NOT performed by this record; a
   separate, Owner-authorized, read-only gate (following the Phase 7/Phase 8/D3 precedent) that would classify
   the §7 quality debts above (including the item-3 MUST-FIX-BEFORE-P9-CLOSURE reclassification) plus any other
   outstanding items before closure eligibility can be determined.
3. **Phase 9 formal closure** — ONLY if the Remaining-Obligation / Exit-Criteria Review returns an eligible
   verdict. NOT authorized, NOT performed, NOT implied by this record.

## §9. Boundary statements

1. **`MECHANICAL = P9-QS QUALIFIED`** — corrected from the stale "NOT qualified" statement found in the four
   locations named in §3; no new qualification work performed, no new Owner authorization implied.
2. **Mechanical remains ACTIVE**: `activated_domains() == ['electronics_electrical', 'mechanical']`, verified
   live this gate.
3. **Zero P9-QS blockers found.** Five non-blocking quality-debt items retained (§7); item 3 is additionally
   flagged MUST FIX BEFORE P9 CLOSURE (a Remaining-Obligation item, not a qualification blocker).
4. **Phase 9 remains OPEN.**
5. **Phase 10 / PSRR / deployment remain NOT AUTHORIZED.**
6. **No third domain activated or implied.**
7. **`OWNER_DECISION_REGISTER.md` — one new row `D-P9-MECH-04`** (governance-truth clarification of
   `D-P9-MECH-03`; Impl. authority NONE; no new Owner authorization event) plus a non-destructive trailing
   annotation on `D-P9-MECH-03`'s existing row. `D-P9-MECH-03`'s own original authorization scope and text are
   otherwise unchanged.
8. **Exact next gate: Phase 9 Remaining-Obligation / Exit-Criteria Review** — not performed here, not authorized
   by this record.

## §10. Scope of THIS candidate

Governance/documentation only: this rewritten status record + `OWNER_DECISION_REGISTER.md` (new row
`D-P9-MECH-04` + non-destructive annotation on `D-P9-MECH-03`) + `ACTIVE_EXECUTION_ROADMAP.md` (append-only
corrective note) + `ACTIVE_INCREMENT_CONTRACT.md` (active-contract section replaced per this file's own
convention) + `CURRENT_PROJECT_STATE.md` (corrective note inserted near the original stale text, not overwriting
it). **ZERO runtime/test/pack/registry/activation/schema/persistence diff.** Next required gate: Mandatory Grill
on this exact candidate, then the governed lifecycle. After this merges, the next eligible step is the **Phase 9
Remaining-Obligation / Exit-Criteria Review** — not authorized or performed here.
