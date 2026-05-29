# GD-002 — Technical Guidance Without Decision Ownership

**Status:** PROPOSED
**Implementation Status:** NOT AUTHORIZED
**Architecture Status:** ASSESSMENT REQUIRED
**Date proposed:** 2026-05-30
**Depends on:** GD-001 (three-stage inventor journey)

This document records direction and constraints only.

It does not authorize:

- workflow changes
- engine changes
- UI changes
- gap changes
- technical guidance implementation

---

## 1. Core Principle

InventorAI owns technical guidance but never owns technical decisions.

---

## 2. Inventor Ownership

The inventor owns:

- the problem
- objectives
- constraints
- assumptions
- invention intent
- final design decisions

---

## 3. Platform Permissions

The platform MAY:

- explain technologies
- explain concepts
- present alternatives
- compare trade-offs
- identify risks
- identify missing information
- organize knowledge
- recommend possible paths
- suggest areas requiring external expertise

---

## 4. Platform Prohibitions

The platform MUST NOT:

- automatically choose engineering solutions
- automatically commit design decisions
- generate inventions on behalf of inventors
- transform recommendations into inventor knowledge
- replace inventor reasoning

---

## 5. Recommendations Are Not Inventor Knowledge

Recommendations must remain separate from inventor knowledge.

A recommendation becomes inventor knowledge only when:

1. the inventor explicitly accepts it
2. the inventor explains it in their own reasoning
3. the inventor confirms it as part of the invention concept

Until all three conditions are satisfied, any platform recommendation remains
platform output — not inventor knowledge — and must not be recorded as such.

---

## 6. Target User Clarification

InventorAI is not intended only for technical specialists.

Many inventors understand:

- the problem
- the desired outcome
- the customer need

but may not understand:

- electronics
- electrical systems
- embedded systems
- PCB design
- communications
- software architecture
- manufacturing
- materials
- solar systems
- robotics

The platform should help such inventors understand technical possibilities
without taking ownership of technical decisions.

---

## 7. Future Technical Guidance Layer

No implementation authorized.
Future work only.

The future platform may eventually support technical guidance across:

- electronics
- electrical systems
- embedded systems
- software
- PCB design
- communications
- solar energy
- robotics
- manufacturing considerations
- materials

without embedding domain-specific logic into the engine core.

Architecture assessment required before any design work.

---

## 8. Response Quality Contract

Future governance proposal only.
No implementation authorized.

Future platform should distinguish:

1. nonsense input
2. filler content
3. off-topic responses
4. low-information responses
5. reasoned responses

Examples that should never advance workflow:

- 444444444444
- asdfasdfasdf
- repeated filler text
- unrelated responses

The objective is not technical correctness.
The objective is minimum meaningful participation.

Architecture options must be assessed before any implementation is proposed.

---

## 9. Knowledge Source Separation

Future architecture should explicitly distinguish:

- inventor knowledge
- platform recommendation
- external expert advice
- unverified assumption

These categories must never be merged.

---

## 10. Status Clarification

ILT-001 proved:

- lifecycle traversal
- gap progression
- gap closure
- state integrity
- inventor ownership

ILT-001 did NOT yet prove:

- Structured Review Lifecycle
- Expert Review Flow
- Feedback-to-Revision Loop
- R-007 (FDC-001 end-to-end verification)

Open findings remain:

- D-001
- D-002
- D-004

These items remain separate from GD-002.

---

## 11. Required Next Actions

1. Complete ILT-001 evidence package.
2. Complete ILT-001 final report.
3. Verify R-007.
4. Close D-001, D-002, D-004.
5. Perform architecture assessment for GD-002.
6. Return recommendations before any implementation.

Evidence before implementation remains mandatory.

---

*GD-002 proposed: 2026-05-30*
*Status: PROPOSED — awaiting architectural assessment*
*No implementation authorized*
