# InventorAI Governance Roadmap

**Document type:** Governance and architecture review
**Date:** 2026-05-30
**Status:** Assessment only — no implementation authorized
**Depends on:** GD-001, GD-002, ILT-001 Final Assessment Report

---

## Preamble

ILT-001 proved lifecycle integrity. The complete Stage Two inventor journey
traverses MC to PF to BA correctly. Completion is governed by gap closure,
not iteration count. The Inventor Ownership Principle holds throughout.

This roadmap records the strategic concerns that remain unresolved after
ILT-001 and defines the governance assessment work required before any
future implementation is authorized.

Evidence before implementation remains mandatory for every item below.

---

## Priority 1 — Knowledge Integrity

### Status: Assessment in progress

ILT-001 proved lifecycle integrity. It did not prove knowledge integrity.

The platform can traverse MC to PF to BA. The remaining question is whether
the platform can distinguish meaningful participation from non-participation.

The Response Quality Governance Assessment (docs/governance/RESPONSE-QUALITY-
GOVERNANCE-ASSESSMENT.md) addresses this question in full. Key conclusions:

The Participation Floor and the Quality Floor are distinct problems. The
existing classifier handles quality. A Participation Floor — not yet
implemented — would handle participation.

Six categories of non-participation are defined:
1. Keyboard noise
2. Filler repetition
3. Off-topic responses
4. Content-free acknowledgment
5. Restated question
6. AI Echo Response (see Priority 2)

The Participation Floor must not evaluate engineering correctness, expertise
level, educational background, or domain specialization. Its sole purpose
is to distinguish participation from non-participation.

Six governance questions must be answered before any design begins. See
RESPONSE-QUALITY-GOVERNANCE-ASSESSMENT.md Section 11.

### Constraint

The platform should reject non-participation.
The platform must not reject genuine but weak reasoning from non-specialist
inventors.

---

## Priority 2 — AI Echo Risk

### Status: Identified — governance treatment required

Proposed category: AI Echo Response

Definition: The inventor copies or paraphrases platform-provided guidance
without contributing original reasoning, assumptions, constraints, decisions,
trade-offs, or analysis.

Example: The platform explains a sensing method. The inventor repeats the
explanation. The response may appear high quality and score REASONED in the
existing classifier while demonstrating no original inventor understanding.

### Current risk level: LOW

The risk is low in the current lifecycle because the platform does not
provide significant technical guidance. The current platform asks questions;
it does not explain technologies.

### Future risk level: HIGH

If a Technical Guidance layer is introduced under GD-002, the platform will
explain technologies, present alternatives, and recommend paths. At that
point, AI Echo responses become systematically more likely and the classifier
may score them as REASONED. The Inventor Ownership Principle would be
violated at scale.

### Governance requirement

AI Echo governance must be assessed and resolved before any Technical
Guidance layer is deployed. This is a hard dependency, not a recommendation.

### Distinguishing characteristic

AI Echo responses are not empty. They contain genuine domain content. The
governance problem is provenance, not quality. The content originated with
the platform, not the inventor. This connects directly to GD-002 knowledge
source separation.

None of the five Participation Floor approaches (A through E) addresses
Category 6 without a separate provenance tracking mechanism. This mechanism
is not appropriate for the current architecture and must be designed
separately as part of GD-002 Technical Guidance layer design.

---

## Priority 3 — Project vs Session

### Status: Unassessed — assessment required before persistence design

A major unresolved architectural question: is InventorAI fundamentally a
session system or a project platform?

Current architecture: session-oriented. Sessions live in memory. No
persistence. Server restart loses all sessions.

### The distinction matters because:

A session system implies: one idea, one pass, done.
A project platform implies: an inventor has an ongoing relationship with
their idea across multiple sessions, versions, and states.

### Assessment questions

Project identity: What uniquely identifies a project? Is it the inventor,
the idea text, a user-assigned name, a system-generated ID, or some
combination?

Project naming: When does naming occur? At creation before any responses,
after completion, or at any point? Naming at creation requires the inventor
to have a name before they understand what they are building. Naming after
completion is more natural but requires the platform to hold unnamed drafts.

Draft state: What constitutes a draft? A session where at least one response
has been submitted? A session where at least one gap has been opened? An
idea text saved before any responses?

