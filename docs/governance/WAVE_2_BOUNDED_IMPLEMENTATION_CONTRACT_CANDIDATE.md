# Wave-2 Corrected Bounded Implementation Contract — CANDIDATE

STATUS: `WAVE-2 CORRECTED CONTRACT CANDIDATE — NOT AUTHORITATIVE UNTIL
OWNER-AUTHORIZED, MERGED, AND POST-MERGE VERIFIED. WAVE-2 IMPLEMENTATION NOT
AUTHORIZED. RVR-7 WAVE PLACEMENT: WAVE 3 — UNCHANGED. RVR-8 EXECUTION NOT
AUTHORIZED. SECOND S2 RUN NOT AUTHORIZED. WHY THIS MATTERS USER-FACING RENDER:
NOT AUTHORIZED (OD-PDVG-12 undecided).`

This is the FINAL corrected candidate after two Independent External Review
rounds. Round 1: prior candidate `89736887c10f1e37c03bc11b8b1f0c70647b7e9c`
returned `ACCEPT WAVE-2 CONTRACT CANDIDATE WITH REQUIRED CORRECTIONS`.
Round 2 (bounded differential review): corrected candidate
`fd2e1052df51d6704913a1418a18a44ac733b4a5` returned `ACCEPT CORRECTED WAVE-2
CONTRACT CANDIDATE WITH REQUIRED CORRECTION` — exactly two remaining material
corrections, applied in this candidate: (A) the W1-S2 attempt boundary is the
canonical durable **active-set rule**, not a temporal "since last OPEN"
anchor (§F); (B) MG-8 distinguishes **implementation locus** from
**governance owner** (§R S-13). Both priors are preserved unamended as
immutable reviewed evidence (`refs/reviewed/wave2-contract-89736887`,
`refs/reviewed/wave2-contract-fd2e1052`); neither is accepted for
publication, and this document supersedes both in full. All differential-
review PASS findings are preserved unchanged. Every reviewer finding was
independently re-verified against the repository before adoption; none was
adopted on the reviewer's authority alone.

Evidence tags: `[REPO]` committed repository truth (cited), `[EXEC]` executed
probe at the verified tip, `[OWNER]` owner decision/authority premise,
`[HYPOTHESIS]` design hypothesis requiring implementation-time proof,
`[OPEN]` genuinely undecided, `[PROPOSED WAVE-2 INVARIANT]` new binding
language first introduced by this contract (not pre-existing repository
authority).

---

## A. Authority reconstruction

Re-verified independently at candidate time:

| Item | Verified value |
|---|---|
| Authoritative branch | `feature/atomic-json-session-persistence` |
| Live tip (0 commits after; re-fetched) | `e02d175b93556213e22e6af0decd66f12966ff7f` — Merge PR #562 (Wave-1 closure) `[EXEC]` |
| Closure merge parents / tree | `93be682a…` + `342cbab5…`; tree `8dadc12c…` = accepted closure-candidate tree `[EXEC]` |
| S2 evidence | `refs/evidence/s2run-ebf243db` → `ebf243db…`, unamended `[EXEC]` |
| Prior Wave-2 candidates | `89736887…` and `fd2e1052…`, both parent `e02d175b…`, preserved as `refs/reviewed/wave2-contract-89736887` / `refs/reviewed/wave2-contract-fd2e1052` `[EXEC]` |
| Supersession analysis | tip unchanged since the prior candidate; NONE required `[EXEC]` |

Owner authority chain unchanged: Owner-frozen Final Remediation Contract
(RVR-1…RVR-8); Wave-1 authoritative and closed; register Wave-1 section:
OD-R1/OD-R2/OD-PDVG-02(a) CONSUMED; OD-R3 (RVR-4, Wave 2+), OD-R5 (RVR-6,
Wave 2+), OD-R4 (RVR-7, **Wave 3**) ACCEPTED IN PRINCIPLE, implementation
Owner-gated `[OWNER][REPO]`.

## B. Reviewer correction matrix — each finding independently re-verified

