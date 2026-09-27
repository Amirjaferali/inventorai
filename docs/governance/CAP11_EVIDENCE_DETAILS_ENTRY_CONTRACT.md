# CAP-11 — EVIDENCE QUALITY LADDER
## ENTRY CONTRACT + SLICE 1 — EVIDENCE DETAILS

**STATUS:** OWNER-APPROVED FOR CAP-11 SLICE 1 ONLY.

**BASE:** `feature/atomic-json-session-persistence`
at `a9e46e57e1d9595fdc92af0bb508ee3fd141c9ea`.

This is the separate Owner-approved CAP-11 contract required by the Capability
Enrichment Register.

Approval of this exact contract authorizes ONLY:

**CAP-11 Slice 1 — Evidence Details.**

**FULL CAP-11 — Evidence Quality Ladder remains NOT AUTHORIZED.**

---

## 1. CAPABILITY / SLICE

Full capability:

**CAP-11 — Evidence Quality Ladder**

Authorization state:

**FULL CAP-11: NOT AUTHORIZED.**

Authorized bounded slice:

**CAP-11 Slice 1 — Evidence Details**

Slice 1 is **PRESENTATION ONLY**.

---

## 2. PRODUCT VALUE

For an existing evidence item, help the inventor understand separately:

- its evidence form;
- its source metadata;
- its validation status.

These facts must remain separate.

They must NOT be combined into a score, rank, tier, confidence value or overall
evidence-strength verdict.

---

## 3. CANONICAL OWNERS

The existing owners remain unchanged.

### Evidence-form / quality vocabulary

Owner:

`engine/idea_state.py`

### Canonical quality ordering

Owner:

`engine/evidence_order.py`

### Provenance vocabulary

Owner:

`engine/idea_state.py`

### Validation vocabulary

Owner:

`engine/idea_state.py`

### Evidence carriers / Section-2 package fields

Owner:

`engine/deliverable_assembler.py`

### Readiness

Owner:

`engine/derived_readiness.py`

### Commercial / Manufacturing evidence

Existing owners remain unchanged and are OUT OF SCOPE for Slice 1.

CAP-11 must not create a second evidence owner.

---

## 4. THREE ORTHOGONAL AXES

### A. FORM

Canonical values:

- `ASSERTED`
- `REASONED`
- `DEMONSTRATED`

Meaning:

the existing evidence-form / reasoning-structure classification.

The existing canonical internal order:

`ASSERTED < REASONED < DEMONSTRATED`

remains owned exclusively by:

`engine/evidence_order.py`

That order remains INTERNAL.

Slice 1 MUST NOT display that order as:

- an Evidence Quality score;
- a strength score;
- a tier;
- a level;
- a colour scale;
- a recommendation;
- a confidence measure.

Form does NOT determine Source.

Form does NOT determine Validation.

---

### B. SOURCE

Canonical provenance values:

- `OWNER_STATED`
- `SYSTEM_INFERRED`
- `EXPERT_SUPPLIED`
- `EXTERNAL_EVIDENCE`
- `LEGACY_UNSPECIFIED`

Meaning:

where the record / evidence came from according to canonical provenance
metadata.

Source is NOT an evidence-strength ranking.

No provenance value automatically grants Validation.

Examples:

`EXPERT_SUPPLIED`

does NOT automatically mean:

`SPECIALIST_REVIEWED`.

`EXTERNAL_EVIDENCE`

does NOT automatically mean:

`INDEPENDENTLY_VERIFIED`.

`OWNER_STATED`

does NOT automatically mean:

weak evidence.

---

### C. VALIDATION

Canonical values:

- `UNVALIDATED`
- `SPECIALIST_REVIEWED`
- `EMPIRICALLY_DEMONSTRATED`
- `INDEPENDENTLY_VERIFIED`

Meaning:

the canonical Validation status recorded for that item.

Validation is independent of:

- Form;
- Source.

Slice 1 creates NO new ordering among:

- `SPECIALIST_REVIEWED`;
- `EMPIRICALLY_DEMONSTRATED`;
- `INDEPENDENTLY_VERIFIED`.

They must not be displayed as a first / second / third hierarchy.

---

## 5. NO CROSS-AXIS LADDER

Never combine:

**Form + Source + Validation**

into any of the following:

