# P9-MECH-I4 — Terminal Cross-Domain Boundary-Evidence Corpus (§9) — Bounded Increment CONTRACT (governance-only contract gate)

**Status of THIS record:** governance/documentation-only **INCREMENT-CONTRACT CANDIDATE** under the AUTHORITATIVE
P9-MECH-QC contract, after the AUTHORITATIVE P9-MECH-I1/I2/I3 implementations. It becomes AUTHORITATIVE only through
the governed lifecycle (Mandatory Grill → independent external exact-candidate review → Owner acceptance →
SHA-preserving publication → PR → create-a-merge-commit → post-merge verification). **It implements nothing in this
gate** and, once authoritative, authorizes ONLY the bounded P9-MECH-I4 implementation increment defined below (itself
requiring separate explicit Owner authorization). It does NOT declare `mechanical` qualified, does NOT activate
anything, and records NO new Owner decision (**`OWNER_DECISION_REGISTER.md` UNCHANGED**). **DOCUMENTED NO-VALID-RED —
GOVERNANCE-ONLY CONTRACT GATE.**

## §1. Authoritative base and dependency proof

Base: `b0be35bb8771aea6ed7edbebcf13b5d106227dbc` (merge of `b99dd2f6` + accepted I3 implementation `32165caf`, merge
tree `551a03e1` == candidate tree; freshly fetched; 0 newer; clean tree). Dependency proof for THIS gate, from
committed truth (not summaries): the authoritative I3 contract's obligation map explicitly deferred the §9 terminal
corpus "after I3 freezes signal content (a terminal corpus built before content changes would immediately go stale)".
I3 is now merged: the Mechanical signal inventory is authoritative and equality-pinned (18 classification / 15
substance signals incl. the multi-word `locking mechanism`; dispositions recorded; engine byte-frozen; suite
2495/3/1/0). **§9 is therefore the unique remaining UNBLOCKED qualification-lane obligation** — §12 stays
blocked-side (open D-GMPR seam), §15/§16 are terminal and require §9, §11/§13 are pre-activation, the dormant-weight
cross-pack residual is shared-core-owned, and thermal is THERM-01-owned.

## §2. Remaining-obligation map (after I3; complete classification)

| Obligation | Classification |
|---|---|
| §5 + §7 declarations | **DISCHARGED (I1)** |
| §6 rule nuances | **DISCHARGED (I2)** |
| §8 signal-quality / AB-006 dispositions | **DISCHARGED (I3**, merge `b0be35bb`**)** |
| §8.4 dormant-`weight` | Mechanical share **DISCHARGED (I1 annotation**, closure-gate confirmation pending**)**; cross-pack residual **shared-core owner (NOT Mechanical)** |
| **§9 terminal cross-domain boundary corpus** | **STILL REQUIRED — NEXT (THIS contract)** |
| §12 question-content sufficiency | **PARTIALLY DISCHARGED context / BLOCKED-side**: pack questions exist (I1-declared scope), but qualification-grade sufficiency validation through the Path-N seam remains blocked by the OPEN D-GMPR coupling (separate owner) |
| §13 Tier-1 EN/AR label | **PRE-ACTIVATION only** |
| §11 safety-cue family | **PRE-ACTIVATION only** (OD-M2 B-hardened; clause 3 activation blocker) |
| §15 evidence package + §16 closure | **TERMINAL — still required** (assembleable only after §9 and the §12 disposition; conditional on OD-M2 clauses) |
| §10 electronics non-degradation + provenance/truthfulness | **CONDITIONAL — every increment** (binds I4) |
| Thermal | **Separate owner (THERM-01, future-only)** |

## §3. The P9-MECH-I4 implementation increment — exact definition

```
INCREMENT CONTRACT — P9-MECH-I4 Terminal Boundary-Evidence Corpus   [implementation NOT started]
Responsibility:   Create the TERMINAL, committed §9 cross-domain boundary-evidence corpus for `mechanical` as a
                  deterministic, self-contained focused test surface — EVIDENCE ONLY. Zero runtime change of any
                  kind: no pack edit, no engine edit, no web/CLI edit, no provenance edit (no new pack content
                  exists to source). The corpus binds to the now-authoritative I3 signal inventory and freezes it
                  as this corpus's validity scope: any FUTURE signal-inventory change invalidates the terminal
                  corpus and requires its re-validation at that future gate (recorded in the corpus file header
                  and the closure record).
Allowed paths:    NEW tests/test_p9_mech_i4_boundary_corpus.py (the corpus lives in the test file — no new
                  framework, no data files, no generator);
                  governance sync at closure only (roadmap/AIC/CPS + closure record).
Forbidden paths:  EVERYTHING else — engine/**, web/**, scripts/**, ALL domain packs (mechanical included —
                  byte-frozen this increment), domains/domain_provenance.json, all existing test files
                  (expected prior-freeze reconciliation = NONE, because nothing runtime-visible changes; if
                  implementation discovers any existing-test conflict, that is an unexplained differential →
                  STOP — CONTRACT AMENDMENT), schemas/, OWNER_DECISION_REGISTER.md, CI.
```

## §4. Required corpus classes (each explicitly present and labeled; P9-QS §6 minimum + I3-preserved findings)

1. **Positive representative Mechanical journeys** — clearly-Mechanical ideas within I1 declared scope classify
   `single mechanical` (incl. multi-word `locking mechanism` phrasing and its bounded final-token plural).