| Review finding | Independent verification | Disposition |
|---|---|---|
| RVR-7 recorded as Wave 3; prior candidate placed it in Wave-2 undisclosed | CONFIRMED — register Wave-1 section: OD-R4 "…(Wave 3, separate Owner authorization)" `[REPO]` | ADOPTED — RVR-7 restored to Wave 3 (§O) |
| "Deliverable is `<html lang=\"en\">` LTR" is false (stale comment) | CONFIRMED — `deliverable.html:1` extends `base.html`; `base.html:2` renders `<html lang="{{ ui_lang }}" … dir="rtl">` in AR sessions; the `lang="en"` text at `deliverable.html:169` is a Jinja comment `[REPO]` | ADOPTED — corrected truth in §C |
| `AssertionRecord` has no `question_id`; WS10 D3 forbids adding one; placeholder ids unsafe; Stage-2 gap types can't own decision questions | CONFIRMED — `idea_state.py:184-209` (no field); WS10 increment contract D3 verbatim: "No `question_id`, `intent_id`, or related registry data is added to `IterationLog`, `AssertionRecord`, `AcknowledgedUnknown`…" `[REPO]`; GD-001 three-stage journey frozen `[REPO]` | ADOPTED — decision-capture mini-gate (§E) |
| W1-S2 "any answered record" gate is junk-bypassable | CONFIRMED — no `refused` disposition (`INTERACTION_DISPOSITIONS`, 7 values `[REPO]` idea_state.py:122-126); any non-empty response is recorded `answered` regardless of relevance; recorded `quality` is the STATE-level leading-evidence aggregate (`app.py:3136-3138`), not the answer's tier `[REPO]` | ADOPTED — strengthened gate (§F), with the reviewer's proposal verified viable, not assumed |
| §D.B "recorded quality tiers / substance detections" are not repository truth | CONFIRMED — same evidence; structured-substance and relevance results are recorded nowhere; canonical export drops `content` and `quality` `[REPO]` | ADOPTED — signal-truth table + recomputation architecture (§G) |
| WS10 scope issues (11→active-domain reconciliation; decision ids outside scope; OD-PDVG-12 silently absorbed) | CONFIRMED — loader takes ONE `source_artifact_path` with exact ID-set equality (D11) `[REPO]`; PDVG-01: "the render is a separate decision (OD-PDVG-12)", OD-PDVG-12 REGISTERED AND UNDECIDED `[REPO]`; OD-PDVG-04 (REVISED) option (a) already contemplates "content authoring for the 21 committed questions" `[REPO]` | ADOPTED — corrected scope (§I) |
| W/M precondition circular | CONFIRMED — the values are produced by W2-B evidence; OD-R5 requires only "Owner-approvable" `[REPO]` | ADOPTED — moved to W2-B acceptance (§P) |
| "Later-merger owns conflicts, per the Wave-1 precedent" misstates the precedent and breaks exact-SHA acceptance | CONFIRMED — Wave-1 was one linear chain, one accepted SHA, empty candidate→merge diff; conflict-resolved merges would produce a tree ≠ the accepted candidate tree | ADOPTED — serialized exact-SHA lifecycle (§M) |
| User-feedback mapped to "OD-PDVG-09/-13 family" is a force-fit | CONFIRMED — PDVG-01 §9: user-feedback capture has **no current owner**, no OD assigned; "Neither is force-fitted into an adjacent owner to make the ledger tidy" `[REPO]` | ADOPTED — `NO CURRENT OWNER / OWNER DECISION REQUIRED` (§R) |
| MG-8 omitted from the sweep | CONFIRMED — MG-8 in the S2 evidence sweep (tier OBSERVATION, "cause unproven"); `known_problem` populates only from answers meeting relevance + ≥REASONED (`progression_loop.py:879, 1114-1115`), never from the durably recorded `seed_idea_text` (`app.py:2234`) `[REPO]` | ADOPTED — restored with disposition (§R) |
| Determinism phrase presented as inherited | CONFIRMED — "Canonical deterministic routing → Adaptive presentation" appears in no committed repository document `[EXEC grep]`; it came from the (chat-level) Owner-frozen remediation architecture, which is not committed text | ADOPTED — labeled `[PROPOSED WAVE-2 INVARIANT]` (§S) |
| Decision export already covered by P7 extensibility | CONFIRMED — P7-I1 IR-6 freezes no schema; P7-I3 floor is a minimum ("MAY preserve more … MAY NEVER reduce") `[REPO]` export_adapter.py:20-25 | ADOPTED — no redundant Owner gate (§L) |
| Slice count "six" wrong | CONFIRMED — W2-E was folded, not independent | ADOPTED — exact counts (§N) |
| `PROHIBITED_STATUS_VALUES` test-enforced only | CONFIRMED — defined once, no runtime reference `[EXEC grep]` | ADOPTED — C.F-style guards mandatory on every new render surface |

Reviewer statements NOT adopted blindly: the review itself corrected its own
premise that renaming a `question_id` breaks replay (ids are not in the
ledger; breakage lands in pinned artifact tests / WS10 ID-set equality /
evidence references) — this candidate records the corrected version. No
reviewer finding was found to contradict repository truth on re-verification.

## C. Current implementation truth — corrections to the prior candidate

