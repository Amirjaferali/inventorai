# G-4-A CLAIM-ELIGIBILITY BOUNDARY — Contract Amendment 1 — CANDIDATE

**Status:** CANDIDATE — awaiting Lead review, any required independent review under
the standing assurance process, and Owner exact-SHA acceptance. **This document
AUTHORIZES NOTHING by itself.** It becomes part of the authoritative G-4-A contract
lineage only through the complete high-assurance lifecycle (review → Owner exact-SHA
acceptance → merge → post-merge identity verification). Even after it becomes
authoritative:

    IMPLEMENTATION AUTHORIZED: NO
    EXECUTABLE CODE CHANGE AUTHORIZED: NO
    SCHEMA IMPLEMENTATION AUTHORIZED: NO
    HUMAN STUDY AUTHORIZED: NO
    EVIDENCE COLLECTION AUTHORIZED: NO
    GOVERNANCE CANDIDATE ACCEPTANCE != IMPLEMENTATION AUTHORIZATION
    CONTRACT FREEZE != EVIDENCE PASS != IMPLEMENTATION AUTHORIZATION

**Authoritative base:** `95608998537f7d0d042be069f9925fd559438428` on
`feature/atomic-json-session-persistence` — the live remote tip verified from Git at
this gate `[EXEC]`, from a fresh same-base subject created by `git init` + depth-1
fetch of that exact object. Commit subject at this base:
`Merge pull request #606 from Amirjaferali/g4a-hybrid-contract-72f687a3`.

**Base contract amended by this document:**
`docs/governance/G4_A_HYBRID_PREVENTIVE_EVIDENCE_FAIL_CLOSED_CONTRACT.md`
("the Hybrid contract"), blob `042a4261b963f2fd981dd4d06aa8911e4b89f019`,
SHA-256 `3cb01258c40752a7143949f5fdf646e1b4208e1f05c9541772f2932abcdba20e`,
385 lines, 18,649 bytes — verified in the tree at this base `[EXEC]`.

**Stale-heading notice `[EXEC]`.** The Hybrid contract's own line 3 still reads
`STATUS: GOVERNANCE CONTRACT CANDIDATE — NOT YET OWNER-ACCEPTED`, and its header
still names its drafting base `100d224ba61dfff35668944d4aaa3e294d95bc7d`. That
heading is **stale historical text**, not current lifecycle authority: the document
became repository-authoritative through merged PR #606, which is the merge commit at
this very base. This amendment does **not** rewrite that heading — historical
evidence is never edited — and no reader may treat the stale heading as evidence that
the Hybrid contract is un-accepted.

**What this document is.** The bounded reconciliation of the Hybrid contract with the
Owner-directed architecture

    SOURCE-AGNOSTIC MECHANISM-CLAIM ELIGIBILITY BOUNDARY
    under EXISTING MECHANISM INTEGRATION / PROGRESSION OWNERSHIP

It supersedes, modifies, or defers exactly the clauses named in the §2 disposition
table and leaves every other clause of the Hybrid contract in force verbatim. It
changes NO runtime code, NO test, NO schema, NO config, NO status surface, and NO
other governance document.

    CHANGED PATH COUNT: 1
    EXECUTABLE DELTA: 0

This document is subordinate to `CLAUDE.md`, the Lean Governance protocol, the
committed anchors, `ACTIVE_EXECUTION_ROADMAP.md`, and the authoritative G-4-A
contracts. It amends none of them and it activates nothing.

**Classification legend.** `[EXEC]` verified in the tree at this base by direct
inspection; `[OWNER-PREMISE]` an Owner-ratified premise conveyed outside the
repository, recorded as premise and never restated as repository fact; `[DERIVED]` a
conclusion derived from repository evidence; `[PROPOSAL]` a contract term proposed by
this amendment for freeze; `[FUTURE-REQ]` a requirement binding on a future
implementation candidate; `[HYPOTHESIS]` a claim a future implementation's own
evidence must confirm or falsify.

---

## §0. Binding product state preserved by this amendment `[PROPOSAL]`

    G-4-A TECHNICAL DEFECT: CURRENT — NOT FIXED
    DIRECT G-4-A CLASSIFIER DEFECT: STILL PRESENT
    G-4-A: OPEN / FRB
    G-4: OPEN / FRB
    G-4-B: SEPARATE
    M-1: SEPARATE
    NO ACCEPTED IMPLEMENTATION CANDIDATE EXISTS
    LEVEL-1 PATCHING: NOT REOPENED
    LEVEL-4 IMPLEMENTATION: NOT AUTHORIZED
    BROADER ARCHITECTURE IMPLEMENTATION: NOT AUTHORIZED

    CLAIM-ELIGIBILITY ARCHITECTURE = PRODUCT-TRUTH CONTAINMENT
    CLAIM-ELIGIBILITY ARCHITECTURE != DIRECT LINGUISTIC CLASSIFIER FIX

**No clause of this amendment may state or imply that the English
causal-disambiguation defect in `engine/progression_loop.py::assess_response` or in
the current causal-recognition surface has been fixed, closed, superseded, or
deferred away.** The measured `"if "` raw-substring false positive on a preference
clause survives this amendment intact and unrepaired. What changes is whether that
defective judgment retains authority to create mechanism progression — not whether it
is still defective. It is still defective.

---

## §1. Amendment mechanism and lineage `[DERIVED from repository precedent]`

Repository governance precedent resolves contract amendments by **additive
supersession artifacts**, never by in-place rewriting of accepted history. The
governing precedent inspected at this base `[EXEC]` is
`docs/governance/W2_B_RVR6A_CONTRACT_AMENDMENT_1_CANDIDATE.md` — an additive
amendment to `W2_B_RVR6A_IMPLEMENTATION_CONTRACT_CANDIDATE.md` that "supersedes
exactly the clauses named in §2 and leaves every other clause of the base contract in
force", and which `engine/progression_loop.py` cites in its own comments as
"Contract Amendment 1 §4-§6 (authoritative via PR #575)". Sibling precedents at this
base include `PHASE_2_GATE_AMENDMENT_1.md`,
`PATH_N_RUNTIME_INTEGRATION_AUTHORIZATION_PLAN_AMENDMENT_1.md`,
`CF5_F003_CLASSIFIER_MATCHING_SEMANTICS_CORRECTIVE_CONTRACT_AMENDMENT_01.md`, and
`MVP_SCOPE_FREEZE_AMENDMENT_FUNCTIONAL_PATH_N.md`.

**Therefore this amendment is an additive artifact.** The Hybrid contract file is not
edited, not renamed, not deleted, and not re-headed. No repository precedent was found
requiring in-place amendment of an accepted contract, so none is used.

    HISTORICAL CONTRACT PRESERVED: YES — byte-unchanged at blob 042a4261...

**Reading order.** Where this amendment and the Hybrid contract conflict, this
amendment governs for the clauses named in §2 and the Hybrid contract governs
everywhere else. Both remain subordinate to `CLAUDE.md`, the Lean protocol, the
committed anchors, and `ACTIVE_EXECUTION_ROADMAP.md`.

---

## §2. Clause disposition table — complete `[PROPOSAL]`

Every clause of the Hybrid contract is classified. No clause is silently ignored.