- number;
- percentage;
- confidence score;
- LOW / MEDIUM / HIGH;
- weak / strong;
- tier;
- colour ranking;
- badge ranking;
- readiness score;
- overall evidence score.

No cross-axis weighting exists.

None is introduced by this Slice.

---

## 6. USER-FACING PRESENTATION

Group heading:

**EN:**
`About this evidence`

**AR:**
`عن هذا الدليل`

Do NOT call the group:

`Evidence Standing`

because `Standing` already has an existing narrower meaning elsewhere in the
product.

The three rows are:

### EN

- `Form`
- `Source`
- `Validation`

### AR

- `الصيغة`
- `المصدر`
- `التحقق`

Raw canonical enum tokens remain internal.

---

## 7. FORM PRESENTATION

User-facing Form values use bounded plain-language presentation of the existing
canonical Form value.

### ASSERTED

EN:
`Asserted`

AR:
natural Arabic equivalent.

### REASONED

EN:
`Reasoned`

AR:
natural Arabic equivalent.

### DEMONSTRATED

EN:
`Demonstrated`

AR:
natural Arabic equivalent.

Provide one short explanatory note making clear that:

**Form describes the evidence-form / reasoning-structure classification and does
NOT mean the evidence has been validated.**

Do NOT reuse the current `_QUALITY_LABELS` wording for this Slice.

Reason:

the existing `_QUALITY_LABELS` wording currently mixes Form with Source and/or
Validation semantics.

This Slice must keep those axes separate.

---

## 8. SOURCE PRESENTATION

### OWNER_STATED

EN:
`You`

AR:
`أنت`

### SYSTEM_INFERRED

EN:
`System-derived`

AR:
natural Arabic equivalent.

### EXPERT_SUPPLIED

EN:
`Expert-supplied`

AR:
natural Arabic equivalent.

### EXTERNAL_EVIDENCE

EN:
`External evidence`

AR:
natural Arabic equivalent.

### LEGACY_UNSPECIFIED

EN:

`Source metadata not available`

AR:

`بيانات المصدر غير متاحة`

`LEGACY_UNSPECIFIED` must NOT be silently reclassified as:

- OWNER_STATED;
- expert supplied;
- external evidence;
- weak;
- strong;
- validated.

Do NOT show:

`pre-provenance session`

for this Slice.

An unknown or unrecognised Source value must display:

EN:
`Not available`

AR:
`غير متاح`

It must NOT be coerced to a canonical Source value.

---

## 9. VALIDATION PRESENTATION

### UNVALIDATED

EN:

`No validation recorded`

AR:

`لا يوجد تحقق مسجّل`

Do NOT say:

`nobody checked it`

or equivalent.

The canonical state proves only that no canonical Validation is recorded.

It does NOT prove what any person outside InventorAI may or may not have done.

### SPECIALIST_REVIEWED

EN:
`Reviewed by a specialist`

AR:
natural Arabic equivalent.

### EMPIRICALLY_DEMONSTRATED

EN:
`Empirically demonstrated`

AR:
natural Arabic equivalent.

### INDEPENDENTLY_VERIFIED

EN:
`Independently verified`

AR:
natural Arabic equivalent.

These are neutral labels.

Slice 1 introduces no ordering among them.

Unknown or unrecognised Validation:

EN:
`Not available`

AR:
`غير متاح`

Never coerce an unknown Validation value to:

`UNVALIDATED`.

---

## 10. SLICE-1 CARRIERS / SURFACE

Eligible carriers:

Report Section 2:

- Known Problem;
- Known Mechanism.

Use only Evidence fields already present in the assembled package.

The same Evidence Details presentation may appear in the PDF because the PDF
uses the same report template.

Out of scope:

- Section 9;
- live session page;
- safety-signal presentation;
- Commercial Evidence;
- Manufacturing Evidence;
- assertion-ledger UI;
- Requirement Landscape;
- Validation Plan.

Do NOT create a new numbered report section.

Enhance the existing Section-2 evidence presentation only.

---

## 11. EMPTY / FAIL-CLOSED BEHAVIOUR

### No Evidence item

Retain existing no-evidence behavior.

Render no CAP-11 metadata rows.

### Missing / malformed / unrecognised metadata

Only the affected row displays:

EN:
`Not available`

AR:
`غير متاح`

