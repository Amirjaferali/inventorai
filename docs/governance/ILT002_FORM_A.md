# ILT002_FORM_A.md
# Type: Evidence Instrument — Idea Signal Classification Record
# Status: DRAFT — PENDING OWNER AUTHORIZATION BEFORE COMMIT
# Authored: 2026-06-05
# Specification: ILT002_AUTHORING_SPECIFICATION.md — Artifact 2
# Governing documents: ILT002_EXECUTION_GUIDE.md §2.1–2.6, §3, §5, §9 Rules 1–7
# Owner decisions applied: A-1, A-2, A-3, ETT-1

---

## HEADER

Campaign ID:         ___
Idea identifier:     ___
Idea description:    ___ [one line — problem + mechanism, inventor-supplied]
Domain detected:     ___
Reviewer ID:         ___
Stage scope:         BOTH (Stage 2 baseline + Stage 3 evidence — A-1)

IMPORTANT (A-3): This form holds signal classifications and cross-references only.
Full inventor response text is owned by the Iteration Evidence Template (ILT002_ITERATION_TEMPLATE.md).
Every signal classification here must reference the corresponding Iteration Template record ID.

---

## SECTION A — STAGE 2 BASELINE EVIDENCE

Purpose: Capture signal observations during Stage 2 iterations to establish
baseline inventor behavior before Stage 3 begins. Enables before/after comparison.

---

### ITERATION RECORD — [copy block for each Stage 2 iteration]

Iteration Template record ID:  IT-[campaign]-[session]-[iteration]
Session №:                     ___
Iteration № within session:    ___
Gap addressed this iteration:  MC / PF / BA / NONE
Gap status after iteration:    OPEN / PARTIAL / CLOSED

**S-1 — SELF-CORRECTION (§2.1, §3)**
Revision marker present:        YES — Tier: 1 / 2 / 3   /   NO
Marker phrase (if present):     ___
Logical contradiction of prior claim: YES / NO
Classification:                 CONFIRMED / NOT CONFIRMED / CONTESTED / N/A
Disconfirming evidence:         ___ [required if CONFIRMED — §9 Rule 3]

**S-2 — OWNERSHIP GROWTH (§2.2)**
Limitation named:               ___
Mechanism-specific (§5):        YES / NO
Named before this session:      YES / NO
Classification:                 CONFIRMED / NOT CONFIRMED / CONTESTED / N/A
Disconfirming evidence:         ___ [required if CONFIRMED]

**S-3 — UNKNOWN AWARENESS / AI-E3 (§2.3, §6)**
Newness marker present:         YES — Tier: 1 / 2 / 3   /   NO
Marker phrase (if present):     ___
Prompt contamination check:     CONTAMINATED / CLEAN
Classification:                 CONFIRMED / PROMPTED RECOGNITION / NOT CONFIRMED / CONTESTED / N/A
Disconfirming evidence:         ___ [required if CONFIRMED]

**S-4 — TRANSFER OF REASONING / M-3 (§2.4)**
Cross-gap reference:            EXPLICIT / INFERABLE / ABSENT
Source gap:   ___   Target gap: ___
Second question required transfer: YES / NO
Specificity test (§5):          MECHANISM-SPECIFIC / GENERIC
Classification:                 CONFIRMED / NOT CONFIRMED / CONTESTED / N/A
Disconfirming evidence:         ___ [required if CONFIRMED]
FORM T reference (if CONFIRMED or CONTESTED): M3-[session]-[iteration]-[seq]

**S-5 — INVENTOR INDEPENDENCE / M-4 (§2.5)**
Gap type named unprompted:      YES / NO
Gap type named:                 ___
Mechanism-specific language (§5): YES / NO
Timing:                         first-response / mid-session / late-session
[first-response does not qualify — §2.5]
Classification:                 CONFIRMED / NOT CONFIRMED / CONTESTED / N/A
Disconfirming evidence:         ___ [required if CONFIRMED]

**Emergence timing update:**
Behavior first appearance this iteration: YES / NO
If YES — update Emergence Timing Table:
  Behavior:  ___
  Stage:     STAGE 2
  ETT reference: ___

---
[End of Stage 2 iteration block — repeat for each Stage 2 iteration]
---

## SECTION B — STAGE 3 EVIDENCE

