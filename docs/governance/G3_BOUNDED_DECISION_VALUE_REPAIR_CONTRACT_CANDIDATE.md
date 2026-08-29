# G-3 — BOUNDED DECISION-VALUE REPAIR — IMPLEMENTATION CONTRACT (CANDIDATE)

**STATUS AT CREATION: `CONTRACT CANDIDATE — NOT AUTHORITATIVE`.** Created on the authoritative base
`39a966995d83ce72ba64a263c048d803f6d95061` (PR #597 — the RVR-8 formal-closure merge; parents
`1f3d9d14b3b645df9595889861140910d63b918c` + `e50723e3c9f715dc55cc42d01eca8bec5b141e5a`, tree
`e68c2e942c6f23930b66063ca906a9b67bd62f72`), verified live from Git at this gate with **0 commits
after it** `[EXEC]`.

This document is a **contract freeze only**. It authorizes nothing. `IMPLEMENTATION AUTHORIZED: NO` ·
`IMPLEMENTATION STARTED: NO`. Every candidate-era statement below is scoped to this gate's freeze and
therefore stays true as a statement about that moment once the gate resolves (repaired AIC semantics,
§15).

**Candidate lineage (disclosure only — no new tracker is created).**

| SHA | Status |
|---|---|
| `06fc86b33cf1a13740cc6cea63ea2ab16435dc2d` | NON-SELECTED EARLIER CANDIDATE / NO EVIDENCE AUTHORITY |
| `daa7c21962645c9c1bc9f591d4dac94e426f9114` | SUPERSEDED PRE-AUTHORSHIP FREEZE / NO EVIDENCE AUTHORITY |
| `db5fb1aa9f73bfb2a21df88d1386a6274902660b` | **INDEPENDENTLY REVIEWED / `REPAIR REQUIRED — BOUNDED SAME-BASE SIBLING` / IMMUTABLE REVIEW EVIDENCE** — not authoritative, not Owner-accepted, not on origin by design (transferred by SHA-preserving bundle only) |
| `27ae273f7b35e909dfd5e275ac7d862b4249db52` | **LEAD REVIEWED / `REPAIR REQUIRED — ONE BOUNDED SAME-BASE SIBLING` / NOT INDEPENDENTLY REVIEWED** — its BD-1 repair is preserved here; three further defects corrected |
| `87dc507e0a2a339333ff2abf6583f7c4cfe1df1b` | **LEAD REVIEWED / `REPAIR REQUIRED — ONE FINAL BOUNDED SAME-BASE SIBLING` / NOT INDEPENDENTLY REVIEWED** — its four repairs are preserved here; the visibility-vs-comparison-membership family corrected (§18) |
| *this document's commit* | FRESH SAME-BASE SIBLING / NOT YET INDEPENDENTLY REVIEWED |

**What this repair changes, and why.** Independent Review found **BD-1 — user withdrawal was
pre-committed as system elimination**: the reviewed candidate froze `withdrawn → option_status =
eliminated` in §6/S-1 and A-5 while escalating only the accompanying basis to D-G3-1. This sibling
removes that mapping, unifies status and basis into one D-G3-1 decision, conditions A-9 on that
decision instead of pre-deciding it, adds `A-22` (withdrawal semantic truth) and `A-23` (canonical
mutation discipline), and removes the `eliminated`-without-basis fallback. **`db5fb1aa…` is not this
candidate's Git parent** — it is documentary input only. The Lead then reviewed the resulting sibling
`27ae273f…` and returned `REPAIR REQUIRED — ONE BOUNDED SAME-BASE SIBLING` on three further defects
(a stale §18 fallback contradicting §12/`A-23`; an S-1 title pre-deciding `non-active`; and an S-2
pre-commitment of the withdrawal-reason carrier), plus one non-blocking citation correction. **This
The Lead then reviewed `87dc507e…` and returned `REPAIR REQUIRED — ONE FINAL BOUNDED SAME-BASE
SIBLING` on one remaining blocking family: **several clauses still collapsed *product visibility* into
*FDC comparison membership***, which would have decided D-G3-1 Option B by construction. This candidate
adds the explicit two-set distinction (§6.0), repairs `S-1`, `S-5`, `A-4`, `A-5` and `A-23` against it,
adds `A-24`, and cleans up the S-2 sequencing. **This candidate is a fresh same-base sibling of
`87dc507e…`, not its descendant**; `db5fb1aa…`, `27ae273f…` and `87dc507e…` are all documentary review
evidence only.

---

## §1. Objective, and the exact measured failure it addresses

RVR-8 closed as `COMPLETED VERIFICATION — VALID EVIDENCE RETURNED — NEGATIVE / MIXED PRODUCT RESULT`,
and `T1-A′` stays **OPEN**. Its measured, registered cause on the release-value side is precise
`[REPO — RVR_8_FORMAL_CLOSURE_RECORD.md §5, DEFERRED_OBLIGATIONS_REGISTER.md L150]`:

> **criteria 5 and 6 FAIL in all 8 records** — *alternatives bounded and truthfully classified*;
> *elimination or qualification reasons explicit* — and **candidate representation / comparison is
> absent on the evaluated Path-N surface**.

**Objective of the eventual implementation:** on the **existing served Path-N surface**, represent the
alternatives the inventor has **already declared** as a bounded, truthfully classified **rendered
alternative set** (§6.0 A — which alternatives are FDC comparison-eligible is D-G3-1, not settled by
this objective), each carrying its recorded evidence state and an explicit qualification /
elimination / retention / cannot-decide reason derived from canonical recorded evidence — or a
truthful statement that the evidence does not support comparison.

**What this contract is NOT.** It is not a new comparison engine, not a database, not a second
decision owner, not readiness, not adaptive questioning, and not a third S2 run.

---

## §2. Exact owner map — reconstructed from the repository at this base, not assumed

Reconstructed per the Owner's §4 instruction. Every row is a **repository fact** at
`39a96699…`; none is inherited from the RVR-8 record's prose.

| Concern | Actual implementation owner at this base | Evidence |
|---|---|---|
| **Canonical decision semantics** (candidates, statuses, dispositions, readiness, blocking) | **FDC-001 `DecisionRecord`** — *"remains the sole canonical decision-semantics owner"* — quoted verbatim from `engine/decision_composition.py:19` and `engine/idea_state.py:126`; Owner decision **OD-R3** (*"as the sole decision-semantics owner"*); W2-ID candidate §36. (`engine/decision_workspace.py:521` **defines** `class DecisionRecord` and does **not** carry the quoted sentence — cited here as the class definition only.) |
| **Comparison / readiness ownership** | **FDC-001 `DecisionRecord`**, stated verbatim as *"the sole comparison/readiness owner"* by the W2-C module that defers to it | `engine/intent_serving.py:35-39` |
| **Durable truth / provenance carrier** | **`IdeaState` `AssertionRecord` ledger** — durable carrier, explicit user-action ledger, provenance/history mechanism; expressly **NOT** a second decision-semantics model | `engine/idea_state.py:212-241`; W2-A contract §6 |
| **User-declared alternatives** (declare / refine / withdraw) | **W2-A / RVR-4** canonical mint wrappers over the fail-closed carrier | `engine/decision_composition.py:64-102`; `engine/idea_state.py:127-134, 513-546` |
| **Path-N decision composition seam** (ledger → `DecisionRecord`) | **`engine/decision_composition.py`** — `compose_decision_records()` / `decision_capture_view()`; pure, derived, never persisted | `engine/decision_composition.py:106,147` |
| **Served Path-N decision surface** | **`web/app.py` `_decision_capture_view_safe`** → `web/templates/session.html:564-619`, `web/templates/deliverable.html:583-604` | `web/app.py:2912, 3020, 3343` |
| **Deliverable assembly** | **`engine/deliverable_assembler.py`** — and the composed decision state is deliberately **NOT** part of the canonical deliverable package (assembler untouched by W2-A) | `web/templates/deliverable.html:578-581` |
| **Per-gap evidence state** | `IdeaState.Gap.evidence` / `Evidence` (quality · provenance · validation_status), four orthogonal Increment-2 axes | `engine/idea_state.py:183-210, 44-77` |
| **Primary next action on the alternatives transition** | **W2-B / RVR-6a** `TRIGGER_MULTIPLE_ALTERNATIVES` → `primary_action="decision_refine"` (action slot only; question slot untouched); derived from the ledger, **not** from `compose_decision_records` | `engine/progression_loop.py:1363,1503,1636-1638`; `web/templates/session.html:292` |
| **Within-gap serving / intent coverage** | **W2-C / RVR-6b** `engine/intent_serving.py`; read-only deference to FDC-001 | `engine/intent_serving.py:20-46` |
| **EN/AR UI chrome** | **`web/ui_text.py`** — the single central presentation-only catalogue; `UI_W2A_*` pairs already exist | `web/ui_text.py:47, 898-958` |
| **ODS-001** | **Nothing.** `SO-5 — "Not designed. Not authorized."` Its only code footprint is the deliverable's material-selection and manufacturing DEFERRED notes | `GOVERNANCE_COMMITMENT_MAP.md §SO-5`; `engine/deliverable_assembler.py:1008,1010` |
| **Decision Snapshot** | **No implementation exists.** `decision_snapshot` / `DecisionSnapshot`: **0 occurrences** across `engine/ web/ tests/ schemas/ database/ scripts/` `[EXEC]`. It is a governance-named surface in the reconciliation inspection set only. The product's `keep-snapshot` route is the unrelated G-UX-SNAPSHOT-DECISION per-session output selection | `[EXEC]`; `web/app.py:3520` |
| **Readiness levels (TRL/MRL/IRL/SRL)** | **No implementation exists** — 0 occurrences across `engine/ web/` `[EXEC]` | `[EXEC]` |
| **G-3 governance owner** | **`T1-A′`** — routed there by the authoritative RVR-8 closure; **no new owner is created by this contract** | `RVR_8_FORMAL_CLOSURE_RECORD.md §6 G-3`; register L150 |

