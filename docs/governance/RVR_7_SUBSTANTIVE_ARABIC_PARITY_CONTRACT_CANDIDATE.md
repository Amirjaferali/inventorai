# RVR-7 — SUBSTANTIVE ARABIC PARITY — CONTRACT FRAMEWORK FREEZE (CANDIDATE)

**Status of THIS record:** governance/documentation-only **CONTRACT FRAMEWORK FREEZE CANDIDATE**.
It freezes the RVR-7 framework ONLY — product scope, fences, mandatory inputs, evidence
requirements, acceptance criteria, stop conditions, and the open diagnostic questions. It does
**NOT** freeze the implementation path manifest (§H), which remains explicitly **NOT YET FROZEN**
and can only be frozen through its own separately Owner-authorized, separately reviewed and
separately Owner-accepted gate (§H.3). It implements nothing, changes no runtime, test, fixture,
pack, pin, registry, schema, or persistence file, and authorizes nothing. It becomes authoritative ONLY if/when this exact candidate is Owner-accepted at
its exact frozen SHA, merged through the established lifecycle (CREATE A MERGE COMMIT; second parent
= the exact accepted candidate; empty candidate→merge diff), and post-merge identity-verified.
**`RVR-7 IMPLEMENTATION AUTHORIZED: NO` — acceptance of this contract is NOT an implementation
start authorization.** Two further, separately Owner-authorized gates stand between this framework
and any implementation: the **RVR-7 Implementation Path Manifest Freeze** (§H.3) and then a
separate explicit **Implementation START** instruction (the W2-A / W2-B / W2-C precedent).
**Implementation START may NOT be authorized while the path manifest is unresolved.**
State this contract establishes when it becomes authoritative:
`RVR-7 CONTRACT FRAMEWORK: AUTHORITATIVE` · `RVR-7 IMPLEMENTATION PATH MANIFEST: NOT YET FROZEN` ·
`RVR-7 IMPLEMENTATION AUTHORIZED: NO` · `RVR-7 IMPLEMENTATION START AUTHORIZED: NO`.
**Governed by:** `CLAUDE.md`; `docs/governance/ACCELERATED_HIGH_ASSURANCE_EXECUTION_PROTOCOL.md`
(AHAEP, authoritative via PR #583); `docs/governance/LEAN_GOVERNANCE_AND_AGENT_CONTINUITY_PROTOCOL.md`
(binding); the committed anchors; `MVP_SCOPE_FREEZE.md`; `ACTIVE_EXECUTION_ROADMAP.md`;
`OWNER_DECISION_REGISTER.md`; `DEFERRED_OBLIGATIONS_REGISTER.md`.
**Anti-circular identity binding:** this file records its BASE and authority; the candidate's own
final SHA and tree are recorded EXTERNALLY post-freeze (gate report + machine evidence manifest +
SHA-preserving bundle), never inside this file.

---

## §A. Base and authority lineage (verified live from Git at this gate) `[REPO]`

| Fact | Verified value | Method |
|---|---|---|
| Live tip / exact base | `507a9b7533b63bb85dcae2d3fa955946b676189a` | `git fetch --prune` + `git rev-parse origin/…` |
| Commits after the tip | **0** | `git rev-list --count` |
| Working tree | clean | `git status --porcelain` empty |

**PR #585 — consolidated post-RVR-6b-closure governance synchronization (the base of this
candidate)**: first parent `814e97b5…` (PR #584 — the RVR-6b formal-closure merge); second parent
`5f3b7cb663025c7519c2f255da48d6b97400b1f9` — the exact Owner-accepted synchronization candidate;
merge tree `7f4c45af…` identical to the candidate tree; candidate→merge diff **EMPTY**; post-merge
identity verified. Chain re-verified with second-parent = exact-accepted-candidate identity:
PR #579 (W2-C contract) → #580 (sync) → #581 (W2-C implementation) → #582 (sync) → #583 (AHAEP
adoption) → #584 (RVR-6b formal closure) → #585 (consolidated sync).

Current truth consumed by this contract: `RVR-6B FORMALLY CLOSED: YES` · `W2-C IMPLEMENTED: YES` ·
`AHAEP: AUTHORITATIVE / BINDING` · `W/M: 2/2 OWNER-ACCEPTED AND FROZEN` · `RVR-7 AUTHORIZED: NO`
(before this gate) · `RVR-8 AUTHORIZED: NO`.

## §B. RVR-7 identity — re-derived, not inherited `[REPO]`

**RVR-7 = SUBSTANTIVE ARABIC PARITY.** Canonical sources, re-read at this base:

- `DEFERRED_OBLIGATIONS_REGISTER.md` §3 row, verbatim item: **"RVR-7 — substantive Arabic parity"**;
  owner "Path-N artifacts + ui_text + deliverable owners; D-P6-18 supersession decision at that
  gate"; origin "register OD-R4 (Wave 3); Wave-2 contract §O"; disposition `OPEN — NOT AUTHORIZED
  YET`; return trigger "Wave-3 authorization after W2 content stabilizes"; latest safe gate "before
  serious release IF Arabic is represented as a substantive supported experience"; blocking
  "FRB (conditional on Arabic positioning)"; closure evidence "RVR-7 merged; EN/AR
  semantic-equivalence review + W1-N1/N2 inputs discharged".
- `OWNER_DECISION_REGISTER.md` **OD-R4**: "**RVR-7 — substantive Arabic parity program** (after
  content stabilizes; W1-N2/W1-N3 are mandatory inputs) | ACCEPTED IN PRINCIPLE — IMPLEMENTATION
  NOT AUTHORIZED (Wave 3, separate Owner authorization)".
- `WAVE_2_BOUNDED_IMPLEMENTATION_CONTRACT_CANDIDATE.md` **§O — Wave-3 boundary — RVR-7**, which
  carries the Wave-3 CONTRACT INPUT forward verbatim (same-`question_id` AR variants via the content
  gate; no runtime translation; EN/AR canonical-state invariance; W1-N1/W1-N2 as mandatory
  verification inputs; semantic-equivalence review; the OD-W2-D-P6-18 display-rule supersession
  decision) and records `RVR-7 WAVE PLACEMENT: WAVE 3 — UNCHANGED`.
- `WAVE_2_BOUNDED_IMPLEMENTATION_CONTRACT_CANDIDATE.md` **§C ("Current implementation truth —
  corrections to the prior candidate"), item 1 "Deliverable language (corrected)"** — the locus of
  the quotation "The RVR-7 gap is **substantive Arabic parity, not shell RTL activation** — the
  shell is already RTL-capable", together with "Canonical state: language-independent". Citation
  locus re-derived mechanically at this base `[EXEC — the quoted line falls under the §C heading,
  not §O and not §B]`; the predecessor candidate mis-attributed this quotation to §O. The product
  conclusion it supports is unchanged.

**RVR-7 is NOT** relevance/precision repair, NOT an RVR-2 continuation, NOT adaptive questioning,
NOT runtime translation, and NOT RVR-8. Its trigger precondition is satisfied: all four Wave-2
executable slices (W2-D, W2-A, W2-B, W2-C) are merged and authoritative, so "W2 content stabilizes"
holds `[REPO]`.

## §C. Owner product positioning — newly decided `[OWNER-PREMISE → recorded here]`

**`ARABIC SUBSTANTIVE POSITIONING: OWNER DECIDED YES`** — Arabic in InventorAI is a **Substantive
Supported Experience**, not merely UI localization. This decision was issued by the Owner at this
gate; it is recorded contemporaneously by this contract candidate and registered in the Owner
Decision Register in this same candidate.

**Exact repository consequence, stated precisely and not overstated.** The register's RVR-7 row
makes its blocking level conditional in two coupled fields: blocking = "FRB (conditional on Arabic
positioning)" and latest safe gate = "before serious release **IF** Arabic is represented as a
substantive supported experience". The Owner has now satisfied that condition. Therefore:

**`RVR-7 SERIOUS-RELEASE BLOCKING STATUS: ACTIVE`** — precisely: RVR-7's conditional
`FUTURE SERIOUS-RELEASE BLOCKER` is now an **unconditional FRB**, and its latest safe gate resolves
from a conditional to a firm **"before serious release"**. Per the register's own permanent
release-closure rule, no serious release may be approved until this obligation is CLOSED,
SUPERSEDED, or RETIRED with evidence.

**What this consequence does NOT do** (bounded exactly): it does not authorize RVR-7
implementation; it does not start any lifecycle; it does not change any other row's blocking level;
it does not make RVR-7 a CURRENT EXECUTION BLOCKER (it is a future-release blocker); and it does not
alter the sequencing rule that RVR-8 remains separately governed and separately authorized.

Two dependent rows follow the RVR-7 row's conditionality by their own wording and therefore also
resolve from conditional to firm, **without changing owner or trigger**: the deliverable
withdrawn-note localization row (`NBF`, latest safe gate "before serious release IF Arabic is
represented as substantive — follows the RVR-7 row's conditionality") and the prose ↔ markers
anchor's Arabic clause (§K.2). Both are recorded in this candidate's register edits; neither is
closed here.

## §D. Objective (narrowest consistent with authoritative truth)

Deliver **substantive Arabic parity for the Path-N journey** by serving **same-`question_id`
Arabic variants through the existing committed content gate**, with canonical state remaining
**language-independent** and **EN/AR semantic equivalence proven** — changing no relevance
semantics, no progression logic, no frozen parameter, and no adaptive behavior.

**Mandatory vocabulary distinctions (frozen; the implementation may never blur them):**

- **Arabic parity (IN SCOPE)** — the substantive journey content an inventor reads and answers
  (Path-N question variants and the substantive prompts in the same journey surface) exists as
  committed Arabic content of equivalent meaning.
- **Arabic localization (ALREADY DELIVERED; NOT this gate's objective)** — UI chrome translation
  and RTL shell, delivered and formally closed by D-P6-18 (PR #388). RVR-7 neither redoes nor
  reopens it.
- **Runtime translation (FORBIDDEN)** — see §M.
- **Language-specific routing (FORBIDDEN)** — see §J.
- **Adaptive-questioning behavior (FORBIDDEN)** — see §J.

**Non-negotiable framing rule:** Arabic parity must NEVER become a mechanism that changes *which*
question the user receives. Only the *rendered language variant* of the canonically selected
question may differ.

## §E. Mandatory inputs (bound at this freeze)

**E.0 — Definition of the "RVR-7 CONTRACT FREEZE" event (governance semantics repaired).** The
register's W1-N2 return trigger reads "RVR-7 contract freeze", but the repository did not define
whether that means Creator candidate creation or authoritative contract adoption. For this lifecycle
the term is now defined, and the definition is deliberately the conservative one:

> **RVR-7 CONTRACT FREEZE EVENT** = the point at which the exact Owner-accepted RVR-7 contract
> candidate has been **merged to the authoritative branch through the authorized merge lifecycle and
> has passed post-merge identity verification**.

Creating or freezing a Creator candidate is therefore **NOT** the contract-freeze event. It follows
non-circularly that this candidate, in its present pre-acceptance state, must not claim the trigger
has fired.

**E.1 — W1-N2 (Arabic adversarial regression test, enumerated small-talk).** Register row
re-verified at this base: owner **"RVR-7 (Wave 3)"**; return trigger **"RVR-7 contract freeze"**;
latest safe gate "RVR-7"; blocking `FRB (verification input)`; closure evidence "merged RVR-7 suite
incl. the W1-N2 AR test".
**`W1-N2 TRIGGER AT CANDIDATE STATE: NOT YET AUTHORITATIVELY FIRED`** (per §E.0).
**IF AND WHEN THIS EXACT CONTRACT CANDIDATE BECOMES AUTHORITATIVE, THE REGISTERED "RVR-7 CONTRACT
FREEZE" TRIGGER FIRES AND W1-N2 BECOMES A BOUND IN-CONTRACT IMPLEMENTATION/REVIEW OBLIGATION.**
Until then W1-N2 remains **`OPEN`** and **`NOT DISCHARGED`** — no Arabic adversarial regression test
exists, none is written here, and nothing about it is closed.
Discharge mechanism, fixed now: the future authorized RVR-7 implementation candidate MUST contain a
merged Arabic adversarial regression test over the enumerated small-talk corpus, exercised through
the real answer-integration path (not a unit stub), with EN↔AR differential assertions; the
Independent Review must independently reproduce it; the row closes only on that merged evidence.
The register row is updated in this candidate to record this **conditional future firing** and the
prospective in-contract obligation — it records **no fired trigger**, and it is **NOT closed**.

**E.1.1 — Post-merge synchronization duties created by the §E.0 definition (named now, performed
later).** Because the freeze event is authoritative adoption, the state transition happens at merge,
not here. The first authorized governance synchronization after this contract framework is
Owner-accepted, merged and post-merge identity-verified MUST therefore:

1. **Deferred Obligations Register — W1-N2 row:** transition it from `TRIGGER FIRED: NO` to
   **`TRIGGER FIRED / BOUND: YES`**, while it **remains `OPEN` and `NOT DISCHARGED`** (the bound
   obligation is the future merged Arabic adversarial regression; the row closes only on that merged
   evidence). This is a status synchronization of an already-defined trigger — never a closure, and
   never a claim that the test exists.
2. **Owner Decision Register — deferred registrations** (unchanged duty, restated for continuity):
   the RVR-7 contract-freeze **START authorization**, and the **exact contract acceptance** (accepted
   SHA + merge identity), both registered at that first appropriate post-acceptance / post-merge
   synchronization, paired with authoritative evidence.

**This contract does NOT perform that synchronization and does NOT claim it has occurred.** At this
candidate state the transition has not happened and must not be recorded as though it had.

**E.2 — W1-N1.** No standalone OPEN register row exists for W1-N1 at this base `[REPO]`; it appears
only inside the RVR-7 row's closure-evidence field ("W1-N1/N2 inputs discharged") and in Wave-2 §O
("W1-N1/W1-N2 as mandatory verification inputs"). Required verification role, fixed here: W1-N1 is a
**verification input to the RVR-7 acceptance evidence**, discharged by demonstrating its Arabic
verification concern in the RVR-7 suite and recording the discharge in the implementation evidence
pack. Because W1-N1 has no independent row, the RVR-7 row's closure-evidence field is its sole
tracking surface; this contract does not create a new row for it (no duplicate owner).

**E.3 — W1-N3.** Status preserved exactly as authoritative: **`CLOSED — evidence verified (bounded
authoritative scope)`**. This contract does **NOT** reopen it, does not re-litigate it, and makes no
claim over the residual it explicitly excluded. See §F.

## §F. Precision boundary — `gap_relevance` / RVR-2 (mandatory, explicit)

**The `gap_relevance` / RVR-2 precision residual is NOT an RVR-7 implementation objective.**
Authoritative wording preserved (W1-N3 row): the W1-N3 closure is "EXACTLY the recorded W1-N3 scope
— NOT 'all relevance false-negatives closed', NOT RVR-2 completion, NOT RVR-7 obsolescence"; the
remaining residual "remain[s] the pre-existing declared residual owned by `gap_relevance`/RVR-2 with
**RVR-7 as the mandatory downstream return/input (OD-R4)**". RVR-2 itself is an already-implemented
Wave-1 gate (`RVR-1 / RVR-2 / RVR-3 / RVR-5: IMPLEMENTED, AUTHORITATIVE`) `[REPO]`; "`gap_relevance`
/RVR-2" names the owning code surface and its delivering gate, not a pending upstream gate — so **no
upstream RVR-2 decision is required before RVR-7**.

RVR-7 **MAY**: consume prior relevance evidence as baseline; and **MUST** trigger EN/AR differential
re-verification if a shared marker/vocabulary surface is touched (§K.2).

RVR-7 **MAY NOT**: repair `gap_relevance`; broaden or narrow relevance semantics; rebalance false
positives against false negatives; reinterpret the W1-N3 closure; or silently absorb the broader
precision residual.

**STOP CONDITION (binding):** if implementation discovery proves a `gap_relevance` change is
necessary to deliver Arabic parity, the executor STOPS and returns
`RVR-7 CONTRACT CANNOT BE FROZEN WITHIN AUTHORIZED SCOPE — SEPARATE OWNER DECISION REQUIRED`.

## §G. Implementation-design discovery (read-only, performed at this gate) `[EXEC/REPO]`

**Current mechanism, mechanically established:**

1. Path-N question content lives in committed per-domain artifacts resolved through an EXPLICIT
   BOUNDED domain→artifact mapping (`engine/path_n_questions.py`; raw domain strings never reach the
   filesystem). Record schema is `{question_id, text}` under a `design_gap_id` parent key, read
   **atomically** so "identity, text, and design-gap always describe one physical record"; the
   loader fails loudly with no fallback on missing/unusable fields; per-domain load-once cache.
2. Committed content carries **0 Arabic characters** in both artifacts; the variant structure is
   electronics 4/4/3 and mechanical 4/2/4 = **21 question ids total**, matching the WS10 registry id
   count exactly.
3. Display localization is a **separate display-time mechanism**: `web/ui_text.py`
   (`SUPPORTED_LANGS = ("en","ar")`, `_MESSAGE_KEYS`, `_DEEP_AR`, `localize_message`,
   `localize_deep`), documented in `web/app.py` as "Storage stays English; display localises through
   `ui_text.localize_message`", with `localize_deep` passing unknown strings through unchanged —
   which is exactly why question text renders English in Arabic sessions today.
4. **Canonical state does not persist question text.** `next_question` is DERIVED at reconstruction
   from the replayed progression result (`(last_result or {}).get("question")`); no persistence
   writer stores it `[EXEC grep: no save/store/write/persist path for `next_question`]`.

**Options evaluated against the required criteria** (none chosen for convenience):

| Criterion | (A) Extend `_DEEP_AR` display catalog with question texts | (B) Bilingual variant field inside the committed content artifacts, served by the same loader | (C) Parallel AR content artifacts (separate files) |
|---|---|---|---|
| Same-`question_id` identity | Weak — catalog is keyed by English STRING, not id | **Strong — id is the record key; text becomes a language-keyed value on the same record** | Medium — ids duplicated across two files, drift-prone |
| Canonical-state invariance | Preserved (display-only) | **Preserved — canonical selection stays id/index-based; text is render-time value** | Preserved |
| Deterministic loading | Display-time lookup, pass-through on miss (silent English fallback) | **Same load-once deterministic gate; fail-loud on malformed record** | Two load paths to keep consistent |
| Validation | None for question coverage | **Loader already validates atomically; coverage validatable per record** | Cross-file coverage check needed |
| Semantic-equivalence reviewability | Poor — EN and AR live far apart | **Best — EN and AR side by side in one record** | Medium |
| Rollback safety | Catalog revert | **Content-only revert** | File deletion; mapping edit |
| Migration risk | Brittle: any English wording edit silently breaks the AR lookup | **Low — additive field; absent field = current behavior** | Medium |
| Persistence / reconstruction impact | None | **None (see finding 4)** | None |
| Duplicate-content-owner risk | **HIGH — creates a second source of question truth** | **None — extends the canonical content owner** | HIGH — two question artifacts per domain |
| Vendor / MT lock-in | None | **None** | None |

**Recommended content architecture: OPTION B — an additive bilingual variant field on the existing
committed question records, served by the existing content gate.** It is the only option that keeps
`question_id` as the record key, preserves the single canonical content owner, inherits the existing
fail-loud validation, and makes semantic equivalence reviewable in place. Option A is rejected
principally for the duplicate-content-owner and string-key fragility; Option C for duplicate
ownership and drift.

**Persistence / schema / architecture escalation test: NO ESCALATION REQUIRED.** The change is an
additive field in a committed content artifact plus loader support for selecting the language
variant of an already-selected record. It reaches no persistence writer, no reconstruction schema
(question text is derived, never stored), no security surface, no product-identity anchor, and no
architecture boundary. **If implementation discovery contradicts this** — i.e. if any design that
delivers parity would touch persistence, the reconstruction contract, or a Level-1 surface — the
executor STOPS and escalates rather than absorbing it (§N).

### §G.2 — COMPLETE LANGUAGE-ROUTING SENTINEL MODEL (binding)

Language parity is safe only if **every** question-text equality / serving comparison in the live
path behaves identically in EN and AR. The rejected predecessor of this contract named only the
exhaustion clamp; Independent Review proved that incomplete, and the following four sentinel sites
were then independently re-derived at this base `[EXEC]`. **All four are binding; the list is a
floor, not a ceiling — the future discovery step must re-run this enumeration and add any sentinel
it finds.**

| ID | Site | Mechanism | Language-routing failure mode if unguarded |
|---|---|---|---|
| **S1** | `engine/progression_loop.py`, the Path-N display/exhaustion clamp in `get_display_question`'s serving path | adjacent-index question-text equality (`current == get_path_n_question(gap_type, iterations_open - 1, …)`, and a second comparison at `- 2`) drives the RVR-2 stall reframe and then the exhausted exit | a non-isomorphic AR variant set fires the clamp at a **different iteration in Arabic** → different progression by language |
| **S2** | `engine/progression_loop.py` `_generic_clamped_repeat` | question-text equality `current == previous` on the GENERIC-variant surface, feeding `TRIGGER_COMPLETED_INTENT_SKIP` and `TRIGGER_CRITICAL_UNRESOLVED` | **currently inert for Path-N** (it returns False whenever a Path-N question exists, yielding to RVR-2's governed surface) — but it becomes live the moment the generic surface becomes language-aware, and would then fire W2-B triggers differently by language |
| **S3** | `engine/progression_loop.py` LAPSED_ACCEPTANCE | `baseline = get_display_question(...)` compared against `primary = get_question(domain, served_gap, 0, …)`; the trigger fires only when `primary != baseline` | the two sides come from **different accessors**; if one becomes language-aware and the other does not, `primary != baseline` becomes true in Arabic where it is false in English → the W2-B adaptive-register trigger **fires only in Arabic** |
| **S4** | `web/app.py`, the W2-C final serving gate: `_canonical_q = get_question(...)`; `if question == _canonical_q:` then `question = w2c_served_question(state, gap_type).text` | equality gate deciding whether W2-C intent-aware serving applies at all | **two opposite failure modes, both fatal** — see §G.2.1 |

**§G.2.1 — The S4 double bind (explicitly fenced).** Both of these are prohibited outcomes and the
implementation must prove it avoids **both**:

- **Bypass mode:** the rendered `question` becomes Arabic while `_canonical_q` stays English, so
  `question != _canonical_q` and the W2-C intent-aware serving law is **silently skipped for Arabic
  users**. That is simultaneously a product regression (Arabic loses W2-C) and a
  language-conditional behavior difference.
- **Overwrite mode:** both sides are made language-aware so equality is preserved, but
  `w2c_served_question(...).text` still returns the **English** committed variant, which then
  **overwrites the Arabic question**. Arabic parity is silently destroyed at the last step.

Avoiding one of these by causing the other is NOT acceptance; the evidence must demonstrate a
design in which neither occurs.

**§G.2.2 — Bound evidence for the sentinel model.** The future implementation candidate MUST prove,
with EN/AR paired evidence over real served routes (not unit stubs alone):

1. **EN/AR trigger-firing invariance** — every W2-B trigger (incl. LAPSED_ACCEPTANCE,
   COMPLETED_INTENT_SKIP, CRITICAL_UNRESOLVED) fires identically for identical state in both
   languages;
2. **W2-C serving-gate invariance** — the S4 gate reaches the same decision in both languages, with
   neither bypass nor overwrite;
3. **canonical `question_id` invariance** — identical id served for identical state in both
   languages;
4. **progression-index invariance** — identical `iterations_open` / variant index progression;
5. **no language-specific W2-B or W2-C behavior** of any kind;
6. **no Arabic question overwritten by English serving content** at any layer;
7. **no bypass of the existing W2-C serving law** for Arabic sessions.

**§G.2.3 — Index-isomorphism requirement (retained, and explicitly insufficient alone).** The AR
variant set MUST remain index-isomorphic to EN: identical variant count per `design_gap_id`,
identical `question_id` ordering, and a distinctness structure such that any clamp fires at exactly
the same index in both languages. **`INDEX-ISOMORPHISM ALONE IS NOT SUFFICIENT`** — it guards S1 and
part of S2 only, and provides no protection whatsoever against S3's cross-accessor asymmetry or S4's
double bind. Both the isomorphism requirement and the full §G.2 sentinel evidence are mandatory.

### §G.3 — Substantive non-question serving surfaces and their pin cost

`_STALL_REFRAME` and `_EXHAUSTED_EXIT_PROMPT` are English constants in
`engine/progression_loop.py` and are **absent from the `ui_text` Arabic catalog** `[EXEC grep: 0
matches]`, so an Arabic session reaching variant exhaustion currently receives English substantive
prompts. They are part of the substantive journey and therefore within the parity concept, but their
inclusion is **Q2**, which depends on the OD-W2-D-P6-18 decision (§H.1, §S).

**Exact pin cost if Q2 brings `engine/progression_loop.py` into the frozen manifest** — evidence must
name all four modules, not three `[EXEC]`:

- `tests/test_p9_mech_i3_signal_quality.py` — digest pin;
- `tests/test_p9_mech_i4_boundary_corpus.py` — digest pin;
- `tests/test_p9_mech_i5_question_sufficiency.py` — digest pin;
- `tests/test_w2b_amc_consumers.py::test_exactly_three_p9_files_pin_the_current_digest` — an
  **independent consistency verifier**, not a fourth stored pin. Verified from source at this base
  `[EXEC]`: it stores **no digest of its own** (zero 64-hex literals in the module); it recomputes
  the **live** SHA-256 of `engine/progression_loop.py` at run time, extracts the stored digest from
  each of the three pin files, and asserts that the set of those three stored digests equals exactly
  the live digest. **Consequence, stated correctly:** a re-freeze edits **three** files (the stored
  pins); this fourth module needs **no edit** and never "enforces an old digest". What it does
  enforce is consistency — it fails if the three pins are updated partially or inconsistently, if a
  pin is missing from any of the three files, or if the pinned set stops matching the live module.
  It must therefore be run and stay green as part of any re-freeze evidence.

Any such re-freeze follows the governed W2-B / W2-C precedent: mechanical recomputation, disclosed
lineage comment recording the pre-change digest, and no semantic change smuggled into the pinned
module.

### §G.4 — Serving-surface inventory (runtime, non-durable)

`web/app.py` holds the served question text in the in-memory session store
(`SESSION_STORE[sid] = {"state": …, "last_result": …, "transcript": []}`). The enumerated runtime
serving surfaces are: **`entry["last_question"]`**, **`last_result`** (which carries the served
question), and the **transcript question text** (which accumulates served questions across the
session). On current evidence this is **NOT
durable persistence** — it is process-local in-memory state, and the durable reconstruction path
derives `next_question` by replay rather than reading it (§G finding 4). It is nonetheless a
**runtime serving surface that MUST participate in parity testing**: language correctness there is
what the user actually sees across a session, and an EN/AR divergence in `entry["last_question"]`,
`last_result` or the transcript is a real parity defect even though nothing is persisted. Recording
these surfaces does **NOT** convert them into persistence and asserts no durability.

## §H. Implementation path manifest — **NOT YET FROZEN** (and not freezeable at this gate)

**H.1 — Status.** `RVR-7 IMPLEMENTATION PATH MANIFEST: NOT YET FROZEN`. This contract freezes the
FRAMEWORK only. An exact allowlist cannot be frozen truthfully here, and this contract will not
guess one. Two genuine technical questions remain, both discovered by read-only inspection at this
gate and neither resolvable without diagnostic work that exceeds this authorization:

- **Q1 — variant-field shape and loader seam.** Whether the bilingual field is `text` becoming a
  `{en, ar}` map or an additive sibling (e.g. `text_ar`); exactly which loader/serving functions
  must become language-aware (`get_served_question`, `get_path_n_question`, `get_display_question`,
  `get_question`); and how the language reaches them **without leaking language into any progression
  decision** — which is constrained by the complete sentinel model in §G.2, not by index-isomorphism
  alone.
- **Q2 — exhaustion / reframe and substantive-prompt parity scope.** Whether `_STALL_REFRAME`,
  `_EXHAUSTED_EXIT_PROMPT` and the other substantive non-question prompts are inside RVR-7
  (requiring an `engine/progression_loop.py` touch and a governed digest re-freeze — see §G.3) or
  are deferred to a separate authorized touch as a registered obligation. **Q2 CANNOT BE ANSWERED
  BEFORE THE OD-W2-D-P6-18 OWNER DECISION** (§S): that decision determines whether substantive
  exhaustion/reframe surfaces are promised in Arabic at all, and therefore whether they belong in
  the manifest.

**H.2 — Bounded pre-implementation discovery sub-step (defined here; NOT authorized here).**
Scope = read-only inspection plus non-mutating diagnostic probes. Permitted output = a proposed
exact path manifest plus evidence-backed answers to Q1 and Q2. **No implementation authorization,
no content added, no runtime or test file modified, no repository state changed.** Stop condition =
any finding that parity requires a persistence, reconstruction-schema, `gap_relevance`, or Level-1
surface change; or that Q1/Q2 cannot be answered without editing pinned or runtime files; or that
OD-W2-D-P6-18 is still undecided when Q2 must be answered. **This sub-step requires its own separate
Owner authorization.**

**H.3 — MANDATORY RVR-7 IMPLEMENTATION PATH MANIFEST FREEZE GATE (separate, non-optional).**
The path manifest becomes frozen ONLY through a dedicated gate with all of the following, in order.
This gate is **NOT** created, executed, or pre-authorized by this contract:

```
RVR-7 CONTRACT FRAMEWORK AUTHORITY  (this artifact, once Owner-accepted + merged + post-merge verified)
  -> OD-W2-D-P6-18 Owner decision                    [PREREQUISITE — §S; must be decided first]
  -> separate Owner authorization of the bounded diagnostic / path-manifest discovery sub-step (§H.2)
  -> RVR-7 IMPLEMENTATION PATH MANIFEST FREEZE candidate
  -> Independent Review of that candidate
  -> Owner exact-SHA acceptance of that candidate
  -> merge + post-merge identity verification
  -> AUTHORITATIVE PATH MANIFEST FREEZE
  -> only then: separate explicit RVR-7 IMPLEMENTATION START authorization
