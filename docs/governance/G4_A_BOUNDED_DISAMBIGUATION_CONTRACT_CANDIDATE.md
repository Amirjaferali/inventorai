# G-4-A — BOUNDED SEMANTIC / SYNTACTIC DISAMBIGUATION — CONTRACT (CANDIDATE)

**STATUS AT CREATION: `CONTRACT CANDIDATE — NOT AUTHORITATIVE`.** Created on the authoritative base
`b1c5b7b092091f50c8181253b1ed3b08b35a837e` (branch `feature/atomic-json-session-persistence`), verified
live from Git at this gate `[EXEC]`.

`IMPLEMENTATION AUTHORIZED: NO` · `IMPLEMENTATION STARTED: NO` · `MECHANISM PRE-SELECTED: NO` ·
`G-4 FULL CLOSURE: NOT ASSERTED` · `EXECUTABLE DELTA: 0`. This document is a contract freeze only; it
authorizes nothing and promises no solution.

## §1. Authority

Governed by the Owner decision **OD-G4-A2** (`OWNER_DECISION_REGISTER.md`), which accepts the
Lead-adjudicated `STOP — BOUNDED G-4-A CORRECTION REQUIRES OWNER DECISION` and authorizes
**contract design only**. It does not reopen `OD-G4-A`, `OD-G4-B`, G-4 ownership, the base G-4-A
contract, Amendment 1 or A-24. Those remain authoritative and this contract is subordinate to them:
where they are silent this contract governs the disambiguation question alone.

The Owner acceptance is explicitly **not** an assertion of universal algorithmic impossibility. It
records that the bounded solution space **under the base contract as written** has been sufficiently
exhausted for governance purposes.

## §2. Residual problem statement `[Q1]`

The measured English causal false positive is **not** a property of the `if`-clause **alone** — that is
proven, because the same tail carries opposite truth in different sentences. Beyond that, only the
**specific surface features and mechanisms actually tested in §3–§5 are falsified, and only where the
evidence supports it**. **No claim is made that every possible single surface feature has been
disproven**, and §4 records that a bounded feature conjunction is materially plausible again once
semantically ambiguous cases are removed from binding truth.

The unresolved ambiguity is exactly this: the identical English surface

    ... if I can avoid it

is **incidental** in the measured record — *"…I would rather not have a wire going to the brake lever
if I can avoid it"* — and **genuine** in constructions where the same tail conditions a system
response. `assess_response` must return different truths for the same tail.

`MEASURED [EXEC]` at this base: the `if`-tail of the measured record and of the same-surface genuine
contrast are **byte-identical** (`'i can avoid it.'`), and in every case in §7 `"if "` is the **sole**
English causal-table hit with `has_registered_causal_structure` **False**.

## §3. Evidence from the three rejected attempts (evidence only, never lineage)

| Candidate | Predicate | Falsified by `[EXEC]` |
|---|---|---|
| `88fe2e8c37bb9301b829dd2ba7f18f95320ecb4b` | no consequent **AND** preference matrix | genuine conditionals inside a preference matrix |
| `317da0ad9a69b9b81053b06fe9f2ea6f22f65183` | short clause ending in a pro-form | short pro-form conditions; `if so`; `if possible`; the length-only split of an equivalent pair |
| `87ec9f4860c735c73bbf0912c4eea2a9e8dd7c59` | first-person `avoid` + pro-form, prefix-matched | substantive continuation after the pro-form; the identical-tail contrast |

They are **evidence only**: not implementation authority, not lineage authority, not accepted design,
not permitted parents. They must not be amended, cherry-picked, merged from, or promoted.

## §4. Separability-audit implications

**The earlier conclusion is WITHDRAWN, and this is the material finding of the oracle-integrity gate.**
The prior text reported that an exhaustive conjunction search over **H** (bounded full-clause-anchored
avoidance tail), **P** (preference marker in the attaching clause), **C** (negative preference frame)
and **D** (first-person matrix subject) returned **NONE** that separates, because the measured record and
three adversarial genuine cases shared the vector `(T,T,T,T)` while requiring opposite results. That
conclusion was valid only if those opposite labels were valid binding truth. **They were not** — the
§7.0 semantic-oracle audit finds all three of those counterexamples **materially ambiguous**, so none of
them falsifies the conjunction.

**Re-run over binding oracles only `[EXEC]`.** With the ambiguous cases removed from binding truth, the
same exhaustive search over every conjunction in every polarity **separates the entire binding set**, and
does so through **eleven** distinct conjunctions:

    C · H AND P · H AND C · H AND D · P AND C · C AND D · H AND P AND C ·
    H AND P AND D · H AND C AND D · P AND C AND D · H AND P AND C AND D

Every binding required-`False` case carries `(H,P,C,D) = (T,T,T,T)`; the one binding required-`True` case
with `H = True` — case 21, whose matrix is a system-behaviour statement rather than a preference — carries
`(T,F,F,F)`.

**Reproducibility of the eleven `[EXEC]`.** The binding oracle set collapses to **four distinct
`(H,P,C,D)` vectors**, from which the count is recomputable directly from this contract:

| Binding cases | `(H,P,C,D)` | required |
|---|---|---|
| 1, 2, 3, 4, 5, 33 | `(T,T,T,T)` | **non-causal** |
| 6, 7, 8 · 13–20 · 22, 23 · 28, 29, 30 · 32 · 36, 37 | `(F,F,F,F)` | causal |
| 9, 10, 11, 12 | `(F,T,F,T)` | causal |
| 21 | `(T,F,F,F)` | causal |