**RVR-4 / W2-A is NOT reopened.** It delivered *user-declared* alternatives and its row is `CLOSED`.
This contract builds on its merged, authoritative output; it does not re-litigate it, does not change
its frozen vocabulary (§2), does not change its frozen `decision_context_root` field (§3), and does
not alter its identity contract (§7). **`RVR-4 REOPEN REQUIRED: NO`.**

---

## §3. The mechanical cause of criteria 5/6 — established, not inferred

Four findings at this base, each mechanically checked. Together they explain the measured failure
without any appeal to a missing engine.

**(a) Withdrawn candidates vanish rather than being represented at all.**
`compose_decision_records` builds the candidate set from **ACTIVE `decision_alternative_declared`
chain heads only**; a withdrawn chain simply *"leaves the composed candidate set"*
(`engine/decision_composition.py:122-127`; `withdraw_alternative` at `:93-102`). A withdrawn
alternative is therefore **not represented at all** — which is exactly criterion 5's *bounded and
truthfully classified* failing. **The defect is the disappearance, not the absence of an `eliminated`
label**: naming the fix "represent it as eliminated" would pre-commit the very mapping BD-1 rejects
(D-G3-1). What criterion 5 needs is representation plus truthful classification, whatever canonical
form D-G3-1 resolves that classification to take.

**(b) The withdrawal reason is accepted by the route but never collected by the form.**
`POST /session/<sid>/decision/withdraw-alternative` reads a `reason` form field and passes it to
`withdraw_alternative(...)`, which stores it as the withdrawal record's `content`
(`web/app.py:3500-3517`; `engine/decision_composition.py:93-102`). **The served withdraw form submits
only `answer_token` and `supersedes_record_id`** (`web/templates/session.html:583-587`), so the reason
is **always empty in practice**. That is criterion 6's *elimination reasons explicit* failing, and its
cause is a missing field on an existing form — not a missing capability.

**(c) The composed candidate carries name only.**
`Candidate(candidate_id=…, name=…)` is constructed with the class defaults, so `option_status` is
always `active` and `disposition_reason` / `disposition_basis` are always `None`
(`engine/decision_composition.py:132-135`; `engine/decision_workspace.py:347-353`). The composition
seam populates **no** inputs, constraints, gaps or evidence, so readiness is
`insufficient_information` *by construction* — as `decision_composition.py:21-22` itself states.

**(d) The served surface renders no per-candidate state.**
Both templates render the candidate **name** and nothing else; the only readiness text is the single
`UI_W2A_READINESS_NOTE` shown when readiness is `insufficient_information`
(`session.html:575, 595`; `deliverable.html:592, 597`). No status, no reason, no evidence state.

**Consequence for scope.** The bounded comparison vocabulary the product needs — `option_status`
(`active` / `eliminated` / `deferred` / `blocked`), `disposition_reason`, `disposition_basis`,
`BlockingReason` incl. `candidate_not_yet_comparable`, and the four-value ordered readiness table that
can never emit a winner — **already exists, merged and authoritative, inside the canonical decision
owner** (`engine/decision_workspace.py:75-111, 347-353, 642-752`). The repair is a **projection and
rendering** repair, not a new capability.

---

## §4. ODS-001 adjudication — falsified, per the Owner's §7 instruction

The preflight conclusion was tested for falsification rather than adopted.

**Falsification attempt.** ODS-001 is defined in the repository as *"Options Database"* / *"Structured
database of components, materials, and manufacturing options"*, `SO-5 — Not designed. Not authorized.`
`[REPO — GOVERNANCE_COMMITMENT_MAP.md §SO-5]`, and as *"Options Database for materials and
manufacturing"* / *"materials, components, and manufacturing"*
`[REPO — INVENTORAI_PROJECT_STATE_FREEZE_v1.2.md §13/§15/§16]`, deferred post-MVP by
`STRATEGIC_PRODUCT_VISION.md §9`. Its **entire** runtime footprint is two deliverable notes:
`category_b_material_selection` and `category_c_manufacturing`, each `"Requires Options Database
(ODS-001). Not in the current MVP."` `[REPO — engine/deliverable_assembler.py:1008,1010]`.

**Result.** Every committed definition scopes ODS-001 to a **catalogue of external component /
material / manufacturing options**. This repair compares **the inventor's own already-declared
candidate mechanisms** using **evidence they themselves recorded**. It retrieves nothing, catalogues
nothing, and supplies no option the inventor did not declare. The two surfaces are disjoint, and no
committed source assigns bounded technical-decision comparison to ODS-001.

    ODS-001 REQUIRED: NO
    ODS-001 ACTIVATION REQUIRED: NO

The two deliverable DEFERRED notes remain **byte-unchanged** and keep their meaning. This contract
neither activates, designs, nor authorizes ODS-001, and the deferral in
`STRATEGIC_PRODUCT_VISION.md §9` is untouched.

---

## §5. FDC-001 adjudication — the boundary that decides whether this gate is safe

**The lane hold, stated exactly.** The broader Decision Workspace Path-T lane is held under S2 §13
`PRESERVE UNMODIFIED AND PAUSE`. **That hold has already been partially and explicitly lifted by the
Owner**, and the lift is `CLOSED — evidence verified` in the register `[REPO — register L127]`:

> **OD-W2-DW-LIFT**, exercised in W2-A contract §5, authorizes exactly three things — (1) **reuse of
> the existing FDC-001 `DecisionRecord` class by the Path-N deterministic decision-composition seam**;
> (2) default-preserving constructor generalization; (3) **reuse of the class vocabulary required by
> the bounded composition seam** — while preserving as forbidden: a second decision journey, a new
> journey owner, broader Path-T activation, live Decision Workspace behaviour change, existing DW
> endpoint changes, DW UI activation, persistence expansion, a second canonical decision model, and
> unrelated DW capabilities.

**Therefore the class is already inside the served Path-N runtime**, lawfully: `decision_composition`
imports `Candidate, DecisionRecord` and the composed record is rendered on the session and deliverable
surfaces today `[REPO — decision_composition.py:36; app.py:2912,3020]`.

    FDC-001 ACTIVATION REQUIRED: NO

**Precisely what "NO" means here, with nothing hidden.** The repair uses **only** permission (1) and
permission (3): the same class, the same vocabulary, projected more completely by the same seam. It
creates **no second journey**, changes **no** `/decision-workspace` endpoint or template, activates
**no** DW UI, expands **no** persistence, and creates **no** second canonical model. The
`PRESERVE UNMODIFIED AND PAUSE` hold on broader DW Path-T work stands entirely.

**The one governance item this contract deliberately surfaces rather than assumes** `[OPEN — LEAD/OWNER]`.
OD-W2-DW-LIFT permission (3) is scoped to *"the class vocabulary **required by the bounded composition
seam**"*, and was exercised for the vocabulary **W2-A** required. This repair needs a **larger subset
of the same already-lifted vocabulary** (`option_status`, `disposition_reason`, `disposition_basis`,
`BlockingReason`, and — subject to §7 D-G3-2 — `add_input`). Whether that is *within* permission (3) as
written, or needs a bounded **extension** of the same exercised lift, is an **Owner reading of the
Owner's own instrument**, not a determination this candidate may make for itself.

> **`REQUIRED AT THE IMPLEMENTATION GATE: an explicit Owner confirmation or bounded extension of
> OD-W2-DW-LIFT permission (3) covering the §7 vocabulary subset.`**