| Hybrid clause | Disposition | Exact treatment under this amendment |
|---|---|---|
| **§0** Binding product state | **RETAINED** and restated in §0 above | Every fence carried forward verbatim; the amendment adds `DIRECT G-4-A CLASSIFIER DEFECT: STILL PRESENT` and the containment/fix distinction. |
| **§1** Purpose and product truth | **MODIFIED** | `HYBRID != TECHNICAL G-4-A FIX` is **RETAINED** and generalised: the Claim-Eligibility Boundary is likewise not a technical fix. `PATH 2 = PREVENTIVE EXPLICIT-EVIDENCE ACQUISITION` ceases to be the load-bearing exposure-reduction mechanism (§4). `PATH 3 = FAIL-CLOSED TRUTH PRESERVATION` is **RETAINED and strengthened** into the mechanism fence of §8. |
| **§2** System-detected insufficiency semantics | **RETAINED** | Every listed consequence of an unresolved claim (`CAUSAL CREDIT: 0`, `MECHANISM CREDIT: 0`, `GAP CLOSURE: NO`, `MATURITY ADVANCE: NO`, `NEW DISPOSITION CREATED AUTOMATICALLY: NO`) is exactly the fail-closed behaviour of an **unqualified claim** under §8. The clause is re-anchored from "system-detected insufficiency" to "absence of a valid positive eligibility event", which is a strictly more determinate trigger. |
| **§3** `evidence_requested` fence | **RETAINED, UNCHANGED** | `INTERACTION LEDGER != ROUTING AUTHORITY` and `EVIDENCE / PROVENANCE RECORD != PROGRESSION STATE` remain binding. A `ClaimEligibilityEvent` is **not** an interaction disposition and is **not** an `AssertionRecord` (§6); it never redefines, auto-creates, or promotes `evidence_requested`. |
| **§4** `ACCEPTED_RISK` fence | **RETAINED, UNCHANGED** | `MISSING EVIDENCE != ACCEPTED_RISK`, `SYSTEM-DETECTED INSUFFICIENCY != ACCEPTED_RISK`, `UNRESOLVED MECHANISM_COMPLETENESS != ACCEPTED_RISK`. Verified favourable property `[EXEC]`: `engine/progression_loop.py::accept_gap_risk` refuses `MECHANISM_COMPLETENESS` by construction, so risk acceptance cannot become an escape hatch around the §8 fence. |
| **§5** Preventive question semantic contract (incl. the Branch A/B/C completion table) | **SUPERSEDED as a runtime requirement; DEFERRED WITH RETURN CONDITION as a question-design option** | The runtime `A/B/C` branch model is not required and is not adopted (§4); the basis is that no admissible automatic mechanism was found to carry it (§3), never a measured human-exposure conclusion. Return condition: §5 returns in full if a preventive or materially different evidence-acquisition question is later separately authorized. Its `no causal credit` intent survives, carried by §8 rather than by a classifier. |
| **§6** Category / yes-no fence | **RETAINED, UNCHANGED** | `CATEGORY / YES-NO SELECTION != CREDIT` and `USER INTENT CONFIRMATION != MECHANISM COMPLETENESS` remain binding and are reinforced: `USER CONFIRMATION != ELIGIBLE`, `FORM COMPLETION != ELIGIBLE` (§5 of this amendment). |
| **§7** Anti-leading / contamination requirement | **DEFERRED WITH RETURN CONDITION** | It governs the wording of a preventive question. No question wording is load-bearing under this architecture, so the requirement has no current subject. Return condition: it returns in full, unmodified, with any later authorized preventive or materially changed evidence-acquisition question. It is **not** deleted. |
| **§8** Question identity / WS10 fence | **MODIFIED** | The WS10 inspection-and-comparison obligation is **RETAINED verbatim** for any future question change. The *trigger* becomes conditional (§19 of this amendment): the Claim-Eligibility Boundary alone changes no question wording, no WS10 record and no Path-N content, so it creates no new question-ID requirement. `SEMANTICALLY EQUIVALENT -> SAME ID MAY REMAIN ELIGIBLE` / `MATERIALLY DIFFERENT -> NEW GOVERNED QUESTION_ID REQUIRED` is retained as the rule. WS10 remains design-time only; the closed WS11 boundary (`question_id` never reconstructed from text) is untouched. |
| **§9** Bounded routing semantics | **RETAINED, UNCHANGED** | `INTERACTION LEDGER != ROUTING AUTHORITY` remains binding, and this amendment strengthens it: no `AssertionRecord` disposition — `evidence_requested`, `AcknowledgedUnknown`, `ACCEPTED_RISK`, or any other — becomes routing or eligibility authority. Eligibility authority is carried **only** by the typed `ClaimEligibilityEvent`, which is not a ledger disposition. |
| **§10** T2-G separation | **RETAINED, UNCHANGED** | No answer meaning selects a question. `T2-G REQUIRED: NO`. The served question is fixed and governed; the eligibility event is attached to a claim after the fact by exact identity, never by meaning-driven question selection. |
| **§11** Yield semantics | **DEFERRED WITH RETURN CONDITION** | `YIELD != EXIT` is retained as a principle, but no yield mechanism is part of this architecture. `CROSS-GAP YIELD / RETURN EXPANSION: NOT REQUIRED` (§20 of this amendment). Return condition: separate Owner authorization for any stronger cross-gap yield architecture. |
| **§12** Return trigger | **DEFERRED WITH RETURN CONDITION** | Its core prohibition is **RETAINED and strengthened**: *"Do not semantically scan unrelated answers and infer that they happened to resolve the obligation."* Under this architecture nothing is inferred from any answer's meaning at all. The yield-then-return event model is deferred with §11. |
| **§13** Latest-safe gate | **RETAINED, UNCHANGED** | `MECHANISM_COMPLETENESS NOT CLOSED -> TRANSITION DOES NOT PASS`. Verified `[EXEC]`: `evaluate_transition` already enforces exactly this at the level-1 rule, and the §8 fence makes its inputs unreachable from free text. |
| **§14** Persistence / provenance requirement | **MODIFIED** | The measured finding is **RETAINED verbatim and re-verified at this base `[EXEC]`**: `AssertionRecord` carries no served-question identity and no content-version field, and WS11 prohibits recovering `question_id` from text. What changes is the consequence: the Claim-Eligibility Boundary does **not** require question-identity persistence, because it keys on `AssertionRecord.record_id` — a durable identity that already exists. `NO SCHEMA MODIFICATION AUTHORIZED NOW` is **RETAINED**; §11 of this amendment establishes that no physical schema change is required at all. The clause's closing sentence — *"The audit requirement must not be reduced merely to avoid persistence expansion"* — is **RETAINED and reaffirmed**: question-identity persistence remains required the moment exact question identity becomes material to audit, and that requirement is not weakened by this architecture's not needing it. |
| **§15** Replay requirements | **MODIFIED (strengthened)** | `No historical record may be rewritten retroactively` is **RETAINED verbatim**. The reconstruction list is retargeted to this architecture: the original answer · the gap · the claim identity · the recomputed claim quality · the eligibility event and its verdict · the active/stale/superseded derivation · credit = 0 where no valid positive event exists · the final gap state. `LIVE = REPLAY` becomes an explicit binding requirement (§13 of this amendment). |
| **§16** Ownership | **RETAINED, UNCHANGED** | `NEW ASSESSMENT OWNER: NO` · `SECOND CAUSAL OWNER: NO` · `SECOND LANGUAGE OWNER: NO` · `SECOND QUESTION SYSTEM: NO` · `SECOND EPISTEMIC TRUTH SOURCE: NO`. WS12 remains observation only. Verified `[EXEC]`: `engine/progression_loop.py` is the sole writer of `known_mechanism` (one write site) and, with `accept_gap_risk`, the sole writer of `MECHANISM_COMPLETENESS` status — and it remains so under §8/§9 of this amendment. |
| **§16A** English-only fence | **RETAINED, UNCHANGED** | `ARABIC WIDENING: NOT AUTHORIZED` · `G-5: NOT CLOSED`. The architecture touches no language-recognition surface; the fence is language-independent and is unaffected. |
| **§17** Exposure-Reduction Evidence Gate | **MODIFIED / RETARGETED** | Complete mapping in §17 of this amendment. Limb 1 retargeted and extended; Limb 2's *principle* retained, its preventive-question wording study superseded and replaced by the Claim-Eligibility Human-Review Evidence Gate. |
| **§18** Evidence-collection authorization dependency | **RETAINED, UNCHANGED** | Acceptance of this amendment authorizes none of: a Creator technical experiment · a human study · a production wording change · `Run-004` · `T1-C'` · any validation lane · implementation. |
| **§19** Non-production study requirement | **RETAINED, MODIFIED IN SCOPE** | Still a separately authorized non-production surface. The audit-preservation clause is retargeted (§17 of this amendment) and returns to question wording if preventive wording returns. |
| **§20** Residual-exposure continuity | **RETAINED, UNCHANGED** | `RETURN TO DIRECT ENGINE DEFECT REQUIRED` if material residual G-4-A product-truth exposure remains after the Evidence Gate. **Never silent disappearance.** |
| **§21** G-4 / FRB continuity | **RETAINED, UNCHANGED** | `HYBRID DOES NOT CLOSE G-4-A` · `HYBRID DOES NOT CLOSE G-4` · `G-4: OPEN / FRB` · `G-4-B: SEPARATE` · `M-1: SEPARATE`. This amendment closes nothing and creates no automatic G-4 closure. |
| **§22** PRE-FCORA fence | **RETAINED, UNCHANGED** | `SILENT DISAPPEARANCE OF G-4-A: PROHIBITED`. The pre-FCORA reconciliation list now also covers this amendment's Evidence Gate result. |
| **§23** B2 status | **RETAINED, UNCHANGED** | `B2: PRESERVED FUTURE CANDIDATE` · `B2 TRIGGER CONTRACT: NOT ACCEPTED`. No structured intent-selection flow is authorized. An eligibility event is a governed third-party attestation about a recorded claim, not a user intent selection. |
| **§24** Potential future surfaces | **MODIFIED (list retargeted)** | `POTENTIAL SURFACE != AUTHORIZED SURFACE` is **RETAINED verbatim**. The indicative list is retargeted in §18 of this amendment. Listing a surface still neither authorizes touching it nor predicts it will be needed. |
| **§25** Forbidden capabilities | **RETAINED, UNCHANGED, and reinforced** | General NLP · POS · coreference · semantic parser · LLM / embeddings · new semantic provider · open-ended semantic or lexical inventory · domain-pack expansion for this repair · M-1 · Mechanism B · Arabic assessment widening · T2-G activation · dynamic generated questions · new question subsystem · new accepted-risk route · new semantic/language/causal/assessment owner · G-4 full closure · FCORA execution · `Run-004` / `S2` — all remain prohibited. This amendment requires **none** of them. |
| **§26** Lifecycle and non-authorization | **RETAINED, UNCHANGED** | Every carried fence remains in force. This amendment likewise becomes authoritative only through review, Owner exact-SHA acceptance, merge, and post-merge identity verification. |

