# P9-E2 / P9-PREREQ-B — Multi-Activated Domain Tie / Conflict Precedence — IMPLEMENTATION CONTRACT CANDIDATE

**Status of THIS record:** governance-only **CONTRACT CANDIDATE** — it becomes the authoritative implementation
contract-of-record only if independently reviewed, Owner-accepted, merged (create-a-merge-commit), and post-merge verified. It
defines the bounded scope, precedence-policy design, acceptance criteria, RED behavioral-test design, representation analysis, and
exact non-goals for a **later, separately-run** P9-E2 implementation gate. **No runtime change, no test change, no domain
activation, and no domain selection is performed or authorized by this contract-first gate.** **DOCUMENTED NO-VALID-RED /
CONTRACT-FIRST** (the RED tests are *designed* here, not implemented).

**Gate identifier.** `P9-E2` = `P9-PREREQ-B` — governed multi-activated-domain tie/conflict precedence (the D3-registered
prerequisite carried by the authoritative P9-QS §16; D3 formal-closure record §8). Trigger: **BEFORE more than one specialist
domain can be activated.**

**Authorization.** Owner authorization is **CONTRACT-FIRST ONLY.** This gate does **not** authorize: implementing P9-E2 runtime;
selecting or activating any new specialist domain; Mechanical or IoT activation; D4 execution; D8 disposition; deterministic
calculations; CAP-12 / CAP-13 / WS-PFV; STG; Output-Language; Phase 10; PSRR; deployment / production.

**Authoritative base.** `05184f9166fa3a9e45a3384be5bafccc86e05ebe` (live tip re-verified; PR #440 = two-parent merge of the P9-E1
implementation merge `f220850` + the P9-E1 formal-closure candidate `6c3c65a6`, merge tree `b8b5462f` == closure candidate tree;
**P9-E1 / P9-PREREQ-A is FORMALLY CLOSED / SATISFIED / AUTHORITATIVE**; boot OK; `activated_domains() == ['electronics_electrical']`).
Built in a disposable worktree; primary working tree + historical bundles untouched; not newer.
*(Baseline note: the Owner-supplied expected tip string was a 39-character transcription of this same PR #440 merge; the verified
40-character live tip above is authoritative and is the intended post-P9-E1-closure state — not a stale/forked baseline.)*

---

## §1. Live baseline and independently verified P9-E2 obligation

**The tie-precedence risk still exists (verified at `05184f91`).**

- **Exact location:** `engine/domain_rules.py::infer_domain` (def line 13), lines **31–33**:
  `activated_tied = sorted(d for d in tied if domain_activation.is_activated(d, _REGISTRY))` → `if activated_tied: return
  activated_tied[0]`. Picking `sorted(...)[0]` imposes **lexical/alphabetical** precedence among ACTIVATED tied domains — an
  incidental, ungoverned ordering, not a semantically justified precedence.
- **A second ungoverned literal (adjacent, in scope to disposition, not necessarily to fix here):** line **34**
  `priority = ["medical_device", "electronics_electrical", "mechanical", "software"]` — the no-activated-tie fallback. It runs only
  when **no** tied domain is activated; today (electronics the only activated domain) a tie among recognized-not-activated domains
  hits this hardcoded order. Per D3-D a non-activated inference cannot become effective activated routing/admission authority, but
  this literal is itself an incidental hardcoded preference and MUST be dispositioned by the contract (see §7 Case 3 / §17).
- **Exact conditions to execute the risky activated-tie path:** **two or more ACTIVATED specialist domains** whose classification
  scores **tie** at the best score for a given idea text.
- **Only one activated specialist domain currently:** `domain_activation._ACTIVATED_DOMAINS == frozenset({"electronics_electrical"})`;
  `activated_domains() == ['electronics_electrical']`. Therefore `activated_tied` has **at most one** element today, and the
  selection is deterministic and never ambiguous — **the risky path is UNREACHABLE at the current authoritative state.**
