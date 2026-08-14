# P9-MECH-I3 — Mechanical Signal-Quality / AB-006 Evidence & Disposition — Bounded Increment CONTRACT (governance-only contract gate)

**Status of THIS record:** governance/documentation-only **INCREMENT-CONTRACT CANDIDATE** under the AUTHORITATIVE
P9-MECH-QC contract, after the AUTHORITATIVE P9-MECH-I1 and P9-MECH-I2 implementations. It becomes AUTHORITATIVE only
through the governed lifecycle (Mandatory Grill → independent external exact-candidate review → Owner acceptance →
SHA-preserving publication → PR → create-a-merge-commit → post-merge verification). **It implements nothing in this
gate** (ZERO runtime/test/pack/registry/Web/CLI diff in this candidate) and, once authoritative, authorizes ONLY the
bounded P9-MECH-I3 implementation increment defined below — which itself requires separate explicit Owner
authorization. It does NOT declare `mechanical` qualified, does NOT activate anything, and records NO new Owner
decision (**`OWNER_DECISION_REGISTER.md` UNCHANGED**). **DOCUMENTED NO-VALID-RED.**

## §1. Authoritative base and repository-first reconstruction (verified mechanically)

Base: `4037a67d037287c3244129a41ba2b14dba139a0d` (merge of `6881db34` + accepted I2 implementation `3d51bb1c`, merge
tree `5f2860b3` == candidate tree; freshly fetched; 0 newer; clean tree).

**Canonical consumed-field map for Mechanical classification (traced, not inferred):**
`classify_domain(idea_text)` → `_TOKEN_RE.findall(lower)` (normalization) → per-pack
`_present_signal_count(pack, tokens, token_set)`, which consumes **ONLY `classification_signals[].signal` strings**
under the authoritative F003 matching semantics (whole-token; bounded final-token `+s`/`+es` plural; same-domain
registered containment) → score = **matched-set cardinality** → tied set construction → D3-D activated-tie precedence
(§5-I2 policy) → F004 arms (sole-top SINGLE / bounded legacy-four precedence / `UNRESOLVED_NON_ACTIVATED_TIE`;
`AMBIGUOUS_TIE` activated-only; `MULTI_DOMAIN_NEEDS_D4` never produced) → `NONE` when the maximum score is 0.
**NOT consumed by `classify_domain`:** `weight`, `layer`, `provenance_ref`, `substance_signals`,
`gap_type_mappings`, `rule_nuances`, `aliases` (aliases are recognition/activation resolution inputs elsewhere).
**Separate runtime path:** `substance_signals[].signal` IS runtime-consumed — `engine/progression_loop.py::
assess_response` reads `get_substance_signals(domain)` for the answer-substance check. For `mechanical` this path is
**latent** today (no admitted session can carry `domain == "mechanical"` while unactivated: web admission is
activation-derived per D-CF5-F002-01 and the CLI refuses non-electronics), while classification outcomes for
mechanical-flavored text are **live** (guidance flavor via `/start` and CLI).

**Dormant `weight` reconstruction:** `weight` (and `layer`) exist on every classification signal of ALL FOUR v1.0
packs with differing value inventories (electronics 0.15–0.9; mechanical 0.4–0.9; software 0.4–0.8; medical 0.5–0.9);
NO runtime code reads them (classifier scores by cardinality; repo-wide grep clean); registry validation does not
interpret them; no test or governance record assigns them runtime meaning. **They are truly dormant cross-pack
metadata under the shared §5-I1 pack schema — a shared classifier-contract question, NOT Mechanical-owned.** The
Mechanical-side §8.4 truthfulness obligation (metadata must not imply unimplemented behavior in a qualified pack) is
**already discharged at the pack level by the merged I1 annotation** (`_governance_notes.p9_mech_i1_declarations`:
"dormant per-signal weight/layer metadata remains dormant and is not implied runtime-active"), subject to confirmation
at the future qualification-closure gate. The residual cross-pack disposition (leave-documented / normalize / remove /
activate / other) is a **separate shared-core governance gate** and is NOT absorbed here; activation of weight
semantics would change classifier behavior for every pack and requires its own explicit Owner-authorized contract.