This is recorded **as a precondition of implementation authorization**, not silently assumed. It is
**not lane activation**: under either reading the lane stays `INACTIVE`. Because it is disclosed here
and gated, this contract does **not** silently activate FDC-001, and the Owner's §8 `STOP` condition
(*"a contract that silently activates it"*) is **not** met.

---

## §6. Minimum scope — DEPTH BEFORE BREADTH

The smallest repair that can move criteria 5 and 6, expressed as behaviour. **No implementation is
authorized; this is the frozen scope an implementation gate would be bound to.**

### §6.0 — The two sets this contract must not conflate

Lead review of `87dc507e…` found that several clauses collapsed **being visible to the inventor** into
**participating in FDC-001 comparison semantics**. They are different concepts, and only the first is
frozen by this contract.

| | **A — BOUNDED RENDERED ALTERNATIVE SET** | **B — FDC COMPARISON-ELIGIBLE CANDIDATE SET** |
|---|---|---|
| What it is | The product-visible set that lets the inventor see what happened to **every alternative they declared**, a withdrawn one included | Membership of `DecisionRecord.candidates` — what participates in comparison semantics, readiness, accounting, blocking reasons and disposition |
| Frozen here | **YES** — `S-1`, `S-4`, `A-4a`, `A-5` | **NO** — a withdrawn alternative's membership is **D-G3-1** |
| Derived from | The canonical `AssertionRecord` ledger, projected deterministically | FDC-001 `DecisionRecord`, **unchanged** |

**Both are deterministic projections of the SAME canonical ledger.** This is a semantic distinction —
**not** a second decision model, a second candidate store, a second comparison engine, a second
persistence layer, or a lifecycle database. `A-17` (no duplicate canonical owner), `A-12`
(determinism), `A-13` (reconstruction) and `A-14` (provenance) bind **both** sets unchanged, and
`_compute_readiness()` is not edited.

**Why the distinction is mechanically load-bearing, not stylistic `[EXEC at this base]`.** Membership in
`DecisionRecord.candidates` is **itself a decision-semantic act — there is no inert membership**:

- `_all_candidates_accounted_for()` iterates **every** member: an `active` member must be `_covered()`
  by ≥1 decision-relevant input or constraint, and a **non-`active`** member must carry a
  `disposition_basis` (`decision_workspace.py:664-673`). **Both branches carry consequences**; there is
  no third, neutral branch.
- `_min_comparison_context()` counts **`active` members** — a withdrawn alternative held `active` would
  count toward the *"at least two active candidates, each covered"* threshold that gates readiness
  rule 1 (`:654-662`).
- `_derive_blocking_reasons()` emits `candidate_not_yet_comparable` **naming the candidate** for every
  uncovered `active` member (`:745-750`) — so a merely-visible withdrawn alternative could manufacture
  a blocking reason it did not earn.
- `_validate_candidate_ids()` rejects any input or constraint that references a non-member
  (`:631-640`) — so a non-member cannot be quietly half-included through input scope either.

Therefore **defining the rendered set as identical to `record.candidates` would decide D-G3-1 by
construction.** This contract refuses that in **both** directions: it neither admits a withdrawn
alternative into the comparison set nor excludes it. It freezes only that the inventor can still see it.

**S-1 — A user-withdrawn alternative stays VISIBLE instead of vanishing; neither its canonical
representation nor its comparison membership is frozen here.** A withdrawn alternative chain **remains
visible, bounded, reconstructable and provenance-traceable in the served decision context** rather than
disappearing. An alternative the inventor has not withdrawn is unaffected and stays `active`. The
**bounded rendered alternative set** (§6.0 A) stays bounded by the ledger: one entry per founding
alternative root, no fabricated entry, ever.

> **This contract does NOT freeze `withdrawn → option_status = eliminated`.** The earlier candidate
> `db5fb1aa…` did, and Independent Review found that a blocking defect (**BD-1**). The requirement
> frozen here is **semantic, not enumerative**: a user-withdrawn candidate must be **truthfully
> distinguishable from an evidence-based system elimination** in canonical representation and on every
> served surface. Which canonical representation carries that truth is **D-G3-1**, unresolved below.
> **Dropping withdrawn alternatives from the rendered set is NOT an acceptable resolution** — that is
> the current behaviour (§3) and it is the criterion-5 failure this repair exists to remove.
>
> **It equally does NOT freeze that a withdrawn alternative remains a member of the FDC
> comparison-eligible candidate set (§6.0 B).** Comparison membership — and therefore any readiness,
> accounting, blocking-reason, owner-preference or disposition consequence — is **part of D-G3-1**,
> which explicitly keeps **Option B** (withdrawal as lifecycle/provenance state: visible, but excluded
> from the comparison set) open. `NO SILENT DISAPPEARANCE` must never be read as
> `MANDATORY FDC COMPARISON MEMBERSHIP`.

**S-2 — Capture the withdrawal reason and render it truthfully; the CARRIER is NOT frozen here.** Add
the missing `reason` input to the existing served withdraw form. The route and the ledger already
accept and store it (§3(b)).

**Frozen here — the product requirement:** the user's withdrawal reason (a) remains **durable and
provenance-traceable** on the canonical `AssertionRecord` ledger, where the withdrawal event already
lives; (b) is rendered **verbatim** on the served surfaces where recorded; (c) renders the governed
*reason not recorded* copy where absent; (d) is **never fabricated**; and (e) is **never given an
epistemic or system-judgment upgrade** — it is the inventor's stated rationale for a lifecycle act, not
a system finding and not evidence.

**NOT frozen here — the semantic carrier.** Whether that reason populates the decision-semantic
`disposition_reason`, a lifecycle/provenance projection, or another already-authorized field is
**part of the unified D-G3-1 decision**, which covers **status + basis/provenance + withdrawal-reason
carrier** together. Placing a lifecycle rationale into a decision-disposition field would itself
mischaracterise lifecycle metadata as disposition semantics — the same class of error as BD-1.

**Sequencing.** There is **no implementation-time *"until D-G3-1 resolves"* state**: §7 forbids the
implementation gate from proceeding until D-G3-1 is resolved, so no implementation may ever run under
an interim carrier. **Once D-G3-1 is resolved and implementation is separately authorized, the served
withdrawal rationale must derive truthfully from the canonical withdrawal ledger event, unless the
authorized D-G3-1 resolution explicitly selects another already-existing canonical carrier.** A
`DecisionRecord` reason mapping is used **only if D-G3-1 authorizes one.** No new carrier is invented
and no second owner is created; (a)–(e) above hold under every resolution.

**S-3 — Derive per-candidate evidence state from the candidate's own chain.** Each candidate is a
supersession chain rooted at its founding `record_id`; its refinement records are the inventor's own
recorded statements about that candidate, already durable, already `OWNER_STATED`, already
reconstruction-stable. Evidence state is derived **only** from that chain — **no new ledger field, no
new attachment mechanism, no schema change**. This is precisely the evidence the served product already
tells the user it is collecting: *"Recording what you know about each alternative … gathers the evidence
a future comparison will need. No comparison has started yet."* `[REPO — ui_text.py:993-998]`.

**S-4 — Render per-alternative state on the existing served surfaces.** For each member of the
bounded rendered alternative set (§6.0 A): name (verbatim, never translated), its **truthful state**
(active, user-withdrawn, or whatever D-G3-1 authorizes — never asserted as an evidence-based
elimination, and **not necessarily the canonical `option_status`**, which exists only for comparison-set
members), reason (or *not recorded*), and evidence state — on
`session.html` and `deliverable.html`, inside the existing `UI_W2A_*` sections, via new governed EN/AR
`ui_text.py` pairs. No new page, no new route family, no new journey.

**S-5 — Truthful comparison outcome and a truthful refusal — over the AUTHORIZED comparison
representation only.** The comparison verdict is whatever the **unchanged** FDC-001
`_compute_readiness()` ordered table returns. **No new readiness algorithm is created and the existing
ordered rule table is not edited.** What this scope item additionally freezes is the table's *input
membership*: it operates **only over the canonical comparison representation that D-G3-1 authorizes**
(§6.0 B) — not over everything the product is required to keep visible (§6.0 A).

> **A user-withdrawn alternative must not alter readiness, blocking reasons, accounting or comparison
> eligibility merely because the product is required to keep it visible.** If D-G3-1 authorizes such
> participation, the exact canonical semantics of that resolution must support it — status,
> basis/provenance, and the invariants they imply. If D-G3-1 does not, visibility remains a derivation
> from the ledger and **no comparison membership is fabricated in order to produce it.**

