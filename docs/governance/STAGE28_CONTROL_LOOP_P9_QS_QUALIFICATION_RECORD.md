# Stage 28 — Bounded Control-Loop Concept Owner — P9-QS Qualification Record (Qualification Slice 2)

> **MANDATORY ANNOTATION (prominent; no unannotated "QUALIFIED" claim exists or is permitted):** the qualification
> recorded below is **`control_loop: P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS; NOT ACTIVATED`** — the repository's
> existing P9-QS qualification phrase, as first recorded for Mechanical (`P9_MECH_QUALIFICATION_RECORD.md`).
> **No governed control-loop safety-cue family exists** (Owner Option (b), §6): safety determination stays NOT COVERED,
> and whether such a family is needed is an OUTSTANDING ACTIVATION-TIME Owner decision. All activation blockers are
> listed in §7. **`control_loop` remains NOT ACTIVATED:** `activated_domains() == ['electronics_electrical',
> 'mechanical']`, `support_state("control_loop") == "recognized_not_activated"`, and Stage 30 is required before any
> future activation.

`STAGE 28 — BOUNDED CONTROL-LOOP CONCEPT OWNER — QUALIFICATION SLICE 2: DELIVERED` ·
`control_loop: P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS; NOT ACTIVATED` ·
`CONTROL-LOOP OWNER: P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS` · `CONTROL-LOOP OWNER: NOT ACTIVATED` ·
`STAGE 28: ENTERED / PARTIAL — CONTROL-LOOP OWNER QUALIFIED, NOT ACTIVATED` ·
`STAGE 30 REQUIRED BEFORE ANY FUTURE ACTIVATION` · `QUALIFIED ≠ ACTIVATED`

**Status of THIS record.** Documents-only qualification record and declaration, written under the Owner's
authorization of Stage 28 — Bounded Control-Loop Concept Owner — Qualification Slice 2 (qualification record +
declaration) and nothing else. It is the qualification evidence package required by the Owner-accepted contract
[`STAGE28_BOUNDED_CONTROL_LOOP_CONCEPT_OWNER_QUALIFICATION_CONTRACT.md`](STAGE28_BOUNDED_CONTROL_LOOP_CONCEPT_OWNER_QUALIFICATION_CONTRACT.md)
§10 item 7 (P9-QS §7), following the Mechanical qualification-record precedent. The declaration it carries is
authoritative as merged; Git / GitHub own its PR, merge and review identity. It changes no runtime code, test
behaviour, Domain Pack, provenance record, registry, classifier, activation allowlist, composition, safety-cue code,
public-label owner, Path-N artifact, schema or persistence. **No evidence was regenerated:** every determination
below rests on the merged Slice-1 evidence at the exact identities of §1. `OWNER_DECISION_REGISTER.md` is unchanged
(P9-QS §2: qualification ≠ Owner authorization ≠ activation).

## §1. Evidence identity (authoritative merged lineage)

