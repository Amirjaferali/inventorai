# Truth Classification Framework
## InventorAI Project Standard
**Version:** 1.0
**Created:** 2026-05-25
**Status:** ACTIVE
**Authority:** Below GOVERNANCE_MODEL.md, above session notes

---

## Purpose

Every finding, claim, or observation made during development, diagnosis,
or review must be classified before being acted upon.

This framework prevents:
- Analysis being treated as fact
- Assumptions being written into fixtures
- Inferences becoming architectural decisions
- Undocumented behavior being assumed stable

---

## The Five Classifications

---

### CLASS 1 — DOCUMENTATION TRUTH

**Definition:**
Explicitly stated in a repository governance or specification document.
The claim can be quoted verbatim from the file.

**Required fields:**
- classification: DOCUMENTATION TRUTH
- source_file: exact filename
- exact_quote: verbatim text from file
- location: section or line reference if available

**Invalid use:**
- Paraphrasing a document and presenting it as a quote
- Inferring intent from document structure
- Combining two document statements into one claim

---

### CLASS 2 — CODE TRUTH

**Definition:**
Directly observable in source code by reading the file.
The behavior can be traced to specific lines without execution.

**Required fields:**
- classification: CODE TRUTH
- source_file: exact file path
- line_range: line numbers
- exact_code: verbatim code excerpt

**Invalid use:**
- Describing what code intends to do
- Inferring behavior from variable names
- Claiming code does X without showing the lines

---

### CLASS 3 — TEST EVIDENCE

**Definition:**
Proven by actual execution: benchmark runs, replay results,
validation logs, or terminal output captured during a session.

**Required fields:**
- classification: TEST EVIDENCE
- source_file: result file or terminal session reference
- observed_value: exact output
- timestamp: when the evidence was captured (if available)

**Invalid use:**
- Inferring future benchmark behavior from past results
- Assuming a passing test proves absence of all bugs
- Using a skipped test result as evidence of engine behavior

---

### CLASS 4 — ANALYSIS

**Definition:**
Any interpretation, hypothesis, concern, recommendation, inference,
or opinion that is not directly sourced from CLASS 1, 2, or 3.

**Required fields:**
- classification: ANALYSIS
- basis: which CLASS 1/2/3 findings this analysis derives from
- confidence: LOW / MEDIUM / HIGH
- statement: the interpretation or recommendation

**Invalid use:**
- Presenting an ANALYSIS as a CODE TRUTH
- Acting on ANALYSIS without human approval
- Writing fixture expected values based on ANALYSIS alone

---

### CLASS 5 — DECISION RECORD

**Definition:**
An explicit project-owner decision that remains authoritative
until superseded by a newer decision record.

A DECISION RECORD is not an analysis, not a code observation,
and not a documentation quote. It is a binding choice made by
the project owner that governs future actions.

**Required fields:**
- classification: DECISION RECORD
- decision_id: unique identifier (DR-XXX)
- decision_owner: who made the decision
- decision_date: date of decision
- decision_statement: exact statement of the decision
- basis: CLASS 1/2/3/4 findings that informed the decision
- supersedes: prior decision_id if this replaces one (optional)
- status: ACTIVE / SUPERSEDED

**Invalid use:**
- Claude generating a DECISION RECORD unilaterally
- Treating an ANALYSIS as a DECISION RECORD
- Backdating a decision to avoid review

---

## Mixing Rules — PROHIBITED

| Prohibited action                             | Why                          |
|-----------------------------------------------|------------------------------|
| Quoting a document then adding interpretation | Mixes CLASS 1 + CLASS 4      |
| Reading code then inferring intent            | Mixes CLASS 2 + CLASS 4      |
| Using past benchmark to predict future pass   | Mixes CLASS 3 + CLASS 4      |
| Writing expected values from ANALYSIS         | Creates self-validating tests |
| Presenting ANALYSIS without labeling          | Obscures decision basis       |

---

## Application to Fixture Design

Before any fixture expected values are written, each field must trace
to a classification:

| Fixture field              | Required classification                       |
|----------------------------|-----------------------------------------------|
| sig                        | CLASS 2 — runner code showing how sig is read |
| expected.scores[x].passed  | CLASS 2 — scoring.py criterion function       |
| expected.weighted_score    | CLASS 2 — score_case() formula                |
| expected.overall           | CLASS 2 — overall = all(scores[n]["passed"])  |
| input.raw_text structure   | CLASS 2 — c1_schema required fields           |
| testcase.exp_gaps          | CLASS 2 — c3_missing_info(out, tc)            |
| testcase.exp_sig           | CLASS 2 — c7_restraint exp_sig check          |

If any field cannot be traced to CLASS 1 or CLASS 2, it must be
labeled CLASS 4 — ANALYSIS and must not be written into a fixture
until approved by the project owner.

---

## Application to Diagnosis

When diagnosing a bug or skip:

    Step 1: State what the evidence shows      (CLASS 3)
    Step 2: Show the code that handles it      (CLASS 2)
    Step 3: Check if documented behavior       (CLASS 1)
             matches
    Step 4: Only then form a hypothesis        (CLASS 4)
    Step 5: Label the hypothesis explicitly    as ANALYSIS
    Step 6: Do not act on ANALYSIS without     approval

---

## Known Findings