1. **Deliverable language (corrected).** Shell language/direction: the
   deliverable extends `base.html` and renders `<html lang="ar" dir="rtl">`
   in Arabic sessions, `<html lang="en">` in English sessions `[REPO]`.
   Substantive technical content language: largely English in both (question
   text, evidence content, technical framing; governed `t()` strings are the
   translated subset). Canonical state: language-independent. The RVR-7 gap
   is **substantive Arabic parity, not shell RTL activation** — the shell is
   already RTL-capable. Stale template comments are not runtime behavior and
   are not cited as such anywhere in this candidate.
2. **Ledger signal truth (corrected).** See §G — no "recorded quality tier"
   or "recorded substance detection" exists per answer.
3. Everything else in the prior candidate's §B reconstruction stands as
   independently re-verified by the review (FDC-001 bicycle-hard-coded,
   separate in-memory journey; `IdeaState` has no decision field; WS10
   loader-only; WS11 dormant; WS12 observation-only; no attempt gating;
   active domains `['electronics_electrical','mechanical']`; `progression_loop.py`
   digest-pinned by three enforcing tests).

## D. Architecture D — confirmed (capture layer redesigned)

Architecture D stands as architecture (review: PASS): FDC-001 `DecisionRecord`
remains the single decision-semantics owner; no second canonical decision
model; ODS stays out of scope (committed post-MVP deferral; no evidence of
necessity); decision state renders inside the existing Path-N
journey/deliverable; export rides the existing canonical output architecture.
The chain
`Path-N journey → bounded decision capture → FDC-001 DecisionRecord →
existing deliverable/export`
remains preferred — **conditional on §E resolving the capture mechanism
before any W2-A implementation.** The prior candidate's capture design
("ledger records against decision-scoped governed question identities") is
WITHDRAWN as unimplementable under the current record contract (§B row 3).

Preserved from the prior candidate (review-verified): constructor
generalization with `None`-defaults preserving bicycle behavior byte-for-byte;
pure composition seam `engine/decision_composition.py` (documented per File
Creation Rules; a seam, not a semantics owner); qualification/elimination only
through FDC-001's existing deterministic vocabulary — no invented scoring;
`OWNER PREFERENCE != TECHNICAL SELECTION`; `insufficient_information` /
`blocked_by_evidence_gap` as the governed NOT-ENOUGH-EVIDENCE states with no
forced winner; one journey (DW lane not expanded; OD-W2-DW-LIFT exercised
only as class reuse); anti-duplication tests C.F(1)–(4), now plus:
(5) runtime guard tests on every new render/export surface asserting no
`PROHIBITED_STATUS_VALUES` member appears (the prohibition is currently
test-enforced only `[EXEC]`).

## E. Decision-Capture Identity / Recording Mini-Gate (W2-ID) — governance sub-gate, before W2-A

A bounded, governance/contract-only gate that MUST complete (Owner-accepted)
before RVR-4 implementation freezes. Corrected dependency:
`W2-D → W2-ID → W2-A`. It must determine, from repository truth:

- **E.A** What durable record legitimately carries: the user-stated decision
  alternative (verbatim), its identity, provenance, relationship to the
  current project, and later qualification/elimination state.
- **E.B** Whether the correct carrier is: an existing legitimate record type;
  a bounded extension of an existing record contract (a governed record-schema
  gate — `AssertionRecord`/store changes are NOT made casually and are
  currently excluded by WS10 D3); a new record type under FDC-001 ownership;
  or another already-authorized seam. `[OPEN — the mini-gate decides]`
- **E.C** Where question identity attaches, if needed — noting the ledger
  carries `gap_context` (gap type) only, and decision-alternative questions
  fit none of the three frozen GD-001 Stage-2 gap types `[REPO]`.
- **E.D** Whether decision-capture questions are: Path-N questions (requires
  the content gate and would strain GD-001); FDC-001 decision prompts
  (rendered inside the same journey); or a separate governed identity class
  consumed inside the same journey. `[OPEN]`
- **E.E** How replay, versioning, and correction (R4-C full re-evaluation)
  operate over the chosen carrier — with live-vs-replay equivalence tests
  mandatory.
- **E.F** How duplication with `IdeaState`, FDC-001, and WS10 is prevented —
  named anti-duplication tests, single-owner assertions.

Hard constraints carried into the mini-gate: **no placeholder canonical
identities anywhere durable** (content-gate re-approval, WS10 D10 registry
reconciliation, and pinned `EXPECTED_IDS_IN_ORDER` tests make
placeholder-then-rename ungoverned `[REPO]`); no silent WS10 scope insertion
(§I); no forcing capture into MECHANISM/FEASIBILITY/BOUNDARY gap types; no
second decision vocabulary. If the mini-gate concludes a record-schema
extension is required, that extension is its own explicitly authorized
contract item, never a side effect.

## F. W1-S2 substantive-attempt contract — strengthened

