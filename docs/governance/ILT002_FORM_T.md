# ILT002_FORM_T.md
# Type: Evidence Instrument — Transfer Event Record
# Status: DRAFT — PENDING OWNER AUTHORIZATION BEFORE COMMIT
# Authored: 2026-06-05
# Specification: ILT002_AUTHORING_SPECIFICATION.md — Artifact 3
# Governing documents: ILT002_EXECUTION_GUIDE.md §2.4, §2.6, §3, §5, §9 Rules 5, 6
#                      STAGE3_CAPABILITY_MODEL.md §5.3
# Owner decisions applied: T-1, T-2, T-3

---

## HEADER

Campaign ID:   ___
Reviewer ID:   ___
Ideas covered: Idea A / Idea B / BOTH [populate as sessions occur]

SCOPE (T-1): This form covers both:
  Section A — M-3 Transfer of Reasoning (within-session, within-idea)
  Section B — S-6 Cross-Idea Transfer (cross-session, cross-idea)

ADMINISTRATION (T-2): Observer record only.
No challenge is administered to the inventor.
All entries record spontaneous events as defined in §2.4.

---

## SECTION A — M-3 TRANSFER OF REASONING
## Within-session. Within-idea. One entry per observed transfer event.
## Observer record — events are not elicited (T-2).

M-3 qualifying criteria (§2.4):
  REQUIRES: Inventor applies reasoning from one gap type to another
            WITHOUT the second question requiring it.
  REQUIRES: Explicit or inferable cross-gap reference present.
  DISQUALIFIES: "like I said before" without identifying prior gap.
  DISQUALIFIES: Second question required the transfer.

---

### EVENT RECORD — [copy block for each observed M-3 candidate event]

Event ID:                       M3-[session]-[iteration]-[sequence]
Session №:                      ___
Iteration № within session:     ___
Idea:                           Idea A / Idea B
Iteration Template record ref:  IT-[campaign]-[session]-[iteration]

Source gap type:                MC / PF / BA / PMF / AI / EGA
Target gap type:                MC / PF / BA / PMF / AI / EGA
Transfer description:           ___ [one sentence — factual, no interpretation]

Explicit cross-gap reference present:   YES / NO
Inferable cross-gap reference present:  YES / NO
[At least one must be YES for M-3 to qualify — §2.4]

Second question required this transfer: YES / NO
[If YES: M-3 does NOT qualify]

Specificity test (§5):          MECHANISM-SPECIFIC / GENERIC
[If GENERIC: M-3 does NOT qualify]

Protocol learning check (STAGE3_CAPABILITY_MODEL §5.3):
Correct isolated response, fails under integration probing: YES / NO
[If YES: record as PROTOCOL LEARNING below — not M-3]

Classification:                 CONFIRMED / CONTESTED / NOT QUALIFIED / PROTOCOL LEARNING
If CONTESTED: both sides recorded: ___
Disconfirming evidence (required if CONFIRMED — §9 Rule 3): ___

---
[End of M-3 event block — repeat for each observed candidate event]
---

### Section A Summary
## Completed after all sessions for each idea are complete.

| Idea | M-3 CONFIRMED count | M-3 CONTESTED count | M-3 NOT QUALIFIED count | PROTOCOL LEARNING count |
|------|--------------------|--------------------|------------------------|------------------------|
| Idea A | ___ | ___ | ___ | ___ |
| Idea B | ___ | ___ | ___ | ___ |

---

## SECTION B — S-6 CROSS-IDEA TRANSFER
## Cross-session. Cross-idea.
## Completed after all Idea B sessions are complete.
## Requires: FORM A Section C complete + Emergence Timing Table Idea A locked.

S-6 qualifying criteria (§2.6):
  REQUIRES ALL THREE:
    Condition 1: Earlier emergence in Idea B vs Idea A (quantified by iteration)
    Condition 2: Idea B-specific content (passes specificity test §5)
    Condition 3: Not explained by false positive conditions