### F-001
    classification: CODE TRUTH
    source_file:    engine/scoring.py
    line_range:     L33
    exact_code:     if tc["id"] == "TC-18" and conf == "HIGH":
                        iss.append("OVERCONFIDENT_ON_EMPTY_INPUT")
    note:           Hardcoded fixture ID in scorer. Not documented
                    as intentional in any governance document.

### F-002
    classification: TEST EVIDENCE
    source_file:    tests/replay/replay_report_v1.json
    observed_value: skipped: 3, skip_reason: "no_raw_text"
                    TC-09, TC-10, TC-17 all show:
                    trace.error_category = "TimeoutError"
                    trace.error = true
                    input.raw_text = null
    timestamp:      2026-05-23 (K-R1 diagnosis)

### F-003
    classification: DOCUMENTATION TRUTH
    source_file:    GOVERNANCE_MODEL.md
    exact_quote:    "VIOLATION-01: Semantic authority not in
                    fixtures — PENDING DESIGN DECISION"
    location:       ## VIOLATIONS

### F-004
    classification: CODE TRUTH
    source_file:    scripts/run_replay_benchmark.py
    line_range:     L72
    exact_code:     Does NOT compare: failure_type,
                    weighted_score, overall.
    note:           Runner compares sig only. weighted_score
                    and overall excluded from pass/fail.

### F-005
    classification: DOCUMENTATION TRUTH
    source_file:    VALIDATION_LOG.md
    exact_quote:    "engine/progression_loop.py assigns
                    quality=ASSERTED to ANY non-empty text.
                    Minimum viable answer threshold does
                    not exist."
    location:       ## Root Cause Identified
    note:           Phase E finding. Fix status unknown.

### F-006
    classification: ANALYSIS
    basis:          F-004 (CODE TRUTH — runner excludes
                    weighted_score from comparison)
    confidence:     HIGH
    statement:      Fixture expected.weighted_score values
                    are not verified by the runner. Writing
                    incorrect values would not cause failure
                    but would create misleading documentation.

### F-007
    classification: TEST EVIDENCE
    source_file:    terminal session 2026-05-25
    observed_value: No file named TRUTH_CLASSIFICATION_FRAMEWORK.md
                    found anywhere in repository or filesystem.
                    git log, git grep, find all returned empty.
    timestamp:      2026-05-25

---

## Active Decision Records

### DR-001
    classification:      DECISION RECORD
    decision_id:         DR-001
    decision_owner:      project owner
    decision_date:       2026-05-23
    decision_statement:  TC-09, TC-10, and TC-17 shall remain
                         unchanged as historical timeout fixtures.
                         They must not be edited, deleted, or
                         overwritten. Preserved for traceability.
    basis:               F-002 (TEST EVIDENCE)
    supersedes:          none
    status:              ACTIVE

### DR-002
    classification:      DECISION RECORD
    decision_id:         DR-002
    decision_owner:      project owner
    decision_date:       2026-05-23
    decision_statement:  Option C (re-record original fixtures)
                         is permanently closed. Source files
                         results_20260519_124751.json and
                         results_20260520_074904.json do not
                         exist. No re-record of TC-09/10/17
                         is possible.
    basis:               TEST EVIDENCE — os.path.exists()=False,
                         FileNotFoundError confirmed 2026-05-23
    supersedes:          none
    status:              ACTIVE

### DR-003
    classification:      DECISION RECORD
    decision_id:         DR-003
    decision_owner:      project owner
    decision_date:       2026-05-23
    decision_statement:  MVP Scope Freeze remains active.
                         No expansion permitted until conditions
                         in MVP_SCOPE_FREEZE.md REVISION PROTOCOL
                         are fully met.
    basis:               DOCUMENTATION TRUTH — MVP_SCOPE_FREEZE.md
                         "Status: ACTIVE FREEZE"
    supersedes:          none
    status:              ACTIVE

### DR-004
    classification:      DECISION RECORD
    decision_id:         DR-004
    decision_owner:      project owner
    decision_date:       2026-05-23
    decision_statement:  TC-23, TC-24, TC-25 shall be created as
                         independent diagnostic coverage additions.
                         Not replacements for TC-09/10/17. Must be
                         designed from scorer source code only.
                         Expected values written before execution,
                         never derived from actual output.
    basis:               DR-001, F-006, CODE TRUTH scoring.py
    supersedes:          none
    status:              ACTIVE

### DR-005
    classification:      DECISION RECORD
    decision_id:         DR-005
    decision_owner:      project owner
    decision_date:       2026-05-25
    decision_statement:  This framework is an active project
                         standard. All future findings, fixture
                         proposals, and diagnostic reports must
                         classify every claim using CLASS 1-5
                         before it can be acted upon. Historical
                         findings created before 2026-05-25
                         (adoption date) are exempt unless
                         reopened for review. Unclassified claims
                         must not be used as basis for code or
                         fixture changes.
    basis:               DOCUMENTATION TRUTH — CLAUDE.md
                         "Document Authority Order"
    supersedes:          none
    status:              ACTIVE

---

## Authority Order

    1. MVP_SCOPE_FREEZE.md                  (hard constraint)
    2. GOVERNANCE_MODEL.md                  (authority hierarchy)
    3. CLAUDE.md                            (engineering rules)
    4. TRUTH_CLASSIFICATION_FRAMEWORK.md   (classification standard)
       — CLASS 5 DECISION RECORDs within this document
    5. DECISION_PROGRESSION_MODEL.md       (proposal only)

---

Document owner: architecture + project owner
Review required before: any fixture creation, any scoring change
Violations: presenting findings without classification label