| Item | Identity |
|---|---|
| Contract candidate | `9f0d2b9fa991f3179f2da3eed66fcd57fc7eba81` |
| Contract merge — Owner-accepted basis (`QUALIFICATION CONTRACT: OWNER-ACCEPTED`) | `540db53613013baf071515cfdb2e3fdec7e7a4cb` (PR #735; parents `89ad1ceb801572704a321d60fd486b11b6caa88e` / `9f0d2b9fa991f3179f2da3eed66fcd57fc7eba81`) |
| Accepted contract blob | `f4b4f1f779d8f6f794bf6d56ea2a6040a6403ef1` |
| Slice-1 implementation | `8cae30649cf617b3f33726683fe4c0163fe4a15d` — hosted CI run `36943761165` (all required jobs green) |
| Reviewed final head (Correction 01) | `42882ee17aeab22b51a236545eba0c2672bfcff9` — hosted CI run `36949299714` (all required jobs green) |
| Authoritative Slice-1 merge | `1d282f0e8915284418935fb1090cf4d493c7ba3f` (PR #736; parents `540db53613013baf071515cfdb2e3fdec7e7a4cb` / `42882ee17aeab22b51a236545eba0c2672bfcff9`) |
| Merge tree | `1e77f04cd7f52fd61318efd8d1c2b1ffa93182ad` (identical to the reviewed final-head tree) |
| `domains/control_loop/domain.json` | blob `8f3406343f3ee7742d834c12d72bc1c4ccc09dda` |
| `domains/domain_provenance.json` | blob `07cc8eb381a981b1f2820147c62d2e0bef28f008` (`control_loop:PR001`–`PR007`) |
| `tests/test_stage28_control_loop_qualification_slice1.py` | blob `39ead26fefe37dc69910ba080086da00e28c741b` (identical at `8cae306` and at the merge) |

The three evidence blobs are byte-identical at the implementation commit, the reviewed final head and the
authoritative merge. This qualification is a qualification of exactly that pack blob and provenance blob.

## §2. Qualification obligation matrix (every obligation mapped to exact merged evidence)

"Slice-1 test" means `tests/test_stage28_control_loop_qualification_slice1.py` at blob `39ead26f…`; "the pack" means
`domains/control_loop/domain.json` at blob `8f340634…`; "provenance" means `domains/domain_provenance.json` at blob
`07cc8eb3…`.

| # | Obligation (contract §10 / P9-QS) | Merged evidence | Status |
|---|---|---|---|
| 1 | Page-level binding of every §3 claim family (§10.1) | `control_loop:PR001` — DOE-HDBK-1013/2-92 IC-07, handbook pages 4–6 (automatic-control functions and elements; comparison; feedback; open / closed loop) and pages 7–10 (Control Loop Diagrams: controlled system, control elements, feedback elements, reference / setpoint, controlled output, actuating / error signal, manipulated variable, disturbance) — families 1–6. `control_loop:PR003` — NASA TM-101739 §1.2.2, printed page 1-3 / PDF page 16 — family 7. `control_loop:PR005` — NIST SP 811 §8.1, page 23 (second; hertz) — family 8. `control_loop:PR007` — governance record — family 9. Every signal, question, nuance and the capability declaration carries a provenance reference that resolves to its own pack-scoped record (Slice-1 test: `test_every_pack_reference_resolves_to_its_own_provenance_record`) | DISCHARGED |
| 2 | DOE / NASA / NIST source-use records (§10.2, §7) | `control_loop:PR002` (DOE Web Policies ↔ PR001), `control_loop:PR004` (NASA STI terms ↔ PR003; NTRS metadata "Work of the US Gov. Public Use Permitted"), `control_loop:PR006` (NIST Technical Series statement ↔ PR005); paraphrase-only limits in the pack's `_governance_notes.source_use_limitations`; seven records, all pack-scoped, earlier records unchanged (`test_provenance_records_are_pack_scoped_and_bounded`) | DISCHARGED |
| 3 | Coverage declaration (§10.3) | `coverage_declaration`: 10 covered areas (the nine §3 families plus gap detection for the two governed gap types), exactly 22 not-covered areas (the 21 §4 items plus the controller's action / update rate), 8 known limitations; exact-list check and 7 widening mutations rejected (`test_declared_scope_holds_exactly`, `test_scope_check_rejects_each_widening`) | DISCHARGED |
| 4 | Capability declaration (§10.3; P9-QS §4) | `capability_declaration`: supported categories limited to concept-level completeness, concept-level boundary differentiation and governed question service; supported gap types `MECHANISM_COMPLETENESS`, `BOUNDARY_AMBIGUITY`; 12 unsupported categories opening with the safety NOT-COVERED statement; evidence expectations; two known unknowns; provenance `control_loop:PR007`; unsupported-expertise wording rejected from everything the pack covers, asks or examines (`_scope_problems`) | DISCHARGED |
| 5 | Classification / signal-conflict review (§10.4) | Six classification signals only (`setpoint`, `set point`, `closed loop`, `open loop`, `control loop`, `manipulated variable`), disjoint from every Electronics and Mechanical classification / substance signal (`test_classification_signals_are_the_minimal_control_loop_set`); the §10.4 words (`microcontroller`, `controls`, `calculates`, `samples`, `threshold`, `filter`, `actuator`) and the generic words `control`, `loop`, `feedback` excluded (`_EXCLUDED_SIGNALS`); dispositions recorded in `_governance_notes.signal_conflict_dispositions` (the six terms hit 3 strings and changed 0 outcomes; the generic words would have hit 105 and changed 82); a load-bearing probe proves generic signals would change outcomes (`test_generic_signals_would_change_the_test_suite_vocabulary`); existing tie policy used, no classifier change | DISCHARGED |
| 6 | Cross-domain boundary evidence (§10.5; P9-QS §6) | See §3 below: positive, negative, ambiguous / tie, known-unknown, recognition-vs-activation, regression and safety boundary classes, each with its merged Slice-1 test | DISCHARGED |
| 7 | Electronics non-degradation (§10.5; P9-QS §7-B) | Electronics examples classify unchanged (`test_electronics_and_mechanical_examples_are_unchanged`); before / after registration differential over the governed classification corpora (`test_governed_classification_corpora_are_unchanged_by_registration`; 284 texts at the recorded Slice-1 run) and over every string literal in the test suite plus the replay-case inputs (`test_the_whole_test_suite_vocabulary_is_unchanged_by_registration`; 11,622 texts at the recorded Slice-1 run): 0 changed outcomes; `_ACTIVATED_DOMAINS` and `COMPOSITION_DOMAINS` unchanged (`test_control_loop_is_recognized_but_not_activated`); hosted CI green on runs `36943761165` and `36949299714` | DISCHARGED |
| 8 | Mechanical non-degradation (§10.5; P9-QS §7-B) | The same differentials, examples and hosted CI runs; the Mechanical I1–I4 evidence suites changed only by adding `control_loop` to their registry-membership pins (`8cae306`) | DISCHARGED |
| 9 | Qualification-grade rule nuances (P9-QS §4; Mechanical I2 precedent) | `control_loop:RN001` (`MECHANISM_COMPLETENESS`, layer 1, provenance `control_loop:PR001`) and `control_loop:RN002` (`BOUNDARY_AMBIGUITY`, layer 2, provenance `control_loop:PR007`), full shape, `active_gap_rule_marker`, "at concept level only" (`test_rule_nuances_have_the_qualification_grade_shape`); read only through `get_active_rules` | DISCHARGED |
| 10 | Authorized gap / question scope (§3; ADR-002) | `MECHANISM_COMPLETENESS` Q1–Q7 and `BOUNDARY_AMBIGUITY` Q1–Q3 only, ordered and identified (`test_questions_are_ordered_and_identified_per_gap`); `get_active_rules("control_loop") == [MECHANISM_COMPLETENESS, BOUNDARY_AMBIGUITY]` and no `PHYSICAL_FEASIBILITY` question (`test_only_the_two_authorized_gap_types_are_active`); universal gap identifiers reused with their ADR-002 meaning; `_governance_notes.physical_feasibility_absent` | DISCHARGED |
| 11 | Safety-cue Owner decision — Option (b) | `has_governed_safety_cue_family("control_loop") is False`; capability statement "Safety determination of any kind is NOT COVERED: no governed control-loop safety-cue family exists …"; known limitation "No safety determination"; `_governance_notes.safety_cue_option_b` (`test_no_safety_cue_family_no_runtime_label_and_no_path_n_artifact`, `test_capability_declaration_carries_the_option_b_safety_statement`); see §6 | DISCHARGED for qualification |
| 12 | Truthful public label / localization (§10.6) | Runtime truth: no Tier-1 entry, the neutral Tier-0 fallback resolves for `control_loop`, and the `/start` refusal never names the pack (`test_no_safety_cue_family_no_runtime_label_and_no_path_n_artifact`, `test_recognized_not_activated_refusal_stays_truthful`). Qualification requirement: approved truthful EN / AR label text recorded in this record (§5); the runtime label is an activation-readiness blocker (Mechanical precedent) | DISCHARGED (record text; runtime label deferred) |
| 13 | P9-QS §7 evidence package (§10.7) | THIS record: dual proof (A) works within its declared scope — §3 positive / boundary classes and the declarations of items 3–4; (B) no material degradation of the activated domains — items 7–8; provenance (items 1–2); deterministic behaviour (the classifier and accessors are deterministic; every Slice-1 assertion is exact); web / CLI consistency: no web or CLI file changed in Slice 1 or Slice 2 and the governing admission surface is the existing activation-derived `/start` refusal — not applicable with reason (Mechanical record item 8 precedent) | DISCHARGED |
| 14 | Exact merged evidence SHAs | §1 | DISCHARGED |

## §3. P9-QS §6 boundary classes

| Boundary class | Merged evidence (Slice-1 test) |
|---|---|
| Positive representative cases | Two control-loop descriptions classify `SINGLE control_loop` (`test_control_loop_examples_recognize_the_pack`); the governed questions are served for the two authorized gap types (`test_only_the_two_authorized_gap_types_are_active`). A full session journey is unreachable while the domain is not activated; activated-service verification is an activation blocker (§7) |
| Negative / out-of-domain | "A customer feedback loop for my bakery", "A remote control toy car", "A loop of rope that holds a bundle", "the controls monitor and adjust the output" and a signal-free text score 0 for `control_loop` (`test_negative_examples_are_not_captured`) |
| Ambiguous-domain | A tie with an activated domain resolves to the activated domain (D3-D) ("A sensor reports when the setpoint is reached" → Electronics); a tie with only a non-activated domain fails closed as `unresolved_non_activated_tie` with the complete candidate set ("A setpoint algorithm" → `control_loop`, `software`) (`test_ties_stay_governed`) |
| Known-unknown | `capability_declaration.known_unknowns` (whether the loop holds its target cannot be established in software; observation-rate adequacy is not determined); the known limitation "what cannot be established in software remains an explicit unknown"; question Q7 invites "If you do not know yet, say so"; in-session known-unknown handling stays with the existing shared record / decision owners (activation verification, §7) |
| Recognition vs activation | `support_state` `recognized_not_activated`, `is_activated` False, allowlist unchanged (`test_control_loop_is_recognized_but_not_activated`); `/start` refuses for every confirm value (none, Electronics, Mechanical, `control_loop`), creates no session and never names the pack (`test_recognized_not_activated_refusal_stays_truthful`) |
| Regression against activated domains | Differentials and examples of §2 items 7–8: 0 changed outcomes; hosted CI green |
| Domain-specific safety behaviour | Option (b): no family, safety NOT COVERED, stated truthfully (§2 item 11; §6) |

## §4. Determination and bounded qualified scope

Every qualification obligation of contract §10 (items 1–7) and of the post-Slice-1 eligibility check (items 1–14) is
evidenced by authoritative merged identities, and P9-QS §7's dual proof holds. This record therefore declares:

> **`control_loop: P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS; NOT ACTIVATED`** (see the header annotation, §6 and §7).

Qualification is declared ONLY relative to the truthful declared scope already implemented (P9-QS §3) — concept level
only:

- concept-level control-loop completeness (a quantity kept at, or within a range around, a target; open vs closed loop);
- feedback relationship;
- measured-value / reference (setpoint) comparison;
- conceptual control action (the concept only, never a control law);
- controlled-element relationship (controlled element, manipulated variable, controlled output);
- disturbance;
- measurement observation-rate concept (how often the measured value is observed — not the controller's own rate);
- shared time / frequency unit discipline (second; hertz), mapped shared knowledge, not re-owned;
- explicit limits, abstention and specialist boundary;
- gap types `MECHANISM_COMPLETENESS` and `BOUNDARY_AMBIGUITY` only.

**Not claimed — each stays NOT COVERED:** `PHYSICAL_FEASIBILITY`; stability; tuning; PID; real-time execution
(scheduling, deadlines, jitter); firmware implementation or embedded execution architecture; safety determination
(including fail-safe, SIL / ASIL and regulatory compliance); the adequacy of the controller's action / update rate;
engineering validation of any kind (project-specific calculation, physical / mechanical / electrical response);
system-level Robotics capability (contract §11: not a Robotics Domain Pack). Everything in the pack's
`coverage_declaration.not_covered_areas` and `capability_declaration.unsupported_categories` stays NOT COVERED.

## §5. Label / localization (record text only — runtime label deferred to activation readiness)

`QUALIFICATION RECORD TEXT ONLY — RUNTIME LABEL DEFERRED TO ACTIVATION READINESS`

Proposed truthful Tier-1 public label text, recorded here only:

| Locale | Proposed Tier-1 label |
|---|---|
| EN | Control-loop concept review |
| AR | مراجعة مفاهيمية لحلقة التحكم |

- Bounded to the qualified concept-level scope: it implies no embedded execution, no Robotics, no engineering
  certification and no physical feasibility; Tier 0–1 wording only (no "Specialist", "Expert", "Professional",
  "Certified" or "Licensed").
- `web/domain_label.py` `_PUBLIC_DOMAIN_LABELS` is NOT modified: the runtime keeps resolving `control_loop` to the
  neutral Tier-0 fallback ("General idea review" / "مراجعة عامة للفكرة") until a separately authorized
  activation-readiness step adds the label in that existing owner, with selected-UI-language rendering (one locale at
  a time; no automatic switching), as for Mechanical (P9-MECH contract §13).

## §6. Safety — Owner Option (b)

Qualification completes with an empty control-loop safety-cue family plus the truthful capability-scope statement:

- **no control-loop safety-cue family exists** (`has_governed_safety_cue_family("control_loop") is False`);
- **safety determination remains NOT COVERED** (capability declaration, first unsupported category; known limitation
  "No safety determination");
- **inventor-stated hazards remain the inventor's own unvalidated statements;**
- no SIL / ASIL, certification or regulatory-compliance claim;
- **a separate activation-time Owner decision remains required** on whether (1) a governed control-loop safety-cue
  family is required, or (2) the existing Mechanical / Electronics safety-cue coverage is sufficient.

No safety cue is created by this record.

## §7. OUTSTANDING ACTIVATION BLOCKERS (distinct from qualification; none resolved or waived here)

Before any activation of `control_loop`, ALL of the following remain outstanding:

1. **Stage 30 safeguards** — cross-domain safeguards before any new-domain activation (`STAGE 30 REQUIRED BEFORE ANY
   FUTURE ACTIVATION`).
2. **Activation-time safety-cue Owner decision** (§6: a governed control-loop family, or sufficiency of the existing
   Mechanical / Electronics coverage), and its implementation and evidence if a family is required.
3. **Runtime Tier-1 EN / AR public label** in the existing `_PUBLIC_DOMAIN_LABELS` owner (§5).
4. **Path-N / non-specialist service review** — whether activated service requires a Path-N content artifact for
   `control_loop`, and that artifact if it does.
5. **CF-6 / CF-2 applicability checks** — both lanes are formally closed for their recorded scope
   (`CF6_FULL_SCOPE_FORMAL_CLOSURE_RECORD.md`, `CF2_FULL_SCOPE_FORMAL_CLOSURE_RECORD.md`); confirm that web / CLI
   pre-classifier consistency and public-message truthfulness hold for an additional activated domain, reopening
   neither lane unless a defect is found.
6. **Root-domain versus optional-part activation semantics** — whether `control_loop` may become a project's root
   analysis focus, an OPTIONAL third composable part of an integrated invention (contract §9; `COMPOSITION_DOMAINS`
   unchanged until a separate Stage-15 composition slice), or both.
7. **PHYSICAL_FEASIBILITY progression implications** — verify that progression, readiness, report and next-step
   surfaces stay truthful for an activated domain with no `PHYSICAL_FEASIBILITY` gap (no implied feasibility verdict).
8. **Activation-specific classification / admission verification** required by the existing controls — activated
   admission, session service and question journeys for `control_loop`, and the D3-D tie behaviour once it becomes an
   activated domain.
9. **Exact Owner activation authorization** — the existing explicit allowlist in `engine/domain_activation.py`;
   never implied by qualification.

## §8. Recorded limitations and observations (non-blocking)

- **Recall is bounded by six classification phrases.** A control-loop description that uses none of them is not
  recognized as `control_loop`; this is the deliberate result of the signal-conflict review (§2 item 5), not a defect.
- **Concept level only.** The pack is not suitable for controller design, detailed engineering or production-ready
  systems (pack known limitation).
- **Pack lifecycle sentence.** The pack's Slice-1 known limitation "Registered for qualification only: not activated
  and not declared qualified; …" was true at its recorded commit. This record supersedes its "not declared qualified"
  clause as to qualification state; its "not activated" clause stays true. The pack is deliberately unchanged because
  this qualification is a qualification of exactly blob `8f340634…`; the sentence is reconciled at the next separately
  authorized pack change.
- **Source identification.** The NASA and NIST page pins were identified by Lead-level independent source inspection
  (executor egress to those hosts was blocked); `control_loop:PR001` and `PR005` carry no URL. Exact source identity
  suffices here; complete URL fields at the next natural provenance touch if the authoritative URL is known and
  verified.

## §9. What qualification does NOT mean (P9-QS §2 — binding)

Qualification ≠ Owner authorization ≠ activation ≠ composition authority. This record activates nothing, changes no
admission behaviour, adds no user-facing capability, adds no runtime label, safety cue or Path-N artifact, and changes
no Stage-15 composition. Stage 28 stays ENTERED / PARTIAL and NOT complete (its checkbox stays unticked); Stage 30 is
NOT started; Robotics, IoT and Drone / Unmanned stay unimplemented and unauthorized; deployment and release stay NOT
AUTHORIZED.
