# S2-PATHN-DCS-001 — Supplemental Decision-Capture Measurement Slice — RUN RECORD

STATUS: EVIDENTIARY RECORD — NOT AN OWNER APPROVAL (S2 §11). NON-ACTIVATING. A result authorizes
nothing (S2 §0). **This is a SUPPLEMENTAL SLICE — it is NOT a Path-N release-candidate run, NOT
Run-004, and NOT part of the original eight-record series.** It consumes no part of the §15.10
8-record boundary and closes nothing. **`T1-A′ CLOSED: NOT ASSERTED BY THIS SLICE`.**

## Identity and preflight

- **Slice:** `S2-PATHN-DCS-001`, executed exactly once per its authoritative frozen design.
- **Evaluated product SHA:** `d867b92eaa69221b1884a9a2eef25cd74225bb86` (PR #601 merge; parents
  `5a392f0…` / `fa5c1f79…`; tree `ce68363d…` — identical to the accepted design candidate's tree).
  **All 4 records used this one SHA — MIXED-SHA: NO.**
- **Design of record:** `docs/benchmarks/S2_PATHN_DECISION_CAPTURE_SLICE_DESIGN.md`, blob
  `b887871a…` — byte-identical to the Owner-accepted candidate `fa5c1f79…`.
- **`INSTRUMENT DELTA: 0`** — instrument blob `4e64b590…` identical at the run-002 authoritative SHA
  and here. **`CORPUS DELTA: 0`** — payloads read from the committed run-001 blob `0ddd1644…`
  (sha256 `0750f3e4…7fce`), with every candidate string asserted **verbatim** in the frozen answer
  `[0]` at runtime, fail-closed. **`PRODUCT DELTA: 0`** — the six G-3 product surfaces byte-identical
  to the evaluated G-3 merge `5a392f0…`; product-path delta `5a392f0..d867b92` = **0 files**.
- **Environment:** in-process Flask test client at the committed tree; `INVENTORAI_DB_PATH` bound to a
  slice store outside the repository; `AI_ADVISORY_ENABLED = False` asserted at import; CWD =
  repository root; working tree clean and detached at the evaluated SHA before execution.
- **Execution accounting:** **1 execution · 4 records · 8 actions each · 0 anomalies · 0 retries ·
  0 restarts · 0 replacement records · 0 aborted attempts.** `FURTHER EXECUTION AUTHORIZED: NO`.

## The four records

| Rec | Case | Lang | Classifier | Domain | Actions | Declared roots | Rendered entries | Comparison-eligible | Anomalies |
|---|---|---|---|---|---|---|---|---|---|
| D1 | E-1 | EN | `NONE` | electronics_electrical | 8/8 · 302 | 4 | 4 | 2 | 0 |
| D2 | E-1 | AR | `NONE` | electronics_electrical | 8/8 · 302 | 4 | 4 | 2 | 0 |
| D3 | M-1 | EN | `SINGLE` | mechanical | 8/8 · 302 | 4 | 4 | 2 | 0 |
| D4 | M-1 | AR | `NONE` | mechanical | 8/8 · 302 | 4 | 4 | 2 | 0 |

Every record realized the design's expected **shape**: 1 active + refined · 1 withdrawn-with-reason ·
1 withdrawn-without-reason · 1 active re-declared under a new root.

## Criterion 5 — *alternatives bounded and truthfully classified* — **PARTIAL ×4**

**Passing, measured on this execution's own captured surfaces and composed record:**

- **bounded** — 4 rendered entries for 4 declared founding roots, each exactly once;
- **no fabricated alternative** — every rendered entry traces to a founding ledger root;
- **no silent disappearance** — both withdrawn alternatives remain visible on **both** served routes,
  in both languages;
- **truthful current-vs-historical membership** — `DecisionRecord.candidates` contains exactly the two
  active roots and **neither** withdrawn chain; the re-declared alternative carries a **new root**
  (`rec_8`) distinct from the withdrawn one (`rec_3`) — no silent reactivation.

**Why not PASS — the measured shortfall.** After the refinement, the refined member's **rendered name
becomes the refinement text**, so that member no longer displays under a name a reader can match to the
case's authoritative bounded candidate set (§3 for E-1, §15.2 for M-1). Its identity is preserved in the
ledger (founding root unchanged) and the set stays bounded, but **as displayed** the bounded set is no
longer fully matchable to the case's bounded candidate set. Measured in **all four** records. This is
contract-specified behaviour — the latest active declaration is the current interpretation (D-G3-2) —
and is reported here as a **measurement finding, not repaired**.

## Criterion 6 — *elimination or qualification reasons explicit* — **PASS ×4**

- the reasoned withdrawal renders the inventor's recorded reason **verbatim** under a governed label;
- the reason-less withdrawal renders the governed *no reason was recorded* copy — **never invented
  text, never omission**;
- **withdrawal is distinguished from system elimination in both languages** via the governed
  *withdrawn by you* state, and **no withdrawn chain carries any `disposition_basis` or
  `disposition_reason` (all `None`)** — no `dispose_candidate()`-equivalent state was fabricated;
- active members that no comparison input references render the derived
  `candidate_not_yet_comparable` reason truthfully;
- **no ranking, preference or winner** anywhere. The only `validated` / `certified` tokens on the
  deliverable sit inside the standing **negative** no-claim disclaimer (*"nothing here has been built,
  tested, demonstrated, validated, certified, or shown feasible"*) — checked in context, so this is the
  no-claim boundary holding, not a finality claim;
- `readiness = insufficient_information` with derived blocking reasons is recorded as a **legitimate
  truthful outcome**, not a failure of 5 or 6.

## EN / AR — **substantive parity PASS**

For one identical action matrix, the entry set, lifecycle states, comparison membership,
not-comparable outcomes, evidence states, reason presence/absence, readiness and blocking reasons are
**identical** across EN and AR (D1↔D2, D3↔D4). User content renders **verbatim and untranslated** in
both. AR surfaces carry `lang="ar" dir="rtl"` and the G-3 section is fully Arabic chrome with no
engine-generated English prose. The English text elsewhere in the AR deliverable is the **pre-existing
registered G-4 generated-output residual** (DOR §3 L160), reproduced and **not repaired here**.

## Comparability

`ORIGINAL SERIES COMPARABILITY: PRESERVED` — Runs 002 and 003 are untouched by this execution.
`SUPPLEMENTAL SLICE IS NOT RECORD-FOR-RECORD COMPARABLE TO RUN-002/003` — different action set,
different cardinality, different namespace (`D1…D4`, never `R1…R8`). The `FAIL ×8` recorded for criteria
5/6 in Runs 002/003 and the `PARTIAL ×4` / `PASS ×4` recorded here are **measurements on different
bases** and must never be merged, averaged, presented as a combined pass rate, or presented as one
superseding the other.

## What this slice proves — and does not

**PROVES**, on the frozen cases at this exact SHA, when the decision-capture surface is exercised: the
served bounded alternative set is complete and non-fabricated; a user withdrawal stays visible and is
truthfully distinguished from a system elimination in EN and AR; a recorded reason renders verbatim and
an absent one renders the governed copy; re-declaration founds a new identity; comparison membership and
the not-comparable reason render truthfully; **criterion 6 moves off `FAIL` and criterion 5 moves to
`PARTIAL` with one specific, named shortfall.**

**DOES NOT PROVE:** G-4 resolution · M-1 relevance resolution · the full §15.7 core gate · deliverable
eligibility · Stage 3 · **T1-A′ closure**. None of these was exercised or measured, and no reader may
infer them.

## Limitations

One evaluator; frozen synthetic cases; an evaluation perspective, not a real user; the perspective axis
held constant by design (the decision-capture projection takes no perspective input, so a
register-specific divergence there would not be detected — stated, not proven absent); the journey
answer corpus deliberately not replayed; judgement is not deterministic and inter-evaluator agreement is
not claimed; §15.11 applies in full. Not user research, market evidence, production readiness, or
generalization beyond the frozen cases.