---

## §3. What the prior technical evidence actually established `[DERIVED]`

Two Creator evidence passes on the authoritative base measured the following, and
they are the basis for the §2 dispositions of Hybrid §5 and §7. **They are technical
runs only. Neither collected human evidence, and neither may be read as a conclusion
about human behaviour.**

1. **No branch-classification capability exists, and none is reachable.** Across a
   corpus of real answers to the committed `N-MC-1` question, the current
   product owners (`assess_response`, `addresses_gap`, `supplemental_relevance`,
   `integrate_response`) produced **4 distinct observable vectors for 3 intended
   branches, with 10 cross-branch collisions** — including a preference statement
   carrying an explicit non-mechanism disclaimer that received `REASONED` causal
   credit and advanced `MECHANISM_COMPLETENESS` from `OPEN` to `PARTIAL`. The only
   question-bound surface in the repository, `engine/question_aware_evaluation.py`,
   has zero runtime consumers and never receives the answer text at all.
2. **A bounded positive-evidence gate is not viable.** A frozen two-slot
   `condition / resulting behaviour` sufficiency gate, feature set and lexicon fixed
   before any case was authored and byte-unchanged through a single one-pass run over
   27 cases, produced 0 false negatives but **2 false positives** — including the
   load-bearing preference-plus-causal-token family the current defect originates
   from — and its load-bearing generic-placeholder set was defeated by 2 of 4
   meaning-preserving paraphrases. `LEXICON GROWTH REQUIRED: YES`;
   `SEMANTIC INTERPRETATION EXPANSION REQUIRED: YES`.

Both results are Creator execution evidence, not Lead acceptance.

**Exactly what is established `[DERIVED]`:**

1. **Current / runtime `A/B/C` branch classification is not sufficient.** The measured
   observable space of the current owners does not separate the intended branches.
2. **The tested `TWO FREE-TEXT SLOTS + BOUNDED MORPHOLOGICAL / CLOSED-CLASS AUTOMATIC
   SUFFICIENCY GATE` is not viable.** It admitted the load-bearing
   preference-plus-causal-token family and its load-bearing set required unbounded
   growth.
3. **The tested bounded deterministic free-text classification / sufficiency
   mechanisms cannot carry the load-bearing protection within the authorized
   capability fence.**

**Exactly what is NOT established, and must not be inferred:**

    PREVENTIVE-QUESTION HUMAN EXPOSURE-REDUCTION EFFECT:
      NOT ESTABLISHED BY THESE TECHNICAL RUNS
      NOT FALSIFIED BY THESE TECHNICAL RUNS

These runs collected no human evidence, so they say nothing either way about whether
asking a preventive question would change how often a real user produces an answer
that triggers the G-4-A condition. Attributing a human-exposure conclusion to them
is prohibited. The preventive-question model is non-load-bearing under the accepted
architecture because no admissible automatic mechanism was found to carry it — not
because its human effect was measured and rejected. It remains non-load-bearing
unless separately reauthorized, and any future authorization of it returns Hybrid
§5, §7 and the preventive-question wording metrics of Hybrid §17 Limb 2 in full
(§2, §17).

---

## §4. The amended architecture `[PROPOSAL]`

    OWNER-STATED CLAIM
    -> UNQUALIFIED CLAIM
    -> VALID CLAIM-ELIGIBILITY EVENT
    -> EXISTING MECHANISM-ONLY PROGRESSION APPLICATION SEAM
    -> NORMAL MECHANISM PROGRESSION