A conjunction separates iff it fires on exactly the `(T,T,T,T)` row and on none of the other three.
Enumerating all 1-, 2-, 3- and 4-term conjunctions in both polarities over those four vectors yields
exactly the eleven listed above — no case label, binding status, feature definition, oracle or result is
changed by publishing this table; it is evidence transparency only.

**What this does and does not establish.**
* It **does** establish that `H ∧ P` and the related Level-1 structural conjunctions are
  **MATERIALLY PLAUSIBLE — NOT YET FALSIFIED**, and that they must **not** be excluded on the ground
  that the prior audit claimed they failed.
* It does **NOT** establish that any of them is correct. Separation over a finite binding set is
  **necessary, not sufficient**: a conjunction that separates today's oracles may still be falsified by
  a genuine case not yet written. `C` alone appears in the list and is obviously fragile on its face —
  its presence is reported because the search was exhaustive, **not** as a recommendation.
* It does **NOT** pre-select a mechanism, and no mechanism is authorized here.

**Consequence for the capability ordering.** Any admissible mechanism no longer must read information
outside that feature set. **Level 1 is not merely OPEN — it now carries at least one materially
plausible unfalsified mechanism family**, so under §5.1 the implementation gate must begin there and may
not advance until the enumeration and the verbatim zero-remaining statement are satisfied.

## §5. Minimum-capability analysis `[Q2]–[Q9]`

Evaluated in the Owner-mandated order. **No level is assumed; each finding is measured.**

### Level 1 — bounded local deterministic syntax `[Q3]`: **OPEN**
With the preceding sentence removed, the measured sentence and the adversarial sentence are identical on
**the explicitly tested dimensions and named measurements** — H, P, C, D, first-person matrix subject
`True`, `if`-clause subject `'i'`, `if`-tail `'i can avoid it.'`, negative preference frame `True`, sole
`"if "` route `True` `[EXEC]`. **Other intra-sentence differences exist and remain available for
Level-1 investigation** — the complement after `have` (possession `a wire going to the brake lever` vs
causative `the emergency brake activate`) is one of them, and this list is measured, not exhaustive. Both implementable proxies for that difference are
**dispositioned, each with its own exact status and evidence class**:

* The `-ing` participle test — status **`REJECTED AS INSUFFICIENT`**, evidence class **binding
  generalisation / paraphrase failure**: it corrects the measured record and case 33, but **fails four binding
  incidental cases — 2, 3, 4 and 5** — which contain no `have`-complement at all (*"…not run a wire to
  the lever…"*, *"…not fit a wire to the brake lever…"*), so the proxy leaves each of them causal
  `[EXEC]`. A rule that corrects the recorded wording but not its materially equivalent paraphrase does
  not satisfy §9.
* **The previously claimed genuine-causal false negative for this proxy is WITHDRAWN.** It rested on
  *"…would rather not have the emergency brake engaging if I can avoid it"*, which §7.0 adjudicates as
  materially ambiguous and §7.2 holds as the non-binding probe **P-31**. **A non-binding ambiguity probe
  cannot support a current falsification**, so that direction is no longer claimed. The proxy's
  rejection rests solely on the binding paraphrase failure above; **it is not asserted to be falsified
  "in both directions"**.
* A verb lexicon for the third proxy — status **`EXCLUDED`**, evidence class **governance / architecture
  exclusion** (a broad lexical family forbidden by §9), independent of any oracle and never tested
  against one. It is **not** `FALSIFIED`.

**Scope of this finding — binding, and corrected at the state-consistency gate.** **The prior
NO-SEPARATOR conclusion over H/P/C/D is WITHDRAWN, and the H/P/C/D conjunction lattice is NOT falsified
as a class** — its only counterexamples were the cases §7.0 found materially ambiguous, and §4's re-run
over binding oracles separates the whole binding set. **`H ∧ P` and the related Level-1 conjunction
family remain `MATERIALLY PLAUSIBLE — NOT YET FALSIFIED`** until a future IMPLEMENTATION gate tests them
against binding, semantically admissible evidence. No mechanism is selected here.

What remains validly **dispositioned** from the prior Level-1 work is only the mechanisms whose
disposition rests on **binding, semantically admissible** grounds — and each keeps its own exact status
and evidence class, which are **not** interchangeable:

* the tested `-ing` complement proxy — status **`REJECTED AS INSUFFICIENT`**, evidence class
  **generalisation / paraphrase failure** (binding incidental cases 2, 3, 4 and 5). It is **not**
  `FALSIFIED`. Its former genuine-causal false-negative claim rested on the non-binding probe P-31 and
  is **`WITHDRAWN`**; the rejection is **not** claimed "in both directions";
* the system-response lexical direction — status **`EXCLUDED`**, evidence class **governance /
  architecture exclusion** (§6 boundary, §9 open-ended lexicon), independent of any oracle. It is **not**
  `FALSIFIED` and was never tested against an oracle.

**No mechanism is retained on the falsified list merely because it was defeated before the ambiguous
oracles were removed.** **The Level-1 capability class is NOT claimed exhausted**, and the
implementation gate must begin here.

### Level 2 — bounded local context analysis `[Q4]`: **OPEN**
The repository's existing Layer-2 pattern (`_connective_whole_word_substance_gate`: connective **plus**
a whole-word domain substance signal in the supporting clause) is the natural in-architecture analogue
and was tested. `MEASURED [EXEC]`: the electronics_electrical substance list contains **neither**
`wire`, `brake` **nor** `controller`, and the measured matrix, the adversarial matrix and the
no-preference genuine matrix each contain **zero** substance signals. The gate is constant across cases
requiring opposite results, so it cannot separate them. Extending the signal list to make it separate
would be domain-pack expansion, forbidden by §9.