- **Reachable only when >1 specialist domain is activated:** confirmed by the logic — an incidental choice requires ≥2 tied
  activated domains.
- **Classification / activation / composition / routing are distinct:** classification/inference = `infer_domain` (evidence →
  candidate); activation = `engine/domain_activation.py` (`support_state` / `is_activated`, the §5-I2 allowlist); routing = the
  single-domain result consumed by `web/app.py:1363` and `scripts/run_cli.py:35`; composition = D4 (separate, not present).
  `infer_domain` already *consumes* the activation policy for its tie-break (D3-D) but does not duplicate it.

**Behavioral proof (executed read-only at `05184f91`; NO real activation, NO file change — `_ACTIVATED_DOMAINS` monkeypatched in a
throwaway process and restored).** Clean tie `"gear and catheter"` → scores `{electronics:0, mechanical:1, medical_device:1,
software:0}`. Baseline (only electronics activated): `infer_domain` → `medical_device` (via the `priority` literal, since neither
tied domain is activated). Simulating **mechanical + medical_device both activated**: `infer_domain` → **`mechanical`** =
`sorted(['mechanical','medical_device'])[0]` — the alphabetically-first, with **no semantic justification** (incidental
precedence). Simulating **electronics + medical_device activated** on `"circuit and catheter"` → `electronics_electrical` — again
purely because it sorts first, not via any governed Electronics preference. **Conclusion: P9-E2 IS STILL REQUIRED** (the gap is
live-in-code and becomes reachable the moment a second specialist domain is activated).

---

## §2. Precise problem definition (concepts the implementation MUST keep distinct)

- **A. Recognition** — a domain may exist in the registry without being activated; recognition MUST NOT imply runtime eligibility
  (`support_state` → `RECOGNIZED_NOT_ACTIVATED`).
- **B. Activation** — only ACTIVATED specialist domains may participate in activated-domain precedence (§5-I2 allowlist).
- **C. Classification / inference** — identifying one or more plausible domains from evidence; NOT activation.
- **D. Tie** — two or more **activated** domains equally plausible under the current inference score/rules.
- **E. Conflict** — a tie may mean: equally strong candidates; insufficient evidence; conflicting evidence; overlapping scope; or a
  genuinely multi-domain invention. The implementation MUST NOT silently pretend these are the same situation.
- **F. Composition** — true multi-domain activated composition belongs to **D4** and MUST remain separate; P9-E2 MUST NOT
  implement D4.

---

## §3. Core product-safety question and forbidden answers

**Question:** when two or more activated specialist domains tie or conflict, what is the truthful and deterministic behavior?

**The answer MUST NOT be:** alphabetical order; file order; registration order; arbitrary iteration order; incidental dictionary
ordering; hardcoded preference for Electronics; model guess; silent default; hidden fallback. **Any precedence MUST be explicitly
governed, deterministic, and explainable.**

---

## §4. Architecture investigation — canonical owner (reuse, do not duplicate)

The canonical owner of domain classification/precedence is **`engine/domain_rules.py::infer_domain`**, which already consumes the
canonical activation policy (`engine/domain_activation.py`, §5-I2) and the canonical Domain Registry
(`engine/domain_registry.py`, §5-I1). **P9-E2 SHALL extend this existing owner** with a small, explicit, governed precedence/
ambiguity policy. P9-E2 SHALL **NOT** create: a second Domain Registry; a second activation engine; a second domain router; a
global orchestration framework; or a duplicate scoring system. If implementation evidence shows the existing owner cannot host
the policy without such duplication, **STOP and report** rather than introducing a parallel owner.

---

## §5. Precedence policy design (the four states)

- **Case 1 — one activated candidate clearly wins:** the existing deterministic inference selects it. **Unchanged.**
- **Case 2 — multiple activated candidates tie AND an explicit governed precedence exists:** use precedence ONLY if it is
  explicit, versioned/otherwise governed, deterministic, testable, independent of incidental ordering, and semantically
  justified. (No such governed precedence exists today; defining one is a governed decision, not an engineering default — see
  §10/§17. Absent an Owner-approved precedence table, Case 2 collapses into Case 3.)
