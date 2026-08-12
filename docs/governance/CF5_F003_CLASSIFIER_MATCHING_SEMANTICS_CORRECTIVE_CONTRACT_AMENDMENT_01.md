# CF5-F003 — Classifier Matching Semantics — Corrective Contract — AMENDMENT 01 (Same-Domain Containment Preservation) — Candidate

**Status of THIS record:** governance/documentation-only **CONTRACT AMENDMENT CANDIDATE**. It amends the already-authoritative
`docs/governance/CF5_F003_CLASSIFIER_MATCHING_SEMANTICS_CORRECTIVE_CONTRACT.md` (merged PR #448). It becomes AUTHORITATIVE only if
this exact accepted candidate is independently reviewed (Mandatory Grill → independent external exact-candidate review),
Owner-accepted, published SHA-preserving, merged (create-a-merge-commit), and post-merge verified. **Until then it authorizes
nothing.** **It implements NOTHING** — no runtime, no test, no behavior change in this gate. **It does NOT close CF5-F003 or CF-5,
does NOT modify P9-E2 tie policy, and selects/qualifies/activates no domain.** **GOVERNANCE-ONLY CONTRACT GATE.** Expected engine /
web / CLI / domains / schemas / persistence / API / architecture-guardrail / test diff in THIS gate: **ZERO**.

**Revision note (this candidate supersedes TWO rejected earlier amendment drafts).**
- Draft `0f48df20f121f70f6edbfe2b94a14b7a593b77d4` — **REJECTED** (blocking finding **A3-OVER-CREDIT / CONTAINMENT DOUBLE-COUNT**):
  §A3 stated the containment addition as an unqualified score increment, double-counting a contained signal that also appears
  standalone.
- Draft `5ebc927d46bd2d954a18ca71cd6eb558663811d6` — **REJECTED by Independent External Review** (blocking findings **M1
  plural-container containment loss** and **M2 over-broad normative score invariant**): its §A3 fired the containment credit only when
  an input token EXACTLY equalled the container signal `Y`, so a container matched through the already-authorized bounded plural
  (`applications` matching `application` via `+s`) did NOT trigger containment preservation and the classification flipped to
  Electronics; and it asserted a global invariant ("a domain's Design-A score never exceeds the historical parent score on any
  input") that is FALSE because authorized phrase/tokenization recognition legitimately produces new matches parent raw-substring
  matching did not.

Both `0f48df20` and `5ebc927d` are immutable rejected evidence (NOT published / NOT merged / NOT reused; retained in history; NEITHER
an ancestor of this candidate). This candidate corrects §A3 so containment preservation fires when the registered container `Y` is
matched through **any authorized base form (exact `Y`, `Y+"s"`, `Y+"es"`, or — for a multi-word signal — its authorized token
sequence with bounded final-token plural)**, keeping at-most-once / set-membership credit, and **replaces the over-broad global
invariant with the narrow, true containment-credit invariant** (§A3a).

**Authoritative base:** `cfdc58cc798d02b8d9f50030b627a8302e0de889` (PR #448 — CF5-F003 corrective contract v2 merge), verified
read-only; boot OK; `activated_domains() == ['electronics_electrical']`; 0 newer. The rejected implementation candidate
`a29789a948829133812d1a80b297e9b5b907cdc1` and the rejected amendment drafts `0f48df20` / `5ebc927d` are NOT ancestors.

---

## §A1. Why this amendment (blocking finding)

The CF5-F003 corrective contract mandated whole-token matching with bounded `+s`/`+es` plural. An implementation candidate
`a29789a9` faithfully implemented it and passed the Creator Grill (PASS WITH NON-BLOCKING HARDENING), but **Independent External
Review REJECTED it — MATERIAL CORRECTION REQUIRED**. Blocking finding: **CONTAINMENT-LOSS TIE FLIPS.** Whole-token matching removes
**same-domain containment score contributions** (a shorter registered signal contained inside a larger registered signal token no
longer scores), which drops a domain's score and lets the unchanged activated-domain tie precedence flip the result to Electronics.
Verified regression (real classifier):

| Input | Parent (substring) | Whole-token (rejected `a29789a9`) | Cause |
|---|---|---|---|
| `an implantable sensor` | `medical_device` | **`SINGLE(electronics_electrical)`** | medical loses `implant`⊂`implantable` reinforcement → medical(1)=electronics(1) tie → activated precedence gives Electronics |
| `an application with a sensor` | `software` | **`SINGLE(electronics_electrical)`** | software loses `app`⊂`application` reinforcement → tie → Electronics |

Downstream, real CLI then prints an untruthful `Domain inferred: electronics_electrical`. This is a **contract-level** conflict
between (1) eliminating arbitrary in-word substring matches and (2) preserving currently-correct classifications. This amendment
resolves it at the **matching/scoring boundary only** — it does NOT reopen P9-E2 tie precedence, AMBIGUOUS_TIE semantics, D4, or
MULTI.

## §A2. Complete signal-to-signal containment inventory (mechanically re-enumerated, tip `cfdc58cc`)

The full registered-signal containment graph (shorter registered signal `X` is a raw substring of a larger registered signal `Y`)
was re-enumerated mechanically over the entire registry. There are exactly **5** pairs; no additional relation exists after plural
normalization or phrase tokenization (plural/phrase forms are input-matching concerns and add no new signal-to-signal substring
relation), and there is **no chained containment** (no signal is both a contained signal and a container) and **no signal contained
in more than one registered container**:

| X (domain) | ⊂ Y (domain) | Relation | Whole-token score consequence | Final classification effect | Disposition |
|---|---|---|---|---|---|
| `implant` (medical) | `implantable` (medical) | **SAME** | medical loses `implant` when token is `implantable`/`implantables` | **REGRESSION** (`implantable sensor` flips to Electronics) | PRESERVE (§A3) |
| `app` (software) | `application` (software) | **SAME** | software loses `app` when token is `application`/`applications` | **REGRESSION** (`application`+electronics token flips to Electronics) | PRESERVE (§A3) |
| `monitoring` (medical) | `patient_monitoring` (medical) | **SAME** | none in practice — `monitoring` is its own token in normal text; `patient_monitoring` is a multi-word signal | NEUTRAL (no reachable loss) | preserved by the general rule; no reachable change |
| `sensor` (electronics) | `biosensor` (medical) | **CROSS** | electronics loses `sensor` when token is `biosensor`/`biosensors` | **IMPROVEMENT** — `biosensor` correctly classifies medical (parent misclassified it Electronics via sensor leakage) | do NOT restore (cross-domain) |
| `neural` (medical) | `neural network` (software) | **CROSS** | none — `neural` is a whole token in `neural network`, still scores medical; the phrase scores software | NEUTRAL | do NOT restore |

**Material regressions to correct: exactly the 2 SAME-domain families** `implant`/`implantable` (medical) and `app`/`application`
(software), **including their bounded-plural container forms** `implantables` / `applications`. The CROSS-domain `sensor`/`biosensor`
loss is an intended improvement and MUST NOT be restored.

## §A3. Amended matching semantics — bounded same-domain registered-signal containment preservation, AT-MOST-ONCE, plural-container aware (Design A)

The whole-token + bounded-plural rule of the base contract §4 is RETAINED unchanged. The containment addition is defined as a
**set-membership (at-most-once) presence rule** keyed on the container being present through ANY authorized base form:

> **Same-domain registered-signal containment (at-most-once / set membership; plural-container aware).** For each domain `D`, define
> the set `present(D)` of registered signals of `D` that are *present* in the input as the UNION of:
> - **(i) base matches** — every registered signal of `D` matched by the base whole-token + bounded-`+s`/`+es` rule (single-word
>   signals via exact / `+s` / `+es`; multi-word signals via a contiguous token subsequence with bounded plural on the final token);
>   and
> - **(ii) same-domain containment** — every single-word registered signal `X` of `D` such that some registered container signal `Y`
>   of the **same domain `D`** is a base match (i.e. `Y ∈ present(D)` via (i), through ANY authorized base form of `Y`: exact `Y`,
>   `Y+"s"`, `Y+"es"`, or a multi-word `Y`'s authorized token sequence), with `X != Y` and `X` a substring of the registered signal
>   string `Y`.
>
> The domain score is `len(present(D))` — each registered signal is counted **AT MOST ONCE**. A signal already present via (i) is
> **NOT** credited a second time via (ii); (ii) contributes only signals not already in `present(D)`. No containment other than
> same-domain registered-signal containment is credited: the container `Y` must be a **registered** signal; the contained `X` must be
> a **registered same-domain single-word** signal that is a substring of `Y`; **no cross-domain containment** and **no containment
> inside a non-registered word** is ever credited.

**Plural-container coverage (M1).** Because the container trigger is `Y ∈ present(D)` — i.e. `Y` matched through any authorized base
form, not exact-token equality — a container matched via the already-authorized bounded plural preserves containment identically to
its singular. Verified this gate: `applications with a sensor` → **software**, `implantables in a sensor` → **medical_device**,
`applications controlling a circuit` → **software**, `medical implantables with a circuit` → **medical_device** (all previously
flipped to Electronics under the exact-token-only draft `5ebc927d`).

### §A3a. Containment-credit invariant (replaces the rejected global invariant) (M2)

The rejected draft `5ebc927d` asserted an **over-broad global invariant**: "a domain's Design-A score never exceeds the historical
parent score on any input." **That claim is FALSE and is withdrawn.** The base contract's retained phrase/tokenization semantics
intentionally recognize some inputs parent raw-substring matching did not (e.g. a punctuation- or underscore-separated multi-word
signal such as `drug delivery` in `drug-delivery`, or `clinical_trial` in `clinical trial`), so the **complete classifier score MAY
legitimately exceed the historical parent score** on such inputs. The narrow, true invariant governs only the **containment
contribution** of a registered signal:

A registered signal's **containment contribution**:
1. is **set-based / at-most-once** — it adds a signal to `present(D)` only if not already present;
2. **cannot duplicate an already-earned base contribution** (a standalone base match of the same signal);
3. **cannot be granted cross-domain** — container and contained signal are the same domain `D`;
4. **cannot arise from a non-registered containing word** — the container `Y` must be a registered signal;
5. **cannot exceed the historical boolean contribution the same registered signal could have supplied through parent substring
   matching** — a contained `X` credited via (ii) is a substring of a present registered container `Y`, hence a substring of the
   input, so parent raw-substring matching would itself have contributed `X` exactly once; the credit reproduces (never exceeds) that
   single boolean contribution.

This invariant is scoped **specifically to containment preservation**; it makes **no** claim about the global classifier score,
which authorized phrase/tokenization recognition may legitimately raise above parent.

**Determinism / boundedness:** the rule is exact and total — it consults only the registered signal set, the authorized base-form
match, and exact substring containment; no stemming, fuzzy, edit-distance, or arbitrary substring. It is **domain-neutral and
N-domain capable** (general over any same-domain registered-signal containment; no per-domain branching; no hardcoded pair list).
**P9-E2 tie precedence, AMBIGUOUS_TIE, the priority fallback, `DomainClassification` semantics, the legacy fail-loud wrapper, and
D3-D are UNCHANGED.**

**Forbidden readings (each verified to produce a wrong result, must be caught — §A9).**
- *Exact-token-only container match* (rejected `5ebc927d`): drops plural-container preservation → `applications with a sensor` flips
  to Electronics.
- *Non-idempotent score increment* (rejected `0f48df20`): double-counts a contained signal that also appears standalone → `an implant
  that is implantable in a sensor circuit` inflates medical to 3 and flips electronics→medical.

## §A4. Compound boundary (§11) — re-classification (unchanged by this amendment; recorded)

Words that CONTAIN a registered signal but are themselves **NOT registered signals** are NOT preserved by §A3:

- `website` / `webcam` / `webinar` (contain `web`, software), `gearbox` (contains `gear`, mechanical) → **arbitrary compounds /
  potential Domain-Pack vocabulary gaps.** The base contract §4 acceptance boundary already scopes these out; recognizing them, if
  desired, is a **separate governed Domain-Pack signal-data decision**, NOT this matching-semantics gate.
- `subsystem` / `ecosystem` (contain `system`, software) → **arbitrary compounds** whose loss is desirable (they are not
  software ideas). Correctly not preserved.

Only **registered-signal same-domain containment** (the two families in §A2) is preserved; Domain-Pack enhancement remains separate.

## §A5. Owner-policy determination

Design A is a **purely technical preservation rule** — it preserves currently-correct classifications (`implantable sensor` →
medical; `application`+sensor → software), including their bounded-plural container forms, that the base whole-token rule
accidentally regressed, and (via §A3a) introduces no containment credit in excess of the historical substring contribution of the
same signal. It introduces **no new product policy** (it does not newly route medical/software ideas to Electronics; it prevents an
accidental such routing, and does not newly route Electronics ideas to medical/software either). **No Owner product-policy decision
is required; `OWNER_DECISION_REGISTER.md` remains UNCHANGED.** (Had the chosen remedy instead ACCEPTED the classification change —
e.g. "implantable ideas may route to Electronics" — that WOULD require an explicit Owner decision; it is explicitly rejected here.)

## §A6. Required preservation evidence (the future implementation MUST add, GREEN)

Singular-container same-domain preservation:

- `an implantable sensor` → **medical_device**; `an implantable circuit` → **medical_device**; `an implantable PCB` →
  **medical_device**;
- `an application with a sensor` → **software**; `an application controlling a circuit` → **software**;
- `a biosensor` → **medical_device** with **no** Electronics `sensor` leakage (cross-domain containment NOT restored);
- `an implantable device` / `an application` singular → their domain (unchanged).

**Plural-container preservation evidence (M1; MANDATORY GREEN).** Containment preservation MUST fire when the container is matched via
the authorized bounded plural:

- `applications with a sensor` → **software**; `applications controlling a circuit` → **software**;
- `implantables in a sensor` → **medical_device**; `implantables with a circuit` → **medical_device**;
- `medical implantables with a circuit` → **medical_device**;
- `biosensors` → **medical_device** with no Electronics leakage (cross-domain plural container NOT restored).

**At-most-once parity evidence (anti-double-count; MANDATORY GREEN).** When the contained signal ALSO appears as its own standalone
token, the domain score MUST equal the parent (substring) score — the classification MUST match parent and MUST NOT flip to the
contained domain — for singular AND plural forms:

- `an implant that is implantable in a sensor circuit` → **electronics_electrical** (medical scores **2**, not 3);
- `implants implantables sensors circuits` → **electronics_electrical** (medical **2**);
- `an application app controlling a circuit sensor` → **electronics_electrical** (software scores **2**, not 3);
- `apps applications sensors circuits` → **electronics_electrical** (software **2**).

## §A7. Original CF5-F003 corrections MUST remain RED-before / GREEN-after (unchanged)

`controlled`↛`led`, `compiled`↛`led`, `patriotic`↛`iot`, `concurrent`↛`current`, `hearth`↛`heart` remain corrected. **No
containment rule may recreate any of these** (guaranteed by §A3's registered-signal requirement). The real Web `/start` and real
CLI RED reproductions of the base contract §6 remain required.

## §A8. Test-evidence corrections (base contract §7 strengthened)

The rejected implementation's test suite **overstated 0/1/2/3+ activation coverage** (the 0-activated scenario was asserted but the
double was not actually exercised as an independent case). The amended requirement: the implementation MUST provide **genuinely
executed** evidence for **0, 1, 2, and 3+** activated-relevant-domain scenarios via self-restoring `_ACTIVATED_DOMAINS` doubles,
each an independent assertion (no narrative-only claim). Web tests MUST clean up any created session state (no persistent
`SESSION_STORE` leakage). The singular- and plural-container containment GREEN cases (§A6), the at-most-once parity cases (§A6), and
the original REDs (§A7) are mandatory.

## §A9. Mutation evidence (base contract §8 extended)

In addition to the base probes, the mutation plan MUST catch: (a) removal of same-domain containment preservation (an
`implantable sensor` → Electronics regression returns); (b) an over-broad containment rule that credits **cross-domain** containment
(a `biosensor` → Electronics leakage returns); (c) an over-broad containment rule that credits containment inside a **non-registered
word** (a `controlled` → `led` false positive returns); (d) a NON-idempotent (score-increment) containment credit that double-counts
a contained signal already present as a standalone token (the at-most-once parity cases regress: `an implant that is implantable in a
sensor circuit` flips electronics→medical); **(e) an EXACT-TOKEN-ONLY container match that ignores the authorized bounded plural of
the container — the plural-container cases regress (`applications with a sensor` flips software→electronics; `implantables in a
sensor` flips medical→electronics).** Each CAUGHT RED, bytecode-isolated, bytes restored.

## §A10. Scope (unchanged fence)

Implementation scope remains `engine/domain_rules.py` (matching/scoring only) + focused tests. **Forbidden:** P9-E2 tie-precedence
change; Web admission redesign (CF5-F002/CF-6); safety-signal redesign (CF5-F001); fallback-priority change (CF5-F004); domain
activation/selection/registration; D4; D8; **Domain-Pack signal-data edits** (Design A needs none — it consults the existing
registered signal set); persistence; MULTI production. If a production file beyond `engine/domain_rules.py` becomes mechanically
required, the implementation gate STOPs before expanding scope.

## §A10a. Underscore-signal reviewer observation — INDEPENDENTLY DISPROVED (recorded)

An Independent Reviewer observed that underscore signals such as `clinical_trial` / `patient_monitoring` "become unmatchable under
whole-token semantics." This was **mechanically verified against the normative specification and the reference matcher and found
INCORRECT.** The authoritative base contract §4 applies the SAME `[a-z0-9]+` tokenizer to BOTH input and registered signal, so
`clinical_trial` tokenizes to `['clinical','trial']` and `patient_monitoring` to `['patient','monitoring']`, matched as contiguous
token subsequences of inputs `clinical trial` / `patient monitoring`. Verified: `clinical trial` → **medical_device** (matched);
`patient monitoring` → **medical_device** (matched). These signals are therefore **MORE** matchable under tokenization than under
parent raw-substring matching (which required the literal underscore), not unmatchable. The observation is recorded as
**independently disproved; the contract is NOT modified to accommodate it.**

## §A11. Governance history (recorded truthfully; nothing erased)

- CF5-F003 corrective contract **v2 AUTHORITATIVE** via **PR #448** (merge `cfdc58cc`; accepted candidate `be27037c`).
- Implementation candidate **`a29789a9`** created (whole-token + bounded plural); **Creator Grill: PASS WITH NON-BLOCKING
  HARDENING**; **Independent External Review: REJECT — MATERIAL CORRECTION REQUIRED**; blocking finding **CONTAINMENT-LOSS TIE
  FLIPS**. `a29789a9` remains **immutable rejected evidence — NOT published / NOT merged / NOT reused**; retained in history.
- Amendment draft **`0f48df20`** created (Design A, §A3 worded as an unqualified score increment); **Mandatory Grill (Creator
  self-review): REJECT — MATERIAL CORRECTION REQUIRED**; blocking finding **A3-OVER-CREDIT / CONTAINMENT DOUBLE-COUNT**. Immutable
  rejected evidence; NOT an ancestor.
- Amendment draft **`5ebc927d`** created (at-most-once, but §A3 container trigger keyed on EXACT-token equality and asserting an
  over-broad global score invariant); **Independent External Review: REJECT — MATERIAL CORRECTION REQUIRED**; blocking findings
  **M1 plural-container containment loss** (`applications with a sensor` → Electronics because a plural-matched container did not fire
  containment) and **M2 over-broad normative score invariant** (the global "never exceeds parent" claim is false under authorized
  phrase/tokenization recognition). Immutable rejected evidence; NOT an ancestor. **This candidate corrects §A3 to trigger on any
  authorized container base form (incl. bounded plural), adds §A3a (narrow containment-credit invariant), §A6 plural-container +
  at-most-once evidence, §A9 probe (e), and §A10a underscore disproof.**
- This amendment corrects the **contract**, not by amending `a29789a9` / `0f48df20` / `5ebc927d`. A fresh implementation candidate
  against §A3 will be a separate later gate.
- **CF5-F003 remains VALIDATED D / OPEN; CF5-F001 / CF5-F002 / CF5-F004 remain open C; CF-5 remains OPEN; first new-domain
  activation remains BLOCKED;** `activated_domains() == ['electronics_electrical']`.

## §A12. Governance scope of THIS amendment candidate

Governance/documentation only: this NEW amendment record + `ACTIVE_EXECUTION_ROADMAP.md` (append-only) +
`ACTIVE_INCREMENT_CONTRACT.md` + `CURRENT_PROJECT_STATE.md` current-truth sync. **`OWNER_DECISION_REGISTER.md` UNCHANGED** (technical
preservation rule; no new Owner product-policy decision — D3 / P9-QS / P9-E1 / CF-5 candidate precedent). ZERO runtime / engine /
test / domain / schema / persistence / API / web / CLI / architecture-guardrail diff.

## §A13. Candidate state & next gate

**CF5-F003 = OPEN; this amendment = AUTHORITATIVE-CONTRACT AMENDMENT CANDIDATE ONLY; implementation NOT started.** It does not claim
the fix is implemented or that CF5-F003 is corrected/closed. It becomes authoritative only after Mandatory Grill → independent
external exact-candidate review → Owner exact-candidate acceptance → SHA-preserving publication → PR → pre-merge verification →
CREATE A MERGE COMMIT → post-merge verification. **Next required gate: INDEPENDENT EXTERNAL EXACT-CANDIDATE REVIEW OF THIS EXACT
CONTRACT AMENDMENT CANDIDATE** (this candidate has passed the Creator Mandatory Grill). After the amendment is authoritative, a fresh
CF5-F003 implementation candidate implementing §A3 (and §A6/§A8/§A9 evidence) is the subsequent gate.