**AB-006 reconstruction:** AB-006 was the architectural-debt Domain Signal Quality initiative, **CLOSED WITH DEFERRED
ITEMS** (`docs/governance/AB-006_CLOSURE_REPORT.md`); its live recorded inputs sit in the mechanical pack itself
(`_governance_notes.ab006_candidates` + per-signal context notes) and in `domains/domain_provenance.json`
(`mechanical:PR001` notes). Flagged Mechanical inventory: **`mechanism`, `force`, `bar`, `bracket`, `fastener`,
`locking`** — "retained for behavioral equivalence; flagged for AB-006 Domain Signal Quality Review" — with recorded
deficiency characters: LOW SPECIFICITY / generic (`mechanism`: "arrangement of parts producing motion or force";
`force`: generic physical interaction; `bar`: explicitly "Ambiguous" — structural rod OR pressure unit), weakly
discriminative low-weight classification entries (`bracket` 0.5, `fastener` 0.4, `locking` 0.4 — e.g. `locking` is
common software vocabulary), plus **declared CROSS-DOMAIN context-ownership signals** `valve` (also medical/process),
`pressure` (also medical/electronics), `compression` (also software data compression), `actuator` (also electronics)
whose context ownership is declared but never yet evidence-verified. Placement of flags: `mechanism`/`bracket`/
`fastener`/`locking` are classification signals (affect `classify_domain` candidate sets, tie composition, selected
domain, and NONE boundaries; `mechanism` additionally appears as a LOW-SPECIFICITY substance signal);
`force`/`bar` are substance-only signals (affect the latent mechanical answer-substance path); of the four declared
cross-domain signals, `valve` (0.8) and `actuator` (0.6) are ALSO classification signals while `pressure` and
`compression` are substance-only — all four carry context-ownership notes. This is the increment's
input inventory; AB-006 itself is NOT reopened as a tracker — its recorded flags are consumed as evidence inputs.

## §2. Remaining P9-MECH-QC obligation map (complete classification after I2)

| Obligation | Classification |
|---|---|
| §5 capability + §7 coverage declarations | **COMPLETE (I1)** |
| §6 qualification-grade rule nuances | **COMPLETE (I2**, merge `4037a67d`; accessor-invariant, runtime-inert disclosed**)** |
| §8 signal-quality / AB-006 evidence | **NEXT — THIS contract (P9-MECH-I3)** |
| §8.4 dormant-`weight` disposition | **Mechanical share: COMPLETE via the I1 pack-level annotation (closure-gate confirmation pending); cross-pack residual: BLOCKED by separate owner** (shared classifier-contract governance; NOT absorbed) |
| §9 cross-domain boundary-test evidence (terminal corpus) | **LATER** — after I3 freezes signal content (a terminal corpus built before content changes would immediately go stale); I3 carries its own working defect/differential corpus |
| §12 question-content sufficiency | **LATER / BLOCKED-side**: pack-content work is qualification-lane, but validation through the Path-N seam remains blocked by the OPEN D-GMPR coupling (separate owner; nothing newly unblocked) |
| §13 Tier-1 EN/AR label | **PRE-ACTIVATION only** |
| §11 safety-cue family | **PRE-ACTIVATION only** per OD-M2 B-hardened (no contradiction found) |
| §15 evidence package + §16 closure | **TERMINAL** |
| §10 electronics non-degradation | **CONDITIONAL — every increment** (strongest form binds THIS increment: see §6) |
| Provenance/truthfulness (§4b, §5.x) | **CONDITIONAL — every increment** |
| Thermal | **Separate owner (THERM-01, future-only)** — untouched |

## §3. Selection and the A-vs-B-vs-C decision

Candidates: **A** signal-quality/AB-006; **B** dormant-weight disposition; **C** combined A+B; **D** terminal boundary
corpus; **E** question sufficiency; **F** governance-reconciliation-only gate; **G** other (none evidenced).
**A-vs-B-vs-C answer: TWO SEPARATE responsibilities — and B is not even next.** (i) Signal-quality CAN be completed
truthfully while `weight` stays dormant: the classifier scores by cardinality, so weight metadata has zero effect on
any signal-quality evidence; the dormancy is already truthfully annotated in the pack (I1), so its presence does not
mislead. (ii) `weight` is cross-pack shared-schema metadata — a Mechanical-only gate absorbing it would silently
govern every pack (the exact absorption failure the Grill must reject); its residual belongs to a separate shared-core
gate, with any semantic activation requiring explicit Owner authority. (iii) Combining A+B would couple a
Mechanical-content evidence increment to a shared-contract policy question with different ownership, risk class, and
authority — not one coherent responsibility. **D** before A would produce a stale terminal corpus; **E** remains
blocked-side; **F** has no repository-evidenced need. **Selected: P9-MECH-I3 = A alone.** It is the last open
qualification-lane content obligation whose dependencies (I1 declared scope; I2 frozen nuances) are all satisfied.

