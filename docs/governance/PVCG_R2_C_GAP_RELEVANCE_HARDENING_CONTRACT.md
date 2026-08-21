# PVCG-R2-C — Gap-Relevance Hardening Contract / Reconciliation Gate

**Status of THIS record:** governance/documentation-only **INCREMENT-CONTRACT CANDIDATE**. It becomes
AUTHORITATIVE only through the governed lifecycle (Creator Grill → independent external exact-candidate
review → Owner acceptance → SHA-preserving publication → PR → create-a-merge-commit → post-merge
verification). **It implements nothing** (ZERO runtime, test, fixture, pin, or module diff in this
candidate) and, once authoritative, authorizes ONLY the bounded **PVCG-R2-I** implementation increment
defined below — which itself requires separate explicit Owner authorization.

**Authoritative base:** `c70bad196de73fc27c21a3e1bd8438f1eab41958` (PR #547 merge — PVCG-R1;
re-resolved live from `origin/feature/atomic-json-session-persistence` before drafting and
independently re-verified on all four merge criteria: first parent
`9d2b651588dc6879948e89aac3ec43c8c7c873d7`, second parent
`5d563203207d81b49076a98d2ddc8c4411c574de`, merge tree
`24b57a2fcb9cfdaf2e958c5d03f68f4e4a06cfdc`, empty candidate→merge diff).

**`OWNER_DECISION_REGISTER.md` UNCHANGED.** This record declares no release readiness of any kind.

---

## §0. Evidence-class legend (binding on every statement below)

| Class | Meaning |
|---|---|
| **[REPO]** | Authoritative repository fact, citable to a committed file and location. |
| **[EXEC]** | **Creator-local executed diagnostic evidence** produced by a run in this session. It is **NOT** externally retrievable or reproducible by SHA alone (the diagnostic commit is unpublished — §1.1), and it is **NOT promoted to permanent repository fact by being recorded here.** R2-I must re-measure independently. |
| **[OWNER]** | An Owner decision or directive. |
| **[OPEN]** | Unresolved; owed to a later gate. |

Nothing in this record may be read as a repository fact unless marked **[REPO]**.

---

## §1. Why this gate exists

The Owner-approved PVCG **Minimum Launch-Conformance Set** includes **R2 — gap relevance /
manufactured-satisfaction hardening** **[OWNER]**. A bounded R2 implementation was attempted and
**stopped before freeze** because it encountered two governance dependencies that an implementation
gate has no authority to resolve on its own **[OWNER]** (Owner decision: *Option B — split R2 into a
governance contract gate first*).

This contract governs exactly those two dependencies, DEP-1 and DEP-2, and freezes the R2 product
truth. It authorizes no code.

### §1.1 The non-candidate diagnostic SHA

`5154bcf40673e19805410d3199f86089da2c810a` is a **NON-CANDIDATE diagnostic commit** whose own message
says so. It is preserved as immutable diagnostic evidence only.

* It is **NOT** in this candidate's lineage (verified: it is not an ancestor of the authoritative
  base, and this candidate's single parent is the authoritative base) **[REPO]**.
* It must **NOT** be published, merged, reviewed as a candidate, or built upon.
* **It is Creator-local and unpublished.** It exists only in the Creator's working repository, so it is
  **NOT externally retrievable or reproducible by SHA alone**. All findings derived from it are
  therefore classified **Creator-local executed diagnostic evidence** — never repository fact, and
  never independently verifiable merely by citing the SHA. **It must not be published just to make
  those findings reproducible**; R2-I re-measures independently instead.

---

## §2. DEP-1 — `engine/progression_loop.py` byte-pin reconciliation

### §2.1 The pin (authoritative, unchanged by this gate)

`tests/test_p9_mech_i3_signal_quality.py` holds a SHA-256 byte freeze **[REPO]**:

* lines 75–78, `_FROZEN_ENGINE_SHA256`, containing
  `"engine/progression_loop.py": "a8e1ffdf9accf3ed57fc6c32d51c7e77ce9e260c0d39a8ec3030e2635ff03dc3"`;
