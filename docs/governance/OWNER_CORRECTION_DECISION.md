# OWNER_CORRECTION_DECISION.md
## ILT-002 §8 Archetype Denominator Correction

**Document ID:** OWNER_CORRECTION_DECISION
**Type:** Owner Decision Record
**Status:** FINAL — owner approved 2026-06-07
**Date:** 2026-06-07
**Scope:** ILT-002 campaign only
**Authority level:** Owner decision
**Governing document amended:** ILT002_EXECUTION_GUIDE.md §8 Step 2
**Depends on:** ARCHETYPE_RESOLUTION_OPTIONS.md, ARCHETYPE_DEFINITION_DECISION_REPORT.md,
              THRESHOLD_PRESERVATION_ANALYSIS.md

---

## 1. BACKGROUND

ILT002_EXECUTION_GUIDE.md §8 Step 2 states:

> S-1 + S-2 + any one of S-3/S-4/S-5 confirmed in >= 2 of **3** archetypes?

The archetype population of "3" is not defined in ILT002_EXECUTION_GUIDE.md
or in any other committed governance document.

The committed ILT-002 operational instruments cover exactly two ideas:

| Instrument | Structure |
|---|---|
| ILT002_EMERGENCE_TIMING_TABLE.md | Part 1 (Idea A) + Part 2 (Idea B) — no Part 3 |
| ILT002_FORM_T.md | Idea A row + Idea B row — no third row |
| ILT002_FORM_A.md | Per-idea form — no Idea C form committed |
| §2.6 S-6 definition | Idea B vs Idea A comparison — no third idea |

The ARCHETYPE_RESOLUTION_OPTIONS.md analysis (2026-06-07) identified
Interpretation C as most operationally consistent with the committed
instruments: the "3" in §8 Step 2 is an authoring inconsistency, and
the ILT-002 campaign is designed around two ideas only.

This document records the owner decision to treat "3" as an authoring
inconsistency and to correct the operational application of §8 Step 2
for ILT-002, without redesigning the campaign.

---

## 2. FINDING OF AUTHORING INCONSISTENCY

**Finding:** The number "3" in §8 Step 2 (">= 2 of 3 archetypes") is
inconsistent with every committed ILT-002 operational instrument, which
are uniformly structured for two ideas. No committed document defines a
third archetype, names it, assigns it a label, or provides an evidence
collection instrument for it.

**Basis:** ARCHETYPE_DEFINITION_DECISION_REPORT.md §1 and ARCHETYPE_RESOLUTION_OPTIONS.md §3.

**Classification:** Authoring inconsistency — unless contradicted by a
higher-authority document.

**Higher-authority check:** ILT002_MEASUREMENT_SCOPE_REVIEW §5.3 has been
verified. It repeats the §8 classification language and introduces no
independent population definition. See Section 8, Risk 1 — CLEARED.

The finding stands.

---

## 3. DECISION

For ILT-002 final classification purposes:

**The archetype population is the two ideas governed by committed
ILT-002 instruments: Idea A and Idea B.**

The "3" in §8 Step 2 is treated as an authoring inconsistency for
ILT-002. It is not silently reinterpreted. It is corrected by this
owner decision record, which is committed to the repository alongside
the other ILT-002 governance artifacts and references the evidence base
that supports the correction.

This correction applies to ILT-002 only. It does not set a precedent
for future campaigns, which may be designed with three or more archetypes.

**Threshold correction — explicit owner choice:**

THRESHOLD_PRESERVATION_ANALYSIS.md (2026-06-07) identified that correcting
the denominator from 3 to 2 does not automatically determine the numerator.
Two options were identified as repository-consistent: 2 of 2 (absolute count
and redundancy preserved) and 1 of 2 (failure tolerance preserved).

The owner has explicitly chosen: **>= 2 of 2 governed ideas.**

**Owner rationale (recorded verbatim):**
This choice preserves the absolute numerator, redundancy, and majority logic
more safely than a 1 of 2 correction. It avoids allowing a final positive
classification from a single idea only.

**Consequence acknowledged by owner:**
This is stricter than the original "2 of 3" structure because it removes
failure tolerance — neither idea may fail the threshold. That consequence
is accepted intentionally to protect evidence quality.

