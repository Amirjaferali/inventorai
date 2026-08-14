# P9-MECH-I2 — Mechanical Qualification-Grade Rule Nuances — Bounded Increment CONTRACT (governance-only contract gate)

**Status of THIS record:** governance/documentation-only **INCREMENT-CONTRACT CANDIDATE** under the AUTHORITATIVE
P9-MECH-QC contract (`docs/governance/P9_MECHANICAL_DOMAIN_QUALIFICATION_CONTRACT.md`) and after the AUTHORITATIVE
P9-MECH-I1 implementation. It becomes AUTHORITATIVE only through the governed lifecycle (Mandatory Grill → independent
external exact-candidate review → Owner acceptance → SHA-preserving publication → PR → create-a-merge-commit →
post-merge verification). **It implements nothing in this gate** (ZERO runtime/test/pack/registry/Web/CLI diff in this
candidate) and, once authoritative, authorizes ONLY the bounded P9-MECH-I2 implementation increment defined in §4 —
which itself requires separate explicit Owner authorization. It does NOT declare `mechanical` qualified, does NOT
activate anything, and records NO new Owner decision (**`OWNER_DECISION_REGISTER.md` UNCHANGED** — no Owner
product-policy decision is conveyed or needed by this gate). **DOCUMENTED NO-VALID-RED.**

## §1. Authoritative base and repository-first reconstruction

Base: `a52656d1ce78e67641685d86fa7a946cd92d2ff4` (merge of `f7ed7448` + corrected D-THERM-01 candidate `3c2ee0bc`,
merge tree `ba3a18dc` == candidate tree; freshly fetched; 0 newer; clean tree). Verified mechanically at this base:

- **`rule_nuances` consumption path (decisive, VERIFIED):** `engine/domain_registry.py` validates `rule_nuances` as a
  list of objects (element keys NOT frozen — enrichment fields are loader-safe, precedent
  `tests/test_s5_i1_domain_registry_hardening.py`); the SOLE runtime read is
  `engine/domain_rules.py::get_active_rules(domain)`, which returns `[rn["modifier_value"] for rn in
  pack["rule_nuances"]]` — and **`get_active_rules` has ZERO callers** in `engine/`, `web/`, and `scripts/`.
  Therefore `rule_nuances` are **runtime-inert beyond the accessor seam for EVERY pack, electronics included**: the
  electronics full-shape nuances have exactly the same (absent) downstream effect as mechanical's degenerate ones.
  Accessor baselines (frozen): `mechanical` → `['MECHANISM_COMPLETENESS', 'PHYSICAL_FEASIBILITY',
  'BOUNDARY_AMBIGUITY']`; `electronics_electrical` → `['PHYSICAL_PRINCIPLE_REQUIRED', 'POWER_ACKNOWLEDGMENT_IF_ENERGY',
  'NO_PLATFORM_SPECIFIC_NAMING']`; `software` → `['MECHANISM_COMPLETENESS', 'BOUNDARY_AMBIGUITY']`; `medical_device` →
  `['MECHANISM_COMPLETENESS', 'PHYSICAL_FEASIBILITY', 'BOUNDARY_AMBIGUITY']`.
- **Semantic difference (VERIFIED):** electronics `modifier_value`s are named reasoning-REQUIREMENT markers with
  `modifier_type: "additional_signal_required"`; mechanical/software/medical `modifier_value`s are the packs' own
  GAP-TYPE ids (migrated verbatim from the historical hardcoded `get_active_rules` branches — the packs'
  `_governance_notes` record this lineage). These are different semantics and MUST NOT be conflated.
- **P9-MECH-QC §6 discovered divergence (disclosed, not hidden):** §6(d) requires "focused tests demonstrating each
  nuance's observable effect." Repository truth shows NO nuance of ANY pack has an observable effect beyond the
  `get_active_rules` accessor seam, because the accessor is uncalled. §6(d) as literally written is therefore
  satisfiable ONLY at the accessor seam; demanding downstream behavior evidence would force inventing a NEW shared-core
  consumption path — a cross-domain runtime redesign that is NOT a Mechanical increment and is NOT authorized by
  P9-MECH-QC. This contract binds the truthful reading: **observable effect = the deterministic, test-pinned accessor
  output**, plus a mandatory explicit disclosure that no downstream consumer exists today. Any future nuance
  consumption (for any pack) is a separate shared-core gate requiring its own contract; nothing here designs or
  authorizes it.
- **I1 state:** the truthful capability/coverage declarations (incl. the OD-M2 clause-1 safety statement) are
  AUTHORITATIVE and byte-frozen by this contract; `mechanical:PR001`/`PR002` provenance records exist; the I1 test
  file pins other-pack byte identity and classifier corpus stability. **THERM-01** is authoritative anti-forgetting
  governance only; Mechanical's thermal NOT-COVERED status remains truthful and untouched here.

## §2. Remaining P9-MECH-QC obligation map (complete classification)

