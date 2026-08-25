# W2-A / RVR-4 — Implementation Contract Candidate (Governance Freeze)

**Status:** CANDIDATE — awaiting Independent External Review and Owner
acceptance. This document AUTHORIZES NOTHING by itself. W2-A runtime
implementation is **NOT authorized** and **NOT started**. No runtime code,
schema, test, route, or UI was modified by the gate that created this file.

**Authoritative base:** `557548db2bb37b21b6b57f893afc2ae1af64744f`
(Merge PR #566; parents `516a184231f3e19fad6e8f6f3301b5b9c4ad9820` +
`3910e86c29e569680be8ac8c728acd6e94453ab6`; tree
`8f6af9a326dd7fc44af924d936075f3e0c53e7ce`) — verified from Git at creation.

**Classification legend used throughout:** `[REPO FACT]` = verified in the
authoritative tree at the base above; `[OWNER DECISION]` = an explicit Owner
directive recorded by this contract; `[PROPOSED CONTRACT]` = a contract term
proposed here for freeze; `[EXECUTED EVIDENCE]` = verified by execution.

---

## 1. Lineage and governing authority

- `docs/governance/WAVE_2_BOUNDED_IMPLEMENTATION_CONTRACT_CANDIDATE.md`
  (authoritative via PR #563): Wave-2 slice contract; §P item 3 records
  OD-W2-DW-LIFT (`:434-436`) `[REPO FACT]`.
- `docs/governance/W2_ID_DECISION_CAPTURE_IDENTITY_RECORDING_CANDIDATE.md`
  v3 (authoritative via PR #565): OD-W2ID-LEDGER (§B), carrier boundary and
  `PROPOSED FOR W2-A FREEZE` vocabulary (§C), identity model (§D),
  determinism contract (§E), ID-11 (§F/`:131`), OW-6 (`:151`) `[REPO FACT]`.
- `docs/governance/DEFERRED_OBLIGATIONS_REGISTER.md` (authoritative via
  PR #566): §2 Before-W2-A due-now set — the W2-A enactment set and
  OD-W2-DW-LIFT, both `CURRENT EXECUTION BLOCKER` (`:81`) `[REPO FACT]`.
- The W2-A read-only reconstruction completed
  `W2-A READ-ONLY GRILL: PASS` /
  `READY FOR W2-A OWNER AUTHORIZATION / CONTRACT-FREEZE WRITE GATE`.
  Its material propositions were **revalidated against the base tree**
  before this freeze, not copied `[EXECUTED EVIDENCE]`.
- Prior sibling `f4d0552317782066dc7704a569653ac35ee94efb` completed
  Independent External Review with `NARROW REPAIR REQUIRED` and is
  preserved as immutable reviewed evidence
  (`refs/reviewed/w2a-contract-f4d0552`). This candidate is a fresh
  sibling from the same base carrying ONLY the bounded review repairs:
  the corrected §10 OW-6 repository baseline, the §19 containment-point
  allowlist repair, the fail-closed mint-seam rule (§3), the frozen
  decision-action provenance rule (§2), and the added RED coverage
  (§20: SEAM / PROV / LANG). Every repair was independently reproduced
  from repository code before adoption `[EXECUTED EVIDENCE]`.

This contract is subordinate to the committed anchors, MVP_SCOPE_FREEZE,
GOVERNANCE_MODEL, CLAUDE.md, and `ACTIVE_EXECUTION_ROADMAP.md`. Recording
work here authorizes nothing downstream.

---

## 2. Frozen decision-action vocabulary — V2 `[OWNER DECISION]`

Exactly three new dispositions are frozen:

- `decision_context_declared`
- `decision_alternative_declared`
- `decision_alternative_withdrawn`

Rules:

- **Refinement is NOT a disposition.** Refinement is represented exclusively
  by the existing single-target supersession relation: a new
  declaration-class record superseding the current active head of its own
  chain. No separate refinement disposition exists; creating one requires a
  new Owner decision preceded by a STOP/contradiction escalation.
- No legacy disposition is overloaded. The legacy vocabulary
  `answered / unknown / deferred / provisional_assumption /
  specialist_requested / evidence_requested / risk_accepted`
  (`engine/idea_state.py:122-126` `[REPO FACT]`) is unchanged in meaning
  and membership semantics.
- The three values join `INTERACTION_DISPOSITIONS` at implementation;
  mint-time validation (`record_interaction`,
  `engine/idea_state.py:347` `[REPO FACT]`) continues to reject unknown
  actions.
- **Context withdrawal is OUT OF SCOPE for W2-A** (see anti-anchoring
  finding AA-1, §22). No workaround is permitted: a
  `decision_alternative_withdrawn` record MUST NOT target a
  `decision_context_declared` record (cross-class, fails closed per ID-11).

Chain semantics per class `[PROPOSED CONTRACT]`:

- `decision_context_declared` with `supersedes == []` **founds** a decision
  context; its `record_id` is the context's founding-chain root.
- `decision_context_declared` with `supersedes == [prior]` where prior is
  the active head of a context founding chain is a context refinement
  (root identity preserved). *No W2-A user route is required for this
  operation* (§14); the semantics are frozen so the model is closed.
- `decision_alternative_declared` with `supersedes == []` **founds** an
  alternative chain (its `record_id` is the alternative root); with
  `supersedes == [prior]` it refines the same alternative chain (root
  identity preserved).
- `decision_alternative_withdrawn` with `supersedes == [head]` withdraws
  the alternative whose active head it supersedes. Its optional free-text
  content is a user-stated reason only — never identity, never attachment.
- Redeclaration after withdrawal is a NEW founding
  `decision_alternative_declared` (no supersedes) → new root → new
  identity. Roots are never reused.

**Frozen decision-action provenance** `[PROPOSED CONTRACT]`
(review repair — no implementation discretion):

`[REPO FACT]` baseline: `record_interaction` derives default provenance
from the action via `_DEFAULT_PROVENANCE_BY_DISPOSITION.get(action,
LEGACY_UNSPECIFIED)` (`engine/idea_state.py:140-145,:350-351`).
Owner-asserting actions (`answered`, `provisional_assumption`,
`risk_accepted`) default to `OWNER_STATED`; unlisted actions fall back to
`LEGACY_UNSPECIFIED` — which would be semantically FALSE for explicit
W2-A decision actions.

Frozen rule: **all three decision-action dispositions are added to
`_DEFAULT_PROVENANCE_BY_DISPOSITION` with `OWNER_STATED`** — declaring a
context, declaring an alternative, and withdrawing an alternative are
each an owner assertion about the owner's own decision, the exact
semantics for which `OWNER_STATED` already exists (the `risk_accepted`
precedent, `idea_state.py:143-145` `[REPO FACT]`). Consequences follow
the existing unchanged rule: `responsibility = OWNER_INPUT` when
provenance is `OWNER_STATED` (`:356` `[REPO FACT]`). No new provenance
vocabulary, value, or owner is created; `LEGACY_UNSPECIFIED` is never
produced by a canonical decision-action mint; legacy defaults are
byte-unchanged. The carrier mint additionally REJECTS (fail closed, per
the §3 mint-seam rule) an explicit `provenance` argument other than
`OWNER_STATED` on any decision-action mint — the generic "an explicit
provenance argument always wins" override (`idea_state.py:135-136,
:349-351` `[REPO FACT]`) cannot be used to stamp a decision action as
legacy/unspecified or platform-derived. Legacy dispositions keep the
override byte-unchanged. RED coverage: `RVR4-PROV-1/2` (§20).

---

## 3. Frozen context-attachment field — `decision_context_root` `[OWNER DECISION]`

Exact field name: **`decision_context_root`**.

Semantics:

- Type: bounded optional string field on the AssertionRecord contract.
- `decision_context_declared` records: `decision_context_root = None` —
  **always**, including refinements within a founding chain (chain
  membership is derived from the supersession edge, never from this field;
  this satisfies "MUST NOT carry a non-null external context root" with a
  single deterministic rule — see AA-3, §22) `[PROPOSED CONTRACT]`.
- `decision_alternative_declared` records: MUST carry the exact
  founding-chain root `record_id` of the owning decision context.
- `decision_alternative_withdrawn` records: MUST carry the SAME exact
  `decision_context_root` as the alternative chain they withdraw.
- All non-decision records (all seven legacy dispositions):
  `decision_context_root = None`.
- Prohibited attachment mechanisms: `gap_context`; `question_id`; content
  encoding; positional/index attachment; inferred text matching;
  replay-position identity. (Per OD-W2ID-LEDGER and W2-ID v3 §C
  `[REPO FACT]`.)

Mint-time validation (fail closed, nothing appended)
`[PROPOSED CONTRACT]`:

- root does not exist → reject;
- root exists but is not the founding record of a
  `decision_context_declared` chain → reject;
- cross-context root on withdrawal (withdrawal's root ≠ target chain's
  root) → reject;
- non-null root on a `decision_context_declared` or legacy-disposition
  record → reject.

**Mint-seam enforcement — fail-closed direct mint** `[PROPOSED CONTRACT]`
(review repair — closes the reviewer's `UNPROVEN` bypass gap via
**option A: fail-closed direct mint**, not an unreachability claim):

`[REPO FACT]` baseline: `IdeaState.record_interaction` accepts ANY action
in `INTERACTION_DISPOSITIONS` (`engine/idea_state.py:347-348`), so once
the three W2-A values join the vocabulary, any caller could mint a
decision-action record directly, without the composition seam. Load-time
rejection (§4) alone is insufficient: invalid live in-memory state must
never exist to be consumed.

Frozen rule: the §3 context validation and the §8 ID-11 forward
constraint are enforced **in the canonical carrier mint itself** —
`IdeaState.record_interaction` MUST fail closed (raise, with NOTHING
appended) for any decision-action disposition whose context semantics
are invalid: missing/invalid/cross-context/non-founding/nonexistent
root; non-null root on a context declaration; multi-target or
cross-class supersession; an explicit `provenance` argument other than
`OWNER_STATED` (§2); and any non-neutral legacy-linkage value —
decision-action mints MUST carry `gap_context=None`, `resolves_gap=None`
and `contradicts=[]` (a non-neutral value on any of these is exactly the
§3-prohibited attachment / OW-6 cross-machinery pollution, so it is
rejected at mint, not merely avoided by convention). The carrier owns
the ledger and can validate all of this locally.
`engine/decision_composition.py` remains the canonical user-flow /
composition seam, but holds NO validation monopoly: there is no bypass
path because the carrier itself rejects invalid decision-action mints.
Legacy actions are byte-/semantics-unchanged through the same function.
The generic supersession primitive is NOT globally narrowed (§8 stands).
RED coverage: `RVR4-SEAM-1/2/3` (§20).

---

## 4. Legacy payload compatibility — bounded load rule `[OWNER DECISION]`

`[REPO FACT]` baseline: `_ASSERTION_FIELDS` is the exact 14-field tuple
`record_id, disposition, content, gap_context, iteration, provenance,
validation_status, quality, pending, responsibility, resolves_gap,
contradicts, supersedes, superseded_by`
(`engine/record_contract.py:64-69`); `assertion_from_dict` rejects unknown
AND missing fields (`:145-158`); the envelope is
`contract_version / idea_id / assertions` with
`CONTRACT_VERSION = "p4-0-record-contract-v1"`.

Frozen rule — the ONLY loader relaxation authorized:

**Legacy payload.** If a payload lacks **only** `decision_context_root`
AND its `disposition` is one of the seven pre-W2-A legacy dispositions,
then `decision_context_root := None` on load. Nothing else is defaulted.

**New decision-action records (fail closed on load AND at mint):**

- `decision_alternative_declared` without a valid `decision_context_root`
  → reject;
- `decision_alternative_withdrawn` without a valid, chain-consistent
  `decision_context_root` → reject;
- `decision_context_declared` with a non-null `decision_context_root`
  → reject;
- invalid root, cross-context root, non-founding root, nonexistent root
  → reject;
- a decision-action payload missing the `decision_context_root` key
  → reject (the legacy default applies to legacy dispositions ONLY).

**Preserved strictness:** unknown extra fields remain rejected; every
other missing field remains rejected; `reconcile_supersession_edges`'s
single-valued inverse edge and `validate()`'s reference/cycle checks are
untouched. The serializer (`assertion_to_dict`) always emits
`decision_context_root` for newly written payloads.

**No contract-version migration.** `CONTRACT_VERSION` is unchanged. A
version bump would fail-close reconstruction of every existing persisted
project (`UnknownVersionError`) unless paired with a migration — a larger,
unauthorized scope. If the bounded rule proves technically impossible at
implementation: **STOP** (do not widen silently).

---

## 5. OD-W2-DW-LIFT — recorded Owner exercise `[OWNER DECISION]`

The Owner hereby exercises **OD-W2-DW-LIFT** (source: Wave-2 contract §P
item 3 `[REPO :434-436]`; register §2 row `[REPO :81]`), authorizing ONLY
the governance permission W2-A requires:

1. reuse of the existing FDC-001 `DecisionRecord` class by the Path-N
   deterministic decision-composition seam;
2. **default-preserving constructor generalization** only where required
   for deterministic injected identities;
3. reuse of the class vocabulary required by the bounded composition seam.

This exercise authorizes **no code implementation in this gate** and does
NOT lift the broader DW Path-T hold. Explicitly preserved as forbidden:
second decision journey; new journey owner; broader Path-T activation;
live Decision Workspace behavior change; existing DW endpoint changes; DW
UI activation; persistence expansion; second canonical decision model;
unrelated DW capabilities. The broader S2 §13
`PRESERVE UNMODIFIED AND PAUSE` boundary remains intact.

**Frozen constructor-generalization scope** `[PROPOSED CONTRACT]` —
flagged for explicit review (see AA-9, §22): the composition seam requires
the generalized constructor to accept, default-preservingly (defaults
reproduce today's behavior byte-for-byte for the live DW lane):

- an injected `decision_id` (already supported:
  `__init__(decision_id=None)`, `decision_workspace.py:525` `[REPO FACT]`);
- injected deterministic sub-object identities in place of the 14 uuid4
  `_new_id` call sites (`:525,529,557,562,567,573,578,755,783,833,844,
  916,987,1071`; the function itself is defined at `:198`) `[REPO FACT]`
  (count corrected per review — the site list was complete, the count
  wrong);
- **suppression of the DW-lane seeds** — the unconditional bicycle-domain
  `CANDIDATE_NAMES` candidates, `_seed_owner_context()` claims/gaps
  (`:529,543-580` `[REPO FACT]`) and the constant `DECISION_QUESTION` —
  because the Owner's §6 premise ("the composed DecisionRecord remains a
  deterministic derived projection from the final amended active assertion
  state") is violated by fabricating bicycle content into an arbitrary
  project's composed decision. Seeds also mint identities, so seed
  handling is inseparable from injected-identity generalization. This is
  recorded as a derived necessary consequence of the Owner's own frozen
  semantics, not a silent widening;
- an injected `decision_question` (the composed value per §9).

---

## 6. FDC-001 ownership `[OWNER DECISION]` — frozen without reinterpretation

FDC-001 `DecisionRecord` remains the **SOLE canonical decision-semantics
owner**. `AssertionRecord` is only: durable carrier; explicit user-action
ledger; provenance/history mechanism. It is NOT a second decision
semantics model. The composed `DecisionRecord` remains a deterministic
derived projection from the final amended active assertion state — it is
recomputed, never persisted (§13).

---

## 7. Identity contract `[OWNER DECISION]` (enacting W2-ID v3 §D `[REPO FACT]`)

- Decision contexts are user-created and **plural** (zero/one/many per
  project). No fabricated/default context, ever (FL-4).
- Context identity: `decision-pn-<idea_id>-<root>` where `<root>` is the
  founding declaration's supersession-chain-root `record_id`.
- Candidate identity: `cand-pn-<root>` where `<root>` is the alternative
  chain's founding `record_id` (context-qualified by construction).
- Refinement within a chain preserves root identity; withdrawal + later
  redeclaration creates a new root and a new identity. Roots never reused.
- `idea_id` role: **stable project qualification input** (uuid4 minted
  once at `/start`, contract-persisted, restored verbatim — W2-ID v2
  ten-point proof stands `[REPO FACT]`).
- No replay-position identity; no ordinals; no placeholders; no
  localized-text identity; no random/uuid-generated identity anywhere in
  the canonical Path-N projection.
- Live DW-lane behavior is NOT altered merely to satisfy Path-N identity.

---

## 8. ID-11 — class-bounded single-target supersession `[OWNER DECISION]`

For records whose disposition is one of the three W2-A decision-action
values:

- a refinement or withdrawal supersedes **exactly ONE** prior compatible
  target (`len(supersedes) == 1`); founding declarations have
  `supersedes == []`;
- fail closed on: multi-target decision supersession; cross-context
  supersession; cross-class supersession (including alternative-withdrawal
  targeting a context declaration, and any decision-action record
  targeting a legacy-disposition record or vice versa); ambiguous roots;
  nonexistent target; already-superseded target.

The **generic supersession primitive is NOT globally narrowed**: legacy
non-decision behavior keeps its existing semantics unchanged.
`[REPO FACT]` note: the durable inverse edge is already single-valued
globally (`reconcile_supersession_edges` rejects two records superseding
the same prior, `record_contract.py`), so ID-11 adds a *forward*-side
class-bounded constraint only.

---

## 9. Full deterministic projection contract `[PROPOSED CONTRACT]`

Invariant (W2-ID v3 §E, preserved): **same amended ledger →
byte-identical `DecisionRecord.to_record_dict()`**. The export timestamp
`to_export_dict().export_metadata.generated_at`
(`decision_workspace.py:1130` `[REPO FACT]`) is OUTSIDE this invariant by
FDC-001's own design.

Every serialized surface of `to_record_dict()`
(`decision_workspace.py:1095-1121` `[REPO FACT]`), classified and frozen.
"Active" below always means: superseded_by is None in the final amended
reconciled ledger. Formulas leave NO implementation discretion.

| Surface | Class | Frozen source/formula |
|---|---|---|
| `schema_version` | DETERMINISTICALLY DERIVED | existing module constant `SCHEMA_VERSION`, unchanged |
| `decision_id` | DETERMINISTICALLY DERIVED | `decision-pn-<idea_id>-<context_root_record_id>` |
| `decision_question` | DETERMINISTICALLY DERIVED | `content` of the unique ACTIVE record of the context founding chain (the founding declaration, or its latest in-chain refinement) |
| `revision` | DETERMINISTICALLY DERIVED | constant `0` (no ChangeEvents exist in composition) |
| `candidates` | DETERMINISTICALLY DERIVED | one entry per ACTIVE alternative chain of this context (chain head is active AND of class `decision_alternative_declared`); withdrawn/superseded chains are ABSENT (the ledger keeps their history). Ordered by ascending numeric component of the chain-root `record_id` (`rec_N` → N). Per entry: `candidate_id = cand-pn-<chain_root_record_id>`; `name` = content of the chain's active head; `option_status = ACTIVE` (constant); `disposition_reason = None`; `disposition_basis = None` |
| `inputs` | EMPTY BY CONSTRUCTION | `[]` — no mapping from legacy assertion classes is authorized in W2-A |
| `constraints` | EMPTY BY CONSTRUCTION | `[]` |
| `gaps` | EMPTY BY CONSTRUCTION | `[]` — no seeded gaps; no derived gaps in W2-A |
| `risks` | EMPTY BY CONSTRUCTION | `[]` |
| `evidence` | EMPTY BY CONSTRUCTION | `[]` |
| `gap_assessments` | EMPTY BY CONSTRUCTION | `[]` |
| `owner_preference` | EMPTY BY CONSTRUCTION | `None` |
| `history` | EMPTY BY CONSTRUCTION | `[]` — the durable ledger IS the history (W2-ID v3 `:116-117` `[REPO FACT]`) |
| `change_impact_summary` | EMPTY BY CONSTRUCTION | `None` |
| conflict ids / `_open_conflicts`-derived output | EMPTY BY CONSTRUCTION | no conflicts are ever minted in composition |
| `readiness_status` | DETERMINISTICALLY DERIVED | the UNCHANGED FDC-001 `_compute_readiness()` applied to the composed state — a pure function of the deterministic composed content |
| `review_required_label` | DETERMINISTICALLY DERIVED | the UNCHANGED `review_required_label()` over the deterministic composed state |
| `blocking_reasons` (+ per-entry `clearing_guidance`) | DETERMINISTICALLY DERIVED | the UNCHANGED recompute derivation over composed state; ordering exactly as that pure function emits it; `clearing_guidance` from the existing static `BLOCKER_CLEARING_GUIDANCE` map |

Seeded DW-lane content (bicycle `CANDIDATE_NAMES`, `_seed_owner_context`
claims/gaps, constant `DECISION_QUESTION`) MUST NOT appear in any composed
projection (§5). If any deterministic derivation above cannot be frozen
safely at implementation: **STOP**.

---

## 10. OW-6 containment `[OWNER DECISION]`

Decision-action records MUST NOT silently become: requirements; gap
answers; gap evidence; deliverable claims; legacy assertions.

`[REPO FACT]` baseline (corrected per Independent External Review — the
prior sibling falsely claimed every consumer selects by explicit
disposition equality/membership): **the requirement-landscape chain does
NOT automatically exclude the new dispositions.**
`derive_requirement_landscape` (`engine/requirement_landscape.py:326-348`)
includes EVERY active ledger record (`superseded_by is None`) with **no
disposition inclusion gate**: its `==`/membership checks (`:213-218`,
`:245-256`) only customize labels/kind, never inclusion, and the module's
own WS6 comment states that `answered` "and every unlisted disposition
keep the legacy assertion vocabulary byte-identically." An active
`decision_context_declared` record would therefore become a legacy
"assertion"-kind requirement row, flow into `validation_plan.py` as a
validate-the-recorded-answer step (`:219-245`, anchor kind `assertion` ∈
`_STEP_ANCHOR_KINDS`), and reach the deliverable — decision actions
masquerading as recorded answers. This is exactly the fall-through W2-ID
v3 §G already recorded as repository truth, mandating that every consumer
**explicitly exclude or explicitly handle** the new class. Consumers #2
and #5–#9 below DO select by explicit disposition equality/membership —
but every containment is frozen as an explicit obligation with its own
RED test (§20), never assumed.

**Primary containment point (requires a bounded code change):** #1.
**Inherited containment (no direct modification):** #3 and #4 consume
the corrected landscape/plan and need no direct change (`[REPO FACT]`:
`validation_plan.py:219` consumes `derive_requirement_landscape`;
`deliverable_assembler.py:25-28,:455,:476,:613` consumes both, and its
only direct disposition selection is `== DISPOSITION_RISK_ACCEPTED`
`:1017`). If implementation finds either needs direct modification:
**STOP** and report the exact evidence (§19).

| # | Consumer | Containment obligation |
|---|---|---|
| 1 | `engine/requirement_landscape.py` (**no disposition inclusion gate** `:326-348` — PRIMARY containment point) | explicit bounded decision-action-class exclusion (or equally bounded explicit decision-action handling) so decision-action records never appear as requirement-landscape / recorded-answer items — per W2-ID v3 §G |
| 2 | `engine/derived_readiness.py` (`:81` explicit `==`) | never counted for readiness / provisional checks |
| 3 | `engine/validation_plan.py` (INHERITS the corrected landscape `:219`; own explicit `==` at `:242` only rewords statements) | never enter validation-plan steps — via landscape containment; no direct change |
| 4 | `engine/deliverable_assembler.py` (INHERITS landscape + plan `:455,:476,:613`; direct selection only `== risk_accepted` `:1017`) | never become deliverable claims — via inherited containment; no direct change |
| 5 | Session correction selection (`web/app.py` `/correct` — fails closed on any non-`answered` target `[REPO FACT]`) | decision-action records are NOT correctable via RVR-5; their refinement/withdrawal flows only through the W2-A routes |
| 6 | W2-D attempt gate (`engine/progression_loop.py:991 substantive_attempt_recorded`, requires `disposition=="answered"` `[REPO FACT]`) | decision-action records never satisfy the attempt gate |
| 7 | Session reconstruction/replay (`engine/session_reconstruction.py`) | replays decision-action records verbatim as ledger records; no misclassification into risk-acceptance or answer semantics |
| 8 | P7-I1 raw export (`engine/idea_development_outputs.py`; provider grounding `:124-133`, disposition selection `:147-153` `[REPO FACT]`) | never selected as development outputs; no provider fabricated for them |
| 9 | P10-D3a read/export service (`engine/read_export_service.py:120-143` governed per-assertion subset `[REPO FACT]`) | exposes the actual disposition truthfully where the existing floor already exports raw per-assertion data; **no relabeling; no second canonical export model; no field-subset expansion in W2-A** |

Raw canonical export truthfulness is containment-compatible: where a
surface already exports raw AssertionRecord data, the real disposition
string flows through unrelabeled.

---

## 11. Correction / R4-C boundary `[OWNER DECISION]`

**`R4-C CHANGE REQUIRED BEFORE W2-A: NO`** — and R4-C remains **OPEN**
(the Owner's open decision on end-of-stream replacement-replay semantics
is neither closed nor prejudged here).

W2-A MUST: consume final amended semantic state only; never derive
identity from replay position; never silently alter R4-C acceptance-lapse
semantics; preserve W2-D lapse transparency unchanged. Discovery of direct
coupling between decision composition and R4-C semantics during
implementation is a **STOP** condition.

---

## 12. Export boundary `[OWNER DECISION]`

**`EXPORT EXPANSION REQUIRED IN W2-A: NO`.** Preserved unchanged: P7-I1;
P7-I3; one canonical model; the vendor-neutral adapter boundary
(`engine/export_adapter.py`); no production connector. Any higher-level
decision-export enhancement is later and separately authorized.

---

## 13. Persistence boundary `[OWNER DECISION]`

**`FDC-001 PERSISTENCE EXPANSION REQUIRED IN W2-A: NO`.** Durable truth
remains the AssertionRecord ledger (INSERT-only store). The composed
`DecisionRecord` remains derived and recomputed on demand; it is never
silently persisted.

---

## 14. User-reachability contract `[OWNER DECISION]` — mandatory

W2-A is NOT implemented if decision composition exists only internally.
Frozen bounded reachability, in the existing Path-N journey only:

1. declare decision context;
2. declare alternative;
3. refine alternative;
4. withdraw alternative;
5. view composed decision state.

Required characteristics: existing Path-N journey only; **no new page**
unless implementation-time evidence proves it unavoidable (which then
requires scope adjudication, not silent addition); explicit user action;
confirmation where required; **persist-before-acknowledge** (durable
append commits before any acknowledgement, per the existing accept-risk /
correction patterns `[REPO FACT]`); correction-aware; deterministic
reconstruction (reconstruction returns the same decision truth);
rendered decision state in the existing session/deliverable surfaces.

`[REPO FACT]`: RVR-5 `/correct` fails closed on any non-`answered` target
(`web/app.py`), so it provides NO declaration path — it does not satisfy
this contract. No second journey.

---

## 15. EN/AR copy `[OWNER DECISION]`

Every new user-facing W2-A label/action introduced by the implementation
has governed EN and AR copy in `web/ui_text.py`, consistent with the
existing UI-language policy. Never render EN+AR simultaneously for the
same label. This does NOT activate RVR-7 substantive Arabic parity — it is
parity only for W2-A's own newly introduced UI.

---

## 16. Time-to-Value / differentiation boundary `[OWNER DECISION]`

W2-A provides mechanisms expected to CONTRIBUTE to decision usefulness,
Time-to-Value, differentiation, and traceability/trust. But:

- `T1-A′ remains OPEN`
- `TIME-TO-VALUE remains OPEN`
- `DIFFERENTIATION remains OPEN`
- `T1-C′ remains OPEN`

Final evidence remains at the applicable RVR-8 / real-user gates. No
self-certification of product success.

---

## 17. Non-blockers / scope exclusions `[OWNER DECISION]`

NOT pulled into W2-A: MG-8 (unless its trigger is newly proven); T2-G
meaning-adaptive reasoning; user-feedback ownership; legal/tax; PSRR;
payment/billing; production deployment; R4-C semantic redesign;
WS10/11/12 activation; new domains; future connectors; broader Decision
Workspace activation.

---

## 18. O.5 / O.6 preserved observations `[OWNER DECISION]`

Carried forward with their return triggers, deliberately NOT repaired in
this candidate (no opportunistic edits; no false disappearance; no
premature blocking): CURRENT_PROJECT_STATE displacement-guard drift; stale
main pin (one merge behind, PR #566); citation precision; generalized
Tier-2 wording; WS14-S6 precision; MG-6-class terminology;
`classify_domain` docstring (and the `idea_state.py:340` "six owner
actions" docstring staleness `[REPO FACT]`); `refs/reviewed` persistence
convention.

Added by Independent External Review (preserved as non-blocking; NOT
repaired or designed-around in this candidate; no FDC-001 redesign):
the W2-A composed projection will truthfully read
`insufficient_information` because comparison inputs are empty by
construction — implementation should FRAME that rendering so users do
not read it as product failure (a display-copy concern inside §14/§15
scope, not a readiness-semantics change); and the §9 candidate-ordering
formula presumes `rec_N`-shaped roots (guaranteed for canonically minted
records; a non-`rec_N` persisted root would fail rather than mis-order —
future pinning consideration only). Context withdrawal likewise remains
OUTSIDE W2-A (§2/AA-1) — usefulness alone does not add it.

---

## 19. Implementation allowlist — FROZEN, NOT EXECUTED `[PROPOSED CONTRACT]`

Revalidated against the base tree (all listed files exist `[REPO FACT]`):

| Path | Bounded purpose |
|---|---|
| `engine/idea_state.py` | three new disposition constants + `INTERACTION_DISPOSITIONS` membership; `decision_context_root` field on `AssertionRecord`; the §3 fail-closed decision-action mint validation in `record_interaction` (carrier-level — no bypass); the three `OWNER_STATED` provenance map entries (§2); legacy actions byte-unchanged |
| `engine/requirement_landscape.py` | ONE bounded purpose only (review repair): explicit decision-action-class exclusion — or equally bounded explicit decision-action handling — preventing W2-A decision-action ledger records from entering legacy requirement-landscape / recorded-answer synthesis (§10, W2-ID v3 §G). NO broader landscape redesign. `engine/validation_plan.py` and `engine/deliverable_assembler.py` remain OUTSIDE the allowlist — they inherit containment (§10); if either provably needs direct modification, implementation must STOP and report the exact evidence |
| `engine/record_contract.py` | 15-field `_ASSERTION_FIELDS`; serializer emits the new field; the bounded legacy load rule of §4 — nothing else |
| `engine/decision_workspace.py` | constructor generalization ONLY, per the frozen §5 scope (injected ids; seed suppression; injected `decision_question`); default behavior byte-identical |
| `engine/decision_composition.py` (NEW) | canonical decision-action mint seam (declare context / declare alternative / refine / withdraw, with §3/§8 fail-closed validation) + the deterministic composition of `DecisionRecord` per §9 |
| `web/app.py` | W2-A routes/affordances per §14, following the accept-risk pattern (token parity, persist-before-acknowledge, idempotency) |
| `web/templates/session.html` | declaration/refinement/withdrawal affordances + composed-state rendering |
| `web/templates/deliverable.html` | composed decision-state rendering |
| `web/ui_text.py` | EN/AR catalog entries per §15 |
| new focused W2-A test modules under `tests/` | the §20 RED inventory |

`engine/progression_loop.py` is expected NOT to be touched.

**Bounded conditional allowance:** existing test modules may be edited
ONLY to reconcile exact-field-set / round-trip assertions with the frozen
15-field contract (e.g. tests asserting the exact `_ASSERTION_FIELDS`
tuple), purely additively, with no weakening of any assertion. Digest-pin
files, if any pin the touched modules, follow the established lineage-
comment reconciliation mechanism. **Any file outside this allowlist:
implementation must STOP and request scope adjudication.**

---

## 20. RED test contract `[PROPOSED CONTRACT]` — frozen BEFORE implementation

Identity — `RVR4-ID-1` plural contexts compose independently;
`RVR4-ID-2` stable context root across resume/replay; `RVR4-ID-3` stable
`decision_id`; `RVR4-ID-4` refinement preserves identity; `RVR4-ID-5`
withdrawal + redeclaration renews identity (old root never reused);
`RVR4-ID-6` replay-order independence (same amended ledger →
byte-identical projection); `RVR4-ID-7` cross-project non-collision
(`idea_id` qualification); `RVR4-ID-8` no placeholder/ordinal identity.

Supersession — `RVR4-SUP-1` exactly one decision target accepted;
`RVR4-SUP-2` multi-target fails closed; `RVR4-SUP-3` cross-context fails
closed; `RVR4-SUP-4` cross-class fails closed (both directions, including
withdrawal→context); `RVR4-SUP-5` generic non-decision supersession
semantics unchanged.

Determinism — `RVR4-DET-1` byte-for-byte double composition;
`RVR4-DET-2` every serialized sub-id matches the §9 formula (no uuid
reachable); `RVR4-DET-3` all collection ordering deterministic per §9.

Compatibility — `RVR4-COMPAT-1` legacy payload missing only
`decision_context_root` loads with `None`; `RVR4-COMPAT-2` decision-action
payload with malformed/missing context fails closed; `RVR4-COMPAT-3`
unknown fields still rejected; `RVR4-COMPAT-4` legacy dispositions load
unchanged; `RVR4-COMPAT-5` no migration/backfill required (existing stored
projects reconstruct verbatim); `RVR4-COMPAT-6` full existing suites
green.

OW-6 — `RVR4-OW6-1`…`RVR4-OW6-9`: one explicit containment test per §10
consumer (requirement_landscape; derived_readiness; validation_plan;
deliverable_assembler; correction selection; W2-D attempt gate;
reconstruction/replay; P7-I1 export; P10-D3a service). `RVR4-OW6-1`
specifically proves an active decision-action record produces NO
requirement-landscape row; `RVR4-OW6-3`/`RVR4-OW6-4` prove the inherited
containment holds end-to-end (no validation step, no deliverable claim)
WITHOUT direct modification of `validation_plan.py` or
`deliverable_assembler.py`.

Mint seam (review repair) — `RVR4-SEAM-1` legacy interaction behavior
through `record_interaction` is byte-/semantics-unchanged for all seven
legacy dispositions; `RVR4-SEAM-2` valid canonical W2-A decision-action
mints succeed through the seam; `RVR4-SEAM-3` a DIRECT
`record_interaction` call with a decision-action disposition and
missing/invalid context semantics (per §3: bad root, non-null root on a
context declaration, cross-context/cross-class/multi-target supersession,
non-neutral `gap_context`/`resolves_gap`/`contradicts`) raises with
NOTHING appended — the bypass fails closed BEFORE any invalid live state
can exist or be consumed.

Provenance (review repair) — `RVR4-PROV-1` each of the three
decision-action mints carries `provenance == OWNER_STATED` and
`responsibility == OWNER_INPUT`; `RVR4-PROV-2` no canonical
decision-action mint ever produces `LEGACY_UNSPECIFIED`; a direct mint
passing an explicit non-`OWNER_STATED` provenance for a decision-action
disposition fails closed with nothing appended; and the legacy
provenance defaults (including the explicit-override behavior for legacy
dispositions) are byte-unchanged.

EN/AR (review repair) — `RVR4-LANG-1` every new W2-A rendered
label/cue has governed EN AND AR catalog text in `web/ui_text.py`;
`RVR4-LANG-2` the active UI language selects which one renders;
`RVR4-LANG-3` EN and AR are never simultaneously rendered for the same
W2-A label; `RVR4-LANG-4` Arabic/English/mixed user INPUT does not
itself switch the UI language. (Coverage of W2-A's own new UI only —
NOT RVR-7 substantive Arabic parity.)

Correction — `RVR4-CORR-1` refine; `RVR4-CORR-2` withdraw;
`RVR4-CORR-3` redeclare; `RVR4-CORR-4` provenance integrity (ledger
retains full verbatim history; inverse edges reconciled).

Reachability — `RVR4-REACH-1` declare-context route reachable;
`RVR4-REACH-2` declare-alternative route reachable; `RVR4-REACH-3`
refinement reachable; `RVR4-REACH-4` withdrawal reachable;
`RVR4-REACH-5` persistence-before-acknowledgement; `RVR4-REACH-6`
composed result rendered in the existing surfaces; `RVR4-REACH-7`
reconstruction returns the same decision truth.

All of these MUST exist RED before the implementation turns them GREEN.

---

## 21. Deferred Obligations Register — transition plan (NOT executed here)

This candidate does NOT modify the register. Frozen future transitions:

**After the authoritative contract-freeze merge of this candidate:**

- OD-W2-DW-LIFT row: eligible for `CLOSED — evidence verified` (the Owner
  exercise is explicitly recorded in §5 and merged).
- Post-W2-ID sync / lineage rows: eligible for
  `CLOSED — evidence verified` using PR #566 merge evidence.
- W2-A enactment set: remains **OPEN**, with contract details FROZEN.
- RVR-4 / W2-A implementation: remains **OPEN / NOT STARTED**.

**After a future accepted W2-A implementation merge (separate gate):**

- W2-A enactment set may become CLOSED only with exact implementation +
  RED→GREEN evidence.
- The RVR-4/W2-A row may close only with exact accepted implementation
  evidence.

No future work is closed inside this candidate; no status is self-
certified.

---

## 22. Anti-anchoring correspondence record `[EXECUTED EVIDENCE]`

Fourteen falsification attempts run against the base tree before freeze:

- **AA-1 (V2 sufficiency):** V2 has no context-withdrawal value. Falsification
  attempt: is one materially necessary? The frozen reachability set (§14)
  contains no context-withdrawal operation; contexts are plural, so a user
  abandons a context by declaring another; the ledger keeps truth. NOT
  materially necessary for W2-A → V2 stands; context withdrawal is a
  future Owner vocabulary decision, and no cross-class workaround is
  permitted (§2, §8).
- **AA-2 (refinement disposition):** unnecessary — `record_interaction`
  already carries `supersedes=` `[REPO FACT]`; the relation expresses
  refinement completely. Stands.
- **AA-3 (`decision_context_root` ambiguity):** the one found ambiguity —
  what a context *refinement* carries — is resolved by freezing `None` for
  ALL `decision_context_declared` records with chain membership derived
  from the supersession edge (§3). No residual ambiguity.
- **AA-4 (legacy defaulting bounded):** the default applies to exactly one
  missing key under a legacy-disposition condition; decision-action
  payloads never benefit. Bounded. Stands.
- **AA-5 (no version bump):** a bump fail-closes every existing project
  (`UnknownVersionError` `[REPO FACT]`) absent a migration; the bounded
  rule preserves losslessness (serializer always emits the field). Stands.
- **AA-6 (lift without broader activation):** class reuse + constructor
  generalization touch no live DW route/UI/persistence. Stands.
- **AA-7 (FDC-001 sole owner):** composition emits FDC-001 objects only;
  AssertionRecord carries. Stands.
- **AA-8 (no second model):** projection is derived/recomputed, never
  persisted; one canonical export model preserved. Stands.
- **AA-9 (all formulas freezable):** YES — with one derived consequence
  surfaced rather than concealed: seed suppression and `decision_question`
  injection are REQUIRED by the Owner's own "derived projection from the
  final amended active assertion state" premise, because the current
  constructor unconditionally fabricates bicycle-domain content
  (`decision_workspace.py:529,543-580` `[REPO FACT]`). Recorded in §5 for
  explicit review adjudication; not treated as silent scope.
- **AA-10 (reachability fits Path-N):** session/deliverable templates and
  the accept-risk affordance pattern exist `[REPO FACT]`; no new page
  needed. Stands.
- **AA-11 (export unchanged):** raw floors expose disposition verbatim;
  new values flow truthfully with zero export code change; D3a subset not
  expanded. Stands.
- **AA-12 (persistence unchanged):** ledger remains sole durable truth.
  Stands.
- **AA-13 (R4-C separable):** composition reads final amended active state
  only; no replay-position dependence anywhere in §9. Stands.
- **AA-14 (missing owner):** EN/AR copy → existing ui_text policy;
  elicitation prompts → governed class under the decision owner (OW-5,
  W2-ID v3 `[REPO FACT]`); no new unowned surface found. Stands.

Review-repair falsification round (fresh sibling — the reviewer was NOT
blindly adopted; each finding was independently reproduced or falsified
against the base tree `[EXECUTED EVIDENCE]`):

- **AA-15 (reviewer's OW-6 finding):** falsification FAILED — the finding
  is TRUE. `derive_requirement_landscape` has no disposition inclusion
  gate (`requirement_landscape.py:326-348` re-read directly); the prior
  sibling's §10 baseline was false for consumers #1/#3/#4 and contradicted
  W2-ID v3 §G. Repaired in §10/§19. The reviewer's minimal containment
  point (one file, `requirement_landscape.py`; #3/#4 inherit) was also
  independently confirmed: `validation_plan.py:219` consumes the
  landscape; `deliverable_assembler.py`'s only direct disposition
  selection is `== risk_accepted` (`:1017`).
- **AA-16 (mint-seam bypass):** confirmed real — `record_interaction`
  accepts any vocabulary action (`idea_state.py:347-348`), so seam-only
  validation would leave a live in-memory hole. Closed via option A
  (carrier-level fail-closed mint, §3) rather than an unreachability
  claim, which could not be proven.
- **AA-17 (provenance):** confirmed — unlisted actions default to
  `LEGACY_UNSPECIFIED` (`:350-351`), false for explicit owner decision
  actions. `OWNER_STATED` verified as the existing, semantically exact
  governed value (the `risk_accepted` precedent `:143-145`); no new
  vocabulary invented, so no escalation was required.
- **AA-18 (EN/AR RED gap):** confirmed — §15 was an obligation without
  RED coverage; `RVR4-LANG-1…4` added, bounded to W2-A's own UI.
- **Self-invalidation check on reviewer-adjudicated-sound areas:** the
  re-reads surfaced NO new evidence invalidating any of them (vocabulary,
  `decision_context_root` semantics, legacy compatibility, AA-9
  boundedness, ID-11, determinism formulas, boundaries, register
  transitions all stand).

No Owner premise was invalidated; no contradiction requires escalation.

---

## 23. Non-authorization statement

This candidate, even once merged, authorizes ONLY the contract terms
above. W2-A implementation requires a separate explicit Owner
authorization under the established lifecycle (verify tip → bounded
candidate → freeze SHA → Grill → bundle → Owner merge). Statuses used
here (`RECORDED` / `PLANNED` / `ELIGIBLE` / `OWNER-AUTHORIZED` / `ACTIVE`
/ `CLOSED`) are never conflated; closing this gate activates nothing.