Owner policy: a currently-served Stage-3 gap must receive **at least one
substantive answer attempt** before `Accept Risk` becomes available.

**Corrected deterministic definition** (smallest current mechanism, verified
against the tree — the reviewer's proposal was independently confirmed viable,
not adopted blindly):

`substantive_attempt_recorded(state, gap_type)` is true iff there exists at
least one **active** ledger record satisfying ALL of (the canonical durable
**active-set rule** — the SAME `superseded_by is None` rule the correction
seam already documents as "the one canonical active-set rule",
`session_reconstruction.py:19, 227, 235` `[REPO]`):

1. `superseded_by is None` (active record);
2. `disposition == answered`;
3. `gap_context ==` the currently served gap type;
4. STORED verbatim `content` is NOT a weak/refusal pattern (the existing
   `_WEAK_PATTERNS` guard, `progression_loop.py:442` `[REPO]`), recomputed at
   evaluation time; and
5. `engine.gap_relevance.addresses_gap(content, gap_type)` is True
   (`gap_relevance.py:209` `[REPO]`), recomputed at evaluation time.

**A superseded/withdrawn attempt does NOT satisfy the live Accept Risk
availability gate.** After a correction supersedes the prior substantive
attempt, it no longer unlocks Accept Risk; the user must make a NEW active
substantive attempt against the corrected state before Accept Risk becomes
available again.

The prior temporal boundary — "recorded since the gap last entered OPEN" —
is WITHDRAWN as unsafe: gap OPEN transitions are not durably recorded as
their own events, reconstructed `opened_at` lives in replay coordinates while
ledger iterations preserve historical/live coordinates, and correction
supersession rebuilds state — so a temporal comparison is ambiguous across
correction/replay. The active-set rule needs no time anchor: supersession
itself removes a lapsed attempt from the active set. **No new "gap opened"
event type is introduced, and no new ledger field is added** — the active-set
rule is sufficient on current evidence.

Properties: deterministic; pure recomputation from durable fields (no new
persisted field, no LLM, no nondeterminism); replayable. **Fail-safe:** the
known W1-N3 false-negative means a legitimate answer may fail check 5 — then
`Accept Risk` stays unavailable while the truthful exits (`unknown`,
`deferred`, specialist/evidence requests) remain; that is accepted behavior.
The gate remains a **live availability precondition** (route + affordance) —
NOT embedded in the canonical writer `accept_gap_risk`, so replay of
historical accepted-risk ledgers (recorded acceptances with zero or weak
attempts) remains reproducible; repository evidence (the reconstruction seam
re-applies recorded acceptances through the writer) confirms this placement.

Mandatory tests (all eight required):
1. active substantive answer → Accept Risk available;
2. weak/refusal answer ("I don't know", "n/a", generic filler) →
   unavailable (blank/whitespace is already unrecordable —
   `app.py:2696/3027` strip + `if response:` gate `[REPO]`);
3. irrelevant answer → unavailable;
4. active legitimate concise technical answer → available;
5. substantive answer later superseded by correction → unavailable;
6. new substantive answer after correction → available;
7. pre-Wave-2 accepted-risk historical ledger still reconstructs
   identically;
8. the W1-N3 fixture remains safe if still false-negative (documents
   current behavior until §J resolves).

Honest mechanism bound (no over-claim): the lexical mechanism does NOT
guarantee that all arbitrary buzzword stuffing is blocked.
**Known/adversarial stuffing fixtures must not unlock Accept Risk; lexical
false-positive bounds remain protected by the existing relevance invariants
and regression tests** (the W1-N1/W1-N2 invariant: REASONED classification
alone is not proof of technical validity or progression eligibility).

Owner: the existing RVR-1 accepted-risk seam. No second risk-acceptance
mechanism. `W1-S2 CLOSED: NO` until implemented and merged.

## G. RVR-6 register evidence basis — corrected

Signal truth at the tip `[REPO]`:

| Signal | Status |
|---|---|
| `AssertionRecord.content` (verbatim answer), `disposition`, `gap_context`, `iteration`, `provenance` | DURABLY STORED |
| `AssertionRecord.quality` | DURABLY STORED but **state-level leading-evidence aggregate** (`app.py:3136-3138`) — NOT the answer's own tier; junk recorded after a good answer carries `REASONED`; MUST NOT be used as an answer-local signal |
| Per-answer quality tier | NOT AVAILABLE as stored; RECOMPUTED deterministically from stored `content` via the existing pure assessors where needed |
| Structured-substance detection (RVR-3 Layer-3) | NOT AVAILABLE as stored; RECOMPUTED from stored `content` (`_structured_technical_form` and companions are pure `[REPO]`) |
| Gap-relevance result | NOT AVAILABLE as stored; RECOMPUTED (`addresses_gap` is pure) |
| Explicit user display preference | DISPLAY-ONLY (presentation; never canonical state) |

