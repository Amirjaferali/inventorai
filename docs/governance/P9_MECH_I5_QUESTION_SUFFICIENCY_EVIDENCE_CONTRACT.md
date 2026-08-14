# P9-MECH-I5 — §12 Question-Content Sufficiency Evidence + D-GMPR Dependency Disposition — Bounded Increment CONTRACT (governance-only contract gate)

**Status of THIS record:** governance/documentation-only **INCREMENT-CONTRACT CANDIDATE** under the AUTHORITATIVE
P9-MECH-QC contract, after the AUTHORITATIVE P9-MECH-I1/I2/I3/I4 implementations. It becomes AUTHORITATIVE only
through the governed lifecycle (Mandatory Grill → independent external exact-candidate review → Owner acceptance →
SHA-preserving publication → PR → create-a-merge-commit → post-merge verification). **It implements nothing in this
gate** and, once authoritative, authorizes ONLY the bounded P9-MECH-I5 implementation increment defined below (itself
requiring separate explicit Owner authorization). It does NOT declare `mechanical` qualified, does NOT activate
anything, does NOT close/absorb/modify the D-GMPR coupling, and records NO new Owner decision
(**`OWNER_DECISION_REGISTER.md` UNCHANGED**). **DOCUMENTED NO-VALID-RED — GOVERNANCE-ONLY CONTRACT GATE.**

## §1. Authoritative base and decisive reconstruction (verified mechanically at this exact base)

Base: `c7c9e413ac142a919b68868280cdddc5af8dce39` (merge of `6414581910…` + accepted I4 implementation `3fe23a8c`,
merge tree `8f321993` == candidate tree; freshly fetched; 0 newer; clean tree; suite 2515/3/1/0).

- **The D-GMPR blocker is REAL in current code:** `engine/path_n_questions.py` remains Electronics-OWNED — a
  non-electronics domain identity receives `None` (`:92-93`), so the committed non-specialist Path-N artifact cannot
  serve Mechanical; the seam's remediation remains the OPEN `D-GMPR-01-D-D3` coupling's own gate (separate owner;
  MANDATORY before first non-electronics activation per the D3 lineage — it therefore sits on the PRE-ACTIVATION
  path regardless of this contract).
- **The canonical pack-question service path is domain-generic and WORKS for `mechanical` TODAY:**
  `engine/domain_rules.get_domain_question(domain, gap_type, iterations_open)` reads the pack's own
  `gap_type_mappings` (questions text, ordered, index clamped to the last question; unknown gap → `None`) and is
  runtime-consumed at `engine/progression_loop.py:243`. Mechanically proven live at this base: mechanical questions
  serve correctly through it. Like the substance path, it is LATENT for mechanical while unactivated (no admitted
  session can carry the domain), which affects reachability, not evidence validity.
- **Consequence — §12 splits exactly as P9-MECH-QC §12 anticipated:** (a) **pack-content sufficiency** is
  Mechanical-owned and EXECUTABLE NOW through the canonical generic path; (b) the **non-specialist Path-N-service
  component** is BLOCKED by the D-GMPR seam and may only be dispositioned (recorded as a dependency), never performed
  here ("Mechanical qualification evidence may DEPEND on that gate's outcome but may not perform it").
- **I4 corpus terminality interaction:** the merged I4 terminal corpus anchors its validity to the mechanical pack's
  byte hash. THIS increment therefore touches NO pack bytes — it is evidence + disposition only. If its evidence
  later proves a question-content defect requiring pack changes, that is a SEPARATE future bounded content gate which
  must then re-validate the I4 corpus and reconcile the I2/I3/I4 freeze pins under its own contract (expected
  prior-freeze reconciliation for THIS increment = NONE; any conflict → STOP).

## §2. Remaining-obligation map (after I4; complete classification)

| Obligation | Classification |
|---|---|
| §5+§7 declarations; §6 nuances; §8 signal quality; **§9 terminal boundary corpus** | **DISCHARGED** (I1 / I2 / I3 / **I4**, merge `c7c9e413`) |
| §8.4 dormant-`weight` | Mechanical share **DISCHARGED** (I1 annotation; closure confirmation pending); cross-pack residual **shared-core owner** |
| **§12(a) pack-content sufficiency evidence** | **OPEN AND EXECUTABLE NOW — NEXT (THIS contract)** |
| **§12(b) non-specialist Path-N service for Mechanical** | **BLOCKED by D-GMPR** (`path_n_questions.py` seam; separate owner; pre-activation-path member via the D3 lineage) — dispositioned, not performed, by this increment |
| §15 evidence package + §16 closure | **TERMINAL** — after §12(a) evidence + the recorded §12(b) disposition, the package becomes assembleable subject to OD-M2 conditions |
| §11 safety-cue family; §13 Tier-1 EN/AR label | **PRE-ACTIVATION only** (OD-M2 B-hardened; label at activation-readiness) |
| §10 non-degradation + provenance/truthfulness | **CONDITIONAL — every increment** (binds I5) |
| Thermal / composition / IoT | **Future-only / separate owners** (THERM-01; D4 REGISTERED-NOT-AUTHORIZED; D8 Owner-reserved) |

**Selection.** Option **A-with-recorded-disposition**: a Mechanical §12 gate is executable NOW for component (a),
with component (b) formally recorded as D-GMPR-blocked. Rejected: **B** (D-GMPR-first — not dependency-required for
(a); shared-core owner; already mandatory pre-activation, so sequencing it before (a) would idle the qualification
lane without need); **pure disposition (C alone)** (would leave (a) undischarged and §15 stuck for no reason);
**D** (no other evidence-proven gate exists — §2 exhausts the obligations).