- **Case 3 — multiple activated candidates tie AND no explicit precedence exists:** the safe behavior MUST be an **explicit
  ambiguous / unresolved outcome** (return/record an explicit ambiguous state; preserve the tied activated candidate set for later
  governed handling; do NOT silently choose one). This is the required default because no governed precedence table exists at
  contract time.
- **Case 4 — evidence suggests a genuine multi-domain invention:** MUST NOT be collapsed into single-domain selection merely to
  satisfy a return type. If true multi-domain composition is required, **surface the need for D4** (record the multi-domain
  candidate set truthfully); P9-E2 does NOT implement D4.

**Recommended P9-E2 behavior (subject to the representation analysis in §6):** replace the incidental `sorted(activated_tied)[0]`
with an **explicit ambiguity outcome** for any ≥2-activated tie that has no Owner-governed precedence — i.e. Case 3 as the safe
default — while preserving Case 1 unchanged. Introducing a governed precedence table (Case 2) is deferred to a separate Owner
decision and MUST NOT be invented by the implementation.

---

## §6. Canonical state / result semantics — representation analysis (critical finding)

`infer_domain` currently returns **`str | None`** (a single domain id, or `None` when nothing matched). This return type **cannot
truthfully express**: (i) an ambiguous activated tie (distinct from "no match"); (ii) the tied activated candidate **set**;
(iii) a "no governed winner" outcome; (iv) a genuine multi-domain candidate set (Case 4). Collapsing any of these into a single
`str` (incidental pick) or into `None` (conflating "ambiguous tie among activated domains" with "no domain matched") would be
**semantically dishonest** and would violate §9 truthfulness.

**Therefore the honest resolution of P9-E2 requires a BOUNDED, SEPARATELY-REVIEWED representation extension** so the inference
seam can express `{single | ambiguous-tie(candidate set, reason) | none | multi-domain-needs-D4(candidate set)}`. This contract
**explicitly calls this out as a prerequisite sub-gate** rather than hiding it:

- **P9-E2-R (representation sub-gate) — bounded inference result/state extension.** A small, additive, backward-compatible
  extension of the inference result contract (e.g. a structured result object or an explicit sentinel distinct from `None`) that
  can carry: resolved single domain; ambiguous-tie + tied activated candidate set + ambiguity reason; no-match; and a
  multi-domain-needs-D4 marker. It MUST preserve every current caller's single-domain behavior for Case 1 and MUST NOT expand
  Domain-Pack schemas or persistence. **P9-E2-R is separately reviewed** (it changes a runtime contract shape) and is a
  prerequisite for the honest Case-3/Case-4 behavior. If, during implementation, P9-E2-R cannot be kept bounded/additive, **STOP
  and report** (do not force a broad schema migration under P9-E2).

*(A strictly minimal fallback — returning `None` on an ungoverned activated tie — is NOT recommended as the closure behavior
because it conflates two distinct truths and yields no provenance; it is recorded only as the degenerate lower bound. The contract
requires the P9-E2-R representation so ambiguity is expressed honestly.)*

---

## §7. Technical truthfulness requirements

P9-E2 MUST preserve: recognition ≠ activation; classification ≠ activation; ambiguity ≠ selection; multi-domain evidence ≠
composition authorization; insufficient evidence ≠ deterministic confidence. **No LLM-based tie-breaking.** **No fabricated /
unsupported confidence.** The ambiguity outcome MUST be deterministic and reproducible.

---

## §8. Engineering evidence / provenance (minimum for explainability — designed, not implemented here)