Where the evidence does not support comparison, the surface says so — the repository-authorized
equivalent of `INSUFFICIENT EVIDENCE TO COMPARE` already exists as the `insufficient_information`
status and the governed `UI_W2A_READINESS_NOTE` copy. `blocking_reasons` — including the existing
`candidate_not_yet_comparable`, which names the specific candidate that lacks inputs — is rendered as
the explicit per-candidate *cannot yet decide* reason.

**S-6 — One primary next action.** The existing W2-B `decision_refine` action block remains the single
primary CTA on the alternatives transition. **No second CTA owner is created.**

**Excluded from minimum scope, explicitly:** materials database · manufacturing-options database ·
commercial alternatives · supplier recommendations · CAD · simulation · adaptive questioning ·
readiness scoring · any change to the canonical deliverable package assembler.

---

## §7. The bounded decision points an implementation gate must resolve FIRST

These are named rather than settled, because settling them silently would be exactly the semantic
drift this repository forbids.

| Id | Question | Why it cannot be settled here |
|---|---|---|
| **D-G3-1 (UNIFIED — status, basis/provenance AND reason carrier: one decision)** | **How is a USER WITHDRAWAL truthfully represented canonically — status, basis/provenance, *and* the carrier of the user's withdrawal reason?** No part may be settled alone: status without basis is rejected by the canonical mutation API; basis without status misdescribes the act; and assigning the reason to a decision-semantic field would pre-commit withdrawal to disposition semantics. Options tested below. | The canonical vocabulary has **no user-withdrawal member on either axis**, and repository authority ties `eliminated` to requirement-incompatibility. **Owner decision required.** |
| **D-G3-2 (full choice set)** | May a candidate's recorded refinement text be projected as a decision-relevant `ClaimItem` so `_covered()` can become true and readiness can leave rule 1 — and if so, under which `claim_class` **and** `provenance`? | A semantic assignment CLAUDE.md forbids making silently. Full repository-authoritative choice set enumerated below; none is pre-selected. **Owner decision required.** |
| **D-G3-3** | Is criterion 5/6 satisfaction intended **with** readiness advancing past `insufficient_information`, or is truthful classification + explicit reasons sufficient with readiness unchanged? | Determines whether D-G3-2 is in scope at all. The narrower reading (S-1…S-6 without D-G3-2) is the **DEPTH BEFORE BREADTH** default this contract recommends. **Lead/Owner adjudication.** |
| **D-G3-4** | Does the composed decision state enter the **canonical deliverable package**, or stay a derived render-only projection as W2-A deliberately left it? | The assembler is a canonical owner; entering it is a materially larger change. **Recommended: stay derived.** |

### D-G3-1 — the four options, each tested against repository authority (none pre-selected)

**Load-bearing repository facts `[REPO/EXEC at this base]`.** `option_status` is exactly
`active` · `eliminated` · `deferred` · `blocked` (`decision_workspace.py:73-77`). `disposition_basis`
is exactly `incompatible_with_recorded_requirement` · `deferred_pending_input` ·
`blocked_by_evidence_gap` (`:79-82`). `dispose_candidate()` raises
`DecisionError("disposition_basis required for non-active status")` (`:1044-1049`).
`_all_candidates_accounted_for()` fails accounting for any non-active candidate lacking a basis
(`:664-673`). The FDC-001 specification titles its §13 **"Candidate elimination is contextual, not a
validity verdict"** and ties elimination to a **confirmed mandatory owner requirement**, which "may
move a candidate to `option_status=eliminated`" with
`disposition_basis = incompatible_with_recorded_requirement`
(`docs/product/FDC-001_FIRST_INCREMENT_IMPLEMENTATION_SPECIFICATION.md` §13 and :355-359).

| Option | Statement | Disposition against repository authority |
|---|---|---|
| **A** | An existing status+basis pair already represents user withdrawal truthfully. | **NOT SUPPORTED.** All three basis values are evidence/requirement-based. `deferred` + `deferred_pending_input` means *awaiting input* — it may coincidentally fit a withdrawal for lack of information, but is false for preference, accidental entry, changed intent or abandonment, so it is not a general representation. `blocked` + `blocked_by_evidence_gap` likewise. |
| **B** | Withdrawal is **lifecycle/provenance state**, distinct from an evidence-based disposition, and should not be expressed as a decision disposition at all. | **OPEN AND PLAUSIBLE.** The ledger already records withdrawal as a lifecycle event (`decision_alternative_withdrawn`), and W2-A treats the composed record as derived. This option keeps the canonical decision vocabulary untouched. Its cost: B must specify **membership first, then status**. If a withdrawn chain is a member of `DecisionRecord.candidates` it needs *some* `option_status`, and **membership is itself a decision-semantic act `[EXEC]`** (§6.0): an `active` member must be `_covered()`, a non-`active` member must carry a basis, an uncovered `active` member emits `candidate_not_yet_comparable`, and an `active` member counts toward the rule-1 threshold. B must therefore state explicitly whether a withdrawn chain (i) remains a member with a stated status, or (ii) is excluded from the comparison set while remaining in the rendered set. **No reading of this contract supplies that answer by default, in either direction.** |
| **C** | A **bounded vocabulary extension inside the existing `DecisionRecord` owner** is required (e.g. a withdrawal-specific basis and/or status member). | **OPEN AND PLAUSIBLE.** A vocabulary residual inside the canonical owner is **not** automatically a new owner. But it edits a canonical enum, so it requires explicit Owner authorization; no permission exercised to date covers it. |
| **D** | Another already-authorized canonical representation exists. | **NONE FOUND** at this base. |

**No option is selected by this contract.** The implementation gate must not proceed until D-G3-1 is
resolved. **Neither outcome is pre-favoured:** vocabulary must not be added merely because it is
convenient, and withdrawal must not be force-fitted into an evidence-based state merely to preserve the
existing enum.

**Latent coupling disclosed (NON-BLOCKING FOR CURRENT PATH-N).** `_owner_preference_conflicts()`
treats `option_status in (ELIMINATED, BLOCKED)` as a conflict with a recorded owner preference
(`decision_workspace.py:753-760`), which has readiness consequences. This is **latent, not live**:
the guard returns `False` whenever `owner_preference` is unset (`:754-755`), and the Path-N composition
seam **never sets `owner_preference`** (0 occurrences in `engine/decision_composition.py` `[EXEC]`) —
it is reachable only through the inactive `/decision-workspace` lane. It is **not a second blocker
today**, and is disclosed here solely because the D-G3-1 status choice would acquire mechanical
consequences if that path ever became reachable.

### D-G3-2 — the full repository-authoritative choice set (none selected)

`claim_class` members are exactly `observed_fact` · `owner_requirement` · `operator_reported_result` ·
`assumption` · `external_reference` · `unsupported_claim` · `missing_information` · `constraint`
(`decision_workspace.py:39-52`). Storable as an input: all except `missing_information`, which "is only
ever a Gap, never a stored input" (`:47`, `:54-58`). Separately, `provenance` is
`seeded_owner_context` · `operator_entered` · `platform_proposed` · `derived_by_rule` (`:61-67`).

**A correction the earlier candidate did not carry:** `OPERATOR_REPORTED_UNVERIFIED` and
`EXTERNAL_REFERENCE_UNVERIFIED` are **display labels, not selectable claim classes** — they are
returned by `ClaimItem.display_label` for `operator_reported_result` and `external_reference`
respectively (`:70-71`, `:244-252`). They must not be treated as candidate values for this decision.
Likewise `EVIDENCE_CLAIM_CLASSES = {operator_reported_result, external_reference}` and
"observed_fact is explicitly forbidden for evidence entry" (`:128-130`).

The decision must therefore choose a `claim_class` **and** a `provenance`, or conclude that inventor
refinement text is **not** projectable as a decision-relevant input at all — which is a legitimate
outcome. `observed_fact` would be a false epistemic upgrade of owner free text and is forbidden for
evidence entry; `operator_reported_result` displays as *unverified* and may fit, but asserts a
**reported result** rather than a description; `assumption` may understate; `constraint` and
`owner_requirement` assert something the inventor did not necessarily mean. **No false binary is
preserved and no class is silently assigned.**

**`D-G3-2: MUST BE RESOLVED BEFORE IMPLEMENTATION AUTHORIZATION`** — and it is legitimately
unresolved here.

**If D-G3-1 or D-G3-2 cannot be resolved without adding vocabulary to `DecisionRecord`, the
implementation gate must STOP and return for a separate Owner vocabulary decision.** Adding a value to
the canonical decision vocabulary is not inside any permission exercised to date.

---

## §8. Canonical ownership — one decision owner, preserved

- **`DecisionRecord` remains the sole canonical decision-semantics and comparison/readiness owner.** No
  second `DecisionRecord`, no comparison database, no parallel gap-selection engine, no alternate
  relevance owner, no second CTA owner, no second evidence store.
