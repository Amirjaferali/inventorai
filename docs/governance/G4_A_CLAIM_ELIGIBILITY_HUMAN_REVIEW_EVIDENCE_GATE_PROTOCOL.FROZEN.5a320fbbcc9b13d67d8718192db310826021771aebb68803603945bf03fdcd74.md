# G-4-A CLAIM-ELIGIBILITY HUMAN-REVIEW EVIDENCE GATE — PRE-PILOT PROTOCOL — PRE-FREEZE DRAFT

    STATUS: PRE-FREEZE DRAFT — MUTABLE WORKING ARTIFACT — NOT AUTHORITATIVE

    IMMUTABLE FREEZE PERFORMED: NO
    FROZEN: NO
    COMMIT CREATED: NO
    BRANCH CREATED / UPDATED: NO
    EXACT-SHA CANDIDATE IDENTITY: NONE — this text has no commit, tree or blob identity
    LEAD SUBSTANTIVE REVIEW OF THIS DRAFT: NOT COMPLETE
    LEAD DIFFERENTIAL PRE-FREEZE RE-REVIEW: NOT PERFORMED
    CLEAN PRE-FREEZE GATE: NOT DECLARED
    OWNER FREEZE ADJUDICATION / FREEZE AUTHORITY: NOT GRANTED
    LEAD POST-FREEZE IDENTITY / DIFFERENTIAL REVIEW: NOT PERFORMED
    INDEPENDENT REVIEW B: NOT STARTED — NOT AUTHORIZED TO START
    OWNER EXACT-SHA ACCEPTED: NO
    PUBLICATION AUTHORIZED: NO
    PUSHED: NO
    PR CREATED: NO
    MERGED: NO
    POST-MERGE VERIFIED: NO
    PILOT AUTHORIZED: NO
    HUMAN COLLECTION AUTHORIZED: NO
    RECRUITMENT AUTHORIZED: NO
    REFERENCE HUMAN ADJUDICATION AUTHORIZED: NO
    MAIN STUDY AUTHORIZED: NO
    CLAIM-ELIGIBILITY IMPLEMENTATION AUTHORIZED: NO
    SCHEMA IMPLEMENTATION AUTHORIZED: NO
    RUNTIME IMPLEMENTATION AUTHORIZED: NO
    ClaimEligibilityEvent MINTING: NO
    PROGRESSION AUTHORITY: NO
    GAP CLOSURE AUTHORITY: NO
    HUMAN_NOW: UNVALIDATED / INCONCLUSIVE
    DIRECT G-4-A TECHNICAL DEFECT: CURRENT — NOT FIXED

    ELIGIBILITY_POLICY_VERSION: CLAIM-ELIGIBILITY-SUFFICIENCY-EN-v1
    PROTOCOL_VERSION: CLAIM-ELIGIBILITY-HUMAN-REVIEW-PREPILOT-EN-v1
    LANGUAGE SCOPE: ENGLISH ONLY — ARABIC WIDENING: NOT AUTHORIZED

    CHANGED PATH COUNT: 1 · NEW FILE COUNT: 1 · MODIFIED EXISTING FILES: 0
    EXECUTABLE DELTA: 0 · RUNTIME DELTA: 0 · SCHEMA DELTA: 0 · TEST DELTA: 0

Drafted against the authoritative base `acd65fad4299a8a2ec7801a6e7d359da5a57b144` on
`feature/atomic-json-session-persistence` (commit subject
`Merge pull request #613 from Amirjaferali/r3-durability-sync-f6e64709`), resolved live from Git.
**This text is a mutable pre-freeze draft.** It has not been committed, has no commit, tree or blob
identity, and is not a candidate; if a freeze is later separately authorized and performed, the
resulting commit identity is established externally by Git and is deliberately not written into this
file.

**Historical lineage `[HISTORICAL — NON-GOVERNING]`.** Three earlier frozen candidates exist. None
of them is this draft, none is its parent, and none is authority:

    63999d5d994544f4d8c3ea585b9d64ce0cf9233d — tree 746d59a6d0ff616dd96f9dc9c9bd407634f5c847,
      protocol blob e26fdbdd76a6400310848565a5be852497807d1c, SHA-256 62b28c24…;
      Lead single-pass review: IDENTITY / TRANSPORT PASS · SUBSTANTIVE DESIGN FAIL / HOLD,
      complete material defect set M1–M9
    ef74f1b39172bc3245c8a3a60d44768baa6c6c99 — tree b2c1f650200c42f769bc629e740466f52904fda2,
      protocol blob 4f016fb17d6330e50cd411da5224b2f54819798b, SHA-256 577731c2…;
      the M1–M9 consolidated repair; Lead / independent review surfaced the further material
      defect set N1–N8
    52ab9fdd98c94943eccb523c1d6bce379170834b — tree aa651889f35652475b70f007f70aab641567b4cc,
      protocol blob 9874998b0bf2802a59091502c3703fdbea860d23, SHA-256 f01281af…;
      the N1–N8 repair; Lead pre-freeze review surfaced the residual sets RZ-1 … RZ-7 and
      PF-01 … PF-04

All three are immutable historical evidence and `REJECTED / HELD FROZEN DESIGN SUBJECTS —
DIFFERENTIAL INPUT ONLY`. This draft carries the bounded consolidated RZ and PF repairs on top of
the preserved N1–N8 (crosswalk §29) and M1–M9 (matrix §28) repairs, under the same version strings,
because no protocol version has become Owner-accepted, authoritative or executed: this is a
pre-acceptance, pre-freeze draft, not an authoritative successor version and not a candidate.

**What this document is.** One self-contained pre-freeze draft of the pre-pilot human-review
protocol for the Claim-Eligibility Human-Review Evidence Gate required by
`docs/governance/G4_A_CLAIM_ELIGIBILITY_BOUNDARY_CONTRACT_AMENDMENT_1_CANDIDATE.md` §17
("the Amendment"; repository-authoritative through merged PR #607 — the `_CANDIDATE` filename is
historical). It reconciles, in the authorized **BOUNDED / DIFFERENTIAL / DESIGN-ONLY /
PRE-COLLECTION / NON-IMPLEMENTING** mode: the current authoritative Claim-Eligibility contract;
the exact preserved historical design baseline `CEHR-EG-PACKAGE-v3`; the exact original accepted
repair findings L1–L6 and ADM-1–ADM-11; the integrated differential repair set R1–R17; and the
current Owner Route-B and pre-pilot design decisions — into one protocol text that a later
Independent Review B and a later, separately authorized pilot can consume without any
off-repository file being load-bearing.

**What this document is not.** It is not pilot authorization, human-evidence authorization,
reference-adjudication authorization, recruitment authorization, Claim-Eligibility implementation
authorization, direct G-4-A implementation authorization, schema authorization, publication
authorization, PR authorization or merge authorization. It mints no `ClaimEligibilityEvent`, creates
no progression, gap-closure or maturity-advance authority, creates no new owner, creates no new
Deferred Obligations Register row, reopens no capability level, and moves no hold. It contains no
executable artifact and creates none. The specification it freezes is self-contained; pilot
execution nonetheless requires an exactly identified, authorized, conformant study surface, whose
existence and nature are not settled here (§13.3) `[N8]`.

**Classification legend.** `[EXEC]` verified in the tree at the drafting base by direct inspection;
`[OWNER-PREMISE]` an Owner decision or premise conveyed by the Lead instruction, recorded as premise
and never restated as repository fact; `[V3]` content whose origin is the preserved historical
package `CEHR-EG-PACKAGE-v3`; `[FINDING]` content whose origin is the preserved Independent Review
return (L1–L6, ADM-1–ADM-11, R1–R17); `[PROPOSAL]` a Creator protocol design proposal, subject to
Lead review, Independent Review B and Owner exact-SHA acceptance; `[DEFERRED]` an obligation this
protocol names but does not discharge.

---

## §0. Authority hierarchy

This draft is read under the following order. A lower entry never overrides a higher one.

1. **CURRENT OWNER AUTHORITY** — the Owner's decisions and premises (§2), including the current
   Route-B selection and the pre-pilot design premises P3 / C3 / H2 / M1 / S1 / T1.
