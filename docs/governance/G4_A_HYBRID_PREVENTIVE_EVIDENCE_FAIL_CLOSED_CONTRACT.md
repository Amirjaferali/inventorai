# G-4-A HYBRID PREVENTIVE-EVIDENCE + FAIL-CLOSED CONTRACT

**STATUS: GOVERNANCE CONTRACT CANDIDATE — NOT YET OWNER-ACCEPTED.**

    IMPLEMENTATION AUTHORIZED: NO
    EVIDENCE COLLECTION AUTHORIZED: NO
    HUMAN TESTING AUTHORIZED: NO
    GOVERNANCE CANDIDATE ACCEPTANCE ≠ IMPLEMENTATION AUTHORIZATION
    CONTRACT FREEZE ≠ EVIDENCE PASS ≠ IMPLEMENTATION AUTHORIZATION

Created on the authoritative base `100d224ba61dfff35668944d4aaa3e294d95bc7d` on
`feature/atomic-json-session-persistence`, verified live from Git at this gate `[EXEC]`, from a fresh
same-base subject. `CHANGED PATH COUNT: 1` · `EXECUTABLE DELTA: 0`. This document is subordinate to
`CLAUDE.md`, the Lean Governance protocol, the committed anchors, `ACTIVE_EXECUTION_ROADMAP.md`, and the
authoritative G-4-A contracts. It amends none of them and it activates nothing.

---

## §0. Binding product state preserved by this contract

    G-4-A TECHNICAL DEFECT: CURRENT — NOT FIXED
    G-4-A: OPEN / FRB
    NO ACCEPTED IMPLEMENTATION CANDIDATE EXISTS
    LEVEL-1 PATCHING: NOT REOPENED
    LEVEL-4 IMPLEMENTATION: NOT AUTHORIZED
    BROADER ARCHITECTURE IMPLEMENTATION: NOT AUTHORIZED

**No Hybrid progress may silently close, supersede, defer away, or erase the original G-4-A technical
defect.** Every clause below is written so that the defect survives this contract intact.

---

## §1. Purpose and product truth

    PATH 2 = PREVENTIVE EXPLICIT-EVIDENCE ACQUISITION
    PATH 3 = FAIL-CLOSED TRUTH PRESERVATION
    HYBRID = EXPOSURE REDUCTION + TRUTHFUL RESIDUE HANDLING
    HYBRID ≠ TECHNICAL G-4-A FIX

The Hybrid has two halves. **Path 2** reduces how often the product is *exposed* to the G-4-A condition
at all, by asking for explicit condition→system-behaviour evidence up front instead of interpreting an
answer after the fact. **Path 3** preserves truth when exposure still occurs, by refusing to convert an
unresolved claim into credit.

**What the Hybrid does not do.** It does not repair `engine/progression_loop.py`. It does not establish
that the measured English causal false positive is corrected. An answer that would be over-credited today
would still be over-credited if it were produced. The Hybrid changes the *rate of arrival* at the defect
and the *handling of the residue*; it does not change the defective judgment itself. Any statement that
Hybrid progress fixes, closes, or supersedes G-4-A is prohibited by this contract.

---

## §2. System-detected insufficiency semantics

    SYSTEM-DETECTED INSUFFICIENCY → NO NEW INTERACTION DISPOSITION
    GAP REMAINS OPEN / PARTIAL ACCORDING TO EXISTING ACCEPTED EVIDENCE
    CAUSAL CREDIT FROM UNRESOLVED CLAIM: 0
    MECHANISM CREDIT FROM UNRESOLVED CLAIM: 0
    GAP CLOSURE: NO
    MATURITY ADVANCE CAUSED BY INSUFFICIENCY: NO
    NEW ASSERTION / INTERACTION DISPOSITION CREATED AUTOMATICALLY: NO

System-detected insufficiency is an **observation about the current answer**, not a new fact about the
idea. It must NOT auto-create `evidence_requested`, an `AcknowledgedUnknown`, or `ACCEPTED_RISK`. It
writes no assertion record of its own. The gap's status continues to be whatever the existing accepted
evidence already made it.

---

## §3. Existing `evidence_requested` fence

