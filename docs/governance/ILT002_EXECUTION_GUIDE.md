# ILT002_EXECUTION_GUIDE

**Document ID:** ILT002_EXECUTION_GUIDE
**Type:** Operational Execution Guide
**Status:** READY FOR USE
**Date:** 2026-06-04
**Author:** Governance Manager
**Governing documents:**
  - ILT-002_VALIDATION_CAMPAIGN_PLAN.md
  - ILT-002A_OBSERVER_BIAS_REVIEW.md
**Baseline:** HEAD 88f2a8a (Stage 3 reachability confirmed)

---

## HOW TO USE THIS GUIDE

Read this guide completely before beginning any session.
Do not start recording until Section 1 preparation is complete.
Do not annotate until Section 2 anchors are internalized.
Do not classify until all sessions are complete.
Every box must be checked or explicitly noted as N/A with a reason.

---

## SECTION 1 — CAMPAIGN PREPARATION

### 1.1 Required artifacts

- [ ] ILT-002_VALIDATION_CAMPAIGN_PLAN.md
- [ ] ILT-002A_OBSERVER_BIAS_REVIEW.md
- [ ] This guide
- [ ] STAGE3_QUESTION_SET.md (Parts 1-3 only)
- [ ] SR-001_INVENTOR_OUTCOME_MEASUREMENT.md (dimensions list)

### 1.2 Baseline reference

Repository baseline: HEAD 88f2a8a
Stage 3 is reachable: confirmed by TC-REACH-001/002/003
If any engine change is made before Session 1, stop. New baseline required.

### 1.3 Evidence collection template (per iteration)
### 1.4 Session sign-off

After each session:
- [ ] All iteration records complete
- [ ] Emergence timing table updated
- [ ] Session-level observations recorded
- [ ] Reviewer sign-off: "Session N complete. Date: ___"

---

## SECTION 2 — BEHAVIORAL ANCHORS

### 2.1 Self-Correction

REQUIRES BOTH:
1. Revision marker phrase present ("actually," "I was wrong," "let me correct,"
   "I realize now," "that's not right," "more accurately," "I should clarify")
2. New statement logically contradicts or substantially narrows a prior statement

POSITIVE: Prior: "works in any environment" → Current: "actually, fails in
high-humidity because capacitive measurement is affected by condensation"
NEGATIVE: Adding new information without contradicting prior = ELABORATION
AMBIGUOUS: "I suppose it would be more accurate to say..." without clear
prior contradiction = ELABORATION (conservative default)
RULE: No revision marker + no contradiction = ELABORATION, not self-correction.

### 2.2 Ownership Growth

REQUIRES: Inventor names a specific limitation, assumption, or expertise gap
that (a) is mechanism-specific — not generic — and (b) was not named before.
Apply specificity test (Section 5) first. If generic: NOT ownership growth.

POSITIVE: "My mechanism assumes fixed RPM baseline — I hadn't accounted for
variable-speed motors requiring recalibration at every operating point"
NEGATIVE: "There will be challenges with implementation" = NOT ownership growth

### 2.3 Unknown Awareness (AI-E3)

REQUIRES: Explicit newness marker introduced by inventor, not prompted by question.
Tier 1: "I hadn't thought of," "I didn't realize," "this makes me realize"
Tier 2: "I realize now," "I wasn't aware," "I overlooked"
Prompt contamination check: Did the question mention the concept? If YES = PROMPTED RECOGNITION, not AI-E3.

### 2.4 Transfer of Reasoning (M-3, within-idea)

REQUIRES: Inventor applies rea
### 1.4 Session sign-off

After each session:
- [ ] All iteration records complete
- [ ] Emergence timing table updated
- [ ] Session-level observations recorded
- [ ] Reviewer sign-off: "Session N complete. Date: ___"

---

## SECTION 2 — BEHAVIORAL ANCHORS

### 2.1 Self-Correction

REQUIRES BOTH:
1. Revision marker phrase present ("actually," "I was wrong," "let me correct,"
   "I realize now," "that's not right," "more accurately," "I should clarify")
2. New statement logically contradicts or substantially narrows a prior statement

POSITIVE: Prior: "works in any environment" → Current: "actually, fails in
high-humidity because capacitive measurement is affected by condensation"
NEGATIVE: Adding new information without contradicting prior = ELABORATION
AMBIGUOUS: "I suppose it would be more accurate to say..." without clear
prior contradiction = ELABORATION (conservative default)
RULE: No revision marker + no contradiction = ELABORATION, not self-correction.

### 2.2 Ownership Growth

REQUIRES: Inventor names a specific limitation, assumption, or expertise gap
that (a) is mechanism-specific — not generic — and (b) was not named before.
Apply specificity test (Section 5) first. If generic: NOT ownership growth.

POSITIVE: "My mechanism assumes fixed RPM baseline — I hadn't accounted for
variable-speed motors requiring recalibration at every operating point"
NEGATIVE: "There will be challenges with implementation" = NOT ownership growth

### 2.3 Unknown Awareness (AI-E3)

