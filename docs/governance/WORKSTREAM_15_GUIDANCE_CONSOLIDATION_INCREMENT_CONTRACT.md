# Workstream 15 — Guidance Consolidation

## Increment Contract — Canonical Governance Document

Standalone, committed WS15 Increment Contract recording the revised,
owner-accepted v1 policy and scope. Governance artifact only: it does **not**
start WS15, does **not** perform Status Canonicalization, does **not** begin
Bounded Defect Search / BASE RED / GREEN, and authorizes **no** implementation.
Repository truth overrides conversation, handover, memory, inference, and
proposal.

Governing Owner Decisions: OD-1 … OD-21 committed at
`dedfba4217fd649de5dadf82b85f0e9900e33df7`
(`docs/governance/WORKSTREAM_15_GUIDANCE_CONSOLIDATION_OWNER_DECISIONS.md`).
Where this contract and the Owner Decisions ever diverge, the Owner Decisions
control.

---

## 1. Header decisions

```
Adapter realization:        NEW DISPLAY-LAYER ADAPTER / ABSTRACTION
Engine module:              NOT AUTHORIZED
Consolidation model:        MULTI-PANEL NORMALIZED COMPOSITION
Global semantic precedence: NONE
Panel activation:           PRESERVE EXISTING SOURCE CONDITIONS
Panel ordering:             FIXED PRESENTATION-ONLY ORDER
Conflict behavior:          TYPED EXPLICIT PRESENTATION-CONTRACT ERROR
EN/AR parity:               AUDIT-SCOPED
New Arabic content:         NOT AUTHORIZED
Canonical locale owner:     NONE / NOT CREATED
RTL:                        EXISTING SINGLE-PANEL METADATA CONSUMED READ-ONLY
                            PAGE-LEVEL RTL DEFERRED
```

## 2. Purpose and base

Smallest WS15 v1 increment implementing or verifying **deterministic
cross-module presentation consolidation** of the five existing display-layer
guidance seams via a **new display-layer adapter/abstraction (OD-2 Option B)**
using **multi-panel normalized composition**. Implementation is not assumed.

| Item | Value |
|---|---|
| Base commit (Owner Decisions) | `dedfba4217fd649de5dadf82b85f0e9900e33df7` |
| WS14 formal closure ancestry | `8faffa6d0bd98ac163e01ae2d888524f5f9763ad` |
| Authoritative governance branch | `feature/atomic-json-session-persistence` |

Boundaries preserved: WS13 (in-place guidance seams) · WS14 (semantic
post-answer decisions) · **WS15 (deterministic cross-module presentation
consolidation)** · WS16 (end-to-end owner validation) · After WS16 (full Product
UX/UI Workstream). WS15 must not duplicate WS13 or reimplement WS14.

## 3. Exact five-seam input contract (SC-1 confirmed)

### answer_coauthoring_prompts
```
get_answer_coauthoring_prompts(gap_type)
Output: { heading, prompts: list, note }
Unknown or None: _FALLBACK
Language: English only
```

### scaffolding_guidance
```
get_scaffolding_guidance(last_result, gap_type=None)
Output on transition == WARN: { heading, lead, prompts: list, note }
Otherwise: None
Language: English only
```

### uncertainty_guidance
```
get_uncertainty_guidance(text)
Output: { heading, prompts, note, eyebrow, lang, dir }
Arabic cue: lang = ar, dir = rtl
Otherwise: lang = en, dir = ltr
Not uncertainty: None
Language: English and Arabic
```

### clarification_labels
```
get_clarification(gap_type)
Output: { label, plain_language, information_needed, answer_shape, support_hint }
None: _FALLBACK
Language: English only
```

### result_feedback
```
get_result_feedback(last_result)
Output: plain-language string for recognized PASS/WARN transition
No result or unrecognized transition: None
Language: English only
```

**Source-confirmed fact:** these seams currently **never raise** for their
normal unsupported or inactive inputs; they return `None` or `_FALLBACK`. No
translation-key system exists (SC-7); all copy is hardcoded module constants.

## 4. Adapter contract (OD-2 Option B; SC-2)

A **new display-layer adapter/abstraction — not an engine module.** It must:
consume all five seams independently; preserve every seam's existing activation
condition; normalize each active seam into a common presentation panel; compose
zero or more active panels deterministically; preserve upstream semantic
ownership; preserve WS13 protected behavior; create no global semantic
precedence; create no canonical state; create no independent state store;
persist nothing; perform no network or external calls; and modify no upstream
value.

A normalized panel may include:
```
seam_id · kind · title · body_parts · reason_display · lang · dir
```
The exact typed implementation form remains subject to later source and defect
verification (`PROPOSED — AWAITING OWNER REVIEW` for the concrete type).

