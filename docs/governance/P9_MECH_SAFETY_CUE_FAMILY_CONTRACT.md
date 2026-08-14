# P9-MECH-SF — Governed Mechanical Safety-Cue Family (OD-M2 Clause 3) — Bounded Implementation CONTRACT (governance-only contract gate — CORRECTED candidate)

**Status of THIS record:** governance/documentation-only **CONTRACT CANDIDATE** for the FIRST activation-blocker gate
recorded by the authoritative Mechanical qualification record: the OD-M2 clause-3 governed Mechanical safety-cue
family (D-P9-MECH-02: "REQUIRED and MUST be complete, merged, and post-merge verified BEFORE any Owner activation
authorization for `mechanical`"). It becomes AUTHORITATIVE only through the governed lifecycle (Mandatory Grill →
independent external exact-candidate review → Owner acceptance → SHA-preserving publication → PR →
create-a-merge-commit → post-merge verification). **It implements nothing in this gate**; once authoritative it
authorizes ONLY the bounded implementation defined below (itself requiring separate explicit Owner authorization).
It does NOT activate Mechanical, does NOT touch the other activation blockers, and records NO new Owner decision
(**`OWNER_DECISION_REGISTER.md` UNCHANGED** — OD-M2/D-P9-MECH-02 already requires this family; this contract
implements the recorded decision). **DOCUMENTED NO-VALID-RED — GOVERNANCE-ONLY CONTRACT GATE.**

