# Wave-1 Remediation Implementation Contracts (RVR-1, RVR-2, RVR-3, RVR-5)

STATUS: BOUNDED IMPLEMENTATION CONTRACTS — WAVE 1 ONLY, UNDER THE OWNER-FROZEN
FINAL REMEDIATION CONTRACT. Authorizes exactly the four increments below.
RVR-4 / RVR-6 / RVR-7 / RVR-8 remain NOT AUTHORIZED. No S2 rerun. The S2
benchmark record stays byte-frozen; the frozen R1–R8 recorded answer corpus is
used ONLY as regression fixtures (not an S2 run).

**Base:** `e119d60450f40b1633433625ae6a011eec112b79` (authoritative tip,
re-verified: 0 commits after). Owner authority: the Owner freeze-and-Wave-1
authorization accepting OD-R1, OD-R2, OD-PDVG-02(a), and the frozen remediation
architecture. Integration is serialized: each increment lands as its own commit
in the order RVR-1 → RVR-2 → RVR-3 → RVR-5; the later-merging increment owns
conflict resolution on shared surfaces (`web/app.py`, session/deliverable
templates) and re-runs its full contract test set after integration.

**Wave-1 preservation invariants (all increments):** no fabricated engineering
facts; truthful REVISE/HOLD; explicit unknowns; deterministic canonical state
and replay; evidence provenance; auditability; domain governance; canonical-
output architecture; R4-C correction semantics unchanged; no second decision
model; no meaning-adaptive routing; `engine/scoring.py`, the historical replay
benchmark, domain packs and their pins byte-unchanged.

---

## RVR-1 — Truthful unknown progression & completion semantics (OD-R1)

**Objective.** An honestly-held unknown, under an explicit owner action, becomes
the governed gap disposition `ACCEPTED_RISK` — truthfully labeled, durably
recorded, replay-stable, counted by completion semantics — so an honest journey
can complete without fabricating evidence.

**Allowed paths.** `engine/idea_state.py`, `engine/progression_loop.py`,
`engine/session_reconstruction.py`, `engine/deliverable_assembler.py`,
`web/app.py`, `web/templates/session.html`, `web/ui_text.py`,
`tests/test_wave1_rvr1_accepted_risk.py` (new).

**Contract.**
1. A seventh governed interaction disposition `risk_accepted` is added to the
   ledger vocabulary (provenance `OWNER_STATED`). It is an OWNER ACTION record,
   not a WS12 path (WS12 OD-3/OD-11 preserved); WS12 is CONSUMED for the path
   classification recorded as metadata (`DEFERRED_BY_USER`) — no second
   unknown vocabulary is created.
2. The ONLY writer of `Gap.status = ACCEPTED_RISK` is the canonical lifecycle
   function `accept_gap_risk(state, gap_type)` in `engine/progression_loop.py`:
   allowed only from OPEN/PARTIAL; **refused for `MECHANISM_COMPLETENESS`**
   (the core mechanism can never be risk-accepted); never automatic — only the
   explicit route below invokes it live, and only the recorded disposition
   replays it.
3. New route `POST /session/<sid>/accept-risk`: ownership check, answer-token
   parity, free-text hardening on the optional reason, explicit confirmation
   field required, staged mint → durable append (idempotent) → live status
   write → next-priority gap opened via the existing cascade. Fail-closed on
   every durable failure; nothing acknowledged that did not commit.
4. Completion semantics: `evaluate_transition` stage-two rule accepts
   `CLOSED` **or** `ACCEPTED_RISK` for `PHYSICAL_FEASIBILITY` and
   `BOUNDARY_AMBIGUITY`; `MECHANISM_COMPLETENESS` must still be `CLOSED` and
   `known_mechanism` ≥ REASONED (unchanged).
5. Reconstruction replays `risk_accepted` records in seq order through the SAME
   lifecycle function (interleaved with the answered replay); histories without
   such records replay byte-identically; `RECONSTRUCTION_VERSION` unchanged
   (additive record type); the answered replay bound is unchanged.
