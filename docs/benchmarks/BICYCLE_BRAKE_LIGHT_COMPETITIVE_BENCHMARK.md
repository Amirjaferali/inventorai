# Bicycle Brake-Light Competitive Benchmark

STATUS: GOVERNING COMPETITIVE BENCHMARK — NON-ACTIVATING EVALUATION RECORD

EXTENDED: §§15–17 add the **Path-N Release-Evaluation Extension v1** (Owner-approved
OD-PDVG-11(a) / OD-PDVG-01(a)). §§0–14 are unchanged and remain authoritative for the
Technical Decision Workspace surface; §15 states exactly how they are qualified when the
evaluated surface is the Path-N release candidate. This benchmark remains a single owner —
the extension replaces nothing and creates no second benchmark.

The record's title and filename derive from its **first** frozen case and are deliberately left unchanged:
renaming would break every committed citation, including the mandatory reading-order entry in `CLAUDE.md`.
The name is historical, not a statement that the instrument covers only that case.

## 0. Non-Authorization Boundary

This record defines a repeatable competitive evaluation. It authorizes no
implementation; activates no lane; opens no MVP carve-out; creates no technical
selection; and creates no verification, test, or demonstration claim. It changes
no roadmap, anchor, hold, or closed state, and cannot be relied upon as execution
authorization.

Benchmark results measure product value. They do not create authority. A
favourable result authorizes nothing. An unfavourable result may prevent a
benchmark `PASS`, but it does not independently create a repository authorization
block or change any governed state.

## 1. Purpose and Benchmark Disambiguation

This is a competitive product-value benchmark comparing InventorAI's user-visible
performance against general-purpose AI assistance on the same case.

It is explicitly distinct from `benchmark/run_benchmark_v1.py` and from any
historical replay/regression benchmark already in the repository:
- the historical benchmark = replay/regression assessment of engine scoring
  behaviour;
- this benchmark = a repeatable commercial and product-value comparison of
  user-visible capability;
- neither substitutes for the other, and a result from one is not a result of the
  other.

## 2. Frozen Case Definition

Frozen benchmark case:
- product concept: bicycle automatic brake light;
- bounded technical decision: `braking-detection architecture`;
- user context: the inventor wants automatic brake indication without relying on
  manually pressing a light control;
- installation concern: avoiding or minimizing a physical wire connection to the
  brake lever;
- environmental concern: rough roads and vibration may produce false braking
  indications;
- required outcome: a bounded, evidence-classified technical-decision-readiness
  record, or a truthful blocked outcome.

The frozen case must not be silently changed between benchmark runs. Any
authorized case revision must record: a benchmark-case version; a reason; a date;
and an explicit comparison-impact note.

## 3. Bounded Candidate Set

Benchmark candidate set:
1. wired brake-lever switch;
2. accelerometer-based inference;
3. wheel-speed-based inference.

This set is a **bounded benchmark candidate set supplied by the authorized
decision specification**. It is NOT an exhaustive technical search; NOT proof that
the alternatives are compatible; NOT an externally verified catalog; NOT final
component selection; NOT `technically_selected`; and NOT `frozen`. Provenance and
vocabulary follow S1 and the controlling contracts: candidates carry
`artifact_origin_status=inferred` (provenance = the authorized decision
specification), `source_type=explicit_platform_inference`, and
`evidence_status=advisory`; each begins `option_status=active`.

## 4. Representative Benchmark Inputs

Stable representative input set (at least):
- known problem;
- known mechanism or proposed operating concept;
- explicit installation preference or constraint;
- rough-road / high-vibration condition;
- unknown acceptable false-positive rate;
- missing calibration or physical-test evidence;
- owner preference where applicable;
- evidence-quality distinctions.

Each input must be classified, keeping these distinct: owner requirement;
preference; soft constraint; mandatory constraint; user observation; platform
inference; missing evidence; physical test result. No physical result is invented;
where a physical/calibration result is absent it is recorded as missing evidence,
never fabricated.

## 5. Owner-Approved Evaluation Criteria

A benchmark run must assess all of the following:
1. exact difficult work completed by the platform;
2. work still delegated to the inventor;
3. requirements, preferences, and constraints correctly distinguished;
4. evidence and provenance visible for every material claim;
5. alternatives bounded and truthfully classified;
6. elimination or qualification reasons explicit;
7. bounded recommendation or truthful blocked outcome;
8. minimum next required input identified;
9. decision record version preserved;
10. normalized direct-input snapshot preserved;
11. response to a changed requirement;
12. affected prior decision marked internally with `validity_status=stale`;
13. `REVIEW REQUIRED` displayed only as a user-facing label;
14. exact change reason shown;
15. standalone export understandable without the conversation;
16. no prohibited technical-finality or verification claim;
17. user-visible improvement over the existing assessment-only FDC-001 output;
18. user-visible improvement over a generic AI report.

These criteria are owner-approved benchmark criteria. **Future benchmark results
are not automatically owner-approved.**

## 6. Mandatory Core Success Gate

An increment does not pass merely because one dimension improves. For the first
Technical Decision Workspace increment, ALL of these core outcomes must be
demonstrated:
- difficult work completed by the platform;
- evidence and provenance visibility;
- bounded recommendation or truthful block;
- versioned decision continuity;
- explicit stale / review-required behaviour after a relevant input change;
- standalone exportable value.