Resume capability: What does resume mean? Returning to the same gap state?
Starting a new iteration from the same idea text? The answer determines
both the data model and the user experience.

Project status lifecycle: What states can a project be in? See Priority 4.

Multiple projects per inventor: Does the platform support multiple
concurrent invention projects for a single user? If yes, what is the
identity model — accounts, tokens, or something else?

Project ownership: The inventor owns the idea. Does the inventor also own
the right to export, delete, or transfer their project data? This is a
product and legal question, not only a technical one.

### Constraint

No persistence architecture should be designed before Priority 3 questions
are answered and before GD-002 knowledge source separation is fully defined.
Persisting a state that blurs inventor knowledge and platform recommendation
would create a governance problem that is very difficult to correct after
the fact.

---

## Priority 4 — Drafts, Persistence, and Versioning

### Status: Unassessed — depends on Priority 3

### Proposed project states

Draft: The inventor has begun but not completed the lifecycle.
In Progress: The inventor is actively working through the lifecycle.
Complete: All Stage Two gaps are closed and the lifecycle has terminated.
Archived: The inventor has closed the project without completing it, or has
superseded it with a newer version.

### Versioning question

Should an inventor be able to create multiple versions of the same invention
rather than independent disconnected projects?

Example:
Smart Irrigation Sensor
  Version 1 — initial concept
  Version 2 — revised after external feedback
  Version 3 — updated mechanism understanding

Version history preserves the relationship between iterations. Independent
projects lose this relationship but are simpler to implement and govern.

### Governance implications

If versions are supported, the knowledge source separation requirement
becomes more complex. Which version of inventor knowledge is authoritative?
Can platform recommendations from Version 1 influence Version 2? These
questions must be answered at the governance level before architecture begins.

If drafts are supported, the platform must define what happens to a draft
that is never completed. Does it expire? Does it remain indefinitely?
Who governs retention?

### Constraint

Persistence and versioning design cannot begin before:
1. Priority 3 questions are answered
2. GD-002 knowledge source separation is defined
3. Owner approves a persistence architecture proposal

---

## Priority 5 — Knowledge Source Separation

### Status: Defined in GD-002 — architecture not yet designed

GD-002 requires future architecture to explicitly distinguish:

- Inventor Knowledge: content originating from the inventor's own reasoning
- Platform Recommendation: guidance, alternatives, or paths suggested by
  the platform
- External Expert Advice: input from domain experts outside the platform
- Unverified Assumption: claims made by the inventor that have not been
  validated

These categories must never be merged in the invention record.

### Why this is critical for persistence and versioning

Once sessions are persisted, the invention record becomes a long-lived
artifact. If knowledge source separation is not enforced at the persistence
layer, it cannot be enforced retroactively. A persisted record that blurs
inventor knowledge and platform recommendation is ungovernable.

### Why this is critical for AI Echo governance

AI Echo responses (Priority 2) are the failure mode where this separation
breaks down at the classification level. Platform content re-enters the
record as inventor knowledge. Knowledge source separation at the data model
level would make this detectable and preventable.

### Assessment required

Before any persistence design, a formal assessment of how knowledge source
separation is enforced at the data model level is required. This assessment
does not exist yet.

---

## Priority 6 — Multi-Domain Scalability

### Status: Architecture partially in progress (Phase 5 migration)

The long-term vision includes domains beyond electronics:

- electronics
- electrical systems
- embedded systems
- PCB design
- software
- communications
- robotics
- solar energy
- manufacturing
- materials

### Current position

The engine is domain-agnostic. The domain knowledge layer is being migrated
from hardcoded domain_rules.py to a capability pack architecture
(domains/iot_electronics/). The Phase 5 migration is in progress but not
complete.

### Confirmed architectural constraint

Domain-specific logic must not be embedded in the engine core. Adding a
new domain must not require modifying core engine files. This constraint
is currently met in design intent and partially met in implementation.

### Assessment question

Can multi-domain technical guidance (GD-002 Technical Guidance layer) be
achieved while preserving deterministic workflow governance and inventor
ownership?

This question cannot be answered until GD-002 architecture assessment is
complete. It is recorded here as a dependency.

### Constraint

Any future domain addition must be validated against the domain-agnostic
engine principle. The Participation Floor must also remain domain-agnostic —
it cannot require per-domain tuning.

---

## Priority 7 — Inventor Development