`evidence_requested` is an existing authorized interaction disposition
(`engine/idea_state.py::DISPOSITION_EVIDENCE_REQUESTED`) with existing accepted semantics. The Hybrid
preserves those semantics unchanged and must NOT: redefine it · auto-create it from assessment output ·
make it a gap status · make it a routing state · make it progression authority.

    INTERACTION LEDGER ≠ ROUTING AUTHORITY
    EVIDENCE / PROVENANCE RECORD ≠ PROGRESSION STATE

## §4. `ACCEPTED_RISK` fence

    MISSING EVIDENCE ≠ ACCEPTED_RISK
    SYSTEM-DETECTED INSUFFICIENCY ≠ ACCEPTED_RISK
    UNRESOLVED MECHANISM_COMPLETENESS ≠ ACCEPTED_RISK

`ACCEPTED_RISK` records a deliberate, owner-side acceptance. Absence of evidence is not acceptance of
risk, and routing an unresolved mechanism obligation into that state to tidy the ledger is a force-fit
this contract prohibits.

---

## §5. Preventive question semantic contract

**Design gap:** `MECHANISM_COMPLETENESS`.

**Primary question intent.** Elicit explicit user-authored evidence of whether a specific condition
changes system behaviour and, if it does, what resulting system behaviour occurs — without granting
credit for a category declaration alone.

**Answer objective.** `CONDITION + RESULTING SYSTEM BEHAVIOUR`, **or** an explicit user statement that no
condition→system-behaviour mechanism is being claimed and the statement is only a design preference.

**Completion branches — binding.**

| Branch | Condition | Effect |
|---|---|---|
| **A** | substantive condition + resulting behaviour supplied | normal assessment may proceed on its own existing terms |
| **B** | explicit preference / no behaviour-changing condition claimed | the interaction may complete · **no causal credit** · does **not** itself close `MECHANISM_COMPLETENESS` |
| **C** | evidence remains insufficient | `SYSTEM-DETECTED INSUFFICIENCY` · no new interaction disposition · gap remains OPEN/PARTIAL · credit = 0 · the current interaction may yield **only** under the bounded routing contract (§8) |

Branch B is the half that reduces exposure: a user who is stating a build preference can say so, and the
product records that truthfully instead of mining the sentence for a causal reading.

**Final product wording is NOT frozen by this governance candidate.**

## §6. Category / yes-no fence

    CATEGORY / YES-NO SELECTION ≠ CREDIT
    USER INTENT CONFIRMATION ≠ MECHANISM COMPLETENESS

A category, radio button, yes/no answer, intent identifier, acknowledgement, or confirmation action
cannot substitute for substantive mechanism evidence. Branch B completes an *interaction*; it never
supplies the mechanism.

## §7. Anti-leading / contamination requirement

    PREVENTIVE QUESTION ≠ COACHING THE USER TOWARD A CREDIT-EARNING CLAIM

The preventive question must not teach the user which answer earns progression. The Evidence Gate (§17)
must explicitly measure `LEADING / CONTAMINATION RISK` and must distinguish

    QUESTION HELPS USER EXPRESS AN EXISTING IDEA
    QUESTION INDUCES USER TO INVENT A CAUSAL MECHANISM

**Material contamination invalidates any apparent exposure-reduction benefit**, because a question that
manufactures causal claims raises false-credit risk while appearing to lower ambiguity.

## §8. Question identity / WS10 fence

Do **not** assume the preventive wording may reuse the existing `question_id`. Before any future
implementation, the then-current authoritative WS10 Question Intent Registry record must be inspected and
its `primary_intent`, `answer_objective` and `completion_condition` compared against the §5 contract.

    SEMANTICALLY EQUIVALENT → SAME QUESTION_ID MAY REMAIN ELIGIBLE (subject to future authorization)
    MATERIALLY DIFFERENT     → NEW GOVERNED QUESTION_ID REQUIRED

**A new technical intent must not masquerade as wording polish or a presentation variant.** WS10 remains
design-time question-intent governance only: no runtime user intent and no scoring is placed into WS10.
This clause is consistent with the closed WS11 boundary, under which a served question's identity is read
atomically from one committed entry and `question_id` is never reconstructed, inferred, derived, parsed,
hashed, normalized, translated, fuzzy-matched or reverse-looked-up from question text.

