# S2 Path-N — Supplemental Decision-Capture Measurement Slice — DESIGN FREEZE

**`SLICE ID: S2-PATHN-DCS-001`** · `DESIGN FREEZE ONLY` · **`RUN-004 AUTHORIZED: NO`** ·
**`SLICE EXECUTION AUTHORIZED: NO`**. This document authorizes no run, no product change, no lane
activation and no closure. A future run of this slice requires its own separate Owner authorization.

## §1. Authority, and what this document is NOT

**Owner design decision (Option B), recorded at this gate.** Same frozen cases · same frozen seeds ·
same criteria · same §15.7 core gate · same perspectives available · the Run-002/003 8-record series
**immutable** · a **separate** supplemental slice exercises the already-authoritative Path-N
decision-capture / G-3 lifecycle · supplemental results are **never** merged, averaged, substituted into
or represented as record-for-record replacements for that series.

**Instrument ownership is unchanged.** `docs/benchmarks/BICYCLE_BRAKE_LIGHT_COMPETITIVE_BENCHMARK.md`
remains the **sole** benchmark owner. This artifact is a **scoped, pointer-only supplemental protocol**
under that record's own §11 amendment mechanism (*"benchmark criteria and protocol may be
owner-approved"*). It **creates no second benchmark owner**, no parallel reasoning-quality programme, and
no new criteria. It **does not modify** the instrument, the frozen corpus, §15.3, §15.5, §15.7, §15.9,
§15.10 or §15.11, and it rewrites no historical evidence.

**§15.10 boundary, stated explicitly so this slice is never miscounted.** §15.10 defines *one Path-N
release-candidate run* as exactly 2×2×2 = 8 records and prohibits splitting those eight to obtain extra
runs. **This slice is NOT a Path-N release-candidate run.** It consumes no part of that boundary, adds no
ninth record to any run, and may never be described as one. It is a supplemental measurement slice with
its own identity and its own reporting namespace.

**Authoritative base at freeze.** Product `5a392f0cfd7d6b19874382441f78fee61cee1a26`; Run-003 evidence
`f1c104ecca38ef99c0937454c8c7419df5130012` (`refs/evidence/s2run003-f1c104ec`); Run-002 evidence
`abc79cee…`; Run-001 evidence `ebf243db…`; instrument tree `61f2bb45…` (unchanged since run 001).

## §2. Objective — the one question this slice exists to answer

> **When the already-authoritative Path-N decision-capture surface is actually exercised, do criteria 5
> and 6 observe a bounded, truthfully classified alternative set and explicit truthful reasons?**

Run-003 established the blocker as reachability, not capability: all 8 records served the
decision-capture section and the `declare-context` form, and the frozen answer-only corpus produced
**0 decision contexts and 0 alternatives**, so criteria 5/6 had **no subject** `[REPOSITORY FACT — Run-003
evidence]`. This slice supplies the subject. **No PASS is pre-decided; `FAIL` and `PARTIAL` remain fully
available outcomes, and `insufficient evidence` remains a legitimate measured result.**

## §3. Cardinality and records

**`CARDINALITY = 2 cases × 2 languages × 1 held-constant perspective = 4 records`.**

| Record | Case | Language | Perspective | Seed |
|---|---|---|---|---|
| `D1` | E-1 | EN | experienced-technical | frozen `E-1\|en` seed, verbatim |
| `D2` | E-1 | AR | experienced-technical | frozen `E-1\|ar` seed, verbatim |
| `D3` | M-1 | EN | experienced-technical | frozen `M-1\|en` seed, verbatim |
| `D4` | M-1 | AR | experienced-technical | frozen `M-1\|ar` seed, verbatim |

**Case and language axes are preserved in full** — both are material: the two cases carry *different*
authoritative bounded candidate sets, and EN↔AR divergence is a live registered obligation (DOR §3
L160), so a single-language slice could not detect a divergence in the G-3 surfaces.

**The perspective axis is deliberately HELD CONSTANT rather than crossed** — `SUPPLEMENTAL DESIGN
CHOICE`, resting on a `REPOSITORY FACT`: the decision-capture projection
(`engine/decision_composition.decision_capture_view` / `rendered_alternative_set`) derives **only** from
the `AssertionRecord` ledger and the composed `DecisionRecord`, and takes **no perspective, register or
answer-quality input whatsoever**; the templates render governed EN/AR chrome plus verbatim user content.
Criteria 5 and 6 are therefore **artifact-subject, not reader-relative** — §15.4 reserves reader-relative
judgement to `P1`, `P6` and criterion 15 and requires artifact-subject criteria to be judged identically
across perspectives. Crossing the axis would double the record count while also varying the payload
register, confounding the case × language contrast this slice exists to make.