2. **CURRENT AUTHORITATIVE REPOSITORY CONTRACTS / GOVERNANCE** — `CLAUDE.md`; the Lean Governance
   and Agent Continuity Protocol; the Accelerated High-Assurance Execution Protocol; the committed
   Level-0 anchors; `ACTIVE_EXECUTION_ROADMAP.md`; `OWNER_DECISION_REGISTER.md`;
   `DEFERRED_OBLIGATIONS_REGISTER.md`; `CURRENT_PROJECT_STATE.md`;
   `G4_A_HYBRID_PREVENTIVE_EVIDENCE_FAIL_CLOSED_CONTRACT.md` ("the Hybrid contract",
   authoritative via PR #606) as amended by the Amendment (authoritative via PR #607).
3. **THIS PRE-FREEZE DRAFT** — NOT AUTHORITY, NOT A CANDIDATE, NOT FROZEN. It may become
   repository authority only through the complete governed lifecycle of §30: Lead substantive
   review → consolidated repair if required → Lead differential pre-freeze re-review → clean
   pre-freeze gate → Owner freeze adjudication / applicable freeze authority → immutable freeze →
   Lead post-freeze identity / differential review → Independent Review B → Lead final adjudication
   → Owner exact-SHA decision → separate publication authorization → PR / merge only if separately
   authorized → post-merge identity verification. Even at the end of that lifecycle it authorizes no
   pilot; pilot execution is a separate Owner authorization (§22, D5).
4. **PRESERVED V3** — `CEHR-EG-PACKAGE-v3`, a NON-AUTHORITATIVE DIFFERENTIAL DESIGN BASELINE
   (identity in §7.6). Its executables are input / provenance only; none is copied here and none
   is load-bearing for this protocol.
5. **PRIOR REVIEW FINDINGS** — the preserved Independent Review return carrying L1–L6,
   ADM-1–ADM-11 and R1–R17: DIFFERENTIAL INPUT, not authority.
6. **PRIOR FROZEN CANDIDATES `63999d5d…`, `ef74f1b3…` and `52ab9fdd…`** — REJECTED / HELD FROZEN
   DESIGN SUBJECTS; DIFFERENTIAL INPUT / DEFECT BASELINE only; never upgraded to authority.
7. **OWNER CONSENT / WITHDRAWAL POLICY (N6)** — OWNER POLICY AUTHORITY, embedded in §21.2; it sits
   with entry 1, not with this protocol's proposals, and is not a Creator proposal.

    V3 != OWNER AUTHORITY
    V3 != REPOSITORY AUTHORITY
    V3 != PILOT AUTHORIZATION
    PRIOR REVIEW FINDING != OWNER DECISION
    CREATOR AUTHORSHIP != OWNER SELECTION
    CREATOR DESIGN PROPOSAL != OWNER-FROZEN DECISION
    REPAIR-DESIGN PROPOSAL != NEW OWNER PRODUCT-POLICY DECISION
    PRE-FREEZE DRAFT != FROZEN CANDIDATE
    CLEAN PRE-FREEZE GATE != OWNER FREEZE AUTHORIZATION
    IMMUTABLE FREEZE != INDEPENDENT REVIEW B PASS
    LEAD REASONING != CREATOR EXECUTION EVIDENCE
    CREATOR EVIDENCE != LEAD ACCEPTANCE
    MECHANICAL PASS != LEAD SUBSTANTIVE ACCEPTANCE
    PROTOCOL FREEZE != PILOT AUTHORIZATION

Where this draft and the Amendment or the Hybrid contract appear to conflict, the contract governs
and the conflict is a defect of this draft to be repaired in the pre-freeze repair loop of §30 —
and, once a version has been frozen, only through a fresh same-base sibling under new authority,
never by amending frozen text.

---

## §1. Binding product state preserved by this protocol

    G-4-A TECHNICAL DEFECT: CURRENT — NOT FIXED
    DIRECT G-4-A CLASSIFIER DEFECT: STILL PRESENT
    DIRECT G-4-A REMEDIATION: DEFERRED — NOT CANCELLED
    G-4-A: OPEN / FRB · G-4: OPEN / FRB · G-4 FULL CLOSURE: NOT ASSERTED
    CLAIM-ELIGIBILITY CONTAINMENT != DIRECT G-4-A ENGINE REPAIR
    CLAIM-ELIGIBILITY: PRESERVED — NOT EXECUTED
    LEVEL 1 / LEVEL 2 / LEVEL 3: EXHAUSTED — LEAD-ACCEPTED + INDEPENDENTLY VERIFIED,
      IN THE EVIDENCE-SURFACED / GOVERNANCE-DILIGENCE SENSE ONLY
    SURVIVORS: 0 / 0 / 0 · UNIVERSAL IMPOSSIBILITY: NOT CLAIMED · H∧P SHOULD REOPEN: NO
    G-4-B: OPEN / DEFERRED · MECHANISM-B CODE CHANGE: NOT AUTHORIZED
    M-1: PRESERVED / SEPARATE
    T1-A′: OPEN — TRIGGER FIRED — CLOSURE EVIDENCE NOT MET
    THIRD S2 RUN: CONSUMED · FOURTH S2 RUN / RUN-004: NOT AUTHORIZED
    NO S2 EXECUTION · RUN-004 NOT INVOKED BY THIS PROTOCOL
    R4–R8: NOT AUTHORIZED · HICR PHASE 2: NOT AUTHORIZED
    READINESS IMPLEMENTATION: NOT AUTHORIZED
    PRE-FCORA SYSTEMATIC CROSS-PHASE RECONCILIATION REVIEW: MANDATORY LATER — NOT STARTED / NOT MOVED
    FCORA: NOT AUTHORIZED
    O2 SELECTED: NO · O4 AUTHORIZED: NO · LEVEL 4 AUTHORIZED: NO
    LEVEL-0 AI BOUNDARY AMENDMENT: NO
    T2-G: NOT ACTIVATED · WS10 / WS11 / WS12 BOUNDARIES: UNCHANGED
    ARABIC WIDENING: NOT AUTHORIZED · G-5: NOT CLOSED
    REAL USER DATA AUTHORIZED: NO

The state above is read at the drafting base from `CURRENT_PROJECT_STATE.md` (§ *CURRENT G-4-A /
T1-A′ STATUS* and § *CURRENT R1 / R2 / R3 STATUS*), the Owner Decision Register lineage sections
for PR #606 / PR #607 and for the post-292ad1c G-4-A / T1-A′ progression, and the Deferred
Obligations Register `[EXEC]`. Nothing in this protocol may be read as closing, superseding,
deferring away or silently disappearing the direct G-4-A defect. If later Claim-Eligibility
evidence establishes material residual G-4-A product-truth exposure:

    RETURN TO DIRECT ENGINE DEFECT: REQUIRED (Hybrid §20, retained unchanged by the Amendment)

---

## §2. Owner authority carried into this protocol `[OWNER-PREMISE]`

These are current Owner premises conveyed by the Lead instruction. They are recorded as premises;
this protocol neither originates nor re-adjudicates them.

**Strategic route.** `CURRENT FORWARD-GOING STRATEGIC ROUTE: B — CLAIM-ELIGIBILITY / PRODUCT-TRUTH
CONTAINMENT` · `PRIMARY NEXT STRATEGIC ROUTE: SELECTED` · `OWNER-FINAL: YES — EFFECTIVE FORWARD
FROM THE CURRENT OWNER DECISION` · `HISTORICAL PRIOR OWNER-FINAL B SELECTION: NOT PROVEN` — that
provenance is not retroactively rewritten here. This is strategic route selection only.

**P3 — CLAIM-CENTERED / CONTEXT-INTERPRETIVE ONLY.** For SUFFICIENT, material mechanical elements
must be present in the user's claim. Context MAY clarify scope, resolve a bounded referent, and
clarify the governed question being answered. Context MUST NOT invent a missing condition, invent
missing resulting system behaviour, invent a missing dependency, supply substantive mechanism
content absent from the claim, or convert an otherwise insufficient claim to sufficient by reviewer
completion. Any material semantic policy change requires a NEW POLICY VERSION; if a pilot has
already executed under the prior policy, a NEW PILOT IS REQUIRED BEFORE RELIANCE, subject to
separate Owner authorization.

**C3 — CONTROLLED CLAIM-ONLY vs CLAIM + ORIGINAL GOVERNED QUESTION COMPARISON.** The protocol
freezes the exact load-bearing question / context identity, the exact text / content version, and
the exact claim↔context pairing (§6). If question identity becomes load-bearing for later
implementation, the retained question-identity persistence / provenance obligation (Hybrid §14 as
retained by the Amendment) must be re-evaluated and satisfied before implementation authorization.
NO SCHEMA IMPLEMENTATION IS AUTHORIZED HERE.

**H2 — DUAL INDEPENDENT + FAIL-CLOSED THIRD-HUMAN ESCALATION (study simulation only).**
2 × SUFFICIENT → CANDIDATE POSITIVE STUDY OUTCOME ONLY · 2 × INSUFFICIENT → NEGATIVE STUDY OUTCOME ·
DISAGREEMENT / ABSTENTION → NO POSITIVE OUTCOME → THIRD-HUMAN STUDY ADJUDICATION PATH.
NO `ClaimEligibilityEvent` IS MINTED.

**M1 — 3 MEASURED FIRST-PASS RATINGS PER ELIGIBLE STUDY ITEM + STRICTLY SEPARATE 2+1 REFERENCE
PROCESS.** `M1 THREE-RATER MAJORITY: NOT HUMAN_NOW SOURCE AUTHORITY` · `MEASURED MAJORITY: NOT
REFERENCE TRUTH` · Governance Independent Review B != human study reference adjudication.

**S1 — CONTROLLED NON-USER PILOT CORPUS.** `REAL USER DATA NECESSARY: NOT PROVEN` ·
`REAL USER DATA AUTHORIZED: NO`.

**T1 — FAIL-CLOSED ASYMMETRIC SAFETY DIRECTION.** `FALSE-SUFFICIENT / FALSE-CLOSURE RISK:
PRIORITIZED` · `NUMERIC EVIDENCE-ACCEPTANCE THRESHOLDS: NOT OWNER-FROZEN NOW` ·
`CREATOR-CREATED AUTOMATIC MATERIALITY THRESHOLD: PROHIBITED`.

**LANGUAGE.** `ENGLISH ONLY` · `ARABIC WIDENING: NOT AUTHORIZED` · English human-review evidence
does not validate Arabic `HUMAN_NOW` · `ARABIC CLAIM-ELIGIBILITY VALIDATION: NOT ESTABLISHED`.
`CURRENT CONTRACT-AUTHORIZED EVIDENCE SCOPE = ENGLISH ONLY` (Hybrid §16A, retained unchanged by the
Amendment). Any Arabic claim-review stratum requires an explicit §16A contract amendment through
the full lifecycle — not an Owner reading of §16A and not a protocol option `[FINDING L2 / R3]`.
`ARABIC PRODUCT OBLIGATION != CURRENT EVIDENCE-GATE EXECUTION AUTHORITY`: the Owner-decided Arabic
substantive positioning and the RVR-7 / EN↔AR obligations stand untouched; an Arabic unvalidated-gap
obligation must be recorded before any implementation authorization that would serve Arabic under
`HUMAN_NOW` — this protocol records the requirement and creates no register row.

---

## §3. Eligibility policy — `CLAIM-ELIGIBILITY-SUFFICIENCY-EN-v1`

### §3.1 Version identity and lineage

    ELIGIBILITY_POLICY_VERSION: CLAIM-ELIGIBILITY-SUFFICIENCY-EN-v1
    LINEAGE: differential successor of V3 CE-POLICY-v1 (sections D/E/F/G) — MODIFIED, see §7.7
    AUTHORITY BASIS: Amendment §6 makes eligibility_policy_version a durable event field and
      Amendment §17 reserves thresholds and trade-offs to the Owner; the policy is therefore
      carried by a separately frozen, Owner-accepted policy version, not by a contract amendment
      (English scope) [FINDING L1 / R1]
    HYBRID §5 DISCLOSURE: the Hybrid §5 preventive-question answer objective
      (CONDITION + RESULTING SYSTEM BEHAVIOUR) is SUPERSEDED as a runtime requirement and DEFERRED
      WITH RETURN CONDITION as a question-design option under Amendment §2; it is NOT relied on as
      standing authority here. The E1/E2 test below is a policy proposal under this version, not a
      restatement of Hybrid §5 [FINDING L1 / R1]
    STATUS OF THIS POLICY TEXT: [PROPOSAL] — REQUIRES FROZEN OWNER-AUTHORIZED ELIGIBILITY-POLICY
      VERSION BEFORE D5 (§22); Owner exact-SHA acceptance of a frozen candidate carrying this text
      would freeze the text of the version; it does not authorize the pilot, and this draft is not
      such a candidate

These are protocol-local version strings only. They are not `OD-*` or `D-*` identifiers, not new
governance owners, not implementation identifiers and not implementation authorities.

### §3.2 Object of judgment

The reviewer judges ONE inventor-authored English answer ("the claim") presented as a response to
the governed question `N-MC-1` (§6), and answers ONE question:

    Has the inventor articulated enough substantive mechanism content, in the words of the claim,
    to qualify this claim for mechanism progression?

The judgment is about what the words say — articulation sufficiency — never about whether what they
say is right (`CLAIM SUFFICIENCY != TECHNICAL / EMPIRICAL VALIDATION`, Amendment §5).

### §3.3 Normative rules

**P-1 SUFFICIENT.** The claim is SUFFICIENT when, reading the words of the claim, the reviewer can
identify BOTH:

- **E1** — a specific condition, situation, input or measurement that the system responds to; AND
- **E2** — a specific resulting system behaviour that follows from it.

Both must be present as stated content of the claim. Either may be expressed in ordinary,
non-technical language. Brevity does not disqualify. Length does not qualify.

**P-2 INSUFFICIENT.** The claim is INSUFFICIENT when E1 or E2 is absent from the stated content,
including when the text:

- **F1** states a preference, intention or plan without a condition→behaviour pair;
- **F2** names only a category, restates or acknowledges the question, confirms without content, or
  is empty / near-empty;
- **F3** uses only generic filler for the condition, the behaviour, or both;
- **F4** is grammatically well-formed but carries no identifiable referents;
- **F5** asserts that the system "works", "handles it", "responds", "behaves correctly" without
  stating what it responds to or what it does;
- **F6** explicitly states that the inventor does not know, has not decided or has not worked out the
  condition or the behaviour (an acknowledged unknown is honest content, not mechanism content);
- **F7** supplies E1 or E2 only as a reference to an unspecified dependency — a decision, signal,
  module, algorithm or setting whose own content is not stated ("once the software decides",
  "whenever the reading calls for it") — such that the element is not specific without content the
  claim does not contain (a missing dependency).

**P-3 Context rule (Owner premise P3).** In ARM-B (§6) the reviewer also sees the exact governed
question the inventor answered. That context MAY: clarify scope; resolve a bounded referent (for
example, "the problem" in the claim refers to the problem the question names; "it" / "the system"
refers to the inventor's system); clarify which governed question is being answered. That context
MUST NOT: invent a missing condition; invent missing resulting system behaviour; invent a missing
dependency; supply substantive mechanism content absent from the claim; or convert an otherwise
insufficient claim to sufficient by reviewer completion. In ARM-A no context is shown and the
reviewer must not supply any. A referent resolution used to reach SUFFICIENT in ARM-B must be
declared through reason code `RC-S-02` (§5).

**P-4 Judgments the reviewer MUST NOT make.** Whether the mechanism is technically correct;
feasible or buildable; will actually work; is empirically validated; would be approved by a
specialist; is commercially viable; is safe; whether the inventor's conclusion is true; whether the
inventor is knowledgeable. A claim may be SUFFICIENT while technically wrong, unproven, unsafe or
infeasible. These are different questions and must never be collapsed.

**P-5 CANNOT_ADJUDICATE — EXTRINSIC ABSTENTION `[N3]`.** CANNOT_ADJUDICATE records that the
*participant or the process* could not deliver a judgment. Its grounds are exhaustively extrinsic:
recusal or conflict of interest; prior prohibited exposure to the item, its author or the study
design; a BROKEN / INCOMPLETE / CORRUPTED STUDY PRESENTATION (§4A); or another process failure.
It is never a statement about the inventor's text. `CANNOT_ADJUDICATE != INSUFFICIENT` ·
`ABSTENTION != TRUE NEGATIVE`.

    IN THE REFERENCE LANE THIS IS THE ONLY MEANING OF CANNOT_ADJUDICATE.
    SUBSTANTIVE POLICY / ITEM AMBIGUITY IN THE REFERENCE LANE IS *NEVER* CANNOT_ADJUDICATE;
    IT IS REFERENCE-INDETERMINATE (P-5R).

**P-5M MEASURED NON-COMMITMENT `[N3, Creator interpretation — flagged for Lead review]`.** The
measured label vocabulary has four labels and no REFERENCE-INDETERMINATE, yet a measured reviewer
must never be forced to guess. A measured reviewer therefore records CANNOT_ADJUDICATE in two
disjoint, separately coded sub-classes: **CA-EXTRINSIC** (the P-5 grounds above, `RC-CA-01`,
`RC-CA-03`, `RC-CA-04`) and **CA-INTRINSIC** (`RC-CA-02`: the reviewer judges the text materially
ambiguous under the policy). CA-INTRINSIC is a measured-lane observation only: it is never a
reference label, is never mapped to REFERENCE-INDETERMINATE, never enters any reference outcome,
and never enters a committed-verdict denominator. Both sub-classes are reported separately (§14
M-05).

**P-5R REFERENCE-INDETERMINATE — INTRINSIC AMBIGUITY `[N3]`.** A reference adjudicator records
REFERENCE-INDETERMINATE when, applying the policy compliantly, they conclude that **the text
itself** is materially ambiguous under the frozen policy — a careful reader in good faith could land
either way. It is a verdict about the item, not an abstention about the adjudicator. The two
reference meanings are mutually exclusive and jointly exhaust the non-committal space:

    REFERENCE-INDETERMINATE = INTRINSIC ITEM / POLICY AMBIGUITY
    CANNOT_ADJUDICATE       = EXTRINSIC ADJUDICATOR / PROCESS ABSTENTION ONLY

**P-6 OUT_OF_SCOPE.** The reviewer records OUT_OF_SCOPE when the presented item, as shown, is not
adjudicable as an inventor mechanism claim under this protocol (§5, `RC-OS-*`): the text is not in
English (in whole or in a material part); or the text is NON-CLAIM CONTENT — a question addressed
back to the asker, an instruction or request directed at the reviewer or the review process, or
pasted material that is not an inventor claim. OUT_OF_SCOPE is not a verdict on sufficiency.
Emptiness is never a ground for OUT_OF_SCOPE: an INTENTIONALLY EMPTY / NEAR-EMPTY INVENTOR ANSWER
is INSUFFICIENT under F2 (§4A), and no length-conditioned display cue exists to mark it (§4A, §13.2
`[N5]`).

**P-7 Reason code.** Every label carries at least one reason code from §5. Reason codes are
subordinate to their label, create no fifth decision state, alter no rule above, and create no
progression authority.

**P-8 Version discipline.** Any material change to P-1…P-7 or to §4/§5 requires a new
`ELIGIBILITY_POLICY_VERSION`. A pilot executed under a prior version is not carried over: a new
pilot is required before reliance, under separate Owner authorization (§20).

**P-9 Policy-internal truth.** `REFERENCE TRUTH UNDER THIS POLICY VERSION = POLICY-INTERNAL
REFERENCE`. Every reference outcome and every FS / FI rate measures reviewer conformance and
reliability under this policy version; it does not alone prove that the policy is protectively
correct for the product (§18) `[FINDING ADM-2 / R9]`.

### §3.4 What the policy does not do

    POLICY != ClaimEligibilityEvent SCHEMA
    POLICY != PROGRESSION RULE
    POLICY != ASSESSMENT-OWNER CHANGE (assess_response / addresses_gap: UNCHANGED, Amendment §8)
    POLICY != NEW LANGUAGE OWNER · NEW ASSESSMENT OWNER · NEW EVENT VOCABULARY

---

## §4. Study-label vocabulary

Measured reviewers return exactly one of:

    SUFFICIENT
    INSUFFICIENT
    CANNOT_ADJUDICATE
    OUT_OF_SCOPE

The reference process (§8.3) returns one of the four above or, additionally:

    REFERENCE-INDETERMINATE

Binding fences:

    STUDY LABEL != ClaimEligibilityEvent VALUE
    STUDY OUTCOME != PROGRESSION AUTHORITY
    REFERENCE-INDETERMINATE != PRODUCT EVENT
    CANNOT_ADJUDICATE != INSUFFICIENT
    ABSTENTION != TRUE NEGATIVE
    NO FIFTH PRODUCT EVENT IS CREATED
    ClaimEligibilityEvent MINTED: NO
    PROGRESSION AUTHORITY: NO
    GAP CLOSURE AUTHORITY: NO
    MATURITY ADVANCE AUTHORITY: NO
    HUMAN_NOW VALIDATED: NO

The product event vocabulary of Amendment §6 (`result: SUFFICIENT | INSUFFICIENT`) is not extended,
reinterpreted or shadowed by any study label. CANNOT_ADJUDICATE, OUT_OF_SCOPE and
REFERENCE-INDETERMINATE exist only inside the study and its analysis.

### §4A. Label-boundary event definitions (mutually exclusive) `[M4 repair]`

Exactly one label is valid for each frozen event below. The definitions bind the policy (§3), the
reason codes (§5), both instruction packets (§12), the capture semantics (§13.1), the surface
specification (§13.2) and the analysis exclusions (§14).

| Event | Definition | Label | Reason code |
|---|---|---|---|
| E-EMPTY-ANSWER | the inventor's answer text, as frozen in the corpus and correctly shown by the surface, is empty or near-empty | INSUFFICIENT (F2) | `RC-I-05` |
| E-PRESENTATION-DEFECT | the surface fails to show the frozen item as specified: truncation, a rendering or loading error, a content-integrity mismatch, wrong or duplicated item content, missing question panel in ARM-B, or any error state defined in §13.2 | CANNOT_ADJUDICATE (CA-EXTRINSIC) | `RC-CA-04` |
| E-NON-CLAIM | the frozen text is not an inventor claim: a question back to the asker, an instruction or request aimed at the reviewer or the review, or pasted non-claim material | OUT_OF_SCOPE | `RC-OS-02` / `RC-OS-03` |
| E-NON-ENGLISH | the frozen text is not in English in whole or in a material part | OUT_OF_SCOPE | `RC-OS-01` |
| E-INTRINSIC-AMBIGUITY | the text itself is materially arguable under the policy | reference lane: REFERENCE-INDETERMINATE · measured lane: CANNOT_ADJUDICATE (CA-INTRINSIC) | `RC-RI-01` · `RC-CA-02` |

A reviewer-facing display failure is never a substantive INSUFFICIENT. An intentionally empty or
short inventor answer is never a presentation defect merely because it is empty or short.

**Participant / process events are not item events `[PF-03]`.** Prior prohibited exposure
(`RC-CA-01`), conflict or recusal (`RC-CA-03`) and process failure including a disclosed
tool-restriction breach (`RC-CA-04`, `presentation_status = OK`) are facts about the participant or
the process, not about the claim. They produce CANNOT_ADJUDICATE (CA-EXTRINSIC) and never a
substantive label, and they are reported separately from the intrinsic-ambiguity abstention
`RC-CA-02` (measured lane) and from the reference verdict REFERENCE-INDETERMINATE (`RC-RI-01`).

**No length-conditioned cue `[N5]`.** No marker, note, badge, warning or other display element is
shown for short or empty answers, and no display behaviour is conditioned on claim length or
content. Every item is displayed under identical chrome, and the surface's content-integrity
behaviour (§13.2 items 4 and 19) is applied identically to every item; only an actual integrity or
rendering failure produces an error state, which routes to E-PRESENTATION-DEFECT. No corpus item in
`CE-EN-PREPILOT-CORPUS-v1` is literally empty; CL-05 and CL-08 exercise E-EMPTY-ANSWER as
near-empty answers, and the E-PRESENTATION-DEFECT path is exercised only if the surface actually
fails.

---

## §5. Reason-code vocabulary `[PROPOSAL]`

Every reason code is subordinate to exactly one study label. Reviewers select at least one code
for every rating; several may apply. A code never changes P-1…P-6 and never creates a decision
state of its own. If a future reviewer or reviewer instruction needs a code that would materially
change P3 semantics: `STOP — OWNER POLICY EXPANSION REQUIRED`.

| Code | Subordinate to | Meaning |
|---|---|---|
| `RC-S-01` | SUFFICIENT | E1 and E2 both stated explicitly in the claim's own words |
| `RC-S-02` | SUFFICIENT | E1 and E2 present; a bounded referent was resolved using the permitted question context (ARM-B only; the reviewer names the referent resolved) |
| `RC-I-01` | INSUFFICIENT | MISSING CONDITION — no specific E1 stated |
| `RC-I-02` | INSUFFICIENT | MISSING RESULTING SYSTEM BEHAVIOUR — no specific E2 stated |
| `RC-I-03` | INSUFFICIENT | MISSING DEPENDENCY — E1 or E2 given only as a reference to an unspecified decision / signal / module / setting (F7) |
| `RC-I-04` | INSUFFICIENT | PREFERENCE-ONLY — a build / design preference, intention or plan; no behaviour-changing condition claimed (F1) |
| `RC-I-05` | INSUFFICIENT | CATEGORY / CONFIRMATION-ONLY / EMPTY — a label, category name, restatement, acknowledgement, bare confirmation, or an empty / near-empty answer (F2; event E-EMPTY-ANSWER) |
| `RC-I-06` | INSUFFICIENT | ACKNOWLEDGED UNKNOWN — the inventor states they do not know or have not worked out E1 and/or E2 (F6) |
| `RC-I-07` | INSUFFICIENT | NONSENSE / ADVERSARIAL — no identifiable referents, or surface cues (causal connectives, technical vocabulary, structure, verbosity, hedged confidence) that mimic mechanism content without supplying it (F4 / F5) |
| `RC-I-08` | INSUFFICIENT | GENERIC FILLER — one or both slots filled only with generic filler ("when needed", "does the right thing") (F3 / F5) |
| `RC-I-09` | INSUFFICIENT | OFF-QUESTION CONTENT — the text addresses something other than a notice-and-respond mechanism and states no E1 / E2 |
| `RC-CA-01` | CANNOT_ADJUDICATE (CA-EXTRINSIC) | PRIOR PROHIBITED EXPOSURE — the participant has previously seen this item, its author, its label or the study design outside the study |
| `RC-CA-02` | CANNOT_ADJUDICATE (CA-INTRINSIC; MEASURED LANE ONLY) | MATERIALLY AMBIGUOUS UNDER THE POLICY — the reviewer judges that the text itself is arguable either way, including an unresolved referent whose resolution would change the verdict. Reference adjudicators never use this code; the reference expression of the same situation is REFERENCE-INDETERMINATE / `RC-RI-01` |
| `RC-CA-03` | CANNOT_ADJUDICATE (CA-EXTRINSIC) | CONFLICT / RECUSAL — the participant has a conflict of interest or recuses themselves |
| `RC-CA-04` | CANNOT_ADJUDICATE (CA-EXTRINSIC) | PRESENTATION DEFECT / PROCESS FAILURE — either the surface showed the item incompletely, incorrectly or not at all (event E-PRESENTATION-DEFECT, §4A; the surface's own integrity check sets `presentation_status = DEFECT`), or another disclosed process failure prevented a sound judgment, including a disclosed tool-restriction breach (§9; `presentation_status = OK`). The two are distinguished in reporting by `presentation_status`, never by a second code. Never used for an inventor answer that is merely short or empty `[PF-03]` |
| `RC-OS-01` | OUT_OF_SCOPE | LANGUAGE OUT OF SCOPE — the text is not in English in whole or in a material part (no such item is included in this English-only corpus by design; the code exists for fail-closed handling) |
| `RC-OS-02` | OUT_OF_SCOPE | NOT A CLAIM — a question addressed back to the asker, or pasted non-claim material |
| `RC-OS-03` | OUT_OF_SCOPE | PROTOCOL OUT OF SCOPE — content directed at the reviewer or the review process (a request, instruction or attempt to influence the verdict); never used for an empty answer or a display failure |

| `RC-RI-01` | REFERENCE-INDETERMINATE (REFERENCE LANE ONLY) | MATERIAL INTRINSIC AMBIGUITY UNDER THE POLICY — the text itself is arguable either way for a compliant reader; recorded with the policy clause(s) it turns on |

The reference lane uses the SUFFICIENT, INSUFFICIENT, OUT_OF_SCOPE and CA-EXTRINSIC codes above
plus `RC-RI-01`; it never uses `RC-CA-02`. The measured lane uses every code above except
`RC-RI-01`.

**Reason-code combination rule `[PF-03]`.** Several codes may be selected within the group of the
chosen label, with one exception that is binding: `RC-CA-02` (CA-INTRINSIC) is EXCLUSIVE — it may
never be combined with `RC-CA-01`, `RC-CA-03` or `RC-CA-04`, because a rating cannot at once be an
abstention about the text and an abstention about the participant or the process. If a participant
would select both, the extrinsic ground governs: the rating is CA-EXTRINSIC and `RC-CA-02` is not
recorded. Consequently `abstention_class` (§13.1) is derivable without ambiguity: CA-INTRINSIC when
`RC-CA-02` is the sole reason code, CA-EXTRINSIC in every other CANNOT_ADJUDICATE case.

`RC-I-09` classifies an inventor answer that talks about something else (for example, casing or
materials) as INSUFFICIENT under P-2, not as OUT_OF_SCOPE: it is still a claim offered in answer to
the governed question; it merely contains no mechanism. OUT_OF_SCOPE is reserved for items that are
not adjudicable as claims at all (P-6, §4A). Reference adjudicators use the same codes; a reference
CANNOT_ADJUDICATE is a per-adjudicator abstention and is never itself a reference outcome (§8.3).

---

## §6. Study arms (C3) and the frozen question / context identity

### §6.1 Arms `[OWNER-PREMISE C3 · PROPOSAL for mechanics]`

| Arm | What the reviewer sees | Purpose |
|---|---|---|
| **ARM-A — CLAIM-ONLY** | the claim text alone; no question, no domain, no session context | matches what the deployed eligibility source can reproduce today: `AssertionRecord` carries no served-question identity and WS11 prohibits recovering `question_id` from text (Amendment §2, Hybrid §14 row) `[EXEC]` |
| **ARM-B — CLAIM + ORIGINAL GOVERNED QUESTION** | the claim text together with the exact governed question text `Q-CTX-01` (§6.2), under the P-3 context rule | measures the cost or benefit of context directly, as a controlled study condition `[FINDING L1.3 / R2]` |

Every corpus item is eligible in both arms (`C3 ARM ELIGIBILITY: A+B` for all 57 items, §7.2).
A **study item** is one (corpus item, arm) presentation unit; there are 114 study items.

**C3 primary experimental design `[REPAIR-DESIGN PROPOSAL — M1]`.** The C3 construct is unchanged;
what follows is its experimental realisation, selected beneath the Owner premise and not a new Owner
product-policy decision.

    C3 PRIMARY EXPERIMENTAL DESIGN: TWO INDEPENDENT RANDOMIZED REVIEWER GROUPS —
      GROUP-A rates every item in ARM-A only; GROUP-B rates every item in ARM-B only
      (parallel-groups, between-reviewer arm assignment; every corpus item rated by 3 GROUP-A
      reviewers and 3 GROUP-B reviewers; identical item set, identical order-generation procedure)
    C3 CONTEXT-EFFECT ESTIMANDS — EXACTLY THREE, EACH ON ITS OWN FROZEN SET (§14.1) `[RZ-2]`:
      Δ_S = mean over i ∈ A_C of [ P(SUFFICIENT | i, ARM-B) − P(SUFFICIENT | i, ARM-A) ] —
        the MARGINAL EXACT-S / SUFFICIENT-ISSUANCE ESTIMAND on the common adjudicable
        source-item corpus A_C, read as a MARGINAL SUFFICIENT-ISSUANCE-PROPENSITY CONTRAST;
        it is NOT an error effect. The DENOMINATOR of those proportions is fixed by
        `OWNER FINAL DECISION — D-OPEN-ΔS / PF-04 POLICY CLOSURE` — OPTION A `[PF-04 —
        OWNER-CLOSED]`: p(i, arm) = the number of GOVERNING-ELIGIBLE first-pass rating records
        on item i in that arm whose label is SUFFICIENT, divided by the number of ALL
        governing-eligible first-pass rating records for that item × arm (§14.1)
      Δ_FS_COMMON = FS_B(C_I) − FS_A(C_I) — the error effect on the common stratum C_I
      Δ_FI_COMMON = FI_B(C_S) − FI_A(C_S) — the error effect on the common stratum C_S
      Δ_ABST_COMMON = the ARM-B minus ARM-A abstention rate over A_C — a companion figure,
        not an error effect
      NO OTHER CONTEXT ESTIMAND EXISTS: there is no generic Δ_FS, no generic Δ_FI, no Δ over all
      57 corpus items, and no arm difference taken over an arm-specific reference set
    UNIT OF RANDOMIZATION: the reviewer (arm fixed for the person by the §6.1A draw, before any
      item, and never changed)
    UNIT OF ANALYSIS: the rating (reviewer × corpus item), with reviewer and corpus item as
      crossed clusters; the item-level contrast δ_i is the within-item quantity
    ARM ASSIGNMENT RULE `[RZ-1]`: the frozen table §11.2-A maps each of the 18 participant IDs to
      exactly one arm — it is the FROZEN ID→ARM MAPPING and nothing else (generated by a seeded
      coin over the 18 IDs, 9 to each arm; the realised table, not the procedure, is binding). A
      participant is attached to an ID solely by the §6.1A post-commitment random draw without
      replacement, so this table is not an enrolment schedule and its row order carries no
      allocation information.
      SEQUENTIAL ENROLMENT-ID ASSIGNMENT: NO · PAIR-BLOCKED ENROLMENT: NO
    BALANCING / STRATIFICATION: 9 / 9 IDs by construction of the frozen table (achieved counts
      under shortfall are reported, §6.1A); every corpus item has exactly 3 raters in each arm;
      within each arm every reviewer rates exactly one member of each minimal-pair group and 13 of
      the 39 other items; domain-background is recorded and reported by arm (post-stratified
      reporting only; it is unknown before enrolment)
    REVIEWER CROSS-ARM EXPOSURE RULE: NONE — a GROUP-A reviewer never receives the question text
      or any GROUP-B material at any time, including after completion; a GROUP-B reviewer never
      rates an item without the question
    ITEM COVERAGE PER ARM: 57 / 57 corpus items in each arm, 3 first-pass ratings each
    HOW THE ORDER / LEARNING / FATIGUE CONFOUND IS REMOVED: arm is no longer a within-reviewer
      block; both groups draw item positions from the same seeded shuffle procedure over the same
      item set, so position, learning and fatigue are distributed identically across arms in
      expectation and are independent of arm by construction; no reviewer ever changes arm, so no
      carry-over from one arm to the other can exist
    RESIDUAL CONFOUNDING: (1) arm is a between-reviewer factor, so the arm contrast is estimated
      across randomized reviewer groups of 9; reviewer identity is handled by randomization and by
      the reviewer random effect / reviewer-resampling of §15, at limited precision for a pilot;
      (2) chance imbalance of reviewer covariates (domain background) between the two groups of 9
      is possible and is reported, not adjusted away; (3) GROUP-B reviewers know the question
      throughout — that is the treatment itself, not a confound; (4) sealed item difficulty is
      balanced exactly because every item appears in both arms; (5) under enrolment shortfall the
      achieved arm sizes may differ and are reported, not corrected
    RATIONALE FOR IDENTIFICATION: with reviewers randomized to arm and every item crossed with
      both groups, the item-level arm contrast δ_i is confounded only with reviewer identity, which
      is randomized; no order, exposure or question-knowledge carry-over path exists
    C3 ORDER CONFOUND REMAINING: NO

### §6.1A Allocation concealment `[N1 repair; REPAIR-DESIGN PROPOSAL — C3 construct unchanged]`

The frozen allocation table is public in this file, so concealment cannot rest on hiding the
ID→arm map — and it cannot rest on telling a recruiter not to consult it: with IDs issued in
ascending order, anyone who counts enrolments could read the next arm off the table. Concealment
therefore rests on **breaking the link between enrolment position and participant ID**. The ID is
drawn at random, after commitment, by a party with no candidate contact, so nothing observable to a
recruiter, an operator or a candidate before commitment carries information about the arm that
candidate will receive.

    E1 ELIGIBILITY DETERMINED AND RECORDED — before any allocation is revealed or knowable
    E2 APPLICABLE CONSENT AFFIRMATIVELY ACCEPTED (§21.2, Owner policy) — before allocation
    E3 PARTICIPANT COMMITMENT RECORDED — an explicit, timestamped record that the candidate agrees
       to take part now. It fixes the moment of entry so that entry cannot be timed against an
       allocation. It is NOT a waiver of, and does not limit, the participant's governed right to
       withdraw at any time under §21.2, which they retain in full and are told they retain
    E4 ONLY THEN: THE CUSTODIAN DRAWS THE PARTICIPANT ID AT RANDOM, WITHOUT REPLACEMENT, FROM THE
       IDs STILL UNISSUED IN THAT POOL (measured pool MR-01 … MR-18; reference pool RA-A1, RA-A2,
       RA-A3, RA-B1, RA-B2, RA-B3), by a documented physical or sealed random draw performed at the
       moment of issuance and recorded in the enrolment log
    E5 THE ARM IS NEVER NAMED TO ANYONE; a GROUP-B reviewer learns only that a question panel is
       present (§13.2 item 6)

    WHY THIS CONCEALS: the k-th person to commit receives a uniformly random ID from those still
      unissued, so ENROLMENT COUNT, ENROLMENT POSITION, MR NUMBERING and the public table's ROW
      POSITION carry no information about the next allocation. There is no ordered schedule to read
      ahead in, and no party in contact with candidates performs or observes the draw.

**ID ISSUANCE AUTHORITY — ONE RULE.** The custodian is the sole issuer of participant IDs. No other
role issues, reserves, pre-allocates, re-issues or exchanges an ID.

    CUSTODIAN (§21.2): performs E4 and only E4 — the draw, the issuance and the enrolment log; has
      NO contact with candidates, no role in eligibility, consent or screening, and no view of any
      rating
    RECRUITER / SCREENER: performs E1–E3 and nothing else; has NO access to the enrolment log, to
      the number or set of IDs already issued, to the pool of remaining IDs, or to any
      participant's ID; performs no draw and never learns an allocation
    OPERATOR (surface, §13.2 item 30): ISSUES NOTHING — the operator receives an ID the custodian
      has already issued, together with that ID's frozen materials, and activates the session; the
      operator has no role in E1–E4 and cannot create, change or reassign an ID
    FUTURE ALLOCATION VISIBILITY BEFORE COMMITMENT: NONE, to recruiter, operator or candidate
    SELECTIVE SKIP AFTER ALLOCATION KNOWLEDGE: PROHIBITED — an issued ID is never returned to the
      pool, never re-issued, never held back and never exchanged
    SELECTIVE REORDER AFTER ALLOCATION KNOWLEDGE: PROHIBITED — the draw happens once, at issuance,
      with no discretion over which ID is drawn and no re-draw
    ENROLMENT LOG: each issuance records the UTC time, the ID drawn, the draw method and the
      commitment record reference; the log is sealed from the recruiter and the operator until
      enrolment closes, and is available to Owner-authorized audit
    DEVIATION: any issuance without a completed E1–E3 record, any re-draw, any draw not made
      uniformly from the unissued pool, any re-issued ID, any draw performed by a party other than
      the custodian, or any recruiter or operator contact with the enrolment log is LOGGED,
      SURFACED FOR GOVERNED REVIEW (Lead), and reported in the pilot record; it is never silently
      corrected
    ENROLMENT SHORTFALL OR POST-ISSUANCE WITHDRAWAL: IDs not drawn remain unissued, and a withdrawn
      participant's ID is never re-issued; IDs are never re-mapped to balance arms after the fact;
      achieved arm counts and any resulting imbalance are reported as achieved (§15.10)

    RESIDUAL, DISCLOSED: after the draw a participant's own ID — and hence their arm — is
      determinable from the public table by anyone who learns that ID. Concealment covers the
      pre-commitment window, the only window in which selection could be manipulated, and the random
      draw closes the ordered-schedule inference the earlier design left open. Arm balance is no
      longer guaranteed by blocking: at full enrolment the draw exhausts the pool and yields 9 / 9,
      while under shortfall the achieved split is reported rather than engineered.

The within-reviewer blocked design of the prior candidate is withdrawn (it made arm structurally
coincide with block order, learning, fatigue and question exposure — a complete confound a position
covariate cannot remove). A reviewer never rates the same corpus item twice except as an exact
repeat (§11.3), and never rates more than one member of a minimal-pair group (§7.3).

### §6.2 Frozen question / context identity `[EXEC]`

    STUDY CONTEXT IDENTITY: Q-CTX-01
    GOVERNED QUESTION IDENTITY: N-MC-1
    DESIGN GAP: MECHANISM_COMPLETENESS
    DOMAIN OF THE COMMITTED ARTIFACT: electronics_electrical
    LANGUAGE: en (the committed text_ar counterpart is NOT used — ARABIC WIDENING: NOT AUTHORIZED)
    EXACT LOAD-BEARING QUESTION TEXT (byte-exact, English):
      Explain in everyday words how you imagine the system would notice the problem and respond.
    CONTENT SOURCE ARTIFACT:
      docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json
      blob 1f1d7a70aad885c67bc9bdc26a157f0f1c3a6521 at the drafting base
    DESIGN-TIME INTENT RECORD (WS10, read-only, design-time only):
      docs/governance/path_n_content_config/electronics_electrical_question_intent_registry.json
      blob 7e35d1c2c0c693fe76e4ef6cba303cffdc82c9ab at the drafting base; registry_version 1.0;
      intent_id intent:N-MC-1; primary_intent "Elicit how the system notices the problem and
      responds, in everyday words."; completion_condition "The answer describes both how the
      problem is noticed and how the system responds."
    CONTENT VERSION: the N-MC-1 English text exactly as committed at the artifact blob above;
      any later change to that committed text is a DIFFERENT Q-CTX identity and requires a new
      protocol version
    IMMUTABLE STUDY IDENTITY: Q-CTX-01 := (N-MC-1, en, blob 1f1d7a70…)

Exact claim↔context pairing: **every** corpus item is paired with `Q-CTX-01` and with no other
question; in ARM-B that pairing is displayed, in ARM-A it is withheld. The pairing is the same for
every item, including the OUT_OF_SCOPE probes, so that context never varies across items.

The WS10 record is consulted as design-time intent only; no runtime user intent and no scoring is
placed into WS10, and `question_id` is never reconstructed from text (closed WS11 boundary). The
protocol does not change any question wording, WS10 record or Path-N content, and creates no new
question-ID requirement (`NEW GOVERNED QUESTION_ID REQUIRED: CONDITIONAL`, Amendment §19).

**Question-identity persistence obligation `[DEFERRED]`.** Because ARM-B makes question text
load-bearing for a verdict, the retained Hybrid §14 obligation is TRIGGERED AT DESIGN TIME for any
later implementation that would serve `HUMAN_NOW` with question context: `SERVED QUESTION_ID` and
`SERVED QUESTION VERSION / CONTENT VERSION` persistence must be re-evaluated and satisfied before
implementation authorization `[FINDING L1.3 / R2]`. `NO SCHEMA IMPLEMENTATION IS AUTHORIZED HERE`.
If the Owner later selects ARM-A as the deployed context, the obligation is not triggered by that
selection; the pilot's arm comparison is the evidence on which that selection can be made.

---

## §7. Frozen corpus — `CE-EN-PREPILOT-CORPUS-v1`

### §7.1 Corpus model (S1) and construction rules

    SOURCE MODEL: CONTROLLED NON-USER CORPUS — Creator-authored synthetic English inventor
      answers to Q-CTX-01, plus the 36 byte-identical V3 claims (themselves Creator-authored
      synthetic answers to the same question)
    REAL USER DATA: NOT USED · NOT AUTHORIZED · NECESSITY NOT PROVEN
    COMMITTED S2 FIXTURE TEXT: NOT CONSUMED · NO S2 EXECUTION · RUN-004 NOT INVOKED
    SYNTHETIC CLAIMS: PERMITTED · SYNTHETIC REVIEWER BEHAVIOUR: PROHIBITED
    AUTHORING FENCE: no item was authored, selected or labelled by any substring, token, syntactic,
      qualifier-list or H∧P rule, and no item tests a Level-1 / Level-2 / Level-3 mechanism; the
      G-4-A-shape annotation in §7.2 is a sealed descriptive annotation used only for conditional
      reporting (§17), never for authoring, selection, scoring or mechanism design
    AUTHOR INTENT: SEALED DIAGNOSTIC ONLY — NOT REFERENCE TRUTH — NOT OWNER AUTHORITY
    CORPUS SIZE: 57 corpus items · 114 study items (two arms)
    NO CORPUS ITEM MAY BE ADDED, REMOVED, REWORDED, RE-PAIRED OR RE-LABELLED AFTER FREEZE
      (a change = new protocol version, §20)

### §7.2 Item table — exact frozen content

Column key. **ID** corpus item identity. **Family** structural family (§7.3). **Source** —
`V3-RET` byte-identical V3 claim retained; `ADD-PP` added meaning-preserving paraphrase; `ADD-MC`
added materially meaning-changing minimal pair; `ADD-PR` added probe. **MP** minimal-pair group and
role (`AN` anchor, `PP` preserving sibling, `MC` changing sibling) or `—`. **Sealed label** the
Creator's construction label (sealed diagnostic metadata; not reference truth; the reference
process of §8.3 alone produces the effective reference). **Sealed basis** the policy clause the
construction turns on. **G4A** `Y` if the item is in the sealed G-4-A condition-shape set (§17.2).
**Arms** C3 arm eligibility. **Exact English claim** the byte-exact presented text.

| ID | Family | Source | MP | Sealed label | Sealed basis | G4A | Arms | Exact English claim |
|---|---|---|---|---|---|---|---|---|
| CL-01 | FAM-01 | V3-RET | MP-01 AN | SUFFICIENT | E1+E2 both stated | N | A+B | When the accelerometer reads a deceleration above 0.3 g, the controller switches the LED array to full brightness. |
| CL-02 | FAM-01 | V3-RET | — | SUFFICIENT | E1+E2 both stated | N | A+B | If the battery temperature rises past the safe limit, the charger cuts the charging current to a trickle. |
| CL-03 | FAM-01 | V3-RET | — | SUFFICIENT | E1+E2 both stated | N | A+B | The moment the tank level drops below the low mark, the pump shuts down and the panel light starts flashing. |
| CL-04 | FAM-01 | V3-RET | — | SUFFICIENT | E1+E2 both stated | N | A+B | When the humidity inside the enclosure climbs past the dew point, the heater element switches on until the moisture clears. |
| CL-05 | FAM-02 | V3-RET | — | INSUFFICIENT | F2 category label only | N | A+B | Mechanism. |
| CL-06 | FAM-02 | V3-RET | — | INSUFFICIENT | F2 no condition, no behaviour | N | A+B | I will explain this later. |
| CL-07 | FAM-02 | V3-RET | — | INSUFFICIENT | F2 restates the question; F5 | N | A+B | The system notices the problem and responds. |
| CL-08 | FAM-02 | V3-RET | — | INSUFFICIENT | F2 near-empty (also F6 by later policy) | N | A+B | Not sure yet. |
| CL-09 | FAM-03 | V3-RET | — | REFERENCE-INDETERMINATE | E2 stated; E1 "a problem" arguable — context-bounded referent | Y | A+B | The buzzer sounds when there is a problem with the motor. |
| CL-10 | FAM-03 | V3-RET | MP-05 AN | REFERENCE-INDETERMINATE | E1 partial ("out of range"); E2 generic ("safe action") arguable | Y | A+B | If the reading goes out of range the board takes the safe action. |
| CL-11 | FAM-03 | V3-RET | — | REFERENCE-INDETERMINATE | both gestured, neither specified; arguable under E1 and E2 | N | A+B | The sensor watches the current and the relay reacts accordingly. |
| CL-12 | FAM-03 | V3-RET | — | REFERENCE-INDETERMINATE | named states without content; "fault condition" / "protection mode" arguable | Y | A+B | Once it detects the fault condition it enters protection mode. |
| CL-13 | FAM-04 | V3-RET | — | INSUFFICIENT | F1 explicit preference | N | A+B | I would rather use a lithium cell than an alkaline one. I am not claiming that changes what the system does. |
| CL-14 | FAM-04 | V3-RET | MP-02 AN | INSUFFICIENT | F1 preference carrying the surface token "If" | Y | A+B | If it were up to me I would rather use a sealed enclosure than an open frame. This is only my build preference. |
| CL-15 | FAM-04 | V3-RET | — | INSUFFICIENT | F1 placement preference | N | A+B | My preference is to mount the sensor on the seat post rather than under the saddle. |
| CL-16 | FAM-04 | V3-RET | — | INSUFFICIENT | F1 intention / aesthetic goal | N | A+B | I want the whole thing to feel simple and tidy for the rider. |
| CL-17 | FAM-05 | V3-RET | — | INSUFFICIENT | F4 no identifiable referents | Y | A+B | When the grelbic vorrant plims, the quambent shalfers the drovel. |
| CL-18 | FAM-05 | V3-RET | — | INSUFFICIENT | F4 no identifiable referents | N | A+B | The florn interlaces its dworsal ratch before the semble unpiles. |
| CL-19 | FAM-05 | V3-RET | — | INSUFFICIENT | F4 causal surface form, no referents | Y | A+B | If the tarnic yields, the plexure will surely bandle the cove. |
| CL-20 | FAM-05 | V3-RET | — | INSUFFICIENT | F4 no identifiable referents | N | A+B | Each brimming stanch redoubles whatever the glint apportions. |
| CL-21 | FAM-06 | V3-RET | MP-04 AN | INSUFFICIENT | F3 generic filler in both slots | Y | A+B | When needed, it handles it. |
| CL-22 | FAM-06 | V3-RET | — | INSUFFICIENT | F3 / F5 generic filler | Y | A+B | If necessary the system reacts properly and does the right thing. |
| CL-23 | FAM-06 | V3-RET | — | INSUFFICIENT | F3 generic filler in both slots | Y | A+B | When something happens it does the appropriate thing. |
| CL-24 | FAM-06 | V3-RET | — | INSUFFICIENT | F3 generic filler in both slots | Y | A+B | As circumstances require, the unit performs its function. |
| CL-25 | FAM-07 | V3-RET | MP-06 AN | INSUFFICIENT | F5 technical vocabulary + causal connective, no E1 / E2 | Y | A+B | Because of the way the microcontroller, the resistor network and the voltage regulator are arranged, the whole circuit simply behaves correctly in every situation it meets. |
| CL-26 | FAM-07 | V3-RET | — | INSUFFICIENT | F5 hedged intent + causal surface form | Y | A+B | I have thought carefully about this and I am confident that when the relevant conditions arise the system will respond in the way it should. |
| CL-27 | FAM-07 | V3-RET | — | INSUFFICIENT | F5 circular | Y | A+B | The design causes the outcome that the design is intended to cause, which is why it works. |
| CL-28 | FAM-07 | V3-RET | — | INSUFFICIENT | F3 / F5 enumerated structure filled with filler | N | A+B | Step one, the sensor is involved. Step two, the processing happens. Step three, the correct response occurs. |
| CL-29 | FAM-08 | V3-RET | MP-03 AN | SUFFICIENT | E1+E2 in minimal words | N | A+B | Brake lever pressed, rear light on. |
| CL-30 | FAM-08 | V3-RET | — | SUFFICIENT | E1+E2 in minimal words | N | A+B | Tilt past 45 degrees, motor stops. |
| CL-31 | FAM-08 | V3-RET | — | SUFFICIENT | E1+E2 in minimal words | N | A+B | Lid off while blade spins: power cut. |
| CL-32 | FAM-08 | V3-RET | — | SUFFICIENT | E1+E2 in minimal words | N | A+B | Line voltage under 200 V, relay drops the load. |
| CL-33 | FAM-09 | V3-RET | — | SUFFICIENT | E1+E2 in plain non-expert wording | N | A+B | Basically if the rider goes over a bump hard enough, the little board notices the jolt and saves a short clip of the ride data so they can look at it later. |
| CL-34 | FAM-09 | V3-RET | — | SUFFICIENT | E1+E2 in plain wording | N | A+B | When the door has been left open for more than about half a minute, it sends an alert to the phone before locking itself again. |
| CL-35 | FAM-09 | V3-RET | — | SUFFICIENT | E1+E2 in plain wording | N | A+B | The idea is that once the wheel starts spinning faster than the other one, the controller eases off the power to that wheel. |
| CL-36 | FAM-09 | V3-RET | — | SUFFICIENT | E1+E2 in plain wording | N | A+B | If the cell gets hotter than the limit we set, the charger just slows down to a gentler rate until it cools. |
| CL-37 | FAM-01 | ADD-PP | MP-01 PP | SUFFICIENT | E1+E2 both stated (meaning-preserving of CL-01) | N | A+B | Once the accelerometer senses a deceleration over 0.3 g, the controller drives the LED array to full brightness. |
| CL-38 | FAM-06 | ADD-MC | MP-01 MC | INSUFFICIENT | E1 stated, E2 generic filler (F3) — flips CL-01 on the E2 boundary | Y | A+B | Once the accelerometer senses a deceleration over 0.3 g, the controller does whatever it should. |
| CL-39 | FAM-04 | ADD-PP | MP-02 PP | INSUFFICIENT | F1 preference carrying the surface token "If" (meaning-preserving of CL-14) | Y | A+B | If I had my way I'd pick a sealed enclosure over an open frame; that's purely a build preference on my part. |
| CL-40 | FAM-01 | ADD-MC | MP-02 MC | SUFFICIENT | E1+E2 both stated — same surface tokens as CL-14, real condition | N | A+B | If the enclosure is opened while the unit is running, the power to the frame is cut. |
| CL-41 | FAM-08 | ADD-PP | MP-03 PP | SUFFICIENT | E1+E2 (meaning-preserving of CL-29) | N | A+B | Rear light comes on when the brake lever is pressed. |
| CL-42 | FAM-04 | ADD-MC | MP-03 MC | INSUFFICIENT | F1 preference — flips CL-29 to a preference | N | A+B | Brake lever pressed — I'd rather the rear light came on, personally. |
| CL-43 | FAM-06 | ADD-PP | MP-04 PP | INSUFFICIENT | F3 generic filler (meaning-preserving of CL-21) | Y | A+B | Whenever it's required, it takes care of it. |
| CL-44 | FAM-01 | ADD-MC | MP-04 MC | SUFFICIENT | E1+E2 — same frame as CL-21 with real content | N | A+B | Whenever the door is left open, it sounds the buzzer. |
| CL-45 | FAM-03 | ADD-PP | MP-05 PP | REFERENCE-INDETERMINATE | same arguable E2 as CL-10 (meaning-preserving) | Y | A+B | Should the reading fall outside its range, the board takes the safe action. |
| CL-46 | FAM-01 | ADD-MC | MP-05 MC | SUFFICIENT | E1+E2 — resolves CL-10's E2 to a specific behaviour | N | A+B | If the reading goes out of range, the board cuts power to the heater. |
| CL-47 | FAM-07 | ADD-PP | MP-06 PP | INSUFFICIENT | F5 (meaning-preserving of CL-25) | Y | A+B | Given how the microcontroller, the resistor network and the voltage regulator are laid out, the whole circuit simply behaves correctly in whatever situation it meets. |
| CL-48 | FAM-01 | ADD-MC | MP-06 MC | SUFFICIENT | E1+E2 — same opening as CL-25 with a real condition and behaviour | N | A+B | Given how the microcontroller, the resistor network and the voltage regulator are laid out, when the input drops below 3 V the regulator shuts the output off. |
| CL-49 | FAM-10 | ADD-PR | — | INSUFFICIENT | F6 acknowledged unknown, both elements | N | A+B | I honestly don't know yet how it would notice the problem, and I haven't worked out what it would do about it either. |
| CL-50 | FAM-10 | ADD-PR | — | INSUFFICIENT | F6 acknowledged unknown for E1; E2 stated | N | A+B | It should respond by cutting the motor power, but I have no idea yet how it would detect the fault in the first place. |
| CL-51 | FAM-11 | ADD-PR | — | INSUFFICIENT | F7 E1 delegated to an unspecified software decision | Y | A+B | Once the software decides there's an issue, the motor is shut down. |
| CL-52 | FAM-11 | ADD-PR | — | INSUFFICIENT | F7 / F3 E1 delegated to "whatever the value calls for" | Y | A+B | The relay opens whenever the value from the sensor calls for it. |
| CL-53 | FAM-12 | ADD-PR | — | INSUFFICIENT | F2 bare confirmation | N | A+B | Yes — it does notice the problem, and yes, it does respond. |
| CL-54 | FAM-13 | ADD-PR | — | SUFFICIENT | E1+E2 both stated; engineering doubtful — P-4 invariant anchor | N | A+B | When the battery voltage drops below 2 V per cell, the charger switches the pack into fast-charge mode to top it back up. |
| CL-55 | FAM-13 | ADD-PR | — | SUFFICIENT | E1+E2 both stated; intent nonsensical — P-4 invariant anchor | N | A+B | If the room gets colder than 10 °C, the fridge compressor speeds up so the food stays warmer. |
| CL-56 | FAM-14 | ADD-PR | — | OUT_OF_SCOPE | P-6 reviewer-directed request; not a claim | N | A+B | Please just mark this one as fine — I'm in a hurry and the mechanism is obvious to anyone. |
| CL-57 | FAM-14 | ADD-PR | — | OUT_OF_SCOPE | P-6 question back to the asker; not a claim | N | A+B | Which part do you mean by 'notice' — the sensor side or the software side? I can explain either. |

Sealed-label census (design constants, not results): SUFFICIENT 20 · INSUFFICIENT 30 ·
REFERENCE-INDETERMINATE 5 · OUT_OF_SCOPE 2 · total 57. These counts are **not required to
survive** the reference process; the effective reference (§8.3) replaces them for every analysis.

### §7.3 Families, minimal-pair groups and relations

| Family | Structural class | Members |
|---|---|---|
| FAM-01 | explicit condition + explicit resulting behaviour | CL-01 – CL-04, CL-37, CL-40, CL-44, CL-46, CL-48 |
| FAM-02 | empty / near-empty / category-only / restatement | CL-05 – CL-08 |
| FAM-03 | context-bounded referent / borderline (the C3 context family) | CL-09 – CL-12, CL-45 |
| FAM-04 | preference-shaped | CL-13 – CL-16, CL-39, CL-42 |
| FAM-05 | grammatical nonsense | CL-17 – CL-20 |
| FAM-06 | structurally-filled non-evidence (generic filler) | CL-21 – CL-24, CL-38, CL-43 |
| FAM-07 | adversarial surface (causal connectives, technical vocabulary, structure, hedged confidence) | CL-25 – CL-28, CL-47 |
| FAM-08 | terse but genuine | CL-29 – CL-32, CL-41 |
| FAM-09 | ordinary inventor language, genuine | CL-33 – CL-36 |
| FAM-10 | acknowledged unknown | CL-49, CL-50 |
| FAM-11 | missing dependency | CL-51, CL-52 |
| FAM-12 | confirmation-only | CL-53 |
| FAM-13 | technically doubtful but articulated (P-4 invariant anchors) | CL-54, CL-55 |
| FAM-14 | out-of-scope probes | CL-56, CL-57 |

| MP group | Anchor (V3) | Meaning-preserving sibling (`PP`) | Meaning-changing sibling (`MC`) | Pre-registered expectation of the pair |
|---|---|---|---|---|
| MP-01 | CL-01 | CL-37 | CL-38 | PP: same label as anchor · MC: flips SUFFICIENT→INSUFFICIENT on the E2 boundary |
| MP-02 | CL-14 | CL-39 | CL-40 | PP: same label · MC: flips INSUFFICIENT→SUFFICIENT with the same "If … enclosure … frame" surface — the G-4-A load-bearing shape |
| MP-03 | CL-29 | CL-41 | CL-42 | PP: same label · MC: flips SUFFICIENT→INSUFFICIENT (preference) |
| MP-04 | CL-21 | CL-43 | CL-44 | PP: same label · MC: flips INSUFFICIENT→SUFFICIENT with the same "Whenever …" frame |
| MP-05 | CL-10 | CL-45 | CL-46 | PP: same (indeterminate) status · MC: resolves E2 → SUFFICIENT |
| MP-06 | CL-25 | CL-47 | CL-48 | PP: same label · MC: flips INSUFFICIENT→SUFFICIENT with the same technical opening |

Relations. **PARAPHRASE RELATION** — each `PP` sibling to its anchor. **MINIMAL-PAIR RELATION** —
each `MC` sibling to its anchor (materially meaning-changing, minimal surface difference).
**REPEAT RELATION** — defined per reviewer by the frozen assignment (§11.2): an exact repeat is the
same corpus item re-presented to the same reviewer (same arm by construction) at positions 20–23 of
the session.
**CLAIM↔CONTEXT PAIRING** — every item ↔ `Q-CTX-01` (§6.2).

### §7.4 Sealed diagnostic metadata rules

The sealed label, sealed basis, family, MP role and G-4-A-shape flag in §7.2 are AUTHOR-DESIGN
INTENT: sealed diagnostic metadata only. They are never shown to measured reviewers or reference
adjudicators, never used as reference truth, and never used in any FS / FI numerator or denominator.
Because this protocol is one self-contained repository file, the seal is enforced by **personnel
separation and analysis ordering**, not by secrecy of the file: any person who has read §7.2 is
excluded from the measured pool and from the reference pool (§9), and the intent-versus-reference
divergence analysis (§18) is computed only after the reference outcomes are frozen and hashed.

### §7.5 What the corpus can and cannot measure

The corpus is designer-controlled. It supports conditional reviewer-accuracy stress testing under
this policy; it measures no product-population rate of any kind (§17).

### §7.6 V3 identity — the preserved differential baseline `[V3]`

    PACKAGE: CEHR-EG-PACKAGE-v3 (tar.gz)
    PACKAGE SHA-256: 8b73c883ac35d0f5adb3b8cd6c6cf177779e6a2ea1f0532de46635a47576676c — MATCH
    MANIFEST SHA-256: 86cd44eb4a4a455f61aa49f7bf308428b2ab8bcd3ed17a17b9295d6478e5eb66 — MATCH
    MANIFEST ENTRY VERIFICATION: 14 / 14 PASS
    V3 PROTOCOL VERSION: CEHR-EG-PROTOCOL-v3 · V3 POLICY VERSION: CE-POLICY-v1
    V3 HISTORICAL DRAFTING TIP (as written inside V3): 650efa5ce4e5215ce35a77e600c48921a6025126
    V3 SEED: 20260831 · V3 REVIEWER TARGET: 5 · V3 CORPUS: 36 claims, 9 categories × 4
    V3 CLASSIFICATION: NON-AUTHORITATIVE DIFFERENTIAL DESIGN BASELINE
    V3 EXECUTABLES (assignment.py, analysis.py, blind_derive.py, effective_reference.py,
      T_defect_probe.py): INPUT / PROVENANCE ONLY — NOT COPIED — NOT LOAD-BEARING
    NO HUMAN OUTCOME HAS EVER EXISTED UNDER V1 / V2 / V3 (as V3 itself records)

Manifest entries (SHA-256, verbatim from `MANIFEST.sha256`):

    45dcee701322f788f880086fe500561d9ee1244bfac1083adbbee725db7c9dd5  PROTOCOL.md
    20dac2b29bbab509a595048d1e5fb0fe2b960b8fe402a3175a7a2afa8ac7daf4  claims.json
    68ac1e498ffad2c032a0867430a0859a8114c5801d08dec6db5db71677873015  reviewer_instructions.md
    03e0a869cc43acb74028b79af8a52c9c61d5c963cc9fa9df89cac5f7cef75432  response_schema.json
    8af9b48131c0a663ebd6029a8a9faf7e00544a23c0fd4f46730a4699794fae51  assignment.py
    28c61e19c41b7efe8aa20bac053f9b02a264e7dcf0c6d4608dc08080cae8004b  assignment.json
    f1a2e8f86e389c7abdb6611c1752574cb00f6f08b79e0600c1d888bc07367b69  analysis.py
    d7eb90a1d74c7f6579940ee625caefe7d2b6cb5816bdf9425845ec319ab2a164  blind_derive.py
    acd1bc7efda55112d3f842b973f45a84412655a553e88443456985202d3a7ed7  reference_claims_blinded.json
    cc9b1a3a01d2f0e0a542be6ae080c3eaa133e0fae2a624eafb8f66c9ee2269f6  reference_adjudication_instructions.md
    1d9acab7a6c813103e78f64e01c1dc4bcbdc3a02a1054e01cb7d89602529cb54  reference_adjudication_schema.json
    edf10a56ae916e94c00471b5df20c35f4076c2a858148fef7bf9864075e6e750  effective_reference.py
    7c455716fbd9f9b97d186ad618ef1762896a482545d6eff9c5da95c9673fe5c0  T_defect_probe.py
    b7241cf6aab96e3f66711e1361838204ba485600e3aa113f531db77f5fa7e435  T_defect_probe.out

### §7.7 V3 differential accounting — NO SILENT CORPUS DRIFT

**Item level.** All 36 V3 claims are **RETAINED** byte-identically as CL-01 – CL-36 (text
unchanged; served question unchanged). Their metadata is **MODIFIED** on an explicit basis:

| V3 items | Disposition | Exact basis |
|---|---|---|
| CL-01 – CL-36 text | RETAINED (byte-identical) | preserved baseline; no reason to drift |
| V3 `category` C1…C9 | MODIFIED → FAM-01…FAM-09 | construct-validity requirement: families are structural classes shared with the added items; C1↔FAM-01 … C9↔FAM-09 map one-to-one |
| V3 `reference_label` / `reference_clause_basis` / `reference_provenance` | MODIFIED → sealed construction label / sealed basis (diagnostic only) | accepted repair (ADM-2 / R9; M1 strictly separate 2+1 reference): Creator labels no longer participate in the effective reference at all |
| V3 rule E (Creator label determinate and adjudicator equal → EFFECTIVE = that label) | REMOVED | Owner premise M1 + accepted repair ADM-2 / R9: the effective reference comes only from the separate human reference process (§8.3) |
| V3 single arm (claim + review question, no governed-question text) | MODIFIED → two arms A / B | Owner premise C3 |
| V3 two-label reviewer vocabulary | MODIFIED → four labels | Lead instruction §10 / accepted repairs ADM-5 / R11 |
| CL-08 basis | MODIFIED (F2, also F6 under EN-v1) | policy version EN-v1 adds F6; text unchanged |
| CL-09 / CL-10 / CL-12 / CL-14 / CL-17 / CL-19 / CL-21 – CL-27 | annotated G4A = Y | accepted repair L6 / R7 (STUDY-CORPUS G-4-A CONDITION PROPORTION); descriptive only |
| CL-37 – CL-48 | ADDED | construct-validity requirement (ADM-2 / R9: pre-registered meaning-preserving and meaning-changing minimal pairs) |
| CL-49, CL-50 | ADDED | reason-code vocabulary requirement (acknowledged unknown) — Lead instruction §11 |
| CL-51, CL-52 | ADDED | Owner premise P3 (missing dependency) — Lead instruction §11 |
| CL-53 | ADDED | Hybrid §6 / Amendment §5 (`USER CONFIRMATION != ELIGIBLE`) — Lead instruction §11 |
| CL-54, CL-55 | ADDED | construct-validity requirement: P-4 invariant anchors (`CLAIM SUFFICIENCY != TECHNICAL / EMPIRICAL VALIDATION`) |
| CL-56, CL-57 | ADDED | study-label requirement: OUT_OF_SCOPE must be exercisable — Lead instruction §10 |
| V3 items REMOVED | NONE | — |

**Protocol-section level (V3 PROTOCOL.md sections → this protocol).**

| V3 section | Disposition | Where / basis |
|---|---|---|
| A reviewer role | MODIFIED | §3.2, §12 — four labels; two arms |
| B exact review question | MODIFIED | §3.2 — wording retargeted to "in the words of the claim"; four labels |
| C reviewer instructions (`reviewer_instructions.md`) | MODIFIED, now in-file | §12.1 / §12.2 — one-file self-containment |
| D policy CE-POLICY-v1 | MODIFIED → EN-v1 | §3 — renamed; P-3 context rule (Owner P3); F6 / F7; P-5 / P-6; P-9 |
| E SUFFICIENT definition | RETAINED (substance E1 / E2) | §3.3 P-1 |
| F INSUFFICIENT definition | RETAINED + EXTENDED (F1–F5 kept; F6, F7 added) | §3.3 P-2 — Owner P3 / reason-code requirement |
| G must-not judgments | RETAINED | §3.3 P-4 |
| H claim construction | RETAINED + EXTENDED | §7.1 — same construction fence; 21 items added |
| I sample composition (36 × full crossing + 25 % repeats) | MODIFIED | §7, §11 — 57 items, two arms, balanced incomplete assignment, 4 repeats per reviewer |
| J category definitions | MODIFIED → families | §7.3 |
| K reviewer sample size (5, full crossing) | MODIFIED | §11.1 — 18 measured reviewers, PROTOCOL DESIGN PROPOSAL (ADM-8 / R14; L4 / R5) |
| L reviewer qualification | MODIFIED | §9 — exclusions extended (Level-1/2/3-exposed personnel, protocol-file exposure), tool restrictions |
| M assignment (full crossing) | REMOVED → balanced incomplete design | §11 — arm and minimal-pair constraints make full crossing inadmissible |
| N repeat / washout (front window 17, ≥ 27 intervening) | MODIFIED | §11.3 — four repeats per reviewer from positions 1–7 appended at 20–23; ≥ 15 intervening; recognition asked once at session end |
| O blinding | RETAINED + EXTENDED | §10 |
| P randomization (seed 20260831) | MODIFIED | §11 — new seeded realisation; the frozen tables are the truth |
| Z independent reference adjudication (one adjudicator; rule E; rule F; rule G; order Z.7) | MODIFIED | §8.3 — 2+1 per arm; rule E REMOVED; rule F retained in substance; rule G superseded by §14 (no script in repo); Z.7 ordering RETAINED in substance |
| Q evidence capture schema | MODIFIED | §13.1 — four labels, reason codes, arm group, presentation status, end-of-session recognition field |
| R analysis method (`analysis.py`) | MODIFIED, no executable | §14 / §15 — dependence-aware framework; no repository script |
| S disagreement analysis | RETAINED | §14 M-16 |
| T stopping rule | MODIFIED | §20.1 |
| U privacy / data handling | RETAINED + EXTENDED | §21 |
| V prohibited post-hoc changes | RETAINED + version-change rule | §20 |
| W missing reviews / withdrawals | RETAINED | §15.4 |
| X ambiguous cases | RETAINED (REFERENCE-INDETERMINATE excluded from FS / FI) | §8.3, §14 |
| Y reference-label basis + provisional-rate limitation | MODIFIED | §7.4 / §8.3 — Creator labels sealed; the provisional-rate clause is superseded by the separate reference process |
| V3 executables | NOT COPIED (provenance only) | §7.6 |

**HISTORICAL / SUPERSEDED / NON-GOVERNING — differential provenance only.** The three paragraphs
below record what changed between successive frozen candidates. They quote superseded design
wording in order to say it was removed; nothing in them states current design. The current design is
whatever the numbered sections say `[RZ-1 … RZ-7]`.

**Sibling differential against the prior frozen candidate `63999d5d…` (differential input only).**
Corpus: all 57 items RETAINED byte-identically, same IDs, families, MP groups, sealed labels and
G-4-A flags (no M-item required a corpus change). Assignment realisation: MODIFIED (two independent
randomized groups; frozen H2 roles; four end-of-session repeats) — basis M1 / M2. Reference
architecture: MODIFIED (six arm-separated reference humans; one semantic path for
CANNOT_ADJUDICATE / REFERENCE-INDETERMINATE) — basis M3. Label boundary: MODIFIED (§4A) — basis M4.
Instruction packets and disclosures: MODIFIED — basis M5. Identity custodian duties: ADDED — basis
M6. Analysis sets: MODIFIED — basis M7. Statistical procedures: MODIFIED (frozen primaries and
fallbacks) — basis M8. Study-surface specification: ADDED (§13.2) — basis M9. Everything else is
RETAINED. The M1–M9 repair matrix is preserved at §28.

**Sibling differential against the prior frozen candidate `ef74f1b3…` (differential input only).**
Corpus: all 57 items RETAINED byte-identically again; no N-item required a corpus change. Changed
on an exact N-basis: allocation concealment ADDED (§6.1A) — N1; per-arm operational references,
common comparative strata C_I / C_S, the decision-propensity estimand Δ_S and the mandatory
reference transition matrix ADDED, and the single pooled Δ_FS / Δ_FI of the prior candidate REMOVED
(§14) — N2; reference label semantics MODIFIED so that intrinsic ambiguity is REFERENCE-INDETERMINATE
and CANNOT_ADJUDICATE is extrinsic only, with the measured CA-INTRINSIC sub-class separated
(§3.3 P-5 / P-5M / P-5R, §4A, §5) — N3; exact presentation orders ADDED as frozen tables and the
"fixed at packet issue" / seeded-procedure formulations REMOVED (§12.5, §8.3, §13.2) — N4; the
length-conditioned display marker REMOVED and a uniform display-integrity behaviour substituted
(§4A, §13.2) — N5; the Owner consent / withdrawal policy EMBEDDED as Owner authority, replacing the
Creator-proposed privacy paragraph (§21.2) — N6; PS-1 … PS-7 REPLACED by the frozen positive-weight
multiplier bootstrap, the GLMM → Bayesian fallback chain and the H2 delete-one-reviewer envelope,
with Clopper–Pearson and Henderson III REMOVED from the governing chain (§15) — N7; the study-surface
lifecycle status MODIFIED from `NEW EXECUTABLE SURFACE REQUIRED: YES` to `NOT YET PROVEN REQUIRED`
and the "no executable is required" formulations REMOVED (§11.4, §13.3, §23) — N8. Everything else
is RETAINED. The complete N1–N8 crosswalk is §29.

**Sibling differential against the prior frozen candidate `efdfad9f…` (differential input only).**
Corpus: all 57 items RETAINED byte-identically; no residual item required a corpus change. N4's
frozen presentation orders (Tables 12.5-A / 12.5-B / 12.5-C) are RETAINED byte-identically and were
not regenerated. Changed on an exact residual basis: allocation concealment MODIFIED to a random
draw at issuance with a single issuance authority, and the commitment wording MODIFIED to preserve
the withdrawal right (§6.1A, §13.2 item 30) — N1; the reference outcome model MODIFIED by the
addition of the non-truth process disposition RU and the removal of process states from the
transition matrix and strata (§8.3, §14) — N2 / N3; the accessibility invariant's marker dependency
REMOVED (§13.2 item 29) — N5; universal-retention statements REMOVED from the consent summary and
§21.1 / §21.4 (§12, §21) — N6; the secondary all-item error analysis REMOVED (§14.1, §14.2, §15.2)
— N7; the header's "requires no executable artifact" claim and Route 2's technology preselection
REMOVED (header, §13.3) — N8. Everything else, including every primary statistical procedure, is
RETAINED. The residual-repair crosswalk is §29.1.

**Observation on the baseline (non-load-bearing, recorded for fidelity).** V3 `assignment.json`
carries `front_window: 17` while its `method` string says "slots 1..18"; V3 PROTOCOL.md §N and
`assignment.py` state 17. The inconsistency is internal to V3 and immaterial here because V3
section M / N is not retained; it is recorded, not repaired.

---

## §8. Measured pool, H2 primary role model and the strictly separate reference process

### §8.1 M1 measured model `[OWNER-PREMISE M1 · PROPOSAL for the unit interpretation]`

    M1 MEASURED RATINGS: 3 PER ELIGIBLE STUDY ITEM
    ELIGIBLE STUDY ITEM := one (corpus item, arm) presentation unit admitted by §7.2 (114 units)
    RATERS PER STUDY ITEM: 3 DISTINCT MEASURED REVIEWERS OF THAT ARM'S GROUP, FIRST PASS
    M1 THREE-RATER MAJORITY: NOT HUMAN_NOW SOURCE AUTHORITY
    MEASURED MAJORITY: NOT REFERENCE TRUTH

Creator interpretation, flagged for Lead review: "per eligible study item" is read at the
(item, arm) level, so every corpus item receives 3 ratings in ARM-A (from GROUP-A) and 3 in ARM-B
(from GROUP-B). The three-rater majority is reported only as a descriptive statistic; it is never an
eligibility source and never a reference.

### §8.2 H2 — primary deployed-configuration model under test `[REPAIR-DESIGN PROPOSAL — M2]`

The Owner-selected candidate deployed configuration is H2: DUAL INDEPENDENT REVIEW + FAIL-CLOSED
THIRD-HUMAN ESCALATION `[OWNER-PREMISE H2; FINDING ADM-1 / R8]`. The pilot does not deploy it; it
simulates exactly ONE deployment per study item from frozen roles.

**Frozen role assignment.** For every study item the three first-pass raters hold three distinct,
pre-assigned roles:

    INITIAL REVIEWER ROLE 1  (ROLE-1)
    INITIAL REVIEWER ROLE 2  (ROLE-2)
    THIRD-HUMAN / ESCALATION ROLE (ROLE-3)

Roles are frozen in table §11.2-D before any outcome exists. They were generated by seeded
randomization over the three raters of each study item, balanced so that every reviewer holds ROLE-3
for 6 or 7 of their 19 first-pass items, with ROLE-1 / ROLE-2 assigned by a seeded coin; roles
therefore rotate across items, across reviewers, across families and across both arms. No reviewer
holds more than one role for the same study item (each reviewer rates each item once). All three
ratings are collected blind and in the same way; the roles determine only which ratings the primary
H2 computation reads and in which order. `POST-HOC ROLE CHOICE: PROHIBITED` — the realised table is
binding and the ROLE-3 rating is read only when the primary rule escalates.

**Primary H2 rule — complete final semantics (deterministic; fail-closed; asymmetric under T1).**
Let v1, v2 be the ROLE-1 / ROLE-2 labels and v3 the ROLE-3 label; S = SUFFICIENT, I =
INSUFFICIENT, CA = CANNOT_ADJUDICATE, OOS = OUT_OF_SCOPE.

| Initial state (v1, v2 — order immaterial) | Step | Final H2 study outcome |
|---|---|---|
| S / S | no escalation | CANDIDATE POSITIVE STUDY OUTCOME |
| I / I | no escalation | NEGATIVE STUDY OUTCOME |
| S / I | escalate | v3 = S → CANDIDATE POSITIVE · v3 = I → NEGATIVE · v3 ∈ {CA, OOS} → FAIL-CLOSED UNRESOLVED |
| S / CA | escalate | v3 = S → CANDIDATE POSITIVE · v3 = I → FAIL-CLOSED UNRESOLVED (one S, one I, one abstention: no two committed agree) · v3 ∈ {CA, OOS} → FAIL-CLOSED UNRESOLVED |
| S / OOS | escalate | v3 = S → CANDIDATE POSITIVE · v3 = I → FAIL-CLOSED UNRESOLVED · v3 = OOS → FAIL-CLOSED UNRESOLVED (sub-code OOS-MAJORITY) · v3 = CA → FAIL-CLOSED UNRESOLVED |
| I / CA | escalate | v3 = I → NEGATIVE · v3 = S → FAIL-CLOSED UNRESOLVED · v3 ∈ {CA, OOS} → FAIL-CLOSED UNRESOLVED |
| I / OOS | escalate | v3 = I → NEGATIVE · v3 = S → FAIL-CLOSED UNRESOLVED · v3 = OOS → FAIL-CLOSED UNRESOLVED (OOS-MAJORITY) · v3 = CA → FAIL-CLOSED UNRESOLVED |
| CA / CA | escalate | v3 = S → FAIL-CLOSED UNRESOLVED (single S) · v3 = I → FAIL-CLOSED UNRESOLVED (single I) · v3 ∈ {CA, OOS} → FAIL-CLOSED UNRESOLVED |
| CA / OOS | escalate | any v3 → FAIL-CLOSED UNRESOLVED (v3 = OOS → sub-code OOS-MAJORITY) |
| OOS / OOS | escalate | v3 = OOS → FAIL-CLOSED UNRESOLVED (OOS-MAJORITY) · any other v3 → FAIL-CLOSED UNRESOLVED |

General statement of the rule, of which the table is the exhaustive enumeration: CANDIDATE POSITIVE
requires two committed SUFFICIENT labels among the considered ratings with the third human
concurring whenever an escalation occurred; NEGATIVE requires two committed INSUFFICIENT labels with
the third human concurring whenever an escalation occurred; every other terminal state is
FAIL-CLOSED UNRESOLVED (no positive outcome; the claim remains unqualified; sub-codes record the
reason). An abstention or OUT_OF_SCOPE never contributes to either committed count. This rule is a
REPAIR-DESIGN PROPOSAL, not Owner policy, until later accepted.

    NO ClaimEligibilityEvent IS MINTED · NO PRODUCT STATE IS TOUCHED
    FAIL-CLOSED UNRESOLVED != NEGATIVE STUDY OUTCOME != INSUFFICIENT LABEL
    THE SIMULATION'S LIMIT: in a deployment the third human would know that an escalation occurred;
      here ROLE-3 rated blind and simultaneously. This is disclosed and is not assumed away.

**Primary H2 estimands** (unit = study item; computed only from the frozen roles): configuration
FS = P(CANDIDATE POSITIVE | primary reference-INSUFFICIENT study item); configuration FI =
P(NEGATIVE | primary reference-SUFFICIENT study item); ESCALATION RATE = P(escalation) over
primary reference-determinate study items; UNRESOLVED RATE = P(FAIL-CLOSED UNRESOLVED) on the same
set, split by sub-code. Exact sets and procedures: §14 M-04, §15 PS-5.

    H2 ALL-PAIRS ANALYSIS: SECONDARY / SENSITIVITY ONLY — the three unordered pairs of a study
      item's ratings may be reported as a correlated sensitivity check of the primary
      configuration rates; they are never the primary HUMAN_NOW configuration estimate.

### §8.3 Strictly separate, arm-safe 2+1 reference process `[REPAIR-DESIGN PROPOSAL — M3]`

    REFERENCE POOL: REAL HUMANS, SEPARATE FROM THE MEASURED POOL (no person in both pools)
    REFERENCE HUMANS: SIX, ARM-SEPARATED —
      ARM-A: RA-A1, RA-A2 (first pass), RA-A3 (third / escalation)
      ARM-B: RA-B1, RA-B2 (first pass), RA-B3 (third / escalation)
    NO REFERENCE HUMAN SERVES IN BOTH ARMS; NO ARM-A REFERENCE HUMAN EVER RECEIVES Q-CTX-01
    LLM, SIMULATED OR CREATOR-GENERATED ADJUDICATION: PROHIBITED

Exact assignment and sequence `[N4]`: RA-A1, RA-A2, RA-B1 and RA-B2 each adjudicate all 57 corpus
items in their arm, in the exact frozen order of **Table 12.5-A**. RA-A3 and RA-B3 receive only the
items escalated in their arm; those items are presented in the exact frozen full ranking of **Table
12.5-B** for that adjudicator, escalated items only, ranks preserved and gaps closed without
reordering. No order is generated later, fixed at packet issue, or derived from a procedure: the
tables are the load-bearing truth. Every reference human works alone, without tools, and is blind to
sealed metadata, to every measured rating and to the other reference humans.

Reference labels `[N3]`: SUFFICIENT · INSUFFICIENT · OUT_OF_SCOPE · REFERENCE-INDETERMINATE ·
CANNOT_ADJUDICATE. Exactly one semantic path exists for each non-committal label, and the two are
mutually exclusive:

    REFERENCE-INDETERMINATE = a REFERENCE VERDICT that THE TEXT ITSELF is materially ambiguous
                              under the frozen policy (intrinsic item / policy ambiguity,
                              `RC-RI-01`); it can be a reference outcome
    CANNOT_ADJUDICATE       = a PER-ADJUDICATOR EXTRINSIC ABSTENTION ONLY — recusal or conflict
                              (`RC-CA-03`), prior prohibited exposure (`RC-CA-01`), broken or
                              incomplete presentation or another process failure (`RC-CA-04`);
                              recorded verbatim; never a reference outcome; never a vote
    SUBSTANTIVE POLICY AMBIGUITY IS NEVER CANNOT_ADJUDICATE IN THE REFERENCE LANE
    THE MEASURED CA-INTRINSIC SUB-CLASS (`RC-CA-02`, §3.3 P-5M) IS A MEASURED-LANE OBSERVATION AND
      NEVER ENTERS REFERENCE TRUTH IN ANY FORM

**Reference outcomes and the separate process disposition `[N3]`.** There are exactly four
reference OUTCOMES — SUFFICIENT, INSUFFICIENT, REFERENCE-INDETERMINATE and OUT_OF_SCOPE — and each
is a statement about the item. Anything the process fails to resolve is not an outcome at all: it is
recorded as

    RU = REFERENCE OUTCOME UNAVAILABLE — UNRESOLVED PROCESS

which is NON-TRUTH PROCESS METADATA, not a fifth semantic category. RU never means the item is
ambiguous, never enters the transition matrix, never enters any denominator or stratum, and is
never reported as REFERENCE-INDETERMINATE.

Reference outcome rule per study item — DETERMINISTIC, MUTUALLY EXCLUSIVE, COLLECTIVELY COMPLETE
`[PF-02]`. The rule branches FIRST on

    k := the number of NON-ABSTAINING first-pass verdicts among {v1, v2}, k ∈ {2, 1, 0}

so the three branches partition the governed state space and no branch can shadow another. Within a
branch the sub-cases are mutually exclusive by construction. A verdict is non-abstaining when it is
one of the four outcomes SUFFICIENT · INSUFFICIENT · REFERENCE-INDETERMINATE · OUT_OF_SCOPE; a
CANNOT_ADJUDICATE is an extrinsic abstention, is never a vote, and its reason is recorded.

    BRANCH k = 2 — both first-pass adjudicators voted
      2.1 v1 = v2                         → REFERENCE OUTCOME = that label. NO ESCALATION.
      2.2 v1 ≠ v2                         → ESCALATE to RA-x3 (blind); let v3 be the third verdict
          2.2.a v3 = CANNOT_ADJUDICATE    → RU · THIRD-ADJUDICATOR-ABSTENTION
          2.2.b v3 = v1 or v3 = v2        → REFERENCE OUTCOME = that label (two humans concur)
          2.2.c v3 ∉ {v1, v2}             → RU · NO-CONCURRENCE
    BRANCH k = 1 — exactly one first-pass adjudicator abstained; let w be the single first-pass vote
      ESCALATE to RA-x3 (blind); let v3 be the third verdict
      1.1 v3 = CANNOT_ADJUDICATE          → RU · THIRD-ADJUDICATOR-ABSTENTION
      1.2 v3 = w                          → REFERENCE OUTCOME = w (two humans concur)
      1.3 v3 ≠ w                          → RU · NO-CONCURRENCE
    BRANCH k = 0 — both first-pass adjudicators abstained
      ESCALATE to RA-x3 (blind) for record completeness; whatever v3 is, at most ONE non-abstaining
      vote can exist for the item, so no two humans can concur
      0.1 ANY v3 (substantive or abstention) → RU · INSUFFICIENT-PANEL

    PRECEDENCE IS FIXED BY THE BRANCH KEY k, NOT BY READING ORDER: INSUFFICIENT-PANEL applies if
      and only if k = 0, NO-CONCURRENCE if and only if k ≥ 1 and the third verdict is substantive
      and does not match any first-pass vote, THIRD-ADJUDICATOR-ABSTENTION if and only if k ≥ 1 and
      the third verdict is an abstention. The three RU sub-codes are therefore mutually exclusive
      and exhaustive over the RU space, and every governed input state yields exactly one
      disposition and at most one sub-code.
    A REFERENCE OUTCOME ALWAYS REQUIRES TWO HUMANS TO CONCUR ON THE SAME LABEL.
    REFERENCE-INDETERMINATE is therefore an OUTCOME only when two humans independently concur that
      the item is materially arguable under the policy; process failure is never converted into it.

    RU ITEMS: listed individually in the PROCESS-DISPOSITION REGISTER (arm, item, sub-code, the
      abstention reasons) at the reference freeze; reported in M-14; excluded from Ref_A / Ref_B,
      from the M-19 transition matrix, from C_I / C_S / A_C and from every metric denominator.
      An RU rate above zero is a study-integrity finding for Lead review, never a data point about
      the corpus.

Material ambiguity is never forced into SUFFICIENT / INSUFFICIENT, and process failure is never
dressed up as ambiguity: a determinate reference requires two humans to concur on the same
determinate label, and REFERENCE-INDETERMINATE requires two humans to concur on ambiguity. Measured
ratings never participate (non-circularity). Creator sealed labels never participate (V3 rule E
REMOVED).

Effective reference used by the analysis:

    EFFECTIVE REFERENCE = REFERENCE OUTCOME, one per study item, ARM-SPECIFIC BY CONSTRUCTION:
      Ref_A(i) for ARM-A study items, Ref_B(i) for ARM-B study items `[N2]`
    PER-ARM OPERATIONAL ERROR RATES USE THAT ARM'S OWN REFERENCE (FS_A / FI_A against Ref_A;
      FS_B / FI_B against Ref_B) — §14.2 M-01 / M-02
    BETWEEN-ARM COMPARISONS USE ONLY THE COMMON STRATA C_I / C_S OF §14.1 — never a difference of
      rates taken over incomparable arm-specific item sets `[N2]`
    FS denominator basis (within an arm): that arm's EFFECTIVE REFERENCE == INSUFFICIENT
    FI denominator basis (within an arm): that arm's EFFECTIVE REFERENCE == SUFFICIENT
    EFFECTIVE REFERENCE == REFERENCE-INDETERMINATE → excluded from FS and FI; retained for
      ambiguity, disagreement, context-effect and construct analyses
    EFFECTIVE REFERENCE == OUT_OF_SCOPE → excluded from FS and FI; used for the OOS-handling metric
    RU (process-unresolved) → NOT AN EFFECTIVE REFERENCE AT ALL; the study item carries no reference
      and is excluded from every reference-based analysis, matrix and stratum
    THERE IS NO "CANNOT_ADJUDICATE" REFERENCE OUTCOME
    Final denominator sizes are reported BEFORE any measured outcome is collected.

Order of operations (binding):

    1 this protocol text reaches immutable freeze and then Owner exact-SHA acceptance through the
      complete §30 lifecycle — NOT YET REACHED; this text is a pre-freeze draft `[PF-01]`
    2 Owner pilot authorization D5 (§22) — NOT GRANTED BY THIS DOCUMENT
    3 Owner-designated human-study identity custodian appointed (§21.2, Owner policy) — NOT
      APPOINTED HERE
    4 reference humans enrolled under the §6.1A concealment procedure; arm-specific packets issued
      (§12.3, §12.4) with the frozen orders of §12.5
    5 reference adjudication completed per arm per this section
    6 the REFERENCE-FREEZE ARTIFACT (§8.3A) is constructed, serialized canonically and hashed;
      its SHA-256 is the reference identity for the whole gate
    7 effective reference and denominators derived and frozen
    8 verification that NO measured outcome existed before steps 5–7 completed
    9 Lead review of the completed reference evidence
    10 only then may measured collection begin

Personnel exposed to material G-4-A Level-1 / Level-2 / Level-3 case identities or expected
outcomes, or to §7.2 of this file, or to any Creator, Lead or LLM label, expected outcome, family
expectation or author intent: `REFERENCE LABEL PROVISION: PROHIBITED`. They may perform methodology
or governance review; they may not provide study reference labels `[FINDING ADM-6 / R12]`. The V3
"non-anchor items" carve-out is not carried.

### §8.3A Reference-freeze artifact and its identity `[RZ-4]`

One deterministic artifact carries every reference disposition. It is constructed once, at the
reference freeze (§8.3 step 6), before any measured outcome exists.

    UNIT: ONE RECORD PER (arm, claim_id) — exactly 114 records, no more and no fewer
    FIELDS, IN THIS FIXED ORDER:
      1 arm                              enum, exact spelling: A | B
      2 claim_id                         CL-01 … CL-57
      3 reference_disposition            enum, exact spelling:
                                           SUFFICIENT | INSUFFICIENT | REFERENCE-INDETERMINATE |
                                           OUT_OF_SCOPE | RU
      4 ru_subcode                       enum, required if and only if field 3 = RU, exact spelling:
                                           THIRD-ADJUDICATOR-ABSTENTION | NO-CONCURRENCE |
                                           INSUFFICIENT-PANEL ; otherwise the empty field
      5 source_adjudicator_record_ids    the exact capture-record identities (§13.1) of every
                                           adjudicator rating used to derive field 3, each written
                                           as <participant_id>:<claim_id>, first-pass records in
                                           ascending participant_id order followed by the third
                                           record when the item escalated, joined by a single comma
                                           with no spaces
    NO OTHER FIELD EXISTS. Nothing further is needed for deterministic reconstruction.

    CANONICAL RECORD ORDER: arm ascending in the FROZEN ARM ORDER A THEN B; within an arm,
      claim_id ascending CL-01 … CL-57
    CANONICAL SERIALIZATION (byte-exact): UTF-8 with no byte-order mark; one record per line;
      fields joined by a single U+007C VERTICAL LINE with no surrounding whitespace; an empty field
      is zero characters between two separators; no header line; no comment line; no blank line; no
      leading, trailing or internal padding whitespace anywhere; each line terminated by a single
      U+000A LINE FEED, including the last, so the byte stream ends with exactly one U+000A and the
      file contains exactly 114 line feeds
    HASH: REFERENCE-FREEZE ARTIFACT HASH := SHA-256 over the exact bytes defined above

    DISTINCT IDENTITIES: the RAW ADJUDICATOR RATING RECORD SET HASH (§13.2 item 26 — the exported
      reference-lane capture records) and the REFERENCE-FREEZE ARTIFACT HASH are two different
      identities of two different byte streams. Both are retained and both are reported; neither
      substitutes for the other, and no statement in this protocol treats outcomes and RU as
      "hashed together" other than by their literal serialization inside this one artifact.

    REPRODUCIBILITY REQUIREMENT: Ref_A, Ref_B, every RU disposition and sub-code, C_I, C_S, A_C and
      the M-19 transition matrix are each derivable from this artifact alone by the rules of §8.3
      and §14.1, without reference to any other file, and any recomputation must reproduce them
      exactly.

    INDEPENDENT REVIEW B != HUMAN STUDY REFERENCE ADJUDICATION (§23)

---

## §9. Reviewer qualification, conflict of interest and tool restrictions

**Measured reviewers (MR-01 … MR-18).** Adults competent in written English who can follow
written instructions. Electronics or engineering expertise is NOT required and NOT screened for,
because the judgment under test is articulation sufficiency, not technical validity; any domain
background is recorded as a covariate (`none / some / professional`), not a qualification.

**Reference humans (RA-A1, RA-A2, RA-A3, RA-B1, RA-B2, RA-B3).** Same competence basis;
additionally must have had no contact with the measured pool or with a reference human of the other
arm about the study.

**Excluded from BOTH pools:** the Creator and any claim author; the Lead; any Independent Reviewer
of this draft, of any prior candidate or of the prior design; anyone exposed to the G-4-A
Level-1 / Level-2 / Level-3 case identities or expected outcomes; anyone who has read §7.2 of this
file or any V3 label file; anyone who authored the contract, the Amendment or this protocol; the
future identity custodian (§21); anyone with a personal or commercial interest in the product's
mechanism-progression outcome.

**Tool restrictions (binding for every participant).** No LLM, search engine, translation tool,
grammar tool, dictionary lookup of nonsense tokens, or any other assistance; no discussion with any
person during or after the session about any item; no note-taking outside the capture record; one
sitting where possible, breaks only between items. A disclosed breach is a PROCESS FAILURE and is
recorded as `RC-CA-04` (with `presentation_status = OK`, which distinguishes it from a surface
defect) for the affected items `[PF-03]`; an undisclosed breach discovered later voids that
participant's affected data, reported as such.

**Consent, compensation and withdrawal.** Governed by the Owner consent / withdrawal policy
embedded at §21.2, which is Owner authority and not a Creator proposal: consent must precede
participation, must be affirmatively accepted before allocation is revealed (§6.1A E2), and must
truthfully disclose every element the policy enumerates. Compensation is flat and never contingent
on any verdict or on completing the session. Withdrawal is available at any time; its consequences
for future participation and for already-collected pseudonymous data are fixed by §21.2 and by the
pre-frozen consent / privacy terms — never improvised.

---

## §10. Blinding, contamination and leakage fences

Measured reviewers are blind to: family, MP group and role, sealed label, sealed basis, the G-4-A
shape flag, their H2 role on any item, the hypothesis, the existence of the G-4-A defect, the
existence of the other arm, which items are repeats, every other reviewer's ratings, and every
reference outcome. Reference humans are additionally blind to every measured rating, to each other,
and (for the third role) to the prior verdicts and to which of them disagreed.

    PROTOCOL-FILE EXPOSURE = EXCLUSION (§9)
    CLAIM TEXT BYTE-IDENTICAL BETWEEN §7.2 AND EVERY PRESENTATION (§13.2)
    ARM-B ADDS ONLY Q-CTX-01 TEXT — NO DOMAIN, NO SESSION, NO OTHER CONTEXT
    GROUP-A NEVER RECEIVES THE QUESTION; GROUP-B ALWAYS SEES IT (§6.1)
    PRESENTATION ORDER CARRIES NO INFORMATION: seeded per-reviewer sequence (§11.2)
    NO "have you seen this before?" PROMPT PER ITEM — recognition is asked once, at the end of the
      session, listing the session's items in the frozen order of Table 12.5-C (NBO-4 retained)
    NO CONFERRING · NO CLARIFICATION DURING THE STUDY · THE PACKET IS THE ONLY INSTRUCTION
    A reviewer who states they recognised a repeat has that pair flagged CONTAMINATED and excluded
      from the stability denominator, with the exclusion reported
    A participant who states they recognised an item, its author or its label from outside the
      study records RC-CA-01 (PRIOR PROHIBITED EXPOSURE) — not RC-CA-03, which is reserved for a
      conflict of interest or recusal `[PF-03]`

Leading / contamination fence carried from Hybrid §7 (deferred there, applied here to the review
instructions): the instructions must help a participant apply the policy; they must never teach
which label is "expected" for any item shape. Instruction clarity is itself a measured output (§14).

---

## §11. Roster, randomized groups, balanced assignment, roles and repeats `[PROPOSAL]`

### §11.1 Design constants

    MEASURED ROSTER: 18 distinct reviewers (MR-01 … MR-18) — GROUP-A 9, GROUP-B 9
    REFERENCE HUMANS: 6 (RA-A1, RA-A2, RA-A3, RA-B1, RA-B2, RA-B3)
    FIRST-PASS ITEMS PER REVIEWER: 19 (one member of each of the 6 minimal-pair groups + 13 of
      the 39 other corpus items), all in the reviewer's single arm
    EXACT REPEATS PER REVIEWER: 4, appended at positions 20–23 in ascending order of original
      position, drawn from first-pass positions 1–7 (guaranteed ≥ 15 intervening items)
    ITEMS PER REVIEWER: 23
    MEASURED FIRST-PASS RATINGS: 342 (114 study items × 3) — 171 per arm
    MEASURED REPEAT RATINGS: 72 (56 study items repeat-tested; 43 distinct corpus items)
    H2 ROLES: every study item has exactly one ROLE-1, ROLE-2, ROLE-3 (table §11.2-D);
      each reviewer holds ROLE-3 for 6 or 7 items
    GENERATION SEED (provenance only): 20260905 — the frozen tables below, not the procedure, are
      the load-bearing truth `[N8: this states where protocol truth lives; it is not a claim that
      the eventual pilot needs no study surface — see §13.3]`

Rationale for each constant, and what it lets the pilot inform:

- **18 reviewers in two groups of 9.** Within one arm, a minimal-pair group has 3 members × 3
  ratings = 9 rater slots that must be filled by distinct reviewers (no reviewer may see two members
  of a group); 9 per arm is the smallest group that fills every minimal-pair group exactly once per
  reviewer while keeping the burden light (23 short items). Two such groups realise the C3 design
  without cross-arm exposure. Reviewer is a random effect with 9 levels per arm and 18 overall,
  enough to report a reviewer variance component and reviewer-level ICC with usable pilot precision
  `[FINDING L4 / R5, ADM-8 / R14]`; V3's roster of 5 made reviewer a fixed effect.
- **57 items / 114 study items × 3.** Every corpus item is rated 3 times in each arm, so the
  within-item context contrast δ_i exists for every item and the item variance component is
  estimable; ≥ 9 items per larger sealed family support family-level reporting. This is a PLANNING
  size for a pilot, not a main-study N.
- **4 exact repeats per reviewer at the end of the session.** 72 repeat pairs inform
  intra-reviewer stability in each arm; the ≥ 15-item washout is structural (positions 1–7 replayed
  at 20–23). The pilot measures how often repeats are recognised, which informs the main-study
  washout design.
- **Frozen H2 roles balanced across reviewers.** Each reviewer serves as the third human for 6–7
  items and as an initial reviewer for the rest, so configuration-level rates are not driven by
  particular people occupying particular roles.
- **Abstention and reference-indeterminacy.** Two OUT_OF_SCOPE probes, two acknowledged-unknown
  items, two missing-dependency items and five construction-indeterminate items ensure that every
  non-committal label and the reference's indeterminate outcome are exercised at pilot scale, so
  their rates are estimable rather than assumed.

None of these numbers is a final main-study N, FS limit, FI limit, agreement threshold,
materiality threshold or production SLA. `FINAL MAIN-STUDY N: NOT DETERMINED NOW`.

### §11.2 Frozen assignment realisation

Notation: `CL-nn` = corpus item in the reviewer's arm; trailing `*` = exact repeat of an earlier
position in the same session. Arm per reviewer is given in Table 11.2-A and repeated in the sequence
table.

**Table 11.2-A — frozen ID→arm mapping (9 / 9). A participant is attached to an ID only by the
§6.1A post-commitment random draw; this table is not an enrolment schedule and its row order carries
no allocation information.**

| Reviewer | Arm group |
|---|---|
| MR-01 | ARM-B (claim + question) |
| MR-02 | ARM-A (claim only) |
| MR-03 | ARM-A (claim only) |
| MR-04 | ARM-B (claim + question) |
| MR-05 | ARM-B (claim + question) |
| MR-06 | ARM-A (claim only) |
| MR-07 | ARM-B (claim + question) |
| MR-08 | ARM-A (claim only) |
| MR-09 | ARM-B (claim + question) |
| MR-10 | ARM-A (claim only) |
| MR-11 | ARM-A (claim only) |
| MR-12 | ARM-B (claim + question) |
| MR-13 | ARM-B (claim + question) |
| MR-14 | ARM-A (claim only) |
| MR-15 | ARM-A (claim only) |
| MR-16 | ARM-B (claim + question) |
| MR-17 | ARM-A (claim only) |
| MR-18 | ARM-B (claim + question) |

**Table 11.2-B — per-reviewer frozen sequences (positions P01–P23; P20–P23 are the exact repeats).**

| Reviewer | Arm | P01 | P02 | P03 | P04 | P05 | P06 | P07 | P08 | P09 | P10 | P11 | P12 | P13 | P14 | P15 | P16 | P17 | P18 | P19 | P20 | P21 | P22 | P23 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MR-01 | B | CL-35 | CL-37 | CL-14 | CL-26 | CL-06 | CL-15 | CL-20 | CL-48 | CL-44 | CL-08 | CL-17 | CL-45 | CL-31 | CL-41 | CL-03 | CL-55 | CL-32 | CL-28 | CL-27 | CL-37* | CL-26* | CL-06* | CL-20* |
| MR-02 | A | CL-51 | CL-38 | CL-28 | CL-34 | CL-08 | CL-10 | CL-05 | CL-52 | CL-42 | CL-07 | CL-35 | CL-44 | CL-39 | CL-48 | CL-30 | CL-36 | CL-13 | CL-12 | CL-27 | CL-51* | CL-28* | CL-34* | CL-10* |
| MR-03 | A | CL-17 | CL-29 | CL-13 | CL-05 | CL-37 | CL-43 | CL-09 | CL-51 | CL-03 | CL-08 | CL-24 | CL-02 | CL-25 | CL-56 | CL-46 | CL-27 | CL-26 | CL-39 | CL-33 | CL-17* | CL-29* | CL-43* | CL-09* |
| MR-04 | B | CL-04 | CL-49 | CL-05 | CL-40 | CL-48 | CL-20 | CL-18 | CL-45 | CL-41 | CL-38 | CL-08 | CL-23 | CL-54 | CL-35 | CL-02 | CL-32 | CL-09 | CL-44 | CL-16 | CL-49* | CL-05* | CL-20* | CL-18* |
| MR-05 | B | CL-07 | CL-43 | CL-22 | CL-54 | CL-23 | CL-29 | CL-46 | CL-05 | CL-39 | CL-50 | CL-47 | CL-31 | CL-19 | CL-11 | CL-01 | CL-08 | CL-55 | CL-15 | CL-06 | CL-07* | CL-43* | CL-23* | CL-29* |
| MR-06 | A | CL-46 | CL-11 | CL-27 | CL-56 | CL-38 | CL-21 | CL-49 | CL-04 | CL-47 | CL-03 | CL-52 | CL-19 | CL-16 | CL-29 | CL-18 | CL-31 | CL-06 | CL-40 | CL-26 | CL-11* | CL-56* | CL-38* | CL-21* |
| MR-07 | B | CL-11 | CL-25 | CL-23 | CL-33 | CL-37 | CL-30 | CL-29 | CL-54 | CL-06 | CL-34 | CL-10 | CL-07 | CL-31 | CL-36 | CL-19 | CL-12 | CL-56 | CL-43 | CL-39 | CL-11* | CL-25* | CL-23* | CL-33* |
| MR-08 | A | CL-48 | CL-45 | CL-41 | CL-40 | CL-07 | CL-32 | CL-24 | CL-08 | CL-53 | CL-16 | CL-51 | CL-05 | CL-38 | CL-23 | CL-21 | CL-55 | CL-50 | CL-09 | CL-52 | CL-48* | CL-40* | CL-07* | CL-32* |
| MR-09 | B | CL-24 | CL-56 | CL-33 | CL-30 | CL-25 | CL-03 | CL-57 | CL-19 | CL-50 | CL-13 | CL-42 | CL-46 | CL-36 | CL-52 | CL-43 | CL-39 | CL-16 | CL-38 | CL-32 | CL-24* | CL-56* | CL-33* | CL-25* |
| MR-10 | A | CL-42 | CL-02 | CL-04 | CL-57 | CL-21 | CL-55 | CL-45 | CL-37 | CL-54 | CL-22 | CL-20 | CL-26 | CL-47 | CL-49 | CL-14 | CL-56 | CL-12 | CL-34 | CL-18 | CL-04* | CL-57* | CL-21* | CL-55* |
| MR-11 | A | CL-06 | CL-57 | CL-01 | CL-34 | CL-31 | CL-10 | CL-29 | CL-15 | CL-07 | CL-43 | CL-18 | CL-47 | CL-11 | CL-14 | CL-16 | CL-19 | CL-36 | CL-20 | CL-28 | CL-57* | CL-34* | CL-31* | CL-29* |
| MR-12 | B | CL-20 | CL-25 | CL-07 | CL-15 | CL-22 | CL-45 | CL-53 | CL-37 | CL-05 | CL-14 | CL-49 | CL-04 | CL-51 | CL-21 | CL-42 | CL-34 | CL-36 | CL-57 | CL-28 | CL-20* | CL-07* | CL-15* | CL-22* |
| MR-13 | B | CL-56 | CL-24 | CL-13 | CL-50 | CL-01 | CL-52 | CL-26 | CL-47 | CL-30 | CL-21 | CL-11 | CL-14 | CL-03 | CL-17 | CL-46 | CL-18 | CL-29 | CL-09 | CL-27 | CL-56* | CL-13* | CL-01* | CL-52* |
| MR-14 | A | CL-10 | CL-13 | CL-40 | CL-24 | CL-57 | CL-44 | CL-30 | CL-22 | CL-17 | CL-33 | CL-53 | CL-41 | CL-23 | CL-09 | CL-15 | CL-32 | CL-37 | CL-25 | CL-54 | CL-10* | CL-40* | CL-57* | CL-44* |
| MR-15 | A | CL-49 | CL-35 | CL-48 | CL-15 | CL-22 | CL-39 | CL-01 | CL-45 | CL-43 | CL-06 | CL-23 | CL-32 | CL-02 | CL-55 | CL-50 | CL-03 | CL-41 | CL-17 | CL-31 | CL-35* | CL-15* | CL-39* | CL-01* |
| MR-16 | B | CL-55 | CL-01 | CL-51 | CL-12 | CL-26 | CL-53 | CL-17 | CL-42 | CL-40 | CL-57 | CL-10 | CL-02 | CL-47 | CL-27 | CL-44 | CL-28 | CL-49 | CL-35 | CL-34 | CL-55* | CL-51* | CL-26* | CL-53* |
| MR-17 | A | CL-50 | CL-44 | CL-28 | CL-14 | CL-11 | CL-20 | CL-46 | CL-19 | CL-42 | CL-33 | CL-01 | CL-35 | CL-30 | CL-12 | CL-36 | CL-04 | CL-54 | CL-53 | CL-25 | CL-50* | CL-44* | CL-14* | CL-20* |
| MR-18 | B | CL-38 | CL-21 | CL-40 | CL-33 | CL-04 | CL-10 | CL-16 | CL-12 | CL-13 | CL-02 | CL-41 | CL-18 | CL-48 | CL-09 | CL-52 | CL-22 | CL-24 | CL-53 | CL-51 | CL-38* | CL-21* | CL-40* | CL-16* |

**Table 11.2-C — realised repeat separations (original position → repeat position; intervening items).**

| Reviewer | Repeat 1 | Repeat 2 | Repeat 3 | Repeat 4 |
|---|---|---|---|---|
| MR-01 | CL-37: P02→P20 (17) | CL-26: P04→P21 (16) | CL-06: P05→P22 (16) | CL-20: P07→P23 (15) |
| MR-02 | CL-51: P01→P20 (18) | CL-28: P03→P21 (17) | CL-34: P04→P22 (17) | CL-10: P06→P23 (16) |
| MR-03 | CL-17: P01→P20 (18) | CL-29: P02→P21 (18) | CL-43: P06→P22 (15) | CL-09: P07→P23 (15) |
| MR-04 | CL-49: P02→P20 (17) | CL-05: P03→P21 (17) | CL-20: P06→P22 (15) | CL-18: P07→P23 (15) |
| MR-05 | CL-07: P01→P20 (18) | CL-43: P02→P21 (18) | CL-23: P05→P22 (16) | CL-29: P06→P23 (16) |
| MR-06 | CL-11: P02→P20 (17) | CL-56: P04→P21 (16) | CL-38: P05→P22 (16) | CL-21: P06→P23 (16) |
| MR-07 | CL-11: P01→P20 (18) | CL-25: P02→P21 (18) | CL-23: P03→P22 (18) | CL-33: P04→P23 (18) |
| MR-08 | CL-48: P01→P20 (18) | CL-40: P04→P21 (16) | CL-07: P05→P22 (16) | CL-32: P06→P23 (16) |
| MR-09 | CL-24: P01→P20 (18) | CL-56: P02→P21 (18) | CL-33: P03→P22 (18) | CL-25: P05→P23 (17) |
| MR-10 | CL-04: P03→P20 (16) | CL-57: P04→P21 (16) | CL-21: P05→P22 (16) | CL-55: P06→P23 (16) |
| MR-11 | CL-57: P02→P20 (17) | CL-34: P04→P21 (16) | CL-31: P05→P22 (16) | CL-29: P07→P23 (15) |
| MR-12 | CL-20: P01→P20 (18) | CL-07: P03→P21 (17) | CL-15: P04→P22 (17) | CL-22: P05→P23 (17) |
| MR-13 | CL-56: P01→P20 (18) | CL-13: P03→P21 (17) | CL-01: P05→P22 (16) | CL-52: P06→P23 (16) |
| MR-14 | CL-10: P01→P20 (18) | CL-40: P03→P21 (17) | CL-57: P05→P22 (16) | CL-44: P06→P23 (16) |
| MR-15 | CL-35: P02→P20 (17) | CL-15: P04→P21 (16) | CL-39: P06→P22 (15) | CL-01: P07→P23 (15) |
| MR-16 | CL-55: P01→P20 (18) | CL-51: P03→P21 (17) | CL-26: P05→P22 (16) | CL-53: P06→P23 (16) |
| MR-17 | CL-50: P01→P20 (18) | CL-44: P02→P21 (18) | CL-14: P04→P22 (17) | CL-20: P06→P23 (16) |
| MR-18 | CL-38: P01→P20 (18) | CL-21: P02→P21 (18) | CL-40: P03→P22 (18) | CL-16: P07→P23 (15) |

**Table 11.2-D — frozen H2 roles per study item (ROLE-1 / ROLE-2 initial reviewers; ROLE-3 third human), per arm.**

| Corpus item | ARM-A ROLE-1 | ARM-A ROLE-2 | ARM-A ROLE-3 | ARM-B ROLE-1 | ARM-B ROLE-2 | ARM-B ROLE-3 |
|---|---|---|---|---|---|---|
| CL-01 | MR-15 | MR-17 | MR-11 | MR-13 | MR-16 | MR-05 |
| CL-02 | MR-03 | MR-10 | MR-15 | MR-04 | MR-18 | MR-16 |
| CL-03 | MR-06 | MR-15 | MR-03 | MR-09 | MR-01 | MR-13 |
| CL-04 | MR-17 | MR-06 | MR-10 | MR-12 | MR-04 | MR-18 |
| CL-05 | MR-08 | MR-03 | MR-02 | MR-05 | MR-12 | MR-04 |
| CL-06 | MR-11 | MR-15 | MR-06 | MR-01 | MR-05 | MR-07 |
| CL-07 | MR-11 | MR-08 | MR-02 | MR-07 | MR-12 | MR-05 |
| CL-08 | MR-02 | MR-08 | MR-03 | MR-01 | MR-04 | MR-05 |
| CL-09 | MR-03 | MR-14 | MR-08 | MR-18 | MR-13 | MR-04 |
| CL-10 | MR-14 | MR-11 | MR-02 | MR-18 | MR-07 | MR-16 |
| CL-11 | MR-17 | MR-06 | MR-11 | MR-05 | MR-07 | MR-13 |
| CL-12 | MR-02 | MR-10 | MR-17 | MR-16 | MR-18 | MR-07 |
| CL-13 | MR-14 | MR-03 | MR-02 | MR-13 | MR-18 | MR-09 |
| CL-14 | MR-11 | MR-17 | MR-10 | MR-01 | MR-13 | MR-12 |
| CL-15 | MR-15 | MR-11 | MR-14 | MR-05 | MR-12 | MR-01 |
| CL-16 | MR-06 | MR-08 | MR-11 | MR-04 | MR-09 | MR-18 |
| CL-17 | MR-15 | MR-14 | MR-03 | MR-16 | MR-01 | MR-13 |
| CL-18 | MR-10 | MR-06 | MR-11 | MR-04 | MR-13 | MR-18 |
| CL-19 | MR-06 | MR-11 | MR-17 | MR-05 | MR-09 | MR-07 |
| CL-20 | MR-10 | MR-17 | MR-11 | MR-12 | MR-04 | MR-01 |
| CL-21 | MR-06 | MR-10 | MR-08 | MR-18 | MR-13 | MR-12 |
| CL-22 | MR-10 | MR-15 | MR-14 | MR-12 | MR-18 | MR-05 |
| CL-23 | MR-08 | MR-14 | MR-15 | MR-05 | MR-07 | MR-04 |
| CL-24 | MR-08 | MR-03 | MR-14 | MR-09 | MR-18 | MR-13 |
| CL-25 | MR-03 | MR-17 | MR-14 | MR-12 | MR-07 | MR-09 |
| CL-26 | MR-03 | MR-06 | MR-10 | MR-16 | MR-13 | MR-01 |
| CL-27 | MR-03 | MR-02 | MR-06 | MR-01 | MR-16 | MR-13 |
| CL-28 | MR-17 | MR-11 | MR-02 | MR-01 | MR-16 | MR-12 |
| CL-29 | MR-11 | MR-03 | MR-06 | MR-13 | MR-07 | MR-05 |
| CL-30 | MR-17 | MR-02 | MR-14 | MR-13 | MR-09 | MR-07 |
| CL-31 | MR-06 | MR-11 | MR-15 | MR-01 | MR-05 | MR-07 |
| CL-32 | MR-08 | MR-14 | MR-15 | MR-09 | MR-01 | MR-04 |
| CL-33 | MR-14 | MR-17 | MR-03 | MR-07 | MR-18 | MR-09 |
| CL-34 | MR-10 | MR-11 | MR-02 | MR-07 | MR-12 | MR-16 |
| CL-35 | MR-02 | MR-15 | MR-17 | MR-04 | MR-01 | MR-16 |
| CL-36 | MR-02 | MR-17 | MR-11 | MR-12 | MR-07 | MR-09 |
| CL-37 | MR-10 | MR-14 | MR-03 | MR-07 | MR-12 | MR-01 |
| CL-38 | MR-08 | MR-02 | MR-06 | MR-18 | MR-09 | MR-04 |
| CL-39 | MR-02 | MR-03 | MR-15 | MR-09 | MR-05 | MR-07 |
| CL-40 | MR-14 | MR-08 | MR-06 | MR-18 | MR-16 | MR-04 |
| CL-41 | MR-15 | MR-14 | MR-08 | MR-18 | MR-04 | MR-01 |
| CL-42 | MR-02 | MR-10 | MR-17 | MR-09 | MR-16 | MR-12 |
| CL-43 | MR-11 | MR-15 | MR-03 | MR-07 | MR-05 | MR-09 |
| CL-44 | MR-02 | MR-14 | MR-17 | MR-16 | MR-04 | MR-01 |
| CL-45 | MR-15 | MR-08 | MR-10 | MR-04 | MR-01 | MR-12 |
| CL-46 | MR-03 | MR-06 | MR-17 | MR-05 | MR-09 | MR-13 |
| CL-47 | MR-06 | MR-11 | MR-10 | MR-13 | MR-05 | MR-16 |
| CL-48 | MR-08 | MR-02 | MR-15 | MR-01 | MR-04 | MR-18 |
| CL-49 | MR-10 | MR-15 | MR-06 | MR-04 | MR-12 | MR-16 |
| CL-50 | MR-15 | MR-17 | MR-08 | MR-05 | MR-13 | MR-09 |
| CL-51 | MR-02 | MR-08 | MR-03 | MR-18 | MR-16 | MR-12 |
| CL-52 | MR-06 | MR-02 | MR-08 | MR-09 | MR-13 | MR-18 |
| CL-53 | MR-14 | MR-17 | MR-08 | MR-16 | MR-12 | MR-18 |
| CL-54 | MR-14 | MR-17 | MR-10 | MR-04 | MR-05 | MR-07 |
| CL-55 | MR-15 | MR-10 | MR-08 | MR-01 | MR-16 | MR-05 |
| CL-56 | MR-03 | MR-06 | MR-10 | MR-07 | MR-09 | MR-13 |
| CL-57 | MR-11 | MR-10 | MR-14 | MR-12 | MR-09 | MR-16 |

### §11.3 Repeat structure and washout

The four repeats are drawn from first-pass positions 1–7 and appended at positions 20–23 in
ascending order of original position; pairing the k-th earliest original with position 19 + k gives
intervening(k) = 18 + k − o_(k) ≥ 15 because the k-th smallest of four positions drawn from 1–7 is at
most 3 + k. Realised separations are in Table 11.2-C. The end-of-session recognition question (§10)
flags recognised pairs CONTAMINATED; the contamination rate is a reported pilot output; intra-reviewer
stability is a secondary, pilot-informing metric under this protocol, not an acceptance criterion.

### §11.4 Self-containment of the specification `[N8]`

    THE PROTOCOL SPECIFICATION IS SELF-CONTAINED.
    PILOT EXECUTION REQUIRES AN EXACTLY IDENTIFIED, AUTHORIZED, CONFORMANT STUDY SURFACE.
    WHETHER THAT REQUIRES NEW EXECUTABLE IMPLEMENTATION: NOT YET PROVEN.

Every outcome-relevant fact a pilot needs is frozen in this file: the item texts (§7.2), the context
text (§6.2), the group assignment, per-reviewer sequences, H2 roles and repeat positions (§11.2), the
presentation orders (§12.5), the instruction packets (§12), the capture record (§13.1) and the
surface specification (§13.2). No off-repository artifact and no re-run of any generation procedure
is load-bearing. That is a statement about where protocol truth lives — not a claim that the pilot
can be executed without a study surface. The generation procedures are recorded for provenance only
(the seeded ID→arm mapping, 9 / 9; seeded load-balanced, constraint-checked item assignment per arm
group; seeded balanced role assignment; seeded shuffles for sequences, orders and rankings; repeats
from positions 1–7); re-running them is neither required nor authorized. None of these procedures
attaches a participant to an ID — that is settled only by the §6.1A post-commitment random draw.

---

## §12. Frozen instruction packets `[M5 repair: truthful disclosure]`

The packets below are the only instructions any participant receives. They are reproduced here in
full so that the study is self-contained; they are issued to participants as separate documents
without any other part of this file. A GROUP-A reviewer receives §12.1 only; a GROUP-B reviewer
receives §12.2 only; reference humans receive §12.3 for their arm (RA-x3 additionally §12.4).

### §12.1 Measured reviewer packet — GROUP-A (claim only)

    CLAIM REVIEW — INSTRUCTIONS

    Thank you for helping. Please read these once, in full, before you start. They are the only
    instructions you will receive; nobody will clarify them during the task, and that is
    deliberate.

    WHAT YOU ARE LOOKING AT
    You will see a series of short texts, one at a time. They are controlled, synthetic
    inventor-style answer texts prepared for this study: each was written to read like an
    inventor's answer to a question about how their system works. They were not taken from real
    users, and none describes a real person's project. Some are deliberately good, some
    deliberately poor, some odd. You will not be shown the question the texts answer. Judge only
    the text in front of you.

    WHAT YOU ARE DOING
    For each text you answer ONE question:
      Has the inventor articulated enough substantive mechanism content, in the words in front of
      you, to qualify this claim for mechanism progression?
    and you choose exactly one of four answers:
      SUFFICIENT · INSUFFICIENT · CANNOT ADJUDICATE · OUT OF SCOPE
    then tick at least one reason from the list on your form.

    SUFFICIENT — choose this when you can point to BOTH of these in the text itself:
      1. a specific condition, situation, input or measurement the system responds to; and
      2. a specific resulting system behaviour that follows from it.
    Plain, everyday language is completely fine. A very short text is fine. Shortness is never a
    reason to mark INSUFFICIENT if both parts are present. Length is never a reason to mark
    SUFFICIENT.

    INSUFFICIENT — choose this when one or both parts are missing, including when the text:
      - states a preference, an intention or a plan, without a condition and a behaviour;
      - gives only a category name, restates or acknowledges the question, just says "yes", or is
        short, empty or near-empty (a short or empty answer is still the inventor's answer — it is
        INSUFFICIENT, not a display problem);
      - fills one or both parts with generic filler ("when needed", "it handles it", "does the
        right thing");
      - reads as proper English but names nothing you can actually identify;
      - says the system "works", "handles it", "responds" or "behaves correctly" without saying
        what it responds to or what it does;
      - says the inventor does not know, has not decided or has not worked it out yet;
      - gives the condition or the behaviour only by pointing at something unspecified ("once the
        software decides", "whenever the reading calls for it") so that you cannot say what the
        condition or the behaviour actually is.

    CANNOT ADJUDICATE — choose this when you cannot reach one of the other answers. Tick the
    reason that applies:
      - "the text itself could honestly be read either way under these rules" — a word refers to
        something you cannot identify and your answer would change depending on what it is, or the
        rules genuinely do not settle this text;
      - "I recognise this text or its author from outside this study" (prior exposure);
      - "I have a conflict and am standing aside" (conflict / recusal);
      - "something in the process stopped me" — the item did not display properly (text cut off, an
        error, the same text twice, or anything that made the item unreadable as presented), or you
        have to disclose that one of the practical rules above was not kept for this item.
    Use it instead of guessing. It is NOT a polite way of saying INSUFFICIENT.

    OUT OF SCOPE — choose this only when the text is not an inventor's claim about their mechanism
    at all: it is in a language other than English; it is a question back to whoever asked, or a
    request or instruction aimed at you or at this review; or it is pasted material that is not a
    claim. It is NOT for claims that are merely bad, short or empty.

    WHAT YOU MUST NOT JUDGE
    This is the part people find hardest, so please read it twice. You are NOT judging whether the
    idea is any good. Do not let any of these affect your answer: whether the mechanism is
    technically correct; feasible or buildable; whether it would actually work; whether it has
    been tested or proven; whether an expert would approve of it; whether the invention is
    commercially sensible; whether it is safe; whether the inventor's conclusion is true; whether
    the inventor seems knowledgeable. A text can be clearly wrong or completely unworkable and
    still be SUFFICIENT, because it still articulated a condition and a resulting behaviour. That
    is the correct outcome.

    THINGS YOU MUST NOT DO
    - Do not invent missing details, even obvious ones.
    - Do not fill gaps from your own technical knowledge.
    - Do not read charitably to complete the explanation.
    - Do not treat a stated intention ("I want it to…") as mechanism content.
    - Do not treat plausible engineering as articulated evidence.
    - Do not treat tidy structure (numbered steps, technical words) as content by itself.
    - Do not reward length. Do not penalise shortness.
    - Do not use any tool, website, assistant, dictionary or other person. Work alone.

    PRACTICAL POINTS
    - Work in one sitting if you can; if you must break, break between items.
    - There is no time limit and no target speed, but please do not pause in the middle of an item.
    - You may add a short note explaining your reasoning. It is optional, it never changes your
      answer, and it helps us find places where these instructions were unclear. Please put no
      personal information in it.
    - Some texts may look similar to each other. Answer each one on its own terms.
    - Once you submit an answer you cannot go back to change it; check before you submit.
    - At the end we will show you the list of texts you saw and ask whether you think any of them
      appeared twice. Please answer honestly; it is useful evidence, not a problem.

    WHAT YOU AGREED TO BEFORE STARTING (summary of your consent)
    You agreed to this before you were enrolled, and it still applies:
    - PURPOSE: this is one part of an evidence gate that a software project must complete before it
      may rely on human review of inventor claims. Your answers are evidence about how well written
      instructions can be applied — not about you.
    - TASK: reading short texts and choosing one of four answers with a reason, as described above.
    - WHAT IS RECORDED: your answers, reason codes, optional notes, the times you started and
      submitted each item, your end-of-session recognition answers, and one background question.
    - PSEUDONYMOUS IDENTITY: the evidence records identify you only as MR-nn and contain no name,
      email, address or other identifying detail.
    - IDENTITY MAPPING: which person holds which ID is held separately, by an appointed study
      custodian, for consent, payment and withdrawal only, under minimum-necessary access. Nobody
      analysing the evidence can see it.
    - USE: the pseudonymous evidence is used for this evidence gate — its analysis, its governance
      and assurance review, audit, and the project owner's decisions about the gate. It is not used
      to train or tune models, for marketing, for product content, or for anything else.
    - RETENTION AND DELETION: the identity mapping is destroyed under the study's frozen retention
      rule once the study record is accepted or the study is abandoned, after a stated grace period
      for payment questions. What happens to your pseudonymous answers is set by the retention and
      privacy terms in your consent form together with the rules that apply to this study — they are
      neither automatically kept for ever nor automatically deleted, and the terms that decide it
      are fixed before you start.
    - WITHDRAWAL: you may withdraw at any time, without giving a reason and without affecting your
      compensation for work already done. After you withdraw you will not be asked for any further
      answers. What happens to answers you already gave is decided by the terms you agreed to and
      by the privacy rules that apply to this study — it is fixed in advance, not decided
      afterwards, and it is explained in your consent form.
    - CONFIDENTIALITY: please do not discuss any text with anyone, during or after.
    - TOOLS: please do not use any tool, website, assistant, dictionary or other person.
    - QUESTIONS OR CONCERNS: use the contact route given in your consent form.
    Your notes are stored word for word; please put no personal information in them.

### §12.2 Measured reviewer packet — GROUP-B (claim + question)

    CLAIM REVIEW — INSTRUCTIONS

    [Identical to the GROUP-A packet in every respect — including the CANNOT ADJUDICATE reasons and
    the consent summary — except the two passages below, which replace "WHAT YOU ARE LOOKING AT"
    and add the section "HOW YOU MAY USE THE QUESTION".]

    WHAT YOU ARE LOOKING AT
    You will see a series of short texts, one at a time, each shown together with the question
    it answers. The question is always the same:

      "Explain in everyday words how you imagine the system would notice the problem and respond."

    The texts are controlled, synthetic inventor-style answer texts prepared for this study: each
    was written to read like an inventor's answer to that question. They were not taken from real
    users, and none describes a real person's project. Some are deliberately good, some
    deliberately poor, some odd.

    HOW YOU MAY USE THE QUESTION
    The question MAY help you: understand what the inventor was being asked; work out what a word
    in the text refers to when the question makes that clear (for example, "the problem" in the
    text means the problem the question refers to, and "it" or "the system" means the inventor's
    system); and see which question is being answered.

    HOW YOU MUST NOT USE THE QUESTION
    The question MUST NOT be used to: supply a condition the text does not state; supply a
    behaviour the text does not state; supply something the text depends on but does not say; add
    any mechanism content that is not in the text; or turn a text that would otherwise be
    INSUFFICIENT into SUFFICIENT by completing it yourself. The question tells you what was asked.
    It never tells you what was answered.

    If you mark SUFFICIENT and the question helped you work out what a word referred to, tick the
    reason "used the question to resolve what a word refers to" and name the word.

### §12.3 Reference adjudicator packet (per arm)

    INDEPENDENT REFERENCE ADJUDICATION — INSTRUCTIONS

    You are an independent reference adjudicator. You are not one of the study's measured
    reviewers, and you are kept separate from them. Your judgments are study evidence of a
    different kind: they establish, against the written policy below, what each text's status IS
    under that policy, and they define the reference basis against which the reviewers' answers
    are later analysed. They are used for this evidence gate's analysis, governance review, audit
    and the project owner's decisions, and for nothing else.

    WHAT YOU ARE LOOKING AT
    You will see 57 short texts. They are controlled, synthetic inventor-style answer texts
    prepared for this study — written to read like inventors' answers to a question about how
    their system works; not taken from real users.
    [ARM-A packet: you will see the texts alone, without the question. Judge only the words in
    front of you.]
    [ARM-B packet: you will see each text together with the exact question it answers:
    "Explain in everyday words how you imagine the system would notice the problem and respond."
    Apply the CONTEXT RULE below.]

    THE POLICY
    You judge ONE question: is enough mechanism content actually articulated in the text in front
    of you? The policy is about what the words say, not about whether what they say is right.

    SUFFICIENT — reading the words of the text, you can identify BOTH
      E1 a specific condition, situation, input or measurement that the system responds to; AND
      E2 a specific resulting system behaviour that follows from it.
    Both must be present as stated content. Ordinary language is fine. Brevity does not
    disqualify. Length does not qualify.

    INSUFFICIENT — E1 or E2 is absent, including when the text
      F1 states a preference, intention or plan without a condition→behaviour pair;
      F2 names only a category, restates or acknowledges the question, confirms without content,
         or is empty / near-empty (a short or empty answer is INSUFFICIENT, not a display problem);
      F3 uses only generic filler for the condition, the behaviour or both;
      F4 is grammatically well-formed but carries no identifiable referents;
      F5 asserts that the system works / handles it / responds / behaves correctly without stating
         what it responds to or what it does;
      F6 explicitly states that the inventor does not know or has not worked out E1 or E2;
      F7 gives E1 or E2 only as a reference to an unspecified decision, signal, module, algorithm
         or setting whose own content is not stated.

    CONTEXT RULE (ARM-B only). The question MAY clarify scope, resolve a bounded referent ("the
    problem", "it", "the system") and clarify what was asked. It MUST NOT invent a missing
    condition, invent missing behaviour, invent a missing dependency, supply mechanism content the
    text lacks, or convert an insufficient text to sufficient by completion.

    REFERENCE-INDETERMINATE — the text's status is genuinely arguable under E and F: a careful
    reader applying this policy in good faith could land either way. This is a real verdict, not a
    failure. Use it whenever you would otherwise have to guess. Do not force a text into SUFFICIENT
    or INSUFFICIENT to avoid it.

    OUT OF SCOPE — the text is not adjudicable as an inventor mechanism claim under this protocol:
    not English; a question back to the asker or a request / instruction aimed at the reviewer or
    the review; or pasted non-claim material. Not for texts that are merely bad, short or empty.

    CANNOT ADJUDICATE — use this ONLY when something outside the text stops you: you recognise the
    text, its author or a label for it from outside the study (prior exposure); you have a conflict
    and are standing aside (conflict / recusal); or the process failed — the item did not display
    properly, or one of the practical rules above was not kept for this item and you are disclosing
    it. It is an abstention about you or the process, never a verdict about the text. If the difficulty is in the text itself — a word you cannot pin down whose
    meaning would change your verdict, or a policy that genuinely does not settle this text — that
    is REFERENCE-INDETERMINATE, not CANNOT ADJUDICATE.

    WHAT YOU MUST NOT JUDGE — technical correctness, feasibility, whether it would work, whether it
    is proven, whether a specialist would approve, commercial sense, safety, whether the inventor's
    conclusion is true, whether the inventor seems knowledgeable. A text can be clearly wrong or
    unbuildable and still be SUFFICIENT.

    THINGS YOU MUST NOT DO — invent missing details; fill gaps from your own knowledge; read
    charitably to complete the explanation; treat a stated intention as mechanism content; treat
    plausible engineering as articulated evidence; treat tidy structure as content; reward length;
    penalise shortness; use any tool, website, assistant, dictionary or other person; discuss any
    text with anyone.

    FOR EVERY TEXT, RECORD
      1. the verdict: SUFFICIENT, INSUFFICIENT, REFERENCE-INDETERMINATE, OUT OF SCOPE, or the
         abstention CANNOT ADJUDICATE;
      2. the governing policy clause: E1+E2, F1, F2, F3, F4, F5, F6, F7, or INDETERMINATE —
         required for every verdict including indeterminate ones (not required for an abstention);
      3. at least one reason code from the list on your form;
      4. a short rationale (one or two sentences) pointing at what is or is not in the text.

    WHAT YOU ARE NOT SHOWN, AND WHY — any label anyone else assigned to these texts, any grouping
    they belong to, why any text was written, or any reviewer's answers. That is what makes your
    adjudication independent. If you learn any of it before you finish, stop and say so.

    Once you submit a verdict you cannot go back to change it. The consent summary in your consent
    form applies to you in the same terms as to the study's reviewers (purpose, task, what is
    recorded, pseudonymous identity, separately held identity mapping, use for this evidence gate
    and its governance / assurance review, audit and owner decisions, retention and deletion,
    withdrawal, confidentiality, tool restrictions and the contact route) — with the difference
    already stated above: your verdicts are the reference basis of the gate, so they are study
    evidence, not measured-reviewer outcome data. As for the reviewers, what happens to verdicts you
    have already given is set by the retention and privacy terms in your consent form together with
    the rules that apply to this study — they are neither automatically kept for ever nor
    automatically deleted, and the terms that decide it are fixed before you start. You may withdraw
    at any time. Put no personal information in your rationales.

### §12.4 Third adjudicator packet (RA-A3 / RA-B3)

    Same packet as §12.3 for your arm, with this addition: you will see only the texts on which
    the two first-pass adjudicators did not reach a shared verdict. You are NOT told what either of
    them chose, nor which of them abstained, nor how many texts the full study contains. Adjudicate
    each text exactly as if you were the first to see it. Your texts are presented in the frozen
    ranking of Table 12.5-B for your arm, escalated texts only, ranks preserved.

### §12.5 Frozen presentation orders `[N4 repair]`

Every outcome-relevant presentation order is an exact frozen table below. No order is generated
later, fixed at packet issue, or defined by a procedure or PRNG description. Measured reviewers'
item order is Table 11.2-B; the three tables here complete the set.

**Table 12.5-A — frozen reference first-pass presentation order (all 57 items, position 1 → 57).**

| Adjudicator | Frozen presentation order |
|---|---|
| RA-A1 | CL-14 · CL-04 · CL-39 · CL-18 · CL-21 · CL-47 · CL-31 · CL-30 · CL-43 · CL-41 · CL-26 · CL-50 · CL-51 · CL-56 · CL-34 · CL-44 · CL-33 · CL-42 · CL-48 · CL-01 · CL-03 · CL-27 · CL-46 · CL-24 · CL-53 · CL-32 · CL-20 · CL-22 · CL-45 · CL-07 · CL-08 · CL-16 · CL-28 · CL-19 · CL-02 · CL-05 · CL-52 · CL-35 · CL-54 · CL-09 · CL-40 · CL-55 · CL-25 · CL-36 · CL-23 · CL-12 · CL-15 · CL-29 · CL-10 · CL-38 · CL-37 · CL-57 · CL-49 · CL-11 · CL-17 · CL-13 · CL-06 |
| RA-A2 | CL-28 · CL-07 · CL-50 · CL-42 · CL-26 · CL-09 · CL-11 · CL-17 · CL-12 · CL-54 · CL-04 · CL-37 · CL-51 · CL-20 · CL-41 · CL-34 · CL-44 · CL-06 · CL-35 · CL-40 · CL-15 · CL-30 · CL-21 · CL-14 · CL-38 · CL-33 · CL-27 · CL-10 · CL-39 · CL-48 · CL-01 · CL-56 · CL-02 · CL-46 · CL-29 · CL-03 · CL-36 · CL-49 · CL-53 · CL-19 · CL-43 · CL-23 · CL-31 · CL-32 · CL-55 · CL-22 · CL-57 · CL-13 · CL-16 · CL-24 · CL-08 · CL-45 · CL-47 · CL-52 · CL-25 · CL-18 · CL-05 |
| RA-B1 | CL-51 · CL-44 · CL-46 · CL-43 · CL-04 · CL-14 · CL-32 · CL-21 · CL-13 · CL-47 · CL-02 · CL-06 · CL-09 · CL-35 · CL-11 · CL-07 · CL-01 · CL-38 · CL-10 · CL-29 · CL-41 · CL-52 · CL-17 · CL-33 · CL-25 · CL-08 · CL-27 · CL-23 · CL-31 · CL-34 · CL-57 · CL-42 · CL-19 · CL-05 · CL-18 · CL-40 · CL-28 · CL-45 · CL-03 · CL-49 · CL-12 · CL-53 · CL-22 · CL-26 · CL-48 · CL-56 · CL-36 · CL-16 · CL-24 · CL-39 · CL-37 · CL-54 · CL-30 · CL-15 · CL-20 · CL-55 · CL-50 |
| RA-B2 | CL-11 · CL-22 · CL-47 · CL-03 · CL-16 · CL-10 · CL-36 · CL-24 · CL-12 · CL-27 · CL-29 · CL-37 · CL-42 · CL-43 · CL-57 · CL-05 · CL-31 · CL-56 · CL-13 · CL-23 · CL-54 · CL-07 · CL-08 · CL-53 · CL-40 · CL-15 · CL-41 · CL-04 · CL-01 · CL-34 · CL-30 · CL-49 · CL-48 · CL-39 · CL-28 · CL-25 · CL-35 · CL-20 · CL-45 · CL-26 · CL-50 · CL-06 · CL-32 · CL-18 · CL-17 · CL-09 · CL-21 · CL-46 · CL-14 · CL-33 · CL-38 · CL-55 · CL-51 · CL-44 · CL-19 · CL-52 · CL-02 |

**Table 12.5-B — frozen third-adjudicator full ranking (rank 1 → 57). The escalated subset is presented in this ranking order, escalated items only, ranks preserved.**

| Adjudicator | Frozen full ranking |
|---|---|
| RA-A3 | CL-44 · CL-57 · CL-20 · CL-16 · CL-35 · CL-53 · CL-10 · CL-31 · CL-12 · CL-02 · CL-22 · CL-48 · CL-18 · CL-49 · CL-43 · CL-28 · CL-51 · CL-08 · CL-07 · CL-25 · CL-39 · CL-56 · CL-21 · CL-54 · CL-37 · CL-15 · CL-14 · CL-30 · CL-09 · CL-23 · CL-42 · CL-52 · CL-33 · CL-45 · CL-40 · CL-01 · CL-13 · CL-32 · CL-26 · CL-50 · CL-36 · CL-17 · CL-04 · CL-47 · CL-06 · CL-38 · CL-41 · CL-19 · CL-24 · CL-29 · CL-27 · CL-55 · CL-46 · CL-11 · CL-05 · CL-34 · CL-03 |
| RA-B3 | CL-28 · CL-42 · CL-34 · CL-45 · CL-21 · CL-39 · CL-56 · CL-18 · CL-38 · CL-27 · CL-17 · CL-26 · CL-19 · CL-20 · CL-22 · CL-25 · CL-31 · CL-30 · CL-12 · CL-15 · CL-13 · CL-49 · CL-08 · CL-06 · CL-41 · CL-23 · CL-29 · CL-54 · CL-51 · CL-46 · CL-47 · CL-40 · CL-02 · CL-43 · CL-09 · CL-53 · CL-52 · CL-11 · CL-33 · CL-24 · CL-14 · CL-04 · CL-05 · CL-55 · CL-48 · CL-07 · CL-01 · CL-37 · CL-36 · CL-35 · CL-03 · CL-50 · CL-44 · CL-16 · CL-32 · CL-10 · CL-57 |

**Table 12.5-C — frozen end-of-session recognition-list order (the reviewer's own 19 first-pass items).**

| Reviewer | Frozen recognition-list order (19 items) |
|---|---|
| MR-01 | CL-27 · CL-32 · CL-08 · CL-55 · CL-17 · CL-28 · CL-15 · CL-31 · CL-48 · CL-35 · CL-14 · CL-20 · CL-06 · CL-41 · CL-26 · CL-03 · CL-45 · CL-37 · CL-44 |
| MR-02 | CL-34 · CL-12 · CL-13 · CL-48 · CL-42 · CL-51 · CL-30 · CL-28 · CL-38 · CL-52 · CL-27 · CL-07 · CL-44 · CL-08 · CL-10 · CL-39 · CL-35 · CL-05 · CL-36 |
| MR-03 | CL-29 · CL-08 · CL-03 · CL-39 · CL-13 · CL-25 · CL-27 · CL-09 · CL-17 · CL-51 · CL-37 · CL-05 · CL-56 · CL-26 · CL-33 · CL-02 · CL-46 · CL-24 · CL-43 |
| MR-04 | CL-48 · CL-16 · CL-45 · CL-38 · CL-20 · CL-04 · CL-02 · CL-05 · CL-09 · CL-40 · CL-49 · CL-44 · CL-41 · CL-18 · CL-32 · CL-35 · CL-08 · CL-23 · CL-54 |
| MR-05 | CL-08 · CL-11 · CL-43 · CL-07 · CL-47 · CL-46 · CL-55 · CL-23 · CL-31 · CL-05 · CL-22 · CL-39 · CL-29 · CL-01 · CL-50 · CL-19 · CL-15 · CL-54 · CL-06 |
| MR-06 | CL-21 · CL-11 · CL-47 · CL-52 · CL-19 · CL-49 · CL-38 · CL-56 · CL-18 · CL-16 · CL-27 · CL-29 · CL-26 · CL-04 · CL-06 · CL-40 · CL-46 · CL-31 · CL-03 |
| MR-07 | CL-36 · CL-07 · CL-33 · CL-34 · CL-39 · CL-56 · CL-31 · CL-23 · CL-19 · CL-37 · CL-12 · CL-43 · CL-11 · CL-25 · CL-54 · CL-10 · CL-06 · CL-30 · CL-29 |
| MR-08 | CL-53 · CL-07 · CL-23 · CL-05 · CL-52 · CL-38 · CL-45 · CL-09 · CL-50 · CL-21 · CL-16 · CL-51 · CL-41 · CL-40 · CL-55 · CL-32 · CL-24 · CL-08 · CL-48 |
| MR-09 | CL-30 · CL-24 · CL-38 · CL-03 · CL-56 · CL-32 · CL-39 · CL-16 · CL-46 · CL-36 · CL-52 · CL-25 · CL-57 · CL-13 · CL-43 · CL-19 · CL-33 · CL-50 · CL-42 |
| MR-10 | CL-56 · CL-49 · CL-42 · CL-26 · CL-04 · CL-20 · CL-14 · CL-55 · CL-34 · CL-37 · CL-47 · CL-02 · CL-12 · CL-21 · CL-54 · CL-22 · CL-18 · CL-45 · CL-57 |
| MR-11 | CL-18 · CL-43 · CL-10 · CL-06 · CL-20 · CL-47 · CL-01 · CL-57 · CL-11 · CL-16 · CL-14 · CL-36 · CL-19 · CL-28 · CL-29 · CL-31 · CL-15 · CL-34 · CL-07 |
| MR-12 | CL-57 · CL-45 · CL-34 · CL-20 · CL-36 · CL-51 · CL-21 · CL-53 · CL-04 · CL-28 · CL-42 · CL-22 · CL-05 · CL-14 · CL-07 · CL-49 · CL-25 · CL-15 · CL-37 |
| MR-13 | CL-26 · CL-52 · CL-27 · CL-17 · CL-01 · CL-21 · CL-29 · CL-13 · CL-47 · CL-11 · CL-03 · CL-24 · CL-18 · CL-14 · CL-09 · CL-46 · CL-50 · CL-30 · CL-56 |
| MR-14 | CL-13 · CL-41 · CL-15 · CL-54 · CL-33 · CL-23 · CL-25 · CL-10 · CL-30 · CL-44 · CL-37 · CL-40 · CL-09 · CL-57 · CL-24 · CL-53 · CL-32 · CL-22 · CL-17 |
| MR-15 | CL-32 · CL-02 · CL-35 · CL-43 · CL-48 · CL-49 · CL-31 · CL-50 · CL-03 · CL-17 · CL-23 · CL-15 · CL-45 · CL-01 · CL-39 · CL-22 · CL-41 · CL-06 · CL-55 |
| MR-16 | CL-27 · CL-02 · CL-51 · CL-17 · CL-12 · CL-26 · CL-49 · CL-10 · CL-53 · CL-28 · CL-55 · CL-35 · CL-34 · CL-40 · CL-57 · CL-42 · CL-01 · CL-47 · CL-44 |
| MR-17 | CL-19 · CL-42 · CL-28 · CL-20 · CL-44 · CL-35 · CL-54 · CL-30 · CL-01 · CL-53 · CL-36 · CL-14 · CL-46 · CL-04 · CL-12 · CL-25 · CL-50 · CL-33 · CL-11 |
| MR-18 | CL-48 · CL-21 · CL-18 · CL-12 · CL-24 · CL-02 · CL-09 · CL-40 · CL-53 · CL-16 · CL-41 · CL-51 · CL-13 · CL-38 · CL-33 · CL-52 · CL-10 · CL-22 · CL-04 |

---

## §13. Capture record and study-surface specification

### §13.1 Capture record (data representation, not a schema implementation)

One record per rating, captured on the study surface specified in §13.2 (a separately authorized
non-production surface; no product schema, no `ClaimEligibilityEvent`, no `AssertionRecord`).

| Field | Values / rule |
|---|---|
| `protocol_version` | `CLAIM-ELIGIBILITY-HUMAN-REVIEW-PREPILOT-EN-v1` (constant) |
| `eligibility_policy_version` | `CLAIM-ELIGIBILITY-SUFFICIENCY-EN-v1` (constant) |
| `participant_id` | `MR-nn` (measured) · `RA-A1 / RA-A2 / RA-A3 / RA-B1 / RA-B2 / RA-B3` (reference); pseudonymous; no PII anywhere |
| `role` | `MEASURED` · `REFERENCE_FIRST_PASS` · `REFERENCE_THIRD` |
| `arm` | `A` · `B` (fixed per participant) |
| `position` | integer position in the participant's frozen sequence |
| `claim_id` | `CL-01` … `CL-57` |
| `context_id` | `Q-CTX-01` when arm = B; empty when arm = A |
| `is_repeat` | boolean (measured only; from the frozen sequence, never participant-declared) |
| `presentation_status` | `OK` · `DEFECT` — set by the surface's own uniform integrity check (§13.2 items 4 / 19) and, independently, by the participant's `RC-CA-04` selection; both are stored |
| `label` | measured: one of the four study labels · reference: one of the five |
| `policy_clause` | reference only: `E1+E2 / F1 … F7 / INDETERMINATE`; empty on CANNOT_ADJUDICATE |
| `reason_codes` | one or more `RC-*` codes from §5 (at least one); the reference lane never carries `RC-CA-02`, the measured lane never carries `RC-RI-01` |
| `abstention_class` | derived, not participant-entered: `CA-EXTRINSIC` (`RC-CA-01` / `RC-CA-03` / `RC-CA-04`) · `CA-INTRINSIC` (`RC-CA-02`, measured lane only) · empty when the label is not CANNOT_ADJUDICATE |
| `referent_resolved` | free text, required when `RC-S-02` is ticked |
| `rationale` | optional (measured) / required, ≤ 2 sentences (reference, except abstention) ; verbatim; never overrides the label |
| `started_at`, `submitted_at` | ISO-8601 UTC, set by the surface, not by the participant |
| `end_of_session_recognition` | measured only, captured once: the list of `claim_id`s the reviewer believes appeared twice |
| `domain_background` | covariate: `none / some / professional` (captured once per participant, after all ratings) |
| `h2_role` | derived at analysis time from Table 11.2-D; NOT shown to and NOT stored by the participant-facing surface |

Constraints: no label value outside the vocabularies; an unanswered item is MISSING, never
imputed; no sealed metadata, family, MP role, H2 role or reference outcome is present in any
participant-facing record; each exported capture-record set (reference lane first, then measured
lane) is hashed at its freeze — SHA-256 over the exact bytes of the §13.2 item 26 export — and the
hashes are reported in the pilot record. Those RAW ADJUDICATOR / MEASURED RATING RECORD SET HASHES
are distinct identities from the REFERENCE-FREEZE ARTIFACT HASH of §8.3A `[RZ-4]`.

### §13.2 Non-executable study-surface specification `[M9 repair — SPECIFICATION ONLY]`

    SURFACE SPECIFICATION != SURFACE IMPLEMENTATION
    THIS SECTION IS NOT IMPLEMENTATION AUTHORITY

Every outcome-relevant interaction is fixed below. ANY LATER AUTHORIZED STUDY-SURFACE REALIZATION
MUST CONFORM TO EVERY FROZEN OUTCOME-RELEVANT INVARIANT BELOW, whatever form it takes; this protocol
names, prefers and excludes no realization technology `[RZ-7]`. Conformance is verified before any
pilot (§13.3).

1. **What measured reviewers see.** One item at a time: the claim text panel (item 4); in ARM-B
   only, the question panel (item 5); the label control (item 10); the reason-code control (item
   8); the optional rationale field (item 12); the submit control (item 13); a neutral progress
   indicator "Item n of 23" with no other counter. Nothing else about the item.
2. **What reference adjudicators see.** As item 1, plus the policy-clause control (required for
   every verdict other than CANNOT_ADJUDICATE) and a required rationale field; progress "Item n of
   57" (first pass) or "Item n of k" (third role, k = escalated count).
3. **What remains hidden from every participant.** Item IDs, families, MP groups and roles, sealed
   labels and bases, the G-4-A flag, H2 roles, repeat status, arm labels, the other arm's existence,
   any other participant's data, any reference outcome, any timestamp, any protocol text.
4. **Claim presentation `[N5]`.** The frozen text of §7.2, byte-identical, in a single plain-text
   panel with a fixed monospace-free readable font, no truncation, no wrapping-induced loss, no
   highlighting, no emphasis, no spell-check underlining, no hyperlinking, no auto-correction. The
   panel, its chrome, its dimensions and every surrounding element are IDENTICAL FOR EVERY ITEM and
   are in no way conditioned on the claim's length, content or family: no marker, note, badge,
   placeholder, warning or completeness cue is ever shown for short, empty or unusual items. The
   surface performs the SAME content-integrity check on EVERY item (comparing the rendered text with
   the frozen text hash) before enabling submit; the check is silent when it passes and, when it
   fails, sets `presentation_status = DEFECT` and shows the neutral error state of item 19.
5. **Question / context presentation.** ARM-B only: the byte-exact `Q-CTX-01` text in a panel
   labelled "The question the inventor was answering:", shown above the claim on every item,
   identically for every item. ARM-A: no question panel, no placeholder, no mention of a question.
6. **Arm indication.** No arm label is shown to any participant; GROUP-B participants infer
   nothing beyond the presence of the question panel; GROUP-A participants are never told a
   question exists.
7. **Item order `[N4]`.** Exactly the participant's frozen order: Table 11.2-B for measured
   reviewers; Table 12.5-A for reference first-pass adjudicators; Table 12.5-B for a third
   adjudicator (that arm's full ranking, escalated items only, ranks preserved and gaps closed
   without reordering). No reordering, no skipping, no adaptive selection, and no order generated
   at packet issue or at run time.
8. **Reason-code presentation.** Reason codes are shown as plain-language checkboxes grouped
   under the currently selected label only (the groups of §5 for the four labels; `RC-RI-01` for
   REFERENCE-INDETERMINATE); the codes for other labels are not visible; the wording shown is the
   §5 meaning text without the code identifiers; group order and within-group order are fixed as
   in §5.
9. **Single / multiple reason codes.** Multiple selection is permitted within the selected label's
   group; at least one is required; changing the label clears the selected reason codes.
10. **Label-selection behaviour.** Exactly one of the four (measured) or five (reference) labels
    via mutually exclusive controls, presented in the fixed order SUFFICIENT, INSUFFICIENT,
    CANNOT ADJUDICATE, OUT OF SCOPE (reference: SUFFICIENT, INSUFFICIENT, REFERENCE-INDETERMINATE,
    OUT OF SCOPE, CANNOT ADJUDICATE); no default selection; no keyboard shortcut that selects a
    label without an explicit confirmation.
11. **Required / optional fields.** Required: label; ≥ 1 reason code; for reference verdicts other
    than CANNOT_ADJUDICATE, policy clause and rationale; `referent_resolved` when `RC-S-02` is
    selected. Optional: measured rationale. Submit is disabled until required fields are complete.
12. **Free-text rationale behaviour.** Plain text, up to 500 characters, no formatting, stored
    verbatim; a fixed hint "Please do not include personal information." is shown; the field never
    alters or validates the label.
13. **Submit / commit behaviour.** One explicit submit action per item; on submit the record (§13.1)
    is written atomically with `submitted_at`; the next item is shown only after a successful
    write; a failed write shows the error state of item 19 and does not advance.
14. **Changing an answer before submit.** Permitted without limit; only the final state is stored;
    no intermediate selections are recorded.
15. **Changing a submitted answer.** Not permitted. No edit, no undo, no re-open, for any participant
    or operator.
16. **Back-navigation.** Not available: no back control, browser back or equivalent returns to the
    current item unchanged.
17. **Forward-navigation.** Only by submitting the current item; no skip.
18. **Missing-item behaviour.** An item that is never submitted (withdrawal, abandonment) is
    recorded as MISSING with no label and no timestamps beyond `started_at` if shown; never
    imputed; the sequence is never re-issued to another participant.
19. **Broken / incomplete presentation behaviour.** On any integrity failure (text-hash mismatch,
    missing question panel in ARM-B, load or render failure) the surface shows a neutral error
    state "This item could not be displayed correctly." with a single control "Record that this
    item could not be displayed" which stores `presentation_status = DEFECT`, label
    CANNOT_ADJUDICATE and reason `RC-CA-04`, then advances; the participant may also select
    CANNOT_ADJUDICATE / `RC-CA-04` manually on any item they judge defective.
20. **Timeout behaviour.** None per item. A session idle for more than 60 minutes is suspended
    (item 21) and can be resumed; no answer is auto-submitted.
21. **Session interruption.** An interrupted session keeps every submitted record; the current
    unsubmitted item is discarded without storage and re-shown on resume.
22. **Resume behaviour.** Resume continues at the first unsubmitted position of the frozen
    sequence; the same items, same order; the participant is told "You are continuing from item n
    of 23."; no summary of earlier answers is shown.
23. **Repeat behaviour.** Repeats are presented exactly like first-pass items with no marker; the
    surface never reveals repeat status.
24. **Recognition-question behaviour `[N4]`.** After the final item of the session (measured only)
    the surface lists the 19 distinct claim texts the reviewer saw, in the exact frozen order of
    Table 12.5-C for that reviewer, each with a checkbox "I think this appeared twice"; multiple
    selection allowed; may be submitted empty; it is never shown before the last item.
25. **Capture behaviour and timestamps.** `started_at` is set when the item is first fully
    displayed; `submitted_at` on successful submit; UTC, millisecond precision; server- or
    form-clock, never participant-entered; per-item elapsed time is derived, not stored.
26. **Export and record canonicalisation.** Export is one UTF-8 JSON Lines file per record set
    (reference; measured), one record per line, fields in the fixed §13.1 order, sorted by
    (`participant_id`, `position`), no whitespace variation; the SHA-256 of that byte stream is the
    record-set hash. Export happens once per set at freeze; later exports must reproduce the same
    bytes.
27. **Pseudonymous participant display.** The surface shows the participant only their own
    pseudonymous ID on the welcome and completion pages; never a name; never another ID.
28. **Error messaging.** Neutral wording only; no message names a label, a reason code, a
    policy clause or the study design; validation messages say only which required field is
    missing.
29. **Accessibility `[N5]`.** Text resizable to 200 % without truncation or loss of any displayed
    content; label and reason controls operable by keyboard; no colour-only distinctions; no
    time-based element. Any assistive rendering must preserve the byte-exact claim text and must
    introduce no element conditioned on claim length or content.
30. **Operator boundary `[N1]`.** The operator ISSUES NO IDENTITIES: participant IDs are drawn and
    issued solely by the custodian (§6.1A E4). Operator access is limited to activating a session
    for an ID the custodian has already issued (serving that ID's frozen materials), suspension /
    resume, and export. No operator action can view, alter, reorder, re-issue or delete a submitted
    record, a sequence or an ID, and the operator has no access to the enrolment log. Every operator
    action is logged with UTC time and is part of the pilot record.
31. **Domain-background question.** Asked once, on the completion page after the recognition
    question; three options; may be left blank (recorded as `unknown`).
32. **Consent gate `[N1 / N6]`.** Consent is obtained and recorded BEFORE enrolment and before any
    participant ID exists (§6.1A E2, §21.2); the surface therefore opens on an ID that already
    carries a completed consent and commitment record, re-displays the consent summary of §12 for
    reference, and requires one explicit affirmative confirmation before the first item. A refusal
    or non-confirmation ends the session immediately with no rating record, and is reported to the
    custodian as a withdrawal before start.
33. **Label-control order.** The label controls appear in the fixed order of item 10 for every item
    and every participant; the reference lane's REFERENCE-INDETERMINATE and CANNOT ADJUDICATE
    controls are separated by a rule and carry their §4A meanings verbatim as their on-screen
    helper text.

### §13.3 Surface realisation status and sequencing `[M9]`

    PROTOCOL SPECIFICATION != EXECUTABLE STUDY SURFACE
    THE PROTOCOL SPECIFICATION IS SELF-CONTAINED.
    PILOT EXECUTION REQUIRES AN EXACTLY IDENTIFIED, AUTHORIZED, CONFORMANT STUDY SURFACE.
    WHETHER THAT REQUIRES NEW EXECUTABLE IMPLEMENTATION: NOT YET PROVEN.

Read-only check at the drafting base `[EXEC]`: no study, survey or adjudication surface is
identified in the repository. The web templates under `web/templates/` and `web/static/` are the
product surfaces of the served application (session, deliverable, decision workspace, account and
authentication pages); none was examined against the §13.2 invariants and none is authorized for
study use. No search of surfaces outside this repository was performed or authorized.

    EXISTING CONFORMANT STUDY SURFACE: NOT PROVEN — no candidate surface has been identified and
      proven conformant; this records the absence of proof, not proof of absence
    NEW EXECUTABLE STUDY SURFACE REQUIRED: NOT YET PROVEN REQUIRED — it does not become "required"
      merely because no surface has yet been identified `[N8]`
    EXECUTABLE SURFACE WORK PERFORMED: NO
    INDEPENDENT REVIEW B AS FINAL PRE-EXECUTION ASSURANCE: NOT AVAILABLE until the applicable exact
      surface assurance subject exists (§23)

Two admissible later routes, neither authorized here:

    ROUTE 1 — an already-authorized existing surface is later identified: it must be proven
      conformant INVARIANT BY INVARIANT against every numbered invariant of §13.2, on exact
      read-only evidence naming the surface's identity and version / SHA. If proven:
      `NEW SURFACE IMPLEMENTATION REQUIRED: NO`.
    ROUTE 2 — no authorized existing surface can conform: RETURN FOR SEPARATE OWNER SURFACE
      AUTHORIZATION. This protocol does not preselect, prefer or exclude any realisation route or
      technology `[N8]`; whatever is later authorized must satisfy every numbered invariant of
      §13.2 and is a new artifact that this protocol does not authorize.

Required later sequence (none of it authorized here): SURFACE IDENTIFICATION OR SEPARATE OWNER
IMPLEMENTATION AUTHORIZATION → EXACT SURFACE (identified or implemented) → SURFACE-CONFORMANCE
VERIFICATION against every invariant of §13.2 → INDEPENDENT REVIEW OF THE EXACT PRE-EXECUTION
SUBJECT (frozen protocol + exact surface identity / version + conformance evidence) or a mandatory
differential invariant recheck as later authorized → OWNER PILOT AUTHORIZATION (D5). No pilot may
execute on a materially load-bearing surface introduced after the last applicable independent
assurance review.

---

## §14. Metric and analysis-set contract `[PROPOSAL; M7 + N2 + N7 repairs]`

### §14.1 Frozen analysis sets and reference bases

**Source sets.**

    SOURCE-ITEM SET S_P (45 corpus items): CL-01 – CL-36 and CL-49 – CL-57 — every corpus item
      that is not a paraphrase / minimal-pair sibling
    SIBLING SET S_S (12 corpus items): CL-37 – CL-48 (the six PP and six MC siblings)
    S_P: PRIMARY ERROR-RATE SOURCE SET
    S_S: EXCLUDED FROM ERROR RATES ENTIRELY — construct / robustness axis only (M-09, M-10, §18)
    REPEATS: STABILITY ONLY (M-08)
    ALL-ITEM (S_P ∪ S_S) ERROR ANALYSIS: REMOVED — NOT PART OF THIS PROTOCOL `[N7]`. No error rate,
      primary or secondary, is computed over any set containing a paraphrase or minimal-pair
      sibling, so no sibling is ever represented as an independent source item and no analysis
      depends on a promised sibling-dependence correction. The construct axis (M-09, M-10, §18) is
      the only place siblings enter, and it computes no error rate.

**Per-arm operational reference bases `[N2]`.** Each arm's operational error rates are computed
against that arm's own effective reference, because that is the reference an operating source in
that condition would face:

    FS_A uses Ref_A(i) = INSUFFICIENT      FI_A uses Ref_A(i) = SUFFICIENT
    FS_B uses Ref_B(i) = INSUFFICIENT      FI_B uses Ref_B(i) = SUFFICIENT
    PRIMARY FS ITEM SET (arm x): { i ∈ S_P : Ref_x(i) = INSUFFICIENT }
    PRIMARY FI ITEM SET (arm x): { i ∈ S_P : Ref_x(i) = SUFFICIENT }
    PRIMARY H2 ERROR ITEM SETS: the same two sets, evaluated at study-item level under the frozen
      roles (§8.2)
    PRIMARY G-4-A CONDITIONAL ERROR ITEM SET (arm x): PRIMARY FS ITEM SET (arm x) ∩ sealed G4A = Y
      (sealed candidates: CL-09, CL-10, CL-12, CL-14, CL-17, CL-19, CL-21 – CL-27, CL-51, CL-52;
      membership is fixed by the effective reference, not by the sealed label)
    PRIMARY GENUINE-EVIDENCE-WITHHELD ANALOGUE SET (arm x): PRIMARY FI ITEM SET (arm x) ∩ text
      carries a causal / conditional connective (sealed candidates: CL-01, CL-02, CL-04,
      CL-33 – CL-36, CL-54, CL-55)
    EXCLUDED FROM EVERY ERROR SET: repeats; S_S items; study items whose arm reference is
      REFERENCE-INDETERMINATE or OUT_OF_SCOPE; study items carrying RU (process-unresolved, §8.3),
      which have no reference outcome at all

**Common comparative strata `[N2 — binding]`.** Between-arm comparisons never difference rates
taken over incomparable arm-specific item sets. Two common strata are frozen:

    C_I = { i ∈ S_P : Ref_A(i) = INSUFFICIENT AND Ref_B(i) = INSUFFICIENT }
    C_S = { i ∈ S_P : Ref_A(i) = SUFFICIENT   AND Ref_B(i) = SUFFICIENT }
    (both strata are built only from actual reference outcomes; an RU in either arm removes the
     item from both strata and from A_C, and it is reported in the process-disposition register)

    Δ_FS_COMMON = FS_B(C_I) − FS_A(C_I)
    Δ_FI_COMMON = FI_B(C_S) − FI_A(C_S)

    DIFFERENCING FS OR FI OVER ARM-SPECIFIC SETS: PROHIBITED
    C_I / C_S SIZES ARE REPORTED BEFORE ANY MEASURED OUTCOME IS COLLECTED, together with the count
      of S_P items excluded from each stratum and why — discordance, indeterminacy, out-of-scope
      or RU (§14.2 M-19)

**Common adjudicable source-item corpus for the marginal exact-S / sufficient-issuance estimand
`[N2 / PF-04]`.**

    A_C = { i ∈ S_P : Ref_A(i) ∈ {SUFFICIENT, INSUFFICIENT, REFERENCE-INDETERMINATE} AND
                      Ref_B(i) ∈ {SUFFICIENT, INSUFFICIENT, REFERENCE-INDETERMINATE} }
    (i.e. every source item that received an actual reference outcome adjudicable as a claim in
     both arms; OUT_OF_SCOPE items are excluded because they are not claim-sufficiency decisions at
     all, and RU items are excluded because they carry no reference outcome)

    OWNER-CLOSED CHOICE — D-OPEN-ΔS `[PF-04 — OWNER-CLOSED]`: the DENOMINATOR of the per-item
      "P(SUFFICIENT | i, arm)" proportions inside Δ_S is fixed by `OWNER FINAL DECISION —
      D-OPEN-ΔS / PF-04 POLICY CLOSURE`, an Owner decision governing this mutable CEHR draft and
      not a merged repository authority. OPTION A IS SELECTED. The primary Δ_S is the
      MARGINAL EXACT-S / SUFFICIENT-ISSUANCE ESTIMAND.

    OBSERVED PER-ITEM / PER-ARM POINT ESTIMATOR (exact; `CREATOR STATISTICAL DISCRETION: NO`):
      p(i, arm) = NUMBER OF GOVERNING-ELIGIBLE FIRST-PASS RATING RECORDS WITH label == SUFFICIENT
                  / NUMBER OF ALL GOVERNING-ELIGIBLE FIRST-PASS RATING RECORDS FOR THAT ITEM × ARM
      Both are ordinary unweighted counts of records. The PS-2 positive-weight multiplier bootstrap
      (§15.3) is an UNCERTAINTY PROCEDURE ONLY; its multiplier weights never redefine this observed
      point estimator, and no point estimator is inferred from the bootstrap machinery.

    ORDER OF EVALUATION — ELIGIBILITY PRECEDES THE EXACT-S INDICATOR `[D1]`:
      STEP 1 — determine whether the first-pass rating record is GOVERNING-ELIGIBLE under the
        separately governing eligibility / disposition / exclusion / voiding rules already in force
        (the analysis-set exclusions of this §14.1, the repeat-rating rule, the deviation
        dispositions of §20.2 and the consent / withdrawal dispositions of §21.2). No eligibility
        rule is created or modified here.
      STEP 2 — only for records already determined to be governing-eligible, evaluate
        `1{label == SUFFICIENT}`.
      DENOMINATOR MEMBERSHIP IS DETERMINED BY GOVERNING ELIGIBILITY.
      IT IS NOT DETERMINED BY THE RECORD BEING "NON-S".

    EXACT-S INDICATOR — NO LABEL RECODING `[D5]`: for every governing-eligible record the indicator
      is 1 if label == SUFFICIENT and 0 otherwise. INDICATOR = 0 DOES NOT MEAN INSUFFICIENT, A TRUE
      NEGATIVE, AN INCORRECT VERDICT, A SEMANTIC FAILURE OR A SUBSTANTIVE NEGATIVE SUFFICIENCY
      JUDGMENT. CANNOT_ADJUDICATE != INSUFFICIENT · ABSTENTION != TRUE NEGATIVE · OUT_OF_SCOPE IS
      NOT A SUFFICIENCY VERDICT. CA-INTRINSIC, CA-EXTRINSIC and OUT_OF_SCOPE keep their original
      labels and semantics (§3.3, §4A, §5): CA-INTRINSIC is not a "non-S verdict", CA-EXTRINSIC is
      not an INSUFFICIENT outcome, and OUT_OF_SCOPE is not a sufficiency judgment.
      `RAW / CANONICAL LABEL RECODING: NO` — the indicator is an analysis-time reading of the
      preserved label, never a rewrite of it.

    CA-EXTRINSIC GOVERNING-DATA-SET MODEL — UNCHANGED `[CA-E1 — OWNER-CLOSED]`: NO NEW GENERAL
      CA-EXTRINSIC ASCERTAINMENT / EXPOSURE-TIMING ELIGIBILITY REGIME IS CREATED. CA-EXTRINSIC
      records remain subject to the already-existing pre-frozen eligibility, participant-validity,
      disposition, exclusion, voiding and consent / privacy rules wherever those rules already
      determine a consequence, and every existing specific exclusion or voiding consequence is
      unchanged. A DISCLOSED CA-EXTRINSIC RECORD IS NOT AUTOMATICALLY EXCLUDED MERELY BECAUSE ITS
      LABEL / CLASS IS CA-EXTRINSIC. No general "pre-exposure ascertainable CA-EXTRINSIC → exclude ·
      post-exposure ascertainable CA-EXTRINSIC → retain" rule exists or is created here (CA-E2 is
      NOT SELECTED), and no new post-hoc discretion is introduced.

    ZERO GOVERNING-ELIGIBLE DENOMINATOR `[D6]`: if a required item × arm has zero governing-eligible
      first-pass rating records, then `PRIMARY Δ_S POINT ESTIMATOR: NOT ESTIMABLE AS SPECIFIED` ·
      `ITEM DROPPING: NO` · `IMPUTATION: NO` · `POST-OUTCOME REDEFINITION OF A_C: NO` ·
      `SUBSTITUTE DENOMINATOR: NO`. The item is not silently removed merely to restore
      computability. This is the direct consequence of the existing FIXED A_C + UNWEIGHTED ITEM-WISE
      Δ_S AGGREGATION + `STRUCTURAL DROPPING: NO` (§15.3); no replacement estimator is created and
      PS-2 is not redesigned.

    OPTION B — NOT SELECTED AS PRIMARY `[D4]`: the committed-substantive-verdicts-only reading,
      conceptually `P(S | S OR I)`, is NOT SELECTED AS PRIMARY. It is not called statistically
      invalid. OPTION B AS A SUPPLEMENTARY ESTIMAND: NOT AUTHORIZED BY THIS DECISION; NOT PROHIBITED
      AS A FUTURE OWNER-GATED PROPOSAL. OPTION B SUPPLEMENTARY WORK: NOT DEFERRED · NOT TRACKED ·
      NOT A CURRENT OBLIGATION · NOT A PF-04 CLOSURE CONDITION · NOT A FUTURE-GATE REQUIREMENT —
      unless separately authorized by a future Owner decision. No deferred-obligation entry is
      created for it.

    UNAFFECTED AND UNSUPPLEMENTED: Δ_FS_COMMON and Δ_FI_COMMON keep their committed-verdict
      denominators, fixed by CEHR metric M-01 — FALSE-SUFFICIENT RATE (FS_A, FS_B), individual level
      and CEHR metric M-02 — FALSE-INSUFFICIENT RATE (FI_A, FI_B), individual level; Δ_ABST_COMMON
      keeps its all-ratings denominator, fixed by CEHR metric M-05 — ABSTENTION RATE, two-sided and
      sub-classified. The companion reporting stays exactly Δ_ABST_COMMON plus CEHR metric M-05,
      CEHR metric M-06 — OUT_OF_SCOPE HANDLING and the applicable CEHR metric M-11 — CONTEXT EFFECTS
      reporting (§14.2), whose existing definitions and ownership are unchanged; these are the CEHR
      protocol's own metric identifiers, not unrelated repository metrics using the same shorthand.
      No CA-EXTRINSIC worst-case / best-case bounding and no new OUT_OF_SCOPE-in-A_C interpretive
      note is added: each is NOT AUTHORIZED, NOT DEFERRED, NOT TRACKED, NOT A CURRENT CLOSURE
      OBLIGATION and NOT A LATER-GATE REQUIREMENT.

    Δ_S = UNWEIGHTED MEAN OVER i ∈ A_C OF [ p(i, ARM-B) − p(i, ARM-A) ]
        = mean over i ∈ A_C of [ P(SUFFICIENT | i, ARM-B) − P(SUFFICIENT | i, ARM-A) ]
      (the unweighted mean of the within-item ARM-B minus ARM-A difference; A_C is unchanged and no
       third estimand exists)

    Δ_S IS A MARGINAL SUFFICIENT-ISSUANCE-PROPENSITY CONTRAST — THE EFFECT OF SHOWING CONTEXT ON THE
    RATE AT WHICH SUFFICIENT IS ISSUED AMONG GOVERNING-ELIGIBLE FIRST-PASS RATINGS `[D2]`.
    Δ_S IS NOT AN ACCURACY EFFECT, NOT AN ERROR EFFECT, NOT A PURE SEMANTIC S-vs-I CONTRAST, NOT AN
    ESTIMATE OF THE PROPORTION OF CLAIMS THAT ARE ACTUALLY SUFFICIENT, AND NOT A STATEMENT THAT ALL
    NON-SUFFICIENT LABELS ARE SEMANTICALLY EQUIVALENT. IT IS NEVER REPORTED AS AN ERROR EFFECT.
    Δ_FS_COMMON / Δ_FI_COMMON ARE THE ERROR EFFECTS; Δ_S IS NOT SUBSTITUTABLE FOR THEM.
    NO CAUSAL CLAIM IS ATTACHED TO EITHER OPTION.

**Abstention handling.** A CANNOT_ADJUDICATE rating is excluded from every committed-verdict
denominator and reported as its own two-sided rate, split by sub-class CA-EXTRINSIC / CA-INTRINSIC
(§3.3 P-5M); it never counts as a correct negative. **Basis qualifier** (mandatory on every reported
figure): `STUDY-CORPUS, CONDITIONAL ON CORPUS COMPOSITION, POLICY-INTERNAL REFERENCE, ENGLISH ONLY —
NOT A PRODUCT-POPULATION RATE`. **Dependence treatment** (all metrics unless stated): ratings are
clustered within reviewer and within corpus item (crossed); items are nested in families and MP
groups; arms are disjoint reviewer groups; every interval or envelope follows §15.

### §14.2 Metric definitions

Each metric states NUMERATOR · DENOMINATOR · UNIT OF ANALYSIS · EXCLUSIONS · ABSTENTION TREATMENT ·
REPEAT-RATING TREATMENT · DEPENDENCE / CORRELATION TREATMENT · BASIS QUALIFIER (as §14.1 unless
stated) and names its §15 procedure.

**M-01 FALSE-SUFFICIENT RATE (FS_A, FS_B), individual level — PRIMARY SAFETY METRIC.** NUM measured
first-pass SUFFICIENT labels on that arm's PRIMARY FS ITEM SET · DEN measured first-pass committed
verdicts on that set · UNIT rating · EXCL §14.1 · ABST excluded from DEN, reported as M-05 · REPEAT
excluded · DEP crossed reviewer × item, PS-1 · reported per arm (never pooled across arms), per
family within S_P, per reviewer. FS-all (DEN = all first-pass ratings on the set including
abstentions) is reported alongside, never alone. No all-item (S_P ∪ S_S) sensitivity exists `[N7]`.

**M-02 FALSE-INSUFFICIENT RATE (FI_A, FI_B), individual level.** As M-01 on that arm's PRIMARY FI
ITEM SET with NUM = committed INSUFFICIENT labels · PS-1.

**M-03 TRUE-INSUFFICIENT COUNT.** NUM committed INSUFFICIENT on that arm's PRIMARY FS ITEM SET ·
DEN committed verdicts on that set · abstention and OUT_OF_SCOPE NEVER count as true insufficient
`[FINDING ADM-5 / R11]`.

**M-04 CONFIGURATION-LEVEL H2 OUTCOMES (primary).** UNIT study item · computed from the frozen roles
and the rule of §8.2 · one final outcome per study item · reported as counts and proportions of
CANDIDATE POSITIVE · NEGATIVE · FAIL-CLOSED UNRESOLVED · ESCALATED, for every applicable set ·
configuration FS = CANDIDATE POSITIVE proportion on that arm's PRIMARY FS ITEM SET; configuration
FI = NEGATIVE proportion on that arm's PRIMARY FI ITEM SET (arm-specific reference) · between-arm
H2 correctness comparison uses ONLY C_I / C_S `[N2]` · EXCL §14.1 · ABST enters the H2 rule as
defined (never positive) · REPEAT excluded · uncertainty: PS-5 delete-one-reviewer envelope only.
H2 all-pairs: SECONDARY SENSITIVITY ONLY, labelled as such `[FINDING ADM-1 / R8]`.

**M-05 ABSTENTION RATE, two-sided and sub-classified `[N3]`.** NUM CANNOT_ADJUDICATE labels · DEN
all first-pass ratings · UNIT rating · reported separately for CA-EXTRINSIC and CA-INTRINSIC, on
each arm's PRIMARY FS ITEM SET, PRIMARY FI ITEM SET, reference-indeterminate items and all 57 items;
per arm; per `RC-CA-*` code · `RC-CA-04` is reported split by `presentation_status`:
`DEFECT` = surface-integrity count, `OK` = disclosed process failure (including tool-restriction
breach); both are reported separately from CA-INTRINSIC abstention `[PF-03]` · PS-1.

**M-06 OUT_OF_SCOPE HANDLING.** NUM OUT_OF_SCOPE labels on CL-56 / CL-57 (correct handling) and on
all other items (over-use) · DEN first-pass ratings on the respective sets · UNIT rating · per arm ·
PS-1 where non-degenerate.

**M-07 INTER-REVIEWER AGREEMENT.** Krippendorff's alpha (nominal) over the four measured labels,
per arm; pairwise raw agreement alongside · UNIT study item · first-pass ratings only · abstention
and OUT_OF_SCOPE are labels for this purpose (agreement on abstaining is reported separately from
agreement on committed verdicts) · PS-4.

**M-08 INTRA-REVIEWER STABILITY.** NUM repeat pairs with identical label · DEN repeat pairs not
flagged CONTAMINATED · UNIT repeat pair · per arm, with the contamination rate · the ONLY metric in
which repeats enter · PS-6.

**M-09 PARAPHRASE CONSISTENCY (construct axis).** For each MP group and arm, the difference between
the first-pass SUFFICIENT proportions of the anchor and its `PP` sibling · UNIT MP group × arm ·
descriptive (6 groups) · PS-7 · not an error rate.

**M-10 MINIMAL-PAIR DISCRIMINATION (construct axis).** For each MP group and arm, the difference
between the `MC` sibling's and the anchor's first-pass SUFFICIENT proportion in the pre-registered
direction (§7.3), together with the reference-level discrimination indicator (the two effective
references differ in the pre-registered direction: yes / no) · UNIT MP group × arm · PS-7.

**M-11 CONTEXT EFFECTS `[N2 / RZ-2 / PF-04]`.** Exactly the estimands of §6.1, never conflated and
never supplemented. `Δ_S` uses the OWNER-CLOSED Option-A denominator of §14.1 — all governing-eligible
first-pass rating records for that item × arm — fixed by `OWNER FINAL DECISION — D-OPEN-ΔS / PF-04
POLICY CLOSURE`: (a) `Δ_S` — the MARGINAL EXACT-S / SUFFICIENT-ISSUANCE ESTIMAND over A_C (§14.1),
read as a MARGINAL SUFFICIENT-ISSUANCE-PROPENSITY CONTRAST and never as an error effect, with its
item-wise δ_i distribution; (b) `Δ_FS_COMMON` over C_I and (c) `Δ_FI_COMMON` over C_S — the error effects; and the
companion (d) `Δ_ABST_COMMON` — the ARM-B minus ARM-A abstention rate over A_C, which is not an
error effect. No generic Δ_FS or Δ_FI and no Δ over all 57 items is computed. Reported alongside:
the `RC-S-02` use rate in ARM-B and the CA-INTRINSIC rate by arm · UNIT rating, contrasts formed
within item · PS-2.

**M-12 REASON-CODE PERFORMANCE.** Coverage (ratings with ≥ 1 code / all ratings; 1.0 by
construction — deviations are capture defects); reason agreement (among reviewers agreeing on the
label for a study item, proportion sharing ≥ 1 code); code-by-family profile over all 57 items;
frequency of rationales indicating an unclear instruction · descriptive · not an error rate.

**M-13 LATENCY / THROUGHPUT.** Per item, per reviewer, per arm, and per primary H2 configuration
(ROLE-1 + ROLE-2 elapsed, plus ROLE-3 where escalated) · median and interquartile range · no SLA is
derived (NBO-5 retained).

**M-14 REFERENCE OUTCOMES AND PROCESS DISPOSITIONS.** Counts of effective reference by label per
arm; REFERENCE-INDETERMINATE split by construction (FAM-03) versus concurred-on-ambiguity; reference
first-pass agreement (RA-x1 vs RA-x2); escalation count to RA-x3; reference CANNOT_ADJUDICATE
(extrinsic) count with reasons; and the RU count per arm by sub-code (THIRD-ADJUDICATOR-ABSTENTION ·
NO-CONCURRENCE · INSUFFICIENT-PANEL), reported as a study-integrity figure and never as a property
of the items `[N3]`.

**M-15 STUDY-CORPUS G-4-A CONDITION PROPORTION — design constant.** 20 / 57 corpus items carry the
sealed G-4-A flag; 15 / 45 within S_P; 2 (CL-14, CL-39) form the load-bearing
preference-with-causal-token family, of which 1 (CL-14) is in S_P. A corpus-composition and
weighting parameter, NOT `G-4-A PRODUCT-POPULATION EXPOSURE RATE` (§17) `[FINDING L6 / R7]`.

**M-16 CONDITIONAL G-4-A-SHAPE FALSE-SUFFICIENT and CONDITIONAL GENUINE-EVIDENCE-WITHHELD.** M-01
restricted to that arm's PRIMARY G-4-A CONDITIONAL ERROR ITEM SET, and M-02 restricted to that
arm's PRIMARY GENUINE-EVIDENCE-WITHHELD ANALOGUE SET (§14.1) · each carries `CONDITIONAL ON CORPUS
CONDITION — NOT A PRODUCT-POPULATION RATE` `[FINDING ADM-3 / R7]` · PS-1 · between-arm comparison
only on the C_I / C_S intersections of those sets. The MC siblings that carry the G-4-A surface with
a real mechanism (CL-40, CL-44, CL-46, CL-48) are analysed on the construct axis (M-10), not here.
The disagreement set (every study item with a non-unanimous first-pass label) is listed individually
with family, arm, effective reference, label split, reason codes and rationales; no disagreement is
resolved by majority for any error-rate purpose.

**M-17 VARIANCE COMPONENTS.** Reviewer, corpus item and residual variance components for the
SUFFICIENT indicator (and, secondarily, for abstention), with the implied ICCs · PS-3 · pilot
outputs that inform later main-study planning `[FINDING L4 / R5, ADM-8 / R14]`.

**M-18 INSTRUCTION-CLARITY SIGNAL.** Count and content of rationales or end-of-session notes that
say an instruction was unclear, plus CA-INTRINSIC (`RC-CA-02`) frequency and its concentration by
family · feeds the policy-undecidability STOP rule (§20.3).

**M-19 REFERENCE TRANSITION MATRIX — MANDATORY `[N2 / N3]`.** A complete 4 × 4 cross-tabulation of
Ref_A(i) × Ref_B(i) over the corpus items that received an ACTUAL REFERENCE OUTCOME IN BOTH ARMS
(reported over all such items and separately over S_P), with rows and columns

    SUFFICIENT · INSUFFICIENT · REFERENCE-INDETERMINATE · OUT_OF_SCOPE

and nothing else: the matrix contains only actual reference outcomes. Every one of the transitions

    A:I → B:I · A:I → B:S · A:S → B:I · A:S → B:S

and every transition involving REFERENCE-INDETERMINATE or OUT_OF_SCOPE is reported explicitly with
its item list. No transition may silently disappear, be pooled away or be omitted for smallness.
Items carrying RU in either arm are NOT in the matrix and are NOT counted as any transition; they
appear only in the PROCESS-DISPOSITION REGISTER published beside it, which lists every RU item with
its arm, sub-code and abstention reasons.

Exact reconciliation, reported verbatim `[RZ-3]`:

    FULL CORPUS
      57 = ( SUM OF ALL 4 × 4 MATRIX CELLS )
         + ( COUNT OF UNIQUE ITEM IDs WHERE RU_A OR RU_B )
    SOURCE SET S_P
      45 = ( SUM OF ALL S_P 4 × 4 MATRIX CELLS )
         + ( COUNT OF UNIQUE S_P ITEM IDs WHERE RU_A OR RU_B )
    REPORTED SEPARATELY, AND NEVER SUBSTITUTED INTO THE IDENTITIES ABOVE:
      RU ARM-ENTRY COUNT = the number of (arm, item) entries carrying RU, which counts an item
        twice when it is RU in both arms and therefore MAY EXCEED the unique RU item count
    PROHIBITED CLAIM: "matrix cells + RU arm entries = 57" — it is false whenever any item is RU in
      both arms

Matrix and register are computed at the reference freeze (§8.3 step 6), before any measured outcome
exists, from the reference-freeze artifact (§8.3A), and the matrix is what determines C_I, C_S and
A_C.

Retained Amendment §17 Limb-2 quantities: `INTER-REVIEWER AGREEMENT` M-07 · `INTRA-REVIEWER
STABILITY` M-08 · `FALSE-SUFFICIENT RATE` M-01 / M-04 · `FALSE-INSUFFICIENT RATE` M-02 / M-04 ·
`PREFERENCE HANDLING` M-01 on FAM-04 ∩ S_P · `NONSENSE / ADVERSARIAL CLAIM HANDLING` M-01 on
FAM-05 / FAM-07 ∩ S_P · `DECISION STABILITY` M-08 + M-09 · `REVIEWER THROUGHPUT / LATENCY` M-13 ·
`POLICY-INSTRUCTION CLARITY` M-18 · `G-4-A EXPOSURE RATE` NOT MEASURED (§17) · `FALSE CAUSAL
CREDIT RATE` and `GENUINE CAUSAL EVIDENCE WITHHELD RATE` measured ONLY as the corpus-conditional
analogues in M-16 · `MECHANISM_COMPLETENESS FALSE-CLOSURE RATE` design only, not executed (§19).

---

## §15. Frozen primary statistical procedures `[PROPOSAL; M8 + N7 repairs]`

    LOAD-BEARING ANALYSIS DEFERRED OUTSIDE SUBJECT: 0
    PRIMARY / FALLBACK ORDERING: PRE-FROZEN — NO OUTCOME-DEPENDENT ESTIMATOR CHOICE
    PRE-FROZEN BOOTSTRAP SEED: 20260906
    BOOTSTRAP REPLICATES B: 10,000
    FINITE-SAMPLE EXACT COVERAGE: NEVER CLAIMED · "EXACT CONFIDENCE INTERVAL": PROHIBITED
    CLOPPER–PEARSON: ABSENT FROM THE GOVERNING METHOD
    HENDERSON III: ABSENT FROM THE GOVERNING FALLBACK CHAIN
    LINEAR-PROBABILITY REML: NOT A GOVERNING FALLBACK
    A later analysis plan may carry only mechanically derivative details (software, table layouts,
      rounding) that change no estimand, estimator, fallback or diagnostic below.

### §15.1 Design structure the procedures must fit

Ratings are binary or categorical outcomes on a crossed, unbalanced two-way layout: each of 18
reviewers rates 19 of 57 corpus items; each corpus item is rated by 3 reviewers in each of two
disjoint reviewer groups; arm is a between-reviewer factor; items are nested in MP groups and
families. Two crossed random sources of variation — reviewer and item — are present in every rate.
Small counts, including zero events, are expected at pilot scale.

### §15.2 PS-1 — operational rates (M-01, M-02, M-03, M-05, M-06, M-16)

    ESTIMAND: the population-averaged probability that a first-pass committed rating on the
      specified item set, in the specified arm, carries the specified label
    UNIT OF ANALYSIS: rating
    POINT ESTIMATOR: EMPIRICAL RATIO (numerator count / denominator count over the set)
    PRIMARY UNCERTAINTY: POSITIVE-WEIGHT TWO-WAY MULTIPLIER (PIGEONHOLE) BOOTSTRAP
      for every replicate b:
        reviewer weight  W_r^(b) ~ Exp(1), independently by reviewer
        item weight      W_i^(b) ~ Exp(1), independently by source item
        observation weight W_ri^(b) = W_r^(b) × W_i^(b)
        the weighted ratio is Σ W_ri·1{label} / Σ W_ri over the set
      STRUCTURAL REVIEWER / ITEM DROPPING: NO — every observation keeps a strictly positive weight
      B = 10,000 · SEED = 20260906
      INTERVAL: the 2.5th and 97.5th percentiles of the 10,000 weighted estimates
      CLASSIFICATION: 95% PILOT UNCERTAINTY INTERVAL (finite-sample exact coverage NOT claimed)
    ARM-SPECIFIC APPLICATION: reviewer multipliers are drawn only over the reviewers of the arm
      being estimated; source-item identities retain their frozen item dimension. Every PS-1 set is
      a subset of S_P, so each item is its own independent item-dimension unit and no sibling group
      appears in any PS-1 set `[N7]`
    DEPENDENCE ADDRESSED: crossed reviewer × item clustering, without dropping data
    FAILURE / FALLBACK TRIGGER: denominator = 0; OR fewer than 5 distinct eligible items;
      OR fewer than 5 contributing reviewers; OR a degenerate bootstrap estimand distribution
      (all replicates identical)
    PRE-FROZEN FALLBACK: report the RAW NUMERATOR, the RAW DENOMINATOR and the EMPIRICAL POINT
      RATE, plus the LEAVE-ONE-REVIEWER INFLUENCE RANGE (recompute the rate with each contributing
      reviewer's ratings removed in turn; report min, max and the maximum absolute shift from the
      full estimate) and, where more than one item contributes, the LEAVE-ONE-ITEM INFLUENCE RANGE
      computed the same way
    WHAT THE FALLBACK REPORTS: the observed rate and its sensitivity to any single reviewer or item.
      NO NOMINAL INTERVAL IS EMITTED. ZERO EVENTS != ZERO RISK — a zero numerator is reported as an
      observed zero with its denominator and its influence ranges, never as a bound on risk
    RATIONALE: the multiplier bootstrap is the standard positive-weight resampling scheme for data
      with crossed random effects; it respects both clusterings, needs no parametric model, and —
      unlike case-resampling with intersection dropping — never discards observations or distorts
      the effective design

### §15.3 PS-2 — context comparison (M-11: Δ_S, Δ_FS_COMMON, Δ_FI_COMMON)

    ESTIMANDS: Δ_S over A_C; Δ_FS_COMMON over C_I; Δ_FI_COMMON over C_S; and the companion
      Δ_ABST_COMMON over A_C (all defined in §6.1 / §14.1) — no other context estimand `[RZ-2]`
    UNIT OF ANALYSIS: rating, with the contrast formed within item
    POINT ESTIMATORS: for Δ_S, the unweighted mean over i ∈ A_C of the ARM-B minus ARM-A SUFFICIENT
      proportions, each proportion being the ordinary count of governing-eligible first-pass records
      with label == SUFFICIENT over the ordinary count of all governing-eligible first-pass records
      for that item × arm — the OWNER-CLOSED Option-A denominator of §14.1, fixed by `OWNER FINAL
      DECISION — D-OPEN-ΔS / PF-04 POLICY CLOSURE` `[PF-04 — OWNER-CLOSED]`. The multiplier weights
      below are used ONLY inside the uncertainty replicates and NEVER redefine this observed point
      estimator; where a required item × arm has zero governing-eligible first-pass records the
      primary Δ_S point estimator is NOT ESTIMABLE AS SPECIFIED and the item is not dropped, imputed
      or given a substitute denominator (§14.1 `[D6]`); for Δ_FS_COMMON / Δ_FI_COMMON, the difference of the PS-1 empirical
      ratios computed on the same common stratum in each arm (committed-verdict denominators per
      M-01 / M-02); for Δ_ABST_COMMON, the difference of the M-05 abstention rates over A_C
      (all-ratings denominator)
    PRIMARY UNCERTAINTY: the same positive-weight multiplier bootstrap as PS-1, with
      ITEM MULTIPLIER: THE SAME VALUE FOR ITEM i IN ARM-A AND ARM-B WITHIN A REPLICATE
      REVIEWER MULTIPLIERS: INDEPENDENT ACROSS THE DISJOINT A / B REVIEWER GROUPS
      B = 10,000 · SEED = 20260906 · percentile 95% PILOT UNCERTAINTY INTERVAL
      STRUCTURAL DROPPING: NO
    Δ_S BOOTSTRAP REPLICATE STATISTIC — SOLE GOVERNING FORM `[NB-4 — OWNER-CLOSED]`: fixed by
      `OWNER DECISION — NB-4 / PS-2 Δ_S BOOTSTRAP REPLICATE — BOUNDED METHODOLOGICAL CLOSURE`
      (FORMULATION 2 SELECTED; FORMULATION 1 NOT SELECTED; FORMULATION 3 NOT SELECTED). For
      replicate b, for each governing item i ∈ A_C and each arm a ∈ {ARM-A, ARM-B}:
        Y_ira = 1{label == SUFFICIENT}, defined on GOVERNING-ELIGIBLE FIRST-PASS rating records only
        REVIEWER-WEIGHTED PER-ITEM / PER-ARM PROPORTION
          p_i,a^(b) = [ Σ_r W_r^(b) Y_ira ] / [ Σ_r W_r^(b) ]
          where both sums contain only the governing-eligible first-pass rating records for item i ×
          arm a, and the reviewer multiplier W_r^(b) is attached to reviewer identity: within
          replicate b the same W_r^(b) applies to that reviewer's eligible ratings wherever that
          reviewer contributes
        THE COMMON ITEM MULTIPLIER CANCELS INSIDE THE PER-ITEM RATIO — writing the already-settled
          observation weight of §15.2 as W_i^(b) × W_r^(b),
          [ Σ_r W_i^(b) W_r^(b) Y_ira ] / [ Σ_r W_i^(b) W_r^(b) ] = p_i,a^(b)
        PAIRED ITEM CONTRAST
          δ_i^(b) = p_i,B^(b) − p_i,A^(b)
        THE ONLY GOVERNING Δ_S BOOTSTRAP REPLICATE
          Δ_S^(b) = [ Σ_{i∈A_C} W_i^(b) δ_i^(b) ] / [ Σ_{i∈A_C} W_i^(b) ]
      `ANALYST CHOICE AMONG FORMULATIONS: NO` · `POST-OUTCOME FORMULA SELECTION: PROHIBITED` ·
      `CREATOR STATISTICAL DISCRETION: 0` · `ANALYST STATISTICAL DISCRETION: 0`. No alternative,
      example, sensitivity or analyst-selectable Δ_S replicate formulation exists or is retained.
      This replicate statistic is an UNCERTAINTY PROCEDURE ONLY: the observed Δ_S point estimator
      (§14.1) remains the UNWEIGHTED mean over i ∈ A_C of the ordinary-count proportions and is
      never redefined by these weights. For a governing item × arm holding at least one
      governing-eligible first-pass rating record, the strictly positive Exp(1) reviewer multipliers
      make the replicate per-item denominator positive; the §14.1 `[D6]` zero-governing-eligible
      rule is unchanged and no new zero-weight fallback is created.
    DEPENDENCE ADDRESSED: shared item difficulty across arms (shared multiplier) and independent
      reviewer variation within each group
    FAILURE / FALLBACK TRIGGER: insufficient common-stratum support — |C_I| < 5, |C_S| < 5 or
      |A_C| < 5 for the respective estimand (Δ_ABST_COMMON follows the A_C trigger); or fewer than 5 contributing reviewers in either arm;
      or a degenerate replicate distribution
    PRE-FROZEN FALLBACK (NO NOMINAL INTERVAL): report the raw stratum size; the item-wise direction
      counts (items with a positive, zero and negative item-level effect); the median item-level
      effect; the leave-one-reviewer influence range; and the leave-one-item influence range
    RATIONALE: every item appears in both arms, so the within-item contrast removes item difficulty
      exactly; reviewers differ across arms by randomization, which the independent reviewer
      multipliers reflect; the common strata keep the comparison on comparable items `[N2]`

### §15.4 PS-3 — variance components and ICC (M-17)

    ESTIMANDS: σ²_reviewer, σ²_item and the implied ICC_reviewer, ICC_item for the SUFFICIENT
      indicator, on the latent logistic scale
    UNIT OF ANALYSIS: rating
    PRIMARY MODEL: CROSSED LOGISTIC GLMM, arm coded A = 0, B = 1
        logit P(Y_ri = 1) = β0 + β_arm × ARM + u_reviewer(r) + v_item(i)
        u_reviewer ~ Normal(0, σ²_reviewer) · v_item ~ Normal(0, σ²_item)
      ESTIMATION: maximum likelihood / Laplace approximation
      ICC_item = σ²_item / (σ²_item + σ²_reviewer + π²/3); ICC_reviewer analogously
      UNCERTAINTY: profile-likelihood or Wald intervals on the components, reported with the fit
        diagnostics
    PRIMARY FAILURE CONDITIONS: non-convergence; non-positive-definite Hessian; complete or
      quasi-complete separation; any other numerical failure preventing reliable variance
      estimation. A variance estimate near the zero boundary is REPORTED TRUTHFULLY and is NOT by
      itself a methodological failure
    GOVERNING FALLBACK: BAYESIAN CROSSED LOGISTIC MODEL — same linear predictor, same arm coding,
      same random-intercept structure; AUTOSCALING: NO; exact priors:
        β0            ~ Student-t(df = 3, location = 0, scale = 2.5)
        β_arm         ~ Normal(mean = 0, sd = 1.5)
        σ_reviewer    ~ half-Student-t(df = 3, location = 0, scale = 1)
        σ_item        ~ half-Student-t(df = 3, location = 0, scale = 1)
      MINIMUM CHAINS: 4
      DIAGNOSTICS (applied at minimum to β0, β_arm, σ_reviewer, σ_item, ICC_reviewer, ICC_item and
        every posterior quantity used for later sizing):
        R-hat <= 1.01 · Bulk ESS >= 400 total · Tail ESS >= 400 total ·
        0 divergent transitions after final tuning
    IF THE BAYESIAN DIAGNOSTICS FAIL: PS-3: NOT ESTIMABLE. THERE IS NO THIRD GOVERNING FALLBACK.
    RATIONALE: the crossed-intercept GLMM is the standard model for crossed reviewer × item binary
      data; the Bayesian model with weakly informative priors is the established remedy for
      boundary and separation failures at pilot scale, and its diagnostics are stated in advance so
      no method is selected after seeing the data
    USE: PS-3 outputs feed later simulation-based main-study planning only.
      FINAL MAIN-STUDY N: NOT SET.

### §15.5 PS-4 — agreement (M-07)

    ESTIMAND: chance-corrected agreement among reviewers over the four measured labels, per arm
    UNIT: study item
    ESTIMATOR: Krippendorff's alpha, nominal metric, on the incomplete reviewer × item matrix
      (each item has 3 of 9 raters in its arm), plus mean pairwise raw agreement
    UNCERTAINTY: the PS-1 positive-weight multiplier bootstrap (no dropping), percentile interval,
      B = 10,000, seed 20260906; CLASSIFICATION: 95% PILOT UNCERTAINTY INTERVAL
    FAILURE: no label variation (alpha undefined); fewer than 5 contributing reviewers
    PRE-FROZEN FALLBACK: raw agreement with the leave-one-reviewer influence range; no nominal
      interval
    RATIONALE: alpha is defined for multiple raters, nominal data and incomplete designs

### §15.6 PS-5 — H2 configuration outcomes (M-04)

    THE PRIOR CASE-RESAMPLING METHOD IS PROHIBITED: no reviewer resampling that leaves an item's
      operative roles unfilled, and NO STRUCTURAL ITEM DROPPING, may be used for H2 `[N7]`
    ESTIMAND: the proportion of study items in the specified set whose FINAL H2 OUTCOME under the
      exact frozen primary role assignment (§8.2, Table 11.2-D) is the specified outcome
    UNIT OF ANALYSIS: study item
    POINT ESTIMATE: the empirical final-outcome proportion, reported for every applicable set as
      counts and proportions of CANDIDATE POSITIVE · NEGATIVE · FAIL-CLOSED UNRESOLVED · ESCALATED,
      one final outcome per study item
    REFERENCE BASIS: per-arm operational H2 error rates use that arm's own reference; between-arm
      H2 correctness comparisons use ONLY the common strata C_I / C_S `[N2]`
    UNCERTAINTY: DELETE-ONE-REVIEWER INFLUENCE ENVELOPE — CLASSIFICATION: SENSITIVITY ENVELOPE
      ONLY; NOT A NOMINAL CONFIDENCE INTERVAL
      for each reviewer g in the arm: remove every H2 study item whose operative role set contains
      g (ROLE-1, ROLE-2, and ROLE-3 where that item escalated), recompute the rate on the remaining
      evaluable items, and repeat for all reviewers in that arm
      REPORT: all leave-one-reviewer estimates, the minimum, the maximum, and the maximum absolute
      shift from the full-panel estimate
    NOT ESTIMABLE CONDITIONS: fewer than 5 full-panel eligible items in the set; or any required
      reviewer deletion leaving fewer than 5 evaluable items
      THEN: return RAW COUNTS AND THE FULL-PANEL POINT RATE ONLY
    ALL-PAIRS ANALYSIS: SECONDARY SENSITIVITY ONLY, never the primary configuration estimate
    RATIONALE: the H2 outcome is defined only under the frozen roles, so any resampling that
      destroys a role set changes the estimand rather than its uncertainty; a deletion envelope
      states the dependence on individual reviewers truthfully without inventing coverage

### §15.7 PS-6 — stability (M-08)

    ESTIMAND: the probability that a non-contaminated repeat pair carries identical labels, per arm
    UNIT: repeat pair · ESTIMATOR: proportion
    UNCERTAINTY: positive-weight reviewer multiplier bootstrap (W_r ~ Exp(1), no dropping;
      pairs carry their reviewer's weight), percentile interval, B = 10,000, seed 20260906;
      CLASSIFICATION: 95% PILOT UNCERTAINTY INTERVAL
    FAILURE: fewer than 5 reviewers with any non-contaminated pair in the arm
    PRE-FROZEN FALLBACK: raw counts, empirical proportion and the leave-one-reviewer influence range
    RATIONALE: reviewer is the only cluster for a repeat pair; item resampling would break pairs

### §15.8 PS-7 — construct axis (M-09, M-10)

    ESTIMANDS: per MP group and arm, the differences defined in M-09 / M-10 and the reference-level
      discrimination indicator
    UNIT: MP group × arm · ESTIMATOR: differences of proportions; indicator from the effective
      references
    UNCERTAINTY: none — six groups; reported descriptively and labelled EXPLORATORY
    FAILURE / FALLBACK: not applicable
    RATIONALE: the axis exists to detect policy insensitivity on pre-registered boundaries, which is
      a qualitative finding at pilot scale; no inferential claim is made

### §15.9 Reporting rules

Every reported figure names its procedure identifier, states whether the primary or the pre-frozen
fallback was used and why, and carries the §14.1 basis qualifier. Primary and fallback outputs are
never blended. No estimator, interval method or diagnostic is chosen after seeing the data. No
figure produced by this protocol is described as an exact confidence interval, and no zero-event
result is described as a bound on risk. The naive `VIF_item × VIF_reviewer` product formula is not
part of this protocol in any role: it treats crossed clusterings as nested and is not used, quoted
or relied on for sizing.

`[NB-4 — OWNER-CLOSED]` For Δ_S, the §15.3 Owner-final NB-4 replicate statistic is the sole
authorized bootstrap replicate form. No alternate Δ_S bootstrap statistic, outer item-weighting
rule, pooled arm-level statistic, or analyst-selectable replicate formulation may be substituted
after measured outcomes are visible.

### §15.10 Missing, incomplete and withdrawn data

A reviewer who completes fewer than all 19 first-pass items is reported as INCOMPLETE. COMPLETED
RATINGS ARE INCLUDED IN THE GOVERNING DATA SET ONLY TO THE EXTENT THEY REMAIN PERMITTED UNDER THE
PRE-FROZEN CONSENT / PRIVACY TERMS AND APPLICABLE GOVERNING REQUIREMENTS; where those rules require
removal, §21.2 controls and the removal is applied before any denominator is formed `[RZ-5]`. An
incomplete reviewer's included ratings are excluded from M-08 unless all four repeat pairs are
present in the governing data set. Withdrawals are handled under §21.2 (Owner policy); their data
consequences are fixed there in advance and are never improvised. Missing ratings are never imputed.
ACHIEVED DENOMINATORS ARE COMPUTED FROM THE GOVERNING DATA SET AFTER THE PRE-FROZEN DISPOSITION
RULES HAVE BEEN APPLIED — never from planned counts, and never from ratings the disposition rules
exclude. A study item that ends without its operative H2 roles is reported as
H2-UNEVALUABLE and excluded from M-04 with the count stated.

### §15.11 Pilot outputs and main-study planning

Where estimable: reviewer variance; item variance; ICC / dependence; abstention (two-sided, by
sub-class); reference outcomes, the transition matrix and indeterminacy; the three context effects;
latency / throughput; reason-code performance; instruction-clarity signal; contamination rate; the
disagreement set. Main-study sizing is a later Owner decision (D4-b) informed by simulation from the
PS-3 outputs and the observed abstention and reference-indeterminacy rates; `FINAL MAIN-STUDY N: NOT
DETERMINED NOW`. The pilot emits NO PASS / FAIL and applies NO threshold.

---

## §16. Safety direction, materiality indicators and Owner-owned thresholds (T1)

    FALSE-SUFFICIENT / FALSE-CLOSURE RISK: PRIORITIZED (asymmetric, fail-closed)
    NUMERIC EVIDENCE-ACCEPTANCE THRESHOLDS: NOT OWNER-FROZEN NOW
    CREATOR-CREATED AUTOMATIC MATERIALITY THRESHOLD: PROHIBITED
    NO NUMERICAL PASS THRESHOLD IS INVENTED BY THIS PROTOCOL (Hybrid §17 / Amendment §17)

**MATERIALITY INDICATOR** — a detection rule computed by the analyst that mandatorily triggers
escalation, a written finding and Owner adjudication. It never by itself determines materiality.
**BINDING MATERIALITY THRESHOLD** — a decision rule converting a measurement into a
material / not-material verdict. Only the Owner may set one; none exists in this protocol
`[FINDING L3 / R4]`.

Indicators frozen here (escalation only):

- IND-1 any measured SUFFICIENT on an item that is reference-INSUFFICIENT in the arm being
  examined, in FAM-04 (preference) or on CL-14 (the G-4-A load-bearing shape);
- IND-2 any measured SUFFICIENT on a primary reference-INSUFFICIENT item in FAM-05 / FAM-07
  (nonsense / adversarial);
- IND-3 any study item on which two or more of its three reviewers give the same wrong committed
  verdict against that arm's determinate reference;
- IND-4 any primary-H2 CANDIDATE POSITIVE on a primary reference-INSUFFICIENT study item;
- IND-5 `Δ_FS_COMMON` > 0 (ARM-B FS above ARM-A FS on the common stratum C_I — context-induced
  completion) `[N2]`; reported together with Δ_S, which is never read as an error effect;
- IND-6 a meaning-preserving pair whose effective references differ, or a meaning-changing pair
  whose effective references coincide (§18);
- IND-7 `RC-CA-02` or instruction-unclear rationales concentrated on any family (§20.3);
- IND-8 any FAM-13 anchor (CL-54, CL-55) receiving a measured INSUFFICIENT with a rationale that
  cites technical validity (P-4 breach signal);
- IND-9 any `RC-CA-04` recorded on any item — reported and escalated as two distinct findings:
  `presentation_status = DEFECT` is a surface-integrity finding, `presentation_status = OK` is a
  disclosed process-failure finding (for example a tool-restriction breach) `[PF-03]`;
- IND-10 any reference transition A:S → B:I or A:I → B:S in the M-19 matrix (the two arms'
  independent references disagree in direction on the same item) `[N2]`;
- IND-11 CA-INTRINSIC (`RC-CA-02`) concentrated on any family, or |C_I| or |C_S| materially smaller
  than |S_P| ∩ the corresponding determinate sets (comparability erosion).

Safety-critical metric list proposed for Owner confirmation under D4-a (§22): M-01 (per arm), M-04
(FS side, per arm), M-16 (conditional G-4-A-shape FS), Δ_FS_COMMON, IND-1, IND-4, IND-5, IND-10, and
the deferred false-closure projection (§19). Every binding determination about any of them reduces to an Owner-set tolerance taken after
the evidence exists.

---

## §17. Product-rate / exposure integrity and the deferred population-exposure sub-limb

### §17.1 Naming discipline

The designer-controlled composition of this corpus is named `STUDY-CORPUS G-4-A CONDITION
PROPORTION` (M-15). It is never called, reported as, or substituted for
`G-4-A PRODUCT-POPULATION EXPOSURE RATE`.

    G-4-A PRODUCT-POPULATION EXPOSURE RATE: NOT MEASURED BY THIS CONTROLLED CHALLENGE CORPUS
    PRODUCT-POPULATION EXPOSURE SUB-LIMB: DEFERRED — NOT DISCHARGED
    RETURN: AFTER PILOT / DESIGN LEARNING AND BEFORE CLAIM-ELIGIBILITY IMPLEMENTATION
      AUTHORIZATION, unless later Owner authority explicitly changes its governing meaning

A true product-population exposure estimate requires: a defined target population of claims to
which `MECHANISM_COMPLETENESS` applies in the served product; a defensible representative /
probability / exhaustive sampling frame over it; and condition labelling independent of the
sampling. None exists here. `REAL USER DATA REQUIRED: NOT PROVEN` — a separately authorized
representative elicitation frame could qualify; `REAL USER DATA AUTHORIZED: NO`. The same basis
integrity applies to `FALSE CAUSAL CREDIT` and `GENUINE CAUSAL EVIDENCE WITHHELD` (M-16):
challenge-set conditional rates are never reported as marginal product rates.

### §17.2 Sealed G-4-A shape annotation

G4A = Y in §7.2 marks items whose text carries an English causal / conditional connective and
whose sealed construction label is not SUFFICIENT — causal surface without mechanism. The
annotation is descriptive, sealed, and used only for M-15 / M-16 conditional reporting. It is not a
scoring rule, not an authoring rule, not a classifier, and not a Level-1 / Level-2 / Level-3
mechanism proposal.

### §17.3 Register discipline

    NEW DOR ROW: NO · NEW DOR OWNER: NO · DOR MUTATION: NO

The deferred sub-limb is routed to the existing G-4 / Claim-Eligibility obligation in the Deferred
Obligations Register — the register row `EN↔AR SUBSTANTIVE-ASSESSMENT OUTCOME DIVERGENCE ON
EQUIVALENT USER ANSWERS`, whose disposition cell carries the G-4 Mechanism A / Mechanism B
adjudication and the Claim-Eligibility containment lane (parallel, non-superseding) `[EXEC]` — and
to Hybrid §22 / the PRE-FCORA reconciliation (`SILENT DISAPPEARANCE OF G-4-A: PROHIBITED`). A
separate Owner scope is created only if later evidence proves it necessary. The prior review's
suggestion of a new DOR row (R7) is satisfied in substance by routing, not by a register act;
recording it there is a later, separately authorized governance act, not part of this draft.

---

## §18. Policy-construct-validity axis `[PROPOSAL; FINDING ADM-2 / R9]`

    REFERENCE TRUTH UNDER CLAIM-ELIGIBILITY-SUFFICIENCY-EN-v1 = POLICY-INTERNAL REFERENCE
    It measures reviewer conformance / reliability under that policy.
    It does NOT alone prove the policy is protectively correct.

A separate construct-validity axis is frozen, using:

1. **Pre-registered meaning-preserving minimal pairs** — the six `PP` siblings (§7.3). Validity
   signal: the effective reference labels anchor and `PP` sibling identically (reference-level
   consistency, M-14 companion) and measured proportions coincide (M-09).
2. **Pre-registered materially meaning-changing minimal pairs** — the six `MC` siblings. Validity
   signal: the effective reference labels anchor and `MC` sibling differently in the pre-registered
   direction (reference-level discrimination) and measured proportions separate (M-10). A policy
   under which the reference labels both halves of a pair identically is shown insensitive on that
   boundary.
3. **Semantic validity anchors — OWNER-ACCEPTED under D-NEW-C `[OWNER-PREMISE]`.** The Owner has
   issued `OWNER DECISION — D-NEW-C CEHR SEMANTIC VALIDITY ANCHORS`, disposition `ACCEPT AS
   PROPOSED WITH GOVERNING BOUNDARY CLARIFICATIONS`. The six anchors below are therefore
   `OWNER-ACCEPTED` and are the `MINIMUM MANDATORY SEMANTIC VALIDITY ANCHORS` for this pre-pilot
   protocol. They are not Creator proposals and are no longer an open Owner-owned choice.

   | # | Anchor | Governing interpretation (Owner) | Exercised by |
   |---|---|---|---|
   | 1 | `PREFERENCE != MECHANISM` | A preference, convenience choice, avoidability statement or desired outcome does not by itself establish a mechanism | MP-02, MP-03, FAM-04 |
   | 2 | `CATEGORY / CONFIRMATION != CREDIT` | Selecting a category, answering yes/no, confirming intent or completing a form does not by itself establish mechanism sufficiency or create causal credit | FAM-02, FAM-12 |
   | 3 | `CLAIM SUFFICIENCY != TECHNICAL / EMPIRICAL VALIDATION` | A claim may be sufficiently articulated for Claim-Eligibility purposes without being technically correct, physically feasible, empirically validated, manufacturable, commercially viable or otherwise real-world verified; conversely `CLAIM-ELIGIBILITY MUST NOT BE REPRESENTED AS TECHNICAL VALIDATION` | FAM-13 — CL-54, CL-55 must not be marked INSUFFICIENT for being wrong |
   | 4 | `SURFACE CAUSAL FORM != MECHANISM` | Causal-looking wording, conditional syntax, causal connectors or other surface linguistic form does not by itself establish a substantive mechanism; this preserves `G-4-A TECHNICAL DEFECT: CURRENT — NOT FIXED` | FAM-05, FAM-07, MP-06 |
   | 5 | `BREVITY != INSUFFICIENCY` | Claim length alone is not evidence of insufficiency: a short claim may be sufficient if the required substantive mechanical elements are present, and a long claim may remain insufficient if they are absent | FAM-08, MP-03 |
   | 6 | `CONTEXT MAY RESOLVE, MUST NOT INVENT` | The Owner-selected P3 rule: context may clarify scope, resolve a bounded referent and clarify the governed question being answered; it must not invent a missing condition, invent missing resulting system behaviour, invent a missing dependency, supply substantive mechanism content absent from the user's claim, or convert an otherwise insufficient claim into sufficient through reviewer completion | FAM-03, M-11, IND-5 |

   **Owner-stated boundaries, binding.** The anchors are semantic-validity constraints. They do NOT
   independently determine SUFFICIENT or INSUFFICIENT: the governing frozen Claim-Sufficiency Policy
   (§3, §4A) remains controlling. They are not automatic scoring rules, not numeric thresholds, not
   new event values, not new product-capability / assessment / progression owners, not
   technical-validation criteria and not a replacement policy. They are also NOT an exhaustive
   permanent semantic universe: an additional anchor requires a materially distinct demonstrated
   validity risk, non-duplication, and applicable Owner authority — no Creator or reviewer may
   silently expand the set into new policy.

       D-NEW-C: OWNER-FINAL ISSUED · SIX ANCHORS OWNER-ACCEPTED · MINIMUM MANDATORY ·
         NON-EXHAUSTIVE · NON-SCORING · SUBORDINATE TO THE CLAIM-SUFFICIENCY POLICY
       D-NEW-C OWNER-OWNED OPEN CHOICE: CLOSED
       SEVENTH ANCHOR CREATED BY THIS DRAFT: NO
4. **Sealed author-design-intent metadata for diagnostics only** — §7.2 sealed labels. Unsealed
   for analysis only after the reference outcomes are frozen and hashed (§8.3 step 6).
   `AUTHOR INTENT: NOT GROUND TRUTH` · `AUTHOR-INTENT ↔ REFERENCE DIVERGENCE: DIAGNOSTIC ONLY` — a
   divergence is a finding about the policy or the item, never a correction to the reference.

If the frozen policy cannot distinguish materially different pre-frozen semantic anchors necessary
for Owner product truth (IND-6 fires on any `MC` pair, or the reference labels a FAM-13 anchor
INSUFFICIENT on validity grounds): `POLICY ADEQUACY CONCERN: YES`, and future execution stops for
Owner decision (§20.3).

---

## §19. False-closure projection — design only `[FINDING ADM-7 / R13]`

    FALSE-CLOSURE PROJECTION =
      HUMAN SOURCE × POLICY / CONTEXT × CURRENT ENGINE / RECONSTRUCTION VERSION
      × DOMAIN / SESSION CONTEXT
    CLASSIFICATION: COMPOSITE PRODUCT-CONSEQUENCE MEASURE — NOT PURE REVIEWER ACCURACY

A projection would ask: had each primary-H2 CANDIDATE POSITIVE been a valid `ClaimEligibilityEvent`,
what would the pinned engine's Amendment §10 quality recomputation
(`assess_response(immutable_claim_content, durable_confirmed_domain)`) have done to
`MECHANISM_COMPLETENESS`? Its output is a human × engine composite: a low projected closure rate may
reflect the still-defective classifier withholding quality, not reviewer accuracy, and a high one
may reflect the classifier's own G-4-A false positive. Future inputs required before any
projection can be specified: domain assignment for every corpus item (none is assigned here; the
corpus is domain-free by design); the required claim / session context; the exact engine /
reconstruction identity (an exact commit and reconstruction version, pinned at projection time);
the exact eligibility-policy version; the human source / configuration verdict input (the primary
H2 outcome); Mechanism-B inheritance disclosure (the structured-form trigger asymmetry is inherited
unchanged); existing G-4-A defect inheritance disclosure (the `"if "` raw-substring false positive
is inherited unchanged).

    HARNESS: NO · EXECUTION: NO · NEW EXECUTABLE ANALYSIS ARTIFACT: NO
    FALSE-CLOSURE PROJECTION EXECUTED: NO
    A projection harness is a SEPARATELY AUTHORIZED ANALYSIS ARTIFACT — never a free consequence,
      never "requiring no code change"
    If reproducibility ever requires it: STOP — EXECUTABLE PROTOCOL ARTIFACT REQUIRED

---

## §20. STOP conditions, deviation, version-change and undecidability rules

### §20.1 Stopping rule and prohibited changes

Measured collection stops when every enrolled reviewer has completed the session, or 14 calendar
days after the first measured invitation, whichever comes first. No interim analysis; no enrolment
decision after looking at any rating; the sample is never extended to change a result. After
freeze it is prohibited to: change any rule in §3 – §5; add, remove, reword, re-pair or re-label any
item; change the groups, the assignment, the roles, the repeat structure or the instructions;
change the reference process; add, drop or redefine a metric or a §15 procedure; introduce a numeric
threshold; or select a repair to improve any result. Any such change voids this protocol version.

### §20.2 Mandatory STOP during execution

STOP the affected part and return to the Lead if: a measured outcome exists before the reference
outcomes are frozen and hashed; a reference human learns any label, grouping, intent, measured
rating or prior verdict before finishing; a participant is found to have read §7.2 or any V3 label
file; a GROUP-A participant or an ARM-A reference human is exposed to the question text; any
presented text differs from §7.2 byte-for-byte (beyond an `RC-CA-04` event handled by the surface);
any presentation order departs from §11.2-B or §12.5; a display behaviour is conditioned on claim
length or content (§13.2 item 4); PII appears in any evidence record; the identity custodian has not
been appointed before recruitment; any allocation-concealment rule of §6.1A is breached (an ID issued
without a completed commitment record, a draw not made uniformly from the unissued pool, a re-draw
or a re-issued ID, a draw made by anyone other than the custodian, or recruiter or operator access
to the enrolment log); a withdrawal arises whose
data consequence the pre-frozen governing rule does not already determine (§21.2 closure rule); the
surface used has not passed conformance verification against §13.2 (§13.3); an executable artifact
becomes necessary to proceed; or any clause of the Amendment or Hybrid contract would be
contradicted by continuing.

### §20.3 Pilot policy-undecidability STOP

    IF THE PILOT SHOWS MATERIAL POLICY AMBIGUITY OR POLICY UNDECIDABILITY
      (IND-6 / IND-7 / IND-11 / M-18 / M-14 by-disagreement concentration, escalated as findings)
    THEN: STOP · NO MAIN STUDY · OWNER POLICY-REVISION DECISION REQUIRED
    IF THE OWNER LATER REVISES:
      NEW eligibility_policy_version
      NEW protocol version where materially required
      NEW PILOT — ONLY UNDER SEPARATE OWNER AUTHORIZATION
    NO SILENT TUNING AND CONTINUATION `[FINDING ADM-10 / R16]`

### §20.4 Version-change rule

`ELIGIBILITY_POLICY_VERSION` changes on any material change to §3 – §5 (including §4A).
`PROTOCOL_VERSION` changes on any change to §6 – §21 once a version has been Owner-accepted; this
sibling keeps both strings because no prior v1 was accepted, authoritative or executed. A pilot
executed under a prior version supports no reliance under a new one; a new pilot is required,
subject to separate Owner authorization `[OWNER-PREMISE P3]`.

---

## §21. Privacy, consent, withdrawal, identity custody, provenance and retention

### §21.1 Two layers, kept apart

    PSEUDONYMOUS EVIDENCE RECORDS (§13.1): carry participant IDs only; no name, email, IP address,
      employer or demographic identifier; these are the study evidence, and whether any given
      participant's records are retained or removed is decided by the pre-frozen consent / privacy
      terms together with the applicable governing requirements (§21.2) — never automatically
      retained, never automatically deleted
    IDENTITY ↔ PSEUDONYM MAPPING + CONSENT / PAYMENT / WITHDRAWAL RECORDS: held ONLY by the
      Owner-designated human-study identity custodian, never in the evidence set, never committed
      to the repository, never seen by the Creator, the Lead, an analyst or a reviewer of the
      evidence

### §21.2 OWNER CONSENT / WITHDRAWAL POLICY — OWNER POLICY AUTHORITY `[N6]`

**This subsection is Owner policy authority, embedded materially and accurately. It is not a Creator
proposal and is not subject to Creator revision.** Where any other part of this protocol appears to
conflict with it, this subsection governs and the conflict is a defect of the protocol.

**Consent must precede participation.** Consent is obtained and affirmatively accepted before
enrolment, before any participant ID is issued and before any allocation is revealed (§6.1A E2).
Consent must truthfully disclose at minimum:

- the study / Evidence-Gate purpose;
- the nature of the task;
- the data recorded;
- the pseudonymous study identity;
- the existence of a separately controlled identity mapping;
- governance / Evidence-Gate / assurance / audit use;
- retention and deletion rules;
- withdrawal rights and their consequences;
- confidentiality boundaries;
- tool restrictions;
- the contact / escalation route required by the later authorized process.

The participant-facing expression of these elements is the consent summary reproduced in §12.1 and
carried into §12.2 and §12.3; the operative consent instrument is the consent form issued under this
policy before enrolment.

**After a valid withdrawal:**

    NO NEW RATINGS · NO NEW ADJUDICATION · NO NEW PARTICIPATION
    from that participant, unless a later valid consent / authorization permits it.

**Already-collected pseudonymous data:**

    AUTOMATIC UNIVERSAL RETROACTIVE DELETION: NO
    AUTOMATIC UNIVERSAL RETENTION: NO
    GOVERNING RULE: THE PRE-FROZEN CONSENT / PRIVACY TERMS
      + APPLICABLE GOVERNING PRIVACY / INSTITUTIONAL / LEGAL REQUIREMENTS
    NO POST-OUTCOME IMPROVISATION.

The consent / privacy terms that govern this question must therefore be frozen before recruitment,
as part of the consent instrument. This protocol does not set them: the retention period, the
payment-dispute grace period and the deletion mechanics are pre-frozen terms whose values are fixed
in the consent instrument under this policy and the applicable requirements, before recruitment and
before any collection. Any value appearing anywhere in this protocol is illustrative of the required
shape, never the operative term.

**Timing rules — binding.**

*Before reference freeze.* If the governing rule requires removal:

    REMOVE AS REQUIRED
    → RECOMPUTE REFERENCE
    → RECOMPUTE DENOMINATORS / STRATA (including C_I, C_S, A_C and the M-19 transition matrix)
    → NEW REFERENCE HASH / IDENTITY
    → FREEZE AGAIN, BEFORE MEASURED COLLECTION

*After reference freeze, before measured collection.* If removal is required:

    OLD REFERENCE FREEZE: INVALID
    MEASURED COLLECTION: MUST NOT START
    REPAIR / RECOMPUTE → NEW REFERENCE IDENTITY / HASH → NEW DENOMINATORS / STRATA → REFREEZE
    → APPLICABLE LEAD VALIDATION

*After measured collection has started.*

    CASE A — PREVIOUSLY COLLECTED DATA MAY REMAIN:
      FUTURE PARTICIPATION STOPS
      PREVIOUSLY VALID FROZEN DATA: MAY REMAIN
      REFERENCE DENOMINATORS: NO SILENT CHANGE
      NO RETROSPECTIVE RELABELLING SOLELY BECAUSE PARTICIPATION ENDED

    CASE B — PREVIOUSLY COLLECTED DATA MUST BE REMOVED:
      MEASURED LANE: STOP
      REFERENCE SUBJECT: MATERIALLY INVALIDATED WHERE AFFECTED
      NO SILENT RECOMPUTATION · NO POST-HOC DENOMINATOR CHANGE
      NO CONTINUATION AFTER OUTCOME VISIBILITY
      RETURN TO GOVERNED LEAD / OWNER ADJUDICATION

**Binding closure rule.**

    NO POST-HOC REFERENCE, STRATUM, DENOMINATOR, EXCLUSION OR DATA-RETENTION DECISION
    AFTER MEASURED OUTCOMES ARE VISIBLE,
    UNLESS THE PRE-FROZEN GOVERNING RULE ALREADY DETERMINES THE CONSEQUENCE.
    IF IT DOES NOT: STOP — RETURN TO OWNER.

**Identity custody.**

    OWNER-DESIGNATED HUMAN-STUDY IDENTITY CUSTODIAN: REQUIRED BEFORE RECRUITMENT
    ACTUAL CUSTODIAN: NOT APPOINTED
    PII ACCESS: NOT AUTHORIZED
    THE CUSTODIAN IS NOT BY DEFAULT: the Lead · the Creator · the Claim-Eligibility owner ·
      the progression owner · any new product-capability owner
    THIS PROTOCOL DOES NOT CREATE, APPOINT OR NOMINATE THE CUSTODIAN

Frozen required custodian duties: **minimum-necessary access** (the custodian alone holds the
mapping; no analyst, Creator, Lead or reviewer access); **identity / evidence separation** (the
custodian never receives ratings; the evidence never receives identity; the custodian performs the
§6.1A E4 issuance and holds the sealed enrolment log); **authorized disclosure boundary** (no
disclosure of any identity to anyone, including the Owner, except as required by law or by a
documented safety emergency, with the disclosure logged); **retention / deletion duties** (holding
the mapping and consent records only for the pre-frozen period, then verified deletion with a
deletion attestation in the pilot record); **auditability** (a log of every access to the mapping
and of every issuance, available to Owner-authorized audit without exposing identities); and receipt
and execution of withdrawal requests under the timing rules above. The custodian is excluded from
both study pools (§9).

    MATERIAL LEGAL / INSTITUTIONAL CONFLICT WITH THIS POLICY: STOP — RETURN TO OWNER.

**This Owner policy is not:** recruitment authorization · collection authorization · pilot
authorization · legal advice · a privacy-officer appointment.

### §21.3 Authorized-use statement (binding; matches the participant packets)

Pseudonymous evidence records — measured ratings, reference verdicts, reason codes, rationales,
timestamps, recognition answers and the domain-background covariate — are used for: the
Claim-Eligibility Human-Review Evidence Gate analysis; governance review of that gate (Lead review,
Independent Review B, later assurance reviews); audit; and Owner adjudication of the gate and its
consequences. They are not used to train or tune any model, for marketing, for product content, or
for any purpose outside that list. Reference verdicts are study evidence that defines the reference
basis, denominators and strata; they are not measured-reviewer outcome data. Any wider use requires
a new consent and a separate Owner decision.

### §21.4 Provenance, audit and retention of evidence

Rationales are stored verbatim; participants are told not to include personal information, and any
that appears is redacted in the evidence copy with the redaction logged. No claim text is drawn from
real user data. Audit preservation per Amendment §17 (Hybrid §19 retained, modified in scope): the
exact frozen claim set (§7.2), the instruction packets (§12), the frozen presentation orders
(§12.5), the eligibility policy version (§3), the reviewer / source configuration (§8, §11) and the
surface specification (§13.2) are preserved in this file; the reference and measured record sets are
hashed at freeze; the pilot record cites this protocol's accepted commit identity (established
externally), the surface identity and conformance evidence, the enrolment-log attestation and both
hashes. Evidence artifacts are held under the repository's existing evidence-retention practice for
governance evidence, subject in every case to the §21.2 disposition rule — the pre-frozen consent /
privacy terms plus applicable governing requirements — which decides whether any particular
participant's pseudonymous records are retained or removed; nothing here creates a new retention
owner and nothing here guarantees universal retention.

---

## §22. Owner decision map and sequencing `[FINDING L5 / R6; PROPOSAL for the restatement]`

| Decision | Content | State at this pre-freeze draft |
|---|---|---|
| D1 language scope | English only; any Arabic stratum via §16A amendment | SUPPLIED BY OWNER PREMISE (LANGUAGE) |
| D2 reviewer model | M1 measured + strictly separate 2+1 reference | SUPPLIED BY OWNER PREMISE (M1); arm-separated realisation is REPAIR-DESIGN PROPOSAL |
| D3 sources / data / privacy | controlled non-user corpus; no real user data | SUPPLIED BY OWNER PREMISE (S1); the consent / withdrawal policy of §21.2 is OWNER POLICY AUTHORITY, not a proposal |
| D-NEW-A review context | controlled claim-only vs claim + question comparison | SUPPLIED BY OWNER PREMISE (C3); the two-group realisation is REPAIR-DESIGN PROPOSAL |
| D-NEW-B candidate deployed `HUMAN_NOW` configuration | dual independent + fail-closed third human | SUPPLIED BY OWNER PREMISE (H2); the role model and final semantics (§8.2) are REPAIR-DESIGN PROPOSAL |
| D-NEW-C semantic validity anchors | the six anchors of §18 item 3 | **CLOSED — OWNER-FINAL**: `ACCEPT AS PROPOSED WITH GOVERNING BOUNDARY CLARIFICATIONS`; the six anchors are OWNER-ACCEPTED, MINIMUM MANDATORY, NON-EXHAUSTIVE, NON-SCORING and subordinate to the Claim-Sufficiency Policy |
| D-POLICY eligibility-policy version freeze | `CLAIM-ELIGIBILITY-SUFFICIENCY-EN-v1` (§3, §4A) | OPEN — this text is a pre-freeze draft; an Owner exact-SHA decision on a later frozen candidate would freeze the version text; it would not authorize the pilot |
| D-CUSTODIAN human-study identity custodian appointment | §21.2 duties | OPEN — NOT APPOINTED; required before recruitment; separate Owner decision |
| D-CONSENT pre-frozen consent / privacy terms (retention period, grace period, deletion mechanics, contact route) | §21.2 requires them frozen before recruitment | OPEN — values not set by this protocol; fixed in the consent instrument under Owner policy and applicable requirements |
| **D-OPEN-ΔS** Δ_S denominator (Option A: all governing-eligible first-pass rating records for the item × arm · Option B: committed substantive verdicts only, abstention carried by Δ_ABST_COMMON) | §14.1, §6.1, M-11, §15.3 PS-2 | **CLOSED — OWNER-FINAL** under `OWNER FINAL DECISION — D-OPEN-ΔS / PF-04 POLICY CLOSURE` `[PF-04]`: **OPTION A SELECTED** — the primary Δ_S is the MARGINAL EXACT-S / SUFFICIENT-ISSUANCE ESTIMAND, `p(i, arm)` = governing-eligible first-pass rating records with label == SUFFICIENT / all governing-eligible first-pass rating records for that item × arm, aggregated as the unweighted item-wise mean over the unchanged A_C. Option B (conceptually `P(S \| S OR I)`) is NOT SELECTED AS PRIMARY, is not statistically invalid, and is NOT DEFERRED / NOT TRACKED / NOT AN OBLIGATION. CA-EXTRINSIC sub-choice: **CLOSED — CA-E1** (no new ascertainment / exposure-timing regime). New CA worst-case / best-case bounding and a new OUT_OF_SCOPE-in-A_C interpretive note: NOT AUTHORIZED. Δ_FS_COMMON, Δ_FI_COMMON and Δ_ABST_COMMON are unaffected. This Owner decision governs the current mutable CEHR draft; it is not a merged repository authority |
| D-SURFACE study surface: identification of an authorized conformant surface, or separate executable-surface authorization | §13.2 specification, §13.3 routes 1 / 2 | OPEN — `EXISTING CONFORMANT STUDY SURFACE: NOT PROVEN`; `NEW EXECUTABLE STUDY SURFACE REQUIRED: NOT YET PROVEN REQUIRED`; nothing authorized here |
| D4-a tolerance direction and safety-critical metric list | fail-closed asymmetric; list in §16 | DIRECTION SUPPLIED BY OWNER PREMISE (T1); metric list is PROPOSAL |
| D5 pilot execution authorization | separate explicit Owner authorization naming the study surface | NOT GRANTED — the full §30 lifecycle (immutable freeze → Lead post-freeze identity / differential review → Independent Review B of the exact pre-execution subject → Lead final adjudication → Owner exact-SHA decision) must precede it (§23, §13.3, §30) |
| PILOT | this protocol | NOT EXECUTED |
| D4-b main-study thresholds / sample size | taken on the pilot's PS-3 components, abstention and indeterminacy outputs | DEFERRED TO POST-PILOT |
| D6 main-study execution authorization | separate from D4-b | NOT GRANTED |

The open items before D5 are D-POLICY (via Owner exact-SHA acceptance of a later frozen candidate
carrying this text), D-CUSTODIAN, D-CONSENT, D-SURFACE with its conformance verification,
confirmation of the D4-a metric list, and D5 itself; no single decision count is asserted. D-NEW-C
and D-OPEN-ΔS are CLOSED (OWNER-FINAL).

---

## §23. Independent Review B fence `[FINDING ADM-9 / R15]`

    INDEPENDENT REVIEW B = governance / assurance review of an EXACT IMMUTABLY FROZEN protocol
      candidate — never of a mutable pre-freeze draft
    REVIEW B OCCURS ONLY AFTER, IN THIS ORDER (§30): a clean pre-freeze gate → Owner freeze
      adjudication / applicable freeze authority → IMMUTABLE FREEZE → LEAD POST-FREEZE IDENTITY /
      DIFFERENTIAL REVIEW. It never runs on this draft and never runs before that review
    INDEPENDENT REVIEW B IS NOT FINAL PRE-EXECUTION ASSURANCE UNTIL THE APPLICABLE EXACT SURFACE
      ASSURANCE SUBJECT EXISTS AND HAS BEEN REVIEWED (§13.3) `[N8]`
    INDEPENDENT REVIEW B != a participant · != a reference adjudicator · != a HUMAN_NOW evidence
      source · != human outcome collection · != HUMAN STUDY REFERENCE ADJUDICATION
    REVIEW B IS ALWAYS SEPARATE AND MANDATORY BEFORE D5 — no "combined with A" route exists
    INDEPENDENT REVIEW B: NOT STARTED · NOT AUTHORIZED TO START
    INDEPENDENT REVIEW B AS FINAL PRE-EXECUTION ASSURANCE: NOT AVAILABLE YET (§13.3)
    A person who performs Review B is excluded from both study pools (§9)

---

## §24. Lane separations and non-effects

    G-4-A TECHNICAL DEFECT: CURRENT — NOT FIXED
    DIRECT G-4-A REMEDIATION: DEFERRED — NOT CANCELLED
    CEHR PREREQUISITE FOR FUTURE DIRECT G-4-A ENGINE REPAIR: NOT ADJUDICATED
    T1-A′: OPEN — TRIGGER FIRED — CLOSURE EVIDENCE NOT MET — not advanced, not closed
    G-4-B: OPEN / DEFERRED — not started, not absorbed · M-1: PRESERVED / SEPARATE — not absorbed
    RUN-004: NOT AUTHORIZED · NO S2 EXECUTION · COMMITTED S2 FIXTURES NOT CONSUMED
    R4–R8: NOT AUTHORIZED · HICR PHASE 2: NOT AUTHORIZED · READINESS IMPLEMENTATION: NOT AUTHORIZED
    PRE-FCORA: MANDATORY LATER — NOT STARTED / NOT MOVED · FCORA: NOT AUTHORIZED
    LEVEL 1 / 2 / 3 REOPENED: NO · H∧P REOPENED: NO · O2 SELECTED: NO · O4 AUTHORIZED: NO
    LEVEL 4 AUTHORIZED: NO · LEVEL-0 AI BOUNDARY AMENDMENT: NO
    NEW EVENT VOCABULARY: NO · NEW PROGRESSION OWNER: NO · NEW ASSESSMENT OWNER: NO
    NEW LANGUAGE OWNER: NO · NEW HUMAN-STUDY IDENTITY OWNER APPOINTED: NO · PII ACCESS GRANTED: NO
    RECORD-CONTRACT IMPLEMENTATION: NO · SCHEMA CHANGE: NO · RUNTIME CHANGE: NO
    NEW DOR OWNER: NO · NEW DOR ROW: NO
    ARABIC WIDENING: NO · REAL USER DATA AUTHORIZED: NO
    REVIEWER RECRUITMENT: NO · HUMAN COLLECTION: NO · REFERENCE HUMAN ADJUDICATION: NO · PILOT: NO
    FALSE-CLOSURE EXECUTION: NO · EXECUTABLE STUDY SURFACE WORK PERFORMED: NO
    CUSTODIAN APPOINTED: NO · PII ACCESS: NO · CONSENT COLLECTED: NO
    T2-G: NOT ACTIVATED · WS10 / WS11 / WS12: UNCHANGED · B2: PRESERVED FUTURE CANDIDATE
    ACTIVE CONTRACT: NONE (untouched) · PSRR GO: NO
    SERIOUS RELEASE / PRODUCTION / PAID ACTIVATION: NOT AUTHORIZED · `main` NOT RECONCILED

Follow-up governance synchronization (roadmap, Owner Decision Register, Deferred Obligations
Register, `CURRENT_PROJECT_STATE.md`) is `NOT PART OF THIS PRE-FREEZE DRAFT` and is a later,
separately authorized act.

---

## §25. Freeze-requirement index (26 load-bearing areas)

| # | Area | Where frozen |
|---|---|---|
| 1 | truthful lifecycle / status + authority hierarchy | header, §0 |
| 2 | exact eligibility policy version and P3 normative policy | §3, §4A |
| 3 | protocol version | header, §3.1, §13.1 |
| 4 | C3 exact study arms | §6.1 |
| 5 | exact frozen corpus / item content | §7.2 |
| 6 | item IDs / family IDs / source classes | §7.2, §7.3 |
| 7 | exact English claims | §7.2 |
| 8 | exact claim↔question / context pairings | §6.2, §7.3 |
| 9 | exact load-bearing question / context text + immutable identity / version | §6.2 |
| 10 | exact study-label vocabulary | §4, §4A |
| 11 | exact reason-code vocabulary | §5 |
| 12 | H2 study source-simulation / escalation rule | §8.2 |
| 13 | M1 measured-reviewer model | §8.1 |
| 14 | strictly separate M1 reference-adjudication model | §8.3 |
| 15 | S1 claim-source / corpus model | §7.1 |
| 16 | T1 safety / materiality direction | §16 |
| 17 | reviewer qualification / COI / tool restrictions | §9 |
| 18 | blinding / contamination fences | §10 |
| 19 | assignment / balanced assignment / randomization / counterbalancing | §6.1, §11.1, §11.2 |
| 20 | repeat / paraphrase structure | §11.3, §7.3 |
| 21 | semantic-validity anchors / minimal-pair structure | §7.3, §18 |
| 22 | metric definitions + numerator / denominator / unit / exclusions / basis | §14 |
| 23 | statistical-analysis / dependence framework | §15 |
| 24 | privacy / provenance / audit / retention + STOP / deviation / version-change rules | §20, §21 |
| 25 | deferred product-population-exposure sub-limb + false-closure design + residual direct-G-4-A defect return rule | §17, §19, §1 |
| 26 | original 17-item ledger + separate integrated R1–R17 coverage matrix | §26, §27 |

Added beyond the 26 by the M1–M9 sibling and preserved here: the label-boundary event table (§4A),
the study-surface specification and realisation status (§13.2, §13.3), the identity-custodian duties
(§21.2) and the M1–M9 repair matrix (§28). Added by this N1–N8 sibling: allocation concealment
(§6.1A), the frozen presentation orders (§12.5), the common comparative strata and reference
transition matrix (§14.1, M-19), the frozen statistical procedures PS-1 … PS-7 in their N7 form
(§15), the embedded Owner consent / withdrawal policy (§21.2) and the N1–N8 crosswalk (§29).

---

## §26. Ledger A — original accepted findings (L1–L6, ADM-1–ADM-11)

    DESIGN ACCOUNTED: 17 / 17
    GOVERNANCE CONSUMED: 0 / 17
    DISCHARGED: 0 / 17
    CLOSED: 0 / 17

Source / provenance for every row: preserved Independent Review return, File Library artifact
`file_00000000677881f4a2f7dd2f303600fc` ("Pasted markdown.md", created 2026-09-02T18:17:35Z),
subject *INDEPENDENT REVIEW RETURN — G-4-A ROUTE B — CLAIM-ELIGIBILITY HUMAN-REVIEW EVIDENCE-GATE
DESIGN*, section named in the row. Mechanical presence of a repair in this pre-freeze draft does not
establish substantive repair quality; every status below awaits Lead review, Independent Review B
and Owner exact-SHA acceptance, and none is consumed, discharged or closed by this pre-freeze
draft.

| Item | Exact finding (source section) | Design disposition | Protocol section(s) | Status | Rationale |
|---|---|---|---|---|---|
| L1 | *L1 — ELIGIBILITY POLICY / CLAIM-SUFFICIENCY AUTHORITY*: the sufficiency definition requires an explicit Owner policy freeze before pilot; the instrument is a frozen Owner-authorized `eligibility_policy_version`, not a contract amendment (English scope); Hybrid §5 is superseded / deferred and must be disclosed as such; review context must be an Owner decision | policy frozen as a named version with its authority basis and the Hybrid §5 disclosure; review context carried as two independent randomized groups | §3.1, §3.3, §6 | REQUIRES OWNER DECISION (D-POLICY) + REQUIRES BOUNDED REPAIR — repair proposed here; NOT CONSUMED | the policy text exists only as pre-freeze draft text until Owner exact-SHA acceptance; the finding's third limb is carried by Owner premise C3 |
| L2 | *L2 — HYBRID §16A / ARABIC SCOPE*: `CURRENT CONTRACT-AUTHORIZED EVIDENCE SCOPE = ENGLISH ONLY`; an Arabic stratum requires a §16A amendment through the full lifecycle, not an Owner reading; preserve `ARABIC PRODUCT OBLIGATION != CURRENT EVIDENCE-GATE EXECUTION AUTHORITY` and the English-only fallback with a recorded Arabic unvalidated-gap obligation | English-only protocol; Arabic stratum excluded; instrument stated; obligation requirement recorded without a register act | §2 (LANGUAGE), header | REQUIRES BOUNDED REPAIR — proposed here; any Arabic stratum REQUIRES OWNER DECISION via amendment; NOT CONSUMED | no Arabic text is used, including the committed `text_ar` |
| L3 | *L3 — MATERIALITY RULE / INVENTED THRESHOLDS*: distinguish MATERIALITY INDICATOR (mandatory escalation) from BINDING MATERIALITY THRESHOLD (Owner only); no Creator numeric / absolute pass rule | indicator / threshold split; nine indicators frozen; zero thresholds | §16 | REQUIRES BOUNDED REPAIR — proposed here; thresholds REQUIRE OWNER DECISION (D4-a / D4-b); NOT CONSUMED | Owner premise T1 forbids a Creator threshold; the protocol complies |
| L4 | *L4 — SAMPLE-SIZE / INDEPENDENCE MODEL*: declare the unit of analysis per metric; size with a design effect over item- and reviewer-level clustering; cluster-aware intervals; planning ranges, not minimums; ρ and abstention are pilot outputs; no final N | unit of analysis on every metric; positive-weight multiplier bootstrap, GLMM → Bayesian chain and deletion envelopes frozen (§15, N7 form); the naive VIF product removed from every role; `FINAL MAIN-STUDY N: NOT DETERMINED NOW` | §14, §15 | REQUIRES BOUNDED REPAIR — proposed here; final sizing DEFERRED TO POST-PILOT (D4-b); NOT CONSUMED | the roster of 18 is a pilot planning value, not a minimum |
| L5 | *L5 — OWNER DECISION SEQUENCING*: PRE-PILOT (D1, D2, D3, D-NEW-A, D-NEW-B, D4-a) → D5 → PILOT → D4-b → D6; `MINIMUM OWNER DECISION COUNT: 5` is incorrect as stated | decision map with the supplied-by-premise / open state of each decision, now including custodian and surface decisions; no single count asserted | §22 | REQUIRES OWNER DECISION (open items) + REQUIRES BOUNDED REPAIR — restatement proposed here; NOT CONSUMED | several decisions are already supplied by Owner premises; the rest remain open |
| L6 | *L6 — G-4-A EXPOSURE RATE*: designer-set composition is not a population rate; rename to `STUDY-CORPUS G-4-A CONDITION PROPORTION`; record `G-4-A EXPOSURE RATE: NOT MEASURED — DEFERRED WITH RETURN CONDITION` with a return gate; state the sampling-frame requirement; label conditional stress-test figures as conditional | naming discipline; deferred sub-limb with return; sampling-frame requirement; conditional labelling | §14 M-15 / M-16, §17 | REQUIRES BOUNDED REPAIR — proposed here; population sub-limb DEFERRED TO POST-PILOT (return before implementation authorization); NOT CONSUMED | routed to the existing register obligation; no new row |
| ADM-1 | *ADM-1 — `HUMAN_NOW` operational unit is never defined*: name the candidate deployed configuration; derive configuration-level FS / FI from individual verdicts under a pre-registered aggregation rule that is not "majority = truth" | H2 named as candidate configuration; one frozen primary role model with complete final semantics; configuration-level metrics alongside individual | §8.2, §11.2-D, §14 M-04 | REQUIRES BOUNDED REPAIR — proposed here; the configuration itself is SUPPLIED BY OWNER PREMISE (H2); NOT CONSUMED | the third-human path is simulated from a blind ROLE-3 rating, and that limit is disclosed |
| ADM-2 | *ADM-2 — reference truth is policy-internal, and the design does not say so*: state the limit; add a policy-validity axis (minimal-pair discrimination; post-hash intent divergence); restrict permitted conclusions | P-9 statement; construct-validity axis; intent unsealed only after reference hash | §3.3 P-9, §18, §7.4 | REQUIRES BOUNDED REPAIR — proposed here; the anchor selection it depended on is now CLOSED by Owner decision D-NEW-C (§18 item 3); NOT CONSUMED | the sealed labels are visible in the file; the seal is personnel / ordering, disclosed |
| ADM-3 | *ADM-3 — retained product-truth metric semantics*: `FALSE CAUSAL CREDIT RATE` and `GENUINE CAUSAL EVIDENCE WITHHELD RATE` are corpus-conditional; basis qualifiers and `NOT A PRODUCT-POPULATION RATE` on every retained metric | mandatory basis qualifier; conditional analogues only, on frozen primary sets | §14.1, §14.2 M-16, §17.1 | REQUIRES BOUNDED REPAIR — proposed here; NOT CONSUMED | no marginal product rate is reported by this protocol |
| ADM-4 | *ADM-4 — FS / FI analysis set and denominators undefined*: first-pass verdicts on distinct source items are the FS / FI analysis set; repeats → stability; siblings → paraphrase axis; unit of analysis per metric | frozen S_P / S_S sets; primary error sets; repeats only in M-08; siblings only on the construct axis, with NO error-rate analysis of any kind including them (§14.1) | §14.1 | REQUIRES BOUNDED REPAIR — proposed here; NOT CONSUMED | — |
| ADM-5 | *ADM-5 — abstention folded into TRUE INSUFFICIENT*: abstention never a correct negative; report two-sided | CANNOT_ADJUDICATE excluded from committed denominators; M-05 two-sided; M-03 committed only; H2 rule never counts an abstention toward either committed count | §4, §4A, §8.2, §14 | REQUIRES BOUNDED REPAIR — proposed here; NOT CONSUMED | FS-all reported only alongside FS-committed, never alone |
| ADM-6 | *ADM-6 — reference-adjudicator exclusion internally impossible*: exclude Level-1/2/3-exposed personnel from the reference panel entirely; delete the non-anchor carve-out | full exclusion; no carve-out; protocol-file exposure added as an exclusion | §8.3, §9 | REQUIRES BOUNDED REPAIR — proposed here; NOT CONSUMED | — |
| ADM-7 | *ADM-7 — false-closure projection under-specified and mis-attributed*: specify domain assignment, harness, exact engine pin, the human × engine attribution limit; classify the harness as a separately authorized artifact; withdraw "requiring no code change" | design-only projection with the required future inputs and the attribution limit; harness NOT created | §19 | REQUIRES BOUNDED REPAIR — proposed here; execution DEFERRED TO POST-PILOT under separate authorization; NOT CONSUMED | `HARNESS: NO · EXECUTION: NO` |
| ADM-8 | *ADM-8 — number of distinct measured reviewers never stated*: state a minimum roster as a planning parameter with justification; reviewer as random effect with a reported variance component | roster 18 (9 + 9) with rationale; reviewer random effect (PS-3); reviewer resampling (PS-1) | §11.1, §15.2 | REQUIRES BOUNDED REPAIR — proposed here; NOT CONSUMED | 18 is a planning value, not a minimum for the main study |
| ADM-9 | *ADM-9 — "PRE-EXECUTION PROTOCOL REVIEW — COMBINED WITH A" route*: Review B always separate and mandatory before D5 | fence stated; no combined route; Review B is not final pre-execution assurance until the exact surface assurance subject exists and has been reviewed | §23, §13.3 | REQUIRES BOUNDED REPAIR — proposed here; NOT CONSUMED | Review B is not started by this pre-freeze draft |
| ADM-10 | *ADM-10 — no route for pilot-demonstrated policy undecidability*: STOP → Owner policy-revision → new `eligibility_policy_version` → re-pilot; never silent tuning | undecidability STOP rule | §20.3 | REQUIRES BOUNDED REPAIR — proposed here; NOT CONSUMED | — |
| ADM-11 | *ADM-11 — over-claimed status lines*: correct `MATERIAL UNRESOLVED STUDY-DESIGN BLOCKERS: 0`, `EVIDENCE-GATE DESIGN COMPLETE: YES`, and the permitted conclusion of the prior design's §26 row 1 | no such lines exist in this pre-freeze draft; the header and §4 fences state `HUMAN_NOW: UNVALIDATED / INCONCLUSIVE`; the only permitted form of a future conclusion is the conformance-under-policy-version form of §3.3 P-9 | header, §3.3 P-9, §4 | REQUIRES BOUNDED REPAIR — addressed by the truthful header of this pre-freeze draft; the prior design's own lines are not edited here; NOT CONSUMED | this pre-freeze draft makes no design-complete or blocker-zero claim |

---

## §27. Ledger B — integrated R1–R17 coverage matrix

    DESIGN ACCOUNTED: 17 / 17
    GOVERNANCE CONSUMED: 0 / 17
    DISCHARGED: 0 / 17
    CLOSED: 0 / 17

Source / provenance for every row: the *EXACT REPAIR SET (single pass — complete)* of the same
preserved Independent Review return (`file_00000000677881f4a2f7dd2f303600fc`). Ledger B is a
separate accounting surface from Ledger A: no L↔R or ADM↔R equivalence is asserted beyond what the
source's own repair text names.

| R | Requirement (source wording, abbreviated only where marked …) | Source / provenance | Protocol section(s) | Disposition | Coverage evidence | Status |
|---|---|---|---|---|---|---|
| R1 | Disclose Hybrid §5's `SUPERSEDED / DEFERRED WITH RETURN CONDITION` disposition wherever relied on; restate the (a)(b)(c) definition as `[DESIGN — REQUIRES FROZEN OWNER-AUTHORIZED ELIGIBILITY-POLICY VERSION BEFORE D5]`; correct the reasoning to the Amendment-§6 policy-version basis | R1 | §3.1, §3.3 | COVERED IN DESIGN | §3.1 `HYBRID §5 DISCLOSURE` and `AUTHORITY BASIS` lines; policy status line names D5 | NOT CONSUMED / NOT DISCHARGED / NOT CLOSED |
| R2 | Convert the review context (CLAIM ONLY / CLAIM + QUESTION / controlled within-study condition) into an explicit pre-pilot Owner decision; reverse the prior Q4 classification; record the Hybrid §14 question-identity-persistence obligation as triggered at design time if CLAIM + QUESTION is selected | R2 | §6.1, §6.2, §22 | COVERED IN DESIGN (decision supplied by Owner premise C3; realisation = two randomized groups) | controlled arms; `[DEFERRED]` persistence obligation paragraph; D-NEW-A row | NOT CONSUMED / NOT DISCHARGED / NOT CLOSED |
| R3 | Restate the Arabic stratum as requiring an explicit §16A contract amendment through the full lifecycle; state `CURRENT CONTRACT-AUTHORIZED EVIDENCE SCOPE = ENGLISH ONLY`; preserve the English-only fallback and the recorded Arabic unvalidated-gap obligation; preserve `ARABIC PRODUCT OBLIGATION != CURRENT EVIDENCE-GATE EXECUTION AUTHORITY`; repair the draft packet's LANGUAGE SCOPE line | R3 | §2 (LANGUAGE), header | COVERED IN DESIGN (no draft packet exists in this pre-freeze draft) | the four statements appear verbatim in §2 | NOT CONSUMED / NOT DISCHARGED / NOT CLOSED |
| R4 | Rewrite the materiality paragraph: reclassify (2a), (3), (5) and paraphrase / language instability as MATERIALITY INDICATORS; every binding determination reduces to an Owner-set tolerance; repair the "no systematic FS pattern" condition identically | R4 | §16 | COVERED IN DESIGN | IND-1 … IND-9 are escalation-only; no binding threshold exists | NOT CONSUMED / NOT DISCHARGED / NOT CLOSED |
| R5 | Replace the independence model: unit of analysis per metric; design effect over item- and reviewer-level clustering; cluster-bootstrap / GEE intervals; relabel 170–250 and the floors as PLANNING RANGES; ρ and abstention are pilot outputs; propose no final N | R5 | §14, §15 | COVERED IN DESIGN | each metric names its unit; PS-1 … PS-7 frozen with pre-frozen fallbacks and diagnostics; `FINAL MAIN-STUDY N: NOT DETERMINED NOW` | NOT CONSUMED / NOT DISCHARGED / NOT CLOSED |
| R6 | Restructure to PRE-PILOT (D1, D2, D3, D-NEW-A, D-NEW-B, D4-a) → D5 → PILOT → D4-b → D6; correct `MINIMUM OWNER DECISION COUNT` | R6 | §22 | COVERED IN DESIGN | decision map; count not restated as a single number | NOT CONSUMED / NOT DISCHARGED / NOT CLOSED |
| R7 | Rename to `STUDY-CORPUS G-4-A CONDITION PROPORTION`; record `G-4-A EXPOSURE RATE: NOT MEASURED BY THIS GATE — DEFERRED WITH RETURN CONDITION` with a DOR row and return gate; state the sampling-frame requirement; basis qualifiers and `NOT A PRODUCT-POPULATION RATE` on the two other corpus-conditional metrics | R7 | §14 M-15 / M-16, §17 | COVERED IN DESIGN, WITH ONE DIVERGENCE DISCLOSED: no new DOR row is created (Lead instruction — `DOR MUTATION: NO`); the obligation is routed to the existing register row | §17.1 lines; §17.3 routing | NOT CONSUMED / NOT DISCHARGED / NOT CLOSED |
| R8 | Define the candidate deployed `HUMAN_NOW` configuration(s) as an Owner decision; add a pre-registered aggregation rule; report FS / FI / agreement / throughput at configuration level as well as individual level | R8 | §8.2, §11.2-D, §14 M-04 / M-07 / M-13 | COVERED IN DESIGN (configuration supplied by Owner premise H2; one frozen primary role model) | role table; final-semantics table; configuration-level metrics | NOT CONSUMED / NOT DISCHARGED / NOT CLOSED |
| R9 | State the policy-internal limit of reference truth; add the minimal-pair discrimination metric and the post-hash intent-divergence analysis; downgrade the permitted conclusion | R9 | §3.3 P-9, §18, §7.4, §14 M-09 / M-10 | COVERED IN DESIGN | P-9; §18 items 1–4; sealed-intent ordering | NOT CONSUMED / NOT DISCHARGED / NOT CLOSED |
| R10 | Define the FS / FI analysis set and denominators (first-pass, distinct source items); route repeats to stability and siblings to the paraphrase axis only | R10 | §14.1 | COVERED IN DESIGN | frozen S_P / S_S; primary sets; no all-item error sensitivity exists (§14.1) | NOT CONSUMED / NOT DISCHARGED / NOT CLOSED |
| R11 | Remove `CANNOT ADJUDICATE` / `OUT-OF-SCOPE` from TRUE INSUFFICIENT; report abstention on both sides | R11 | §4, §4A, §14 M-03 / M-05 | COVERED IN DESIGN | `ABSTENTION != TRUE NEGATIVE`; M-05 two-sided | NOT CONSUMED / NOT DISCHARGED / NOT CLOSED |
| R12 | Exclude Level-1/2/3-exposed personnel from the reference panel entirely; delete the "non-anchor items" carve-out | R12 | §8.3, §9 | COVERED IN DESIGN | exclusion paragraph; "carve-out is not carried" | NOT CONSUMED / NOT DISCHARGED / NOT CLOSED |
| R13 | Specify the false-closure projection: domain assignment, session harness, exact engine pin, the human × engine attribution limit, the harness as a separately authorized analysis artifact; withdraw "requiring no code change" | R13 | §19 | COVERED IN DESIGN (design only; inputs named; nothing executed) | §19 input list and fences | NOT CONSUMED / NOT DISCHARGED / NOT CLOSED |
| R14 | State a minimum distinct-reviewer roster size as a planning parameter; treat reviewer as a random effect with a reported variance component | R14 | §11.1, §15.2 PS-3, §14 M-17 | COVERED IN DESIGN | roster 18 with rationale; PS-3 primary and Bayesian governing fallback | NOT CONSUMED / NOT DISCHARGED / NOT CLOSED |
| R15 | Make Independent Review B always separate and mandatory before D5; delete the "COMBINED WITH A" route | R15 | §23 | COVERED IN DESIGN | fence lines | NOT CONSUMED / NOT DISCHARGED / NOT CLOSED |
| R16 | Add the pilot-undecidability route: STOP → Owner policy-revision decision → new `eligibility_policy_version` → re-pilot | R16 | §20.3 | COVERED IN DESIGN | STOP rule | NOT CONSUMED / NOT DISCHARGED / NOT CLOSED |
| R17 | Correct the prior design's §41 and §46 status lines and §26 row 1 per ADM-11 | R17 | header, §3.3 P-9, §4 | COVERED IN DESIGN for this pre-freeze draft's own status surface; the prior design return is a preserved non-repository artifact and is not edited | truthful header; `HUMAN_NOW: UNVALIDATED / INCONCLUSIVE` | NOT CONSUMED / NOT DISCHARGED / NOT CLOSED |

---

## §28. M1–M9 repair matrix (Lead single-pass findings on the prior candidate `63999d5d…`)

**Historical preservation notice.** This matrix records the M1–M9 repair **as it was made in the
frozen candidate `ef74f1b3…`**. It is preserved unedited as differential provenance. Where the
later N1–N8 repair (§29) changed one of those repairs, the N-row governs and this matrix's
description of that repair is historical, not current: specifically M1 (the arm design gains the
allocation concealment of §6.1A — N1), M4 (the length-conditioned marker described here is removed —
N5), M7 / M8 (the analysis sets gain per-arm references and common strata — N2 — and the statistical
procedures described here, including the Clopper–Pearson and Henderson III fallbacks, are replaced
by §15 in its N7 form), and M9 (the surface status asserted here is corrected to `NOT YET PROVEN
REQUIRED` — N8). Nothing in this matrix is a current governing method.

    M1–M9: 9 / 9 MECHANICALLY ACCOUNTED
    REPAIR COMPLETE: NOT A CREATOR DECLARATION OF ACCEPTANCE
    MECHANICAL 9 / 9 != SUBSTANTIVE LEAD PASS
    SUBSTANTIVE LEAD PASS != INDEPENDENT REVIEW B PASS
    INDEPENDENT REVIEW B PASS != OWNER EXACT-SHA ACCEPTANCE

| Lead defect | Exact defect | Repair | Protocol section(s) | Mechanical coverage | Residual limitation | Status |
|---|---|---|---|---|---|---|
| M1 | C3 arm / order confound: ARM-A always preceded ARM-B within reviewer, so context arm coincided with order, learning, fatigue and question exposure; a position covariate cannot remove a complete confound | two independent randomized reviewer groups (A-only / B-only), pair-blocked by enrolment order; identical item set and order procedure in both groups; estimand, units, assignment rule, balancing, cross-arm exposure rule, coverage, identification and residuals frozen; `C3 ORDER CONFOUND REMAINING: NO`; C3 construct unchanged | §6.1, §11.1, §11.2-A/B, §15 PS-2 | design constants and frozen tables present; within-reviewer blocking removed everywhere (§10, §11.3, §12) | the arm contrast is between randomized groups of 9 reviewers, so its precision is that of a pilot; chance covariate imbalance is reported, not adjusted | MECHANICALLY ACCOUNTED — awaiting Lead substantive review |
| M2 | H2 primary role assignment / final semantics: all three unordered pairs were treated as three deployments (correlated pseudo-deployments); no deterministic primary configuration; post-escalation semantics incomplete | one frozen primary role model (ROLE-1 / ROLE-2 / ROLE-3 per study item, table §11.2-D, seeded, balanced, frozen before outcomes; post-hoc choice prohibited); exhaustive final-semantics table for every initial state and every third outcome; fail-closed asymmetric; primary estimands on the frozen roles only; all-pairs demoted to secondary / sensitivity | §8.2, §11.2-D, §14 M-04, §15 PS-5 | role table covers 114 study items; semantics table covers all 10 initial-state classes × all third outcomes | ROLE-3 rated blind and simultaneously, unlike a deployed third human who would know an escalation occurred; disclosed | MECHANICALLY ACCOUNTED — awaiting Lead substantive review |
| M3 | Reference 2+1 contamination (shared RA-3 across arms) and semantic contradiction (CANNOT_ADJUDICATE both a possible reference outcome and REFERENCE-INDETERMINATE) | six arm-separated reference humans (RA-A1/A2/A3, RA-B1/B2/B3), no cross-arm service or exposure; exact assignment, sequence, blinding; one semantic path: CANNOT_ADJUDICATE = per-adjudicator abstention, never an outcome; REFERENCE-INDETERMINATE = verdict; deterministic outcome rule requiring two concurring humans; no forcing of ambiguity | §8.3, §12.3, §12.4, §4A | rule enumerated; reference labels and capture aligned (§13.1 `policy_clause` empty on abstention) | one more reference human than the prior design (six); the third role in each arm sees only escalated items | MECHANICALLY ACCOUNTED — awaiting Lead substantive review |
| M4 | Label-boundary contradiction for empty / broken / non-claim content (P-6 and RC-OS-03 put "empty or defective presentation" under OUT_OF_SCOPE while RC-CA-04 put presentation defects under CANNOT_ADJUDICATE) | event table §4A: E-EMPTY-ANSWER → INSUFFICIENT (F2, RC-I-05, with the frozen "shown in full" marker); E-PRESENTATION-DEFECT → CANNOT_ADJUDICATE (RC-CA-04); E-NON-CLAIM → OUT_OF_SCOPE; E-NON-ENGLISH → OUT_OF_SCOPE; policy, reason codes, both packets, reference packet, capture (`presentation_status`), surface (items 4, 19) and analysis exclusions synchronized | §3.3 P-5 / P-6, §4A, §5, §12, §13.1, §13.2, §14.1 | no two labels valid for one event; marker defined as part of the frozen presentation | no literally empty item exists in the corpus; E-EMPTY-ANSWER is exercised by near-empty items only | MECHANICALLY ACCOUNTED — awaiting Lead substantive review |
| M5 | Untruthful participant / reference disclosure: measured packets implied real-inventor provenance; reference humans told their judgments were "not study data"; privacy text claimed no identifying detail anywhere and no use outside the study | packets describe the texts as controlled, synthetic inventor-style answer texts not taken from real users; reference packet states their verdicts are study evidence defining the reference basis; disclosures separate pseudonymous evidence records from custodian-held identity mapping; bounded authorized-use statement (gate analysis, governance review, audit, Owner adjudication; no model training, marketing or other use) | §12.1, §12.2, §12.3, §21.1, §21.3, §9 | statements appear in every packet and in §21 | disclosing synthetic provenance is itself a design choice whose effect on reviewer behaviour is unmeasured; it is the truthful option | MECHANICALLY ACCOUNTED — awaiting Lead substantive review |
| M6 | Identity ↔ pseudonym mapping ledger assigned to the Lead without authority | Owner-designated human-study identity custodian required before recruitment; duties and boundaries frozen (custody, minimum-necessary access, separation, consent, withdrawal, retention, deletion, auditability, disclosure boundary, breach handling); `HUMAN IDENTITY CUSTODIAN: NOT APPOINTED`; no Lead / Creator / capability-owner assignment; `PII ACCESS AUTHORIZED NOW: NO`; D-CUSTODIAN added | §21.2, §22, §9, §20.2 | required status lines present; custodian excluded from pools; STOP if not appointed before recruitment | retention grace period (90 days) is a PROPOSAL awaiting Owner decision | MECHANICALLY ACCOUNTED — awaiting Lead substantive review |
| M7 | FS / FI / sibling analysis-set contradiction (siblings excluded from M-01 – M-04 in one place, included in M-16's list in another) | frozen analysis sets S_P (45) / S_S (12); primary FS, FI, H2 and G-4-A-conditional sets defined on S_P; siblings confined to the construct axis (M-09, M-10) and to a labelled SECONDARY CORRELATED SENSITIVITY with MP-group clustering; M-01 / M-02 / M-04 / M-09 / M-10 / M-12 / M-16 restated consistently | §14.1, §14.2 | every primary set enumerated; M-16 candidate lists restricted to S_P | primary G-4-A conditional set holds 15 sealed candidates; the MC siblings carrying the G-4-A surface with a real mechanism are analysed only on the construct axis | MECHANICALLY ACCOUNTED — awaiting Lead substantive review |
| M8 | Load-bearing statistical procedures deferred to an unreviewed later plan; naive VIF product stated as sizing law | seven primary procedures frozen (PS-1 … PS-7) each with estimand, unit, estimator / model, dependence, uncertainty, failure condition, pre-frozen fallback, what the fallback estimates, rationale; crossed pigeonhole bootstrap (Owen–Eckles) as the non-parametric interval; crossed-intercept logistic GLMM with Henderson III fallback for components; seeds and B frozen; VIF product demoted to heuristic; `LOAD-BEARING ANALYSIS DEFERRED OUTSIDE SUBJECT: 0` | §15 | primary / fallback ordering pre-frozen; no outcome-dependent choice | pilot-scale precision is limited; zero-event fallbacks estimate item-level any-event probabilities and are named as such | MECHANICALLY ACCOUNTED — awaiting Lead substantive review |
| M9 | No frozen study-surface specification; implementation status unstated | 32-invariant non-executable surface specification covering every listed interaction (presentation, arms, order, reason codes, labels, fields, rationale, submit, change rules, navigation, missing / broken items, timeout, interruption, resume, repeats, recognition, capture, timestamps, export, canonicalisation, pseudonymous display, errors, accessibility, operator boundary, consent); truthful realisation status: no existing surface (repository check), `NEW EXECUTABLE SURFACE REQUIRED: YES`, `EXECUTABLE SURFACE CREATED: NO`, `INDEPENDENT REVIEW B SUBJECT READY: NO`; later sequence frozen | §13.2, §13.3, §22 (D-SURFACE), §23 | specification present; status lines present; STOP recorded | the STOP — EXECUTABLE STUDY SURFACE REQUIRED applies after this freeze; no surface work is authorized or performed | MECHANICALLY ACCOUNTED — awaiting Lead substantive review |

---

## §29. N1–N8 repair crosswalk (Lead / independent findings on the prior candidate `ef74f1b3…`)

**HISTORICAL / SUPERSEDED / NON-GOVERNING where it quotes earlier design text.** The "Exact defect"
and "Repair" columns describe the state of the prior candidates and the change made to them; the
wording they quote — ascending or pair-blocked allocation, the length-conditioned marker, the 5 × 5
matrix admitting a process state, the retained secondary all-item sensitivity, the technology
examples — is superseded and is not current design. Where §29.1 later repaired the same area, §29.1
and the numbered sections govern.

    N1–N8: 8 / 8 MECHANICALLY ACCOUNTED
    MECHANICAL 8 / 8 != LEAD DIFFERENTIAL PASS
    LEAD DIFFERENTIAL PASS != INDEPENDENT REVIEW B PASS
    INDEPENDENT REVIEW B PASS != OWNER EXACT-SHA ACCEPTANCE
    THE N1–N8 REPAIR CREATES NO GOVERNANCE DISCHARGE: the 17-item and R1–R17 counters remain
      CONSUMED 0 / 17 · DISCHARGED 0 / 17 · CLOSED 0 / 17

| Defect | Basis | Exact defect | Repair | Sections | Transitive effects | Residual limitation | Status |
|---|---|---|---|---|---|---|---|
| **N1** allocation concealment | Lead execution instruction §6 (Owner-authorized repair scope) | The randomized two-group C3 realisation froze an ID→arm table but no concealment procedure: nothing prevented a recruiter or operator from learning a candidate's future arm before commitment, or from skipping / reordering placements after allocation became knowable | Allocation-concealment procedure E1–E5 with role separation: eligibility, consent and commitment complete and recorded before any participant ID exists; the custodian alone issues the next ID in strict ascending order; the recruiter has no access to the issuance log, the issued count or any ID; arm is never named; skip, hold-back, re-issue and reorder prohibited; every deviation logged and surfaced for governed review; enrolment shortfall handled without re-mapping | §6.1A, §9, §13.2 items 30 / 32, §20.2, §21.2 | consent gate moved before enrolment (§13.2 item 32); custodian gains the issuance duty (§21.2); STOP conditions extended; decision map gains D-CONSENT | The allocation table is public, so a participant's arm is inferable once their ID is known — i.e. after commitment; concealment covers only the pre-commitment window, which is the manipulable one. C3 construct unchanged | MECHANICALLY ACCOUNTED — awaiting Lead differential review |
| **N2** reference basis / context estimands | Lead execution instruction §7 | The prior candidate differenced FS and FI across arms whose reference sets were arm-specific and therefore not comparable, and conflated the decision-propensity effect of showing context with an error effect | Per-arm operational rates against that arm's own reference (FS_A / FI_A vs Ref_A, FS_B / FI_B vs Ref_B); common comparative strata C_I and C_S frozen, with Δ_FS_COMMON and Δ_FI_COMMON defined only on them; the decision-propensity effect Δ_S preserved separately on the common adjudicable corpus A_C and expressly not an error effect; differencing over arm-specific sets prohibited; mandatory 5 × 5 reference transition matrix (M-19) reporting every A×B transition, including every transition through REFERENCE-INDETERMINATE and OUT_OF_SCOPE, with item lists | §8.3, §14.1, §14.2 M-01 / M-02 / M-04 / M-11 / M-16 / M-19, §15.3 PS-2, §16 IND-5 / IND-10 | PS-2 estimands and shared-item multiplier follow the strata; IND-5 restated on Δ_FS_COMMON; IND-10 added for direction-reversing transitions; strata sizes reported before measured collection | C_I / C_S can be materially smaller than S_P, reducing comparative power; that erosion is reported (IND-11), never repaired by pooling | MECHANICALLY ACCOUNTED — awaiting Lead differential review |
| **N3** reference label semantics | Lead execution instruction §8 | CANNOT_ADJUDICATE was allowed to absorb substantive policy ambiguity while REFERENCE-INDETERMINATE covered the same ground, leaving two labels valid for one situation | Mutually exclusive meanings frozen: REFERENCE-INDETERMINATE = intrinsic item / policy ambiguity (`RC-RI-01`); CANNOT_ADJUDICATE = extrinsic adjudicator / process abstention only (recusal, conflict, prior prohibited exposure, broken presentation, process failure); the measured lane, which has no REFERENCE-INDETERMINATE, records intrinsic ambiguity as the separately coded CA-INTRINSIC sub-class (`RC-CA-02`) that never enters reference truth | §3.3 P-5 / P-5M / P-5R, §4A, §5, §8.3, §12.1 / §12.3, §13.1, §14.2 M-05 / M-18 | reason-code table split by lane; capture gains `abstention_class`; M-05 reports both sub-classes; M-18 uses CA-INTRINSIC; packets reworded | The measured CA-INTRINSIC sub-class is a Creator interpretation of how a four-label lane should record intrinsic ambiguity without forcing a guess; it is flagged for Lead review and is never mapped into reference truth | MECHANICALLY ACCOUNTED — awaiting Lead differential review |
| **N4** exact load-bearing order | Lead execution instruction §9 | Reference first-pass order, third-adjudicator order and the recognition-list order were left to "seeded order fixed at packet issue" — outcome-relevant order defined outside the frozen subject | Exact frozen tables: 12.5-A reference first-pass order for each of the four first-pass adjudicators (57 positions each); 12.5-B third-adjudicator full ranking per arm (57 ranks each), the escalated subset presented in that ranking order with ranks preserved; 12.5-C recognition-list order for each of the 18 reviewers (19 items each). Measured item order remains Table 11.2-B. No order is generated later or by a described procedure | §12.5, §8.3, §10, §12.4, §13.2 items 7 / 24, §20.2, §21.4 | STOP condition added for any order departure; audit preservation extended to §12.5 | Escalation subsets are not known until the reference first pass completes; the ranking fixes their order in advance, which is the strongest form available without knowing the subset | MECHANICALLY ACCOUNTED — awaiting Lead differential review |
| **N5** selective cue removal | Lead execution instruction §10 | The surface displayed a completeness marker only for items under 25 characters — a claim-length-conditioned display cue that could shift substantive judgments on exactly the shortest items | Every length-conditioned cue removed. Identical chrome for every item; no marker, badge, note or placeholder; the same content-integrity check applied identically to every item, silent on success; only a real rendering / loading / integrity failure produces the neutral error state, which routes to E-PRESENTATION-DEFECT → CANNOT_ADJUDICATE / `RC-CA-04` and never alters substantive claim semantics | §4A, §13.2 items 4 / 19, §12.1, §12.2, §12.3 | packets reworded in both lanes; §4A table rewritten; STOP condition added for any length-conditioned behaviour | Without a marker, a genuinely near-empty answer and a blank render are distinguished only by the surface's own integrity check and the reviewer's `RC-CA-04` option; the corpus contains no literally empty item, and CL-05 / CL-08 exercise the near-empty case | MECHANICALLY ACCOUNTED — awaiting Lead differential review |
| **N6** Owner consent / withdrawal policy | Lead execution instruction §11 — **OWNER POLICY AUTHORITY** | The prior candidate carried a Creator-proposed privacy paragraph, including a Creator-chosen retention period, in place of the Owner's consent / withdrawal policy, and had no pre-frozen rule for withdrawal at each timing phase | The Owner policy is embedded materially and accurately as §21.2 and marked Owner authority: consent precedes participation with the full disclosure list; withdrawal stops future participation; already-collected pseudonymous data is governed by pre-frozen consent / privacy terms plus applicable requirements, with neither automatic universal deletion nor automatic universal retention; the three timing phases (before reference freeze, after reference freeze but before measured collection, after measured collection with Cases A and B) frozen verbatim in effect; the binding no-post-hoc rule after outcome visibility; custodian custody duties and the not-by-default exclusions; STOP on material legal / institutional conflict | §21.1 – §21.4, §9, §12.1 / §12.2 / §12.3, §13.2 item 32, §20.2, §22 (D-CONSENT) | the Creator's 90-day figure is withdrawn as an operative term; consent summary rewritten in the packets; decision map gains D-CONSENT; STOP condition added for an undetermined withdrawal consequence | The operative consent / privacy terms are not set here and must be frozen in the consent instrument before recruitment; this protocol states their required shape only | MECHANICALLY ACCOUNTED — Owner policy embedded, not Creator-proposed |
| **N7** final statistical method | Lead execution instruction §12 | The prior PS chain used case-resampling with structural dropping (including for H2, where dropping changes the estimand), Clopper–Pearson "exact" bounds, and Henderson III as the variance fallback | PS-1 / PS-2: positive-weight two-way multiplier bootstrap, reviewer and item weights ~ Exp(1), observation weight their product, no structural dropping, B = 10,000, pre-frozen seed 20260906, percentile interval classified as a 95% PILOT UNCERTAINTY INTERVAL with no exact-coverage claim; fallbacks are raw counts plus leave-one-reviewer / leave-one-item influence ranges, never a nominal interval, with `ZERO EVENTS != ZERO RISK`. PS-2 shares the item multiplier across arms within a replicate and draws reviewer multipliers independently in the disjoint groups, applied to the N2 estimands. PS-3: crossed logistic GLMM with the exact linear predictor and arm coding, governing fallback a Bayesian crossed logistic model with the exact priors, ≥ 4 chains and the R-hat / ESS / divergence diagnostics; on diagnostic failure PS-3 is NOT ESTIMABLE with no third fallback. PS-5: empirical final-outcome proportions under the frozen roles with a delete-one-reviewer sensitivity envelope, resample-dropping prohibited, not-estimable thresholds stated. PS-4 / PS-6 realigned to the same positive-weight scheme. Clopper–Pearson and Henderson III removed from the governing chain; the VIF product removed from every role | §15 (all subsections), §14.2 (procedure references) | every metric's uncertainty reference updated; §15.9 reporting rules; ledger rows L4 / R5 / R14 restated | Pilot-scale precision remains limited; multiplier-bootstrap intervals are asymptotic in both cluster dimensions and are labelled pilot uncertainty intervals, not exact coverage | MECHANICALLY ACCOUNTED — awaiting Lead differential review |
| **N8** study surface | Lead execution instruction §13 | The prior candidate asserted `NEW EXECUTABLE SURFACE REQUIRED: YES` on the strength of not having found a surface, and elsewhere implied the pilot needed no executable realisation | Truthful status frozen: `EXISTING CONFORMANT STUDY SURFACE: NOT PROVEN` (absence of proof, not proof of absence) and `NEW EXECUTABLE STUDY SURFACE REQUIRED: NOT YET PROVEN REQUIRED`; the two admissible later routes (identify an authorized surface and prove conformance invariant-by-invariant, or return for separate Owner executable-surface authorization); the material three-line statement that the specification is self-contained while the eventual pilot requires an exact, conformant, authorized surface; the "no executable is required" formulations removed; Independent Review B is not final pre-execution assurance until the surface subject exists and has been reviewed | §11.4, §13.2, §13.3, §23, §22 (D-SURFACE), §25 | decision map D-SURFACE restated; §11.1 seed note qualified; Review B fence restated | Whether any authorized surface can conform is unknown and unexamined; no search outside this repository was performed or authorized | MECHANICALLY ACCOUNTED — awaiting Lead differential review |


### §29.1 Residual-repair crosswalk (Lead differential re-review of `efdfad9f…`; Owner-authorized residual set)

**HISTORICAL / SUPERSEDED / NON-GOVERNING where it quotes earlier design text**, on the same terms
as §29: its defect column quotes wording that has been removed, and the numbered sections govern.

    RESIDUAL SET N1 / N2 / N3 / N5 / N6 / N7 / N8: 7 / 7 ACCOUNTED
    N4: PASS — PRESERVED EXACTLY (Tables 12.5-A / 12.5-B / 12.5-C unchanged and not regenerated)
    MECHANICAL 7 / 7 != LEAD DIFFERENTIAL PASS
    LEAD DIFFERENTIAL PASS != INDEPENDENT REVIEW B PASS
    INDEPENDENT REVIEW B PASS != LEAD FINAL ADJUDICATION != OWNER EXACT-SHA DECISION
    THIS REPAIR CREATES NO GOVERNANCE DISCHARGE: CONSUMED 0 / 17 · DISCHARGED 0 / 17 · CLOSED 0 / 17

| Item | Residual defect in `efdfad9f…` | Repair | Sections | Transitive effects | Residual limitation | Status |
|---|---|---|---|---|---|---|
| **N1** | Concealment rested on ascending ID issuance plus an instruction that the recruiter not consult a publicly readable MR-ID→arm table: enrolment count, MR numbering or table position could still reveal the next arm. Two roles were named as issuer (custodian in §6.1A, operator in §13.2 item 30). The commitment record was an "irrevocable undertaking to complete the session", conflicting with the Owner N6 withdrawal right | The custodian draws the participant ID **at random without replacement** from the unissued pool at the moment of issuance, after E1–E3, by a documented physical or sealed draw recorded in the enrolment log; enrolment count, position, MR numbering and table row position therefore carry no allocation information, and no ordered schedule exists to read ahead in. ID ISSUANCE AUTHORITY is one rule: the custodian is the sole issuer; the operator issues nothing and only activates a session for an already-issued ID. The commitment record is restated as a timestamped record of agreement to take part now, expressly not a waiver of and not a limit on the §21.2 withdrawal right | §6.1A, §6.1 (table note), §13.2 item 30, §20.2, §21.2 | pair-blocked balance replaced by draw-exhaustion balance; achieved arm counts reported under shortfall (§15.10); allocation-table note added; residual-confound list extended | After the draw a participant's own ID, hence arm, is determinable from the public table by anyone who learns that ID; balance is guaranteed only at full enrolment | REPAIRED — awaiting Lead differential review |
| **N2** | Preserved from the prior candidate (arm-specific Ref_A / Ref_B, C_I / C_S, transition matrix) but the matrix admitted process states, so comparative strata could rest on non-outcomes | Ref_A / Ref_B, C_I / C_S and the mandatory transition matrix preserved; the matrix now contains only actual reference outcomes (4 × 4 over S · I · RI · OOS), items carrying RU are excluded from it and from C_I / C_S / A_C, and matrix cells plus the process-disposition register reconcile to the full item count | §8.3, §14.1, §14.2 M-19, §15.3 | stratum-exclusion reporting extended to name RU; A_C definition qualified | Common strata may shrink further when RU items exist; the erosion is reported (IND-11), never pooled away | REPAIRED — awaiting Lead differential review |
| **N3** | A third-adjudicator extrinsic CANNOT_ADJUDICATE, and a three-way no-concurrence, were both converted into REFERENCE-INDETERMINATE — process failure masquerading as intrinsic ambiguity | Explicit separate disposition `RU = REFERENCE OUTCOME UNAVAILABLE — UNRESOLVED PROCESS`, non-truth metadata with sub-codes THIRD-ADJUDICATOR-ABSTENTION · NO-CONCURRENCE · INSUFFICIENT-PANEL; no fifth truth category is created; REFERENCE-INDETERMINATE is an outcome only when two humans concur that the item is materially arguable; RU never enters a reference, matrix, stratum or denominator and is reported as a study-integrity figure | §8.3, §14.1, §14.2 M-14 / M-19 | reference freeze now hashes the register with the outcomes; M-14 extended; exclusion lists extended | A high RU rate would leave the pilot with fewer comparable items; that is surfaced for Lead review rather than absorbed into the data | REPAIRED — awaiting Lead differential review |
| **N5** | The marker line was removed from the surface but an accessibility invariant still required preserving it — a live dependency on a deleted element | Accessibility invariant restated as preserving displayed content generally, with an explicit prohibition on any element conditioned on claim length or content; no live reference to a marker line remains anywhere in the protocol | §13.2 item 29 | none beyond the invariant | Near-empty answers and blank renders are distinguished only by the uniform integrity check and the reviewer's `RC-CA-04` option | REPAIRED — awaiting Lead differential review |
| **N6** | The consent summary and §21.1 / §21.4 stated that pseudonymous evidence is retained as governance evidence — a universal-retention claim the Owner policy does not make; and the N1 commitment wording conflicted with the withdrawal right | Every universal-retention statement replaced by the Owner rule: no automatic universal retention, no automatic universal retroactive deletion, disposition set by the pre-frozen consent / privacy terms plus applicable governing requirements; the participant-facing summary states the same rule in the same terms; the N1 commitment wording no longer touches withdrawal; the post-outcome no-post-hoc rule is preserved unchanged | §12.1 (carried into §12.2 / §12.3), §21.1, §21.4, §6.1A | evidence-retention paragraph made subordinate to §21.2 | The operative retention and deletion terms are still to be frozen in the consent instrument before recruitment (D-CONSENT) | REPAIRED — awaiting Lead differential review |
| **N7** | The primary methods were closed, but the retained secondary S_P ∪ S_S all-item error analysis promised MP-group dependence while PS-1 assigned independent item multipliers — a promise the method did not keep | Option A taken: the secondary all-item error analysis is REMOVED. No error rate, primary or secondary, is computed over any set containing a sibling; every PS-1 set is a subset of S_P, so each item is its own item-dimension unit; siblings enter only the construct axis, which computes no error rate. PS-1 / PS-2 / PS-3 / PS-5 and the closed statistical basis are otherwise untouched | §14.1, §14.2 M-01, §15.2 | PS-1 section title and application note updated; no other procedure changed | The paraphrase / minimal-pair sets now inform construct validity only, with no error-rate reading at all | REPAIRED — awaiting Lead differential review |
| **N8** | The header still claimed the document "requires none [no executable artifact] for the pilot it specifies to be reproducible", and Route 2 preselected implementation routes (application / paper / PDF) | Header restated: the specification is self-contained, and pilot execution requires an exactly identified, authorized, conformant study surface whose existence and nature are not settled here. Route 2 preselects, prefers and excludes no realisation route or technology. Evidence state preserved: `EXISTING CONFORMANT STUDY SURFACE: NOT PROVEN` · `NEW EXECUTABLE STUDY SURFACE REQUIRED: NOT YET PROVEN REQUIRED`; Route 1 (identify and prove conformance invariant-by-invariant) unchanged | header, §11.4, §13.3, §23 | none beyond the wording | Whether any authorized surface can conform remains unknown and unexamined; no search outside this repository was performed or authorized | REPAIRED — awaiting Lead differential review |

### §29.2 Pre-freeze reconciliation crosswalk (RZ-1 … RZ-7) `[current — governing]`

    RZ-1 … RZ-7: 7 / 7 ACCOUNTED
    THIS RECONCILIATION CREATES NO GOVERNANCE DISCHARGE: CONSUMED 0 / 17 · DISCHARGED 0 / 17 ·
      CLOSED 0 / 17
    MECHANICAL 7 / 7 != LEAD PRE-FREEZE SUBSTANTIVE PASS

| Item | Requirement | What the draft now says | Sections |
|---|---|---|---|
| RZ-1 | one allocation model on every live surface: participant→ID random without replacement after commitment, custodian-only issuance, no sequential or pair-blocked enrolment, commitment ≠ waiver of withdrawal | §6.1 ARM ASSIGNMENT RULE restated with `SEQUENTIAL ENROLMENT-ID ASSIGNMENT: NO · PAIR-BLOCKED ENROLMENT: NO`; Table 11.2-A retitled as the frozen ID→arm mapping and expressly not an enrolment schedule; §11.4 provenance restated; §6.1A deviation list and the §20.2 STOP condition restated in draw terms; commitment defined as the timestamped moment of joining, expressly not a waiver or limit of the §21.2 withdrawal right | §6.1, §6.1A, §11.2-A caption, §11.4, §20.2 |
| RZ-2 | only Δ_S over A_C, Δ_FS_COMMON over C_I, Δ_FI_COMMON over C_S on live surfaces; per-arm FS / FI keep arm-specific references | §6.1 estimand block replaced by the exact three (plus the companion Δ_ABST_COMMON over A_C) with an explicit statement that no generic Δ_FS / Δ_FI, no Δ over all 57 items and no arm difference over an arm-specific set exists; §14 and §15.3 already carried the exact forms | §6.1, §14.1, §14.2 M-11, §15.3 |
| RZ-3 | RU never a truth cell; exact reconciliation identities; RU arm-entry count reported separately | M-19 carries the two verbatim identities (57 and 45, each = matrix-cell sum + unique RU item count), reports RU ARM-ENTRY COUNT separately, and expressly prohibits the claim "matrix cells + RU arm entries = 57"; the matrix stays 4 × 4 over actual outcomes | §14.2 M-19, §8.3 |
| RZ-4 | exact deterministic reference-freeze artifact and identity | new §8.3A: one record per (arm, claim_id), 114 records, five fixed fields with fixed enum spellings, canonical order (arm A then B, then CL-01 … CL-57), byte-exact UTF-8 serialization with `\|` separators, LF terminators and a stated final-newline rule, SHA-256 over those exact bytes; raw capture-set hashes declared distinct identities; reproducibility of Ref_A / Ref_B / RU / C_I / C_S / A_C / matrix required from the artifact alone | §8.3 step 6, §8.3A, §13.1, §21.4 |
| RZ-5 | no blanket retention; achieved denominators computed after the disposition rules | §15.10 restated in the required terms (`COMPLETED RATINGS ARE INCLUDED IN THE GOVERNING DATA SET ONLY TO THE EXTENT THEY REMAIN PERMITTED …`), denominators computed from the governing data set after disposition; the reference packet now carries the same truth as the reviewer packet; §21.1 / §21.4 already carried the Owner rule | §15.10, §12.3, §21.1, §21.2, §21.4 |
| RZ-6 | current design-disposition and coverage surfaces must not retain a secondary all-item error sensitivity | Ledger A ADM-4 and Ledger B R10 restated: siblings appear only on the construct axis with no error-rate analysis including them; §14.1 already states the removal; §29 / §29.1 rows marked historical | §26 ADM-4, §27 R10, §14.1 |
| RZ-7 | technology-neutral surface rule | §13.2 preamble restated as `ANY LATER AUTHORIZED STUDY-SURFACE REALIZATION MUST CONFORM TO EVERY FROZEN OUTCOME-RELEVANT INVARIANT`, naming no technology; §13.3 Route 2 already neutral; the remaining technology words appear only in historical crosswalk text | §13.2, §13.3 |

---

### §29.3 Pre-freeze consolidated repair crosswalk (PF-01 … PF-04 + D-NEW-C) `[current — governing]`

**The "Defect" column quotes wording that has been REMOVED from this draft; those quotations are
HISTORICAL / SUPERSEDED / NON-GOVERNING and state no current design.** The "Repair" column and the
numbered sections state current design.

    PF-01 · PF-01-b · PF-02 · PF-03: REPAIRED IN THIS DRAFT
    PF-04: OWNER-CLOSED — resolved by `OWNER FINAL DECISION — D-OPEN-ΔS / PF-04 POLICY CLOSURE`
      (Option A + CA-E1) and implemented in this draft; UNRESOLVED LOAD-BEARING PF-04 CHOICES: 0 ·
      OPEN OWNER DECISIONS REQUIRED FOR THIS BOUNDED REPAIR: 0
    PF-04 POLICY CHOICE CLOSED != CLEAN PRE-FREEZE GATE PASS — the overall pre-freeze gate still
      requires Lead differential review of this repair
    D-NEW-C: OWNER-FINAL — INCORPORATED (§18 item 3)
    THIS REPAIR CREATES NO GOVERNANCE DISCHARGE: CONSUMED 0 / 17 · DISCHARGED 0 / 17 · CLOSED 0 / 17
    CREATOR REPAIR EVIDENCE != LEAD DIFFERENTIAL PRE-FREEZE PASS != CLEAN PRE-FREEZE GATE

| Item | Defect | Repair in this draft | Sections | Residual |
|---|---|---|---|---|
| **PF-01** | live surfaces described the artifact as already frozen / an immutable commit / a fresh same-base sibling while other surfaces said `PRE-FREEZE DRAFT != FROZEN CANDIDATE`; the pre-freeze ordering was not represented | header restated as `PRE-FREEZE DRAFT — MUTABLE WORKING ARTIFACT` with explicit NO flags for freeze, commit, branch, exact-SHA identity, Lead reviews, clean gate, freeze authority and Review B; provenance restated (no commit / tree / blob identity); lineage restated as three HISTORICAL frozen candidates including `52ab9fdd…`; §0 entry 3 restated with the full lifecycle; §23 Review B fence bound to post-freeze position; §30 rewritten with the pre-freeze and post-freeze sequences, `PRE-FREEZE PASS != OWNER FREEZE AUTHORIZATION` and the exact-SHA ≠ publication distinction; §22 D5 / D-POLICY rows restated | header, §0, §7.7, §22, §23, §30 | historical descriptions of earlier frozen candidates remain, marked HISTORICAL / NON-GOVERNING |
| **PF-02** | RU sub-code was precedence-dependent: the old 4c (no label held by two) shadowed 4d (both first-pass adjudicators abstained), so `CA, CA, SUFFICIENT` could terminate as NO-CONCURRENCE or INSUFFICIENT-PANEL | the rule now branches first on `k` = number of non-abstaining first-pass verdicts (2 / 1 / 0), partitioning the state space; within each branch the sub-cases are mutually exclusive; INSUFFICIENT-PANEL ⇔ k = 0, THIRD-ADJUDICATOR-ABSTENTION ⇔ k ≥ 1 ∧ v3 abstains, NO-CONCURRENCE ⇔ k ≥ 1 ∧ v3 substantive ∧ matches nothing; a reference outcome always requires two humans to concur | §8.3, §8.3A | none identified; the six boundary cases resolve uniquely (determinism table in the Creator return) |
| **PF-03** | operating text mapped a disclosed tool-restriction breach and outside-study recognition to `RC-CA-03` (conflict / recusal), contradicting the frozen vocabulary | outside-study recognition → `RC-CA-01` (prior prohibited exposure); disclosed tool / process breach → `RC-CA-04` with `presentation_status = OK`, distinguished from a surface defect by that field rather than by a second code; §5 entry for `RC-CA-04` restated; exclusivity rule added (`RC-CA-02` never combines with an extrinsic code, extrinsic governs, so `abstention_class` is unambiguous); §4A note that participant / process events are not item events; both packets reworded; M-05 and IND-9 report `RC-CA-04` split by `presentation_status` | §4A, §5, §9, §10, §12.1, §12.2, §12.3, §13.1, §14.2 M-05, §16 IND-9 | none identified; the canonical mapping is reproduced in the Creator return |
| **PF-04** | the Δ_S denominator was not fixed at the estimand / estimator definition; two interpretations survive and estimate different quantities | RESOLVED BY OWNER DECISION, NOT BY THE CREATOR. `OWNER FINAL DECISION — D-OPEN-ΔS / PF-04 POLICY CLOSURE` selects **OPTION A**: the primary Δ_S is the MARGINAL EXACT-S / SUFFICIENT-ISSUANCE ESTIMAND with `p(i, arm)` = governing-eligible first-pass records labelled SUFFICIENT / all governing-eligible first-pass records for that item × arm, aggregated as the unweighted item-wise mean over the unchanged A_C; governing eligibility is determined before the exact-S indicator is evaluated `[D1]`; no raw or canonical label is recoded `[D5]`; a zero governing-eligible denominator makes the primary estimator NOT ESTIMABLE AS SPECIFIED, without item dropping, imputation, A_C redefinition or a substitute denominator `[D6]`; the CA-EXTRINSIC sub-choice is **CA-E1** — no new ascertainment / exposure-timing regime `[CA-E1]`; Option B is NOT SELECTED AS PRIMARY and carries no deferred, tracked or gate obligation `[D4]`; Δ_S is a marginal sufficient-issuance-propensity contrast and never an accuracy or error effect `[D2]`; Δ_FS_COMMON / Δ_FI_COMMON (committed-verdict denominators, CEHR metrics M-01 / M-02) and Δ_ABST_COMMON (all-ratings denominator, CEHR metric M-05) explicitly unaffected | §6.1, §14.1, §14.2 M-11, §15.3 PS-2, §22 | the Owner decision governs this mutable draft and is not a merged repository authority; PS-2's architecture, seed, replicate count and interval procedure are untouched; PF-04 closure is not a clean pre-freeze gate |
| **PF-01-b** | residual live surfaces still described the current mutable artifact itself as a candidate — `State at this candidate`, `NOT PART OF THIS CANDIDATE`, `repair in this candidate`, `closed by this candidate`, `only as candidate text`, `not started by this candidate`, `no such lines exist in this candidate`, `no draft packet exists in this candidate`, `this candidate's own status surface`, `governance-only protocol candidate` | every live current-artifact reference restated as `this pre-freeze draft` / `this draft`; no global replacement performed, so historical, future, configuration, implementation, evidence, person and `CANDIDATE POSITIVE` uses of the word are preserved unchanged | §22, §24, §26, §27, §30 | `LIVE CURRENT-ARTIFACT CANDIDATE MISLABELS: 0`; every remaining occurrence refers to another object or is marked HISTORICAL / NON-GOVERNING |
| **D-NEW-C** | anchors were carried as `Creator-proposed, not Owner-selected` / `OPEN — Owner selection required`, which is no longer true | the six anchors are recorded as OWNER-ACCEPTED under `D-NEW-C: ACCEPT AS PROPOSED WITH GOVERNING BOUNDARY CLARIFICATIONS`, MINIMUM MANDATORY, NON-EXHAUSTIVE, NON-SCORING and subordinate to the Claim-Sufficiency Policy, each with its Owner governing interpretation and the corpus families that exercise it; §22 row CLOSED — OWNER-FINAL; the open-items sentence and Ledger A ADM-2 updated | §18 item 3, §22, §26 ADM-2 | no seventh anchor and no new policy criterion introduced; anchors create no scoring rule, threshold, event value or owner |

---

## §30. Lifecycle state and non-authorization

**Current state of this artifact.**

    PRE-FREEZE DRAFT — MUTABLE WORKING ARTIFACT · NOT FROZEN · NOT A COMMIT · NOT A CANDIDATE ·
      NO EXACT-SHA IDENTITY · NOT OWNER-ACCEPTED · NOT INDEPENDENTLY REVIEWED ·
      NOT REPOSITORY-AUTHORITATIVE

**Governed pre-freeze lifecycle — the stage this draft is in.**

    PRE-FREEZE DRAFT
    → LEAD SUBSTANTIVE REVIEW
    → CONSOLIDATED REPAIR IF REQUIRED
    → LEAD DIFFERENTIAL PRE-FREEZE RE-REVIEW
    → CLEAN PRE-FREEZE GATE
    → OWNER FREEZE ADJUDICATION / APPLICABLE FREEZE AUTHORITY
    → ONLY THEN IMMUTABLE FREEZE

    PRE-FREEZE PASS != OWNER FREEZE AUTHORIZATION
    A clean Lead differential pre-freeze review does NOT itself authorize immutable freeze.

**Governed post-freeze lifecycle — none of it reached.**

    IMMUTABLE FREEZE
    → LEAD POST-FREEZE IDENTITY / DIFFERENTIAL REVIEW
    → INDEPENDENT REVIEW B
    → LEAD FINAL ADJUDICATION
    → OWNER EXACT-SHA DECISION
    → SEPARATE PUBLICATION AUTHORIZATION
    → PR / MERGE ONLY IF SEPARATELY AUTHORIZED
    → POST-MERGE IDENTITY VERIFICATION

Independent Review B never runs on a mutable pre-freeze draft. An Owner exact-SHA decision would
freeze the **protocol and policy text** of the accepted candidate — not pilot execution, not
recruitment, not custodian appointment, not surface implementation, not reference adjudication, not
human collection, not the main study, not Claim-Eligibility implementation, not schema work, and not
any run — each of which requires its own separate Owner authorization; and Owner exact-SHA
acceptance does not itself authorize a PR or a merge unless applicable authority separately says so.

    CREATOR REPAIR EVIDENCE != LEAD DIFFERENTIAL PASS
    MECHANICAL 9 / 9 (M-set) != LEAD SUBSTANTIVE PASS
    MECHANICAL 8 / 8 (N-set) != LEAD DIFFERENTIAL PASS
    MECHANICAL 7 / 7 (RESIDUAL SET) != LEAD DIFFERENTIAL PASS
    MECHANICAL 7 / 7 (RZ SET) != LEAD PRE-FREEZE SUBSTANTIVE PASS
    PRE-FREEZE DRAFT != FROZEN CANDIDATE
    INDEPENDENT REVIEW B PASS != LEAD FINAL ADJUDICATION
    LEAD FINAL ADJUDICATION != OWNER EXACT-SHA DECISION
    LEAD DIFFERENTIAL PASS != INDEPENDENT REVIEW B PASS
    INDEPENDENT REVIEW B PASS != OWNER EXACT-SHA ACCEPTANCE
    OWNER EXACT-SHA ACCEPTANCE != PUBLICATION AUTHORIZATION
    PUBLICATION AUTHORIZATION != MERGE AUTHORIZATION
    PROTOCOL FREEZE != PILOT AUTHORIZATION
    MERGE != COMPLETE UNTIL POST-MERGE IDENTITY VERIFICATION

This draft does not declare and must not be read as declaring: FROZEN · IMMUTABLE · A COMMIT · AN
EXACT-SHA CANDIDATE · PRE-FREEZE GATE CLEAN · PROTOCOL ACCEPTED · PROTOCOL AUTHORITATIVE · REPAIR
SUBSTANTIVELY ACCEPTED · PILOT READY · HUMAN_NOW VALIDATED · CEHR BACKLOG
DISCHARGED · CEHR BACKLOG CLOSED · STUDY SURFACE APPROVED · SURFACE REQUIREMENT SETTLED ·
IMPLEMENTATION READY.

**Lean classification.** `LEAN RISK LEVEL: 2` · `REVIEW DEPTH: 2` — governance-only protocol
pre-freeze draft, zero executable delta, one new file, no existing file changed.
