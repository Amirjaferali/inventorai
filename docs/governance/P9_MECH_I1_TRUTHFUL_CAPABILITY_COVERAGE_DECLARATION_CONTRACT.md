# P9-MECH-I1 — Mechanical Truthful Capability & Coverage Declaration — Bounded Increment CONTRACT (governance-only contract gate)

**Status of THIS record:** governance/documentation-only **INCREMENT-CONTRACT CANDIDATE** under the AUTHORITATIVE
P9-MECH-QC contract (`docs/governance/P9_MECHANICAL_DOMAIN_QUALIFICATION_CONTRACT.md`, merged PR #467). It becomes
AUTHORITATIVE only if this exact candidate completes the governed lifecycle (Mandatory Grill → independent external
exact-candidate review → Owner acceptance → SHA-preserving publication → PR → create-a-merge-commit → post-merge
verification). **It implements nothing in this gate** — ZERO runtime / test / domain-pack / registry / Web / CLI /
activation / schema / persistence diff in this candidate — and, once authoritative, it authorizes ONLY the bounded
P9-MECH-I1 implementation increment defined in §4 (which itself still requires the governed implementation lifecycle).
It does NOT declare `mechanical` qualified, does NOT activate anything, and changes no registry membership.
**DOCUMENTED NO-VALID-RED — GOVERNANCE-ONLY CONTRACT GATE.**

## §1. Authoritative base and reconstruction

Base: `90b1b00f0bd384911735a55340ee15829a77bbad` (PR #467 merge — P9-MECH-QC AUTHORITATIVE; freshly fetched; 0 newer;
clean tree). P9-MECH-QC requires, before any qualification claim: §5 truthful capability contract; §6 real rule
nuances; §7 coverage declaration at electronics governance parity; §8 signal-quality evidence incl. the dormant
`weight`-metadata truthfulness disposition; §9 boundary tests; §10 electronics non-degradation; §11 safety-cue family
per OD-M2; §12 pack-question sufficiency; §13 truthful label (activation-readiness edge); §15 the full evidence
package. **Mechanically verified this gate:** `engine/domain_registry.py` §5-I1 validation is required-fields-only
(`_TOP_LEVEL_REQUIRED` / `_GOVERNANCE_REQUIRED` / `_V1_REQUIRED`; no unknown-field rejection), and the activated
electronics pack already carries a tolerated `coverage_declaration` — so **additive declaration fields in
`domains/mechanical/domain.json` are provably loader-safe with zero engine change**, making a declaration-only first
increment technically coherent.

## §2. OD-M2 — CANONICALLY RESOLVED (recorded THIS gate; no standalone OD-M2 gate)

Recorded as **`D-P9-MECH-02`** in `docs/governance/OWNER_DECISION_REGISTER.md` (same in-contract-gate recording
pattern as D-P9-MECH-01 / D-CF5-F002-01 / D-CF5-F004-01). Owner-approved substance, binding verbatim:

**OD-M2 — RESOLVED: Option B-hardened, Mechanical-specific.** A governed Mechanical safety-cue family is **NOT**
required for `mechanical` to be declared P9-QS QUALIFIED, PROVIDED ALL of:
1. the Mechanical capability and coverage declarations **explicitly declare inventor-stated safety-signal derivation
   NOT COVERED** pending a governed Mechanical safety-cue family;
2. any Mechanical qualification record **prominently records the absent safety-cue family as an outstanding
   ACTIVATION BLOCKER** for `mechanical` — no unannotated or misleading "QUALIFIED" claim is permitted;
3. a governed Mechanical safety-cue family — via the existing `engine/safety_signal.py` F001 per-domain seam, with
   provenance-tagged hazard vocabulary, focused tests, negative tests, mutation/adversarial tests, and electronics
   non-degradation evidence — is **REQUIRED and MUST be complete, merged, and post-merge verified BEFORE any Owner
   activation authorization for `mechanical`**.

This decision applies to **`mechanical` only**; it neither creates, waives, nor predetermines safety-cue-family policy
for any other current or future domain, and it does NOT modify or close P9-QS, F001, CF-6, CF-2, D-GMPR, D4, D8,
Phase 10, PSRR, or deployment. Consequences bound into this contract: the truthful empty-family state remains valid
ONLY while clause 1's NOT-COVERED declaration exists (delivered by THIS increment); the family's absence is an
ACTIVATION BLOCKER independent of qualification progress; the Mechanical safety-family implementation is a **separate
future evidence-bearing gate** before activation; and **this first increment MUST NOT implement the safety family** —
repository truth shows the declaration increment is fully coherent without it (the family is runtime vocabulary in
`engine/safety_signal.py`, an explicitly forbidden path here, while the declaration is pack metadata).

## §3. Increment selection — smallest coherent first increment (repository-derived)

**Selected: P9-MECH-I1 = the truthful declaration foundation — Mechanical capability contract + coverage declaration,
as ONE additive pack-metadata artifact, plus the focused tests that pin its truthfulness.**

Why capability + coverage are one inseparable responsibility: P9-QS §4's Domain Capability Contract is *expressed*
through the declared covered / not-covered / limitations / known-unknowns content — in the repository's only precedent
(electronics) that expression IS the `coverage_declaration` block. P9-MECH-QC §5 and §7 describe the same truthful
declaration from two angles (what is claimed vs how it is governed). OD-M2 clause 1 requires the safety-derivation
NOT-COVERED statement to live in "the Mechanical capability and coverage declarations" — a single pack artifact.
Splitting them would create two gates editing the same JSON block with no independent evidence, violating the
one-responsibility rule in the other direction.

Why this is FIRST: P9-QS §3 judges every other qualification evidence class **relative to truthful declared
capabilities**. Rule-nuance enrichment (§6), signal-quality/AB-006 evidence (§8), and boundary tests (§9) all need the
declared scope as their yardstick; the declaration needs none of them. It is also the increment OD-M2 clause 1
depends on — until it lands, the truthful-empty-family state rests only on the runtime disclaimer rather than on
declared scope.

Why the deferred items are NOT needed for coherence (each stays a separate future increment under P9-MECH-QC):
- **Rule nuances (§6):** behavior-affecting content consumed via the migrated `get_active_rules` lineage — enrichment
  requires its own observable-effect tests; combining it would mix metadata-only and behavior-affecting work.
- **Signal quality / AB-006 / dormant `weight` disposition (§8):** touches fields the classifier actually consumes
  (`classification_signals`) or shared-core truthfulness questions with cross-pack reach — explicitly kept separate
  (this contract keeps `weight` dormant and untouched; §5.3 forbids implying otherwise).
- **Boundary tests (§9), question sufficiency (§12), label (§13):** each depends on the declared scope and carries its
  own evidence class. **Safety-cue family:** its own pre-activation gate per OD-M2 clause 3.

## §4. The P9-MECH-I1 implementation increment — exact definition

```
INCREMENT CONTRACT — P9-MECH-I1 Truthful Capability & Coverage Declaration   [defined here; implementation NOT started]
Objective:            Add the truthful, provenance-tagged Mechanical capability/coverage declaration (electronics-
                      parity governance shape) to domains/mechanical/domain.json, incl. the OD-M2 clause-1 statement,
                      pinned by focused tests. Declaration/metadata ONLY — zero behavior change.
Allowed paths:        domains/mechanical/domain.json (ADDITIVE declaration fields only);
                      NEW tests/test_p9_mech_i1_capability_coverage_declaration.py;
                      governance sync at closure (roadmap/AIC/CPS + closure record).
Forbidden paths:      engine/** (incl. domain_registry.py, domain_rules.py, safety_signal.py), web/**, scripts/**,
                      templates/static, all other domain packs (byte-frozen, incl. electronics + iot_electronics),
                      domains/domain_provenance.json beyond what existing provenance convention REQUIRES for new
                      provenance_refs (if required, additive rows only, disclosed), schemas/, database/, benchmark/,
                      requirements/CI, OWNER_DECISION_REGISTER.md (implementation gate = ZERO ODR diff).
Deliverables:         (a) `coverage_declaration` for mechanical in the electronics-precedent shape (covered_areas /
                      not_covered_areas / known_limitations) — truthful per P9-MECH-QC §5: concept-level claims only
                      (mechanism completeness; concept-level physical feasibility vs stated principles; boundary/
                      differentiation reasoning; gap detection for the three governed gap types); not_covered_areas
                      MUST include at minimum: inventor-stated safety-signal derivation (OD-M2 clause 1, pending the
                      governed family), stress/FEA & fatigue analysis, tolerance/GD&T verification, materials
                      selection/certification, manufacturing process validation, CAD/physical-fit verification,
                      regulatory/machinery-safety certification, production cost/supply chain, physical testing;
                      known_limitations MUST state: early-concept only; parent-level breadth without sub-domain depth;
                      questions calibrated for concept validation not specialist review; unknowns requiring physical/
                      specialist validation remain unknowns (WS-PFV-001 routing referenced, not executed).
                      (b) capability-contract expression per P9-QS §4 carried by (a) plus, ONLY if needed, additional
                      ADDITIVE truthful fields (e.g. supported gap types, evidence expectations, known unknowns);
                      exact field naming decided at implementation; every field additive, loader-tolerated (verified
                      §1), and describing ONLY implemented-and-governed behavior.
                      (c) provenance tagging for all new declaration content via the existing pack provenance
                      conventions (provenance_ref lineage / _governance_notes) — no new provenance framework.
                      (d) the focused test file (§6).
Non-goals:            Everything in §3's deferred list; any behavior change; any qualification claim.
```

## §5. Technical-truth acceptance criteria (binding on the implementation increment)

1. **No false upgrade by metadata:** richer declaration content MUST NOT be presented, tested, or recorded as
   increased Mechanical capability; the increment's closure record must state that Mechanical's runtime behavior is
   **byte-for-byte unchanged** and that the increment moves Mechanical toward qualification ONLY by making its
   existing scope truthfully declared.
2. **Truthful claims only:** every `covered_areas` entry maps to behavior that exists and is governed TODAY (signals,
   gap types, questions actually in the pack); no unsupported Mechanical expertise (no FEA/fatigue/tolerance/
   materials/manufacturing/regulatory claim anywhere in covered content).
3. **Dormant metadata stays dormant and truthfully framed:** per-signal `weight`/`layer` metadata is untouched and
   MUST NOT be referenced by the declaration as runtime-active; its truthfulness disposition remains the separate
   §8-lane increment (P9-MECH-QC §8.4).
4. **Determinism & backward compatibility:** pack parses; §5-I1 registry load succeeds; recognized-domain set
   IDENTICAL before/after; alias resolution unchanged; `classify_domain` outputs on a committed corpus IDENTICAL
   before/after (declarations are not classifier inputs — proven, not assumed); electronics pack and all other packs
   byte-identical.
5. **No recognition/classification drift:** if implementation proves ANY consumed field must change to satisfy this
   contract → STOP — CONTRACT AMENDMENT REQUIRED (with before/after differential evidence attached to the stop
   report). This contract authorizes NO consumed-field change.
6. **OD-M2 clause-1 satisfaction:** the NOT-COVERED safety-derivation statement present verbatim-equivalent in the
   declaration and pinned by test; its absence after this increment is a defect, not a policy option.

## §6. Evidence / test requirements (proportionate; all load-bearing)

- **Parent RED / deficiency evidence:** the new focused tests run on the clean parent MUST fail for the right reasons
  (no `coverage_declaration`; no capability expression; no safety-derivation NOT-COVERED statement) — each failure
  message inspected and recorded.
- **Focused GREEN tests (NEW `tests/test_p9_mech_i1_capability_coverage_declaration.py`):** declaration present with
  the required shape; mandatory not_covered entries present (incl. the OD-M2 clause-1 item); known_limitations
  present; provenance refs present and resolvable per existing convention; forbidden-claim guard (no covered-area
  text asserting the §5.2 excluded expertise); electronics `coverage_declaration` untouched (byte pin of the
  electronics pack file); recognized-registry set IDENTICAL to the parent's (the four v1.0
  recognized packs; `iot_electronics` remains intentionally registry-skipped per D8 — untouched); deterministic
  repeated-load equality.