An owner's answer to a `MECHANISM_COMPLETENESS` question is durably accepted as an
**unqualified candidate claim**. It carries no mechanism credit on its own, however it
is worded, whatever tier the existing classifier assigns it, and whatever the existing
relevance owner says about it. Mechanism progression becomes possible only when a
valid positive eligibility event, issued by a governed and authenticated source,
targets that exact claim.

The protection is therefore **structural, not linguistic**. It does not depend on any
system correctly interpreting a sentence.

---

## §5. Binding invariants `[PROPOSAL]`

    UNQUALIFIED CLAIM != PROGRESSION-ELIGIBLE CLAIM
    REASONED != ELIGIBLE
    RELEVANT != ELIGIBLE
    USER CONFIRMATION != ELIGIBLE
    FORM COMPLETION != ELIGIBLE
    CLAIM SUFFICIENCY != TECHNICAL / EMPIRICAL VALIDATION
    HUMAN REVIEW NOW != HUMAN REVIEW FOREVER
    FUTURE AUTHORIZED VALIDATOR != NEW PROGRESSION OWNER
    NEW ASSESSMENT OWNER: NO
    ROUTING EXPANSION REQUIRED: NO
    GENERAL NLP / LLM: NOT REQUIRED / NOT AUTHORIZED
    A/B/C RUNTIME CLASSIFIER: NOT REQUIRED
    RUNTIME PREFERENCE CLASSIFIER: PROHIBITED
    FREE-TEXT SEMANTIC SUFFICIENCY CLASSIFIER: PROHIBITED

`CLAIM SUFFICIENCY != TECHNICAL / EMPIRICAL VALIDATION` is load-bearing and has a
measured basis `[EXEC]`: the existing `validation_status` vocabulary
(`UNVALIDATED` / `SPECIALIST_REVIEWED` / `EMPIRICALLY_DEMONSTRATED` /
`INDEPENDENTLY_VERIFIED`) means technical or independent validation and is rendered to
the user with exactly those words by `engine/deliverable_assembler.py`, while
`engine/derived_readiness.py` treats any record still `UNVALIDATED` as blocking
verified readiness. Overloading it to mean "claim sufficiently articulated" would make
the product's own deliverable false. **`validation_status` is not touched, not
extended, and not reinterpreted by this architecture.**

---

## §6. Typed `ClaimEligibilityEvent` `[PROPOSAL]`

A `ClaimEligibilityEvent` is a **typed logical record, distinct from
`AssertionRecord`**. Its semantics are never disguised as an assertion, never hidden
inside `AssertionRecord.content`, and never carried by reinterpreting `disposition`,
`validation_status`, `quality`, `provenance`, or `supersedes` outside their current
authoritative meanings.

**Minimum semantic fields.**

| Field | Meaning | Durability |
|---|---|---|
| `event_id` | the event's own durable identity | durable |
| `target_claim_id` | the exact `AssertionRecord.record_id` of the reviewed claim | durable |
| `result` | `SUFFICIENT` \| `INSUFFICIENT` | durable |
| `source_type` | `HUMAN_CLAIM_SUFFICIENCY_REVIEW` \| `FUTURE_AUTHORIZED_VALIDATOR` | durable |
| `source_authority_id` | the governed reviewer / validator authority identity | durable |
| `source_version` | the version of that authority's method or configuration | durable |
| `eligibility_policy_version` | the governed policy the verdict was issued under | durable |
| `mint_principal_id` | the authenticated machine credential identity that executed the mint | durable |
| `mint_request_id` | the exact durable audit-link identity for the mint decision | durable |
| `supersedes_prior_event_id` | set only when correcting a prior eligibility event | durable, nullable |
| *ordering* | the existing durable record stream's `seq` | already durable — **nothing added** |
| *staleness* | **DERIVED at read time, NEVER STORED** | — |

**Frozen event rules.**

    MAXIMUM ONE ACTIVE ELIGIBILITY EVENT PER CLAIM
    VERDICT CHANGE -> NEW EVENT SUPERSEDES PRIOR EVENT
    TARGET CLAIM CORRECTED / SUPERSEDED -> PRIOR ELIGIBILITY STALE FOR PROGRESSION
    ELIGIBILITY NEVER TRANSFERS TO A REPLACEMENT CLAIM
    SUFFICIENT AND INSUFFICIENT ARE BOTH DURABLE REVIEW TRUTH
    ABSENCE OF AN EVENT = UNREVIEWED / NO VALID ELIGIBILITY -> FAILS CLOSED

    ACTIVE EVENT     = not named by the supersedes_prior_event_id of any
                       later-seq event in the validated history
    SUPERSEDED EVENT = named by the supersedes_prior_event_id of a later-seq event
    STALE EVENT      = ACTIVE, but its target claim carries superseded_by
                       (derived, never stored; the event remains durable review truth
                        and simply carries no eligibility for progression)

Every one of these is **derived from the authoritative `seq` order of the one global
ordered record stream (§11)**, never from insertion order in memory, never from a
stored flag, and never from wall-clock time.

**Same-claim correction invariant — binding validation `[PROPOSAL]`.** When
`supersedes_prior_event_id != NULL`, **all** of the following must hold:

    PRIOR EVENT MUST EXIST
    PRIOR RECORD KIND MUST BE ClaimEligibilityEvent
    PRIOR EVENT MUST BE VALID FOR THE SAME PROJECT
    prior_event.target_claim_id == new_event.target_claim_id
    OTHERWISE FAIL CLOSED

    CROSS-CLAIM ELIGIBILITY-EVENT SUPERSESSION: PROHIBITED

An eligibility event for Claim Y must never supersede, deactivate, or otherwise
disturb an event for Claim X. Correction is always *within* one target claim. This is
what makes `MAXIMUM ONE ACTIVE ELIGIBILITY EVENT PER CLAIM` a per-claim invariant
rather than a global one, and it is the reason a cross-claim supersession edge can
never silently strip a claim of its eligibility.

**Correction-chain temporal semantics — binding `[PROPOSAL]`.** The clauses above are
evaluated at two different moments against two different histories, and the difference
is load-bearing. Stating them as one undifferentiated "at mint time and again on load"
check is ambiguous and, at full-history load, self-invalidating: the correction event
`E_new` is itself the reason its predecessor `E_prior` is superseded, so a loader that
required `E_prior` to be un-superseded in the *final* history would reject every
legitimate correction. That reading is prohibited.

**Mint-time rule** — evaluated immediately BEFORE minting `E_new`, against the
validated **pre-mint** history:

    PRIOR EVENT MUST BE ACTIVE IN THE VALIDATED PRE-MINT HISTORY
    PRIOR EVENT MUST PRECEDE THE NEW EVENT IN AUTHORITATIVE seq ORDER
    PRIOR EVENT MUST NOT ALREADY HAVE A DIFFERENT SUPERSEDER
    OTHERWISE FAIL CLOSED — NOTHING IS MINTED

**Load-time rule** — evaluated over the full validated history, in authoritative `seq`
order:

    A correction edge E_new -> E_prior is valid only if E_prior precedes E_new in
    authoritative seq order and E_new is the SOLE DIRECT SUPERSEDER of E_prior.