## §4. The P9-MECH-I3 implementation increment — exact definition

```
INCREMENT CONTRACT — P9-MECH-I3 Signal-Quality / AB-006 Evidence & Disposition   [implementation NOT started]
Responsibility:   Evidence-based disposition of the recorded AB-006-flagged Mechanical signal-quality candidates
                  (mechanism, force, bar, bracket, fastener, locking) and evidence verification of the declared
                  cross-domain context ownerships (valve, pressure, compression, actuator), driven by a
                  difficult-case defect corpus — with bounded, evidence-derived content corrections in the
                  mechanical pack ONLY. NOTHING is pre-decided here: per signal, the implementation outcome MUST be
                  one of — retain-with-evidence / narrow / replace / remove / add-better-discriminative-signal /
                  reclassify (classification↔substance/context) / no-safe-correction-possible — each recorded with
                  its supporting evidence cases.
Evidence prereq:  Parent RED (see §5) proving REAL defects before any change; no change without a defect case.
Allowed paths:    domains/mechanical/domain.json — classification_signals and substance_signals entries ONLY as
                  evidence-derived dispositions require, plus ONE additive _governance_notes disposition record
                  (per-signal outcomes + evidence refs; ab006_candidates historical note preserved);
                  domains/domain_provenance.json — additive record(s) only (e.g. mechanical:PR004 for any ADDED
                  signal's source; existing records byte-untouched);
                  NEW tests/test_p9_mech_i3_signal_quality.py (corpus embedded in the test file — no new framework);
                  governance sync at closure only.
Forbidden paths:  engine/** (F003 matcher, F004 arms, D3-D precedence, tie handling, get_active_rules,
                  get_substance_signals, progression_loop — ALL byte-frozen), web/**, scripts/**, all other packs
                  (byte-frozen), mechanical fields OTHER than the two signal lists + the one note (rule_nuances (I2),
                  capability/coverage declarations (I1), gap_type_mappings, aliases, journey_extension — byte-frozen;
                  if an evidence-justified disposition would falsify a declaration statement → STOP — CONTRACT
                  AMENDMENT), the weight/layer values of RETAINED signals (byte-frozen; no normalization — cross-pack
                  owner; any ADDED signal carries weight/layer ONLY as dormant metadata consistent with the pack's
                  existing dormant pattern and the I1 annotation), OWNER_DECISION_REGISTER.md (ZERO ODR diff), CI.
```

## §5. Parent RED requirement (real defects, not future-keyword assertions)

The implementation MUST first commit a difficult-case corpus and demonstrate on the CLEAN PARENT at least the
following classes, with each later content change traceable to at least one failing/deficient case: Mechanical-vs-
Electronics hard cases; Mechanical-vs-Software hard cases (e.g. `locking` in concurrency prose); Mechanical-vs-Medical
hard cases (e.g. `valve`/`pressure` in clinical prose); mixed-domain concepts; generic engineering language that
should NOT attract Mechanical (e.g. `mechanism`/`force`/`bar` in non-mechanical prose — false-attraction defects);
genuinely-Mechanical concepts the current inventory misses (missed-concept defects, if any are evidenced);
adversarial synonyms/paraphrases; ambiguous terms (`bar` unit-vs-rod); empty/irrelevant input; and none/unknown cases
that must stay NONE. **RED is defined as demonstrated misclassification, false attraction, missed concept, or
ambiguity — measured against truthful expected labels justified from the packs' own declared context ownership — NOT
as "the future keyword list is absent."** Tests that merely assert desired future keywords are forbidden. If the
corpus proves NO material defect for a flagged signal, the truthful outcome is retain-with-evidence — that is a valid,
non-failing disposition.

## §6. Objective acceptance criteria, expected and forbidden differentials