**Candidate lineage:** the first contract candidate `cfab650fedbbaa4d5fa60db4bea1fa84575aae62` was independently
REJECTED (sole material defect: its §4 flip inventory claimed exhaustiveness while missing the CERTAIN I5 full-pack
hash flip — `tests/test_p9_mech_i5_question_sufficiency.py::test_pack_bytes_frozen_incl_i4_validity_anchor` — and
omitted that file from the permitted reconciliation set, so a compliant implementation would have hit the
contract's own extra-flip STOP) and is preserved as immutable rejected evidence. THIS corrected candidate is
created from the SAME authoritative parent and corrects exactly that enumeration (plus the reviewer's non-blocking
precision clarifications); every other architectural finding of the rejected candidate is preserved in substance.

## §1. Authoritative base and blocker-dependency reconstruction

Base: `cac658d70b841772b1a496b60b65a2da4309814a` (SHA-preserving merge of the accepted qualification record
`dd7b4878` onto `ac8ac2d9`; merge tree `178c5dbb` == candidate tree; POST-MERGE PASS; freshly fetched; 0 newer;
clean tree) — **`MECHANICAL = P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS; NOT ACTIVATED`** is authoritative.

**Blocker dependency graph (reconstructed; the five non-Owner blockers are mutually INDEPENDENT — none technically
requires another):**
- **(1) OD-M2 clause-3 safety-cue family — THIS lane, FIRST.** The only Mechanical-lane engineering-content blocker;
  the qualification record itself names it "first among them"; fully specified by D-P9-MECH-02 (F001 seam;
  provenance-tagged hazard vocabulary; focused/negative/mutation evidence; electronics non-degradation). Depends on
  nothing among (2)–(5).
- **(2) Tier-1 EN/AR label — LAST of the technical blockers** (P9-MECH-QC §13: the label becomes truthful only at
  activation-readiness; implementing it earlier would label an unserved domain — it naturally couples to the eventual
  activation-readiness/activation gate). No dependency on (1), but correctly sequenced after it.
- **(3) CF-6 and (4) CF-2 — separate shared-surface lanes** with their own registered owners; NO technical dependency
  on Mechanical activation readiness (they are Web/CLI consistency/truthfulness debts required before
  second-specialist-domain activation generally). They share one facet (the CLI electronics-pinned copy/literal), so
  a future CLI gate may discharge facets of both (the F002 facet-discharge precedent) — but they are NOT combined
  with this lane and NOT combined with each other by this contract.
- **(5) NMF-1/FU-1 — bounded test-only carry-forwards**; their registered earliest gates are "a bounded standalone
  test-only hardening gate or the pre-activation readiness review". **Required disposition: record their execution or
  explicit accepted-risk disposition NO LATER than the pre-activation readiness review preceding Owner activation
  authorization** — independent of this lane; not absorbed.
- **(6) Explicit Owner activation authorization — always last; Owner-only.**
**Hidden-prerequisite sweep:** none found beyond the recorded six — per-domain P9-QS is QUALIFIED; D-GMPR-01-D-D3 is
FULLY DISCHARGED; D8 is not implicated (`mechanical` is not IoT); pack lifecycle `status` is not activation; the
§5-I2 allowlist edit IS the activation gate itself. **Therefore the smallest dependency-correct next gate is THIS
contract** — governance-only now (H: the contract gate), with the implementation gate implementation-bearing.

## §2. The bounded implementation increment — exact definition

```
INCREMENT CONTRACT — P9-MECH-SF Governed Mechanical Safety-Cue Family   [implementation NOT started]
Responsibility:   (a) ADD the governed `mechanical` entry to `_DOMAIN_CUE_FAMILIES` in engine/safety_signal.py —
                  the EXISTING F001 per-domain seam (family shape EXACTLY mirrors the electronics precedent:
                  owner / failure / subject / consequence / context_terms), backed by NEW provenance-tagged
                  Mechanical hazard vocabulary module constants. Vocabulary authorship IS in scope (OD-M2 clause 3
                  requires it) under §3's objective criteria — nothing else in the module changes: the derivation
                  logic, the electronics family and its constants, and the legacy None-default remain byte-frozen
                  in behavior (electronics-derivation byte-parity proven).
                  (b) TRUTHFULNESS CASCADE (mandatory, same increment): update the mechanical pack's
                  capability/coverage declarations so the "inventor-stated safety-signal derivation NOT COVERED
                  pending a governed Mechanical safety-cue family" statements (OD-M2 clause 1) are replaced by a
                  truthful covered statement (inventor-stated safety-SIGNAL derivation only — detection-scoped,
                  requires independent validation, NOT a safety determination; limitations preserved). Leaving the
                  NOT-COVERED statement after the family merges would be untruthful; deferring it to a second gate
                  would leave an untruthful interim state — both unacceptable, hence one increment.
                  (c) NEW focused evidence file tests/test_p9_mech_safety_cue_family.py.
                  (d) additive provenance record (e.g. mechanical:PR005) in the existing manifest for the authored
                  vocabulary and the declaration update.
                  (e) the ENUMERATED reconciliations of §4 ONLY, restricted to the §4 permitted-file list.
Allowed paths:    engine/safety_signal.py (additive family entry + its vocabulary constants ONLY);
                  domains/mechanical/domain.json (declaration safety-statements ONLY — signals/gap types/nuances/
                  aliases byte-frozen); domains/domain_provenance.json (additive record only);
                  NEW tests/test_p9_mech_safety_cue_family.py; the §4 PERMITTED RECONCILIATION FILES (exact list
                  in §4 — nothing else); closure-time governance sync only.
Forbidden paths:  every other engine file (progression_loop, domain_rules, path_n_questions, deliverable_assembler
                  — the S15 statement change for mechanical is AUTOMATIC via has_governed_safety_cue_family and
                  needs no assembler edit), web/**, scripts/**, all other packs and the electronics Path-N
                  artifact, every other existing test beyond §4, schemas/, OWNER_DECISION_REGISTER.md, CI.
                  FORBIDDEN OUTCOMES: any electronics derivation delta; any activation state change; any admission
                  change; any label work; any CF-6/CF-2 work; any second safety framework or family shape.
```

## §3. Vocabulary authorship — objective criteria (no unsupported expertise; no policy invention)

The authored Mechanical hazard vocabulary MUST be: (1) mechanical-hazard-relevant (drawn from recognized mechanical
hazard classes — e.g. crush/pinch/shear/entanglement points, stored-energy release (springs/pressure), fracture/
ejection of parts, rotating-part entrapment — final inventory decided at implementation under these criteria);
(2) lay-accessible (inventor-stated phrasing, mirroring the electronics family's register); (3) detection-scoped
ONLY — cues mark inventor-STATED safety-relevant statements for REQUIRED-INDEPENDENT-VALIDATION labeling, never a
safety determination (the F001 semantics, unchanged); (4) provenance-tagged (the additive manifest record names the
hazard-class basis and this contract); (5) equality-pinned in the evidence file (the proven anti-drift/anti-stuffing
pattern) with every cue class non-empty; (6) free of electronics vocabulary (no cross-family collision that could
relabel electronics content); (7) truthful in scope statements (the updated declaration says signal DETECTION is
covered — not analysis, not assessment, not THERM-01 territory: no thermal-analysis implication).
**(8) I1 lexicon-guard compatibility (explicit reminder for implementation authors):** the new covered declaration
wording MUST also satisfy the EXISTING I1 forbidden-covered lexicon guard
(`tests/test_p9_mech_i1_capability_coverage_declaration.py::test_no_forbidden_expertise_in_covered_content`,
`_FORBIDDEN_IN_COVERED`) — i.e. it must avoid unsupported-expertise terms including `thermal`, `certif…`,
`simulation`, `tolerance stack`, `fea`/`finite element`, `fatigue`, `gd&t`, `regulatory`, `manufactur…`,
`stress analysis`, `physical testing`, `supply chain`, and `cost` — and must keep the declaration key shape
(`covered_areas` / `known_limitations` / `not_covered_areas`) unchanged. That guard is a CONSTRAINT that keeps
passing, not a flip; "safety determination" remains in the NOT-COVERED concepts (detection is covered; determination
never is).

## §4. EXPECTED RECONCILIATIONS — enumerated EXHAUSTIVELY (the D-GMPR-D3-PN lesson; anything beyond = STOP — CONTRACT AMENDMENT)

**Certain — family-presence flips (6):**
1. `tests/test_p9_mech_i1_capability_coverage_declaration.py::test_safety_family_remains_absent_for_mechanical`
   (False pin + the derive-()-on-stub assertion) → re-pinned to the governed-present state with disclosure;
2. `tests/test_p9_mech_i2_rule_nuances.py::test_safety_family_remains_absent_for_mechanical` → same;
3. `tests/test_p9_mech_i3_signal_quality.py::test_safety_family_remains_absent_for_mechanical` → same;
4. `tests/test_p9_mech_i4_boundary_corpus.py::test_mechanical_safety_family_remains_absent` → same;
5. `tests/test_cf5_f001_safety_signal_domain_seam.py::test_green_capability_query` (mechanical in the False loop)
   → mechanical moves to the True set; the electronics/None True pins and the other-domain False pins unchanged;
6. `tests/test_cf5_f001_safety_signal_domain_seam.py::test_red_r1_family_less_domain_gets_truthful_scope_statement`
   — **CERTAIN, not conditional** (reviewer-precision): it uses `mechanical` as THE family-less example, so once
   the family exists its `capability_scope == "no_governed_safety_cue_family"` / truthful-empty-statement
   assertions fail REGARDLESS of vocabulary. Minimal reconciliation: switch the example to a still-family-less
   domain (`software`/`medical_device`), disclosed, preserving the pin's load-bearing truth (family-less domains
   get the truthful scope statement). NOTE: the OTHER S15 capability_scope pin (the medical/software/unknown loop
   in `test_green_family_less_domain_never_crashes_or_stamps_electronics`) does NOT use mechanical and does NOT
   flip.
**Certain — declaration-truthfulness flips (5 surfaces):**
7. I1 declaration content pins (the OD-M2 statement pins in coverage AND capability; the
   `_MANDATORY_NOT_COVERED_CONCEPTS` entry for safety-signal derivation; the exact covered/supported equality pins
   when the covered statement is added) → re-pinned to the updated truthful declaration with disclosure;
8. `tests/test_p9_mech_i2_rule_nuances.py` `_FROZEN_MECH_FIELDS` capability/coverage hashes → re-frozen;
9. `tests/test_p9_mech_i3_signal_quality.py` `_FROZEN_MECH_FIELDS` capability/coverage hashes → re-frozen;
10. `tests/test_p9_mech_i4_boundary_corpus.py` mechanical full-pack sha256 (the I4 corpus validity anchor) →
    re-frozen WITH the mandatory proof that the classification/substance SIGNAL INVENTORY is byte-unchanged (the
    corpus's own validity terms: declaration-only pack change ⇒ NO corpus re-build; the anchor hash update is
    disclosed);
11. `tests/test_p9_mech_i5_question_sufficiency.py::test_pack_bytes_frozen_incl_i4_validity_anchor` — **the
    correction this candidate exists for:** the I5 evidence file ALSO byte-pins the entire mechanical pack
    (`_FROZEN_PACK_SHA256["mechanical"]`), so the declaration cascade CERTAINLY flips it. Its mechanical pack hash
    is re-frozen using the SAME explicit signal-inventory-unchanged proof as item 10 (one proof covers both
    anchors), disclosed in-file; NO corpus rebuild is required unless the ACTUAL signal inventory changes (it does
    not — declarations are not signals). The I5 file's engine hashes, other-pack hashes, question-inventory pins,
    and test inventory are UNTOUCHED.
**Conditional — vocabulary-dependent derive-() pins (4 — implementation must verify and disclose each; all are
protected by the §3(6) no-collision rule and the fail-closed flip sweep):**
12. `tests/test_d3_core_domain_neutrality.py::test_d3a_non_electronics_domain_context_not_forced_electronics`
    (derive == () for a mechanical-domain state whose trigger text is electronics-flavored) — flips ONLY if the
    authored vocabulary matches that trigger text; the LOAD-BEARING D3-A invariant (never electronics-labeled)
    MUST be preserved either way;
13. `tests/test_cf5_f001_safety_signal_domain_seam.py::test_red_r2_no_unconditional_electronics_cue_exposure`
    (derive == () for mechanical + electronics hazard text) — flips ONLY on an electronics-vocabulary collision,
    which §3(6) forbids; if the pin is kept it becomes a standing collision guard;
14. the MECHANICAL branch of
    `tests/test_cf5_f001_safety_signal_domain_seam.py::test_green_family_less_domain_never_crashes_or_stamps_electronics`
    (derive == () for mechanical over "", "plain words", and the two electronics texts) — flips ONLY if the
    authored vocabulary matches those texts; the medical/software/unknown branch (incl. its S15 capability_scope
    pin) is unaffected; a disclosed minimal example-domain swap is permitted if the test's family-less premise for
    mechanical is retired;
15. the derive-() pin in
    `tests/test_cf5_f001_safety_signal_domain_seam.py::test_green_cold_load_restores_stored_domain_verbatim`
    (the MECH-envelope cold-load around the `domain_signal` fallback; seed text "a hinge idea") — flips ONLY if
    the authored vocabulary matches that seed text; if it flips, the verbatim-restoration and guard-anchor
    assertions are PRESERVED and only the derive expectation is re-pinned (with the never-electronics-labeled
    invariant asserted), disclosed.
**PERMITTED RECONCILIATION FILES (exact; changes to ANY other existing test = STOP):**
`tests/test_p9_mech_i1_capability_coverage_declaration.py`, `tests/test_p9_mech_i2_rule_nuances.py`,
`tests/test_p9_mech_i3_signal_quality.py`, `tests/test_p9_mech_i4_boundary_corpus.py`,
`tests/test_p9_mech_i5_question_sufficiency.py`, `tests/test_cf5_f001_safety_signal_domain_seam.py`,
`tests/test_d3_core_domain_neutrality.py`.
**Mandatory pre-freeze flip-sweep:** the implementation MUST simulate its end-state and prove the executed
reconciliation set is EXACTLY the applicable subset above (grep-based broad pin search — full-pack/blob/hash
snapshots, declaration content pins, derive-() pins, family-presence pins, provenance pins — plus the full suite);
any additional existing-test change → STOP.

## §5. Required evidence (future implementation)

**RED (clean parent):** `has_governed_safety_cue_family("mechanical") is False`; derivation on mechanical-domain
states with clearly hazard-stating inventor text returns `()` — the truthful pre-family gap. **GREEN:** the family
query flips True; derivation on mechanical-domain states with inventor-stated hazard text yields signals carrying
the F001 semantics (inventor-stated; required-independent-validation labeling; mechanical domain context — NEVER
electronics-labeled); non-cue mechanical text still derives `()`; the S15 deliverable surface for mechanical drops
the no-family statement automatically (evidence-only observation, no assembler change); the updated declarations
are truthful and equality-pinned. **Electronics byte-parity:** the electronics family constants byte-identical;
derivation outputs for a committed electronics state corpus byte-identical pre/post (the F001 d1-precedent);
electronics deliverable blocks unchanged. **Latency honesty:** mechanical remains unadmittable (activation-derived
admission unchanged); `support_state`/`activated_domains` pins. **Fail-safe:** software/medical/unknown domains
still have NO family (False + `()`). **Determinism.** **Mutations (each flips a pinned test; none retained):** m1
remove a cue class → family-shape pin; m2 inject electronics vocabulary into the mechanical family → collision
guard; m3 alter the electronics family → byte/parity pin; m4 revert the declaration update (reintroduce NOT
COVERED) → declaration pin; m5 tamper a reconciled absence-pin back to False → its reconciled test; m6 weaken the
never-electronics-labeled invariant probe → D3-A-style pin; plus the established self-integrity pattern (introspected
inventory + runtime-constructed needles) in the new evidence file. **Full governed suite; `git diff --check`; scope
proof; pycache discipline per the established runner.**

## §6. Closure criteria and boundaries

**Closure:** all §5 evidence green; §4 reconciliations executed exactly with in-file disclosures and the flip-sweep
proof; closure record stating — the governed Mechanical safety-cue family EXISTS, is merged and post-merge verified
→ **OD-M2 clause-3 activation blocker #1 = DISCHARGED**; the qualification record's clause-2 annotation is then
updated ONLY by that closure's sync (the QUALIFIED-WITH-ACTIVATION-BLOCKERS status persists with the remaining
blockers restated). **Remaining activation blockers after this lane closes: Tier-1 EN/AR label; CF-6; CF-2;
NMF-1/FU-1 disposition; explicit Owner activation authorization — none moved here.** Mechanical remains **NOT
ACTIVATED** throughout; Electronics unaffected; no D4/D8/THERM-01 (no thermal claim enters the vocabulary or
declarations)/Phase 10/PSRR/deployment; no P9 closure. **STOP conditions:** any forbidden-path need; any flip beyond
§4; any electronics derivation delta; any vocabulary that cannot satisfy §3 truthfully; any Owner-policy question.
**Next required gate: Mandatory Grill on this exact contract candidate.**