* enforced at line 313 by `test_engine_files_byte_frozen`, which asserts
  `"engine file changed (forbidden in P9-MECH-I3): {path}"` (line 317);
* the block's own comment states its purpose: *"Engine byte freeze (no classifier/tie/substance-
  semantics change may ride along)."*

Governing authority: `docs/governance/P9_MECH_I3_SIGNAL_QUALITY_AB006_DISPOSITION_CONTRACT.md`
**[REPO]**. **Supersession check: not superseded; the pin is live and enforced at the authoritative
base** (independently re-verified: the working-tree digest of `engine/progression_loop.py` equals the
pinned digest exactly) **[REPO]**.

### §2.2 Why R2 must touch the pinned file

The served `gap_type` and the inventor's answer meet in exactly one place on the live path —
`engine.progression_loop.integrate_response`, which already receives `gap_type` as a parameter
**[REPO]**. A relevance-eligibility decision cannot be made anywhere else without inventing a second
integration seam, which §6 forbids. Therefore the minimum R2 implementation requires a bounded change
to `engine/progression_loop.py`.

**This is NOT** a classifier change, a tie-precedence change, a substance-signal change, a domain
change, or an admission change — i.e. it is not the class of change the pin's comment exists to
prevent. R2 adds a distinct, additive eligibility axis and changes none of those.

### §2.3 Precedent — verified from repository history, not from prose

**Corrected characterization (B-1).** An earlier draft of this contract stated that the
`engine/progression_loop.py` digest had been reconciled **twice**. That was **false** and is withdrawn.
Independently re-derived here by reading the pinned value out of every commit that touched the pin
file, per key **[REPO]**:

| Commit | Gate | `engine/progression_loop.py` | `engine/domain_rules.py` |
|---|---|---|---|
| `32165ca` | P9-MECH-I3 implementation | introduced (`<absent>` → `bbb49b49…`) | introduced (`<absent>` → `5df2ae26…`) |
| `9399f9d` | L2SC-01 runtime implementation | **reconciled** (`bbb49b49…` → `a8e1ffdf…`) | reconciled (`5df2ae26…` → `1977418f…`) |
| `41bf30c` | P10-DBT1 Phase-9 registered-debt remediation | **UNCHANGED** (`a8e1ffdf…` → `a8e1ffdf…`) | reconciled (`1977418f…` → `0e47326a…`) |

Therefore, stated truthfully:

* the **`engine/progression_loop.py` pin reconciliation precedent exists and occurred ONCE**, at
  `9399f9d` **[REPO]**;
* the broader `_FROZEN_ENGINE_SHA256` protection block **was** later updated again at `41bf30c`, but
  that later change concerned **`engine/domain_rules.py` only**, not `engine/progression_loop.py`
  **[REPO]**;
* this history still establishes that **exact digest reconciliation under explicit later governance is
  an established repository mechanism** **[REPO]** — which is the only proposition DEP-1 relies on.

The precedent count is **not** overstated, and the R2-I authorization in §2.4/§2.5 is **not** weakened
by the correction: one prior reconciliation of this exact key, plus a live protection block that has
demonstrably been reconciled per-key under later authorized gates, is sufficient basis for the single
bounded R2 reconciliation authorized below.

> **NB-R2C-1 (non-blocking observation, recorded, NOT fixed here, and NOT relied upon).** The pin
> comment's cross-reference to the L2SC-01 contract does not resolve to a section discussing the pin.
> Independent review indicates this stale-reference defect is **broader than previously described**
> **[OPEN]**, so it is **not reused as evidence anywhere in this contract** — the DEP-1 precedent above
> rests solely on the per-key digest history re-derived from commits, not on that cross-reference. No
> unrelated documentation-synchronization repair is in scope for this gate.

### §2.4 What R2-I is authorized to do — and only this

R2-I **MAY**:

1. modify `engine/progression_loop.py` **solely** to add the relevance-eligibility call and its
   bounded effect at the answer→gap integration seam;