**Chosen architecture: A — deterministic recomputation from stored answer
content using existing pure assessors.** No new persistent fields are
required for register derivation `[HYPOTHESIS — confirmed or falsified by
W2-B's RED tests; if recomputation proves semantically insufficient, option B
(a separately governed record-schema addition) requires its own gate and is
NOT pre-authorized]`. The register remains: deterministic; replayable;
reversible; no persona; no hidden profile; no model inference; no permanent
expert flag; NEUTRAL on insufficient/conflicting evidence. W/M are bounded
implementation parameters (§P). The prior candidate's "recorded response
quality tiers / recorded structured-substance detections" wording is
WITHDRAWN as factually wrong.

Related mandatory disclosure (review sweep finding 1): the ledger-quality
aggregate semantics above also mean any evaluator or surface reading recorded
`quality` as answer quality is misled; Wave-2 surfaces MUST NOT do so, and
W2-B's evidence pack must state this. Changing what the route records is a
record-semantics change OUTSIDE Wave-2 scope unless separately authorized.

## H. RVR-6a contract — bounded adaptive routing / register core

Unchanged from the prior candidate except as corrected by §G and §M:
Tier-1/Tier-2 fence preserved (`STATE-ADAPTIVE = Tier-1`;
`MEANING-ADAPTIVE = Tier-2`, OD-PDVG-10 undecided, untouched — review: PASS);
domain-aware routing through the existing domain-aware seams and content
gates (no new domain-owner system); prior-answer-aware suppression from
canonical state + gap state + governed evidence + dispositions +
`ServedQuestion.question_id` (+ WS10 completion state after W2-C); state-aware
ordering as ONE bounded deterministic policy layer over the `select_next_gap`
core (may promote: critical unresolved gap, lapsed acceptance, newly
comparable decision state, completed-intent skip); unknown-aware rerouting
(accepted risks not re-asked; visible governed cue; reopened only by
correction lapse). All selection/derivation functions are pure functions of
committed content + canonical state.

## I. WS10 corrected scope

1. **Existing scope.** The active committed Path-N question-ID set is 21
   (electronics 11 = 4/4/3; mechanical 10 = 4/2/4) `[EXEC]`. PDVG-01's
   OD-PDVG-04 (REVISED) option (a) already contemplates "content authoring
   for the **21 committed questions**" `[REPO]`, and OD-R5 partially promoted
   OD-PDVG-04(a) in principle `[OWNER]`. However the WS10 loader contract
   validates ONE registry against ONE `source_artifact_path` with exact
   ID-set equality (D11/D19) `[REPO]` — written in the electronics era. The
   corrected WS10 scope decision (§P) must explicitly choose the covering
   mechanism: per-domain registry instances (one per committed artifact,
   loaded through the same loader) or an explicitly approved combined source
   reconciliation. **Nothing here assumes 21-in-one-registry is already
   contract-valid.**
2. **Decision identities.** Decision-capture identities (§E) are NOT inserted
   into this scope. If decision capture needs intent metadata, the W2-ID
   mini-gate decides between an explicit, separately approved WS10 scope
   extension or a decision-owner metadata mechanism under FDC-001 — one
   registry loader, no duplicate registry, either way.
3. **`Why this matters`.** The user-facing question-explainability render is
   **OD-PDVG-12 — REGISTERED AND UNDECIDED** `[REPO]`, deliberately split
   from content authoring by PDVG-01. This contract does NOT absorb it:
   `WHY THIS MATTERS USER-FACING RENDER: NOT AUTHORIZED`. WS10 content
   authoring proceeds within its approved scope regardless; W2-C ships
   suppression / completion detection / intent-aware ordering WITHOUT the
   explainability render unless OD-PDVG-12 is separately decided by then, in
   which case the render is a bounded W2-C display item under the Phase-3
   UX display owner PDVG-01 names.

## J. W1-N3 — reconciled disposition

Strategy accepted by review, preserved: question-id-scoped supplemental
relevance; broad markers prohibited (measured leaks recorded in
`gap_relevance.py` `[REPO]`); frozen S2 fixture as regression evidence only;
no semantic model judgment; mandatory false-positive guard (R3
semantic-stability corpus); evidenced fallback = SAFE FALSE-NEGATIVE.

**Dependency correction:** W1-N3's question-id scoping uses the EXISTING 21
committed Path-N question identities — which exist today `[EXEC]` — and its
intent-derived markers use the W2-C-authored WS10 content for those SAME
existing ids. It depends on NO new or placeholder identity and does NOT
depend on W2-ID. Placement: W2-C work-item. Disposition frozen by OD-W2-AUTH:
`ATTEMPT BOUNDED CLOSURE IN W2-C; EVIDENCED FALLBACK = DEFER AS SAFE
FALSE-NEGATIVE`.