REQUIRES: Explicit newness marker introduced by inventor, not prompted by question.
Tier 1: "I hadn't thought of," "I didn't realize," "this makes me realize"
Tier 2: "I realize now," "I wasn't aware," "I overlooked"
Prompt contamination check: Did the question mention the concept? If YES = PROMPTED RECOGNITION, not AI-E3.

### 2.4 Transfer of Reasoning (M-3, within-idea)

REQUIRES: Inventor applies reasoning from one gap type to another without
the second question requiring it. Must be an explicit or inferable cross-gap reference.
Generic "like I said before" without identifying prior gap = does NOT qualify.

### 2.5 Inventor Independence (M-4)

REQUIRES: Inventor names a specific gap type or evidence item from
STAGE3_QUESTION_SET.md not yet asked, using mechanism-specific language,
appearing mid-session or late-session (not first response).
Generic "I'm sure you'll ask about my assumptions" = NOT M-4.

### 2.6 S-6 Cross-Idea Transfer

REQUIRES ALL THREE:
1. Earlier emergence in Idea B vs Idea A (quantified by iteration number)
2. Idea B-specific content (passes specificity test)
3. Not explained by: domain familiarity difference, warmup effect,
   verbatim reuse of Idea A phrases, or protocol learning

---

## SECTION 3 — REVISION MARKER PROTOCOL

Genuine correction = Tier 1/2 marker + logical contradiction of prior claim.
Tier 1 (strong): "actually," "I was wrong," "let me correct," "I realize now"
Tier 2 (acceptable): "more accurately," "I should clarify," "I misstated"
Tier 3 (borderline): "I suppose," "come to think of it" — require clear Condition 2.
What does NOT count: adding information, changing emphasis, question-prompted acknowledgment.

Recording format:
S-6 confirmed when: Idea B first appearance < Idea A first appearance
for at least 2 of 3 behaviors (assumption, boundary, expertise gap)
AND Idea B content is specific AND no false positive condition applies.

---

## SECTION 5 — SPECIFICITY TEST

Question: Could this exact statement be made by any inventor working on
any device in this domain without knowing anything about this specific invention?

YES = GENERIC. Not evidence of development.
NO = MECHANISM-SPECIFIC. May qualify.

GENERIC: "I need to consider the power requirements."
SPECIFIC: "The LM393 comparator I'm using has 1.3us propagation delay,
which at motor speeds above 3000 RPM makes the fault window narrower
than the fault duration — I may miss events."

---

## SECTION 6 — NEWNESS MARKER PROTOCOL

Tier 1: "I hadn't thought of," "I didn't realize," "this makes me realize,"
        "I just noticed," "I didn't recognize this as"
Tier 2: "I realize now," "I wasn't aware," "I overlooked"
Tier 3: "I suppose," "I guess" — require strong newness content.
Prompt contamination check: Did question mention/imply this concept? If YES = NOT AI-E3.

---

## SECTION 7 — EVIDENCE CAPTURE FORMS

### FORM A (Idea A — Early Stage)
### FORM T (Transfer Challenge)
---

## SECTION 8 — FINAL CLASSIFICATION PROCEDURE

Step 1 — Compile signal counts (S-1 through S-6 per archetype).
Step 2 — Minimum threshold check:
  S-1 + S-2 + any one of S-3/S-4/S-5 confirmed in >= 2 of 3 archetypes?
  NO → IDEA DEVELOPMENT PLATFORM
  YES → Step 3
Step 3 — S-6 check:
  S-6 confirmed → INVENTOR DEVELOPMENT PLATFORM
  S-6 contested → HYBRID SYSTEM (note)
  S-6 absent → HYBRID SYSTEM
Step 4 — F-3 check:
  F-3 confirmed in any archetype → exclude that archetype, recalculate Step 2.
Step 5 — Write final verdict with qualification statement from
  ILT002_MEASUREMENT_SCOPE_REVIEW Section 5.3.

---

## SECTION 9 — REVIEWER DISCIPLINE RULES

Rule 1: Record full response before writing any annotation.
Rule 2: Look up anchor definition before classifying — no intuition.
Rule 3: For every positive signal, explicitly record disconfirming evidence.
Rule 4: Do not revise past records based on later observations.
        Factual corrections only — must be initialed and dated.
Rule 5: Lock Idea A timing table before Idea B begins. Cannot be modified after.
Rule 6: Contested signals do not count for or against. Record both sides.
Rule 7: Platform identity does not affect verdict.
        Hybrid System or Idea Development Platform is a valid finding,
        not a campaign failure.

---

## APPENDIX — APPROVED PARTICIPANT RESPONSES

"What is the platform measuring?"
→ "The platform asks questions to help you think through your idea.
   We're studying how people develop their thinking about inventions."

"Am I doing well?"
→ "There are no right or wrong answers. We want your genuine thoughts."

"What does the platform think of my idea?"
→ "The platform doesn't evaluate whether ideas are good or bad."

"Why these particular questions?"
→ "The questions follow a structure designed to help inventors think
   through different aspects of their ideas. That's all we can say."

---

*Apply the anchors mechanically.*
*Record what you observe, not what you hope to observe.*
*The platform's identity is determined by evidence, not aspiration.*