- **Negative tests:** a non-existent/foreign domain still has no Mechanical declaration leakage; declaration presence
  does NOT alter `has_governed_safety_cue_family("mechanical")` (stays False) nor any classifier output.
- **Mutation/adversarial probes (each must flip a test to RED):** (m1) remove the safety-derivation NOT-COVERED entry;
  (m2) insert an unsupported-expertise covered claim (e.g. FEA); (m3) delete `coverage_declaration` entirely;
  (m4) tamper one byte of the electronics pack; (m5) remove a mandatory known_limitations statement; (m6) strip the
  new content's provenance tagging.
- **Differential evidence:** committed classification corpus (reuse the F004 D1-corpus pattern) byte-identical
  before/after; `/start` outcomes for that corpus identical (web untouched — proven, not assumed).
- **Full-suite regression:** entire governed suite green at the implementation candidate; counts reported against the
  parent baseline. **`git diff --check`** clean. NOT required (with reason): benchmark re-runs (no scoring/classifier
  surface touched), Playwright/UI classes (no web change), performance evidence (metadata-only).

## §7. Boundaries and non-goals (all preserved)

This gate and the increment it defines do NOT: declare Mechanical P9-QS QUALIFIED (the §15 package remains far from
complete — §3 deferred list); activate Mechanical or touch `_ACTIVATED_DOMAINS`; register any domain or change
recognized membership; implement or invoke D4 (Amendment 01 semantics untouched); resolve or prejudge D8; close or
absorb CF-6, CF-2, or the D-GMPR `path_n_questions` coupling; implement the Mechanical safety-cue family (separate
pre-activation gate per OD-M2 clause 3); modify the F003/F004 classifier semantics or any engine/web/CLI file; start
Phase 10 / PSRR / deployment. `activated_domains() == ['electronics_electrical']`; first new-domain activation remains
BLOCKED behind its existing prerequisites plus OD-M2 clause 3. NMF-1/FU-1 unchanged in their lane. Canonical owners
reused throughout (§5-I1 registry ownership; pack provenance conventions; F001 seam untouched; AB-006 flags remain the
§8-lane input) — **no second registry, capability framework, qualification model, safety framework, provenance ledger,
or duplicate tracker**.

## §8. Lifecycle, stop conditions, and next gate

The implementation increment requires: separate explicit Owner authorization; execution fresh from the then-current
authoritative tip; the §6 evidence in full; candidate freeze; Mandatory Grill; independent external exact-candidate
review; Owner acceptance; SHA-preserving publication; PR (create-a-merge-commit); post-merge verification; then a
closure record before any next increment activates. **Stop conditions:** any forbidden-path need; any consumed-field
change (§5.5); any truthful-claim impossibility (a required covered_area cannot be truthfully claimed); any provenance
convention that would require a new framework; any OD-M2 inconsistency → STOP — CONTRACT AMENDMENT / OWNER DECISION
REQUIRED. **Next required gate: Mandatory Grill on this exact contract candidate.**