---

### Cross-Reference Record (T-3)

FORM A Idea A record reference:           ___
FORM A Idea B record reference:           ___
Emergence Timing Table reference:         ___
Idea A timing table lock confirmed:       YES / NO
Lock date:                                ___

[Section B must not be completed if Idea A timing table is not locked]

---

### Condition 1 — Earlier Emergence in Idea B vs Idea A

Source: Emergence Timing Table — Part 3 comparison section

Stage 3 comparison results (primary — §3):

| Behavior | Idea A first appearance (S№/I№) | Idea B first appearance (S№/I№) | Result |
|----------|--------------------------------|--------------------------------|--------|
| Assumption surfacing | ___ | ___ | EARLIER / LATER / EQUAL / NOT COMPARABLE |
| Boundary articulation | ___ | ___ | EARLIER / LATER / EQUAL / NOT COMPARABLE |
| Expertise gap naming | ___ | ___ | EARLIER / LATER / EQUAL / NOT COMPARABLE |

NOT COMPARABLE = either value is NOT OBSERVED (ETT-2: NULL does not count in either direction)

Behaviors showing EARLIER (excluding NOT COMPARABLE): ___ of ___ comparable
Threshold: >= 2 of comparable behaviors showing EARLIER
Condition 1 status: MET / NOT MET / INSUFFICIENT DATA
[INSUFFICIENT DATA = fewer than 2 comparable behaviors]

---

### Condition 2 — Idea B-Specific Content

For each behavior showing EARLIER — specificity test (§5):

| Behavior | Result | Specificity test |
|----------|--------|-----------------|
| Assumption surfacing | EARLIER / NOT APPLICABLE | MECHANISM-SPECIFIC / GENERIC / NOT OBSERVED |
| Boundary articulation | EARLIER / NOT APPLICABLE | MECHANISM-SPECIFIC / GENERIC / NOT OBSERVED |
| Expertise gap naming | EARLIER / NOT APPLICABLE | MECHANISM-SPECIFIC / GENERIC / NOT OBSERVED |

Condition 2 status: MET (all EARLIER behaviors pass specificity) / NOT MET

---

### Condition 3 — False Positive Exclusion (§2.6 — all four required)

| False positive condition | Assessment | Notes |
|--------------------------|-----------|-------|
| Domain familiarity difference | EXCLUDED / CANNOT EXCLUDE / N/A | ___ |
| Warmup effect | EXCLUDED / CANNOT EXCLUDE / N/A | ___ |
| Verbatim reuse of Idea A phrases | EXCLUDED / CANNOT EXCLUDE / N/A | ___ |
| Protocol learning | EXCLUDED / CANNOT EXCLUDE / N/A | ___ |

Condition 3 status: MET (all EXCLUDED) / NOT MET / CONTESTED
[CONTESTED = any condition CANNOT EXCLUDE]

---

### S-6 Final Status

| Condition | Status |
|-----------|--------|
| Condition 1 — Earlier emergence | MET / NOT MET / INSUFFICIENT DATA |
| Condition 2 — Idea B-specific content | MET / NOT MET |
| Condition 3 — False positive exclusion | MET / NOT MET / CONTESTED |

S-6 final status:
  CONFIRMED        = all three conditions MET
  CONTESTED        = conditions 1 and 2 MET + condition 3 CONTESTED
  NOT CONFIRMED    = any condition NOT MET
  INSUFFICIENT DATA = condition 1 INSUFFICIENT DATA

S-6 final status: CONFIRMED / CONTESTED / NOT CONFIRMED / INSUFFICIENT DATA

Section B completed by: ___   Date: ___

---

*M-3 requires spontaneous transfer without question elicitation (T-2).*
*S-6 requires all three conditions (§2.6). CONTESTED signals do not count for or against (§9 Rule 6).*
*NULL is not evidence of later emergence (ETT-2).*