2. recompute the exact post-R2-I digest of that file and **update the pinned value** in
   `_FROZEN_ENGINE_SHA256`;
3. record the reconciliation in the pin's comment block in the established disclosed style.

R2-I **MUST NOT**:

* weaken, delete, disable, skip, or `xfail` `test_engine_files_byte_frozen`;
* remove `engine/progression_loop.py` from `_FROZEN_ENGINE_SHA256`;
* relax P9-MECH-I3 in any other respect, or touch the `engine/domain_rules.py` pin, the pack pins, or
  the mechanical field pins;
* make any other behavioural change to `engine/progression_loop.py` ride along.

**The authorization is ONE BOUNDED R2 RECONCILIATION. It is not, and must never be read as, future
unrestricted edit rights to `engine/progression_loop.py`.** Any later change to that file outside R2-I
requires its own authorization.

### §2.5 Mandatory pin-reconciliation procedure (binding on R2-I, before freeze)

1. Record the **pre-R2 pinned digest** (`a8e1ffdf…`) and prove it matches the base file **[REPO]**.
2. Record the **exact post-R2-I digest** of `engine/progression_loop.py`.
3. Update **only** the pin location(s) that must change.
4. State, in the pin comment and the governance record, **why this is an authorized R2 reconciliation**.
5. **Prove no unrelated progression-loop behaviour changed** — a differential against the previous
   pinned content showing the diff is confined to the authorized relevance seam.
6. Re-run `test_engine_files_byte_frozen` and prove it passes against the NEW digest.
7. Preserve the old digest as historical evidence in the disclosed comment.

The protection mechanism survives the reconciliation. Only its expected value moves.

---

## §3. DEP-2 — defect-dependent fixture correction

### §3.1 The finding

Existing tests drive journeys that satisfy and CLOSE gaps using answers that do not address those
gaps — the exact manufactured-satisfaction behaviour R2 exists to remove **[EXEC]**. Once R2's truth
condition holds, those inputs are **no longer valid evidence** for the post-R2 truth condition.

The largest affected group reuses a Workstream-1 baseline journey whose header states it was *"copied
verbatim from the committed Workstream 3 evidence harness … **do not edit**"*
(`tests/test_structured_criticality.py`, comment block lines 66–69, with *"do not edit"* at line 69;
that same block cites *"contract §11: the reused WS1 journey"*) **[REPO]**.

### §3.1a Prior fixture-preservation authority — named exactly (B-2)

That comment is **not** a casual note. It restates binding prior authority in
`docs/governance/STRUCTURED_CRITICALITY_CAPTURE_INCREMENT_CONTRACT.md` **[REPO]**:

| Locus | Verified wording | Where |
|---|---|---|
| **§11 — RED gate** | *"using the reused WS1 journey (**byte-identical inputs**) and direct real-path fixtures"* | line 99 |
| **§12 — GREEN gate** | *"never-interacted requirements remain byte-identical to today (`UNDETERMINED`/`system-derived`, existing wording — **asserted on the untouched WS1 journey**)"* | §12 spans lines 101–110; the phrase is at **line 105** |
| **F4** | *"WS1/WS2/WS3 evidence trees **byte-identical** (F4)"* | line 117 |

> **Correction (B-3) — withdrawal of a false precision note.** An earlier revision of this contract
> stated that §12's heading and body state the GREEN acceptance criteria and that *"the literal phrase
> 'untouched WS1 journey' does not appear there"*, and on that basis carried the byte-identical /
> untouched obligation on **§11** and **F4** alone. **That statement was false and is withdrawn.**
> Re-verified directly against the authoritative repository: `## 12. GREEN gate` begins at line 101 and
> `## 13.` begins at line 111, so **§12 spans lines 101–110**; the *Correctness* paragraph at **line
> 105** — inside §12 — contains the literal phrase **`asserted on the untouched WS1 journey`**.
> §12 is therefore **part of the prior fixture-preservation / evidence authority in its own right**,
> not merely the head-side companion of §11, and it must be reconciled for PVCG-R2-I. The earlier
> narrower framing must not be relied on by any reviewer or by R2-I. No wording is attributed to any
> locus that the locus does not contain: each cell above quotes the verified text at the cited line.