For any tie/conflict outcome to be auditable and explainable, the future decision SHOULD be able to record the **minimum**
evidence: the **activated candidate set** considered; the **best score** and per-candidate score basis (matched
classification signals); the **precedence rule applied** (or "none — ambiguous"); the **ambiguity reason** (equal-score /
insufficient-evidence / overlapping-scope / multi-domain); and the **version/identity of the domain-rule owner**. This provenance
is *designed* here; **no provenance expansion is implemented in this contract task.** Provenance MUST NOT be persisted or
schema-expanded beyond what a bounded P9-E2-R result object can carry.

---

## §9. Boundary with D4 (explicit)

P9-E2 solves **deterministic tie/conflict handling among activated domain candidates**. It does **NOT**: implement simultaneous
multi-domain analysis; combine Domain Packs; reconcile cross-domain contradictions; merge outputs; or decide shared ownership of
cross-domain gaps — those belong to **D4** (or a later governed capability). If a tie represents a genuine multi-domain
composition need, P9-E2 **records/returns that truthfully** (Case 4 marker) rather than silently choosing one domain or performing
composition.

## §10. Boundary with D8 (explicit)

`domains/iot_electronics/**` remains **Owner-reserved**. P9-E2 MUST NOT: activate IoT; select IoT as the next domain;
normalize/migrate/delete/reuse IoT content; or decide D8.

## §11. First-future-new-domain-activation implication (verified; recorded)

**Electronics is already activated.** Activating the **first** new non-electronics specialist domain would create a state with
**more than one** activated specialist domain, immediately making the §1 tie path reachable. **Therefore P9-E2 / P9-PREREQ-B is a
MANDATORY prerequisite before the first actual new-domain activation gate.** (Recorded per Owner instruction; **no activation is
performed or authorized here.**)

---

## §12. RED behavioral test design (designed here; IMPLEMENTED ONLY at the later gate)

Behavioral tests (assert selection/ambiguity behavior, not source text). Activated multi-domain ties are simulated with a
**bounded, self-restoring test double** of the §5-I2 activation set (e.g. patch `domain_activation._ACTIVATED_DOMAINS` within the
test and restore) using **repository-recognized** packs (`mechanical`, `medical_device`) as neutral fixtures — **NO real new
domain is activated**, and the activation policy file is never modified. Proposed location:
`tests/test_p9e2_multi_activated_tie_precedence.py`.

- **RED-1 — incidental/alphabetical precedence exposure.** With two activated domains tied at best score (e.g. `mechanical` +
  `medical_device` on `"gear and catheter"`), assert the result is **not** a silent alphabetical pick (`mechanical`) — it must be
  the explicit ambiguous outcome (Case 3). Fails on the live baseline (`sorted(...)[0]` returns `mechanical`).
- **RED-2 — stable deterministic behavior.** Repeated runs and equivalent candidate-order permutations (registry insertion order /
  input phrasing that preserves the tie) MUST yield the **same** outcome. Fails if the result depends on incidental ordering.
- **RED-3 — no hidden Electronics favoritism.** A tie **involving** Electronics (e.g. `electronics_electrical` + `medical_device`)
  MUST NOT automatically choose Electronics unless an explicit governed policy says so — it must be the ambiguous outcome. Fails on
  baseline (Electronics wins by alphabetical coincidence).
- **RED-4 — recognition-only exclusion.** A `recognized_not_activated` domain MUST NOT participate in activated-domain precedence
  (only activated domains form the tie set). Guards D3-D; must remain green through the change.
- **RED-5 — ambiguity honesty.** When no governed precedence exists, the outcome MUST be an explicit unresolved/ambiguous state
  (distinct from "no domain matched" and from any single-domain pick) — it MUST NOT fabricate a winner. Fails on baseline.
- **RED-6 — D4 boundary.** A genuine multi-domain scenario MUST be surfaced as a multi-domain/ambiguous outcome (needs-D4 marker),
  NOT falsely collapsed into single-domain composition logic. Fails on baseline (collapsed to one `str`).

All RED tests MUST fail on the live baseline for the stated behavioral reason (incidental precedence / dishonest collapse), not by
source-string inspection, and become GREEN only after the bounded P9-E2 (+ P9-E2-R) implementation.