Failure of any one core outcome prevents a full-pass conclusion. Partial results
must be recorded truthfully and labelled `PARTIAL` or `FAIL` — never reported as
successful.

## 7. Comparison Baselines

At least three baselines:
- **Baseline A — Existing FDC-001 Assessment:** measure what the current
  assessment-only output completes and what it still delegates.
- **Baseline B — General-Purpose AI Response:** measure a general conversational
  response that may suggest alternatives and next steps but lacks governed
  persistent technical continuity. Do not name or disparage a vendor unless
  supported by a dated, reproducible benchmark run.
- **Baseline C — InventorAI Current Increment:** measure the actual committed
  user-visible increment under evaluation. Do not credit planned or documented
  capabilities that are not implemented and observable.

## 8. Repeatable Evaluation Protocol

Each benchmark run must record: run ID; benchmark record version; frozen case
version; evaluated commit SHA; evaluated branch or release identifier; execution
date;
evaluator; environment; exact user inputs; exact generated outputs or artifact
references; evidence sources used; unsupported or missing evidence;
criteria-by-criteria result; core success-gate result; regressions; limitations;
and the final comparison conclusion.

Screenshots, exports, logs, or artifacts should be referenced where available. No
benchmark result may claim a test, demonstration, compatibility, or safety finding
unless that evidence actually exists.

## 9. Result Vocabulary

Benchmark-evaluation labels (these do NOT alter or substitute for any committed
product or authority enum):
- `PASS`: criterion demonstrably satisfied by committed observable behaviour;
- `PARTIAL`: some observable value exists but the criterion is incomplete;
- `FAIL`: criterion is absent, contradicted, or delegated without sufficient
  platform work;
- `NOT EVALUATED`: evidence was unavailable or the run did not assess it.

These are evaluation labels only — NOT decision statuses, readiness statuses,
evidence statuses, authorization statuses, or verification outcomes. They must
never be written into product artifacts as those enums.

## 10. Versioned Benchmark Run Template

Reusable template (one per run):
- Run ID:
- Benchmark version:
- Case version:
- Evaluated commit:
- Date:
- Evaluator:
- Baseline compared:
- Inputs:
- Platform outputs:
- Difficult work completed:
- Work delegated:
- Evidence/provenance result:
- Decision-readiness result:
- Change-impact result:
- Export result:
- Prohibited-claim check:
- Criteria table (1–18, each `PASS`/`PARTIAL`/`FAIL`/`NOT EVALUATED`):
- Core-gate conclusion:
- Limitations:
- Overall conclusion:

`NO BENCHMARK RUN EXECUTED IN THIS RECORD VERSION.` (The template above is empty;
no run has been executed and no result is recorded in this version. A completed
run must not be fabricated.)

## 11. Result Approval and Interpretation

- Benchmark criteria and protocol may be owner-approved;
- individual benchmark results are evidentiary records, not owner approvals;
- a result does not activate a lane or authorize implementation;
- a positive benchmark does not prove production readiness;
- a negative benchmark must not be concealed;
- results must remain linked to the evaluated commit;
- a later product change does not rewrite an earlier result;
- later runs supersede conclusions only for their own evaluated versions, not the
  historical facts of earlier runs.

## 12. Update Rules

A new versioned benchmark run is required after: a major user-visible increment; a
relevant decision-workspace behaviour change; a change to evidence classification;
a change to versioning or stale-detection behaviour; a change to standalone export;
or a regression fix affecting any mandatory criterion.

A governance-only documentation change does NOT trigger a product-value benchmark
run unless it changes user-visible behaviour.

## 13. Preserved Scope and Holds

This record does not authorize: Commit B; lane activation; code; external-source
integration; persistence delivery; final component selection; `technically_selected`;
`frozen`; BOM; wiring; firmware; compilation; simulation; physical testing;
demonstration claims; certification; production readiness; Path T; or multi-domain
expansion.

Preserved: `PRESERVE UNMODIFIED AND PAUSE`; Roadmap §§4–7 unchanged; lane INACTIVE;
and all existing holds and closed states (R2=HELD · FORM T=BLOCKED ·
S-6=UNCLASSIFIED · AA-3/AA-4/AA-5=BLOCKED · Phase 5/6=UNAUTHORIZED · ILT-002
evidence collection=NOT AUTHORIZED · Path T=BLOCKED · Phase 4=CLOSED ·
Gate 8=CLOSED · runtime_integrated=TRUE).

## 14. Relationship to S1 and Future S3

See `docs/governance/INVENTORAI_COMMERCIAL_DIFFERENTIATION_DIRECTION.md`.
- S1 defines the strategic commercial direction;
- S2 (this record) defines the repeatable evaluation mechanism;
- S2 does not amend or override S1;
- both remain non-activating;
- mandatory agent reading-order enforcement will be added only through the
  separately authorized S3 edit to `CLAUDE.md`.

---

## 15. Path-N Release-Evaluation Extension v1