## 5. Fixed presentation-only ordering (SC-4; owner decision)

```
1. result_feedback
2. uncertainty_guidance
3. scaffolding_guidance
4. clarification_labels
5. answer_coauthoring_prompts
```
This order controls rendering order only; it creates no semantic winner, does
not suppress active panels, does not alter activation, and does not change
blocking/progression/completion/verification. It may change only through a later
owner-approved contract amendment. If the Bounded Defect Search reveals a
committed-source contradiction with this order, STOP and report — do not silently
reorder.

## 6. Conflict behavior (owner decision)

When active panels make genuinely conflicting presentation claims about the same
canonical state:
```
FAIL EXPLICITLY WITH A TYPED PRESENTATION-CONTRACT ERROR
```
The adapter must not guess, silently suppress a panel, rewrite upstream meaning,
infer semantic precedence, or convert conflict into success / completion /
progression / verification / blocking. The exact exception class and bounded
reason-code vocabulary remain future implementation details and are **not**
invented in this artifact (they reuse the existing typed `*Error(reason_code)`
pattern).

## 7. Language and Arabic contract (SC-5/SC-7; owner decision)

```
WS15 EN/AR PARITY: AUDIT-SCOPED
```
WS15 v1 may: consolidate existing committed copy; preserve bilingual uncertainty
guidance; identify structural Arabic coverage gaps; audit existing Arabic/English
variants for equivalent canonical meaning. WS15 v1 must not: generate new Arabic
content; translate the four English-only seams; introduce translation keys;
introduce an i18n framework; introduce a canonical locale owner; create machine
translation; silently represent English copy as Arabic; or alter page-level
language behavior. For the four English-only seams:
```
ARABIC OUTPUT: UNAVAILABLE — STRUCTURAL COVERAGE GAP
```
This is an audit finding, not a runtime exception in the existing seams.

## 8. Locale and RTL boundaries (SC-5/SC-6; owner decision)

```
CANONICAL LOCALE OWNER: NONE — WS15 MAY NOT CREATE ONE
```
The uncertainty-panel language inference (`_uncertainty_language`) remains scoped
to that panel only.
```
RTL: PRESENTATION-ONLY SINGLE-PANEL SEAM — READ-ONLY DURING WS15
```
WS15 may consume the existing uncertainty-panel `lang` and `dir` values. WS15
must not create page-level RTL, modify templates or layouts, infer global RTL
from one panel, or create session/profile locale ownership. Page-level language
and RTL are forward Product UX/UI responsibilities after WS16.

## 9. Presentation-only ownership (OD-7…OD-11; SC-8)

WS15 may consolidate presentation of existing: progress; completion;
progression permission; technical verification; open items; deferred items;
blocking explanations; canonical next actions; reason codes and references;
`INCOMPLETE`; `UNAVAILABLE`; typed input-error states. WS15 must not: derive
these states; modify them; close or reopen items; infer missing states; alter
progression/completion/verification; invent blocking reasons or next-step
semantics; create the WS14 reason taxonomy; or create an independent open-item
store. (SC-8: semantics are engine-owned; presentation is currently scattered
inline in `web/app.py` with no consolidated owner.)

## 10. Failure-mode contract

| Failure mode | Required behavior |
|---|---|
| Missing canonical source | preserve existing `None`/`_FALLBACK`; omit inactive panel; no fabrication |
| Conflicting active panels | typed explicit presentation-contract conflict |
| Missing reason code | explicit unavailable/no-reason presentation; no invention |
| Requested Arabic unavailable | structural coverage gap; no silent substitution |
| Invalid normalized payload | typed presentation-contract error |
| `INCOMPLETE` | preserve unchanged |
| `UNAVAILABLE` | preserve unchanged |
| Typed upstream error | preserve as error state |
| Missing RTL metadata | audit finding only |

No silent misleading fallback.

## 11. Testing contract (future; none created/run by this artifact)

Identical-input deterministic replay; fixed panel-order determinism; existing
activation conditions preserved; no active-panel automatic suppression;
conflicting panels fail explicitly; no semantic precedence created; four
English-only seams report structural Arabic gap; no new Arabic copy generated;
no locale owner created; uncertainty-panel `lang`/`dir` consumed read-only;
progress/completion/progression/verification remain distinct; open/deferred item
semantics unchanged; blocking explanation consumes existing data only; no
invented next action; reason-code identity preserved; `INCOMPLETE`/`UNAVAILABLE`/
typed errors preserved; no AI/network/fuzzy/hidden fallback; no store/persistence;
no production UI change; WS13 protected behavior remains green; WS14 semantic
boundaries remain green; no WS16 or Product UX/UI activation. Not created or run
in this gate.