Equivalently, in prefix form:

    When validating events in authoritative seq order, E_prior must be ACTIVE in the
    validated prefix immediately before E_new; applying E_new then makes E_prior
    SUPERSEDED by E_new.

    THE CURRENT CORRECTION EDGE MUST NOT SELF-INVALIDATE ON LOAD

That `E_prior` is superseded **by `E_new` itself** in the final loaded history is not a
defect: it is the VALID and REQUIRED outcome of applying `E_new`. Only a superseder
that is *not* `E_new` invalidates the edge.

**Linear per-claim chain `[PROPOSAL]`.**

    ELIGIBILITY CORRECTION GRAPH PER CLAIM = LINEAR, NON-BRANCHING CHAIN

Therefore, per claim: one event has at most one direct superseder · one correction
event supersedes at most one prior eligibility event · every correction stays within
the same `target_claim_id` · no forward reference to a later-`seq` event · no cycle ·
exactly one ACTIVE chain head. Two events naming the same predecessor is a branch and
fails closed; so does an edge pointing forward in `seq`, which is what makes a cycle
unrepresentable rather than merely detected.

This clarifies the already-accepted `MAXIMUM ONE ACTIVE ELIGIBILITY EVENT PER CLAIM`
— the single ACTIVE chain head *is* that one active event. It introduces no new
architecture, no new field, no new record kind, and no new owner.

Any clause above that fails makes the new event invalid: at mint time nothing is
minted, and at load time the contract does not load.

`SUFFICIENT` means only that the existing progression owner **may now evaluate**
mechanism progression on its own existing terms. It does not mean the mechanism is
technically valid, empirically demonstrated, or independently verified.

---

## §7. Target fence `[PROPOSAL]`

A progression-bearing `ClaimEligibilityEvent` is valid only when **all** hold:

    TARGET EXISTS
    TARGET RECORD KIND = ASSERTION
    TARGET DISPOSITION = ANSWERED
    TARGET GAP_CONTEXT = MECHANISM_COMPLETENESS
    TARGET NOT SUPERSEDED

Linkage is by **exact durable claim identity only**. Explicitly prohibited:

    TEXT SIMILARITY LINKAGE: PROHIBITED
    POSITIONAL INFERENCE: PROHIBITED
    GAP-ONLY LINKAGE: PROHIBITED
    QUESTION-TEXT REVERSE LOOKUP: PROHIBITED

The last of these is continuous with the closed WS11 boundary, under which
`question_id` is never reconstructed, inferred, derived, parsed, hashed, normalized,
translated, fuzzy-matched, or reverse-looked-up from text.

**Late-event rule.** If a valid `SUFFICIENT` event arrives after
`MECHANISM_COMPLETENESS` has already become `CLOSED` through another eligible claim:

    EVENT REMAINS DURABLE REVIEW TRUTH
    PROGRESSION APPLICATION = NO-OP — GAP ALREADY CLOSED
    known_mechanism MUST NOT BE OVERWRITTEN BY THE LATE EVENT

`[FUTURE-REQ]` This requires an explicit ordering discipline inside the application
seam. Measured at this base `[EXEC]`: in the current code the `known_mechanism` write
precedes the already-`CLOSED` guard, so a naive relocation of the existing blocks in
their existing order would let a late event overwrite `known_mechanism` whenever the
recomputed quality is greater than or equal to the stored one. **The seam must
evaluate the already-closed guard first and return before touching `known_mechanism`.**

---

## §8. Fail-closed mechanism fence `[PROPOSAL]`

Existing mechanism progression / integration ownership remains the **sole canonical
writer** of `known_mechanism` and of the `MECHANISM_COMPLETENESS` lifecycle.

Without a valid positive eligibility event for the exact claim:

    NEW MECHANISM CREDIT = 0
    NO NEW known_mechanism WRITE
    NO OPEN -> PARTIAL
    NO PARTIAL -> CLOSED
    NO MATURITY ADVANCE DERIVED FROM THE UNQUALIFIED CLAIM
    NO STAGE ADVANCE DERIVED FROM THE UNQUALIFIED CLAIM

Neither `REASONED`, nor `addresses_gap = True`, nor their combination may create
progression eligibility.

    assess_response: UNCHANGED
    addresses_gap: UNCHANGED
    addresses_gap != ELIGIBILITY AUTHORITY

The defective classifier is deliberately left byte-unchanged. The architecture removes
its **authority**, not its defect. `RELEVANT != ELIGIBLE` applies only within the §7
target fence: outside an exact active answered `MECHANISM_COMPLETENESS` claim, an
eligibility event confers nothing at all.

---

## §9. Mechanism-only application seam `[PROPOSAL + FUTURE-REQ]`

One bounded, mechanism-specific application seam inside the existing progression
owner — conceptually `apply_eligible_mechanism_claim(...)`, or the
repository-appropriate equivalent — is the single canonical path by which an eligible
claim produces mechanism progression. **`LIVE` and `REPLAY` must call the same seam.**

It **may** apply only: claim-specific quality (§10) · `known_mechanism` consequences ·
`MECHANISM_COMPLETENESS` lifecycle · and normal transition evaluation afterwards.

It **must not**: re-run full response integration for a historical claim · duplicate
`known_problem` · duplicate acknowledged-unknown capture · perform general response
ingestion · process unrelated gaps · or mutate the interaction ledger.

    SOLE MECHANISM PROGRESSION OWNER: PRESERVED
    NEW PROGRESSION OWNER: NO
    A FUTURE AUTHORIZED VALIDATOR NEVER BECOMES A PROGRESSION OWNER

---

## §10. Claim quality `[PROPOSAL]`

    AssertionRecord.quality != AUTHORITATIVE CLAIM-SPECIFIC QUALITY

Measured at this base `[EXEC]`: the runtime writes that field from the post-progression
`known_mechanism` / `known_problem` value, making it a snapshot of session state rather
than a property of the claim.

The quality required by the application seam is instead a **deterministic recomputation
from the immutable candidate-claim content under the pinned assessment / engine
version** — conceptually
`assess_response(immutable_claim_content, durable_confirmed_domain)`.

This recomputation is `QUALITY`, never `ELIGIBILITY`. A `SUFFICIENT` event whose
recomputed tier is `ASSERTED` still yields only the existing `ASSERTED` consequence; it
never manufactures closure.

    SCHEMA ADDITION FOR CLAIM QUALITY: NO
    ASSESSMENT-AFFECTING CHANGE -> RECONSTRUCTION VERSION BUMP REQUIRED

**Assessment-affecting scope** includes every load-bearing surface whose change can
alter the recomputed claim quality: the assessment entry point and its helper gates,
the registered causal-structure surfaces, the domain substance-signal packs, and the
registered non-English surface sets consulted by relevance and assessment. A change to
any of them without a reconstruction-version bump would silently break replay parity
and is prohibited.

---

## §11. Global ordered typed record contract `[PROPOSAL]`

    ONE GLOBAL ORDERED TYPED RECORD STREAM

