# Workstream 15 — Guidance Consolidation

## Owner Decisions — Canonical Governance Document

Standalone, committed record of the owner-accepted WS15 Owner Decisions
(OD-1 … OD-21). Governance artifact only: it does **not** start WS15, does
**not** create the Increment Contract, performs **no** Status Canonicalization,
and authorizes **no** implementation. Repository truth overrides conversation,
handover, memory, inference, and proposal.

---

## 1. Authoritative base

| Item | Value |
|---|---|
| Repository | `Amirjaferali/inventorai` |
| Authoritative governance branch | `feature/atomic-json-session-persistence` |
| Base commit | `8faffa6d0bd98ac163e01ae2d888524f5f9763ad` (WS14 formal closure) |
| WS15 status at this base | NOT STARTED |
| Committed WS15 Owner Decisions at this base | none (this document is the first) |
| Committed WS15 Increment Contract at this base | none (separate later gate) |

Workstreams 9–14 remain FORMALLY CLOSED at this base; their artifacts are
unchanged.

## 2. Canonical WS15 scope

WS15 is **deterministic cross-module presentation consolidation** of the five
existing display-layer guidance seams through a **shared deterministic
display-layer adapter / abstraction**. The five seams are:

```
answer_coauthoring_prompts
scaffolding_guidance
uncertainty_guidance
clarification_labels
result_feedback
```

The adapter: consumes existing canonical outputs read-only; preserves each
seam's existing activation condition; normalizes active guidance into a common
presentation contract; uses multi-panel normalized composition; preserves
upstream semantic ownership; preserves WS13 protected behavior; creates no
global semantic precedence; creates no new engine semantic layer; creates no
canonical locale owner; and has no persistence or independent state store.