Purpose: Capture signal observations during Stage 3 iterations.
Structure identical to Section A except gap identifiers are Stage 3 gap types.

---

### ITERATION RECORD — [copy block for each Stage 3 iteration]

Iteration Template record ID:  IT-[campaign]-[session]-[iteration]
Session №:                     ___
Iteration № within session:    ___
Gap addressed this iteration:  PMF / AI / EGA / NONE
Gap status after iteration:    OPEN / PARTIAL / CLOSED

**S-1 — SELF-CORRECTION (§2.1, §3)**
Revision marker present:        YES — Tier: 1 / 2 / 3   /   NO
Marker phrase (if present):     ___
Logical contradiction of prior claim: YES / NO
Classification:                 CONFIRMED / NOT CONFIRMED / CONTESTED / N/A
Disconfirming evidence:         ___ [required if CONFIRMED — §9 Rule 3]

**S-2 — OWNERSHIP GROWTH (§2.2)**
Limitation named:               ___
Mechanism-specific (§5):        YES / NO
Named before this session:      YES / NO
Classification:                 CONFIRMED / NOT CONFIRMED / CONTESTED / N/A
Disconfirming evidence:         ___ [required if CONFIRMED]

**S-3 — UNKNOWN AWARENESS / AI-E3 (§2.3, §6)**
Newness marker present:         YES — Tier: 1 / 2 / 3   /   NO
Marker phrase (if present):     ___
Prompt contamination check:     CONTAMINATED / CLEAN
Classification:                 CONFIRMED / PROMPTED RECOGNITION / NOT CONFIRMED / CONTESTED / N/A
Disconfirming evidence:         ___ [required if CONFIRMED]

**S-4 — TRANSFER OF REASONING / M-3 (§2.4)**
Cross-gap reference:            EXPLICIT / INFERABLE / ABSENT
Source gap:   ___   Target gap: ___
Second question required transfer: YES / NO
Specificity test (§5):          MECHANISM-SPECIFIC / GENERIC
Classification:                 CONFIRMED / NOT CONFIRMED / CONTESTED / N/A
Disconfirming evidence:         ___ [required if CONFIRMED]
FORM T reference (if CONFIRMED or CONTESTED): M3-[session]-[iteration]-[seq]

**S-5 — INVENTOR INDEPENDENCE / M-4 (§2.5)**
Gap type named unprompted:      YES / NO
Gap type named:                 ___
Mechanism-specific language (§5): YES / NO
Timing:                         first-response / mid-session / late-session
Classification:                 CONFIRMED / NOT CONFIRMED / CONTESTED / N/A
Disconfirming evidence:         ___ [required if CONFIRMED]

**Emergence timing update:**
Behavior first appearance this iteration: YES / NO
If YES — update Emergence Timing Table:
  Behavior:  ___
  Stage:     STAGE 3
  ETT reference: ___

---
[End of Stage 3 iteration block — repeat for each Stage 3 iteration]
---

## SECTION C — CROSS-STAGE COMPARISON SUMMARY
## Completed after all Stage 3 sessions for this idea are complete.
## Must not be completed during sessions.

Date completed: ___
All Stage 3 sessions complete for this idea: YES

| Signal | Stage 2 confirmed count | Stage 3 confirmed count | Direction |
|--------|------------------------|------------------------|-----------|
| S-1 Self-Correction | ___ | ___ | INCREASED / UNCHANGED / DECREASED / INSUFFICIENT DATA |
| S-2 Ownership Growth | ___ | ___ | INCREASED / UNCHANGED / DECREASED / INSUFFICIENT DATA |
| S-3 Unknown Awareness | ___ | ___ | INCREASED / UNCHANGED / DECREASED / INSUFFICIENT DATA |
| S-4 Transfer of Reasoning | ___ | ___ | INCREASED / UNCHANGED / DECREASED / INSUFFICIENT DATA |
| S-5 Inventor Independence | ___ | ___ | INCREASED / UNCHANGED / DECREASED / INSUFFICIENT DATA |

Overall pattern note (factual observation only — no interpretation):
___

Section C completed by: ___   Date: ___

---

*Signal classifications are recorded here. Full response text is in the Iteration Template (A-3).*
*CONTESTED signals do not count for or against (§9 Rule 6).*
*Disconfirming evidence is required for every CONFIRMED classification (§9 Rule 3).*