2. **Mechanical vs Electronics hard cases** — incl. electro-mechanical prose where the activated-tie/precedence rules
   truthfully yield electronics, and clearly-electronics prose that must NOT attract mechanical.
3. **Mechanical vs Software hard cases** — incl. the I3-corrected classes (generic `mechanism` prose, software
   locking prose) pinned at their corrected truthful outcomes.
4. **Mechanical vs Medical hard cases** — incl. clinical valve/pressure prose truthfully medical via medical's own
   signals and the medical>mechanical precedence.
5. **EXPLICIT tie cases** (I3-preserved finding): activated-tie class (mech+electronics → electronics via D3-D);
   legacy zero-activated precedence classes (mech+software → mechanical; mech+medical → medical); at least one
   three-way composition; ties must be asserted as ties-by-construction (score parity justified in comments), never
   incidental.
6. **Mixed-domain cases** — multi-domain prose exercising the F004 arms as they truthfully resolve today (no D4
   semantics invoked or simulated: mixed cases test CLASSIFICATION boundaries only).
7. **NONE / unknown / generic-ambiguity cases** — non-domain text, generic engineering language, empty/whitespace
   and irrelevant input → NONE; documented I3 residuals (e.g. tournament-bracket prose) pinned AT their recorded
   residual outcomes with comments marking them as known documented limitations, not endorsements.
8. **Adversarial synonyms/paraphrases** — mechanical concepts phrased without inventory tokens (truthful NONE today
   — honest recall boundary, labeled as such) and sibling concepts phrased near mechanical vocabulary.
9. **Backward compatibility** — the corrected EIGHT-text legacy classifier corpus (I3-preserved finding: 8, not 10)
   embedded verbatim and pinned unchanged.
10. **Sibling non-degradation** — electronics/software/medical single-domain corpora pinned; sibling pack sha256
    pins; engine byte-hash pins (`domain_rules.py`, `progression_loop.py`) so no classifier/tie-semantics change can
    ride along; recognized-set, activation (`['electronics_electrical']`), and mechanical safety-family-absent pins.
11. **Recognition-vs-activation boundary** — classification-level evidence that `mechanical` outcomes remain
    recognized-not-activated (no admission change; evidence-only; the F002 activation-derived admission behavior is
    NOT re-tested here beyond classification outcomes — no web surface is touched).

## §5. Evidence rules, expected/forbidden differentials, and anti-gaming probes

**Expected runtime differential: ZERO** (evidence-only increment — proven by scope: no runtime file changes; the new
tests must pass against the UNCHANGED parent runtime). There is accordingly **no parent-RED requirement** — the
increment creates terminal evidence, corrects nothing; its integrity is protected instead by honest-precondition
rules and mutation probes: every expected label carries a truthfulness justification grounded in the packs' declared
context ownership and the governed precedence rules (comment-per-case or per-class); no case may pass for the wrong
reason (score-parity assertions for tie cases; explicit candidate-set checks where the arm matters).
**Forbidden:** any runtime/pack/engine/provenance edit; any existing-test modification; any corpus case whose label
cannot be truthfully justified; any duplication of the I1/I2/I3 pin surfaces beyond the §4.10 invariance pins that
the terminal corpus needs as its own validity anchors (referencing, not re-deriving, prior evidence).
**Mutation/adversarial probes (each must flip a specific pin RED; none retained):** m1 flip one corpus expected
label → its class pin RED; m2 tamper one byte of `engine/domain_rules.py` → engine hash pin RED; m3 tamper the
mechanical pack (one signal) → inventory/validity-anchor pin RED; m4 tamper one sibling pack byte → sibling pin RED;
m5 delete an entire corpus class → class-coverage completeness pin RED (the file pins its own class inventory);
m6 weaken a tie case to a non-tie (single-signal text) → the tie's score-parity precondition assertion RED.

## §6. Full verification, closure criteria, and boundaries

**Verification:** focused I4 corpus green on the unchanged runtime; I1/I2/I3 suites green unchanged; full governed
suite green (expected = parent baseline + the new corpus tests; exact counts reported); `git diff --check` clean;
scope proof (zero diff outside the single new test file + closure-time governance sync). **Closure criteria:** all
§4 classes present and green; mutation probes m1–m6 executed with right-reason RED and byte-verified restoration;
the corpus-validity scope statement recorded (bound to the exact I3 signal inventory); closure record merged and
post-merge verified. On I4 closure the remaining qualification-lane items are exactly: the §12 disposition
(blocked-side pending D-GMPR or an Owner-directed bounded alternative) and the terminal §15/§16 package/closure —
which this contract does NOT start, and which cannot complete while OD-M2 clause-2 conditions and the §12
disposition remain open. **Boundaries (nothing over-closed):** Mechanical remains NOT QUALIFIED and NOT ACTIVATED;
`_ACTIVATED_DOMAINS` untouched; classifier semantics and tie policy untouched; D-GMPR, CF-6, CF-2, safety family,
Tier-1 label, THERM-01, CAP-12/13, WS-PFV-001, dormant-weight cross-pack residual, D4, D8, Phase 10, PSRR,
deployment — all untouched with their existing owners. **STOP conditions:** any forbidden-path need; any
existing-test conflict; any label that cannot be truthfully justified; any pressure to alter tie policy or
vocabulary to make the corpus "pass" → STOP — CONTRACT AMENDMENT / OWNER DECISION REQUIRED.
**Next required gate: Mandatory Grill on this exact contract candidate.**
