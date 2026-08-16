# L2SC-01 — Substance-Signal Plural-Alias Domain-Completeness — Bounded Implementation Contract (governance-only; implements nothing; MATERIAL CORRECTION of rejected candidate `219f7c1`)

**Status of THIS record:** governance/documentation-only **CONTRACT CANDIDATE**, superseding rejected candidate
`219f7c10c4ba23f795f0461dd831f71052469e65` (preserved immutable at `refs/rejected/l2sc01-plural-alias-contract-
219f7c1`; independent review verdict: REJECT — MATERIAL CORRECTION REQUIRED, defect MD-1: the rejected candidate
authorized Mechanical plural aliases using "is this a normal English plural" alone, without screening for verb-
form/idiom/meaning-shift false-positive risk). It implements nothing in this gate — no runtime, domain-pack,
registry-validator, test, schema, or persistence change. **`OWNER_DECISION_REGISTER.md` UNCHANGED.**

## §1. Authoritative base and fresh verification

Base: `c8e7af24adf2cee31104abc9c810d38e05569c52` (PR #495 — SHA-preserving merge of the accepted CF-2 full-scope
formal closure candidate `4b45a3e` onto `6c168a6`; merge tree `3a28cc96` == candidate tree; POST-MERGE PASS;
freshly re-fetched this gate; 0 newer; clean tree) — `CF-2 = FORMALLY CLOSED`, `CF-6 = FULLY DISCHARGED`; full
governed suite **2616 passed / 3 skipped / 1 xfailed / 0 failed** (fresh re-verification this gate, unchanged).

## §2. What independent review accepted — not reopened

The reconstruction, the domain-generic substance-signal finding, the exact hardcoded-map gap, the WARN/PASS
divergence proof, the rejection of Option A (would reopen §5-I1's closed element-shape-validation surface) and
Option C (shared-core coupling), the selection of **Option B** (top-level, pack-scoped
`substance_signal_plural_aliases`, mirroring the existing pack-level `aliases` precedent), electronics
migration, the `L2SC-02` registration, and every protected boundary (CF-2/CF-6/ILT-002/L10N-RH-01/Tier-1/
Mechanical/Phase 9) are **unchanged and not re-derived here**. This contract corrects exactly the alias-safety
defect (MD-1) and the accuracy defects it exposed (§8-§10 below); it does not restart the reconstruction.

## §3. MD-1 — corrected Mechanical alias-safety criterion

The rejected candidate's test was **"is this the grammatically normal plural of an authorized signal?"** —
insufficient, because a plural surface form can independently function as a common third-person verb, a fixed
idiom, or a materially different lexical meaning, any of which can appear inside an otherwise generic-verb-trap
response and incorrectly rescue it toward `REASONED`/`PASS` without the text actually establishing Mechanical
substance. The corrected, authoritative criterion:

> A candidate alias is authorized only when its observed surface form is acceptably safe in the Layer-2
> matching context — i.e. it is not a common verb form, established idiom, or other predictable non-substance
> meaning of comparable prominence to the electronics precedent's own excluded forms ("hall", "chip", "display",
> "esp"). The existence of a normal English plural is NOT sufficient for authorization. Explicit aliases are a
> manually governed exception list whose purpose is safe recognition, not linguistic completeness;
> under-recognition is preferred over any false-positive path that can alter progression truth.

## §4. Full Mechanical alias reclassification (all 15 current `mechanical` substance signals)

Categories: **A** = safe explicit alias (authorize); **B** = ambiguous surface form (exclude); **C** = no
natural count-plural (exclude); **D** = meaning-shift/idiom risk (exclude); **E** = other.