The logical stream is `AssertionRecord | ClaimEligibilityEvent` in the existing durable
`seq` order of the existing physical `records(project_id, seq, record_id, payload)`
store. Original interleaving is authoritative and must never be reconstructed from two
separately stored logical lists. Derived assertion-only and event-only views may exist
for convenience but are **never the ordering authority**.

**Contract version strategy: B — version bump with explicit legacy read support.**

    CONTRACT VERSION STRATEGY: B
    V1: LEGACY READ SUPPORT — ASSERTION RECORDS ONLY
    V1 CLAIM-ELIGIBILITY EVENT APPEND: PROHIBITED
    V1 PROJECT -> CLAIM-ELIGIBILITY EVENT APPEND: PROHIBITED
    V2: TYPED ASSERTION + CLAIM-ELIGIBILITY EVENT SUPPORT
    NO IMPLICIT PROJECT UPGRADE
    NO SILENT V1 -> V2 MUTATION

No event may be written into a v1 project, and no write may leave a project
unloadable. Eligibility support for an existing v1 project would require a separately
governed explicit upgrade path; **that path is deliberately not designed here** and is
not authorized.

Strategy B is chosen over a silent additive default under the current version because
the latter would leave the stored version string unable to distinguish a project that
may contain events from one that may not. Legacy compatibility is therefore explicit
and authorized, never implicit.

    LEGACY PROJECT LOAD: PRESERVED UNDER AN EXPLICIT AUTHORIZED VERSION RULE
    PHYSICAL DATABASE SCHEMA CHANGE REQUIRED: NO
    LOGICAL RECORD CONTRACT EXPANSION REQUIRED: YES

Measured basis for `PHYSICAL ... : NO` `[EXEC]`: the durable payload is a single JSON
text column, so a typed discriminator and a second record kind are new keys and values
inside an existing column — no `ALTER TABLE`, no new table, no new index, no
migration. Verified favourable property `[EXEC]`: the bounded reconstruction replay
limit counts accepted-answer evidence only, so eligibility events do not consume it.

---

## §12. Atomicity and idempotency `[PROPOSAL]`

    AUTHENTICATE
    -> VALIDATE SOURCE / POLICY / TARGET
    -> CREATE EVENT
    -> STAGE CONSEQUENCES
    -> DURABLE APPEND WITH IDEMPOTENCY
    -> ONLY THEN PUBLISH STAGED STATE

This ordering exists to prohibit exactly one outcome:

    LIVE STATE ADVANCES + DURABLE EVENT APPEND FAILS: PROHIBITED

**Idempotency carrier.** The existing physical idempotency architecture is reused: the
existing nullable durable idempotency column on the records table plus its existing
partial-unique durability backstop. **No second idempotency system.**

**Key construction.** A bounded eligibility-specific sibling key constructor using the
existing HMAC construction is required and expected. It must bind at minimum:

    sid · target_claim_id · result · source_type · source_authority_id
    source_version · eligibility_policy_version · mint_principal_id
    supersedes_prior_event_id

    ELIGIBILITY-SPECIFIC SIBLING KEY CONSTRUCTION USING THE EXISTING
    HMAC / IDEMPOTENCY CARRIER: REQUIRED

`mint_principal_id` is bound because mint-principal attribution is durable contract
truth (§6, §14): the same verdict on the same claim executed by a different
authenticated principal is a different event, not a retry of the first.

The existing interaction-key signature is **not** claimed sufficient unchanged: it
binds an interaction's action, gap context, iteration and content, none of which
distinguishes two eligibility verdicts on the same claim under different policy,
source, or principal identity.

**Idempotent retry equivalence — binding `[PROPOSAL]`.**

    IDEMPOTENT RETRY EQUIVALENCE =
      THE SAME LOAD-BEARING ELIGIBILITY-MINT SEMANTICS
      UNDER THE SAME AUTHENTICATED MINT PRINCIPAL

Equivalence is decided **only** over the governed semantic mint fingerprint — exactly
the bound field set above. **Server-generated identities must never turn an otherwise
identical retry into a conflicting event:** a freshly proposed `event_id` and a fresh
`mint_request_id` differ on every retry by construction and are therefore explicitly
**excluded** from the equivalence comparison. Requiring them to match would make every
legitimate retry fail closed.

**On a duplicate durable key:**

    RELOAD THE STORED EVENT
    COMPARE THE GOVERNED SEMANTIC MINT FINGERPRINT
    SEMANTIC MATCH    -> IDEMPOTENT NO-OP; THE EXISTING STORED EVENT REMAINS
                         AUTHORITATIVE (its event_id and mint_request_id stand;
                         the newly proposed ones are discarded)
    SEMANTIC MISMATCH -> FAIL CLOSED

A retry can therefore never mint a second `ACTIVE` event, and can never displace the
stored event's identity. An `IntegrityError` is never auto-classified as a duplicate.
**No second idempotency system.**

**Durable failure behaviour.** On any durable append failure, live state remains
exactly unchanged, the staged consequence is discarded, and nothing is acknowledged.
Authentication, authorization, or validation failure denies before any staging, and an
audit-write failure itself fails closed.

---

## §13. Corrections and replay `[PROPOSAL]`

**No backward mutation of live state.** Before any replay progression, the
`ACTIVE CLAIM SET` and the `ACTIVE ELIGIBILITY EVENT SET` are derived from the full
validated ordered contract. It is prohibited to apply superseded eligibility events,
later discover they were superseded, and attempt to undo their consequences.

**Eligibility correction.** Any event with `supersedes_prior_event_id` set requires
`FULL FRESH DETERMINISTIC REPLAY` before corrected live state is published. This
includes `SUFFICIENT -> INSUFFICIENT`, `INSUFFICIENT -> SUFFICIENT`,
`SUFFICIENT -> SUFFICIENT` replacement, and every other correction.

**Claim correction.** If a claim is corrected or superseded and prior eligibility for
the old claim may have affected mechanism progression:
`FULL FRESH DETERMINISTIC REPLAY REQUIRED`. The old eligibility becomes stale, the new
claim begins with `NO VALID ELIGIBILITY`, and eligibility never transfers.

    LIVE CORRECTED STATE = FRESH REPLAY OF CORRECTED DURABLE HISTORY
    TARGETED REVERSE MUTATION: PROHIBITED
    LIVE AND REPLAY CONSUME THE SAME MECHANISM-ONLY APPLICATION SEAM

**Correction atomicity — the safer transaction model.**

    BUILD CANDIDATE ORDERED CONTRACT IN MEMORY
    -> VALIDATE CANDIDATE CONTRACT
    -> FRESH DETERMINISTIC REPLAY OF CANDIDATE HISTORY
    -> IF REPLAY VALID, DURABLE APPEND
    -> ONLY THEN PUBLISH THE EXACT STAGED REPLAYED STATE

If the durable append fails: live state remains unchanged. If the candidate replay is
invalid: no durable append and no live change. **It is prohibited to knowingly create a
durable corrected history while leaving an incompatible advanced live state.** This is
a design requirement; no implementation is authorized here.

**Replay must:** preserve claim ids and event ids · preserve event-to-claim linkage ·
preserve correction and supersession · reject orphan targets · reject more than one
active event per claim · reject stale events for progression · reject unsupported
source, policy and engine versions · **never re-decide eligibility from answer text** ·
and produce the same mechanism state as live.

    LIVE = REPLAY: REQUIRED, under the pinned assessment / reconstruction version
    and the pinned eligibility policy version