## K. W1-N4 — preserved (review: PASS)

Computation at the RVR-1/R4-C reconstruction seam: the sole re-application
site (`session_reconstruction.py:274-279`) today silently skips an
inapplicable recorded acceptance (`except ValueError: pass` `[REPO]`) — it
gains a read-only applied/lapsed report (record_id, gap_type, refusal
reason). RVR-5 renders the truthful explanation: what changed, which
acceptance lapsed, why the gap reopened, what to do next. D-AISR-06
unchanged; no stale acceptance retained; RVR-6a may cue but a named test
asserts a single explanation owner. `W1-N4 CLOSED: NO` until implemented and
merged (W2-D).

## L. Decision export authority — corrected statement

Verified: P7-I1 deliberately freezes no export version identity and no field
names (IR-6); P7-I2 permits additive backward-compatible change; P7-I3's
preservation floor is a minimum that may never shrink but may be exceeded
`[REPO]` export_adapter.py:20-25. Therefore: **additive decision-state export
is permitted under the existing canonical export owner** — no second output
model, no new export version identity, preservation floor not reduced,
adapter equivalence rules intact, and **no quality semantics smuggled into
export** (the canonical export today deliberately drops `content` and
`quality`; decision-state fields must not reintroduce answer-quality claims).
No redundant Owner gate is created; the addition is authorized by OD-W2-AUTH
through the W2-A slice that carries it.

## M. Exact-SHA serialized integration lifecycle — corrected

The prior candidate's "later-merger owns conflict resolution (per the Wave-1
precedent)" is WITHDRAWN: Wave-1 was one linear chain with one accepted SHA
and an empty candidate→merge diff; conflict-resolution at merge time would
make a tree authoritative that differs from the Owner-accepted candidate
tree, destroying the empty-diff post-merge verification invariant.

Corrected model, binding for all Wave-2 slices:

- Functional analysis and implementation **exploration** may proceed in
  parallel (W2-A ∥ W2-B are functionally independent).
- Authoritative candidate lifecycle is **serialized**: candidate 1 freezes
  against the current authoritative base → Grill → Independent Review →
  Owner exact-SHA acceptance → merge (merge tree must equal the accepted
  candidate tree) → post-merge verification; candidate 2 then reconstructs
  from the NEW authoritative tip — any prior parallel work is re-integrated
  and frozen as a NEW SHA against the new base and runs the FULL
  Grill/review/acceptance lifecycle on that new SHA.
- No accepted candidate ever receives conflict-resolution edits; no
  amend/rebase/force-push of any frozen SHA; failed candidates preserved as
  refs.

Shared-surface risk (both W2-A and W2-B touch `web/app.py`, templates,
`ui_text.py`, and W2-B touches digest-pinned `progression_loop.py`) is
handled by this serialization, not by merge-time resolution.

## N. Corrected Wave-2 sequencing and exact counts

```
W2-D  (W1-S2 strengthened gate + W1-N4 lapse report/render)     [executable]
  ↓
W2-ID (Decision-Capture Identity / Recording Mini-Gate)          [governance sub-gate]
  ↓
W2-A  (RVR-4 decision composition per W2-ID outcome)             [executable]
  ∥ analysis only — acceptance serialized per §M
W2-B  (RVR-6a routing/register core per §G/§H)                   [executable]
  ↓
W2-C  (RVR-6b WS10 bounded content + intent-aware suppression/
       completion/ordering + decision-aware routing consuming
       W2-A state + W1-N3 bounded attempt; explainability render
       ONLY if OD-PDVG-12 separately decided)                    [executable]
```

`WAVE-2 GOVERNANCE SUB-GATES: 1` (W2-ID — governance/content-contract only;
if its outcome requires implementation, that implementation lands inside
W2-A, not in the sub-gate).
`WAVE-2 EXECUTABLE IMPLEMENTATION SLICES: 4` (W2-D, W2-A, W2-B, W2-C).
The prior "six slices" statement is WITHDRAWN (RVR-7 left Wave-2; W2-E was
never independently frozen — it is a W2-C work-item).

## O. Wave-3 boundary — RVR-7