## §3. The P9-MECH-I5 implementation increment — exact definition

```
INCREMENT CONTRACT — P9-MECH-I5 §12(a) Question-Sufficiency Evidence + §12(b) Dependency Disposition
                                                                     [implementation NOT started]
Responsibility:   EVIDENCE ONLY (zero runtime/pack/provenance/engine/existing-test change):
                  (a) a committed, deterministic evidence surface proving — or truthfully refuting — that the
                      mechanical pack's question content is qualification-grade THROUGH THE CANONICAL GENERIC PATH
                      (`get_domain_question`), covering: full gap-type coverage (every declared gap type serves a
                      question); ordered progression and index-clamp behavior per gap type; truthful calibration
                      (questions ask only within the I1 declared concept-level scope — no unsupported-expertise
                      demands); non-specialist accessibility of the PACK TEXT itself (lay-readable wording pins —
                      assessed on the committed text, independent of the blocked Path-N surface); provenance
                      (questions carry the pack's recorded provenance lineage); unknown-gap and foreign-domain
                      fail-safe behavior (None; no electronics leakage into mechanical service and vice versa);
                      latency honesty (an explicit pin that the mechanical service path is LATENT while
                      unactivated — recognition/activation separation).
                  (b) the formal §12(b) disposition, recorded in the closure governance surfaces (NOT in the pack):
                      Mechanical non-specialist Path-N service = BLOCKED BY the OPEN D-GMPR-01-D-D3 coupling;
                      the dependency is recorded, its owner named, and NOTHING of it performed; qualification-grade
                      §12 completion for activation purposes remains conditional on that gate's own outcome.
Allowed paths:    NEW tests/test_p9_mech_i5_question_sufficiency.py (evidence embedded; no new framework);
                  governance sync at closure only (roadmap/AIC/CPS + closure record carrying the §12(b) disposition).
Forbidden paths:  EVERYTHING else — engine/** (incl. path_n_questions.py — the seam is NOT repaired, worked
                  around, wrapped, or re-implemented here), web/**, scripts/**, ALL domain packs (mechanical
                  byte-frozen — the I4 corpus validity anchor), domains/domain_provenance.json, all existing
                  test files (expected prior-freeze reconciliation = NONE; conflict → STOP), schemas/,
                  OWNER_DECISION_REGISTER.md, CI. FORBIDDEN OUTCOME: any second question framework, any parallel
                  Path-N architecture, any duplicate D-GMPR responsibility.
```

## §4. Evidence/test requirements for the future implementation (proportionate; all load-bearing)

No parent-RED (evidence-only; nothing is corrected). Integrity rules instead: every pin asserts the UNCHANGED
runtime; expected values grounded in the pack's committed content; honest-precondition style throughout.
Required pins: (1) every declared gap type (exactly the pack's three) serves a non-empty question at index 0;
(2) ordered progression — each gap type's questions serve in pack order with index clamping at the last question
(proven against the pack's own `questions` arrays, not re-typed constants where avoidable); (3) calibration guard —
question texts contain no unsupported-expertise demands (equality-pinned full text set as the primary anti-drift
protection; the I1 NOT-COVERED exclusion classes as the semantic yardstick); (4) non-specialist wording pins on the
committed text (lay-accessibility assertions recorded as evidence, with any deficiency reported truthfully rather
than patched); (5) provenance lineage pins (the pack's recorded `provenance_ref` on gap types/questions resolves in
the manifest); (6) fail-safe pins — unknown gap → None; unknown domain → None; electronics gap ids do not serve
mechanical content and vice versa; (7) the D-GMPR seam pin — `path_n_questions` still returns None for mechanical
(the recorded blocker, asserted AS a blocker, so its future remediation surfaces visibly); (8) latency/recognition
pins — `support_state("mechanical") == "recognized_not_activated"`, activation list unchanged; (9) engine byte-hash
pins (`domain_rules.py`, `progression_loop.py`, **`path_n_questions.py`**) and the five pack hashes (I4-consistent);
(10) deterministic repeated service. Mutations (each flips a specific pin RED; none retained): m1 flip an expected
question text; m2 tamper `domain_rules.py`; m3 tamper `path_n_questions.py` (proves the seam pin is load-bearing);
m4 tamper the mechanical pack (validity anchor); m5 delete an evidence class; m6 weaken the calibration guard's
equality pin. Full governed suite; `git diff --check`; scope proof (single new test file).

## §5. Closure criteria and boundaries

**Closure:** all §4 pins green on the unchanged runtime; mutations executed right-reason with byte-verified
restoration; the closure record states — §12(a) = DISCHARGED (or truthfully NOT dischargeable, with the specific
deficiency and a STOP for a separate content gate); §12(b) = FORMALLY DISPOSITIONED AS D-GMPR-BLOCKED (owner named;
nothing performed; completion conditional on that gate). After I5 closure the qualification lane reduces to exactly
the TERMINAL §15/§16 package/closure — whose contract must then enumerate: the OD-M2 clause-2 annotation duty, the
§12(b) conditional, the §8.4 closure confirmation, and every pre-activation item it does NOT close. **Boundaries:**
Mechanical remains NOT QUALIFIED and NOT ACTIVATED; `activated_domains() == ['electronics_electrical']`; D-GMPR,
CF-6, CF-2, safety family, Tier-1 label, dormant-weight residual, THERM-01, CAP-12/13, WS-PFV-001, D4, D8,
Phase 10, PSRR, deployment — all untouched with their existing owners. **STOP conditions:** any forbidden-path
need; any seam-repair pressure; any existing-test conflict; any evidence-forced pack change (→ separate content
gate); any Owner-policy question. **Next required gate: Mandatory Grill on this exact contract candidate.**