**Stated residual of that choice, not hidden:** this slice cannot detect a register-specific divergence
in the decision surface. Given the repository fact above no such path exists, but the slice does not
prove its absence.

## §4. Exact action matrix — identical in all four records

Executed through the **existing governed served routes only**, in this exact order. No route is added,
modified or driven outside what the served surface offers.

| # | Action | Route | Payload (see §5) | Lifecycle state exercised |
|---|---|---|---|---|
| 1 | Declare decision context | `POST /session/<sid>/decision/declare-context` | `CTX` | context founded; candidate set becomes renderable |
| 2 | Declare alternative 1 | `POST /session/<sid>/decision/declare-alternative` | `ALT1` | bounded set member; `option_status=active` |
| 3 | Declare alternative 2 | same | `ALT2` | second member — makes "bounded set" measurable |
| 4 | Declare alternative 3 | same | `ALT3` | third member — the full authoritative bounded set |
| 5 | Refine alternative 1 | `POST /session/<sid>/decision/refine-alternative` | `REF` | successor record in the SAME chain; founding root preserved; evidence state `recorded_detail`; **D-G3-2: no `ClaimItem`, no claim class** |
| 6 | Withdraw alternative 2 **WITH** a reason | `POST /session/<sid>/decision/withdraw-alternative` | `REASON` | lifecycle withdrawal; reason recorded; **must render verbatim and must NOT be presented as an evidence-based system elimination** |
| 7 | Withdraw alternative 3 **WITHOUT** a reason | same, `reason` empty | *(none)* | withdrawal with no recorded reason; **the governed *reason not recorded* copy, never invented text and never omission** |
| 8 | Re-declare alternative 2's concept | `POST …/declare-alternative` | `ALT2` (identical string) | **new founding root / new identity**; the withdrawn chain must NOT be silently reactivated |

**Observed, not actioned:** active alternatives remaining comparison-eligible; the truthful
`candidate_not_yet_comparable` / insufficient-evidence outcome. These are read from the served surfaces
and the composed record, never induced.

**Expected end state per record — 4 rendered entries:** 1 active + refined · 1 withdrawn-with-reason ·
1 withdrawn-without-reason · 1 active (re-declared, new root). Comparison-eligible members: 2.
**This is the expected SHAPE, not an expected RESULT** — whether the product renders it truthfully is
exactly what is being measured.

**Journey answers.** The slice exercises the decision actions only. Whether the record also replays the
frozen answer corpus beforehand is fixed here as: **it does NOT** — the decision-capture surface is served
independently of gap answering (`REPOSITORY FACT`: Run-003 shows the section and its forms present in all
8 records), and replaying answers would import the unrelated `assess_response` / `gap_relevance`
residuals into a slice that is not measuring them.

## §5. Action-payload provenance — every payload is frozen content, verbatim

**No novel technical alternative, reason or refinement is invented anywhere in this slice.** Every
payload is taken **verbatim** from the frozen run-001 answer corpus (committed evidence blob
`0ddd1644afe1f5b57ca5b396fae51a69080e8de3`, sha256 `0750f3e4…7fce`) at key
`<case>|expert|<lang>`, gap type `MECHANISM_COMPLETENESS`, answers `[0] [1] [2]`.

