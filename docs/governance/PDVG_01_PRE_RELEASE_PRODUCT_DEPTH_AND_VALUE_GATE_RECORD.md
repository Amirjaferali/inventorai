# PDVG-01 — PRE-RELEASE PRODUCT DEPTH & VALUE GATE (Candidate)

**Status of THIS record:** governance/documentation-only **CLASSIFICATION RECORD — REPAIR CANDIDATE**
(bounded repair after Independent External Review REJECT of `fd7de207…`; that candidate is preserved as
immutable rejected evidence and is neither amended nor published). It
implements nothing, authorizes no runtime work, activates no workstream or capability, creates no new
numbering for existing owners, and becomes authoritative **ONLY if/when this exact candidate is merged
and post-merge verified**. **`OWNER_DECISION_REGISTER.md` UNCHANGED** — this gate surfaces Owner
decisions (§21) but records none as made.

**Base:** `1295ed08ec902f2fcc21934eac3622548a44719b` — the live authoritative tip, independently
re-verified this gate: PR #558 merge; first parent `2da8a6a3bb832bf3326c4cb7cc9e1dc8a99499e7`; second
parent `1f5989b5c81b08d81cb00a145007dc3b430072a4` (the exact Owner-accepted TDVP reconciliation
candidate); merge tree `bdb6e6b9a4a62eb4b41d1b7c612a737dfc851a81`; candidate→merge diff **EMPTY**
(0 lines); `git diff --check` **PASS**; zero later commits; clean tree **[EXEC]**.

**Evidence classes:** `[REPO]` committed fact at this tip · `[EXEC]` executed/measured this session at
this tip · `[OWNER]` Owner decision or directive · `[OPEN]` unresolved.

**PDVG-01 is not:** TDVP reopened, TDVP renamed, a duplicate technical-depth program, an implementation
gate, a PSRR execution gate, a deployment gate, a production gate, or a commercial activation gate. It
classifies, by release value, the product-depth work this repository actually carries — in four kinds:
**adequately owned**, **partially owned**, **dormant or planned**, and **independently proven ownership
gaps**. Two §9 rows have **no current owner** — semantic adaptive questioning (§4A) and user-feedback
capture (§8.19) — and both are recorded as unowned rather than attached to an adjacent owner.
**PDVG-01 assigns no owner and creates no workstream by itself**: where a gap is proven it is surfaced
for Owner adjudication, never resolved here.

---

## §1. Required opening status lines — traced, not inherited

§4 of the directive requires four lines and forbids writing them merely because they were previously
said. Each is traced below; one **cannot be supported as a repository fact** and is reported as a
conflict rather than forced.