**Scope of this finding — binding.** What is measured insufficient is **that existing gate**. **The
Level-2 capability class is NOT claimed exhausted** — a different bounded local-context mechanism that
adds no signal, no pack entry and no open-ended lexicon remains admissible, and the implementation gate
must look for one before advancing.

### Level 3 — bounded reference / disambiguation logic `[Q5] [Q6]`: **CONDITIONAL — NOT PRE-SELECTED**
**Scoped evidence statement, not a conclusion.** For the specific preceding-sentence adversarial cases
tested, useful distinguishing evidence occurs in preceding context: with that sentence removed those
cases are structurally the measured hedge. **This does NOT establish that cross-sentence information is
necessary, that Level 3 is required, or that same-sentence and local structural information is
insufficient as a capability class.** **§7.1 case 37** — the binding same-sentence case, where the
antecedent sits inside the same sentence — is the binding guard against that premature conclusion
(case 35, its ambiguous predecessor, is now a **non-binding** §7.2 probe and guards nothing), and Levels 1 and 2 remain **OPEN**. One smallest
deterministic version of a Level-3 rule was constructed and remains **FALSIFIED — on binding evidence
substituted at the provenance gate**: a prior-sentence avoid-lemma cue (`can be avoided` / `can prevent`
/ `can avoid` / `avoidable`) requires an externally introduced avoidable antecedent before the
`if`-clause, and **no such lemma appears in binding genuine cases 21, 22, 32, 36 or 37**, so the cue
rejects **all five** `[EXEC]` — five genuine-causal false negatives, case 32 among them. **The evidence
originally cited for this falsification is WITHDRAWN**: it was *"The rider can steer around the pothole.
I would rather not have the emergency brake activate if I can avoid it."*, which carries the same
first-person negative-preference ambiguity as the §7.2 probes and is adjudicated **AMBIGUOUS —
NON-BINDING**; it is not used as an oracle and is not promoted to binding truth. The falsified status
survives on the binding cases alone. **Under the tested cue that withdrawn sentence would have returned
a non-causal (`False`) result `[EXEC]`; because its own causal truth is ambiguous, that result is NOT
binding false-negative evidence and no causal truth is assigned to the sentence here.**

**One falsified instance is not a proof that the level is empty**, and it is equally not evidence that
Level 3 is where the answer lies. This contract declines both inferences. Level 3 is **CONDITIONAL**: it
may be explored **only after** materially plausible Level-1 and Level-2 mechanisms have been falsified
against §7 by evidence. The observation that the adversarial cases depend on a preceding sentence is
recorded as an **observation, not a conclusion** — **§7.1 case 37**, the binding same-sentence guard,
exists precisely to test whether the discriminating information must be cross-sentence at all.

### Level 4 — broader semantic capability: NOT AUTHORIZED, NOT CONCLUDED
Nothing in this contract concludes that coreference resolution, POS/NLP infrastructure, semantic
parsing, LLM interpretation, embeddings, a new assessment engine, a second causal model, a second
language owner, a second semantic registry or general English understanding is required. If the
implementation gate establishes by measurement that one of them **is** materially necessary, that is a
finding to return, not a licence — see §11.

### §5.1 Capability-level progression rule — binding

| Level | State at this freeze |
|---|---|
| 1 — bounded local deterministic syntax | **OPEN, with at least one MATERIALLY PLAUSIBLE — NOT YET FALSIFIED mechanism family** (§4: `H ∧ P` and related conjunctions, once ambiguous cases are removed from binding truth). The `-ing` complement proxy is **REJECTED AS INSUFFICIENT** on binding generalisation evidence (incidental cases 2, 3, 4, 5); the system-response lexical direction is **EXCLUDED** by the architecture/governance boundary (§6, §9). Neither disposition exhausts the Level-1 capability class |
| 2 — bounded local context | **OPEN** — the existing Layer-2 substance route is measured insufficient; the class is **not** claimed exhausted |
| 3 — bounded reference / disambiguation | **CONDITIONAL — NOT PRE-SELECTED** — eligible only once the materially plausible lower-level mechanisms surfaced at the gate have been enumerated, tested or dispositioned and the level-exit statement `MATERIALLY PLAUSIBLE CURRENT-LEVEL MECHANISMS REMAINING: 0` has been made for Levels 1 and 2. That statement is **NOT** mathematical or universal capability exhaustion |
| 4 — broader semantic capability | **NOT AUTHORIZED / NOT CONCLUDED** |

**The implementation gate must always begin at the LOWEST surviving capability level.** Failure of a
single candidate mechanism does **not** authorize advancement. Before advancing from a capability level
the implementation return must:

1. **enumerate** the materially plausible mechanisms at that level surfaced by the current repository
   evidence, the prior falsifications recorded in §3 and §5, and the §7 matrix;
2. **identify which were tested**;
3. **identify the exact §7 falsification case** that rejected each tested mechanism;
4. **disposition any mechanism considered inadmissible**, stating why it falls outside this contract
   (§6 boundary, §9 anti-hardcoding, or §10 surfaces); and
