# G-4 MECHANISM A — EN CAUSAL FALSE-POSITIVE CORRECTION — IMPLEMENTATION CONTRACT (CANDIDATE)

**STATUS AT CREATION: `CONTRACT CANDIDATE — NOT AUTHORITATIVE`.** Created on the authoritative base
`3359c92a3a05c1306feb959ce55e1e7fd8fd8267`, verified live from Git at this gate `[EXEC]`.

`IMPLEMENTATION AUTHORIZED: NO` · `IMPLEMENTATION STARTED: NO` · `MECHANISM B: NOT IN SCOPE, NOT
AUTHORIZED` · `M-1 RELEVANCE: NOT IN SCOPE` · `G-4 FULL CLOSURE: NOT ASSERTED BY THIS CONTRACT`. This
document is a contract freeze only; it authorizes nothing. Every candidate-era statement is scoped to
this gate's freeze and stays true once the gate resolves.

## §1. Authority and scope

Governed by Owner decision **OD-G4-A** (`OWNER_DECISION_REGISTER.md`) and the G-4 obligation row
(`DEFERRED_OBLIGATIONS_REGISTER.md` §3, `OPEN` / `FRB`, ownership adjudicated as **COMPOSITION ACROSS
EXISTING OWNERS**). This contract covers **G-4 Mechanism A ONLY**.

**Mechanism B is expressly excluded** — `_structured_technical_form`, the hyphenated-compound trigger and
any structural-signal change are **NOT** touched, and OD-G4-B records `MECHANISM-B CODE CHANGE: NOT
AUTHORIZED`. **M-1 relevance is expressly excluded** — it is language-symmetric and owned by
`gap_relevance` / RVR-2 with RVR-7 downstream return.

## §2. The measured defect this contract exists to correct

`MEASURED EVIDENCE` at this base:

| | Answer | `assess_response` | `_has_causal_structure` | Cause |
|---|---|---|---|---|
| **EN** | `E-1\|novice\|en` `MECHANISM_COMPLETENESS[1]` | `REASONED` | **True** | raw-substring hit on **`"if "`** inside *"…not have a wire going to the brake lever **if I can avoid it**"* |
| **AR** | `E-1\|novice\|ar` `MECHANISM_COMPLETENESS[1]` | `ASSERTED` | **False** | the equivalent Arabic preference wording is not a registered `CAUSAL_SURFACES` entry |

The matched clause states a **user installation preference**, not a causal mechanism, and the match is a
**legal word-boundary match** — so this is a semantic false positive, not a tokenization artifact. The
English side is over-permissive; the Arabic side is correct.

**Consequence the Owner has accepted (OD-G4-A):** correcting this means the English novice journey will
no longer close `MECHANISM_COMPLETENESS` on that answer, because the previous closure was **not
semantically earned**.

## §3. Objective

Remove or constrain **the measured English preference-clause false positive**, so that the same meaning
expressed in English and in Arabic receives the same truthful assessment — **without** widening Arabic
recognition, **without** creating a new assessment capability, and **without** altering unrelated causal
patterns.

## §4. Solution-space boundary — deliberately NOT pre-selected

This contract **does not mandate a code mechanism**, and must not be read as selecting one. It records
one measured feasibility fact and one measured risk, and leaves the predicate choice to the
implementation gate.

**Feasibility fact `[MEASURED]`.** Removing `"if "` from `_CAUSAL_STRUCTURE_PATTERNS` changes the
causal-structure result of **exactly one answer in the entire frozen EN corpus** — the target answer —
and it is the **only** corpus answer where `"if "` is the sole causal hit. No RVR-3 pin breaks
(`test_novice_answers_do_not_regress` pins `novice|en` `[0]`, which fires on `"when "`). A bounded
correction therefore **exists**, so the `STOP — BOUNDED G-4-A CONTRACT NOT SAFE` condition does not fire.

**BINDING TWO-SIDED REQUIREMENT — a genuine-causal false negative is NOT acceptable, and disclosure does
NOT make it acceptable.** A blanket removal of `"if "` would also stop recognising a **genuine causal
conditional** such as *"if the wheel speed drops, the light turns on"*. The frozen corpus **cannot detect
that regression** — it contains exactly one answer using `"if "` at all. The correction is therefore
bound to satisfy **both** sides at once:

1. the **measured preference clause no longer qualifies as causal structure**; **AND**
2. **genuine causal conditional constructions remain truthfully recognised**, demonstrated by **targeted
   deterministic tests** written independently of the frozen corpus.

The implementation gate must state explicitly which predicate change it adopts and why. **Trading (2)
away to obtain (1) is NOT an acceptable outcome, and reporting the loss does not authorize it** — an
implementation that newly rejects a genuine causal conditional **fails this contract** and must not be
presented as passing.

**The one authorized exit, if both sides cannot be satisfied.** If **no bounded deterministic correction
within the authorized surfaces of §5** can distinguish the measured preference use of `"if"` from genuine
causal conditional use, the implementation gate must return

    STOP — BOUNDED G-4-A CORRECTION REQUIRES OWNER DECISION

and **return rather than accept a new genuine-causal false negative through disclosure alone**. Reaching
for a new semantic model, an NLP subsystem, Arabic widening or a broad causal-table redesign in order to
avoid that STOP is **prohibited** — see the prohibition list immediately below, and §5.

**Prohibited as a solution:** widening Arabic to mirror the false positive · adding any semantic
interpretation or model inference · redesigning the causal table beyond the measured matcher · expanding
`semantic_registry` · creating any second assessment, relevance, Arabic-language or normalization owner.
If the correction cannot be made without one of these, the implementation gate must return
`STOP — BOUNDED G-4-A CORRECTION REQUIRES OWNER DECISION` rather than proceed — the **same** required
return as the both-sides-unsatisfiable case above, because both need the same separate Owner decision.

## §5. Allowed implementation surfaces (exhaustive)

1. `engine/progression_loop.py` — `_CAUSAL_STRUCTURE_PATTERNS` and/or the existing
   `_has_causal_structure` handling, **only as required for Mechanism A**.
2. `tests/test_causal_connective_substance_gate.py` — amendment of the byte-pinned expectation
   `test_existing_causal_structure_patterns_frozen`, **only as OD-G4-A explicitly authorizes, and only as
   part of this bounded correction**.
3. One bounded new G-4-A test surface, if necessary.

**Excluded, and not authorized by any reading of this contract:** `engine/semantic_registry.py` ·
`CAUSAL_SURFACES` · `SUBSTANCE_SURFACES` · Arabic normalization · `engine/gap_relevance.py` ·
`engine/intent_serving.py` · `_structured_technical_form` and the hyphen logic · `engine/scoring.py` ·
domain packs · pins · the replay benchmark and golden fixtures · `web/` · the S2 instrument, its frozen
corpus and all benchmark evidence. **If another surface is required, the implementation gate must STOP
and return the exact dependency** rather than widen scope.

## §6. Acceptance evidence contract — frozen BEFORE implementation

The implementation gate is bound to this list. **No PASS is pre-decided**, and no item may be waived by a
green suite elsewhere.

### A. BASE RED — prove the cause, do not infer it

1. `A-1` At the authoritative base, the measured EN preference clause assesses **`REASONED`**, and
   `_has_causal_structure` returns **True** for it.
2. `A-2` The cause is proven **at the matcher**, not inferred from final progression: the demonstration
   must show that **`"if "` is the matching pattern**, and that it is the **sole** causal hit for that
   answer.
3. `A-3` The equivalent Arabic clause assesses **`ASSERTED`** with `_has_causal_structure` **False** at the
   same base.

### B. GREEN

4. `A-4` The EN preference clause **no longer qualifies as causal structure through the incidental
   matcher**.
5. `A-5` The measured EN/AR pair reaches **equivalent truthful assessment** — asserted on both members of
   the pair, not on the English side alone.
6. `A-6` **Arabic recognition is not widened**: `engine/semantic_registry.py` is **byte-unchanged**, and
   `CAUSAL_SURFACES` / `SUBSTANCE_SURFACES` gain no member.
7. `A-7` **No system behaviour calls the preference clause causal mechanism structure** — asserted at the
   predicate, and on any surface that renders or records an assessment for it.
