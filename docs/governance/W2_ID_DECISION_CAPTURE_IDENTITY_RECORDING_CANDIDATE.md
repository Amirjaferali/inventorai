# W2-ID — Decision-Capture Identity / Recording Mini-Gate — CANDIDATE (v3, post Owner architecture decision)

STATUS: `W2-ID GOVERNANCE / ARCHITECTURE CANDIDATE — NOT AUTHORITATIVE UNTIL
INDEPENDENTLY SPOT-CHECKED, OWNER-ACCEPTED AT EXACT SHA, MERGED, AND POST-MERGE
VERIFIED. RVR-4 / W2-A IMPLEMENTATION NOT AUTHORIZED. ZERO PRODUCT/TEST/RUNTIME
CODE DELTA.`

Fresh sibling from the authoritative base after the Owner's narrow repair
instruction. Prior reviewed candidates preserved unamended:
`refs/reviewed/w2id-f2cfe745` (v1) and `refs/reviewed/w2id-v2-538d57fa` (v2) —
neither is accepted; this v3 supersedes both in full. Evidence tags: `[REPO]`,
`[EXEC]`, `[OWNER]`, `[HYPOTHESIS]`, `[OPEN]`.

---

## A. Authority verification

Re-verified at candidate time: tip `91475e456cbe8ff21bfa8e7bf2fb3e6dd801f762`
(Merge PR #564, parents `58e92e09…` + `528b4519…`, tree `ed3f8685…`, 0 commits
after) `[EXEC]`. Base unchanged since v1/v2; supersession: NONE.

## B. Owner architecture decision — `OD-W2ID-LEDGER — APPROVED` `[OWNER]`

The Owner has DECIDED the carrier architecture (this resolves what the
Independent External Review found could not remain deferred beyond W2-ID):

> The existing `AssertionRecord` ledger is approved as the bounded
> decision-capture carrier architecture, while FDC-001 `DecisionRecord`
> remains the sole canonical owner of decision semantics. Implementation
> remains deferred to W2-A.

Effect, recorded precisely:

- the existing `AssertionRecord` ledger is the **approved bounded durable
  carrier** for decision-capture owner actions;
- FDC-001 `DecisionRecord` **remains the sole canonical decision-semantics
  owner**;
- `AssertionRecord` remains a **carrier / provenance / history** object and
  is NEVER presented as the decision itself;
- implementation — including any disposition-value or field change — is
  **separately authorized only in W2-A**.

**`ARCHITECTURE DECIDED NOW`** ≠ **`IMPLEMENTATION AUTHORIZATION DEFERRED TO
W2-A`**. The ledger-carrier architecture is NOT undecided and NOT deferred;
only its enactment is. (v2's `LEDGER CARRIER: OWNER DECISION REQUIRED` /
"OD-W2A-LEDGER may be deferred" framing is SUPERSEDED by this decision.)

## C. Carrier semantic boundary — approved bounded extension, not false reuse

This is an **Owner-approved bounded semantic extension** of the ledger's
domain: the future RVR-4/W2-A implementation may introduce bounded
decision-scoped owner-action records for purposes such as declaring a
decision context/subject; declaring an alternative; explicit attachment to
an existing decision context; and governed refinement/withdrawal operations.
W2-ID implements NONE of this. The carrier choice is an **Owner-selected
architecture**, grounded in: existing durable provenance; correction/
supersession lineage; deterministic, never-renumbered record identities
(`idea_state.py:366-370` `[REPO]`); avoidance of duplicate canonical
decision semantics; and minimal architectural duplication. It is
deliberately NOT justified as "the only legally possible carrier" (§H).

**Context attachment (Owner-approved architecture):** an alternative
attaches to its decision context by an **explicit, durable, deterministic
reference to the context's founding-chain ROOT**. Attachment must NOT be
carried by overloading `gap_context`, `question_id`, `content`, localized
text, sequence/index, or implicit inference. The exact field name/encoding
is a W2-A implementation-contract item; if a new optional field is needed to
represent the reference truthfully, **W2-A proposes that exact bounded
schema extension for Owner authorization** — nothing is pre-authorized here.

**Disposition vocabulary:** the decision-action class is approved as
architecture; exact runtime values are frozen in the W2-A contract. The
working concepts *decision context declared* and *decision alternative
declared* — and any concrete strings derived from them — are
`PROPOSED FOR W2-A FREEZE`, not authorized runtime vocabulary.

## D. Identity model (preserved from v2, unchanged)

- **Contexts are user-created and plural** (zero/one/many per project); one
  `DecisionRecord` = one bounded decision ("ONE bounded technical decision"
  scopes the RECORD — the DW lane mints per GET, `app.py:3285-3287`
  `[REPO]`); no default context is ever invented (FL-4); membership is
  explicit attachment (ID-9).