## §13. Regression guards (future implementation)

Future tests MUST preserve: Electronics-only current behavior (Case 1 single winner unchanged); current recognized-not-activated
behavior (D3-D); single activated-winner behavior; no Domain Registry regression; no activation-policy regression; **no P9-E1
Path-N regression**; **no D4 work**; **no D8 change**.

---

## §14. Phase-9 mandatory completeness checklist (all 10 areas dispositioned)

1. **Engineering knowledge quality / correctness of domain questions/gaps:** `NOT APPLICABLE` — P9-E2 governs tie/conflict
   precedence among activated domains, not domain knowledge content.
2. **Technical truthfulness / known-unknown / no unsupported certainty:** `APPLICABLE / PASS (by design)` — the contract mandates
   an explicit ambiguous/unresolved outcome instead of a fabricated winner; enforced by RED-1/RED-5 at implementation.
3. **Specialization without shared-core coupling / no recurring domain `if/elif`:** `APPLICABLE / PASS (by design)` — extends the
   existing canonical owner with a general (domain-agnostic) precedence/ambiguity policy; no per-domain branching, no second
   router (§4).
4. **Rigorous pre-activation qualification (positive/negative/ambiguous/boundary/safety + regression):** `APPLICABLE / PASS (by
   design)` — RED-1…RED-6 cover positive (single winner), negative (recognition-only excluded), ambiguous (tie), boundary
   (Electronics-involved tie), and regression guards (§13). Full pre-activation domain qualification remains a separate domain
   qualification gate.
5. **Cross-domain interaction/composition, ownership, provenance, duplicate prevention, contradiction handling, no silent
   overwrite/hidden precedence:** `APPLICABLE / PASS (by design)` for the *no-hidden-precedence* and *no-silent-overwrite* aspects
   (the core of P9-E2); true cross-domain **composition/contradiction reconciliation** is `DEFERRED TO D4`. P9-E2 surfaces the
   multi-domain need (Case 4) rather than performing composition.
6. **Materials/manufacturing/prototype extensibility:** `DEFERRED TO CAP-12 / CAP-13 / WS-PFV` (their owners are untouched).
7. **Deterministic engineering calculations / units / provenance / reproducibility:** `DEFERRED TO SEPARATE GOVERNED FUTURE GATE`
   (no calculation capability here).
8. **Trustworthy knowledge sources / licensing / provenance / version control:** `DEFERRED TO DOMAIN QUALIFICATION AND FUTURE
   KNOWLEDGE-SOURCE GOVERNANCE` (the D13 family); untouched by P9-E2.
9. **Long-term Nth-domain extensibility:** `APPLICABLE / PASS (by design)` — a governed, domain-agnostic tie/ambiguity policy plus
   the bounded P9-E2-R result shape lets future domains be added via packs/rules/activation without recurring shared-core redesign
   of precedence.
10. **End-to-end disciplined engineering reasoning chain:** `APPLICABLE / PASS FOR P9-E2 SCOPE (by design)` — the classification
    step no longer silently substitutes an incidental winner; ambiguity/insufficient-evidence/multi-domain are represented
    truthfully so downstream reasoning is not built on a fabricated single-domain premise.

**No `APPLICABLE / GAP` remains for P9-E2** (contract-first). The only representation dependency (§6, P9-E2-R) is explicitly
called out as a bounded, separately-reviewed sub-gate — not an unresolved gap.

---

## §15. Acceptance criteria (implementation gate — testable minimum)