## §9. Bounded routing semantics

Any future routing may depend **only** on then-authoritative deterministic progression state already
owned by the existing progression / question-selection lifecycle.

    INTERACTION LEDGER ≠ ROUTING AUTHORITY

Explicitly prohibited: `evidence_requested`, `AcknowledgedUnknown`, `ACCEPTED_RISK`, or any other
assertion-ledger disposition becoming a routing input **merely because that record exists**. If
ledger-coupled routing later proves materially necessary:

    RETURN FOR SEPARATE OWNER AUTHORIZATION

## §10. T2-G separation

    HYBRID ROUTING ≠ T2-G MEANING-ADAPTIVE QUESTIONING

The Hybrid authorizes none of: semantic interpretation of arbitrary answers to choose the next question ·
transcript-wide user-intent inference · generated adaptive questions · a new runtime semantic taxonomy.
Future Hybrid routing must remain `STATE-BOUND`, `GAP-BOUND`, `QUESTION-ID-BOUND` and deterministic. If
success requires `ANSWER MEANING → DYNAMIC QUESTION SELECTION`:

    STOP — T2-G / SEPARATE OWNER DECISION REQUIRED

## §11. Yield semantics

    YIELD ≠ EXIT

An unresolved `MECHANISM_COMPLETENESS` obligation remains open. Yielding the current interaction does not
close the gap · does not satisfy a maturity transition · does not waive the missing evidence · does not
permit infinite immediate re-serving of the same unsuccessful question. **The exact executable yield
mechanism remains evidence-dependent and is NOT authorized here.**

## §12. Return trigger

    NEW SUBSTANTIVE EVIDENCE FOR THE SAME MECHANISM_COMPLETENESS OBLIGATION

New evidence must reach the obligation through an explicitly governed path. **Do not semantically scan
unrelated answers and infer that they happened to resolve the obligation** — that would reintroduce the
post-hoc interpretation the Hybrid exists to avoid. The return event makes reassessment **eligible**; it
is not sufficiency evidence by itself.

## §13. Latest-safe gate

    BEFORE ANY TRANSITION REQUIRING MECHANISM_COMPLETENESS = CLOSED
    MECHANISM_COMPLETENESS NOT CLOSED → TRANSITION DOES NOT PASS

No unresolved state may be interpreted as "good enough" without a separate Owner decision.

## §14. Persistence / provenance requirement

    CURRENT ASSERTION RECORD SEAM SUFFICIENCY FOR EXACT QUESTION-ID REPLAY: NOT ASSUMED

**Measured at this gate `[EXEC]`:** `engine/idea_state.py::AssertionRecord` carries `record_id`,
`disposition`, `content`, `gap_context`, `iteration`, `provenance`, `validation_status`, `quality`,
`pending`, `responsibility`, `resolves_gap`, `contradicts`, `supersedes`, `superseded_by` and
`decision_context_root` — and **no served-question identity or content-version field**. The closed WS11
`ServedQuestion` seam binds `question_id` + text + `design_gap_id` atomically at serve time but is not
persisted into the assertion record, and WS11 expressly prohibits recovering `question_id` from text. No
reconstruction workaround therefore exists.

If exact question identity/version becomes material to audit, replay, experimental attribution, or return
linkage, the design must preserve `SERVED QUESTION_ID`, `SERVED QUESTION VERSION / CONTENT VERSION`, and
the minimum governed identity needed to reconstruct what the user actually saw.

    PERSISTENCE / PROVENANCE CONTRACT EXPANSION MAY BE REQUIRED BEFORE IMPLEMENTATION
    NO SCHEMA MODIFICATION AUTHORIZED NOW

**The audit requirement must not be reduced merely to avoid persistence expansion.**

## §15. Replay requirements

Any future durable Hybrid state must be third-party reproducible. Where material, replay must reconstruct:
the original answer · the gap · the assessment result · the system-detected insufficiency · the
open/partial gap state · credit = 0 · the yield event · the later substantive evidence · the reassessment ·
the final gap state · and the exact question ID/version if the design makes it material.