- **The `AssertionRecord` ledger remains the sole durable truth.** The composed record stays
  **recomputed on demand and never persisted** (W2-A §13).
- **The two sets of §6.0 are projections, not owners.** The bounded rendered alternative set and the
  FDC comparison-eligible candidate set are both **deterministic projections of that one canonical
  ledger**. Distinguishing them creates **no second candidate store, no second decision model, no
  second comparison engine, no second persistence layer and no lifecycle database**; `DecisionRecord`
  remains the sole owner of comparison-membership semantics, and **what may be a member is D-G3-1's to
  authorize**, not this contract's.
- **`select_next_gap` remains the sole gap-selection owner**; `gap_relevance` remains the canonical
  relevance owner. Neither is read, called, or influenced by this repair.
- **W2-B × W2-C precedence is untouched by construction** `[EXEC]`: `_alternatives_crossing_context`
  derives its trigger from the ledger directly and never calls `compose_decision_records`
  (`progression_loop.py:1517-1545`), so extending the composition cannot alter the W2-B action slot,
  the `W2B_QUESTION_SLOT_PRECEDENCE` question slot, or the W2-C within-gap serving law.
- **WS11 stays dormant**; `gap_relevance` unchanged; canonical risk architecture unchanged.

---

## §9. Determinism

Every value on the new surface must be a pure function of canonical recorded state:

- derived from the final amended ACTIVE-and-withdrawn assertion ledger and committed content only;
- root-based identity, never uuid, never replay-position, never display text (W2-A §7 unchanged);
- deterministic ordering by ascending numeric founding root;
- equal ledgers compose byte-identically; a reconstructed session recomputes identical results;
- **no random scoring · no numeric score · no hidden confidence percentage · no volatile external
  truth in canonical state · no clock · no process memory.**

**No numerical score is introduced.** FDC-001 emits a categorical readiness value and never a number;
`[EXEC]` confirms no scoring surface exists in the decision owner.

---

## §10. EN / AR

- All new chrome enters `web/ui_text.py` as governed **EN + AR pairs**, rendered through the existing
  `t()` / `ui_lang` seam. No new translation mechanism.
- **User content — decision question, candidate names, recorded reasons — renders verbatim and is never
  translated**, exactly as W2-A §15 already requires.
- Correct RTL structure is inherited from the existing `dir` handling; the new markup must not break it.
- **No language-specific qualification divergence**: classification, reasons, evidence state and
  readiness are computed **before** presentation and are byte-identical across languages for identical
  evidence. Language must not be an input to any classification path.
- **G-4 is NOT merged into this repair.** The EN↔AR *assessment/progression* divergence measured in two
  of four controlled pairs keeps its own register row, its own `FRB` level and its own unresolved root
  cause. This contract must not introduce a **new** EN/AR divergence, and does not claim to fix G-4.

---

## §11. Early-intersection assessment — performed, per the Owner's §12

The registered early-intersection rule fires when authorized work touches *"CAP-12, CAP-13, CAP-18,
Commercial Evidence, Manufacturing Evidence, **Decision Snapshot architecture**, external-evidence
architecture, or another surface materially intersecting this direction"*
`[REPO — DEFERRED_OBLIGATIONS_REGISTER.md L149]`.

    DEFERRED MARKET / MANUFACTURING PRODUCT-DIRECTION INTERSECTION DETECTED: YES
    RECONCILIATION BROUGHT FORWARD: NO
    RECONCILIATION MUST BE INFORMED: YES
    NO-FORECLOSURE CONSTRAINT APPLIES: YES

**Assessment on the rule's own three-way test — a no-foreclosure rule suffices.** The intersection is
real: the reconciliation's dimension (1) *Technical Readiness* is *"the composition baseline the other
two must consume"*, and this repair improves exactly that baseline's decision surface. It is also
**bounded**: this contract implements nothing, activates no CAP (`CAP-06 / CAP-12 / CAP-13 / CAP-14 /
CAP-18 ACTIVATED: NO`), touches no manufacturing or commercial evidence, performs no external-evidence
access, and designs no Decision Snapshot — of which **no implementation exists at this base** `[EXEC]`.

**The no-foreclosure constraint that travels with the eventual implementation.** It must not foreclose
the reconciliation's open architectural choice between *"one Decision Snapshot with three dimensions,
two composed layers, existing-owner composition, or a simpler structure"*. Concretely: the repair must
add **no** new canonical decision owner, **no** dimension vocabulary, **no** readiness level, and **no**
cross-layer confidence propagation — leaving every one of those options equally available. §8 already
binds it to that.

**Nothing is discharged, closed, or treated as discharged.** The reconciliation row's owner
(`UNRESOLVED — REPOSITORY RECONCILIATION REQUIRED`), disposition, return trigger (after terminal RVR-7
**and** RVR-8) and latest safe gate (**BEFORE FCORA CONVENES**) are **UNCHANGED**.
**`READINESS IMPLEMENTATION AUTHORIZED: NO`.** The intersection does **not** block G-3, and is not used
to block it.

---

## §12. Acceptance evidence contract — frozen BEFORE implementation

The implementation gate is bound to this list. Every item is a required test; none may be waived by a
green suite elsewhere.

**Reachability and serving**
1. `A-1` The per-candidate state is reachable on the **served** Path-N session route for a session that
   declared a context and ≥1 alternative — asserted against rendered output, not a helper return.
2. `A-2` The same state is reachable on the served deliverable route.
3. `A-3` Cold read-only view (`state.domain is None`): composed state still displays; mutation forms
   stay suppressed (the existing W2-A rule is preserved).

**Boundedness and truthful classification (criterion 5)**
4. `A-4a` **RENDERED BOUNDEDNESS.** Every founding alternative root in the context's ledger that is
   materially relevant to the inventor's alternative history is represented **exactly once** in the
   bounded served view (§6.0 A), a withdrawn one included and truthfully represented as withdrawn —
   **no fabricated root, no duplicated root, no defaulted or seeded entry, no silent loss**; a project
   that declared nothing renders nothing.
   `A-4b` **COMPARISON MEMBERSHIP IS NOT ASSERTED HERE.** Which of those alternatives are members of the
   FDC comparison-eligible candidate set (§6.0 B) is whatever **D-G3-1** truthfully authorizes.
   `A-4a`/`A-4b` **must not decide that question ahead of D-G3-1, in either direction**; the membership
   assertion is written only after D-G3-1 resolves, and it asserts exactly that resolution.
5. `A-5` A withdrawn alternative **is visible in the bounded rendered set and is not dropped**, and is
   **truthfully distinguishable** from an evidence-based system elimination; an alternative the
   inventor has not withdrawn is `active`. **Its canonical status, its basis/provenance AND its
   comparison membership are whatever D-G3-1 resolves** — this test asserts *visibility and truthful
   distinguishability*, **NOT** the `eliminated` value and **NOT** membership of
   `DecisionRecord.candidates`, neither of which this contract freezes. Withdraw → re-declare founds a
   **new** root and a **new** rendered entry (W2-A identity contract unchanged).
6. `A-6` **No output ever carries a prohibited status** (`technically_selected`, `approved`,
   `validated`, `certified`, `production_ready`, `frozen`), and no candidate is ever marked a winner.

**Explicit reasons (criterion 6)**
7. `A-7` A withdrawal with a recorded reason renders that reason **verbatim**.
8. `A-8` A withdrawal **without** a recorded reason renders the governed *reason not recorded* copy —
   never invented text, never omission.
9. `A-9` **Conditioned on the authoritative resolution of D-G3-1, and not a pre-decision of it.** Once
   D-G3-1 is resolved, the canonical invariant it implies must be enforced and asserted — under the
   options that place a withdrawn candidate in a **non-active** status, that invariant is
   *every non-`active` candidate carries a `disposition_basis`* (`decision_workspace.py:664-673`,
   `:1044-1049`); under an option that does not, the invariant asserted is the one that resolution
   actually implies. **This test must never be read as establishing that a withdrawn candidate is
   non-active.** Independently of D-G3-1: an `active` **member of the comparison-eligible set (§6.0 B)**
   that is not yet comparable renders the existing `candidate_not_yet_comparable` blocking reason
   naming that candidate. **Visibility alone never triggers it** (`A-24`).

**Truthful no-decision**
10. `A-10` With insufficient evidence the surface renders the insufficiency outcome and **no** ranking,
    ordering-by-merit, preference or winner appears anywhere in the output.
11. `A-11` No fabricated comparison: with zero recorded inputs, readiness is `insufficient_information`
    and the rendered reasons are exactly the derived `blocking_reasons` — not prose.

**Determinism, reconstruction, provenance**
12. `A-12` Byte-identical composition for equal ledgers, run twice in-process.
13. `A-13` Full state reconstruction: a reconstructed session reproduces identical candidate ids,
    statuses, reasons and evidence state.
