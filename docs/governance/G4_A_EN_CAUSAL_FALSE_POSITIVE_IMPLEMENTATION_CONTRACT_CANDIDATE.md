# G-4 MECHANISM A — EN CAUSAL FALSE-POSITIVE CORRECTION — IMPLEMENTATION CONTRACT (CANDIDATE)

**STATUS AT CREATION: `CONTRACT CANDIDATE — NOT AUTHORITATIVE`.** Created on the authoritative base
`3359c92a3a05c1306feb959ce55e1e7fd8fd8267`, verified live from Git at this gate `[EXEC]`.

`IMPLEMENTATION AUTHORIZED: NO` · `IMPLEMENTATION STARTED: NO` · `MECHANISM B: NOT IN SCOPE, NOT
AUTHORIZED` · `M-1 RELEVANCE: NOT IN SCOPE` · `G-4 FULL CLOSURE: NOT ASSERTED BY THIS CONTRACT`. This
document is a contract freeze only; it authorizes nothing. Every candidate-era statement is scoped to
this gate's freeze and stays true once the gate resolves.

**AMENDMENT 1 (this gate) — bounded digest-pin allowance + genuine-conditional falsification
hardening.** Governed by Owner decision **OD-G4-A1** (`OWNER_DECISION_REGISTER.md`), recorded on the
authoritative base `89534a55720a25b8d5928c76bf09011e608294b0`, verified live from Git at this gate
`[EXEC]`. Amendment 1 changes **§5** (adds a fourth allowed surface class, bounded to a mechanical
digest re-freeze) and **§6** (adds sections **E** and **F**). It changes **nothing else**: §2's measured
defect, §3's objective, §4's binding two-sided requirement and its prohibition list, and §7's disclosed
consequence stand **unamended**. **Amendment 1 does not resume, restart or authorize implementation** —
`IMPLEMENTATION AUTHORIZED: NO` remains true, and the implementation START that was previously
authorized was returned unstarted under `STOP — IMPLEMENTATION REQUIRES OUT-OF-CONTRACT SURFACE`; a
further separate Owner decision is required to resume it. `EXECUTABLE DELTA: 0` at this gate.

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

**Amendment 1 — measured falsification of the exploratory mechanism, recorded so it cannot be mistaken
for the frozen answer.** The blocked implementation attempt explored a qualifier-list predicate that
treats a leading `"if I can" / "if I could" / "if I may" / "if I might" / "if we can" / "if we could" /
"if we may" / "if we might" / "if possible" / "if at all possible"` occurrence as non-causal and any
other `"if "` as causal. That mechanism **is recorded as evidence only and is NOT frozen as the required
code solution.** It is **measured to fail** the falsification case Amendment 1 now requires: for
*"if I can detect wheel slip, the controller turns on"* the base matcher's **sole** causal hit is
`"if "`, `has_registered_causal_structure` is **False**, and the sentence **opens with the qualifier
`"if i can"`** — so the qualifier-list predicate would return **False** and introduce exactly the
genuine-causal false negative §4 forbids `[EXEC]`. The implementation gate must therefore **not** adopt
it unchanged, and must not read this paragraph as selecting any replacement.

**Solution space is narrowed by that measurement, not closed by it.** Recorded as an observation and
**not** as a mandated mechanism: the measured preference clause (*"…if I can avoid it"*) is a **trailing
`if` clause with no consequent**, while the falsification case is an **`if X, Y` construction with a
consequent clause**. Whether any bounded deterministic predicate within §5 can carry that distinction
truthfully is for the implementation gate to establish by measurement. If it cannot, the required return
remains `STOP — BOUNDED G-4-A CORRECTION REQUIRES OWNER DECISION` — reaching outside §5 to avoid that
STOP stays prohibited.

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
4. **`AMENDMENT 1`** — `tests/test_p9_mech_i3_signal_quality.py`,
   `tests/test_p9_mech_i4_boundary_corpus.py` and `tests/test_p9_mech_i5_question_sufficiency.py`,
   **for a mechanical SHA-256 digest re-freeze of the `engine/progression_loop.py` pin ONLY** — that is,
   replacing the stale `_FROZEN_ENGINE_SHA256["engine/progression_loop.py"]` value with the digest of the
   candidate's own bytes, plus the lineage comment the existing pin-comment convention in those files
   requires. Nothing else in those three files may change. See §5.1.

### §5.1 Amendment 1 — bounded digest-pin allowance (exhaustive limits)

**Why the allowance exists `[MEASURED]`.** Three P9 modules pin the whole-file SHA-256 of
`engine/progression_loop.py` (`a7e8bd62b9ab76aaba5889ce52b5f32ee646b2817ba1c790ed7a231d259fa41f` at this
base), and two guards enforce that pin —
`tests/test_rvr7_render_edge_resolution.py::test_progression_loop_is_byte_unchanged_by_rvr7` and
`tests/test_w2b_amc_consumers.py::test_exactly_three_p9_files_pin_the_current_digest`. **Any** byte change
to `engine/progression_loop.py`, including the §5 item 1 Mechanism-A correction, turns those guards
red until the pin is re-frozen. This is a **mechanical consequence of pinning**, not a P9 behavioural
question. This allowance is the same bounded shape as the historical `W2-B §G` and `W2-C §M` digest-pin
allowances already recorded in those files' pin-comment lineage `[REPO]`.

**Authorized, and only this:** replacing the `engine/progression_loop.py` digest value in the three named
files with the digest computed from the candidate's own final `engine/progression_loop.py` bytes, and
adding the lineage comment the surrounding convention requires.