**No historical record may be rewritten retroactively.**

## §16. Ownership

    ASSESSMENT / GAP TRUTH        → EXISTING OWNER
    QUESTION CONTENT              → EXISTING PATH-N CONTENT OWNER
    DESIGN-TIME QUESTION INTENT   → EXISTING WS10 OWNER
    EVIDENCE / INTERACTION RECORDS→ EXISTING LEDGER UNDER CURRENT SEMANTICS
    ROUTING                       → EXISTING PROGRESSION OWNER

    NEW ASSESSMENT OWNER: NO
    SECOND CAUSAL OWNER: NO
    SECOND LANGUAGE OWNER: NO
    SECOND QUESTION SYSTEM: NO
    SECOND EPISTEMIC TRUTH SOURCE: NO

WS12 remains observation/classification only and is **NOT** made the progression owner.

## §16A. English-only fence

    INITIAL HYBRID EVIDENCE WORK: G-4-A ENGLISH ONLY
    ENGLISH-ONLY HYBRID ≠ ARABIC PARITY
    G-5: NOT CLOSED BY HYBRID
    ARABIC WIDENING: NOT AUTHORIZED

No Hybrid progress may be used as evidence that broader language-parity obligations are satisfied.

---

## §17. Exposure-Reduction Evidence Gate — MANDATORY PREREQUISITE

    G-4-A PREVENTIVE-QUESTION EXPOSURE-REDUCTION EVIDENCE GATE: MANDATORY
    CONTRACT FREEZE ≠ EVIDENCE PASS ≠ IMPLEMENTATION AUTHORIZATION

Before any implementation authorization, both limbs below must exist.

**Limb 1 — Creator technical evidence.** At minimum: deterministic behaviour · no category/yes-no →
credit · no false closure · no accidental maturity advance · bounded yield behaviour · correct
return/reassessment · restart/replay · provenance · no ledger-routing leakage · no `ACCEPTED_RISK` route ·
no T2-G semantic routing · no Arabic widening · no unrelated regression.

**Limb 2 — Human / independent elicitation evidence.** Mandatory to support **any** claim that the
preventive question reduces G-4-A exposure. Compare `CURRENT QUESTION CONDITION` against
`PREVENTIVE QUESTION CONDITION` using frozen exact wording on a separately authorized non-production study
surface. Required measurements:

    G-4-A EXPOSURE RATE
    FALSE CAUSAL CREDIT RATE
    GENUINE CAUSAL EVIDENCE WITHHELD RATE
    EVIDENCE_REQUESTED / INSUFFICIENT-EVIDENCE RATE (where semantically applicable to the study)
    MECHANISM_COMPLETENESS FALSE-CLOSURE RATE
    EXTRA FOLLOW-UP RATE
    USER FRICTION / ABANDONMENT SIGNAL
    LEADING / CONTAMINATION RISK
    PARAPHRASE ROBUSTNESS

**No numerical pass threshold is invented by this contract.** The Owner decides thresholds and trade-offs
after the evidence exists. A technical limb that passes while the human limb is absent establishes
nothing about exposure reduction.

## §18. Evidence-collection authorization dependency

    EVIDENCE COLLECTION AUTHORIZATION REQUIRED BEFORE IMPLEMENTATION GATE

Creating or accepting this contract candidate authorizes none of: a Creator technical experiment · a human
study · a production wording change · `Run-004` · `T1-C′` · any validation lane. A later Owner
authorization must identify the exact study/evidence surface.

## §19. Non-production study requirement

    HUMAN / INDEPENDENT ELICITATION EVIDENCE: SEPARATELY AUTHORIZED NON-PRODUCTION STUDY SURFACE

Contract acceptance does not authorize live or product question modification. The exact question wording
and version used in the study must be preserved for audit.

## §20. Residual-exposure continuity

After the Evidence Gate, if material G-4-A exposure remains:

    RETURN TO DIRECT ENGINE DEFECT REQUIRED

Possible future dispositions include `DIRECT ENGINE DEFECT CONTINUES`, `OWNER-ACCEPTED LIMITATION — ONLY
IF SEPARATELY AUTHORIZED`, or `BROADER OWNER DECISION`. **Never silent disappearance.**