- **Context identity:** `decision-pn-<idea_id>-<context_root_record_id>`.
- **Candidate identity:** root-based (`cand-pn-<root>`), context-qualified.
- **Refinement within a declaration chain preserves identity; withdraw +
  redeclare creates a new root → new identity.** Roots are never reused; no
  ordinal anchors (the withdrawn `"d1"` class stays withdrawn); no
  placeholders; no localized-text identity; no replay-position identity.
- **`idea_id`:** the v2 ten-point lifecycle proof stands `[REPO][EXEC]`
  (uuid4 minted once at `/start`, contract-persisted, restored verbatim
  across resume/correction/replay, no canonical-hash participation). Its
  precise role: **`stable project qualification input`** — NOT a decision
  semantics owner and NOT claimed as canonical-hash authority.

## E. Full derived-projection determinism contract (corrected per review)

Contract-level invariant, preserved:
`same amended ledger → byte-identical DecisionRecord.to_record_dict()`.
The existing export timestamp (`to_export_dict`'s
`export_metadata.generated_at`, decision_workspace.py:1128 `[REPO]`) is
explicitly OUTSIDE this invariant by FDC-001's own design.

**The RVR-4 contract MUST, at its freeze, enumerate EVERY serialized
identity/collection surface of `to_record_dict()` and classify each as
exactly one of `DETERMINISTICALLY DERIVED` or `EMPTY BY CONSTRUCTION`** —
at minimum: `decision_id`; Candidate ids; ClaimItem ids; Constraint ids;
Gap ids; Risk ids; EvidenceItem ids; GapAssessment ids; conflict ids and
conflict-derived serialization; ChangeEvent ids/`history`; `revision`;
`change_impact_summary`; and readiness/`blocking_reasons` derived output
wherever ordering can matter. Exact deterministic formulas are NOT invented
here — the RVR-4 contract freezes each exact formula before implementation,
and no random sub-object identity may survive RED test **ID-6** (two
compositions of the same amended ledger → byte-identical serialization).
Architectural defaults carried from v2: derived projections carry
`history == []` and `change_impact_summary == None` EMPTY BY CONSTRUCTION
(the durable ledger is the history); pn-prefixed root-derived ids for
declaration-sourced objects.

## F. Supersession constraint — single-target rule (new, per review finding)

The generic supersession primitive can supersede multiple records and could
therefore merge chains `[REPO — reviewer-verified]`. For decision-declaration
records this is FORBIDDEN. Binding future RVR-4 invariant:

> A decision-declaration refinement MAY supersede exactly ONE prior
> declaration record. Multi-target supersession for decision-declaration
> records is invalid and must fail closed.

This protects unique chain-root identity. Mandatory RED test:
**ID-11 — declaration-class multi-target supersession is refused; a
declaration chain always has one unambiguous root.**
The current generic supersession primitive is NOT modified now; the
restriction binds the future decision-declaration class under RVR-4.

## G. Derived-surface containment (new, per review finding)

Repository truth: new `AssertionRecord` dispositions can be mechanically
consumed by downstream derived surfaces (requirement landscape's
disposition-labeled synthesis; exported record disposition vocabulary)
`[REPO]`. Binding future RVR-4 rule:

> Decision-capture declaration/action records MUST NOT automatically become
> requirement-landscape requirements, gap answers, legacy deliverable
> claims, or any other semantic class merely because they inhabit the
> AssertionRecord ledger. Every downstream consumer either explicitly
> EXCLUDES the decision-action class or explicitly handles it as
> decision-action provenance under separately authorized semantics. No
> accidental fall-through into legacy assertion vocabulary.

Mandatory RED test: **OW-6 — decision-action dispositions do not silently
surface as requirement-landscape rows, gap-answer semantics, legacy
deliverable content, or mislabeled exported semantics.**
Raw-record export truth: if the existing P7 floor inherently exports record
dispositions, new values may appear ONLY truthfully as decision-action
disposition values — never relabeled as requirements or gap evidence; any
higher-level decision export remains separately governed / additive-deferred
under the existing P7-I1/P7-I3 posture. Nothing implemented now.

## H. FDC-001 persistence wording — corrected

v2 overstated the carrier justification. Corrected truth: FDC-001 is
**currently in-memory / non-durable under its current implemented
increment** (`decision_workspace.py:12-14`; `FDC001_DECISIONS = {}`
`[REPO]`) — an increment-scoped limitation, **NOT a permanent prohibition**
against future persistence; adding persistence would require its own
Owner-authorized governance/implementation. The carrier choice therefore
stands as the **Owner-selected architecture** (§B/§C rationale), not as the
only legally possible option. `FDC-001 PERSISTENCE PERMANENTLY PROHIBITED:
NO`.

## I. Elicitation-prompt ownership (preserved from v2)