Grounded in WS13 OD-10 (binding invariant: "Cross-module consolidation remains
WS15") and the WS13 Increment Contract R-1. WS15 must not duplicate WS13
in-place defect correction or WS14 semantic post-answer decision logic.

## 3. Approved consolidation model

```
CONSOLIDATION MODEL:      MULTI-PANEL NORMALIZED COMPOSITION
GLOBAL SEMANTIC PRECEDENCE: NONE
PANEL ACTIVATION:         PRESERVE EXISTING SOURCE CONDITIONS
PANEL ORDERING:           FIXED PRESENTATION-ONLY ORDER
```

Approved panel order:

```
1. result_feedback
2. uncertainty_guidance
3. scaffolding_guidance
4. clarification_labels
5. answer_coauthoring_prompts
```

This ordering is rendering-only; it does not establish a semantic winner, does
not suppress active panels automatically, does not alter canonical state, and
does not create blocking, progression, completion, or verification logic.

## 4. Conflict behavior

```
GENUINELY CONFLICTING PRESENTATION CLAIMS ABOUT THE SAME CANONICAL STATE
MUST FAIL EXPLICITLY THROUGH A TYPED PRESENTATION-CONTRACT ERROR.
```

The adapter must not guess which panel is correct, silently suppress a panel,
invent semantic precedence, rewrite upstream meaning, or convert a conflict into
success, completion, progression, verification, or blocking. The exact
implementation type and reason-code shape remain subject to the later Increment
Contract and implementation gate and are **not** invented in this artifact.

## 5. Owner Decisions OD-1 … OD-21

### OD-1 — Operating definition — OWNER APPROVED
WS15 is guidance-consolidation governance/contract work for the five existing
display-layer seams; deterministic cross-module presentation consolidation. No
engine module assumed.

### OD-2 — Realization boundary — OWNER APPROVED — OPTION B
WS15 v1 uses a shared deterministic display-layer adapter/abstraction over the
five seams. It consumes existing canonical outputs, normalizes presentation
contracts, preserves existing semantic ownership and WS13 protected behavior,
introduces no AI/LLM/network/fuzzy/semantic inference, introduces no production-
UI authority, and avoids creating a new engine semantic layer. A new engine
module is not authorized. Exact file/module realization is subject to the
Increment Contract and later source verification.

### OD-3 — Production UI authority — OWNER APPROVED
`WS15 HAS NO PRODUCTION UI AUTHORITY`. WS15 may perform read-only audit and
define display-layer consolidation contracts only. No frontend, production UI,
screen-layout, visual-design, button-copy, or production interaction-design
modification.

### OD-4 — Message consistency — OWNER APPROVED
WS15 includes cross-module consistency for Arabic and English messages,
terminology, guidance labels, equivalent explanation of the same canonical
state, and avoidance of inconsistent guidance across the five seams —
consolidation of existing guidance only, not UX redesign.

### OD-5 — Arabic/English parity — OWNER APPROVED
Arabic and English outputs must preserve equivalent canonical meaning; identical
wording is not required; language rendering must not alter decision identity,
state meaning, blocking meaning, completion meaning, or required next action.

### OD-6 — Conflicting messages — OWNER APPROVED
The consolidated guidance layer must not emit conflicting messages for the same
canonical state; precedence must be deterministic and based only on existing
canonical inputs; WS15 must not create new semantic logic to resolve conflicts;
the exact precedence/conflict contract is defined in the Increment Contract.

### OD-7 — Progress/completion/progression/verification display — OWNER APPROVED — PRESENTATION ONLY
WS15 owns presentation-level distinction between progress, completion,
progression permission, and technical verification. WS14 and existing engine
seams retain semantic ownership. WS15 consumes those states read-only and must
not derive, modify, reinterpret, or reimplement them.

### OD-8 — Open and deferred item presentation — OWNER APPROVED — PRESENTATION ONLY
WS15 owns consolidated presentation of existing open and deferred items. WS14
and upstream engine records retain semantic derivation and source-of-truth
ownership. WS15 must not create an independent open-item store, close or reopen
items, infer missing item state, or alter progression or completion.

### OD-9 — Blocking explanation — OWNER APPROVED
WS15 may consolidate presentation of why progression is blocked and what
canonical next action is available, consuming existing blocking rules and reason
data only. WS15 must not invent blocking reasons, next-step semantics, technical
recommendations, or completion conditions.

### OD-10 — Decision-reason display — OWNER APPROVED
WS15 may consolidate display of existing deterministic reason codes and their
canonical references. WS15 must not create or redefine the WS14 decision-reason
taxonomy; Arabic and English rendering must not change reason identity.

### OD-11 — Missing/unavailable/invalid data display — OWNER APPROVED
WS15 may consolidate presentation of existing `INCOMPLETE`, `UNAVAILABLE`, and
typed input-error states. These remain upstream semantic states; WS15 must not
silently convert them into success, completion, retry, follow-up, blocking, or
technical verification.

### OD-12 — RTL — OWNER APPROVED
RTL is a read-only audit constraint during WS15. WS15 may record RTL findings
and consolidation constraints. No production RTL modification is authorized; any
implementation belongs to the later Product UX/UI Workstream after WS16 unless
separately authorized.

### OD-13 — Accessibility — OWNER APPROVED
`FORWARD PRODUCT UX/UI RESPONSIBILITY — NOT WS15`. WS15 may record read-only
findings only; no accessibility implementation is authorized.

### OD-14 — Non-technical-user clarity — OWNER APPROVED
WS15 may define clarity constraints for consolidated guidance intended for a
non-technical user. This does not authorize user research, comprehension
testing, redesign, production UI implementation, or engineering-instruction
generation.

### OD-15 — End-to-end journey review — OWNER APPROVED
`DOWNSTREAM WS16 RESPONSIBILITY — DO NOT PREEMPT`. WS15 may identify presentation
seams and risks only; it must not perform full end-to-end owner validation.

### OD-16 — Message comprehension measurement — OWNER APPROVED
`FORWARD PRODUCT UX/UI RESPONSIBILITY — NOT WS15`. No user research, usability
study, or comprehension measurement is authorized during WS15.

### OD-17 — UX/UI debt register — OWNER APPROVED
WS15 may create one governance-only deferred UX/UI debt register. Every item
must be evidence-linked and marked deferred; it must not become a production
backlog automatically, must not activate the Product UX/UI Workstream, must not
authorize implementation, and remains review input for the Product UX/UI
Workstream after WS16.

### OD-18 — WS14 deferred obligations — OWNER APPROVED
```
S2 — NOT WS15
S3 — NOT WS15
S5 — ENGINE TAXONOMY NOT WS15
S6 — RESOLVED FOR PRESENTATION OWNERSHIP ONLY
```
WS15 owns presentation consolidation only for S6. No WS14 semantic or engine
obligation transfers to WS15.

### OD-19 — WS13 ownership protection — OWNER APPROVED
WS15 must preserve WS13's existing in-place guidance behavior and protected
tests. Consolidation must not rewrite semantic ownership or remove existing
behavior without a separately accepted defect and authorization.

### OD-20 — Determinism and no-AI posture — OWNER APPROVED
WS15 v1 has no AI, no LLM, no embeddings, no network dependency, no fuzzy
semantic matching, no hidden fallback, no text-derived canonical state identity,
no random presentation selection, and deterministic replay from the same
canonical inputs.

### OD-21 — No automatic downstream activation — OWNER APPROVED
Every later gate requires separate owner authorization: Increment Contract,
Status Canonicalization, Bounded Defect Search, BASE RED, GREEN, WS16, Product
UX/UI Workstream. Nothing activates automatically.

## 6. Language and Arabic scope

```
WS15 EN/AR PARITY: AUDIT-SCOPED
```

WS15 may consolidate existing committed copy, preserve the bilingual
`uncertainty_guidance` behavior, identify and report structural Arabic coverage
gaps, and require equivalent canonical meaning where Arabic and English variants
already exist. WS15 must not generate new Arabic copy, translate the four
English-only seams, introduce translation keys, introduce a locale framework,
create a canonical locale owner, silently represent English output as Arabic, or
create automatic machine translation. For the four English-only seams
(`answer_coauthoring_prompts`, `scaffolding_guidance`, `clarification_labels`,
`result_feedback`):

```
ARABIC OUTPUT: UNAVAILABLE — STRUCTURAL COVERAGE GAP
```

## 7. RTL boundary

```
RTL DURING WS15: READ-ONLY AUDIT CONSTRAINT
```

WS15 may consume the existing uncertainty-panel `lang` and `dir` metadata
read-only. WS15 must not create page-level RTL ownership, modify production
templates or layout, infer global RTL from one panel, or implement production
RTL. Page-level RTL remains a forward Product UX/UI responsibility after WS16
unless separately authorized.

## 8. Presentation-only responsibilities

WS15 may consolidate presentation of existing progress, completion, progression
permission, technical verification, open items, deferred items, blocking
explanations, canonical next actions, reason codes and references, `INCOMPLETE`,
`UNAVAILABLE`, and typed input-error states. WS15 must not derive or modify
semantic states, close or reopen items, infer missing item state, alter
progression/completion/verification, invent blocking reasons or next-step
semantics, create the WS14 reason-code taxonomy, or create an independent
open-item store.

## 9. Production UI prohibition

```
WS15 HAS NO PRODUCTION UI AUTHORITY
```

No authorization exists for frontend modification, production UI changes,
screen-layout changes, visual design, button-copy changes, production
interaction-design changes, production RTL implementation, or accessibility
implementation.

## 10. UX/UI review boundaries

```
DURING WS15: READ-ONLY UX/UI AUDIT AND PRESENTATION-CONSOLIDATION GOVERNANCE
WS16:        END-TO-END OWNER VALIDATION
AFTER WS16:  FULL PRODUCT UX/UI WORKSTREAM
```

Accessibility implementation and message-comprehension measurement are forward
Product UX/UI responsibilities. Full end-to-end journey review must not preempt
WS16. The governance-only deferred UX/UI debt register is permitted but must not
activate implementation, become an automatic production backlog, activate the
Product UX/UI Workstream, or authorize remediation.

## 11. WS14 obligation boundary

```
S2 — NOT WS15
S3 — NOT WS15
S5 — ENGINE TAXONOMY NOT WS15
S6 — RESOLVED FOR PRESENTATION OWNERSHIP ONLY
```

No WS14 semantic or engine obligation transfers to WS15.

## 12. Determinism

WS15 v1 has no AI, no LLM, no embeddings, no network dependency, no fuzzy
semantic matching, no hidden fallback, no text-derived canonical state identity,
no random presentation selection, and deterministic replay from the same
canonical inputs.

## 13. Explicit non-goals

New engine semantic module; production UI or frontend modification; redesign;
new semantic precedence; new blocking semantics; new completion or progression
logic; new reason-code taxonomy; new locale owner; new Arabic content; machine
translation; production RTL; accessibility implementation; user research;
comprehension measurement; end-to-end owner validation; independent state store;
WS13 behavior rewriting; WS14 semantic reimplementation; WS16 or Product UX/UI
activation; D13 / Structured Technical Guidance; Patent Export; WS-PFV-001;
CAP-12, CAP-13, CAP-14; AI Coach.

## 14. Workstream boundaries

```
WS13:        in-place guidance seams
WS14:        semantic post-answer decisions
WS15:        deterministic cross-module presentation consolidation
WS16:        end-to-end owner validation
After WS16:  full Product UX/UI Workstream
```

## 15. Status statement

```
OWNER DECISIONS:        COMPLETE AND OWNER APPROVED
WS15 IMPLEMENTATION:    NOT STARTED
INCREMENT CONTRACT:     NOT YET COMMITTED
STATUS CANONICALIZATION: NOT STARTED
DEFECT SEARCH:          NOT STARTED
BASE RED:               NOT STARTED
GREEN:                  NOT STARTED
```

WS15 is not formally started, implemented, or closed by this document. The WS15
Increment Contract must be committed as its own separate governance artifact in a
separately authorized gate before any §15 status row records the Increment
Contract as approved. `engine/adaptive_follow_up.py` remains absent; the
WS13/WS14 absence guards remain unchanged; Workstreams 9–14 remain FORMALLY
CLOSED. WS16, WS17, D13 (Structured Technical Guidance), Patent Export,
WS-PFV-001, CAP-12/CAP-13/CAP-14, and the AI Coach remain inactive, blocked,
separately gated, or unauthorized. No automatic downstream activation occurs.