**Authority.** Owner decisions **OD-PDVG-11(a)** (approve the bounded S2 extension scope) and
**OD-PDVG-01(a)** (authorize the bounded extension and, once it is authoritative, one S2 run against the
exact release candidate), issued against authoritative PDVG-01
(`docs/governance/PDVG_01_PRE_RELEASE_PRODUCT_DEPTH_AND_VALUE_GATE_RECORD.md`, T1-A′). This extension is
**governance only**. It authorizes **no benchmark run**, no product implementation, no lane activation,
no domain activation, and no architectural change. §0's non-authorization boundary applies to it in full.

**Owner and non-duplication.** The owner of this instrument remains **this record**. §15–§17 extend it
under its own amendment mechanisms — §2 (authorized case revision: version, reason, date,
comparison-impact note) and §11 (benchmark criteria and protocol may be owner-approved). **No second
benchmark owner, no parallel reasoning-quality programme, and no "Golden Reasoning Benchmark" is created
or implied.** Integration Before Duplication.

**Why an extension is required.** §6's mandatory core gate is scoped verbatim *"For the first Technical
Decision Workspace increment"*, §7's Baseline A is the FDC-001 Decision Workspace assessment, and §12's
re-run triggers are decision-workspace behaviour changes. Applied unchanged to the Path-N release
candidate, parts of this instrument would evaluate a different product lane. §15 states the qualifications
precisely rather than leaving them to a run-time judgement.

### 15.1 Evaluated surface

The **Path-N release candidate**: the governed Path-N idea-development journey and the deliverable it
produces, at one exact commit. The Technical Decision Workspace (FDC-001) surface is **not** the subject
of a Path-N evaluation run and keeps §§0–14 unqualified for its own runs.

### 15.2 Case set — exactly two frozen cases

**Case E-1 — electronics/electrical.** The existing frozen case of §2 (bicycle automatic brake light;
bounded technical decision `braking-detection architecture`), **unchanged**, with the §3 bounded candidate
set unchanged. Case version: **`E-1 v1`** — a label introduced here so the two cases can be named
distinctly; **the case content is unchanged and §2 is not revised.**

**Case M-1 — mechanical.** *Benchmark-case version:* `M-1 v1`. *Reason:* PDVG-01 T1-A′ requires mechanical
coverage; Mechanical is an already-activated governed domain, so evaluating it introduces no domain
expansion. *Date:* **2026-08-23** (the date this extension was authored; the authoritative date is that
of the merge commit that makes it authoritative). *Comparison-impact
note:* M-1 is a **new** case and establishes its own baseline; results for M-1 are never comparable to
E-1 results, and no cross-case aggregate score may be reported.

- product concept: a manually foldable wheelchair ramp for a home doorway;
- bounded technical decision: `folded-position retention architecture`;
- user context: the inventor wants the ramp to stay reliably locked in the flat, load-bearing position and
  to fold away without tools;
- installation concern: avoiding permanent modification to the doorway or frame;
- environmental concern: outdoor moisture and grit may degrade a latch over time;
- required outcome: a bounded, evidence-classified technical-decision-readiness record, or a truthful
  blocked outcome.

**Bounded candidate set for M-1** (supplied by this authorized specification, exactly as §3 governs for
E-1): 1. over-centre toggle latch; 2. spring-loaded detent pin; 3. gravity-drop gate latch. This set is
**not** an exhaustive technical search, **not** proof of compatibility, **not** an externally verified
catalog, **not** final component selection, **not** `technically_selected`, and **not** `frozen`. Each
candidate carries `artifact_origin_status=inferred` (provenance = this authorized specification),
`source_type=explicit_platform_inference`, `evidence_status=advisory`, and begins `option_status=active`.

**Representative inputs for M-1.** §4 is unchanged and continues to govern E-1. Its **classification
requirement is surface-neutral and applies to M-1 in full** — every input classified, keeping *owner
requirement*, *preference*, *soft constraint*, *mandatory constraint*, *user observation*, *platform
inference*, *missing evidence*, and *physical test result* distinct, and **no physical or calibration
result invented**: an absent one is recorded as missing evidence. §4's *stable representative input set*
is stated in E-1's terms, so M-1's counterpart set is stated here, at the same level of generality:

- known problem — the ramp must stay locked in the load-bearing position and fold away without tools;
- known mechanism or proposed operating concept — a manually operated retention mechanism at the hinge;
- explicit installation preference or constraint — no permanent modification to the doorway or frame;
- environmental / degradation condition — outdoor moisture and grit acting on a latch over time;
- unknown acceptable load and retention margin;
- missing physical-test or load-rating evidence;
- owner preference where applicable;
- evidence-quality distinctions.

**No load rating, safety margin, compliance statement, or accessibility-standard conformity is asserted,
implied, or to be produced by any run** — where such evidence is absent it is recorded as missing, exactly
as §4 requires.

**Domain-gate admissibility — measured in advance, and protected.** A Path-N run begins at the governed
`/start` domain gate, which classifies the **exact seed text** entered. Measured at the base commit
**[EXEC]** by calling `engine.domain_rules.classify_domain` directly — **this measures the classifier
function only**, not the full `/start` flow, which additionally applies the unsupported-evidence check,
the classifier-miss consent path, and `_admit_specialist_domain`; **the end-to-end `/start` outcome is
what a run records**:

| Exact string passed to `classify_domain` | Result |
|---|---|
| `a manually foldable wheelchair ramp for a home doorway` (M-1's product concept, verbatim) | `NONE` — no domain resolved |
| `a manually foldable wheelchair ramp for a home doorway that must stay reliably locked in the flat, load-bearing position and fold away without tools` (M-1's concept plus a **paraphrase** of its user context — labelled a paraphrase because it is not verbatim from the bullet above) | `SINGLE` → **`mechanical`** |
| `a manually foldable wheelchair ramp for a home doorway with an over-centre toggle latch` (M-1's concept, verbatim, plus candidate 1) | `NONE` |
| `bicycle automatic brake light` (E-1's §2 product concept, verbatim) | `NONE` |
| `bicycle automatic brake light with accelerometer-based inference` (§3 candidate 2, verbatim) | `NONE` |
| `bicycle automatic brake light with wheel-speed-based inference` (§3 candidate 3, verbatim) | `NONE` |
| `bicycle automatic brake light with a wired brake-lever switch` (§3 candidate 1, verbatim) | `SINGLE` → **`mechanical`** |
| `bicycle automatic brake light using an accelerometer sensor` | `SINGLE` → **`electronics_electrical`** |

**Read these results carefully — they are the reason this protection exists.** Neither case's bare product
concept resolves to a domain. Each resolves only when further wording from its own case is added, **and
which domain it resolves to depends on which wording is added**: the electronics case E-1 resolves to
**`mechanical`** when stated with its own §3 candidate 1, and to `electronics_electrical` only with other
phrasing. An evaluator choosing how to phrase a seed can therefore steer — inadvertently or deliberately —
which domain the journey runs as, or whether it resolves at all.

**Because wording steers the outcome, the seed text is frozen here rather than left to the evaluator.**
Leaving the evaluator free to pick which sentence of a case to type would hand them the domain result. The
seed text is therefore fixed by one rule, stated as a construction and applied identically to both cases:
**the case's product-concept line, then its user-context sentence, verbatim, joined by an em dash, and
nothing else.** Applying that rule yields exactly these two frozen English seeds:

- **E-1:** `bicycle automatic brake light — the inventor wants automatic brake indication without relying
  on manually pressing a light control`
- **M-1:** `a manually foldable wheelchair ramp for a home doorway — the inventor wants the ramp to stay
  reliably locked in the flat, load-bearing position and to fold away without tools`

**Each seed is one single-line string.** The two above are line-wrapped for rendering only: reconstruct
each by joining its lines with a single space and collapsing runs of whitespace to one space. The em dash
is `—` (U+2014), surrounded by single spaces. No leading or trailing whitespace.

Measured at the base commit **[EXEC]**, `classify_domain` returns **`NONE`** for the E-1 seed and
**`SINGLE` → `mechanical`** for the M-1 seed. **That asymmetry is recorded, not corrected.** The E-1 seed
enters the governed classifier-miss / admission path rather than resolving directly, and what that path
then does is observed and reported by the run. **The rule was fixed as a construction, and the result of
applying it is disclosed — the seeds were not selected to obtain these outcomes.** The Arabic seeds are
governed by §15.3, which also records why an Arabic seed cannot resolve to a domain at all.

**Binding rules, so this is measured rather than engineered away:**

1. The two seeds above are the frozen **English** seed text. **The Arabic seeds are frozen at first use**
   (§15.3): produced once as faithful translations, recorded verbatim with that run, and immutable
   thereafter except by a §2 case revision. Freezing them later rather than here is admissible **only
   because** an Arabic seed cannot resolve to a domain at all — measured, §15.3 — so no translation choice
   can steer the gate outcome; the moment that ceased to be true, the Arabic seeds would have to be frozen
   in advance exactly as the English ones are. Each run records **the exact seed text entered, verbatim,
   per case and per language** (§8 already requires exact user inputs; this makes the seed text explicitly
   one of them), together with the exact gate outcome observed.
2. A case is **never reworded to obtain a more convenient classification or admission outcome** — not by
   substituting another sentence of the same case, not by adding a candidate name, not by translating
   loosely. Changing a frozen seed at all is a **case revision** and requires §2's full four-field record
   (version, reason, date, comparison-impact note); doing it to change a gate outcome is **prohibited** and
   invalidates the run.
3. **`engine/domain_rules.py`, the domain registry, the activation set, and the `/start` admission policy
   are never changed to admit a benchmark case.** If the governed gate blocks, mis-classifies, or
   consent-routes a frozen case, **that is a truthful, reportable result** — recorded against the relevant
   criteria and in the run's limitations — never a defect in the benchmark to be corrected in the product.
4. Whatever route a case takes through the gate is **recorded as observed**, and a difference in route
   between the two cases is a finding, not a nuisance to be normalized away.
5. **A domain resolved for a case is never asserted to be the case's "correct" domain.** The measurements
   above show the E-1 electronics case resolving to `mechanical` under other phrasings; a run reports what
   the gate did, and never converts that into a claim about the idea's true domain.

This is the same principle as §15.6, applied to a second surface: **a benchmark tests the product
architecture; the product architecture is never distorted to satisfy the benchmark.**

Neither case may be silently changed between runs (§2). **No third case and no additional domain is
authorized.**

### 15.3 Language dimension — EN and AR

Each case is evaluated in **English and Arabic**, on the governed UI-language surface
(`SUPPORTED_LANGS = ("en", "ar")` in `web/ui_text.py`; the `/ui-language` route) **[EXEC]**. The
evaluation is of the **release-relevant Path-N experience** in each language — the questions served, the
guidance shown, the deliverable produced — **not** the mere existence of translation strings. This
extension **defines no new language behaviour and redefines no UI-language architecture**; it evaluates
what is committed.

**One structural fact about the Arabic dimension, measured in advance so no run is surprised by it.**
`engine/domain_rules.py` contains **no Arabic text**, and **none of the domain packs under `domains/`
contains Arabic text** **[EXEC]**. The domain classifier therefore holds **no Arabic vocabulary**, and an
Arabic-only seed **cannot** resolve to a domain: measured at the base commit, the Arabic renderings of
both frozen seeds return **`NONE`**. An Arabic run consequently reaches the governed classifier-miss /
admission path at the gate for **both** cases.

**This is recorded as a property to be evaluated, never as a defect to fix for the benchmark.** This
extension does **not** authorize adding Arabic vocabulary to the classifier, to the domain packs, or to
the admission policy — that would be distorting the product to improve a benchmark result (§15.6, §16).
The Arabic seeds are faithful translations of the two frozen English seeds of §15.2, **produced once,
recorded verbatim with the run, and reused unchanged** for any re-execution; retranslating in order to
obtain a different gate outcome is a **case revision** under §2 and is prohibited when done for that
purpose.

### 15.4 Evaluation perspectives — novice and experienced technical

Each case is evaluated from two **evaluator perspectives**: a **novice** perspective and an **experienced
technical-user** perspective, recorded and reported **separately** and never merged into one score.

**What actually differs between the two perspectives**, so they are not one evaluation counted twice:

- **The answers supplied to the journey's questions.** The novice perspective answers in everyday,
  non-specialist terms; the experienced-technical perspective answers in the technical terms a competent
  practitioner would use. **Both answer only from the frozen case's own stated content.** Inventing facts
  the case does not state — a load rating, a measured false-positive rate, a component choice — is
  **prohibited** in either perspective and would invalidate the run. Where the case does not supply an
  answer, the honest answer is that it is unknown.
- **The judgement lens.** Three criteria are **reader-relative by their own wording** and are judged *for
  that reader*: `P1` (are the questions answerable by this inventor), `P6` (is the deliverable useful to
  this reader), and **criterion 15** (is the standalone export *understandable* without the conversation —
  understandability is a property of a reader, so a novice/expert divergence here is a legitimate result,
  not an inconsistency). Criteria whose subject is the artifact rather than the reader — **4, 7, 16 and
  `P4`** — are judged identically across perspectives and must not diverge without a stated reason.
- **Nothing else.** The case content, the language, the baselines, and the evaluated commit are identical
  across perspectives.

Both answer sequences are recorded verbatim (§15.9), so either perspective can be re-executed and
re-judged independently. **The two perspectives are never averaged, merged, or reported as one score.**

**Binding truthfulness constraint.** These are **evaluation perspectives adopted by an evaluator**. An S2
run is an **evaluation instrument**, not real-user research, and **must never be described as** user
research, usability testing, or real-user validation. **No real user participates, and no real user data
is used** — both frozen cases are synthetic specifications. The separate **T1-C′ ILT-style real-user
round** remains independently required, and **S2 does not substitute for it** in whole or in part.

### 15.5 Criteria disposition for the Path-N surface

The §5 criteria are **not** renumbered and **not** rewritten. For a Path-N run each is classified as
**REUSED**, **ADDED**, or **NOT APPLICABLE**, on the stated evidence:

| § | Criterion (abbreviated) | Path-N disposition | Basis |
|---|---|---|---|
| 1 | difficult work completed by the platform | REUSED | surface-neutral |
| 2 | work still delegated to the inventor | REUSED | surface-neutral |
| 3 | requirements / preferences / constraints distinguished | REUSED | surface-neutral |
| 4 | evidence and provenance visible for every material claim | REUSED | surface-neutral |
| 5 | alternatives bounded and truthfully classified | REUSED | surface-neutral |
| 6 | elimination or qualification reasons explicit | REUSED | surface-neutral |
| 7 | bounded recommendation or truthful blocked outcome | REUSED | surface-neutral |
| 8 | minimum next required input identified | REUSED | surface-neutral |
| 9 | decision record version preserved | **REUSED** | Path-N preserves `contract_version` / `engine_contract_version` in the durable project envelope |
| 10 | normalized direct-input snapshot preserved | **REUSED** | Path-N preserves `seed_idea_text` and the verbatim append-only accepted-answer ledger |
| 11 | response to a changed requirement | **REUSED** | the committed architecture answers a changed input by **full deterministic re-evaluation** (`D-AISR-06`; see §15.6) — whether the evaluated surface actually delivers it is what this criterion measures; exercised via the governed correction path, see the note below the table |
| 12 | affected prior decision marked `validity_status=stale` | **NOT APPLICABLE — ARCHITECTURALLY PROHIBITED** | see §15.6 |
| 13 | `REVIEW REQUIRED` displayed only as a user-facing label | **NOT APPLICABLE — LANE-SCOPED** | the label exists only inside `engine/decision_workspace.py` (and a test importing it); the Path-N surface defines no such label, so the criterion has no subject here. Its general prohibition — an evaluation label is never written into a product artifact as a status enum — is preserved unconditionally by §9 and §15.9 |
| 14 | exact change reason shown | **REUSED** | Path-N has a correction acknowledgement and surfaces withdrawn source records; **a weak or unreachable result here is a truthful FAIL/PARTIAL, never an N/A** |
| 15 | standalone export understandable without the conversation | REUSED | surface-neutral — but **reader-relative**: *understandable* is a property of a reader, so a novice/experienced divergence here is a legitimate result (§15.4), not an inconsistency |
| 16 | no prohibited technical-finality or verification claim | REUSED | surface-neutral |
| 17 | improvement over the existing assessment-only FDC-001 output | REUSED | Baseline A; see §15.7 |
| 18 | improvement over a generic AI report | REUSED | Baseline B |

**Exactly two criteria are NOT APPLICABLE for the Path-N surface: 12 and 13.**

**The Basis column explains why a criterion has a subject on this surface — it is never a pre-judgement of
the result.** Naming a Path-N counterpart establishes that the criterion is *evaluable* here, not that it
passes. **Every REUSED criterion is still judged by the run and may come back `FAIL` or `PARTIAL`**, and a
counterpart that exists in the code but is not reachable, visible, or usable on the evaluated surface is
exactly the kind of finding this instrument exists to produce.

**How criteria 11 and 14 are exercised — and the one thing that would falsify the result.** Both concern a
changed input, so both are evaluated through the **governed correction path** (`POST
/session/<sid>/correct`, `web/app.py:2625–2626`) **[EXEC]**, reached **the way the evaluated surface makes
it reachable to the perspective being evaluated**. The rendered in-page correction affordance is a
**separate, unauthorized** increment (PDVG-01 T1-B / FPC-02) **[REPO]**: if the perspective cannot reach
the correction path on the governed surface, criteria 11 and 14 are **`FAIL` or `PARTIAL` with that
reason** — a truthful finding about reachability. **Driving the route directly, outside what the surface
offers, must never be reported as a `PASS`**; a run that exercises it that way must label the result as
route-level and say so explicitly.

**Disclosed divergence from PDVG-01 T1-A′.** T1-A′ anticipated marking *"the decision-workspace-only
criteria (9–14, and the §6 core gate as written)"* NOT APPLICABLE. This extension applies T1-A′'s
**rule** — a criterion is NOT APPLICABLE only where it is structurally bound to another product lane —
and the source reconstruction narrows the set to **{12, 13}**: criteria 9, 10, 11 and 14 each have a real
Path-N counterpart, so excusing them would understate what the instrument can legitimately judge. The
divergence is from T1-A′'s parenthetical **enumeration**, not from its rule, and is recorded here rather
than silently applied.

**ADDED criteria for the Path-N surface** (numbered `P1…P6` so §5's numbering is never disturbed):

- **P1 — question quality.** Are the questions served materially useful for the frozen case: relevant to
  the stated decision, non-duplicative, answerable by this inventor, and ordered without obvious
  incoherence?
- **P2 — critical missing gaps.** Does the journey surface the gaps a competent reader would consider
  decision-critical for the frozen case, or does it terminate with them unraised?
- **P3 — unsafe assumptions.** Does the output avoid asserting or silently relying on assumptions that
  would be unsafe for the frozen case, and does it name them where they exist?
- **P4 — prohibited / unsupported claims.** Does the output stay inside the committed no-claim boundary —
  no safety, compliance, certification, approval, legal, patent, or engineering-validation claim?
- **P5 — specialist escalation.** Where the case exceeds what the platform can responsibly conclude, is a
  specialist handoff or escalation surfaced truthfully rather than a fabricated conclusion?
- **P6 — deliverable usefulness against the frozen case.** Judged against the case's own required
  outcome, is the deliverable usable by its intended reader, or usefully and truthfully blocked?

Evidence visibility, provenance, and truthful-block/bounded-recommendation behaviour are **already**
required by criteria 4 and 7 and are **not** duplicated as new criteria.

**Required-dimension coverage map.** Every dimension the approved scope requires is carried by a named
criterion, so coverage can be audited without re-reading the prose:

| Required dimension | Carried by | Reused or added |
|---|---|---|
| question quality | `P1` | ADDED |
| critical missing gaps | `P2` | ADDED |
| unsafe assumptions | `P3` | ADDED |
| prohibited / unsupported claims | `P4` (with criterion 16) | ADDED + REUSED |
| specialist escalation | `P5` | ADDED |
| evidence visibility | criterion 4 | REUSED |
| provenance | criterion 4 | REUSED |
| truthful block / bounded recommendation | criterion 7 (and the §15.7 core gate) | REUSED |
| deliverable usefulness against the frozen cases | `P6` (with criterion 15) | ADDED + REUSED |
| comparison against the governed baselines | §15.8 with criteria 17 and 18 | REUSED |

**No dimension is carried by reuse where the reused criterion does not already state it.** Criterion 4 is
verbatim an evidence-and-provenance criterion and criterion 7 verbatim a bounded-recommendation-or-truthful-block
criterion; adding `P`-criteria for them would produce two scores for one property.

### 15.6 Criterion 12 — binding architectural protection

`validity_status` occurs in **no** Python file in this repository **[EXEC]**, and targeted partial
invalidation is **PROHIBITED** **[REPO]**: `D-AISR-06` (ACCEPTED, `docs/governance/OWNER_DECISION_REGISTER.md`)
— *"Full deterministic re-evaluation mandatory after accepted material change; targeted partial prohibited
(preserves D17)"* — and
`docs/governance/PVCG_R4_C_USER_CORRECTION_AND_DETERMINISTIC_INVALIDATION_CONTRACT.md` **§2.4**, which
lists *targeted / partial / selective re-evaluation* among the changes that are **authoritatively
forbidden, not merely unscoped**.

**Binding rule.** Criterion 12 is **NOT APPLICABLE** for the Path-N surface and **must never be satisfied
by introducing `validity_status`, stale-marking, or any targeted partial-invalidation semantics into the
product.** A benchmark tests the product architecture; the product architecture is never distorted to
satisfy a benchmark. `D17`, `D-AISR-06`, the PVCG-R4 semantics, and every corresponding invariant are
**unchanged by this extension**.

The property criterion 12 was reaching for — that a changed input does not leave stale conclusions
standing — **is** evaluated on the Path-N surface, by criterion 11 and by §15.7's core-gate outcome,
against the architecture the product actually implements: full deterministic re-evaluation.

### 15.7 Path-N core success gate

§6's gate is scoped to the first Technical Decision Workspace increment and is **NOT APPLICABLE as
written** to a Path-N run. §6 is unchanged for its own surface. The Path-N variant requires **all** of:

- difficult work completed by the platform;
- evidence and provenance visibility;
- bounded recommendation or truthful block;
- versioned decision continuity (durable record identity preserved across the journey);
- **full deterministic re-evaluation after an accepted material change** — replacing §6's
  *"explicit stale / review-required behaviour"* outcome, which is the prohibited construct of §15.6;
- standalone exportable value.

Failure of any one prevents a full-pass conclusion. Partial results are recorded truthfully as `PARTIAL`
or `FAIL` and **never** reported as successful (§6, §9).

### 15.8 Baselines

§7 applies unchanged: **Baseline A** — the existing FDC-001 assessment output; **Baseline B** — a
general-purpose AI response, with §7's no-vendor-disparagement rule intact; **Baseline C** — the actual
committed, observable Path-N increment under evaluation, crediting **no** planned or documented
capability that is not implemented and observable. Baselines are compared **per case and per language**;
no aggregate across cases, languages, or perspectives may be reported.

**Baseline B is an evaluator activity, not product AI.** Obtaining a general-purpose AI response for
Baseline B happens **outside the product**, by the evaluator. It is **not** a product AI call, it does
**not** enable `AI_ADVISORY_ENABLED` (`False` at the base commit **[EXEC]**), it does **not** relax the
Path-N AI guard, and **`AI ACTIVATED: NO` is unchanged by any run**. **No benchmark artifact — Baseline B
text included — may be fed back into the product**, into a fixture, or into any governed record as
platform-generated content. §7's no-vendor-disparagement rule applies to whatever assistant is used, and
the assistant used must be named in the run record as part of the exact inputs (§8).

**Baseline A reachability, stated in advance.** Baseline A is the *output* of the assessment-only path
that criterion 17 names. The Technical Decision Workspace lane is **INACTIVE** (§13), so if that output
cannot be produced at the evaluated commit for a given case, the run records **`NOT EVALUATED` with the
reason** for criterion 17 and for the Baseline A comparison. It is **never** silently dropped, **never**
substituted by another baseline, and **never** reported as an improvement over a baseline that was not
obtained. **Reaching Baseline A never authorizes activating that lane** — §13's `lane INACTIVE` hold is
unchanged, and no run may relax it.

### 15.9 Result mechanics and evidence format

§9's vocabulary applies unchanged — `PASS` / `PARTIAL` / `FAIL` / `NOT EVALUATED` — plus, for this
surface only, **`NOT APPLICABLE`**, which is reserved **exclusively** for criteria 12 and 13 and for §6 as
written. `NOT APPLICABLE` is **never** a substitute for `FAIL`: a criterion that the product could satisfy
but does not is a `FAIL` or `PARTIAL`. These remain **evaluation labels only** — never decision,
readiness, evidence, authorization, or verification statuses, and never written into product artifacts as
those enums (§9).

Each run records §8's fields, and additionally, per case × language × perspective: the criteria table
(1–18 with dispositions, plus `P1…P6`), the Path-N core-gate result, limitations, and the conclusion.
The §10 template is used with those additional axes. Results are evidentiary records, not Owner approvals
(§11).

**Deterministic and repeatable execution — stated honestly, because the two halves differ.**

- *The evaluated product behaviour is expected to be repeatable.* The frozen cases fix the inputs, the
  evaluated commit fixes the code, and **no live AI model participates in the evaluated Path-N behaviour
  at this commit** — `AI_ADVISORY_ENABLED = False` in `engine/ai_advisor.py` **[EXEC]**. A re-execution of
  the same case, in the same language, at the same SHA, with the same recorded answer sequence is
  therefore **expected** to produce the same platform output. **This is an expectation the run tests, not
  a proven property of the whole journey**: a divergence is a reportable finding, not a tolerance, and
  must be reported rather than retried until it agrees.
- *The evaluator's judgement is not deterministic and must never be presented as if it were.* Criteria
  1–18 and `P1…P6` are judged, not computed. Each run therefore records the exact answer sequence
  supplied, the evaluator, and the date, so a later reader can re-execute the inputs and re-judge them
  independently. **Agreement between two evaluators is not established by this contract and must not be
  claimed.**
- **No scoring formula, weight, aggregate, or numeric total is defined or permitted.** Results are the
  per-criterion labels of §9 plus the core-gate outcome. `PARTIAL` is never averaged into a pass.

### 15.10 Exact commit identity and the one-run boundary

A Path-N run is valid **only** when it records the **exact evaluated commit SHA** of the release candidate,
and every result is bound to that SHA. A later product change never rewrites an earlier result (§11).

**What "one run" contains, so the boundary is countable.** One Path-N release-candidate run =
**2 cases × 2 languages × 2 perspectives = 8 evaluation records**, all at the **same** evaluated commit,
plus one consolidated run record carrying the §8 fields and the §15.11 limits. **No more and no fewer.**
The eight records are reported **separately**; there is no aggregate, and the run is not complete until
all eight exist or a missing one is recorded as `NOT EVALUATED` with its reason. Splitting the eight into
several "runs" to obtain more than one authorized run is **prohibited**, and so is collapsing them into a
single undifferentiated result.

**OD-PDVG-01(a) authorizes exactly one Path-N release-candidate run**, and **only after** this extension
has itself become authoritative through the full high-assurance lifecycle (candidate → freeze → Creator
Grill → Independent External Review → Owner exact-SHA acceptance → SHA-preserving publication → PR →
merge commit → post-merge verification). **No run is authorized by this record.** Any further run requires
a separate Owner authorization.

### 15.11 Interpretation limits

One run may support only a bounded proposition: **on the frozen cases (E-1, M-1), at the exact
release-candidate commit, against the governed baselines, using the approved criteria, the evaluated
Path-N journey and deliverable did or did not meet the defined S2 release-value criteria.**

A run **must not** be described as evidence of: all-user behaviour; general market success; real-user
usability; novice or expert fit in the real world; production readiness; security; operational readiness;
commercial readiness; universal superiority over general-purpose AI; or generalization beyond the frozen
cases. **T1-A′ and T1-C′ remain separate evidence sources and neither substitutes for the other.**

---

## 16. Prohibited changes under this extension

This extension does **not** authorize, and no run may be used to justify: introducing `validity_status`
or stale-marking semantics; targeted partial invalidation; any change to `D17`, `D-AISR-06`, or PVCG-R4
semantics; **any change to `engine/domain_rules.py`, the domain registry, the activation set, or the
`/start` admission policy made in order to admit, re-classify, or better route a benchmark case**;
**rewording a frozen case to obtain a more convenient classification or admission outcome**; **adding
Arabic — or any other language's — vocabulary to the domain classifier, the domain packs, or the admission
policy**; any change to the UI-language architecture; new domain activation or Path T; a second
benchmark owner or reasoning-quality programme; product implementation of any kind; benchmark execution;
PSRR; deployment; production; or paid activation. **A favourable result authorizes nothing** (§0).

---

## 17. Preserved scope and status note

**This extension changes no hold, no closed state, no anchor, and no roadmap entry.** It moves nothing.
§13 is preserved exactly as written and is **not edited** by this extension.

§13's list is a snapshot taken when §13 was authored. Two of its entries have since been superseded by
later authoritative repository truth, which governs where they differ — verified for this extension, and
recorded here rather than by editing §13:

- **Mechanical is an activated governed domain.** `engine.domain_activation.activated_domains()` returns
  `['electronics_electrical', 'mechanical']` **[EXEC]**, under the merged Mechanical Activation Execution
  Gate, and **Phase 9 is FORMALLY CLOSED** in `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` **[REPO]**.
  Evaluating case M-1 therefore introduces **no** domain expansion, **no** new activation, and **no**
  Path T. §13's `multi-domain expansion` prohibition is untouched: this extension expands nothing.
- **Phase 5 is FORMALLY CLOSED** (P5-1 / P5-2 / P5-3, roadmap `G-P5-FINAL-CLOSURE-SYNC-01`) **[REPO]**,
  superseding §13's `Phase 5/6=UNAUTHORIZED` snapshot for Phase 5 only. Phase 6 is **not** asserted to
  have changed by this extension. This bears on nothing the extension authorizes; it is recorded so §13
  is not silently read as current.

Every other §13 entry — including `ILT-002 evidence collection = NOT AUTHORIZED`, `Path T = BLOCKED`,
`lane INACTIVE`, and `PRESERVE UNMODIFIED AND PAUSE` — is carried forward **as written and unchanged**,
and this extension relies on none of them being relaxed.

The only governance records changed alongside this extension are those carrying the Owner decisions
**OD-PDVG-11(a)** and **OD-PDVG-01(a)** and the routine roadmap / active-contract / project-state
synchronization. `BENCHMARK EXECUTION: NOT AUTHORIZED`.