```

**Binding sequencing rules (each independently sufficient to stop a gate):**

1. The Path Manifest Freeze is a **distinct gate** from Implementation START. They are never the
   same decision, never the same candidate, and never combined.
2. The Path Manifest Freeze gate requires **its own separate Owner authorization**; framework
   acceptance never implies it.
3. Its candidate must be **independently reviewed AND Owner-accepted at its exact SHA, merged and
   post-merge verified** before implementation can start.
4. **`RVR-7 IMPLEMENTATION START` MAY NOT BE AUTHORIZED WHILE THE PATH MANIFEST IS UNRESOLVED.**
5. **OD-W2-D-P6-18 must be decided BEFORE the Path Manifest Freeze** (§S, §H.1 Q2).
6. **Lean LEVEL and Review DEPTH for the implementation MUST BE RE-DERIVED after the actual path
   manifest exists** — the §V classification is explicitly provisional and may never be carried
   into implementation unexamined.
7. The path manifest may **NOT** be frozen "as a bounded amendment to this contract" and may **NOT**
   be frozen "at the implementation-start gate". Both routes are prohibited by this section; any
   candidate attempting either is invalid on its face.

**H.4 — Provisional path envelope (indicative only — NOT an allowlist, NOT authorization, and
explicitly NOT the frozen manifest).** Recorded solely so the future discovery step starts from
evidence rather than memory: `docs/governance/path_n_content_config/*_path_n_questions.json`;
`engine/path_n_questions.py`; possibly `web/app.py` and `web/ui_text.py`; new `tests/test_rvr7_*.py`;
conditionally `engine/progression_loop.py` plus the digest-pin consumers of §G.3 (Q2 only). Once the
manifest is frozen at its own gate, every path outside it is forbidden.

## §I. Allowed scope (exact, once the §H manifest is frozen)

1. Adding committed Arabic question-variant content of equivalent meaning for the existing 21
   `question_id`s, index-isomorphic to English (§G).
2. The minimum loader/serving change required to select the language variant of an
   already-canonically-selected record, with English as the deterministic fallback when an AR
   variant is absent — never a silent substantive-English fallback where Arabic is promised
   (§L.2 governs how that is proven, not hidden).
3. Language propagation from the existing UI-language mechanism to the render seam only.
4. New RVR-7 tests, including the W1-N2 Arabic adversarial regression (§E.1).
5. The RVR-7 implementation evidence pack and its governance records.
6. Conditionally, per §H Q2 and only if the frozen manifest includes it: Arabic parity for the
   exhaustion/reframe prompts, with governed digest re-freeze and disclosed lineage.

## §J. Forbidden scope and hard fences (binding)

**Adaptive / routing fences — explicitly prohibited:** Full Adaptive Questioning; Meaning-Adaptive /
Tier-2; WS11 activation; **language-conditional question selection**; different question progression
merely because the UI/output language is Arabic; creation of a second adaptive engine.
**Invariance rule:** the same idea/user state under the same progression conditions MUST preserve
canonical question identity (`question_id`, `design_gap_id`, index) independent of language; only
the rendered language variant may differ. Current fence state re-verified at this base:
`FULL ADAPTIVE QUESTIONING ACTIVATED: NO`; `MEANING-ADAPTIVE / TIER-2 ACTIVATED: NO`;
`WS11 dormant`.

**Also forbidden:** modifying `gap_relevance` (§F); modifying or tuning `W`/`M` (§O); MG-8 semantic
repair (§P); exercising OD-PDVG-12 (§Q); runtime or machine translation (§M); reopening W1-N3 or
RVR-6b; closing either RVR-6b Option-A anchor (§K); authorizing or preparing RVR-8 (§R); deployment;
production; Serious Release; Paid Activation; billing changes; new domain activation; unrelated UI
changes; new workstream creation; architecture redesign; and any path outside the frozen manifest.

## §K. RVR-6b Option-A anchors — conditional, non-transferable

**K.1 — Registry CWD / path-binding limitation.** Row re-read at this base: `OPEN — return at
defined gate`; owner "WS10 loader-contract owner + `engine/intent_serving.py` accessor (code
surfaces); disposition decision reserved to the Owner / a future loader-contract gate"; trigger "the
next authorized touch of the WS10 loader contract or the `intent_serving` accessor; **AND**
mandatorily the PSRR/deployment gate"; latest safe gate before deployment/production; CONDITIONAL.
**RVR-7 alone does NOT fire it** — the mandatory conjunct is the PSRR/deployment gate, which RVR-7
is not, and PSRR is NOT pulled into RVR-7. It remains **OUTSIDE RVR-7 / downstream**. Should the
frozen §H manifest include a WS10-loader-contract or `intent_serving`-accessor touch, the first
conjunct becomes relevant and the implementation records that fact in its evidence pack — the row is
**NOT closed**, its ownership is **NOT transferred**, and its PSRR conjunct still governs.

**K.2 — Registry intent prose ↔ `_INTENT_MARKERS` binding/divergence surface.** Row re-read at this
base: `OPEN — return at defined gate`; owner "the W2-C content/marker surfaces
(`engine/intent_serving.py` `_INTENT_MARKERS` + the two committed per-domain registries)"; trigger
"the next authorized touch of EITHER artifact (any WS10 content or marker edit must re-verify id-set
equality and EN/AR pairing); **AND** RVR-7 (its substantive Arabic-parity program works exactly this
vocabulary surface)"; latest safe gate "before serious release (with RVR-7 if Arabic is represented
as substantive)"; CONDITIONAL. Mechanically confirmed divergence at this base: `_INTENT_MARKERS`
carries **578 Arabic characters** while both committed registries carry **0** `[EXEC]`.
**A trigger reference is not ownership.** The anchor stays owned by the W2-C content/marker
surfaces; RVR-7 is a return gate. **Conditional IN-CONTRACT OBLIGATION:** if the frozen manifest
touches the committed per-domain registry content or `_INTENT_MARKERS`, the implementation MUST
produce, as acceptance evidence: (i) id-set equality across registries and markers; (ii) complete
EN/AR marker pairing; (iii) registry ↔ marker alignment; (iv) proof of no EN-only or AR-only
semantic leak; (v) differential EN/AR relevance behavior over the affected surface. The row is
**NOT closed at this contract freeze** and **NOT transferred**. Its Arabic clause is no longer
conditional on positioning (§C), which this candidate records in the row without altering owner,
trigger, or disposition.

## §L. Acceptance criteria — substantive, not string-count parity

**L.1 — Mechanical parity.** Every one of the 21 existing `question_id`s has an Arabic variant; zero
missing AR variants; deterministic content loading through the existing gate with fail-loud
behavior preserved; EN/AR pairing complete and mechanically enumerated (counts derived, never
hand-tallied); AR variant set **index-isomorphic** to EN per §G.

**L.2 — Semantic parity.** Each Arabic question asks the **same decision-relevant question** as its
English twin: no meaning narrowing or broadening; no tone or complexity shift material enough to
change answer behavior; no untranslated substantive-journey fallback anywhere Arabic is promised —
where an English fallback can still occur, it must be enumerated and justified, never silent.

**L.2.1 — Semantic-equivalence review competence (binding).** The semantic-equivalence review is a
**human** review and must be performed by a reviewer with **demonstrated bilingual EN/AR competence
appropriate to the product's technical register** — inventor-facing engineering language, not
general conversational Arabic. The review MUST record: the reviewer's competence basis; the explicit
review standard applied (what counts as equivalent, and what counts as a material narrowing,
broadening, or register shift); the per-item comparison outcome; and every **disagreement or
ambiguity encountered, left visible rather than resolved silently**. Machine translation **may
assist drafting** but **may NEVER be the semantic-equivalence authority**, and a machine-translation
round-trip is not evidence of equivalence. An otherwise complete candidate whose semantic review
lacks demonstrated bilingual competence does not satisfy §L.2.

**L.3 — Behavioral invariance.** Same canonical records; same `design_gap_id` / `question_id`
identity; same progression logic and clamp/exhaustion timing (§G hazard); same completion and
decision semantics; **no language-driven routing**; reconstruction/replay parity preserved.

**L.4 — Adversarial Arabic quality.** W1-N2 enumerated small-talk regression (§E.1); representative
Arabic inventor responses; weak-answer and boundary cases; EN↔AR differential checks over relevance
and progression outcomes — the historical W2-C R3 failure (an English marker matching where its
Arabic twin missed) is the precedent this must defend against.

## §M. Runtime / machine translation — frozen prohibitions

`RUNTIME TRANSLATION: FORBIDDEN` · `MACHINE-TRANSLATION DEPENDENCY: NOT PART OF RVR-7`.
Arabic variants MUST be canonical committed content, never generated at request time. No external
translator dependency, no language-vendor lock-in, no AI call in the content gate (the loader's
existing "No AI calls" prohibition is preserved unchanged).

## §N. Stop conditions (explicit)

Stop and escalate — do not absorb — on any of: base advancement; a proven need to change
`gap_relevance` (§F); any design that reaches persistence, the reconstruction schema, security,
product identity, or another Level-1 trigger; any language-conditional routing appearing in the
design; inability to keep the AR variant set index-isomorphic to EN; any path outside the frozen
manifest; any pressure to close an Option-A anchor, reopen W1-N3/RVR-6b, decide D-P6-18 without the
Owner, or treat contract acceptance as an implementation start.

## §O. W / M — reference and consume only

Verified authoritative at this base: **`W = 2`, `M = 2`, OWNER-ACCEPTED AND FROZEN** (fixed at the
exact-SHA acceptance of `6cf09582…`, PR #576, per the Wave-2 §P mechanism as amended).
**Contract rule: REFERENCE / CONSUME ONLY — NO MODIFICATION.** Any proposed tuning, any
localization-specific override, and any Arabic-specific W or M value are **forbidden**; a change
would be a new Owner decision under the §P mechanism, never an implementation choice.

## §P. MG-8 — excluded

Verified at this base: **`MG-8 OPEN`**, W2-B diagnosis delivered, semantics UNCHANGED, governance
owner "NONE ESTABLISHED (locus ≠ owner)", trigger "explicit Owner adjudication on the delivered
diagnosis", latest safe gate before serious release (adjudication, not necessarily change),
CONDITIONAL. **`MG-8 SEMANTIC REPAIR: NOT AUTHORIZED`** and explicitly excluded from RVR-7. If an
Arabic-parity implementation exposes MG-8 behavior during testing, the executor **records the
evidence and does not repair it** under RVR-7.

## §Q. OD-PDVG-12 — remains unexercised

Verified at this base: `OPEN`; owner "Phase-3 UX display lane (content: WS10)"; trigger
"OD-PDVG-12 decision (optionally at W2-C freeze for inclusion)"; that optional W2-C window passed
unused. **`OD-PDVG-12 EXERCISED: NO`.** The contract explicitly forbids adding "Why this matters" /
question-explainability rendering merely because question content is being localized — the surfaces
are adjacent (both WS10 question content), which is precisely why the prohibition is explicit. If
the Owner wants it later, it requires its own decision.

## §R. RVR-8 — hard fence

`RVR-8 AUTHORIZED: NO`. This contract does not authorize RVR-8, does not prepare RVR-8
implementation, does not absorb RVR-8 acceptance criteria, and claims no RVR-8 readiness beyond the
factual dependency status already recorded (the RVR-8 row's trigger remains "Owner authorization
after RVR-7"). RVR-8 remains separately governed.

## §S. D-P6-18 display-rule supersession — **OWNER DECISION REQUIRED** (not decided here)

**Decision question, reconstructed.** D-P6-18 ("Global UI language selector") is
`IMPLEMENTED / INDEPENDENTLY REVIEWED (B) / MERGED (PR #388) / FORMALLY CLOSED` and established the
current display rule: the shell renders `<html lang="ar" dir="rtl">` in Arabic sessions and
`<html lang="en">` in English sessions, while **substantive technical content remains largely
English in both**, with "governed `t()` strings [as] the translated subset" and canonical state
language-independent `[REPO — Wave-2 contract §C, item 1 "Deliverable language (corrected)"]`. Wave-2 §O routes "the OD-W2-D-P6-18
display-rule supersession decision" to this Wave-3 gate.

**What must be decided:** whether, and how far, that display rule is superseded once substantive
Arabic content exists — i.e. what an Arabic session is promised and what may still legitimately
render in English.

**Candidate outcomes (presented, not chosen):** (a) **Full substantive supersession** — in Arabic
sessions the entire substantive journey renders Arabic, any English substantive fallback is a
defect; (b) **Bounded supersession (scoped)** — the Path-N question journey is superseded to Arabic
while enumerated non-journey surfaces (e.g. deliverable technical artifacts) remain English by
explicit, disclosed rule; (c) **No supersession** — Arabic variants are served but the D-P6-18 rule
stands unchanged as the governing display policy.

**Product impact.** (a) is strongest for the Owner's "Substantive Supported Experience" positioning
but has the widest surface and interacts with the still-open deliverable-localization defect row;
(b) matches the Owner's positioning for the journey while keeping the remaining English surfaces
honest and registered, at the cost of requiring an explicit and disclosed boundary; (c) is
inconsistent in spirit with §C and risks promising Arabic while substantive English persists
undisclosed.

**Recommendation (evidence-based, non-binding):** **(b) Bounded supersession scoped to the Path-N
substantive journey**, with every remaining English substantive surface explicitly enumerated and
carried as a registered obligation rather than silently tolerated. It is the outcome the current
evidence supports: it delivers the Owner's positioning where the journey actually happens, it
matches the existing register structure (the deliverable withdrawn-note localization row already
tracks one such surface separately), and it avoids expanding RVR-7 into the deliverable stack, which
has its own owners.

**Status: `OWNER DECISION REQUIRED` — NOT DECIDED AT THIS FREEZE.** The Owner has selected no
outcome; the recommendation above is advisory and is expressly **not** pre-authorized. Contract
framework authorization is NOT authorization of the supersession, and nothing in this candidate may
be read as deciding it.

**§S.1 — Ordering (binding).** **`D-P6-18 OWNER DECISION MUST PRECEDE THE RVR-7 IMPLEMENTATION PATH
MANIFEST FREEZE`.** Its outcome determines whether the substantive exhaustion / reframe surfaces
(§G.3) are promised in Arabic, and therefore whether they belong inside the RVR-7 implementation
manifest — which is exactly open question **Q2** (§H.1). Q2 is consequently **dependent on D-P6-18**
and cannot be answered before it. Precisely:

1. D-P6-18 **MAY remain unresolved** while this contract-framework candidate is reviewed and
   Owner-accepted — the framework does not depend on its outcome.
2. D-P6-18 **MAY NOT remain unresolved** when the path manifest is frozen: an unresolved D-P6-18
   makes Q2 unanswerable and any manifest claiming to answer it unsound.
3. D-P6-18 is therefore an **explicit prerequisite of the Path Manifest Freeze gate** (§H.3,
   sequencing rule 5), and transitively of Implementation START.

This contract reserves the explicit **Owner Decision Gate** for it at that point in the sequence.

## §T. Test and evidence contract (claim-scoped, dependency-aware)

The future authorized implementation candidate MUST produce, at minimum: (1) content-id completeness
(all 21 ids, mechanically enumerated); (2) EN/AR pairing evidence; (3) the documented
semantic-equivalence review; (4) canonical-state invariance evidence (identical canonical records
and progression for the same inputs in EN and AR); (5) W1-N1 verification discharge; (6) the W1-N2
Arabic adversarial regression (§E.1); (7) proof of no language-conditional routing, including the
clamp-timing isomorphism of §G; (8) marker/registry differential evidence **if** those surfaces are
touched (§K.2); (9) replay/reconstruction parity evidence; (10) real served-route / UI evidence, not
unit stubs alone; (11) Universal Guardrail Smoke PASS; (12) the full suite where the actual runtime
or test-semantic delta requires it, per AHAEP and Lean §5B.

**Evidence economy (AHAEP §1/§7):** unchanged historical facts are not re-proven merely to raise
test counts; every reuse is claim-scoped and dependency-checked, and any evidence whose dependency
the implementation touches is re-run rather than inherited.

## §U. Evidence-reuse and invalidation map (as frozen at this gate)

| Claim | Prior evidence | Dependency | Reusable? | Invalidation trigger |
|---|---|---|---|---|
| RVR-6b implementation correctness | PR #581 pack; focused 48 (14/14/11/9); affected family 22 modules 1637/0/0/0 | `intent_serving.py`, the two registries, the WS10 loader | YES as baseline | any touch of markers/registries/loader — **probable** under §K.2 |
| RVR-6b formal closure | closure record + PR #584 merge identity | closure surfaces | YES (historical fact) | none |
| W1-N3 bounded closure | M-1 fixture reproduction, EN and AR identical outcome | `gap_relevance` + markers | YES, strictly within its bounded scope | marker or `gap_relevance` change |
| Registry loader behavior | loader validation tests; D8/D6 path checks | committed JSON schema + loader | YES | **PROBABLY INVALIDATED** — the recommended Option B adds a variant field and language-aware serving |
| Current marker behavior | R2 / R2-marker / RVR-2 and R3 differential suites green | `_INTENT_MARKERS`, `gap_relevance` byte-unchanged | YES as baseline | any marker/vocabulary edit → must re-run differentials |
| `gap_relevance` baseline | Wave-1 RVR-2 implementation + W2-C differentials | module byte-unchanged | YES | forbidden to change (§F); a change is a STOP |
| EN/AR UI catalog behavior | D-P6-18 (PR #388) closure evidence | `web/ui_text.py`, templates | YES | a §S outcome that supersedes the display rule; or an exhaustion-prompt touch (§H Q2) |
| Full-suite baseline | 4710 passed / 3 skipped / 1 xfailed / 0 failed (4712 collected at this base) | whole tree | YES as baseline only | any runtime delta → full re-run required |

**Explicitly identified as probably invalidated by the proposed direction:** registry/content loader
behavior evidence (schema + serving change) and, if §K.2 fires, marker differential evidence.

## §V. Future RVR-7 classification (derived at this gate, provisional until the manifest freezes)

`FUTURE RVR-7 LEAN LEVEL: LEVEL 2` — an authorized phase increment under an approved contract. It is
not LEVEL 1 on current evidence: no product identity, architecture, database, authentication,
authorization, privacy/security, billing, domain activation, Structured Technical Guidance, release
/ deployment, or main-reconciliation surface is reached (§G escalation test).
**Escalation rule (binding):** if the frozen manifest reaches persistence, the reconstruction
schema, security, product identity, or any other Lean §3 LEVEL-1 trigger, the increment escalates to
**LEVEL 1** with a mandatory independent full suite (Lean §5B.4) — the forecast may never be used to
hold assurance down.
`FUTURE RVR-7 REVIEW DEPTH: DEPTH 2` (escalating with the level).
`FUTURE RVR-7 AHAEP MODE: FULL SEMANTIC LIFECYCLE` — the change is user-visible and behavior-adjacent
(content + serving seam), so the mechanical and focused-differential modes are both inadequate.
`INDEPENDENT REVIEW: REQUIRED` — Lean §5/§5B: user-visible behavior change carrying EN/AR
differential risk, the exact class that produced the historical W2-C R3 leak.

## §W. Self-invalidation

If any proposition in this contract is contradicted by authoritative repository truth at the time of
use, the contradicted proposition is void and the executor STOPS and escalates rather than
proceeding under it. This contract creates no authority of its own, activates nothing, and confers
no implementation permission under any reading.
