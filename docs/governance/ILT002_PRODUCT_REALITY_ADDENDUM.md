# ILT002_PRODUCT_REALITY_ADDENDUM

**Document ID:** ILT002_PRODUCT_REALITY_ADDENDUM
**Type:** Campaign Addendum — Evidence Collection Extension
**Status:** ADMITTED
**Admission date:** 2026-06-04
**Author:** Governance Manager
**Addendum to:** ILT002_EXECUTION_GUIDE.md, ILT002_CASE1_PREPARATION_PACKAGE.md
**Baseline:** HEAD ceb2dc9

**Purpose:** Capture product truth during ILT-002 by recording every
moment where an inventor requires capabilities not currently available.
Use that evidence — not architectural preference — to determine the
next activation priority after the campaign concludes.

**This document does not replace, modify, or supersede any admitted
ILT-002 artifact. It extends evidence collection only.**

---

## SECTION A — DEFERRED VISION OBSERVATION LOG

### A.1 What to Record

During every ILT-002 session, the reviewer must watch for moments
where the inventor's journey is interrupted, blocked, slowed, or
diverted by a capability the platform does not currently provide.

These moments are the most valuable evidence the campaign produces.
They reveal what the platform must become — not through architectural
reasoning, but through inventor behavior.

**Record every observation where the inventor:**
- Asks a question the platform cannot answer
- Needs information the platform cannot provide
- Reaches a point where the next step requires external capability
- Expresses frustration, confusion, or a dead end
- Makes a decision without sufficient platform support
- Names something they need that the platform does not have

### A.2 Deferred Vision Observation Record (one per observation)
### A.3 When to Record

Record whenever the reviewer observes:

**Explicit triggers (inventor names the need):**
- "I need to know what component to use" → Component Selection / ODS-001
- "I don't know how to test this" → Validation Requirements
- "I need to come back after I research" → Multi-session Persistence
- "I need an expert for this" → External Expertise Routing
- "How would this be manufactured?" → Manufacturing Path
- "What material would work here?" → Material Selection / ODS-001

**Implicit triggers (reviewer infers the need):**
- Inventor gives vague answer where a specific component name
  would have enabled REASONED classification
- Inventor acknowledges an assumption cannot be validated without
  equipment or expertise not mentioned
- Inventor's response quality drops at a point where domain
  knowledge would have enabled specificity

**Do not record:**
- Ordinary gaps in mechanism understanding (the platform's normal work)
- Platform behavior the execution guide already addresses

---

## SECTION B — DEFERRED VISION DEMAND SCORING

### B.1 Purpose

At campaign end, Section A observations are scored to produce
an evidence-based ranking of deferred vision items.

### B.2 Scoring Dimensions

**D1 — Frequency across inventors (max 5 points)**
**D2 — Frequency across sessions (max 5 points)**
**D3 — Worst observed severity (max 5 points)**
Rationale for worst-case: A capability that blocked any real
inventor even once is a genuine platform gap. This signal must
not be diluted by averaging. The multi-dimensional scoring model
(D1, D2, D4, D5 and the threshold of 8) already prevents a
single BLOCKED observation from driving activation independently.

**D4 — Explicit inventor request (max 3 points)**
**D5 — Reappearance after workaround (max 2 points)**
Maximum total score: 20 points

### B.3 Scoring Table
### B.4 Scoring Integrity Rules

Rule S-1: Each observation maps to at most one primary item. No double-counting.
Rule S-2: Score each dimension from raw observation log independently.
          Do not adjust based on architectural preference.
Rule S-3: Ties broken by D3 first, then D4. If still tied: TIED.
Rule S-4: Zero observations = zero score, regardless of architectural importance.

---

## SECTION C — POST-CAMPAIGN ACTIVATION FRAMEWORK

### C.1 The Question to Ask

Do not ask: "What should we build next?"
Ask: "What capability was most strongly demanded by real inventor behavior?"

### C.2 Activation Decision Procedure

Step 1 — Complete Section B.3 scoring table (all sessions complete first).
Step 2 — Rank items by total score in descending order.
Step 3 — Apply activation threshold:
          Qualifies if: total score ≥ 8 AND at least one observation recorded.
Step 4 — Review top candidate against existing governance foundations.
          Per archaeology review: most deferred items exist as governance
          placeholders from PROJECT_STATE_FREEZE_v1.2. Check before
          treating activation as new architecture.
Step 5 — Owner decision. Ranked list is input, not decision.

### C.3 Activation Candidate Reference

| Activation Candidate | Governance Status | Code Foundation |
|---------------------|------------------|-----------------|
| ODS-001 | Deferred post-MVP (explicit) | assembler sections B+C deferred |
| Validation Requirements | SPV §1 journey item | No implementation |
| Manufacturing Path | assembler DEFERRED | Structural placeholder |
| Material Selection | ODS-001 dependent | assembler DEFERRED |
| Component Selection | ODS-001 dependent | assembler DEFERRED |
| External Expertise Routing | EGA surfaces need, no routing | None |
| Multi-session Persistence | Deferred post-MVP (explicit) | Supabase schema exists |
| Resource Identification | Not in governance | None |
| Regulatory Pathway | Not in governance | None |

### C.4 Evidence Sufficiency Threshold

High-confidence evidence-driven activation requires:
- Observations from at least 2 distinct inventors
- Observations from at least 3 distinct sessions
- At least one BLOCKED or SIGNIFICANT severity observation

Provisional evidence (1 inventor, 2+ sessions, no BLOCKED):
- Requires explicit owner acknowledgment that evidence is limited.

### C.5 If No Item Reaches Threshold

This is itself a product truth finding.

It means ILT-002 inventors completed the journey without strong
demand for any currently-deferred capability. The correct response:

1. Confirm the finding explicitly.
2. Do not activate any deferred vision item based on this campaign.
3. Run additional sessions with different archetypes before activating.

Do not interpret low scores as evidence that deferred items are
unimportant. It means they were not strongly demanded in this
campaign with this participant profile.

---

## SECTION D — OBSERVATION LOG SUMMARY (complete after campaign)
---

## APPENDIX — REVIEWER QUICK REFERENCE

**The single diagnostic question:**
"Is the inventor being limited by their own reasoning capability,
or by the platform's missing capability?"

If reasoning limitation → platform's normal work, do not record.
If platform limitation → record a DVO observation.

**Severity guide:**
- BLOCKED: Inventor cannot answer the current question without
  this capability. Gap cannot close.
- SIGNIFICANT: Inventor gives ASSERTED where platform capability
  would have enabled REASONED.
- MODERATE: Long detour but self-resolved.
- MINOR: Gap noticed but does not affect the session.

---

*Product truth comes from inventor behavior, not from architecture.*
*Record what inventors demand. Let evidence determine what to build.*