| Signal | Candidate plural | Class | Evidence |
|---|---|---|---|
| `piston` | pistons | **A** | No verb form of "piston" in standard English; no established idiom located. Empirically re-verified: a clean qualifying sentence using only "pistons" (no other substance word present) currently yields `ASSERTED` where the singular "piston" yields `REASONED` — reproduces the exact target gap. |
| `spring` | springs | **D** | "springs" is a common third-person verb ("the trap springs shut", "he springs into action", "springs open") — high collision risk directly inside causal sentences of the kind this gate matches. |
| `valve` | valves | **A** | No verb form of "valve"; no idiom collision found. "Release valve" is a live metaphor but stays conceptually tied to the same physical mechanism concept (comparable to the registry's own accepted cross-domain use of "pressure"), not an unrelated meaning-shift. Empirically re-verified with a clean sentence (no other substance word present): plural fails, singular passes — reproduces the target gap. |
| `gear` | gears | **D** | "gears up" is a common idiom (prepares/intensifies); "gears" also functions informally as a verb. Independent-review-demonstrated example ("the plant gears up") confirmed. |
| `lever` | levers | **D** | "levers of power/influence" is an established political/business idiom, unrelated to the mechanical component. |
| `hydraulic` | hydraulics | **D** | Adjectival; the plural shifts meaning to the field-of-study noun ("hydraulics" the discipline), not a countable-instance plural — same ambiguity class as the Owner's existing "hall"/"chip"/"display"/"esp" exclusions. |
| `pneumatic` | pneumatics | **D** | Same reasoning as `hydraulic`. |
| `pressure` | pressures | **C, D** | Mass/non-count noun in its technical sense; "pressures" commonly means distinct readings or, idiomatically, "under pressures" (stress) — an unrelated meaning-shift. |
| `torque` | torques | **C** | Mass noun / single measurable quantity in technical usage; "torques" is not idiomatic English in this context and no true count-plural use was found. |
| `compression` | compressions | **D** | Independent review correctly noted Option B is pack-scoped, so cross-PACK leakage is not the actual risk (§10 corrects the rationale). The real risk survives pack-scoping: within an ACTIVE Mechanical session, a user's free-text can still use "compressions" in its far more common ordinary-English sense ("chest compressions", CPR) without establishing any Mechanical substance — an intra-session lexical-ambiguity risk, not a cross-domain one. |
| `seal` | seals | **D** | "seals" is a common third-person verb ("the gasket seals the joint") — independent-review-demonstrated example confirmed, high collision risk in exactly this causal-sentence context. |
| `bearing` | bearings | **D** | "loses their bearings" is a well-established idiom (disorientation), unrelated to the mechanical component — independent-review-demonstrated example confirmed. |
| `actuator` | actuators | **A** | Purely technical term; no verb form; no idiom located. Empirically re-verified with a clean sentence: plural fails, singular passes — reproduces the target gap. |
| `mechanism` | mechanisms | **B** | Re-examined and RECLASSIFIED from the rejected candidate's inclusion. `mechanism` already carries a pre-existing, Owner-flagged `AB-006` "LOW SPECIFICITY" caveat on its own singular form. Its plural appears heavily in generic, non-substantive usage ("coping mechanisms", "mechanisms of action") that is exactly the shape of vacuous-but-plausible-sounding text the Layer-2 gate exists to screen out. Given the corrected §3 criterion and the "under-recognition is preferred" principle, this is excluded here; the pre-existing AB-006 note is independent evidence the Owner may still choose to authorize it at contract-acceptance time without affecting the other 3. |
| `friction` | frictions | **C, D** | Mass/non-count noun in technical usage; "frictions" commonly means interpersonal/political tensions ("trade frictions") — an unrelated meaning-shift, and not idiomatic in the mechanical technical sense either way. |

**Exact approved alias set (3 of 15):** `piston`→`pistons`, `valve`→`valves`, `actuator`→`actuators`.

**Exact excluded alias set (12 of 15):** `spring`, `gear`, `lever`, `hydraulic`, `pneumatic`, `pressure`,
`torque`, `compression`, `seal`, `bearing`, `mechanism`, `friction` — each with its own evidence row above.

**Outcome-sensitivity check (required by §12.H, performed before freezing, not assumed):** with only the 3
surviving safe aliases, the original WARN-vs-PASS class of defect is still concretely and cleanly reproduced —
verified this gate with clean qualifying sentences (containing no other substance word) for `piston`/`pistons`
and `actuator`/`actuators` in addition to the already-demonstrated `gear`/`gears` case from the rejected
candidate's own reconstruction evidence. The conservative review does **not** leave too few safe aliases to
meaningfully justify the future implementation; §12's STOP condition does not apply.

## §5. Option B confirmation (unchanged, restated)

`substance_signal_plural_aliases` remains the frozen architecture: optional, pack-scoped, additive-only,
mirroring the existing top-level `aliases` (pack-id) precedent in the same loader. Nested per-signal aliases
(Option A) and engine-hardcoded expansion (Option C) remain rejected for the reasons in the prior reconstruction
(not re-derived here).

## §6. Alias-map direction — stated consistently

The authoritative representation, used consistently everywhere in this document and required of the future
implementation: **alias → canonical signal**. Example: `"pistons": "piston"`. No canonical→alias arrow notation
is used anywhere in this contract.

## §7. Structural validation guarantees (what the canonical validator CAN enforce)

The future `engine/domain_registry.py` extension can deterministically, fail-closed enforce, on the ALREADY-
PARSED Python data structure: the field, if present, is a JSON object; every key is a non-empty string; every
value is a non-empty string; every value equals some element's `signal` value present in that SAME pack's
`substance_signals` list (dangling-target rejection); the field's absence is valid for every pack.

## §8. Semantic-validation limitation — stated truthfully (corrects the rejected candidate's overclaim)

Structural validation **cannot** prove that `"pistons": "piston"` is the semantically CORRECT pairing rather
than, say, `"pistons": "lever"` (a real, differently-canonical signal that would also pass structural
validation, since both `"piston"` and `"lever"` exist as signals somewhere in the pack). **Semantic correctness
of each explicit alias is governed entirely by the reviewed, Owner-accepted alias allow-list (§4) and by the
required tests (§12) — not by the validator.** No automatic morphology, stemming, or semantic inference is
introduced anywhere; the validator's guarantee is structural integrity only, never semantic correctness.

## §9. Duplicate-JSON-key claim — corrected (the rejected candidate's inaccurate statement is withdrawn)

The rejected candidate stated that conflicting duplicate JSON keys within one pack's alias map "cannot be
represented... at the JSON level" — **this is inaccurate and is withdrawn.** Standard JSON parsing (Python's
`json.load`, used unchanged by `engine/domain_registry.py`) resolves duplicate object keys with **last-value-
wins** at parse time, silently, before any validator ever sees the data. This is a **pre-existing characteristic
of the entire loader**, equally true of every other JSON object in every domain pack today (e.g. a duplicated
top-level key, or a duplicated `signal` key inside one `substance_signals` element) — it is not introduced,
worsened, or newly discovered by this contract's proposed field. Detecting raw duplicate keys before parsing
would require a custom `object_pairs_hook` (or equivalent) across the ENTIRE loader — a broader loader redesign
with its own cost/benefit tradeoff spanning every existing field, not something this narrow, bounded increment
is authorized or positioned to solve. It is explicitly classified **OUTSIDE this bounded increment**. What §7's
validator DOES deterministically enforce operates only on the already-parsed result (where duplicate-key
collisions, if any occurred, are already silently resolved by `json.load` and therefore invisible to it) — §7's
guarantees stand as stated, scoped to that parsed structure, not to the raw JSON source text.

