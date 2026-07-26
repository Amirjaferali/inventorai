# Workstream 14 — Adaptive Follow-Up and Completion Logic

## Increment Contract — Canonical Governance Document

This is the standalone, committed WS14 Increment Contract. It records the final
owner-approved policy and scope content. It is a governance artifact only: it
does **not** start WS14, does **not** perform Status Canonicalization, does
**not** begin bounded defect search / BASE RED / GREEN, and authorizes no
implementation. Repository truth overrides conversation, handover, memory,
inference, and proposal.

---

## 1. Contract status and purpose

- **Status:** OWNER APPROVED (policy and scope content). Not canonical status;
  not a Status Canonicalization; not an activation.
- **Purpose:** define the smallest canonical WS14 v1 increment required to
  implement or verify **deterministic post-answer decision logic**, in which a
  follow-up question is one possible bounded outcome, not the default. The
  contract does not assume implementation is required.

## 2. Authoritative base and dependency chain

| Item | Value |
|---|---|
| Repository | `Amirjaferali/inventorai` |
| Authoritative governance branch | `feature/atomic-json-session-persistence` |
| Program authoritative tip | `ddead62ddf9a54d9223a955e6c1cb97de52e1f65` (PR #278 merge) |
| Accepted WS14 Owner Decisions artifact | `docs/governance/WORKSTREAM_14_ADAPTIVE_FOLLOW_UP_AND_COMPLETION_LOGIC_OWNER_DECISIONS.md` |
| Accepted Owner Decisions commit | `4fd50018ee63d06c88c48e495d8a729517bb4092` (parent `ddead62`) |
| This contract's base commit | `4fd50018ee63d06c88c48e495d8a729517bb4092` |
| Reserved future module (absent) | `engine/adaptive_follow_up.py` (guarded absent by `tests/test_workstream_9_single_intent_question_design.py:301`) |

This contract is governed by, and must be read together with, the accepted
Owner Decisions OD-1 … OD-21 at commit `4fd50018`. Where this contract and the
Owner Decisions ever appear to diverge, the accepted Owner Decisions control.

Gate lifecycle (OD-18): Evidence Lock / Fresh Source Review → Owner Decisions →
**Increment Contract (this document)** → Status Canonicalization → Bounded
Defect Search → (valid observable defect, if any) → separately authorized BASE
RED → independent acceptance → separately authorized GREEN. If no valid
observable defect exists: no-valid-RED evidence path → owner review → possible
formal closure without implementation.

## 3. Scope and non-goals

**In scope:** deterministic `post_answer_action` selection; consumption of the
canonical inputs in §4; a structured deterministic reason (§7); the bounded
follow-up policy (§9); repetition prevention (§10); the unknown/deferred
lifecycle (§11); contradiction/supersession consumption (§12); criticality
consumption without ordering change (§13, Option B); derived progress/
remaining-item semantics (§15).

**Out of scope / non-goals:** production UI modification; frontend redesign;
WS15 guidance consolidation; Structured Technical Guidance / D13; research
topics and search terms; engineering instructions; material grades/thickness;
Patent Export; WS-PFV-001; CAP-12; CAP-13; CAP-14; AI Coach; CAD; simulation;
semantic answer verification; semantic expressed-intent detection; cross-session
persistence expansion; new independent remaining-item store; automatic gap
closure; automatic Workstream activation; invented blocking rules.

## 4. Canonical input contract

WS14 consumes, never reimplements. For each input: owner, symbol, read-only,
modification prohibited, and unavailable-behavior.

| Input | Owner | Symbol | Read-only | Modify prohibited | Unavailable → |
|---|---|---|---|---|---|
| Criticality (OD-9) | WS4 | `engine/idea_state.py` CRITICALITY categories | Yes | Yes | NO PRIORITY INVENTED |
| One-question-one-intent (OD-10) | WS9 | `tests/test_workstream_9_single_intent_question_design.py`; `primary_intent` | Yes | Yes | N/A (invariant) |
| `question_id`/`intent_id`/`design_gap_id`/`answer_objective`/`completion_condition` (OD-4/5/6/20) | WS10 | `engine/question_intent_registry.py` | Yes | Yes | typed input-error; no inference |
| Structural evaluation (OD-3) | WS11 | `engine/question_aware_evaluation.py` (`evaluate_question_intent`) | Yes | Yes | typed input-error |
| Technical verification (OD-3/13) | axis | `validation_status` | Yes | Yes | UNVALIDATED consumed as unverified; missing source → explicit unavailable/input-error |
| Controlled-unknown classification (OD-2/7) | WS12 | `engine/controlled_unknown_progression.py` (`classify_controlled_unknown`) | Yes | Yes | typed input-error; no fabricated path |
| Interaction dispositions (OD-2) | engine | `INTERACTION_DISPOSITIONS` | Yes | Yes | typed input-error |
| Contradiction/supersession (OD-8) | idea_state | `mark_contradiction`, `has_unresolved_contradiction`, `mark_supersession` | history read; append via existing API | second model prohibited | typed input-error |
| Session records (OD-16) | session persistence | existing session record | existing-write only | no new store | explicit failure; no silent write |
| `AssertionRecord`/`IterationLog`/`iterations_open` (OD-4/5/16) | ledgers/idea_state | append-only | append via existing API only | no second counter / schema change | typed input-error |
| State revision/sequence (OD-4/6) | idea_state | revision/sequence | Yes | Yes | typed input-error |
| Display ownership (OD-11) | WS13 | `web/*.py`; `web/app.py` | boundary only | WS14 must not modify | N/A |

No missing data is inferred (OD-15).

## 5. Output contract

Two separate concepts (OD-2).

**`post_answer_action`** — closed WS14-native set:
`ASK_FOLLOW_UP`, `NO_FOLLOW_UP`, `CONTINUE`, `CONTINUE_WITH_OPEN_ITEM`,
`RESOLVE_CONTRADICTION`, `BLOCK_PROGRESSION`, `BLOCK_FINAL_COMPLETION`.

**`controlled_unknown_classification`** — the existing WS12 classification when
applicable. `OUT_OF_SCOPE` remains a WS12 classification, **not** a
`post_answer_action`. No duplicate `REQUIRE_*` vocabulary; no implicit mapping
between the separate WS12 vocabularies.

Proposed output record (`PROPOSED — AWAITING OWNER REVIEW` for exact field
implementation): required `post_answer_action`; structured reason (§7); optional
`controlled_unknown_classification`; optional existing disposition. Output is
**derived**, not persisted (OD-16).

## 6. Separation of concepts

The following remain logically separate (OD-3/OD-13); reuse existing
representations; no new persisted enums/fields/axes/schemas merely to express
separation:

- **post-answer action** (WS14-native decision);
- **WS12 controlled-unknown classification** (consumed);
- **answer capture**;
- **conversational sufficiency**;
- **progression permission**;
- **technical verification** (`validation_status`, read-only).

Progression permission is independent from item-open state, completion state,
and technical verification. **`CONTINUE` (and every action) never automatically
means COMPLETE, closed, resolved, or verified**; item-open and completion state
remain independently derived from canonical records. Technical verification is
never created, inferred, promoted, or modified by WS14 from answer quality,
conversational sufficiency, or progression permission. An existing
`validation_status = UNVALIDATED` is consumed as technically unverified; a
missing/unreadable validation-status source yields an explicit unavailable/
input-error and is never silently replaced with `UNVALIDATED`.

## 7. Structured deterministic reason; replay and determinism

Structured derived reason (OD-4):

- `decision_reason_code` — deterministic and bounded;
- `decision_reason_refs` — pointers to canonical records
  (`question_id`/`intent_id`/`design_gap_id`/`completion_condition`/
  `ServedQuestion`/`AssertionRecord`/`IterationLog`/state-revision);
- `rendered_reason` — optional, derived presentation only.

Arabic/English rendering must not change decision identity; no field becomes a
separate persisted source of truth; no parallel provenance store. The exact
`decision_reason_code` taxonomy is a source-confirmation obligation (§17) unless
already source-backed.

Replay/determinism (OD-15): *same canonical input state → same
`post_answer_action` → same `decision_reason_code` → same refs*, unless a
documented material canonical state change occurred. WS14 v1 has no AI, no LLM
semantic inference, no embeddings, no network, no hidden fallback, no random
selection, no text-derived identity, no silent technical verification, and no
automatic gap closure.

**Input-error contract:** contract-level input failure must use an existing
typed error boundary or an explicit deterministic decision-input error result.
It must not become an uncontrolled crash, a silent fallback, or a normal
`post_answer_action`. The exact implementation error type is not invented here
(source-confirmation obligation §17).

## 8. Blocking discipline

`BLOCK_PROGRESSION`, `BLOCK_FINAL_COMPLETION`, and `RESOLVE_CONTRADICTION` may be
emitted **only when an existing canonical rule or trusted source requires that
result** (OD-8/OD-9). **WS14 does not invent a blocking rule.** A contradiction
does not automatically block progression or final completion in every case.

## 9. Follow-up bound (OD-5)

- Counting unit: `completion_condition` (WS10-owned, consumed).
- Maximum: two follow-up questions after the original question for the same
  unresolved completion condition.
- **Valid reset conditions:** a material canonical state change; an explicit
  supersession; activation of a genuinely different completion condition.
- Prohibited: a second independent counter when existing accounting suffices;
  `maturity_level` as a follow-up counter or limit; a third follow-up for the
  same unresolved completion condition without a valid reset.
- At the maximum: `post_answer_action = NO_FOLLOW_UP` with the appropriate
  existing disposition or WS12 classification and, where permitted,
  `CONTINUE_WITH_OPEN_ITEM`. Reaching the maximum alone does not automatically
  block final completion.

## 10. Repetition prevention (OD-6)

Do not repeat the same unresolved completion condition without a relevant
canonical state change. A different detail under the same intent may be
requested only when it has a different canonical completion condition. No text
equality, fuzzy matching, semantic similarity, embeddings, AI/LLM inference, or
network dependency.

## 11. Unknown and deferred lifecycle (OD-7/OD-16)

Preserve WS12 observation-only. UNKNOWN/DEFERRED/NEEDS_* remain open unless
existing canonical rules say otherwise. UNKNOWN is neither COMPLETE nor
automatic failure; UNKNOWN does not automatically trigger a follow-up; no
automatic immediate revisit. Revisit only on explicit user request, selection
from the derived open-item state, or an existing blocking rule before final
completion. Persistence, revisit, and completion effects are new WS14 policy
choices, not inherited from WS12. Reuse existing canonical session records and
append-only ledgers; no new independent store; persistence beyond the current
canonical session mechanism is not approved; any cross-session artifact requires
separate justification (schema, migration, recovery, atomicity, protected
regression, side-effect boundaries).

## 12. Contradiction and supersession boundaries (OD-8)

Consume `mark_contradiction`, `has_unresolved_contradiction`, `mark_supersession`;
no second contradiction model; preserve append-only history. Distinguish an
incompatible active assertion from an explicit replacement/answer change. At
most one targeted clarification question per unresolved contradiction unless a
material canonical state change occurs. Blocking only where an existing trusted
rule requires (§8). No semantic/fuzzy/AI/LLM/embedding/network detection.

## 13. Criticality — Option B (OD-9)

**WS14 consumes trusted criticality metadata but does not alter follow-up or
open-item ordering in v1.** WS14 may consume FEASIBILITY-THREATENING,
VALUE-ENHANCING, REFINEMENT for decision context, provenance, and consumption of
an existing blocking rule. WS14 must not modify `select_next_gap`; must not
reorder questions or open items based on criticality; must not create a priority
algorithm; must not infer missing priority; must not create
CRITICAL/IMPORTANT/OPTIONAL; must not claim criticality ordering is implemented.
The existing deterministic ordering is preserved unchanged. A
feasibility-threatening item may block final completion only when an existing
canonical rule requires it. If a later bounded defect search proves the absence
of criticality-based ordering is a valid observable WS14 defect, that requires
separate owner review → valid BASE RED authorization → independent acceptance →
separate GREEN authorization. No ordering defect may be assumed or manufactured.

## 14. WS8 expressed-intent limitation (OD-20, Option b)

WS14 v1 consumes WS10 design-time intent identity only. It must not claim that
design-time identity equals user-expressed intent. User-expressed-intent capture
remains a RECORDED LIMITATION, a DEFERRED CAPABILITY, and NOT COMPLETED BY WS14.
No semantic/fuzzy/LLM expressed-intent inference. Traceability to the WS8
deferral (`WORKSTREAM_8_NO_VALID_RED_DISPOSITION_AND_FORMAL_CLOSURE.md`) is
preserved.

## 15. Derived progress and remaining-item semantics (OD-12)

Any progress or remaining-item result is derived from canonical records,
deterministic, rebuildable, and non-authoritative as an independent store; it
must never silently omit an open item, and must preserve unknown, deferred,
test, measurement, specialist, contradiction, blocked, and open-item semantics
where applicable. If derivation data is incomplete, return an explicit
`INCOMPLETE` or `UNAVAILABLE` result rather than guessing; these are statuses of
the derived result only — not `post_answer_action` values, completion states,
WS12 classifications, or technical-verification statuses. WS14 may define
semantic derivation only; presentation ownership remains
**PROVISIONAL — PENDING WS15 CANONICAL CONTRACT**.

## 16. Failure modes, persistence, side-effect, migration, recovery

**Failure-mode table:**

| Failure mode | Trigger | Required behavior |
|---|---|---|
| Missing canonical id | absent `question_id`/`completion_condition` | typed input-error via existing boundary; no inference |
| Absent WS12 classification | classification unavailable | typed input-error; no fabricated path |
| `validation_status = UNVALIDATED` | existing value | consume as technically unverified |
| Validation-status source missing/unreadable | source unavailable | explicit unavailable/input-error; never substitute UNVALIDATED |
| Incomplete derivation data | remaining-map source incomplete | explicit `INCOMPLETE`/`UNAVAILABLE` (derived-map status only) |
| Follow-up max reached | 2 follow-ups, same condition | `NO_FOLLOW_UP` (+ disposition/classification; `CONTINUE_WITH_OPEN_ITEM` where allowed) |
| Unresolved contradiction with existing rule | `has_unresolved_contradiction` true + rule requires | `RESOLVE_CONTRADICTION`; one clarification max |
| No trusted criticality | metadata absent | no invented priority |
| Contract-level input failure | any invalid input | existing typed error boundary or explicit deterministic decision-input error; never a normal action |

**Persistence and side-effect boundary (OD-16):** reuse existing canonical
records and append-only ledgers; no new independent store; read canonical
records; append only via existing ledger APIs; no new file/store/network/UI
write.

**Migration impact:** none currently authorized; subject to bounded-defect-
search confirmation. **Recovery impact:** no new impact currently authorized;
reassess if existing accounting cannot represent the approved follow-up bound.

**Security & privacy impact:** no new persistence, no network, no external
egress; in-memory/derived only.

## 17. Source-confirmation obligations (later bounded defect search)

Not open Owner Decisions; must not be resolved by assumption in this artifact:

1. machine-consumable blocking-rule seam for `BLOCK_PROGRESSION`,
   `BLOCK_FINAL_COMPLETION`, and contradiction-driven blocking;
2. derivability of the per-`completion_condition` follow-up count from existing
   `IterationLog` / `iterations_open` without a new counter;
3. source-established effects of `OUT_OF_SCOPE`;
4. existing typed input-error boundary;
5. exact bounded `decision_reason_code` taxonomy;
6. provisional WS14/WS15 presentation boundary.

## 18. Binding UX/UI scope constraint (OD-21) — OWNER-DIRECTED BINDING SCOPE CONSTRAINT

```
أثناء WS14: تُراعى قيود تجربة المستخدم فقط داخل القرارات والعقود، دون إعادة تصميم أو تعديل واجهة الإنتاج.
```

WS14 may consider UX/UI only as usability, explainability, non-technical-user
clarity, RTL implications, and presentation implications. WS14 must not modify
or authorize production frontend, production UI, redesign, screen layout, visual
design, button copy, or production interaction design. The WS14/WS15
presentation boundary remains **PROVISIONAL — PENDING WS15 CANONICAL CONTRACT**.

## 19. Testing contract (future required tests — none created/run by this artifact)

Identical-input replay; follow-up count 0/1/2; third follow-up prohibited; valid
reset after canonical state change; no reset without state change; same intent
with different completion condition (allowed); same completion condition
repetition prohibited; UNKNOWN does not complete; UNKNOWN does not auto-follow-up;
deferred item remains open; no automatic revisit; WS12 classification preserved;
no duplicate unknown vocabulary; `validation_status` read-only; UNVALIDATED vs
missing-source distinction; `CONTINUE` does not imply completion/closure/
verification; blocking actions only under an existing rule; contradiction
clarification max one; supersession preserves history; no invented priority; no
new store; derived remaining-map rebuildability; incomplete derivation returns
explicit `INCOMPLETE`/`UNAVAILABLE`; derived-map statuses are not
actions/classifications; no AI/network/LLM/fuzzy path.

**Protected regression:** WS9 single-intent, WS10 registry, WS11 evaluation, and
WS12 controlled-unknown protected suites remain green; WS13 display-layer tests
remain green; the WS13/WS14 absence guard
(`tests/test_workstream_9_single_intent_question_design.py:301`) remains
unchanged before activation. Tests are not created, edited, or run by this
artifact.

## 20. OD-1 … OD-21 traceability

| OD | Contract clause | Consumed source | Modify prohibited? |
|---|---|---|---|
| OD-1 | §1, §5 | post-answer path | Yes |
| OD-2 | §5, §8 | `classify_controlled_unknown`; `INTERACTION_DISPOSITIONS` | Yes |
| OD-3 | §6 | `validation_status`; `assess_response` | Yes |
| OD-4 | §7 | WS10 ids; `AssertionRecord`; `IterationLog` | Yes |
| OD-5 | §9 | `completion_condition`; `IterationLog`/`iterations_open` | Yes |
| OD-6 | §10 | `completion_condition`; `mark_supersession` | Yes |
| OD-7 | §11 | WS12; dispositions | Yes |
| OD-8 | §8, §12 | contradiction primitives | Yes |
| OD-9 | §13 | CRITICALITY categories; `select_next_gap` | Yes |
| OD-10 | §4, §19 | WS9 `:301`; `primary_intent` | Yes |
| OD-11 | §15, §18 | WS13 seams | Yes |
| OD-12 | §15 | gap set; `select_next_gap` | Yes |
| OD-13 | §6 | `evaluate_transition`; `validation_status` | Yes |
| OD-14 | §5 | post-answer path | Yes |
| OD-15 | §7 | `ai_advisor` (off) | Yes |
| OD-16 | §11, §16 | ledgers; session record | Yes |
| OD-17 | §21 | roadmap; `:301` guard | Yes |
| OD-18 | §2, §21 | WS8/WS13 precedent | Yes |
| OD-19 | §21 | prior-gate governance | Yes |
| OD-20 | §14 | WS10 identity; WS8 doc | Yes |
| OD-21 | §18 | governance scope | Yes |

## 21. No-valid-RED path and stop conditions

**No-valid-RED path (OD-18):** Owner Decisions → Increment Contract → Status
Canonicalization → Bounded Defect Search → (valid observable defect, if any) →
separately authorized BASE RED → independent acceptance → separately authorized
GREEN. If none: no-valid-RED evidence path → owner review → possible formal
closure without implementation. No RED manufactured; no GREEN without an
accepted BASE RED.

**Stop conditions:** this artifact records the Increment Contract only. It does
not perform Status Canonicalization, does not change the §15 status row, does
not begin defect search / BASE RED / GREEN, and does not create
`engine/adaptive_follow_up.py`. WS14 remains NOT STARTED; the WS13/WS14 absence
guards remain unchanged. WS15, WS16, WS17, D13, Patent Export, WS-PFV-001, and
CAP-12/CAP-13/CAP-14 remain inactive, blocked, separately gated, or unauthorized;
no automatic downstream activation occurs. The next authorized gate is Status
Canonicalization, which is not authorized by this artifact.
