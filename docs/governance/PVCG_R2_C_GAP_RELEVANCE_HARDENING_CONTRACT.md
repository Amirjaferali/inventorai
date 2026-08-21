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
| **[EXEC]** | **Executed diagnostic evidence** produced by a run in this session. Reproducible at the stated non-candidate diagnostic SHA. **It is NOT promoted to permanent repository fact by being recorded here.** |
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
* Its purpose is solely to make the **[EXEC]** evidence in §4 reproducible.

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

The pinned digest has been reconciled **twice** under later authorized gates **[REPO]**:

| Event | Commit | Gate |
|---|---|---|
| Pin introduced | `32165ca` | P9-MECH-I3 implementation |
| Digest reconciled (1st) | `9399f9d` | L2SC-01 runtime implementation |
| Digest reconciled (2nd) | `41bf30c` | P10-DBT1 Phase-9 registered-debt remediation |

Each reconciliation is disclosed in the pin's own comment block **[REPO]**. Re-freezing under an
explicitly authorized later gate is therefore an **established governed procedure**, not a novelty.

> **NB-R2C-1 (non-blocking observation, disclosed, NOT fixed here).** The pin comment cites
> "`L2SC01_SUBSTANCE_SIGNAL_PLURAL_ALIAS_INCREMENT_CONTRACT.md §10`" for the first reconciliation, but
> §10 of that document is titled *"Compression rationale — corrected (survives pack scoping)"* and does
> not discuss the pin **[REPO]**. The reconciliation **did** occur (commit `9399f9d`, above); only the
> section cross-reference appears inaccurate. Recorded for a future documentation-synchronization gate;
> **no correction is authorized here.**

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
(`tests/test_structured_criticality.py`, line 69) **[REPO]**.

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

For **every** changed test fixture, R2-I must publish a ledger row containing:

1. the original fixture answer (verbatim);
2. the served gap;
3. why the original answer depended on manufactured satisfaction;
4. the replacement gap-appropriate answer (verbatim);
5. the assertion target **before**;
6. the assertion target **after**;
7. explicit confirmation that assertion semantics did not change.

Required result: **`ASSERTION-TARGET CHANGES: 0`**.

If any assertion target must change, R2-I **STOPS** and seeks Owner review before freeze. It may not
be resolved by the implementing agent.

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

Reproducible at the non-candidate diagnostic SHA `5154bcf4…`; **[EXEC]**, not repository fact:

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

Next required step after Owner acceptance: SHA-preserving publication, then a **separate** Owner
execution authorization before any R2-I work begins.