`RVR-7 WAVE PLACEMENT: WAVE 3 — UNCHANGED` (register: OD-R4 accepted in
principle, implementation NOT authorized, Wave 3, separate Owner
authorization `[REPO]`). Wave-3 remains `RVR-7 → separately authorized
RVR-8`. Strategic requirement preserved, not downgraded: **Arabic substantive
parity remains required before first serious release IF Arabic is represented
as a substantive supported experience** — and Wave-2 therefore makes NO
Arabic-parity closure claim. The prior candidate's RVR-7 contract content
(same-question_id AR variants via the content gate; no runtime translation;
EN/AR canonical-state invariance; W1-N1/W1-N2 as mandatory verification
inputs; semantic-equivalence review; the OD-W2-D-P6-18 display-rule
supersession decision) is carried forward as the Wave-3 CONTRACT INPUT, to be
frozen at the Wave-3 gate — nothing of it is executable in Wave-2. The
D-P6-18 supersession decision moves to that Wave-3 gate.

## P. Owner decisions — simplified package

**Required before the relevant implementation:**

1. **OD-W2-AUTH** — authorize the corrected Wave-2 architecture/sequencing
   (§N), the exact-SHA lifecycle (§M), the W1-N3 disposition (§J), and the
   artifact/content-gate changes Wave-2 needs (WS10 registry artifact; any
   Path-N artifact metadata the slices touch) — the content-gate approvals
   may alternatively be given at each content-touching slice's contract
   freeze.
2. **W2-ID mini-gate Owner acceptance** — before W2-A freeze (§E).
3. **OD-W2-DW-LIFT** — before W2-A: exercise OD-R3's bounded DW-lane-hold
   lift exactly as §D scopes it (class reuse; no second journey; the S2 §13
   `PRESERVE UNMODIFIED AND PAUSE` hold otherwise stands).
4. **OD-W2-WS10-SCOPE (corrected)** — before W2-C freeze: exercise
   OD-PDVG-04(a) for the 21 committed ids AND decide the loader-contract
   covering mechanism (§I.1).

**Deferred to slice acceptance (NOT pre-Wave-2 gates):**

- **W/M hysteresis values** — proposed and frozen inside the W2-B
  candidate/evidence pack; accepted through Owner exact-SHA acceptance of
  W2-B. (The prior OD-W2-WM pre-gate is WITHDRAWN as circular.)
- The prior separate OD-W2-N3 is WITHDRAWN — OD-W2-AUTH freezes §J.

**Remain undecided / outside current authorization unless separately
approved:** OD-PDVG-12 (`Why this matters` render); RVR-7 Wave-3
implementation (and OD-W2-D-P6-18 at that gate); RVR-8; OD-PDVG-10
meaning-adaptive questioning; user-feedback ownership.

## Q. Product-value acceptance — honest scope

