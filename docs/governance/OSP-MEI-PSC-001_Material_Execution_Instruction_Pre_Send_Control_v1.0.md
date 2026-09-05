# OWNER STANDING PROCESS CONTROL

## OSP-MEI-PSC-001 — Material Execution-Instruction Pre-Send Control

**Version:** 1.0  
**Effective date:** 2026-09-04  
**Status:** ACTIVE  
**Authority:** OWNER STANDING PROCESS AUTHORITY  
**Successor propagation:** REQUIRED  
**Universal agent applicability:** ACTIVE  
**Function-triggered:** YES  
**Material-instruction only:** YES  
**Repository status:** NOT YET DURABLY INTEGRATED — repository mutation remains separately governed  
**Handover-only authority:** NO  

---

## 1. Purpose

This control exists to prevent defects in a material execution instruction **before** that instruction reaches the execution agent.

It addresses recurring risks including:

- instruction lifecycle contradictions;
- exact-send provenance ambiguity;
- wrong or ambiguous input/output artifacts;
- unverified filesystem/hash/path claims;
- silent delegation of load-bearing statistical, architectural, governance, product-policy, lifecycle, persisted-state, or ownership choices;
- missing STOP conditions;
- incomplete evidence-return requirements;
- scope expansion;
- duplicate execution or unnecessary re-runs;
- authority/provenance drift;
- foreseeable post-send and post-freeze repair loops caused by instruction defects.

The process must reduce review loops, not create reviewer recursion.

---

## 2. Relationship to Existing Governance

This control is **not a competing workflow**.

It is integrated conceptually under the existing:

- `MATERIAL MESSAGE GOVERNANCE`;
- `OWNER REVIEW-LOOP COMPRESSION REQUIREMENT`;
- `OWNER PRE-FREEZE DEFECT-PREVENTION REQUIREMENT`.

It governs **how a material execution instruction is prepared and released**.

It does **not** grant execution authority.

A checklist PASS means only that the instruction is sufficiently clean to be sent **if separate execution authority exists**.

---

## 3. Applicability

### 3.1 Universal Agent Rule

This control applies to **all current and future InventorAI agents** whenever the agent performs a function that:

- authors;
- finalizes;
- materially modifies;
- or relays

a **MATERIAL / LOAD-BEARING EXECUTION INSTRUCTION**.

The control follows the **function**, not the model/provider/agent name.

### 3.2 Role Authority Is Unchanged

Universal applicability does not authorize every agent to originate execution.

Under the current role model:

- Owner-side Reviewer does not become Creator execution originator.
- Independent reviewers do not become execution originators.
- Codex review does not become execution originator authority.
- Creator does not self-authorize new load-bearing work.
- Lead remains the centralized execution originator unless later Owner authority explicitly changes that structure.

### 3.3 Non-Material Messages

The full MC-01 through MC-18 checklist is not required for every discussion, recommendation, ordinary review comment, question, or routine mechanical read-only task.

Use proportional control.

---

## 4. Universal Evidence-Integrity Rule

No agent may claim a live verification merely because an expected value appears in an instruction, handover, prior message, or another agent's report.

Always distinguish:

- `TEXTUAL / LOGICAL VERIFICATION`
from
- `LIVE / TOOL-VERIFIED EXECUTION EVIDENCE`.

### 4.1 Claims Requiring Actual Evidence

The following claims require actual tool/execution evidence or explicit reliance on preserved evidence produced by another authorized source:

- filesystem/path verified;
- path exists / path unoccupied;
- hash verified;
- bytes/lines verified;
- repository state verified;
- send completed;
- Creator execution completed;
- diff identity verified;
- artifact identity verified.

If not verified, state:

- `NOT VERIFIED`; or
- `NOT PROVEN`.

### 4.2 Reliance on Another Agent's Evidence

If relying on preserved evidence produced elsewhere, record:

`SOURCE-AGENT / TOOL VERIFIED: YES`

and separately:

`CURRENT AGENT INDEPENDENTLY RE-VERIFIED: YES / NO`

Never silently convert “another source verified this” into “I verified this.”

---

## 5. Mandatory Material Execution-Instruction Pre-Send Checklist

For every material instruction, each applicable control returns:

- `PASS`;
- `FAIL`; or
- `N/A — WITH RATIONALE`.

Material PASS findings must identify the evidence, authority, artifact identity, rule, or instruction section supporting the result.

A bare “checked” or “looks correct” is insufficient.

### MC-01 — Authority Closure

Return:

- `OPEN OWNER DECISIONS: 0 / <count>`
- `INFERRED OWNER DECISIONS: 0 / <count>`
- `CREATOR-DELEGATED LOAD-BEARING CHOICES: 0 / <count>`

PASS requires all material counts = 0.

### MC-02 — Instruction Lifecycle State

The instruction must be clearly one of:

- `DRAFT FOR PRE-EXECUTION REVIEW`; or
- `FINAL EXECUTION INSTRUCTION`.

Return:

- `INSTRUCTION STATE: DRAFT / FINAL`
- `LIFECYCLE CONTRADICTIONS: 0 / <count>`

No draft-only language may remain in the final execution copy.

### MC-03 — Final Instruction Identity

Before final send establish:

- `FINAL INSTRUCTION: IDENTIFIED`
- `FINAL INSTRUCTION ID: <stable identifier>`
- `EXACT FINAL SENT TEXT: PRESERVED BY LEAD`

Where technically practical also preserve:

- SHA-256;
- bytes;
- lines.

A future bare statement such as “sent to Claude” is insufficient exact-send provenance.

### MC-04 — Exact Execution Subject

Identify every material input using the strongest available identity:

- exact input path/location;
- input name;
- hash;
- bytes/lines where useful.

If the intended artifact cannot be identified uniquely:

`FAIL / STOP`

No execution-agent guessing.

### MC-05 — Output Destination / Input Preservation

Where the task creates a repaired/transformed artifact, define:

- exact output path/location;
- whether output must be distinct from input;
- whether input overwrite is authorized or prohibited.

If differential verification requires the original base, preserve it byte-exact.

### MC-06 — Scope Boundary

State:

- authorized changes;
- forbidden changes;
- whether scope expansion is authorized.

No adjacent cleanup merely because it appears desirable.

### MC-07 — Lifecycle / Authorization Fences

State all materially relevant non-authorizations, where applicable, including:

- no implementation;
- no human collection;
- no pilot;
- no freeze;
- no repository mutation;
- no publication;
- no PR;
- no merge.

One authorization must not be interpreted as another.

### MC-08 — No Unresolved Load-Bearing Discretion

Search the instruction for ambiguous delegation, including phrases such as:

- “as applicable”;
- “as appropriate”;
- “if needed”;
- “where suitable”;
- “use best judgment”;
- “choose whichever”;
- equivalent wording.

Classify each occurrence as mechanical or load-bearing.

Required:

`UNRESOLVED LOAD-BEARING CREATOR DISCRETION: 0`

Statistical, architectural, product-policy, governance, evidence-methodology, lifecycle, persisted-state, and ownership choices must not be silently delegated.

### MC-09 — Load-Bearing Method / Formula Precision

Where execution depends on a material:

- formula;
- denominator;
- numerator;
- threshold;
- mapping;
- selection rule;
- state transition;
- precedence rule;
- eligibility rule;
- deterministic branch;

state the governing rule explicitly or cite its exact governing source.

### MC-10 — Provenance / Authority Separation

Verify correct classification of:

- Owner authority;
- Lead analysis;
- Creator evidence;
- independent review;
- Codex/architectural review;
- advisory review;
- repository authority;
- mutable-draft evidence.

Required:

- `AUTHORITY UPGRADES WITHOUT BASIS: 0`
- `AUTHORITY DOWNGRADES WITHOUT BASIS: 0`

### MC-11 — Governing-Reference Resolution

Every material governing reference must be uniquely resolvable.

If a material governing source cannot be resolved uniquely, or material candidate authorities conflict:

`STOP — GOVERNING PROVENANCE AMBIGUITY`

Do not guess.

### MC-12 — STOP Conditions

Define applicable STOP conditions for:

- identity mismatch;
- authority conflict;
- scope conflict;
- missing required evidence;
- unresolvable provenance;
- review-invalidating contradiction;
- other material execution blockers.

Execution agent must not improvise around a STOP.

### MC-13 — Required Evidence Return

Before execution specify the evidence needed to judge the return.

Where applicable include:

- input identity;
- output identity;
- complete diff;
- diff identity;
- repair ledger;
- forbidden-change attestations;
- search/sweep results;
- mechanical-integrity checks;
- transitive-consequence return.

Creator must not claim Lead acceptance.

### MC-14 — Dependency-Bounded Transitive Sweep

For material repairs:

`TRANSITIVE CONSEQUENCE SWEEP: REQUIRED`

but it must be:

- dependency-bounded;
- no broad redesign;
- no unrelated cleanup.

The instruction must define the affected-surface set or rule for determining it.

### MC-15 — Preserved Invariants

List material states that must remain unchanged.

Required:

`SILENT STATUS CHANGE: 0`

Examples include:

- technical defect remains open;
- implementation remains unauthorized;
- prior PASS surfaces do not regress;
- deferred obligations remain discoverable;
- mandatory future gates remain preserved.

### MC-16 — Duplication / Re-Run Control

Verify:

- no duplicate send;
- no automatic full re-run;
- no new parallel owner;
- no duplicate remediation plan;
- no new deferred obligation unless explicitly authorized.

### MC-17 — Pre-Execution Challenge Complete

For material instructions governed by Material Message Governance:

- `PRE-EXECUTION CHALLENGE: COMPLETE`
- `COMPLETE MATERIAL INSTRUCTION-DEFECT SET: OBTAINED`
- `REQUIRED CONSOLIDATED REVISION: COMPLETE / NOT REQUIRED`

Do not send while materially incomplete.

### MC-18 — Final Pre-Send Gate

Return:

`MATERIAL INSTRUCTION PRE-SEND GATE: PASS / FAIL`

PASS requires:

- `OPEN OWNER DECISIONS: 0`
- `UNRESOLVED LOAD-BEARING CREATOR DISCRETION: 0`
- `KNOWN MATERIAL INSTRUCTION DEFECTS: 0`
- `INSTRUCTION LIFECYCLE CONTRADICTIONS: 0`
- `UNRESOLVED MATERIAL PROVENANCE: 0`
- `UNSPECIFIED REQUIRED INPUT / OUTPUT IDENTITY: 0`
- `MISSING MATERIAL STOP CONDITIONS: 0`
- `MISSING MATERIAL EVIDENCE-RETURN REQUIREMENTS: 0`
- `UNEXPLAINED MATERIAL TRANSITIVE CONSEQUENCES: 0`
- `SCOPE EXPANSION: 0`

---

## 6. Final Send Provenance

At actual send, preserve at minimum:

- final instruction ID;
- exact final sent text;
- send occurred after pre-send gate PASS;
- no duplicate send.

Where technically practical also preserve final instruction SHA-256 / bytes / lines.

Creator return must identify the instruction executed.

---

## 7. Failure Handling

If any applicable checklist item returns a **material FAIL**:

- do not send;
- do not self-repair a new load-bearing choice;
- return only the failed MC item(s), exact defect, material consequence, and minimum correction required;
- do not restart broad review unless new material evidence requires it.

---

## 8. Review-Loop Compression Rule

The checklist must reduce review recursion.

If MC-18 passes with all material failure counts = 0 and execution authority exists:

- no extra Owner-side review is required merely for reassurance;
- send through the authorized execution channel;
- preserve exact-send provenance;
- proceed to evidence return and differential post-execution review.

A new reviewer is warranted only when a material decision can actually change.

---

## 9. Successor / Handover Durability

Every successor handover must carry, at minimum:

- `OSP-MEI-PSC-001: ACTIVE`
- current version;
- canonical artifact hash/reference;
- `UNIVERSAL AGENT APPLICABILITY: ACTIVE`
- `FUNCTION-TRIGGERED: YES`
- `MATERIAL-INSTRUCTION ONLY: YES`
- `NO VERIFICATION CLAIM WITHOUT EVIDENCE: ACTIVE`

However:

**the handover is not the source of authority for this control.**

It is only a continuity pointer to this durable control artifact / later repository authority.

---

## 10. Change Control

This control may not be silently modified.

Any material change requires:

1. explicit Owner authority;
2. new version identifier;
3. new content hash;
4. preservation of the prior version for provenance;
5. update to the Owner Standing Process Register.

No successor agent may “simplify” or omit this control merely because it appears burdensome.

---

## 11. Durable Integration Plan

### Current interim durability

Until repository mutation is separately authorized, preserve this exact Markdown artifact as the **canonical interim Owner-standing control artifact**.

The artifact should be retained in the Owner-controlled project/file store and referenced by document ID + version + hash.

### Repository integration

At the already-planned governance placement / integration step, and only when repository mutation is authorized:

1. perform a read-only placement check;
2. integrate this control into the existing process owner under Material Message Governance / Review-Loop Compression / Pre-Freeze Defect-Prevention;
3. avoid duplicate process authority;
4. preserve this document ID and version lineage;
5. update the Owner Standing Process Register to point to the authoritative repository location/commit.

The durable target may be a named section or appendix inside the existing governing process owner rather than a competing standalone workflow.

---

## 12. Non-Negotiable Anti-Loss Rule

This control must survive:

- Lead replacement;
- model/provider change;
- tool change;
- handover compression;
- conversation loss;
- agent reset.

No future agent may treat absence from conversational memory as evidence that the control does not exist.

The authoritative continuity key is:

`OSP-MEI-PSC-001`

plus its current registered version and content hash.

---

## 13. Current Status

`OSP-MEI-PSC-001: ACTIVE`

`VERSION: 1.0`

`OWNER STANDING PROCESS AUTHORITY: YES`

`REPOSITORY DURABLE INTEGRATION: PENDING AUTHORIZED PLACEMENT STEP`

`HANDOVER-ONLY AUTHORITY: NO`

`SUCCESSOR PROPAGATION REQUIRED: YES`

`UNIVERSAL AGENT APPLICABILITY: ACTIVE`

`NO VERIFICATION CLAIM WITHOUT EVIDENCE: ACTIVE`

END CONTROL