| Obligation (P9-MECH-QC §) | Classification after I1 |
|---|---|
| §5 capability contract + §7 coverage declaration | **COMPLETE by I1** (merged `f7ed7448`) |
| §6 qualification-grade rule nuances | **NEXT — THIS contract (P9-MECH-I2)** |
| §8 signal-quality / AB-006 evidence + §8.4 dormant-`weight` truthfulness disposition | **LATER qualification increment** (touches classifier-consumed fields / cross-pack disposition; kept separate — NOT absorbed; `weight` remains dormant and untouched in I2) |
| §9 cross-domain boundary-test evidence | **LATER qualification increment** (evidence-only; maximized once pack content is final, i.e. after I2 and the §8 lane) |
| §12 question / Path-N sufficiency | **LATER / partially blocked**: pack-question sufficiency is qualification work; validation through the Path-N seam is blocked behind the OPEN D-GMPR `path_n_questions` coupling (separate owner; NOT absorbed; not forced) |
| §13 Tier-1 EN/AR label | **PRE-ACTIVATION only** (activation-readiness edge; CF-2 NOT absorbed) |
| §11 safety-cue family | **PRE-ACTIVATION only** per OD-M2 (D-P9-MECH-02, Option B-hardened) — NOT pulled into qualification increments; no contradiction found |
| §15 qualification evidence package / §16 closure | **LATER — terminal** (assembled only after all qualification increments; conditional on the finally-standing OD-M2 clauses) |
| §10 electronics non-degradation | **CONDITIONAL / evidence-triggered — every increment** (re-proven per increment, incl. I2) |
| Provenance/truthfulness (§4b lineage; §5.1–5.6 acceptance criteria) | **CONDITIONAL — every increment** (binding on I2 as on I1) |
| Thermal capability | **Separate existing owner** — THERM-01 (future path; CAP-13/CAP-12/WS-PFV-001/D4 unchanged) |

## §3. Increment selection — why P9-MECH-I2 = rule-nuance enrichment is the smallest coherent NEXT

Candidates evaluated: **A** rule-nuance enrichment; **B** signal-quality/AB-006 + `weight` disposition; **C**
cross-domain boundary evidence; **D** question/Path-N sufficiency; **E** other (none evidenced). Dependency tests:
- **A** depends only on I1 (satisfied: nuances are judged against the declared scope); modifies NO runtime-consumed
  behavior (accessor output is pinned identical); changes NO classification or rule behavior; needs no Path-N/CF-6/
  CF-2/safety-family precondition; is qualification work; needs NO new Owner decision; has no competing owner (AB-006
  flags concern SIGNALS, not nuances). It is the LAST content gap P9-MECH-QC explicitly flags as
  not-qualification-grade ("degenerate `modifier_value`-only pointers").
- **B** touches `classification_signals` (classifier-consumed) and the cross-pack `weight` truthfulness question —
  higher risk class, potential Owner-decision surface, and its outcomes could invalidate boundary evidence run before
  it; correctly LATER and separate.
- **C** is evidence-only but its corpus value is maximized when pack content is final; running it before A/B risks
  re-running; correctly LATER.
- **D** is partially blocked by the OPEN D-GMPR coupling (validation path); forcing it would absorb or race a separate
  owner; correctly LATER/blocked.
Therefore **A** is the unique candidate that is unblocked, dependency-satisfied, runtime-neutral, owner-clean, and
closes a mandated content gap — the smallest coherent next increment.

## §4. The P9-MECH-I2 implementation increment — exact definition

```
INCREMENT CONTRACT — P9-MECH-I2 Qualification-Grade Rule Nuances   [defined here; implementation NOT started]
Responsibility:   Replace the mechanical pack's three degenerate rule_nuances entries with truthful, full-shape,
                  provenance-tagged entries — metadata enrichment ONLY, with the accessor-visible output proven
                  byte-identical. No behavior change of any kind.
Allowed paths:    domains/mechanical/domain.json — rule_nuances entries enriched IN PLACE (plus one additive
                  _governance_notes key recording this enrichment; the historical rule_nuances_absent note is
                  preserved untouched as history);
                  domains/domain_provenance.json — ONLY if a new additive provenance record (e.g. mechanical:PR003,
                  same mechanism as I1's PR002) is needed for the nuance metadata; existing records byte-untouched;
                  NEW tests/test_p9_mech_i2_rule_nuances.py;
                  governance sync at closure only (roadmap/AIC/CPS + closure record).
Forbidden paths:  engine/** (incl. domain_rules.py — get_active_rules MUST NOT gain callers or change), web/**,
                  scripts/**, all other domain packs (byte-frozen), every other mechanical pack field (incl.
                  capability_declaration, coverage_declaration, classification_signals, substance_signals,
                  gap_type_mappings, aliases, weight/layer metadata — all byte-frozen except the rule_nuances list
                  and the one additive note), schemas/, OWNER_DECISION_REGISTER.md (ZERO ODR diff), CI.
Deliverables:     For EACH of the three entries (exact modifier_value strings, order, and count preserved:
                  MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY):
                  (a) full-shape fields at electronics governance parity — rule_id (mechanical:RN00n), description,
                      layer, modifier_type, modifier_value, provenance_ref;
                  (b) TRUTHFUL semantics: modifier_type MUST truthfully name what these entries ARE — governed
                      active-gap-rule markers enumerating the pack's gap types (the migrated hardcoded-branch
                      lineage) — and MUST NOT copy electronics' "additional_signal_required" semantic untruthfully;
                      the naming is decided at implementation but bound by this truthfulness rule;
                  (c) each description states the reasoning requirement its gap type governs, grounded ONLY in the
                      pack's existing gap-type content and I1 declared scope — no unsupported Mechanical expertise
                      (no FEA/tolerance/materials/manufacturing/certification/thermal/physical-testing claims);
                  (d) canonical source per nuance = the pack's own gap_type_mappings + the I1 declarations + this
                      contract, recorded via provenance_ref resolving in the existing manifest;
                  (e) mandatory in-pack disclosure (the additive note) that rule_nuances have NO downstream runtime
                      consumer today (accessor-seam only; future consumption = separate shared-core gate).
```