---

## §14. Source authority and authentication `[PROPOSAL]`

    MINT PRINCIPAL != SOURCE AUTHORITY

`mint_principal_id` is the authenticated machine-credential identity that executed the
mint. `source_authority_id` is the governed human, reviewer, or validator authority
identity under the eligibility policy. **A credential is not itself a human reviewer
identity and must never be labelled as one.** Where human attribution is load-bearing,
the stable governed authority identity is preserved separately from the credential used
to execute the mint.

Authentication may reuse the existing machine-credential primitives.

    NEW BROAD RBAC / ROLE SYSTEM REQUIRED: NO

**Mint authorization requires BOTH:**

1. an authenticated, active, authorized principal carrying an eligibility-mint scope;
   and
2. a governed source-policy mapping authorizing that principal to act for the stamped
   `source_type`, `source_authority_id`, `source_version`, and
   `eligibility_policy_version`.

    CLIENT-SUPPLIED IDENTITY ALONE IS NEVER AUTHORITY

Audit linkage is preserved by `mint_principal_id` together with `mint_request_id` or an
equivalent exact durable audit identity.

---

## §15. Historical authorization `[PROPOSAL]`

    LATER CREDENTIAL REVOCATION BLOCKS FUTURE MINTS
    LATER CREDENTIAL REVOCATION DOES NOT RETROACTIVELY INVALIDATE AN EVENT
    THAT WAS VALIDLY AUTHORIZED WHEN ISSUED

Replay evaluates an event against the **retained historical** source and policy
authorization for its recorded `source_type`, `source_authority_id`, `source_version`,
`eligibility_policy_version`, and recorded mint attribution. **Historical validity is
never determined solely from present-day credential status.** This is continuous with
the repository's existing principle that historical records are never rewritten.

The eligibility-policy registry and its history must therefore be **version-retentive**
for every version any durable replay may require: historical entries are retained, never
mutated in place.

    UNSUPPORTED HISTORICAL eligibility_policy_version
    -> WHOLE RECONSTRUCTION FAILS CLOSED

An unsupported policy version must never be handled by silently dropping the event and
continuing with weaker progression truth — that would regress a project's mechanism
state invisibly instead of failing visibly.

---

## §16. Yield / return `[PROPOSAL]`

    CROSS-GAP YIELD / RETURN EXPANSION: NOT REQUIRED FOR THE CURRENT MINIMUM ARCHITECTURE

Existing bounded Path-N exhaustion and reframe behaviour remains the current
interaction-level handling. This architecture does **not** authorize serving unrelated
lower-priority gaps while `MECHANISM_COMPLETENESS` remains unresolved.

**Correction of a prior provisional statement.** An earlier Creator return recorded
`ROUTING EXPANSION REQUIRED: YES` while adjudicating the yield/return model of Hybrid
§11/§12. That statement is **not** carried forward as present architecture truth: it
described what a yield/return architecture would need, not what this architecture
needs. It is preserved as the recorded reason the yield/return model is deferred, and
for no other purpose.

If a stronger cross-gap yield architecture is desired later:

    RETURN FOR SEPARATE OWNER AUTHORIZATION

---

## §17. Claim-Eligibility Human-Review Evidence Gate — MANDATORY PREREQUISITE `[PROPOSAL]`

    CLAIM-ELIGIBILITY HUMAN-REVIEW EVIDENCE GATE: MANDATORY BEFORE IMPLEMENTATION AUTHORIZATION
    TECHNICAL EVIDENCE ALONE != SUFFICIENT FOR IMPLEMENTATION AUTHORIZATION

Human review is the **current safe / reference eligibility source**. It is explicitly
**not** a permanent architectural requirement: a future authorized validator may later
emit the identical normalized event. But `HUMAN_NOW` is the currently intended source,
so it carries its own evidence obligation, which replaces the preventive-question
wording study of Hybrid §17 Limb 2.

**Limb 1 — Creator technical evidence (retargeted from Hybrid §17 Limb 1).**

*Retained from the Hybrid list:* deterministic behaviour · no category / yes-no to
credit · no false closure · no accidental maturity advance · restart / replay ·
provenance · no ledger-routing leakage · no `ACCEPTED_RISK` route · no T2-G semantic
routing · no Arabic widening · no unrelated regression · no new assessment owner.

*Added for this architecture:* exact target validation (§7) · typed-record global
ordering (§11) · atomic and idempotent mint including retry behaviour (§12) ·
fail-closed mechanism fence (§8) · no false mechanism progression from an unqualified
claim · correction via fresh replay (§13) · staleness derivation (§6) · historical
source authorization (§15) · `LIVE = REPLAY` equality · legacy v1 project load
preserved and v1 event append refused (§11).

*Deferred with return condition from the Hybrid list:* bounded yield behaviour and
correct return / reassessment. These were properties of the yield/return routing model
(§16) and have no current subject. They return in full with any later authorized
cross-gap yield architecture. **They are not deleted.**

**Limb 2 — Human claim-sufficiency review evidence (replaces the preventive-question
wording study).** A later, separately authorized evidence program must at minimum
evaluate:

    INTER-REVIEWER AGREEMENT
    INTRA-REVIEWER STABILITY
    FALSE-SUFFICIENT RATE
    FALSE-INSUFFICIENT RATE
    PREFERENCE HANDLING
    NONSENSE / ADVERSARIAL CLAIM HANDLING
    DECISION STABILITY
    REVIEWER THROUGHPUT / LATENCY
    POLICY-INSTRUCTION CLARITY

*Retained from Hybrid §17 Limb 2* because they remain meaningful under this
architecture: `G-4-A EXPOSURE RATE` · `FALSE CAUSAL CREDIT RATE` ·
`GENUINE CAUSAL EVIDENCE WITHHELD RATE` · `MECHANISM_COMPLETENESS FALSE-CLOSURE RATE`.

*Superseded, conditionally:* the `CURRENT QUESTION CONDITION` versus
`PREVENTIVE QUESTION CONDITION` wording comparison, and the wording-study metrics
`LEADING / CONTAMINATION RISK`, `PARAPHRASE ROBUSTNESS`, `EXTRA FOLLOW-UP RATE`, and
`USER FRICTION / ABANDONMENT SIGNAL` as applied to a question change. **Return
condition:** all of them return in full if a preventive or materially different
evidence-acquisition question is later authorized as load-bearing.

    NO NUMERICAL PASS THRESHOLD IS INVENTED BY THIS AMENDMENT

The Owner decides thresholds and trade-offs after the evidence exists.

**Two-limb classification — binding `[PROPOSAL]`.** A passing technical limb is not
worthless while the human limb is absent; it is *bounded*.

    TECHNICAL LIMB MAY ESTABLISH STRUCTURAL CONTAINMENT PROPERTIES

where actually proven, including: unqualified free text cannot create mechanism
progression · fail-closed fence integrity · target validation · correction and replay
safety · idempotency · `LIVE = REPLAY`. These are real properties of the system and
may be relied on as such once demonstrated.

    TECHNICAL LIMB ALONE !=
      END-TO-END PRODUCT-TRUTH / ELIGIBILITY-SOURCE VALIDATION