Do NOT expose exception text.

Unavailable must never silently become:

- `UNVALIDATED`;
- `OWNER_STATED`;
- `LEGACY_UNSPECIFIED`;
- an evidence tier;
- a score;
- a readiness conclusion.

---

## 12. CURRENT WRITER REALITY

Slice 1 creates NO writer.

Representation of canonical vocabulary is NOT authority to mint its values.

Current live assertion flows retain their existing writer authorization.

Slice 1 does NOT authorize:

- Validation promotion;
- new provenance assignment;
- evidence-quality promotion;
- Specialist Review capture;
- empirical-validation capture;
- independent-verification capture.

No promotion workflow is authorized.

---

## 13. READINESS / STATE BOUNDARY

CAP-11 Slice 1 MUST NOT change:

- derived readiness;
- maturity;
- progression;
- gap lifecycle;
- evidence records;
- provenance;
- validation;
- Form / quality;
- persistence;
- replay;
- schema;
- package semantics.

Rendering Evidence Details has ZERO state authority.

The existing behavior of:

`engine/derived_readiness.py`

remains unchanged.

---

## 14. PACKAGE / EXPORT BOUNDARY

Slice 1 is a PRESENTATION of fields already available in the existing assembled
package.

Do NOT alter the canonical package or JSON export merely to implement this
Slice.

Existing package / JSON output must remain unchanged.

---

## 15. COMMERCIAL / MANUFACTURING BOUNDARY

Commercial Evidence and Manufacturing Evidence remain unchanged.

Their current:

- provenance semantics;
- claim-status semantics;
- `Standing` terminology;
- writers;
- rendering;

are not modified by CAP-11 Slice 1.

CAP-11 does not create a commercial-specific or manufacturing-specific evidence
ladder.

---

## 16. LANGUAGE

Preserve the Owner policy:

**ARABIC-FIRST UX, NOT ARABIC-ONLY TERMINOLOGY.**

Arabic chrome and explanatory prose should be Arabic.

Precise English technical terminology may remain English where that improves
technical precision or readability.

Inventor-authored content remains verbatim.

No live:

- MSNL;
- LLM;
- provider;

is authorized.

---

## 17. ACCEPTANCE CRITERIA

1. Each present Known Problem / Known Mechanism Evidence item in Report Section
   2 displays:

   - Form;
   - Source;
   - Validation.

2. Values derive only from the already assembled Evidence fields.

3. Form, Source and Validation remain visibly separate.

4. No combined score, ranking, tier, weighting or cross-axis evidence-strength
   verdict exists.

5. `LEGACY_UNSPECIFIED` displays:

   `Source metadata not available`

   / `بيانات المصدر غير متاحة`

   and is not reclassified.

6. `UNVALIDATED` displays:

   `No validation recorded`

   / `لا يوجد تحقق مسجّل`.

7. Unrecognised Form, Source or Validation fails closed to:

   `Not available`

   / `غير متاح`.

8. No raw canonical token appears in user-facing report or PDF HTML.

9. The existing canonical package / JSON output remains unchanged.

10. Readiness remains unchanged.

11. Maturity remains unchanged.

12. Progression remains unchanged.

13. Gap state remains unchanged.

14. Stored state remains unchanged.

15. Commercial Evidence rendering and semantics remain unchanged.

16. Manufacturing Evidence rendering and semantics remain unchanged.

17. Section 9 remains unchanged.

18. Session UI remains unchanged.

19. EN rendering is coherent.

20. AR / RTL rendering is coherent.

---

## 18. NON-GOALS

This Slice does NOT authorize:

- Full CAP-11 Evidence Quality Ladder;
- ladder scores;
- ladder levels;
- new evidence-strength categories;
- evidence promotion;
- Validation writers;
- provenance writers;
- Form / quality writers;
- Section-9 expansion;
- session-page expansion;
- CAP-06;
- Stage 23;
- AI / LLM / provider integration.

---

## 19. AUTHORIZATION BOUNDARY

Approval of this exact contract authorizes ONLY:

**CAP-11 Slice 1 — Evidence Details.**

FULL CAP-11 remains:

**NOT AUTHORIZED.**

Every future:

- ladder level;
- promotion workflow;
- Validation writer;
- evidence-strength conclusion;
- additional surface;

requires separate authorization.