1. No incidental/alphabetical precedence among activated tied domains (`sorted(activated_tied)[0]` removed/replaced).
2. Deterministic behavior independent of candidate ordering (registry/input permutations yield the same outcome).
3. Explicit ambiguity behavior when no governed winner exists (distinct, not a silent pick, not conflated with "no match").
4. `recognized_not_activated` domains excluded from activated-domain precedence (D3-D preserved).
5. Activation semantics unchanged (`engine/domain_activation.py` / `_ACTIVATED_DOMAINS` untouched).
6. No new domain activated (`activated_domains() == ['electronics_electrical']` unchanged) and no domain selected.
7. Electronics current behavior preserved (Case 1 single-winner outcomes identical; P9-E1 Path-N unaffected).
8. No new shared-core domain-specific `if/elif` branching (policy is domain-agnostic).
9. No duplicate router / registry / scoring owner introduced (extend the existing owner only).
10. Provenance/explainability sufficient for the chosen outcome (activated candidate set + score basis + rule-applied/ambiguity
    reason available via the bounded P9-E2-R result).
11. D4 boundary preserved (no composition/merge/contradiction reconciliation; multi-domain need surfaced truthfully).
12. D8 untouched (`domains/iot_electronics/**` unchanged; no IoT decision).
13. P9-E1 remains intact (Path-N caller propagation regression-guarded).
14. Full focused **RED→GREEN** (RED-1…RED-6 red on baseline, green after the fix; ≥1 load-bearing mutation probe per governed
    decision point).
15. Full regression suite green (baseline 2264 passed / 3 skipped / 1 xfailed / 0 failed; delta explained by new tests only).
16. Nth-domain extensibility preserved (adding a domain requires packs/rules/activation/tests, not shared-core precedence
    redesign).
17. No hidden single-domain collapse of genuine multi-domain evidence (Case 4 surfaced, not collapsed).
18. Closure truthfulness / no unsupported engineering certainty (ambiguity and insufficient-evidence represented honestly).
19. *(Live-evidence addition.)* The **P9-E2-R** representation change, if used, is bounded, additive, backward-compatible, and
    **separately reviewed**; the `priority` no-activated-tie literal (line 34) is explicitly dispositioned (retained as a
    D3-D-guarded backward-compatible non-activated fallback, or governed) — not left as an undocumented incidental order.

Add any further criteria required by live evidence at the implementation gate.

---

## §16. Scope boundaries for the future implementation (identified from live evidence)

Likely canonical owner: **`engine/domain_rules.py`** (the `infer_domain` tie/precedence logic) plus the bounded **P9-E2-R** result
representation and **focused tests** (`tests/test_p9e2_multi_activated_tie_precedence.py`), and — only if repository precedent
requires — governance current-truth registration. Callers `web/app.py:1363` and `scripts/run_cli.py:35` may need a **minimal,
backward-compatible** adaptation to consume the P9-E2-R result (single-domain behavior preserved); this is expected to be small
and MUST be justified by evidence at the implementation gate, not pre-authorized broadly.

**HARD STOP** (report, do not proceed) if the implementation would require: domain activation; D4; Domain-Pack redesign; a new
global orchestrator; schema migration beyond a bounded, separately-reviewed representation change (P9-E2-R); or any D8 change.

---

## §17. Candidate-vs-authoritative boundary

**P9-E2 = CONTRACT CANDIDATE ONLY** (contract-first). It becomes the authoritative implementation contract-of-record only if this
exact accepted candidate is independently reviewed, Owner-accepted, merged (create-a-merge-commit), and post-merge verified. The
P9-E2 **runtime implementation, the P9-E2-R representation sub-gate, and their tests are separate, later, separately-run gates —
NOT authorized here.** **NO domain is activated or selected here.** Governance scope of this candidate: this NEW contract doc +
`ACTIVE_EXECUTION_ROADMAP.md` (append-only) + `ACTIVE_INCREMENT_CONTRACT.md` + `CURRENT_PROJECT_STATE.md` current-truth sync;
**`OWNER_DECISION_REGISTER.md` UNCHANGED**; **ZERO** runtime/test/domain/schema/prompt/benchmark/web/CI diff. P9-E1 remains
FORMALLY CLOSED / SATISFIED; D4 separate/unexecuted; D8 Owner-reserved; Phase 10 NOT AUTHORIZED; PSRR NOT EXECUTED; deployment /
production NOT AUTHORIZED.