14. `A-14` Provenance preserved: every rendered value traces to a canonical ledger record; the composed
    record is **not persisted** (asserted, not assumed).

**EN / AR**
15. `A-15` EN and AR served outputs both render the full per-candidate surface; AR carries
    `lang="ar" dir="rtl"`.
16. `A-16` **Semantic parity**: for one identical ledger, the classification, reasons, evidence state and
    readiness are identical across EN and AR — only chrome differs. User content is untranslated in both.

**Non-regression and ownership**
17. `A-17` No duplicate canonical owner: exactly one `DecisionRecord` construction path for Path-N;
    no new persistence; no new decision model class.
18. `A-18` **W2-B × W2-C precedence unchanged** — the W2-B trigger matrix, `W2B_QUESTION_SLOT_PRECEDENCE`
    and the W2-C intent-coverage law produce identical results before and after.
19. `A-19` Existing Path-N behaviour unregressed: the full existing suite green, including
    `test_w2a_rvr4_*`, `test_w2b_amc_*`, `test_w2c_rvr6b_*`, `test_rvr7_*`, WPS-001 invariants and the
    FDC-001 contract tests.
20. `A-20` The live `/decision-workspace` lane is **byte-behaviourally unchanged** — its own tests green,
    its endpoints and templates untouched.
21. `A-21` `engine/deliverable_assembler.py` unchanged unless D-G3-4 is decided otherwise by the Owner;
    the two ODS-001 DEFERRED notes byte-identical either way.

**Withdrawal semantic truth and canonical mutation discipline (added at the BD-1 repair)**
22. `A-22` **WITHDRAWAL SEMANTIC TRUTH.** A candidate whose chain ended because of a **USER
    withdrawal** must not be canonically represented, classified, or rendered in a way that asserts an
    **evidence-based system elimination**, unless canonical evidence actually supports that judgment.
    The assertion applies to **all five** surfaces: (a) canonical representation (status and
    basis/provenance as D-G3-1 resolves them); (b) served **EN**; (c) served **AR**; (d) the rendered
    reason; (e) the rendered basis/provenance. The product must keep at least these semantics
    distinguishable: **user-withdrawn** · **evidence-based eliminated** · **retained / qualified** ·
    **unresolved** · **insufficient evidence / unable to compare**. Exact UI labels are not mandated;
    semantic truth is. **An identical error in both languages is NOT EN/AR parity** — parity is
    asserted only over outputs that are each independently truthful.
23. `A-23` **CANONICAL MUTATION DISCIPLINE — CONDITIONED ON D-G3-1, NOT A PRE-DECISION OF IT.** The
    invariant frozen here is `NO WEAKER SEMANTIC DISCIPLINE`. It is **NOT**
    *"every lifecycle event must have a `dispose_candidate()` equivalent"* — requiring that would
    silently force D-G3-1 Option B back into decision-disposition semantics, which is the BD-1 error
    in a different place.
    **(a) If D-G3-1 maps withdrawal into an existing or extended `DecisionRecord` disposition:** the
    composition seam must not produce a `Candidate` or `DecisionRecord` state that the canonical
    mutation API (`dispose_candidate()`) or the canonical accounting/readiness invariants
    (`_all_candidates_accounted_for()`) would **reject for the same semantic state**. A single
    construction path is insufficient if that path applies a weaker invariant: **no direct-constructor
    escape, no second and laxer construction discipline, and no hidden implementation waiver.**
    Asserted by constructing the composed state and submitting the equivalent semantic state through
    the canonical mutation path, not by inspection.
    **(b) If D-G3-1 keeps withdrawal OUTSIDE `DecisionRecord` disposition semantics:** **no equivalent
    `dispose_candidate()` call may be fabricated**, and none is required. Instead the assertions are:
    the underlying `DecisionRecord` remains in a canonically valid state on its own terms; the
    lifecycle projection alters no readiness, blocking reason, accounting outcome or comparison
    eligibility (`A-24`); and no derived presentation is shaped, labelled or exported such that it
    **masquerades as a decision disposition**.
    Under **both** branches the direct-constructor escape stays forbidden for whatever *is* a
    `DecisionRecord` candidate, and no implementation may reach through it a state the mutation API
    would reject.
24. `A-24` **WITHDRAWAL VISIBILITY MUST NOT IMPLY COMPARISON MEMBERSHIP.** A user-withdrawn alternative
    being visible in the served bounded view must not, **by itself**: (a) qualify it for comparison;
    (b) feed readiness — including the `_min_comparison_context()` active-candidate threshold;
    (c) create or suppress any `blocking_reason`, `candidate_not_yet_comparable` included;
    (d) trigger the accounting disposition requirement of `_all_candidates_accounted_for()`;
    (e) create an owner-preference conflict; or (f) create any other decision-semantic consequence.
    **Asserted differentially:** for one ledger, the composed comparison state with and without the
    withdrawn chain present yields identical `readiness_status`, identical `blocking_reasons` and
    identical accounting for every non-withdrawn candidate — **unless** the authorized D-G3-1
    resolution explicitly requires participation, in which case the assertion becomes that the
    difference is **exactly** what that resolution requires and nothing more. Any such consequence
    requires the canonical D-G3-1 resolution; **none may arise as a side effect of the visibility
    requirement.**

**The fallback contemplated by the earlier candidate is REMOVED.** `option_status = eliminated` with
`disposition_basis` absent is **not available** as an implementation escape: `dispose_candidate()`
raises on it and `_all_candidates_accounted_for()` fails accounting for it `[EXEC]`. No implementation
may rely on it, and no direct-construction path may be used to reach a state the mutation API rejects.

**Future benchmark evidence needed to show criteria 5/6 improved** — defined here, **not authorized**.
A future authorized verification would need, per record: the rendered alternative set matching the
declared set; a truthful state for every rendered alternative; an explicit reason for every
non-`active` comparison-set member and a
`candidate_not_yet_comparable` reason for every non-comparable active one; a truthful insufficiency
outcome where evidence is absent; zero fabricated rankings; and EN/AR parity of all of the above. It
must be measured against the **same frozen S2 corpus** to remain comparable, and — because the frozen
corpus does not exercise the withdraw path — a corpus extension would itself require separate Owner
authorization.

    THIRD S2 RUN: NOT AUTHORIZED — and none is requested, armed or implied by this contract.

---

## §13. Minimum contract path set — and why each path must change

**Exactly 2 paths.** No path count was assumed; the set was derived from the Lean §11 update
responsibilities and the repaired AIC semantics.

| # | Path | WHY THIS PATH MUST CHANGE |
|---|---|---|
| 1 | `docs/governance/G3_BOUNDED_DECISION_VALUE_REPAIR_CONTRACT_CANDIDATE.md` (**new**) | It **is** the authorized deliverable. The Owner authorized creation of one bounded implementation-contract candidate; the contract must exist as a committed artifact to be reviewable. |
| 2 | `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` (**append-only entry**) | Lean §11: *"The append-only roadmap receives one record per governed gate."* This is a governed gate, so exactly one provenance-only entry is required. |

**Paths deliberately NOT changed, each with its reason:**

- **`DEFERRED_OBLIGATIONS_REGISTER.md`** — no obligation fires, closes, is created, or is re-owned by
  freezing a contract candidate. G-3 is **already** routed to `T1-A′` in that row `[REPO — L150]`;
  re-recording it would duplicate an existing routing and risk creating a competing owner.
- **`ACTIVE_INCREMENT_CONTRACT.md`** — the repaired AIC Authoritative-only rule: *an in-flight candidate
  is a proposal and never appears*; candidate-era lifecycle lives solely in the roadmap's append-only
  entries. Touching it would re-create the non-terminating loop that repair removed.