8. `A-8` **Genuine causal conditional constructions remain truthfully recognised**, demonstrated by
   **targeted deterministic tests** written independently of the frozen corpus (§4). **A newly introduced
   genuine-causal false negative FAILS this item; disclosing it does not satisfy it.** If both sides of
   §4 cannot be satisfied within the §5 surfaces, the required return is
   `STOP — BOUNDED G-4-A CORRECTION REQUIRES OWNER DECISION`, not a disclosed regression.

### C. REGRESSION

9. `A-9` All remaining `_CAUSAL_STRUCTURE_PATTERNS` entries and their intended semantics are unchanged,
   unless the contract-bound implementation identifies an **unavoidable bounded dependency** and states it.
10. `A-10` **RVR-3 expert MECHANISM EN/AR pins remain green**
    (`test_expert_mechanism_closure_answers_reach_reasoned_en_and_ar`).
11. `A-11` **RVR-3 expert PHYSICAL English pins remain green**
    (`test_expert_feasibility_and_boundary_answers_reach_reasoned_en`).
12. `A-12` The existing assessment and progression suites remain green.
13. `A-13` The **full repository suite is run and actual counts are returned** — including any
    pre-existing failure, disclosed as pre-existing with evidence, never absorbed into a clean claim.

### D. GOVERNANCE

14. `A-14` **Mechanism B remains unchanged and OPEN** — `_structured_technical_form` and the hyphen logic
    byte-unchanged.
15. `A-15` **M-1 relevance remains untouched** — `engine/gap_relevance.py` byte-unchanged.
16. `A-16` **No G-4 full closure is asserted** — the G-4 row stays `OPEN` / `FRB`; completing Mechanism A
    alone does not close it.
17. `A-17` **No new assessment, language, relevance or normalization owner is created**; one assessment
    model and one relevance owner are preserved.
18. `A-18` The benchmark instrument, its frozen corpus and all benchmark evidence are **byte-unchanged**;
    `NO S2 RUN` is performed or implied.

## §7. Known measured consequence — disclosed, not hidden

Correcting Mechanism A is expected to change the measured S2 behaviour of the English novice E-1 record:
`MECHANISM_COMPLETENESS` would no longer close on that answer, so R1 would behave like R3. **This is
parity achieved by removing an unearned closure**, accepted by the Owner in OD-G4-A. It must be reported
as a measured consequence at the implementation gate. **It does not license a benchmark re-run**, and it
does not by itself change any recorded S2 result — historical evidence is never rewritten.

## §8. Lifecycle and non-authorization

This contract becomes authoritative only through Lead review, Independent Review, Owner exact-SHA
acceptance, separate publication authorization, PR, separate merge authorization, a merge commit and
post-merge identity verification. **Implementation START is a further separate Owner decision** after
that.

**Fences unchanged by this contract:** `G-4: OPEN / FRB` · `MECHANISM B: OPEN / DEFERRED, CODE CHANGE NOT
AUTHORIZED` · `M-1 RELEVANCE: SEPARATE OWNER, UNTOUCHED` · `RVR-3: NOT REOPENED` · `RVR-7: NOT REOPENED` ·
`W1-N3 / RVR-2: NOT REOPENED` · `T1-A′: OPEN` · `T1-C′ / T1-D: OPEN, SEPARATE` · `G-5: UNCHANGED` ·
readiness reconciliation **ELIGIBLE, NOT CONVENED** · `FDC-001 LANE: INACTIVE` · `DECISION WORKSPACE /
PATH-T: NOT ACTIVATED` · `ODS-001: NOT ACTIVATED` · `THIRD S2 RUN: CONSUMED` ·
`FOURTH S2 RUN: NOT AUTHORIZED` · `FURTHER SUPPLEMENTAL SLICE EXECUTION: NOT AUTHORIZED` ·
`FCORA AUTHORIZED: NO` · `PSRR GO: NO` · `ACTIVE CONTRACT: NONE` (untouched) ·
`DEPLOYMENT / PRODUCTION / SERIOUS RELEASE / PAID ACTIVATION: NOT AUTHORIZED` · `main` NOT RECONCILED.

**Lean classification.** `LEAN RISK LEVEL: 2` · `REVIEW DEPTH: 2` — bounded governance-only contract
freeze, zero executable delta.
