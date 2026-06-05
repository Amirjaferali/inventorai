# ILT002_ITERATION_TEMPLATE.md
# Type: Evidence Instrument — Per-Iteration Evidence Record (Authoritative)
# Status: DRAFT — PENDING OWNER AUTHORIZATION BEFORE COMMIT
# Authored: 2026-06-05
# Specification: ILT002_AUTHORING_SPECIFICATION.md — Artifact 4
# Governing documents: ILT002_EXECUTION_GUIDE.md §1.3, §1.4, §2.1–2.6, §3, §5, §6, §9 Rules 1–7
#                      PRE_ILT002_BASELINE_FREEZE.md §2.1
# Owner decisions applied: A-3, IT-1, IT-2, IT-3

---

## INSTRUMENT AUTHORITY (A-3)

This is the authoritative per-iteration evidence record.
Full inventor response text lives here only.
FORM A, FORM T, and Emergence Timing Table cross-reference this record by Record ID.
Do not duplicate response text in any other instrument.

---

## ITERATION RECORD — [copy this entire block for each iteration]

---

### RECORD HEADER

Record ID:          IT-[campaign]-[session]-[iteration]
Campaign ID:        ___
Session №:          ___
Iteration № within session: ___
Idea identifier:    ___
Stage:              STAGE 1 / STAGE 2 / STAGE 3
Reviewer ID:        ___
Record date:        ___

---

### ENGINE STATE — START OF ITERATION (IT-3, PRE_ILT002_BASELINE_FREEZE §2.1)

Maturity level at iteration start:      0 / 1 / 2
Current stage at iteration start:       1 / 2 / 3

Gap statuses at iteration start:
  MC  (Mechanism Completeness):         OPEN / PARTIAL / CLOSED / NOT YET ACTIVE
  PF  (Physical Feasibility):           OPEN / PARTIAL / CLOSED / NOT YET ACTIVE
  BA  (Boundary Ambiguity):             OPEN / PARTIAL / CLOSED / NOT YET ACTIVE
  PMF (Problem Mechanism Fit):          OPEN / PARTIAL / CLOSED / NOT YET ACTIVE
  AI  (Assumption Inventory):           OPEN / PARTIAL / CLOSED / NOT YET ACTIVE
  EGA (Expertise Gap Awareness):        OPEN / PARTIAL / CLOSED / NOT YET ACTIVE

Gap addressed this iteration:           [gap name] / NONE

---

### QUESTION DELIVERED (IT-1 — prompt contamination auditability)

Question ID (if Stage 3, from STAGE3_QUESTION_SET.md): ___
Question type:      PRIMARY / CONDITIONAL_PROBE / DOMAIN-SPECIFIC / GENERIC FALLBACK
Question text as delivered: [verbatim]

Prompt contamination risk assessment:
  Does this question mention or imply any concept relevant to S-3 (AI-E3)
  or S-5 (M-4) assessment?          YES / NO
  If YES — affected signal IDs:     ___

---

### INVENTOR RESPONSE — FULL TEXT (§9 Rule 1)
## Record complete before writing any annotation. No exceptions.

[Full verbatim response recorded here]

Response length (characters):  ___
Response recorded:             YES
Timestamp:                     ___

---

### ENGINE STATE — END OF ITERATION (IT-3)

Gap status change this iteration:
  [gap name]: [prior status] → [new status]   /   UNCHANGED
Maturity level after iteration:    0 / 1 / 2
Current stage after iteration:     1 / 2 / 3

---

### SIGNAL ANNOTATIONS
## Recorded after full response is captured (§9 Rule 1).
## All six signals assessed every iteration.
## If signal not applicable this iteration: mark N/A with explicit reason.

---

**S-1 — SELF-CORRECTION (§2.1, §3)**

Revision marker present:               YES — Tier: 1 / 2 / 3   /   NO
Marker phrase (if present):            ___
Prior claim identified:                ___
Logical contradiction present:         YES / NO
Classification:                        CONFIRMED / NOT CONFIRMED / CONTESTED / N/A
If N/A — reason:                       ___
Disconfirming evidence:                ___ [required if CONFIRMED — §9 Rule 3]
FORM A cross-reference:                ___

---

**S-2 — OWNERSHIP GROWTH (§2.2)**

Limitation named:                      ___
Specificity test (§5):                 MECHANISM-SPECIFIC / GENERIC
  If GENERIC: classification = NOT CONFIRMED
Named before this session:             YES / NO
Classification:                        CONFIRMED / NOT CONFIRMED / CONTESTED / N/A
If N/A — reason:                       ___
Disconfirming evidence:                ___ [required if CONFIRMED]
FORM A cross-reference:                ___