## §10. Compression rationale — corrected (survives pack scoping)

The rejected candidate excluded `compression`/`compressions` using a cross-domain-leakage rationale ("chest
compressions" as a different PACK's concern) that independent review correctly identified as weakened by
Option B's actual pack-scoping (an alias registered under `mechanical` is only ever consulted when
`domain == "mechanical"`, so it cannot leak into a different pack's own matching). The CORRECTED rationale (§4
table) does not depend on cross-pack leakage at all: the risk is that a Mechanical-domain SESSION's free-text
can still use "compressions" in its ordinary-English, non-mechanical sense (CPR/chest compressions) without
establishing any genuine Mechanical substance — an intra-session lexical-ambiguity risk that exists regardless
of which pack the alias is scoped to. The exclusion stands, on corrected grounds.

## §11. Electronics migration — no-overlap evidence (independently re-verified this gate)

Confirmed by direct registry inspection this gate: **none of the 8 existing hardcoded electronics plural-alias
singulars (`sensor`, `relay`, `resistor`, `battery`, `capacitor`, `motor`, `led`, `ic`) appears as a `signal`
value in the `mechanical`, `medical_device`, or `software` domain packs.** Retiring the engine-hardcoded
`_SUBSTANCE_PLURAL_ALIASES` map in favor of migrating those 8 pairs into `electronics_electrical`'s own new
`substance_signal_plural_aliases` field therefore does not silently remove alias-recognition behavior that any
other domain pack currently relies on or shares.

