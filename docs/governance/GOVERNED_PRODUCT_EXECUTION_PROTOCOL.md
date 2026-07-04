 # GOVERNED_PRODUCT_EXECUTION_PROTOCOL.md

**Status:** PROPOSED — requires explicit owner authorization before commit
**Scope:** Execution-efficiency triage layer only
**Does NOT supersede:** Any active anchor, scope freeze, blocked state, or existing governance document
**Authoritative repository:** Amirjaferali/inventorai
**Authoritative branch at proposal time:** feature/atomic-json-session-persistence @ 16d62f1e461dbd2a780c82e3b0654d068c31d30c

---

## Table of Contents

* [A. Purpose](#a-purpose)
* [B. Non-Negotiable Preserved Constraints](#b-non-negotiable-preserved-constraints)
* [C. Governance Observation Classification](#c-governance-observation-classification)
* [D. Execution Efficiency Rules](#d-execution-efficiency-rules)
* [E. Required Output Format](#e-required-output-format)
* [F. Escalation Protocol](#f-escalation-protocol)
* [G. Precedence Order](#g-precedence-order)
* [H. Protocol Validity and Limits](#h-protocol-validity-and-limits)

---

## A. Purpose

This protocol controls how governance findings during product execution are triaged. It does not weaken anchors, does not authorize persistence recovery, does not authorize main synchronization, does not authorize scope expansion, and does not supersede the active roadmap or any existing governance document.

**Primary goal:** Move the project from repeated closure cycles toward visible inventor-facing product value without sacrificing repository truth, governance integrity, or owner authorization discipline.

**Definition — Inventor-Facing Value:**

A shipped, reachable, and testable behavior that an inventor can personally experience. This means one or more of:

* A rendered interface element visible in a browser without special tooling;
* A changed workflow state resulting from a real user action;
* A corrected or improved decision output;
* A documented explanation of a result that the inventor can read and act on.

Governance documents, test files, internal refactoring, roadmap updates, and documentation corrections alone do **not** constitute inventor-facing value. They may accompany authorized work but cannot be the sole justification for an execution step.

---

## B. Non-Negotiable Preserved Constraints

The following constraints are permanently protected. **No section of this protocol may override, weaken, reinterpret, or work around them.** If any tension arises between this protocol and these constraints, the constraint wins unconditionally and execution stops until the owner resolves the conflict.

| Constraint | Current Status |
| --- | --- |
| Repository evidence overrides narrative — always | ACTIVE |
| No domain expansion beyond committed scope | ACTIVE |
| No Stage 4-7 | ACTIVE |
| No maturity or scoring expansion | ACTIVE |
| No professional workspace | ACTIVE |
| No persistence restart, recovery, or reconciliation | PAUSED — no authority granted |
| No main synchronization | UNAUTHORIZED — requires separate authorization |
| No new generated truth | ACTIVE |
| No bypassing active named anchors | ACTIVE |
| No owner-authorization boundary crossed without explicit approval | ACTIVE |

**Persistence note:** The paused persistence artifact must not be assumed recoverable. Any future persistence work requires separate owner-authorized assessment. Clean reimplementation from the current authoritative tip is the safer planning assumption unless recovery evidence is produced.

---

## C. Governance Observation Classification

Every governance finding during an authorized execution task must be classified as **exactly one** of the following four types before any action is taken. Classification must be explicit, cited, and one-sentence per finding.

---

### C.1 — BLOCKING GOVERNANCE ISSUE

**Effect:** Stops the current authorized execution immediately.
**Resumption:** Only after owner resolves the finding in writing.

A finding is **BLOCKING only if** it directly and specifically affects one or more of the following named criteria. Claude Code must cite the exact criterion violated — not a general concern.

**Blocking criteria:**

1. **Active named anchor:** A committed anchor document is contradicted or bypassed. Must cite anchor name and exact document path.
2. **Scope freeze:** An action would expand domain, stage, maturity, scoring, or workspace beyond what MVP_SCOPE_FREEZE.md permits. Must cite the exact section of MVP_SCOPE_FREEZE.md.
3. **Product identity:** An action contradicts the committed product definition. Must cite STRATEGIC_PRODUCT_VISION.md section.
4. **Persistence status:** Any mutation of the paused persistence artifact, or any action that assumes persistence is active or recoverable. Currently PAUSED — any touch is BLOCKING.
5. **Main synchronization:** Any push, merge, or rebase that would alter the main branch without explicit owner authorization.
6. **Domain, stage, scoring, or maturity logic:** Any change to the rules governing how the engine determines progression, gap status, or maturity transitions. Must cite the exact function and file.
7. **Provenance integrity — specifically:** A committed hash, authorship record, or evidence chain is broken, falsified, or irrecoverably ambiguous. This does **not** include: imprecise comments, incomplete docstrings, naming inconsistencies, or documentation gaps.
8. **Build or test suite integrity:** Existing passing tests would break, or existing committed behavior would regress. Must cite the exact test name and file.
9. **Owner authorization boundary:** An action requires authorization that has not been granted in the current session or in a committed governance document. Must cite the exact missing authorization.

**A finding is NOT BLOCKING merely because it involves:**

* Documentation style, wording, or formatting;
* Test naming, organization, or grouping;
* Code comments or docstrings;
* Roadmap phrasing that is imprecise but not materially misleading;
* An observation that matches actual design intent;
* A concern about future risk that is not currently active.

**Required citation format for every BLOCKING finding:**

```
BLOCKING: [one-sentence description]
Criterion violated: [exact criterion from C.1 list above]
File and line: [exact reference]
Why no narrower interpretation is possible: [one sentence]
```

---

### C.2 — NON-BLOCKING OBSERVATION

**Effect:** Recorded. Must not stop an otherwise authorized implementation.

**Batching rule:** Non-blocking observations are surfaced to the owner at the **end of each PR or Increment**, not inline during execution.

**Maximum accumulation:** If 10 or more non-blocking observations accumulate before a PR is closed, Claude Code must surface them to the owner before continuing — regardless of Increment boundary.

**Required format for each observation:**

```
OBSERVATION: [one-sentence description]
File: [path]
Suggested handling: [batch / next PR / document reconciliation]
```

---

### C.3 — DOCUMENTATION DEBT

**Effect:** Recorded for a dedicated documentation reconciliation task. Must **not** trigger a new governance document during active execution. Must **not** block a PR merge unless the gap creates an immediate logical contradiction in the codebase, not merely in documentation.

**What qualifies:**

* Missing or outdated docstrings;
* Roadmap phrasing that lags behind committed state;
* Governance document references that are correct in intent but imprecise in wording.

**What does not qualify:**

* A contradiction between a committed governance ruling and committed code behavior — that is C.1.8 build integrity or C.1.7 provenance, not documentation debt.

---

### C.4 — NOISE / OVER-INTERPRETATION

**Effect:** Identified, named, and discarded. Must not create new work.

**What qualifies:**

* A finding that does not meet the threshold for C.1, C.2, or C.3 under any reasonable interpretation;
* A finding that restates a known and accepted design trade-off;
* A finding that was already addressed in a prior committed governance document.

**Self-classification prohibition:** Claude Code must **not** self-classify a finding as NOISE if there is genuine uncertainty about whether it meets C.1 criteria. Uncertain findings must follow the Escalation Protocol in Section F. Classifying uncertain findings as NOISE to avoid stopping execution is a governance violation.

---

## D. Execution Efficiency Rules

1. **One PR per inventor-facing product outcome.** An outcome means a behavior the inventor can personally experience as defined in Section A. An outcome is not: a governance document, a test file alone, a refactoring, or a documentation correction.
2. **Do not create new governance documents** unless a C.1 BLOCKING finding explicitly requires one. If uncertain whether a document is required, ask the owner before creating it.
3. **Do not perform roadmap synchronization after every step.** Synchronize only when the roadmap would become materially misleading to a reader who relies on it for next-action decisions.
4. **Do not reopen closed Increments** without direct owner authorization naming the specific Increment.
5. **Do not convert no downstream authority into permanent paralysis.** Instead: identify the exact next bounded action in one sentence, state the exact authorization text needed, and wait for the owner response. Do not create governance documents describing the paralysis.
6. **Prefer evidence over narrative.** Tests, changed-path evidence, and working product verification are preferred over repeated narrative review cycles.
7. **Batch minor documentation cleanup** into dedicated tasks that are separate from product execution PRs.
8. **Every execution step must name its inventor-facing value** using the definition in Section A before work begins. If no inventor-facing value can be named, the step requires owner authorization before proceeding.

---

## E. Required Output Format

Every Claude Code review response during an authorized execution task must use this exact structure. Sections may not be omitted or merged.

```
## BLOCKING FINDINGS
<!-- List each with required citation format from C.1, or: NONE -->

## NON-BLOCKING OBSERVATIONS
<!-- List each with format from C.2, or: NONE -->

## DOCUMENTATION DEBT
<!-- List each with format from C.3, or: NONE -->

## NOISE / OVER-INTERPRETATION IDENTIFIED
<!-- List each with one-sentence justification, or: NONE -->

## ESCALATION REQUIRED — CLASSIFICATION UNCERTAIN
<!-- List any finding that cannot be classified, or: NONE -->

## INVENTOR-FACING VALUE OF THIS STEP
<!-- One sentence naming the value per Section A definition -->

## RECOMMENDED NEXT ACTION
<!-- One specific action -->

## EXACT AUTHORIZATION REQUIRED FROM OWNER
<!-- Specific text owner must approve, or: NONE REQUIRED -->
```

If the BLOCKING FINDINGS section is not NONE, execution stops immediately after the response. No further work may proceed until the owner provides written resolution.

---

## F. Escalation Protocol

When Claude Code cannot determine whether a finding is BLOCKING, it must follow this exact sequence:

1. Stop the current execution step immediately.
2. State the finding in one sentence.
3. State which C.1 criterion it might violate.
4. State in one sentence why the classification is uncertain.
5. Request owner classification before continuing any work.

**Claude Code must never:**

* Proceed past an uncertain BLOCKING candidate by resolving the uncertainty in its own favor;
* Classify an uncertain finding as NOISE to avoid stopping;
* Create a governance document about the uncertainty instead of asking the owner directly.

---

## G. Precedence Order

When this protocol conflicts with any other governance document or instruction, the following order applies unconditionally:

```
1. Active named anchors
2. MVP_SCOPE_FREEZE.md
3. GOVERNANCE_MODEL.md
4. CLAUDE.md
5. This protocol
6. Individual PR descriptions or session decisions
```

This protocol does not grant itself authority over items 1-4 above. Any apparent conflict between this protocol and items 1-4 must be treated as a C.1 BLOCKING finding and escalated to the owner.

---

## H. Protocol Validity and Limits

**This protocol is valid only when all of the following are true:**

* It has been committed to the repository at an authorized commit on the authoritative branch.
* The owner has explicitly approved the commit in writing.
* No active anchor contradicts its application to the current task.
* The current authoritative tip has been verified against the preserved state in Section B.

**This protocol explicitly does not:**

* Weaken any anchor.
* Authorize persistence restart, recovery, or reconciliation.
* Authorize main synchronization.
* Authorize scope expansion of any kind.
* Supersede the active roadmap.
* Grant any implementation authority not separately and explicitly granted by the owner.
* Permit Claude Code to infer owner approval from protocol compliance.

**Until committed and approved, this document is PROPOSED only and carries no execution authority.**

---

*Proposed — not yet committed.*
*Requires owner authorization before any repository action.*
*Authoritative branch: feature/atomic-json-session-persistence*
*Proposed at tip: 16d62f1e461dbd2a780c82e3b0654d068c31d30c*