5. **state, verbatim:**

       MATERIALLY PLAUSIBLE CURRENT-LEVEL MECHANISMS REMAINING: 0

Only then may the gate advance to the next capability level. If

    MATERIALLY PLAUSIBLE CURRENT-LEVEL MECHANISMS REMAINING > 0

the gate **remains at the current level** and must test what remains.

**What that statement does and does not claim.** It is **NOT** a claim of mathematical or universal
capability exhaustion, and no return may present it as one. It claims only that **no materially
plausible mechanism identified from the evidence available at that gate has been silently skipped in
order to move to a more complex capability level**. A later gate that surfaces a new materially
plausible mechanism at a lower level re-opens that level; the statement is a record of diligence at one
gate, not a permanent closure.

**A falsified proxy is not a falsified capability class.** No single failed candidate mechanism
constitutes level exhaustion. No return may infer the exhaustion of a level from the failure of specific
mechanisms within it, and no return may advance a level on the ground that a lower level "feels"
insufficient. This rule binds this contract's own §5 findings as much as any future one.

## §6. Architecture boundary `[Q7] [Q8] [Q9]`

**Available (bounded local deterministic structure).** Sentence and clause segmentation; token
sequences; anchored full-clause matching; literal markers; clause-scoped locality; and **bounded
local-context inspection sufficient to cover the binding §7 context positions**. **Reading the matrix,
or preceding context, is not by itself a new capability** — the rejected candidates already read the
matrix and their defect was overbreadth, not the reading.

**Local-context horizon — aligned with §7, and no wider.** The binding matrix requires correct
classification when the material antecedent sits in the **same sentence** (**case 37**), in the
**immediately preceding sentence** (**cases 21, 22, 32**), and with **one intervening sentence**
(**case 36**). Every case named here is a **binding, semantically admissible §7.1 oracle**; the
ambiguous §7.2 probes establish no context horizon.
The implementation may therefore inspect **the minimum bounded local context the binding matrix
requires**, and no more. This is **not** authorization for an unlimited history, a response-wide
semantic scan, or any materially broader context horizon: a broader horizon requires its own separate
justification at the gate that proposes it and **is not silently authorized by this wording**. The §7
context-position invariant continues to apply in full — **no arbitrary context-distance threshold may
create an A-8 false negative**, and a horizon widened until a case passes is tuning, not
justification.

**Not available (new semantic interpretation capability).** General POS/NLP infrastructure, parsing
architecture, semantic-model expansion, an open-ended lexicon of domain verbs or hazards, or general
language understanding. A mechanism is in this class when adding a new English paraphrase of the same
meaning would require adding a new entry to make it behave correctly.

**Word-class boundary — stated precisely, because the distinction matters.** A **general** POS tagger,
grammar or linguistic model is **NOT AUTHORIZED**. A **bounded deterministic local-form check** inside
the existing `progression_loop.py` seam is **NOT pre-forbidden merely because it concerns grammatical
form**, and **MAY REMAIN ELIGIBLE** when **all** of the following hold: it adds no new module or
subsystem · it performs no model inference · it uses no open-ended lexicon · it expands no domain pack ·
its behaviour is a pure deterministic property of the text · it survives the entire §7 matrix · and
materially equivalent paraphrases do **not** require adding entries to keep it correct. Such a mechanism
is **not pre-authorized** either: eligibility means it may be proposed, and it must then be falsified
like any other. The earlier `-ing` proxy failed §7, not this eligibility test — form-based mechanisms
are ruled out by evidence, never by the label.

**Implicit-semantic-upgrade test `[Q9]`.** A proposed mechanism is an implicit semantic upgrade —
forbidden by `./CLAUDE.md` line 246 — if it grants or withholds REASONED on the basis of a meaning
judgement the engine does not otherwise make anywhere, or if its behaviour cannot be stated as a
deterministic property of the text.

## §7. Mandatory adversarial falsification matrix

### §7.0 Semantic-oracle integrity — which cases may bind

A case may serve as a binding `CAUSAL` / `NON-CAUSAL` oracle **only if its own English is
unambiguous**. Every case whose classification turns on the referent of `it` / `this` / `that` / `them`
was re-read independently of its inherited label, asking one question: **would an ordinary competent
English reader have more than one materially plausible antecedent?** Anti-anchoring applies to prior
Lead and Creator labels alike — an inherited label is not evidence.

**Cases found AMBIGUOUS and REMOVED from binding truth** — each has a first-person negative-preference
matrix, so `it` may plausibly denote *either* the hazard named earlier *or* the matrix proposition
itself (the brake activating, the valve venting, the controller intervening). Under the second reading
each is an incidental preference hedge, not a condition → system-response relationship, so the case
cannot be a binding `CAUSAL` oracle: **24, 25, 26, 27, 31, 34, 35**.