## §5. Expected vs forbidden runtime differential (binding)

**Expected runtime differential: NONE — zero.** `get_active_rules` output byte-identical for ALL packs (the four
baselines in §1 are frozen pins); classifier outputs identical over the committed corpus; registry recognition set
identical; all I1 tests still green; full suite green. **Forbidden differential:** any change to any accessor output
(value/order/count); any new caller of `get_active_rules` or any new nuance-consumption path; any change to
classification, admission, questions, safety derivation, labels, or deliverables; any byte change to any other pack or
to any other mechanical field. **No false behavior claim:** no test, note, record, or report may claim the enrichment
changes or specializes runtime behavior — repository truth (§1) is that it cannot, and saying otherwise would be the
exact false-expertise failure P9-MECH-QC forbids.

## §6. Evidence / test requirements (proportionate; all load-bearing)

- **Parent RED:** the new focused tests fail on the clean parent for the right reasons (entries lack rule_id/
  description/layer/modifier_type/provenance_ref; disclosure note absent) — messages inspected and recorded.
- **Focused GREEN (NEW `tests/test_p9_mech_i2_rule_nuances.py`):** full-shape pin per entry; EXACT modifier_value
  sequence pin (`['MECHANISM_COMPLETENESS','PHYSICAL_FEASIBILITY','BOUNDARY_AMBIGUITY']`); `get_active_rules`
  byte-identity pins for ALL FOUR packs (the §1 baselines); exact-content equality pin on the three descriptions
  (the I1 anti-paraphrase pattern — ANY reworded or added claim flips RED); truthful modifier_type pin (equality);
  provenance_ref resolution in the manifest with existing records untouched; disclosure-note presence pin;
  I1-declaration byte-stability pin (capability/coverage blocks unchanged); other-pack byte-identity (reuse/extend the
  I1 sha256 pattern); deterministic repeated load.
- **Negative tests:** foreign/unknown domain → `get_active_rules` returns `[]` unchanged; enrichment does not alter
  `has_governed_safety_cue_family("mechanical")` (False) or any classifier pin.
- **Differentials:** parent-vs-candidate sweep — accessor outputs (4 packs), classifier corpus, registry set — ZERO
  deltas; full governed suite green; `git diff --check` clean.

## §7. Mutation / adversarial probes (each must flip a specific test RED; none retained)

m1 change one modifier_value → accessor-sequence pin RED; m2 remove one entry → count/sequence RED; m3 reorder
entries → sequence RED; m4 insert an unsupported-expertise description clause (e.g. FEA wording) → description
equality pin RED; m5 paraphrased overclaim NOT using the forbidden lexicon (e.g. a load-bearing-verification claim
reworded) → equality pin RED; m6 strip a provenance_ref or the new manifest record → provenance test RED; m7 tamper
one byte of the electronics pack → byte pin RED; m8 alter an electronics nuance via the registry double or file →
electronics accessor pin RED; m9 remove the no-downstream-consumer disclosure note → disclosure pin RED.

## §8. Boundaries, stop conditions, closure

**Qualification/activation:** completing I2 does NOT declare Mechanical qualified (the §2 map shows §8/§9/§12/§15
obligations remain; OD-M2 clause 2 forbids any unannotated claim); does NOT activate anything
(`activated_domains() == ['electronics_electrical']`; first new-domain activation remains BLOCKED incl. OD-M2
clause 3). **Anti-duplication:** AB-006 flags stay in the §8 signal lane; D-GMPR coupling untouched; CF-6/CF-2
untouched; THERM-01 untouched (no thermal claim — the nuance descriptions MUST NOT mention thermal capability);
CAP-12/CAP-13/WS-PFV-001/D4/D8 untouched; no new framework, owner, or consumption path. **Stop conditions:** any need
to touch a forbidden path; any accessor-output delta; any pressure to invent a consumption path or behavior claim; any
truthful-description impossibility → STOP — CONTRACT AMENDMENT / OWNER DECISION REQUIRED. **Closure:** the increment
closes only via its own evidence package (RED/GREEN/negative/mutations/differentials/full suite), candidate freeze,
Grill, independent review, Owner acceptance, merge, post-merge verification, and a closure record; closing I2
authorizes NO later increment. **Next required gate: Mandatory Grill on this exact contract candidate.**
