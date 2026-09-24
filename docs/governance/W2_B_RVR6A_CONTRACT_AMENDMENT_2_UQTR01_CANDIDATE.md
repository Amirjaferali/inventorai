# W2-B / RVR-6a — Contract Amendment 2 (UQTR-01 serving suppression) — CANDIDATE

**Status:** CANDIDATE, delivered with the UQTR-01 CORE SUCCESSOR CANDIDATE 02 commit, which
REPLACES Candidate 01 (`0166fbda5240fe7ccef9fcd987ac760d00f83f1f`, tree `20eb9aae…`, reviewed
patch SHA-256 `1ec4bdfe…20dc3`). Candidate 01 stays immutable reviewed evidence and is NOT an
ancestor of Candidate 02; Candidate 02 is one commit whose sole parent is the base below. This
document authorizes nothing by itself and joins the authoritative W2-B contract lineage only
through Owner acceptance of the exact Candidate 02 and its merge. It is ADDITIVE: the base contract
(`W2_B_RVR6A_IMPLEMENTATION_CONTRACT_CANDIDATE.md`, PR #573) and Amendment 1
(`W2_B_RVR6A_CONTRACT_AMENDMENT_1_CANDIDATE.md`, PR #575) remain in force unchanged, and no
historical W2-B, W2-C or Wave-1 document is edited.

**Authorizing instructions:** Owner authorization "UQTR-01 CORE IMPLEMENTATION CANDIDATE 01";
Owner authorization "UQTR-01 CORE REVIEW CORRECTION — SUCCESSOR CANDIDATE 02" (Lead review:
core architecture ACCEPTED as the correction basis; one bounded UX/composition correction).
**Base:** `e3d758995a2fd17dccddb4e4ba8b530bd7746649` (tree `3b27e5d63380485fce58141ed08af2a037df7a6e`).

## 1. Serving-only non-answer suppression (additive serving consequence)

A second pure serving rule, `engine.progression_loop.compute_non_answer_suppression(state)`, is
composed BESIDE `compute_serving_decision` at the same single render surface (`show_session`).

- **It is not a fifth trigger.** The four trigger classes of Amendment 1 §5 and
  `W2B_TRIGGERS` are unchanged; `ServingDecision` is unchanged; no served text is replaced.
- **Rule.** For the gap `select_next_gap(state)` selects (the one canonical selector, never
  overridden), read ACTIVE ledger records (`superseded_by is None`) in durable order whose
  `gap_context` is that gap and whose disposition is one of the six owner interaction actions.
  If the latest is `unknown`, `deferred`, `provisional_assumption`, `specialist_requested` or
  `evidence_requested`, the automatic re-ask of that question is suppressed. A later active
  `answered` record for the same gap (or no applicable record) restores ordinary serving.
  Superseded records never decide.
- **Pure derivation.** A function of the durable, restored ledger only: no clock, render
  counter, retry count, transient session memory, randomness, model call or persisted serving
  state. Live, cold-reconstructed and writable-resumed states therefore derive the same result.
- **Serving only (question suppression is not gap resolution).** It never changes gap status,
  `iterations_open`, maturity, `current_stage`, evidence quality, validation, accepted risk,
  completion, deliverable eligibility or derived readiness, and no canonical engine path
  (`run_iteration`, `advance_after_disposition`, reconstruction/replay) consults it.
- **Language-neutral.** The rule reads only canonical state (disposition, `gap_context`,
  `superseded_by`, the canonical selected gap). No displayed or translated text, UI language,
  localized label or Arabic/English vocabulary takes part; EN and AR presentations of the same
  durable state derive the same decision. Localization stays a rendering concern.

## 1A. W2-B × UQTR composition (binding)

- `compute_non_answer_suppression` governs automatic QUESTION-SLOT solicitation for the
  canonical selected gap; `compute_serving_decision` keeps every W2-B consequence. UQTR never
  mutates, removes or fabricates W2-B triggers and never changes `ServingDecision`.
- **Exactly one primary CTA per serve** (MVP_SCOPE_FREEZE failure signal 5, Amendment 1 §4). An
  independently legitimate W2-B action-slot primary action (`decision_refine`) keeps its
  precedence; where none is active, the suppressed state uses its own single CTA, "Review what
  is still needed" / «مراجعة ما لا يزال مطلوبًا», pointing to the SAME existing
  deliverable/handoff route (user-facing copy only; no new route, output or report).
- UQTR never selects or pre-opens another gap; `select_next_gap` stays the one selector.

## 2. Voluntary revisit

The suppressed question stays available through a native, user-controlled `<details>`
disclosure ("Revisit this technical question") containing the EXISTING question and the
EXISTING answer form. There is no new route, no persisted revisit state, no JavaScript
dependency and no new disposition; an answer given there goes through the unchanged
canonical answered path against the unchanged canonical gap. The completion branch is not
reachable through suppression, because the served question itself is never cleared.

**No answer pressure after suppression (Candidate 02).** The question-specific answer-help
panels — More-Detail-Needed scaffolding, Increment-1B clarification, responsibility guidance,
Guided Uncertainty Support and Guided Answer Co-Authoring — are each defined ONCE in the
template. While suppressed they render only inside the voluntary revisit; otherwise each renders
at its unchanged original position under its unchanged precedence rules. No helper is changed,
removed or duplicated.

## 3. Presentation of the six frozen actions (4 primary + 2 additional)

The six Increment-1A/Increment-2 action values are unchanged and remain ONE radio group:
four primary choices (`answered`, `unknown`, `specialist_requested`, `deferred`) and two
additional choices (`provisional_assumption`, `evidence_requested`) inside a native
disclosure. Answer text stays required for `answered` and optional for every non-answer
action, exactly as before; the existing bilingual action labels are reused.

## 4. RVR-2 exhausted-prompt wording (truth fix)

The generic `_EXHAUSTED_EXIT_PROMPT` (Wave-1 contract, RVR-2) is served for every Stage-2 gap,
including MECHANISM_COMPLETENESS, which `accept_gap_risk` refuses. Its wording no longer
promises the accept-as-known-risk exit; it states that the exit exists only where the page
shows that option. The separate governed accept-risk affordance, its W2-D availability gate,
`accept_gap_risk` and the MECHANISM_COMPLETENESS exemption are unchanged. The paired Arabic
surface (`RVR7_SUBSTANTIVE_AR[_EXHAUSTED_EXIT_PROMPT]`) is updated in the same change.
The final pair is the Owner-approved copy supplied in the Candidate-02 authorization:

- EN: "The prepared questions for this area are exhausted, and repeating them will not move it
  forward. Your available options now: add genuinely new information in the answer box; mark
  this unknown or deferred; note a provisional assumption; or ask for a specialist or evidence.
  Accepting an area as a known risk is possible only where this page shows that option."
- AR: «لقد استُنفدت الأسئلة المعدّة لهذا الجانب، ولن يساعد تكرارها على إحراز مزيد من التقدم.
  الخيارات المتاحة لك الآن: أضف معلومات جديدة فعلًا في خانة الإجابة؛ أو حدّد هذه النقطة على أنها
  غير معروفة أو مؤجلة؛ أو سجّل افتراضًا مبدئيًا؛ أو اطلب رأي مختص أو دليلًا. ولا يمكن قبول هذا
  الجانب كمخاطرة معروفة إلا إذا ظهر هذا الخيار في الصفحة.»

The earlier RVR-7 EN/AR equivalence acceptance (review item 23) covered the pre-UQTR text; this
Owner-approved pair supersedes it for this identity. All UQTR user-facing strings (notice,
per-disposition meanings, revisit, journey note, text hint, CTA) are the Owner-supplied EN/AR
copy, rendered through the existing catalogue — never generated or translated at runtime.

## 5. Mechanical digest re-freeze

`engine/progression_loop.py` changes, so its SHA-256 is re-frozen in the three P9 pin files
under the base contract's bounded mechanical re-freeze allowance, with a disclosed
reconciliation note in each (precedent: W2-B, W2-C, T2-F, T2-G, MG-8). Lineage: pre-UQTR
`da2c405d3f7b4995f43141d0b89720f97e94b731345b1ad054c77b821f58ab90` → Candidate 02
`9220530bf99a796d5f13af84c17cb3c8eeb1fb76754292f16f8cd0506eb0bb77`; the Candidate-01 pin
(`4b3e353c…`) is not in this lineage.

## 5A. Multilingual and model boundary

Candidate 02 stays compatible with the separately adjudicated future Multilingual Semantic
Normalization direction (a future provider-neutral `SemanticNormalizerPort` proposing canonical
InventorAI concepts through a deterministic acceptance boundary) WITHOUT implementing or
activating it. No runtime LLM or AI provider, no `SemanticNormalizerPort`, no change to
`ai_advisor.py` or `semantic_registry.py`, no model configuration or secret, no machine
translation, no dynamically generated Arabic, and no external transmission of user or project
data. Any future model output would be a proposal only — never owner-stated fact, evidence,
validation, gap closure, maturity or readiness promotion, accepted risk or specialist approval.
The Question Translation Assistant (مساعد الترجمة) is a separate future concept and is NOT
implemented. The three responsibilities stay separate: UQTR serving (this amendment), semantic
normalization (future), question translation assistance (future).

## 6. Out of scope (unchanged)

Mechanical Path-N wording (approved as the next UQTR work after CORE closure, not here);
Stage-3 early or cross-gap questioning; `current_stage` or maturity
rules; accepted-risk widening; cross-gap or versioned answer targeting; autonomous technical
orchestration or system-inferred proposals; any new ledger, disposition, status, persisted
field, schema or migration; `idea_state.py`, `record_contract.py`, `session_reconstruction.py`,
`record_store.py`, `deliverable_assembler.py`, `semantic_registry.py`, `ai_advisor.py`, domain
packs and Path-N artifacts; D4, subsystem persistence or any new domain activation; T1-C′ corpus
use; human activity; deployment.