**Cases confirmed UNAMBIGUOUS and retained as binding.** The incidental family (1–5, 33): `it` can only
denote the matrix object — having or fitting the wire — and no earlier noun is a plausible avoidance
target, so no competing reading exists. The genuine family (6–12, 13–20, 21–23, 28–30): either no
pro-form is involved, or the matrix is a **system-behaviour statement rather than a preference**, which
leaves the earlier-introduced entity as the only plausible antecedent (21: *"The assistance controller
stays inactive if I can avoid it"* — `it` = the collision risk), or an explicit continuation fixes the
referent (22, 23, 28, 29: *"…by steering manually"*, *"…through the bypass line"*, *"…under the cover"*).
**Case 30 is retained as binding on the first ground, not the second**: *"The controller selects the
secondary route if we may avoid that under the current limit."* has no referent-fixing continuation —
*"under the current limit"* qualifies the avoidance, it does not name what `that` denotes. It is binding
because **its matrix is a system-behaviour assertion rather than a first-person preference**, so
plausible variation in what `that` denotes does not produce a competing incidental preference-hedge
reading; whichever candidate referent is taken, the sentence still conditions a system action. **This
states no ambiguity policy** and creates none.

**NO AMBIGUITY POLICY IS CREATED HERE.** This contract does **not** decide that ambiguous English
conditionals count as causal or as non-causal, and it adopts no nearest-antecedent,
previous-sentence-antecedent, technical-antecedent or preference-matrix-antecedent rule. If truthful
implementation ultimately requires an ambiguity **policy** rather than a factual discriminator, the
implementation gate must return that as a **future Owner decision**, not adopt one.

### §7.1 Binding matrix

The implementation gate is bound to **all** of the following. Every case must be shown
**predicate-isolated** — `"if "` its only English table hit and `has_registered_causal_structure`
False — so no other route can mask a failure.

**Must be NON-CAUSAL (incidental family).**
1. The measured record `E-1|novice|en` `MECHANISM_COMPLETENESS[1]`.
2. `i would rather not run a wire to the lever if i can avoid it.`
3. `we would rather not run a wire to the lever if we can avoid it.`
4. `i would rather not run a wire if i can reasonably avoid having to do it.`
5. **A materially equivalent paraphrase of the measured meaning** — e.g. the measured record with
   *"not have a wire going to"* replaced by *"not fit a wire to"*. A rule that corrects the recorded
   wording but not its paraphrase does **not** satisfy this contract (§9).

**Must remain CAUSAL (genuine family).**
6. `if the wheel speed drops, the light turns on`
7. `if I can detect wheel slip, the controller turns on`
8. `the light turns on if the wheel speed drops` (post-posed, no consequent marker)
9. `I would prefer the controller to turn on if wheel slip occurs.`
10. `I would prefer the light to turn on if the wheel speed drops.`
11. `I would rather the backup pump activate if pressure drops.`
12. `I would prefer the controller to turn on if I can detect wheel slip.`
13. `An obstacle is present. The brake activates if the camera sees it.`
14. `Several objects are present. The doors close if the sensors detect them.`
15. `The prior diagnostic may pass. If so, the controller advances to the next stage.`
16. `Manual bypass is available. The relay switches if the operator selects this.`
17. `A fault state is available. The alarm sounds if the sensor reports that.`
18. `A start command is available. The backup pump starts if the controller commands it.`
19. `Backup power is available. The controller switches to the backup supply if possible.`
20. `The brake activates if the camera sees it.` **and** `The brake activates if the camera can
    reliably see it.` — and the two must be classified **identically**.
21. `A collision risk is present. The assistance controller stays inactive if I can avoid it.`
22. `A collision risk is present. The assistance controller stays inactive if I can safely avoid it
    using manual steering.`
23. `If I can avoid it using manual steering, the assistance controller stays inactive.`
24. **WITHDRAWN — MOVED TO §7.2** (ambiguous pro-form referent). Not a binding oracle.
25. **WITHDRAWN — MOVED TO §7.2** (ambiguous pro-form referent). Not a binding oracle.
26. **WITHDRAWN — MOVED TO §7.2** (ambiguous pro-form referent). Not a binding oracle.
27. **WITHDRAWN — MOVED TO §7.2** (ambiguous pro-form referent). Not a binding oracle.
28. `The valve remains closed if we can safely avoid having to vent it through the bypass line.`
29. `The cable stays in the upper channel if we can avoid having to bend it under the cover.`
30. `The controller selects the secondary route if we may avoid that under the current limit.`
31. **WITHDRAWN — MOVED TO §7.2** (ambiguous pro-form referent). Not a binding oracle, and **not
    evidence for any current falsification**: the genuine-causal false-negative claim it once supported
    against the `-ing` proxy is withdrawn in §5, which now rejects that proxy solely on the binding
    paraphrase failure. The participle-shaped risk it was written to cover is **not currently covered by
    any binding case**, and that gap is disclosed rather than papered over.
32. **A paraphrase of at least one preceding-context genuine case that removes every avoidance lemma
    from the antecedent/context sentence, while preserving the genuine conditional surface under test**
    — `The rider can steer around the pothole. The assistance controller stays inactive if I can avoid
    it by steering manually.` The prior wording of this case used a first-person negative-preference
    matrix and was therefore ambiguous; it is rebuilt on the unambiguous system-behaviour form.
    `SOLE-IF: True [EXEC]`.

**Must be NON-CAUSAL — shallow-context-cue guards (added at the contract-repair gate).**
33. `The design also includes a collision sensor. I would rather not have a wire going to the brake
    lever if I can avoid it.` — the measured incidental use with a **technical preceding-sentence
    distractor**. A mechanism must not conclude that `it` has an external causal antecedent merely
    because the preceding sentence carries technical or hazard language. `SOLE-IF: True [EXEC]`

**Must remain CAUSAL — antecedent-position guards (added at the contract-repair gate).**
34. **WITHDRAWN — moved to §7.2** (ambiguous pro-form referent).
35. **WITHDRAWN — moved to §7.2** (ambiguous pro-form referent).
36. `A collision risk is present. The road is wet. The assistance controller stays inactive if I can
    avoid it by steering manually.` — replaces case 34. The material antecedent sits **one sentence
    further back**; the matrix is a system-behaviour statement and `by steering manually` fixes the
    referent, so `it` can only denote the collision risk. `SOLE-IF: True [EXEC]`.
37. `With a collision risk present, the assistance controller stays inactive if I can avoid it by
    steering manually.` — replaces case 35. The antecedent is in the **same sentence**, so the contract
    does not freeze the conclusion that the discriminating information is necessarily cross-sentence.
    `SOLE-IF: True [EXEC]`.

    **Disclosed limitation of cases 36 and 37.** Both carry `H = False` (the tail has substantive
    continuation), so neither discriminates an `H`-based Level-1 mechanism — such a mechanism passes
    them trivially. They bind **context-using** mechanisms at Levels 2 and 3, which is the risk the
    context-position invariant exists to control. This is stated rather than left for a reviewer to
    discover, and no case was forced merely to preserve a count.

**Context-position invariance, binding.** Moving a truthful antecedent within the bounded local context
— same sentence, immediately preceding sentence, or one sentence earlier — **must not change the causal
classification** unless a real semantic or structural distinction justifies the change and that
distinction is stated and defended. **No arbitrary context-distance threshold may create an A-8 false
negative**, and a mechanism that passes **the binding one-intervening-sentence guard** only by tuning a
numeric window until that case passes has not satisfied this clause: the window must be justified, not
tuned. This clause is stated against the binding guard rather than a case number so it cannot go stale
if the matrix is renumbered.

**Same-surface contrast, binding.** Cases 1 and 21 carry a byte-identical `if`-tail and require
opposite results. **A mechanism that cannot distinguish them truthfully must NOT be authorized for
implementation**, and disclosure does not substitute for satisfying them.

### §7.2 AMBIGUITY PROBE — NON-BINDING CLASSIFICATION

The following are **NOT** pass/fail oracles and **must not** cause an implementation candidate to PASS
or FAIL. Each has more than one materially plausible reading, and the Owner has adopted no ambiguity
policy. The implementation return **must disclose**, for each: its classification, why, and **which
antecedent/reading it selected**. A disclosure obligation is all these carry.

P-24. `A collision can be avoided by manual steering. I would rather the assistance controller stay
      inactive if I can avoid it.`
P-25. `A collision can be avoided by steering. I would rather not have the emergency brake activate if
      I can avoid it.`
P-26. `Manual bypass can prevent venting. I would prefer not to have the valve vent if I can avoid it.`
P-27. `The driver can avoid the obstacle manually. I would rather not have the automatic brake
      intervene if I can avoid it.`
P-31. `A collision can be avoided by steering. I would rather not have the emergency brake engaging if
      I can avoid it.`
P-34. `A collision risk is present. The road is wet. I would rather not have the emergency brake
      activate if I can avoid it.`
P-35. `With a collision risk present, I would rather not have the emergency brake activate if I can
      avoid it.`

**The ambiguity in each:** `it` may denote the hazard named earlier, or the matrix proposition itself —
the brake activating, the valve venting, the controller intervening. Under the first reading the
sentence states a condition → system response; under the second it is an incidental preference hedge.
Both readings are ordinary English. **If a divergence between these probes and the binding matrix ever
becomes decisive for a mechanism's admissibility, the implementation gate must return that to the Owner
as an ambiguity-policy decision rather than resolve it.**

**Cross-language and pipeline invariants.** The Arabic member of the measured pair keeps its existing
result; `engine/semantic_registry.py` byte-unchanged; `CAUSAL_SURFACES` / `SUBSTANCE_SURFACES` gain no
member; `_structured_technical_form` and the hyphen handling byte-unchanged; `engine/gap_relevance.py`
byte-unchanged.

## §8. Ownership `[Q7]` `[§10]`

**Existing owner:** `engine/progression_loop.assess_response` and its causal-recognition seam. G-4
ownership stays **COMPOSITION ACROSS EXISTING OWNERS** as adjudicated at the G-4 direction gate; this
contract creates **no** new owner and needs none. **No-new-owner proof obligation:** the implementation
gate must show the change lives inside the existing seam, adds no second assessment model, no second
causal model, no second language owner, no second relevance owner and no second normalization owner.
**No-new-subsystem proof obligation:** no module is added whose purpose is language analysis.
**Deterministic-state impact:** none — the predicate is a pure function of the response text; no
session, ledger or replay state is read or written. **Language-boundary impact:** English-side only;
Arabic recognition is not widened, and the Arabic registry route is untouched.
**Assessment-pipeline impact:** confined to the `"if "` route into `_has_causal_structure`; REASONED
paths C and D and the weak-pattern and generic-verb-trap rejections are unchanged.

## §9. Anti-hardcoding safeguards

**Prohibited absolutely:** exact fixture identity checks · question-ID-specific behaviour ·
benchmark-row-specific behaviour · corpus-position-specific behaviour · whole-answer verbatim
exceptions · cosmetic replay parity · benchmark gaming · semantic masking. These mirror `./CLAUDE.md`
lines 238–247 (`hidden fallback logic`, `benchmark gaming`, `replay-only hacks`, `implicit semantic
upgrades`, `uncontrolled aliasing`), line 180 (`No replay cosmetics.`), line 202 and lines 206–212
(`artificial replay parity`, `semantic masking`).

**Generalisation requirement, and it is testable.** A proposed rule must behave identically on
materially equivalent paraphrases of the measured meaning — case 5 of §7 exists precisely to enforce
this. `MEASURED [EXEC]` at this base: a clause-verbatim exception scoped to the recorded sentence leaves
that paraphrase at `_has_causal_structure` **True** / `REASONED`, so it does not achieve the base
contract's §3 objective and is rejected on evidence, not on assertion.

**Narrow is not the same as hardcoded.** A bounded structural rule stated over English form, applying to
every text with that form, is admissible however few corpus records happen to exhibit it. A rule is
hardcoding when it is keyed to a record's identity or literal text rather than to a form. The
implementation gate must state which of the two its rule is, and prove it with the paraphrase case.

## §10. Surfaces, regression and evidence `[Q10] [Q11] [Q12] [Q13]`

**Allowed implementation surfaces (exhaustive).**
1. `engine/progression_loop.py` — the `"if "` route into `_has_causal_structure`, plus bounded private
   helper functions in the same module if required. `_CAUSAL_STRUCTURE_PATTERNS` may be amended only if
   the correction genuinely requires it.
2. `tests/test_causal_connective_substance_gate.py` — only if the frozen table expectation genuinely
   must change.
3. One bounded new G-4-A test file.
4. `tests/test_p9_mech_i3_signal_quality.py`, `tests/test_p9_mech_i4_boundary_corpus.py`,
   `tests/test_p9_mech_i5_question_sufficiency.py` — **mechanical `engine/progression_loop.py` digest
   re-freeze only**, under the Amendment 1 §5.1 limits, unchanged by this contract.

**Forbidden surfaces.** `engine/semantic_registry.py` · `CAUSAL_SURFACES` · `SUBSTANCE_SURFACES` ·
Arabic normalization · `engine/gap_relevance.py` · `engine/intent_serving.py` ·
`_structured_technical_form` and hyphen handling · `engine/scoring.py` · domain packs · every pin except
the one `engine/progression_loop.py` digest in the three files above · the replay benchmark and golden
fixtures · `web/` · the S2 instrument, its frozen corpus and all benchmark evidence · every governance
and evidence document. **Governance documents must not be edited to narrate an implementation.**

**Digest-pin and A-24 implications.** Unchanged from Amendment 1: finalize `engine/progression_loop.py`
first, hash those exact bytes, write the identical value into the three ACTIVE pins, run both
cross-check guards green, record lineage against the **authoritative base** digest
`a7e8bd62b9ab76aaba5889ce52b5f32ee646b2817ba1c790ed7a231d259fa41f`, never record a rejected candidate's
digest as an intermediate event, and repeat the A-24 repository-wide classification with every
occurrence labelled `ACTIVE PIN — NOT ALLOWED` or `HISTORICAL / GOVERNANCE / EVIDENCE LINEAGE — ALLOWED
TO REMAIN`. Truthful historical records are never edited to empty the search.

**Materially exposed regression surfaces `[Q12]`.** The English causal route feeds `assess_response`
REASONED paths A/B and `_is_generic_verb_trap`; downstream, gap satisfaction and progression closure.
The RVR-3 pins are the sensitive boundary: `test_expert_mechanism_closure_answers_reach_reasoned_en_and_ar`
(EN **and** AR), `test_expert_feasibility_and_boundary_answers_reach_reasoned_en` (EN only),
`test_novice_answers_do_not_regress` (`novice|en` `[0]`, fires on `"when "`).

**Required regression evidence.** *Focused tier:* the new G-4-A tests, the causal-connective/substance
gate, the RVR-3 structured-substance module including the three named pins, both digest guards and the
pin-count cross-check. *Broad tier:* the assessment/progression/causal/substance/gap modules.
*Full tier:* the entire repository suite, with exact `passed / failed / skipped / xfailed /
xpassed / error` counts. Any failure claimed pre-existing must be demonstrated at the exact
authoritative base with a clean tree. **No blanket "green" without counts.** RED must be demonstrated at
the authoritative base **and** against each rejected candidate whose defect the new mechanism repairs.

**Determinism and independent falsifiability `[Q13]`.** The predicate must be a pure function of the
response text, free of randomness, clocks, network, model inference and session state, and reproducible
by a third party from the returned evidence alone.

## §11. STOP conditions `[Q14]`

The implementation gate must return, exactly and without proceeding:

- `STOP — G-4-A REQUIRES BROADER ARCHITECTURAL OWNER DECISION` — if satisfying §7 materially requires
  coreference implementation, POS/NLP infrastructure, semantic parsing, LLM or embedding inference, a
  new assessment engine, a second causal model, a second language owner, a second semantic registry,
  domain-pack expansion, or general English understanding. **This finding is to be returned, never
  acted on.**
- `STOP — BOUNDED G-4-A CORRECTION REQUIRES OWNER DECISION` — if no mechanism within §10 satisfies §7
  and the blocker is not architectural in the sense above.
- `STOP — IMPLEMENTATION REQUIRES OUT-OF-CONTRACT SURFACE` — if a surface outside §10 is required.
- `STOP — DIGEST-PIN RECONCILIATION EXCEEDS OWNER ALLOWANCE` — per Amendment 1 §5.1.
- `STOP — AUTHORITATIVE BASE ADVANCED` — if the live tip differs from the expected base.

**A fourth semantic approximation must not be produced to avoid a STOP**, and a disclosed
genuine-causal false negative never satisfies §7.

## §12. Product-value justification `[§10]`

Arabic is an Owner-decided **Substantive Supported Experience**. The measured defect means the same
meaning can earn progression in English and be withheld in Arabic — a parity failure on the product's
own promise, not a benchmark artifact. The correction's value is that an inventor's answer is judged on
what it says, in either language. That value is destroyed, not served, by a rule that turns the recorded
sentence green while leaving its paraphrase over-credited: **product truth over replay greenness**.
Equally, a correction that silences genuine conditionals would withhold progression from inventors who
did explain their mechanism — a worse product outcome than the defect being repaired. This is why §7 is
two-sided and why no disclosure clause can excuse a false negative.

## §13. Creator Grill obligations at the implementation gate

The implementation gate must answer, with evidence, at minimum: can the measured false positive still
pass · can its paraphrase still pass · is any genuine case in §7 newly rejected · is the same-surface
contrast (1 vs 21) satisfied and how · is the rule keyed to form or to a record's text · was any
rejected candidate's mechanism reused · was Arabic widened · was Mechanism B or M-1 touched · were the
three P9 files changed mechanically only · did any other pin change · did any superseded digest remain
in an ACTIVE pin · were historical records rewritten · was an out-of-contract surface required · was any
S2 or benchmark run performed · is G-4 full closure asserted.

## §14. Lifecycle and non-authorization — TWO DISTINCT INDEPENDENT REVIEWS

**These are different gates and must never be conflated.**

### §14.1 Contract lifecycle — the gate this document is in

`Lead Review` → `Independent CONTRACT Review` → `Lead re-adjudication` → `Owner exact-SHA acceptance` →
`publication` → `PR` → `separate merge authorization` → `CREATE A MERGE COMMIT` → `post-merge identity
verification`.

**Independent CONTRACT Review evaluates, and only this:** candidate identity · sole parent, tree and
bundle · the exact governance changed paths · `EXECUTABLE DELTA = 0` · faithful recording of the Owner
decisions · absence of authorization leakage · the truth of the residual problem statement · the
minimum-capability ordering and the §5.1 progression rule · the architecture boundaries including the
word-class boundary · the sufficiency of the §7 falsification matrix · the anti-hardcoding safeguards ·
the allowed and forbidden implementation surfaces · the STOP conditions · lifecycle correctness.

**Independent CONTRACT Review MUST NOT require** implementation test results, RED evidence,
implementation digests, P9 re-freeze evidence, regression counts or an implementation Creator Grill —
**no implementation exists at this gate**, and demanding them would be a category error. The §13
obligations are obligations placed **on a future gate**, not evidence owed at this one.

### §14.2 Implementation lifecycle — a separate, later gate

Only **after** this contract is authoritative **and** after a separate Owner decision
**`G-4-A IMPLEMENTATION START: YES`** may an implementation candidate be created. That candidate then
follows: `Creator implementation` → `Lead Delta Review` → `Independent IMPLEMENTATION Review` →
`Lead re-adjudication` → `Owner exact-SHA acceptance` → `publication` → `PR` → `separate merge
authorization` → `post-merge identity verification`.

**Independent IMPLEMENTATION Review is the stage that requires:** the full §7 binding matrix executed,
with predicate isolation shown per case · RED evidence at the authoritative base and against each
rejected candidate the mechanism repairs · the focused, broad and full regression tiers with exact
counts · the digest, P9 and A-24 evidence · the §13 implementation Creator Grill · the exact changed
executable paths · the implementation bundle identity.

**Neither review may be substituted for the other**, and passing §14.1 grants no implementation
authority whatsoever.

**Fences unchanged by this contract:** `G-4: OPEN / FRB` · `G-4 FULL CLOSURE: NOT ASSERTED` ·
`G-4-B / MECHANISM B: OPEN / DEFERRED, CODE CHANGE NOT AUTHORIZED` · `M-1: SEPARATE, NOT AUTHORIZED` ·
`T1-A′: OPEN` · `RVR-3 / RVR-7: NOT REOPENED` · `ARABIC WIDENING: NOT AUTHORIZED` ·
`SEMANTIC REGISTRY / DOMAIN PACK EXPANSION: NOT AUTHORIZED` · `THIRD S2 RUN: CONSUMED` ·
`FOURTH S2 RUN / RUN-004: NOT AUTHORIZED` · `FURTHER SUPPLEMENTAL SLICE EXECUTION: NOT AUTHORIZED` ·
`FDC-001 LANE: INACTIVE` · `DECISION WORKSPACE / PATH-T: NOT ACTIVATED` · `ODS-001: NOT ACTIVATED` ·
`RVR-4: CLOSED` · `HICR PHASE 2: NOT AUTHORIZED` · `READINESS IMPLEMENTATION: NOT AUTHORIZED` ·
`CAP ACTIVATION: NONE` · `FCORA: NOT AUTHORIZED` · `PSRR GO: NO` · `ACTIVE CONTRACT: NONE` (untouched) ·
`SERIOUS RELEASE / PRODUCTION / PAID ACTIVATION: NOT AUTHORIZED` · `main` NOT RECONCILED.

**Lean classification.** `LEAN RISK LEVEL: 2` · `REVIEW DEPTH: 2` — governance-only contract freeze,
zero executable delta.