### Status: Not yet addressed — future governance topic

ILT-001 proved session progression. It did not prove inventor development.

The long-term goal of InventorAI is not simply to complete sessions. The
goal is to help inventors think more clearly, define ideas more rigorously,
and make better decisions over time.

### The unasked question

How does the platform determine whether an inventor is improving?

A session can be completed successfully without the inventor having
developed any genuine understanding. They may have been guided through
the correct responses by the platform's questioning without internalizing
the reasoning.

### Why this matters

If the platform is optimized for session completion rates, it may produce
metrics that look positive while failing to achieve the product's actual
purpose. A platform that helps inventors complete sessions is different from
a platform that helps inventors become better inventors.

### Future governance questions

What evidence would demonstrate that an inventor has improved across
multiple sessions?

Is improvement measurable within the current evidence model (ASSERTED vs
REASONED, gap closure, iteration count)?

Should the platform attempt to measure inventor development at all, or
is this an external validation question?

If version history is implemented (Priority 4), does the quality trajectory
across versions constitute evidence of inventor development?

### Constraint

No implementation is proposed. This is recorded as a future governance topic
that must be considered before any analytics or reporting layer is designed.

---

## Priority 8 — Not Yet Proven

### Status: Explicitly tracked as unverified capabilities

The following capabilities are defined in the product vision but have not
been proven in any validation campaign:

Structured Review Lifecycle: The process by which an inventor takes their
completed Stage Two record and prepares it for structured technical review.
Not implemented. Not validated.

Expert Review Flow: The process by which external domain experts review and
provide feedback on an inventor's record. Not implemented. Not validated.

Feedback-to-Revision Loop: The process by which expert feedback re-enters
the inventor journey and produces a new iteration. Not implemented. Not
validated.

R-007 — FDC-001 end-to-end verification: idea_summary is read via getattr
and is likely always None. The FDC-001 package has been assembled in tests
but has not been verified to produce a non-empty invention summary from a
real live session. This is a known open item from ILT-001.

### Constraint

These items must not be treated as implemented capabilities. They must not
be referenced in any user-facing documentation or marketing claims. They
remain future work items requiring independent validation campaigns before
they can be considered proven.

---

## Governance Dependency Map

The following dependencies govern sequencing. No item should be designed
before its dependencies are resolved.

Participation Floor design
  depends on: governance questions 1-6 answered (RESPONSE-QUALITY-
  GOVERNANCE-ASSESSMENT.md Section 11)

AI Echo governance design
  depends on: GD-002 Technical Guidance layer design
  depends on: Participation Floor design complete

Persistence architecture
  depends on: Priority 3 questions answered
  depends on: GD-002 knowledge source separation defined

Versioning design
  depends on: Persistence architecture approved
  depends on: Priority 3 questions answered

Technical Guidance layer design
  depends on: GD-002 architecture assessment complete
  depends on: AI Echo governance resolved
  depends on: Knowledge source separation defined

Multi-domain expansion
  depends on: Phase 5 capability pack migration complete
  depends on: Technical Guidance layer design approved

Inventor Development metrics
  depends on: Versioning design complete
  depends on: Knowledge source separation defined

---

## Immediate Next Actions

Before any future implementation work is authorized:

1. Close deferred disclosure findings: D-001, D-002, D-004
2. Verify R-007 (FDC-001 idea_summary in live session)
3. Execute ILT-001S (stall detection probe)
4. Answer governance questions 1-6 in RESPONSE-QUALITY-GOVERNANCE-ASSESSMENT
5. Produce GD-002 architecture assessment
6. Define knowledge source separation at data model level
7. Answer Priority 3 project identity questions
8. Return with design proposals for owner review

No implementation precedes owner approval of the relevant assessment and
design proposal for that item.

---

*Roadmap date: 2026-05-31*
*Based on: ILT-001 Final Assessment Report, GD-002, owner priorities 1-8, Stage 2 completion commit 5661504 → WPS001 restored at 65acf6e*
*Status: Governance record only — no implementation authorized*
*Stage 2 COMPLETE — commit 5661504 → WPS001 restored at 65acf6e — artifacts: STRATEGIC_PRODUCT_VISION.md, DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md, STAGE2_REVIEW_DECISIONS.md, OFFICIAL_BENCHMARK_BASELINE.md*