**Expected runtime differential: BOUNDED, CATEGORIZED, NON-ZERO ONLY WHERE EVIDENCE REQUIRES.** Every parent-vs-
candidate delta on the committed corpora MUST be categorized to exactly one recorded disposition with ZERO
unexplained deltas (the F004 categorized-differential precedent). Deltas may appear ONLY in: (i) classification
outcomes of texts matching a corrected/added/removed mechanical signal; (ii) the latent mechanical answer-substance
path. **Forbidden differentials (hard invariants):** the electronics-only, software-only, and medical-only
single-domain corpora — outcomes byte-identical; every committed NONE case stays NONE; the F003 matching semantics
and F004/D3-D tie ARCHITECTURE — byte-frozen engine (any tie-break or matcher change is a separate classifier-owner
gate); the OD2-preserved legacy-four precedence RULE — untouched; any legacy-four tie-outcome flip caused by a
disposition MUST be individually disclosed in the differential, and if it would contradict the preserved OD2 rule
semantics (rather than merely re-score corrected vocabulary) → STOP — OWNER DECISION REQUIRED; `activated_domains()`
and admission behavior for non-mechanical inputs — unchanged. **Anti-win-rate rule (binding):** signal quality ≠
keyword count and ≠ Mechanical win-rate. No signal may be added merely to increase Mechanical scores; every ADDED
signal requires discriminative evidence (cases it correctly captures AND cases it correctly does not capture),
provenance, and a context note; the final inventory is equality-pinned (anti-stuffing); domain neutrality is a
protected property.

## §7. Test / evidence requirements (proportionate; all load-bearing)

Focused tests (NEW file): exact final classification-signal and substance-signal inventory equality pins
(anti-stuffing/anti-paraphrase — the proven I1/I2 pattern); per-flagged-signal disposition record pin (all six AB-006
flags + four cross-domain ownerships dispositioned; each maps to evidence cases); corpus outcome pins in BOTH
directions (defect cases now truthful; protected cases unchanged); none/unknown pins; other-pack byte pins;
frozen-mechanical-field canonical-hash pins (declarations, nuances, gap types, aliases, retained weight/layer);
engine-file byte pins for `domain_rules.py` and `progression_loop.py` (hash-frozen — no engine change rides along);
activation + safety-family + recognized-set pins; deterministic repeated classification. Differential sweep: parent
worktree vs candidate over the full committed corpus + the established 10-text legacy corpus, categorized, ZERO
unexplained. Full governed suite; `git diff --check`. NOT required (with reason): benchmark re-runs (scoring engine
untouched; classification-corpus differential is the stronger targeted evidence), UI/Playwright (no web change).

## §8. Mutation / adversarial probes (each must flip a specific pin RED; none retained)

m1 add an unjustified signal (not in the approved final inventory) → inventory equality pin RED; m2 remove a
disposition record entry → disposition pin RED; m3 re-introduce a removed/narrowed ambiguous signal → inventory pin
RED; m4 alter a retained signal's weight value → frozen-metadata pin RED; m5 tamper one byte of the electronics pack →
byte pin RED; m6 flip one corpus expected label to game a defect → corpus pin RED (the defect case's truthful-label
justification is part of the recorded evidence); m7 strip a new signal's provenance/context → provenance pin RED;
m8 modify `engine/domain_rules.py` (any byte) → engine hash pin RED; m9 remove the disposition governance note →
note pin RED; m10 adversarial paraphrase overclaim in the disposition note (capability language, e.g. claiming
improved "accuracy guarantees") → note equality/content pin RED.

## §9. Boundaries, STOP conditions, closure

Completing I3 does NOT declare Mechanical qualified (§9-terminal corpus, §12, §15/§16 remain; OD-M2 clause-2 bar
stands) and does NOT activate anything (`activated_domains() == ['electronics_electrical']`; first new-domain
activation remains BLOCKED incl. OD-M2 clause 3). Anti-duplication: shared-core classifier files byte-frozen (their
owner is the classifier lane, not Mechanical qualification); AB-006 consumed as recorded input, not reopened;
dormant-weight cross-pack residual stays with its shared owner; D-GMPR, CF-6, CF-2, THERM-01, CAP-12/13, WS-PFV-001,
D4, D8 untouched. **STOP conditions:** any forbidden-path need; any engine change pressure; any declaration-falsifying
disposition; any OD2-contradicting precedence effect; any disposition requiring cross-pack edits; any Owner-policy
question surfacing (e.g. a defect fixable only by weight activation) → STOP — CONTRACT AMENDMENT / OWNER DECISION
REQUIRED. **Closure:** via the increment's own evidence package (§5–§8), freeze, Grill, independent review, Owner
acceptance, merge, post-merge verification, and a closure record; closing I3 authorizes NO later increment.
**Next required gate: Mandatory Grill on this exact contract candidate.**