### §3.1b Narrow supersession / reconciliation of that authority

**Binding rule.** For **PVCG-R2-I only**, and **only** for fixture inputs proven to depend on
manufactured satisfaction, the prior preservation requirements in **§11**, the **§12 acceptance
criterion predicated on the untouched WS1 journey**, the **live fixture provenance/preservation
comment**, and **F4 to the minimum extent directly affected** are **SUPERSEDED only as necessary to
replace defect-dependent inputs with gap-appropriate inputs.**

The reconciled set is exactly:

| # | Reconciled locus | Citation |
|---|---|---|
| 1 | **§11** — the reused WS1 journey, *byte-identical inputs* | `STRUCTURED_CRITICALITY_CAPTURE_INCREMENT_CONTRACT.md` line 99 |
| 2 | **§12** — the acceptance criterion predicated on the *untouched WS1 journey* | same file, line 105 (§12 = lines 101–110) |
| 3 | **the live fixture provenance/preservation comment** | `tests/test_structured_criticality.py`, comment block lines 66–69; *"do not edit"* at line 69 |
| 4 | **F4** — only to the minimum extent directly affected | `STRUCTURED_CRITICALITY_CAPTURE_INCREMENT_CONTRACT.md` line 117 |

**§12 is explicitly inside this reconciled set (B-3).** It is not reached by implication through §11,
and it is not omitted.

Bounding conditions, all binding:

* The supersession reaches **only** inputs that satisfy every test in §3.4. It reaches nothing else.
* Superseding the §12 criterion means **only** that a *defect-dependent* WS1 input may be replaced. The
  rest of §12 — every other correctness, usability and protection acceptance criterion — stands in
  full, and the never-interacted `UNDETERMINED`/`system-derived` semantics that criterion protects are
  **not** changed by R2. R2-I proves that separately or STOPS.
* The prior authority **remains historical evidence** and is not deleted, rewritten, or invalidated.
  It remains the correct account of what WS1–WS4 required at their own gates.
* This is **NOT** general permission to rewrite WS1 evidence or fixtures. Outside the proven
  defect-dependent set, the byte-identical/untouched requirement stands unchanged.
* **F4 supersession is NOT broadened by this clause.** *"To the minimum extent directly affected"*
  means only that F4 ceases to be a bar to the authorized **fixture-input** correction itself. It does
  **not** authorize regenerating, rewriting, or synchronizing any committed WS1–WS7 evidence artifact.
  `COMMITTED EVIDENCE TREES REMAIN FROZEN` by default — see §3.5. If a future R2-I fixture change makes
  historical evidence materially false, unreproducible, or misleading, R2-I **STOPS** and obtains
  separate Owner authorization before any regeneration or rewrite. Evidence is never silently
  synchronized.

### §3.2 Authorization granted to R2-I

R2-I **MAY** correct **only** those fixtures whose existing **input** encodes manufactured
satisfaction, and **only** by replacing that input with a gap-appropriate answer.

**Binding rule:** *preserve the original assertion target and test purpose; replace only the
defect-dependent input.*

R2-I **MUST NOT**:

* delete a test merely because R2 makes it fail;
* weaken, loosen, or remove an assertion;
* mark a test `skip` or `xfail` to obtain green;
* broaden the relevance guard to re-admit the old defective fixture;
* rewrite unrelated tests;
* alter expected product behaviour beyond the R2 truth condition in §4.

### §3.3 Mandatory fixture-differential ledger (binding on R2-I)

For **every** changed test fixture, R2-I must publish a ledger row containing **all eleven** fields:

1. **source test file**;
2. **served gap**;
3. the **original fixture answer** (verbatim);
4. **why it depended on manufactured satisfaction**;
5. the **replacement gap-appropriate answer** (verbatim);
6. the **assertion target BEFORE**;
7. the **assertion target AFTER**;
8. **CROSS-FILE / EVIDENCE IMPACT**;
9. whether the **same fixture/input is duplicated elsewhere**;
10. whether any **committed evidence artifact refers to or embeds it**;
11. whether a **generator/harness embeds the old input**.

