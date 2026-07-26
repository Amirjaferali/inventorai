# Workstream 14 — Adaptive Follow-Up and Completion Logic

## Owner Decisions — Canonical Governance Document

This is the standalone, committed record of the owner-accepted WS14 Owner
Decisions (OD-1 … OD-21). It is a governance artifact only. It does **not**
start WS14, does not perform Status Canonicalization, does not create the
Increment Contract artifact, and authorizes no implementation.

Repository truth overrides conversation, handover, memory, inference, and
proposal.

---

## 1. Workstream identity and scope

- **Workstream:** 14 — Adaptive Follow-Up and Completion Logic (canonical name;
  not renamed).
- **Operating definition (OD-1):** WS14 is deterministic post-answer decision
  logic. It determines what should happen after a user response. A follow-up
  question is one possible bounded outcome, not the default or mandatory
  outcome. WS14 must not become an engine that asks another question whenever
  information is incomplete.
- **Scope posture:** WS14 v1 **consumes, never reimplements**, the closed
  outputs of WS4 and WS8–WS13 and the existing engine primitives; it introduces
  no new persistence, no new vocabulary, no AI/network/fuzzy behavior, and no
  automatic downstream activation.

## 2. Authoritative base

| Item | Value |
|---|---|
| Repository | `Amirjaferali/inventorai` |
| Authoritative governance branch | `feature/atomic-json-session-persistence` |
| Authoritative base tip | `ddead62ddf9a54d9223a955e6c1cb97de52e1f65` (PR #278 merge) |
| WS14 status at this base | NOT STARTED |
| Committed WS14 Owner Decisions at this base | none (this document is the first) |
| Committed WS14 Increment Contract at this base | none (separate later gate) |
| `engine/adaptive_follow_up.py` at this base | absent |

The WS9–WS13 closure records at this base are historical and are not altered by
this document.

## 3. Final classification counts

- **17 OWNER APPROVED:** OD-1, OD-2, OD-3, OD-4, OD-5, OD-6, OD-7, OD-8, OD-9,
  OD-11, OD-12, OD-13, OD-14, OD-15, OD-16, OD-18, OD-20.
- **3 PRESERVED CANONICAL INVARIANTS:** OD-10, OD-17, OD-19.
- **1 OWNER-DIRECTED BINDING SCOPE CONSTRAINT:** OD-21.
- Total: 21 decisions, all resolved.

OD-11 and OD-12 are OWNER APPROVED for their WS14 portions; their presentation
halves remain **PROVISIONAL — PENDING WS15 CANONICAL CONTRACT**.

---

## 4. Owner Decisions OD-1 … OD-21

### OD-1 — Operating definition — OWNER APPROVED
WS14 v1 is deterministic post-answer decision logic; a follow-up is one bounded
outcome, not the default or mandatory outcome. WS14 must not ask another
question merely because information is incomplete.

### OD-2 — Post-answer action vs controlled-unknown classification — OWNER APPROVED
Model two separate concepts.

`post_answer_action` (WS14-native closed set):
`ASK_FOLLOW_UP`, `NO_FOLLOW_UP`, `CONTINUE`, `CONTINUE_WITH_OPEN_ITEM`,
`RESOLVE_CONTRADICTION`, `BLOCK_PROGRESSION`, `BLOCK_FINAL_COMPLETION`.

`controlled_unknown_classification`: consume the existing WS12 classification
when applicable. Do not create duplicate `REQUIRE_*` vocabulary. Do not create
an implicit mapping between the separate WS12 vocabularies (the six WS12 path
classifications versus the six `INTERACTION_DISPOSITIONS`). WS14 outcomes that
correspond to a controlled unknown (`RECORD_UNKNOWN`, `DEFER`,
`REQUIRE_EVIDENCE`, `REQUIRE_MEASUREMENT`, `REQUIRE_TEST`, `REQUIRE_SPECIALIST`,
`OUT_OF_SCOPE`) consume/map explicitly and 1:1 to an existing WS12 concept.
`OUT_OF_SCOPE` remains a WS12 classification, not a `post_answer_action`.

### OD-3 — Four-axis separation — OWNER APPROVED
Keep answer capture, conversational sufficiency, progression permission, and
technical verification logically separate. Reuse existing representations; do
not create new persisted enums, fields, axes, or schemas merely to make the
separation explicit. Technical verification is read from the existing
`validation_status` axis and is never created, inferred, promoted, or modified
by WS14 based on answer quality, conversational sufficiency, or progression
permission. Distinguish an existing `UNVALIDATED` value (consumed as
technically unverified) from a missing/unreadable validation-status source
(explicit unavailable/input-error, never silently substituted with
`UNVALIDATED`).

### OD-4 — Decision reason and provenance — OWNER APPROVED
Every post-answer decision must be explainable and reproducible from canonical
records. Distinguish "why the question or requirement exists" from "why the
current post-answer action was selected now." Consume existing canonical
identifiers, history, ledgers, and state revision. Do not create a parallel
provenance store. The structured reason is `decision_reason_code` (deterministic,
bounded), `decision_reason_refs` (pointers to canonical records), and an optional
`rendered_reason` (derived presentation only); Arabic/English rendering must not
change decision identity; none becomes a second source of truth.

### OD-5 — Follow-up counting and bound — OWNER APPROVED
Counting unit: `completion_condition` (owned by WS10, consumed by WS14).
Maximum: two follow-up questions after the original question for the same
unresolved completion condition. Reset only after a material canonical state
change, an explicit supersession, or activation of a genuinely different
completion condition. Do not create a second independent counter when existing
iteration accounting and history are sufficient; do not use `maturity_level` as
a follow-up counter or limit; do not allow a third follow-up for the same
unresolved completion condition without a valid reset. At the maximum, another
follow-up is prohibited; the controlled result is `NO_FOLLOW_UP` combined with
the appropriate existing disposition or WS12 classification and, where allowed,
`CONTINUE_WITH_OPEN_ITEM`. Reaching the maximum alone must not automatically
block final completion; final completion is blocked only when an existing
trusted blocking rule requires it.

### OD-6 — Repetition prevention — OWNER APPROVED
Do not repeat the same unresolved completion condition without a relevant
canonical state change. A different detail under the same intent may be
requested only when it has a different canonical completion condition. No text
equality, fuzzy matching, semantic matching, embeddings, LLM inference, or
network dependency is authorized.

### OD-7 — Unknown and deferred behavior — OWNER APPROVED
UNKNOWN, DEFERRED, and NEEDS_* remain open states unless their existing
canonical rules say otherwise. UNKNOWN is neither COMPLETE nor automatic
failure; UNKNOWN does not automatically trigger another follow-up; there is no
automatic immediate revisit. Revisit occurs only when the user explicitly
requests it, the item is selected from the derived open-item state, or an
existing blocking rule requires resolution before final completion. Preserve
WS12 as observation-only; persistence, revisit, and completion effects are new
WS14 policy choices and are not inherited from WS12. Reuse existing canonical
session records and append-only ledgers; no new independent state store;
persistence beyond the current canonical session mechanism is not approved here.

### OD-8 — Contradiction and supersession — OWNER APPROVED
WS14 consumes `mark_contradiction`, `has_unresolved_contradiction`, and
`mark_supersession`. Do not create a second contradiction model; preserve
append-only history. Distinguish an incompatible active assertion from an
explicit replacement or change of answer. At most one targeted clarification
question may be produced for the same unresolved contradiction unless a material
canonical state change occurs. Progression or final completion is blocked only
where an existing trusted rule requires resolution. No semantic, fuzzy, AI, LLM,
embedding, or network-based contradiction detection is authorized.

### OD-9 — Criticality and priority — OWNER APPROVED (Option B)
WS14 consumes the existing owner-confirmed categories FEASIBILITY-THREATENING,
VALUE-ENHANCING, REFINEMENT for deterministic decision context, explanation and
provenance, consuming an existing canonical blocking rule where one exists, and
identifying that trusted criticality metadata is present. **Option B:** WS14
consumes trusted criticality metadata but does not alter follow-up or open-item
ordering in v1. WS14 must not reorder questions or open items based on
criticality, must not modify `select_next_gap`, must not create a new priority
algorithm, must not infer priority when trusted metadata is absent, must not
create CRITICAL/IMPORTANT/OPTIONAL, and must not claim that criticality-based
ordering is already implemented. The existing deterministic ordering is
preserved unchanged. A feasibility-threatening item may block final completion
only when an existing canonical rule requires it. If a later bounded defect
search proves that the absence of criticality-based ordering is a valid
observable WS14 defect, that finding requires separate owner review → valid BASE
RED authorization → independent acceptance → separate GREEN authorization. No
ordering defect may be assumed or manufactured.

### OD-10 — One question, one intent — PRESERVED CANONICAL INVARIANT
One primary intent, one requested user action, one completion condition. A
follow-up must not request multiple independently answerable facts. WS14
consumes and protects the existing WS9 invariant and must not reimplement,
weaken, or reinterpret it.

### OD-11 — Engine and display boundary — OWNER APPROVED (WS14/WS15 half provisional)
WS14 owns semantic post-answer decisions; WS13 owns its existing display
guidance surfaces. WS14 may determine that clarification or reframe is required;
WS14 does not own production wording, layout, buttons, examples, or visual
treatment. The WS14/WS15 presentation boundary remains
**PROVISIONAL — PENDING WS15 CANONICAL CONTRACT**. Candidate WS15 concerns are
not converted into canonical WS15 scope. `_STALL_REFRAME` must not be overstated
as a complete progressive-simplification system.

### OD-12 — Progress and remaining-item derivation — OWNER APPROVED (presentation provisional)
Any progress or remaining-item representation must be derived from canonical
records, deterministically rebuildable, and never an independently authoritative
state store; it must preserve unknown, deferred, test, measurement, specialist,
contradiction, blocked, and open-item semantics where applicable, and must never
silently omit an item. If canonical derivation data is incomplete, return an
explicit `INCOMPLETE` or `UNAVAILABLE` result rather than guessing; these are
statuses of the derived result only, not `post_answer_action` values, completion
states, WS12 classifications, or technical-verification statuses. WS14 may own
semantic derivation; presentation ownership remains
**PROVISIONAL — PENDING WS15 CANONICAL CONTRACT**.

### OD-13 — Completion model (separate axes) — OWNER APPROVED
Preserve separate axes; reuse existing representations where sufficient; no new
schema merely to express separation. Proposed axes for later contract:
Completion {OPEN, PARTIAL, COMPLETE}; Disposition {ACTIVE, UNKNOWN, DEFERRED,
OUT_OF_SCOPE}; Progression {ALLOWED, ALLOWED_WITH_OPEN_ITEM, BLOCKED}; Technical
verification = the existing `validation_status` axis, read-only. No single
overloaded enum. `CONTINUE` (and every action) expresses progression permission
only and never implies the item is closed, the completion condition is
satisfied, the item is removed from the open-item set, or that technical
verification is complete — these remain independently derived.

### OD-14 — NO_FOLLOW_UP is a valid result — OWNER APPROVED
`NO_FOLLOW_UP` is a valid deterministic result. It must not be interpreted as
COMPLETE, technically verified, resolved, removal of an open item, or permission
to discard an unresolved risk. It may be combined with an existing WS12
classification, disposition, or `CONTINUE_WITH_OPEN_ITEM` per the approved rules.

### OD-15 — Determinism and replay — OWNER APPROVED
Require: same canonical input state → same post-answer action → same reason,
unless a documented material canonical state change occurred. WS14 v1 must have
no AI, no LLM semantic inference, no embeddings, no network dependency, no hidden
fallback, no random selection, no text-derived identity, no silent technical
verification, and no automatic gap closure.

### OD-16 — Persistence boundary — OWNER APPROVED
Default: reuse existing canonical records and append-only ledgers
(`AssertionRecord`, `IterationLog`, existing session records); no new
independent state store. Persistence beyond what the current canonical session
mechanism already supports is not approved here. Any new cross-session
persistence artifact requires separate justification covering schema, migration,
recovery, atomicity, protected regression, and side-effect boundaries.

### OD-17 — No automatic activation — PRESERVED CANONICAL INVARIANT
WS14 completion does not activate WS15. No Workstream, capability, export, D13,
Patent Export, WS-PFV-001, CAP-12, CAP-13, CAP-14, or AI Coach activates
automatically. No owner decision may weaken this rule.

### OD-18 — No-valid-RED path — OWNER APPROVED
Authorized sequence: Owner Decisions → Increment Contract → Status
Canonicalization → Bounded Defect Search. If a valid observable defect is found:
→ separately authorized BASE RED → independent acceptance → separately
authorized GREEN. If no valid observable defect is found: → no-valid-RED
evidence path → owner review → possible formal closure without implementation.
No defect may be manufactured. No GREEN may begin without an accepted BASE RED.

### OD-19 — Acceleration and evidence governance — PRESERVED CANONICAL INVARIANT
One unified preflight per gate; avoid repetitive checks; parallelize independent
inspections; focused/protected tests before full-suite runs; full suite only at
decisive gates; smallest necessary diff; separate executor and independent
reviewer; one final bundle after the head stabilizes; no jump to GREEN before
BASE RED acceptance; no reduction of evidence quality for speed.

### OD-20 — WS8 expressed-intent limitation — OWNER APPROVED (Option b)
WS14 v1 consumes WS10 design-time intent identity only. It must not claim that
design-time intent identity equals the user's expressed intent. User-expressed-
intent capture remains a RECORDED LIMITATION, a DEFERRED CAPABILITY, and NOT
COMPLETED BY WS14. No semantic, fuzzy, or LLM-based expressed-intent inference
is authorized. Traceability to the WS8 deferral
(`WORKSTREAM_8_NO_VALID_RED_DISPOSITION_AND_FORMAL_CLOSURE.md`, expressed-intent
objectives deferred to WS9/10/11/14) is preserved so the deferred output is not
orphaned.

### OD-21 — Binding WS14 UX/UI scope constraint — OWNER-DIRECTED BINDING SCOPE CONSTRAINT

```
أثناء WS14: تُراعى قيود تجربة المستخدم فقط داخل القرارات والعقود، دون إعادة تصميم أو تعديل واجهة الإنتاج.
```

Operational meaning: WS14 may consider usability, explainability,
non-technical-user clarity, RTL implications, and presentation consequences as
constraints only. WS14 must not authorize or implement frontend changes,
production UI changes, redesign, screen-layout changes, visual-design changes,
button-copy changes, or production interaction-design changes. Any UX/UI
implementation requires its proper later gate and separate owner authorization.

---

## 5. Follow-up limit policy (consolidated, from OD-5)

- Counting unit: `completion_condition` (WS10-owned, consumed).
- Maximum: two follow-ups after the original question for the same unresolved
  completion condition.
- Reset: only after a material canonical state change, explicit supersession, or
  a genuinely different completion condition.
- Prohibited: a second counter when existing accounting suffices; `maturity_level`
  as a limit; a third follow-up without a valid reset.
- At the maximum: `NO_FOLLOW_UP` (+ existing disposition / WS12 classification;
  `CONTINUE_WITH_OPEN_ITEM` where allowed); no automatic final-completion block.

## 6. Preserved invariants and prohibitions

- No automatic downstream activation (OD-17).
- No AI, LLM, embeddings, network, fuzzy matching, or semantic inference
  (OD-15).
- No automatic gap closure; no automatic technical verification (OD-15).
- No duplicate WS12 vocabulary; no implicit mapping between WS12 vocabularies
  (OD-2).
- No new independent store; reuse existing canonical records and append-only
  ledgers (OD-16).
- WS9 one-question-one-intent preserved (OD-10).
- No invented blocking rule; blocking/contradiction actions consume existing
  canonical rules only (OD-8, OD-9).
- Criticality Option B: consumed but ordering unchanged (OD-9).

## 7. WS8 expressed-intent limitation (from OD-20)

WS14 consumes WS10 design-time intent identity only. User-expressed-intent
capture remains a RECORDED LIMITATION, a DEFERRED CAPABILITY, and NOT COMPLETED
BY WS14. No semantic/fuzzy/LLM intent inference. WS8 deferral traceability is
preserved.

## 8. No-valid-RED path (from OD-18)

Owner Decisions → Increment Contract → Status Canonicalization → Bounded Defect
Search → (valid observable defect, if any) → separately authorized BASE RED →
independent acceptance → separately authorized GREEN. If none: no-valid-RED
evidence path → owner review → possible formal closure without implementation.
No RED manufactured; no GREEN without an accepted BASE RED.

## 9. Source-confirmation obligations (for the later bounded defect search)

These are not open Owner Decisions and must not be resolved by assumption:

1. machine-consumable blocking-rule seam for `BLOCK_PROGRESSION`,
   `BLOCK_FINAL_COMPLETION`, and contradiction-driven blocking;
2. follow-up accounting derivability from existing `IterationLog` /
   `iterations_open` without a new counter;
3. source-established `OUT_OF_SCOPE` effects;
4. existing typed input-error boundary;
5. bounded deterministic `decision_reason_code` taxonomy;
6. provisional WS14/WS15 presentation boundary (resolved only when the WS15
   canonical contract exists).

## 10. Repository traceability (owner-confirmed source anchors)

| OD | Consumed source (authoritative tip `ddead62`) | Owner |
|---|---|---|
| OD-2 | `engine/controlled_unknown_progression.py` (`classify_controlled_unknown`); `INTERACTION_DISPOSITIONS` | WS12 |
| OD-3 / OD-13 | `validation_status`; `engine/progression_loop.py` (`assess_response`, `evaluate_transition`) | WS11 / engine |
| OD-4 | `engine/question_intent_registry.py` (`question_id`, `intent_id`, `design_gap_id`, `answer_objective`, `completion_condition`); `AssertionRecord`; `IterationLog` | WS10 / ledgers |
| OD-5 / OD-6 | `completion_condition`; `engine/idea_state.py` (`iterations_open`, `IterationLog`, `mark_supersession`) | WS10 / idea_state |
| OD-8 | `engine/idea_state.py` (`mark_contradiction`, `has_unresolved_contradiction`, `mark_supersession`) | idea_state |
| OD-9 | `engine/idea_state.py` CRITICALITY categories; `engine/progression_loop.py` (`select_next_gap`) | WS4 / engine |
| OD-10 | `tests/test_workstream_9_single_intent_question_design.py`; `primary_intent` | WS9 |
| OD-11 | WS13 display seams (`web/answer_coauthoring_prompts.py`, `web/scaffolding_guidance.py`, `web/uncertainty_guidance.py`, `web/clarification_labels.py`, `web/result_feedback.py`); `web/app.py` | WS13 |
| OD-12 | gap set; `engine/progression_loop.py` (`select_next_gap`) | engine |
| OD-16 | `AssertionRecord`; `IterationLog`; existing session persistence | ledgers / session |
| OD-17 | `ACTIVE_EXECUTION_ROADMAP.md` stop conditions; WS13/WS14 absence guard | governance |
| OD-20 | WS10 design-time identity; `WORKSTREAM_8_NO_VALID_RED_DISPOSITION_AND_FORMAL_CLOSURE.md` | WS10 / WS8 |

## 11. Approval and stop conditions

- WS14 Owner Decisions gate (Gate 14-B): COMPLETE — all 21 decisions resolved.
- This document records those decisions as a committed governance artifact. It
  does **not** start WS14, does **not** perform Status Canonicalization, and does
  **not** create the Increment Contract artifact.
- The WS14 Increment Contract must be committed as its own separate governance
  artifact in a separately authorized gate before any §15 status row records the
  Increment Contract as approved.
- WS14 remains NOT STARTED; `engine/adaptive_follow_up.py` remains absent; the
  WS13/WS14 absence guards remain unchanged.
- WS15, WS16, WS17, D13 (Structured Technical Guidance), Patent Export,
  WS-PFV-001, and CAP-12/CAP-13/CAP-14 remain inactive, blocked, separately
  gated, or unauthorized. No automatic downstream activation occurs.
