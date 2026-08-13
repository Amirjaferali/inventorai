# P9-MECH-QC — Mechanical Domain P9-QS Qualification Contract (governance-only contract gate)

**Status of THIS record:** governance/documentation-only **CONTRACT CANDIDATE**. It becomes AUTHORITATIVE only if this
exact candidate completes the governed lifecycle (Mandatory Grill → independent external exact-candidate review → Owner
exact-candidate acceptance → SHA-preserving publication → PR → create-a-merge-commit → post-merge verification). Until
then it authorizes nothing. **It does NOT declare `mechanical` qualified, does NOT activate any domain, does NOT change
the recognized-registry set, and implements nothing** — ZERO runtime / test / Web / CLI / Domain-Pack / registry /
activation / schema / persistence diff in this gate. It defines what future implementation and evidence MUST exist
before `mechanical` may be declared **P9-QS QUALIFIED** under the already-authoritative P9-QS standard
(`docs/governance/P9_QS_PHASE_9_TECHNICAL_QUALITY_STANDARD_CONTRACT.md`, merged PR #437). Subordinate to CLAUDE.md, the
committed anchors, `ACTIVE_EXECUTION_ROADMAP.md`, and P9-QS itself. **DOCUMENTED NO-VALID-RED — GOVERNANCE-ONLY
CONTRACT GATE.**

## §1. Authoritative base and repository-first reconstruction

Base: `c4abe0207c34f15e89438cc931c114db9d2e6225` (`feature/atomic-json-session-persistence`; PR #466 merge —
`D-GMPR-01-D-D4` Amendment 01 AUTHORITATIVE; freshly fetched; 0 newer; clean tree). Reconstructed and verified from
repository truth at this exact base (all claims below re-checked mechanically, not assumed from advisory inputs):

- **P9-QS** is the authoritative qualification standard: §2 binding separations; §3 activation-quality relative to
  truthful declared capabilities; §4 Domain Capability Contract via existing §5-I1 Domain-Pack/Registry ownership; §4b
  D13 knowledge/provenance/licensing reuse; §5 existing-owner reuse (no second ledger/engine); §6 cross-domain
  boundary-test minimum; §7 qualification proof (A: works in declared scope; B: does not materially degrade activated
  domains); §9 versioning/backward compatibility; §15 D4 reference-only placeholder; §17 D8 boundary.
- **`domains/mechanical/domain.json`** (schema 1.0; lifecycle `status: "active"` — a legacy lifecycle label that is NOT
  runtime activation per §5-I2): 19 classification signals (with `weight`/`layer` metadata), 17 substance signals with
  real provenance-tagged contexts (including declared CROSS-DOMAIN ownership for `valve`/`pressure`/`compression`/
  `actuator` and LOW-SPECIFICITY flags for `mechanism`/`force`/`bar` recorded as AB-006 candidates), 3 gap types
  (`MECHANISM_COMPLETENESS`, `PHYSICAL_FEASIBILITY`, `BOUNDARY_AMBIGUITY`) carrying 10 verbatim-migrated questions,
  aliases `["mechanical"]` only, and **degenerate `rule_nuances`** (three `modifier_value`-only entries).
- **`domains/electronics_electrical/domain.json`** (the activated reference): 15 classification signals but **53**
  substance signals, **full-shape rule nuances** (`rule_id`/`description`/`layer`/`modifier_type`/`modifier_value`/
  `provenance_ref`), a **`coverage_declaration`** (`covered_areas` / `not_covered_areas` / `known_limitations`),
  shorthand aliases, and family metadata (`authorized_child_domains`, `domain_family_role`).
- **Recognition owner:** `engine/domain_registry.py` (§5-I1). **Activation owner:** `engine/domain_activation.py`
  (§5-I2; `_ACTIVATED_DOMAINS = frozenset({"electronics_electrical"})`; REGISTERED ≠ USER-ACTIVE; aliases are
  recognition-only). **Classifier owner:** `engine/domain_rules.py::classify_domain` — score = **cardinality of the
  matched-signal set** under the F003 bounded whole-token + final-token `+"s"`/`+"es"` plural matcher (domain-generic
  by construction); F004 architecture (sole-top SINGLE; bounded legacy-four precedence layer;
  `UNRESOLVED_NON_ACTIVATED_TIE` fail-closed; `AMBIGUOUS_TIE` activated-only; `MULTI_DOMAIN_NEEDS_D4` reserved, never
  produced). **VERIFIED FACT: the per-signal `weight` metadata is NOT consumed by `classify_domain`** — it is dormant
  declared metadata (see §8/§19).
- **Safety signals:** `engine/safety_signal.py` (F001 seam) — `_DOMAIN_CUE_FAMILIES` contains ONLY
  `electronics_electrical`; `has_governed_safety_cue_family("mechanical")` is False; derivation returns `()` and the
  deliverable renders the truthful capability-scope statement. **Mechanical has NO governed safety-cue family today.**
- **Path-N:** `engine/path_n_questions.py` serves the Electronics-OWNED committed artifact only for electronics or the
  backward-compatible `None`; a recognized non-electronics domain receives `None` (caller fallthrough) — canonical
  per-domain question ownership is the Domain-Pack `gap_type_mappings`. The **D-GMPR-01-D-D3 `path_n_questions.py`
  coupling remains OPEN** (separate lane).
- **Public labels:** `web/domain_label.py::_PUBLIC_DOMAIN_LABELS` carries ONLY electronics (EN/AR Tier-1);
  `mechanical` truthfully resolves to the neutral Tier-0 "General idea review" fallback (never silently electronics).
- **CF-6 remainder (OPEN):** Web/CLI pre-classifier consistency incl. the CLI §5-I2-bypassing electronics literal
  (`scripts/run_cli.py` hardcodes `domain != "electronics_electrical"` and electronics-only copy). **CF-2 (OPEN):**
  public-message truthfulness beyond the F002 `/start` flow. **NMF-1 / FU-1:** pre-activation test-hardening
  carry-forwards (CF-5 closure §6). **D4:** Amendment 01 authoritative; execution NOT AUTHORIZED. **D8:**
  `iot_electronics` Owner-reserved, untouched.
- **Relevant durable decisions:** D3 core domain-neutrality lineage (three couplings discharged; `path_n_questions`
  open); D-CF5-F002-01 activation-derived `/start` admission; D-CF5-F004-01 (OD1 satisfied by F004 formal closure —
  recognized-set-changing pack-schema/provenance work is no longer F004-blocked, but none is performed here; OD2 legacy
  precedence preserved); P9-E1/P9-E2/P9-E2-R caller-propagation and activated-tie policies; D-P6-16/17/18 label and
  language decisions; OD-F/OD-G/OD-H extensibility; AB-006 CLOSED WITH DEFERRED ITEMS (its recorded signal-quality
  candidate flags remain live inputs inside the mechanical pack's `_governance_notes`).

The advisory selection review's thinness claim is therefore **independently confirmed in substance**: `mechanical` is
genuinely recognized with real provenance-tagged content, but it is materially thinner than electronics where P9-QS
quality lives (substance depth 17 vs 53; degenerate vs full rule nuances; no coverage declaration; no safety-cue
family; no Tier-1 public label; alias inventory minimal). Recognition does NOT make it qualification-grade (P9-QS §2.1).

## §2. Canonical Owner selection decision (recorded THIS gate — no standalone selection gate)

Recorded canonically as **`D-P9-MECH-01`** in `docs/governance/OWNER_DECISION_REGISTER.md` (per the
D-CF5-F002-01/D-CF5-F004-01 convention: the contract gate records the Owner decision it operates under; both become
authoritative together at this candidate's merge). Substance, binding here and there:

1. The Owner SELECTS **`mechanical`** as the next specialist domain to pursue through Phase-9 P9-QS qualification.
2. **Selection ≠ qualification.** This selection authorizes Mechanical qualification **planning/governance only** — it
   does not declare, imply, or schedule qualification completion.
3. **Qualification ≠ activation.** Even a future successful qualification does NOT activate `mechanical`; activation
   remains a separate, explicitly-Owner-authorized §5-I2 gate behind the existing prerequisites (§16).
4. This decision changes **NO** recognized-registry membership and modifies **NO** pack, registry, classifier,
   activation, Web, or CLI file.
5. This decision does **NOT** authorize Mechanical activation.
6. A future successful Mechanical qualification proves ONLY **qualification-extensibility for an already-recognized
   domain**; it does **NOT** prove registration-extensibility for future fifth/sixth/new domains, and the ability to
   independently test genuinely-new-domain registration extensibility is explicitly preserved as future, separately
   governed work.
7. All existing boundaries are preserved: D4 (registered, NOT AUTHORIZED), D8 (Owner-reserved), CF-6 (OPEN), CF-2
   (OPEN), D-GMPR `path_n_questions` coupling (OPEN), Phase 10 (NOT AUTHORIZED), PSRR (NOT EXECUTED), deployment (NOT
   AUTHORIZED).

## §3. Purpose and non-goals

**Purpose.** Define the exact, bounded governance contract under which `mechanical` can eventually be determined
**P9-QS QUALIFIED**. The contract defines required future implementation/evidence; it decides nothing that P9-QS or the
Owner has not already decided. **Non-goals (binding):** qualifying Mechanical by declaration; activating Mechanical;
editing `domains/mechanical/domain.json`; adding safety cues, Path-N content, labels, or classifier/registry changes;
resolving CF-6/CF-2/D-GMPR; executing D4/D8; any implementation. Future implementation increments under this contract
each require their own Owner authorization and the governed lifecycle.

## §4. Binding separations (restated from P9-QS §2; nothing weakened)

Recognition ≠ qualification; qualification ≠ Owner authorization; Owner authorization ≠ runtime activation (activation
= the governed §5-I2 allowlist gate completes under explicit Owner authorization); activation ≠ multi-domain
composition authority (D4); Phase-9 work ≠ Phase 10/PSRR/deployment/production. Additionally, per D-P9-MECH-01:
selection ≠ qualification, and qualification-extensibility ≠ registration-extensibility.

## §5. Requirement 1 — Mechanical Domain Capability Contract (P9-QS §4; existing ownership only)

Before qualification may be claimed, `mechanical` MUST expose a truthful, canonical, machine-readable capability
declaration through the EXISTING §5-I1 Domain-Pack/Registry ownership (no second registry, no new schema framework;
any additive pack-schema evolution needed is governed by the existing pack-schema owners and MUST NOT change the
recognized-registry set). It must express, where applicable, and without inventing unsupported Mechanical expertise:

- **Claims to assess (concept-level only, mirroring the electronics precedent):** mechanism completeness (what moves,
  connects, transfers force); concept-level physical feasibility relative to stated principles (leverage, spring
  tension, gear ratio, friction); boundary/differentiation reasoning; evidence-vs-assumption distinction within its
  declared scope; gap detection for its three governed gap types (or a truthfully extended, provenance-tagged set).
- **Explicitly NOT assessed (minimum, subject to truthful refinement at the implementation gate):** stress/FEA and
  fatigue analysis; tolerance/GD&T verification; materials certification; manufacturing process validation; CAD/fit
  verification; regulatory/safety certification (e.g. machinery directives); production cost/supply chain; physical
  testing of any kind. A capability MUST NOT be implied that is not implemented AND qualified (P9-QS §4 truthfulness
  rule; the listed items are non-binding examples, never requirements).
- **Limitations & known unknowns:** early-concept stage only; parent-level breadth without sub-domain depth; questions
  calibrated for concept validation, not specialist engineering review; explicit statement of what remains unknown
  without physical validation (routing per §14).
- **Supported gap types, provenance expectations** (verbatim provenance via the existing D13/§4b and
  `record_contract`/`record_store` owners), **evidence expectations, and scope boundaries** for each declared area.

## §6. Requirement 2 — Real rule nuances (no placeholder qualification-grade content)

VERIFIED: mechanical `rule_nuances` are degenerate `modifier_value`-only pointers; electronics nuances carry
`rule_id`/`description`/`layer`/`modifier_type`/`provenance_ref`. **Binding rule:** degenerate/placeholder rule-nuance
content MUST NOT be treated as qualification-grade. Qualification requires Mechanical-specific rule nuances that are
(a) full-shape (at minimum the electronics nuance shape), (b) provenance-tagged to real Mechanical engineering
rationale, (c) truthful (each nuance describes an actually-enforced reasoning requirement, not aspiration), and
(d) evidenced by focused tests demonstrating each nuance's observable effect. Migrated-pointer parity alone is
insufficient; equally, nuances MUST NOT encode expertise the capability contract does not claim.

## §7. Requirement 3 — Coverage declaration (required; electronics-parity governance quality)

VERIFIED: mechanical has NO `coverage_declaration`; the activated electronics pack has one. **Determination:** yes —
qualification REQUIRES a Mechanical coverage declaration of at least the electronics governance shape
(`covered_areas` / `not_covered_areas` / `known_limitations`), consistent with §5, truthful, provenance-tagged, and
test-referenced. Its absence is a verified qualification gap, not an activation-time nicety: P9-QS §3 judges quality
relative to truthful DECLARED capabilities, which requires the declaration to exist.

## §8. Requirement 4 — Domain signal quality (evidence, not assertion)

Qualification requires committed evidence that:

1. **Domain relevance:** each classification/substance signal is genuinely Mechanical (the pack's own AB-006 candidate
   flags — `mechanism`, `force`, `bar`, `bracket`, `fastener`, `locking` — are resolved by evidence: retained with
   justification, re-weighted in meaning via context, or dispositioned; the AB-006 identity is REUSED as the recorded
   input; AB-006 itself, CLOSED WITH DEFERRED ITEMS, is not reopened as a tracker).
2. **Electronics overlap is acceptable:** the declared CROSS-DOMAIN signals (`valve`, `pressure`, `compression`,
   `actuator`) and any newly evidenced overlaps have explicit context ownership and boundary-test coverage (§9), with
   no unacceptable capture of clearly-electronics ideas and no hidden electronics assumption distorting Mechanical
   recognition (shared-core neutrality per the closed D3/F001-F004 lineage is preserved, not re-litigated).
3. **Truthful matching semantics:** singular/plural/normalization behavior of Mechanical vocabulary under the
   authoritative F003 bounded whole-token + final-token `+s`/`+es` matcher is evidenced (which Mechanical terms do and
   do not match in plural/irregular forms — e.g. sibilant/irregular forms that the bounded rule intentionally does not
   catch — stated truthfully; NO matcher change is authorized by this contract; any proposed matcher change is a
   separate classifier-owner gate with F003 parity obligations).
4. **Declared-metadata truthfulness:** the VERIFIED dormancy of per-signal `weight` metadata (unused by
   `classify_domain`, which scores by matched-set cardinality) MUST be truthfully dispositioned for Mechanical
   qualification — either the declaration is corrected/annotated at the pack level so metadata no longer implies
   unimplemented behavior, or the semantics are implemented under the classifier owner with full F003/F004 parity
   evidence. **This contract does NOT choose implementation; it forbids leaving the untruthful implication in a
   qualified pack.** (This fact equally affects other packs; recording it here creates no new tracker — it binds only
   Mechanical qualification, and is surfaced to the Owner via §19.)

## §9. Requirement 5 — Cross-domain boundary testing (P9-QS §6; D4 NOT invoked)

Required boundary-test classes between `mechanical` and `electronics_electrical` (deterministic, committed,
vocabulary-honest — inputs must not accidentally pass for the wrong reason):

- clearly Mechanical ideas → Mechanical recognition path (truthful non-activated handling while unactivated);
- clearly electronics ideas → electronics outcome UNCHANGED (byte-level parity where the surface permits);
- mixed electro-mechanical ideas → truthful classifier outcome under the F004 architecture (SINGLE sole-top /
  legacy-layer / `UNRESOLVED_NON_ACTIVATED_TIE` / `AMBIGUOUS_TIE` activated-only as applicable), with the web/CLI
  fail-closed dispatches exercised;
- low-evidence ideas → truthful NONE/guidance behavior, no silent electronics capture and no silent Mechanical capture;
- ambiguous/tied ideas → the governed tie kinds, never an invented winner;
- negative cases → non-domain text stays NONE; collision guards for Mechanical vocabulary;
- legacy regression cases → the D-CF5-F004-01 OD2 legacy-four precedence outcomes preserved.

**D4 separation (binding):** testing mixed-domain classification boundaries grants NO multi-domain composition
authority. `MULTI_DOMAIN_NEEDS_D4` remains reserved/never-produced; no cross-domain evaluation, shared-constraint
propagation, or unified assessment may be implemented or simulated as product behavior under this contract (§18).

## §10. Requirement 6 — Electronics non-degradation (P9-QS §7-B)

Qualification requires explicit evidence that the activated `electronics_electrical` experience is not materially
degraded: full governed suite green (baseline at the qualification gate's parent, compared like-for-like); the
electronics-specific focused suites unchanged-passing; byte-parity differentials on electronics classification and
`/start` outcomes for a committed electronics corpus (the F002/F004 differential-sweep pattern is the precedent);
no change to activated-domain admission, labels, safety derivation, Path-N service, or deliverable output for
electronics inputs, except under an explicitly Owner-approved contract amendment.

## §11. Requirement 7 — Safety-cue family (governed treatment + explicit OPEN Owner decision)

Repository truth: the F001 seam makes safety-cue families per-domain and additive; Mechanical currently has none, and
`has_governed_safety_cue_family("mechanical") is False` truthfully yields empty signals plus the capability-scope
statement. The CF-5 closure carries "per-domain P9-QS qualification (including the safety-cue-family-before-activation
input)" as a pre-activation prerequisite — i.e. repository truth REQUIRES the safety-cue-family question to be
answered before ACTIVATION, but does NOT itself decide whether qualification may complete with an empty family.
The advisory review's view (a physical-hazard domain should not activate with an empty family) is NOT adopted blindly.

**OWNER DECISION REQUIRED — `OD-M2` (OPEN; surfaced, not decided here):** choose one governed treatment:
- **(a)** a governed Mechanical safety-cue family (failure/subject/consequence/context vocabulary, provenance-tagged,
  evidence-tested through the existing F001 seam) is REQUIRED before `mechanical` may be declared P9-QS qualified; or
- **(b)** qualification may complete with the truthful empty-family state, but a governed Mechanical family is REQUIRED
  before ACTIVATION (the repository's existing pre-activation input made concrete); or
- **(c)** another explicitly governed treatment defined by the Owner.
Until OD-M2 is decided, no Mechanical qualification declaration may be made — the decision is a hard input to §15's
evidence definition. This contract records the trade space without recommending engineering policy it cannot verify.

## §12. Requirement 8 — Path-N / question content (D-GMPR coupling NOT absorbed)

Canonical Mechanical question ownership is the Domain-Pack `gap_type_mappings` (10 questions exist). Qualification
requires evidence that pack-owned Mechanical question content is qualification-grade: coverage of the declared gap
types, non-specialist accessibility where served through Path-N-style flows, truthful calibration to declared
capabilities, and provenance. **Boundary (binding):** the `engine/path_n_questions.py` seam is Electronics-OWNED
content behind the open D-GMPR-01-D-D3 coupling; this contract does NOT close, absorb, or modify that coupling. If
Mechanical non-specialist Path-N service requires seam work, that work happens at the D-GMPR coupling's own gate (or a
jointly-authorized gate that explicitly names both owners) — Mechanical qualification evidence may DEPEND on that
gate's outcome but may not perform it. The precise boundary: pack-content sufficiency = THIS contract; seam
remediation = D-GMPR lane.

## §13. Requirement 9 — Public label / localization (CF-2 NOT over-closed)

Qualification-for-activation requires a truthful Tier-1 Mechanical public label in the EXISTING
`web/domain_label.py::_PUBLIC_DOMAIN_LABELS` owner, with EN and AR canonical variants per the D-P6-16/17/18 language
decisions (selected-UI-language rendering; no simultaneous EN+AR; no auto-switching), replacing the current truthful
Tier-0 neutral fallback for `mechanical` only when the label becomes truthful (i.e. not before activation-readiness).
No Tier-2/3/4 professional/specialist/certification claim. **CF-2 remains OPEN and separate:** general public-message
truthfulness beyond `/start` (including the CLI's electronics-pinned copy, CF-6/CF-2 lanes) is NOT discharged, closed,
or absorbed by Mechanical labeling work; only the Mechanical-label addition itself is in this contract's future scope.

## §14. Requirement 10 — Output truthfulness (known/unknown behavior)

Mechanical outputs (questions, gaps, deliverables, capability-scope statements) MUST NOT overstate feasibility,
safety, manufacturability, validation, certification, regulatory acceptance, or physical correctness. Required
behavior: explicit evidence-vs-assumption distinction (existing owners, P9-QS §5); explicit Known-Unknown
representation; truthful "cannot be established in software" routing toward the separately governed physical-validation
lineage (WS-PFV-001: simulation/prototype/laboratory/certification/specialist review — referenced, NOT executed or
absorbed); the F001-style truthful capability-scope statement whenever a governed capability (e.g. safety-cue family)
is absent; and consistency with the D4 Amendment 01 principle that per-domain acceptability claims never imply
system-level claims.

## §15. Requirement 11 — Qualification evidence package (exact; per P9-QS §7)

`mechanical` may be declared **P9-QS QUALIFIED** only by a future, separately-authorized qualification gate presenting
ALL of (as applicable per the finally-decided OD-M2):

1. the §5 capability declaration, §6 real rule nuances, and §7 coverage declaration, committed through existing owners
   with provenance;
2. focused deterministic tests for every declared capability, gap type, rule nuance, and boundary class (§9), including
   negative tests and the honest-precondition pattern (inputs proven not to pass for the wrong reason);
3. mutation/adversarial probes on the new Mechanical evidence (each governed behavior demonstrably load-bearing —
   the F002/F004 mutation-probe precedent), including signal-quality probes (§8);
4. full governed-suite regression green plus the §10 electronics non-degradation differentials (byte-parity corpus
   evidence);
5. benchmark/representative-journey cases for clearly-Mechanical ideas within declared scope (P9-QS §6 positive
   journeys), with truthful refusal/degradation outside declared scope;
6. provenance evidence per §4b/D13 and verbatim-provenance owners;
7. deterministic behavior evidence (no randomness/time dependence in qualification-relevant paths);
8. Web/UI and CLI consistency evidence where surfaces are touched by later authorized gates (activation-derived
   admission per D-CF5-F002-01; fail-closed dispatches; truthful labels per §13) — without absorbing CF-6/CF-2;
9. the OD-M2-decided safety-cue-family evidence (§11);
10. a qualification record proving each item above with exact SHAs, then the governed lifecycle for that record.
Partial evidence NEVER supports a qualification claim; replay/greenness alone is not proof (CLAUDE.md).

## §16. Requirement 12 — Activation separation (explicit)

**Mechanical qualification does NOT activate `mechanical`.** Activation remains a future, separate, explicitly
Owner-authorized §5-I2 allowlist gate, and remains BLOCKED behind the existing prerequisites independent of this
contract: remaining CF-6, CF-2, the open D-GMPR `path_n_questions` coupling, per-domain P9-QS qualification itself,
NMF-1/FU-1 pre-activation test-hardening disposition, D8 if IoT is implicated, and explicit Owner activation
authorization. Nothing in this contract, its future implementation gates, or a future qualification declaration moves
`activated_domains()` off `['electronics_electrical']`.

## §17. Requirement 13 — Future-extensibility claim boundary

A successful Mechanical qualification proves ONLY qualification-extensibility of an already-recognized specialist
domain. It does NOT prove: new-domain registration extensibility (the recognized-registry set is unchanged throughout);
fifth/future-domain admission; D4 multi-domain composition; IoT disposition (D8); or universal domain scalability.
Independent future testing of genuinely-new-domain registration extensibility is explicitly preserved as separate,
not-yet-authorized work; this contract creates no precedent narrowing it.

## §18. Requirement 14 — D4 Amendment 01 boundary

`D-GMPR-01-D-D4` Amendment 01 is authoritative (scope meaning: governed system-level engineering compatibility across
participating domains; per-domain PASS ≠ system-level PASS) but D4 remains REGISTERED / NOT AUTHORIZED. Under this
contract, mixed-domain inputs may be used ONLY to test classification/admission boundaries (§9). It is FORBIDDEN to
implement cross-domain system composition, system-level engineering-compatibility evaluation, shared-constraint
propagation, or unified multi-domain assessment. Those remain D4, sequenced after ≥2 activated domains, which
Mechanical qualification alone does not reach.

## §19. Requirement 15 — Verified latent-risk register (classified; no duplicate ownership)

| # | Advisory observation | Repository verification | Classification |
|---|---|---|---|
| 1 | "Electronics-specific plural alias assumptions in shared core" | **NOT VERIFIED as stated**: the F003 matcher is domain-generic (whole-token; bounded final-token `+s`/`+es`). Verified adjacent facts: alias inventories are per-pack data (electronics has shorthands; mechanical only `["mechanical"]`); the web layer's `_LAY_ELECTRICAL_WORDS` is electronics-only lay vocabulary (already-fenced observation) | Mechanical vocabulary-adequacy evidence under the generic matcher = **this contract (§8.3)**; `_LAY_ELECTRICAL_WORDS` and CLI copy = **separate existing owners (CF-6/CF-2 lanes)** |
| 2 | Pack `weight` metadata vs classifier behavior mismatch | **VERIFIED**: `classify_domain` scores by matched-set cardinality; `weight`/`layer` unused at classification time | **This contract (§8.4)** as a truthfulness disposition required for Mechanical qualification; cross-pack generality surfaced to the Owner here — no new tracker created |
| 3 | Mechanical pack placeholder-quality content | **PARTIALLY VERIFIED**: real provenance-tagged signals/questions (not placeholders), but degenerate rule nuances, no coverage declaration, substance depth 17 vs 53 | **This contract (§5–§7)** — qualification gap-closure evidence |
| 4 | No Mechanical safety-cue family | **VERIFIED** (`_DOMAIN_CUE_FAMILIES` electronics-only) | **This contract (§11) + OPEN Owner decision OD-M2**; activation-side input already registered by CF-5 closure carry-forward (existing owner; not duplicated) |
| 5 | No Mechanical Path-N content | **VERIFIED at the seam** (Electronics-owned artifact; non-electronics served `None`); pack owns 10 questions of unproven qualification grade | Pack-content sufficiency = **this contract (§12)**; seam remediation = **separate existing owner (open D-GMPR-01-D-D3 coupling)** |
| 6 | No Mechanical truthful public label/localization | **VERIFIED** (`_PUBLIC_DOMAIN_LABELS` electronics-only; mechanical → truthful neutral Tier-0 fallback) | Mechanical Tier-1 EN/AR label = **this contract (§13)** at a future authorized gate; general public-message truthfulness = **separate existing owner (CF-2, OPEN)** |

None of the above is an activation blocker beyond the blockers that already exist (§16); none is closed, moved, or
re-owned here; NMF-1/FU-1 remain in their registered lane (non-blocking pre-activation test-hardening).

## §20. P9-QS completeness-dimension mapping

Engineering-knowledge quality (§5, §6, §8); technical truthfulness / known-unknowns (§5, §7, §14); recognition/
classification/qualification/activation boundaries (§2, §4, §16); backward compatibility / prior-domain safety (§10,
§9 legacy cases); deterministic runtime behavior (§15.7); governance consistency (§21–§22); test sufficiency incl.
negative/mutation/adversarial (§9, §15.2–15.3); UI/Web admission consistency (§15.8, D-CF5-F002-01 reuse); cross-module
coupling (§12 D-GMPR boundary; §8 shared-core neutrality); anti-duplication / canonical-owner reuse (§21);
retrospective architecture-audit obligations/state (CF-5 FORMALLY CLOSED; its carry-forwards preserved in §16/§19).
**Not material here, stated why:** performance/observability — no runtime change occurs in this gate and Mechanical
qualification adds no new runtime surface class beyond existing deterministic evaluation (any later gate that
materially changes hot paths must present its own evidence); security/abuse — no new input surface, privilege, or
storage is created by qualification content (existing security containment tests remain binding regression evidence).

## §21. Anti-duplication / canonical owners reused (D-FPC-MAP-06)

Registry/recognition: `engine/domain_registry.py` (§5-I1). Activation: `engine/domain_activation.py` (§5-I2).
Classification: `engine/domain_rules.py::classify_domain` (+ F003/F004 semantics). Safety cues: `engine/safety_signal.py`
F001 seam. Questions: Domain-Pack `gap_type_mappings`; Path-N seam stays D-GMPR-owned. Labels: `web/domain_label.py`.
Admission: D-CF5-F002-01 activation-derived `/start`. Evidence/provenance: `record_contract`/`record_store`/D13.
Physical validation: WS-PFV-001 (referenced only). Signal-quality flags: AB-006 recorded candidates (reused, not
reopened). Composition: D4 (untouched). **No new registry, ledger, engine, framework, tracker, workstream, or second
canonical owner is created by this contract.**

## §22. Change surface of THIS gate, sequencing, and stop conditions

THIS gate changes only: this NEW contract record; `OWNER_DECISION_REGISTER.md` (the single `D-P9-MECH-01` row + its
section); `ACTIVE_EXECUTION_ROADMAP.md` (append-only entry); `ACTIVE_INCREMENT_CONTRACT.md` and
`CURRENT_PROJECT_STATE.md` current-truth sync. **Sequencing:** this contract becoming authoritative does NOT authorize
its own implementation; each future increment (capability declaration, nuances/coverage, signal-quality evidence,
safety family per OD-M2, boundary tests, qualification record) requires separate explicit Owner authorization under
the governed lifecycle. **Stop conditions:** any need to touch a forbidden surface, any sign a required owner must be
duplicated, any OD-M2-dependent ambiguity, or any evidence that Mechanical content cannot be made truthful within
declared scope → STOP — CONTRACT AMENDMENT / OWNER DECISION REQUIRED. **Next required gate: Mandatory Grill on this
exact candidate**, then the governed lifecycle through Owner-side publication, PR, and post-merge verification.