Required result: **`ASSERTION-TARGET CHANGES: 0`**.

If any assertion target must change, R2-I **STOPS FOR OWNER REVIEW** before freeze. It may not be
resolved by the implementing agent.

Fields 8–11 are mandatory because the WS1-style journey input is **shared**, not local. Executed
scoping at this base, recorded as **[EXEC]** so R2-I re-measures rather than trusting it: the WS1 base
sentence appears in **5 test files**, **44 committed evidence artifacts across 7 evidence trees**
(`workstream1_deliverable_baseline` … `workstream7_actionable_validation_plan`), and **7
generator/harness scripts**. A fixture edit is therefore never self-contained by default.

### §3.4 Fixture-scope rule — all five must be proven

R2-I may modify a fixture **only** when **every** one of these is proven for that fixture:

1. the existing fixture input **relies on the manufactured-satisfaction defect**;
2. the **R2 truth condition causes the fixture to fail for that reason** (and not for another);
3. the **original assertion target remains valid**;
4. **only** the input necessary to truthfully address the served gap is changed;
5. **assertion semantics remain unchanged**.

Failing any one of the five, the fixture is **out of scope** and must be left alone.

### §3.5 Committed WS1–WS7 evidence trees — DEFAULT FREEZE

**`COMMITTED EVIDENCE TREES REMAIN FROZEN`.** Regeneration of committed WS1–WS7 evidence trees is
**NOT** authorized by this contract, automatically or otherwise. R2-I may correct defect-dependent
test-fixture inputs **without** rewriting historical evidence artifacts.

If a changed fixture makes a committed evidence artifact or a generator claim **materially false,
unreproducible, or misleading**, R2-I must:

1. identify the **exact affected artifact**;
2. identify the **exact generator/harness**, if any;
3. explain **why leaving it unchanged would be untruthful**;
4. **STOP before any regeneration or evidence rewrite**;
5. **request Owner authorization** for the evidence synchronization as a separate decision.

Historical evidence must remain **distinguishable from current post-R2 behaviour**. Silent regeneration
is prohibited.

### §3.6 Generator / harness classification rule

R2-I must inspect `docs/governance/evidence/workstream3_deliverable_hygiene/generate_ws3_artifacts.py`
and every other committed generator or harness that embeds or reproduces the old WS1-style input, and
**classify each one** as exactly one of:

* **unaffected**;
* **historical-only and frozen**;
* **requires future evidence-synchronization authorization**.

Classification is mandatory; acting on the third class is **not** authorized here. Executed scoping at
this base identified **7 such scripts** **[EXEC]** — `generate_ws3_artifacts.py`,
`generate_ws4_artifacts.py`, `generate_ws5_artifacts.py`, `generate_ws6_artifacts.py`,
`generate_ws7_artifacts.py`, `reproduce_baseline.py`, and `regenerate_and_compare.py`. **R2-C modifies
none of them**, and R2-I may not modify any of them without a separate Owner authorization.

### §3.7 Stale "do not edit / byte-identical" comments must be corrected truthfully

If R2-I changes a fixture whose source comment claims the input is *copied verbatim*, *byte-identical*,
*untouched*, or *do not edit*, and that statement becomes **false** after the authorized correction,
R2-I **must update that comment/documentation truthfully in the same candidate**.

The replacement wording must **preserve historical provenance** — conceptually: *originally copied from
the WS1 evidence harness; later explicitly reconciled under PVCG-R2 because the original input encoded
manufactured satisfaction*.

**Do not erase history. Do not leave a false "byte-identical / untouched" claim standing.**

---

## §4. The R2 product truth (frozen by this contract)