## 12. Read-only audit contract

English/Arabic consistency findings; RTL findings; non-technical-user clarity
findings; conflicting-message findings; overclaiming beyond engine truth;
missing or ambiguous guidance; deferred UX/UI debt. The governance-only UX/UI
debt register (OD-17) is permitted but must remain evidence-linked, explicitly
deferred, not an automatic backlog, non-implementing, non-activating, and review
input after WS16 only.

## 13. Explicit non-goals

Engine semantic module; production UI modification; frontend redesign; visual or
interaction redesign; new semantic precedence; new blocking semantics; new
progression/completion/verification logic; new reason-code taxonomy; new locale
owner; new Arabic content; machine translation; production RTL; accessibility
implementation; user research; comprehension measurement; end-to-end owner
validation; independent store; WS13 behavior rewriting; WS14 semantic
reimplementation; WS16 activation; Product UX/UI activation; D13 / Structured
Technical Guidance; Patent Export; WS-PFV-001; CAP-12, CAP-13, CAP-14; AI Coach.

## 14. Traceability

| Ref | Contract clause | Consumed source | Modification prohibited | Future test family |
|---|---|---|---|---|
| OD-1 / OD-2 / SC-2 | §4 adapter (new display-layer, no engine module) | five seams; no existing adapter | Yes | adapter shape; replay |
| OD-6 / SC-4 | §5 fixed order; §6 no semantic precedence | independent `app.py` slots | Yes | order determinism; no-precedence |
| owner-dec conflict / OD-6 | §6 typed conflict error | existing `*Error(reason_code)` | Yes | conflicting-panels-fail |
| OD-4/OD-5 / SC-5/SC-7 | §7 audit-scoped parity | 4 EN-only + 1 EN/AR seam; no locale owner | Yes | structural-gap; no-new-AR |
| OD-12 / SC-6 | §8 RTL panel-consume; page-forward | `uncertainty_guidance` `lang`/`dir` | Yes | RTL read-only |
| OD-7/OD-8 / SC-8 | §9 presentation-only consolidation | `maturity_label`, `get_open_gaps`, dispositions | Yes | progress≠completion≠verification |
| OD-9/OD-10/OD-11 | §9/§10 blocking/reason/error display | `decision_workspace`, reason codes, derived statuses | Yes | consume-only; preserve identity |
| OD-13/OD-14/OD-15/OD-16/OD-17 | §12 audit contract | audit findings | Yes | audit-only; no implementation |
| OD-18 | §2/§13 WS14 boundary | WS14 S2/S3/S5/S6 | Yes | no obligation transfer |
| OD-19 | §2/§13 WS13 protection | WS13 seams + tests | Yes | WS13 protected green |
| OD-20/OD-21 | §1/§13/§17 determinism; no auto-activation | — | Yes | no AI/network; no activation |
| SC-1/SC-3 | §3 input contract | exact seam shapes | Yes | shape/None behavior |

## 15. No-valid-RED path (OD-18/OD-21)

Owner Decisions → Increment Contract → Status Canonicalization → Bounded Defect
Search. If a valid observable defect exists: separate BASE RED authorization →
independent acceptance → separate GREEN authorization. If no valid defect
exists: No-Valid-RED evidence → independent verification → owner acceptance →
possible formal closure without implementation. No defect may be manufactured;
no GREEN without an accepted BASE RED. Note: because WS15 defines a new adapter
over currently-correct independent seams (SC-2/SC-4/SC-8), a valid observable
defect in an existing owned seam may not exist; the bounded defect search will
determine the path, and the §5 fixed-order contradiction check is a
stop-and-report condition, not a manufactured RED.

## 16. Status statement

```
OWNER DECISIONS:         COMMITTED AND INDEPENDENTLY ACCEPTED
INCREMENT CONTRACT:      OWNER APPROVED AND COMMITTED BY THIS ARTIFACT
WS15 IMPLEMENTATION:     NOT STARTED
STATUS CANONICALIZATION: NOT STARTED
DEFECT SEARCH:           NOT STARTED
BASE RED:                NOT STARTED
GREEN:                   NOT STARTED
```

WS15 is not started, implemented, or closed by this document. The next
authorized gate is a separately authorized WS15 Status Canonicalization.
`engine/adaptive_follow_up.py` remains absent; the WS13/WS14 absence guards
remain unchanged; Workstreams 9–14 remain FORMALLY CLOSED. WS16, WS17, D13,
Patent Export, WS-PFV-001, CAP-12/CAP-13/CAP-14, and the AI Coach remain
inactive, blocked, separately gated, or unauthorized. No automatic downstream
activation occurs.