| Line | Verdict | Basis |
|---|---|---|
| `NO NEW TDVP PROGRAM REQUIRED: YES` | **SUPPORTED [REPO]** | Merged `TDVP_POST_PVCG_RECONCILIATION_RECORD.md` §7 (*"OUTCOME A — NO NEW PROGRAM REQUIRED"*) and §8 (`TDVP AUTHORITATIVE ROADMAP CREATED: NO`), authoritative since PR #558. |
| `UNOWNED TDVP GAP COUNT: 0` | **NO LONGER SUPPORTABLE AS WRITTEN — QUALIFIED (see §4A)** | The committed phrase is `TRUE RESIDUAL GAP COUNT: 0` (TDVP §4/§8), and TDVP's own predicate is *"No provisional topic identifies a material capability gap that lacks an adequate current owner."* **PDVG-01's deeper contract-by-contract reconstruction has since falsified that predicate for one narrower constituent** — semantic adaptive questioning (§4A). The historical TDVP statement is preserved as authority-at-that-time and is **not rewritten**; the current count is restated as `UNOWNED CAPABILITY GAP COUNT (PDVG-01 reconstruction): 1` pending Owner adjudication (**OD-PDVG-10**). |
| `MATERIAL OWNED PRODUCT-DEPTH WORK REMAINS: YES` | **SUPPORTED [REPO]** | TDVP §4 names four surviving owned residual facts; §15 rows 8/13/14/15 record four workstreams closed with **zero implementation**; WS16 closed with `FINAL LIMITATIONS 10 (OWNER-ACCEPTED, UNREMEDIATED)`; WS10/WS11/WS12 recorded dormant. Independently re-measured this gate (§3). |
| `FIRST SERIOUS RELEASE REQUIRES PRE-RELEASE INCREMENTS: YES` | **[OWNER] ONLY — NOT REPOSITORY-DERIVABLE. CONFLICT REPORTED.** | *"first serious release"* was **not a committed repository term at base `1295ed08…`** — zero occurrences in `ACTIVE_EXECUTION_ROADMAP.md`, `CURRENT_PROJECT_STATE.md`, or `ACTIVE_INCREMENT_CONTRACT.md` **[EXEC]**. *(This candidate's own tracker entries introduce the phrase while reporting it as an [OWNER] premise; the absence is asserted of the base, never of the candidate.)* The repository's own release-precondition concept is the **Minimum Launch-Conformance Set**, and it is explicitly undefined: `MINIMUM LAUNCH-CONFORMANCE SET SATISFIED: NO`; `FULL MLC DEFINITION FROZEN: NO`; *"whether to commit a definition remains an OPEN Owner decision"* (`PVCG_FORMAL_CLOSURE_RECORD.md`; roadmap L14634–14637) **[REPO]**. With no committed definition of the release and no committed criteria for it, **the repository cannot support or refute this line.** It stands as an Owner premise, and this record proceeds under it as such. |

**Consequence, stated plainly.** The Tier-1 set proposed in §5 is, functionally, a **candidate MLC
definition**. This record does not commit it as one. Whether to freeze the Tier-1 set as the MLC is
surfaced as Owner decision **OD-PDVG-07** (§10).

---

## §2. Governance-surface staleness — observed, governed, NOT repaired here

Two canonical surfaces carry stale current-truth pointers. **Both are already neutralized by their own
adjacent committed rules**, so neither is treated as a defect and neither is rewritten by this record.

1. `CURRENT_PROJECT_STATE.md` L18–24 pins the branch tip at `3a802fd8…` (PR #427) — ~130 PRs behind
   **[EXEC]**. Neutralized in place at L15–17: *"**Live tip:** resolve from Git each session … Do
   **not** trust a prose-pinned SHA."*
2. `PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md` L10 still reads `PHASE 3 NOT
   STARTED — PHASE 4 NOT STARTED … PHASE 9 NOT STARTED` **[REPO]**, while current truth records
   Phase 4 formally closed within its implemented boundary (`CURRENT_PROJECT_STATE.md` L4559–4565) and
   Phase 9 formally closed. Neutralized by `CLAUDE.md`, which binds every agent to *"verify the
   currently active phase from the latest committed roadmap and status surfaces"* and not to treat the
   plan's baseline as expected truth.

Recording these is disclosure, not a finding. No historical or append-only record is rewritten by
PDVG-01.

**One precision note on the immediately-prior merged record.** `TDVP_POST_PVCG_RECONCILIATION_RECORD.md`
§2 T-10 describes WS13/WS14/WS15 as being at *"contract/owner-decision stages in §15"*. At that tip and
at this one, §15 rows 13/14/15 read `WORKSTREAM 13/14/15 FORMALLY CLOSED` (unchanged since PR #335,
long before TDVP) **[EXEC]**. The TDVP characterization **understates their recorded status**. It is a
merged, append-only record and is **not rewritten**; the correction is recorded here and the correct
status is used throughout this record.

---

## §3. What the product actually is today — measured, not inferred

Every line in this section was executed or read at this tip.

### 3.1 Full-suite baseline (fresh)

`4418 passed · 3 skipped · 1 xfailed · 0 failed` (109.6s) **[EXEC]** — identical to the figure recorded
at the PVCG closure tip `ca9fb4be…`, confirming PR #557 and PR #558 `TEST DELTA: 0` by measurement.

### 3.2 A stale residue, discharged — the 31 baseline failures

`FINAL_LIMITATION_REGISTER.md` L222–229 carves out *"The 31 `tests/test_domain_registry.py` failures …
PRE-EXISTING NON-WS16 BASELINE ISSUE … require a SEPARATE REMEDIATION PATH IF LATER AUTHORIZED"* —
excluded from the limitation count, with no owner **[REPO]**.

Re-measured this gate: `tests/test_domain_registry.py` → **41 passed, 0 failed** **[EXEC]**.

**The 31-failure residue no longer exists.** It is discharged by later work, not carried forward. Any
record still citing it as open is stale.

### 3.3 The live user path makes **zero** AI calls

- `engine/ai_advisor.py:11` — `AI_ADVISORY_ENABLED = False`; `:28` returns before building any request.
- `web/app.py:2174` sets `state.path = "N"`; `engine/progression_loop.py:1005/1045/1079` guard every
  call site with `None if state.path == "N" else get_ai_question(...)` — so the advisor is never
  invoked on the live path.
- `engine/ai_advisor.py:54–61` builds headers with no `x-api-key`; no `ANTHROPIC_API_KEY` is read
  anywhere in `engine/` or `web/`. An enabled call would 401 into `except Exception: return None`.
- `requirements.txt` pins exactly Flask, gunicorn, pytest — no provider SDK.
- `tests/test_wps001_invariants.py:19/22/25` assert the gate functions cannot reference `ai_advisor`;
  `tests/test_baseline_readiness.py:63` asserts `AI_ADVISORY_ENABLED is False`. **[EXEC/REPO]**

**InventorAI is, at this tip, a fully deterministic offline engine.** This single fact governs §7
(CAP-15/CAP-17) and §8 (Golden benchmark) below.

### 3.4 Active user-facing capability

Deterministic journey over **six governed gap types** in two fixed-priority lists
(`GAP_PRIORITY`, `STAGE3_GAP_PRIORITY`, `progression_loop.py:41–53`); **21 committed Path-N questions**
(11 electronics + 10 mechanical) **[EXEC]**; deterministic assessment (`assess_response`,
`domain_rules`, `semantic_registry`, `gap_relevance`); conservative provenance-labelled safety signals;
a **14-section deliverable** (`deliverable_assembler.assemble_deliverable`, `:206–227`); Increment-2
record axes with supersession; INSERT-only durable store; deterministic full replay; the R4 correction
route; P7-I1/P7-I3 canonical one-way export; accounts/auth/entitlements/quotas/subscription
lifecycle/payment port; `activated_domains() == ['electronics_electrical', 'mechanical']` **[EXEC]**.

**True writable resume is LIVE** — `POST /session/<sid>/resume` (`web/app.py:2301`), guarded by the
evolved `UG-CORE-08` and the new `UG-CORE-16` (`tests/universal_guardrail_manifest.py:148,172`),
merged via PR #535, roadmap L12149: *"P10-PC3 AUTHORITATIVE: YES. True Writable Resume is live"*
**[REPO/EXEC]**. *(The `P10_PC3_…CONTRACT.md` header still self-describes as a non-authorizing contract
candidate — that is its creation-time text, superseded by the recorded contract merge PR #534 and the
implementation merge PR #535. Reading the document header alone would produce a planned-vs-implemented
error.)*

### 3.5 Dormancy — measured by reference, not assumed

Non-test references to each module, across all Python outside `tests/` **[EXEC]**:

| Module | Owner | Non-test references |
|---|---|---|
| `engine/question_intent_registry.py` | WS10 | **only** `engine/question_aware_evaluation.py` |
| `engine/question_aware_evaluation.py` | WS11 | **NONE** |
| `engine/controlled_unknown_progression.py` | WS12 | **NONE** |
| `engine/stage3_evaluator.py` | Stage 3 | **NONE** |

No user-facing path reaches any of them. **WS10, WS11 and WS12 are formally CLOSED workstreams
delivering zero user-visible capability at this tip.**

**A material correction to the standing characterization.** WS10 is repeatedly recorded as
"built-dormant", implying activation is a wiring decision. It is not: **no WS10 registry data artifact
exists anywhere in the repository** — a repo-wide search for a JSON file containing `primary_intent`
returns nothing **[EXEC]**. WS10 is a validated *loader and record contract with no committed content*.
Activating it requires first authoring and governing intent content for the 21 committed questions.

### 3.6 Capabilities with **no code at all**

`engine/adaptive_follow_up.py` (WS14), `engine/guided_answer_support.py` (WS13), and any WS15
display-layer adapter are **absent**, and their absence is actively enforced by committed test guards
(`tests/test_workstream_9_single_intent_question_design.py:315–316`;
`tests/test_workstream_12_controlled_unknown_progression_base_red.py:462`) **[EXEC]**. WS13, WS14 and
WS15 each closed *"WITHOUT BASE RED, IMPLEMENTATION, OR GREEN"* **[REPO]**. Their governance records are
candid throughout and never claim delivery; the product-depth consequence is nonetheless that **three
consecutive P2 workstreams produced zero production code.**

---

## §4. THE STRUCTURAL FINDING — the upper evidence ladder is unreachable

This is the single most consequential product-depth fact at this tip, and it is not recorded anywhere in
the current governance corpus.

The evidence architecture defines a full ladder — quality `ASSERTED | REASONED | DEMONSTRATED`
(`idea_state.py:13–15`); validation `UNVALIDATED | SPECIALIST_REVIEWED | EMPIRICALLY_DEMONSTRATED |
INDEPENDENTLY_VERIFIED` (`:59–115`); provenance `OWNER_STATED | SYSTEM_INFERRED | EXPERT_SUPPLIED |
EXTERNAL_EVIDENCE`; with public labels for every value (`deliverable_assembler.py:49,56`) **[REPO]**.

**No production code path can produce any value above the floor of any axis [EXEC]:**

* `progression_loop.py:750` — `return ASSERTED  # DEMONSTRATED requires external evidence — not in MVP`.
  `_classify_quality` returns only `ASSERTED` or `REASONED`.
* `validation_status` **on the Increment-2 record axis has no writer**: across `engine/` and `web/`
  the only assignments are the default parameter (`idea_state.py:324`), its pass-through (`:381`) and
  deserialization (`record_contract.py:166`). All three `record_interaction` call sites in `web/app.py`
  omit it. **One assignment exists elsewhere and is deliberately excluded from that count:**
  `safety_signal.py:494` sets `validation_status=VALIDATION_REQUIRES_INDEPENDENT` on the
  **`SafetySignal`** dataclass — a distinct, frozen, advisory, explicitly **non-persisted** object
  (*"All fields are display context … nothing is persisted"*, `:311–312`) carrying its own frozen
  single-value vocabulary (`:48`). It is not the `AssertionRecord` / `Evidence` axis and makes no ladder
  value reachable **[EXEC]**.
* Provenance reaches only `OWNER_STATED`, via `_DEFAULT_PROVENANCE_BY_DISPOSITION` (`idea_state.py:129`).

**Three consequences, each verified:**

1. **`derive_readiness().overall_verified()` always returns `False` in production** — `is_verified`
   (`derived_readiness.py:73`) fails on `any(r.validation_status == UNVALIDATED ...)`, which is
   universally true. This is fail-closed by construction, not by evaluation. Truthful, but it means
   the readiness axis is a constant.
2. **WS11 activation would be actively harmful today.** WS11's outcome is a strict function of the
   quality tier — `DEMONSTRATED→SATISFIED, REASONED→PARTIALLY_SATISFIED, ASSERTED→NOT_SATISFIED`
   (`question_aware_evaluation.py:11–13`). Since `DEMONSTRATED` is unreachable, **no answer could ever
   be `SATISFIED`.** Wiring WS11 now would surface a permanently negative evaluation to every user.
3. **A latent correctness defect, verified.** Four sites in `progression_loop.py` (782, 786, 878, 959)
   order quality by raw string comparison. Python orders these strings
   `ASSERTED < DEMONSTRATED < REASONED`, so **`'DEMONSTRATED' >= 'REASONED'` is `False`** **[EXEC]**.
   `deliverable_assembler.py:1439` encodes the *intended* order explicitly as
   `{ASSERTED: 0, REASONED: 1, DEMONSTRATED: 2}`, and `progression_loop.py:796` comments that the branch
   *"runs for DEMONSTRATED, REASONED, and ASSERTED"* — so the intent is unambiguous and the comparison
   contradicts it. The defect is **currently masked** only because `DEMONSTRATED` is unreachable.

**Classification (per `CLAUDE.md`): actual logic defect**, not structural, semantic, fixture or runtime
drift. **PDVG-01 is not authorized to repair it** (`executable delta = 0`).

**CORRECTED CLASSIFICATION — the rejected candidate under-tiered all three consequences by folding them
into a single "precondition of a future increment". They are now separated and tiered independently:**

* **§4.a — Product truth today → TIER 1 (T1-D).** The deliverable ships honest per-value labels while no
  value above the floor is reachable. That gap between shipped labels and reachable states is a
  **user-facing truthfulness** issue, not a future-increment issue, and it belongs in the release gate.
* **§4.b — Evidence-writer mapping → TIER 2 MUST before paid activation (T2-E).** A readiness axis whose
  value is a constant `False` is not a measurement; it is a constant rendered where a measurement is
  implied. Fail-closed is honest, but selling evidence/readiness *progression* when progression cannot
  occur is a product-value defect. The future governance requirement is defined here and **not
  implemented**: *which governed user action, through which route, with what qualifying evidence, may
  write each non-default quality / validation-status / provenance value.*
* **§4.c — Ordering repair + mandatory guard test → TIER 2 bounded repair before paid activation
  (T2-F).** The rejected candidate left the trigger dependent on someone *recognising* a future change
  as an "evidence-ladder increment". That is not a safeguard. The defect is live in shipped code and its
  only protection is an emergent invariant **that no test enforces** — so any change making
  `DEMONSTRATED` reachable, including one nobody labels a ladder increment, silently activates wrong
  `known_mechanism` / `known_problem` promotion. The repair must ship **with a guard test** that fails if
  the ordering is ever wrong, which converts the invariant from emergent to enforced.

Surfaced under the **OD-PDVG-08 container** (§10) — a non-actionable parent heading whose two
actionable children, **OD-PDVG-08a** and **OD-PDVG-08b**, carry these parts distinctly.

This single dependency simultaneously gates WS11, CAP-11, CAP-12, CAP-13 and verified-readiness. It is
the **central product-depth bottleneck** at this tip.

---

## §4A. TRUE OWNERSHIP GAP — semantic adaptive questioning

This section exists because PDVG-01's own §17 finding (the questioning is the product's weak axis) and
its inherited status line (`UNOWNED TDVP GAP COUNT: 0`) **contradicted each other**. The contradiction
was resolved against the contracts, not against governance tidiness.

**The capability, stated exactly:** `material answer content` → `new / changed canonical technical
state` → `next-question decision materially adapts` — while preserving determinism, semantic stability,
relevance, safe skip, unknown-aware routing, one-question-at-a-time, and no generic chatbot drift.

### §4A.1 Contract-by-contract disclaimer trace — every candidate owner excludes it in its own words

| Candidate | Its own committed text | Verdict |
|---|---|---|
| **WS8** | P8-1/P8-2 expressed-intent **DEFERRED**; deferral destination named as WS9/WS10/WS11/WS14 | not owner |
| **WS9** | single-intent question **design** — design-time authoring of question content | not owner |
| **WS10** | contract L71: registry is *"a descriptive layer over already-committed content — **without changing question text, serving selection or order, evaluation, persistence, or user-facing behavior**"*; §3: *"User-expressed-intent capture and all intent-aware runtime behavior remain **deferred and separately owner-gated**"* | **explicitly excludes it** |
| **WS11** | *"NOT semantic answer evaluation"*; content matching *"explicitly deferred and blocked"*; **D14** defers *"any consumption that changes user-facing output, gap status, `Evidence`, or **transition decisions**"* | **explicitly excludes it** |
| **WS12** | observation-only; `mutates_progression=False` | not owner |
| **WS13 / WS15** | display/guidance layer; no engine code exists | not owner |
| **WS14** | contract L59 lists **out of scope**: *"semantic answer verification; semantic expressed-intent detection"*; L227: expressed-intent capture *"remains a RECORDED LIMITATION, a DEFERRED CAPABILITY, and **NOT COMPLETED BY WS14**"* | **explicitly excludes it** |
| **WS16** | read-only validation gate, electronics-only | not owner |
| **WS17 / STG / AISR** | post-gate / reserved / specialist routing — none owns next-question semantics | not owner |
| **`stage3_evaluator`** | recorded not integrated; zero non-test references **[EXEC]** | not owner |
| **`gap_relevance`** | header L23–25: *"a **LEXICAL**, deterministic marker test … not a semantic component. It does not interpret an answer"* — it gates whether an answer counts for the **served** gap; it never changes which gap comes next | not owner |
| **WS4 §7.5** | "adaptive question sequencing" is a within-step clarify-or-defer branch of criticality capture | not owner |

**Two findings that make this conclusive rather than merely eliminative [REPO]:**

1. **WS11.2 is not an owner — it is a name.** WS11's owner-decisions document defers content-semantic
   matching to *"a later WS11.2 owner-decisions [gate]"*. **WS11.2 exists only as forward-reference text; it has no contract, implementation file, or §15
   ownership row** — the six occurrences of the name in `WORKSTREAM_11_…OWNER_DECISIONS.md` are all
   forward references, and the count of contracts, files and §15 rows is zero **[EXEC]**. And even a delivered WS11.2 would not produce the capability, because **D14 blocks
   transition-decision consumption independently of D7.2**: `select_next_gap` would remain pure
   fixed priority.
2. **The repository already records the capability as desired and assigns it to nobody.** WS4 §17 states,
   as a *"**[FUTURE — recorded product observation, outside Workstream 4, non-authorizing]**"*, that the
   full journey *"should eventually follow: understand → summarize → confirm → **ask only what is
   missing** → then generate advanced outputs"*, and then disclaims: *"authorizes no implementation, no
   journey redesign, and **no new workstream**"* **[REPO]**. *"Ask only what is missing"* **is** this
   capability. It is named, wanted, and ownerless by explicit statement — not merely unfound.

**Verdict: TRUE OWNERSHIP GAP. No workstream, capability, or phase owns it.** The deferral chain closes
on itself: WS8 → WS10/WS11/WS14 → each disclaims it → WS11 → WS11.2 → does not exist → and would be
blocked by D14 anyway.

### §4A.2 Why TDVP's conclusion was reasonable then and is falsified now

TDVP T-10 concluded that every constituent of "Adaptive Technical Reasoning & Question Routing" is
*"either already implemented … or already owned by a named, deliberately staged workstream."* At that
depth — mapping the **topic** to the **WS8–WS17 family** — the conclusion followed from the evidence
available. PDVG-01 was required to reconstruct one level deeper, at the level of the **capability
each contract actually admits**, and at that depth the family does not contain this constituent: every
member disclaims it individually, so the set does not own it collectively. **The historical TDVP
statement stands as authority-at-that-time and is not rewritten.** What changes is the current count.

### §4A.3 Release classification — re-proved, not inherited

* **First serious release: SHOULD, not MUST.** A bounded release can honestly ship a governed fixed
  question set. The active differentiation (§17) is output-side and does not depend on adaptivity, and
  no committed surface claims adaptivity — `FULL ADAPTIVE QUESTIONING ACTIVATED: NO` stands in eight
  documents **[REPO]**. *Binding condition:* no surface, copy, or marketing may imply adaptive
  questioning, and the T1-D disclosure must state the fixed question set plainly.
* **Paid activation: MUST.** Charging for technical depth while the input side is measurably weaker
  than a free general assistant is a product-value defect, not a roadmap preference.
* **Strategic importance: HIGH.** It is the single largest differentiation gap in the product.

It is therefore **Tier 2 (T2-G)** — not Tier 1, and emphatically not "optional future".

### §4A.5 Four questions that were being collapsed into one — separated and answered

An earlier formulation of this record said *"completeness cannot be established while OD-PDVG-10 is
unresolved."* That is **withdrawn as unsound**. It made an ownership question gate a conformance
question, which turned a **SHOULD** into a **MUST** by the back door and would have made option **D** of
OD-PDVG-10 (decline / defer) self-defeating — under it, declining would still leave the release
definition blocked, so D was not really available. Re-adjudicated from first principles:

**1. Must semantic-adaptivity *ownership* be resolved for PDVG-01's governance truth to hold?**
**NO.** The truthful statement is *"one capability gap exists and has no owner"* — and that statement is
already true, evidenced (§4A.1) and recorded. A governance record is complete when it states what is
and is not owned; it does not become incomplete because an Owner has not yet chosen what to do about it.
PDVG-01 is governance-truthful as it stands, with OD-PDVG-10 open.

**2. Must it be *implemented* for the first serious release?**
**NO — SHOULD, not MUST** (§4A.3, unchanged and re-proved). No committed surface claims adaptivity;
`FULL ADAPTIVE QUESTIONING ACTIVATED: NO` stands in eight documents; the active differentiation (§17) is
output-side and does not depend on it. The deferral is honest **on one condition**: T1-D discloses the
fixed, non-adaptive question set. That condition is a **Tier-1 item in this record**, not a promise.

**3. Must the ownership disposition be settled before the MLC may be frozen?**
**NO.** The MLC is the set of conditions that must hold **before launch**. Semantic adaptive questioning
is **Tier 2** — by construction **not a member** of that set. Whether a non-member has an owner cannot
change the membership of the set. Ownership is a **roadmap** question; conformance is a **release**
question; conflating them is precisely the error being repaired. **OD-PDVG-10 does not block MLC
definition**, and no evidence in this gate establishes any separate reason that it should.

**4. Is it mandatory only before paid activation?**
**YES, for implementation** (§4A.3). The ownership decision should precede the implementation it
authorizes, so it too falls before paid activation — but that is sequencing within Tier 2, not a
release-gate condition.

**Consequence for MLC.** MLC remains **unfrozen in this candidate** — but for reasons that are actually
evidenced, and none of them is OD-PDVG-10: (i) the corrected Tier-1 set has **not itself been
independently reviewed**, and the prior set was judged INCOMPLETE by review; (ii) **T1-A′'s own scope is
undefined pending OD-PDVG-11** — a conformance set cannot be frozen while one of its members has
unapproved scope; and (iii) freezing the MLC was already a standing open Owner decision before PDVG-01
existed. See OD-PDVG-07.

### §4A.4 Ownership is surfaced, never assigned here

**OD-PDVG-10** (§10) puts four bounded options to the Owner. This record assigns no owner, opens no
workstream, and **refuses to force the capability into WS14 or WS11**, both of which exclude it in their
own committed text. Doing so would be false reuse, and would make the governance record claim a
capability the product does not have.

---

## §5. Release tier model — tested, not assumed

The four-tier model is **justified and adopted** for this classification. Its discriminator is *what
the absence does to the central product promise for a serious target user* — never ownership state,
never test count, never governance maturity.

Three dimensions are held separate for every capability, per §5 of the directive: **governance state**,
**implementation/activation state**, and **release tier**.

### TIER 1 — MUST BEFORE FIRST SERIOUS RELEASE

**T1-A′ · Bounded S2 extension, then one run on the release candidate.** *(CORRECTED — the rejected
candidate proposed running S2 unchanged and marked its coverage ADEQUATE. Re-verification shows that is
materially wrong.)*

Owner: `docs/benchmarks/BICYCLE_BRAKE_LIGHT_COMPETITIVE_BENCHMARK.md` (S2) — **unchanged. No second
benchmark owner is created.** What S2 actually measures, verified from its own text and from code
**[REPO/EXEC]**:

* **Its mandatory core gate is scoped to a different lane.** §6 verbatim: *"**For the first Technical
  Decision Workspace increment**, ALL of these core outcomes must be demonstrated."*
* **Two of its criteria are unimplementable against any current surface.** Criterion 12 requires
  *"affected prior decision marked internally with `validity_status=stale`"* — **`validity_status`
  occurs in no Python file in the repository at all** **[EXEC]**. Criterion 13 requires a
  `REVIEW REQUIRED` label, which exists only as `REVIEW_REQUIRED_LABEL` in
  `engine/decision_workspace.py:102` — the isolated, non-durable, hard-coded FDC-001 workspace.
* **Its baseline and re-run triggers are decision-workspace-bound.** §7 Baseline A is *"Existing FDC-001
  Assessment"*; §12 triggers on *"a relevant **decision-workspace** behaviour change"*; §13 preserves the
  **lane INACTIVE**.
* **Eight dimensions have zero coverage.** Case-insensitive occurrence counts in S2: `mechanical` **0**,
  `arabic` **0**, `novice` **0**, `expert` **0**, `bilingual` **0**, `question quality` **0**,
  `specialist` **0**, `unsafe` **0** **[EXEC]**. One frozen electronics case.

*Consequence:* run unchanged against the Path-N release candidate, criteria 9–14 and the core gate
return structural FAIL / NOT EVALUATED — not because the product lacks value, but because the instrument
is scoped to a paused lane. **The largest Tier-1 item could not measure the premise it exists to test.**

*The two functions, kept distinct (they were conflated in the rejected candidate):* S2 today is a
**competitive product-value benchmark** over one frozen decision-workspace case. A **reasoning-regression
/ journey-quality evaluation** — multi-domain, bilingual, multi-profile, re-runnable per increment — does
not exist in any form. The correct construction is to extend the existing owner to carry the second
function, not to create a second owner.

*Minimum bounded extension — release-gate sufficient, deliberately not a benchmark programme.* Under S2's
own §12 update rules and its versioned-run protocol: add one mechanical frozen case alongside the
electronics case; add EN/AR as an evaluated dimension; add novice and experienced-technical-user profiles;
add criteria for **question quality**, **critical missing gaps**, **unsafe assumptions / prohibited
claims**, and **specialist escalation**; and mark the decision-workspace-only criteria (**9–14**, and the
§6 core gate as written) **NOT APPLICABLE** when the evaluated surface is the Path-N journey, recording
that non-applicability explicitly rather than scoring it FAIL.

*One criterion must not be carried blindly.* Criterion 12's *"affected prior decision marked stale"* is
adjacent to **targeted partial invalidation, which is PROHIBITED in the main product** (D17 / D-AISR-06 /
`PVCG_R4_C…` §2.4) **[REPO]**. Pointing it at the RC without adjudication would set a benchmark criterion
against a committed architectural prohibition. It must be marked NOT APPLICABLE for the Path-N surface,
never satisfied by introducing stale-marking semantics into the main product.

*What one run of the extended S2 proves, stated precisely so it cannot be over-read:* that on the frozen
cases, against Baselines A/B/C, the platform's **output artifact** — evidence visibility, bounded
recommendation or truthful block, provenance, export, prohibited-claim compliance — is or is not superior
to a general assistant, **at one commit, on the cases run, judged by one evaluator**. It does **not**
prove behaviour with real users, novice/expert fit, longitudinal behaviour, commercial usability,
production readiness (S2 §11 says so), or that the result generalises beyond the frozen cases.
**T1-A′ does not substitute for T1-C′**, and no statement anywhere may treat it as doing so.

*Why still Tier 1:* the product's commercial premise is defensible value beyond a general assistant; the
repository holds the instrument for exactly that question and has never used it. Releasing seriously on
an unmeasured premise is the risk; releasing on a **falsely** measured one is worse. Extension first,
then one run. **No benchmark execution is authorized by this record.**

**T1-B · Rendered correction UX (Phase-3C / FPC-02).** The R4 correction mechanism is IMPLEMENTED, but
`web/templates/` is byte-unchanged across the entire R4-I lineage: the route *"is NOT reachable by
clicking anything in the product"* (roadmap L14497–14498) **[REPO]**. A serious user who realises an
earlier answer was wrong **cannot correct it**. For a product whose central promise is governed
epistemic honesty — and which ran an entire PVCG round on user correction — shipping a correction
capability no user can reach is the clearest Tier-1 product gap in the set. Owner unchanged
(**Phase-3C / FPC-02**, classified `CANONICAL PRODUCT REQUIREMENT — ALREADY OWNED BY P4-2 + D17 +
PHASE-3C`); status unchanged (`NOT AUTHORIZED / NOT STARTED`). Backend is implemented, tested and
replay-verified, so the increment is UX-only.

**T1-C′ · One bounded ILT-style real-user round on the release candidate, including at least one
experienced technical participant.** See §6.C. This is the release-candidate decision evidence itself,
executed *on* the RC rather than before it. *(CORRECTED — the rejected candidate's minimum was
novice-inclusive but expert-optional.)*

**T1-D · Truthful disclosure of what this version does not do.** *(NEW.)* Two deferrals in this record
are only honest if the product says so on its own surfaces, and neither currently does:

* **Evidence/validation progression is not available in this version.** `deliverable_assembler.py:49,56`
  ships per-value labels — *"Not validated"*, *"Specialist-reviewed"*, *"Empirically demonstrated"*,
  *"Independently verified"* — while §4 establishes that **no value above the floor is reachable**. Labels
  existing is not the same as levels being active, and no shipped surface discloses the difference.
* **Questioning is a fixed governed set, not adaptive.** This is the binding condition attached to
  deferring T2-G past first release (§4A.3).

The repository already ships the correct pattern for exactly this kind of statement:
`web/ui_text.py:362–363` — *"Version history and branching are not currently provided."* **[REPO]** The
equivalent disclosure for these two does not exist. **Prefer the smallest truthful disclosure**; one
surface can carry both. No UX implementation is authorized by this record, and nothing here implies the
upper evidence levels are active merely because their labels exist.

**Tier 1 contains four classification groups (T1-A′, T1-B, T1-C′, T1-D), corresponding to four §9
matrix rows. It deliberately contains no others.** Throughout §5, a lettered entry is a **classification
group**, not necessarily a single capability: where one release decision governs several capabilities
they share a group, and the exact per-capability tally is the §9 matrix (25 rows, no ambiguous tier).

### TIER 2 — MUST / SHOULD BEFORE PAID ACTIVATION

* **T2-A · WS6 Quantified Requirements extension** — §6.D. *(Classification conflicts with a merged
  record; see §6.D and OD-PDVG-03.)*
* **T2-B′ · WS10 intent content **plus a named display owner** for question explainability** — §6.E.
  *(CORRECTED — WS10's own contract excludes user-facing behavior, so WS10 alone cannot own the render.)*
* **T2-C′ · A bounded **WS16 extension** covering product completeness and user value** — §9.
  *(CORRECTED from "re-execution unchanged", which cannot cover the function — see §6.B.)*
* **T2-D · A bounded user-feedback capture increment** — §8.19. Currently the first link of the
  feedback loop does not exist and is architecturally excluded.
* **T2-E · Evidence-writer mapping** — §6.G. *(RAISED from "precondition of a future increment".)*
* **T2-F · Ordering-defect repair plus a mandatory guard test** — §6.G. *(RAISED from "precondition".)*
* **T2-G · Minimum semantic adaptive questioning** — §4A. *(NEW — from the ownership gap.)*

### TIER 3 — SAFE POST-RELEASE

* **T3-A · Longitudinal project-evolution rendering** — §8.20. Durable history exists; no view renders
  it. The truthful first-release substitute is already committed and shipping: *"Version history and
  branching are not currently provided"* (`web/ui_text.py:362–363`) **[REPO]**.
* **T3-B · FPC-04A specialist-handoff assembly** (in-app preview + durable handoff record) — §6.J.
  Truthful substitute exists: the 14-section deliverable plus P7-I1 canonical export.
* **T3-C · WS15 S8 typed presentation-error boundary.** A future-adapter dependency; the five existing
  guidance seams are documented *"Never raises"*.
* **T3-D · WS14 residual obligations S2, S3, S5** — §6.A.

### TIER 4 — STRATEGICALLY PRESERVED / NOT RELEASE-SEQUENCED

*(Band **relabelled** from "OPTIONAL FUTURE". Tier 4 means **not sequenced into this release**, never
"unimportant". Two members carry HIGH long-term product importance — WS11 and the CAP-12/CAP-13 pair —
and the prior label invited exactly the misreading this record must prevent.)*

* **T4-A · CAP-12** Prototype Materials & Manufacturing Recommendation — §6.M.
* **T4-B · CAP-13** Component Thickness, Specification & Safety Advisory — §6.N.
* **T4-C · CAP-15 / CAP-17** AI provider abstraction and central model config — §6.K. *Conditional:*
  these become Tier 2 **if and only if** live AI usage is ever activated.
* **T4-D · WS11 *current activation*** — blocked by dependency, not merely deferred (§4, §6.F).
  **Long-term product importance: HIGH.** Activation timing and strategic importance are separate axes
  and must not be collapsed.
* **T4-E · WS17 AI Coach; STG; WS-PFV-001** — each already post-gate / reserved / not authorized.
* **T4-F · WS13 Guided Answer Support** — §6.G. No evidenced release case; preserved, not sequenced.

---

## §6. Capability adjudications

### A. WS14 — Adaptive Follow-Up & Completion Logic → **TIER 3 (residuals)**

*Governance:* FORMALLY CLOSED via the No-Valid-RED path — *"WITHOUT BASE RED, IMPLEMENTATION, OR
GREEN"* (`WORKSTREAM_14_FORMAL_CLOSURE.md:169–170`). *Implementation:* **none**;
`engine/adaptive_follow_up.py` absent and guard-enforced **[EXEC]**.

*What active questioning already does:* deterministic fixed-priority gap selection, per-gap
`iterations_open` accounting, a stall reframe at `STALL_THRESHOLD = 3`, and quality-tiered assessment.
*What WS14 would add that is not active:* `completion_condition`-keyed follow-up accounting with a
two-follow-up maximum and defined reset semantics (S2); `OUT_OF_SCOPE` progression effects (S3); a
`decision_reason_code` taxonomy (S5); the WS14/WS15 presentation boundary (S6).

*Does it mine answer content for new material gaps?* **No.** The contract keeps it structural; content
matching is explicitly deferred and blocked across this family. *Does it govern follow-up depth?* Yes,
via S2. *Does it know when enough is collected?* Only in the S2 counting sense — not semantically.
*Determinism / no chatbot drift / one-question-at-a-time:* preserved by construction.

**Adjudication: NOT `MUST BEFORE FIRST SERIOUS RELEASE`.** The active journey already terminates
deterministically and truthfully; WS14's absence bounds depth but does not break the promise. Its
residuals are Tier 3.

**Two orphans recorded, not invented:**
1. **S2, S3, S5 are deferred with no destination workstream named** — only *"a new, separately
   authorized Workstream or contract amendment"* (`:136–139`) **[REPO]**.
2. **S6 is `PROVISIONAL — PENDING WS15 CANONICAL CONTRACT`** (`:131–133`), and WS15 subsequently closed
   without producing that contract. **S6's blocking dependency was closed out from under it.**

### B. WS16 — Final Deliverable / E2E Owner Validation → **the audit function is Tier 2; the workstream is CLOSED**

*Governance:* `WORKSTREAM 16 FORMALLY CLOSED` (§15 row 16), `STAGE DISPOSITIONS PASS ×8 / LIMITATION ×6
/ NOT APPLICABLE ×1 / BLOCKER ×0`, `FINAL LIMITATIONS 10 (OWNER-ACCEPTED, UNREMEDIATED)`, PR #287
**[REPO]**. Scope: fifteen-stage end-to-end validation of the committed application. **WS16 is not
silently rescoped by this record.**

*Prerequisites:* WS13/WS15 were **historical sequencing**, not implementation dependencies — both closed
with no code, and WS16 validated the application as it stood. No prerequisite conflict exists.

**The material finding: five of the ten accepted limitations are now discharged.** Re-tested at this
tip **[EXEC]**:

| ID | Subject | Status now |
|---|---|---|
| WS16-IR-101 | In-memory-only sessions | **DISCHARGED** — `SqliteRecordStore` durable envelope + ledger; `_cold_load_entry` restart rebuild |
| WS16-IR-102 | No durable/atomic recovery surface | **DISCHARGED** — P4-1a/P4-1b/P4-2 + P10-PC1/PC2 read-only render + **P10-PC3 writable resume live** |
| WS16-IR-103 | No authentication layer | **DISCHARGED** — `/register`, `/login`, `/logout`, `/logout-all`, `/account`, `/verify/<token>`, `/account/deactivate` |
| WS16-IR-104 | `/tmp` transcript holds user idea text | **DISCHARGED** — no `/tmp` transcript write remains in `web/app.py` |
| WS16-IR-105 | Partial AR/EN; no page-level RTL | **PARTIALLY DISCHARGED** — `base.html:2` emits `dir="rtl"`; `ui_text.py` carries 3614 Arabic tokens; four guidance seams remain English-only |
| WS16-IR-106 | Progress-vs-verification clarity | **OPEN** (LOW) |
| WS16-IR-107 | Bounded deliverable-synthesis depth | **OPEN** (LOW) |
| WS16-IR-002/003/004 | Representative-journey prototype defects | **OPEN, non-production** (LOW) |

**The register is substantially stale**, having been measured at tip `143a1ed4`. It is an append-only
evidence artifact and is **not rewritten**; the re-measurement is recorded here.

**The genuine ownership hole.** `WORKSTREAM_16_FINAL_DELIVERABLE_OWNER_DECISIONS.md:108–109` (OD-10)
pre-classified two items as WS16 limitations — *"No WS14 adaptive-follow-up implementation"* and
*"No WS15 display-layer adapter"* — and **neither appears among the final ten** **[REPO]**. They were
absorbed into the WS13/WS14/WS15 no-valid-RED closures and then dropped out of WS16's register, so the
two largest missing capabilities named in WS16's own Owner Decisions are **recorded nowhere as an open
WS16 limitation**. This is the concrete evidence that the pre-release audit function needs
re-execution (§9), not that a new owner is needed.

*Is WS16 itself the pre-release completion gate?* **No** — it was deliverable-and-application-scoped
validation at a point in time.

**CORRECTED OWNERSHIP ARCHITECTURE (the rejected candidate claimed WS16 "already owns exactly this
function; only re-execution is needed" — re-verification shows that overstates WS16's own contract).**

WS16's authoritative scope, from its own contract: §1 — *"validate — owner-witnessed, read-only — that
the currently approved **electronics/electrical** MVP journey and deliverable can be honestly completed
end-to-end"*; §2 — a **comprehension** checklist (*where they are · what happened · why · what remains
unresolved · what action is available next · what the system has and has not verified · what limitations
remain*); §4 — *"WS16 must not imply that validation itself improves, redesigns, or implements the
production experience."* **[REPO]**

Occurrence counts in the WS16 contract, case-insensitive **[EXEC]**: `user value` **0**,
`differentiation` **0**, `reasoning quality` **0**, `question quality` **0**, `commercial` **0**,
`mechanical` **0**, `cost` **0**, `resilience` **0**, `integration readiness` **0**, `cognitive load`
**0**, `actionab*` **0**. Only `performance` occurs, once, and in the user time-and-steps sense.

| Dimension | Owned by WS16? |
|---|---|
| capability completeness · UX/cognitive load · evidence truthfulness · failure handling | **YES** |
| actionability · real user value | **PARTIAL** — §2 covers *"what action is available next"* and comprehension, not value |
| reasoning quality · question quality · product differentiation · commercial usability · mechanical-domain coverage | **NO** |
| performance · cost/model resilience · infrastructure/production assurance · integration readiness · longitudinal behavior | **NO** |

Roughly **6 of 14**, and **electronics/electrical only** — while Mechanical is now activated. Unchanged
re-execution therefore cannot deliver a product-completeness and user-value audit. *"E2E" in the
workstream title does not confer the scope; the contract text does.*

**Correct form: a bounded WS16 extension under the existing §15 row.** Not unchanged re-execution; not a
new workstream and **no new numbering**; **not PSRR** — PSRR's registered scope is *"security scan /
penetration test / configuration review"* and production release assurance **[REPO]**, and expanding it
into user-value governance would distort it.

*The extension adds only legitimately adjacent dimensions:* user value · product differentiation ·
reasoning quality · question quality · commercial usability · **mechanical-domain coverage**.

*And it must state explicitly what remains outside it:* performance · cost/model resilience ·
infrastructure and production assurance · integration readiness — so those are not silently absorbed by
an extension that does not own them.

*It must also recover the two dropped OD-10 observations* (no WS14 adaptive-follow-up implementation; no
WS15 display-layer adapter) **where still relevant**, since WS16's own Owner Decisions classified them as
limitations and the final register omits them.

### C. ILT-style real-user-value validation → **TIER 1 (T1-C′)**

*Reconstruction.* `ILT-002_GOVERNANCE_ANCHOR.md` defines an evidence-ledger system that forbids global
state reconstruction; **only per-session evidence is valid** (§3). The campaign was disposed
**INDETERMINATE** under a one-time, explicitly non-precedent authority
(`ILT-002_CAMPAIGN_DISPOSITION_INDETERMINATE_ONE_TIME_AUTHORITY.md` §3/§20). `ILT-002 evidence
collection` is recorded `NOT AUTHORIZED` **[REPO]**. `D-CF6CF2-ILT002-01` fixes the three
`start_ilt002_*` routes as a **governed fixed-domain protocol invariant**, not a classifier defect.

*Therefore:* a new round must be **new authority under a new gate**. ILT-002 must **not** be reactivated,
and its disposition must not be reopened — the one-time authority is non-reusable by construction. A
repeatable execution mechanism **does** exist in form (the ILT-002 execution guide, iteration template
and forms), and it can be reused as *method* without reactivating the campaign.

*Existing nearest evidence:* the FDC-001 practical-use exercise, recorded `COMPLETE — VISIBLE VALUE
CONFIRMED`, ending truthfully at `blocked_by_evidence_gap` (roadmap L74) **[REPO]**. That is an
owner-side exercise on the decision-workspace demo, **not** the main Path-N journey, and it is not a
real-user round.

*Minimum credible coverage — deliberately small, not a research program, CORRECTED for expert coverage:*
a **single bounded round**, on the exact release-candidate tip, with **two ideas** (one
electronics/electrical, one mechanical), **EN and AR coverage**, **at least one novice participant**,
**at least one participant with genuine domain engineering/technical experience**, each run to a
**completed deliverable**, with **journey evidence preserved** and **novice and expert results recorded
and compared separately**. Two ideas, both languages, two to four participants — still a bounded round.

*Why expert coverage is not optional.* A technical-depth product can appear valuable to a novice — who
cannot distinguish a good technical question from a merely plausible one — while being shallow to an
engineer. §17 identifies **question quality** as the product's weakest axis. A novice-only round would
therefore return a **falsely reassuring** result on precisely the dimension most in doubt, and would be
worse than no round at all, because it would be treated as evidence. It tests the seven questions §7.C names — better technical questions;
newly discovered important gaps; useful next validation actions; appropriate specialist escalation;
reduction of uncertainty; usable handoff; clear value beyond a general AI assistant.

**Tier 1**, because every one of those claims is currently **unmeasured with a real user on the current
build**. No implementation in this gate.

### D. WS6 — Quantified Requirements extension → **TIER 2 MUST (conflicts with a merged record)**

*Can the canonical Requirements model represent units, targets, min/max, ranges, thresholds, tolerances,
operating limits, or acceptance criteria?* **No.** `DerivedRequirement`
(`requirement_landscape.py:173–183`) carries `requirement_id, statement, primary_anchor,
supporting_references, source_status, criticality, criticality_authority, criticality_rationale,
resolving_action, linked_risk_ids` — **not one quantitative field** **[REPO]**. A quantitative
requirement can exist only as unstructured prose inside `statement`.

*The distinction §7.D demands — semantic recognition versus canonical structured representation — is
sharper than "no fields", and the evidence is decisive:*

* **Lexical recognition of the vocabulary exists.** `semantic_registry.py:365` registers
  `("tolerance", WORD), ("tolerances", WORD)`; `:641` maps `"threshold"` to its Arabic equivalent.
* **Numeric recognition does not exist at any layer.** The semantic tokenizer is
  `_TOKEN_RE = re.compile(r"[^\W\d_]+")` (`semantic_registry.py:194`) — **digits are excluded from
  tokenization**. Demonstrated on *"The bracket must withstand 250 N and stay within 0.5 mm tolerance
  at 85 degrees"*: the semantic layer yields `['The','bracket','must','withstand','N','and','stay',
  'within','mm','tolerance','at','degrees']` — **every magnitude is gone**, leaving bare unit words with
  no attached value. The `domain_rules` tokenizer keeps digits but splits `0.5` into `'0'` and `'5'`,
  so it cannot carry a decimal either **[EXEC]**.

**No layer of the system can represent, match, or carry a numeric magnitude.** The word "tolerance" is
recognised; the value `0.5 mm` is not.

*Is it a prerequisite for CAP-12/CAP-13 depth?* **Yes, demonstrably.** CAP-13 requires *"proposed
thickness or thickness range; explicit unit"* and forbids precision where *"tolerance, safety factor,
or applicable requirements are insufficient"*; CAP-12 requires environmental and operating assumptions.
Neither is expressible in the current model.

*Release tier — and a conflict that must not be papered over.* The merged TDVP record §5 classifies
this residual as **"post-release / PVCG-successor enhancement — NOT a product-core, release, production,
or commercial blocker"** **[REPO]**. The Owner's PDVG-01 framing calls it *MUST before paid activation*
**[OWNER]**. These are **not compatible on the commercial axis.**

PDVG-01 **cannot silently overwrite a merged classification**. Evaluated from real user value, the
evidence favours the Owner's framing — a paid engineering-decision-support product that cannot carry a
number is materially weak, and two registered capabilities are blocked behind it. **Recommendation:
Tier 2 MUST before paid activation, adopted by explicit Owner supersession of the TDVP §5 row
(OD-PDVG-03)** — not by assertion here. For a bounded, truthfully-labelled first release it is
survivable, so it is **not Tier 1**.

**Extension of WS6 only. No second requirements model** (`D-FPC-MAP-06`).

### E. WS10 — Question Intent Registry → **TIER 2 (T2-B′), safe without WS11**

*Governance:* `WORKSTREAM 10 FORMALLY CLOSED` (contract PR #242; interface + behavioural RED/GREEN)
**[REPO]**. *Implementation:* module present and validated. *Activation:* **dormant — referenced only
by WS11** **[EXEC]**, and, as §3.5 establishes, **no registry data artifact exists**.

*Intended output:* immutable design-time `QuestionIntentRecord`s carrying `primary_intent`,
`answer_objective`, `completion_condition`, `design_gap_id` and a source reference
(`question_intent_registry.py:148–157`) **[REPO]**.

*Relation to explainability and "Why this question?":* direct and strong. Those three fields are exactly
the substrate for telling a user why a question is being asked — the highest-value **Simple Outside —
Deep Inside** surface available from already-closed work.

*Is activation safe without WS11/WS14?* **Yes.** WS10 is a pure design-time metadata registry with no
evaluation coupling, no engine mutation and no scoring effect. WS11 depends on WS10; WS10 depends on
neither.

**Two owners are required, not one — the rejected candidate named only WS10.** WS10's contract L71
places the registry *"without changing question text, serving selection or order, evaluation,
persistence, or **user-facing behavior**"* **[REPO]**. Rendering *"Why this question?"* **is** user-facing
behavior, so it falls outside WS10 by WS10's own text. The split is therefore:

* **Content owner — WS10.** The governed design-time intent data (`primary_intent`, `answer_objective`,
  `completion_condition`) for the 21 committed questions. Authoring it is legitimate WS10 work.
* **Display owner — Phase 3 Product UX/UI.** An adequate existing owner **does exist** and no new one is
  needed: the roadmap records that *"actual UX/UI design and implementation remain **Phase 3** work"*
  **[REPO]**. Its exact state: Phase 3A **FORMALLY CLOSED**; Phase 3B product-decision scope **FORMALLY
  COMPLETE AND CLOSED**; **bounded implementation increments NOT AUTHORIZED / NOT STARTED**
  (`PHASE 3 AND LATER: NOT STARTED / NOT AUTHORIZED`) **[REPO]**. So the display owner is identified and
  inactive — what is missing is **activation**, not ownership.

**A structural economy worth recording:** T1-B's rendered correction UX is owned by **Phase-3C**, which
is the *same* Phase 3 UX lane. **T1-B and T2-B′ share a display owner.** Activating that lane once serves
both; no separate display owner should be invented for explainability.

**Simple Outside — Deep Inside constraint (binding):** one short explanation; no taxonomy; no internal
intent IDs; no dependency graphs.

**Tier 2.** Real user value, safe, bounded — but it is a **content-authoring increment** (21 questions ×
five governed fields) **plus a display activation**, not a wiring switch. It does not weaken the core
promise enough for Tier 1.

### F. WS11 — Question-Aware Evaluation → **TIER 4, BLOCKED BY DEPENDENCY**

*Governance:* `WORKSTREAM 11 FORMALLY CLOSED` (PR #257/#264). *Implementation:* present.
*Activation:* **dormant, zero non-test references** **[EXEC]**.

*What evaluation quality improves when activated?* **On current evidence, none — and it would regress
truthfulness.** WS11 v1 is *"a deterministic, question-bound STRUCTURAL evaluation observation … NOT
semantic answer evaluation"*, whose outcome is a strict function of the **existing, unchanged**
`assess_response` tier (`question_aware_evaluation.py:11–13`) **[REPO]**. Because `DEMONSTRATED` is
unreachable (§4), **`SATISFIED` is unreachable**: every answer would be permanently
`PARTIALLY_SATISFIED` or `NOT_SATISFIED`.

*Prerequisite for WS14, or independent?* Independent. WS14's deferred obligations are accounting and
taxonomy concerns; nothing in them requires WS11.

**Two axes, deliberately not collapsed:**

* **Current activation timing — TIER 4, BLOCKED BY DEPENDENCY.** Activation is NOT recommended until
  §4.b (evidence-writer mapping) and §4.c (ordering repair + guard) are both resolved. Those are the
  exact unlocking prerequisites.
* **Long-term product importance — HIGH.** WS11 is not "optional future". It is a built, reviewed,
  closed evaluator whose value is currently gated by an unrelated defect.

**And a further finding that survives the unlock:** even once `DEMONSTRATED` becomes reachable, WS11's
own **D7.1.T** states a `SATISFIED` result would mean *only* that the generic quality tier was reached —
explicitly **not** semantic fulfilment of `answer_objective` or `completion_condition`, and it must emit
*"no content-intent alignment claim"* **[REPO]**. So a user-facing "SATISFIED" would overclaim unless
content-semantic matching (the deferred WS11.2, which does not exist — §4A.1) also exists. **Recorded:
semantic matching remains necessary before any user-facing `SATISFIED` claim can be meaningful.** WS11 is
not redesigned here.

This also rejects the standing implication that WS10/WS11 activation is a single joint decision: **they
are separable, and only WS10's content work is currently safe.**

### G. WS13 — Guided Answer Support → **TIER 4; no evidenced case for it**

Closed via OD-14 / WS13-CD-2 with `valid observable defect count: 0` across the five display-layer
seams; `engine/guided_answer_support.py` absent and guard-enforced **[REPO/EXEC]**. The five existing
seams are pre-existing and *"NOT silently reclassified as completed WS13 implementation"*.

Classified independently, **not** because it sits in sequence: the bounded read-only search found the
existing seams deterministic, exception-free, provenance-traceable and non-overclaiming. **No release
case exists.** Classified **Tier 4 — strategically preserved / not release-sequenced**: not "safe
post-release valuable" (Tier 3 implies an evidenced value case with a truthful substitute) but carrying
**no currently evidenced case at all**. Any future work requires new evidence. The prior `3/4` straddle
is removed — an ambiguous tier is not a classification.

### H. WS15 — Guidance Consolidation → **TIER 3 (S8 only)**

Closed without a display-layer adapter; the five seams remain deterministic and honest **[REPO]**. Its
own boundary statement scopes it to *"deterministic cross-module presentation consolidation
**governance**"* — governance of consolidation, not consolidation. The only residual is **S8**, a typed
presentation-error boundary that is a *future-adapter dependency, not a current defect*. **Tier 3.**

### I. Golden reasoning evaluation / benchmark → **REJECTED as a new increment. NO NEW OWNER.**

*Distinguishing the two kinds of testing, from repository truth:*

* **Deterministic software/invariant testing — owned and green.** WPS-001 invariants
  (`20 passed / 1 skipped`), the replay corpus (`tests/replay/cases/`), golden snapshot fixtures
  (`tests/golden/`), `engine/scoring.score_case()`, and the full 4418-test suite **[EXEC]**. This lane
  is **frozen** by `CLAUDE.md` and excluded from remediation by the Deliverable Stabilization plan §6.
* **Reasoning-quality evaluation — owned, and never executed.** The Bicycle Brake-Light Competitive
  Benchmark (S2) is precisely a reasoning-and-value evaluation instrument.

*Does a corpus exist that catches regressions in the seven named dimensions?* Partly, and the mapping
matters: important next questions, critical gaps, unsafe/fabricated claims, specialist escalation and
readiness outcomes are all covered by S2's 18 criteria and core success gate; Arabic/English parity is
covered by the PVCG-R3 semantic-stability suite (579 tests) and the bilingual test classes;
novice/expert handling is covered by **nothing** — that is the one genuine coverage hole, and it belongs
inside the T1-C′ ILT round, not in a new corpus.

*Testing the review hypothesis:*

* *"MUST before any model/provider change"* — **moot at this tip.** There is no model in the live path
  (§3.3). The requirement should attach to the **AI-activation gate itself**, if one is ever opened.
* *"SHOULD before paid activation"* — **accepted, and satisfied by T1-A′ (extended S2)**, not by S2 as
  it stands today.
* *"not necessarily Tier 1"* — **rejected in part**: *executing the existing instrument* is Tier 1
  (T1-A′, after the bounded S2 extension). *Building a new corpus* is not needed at all.

**CORRECTION carried from T1-A′:** the rejected candidate said reasoning-quality evaluation *"is already
owned by S2"* and marked §8 row 2 **ADEQUATE**. S2 owns the *competitive product-value* function; the
*reasoning-regression / journey-quality* function is **not covered by S2 in its current form** (eight
dimensions at zero coverage; core gate scoped to the Technical Decision Workspace increment). The
conclusion that **no new owner is needed** survives — but only because S2 is **extended** to carry the
second function, not because it already did. §8 row 2 is re-marked **PARTIAL**.

**Creating a "Golden Reasoning Benchmark" owner would duplicate S2 and risk conflation with the frozen
replay/golden fixture lane** (where `GOVERNANCE_MODEL.md:33–34` still records two open replay-era
violations, in a lane PDVG-01 does not touch). *Integration Before Duplication* applies: **no new
benchmark owner; execute the one that exists.**

### J. FPC-04A — Specialist Handoff → **TIER 3**

*Scope:* Specialist Handoff Pack **Assembly**, split from FPC-04B Delivery, with *missing bounded
elements only*: an internal in-app preview; a durable handoff-package record; assembly of the current
**non-stale** snapshot, evidence, gaps, contradictions, specialist category and bounded specialist
questions (roadmap L3577–3580). Status `NOT AUTHORIZED / NOT STARTED` **[REPO]**.

*Relationship to existing deliverable/export:* the 14-section deliverable already **is** a reviewable
snapshot, and P7-I1 provides a data-minimized canonical outward projection; P7-I3 proves a
vendor-neutral adapter. *Is durable specialist handoff missing?* The **durable handoff-package record**
and the **in-app preview** are missing; the content is not.

*Relationship to CAP-12/CAP-13:* FPC-04A is the correct **near-term truthful substitute** for both —
routing a bounded question to a human specialist is exactly what the platform should do while
materials/thickness advisory remains unbuilt. *External tools:* one-way export only; **never** to be
described as round-trip.

**Tier 3** — a truthful first-release substitute exists. The decision-support boundary is preserved:
**InventorAI is not an engineering sign-off authority**, and FPC-04A must not become one.

### K. CAP-15 / CAP-17 — model / provider resilience → **TIER 4 today; conditionally Tier 2**

*Current architecture, measured (§3.3):* one dormant 69-line advisor; **no provider port**
(contrast `engine/payment_provider_port.py`, which is a fully realized port with a fake adapter);
**no central model/prompt configuration**; **no retry**; total unconditional fallback
(`except Exception: return None` → deterministic question bank); **no cost or latency instrumentation**.
Two hardcoded model literals exist and **disagree** — `claude-sonnet-4-20250514`
(`ai_advisor.py:49`) versus `claude-3-5-sonnet-20241022` (`benchmark/run_benchmark_v1.py:8`) **[EXEC]**
— which is latent evidence *for* CAP-17's premise but is not a live defect, since neither runs in
production.

*Classified separately, as §10 requires:*

| Horizon | CAP-15 | CAP-17 |
|---|---|---|
| First serious release | **Tier 4 — no action** | **Tier 4 — no action** |
| Paid activation | **Tier 4 — no action** *(unless AI activated)* | **Tier 4 — no action** *(unless AI activated)* |
| Future | Tier 2 **at** the AI-activation gate | Tier 2, alongside CAP-15 |

This is **their own registered rule**, not a new judgement: CAP-15's *Critical Lean rule* is *"do NOT
create speculative provider abstractions before live AI usage justifies the boundary"* **[REPO]**.
With zero live AI usage, building either now would be exactly the speculative abstraction the register
forbids. **No provider migration is invented; no provider is selected.**

### L. PC-10 — product completeness & user value audit → **FUNCTION OWNED; NO NEW ITEM CREATED**

*First, the literal fact, scoped to the base tip:* **`PC-10` did not exist anywhere in the repository
at base `1295ed08…`** — zero occurrences, case-insensitive, across all tracked files **[EXEC]**. *(This
record and its tracker entries are the first commit to contain the string, so the claim is asserted of
the base, never of the candidate.)* (`P10-PC1`, `P10-PC2`, `P10-PC3` are distinct
Phase-10 product-capability gates.) PC-10 is a reviewer label, not a repository item — so the question
is about the **function**, not the identifier.

*Re-proving the hypothesis (does any current gate own a final pre-release audit of product completeness
and user value?):*

| Candidate | Verdict |
|---|---|
| **WS16** | **PARTIAL — the closest owner, but not the whole function.** Fifteen-stage read-only end-to-end validation with a limitation/blocker register and durable Owner stage acceptance — genuinely this function for **completeness, comprehension, evidence truthfulness and failure handling**. But its contract is **electronics/electrical only** and carries **zero** occurrences of user value, differentiation, reasoning quality, question quality, commercial usability, mechanical coverage, cost, resilience, integration readiness or cognitive load (§6.B): roughly **6 of 14 dimensions**. Executed once, at an older tip. |
| **PSRR** | **NO — and must not be distorted.** Its authoritative scope is production security / operational / release **assurance**, registered as mandatory before public production. It is not user-value governance. |
| **Phase 10** | **NO.** Commercial, legal, security, operational readiness — adjacent, not this. |
| **Product Foundation phases** | **NO.** Phase-sequencing authority, not an audit instrument. |
| **FPC** | **NO.** Capability-integration mapping, non-authorizing. |
| **ILT** | **PARTIAL.** Real-user evidence, not completeness auditing. Complementary (T1-C′). |
| **Benchmark governance** | **PARTIAL.** S2 measures competitive product value, not completeness. Complementary (T1-A′). |

**The closest adequate owner is WS16 — but only once extended.** Two safeguards apply here at once, and
both are honoured. *Against creating a duplicate owner:* WS16 already owns the audit machinery, the
limitation register and the Owner stage-acceptance discipline, so a new workstream would duplicate it —
rejected. *Against false reuse:* WS16's contract does **not** reach user value, differentiation,
reasoning quality, question quality, commercial usability or mechanical coverage, so unchanged
re-execution would force-fit the function into an owner that cannot carry it — also rejected.

The correct bounded form is therefore a **WS16 extension under the existing §15 row** — no new workstream
and **no new number** — which must (i) add the six adjacent dimensions above, (ii) name performance,
cost/model resilience, infrastructure and production assurance, and integration readiness as **outside**
it, (iii) re-test the ten limitations, five of which are now discharged (§6.B), and (iv) recover the two
OD-10 items that fell out of the register. Registered as **T2-C′**. **No PC-10 implementation is
created, and PSRR is not expanded.**

### M. CAP-12 — deep reconstruction → **TIER 4, preserved on the future roadmap**

*Status:* `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`; register is `NON-ACTIVATING and
NON-AUTHORIZING`. *Implementation:* none. *Feasibility gate:* required — *"a dedicated
materials-and-manufacturing feasibility gate (§6)"*, then source review, **data licensing review**,
knowledge-source contract, deterministic rule/calculation boundary, increment contract, Owner decisions,
separate authorization, RED/GREEN, independent verification, closure **[REPO]**.

*Boundaries already registered:* must not create a mandatory material specification; must not claim
final engineering approval; must not fabricate material properties, manufacturer specifications,
standards or certifications; must not infer material from visual appearance; must not replace qualified
specialist review; must clearly separate prototype from production material; declining it must not
block the journey. *Overlaps:* CAP-01, CAP-08–CAP-11, CAP-13, CAP-14, WS-PFV-001; technical-guidance
content defers to D13; prototype/validation to WS-PFV-001; specialist routing to D13 + AISR.

**Critical verification, as §12 demands:**

* *Deep enough to become an implementable contract?* **No — directionally deep only.** The entry is a
  rich capability description, not a contract: it has no field schema, no determinism boundary, no
  acceptance gates and no RED items.
* *Missing recommendation-status mapping?* **Yes — and this is a precise, checkable asymmetry.**
  CAP-13 enumerates four levels (`CONCEPTUAL · PROTOTYPE-SUITABLE · ENGINEERING REVIEW REQUIRED ·
  UNABLE TO RECOMMEND`); **CAP-12 names "recommendation status" as a proposed field but enumerates no
  levels** **[REPO]**. CAP-12 must not silently inherit CAP-13's — they are registered as distinct
  capabilities that *"must not be consolidated"*.
* *Missing data/property substrate?* **Yes.** No material-property data, no source, no licensing
  position. `AI SOLE AUTHORITY` is prohibited by the register's own non-goals and by the committed
  no-claim boundary; without a licensed property substrate the capability could only fabricate.
* *`UNABLE TO RECOMMEND` behaviour?* Present in **CAP-13's** level set, **absent** from CAP-12's.
* *Dependent on Quantified Requirements?* **Yes** (§6.D).

**Tier 4 — not promoted, not deleted.** Repository truth supports its long-term value; the evidence does
not support promoting it. Its earliest step remains its own feasibility gate.

### N. CAP-13 — deeper safety standard → **TIER 4, with the highest safety bar in the register**

*Governs (verified against the register entry):* geometry ✓, material ✓, load ✓, support/joints ✓, use
conditions ✓, impact/fatigue ✓, temperature/environment ✓, manufacturing method ✓, safety factor ✓,
units ✓ (*"explicit unit"* required), ranges ✓ (*"prefer an advisory range rather than false
precision"*), tolerances ✓, operating limits ✓, warnings ✓ (seven mandatory categories: general,
structural, electrical/battery, heat/pressure, medical/food/human-contact, children/consumer safety,
chemical/outdoor), false precision ✓ (explicitly prohibited), insufficient evidence ✓
(`UNABLE TO RECOMMEND`), specialist routing ✓, calculation/simulation/test requirements ✓ **[REPO]**.

**The safety rule is already correctly stated in the register:** the system must not provide a precise
thickness where dimensions, geometry, loads, supports, joints, temperature, environment, manufacturing
method, tolerance, safety factor, or applicable requirements are insufficient. `Recommended thickness:
X mm` without adequate evidence is prohibited **by the entry itself**.

**Does CAP-13 require the following? Each answered from repository truth:**

| Requirement | Verdict |
|---|---|
| WS6 Quantified Requirements | **YES — hard blocker.** *"Explicit unit"* and thickness ranges are unrepresentable and even untokenizable today (§6.D). |
| CAP-12 material/process context | **YES.** Thickness without material and manufacturing method is meaningless. |
| Component/subsystem substrate extension | **YES.** `engine/subsystem_model.py` exists but is referenced only by `idea_state.py`; it is *metadata only* and confers no specialist behaviour **[EXEC]**. |
| Domain profiles / checks | **YES** — via P9-QS and the domain packs. |
| Specialist routing | **YES** — D13 + AISR + FPC-04A. |
| Standards / data licensing | **YES** — unresolved, shared with CAP-12. |
| External simulation / calculation | **YES** — and **excluded** by the committed no-claim boundary; must route out, never be built in. |
| Evidence / provenance | **YES** — and **blocked by §4**: the ladder value that would justify a thickness statement (`DEMONSTRATED` / `EMPIRICALLY_DEMONSTRATED`) has no writer, and the comparison defect would mis-order it. |
| Deterministic reassessment | **AVAILABLE** — P4-2 full re-evaluation + the R4 correction/replay path. |

**Tier 4.** CAP-13 is the deepest capability in the register and the furthest from feasible: it is
blocked on quantified requirements, on CAP-12, on a licensed property substrate, and on the §4 evidence
writer. Promoting it now would create precisely the unsafe-precision risk its own entry forbids.

---

## §7. CAP-12 ↔ CAP-13 dependency architecture (§14) — every link traced to its owner

The proposed chain is **tested, not copied as authority**:

| # | Link | Current owner | State |
|---|---|---|---|
| 1 | Requirements | **WS6** `engine/requirement_landscape.py` | **IMPLEMENTED + ACTIVE** |
| 2 | Quantified Constraints | **WS6 extension** (T2-A) | **MISSING LINK** — no representation, no tokenization (§6.D) |
| 3 | Confirmed Component / Subsystem Context | **§5-I3** `engine/subsystem_model.py` | **DORMANT** — referenced only by `idea_state.py`; metadata only |
| 4 | Material / Process Candidates | **CAP-12** | **FUTURE-ONLY** — recorded, not authorized, needs its feasibility gate |
| 5 | Geometry / Thickness / Specification Reasoning | **CAP-13** | **FUTURE-ONLY** — recorded, not authorized |
| 6 | Failure / Safety Checks | `GroundedRisk` + `engine/safety_signal.py`; depth → **STG / WS-PFV-001** | **ACTIVE (shallow)** + **FUTURE (depth)** |
| 7 | Evidence / Validation | Increment-2 axes + **WS7** `validation_plan.py`; ladder → **CAP-11** | **ACTIVE (floor only)** — **upper ladder unreachable (§4)** |
| 8 | External Tool / Specialist | **P7-I1 / P7-I3** (out, proven); **D13 + AISR** (specialist); **FPC-04A** (handoff) | **ACTIVE one-way export** + **FUTURE inbound** |
| 9 | Provenance-backed Result | `ProvenanceAnchor`, `SupportingReference` | **ACTIVE (single provenance value reachable)** |
| 10 | Deterministic InventorAI Reassessment | **P4-2** full re-evaluation + **PVCG-R4** correction/replay | **IMPLEMENTED + ACTIVE** |

**Missing links:** 2. **Dormant links:** 3, and the upper half of 7. **Future-only links:** 4, 5, the
depth half of 6, the inbound half of 8.

**Duplicate risks identified and refused:** a second requirements model (link 2 must be a WS6
*extension*); a second evidence ladder (link 7 must reuse Increment-2 + CAP-11); a second specialist
model (link 8 is D13 + AISR); a second dependency/propagation engine — **targeted partial invalidation
remains PROHIBITED** by D17 / D-AISR-06 / PVCG-R4-C §2.4 and is not reintroduced by any link above.

**Safe integration boundary:** links 4–5 consume 1–3 and emit into 7–8; they must never write link 10,
and must never bypass link 7's provenance.

**No internal CAD / FEA / CFD / PCB engine is proposed.** Repository evidence establishes the opposite:
physics simulation, CAD/CAE, certification and specialist sign-off are excluded by the committed
truthfulness boundary — the product *"makes NO final safety / compliance / certification / approval /
legal / patent / engineering-validation claim"* **[REPO]**. Any such capability would require its own
separately justified gate, and none exists. **Integration Before Duplication** is preserved throughout.

---

## §8. The ten product-completeness coverage checks (§18) — and §§15–17, 19–20

| # | Check | Owner status | Impl./activation | Release relevance | Recommendation |
|---|---|---|---|---|---|
| 1 | Real-world user-value validation | **PARTIAL** — ILT method + FDC-001 exercise; ILT-002 collection NOT AUTHORIZED | Not executed on current build | **Tier 1** | **T1-C′** — one bounded round under new authority, incl. an experienced technical participant |
| 2 | Golden reasoning evaluation / benchmark | **PARTIAL** *(corrected from ADEQUATE)* — S2 owns competitive product-value; reasoning-regression is uncovered in its current scope | **Never run**; template empty; 8 dimensions at zero coverage | **Tier 1** | **T1-A′** — **extend S2**, then one run; **create no new owner** |
| 3 | Decision quality / calibration | **ADEQUATE in structure, BROKEN in reach** — Increment-2 axes + CAP-11 | Floor values only; upper ladder unreachable; latent ordering defect | **Tier 1 (disclosure) + Tier 2 (T2-E, T2-F)** | T1-D disclosure now; mapping + guarded repair before paid activation; **no parallel confidence system** |
| 4 | Cost / latency / model resilience | **ADEQUATE** — CAP-15 / CAP-17 | No live AI ⇒ nothing to abstract or meter | **Tier 4** *(Tier 2 iff AI activated)* | **No action** |
| 5 | Controlled user feedback → improvement loop | **UNOWNED (first link)** | **ABSENT** and architecturally excluded | **Tier 2** | **T2-D** — bounded capture increment |
| 6 | UX / cognitive load | **PARTIAL** — Product UX/UI workstream (post-WS16, not started) | Journey is one-question-at-a-time today | **Tier 3** | No action beyond T1-B |
| 7 | Actionability / next-step quality | **ADEQUATE** — WS7 validation plan + deliverable §10/§11/§14 | Implemented and active | Post-release | **No action** |
| 8 | Explainability / "Why this question?" | **SPLIT** — WS10 owns intent content; **Phase 3 Product UX/UI** owns the render (identified, NOT ACTIVATED) | Dormant; **no registry artifact exists**; display lane not started | **Tier 2** | **T2-B′** — author content **and** activate the display owner (shared with T1-B) |
| 8b | **Semantic adaptive questioning** *(NEW ROW)* | **UNOWNED — TRUE GAP (§4A)** | absent; every candidate owner disclaims it in its own contract | **Tier 2 (T2-G)**; SHOULD before first release, MUST before paid | **OD-PDVG-10** — Owner adjudicates ownership; no owner assigned here |
| 9 | Longitudinal project intelligence | **PARTIAL** — durable ledger + supersession + replay | Stored, **never rendered**; **no timestamp column** | **Tier 3** | **T3-A** — post-release |
| 10 | Product completeness & user-value audit | **PARTIAL** *(corrected from ADEQUATE)* — WS16 covers ~6 of 14 dimensions, electronics-only | Executed once, at an older tip | **Tier 2** | **T2-C′** — bounded **WS16 extension**; **not re-execution**, **not PSRR**, **not a new owner** |

### §15 — Technical claim-strength / calibration

The existing architecture **can** express asserted / reasoned / demonstrated / specialist-reviewed /
empirically-demonstrated / independently-verified — the vocabulary is committed and CAP-12/CAP-13 can
**reuse it** rather than create a parallel system. Two gaps must be resolved **before** any CAP
implementation, and both are flagged here rather than fixed:

1. **No writer exists for any value above the floor of any axis** (§4). The unresolved mapping is:
   *which governed user action, through which route, writes a non-default quality, validation status or
   provenance — and what evidence must accompany it?*
2. **The ordering defect** (§4.3) must be repaired as a precondition of the first increment that makes
   `DEMONSTRATED` reachable.

*Calculation/simulation-backed* and *prototype-tested* have **no representation at all**: the prototype
surface is proposal-only, `SuccessCriterion` is *"planning metadata ONLY: never graded … never treated
as a result"*, and `validation_plan.py` states it *"generates NO level-3 (supplied) or level-4
(verified) claim"* **[REPO]**. A generic `Technically feasible — confirmed` claim is therefore
structurally impossible today, and must never be authorized without matching evidence.

### §16 — Simple Outside — Deep Inside (mandatory test on every Tier 1 / Tier 2 item)

| Item | Verdict |
|---|---|
| **T1-A′** extended-S2 run | **PASS** — evaluation only; zero user-facing surface. |
| **T1-B** correction UX | **PASS** — one affordance on an existing page; deepens honesty without exposing any internal model. **Constraint required:** must not surface the record ledger, supersession edges, or replay internals. |
| **T1-C′** ILT round | **PASS** — observation of the existing journey. |
| **T2-A** quantified requirements | **AT RISK — constraint required.** A units/threshold/tolerance form is exactly the "giant engineering form for novices" failure. **Contract must require progressive disclosure and optionality: a novice must complete the journey without entering a single number.** |
| **T2-B′** WS10 explainability | **PASS — and it is the strongest Simple-Outside/Deep-Inside item available**: one short "why this question" line backed by governed design-time intent. **Constraint:** one sentence, no taxonomy, no intent-id exposure. |
| **T2-C′** WS16 extension | **PASS** — internal. |
| **T2-D** feedback capture | **PASS** — constraint: one lightweight control, never a survey. |

Flagged for cognitive overload unless contract-constrained: **T2-A**. Also flagged for the future:
**CAP-12/CAP-13**, whose full field lists would overwhelm a novice if surfaced directly.

### §17 — Product differentiation verdict

*If a serious user uses InventorAI today, with only active capabilities, what defensible value exists
beyond a carefully prompted general-purpose AI assistant?* Answered as a release-value classification,
without marketing language:

* **Already active differentiation — real and defensible.** Governed epistemic state that a chat
  assistant structurally cannot provide: a durable INSERT-only record ledger with provenance anchoring;
  supersession that retains history immutably; deterministic full replay of a session through the
  unchanged engine; a 14-section structured deliverable with requirement/risk linkage and a validation
  plan; committed no-claim truthfulness boundaries; deterministic, reproducible progression;
  correction with mandatory **full** re-evaluation (targeted partial invalidation prohibited); durable
  writable resume; canonical vendor-neutral export; EN/AR semantic stability.
* **Essential differentiation still dormant or planned.** Question explainability (WS10 — content does
  not exist); reachable correction (T1-B); quantified requirements (T2-A).
* **Important strengthening.** Adaptive follow-up depth (WS14 residuals); specialist handoff assembly
  (FPC-04A); longitudinal evolution rendering (T3-A).
* **Optional enhancement.** CAP-12, CAP-13, CAP-15/CAP-17, WS17, STG.

**The honest verdict, stated without softening.** Differentiation today is **strong on the output and
memory side and weak on the input side**. The deliverable, the evidence discipline and the durable
governed state are genuinely defensible. The **questioning** is not: 21 static questions selected by
fixed priority, with no adaptivity, no answer-content mining, no user control over what to work on
(`select_next_gap` is pure fixed priority; WS8's expressed-intent objectives P8-1/P8-2 were deferred to
WS10/WS11, both dormant) **[EXEC]**. On question quality alone, a well-prompted general assistant is
competitive or better. **InventorAI's defensible claim is not "better questions" — it is "a governed,
durable, replayable, truthfully-bounded record of an engineering decision."**

**T1-A′ (extended S2) tests the output-side claim; T1-C′ (the ILT round, with expert coverage) tests the
input-side claim. Neither substitutes for the other** — and the rejected candidate's line *"T1-A exists
to test exactly this"* was itself the error, since S2 carries **no question-quality criterion** (§6.I).
Marketing must not run ahead of either result.

### §19 — Controlled feedback loop

Required chain: *user feedback → structured observation → evaluation evidence → reviewed improvement →
regression proof → controlled release.*

* **Link 1 — user feedback: ABSENT, and architecturally excluded.** No rating, no "was this useful",
  no report-a-problem route, no feedback table across 44 routes and 15 tables.
  `web/result_feedback.py` runs the opposite direction (system→user, display-only).
  `web/observability.py` bans analytics and behavioural tracking outright, with a six-field allowlist
  (`component, outcome, error_class, detail_code, count, duration_ms`) that structurally cannot carry
  free text **[REPO/EXEC]**.
* **Links 3–6 exist and are strong**: the 4418-test suite, the replay/golden corpora, universal
  guardrail smoke, independent review, owner-gated merge and post-merge verification.

**The loop cannot start.** ILT/Product-Reality mechanisms produce *episodic* evidence, not a standing
channel. A **bounded capture increment is warranted later (T2-D)** — explicitly **not** uncontrolled
automatic learning: capture only, with every downstream step remaining governed and human-reviewed.

### §20 — Longitudinal project intelligence

*Does the system merely store history, or support meaningful project evolution?*

**It stores, and renders nothing.** Durable: the project envelope and the append-only assertion ledger,
ordered by `seq`, with non-destructive supersession. There is no timestamp column in the durable schema
(`record_store.py:65`) **[REPO]**.

**FRAMING CORRECTED.** The rejected candidate wrote *"no wall-clock time axis at all"* in a way that
could be read as a deficiency requiring repair. **A wall-clock timestamp is NOT required.** A monotonic
`seq` plus non-destructive supersession already answers the whole of the value question — *what changed,
in what order, and what superseded what*. Adding a time column would widen an INSERT-only durable schema
for presentation convenience, and **no evidence in this gate justifies that**. The absence is a
**non-finding**; the missing piece is rendering, not storage. The
only before/after capture in the engine is `IterationLog`
(`maturity_before` / `maturity_after`, `progression_loop.py:1099`), which is **in-memory only, never
persisted and never rendered**. No template iterates the ledger; no route exposes history, timeline,
changes or versions; the deliverable has no "what changed" section. The single computed change view —
`readiness: prior → new` — lives in the isolated, non-durable, hard-coded FDC-001 Decision Workspace
and displays only the **latest** event **[EXEC]**.

So of the six evolution events named in §20: *unknown→evidenced*, *requirement changed*, *risk closed*,
*blocker added/removed*, *prototype evidence added*, *readiness changed* — **none has a rendered
representation** in the main flow. The substrate is genuinely there; the intelligence is not.

**Release value: Tier 3.** The truthful substitute is already committed and shipping
(`ui_text.py:362–363`) — and that same line is the precedent T1-D applies to the evidence ladder.

**Smallest useful future form:** a bounded, deterministic, provenance-backed **"what changed" view over
the existing ledger**, ordered by `seq`, rendering supersession edges — **no wall-clock axis, no durable
schema change**. **This must not become a generic project-management system**: no tasks, no assignees,
no schedules.

---

## §9. Required output matrix (§22)

| Capability | Existing Owner | Governance State | Implementation State | Activation State | User-Value Gap | Dependencies | Release Tier | Owner Decision? | Next Authorized Gate |
|---|---|---|---|---|---|---|---|---|---|
| **Bounded S2 extension + one run** | **S2 Bicycle Brake-Light Benchmark (extended, not replaced)** | authoritative + closed (protocol); extension PLANNED | instrument complete but scoped to the Technical Decision Workspace lane | **never executed**; 8 dimensions at zero coverage | differentiation claim unmeasured, and unmeasurable by S2 as it stands | RC tip | **1** | **OD-PDVG-01** *(revised)* + **OD-PDVG-11** | S2 extension gate, then one run |
| Rendered correction UX | Phase-3C / FPC-02 | recorded / NOT AUTHORIZED | backend implemented | **not user-reachable** | user cannot correct an answer | R4 route (done) | **1** | **OD-PDVG-02** | Phase-3C/FPC-02 UX increment |
| ILT-style real-user round **incl. experienced technical participant** | new authority (ILT method reused) | ILT-002 collection NOT AUTHORIZED | n/a | not executed | all value claims unmeasured with users; question quality unmeasured | RC tip; T1-A′ | **1** | **OD-PDVG-06** *(revised)* | new bounded round gate |
| Quantified Requirements | **WS6 extension** | closed + PLANNED extension | none | n/a | no numeric representation at all | none | **2 MUST** | **OD-PDVG-03** *(supersedes TDVP §5)* | WS6 extension contract |
| Question intent **content** | **WS10** | authoritative + closed | loader present, **no data** | dormant | no governed intent data | content authoring | **2** | **OD-PDVG-04** *(revised)* | WS10 content gate |
| Question explainability **render** | **Phase 3 Product UX/UI** (3A/3B closed; implementation NOT AUTHORIZED) | authoritative + planned | none | **not activated** | no "why this question?" | WS10 content; **shared display lane with T1-B** | **2** | **OD-PDVG-12** | Phase-3 UX activation gate |
| Pre-release completeness & value audit | **WS16 (bounded EXTENSION, existing §15 row)** | authoritative + closed; extension PLANNED | executed once, older tip, **~6 of 14 dimensions, electronics-only** | n/a | user value, differentiation, reasoning/question quality, commercial usability, mechanical coverage all unowned by WS16 as scoped | RC tip | **2** | **OD-PDVG-05** *(revised)* | WS16 extension gate — **not PSRR**, no new number |
| User-feedback capture | **none (first link)** | no current owner | absent | n/a | improvement loop cannot start | none | **2** | — | bounded capture contract |
| Longitudinal evolution view | ledger + replay | authoritative + implemented (storage) | stored, unrendered | n/a | no evolution visible | **none — `seq` + supersession suffice; no timestamp required** | **3** | — | post-release bounded "what changed" view |
| Specialist handoff assembly | **FPC-04A** | recorded / NOT AUTHORIZED | none | n/a | no durable handoff record | output + persistence | **3** | — | FPC-04A assembly gate |
| WS14 residuals S2/S3/S5 | **WS14 (no successor named)** | closed, obligations deferred | none | n/a | bounded follow-up depth | new authorization | **3** | — | new increment |
| WS14 residual S6 | **orphaned** — pending a contract WS15 never produced | closed | none | n/a | presentation boundary undefined | WS15 (closed) | **3** | — | new increment |
| WS15 S8 error boundary | **WS15** | closed, obligation deferred | none | n/a | future-adapter dependency | future adapter | **3** | — | new increment |
| WS13 guided answer support | **WS13** | closed, 0 defects found | none | n/a | none evidenced | new evidence required | **4** | — | none |
| Question-aware evaluation | **WS11** | authoritative + closed | present | dormant | **would regress truth if wired**; `SATISFIED` unreachable, and semantic-only after unlock | **T2-E + T2-F**; then WS11.2-like semantic matching | **4 (activation)** · **importance HIGH** | — | blocked until T2-E/T2-F resolved |
| **Semantic adaptive questioning** | **NONE — TRUE OWNERSHIP GAP (§4A)** | **no current owner**; every candidate disclaims it in its own contract | none | n/a | next question never adapts to answer content | T2-E/T2-F not required; independent | **2 (T2-G)** — SHOULD pre-release, MUST pre-paid | **OD-PDVG-10** | Owner adjudication of ownership |
| Evidence-progression + fixed-question-set **truthfulness disclosure** | **Phase 3 Product UX/UI** (same display lane as T1-B and T2-B′) | **owner identified; implementation increment NOT AUTHORIZED / NOT STARTED** | none — disclosure content not authored, render not implemented | not activated | labels shipped for states that cannot occur; no surface states the question set is fixed | Phase-3 UX activation (**OD-PDVG-12**) | **1 (T1-D)** | **OD-PDVG-13** | smallest truthful disclosure |
| Evidence-**writer mapping** | Increment-2 / CAP-11 | authoritative + implemented (structure) | **floor only** | n/a | readiness axis is a constant `False` | none | **2 (T2-E)** | **OD-PDVG-08a** | governed-writer definition gate |
| Ordering-defect repair **+ guard test** | Increment-2 / `progression_loop` | authoritative + implemented | **latent defect, unguarded** | n/a | strongest evidence would sort below `REASONED` | none | **2 (T2-F)** | **OD-PDVG-08b** | bounded repair + guard |
| CAP-12 materials/manufacturing | **CAP-12** | recorded / NOT AUTHORIZED | none | n/a | no materials guidance | T2-A; licensing; §4 | **4** | **OD-PDVG-09** | CAP-12 feasibility gate |
| CAP-13 thickness/safety advisory | **CAP-13** | recorded / NOT AUTHORIZED | none | n/a | no specification guidance | T2-A; CAP-12; §4; substrate | **4** | **OD-PDVG-09** | CAP-13 feasibility gate |
| AI provider abstraction | **CAP-15** | recorded / NOT AUTHORIZED | none | n/a | none (no live AI) | AI activation | **4** | — | AI-activation gate |
| Central prompt/model config | **CAP-17** | recorded / NOT AUTHORIZED | none | n/a | none (no live AI) | CAP-15 | **4** | — | AI-activation gate |
| AI Coach | **WS17** | post-gate, NOT AUTHORIZED | none | n/a | out of scope now | WS1–16 closed | **4** | — | separate authorization |
| Structured Technical Guidance | **STG / D13** | reserved / inactive | none | n/a | domain depth | separate authorization | **4** | — | separate authorization |

No new numbering is created for any existing workstream. **Two rows name no owner** — user-feedback
capture and semantic adaptive questioning — and both are recorded as **having no current owner** rather
than being assigned one. Neither is force-fitted into an adjacent owner to make the ledger tidy.

---

## §10. Owner decisions required (§21) — surfaced, none recorded

Only decisions repository truth genuinely requires. Each states why the Owner must decide, the bounded
options, a recommendation, and what stays unauthorized until chosen.

**OD-PDVG-01 (REVISED) — Authorize a bounded S2 extension, then one run on the release candidate.**
*Why the Owner:* S2's criteria are owner-approved, so changing its case set or criteria is an owner act;
§11 also reserves result approval. *Why revised:* S2 as it stands is scoped to the Technical Decision
Workspace lane and cannot measure the Path-N RC (T1-A′). *Options:* (a) authorize the bounded extension
**and** one run; (b) authorize one run of S2 unchanged; (c) defer to post-release; (d) decline.
*Recommendation:* **(a)**. **(b) is specifically not recommended** — it would return structural
FAIL / NOT EVALUATED on criteria 9–14 and yield a result aimed at the wrong surface. *Until chosen:* no
extension and no run; the differentiation claim stays unmeasured.

**OD-PDVG-02 — Authorize the Phase-3C / FPC-02 rendered correction UX as a bounded pre-release
increment.** *Why the Owner:* FPC-02 is `NOT AUTHORIZED / NOT STARTED` and only the Owner opens it.
*Options:* (a) authorize a minimal in-page correction affordance over the existing route; (b) authorize
the fuller "What changed?" presentation as well; (c) defer. *Recommendation:* **(a)** — smallest
increment that makes an implemented, tested capability reachable. *Until chosen:* users cannot correct
answers, and no surface may imply they can.

**OD-PDVG-03 — Resolve the Quantified-Requirements release-class conflict.** *Why the Owner:* the merged
TDVP §5 classifies it *not a commercial blocker*; the Owner's framing makes it MUST before paid
activation. **A merged classification cannot be superseded by an executor.** *Options:* (a) supersede
TDVP §5 and admit it as Tier 2 MUST before paid activation; (b) affirm TDVP §5 and keep it
post-release; (c) fold it into a future STG scope. *Recommendation:* **(a)** — the evidence is stronger
than TDVP's row assumed (no numeric representation *or tokenization* at any layer; CAP-12 and CAP-13
both blocked behind it). *Until chosen:* TDVP §5 stands and no extension is authorized.

**OD-PDVG-04 (REVISED) — Authorize WS10 intent-content authoring.**
*Why the Owner:* the registry content **does not exist**, and WS10's own contract makes the authored
intent taxonomy new normative data requiring owner review. *Why revised:* the rejected candidate bundled
the user-facing render into this decision; WS10's contract L71 excludes user-facing behavior, so the
render is a separate decision (**OD-PDVG-12**). *Options:* (a) authorize content authoring for the 21
committed questions; (b) defer. *Recommendation:* **(a)**. *Until chosen:* WS10 stays a loader with no
data. **Independent of WS11, which must not be activated (§6.F).**

**OD-PDVG-05 (REVISED) — Authorize a bounded WS16 extension for product completeness and user value.**
*Why the Owner:* WS16 is formally closed; extending its scope is an owner act, and the added and excluded
dimensions must be fixed in advance. *Why revised:* the rejected candidate proposed unchanged
re-execution on the claim that WS16 "already owns exactly this function"; WS16's contract covers roughly
6 of 14 dimensions and is electronics-only (§6.B), so re-execution cannot deliver the audit. *Options:*
(a) bounded extension under the existing §15 row — adding user value, product differentiation, reasoning
quality, question quality, commercial usability and mechanical-domain coverage, and naming performance,
cost/resilience, infrastructure assurance and integration readiness as **outside** it; (b) unchanged
re-execution; (c) a new numbered workstream; (d) fold into PSRR. *Recommendation:* **(a)** — reuses the
existing owner, creates no new number, and **avoids distorting PSRR**, whose registered scope is security
scanning, penetration testing, configuration review and production release assurance. **(d) is
specifically not recommended.** *Until chosen:* the five stale limitations and the two dropped OD-10
items have no re-test path, and the audit function stays unowned in its non-WS16 half.

**OD-PDVG-06 — Authorize one bounded ILT-style real-user round under new authority.** *Why the Owner:*
ILT-002 evidence collection is `NOT AUTHORIZED` and its disposition is a **non-reusable one-time
authority**; a new round cannot borrow it. *Options:* (a) authorize one bounded round with the corrected §6.C
minimum coverage — **two ideas (electronics + mechanical), EN and AR, ≥1 novice and ≥1 experienced
technical participant, results recorded separately**; (b) the novice-only variant; (c) a larger
programme; (d) release without real-user evidence. *Recommendation:* **(a)**. **(b) is specifically not
recommended** — novice-only evidence is falsely reassuring on question quality, the axis §17 identifies
as weakest; (c) is the oversized-research-program failure §7.C warns against. *Until chosen:* no round;
ILT-002 stays closed and untouched.

**OD-PDVG-07 — Decide whether the Tier-1 set becomes the committed Minimum Launch-Conformance Set.**
*Why the Owner:* MLC is explicitly undefined and its definition is already a standing open Owner
decision; §1 shows the Tier-1 set functions as a candidate definition. *Options:* (a) adopt Tier 1
(T1-A′, T1-B, T1-C′, T1-D) as the MLC; (b) adopt a different set; (c) leave MLC undefined and treat Tier 1 as
advisory. *Recommendation:* **no recommendation for (a) can be made in this candidate**, for two evidenced
reasons — **and OD-PDVG-10 is not one of them** (§4A.5 withdraws that linkage as unsound; an unowned
**Tier-2** item is not a member of the launch-conformance set, so its ownership cannot gate the set's
definition). The two reasons that do hold: **(i)** the corrected set has **not itself been independently
reviewed** — the prior set was judged INCOMPLETE by review, and this repair agrees on its own evidence
that it rested on an S2 item unable to measure its premise, an expert-free ILT round, and an ownership
ledger asserting zero unowned gaps; **(ii)** **T1-A′'s scope is undefined pending OD-PDVG-11**, and a
conformance set cannot be frozen while one of its members has unapproved scope. Both are discharged by
ordinary process, not by resolving the ownership gap. *Until chosen:*
`MINIMUM LAUNCH-CONFORMANCE SET SATISFIED: NO` and `MLC DEFINITION FROZEN: NO` stand unchanged, and
**no set in this record may be treated as the MLC.**

**OD-PDVG-08 (CONTAINER — NOT ITSELF ACTIONABLE; its actionable children are 08a and 08b below)** —
originally framed as: bind the evidence-writer mapping and the ordering repair as preconditions of the first
evidence-ladder increment.** *Why the Owner:* §4 records a verified latent logic defect and an
unreachable ladder that jointly gate WS11, CAP-11, CAP-12 and CAP-13; PDVG-01 cannot repair either.
*Why revised:* binding the repair to "the first evidence-ladder increment" left the trigger dependent on
someone **recognising** a future change as one — not a safeguard, since the masking invariant **is
enforced by no test**. The decision is split:
**OD-PDVG-08a — evidence-writer mapping (T2-E).** Define which governed user action, route and
qualifying evidence may write each non-default quality / validation-status / provenance value.
*Options:* (a) authorize the definition as a bounded governance increment before paid activation;
(b) defer and record the readiness axis as permanently constant. *Recommendation:* **(a)**.
**OD-PDVG-08b — ordering repair + guard test (T2-F).** *Options:* (a) authorize a bounded code repair
**with a mandatory guard test** before paid activation; (b) bind it as a precondition of the first
ladder increment; (c) no action. *Recommendation:* **(a)** — it removes the dependence on recognition.
*Until chosen:* the defect stays masked but live, and WS11 activation stays unsafe.

**OD-PDVG-09 — Confirm the future disposition of CAP-12 and CAP-13.** *Why the Owner:* §12/§13 require
that they neither be promoted for attractiveness nor be allowed to disappear. *Options:* (a) preserve
both as Tier 4, each behind its own feasibility gate, sequenced after T2-A; (b) promote one; (c) retire
one. *Recommendation:* **(a)** — repository truth supports long-term value and refuses near-term
feasibility. *Until chosen:* both stay `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`, unconsolidated.

**OD-PDVG-10 (NEW) — Adjudicate the semantic adaptive questioning ownership gap.**
*Why the Owner:* §4A establishes that no workstream, capability or phase owns `material answer content →
changed canonical technical state → next-question decision materially adapts`, and every candidate owner
disclaims it in its own committed text. Assigning an owner — or declining to — is a product-priority act
only the Owner can perform, and until it is performed the inherited line `UNOWNED TDVP GAP COUNT: 0`
cannot be truthfully carried. *Options:* **(A)** register a **new bounded owner**; **(B)** convert the
named-only **WS11.2** into a real governed contract **and** extend its scope to semantic next-question
adaptation — admissible **only if** the architecture supports it without violating WS11's D14
transition-decision boundary, which today it does **not**, so (B) additionally requires a governed D14
amendment; **(C)** another existing-owner extension, admissible **only** on independent proof of
sufficiency — none was found in §4A.1; **(D)** decline or defer, recording the limitation explicitly and
permitting **no** implied adaptive-questioning claim anywhere. *Recommendation:* **(A)**, sequenced after
the Tier-1 set and before paid activation; (B) is coherent but reopens a boundary deliberately set;
(C) is unsupported on current evidence; (D) is honest and acceptable **provided** T1-D carries the
limitation. *Until chosen:* no owner exists, no adaptivity may be claimed, and
`UNOWNED CAPABILITY GAP COUNT (PDVG-01 reconstruction): 1` stands. **This decision does not block the
first serious release, does not block MLC definition, and does not convert T2-G's SHOULD into a MUST**
(§4A.5). Option **(D)** is genuinely available: declining is a resolution, and a declined Tier-2 item
sits outside the launch-conformance set exactly as an unadjudicated one does.

**OD-PDVG-11 (NEW) — Approve the S2 bounded-extension scope.** *Why the Owner:* S2's criteria are
owner-approved, so the added case, dimensions and criteria — and marking criteria 9–14 NOT APPLICABLE to
the Path-N surface — require owner approval. *Options:* (a) approve the T1-A′ minimum extension;
(b) approve a narrower subset; (c) decline. *Recommendation:* **(a)**. **Binding constraint:**
criterion 12's stale-marking must be marked NOT APPLICABLE and **never** satisfied by introducing
targeted-partial-invalidation semantics into the main product, which remains PROHIBITED. *Until chosen:*
T1-A′ cannot proceed.

**OD-PDVG-12 (NEW) — Name and activate the display owner for question explainability.** *Why the Owner:*
WS10's contract excludes user-facing behavior; the adequate owner is the **Phase 3 Product UX/UI** lane,
whose implementation increments are `NOT AUTHORIZED / NOT STARTED`. *Options:* (a) activate one bounded
Phase-3 UX increment covering **both** the T1-B correction affordance and the T2-B′ explainability line,
since they share the lane; (b) activate for T1-B only; (c) defer explainability. *Recommendation:*
**(a)** — one activation serves both and avoids inventing a second display owner. *Until chosen:* WS10
content, if authored, has nowhere to render.

**OD-PDVG-13 (NEW) — Authorize the truthful "what this version does not do" disclosure (T1-D).**
*Why the Owner:* it is a user-facing product statement. *Options:* (a) one combined disclosure covering
evidence-progression unavailability **and** the fixed non-adaptive question set; (b) evidence only;
(c) decline. *Recommendation:* **(a)** — (b) leaves the T2-G deferral unstated, and that statement is the
condition on which deferring T2-G past first release depends. *Until chosen:* the product ships evidence
labels for states that cannot occur, with no disclosure.

**No other Owner decision is required by this gate.** Nothing above is recorded as decided.

---

## §10A. New-evidence self-invalidation test, and the mandatory contradiction ledger

Every major PDVG-01 finding was tested against the question: *does this newly discovered fact invalidate
an ownership, tier, release, completeness or roadmap assumption inherited from TDVP or from the rejected
candidate itself?* Historical facts are preserved; only current dispositions move.

| Subject | Self-invalidation verdict |
|---|---|
| **Semantic adaptive questioning** | **INVALIDATES** TDVP T-10 / `UNOWNED TDVP GAP COUNT: 0` at the constituent level (§4A) |
| **S2 benchmark scope** | **INVALIDATES** the rejected candidate's ADEQUATE marking and its T1-A (T1-A′) |
| **WS16 scope** | **INVALIDATES** the rejected candidate's "exactly the function" claim and T2-C (§6.B) |
| **Quantitative representation** | Confirms and strengthens T2-A; **contradicts** merged TDVP §5's commercial classification (unchanged since the rejected candidate — still surfaced, still not overwritten) |
| **Evidence-ladder reachability** | **INVALIDATES** the rejected candidate's single-precondition treatment; splits into T1-D / T2-E / T2-F (§4) |
| **WS10 user-facing boundary** | **INVALIDATES** the rejected candidate's single-owner T2-B (§6.E) |
| **WS11 meaning** | **INVALIDATES** the "optional future" framing; activation timing and strategic importance separated (§6.F) |
| **ILT user coverage** | **INVALIDATES** the expert-optional minimum (§6.C) |

### Contradiction ledger (mandatory)

| Earlier proposition | New evidence | Current disposition | Owner action needed? |
|---|---|---|---|
| **TDVP §4/§8:** `TRUE RESIDUAL GAP COUNT: 0` — no topic lacks an adequate owner *(merged, PR #558)* | Contract-by-contract trace: WS10 L71, WS11 D14, WS14 L59/L227, WS4 §17's explicit no-owner disclaimer; WS11.2 has no contract, file or §15 row **[REPO/EXEC]** | **Historical statement preserved as authority-at-that-time and NOT rewritten.** Current: `UNOWNED CAPABILITY GAP COUNT (PDVG-01 reconstruction): 1`. TDVP mapped the *topic* to the WS8–WS17 family; PDVG-01 reconstructed the *capability each contract admits*, and no member admits this one | **YES — OD-PDVG-10** |
| **TDVP §5:** quantified-requirement fields are *"post-release … NOT a product-core, release, production, or **commercial** blocker"* *(merged)* | No layer can represent **or tokenize** a magnitude (`semantic_registry._TOKEN_RE` drops digits; `domain_rules` splits `0.5`); CAP-12 and CAP-13 both hard-blocked behind it **[EXEC]** | **Historical classification preserved.** PDVG-01 recommends Tier 2 MUST before paid activation — **by Owner supersession only**, never by executor fiat | **YES — OD-PDVG-03** |
| **Rejected PDVG `fd7de207…` §6.I / §8 row 2:** S2 coverage **ADEQUATE**; extension refused | S2 §6 core gate scoped *"For the first Technical Decision Workspace increment"*; criterion 12 needs `validity_status`, which occurs in **no** Python file; criterion 13's label exists only in `engine/decision_workspace.py:102`; eight dimensions at **zero** occurrences; lane INACTIVE **[REPO/EXEC]** | **Superseded within PDVG-01 by T1-A′** — bounded S2 extension under the **existing** owner, then one run. Row re-marked **PARTIAL**. No second benchmark owner | **YES — OD-PDVG-01 (revised), OD-PDVG-11** |
| **Rejected PDVG `fd7de207…` §6.L:** *"WS16 — YES, this is the owner… Exactly the function"*; T2-C = unchanged re-execution | WS16 §1 is read-only completion validation, **electronics/electrical only**; §2 is a comprehension checklist; eleven dimension terms occur **zero** times in its contract **[REPO/EXEC]** | **Superseded within PDVG-01 by T2-C′** — bounded **WS16 extension** under the existing §15 row, added and excluded dimensions named. **PSRR not expanded** | **YES — OD-PDVG-05 (revised)** |
| **Rejected PDVG §12:** `da8c1fd8…` *"is preserved as immutable rejected evidence"* | Absent from that candidate's bundle; no remote ref contains it **[EXEC]** | **Corrected to a per-medium statement** (§12): local Git object only, now also bundled; **not remotely verifiable** | No |
| **Rejected PDVG §17:** *"T1-A exists to test exactly this"* (question quality vs a general assistant) | S2 carries **no** question-quality criterion | **Corrected:** T1-A′ tests the output-side claim, T1-C′ the input-side claim; neither substitutes for the other | No |
| **Rejected PDVG §20:** *"no wall-clock time axis at all"* | `seq` + non-destructive supersession already answer *what changed, in what order, what superseded what* | **Framing corrected:** a timestamp is **not required**; the absence is a non-finding; the gap is rendering, not storage | No |

**This ledger exists so that governance consistency cannot hide product truth.** Four of the seven rows
move a disposition that would have been more convenient to leave alone.

---

## §11. Status ledger (effective ONLY if/when this candidate is merged and post-merge verified)

```
NO NEW TDVP PROGRAM REQUIRED: YES                  (traced to merged TDVP §7/§8)
UNOWNED TDVP GAP COUNT (TDVP, historical): 0       (committed phrasing: TRUE RESIDUAL GAP COUNT: 0)
UNOWNED CAPABILITY GAP COUNT (PDVG-01 reconstruction): 1 — semantic adaptive questioning (§4A)
ADAPTIVE-QUESTIONING OWNER ASSIGNED: NO (Owner decision OD-PDVG-10 pending)
MATERIAL OWNED PRODUCT-DEPTH WORK REMAINS: YES     (traced; independently re-measured)
FIRST SERIOUS RELEASE REQUIRES PRE-RELEASE INCREMENTS: YES — [OWNER] PREMISE, NOT REPOSITORY-DERIVABLE
PDVG-01 IMPLEMENTATION STARTED: NO
TIER-1 IMPLEMENTATION AUTHORIZED: NO
PSRR GO: NO
DEPLOYMENT AUTHORIZED: NO
PRODUCTION AUTHORIZED: NO
PAID ACTIVATION AUTHORIZED: NO
NEW WORKSTREAMS CREATED: 0
NEW OWNERS CREATED: 0
NEW NUMBERING FOR EXISTING WORKSTREAMS: NONE
TDVP REOPENED OR RENAMED: NO
PVCG REOPENED: NO
TIER CLASSIFICATION GROUPS (§5 entries — labelled groups, NOT literal item counts):
  T1 = 4 (T1-A′, T1-B, T1-C′, T1-D)   T2 = 7 (T2-A…T2-G)   T3 = 4 (T3-A…T3-D)   T4 = 6 (T4-A…T4-F)
TIER MATRIX ROWS (§9, exact, one row per capability): T1 = 4, T2 = 8, T3 = 5, T4 = 8; TOTAL = 25
GROUPING RULE: a §5 bullet is a classification group and may span more than one §9 row where one
  release decision governs several capabilities (T2-B′ = WS10 content + Phase-3 render; T4-C = CAP-15 +
  CAP-17; T4-E = WS17 + STG + WS-PFV-001, of which WS-PFV-001 has no §9 row of its own; T3-D = WS14
  S2/S3/S5 and the orphaned S6 are two rows). No §9 row carries an ambiguous tier.
TIER 4 BAND MEANING: STRATEGICALLY PRESERVED / NOT RELEASE-SEQUENCED (never "unimportant")
OWNER DECISIONS SURFACED: 14 — 01, 02, 03, 04, 05, 06, 07, 08a, 08b, 09, 10, 11, 12, 13
  OD-PDVG-08 is a NON-ACTIONABLE CONTAINER / parent heading only; its two children OD-PDVG-08a and
  OD-PDVG-08b are the independently actionable decisions and are counted separately.
  ACTIONABLE OWNER DECISIONS: 14 (§10 carries 15 bolded OD headings — the 14 actionable plus the
  OD-PDVG-08 container, which is never counted as a decision)
OWNER DECISIONS RECORDED AS MADE: 0
WS10 ACTIVATED: NO    WS11 ACTIVATED: NO (activation NOT recommended — blocked by dependency)
WS12 ACTIVATED: NO    stage3_evaluator INTEGRATED: NO
FULL ADAPTIVE QUESTIONING ACTIVATED: NO
RENDERED CORRECTION UX DELIVERED: NO (owner Phase-3C / FPC-02; unchanged)
AI ACTIVATED: NO — the live user path makes zero external AI calls
NEW DOMAINS ACTIVATED: NO (electronics_electrical + mechanical unchanged)
MINIMUM LAUNCH-CONFORMANCE SET SATISFIED: NO
MLC DEFINITION FROZEN: NO — the corrected Tier-1 set is NOT proposed as the MLC; the two evidenced
  reasons are (i) it has not been independently reviewed and (ii) T1-A′'s scope is undefined pending
  OD-PDVG-11. OD-PDVG-10 does NOT gate MLC definition (§4A.5)
OD-PDVG-10 BLOCKS FIRST SERIOUS RELEASE: NO      OD-PDVG-10 BLOCKS MLC DEFINITION: NO
SEMANTIC ADAPTIVE QUESTIONING BEFORE FIRST RELEASE: SHOULD (not MUST); BEFORE PAID ACTIVATION: MUST
"FIRST SERIOUS RELEASE" DEFINED AS A REPOSITORY FACT: NO
BENCHMARK RUN EXECUTED: NO       S2 EXTENSION AUTHORIZED: NO       ILT ROUND EXECUTED: NO
MAIN RECONCILIATION STARTED: NO
LATENT EVIDENCE-ORDERING DEFECT: RECORDED, NOT REPAIRED (executable delta = 0); guard test REQUIRED
  by T2-F so the masking invariant stops depending on recognition
REJECTED CANDIDATES: 11 — da8c1fd8, 5974baf7, fd7de207, d6d55db0, 97233ad9, 8cddcda3, fa93acef,
  ecc9bde9, 1a9cdad7, b287c4b6, 615fcb8e
  All eleven are retained as local refs AND included in the SHA-preserving bundle; NONE published to origin
```

---

## §12. Rejected evidence — exact preservation status, no ambiguous language

**Eleven PDVG-01 candidates have been rejected.** **None is published to any remote.** Preservation is
stated per-candidate and per-medium; nothing is described merely as "preserved", and no aggregate in this
record is left at a superseded value (see §12.3 on how this count is derived).

| Rejected SHA | Rejected by | Local Git object / ref | In the repair bundle | Published remote ref | Verifiable at `origin` |
|---|---|---|---|---|---|
| `da8c1fd8734a8e983b39ff4abac647cabe2b8f41` | Creator Grill (CG-1, CG-2) | **YES** — `refs/rejected/pdvg01-cg1-cg2` | **YES** | **NO** | **NO** |
| `5974baf75bbdd7b33bf5fcf6d4f08e9e12e0a412` | Creator Grill (CG-3) | **YES** — `refs/rejected/pdvg01-cg3` | **YES** | **NO** | **NO** |
| `fd7de207027c25a4f43249630616efc9755893e8` | **Independent External Review** | **YES** — `refs/rejected/pdvg01-independent-review` | **YES** | **NO** | **NO** |
| `d6d55db0537d5c91ae3e1f34a8ffad63914942c1` | Creator Re-Grill (RG-1) | **YES** — `refs/rejected/pdvg01-rg1` | **YES** | **NO** | **NO** |
| `97233ad9b81f1dfd0e1f1264258937dcbe884c97` | Creator Re-Grill (RG-2) | **YES** — `refs/rejected/pdvg01-rg2` | **YES** | **NO** | **NO** |
| `8cddcda37c65a520006b54b06b1d284fcf27c310` | **post-Creator Instruction-to-Result Audit** (P1–P5) | **YES** — `refs/rejected/pdvg01-audit-p1p5` | **YES** | **NO** | **NO** |
| `fa93acef98496d79e961023a226bcf23d4617b2c` | **post-Grill audit** — stale rejected-evidence aggregate | **YES** — `refs/rejected/pdvg01-audit-aggregate` | **YES** | **NO** | **NO** |
| `ecc9bde93bfd5c89974d1f2e8e990fe2a7defc28` | **Independent External Review (substantive)** — F-1 governance-consistency | **YES** — `refs/rejected/pdvg01-independent-review-2` | **YES** | **NO** | **NO** |
| `1a9cdad79d3ce44152da2a6bb3d608aa7f4d0509` | **Reviewer micro-repair directive** — §12.1a historical-reference precision | **YES** — `refs/rejected/pdvg01-121a-precision` | **YES** | **NO** | **NO** |
| `b287c4b61fe07c9e9d1ed60338fad6ed16a7d634` | **Pre-review audit (B24)** — stale §12.4 aggregate; fragile §12.1a self-count | **YES** — `refs/rejected/pdvg01-b24` | **YES** | **NO** | **NO** |
| `615fcb8ecdd5f5497181e5e8f4b2e415838b9c78` | **Creator pre-freeze self-check** — B24-F2 recurrence: locative enumeration falsified by §12.1f | **YES** — `refs/rejected/pdvg01-b24-locative` | **YES** | **NO** | **NO** |

**Verified this gate [EXEC]:** **no remote ref contains any of the eleven; each of the eleven is absent
from `origin`.** The rejected identities of `fd7de207…` (tree `e68b8f15…`), `fa93acef…` (tree
`66d7bba5…`), `ecc9bde9…` (tree `f7f924c3…`), `1a9cdad7…` (tree `834cfc6a…`) and `b287c4b6…` (tree
`7bd71f6f…`) and `615fcb8e…` (tree `5d9607cd…`) are intact — each a single-parent child of
`1295ed08…`. **None of the eleven is amended, rebased, or published.**

**Candidate `fd7de207…`'s own §12 claimed `da8c1fd8…` "is preserved as immutable rejected evidence"
without qualifying the medium.** The Independent Reviewer could not verify that and was right not to.
Corrected: it was true **as a local Git object only**, and it was **absent from that candidate's bundle**,
which carried the branch tip alone — a statement scoped to *the three rejected candidates that existed at
that earlier candidate stage*, not to the current set.

**Current aggregate, unambiguous:** *All eleven rejected candidates are retained as local refs and
included in the SHA-preserving bundle; none is published to `origin`.*

### §12.3 How this count is derived, and why it does not go stale on freeze

The aggregate above is **eleven**, and it includes this repair candidate's immediate predecessor
`615fcb8e…`. That is deliberate, and it resolves a self-referential trap that produced the very defect
being repaired here: a count written before the rejected set was complete becomes false the moment the
next candidate is rejected.

**Derivation rule applied:** the current aggregate is fixed only once a Grill-passed candidate exists,
and it counts **every candidate rejected for this gate up to and including the predecessor of the
surviving candidate**. A surviving candidate is not a member of its own rejected set, so a passing
candidate's aggregate is stable at freeze. Were this candidate itself rejected, its successor would
re-derive the count one higher — **the rule, not the number, is what carries forward**. It has been
exercised at every repair since it was written, and this clause deliberately does not enumerate those
exercises, for the same reason the §12.4 classification clause states no number.

**Topology note.** Synchronising the count strictly *after* a Grill pass would require a further commit,
which would itself become the reviewed candidate and reopen the same question. The structure used
instead: the count is written to its **fixed point** (predecessors, excluding self), the candidate is
frozen, the Grill and a machine-derived aggregate check then **confirm** the written value against the
actual ref set rather than changing it. Verification, not mutation, closes the loop — so the frozen
candidate is truthful at freeze and stays truthful.

### §12.4 Cross-Surface Repair Closure Rule

The general lesson from the surviving roadmap citation, stated once and kept short:

> **When a candidate claims a defect has been repaired across multiple canonical surfaces: enumerate
> every affected occurrence; verify each corrected proposition at the final candidate; and do not infer
> closure from repairing one document, or from a string count reaching zero in one file.**

This extends §12.3's aggregate fixed-point rule from *counts and lists* to *propositions*. The RG-2
repair searched for the defective string, found and fixed every instance **in the record**, and treated
a zero count there as closure — while the same defect stood on the roadmap, which `CLAUDE.md` designates
as a controlling surface. A count reaching zero in one file is evidence about that file and nothing
more. Closure is per-proposition and per-surface, verified at the candidate that claims it.

**Classification discipline applied across all four surfaces.** Every occurrence of a rejected-evidence
number is classified before editing, and three kinds are kept apart: **current aggregates** (re-derived
to the then-current value at every repair — this clause deliberately states **no** number, because a
number written here is a second copy of the aggregate and goes stale exactly as the first one did);
**historical subsets** (left in place but made explicit about which subset they name — e.g. *"the three
rejected candidates that existed at that earlier candidate stage"*); and **candidate-specific
statements** (left exact where already correctly scoped). Numbers that count something other than
rejected candidates — the Independent Review's *three blocking findings*, the ENFORCING pin locations,
the domain packs, the gap types — were deliberately **not** touched.

### §12.1 Prior Creator-Grill rejections (retained)

* **`da8c1fd8…` — CG-1, self-contaminated repository claims.** Asserted in the present tense that
  `PC-10` has *"zero occurrences"* and *"first serious release"* is *"not a committed repository term"*.
  Both true at base `1295ed08…`, **false at that candidate's own SHA**, because its own tracker entries
  introduce both strings. Repaired by scoping every absence claim to the base tip.
* **`da8c1fd8…` — CG-2, incorrect enumeration.** Stated `validation_status` has *"no writer"* and
  enumerated *"the only occurrences"*, omitting `safety_signal.py:494` — an assignment on the distinct,
  frozen, non-persisted `SafetySignal` object. The substantive finding survived; the enumeration did not.
* **`5974baf7…` — CG-3, off-by-one citations.** `idea_state.py:12` named the section comment rather than
  the constants (`:13–15`); the `SafetySignal` vocabulary was cited at `:47` rather than `:48`.

### §12.1a Creator Re-Grill rejections of the repair itself

The repair candidate was Grilled twice more before it survived:

* **`d6d55db0…` — RG-1, residual contradiction.** §6.B had been corrected to *"WS16 covers ~6 of 14
  dimensions"*, but **§6.L still asserted `WS16 | YES — this is the owner … Exactly the function`** and
  registered T2-C as unchanged re-execution. The document contradicted itself on the very finding the
  repair existed to fix. Also repaired: two un-primed `T1-A` references in §6.I, and OD-PDVG-07's option
  (a), which still listed the superseded three-item Tier-1 set.
* **`97233ad9…` — RG-2, citations that do not resolve.** References cited `web/ui_text.py:361` for a
  quoted sentence that lives at `:362–363`; line 361 is the entry key (`"UI_SENS_DATA_02": {`).

  **Corrected enumeration — there were FOUR defective citations at the RG-2 stage, not three.** Machine
  re-derived from the rejected trees **[EXEC]**:

  | Candidate | Record `:361` (live) | Roadmap `:361` (live) | Defective total |
  |---|---|---|---|
  | `d6d55db0…` (RG-1) | 3 | 1 | **4** |
  | `97233ad9…` (RG-2) | 3 | 1 | **4** — rejected for this defect |
  | `8cddcda3…` | 0 (repaired to `:362–363`) | **1 — MISSED** | 1 |
  | `fa93acef…` | 0 | **1 — survives** | 1 |
  | `ecc9bde9…` | 0 | **1 — survives** | 1 |

  **The RG-2 repair was incomplete, and this record previously said otherwise.** Three of the four
  occurrences — all in this record — were repaired at `8cddcda3…`. The fourth, in the
  `ACTIVE_EXECUTION_ROADMAP.md` PDVG-01 entry, was never touched: it **survived `8cddcda3…`,
  `fa93acef…` and `ecc9bde9…`**, and it is the finding on which the substantive Independent External
  Review **rejected `ecc9bde9…`**. It is repaired in the present candidate. `ACTIVE_INCREMENT_CONTRACT.md`
  and `CURRENT_PROJECT_STATE.md` never carried a `ui_text` citation (0 at every stage), so four is the
  complete historical total across all four surfaces.

  *(**Every** `web/ui_text.py:361` reference remaining in this record is a historical quotation of a
  repaired defect; **none is a live citation**. Every live citation to that sentence, on every surface,
  resolves to `web/ui_text.py:362–363`. This clause deliberately neither counts those references nor
  enumerates where they sit: both are self-references that this record's own narrative falsifies as it
  grows — which is precisely how B24-F2 arose, and how it recurred once more before this wording
  settled.)*

### §12.1b Post-Creator Instruction-to-Result Audit rejection of `8cddcda3…`

The audit found five residual **internal-governance** defects — none of them a truthfulness or evidence
failure, all of them internal inconsistency between what the repair established and what the record
still said:

* **P1 — opening scope contradicted the record's own findings.** The header still described PDVG-01 as
  classifying *"already-owned work"* while §9 carried **two rows with no current owner**. Repaired to the
  four-kind formulation; the owned-only premise is **not** restored.
* **P2 — a SHOULD behaving as a MUST.** OD-PDVG-07 said completeness *"cannot be established while
  OD-PDVG-10 is unresolved"*, which made an ownership question gate a conformance question and rendered
  OD-PDVG-10's option D self-defeating. Re-adjudicated from first principles in **§4A.5**; the linkage is
  **withdrawn as unsound**. MLC stays unfrozen for two evidenced reasons that are not OD-PDVG-10.
* **P3 — miscount.** Fourteen decisions were listed and thirteen counted. 08a and 08b are independently
  actionable — a governance-definition increment and a bounded code repair with a guard — so they are
  counted separately, not merged to preserve the old number.
* **P4 — ambiguous counts.** §5 entries were being reported as literal item counts while §9 held more
  rows, and WS13 carried an ambiguous `3/4`. §5 entries are now labelled **classification groups** with a
  stated grouping rule, the exact §9 row tally is published beside them, and WS13 is resolved to Tier 4
  on the evidence that no release case exists.
* **P5 — T1-D owner understated.** The row said *"none — gap"* while the record elsewhere identified
  Phase 3 Product UX/UI as an adequate display owner. Corrected to owner-identified /
  implementation-not-authorized, with the missing capability named. **No new owner was manufactured.**

### §12.1c Post-Grill audit rejection of `fa93acef…`

One residual defect, of the aggregate-staleness class the bounded review had already flagged: §12 still
carried *"no remote ref contains any of the three"* and *"All three rejected SHAs are carried in this
repair bundle"* — statements written when three candidates existed and never updated as the set grew to
five and then six, even though the same §12's table, its opening sentence and the status ledger had all
been kept current. The table said six; the prose said three. Repaired by classifying every
rejected-evidence reference on all four surfaces and stating the current aggregate unambiguously, with
the derivation rule in §12.3 so the count cannot silently go stale again.

### §12.1d Independent External Review (substantive) rejection of `ecc9bde9…`

The reviewer **concurred with the substantive architecture** — ownership adjudication, S2, WS16, the
evidence-ladder tiers, Quantified Requirements, WS10/WS11, ILT, feedback-loop ownership, MLC logic, the
tier model, product differentiation and CAP-12/CAP-13 — and independently re-proved the measured base,
rating truthfulness **HIGH**. The single **BLOCKING** finding was **F-1**, governance internal
consistency: the roadmap's PDVG-01 entry still cited `web/ui_text.py:361`, a surviving instance of the
defect for which `97233ad9…` had already been formally rejected, while this record simultaneously
claimed the repair complete and enumerated it as three occurrences rather than four. Non-blocking
findings F-2 (OD-PDVG-08 container wording), F-3 (un-primed tier labels) and F-5 (WS11.2 phrasing) are
folded into the same repair; F-4 (§12 section order) is deliberately **not** actioned — presentation
order only, and reordering would be churn.

### §12.1e Reviewer micro-repair directive — rejection of `1a9cdad7…`

One residual historical-reference precision defect in §12.1a's own closing parenthetical, which said the
*"single"* surviving `:361` string sat in *"this bullet and §12.1c"*. Both halves were wrong: **two**
occurrences remain in this record (§12.1a and §12.1d), and **§12.1c contains none**. Independently
re-derived before repair by attributing every `:361` line in the record to its owning sub-section
**[EXEC]**. The repaired sentence stays scoped to *this record*, so the third historical `:361` — in the
roadmap entry narrating its own repaired F-1 defect — remains correctly outside its claim. No
substantive finding, tier, owner, decision, count or architecture changed.

### §12.1f Pre-review audit (B24) rejection of `b287c4b6…`

Two blocking findings, both of the self-referential-staleness class this section exists to prevent, and
both **created by earlier repairs in this same section**:

* **B24-F1 — a stale current aggregate inside the §12.4 method clause.** It read *"current aggregates
  (updated to seven)"* while the record's ledger, table, §12.3 and bundle all said nine. The clause was
  a **second copy** of the aggregate, hidden inside a sentence about methodology, and it wrapped across
  a line break, which is why earlier string sweeps for the aggregate did not reach it. Repaired by
  removing the number rather than incrementing it: a methodology clause now states the *rule* and no
  value, so it cannot go stale again. The same treatment is applied to §12.3's enumeration of how many
  times the fixed-point rule had been exercised.
* **B24-F2 — a fragile bare-token self-count in §12.1a.** The sentence asserted that two `:361` strings
  remained in this record. Literally false: the token also occurs in the historical table headers and in
  §12.1e's own narrative. The **narrow** proposition was true **at that candidate** — exactly two
  historical full `web/ui_text.py:361` citation references existed there, in §12.1a and §12.1d, neither
  live. The first repair restated it as a universal claim but kept a locative enumeration (*"this bullet
  and §12.1d"*), which **this very section immediately falsified** by adding a fourth reference; that
  intermediate candidate (`615fcb8e…`) was caught by the pre-freeze self-check and preserved as rejected
  evidence. The settled wording asserts only the universal property — every remaining reference is
  historical, none is live — with **no count and no location**, so no future narrative can falsify it.

**The pattern, recorded once.** Three consecutive rejections have now come from statements in §12 that
count or copy their own document's contents, not from the gate's substance. The durable correction is
the one applied here: **a governance record should state rules and lists, and should not assert counts
of its own prose.** Aggregates live in exactly one place per surface — the ledger line and the table —
and every other mention describes rather than re-counts.

### §12.2 Independent External Review rejection of `fd7de207…`

Disposition **REJECT**, on ownership architecture and release classification — explicitly **not** on
truthfulness, which the reviewer rated **HIGH** after independently reproducing the measured facts. Three
blocking findings, **each independently re-proved from source in this repair** (§4A, T1-A′, §6.B), none
accepted on the reviewer's authority:

1. Unrecorded ownership gap — semantic adaptive questioning (§4A).
2. T1-A rested on a misidentification of S2's measurable scope (T1-A′).
3. WS16 scope overstated; T2-C insufficient (§6.B).

**Where this repair goes beyond the review, on its own evidence:** WS4 §17 records the capability as
wanted and ownerless by explicit disclaimer (§4A.1); `validity_status` occurs in **no** Python file at
all, not merely outside `decision_workspace.py`; the WS16 contract carries **eleven** dimension terms at
zero occurrences; and the display owner for T2-B′ is the **same Phase 3 UX lane** T1-B already requires,
so **no new owner is needed** (§6.E). **Where it declines to defer:** the reviewer's proposed tier shape
was treated as evidence, not authority, and every changed tier was re-proved independently.

---

## §13. Scope of this gate

Governance/documentation only — this record plus one append-only roadmap entry and the two status
surfaces. No `engine/`, `web/`, `tests/`, `domains/`, `scripts/`, `benchmark/`, `prompts/`, `schemas/`
or evidence path. `EXECUTABLE DELTA: 0`; `TEST DELTA: 0`; `PIN DELTA: 0`; `PACK DELTA: 0`;
`DOMAIN-RULE DELTA: 0`. `main` not reconciled. `OWNER_DECISION_REGISTER.md` UNCHANGED. No historical or
append-only record is rewritten — including the WS16 limitation register, the TDVP reconciliation
record, and every workstream closure cited above. Every disposition here is
**`PLANNED / GOVERNED — NOT YET IMPLEMENTATION-AUTHORIZED`** unless a cited owner already carries its
own separate authorization. Recording a capability in this record authorizes no work on it.