> **A response may influence gap satisfaction only when it is sufficiently relevant to the specific
> served gap/question context.**
>
> **Generic technical substance, domain vocabulary, causal language, or signal density alone is
> insufficient to establish satisfaction for an unrelated gap.**
>
> The decision must be **deterministic** and **fail-closed**: `uncertain relevance ≠ satisfied`.

Fail-closed means *not eligible to satisfy or close*. It must **NOT** be converted automatically into
`BLOCK`, a contradiction, an input-validation failure, a quality downgrade, or a claim that the
inventor's answer is wrong.

### §4.1 Executed diagnostic evidence supporting the requirement

**Creator-local executed diagnostic evidence** produced at the unpublished non-candidate diagnostic
commit `5154bcf4…`; **[EXEC]**, not repository fact and not externally reproducible by SHA alone:

* At the authoritative base, one signal-rich, causally-structured sentence that answers nothing
  (*"The circuit uses a sensor and a relay and a capacitor and a resistor, and the voltage increases
  because the current flows through the microcontroller."*) is rated `REASONED` and, served against
  each gap in turn, returns `PASS` and `CLOSED` for **all six** gap types, and sets `known_mechanism`
  for `MECHANISM_COMPLETENESS`.
* With the exploratory R2 test file, RED at the authoritative base was **36 failed / 5 passed** — 22
  behavioural-defect failures plus 14 failures caused solely by the not-yet-existing module — and
  GREEN was **41/41** at the diagnostic SHA.
* PVCG-R1 focused suite remained **26/26** and `UNIVERSAL GUARDRAIL SMOKE: PASS` throughout.
* With the guard active the full suite showed **59 affected items across 14 files**; **zero** of them
  touched R1, persistence, reconstruction, or the smoke manifest.
* Per-iteration eligibility tracing of the WS1 baseline journey showed its answers are **never**
  eligible for `BOUNDARY_AMBIGUITY` at any iteration, which is why that journey cannot complete once
  the truth condition holds.

These figures are **executed evidence at a non-candidate SHA**. R2-I must re-measure independently and
must not carry them forward as established fact.

---

## §5. Explicit non-goals — NOT AUTHORIZED by this contract

R2-C authorizes none of the following, and R2-I must not introduce any of them:

* **PVCG-R3 Semantic Stability** — and specifically **EN/AR equivalence remediation**;
* full **Adaptive Questioning**; question **skip / reorder / add** behaviour;
* **WS10** activation; **WS11** activation or integration; **WS12** progression role;
* **Stage 3 evaluator** integration;
* a full **contradiction engine** (PVCG-R4);
* any **LLM / NLP subsystem**, embeddings, vector store, probabilistic classifier, model-based
  adjudication, or external semantic model call;
* domain expansion or domain activation; versioning / change-impact; Render; `main` reconciliation;
  deployment; provider selection.

**R2-C must not, and does not, turn gap relevance into a general semantic-understanding claim.** If
the R2-I solution is lexical/deterministic, it must be described truthfully as lexical, and its
inability to stabilise materially equivalent wording or a different language must be stated as a
known bound — not concealed and not framed as understanding meaning.

---

## §6. Implementation shape — contractual bounds only

R2-I **may** introduce the **smallest deterministic relevance-eligibility seam** necessary to decide:

> *Does this answer address this served gap/question sufficiently to be eligible for satisfaction?*

Permitted:

* one bounded, pure, deterministic relevance module;
* a narrow integration call at the **existing** answer→gap seam (`integrate_response`);
* test-only fixture corrections required by the new truth condition (§3);
* exact re-freezing of the P9-MECH-I3 progression-loop digest (§2.5).

Prohibited: a broad new architecture, a second integration seam, a parallel evaluation pipeline, or a
new truth source. R2-C does **not** prescribe any particular internal design; R2-I must justify the
design it chooses against repository truth and must not build more than the requirement needs.

Progression isolation (binding): R2-I must not redesign gap priority, maturity thresholds, stage
transitions, question ordering, Path N, domain activation, answer persistence, R1 reconstruction,
readiness, or correction/supersession. The only authorized effect is preventing invalid manufactured
satisfaction caused by lack of gap relevance.

---

## §7. Existing dormant components

WS10 (`engine/question_intent_registry.py`), WS11 (`engine/question_aware_evaluation.py`) and WS12
(`engine/controlled_unknown_progression.py`) are dormant by their own merged contracts and are not
reachable from `web.app` **[REPO]**.

* Their **architectural ideas may be referenced** in R2-I's design reasoning.
* **No dormant component becomes runtime reachable merely because it is convenient.**
* Any actual activation requires its own contract amendment and Owner authorization, and remains
  outside R2 entirely.
* WS10 additionally has **no committed registry artifact**, so it could not be activated by R2-I even
  if that were authorized **[REPO]**.

---

## §8. Required R2-I RED / GREEN shape

**RED — at the authoritative base, re-measured independently by R2-I:**

* a signal-rich off-topic answer can satisfy/close unrelated gaps;
* the same generic answer can satisfy materially different gaps.

**GREEN — at the R2-I candidate:**

* an off-topic signal-rich answer cannot satisfy the unrelated served gap;
* a gap-appropriate answer still progresses normally;
* an answer copied from Gap A cannot automatically satisfy Gap B (at least two materially different
  gaps must be exercised, and no single hard-coded sentence may be special-cased);
* the decision is deterministic — same served gap context, same canonical state, same answer, same
  eligibility outcome; no wall-clock, no randomness, no model output;
* **PVCG-R1 behaviour is unchanged**: the five governed non-answer dispositions still persist and
  reconstruct across a real process restart, no second truth source appears, and accepted-answer
  replay stays compatible. The existing R1 focused suite runs **unchanged** and must stay green.

---

## §9. Full-suite reconciliation rule (binding on R2-I)

R2-I may correct a failing defect-dependent fixture only after:

1. proving it fails **because** the new R2 truth condition invalidates its old input;
2. confirming its assertion target remains valid;
3. replacing **only** the input needed to make the fixture truthfully gap-appropriate.

R2-I must return the full suite to green **without** weakening R2, weakening any guard, deleting
coverage, or changing unrelated assertions. `UNIVERSAL GUARDRAIL SMOKE` must PASS and must not be
weakened.

---

## §10. Status ledger preserved by this gate

| Item | Status |
|---|---|
| PVCG-R1 | **AUTHORITATIVE** (PR #547, merge `c70bad19…`) |
| PVCG-R2-C | governance candidate — **NOT AUTHORITATIVE UNTIL MERGED** |
| PVCG-R2-I | **NOT STARTED / NOT AUTHORIZED** until R2-C is authoritative **and** a separate Owner execution authorization is issued |
| PVCG-R3 (semantic stability) | **NOT STARTED** |
| PVCG-R4 (correction / invalidation) | **NOT STARTED** |
| PVCG | **NOT SATISFIED** |
| Minimum Launch-Conformance Set | **NOT SATISFIED** |
| Controlled / Public / Commercial release readiness | **NO CLAIM** |

---

## §11. Review path

LEVEL 2 governance-only under the LEAN §5B risk-based review model, with mandatory independent smoke.
Zero executable bytes change in this candidate, so §5B.1's full-suite Creator-evidence trigger is not
met by an implementation change; the authoritative full-suite truth
(**3021 passed / 3 skipped / 1 xfailed / 0 failed**) stands from the merged PVCG-R1 lineage and was
independently re-run at this base during this gate **[EXEC]**.

**Environment precondition for that figure (stated truthfully, not implementation scope).** The
serving-stack access-log tests EXECUTE only when `gunicorn` is resolvable on `PATH`; where it is not,
they SKIP and the skipped/passed split differs. The figure above was measured in an environment where
`gunicorn 26.1.0` was on `PATH`, so those tests ran rather than skipped **[EXEC]**. Any later
re-measurement must state its own `PATH` precondition rather than assuming this one. R2-I must not
convert this precondition into implementation scope.

Next required step after Owner acceptance: SHA-preserving publication, then a **separate** Owner
execution authorization before any R2-I work begins.