Wave-2 must demonstrate material improvement in: decision usefulness
(stateful, evidence-bound — alternatives, visible evidence requirements,
explicit supported elimination, unresolved stays unresolved, preference
separate, bounded recommendation only when evidence permits, provenance
visible — never a generic pros/cons table); prior-answer responsiveness;
project/domain responsiveness; technical-user respect (conditional on §G's
repaired evidence basis and §J's outcome — stated, not assumed); reduced
repetitive questioning; unknown handling; perceived responsiveness ("the
system knows I am deciding between A and B"). **Wave-2 claims NO Arabic
parity closure** (Wave 3). Evaluator-facing evidence only; no subjective
scoring in canonical logic. Preserved: **T1-C′ future real-user validation
must measure perceived differentiation, return intent, decision impact,
clarity/usefulness, trust, and perceived responsiveness — RVR-8/S2 is not
proof of adoption or retention.** TTV metrics continue as measurement
hypotheses only (≤12/≤5/≤15/±1 remain unfrozen pending Owner approval after
observing remediated behavior).

## R. Material Gap & Improvement Sweep (fresh; corrected)

| # | Finding | Class |
|---|---|---|
| S-1 | Questions ignore prior answers/state (S2 R2/R6) | COVERED BY WAVE-2 (W2-B/W2-C) |
| S-2 | No decision representation in main journey; DW separate + hard-coded | COVERED BY WAVE-2 (W2-ID → W2-A) |
| S-3 | WS10 content absent | COVERED BY WAVE-2 (W2-C, scope §I) |
| S-4 | Experienced users get novice-phrased repeats | COVERED BY WAVE-2 (W2-B; conditional on §G repair — disclosed) |
| S-5 | Arabic journey substantively English (R3/R4/R7/R8) | EXISTING WAVE-3 OWNER (RVR-7/OD-R4) — NOT Wave-2 |
| S-6 | Accept Risk reachable with zero substantive attempts | COVERED BY WAVE-2 (W2-D, §F) |
| S-7 | Lapsed acceptance unexplained after correction | COVERED BY WAVE-2 (W2-D, §K) |
| S-8 | W1-N3 residual relevance false-negative | COVERED BY WAVE-2 (W2-C, conditional §J) |
| S-9 | Meaning-adaptive understanding of novel phrasing | EXISTING TIER-2 OWNER (OD-PDVG-10 — undecided; NOT Wave-2) |
| S-10 | Ledger `quality` aggregate misleads any answer-quality reader; substance/relevance results not durably recorded; export drops content/quality | OBSERVATION + partially COVERED BY WAVE-2 (§G recomputation; record-semantics change itself OWNER DECISION REQUIRED) |
| S-11 | No durable question-identity carrier for decision capture | COVERED BY WAVE-2 (W2-ID) |
| S-12 | User-feedback capture | **NO CURRENT OWNER / OWNER DECISION REQUIRED** (PDVG-01 T2-D bounded capture increment; no existing OD family; outside Wave-2; no workstream auto-created) |
| S-13 | **MG-8** — seed problem statement not captured as `known_problem` (`seed_idea_text` durably recorded at `/start` but `known_problem` populates only from relevance+≥REASONED answers). Evidence status: **OBSERVATION — cause unproven** (S2 evidence). **Implementation locus: `progression/intake seam`** (an architectural code location, `progression_loop.py:879, 1114-1115` `[REPO]`). **Governance owner: `NO ESTABLISHED OWNER`** — no committed authority assigns MG-8 to any workstream/owner; the intake seam is where a fix would land, not who may authorize it, and MG-8 is not force-fitted into RVR-6, WS6, Path-N, or any adjacent owner | Disposition: **OWNER DECISION REQUIRED before any change to seed→`known_problem` / canonical evidence / maturity semantics**. Wave-2 may measure, diagnose, and include evidence in W2-B/W2-C packs, but MUST NOT silently change canonical intake/evidence/maturity semantics; no workstream auto-created |
| S-14 | Over-questioning if suppression and ordering disagree | COVERED BY WAVE-2 (single-policy test) |
| S-15 | Trust/provenance regression risk on new render surfaces | COVERED BY WAVE-2 (provenance visible + prohibited-status guards, §D) |
| S-16 | Generic-chatbot feel of exit prompts post-adaptivity | POST-RELEASE (re-evaluate at RVR-8) |

No new workstream is created by this sweep.

## S. Determinism / duplicate-owner protections

`Canonical deterministic routing → Adaptive presentation` —
`[PROPOSED WAVE-2 INVARIANT]`: first introduced by this contract (it appears
in no committed repository document); it becomes binding only when this
contract is Owner-authorized and merged; it restates, in contract language,
the Owner-frozen remediation architecture's determinism boundary. No history
is rewritten to claim otherwise. Prohibitions unchanged: no free-form
model-generated canonical questions; no model-based hidden routing; no
opaque persona inference; no nondeterministic canonical scoring; no
stochastic decision selection; no second canonical decision model; any
future AI assistance outside canonical truth and separately governed.
Duplicate-owner protections: one risk-acceptance mechanism; one correction
explanation owner; one intent vocabulary/registry; one routing policy layer;
one decision-semantics owner; one canonical export model — each enforced by
a named test.

## T. Candidate lifecycle / Grill evidence

Prior candidates `89736887…` and `fd2e1052…`: immutable reviewed evidence
(`refs/reviewed/wave2-contract-89736887`,
`refs/reviewed/wave2-contract-fd2e1052`); neither amended, rebased,
force-pushed, published, PR'd, or merged. This final candidate: parent =
re-verified tip `e02d175b…`; governance/contract file only; no product/test
implementation; narrow-repair Mandatory Grill run before return:
(A) `superseded_by is None` verified as the canonical active-record rule the
correction seam itself documents (`session_reconstruction.py:19, 227, 235`
`[REPO]`); (B) no second unlock path — availability is computed only by the
one helper consumed by the one route and the one affordance, with a named
test; (C) live-gate placement keeps historical replay reproducible (writer
unchanged); (D) no "last OPEN" event is needed under active-set semantics —
supersession removes lapsed attempts from the active set; (E) MG-8 has no
established governance owner in any committed authority (re-verified); (F) no
new owner/workstream introduced by this repair; (G) no authorization boundary
changed; (H) Wave-2 remains design-sufficient after the corrections. All
previously reviewed PASS findings preserved unchanged. SHA-preserving bundle
created; not published, no PR, no merge. Owner decision on §P is the next
lifecycle step.

---

`PRIOR CANDIDATE 89736887: IMMUTABLE REVIEWED EVIDENCE`
`PRIOR CANDIDATE fd2e1052: IMMUTABLE REVIEWED EVIDENCE — SUPERSEDED BY NARROW REPAIR`
`NEXT GATE: OWNER REVIEW AND AUTHORIZATION OF THIS CORRECTED WAVE-2 CONTRACT CANDIDATE`