## §21. G-4 / FRB continuity

    HYBRID DOES NOT CLOSE G-4-A
    HYBRID DOES NOT CLOSE G-4
    G-4: OPEN / FRB
    G-4-B: SEPARATE
    M-1: SEPARATE

No automatic G-4 closure is created by this contract or by any Hybrid milestone.

## §22. PRE-FCORA fence

    PRE-FCORA G-4-A DISPOSITION REQUIRED IF G-4-A REMAINS OPEN
    SILENT DISAPPEARANCE OF G-4-A: PROHIBITED

Before FCORA convenes, the then-current authority must reconcile: G-4-A status · residual exposure ·
Evidence-Gate result · return routing · any separately Owner-accepted limitation · the G-4 / FRB
relationship · and the applicable Deferred Obligations Register state.

## §23. B2 status

    B2: PRESERVED FUTURE CANDIDATE
    B2 TRIGGER CONTRACT: NOT ACCEPTED
    B2 NOT PART OF CURRENT HYBRID CONTRACT

No structured intent-selection flow is authorized.

---

## §24. Potential future surfaces — identified for planning only

    POTENTIAL SURFACE ≠ AUTHORIZED SURFACE
    NO IMPLEMENTATION AUTHORIZATION CREATED

A future, separately authorized implementation **could** require bounded work in existing owners such as:
`engine/progression_loop.py` · the current Path-N question content surface · the current
question-serving / iteration surface · the authoritative WS10 design-intent artifact where a question
identity/content synchronization is actually required · contract-scoped tests · and mechanical P9 digest
synchronization if the then-current P9 lifecycle requires it after executable-byte changes.

Listing a surface here neither authorizes touching it nor predicts that it will be needed.
Persistence/schema changes (§14) remain separately authorized only if a future implementation proves them
necessary.

## §25. Forbidden capabilities

Prohibited under this contract: general NLP · POS infrastructure · coreference · semantic parser ·
LLM / embeddings · a new semantic provider · an open-ended semantic or lexical inventory · domain-pack
expansion for this repair · M-1 · Mechanism B · Arabic assessment widening · T2-G activation · dynamic
generated questions · a new question subsystem · a new accepted-risk route · a new semantic / language /
causal / assessment owner · G-4 full closure · FCORA execution · `Run-004` / `S2`.

---

## §26. Lifecycle and non-authorization

This document becomes authoritative only through independent review, Owner exact-SHA acceptance, normal
merge, and post-merge identity verification. Governance acceptance of this contract would authorize the
**Evidence Gate design**, not implementation, not evidence collection, and not human testing — each of
which requires its own separate Owner authorization.

**Fences carried unchanged:** `G-4-A TECHNICAL DEFECT: CURRENT — NOT FIXED` · `G-4: OPEN / FRB` ·
`G-4 FULL CLOSURE: NOT ASSERTED` · `G-4-B / MECHANISM B: SEPARATE, CODE CHANGE NOT AUTHORIZED` ·
`M-1 / gap_relevance.py: SEPARATE, NOT AUTHORIZED` · `T1-A′: OPEN` · `T2-G: NOT ACTIVATED` ·
`WS10 / WS11 / WS12 BOUNDARIES: UNCHANGED` · `ARABIC WIDENING: NOT AUTHORIZED` ·
`SEMANTIC REGISTRY / DOMAIN PACK EXPANSION: NOT AUTHORIZED` · `PERSISTENCE / SCHEMA CHANGE: NOT AUTHORIZED` ·
`FOURTH S2 RUN / RUN-004: NOT AUTHORIZED` · `FCORA: NOT AUTHORIZED` · `PSRR GO: NO` ·
`ACTIVE CONTRACT: NONE` (untouched) · `SERIOUS RELEASE / PRODUCTION / PAID ACTIVATION: NOT AUTHORIZED` ·
`main` NOT RECONCILED.

**Lean classification.** `LEAN RISK LEVEL: 2` · `REVIEW DEPTH: 2` — governance-only contract candidate,
zero executable delta, one new file, no existing file changed.