## §12. Corrected test contract (supersedes the rejected candidate's §12/§10 `Required tests`)

**A. Electronics preservation.** Byte/behavior-identical output before and after migration (both via the new
registry-derived path and via removal of the retired hardcoded map).

**B. Mechanical approved-alias parity.** Only the 3 §4-authorized pairs (`piston`/`pistons`, `valve`/`valves`,
`actuator`/`actuators`): singular and plural produce identical Layer-2/`REASONED` classification in otherwise-
identical, clean qualifying sentences (no other substance word present, isolating the alias under test).

**C. Authorized-alias false-positive guards (new, mandatory).** For EACH of the 3 approved aliases, at least one
adversarial sentence using the SAME word in a plausible non-substance/ambiguous context, asserting it must NOT
gain `REASONED` solely from the alias match (e.g. a sentence where "pistons"/"valves"/"actuators" appears but
the sentence otherwise carries no genuine causal/mechanism substance and would be `ASSERTED` for any other
generic noun in that position) — proving the 3 survivors are not merely untested for risk, but actively verified
low-risk.

**D. Rejected-alias guards (new, mandatory).** For each of the 12 excluded forms, at minimum the independent-
review-demonstrated adversarial sentences (or an equivalent constructed case for forms without a reviewer-
supplied example): "the gasket seals the joint...", "the latch springs open...", "the operator loses their
bearings...", "the plant gears up...", plus at minimum one constructed case each for `lever` ("levers of
influence"), `hydraulic`/`pneumatic` (field-noun usage), `pressure` ("under pressures"), `compression` ("chest
compressions"), `friction` ("trade frictions"), `torque` (non-idiomatic rejection), `mechanism` ("coping
mechanisms") — each must demonstrate the excluded plural does NOT become Layer-2 substance evidence merely from
its surface word.

**E. No generic morphology.** No `s`/`es`/`ies` derivation is ever introduced; only the explicit §4 pairs match.

**F. Validation.** A dangling alias target (pointing to a signal absent from that same pack) is rejected by the
canonical validator, fail-closed.

**G. Cross-domain isolation.** A Mechanical alias must not become recognized as an Electronics substance signal
merely by existing in the Mechanical pack, and vice versa.

**H. Outcome sensitivity.** At least one of the 3 approved Mechanical aliases (§4 already performed this check
for `piston` and `actuator` this gate) must demonstrate, end-to-end through the real gap-closure state machine,
that the original singular/plural `WARN`-vs-`PASS` divergence is fixed for that pair.

**Full governed suite green**, in addition to all of the above.

## §13. Corrected mutation/adversarial probe contract (supersedes the rejected candidate's §13)