- **`CURRENT_PROJECT_STATE.md`** — its SHA pin is expressly subordinated (*"resolve from Git each
  session; do not trust a prose-pinned SHA"*); re-pinning recreates the staleness pattern under repair.
- **`OWNER_DECISION_REGISTER.md`** — Lean §11 keys the append to a decision *"accepted and committed"*,
  which this candidate is not at freeze. This gate's own authorization is recorded in its roadmap entry,
  per the convention established at the AIC repair gate (§6 of that entry).
- **All product, runtime, test, schema, domain, prompt, script and benchmark paths** — forbidden in this
  gate, and none is necessary to freeze the contract.

    IF IMPLEMENTATION CODE CHANGES WERE NECESSARY TO FREEZE THIS CONTRACT: STOP.
    THEY ARE NOT. NO SUCH PATH IS TOUCHED.

**Delta.** `engine/ 0 · web/ 0 · domains/ 0 · tests/ 0 · database/ 0 · schemas/ 0 · prompts/ 0 ·
scripts/ 0 · benchmark instrument 0` — **`EXECUTABLE DELTA: 0`**.

---

## §14. Non-goals — explicitly excluded

ODS-001 activation · FDC-001 lane activation · new comparison engine · new database · market comparison ·
manufacturing readiness · commercial readiness · TRL / MRL / IRL / SRL · readiness scoring · CAP
activation of any kind · Decision Workspace activation · G-4 repair · G-5 generated-output repair ·
T2-G adaptive questioning · meaning-adaptive / Tier-2 · WS11 activation · FCORA · Serious Release ·
deployment · production · paid activation · `main` reconciliation · a third S2 run.

---

## §15. Contract self-termination (repaired AIC semantics)

This gate is **governance-only** and, per the repaired AIC rule, *a governance-only gate opens no
implementation contract and never becomes one*. Accordingly:

- **`ACTIVE CONTRACT: NONE`** is **untouched** by this candidate.
- No durable current-state sentence anywhere is set from this candidate's lifecycle.
- Every acceptance/publication/merge condition here is **freeze-scoped** and self-expires on merge.
- **No mandatory post-merge synchronization is created merely because this contract candidate later
  merges.** No current-state sentence becomes false solely because it merges.

---

## §16. Anti-anchoring — each proposition tested and disposed

| # | Proposition | Disposition |
|---|---|---|
| 1 | ODS-001 owns the comparison gap | **FALSE** — every committed definition scopes it to a components/materials/manufacturing catalogue; footprint is two deliverable notes (§4) |
| 2 | FDC-001 must be activated | **FALSE** — the class is already lawfully in the served Path-N runtime under the CLOSED OD-W2-DW-LIFT; the lane stays INACTIVE (§5) |
| 3 | RVR-4 must reopen | **FALSE** — it delivered user-declared alternatives and stays CLOSED; this builds on its merged output (§2) |
| 4 | T1-A′ is the implementation owner | **FALSE** — T1-A′ is the **release-value / governance** owner. The implementation surfaces are `decision_composition.py`, `web/app.py`, the two templates and `ui_text.py` (§2). Routing ≠ implementation ownership |
| 5 | A new comparison engine is required | **FALSE** — the vocabulary and the ordered readiness table already exist in the canonical owner (§3) |
| 6 | A numerical score is necessary | **FALSE** — readiness is categorical; no score exists or is introduced (§9) |
| 7 | One candidate must always win | **FALSE** — winner statuses are structurally prohibited; owner preference is preference only (§12 A-6) |
| 8 | Commercial / manufacturing readiness belongs here | **FALSE** — excluded; the intersection is recorded with a no-foreclosure constraint only (§11, §14) |
| 9 | G-4 belongs here | **FALSE** — separate register row, separate `FRB`, unresolved root cause; not merged in (§10) |
| 10 | G-5 belongs here | **FALSE** — Arabic generated-output parity keeps its existing Increment-3 row |
| 11 | Adaptive questioning is necessary | **FALSE** — no question is added, reworded, reordered or routed; T2-G untouched |
| 12 | More questions are necessary to create value | **FALSE** — the value comes from representing evidence the inventor **already recorded** (§6 S-3) |
| 13 | Decision Snapshot intersection blocks the repair | **FALSE** — no Decision Snapshot implementation exists `[EXEC]`; a no-foreclosure rule suffices (§11) |
| 14 | The repair can avoid evidence / provenance requirements | **FALSE** — every rendered value must trace to a canonical ledger record (§9, A-14) |
| 15 | Generic AI prose would satisfy criteria 5/6 | **FALSE** — and it is forbidden: reasons are recorded owner text or derived `blocking_reasons`; a missing reason renders as *not recorded*, never invented (§6 S-2, A-8, A-11) |
| 16 | Keeping a withdrawn alternative **visible** requires making it an FDC **comparison candidate** | **FALSE** — membership in `DecisionRecord.candidates` is a separate and decision-semantic act, with no inert branch (§6.0 `[EXEC]`); visibility is a deterministic ledger projection. Equating them would decide D-G3-1 Option B by construction |
| 17 | Therefore the safe repair is to hide the withdrawal again | **FALSE**, and forbidden — the opposite direction of the same error. `A-4a`/`A-5` freeze non-disappearance and `A-24` forbids visibility from carrying decision consequences; over-correction is explicitly excluded (§14) |
| 18 | Separating the two sets needs a second candidate store / decision model / comparison engine / persistence layer | **FALSE** — both are deterministic projections of the one canonical ledger; `A-17` binds both, `_compute_readiness()` is unedited, and nothing is persisted (`A-14`) |
| 19 | Every lifecycle event must have a `dispose_candidate()` equivalent | **FALSE** — the canonical invariant is `NO WEAKER SEMANTIC DISCIPLINE`. Under a lifecycle-only D-G3-1 resolution there may be no legitimate disposition to submit, and fabricating one would re-commit BD-1 (§12 `A-23(b)`) |

---

## §17. Lifecycle and non-authorization

**`G-3 IMPLEMENTATION AUTHORIZED: NO` · `G-3 IMPLEMENTATION STARTED: NO`.** This contract becomes
authoritative only through Lead review, Independent Review, Owner exact-SHA acceptance of this exact
candidate, a separate publication authorization, PR, a separate merge authorization, a merge commit
(second parent = the accepted candidate; EMPTY candidate→merge diff) and post-merge identity
verification. **Implementation START is a further separate Owner decision** even after that.

As at this candidate's freeze, stated as a fact about that moment:
`OWNER CONTRACT-FREEZE LIFECYCLE AUTHORIZED: YES` · `OWNER EXACT CONTRACT-SHA ACCEPTED: NO`.

**Fences unchanged by this contract:** `T1-A′ / T1-C′ / T1-D / MG-8 / R4-C: OPEN` ·
`T2-G / OD-PDVG-10: OPEN, UNDECIDED` · `RVR-4: CLOSED` · `W1-N3: NOT REOPENED` ·
`ODS-001: NOT ACTIVATED` · `FDC-001 LANE: INACTIVE` · `DECISION WORKSPACE: NOT ACTIVATED` ·
`CAP ACTIVATION: NONE` · `READINESS IMPLEMENTATION AUTHORIZED: NO` · `MEANING-ADAPTIVE / TIER-2: NO` ·
`WS11: DORMANT` · `gap_relevance` UNCHANGED · `SECOND S2 RUN: CONSUMED` · `THIRD S2 RUN: NOT AUTHORIZED` ·
`FCORA AUTHORIZED: NO` · readiness reconciliation ELIGIBLE, NOT CONVENED · `PSRR GO: NO` ·
`ACTIVE CONTRACT: NONE` (untouched) ·
`DEPLOYMENT / PRODUCTION / SERIOUS RELEASE / PAID ACTIVATION: NOT AUTHORIZED` · `main` NOT RECONCILED.

**Lean classification.** `LEAN RISK LEVEL: 2` · `REVIEW DEPTH: 2` — bounded governance-only contract
freeze, zero executable delta.

---

## §18. Pre-delivery adversarial self-review (Lean §5A)

Performed against **this sibling**, not against a prior one.

    PRE-DELIVERY ADVERSARIAL SELF-REVIEW:
    COMPLETED

    BLOCKING DEFECTS FOUND AND CORRECTED:
    5  (one family: product visibility collapsed into FDC comparison membership)

    REMAINING BLOCKING DEFECTS:
    0

    THE SEVEN REQUIRED QUESTIONS, ANSWERED AGAINST THIS TEXT:

    1. DID I DISTINGUISH VISIBILITY FROM COMPARISON MEMBERSHIP?
       YES. Sec 6.0 names both sets, states which one this contract freezes (A only), and proves
       from EXEC evidence that membership in DecisionRecord.candidates is itself decision-semantic
       (no inert branch in _all_candidates_accounted_for; the rule-1 active threshold; the
       candidate_not_yet_comparable emission; _validate_candidate_ids). S-1, S-5, A-4a/A-4b, A-5,
       A-9, A-23 and A-24 each carry the distinction explicitly.

    2. DID ANY ACCEPTANCE TEST STILL FORCE A WITHDRAWN ITEM INTO DecisionRecord?
       NO. A-4 was split: A-4a asserts rendered boundedness only; A-4b defers membership to D-G3-1
       in BOTH directions. A-5 now asserts visibility and distinguishability and explicitly not
       membership. A-9's independent clause is scoped to members of the comparison-eligible set.

    3. DOES A-23 STILL REQUIRE dispose_candidate() FOR A LIFECYCLE-ONLY RESOLUTION?
       NO. A-23 is now two-branch. Branch (b) states that no equivalent dispose_candidate() call may
       be fabricated and none is required; what is asserted instead is canonical validity of the
       record on its own terms, no readiness/accounting/eligibility effect, and no presentation that
       masquerades as a disposition. The frozen invariant is NO WEAKER SEMANTIC DISCIPLINE.

    4. CAN A VISIBLE WITHDRAWAL SILENTLY AFFECT READINESS?
       NO, and it is now asserted rather than assumed. A-24 forbids readiness, blocking-reason,
       accounting, eligibility and owner-preference consequences arising from visibility alone, and
       requires a DIFFERENTIAL assertion: composing with and without the withdrawn chain must yield
       identical readiness_status, blocking_reasons and accounting for the non-withdrawn candidates,
       unless the authorized D-G3-1 resolution requires exactly that difference and no more.

    5. CAN OPTION B ACTUALLY PASS THE FROZEN ACCEPTANCE CONTRACT?
       YES, and this was tested rather than asserted. Under Option B a withdrawn chain is visible
       (A-4a, A-5, S-4), is not a member of the comparison set (A-4b), triggers no accounting or
       blocking consequence (A-24), needs no dispose_candidate() equivalent (A-23(b)) and needs no
       disposition_basis, so the basis-absence problem does not arise on that branch. No acceptance
       item requires a status value for a non-member. Option B is therefore satisfiable, not merely
       nominally open. Option C remains equally satisfiable via A-23(a).

    6. DID I HIDE WITHDRAWAL TO MAKE THE PROBLEM DISAPPEAR?
       NO. Non-disappearance is strengthened, not weakened: S-1 freezes visibility, A-4a forbids
       silent loss, A-5 forbids dropping, and Sec 16 proposition 17 records over-correction as an
       explicitly FALSE and forbidden direction.

    7. DID I INVENT A SECOND OWNER OR STORE?
       NO. Sec 6.0 states both sets are deterministic projections of the one canonical ledger, and
       binds A-12/A-13/A-14/A-17 across both. No new model class, no new persistence, no new
       comparison engine, no lifecycle database, and _compute_readiness() is unedited. Sec 8
       (one decision owner) and A-20 (Decision Workspace byte-behaviourally unchanged) are untouched.

    KNOWN NON-BLOCKING OBSERVATIONS:
    1. The withdraw-reason capture (S-2) changes a served form. It is presentation-layer only and the
       receiving route and ledger already accept the field, but it is a real user-visible change and
       must not be characterised at the implementation gate as "render-only".
    2. Sec 3(b) establishes that the withdraw reason is empty in the served product by form omission.
       The frozen S2 corpus does not exercise the withdraw path at all, so no run-002 record can
       confirm or refute this from evidence; it is a source-level finding, labelled as such.
    3. D-G3-1 has no truthful existing disposition_basis value for a user withdrawal. NO
       BASIS-ABSENT IMPLEMENTATION FALLBACK IS AVAILABLE if the Owner declines a vocabulary
       addition: dispose_candidate() raises DecisionError for a non-active status without a basis,
       _all_candidates_accounted_for() fails the same state, and A-23(a) forbids reaching it by any
       other construction path. This constrains the branch on which a withdrawn chain IS a member of
       the comparison set; it does not constrain Option B, where no member and therefore no basis is
       required. D-G3-1 must resolve a COMPLETE truthful representation (membership, status,
       basis/provenance and reason carrier). If no authorized representation satisfies the canonical
       invariants, IMPLEMENTATION MUST STOP and return for a separate Owner decision.
    4. A-24's differential assertion is expressed over the composed comparison state. Naming the
       exact test seam is an implementation-gate decision; the contract fixes the assertion, not the
       harness.

    UNRESOLVED EVIDENCE GAPS:
    1. Whether OD-W2-DW-LIFT permission (3) already covers the Sec 7 vocabulary subset is an Owner
       reading of the Owner's own instrument and is NOT resolvable from repository evidence. Surfaced
       in Sec 5 as a precondition of implementation authorization rather than assumed either way.
    2. The historical intent behind the withdraw form omitting the reason field is not recorded in the
       repository. This contract states the mechanical fact only and asserts no intent.
    3. Whether the Owner intends a withdrawn alternative to participate in comparison at all is
       precisely D-G3-1 and is not decidable from repository evidence; the repository supplies the
       mechanical consequences of each answer, not the answer.

    UNAUTHORIZED SCOPE REQUIRED TO CORRECT ANY REMAINING ISSUE:
    NO

    READY FOR OWNER OR INDEPENDENT REVIEW:
    YES

**Defects found in the Lead-reviewed sibling `87dc507e…` and corrected in THIS candidate.** One family:
*product visibility collapsed into FDC comparison membership*, which would have decided **D-G3-1 Option
B by construction** — the BD-1 error class relocated from *status* to *set membership*.

1. **`S-1` conflated the two sets.** It froze that the withdrawn chain *"remains represented … in the
   composed record"* and that *"the candidate set stays bounded … one candidate per founding root"* —
   readable as freezing FDC comparison membership. **Corrected:** `S-1` now freezes **visibility**
   (visible, bounded, reconstructable, provenance-traceable in the served decision context) and states
   explicitly that comparison membership is part of D-G3-1, with `NO SILENT DISAPPEARANCE` never to be
   read as `MANDATORY FDC COMPARISON MEMBERSHIP`. `S-4` carried the same conflation in its rendering
   list (*"for each candidate … status"*) and is likewise scoped to the rendered set, with the rendered
   state stated as not necessarily the canonical `option_status`.
2. **`A-4` / `A-5` pre-decided membership.** `A-4` asserted *"the candidate set is exactly the ledger's
   founding roots"*, and `A-5` asserted representation *"in the candidate set"*. **Corrected:** `A-4`
   is split into `A-4a` (rendered boundedness: exactly once, no fabrication, no duplication, no silent
   loss) and `A-4b` (membership deferred to D-G3-1 **in both directions**); `A-5` asserts visibility and
   truthful distinguishability and explicitly **not** membership of `DecisionRecord.candidates`.
3. **`S-5` left readiness input membership unbounded.** It froze the verdict as whatever the unchanged
   table returns *"over the composed state"* — so a merely-visible withdrawal could depress readiness,
   manufacture `candidate_not_yet_comparable`, or enter accounting without Owner authorization.
   **Corrected:** the ordered rule table is preserved and unedited, and `S-5` now binds its **input
   membership** to the canonical comparison representation D-G3-1 authorizes.
4. **`A-23` pre-decided a mutation path.** It required submitting *"the equivalent semantic state
   through the canonical mutation path"* unconditionally; under a lifecycle-only resolution there may
   be no legitimate withdrawal state to submit, so the requirement would have forced Option B back into
   disposition semantics. **Corrected:** `A-23` is now two-branch and conditioned on D-G3-1, freezing
   `NO WEAKER SEMANTIC DISCIPLINE` rather than a mandatory `dispose_candidate()` equivalent.
5. **No guard separated visibility from consequence.** **Corrected:** `A-24` added — visibility alone
   may not qualify a candidate for comparison, feed readiness, create or suppress a blocking reason,
   trigger the accounting disposition requirement, create an owner-preference conflict, or create any
   other decision-semantic consequence; asserted **differentially**.
6. **`S-2` sequencing (non-blocking, fixed now).** It described an *"until D-G3-1 resolves"* rendering
   state while §7 forbids implementation before D-G3-1 resolves — a logically unreachable state.
   **Corrected** to post-resolution wording; the five frozen product properties (durable,
   provenance-traceable, verbatim where recorded, *reason not recorded* where absent, never fabricated,
   never epistemically upgraded) are unchanged.

**Preserved from the earlier siblings, deliberately not redesigned** (recorded, not re-litigated): the
removed §18 basis-absent fallback; the status-neutral `S-1` title; `withdrawn → eliminated` explicitly
NOT frozen; no silent disappearance; `S-2` not pre-committing `disposition_reason`; D-G3-1 unified over
status + basis/provenance + reason carrier; D-G3-2's full claim/provenance choice set; `A-5` not
freezing `eliminated`; `A-9` conditional on D-G3-1; `A-22`; the corrected ownership citation; the
latent `_owner_preference_conflicts()` disclosure as NON-BLOCKING for current Path-N; the
FDC-001 / ODS-001 / RVR-4 / T1-A′ boundaries; no readiness engine; no third S2 run; no implementation;
`EXECUTABLE DELTA: 0`. AHAEP §11 treats an incorrect material identity claim as a candidate defect even
where the underlying finding is correct, which is why item 6 is recorded rather than fixed silently.

---

*Contract candidate only. Nothing here authorizes implementation, product change, runtime change, test
implementation, ODS-001, FDC-001, CAP, readiness, deployment, publication, PR, or merge.*
