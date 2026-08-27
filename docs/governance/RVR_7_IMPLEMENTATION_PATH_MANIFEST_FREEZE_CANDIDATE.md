# RVR-7 — Implementation Path Manifest Freeze — CANDIDATE

**Status:** `CANDIDATE — awaiting Independent Review and Owner exact-SHA acceptance.`
This document **AUTHORIZES NOTHING** by itself. It becomes part of the authoritative RVR-7
lineage only through the complete high-assurance lifecycle (Independent Review → Owner
exact-SHA acceptance → merge → post-merge identity verification). Even once authoritative,
**RVR-7 implementation start remains NOT authorized**: the RVR-7 Contract Framework §H.3
sequencing rule 1 makes Path Manifest Freeze and Implementation START distinct gates that are
never the same decision and never the same candidate.

**`PATH MANIFEST AUTHORITATIVE/FROZEN: NO`** (this candidate proposes the freeze; adoption
alone confers it).
**`RVR-7 IMPLEMENTATION AUTHORIZED: NO`** · **`RVR-7 IMPLEMENTATION START AUTHORIZED: NO`**
**`W1-N2 DISCHARGED: NO`** · **`RVR-8 AUTHORIZED: NO`**
**`CAP-12 ACTIVATED: NO`** · **`CAP-13 ACTIVATED: NO`** · **`CAP-14 ACTIVATED: NO`** ·
**`CAP-18 ACTIVATED: NO`**

**Classification legend:** `[REPO]` verified in the tree at the base; `[OWNER-PREMISE]` an
Owner-ratified premise conveyed outside the repository, recorded as premise and never restated
as historical repository fact; `[DERIVED]` a conclusion derived from repository evidence;
`[PROPOSAL]` a term proposed by this candidate for freeze; `[FUTURE-REQ]` a requirement binding
on the future implementation candidate.

---

## §1. Authoritative base and lineage `[REPO]`

**Base:** `dad450bfb86cb96a29527a733a213897950c57ec` — verified live from Git at this gate as the
tip of `feature/atomic-json-session-persistence` (0 commits after it). **PR #587** — the
post-RVR-7-contract-framework governance synchronization; first parent
`b4a0d5fc076292a36385f9228d5a37eedf3a4da1` (PR #586 — the authoritative RVR-7 Contract Framework
merge); second parent `c832c8876e3634f1996bf1d5c947a150abf2a8dc` (the exact Owner-accepted
synchronization candidate); merge tree `eb26d034a1548ec4d56b1628c0b0af397ce74aaa`; EMPTY
candidate→merge diff; post-merge identity verified.

**Governing instrument:** `docs/governance/RVR_7_SUBSTANTIVE_ARABIC_PARITY_CONTRACT_CANDIDATE.md`
("the base contract"), authoritative via PR #586 (accepted candidate
`d95a610b393c61f8b134b3cb747606f944cfb67e`, merge tree
`e0d4cb5b44edb48ac867b45446b30e5163621d54`).