| Payload | Source | Tier |
|---|---|---|
| `CTX` | frozen answer **`[0]`**, in full, verbatim (the inventor's own statement of the decision, per case and language) | **1 — frozen corpus** |
| `ALT1` `ALT2` `ALT3` | the three candidate names enumerated inside that same frozen answer `[0]`, extracted deterministically at its `(1)` `(2)` `(3)` markers | **1 — frozen corpus**, corroborated for EN by the authoritative bounded candidate sets of instrument §3 (E-1) and §15.2 (M-1) — **tier 2** |
| `REF` | frozen answer **`[1]`**, verbatim | **1 — frozen corpus** |
| `REASON` | frozen answer **`[2]`**, verbatim | **1 — frozen corpus** |
| withdrawal-without-reason | *(empty — no payload exists to source)* | n/a |
| re-declaration | `ALT2`, the identical string already sourced | **1 — frozen corpus** |

**Exact extracted candidate strings** (frozen, recorded here so a later reader can re-execute without
re-deriving them):

| | alternative 1 | alternative 2 | alternative 3 |
|---|---|---|---|
| **E-1 EN** | `a wired brake-lever switch` | `accelerometer-based inference of deceleration` | `wheel-speed-based inference` |
| **E-1 AR** | `مفتاح سلكي على ذراع الفرامل` | `استدلال بالتسارع عبر مقياس تسارع` | `استدلال عبر سرعة العجلة` |
| **M-1 EN** | `over-centre toggle latch` | `spring-loaded detent pin` | `gravity-drop gate latch` |
| **M-1 AR** | `مزلاج قلاب متجاوز للمركز` | `دبوس تعشيق بنابض` | `مزلاج بوابة يسقط بالجاذبية` |

**A deliberate adversarial choice, disclosed:** `REASON` is the inventor's own *missing-evidence*
statement (*"No calibration data or physical test results exist yet…"* / *"No load rating, retention
margin, or physical test evidence exists…"*). It is evidence-shaped language attached to a **user
lifecycle act**, which makes it the strongest available test of whether the product still presents the
act as a **user withdrawal** rather than an evidence-based system elimination (contract `A-22`). It is
frozen inventor content, not authored for this slice.

**`SUPPLEMENTAL ACTION PAYLOAD AUTHORITY: ESTABLISHED`** — no payload required invention, so the §7 STOP
condition does not fire.

## §6. Criteria 5 / 6 observation contract — frozen before execution

**The criteria themselves are unchanged.** §5 criterion 5 = *"alternatives bounded and truthfully
classified"*; criterion 6 = *"elimination or qualification reasons explicit"*. Their §15.5 disposition
stays **REUSED — surface-neutral**. What is frozen here is only **what counts as measured evidence**.

**Criterion 5 — observed on both served routes (`/session/<sid>` and `/session/<sid>/deliverable`), in
the active language, plus the composed record:**

1. **Bounded representation** — every declared founding alternative root appears **exactly once**; the
   rendered count equals the declared count (4 after action 8).
2. **No fabricated alternative** — no rendered entry lacks a founding ledger root.
3. **No silent disappearance** — both withdrawn alternatives remain visible on both served routes.
4. **Truthful current-vs-historical membership** — each entry's state is distinguishable as active or
   user-withdrawn, and comparison membership is read from `DecisionRecord.candidates` (expected: the
   refined alternative and the re-declared one; the two withdrawn chains absent from that set), with the
   re-declared alternative carrying a **new root** distinct from the withdrawn one.

**Criterion 6 — observed on the same surfaces:**

1. **Explicit truthful classification/reason** for every non-active entry.
2. **Withdrawal distinguished from system elimination** — the withdrawn entries are never labelled or
   worded as an evidence-based elimination, in **either** language, and carry no
   `disposition_basis`/`disposition_reason` fabricated for them.
3. **Active / not-comparable states explained truthfully** — an active member that no comparison input
   references renders the derived `candidate_not_yet_comparable` reason.
4. **No forced winner** — no ranking, ordering-by-merit, preference or winner anywhere.
5. **No fabricated qualification/elimination** — the recorded reason renders **verbatim**; the
   reason-less withdrawal renders the governed *not recorded* copy.
6. **Insufficient evidence remains legitimate** — a truthful `insufficient_information` readiness with
   derived blocking reasons is a valid measured outcome and is **not** scored as a failure of 5 or 6.

**Result vocabulary is §15.9's, unchanged:** `PASS` / `PARTIAL` / `FAIL` / `NOT EVALUATED`.
`NOT APPLICABLE` stays reserved to criteria 12 and 13 and is **not** available here. **No PASS is
pre-decided; no scoring formula, weight, aggregate or numeric total is defined or permitted.**

## §7. EN / AR handling

Both languages are set through the governed `/ui-language` route, exactly as runs 001–003 did. The AR
records use the **frozen Arabic seeds and frozen Arabic payloads**, unchanged; retranslating to obtain a
different outcome is a §2 case revision and is prohibited. User content is **never translated** by the
product and must render verbatim in both languages. EN/AR observation is **substantive**: for the same
action matrix, the membership, lifecycle states, reasons and not-comparable outcomes must be
**semantically identical** across languages — `dir="rtl"` alone does not evidence parity, and an
identical error in both languages is not parity. Any divergence found is a **measured finding routed to
the existing DOR §3 L160 obligation**, not a new owner and not a repair.

## §8. Deterministic replay requirements

The slice inherits §15.9 unchanged and adds nothing to it. `AI_ADVISORY_ENABLED = False` must be asserted
at import. The exact action sequence, payloads and served responses are recorded verbatim so a later
reader can re-execute and re-judge independently. Composition is expected to be byte-identical for an
equal ledger; **a divergence is a reportable finding, never retried until it agrees**. Evaluator
judgement is **not** deterministic and must never be presented as if it were; agreement between
evaluators is not claimed.

## §9. Comparability boundary — frozen

- **`ORIGINAL SERIES COMPARABILITY: PRESERVED`** — Runs 002 and 003 are untouched by this design and by
  any future slice execution.
- **`SUPPLEMENTAL SLICE IS NOT RECORD-FOR-RECORD COMPARABLE TO RUN-002/003`** — it exercises a different
  action set, has a different cardinality and a different record namespace (`D1…D4`, never `R1…R8`).
- A specific measurement surface may be compared **only** where it is genuinely unchanged between the
  two designs, and any such comparison must name the surface and state why it is comparable.
- The future report must present **`ORIGINAL 8-RECORD SERIES`** and **`SUPPLEMENTAL DECISION-CAPTURE
  SLICE`** as separate sections. **No averaging. No combined pass rate. No substitution.** The slice may
  never be described as part of Runs 002/003, and §15.3's history is not rewritten.

## §10. What this slice CAN and CANNOT prove

**CAN prove**, on the frozen cases, at one exact product SHA, using the approved criteria:

- whether the served Path-N surface represents a **bounded** alternative set matching what was declared;
- whether a user withdrawal stays **visible** and is **truthfully distinguished** from a system
  elimination, in EN and AR;
- whether a recorded withdrawal reason renders **verbatim** and an absent one renders the governed
  *not recorded* copy;
- whether re-declaration founds a **new identity** rather than silently reactivating a withdrawn chain;
- whether comparison membership and the not-comparable reason are rendered truthfully;
- whether criteria 5 and 6 move off `FAIL` **when they have a subject** — in either direction.

**CANNOT prove** — and no future report may imply otherwise:

- **G-4** (EN↔AR substantive-assessment divergence, DOR L160) — the slice does not exercise
  `assess_response`;
- **M-1 relevance false-negative** (`gap_relevance`/RVR-2 via RVR-7) — the slice does not exercise
  `addresses_gap`;
- the **full §15.7 core gate** — the slice does not exercise the corpus journey, correction, or full
  deterministic re-evaluation after an accepted material change;
- **deliverable eligibility** or **Stage 3** — both remain gated by the gap-closure path the slice does
  not run;
- **T1-A′ closure** — closure needs the release-value gate as a whole, and **`T1-A′ CLOSED: NOT ASSERTED
  BY THIS SLICE`** under every possible outcome;
- anything about real users, market, production readiness, or generalization beyond the frozen cases
  (§15.11 applies in full).

## §11. Future evidence-custody model

A future authorized execution follows the established S2 pattern exactly: evidence under
`docs/benchmarks/evidence/s2_pathn_dcs_001/` — a slice record, `slice_identity.json`, per-record captured
served HTML, the criteria 5/6 observation table, the verbatim action/payload log, and `SHA256SUMS.txt`;
one evidence commit parented on the evaluated product SHA, published under a `refs/evidence/*` ref and a
SHA-preserving bundle; **evidence authority only, never product ancestry, never merged into the product
branch**. Product delta, instrument delta and corpus delta must each be **0** and verified before and
after execution.

## §12. Non-goals and fences

`PRODUCT DELTA DURING FUTURE RUN: 0` — no G-3 repair · no routing repair · no G-4 repair · no M-1
relevance repair · no UI modification · no benchmark or corpus modification · no §15.3 rewrite. The
slice drives **only** committed served routes; **product dependency check performed at this freeze:
NONE FOUND** — Run-003 measured the decision-capture section, the `declare-context` form and the
declare/refine/withdraw routes present and reachable on all 8 records at the authoritative SHA, and the
withdraw route already accepts an optional `reason`, so the matrix of §4 is executable **as designed
without any product change** `[REPOSITORY FACT]`.

Also not authorized by this design: ODS-001 · FDC-001 lane activation · Decision Workspace · Path-T ·
persistence expansion · new `DecisionRecord` vocabulary · readiness/TRL/MRL/IRL/SRL · adaptive
questioning · corpus extension · a fourth Path-N release-candidate run · FCORA · Serious Release ·
deployment · production · paid activation.

## §13. Run-authorization boundary

**`SLICE EXECUTION AUTHORIZED: NO`.** This is a design freeze. A future execution requires a **separate**
Owner authorization naming this slice ID, the exact product SHA to evaluate, and the one-execution
boundary. Recording this design authorizes nothing and closes nothing.