The option "1 of 2" was considered and rejected. It is not an available
interpretation for ILT-002 under this decision.

---

## 4. SCOPE OF CORRECTION

The following are **unchanged** by this decision:

- Signal definitions S-1 through S-6 (ILT002_EXECUTION_GUIDE.md §2)
- Behavioral anchors (ILT002_EXECUTION_GUIDE.md §2.1 through §2.6)
- Specificity test (ILT002_EXECUTION_GUIDE.md §5)
- Newness marker protocol (ILT002_EXECUTION_GUIDE.md §6)
- §8 Steps 1, 3, 4, and 5
- All existing signal classifications for Sessions 3 and 4
- All committed ILT-002 evidence instruments
- ILT002_EMERGENCE_TIMING_TABLE.md structure
- ILT002_FORM_T.md structure
- ILT002_FORM_A.md structure
- Decision D-1 (same participant for Idea A and Idea B)

The following is **corrected** by this decision:

- §8 Step 2: `>= 2 of 3 archetypes` → `>= 2 of 2 governed ideas` for ILT-002 only
  (Both the population label and the denominator are corrected; the numerator
  is preserved at 2 by explicit owner choice, not by default)

No new archetypes are designed. No Idea C is created. No third evidence
instrument is required.

---

## 5. WHAT §8 STEP 2 BECOMES OPERATIONALLY UNDER THIS CORRECTION

**Original text (ILT002_EXECUTION_GUIDE.md §8 Step 2):**
> S-1 + S-2 + any one of S-3/S-4/S-5 confirmed in >= 2 of 3 archetypes?

**Threshold option considered and rejected:**
"1 of 2" — would have required only one of Idea A or Idea B to satisfy
the threshold. Rejected by owner decision because it removes redundancy,
allows a positive classification from a single idea, and is weaker than
the original 2/3 evidentiary standard.

**Operational reading for ILT-002 under this correction:**
> S-1 + S-2 + any one of S-3/S-4/S-5 confirmed in >= 2 of 2 governed ideas?

Equivalently:
> S-1 confirmed in Idea A AND S-1 confirmed in Idea B
> AND S-2 confirmed in Idea A AND S-2 confirmed in Idea B
> AND at least one of S-3/S-4/S-5 confirmed in Idea A
> AND at least one of S-3/S-4/S-5 confirmed in Idea B?
> If YES to all → YES → proceed to Step 3
> If NO to any → NO → IDEA DEVELOPMENT PLATFORM

Steps 1, 3, 4, and 5 are applied exactly as written in §8 with the
substitution that "archetype" throughout means Idea A or Idea B.

**Step 4 arithmetic note:** If F-3 is confirmed for one idea and that
idea is excluded, Step 2 recalculates across the remaining one idea.
The effective threshold becomes 1 of 1 — that single idea must satisfy
the full threshold alone. This is a more demanding standard than the
original 2 of 3 after one exclusion (which would have been 2 of 2).
This consequence is accepted as inherent to a two-idea campaign design.

---

## 6. EVIDENCE REQUIRED BEFORE FINAL CLASSIFICATION

The following evidence remains required before §8 can be applied.
This list is unchanged by the correction.

| Evidence item | Current status |
|---|---|
| Idea A sessions executed (minimum 2) | NOT YET RUN |
| Idea A signals S-1 through S-5 classified per §2 anchors | NOT YET DONE |
| Idea A timing table (Part 1) populated and locked per §9 Rule 5 | NOT YET DONE |
| S-6 evaluated using FORM T after Idea A lock | NOT YET DONE |
| F-3 check for both Idea A and Idea B | NOT YET DONE |
| ILT002_MEASUREMENT_SCOPE_REVIEW §5.3 qualification statement identified | NOT YET DONE |
| ILT002_MEASUREMENT_SCOPE_REVIEW §5.3 verified not to contradict two-idea population | **CLEARED — verified by owner 2026-06-07** |

Idea B evidence (Sessions 3 and 4) is complete and valid.
No re-collection or reclassification of Idea B evidence is required.

---

## 7. EXISTING EVIDENCE STATUS

**Session 3 (SID: 34d3a4a1) — VALID. No change required.**
Signal record: S-2 CONFIRMED, S-4 CONFIRMED, S-1/S-3/S-5 NOT CONFIRMED.
This constitutes the Idea B signal record. It stands unchanged.