---

**S-3 — UNKNOWN AWARENESS / AI-E3 (§2.3, §6)**

Newness marker present:                YES — Tier: 1 / 2 / 3   /   NO
Marker phrase (if present):            ___
Prompt contamination check (§2.3, §6):
  Did question mention or imply this concept?  YES / NO
  If YES: classification = PROMPTED RECOGNITION (not AI-E3)
Classification:                        CONFIRMED / PROMPTED RECOGNITION / NOT CONFIRMED / CONTESTED / N/A
If N/A — reason:                       ___
Disconfirming evidence:                ___ [required if CONFIRMED]
FORM A cross-reference:                ___

---

**S-4 — TRANSFER OF REASONING / M-3 (§2.4)**

Cross-gap reference:                   EXPLICIT / INFERABLE / ABSENT
Source gap:   ___     Target gap:      ___
Second question required transfer:     YES / NO
  If YES: classification = NOT QUALIFIED
Specificity test (§5):                 MECHANISM-SPECIFIC / GENERIC
  If GENERIC: classification = NOT QUALIFIED
Protocol learning check (STAGE3_CAPABILITY_MODEL §5.3):
  Correct isolated response, fails under integration probing: YES / NO
  If YES: classification = PROTOCOL LEARNING
Classification:                        CONFIRMED / CONTESTED / NOT QUALIFIED / PROTOCOL LEARNING / N/A
If N/A — reason:                       ___
Disconfirming evidence:                ___ [required if CONFIRMED]
FORM T reference (if CONFIRMED or CONTESTED): M3-[session]-[iteration]-[seq]
FORM A cross-reference:                ___

---

**S-5 — INVENTOR INDEPENDENCE / M-4 (§2.5)**

Gap type named unprompted:             YES / NO
Gap type named:                        ___
Mechanism-specific language (§5):      YES / NO
  If NO: classification = NOT CONFIRMED
Timing:                                first-response / mid-session / late-session
  If first-response: classification = NOT CONFIRMED (§2.5)
Classification:                        CONFIRMED / NOT CONFIRMED / CONTESTED / N/A
If N/A — reason:                       ___
Disconfirming evidence:                ___ [required if CONFIRMED]
FORM A cross-reference:                ___

---

**S-6 — CROSS-IDEA TRANSFER TIMING INPUT (§2.6)**

Note: S-6 final classification is performed in FORM T Section B after all
sessions complete. This field records emergence timing inputs only.

Behavior first-appearance check this iteration:

  Assumption surfacing:
    Status:    FIRST APPEARANCE / PRIOR APPEARANCE / NOT OBSERVED
    If FIRST APPEARANCE: specificity test (§5): MECHANISM-SPECIFIC / GENERIC
    ETT update required:  YES / NO
    ETT reference:        ___

  Boundary articulation:
    Status:    FIRST APPEARANCE / PRIOR APPEARANCE / NOT OBSERVED
    If FIRST APPEARANCE: specificity test (§5): MECHANISM-SPECIFIC / GENERIC
    ETT update required:  YES / NO
    ETT reference:        ___

  Expertise gap naming:
    Status:    FIRST APPEARANCE / PRIOR APPEARANCE / NOT OBSERVED
    If FIRST APPEARANCE: specificity test (§5): MECHANISM-SPECIFIC / GENERIC
    ETT update required:  YES / NO
    ETT reference:        ___

---

### ITERATION RECORD SIGN-OFF (§1.4)

All signal blocks complete or marked N/A with reason:    YES
Emergence timing updated where required:                 YES / N/A
FORM A updated with cross-references:                    YES / N/A
FORM T updated if M-3 event recorded:                    YES / N/A

Reviewer: ___     Date: ___

---

### CORRECTION PROTOCOL (§9 Rule 4)
## Factual corrections only. Append below — do not overwrite.
## Each correction must be initialed and dated.

| Date | Reviewer initials | Field corrected | Original value | Corrected value | Reason |
|------|-------------------|----------------|---------------|----------------|--------|
| | | | | | |

---
[End of iteration record — copy entire block for next iteration]
---

## SESSION SIGN-OFF (§1.4)
## Completed after all iterations for the session are recorded.

Session №: ___
All iteration records complete:             YES
Emergence timing table updated:             YES / N/A
Session-level observations (factual):       ___

Reviewer sign-off: "Session ___ complete."
Reviewer: ___     Date: ___

---

*This is the authoritative response capture instrument (A-3).*
*Record full response before any annotation (§9 Rule 1).*
*Do not revise past records. Factual corrections only, initialed and dated (§9 Rule 4).*
*Contested signals do not count for or against (§9 Rule 6).*