**FORBIDDEN under this allowance — each one exceeds it:** changing any P9 test logic, assertion,
expectation, fixture, corpus, threshold or signal list · changing any **other** pin, including
`_FROZEN_ENGINE_SHA256["engine/domain_rules.py"]`, `_FROZEN_PACK_SHA256` and `_FROZEN_MECH_FIELDS` ·
adding, removing, renaming, skipping or xfailing any test · relaxing, deleting or rewriting either
cross-check guard · touching any fourth test module to make the pins reconcile · re-freezing a digest for
any file other than `engine/progression_loop.py`.

**If reconciliation cannot be completed within those limits — for example if a guard stays red after a
correct mechanical re-freeze, or if a fourth file proves to pin the same digest — the implementation gate
must return**

    STOP — DIGEST-PIN RECONCILIATION EXCEEDS OWNER ALLOWANCE

**and must not widen the change to obtain green.** Disclosing an out-of-allowance edit does not authorize
it.

**Excluded, and not authorized by any reading of this contract:** `engine/semantic_registry.py` ·
`CAUSAL_SURFACES` · `SUBSTANCE_SURFACES` · Arabic normalization · `engine/gap_relevance.py` ·
`engine/intent_serving.py` · `_structured_technical_form` and the hyphen logic · `engine/scoring.py` ·
domain packs · **every pin except the single `engine/progression_loop.py` digest value in the three files
named in §5 item 4, under the exhaustive limits of §5.1** · the replay benchmark and golden fixtures ·
`web/` · the S2 instrument, its frozen corpus and all benchmark evidence. **If another surface is required, the implementation gate must STOP
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

### E. AMENDMENT 1 — GENUINE-CONDITIONAL FALSIFICATION HARDENING

19. `A-19` A **targeted deterministic falsification case** proves that a **genuine causal conditional
    remains recognised** after the correction. It must include, verbatim, the construction
    **`"if I can detect wheel slip, the controller turns on"`**, and must assert that
    `_has_causal_structure` returns **True** for it and that the answer still reaches the assessment it
    reaches at base. This case is chosen deliberately because it **shares the leading `"if I can"`
    wording with the measured preference clause** and therefore cannot be satisfied by a qualifier-list
    predicate; a mechanism that fails it **fails `A-8`**, and disclosure does not rescue it. The case must
    be written **independently of the frozen corpus** and must **not** depend on any other causal term —
    at base, `"if "` is its **sole** causal hit and `has_registered_causal_structure` is **False**
    `[EXEC]`. The exploratory qualifier-list mechanism recorded in §4 is **evidence only** and is
    **NOT** frozen as the required code solution.

### F. AMENDMENT 1 — DIGEST-PIN RE-FREEZE TRUTH

20. `A-20` `engine/progression_loop.py` is **frozen first**: the digest is re-frozen only after that
    file's final candidate bytes exist, never against an intermediate or anticipated state.
21. `A-21` The pinned value is **computed from the exact candidate bytes** of
    `engine/progression_loop.py` in the frozen candidate — not transcribed, adapted, or carried over.
22. `A-22` The **identical** value appears in **all three** files named in §5 item 4, and the returned
    evidence shows the computed digest alongside the three pinned values.
23. `A-23` Both cross-check guards are **run and green**:
    `tests/test_rvr7_render_edge_resolution.py::test_progression_loop_is_byte_unchanged_by_rvr7` and
    `tests/test_w2b_amc_consumers.py::test_exactly_three_p9_files_pin_the_current_digest`.
24. `A-24` **No superseded digest remains in any ACTIVE `engine/progression_loop.py` P9 pin location
    authorized by this amendment**, and all three active pin sites carry the **same** digest computed from
    the exact final candidate bytes of `engine/progression_loop.py`. A **repository-wide search for the
    superseded value must be returned as evidence**, and **every** remaining occurrence must be classified
    explicitly as exactly one of:

    - **`ACTIVE PIN — NOT ALLOWED`**, or
    - **`HISTORICAL / GOVERNANCE / EVIDENCE LINEAGE — ALLOWED TO REMAIN`**.

    **Historical governance and evidence documents are NOT to be edited merely because they accurately
    record the former digest.** Truthful historical records of the value that was pinned at the time they
    were written stay as written; erasing an old digest from history is a falsification of evidence, not a
    reconciliation. This applies to the pin-comment lineage inside the three authorized files as well —
    that lineage is `HISTORICAL / GOVERNANCE / EVIDENCE LINEAGE — ALLOWED TO REMAIN`, and only the
    **active** `_FROZEN_ENGINE_SHA256["engine/progression_loop.py"]` value is re-frozen.

    **If the superseded digest remains in an ACTIVE pin location outside the three files authorized in
    §5 item 4, the required return is**

        STOP — DIGEST-PIN RECONCILIATION EXCEEDS OWNER ALLOWANCE

    **— the allowed implementation surfaces are NOT broadened to reach it, and no historical governance or
    evidence document is edited to make the search come back empty.**
25. `A-25` The re-freeze is **not** presented as a P9 semantic change: no P9 signal, threshold, corpus,
    fixture or assertion changes, and the returned evidence states this from the diff, not from
    assertion.
26. `A-26` **The future digest is NOT pre-computed or invented at this governance gate.** At the
    Amendment 1 freeze the digest is unknown and must remain unknown; any document, comment or evidence
    line stating a post-correction digest before the correction exists is a **defect**, not a
    convenience.

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

**Amendment 1 lineage.** Amendment 1 is folded into this document in place rather than filed as a second
artifact, so that exactly one contract governs G-4-A and no reader can act on a superseded surface list.
The pre-amendment text of §5 and §6 is preserved as history in Git, not duplicated here. Amendment 1
carries the same lifecycle as the base contract: it becomes authoritative only through the sequence
above, and it **does not** resume the returned implementation START — that resumption is a further
separate Owner decision, and `IMPLEMENTATION AUTHORIZED: NO` is unchanged by this gate.

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