**Session 4 (SID: 294faf4f) — VALID. No change required.**
Signal record: S-2 CONFIRMED, S-4 CONFIRMED, S-1/S-3/S-5 NOT CONFIRMED.
Correction note committed at c3f1199. Premature verdict withdrawn.

**Idea B threshold status under corrected §8 Step 2:**
S-1 is NOT CONFIRMED for Idea B. Under the corrected threshold, Idea B
does not independently satisfy Step 2 (S-1 required). This is unchanged
from the pre-correction analysis. The correction does not rescue Idea B's
threshold status — it only changes the denominator, not the signal record.

**FACT:** For the corrected §8 Step 2 to return YES, Idea A must
independently produce S-1 confirmed, S-2 confirmed, and at least one
of S-3/S-4/S-5 confirmed. Idea B's current S-1 absence means the
threshold requires Idea A to satisfy the full requirement — and Idea B
must also satisfy it. Both must satisfy it under a 2 of 2 threshold.

---

## 8. RISKS OF THIS CORRECTION

### Risk 1 — Higher-authority document conflict — CLEARED

ILT002_MEASUREMENT_SCOPE_SECTION53.md has been read. It does not define
the archetype population independently. It repeats §8 classification
language only. No conflict exists.

### Risk 2 — Correction removes failure tolerance (acknowledged consequence)

Under the original "2 of 3," one idea failing the threshold could be
rescued by a third idea satisfying it. Under the corrected "2 of 2,"
both ideas must satisfy the threshold with no rescue path. If either idea
does not satisfy the full threshold (particularly S-1), the final verdict
is IDEA DEVELOPMENT PLATFORM with no further recourse within the ILT-002
campaign design.

**Owner rationale for accepting this consequence (recorded):**
Preserving absolute numerator, redundancy, and majority logic more safely
than 1 of 2. Avoiding a positive classification resting on a single idea.
The increased strictness intentionally protects evidence quality.

### Risk 3 — F-3 exclusion creates a 1 of 1 threshold

If F-3 contaminates one idea and it is excluded per §8 Step 4, the
remaining single idea must satisfy the threshold alone. Under the
original "3 archetypes," one exclusion left a "2 of 2" recalculation.
Under the corrected "2 archetypes," one exclusion leaves a "1 of 1"
recalculation. This is a materially more demanding fallback standard.

### Risk 4 — ILT-002-only scope must be enforced

This correction must not be interpreted as establishing that all
measurement campaigns use a two-idea population. The correction is
explicitly scoped to ILT-002. Future campaigns may be designed for
three or more archetypes and must define their own population.

### Risk 5 — The "3" may have been intentional

"3 archetypes" in §8 may have been drafted when an Idea C was planned
and subsequently dropped without updating §8. If so, this correction
accurately reflects the current campaign scope. Alternatively, dropping
Idea C may itself have been an oversight. If Idea C was dropped
intentionally, the correction is correct. If it was dropped by error,
this correction permanently removes a safeguard. This ambiguity cannot
be resolved from committed documents alone.

---

## 9. WHAT THIS DECISION DOES NOT AUTHORIZE

- Designing a third archetype or Idea C
- Modifying signal anchors §2.1 through §2.6
- Modifying S-1 through S-6 definitions
- Reclassifying Sessions 3 or 4 signal records
- Running Idea A sessions (separate authorization required)
- Issuing a final platform classification
- Applying §8 to incomplete evidence

---

## 10. SIGN-OFF

This document has been reviewed and approved by the owner on 2026-06-07.
It takes effect upon commit to the repository.

Pre-commit checklist — all items resolved:

1. ILT002_MEASUREMENT_SCOPE_REVIEW §5.3 read and confirmed — does not
   define the archetype population as three. Risk 1 CLEARED.
2. Threshold choice of 2 of 2 recorded as explicit owner decision.
   Alternative 1 of 2 considered and rejected. Removal of failure
   tolerance accepted intentionally.
3. F-3 exclusion consequence acknowledged — one exclusion produces
   1 of 1 recalculation.

---

*Owner approved 2026-06-07. In effect upon commit.*
*No new archetype design. No signal anchor changes.*
*No modification to S-1 through S-6 definitions.*
*Existing evidence preserved and valid.*