while `HUMAN_NOW` is the current intended eligibility source. Structural containment
says what the machinery does with a verdict; it says nothing about whether the human
source produces verdicts that are accurate, stable, and reproducible. Therefore:

    HUMAN CLAIM-SUFFICIENCY EVIDENCE GATE REMAINS MANDATORY
    BEFORE IMPLEMENTATION AUTHORIZATION

    NO NUMERICAL THRESHOLD IS INVENTED

    HUMAN-STUDY EXECUTION: NOT AUTHORIZED BY THIS AMENDMENT

**Evidence-collection authorization dependency (Hybrid §18, retained unchanged).**
Creating or accepting this amendment authorizes none of: a Creator technical experiment
· a human study · a production wording change · `Run-004` · `T1-C'` · any validation
lane · implementation. A later Owner authorization must identify the exact
study / evidence surface.

**Non-production surface (Hybrid §19, retained, modified in scope).** Human evidence is
collected only on a separately authorized non-production surface. For eligibility-review
evidence the audit preservation requirement is: the exact frozen **claim set**, the
**reviewer instructions**, the **eligibility policy version**, and the
**reviewer / source configuration** needed for audit. If preventive wording returns
later, exact question wording and version preservation returns with it.

**Residual-exposure continuity (Hybrid §20, retained unchanged).** After the Evidence
Gate, if material residual G-4-A product-truth exposure remains:

    RETURN TO DIRECT ENGINE DEFECT REQUIRED

Never silent disappearance.

---

## §18. Potential future surfaces — planning only `[PROPOSAL]`

    POTENTIAL SURFACE != AUTHORIZED SURFACE
    NO IMPLEMENTATION AUTHORIZATION CREATED

A future, separately authorized implementation could require bounded work in existing
owners such as: the canonical state / carrier module · the durable record contract ·
the durable record store adapter (payload handling only) · the progression owner · the
deterministic reconstruction replay · the runtime submission and mint seam · contract-
scoped tests · and mechanical digest synchronization if the then-current lifecycle
requires it after executable-byte changes. Listing a surface here neither authorizes
touching it nor predicts it will be needed.

**Disclosed implementation cost `[EXEC]`.** At this base, 35 test files exercise the
progression entry points against `MECHANISM_COMPLETENESS` or `known_mechanism` **and**
assert a closed gap or a maturity advance; 50 reference both concepts. Under the §8
fence those assertions no longer describe the product's behaviour and must be migrated.
**A default-permissive migration switch is prohibited** — it would reintroduce exactly
the defect this architecture contains.

**Disclosed continuity cost `[EXEC]`.** A reconstruction-version bump (§10, §13) drops
projects created before the bump to accepted-answer-evidence-only reconstruction. That
is the existing intended fail-closed behaviour and must be stated to the Owner rather
than discovered later.

---

## §19. Question-ID rule `[PROPOSAL]`

    NEW GOVERNED QUESTION_ID REQUIRED: CONDITIONAL

    SEMANTICALLY EQUIVALENT QUESTION
    -> SAME QUESTION_ID MAY REMAIN ELIGIBLE

    MATERIALLY DIFFERENT EVIDENCE-ACQUISITION QUESTION
    -> NEW GOVERNED QUESTION_ID REQUIRED

    THE CLAIM-ELIGIBILITY BOUNDARY ITSELF DOES NOT CREATE A NEW QUESTION-ID REQUIREMENT

**Correction of a prior Creator return.** Earlier Creator returns recorded
`NEW GOVERNED QUESTION_ID REQUIRED: YES` as an absolute. That finding was premised on
deploying the two-slot preventive question, a design this architecture does not adopt.
Under the Claim-Eligibility Boundary alone the correct value is `CONDITIONAL`. The
absolute `YES` still holds for any future deployment of a materially different
evidence-acquisition question, and the Hybrid §8 WS10 inspection-and-comparison
obligation is retained unchanged for that case.

---

## §20. Preserved observations and continuity `[PROPOSAL]`

    KNOWN_PROBLEM PARALLEL QUALITY RISK: NON-BLOCKING OBSERVATION
    NO G-4-A SCOPE EXPANSION

The same quality-and-relevance condition that governs the mechanism path also governs
the `known_problem` write feeding the level-0 to level-1 transition. The mechanism-
scoped fence of §8 deliberately does not cover it. This is recorded as a preserved
observation, is **not** a Claim-Eligibility implementation blocker, and authorizes no
level-0 problem-claim redesign.

    DIRECT G-4-A CLASSIFIER DEFECT: CURRENT — NOT FIXED
    LEVEL-1 PATCHING: NOT REOPENED
    NO GENERAL NLP / LLM
    NO NEW ASSESSMENT OWNER
    NO ARABIC WIDENING
    G-4: OPEN / FRB
    G-4-A: OPEN / FRB
    G-4-B: SEPARATE
    M-1: SEPARATE

**No language in this amendment may silently close, supersede, or defer away the
original defect.**

---

## §21. Amendment lifecycle state `[PROPOSAL]`

This document becomes authoritative only through Lead review, any required independent
review under the standing assurance process, Owner **exact-SHA** acceptance, normal
merge, and post-merge identity verification. Governance acceptance of this amendment
would authorize the **amended architecture and its Evidence Gate design** — not
implementation, not evidence collection, not human testing, and not schema work, each of
which requires its own separate Owner authorization.

**Fences carried unchanged from the Hybrid contract §26:**
`G-4-A TECHNICAL DEFECT: CURRENT — NOT FIXED` · `G-4: OPEN / FRB` ·
`G-4 FULL CLOSURE: NOT ASSERTED` ·
`G-4-B / MECHANISM B: SEPARATE, CODE CHANGE NOT AUTHORIZED` ·
`M-1 / gap_relevance.py: SEPARATE, NOT AUTHORIZED` · `T1-A': OPEN` ·
`T2-G: NOT ACTIVATED` · `WS10 / WS11 / WS12 BOUNDARIES: UNCHANGED` ·
`ARABIC WIDENING: NOT AUTHORIZED` ·
`SEMANTIC REGISTRY / DOMAIN PACK EXPANSION: NOT AUTHORIZED` ·
`PERSISTENCE / SCHEMA CHANGE: NOT AUTHORIZED` ·
`FOURTH S2 RUN / RUN-004: NOT AUTHORIZED` · `FCORA: NOT AUTHORIZED` · `PSRR GO: NO` ·
`SERIOUS RELEASE / PRODUCTION / PAID ACTIVATION: NOT AUTHORIZED` ·
`main` NOT RECONCILED.

**Follow-up governance synchronization — NOT PART OF THIS CANDIDATE.** Recording this
architecture in `ACTIVE_EXECUTION_ROADMAP.md`, the Owner Decision Register, and the
Deferred Obligations Register is desirable once the Owner accepts this amendment, but
it is not required for this amendment to be internally truthful and it is deliberately
excluded from this candidate. It is classified as
`FOLLOW-UP GOVERNANCE SYNCHRONIZATION — NOT PART OF THIS CANDIDATE`.

**Lean classification.** `LEAN RISK LEVEL: 2` · `REVIEW DEPTH: 2` — governance-only
contract amendment candidate, zero executable delta, one new file, no existing file
changed.