**Prerequisites satisfied `[DERIVED]`.** Base contract §H.3 lists the gate order. Its two
prerequisites for this gate are met: (a) the Contract Framework is authoritative (PR #586);
(b) **OD-W2-D-P6-18 is now decided** (§3 below), which §H.3 sequencing rule 5 and §S.1 require
before the manifest may be frozen. The separate Owner authorization of the §H.2 bounded
diagnostic / path-manifest discovery sub-step was issued and exercised; its read-only findings
are the evidence base of §5–§9 here.

---

## §2. Amendment mechanism — repository-native form `[DERIVED from repository precedent]`

**Selected mechanism: ADDITIVE AUTHORITATIVE SUPERSESSION DOCUMENT.**
The base contract file is **byte-unchanged** in this candidate.

Repository governance resolves amendments to already-authoritative instruments by additive
supersession, never by in-place rewriting of accepted history. Precedent `[REPO]`:

- `docs/governance/W2_B_RVR6A_CONTRACT_AMENDMENT_1_CANDIDATE.md` §1 states the rule explicitly —
  *"Repository governance precedent resolves amendments by additive supersession documents, never
  by in-place rewriting of accepted history"* — and applies it to the authoritative W2-B contract
  (PR #573) via an additive amendment (PR #575), with a §2 exact old → new supersession map.
- `CLAUDE.md` item 7: the owner-approved remediation plan v2 *"supersedes any earlier draft"*.
- `OWNER_PRODUCT_IDENTITY_CORRECTION.md` corrects earlier statements additively.
- Rejected candidates are preserved unamended as immutable evidence.
- The post-RVR-7-contract-framework synchronization (PR #587) recorded that *"the authoritative
  RVR-7 contract instrument itself is not rewritten (the RVR-6a / RVR-6b precedent for merged
  instruments)"*.

Form **A** (modifying the live authoritative contract instrument) is therefore **rejected as
non-native**: it would rewrite accepted history. Form **C** was searched for and none exists.

This candidate accordingly:

- is **ADDITIVE** — the base contract's historical lineage is preserved intact;
- **supersedes, upon authoritative adoption, exactly the base-contract clause portions listed in
  §4** — where this candidate and the base contract conflict, this candidate governs; where this
  candidate is silent, the base contract remains in force unchanged;
- follows the exact-SHA serialized lifecycle of base contract §H.3 and AHAEP §9/§17-§20.

**`AMENDMENT MECHANISM: ADDITIVE CLAUSE SUPERSESSION DOCUMENT`**
**`HISTORICAL CONTRACT PRESERVED: YES`**
**`BASE CONTRACT FILE BYTE-CHANGED IN THIS CANDIDATE: NO`**

---

## §3. Owner decisions recorded — exactly as issued, not expanded `[OWNER-PREMISE]`

### §3.1 — D-P6-18 display-rule supersession

**`D-P6-18 DISPLAY-RULE SUPERSESSION: BOUNDED`**
Scope: **`RVR-7 Path-N substantive journey`**. Arabic sessions receive the substantive journey
asks in Arabic.

The decision carries these boundaries verbatim, and this candidate expands none of them:
canonical state remains language-independent; persistence remains language-independent; replay
and determinism remain unchanged; **no runtime or machine translation**; **no parallel Arabic
question registry**.

The base contract §S presented outcomes (a) full supersession, (b) bounded supersession, (c) no
supersession, and expressly chose none. The Owner has selected **(b)**. The base contract's §S
status line `OWNER DECISION REQUIRED` is superseded by this record (§4).

### §3.2 — Q2

**`Q2: INCLUDE`** — the substantive exhaustion/reframe prompts belonging to the same journey are
inside the Arabic parity requirement. This satisfies the base contract §I item 6's conditional
("Conditionally, per §H Q2 and only if the frozen manifest includes it").

### §3.3 — Implementation architecture selected by repository evidence

**`RENDER-EDGE / IDENTITY-BASED RESOLUTION`** — **NOT** language-aware progression.
Frozen in full at §5.

### §3.4 — D-RVR7-1

**`D-RVR7-1: OPTION A — JOURNEY-COMPLETE`.** For the **currently activated domains** the RVR-7
Arabic substantive scope is exactly:

1. the existing **21** committed Path-N `question_id`s;
2. `_STALL_REFRAME`;
3. `_EXHAUSTED_EXIT_PROMPT`;
4. **reachable** Stage-3 generic substantive asks;
5. `INTAKE_QUESTION`;
6. `closing_q`.

**It does NOT absorb** — and nothing in this candidate may be read as absorbing — generated
substantive outputs; `next_development_step`; deliverables; Decision Snapshot generated content;
PDF / export generated output; CAP-12 / CAP-13 / CAP-14 / CAP-18; unrelated UI chrome; or
future-domain latent generic questions merely because they exist (§4.3).

---

## §4. Bounded §I.1 supersession — exact old → new

### §4.1 Supersession map

| Base-contract clause | Disposition under this candidate |
|---|---|
| **§I item 1** — "Adding committed Arabic question-variant content of equivalent meaning for the existing 21 `question_id`s, index-isomorphic to English (§G)." | **SUPERSEDED IN PART** by §4.2 below. The 21-id enumeration is no longer the complete substantive-journey content promise. The index-isomorphism requirement, the equivalent-meaning requirement and §G remain **IN FORCE UNCHANGED** for the 21 ids. |
| **§I item 6** — "Conditionally, per §H Q2 and only if the frozen manifest includes it: Arabic parity for the exhaustion/reframe prompts, with governed digest re-freeze and disclosed lineage." | **CONDITION SATISFIED AND RESOLVED**: Q2 = INCLUDE, and the manifest includes the exhaustion/reframe prompts. The clause's "**with governed digest re-freeze**" premise is **SUPERSEDED** by §5.D and §9: under the frozen Q2 shape B no `engine/progression_loop.py` digest re-freeze occurs. Disclosed lineage remains required. |
| **§H.1 Q1** — open question on variant-field shape and loader seam | **RESOLVED** by §5.B/§5.E and §6 (additive sibling field; `text` remains a `str`; the loader seam is the sole reader). |
| **§H.1 Q2** — open question on exhaustion/reframe scope, including its parenthetical that inclusion requires *"an `engine/progression_loop.py` touch and a governed digest re-freeze"* | **RESOLVED AND, as to the parenthetical, SUPERSEDED** by §5.D — the parenthetical was a stated expectation, not a proven repository constraint; shape B satisfies Q2 with that file byte-unchanged. |
| **§H.1 / §H.4** — `RVR-7 IMPLEMENTATION PATH MANIFEST: NOT YET FROZEN`; provisional path envelope "indicative only — NOT an allowlist" | **SUPERSEDED** by §6 upon authoritative adoption of this candidate. Until adoption both remain in force and the manifest remains unfrozen. |
| **§S** — "Status: `OWNER DECISION REQUIRED` — NOT DECIDED AT THIS FREEZE" | **SUPERSEDED** by §3.1: outcome (b) is selected. §S's outcome descriptions and §S.1 ordering rules remain in force as the historical record and as satisfied prerequisites. |
| **§L.2 / §L.2.1** acceptance, **§M** no-translation, **§J** forbidden scope and fences, **§N** stop conditions, **§T** evidence contract, **§K** Option-A anchors, **§O** W/M, **§P** MG-8, **§Q** OD-PDVG-12, **§R** RVR-8, **§E** W1-N1/N2/N3, **§F** precision boundary, **§G** sentinel model, **§V** provisional classification, **§W** self-invalidation | **IN FORCE UNCHANGED**, extended only where §5–§11 here add requirements. §H.3 sequencing rules 1–7 remain in force **verbatim**, including rule 6 (Lean LEVEL and review DEPTH re-derived after the manifest exists — performed at §13). |
| All other clauses | **IN FORCE UNCHANGED.** |

### §4.2 The new bounded content rule `[PROPOSAL]`

> **RVR-7 Arabic substantive content scope (currently activated domains).** RVR-7 delivers
> committed Arabic content of equivalent meaning for exactly the substantive asks a Path-N
> session can serve into its question slot, namely: (1) the 21 committed Path-N `question_id`s,
> index-isomorphic to English; (2) `_STALL_REFRAME`; (3) `_EXHAUSTED_EXIT_PROMPT`; (4) the
> generic Stage-3 substantive asks that are **reachable** in an activated domain; (5)
> `INTAKE_QUESTION`; (6) `closing_q`. Every such ask resolves through a **forward** identity →
> content path. No new `question_id` is minted; identities without a committed `question_id`
> (items 2, 3, 5, 6, and the positional generic asks of item 4) resolve through an explicit
> governed semantic identity, never through text matching.

This is a **bounded expansion** of the enumeration in base contract §I item 1. It expands the
**content set**; it expands neither the surface set nor the authorization set.

### §4.3 What the expansion explicitly does not reach `[PROPOSAL]`

- **Generated substantive outputs** — including `next_development_step`
  (`engine/idea_development_outputs.py`), whose capability owner is **Increment 3**
  (`INCREMENT_3_AUTHORITY_RULINGS.md` R-1..R-6 + `INCREMENT_3_IMPLEMENTATION_CONTRACT.md`) and
  which is consumed by both the session callout and deliverable section 12 `[REPO]`. Routed at
  §12; **not** RVR-7 runtime scope.
- **Deliverables**, Decision Snapshot generated content, PDF / export generated output.
- **CAP-12 / CAP-13 / CAP-14 / CAP-18** — no CAP is activated, referenced as an owner, or
  foreclosed. **No `DEFERRED MARKET/MANUFACTURING PRODUCT DIRECTION INTERSECTION DETECTED`**:
  the material-gap sweep encountered no CAP-12 / CAP-13 / CAP-18 / Commercial-Evidence /
  Manufacturing-Evidence / Decision-Snapshot-architecture / external-evidence surface.
- **Unrelated UI chrome** — the `PROGRESSING` / `STALLED` direction token and the raw engine
  `reason` provenance line stay outside RVR-7 as pre-existing D-P6-18 chrome matters.
- **Future-domain latent generic questions.** The generic Stage-2 variants
  (`engine/progression_loop.QUESTIONS`, 3 gap types × 3) are **UNREACHABLE** in both currently
  activated domains, because each activated domain's Path-N artifact covers all three Stage-2
  gaps `[REPO]`. They are **NOT activated** by D-RVR7-1 and remain with the existing
  future-domain-activation obligation. Reachability, not existence, is the test.

---

## §5. Architecture freeze `[PROPOSAL / FUTURE-REQ]`

### §5.A — Engine remains language-blind (BINDING FENCE)

No language parameter, argument, global, thread-local, environment read, or other language
signal may enter: `engine/progression_loop.py`; `get_question`; `get_display_question`; any
sentinel comparison; S1; S2; S3; W2-B trigger decision logic; or S4 eligibility logic.

Repository basis `[REPO]`: `grep -rn "ui_lang|lang" engine/` returns **zero** matches at this
base; the engine is language-agnostic today and this freeze preserves that property rather than
creating it.

Falsification evidence `[DERIVED]`: partial threading is not merely incomplete but actively
harmful — making `get_display_question` language-aware while `get_question` stays English flips
the S3 predicate `primary != baseline` from `False` to `True` at `iterations_open == 0`, firing
`TRIGGER_LAPSED_ACCEPTANCE` where it previously did not and overwriting the Arabic display with
an English candidate. The fence exists to make that class unreachable.

### §5.B — Render-edge resolution

The canonical engine decision remains English and language-independent. **After** the final
semantic identity is known:

```
canonical engine decision (EN)
  -> final semantic identity        (derived from canonical non-text state)
  -> EN/AR variant resolution       (forward: identity -> committed content)
  -> rendered substantive question
```

**No text → `question_id` reverse lookup.** Only forward identity → content resolution. This
preserves `ServedQuestion` D4.4 (*"`question_id` is NEVER … translated, fuzzy-matched, or
reverse-looked-up from `text`"*).

Permitted identity sources, all already present at the render edge `[REPO]`: `gap_type` from
`select_next_gap(state)` (`web/app.py:2468` — the same pure call `compute_serving_decision` makes
for `served_gap`, on the same state in the same render); `iterations_open`; `state.domain`;
`state.path`; `_w2b.question_override_source`; `_w2c.question_id`; and the public constants
`STALL_THRESHOLD` and `TRIGGER_*`.

Verification duty `[FUTURE-REQ]`: the implementation MUST verify each resolved identity forward
(identity → committed EN text, compared for equality against the engine's own English decision)
and fail closed to English on mismatch. Comparing an identity's English text to the engine's
English text is a forward verification, not a reverse lookup.

### §5.C — W2-C

`engine/intent_serving.w2c_served_question` already returns the full
`IntentServing(question_id, text, design_gap_id, adjusted)` `[REPO]`. The implementation MUST
preserve that `question_id` through the render edge instead of reducing it to `.text` at
`web/app.py:2549`. This is a local change at the consuming call site; **no return type changes
and `engine/intent_serving.py` is not modified**.

`RVR-7 CONTRACT FRAMEWORK: AUTHORITATIVE` alone is not implementation completion, and adoption
of this manifest freeze is not implementation completion either.

### §5.D — Q2 shape

**`Q2 SHAPE: B` (FROZEN).** The canonical English `_STALL_REFRAME` and `_EXHAUSTED_EXIT_PROMPT`
remain `engine/progression_loop.py` constants, byte-unchanged. Arabic display resolves from the
explicit semantic identity at the render-edge / catalogue layer. **`engine/progression_loop.py`
MUST NOT be touched for language.**

Shape B must cover, and the frozen evidence set proves it covers, all four routes:
S1-served stall/reframe; S1-served exhausted exit; W2-B `TRIGGER_COMPLETED_INTENT_SKIP`; W2-B
`TRIGGER_CRITICAL_UNRESOLVED` (whose candidate is `_STALL_REFRAME` when
`iterations_open == STALL_THRESHOLD`, else `_EXHAUSTED_EXIT_PROMPT` — the identical predicate,
recomputed forward).

Identity → catalogue-key resolution is **identity-keyed, never text-keyed**: an edit to an
English constant can therefore never silently drop its Arabic surface.

### §5.E — Mechanical artifact

`domains/mechanical/domain.json` remains **byte-identical**
(`901dd7188ddefda9cbe69a835cc64959c1d55debfe61b262d720abd904069e79`).

The mechanical Path-N artifact may gain the governed Arabic sibling field while preserving:
exact `question_id`; exact English `text` projection from the pack; exact order; exact entry
count (10); a **closed** allowed-key set; and English pack provenance.

The evidence invariant in `tests/test_dgmpr_d3_path_n_domain_neutral_service.py` may be updated
**only** to permit the explicitly governed Arabic field, and **only** in the following shape,
which weakens no English guarantee `[FUTURE-REQ]`:

- the `{question_id, text}` projection of every artifact entry equals the pack's
  `gap_type_mappings` projection **1:1** (English provenance — unchanged in strength);
- ids and order exact; entry count exactly 10;
- per-entry keys are a subset of the **closed** set `{question_id, text, text_ar}` — no other key
  is admissible.

Reconciliation of `DGMPR_D3_PATH_N_DOMAIN_NEUTRAL_SERVICE_CONTRACT.md` §3 `[DERIVED]`: that
section's "no new content authorship" clause governs the **English wording verdict** — it exists
so the mechanical questions cannot drift from the merged I5 W1–W6 wording at the projection
surface. An additive Arabic sibling under the same `question_id` cannot cause that drift, and the
rewritten invariant asserts the English projection byte-exactly. This reconciliation is recorded
here explicitly rather than assumed. **Neither the pack nor `get_domain_question` acquires any
Arabic content**, so no second Arabic content location and no duplicate content owner is created.

### §5.F — Cold load

No reconstruction schema change. No `ReconstructedReviewState` field change. **No
`RECONSTRUCTION_VERSION` bump** (currently `p4-2-level1-recon-v1`) — `engine_contract_version` is
persisted per project and `engine/session_reconstruction.py:229` fails closed to Level 0 on
mismatch, so a bump would demote every existing saved project.

The display identity is derived at the render seam from the existing reconstructed canonical
state. `reconstruct_readonly_state` already returns `(review, state)` from the **same single
replay** (`reconstruct_review_state` is literally `_reconstruct(...)[0]`) and is already imported
in `web/app.py:84` and already used at three call sites `[REPO]`. No new replay, no new
subsystem, and **no reverse lookup from reconstructed English text**.

---

## §6. Exact implementation path manifest — proposed for freeze `[PROPOSAL]`

Exact paths only. **No wildcard is frozen.**

| # | Exact path | Op | Reason | Digest/pin effect |
|---|---|---|---|---|
| 1 | `docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json` | MODIFY | Arabic variants for the 11 electronics ids under the same `question_id`s | byte-freeze re-freeze (§9) |
| 2 | `docs/governance/path_n_content_config/mechanical_path_n_questions.json` | MODIFY | Arabic variants for the 10 mechanical ids; governed sibling field per §5.E | no digest pin; structural invariants in path 7 |
| 3 | `engine/path_n_questions.py` | MODIFY | the sole lawful reader of the artifacts; additive optional variant field on `ServedQuestion`; `text` stays a `str` | pin re-freeze (§9) |
| 4 | `web/app.py` | MODIFY | the sole render edge: identity resolver (§5.B); preserve `_w2c.question_id` (§5.C); use `reconstruct_readonly_state` for the cold-load identity (§5.F); supply question language/direction to the template | none |
| 5 | `web/templates/session.html` | MODIFY | the substantive question element hardcodes `lang="en" dir="ltr"` (§10) | none |
| 6 | `web/ui_text.py` | MODIFY | identity-keyed Arabic entries for the non-`question_id` substantive identities (§5.D, §4.2 items 2–6) | none |
| 7 | `tests/test_dgmpr_d3_path_n_domain_neutral_service.py` | MODIFY | holds the electronics byte-freeze, the mechanical key-set assertion, the verbatim-pack-projection invariant and the module test-inventory lock | holds the electronics artifact digest; inventory lock (§9) |
| 8 | `tests/test_path_n_content_config_artifact.py` | MODIFY | Arabic-surface policy guards (§11); the module's own static no-runtime-dependency assertion must remain satisfied | none |
| 9 | `tests/test_p9_mech_i5_question_sufficiency.py` | MODIFY | holds the `engine/path_n_questions.py` pin — **that entry only** | one pin entry re-freeze (§9) |
| 10 | `tests/test_rvr7_arabic_content_parity.py` | ADD | content-level: AR completeness for every in-scope ask, EN byte-unchanged, closed key allowlist, no-parallel-registry, Arabic policy-guard mirror | none |
| 11 | `tests/test_rvr7_render_edge_resolution.py` | ADD | engine/seam-level: identity resolution, forward-only (no reverse lookup), EN selection unchanged, S1 timing, S2, S3 trigger sets, S4 eligibility, W2-B identity, W2-C identity preservation, deterministic replay, `RECONSTRUCTION_VERSION` unchanged | none |
| 12 | `tests/test_rvr7_web_arabic_serving.py` | ADD | Flask-level on the real served route: Arabic serving, question-element `lang`/`dir`, cold-load Arabic banner, mixed-language regression, missing-AR fail-closed, W1-N2 adversarial corpus | none |

```
FROZEN PATH COUNT: 12
MODIFY: 9      ADD: 3      DELETE: 0
```

### §6.1 Why three ADD paths, and why one file is insufficient `[DERIVED]`

The split is forced by existing repository discipline, not by preference:

1. **A static self-inspection forbids mixing surfaces.**
   `tests/test_path_n_content_config_artifact.py::test_no_runtime_or_domain_dependency` asserts on
   that module's own source that it does not import the web framework, read a domain pack, or
   reference session routes `[REPO]`. The repository therefore already enforces that content-guard
   modules stay import-free — a single combined RVR-7 module containing Flask-route evidence could
   not satisfy that discipline if the same pattern is followed, and following it is required for
   the Arabic guards added at path 8.
2. **A Flask test client is a different fixture surface** from pure-engine sentinel tests; the
   real-served-route evidence required by base contract §T item 10 ("real served-route / UI
   evidence, not unit stubs alone") cannot be produced without it.
3. **The governing convention is per-surface modules.** The directly analogous W2-C / RVR-6b work
   shipped four modules split by surface — `test_w2c_rvr6b_registry.py`, `..._serving.py`,
   `..._web.py`, `..._w1n3.py` `[REPO]`. Three is the smaller analogue, not an expansion.

Two files were considered (merging 11 and 12). Rejected: it would place Flask-client fixtures in
the module that owns the sentinel-parity evidence, making the engine-level evidence dependent on
the web fixture and weakening the §5.A fence's own proof.

**No convenience paths.** Every path in §6 has a concrete execution route to a user-visible RVR-7
requirement; governance and evidence-pack artifacts are deliberately **excluded** from the runtime
manifest and belong to a separate closure/status action.

---

## §7. Excluded and inspection-only paths `[PROPOSAL]`

**EXCLUDED from the implementation manifest** — absent new contradictory repository evidence:

| Path | Basis for exclusion |
|---|---|
| `engine/progression_loop.py` | §5.A fence + §5.D shape B; no language parameter required |
| `tests/test_p9_mech_i3_signal_quality.py` | pins only `engine/progression_loop.py` and `engine/domain_rules.py`, both untouched |
| `tests/test_p9_mech_i4_boundary_corpus.py` | same, plus the mechanical pack pin — pack untouched |
| `domains/mechanical/domain.json` | §5.E — pack stays byte-identical |
| `engine/session_reconstruction.py` | §5.F — no schema or version change |
| `engine/intent_serving.py` | §5.C — identity already returned; markers already EN/AR paired |
| `engine/question_intent_registry.py` | additive keys are invisible to `_extract_source_question_ids`, which reads only `question_id` |
| `docs/governance/path_n_content_config/electronics_electrical_question_intent_registry.json` | English audit prose, never displayed; `"language": "en"` stays truthful |
| `docs/governance/path_n_content_config/mechanical_question_intent_registry.json` | same |
| `tests/test_w2b_amc_consumers.py` | stores zero digests; recomputes the live one; needs no edit and must stay green |
| generated-output implementation files (incl. `engine/idea_development_outputs.py`) | §4.3; Increment-3 owned; routed at §12 |
| deliverable implementation files (`engine/deliverable_assembler.py`, `web/templates/deliverable.html`) | §4.3; existing owners |

**INSPECTION-ONLY is not implementation scope.** The inspection-only surfaces above are read to
prove invariants; none may be modified under this manifest.

**If any excluded path becomes necessary: STOP.** The implementation must halt and prove the
invalidation — naming the exact repository fact that falsifies the exclusion — before any manifest
expansion, which requires its own governed gate. Silent expansion invalidates the candidate
(§15).

---

## §8. Test and evidence freeze `[FUTURE-REQ]`

### BLOCKING

1. EN question selection byte-unchanged for every in-scope ask, both activated domains.
2. An AR variant exists for every in-scope substantive ask (§4.2 items 1–6).
3. The same `question_id` across EN and AR wherever an id exists; no id minted, renamed or split.
4. All **21** committed Path-N records complete in Arabic, mechanically enumerated.
5. Stage-3 reachable / `INTAKE_QUESTION` / `closing_q` Arabic completeness.
6. No parallel registry: exactly two Path-N artifacts; the domain→artifact mapping stays
   one-dimensional; WS10 D11 source/registry ID-set equality still holds.
7. Language reaches the render edge from the existing UI-language mechanism **only**; no second
   language-state source exists.
8. S1 exhaustion timing unchanged (same `iterations_open` in EN and AR).
9. S2 behaviour unchanged.
10. S3 trigger sets identical in EN and AR.
11. S4 reachability identical in EN and AR.
12. W2-B candidate identity unchanged for all three question-slot triggers.
13. W2-C `IntentServing.question_id` preserved through the render edge.
14. Q2 Arabic proven through **both** the S1 route and the W2-B route.
15. Cold-load Arabic question display with **no** reconstruction-schema change.
16. Persisted and canonical state language-independent (identical durable records and canonical
    hashes for identical inputs in EN and AR).
17. Deterministic replay parity.
18. `RECONSTRUCTION_VERSION` unchanged.
19. The question element carries the correct `lang` and `dir` for the language actually rendered.
20. Arabic early-gate-terminology guard.
21. Arabic R1-regression guard.
22. No silent missing-AR fallback for the RVR-7 required substantive set — a missing required AR
    entry is a test failure, never a silent English render.
23. **No reverse lookup**: a static assertion that the resolution path derives identity from
    canonical state and never from displayed text.

### EVIDENCE

24. Per-question EN ↔ AR semantic-equivalence review artifact covering every in-scope ask.
25. Human bilingual review (base contract §L.2.1) — not substitutable by automated checks.
26. W1-N1 verification discharge.
27. W1-N2 Arabic adversarial enumerated small-talk corpus **on the real served route**.
28. Mixed-language adversarial regression (language switch mid-session; cold load; W2-B override).
29. Universal Guardrail Smoke PASS.
30. The broader suite as determined by Lean §5B and the actual invalidation surface.

### OBSERVATION / CONDITIONAL EVIDENCE

31. `_INTENT_MARKERS` re-validation against the new Arabic question wording — the 21 Arabic marker
    sets were authored against English question wording.
32. **If** the markers change, the already-governed differential-evidence requirement (base
    contract §K.2 / the DOR Option-A anchor row) is invoked; it is not re-created here.

**`W1-N2 DISCHARGED: NO`.** This candidate claims no discharge of W1-N2, W1-N1, or any evidence
item above; it freezes what the future implementation must produce.

---

## §9. Pin / digest consequences — machine-derived at this base `[REPO]`

Complete pin table derived by scanning `tests/` for 64-hex digest bindings; every listed pin
matches its live artifact at this base.

| Pinned artifact | Live digest | Pin holders | Expected under this manifest |
|---|---|---|---|
| `docs/.../electronics_electrical_path_n_questions.json` | `399ce8b9a7f65f33b77d4f8a11d8e544f49133b27e2689c04c24fb7ef92efbfd` | `tests/test_dgmpr_d3_path_n_domain_neutral_service.py` (1) | **CHANGES** — re-freeze; `EXPECTED CONSEQUENCE OF AUTHORIZED RVR-7 SCOPE` |
| `engine/path_n_questions.py` | `a1a682d38293defd4b351e6238aeb870b4f765eaf3fc0f105c4932f75286ce7f` | `tests/test_p9_mech_i5_question_sufficiency.py` (1) | **CHANGES** — re-freeze that one entry; `EXPECTED CONSEQUENCE` |
| `engine/progression_loop.py` | `a7e8bd62b9ab76aaba5889ce52b5f32ee646b2817ba1c790ed7a231d259fa41f` | i3, i4, i5 (3) | **UNCHANGED** — any change is `UNAUTHORIZED SCOPE EXPANSION` |
| `engine/domain_rules.py` | `0e47326ad92a6e5b0a63eb06db9e3ad96ae72c9aaf64471dd21621265b1db1ab` | i3, i4, i5 (3) | **UNCHANGED** |
| `domains/mechanical/domain.json` | `901dd7188ddefda9cbe69a835cc64959c1d55debfe61b262d720abd904069e79` | i4, i5 (2) | **UNCHANGED** — any change is `UNAUTHORIZED SCOPE EXPANSION` |
| `domains/electronics_electrical/domain.json` | `53f431e38a70c2b621e19afb7323ad9bc4732c6c4151ea6b8c46a3214f098dfb` | i1, i2, i3, i4, i5 (5) | **UNCHANGED** |
| `docs/.../mechanical_path_n_questions.json` | (no digest pin) | — | structural invariants only (§5.E) |
| `RECONSTRUCTION_VERSION` | `p4-2-level1-recon-v1` | `engine/session_reconstruction.py` + consumers | **UNCHANGED** (§5.F) |
| Test-inventory lock (15 exact test names) | — | `tests/test_dgmpr_d3_path_n_domain_neutral_service.py` | **CHANGES** only if a test is added/renamed in that module; disclosure required; `EXPECTED CONSEQUENCE` |
| Meta-consistency test (stores zero digests) | — | `tests/test_w2b_amc_consumers.py` | **NO EDIT**; must stay green |

**`EXPECTED DIGEST CHANGES: 2`** (plus the conditional inventory lock).
**`EXPECTED PACK / PROGRESSION / DOMAIN-RULE / RECONSTRUCTION-VERSION CHANGES: 0`.**
Counts are machine-derived at this base, not inherited. The Q2 inclusion conceals no
digest-sensitive blast radius: under shape B the Q2 surfaces cost **zero** additional pins.

---

## §10. Session template — BLOCKING implementation requirement (M-13) `[REPO / FUTURE-REQ]`

`web/templates/session.html:261` renders the substantive question as:

```html
<p class="question" lang="en" dir="ltr">{{ question }}</p>
```

The element is hardcoded English / left-to-right. Rendering Arabic inside it would declare the
wrong language to assistive technology and apply the wrong bidirectional base direction, which
misplaces neutral characters (punctuation, digits, parentheses) at line boundaries.

**This is BLOCKING, not cosmetic.** The implementation MUST make the question element's `lang`
and `dir` match the language of the substantive question actually rendered. The repository
already contains the pattern to mirror: `session.html:355` renders
`lang="{{ current_uncertainty_guidance.lang }}" dir="{{ current_uncertainty_guidance.dir }}"`,
and `web/ui_text.direction(lang)` already exists `[REPO]`.

Related non-blocking truth defect, correctable during the same authorized touch: the comments at
`session.html:112` and `:352` and at `deliverable.html:169` state that the shell is
`<html lang="en">`, which `base.html:2` (`<html lang="{{ ui_lang }}">` with `dir="rtl"`)
contradicts. Pre-D-P6-18 wording; **OBSERVATION**, not blocking.

---

## §11. Arabic policy guards (M-5) `[REPO / FUTURE-REQ]`

`tests/test_path_n_content_config_artifact.py` enforces two content policies against
`q["text"]` using **English word-boundary regexes only**: `test_no_disallowed_terms`
(10 disallowed early-gate terms) and `test_r1_regression_markers_absent` (5 R1 markers) `[REPO]`.

Arabic content added under this manifest would receive **no** equivalent protection: an Arabic
rendering of a disallowed early-gate term would pass today's guards silently.

**The future implementation MUST include BLOCKING Arabic-surface enforcement** equivalent in
strength to the English guards, for both activated domains. This finding is now known and
represented in the frozen evidence plan (§8 items 20–21); it blocks Implementation START
completion and its evidence, and it does not block this freeze.

---

## §12. Increment-3 generated-output language obligation — routing `[DERIVED]`

`next_development_step.{title, why_it_matters, next_action}` renders raw English on the session
page and is consumed identically by deliverable section 12 `[REPO]`. Its **capability owner is
Increment 3**; **no language-obligation owner exists** for it at this base.

It is **NOT RVR-7 runtime scope** (§4.3) and is **not** force-fitted into RVR-7. It is registered
as its own row in `DEFERRED_OBLIGATIONS_REGISTER.md` §3 by this candidate, discoverable through
the normal obligation route, with the capability owner unchanged, the language obligation OPEN,
blocking level **NBF**, and an explicit return event and closure evidence. The registration
creates **no implementation authorization** and no generated-output implementation is performed
or authorized here. Orphan count remains defensible: the item has a named capability owner and a
named return route, so it adds nothing to the register's §6 unowned-items table.

---

## §13. Lean risk LEVEL and review DEPTH — re-derived, not inherited `[DERIVED]`

Base contract §H.3 sequencing rule 6 requires re-derivation once the manifest exists. Performed
here; the base contract's own §V classification is expressly provisional and is not carried.

**`LEAN RISK LEVEL: 1`** · **`REVIEW DEPTH: 1`**

Justification. Lean §3 LEVEL 1 enumerates **architecture** among its triggers. This candidate
freezes an implementation architecture (§5.A–§5.F) and **supersedes in part a clause of an
authoritative merged contract** (§4). Either fact alone reaches LEVEL 1. The competing reading —
Lean §3 LEVEL 2 lists "Arabic/RTL" — describes *implementing* Arabic/RTL inside an already
approved contract; it does not describe freezing an architecture or amending a contract boundary,
and where the readings compete the higher requirement is taken. **Requirements are never lowered
by this derivation.**

LEVEL 1 requires separate explicit Owner authorization **and** independent review. Both are
already mandated for this gate by base contract §H.3 sequencing rules 2 and 3, so the
classification adds no new obligation and removes none. AHAEP execution mode is a **non-risk
axis** and may never lower these requirements.

**Independent Review is REQUIRED before Owner exact-SHA acceptance.**

---

## §14. Status fences (binding wording rules)

```
PATH MANIFEST FREEZE CANDIDATE CREATED:      YES
PATH MANIFEST AUTHORITATIVE/FROZEN:          NO
RVR-7 IMPLEMENTATION AUTHORIZED:             NO
RVR-7 IMPLEMENTATION START AUTHORIZED:       NO
W1-N2 DISCHARGED:                            NO
RVR-8 AUTHORIZED:                            NO
CAP-12 ACTIVATED:                            NO
CAP-13 ACTIVATED:                            NO
CAP-14 ACTIVATED:                            NO
CAP-18 ACTIVATED:                            NO
DEPLOYMENT / PRODUCTION / SERIOUS RELEASE:   NOT AUTHORIZED
LANGUAGE-CONDITIONAL ROUTING:                FORBIDDEN
RUNTIME / MACHINE TRANSLATION:               FORBIDDEN
PARALLEL ARABIC QUESTION REGISTRY:           FORBIDDEN
```

No statement in this document, and no statement in any document synchronized with it, may be
read as authorizing implementation. The manifest becomes authoritative only on Owner exact-SHA
acceptance, merge, and post-merge identity verification of **this exact candidate**; adoption of
the manifest authorizes the manifest, never the implementation, which remains a separate Owner
decision under §H.3 sequencing rules 1 and 4.

---

## §15. Self-invalidation

This candidate is invalid on its face, and must not be accepted, if any of the following is true:

1. the authoritative base has advanced beyond `dad450bf…` without re-derivation;
2. it modifies any runtime, test, content, pack, or pin file (`EXECUTABLE / TEST / PIN / PACK /
   DOMAIN-RULE / CONTENT DELTA` must be **0**);
3. it rewrites the base contract file or any other accepted historical instrument;
4. it is read as authorizing implementation, Implementation START, RVR-8, or any CAP;
5. it freezes a wildcard path instead of exact paths;
6. it claims freeze authority before Owner acceptance, merge and post-merge verification;
7. it expands the manifest beyond §6 without a governed gate;
8. it claims W1-N2, W1-N1, or any §8 evidence item is discharged.