6. Deliverable truthfulness: accepted-risk gaps are ALWAYS visible — status
   label "Accepted risk" (exists), a Section-8 `accepted_risk` item per gap,
   and a verdict rationale qualifier + Category-D item whenever any accepted
   risk exists (a PROCEED-class verdict must never read "all identified gaps
   resolved" while a risk is merely accepted).

**Prohibited.** Auto-acceptance; accepting MECHANISM; WS12 mutating anything;
`resolves_gap=True` on the record; any change to D17/D-AISR-06/R4-C; silent
closure semantics (ACCEPTED_RISK never displays as resolved/closed).

---

## RVR-2 — Question-flow dead-end removal + relevance re-derivation

**Objective.** The identical exhausted question is never re-served more than
once after its reframe without a governed reason; honest on-topic answers are
not judged irrelevant because the marker families lag the committed banks.

**Allowed paths.** `engine/progression_loop.py` (display selection only),
`engine/gap_relevance.py` (marker families only, under the R2 contract's own
derivation rule), `web/templates/session.html` (exit-surface hint only),
`web/ui_text.py`, `tests/test_wave1_rvr2_flow_and_relevance.py` (new).

**Contract.**
1. Display selection after Path-N variant exhaustion: the deterministic reframe
   is served ONCE; every later render serves the deterministic EXIT PROMPT — a
   different, stable, governed message that names the honest exits (answer with
   new content; record unknown; accept as known risk (RVR-1); the other owner
   actions). Canonical state, gap status, and `get_question` are untouched.
2. `gap_relevance` marker families are RE-DERIVED from the committed Path-N
   question banks per the contract's own stated rule (whole-word, deterministic,
   fail-closed): additions are drawn from the questions' OWN vocabulary and its
   close inflections; the R2 exclusions (bare component nouns, bare causal
   connectives) stay excluded; every existing R2 fixture must remain green.

**Prohibited.** Removing any existing marker; changing the two-tier
threshold/eligibility semantics; touching `addresses_gap`'s fail-closed shape;
serving any non-committed question text.

---

## RVR-3 — Deterministic structured-substance assessment + MG-5 + T2-F guard (OD-R2)

**Objective.** Technically substantive practitioner-form answers are not
penalized solely for lacking preferred conversational causal phrases; rendered
provenance matches durable provenance; the quality-tier ordering hazard gains
a pinned guard.

**Allowed paths.** `engine/progression_loop.py`,
`tests/test_wave1_rvr3_structured_substance.py` (new).

**Contract.**
1. A new deterministic gated REASONED path (Layer-3, STRUCTURED-TECHNICAL),
   evaluated with the existing rejections intact (weak patterns, weak tokens,
   length): fires only for answers exhibiting committed structural-technical
   form — enumeration markers, labeled technical clauses, hyphenated technical
   compounds — per an explicit, reviewable predicate with fixed thresholds. No
   model inference; no semantic interpretation; pure text predicate.
2. The generic-verb trap yields to Layer-3 exactly as it already yields to
   Layer-2 (same composition point); Layer-2 and path A/B/C byte-unchanged.
3. The Wave-1 fixture set embeds the frozen S2 R1–R8 answer corpus: every
   novice-corpus REASONED answer stays REASONED; the expert-corpus closure
   answers reach REASONED (EN and AR); the weak/vague corpus stays ASSERTED.
4. MG-5: `Evidence` constructed from an owner answer is stamped
   `provenance=OWNER_STATED` at both construction sites; deliverable display
   maps unchanged.
5. T2-F guard: pinned tests record that `assess_response` never returns
   DEMONSTRATED, that Python string ordering of the tier constants is NOT the
   semantic order, and that `deliverable_assembler`'s numeric map is the
   canonical order — so any future DEMONSTRATED writer or ordering use trips a
   test instead of the latent defect. The 782/786/878/959 comparisons are NOT
   repaired here (OD-PDVG-08b owns the repair).

**Prohibited.** Touching `engine/scoring.py`, replay benchmark, golden
fixtures, domain packs, pins; granting REASONED to weak-token/weak-pattern
answers; any LLM/scoring model.

---

## RVR-5 — Rendered correction UX / T1-B (OD-PDVG-02(a))

**Objective.** The existing governed correction mechanism becomes user-reachable
through truthful rendered UX; the change reason becomes visible (criterion 14).

**Allowed paths.** `web/app.py` (render context only — the `/correct` route
body is byte-unchanged), `web/templates/session.html`,
`web/templates/deliverable.html` (withdrawn-history visibility only),
`web/ui_text.py`, `tests/test_wave1_rvr5_correction_ux.py` (new).

**Contract.**
1. The session page renders a "Correct an earlier answer" affordance listing
   the ACTIVE accepted answer records (rec id, gap label, excerpt) with a form
   posting `supersedes_record_id` + `response` + the SAME server answer token to
   the EXISTING route. Truthful copy (EN+AR catalog entries): a correction
   preserves the prior answer as withdrawn history and re-evaluates the whole
   journey deterministically; nothing is erased.
2. The existing `CORRECTION_APPLIED_ACK` renders through the existing
   `interaction_ack` surface (no new ack model); the deliverable surfaces the
   withdrawn-source count it already carries.
3. Correction semantics (route body, replay, supersession, idempotency,
   tokens) are BYTE-UNCHANGED.

**Prohibited.** Any change to R4-C semantics, the route body, supersession or
replay behavior; any second correction model; erasure language in UX copy.