The decision-capture elicitation is substantive, not display chrome: a
bounded **governed elicitation class under the decision owner** — no Path-N
question identity; no WS10 coverage; no progression/relevance semantics;
fixed/non-adaptive; Owner-reviewed wording at W2-A freeze; governed EN/AR
UI localization; no shadow Path-N architecture. Mandatory test **OW-5**
(prompts absent from every question-serving path) stands.
Capture remains explicit — a user may type a new subject/alternative or
explicitly CONFIRM an existing active statement as an alternative; no
silent inference/auto-promotion of ordinary answers (RVR-4 UX detail under
this settled architecture).

## J. Preserved boundaries (unchanged)

- **WS10:** question-intent owner only; no content/activation authorized;
  optional Stage-2 provenance enrichment only if its own RED tests pass;
  `HISTORICAL PROVENANCE PARTIAL` (Stage-3 questions have no governed
  identity `[EXEC]`); no backfill; no fabricated ids; no identity
  dependency.
- **AssertionRecord:** carrier/provenance/history — never the decision;
  schema unchanged by W2-ID; any field/disposition change is a W2-A-proposed,
  Owner-authorized item.
- **P7/export:** no new canonical output model, no export version change,
  floor intact (§G).
- **R4-C replay-order acceptance-lapse Owner decision:** OPEN, untouched;
  decision identity is designed from the FINAL amended active state, not
  replay position.
- **RVR-6 / W1-N3 / RVR-7 / RVR-8:** not started, not authorized, not
  modified.
- Prior RVR-4 RED-test contract stands: ID-1…ID-10, PV-1…PV-4, OW-1…OW-5,
  CP-1/2, FL-1…FL-4 — now plus **ID-11** and **OW-6**.

## K. Status-surface divergence — recorded, not rewritten

The Independent External Review observed that committed status surfaces
(`CURRENT_PROJECT_STATE.md`, `ACTIVE_EXECUTION_ROADMAP.md`,
`ACTIVE_INCREMENT_CONTRACT.md`) still carry `WAVE-2 … AUTHORIZED: NO`
lines, while PR #563 (Wave-2 contract) and PR #564 (W2-D implementation)
are merged and authoritative `[EXEC — divergence re-confirmed at this
base]`. Classification: **HISTORICAL/STALE STATUS TEXT — POST-ACCEPTANCE
GOVERNANCE SYNCHRONIZATION REQUIRED.** The merged repository facts govern;
stale status text does not override them. This narrow v3 candidate does NOT
rewrite those surfaces and does NOT retroactively invent an OD-W2-AUTH
record; a later synchronization candidate may reconcile the status surfaces
after W2-ID acceptance/merge per the repository's established sync-gate
workflow.

## L. Narrow Creator Re-Grill R1–R20

R1 PASS (§B records the Owner decision verbatim with its four effects) ·
R2 PASS (§B: architecture decided now vs enactment deferred — stated as a
contrast, twice) · R3 PASS (no "undecided/deferred architecture" statement
survives; v2's framing explicitly superseded) · R4 PASS (§H current-only
wording; permanent-prohibition claim withdrawn) · R5 PASS (§F single-target
invariant verbatim) · R6 PASS (ID-11 present, scoped to the declaration
class, root-uniqueness stated) · R7 PASS (§E enumeration requirement with
the full minimum list and freeze-time formula rule) · R8 PASS (ID-6
byte-identity gate; no random id may survive) · R9 PASS (§G prohibition
with the exclude-or-explicitly-handle rule) · R10 PASS (OW-6 present,
covering landscape/gap/deliverable/export mislabeling) · R11 PASS (§G raw
export: truthful disposition values only; higher-level export deferred) ·
R12 PASS (§B/§J: carrier, never the decision) · R13 PASS (§B/§D sole
canonical owner) · R14 PASS (§D chain-root + idea_id, roles precise) ·
R15 PASS (§D plurality, ID-9/FL-4) · R16 PASS (§D refine-vs-redeclare) ·
R17 PASS (§I + OW-5) · R18 PASS (one governance file; zero engine/web/
tests/schema/disposition/export/roadmap/WS10/runtime/persistence delta
`[EXEC]`) · R19 PASS (both reviewed SHAs preserved as refs, unamended) ·
R20 PASS (adversarial re-read: the Owner decision is recorded without
expanding it — no field pre-authorized, no vocabulary enacted, no
implementation begun; no contradiction with §D–§J introduced).
**NARROW CREATOR RE-GRILL: PASS.**

---

`NEXT STEP: FOUR-POINT INDEPENDENT SPOT-CHECK, THEN OWNER EXACT-SHA
ACCEPTANCE; W2-A/RVR-4 IMPLEMENTATION REMAINS SEPARATELY AUTHORIZED.`