`__pycache__` cleared before each: (1) remove one authorized alias (e.g. `pistons`) from the registry data → the
corresponding parity test (§12.B) must go RED; (2) bypass the new registry-driven accessor and restore/hardcode
the OLD electronics-only map → a Mechanical parity test must go RED; (3) reintroduce generic suffix-stripping
(e.g. a blanket `-s` strip) → the false-positive guard tests (§12.C/D, mirroring the existing `ices`/`halls`/
`chips`/`displays` class) must go RED; (4) point an alias at a nonexistent canonical signal in a domain pack →
registry load must fail, and a load-failure test going missing/removed must itself go RED; **(5) NEW — introduce
one known-ambiguous excluded Mechanical alias (e.g. `"seals": "seal"` or `"gears": "gear"`) into the authorized
map** → the corresponding §12.D adversarial false-positive guard test must go RED. This fifth probe is mandatory
because it directly protects against a recurrence of MD-1. All mutations reverted, byte-verified restoration,
before freezing any future candidate.

## §14. Risk level and required lifecycle for the future implementation (unchanged, restated)

**HIGH-RISK.** Full lifecycle required: create → freeze exact SHA → Mandatory Grill → independent external
exact-candidate review → Owner exact-SHA acceptance → SHA-preserving publication → PR → pre-merge verification →
merge (create-a-merge-commit) → post-merge verification. **Fast Track is explicitly NOT authorized.**

## §15. L2SC-01 closure criteria (for the future implementation gate, not this contract)

L2SC-01 closes only when: the registry field + accessor + engine consumption are implemented exactly per this
contract's frozen scope (the 3-pair §4 authorized set, or a smaller/differently-justified set the future gate's
own review may further narrow — never a larger one without its own fresh alias-safety review); electronics
behavior is byte/behavior-identical (proven, not assumed); the exact WARN-vs-PASS divergence is proven closed
for the authorized pairs; every §12/§13 test and probe passes; full suite is green; independent review accepts
the exact frozen SHA; Owner accepts. This contract does NOT itself close L2SC-01, and does NOT claim the alias
set is linguistically complete — only that the authorized subset is safe.

## §16. L2SC-02 status (unchanged, not reopened)

Remains registered, distinct, non-implementing, not expanded or touched by this correction.

## §17. Non-effects (no over-closure, no over-authorization)

Identical to the rejected candidate's §16: ZERO runtime/test/pack/registry/activation/schema/persistence diff;
`CF-2`/`CF-6` not reopened; `D-CF6CF2-ILT002-01`/`L10N-RH-01` untouched; Tier-1 not implemented; Mechanical NOT
ACTIVATED; no D4/D8/THERM-01/Phase 10/PSRR/deployment; no P9 closure. Populating registry alias data in a future
gate does not itself activate Mechanical.

## §18. Whether an Owner architecture decision is required

**NO** — unchanged from the prior (accepted-on-this-point) determination; the alias-safety correction in this
document is a scope/data-safety narrowing, not an architecture question, and required no new competing-design
evaluation beyond §3-§4's stricter safety criterion.

## §19. Closure statement and scope of THIS candidate

Governance/documentation only: this REVISED contract (same canonical file path, corrected content, new SHA) +
`ACTIVE_EXECUTION_ROADMAP.md` (append-only) + `ACTIVE_INCREMENT_CONTRACT.md` + `CURRENT_PROJECT_STATE.md`
current-truth sync + a citation of the rejected SHA in the capability register's `L2SC-01` amendment.
`OWNER_DECISION_REGISTER.md` UNCHANGED. **ZERO runtime/test/pack/registry/activation/schema/persistence diff.**
Rejected candidate `219f7c10c4ba23f795f0461dd831f71052469e65` remains immutable, preserved at
`refs/rejected/l2sc01-plural-alias-contract-219f7c1`, unpushed, unamended. `CF-2 = FORMALLY CLOSED`, `CF-6 =
FULLY DISCHARGED`, `D-CF6CF2-ILT002-01` unchanged, Mechanical NOT ACTIVATED, Phase 9 OPEN — all unchanged.
**Next required gate: Mandatory Grill on this exact candidate**, then the governed lifecycle; thereafter, per
§14, the separately-authorized L2SC-01 bounded implementation gate.
